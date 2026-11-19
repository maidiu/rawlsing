# SRC04 SQLite-free cut — native contract repair

## Verdict

Scoped executable cut remains isolated from the running Wave 1 tree and
worktree. Three intake gaps are repaired as follows.

- Base: `bf59f7d708ea250445234776de318ddf620be6ea`
- Previous cut: `f317ebbd795b83a746906eb84abc101d595c3ad7`
- New return: this directory.

## 1. No stale legacy logical claim

`_new_roots` no longer copies `expected.logical`, `release` or `replay`.
A supplied legacy `ExternalI02Roots` is refused with:

`LEGACY_EXPECTED_ROOT_UNVERIFIABLE__VERSIONED_STREAM_IDENTITY_REQUIRED`

The new identity is derived from the validated stream and member/footer
content:

- new `logical` from manifest, family counts, member hashes and proof version;
- new `replay` includes that logical identity;
- new `release` includes the logical identity;
- existing old `physical` is never claimed equal.

Changed legal input produces changed logical and replay roots. Exact restore
produces the same new roots. A stale old supplied root cannot authorize changed
bytes.

## 2. Existing native first consumer

`open_stream_native_estate()` validates the versioned stream proof, then returns
the **existing `VerifiedDirectEstate` object** assembled through a narrow
proof-reader boundary. The existing methods are used unchanged for:

- `iter_family()` typed row reconstruction;
- `select_events()` actual public row/selector path;
- current/revocation callback on each materializing call.

No second reader engine and no second body corpus are introduced. The legacy
`VerifiedDirectEstate` constructor and old estates remain valid and untouched.

The isolated wiring patch routes both normal and resume calls in
`single_pass_handoff.py` to the new writer and passes the existing progress
callback. The active runner/tree is not edited.

## 3. Separate strict audit

`audit_stream_estate.py` and `audit_stream_estate()` perform a separate
read-only invocation against an already written estate. The audit:

- uses the same versioned proof boundary and existing `iter_family()` path;
- requires an independently supplied manifest SHA and roots;
- checks exact family counts;
- makes no writes and does not rebuild Parquet;
- does not call the old writer as an audit substitute.

Test invokes it in a separate process and verifies the estate manifest is
byte-unchanged.

## Progress

The new writer emits timestamped phases through the existing runner progress
callback:

- `stream_start`
- `family_written` with processed/expected aggregates
- `footers_verified`
- `published`
- `reopened_validation`
- `audit_complete`

The patch passes `progress=progress` for both write and resume, so the existing
supervisor-visible stderr JSON stream carries phase and aggregate counts. No
live runner file was edited.

## Refusals and parity

Focused 5-row sourcefree tests prove:

- old/new family counts and all Parquet member bytes equal;
- new versioned roots differ from legacy roots by declaration, never equality;
- changed legal input produces changed new logical/replay roots;
- exact restore produces identical new roots;
- stale supplied legacy roots refused;
- duplicate exact ref refused;
- dropped family/object census refused;
- locator mismatch refused;
- revoked current callback refused;
- old legacy reader still reads old estate;
- native `select_events()` row/selector path works on new estate;
- `sqlite3.connect` patched to fail in normal writer, no `.sqlite` under new
  root;
- audit runs separately and does not rewrite the estate.

Tests: **4 passed in 3.50 s**.

Measured fixture run:
`{"old_seconds":0.193897,"new_seconds":0.078576,"old_bytes":356679,"new_bytes":356442,"new_proof_scratch_bytes":27436,"sqlite_proof_built":false,"read_back_audit":false}`

Proof scratch in normal path is a temporary compact dbm ref index plus staging
Parquet; it is removed before publication. No SQLite proof is built. Retained
bytes are not proof scratch and are not used as a performance claim.

## Residual

Full legacy **physical** identity is not reconstructed because it is the byte
hash of the SQLite certificate. The exact safe scoped route is versioned stream
identity with logical/replay identities derived from actual content. A legacy
`expected_i02` is refused rather than copied. This is the remaining precise
residual; no parity is claimed.

## Existing caller command (not run here)

```bash
MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_WITNESS_RUNNER_20261118/witness_caller.py \
  --mode run \
  --candidate-tree evidence/anvil-src04-candidate-31rqm9z_/candidate \
  --candidate-patch OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch \
  --config IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json \
  --runtime-config MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/SRC04.post_alignment.runtime.config.json \
  --binding-dir MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118 \
  --work-root <owner-private-work> \
  --authorized-source-launch
```

Patch pins: candidate patch SHA `ffa4520f…`, base config SHA `5e107de4…`, runtime
config SHA `dd5cf699…`, canonical `ba886d87…`. Not launched.

## Commands

```bash
PYTHONPATH="MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree:\
MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_WITNESS_RUNNER_20261118:\
IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_CONSTRUCTION_20261118" \
python3 -B -m pytest -q -o addopts='' -p no:cacheprovider \
  IMPLEMENTER/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_CONSTRUCTION_20261118/test_streaming_cut.py
```

Files: `streaming_estate.py`, `audit_stream_estate.py`,
`sqlite_free_wiring.patch`, `evidence_metrics.json`, `test.out`.

No live Wave 1 tree, worktree, artifacts, source, PIDs 11521/11526, product,
science, grants, protected refs, or DHIKR were touched.
