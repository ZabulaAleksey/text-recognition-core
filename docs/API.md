# API contracts

**Статус:** contract design for Schema v1 / API v1. Код и OpenAPI ещё не созданы. Typed application models являются источником generated JSON Schema/OpenAPI; ручная параллельная схема запрещена.

## Conventions

- JSON uses `snake_case`, UTF-8 and RFC 3339 UTC timestamps.
- IDs are opaque, stable strings; clients do not parse their format.
- Coordinates use normalized page space `[0.0, 1.0]`, origin top-left; polygon points follow reading order. Pixel dimensions remain on `Page` for rendering.
- Confidence is `0.0..1.0` or absent with an explicit reason; no sentinel values.
- Unknown enum/capability in a request is rejected in v1. Response additive fields are allowed; semantic changes require a new schema/API version.

## RecognitionRequest

```text
RecognitionRequest
  schema_version: "recognition-request/v1"
  sources: list[SourceRef]  # 1..configured batch limit
  batch_policy: ALL_OR_NOTHING | ALLOW_PARTIAL
  mode: AUTO | OCR | HTR | MIXED
  languages: list[BCP-47]
  capabilities: list[CapabilityRequirement]
  privacy_mode: LOCAL_ONLY | HYBRID | REMOTE_ALLOWED
  preprocessing: PreprocessingOptions
  engine_preferences: EnginePreferences
  output: OutputOptions
  context: map[string, JSON value]
  idempotency_key?: string
```

Each capability has `name` and `required`. Unsupported required capability returns `CAPABILITY_UNSUPPORTED`; optional capability may be omitted with a warning. One source creates one Document/RecognitionResult. `ALL_OR_NOTHING` validates every source before accepting the job and produces no Documents/results when any source is rejected; a later per-source processing failure makes the batch job `FAILED` while preserving only internal diagnostic artifacts subject to cleanup. `ALLOW_PARTIAL` returns ordered per-source outcomes and creates Documents/results only for successful sources. Job/result order always matches request source order.

`SourceRef` is either an uploaded opaque source ID or trusted internal blob reference. Public clients never send arbitrary server filesystem paths or executable URLs.

## RecognitionResult

```text
RecognitionResult
  schema_version: "recognition-result/v1"
  document_id: ID
  raw_result_id: ID
  current_revision_id: ID
  provenance: Provenance
  detected_languages: list[LanguageScore]
  pages: list[Page]
  plain_text: string
  confidence?: float
  warnings: list[Warning]
  metadata: map[string, JSON value]
```

`raw_result_id` and `current_revision_id` are deliberately separate. Provenance contains input hash, engine/model/pipeline versions, normalized configuration hash, timestamps and attempts.

## RecognitionEngine port

```text
capabilities() -> EngineCapabilities
recognize(EngineRequest, CancellationToken, ResourceBudget) -> EngineResult
recognize_region(EngineRegionRequest, CancellationToken, ResourceBudget) -> EngineResult
health() -> EngineHealth
version() -> EngineVersion
```

Adapters must not leak vendor DTOs. They normalize confidence, coordinates, errors and provenance and pass the shared contract suite.

## REST API v1

| Method | Path | Result |
|---|---|---|
| `POST` | `/v1/recognitions` | `202 RecognitionJob`; idempotency supported |
| `GET` | `/v1/recognitions/{job_id}` | job status/progress/error/result link |
| `POST` | `/v1/recognitions/{job_id}/cancel` | accepted cancellation request |
| `GET` | `/v1/documents/{document_id}` | current view metadata |
| `GET` | `/v1/documents/{document_id}/pages` | paginated pages |
| `POST` | `/v1/documents/{document_id}/corrections` | new correction and revision |
| `GET` | `/v1/documents/{document_id}/revisions` | paginated revision summaries |
| `GET` | `/v1/documents/{document_id}/revisions/{revision_id}` | selected immutable view |
| `GET` | `/v1/documents/{document_id}/diff?from=&to=` | structural/text diff |
| `POST` | `/v1/documents/{document_id}/recognitions` | scoped document/page/region/line rerun job |
| `POST` | `/v1/documents/{document_id}/revisions` | create rollback/rebase-derived revision with explicit base/target |
| `GET` | `/v1/engines` | available engines without secrets |
| `GET` | `/v1/capabilities` | API/core capabilities |

List endpoints use opaque cursor pagination: `items`, `next_cursor`. Authorization and rate-limit headers are deployment-profile concerns but errors are standardized.

## CorrectionRequest

```text
CorrectionRequest
  schema_version: "correction/v1"
  base_revision_id: ID
  target: {type, id}
  operation: CorrectionOperation
  payload: CorrectionPayload  # discriminated by operation
  reason?: string
  metadata: map[string, JSON value]
```

The public correction endpoint always derives actor, tenant and source classification (`USER`) from authenticated execution context; it does not accept `TRUSTED_IMPORT` or `AUTOMATED_POSTPROCESSOR` claims. Dedicated internal/import use cases may assign those classifications only from authorized service credentials/routes. Client-supplied claimed attribution, if accepted for an import, is untrusted metadata and never an authorization/audit identity. The server verifies `before` against the base revision and that the target belongs to an authorized document. Stale base returns `REVISION_CONFLICT` with current revision ID; it never silently rebases.

Correction storage never implies training consent. Dataset export uses a separate immutable, purpose/scope/policy-versioned `ConsentGrant` obtained from authenticated identity and revalidated at export time; missing, expired or revoked grants deny export.

### Correction operation payloads

`CorrectionOperation` is a discriminated union; no untyped generic before/after wire payload exists:

| Operation | Required payload |
|---|---|
| `REPLACE_TEXT` | `before_text`, `after_text` |
| `INSERT_TEXT` | anchor target/position, `inserted_text` |
| `DELETE_TEXT` | `before_text` |
| `MERGE_TOKENS` / `MERGE_LINES` | ordered `source_ids`, expected values, resulting value |
| `SPLIT_TOKEN` / `SPLIT_LINE` | expected value, ordered split values/boundaries |
| `CHANGE_REGION_TYPE` | expected and new region enum |
| `CHANGE_READING_ORDER` | parent ID, expected and new ordered child IDs |
| `CHANGE_LANGUAGE` | expected and new BCP-47 values |
| `CHANGE_BBOX` | expected and new normalized geometry |
| `MARK_CORRECT` / `MARK_UNCERTAIN` / `IGNORE` | expected target content hash and optional reason |

Unknown operation or a mismatched payload discriminator is rejected. Server stores canonical before/after values derived from the validated base revision, not trusted client claims.

## Partial rerun and revision commands

`RecognitionScope` is exactly one of `{DOCUMENT, document_id}`, `{PAGE, page_id}`, `{REGION, region_id}`, `{LINE, line_id}` and includes base revision ID plus optional engine/options overrides allowed by policy. The server authorizes target ancestry and returns an async job; completion appends new raw evidence and a revision.

`CreateRevisionRequest` supports `ROLLBACK` with `base_revision_id` (the current optimistic base) and `target_revision_id`. Rollback never moves a pointer backward or deletes later revisions; it appends a new revision whose view equals the authorized target and records provenance.

## Revision and diff responses

```text
RevisionSummary
  schema_version: "revision/v1"
  id, document_id, parent_revision_id?, base_raw_result_id
  kind: MACHINE | CORRECTION | RERUN | ROLLBACK | POSTPROCESSING
  correction_ids[], created_at, actor, content_hash

RevisionView
  revision: RevisionSummary
  result: RecognitionResult

RevisionDiff
  schema_version: "revision-diff/v1"
  from_revision_id, to_revision_id
  operations: list[typed structural/text/layout change]
  summary: added/removed/changed counts
```

Diff operations contain stable/ancestry IDs and typed before/after values. Pagination applies to revision lists and large diff operation lists.

## Jobs and idempotency

`RecognitionJob` exposes `status`, `attempt`, source/document/result IDs in request order, per-source outcome, `current_page`, `total_pages`, `progress_percent`, `current_stage`, timestamps and terminal result/error.

Idempotency uses a two-level contract. Unique identity `(tenant, authenticated principal, operation, idempotency_key)` maps to exactly one stored canonical request hash and authorized result. Same identity + same hash returns that job; same identity + different hash returns `IDEMPOTENCY_CONFLICT` and never creates a second job. A lookup never reveals whether another identity has a hit. Retention duration is deployment-configured and advertised.

Recognition cache is separate: its key includes policy-required tenant/principal, canonical request, privacy mode, schema/pipeline versions and exact engine/model artifact digests. Every cache retrieval is re-authorized and invalidated by deletion/policy/version changes.

## Error envelope

```text
ErrorResponse
  error:
    code: stable machine code
    message: safe human message
    category: VALIDATION | ENGINE | RESOURCE | STORAGE | CONFLICT | SECURITY | INTERNAL
    retryable: boolean
    details: safe structured fields
    correlation_id: opaque ID
```

Minimum codes include those from SPEC plus `CAPABILITY_UNSUPPORTED`, `REVISION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `CANCELLED`, `PRIVACY_MODE_VIOLATION`, `RESOURCE_LIMIT_EXCEEDED`. Stack traces, local paths and recognized content are never returned.

## Local service boundary

Local REST defaults to loopback or local IPC, a generated high-entropy bearer credential (or verified OS peer credential), deny-all CORS and no cookie authentication. Credential bootstrap uses a private permission-checked token file or OS credential store, never command-line arguments or loggable environment output; verification is constant-time and rotation/revocation invalidates prior tokens. Startup fails closed if secure generation/storage cannot be established and refuses wildcard/non-loopback bind unless the remote profile security gate is satisfied. Request body, JSON depth/container/string cardinality and response size limits are enforced before expensive parsing and before serialization.

## Future MCP

Product MCP may expose `recognize_document`, `recognize_region`, `get_recognition`, `list_uncertain_regions`, `apply_correction`, `get_revision`. Each tool delegates to the same application use cases and authorization/privacy policy; no OCR implementation exists in MCP.
