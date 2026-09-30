# Контракты API

**Статус:** Stage 01 содержит Pydantic v2 `RecognitionRequest`/`RecognitionResult` и две
генерируемые JSON Schema v1. REST/OpenAPI и application use cases ещё не созданы.
Boundary models являются источником схем; ручная параллельная схема запрещена.
`parse_request_json`/`parse_result_json` — публичные byte-bounded validation entrypoints;
они возвращают только редактированные machine-readable codes при ошибке. Transport
adapter не должен логировать raw `ValidationError`, request body или распознанный текст.

## Соглашения

- JSON использует `snake_case`, UTF-8 и timestamps UTC по RFC 3339.
- IDs являются непрозрачными стабильными строками; clients не разбирают их формат.
- Координаты используют нормализованное пространство страницы `[0.0, 1.0]` с началом в левом верхнем углу; точки polygon следуют порядку чтения. Размеры Page в пикселях сохраняются для рендеринга.
- Confidence находится в диапазоне `0.0..1.0` либо отсутствует с явным объяснением; sentinel values запрещены.
- Неизвестный enum или capability в request отклоняется в v1. В response разрешены новые дополнительные поля; изменение семантики требует новой версии schema/API.

## RecognitionRequest

```text
RecognitionRequest
  schema_version: "recognition-request/v1"
  sources: list[SourceRef]  # от 1 до настроенного batch limit
  batch_policy: ALL_OR_NOTHING | ALLOW_PARTIAL
  mode: AUTO | OCR | HTR | MIXED
  languages: list[BCP-47]
  capabilities: list[CapabilityRequirement]
  privacy_mode: LOCAL_ONLY | HYBRID | REMOTE_ALLOWED
  preprocessing: PreprocessingOptions
  engine_preferences: EnginePreferences
  output: OutputOptions
  context: map[string, JSON value]
  idempotency_key?: string
```

Каждая capability имеет `name` и `required`. Неподдерживаемая обязательная capability возвращает `CAPABILITY_UNSUPPORTED`; необязательная capability может быть пропущена с предупреждением. Один source создаёт один Document/RecognitionResult. `ALL_OR_NOTHING` проверяет все sources до принятия job и не создаёт Documents/results, если любой source отклонён; последующая ошибка обработки отдельного source переводит batch job в `FAILED`, сохраняя только внутренние диагностические артефакты, подлежащие очистке. `ALLOW_PARTIAL` возвращает упорядоченные результаты по каждому source и создаёт Documents/results только для успешных sources. Порядок job/result всегда соответствует порядку sources в request.

`SourceRef` является либо загруженным непрозрачным source ID, либо доверенной внутренней ссылкой на blob. Публичные clients никогда не передают произвольные пути файловой системы сервера или исполняемые URLs.

## RecognitionResult

```text
RecognitionResult
  schema_version: "recognition-result/v1"
  document_id: ID
  raw_result_id: ID
  current_revision_id: ID
  provenance: Provenance
  detected_languages: list[LanguageScore]
  pages: list[Page]
  plain_text: string
  confidence?: float
  warnings: list[Warning]
  metadata: map[string, JSON value]
```

`raw_result_id` и `current_revision_id` намеренно разделены. Provenance содержит input hash, версии engine/model/pipeline, нормализованный configuration hash, timestamps и attempts.

## Port RecognitionEngine

```text
capabilities() -> EngineCapabilities
recognize(EngineRequest, CancellationToken, ResourceBudget) -> EngineResult
recognize_region(EngineRegionRequest, CancellationToken, ResourceBudget) -> EngineResult
health() -> EngineHealth
version() -> EngineVersion
```

Adapters не должны раскрывать vendor DTOs. Они нормализуют confidence, coordinates, errors и provenance и проходят общий contract suite.

## REST API v1

| Метод | Путь | Результат |
|---|---|---|
| `POST` | `/v1/recognitions` | `202 RecognitionJob`; поддерживается idempotency |
| `GET` | `/v1/recognitions/{job_id}` | status/progress/error job и ссылка на result |
| `POST` | `/v1/recognitions/{job_id}/cancel` | принятый запрос отмены |
| `GET` | `/v1/documents/{document_id}` | metadata текущего представления |
| `GET` | `/v1/documents/{document_id}/pages` | страницы с pagination |
| `POST` | `/v1/documents/{document_id}/corrections` | новые correction и revision |
| `GET` | `/v1/documents/{document_id}/revisions` | сводки revisions с pagination |
| `GET` | `/v1/documents/{document_id}/revisions/{revision_id}` | выбранное неизменяемое представление |
| `GET` | `/v1/documents/{document_id}/diff?from=&to=` | структурный и текстовый diff |
| `POST` | `/v1/documents/{document_id}/recognitions` | job повторного запуска для document/page/region/line |
| `POST` | `/v1/documents/{document_id}/revisions` | создание производной rollback/rebase revision с явными base/target |
| `GET` | `/v1/engines` | доступные engines без секретов |
| `GET` | `/v1/capabilities` | capabilities API/Core |

List endpoints используют непрозрачную cursor pagination: `items`, `next_cursor`. Заголовки authorization и rate limit зависят от deployment profile, но errors стандартизированы.

## CorrectionRequest

```text
CorrectionRequest
  schema_version: "correction/v1"
  base_revision_id: ID
  target: {type, id}
  operation: CorrectionOperation
  payload: CorrectionPayload  # определяется значением operation
  reason?: string
  metadata: map[string, JSON value]
```

Публичный endpoint corrections всегда получает actor, tenant и классификацию source (`USER`) из аутентифицированного execution context; он не принимает заявления `TRUSTED_IMPORT` или `AUTOMATED_POSTPROCESSOR`. Специализированные внутренние или import use cases могут назначать эти классификации только по авторизованным service credentials/routes. Если для import принимается заявленная client attribution, она считается недоверенными metadata и никогда не используется как identity для authorization/audit. Сервер проверяет `before` относительно base revision и принадлежность target авторизованному document. Устаревшая base возвращает `REVISION_CONFLICT` с ID текущей revision и никогда не выполняет скрытый rebase.

Хранение correction не означает согласие на обучение. Export dataset использует отдельный неизменяемый `ConsentGrant`, версионированный по purpose/scope/policy, полученный из аутентифицированной identity и повторно проверенный во время export; отсутствующий, истёкший или отозванный grant запрещает export.

### Payloads операций correction

`CorrectionOperation` является discriminated union; нет нетипизированного общего wire payload before/after:

| Операция | Обязательный payload |
|---|---|
| `REPLACE_TEXT` | `before_text`, `after_text` |
| `INSERT_TEXT` | anchor target/position, `inserted_text` |
| `DELETE_TEXT` | `before_text` |
| `MERGE_TOKENS` / `MERGE_LINES` | упорядоченные `source_ids`, ожидаемые значения и результирующее значение |
| `SPLIT_TOKEN` / `SPLIT_LINE` | ожидаемое значение, упорядоченные split values/boundaries |
| `CHANGE_REGION_TYPE` | ожидаемый и новый region enum |
| `CHANGE_READING_ORDER` | parent ID, ожидаемые и новые упорядоченные child IDs |
| `CHANGE_LANGUAGE` | ожидаемые и новые значения BCP-47 |
| `CHANGE_BBOX` | ожидаемая и новая нормализованная geometry |
| `MARK_CORRECT` / `MARK_UNCERTAIN` / `IGNORE` | ожидаемый content hash цели и необязательная причина |

Неизвестная operation или несоответствующий payload discriminator отклоняются. Сервер сохраняет канонические значения before/after, полученные из проверенной base revision, а не доверяет заявлениям клиента.

## Частичный повторный запуск и команды revisions

`RecognitionScope` является ровно одним из вариантов `{DOCUMENT, document_id}`, `{PAGE, page_id}`, `{REGION, region_id}`, `{LINE, line_id}` и включает ID base revision и необязательные overrides engine/options, разрешённые политикой. Сервер авторизует ancestry цели и возвращает async job; завершение добавляет новые raw evidence и revision.

`CreateRevisionRequest` поддерживает `ROLLBACK` с `base_revision_id`, то есть текущей optimistic base, и `target_revision_id`. Rollback никогда не перемещает pointer назад и не удаляет поздние revisions; он добавляет новую revision, представление которой равно авторизованной target, и записывает provenance.

## Ответы revisions и diff

```text
RevisionSummary
  schema_version: "revision/v1"
  id, document_id, parent_revision_id?, base_raw_result_id
  kind: MACHINE | CORRECTION | RERUN | ROLLBACK | POSTPROCESSING
  correction_ids[], created_at, actor, content_hash

RevisionView
  revision: RevisionSummary
  result: RecognitionResult

RevisionDiff
  schema_version: "revision-diff/v1"
  from_revision_id, to_revision_id
  operations: list[typed structural/text/layout change]
  summary: added/removed/changed counts
```

Операции diff содержат stable/ancestry IDs и типизированные значения before/after. Pagination применяется к спискам revisions и большим спискам операций diff.

## Jobs и idempotency

`RecognitionJob` предоставляет `status`, `attempt`, IDs source/document/result в порядке request, результат каждого source, `current_page`, `total_pages`, `progress_percent`, `current_stage`, timestamps и итоговый result/error.

Idempotency использует двухуровневый контракт. Уникальная identity `(tenant, authenticated principal, operation, idempotency_key)` соответствует ровно одному сохранённому canonical request hash и авторизованному result. Та же identity и тот же hash возвращают существующий job; та же identity и другой hash возвращают `IDEMPOTENCY_CONFLICT` и никогда не создают второй job. Lookup никогда не раскрывает наличие результата у другой identity. Срок retention определяется deployment configuration и публикуется.

Recognition cache отделён: его key включает требуемые политикой tenant/principal, canonical request, privacy mode, версии schema/pipeline и точные digests артефактов engine/model. Каждое получение из cache повторно авторизуется и инвалидируется при удалении или изменении policy/version.

## Формат ошибки

```text
ErrorResponse
  error:
    code: stable machine code
    message: safe human message
    category: VALIDATION | ENGINE | RESOURCE | STORAGE | CONFLICT | SECURITY | INTERNAL
    retryable: boolean
    details: safe structured fields
    correlation_id: opaque ID
```

Минимальный набор codes включает значения из SPEC и `CAPABILITY_UNSUPPORTED`, `REVISION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `CANCELLED`, `PRIVACY_MODE_VIOLATION`, `RESOURCE_LIMIT_EXCEEDED`. Stack traces, локальные пути и распознанное содержимое никогда не возвращаются.

## Граница локального сервиса

Локальный REST по умолчанию использует loopback или local IPC, сгенерированные bearer credentials высокой энтропии либо проверенные OS peer credentials, deny-all CORS и отсутствие cookie authentication. Bootstrap credentials использует приватный token file с проверенными permissions или OS credential store, но не аргументы командной строки или environment output, который может попасть в logs; проверка выполняется за постоянное время, а rotation/revocation инвалидирует предыдущие tokens. Если безопасная генерация или storage невозможны, запуск завершается закрытым отказом; wildcard/non-loopback bind запрещён, пока не выполнен security gate remote profile. Ограничения размера request body, глубины JSON, container/string cardinality и response применяются до дорогого parsing и до serialization.

## Будущий MCP

Product MCP может предоставлять `recognize_document`, `recognize_region`, `get_recognition`, `list_uncertain_regions`, `apply_correction`, `get_revision`. Каждый tool делегирует тем же application use cases и политикам authorization/privacy; собственной реализации OCR в MCP нет.
