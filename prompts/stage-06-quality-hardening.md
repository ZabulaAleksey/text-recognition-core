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
