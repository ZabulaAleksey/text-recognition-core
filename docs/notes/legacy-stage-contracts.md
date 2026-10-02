# Historical readable stage catalog

Исторический snapshot прежнего `prompts/STAGES.md` на `d6344b4c7ca3a1001d7137a935d91c8e18f1bce6`; это не execution-state owner и не launcher. Текущий selected record, plan/status/evidence/NEXT находятся только в `docs/STAGES.md`.

Source UTF-8/LF bytes SHA-256: `911e735981dabb8083316ec399a45c2e1a09bfd9a6754a76b0c8e2e06a749a8a`. Previous archived bytes retained in reachable remote parent `c6f6b39573fef8f2c0e6149a67e407afb263059c`, SHA-256 `5fbf50bfec9610dd7e8be14357d839ebbc3b6c543b38448c0793c4164beffb5d`; исходный повреждённый catalog этим не удалён из истории.

# Канонические этапы text-recognition-core  Единый источник stage-prompts. Ниже сохранено полное содержание ранее существовавших этапов.

## stage-01-foundation
# Этап 01 — Фундамент и типизированные контракты

## Цель

Создать фундамент Python-библиотеки и неизменяемые типизированные контракты Core без продуктовых интеграций.

## Обязательный контекст

`AGENTS.md`; разделы SPEC 7–16, 40, 56–58 и IDs `FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `AC-001`; `docs/ARCHITECTURE.md`, `API.md`, `DATA_MODEL.md`, ADR-002–005; текущие `AI_STATUS` и `AI_PLAN`.

## Зависимости

Принятый КАРКАС и поддерживаемая среда Python 3.13. Предыдущих этапов кода нет.

## Область

Упаковка, domain values/entities, application ports, граница schema, ports детерминированных IDs и clock, in-memory test doubles и фундаментальные тесты.

## Задачи

1. Создать `pyproject.toml` и границы пакета `src/`, соответствующие архитектуре.
2. Реализовать строгие неизменяемые value types для IDs, coordinates, confidence, modes/capabilities/privacy, errors и provenance.
3. Реализовать типизированные контракты request/result и Document/Page/Region/Line/Token; разделить IDs raw и current revision.
4. Определить независимые от фреймворка ports engine/storage/job/cancellation без конкретных adapters.
5. Генерировать JSON Schema из одного источника boundary models и добавить fixture версии и совместимости.
6. Добавить тесты границ architecture/import и domain invariants.
7. Создать набор dependencies с закреплёнными hashes, политику доверенных indexes и первоначальные проверки SBOM/license/vulnerability/unsafe deserialization.

## Файлы, которые разрешено изменять

Файлы упаковки; `src/text_recognition_core/domain/**`, `application/**`, `schemas/**`; `tests/unit/**`, `tests/contracts/schema/**`; фактические документы status/decision/log.

## Файлы, которые не должны изменяться

Поведение SPEC; реализация engine/storage/REST/application adapters; golden/private fixtures; глобальная конфигурация workspace.

## Тесты

Строгие допустимые и недопустимые случаи schema, включая одиночные и batch requests и обе batch policies, границы глубины и cardinality JSON, body и response, вложенную иерархию, границы coordinates, конечный confidence, правила reading order и IDs, serialization errors, snapshot сгенерированной schema, запрещённые imports infrastructure, lock drift и запрещённую исполняемую или объектную serialization.

## Контроль качества

Проходят formatter, linter, type checker и test suite; в domain/application отсутствуют imports framework/OCR/database; public contracts трассируются к IDs требований текущей области; с первого устанавливаемого пакета существуют подтверждения hashes dependencies, SBOM, licenses и vulnerabilities.

## Определение готовности

Пакет устанавливается локально, contracts могут валидировать и сериализовать репрезентативные примеры, генерация schema детерминирована, а все ports не имеют реализации infrastructure.

## Критерии приёмки

`AC-001`, `AC-010`; архитектурное `NFR-002`; явные версии API/schema и разделение raw/current IDs.

## Ожидаемые артефакты

Каркас пакета Python, fixtures сгенерированных schemas, tests, обновлённые по фактам status/log и необходимые уточнения ADR.

## Условия остановки и отката

Остановиться, если contracts требуют изменить семантику SPEC, если один источник models не может генерировать schemas или если domain требует import фреймворка. Отменить commit этапа; миграции и внешнее состояние запрещены.


## stage-02-engine-pipeline

- `TRC-NIGHT-JSON-DUPLICATE-01` — VERIFIED LOCALLY / INTEGRATION_PENDING. Public request/result byte parsers reject duplicate decoded JSON keys at every nesting level before unchanged Pydantic JSON validation; duplicate privacy policy values cannot select the later value. Twelve new regressions PASS; full75 PASS, Ruff check/format55 files and strict mypy11 source files PASS. Existing tests/schemas/dependencies unchanged. Validation used existing locked `--no-sync` environment Python3.13.7 with its retained3.13.6 marker warning; no fresh restore claimed. SPEC: `specs/features/json-boundary-validation.spec.md`. Stage02 remains PARTIAL; this does not activate engine/transport or prove egress isolation. Remote canonical documentation convergence is required before publication.

- Night restore checkpoint 2026-10-01: PARTIAL remains; locked editable-build gap fixed via editables~=0.3 (0.6). Fresh separate-environment offline two-step restore/import PASS; 56 tests/Ruff/strict mypy/lock/wheel/sdist PASS, uv audit 20 packages zero known. Evidence: docs/notes/night-reproducibility-2026-10-01.md. NEXT remains isolated decoder contract and representative OCR benchmark, no native parser activation.
- 2026-10-02 bounded diagnostic repair: `tools/printed_golden_smoke.py` enforces a joint 16 KiB stdout+stderr cap while reading, strictly decodes bounded UTF-8, sanitizes process-start/output errors, and kills/reaps only its exact direct child on overflow, timeout, or read failure. Seven new regressions cover simultaneous flood, joint accounting, exact cap, invalid UTF-8, sanitized start failure, timeout/reap, and read failure/reap. Full suite 63 PASS; Ruff check/format and strict mypy PASS; actual synthetic Tesseract rerun CER/WER 0 for EN/RU/UA. Evidence: `docs/evidence/stage02-printed-smoke.md`. The smoke remains developer-only and does not claim descendant containment, worker isolation, representative quality, or engine selection. NEXT remains ADR-P01 isolated decoder/security decision, then representative benchmark and ADR-P02; Stage 02 PARTIAL.
Stage 02 current outcome (2026-09-30): PARTIAL. Pure immutable engine routing planner,
privacy/capability fail-closed behavior and region planning verified locally; see
`specs/features/engine-routing.spec.md` and `docs/AI_STATUS.md`. Binary intake,
isolated workers, representative golden benchmark and baseline OCR adapter remain open. This
bounded slice does not satisfy the complete Stage 02 acceptance contract.
A pre-decoder bounded source-byte envelope now hashes and recognizes only leading
PNG/JPEG/PDF signatures; binary decoding and worker isolation remain open.
Synthetic printed golden smoke now covers eng/rus/ukr with fixed SHA-256 images and a bounded executable fingerprint,
manifest integrity and tamper/path-negative tests. Installed Tesseract 5.5.3
scores CER/WER 0 only on these three easy images; see
`specs/features/printed-golden-smoke.spec.md` and
`docs/evidence/stage02-printed-smoke.md`. This does not select an OCR engine,
establish representative thresholds or activate native parsing.

# Этап 02 — Intake, pipeline и базовый OCR

## Цель

Реализовать безопасную orchestration распознавания и выбрать один локальный OCR adapter на основании воспроизводимых подтверждений.

## Обязательный контекст

Разделы SPEC 23–29, 42–50, 59, 62 и `FR-003`, `NFR-001`, `NFR-003`, `PERF-001`, `AC-002`, `AC-005`; потоки engine/intake архитектуры; port engine из API; правила security для входа и ресурсов; стратегия тестирования; ADR-007/P01/P02.

## Зависимости

Принят этап 01. Подготовлены разрешённый синтетический или анонимизированный печатный golden slice и среда оценки.

## Область

Безопасный intake изображений, сменяемые этапы preprocessing/layout, registry, выбор и fallback engines, fake engine, benchmark кандидатов и ровно один базовый локальный OCR adapter.

## Задачи

1. Исследовать и выбрать библиотеки decoder PDF/image с подтверждениями license/security/resources; ADR-P01 не принимается без описанной ниже изоляции.
2. Реализовать декодирование binary, parsing metadata и inference OCR/model в одноразовых subprocess workers с минимальными правами или эквивалентном sandbox: без сети, с непривилегированной identity, минимальным read-only source, приватным per-job temp root, OS limits CPU/RSS/files/processes, жёстким timeout/kill и очисткой после crash/cancel.
3. Реализовать validation, hashing, производные preprocessing artifacts и обратимые coordinate transforms.
4. Реализовать registry, selection capabilities, правила fallback и budgets cancellation/resources, включая quotas output/artifacts/disk.
5. Создать общий contract suite engines и fake adapter.
6. Проверять подписанные или digest-verified manifests model/engine и отклонять unsafe serialization до загрузки.
7. Выполнить benchmark локальных OCR-кандидатов на версионированных golden data; сохранить отчёт quality/resources и принять ADR-P02.
8. Интегрировать только выбранный adapter и нормализовать errors/confidence/provenance.

## Файлы, которые разрешено изменять

`pyproject.toml`, lock dependencies и артефакты SBOM/license; `src/**/intake/**`, `pipelines/**`, `engines/**`, относящаяся application orchestration; разрешённые `tests/fixtures/**`, contract/integration/benchmark/security tests; ADR/status/log.

## Файлы, которые не должны изменяться

Реализация corrections/revisions, REST и persistent jobs, business models consumers, remote/cloud engines и private fixtures.

## Тесты

Contract suite engines, упорядоченные multi-source success/failure при обеих batch policies, повреждённый или превышающий limits input/output, coordinate transforms, обязательные и необязательные capabilities, fallback, детерминированный fake pipeline, worker crash/hang/hard-kill/cancel/cleanup/private-root/no-egress, подменённый artifact и unsafe serialization, golden CER/WER/layout и отчёт latency/memory/disk.

## Контроль качества

`AC-002`, `AC-005`, `AC-007`, `AC-010`; scan vulnerability/license/provenance dependencies и проверка lock; security review decoders/adapters и isolation worker; evidence benchmark указывает dataset и versions; нет неподтверждённых заявлений о точности; включён ровно один production baseline OCR adapter.

## Определение готовности

Поддерживаемый печатный input offline проходит через ports и создаёт корректный неизменяемый raw result, а решение о выбранном engine воспроизводимо.

## Критерии приёмки

Замена engine требует только нового adapter; raw result содержит полный provenance; недопустимый input завершается безопасно; необязательные capabilities создают предупреждение, а обязательные завершаются явной ошибкой.

## Ожидаемые артефакты

Код pipeline и adapter, golden manifest/report, принятые ADR decoder/engine и contract/security tests.

## Условия остановки и отката

Остановиться, если ни один кандидат не достигает согласованного минимума, licenses несовместимы, decoding нельзя изолировать или ограничить, integrity артефактов нельзя проверить либо обнаружены private data. Удалить adapter и artifacts и сохранить fake contract baseline; не ослаблять gates молча.


## stage-03-corrections-revisions
# Этап 03 — Corrections, revisions и частичный повторный запуск

## Цель

Реализовать append-only пользовательские исправления и детерминированное поведение revisions без изменения доказательств распознавания.

## Обязательный контекст

Разделы SPEC 17–23, 55–57 и `FR-004`–`FR-006`, `AC-003`; поток corrections в архитектуре; `CorrectionRequest` из API; инварианты identity/revision модели данных; ADR-005.

## Зависимости

Приняты этапы 01–02; доступны raw snapshots и ports распознавания regions.

## Область

Операции corrections, validation target, оптимистичные линейные revisions, replay/current view/diff/rollback, ancestry split/merge и orchestration повторного распознавания scope сначала с in-memory repositories.

## Задачи

1. Реализовать типизированные операции corrections и validation before/base.
2. Атомарно добавлять revisions через port unit-of-work; отклонять устаревшие bases.
3. Реализовать детерминированные replay, current projection, структурный и текстовый diff и rollback как новую revision.
4. Сохранять или создавать IDs для replace/split/merge и поддерживать ancestry.
5. При partial rerun добавлять raw evidence и revision без перезаписи предыдущих results.
6. Получать actor/tenant/source из доверенного execution context route/service; публичные corrections всегда имеют `USER`, подмена source role и cross-document target отклоняется, заявленная import attribution остаётся недоверенной.
7. Добавить отдельные от corrections неизменяемые grants и revocations consent, версионированные по purpose/scope/policy; export повторно авторизуется при выполнении.

## Файлы, которые разрешено изменять

Domain/application modules corrections/revisions, in-memory repositories, относящиеся schemas и unit/property/integration tests; фактическая документация.

## Файлы, которые не должны изменяться

Vendor adapter engine, если не доказан дефект контракта; persistent DB/REST; application projectors; семантика обновления raw snapshot.

## Тесты

Все операции corrections, детерминированность replay, сохранение raw hash, устаревшая и конкурентная base, rollback, diff, ancestry split/merge, partial rerun, подмена actor/source role/cross-document target и отсутствующий, поддельный, устаревший или отозванный consent.

## Контроль качества

`AC-003`; property/replay/concurrency tests; reviewer подтверждает отсутствие пути изменения raw evidence и targets, основанных только на offsets.

## Определение готовности

Пользователь может исправить или подтвердить token или line, просмотреть revisions и diff, выполнить rollback и повторно распознать scope, при этом все предыдущие raw/revisions остаются доступными, а provenance actor/consent — доверенным и пригодным для аудита.

## Критерии приёмки

Raw hash не изменяется; hash replay стабилен; устаревшая base сообщается явно; новые структурные IDs связаны с ancestry; использование для training/export требует действующий отзываемый grant и остаётся opt-in.

## Ожидаемые артефакты

Services и schemas corrections/revisions, in-memory implementation, replay/property tests и обновлённые status/log.

## Условия остановки и отката

Остановиться при недетерминированном replay, неоднозначной target identity, потерянном конкурентном обновлении или любой перезаписи raw. Отменить commit этапа; persistent migration ещё не существует.


## stage-04-storage-jobs-api
# Этап 04 — Локальное persistence, jobs и REST API

## Цель

Сделать завершённые use cases Core долговечными и асинхронно доступными в local/offline deployment profile.

## Обязательный контекст

Разделы SPEC 37–59 и `FR-007`, `FR-009`, `SEC-002`, `SEC-003`, `SEC-005`; storage/jobs архитектуры; endpoints, errors и idempotency API; инварианты данных; security model; ADR-006/009.

## Зависимости

Приняты этапы 01–03 и стабильные schemas. До любой постоянной записи пользовательских данных необходимо принять ADR-P03, определяющий local retention, permissions/encryption, SLA удаления, очистку temp/crash и поведение logs/audit/rotation/export/backups.

## Область

Metadata SQLite, атомарные blobs файловой системы, unit-of-work, migrations и recovery, постоянный local worker, idempotency/progress/cancel/cache и REST adapter FastAPI. Без remote/multi-tenant profile.

## Задачи

1. Принять ADR-P03, затем определить обратимые schema migrations и adapters repository/blob/cache с правилами retention/deletion/reference count.
2. Реализовать долговечный state machine jobs, attempts, checkpoints cancellation и учёт ресурсов.
3. Реализовать двухуровневую idempotency identity `(tenant, principal, operation, key) → request hash/result`; другой hash вызывает conflict без создания второго job. Отдельно реализовать scoped recognition cache и повторно авторизовать каждый lookup.
4. Добавить handlers REST v1 как тонкие application adapters с безопасными errors и pagination; выполнять bind только на loopback/local IPC, создавать credential высокой энтропии через приватный permission-checked file или OS store, но не CLI или loggable env, проверять за постоянное время, поддерживать rotate/revoke, завершать запуск закрытым отказом при небезопасном storage, запрещать CORS/cookies и отказывать в non-loopback без remote gate.
5. В `LOCAL_ONLY` запрещать весь egress, включая telemetry, fallback и update checks.
6. Применять quotas request/output/disk/queue/cardinality и принятый lifecycle retention/deletion/backup/observability; проверить crash consistency и удаление shared blobs.

## Файлы, которые разрешено изменять

Infrastructure adapters/migrations, jobs, REST interface, deployment/test config, integration/security/API compatibility tests и относящиеся документы.

## Файлы, которые не должны изменяться

Семантика domain без обновления ADR/SPEC; remote auth и multi-tenant deployment; CLI/MCP; projectors consumers.

## Тесты

Migration up/down/recovery, транзакции и удаление atomic/shared blobs и `AC-011`, переходы jobs, retry/cancel, idempotency одинакового key с одинаковым и различным hash с доказательством отсутствия duplicate job, collisions отдельно scoped cache и invalidation удалённого document, REST schema/errors/pagination, permissions/bootstrap/rotation/revocation/redaction token-file, отказ wildcard bind, missing/wrong credentials и hostile Origin, amplification request/output/disk/queue, no-egress, rotation/access/retention log/audit и leakage telemetry.

## Контроль качества

`AC-008`, `AC-009`, `AC-011`; security review; проходят integration/compatibility tests; ADR-P03 принят до постоянных записей; injection failure не оставляет видимого dangling state; авторизованное удаление соблюдает SLA для всех retention classes; нет утечек stack/path/content; non-loopback startup запрещён без remote gate.

## Определение готовности

Локальный client может через REST отправить, отслеживать, отменить и получить persistent result распознавания или correction с состоянием, переживающим restart, и принудительно применяемой offline privacy.

## Критерии приёмки

`FR-007`, `FR-009`, `AC-004`, `AC-011`; семантика duplicate key и terminal states соответствует API; retention classes source/raw/revision остаются разделёнными; авторизованное удаление полно, а preprocessing/corrections не могут его инициировать.

## Ожидаемые артефакты

Migrations, local adapters/worker, REST v1/OpenAPI, recovery/security tests, operating notes и обновления status/log.

## Условия остановки и отката

Остановиться при необратимой migration, видимых после crash частичных writes, неограниченном worker, privacy egress или небезопасном external bind. Восстановить backup DB до этапа и отменить code/migration; не включать remote mode.


## stage-05-application-adapters
# Этап 05 — Adapters приложений

## Цель

Подключить трёх первоначальных consumers через отдельные input profiles и output projectors с полным provenance и без утечки домена Core.

## Обязательный контекст

Разделы SPEC 24, 33–36, 67, 82–83 и `FR-008`, `AC-006`; `docs/INTEGRATIONS.md`, контракты result/data и стратегия integration tests; ADR-008.

## Зависимости

Стабильный API recognition/revision из этапов 01–04.

## Область

Integration packages/contracts и синтетические fixtures adapters для Personal Chronicle, Receipt Scanner и Tutor. Изменения приложений-consumers требуют отдельных задач в их репозиториях.

## Задачи

1. Реализовать общий контракт profile/projector и validation version/provenance.
2. Реализовать проекцию Chronicle без логики RAG/timeline/summary.
3. Реализовать проекцию extraction чеков со ссылками amount/item/source и явной неоднозначностью.
4. Реализовать проекцию regions Tutor без логики student/grading/solution.
5. Добавить проверки dependencies, запрещающие entities/services consumers внутри Core.
6. Опубликовать пример подключения четвёртого consumer через существующие contracts.

## Файлы, которые разрешено изменять

Integration packages, принадлежащие им schemas, синтетические fixtures, adapter/contract tests и документация интеграций.

## Файлы, которые не должны изменяться

Vocabulary домена Core, семантика OCR pipeline и corrections, репозитории consumers, приватные пользовательские данные и неподдерживаемые math/business features.

## Тесты

Детерминированные projections, покрытие provenance, поля low-confidence/missing/ambiguous, privacy profiles, schema versioning и проверки запрещённых dependencies/imports.

## Контроль качества

`AC-006`; 100% заполненных производных полей имеют действующие source references или явный derived provenance; в integrations отсутствует прямой OCR SDK; в Core отсутствуют business services consumers.

## Определение готовности

Все три projections принимают один стабильный result, а пример нового consumer добавляется без изменения contracts Core.

## Критерии приёмки

Суммы чека трассируются к tokens/regions, Chronicle поддерживает `LOCAL_ONLY`, Tutor явно деградирует неподдерживаемую необязательную capability, а mapping adapter никогда не перезаписывает raw text.

## Ожидаемые артефакты

Три версионированных integration packages/contracts, синтетические fixtures/tests, документация onboarding и обновление status/log.

## Условия остановки и отката

Остановиться, если projection требует business logic consumer внутри Core или неверсионированного изменения public contract. Отменить только затронутый integration package; Core остаётся пригодным для использования.


## stage-06-quality-hardening
# Этап 06 — HTR, mixed routing и укрепление качества

## Цель

Добавить основанное на подтверждениях распознавание handwriting/mixed и завершить privacy, security, regression и performance gates для review MVP Core.

## Обязательный контекст

Разделы SPEC 29–32, 41–50, 59–66 и `NFR-001`, `NFR-003`–`NFR-005`, `SEC-001`–`SEC-010`, `PERF-001`, `AC-004`–`AC-011`; стратегия security/testing; ожидающие ADR-P04–P05. ADR-P03 должен быть уже принят на этапе 04.

## Зависимости

Приняты этапы 01–05; существует репрезентативный разрешённый golden dataset handwriting/mixed.

## Область

Benchmark и выбор HTR-кандидатов, routing OCR/HTR на уровне regions, thresholds fallback/review, calibration, полная регрессия hostile input, privacy, quality и performance и evidence релиза. Без training/personalization/ensemble.

## Задачи

1. Версионировать dataset handwriting/mixed и предотвратить leakage и private content.
2. Выполнить benchmark HTR-кандидатов и принять или отложить ADR-P05 по подтверждениям.
3. Реализовать выбранный adapter и mixed routing regions только при прохождении gates.
4. Откалибровать thresholds review и принять ADR-P04 по evidence конкретного dataset.
5. Завершить тесты no-egress, lifecycle leakage/observability, hostile corpus, isolation worker, supply chain, consent, identity/scope, resources/amplification и cancellation.
6. Подготовить воспроизводимый отчёт MVP benchmark/security/compatibility и review готовности релиза.

## Файлы, которые разрешено изменять

HTR engine adapter/routing, разрешённые fixtures/manifests, benchmark/security/performance tests и reports, configuration thresholds и относящиеся ADR/status docs.

## Файлы, которые не должны изменяться

Training/fine-tuning, user personalization, ensemble/LLM, remote deployment, business logic consumers и private datasets.

## Тесты

Общий contract suite engine, golden metrics HTR/mixed, calibration confidence, routing/fallback regions, partial rerun, no-egress, hostile corpus, cancellation/resource limits, telemetry canary и полная относящаяся regression.

## Контроль качества

Security и performance reviews; документированы dataset, versions и environment; согласованные численные thresholds проходят; отсутствует regression сверх разрешённого tolerance; связаны все evidence для `SEC-001`–`SEC-010` и `AC-004`–`AC-011` в текущей области.

## Определение готовности

Core MVP поддерживает как минимум один OCR adapter и контракт HTR; выбранный runtime HTR/mixed включается только при прохождении evidence. Release report явно показывает неподдерживаемые и отложенные capabilities.

## Критерии приёмки

`AC-004`, `AC-005`; local-only mixed job не имеет egress; низкий confidence приводит к review-required; results остаются воспроизводимыми и traceable.

## Ожидаемые артефакты

HTR/mixed adapter или явное отложенное по evidence решение, принятый ADR thresholds, benchmark/security reports, release checklist и обновление status/log.

## Условия остановки и отката

Если ни один HTR-кандидат не проходит gates, сохранить port/contract HTR и явно отложить runtime support; не снижать thresholds и не выпускать слабый adapter. Отменить включение и config adapter, сохранив evidence benchmark.

<!-- End of historical snapshot. -->
