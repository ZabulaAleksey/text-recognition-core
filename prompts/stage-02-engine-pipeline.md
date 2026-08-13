# Stage 02 — Intake, pipeline and baseline OCR

## Goal

Implement safe recognition orchestration and select one local OCR adapter using reproducible evidence.

## Required context

SPEC sections 23–29, 42–50, 59, 62 and `FR-003`, `NFR-001`, `NFR-003`, `PERF-001`, `AC-002`, `AC-005`; architecture engine/intake flows; API engine port; security input/resource rules; test strategy; ADR-007/P01/P02.

## Dependencies

Stage 01 accepted. Approved synthetic/anonymized printed golden slice and evaluation environment.

## Scope

Safe image intake, replaceable preprocessing/layout stages, engine registry/selection/fallback, fake engine, candidate benchmark and exactly one baseline local OCR adapter.

## Tasks

1. Spike and decide PDF/image decoder libraries with license/security/resource evidence; ADR-P01 is not accepted without the isolation gate below.
2. Implement binary decoding, metadata parsing and OCR/model inference in disposable least-privilege subprocess workers (or equivalent sandbox): no network, unprivileged identity, minimal read-only source, private per-job temp root, OS CPU/RSS/file/process limits, hard timeout/kill and crash/cancel cleanup.
3. Implement validation, hashing, derived preprocessing artifacts and reversible coordinate transforms.
4. Implement registry, capability selection, fallback rules and cancellation/resource budgets, including output/artifact/disk quotas.
5. Build shared engine contract suite and fake adapter.
6. Verify signed/digested model/engine manifests and reject unsafe serialization before load.
7. Benchmark local OCR candidates on versioned golden data; record quality/resource report and accept ADR-P02.
8. Integrate only the selected adapter and normalize errors/confidence/provenance.

## Files allowed to change

`pyproject.toml`, dependency lock/SBOM/license artifacts; `src/**/intake/**`, `pipelines/**`, `engines/**`, relevant application orchestration; approved `tests/fixtures/**`, contract/integration/benchmark/security tests; ADR/status/log.

## Files that should not change

Correction/revision implementation, REST/persistent jobs, consumer business models, remote/cloud engines, private fixtures.

## Tests

Engine contract suite, ordered multi-source success/failure under both batch policies, corrupt/oversized/amplifying input/output, coordinate transforms, required/optional capabilities, fallback, deterministic fake pipeline, worker crash/hang/hard-kill/cancel/cleanup/private-root/no-egress, tampered artifact/unsafe serialization, golden CER/WER/layout and latency/memory/disk report.

## Quality gates

`AC-002`, `AC-005`, `AC-007`, `AC-010`; dependency vulnerability/license/provenance scan and lock verification; security review of decoders/adapters and worker isolation; benchmark evidence names dataset and versions; no unsupported accuracy claim; exactly one production baseline OCR adapter.

## Definition of Done

Supported printed input yields a valid immutable raw result offline through ports, and the selected engine decision is reproducible.

## Acceptance Criteria

Engine replacement requires only a new adapter; raw result includes full provenance; invalid inputs fail safely; optional capabilities warn and required capabilities fail explicitly.

## Expected artifacts

Pipeline and adapter code, golden manifest/report, accepted decoder/engine ADRs, contract/security tests.

## Failure / rollback conditions

Stop if no candidate meets an agreed minimum, licenses are incompatible, decoding cannot be isolated/bounded, artifact integrity cannot be verified, or private data appears. Remove the adapter/artifacts and retain the fake contract baseline; do not weaken gates silently.
