# Stage 04 — Local persistence, jobs and REST API

## Goal

Make completed Core use cases durable and asynchronously accessible in a local/offline deployment profile.

## Required context

SPEC sections 37–59 and `FR-007`, `FR-009`, `SEC-002`, `SEC-003`, `SEC-005`; architecture storage/jobs; API endpoints/errors/idempotency; data invariants; security model; ADR-006/009.

## Dependencies

Stages 01–03 accepted and stable schemas. Before any persistent user-data write, accept ADR-P03 defining local retention, permissions/encryption, deletion SLA, temp/crash cleanup, logs/audit/rotation/export and backup behavior.

## Scope

SQLite metadata, atomic filesystem blobs, unit-of-work/migrations/recovery, persistent local worker, idempotency/progress/cancel/cache and FastAPI REST adapter. No remote/multi-tenant profile.

## Tasks

1. Accept ADR-P03, then define reversible schema migrations and repository/blob/cache adapters with retention/deletion/reference-count rules.
2. Implement durable job state machine, attempts, cancellation checkpoints and resource accounting.
3. Implement two-level idempotency identity `(tenant, principal, operation, key) → request hash/result`; different hash conflicts without a second job. Implement separately scoped recognition cache and re-authorize every lookup.
4. Add REST v1 handlers as thin application adapters with safe errors/pagination; bind loopback/local IPC only, bootstrap a high-entropy credential via private permission-checked file/OS store (never CLI/loggable env), constant-time verify, rotate/revoke, fail closed on insecure storage, deny CORS/cookies and refuse non-loopback without remote gate.
5. Make `LOCAL_ONLY` deny all egress, including telemetry/fallback/update checks.
6. Enforce request/output/disk/queue/cardinality quotas and the accepted retention/deletion/backup/observability lifecycle; validate crash consistency and shared-blob deletion.

## Files allowed to change

Infrastructure adapters/migrations, jobs, REST interface, deployment/test config, integration/security/API compatibility tests and relevant docs.

## Files that should not change

Domain semantics without ADR/SPEC update; remote auth/multi-tenant deployment; CLI/MCP; consumer projectors.

## Tests

Migration up/down/recovery, atomic/shared blob transaction/deletion and `AC-011`, job transitions/retry/cancel, same-key same/different-hash idempotency with proof no duplicate job, separately scoped cache collisions/deleted-document invalidation, REST schema/errors/pagination, token-file permissions/bootstrap/rotation/revocation/redaction, wildcard bind/missing-wrong credential/hostile Origin denial, request/output/disk/queue amplification, no-egress, log/audit rotation/access/retention and telemetry leakage.

## Quality gates

`AC-008`, `AC-009`, `AC-011`; security review; integration/compatibility tests pass; ADR-P03 accepted before persistent writes; failure injection leaves no visible dangling state; authorized deletion meets the SLA across retention classes; no stack/path/content leaks; non-loopback startup refused without remote gate.

## Definition of Done

A local client can submit, monitor, cancel and retrieve a persistent recognition/correction result through REST with restart-safe state and enforced offline privacy.

## Acceptance Criteria

`FR-007`, `FR-009`, `AC-004`, `AC-011`; duplicate key semantics and terminal states match API; source/raw/revision retention classes remain separable; authorized deletion is complete and preprocessing/corrections cannot trigger it.

## Expected artifacts

Migrations, local adapters/worker, REST v1/OpenAPI, recovery/security tests, operating notes and status/log updates.

## Failure / rollback conditions

Stop on irreversible migration, crash-visible partial writes, unbounded worker, privacy egress or unsafe external bind. Restore the pre-stage DB backup and revert code/migration; do not enable remote mode.
