# Инженерные решения

Статусы: `Принято`, `Предложено`, `Заменено`. Дата bootstrap: 2026-08-13.

## ADR-001 — Самостоятельный репозиторий и тонкий overlay

**Статус:** принято.

TRC развивается как самостоятельный Git repository. Файлы проекта содержат только domain requirements, contracts, staged plan и локальные инварианты; общие agents, hooks, Skills, Git workflow и MCP наследуются из `codex-workspace`.

Альтернативы: хранить TRC внутри consumer или скопировать AI Dev Team. Они создают дубли pipeline и управления и нарушают границы SPEC.

## ADR-002 — Модульный монолит Python, сначала библиотека

**Статус:** принято для первоначальной реализации.

Использовать пакет, совместимый с Python 3.13, с domain/application ports. Начать с embedded/offline profile; FastAPI является поздним REST adapter, а не местом business logic. Причины: экосистема Python для OCR/HTR, возможность локального inference и единый Core для library/service/CLI/MCP.

Альтернативы: microservices с service-first подходом создают слишком раннюю operational complexity; Rust core усложняет ML integrations до подтверждения bottleneck. Rust/WASM остаются путями расширения после profiling.

Python 3.13 является стабильной поддерживаемой линией согласно официальной документации: <https://docs.python.org/3.13/>.

## ADR-003 — Типизированные контракты и генерируемые схемы

**Статус:** принято.

Domain types остаются независимыми от фреймворка; Pydantic v2 применяется на границах validation/serialization со strict configuration, `extra='forbid'` для requests v1 и сгенерированной JSON Schema. FastAPI генерирует OpenAPI из тех же transport models. Запрещено вручную поддерживать второй источник истины OpenAPI/DTO.

Pydantic документирует typed validation и генерацию JSON Schema: <https://docs.pydantic.dev/latest/concepts/models/> и <https://docs.pydantic.dev/latest/concepts/json_schema/>. FastAPI использует объявления типов и OpenAPI: <https://fastapi.tiangolo.com/features/>.

## ADR-004 — Нормализованные координаты исходной страницы

**Статус:** принято.

Публичная модель использует нормализованные координаты `[0,1]` с началом в левом верхнем углу, при этом Page хранит исходные размеры в пикселях. Preprocessing сохраняет обратимые transforms. Это делает contracts независимыми от resolution engine и сохраняет overlay mapping.

Альтернатива только в пикселях привязывает результат к производным изображениям; только нормализованные координаты без dimensions затрудняют точный rendering.

## ADR-005 — Неизменяемые доказательства и append-only линейные revisions

**Статус:** принято для MVP.

Raw snapshots являются append-only. Corrections ссылаются на `base_revision_id`; каждое принятое исправление добавляет revision с optimistic concurrency. Split/merge/rerun использует ancestry links. Линейная история уменьшает неоднозначность; branching/merge отложены.

## ADR-006 — Первоначальный профиль локального хранения

**Статус:** принято для этапа 04.

Первый adapter: metadata SQLite, атомарные content-addressed blobs файловой системы и постоянный local worker. Storage остаётся за ports. PostgreSQL, object storage и external queue требуют подтверждённой потребности remote deployment и отдельного ADR миграции.

## ADR-007 — Выбор engine только по подтверждениям

**Статус:** предложено; решение принимается на этапе 02.

Сравнить как минимум локальные варианты, совместимые с Tesseract и PaddleOCR, на одобренных печатных golden data на украинском, русском и английском языках. Оценить качество CER/WER/layout, license, offline support, CPU memory/latency, packaging и поверхность вредоносного ввода. Включить ровно один базовый OCR adapter. HTR engine остаётся только контрактом до собственного репрезентативного benchmark.

До этой проверки ни один engine не получает архитектурной привилегии.

## ADR-008 — Adapters приложений находятся вне домена Core

**Статус:** принято.

Интеграция имеет два контракта: input profile/hints consumer и output projector. Сущности Chronicle/Receipt/Tutor находятся в integration packages или репозиториях consumers; Core предоставляет только понятия распознавания и provenance.

## ADR-009 — Remote mode требует отдельного допуска

**Статус:** принято.

Сначала разрешено реализовать `LOCAL_ONLY`/embedded profile. Remote deployment заблокирован до появления решений об authentication, authorization, tenant isolation, encryption/retention, rate limiting, audit и incident logging. Это не позволяет цели интерфейса скрыто расширить границу доверия.

## ADR-010 — Изоляция недоверенной обработки и целостность артефактов

**Статус:** принято.

Декодирование binary, parsing metadata и inference OCR/model должны выполняться в одноразовых workers с минимальными правами, запретом сети, приватными per-job roots, OS limits и очисткой после hard kill. Начиная с этапа 01 dependencies закрепляются hashes и сканируются; артефакты model/engine требуют проверенных digests/signatures. Исполняемая и объектная десериализация запрещена без отдельного решения о sandboxed conversion.

## ADR-011 — Граница идентификации локального сервиса

**Статус:** принято.

Локальный REST по умолчанию использует loopback/local IPC и аутентифицирует сгенерированный bearer token высокой энтропии или проверенные OS peer credentials. Bootstrap token использует приватный файл с проверенными permissions или OS credential store, но не аргументы CLI или environment output, который может попасть в logs; проверка выполняется за постоянное время, а rotation/revocation инвалидирует старые tokens. При отсутствии безопасного storage запуск завершается закрытым отказом. CORS полностью запрещён, cookie auth отсутствует. Non-loopback bind является remote profile и не может включаться одним удобным флагом.

## ADR-012 — Stage 01 lock-aware Python build

**Статус:** принято для local library foundation 2026-09-30.

**AUTONOMOUS_DECISION.** Context: `uv sync --locked` проверяет project graph, но
изолированная PEP 517 сборка может отдельно разрешить `hatchling` и зависимости
вне `uv.lock`. Варианты: оставить default build и считать hashes достаточными;
создать второй requirements lock; или включить build backend в dev group и выполнять
двухшаговый restore с `--no-build-isolation`. Выбран последний: один lock, явно
указанный PyPI index, сначала locked dependencies без project, затем project build
в уже locked environment. Он обратим через Git revert без миграции данных.
Evidence: clean offline two-step restore, no-build-isolation wheel/sdist, installed
wheel smoke, 29 tests, Ruff/mypy и OSV audit 19/0. Rollback: revert Stage 01 commit,
удалить только проверенную rebuildable `.venv` по отдельной cleanup процедуре.
Affected stage: 01. Runtime OCR/model loaders остаются Stage 02 и не получают
разрешения из этого решения.

## ADR-013 — Детерминированный planning slice до включения OCR runtime

**Статус:** принято для Stage 02 local partial, 2026-09-30.

**AUTONOMOUS_DECISION.** Context: Stage 02 требует routing и fallback, но выбор OCR
engine зависит от golden benchmark и worker isolation. Варианты: преждевременно
подключить установленный на машине Tesseract; ждать всего runtime; или выделить
pure immutable planner. Выбран planner: максимум 32 descriptors, явные OCR/HTR
capabilities, стабильный rank/name порядок, `LOCAL_ONLY` до выдачи route, explicit
selection без fallback. Это обратимо через revert, persistent state отсутствует.
Evidence: unit/privacy/negative tests, полный suite и static checks в `docs/AI_STATUS.md`.
Rollback: revert Stage 02 planning commit. Affected stage: 02. Установленный
Tesseract 5.5.3 с `eng/rus/ukr/osd` — кандидат benchmark, не выбранный adapter.

## Ожидающие решения

- `ADR-P01`: библиотеки декодирования PDF/image после исследования security/license/resources.
- `ADR-P02`: базовый OCR engine после benchmark этапа 02.
- `ADR-P03`: конкретная политика retention/deletion/encryption/observability для локального persistence profile; должна быть принята до записи постоянных пользовательских данных на этапе 04.
- `ADR-P04`: численные пороги review и performance budgets релиза по результатам baseline.
- `ADR-P05`: HTR engine и GPU policy после появления репрезентативного handwriting dataset.
