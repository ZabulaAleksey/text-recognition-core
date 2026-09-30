# Поэтапные prompts реализации

Каждый heading в `prompts/STAGES.md` — самостоятельный ограниченный этап для review
и commit. Перед стартом сверить `docs/AI_STATUS.md`, зависимости и решения. Prompt не
изменяет требования SPEC. Шесть прежних отдельных файлов объединены в `STAGES.md`.

| Этап | Prompt | Основной результат |
|---|---|---|
| 01 | [`stage-01-foundation`](STAGES.md#stage-01-foundation) | типизированный фундамент domain/application |
| 02 | [`stage-02-engine-pipeline`](STAGES.md#stage-02-engine-pipeline) | безопасный pipeline и выбранный OCR adapter |
| 03 | [`stage-03-corrections-revisions`](STAGES.md#stage-03-corrections-revisions) | append-only corrections/revisions/rerun |
| 04 | [`stage-04-storage-jobs-api`](STAGES.md#stage-04-storage-jobs-api) | локальные persistence/jobs/REST |
| 05 | [`stage-05-application-adapters`](STAGES.md#stage-05-application-adapters) | integration packages consumers |
| 06 | [`stage-06-quality-hardening`](STAGES.md#stage-06-quality-hardening) | HTR/mixed routing и укрепление качества |

Интерфейсы и deployment этапа 07 остаются необязательными и после утверждения требуют новой SPEC и prompt.

После каждого этапа: выполнить его gates, получить соответствующий риску review, обновить только фактическую документацию, создать commit и спросить пользователя перед merge. Никогда не запускать следующий этап автоматически.
