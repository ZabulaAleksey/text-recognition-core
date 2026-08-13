# Модель безопасности и приватности

**Уровень риска:** высокий. TRC принимает потенциально вредоносный бинарный ввод и может обрабатывать дневники, работы учеников, документы и финансовые данные. Эта модель действует до любого открытия удалённого доступа.

## Защищаемые активы

- исходные изображения и PDF, а также производные графические артефакты;
- распознанный текст, alternatives и координаты;
- corrections, идентичность автора и история revisions;
- учётные данные шифрования, auth и engines;
- артефакты моделей, конфигурация и provenance;
- доступность CPU, GPU, памяти, хранилища и workers.

## Границы доверия

```text
недоверенный client/file
  → intake sandbox/validator
  → application/domain
  → local или remote engine adapter
  → storage/job/telemetry adapters
```

Каждый engine, decoder, metadata parser, библиотека archive/PDF и удалённый сервис образуют отдельную границу. Privacy mode является принудительно применяемой политикой, проходящей через весь job, а не подсказкой UI.

## Угрозы и средства защиты

| Угроза | Минимальная защита | Проверка |
|---|---|---|
| усиление объёма request/output/storage | предварительные лимиты request/JSON, а также decoded pixels, regions/tokens/alternatives/text, artifacts/temp/persistent bytes и quotas очереди и пользователя | негативные тесты aggregate/nested/output/disk |
| слишком большое изображение/PDF, decompression bomb | предварительные и потоковые ограничения bytes/pages/pixels/depth; процессный бюджет | негативные resource tests |
| повреждённый ввод parser / decoder RCE | одноразовый subprocess/sandbox с минимальными правами, без сети, с приватным temp root, OS limits и принудительным завершением и очисткой | corpus fuzzing, тесты crash/hang/cleanup |
| path traversal, symlink или temp race | непрозрачные source IDs, канонизированные allowlisted storage roots, приватные случайные temp dirs и атомарная запись | traversal/symlink tests |
| SSRF или неразрешённый egress | отсутствие client URLs; разрешённые scheme/host/port, политика resolved IP, запрет redirects/proxies/caller auth headers; запрет loopback/private/link-local/metadata и сети в `LOCAL_ONLY` | no-egress и DNS/redirect rebinding tests |
| исчерпание ресурсов и злоупотребление API | quotas, ограничения concurrency/memory/time, отмена, ограниченные retries и remote rate limits | load/abuse tests |
| раскрытие данных tenant/user | авторизация на каждый document/job/revision, tenant-scoped keys/storage/cache | cross-tenant негативные тесты до remote mode |
| утечка текста или путей через logs/traces | структурированные allowlist fields, redaction, безопасные ошибки и метрики без содержимого | поиск canary-утечек |
| отравленная модель или dependency | закреплённые hashes/lockfile, доверенный registry, проверка signature/hash, SBOM и scanning | проверки provenance в CI |
| злоупотребление corrections или согласием на dataset | доверенный actor context; неизменяемое, версионированное по purpose/scope/policy разрешение с revocation; авторизация export во время выполнения | тесты forged/stale/revoked consent |
| утечка cache/idempotency | scope по tenant/principal/operation/request/privacy/schema/pipeline и точному digest артефакта; авторизация каждого lookup | тесты isolation/collision/deletion |

## Режимы приватности

- `LOCAL_ONLY`: только локальные engines и storage; network egress отключён для workers, fallbacks, telemetry и проверки обновлений. Невозможность соблюсти политику возвращает `PRIVACY_MODE_VIOLATION`.
- `HYBRID`: только явно разрешённые этапы могут обращаться к утверждённым endpoints; consent/configuration фиксируют destination и класс данных.
- `REMOTE_ALLOWED`: по-прежнему требуются authorization, TLS, minimization, retention и provider policy; режим не является общим согласием на обучение.

Участие в training/dataset отделено от обработки и по умолчанию выключено во всех режимах.

## Контракт ограничения ресурсов

До parsing проверяются: bytes upload/body, глубина JSON, размеры container/string/cardinality, MIME/magic файла и количество страниц, если его можно безопасно определить. Во время обработки и до serialization/persistence проверяются: суммарное число decoded pixels, dimensions, nesting/decompression ratio, regions/tokens/alternatives/text, derived/temp/persistent bytes, queued jobs, per-principal usage, память, wall/CPU time, artifacts и concurrency. Ограничения настраиваются, но имеют безопасные ненулевые defaults; отключение лимита требует явного deployment-решения.

## Хранение и удаление

- originals/raw/corrections/revisions/cache/exports/logs/traces/audit имеют отдельные retention classes и ограниченную кардинальность;
- чувствительные blobs требуют OS permissions; encryption at rest обязателен до remote или multi-user profile;
- секреты находятся вне исходного кода и конфигурационных документов и никогда не записываются в logs;
- удаление авторизуется, аудируется и инвалидирует cache/exports согласно политике;
- backups и копии export подчиняются тому же контракту deletion/retention.

До сохранения данных на этапе 04 ADR-P03 должен определить default retention, решение о локальных permissions/encryption, SLA удаления, обработку ссылок shared blobs, очистку temp/crash, rotations и удаление backup/export. Доступ к observability и exporters задаётся allowlist; содержимое exceptions/vendor payloads и управляющие символы очищаются.

## Проверка локального сервиса

Локальный REST adapter по умолчанию выполняет bind только на loopback или local IPC, аутентифицирует сгенерированный bearer token высокой энтропии или проверенные OS peer credentials, запрещает CORS и не использует cookie sessions. Bootstrap token использует OS credential store или приватный файл с проверенными permissions, но не аргументы CLI или выводимые в logs environment values; проверка выполняется за постоянное время, rotation/revocation инвалидирует старые tokens, а при невозможности безопасного хранения запуск завершается закрытым отказом. Без полного remote gate запуск с wildcard или non-loopback запрещён. Тесты покрывают permissions token-file, bootstrap/rotation/revocation/redaction, неверные и отсутствующие credentials, hostile Origin и отказ wildcard bind.

## Проверка сетевого сервиса

Не открывать remote REST/MCP до определения и негативного тестирования authentication, authorization, tenant isolation, TLS, rate limiting, audit, retention/encryption и incident response. Stack traces и внутренние пути никогда не пересекают границу API.

Remote engine adapters дополнительно по умолчанию запрещают управляемые вызывающей стороной URLs, proxy/auth headers и redirects. Разрешённые endpoints задаются allowlist по scheme/host/port; каждое разрешение имени и соединение отклоняет loopback, private, link-local и metadata ranges и защищается от DNS rebinding.

## Контроль качества безопасности

Любое изменение parsers входа, сети, storage, auth, privacy mode, logging, export, engines/models или resource limits требует трассировки `SEC-*`, негативных тестов, сканирования dependency/security и security review. Начиная с этапа 01 зависимости фиксируются hashes для доверенных indexes и проверяются через SBOM, license и vulnerability checks. Артефакты engine/model до загрузки требуют подписанные или проверенные по digest manifests. Pickle/joblib, unrestricted `torch.load`, unsafe YAML и другая исполняемая или объектная десериализация запрещены, если отдельный ADR о sandboxed conversion не докажет её необходимость. Реальные приватные документы запрещено коммитить в публичный репозиторий.

## Безопасная при инцидентах observability

По умолчанию разрешены: непрозрачные correlation/job/engine IDs, durations, counts, status/error code, суммарное использование ресурсов и bucketed confidence. По умолчанию запрещены: распознанный текст, alternatives, изображения, raw metadata, локальные source paths, авторский текст, tokens и secrets.
