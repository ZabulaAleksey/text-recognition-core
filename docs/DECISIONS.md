# Engineering decisions

Статусы: `Accepted`, `Proposed`, `Superseded`. Дата bootstrap: 2026-08-13.

## ADR-001 — Standalone repository and thin overlay

**Status:** Accepted.

TRC развивается как самостоятельный Git repository. Project files содержат только domain requirements, contracts, staged plan и локальные инварианты; generic agents, hooks, Skills, Git workflow и MCP наследуются из `codex-workspace`.

Альтернативы: хранить TRC внутри consumer; скопировать AI Dev Team. Они создают дубли pipeline/управления и нарушают границы SPEC.

## ADR-002 — Python modular monolith, library-first

**Status:** Accepted for initial implementation.

Использовать Python 3.13-compatible package с domain/application ports. Начать с embedded/offline profile; FastAPI является поздним REST adapter, а не местом business logic. Причины: Python ecosystem OCR/HTR, возможность локального inference и один Core для library/service/CLI/MCP.

Альтернативы: service-first microservices (слишком ранняя operational complexity); Rust core (усложняет ML integrations до подтверждённого bottleneck). Rust/WASM остаются extension paths после profiling.

Python 3.13 — стабильная поддерживаемая линия по официальной документации: <https://docs.python.org/3.13/>.

## ADR-003 — Typed contracts and generated schemas

**Status:** Accepted.

Domain types остаются framework-neutral; Pydantic v2 применяется на validation/serialization boundaries с strict configuration, `extra='forbid'` для v1 requests и generated JSON Schema. FastAPI генерирует OpenAPI из тех же transport models. Не вести ручную вторую OpenAPI/DTO truth.

Pydantic документирует typed validation и JSON Schema generation: <https://docs.pydantic.dev/latest/concepts/models/> и <https://docs.pydantic.dev/latest/concepts/json_schema/>. FastAPI использует type declarations/OpenAPI: <https://fastapi.tiangolo.com/features/>.

## ADR-004 — Normalized original-page coordinates

**Status:** Accepted.

Public model использует normalized `[0,1]` coordinates with top-left origin, при этом Page хранит original pixel dimensions. Preprocessing хранит reversible transforms. Это делает contracts независимыми от engine resolution и сохраняет overlay mapping.

Альтернатива pixel-only привязывает результат к derived images; normalized-only без dimensions затрудняет точный rendering.

## ADR-005 — Immutable evidence, append-only linear revisions

**Status:** Accepted for MVP.

Raw snapshots append-only. Corrections reference `base_revision_id`; each accepted correction appends a revision under optimistic concurrency. Split/merge/rerun uses ancestry links. Linear history reduces ambiguity; branching/merge is deferred.

## ADR-006 — Initial local persistence profile

**Status:** Accepted for Stage 04.

Первый adapter: SQLite metadata + atomic filesystem/content-addressed blobs + persistent local worker. Storage remains behind ports. PostgreSQL/object storage/external queue require remote deployment evidence and migration ADR.

## ADR-007 — Engine choice is evidence-gated

**Status:** Proposed; decision gate in Stage 02.

Compare at least Tesseract and PaddleOCR-compatible local candidates on approved Ukrainian/Russian/English printed golden data. Evaluate quality (CER/WER/layout), license, offline support, CPU memory/latency, packaging and hostile-input surface. Enable exactly one baseline OCR adapter. HTR engine is contract-only until its own representative benchmark.

No engine receives architectural privilege before this gate.

## ADR-008 — Application adapters live outside Core domain

**Status:** Accepted.

Integration has two contracts: consumer input profile/hints and output projector. Chronicle/receipt/tutor entities live in integration packages or consumer repos; Core only exposes recognition concepts and provenance.

## ADR-009 — Remote mode is gated

**Status:** Accepted.

`LOCAL_ONLY`/embedded profile may be implemented first. Remote deployment is blocked until authentication, authorization, tenant isolation, encryption/retention, rate limiting, audit and incident logging decisions exist. This prevents an interface goal from silently widening the trust boundary.

## ADR-010 — Untrusted processing isolation and artifact integrity

**Status:** Accepted.

Binary decoding, metadata parsing and OCR/model inference must run in disposable least-privilege workers with network denial, private per-job roots, OS limits and hard-kill cleanup. Dependencies are hash-locked and scanned from Stage 01; model/engine artifacts require verified digests/signatures. Executable/object deserialization is forbidden without a separate sandboxed conversion decision.

## ADR-011 — Local service identity boundary

**Status:** Accepted.

Local REST defaults to loopback/local IPC and authenticates a generated high-entropy bearer token or verified OS peer credentials. Token bootstrap uses a private permission-checked file or OS credential store, never CLI arguments or loggable environment output; verification is constant-time and rotation/revocation invalidates old tokens. Startup fails closed without secure storage. CORS is deny-all and cookie auth is absent. Non-loopback bind is a remote profile and cannot be enabled by a convenient flag alone.

## Pending decisions

- `ADR-P01`: PDF/image decoding libraries after security/license/resource spike.
- `ADR-P02`: baseline OCR engine after Stage 02 benchmark.
- `ADR-P03`: concrete retention/deletion/encryption/observability policy for the local persistence profile; must be accepted before Stage 04 writes persistent user data.
- `ADR-P04`: numerical review thresholds and release performance budgets from baseline results.
- `ADR-P05`: HTR engine and GPU policy after a representative handwriting dataset exists.
