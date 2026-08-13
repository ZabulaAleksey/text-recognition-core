# Stage 01 — Foundation and typed contracts

## Goal

Create a Python library foundation and immutable typed contracts for the Core without product integrations.

## Required context

`AGENTS.md`; SPEC sections 7–16, 40, 56–58 and IDs `FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `AC-001`; `docs/ARCHITECTURE.md`, `API.md`, `DATA_MODEL.md`, ADR-002–005; current `AI_STATUS`/`AI_PLAN`.

## Dependencies

Accepted KАРКАС; supported Python 3.13 environment. No earlier code stage.

## Scope

Packaging, domain values/entities, application ports, schema boundary, deterministic IDs/clock ports, in-memory test doubles and foundational tests.

## Tasks

1. Create `pyproject.toml` and `src/` package boundaries matching architecture.
2. Implement strict immutable value types for IDs, coordinates, confidence, modes/capabilities/privacy, errors and provenance.
3. Implement typed request/result and Document/Page/Region/Line/Token contracts; separate raw/current revision IDs.
4. Define framework-neutral engine/storage/job/cancellation ports without concrete adapters.
5. Generate JSON Schema from one boundary model source and add version/compatibility fixture.
6. Add architecture/import-boundary and domain invariant tests.
7. Create a hash-locked dependency set, trusted-index policy and initial SBOM/license/vulnerability/unsafe-deserialization checks.

## Files allowed to change

Packaging files; `src/text_recognition_core/domain/**`, `application/**`, `schemas/**`; `tests/unit/**`, `tests/contracts/schema/**`; factual status/decision/log docs.

## Files that should not change

SPEC behavior; engine/storage/REST/application-adapter implementation; golden/private fixtures; global workspace configuration.

## Tests

Strict valid/invalid schema cases including single/batch requests and both batch policies, JSON depth/cardinality/body/response boundaries, nested hierarchy, coordinate bounds, finite confidence, reading order/ID rules, error serialization, generated schema snapshot, forbidden infrastructure imports, lock drift and forbidden executable/object serialization.

## Quality gates

Formatter/linter/type checker/test suite pass; no framework/OCR/database imports in domain/application; public contracts trace to scoped requirement IDs; dependency hashes/SBOM/license/vulnerability evidence exists from the first installable package.

## Definition of Done

Package installs locally, contracts can validate/serialize representative examples, schema generation is deterministic and all ports lack infrastructure implementation.

## Acceptance Criteria

`AC-001`, `AC-010`; architectural `NFR-002`; explicit API/schema versions and raw/current ID separation.

## Expected artifacts

Python package skeleton, generated schema fixtures, tests, updated factual status/log and any necessary ADR refinement.

## Failure / rollback conditions

Stop if contracts require changing SPEC semantics, if one model truth cannot generate schemas, or if domain requires a framework import. Roll back the stage commit; no migration/external state is allowed.
