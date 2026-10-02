# Текущий исполняемый срез — этап 02, synthetic printed golden smoke and byte envelope

- `TRC-NIGHT-JSON-DUPLICATE-01` — VERIFIED LOCALLY / INTEGRATION_PENDING. Public request/result byte parsers reject duplicate decoded JSON keys at every nesting level before unchanged Pydantic JSON validation; duplicate privacy policy values cannot select the later value. Twelve new regressions PASS; full75 PASS, Ruff check/format55 files and strict mypy11 source files PASS. Existing tests/schemas/dependencies unchanged. Validation used existing locked `--no-sync` environment Python3.13.7 with its retained3.13.6 marker warning; no fresh restore claimed. SPEC: `specs/features/json-boundary-validation.spec.md`. Stage02 remains PARTIAL; this does not activate engine/transport or prove egress isolation. Remote canonical documentation convergence is required before publication.

**Состояние:** независимый planning slice Stage 02 реализуется после локально проверенного
Stage 01. Pure routing, bounded synthetic printed golden smoke, joint stdout/stderr capture limit, and byte envelope проверены локально; контракты: `specs/features/engine-routing.spec.md`, `specs/features/printed-golden-smoke.spec.md` и `specs/features/source-byte-envelope.spec.md`. Полный Stage 02 остаётся открытым до worker isolation, репрезентативного golden benchmark и одного выбранного OCR adapter.

## Результат текущего среза

Immutable registry descriptors и детерминированный OCR/HTR routing уже проверены. Добавлены три trusted synthetic printed images, manifest с digest и фиксированный local Tesseract smoke без активации production engine. Pre-decoder bounded byte envelope is verified; next Stage 02 slice requires isolated binary decoder/worker и репрезентативный golden dataset.

## Проверки текущего среза

63 unit/schema/contract tests PASS via `uv run --locked --offline --no-sync` using the existing project environment; Ruff check/format and strict mypy PASS. Seven real-child subprocess regressions cover joint stdout/stderr overflow and boundary, invalid UTF-8, sanitized process-start errors, timeout/reap and read-failure/reap. Локальный Tesseract smoke дал CER/WER 0 на трёх простых изображениях. This remains a tiny developer diagnostic and is not worker isolation or a representative quality gate. The no-sync run warned that the environment uses Python 3.13.7 while its creation marker records 3.13.6; normal uv sync was blocked by protected cache/project-venv metadata ACLs, so no fresh locked restore is claimed.

## Предыдущий завершённый срез — этап 01

**Состояние:** Stage 01 verified locally в `feature/trc-stage-01-foundation` после
прямого запроса NIGHT RUN V2. Verification evidence и следующие границы — `docs/AI_STATUS.md`.

## Цель

Создать ориентированный на библиотечное использование фундамент Python и типизированные, не зависящие от фреймворка контракты без интеграции реального OCR-engine, REST, базы данных или очереди.

## Охватываемые требования

`FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `SEC-009`, `AC-001`, `AC-010`.

## Планируемые области файлов

- упаковка и конфигурация;
- `src/text_recognition_core/domain/`;
- ports и границы use cases в `src/text_recognition_core/application/`;
- сгенерированные граничные схемы в `src/text_recognition_core/schemas/`;
- `tests/unit/`, `tests/contracts/schema/`.

## Обязательные проверки

Следовать stage-01 record в `prompts/STAGES.md`. Тесты должны доказать строгую
валидацию, включая ограничения контейнеров и кардинальности, инварианты иерархии,
координат и confidence, согласованность сгенерированных схем, запрет инфраструктурных
импортов, целостность зависимостей с закреплёнными хешами и запрет небезопасной
десериализации. Обновлять этот план и статус только по фактическим результатам.

## Откат

Отменить commit этапа 01; миграции и внешнее состояние в этом срезе запрещены.
