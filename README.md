# Text Recognition Core

Text Recognition Core (TRC) — проектируемое переиспользуемое ядро OCR/HTR с единым результатом распознавания, неизменяемым raw snapshot, исправлениями, revisions и сменяемыми recognition engines.

Сейчас repository находится на этапе КАРКАСА: здесь определены требования, архитектура, контракты, безопасность, проверки и последовательность будущей реализации. Исходного кода продукта пока нет намеренно.

## Основной инвариант

```text
Applications → stable TRC contracts → RecognitionEngine ports → engine adapters
```

Приложения не зависят от Tesseract, PaddleOCR, TrOCR или другого конкретного engine. TRC не содержит бизнес-логику Personal Chronicle, Receipt Scanner или Tutor.

## Навигация

- [`specs/system.spec.md`](specs/system.spec.md) — канонические продуктовые требования.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — bounded contexts, зависимости и потоки.
- [`docs/API.md`](docs/API.md) и [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — публичные и доменные контракты.
- [`docs/SECURITY.md`](docs/SECURITY.md) — threat model и privacy/offline ограничения.
- [`docs/TEST_STRATEGY.md`](docs/TEST_STRATEGY.md) — проверки, benchmarks и quality gates.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — порядок развития.
- [`docs/STAGES.md`](docs/STAGES.md) — выбранный этап, фактическое состояние и следующий шаг.

`Определение для Codex.md` сохранено как исходный bootstrap-brief. Общие для всех проектов определения КАРКАСА и АВТОМАТИЗАЦИИ КОНТЕКСТА вынесены в `~/.codex/docs/PROJECT_FRAMEWORK.md`; при расхождении действуют канонические имена и каскад workspace.

## Следующий шаг

После review КАРКАСА явно запустить Stage 01 по `docs/STAGES.md`; повреждённый исторический launcher требует читаемого ограниченного контракта до реализации. Merge остаётся отдельным решением пользователя; push документационной ветки разрешён ранее.
