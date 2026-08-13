# Архитектура Text Recognition Core

**Статус:** КАРКАС; runtime ещё не реализован. Архитектура обеспечивает `specs/system.spec.md` и не утверждает наличие компонентов в коде.

## Цели и границы

TRC предоставляет стабильные OCR/HTR contracts, orchestration, унифицированный recognition model, corrections/revisions и extension ports. Consumer-specific semantic search, accounting, teaching logic, UI и model training находятся вне Core.

## Dependency rule

```text
interfaces (REST / SDK / CLI / MCP / workers)
                    ↓
application use cases + ports
                    ↓
domain model and invariants
                    ↑
infrastructure + engine/storage/job adapters
```

Domain не импортирует FastAPI, Pydantic transport DTO, database/queue clients или OCR SDK. Infrastructure реализует application ports. Application adapters потребителей являются sibling integration packages и не вносят consumer entities в domain.

## Bounded contexts

| Контекст | Ответственность | Не входит |
|---|---|---|
| Document Intake | source descriptor, validation, hashing, original preservation, safe normalization | OCR и consumer parsing |
| Recognition Orchestration | request validation, pipeline plan, capabilities, engine selection/fallback, partial rerun | engine SDK details |
| Engine Integration | registry, `RecognitionEngine`, confidence/provenance normalization | application business rules |
| Recognition Model | Document/Page/Region/Line/Token, layout, alternatives, raw snapshot | mutable user edits |
| Corrections & Revisions | append-only corrections, revision graph, replay/diff/rollback/current view | raw overwrite |
| Jobs & Execution | lifecycle, progress, cancellation, idempotency, resource budgets | transport handlers |
| Application Integration | input profiles/hints and output projectors for consumers | Chronicle/receipt/tutor domain ownership |
| Persistence & Privacy | logical stores, transactions, cache, retention/deletion ports, privacy policy | fixed database technology in domain |
| Quality & Benchmarking | golden datasets, CER/WER/layout/adapter metrics, reproducible reports | production training loop |

## Recognition flow

```text
Untrusted Source
  → size/format/resource validation
  → disposable least-privilege decoder/OCR worker
  → immutable original + input hash
  → normalization/preprocessing (derived artifacts)
  → layout analysis and region classification
  → capability-aware engine selection
  → RecognitionEngine adapter(s)
  → normalized confidence/coordinates/provenance
  → immutable RawRecognitionSnapshot
  → Revision 1 / Current View
  → optional application projection
```

Pipeline stages implement replaceable ports: `Preprocessor`, `LayoutAnalyzer`, `RecognitionEngine`, `Postprocessor`, `ResultValidator`. Binary decoding, metadata parsing and engine/model inference run in disposable subprocess workers (or an equivalently isolated sandbox) with network denied, private per-job temp root, minimal read-only source access, unprivileged identity, OS CPU/RSS/file/process limits, hard timeout/kill and crash/cancel cleanup. Each stage consumes/produces typed values and checks cancellation/resource budget at safe boundaries.

## Corrections and partial rerun

```text
stable target + base_revision_id + operation
  → validate target and optimistic version
  → append Correction
  → append Revision(parent_revision_id)
  → deterministic replay/current view
```

Split/merge creates new stable IDs plus explicit ancestry links; old IDs remain addressable in prior revisions. Partial rerun creates new raw evidence associated with the selected scope and then a new revision; it never mutates the previous raw snapshot.

## Async jobs

Allowed transitions:

```text
PENDING → RUNNING → COMPLETED
                  ↘ REVIEW_REQUIRED
                  ↘ FAILED
PENDING/RUNNING → CANCELLED
```

Terminal states are immutable. Retry creates a new attempt under the same logical job and records its reason. Idempotency identity `(tenant, principal, operation, key)` maps to one canonical request hash/result; a different hash conflicts and cannot create a second job. Recognition cache is independent and keyed by policy-required identity plus canonical request, privacy mode, schema/pipeline versions and exact engine/model artifact digests. Every retrieval is re-authorized and never reveals another scope's hit/existence.

## Storage boundaries

Logical stores are separate even when the first adapter uses one SQLite database plus filesystem blobs:

- original sources and derived artifacts;
- immutable raw recognition snapshots;
- corrections and revisions;
- jobs/idempotency/progress;
- cache indexed by input/config/version hashes;
- derived application projections outside Core ownership.

Blob writes are content-addressed/atomic; database transactions publish metadata only after a blob is durable. Deletion policy may remove retained source data when authorized; «original is not destroyed» means preprocessing never overwrites it, not infinite retention.

## Interfaces and extension points

- Public: versioned Python application API first; REST adapter after contracts; CLI/MCP later.
- Engine: `RecognitionEngine` and capability descriptors.
- Pipeline: preprocessor/layout/postprocessor ports.
- Persistence: repositories/blob/cache/unit-of-work ports.
- Execution: job runner, cancellation token, resource budget, clock/id generator.
- Integration: consumer input profile and output projector interfaces.
- Export: privacy-aware benchmark/dataset exporter.

## Deployment profiles

1. **Embedded/offline first:** Python library, local engine, SQLite/filesystem and persistent local coordinator; untrusted decoding/inference still runs in isolated disposable workers.
2. **Local service:** REST adapter binds loopback/local IPC only, requires generated local bearer token or verified OS peer credentials, denies browser CORS by default and retains no cookie-based session; still no external egress in `LOCAL_ONLY`.
3. **Remote service:** authentication, authorization, tenant isolation, encryption, rate limits and external queue/storage only after separate decisions.

Docker packages a selected profile but does not define architecture. MCP is a late interface over application use cases.

## Technology baseline

Recorded in `DECISIONS.md`: Python 3.13-compatible package, typed internal models, Pydantic v2 at validation/schema boundaries, FastAPI only as REST adapter, pytest, initial SQLite/filesystem adapter. OCR/HTR and PDF/image libraries remain benchmark/ADR decisions.

## Failure model

- Fatal errors stop the job and use stable error codes.
- Warnings preserve usable output.
- Low confidence leads to `REVIEW_REQUIRED`, not automatic failure.
- Adapter failure may use an allowed fallback; every attempt and parameter set remains traceable.
- No retry is automatic for deterministic invalid input; transient retries are bounded and cancellation-aware.

## Architectural fitness checks

- dependency/import boundaries;
- schema compatibility snapshots;
- engine contract suite;
- correction replay/raw immutability;
- `LOCAL_ONLY` no-egress test;
- private fixture and telemetry leakage detection;
- worker isolation/crash/cleanup and dependency/model integrity checks;
- golden quality/performance regression reports.
