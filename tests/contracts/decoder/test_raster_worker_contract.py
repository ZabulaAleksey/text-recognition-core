from __future__ import annotations

import hashlib
import io
import json
import struct
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Any

import pytest

from workers import raster_worker as worker


@dataclass
class Profile:
    size: tuple[int, int] = (1, 1)
    format: str = "PNG"
    mode: str = "RGB"
    n_frames: int = 1
    info: dict[str, Any] = field(default_factory=dict)
    exif: dict[str, Any] = field(default_factory=dict)

    def getexif(self) -> dict[str, Any]:
        return self.exif


@pytest.mark.parametrize("length,accepted", [(32, True), (33, False)])
def test_input_limit_accepts_exact_ceiling_and_rejects_one_over(
    monkeypatch: pytest.MonkeyPatch, length: int, accepted: bool
) -> None:
    monkeypatch.setattr(worker, "MAX_SOURCE_BYTES", 32)
    stream = io.BytesIO(b"x" * length)
    if accepted:
        assert worker.read_source(stream) == b"x" * length
        assert stream.read() == b""
    else:
        with pytest.raises(worker.WorkerFailure, match="^DECODER_INPUT_LIMIT$"):
            worker.read_source(stream)


@pytest.mark.parametrize("source", [b"", b"%PDF-1.7", b"private-canary/path/file", b"\xff\xd8"])
def test_non_raster_envelopes_fail_content_free(source: bytes) -> None:
    with pytest.raises(worker.WorkerFailure, match="^DECODER_INPUT_INVALID$"):
        worker.source_kind(source)


@pytest.mark.parametrize(
    "changes",
    [
        {"mode": "RGBA"},
        {"mode": "P"},
        {"mode": "CMYK"},
        {"n_frames": 2},
        {"info": {"exif": b""}},
        {"info": {"icc_profile": b""}},
        {"info": {"transparency": 0}},
        {"exif": {"secret": "private-canary"}},
        {"format": "JPEG"},
    ],
)
def test_unsupported_profiles_never_silently_transform(changes: dict[str, Any]) -> None:
    with pytest.raises(worker.WorkerFailure, match="^DECODER_PROFILE_UNSUPPORTED$"):
        worker.validate_profile(Profile(**changes), "png")


@pytest.mark.parametrize("size", [(0, 1), (-1, 1), (4097, 1), (1, 4097), (True, 1)])
def test_geometry_rejects_overflow_invalid_and_bool_dimensions(size: tuple[int, int]) -> None:
    with pytest.raises(worker.WorkerFailure, match="^DECODER_GEOMETRY_LIMIT$"):
        worker.validate_profile(Profile(size=size), "png")


def test_exact_geometry_ceiling_and_gray_profile_are_admitted() -> None:
    assert worker.validate_profile(Profile(size=(4096, 4096), mode="L"), "png") == (4096, 4096)


def test_pixel_ceiling_remains_independent_of_dimension_ceiling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(worker, "MAX_PIXELS", 3)
    with pytest.raises(worker.WorkerFailure, match="^DECODER_GEOMETRY_LIMIT$"):
        worker.validate_profile(Profile(size=(2, 2)), "png")


def test_protocol_header_binds_independent_source_and_pixel_digests() -> None:
    source, pixels = b"authored-source", bytes((1, 2, 3, 4, 5, 6))
    framed = worker.frame_header(source, "png", 2, 1, pixels)
    assert framed[:11] == b"TRCRASTER1\n"
    length = struct.unpack(">I", framed[11:15])[0]
    assert len(framed) == 15 + length
    assert json.loads(framed[15:]) == {
        "schema": 1,
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "kind": "png",
        "width": 2,
        "height": 1,
        "pixel_format": "RGB8",
        "pixel_bytes": 6,
        "pixel_sha256": hashlib.sha256(pixels).hexdigest(),
    }


@pytest.mark.parametrize("pixels", [b"", b"xx", b"xxxx"])
def test_protocol_cannot_emit_incomplete_or_trailing_pixels(pixels: bytes) -> None:
    with pytest.raises(worker.WorkerFailure, match="^DECODER_OUTPUT_LIMIT$"):
        worker.frame_header(b"source", "png", 1, 1, pixels)


def test_failures_emit_only_allowlisted_diagnostic_and_no_stdout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stdout, stderr = io.BytesIO(), io.BytesIO()
    monkeypatch.setattr(worker.sys, "version_info", (3, 13, 0))
    monkeypatch.setattr(worker.sys, "stdin", SimpleNamespace(buffer=io.BytesIO(b"canary")))
    monkeypatch.setattr(worker.sys, "stdout", SimpleNamespace(buffer=stdout))
    monkeypatch.setattr(worker.sys, "stderr", SimpleNamespace(buffer=stderr))

    def fail_decode(source: bytes) -> Any:
        raise RuntimeError("private-canary C:/secret/path untrusted metadata")

    monkeypatch.setattr(worker, "decode_source", fail_decode)
    assert worker.main() == 1
    assert stdout.getvalue() == b""
    assert stderr.getvalue() == b"DECODER_DECODE_FAILED\n"


def test_unsupported_python_fails_before_binary_decoder_or_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    stdout, stderr = io.BytesIO(), io.BytesIO()
    monkeypatch.setattr(worker.sys, "version_info", (3, 12, 5))
    monkeypatch.setattr(worker.sys, "stdout", SimpleNamespace(buffer=stdout))
    monkeypatch.setattr(worker.sys, "stderr", SimpleNamespace(buffer=stderr))
    assert worker.main() == 1
    assert stdout.getvalue() == b""
    assert stderr.getvalue() == b"DECODER_RUNTIME_UNAVAILABLE\n"
