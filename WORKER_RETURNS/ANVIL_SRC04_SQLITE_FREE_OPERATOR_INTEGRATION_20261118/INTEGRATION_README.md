# SQLite-free operator integration

Isolated successor only. No existing runner file, candidate tree, live run directory or process was edited.

## Wired path

- `streaming_estate.write_streaming_estate`: normal producer has no SQLite proof/read-back.
- `streaming_estate.open_stream_native_estate`: explicit `StreamVerifiedEstate(VerifiedDirectEstate)` boundary with exact member/footer/locator/root checks; no `object.__new__` and no legacy constructor bypass.
- `sqlite_free_single_pass`: projected sections → streaming writer; authenticated checkpoint retained; resume does not decode.
- `sqlite_free_witness`: producer, actual native stream reader, supervisor, progress JSONL (`progress.jsonl`) with admission/checkpoint/write/footer/publish/reopen phases.
- `audit_stream_estate.py`: optional separately executable read-only audit.

Legacy `VerifiedDirectEstate` and old estates remain untouched; the cut regression includes legacy read compatibility.

## Sourcefree test status

- 4 cut tests pass: normal writer/no SQLite, old/new parity + fresh reader, drop/duplicate/locator refusals, current refusal and separate audit.
- New sourcefree normal/resume rehearsal: exact counts 90 identities/events/routing/coordinates, 7 authority snapshots, 0 weights; normal and checkpoint-resumed roots/counts/digests equal; resume does not decode.

## Exact operator commands

Preflight (metadata only):

```bash
python3 WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118/sqlite_free_witness.py \
  --mode preflight \
  --candidate-tree /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree \
  --candidate-patch /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch \
  --config /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json \
  --runtime-config /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/SRC04.post_alignment.runtime.config.json
```

Authorized run (only after review; not run here):

```bash
python3 WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118/sqlite_free_witness.py \
  --mode run \
  --candidate-tree /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree \
  --candidate-patch /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/OWNER/WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_ONLY_CANDIDATE_20261118/candidate.patch \
  --config /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER/WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json \
  --runtime-config /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/SRC04.post_alignment.runtime.config.json \
  --binding-dir /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118 \
  --work-root /Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/evidence/anvil-src04-candidate-31rqm9z_/private-runs-aligned \
  --authorized-source-launch
```

Resume after checkpoint interruption: add
`--resume-checkpoint <work-root>/<run>/private/prepared-sections.checkpoint.json`
and omit source-path semantics; the resume path verifies checkpoint HMAC/current authority and does not decode.

## Constraints

Sourcefree evidence only. No original source read, real build, product/protected/Q2/science change, benchmark, object root promotion, or DHIKR. The old expected SQLite/I02 roots are refused rather than promoted.
