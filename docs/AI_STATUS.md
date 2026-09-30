# Состояние проекта для AI

## Текущий Stage 02 — routing и synthetic golden smoke (2026-09-30)

- Status: PARTIAL; pure immutable routing planner реализован и проверен локально.
- `EngineRegistry` ограничен 32 descriptors; OCR/HTR capabilities, explicit selection,
  deterministic rank/name order, privacy `LOCAL_ONLY`, 4096 unique region routes и
  fail-closed errors покрыты unit tests. Ни один engine не исполняется.
- SPEC: `specs/features/engine-routing.spec.md`; rationale ADR-013.
- Synthetic printed golden smoke v1: три авторских PNG (eng/rus/ukr), manifest, SHA-256/dimensions и fixed-corpus Tesseract diagnostic. Digest tamper и path escape отклоняются до запуска engine. Installed Tesseract 5.5.3 scored CER/WER 0 только на этих простых samples; `docs/evidence/stage02-printed-smoke.md` фиксирует latency.
- Stage 02 остаётся открытым: нет binary decoder/intake, изолированного worker, representative golden corpus/benchmark, принятого OCR adapter и runtime end-to-end evidence.
- Установленный Tesseract 5.5.3 с языками eng/rus/ukr/osd — только доступный
  benchmark candidate; проектный пакет от него не зависит.
- Current local validation: 41 tests PASS via both `uv run pytest` and `uv run python -m pytest` after explicit pytest project-root import path; Ruff check/format PASS, strict mypy PASS. Restricted Windows Temp required a writable workspace `--basetemp`.


## Текущий Stage 01 — typed foundation (2026-09-30)

- Status: verified locally for the Stage 01 contract; branch `feature/trc-stage-01-foundation`.
- Source: Python 3.13 library packaging, immutable domain values and Document → Page →
  Region → Line → Token hierarchy, separate raw/current revision IDs, application ports,
  strict Pydantic v2 request/result boundary, generated versioned JSON Schema.
- Local checks: 29 unit/schema/supply-chain tests PASS; Ruff check/format PASS; mypy strict
  PASS; `uv lock --check --offline` PASS; wheel/sdist build PASS; isolated wheel install,
  import and packaged schema read PASS. Two-step clean offline restore with locked
  Hatchling and `--no-build-isolation` PASS. `uv audit --locked`: 19 packages, zero known
  vulnerabilities/adverse statuses after pytest `8.4.2 → 9.1.1`. CycloneDX SBOM and
  license inventory: `docs/evidence/stage01-supply-chain.md`.
- Environment: CPython 3.13.7 is installed at a machine-local exact path although
  `py -0p` lists only 3.12; `uv` 0.12.3 created project-local `.venv`. No machine path
  is embedded in `pyproject.toml`.
- The accepted local path pins PyPI as the default index in `pyproject.toml`; registry
  artifacts including the build backend are SHA-256 locked. Default isolated builds
  can resolve build deps separately, so the documented verified path uses the
  two-step lock-aware environment plus `--no-build-isolation`.
- Boundary review: request/result JSON is byte-bounded and rejects invalid hierarchy,
  coordinates, IDs, language tags, non-finite confidence, unknown fields and unknown
  capabilities. Public parse functions expose redacted machine codes on validation
  failure. Domain/application imports contain no infrastructure or executable
  deserialization; the no-engine/no-storage boundary was checked against source.
- Actual model artifact loading, binary parser isolation and live OCR remain Stage 02.
- Runtime limits: no engine/model loader, worker, storage, REST, job execution or external
  integration exists. Schema limits do not prove binary input isolation.
- NEXT: Stage 02 requires a bounded synthetic golden slice and decoder/engine isolation
  contract before any OCR adapter is activated. No live OCR acceptance is claimed.

## Historical scaffold record (2026-08)

## Governance migration — 2026-08-24

- Шесть подробных stage-файлов полностью объединены в `prompts/STAGES.md`; project overlay — PASS.
- Продуктовый test environment не настроен в этом repository; продуктовый код не изменялся.
- Репозиторий находится в `${PROJECTS_ROOT}/text-recognition-core` (локальный default: `~/text-recognition-core`); `main` синхронизирован с `origin/main`.

**Обновлено:** 2026-08-13

**Этап:** bootstrap архитектуры и дизайна завершён; реализация не начата.

**Ветка:** `docs/project-skeleton`.

## Реализовано

- Инициализирован самостоятельный Git-репозиторий; `origin` указывает на `https://github.com/ZabulaAleksey/text-recognition-core.git`.
- По исходной SPEC создан полный КАРКАС: канонические требования, архитектура, контракты API, данных и интеграций, решения, стратегия безопасности и тестирования, roadmap и stage prompts.
- Тонкий проектный `AGENTS.md` и аудит совместимости контекста переиспользуют глобальную AI Dev Team без локальных дубликатов agents, hooks, Skills, MCP и config.
- В системную SPEC добавлены стабильные идентификаторы требований и критериев приёмки.

## Не реализовано

- Отсутствуют пакет Python, REST API, хранилище, jobs, OCR/HTR-engine, adapters и UI.
- OCR/HTR-engine ещё не выбран; для выбора требуется golden benchmark этапа 02.
- Удалённое развёртывание запрещено до завершения соответствующих решений и проверок безопасности; локальный REST ограничен loopback и локальными учётными данными.

## Известные вопросы и технический долг

- Пока отсутствуют golden datasets и численные пороги качества и производительности.
- Библиотеки PDF и изображений, базовый OCR, HTR-engine, конкретная локальная политика хранения и шифрования, а также удалённый профиль остаются ожидающими ADR. Изоляция декодеров, целостность supply chain и идентификация локального сервиса уже являются обязательными решениями.
- Исходный `Определение для Codex.md` сохранён как bootstrap brief; каноническая терминология workspace находится в `docs/PROJECT_FRAMEWORK.md`.

## Блокеры

Технических блокеров для этапа 01 нет. Поскольку удалённый репозиторий пуст, у первой публикации нет общей базы для merge: после первоначального commit КАРКАСА локальная ссылка `main` будет указывать на тот же commit, а работа останется в `docs/project-skeleton`. Push по-прежнему требует явного разрешения пользователя. Последующие feature-ветки используют обычный процесс review и merge.

## Следующее рекомендуемое действие

Проверить КАРКАС, затем выполнить `prompts/stage-01-foundation.md`. Ограниченный текущий срез кратко описан в `docs/AI_PLAN.md`.
