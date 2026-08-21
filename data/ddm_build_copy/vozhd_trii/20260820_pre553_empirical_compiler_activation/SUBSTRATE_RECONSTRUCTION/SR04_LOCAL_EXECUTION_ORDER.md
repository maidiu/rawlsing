# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 12 REAL B2 R4 CHECKPOINT-ONLY EXECUTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`
Accepted corrected harness implementation: `e249f809f194cb369bf08094ac2cbf4c2d1fcd43`
Accepted corrected harness SHA-256: `e1aa6deaeedf7fb2bbb68c6019e791363e8ad10dcf492087b32a221959e90211`

The exact launch HEAD is supplied by HQ. Verify it before execution.

## Current status

Accepted:

- Stage A / A.1 / A.2;
- B1/B2 CLI separation;
- REAL B1 neutral checkpoint;
- PostgreSQL UTF-8 transport correction/proof;
- shape-agnostic wrong-oracle negative-test correction/proof;
- real-oracle canonicalization/Q01/Q06 correction/proof.

Binding newest authority:

`31_SR04_REAL_ORACLE_CANONICALIZATION_PROOF_ACCEPTANCE_AND_B2_RETRY_AUTHORITY.md`

Previous failed REAL B2 attempts are non-admissible carrier evidence.

REAL B2 R4 IS AUTHORIZED.

## Mission

Run the accepted harness in checkpoint-only `--stage-b2` mode and complete the four-candidate physical carrier court.

Boundary:

`accepted checkpoint -> checkpoint verification -> PARQUET_DUCKDB_DIRECT -> DUCKDB_NATIVE -> POSTGRES_EPHEMERAL -> SQLITE -> canonical Q00-Q15 oracle checks -> replay checks -> performance -> provisional selection -> nine-file package -> deterministic ZIP -> STOP`

No raw-source decode is authorized.

## Preflight

Verify harness SHA-256 exactly:

`e1aa6deaeedf7fb2bbb68c6019e791363e8ad10dcf492087b32a221959e90211`

Verify checkpoint exactly:

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

Total: `114705938` bytes.

Stop on any mismatch.

## Fresh R4 paths

Use new paths; do not reuse prior failed B2 output/work directories:

`/private/tmp/SR04_B2_R4_WORK`

`/private/tmp/SR04_B2_R4_CARRIER_BAKEOFF_RESULTS`

If either R4 path already exists before this authorized run, STOP rather than deleting ambiguous evidence.

Never modify:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

## Exact command

`python3 data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py --stage-b2 --checkpoint-dir /private/tmp/SR04_B1_NEUTRAL_CHECKPOINT --work-root /private/tmp/SR04_B2_R4_WORK --output-dir /private/tmp/SR04_B2_R4_CARRIER_BAKEOFF_RESULTS`

Do NOT pass `--source-root`.
No short wrapper timeout.

## Required correctness law

For each candidate:

- exact canonical comparison for Q00-Q05 and Q07-Q15;
- Q06 finite-value abs/rel tolerance `1e-9`;
- exact stored relation replay digests;
- accepted wrong-oracle negative test;
- accepted stored-corruption negative test.

A candidate is not `MEASURED_CORRECT` unless its canonical oracle and replay checks pass.

The accepted real B1 oracle remains byte-identical and is canonicalized only in memory for comparison.

## Required performance law

For every candidate preserve:

- one warm-up + five scored repetitions for each Q00-Q15 query;
- median and p95;
- sequential batch time;
- cold-open time;
- index-build time where applicable;
- persistent disk bytes;
- peak RSS;
- 5 GiB reserve / frozen disk budget;
- frozen build/query ceilings;
- candidate-local cleanup.

PostgreSQL must retain UTF8 server/client transport and stop cleanly.

Selection law remains:

`flawless effectiveness -> fastest batch -> <=10% speed tie -> lightness`

## Required final package

Exactly:

- `RECEIPT.json`
- `ENVIRONMENT.json`
- `FIXTURE_MANIFEST.json`
- `FIXTURE_DIGESTS.json`
- `QUERY_ORACLE.json`
- `CANDIDATE_RESULTS.json`
- `PROVISIONAL_SELECTION.json`
- `STDOUT.txt`
- `STDERR.txt`

Plus deterministic ZIP.

Required token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Return to HQ

Return:

- exact checkout HEAD;
- harness SHA-256;
- exact command;
- exit code;
- checkpoint preflight hashes/sizes;
- final result directory;
- deterministic ZIP path, bytes, SHA-256;
- complete nine-file package;
- all four candidate dispositions;
- all four oracle-comparison outcomes;
- all four replay-comparison outcomes;
- all four batch times;
- all four persistent disk sizes;
- all four peak RSS values;
- PostgreSQL UTF8/lifecycle evidence if recorded;
- wrong-oracle negative-test outcome;
- stored-corruption negative-test outcome;
- provisional selection;
- token presence;
- final `git status -sb`.

Then STOP.

## Forbidden

Do not:

- rerun B1;
- pass `--source-root`;
- decode raw survey files;
- mutate/rewrite/repackage the accepted checkpoint;
- use or inspect DATABASE_URL;
- touch live Rawlsing PostgreSQL;
- modify harness/governance/runtime during execution;
- change candidate/query/oracle/replay/performance/index/budget/selection law;
- treat previous failed B2 attempts as carrier evidence;
- commit local execution outputs.
