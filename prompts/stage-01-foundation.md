# Этап 01 — Фундамент и типизированные контракты

## Цель

Создать фундамент Python-библиотеки и неизменяемые типизированные контракты Core без продуктовых интеграций.

## Обязательный контекст

`AGENTS.md`; разделы SPEC 7–16, 40, 56–58 и IDs `FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `AC-001`; `docs/ARCHITECTURE.md`, `API.md`, `DATA_MODEL.md`, ADR-002–005; текущие `AI_STATUS` и `AI_PLAN`.

## Зависимости

Принятый КАРКАС и поддерживаемая среда Python 3.13. Предыдущих этапов кода нет.

## Область

Упаковка, domain values/entities, application ports, граница schema, ports детерминированных IDs и clock, in-memory test doubles и фундаментальные тесты.

## Задачи

1. Создать `pyproject.toml` и границы пакета `src/`, соответствующие архитектуре.
2. Реализовать строгие неизменяемые value types для IDs, coordinates, confidence, modes/capabilities/privacy, errors и provenance.
3. Реализовать типизированные контракты request/result и Document/Page/Region/Line/Token; разделить IDs raw и current revision.
4. Определить независимые от фреймворка ports engine/storage/job/cancellation без конкретных adapters.
5. Генерировать JSON Schema из одного источника boundary models и добавить fixture версии и совместимости.
6. Добавить тесты границ architecture/import и domain invariants.
7. Создать набор dependencies с закреплёнными hashes, политику доверенных indexes и первоначальные проверки SBOM/license/vulnerability/unsafe deserialization.

## Файлы, которые разрешено изменять

Файлы упаковки; `src/text_recognition_core/domain/**`, `application/**`, `schemas/**`; `tests/unit/**`, `tests/contracts/schema/**`; фактические документы status/decision/log.

## Файлы, которые не должны изменяться

Поведение SPEC; реализация engine/storage/REST/application adapters; golden/private fixtures; глобальная конфигурация workspace.

## Тесты

Строгие допустимые и недопустимые случаи schema, включая одиночные и batch requests и обе batch policies, границы глубины и cardinality JSON, body и response, вложенную иерархию, границы coordinates, конечный confidence, правила reading order и IDs, serialization errors, snapshot сгенерированной schema, запрещённые imports infrastructure, lock drift и запрещённую исполняемую или объектную serialization.

## Контроль качества

Проходят formatter, linter, type checker и test suite; в domain/application отсутствуют imports framework/OCR/database; public contracts трассируются к IDs требований текущей области; с первого устанавливаемого пакета существуют подтверждения hashes dependencies, SBOM, licenses и vulnerabilities.

## Определение готовности

Пакет устанавливается локально, contracts могут валидировать и сериализовать репрезентативные примеры, генерация schema детерминирована, а все ports не имеют реализации infrastructure.

## Критерии приёмки

`AC-001`, `AC-010`; архитектурное `NFR-002`; явные версии API/schema и разделение raw/current IDs.

## Ожидаемые артефакты

Каркас пакета Python, fixtures сгенерированных schemas, tests, обновлённые по фактам status/log и необходимые уточнения ADR.

## Условия остановки и отката

Остановиться, если contracts требуют изменить семантику SPEC, если один источник models не может генерировать schemas или если domain требует import фреймворка. Отменить commit этапа; миграции и внешнее состояние запрещены.
