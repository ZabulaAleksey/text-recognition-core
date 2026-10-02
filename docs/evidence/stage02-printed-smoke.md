# Stage 02 printed golden smoke — 2026-09-30

Candidate: installed Tesseract `v5.5.3.20260724`, bounded executable SHA-256 `c66f0f12ed76f6aa455dac97684bbc86756d6a732380bee09122454cfda3f420`, languages `eng`, `rus`, `ukr`, page segmentation mode 6. Fixed checked-in synthetic images are 1024x320. The manifest records exact SHA-256 and references. Command: `uv run --locked --offline python -m tools.printed_golden_smoke`.

| Sample | CER | WER | One-run latency |
|---|---:|---:|---:|
| en-001 | 0 | 0 | 114.05 ms |
| ru-001 | 0 | 0 | 63.69 ms |
| uk-001 | 0 | 0 | 75.52 ms |

Local `python -m pytest` 41 PASS, Ruff check/format PASS and strict mypy PASS. The first test attempt used a non-writable machine Temp and produced two pytest fixture setup errors; rerun with a writable workspace basetemp passed. The three images are deliberately simple and do not represent real receipts, handwriting, layouts, noisy scans or malicious input. No candidate ranking or production adapter selection follows from this smoke; worker isolation and representative benchmark remain Stage 02 gates.

The executable digest is a reproducibility fingerprint, not a publisher signature or a digest of traineddata. The fingerprint helper rejects empty or oversized binaries; two new contract tests cover exact digest and size bounds.

## Bounded subprocess output follow-up — 2026-10-02

The smoke runner now reads stdout and stderr concurrently under one 16 KiB retained-output budget, checks the joint byte limit before retaining bytes, and decodes only the bounded output. Version and OCR subprocesses use the same 5 s / 10 s command deadlines. Timeout, output overflow and stream-read failure kill and reap the exact direct child; this diagnostic has no process-tree containment claim. Five added real-child tests cover simultaneous stream flooding, joint stdout+stderr accounting, exact joint boundary with UTF-8, timeout/reap, and read-failure/reap. Full project suite: 61 passed via `uv run --locked --offline --no-sync`; Ruff check/format and strict mypy passed using the existing project environment without dependency sync. The no-sync run warned that the environment uses Python 3.13.7 but its creation marker records 3.13.6. Normal uv sync was blocked by protected machine-cache/project-venv metadata ACLs; no fresh locked restore is claimed.

Fresh read-only local candidate rerun: `python -B -m tools.printed_golden_smoke`; Tesseract `v5.5.3.20260724`, executable SHA-256 unchanged. Synthetic sample results: en-001 CER/WER 0/0, 286.65 ms; ru-001 0/0, 154.11 ms; uk-001 0/0, 123.52 ms. These single-run timings are observations only. No recognized text was added to evidence. This remains a fixed synthetic smoke, not representative benchmark, publisher verification, adapter acceptance, or worker-isolation evidence.

## Review corrections and final local validation — 2026-10-02

The output limit follow-up now rejects invalid UTF-8 instead of replacing bytes, and process-start failures are reported without the executable path or OS error detail. Two additional regressions cover invalid child bytes and a sentinel-bearing start error. Final local suite: 63 PASS via the existing no-sync environment; the seven subprocess regressions pass. Ruff check/format and strict mypy pass. The Ruff format check used a writable task-scratch cache after the repository cache path denied writes. The locked restore limitation and Python 3.13.7 versus 3.13.6 environment marker warning remain as recorded above.

Final fixed-corpus Tesseract observation: same `v5.5.3.20260724` executable digest and CER/WER 0/0 for each synthetic sample; en-001 270.56 ms, ru-001 169.12 ms, uk-001 152.03 ms. Timings are one-run observations only. No recognized text is recorded. The diagnostic still owns only its direct child and does not establish descendant containment, worker isolation, representative quality, or engine selection.
