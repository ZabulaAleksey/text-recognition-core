# Канонические этапы text-recognition-core  Единый источник stage-prompts. Ниже сохранено полное содержание ранее существовавших этапов.

## stage-01-foundation
# Р­С‚Р°Рї 01 вЂ” Р¤СѓРЅРґР°РјРµРЅС‚ Рё С‚РёРїРёР·РёСЂРѕРІР°РЅРЅС‹Рµ РєРѕРЅС‚СЂР°РєС‚С‹

## Р¦РµР»СЊ

РЎРѕР·РґР°С‚СЊ С„СѓРЅРґР°РјРµРЅС‚ Python-Р±РёР±Р»РёРѕС‚РµРєРё Рё РЅРµРёР·РјРµРЅСЏРµРјС‹Рµ С‚РёРїРёР·РёСЂРѕРІР°РЅРЅС‹Рµ РєРѕРЅС‚СЂР°РєС‚С‹ Core Р±РµР· РїСЂРѕРґСѓРєС‚РѕРІС‹С… РёРЅС‚РµРіСЂР°С†РёР№.

## РћР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚

`AGENTS.md`; СЂР°Р·РґРµР»С‹ SPEC 7вЂ“16, 40, 56вЂ“58 Рё IDs `FR-001`, `FR-002`, `FR-010`, `NFR-002`, `NFR-005`, `AC-001`; `docs/ARCHITECTURE.md`, `API.md`, `DATA_MODEL.md`, ADR-002вЂ“005; С‚РµРєСѓС‰РёРµ `AI_STATUS` Рё `AI_PLAN`.

## Р—Р°РІРёСЃРёРјРѕСЃС‚Рё

РџСЂРёРЅСЏС‚С‹Р№ РљРђР РљРђРЎ Рё РїРѕРґРґРµСЂР¶РёРІР°РµРјР°СЏ СЃСЂРµРґР° Python 3.13. РџСЂРµРґС‹РґСѓС‰РёС… СЌС‚Р°РїРѕРІ РєРѕРґР° РЅРµС‚.

## РћР±Р»Р°СЃС‚СЊ

РЈРїР°РєРѕРІРєР°, domain values/entities, application ports, РіСЂР°РЅРёС†Р° schema, ports РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹С… IDs Рё clock, in-memory test doubles Рё С„СѓРЅРґР°РјРµРЅС‚Р°Р»СЊРЅС‹Рµ С‚РµСЃС‚С‹.

## Р—Р°РґР°С‡Рё

1. РЎРѕР·РґР°С‚СЊ `pyproject.toml` Рё РіСЂР°РЅРёС†С‹ РїР°РєРµС‚Р° `src/`, СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёРµ Р°СЂС…РёС‚РµРєС‚СѓСЂРµ.
2. Р РµР°Р»РёР·РѕРІР°С‚СЊ СЃС‚СЂРѕРіРёРµ РЅРµРёР·РјРµРЅСЏРµРјС‹Рµ value types РґР»СЏ IDs, coordinates, confidence, modes/capabilities/privacy, errors Рё provenance.
3. Р РµР°Р»РёР·РѕРІР°С‚СЊ С‚РёРїРёР·РёСЂРѕРІР°РЅРЅС‹Рµ РєРѕРЅС‚СЂР°РєС‚С‹ request/result Рё Document/Page/Region/Line/Token; СЂР°Р·РґРµР»РёС‚СЊ IDs raw Рё current revision.
4. РћРїСЂРµРґРµР»РёС‚СЊ РЅРµР·Р°РІРёСЃРёРјС‹Рµ РѕС‚ С„СЂРµР№РјРІРѕСЂРєР° ports engine/storage/job/cancellation Р±РµР· РєРѕРЅРєСЂРµС‚РЅС‹С… adapters.
5. Р“РµРЅРµСЂРёСЂРѕРІР°С‚СЊ JSON Schema РёР· РѕРґРЅРѕРіРѕ РёСЃС‚РѕС‡РЅРёРєР° boundary models Рё РґРѕР±Р°РІРёС‚СЊ fixture РІРµСЂСЃРёРё Рё СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё.
6. Р”РѕР±Р°РІРёС‚СЊ С‚РµСЃС‚С‹ РіСЂР°РЅРёС† architecture/import Рё domain invariants.
7. РЎРѕР·РґР°С‚СЊ РЅР°Р±РѕСЂ dependencies СЃ Р·Р°РєСЂРµРїР»С‘РЅРЅС‹РјРё hashes, РїРѕР»РёС‚РёРєСѓ РґРѕРІРµСЂРµРЅРЅС‹С… indexes Рё РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё SBOM/license/vulnerability/unsafe deserialization.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂРµС€РµРЅРѕ РёР·РјРµРЅСЏС‚СЊ

Р¤Р°Р№Р»С‹ СѓРїР°РєРѕРІРєРё; `src/text_recognition_core/domain/**`, `application/**`, `schemas/**`; `tests/unit/**`, `tests/contracts/schema/**`; С„Р°РєС‚РёС‡РµСЃРєРёРµ РґРѕРєСѓРјРµРЅС‚С‹ status/decision/log.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ РЅРµ РґРѕР»Р¶РЅС‹ РёР·РјРµРЅСЏС‚СЊСЃСЏ

РџРѕРІРµРґРµРЅРёРµ SPEC; СЂРµР°Р»РёР·Р°С†РёСЏ engine/storage/REST/application adapters; golden/private fixtures; РіР»РѕР±Р°Р»СЊРЅР°СЏ РєРѕРЅС„РёРіСѓСЂР°С†РёСЏ workspace.

## РўРµСЃС‚С‹

РЎС‚СЂРѕРіРёРµ РґРѕРїСѓСЃС‚РёРјС‹Рµ Рё РЅРµРґРѕРїСѓСЃС‚РёРјС‹Рµ СЃР»СѓС‡Р°Рё schema, РІРєР»СЋС‡Р°СЏ РѕРґРёРЅРѕС‡РЅС‹Рµ Рё batch requests Рё РѕР±Рµ batch policies, РіСЂР°РЅРёС†С‹ РіР»СѓР±РёРЅС‹ Рё cardinality JSON, body Рё response, РІР»РѕР¶РµРЅРЅСѓСЋ РёРµСЂР°СЂС…РёСЋ, РіСЂР°РЅРёС†С‹ coordinates, РєРѕРЅРµС‡РЅС‹Р№ confidence, РїСЂР°РІРёР»Р° reading order Рё IDs, serialization errors, snapshot СЃРіРµРЅРµСЂРёСЂРѕРІР°РЅРЅРѕР№ schema, Р·Р°РїСЂРµС‰С‘РЅРЅС‹Рµ imports infrastructure, lock drift Рё Р·Р°РїСЂРµС‰С‘РЅРЅСѓСЋ РёСЃРїРѕР»РЅСЏРµРјСѓСЋ РёР»Рё РѕР±СЉРµРєС‚РЅСѓСЋ serialization.

## РљРѕРЅС‚СЂРѕР»СЊ РєР°С‡РµСЃС‚РІР°

РџСЂРѕС…РѕРґСЏС‚ formatter, linter, type checker Рё test suite; РІ domain/application РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‚ imports framework/OCR/database; public contracts С‚СЂР°СЃСЃРёСЂСѓСЋС‚СЃСЏ Рє IDs С‚СЂРµР±РѕРІР°РЅРёР№ С‚РµРєСѓС‰РµР№ РѕР±Р»Р°СЃС‚Рё; СЃ РїРµСЂРІРѕРіРѕ СѓСЃС‚Р°РЅР°РІР»РёРІР°РµРјРѕРіРѕ РїР°РєРµС‚Р° СЃСѓС‰РµСЃС‚РІСѓСЋС‚ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ hashes dependencies, SBOM, licenses Рё vulnerabilities.

## РћРїСЂРµРґРµР»РµРЅРёРµ РіРѕС‚РѕРІРЅРѕСЃС‚Рё

РџР°РєРµС‚ СѓСЃС‚Р°РЅР°РІР»РёРІР°РµС‚СЃСЏ Р»РѕРєР°Р»СЊРЅРѕ, contracts РјРѕРіСѓС‚ РІР°Р»РёРґРёСЂРѕРІР°С‚СЊ Рё СЃРµСЂРёР°Р»РёР·РѕРІР°С‚СЊ СЂРµРїСЂРµР·РµРЅС‚Р°С‚РёРІРЅС‹Рµ РїСЂРёРјРµСЂС‹, РіРµРЅРµСЂР°С†РёСЏ schema РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅР°, Р° РІСЃРµ ports РЅРµ РёРјРµСЋС‚ СЂРµР°Р»РёР·Р°С†РёРё infrastructure.

## РљСЂРёС‚РµСЂРёРё РїСЂРёС‘РјРєРё

`AC-001`, `AC-010`; Р°СЂС…РёС‚РµРєС‚СѓСЂРЅРѕРµ `NFR-002`; СЏРІРЅС‹Рµ РІРµСЂСЃРёРё API/schema Рё СЂР°Р·РґРµР»РµРЅРёРµ raw/current IDs.

## РћР¶РёРґР°РµРјС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹

РљР°СЂРєР°СЃ РїР°РєРµС‚Р° Python, fixtures СЃРіРµРЅРµСЂРёСЂРѕРІР°РЅРЅС‹С… schemas, tests, РѕР±РЅРѕРІР»С‘РЅРЅС‹Рµ РїРѕ С„Р°РєС‚Р°Рј status/log Рё РЅРµРѕР±С…РѕРґРёРјС‹Рµ СѓС‚РѕС‡РЅРµРЅРёСЏ ADR.

## РЈСЃР»РѕРІРёСЏ РѕСЃС‚Р°РЅРѕРІРєРё Рё РѕС‚РєР°С‚Р°

РћСЃС‚Р°РЅРѕРІРёС‚СЊСЃСЏ, РµСЃР»Рё contracts С‚СЂРµР±СѓСЋС‚ РёР·РјРµРЅРёС‚СЊ СЃРµРјР°РЅС‚РёРєСѓ SPEC, РµСЃР»Рё РѕРґРёРЅ РёСЃС‚РѕС‡РЅРёРє models РЅРµ РјРѕР¶РµС‚ РіРµРЅРµСЂРёСЂРѕРІР°С‚СЊ schemas РёР»Рё РµСЃР»Рё domain С‚СЂРµР±СѓРµС‚ import С„СЂРµР№РјРІРѕСЂРєР°. РћС‚РјРµРЅРёС‚СЊ commit СЌС‚Р°РїР°; РјРёРіСЂР°С†РёРё Рё РІРЅРµС€РЅРµРµ СЃРѕСЃС‚РѕСЏРЅРёРµ Р·Р°РїСЂРµС‰РµРЅС‹.


## stage-02-engine-pipeline
Stage 02 current outcome (2026-09-30): PARTIAL. Pure immutable engine routing planner,
privacy/capability fail-closed behavior and region planning verified locally; see
`specs/features/engine-routing.spec.md` and `docs/AI_STATUS.md`. Binary intake,
isolated workers, representative golden benchmark and baseline OCR adapter remain open. This
bounded slice does not satisfy the complete Stage 02 acceptance contract.
Synthetic printed golden smoke now covers eng/rus/ukr with fixed SHA-256 images and a bounded executable fingerprint,
manifest integrity and tamper/path-negative tests. Installed Tesseract 5.5.3
scores CER/WER 0 only on these three easy images; see
`specs/features/printed-golden-smoke.spec.md` and
`docs/evidence/stage02-printed-smoke.md`. This does not select an OCR engine,
establish representative thresholds or activate native parsing.

# Р­С‚Р°Рї 02 вЂ” Intake, pipeline Рё Р±Р°Р·РѕРІС‹Р№ OCR

## Р¦РµР»СЊ

Р РµР°Р»РёР·РѕРІР°С‚СЊ Р±РµР·РѕРїР°СЃРЅСѓСЋ orchestration СЂР°СЃРїРѕР·РЅР°РІР°РЅРёСЏ Рё РІС‹Р±СЂР°С‚СЊ РѕРґРёРЅ Р»РѕРєР°Р»СЊРЅС‹Р№ OCR adapter РЅР° РѕСЃРЅРѕРІР°РЅРёРё РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹С… РїРѕРґС‚РІРµСЂР¶РґРµРЅРёР№.

## РћР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚

Р Р°Р·РґРµР»С‹ SPEC 23вЂ“29, 42вЂ“50, 59, 62 Рё `FR-003`, `NFR-001`, `NFR-003`, `PERF-001`, `AC-002`, `AC-005`; РїРѕС‚РѕРєРё engine/intake Р°СЂС…РёС‚РµРєС‚СѓСЂС‹; port engine РёР· API; РїСЂР°РІРёР»Р° security РґР»СЏ РІС…РѕРґР° Рё СЂРµСЃСѓСЂСЃРѕРІ; СЃС‚СЂР°С‚РµРіРёСЏ С‚РµСЃС‚РёСЂРѕРІР°РЅРёСЏ; ADR-007/P01/P02.

## Р—Р°РІРёСЃРёРјРѕСЃС‚Рё

РџСЂРёРЅСЏС‚ СЌС‚Р°Рї 01. РџРѕРґРіРѕС‚РѕРІР»РµРЅС‹ СЂР°Р·СЂРµС€С‘РЅРЅС‹Р№ СЃРёРЅС‚РµС‚РёС‡РµСЃРєРёР№ РёР»Рё Р°РЅРѕРЅРёРјРёР·РёСЂРѕРІР°РЅРЅС‹Р№ РїРµС‡Р°С‚РЅС‹Р№ golden slice Рё СЃСЂРµРґР° РѕС†РµРЅРєРё.

## РћР±Р»Р°СЃС‚СЊ

Р‘РµР·РѕРїР°СЃРЅС‹Р№ intake РёР·РѕР±СЂР°Р¶РµРЅРёР№, СЃРјРµРЅСЏРµРјС‹Рµ СЌС‚Р°РїС‹ preprocessing/layout, registry, РІС‹Р±РѕСЂ Рё fallback engines, fake engine, benchmark РєР°РЅРґРёРґР°С‚РѕРІ Рё СЂРѕРІРЅРѕ РѕРґРёРЅ Р±Р°Р·РѕРІС‹Р№ Р»РѕРєР°Р»СЊРЅС‹Р№ OCR adapter.

## Р—Р°РґР°С‡Рё

1. РСЃСЃР»РµРґРѕРІР°С‚СЊ Рё РІС‹Р±СЂР°С‚СЊ Р±РёР±Р»РёРѕС‚РµРєРё decoder PDF/image СЃ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏРјРё license/security/resources; ADR-P01 РЅРµ РїСЂРёРЅРёРјР°РµС‚СЃСЏ Р±РµР· РѕРїРёСЃР°РЅРЅРѕР№ РЅРёР¶Рµ РёР·РѕР»СЏС†РёРё.
2. Р РµР°Р»РёР·РѕРІР°С‚СЊ РґРµРєРѕРґРёСЂРѕРІР°РЅРёРµ binary, parsing metadata Рё inference OCR/model РІ РѕРґРЅРѕСЂР°Р·РѕРІС‹С… subprocess workers СЃ РјРёРЅРёРјР°Р»СЊРЅС‹РјРё РїСЂР°РІР°РјРё РёР»Рё СЌРєРІРёРІР°Р»РµРЅС‚РЅРѕРј sandbox: Р±РµР· СЃРµС‚Рё, СЃ РЅРµРїСЂРёРІРёР»РµРіРёСЂРѕРІР°РЅРЅРѕР№ identity, РјРёРЅРёРјР°Р»СЊРЅС‹Рј read-only source, РїСЂРёРІР°С‚РЅС‹Рј per-job temp root, OS limits CPU/RSS/files/processes, Р¶С‘СЃС‚РєРёРј timeout/kill Рё РѕС‡РёСЃС‚РєРѕР№ РїРѕСЃР»Рµ crash/cancel.
3. Р РµР°Р»РёР·РѕРІР°С‚СЊ validation, hashing, РїСЂРѕРёР·РІРѕРґРЅС‹Рµ preprocessing artifacts Рё РѕР±СЂР°С‚РёРјС‹Рµ coordinate transforms.
4. Р РµР°Р»РёР·РѕРІР°С‚СЊ registry, selection capabilities, РїСЂР°РІРёР»Р° fallback Рё budgets cancellation/resources, РІРєР»СЋС‡Р°СЏ quotas output/artifacts/disk.
5. РЎРѕР·РґР°С‚СЊ РѕР±С‰РёР№ contract suite engines Рё fake adapter.
6. РџСЂРѕРІРµСЂСЏС‚СЊ РїРѕРґРїРёСЃР°РЅРЅС‹Рµ РёР»Рё digest-verified manifests model/engine Рё РѕС‚РєР»РѕРЅСЏС‚СЊ unsafe serialization РґРѕ Р·Р°РіСЂСѓР·РєРё.
7. Р’С‹РїРѕР»РЅРёС‚СЊ benchmark Р»РѕРєР°Р»СЊРЅС‹С… OCR-РєР°РЅРґРёРґР°С‚РѕРІ РЅР° РІРµСЂСЃРёРѕРЅРёСЂРѕРІР°РЅРЅС‹С… golden data; СЃРѕС…СЂР°РЅРёС‚СЊ РѕС‚С‡С‘С‚ quality/resources Рё РїСЂРёРЅСЏС‚СЊ ADR-P02.
8. РРЅС‚РµРіСЂРёСЂРѕРІР°С‚СЊ С‚РѕР»СЊРєРѕ РІС‹Р±СЂР°РЅРЅС‹Р№ adapter Рё РЅРѕСЂРјР°Р»РёР·РѕРІР°С‚СЊ errors/confidence/provenance.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂРµС€РµРЅРѕ РёР·РјРµРЅСЏС‚СЊ

`pyproject.toml`, lock dependencies Рё Р°СЂС‚РµС„Р°РєС‚С‹ SBOM/license; `src/**/intake/**`, `pipelines/**`, `engines/**`, РѕС‚РЅРѕСЃСЏС‰Р°СЏСЃСЏ application orchestration; СЂР°Р·СЂРµС€С‘РЅРЅС‹Рµ `tests/fixtures/**`, contract/integration/benchmark/security tests; ADR/status/log.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ РЅРµ РґРѕР»Р¶РЅС‹ РёР·РјРµРЅСЏС‚СЊСЃСЏ

Р РµР°Р»РёР·Р°С†РёСЏ corrections/revisions, REST Рё persistent jobs, business models consumers, remote/cloud engines Рё private fixtures.

## РўРµСЃС‚С‹

Contract suite engines, СѓРїРѕСЂСЏРґРѕС‡РµРЅРЅС‹Рµ multi-source success/failure РїСЂРё РѕР±РµРёС… batch policies, РїРѕРІСЂРµР¶РґС‘РЅРЅС‹Р№ РёР»Рё РїСЂРµРІС‹С€Р°СЋС‰РёР№ limits input/output, coordinate transforms, РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Рё РЅРµРѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ capabilities, fallback, РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹Р№ fake pipeline, worker crash/hang/hard-kill/cancel/cleanup/private-root/no-egress, РїРѕРґРјРµРЅС‘РЅРЅС‹Р№ artifact Рё unsafe serialization, golden CER/WER/layout Рё РѕС‚С‡С‘С‚ latency/memory/disk.

## РљРѕРЅС‚СЂРѕР»СЊ РєР°С‡РµСЃС‚РІР°

`AC-002`, `AC-005`, `AC-007`, `AC-010`; scan vulnerability/license/provenance dependencies Рё РїСЂРѕРІРµСЂРєР° lock; security review decoders/adapters Рё isolation worker; evidence benchmark СѓРєР°Р·С‹РІР°РµС‚ dataset Рё versions; РЅРµС‚ РЅРµРїРѕРґС‚РІРµСЂР¶РґС‘РЅРЅС‹С… Р·Р°СЏРІР»РµРЅРёР№ Рѕ С‚РѕС‡РЅРѕСЃС‚Рё; РІРєР»СЋС‡С‘РЅ СЂРѕРІРЅРѕ РѕРґРёРЅ production baseline OCR adapter.

## РћРїСЂРµРґРµР»РµРЅРёРµ РіРѕС‚РѕРІРЅРѕСЃС‚Рё

РџРѕРґРґРµСЂР¶РёРІР°РµРјС‹Р№ РїРµС‡Р°С‚РЅС‹Р№ input offline РїСЂРѕС…РѕРґРёС‚ С‡РµСЂРµР· ports Рё СЃРѕР·РґР°С‘С‚ РєРѕСЂСЂРµРєС‚РЅС‹Р№ РЅРµРёР·РјРµРЅСЏРµРјС‹Р№ raw result, Р° СЂРµС€РµРЅРёРµ Рѕ РІС‹Р±СЂР°РЅРЅРѕРј engine РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјРѕ.

## РљСЂРёС‚РµСЂРёРё РїСЂРёС‘РјРєРё

Р—Р°РјРµРЅР° engine С‚СЂРµР±СѓРµС‚ С‚РѕР»СЊРєРѕ РЅРѕРІРѕРіРѕ adapter; raw result СЃРѕРґРµСЂР¶РёС‚ РїРѕР»РЅС‹Р№ provenance; РЅРµРґРѕРїСѓСЃС‚РёРјС‹Р№ input Р·Р°РІРµСЂС€Р°РµС‚СЃСЏ Р±РµР·РѕРїР°СЃРЅРѕ; РЅРµРѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ capabilities СЃРѕР·РґР°СЋС‚ РїСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ, Р° РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р·Р°РІРµСЂС€Р°СЋС‚СЃСЏ СЏРІРЅРѕР№ РѕС€РёР±РєРѕР№.

## РћР¶РёРґР°РµРјС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹

РљРѕРґ pipeline Рё adapter, golden manifest/report, РїСЂРёРЅСЏС‚С‹Рµ ADR decoder/engine Рё contract/security tests.

## РЈСЃР»РѕРІРёСЏ РѕСЃС‚Р°РЅРѕРІРєРё Рё РѕС‚РєР°С‚Р°

РћСЃС‚Р°РЅРѕРІРёС‚СЊСЃСЏ, РµСЃР»Рё РЅРё РѕРґРёРЅ РєР°РЅРґРёРґР°С‚ РЅРµ РґРѕСЃС‚РёРіР°РµС‚ СЃРѕРіР»Р°СЃРѕРІР°РЅРЅРѕРіРѕ РјРёРЅРёРјСѓРјР°, licenses РЅРµСЃРѕРІРјРµСЃС‚РёРјС‹, decoding РЅРµР»СЊР·СЏ РёР·РѕР»РёСЂРѕРІР°С‚СЊ РёР»Рё РѕРіСЂР°РЅРёС‡РёС‚СЊ, integrity Р°СЂС‚РµС„Р°РєС‚РѕРІ РЅРµР»СЊР·СЏ РїСЂРѕРІРµСЂРёС‚СЊ Р»РёР±Рѕ РѕР±РЅР°СЂСѓР¶РµРЅС‹ private data. РЈРґР°Р»РёС‚СЊ adapter Рё artifacts Рё СЃРѕС…СЂР°РЅРёС‚СЊ fake contract baseline; РЅРµ РѕСЃР»Р°Р±Р»СЏС‚СЊ gates РјРѕР»С‡Р°.


## stage-03-corrections-revisions
# Р­С‚Р°Рї 03 вЂ” Corrections, revisions Рё С‡Р°СЃС‚РёС‡РЅС‹Р№ РїРѕРІС‚РѕСЂРЅС‹Р№ Р·Р°РїСѓСЃРє

## Р¦РµР»СЊ

Р РµР°Р»РёР·РѕРІР°С‚СЊ append-only РїРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРёРµ РёСЃРїСЂР°РІР»РµРЅРёСЏ Рё РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅРѕРµ РїРѕРІРµРґРµРЅРёРµ revisions Р±РµР· РёР·РјРµРЅРµРЅРёСЏ РґРѕРєР°Р·Р°С‚РµР»СЊСЃС‚РІ СЂР°СЃРїРѕР·РЅР°РІР°РЅРёСЏ.

## РћР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚

Р Р°Р·РґРµР»С‹ SPEC 17вЂ“23, 55вЂ“57 Рё `FR-004`вЂ“`FR-006`, `AC-003`; РїРѕС‚РѕРє corrections РІ Р°СЂС…РёС‚РµРєС‚СѓСЂРµ; `CorrectionRequest` РёР· API; РёРЅРІР°СЂРёР°РЅС‚С‹ identity/revision РјРѕРґРµР»Рё РґР°РЅРЅС‹С…; ADR-005.

## Р—Р°РІРёСЃРёРјРѕСЃС‚Рё

РџСЂРёРЅСЏС‚С‹ СЌС‚Р°РїС‹ 01вЂ“02; РґРѕСЃС‚СѓРїРЅС‹ raw snapshots Рё ports СЂР°СЃРїРѕР·РЅР°РІР°РЅРёСЏ regions.

## РћР±Р»Р°СЃС‚СЊ

РћРїРµСЂР°С†РёРё corrections, validation target, РѕРїС‚РёРјРёСЃС‚РёС‡РЅС‹Рµ Р»РёРЅРµР№РЅС‹Рµ revisions, replay/current view/diff/rollback, ancestry split/merge Рё orchestration РїРѕРІС‚РѕСЂРЅРѕРіРѕ СЂР°СЃРїРѕР·РЅР°РІР°РЅРёСЏ scope СЃРЅР°С‡Р°Р»Р° СЃ in-memory repositories.

## Р—Р°РґР°С‡Рё

1. Р РµР°Р»РёР·РѕРІР°С‚СЊ С‚РёРїРёР·РёСЂРѕРІР°РЅРЅС‹Рµ РѕРїРµСЂР°С†РёРё corrections Рё validation before/base.
2. РђС‚РѕРјР°СЂРЅРѕ РґРѕР±Р°РІР»СЏС‚СЊ revisions С‡РµСЂРµР· port unit-of-work; РѕС‚РєР»РѕРЅСЏС‚СЊ СѓСЃС‚Р°СЂРµРІС€РёРµ bases.
3. Р РµР°Р»РёР·РѕРІР°С‚СЊ РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹Рµ replay, current projection, СЃС‚СЂСѓРєС‚СѓСЂРЅС‹Р№ Рё С‚РµРєСЃС‚РѕРІС‹Р№ diff Рё rollback РєР°Рє РЅРѕРІСѓСЋ revision.
4. РЎРѕС…СЂР°РЅСЏС‚СЊ РёР»Рё СЃРѕР·РґР°РІР°С‚СЊ IDs РґР»СЏ replace/split/merge Рё РїРѕРґРґРµСЂР¶РёРІР°С‚СЊ ancestry.
5. РџСЂРё partial rerun РґРѕР±Р°РІР»СЏС‚СЊ raw evidence Рё revision Р±РµР· РїРµСЂРµР·Р°РїРёСЃРё РїСЂРµРґС‹РґСѓС‰РёС… results.
6. РџРѕР»СѓС‡Р°С‚СЊ actor/tenant/source РёР· РґРѕРІРµСЂРµРЅРЅРѕРіРѕ execution context route/service; РїСѓР±Р»РёС‡РЅС‹Рµ corrections РІСЃРµРіРґР° РёРјРµСЋС‚ `USER`, РїРѕРґРјРµРЅР° source role Рё cross-document target РѕС‚РєР»РѕРЅСЏРµС‚СЃСЏ, Р·Р°СЏРІР»РµРЅРЅР°СЏ import attribution РѕСЃС‚Р°С‘С‚СЃСЏ РЅРµРґРѕРІРµСЂРµРЅРЅРѕР№.
7. Р”РѕР±Р°РІРёС‚СЊ РѕС‚РґРµР»СЊРЅС‹Рµ РѕС‚ corrections РЅРµРёР·РјРµРЅСЏРµРјС‹Рµ grants Рё revocations consent, РІРµСЂСЃРёРѕРЅРёСЂРѕРІР°РЅРЅС‹Рµ РїРѕ purpose/scope/policy; export РїРѕРІС‚РѕСЂРЅРѕ Р°РІС‚РѕСЂРёР·СѓРµС‚СЃСЏ РїСЂРё РІС‹РїРѕР»РЅРµРЅРёРё.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂРµС€РµРЅРѕ РёР·РјРµРЅСЏС‚СЊ

Domain/application modules corrections/revisions, in-memory repositories, РѕС‚РЅРѕСЃСЏС‰РёРµСЃСЏ schemas Рё unit/property/integration tests; С„Р°РєС‚РёС‡РµСЃРєР°СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ РЅРµ РґРѕР»Р¶РЅС‹ РёР·РјРµРЅСЏС‚СЊСЃСЏ

Vendor adapter engine, РµСЃР»Рё РЅРµ РґРѕРєР°Р·Р°РЅ РґРµС„РµРєС‚ РєРѕРЅС‚СЂР°РєС‚Р°; persistent DB/REST; application projectors; СЃРµРјР°РЅС‚РёРєР° РѕР±РЅРѕРІР»РµРЅРёСЏ raw snapshot.

## РўРµСЃС‚С‹

Р’СЃРµ РѕРїРµСЂР°С†РёРё corrections, РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅРѕСЃС‚СЊ replay, СЃРѕС…СЂР°РЅРµРЅРёРµ raw hash, СѓСЃС‚Р°СЂРµРІС€Р°СЏ Рё РєРѕРЅРєСѓСЂРµРЅС‚РЅР°СЏ base, rollback, diff, ancestry split/merge, partial rerun, РїРѕРґРјРµРЅР° actor/source role/cross-document target Рё РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‰РёР№, РїРѕРґРґРµР»СЊРЅС‹Р№, СѓСЃС‚Р°СЂРµРІС€РёР№ РёР»Рё РѕС‚РѕР·РІР°РЅРЅС‹Р№ consent.

## РљРѕРЅС‚СЂРѕР»СЊ РєР°С‡РµСЃС‚РІР°

`AC-003`; property/replay/concurrency tests; reviewer РїРѕРґС‚РІРµСЂР¶РґР°РµС‚ РѕС‚СЃСѓС‚СЃС‚РІРёРµ РїСѓС‚Рё РёР·РјРµРЅРµРЅРёСЏ raw evidence Рё targets, РѕСЃРЅРѕРІР°РЅРЅС‹С… С‚РѕР»СЊРєРѕ РЅР° offsets.

## РћРїСЂРµРґРµР»РµРЅРёРµ РіРѕС‚РѕРІРЅРѕСЃС‚Рё

РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ РјРѕР¶РµС‚ РёСЃРїСЂР°РІРёС‚СЊ РёР»Рё РїРѕРґС‚РІРµСЂРґРёС‚СЊ token РёР»Рё line, РїСЂРѕСЃРјРѕС‚СЂРµС‚СЊ revisions Рё diff, РІС‹РїРѕР»РЅРёС‚СЊ rollback Рё РїРѕРІС‚РѕСЂРЅРѕ СЂР°СЃРїРѕР·РЅР°С‚СЊ scope, РїСЂРё СЌС‚РѕРј РІСЃРµ РїСЂРµРґС‹РґСѓС‰РёРµ raw/revisions РѕСЃС‚Р°СЋС‚СЃСЏ РґРѕСЃС‚СѓРїРЅС‹РјРё, Р° provenance actor/consent вЂ” РґРѕРІРµСЂРµРЅРЅС‹Рј Рё РїСЂРёРіРѕРґРЅС‹Рј РґР»СЏ Р°СѓРґРёС‚Р°.

## РљСЂРёС‚РµСЂРёРё РїСЂРёС‘РјРєРё

Raw hash РЅРµ РёР·РјРµРЅСЏРµС‚СЃСЏ; hash replay СЃС‚Р°Р±РёР»РµРЅ; СѓСЃС‚Р°СЂРµРІС€Р°СЏ base СЃРѕРѕР±С‰Р°РµС‚СЃСЏ СЏРІРЅРѕ; РЅРѕРІС‹Рµ СЃС‚СЂСѓРєС‚СѓСЂРЅС‹Рµ IDs СЃРІСЏР·Р°РЅС‹ СЃ ancestry; РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ РґР»СЏ training/export С‚СЂРµР±СѓРµС‚ РґРµР№СЃС‚РІСѓСЋС‰РёР№ РѕС‚Р·С‹РІР°РµРјС‹Р№ grant Рё РѕСЃС‚Р°С‘С‚СЃСЏ opt-in.

## РћР¶РёРґР°РµРјС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹

Services Рё schemas corrections/revisions, in-memory implementation, replay/property tests Рё РѕР±РЅРѕРІР»С‘РЅРЅС‹Рµ status/log.

## РЈСЃР»РѕРІРёСЏ РѕСЃС‚Р°РЅРѕРІРєРё Рё РѕС‚РєР°С‚Р°

РћСЃС‚Р°РЅРѕРІРёС‚СЊСЃСЏ РїСЂРё РЅРµРґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅРѕРј replay, РЅРµРѕРґРЅРѕР·РЅР°С‡РЅРѕР№ target identity, РїРѕС‚РµСЂСЏРЅРЅРѕРј РєРѕРЅРєСѓСЂРµРЅС‚РЅРѕРј РѕР±РЅРѕРІР»РµРЅРёРё РёР»Рё Р»СЋР±РѕР№ РїРµСЂРµР·Р°РїРёСЃРё raw. РћС‚РјРµРЅРёС‚СЊ commit СЌС‚Р°РїР°; persistent migration РµС‰С‘ РЅРµ СЃСѓС‰РµСЃС‚РІСѓРµС‚.


## stage-04-storage-jobs-api
# Р­С‚Р°Рї 04 вЂ” Р›РѕРєР°Р»СЊРЅРѕРµ persistence, jobs Рё REST API

## Р¦РµР»СЊ

РЎРґРµР»Р°С‚СЊ Р·Р°РІРµСЂС€С‘РЅРЅС‹Рµ use cases Core РґРѕР»РіРѕРІРµС‡РЅС‹РјРё Рё Р°СЃРёРЅС…СЂРѕРЅРЅРѕ РґРѕСЃС‚СѓРїРЅС‹РјРё РІ local/offline deployment profile.

## РћР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚

Р Р°Р·РґРµР»С‹ SPEC 37вЂ“59 Рё `FR-007`, `FR-009`, `SEC-002`, `SEC-003`, `SEC-005`; storage/jobs Р°СЂС…РёС‚РµРєС‚СѓСЂС‹; endpoints, errors Рё idempotency API; РёРЅРІР°СЂРёР°РЅС‚С‹ РґР°РЅРЅС‹С…; security model; ADR-006/009.

## Р—Р°РІРёСЃРёРјРѕСЃС‚Рё

РџСЂРёРЅСЏС‚С‹ СЌС‚Р°РїС‹ 01вЂ“03 Рё СЃС‚Р°Р±РёР»СЊРЅС‹Рµ schemas. Р”Рѕ Р»СЋР±РѕР№ РїРѕСЃС‚РѕСЏРЅРЅРѕР№ Р·Р°РїРёСЃРё РїРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРёС… РґР°РЅРЅС‹С… РЅРµРѕР±С…РѕРґРёРјРѕ РїСЂРёРЅСЏС‚СЊ ADR-P03, РѕРїСЂРµРґРµР»СЏСЋС‰РёР№ local retention, permissions/encryption, SLA СѓРґР°Р»РµРЅРёСЏ, РѕС‡РёСЃС‚РєСѓ temp/crash Рё РїРѕРІРµРґРµРЅРёРµ logs/audit/rotation/export/backups.

## РћР±Р»Р°СЃС‚СЊ

Metadata SQLite, Р°С‚РѕРјР°СЂРЅС‹Рµ blobs С„Р°Р№Р»РѕРІРѕР№ СЃРёСЃС‚РµРјС‹, unit-of-work, migrations Рё recovery, РїРѕСЃС‚РѕСЏРЅРЅС‹Р№ local worker, idempotency/progress/cancel/cache Рё REST adapter FastAPI. Р‘РµР· remote/multi-tenant profile.

## Р—Р°РґР°С‡Рё

1. РџСЂРёРЅСЏС‚СЊ ADR-P03, Р·Р°С‚РµРј РѕРїСЂРµРґРµР»РёС‚СЊ РѕР±СЂР°С‚РёРјС‹Рµ schema migrations Рё adapters repository/blob/cache СЃ РїСЂР°РІРёР»Р°РјРё retention/deletion/reference count.
2. Р РµР°Р»РёР·РѕРІР°С‚СЊ РґРѕР»РіРѕРІРµС‡РЅС‹Р№ state machine jobs, attempts, checkpoints cancellation Рё СѓС‡С‘С‚ СЂРµСЃСѓСЂСЃРѕРІ.
3. Р РµР°Р»РёР·РѕРІР°С‚СЊ РґРІСѓС…СѓСЂРѕРІРЅРµРІСѓСЋ idempotency identity `(tenant, principal, operation, key) в†’ request hash/result`; РґСЂСѓРіРѕР№ hash РІС‹Р·С‹РІР°РµС‚ conflict Р±РµР· СЃРѕР·РґР°РЅРёСЏ РІС‚РѕСЂРѕРіРѕ job. РћС‚РґРµР»СЊРЅРѕ СЂРµР°Р»РёР·РѕРІР°С‚СЊ scoped recognition cache Рё РїРѕРІС‚РѕСЂРЅРѕ Р°РІС‚РѕСЂРёР·РѕРІР°С‚СЊ РєР°Р¶РґС‹Р№ lookup.
4. Р”РѕР±Р°РІРёС‚СЊ handlers REST v1 РєР°Рє С‚РѕРЅРєРёРµ application adapters СЃ Р±РµР·РѕРїР°СЃРЅС‹РјРё errors Рё pagination; РІС‹РїРѕР»РЅСЏС‚СЊ bind С‚РѕР»СЊРєРѕ РЅР° loopback/local IPC, СЃРѕР·РґР°РІР°С‚СЊ credential РІС‹СЃРѕРєРѕР№ СЌРЅС‚СЂРѕРїРёРё С‡РµСЂРµР· РїСЂРёРІР°С‚РЅС‹Р№ permission-checked file РёР»Рё OS store, РЅРѕ РЅРµ CLI РёР»Рё loggable env, РїСЂРѕРІРµСЂСЏС‚СЊ Р·Р° РїРѕСЃС‚РѕСЏРЅРЅРѕРµ РІСЂРµРјСЏ, РїРѕРґРґРµСЂР¶РёРІР°С‚СЊ rotate/revoke, Р·Р°РІРµСЂС€Р°С‚СЊ Р·Р°РїСѓСЃРє Р·Р°РєСЂС‹С‚С‹Рј РѕС‚РєР°Р·РѕРј РїСЂРё РЅРµР±РµР·РѕРїР°СЃРЅРѕРј storage, Р·Р°РїСЂРµС‰Р°С‚СЊ CORS/cookies Рё РѕС‚РєР°Р·С‹РІР°С‚СЊ РІ non-loopback Р±РµР· remote gate.
5. Р’ `LOCAL_ONLY` Р·Р°РїСЂРµС‰Р°С‚СЊ РІРµСЃСЊ egress, РІРєР»СЋС‡Р°СЏ telemetry, fallback Рё update checks.
6. РџСЂРёРјРµРЅСЏС‚СЊ quotas request/output/disk/queue/cardinality Рё РїСЂРёРЅСЏС‚С‹Р№ lifecycle retention/deletion/backup/observability; РїСЂРѕРІРµСЂРёС‚СЊ crash consistency Рё СѓРґР°Р»РµРЅРёРµ shared blobs.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂРµС€РµРЅРѕ РёР·РјРµРЅСЏС‚СЊ

Infrastructure adapters/migrations, jobs, REST interface, deployment/test config, integration/security/API compatibility tests Рё РѕС‚РЅРѕСЃСЏС‰РёРµСЃСЏ РґРѕРєСѓРјРµРЅС‚С‹.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ РЅРµ РґРѕР»Р¶РЅС‹ РёР·РјРµРЅСЏС‚СЊСЃСЏ

РЎРµРјР°РЅС‚РёРєР° domain Р±РµР· РѕР±РЅРѕРІР»РµРЅРёСЏ ADR/SPEC; remote auth Рё multi-tenant deployment; CLI/MCP; projectors consumers.

## РўРµСЃС‚С‹

Migration up/down/recovery, С‚СЂР°РЅР·Р°РєС†РёРё Рё СѓРґР°Р»РµРЅРёРµ atomic/shared blobs Рё `AC-011`, РїРµСЂРµС…РѕРґС‹ jobs, retry/cancel, idempotency РѕРґРёРЅР°РєРѕРІРѕРіРѕ key СЃ РѕРґРёРЅР°РєРѕРІС‹Рј Рё СЂР°Р·Р»РёС‡РЅС‹Рј hash СЃ РґРѕРєР°Р·Р°С‚РµР»СЊСЃС‚РІРѕРј РѕС‚СЃСѓС‚СЃС‚РІРёСЏ duplicate job, collisions РѕС‚РґРµР»СЊРЅРѕ scoped cache Рё invalidation СѓРґР°Р»С‘РЅРЅРѕРіРѕ document, REST schema/errors/pagination, permissions/bootstrap/rotation/revocation/redaction token-file, РѕС‚РєР°Р· wildcard bind, missing/wrong credentials Рё hostile Origin, amplification request/output/disk/queue, no-egress, rotation/access/retention log/audit Рё leakage telemetry.

## РљРѕРЅС‚СЂРѕР»СЊ РєР°С‡РµСЃС‚РІР°

`AC-008`, `AC-009`, `AC-011`; security review; РїСЂРѕС…РѕРґСЏС‚ integration/compatibility tests; ADR-P03 РїСЂРёРЅСЏС‚ РґРѕ РїРѕСЃС‚РѕСЏРЅРЅС‹С… Р·Р°РїРёСЃРµР№; injection failure РЅРµ РѕСЃС‚Р°РІР»СЏРµС‚ РІРёРґРёРјРѕРіРѕ dangling state; Р°РІС‚РѕСЂРёР·РѕРІР°РЅРЅРѕРµ СѓРґР°Р»РµРЅРёРµ СЃРѕР±Р»СЋРґР°РµС‚ SLA РґР»СЏ РІСЃРµС… retention classes; РЅРµС‚ СѓС‚РµС‡РµРє stack/path/content; non-loopback startup Р·Р°РїСЂРµС‰С‘РЅ Р±РµР· remote gate.

## РћРїСЂРµРґРµР»РµРЅРёРµ РіРѕС‚РѕРІРЅРѕСЃС‚Рё

Р›РѕРєР°Р»СЊРЅС‹Р№ client РјРѕР¶РµС‚ С‡РµСЂРµР· REST РѕС‚РїСЂР°РІРёС‚СЊ, РѕС‚СЃР»РµР¶РёРІР°С‚СЊ, РѕС‚РјРµРЅРёС‚СЊ Рё РїРѕР»СѓС‡РёС‚СЊ persistent result СЂР°СЃРїРѕР·РЅР°РІР°РЅРёСЏ РёР»Рё correction СЃ СЃРѕСЃС‚РѕСЏРЅРёРµРј, РїРµСЂРµР¶РёРІР°СЋС‰РёРј restart, Рё РїСЂРёРЅСѓРґРёС‚РµР»СЊРЅРѕ РїСЂРёРјРµРЅСЏРµРјРѕР№ offline privacy.

## РљСЂРёС‚РµСЂРёРё РїСЂРёС‘РјРєРё

`FR-007`, `FR-009`, `AC-004`, `AC-011`; СЃРµРјР°РЅС‚РёРєР° duplicate key Рё terminal states СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ API; retention classes source/raw/revision РѕСЃС‚Р°СЋС‚СЃСЏ СЂР°Р·РґРµР»С‘РЅРЅС‹РјРё; Р°РІС‚РѕСЂРёР·РѕРІР°РЅРЅРѕРµ СѓРґР°Р»РµРЅРёРµ РїРѕР»РЅРѕ, Р° preprocessing/corrections РЅРµ РјРѕРіСѓС‚ РµРіРѕ РёРЅРёС†РёРёСЂРѕРІР°С‚СЊ.

## РћР¶РёРґР°РµРјС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹

Migrations, local adapters/worker, REST v1/OpenAPI, recovery/security tests, operating notes Рё РѕР±РЅРѕРІР»РµРЅРёСЏ status/log.

## РЈСЃР»РѕРІРёСЏ РѕСЃС‚Р°РЅРѕРІРєРё Рё РѕС‚РєР°С‚Р°

РћСЃС‚Р°РЅРѕРІРёС‚СЊСЃСЏ РїСЂРё РЅРµРѕР±СЂР°С‚РёРјРѕР№ migration, РІРёРґРёРјС‹С… РїРѕСЃР»Рµ crash С‡Р°СЃС‚РёС‡РЅС‹С… writes, РЅРµРѕРіСЂР°РЅРёС‡РµРЅРЅРѕРј worker, privacy egress РёР»Рё РЅРµР±РµР·РѕРїР°СЃРЅРѕРј external bind. Р’РѕСЃСЃС‚Р°РЅРѕРІРёС‚СЊ backup DB РґРѕ СЌС‚Р°РїР° Рё РѕС‚РјРµРЅРёС‚СЊ code/migration; РЅРµ РІРєР»СЋС‡Р°С‚СЊ remote mode.


## stage-05-application-adapters
# Р­С‚Р°Рї 05 вЂ” Adapters РїСЂРёР»РѕР¶РµРЅРёР№

## Р¦РµР»СЊ

РџРѕРґРєР»СЋС‡РёС‚СЊ С‚СЂС‘С… РїРµСЂРІРѕРЅР°С‡Р°Р»СЊРЅС‹С… consumers С‡РµСЂРµР· РѕС‚РґРµР»СЊРЅС‹Рµ input profiles Рё output projectors СЃ РїРѕР»РЅС‹Рј provenance Рё Р±РµР· СѓС‚РµС‡РєРё РґРѕРјРµРЅР° Core.

## РћР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚

Р Р°Р·РґРµР»С‹ SPEC 24, 33вЂ“36, 67, 82вЂ“83 Рё `FR-008`, `AC-006`; `docs/INTEGRATIONS.md`, РєРѕРЅС‚СЂР°РєС‚С‹ result/data Рё СЃС‚СЂР°С‚РµРіРёСЏ integration tests; ADR-008.

## Р—Р°РІРёСЃРёРјРѕСЃС‚Рё

РЎС‚Р°Р±РёР»СЊРЅС‹Р№ API recognition/revision РёР· СЌС‚Р°РїРѕРІ 01вЂ“04.

## РћР±Р»Р°СЃС‚СЊ

Integration packages/contracts Рё СЃРёРЅС‚РµС‚РёС‡РµСЃРєРёРµ fixtures adapters РґР»СЏ Personal Chronicle, Receipt Scanner Рё Tutor. РР·РјРµРЅРµРЅРёСЏ РїСЂРёР»РѕР¶РµРЅРёР№-consumers С‚СЂРµР±СѓСЋС‚ РѕС‚РґРµР»СЊРЅС‹С… Р·Р°РґР°С‡ РІ РёС… СЂРµРїРѕР·РёС‚РѕСЂРёСЏС….

## Р—Р°РґР°С‡Рё

1. Р РµР°Р»РёР·РѕРІР°С‚СЊ РѕР±С‰РёР№ РєРѕРЅС‚СЂР°РєС‚ profile/projector Рё validation version/provenance.
2. Р РµР°Р»РёР·РѕРІР°С‚СЊ РїСЂРѕРµРєС†РёСЋ Chronicle Р±РµР· Р»РѕРіРёРєРё RAG/timeline/summary.
3. Р РµР°Р»РёР·РѕРІР°С‚СЊ РїСЂРѕРµРєС†РёСЋ extraction С‡РµРєРѕРІ СЃРѕ СЃСЃС‹Р»РєР°РјРё amount/item/source Рё СЏРІРЅРѕР№ РЅРµРѕРґРЅРѕР·РЅР°С‡РЅРѕСЃС‚СЊСЋ.
4. Р РµР°Р»РёР·РѕРІР°С‚СЊ РїСЂРѕРµРєС†РёСЋ regions Tutor Р±РµР· Р»РѕРіРёРєРё student/grading/solution.
5. Р”РѕР±Р°РІРёС‚СЊ РїСЂРѕРІРµСЂРєРё dependencies, Р·Р°РїСЂРµС‰Р°СЋС‰РёРµ entities/services consumers РІРЅСѓС‚СЂРё Core.
6. РћРїСѓР±Р»РёРєРѕРІР°С‚СЊ РїСЂРёРјРµСЂ РїРѕРґРєР»СЋС‡РµРЅРёСЏ С‡РµС‚РІС‘СЂС‚РѕРіРѕ consumer С‡РµСЂРµР· СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ contracts.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂРµС€РµРЅРѕ РёР·РјРµРЅСЏС‚СЊ

Integration packages, РїСЂРёРЅР°РґР»РµР¶Р°С‰РёРµ РёРј schemas, СЃРёРЅС‚РµС‚РёС‡РµСЃРєРёРµ fixtures, adapter/contract tests Рё РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ РёРЅС‚РµРіСЂР°С†РёР№.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ РЅРµ РґРѕР»Р¶РЅС‹ РёР·РјРµРЅСЏС‚СЊСЃСЏ

Vocabulary РґРѕРјРµРЅР° Core, СЃРµРјР°РЅС‚РёРєР° OCR pipeline Рё corrections, СЂРµРїРѕР·РёС‚РѕСЂРёРё consumers, РїСЂРёРІР°С‚РЅС‹Рµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊСЃРєРёРµ РґР°РЅРЅС‹Рµ Рё РЅРµРїРѕРґРґРµСЂР¶РёРІР°РµРјС‹Рµ math/business features.

## РўРµСЃС‚С‹

Р”РµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹Рµ projections, РїРѕРєСЂС‹С‚РёРµ provenance, РїРѕР»СЏ low-confidence/missing/ambiguous, privacy profiles, schema versioning Рё РїСЂРѕРІРµСЂРєРё Р·Р°РїСЂРµС‰С‘РЅРЅС‹С… dependencies/imports.

## РљРѕРЅС‚СЂРѕР»СЊ РєР°С‡РµСЃС‚РІР°

`AC-006`; 100% Р·Р°РїРѕР»РЅРµРЅРЅС‹С… РїСЂРѕРёР·РІРѕРґРЅС‹С… РїРѕР»РµР№ РёРјРµСЋС‚ РґРµР№СЃС‚РІСѓСЋС‰РёРµ source references РёР»Рё СЏРІРЅС‹Р№ derived provenance; РІ integrations РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ РїСЂСЏРјРѕР№ OCR SDK; РІ Core РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‚ business services consumers.

## РћРїСЂРµРґРµР»РµРЅРёРµ РіРѕС‚РѕРІРЅРѕСЃС‚Рё

Р’СЃРµ С‚СЂРё projections РїСЂРёРЅРёРјР°СЋС‚ РѕРґРёРЅ СЃС‚Р°Р±РёР»СЊРЅС‹Р№ result, Р° РїСЂРёРјРµСЂ РЅРѕРІРѕРіРѕ consumer РґРѕР±Р°РІР»СЏРµС‚СЃСЏ Р±РµР· РёР·РјРµРЅРµРЅРёСЏ contracts Core.

## РљСЂРёС‚РµСЂРёРё РїСЂРёС‘РјРєРё

РЎСѓРјРјС‹ С‡РµРєР° С‚СЂР°СЃСЃРёСЂСѓСЋС‚СЃСЏ Рє tokens/regions, Chronicle РїРѕРґРґРµСЂР¶РёРІР°РµС‚ `LOCAL_ONLY`, Tutor СЏРІРЅРѕ РґРµРіСЂР°РґРёСЂСѓРµС‚ РЅРµРїРѕРґРґРµСЂР¶РёРІР°РµРјСѓСЋ РЅРµРѕР±СЏР·Р°С‚РµР»СЊРЅСѓСЋ capability, Р° mapping adapter РЅРёРєРѕРіРґР° РЅРµ РїРµСЂРµР·Р°РїРёСЃС‹РІР°РµС‚ raw text.

## РћР¶РёРґР°РµРјС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹

РўСЂРё РІРµСЂСЃРёРѕРЅРёСЂРѕРІР°РЅРЅС‹С… integration packages/contracts, СЃРёРЅС‚РµС‚РёС‡РµСЃРєРёРµ fixtures/tests, РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ onboarding Рё РѕР±РЅРѕРІР»РµРЅРёРµ status/log.

## РЈСЃР»РѕРІРёСЏ РѕСЃС‚Р°РЅРѕРІРєРё Рё РѕС‚РєР°С‚Р°

РћСЃС‚Р°РЅРѕРІРёС‚СЊСЃСЏ, РµСЃР»Рё projection С‚СЂРµР±СѓРµС‚ business logic consumer РІРЅСѓС‚СЂРё Core РёР»Рё РЅРµРІРµСЂСЃРёРѕРЅРёСЂРѕРІР°РЅРЅРѕРіРѕ РёР·РјРµРЅРµРЅРёСЏ public contract. РћС‚РјРµРЅРёС‚СЊ С‚РѕР»СЊРєРѕ Р·Р°С‚СЂРѕРЅСѓС‚С‹Р№ integration package; Core РѕСЃС‚Р°С‘С‚СЃСЏ РїСЂРёРіРѕРґРЅС‹Рј РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ.


## stage-06-quality-hardening
# Р­С‚Р°Рї 06 вЂ” HTR, mixed routing Рё СѓРєСЂРµРїР»РµРЅРёРµ РєР°С‡РµСЃС‚РІР°

## Р¦РµР»СЊ

Р”РѕР±Р°РІРёС‚СЊ РѕСЃРЅРѕРІР°РЅРЅРѕРµ РЅР° РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏС… СЂР°СЃРїРѕР·РЅР°РІР°РЅРёРµ handwriting/mixed Рё Р·Р°РІРµСЂС€РёС‚СЊ privacy, security, regression Рё performance gates РґР»СЏ review MVP Core.

## РћР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ РєРѕРЅС‚РµРєСЃС‚

Р Р°Р·РґРµР»С‹ SPEC 29вЂ“32, 41вЂ“50, 59вЂ“66 Рё `NFR-001`, `NFR-003`вЂ“`NFR-005`, `SEC-001`вЂ“`SEC-010`, `PERF-001`, `AC-004`вЂ“`AC-011`; СЃС‚СЂР°С‚РµРіРёСЏ security/testing; РѕР¶РёРґР°СЋС‰РёРµ ADR-P04вЂ“P05. ADR-P03 РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СѓР¶Рµ РїСЂРёРЅСЏС‚ РЅР° СЌС‚Р°РїРµ 04.

## Р—Р°РІРёСЃРёРјРѕСЃС‚Рё

РџСЂРёРЅСЏС‚С‹ СЌС‚Р°РїС‹ 01вЂ“05; СЃСѓС‰РµСЃС‚РІСѓРµС‚ СЂРµРїСЂРµР·РµРЅС‚Р°С‚РёРІРЅС‹Р№ СЂР°Р·СЂРµС€С‘РЅРЅС‹Р№ golden dataset handwriting/mixed.

## РћР±Р»Р°СЃС‚СЊ

Benchmark Рё РІС‹Р±РѕСЂ HTR-РєР°РЅРґРёРґР°С‚РѕРІ, routing OCR/HTR РЅР° СѓСЂРѕРІРЅРµ regions, thresholds fallback/review, calibration, РїРѕР»РЅР°СЏ СЂРµРіСЂРµСЃСЃРёСЏ hostile input, privacy, quality Рё performance Рё evidence СЂРµР»РёР·Р°. Р‘РµР· training/personalization/ensemble.

## Р—Р°РґР°С‡Рё

1. Р’РµСЂСЃРёРѕРЅРёСЂРѕРІР°С‚СЊ dataset handwriting/mixed Рё РїСЂРµРґРѕС‚РІСЂР°С‚РёС‚СЊ leakage Рё private content.
2. Р’С‹РїРѕР»РЅРёС‚СЊ benchmark HTR-РєР°РЅРґРёРґР°С‚РѕРІ Рё РїСЂРёРЅСЏС‚СЊ РёР»Рё РѕС‚Р»РѕР¶РёС‚СЊ ADR-P05 РїРѕ РїРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏРј.
3. Р РµР°Р»РёР·РѕРІР°С‚СЊ РІС‹Р±СЂР°РЅРЅС‹Р№ adapter Рё mixed routing regions С‚РѕР»СЊРєРѕ РїСЂРё РїСЂРѕС…РѕР¶РґРµРЅРёРё gates.
4. РћС‚РєР°Р»РёР±СЂРѕРІР°С‚СЊ thresholds review Рё РїСЂРёРЅСЏС‚СЊ ADR-P04 РїРѕ evidence РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ dataset.
5. Р—Р°РІРµСЂС€РёС‚СЊ С‚РµСЃС‚С‹ no-egress, lifecycle leakage/observability, hostile corpus, isolation worker, supply chain, consent, identity/scope, resources/amplification Рё cancellation.
6. РџРѕРґРіРѕС‚РѕРІРёС‚СЊ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹Р№ РѕС‚С‡С‘С‚ MVP benchmark/security/compatibility Рё review РіРѕС‚РѕРІРЅРѕСЃС‚Рё СЂРµР»РёР·Р°.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂРµС€РµРЅРѕ РёР·РјРµРЅСЏС‚СЊ

HTR engine adapter/routing, СЂР°Р·СЂРµС€С‘РЅРЅС‹Рµ fixtures/manifests, benchmark/security/performance tests Рё reports, configuration thresholds Рё РѕС‚РЅРѕСЃСЏС‰РёРµСЃСЏ ADR/status docs.

## Р¤Р°Р№Р»С‹, РєРѕС‚РѕСЂС‹Рµ РЅРµ РґРѕР»Р¶РЅС‹ РёР·РјРµРЅСЏС‚СЊСЃСЏ

Training/fine-tuning, user personalization, ensemble/LLM, remote deployment, business logic consumers Рё private datasets.

## РўРµСЃС‚С‹

РћР±С‰РёР№ contract suite engine, golden metrics HTR/mixed, calibration confidence, routing/fallback regions, partial rerun, no-egress, hostile corpus, cancellation/resource limits, telemetry canary Рё РїРѕР»РЅР°СЏ РѕС‚РЅРѕСЃСЏС‰Р°СЏСЃСЏ regression.

## РљРѕРЅС‚СЂРѕР»СЊ РєР°С‡РµСЃС‚РІР°

Security Рё performance reviews; РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅС‹ dataset, versions Рё environment; СЃРѕРіР»Р°СЃРѕРІР°РЅРЅС‹Рµ С‡РёСЃР»РµРЅРЅС‹Рµ thresholds РїСЂРѕС…РѕРґСЏС‚; РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ regression СЃРІРµСЂС… СЂР°Р·СЂРµС€С‘РЅРЅРѕРіРѕ tolerance; СЃРІСЏР·Р°РЅС‹ РІСЃРµ evidence РґР»СЏ `SEC-001`вЂ“`SEC-010` Рё `AC-004`вЂ“`AC-011` РІ С‚РµРєСѓС‰РµР№ РѕР±Р»Р°СЃС‚Рё.

## РћРїСЂРµРґРµР»РµРЅРёРµ РіРѕС‚РѕРІРЅРѕСЃС‚Рё

Core MVP РїРѕРґРґРµСЂР¶РёРІР°РµС‚ РєР°Рє РјРёРЅРёРјСѓРј РѕРґРёРЅ OCR adapter Рё РєРѕРЅС‚СЂР°РєС‚ HTR; РІС‹Р±СЂР°РЅРЅС‹Р№ runtime HTR/mixed РІРєР»СЋС‡Р°РµС‚СЃСЏ С‚РѕР»СЊРєРѕ РїСЂРё РїСЂРѕС…РѕР¶РґРµРЅРёРё evidence. Release report СЏРІРЅРѕ РїРѕРєР°Р·С‹РІР°РµС‚ РЅРµРїРѕРґРґРµСЂР¶РёРІР°РµРјС‹Рµ Рё РѕС‚Р»РѕР¶РµРЅРЅС‹Рµ capabilities.

## РљСЂРёС‚РµСЂРёРё РїСЂРёС‘РјРєРё

`AC-004`, `AC-005`; local-only mixed job РЅРµ РёРјРµРµС‚ egress; РЅРёР·РєРёР№ confidence РїСЂРёРІРѕРґРёС‚ Рє review-required; results РѕСЃС‚Р°СЋС‚СЃСЏ РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјС‹РјРё Рё traceable.

## РћР¶РёРґР°РµРјС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹

HTR/mixed adapter РёР»Рё СЏРІРЅРѕРµ РѕС‚Р»РѕР¶РµРЅРЅРѕРµ РїРѕ evidence СЂРµС€РµРЅРёРµ, РїСЂРёРЅСЏС‚С‹Р№ ADR thresholds, benchmark/security reports, release checklist Рё РѕР±РЅРѕРІР»РµРЅРёРµ status/log.

## РЈСЃР»РѕРІРёСЏ РѕСЃС‚Р°РЅРѕРІРєРё Рё РѕС‚РєР°С‚Р°

Р•СЃР»Рё РЅРё РѕРґРёРЅ HTR-РєР°РЅРґРёРґР°С‚ РЅРµ РїСЂРѕС…РѕРґРёС‚ gates, СЃРѕС…СЂР°РЅРёС‚СЊ port/contract HTR Рё СЏРІРЅРѕ РѕС‚Р»РѕР¶РёС‚СЊ runtime support; РЅРµ СЃРЅРёР¶Р°С‚СЊ thresholds Рё РЅРµ РІС‹РїСѓСЃРєР°С‚СЊ СЃР»Р°Р±С‹Р№ adapter. РћС‚РјРµРЅРёС‚СЊ РІРєР»СЋС‡РµРЅРёРµ Рё config adapter, СЃРѕС…СЂР°РЅРёРІ evidence benchmark.
