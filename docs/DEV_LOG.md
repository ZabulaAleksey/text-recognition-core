# Development log

## 2026-08-13 — KАРКАС bootstrap

- Read `Определение для Codex.md`, full source `SPEC.md`, workspace routing/SDD/domain rules and active AI Dev Team capabilities.
- Performed read-only architecture and global overlay audits.
- Verified GitHub repository `ZabulaAleksey/text-recognition-core` exists, is empty, uses `main` and grants push/admin permissions.
- Initialized a standalone Git repository, created `docs/project-skeleton` and configured `origin`.
- Moved the canonical specification to `specs/system.spec.md`, added stable requirement/acceptance IDs and created the project KАРКАС documents.
- Resolved workspace conflicts: `AI_STATUS` instead of `PROGRESS`, `AI_PLAN` separate from prompt library, canonical docs paths, no duplicate AI infrastructure.
- Chose a contract-first Python baseline; deferred OCR/HTR and binary-decoder choices to evidence gates.
- Created no product source code and performed no push/merge.

### Notable issue

Git initially rejected the newly initialized nested repository because sandbox and Windows directory owners differ. Subsequent local commands use a repository-specific `safe.directory` command option; no global Git setting was changed.

### Planned verification

Completed verification:

- all relative Markdown links resolve;
- every one of six stage prompts contains all 13 required sections;
- only one status/source file candidate exists (`docs/AI_STATUS.md`); no obsolete canonical layout blocks remain;
- requirement registry contains 37 stable IDs;
- independent reviewer returned `PASS` after dependency allowlist, canonical naming, batch/rerun/rollback/correction/revision API and empty-repository workflow fixes;
- independent security reviewer returned `PASS` after isolation, amplification, local identity, actor/consent, supply-chain, retention/deletion, cache/idempotency and SSRF gates were made explicit;
- no product `src/`, dependencies, runtime or private fixtures were created.
