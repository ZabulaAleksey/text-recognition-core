# Журнал разработки

## 2026-08-13 — Bootstrap КАРКАСА

- Прочитаны `Определение для Codex.md`, полная исходная `SPEC.md`, правила маршрутизации, SDD и доменов workspace и активные возможности AI Dev Team.
- Выполнены read-only аудиты архитектуры и глобального overlay.
- Проверено, что GitHub-репозиторий `ZabulaAleksey/text-recognition-core` существует, пуст, использует `main` и предоставляет разрешения push/admin.
- Инициализирован самостоятельный Git-репозиторий, создана ветка `docs/project-skeleton` и настроен `origin`.
- Каноническая спецификация перемещена в `specs/system.spec.md`, добавлены стабильные IDs требований и приёмки и созданы документы КАРКАСА проекта.
- Разрешены конфликты workspace: `AI_STATUS` вместо `PROGRESS`, отдельный от библиотеки prompts `AI_PLAN`, канонические пути документов и отсутствие дубликатов AI-инфраструктуры.
- Выбрана основа Python с contract-first подходом; выбор OCR/HTR и binary decoder отложен до evidence gates.
- Product source code не создавался; push и merge не выполнялись.

### Существенная проблема

Git первоначально отклонил новый вложенный repository из-за различия владельцев каталогов sandbox и Windows. Последующие локальные команды используют специфичный для repository параметр `safe.directory`; глобальная настройка Git не изменялась.

### Выполненные проверки

- все относительные Markdown links разрешаются;
- каждый из шести stage prompts содержит все 13 обязательных разделов;
- существует только один кандидат status/source (`docs/AI_STATUS.md`); устаревших канонических блоков layout нет;
- registry требований содержит 37 стабильных IDs;
- независимый reviewer вернул `PASS` после исправлений allowlist dependencies, канонических имён, API batch/rerun/rollback/correction/revision и процесса пустого repository;
- независимый security reviewer вернул `PASS` после явной фиксации изоляции, amplification, local identity, actor/consent, supply chain, retention/deletion, cache/idempotency и SSRF gates;
- product `src/`, dependencies, runtime и приватные fixtures не создавались.
