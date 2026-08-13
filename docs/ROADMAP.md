# Дорожная карта

Этапы выполняются последовательно, если prompt явно не разрешает независимое исследование. Каждый этап реализации завершается тестами, review, синхронизацией status/log, commit и merge под управлением пользователя.

## Завершено

### K0 — КАРКАС проекта

- самостоятельный локальный Git repository и настроенный remote;
- каноническая SPEC и стабильный registry требований;
- архитектура и контракты API, данных и интеграций;
- решения о stack и архитектуре;
- стратегия security, testing и совместимости контекста;
- project overlay, stage prompts и текущий status.

Product source code не создавался.

## Текущий этап

### Этап 01 — Фундамент и типизированные контракты

Создать границы пакета Python, неизменяемые типизированные domain/application contracts, сгенерированные schemas, in-memory ports и фундаментальные tests. Без реального OCR SDK, REST или persistent storage.

Gate: доказаны `FR-001`, `FR-002`, `FR-010`, `AC-001`, `AC-010`, правила dependencies и базовая линия supply chain с закреплёнными hashes.

## Запланировано

### Этап 02 — Intake, pipeline и один базовый OCR adapter

Реализовать безопасные ports intake/preprocessing, registry и выбор engines, fake adapter и локальный OCR adapter, выбранный по подтверждениям. Создать golden/baseline report и выбрать engine через ADR.

Зависит от этапа 01. Gate: `FR-003`, `NFR-003`, `PERF-001`, `AC-002`, `AC-005`, `AC-007`, `AC-010`; изоляция decoder/engine обязательна.

### Этап 03 — Corrections, revisions и частичный повторный запуск

Реализовать append-only raw snapshot, детерминированный replay corrections, оптимистичные линейные revisions, стабильную ancestry и orchestration повторного запуска region/line.

Зависит от этапов 01–02. Gate: `FR-004`–`FR-006`, `AC-003`, `AC-009`; доверенный actor и отзываемая модель consent.

### Этап 04 — Локальное persistence, jobs и REST adapter

Добавить adapters SQLite/filesystem, постоянный local worker, idempotency/cancellation/progress/cache и REST adapter FastAPI. Remote mode остаётся отключённым.

Зависит от этапов 01–03 и принятого локального ADR-P03 о retention/deletion. Gate: `FR-007`, `SEC-002`, `SEC-005`, `SEC-007`, `SEC-010`, `AC-008`, `AC-009`, `AC-011`, тесты recovery и compatibility.

### Этап 05 — Контракты интеграции приложений

Реализовать profiles/projectors consumers для Personal Chronicle, Receipt Scanner и Tutor как integration packages с provenance и без утечки domain.

Зависит от стабильного API result/revision. Gate: `FR-008`, `AC-006` и adapter tests.

### Этап 06 — HTR, mixed routing и укрепление качества

Создать репрезентативный handwriting/mixed golden set, выбрать HTR adapter через ADR, реализовать routing/fallback regions и завершить regression gates privacy/security/performance.

Зависит от этапов 02–05. Gate: `NFR-001`, `NFR-004`, `SEC-001`–`SEC-010`, `AC-004`–`AC-011`.

## Позднее / необязательно

### Этап 07 — Дополнительные интерфейсы и профили развёртывания

Сначала CLI, если он будет полезен; product MCP, remote service, external queue/storage, GPU/distributed execution и другие интерфейсы — только после подтверждения потребности и собственных security/operational решений.

### Исследовательские направления

Personalized HTR, export dataset и fine-tuning, ensemble recognition, OCR математических выражений, таблиц и диаграмм, WASM/mobile/edge и LLM postprocessing остаются экспериментальными до появления отдельных SPEC, ADR и metrics.

## Определение релиза

Core MVP не считается готовым только потому, что существует КАРКАС. Требуются runtime checklist из раздела 63 SPEC, все относящиеся к нему acceptance evidence, утверждённые baseline benchmarks и release/security review.
