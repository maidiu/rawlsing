# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 10 REAL B2 RETRY AFTER ORACLE-PROOF ACCEPTANCE

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`
Accepted real B1 checkpoint: `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`
Accepted corrected harness implementation: `ea0d02ffde10a98872e73ea2b1fed8e453246cfb`
Accepted corrected harness SHA-256: `12a4eb3bace293ddf355c9661e051f77be3735813d6d776c61c472be0ba81c7d`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted:

- Stage A / A.1 / A.2;
- B1/B2 CLI separation;
- real B1 neutral checkpoint;
- PostgreSQL UTF-8 transport correction and proof;
- shape-agnostic deliberate wrong-oracle negative-test correction and proof.

Two earlier real B2 attempts are NON-ADMISSIBLE carrier evidence:

1. first failed during PostgreSQL ASCII COPY transport;
2. second passed corrected PostgreSQL UTF-8 transport but failed in the synthetic-era list-only deliberate wrong-oracle negative test.

Binding newest authority:

`28_SR04_ORACLE_NEGATIVE_PROOF_ACCEPTANCE_AND_B2_RETRY_AUTHORITY.md`

REAL B2 RETRY IS AUTHORIZED.
No raw-source execution is authorized.

## Mission — REAL B2 RETRY ONLY

Execute the accepted corrected harness in explicit `--stage-b2` mode against the accepted neutral checkpoint only.

Harness and governance are READ ONLY.

Boundary:

`accepted checkpoint -> checkpoint verification -> shared four-candidate carrier court -> shared validation -> provisional selection -> exact final package -> deterministic ZIP -> STOP`

B2 MUST NOT invoke `build_fixture` and MUST NOT decode raw survey bytes.

## Preflight

Verify exact checkout HEAD supplied by HQ.

Verify harness SHA-256:

`12a4eb3bace293ddf355c9661e051f77be3735813d6d776c61c472be0ba81c7d`

Verify `/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT` contains exactly these six substantive files:

| file | bytes | SHA-256 |
|---|---:|---|
| `CHECKPOINT_MANIFEST.json` | 4490 | `f56e6c0710babde0449e5e85da3f1446df4abf1da7b8e866f1f3c4743b031bb0` |
| `QUERY_ORACLE.json` | 131552 | `446c3a2d2ba5127dd48441156e8bfec6a288674233862eb694c2577816845f1a` |
| `events.arrow` | 104610186 | `c0d3c0d3fb426a24408738148424740ff9eb8103fa7cbc01d5c3eb3971e57c25` |
| `respondents.arrow` | 9920410 | `1eca810c4eb369299f62dda31eef3a972e4b3b4ac5c499384ff4298099ff6b73` |
| `sources.arrow` | 5418 | `080ec67148c16d34760daadc94d667c0dd6c101b5b9dcb7d063b24909bd3bf2d` |
| `variables.arrow` | 33882 | `cf8db06e43834a252e737b5f273059cb028d20ad9d51d38f374bfb02e28f241b` |

If any identity differs, STOP.

## Failed-run cleanup

The failed B2 attempt may have left:

`/private/tmp/SR04_B2_CARRIER_BAKEOFF_RESULTS`

and/or:

`/private/tmp/SR04_B2_WORK`

Before deleting anything, verify each existing path is exactly that disposable failed-B2 path, is not a symlink, and is not a parent, child, alias, or other resolution of the accepted B1 checkpoint.

It is authorized to delete ONLY those two failed disposable B2 paths so the retry can use fresh paths.

Never delete, move, rewrite, or repackage:

`/private/tmp/SR04_B1_NEUTRAL_CHECKPOINT`

## Exact retry command

After the two B2 paths are confirmed absent/fresh:

`python3 data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py --stage-b2 --checkpoint-dir /private/tmp/SR04_B1_NEUTRAL_CHECKPOINT --work-root /private/tmp/SR04_B2_WORK --output-dir /private/tmp/SR04_B2_CARRIER_BAKEOFF_RESULTS`

Do NOT pass `--source-root`.
No short wrapper timeout.

## Required carrier law

Execute exactly:

1. `PARQUET_DUCKDB_DIRECT`
2. `DUCKDB_NATIVE`
3. `POSTGRES_EPHEMERAL`
4. `SQLITE`

The PostgreSQL candidate must retain the accepted UTF8 server/client transport.

The shared wrong-oracle negative test must use the accepted shape-agnostic corruption helper.

For every candidate preserve:

- oracle correctness;
- true stored readback digest;
- one warm-up + five scored Q00-Q15 repetitions;
- median and p95;
- sequential batch time;
- cold-open time;
- index-build time where applicable;
- persistent disk;
- peak RSS;
- 5 GiB reserve and frozen candidate disk budget;
- frozen build/query ceilings;
- candidate-local cleanup only.

A candidate may not be `MEASURED_CORRECT` unless both oracle and replay checks pass.

Selection law remains:

`flawless effectiveness -> fastest batch -> <=10% speed tie -> lightness`

## Final package

Required output files exactly:

- `RECEIPT.json`
- `ENVIRONMENT.json`
- `FIXTURE_MANIFEST.json`
- `FIXTURE_DIGESTS.json`
- `QUERY_ORACLE.json`
- `CANDIDATE_RESULTS.json`
- `PROVISIONAL_SELECTION.json`
- `STDOUT.txt`
- `STDERR.txt`

Also require the deterministic ZIP produced by the harness.

Required token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## Return to HQ

Return:

- exact checkout HEAD;
- harness SHA-256;
- exact command;
- exit code;
- checkpoint preflight sizes/hashes;
- final result directory;
- deterministic ZIP path, bytes, SHA-256;
- complete nine-file final package;
- all four candidate dispositions;
- all four batch times;
- all four persistent disk sizes;
- all four peak RSS measurements;
- PostgreSQL server/client encoding observed during real B2 if recorded;
- wrong-oracle negative-test result;
- stored-corruption negative-test result;
- provisional selection;
- completion-token presence;
- final `git status -sb`.

Then STOP.

## Forbidden

Do not:

- rerun B1;
- pass `--source-root`;
- decode WVS7 or LiTS I;
- mutate checkpoint bytes;
- use or inspect `DATABASE_URL`;
- touch live Rawlsing PostgreSQL;
- modify harness/governance/runtime;
- change candidates, Q00-Q15, oracle construction, normalization, replay, timing, indexes, budgets, or selection law;
- reopen the accepted PostgreSQL UTF-8 correction;
- modify the accepted oracle-negative-test helper;
- commit execution outputs;
- treat either earlier failed B2 attempt as carrier evidence.

Fail closed on any checkpoint mismatch or execution ambiguity.
