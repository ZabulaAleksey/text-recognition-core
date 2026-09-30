"""Developer-only smoke of installed Tesseract on fixed, trusted synthetic PNGs."""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import subprocess
import time
import unicodedata
from pathlib import Path
from typing import Any

CORPUS = Path(__file__).resolve().parents[1] / "tests/fixtures/printed_golden_v1"
MAX_IMAGE_BYTES = 100_000
MAX_STDOUT_BYTES = 16_384
LANGUAGES = {"eng", "rus", "ukr"}


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


def benchmark() -> dict[str, Any]:
    samples = manifest_samples()
    executable = shutil.which("tesseract")
    if executable is None:
        raise RuntimeError("tesseract unavailable")
    version = (
        subprocess.run([executable, "--version"], capture_output=True, timeout=5, check=True)
        .stdout.decode("utf-8", errors="replace")
        .splitlines()[0]
    )
    results: list[dict[str, Any]] = []
    for sample in samples:
        start = time.monotonic()
        process = subprocess.run(
            [
                executable,
                str(CORPUS / sample["file"]),
                "stdout",
                "-l",
                sample["language"],
                "--psm",
                "6",
            ],
            capture_output=True,
            timeout=10,
            check=False,
        )
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        if process.returncode or len(process.stdout) > MAX_STDOUT_BYTES:
            raise RuntimeError(f"OCR candidate failed for {sample['id']}")
        expected = _normalized(sample["expected"])
        actual = _normalized(process.stdout.decode("utf-8", errors="replace"))
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
    return {"corpus": "printed_golden_smoke_v1", "engine": version, "results": results}


if __name__ == "__main__":
    print(json.dumps(benchmark(), ensure_ascii=False, indent=2))
