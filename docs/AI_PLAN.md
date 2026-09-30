# Текущий исполняемый срез — этап 02, synthetic printed golden smoke

**Состояние:** независимый planning slice Stage 02 реализуется после локально проверенного
Stage 01. Pure routing и bounded synthetic printed golden smoke проверены локально; контракты: `specs/features/engine-routing.spec.md` и `specs/features/printed-golden-smoke.spec.md`. Полный Stage 02 остаётся открытым до worker isolation, репрезентативного golden benchmark и одного выбранного OCR adapter.

## Результат текущего среза

Immutable registry descriptors и детерминированный OCR/HTR routing уже проверены. Добавлены три trusted synthetic printed images, manifest с digest и фиксированный local Tesseract smoke без активации production engine. Следующий Stage 02 slice требует isolated binary decoder/worker и репрезентативный golden dataset.

## Проверки текущего среза

39 unit/schema/contract tests PASS, Ruff check/format и strict mypy PASS. Локальный Tesseract smoke дал CER/WER 0 на трёх простых изображениях. Это не worker-isolation и не representative quality gate.

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
