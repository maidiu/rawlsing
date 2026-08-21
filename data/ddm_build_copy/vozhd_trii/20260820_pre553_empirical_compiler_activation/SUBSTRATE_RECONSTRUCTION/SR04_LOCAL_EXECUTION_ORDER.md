# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 6 REAL B2 CHECKPOINT-ONLY EXECUTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted harness implementation: `4743c40c783544c6c21ec490644896bd0b71ada5`
Accepted harness SHA-256: `d33a86ccfa4fc75916f2f24a3ca627732abc45fa29cafd15cc8ab3439836b5b4`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted milestones:

- Stage A correctness contract: ACCEPTED
- Stage A.1 shared execution path: ACCEPTED
- Stage A.2 performance/packaging/checkpoint contract: ACCEPTED
- B1/B2 CLI separation proof: ACCEPTED
- Real B1 neutral checkpoint: ACCEPTED

Binding newest authority:

`24_SR04_REAL_B1_ACCEPTANCE_AND_B2_AUTHORITY.md`

REAL B2 IS AUTHORIZED.
No raw-source execution is authorized.

## Read first, in order

1. `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
2. `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`
3. `21_SR04_STAGE_A_ACCEPTANCE_AND_STAGE_B_WIRING_GATE.md`
4. `22_SR04_STAGE_A2_ACCEPTANCE_AND_B1_B2_CLI_GATE.md`
5. `23_SR04_CLI_PROOF_ACCEPTANCE_AND_REAL_B1_AUTHORITY.md`
6. `24_SR04_REAL_B1_ACCEPTANCE_AND_B2_AUTHORITY.md`

## Mission — REAL B2 ONLY

Execute the accepted harness in explicit `--stage-b2` mode against the accepted neutral checkpoint only.

Harness and governance are READ ONLY.

B2 boundary:

`accepted checkpoint -> checkpoint_read verification -> shared four-candidate carrier court -> provisional selection -> exact final package -> deterministic ZIP -> STOP`

B2 MUST NOT decode source bytes and MUST NOT invoke `build_fixture`.

## Exact checkpoint input

Use only:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

Before invoking Python, verify that directory contains exactly the six substantive checkpoint files below and that each has the exact accepted byte size and SHA-256:

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

If any identity differs, STOP and return the mismatch unchanged.

Do not use a ZIP as B2 input.

## Fresh execution paths

Output directory:

`/private/tmp/SR04_B2_CARRIER_BAKEOFF_RESULTS`

Disposable work root:

`/private/tmp/SR04_B2_WORK`

If either path already exists, STOP rather than merge or overwrite.

Do not modify, move, delete, or repackage:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

## Exact command

From the verified repository checkout:

`python3 data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py --stage-b2 --checkpoint-dir /private/tmp/SR04_B1_NEUTRAL_CHECKPOINT --work-root /private/tmp/SR04_B2_WORK --output-dir /private/tmp/SR04_B2_CARRIER_BAKEOFF_RESULTS`

Do NOT pass `--source-root`.

No short wrapper timeout.

## Required execution law

The accepted checkpoint reader must verify:

- checkpoint version / source identities;
- neutral relation digests;
- oracle digest.

Then execute exactly four candidates:

1. `PARQUET_DUCKDB_DIRECT`
2. `DUCKDB_NATIVE`
3. `POSTGRES_EPHEMERAL`
4. `SQLITE`

For every candidate, preserve the accepted law:

- oracle correctness required;
- true stored readback digest required;
- one warm-up + five scored Q00-Q15 repetitions;
- recorded median and p95;
- scored sequential batch time;
- measured cold-open time;
- measured index-build time where applicable;
- measured persistent disk;
- measured peak RSS;
- frozen 5 GiB reserve / candidate disk budget;
- frozen build/query time ceilings;
- disposable candidate cleanup only.

A candidate is not `MEASURED_CORRECT` unless oracle and replay checks both pass.

Selection remains:

`flawless effectiveness -> fastest batch -> <=10% speed tie -> lightness`

## Required final package

The output directory must contain exactly:

- `RECEIPT.json`
- `ENVIRONMENT.json`
- `FIXTURE_MANIFEST.json`
- `FIXTURE_DIGESTS.json`
- `QUERY_ORACLE.json`
- `CANDIDATE_RESULTS.json`
- `PROVISIONAL_SELECTION.json`
- `STDOUT.txt`
- `STDERR.txt`

The harness must also create the deterministic ZIP corresponding to that output directory.

Required success token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Return to HQ

Return:

- exact checkout HEAD;
- harness SHA-256;
- exact command;
- exit code;
- preflight checkpoint file sizes + SHA-256;
- complete final result directory;
- deterministic ZIP path, byte size, SHA-256;
- `RECEIPT.json`;
- `ENVIRONMENT.json`;
- `FIXTURE_MANIFEST.json`;
- `FIXTURE_DIGESTS.json`;
- `QUERY_ORACLE.json`;
- `CANDIDATE_RESULTS.json`;
- `PROVISIONAL_SELECTION.json`;
- `STDOUT.txt`;
- `STDERR.txt`;
- all four candidate dispositions;
- all four candidate batch times;
- all four candidate persistent disk sizes;
- all four candidate peak RSS measurements;
- provisional selection;
- completion-token presence;
- final `git status -sb`.

Then STOP.

## Forbidden

Do not:

- run `--stage-b1`;
- pass `--source-root`;
- decode WVS7 or LiTS I;
- alter checkpoint bytes;
- use or inspect `DATABASE_URL`;
- touch live Rawlsing PostgreSQL;
- modify harness/governance/runtime;
- change candidates, queries, budgets, timing protocol, or selection law;
- commit benchmark outputs;
- delete the accepted B1 checkpoint before HQ adjudication.

Fail closed on any checkpoint mismatch or execution ambiguity.