# Этапы Text Recognition Core

- Stage ID: TRC-01-FOUNDATION

## TRC-01-FOUNDATION — библиотечный фундамент

- Status: blocked
- Condition: продуктовой реализации и test environment ещё нет; пользователь не принял КАРКАС и не запустил Stage 01; старый подробный stage launcher содержит mojibake, а ссылка на `stage-01-foundation.md` отсутствовала уже в GitHub main. Completion claim запрещён.
- Plan: после явного запуска уточнить читаемый Stage 01 contract по `specs/system.spec.md`, `docs/ROADMAP.md` и принятым ADR; затем создать Python 3.13 library-first domain/application ports и strict schemas без OCR engine, REST, БД или queue. Requirements: `FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `SEC-009`, `AC-001`, `AC-010`. Проверки должны охватить контейнеры/кардинальность, координаты/confidence, scheme consistency, import boundary, hash-locked dependencies и запрет unsafe deserialization.
- Evidence: read-only brownfield reconcile BROWNFIELD; GitHub main `7e46a05`; нет src/tests/package manifest. Старые source SHA/facts сохранены в `docs/notes/legacy-ai-state-evidence.md`, полный исходный catalog в `docs/notes/legacy-stage-contracts.md`, launcher index в `docs/notes/legacy-prompt-launcher.md`; Git parent является rollback point.
- NEXT: TRC-01-CONTRACT-AND-APPROVAL
- Blockers: нет явного запуска Stage 01 и readable полного контракта; старый launcher повреждён и целевой файл отсутствовал до миграции.
- USER action `TRC-01-APPROVAL`: PENDING; после review КАРКАСА явно поручить начать Stage 01; evidence — утверждённый scope/contract и команда пользователя; unlock — limited Stage 01 implementation.
- USER action `TRC-MERGE-DOCS`: PENDING; после публикации этой документационной ветки явно разрешить merge в `main`; evidence — GitHub default-branch read-back только `docs/STAGES.md`; unlock — удаление полностью слитой ветки.

## Поздние этапы

- Stage 02 — printed OCR engine/pipeline после approved golden benchmark и engine ADR.
- Stage 03 — append-only corrections/revisions/rerun после stable raw contract.
- Stage 04 — local persistence/jobs/REST после retention/deletion ADR.
- Stage 05 — consumer integration adapters после stable result/revision API.
- Stage 06 — HTR/mixed routing и hardening после репрезентативного benchmark.
- Stage 07 — CLI/MCP/remote профили необязательны, требуют отдельной SPEC и security decisions.
