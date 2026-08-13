# Data model

This is the logical domain model. Persistence details may differ but must preserve these invariants.

## Aggregate map

```text
Document
 ├─ OriginalSource
 ├─ RawRecognitionSnapshot 1..n
 │   └─ Page → Region → Line → Token
 ├─ Correction 0..n
 └─ Revision 1..n

RecognitionJob → request/provenance → result or error
EngineDescriptor → capabilities/version/health
```

## Entities

### Document

`id`, `source_id`, `input_hash`, `created_at`, `privacy_mode`, `current_revision_id`, `schema_version`. Document owns recognition history, not consumer-derived entities.

### Page / Region / Line / Token

- All have stable `id`, parent ID, reading order, optional confidence and provenance reference.
- Page stores number, pixel width/height, rotation and regions.
- Region stores type, normalized bbox, optional polygon, lines and metadata.
- Line stores bbox, text and tokens.
- Token stores text, bbox, confidence and ranked alternatives.
- Derived plain text is reproducible from ordered structure and never the only stored representation.

### RawRecognitionSnapshot

`id`, `document_id`, `scope`, `source_hash`, `engine_runs`, `pipeline_version`, `configuration_hash`, `created_at`, immutable hierarchy root and content hash. No update operation exists; re-recognition appends another snapshot.

### Correction

`id`, `document_id`, `base_revision_id`, `target_type`, `target_id`, `operation`, `before`, `after`, trusted `actor_id`/`tenant_id` from execution context, `source`, `timestamp`, `reason`, optional untrusted claimed-attribution metadata. The resulting revision references correction IDs; `base_revision_id` is never overloaded. Correction has no training-consent flag.

### Revision

`id`, `document_id`, `parent_revision_id?`, `base_raw_result_id`, ordered `correction_ids`, `created_at`, `created_by`, `kind`, `content_hash`. MVP uses a linear optimistic-concurrency history; branching is a future schema extension.

`Revision 1` is the machine view with no user corrections. Current view is a deterministic projection, not mutable storage.

### RecognitionJob

`id`, `request_hash`, `idempotency_scope`, `status`, `attempt`, progress fields, timestamps, cancellation request, result/error, resource usage and provenance. State transitions follow `ARCHITECTURE.md`.

### EngineDescriptor / EngineRun

Descriptor: `name`, adapter version, engine/model versions, capabilities, languages, locality, health. Run: selected scope, options hash, start/end, outcome, fallback reason and normalized metrics.

### ConsentGrant / ConsentRevocation

Grant: immutable `id`, trusted subject/tenant, purpose, exact document/region/data scope, allowed processing/export use, policy/terms version, `granted_at`, optional `expires_at` and provenance. Revocation: append-only grant ID, trusted actor, time and reason. Export records snapshot the valid grant and re-authorize at execution; revocation invalidates pending use and triggers derived-export handling under retention policy.

## Identity after structural edits

- Unchanged nodes retain IDs in a derived revision.
- Replace text retains target ID and records correction.
- Split/merge creates new IDs with `derived_from_ids`; old nodes remain in earlier revisions.
- Partial rerun produces new raw node IDs and `supersedes_ids`; revision decides the current projection.
- Corrections never refer only to text offsets.

## Coordinates

Canonical coordinates are normalized to the original page `[0,1]`, top-left origin. Derived preprocessing spaces record reversible transforms. Bbox is `(x, y, width, height)` and must remain inside the page; polygon is optional and cannot contradict bbox beyond defined tolerance.

## Invariants

- confidence is absent or finite in `[0,1]`;
- page numbers unique per document; reading order unique within a parent;
- IDs are immutable and globally unique within a deployment;
- raw content hash changes only by appending a new snapshot;
- a revision belongs to one document and references existing ancestors/targets;
- correction replay is deterministic for fixed schemas and input;
- actor/tenant/consent identity is never derived from client claims;
- current revision update and correction append are one transaction;
- application projections keep provenance links but are not Core-owned records.

## Logical persistence and deletion

Original, raw, corrections/revisions, jobs/cache, logs/audit and derived projections/exports are separate retention classes. Stage 04 must decide safe default retention, permissions/encryption, deletion SLA and backup behavior before persistence. Authorized deletion creates a minimized auditable tombstone and removes configured blobs/records/cache/exports/temp/backups according to policy; shared content-addressed blobs are deleted only after authorized reference accounting. Immutable means no silent mutation, not immunity from privacy deletion. Training exports are separate artifacts with a currently valid consent grant and provenance.

## Schema evolution

API, recognition, correction and persistence schema versions evolve independently. Additive optional fields are backward-compatible; renamed/removed fields, enum semantic changes and coordinate changes require migration plus compatibility tests.
