# AI status

**Updated:** 2026-08-13

**Phase:** architecture/design bootstrap complete; implementation not started.

**Branch:** `docs/project-skeleton`.

## Implemented

- Standalone Git repository initialized; `origin` points to `https://github.com/ZabulaAleksey/text-recognition-core.git`.
- Full KАРКАС created from the source SPEC: canonical requirements, architecture, API/data/integration contracts, decisions, security/testing strategy, roadmap and stage prompts.
- Thin project `AGENTS.md` and context compatibility audit reuse the global AI Dev Team without local duplicate agents/hooks/Skills/MCP/config.
- Stable requirement/acceptance IDs appended to the system SPEC.

## Not implemented

- No Python package, REST API, storage, jobs, OCR/HTR engine, adapters or UI exists.
- No OCR/HTR engine has been selected; selection requires the Stage 02 golden benchmark.
- Remote deployment is not allowed until its security decisions/gates are complete; local REST is loopback/local-credential only.

## Known questions / debt

- Golden datasets and numerical quality/performance thresholds do not yet exist.
- PDF/image libraries, OCR baseline, HTR engine, concrete local retention/encryption and remote profile remain pending ADRs. Decoder isolation, supply-chain integrity and local-service identity are already mandatory decisions.
- Source `Определение для Codex.md` is retained as a bootstrap brief; workspace canonical terminology is `docs/PROJECT_FRAMEWORK.md`.

## Blockers

No technical blocker for Stage 01. Because the remote repository is empty, the first publication has no merge base: after the initial KАРКАС commit a local `main` ref will point to that same commit while work remains on `docs/project-skeleton`. Push still requires explicit user permission. Later feature branches follow normal review/merge flow.

## Next recommended action

Review the KАРКАС, then run `prompts/stage-01-foundation.md`. The bounded current slice is summarized in `docs/AI_PLAN.md`.
