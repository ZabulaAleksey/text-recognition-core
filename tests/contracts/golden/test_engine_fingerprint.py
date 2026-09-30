from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tools import printed_golden_smoke


def test_engine_executable_fingerprint_is_exact_and_streamed(tmp_path: Path) -> None:
    executable = tmp_path / "candidate"
    payload = b"engine" * 200_000
    executable.write_bytes(payload)
    assert (
        printed_golden_smoke.executable_sha256(str(executable))
        == hashlib.sha256(payload).hexdigest()
    )


def test_empty_or_oversized_engine_executable_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    executable = tmp_path / "candidate"
    executable.write_bytes(b"")
    with pytest.raises(ValueError, match="size invalid"):
        printed_golden_smoke.executable_sha256(str(executable))
    executable.write_bytes(b"engine")
    monkeypatch.setattr(printed_golden_smoke, "MAX_EXECUTABLE_BYTES", 5)
    with pytest.raises(ValueError, match="size invalid"):
        printed_golden_smoke.executable_sha256(str(executable))
