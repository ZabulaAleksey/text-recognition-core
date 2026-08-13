# Roadmap

Stages are sequential unless a prompt explicitly permits independent research. Each implementation stage ends with tests, review, status/log synchronization, commit and user-controlled merge.

## Completed

### K0 — Project КАРКАС

- standalone local Git repository and remote configured;
- canonical SPEC and stable requirement registry;
- architecture, API/data/integration contracts;
- stack and architecture decisions;
- security, testing and context-compatibility strategy;
- project overlay, stage prompts and current status.

No product source code was created.

## Current

### Stage 01 — Foundation and typed contracts

Create Python package boundaries, immutable typed domain/application contracts, generated schemas, in-memory ports and foundational tests. No real OCR SDK, REST or persistent storage.

Gate: `FR-001`, `FR-002`, `FR-010`, `AC-001`, `AC-010`, dependency rules and hash-locked supply-chain baseline proven.

## Planned

### Stage 02 — Intake, pipeline and one baseline OCR adapter

Implement safe intake/preprocessing ports, engine registry/selection, fake adapter and evidence-gated local OCR adapter. Establish golden/baseline report and select the engine via ADR.

Depends on Stage 01. Gate: `FR-003`, `NFR-003`, `PERF-001`, `AC-002`, `AC-005`, `AC-007`, `AC-010`; decoder/engine isolation is mandatory.

### Stage 03 — Corrections, revisions and partial rerun

Implement append-only raw snapshot, deterministic correction replay, optimistic linear revisions, stable ancestry and region/line rerun orchestration.

Depends on Stages 01–02. Gate: `FR-004`–`FR-006`, `AC-003`, `AC-009`; trusted actor and revocable consent model.

### Stage 04 — Local persistence, jobs and REST adapter

Add SQLite/filesystem adapters, persistent local worker, idempotency/cancellation/progress/cache and FastAPI REST adapter. Remote mode remains disabled.

Depends on Stages 01–03 and accepted local retention/deletion ADR-P03. Gate: `FR-007`, `SEC-002`, `SEC-005`, `SEC-007`, `SEC-010`, `AC-008`, `AC-009`, `AC-011`, recovery and compatibility tests.

### Stage 05 — Application integration contracts

Implement consumer profiles/projectors for Personal Chronicle, Receipt Scanner and Tutor as integration packages with provenance and no domain leakage.

Depends on stable result/revision API. Gate: `FR-008`, `AC-006` and adapter tests.

### Stage 06 — HTR/mixed routing and quality hardening

Build representative handwriting/mixed golden set, select an HTR adapter by ADR, implement region routing/fallback and complete privacy/security/performance regression gates.

Depends on Stages 02–05. Gate: `NFR-001`, `NFR-004`, `SEC-001`–`SEC-010`, `AC-004`–`AC-011`.

## Later / optional

### Stage 07 — Additional interfaces and deployment profiles

CLI first if useful; product MCP, remote service, external queue/storage, GPU/distributed execution or other interfaces only after demand and their own security/operational decisions.

### Research tracks

Personalized HTR, dataset export/fine-tuning, ensemble recognition, math/table/diagram OCR, WASM/mobile/edge and LLM postprocessing are experimental until separate SPEC/ADR/metrics exist.

## Release definition

Core MVP is not complete merely because the KАРКАС exists. It requires the runtime checklist in SPEC section 63, all relevant acceptance evidence, approved benchmark baselines and release/security review.
