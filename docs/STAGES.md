# Этапы Text Recognition Core

- Stage ID: TRC-02-ENGINE-PIPELINE

## TRC-02-ENGINE-PIPELINE — Intake, pipeline и базовый OCR

- Status: partial
- Scope: accepted Stage 02 requirement owners FR-003, NFR-001, NFR-003, PERF-001, AC-002, AC-005, AC-007, AC-010; security SEC-001/002/003/005/006/009. Предшественник Stage 01 verified locally; direct NIGHT FACTORY разрешает dependency-ready работу, обычную интеграцию и публикацию. Stage 03–07 не разблокированы этой частичной реализацией.
- Implemented: pure immutable engine routing (maximum32 descriptors, required capability/privacy fail-closed, explicit selection, deterministic ranking,4096 region routes); source-byte envelope (PNG/JPEG/PDF signatures,64MiB streaming SHA-256, без decoding); fixed public synthetic EN/RU/UK golden smoke with executable fingerprint and digest/path admission. Production OCR adapter, native decoder и worker isolation отсутствуют.
- Bound security repairs: diagnostic child output now has aggregate16KiB cap, strict UTF-8, sanitized start/output errors, deadlines and exact direct-child kill/reap. Commit49911b6,7 new tests/full63PASS; descendant/worker containment не заявляется. TRC-NIGHT-JSON-DUPLICATE-01 commitd6344b4 closes decoded duplicate member overwrite (including privacy_mode) at both public byte parsers and sanitizes syntax/UTF8/recursion/large-int failures;12 new tests/full75PASS. Existing accepted tests/models/generated schemas/dependencies unchanged. Source SPECs: printed-golden-smoke.spec.md and json-boundary-validation.spec.md.
- Evidence: latest locked offline --no-sync suite75PASS, Ruff check/format55 files PASS, strictmypy11 source files PASS; Python3.13.7 differs from retained3.13.6 venv creation marker. This validation is not fresh restore. Earlier unchanged-lock clean two-step restore/import/build/audit20packages0findings at934366 is retained in docs/notes/night-reproducibility-2026-10-01.md. Synthetic Tesseract5.5.3.20260724 on3 authored images CER/WER0; exact fingerprint/latencies/limits in docs/evidence/stage02-printed-smoke.md. This does not establish representative quality or select an adapter. Independent subprocess/JSON boundary reviews ACCEPT; canonical integration documentation review ACCEPTED_BOUNDED. Normal publication/readback remains pending.
- Plan: (1) исследовать decoder PDF/image security/license/resources and define ADR-P01 plus bounded isolation contract; (2) implement disposable least-privilege no-network workers with private per-job roots, CPU/RSS/file/process/output/disk caps, hard timeout/kill and crash/cancel cleanup; (3) hashing/preprocessing coordinate transforms and application orchestration; (4) common engine contract suite and deterministic fake pipeline; (5) verified engine/model manifests and no unsafe serialization; (6) versioned representative approved golden benchmark with CER/WER/layout/latency/memory/disk, then ADR-P02; (7) integrate exactly one evidence-selected local OCR adapter.
- Consumer scenario / terminal gates: approved printed input through actual intake→isolated decoder/preprocessing→selected adapter→immutable result with provenance, supported capability behavior and reversible coordinates. Required tests: ordered multi-source both batch policies, malformed/limit inputs and outputs, mandatory/optional capability/fallback, crash/hang/cancel/hard-kill/cleanup/private-root/no-egress, tampered artifact/unsafe serialization, engine substitution contract and representative benchmark. The current diagnostic does not satisfy this end-to-end scenario.
- Blockers: ADR-P01 decoder/isolation research and contract, representative golden admission, benchmark and ADR-P02 remain engineering work. No dependency on a future Stage may replace these gates. Installed Tesseract is candidate only; no cloud/remote OCR activation.
- NEXT: TRC-02-ISOLATED-DECODER-CONTRACT
- USER action TRC-REPRESENTATIVE-CORPUS-01: pending_if_private_data_needed; only if public/authored representative data cannot cover the agreed benchmark, owner must authorize anonymized local corpus, privacy/export scope and reproducible manifest without publishing private files. Expected evidence: approved corpus scope/digests and quality/resource evaluation; unlock: representative benchmark. Public synthetic research can proceed now.
- Integration checkpoint: locald6344b4 and remotec6f6b39 histories are converged in the accepted integration candidate without rewrite; remote ADR-012 single-owner policy preserved, colliding local ADRs renumbered013/014/015. Remote Stage01 no-code/no-launch facts are superseded by verified local implementation and explicit NIGHT authorization. No merge publication/release is claimed until readback.
- Temporary implementation: pure planner and developer-only synthetic diagnostic are fully working within their scopes, but Stage02 remains partial until its actual isolated consumer path and all terminal evidence pass.
- Deferred: corrections/revisions, REST, persistent jobs, consumer business models and remote/cloud engines remain outside Stage02 scope. No private fixtures, installation or runtime/model activation is authorized by metadata/candidate presence.
- Stop/rollback: fail closed on incompatible license, uncontainable decoding, integrity failure or private data; retain current pure contract baseline and evidence. Do not weaken accepted tests. New behavior is reversible through ordinary commits; no persistent data migration is involved.

## TRC-01-FOUNDATION — библиотечный фундамент

- Status: verified locally
- Requirements: FR-001, FR-002, FR-010, NFR-002, NFR-005, SEC-009, AC-001, AC-010.
- Evidence: Python3.13 library-first immutable Document→Page→Region→Line→Token domain, framework-neutral application ports, strict request/result boundaries, generated JSON Schema. Original29 unit/schema/supply-chain tests, Ruff/mypy, locked wheel/sdist, installed wheel/import/schema smoke and clean two-step offline restore passed; source docs/evidence/stage01-supply-chain.md. Editable build lock correction934366 adds declared editables0.6 without another lock/manager; current full75PASS covers preserved contracts. No OCR SDK, REST, DB or queue is claimed implemented.
- Condition: earlier remote blocked/no-product facts atc6f6b39 are historical and superseded by accepted local evidence, readable retained contract and explicit NIGHT execution. Earlier user-authorized documentation integration b1af28b remains retained in ancestry.
- NEXT: TRC-02-ENGINE-PIPELINE

## Поздние этапы

- Stage03 corrections/revisions/rerun requires completed Stage02 stable raw contract.
- Stage04 local persistence/jobs/REST requires prior stages and ADR-P03 retention/deletion.
- Stage05 consumer adapters requires stable result/revision API.
- Stage06 HTR/mixed routing requires representative handwriting benchmark.
- Stage07 CLI/MCP/remote remains optional and needs separate SPEC/security admission.
