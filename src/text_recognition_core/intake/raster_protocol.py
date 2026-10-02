"""Incremental bounded worker framing with independently bound input provenance."""

from __future__ import annotations

import hashlib
import json
import struct
from typing import Any, cast

from text_recognition_core.application.raster import (
    MAX_DIMENSION,
    MAX_PIXEL_BYTES,
    MAX_PIXELS,
    DecodedRaster,
    RasterKind,
)
from text_recognition_core.intake.envelope import SourceByteEnvelope

MAGIC = b"TRCRASTER1\n"
MAX_HEADER_BYTES = 4096
MAX_FRAME_BYTES = len(MAGIC) + 4 + MAX_HEADER_BYTES + MAX_PIXEL_BYTES
HEADER_FIELDS = frozenset(
    {
        "schema",
        "source_sha256",
        "kind",
        "width",
        "height",
        "pixel_format",
        "pixel_bytes",
        "pixel_sha256",
    }
)


class RasterProtocolError(ValueError):
    def __init__(self) -> None:
        super().__init__("invalid_raster_protocol")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RasterProtocolError
        result[key] = value
    return result


def _reject_constant(_: str) -> Any:
    raise RasterProtocolError


class RasterFrameReader:
    """One frame, no result until explicit EOF and all digest checks pass."""

    def __init__(self, expected: SourceByteEnvelope) -> None:
        if expected.kind not in ("png", "jpeg"):
            raise RasterProtocolError
        self._expected = expected
        self._prefix = bytearray()
        self._header: dict[str, Any] | None = None
        self._pixels = bytearray()
        self._digest = hashlib.sha256()
        self._received = 0
        self._closed = False

    def feed(self, chunk: bytes) -> None:
        try:
            self._feed(chunk)
        except RasterProtocolError:
            self._closed = True
            self._prefix.clear()
            self._pixels.clear()
            raise

    def _feed(self, chunk: bytes) -> None:
        if (
            self._closed
            or type(chunk) is not bytes
            or self._received + len(chunk) > MAX_FRAME_BYTES
        ):
            raise RasterProtocolError
        self._received += len(chunk)
        if self._header is not None:
            self._append_pixels(chunk)
            return
        # Never allocate an attacker-sized prefix: only magic/length/header fit here.
        prefix_limit = len(MAGIC) + 4 + MAX_HEADER_BYTES
        take = min(len(chunk), prefix_limit - len(self._prefix))
        self._prefix.extend(chunk[:take])
        magic_length = min(len(self._prefix), len(MAGIC))
        if self._prefix[:magic_length] != MAGIC[:magic_length]:
            raise RasterProtocolError
        if len(self._prefix) < len(MAGIC) + 4:
            return
        header_size = struct.unpack(">I", self._prefix[len(MAGIC) : len(MAGIC) + 4])[0]
        if not 0 < header_size <= MAX_HEADER_BYTES:
            raise RasterProtocolError
        end = len(MAGIC) + 4 + header_size
        if len(self._prefix) < end:
            return
        self._parse_header(bytes(self._prefix[len(MAGIC) + 4 : end]))
        buffered_pixels = bytes(self._prefix[end:])
        self._prefix.clear()
        self._append_pixels(buffered_pixels)
        self._append_pixels(chunk[take:])

    def _parse_header(self, raw: bytes) -> None:
        try:
            header = json.loads(
                raw.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_constant=_reject_constant,
            )
            if type(header) is not dict or set(header) != HEADER_FIELDS:
                raise RasterProtocolError
            if (
                type(header["schema"]) is not int
                or header["schema"] != 1
                or header["source_sha256"] != self._expected.sha256_hex
                or header["kind"] != self._expected.kind
                or header["pixel_format"] != "RGB8"
                or type(header["width"]) is not int
                or type(header["height"]) is not int
                or not 1 <= header["width"] <= MAX_DIMENSION
                or not 1 <= header["height"] <= MAX_DIMENSION
                or header["width"] * header["height"] > MAX_PIXELS
                or type(header["pixel_bytes"]) is not int
                or header["pixel_bytes"] != 3 * header["width"] * header["height"]
                or type(header["pixel_sha256"]) is not str
                or len(header["pixel_sha256"]) != 64
                or any(c not in "0123456789abcdef" for c in header["pixel_sha256"])
            ):
                raise RasterProtocolError
        except (ValueError, TypeError, UnicodeError, RecursionError, KeyError, OverflowError):
            raise RasterProtocolError from None
        self._header = header

    def _append_pixels(self, chunk: bytes) -> None:
        assert self._header is not None
        if len(self._pixels) + len(chunk) > self._header["pixel_bytes"]:
            raise RasterProtocolError
        self._digest.update(chunk)
        self._pixels.extend(chunk)

    def finish(self) -> DecodedRaster:
        if self._closed:
            raise RasterProtocolError
        self._closed = True
        header = self._header
        if (
            header is None
            or len(self._pixels) != header["pixel_bytes"]
            or self._digest.hexdigest() != header["pixel_sha256"]
        ):
            self._pixels.clear()
            raise RasterProtocolError
        result = DecodedRaster(
            cast(RasterKind, header["kind"]),
            self._expected.sha256_hex,
            header["width"],
            header["height"],
            bytes(self._pixels),
            header["pixel_sha256"],
        )
        self._pixels.clear()
        return result
