# Текущий исполняемый срез — этап 02, pure engine routing

**Состояние:** независимый planning slice Stage 02 реализуется после локально проверенного
Stage 01. Контракт: `specs/features/engine-routing.spec.md`. Полный Stage 02 остаётся
открытым до worker isolation, golden benchmark и одного выбранного OCR adapter.

## Задача текущего среза

Сделать immutable registry descriptors и детерминированный выбор кандидатов OCR/HTR
для регионов. `LOCAL_ONLY` исключает remote engines, явный выбор не допускает
скрытого fallback. Планировщик не исполняет binary decoder, модель или сеть.

## Проверки текущего среза

Unit tests для порядка, capability/privacy отказов и маршрутизации регионов;
полный unit/schema suite Stage 01, Ruff и strict mypy. После этого сохранится
граница между локальным routing plan и фактическим OCR runtime.

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
