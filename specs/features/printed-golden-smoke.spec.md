# Stage 02 — printed OCR synthetic golden smoke

Status: accepted local preparation slice; not Stage 02 engine acceptance.

## Scope

- Three authored, synthetic printed images cover English, Russian and Ukrainian.
- A versioned manifest records language, expected text, SHA-256, dimensions, split and provenance. Only this trusted checked-in corpus is eligible for the local benchmark command.
- A local tool verifies every digest before invoking the installed Tesseract candidate with bounded wall time and output. It reports CER, WER and latency without embedding recognized text.
- No production engine adapter, decoder, model loader or network path is added. The tool is an explicit developer diagnostic and must never accept private or untrusted input.

## Acceptance and limits

- Manifest integrity, unique IDs, language map, image bounds and nonempty reference are tested without Tesseract.
- The candidate command produces a machine-readable report with per-image results and exact installed version. Nonzero engine exit, timeout, changed digest or excessive output fails visibly.
- Zero error on this tiny synthetic corpus is only a smoke result. It does not select an engine, establish representative quality/performance thresholds, prove layout, worker isolation or live OCR acceptance.
- Rollback: remove this bounded fixture/tool/test slice. No application or persisted user state changes.
