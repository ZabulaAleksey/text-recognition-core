# Проектный overlay Text Recognition Core

Наследуй общие правила из `~/codex-workspace/AGENTS.md`. Этот файл добавляет только инварианты TRC.

## Источники истины

1. `specs/system.spec.md` — требования продукта.
2. `docs/DECISIONS.md` — принятые существенные решения.
3. `docs/ARCHITECTURE.md`, `docs/API.md`, `docs/DATA_MODEL.md` — границы и контракты.
4. текущий stage prompt / `docs/AI_PLAN.md` — ограниченный исполняемый срез.
5. `docs/AI_STATUS.md` — фактическое состояние.

Не менять требования или публичные контракты молча. При конфликте остановить спорное изменение, зафиксировать решение и синхронизировать источники истины.

## Обязательные инварианты

- Raw recognition — неизменяемый snapshot; corrections и revisions только добавляются.
- Core зависит от OCR/HTR engines только через `RecognitionEngine` port и adapters.
- Бизнес-логика Personal Chronicle, Receipt Scanner и Tutor не входит в Core.
- Stable IDs, provenance, engine/model/pipeline versions и параметры сохраняют traceability.
- Confidence нормализуется в `0.0..1.0`; вероятностный результат не выдаётся за достоверный.
- `LOCAL_ONLY` запрещает сетевой egress; training use требует отдельного opt-in и по умолчанию выключен.
- Распознанный пользовательский текст, изображения и пути не попадают в telemetry/logs по умолчанию.
- Файлы/PDF/изображения считаются недоверенным вводом; resource limits и безопасные временные файлы обязательны.
- Binary decoding/OCR/model loading выполняются изолированно; dependencies/models проверяются по lock/hash и unsafe deserialization запрещена.
- Actor/tenant/consent берутся из доверенного execution context; local REST не расширяет bind/identity boundary молча.
- Каждый engine adapter проходит один contract test suite; приватные реальные документы запрещены в публичных fixtures.
- REST, CLI, SDK, jobs и будущий MCP обращаются к одному Application/Core.

## Маршрутизация контекста

- Domain/API: соответствующие `FR-*`/`AC-*`, `docs/API.md`, `docs/DATA_MODEL.md`, ADR и contract tests.
- Engine/pipeline: разделы SPEC 25–29, `docs/ARCHITECTURE.md`, `docs/TEST_STRATEGY.md`, engine contract tests.
- Corrections/revisions: разделы SPEC 17–23, `docs/DATA_MODEL.md`, revision ADR и replay/concurrency tests.
- Storage/jobs: разделы SPEC 37–59, `docs/SECURITY.md`, storage/job ADR и integration tests.
- Application adapter: `docs/INTEGRATIONS.md`, relevant result schema и adapter tests; не загружать логику остальных consumers.
- Security/privacy: `SEC-*`, `docs/SECURITY.md` и negative tests; использовать security review.
- Текущий этап: читать только соответствующий файл из `prompts/`, `docs/AI_PLAN.md` и компактный `docs/AI_STATUS.md`.

Не загружать автоматически все prompts, logs, fixtures и весь SPEC, если достаточно конкретных разделов.


## Локальные правила тестирования

### Тестовый контракт
- После принятия тестов/fixtures/golden-сценариев они считаются контрактом и в этом цикле не редактируются.
- Новые требования не должны обходить существующий контрактные проверки.

### Unit / integration / component
- Рекомендуемый базовый стек после настройки окружения: `python -m pytest`.
- Пока dedicated test directories не стабилизированы, обязательный минимум — поддержать порядок появления и запусков unit → integration → component по мере роста модуля.

### E2E
- Автоматизированные E2E в текущем состоянии не настроены.
- Критичные будущие сценарии (OCR→correction pipeline, adapter contracts) ожидают инфраструктуру; до этого: `BLOCKED_BY_TEST_INFRASTRUCTURE_TRC`.
