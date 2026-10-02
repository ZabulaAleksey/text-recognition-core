"""Standalone containment worker; Pillow is imported only inside decode_source."""

from __future__ import annotations

import hashlib
import io
import json
import struct
import sys
import warnings
from typing import Any, BinaryIO

MAGIC = b"TRCRASTER1\n"
MAX_SOURCE_BYTES = 64 * 1024 * 1024
MAX_DIMENSION = 4096
MAX_PIXELS = 16777216
MAX_PIXEL_BYTES = 50331648
MAX_HEADER_BYTES = 4096
FAILURE_CODES = frozenset(
    {
        "DECODER_RUNTIME_UNAVAILABLE",
        "DECODER_INPUT_INVALID",
        "DECODER_INPUT_LIMIT",
        "DECODER_PROFILE_UNSUPPORTED",
        "DECODER_GEOMETRY_LIMIT",
        "DECODER_DECODE_FAILED",
        "DECODER_OUTPUT_LIMIT",
    }
)


class WorkerFailure(Exception):
    def __init__(self, code: str) -> None:
        if code not in FAILURE_CODES:
            raise ValueError("invalid worker failure code")
        self.code = code
        super().__init__(code)


def read_source(stream: BinaryIO) -> bytes:
    buffer = io.BytesIO()
    while True:
        chunk = stream.read(min(65536, MAX_SOURCE_BYTES + 1 - buffer.tell()))
        if not chunk:
            break
        buffer.write(chunk)
        if buffer.tell() > MAX_SOURCE_BYTES:
            raise WorkerFailure("DECODER_INPUT_LIMIT")
    source = buffer.getvalue()
    if not source:
        raise WorkerFailure("DECODER_INPUT_INVALID")
    return source


def source_kind(source: bytes) -> str:
    if source.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if source.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    raise WorkerFailure("DECODER_INPUT_INVALID")


def validate_profile(image: Any, kind: str) -> tuple[int, int]:
    width, height = image.size
    if (
        type(width) is not int
        or type(height) is not int
        or not 1 <= width <= MAX_DIMENSION
        or not 1 <= height <= MAX_DIMENSION
        or width * height > MAX_PIXELS
    ):
        raise WorkerFailure("DECODER_GEOMETRY_LIMIT")
    if (
        image.format != {"png": "PNG", "jpeg": "JPEG"}.get(kind)
        or image.mode not in ("RGB", "L")
        or getattr(image, "n_frames", 1) != 1
        or "exif" in image.info
        or "icc_profile" in image.info
        or "transparency" in image.info
        or image.getexif()
    ):
        raise WorkerFailure("DECODER_PROFILE_UNSUPPORTED")
    return width, height


def frame_header(source: bytes, kind: str, width: int, height: int, pixels: bytes) -> bytes:
    if (
        type(width) is not int
        or type(height) is not int
        or not 1 <= width <= MAX_DIMENSION
        or not 1 <= height <= MAX_DIMENSION
        or width * height > MAX_PIXELS
    ):
        raise WorkerFailure("DECODER_GEOMETRY_LIMIT")
    if kind not in ("png", "jpeg"):
        raise WorkerFailure("DECODER_INPUT_INVALID")
    if len(pixels) != 3 * width * height or len(pixels) > MAX_PIXEL_BYTES:
        raise WorkerFailure("DECODER_OUTPUT_LIMIT")
    header = json.dumps(
        {
            "schema": 1,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "kind": kind,
            "width": width,
            "height": height,
            "pixel_format": "RGB8",
            "pixel_bytes": len(pixels),
            "pixel_sha256": hashlib.sha256(pixels).hexdigest(),
        },
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    if len(header) > MAX_HEADER_BYTES:
        raise WorkerFailure("DECODER_OUTPUT_LIMIT")
    return MAGIC + struct.pack(">I", len(header)) + header


def decode_source(source: bytes) -> tuple[str, int, int, bytes]:
    kind = source_kind(source)
    from PIL import Image, ImageFile

    Image.MAX_IMAGE_PIXELS = MAX_PIXELS
    ImageFile.LOAD_TRUNCATED_IMAGES = False
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        with Image.open(io.BytesIO(source), formats=("PNG", "JPEG")) as image:
            width, height = validate_profile(image, kind)
            image.load()
            # Loading may expose additional frame/profile information; recheck.
            validate_profile(image, kind)
            if image.mode == "L":
                with image.convert("RGB") as expanded:
                    pixels = expanded.tobytes()
            else:
                pixels = image.tobytes()
    return kind, width, height, pixels


def main() -> int:
    try:
        if not (3, 13) <= sys.version_info[:2] < (4, 0):
            raise WorkerFailure("DECODER_RUNTIME_UNAVAILABLE")
        source = read_source(sys.stdin.buffer)
        kind, width, height, pixels = decode_source(source)
        header = frame_header(source, kind, width, height, pixels)
    except WorkerFailure as error:
        sys.stderr.buffer.write((error.code + "\n").encode("ascii"))
        return 1
    except Exception:
        sys.stderr.buffer.write(b"DECODER_DECODE_FAILED\n")
        return 1
    try:
        sys.stdout.buffer.write(header)
        sys.stdout.buffer.write(pixels)
        sys.stdout.buffer.flush()
    except OSError:
        # Transport failure may leave partial bytes; parent discards the frame.
        sys.stderr.buffer.write(b"DECODER_DECODE_FAILED\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
