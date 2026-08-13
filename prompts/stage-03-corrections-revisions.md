# Этап 03 — Corrections, revisions и частичный повторный запуск

## Цель

Реализовать append-only пользовательские исправления и детерминированное поведение revisions без изменения доказательств распознавания.

## Обязательный контекст

Разделы SPEC 17–23, 55–57 и `FR-004`–`FR-006`, `AC-003`; поток corrections в архитектуре; `CorrectionRequest` из API; инварианты identity/revision модели данных; ADR-005.

## Зависимости

Приняты этапы 01–02; доступны raw snapshots и ports распознавания regions.

## Область

Операции corrections, validation target, оптимистичные линейные revisions, replay/current view/diff/rollback, ancestry split/merge и orchestration повторного распознавания scope сначала с in-memory repositories.

## Задачи

1. Реализовать типизированные операции corrections и validation before/base.
2. Атомарно добавлять revisions через port unit-of-work; отклонять устаревшие bases.
3. Реализовать детерминированные replay, current projection, структурный и текстовый diff и rollback как новую revision.
4. Сохранять или создавать IDs для replace/split/merge и поддерживать ancestry.
5. При partial rerun добавлять raw evidence и revision без перезаписи предыдущих results.
6. Получать actor/tenant/source из доверенного execution context route/service; публичные corrections всегда имеют `USER`, подмена source role и cross-document target отклоняется, заявленная import attribution остаётся недоверенной.
7. Добавить отдельные от corrections неизменяемые grants и revocations consent, версионированные по purpose/scope/policy; export повторно авторизуется при выполнении.

## Файлы, которые разрешено изменять

Domain/application modules corrections/revisions, in-memory repositories, относящиеся schemas и unit/property/integration tests; фактическая документация.

## Файлы, которые не должны изменяться

Vendor adapter engine, если не доказан дефект контракта; persistent DB/REST; application projectors; семантика обновления raw snapshot.

## Тесты

Все операции corrections, детерминированность replay, сохранение raw hash, устаревшая и конкурентная base, rollback, diff, ancestry split/merge, partial rerun, подмена actor/source role/cross-document target и отсутствующий, поддельный, устаревший или отозванный consent.

## Контроль качества

`AC-003`; property/replay/concurrency tests; reviewer подтверждает отсутствие пути изменения raw evidence и targets, основанных только на offsets.

## Определение готовности

Пользователь может исправить или подтвердить token или line, просмотреть revisions и diff, выполнить rollback и повторно распознать scope, при этом все предыдущие raw/revisions остаются доступными, а provenance actor/consent — доверенным и пригодным для аудита.

## Критерии приёмки

Raw hash не изменяется; hash replay стабилен; устаревшая base сообщается явно; новые структурные IDs связаны с ancestry; использование для training/export требует действующий отзываемый grant и остаётся opt-in.

## Ожидаемые артефакты

Services и schemas corrections/revisions, in-memory implementation, replay/property tests и обновлённые status/log.

## Условия остановки и отката

Остановиться при недетерминированном replay, неоднозначной target identity, потерянном конкурентном обновлении или любой перезаписи raw. Отменить commit этапа; persistent migration ещё не существует.
