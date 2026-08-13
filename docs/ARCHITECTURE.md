# Архитектура Text Recognition Core

**Статус:** КАРКАС; runtime ещё не реализован. Архитектура обеспечивает `specs/system.spec.md` и не утверждает наличие компонентов в коде.

## Цели и границы

TRC предоставляет стабильные контракты OCR/HTR, orchestration, унифицированную модель распознавания, corrections/revisions и ports расширения. Семантический поиск конкретного consumer, бухгалтерский и учебный домен, UI и обучение моделей находятся вне Core.

## Правило зависимостей

```text
interfaces (REST / SDK / CLI / MCP / workers)
                    ↓
application use cases + ports
                    ↓
domain model and invariants
                    ↑
infrastructure + engine/storage/job adapters
```

Domain не импортирует FastAPI, transport DTO Pydantic, clients базы данных или очереди и OCR SDK. Infrastructure реализует application ports. Application adapters потребителей являются соседними integration packages и не вносят consumer entities в domain.

## Ограниченные контексты

| Контекст | Ответственность | Не входит |
|---|---|---|
| Document Intake | descriptor источника, validation, hashing, сохранение original, безопасная normalization | OCR и consumer parsing |
| Recognition Orchestration | validation request, план pipeline, capabilities, выбор engine/fallback, partial rerun | детали SDK engine |
| Engine Integration | registry, `RecognitionEngine`, нормализация confidence/provenance | business rules приложения |
| Recognition Model | Document/Page/Region/Line/Token, layout, alternatives, raw snapshot | изменяемые пользовательские правки |
| Corrections & Revisions | append-only corrections, граф revisions, replay/diff/rollback/current view | перезапись raw |
| Jobs & Execution | lifecycle, progress, cancellation, idempotency, resource budgets | transport handlers |
| Application Integration | входные profiles/hints и выходные projectors для consumers | владение доменом Chronicle/Receipt/Tutor |
| Persistence & Privacy | логические stores, transactions, cache, ports retention/deletion, privacy policy | фиксированная технология базы данных в domain |
| Quality & Benchmarking | golden datasets, CER/WER/layout/adapter metrics, воспроизводимые reports | production training loop |

## Поток распознавания

```text
Недоверенный Source
  → validation размера, формата и ресурсов
  → одноразовый decoder/OCR worker с минимальными правами
  → неизменяемые original + input hash
  → normalization/preprocessing (производные artifacts)
  → анализ layout и классификация regions
  → выбор engine с учётом capabilities
  → adapter(s) RecognitionEngine
  → нормализованные confidence/coordinates/provenance
  → неизменяемый RawRecognitionSnapshot
  → Revision 1 / Current View
  → необязательная application projection
```

Этапы pipeline реализуют сменяемые ports: `Preprocessor`, `LayoutAnalyzer`, `RecognitionEngine`, `Postprocessor`, `ResultValidator`. Декодирование binary, parsing metadata и inference engine/model выполняются в одноразовых subprocess workers или эквивалентном изолированном sandbox без сети, с приватным per-job temp root, минимальным read-only доступом к source, непривилегированной identity, OS limits для CPU/RSS/files/processes, жёстким timeout/kill и очисткой после crash/cancel. Каждый этап принимает и создаёт типизированные значения и проверяет cancellation/resource budget на безопасных границах.

## Corrections и частичный повторный запуск

```text
stable target + base_revision_id + operation
  → validation target и optimistic version
  → добавление Correction
  → добавление Revision(parent_revision_id)
  → deterministic replay/current view
```

Split/merge создаёт новые стабильные IDs и явные ancestry links; старые IDs остаются доступными в предыдущих revisions. Partial rerun создаёт новые raw evidence для выбранного scope, а затем новую revision; предыдущий raw snapshot никогда не изменяется.

## Асинхронные jobs

Допустимые переходы:

```text
PENDING → RUNNING → COMPLETED
                  ↘ REVIEW_REQUIRED
                  ↘ FAILED
PENDING/RUNNING → CANCELLED
```

Terminal states неизменяемы. Retry создаёт новую attempt внутри того же логического job и записывает её причину. Idempotency identity `(tenant, principal, operation, key)` соответствует одному canonical request hash/result; другой hash вызывает conflict и не может создать второй job. Recognition cache независим и использует key из требуемой политикой identity, canonical request, privacy mode, версий schema/pipeline и точных digests артефактов engine/model. Каждое получение повторно авторизуется и никогда не раскрывает наличие результата в другом scope.

## Границы хранения

Логические stores разделены, даже если первый adapter использует одну базу SQLite и filesystem blobs:

- исходные sources и производные artifacts;
- неизменяемые raw recognition snapshots;
- corrections и revisions;
- jobs, idempotency и progress;
- cache, индексированный по hashes входа, config и versions;
- производные application projections вне владения Core.

Записи blobs являются content-addressed и атомарными; database transactions публикуют metadata только после надёжного сохранения blob. Политика удаления может удалить хранимые source data после авторизации; «original не уничтожается» означает, что preprocessing его не перезаписывает, а не бесконечный retention.

## Интерфейсы и точки расширения

- Public: сначала версионированный Python application API; REST adapter после контрактов; CLI/MCP позднее.
- Engine: `RecognitionEngine` и descriptors capabilities.
- Pipeline: ports preprocessor/layout/postprocessor.
- Persistence: ports repositories/blob/cache/unit-of-work.
- Execution: job runner, cancellation token, resource budget, clock/id generator.
- Integration: interfaces input profile и output projector consumer.
- Export: exporter benchmark/dataset с учётом privacy.

## Профили развёртывания

1. **Embedded/offline first:** Python library, local engine, SQLite/filesystem и постоянный локальный coordinator; недоверенные decoding/inference всё равно выполняются в изолированных одноразовых workers.
2. **Local service:** REST adapter выполняет bind только на loopback/local IPC, требует сгенерированный local bearer token или проверенные OS peer credentials, по умолчанию запрещает browser CORS и не хранит cookie-based session; в `LOCAL_ONLY` по-прежнему отсутствует внешний egress.
3. **Remote service:** authentication, authorization, tenant isolation, encryption, rate limits и внешние queue/storage только после отдельных решений.

Docker упаковывает выбранный профиль, но не определяет архитектуру. MCP является поздним интерфейсом поверх application use cases.

## Технологическая основа

Зафиксировано в `DECISIONS.md`: пакет, совместимый с Python 3.13, типизированные внутренние модели, Pydantic v2 на границах validation/schema, FastAPI только как REST adapter, pytest и начальный adapter SQLite/filesystem. Библиотеки OCR/HTR и PDF/image остаются решениями benchmark/ADR.

## Модель отказов

- Fatal errors останавливают job и используют стабильные error codes.
- Warnings сохраняют пригодный для использования результат.
- Низкий confidence приводит к `REVIEW_REQUIRED`, а не к автоматическому failure.
- Ошибка adapter может использовать разрешённый fallback; каждая attempt и набор parameters сохраняют traceability.
- Для детерминированного invalid input автоматический retry запрещён; transient retries ограничены и учитывают cancellation.

## Архитектурные проверки

- границы dependencies/imports;
- snapshots совместимости schema;
- contract suite engines;
- replay corrections и неизменяемость raw;
- no-egress test для `LOCAL_ONLY`;
- обнаружение приватных fixtures и утечки telemetry;
- проверки isolation/crash/cleanup workers и целостности dependency/model;
- golden reports регрессии качества и производительности.
