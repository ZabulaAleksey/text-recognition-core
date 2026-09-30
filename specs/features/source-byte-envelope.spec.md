# Stage 02 — bounded source byte envelope

Status: approved local preparation slice under NIGHT RUN V2. This is not decoder,
metadata parser, OCR activation or full Stage 02 acceptance.

## Scope and invariants

- Accept only a caller-supplied binary stream; this helper opens no path or URL.
- Read at most 64 MiB plus one byte using fixed 64 KiB requests, with a smaller
  positive configured limit allowed. Reject empty input, oversized responses,
  unsupported leading signatures, read failures and non-byte stream responses
  with stable, content-free error codes.
- Identify only literal PNG, JPEG and PDF leading signatures. Signature matching
  is a routing hint, never proof of a well-formed file or a trusted MIME type.
- Return only immutable kind, byte count and SHA-256 digest. The helper retains
  no input bytes and emits no user path, content or supplied MIME value.
- The caller owns stream lifetime and must run any binary decoder, metadata
  parser or OCR/model runtime inside the required isolated worker.

## Acceptance and rollback

Tests cover exact size boundary, one-byte excess, chunked reads, short reads,
malformed/unsupported signature, nonbinary or oversized stream responses,
invalid limit, and digest of accepted bytes. No engine is invoked. Rollback is
reverting this module, SPEC and tests; there is no persistent state.
