from __future__ import annotations

import hashlib
import io
import json
import struct

import pytest

from text_recognition_core.intake.envelope import inspect_source_bytes
from text_recognition_core.intake.raster_protocol import (
    MAGIC,
    RasterFrameReader,
    RasterProtocolError,
)

SOURCE = b"\x89PNG\r\n\x1a\npublic-source-envelope-only"
PIXELS = bytes((12, 34, 56, 78, 90, 12))


def header() -> dict[str, object]:
    return {
        "schema": 1,
        "source_sha256": hashlib.sha256(SOURCE).hexdigest(),
        "kind": "png",
        "width": 2,
        "height": 1,
        "pixel_format": "RGB8",
        "pixel_bytes": len(PIXELS),
        "pixel_sha256": hashlib.sha256(PIXELS).hexdigest(),
    }


def frame(raw_header: bytes | None = None, pixels: bytes = PIXELS) -> bytes:
    raw = raw_header if raw_header is not None else json.dumps(header()).encode("utf-8")
    return MAGIC + struct.pack(">I", len(raw)) + raw + pixels


def reader() -> RasterFrameReader:
    return RasterFrameReader(inspect_source_bytes(io.BytesIO(SOURCE)))


@pytest.mark.parametrize("chunk_size", [1, 2, 13, 257, 65536])
def test_fragmented_binary_raster_preserves_pixels_and_parent_provenance(chunk_size: int) -> None:
    parsed = reader()
    raw = frame()
    for start in range(0, len(raw), chunk_size):
        parsed.feed(raw[start : start + chunk_size])
    result = parsed.finish()
    assert result.pixels == PIXELS
    assert (result.width, result.height, result.kind) == (2, 1, "png")
    assert result.source_sha256 == hashlib.sha256(SOURCE).hexdigest()
    with pytest.raises(RasterProtocolError, match="^invalid_raster_protocol$"):
        parsed.finish()


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("schema", True),
        ("schema", 2),
        ("source_sha256", "0" * 64),
        ("kind", "jpeg"),
        ("width", True),
        ("width", 4097),
        ("height", 0),
        ("pixel_format", "RGBA8"),
        ("pixel_bytes", True),
        ("pixel_bytes", 7),
        ("pixel_sha256", "F" * 64),
        ("extra", "private-canary"),
    ],
)
def test_header_claim_cannot_override_parent_or_resource_contract(key: str, value: object) -> None:
    altered = header()
    altered[key] = value
    parsed = reader()
    with pytest.raises(RasterProtocolError, match="^invalid_raster_protocol$"):
        parsed.feed(frame(json.dumps(altered).encode("utf-8")))
    with pytest.raises(RasterProtocolError):
        parsed.feed(frame())
    with pytest.raises(RasterProtocolError):
        parsed.finish()


@pytest.mark.parametrize(
    "raw_header",
    [
        b"\xffprivate-canary",
        b"[]",
        b'{"schema":1,"schema":1}',
        b'{"schema":NaN}',
        b"[" * 2000 + b"]" * 2000,
        b"",
        b"x" * 4097,
    ],
)
def test_malformed_header_is_sanitized_and_never_returns_raster(raw_header: bytes) -> None:
    parsed = reader()
    with pytest.raises(RasterProtocolError, match="^invalid_raster_protocol$"):
        parsed.feed(frame(raw_header))
    with pytest.raises(RasterProtocolError):
        parsed.finish()


@pytest.mark.parametrize("cut", [0, 1, len(MAGIC), len(MAGIC) + 3, -1])
def test_truncated_frame_never_exposes_partial_pixels(cut: int) -> None:
    parsed = reader()
    parsed.feed(frame()[:cut])
    with pytest.raises(RasterProtocolError, match="^invalid_raster_protocol$"):
        parsed.finish()


def test_corrupt_pixel_digest_and_trailing_data_are_rejected() -> None:
    parsed = reader()
    parsed.feed(frame(pixels=b"x" * len(PIXELS)))
    with pytest.raises(RasterProtocolError):
        parsed.finish()
    parsed = reader()
    parsed.feed(frame())
    with pytest.raises(RasterProtocolError):
        parsed.feed(b"private-canary")
    with pytest.raises(RasterProtocolError):
        parsed.finish()


def test_unsupported_source_cannot_construct_a_decoder_reader() -> None:
    envelope = inspect_source_bytes(io.BytesIO(b"%PDF-public-envelope"))
    with pytest.raises(RasterProtocolError):
        RasterFrameReader(envelope)
