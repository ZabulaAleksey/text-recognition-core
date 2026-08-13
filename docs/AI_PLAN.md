# Current executable slice — Stage 01

**State:** ready, not started. Execute only after user accepts the KАРКАС and asks to begin Stage 01.

## Goal

Create the library-first Python foundation and typed framework-neutral contracts without integrating a real OCR engine, REST, database or queue.

## Requirement scope

`FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `SEC-009`, `AC-001`, `AC-010`.

## Planned file areas

- packaging/configuration;
- `src/text_recognition_core/domain/`;
- `src/text_recognition_core/application/` ports/use-case boundaries;
- `src/text_recognition_core/schemas/` generated boundary schemas;
- `tests/unit/`, `tests/contracts/schema/`.

## Gates

Follow `prompts/stage-01-foundation.md`. Tests must prove strict validation including container/cardinality boundaries, hierarchy/coordinate/confidence invariants, generated schema consistency, forbidden infrastructure imports, hash-locked dependency integrity and unsafe-deserialization denial. Update this plan/status only with factual results.

## Rollback

Revert the Stage 01 commit; no migrations or external state are permitted in this slice.
