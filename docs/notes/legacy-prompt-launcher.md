# Historical launcher index

Исторический snapshot прежнего `prompts/README.md` на `d6344b4c7ca3a1001d7137a935d91c8e18f1bce6`; это не execution-state owner и не launcher. Текущий selected record, plan/status/evidence/NEXT находятся только в `docs/STAGES.md`.

Source UTF-8/LF bytes SHA-256: `e52b97e9310b8f5f29f1c8d78b777320bc0be076967e7834d24ffb6ac1a6115c`. Previous archived bytes retained in reachable remote parent `c6f6b39573fef8f2c0e6149a67e407afb263059c`, SHA-256 `4ed993002e6bb6ab6607bfde65b55ee606602894a3743cd97ffb49048762c940`; исходный повреждённый catalog этим не удалён из истории.

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

<!-- End of historical snapshot. -->
