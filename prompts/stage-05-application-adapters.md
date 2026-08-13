# Stage 05 — Application adapters

## Goal

Connect the three initial consumers through separate input profiles and output projectors with complete provenance and no Core domain leakage.

## Required context

SPEC sections 24, 33–36, 67, 82–83 and `FR-008`, `AC-006`; `docs/INTEGRATIONS.md`, result/data contracts and integration test strategy; ADR-008.

## Dependencies

Stable recognition/revision API from Stages 01–04.

## Scope

Integration packages/contracts and synthetic adapter fixtures for Personal Chronicle, Receipt Scanner and Tutor. Consumer application changes require separate repository tasks.

## Tasks

1. Implement common profile/projector contract and version/provenance validation.
2. Implement Chronicle projection without RAG/timeline/summary logic.
3. Implement receipt extraction projection with amount/item/source links and explicit ambiguity.
4. Implement Tutor region projection without student/grading/solution logic.
5. Add dependency checks preventing consumer entities/services inside Core.
6. Publish onboarding example for a fourth consumer through existing contracts.

## Files allowed to change

Integration packages, schemas owned by those packages, synthetic fixtures, adapter/contract tests and integration docs.

## Files that should not change

Core domain vocabulary, OCR pipeline/correction semantics, consumer repositories, private user data, unsupported math/business features.

## Tests

Deterministic projections, provenance coverage, low-confidence/missing/ambiguous fields, privacy profiles, schema versioning and forbidden dependency/import checks.

## Quality gates

`AC-006`; 100% populated derived fields have valid source references or explicit derived provenance; no direct OCR SDK in integrations; no consumer business service in Core.

## Definition of Done

All three projections consume the same stable result and a sample new consumer can be added without changing Core contracts.

## Acceptance Criteria

Receipt amounts trace to tokens/regions, Chronicle supports `LOCAL_ONLY`, Tutor degrades unsupported optional capability explicitly, and adapter mapping never overwrites raw text.

## Expected artifacts

Three versioned integration packages/contracts, synthetic fixtures/tests, onboarding documentation and status/log update.

## Failure / rollback conditions

Stop if a projection requires consumer business logic in Core or an unversioned public contract change. Revert only the affected integration package; Core remains usable.
