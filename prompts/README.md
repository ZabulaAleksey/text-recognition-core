# Staged implementation prompts

Каждый файл — самостоятельный ограниченный этап для отдельной Codex session/review/commit. Выполнять по порядку; перед стартом сверить `docs/AI_STATUS.md`, зависимости и решения. Prompt не изменяет требования SPEC.

| Stage | Prompt | Основной результат |
|---|---|---|
| 01 | [`stage-01-foundation.md`](stage-01-foundation.md) | typed domain/application foundation |
| 02 | [`stage-02-engine-pipeline.md`](stage-02-engine-pipeline.md) | safe pipeline + selected OCR adapter |
| 03 | [`stage-03-corrections-revisions.md`](stage-03-corrections-revisions.md) | append-only corrections/revisions/rerun |
| 04 | [`stage-04-storage-jobs-api.md`](stage-04-storage-jobs-api.md) | local persistence/jobs/REST |
| 05 | [`stage-05-application-adapters.md`](stage-05-application-adapters.md) | consumer integration packages |
| 06 | [`stage-06-quality-hardening.md`](stage-06-quality-hardening.md) | HTR/mixed routing and hardening |

Stage 07 interfaces/deployment remain optional and require a new SPEC/prompt when approved.

After each stage: run its gates, obtain review appropriate to risk, update only factual docs, commit, and ask the user before merge. Never auto-run the next stage.
