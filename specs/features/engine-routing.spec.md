# Stage 02 — bounded engine routing foundation

Status: approved by the direct NIGHT RUN V2 technical-autonomy request for a
reversible, local planning slice. Engine execution and Stage 02 acceptance remain open.

## Scope

- A framework-independent immutable registry describes at most 32 engine candidates.
- Each candidate has a stable name/version, nonempty explicit OCR/HTR capability set,
  locality and deterministic rank. Duplicate names and malformed descriptors fail.
- Automatic selection sorts eligible candidates by rank, then name. The returned
  sequence is a *plan* for an explicit, bounded fallback executor; the planner
  never invokes an engine, decoder, network or filesystem.
- Explicit selection returns exactly the named candidate or fails with a stable
  unavailable/capability/privacy error; it cannot silently switch engines.
- `LOCAL_ONLY` excludes remote candidates before any route is returned.
  `AUTO` is not a region capability: classification must choose OCR or HTR first.
- Region routing accepts at most 4096 unique region IDs and returns one plan per
  region in input order. An unsupported region fails the whole plan, never
  silently drops a region.

## Boundaries and rollback

The registry does not authorize a remote engine under `HYBRID`/`REMOTE_ALLOWED`;
consent, worker isolation, egress policy, model verification, retries and attempt
provenance belong to later Stage 02 slices. No adapter is activated by this SPEC.
Rollback is removal of the pure planner and its tests; no persistent state exists.

## Acceptance

Tests cover deterministic tie ordering, explicit selection, privacy exclusion,
capability mismatch, duplicate/malformed candidates, region order and missing
region capability. Ruff, mypy and the full Stage 01 suite remain green.
