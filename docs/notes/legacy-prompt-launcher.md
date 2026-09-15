# Исторический prompt index

Содержимое прежнего `prompts/README.md` сохранено ниже. SHA-256 source worktree: `d7cce51100831ca44b5159ceea5e1cf8022f69152c72bec91b47266b2b2f63f7`. Ссылки `stage-01-foundation.md` — `stage-06-quality-hardening.md` отсутствовали уже в GitHub main перед миграцией.

# Поэтапные prompts реализации

Каждый файл — самостоятельный ограниченный этап для отдельной сессии Codex, review и commit. Выполнять по порядку; перед стартом сверить `docs/AI_STATUS.md`, зависимости и решения. Prompt не изменяет требования SPEC.

| Этап | Prompt | Основной результат |
|---|---|---|
| 01 | [`stage-01-foundation.md`](stage-01-foundation.md) | типизированный фундамент domain/application |
| 02 | [`stage-02-engine-pipeline.md`](stage-02-engine-pipeline.md) | безопасный pipeline и выбранный OCR adapter |
| 03 | [`stage-03-corrections-revisions.md`](stage-03-corrections-revisions.md) | append-only corrections/revisions/rerun |
| 04 | [`stage-04-storage-jobs-api.md`](stage-04-storage-jobs-api.md) | локальные persistence/jobs/REST |
| 05 | [`stage-05-application-adapters.md`](stage-05-application-adapters.md) | integration packages consumers |
| 06 | [`stage-06-quality-hardening.md`](stage-06-quality-hardening.md) | HTR/mixed routing и укрепление качества |

Интерфейсы и deployment этапа 07 остаются необязательными и после утверждения требуют новой SPEC и prompt.

После каждого этапа: выполнить его gates, получить соответствующий риску review, обновить только фактическую документацию, создать commit и спросить пользователя перед merge. Никогда не запускать следующий этап автоматически.
