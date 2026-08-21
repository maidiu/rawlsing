# SR04 STAGE A.2 ACCEPTANCE AND B1/B2 CLI SEPARATION GATE

Status: `STAGE_A2_ACCEPTED__B1_B2_CLI_SEPARATION_REQUIRED_BEFORE_RAW_EXECUTION`

Accepted harness parent: `f303198853c0f494efd23eb598231cfea948fad0`

## 1. Stage A.2 holding

Stage A.2 is accepted as proof that the shared SR04 carrier-court machinery can, on a deterministic synthetic fixture:

- use one Q00-Q15 query map;
- use one candidate execution path;
- compare all candidate answers to an independent oracle;
- compute replay digests from stored candidate data;
- execute 1 warm-up + 5 scored repetitions per query;
- record median/p95, batch time, cold-open time, index time, disk bytes, and RSS;
- create and verify required SQLite/PostgreSQL indexes;
- enforce typed disk/time nonviability paths;
- write/read a digest-bound neutral checkpoint;
- detect checkpoint corruption;
- produce the exact Stage-B result-package schema without emitting the real completion token;
- avoid DATABASE_URL and raw-source decoding during the proving stage.

The synthetic provisional winner has no architectural authority.

## 2. Static review finding

At accepted harness parent `f303198...`, the CLI still lacks separately invokable B1 and B2 modes. The default real-source path performs:

`build_fixture(raw WVS7/LiTS I) -> shared_carrier_court(all four candidates)`

in one invocation.

That violates the execution discipline frozen after the earlier expensive debug loops.

This is a CLI/orchestration defect only. It does not reopen the accepted shared correctness/performance/checkpoint logic.

## 3. Required terminal CLI structure

The harness must expose exactly these real-source stages:

### B1 — checkpoint build only

Required invocation mode: `--stage-b1`.

Inputs:

- exact `--source-root` containing the frozen WVS7 and LiTS I bytes;
- explicit `--checkpoint-dir` under a disposable/local execution root;
- small `--output-dir` for B1 receipt only.

B1 must do exactly:

1. verify source hashes;
2. decode WVS7 and LiTS I under the frozen reader contract;
3. build the exact neutral 24-variable-per-source fixture;
4. prove hostile fixture facts;
5. compute the independent real oracle;
6. compute neutral relation digests;
7. write the neutral checkpoint using the already-tested checkpoint writer;
8. immediately read the checkpoint back using the already-tested checkpoint reader;
9. require exact relation-digest, source-identity, manifest, and oracle identity;
10. emit a small B1 receipt;
11. STOP before any carrier candidate is created.

Required B1 token:

`PRE553_SR04_B1_NEUTRAL_CHECKPOINT_COMPLETE`

The B1 receipt must identify:

- exact harness HEAD and harness SHA-256;
- exact source hashes;
- checkpoint version;
- checkpoint absolute path;
- checkpoint byte size;
- relation digests;
- oracle digest;
- selected variable names/ordinals;
- hostile fixture check results;
- read-back verification PASS;
- `candidate_execution_started=false`;
- `DATABASE_URL_unused=true`.

B1 checkpoint data are local execution artifacts and MUST NOT be committed to Git.

### B2 — checkpoint-only carrier court

Required invocation mode: `--stage-b2`.

Inputs:

- explicit `--checkpoint-dir`;
- `--output-dir` for the final small SR04 result package.

B2 must NOT accept or require raw source paths for normal execution.

B2 must do exactly:

1. read and fully verify the checkpoint using the accepted checkpoint reader;
2. fail closed on source identity, relation digest, manifest, version, or oracle mismatch;
3. execute the existing accepted shared carrier court against the checkpoint relations/oracle;
4. apply the frozen selection law;
5. produce the exact final Stage-B package and deterministic ZIP;
6. emit the real SR04 completion token only after all required candidate dispositions and package files exist.

Required final token:

`PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE`

## 4. Cheap CLI proving test before B1

Before any raw decode, the worker must prove the stage separation on the synthetic fixture.

Synthetic CLI proof must establish:

- synthetic B1 creates a checkpoint and records `candidate_execution_started=false`;
- synthetic B2 consumes only that checkpoint and executes the shared court;
- B2 fails closed on a corrupted checkpoint;
- normal B2 does not read source-root/raw source bytes;
- final-package writer is reached through B2, not B1;
- no duplicate candidate/query/oracle/checkpoint implementation is introduced.

Required proof token:

`PRE553_SR04_B1_B2_CLI_SEPARATION_PASS`

## 5. Implementation confinement

Only this repository file may be modified by the local worker:

`SR04_CARRIER_BAKEOFF.py`

Do not change the source constitution, candidate set, query truth conditions, benchmark budgets, runtime code, or accepted PRE553 tests.

After the cheap CLI proof passes, commit/push the harness and RETURN TO HQ. Do not launch real B1 until HQ accepts the committed CLI wiring.
