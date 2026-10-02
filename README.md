# Text Recognition Core

Text Recognition Core (TRC) — проектируемое переиспользуемое ядро OCR/HTR с единым результатом распознавания, неизменяемым raw snapshot, исправлениями, revisions и сменяемыми recognition engines.

КАРКАС принят. Stage 01 реализует локальный Python 3.13 package с immutable domain hierarchy,
framework-independent ports, strict versioned request/result models и генерируемыми JSON Schema.
OCR engine, adapters, persistence и REST ещё не реализованы.

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
- [`docs/STAGES.md`](docs/STAGES.md) — выбранный этап, plan/status/evidence/NEXT.
- [`docs/notes/legacy-prompt-launcher.md`](docs/notes/legacy-prompt-launcher.md) — исторический launcher index; текущий этап выбирается через docs/STAGES.md.

`Определение для Codex.md` сохранено как исходный bootstrap-brief. Общие для всех проектов определения КАРКАСА и АВТОМАТИЗАЦИИ КОНТЕКСТА вынесены в `~/.codex/docs/PROJECT_FRAMEWORK.md`; при расхождении действуют канонические имена и каскад workspace.

## Следующий шаг

Для clean restore Stage 01: `uv sync --locked --no-install-project`, затем
`uv sync --locked --no-build-isolation`. Для проверки: `uv run pytest`,
`uv run ruff check src tests`, `uv run ruff format --check src tests`, `uv run mypy src`,
`uv lock --check --offline` и `uv audit --locked`. Offline build:
`uv build --offline --no-build-isolation` из активной проектной `.venv`.
Python должен удовлетворять `requires-python` в pyproject.toml; проверенные версии и restore limitations находятся в selected STAGES record. Source of truth для
статуса и открытых gates — [`docs/STAGES.md`](docs/STAGES.md). Текущий Stage 02 остаётся partial; isolated decoder и representative OCR benchmark ещё не приняты.
