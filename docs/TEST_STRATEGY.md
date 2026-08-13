# Test and benchmark strategy

Tests prove the stable requirements in `specs/system.spec.md`; snapshots and benchmarks do not redefine them.

## Test layers

| Layer | Scope | Required evidence |
|---|---|---|
| Unit | value objects, coordinate/confidence normalization, selection, correction operations | fast deterministic tests |
| Domain properties | tree/revision invariants, replay, hashes, stable IDs | property-based cases where useful |
| Engine contract | every `RecognitionEngine` adapter | one parametrized shared suite |
| Integration | intake → pipeline → engine → raw/result; storage/jobs/cancel/idempotency | local deterministic fixtures |
| API/schema | JSON Schema/OpenAPI/error/compatibility | contract snapshots + breaking-change detection |
| Application adapter | Chronicle/Receipt/Tutor projections and provenance | synthetic/anonymized fixtures |
| Golden/regression | OCR/HTR/layout/field quality | versioned report versus baseline |
| Security | hostile input, limits, traversal, egress, leakage, tenant boundaries | negative suite + security review |
| Performance | latency/pages-sec/memory/CPU/GPU/queue | reproducible environment/report |

Pytest is the baseline runner; its fixtures and parametrization support the shared adapter suite (<https://docs.pytest.org/en/stable/>).

## Engine contract suite

For every enabled adapter:

- declared capabilities/languages/version match behavior;
- output IDs/tree/reading order/coordinates are valid;
- confidence is normalized or explicitly unavailable;
- provenance contains engine/model/adapter/config versions;
- required unsupported capability fails explicitly;
- timeout/cancel/resource budget is honored;
- vendor errors map to stable codes without sensitive content;
- `LOCAL_ONLY` rejects nonlocal engines;
- `recognize_region` does not require whole-document rerun;
- repeated deterministic fixture produces schema-equivalent output.

## Correction/revision suite

- raw content hash never changes after correction, rollback or rerun;
- correction `before` and base revision are validated;
- stale base returns conflict;
- replay produces stable content hash/current view;
- split/merge ancestry and old revisions remain addressable;
- partial rerun appends new evidence and revision;
- concurrent correction transaction cannot lose an accepted update.

## Golden dataset policy

Only synthetic, anonymized or explicitly approved data. Manifest records dataset version, license/approval, language/script, document type, expected structure and split. No real private diaries/student work/receipts in public Git. Train, validation and test/golden sets cannot overlap silently.

Initial slices: printed Ukrainian/Russian/English, handwriting, mixed pages, synthetic UA receipts, tutor worksheets and hostile/edge cases. HTR selection is blocked until the handwriting slice is representative.

## Metrics

- OCR/HTR: CER, WER, coverage, low-confidence calibration.
- Layout: region detection/reading order and coordinate validity.
- Receipt projection: field/item/total accuracy with provenance coverage.
- Operations: latency percentiles, pages/sec, peak RSS, CPU/GPU, queue/fallback/error counts.

Stage 02 establishes versioned baselines and proposed numerical budgets. Until then, no unsupported accuracy or throughput claim is a release gate.

## Security tests

Malformed/corrupt formats; request body/JSON depth/cardinality; aggregate multi-page output, tokens/alternatives/text and disk/queue amplification; oversized dimensions/pages/decompression; worker crash/hang/hard-kill/cancel/cleanup and private-root isolation; traversal/symlink; unsafe metadata; parser corpus; no-egress `LOCAL_ONLY`; local wildcard bind, token-file permissions/bootstrap/rotation/revocation/redaction, credential/Origin denial; actor/source-role/target spoofing; consent omission/forgery/expiry/revocation; tampered dependency/model/lock drift/unsafe serialization; telemetry canaries through validation/parser/vendor/audit/rotation; same idempotency identity with same/different request hash proves return/conflict and no duplicate job, separate cache-scope collisions and deletion/`AC-011`; remote SSRF/DNS/redirect/cross-tenant cases before those modes are enabled.

## Quality gates by stage

- Foundation: lint/type/unit/schema/invariant tests plus hash lock, SBOM/license/vulnerability and unsafe-serialization policy checks.
- Engine: shared contract suite + isolated-worker acceptance + golden benchmark + signed/digested artifact and license/security evidence.
- Corrections: replay/property/concurrency/raw immutability.
- Storage/jobs/API: integration, migration/recovery, idempotency/cancel, API compatibility and negative security tests.
- Applications: adapter contract/provenance tests and no domain leakage.
- Release: full relevant suite, benchmark comparison, dependency scan, reviewer, security review; performance review when hot paths change.

## Traceability

Tests reference `FR-*`, `NFR-*`, `SEC-*`, `PERF-*` or `AC-*` in names/markers/report metadata. A requirement is complete only when implemented and linked to automated evidence, or when the documented manual verification explains why automation is unavailable.
