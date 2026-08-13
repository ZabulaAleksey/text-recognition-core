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
