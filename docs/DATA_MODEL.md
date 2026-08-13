# Модель данных

Это логическая доменная модель. Детали хранения могут отличаться, но должны сохранять перечисленные инварианты.

## Карта агрегатов

```text
Document
 ├─ OriginalSource
 ├─ RawRecognitionSnapshot 1..n
 │   └─ Page → Region → Line → Token
 ├─ Correction 0..n
 └─ Revision 1..n

RecognitionJob → request/provenance → result или error
EngineDescriptor → capabilities/version/health
```

## Сущности

### Document

`id`, `source_id`, `input_hash`, `created_at`, `privacy_mode`, `current_revision_id`, `schema_version`. Document владеет историей распознавания, но не производными сущностями приложений-потребителей.

### Page / Region / Line / Token

- Все сущности имеют стабильный `id`, идентификатор родителя, порядок чтения, необязательный confidence и ссылку на provenance.
- Page хранит номер, ширину и высоту в пикселях, поворот и regions.
- Region хранит тип, нормализованный bbox, необязательный polygon, lines и metadata.
- Line хранит bbox, текст и tokens.
- Token хранит текст, bbox, confidence и ранжированные alternatives.
- Производный plain text воспроизводится из упорядоченной структуры и никогда не является единственным сохранённым представлением.

### RawRecognitionSnapshot

`id`, `document_id`, `scope`, `source_hash`, `engine_runs`, `pipeline_version`, `configuration_hash`, `created_at`, неизменяемый корень иерархии и content hash. Операции обновления не существует; повторное распознавание добавляет новый snapshot.

### Correction

`id`, `document_id`, `base_revision_id`, `target_type`, `target_id`, `operation`, `before`, `after`, доверенные `actor_id`/`tenant_id` из execution context, `source`, `timestamp`, `reason`, необязательные недоверенные metadata заявленной атрибуции. Полученная revision ссылается на correction IDs; `base_revision_id` никогда не используется для другой цели. Correction не содержит флаг согласия на обучение.

### Revision

`id`, `document_id`, `parent_revision_id?`, `base_raw_result_id`, упорядоченные `correction_ids`, `created_at`, `created_by`, `kind`, `content_hash`. MVP использует линейную историю с optimistic concurrency; ветвление является будущим расширением схемы.

`Revision 1` представляет машинное состояние без пользовательских исправлений. Текущее представление является детерминированной проекцией, а не изменяемым хранилищем.

### RecognitionJob

`id`, `request_hash`, `idempotency_scope`, `status`, `attempt`, поля прогресса, timestamps, запрос отмены, result/error, использование ресурсов и provenance. Переходы состояний соответствуют `ARCHITECTURE.md`.

### EngineDescriptor / EngineRun

Descriptor: `name`, версия adapter, версии engine/model, capabilities, languages, locality, health. Run: выбранный scope, options hash, начало и окончание, outcome, причина fallback и нормализованные metrics.

### ConsentGrant / ConsentRevocation

Grant: неизменяемые `id`, доверенные subject/tenant, purpose, точный scope документа, региона и данных, разрешённое использование для обработки или export, версия policy/terms, `granted_at`, необязательный `expires_at` и provenance. Revocation: append-only запись с ID разрешения, доверенным actor, временем и причиной. Export-записи фиксируют действующее разрешение и повторно проходят авторизацию при выполнении; отзыв прекращает ожидающее использование и запускает обработку производных exports по retention policy.

## Идентичность после структурных изменений

- Неизменившиеся узлы сохраняют IDs в производной revision.
- Замена текста сохраняет ID цели и записывает correction.
- Split/merge создаёт новые IDs с `derived_from_ids`; старые узлы сохраняются в предыдущих revisions.
- Частичный повторный запуск создаёт новые raw node IDs и `supersedes_ids`; revision определяет текущую проекцию.
- Corrections никогда не ссылаются только на смещения в тексте.

## Координаты

Канонические координаты нормализованы относительно исходной страницы в диапазоне `[0,1]`, начало координат находится в левом верхнем углу. Производные пространства preprocessing записывают обратимые преобразования. Bbox имеет вид `(x, y, width, height)` и должен оставаться внутри страницы; polygon необязателен и не может противоречить bbox сверх заданного допуска.

## Инварианты

- confidence отсутствует либо является конечным числом в `[0,1]`;
- номера страниц уникальны внутри документа; порядок чтения уникален внутри родителя;
- IDs неизменяемы и глобально уникальны в пределах deployment;
- raw content hash изменяется только при добавлении нового snapshot;
- revision принадлежит одному документу и ссылается на существующих предков и цели;
- replay исправлений детерминирован при фиксированных схемах и входе;
- actor, tenant и consent никогда не определяются из заявлений клиента;
- обновление текущей revision и добавление correction выполняются одной транзакцией;
- проекции приложений сохраняют ссылки provenance, но не являются записями, принадлежащими Core.

## Логическое хранение и удаление

Original, raw, corrections/revisions, jobs/cache, logs/audit и производные projections/exports являются отдельными классами хранения. До создания persistence этап 04 обязан определить безопасный срок хранения по умолчанию, permissions/encryption, SLA удаления и поведение backups. Авторизованное удаление создаёт минимизированный auditable tombstone и удаляет настроенные blobs, records, cache, exports, temp и backups согласно политике; общие content-addressed blobs удаляются только после авторизованного подсчёта ссылок. Неизменяемость означает отсутствие скрытой мутации, но не запрет privacy deletion. Training exports являются отдельными артефактами с действующим ConsentGrant и provenance.

## Эволюция схем

Версии API, recognition, correction и persistence schemas развиваются независимо. Добавление необязательных полей обратно совместимо; переименование или удаление полей, изменение семантики enum и координат требуют миграции и тестов совместимости.
