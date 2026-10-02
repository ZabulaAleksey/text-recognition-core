"""Developer-only smoke of installed Tesseract on fixed, trusted synthetic PNGs."""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import subprocess
import threading
import time
import unicodedata
from collections.abc import Sequence
from pathlib import Path
from typing import Any

CORPUS = Path(__file__).resolve().parents[1] / "tests/fixtures/printed_golden_v1"
MAX_IMAGE_BYTES = 100_000
MAX_OUTPUT_BYTES = 16_384
_OUTPUT_READ_BYTES = 4_096
MAX_EXECUTABLE_BYTES = 100_000_000
LANGUAGES = {"eng", "rus", "ukr"}


class CandidateProcessError(RuntimeError):
    """A bounded diagnostic child failed without exposing its output."""


def _run_bounded_process(
    command: Sequence[str], *, timeout_seconds: float, max_output_bytes: int = MAX_OUTPUT_BYTES
) -> tuple[str, str, int]:
    """Run one direct child with bounded joint output and bounded cleanup.

    This developer diagnostic owns and reaps only the exact process returned by
    Popen. It does not claim to contain or terminate descendants.
    """
    if (
        not command
        or isinstance(command, (str, bytes))
        or any(not isinstance(argument, str) for argument in command)
        or type(timeout_seconds) not in (int, float)
        or not 0 < timeout_seconds <= 10
    ):
        raise ValueError("invalid candidate process limits")
    if type(max_output_bytes) is not int or not 0 < max_output_bytes <= MAX_OUTPUT_BYTES:
        raise ValueError("invalid candidate output limit")

    started = time.monotonic()
    deadline = started + timeout_seconds
    cleanup_reserve = min(0.5, timeout_seconds * 0.25)
    run_deadline = deadline - cleanup_reserve
    try:
        process = subprocess.Popen(
            list(command),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
    except OSError:
        raise CandidateProcessError("candidate process start failed") from None
    assert process.stdout is not None and process.stderr is not None

    outputs = {"stdout": bytearray(), "stderr": bytearray()}
    output_lock = threading.Lock()
    output_limit = threading.Event()
    read_failure = threading.Event()

    def drain(name: str, stream: Any) -> None:
        try:
            while chunk := stream.read(_OUTPUT_READ_BYTES):
                with output_lock:
                    current_size = len(outputs["stdout"]) + len(outputs["stderr"])
                    remaining = max_output_bytes - current_size
                    if len(chunk) > remaining:
                        output_limit.set()
                        return
                    outputs[name].extend(chunk)
        except OSError:
            read_failure.set()
        finally:
            try:
                stream.close()
            except OSError:
                read_failure.set()

    readers = [
        threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
        threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
    ]
    for reader in readers:
        reader.start()

    failure: str | None = None
    while True:
        if output_limit.is_set():
            failure = "candidate output exceeded the byte limit"
            break
        if read_failure.is_set():
            failure = "candidate output read failed"
            break
        if process.poll() is not None:
            break
        remaining = run_deadline - time.monotonic()
        if remaining <= 0:
            failure = "candidate process timed out"
            break
        output_limit.wait(min(0.01, remaining))

    if failure is not None and process.poll() is None:
        try:
            process.kill()
        except OSError:
            failure = "candidate process cleanup failed"

    try:
        remaining = max(0.0, deadline - time.monotonic())
        returncode = process.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        failure = "candidate process cleanup timed out"
        returncode = process.poll()

    for reader in readers:
        reader.join(timeout=max(0.0, deadline - time.monotonic()))
    if any(reader.is_alive() for reader in readers):
        failure = "candidate output stream cleanup timed out"
    elif output_limit.is_set():
        failure = "candidate output exceeded the byte limit"
    elif read_failure.is_set():
        failure = "candidate output read failed"

    if failure is not None:
        raise CandidateProcessError(failure)
    if returncode is None:
        raise CandidateProcessError("candidate process state unavailable")
    try:
        stdout = outputs["stdout"].decode("utf-8", errors="strict")
        stderr = outputs["stderr"].decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise CandidateProcessError("candidate output is not valid UTF-8") from None
    return stdout, stderr, returncode


def manifest_samples() -> list[dict[str, Any]]:
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("split") != "golden_smoke":
        raise ValueError("unsupported golden manifest")
    samples = manifest.get("samples")
    if not isinstance(samples, list) or len(samples) != 3:
        raise ValueError("expected three golden samples")
    ids: set[str] = set()
    for sample in samples:
        if not isinstance(sample, dict):
            raise ValueError("invalid golden sample")
        sample_id = sample.get("id")
        filename = sample.get("file")
        expected = sample.get("expected")
        if not isinstance(sample_id, str) or not sample_id or sample_id in ids:
            raise ValueError("duplicate or invalid golden ID")
        ids.add(sample_id)
        if filename not in {"en.png", "ru.png", "uk.png"}:
            raise ValueError("golden filename outside allowlist")
        if sample.get("language") not in LANGUAGES:
            raise ValueError("unsupported golden language")
        if not isinstance(expected, str) or not expected.strip() or len(expected) > 1024:
            raise ValueError("invalid golden reference")
        path = CORPUS / filename
        data = path.read_bytes()
        if len(data) > MAX_IMAGE_BYTES or len(data) < 24:
            raise ValueError("golden image size invalid")
        if data[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
            raise ValueError("golden PNG header invalid")
        width, height = struct.unpack(">II", data[16:24])
        if (width, height) != (sample.get("width"), sample.get("height")):
            raise ValueError("golden image dimensions changed")
        if hashlib.sha256(data).hexdigest() != sample.get("sha256"):
            raise ValueError("golden image digest changed")
    return samples


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split())


def edit_distance(left: list[str], right: list[str]) -> int:
    previous = list(range(len(right) + 1))
    for i, item in enumerate(left, 1):
        current = [i]
        for j, other in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (item != other)))
        previous = current
    return previous[-1]


def executable_sha256(executable: str) -> str:
    """Fingerprint a bounded local candidate without reading it into memory."""
    path = Path(executable)
    size = path.stat().st_size
    if not 0 < size <= MAX_EXECUTABLE_BYTES:
        raise ValueError("engine executable size invalid")
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            total += len(chunk)
            if total > MAX_EXECUTABLE_BYTES:
                raise ValueError("engine executable size invalid")
            digest.update(chunk)
    if total != size:
        raise ValueError("engine executable changed during read")
    return digest.hexdigest()


def benchmark() -> dict[str, Any]:
    samples = manifest_samples()
    executable = shutil.which("tesseract")
    if executable is None:
        raise RuntimeError("tesseract unavailable")
    version_stdout, _, version_returncode = _run_bounded_process(
        [executable, "--version"], timeout_seconds=5
    )
    version_lines = version_stdout.splitlines()
    if version_returncode != 0 or not version_lines:
        raise CandidateProcessError("candidate version probe failed")
    version = version_lines[0]
    engine_sha256 = executable_sha256(executable)
    results: list[dict[str, Any]] = []
    for sample in samples:
        start = time.monotonic()
        stdout, _, returncode = _run_bounded_process(
            [
                executable,
                str(CORPUS / sample["file"]),
                "stdout",
                "-l",
                sample["language"],
                "--psm",
                "6",
            ],
            timeout_seconds=10,
        )
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        if returncode:
            raise RuntimeError(f"OCR candidate failed for {sample['id']}")
        expected = _normalized(sample["expected"])
        actual = _normalized(stdout)
        results.append(
            {
                "id": sample["id"],
                "language": sample["language"],
                "sha256": sample["sha256"],
                "cer": edit_distance(list(expected), list(actual)) / len(expected),
                "wer": edit_distance(expected.split(), actual.split()) / len(expected.split()),
                "latency_ms": elapsed_ms,
            }
        )
    return {
        "corpus": "printed_golden_smoke_v1",
        "engine": version,
        "engine_sha256": engine_sha256,
        "results": results,
    }


if __name__ == "__main__":
    print(json.dumps(benchmark(), ensure_ascii=False, indent=2))
