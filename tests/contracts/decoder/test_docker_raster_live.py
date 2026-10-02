"""Opt-in actual consumer→Docker worker contracts; authored fixtures only."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import struct
import sys
import zlib
from pathlib import Path

import pytest

from text_recognition_core.intake.docker_raster import (
    DockerRasterBinding,
    WindowsDockerRasterDecoder,
)

pytestmark = pytest.mark.skipif(
    os.name != "nt" or not os.environ.get("TRC_RASTER_TEST_ADMISSION"),
    reason="requires explicitly reviewed local Windows/Docker worker admission receipt",
)


class NeverCancelled:
    def cancelled(self) -> bool:
        return False


@pytest.fixture
def live_decoder() -> WindowsDockerRasterDecoder:
    path = Path(os.environ["TRC_RASTER_TEST_ADMISSION"])
    with path.open("rb") as stream:
        raw = stream.read(65537)
    assert len(raw) <= 65536
    receipt = json.loads(raw)
    assert receipt["status"] == "ADMITTED_LOCAL_AUTHORED_RASTER_PROBES_ONLY"
    assert receipt["cleanup_verified"] is True
    assert receipt["production_admission"] is False
    assert receipt["private_inputs_admission"] is False
    assert (3, 13) <= tuple(receipt["actual_python"][:2]) < (4, 0)
    assert receipt["actual_pillow"] == "12.3.0"
    cli = Path(os.environ["ProgramFiles"]) / "Docker/Docker/resources/bin/docker.exe"
    binding = DockerRasterBinding(
        cli,
        "00ffff945b67c65aae98dd980621a80ee135ed4e0931b33ca03687caee019713",
        receipt["image_id"],
        tuple(receipt["image_environment"]),
        hashlib.sha256(raw).hexdigest(),
    )
    return WindowsDockerRasterDecoder(binding)


def chunk(name: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + name
        + data
        + struct.pack(">I", zlib.crc32(name + data) & 0xFFFFFFFF)
    )


def test_actual_authored_rgb_png_source_pixels_and_terminal_cleanup(
    live_decoder: WindowsDockerRasterDecoder,
) -> None:
    pixels = bytes([1, 2, 3, 40, 50, 60])
    source = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 1, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"\x00" + pixels))
        + chunk(b"IEND", b"")
    )
    assert sys.version_info >= (3, 13)
    assert "PIL" not in sys.modules
    result = live_decoder.decode(source, NeverCancelled())
    assert (result.kind, result.width, result.height, result.pixels) == ("png", 2, 1, pixels)
    assert result.source_sha256 == hashlib.sha256(source).hexdigest()
    assert result.pixel_sha256 == hashlib.sha256(pixels).hexdigest()
    assert live_decoder.pending_recovery is None
    assert "PIL" not in sys.modules


def test_actual_authored_constant_gray_jpeg_identity_expansion(
    live_decoder: WindowsDockerRasterDecoder,
) -> None:
    # Authored 2×2 uniform L=128, quality95/subsampling0, created inside the admitted
    # worker image. Independently expected RGB channels remain exactly 128.
    source = base64.b64decode(
        "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkI"
        "BgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/wAALCAACAAIBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAA"
        "AAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII"
        "0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlq"
        "c3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1N"
        "XW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/ACv/2Q==",
        validate=True,
    )
    result = live_decoder.decode(source, NeverCancelled())
    pixels = bytes([128]) * 12
    assert (result.kind, result.width, result.height, result.pixels) == ("jpeg", 2, 2, pixels)
    assert result.source_sha256 == hashlib.sha256(source).hexdigest()
    assert result.pixel_sha256 == hashlib.sha256(pixels).hexdigest()
    assert live_decoder.pending_recovery is None
    assert "PIL" not in sys.modules
