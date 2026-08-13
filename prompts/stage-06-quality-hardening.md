# Stage 06 — HTR, mixed routing and hardening

## Goal

Add evidence-based handwriting/mixed recognition and complete privacy, security, regression and performance gates for Core MVP review.

## Required context

SPEC sections 29–32, 41–50, 59–66 and `NFR-001`, `NFR-003`–`NFR-005`, `SEC-001`–`SEC-010`, `PERF-001`, `AC-004`–`AC-011`; security/test strategy; pending ADR-P04–P05 (ADR-P03 must already be accepted in Stage 04).

## Dependencies

Stages 01–05 accepted; representative approved handwriting/mixed golden dataset exists.

## Scope

HTR candidate benchmark/selection, region-level OCR/HTR routing, fallback/review thresholds, calibration, full hostile-input/privacy/quality/performance regression and release evidence. No training/personalization/ensemble.

## Tasks

1. Version handwriting/mixed dataset and prevent leakage/private content.
2. Benchmark HTR candidates and accept or defer ADR-P05 based on evidence.
3. Implement selected adapter and mixed region routing only if gates pass.
4. Calibrate review thresholds and accept ADR-P04 with dataset-specific evidence.
5. Complete no-egress, leakage/observability lifecycle, hostile corpus, worker isolation, supply-chain, consent, identity/scope, resource/amplification and cancellation tests.
6. Produce reproducible MVP benchmark/security/compatibility report and release-readiness review.

## Files allowed to change

HTR engine adapter/routing, approved fixtures/manifests, benchmark/security/performance tests and reports, configuration thresholds and relevant ADR/status docs.

## Files that should not change

Training/fine-tuning, user personalization, ensemble/LLM, remote deployment, consumer business logic, private datasets.

## Tests

Shared engine contract, HTR/mixed golden metrics, confidence calibration, region routing/fallback, partial rerun, no-egress, hostile corpus, cancellation/resource limits, telemetry canary and full relevant regression.

## Quality gates

Security and performance reviews; documented dataset/versions/environment; agreed numerical thresholds pass; no regression beyond approved tolerance; all scoped `SEC-001`–`SEC-010` and `AC-004`–`AC-011` evidence linked.

## Definition of Done

Core MVP supports at least one OCR adapter and an HTR contract; selected HTR/mixed runtime is enabled only if evidence passes. Release report makes unsupported/deferred capabilities explicit.

## Acceptance Criteria

`AC-004`, `AC-005`; local-only mixed job has zero egress; low confidence becomes review-required; results remain reproducible and traceable.

## Expected artifacts

HTR/mixed adapter or explicit evidence-based deferral, accepted thresholds ADR, benchmark/security reports, release checklist and status/log update.

## Failure / rollback conditions

If no HTR candidate meets gates, retain the HTR port/contract and defer runtime support explicitly; do not lower thresholds or ship a weak adapter. Revert adapter enablement/config while preserving benchmark evidence.
