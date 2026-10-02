# TRC-02-RASTER-01 — isolated single-page raster decoder

Status: bounded slice validated locally; Stage02 remains partial. Local acceptance
receipt: docs/evidence/stage02-isolated-raster.md and .json. External dependency audit
is BLOCKED_EXTERNAL_APPROVAL; no production/customer-distribution admission. Requirements:
FR-003, NFR-001/002/003/005, SEC-001/002/003/005/006/009, AC-004/007/010;
ADR-010 and ADR-016. Public raster decoder is a separate Application port;
RecognitionEngine/domain/registry/result schemas stay unchanged.

## Runnable slice and dependency admission

Authored PNG/JPEG source bytes → existing bounded signature/hash envelope →
one disposable Linux worker → exact immutable RGB8 pixels/source provenance →
verified cleanup → caller. No OCR, PDF rasterization, jobs, DB, REST or user corpus.
Worker-only optional dependency candidate: Pillow12.3.0, exact uv hash lock.
Parent/domain must not import Pillow. Before enabled runtime: official source/release,
exact wheel and bundled license inventory/security checks, immutable reviewed image
digest/platform, actual Python>=3.13,<4, no automatic image pull or host fallback.
Tags, labels alone, cached3.12.5 image and metadata-only checks never establish this gate.
PDF remains unsupported; ADR-P01 stays open for PDF/whole decoder evaluation.

## Content and geometry profile v1

One PNG/JPEG, one frame, raw mode RGB or L. L expands each gray byte equally to RGB;
RGB preserves channel bytes. No resize, crop, rotate, normalization or ICC conversion.
Any EXIF or ICC profile, alpha/palette/CMYK/animated/multi-frame source is rejected
content-free rather than silently transformed. Non-semantic format decoder metadata
is never returned/logged. Geometry mapping is identity in source pixel coordinates;
provenance records source SHA256/kind and pixel SHA256/dimensions/format.
Pillow Image.open has explicit PNG/JPEG format allowlist, decompression warning is an
error, finite MAX_IMAGE_PIXELS, truncated images denied; dimensions/mode/frame/profile
checked before load/tobytes. Decoder errors never include raw exception/path/metadata.

## Limits and containment

Input64MiB (existing ceiling); one page; width/height<=4096; pixels<=16777216;
RGB payload<=50331648 bytes. Fixed protocol header<=4096 bytes; combined fixed status
diagnostics<=16384 bytes; unknown/extra/truncated protocol bytes rejected, not truncated.
Worker aggregate memory256MiB, memory+swap256MiB (no added swap), CPU1, PIDs8;
per-process NOFILE32 and FSIZE64MiB; private /tmp tmpfs64MiB noexec/nosuid/nodev;
read-only root, UID65532, all capabilities dropped, no-new-privileges, network none,
no privileged/device/host socket/home/repository/DB mounts. Concurrency1 per adapter.
Parent total monotonic deadline20s including4s cleanup reserve; cancellation checked
while streaming/polling. No stage resets deadline; no retry/in-process fallback.
Defaults are finite engineering bounds, not product latency/quality guarantees.

Initial parent provider is Windows with a trusted signed native Docker CLI and
fixed local Docker Desktop Linux named-pipe endpoint. The worker is Linux/amd64.
An owned Windows Job contains native helper descendants before resume.
POSIX host providers are unavailable in this slice: a process group does not
prove containment of descendants that create another session. The Application
port stays platform independent; no unsafe host-provider fallback is admitted.

Docker Desktop daemon/VM is trusted privileged infrastructure; this is not a rootless
daemon claim. Caller controls only bounded source bytes and CancellationToken, not
image/command/options/environment/paths/network/daemon endpoint. Deployment-owned
runtime binding is explicit and immutable. Source enters worker over bounded stdin:
no host source file or user path is mounted. Worker-only private tmpfs satisfies scratch
root; no source/raster is persisted to Docker logs (log driver none) or application logs.
Ownership is exact imageID plus unpredictable nonce label plus full containerID.
Inspect required controls before source transfer; stopped/removal/nonce-match cleanup
must complete before success. Incomplete creation/control/cleanup returns unavailable,
no partial raster, records content-free owned-resource recovery evidence where possible.
After an uncertain create/cleanup the adapter retains immutable pending recovery
evidence and refuses further decode calls. Deployment owns durable retention and
exact ownership resolution before replacing the instance or admitting a new runtime;
this library never silently clears recovery or prunes resources. Process/host-loss
recovery remains outside the automatic guarantee described below.
Container termination includes descendants; parent-owned helper processes are killed/
reaped on timeout. No global prune/other resource mutation.

## Binary protocol v1

stdin: original bounded source bytes, EOF; worker verifies same envelope itself.
stdout success: ASCII magic TRCRASTER1 newline, four-byte big-endian header length,
strict UTF8 JSON header, exactly pixel_bytes bytes, EOF; stderr empty.
Header keys exactly schema/source_sha256/kind/width/height/pixel_format/pixel_bytes/
pixel_sha256; schema exact integer1, kind png|jpeg, format RGB8, SHA lowercase64hex,
dimensions exact integers (bool forbidden), pixel_bytes=3*width*height. Duplicate JSON
members, NaN, unknown keys, digest/source mismatch, size overflow and trailing data denied.
Failure stdout empty, stderr one allowlisted DECODER_* code newline, nonzero exit.
No external header/source field is authority for image/runtime/privacy admission.

## Owned lifecycle and failure atomicity clarifications

Parent retains independent original envelope hash/kind/length. Frame claims
are compared to the original hash and kind; the eight-key wire header has no
source-length field. The parent independently verifies completed stdin byte
count equals the original envelope length before exposure. Incremental stdin reads use at most the
remaining allowance+1 byte to distinguish exact limit/overflow; EOF is mandatory.
Worker completes profile validation/decode/pixel buffer/hash before any success
frame byte. Errors before emission have empty stdout; transport failure after a
partial emission cannot retract bytes, so parent discards all partial output.
Incremental parent reads exact magic/length/header/payload, caps before allocation,
requires EOF and zero process/container exit plus cleanup. No unbounded communicate
or raster/log collection. stdout/stderr drain concurrently, each with explicit caps;
Docker diagnostics also remain bounded and are sanitized to constants.

One absolute monotonic deadline covers creation, inspection, bounded input writer,
both drains, status wait and cleanup. The processing phase stops at deadline minus
cleanup reserve. Cancellation token, language task cancellation, KeyboardInterrupt,
timeout, malformed/flooded output, CLI/container failure and daemon error use one
finally lifecycle. Parent helpers stop/reap boundedly, exact owned container is
stopped/killed and removed; unverifiable cleanup is unavailable, never success.
Parent-process/host loss is outside this slice's cleanup guarantee: no daemon lease/
reaper exists yet. Record exact nonce/CID content-free recovery evidence, retain
unknown resources and fail closed on next admission rather than broad prune.

Before source transfer inspect image/platform, fullCID/nonce, fixed entrypoint/argv,
user/workdir/env allowlist, no bind/volume/device/socket mounts, expected private
tmpfs, network none/ports empty, read-only root, CapDrop ALL, NoNewPrivileges,
no privileged/host PID/IPC, memory/swap/CPU/PID/NOFILE/FSIZE and log driver none.
Absent or mismatched required control fields prohibit source transfer. Docker
may omit empty optional HostConfig.Mounts/Config.ExposedPorts in its wire schema;
these are checked when present, with required authoritative top-level Mounts=[]
and NetworkSettings.Ports={} plus no Binds/VolumesFrom/PortBindings. This observed
serialization compatibility is not permission to omit authoritative controls. Deployment binding fixes
local daemon context/endpoint and trusted helper executable identity; caller source
never supplies those values. No helper shell or inherited endpoint override.
Minimize/release source/raster references after terminal paths; in-memory Python/
Docker buffers are not secure-zeroization evidence. No pixels/raw metadata in logs.

Allowlisted worker failures: DECODER_RUNTIME_UNAVAILABLE, DECODER_INPUT_INVALID,
DECODER_INPUT_LIMIT, DECODER_PROFILE_UNSUPPORTED, DECODER_GEOMETRY_LIMIT,
DECODER_DECODE_FAILED, DECODER_OUTPUT_LIMIT. Parent adds only fixed
DECODER_UNAVAILABLE/DECODER_FAILED/DECODER_TIMEOUT/DECODER_CANCELLED.
Adversarial tests must cover internally valid but wrong-source frame, fragmented
reads, valid frame/nonzero exit, failed cleanup, slow/noEOF input, pipe backpressure
and cancellation during each phase. Every such path returns no raster.

## Acceptance and honest completion boundary

Live actual Python3.13 pinned worker decodes authored RGB PNG and constant-gray JPEG
to independently expected pixels, including source/pixel digests and exact cleanup.
Required negatives: malformed/signature-only/truncated/PDF; exact/one-over byte,
dimension/pixel/output limits; warning/error bombs and unsupported profiles; forged
header/version/bool/duplicate/hash/frame/trailing tokens; tampered runtime; privacy
canary; no-egress/private-root/control inspect; crash/hang/OOM/output flood/cancel and
descendant cleanup. Boundary unit/worker tests alone never prove Docker adapter safety.
All accepted75 tests/schema/fixtures retain bytes/assertions; rootless/native/production,
representative CER/WER and full Stage02/engine contract completion remain unproved.
Independent security review and existing full locked gates required before publication.
Platform controls already observed with different cached3.12.5 image are supporting
evidence only; actual decoder runtime controls and failure paths need fresh proof.

Rollback: ordinary source/lock commit reversal; no persistent data migration. Fail
closed on incompatible license/provenance/containment, preserve prior pure baseline.
Sources: https://pillow.readthedocs.io/en/stable/handbook/security.html ;
https://pillow.readthedocs.io/en/stable/releasenotes/12.3.0.html ;
https://github.com/python-pillow/Pillow/blob/12.3.0/LICENSE .
