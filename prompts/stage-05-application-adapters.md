# Этап 05 — Adapters приложений

## Цель

Подключить трёх первоначальных consumers через отдельные input profiles и output projectors с полным provenance и без утечки домена Core.

## Обязательный контекст

Разделы SPEC 24, 33–36, 67, 82–83 и `FR-008`, `AC-006`; `docs/INTEGRATIONS.md`, контракты result/data и стратегия integration tests; ADR-008.

## Зависимости

Стабильный API recognition/revision из этапов 01–04.

## Область

Integration packages/contracts и синтетические fixtures adapters для Personal Chronicle, Receipt Scanner и Tutor. Изменения приложений-consumers требуют отдельных задач в их репозиториях.

## Задачи

1. Реализовать общий контракт profile/projector и validation version/provenance.
2. Реализовать проекцию Chronicle без логики RAG/timeline/summary.
3. Реализовать проекцию extraction чеков со ссылками amount/item/source и явной неоднозначностью.
4. Реализовать проекцию regions Tutor без логики student/grading/solution.
5. Добавить проверки dependencies, запрещающие entities/services consumers внутри Core.
6. Опубликовать пример подключения четвёртого consumer через существующие contracts.

## Файлы, которые разрешено изменять

Integration packages, принадлежащие им schemas, синтетические fixtures, adapter/contract tests и документация интеграций.

## Файлы, которые не должны изменяться

Vocabulary домена Core, семантика OCR pipeline и corrections, репозитории consumers, приватные пользовательские данные и неподдерживаемые math/business features.

## Тесты

Детерминированные projections, покрытие provenance, поля low-confidence/missing/ambiguous, privacy profiles, schema versioning и проверки запрещённых dependencies/imports.

## Контроль качества

`AC-006`; 100% заполненных производных полей имеют действующие source references или явный derived provenance; в integrations отсутствует прямой OCR SDK; в Core отсутствуют business services consumers.

## Определение готовности

Все три projections принимают один стабильный result, а пример нового consumer добавляется без изменения contracts Core.

## Критерии приёмки

Суммы чека трассируются к tokens/regions, Chronicle поддерживает `LOCAL_ONLY`, Tutor явно деградирует неподдерживаемую необязательную capability, а mapping adapter никогда не перезаписывает raw text.

## Ожидаемые артефакты

Три версионированных integration packages/contracts, синтетические fixtures/tests, документация onboarding и обновление status/log.

## Условия остановки и отката

Остановиться, если projection требует business logic consumer внутри Core или неверсионированного изменения public contract. Отменить только затронутый integration package; Core остаётся пригодным для использования.
