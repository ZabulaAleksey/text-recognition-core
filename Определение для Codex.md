# Терминология: КАРКАС и АВТОМАТИЗАЦИЯ КОНТЕКСТА

> **Статус после bootstrap:** исходный проектный brief. Его общие определения нормализованы для всех проектов в `~/codex-workspace/docs/PROJECT_FRAMEWORK.md`. Канонические имена и правила context routing задаются workspace-документами; OCR-примеры и TRC-специфика остаются только в этом repository.

В рамках данного проекта слова **КАРКАС** и **АВТОМАТИЗАЦИЯ КОНТЕКСТА** имеют специальные значения.

Codex должен использовать определения из этого раздела во всех последующих задачах проекта.

---

# 1. КАРКАС — определение

**КАРКАС проекта** — это полный проектный пакет, который переводит исходную идею или SPEC в состояние, пригодное для системной поэтапной разработки с помощью Codex и AI Dev Team.

КАРКАС — это **не исходный код приложения** и не просто набор документации.

КАРКАС определяет:

- что строится;
- зачем это строится;
- какие существуют архитектурные границы;
- какие технологии используются;
- какие правила нельзя нарушать;
- как приложение должно эволюционировать;
- на какие этапы разбита разработка;
- что именно Codex должен делать на каждом этапе;
- какие тесты необходимо выполнить;
- когда этап считается завершённым;
- где хранится текущее состояние;
- где фиксируются инженерные решения;
- где фиксируются подробные объяснения;
- какие AI-инструменты и автоматизации доступны проекту;
- как конкретный repository взаимодействует с глобальной AI Dev Team.

Таким образом:

```text
SPEC / IDEA
     ↓
   КАРКАС
     ↓
поэтапная разработка
     ↓
реализация продукта
```

---

# 2. КАРКАС — не отдельная AI-система

КАРКАС конкретного проекта не должен создавать независимую копию AI Dev Team.

Правильная модель:

```text
                    AI Dev Team
                         │
               generic engineering layer
                         │
                         ▼
               Project КАРКАС / Overlay
                         │
                         ▼
                    Repository
                         │
                         ▼
                 Product Source Code
```

AI Dev Team предоставляет глобальные возможности.

КАРКАС предоставляет только:

> специфику конкретного проекта.

---

# 3. Что входит в КАРКАС

Полный КАРКАС должен рассматривать следующие категории.

## 3.1. Specification

Исходные требования и инварианты проекта.

Например:

```text
SPEC.md
```

SPEC отвечает на вопрос:

> Что именно мы строим и какие фундаментальные требования нельзя потерять?

---

# 3.2. Architecture

Архитектура системы.

Например:

```text
docs/ARCHITECTURE.md
```

Она должна описывать:

- модули;
- bounded contexts;
- dependency directions;
- interfaces;
- data flow;
- extension points;
- инфраструктурные границы;
- интеграции;
- ключевые архитектурные ограничения.

---

# 3.3. Data contracts

Контракты данных и API.

Например:

```text
docs/API.md
docs/DATA_MODEL.md
```

---

# 3.4. Engineering decisions

Существенные решения и причины их принятия.

```text
docs/DECISIONS.md
```

Решения не должны существовать только в истории чата или commit message.

---

# 3.5. Design

```text
docs/DESIGN.md
```

Может содержать:

- UI/UX;
- interaction model;
- review workflow;
- пользовательские сценарии;
- визуальные ограничения.

Если UI отсутствует, допускается skeleton до соответствующего этапа.

---

# 3.6. Security model

```text
docs/SECURITY.md
```

Должен определять:

- threat model;
- trust boundaries;
- sensitive data;
- privacy requirements;
- authentication/authorization;
- malicious input handling;
- resource limits;
- dependency security;
- logging policy;
- secrets policy.

---

# 3.7. Testing and Quality Gates

```text
docs/TEST_STRATEGY.md
```

КАРКАС определяет:

- unit tests;
- integration tests;
- contract tests;
- regression tests;
- security tests;
- performance tests;
- benchmarks;
- quality gates.

---

# 3.8. ROADMAP

```text
ROADMAP.md
```

ROADMAP отвечает на вопрос:

> В каком порядке проект должен эволюционировать?

ROADMAP описывает крупные этапы и зависимости.

Он не должен заменять PROMPTS.

---

# 3.9. PROMPTS

PROMPTS являются **исполняемым планом разработки для Codex**.

Например:

```text
prompts/
    README.md
    stage-01-foundation.md
    stage-02-domain-model.md
    stage-03-engine-contract.md
    ...
```

или для небольшого проекта:

```text
PROMPTS.md
```

Каждый этап должен содержать минимум:

```text
Goal

Required context

Dependencies

Scope

Tasks

Files allowed to change

Files that should not change

Tests

Quality gates

Definition of Done

Acceptance Criteria

Expected artifacts

Failure / rollback conditions
```

PROMPT должен быть достаточно самостоятельным, чтобы пользователь мог сказать:

> «Начинай этап 7»

и Codex смог получить нужный контекст из repository без необходимости заново объяснять весь проект в чате.

---

# 3.10. PROGRESS

```text
PROGRESS.md
```

Это единый оперативный статус проекта.

Не создавать параллельно:

```text
AI_STATUS.md
AI_PLAN.md
PROJECT_SNAPSHOT.md
PROGRESS.md
```

с дублирующей информацией.

Использовать один:

```text
PROGRESS.md
```

Он должен содержать:

- текущий этап;
- последний завершённый этап;
- состояние ROADMAP;
- выполненные задачи;
- pending;
- blockers;
- next recommended step;
- важные временные ограничения или проблемы.

---

# 3.11. DEV_LOG

```text
DEV_LOG.md
```

DEV_LOG отвечает на вопрос:

> Что Codex фактически сделал?

Записывать достаточно подробно:

- какие файлы изменены;
- какие компоненты созданы;
- какие проблемы возникли;
- как они решены;
- какие команды выполнялись;
- какие тесты выполнялись;
- какие результаты получены.

DEV_LOG является техническим журналом реализации.

---

# 3.12. LEARNING

```text
LEARNING.md
```

LEARNING отвечает на другой вопрос:

> Почему это сделано именно так и как это работает?

Он должен быть образовательным.

В нём следует подробно объяснять:

- используемые технологии;
- паттерны;
- архитектурные решения;
- альтернативы;
- причины выбора;
- сложные фрагменты реализации;
- ошибки и полученные уроки.

Нельзя заменять LEARNING коротким перечнем изменений.

---

# 3.13. Project Rules / AGENTS

```text
AGENTS.md
```

Project `AGENTS.md` должен быть тонким overlay.

Он должен содержать только правила, специфичные для проекта.

Например, для Text Recognition Core:

```text
raw recognition is immutable

all engines must be behind adapters

application business logic must not enter Core

correction history must remain traceable

private text must not enter telemetry by default
```

Generic engineering rules должны оставаться в AI Dev Team.

---

# 3.14. Hooks

КАРКАС должен определить, нужны ли project-specific hooks.

Примеры:

```text
schema compatibility
golden dataset validation
sensitive fixture detection
benchmark regression
```

Но:

> наличие hooks в понятии КАРКАСА не означает обязательное создание новых hooks.

Сначала необходимо проверить AI Dev Team.

---

# 3.15. Skills

КАРКАС должен определить, нужны ли project-specific Skills.

Например:

```text
OCR benchmark skill
engine adapter verification skill
golden dataset validation skill
```

Но локальный Skill создаётся только если он действительно специфичен для проекта.

---

# 3.16. Subagents

КАРКАС учитывает возможность специализированных subagents.

Но:

```text
architect
tester
security
reviewer
documentation
```

не должны автоматически создаваться локально, если они уже предоставляются AI Dev Team.

---

# 3.17. MCP

КАРКАС должен определить:

- нужен ли MCP;
- когда он нужен;
- какие tools/resources/prompts он предоставляет;
- как MCP обращается к Application/Core.

Наличие MCP в проектировании КАРКАСА не означает, что MCP обязан быть реализован на этапе bootstrap.

Он может появиться на позднем этапе ROADMAP.

---

# 3.18. Context strategy

КАРКАС обязательно включает стратегию управления AI-контекстом.

Необходимо определить:

- какие документы Codex читает всегда;
- какие документы загружаются только по необходимости;
- какой context нужен конкретному stage prompt;
- какие сведения находятся глобально в AI Dev Team;
- какие сведения остаются только в repository.

Цель:

> не заставлять Codex каждый раз загружать весь repository и десятки страниц документации.

---

# 4. Что НЕ является КАРКАСОМ

Следующие вещи по отдельности не являются КАРКАСОМ:

```text
AGENTS.md
```

или:

```text
ARCHITECTURE.md
```

или:

```text
PROMPTS.md
```

или:

```text
набор subagents
```

или:

```text
MCP server
```

или:

```text
ROADMAP
```

КАРКАС — это **согласованная система этих элементов**, причём только тех, которые действительно нужны проекту.

---

# 5. КАРКАС не означает бюрократию

Одной из целей КАРКАСА является уменьшение ручной работы пользователя.

Поэтому действует принцип:

> документ, агент, hook, Skill или процесс не должен существовать только потому, что он присутствует в шаблоне.

Если два документа выполняют одну функцию — предпочтительно объединить их.

Если возможность уже предоставлена AI Dev Team — не дублировать её.

Если файл не помогает:

- разработке;
- Codex;
- тестированию;
- пониманию;
- сопровождению;

его создание должно быть обосновано.

---

# 6. АВТОМАТИЗАЦИЯ КОНТЕКСТА — определение

**АВТОМАТИЗАЦИЯ КОНТЕКСТА** — это процесс и инфраструктурный механизм, благодаря которому Codex автоматически получает необходимый контекст проекта и следует правилам КАРКАСА без необходимости каждый раз вручную пересказывать ему состояние проекта.

Таким образом:

> КАРКАС определяет знания и процессы проекта.

> АВТОМАТИЗАЦИЯ КОНТЕКСТА обеспечивает автоматическую доставку, выбор, обновление и применение этих знаний AI-агентами.

---

# 7. Главное различие

Кратко:

```text
КАРКАС
=
ЧТО Codex должен знать и КАК проект должен разрабатываться
```

```text
АВТОМАТИЗАЦИЯ КОНТЕКСТА
=
КАК нужная часть этих знаний автоматически попадает к Codex
в нужный момент
```

---

# 8. Пример

Допустим, в `ARCHITECTURE.md` написано:

> Recognition engines разрешено подключать только через RecognitionEngine adapter.

Это является частью:

```text
КАРКАСА
```

Если при реализации нового OCR engine Codex автоматически получает соответствующий architecture section и project rule, это уже:

```text
АВТОМАТИЗАЦИЯ КОНТЕКСТА
```

---

# 9. Второй пример

В `PROMPTS/stage-06-revisions.md` определены:

- задача;
- scope;
- tests;
- DoD;
- acceptance criteria.

Это:

```text
КАРКАС
```

Когда пользователь говорит:

> «Начинай этап 6»

и Codex автоматически:

1. открывает stage prompt;
2. загружает релевантный SPEC;
3. получает architecture rules;
4. проверяет DECISIONS;
5. видит текущий PROGRESS;
6. применяет глобальные AI Dev Team rules;

это:

```text
АВТОМАТИЗАЦИЯ КОНТЕКСТА
```

---

# 10. Третий пример — code review

В КАРКАСЕ определено:

```text
all RecognitionEngine implementations must pass engine contract tests
```

АВТОМАТИЗАЦИЯ КОНТЕКСТА должна сделать так, чтобы при изменении:

```text
engines/*
```

Codex или соответствующий workflow автоматически понимал необходимость:

```text
engine contract tests
```

без повторного ручного указания пользователя.

---

# 11. Взаимодействие с AI Dev Team

Полная модель:

```text
                    USER / SPEC
                         │
                         ▼
                       КАРКАС
                         │
             project knowledge + process
                         │
                         ▼
              АВТОМАТИЗАЦИЯ КОНТЕКСТА
                         │
              выбирает нужный контекст
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        AI Dev Team              Project Overlay
      generic capabilities      project-specific rules
             │                       │
             └───────────┬───────────┘
                         ▼
                       Codex
                         │
                         ▼
                     Repository
```

---

# 12. AI Dev Team

AI Dev Team является глобальным инженерным уровнем.

Там должны находиться generic-возможности:

- общие правила разработки;
- Git workflow;
- generic architecture review;
- testing workflow;
- security review;
- documentation workflow;
- generic agents;
- generic Skills;
- общие hooks;
- общие quality gates.

---

# 13. Project КАРКАС

Project КАРКАС добавляет только delta:

```text
GLOBAL
+
PROJECT DELTA
```

Для Text Recognition Core project delta включает, например:

```text
OCR/HTR domain rules
RecognitionEngine contract
Correction model
Revision model
Privacy requirements
Golden OCR datasets
Recognition benchmarks
Application adapters
```

---

# 14. АВТОМАТИЗАЦИЯ КОНТЕКСТА как мост

АВТОМАТИЗАЦИЯ КОНТЕКСТА должна связывать:

```text
AI Dev Team
+
КАРКАС
+
current task
+
repository state
```

и формировать минимально достаточный context.

Концептуально:

```text
Context =
Global rules
+
Project rules
+
Relevant SPEC
+
Relevant architecture
+
Current stage prompt
+
Relevant decisions
+
Current progress
+
Relevant source code
```

Не весь набор должен загружаться для каждой задачи.

---

# 15. Principle of Minimum Sufficient Context

Codex должен использовать:

> минимальный контекст, достаточный для безопасного и корректного выполнения текущей задачи.

Например, маленькая UI-правка не должна автоматически загружать:

```text
полный SECURITY.md
полный ROADMAP
все предыдущие DEV_LOG
весь LEARNING
все PROMPTS
весь repository
```

---

# 16. Context routing

При проектировании АВТОМАТИЗАЦИИ КОНТЕКСТА Codex должен определить правила маршрутизации.

Пример:

```text
изменение RecognitionEngine
    ↓
подтянуть:
    RecognitionEngine contract
    ARCHITECTURE engine section
    API schemas
    relevant DECISIONS
    contract tests
```

---

```text
изменение correction system
    ↓
подтянуть:
    SPEC correction sections
    DATA_MODEL
    revision architecture
    correction tests
```

---

```text
изменение Receipt Adapter
    ↓
подтянуть:
    adapter contract
    INTEGRATIONS receipt section
    relevant RecognitionResult schema
```

---

# 17. Контекст не должен храниться только в чате

Архитектурно важные знания должны попадать в repository.

Плохо:

```text
пользователь однажды объяснил правило ChatGPT
↓
правило существует только в истории чата
```

Правильно:

```text
обсуждение
↓
SPEC / DECISIONS / ARCHITECTURE / AGENTS
↓
repository source of truth
↓
Codex автоматически получает правило
```

---

# 18. Context lifecycle

АВТОМАТИЗАЦИЯ КОНТЕКСТА должна учитывать жизненный цикл информации.

```text
Idea
 ↓
SPEC
 ↓
Architecture / Decision
 ↓
ROADMAP
 ↓
PROMPT
 ↓
Implementation
 ↓
Tests
 ↓
DEV_LOG
 ↓
PROGRESS
 ↓
LEARNING
```

Если в ходе реализации обнаружено новое фундаментальное ограничение, информация должна двигаться обратно:

```text
Implementation discovery
        ↓
DECISION
        ↓
ARCHITECTURE / SPEC update
        ↓
future PROMPTS
```

---

# 19. Context feedback loop

КАРКАС не является статическим архивом.

Он должен обновляться вместе с проектом.

Правильная модель:

```text
КАРКАС
   ↓
Implementation
   ↓
new knowledge
   ↓
КАРКАС update
   ↓
future implementation
```

АВТОМАТИЗАЦИЯ КОНТЕКСТА должна обеспечивать использование уже обновлённой версии знаний.

---

# 20. Merge как контрольная точка

Если разработка ведётся через staged workflow:

```text
PROMPT stage
↓
Codex implementation
↓
tests
↓
review
↓
merge
```

merge завершённого stage является естественной точкой синхронизации КАРКАСА.

После успешного этапа следует при необходимости обновить:

```text
PROGRESS.md
DEV_LOG.md
LEARNING.md
ROADMAP.md
DECISIONS.md
ARCHITECTURE.md
```

но только те файлы, содержание которых действительно изменилось.

---

# 21. КАРКАС и PROMPTS

PROMPTS — важная часть КАРКАСА, но не источник истины выше SPEC и Architecture.

PROMPT отвечает:

> что делать сейчас?

SPEC отвечает:

> что должно быть построено?

ARCHITECTURE отвечает:

> какие границы нельзя нарушать?

DECISIONS отвечает:

> почему мы выбрали именно такой путь?

---

# 22. КАРКАС и исходный код

Исходный код является реализацией КАРКАСА.

Но фактический код также является источником технической истины.

Если документация расходится с реализацией, Codex не должен автоматически считать ни одну сторону правильной.

Он должен определить:

1. реализация устарела относительно архитектуры;
2. документация устарела относительно реализации;
3. произошёл незадокументированный architecture change;
4. существует bug.

Результат должен быть исправлен и при необходимости зафиксирован в `DECISIONS.md`.

---

# 23. КАРКАС и Git

КАРКАС должен быть version-controlled вместе с проектом.

Изменения архитектуры, SPEC, PROMPTS и правил должны проходить через Git так же, как код.

Это позволяет связать:

```text
code version
+
architecture version
+
prompt version
+
project state
```

---

# 24. АВТОМАТИЗАЦИЯ КОНТЕКСТА и Git

Git может использоваться как источник событий для обновления состояния.

Например:

```text
stage merged
    ↓
PROGRESS update
    ↓
next stage becomes active
```

При наличии соответствующей инфраструктуры состояние repository может использоваться для определения:

- текущего этапа;
- последних изменений;
- необходимости обновить документацию;
- quality gates.

---

# 25. КАРКАС и hooks

Hook является не КАРКАСОМ целиком, а механизмом исполнения отдельных правил КАРКАСА.

Например:

КАРКАС говорит:

```text
private OCR fixtures must never enter public repository
```

Project-specific hook может проверять это автоматически.

Следовательно:

```text
rule
=
КАРКАС
```

```text
automatic enforcement
=
АВТОМАТИЗАЦИЯ КОНТЕКСТА / workflow automation
```

---

# 26. КАРКАС и Skills

Skill содержит повторяемую специализированную процедуру.

Например:

```text
run OCR golden benchmark
```

Само требование benchmark является частью КАРКАСА.

Skill позволяет Codex выполнять процедуру одинаково и без повторного большого prompt.

То есть Skill является одним из инструментов АВТОМАТИЗАЦИИ КОНТЕКСТА.

---

# 27. КАРКАС и subagents

КАРКАС определяет, какие роли необходимы проекту.

АВТОМАТИЗАЦИЯ КОНТЕКСТА может маршрутизировать задачу соответствующему agent/subagent.

Но запрещено создавать subagent только ради существования ещё одного subagent.

---

# 28. КАРКАС и MCP

MCP выполняет две разные потенциальные функции.

## Development MCP

Помогает Codex получать данные или использовать внешние инструменты во время разработки.

## Product MCP

Позволяет AI-клиентам пользоваться уже самим Text Recognition Core.

Например:

```text
recognize_document
get_uncertain_regions
apply_correction
```

Оба варианта должны быть архитектурно разделены.

---

# 29. АВТОМАТИЗАЦИЯ КОНТЕКСТА не равна MCP

MCP — только один из возможных механизмов.

АВТОМАТИЗАЦИЯ КОНТЕКСТА может использовать комбинацию:

```text
AGENTS
Rules
Skills
Hooks
Subagents
PROMPTS
Repository docs
Git state
MCP
scripts
tests
CI
```

---

# 30. АВТОМАТИЗАЦИЯ КОНТЕКСТА не равна AGENTS.md

`AGENTS.md` является лишь одной точкой входа.

Он должен помогать Codex определить:

- где находится источник истины;
- какие проектные правила обязательны;
- какие документы читать для конкретной задачи.

Он не должен превращаться в копию всей SPEC.

---

# 31. Желаемое взаимодействие пользователя с системой

После создания качественного КАРКАСА и АВТОМАТИЗАЦИИ КОНТЕКСТА пользователь должен иметь возможность работать короткими командами.

Например:

```text
Создай КАРКАС по этой SPEC.
```

---

```text
Начинай этап 4.
```

---

```text
Проверь этап 4.
```

---

```text
Этап пройден, обнови состояние проекта.
```

---

```text
Добавь это решение в архитектуру.
```

---

```text
Эта идея относится к Receipt Adapter — зафиксируй её.
```

Codex должен самостоятельно определить соответствующие project documents и обновить их без требования от пользователя перечислять файлы вручную.

---

# 32. Требование к созданию КАРКАСА

Когда пользователь говорит:

```text
создай КАРКАС
```

Codex должен интерпретировать это как:

> провести проектирование полного project-specific development overlay вокруг данной SPEC с учётом существующей AI Dev Team и подготовить repository к системной staged development.

Это НЕ означает:

> немедленно написать всё приложение.

---

# 33. Требование к АВТОМАТИЗАЦИИ КОНТЕКСТА

Когда пользователь говорит:

```text
сделай АВТОМАТИЗАЦИЮ КОНТЕКСТА
```

Codex должен:

1. определить существующий КАРКАС;
2. определить существующие возможности AI Dev Team;
3. определить источники project context;
4. минимизировать дублирование;
5. настроить механизмы автоматического получения нужного контекста;
6. определить routing context по типам задач;
7. добавить project-specific rules/hooks/skills/subagents/MCP только при необходимости;
8. обеспечить обновление project state после этапов;
9. проверить context budget;
10. задокументировать получившуюся систему.

---

# 34. Если КАРКАС ещё отсутствует

Если пользователь просит:

```text
АВТОМАТИЗАЦИЯ КОНТЕКСТА
```

для проекта, у которого ещё отсутствует нормальный КАРКАС, Codex должен сначала определить недостающие элементы.

Он не должен автоматизировать хаотичный набор файлов.

Правильный порядок:

```text
SPEC
 ↓
КАРКАС
 ↓
АВТОМАТИЗАЦИЯ КОНТЕКСТА
 ↓
Development
```

При этом создание КАРКАСА и настройка АВТОМАТИЗАЦИИ КОНТЕКСТА могут выполняться одним bootstrap-этапом.

---

# 35. Если КАРКАС уже существует

Не генерировать его заново.

Codex должен:

```text
inspect
↓
gap analysis
↓
update only missing/outdated parts
```

То есть КАРКАС является living system, а не одноразовым шаблоном.

---

# 36. Главное правило против дублирования

Перед созданием любого из следующих элементов:

```text
AGENTS rule
Skill
Hook
Subagent
MCP integration
Git workflow
Quality gate
Documentation workflow
```

Codex обязан проверить:

> существует ли уже соответствующая generic возможность в AI Dev Team?

Если существует — использовать её.

Локально хранить только project-specific delta.

---

# 37. Приоритет локальной специфики

AI Dev Team является глобальным инженерным фундаментом.

Но глобальный слой не должен случайно отменять осознанные domain-specific ограничения проекта.

Например, для TRC:

```text
RAW recognition must be immutable
```

является фундаментальным проектным invariant.

Если generic подход предполагает mutable update, проектное правило должно быть явно учтено.

При реальном конфликте правил Codex не должен молча выбирать вариант.

Нужно:

1. определить конфликт;
2. применить установленную hierarchy;
3. при архитектурной неоднозначности зафиксировать решение.

---

# 38. Source-of-truth model

Рекомендуемая hierarchy:

```text
Global AI Dev Team rules
        +
Project SPEC
        ↓
Project DECISIONS
        ↓
ARCHITECTURE / DATA_MODEL / API
        ↓
ROADMAP
        ↓
Current PROMPT
        ↓
PROGRESS
        ↓
Implementation
```

При этом global rules задают инженерные нормы, а SPEC задаёт доменные требования проекта.

Ни один stage prompt не имеет права сознательно нарушать SPEC без явного architecture decision.

---

# 39. КАРКАС как контракт между пользователем и Codex

КАРКАС должен позволять пользователю не держать весь проект в голове.

Пользователь определяет:

```text
цели
решения
приоритеты
review/merge
```

Codex берёт на себя:

```text
контекст
документацию
этапность
проверки
синхронизацию файлов
техническое выполнение
```

---

# 40. Конечная цель

КАРКАС + АВТОМАТИЗАЦИЯ КОНТЕКСТА должны привести проект к состоянию:

```text
User intent
     ↓
small command
     ↓
automatic context selection
     ↓
Codex execution
     ↓
tests / review
     ↓
merge
     ↓
automatic project-state synchronization
     ↓
next stage
```

При этом пользователь не должен каждый раз вручную объяснять Codex:

- архитектуру;
- предыдущие решения;
- текущий этап;
- требования к тестам;
- где находится следующий prompt;
- какие generic agents использовать;
- какие project rules нельзя нарушать.

---

# 41. Определение одной строкой

Для использования Codex:

> **КАРКАС** — это полный living project-development contract: SPEC, архитектура, правила, staged PROMPTS, DoD, tests, quality gates, project state, engineering logs и необходимые project-specific AI-инструменты.

> **АВТОМАТИЗАЦИЯ КОНТЕКСТА** — это система, которая связывает этот КАРКАС с AI Dev Team и автоматически доставляет Codex минимально необходимый актуальный контекст для конкретной задачи.

Формула:

```text
AI Dev Team
+
КАРКАС проекта
+
АВТОМАТИЗАЦИЯ КОНТЕКСТА
=
управляемая AI-assisted разработка
```
