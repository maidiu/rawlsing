# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 5 REAL B1 CHECKPOINT EXECUTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted harness milestones:

- Stage A correctness contract: ACCEPTED
- Stage A.1 shared execution path: ACCEPTED
- Stage A.2 performance/packaging/checkpoint contract: ACCEPTED
- B1/B2 CLI separation proof: ACCEPTED at harness HEAD `4743c40c783544c6c21ec490644896bd0b71ada5`

Binding newest authority:

`23_SR04_CLI_PROOF_ACCEPTANCE_AND_REAL_B1_AUTHORITY.md`

Real B1 is AUTHORIZED.
Real B2 remains BLOCKED pending HQ adjudication of the real B1 return.

## Read first, in order

1. `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
2. `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`
3. `21_SR04_STAGE_A_ACCEPTANCE_AND_STAGE_B_WIRING_GATE.md`
4. `22_SR04_STAGE_A2_ACCEPTANCE_AND_B1_B2_CLI_GATE.md`
5. `23_SR04_CLI_PROOF_ACCEPTANCE_AND_REAL_B1_AUTHORITY.md`
6. `16_SR03_R3_ADJUDICATION.md`
7. `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`

## Mission — REAL B1 ONLY

Execute the already-committed harness in explicit `--stage-b1` mode against the exact local source bytes.

The harness source is READ ONLY for this execution.
No repository writes are authorized.

B1 must execute exactly this boundary:

`raw WVS7 + raw LiTS I -> neutral fixture -> hostile checks -> independent oracle -> relation digests -> checkpoint_write -> checkpoint_read verification -> B1 receipt -> STOP`

B1 MUST NOT invoke `shared_carrier_court`.
B1 MUST NOT create or benchmark Parquet, DuckDB, PostgreSQL, or SQLite candidates.
B1 MUST NOT use or inspect `DATABASE_URL`.

## Exact source bytes

Use the local Rawlsing source directory containing the hash-matched source files, normally:

`/Users/matthewsmith/Desktop/Rawlsing/data/Data`

Required exact source identities:

### WVS7

- file: `WVS Wave 7.sav`
- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`
- expected rows: `97220`

### LiTS I

- file: `LiTS_I.dta`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- expected rows: `29002`

Do not substitute alternate files.

## Output locations

Use fresh local paths under `/private/tmp`.

Recommended exact paths:

Checkpoint:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

Small B1 receipt directory:

`/private/tmp/SR04_B1_RECEIPT`

Disposable work root:

`/private/tmp/SR04_B1_WORK`

Do not reuse or merge a prior synthetic checkpoint.
If any recommended real-B1 path already exists, fail closed and return that fact rather than overwriting it silently.

## Recommended exact command

From the verified repository checkout:

`python3 data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py --stage-b1 --source-root /Users/matthewsmith/Desktop/Rawlsing/data/Data --checkpoint-dir /private/tmp/SR04_B1_NEUTRAL_CHECKPOINT --work-root /private/tmp/SR04_B1_WORK --output-dir /private/tmp/SR04_B1_RECEIPT`

No wrapper timeout shorter than the work itself is permitted.

## Required success conditions

The B1 receipt must show:

- exact checkout HEAD;
- harness SHA-256;
- source hashes equal the frozen WVS7/LiTS I hashes;
- checkpoint version `SR04_NEUTRAL_CHECKPOINT_V1`;
- exact relation digests for `sources`, `respondents`, `variables`, `events`;
- exact oracle digest;
- selected source variables / ordinals;
- frozen hostile-check results;
- checkpoint readback verification `PASS`;
- `candidate_execution_started=false`;
- `DATABASE_URL_unused=true`;
- `raw_source_decode=true`;
- checkpoint total byte size;
- exact absolute checkpoint path.

Required token:

`PRE553_SR04_B1_NEUTRAL_CHECKPOINT_COMPLETE`

## Return to HQ

Return:

- exact checkout HEAD;
- harness SHA-256;
- exact command;
- exit code;
- complete `B1_RECEIPT.json`;
- absolute checkpoint path;
- checkpoint byte size;
- `CHECKPOINT_MANIFEST.json`;
- checkpoint relation file names and byte sizes;
- SHA-256 of every checkpoint file;
- source hashes;
- fixture relation digests;
- oracle digest;
- selected variables / ordinals;
- hostile-check results;
- completion-token presence;
- final `git status -sb`.

Preserve the checkpoint exactly at the returned path after success. Do not zip, move, mutate, or delete it unless HQ later orders that.

## Forbidden

Do not:

- run `--stage-b2`;
- execute the carrier court;
- modify the harness;
- modify governance;
- modify source bytes;
- connect to live PostgreSQL;
- use `DATABASE_URL`;
- commit the checkpoint or receipt;
- delete or move a successful checkpoint;
- reinterpret source semantics.

Fail closed on any ambiguity or exact-source/checkpoint-verification failure and return the failure unchanged.
