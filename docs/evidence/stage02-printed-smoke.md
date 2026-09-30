# Stage 02 printed golden smoke — 2026-09-30

Candidate: installed Tesseract `v5.5.3.20260724`, languages `eng`, `rus`, `ukr`, page segmentation mode 6. Fixed checked-in synthetic images are 1024x320. The manifest records exact SHA-256 and references. Command: `uv run --locked --offline python -m tools.printed_golden_smoke`.

| Sample | CER | WER | One-run latency |
|---|---:|---:|---:|
| en-001 | 0 | 0 | 114.05 ms |
| ru-001 | 0 | 0 | 63.69 ms |
| uk-001 | 0 | 0 | 75.52 ms |

Local `python -m pytest` 39 PASS, Ruff check/format PASS and strict mypy PASS. The first test attempt used a non-writable machine Temp and produced two pytest fixture setup errors; rerun with a writable workspace basetemp passed. The three images are deliberately simple and do not represent real receipts, handwriting, layouts, noisy scans or malicious input. No candidate ranking or production adapter selection follows from this smoke; worker isolation and representative benchmark remain Stage 02 gates.
