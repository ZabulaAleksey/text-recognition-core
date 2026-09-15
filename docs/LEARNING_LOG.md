# Learning log

## Почему КАРКАС не содержит `src/`

В этой задаче КАРКАС означает living development contract: он превращает широкую SPEC в архитектурные границы, контракты, решения, проверяемые этапы и context routing. Если сразу написать OCR code, пришлось бы неявно выбрать engine, coordinate semantics, persistence и privacy behavior до согласования их контрактов. Поэтому product implementation начинается отдельным Stage 01.

## Почему library-first modular monolith

TRC должен работать embedded/offline и как service. Framework-neutral domain/application позволяет сначала проверить модель локально, а REST/CLI/MCP оставить тонкими interfaces. Modular monolith сохраняет границы без преждевременной распределённой инфраструктуры; ports дают возможность позже заменить SQLite, worker или engine.

## Почему raw и revision разделены

Raw recognition — evidence конкретного engine/pipeline. Пользовательское исправление — новая информация, а не доказательство того, что engine изначально распознал иначе. Append-only corrections и deterministic revisions дают audit, rollback, comparison и training feedback без потери исходного результата.

## Почему engine не выбран сейчас

Наличие известного OCR engine не доказывает его качество на украинских чеках, смешанных страницах или доступном CPU. Stage 02 сравнивает кандидатов на versioned golden data по CER/WER/layout, latency, memory, offline support, license и security surface. Это превращает технологический выбор в воспроизводимое решение.

## Как продолжить самостоятельно

1. Прочитать выбранный record `docs/STAGES.md` и относящиеся sections `specs/system.spec.md`.
2. Проверить readable Stage 01 contract и approvals до реализации; исторический catalog из `docs/notes/` не использовать как launcher.
3. Создать отдельную feature branch от принятого `main`.
4. Реализовать только разрешённые области и связать тесты с IDs требований.
5. Выполнить stage tests/review, обновить status/logs и сделать один логический commit.
6. Попросить review и отдельное разрешение на merge; не переходить автоматически к Stage 02.
