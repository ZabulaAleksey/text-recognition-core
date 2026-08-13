# Context compatibility audit

Аудит выполнен 2026-08-13 перед созданием project overlay.

| Возможность | Что уже есть глобально / workspace | Потребность TRC | Статус | Решение / источник |
|---|---|---|---|---|
| Architecture/planning | architect, planner, `plan-stage` | OCR-specific contracts | `EXTEND` | generic roles + project docs |
| Testing/review | test_engineer, reviewer, `review-change` | engine/golden/replay suites | `EXTEND` | project `TEST_STRATEGY.md`; no agent copy |
| Security | security_reviewer, security rules | hostile documents/privacy modes | `EXTEND` | project `SECURITY.md`; no agent copy |
| Documentation/status | workspace docs policy and SessionStart context | one status/plan | `CONFLICT` resolved | `docs/AI_STATUS.md` + `docs/AI_PLAN.md`; no `PROGRESS.md` |
| Specification path | workspace `specs/system.spec.md` | source was root `SPEC.md` | `CONFLICT` resolved | moved to canonical path; no duplicate |
| Logs | optional workspace templates | explicit educational/technical value | `PROJECT_ONLY` | `docs/LEARNING_LOG.md`, `docs/DEV_LOG.md` |
| Git workflow | workspace branch/commit rules | standalone repository | `INHERITED` | no local workflow copy |
| Session/destructive hooks | active global hooks | no additional bootstrap need | `INHERITED` | no local hooks |
| Schema/golden/privacy hooks | none project-specific | may become enforcement after tests exist | `OBSOLETE` now | begin as tests/CI; reconsider with evidence |
| Supply-chain/model integrity | generic security review; no project lock yet | hashes/SBOM/artifact manifests from Stage 01 | `EXTEND` | project tests/CI and `SEC-009`; no hook at bootstrap |
| Skills | global plan/implement/fix/review/explain | repeated OCR benchmark may need procedure later | `INHERITED` now | no local Skill; reassess after repeated workflow |
| Generic subagents | architecture/backend/database/test/security/performance/release | no uncovered role | `INHERITED` | no local agents |
| OCR specialist | none generic | possible future evaluation gap | `OBSOLETE` now | use specialists + project strategy; reassess after Stage 02 |
| Development MCP | configured tools when active | no mandatory OCR dev connector | `INHERITED`/not relied on | no local MCP |
| Product MCP | none | future interface over Core | `PROJECT_ONLY` later | Stage 07; not bootstrap |
| Codex config/rules | workspace/global | thin local invariants | `EXTEND` | `AGENTS.md`; no `.codex/config.toml` |

## Context budget decision

Keep the global SessionStart payload unchanged. Task-specific routing lives in project `AGENTS.md`; current stage reads one prompt, affected SPEC sections/contracts/tests and compact status. Do not auto-load all decisions, security, roadmap, fixtures or logs.

## Re-evaluation triggers

- Promote benchmark/golden validation to a local Skill or hook only after repeat use shows a stable procedure or an enforcement gap.
- Add project agent only when an OCR/HTR responsibility cannot be covered by existing roles plus repository context.
- Add product MCP only after application use cases and authorization/privacy gates exist.
