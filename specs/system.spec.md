# Text Recognition Core — Product & System Specification

**Status:** Draft / Source of Truth for Context Automation

**Version:** 0.1

**Purpose:** спецификация для последующего создания КАРКАСА проекта средствами Codex.

**Canonical path:** `specs/system.spec.md`. Исходное имя `SPEC.md` было нормализовано при создании КАРКАСА; второй активной копии нет.

---

# 1. Назначение проекта

**Text Recognition Core (TRC)** — независимое переиспользуемое ядро распознавания текста, предназначенное для использования несколькими приложениями.

Основная задача TRC:

> предоставить единый API для OCR/HTR, единый формат результата распознавания, единый механизм пользовательских исправлений и адаптеры для специализированных приложений.

Первоначальные потребители:

1. **Personal Chronicle / Life Intelligence**
   - дневники;
   - рукописные записи;
   - фотографии страниц;
   - архивные документы;
   - исправление человеком;
   - последующий семантический поиск по распознанному тексту.

2. **Receipt Scanner**
   - украинские кассовые чеки;
   - печатный текст;
   - позиции товаров;
   - цены;
   - количество;
   - итоговые суммы;
   - дата/время;
   - магазин;
   - структурированное представление данных.

3. **Tutor**
   - фотографии ученических работ;
   - печатный и рукописный текст;
   - задания;
   - ответы;
   - комментарии;
   - в дальнейшем — математические выражения, таблицы, схемы и другие учебные элементы.

TRC не должен содержать бизнес-логику этих приложений.

---

# 2. Основной архитектурный принцип

Text Recognition Core должен быть отдельным сервисом/модулем:

```text
Personal Chronicle ─┐
Receipt Scanner   ──┼── Adapters ── Text Recognition Core
Tutor             ──┘
```

Внутри:

```text
                   ┌─ OCR Engines
                   │
                   ├─ HTR Engines
Input → Pipeline → ├─ Preprocessing
                   ├─ Layout Analysis
                   ├─ Postprocessing
                   └─ Confidence / Alternatives
                            │
                            ▼
                   Unified Recognition Model
                            │
                ┌───────────┴────────────┐
                ▼                        ▼
        Correction Engine           Application Adapters
```

Основной принцип:

> приложения не должны напрямую зависеть от конкретного OCR/HTR-движка.

Запрещён сценарий:

```text
Receipt Scanner → Tesseract API
Personal Chronicle → PaddleOCR API
Tutor → TrOCR API
```

Предпочтительный сценарий:

```text
Application
    ↓
TRC API
    ↓
Recognition Engine Adapter
    ↓
Tesseract / PaddleOCR / TrOCR / custom model / cloud engine / etc.
```

Конкретные recognition engines являются заменяемыми backend-адаптерами.

---

# 3. Терминология

## OCR

Optical Character Recognition — распознавание преимущественно печатного текста.

## HTR

Handwritten Text Recognition — распознавание рукописного текста.

## Recognition Engine

Конкретная технология или модель распознавания.

Примеры:

- Tesseract;
- PaddleOCR;
- EasyOCR;
- TrOCR;
- специализированная локальная модель;
- будущая собственная модель.

TRC не должен быть архитектурно привязан ни к одному из них.

## Document

Логический документ, состоящий из одной или нескольких страниц.

## Page

Отдельная страница или изображение.

## Region

Прямоугольная либо полигональная область страницы.

## Block

Семантический или визуальный блок:

- paragraph;
- heading;
- table;
- receipt;
- handwriting;
- printed_text;
- image;
- unknown;
- и т. п.

## Recognition Result

Полный машинный результат распознавания.

## Correction

Изменение результата, сделанное пользователем или другим доверенным источником.

## Revision

Версия результата после применения набора Correction.

---

# 4. Цели

TRC должен обеспечивать:

1. единый OCR/HTR API;
2. единый внутренний формат результатов;
3. сменяемость recognition engines;
4. сохранение координат текста;
5. confidence score;
6. альтернативные варианты распознавания;
7. поддержку нескольких языков;
8. поддержку печатного и рукописного текста;
9. пользовательское исправление распознавания;
10. сохранение истории исправлений;
11. возможность повторного использования исправлений для улучшения качества;
12. асинхронную обработку больших документов;
13. пакетную обработку;
14. возможность локальной/offline работы;
15. расширение через adapters/plugins;
16. интеграцию с несколькими приложениями;
17. возможность построения CLI/API/MCP поверх одного Application/Core.

---

# 5. Не-цели первого этапа

В первоначальный Core НЕ требуется включать:

- полноценную LLM;
- семантический поиск;
- векторную БД;
- бизнес-логику дневников;
- бухгалтерскую аналитику чеков;
- систему обучения репетитора;
- генерацию математических решений;
- полноценный редактор документов;
- собственную OCR neural network с нуля;
- автоматическое обучение модели без контроля пользователя.

Эти возможности могут использовать TRC, но не должны становиться частью его доменного ядра.

---

# 6. Архитектурные слои

Предпочтительная архитектура:

```text
interfaces/
    REST
    CLI
    MCP
    Python SDK

application/
    use cases
    orchestration

domain/
    RecognitionDocument
    RecognitionPage
    TextRegion
    TextToken
    Correction
    Revision
    Confidence

pipelines/
    preprocessing
    recognition
    postprocessing
    validation

engines/
    OCR adapters
    HTR adapters
    layout adapters

corrections/
    correction engine
    revision engine
    feedback processing

adapters/
    personal_chronicle
    receipt_scanner
    tutor

infrastructure/
    storage
    queues
    files
    telemetry
```

Точные технологии определяются КАРКАСОМ позже.

---

# 7. Unified Recognition API

TRC должен иметь единую операцию распознавания независимо от используемого движка.

Концептуально:

```text
recognize(input, options) -> RecognitionResult
```

`input` может представлять:

- image;
- PDF;
- page;
- document;
- batch.

---

# 8. RecognitionRequest

Минимальная модель запроса:

```text
RecognitionRequest
    source
    mode
    languages[]
    capabilities[]
    preprocessing_options
    engine_preferences
    output_options
    context
```

## mode

Минимально:

```text
AUTO
OCR
HTR
MIXED
```

### AUTO

TRC определяет подходящий pipeline самостоятельно.

### OCR

Приоритет печатного текста.

### HTR

Приоритет рукописного текста.

### MIXED

Документ может содержать оба типа.

---

# 9. Capabilities

Запрос должен позволять сообщить Core, какие возможности нужны.

Например:

```text
TEXT
LAYOUT
TABLES
HANDWRITING
RECEIPT
MATH
CHECKBOXES
BARCODES
```

Не все capabilities обязаны быть реализованы в v1.

Архитектура должна позволять их добавление без изменения основного API.

---

# 10. RecognitionResult

Результат не должен быть просто строкой.

Минимальная структура:

```text
RecognitionResult
    document_id
    revision_id
    engine
    engine_version
    pipeline_version

    detected_languages[]

    pages[]
    plain_text

    confidence

    warnings[]
    metadata
```

---

# 11. Page Model

```text
Page
    id
    page_number
    width
    height
    rotation
    regions[]
    plain_text
    confidence
```

---

# 12. Region Model

```text
Region
    id
    type
    bbox
    polygon?
    reading_order
    text
    confidence
    lines[]
    metadata
```

Примеры `type`:

```text
paragraph
heading
handwriting
printed_text
table
receipt_item
image
unknown
```

---

# 13. Line и Token

TRC должен позволять дойти минимум до уровня отдельного слова/token.

```text
Line
    id
    bbox
    text
    confidence
    tokens[]
```

```text
Token
    id
    text
    bbox
    confidence
    alternatives[]
```

Это необходимо для:

- подсветки ошибок;
- UI исправления текста;
- сопоставления текста с исходным изображением;
- частичного повторного распознавания.

---

# 14. Bounding Boxes

Для распознанного элемента по возможности необходимо сохранять его координаты.

Минимальный вариант:

```text
x
y
width
height
```

Желательно предусмотреть поддержку polygon.

Координаты должны иметь чётко определённую систему:

```text
top-left origin
```

или нормализованные координаты.

Выбранная система должна быть зафиксирована в API specification.

---

# 15. Confidence

Confidence должен храниться не только на уровне документа.

Желательные уровни:

```text
document
page
region
line
token
```

Стандартный диапазон Core:

```text
0.0 .. 1.0
```

Если внешний engine использует другую шкалу, adapter обязан нормализовать её.

---

# 16. Alternatives

Recognition engine может возвращать несколько вариантов.

Например:

```text
recognized: "котёнок"

alternatives:
    "котенок" 0.82
    "котёнок" 0.89
    "котенок." 0.61
```

TRC должен уметь сохранить alternatives.

Это особенно важно для HTR.

---

# 17. Human-in-the-loop correction model

Исправления пользователя являются ключевой частью Text Recognition Core.

Модель должна соблюдать принцип:

> машинный результат не уничтожается пользовательским редактированием.

Хранятся:

```text
RAW RECOGNITION
        ↓
CORRECTIONS
        ↓
REVISION
        ↓
CURRENT VIEW
```

---

# 18. Immutable Raw Result

Первоначальный результат recognition engine должен сохраняться как immutable snapshot.

Пользовательское исправление не должно молча перезаписывать исходное значение.

Например:

```text
RAW:
"возле сарая увидел катёнка"

CORRECTION:
"катёнка" → "котёнка"

CURRENT:
"возле сарая увидел котёнка"
```

Это позволит:

- анализировать ошибки;
- переобрабатывать документы;
- сравнивать модели;
- создавать datasets;
- откатывать ошибочные исправления.

---

# 19. Correction Entity

Пример:

```text
Correction
    id
    document_id
    revision_id

    target_type
    target_id

    operation

    before
    after

    author
    timestamp

    source

    confidence_before?
    reason?
    metadata
```

---

# 20. Correction Operations

Минимально предусмотреть:

```text
REPLACE_TEXT
INSERT_TEXT
DELETE_TEXT

MERGE_TOKENS
SPLIT_TOKEN

MERGE_LINES
SPLIT_LINE

CHANGE_REGION_TYPE

CHANGE_READING_ORDER

CHANGE_LANGUAGE

CHANGE_BBOX

MARK_CORRECT
MARK_UNCERTAIN
IGNORE
```

Архитектура должна позволять добавлять новые операции.

---

# 21. Пользовательское подтверждение

Важно различать:

```text
не проверено пользователем
```

и

```text
проверено пользователем и признано правильным
```

Поэтому должна существовать операция:

```text
MARK_CORRECT
```

Подтверждённое правильное распознавание также является полезным feedback.

---

# 22. Revision Model

Исправления должны формировать версии.

Пример:

```text
Revision 1
machine recognition

Revision 2
user corrected line 5

Revision 3
user merged two regions

Revision 4
automatic postprocessing applied
```

Необходимо иметь возможность:

- получить текущую revision;
- получить конкретную revision;
- увидеть diff;
- откатиться;
- создать новую revision на основе предыдущей.

---

# 23. Partial re-recognition

TRC должен предусматривать повторное распознавание:

```text
document
page
region
line
```

Например пользователь выделяет плохо распознанный кусок рукописи и выбирает:

```text
Recognize again
```

TRC не должен для этого обязательно обрабатывать весь документ.

---

# 24. Recognition Context / Hints

Приложение должно иметь возможность передавать подсказки.

Пример:

```text
context:
    domain: personal_chronicle
    expected_languages:
        - uk
        - ru
    probable_date: 2017-04-15
```

Receipt Scanner:

```text
domain: receipt
country: UA
currency: UAH
```

Tutor:

```text
domain: education
subject: mathematics
grade: 8
```

Recognition engine не обязан использовать все hints.

Но API должен позволять их передавать.

---

# 25. Engine abstraction

Каждый recognition engine реализует унифицированный adapter contract.

Концептуально:

```text
RecognitionEngine
    capabilities()
    recognize()
    recognize_region()
    health()
    version()
```

TRC должен иметь Engine Registry.

Например:

```text
paddle_ocr
tesseract
trocr
custom_htr
```

---

# 26. Engine Selection

Core должен иметь возможность:

1. использовать явно указанный engine;
2. выбрать engine автоматически;
3. использовать fallback;
4. применять разные engines для разных regions.

Пример:

```text
printed regions → OCR Engine A
handwritten regions → HTR Engine B
```

---

# 27. Pipeline

Основной pipeline:

```text
INPUT
 ↓
Validation
 ↓
Normalization
 ↓
Image preprocessing
 ↓
Orientation detection
 ↓
Deskew
 ↓
Layout analysis
 ↓
Region classification
 ↓
OCR / HTR routing
 ↓
Recognition
 ↓
Postprocessing
 ↓
Confidence normalization
 ↓
Unified result
 ↓
Application adapter
```

Каждый этап должен быть заменяемым.

---

# 28. Preprocessing

Архитектура должна предусматривать:

- rotation;
- deskew;
- crop;
- contrast enhancement;
- grayscale;
- denoise;
- perspective correction;
- background normalization;
- page detection.

Preprocessing, recognition и corrections не могут перезаписывать или молча уничтожать оригинальный файл. Авторизованное удаление по retention/privacy policy допускается и должно удалить связанные cache/exports/backups согласно проверяемому deletion contract.

---

# 29. Language Support

Минимальный приоритет:

1. Ukrainian;
2. Russian;
3. English.

Архитектура должна позволять добавление языков.

Для документа могут быть указаны несколько языков одновременно.

---

# 30. Privacy

Text Recognition Core будет использоваться для потенциально очень конфиденциальных материалов.

Особенно:

- личные дневники;
- документы;
- ученические работы;
- финансовые данные из чеков.

Поэтому архитектура должна поддерживать:

```text
LOCAL_ONLY
HYBRID
REMOTE_ALLOWED
```

Для Personal Chronicle должен существовать режим:

```text
LOCAL_ONLY
```

при котором данные не покидают устройство/локальную инфраструктуру.

---

# 31. Training Feedback

Исправления пользователя потенциально могут использоваться для улучшения распознавания.

Но:

> исправление пользователя НЕ означает автоматического согласия на использование данных для обучения.

Необходимо разделить:

```text
correction storage
```

и

```text
training dataset participation
```

Пример:

```text
allow_training_use = false
```

по умолчанию.

---

# 32. Dataset Export

В будущем должна быть возможность экспортировать пары:

```text
image region
+
raw recognition
+
corrected text
```

для:

- анализа ошибок;
- benchmark;
- fine-tuning;
- обучения специализированных моделей.

Экспорт должен учитывать privacy policy.

---

# 33. Adapter Architecture

Application Adapter преобразует универсальный RecognitionResult в модель конкретного приложения.

```text
RecognitionResult
       ↓
Application Adapter
       ↓
Application-specific Result
```

Adapter не должен менять Core domain model.

---

# 34. Personal Chronicle Adapter

## Назначение

Преобразование распознанных записей в структуру, пригодную для Personal Chronicle.

Особые требования:

- высокий приоритет HTR;
- сохранение расположения текста;
- работа со страницами дневников;
- смешанный рукописный/печатный текст;
- возможность интерактивного исправления;
- фиксация дат;
- разделение отдельных записей;
- сохранение неопределённых фрагментов.

Пример результата adapter:

```text
ChronicleRecognition
    document_id
    probable_date
    entries[]
    uncertain_fragments[]
```

Adapter НЕ должен:

- выполнять RAG;
- строить embeddings;
- отвечать на вопросы о дневнике;
- создавать LLM summary.

Это ответственность Personal Chronicle.

---

# 35. Receipt Scanner Adapter

Особые требования:

- OCR печатного текста;
- layout preservation;
- строки товаров;
- количество;
- цена;
- стоимость;
- скидки;
- магазин;
- адрес;
- дата;
- время;
- итоговая сумма;
- валюта;
- налоговая информация при наличии.

Пример:

```text
ReceiptRecognition
    merchant
    timestamp

    items[]
        name
        quantity
        unit_price
        total_price

    subtotal
    discount
    total
    currency
```

Каждое структурированное поле желательно связывать с исходным Region/Token.

Например:

```text
total = 482.30
source_token_id = token_391
```

Это позволит UI показать пользователю, откуда взялось значение.

---

# 36. Tutor Adapter

Особые требования:

- печатный текст;
- рукописный текст;
- задания;
- ответы ученика;
- исправления;
- таблицы;
- потенциальные математические выражения.

Структура должна позволять в дальнейшем добавить:

```text
MATH_EXPRESSION
DIAGRAM
TABLE
ANSWER_REGION
TEACHER_COMMENT
```

Math OCR не является обязательной частью TRC v1, но архитектура не должна препятствовать его появлению.

---

# 37. API Boundary

Рекомендуемая внешняя модель:

```text
POST /recognitions
GET  /recognitions/{id}

GET  /documents/{id}
GET  /documents/{id}/pages

POST /documents/{id}/corrections
GET  /documents/{id}/revisions

POST /regions/{id}/recognize

GET /engines
GET /capabilities
```

Это концептуальный контракт.

Фактическая OpenAPI-схема должна быть создана в КАРКАСЕ/реализации.

---

# 38. Async Jobs

Обработка документов может занимать значительное время.

Поэтому API должен поддерживать job model:

```text
PENDING
RUNNING
REVIEW_REQUIRED
COMPLETED
FAILED
CANCELLED
```

Пример:

```text
POST /recognitions

→

202 Accepted

job_id
```

---

# 39. Progress

Для больших документов желательно предоставлять:

```text
current_page
total_pages
progress_percent
current_stage
```

Например:

```text
page 43 / 120
stage: handwriting_recognition
```

---

# 40. Error Model

Ошибки должны иметь machine-readable code.

Пример:

```text
UNSUPPORTED_FORMAT
FILE_TOO_LARGE
CORRUPTED_FILE

ENGINE_UNAVAILABLE
ENGINE_FAILED

LANGUAGE_UNSUPPORTED

LOW_CONFIDENCE

PROCESSING_TIMEOUT

INVALID_CORRECTION

STORAGE_ERROR
```

Необходимо разделять:

- fatal errors;
- warnings;
- review-required conditions.

---

# 41. Low-confidence workflow

Низкая уверенность не всегда является ошибкой.

Вместо:

```text
FAILED
```

может использоваться:

```text
REVIEW_REQUIRED
```

UI приложения сможет показать:

> 17 фрагментов требуют проверки.

---

# 42. Traceability

Необходимо иметь возможность определить:

> каким движком, какой версией, каким pipeline и с какими параметрами был получен конкретный результат.

Хранить:

```text
engine_name
engine_version
model_version
pipeline_version
configuration
timestamp
```

---

# 43. Reproducibility

Если возможно, recognition job должен быть воспроизводим.

Для этого необходимо сохранять:

- input hash;
- engine/model version;
- pipeline version;
- параметры;
- preprocessing configuration.

---

# 44. Observability

TRC должен предоставлять техническую телеметрию.

Минимально:

- processing duration;
- pages processed;
- engine errors;
- fallback count;
- confidence distribution;
- queue duration;
- resource consumption;
- failed jobs.

При этом telemetry НЕ должна автоматически содержать распознанный пользовательский текст.

---

# 45. Product-quality metrics

Необходимо предусмотреть benchmark framework.

Метрики:

### OCR/HTR

```text
CER — Character Error Rate
WER — Word Error Rate
```

Для Receipt Scanner дополнительно:

```text
field accuracy
item extraction accuracy
total amount accuracy
```

Для layout:

```text
region detection metrics
reading order accuracy
```

---

# 46. Golden Dataset

Проект должен предусматривать набор контрольных примеров.

Структура условно:

```text
tests/
    fixtures/
        printed/
        handwriting/
        mixed/
        receipts/
        tutor/
```

Не помещать реальные приватные дневники пользователей в публичный repository.

Использовать:

- synthetic;
- anonymized;
- explicitly approved test data.

---

# 47. Security

При проектировании КАРКАСА Codex должен выполнить отдельный threat analysis.

Минимально учитывать:

- malicious files;
- decompression bombs;
- oversized images;
- malformed PDF;
- path traversal;
- unsafe temporary files;
- arbitrary file execution;
- dependency vulnerabilities;
- API abuse;
- authentication/authorization при сетевой работе;
- rate limiting;
- resource exhaustion;
- sensitive-data leakage;
- unsafe logging.

OCR input должен рассматриваться как недоверенный пользовательский ввод.

---

# 48. Resource Limits

Должны существовать configurable limits:

```text
max_file_size
max_pages
max_image_dimensions
max_processing_time
max_concurrent_jobs
max_memory_per_job
```

---

# 49. Cancellation

Длительный recognition job должен быть отменяемым.

```text
cancel(job_id)
```

Pipeline должен по возможности корректно освобождать ресурсы.

---

# 50. Caching

Разрешается кеширование распознавания по комбинации:

```text
input hash
+
pipeline version
+
engine/model version
+
recognition options
```

Изменение параметров должно инвалидировать соответствующий cache key.

---

# 51. Storage

Core должен логически разделять:

```text
Original Source
Raw Recognition
Corrections
Revisions
Derived Application Data
```

Application-specific данные желательно хранить за границей Core или через отдельный adapter storage.

---

# 52. Portability

Core должен проектироваться так, чтобы его можно было использовать:

```text
Embedded Python library
Local service
Docker service
Remote API
CLI
MCP server
```

Все интерфейсы должны обращаться к одному Application/Core, а не реализовывать бизнес-логику повторно.

Ориентир:

```text
REST ─┐
CLI  ─┤
SDK  ─┼── Application/Core
MCP  ─┤
Jobs ─┘
```

---

# 53. MCP

MCP является интерфейсом поверх существующего Application/Core.

Он не должен содержать собственную recognition implementation.

Будущий MCP может предоставлять AI-агентам инструменты вроде:

```text
recognize_document
recognize_region
get_recognition
list_uncertain_regions
apply_correction
get_revision
```

---

# 54. CLI

В будущем желательно:

```bash
trc recognize file.jpg
trc recognize diary.pdf --mode htr
trc engines
trc benchmark
```

CLI также является adapter/interface поверх Application/Core.

---

# 55. Idempotency

Повторный запрос с одним и тем же idempotency key не должен случайно создавать множество одинаковых jobs.

Особенно важно для REST/API integrations.

---

# 56. Stable identifiers

Document/Page/Region/Line/Token должны иметь устойчивые IDs.

Исправления должны ссылаться на IDs, а не только на строковые позиции текста.

Это необходимо, поскольку изменение текста может сдвигать offsets.

---

# 57. Compatibility

Версии API и domain schema должны иметь явную версионность.

Например:

```text
API v1
Recognition Schema v1
Correction Schema v1
```

Нельзя незаметно менять смысл существующих полей.

---

# 58. Extension points

Новые компоненты должны подключаться через чёткие интерфейсы.

Минимальные extension points:

```text
RecognitionEngine
Preprocessor
LayoutAnalyzer
Postprocessor
ApplicationAdapter
Exporter
StorageBackend
```

---

# 59. Offline-first requirement

TRC должен иметь возможность функционировать полностью offline при наличии локальных models/engines.

Это критично для Personal Chronicle.

Удалённые engines могут быть дополнительными adapters, но Core не должен зависеть от Internet connectivity.

---

# 60. Основные сценарии

## UC-01 — Printed OCR

Пользователь отправляет фотографию печатного документа.

TRC:

1. принимает изображение;
2. нормализует;
3. находит ориентацию;
4. обнаруживает regions;
5. выполняет OCR;
6. возвращает текст + layout + confidence.

---

## UC-02 — Handwritten diary

Пользователь отправляет страницу дневника.

TRC:

1. определяет handwriting;
2. использует HTR engine;
3. возвращает строки и tokens;
4. отмечает низкоуверенные fragments;
5. пользователь исправляет ошибки;
6. создаётся новая Revision.

---

## UC-03 — Mixed page

Страница содержит печатный заголовок и рукописные записи.

TRC маршрутизирует разные regions в разные recognition engines.

---

## UC-04 — Receipt

Receipt Scanner отправляет фотографию чека.

TRC выполняет OCR.

Receipt Adapter преобразует RecognitionResult в:

```text
merchant
items
prices
total
date
```

---

## UC-05 — Tutor worksheet

Tutor отправляет фотографию работы ученика.

TRC разделяет:

```text
printed assignment
handwritten answer
```

и распознаёт их соответствующими engines.

---

## UC-06 — User correction

Пользователь видит:

```text
"карова"
```

и исправляет:

```text
"корова"
```

TRC:

1. сохраняет Correction;
2. сохраняет исходное значение;
3. создаёт новую Revision;
4. обновляет Current View.

---

## UC-07 — Partial rerun

Пользователь выделяет одну строку и запускает повторное HTR.

Core не перераспознаёт весь документ.

---

# 61. Quality Requirements

Архитектура должна стремиться к:

- deterministic core behavior там, где это возможно;
- typed contracts;
- isolated engine adapters;
- repeatable tests;
- reproducible recognition jobs;
- graceful degradation;
- no silent data loss;
- explicit errors;
- explicit versioning.

---

# 62. Testing strategy

КАРКАС должен предусмотреть минимум следующие уровни.

## Unit tests

Для:

- domain models;
- corrections;
- revisions;
- engine selection;
- confidence normalization;
- adapter mapping.

## Contract tests

Каждый RecognitionEngine adapter должен проходить единый contract test suite.

## Integration tests

```text
input
→ pipeline
→ engine
→ unified result
```

## Adapter tests

Отдельно:

```text
Personal Chronicle
Receipt Scanner
Tutor
```

## Regression tests

Golden documents должны защищать от ухудшения recognition quality.

## Security tests

Проверка malicious/invalid/oversized inputs.

## Performance tests

Измерение:

```text
pages/sec
latency
memory
CPU/GPU utilization
```

---

# 63. Definition of Done для Core MVP

MVP Text Recognition Core считается архитектурно состоятельным, если:

- [ ] существует единая RecognitionRequest schema;
- [ ] существует единая RecognitionResult schema;
- [ ] определены Document/Page/Region/Line/Token;
- [ ] поддерживается минимум один OCR engine;
- [ ] предусмотрен HTR engine contract;
- [ ] engine скрыт за adapter;
- [ ] поддерживаются confidence values;
- [ ] сохраняются bounding boxes;
- [ ] реализована correction model;
- [ ] raw recognition не уничтожается;
- [ ] существуют revisions;
- [ ] возможно исправить отдельный token/line;
- [ ] возможно повторно распознать region;
- [ ] создан Personal Chronicle Adapter contract;
- [ ] создан Receipt Scanner Adapter contract;
- [ ] создан Tutor Adapter contract;
- [ ] API поддерживает async job model;
- [ ] ошибки имеют machine-readable codes;
- [ ] предусмотрен offline-only режим;
- [ ] logging не раскрывает пользовательский текст по умолчанию;
- [ ] имеются contract tests;
- [ ] имеются golden test fixtures;
- [ ] существует benchmark mechanism;
- [ ] проект не зависит архитектурно от одного OCR engine.

---

# 64. Будущие расширения

Спецификация должна позволять в будущем добавить без фундаментальной переделки:

- собственную OCR model;
- собственную HTR model;
- fine-tuning;
- active learning;
- handwriting personalization;
- математический OCR;
- chemical formulas;
- tables;
- diagrams;
- signatures;
- checkboxes;
- document classification;
- handwriting writer profiles;
- multilingual recognition;
- GPU acceleration;
- distributed recognition;
- WebGPU/WASM inference;
- mobile inference;
- edge inference;
- cloud worker pools;
- model routing;
- ensemble recognition;
- LLM-based postprocessing.

---

# 65. Персонализация HTR

Архитектурно предусмотреть будущий сценарий:

```text
generic HTR
    ↓
user corrections
    ↓
user-specific adaptation
    ↓
better recognition of that handwriting
```

Но персонализация НЕ является обязательным функционалом первого MVP.

Она должна быть отдельным будущим subsystem, а не логикой Correction Engine.

---

# 66. Ensemble Recognition

В будущем TRC может запустить несколько engines:

```text
Engine A ─┐
Engine B ─┼→ Result Resolver
Engine C ─┘
```

и сравнить варианты.

Unified API не должен препятствовать такой реализации.

---

# 67. Separation from applications

Особо зафиксировать архитектурную границу.

## Text Recognition Core знает:

```text
document
page
image
region
text
layout
confidence
correction
revision
recognition engine
```

## Personal Chronicle знает:

```text
life event
journal entry
timeline
memory
semantic search
```

## Receipt Scanner знает:

```text
product
merchant
purchase
price
expense
```

## Tutor знает:

```text
student
lesson
exercise
answer
grade
```

TRC не должен превращаться в общий монолит этих проектов.

---

# 68. Repository role

Text Recognition Core рекомендуется развивать как самостоятельный repository/library/service.

Остальные проекты должны зависеть от его публичных contracts.

Не следует копировать исходный OCR pipeline отдельно в:

```text
Personal Chronicle
Receipt Scanner
Tutor
```

---

# 69. Требования к создаваемому КАРКАСУ

Эта SPEC является источником предметных требований.

После её принятия Codex должен создать **КАРКАС Text Recognition Core**, но не дублировать глобальную AI Dev Team.

Проект рассматривается как:

```text
AI Dev Team
    +
Text Recognition Core overlay
```

а не как автономная вторая система управления AI-агентами.

---

# 70. Что КАРКАС должен определить

На основании этой SPEC Codex должен спроектировать:

## Architecture

Минимально:

```text
docs/ARCHITECTURE.md
```

С:

- bounded contexts;
- module boundaries;
- interfaces;
- recognition pipeline;
- correction architecture;
- adapter architecture;
- storage boundaries;
- async jobs;
- extension points.

---

## API

Создать:

```text
docs/API.md
```

и определить:

- RecognitionRequest;
- RecognitionResult;
- corrections;
- revisions;
- errors;
- async job API;
- versioning.

---

## Data Model

Создать:

```text
docs/DATA_MODEL.md
```

Для:

```text
Document
Page
Region
Line
Token
Correction
Revision
RecognitionJob
Engine
```

---

## Integrations

Создать:

```text
docs/INTEGRATIONS.md
```

Для:

```text
Personal Chronicle
Receipt Scanner
Tutor
```

с контрактами каждого adapter.

---

## Security

Создать:

```text
docs/SECURITY.md
```

С:

- threat model;
- privacy model;
- local-only processing;
- hostile input;
- resource limits;
- storage protection;
- logs;
- dependency security.

---

## Testing

Создать:

```text
docs/TEST_STRATEGY.md
```

С:

- unit;
- integration;
- contract;
- golden;
- regression;
- benchmark;
- security;
- performance tests.

---

## Decisions

Использовать:

```text
docs/DECISIONS.md
```

для существенных архитектурных решений.

---

## Design

Создать:

```text
docs/DESIGN.md
```

На первом этапе допускается skeleton.

UI не является основной частью Core, но документ должен предусматривать будущий Review/Correction UI.

---

# 71. PROMPTS

КАРКАС должен создать поэтапный:

```text
PROMPTS.md
```

или структуру:

```text
prompts/
    README.md
    stage-01-...
    stage-02-...
```

если количество этапов достаточно велико.

Каждый этап должен иметь:

```text
Goal
Context
Dependencies
Tasks
Files allowed to change
Tests
Definition of Done
Acceptance Criteria
Artifacts produced
Rollback / failure conditions
```

Этапы должны быть достаточно небольшими для отдельного Codex session/review/merge.

---

# 72. Progress tracking

Не создавать одновременно несколько дублирующих status-документов.

Использовать `docs/AI_STATUS.md` как единственный текущий источник состояния проекта. Не создавать рядом `PROGRESS.md` или другой дублирующий snapshot.

Туда заносить:

- текущий этап;
- завершённые этапы;
- pending;
- blockers;
- существенные изменения.

---

# 73. DEV_LOG

Использовать `docs/DEV_LOG.md` для подробной истории конкретных выполненных действий, когда такая хронология полезна проекту.

Codex должен писать туда, что именно было сделано технически.

---

# 74. LEARNING

Использовать `docs/LEARNING_LOG.md` для подробных объяснений:

- почему выбрано решение;
- как работает технология;
- какие альтернативы были рассмотрены;
- чему можно научиться из реализации.

LEARNING_LOG должен оставаться достаточно подробным, чтобы пользователю не приходилось самостоятельно восстанавливать смысл изменений по Git diff.

---

# 75. AGENTS / Rules

Project-specific `AGENTS.md` должен быть **тонким overlay**.

Он не должен копировать generic правила AI Dev Team.

Он должен указывать только специфичные для Text Recognition Core правила, например:

- соблюдение этой SPEC;
- immutable raw recognition;
- engine abstraction;
- отсутствие application business logic;
- сохранение traceability;
- privacy-by-default;
- обязательные contract tests для engine adapters.

---

# 76. Subagents

Перед созданием project-specific subagents Codex обязан проверить существующую AI Dev Team.

Не создавать дубликаты generic:

```text
architect
security reviewer
tester
documentation agent
```

если они уже существуют глобально.

Project-specific subagent допускается только при объективной необходимости.

Например, потенциально:

```text
ocr-domain-reviewer
```

но только если его обязанности невозможно нормально покрыть существующими агентами.

---

# 77. Skills

Аналогично:

не создавать project-local Skill, если задача уже покрывается глобальным Skill.

Project-specific Skills допустимы для:

- OCR benchmark workflow;
- recognition engine contract verification;
- golden dataset validation;

если они действительно уменьшают контекст и повторение инструкций.

---

# 78. Hooks

Не создавать второй generic Git workflow.

Project hooks допускаются для специфичных проверок, например:

```text
Recognition schema compatibility check
Golden dataset regression check
Sensitive fixture detection
```

Но они должны интегрироваться с существующей AI Dev Team.

---

# 79. MCP

При создании КАРКАСА описать будущий MCP interface Text Recognition Core.

Не требуется немедленная полноценная реализация MCP, если она находится на более позднем этапе ROADMAP.

MCP должен быть интерфейсом к Application/Core.

---

# 80. Context budget

КАРКАС должен проектироваться с минимизацией перегрузки AI-контекста.

Принцип:

```text
global generic knowledge → AI Dev Team

project-specific knowledge → repository overlay
```

Не копировать десятки страниц глобальных инструкций в локальный AGENTS.md.

SPEC, ARCHITECTURE и текущий PROMPT должны загружаться по необходимости.

---

# 81. Source-of-truth hierarchy

При конфликте документов использовать следующий приоритет:

```text
specs/system.spec.md
    ↓
DECISIONS.md
    ↓
ARCHITECTURE.md
    ↓
PROMPTS / current stage
    ↓
docs/AI_STATUS.md
```

Если реализация требует отойти от SPEC:

1. не изменять архитектуру молча;
2. зафиксировать причину;
3. создать соответствующее решение в DECISIONS;
4. при необходимости обновить SPEC.

---

# 82. Главный архитектурный инвариант

Ни одна последующая реализация не должна разрушить следующий принцип:

```text
              ┌─ Engine A
              ├─ Engine B
Applications → TRC Core
              ├─ Engine C
              └─ Future Engine
```

Приложения зависят от стабильного Text Recognition Core contract.

Core зависит от recognition engines только через adapters.

---

# 83. Критерий успеха проекта

Text Recognition Core считается успешно выделенным в самостоятельный проект, если новый OCR/HTR consumer можно подключить примерно следующим образом:

```text
New Application
       ↓
New Application Adapter
       ↓
Existing TRC API
```

без:

- копирования OCR pipeline;
- изменения существующих приложений;
- прямой зависимости от конкретного OCR engine;
- переписывания correction system.

---

# 84. Инструкция Codex после получения этой SPEC

После чтения данного документа Codex должен:

1. изучить глобальную конфигурацию **AI Dev Team / AI Dev Team Codex**;
2. изучить существующие `AGENTS.md`, rules, skills, hooks, MCP и subagents;
3. определить, что уже предоставляется глобальной системой;
4. не создавать их дубликаты;
5. рассматривать новый repository как **project overlay**;
6. на основании `specs/system.spec.md` спроектировать полный КАРКАС Text Recognition Core;
7. подготовить архитектуру;
8. определить технологический стек и обосновать выбор;
9. определить API и data contracts;
10. определить correction/revision model;
11. определить contracts RecognitionEngine;
12. определить adapters Personal Chronicle, Receipt Scanner и Tutor;
13. подготовить security model;
14. подготовить testing/benchmark strategy;
15. создать ROADMAP;
16. разбить реализацию на небольшие последовательные PROMPTS;
17. каждому PROMPT назначить tests, DoD и acceptance criteria;
18. настроить `docs/AI_STATUS.md`, `docs/AI_PLAN.md`, `docs/DEV_LOG.md` и `docs/LEARNING_LOG.md` без дублирующих status-файлов;
19. добавить только необходимые project-specific hooks/skills/subagents/MCP;
20. проверить весь КАРКАС на конфликт и дублирование AI Dev Team;
21. **не начинать крупную реализацию OCR Core до завершения проектирования КАРКАСА**, если пользователь явно не потребовал обратного.

---

# 85. Конечный результат этапа Context Automation

После выполнения Codex в repository должен существовать согласованный набор примерно следующего вида:

```text
AGENTS.md

specs/
    README.md
    system.spec.md

prompts/
    README.md
    stage-*.md

docs/
    AI_STATUS.md
    AI_PLAN.md
    ROADMAP.md
    DEV_LOG.md
    LEARNING_LOG.md
    ARCHITECTURE.md
    API.md
    DATA_MODEL.md
    INTEGRATIONS.md
    SECURITY.md
    TEST_STRATEGY.md
    DECISIONS.md
    DESIGN.md
```

Дополнительные:

```text
.codex/
rules/
skills/
hooks/
agents/
mcp/
```

создаются **только если Text Recognition Core действительно требует project-specific дополнения к глобальному AI Dev Team**.

Отсутствие локального дубликата является нормальным и предпочтительным результатом.

---

# 86. Итоговая концепция

Text Recognition Core должен стать не:

> «ещё одной программой для OCR»

а:

> **унифицированной инфраструктурой машинного чтения документов для всех проектов пользователя.**

Его фундаментальные возможности:

```text
OCR
+
HTR
+
Layout
+
Confidence
+
Corrections
+
Revisions
+
Engine Abstraction
+
Application Adapters
```

Первоначальные consumers:

```text
Personal Chronicle
Receipt Scanner
Tutor
```

а дальнейшие проекты должны иметь возможность подключаться к Core без архитектурной переделки самого ядра.

---

# 87. Реестр стабильных требований и критериев приёмки

Этот реестр присваивает идентификаторы обязательным требованиям существующих разделов, не заменяя их подробное содержание.

## Функциональные требования

- `FR-001` — единый versioned `RecognitionRequest`/`RecognitionResult` для OCR, HTR, MIXED и AUTO (разделы 7–10, 57).
- `FR-002` — результат хранит Document → Page → Region → Line → Token, layout, coordinates, confidence и alternatives (разделы 10–16).
- `FR-003` — каждый engine подключается только через `RecognitionEngine`; registry поддерживает выбор, fallback и region routing (разделы 25–27).
- `FR-004` — raw recognition и оригинальный source не перезаписываются preprocessing или corrections (разделы 17–18, 28, 51).
- `FR-005` — corrections формируют traceable revisions, current view, diff и rollback (разделы 19–22).
- `FR-006` — partial re-recognition поддерживает page/region/line без обязательной обработки всего документа (раздел 23).
- `FR-007` — длительная обработка использует async job lifecycle, progress, cancellation и idempotency (разделы 37–39, 48–49, 55).
- `FR-008` — Personal Chronicle, Receipt Scanner и Tutor интегрируются через отдельные application adapters/projections с provenance к source IDs (разделы 33–36, 67).
- `FR-009` — REST, Python SDK, CLI, jobs и будущий MCP используют один Application/Core (разделы 52–54).
- `FR-010` — schemas и stable identifiers явно версионируются и не меняют семантику незаметно (разделы 56–57).

## Нефункциональные требования

- `NFR-001` — Core полностью работает offline при наличии локального engine/model (раздел 59).
- `NFR-002` — domain/application не зависят от web framework, database, queue или OCR SDK (разделы 6, 52, 58).
- `NFR-003` — job сохраняет input hash, engine/model/pipeline versions, configuration и timestamp для воспроизводимости (разделы 42–43).
- `NFR-004` — telemetry содержит технические метрики, но не пользовательский text/image/path по умолчанию (раздел 44).
- `NFR-005` — unsupported capability, engine failure и low confidence обрабатываются явно и без silent data loss (разделы 40–41, 61).

## Требования безопасности

- `SEC-001` — `LOCAL_ONLY` технически блокирует network egress для job и всех его adapters (разделы 30, 59).
- `SEC-002` — image/PDF/archive и metadata считаются недоверенным вводом; validation защищает от traversal, malformed files, bombs и execution (раздел 47).
- `SEC-003` — logs, traces, metrics и errors не раскрывают распознанный text, изображения, токены доступа или локальные пути по умолчанию (разделы 44, 47).
- `SEC-004` — corrections и raw data не участвуют в training/dataset export без отдельного явного согласия; default `false` (разделы 31–32).
- `SEC-005` — configurable file/page/dimension/time/concurrency/memory limits применяются до и во время обработки (раздел 48).
- `SEC-006` — binary decoders, metadata parsers и OCR/model runtimes выполняются в disposable least-privilege worker с no-network policy, частным temp root, OS resource caps, hard kill и cleanup.
- `SEC-007` — локальный REST по умолчанию доступен только через loopback/локальный IPC и требует сгенерированный local credential или проверенные OS peer credentials; non-loopback относится к remote gate.
- `SEC-008` — actor/tenant/source role для audit, corrections, consent, idempotency и authorization выводятся из доверенного execution context, а не из заявленного клиентом identity/role.
- `SEC-009` — dependencies и model artifacts hash-locked/verified; executable/object deserialization запрещена без отдельного sandboxed conversion decision.
- `SEC-010` — request/output/disk/queue/cardinality quotas, cache/idempotency scope, retention/deletion и observability lifecycle предотвращают amplification и cross-scope leakage.

## Производительность

- `PERF-001` — baseline фиксирует latency, pages/sec, peak memory и CPU/GPU utilization на versioned golden dataset; численные release thresholds утверждаются после Stage 02 benchmark, а не выдумываются на этапе КАРКАСА (разделы 45–46, 62).

## Критерии приёмки

- `AC-001` — schema validation принимает валидные примеры всех режимов и отклоняет неизвестные/некорректные значения machine-readable error.
- `AC-002` — один parametrized contract suite проходит для каждого включённого `RecognitionEngine` adapter.
- `AC-003` — replay corrections создаёт тот же current view, а hash raw snapshot до/после correction и rollback совпадает.
- `AC-004` — integration test с network deny проверяет отсутствие egress в `LOCAL_ONLY`, включая fallback и telemetry exporters.
- `AC-005` — benchmark report содержит dataset, engine/model/pipeline versions, CER/WER, latency и memory; приватные fixtures отсутствуют.
- `AC-006` — dependency/static review подтверждает отсутствие consumer business entities в Core и прямых engine SDK imports вне adapters.
- `AC-007` — parser/OCR worker crash, hang, limit breach и cancellation завершаются hard kill/cleanup без egress или доступа вне private job roots.
- `AC-008` — local service отказывается от wildcard/non-loopback bind без remote profile и отклоняет missing/wrong credentials и hostile browser Origin.
- `AC-009` — spoofed actor/source role, cross-document target, cache/idempotency collision и revoked/forged consent не создают duplicate job, не раскрывают и не изменяют чужое состояние.
- `AC-010` — tampered dependency/model, lock drift и запрещённый serialization format блокируются до загрузки.
- `AC-011` — authorized deletion соблюдает retention policy и удаляет либо криптографически делает недоступными original/raw/cache/export/temp/backup copies в установленный SLA, сохраняя только минимальный audit tombstone; preprocessing/corrections никогда не запускают deletion.

## Открытые вопросы до реализации

- Численные confidence/review thresholds и performance budgets утверждаются после versioned benchmark.
- Baseline OCR/HTR engines выбираются по quality/security/license/resource evidence, не по предположению.
- Retention, deletion, encryption-at-rest и multi-tenant isolation требуют deployment profile; отсутствие решения блокирует remote mode, но не локальный contract-first этап.
