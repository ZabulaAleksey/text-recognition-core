from __future__ import annotations

from hashlib import sha256
from io import BytesIO

import pytest

from text_recognition_core.intake.envelope import inspect_source_bytes


@pytest.mark.parametrize(
    ("source", "kind"),
    [
        (b"\x89PNG\r\n\x1a\n" + b"abc", "png"),
        (b"\xff\xd8\xff" + b"abc", "jpeg"),
        (b"%PDF-1.7\nabc", "pdf"),
    ],
)
def test_immutable_digest_envelope(source: bytes, kind: str) -> None:
    result = inspect_source_bytes(BytesIO(source))
    assert (result.kind, result.byte_count, result.sha256_hex) == (
        kind,
        len(source),
        sha256(source).hexdigest(),
    )
    with pytest.raises(AttributeError):
        result.byte_count = 2  # type: ignore[misc]


def test_exact_limit_and_one_excess_byte() -> None:
    source = b"%PDF-" + b"x" * 100000
    assert inspect_source_bytes(BytesIO(source), max_bytes=len(source)).byte_count == len(source)
    with pytest.raises(ValueError, match="^source_too_large$"):
        inspect_source_bytes(BytesIO(source), max_bytes=len(source) - 1)


class OneByteStream:
    def __init__(self, payload: bytes) -> None:
        self.payload = BytesIO(payload)

    def read(self, amount: int = -1) -> bytes:
        return self.payload.read(min(amount, 1))


def test_short_reads_are_hashed_exactly() -> None:
    source = b"%PDF-1.7\n"
    assert inspect_source_bytes(OneByteStream(source)).sha256_hex == sha256(source).hexdigest()


@pytest.mark.parametrize(
    ("source", "code"),
    [
        (b"", "source_empty"),
        (b"\x89PNG\r\n", "source_format_unsupported"),
        (b"not an image", "source_format_unsupported"),
    ],
)
def test_rejected_source_has_content_free_error(source: bytes, code: str) -> None:
    with pytest.raises(ValueError, match=f"^{code}$"):
        inspect_source_bytes(BytesIO(source))


@pytest.mark.parametrize("limit", [0, -1, True, 64 * 1024 * 1024 + 1])
def test_invalid_limit(limit: int) -> None:
    with pytest.raises(ValueError, match="^invalid_source_limit$"):
        inspect_source_bytes(BytesIO(b"%PDF-"), max_bytes=limit)


class InvalidStream:
    def __init__(self, value: object) -> None:
        self.value = value

    def read(self, amount: int = -1) -> object:
        return self.value


@pytest.mark.parametrize("value", ["%PDF-", b"%PDF-" + b"x" * 100])
def test_invalid_stream_response(value: object) -> None:
    with pytest.raises(ValueError, match="^invalid_source_stream$"):
        inspect_source_bytes(InvalidStream(value), max_bytes=10)  # type: ignore[arg-type]


class FailedStream:
    def read(self, amount: int = -1) -> bytes:
        raise OSError("private/path/and/content")


def test_read_error_is_redacted() -> None:
    with pytest.raises(ValueError, match="^source_read_failed$") as error:
        inspect_source_bytes(FailedStream())
    assert "private/path" not in str(error.value)
