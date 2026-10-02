# TRC-02-RASTER-01 — локальный isolated raster SDK slice

Status: validated locally; full Stage02 partial. Baseline8be0282. Recovery2026-10-02
подтвердила совпадение всех24 source/test/worker working hashes с final gate receipt.
Fresh consumer оставался незавершённым и завершён после recovery; прежние canary
кампании не повторялись. Machine-readable identities: stage02-isolated-raster.json.

## Что проверено

- Locked offline full suite238PASS/0skip (20.78s), preserved75baseline +163new.
- Ruff check/format37files, mypy15sourcefiles, lock22resolved, offline wheel/sdist PASS.
- Actual runtime CPython3.13.16/Pillow12.3 immutable candidate image; fresh parent SDK
  CPython3.13.7 from installed site-packages, not repository. Default five dependencies
  restored offline with require-hashes; no Pillow distribution/PIL in host consumer.
- Authored RGB PNG2x1 and gray JPEG2x2 returned exact independently expected pixels,
  source/pixel hashes, zero exits and exact cleanup. This is actual SDK→CLI→worker
  decoder consumer, not mock; it is not OCR recognition E2E.
- Previously preserved18actual input profiles/limits and8failure canaries plus native
  Windows Job/helper10, strict parser31, worker28 and parent/recovery/interruption92
  tests. Independent final bounded cleanup review accepted exact source hashes.

## Fresh restore recovery

Only missing existing pin pydantic-core2.46.5 cp313 Windows wheel was acquired before
recovery,2,041,980bytes, SHA256
15f4a94963c95accac15b7b657bb177d3ad82bb90b0d0526d9a9b85079925db5.
uv0.12.3 local-file original46/two-distinct hash allowance failed even with the correct
hash present. One correct hash and duplicated same hash passed; wrong hash failed.
No internal implementation cause is asserted. Selected exact locked artifact hash
narrows only this allowance; four other dependency/version/hash blocks byte-identical.
No hash disabling, package/version upgrade, lock mutation or audit workaround.
v4 failed at harness regex assertion before install; v5 corrects only scratch harness.
Fresh requirements recipeSHA0eb9ac0c60e47250e1004bb7d206329b5bb662ede17c93a5b6cc8cc5923fdb35.

SDK wheelSHA13ed0495dddb28ee86c19945c430bed9aaf4f36e4573d854e847518b42fd1a36;
sdistSHA1a6cdfa2eacaee698621b7b54b1093fd8ec4259c2e69bd46b1e0ece339ae367a.
Working-copy receipt hashes and staged Git-content hashes are distinct dimensions;
JSON explicitly records both. No assumption that Windows CRLF bytes equal Git LF.

## Worker build materialization

`workers/Raster.Dockerfile` fixes base88310c08 and offline Pillow12.3 install. Before
build, deployment creates a minimal owned context with Raster.Dockerfile,
raster_worker.py, raster_requirements.txt, exact
pillow-12.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
and license-notices/. WheelSHA0847a763afefb695bc912d7c131e7e0632d4edc1d8698f58ddabec8e46b8b6d3;
full unmodified PillowLICENSE70,307bytes SHA
dda12a98c1979cf3d94df1cff45d27a4cb3f04a60c76f76902ac54cac03ec0ce.
Keep full wheel/license notices, PSF/base notices and RASTER_THIRD_PARTY_NOTICE.txt
in that context; no repository/private sources or user paths mounted. Build with
`docker build --pull=false --network=none -f Raster.Dockerfile <owned-context>`
only after independently verifying/admitting all exact inputs and available local base.
No SDK runtime auto-build/pull/download is provided. Candidate image is a local proof,
not a portable distributed artifact or automatic default provider.

## Limits and exclusions

See featureSPEC for fixed64MiB input/4096dimensions/50331648RGB bytes,20s total,
4s cleanup reserve and inspected worker controls. Docker Desktop privileged daemon/VM
is trusted, not rootless. POSIX parent unavailable. Same-instance pending recovery
blocks retries; durable cross-instance journal/host-loss reaper is outside this slice.

TRC_DEPENDENCY_AUDIT = BLOCKED_EXTERNAL_APPROVAL. No locked21 inventory sent to OSV
or substitute. Full base/native license/vulnerability closure, production/private
inputs, customer container distribution, PDF, representative benchmark, OCR adapter
and full Stage02 remain unproved. There is no hosted TRC CI receipt. Old Stage01 audit
or a single public Pillow metadata snapshot cannot establish current zero-findings.

## Reproduce ordinary gates

1. Read selectedSTAGES and featureSPEC; verify admitted runtime/build inputs first.
2. `uv lock --check --offline` in existing locked environment.
3. `uv run --locked --offline --no-sync pytest -q` (actual2live tests require explicit
   authored-only local admission; unavailable runtime produces skips, not live PASS).
4. `uv run --locked --offline --no-sync ruff check src tests workers`, then format check
   and `uv run --locked --offline --no-sync mypy src`.
5. `uv build --offline --no-build-isolation`; restore a fresh default consumer with
   exact artifact hashes and install wheel offline/no-deps, asserting installed path,
   absence of host Pillow and independently expected benign PNG/JPEG pixels.

External audit is deliberately excluded while its exact approval is blocked.
