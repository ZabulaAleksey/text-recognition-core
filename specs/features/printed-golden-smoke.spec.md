# Stage 02 — printed OCR synthetic golden smoke

Status: accepted local preparation slice; not Stage 02 engine acceptance.

## Scope

- Three authored, synthetic printed images cover English, Russian and Ukrainian.
- A versioned manifest records language, expected text, SHA-256, dimensions, split and provenance. Only this trusted checked-in corpus is eligible for the local benchmark command.
- A local tool verifies every digest before invoking the installed Tesseract candidate with bounded wall time and output. The per-process output budget is a joint stdout+stderr byte cap enforced while reading; no child output is fully buffered before the cap is checked. Bounded output is decoded as strict UTF-8; invalid bytes fail with a sanitized error rather than being replaced. Process-start, read, timeout, exit and overflow errors never include executable paths or child output. The tool reports CER, WER and latency without embedding recognized text.
- No production engine adapter, decoder, model loader or network path is added. The tool is an explicit developer diagnostic and must never accept private or untrusted input.

## Acceptance and limits

- Manifest integrity, unique IDs, language map, image bounds and nonempty reference are tested without Tesseract.
- The candidate command produces a machine-readable report with per-image results, exact installed version and a SHA-256 fingerprint of the bounded installed executable. The digest identifies the local candidate only; it does not attest to a trusted publisher or model data. Nonzero engine exit, timeout, changed digest or excessive combined stdout+stderr output fails visibly. Timeout and output overflow terminate and reap the exact direct child process within the same bounded command deadline; this developer diagnostic does not claim descendant/process-tree containment or worker isolation.
- Zero error on this tiny synthetic corpus is only a smoke result. It does not select an engine, establish representative quality/performance thresholds, prove layout, worker isolation or live OCR acceptance.
- Rollback: remove this bounded fixture/tool/test slice. No application or persisted user state changes.
