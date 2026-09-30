"""Bounded source-byte envelope before isolated decoding.

This inspects only leading signatures and computes a digest. It does not make
untrusted images or PDF safe to parse in this process.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import BinaryIO, Literal

SourceKind = Literal["png", "jpeg", "pdf"]
MAX_SOURCE_BYTES = 64 * 1024 * 1024
_CHUNK_BYTES = 64 * 1024


@dataclass(frozen=True, slots=True)
class SourceByteEnvelope:
    kind: SourceKind
    byte_count: int
    sha256_hex: str


def inspect_source_bytes(
    stream: BinaryIO, *, max_bytes: int = MAX_SOURCE_BYTES
) -> SourceByteEnvelope:
    """Hash a bounded binary stream without opening paths or decoding content."""
    if type(max_bytes) is not int or not 0 < max_bytes <= MAX_SOURCE_BYTES:
        raise ValueError("invalid_source_limit")

    digest = sha256()
    count = 0
    prefix = b""
    while True:
        # One excess byte distinguishes a full source from an oversized one.
        requested = min(_CHUNK_BYTES, max_bytes - count + 1)
        try:
            chunk = stream.read(requested)
        except OSError:
            raise ValueError("source_read_failed") from None
        if type(chunk) is not bytes or len(chunk) > requested:
            raise ValueError("invalid_source_stream")
        if not chunk:
            break
        count += len(chunk)
        if count > max_bytes:
            raise ValueError("source_too_large")
        if len(prefix) < 8:
            prefix = (prefix + chunk)[:8]
        digest.update(chunk)

    if count == 0:
        raise ValueError("source_empty")
    if prefix.startswith(b"\x89PNG\r\n\x1a\n"):
        kind: SourceKind = "png"
    elif prefix.startswith(b"\xff\xd8\xff"):
        kind = "jpeg"
    elif prefix.startswith(b"%PDF-"):
        kind = "pdf"
    else:
        raise ValueError("source_format_unsupported")
    return SourceByteEnvelope(kind=kind, byte_count=count, sha256_hex=digest.hexdigest())
