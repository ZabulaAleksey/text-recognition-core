# Stage 03 — Corrections, revisions and partial rerun

## Goal

Implement append-only human correction and deterministic revision behavior without mutating recognition evidence.

## Required context

SPEC sections 17–23, 55–57 and `FR-004`–`FR-006`, `AC-003`; correction flow in architecture; API CorrectionRequest; data model identity/revision invariants; ADR-005.

## Dependencies

Stages 01–02 accepted; raw snapshots and region recognition ports available.

## Scope

Correction operations, target validation, optimistic linear revisions, replay/current view/diff/rollback, split/merge ancestry and scoped re-recognition orchestration using in-memory repositories first.

## Tasks

1. Implement typed correction operations and before/base validation.
2. Append revisions atomically through a unit-of-work port; reject stale bases.
3. Implement deterministic replay, current projection, structural/text diff and rollback-as-new-revision.
4. Preserve/derive IDs for replace/split/merge and maintain ancestry.
5. Make partial rerun append raw evidence and a revision without overwriting earlier results.
6. Derive actor/tenant/source from trusted route/service execution context; public corrections are always `USER`, reject source-role spoofing/cross-document target and keep claimed import attribution untrusted.
7. Add immutable purpose/scope/policy-versioned consent grants and revocations separate from corrections; export re-authorizes at execution.

## Files allowed to change

Domain/application correction/revision modules, in-memory repositories, relevant schemas and unit/property/integration tests; factual docs.

## Files that should not change

Engine vendor adapter unless a contract bug is proven; persistent DB/REST; application projectors; raw snapshot update semantics.

## Tests

All correction operations, replay determinism, raw hash preservation, stale/concurrent base, rollback, diff, split/merge ancestry, partial rerun, spoofed actor/source role/cross-document target and omitted/forged/stale/revoked consent.

## Quality gates

`AC-003`; property/replay/concurrency tests; reviewer verifies no mutation path to raw evidence and no offset-only targets.

## Definition of Done

Users can correct/confirm a token or line, inspect revisions/diff, roll back and rerun a scope while every prior raw/revision remains addressable and actor/consent provenance remains trusted/auditable.

## Acceptance Criteria

Raw hash is unchanged; replay hash is stable; stale base is explicit; new structural IDs link to ancestry; training/export use requires a valid revocable grant and remains opt-in.

## Expected artifacts

Correction/revision services and schemas, in-memory implementation, replay/property tests and updated status/log.

## Failure / rollback conditions

Stop on nondeterministic replay, ambiguous target identity, lost concurrent update or any raw overwrite. Revert the stage commit; no persistent migration exists yet.
