# TRC-NIGHT-JSON-DUPLICATE-01 — однозначный JSON boundary

Status: accepted bounded security repair under NIGHT FACTORY; requirement owners SEC-001, SEC-002, SEC-003 and AC-001 in system.spec.md. This clarifies the existing strict public byte-boundary contract; no engine, transport or egress is activated.

- Public `parse_request_json` and `parse_result_json` reject repeated JSON object member names at every nesting level before model construction. Equality applies to decoded member names, including escaped spellings. A repeated privacy_mode cannot silently replace LOCAL_ONLY with REMOTE_ALLOWED. Unknown-member duplicates also fail closed.
- Existing byte limits, models, generated schemas and valid-input semantics remain unchanged. Use a bounded standard-library syntax/member preflight, then the existing Pydantic JSON validation path; do not replace JSON-specific validation with Python-object coercion.
- Duplicate-member failures expose only `duplicate_json_key`. Syntax, encoding, bounded integer-conversion or preflight recursion failures expose only `json_invalid`; input names, values, private paths and raw decoder/Pydantic errors must not appear in public errors.
- Existing accepted tests remain unchanged. Add request root/nested/escaped duplicate cases, result root/nested duplicates, valid-boundary roundtrip, malformed encoding/syntax and deep-input redaction checks.
- Required evidence: focused boundary regressions, full existing suite, Ruff and strict mypy; synthetic local parser tests prove this boundary only. Stage 02 decoder/worker/benchmark/engine-choice gates remain PARTIAL.

Models may still be constructed internally using their model APIs; an untrusted adapter must use the public bounded parse entrypoints rather than bypass them. No future adapter is declared implemented here.
