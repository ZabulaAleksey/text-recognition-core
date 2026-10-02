# Стратегия тестирования и benchmarks

Тесты доказывают стабильные требования `specs/system.spec.md`; snapshots и benchmarks не переопределяют их.

## Уровни тестирования

| Уровень | Область | Обязательное подтверждение |
|---|---|---|
| Unit | value objects, нормализация координат и confidence, selection, операции corrections | быстрые детерминированные тесты |
| Domain properties | инварианты tree/revision, replay, hashes, стабильные IDs | property-based сценарии, где это полезно |
| Engine contract | каждый adapter `RecognitionEngine` | один общий параметризованный набор |
| Integration | intake → pipeline → engine → raw/result; storage/jobs/cancel/idempotency | локальные детерминированные fixtures |
| API/schema | JSON Schema/OpenAPI/error/compatibility | contract snapshots и обнаружение breaking changes |
| Application adapter | проекции Chronicle/Receipt/Tutor и provenance | синтетические или анонимизированные fixtures |
| Golden/regression | качество OCR/HTR/layout/fields | версионированный отчёт относительно baseline |
| Security | вредоносный ввод, limits, traversal, egress, leakage, tenant boundaries | негативный набор и security review |
| Performance | latency, pages/sec, memory, CPU/GPU, queue | воспроизводимая среда и отчёт |

Базовым runner является Pytest; его fixtures и параметризация поддерживают общий набор тестов adapters (<https://docs.pytest.org/en/stable/>).

Stage 02 pre-decoder envelope tests validate bounded byte reads, signatures,
SHA-256 and redacted errors; they do not count as decoder isolation or OCR E2E.

## Общий набор контрактных тестов engine

Для каждого включённого adapter:

- заявленные capabilities/languages/version соответствуют поведению;
- выходные IDs, tree, reading order и coordinates корректны;
- confidence нормализован или явно недоступен;
- provenance содержит версии engine/model/adapter/config;
- обязательная неподдерживаемая capability завершается явной ошибкой;
- соблюдаются timeout, cancel и resource budget;
- vendor errors преобразуются в стабильные codes без чувствительного содержимого;
- `LOCAL_ONLY` отклоняет нелокальные engines;
- `recognize_region` не требует повторного запуска всего документа;
- повторная обработка детерминированного fixture создаёт эквивалентный по схеме результат.

## Набор тестов corrections и revisions

- raw content hash не изменяется после correction, rollback или rerun;
- проверяются `before` correction и base revision;
- устаревшая base возвращает conflict;
- replay создаёт стабильные content hash и current view;
- ancestry split/merge и старые revisions остаются доступными;
- частичный rerun добавляет новые evidence и revision;
- конкурентная транзакция correction не может потерять принятое обновление.

## Политика golden dataset

Разрешены только синтетические, анонимизированные или явно одобренные данные. Manifest фиксирует версию dataset, license/approval, language/script, тип документа, ожидаемую структуру и split. Реальные приватные дневники, работы учеников и чеки запрещены в публичном Git. Наборы train, validation и test/golden не могут пересекаться молча.

Начальные срезы: печатные тексты на украинском, русском и английском языках, рукописный текст, смешанные страницы, синтетические чеки UA, учебные листы Tutor и вредоносные или граничные случаи. Выбор HTR заблокирован, пока handwriting-срез не станет репрезентативным.

## Метрики

- OCR/HTR: CER, WER, coverage и калибровка low-confidence.
- Layout: обнаружение regions, reading order и корректность coordinates.
- Проекция Receipt: точность fields/items/total с покрытием provenance.
- Операционные показатели: процентили latency, pages/sec, peak RSS, CPU/GPU, количество queue/fallback/error.

Этап 02 устанавливает версионированные baselines и предлагаемые численные бюджеты. До этого неподтверждённые заявления о точности или throughput не являются release gate.

## Тесты безопасности

Повреждённые форматы; request body, глубина JSON и cardinality; усиление aggregate multi-page output, tokens/alternatives/text, disk и queue; слишком большие dimensions/pages/decompression; crash/hang/hard-kill/cancel/cleanup worker и изоляция private root; traversal/symlink; небезопасные metadata; corpus parser; отсутствие egress в `LOCAL_ONLY`; local wildcard bind, permissions/bootstrap/rotation/revocation/redaction token-file, отказ credentials/Origin; подмена actor/source-role/target; отсутствие, подделка, истечение и отзыв consent; подмена dependency/model, lock drift и unsafe serialization; telemetry canaries через validation/parser/vendor/audit/rotation; одинаковая idempotency identity с одинаковым и различным request hash доказывает возврат или conflict и отсутствие duplicate job; отдельные collisions cache scope и deletion/`AC-011`; remote SSRF/DNS/redirect/cross-tenant сценарии до включения этих режимов.

## Контроль качества по этапам

- Foundation: lint/type/unit/schema/invariant tests, а также проверки hash lock, SBOM/license/vulnerability и политики unsafe serialization.
- Engine: общий contract suite, приёмка isolated worker, golden benchmark, проверенные signature/digest артефакта и license/security evidence.
- Corrections: replay/property/concurrency и raw immutability.
- Storage/jobs/API: integration, migration/recovery, idempotency/cancel, API compatibility и негативные security tests.
- Applications: contract/provenance tests adapter и отсутствие утечки доменной логики.
- Release: полный относящийся к изменению набор, сравнение benchmark, dependency scan, reviewer и security review; performance review при изменении горячих путей.

## Трассировка

Stage 02 printed smoke evidence: `tests/fixtures/printed_golden_v1/manifest.json` and `tests/contracts/golden/test_printed_smoke.py` prove bounded synthetic corpus integrity; `python -m tools.printed_golden_smoke` reports the installed Tesseract candidate on only those trusted fixtures. Tiny synthetic CER/WER 0 is not a representative quality or worker-isolation gate.

Stage 02 planning evidence: `tests/unit/test_engine_registry.py` проверяет порядок,
explicit selection, region mapping и fail-closed privacy/capability. Эти тесты
не подтверждают worker isolation, engine contract или OCR quality.

Pytest entrypoint parity: `uv run --locked --offline pytest` and `uv run --locked --offline python -m pytest` both resolve repository-local `tests` and diagnostic `tools` through the explicit project-root pythonpath. Use a writable `--basetemp` on restricted Windows hosts.

Stage 01 local evidence: `uv lock --check --offline`, two-step `uv sync --locked
--no-install-project` → `uv sync --locked --no-build-isolation`, `uv run pytest`,
`uv run ruff check src tests`, `uv run ruff format --check src tests`, `uv run mypy src`,
`uv audit --locked` и `uv build --offline --no-build-isolation`. На Windows sandbox
проверки использовали writable scratch `TEMP`/`TMP` и cache dirs; это не продуктовая
runtime configuration. 29 unit/schema/supply-chain tests PASS, lint/type/build PASS.


Тесты ссылаются на `FR-*`, `NFR-*`, `SEC-*`, `PERF-*` или `AC-*` в именах, markers или metadata отчёта. Требование завершено только после реализации и связи с автоматическим подтверждением либо когда документированная ручная проверка объясняет невозможность автоматизации.

## Stage 02 isolated raster evidence (2026-10-02)

Сохранённый final locked offline suite:238PASS/0skip на project CPython3.13.7,
Ruff check/format37files PASS, mypy15sourcefiles PASS, lock check22resolved PASS,
offline no-build-isolation wheel/sdist PASS. Original75 accepted tests/models/fixtures
не изменены. New163: worker28, framing31, parent64, review10, recovery4,
interruption14, native Windows helper10, actual authored PNG/JPEG2.

Current source/test/worker working-copy hashes совпали с final receipt после recovery;
прошедшие canary campaigns не повторялись. Existing live controls,18actual input cases
и8failure canaries документированы отдельно от unit/mock evidence. Они не подтверждают
representative OCR quality, rootless daemon, process/host-loss recovery или production.

Fresh consumer v5: offline restore unchanged five default dependencies with
`--require-hashes`, install built SDK wheel `--no-deps`, isolated `-I -B` Python3.13.7
import from fresh site-packages; Pillow distribution/PIL import absent. Actual benign
authored RGB PNG/gray JPEG returned exact expected pixels and hashes after cleanup.
uv0.12.3 local-file multiple-distinct SHA allowance reproduced a mismatch even when
computed hash was a member; narrowing only core to its exact already-locked Windows
wheel hash succeeded. Other four package/hash blocks stayed byte-identical; wrong-hash
negative stayed fail. No hash bypass, version upgrade or dependency scan occurred.

External audit is `BLOCKED_EXTERNAL_APPROVAL`; no hosted TRC CI run is inferred from
local validation. Detailed sanitized proof: `docs/evidence/stage02-isolated-raster.md`
and `.json`. The entire Stage02 remains partial.
