# Аудит совместимости контекста

Аудит выполнен 2026-08-13 перед созданием project overlay.

| Возможность | Что уже есть глобально / в workspace | Потребность TRC | Статус | Решение / источник |
|---|---|---|---|---|
| Архитектура и планирование | architect, planner, `plan-stage` | специфичные для OCR контракты | `EXTEND` | общие роли и документы проекта |
| Тестирование и review | test_engineer, reviewer, `review-change` | наборы engine/golden/replay | `EXTEND` | проектный `TEST_STRATEGY.md`; без копии agent |
| Безопасность | security_reviewer и security rules | вредоносные документы и privacy modes | `EXTEND` | проектный `SECURITY.md`; без копии agent |
| Документация и статус | политика workspace docs и контекст SessionStart | один status и plan | конфликт разрешён | `docs/STAGES.md` после безопасной миграции 2026-09-15; без `PROGRESS.md` |
| Путь спецификации | workspace `specs/system.spec.md` | исходником был корневой `SPEC.md` | конфликт разрешён | перемещён в канонический путь; без дубликата |
| Журналы | необязательные workspace templates | явная учебная и техническая ценность | `PROJECT_ONLY` | `docs/LEARNING_LOG.md`, `docs/DEV_LOG.md` |
| Git workflow | правила branches и commits workspace | самостоятельный repository | `INHERITED` | без локальной копии workflow |
| Hooks сессии и разрушительных команд | глобальные hooks, activation не подтверждается одним наличием файлов | дополнительная bootstrap-потребность отсутствует | `INHERITED` | без локальных hooks |
| Hooks schema/golden/privacy | специфичных проектных hooks нет | могут стать enforcement после появления тестов | сейчас `OBSOLETE` | начать с tests/CI; пересмотреть по фактам |
| Целостность supply chain и models | общий security review; project uv.lock и Stage01 supply-chain evidence существуют | hashes, SBOM и manifests артефактов с этапа 01 | `EXTEND` | project tests/CI и `SEC-009`; без hook на bootstrap |
| Skills | глобальные plan/implement/fix/review/explain | позднее повторяемому OCR benchmark может понадобиться процедура | сейчас `INHERITED` | без локального Skill; пересмотреть после повторений |
| Общие subagents | architecture/backend/database/test/security/performance/release | непокрытой роли нет | `INHERITED` | без локальных agents |
| Специалист OCR | общей роли нет | возможный будущий пробел evaluation | сейчас `OBSOLETE` | использовать специалистов и стратегию проекта; пересмотреть после этапа 02 |
| MCP разработки | настроенные инструменты, когда активны | обязательный OCR connector не нужен | `INHERITED`, без зависимости | без локального MCP |
| Product MCP | отсутствует | будущий интерфейс поверх Core | позднее `PROJECT_ONLY` | этап 07; не bootstrap |
| Codex config/rules | workspace/global | тонкие локальные инварианты | `EXTEND` | `AGENTS.md`; без `.codex/config.toml` |

## Решение по бюджету контекста

Сохранить глобальную нагрузку SessionStart без изменений. Маршрутизация по задаче находится в проектном `AGENTS.md`; текущий этап читает один selected record `docs/STAGES.md`, затрагиваемые разделы SPEC, contracts и tests. Не загружать автоматически все decisions, security, roadmap, fixtures или logs.

## Условия повторной оценки

- Переносить проверку benchmark/golden в локальный Skill или hook только после того, как повторное использование покажет стабильную процедуру или пробел enforcement.
- Добавлять проектного agent только тогда, когда ответственность OCR/HTR нельзя покрыть существующими ролями и контекстом репозитория.
- Добавлять product MCP только после появления application use cases и проверок authorization/privacy.

## Brownfield STAGES reconciliation 2026-09-15

`AGENTS.md`, old AI pair, prompt catalog/launcher, architecture/decisions/roadmap/SPEC — MERGE; `docs/STAGES.md` — ADD. Product code/tests/API/data/security/brief and historical DEV_LOG — FORBIDDEN_TO_OVERWRITE. Old bytes/hash/facts preserved in `docs/notes/` and Git parent; no formal DEV bridge opt-in is asserted.
