# Этап 04 — Локальное persistence, jobs и REST API

## Цель

Сделать завершённые use cases Core долговечными и асинхронно доступными в local/offline deployment profile.

## Обязательный контекст

Разделы SPEC 37–59 и `FR-007`, `FR-009`, `SEC-002`, `SEC-003`, `SEC-005`; storage/jobs архитектуры; endpoints, errors и idempotency API; инварианты данных; security model; ADR-006/009.

## Зависимости

Приняты этапы 01–03 и стабильные schemas. До любой постоянной записи пользовательских данных необходимо принять ADR-P03, определяющий local retention, permissions/encryption, SLA удаления, очистку temp/crash и поведение logs/audit/rotation/export/backups.

## Область

Metadata SQLite, атомарные blobs файловой системы, unit-of-work, migrations и recovery, постоянный local worker, idempotency/progress/cancel/cache и REST adapter FastAPI. Без remote/multi-tenant profile.

## Задачи

1. Принять ADR-P03, затем определить обратимые schema migrations и adapters repository/blob/cache с правилами retention/deletion/reference count.
2. Реализовать долговечный state machine jobs, attempts, checkpoints cancellation и учёт ресурсов.
3. Реализовать двухуровневую idempotency identity `(tenant, principal, operation, key) → request hash/result`; другой hash вызывает conflict без создания второго job. Отдельно реализовать scoped recognition cache и повторно авторизовать каждый lookup.
4. Добавить handlers REST v1 как тонкие application adapters с безопасными errors и pagination; выполнять bind только на loopback/local IPC, создавать credential высокой энтропии через приватный permission-checked file или OS store, но не CLI или loggable env, проверять за постоянное время, поддерживать rotate/revoke, завершать запуск закрытым отказом при небезопасном storage, запрещать CORS/cookies и отказывать в non-loopback без remote gate.
5. В `LOCAL_ONLY` запрещать весь egress, включая telemetry, fallback и update checks.
6. Применять quotas request/output/disk/queue/cardinality и принятый lifecycle retention/deletion/backup/observability; проверить crash consistency и удаление shared blobs.

## Файлы, которые разрешено изменять

Infrastructure adapters/migrations, jobs, REST interface, deployment/test config, integration/security/API compatibility tests и относящиеся документы.

## Файлы, которые не должны изменяться

Семантика domain без обновления ADR/SPEC; remote auth и multi-tenant deployment; CLI/MCP; projectors consumers.

## Тесты

Migration up/down/recovery, транзакции и удаление atomic/shared blobs и `AC-011`, переходы jobs, retry/cancel, idempotency одинакового key с одинаковым и различным hash с доказательством отсутствия duplicate job, collisions отдельно scoped cache и invalidation удалённого document, REST schema/errors/pagination, permissions/bootstrap/rotation/revocation/redaction token-file, отказ wildcard bind, missing/wrong credentials и hostile Origin, amplification request/output/disk/queue, no-egress, rotation/access/retention log/audit и leakage telemetry.

## Контроль качества

`AC-008`, `AC-009`, `AC-011`; security review; проходят integration/compatibility tests; ADR-P03 принят до постоянных записей; injection failure не оставляет видимого dangling state; авторизованное удаление соблюдает SLA для всех retention classes; нет утечек stack/path/content; non-loopback startup запрещён без remote gate.

## Определение готовности

Локальный client может через REST отправить, отслеживать, отменить и получить persistent result распознавания или correction с состоянием, переживающим restart, и принудительно применяемой offline privacy.

## Критерии приёмки

`FR-007`, `FR-009`, `AC-004`, `AC-011`; семантика duplicate key и terminal states соответствует API; retention classes source/raw/revision остаются разделёнными; авторизованное удаление полно, а preprocessing/corrections не могут его инициировать.

## Ожидаемые артефакты

Migrations, local adapters/worker, REST v1/OpenAPI, recovery/security tests, operating notes и обновления status/log.

## Условия остановки и отката

Остановиться при необратимой migration, видимых после crash частичных writes, неограниченном worker, privacy egress или небезопасном external bind. Восстановить backup DB до этапа и отменить code/migration; не включать remote mode.
