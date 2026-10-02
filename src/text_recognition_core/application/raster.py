"""Immutable, content-only raster port; binary parsing belongs to isolated workers."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Literal, Protocol

from text_recognition_core.application.ports import CancellationToken

MAX_DIMENSION = 4096
MAX_PIXELS = 16777216
MAX_PIXEL_BYTES = 3 * MAX_PIXELS
RasterKind = Literal["png", "jpeg"]


@dataclass(frozen=True, slots=True)
class DecodedRaster:
    kind: RasterKind
    source_sha256: str
    width: int
    height: int
    pixels: bytes
    pixel_sha256: str

    def __post_init__(self) -> None:
        if (
            self.kind not in ("png", "jpeg")
            or type(self.width) is not int
            or type(self.height) is not int
            or not 1 <= self.width <= MAX_DIMENSION
            or not 1 <= self.height <= MAX_DIMENSION
            or self.width * self.height > MAX_PIXELS
            or type(self.pixels) is not bytes
            or len(self.pixels) != 3 * self.width * self.height
            or any(
                type(value) is not str
                or len(value) != 64
                or any(character not in "0123456789abcdef" for character in value)
                for value in (self.source_sha256, self.pixel_sha256)
            )
            or sha256(self.pixels).hexdigest() != self.pixel_sha256
        ):
            raise ValueError("invalid_decoded_raster")


class RasterDecoder(Protocol):
    def decode(self, source: bytes, cancellation: CancellationToken) -> DecodedRaster: ...
