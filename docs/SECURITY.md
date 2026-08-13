# Security and privacy model

**Risk level:** high. TRC accepts hostile binary input and may process diaries, student work, documents and financial data. This model applies before any remote exposure.

## Assets

- original images/PDFs and derived image artifacts;
- recognized text, alternatives and coordinates;
- corrections, author identity and revision history;
- encryption/auth credentials and engine credentials;
- model artifacts, configuration and provenance;
- availability of CPU/GPU/memory/storage/worker capacity.

## Trust boundaries

```text
untrusted client/file
  → intake sandbox/validator
  → application/domain
  → local or remote engine adapter
  → storage/job/telemetry adapters
```

Every engine, decoder, metadata parser, archive/PDF library and remote service is a separate boundary. A privacy mode is an enforced policy propagated through the complete job, not a UI hint.

## Threats and controls

| Threat | Minimum control | Verification |
|---|---|---|
| request/output/storage amplification | preflight request/JSON limits plus decoded pixels, regions/tokens/alternatives/text, artifacts/temp/persistent bytes, queued/per-principal quotas | aggregate/nested/output/disk negative tests |
| oversized image/PDF, decompression bomb | preflight and streaming limits on bytes/pages/pixels/depth; process budget | negative resource tests |
| malformed parser input / decoder RCE | disposable least-privilege subprocess/sandbox, no network, private temp root, OS caps, hard kill/cleanup | corpus fuzzing, crash/hang/cleanup tests |
| path traversal/symlink/temp race | opaque source IDs, canonicalized allowlisted storage roots, private random temp dirs, atomic writes | traversal/symlink tests |
| SSRF/unauthorized egress | no client URLs; approved scheme/host/port, resolved-IP policy, no redirects/proxies/caller auth headers; deny loopback/private/link-local/metadata and network in `LOCAL_ONLY` | no-egress, DNS/redirect rebinding tests |
| resource exhaustion/API abuse | quotas, concurrency/memory/time limits, cancellation, bounded retries, remote rate limits | load/abuse tests |
| tenant/user data disclosure | authorization per document/job/revision, tenant-scoped keys/storage/cache | cross-tenant negative tests before remote mode |
| logs/traces leak text/path | structured allowlist fields, redaction, safe errors, content-free metrics | canary leakage scan |
| poisoned model/dependency | pinned hashes/lockfile, trusted registry, signature/hash verification, SBOM/scanning | CI provenance checks |
| correction/dataset consent abuse | trusted actor context; immutable purpose/scope/policy-versioned consent grant + revocation; execution-time export authorization | forged/stale/revoked consent tests |
| cache/idempotency leakage | tenant/principal/operation/request/privacy/schema/pipeline/exact artifact digest scope; authorize every lookup | isolation/collision/deletion tests |

## Privacy modes

- `LOCAL_ONLY`: local engines/storage only; network egress disabled for workers, fallbacks, telemetry and update checks. Failure to satisfy policy returns `PRIVACY_MODE_VIOLATION`.
- `HYBRID`: only explicitly allowed stages may call approved endpoints; consent/configuration records destination and data class.
- `REMOTE_ALLOWED`: still requires authorization, TLS, minimization, retention and provider policy; it is not blanket consent for training.

Training/dataset participation is separate from processing and defaults false in all modes.

## Resource-limit contract

Before parsing: upload/body bytes, JSON depth/container/string/cardinality, file MIME/magic and page count when safely available. During processing and before serialization/persistence: total decoded pixels, dimensions, nesting/decompression ratio, regions/tokens/alternatives/text, derived/temp/persistent bytes, queued jobs, per-principal usage, memory, wall/CPU time, artifacts and concurrency. Limits are configurable but have safe non-zero defaults; disabling a limit requires an explicit deployment decision.

## Storage and deletion

- originals/raw/corrections/revisions/cache/exports/logs/traces/audit have separate retention classes and bounded cardinality;
- sensitive blobs require OS permissions; encryption at rest is mandatory before remote/multi-user profile;
- secrets stay outside source/config docs and are never logged;
- deletion is authorized, auditable and invalidates cache/exports according to policy;
- backups and export copies must follow the same deletion/retention contract.

Before Stage 04 persists data, ADR-P03 must define default retention, local permissions/encryption decision, deletion SLA, shared-blob reference handling, temp/crash cleanup, rotations and backup/export deletion. Observability access and exporters are allowlisted; exception/vendor payloads and control characters are sanitized.

## Local service gate

The local REST adapter binds loopback/local IPC only by default, authenticates a generated high-entropy bearer token or verified OS peer credentials, denies CORS and does not use cookie sessions. Token bootstrap uses an OS credential store or a private permission-checked file, never CLI arguments or loggable environment output; verification is constant-time, rotation/revocation invalidates old tokens, and startup fails closed when secure storage cannot be established. Startup refuses wildcard/non-loopback without the complete remote gate. Tests cover token-file permissions, bootstrap/rotation/revocation/redaction, wrong/missing credentials, hostile Origin and wildcard bind refusal.

## Network service gate

Do not expose remote REST/MCP until authentication, authorization, tenant isolation, TLS, rate limiting, audit, retention/encryption and incident response are specified and negatively tested. Stack traces and internal paths never cross the API boundary.

Remote engine adapters additionally prohibit caller-controlled URLs, proxy/auth headers and redirects by default. Approved endpoints are allowlisted by scheme/host/port; every resolution/connection rejects loopback, private, link-local and metadata ranges and resists DNS rebinding.

## Security quality gate

Any change touching input parsers, network, storage, auth, privacy mode, logging, export, engines/models or resource limits requires `SEC-*` traceability, negative tests, dependency/security scan and security review. From Stage 01, dependencies are hash-locked to trusted indexes with SBOM/license/vulnerability checks. Engine/model artifacts require signed or digest-verified manifests before loading. Pickle/joblib, unrestricted `torch.load`, unsafe YAML and other executable/object deserialization are forbidden unless a separate sandboxed conversion ADR proves necessity. Real private documents may not be committed to the public repository.

## Incident-safe observability

Allowed defaults: opaque correlation/job/engine IDs, durations, counts, status/error code, resource totals and bucketed confidence. Disallowed defaults: recognized text, alternatives, images, raw metadata, local source paths, author text and tokens/secrets.
