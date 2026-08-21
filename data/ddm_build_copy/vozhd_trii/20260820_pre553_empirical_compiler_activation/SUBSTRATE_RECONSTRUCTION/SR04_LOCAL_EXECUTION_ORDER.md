# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 4 B1/B2 CLI SEPARATION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Accepted harness milestones:

- Stage A correctness contract: ACCEPTED
- Stage A.1 shared execution path: ACCEPTED
- Stage A.2 performance/packaging/checkpoint contract: ACCEPTED at harness HEAD `f303198853c0f494efd23eb598231cfea948fad0`

Binding newest gate:

`22_SR04_STAGE_A2_ACCEPTANCE_AND_B1_B2_CLI_GATE.md`

Real raw-source B1 and checkpoint-only B2 are NOT yet authorized.

Static HQ review found one remaining orchestration defect: at `f303198...` the default real-source CLI still performs raw fixture construction and the four-candidate court in one invocation. The already-tested checkpoint writer/reader is not exposed as a separately stoppable B1/B2 CLI.

This gate does not reopen accepted correctness, query, performance, budget, checkpoint, or package semantics. It only separates their invocation.

## Read first, in order

1. `11_PHYSICAL_CARRIER_SELECTION_COURT.md`
2. `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
3. `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md`
4. `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`
5. `21_SR04_STAGE_A_ACCEPTANCE_AND_STAGE_B_WIRING_GATE.md`
6. `22_SR04_STAGE_A2_ACCEPTANCE_AND_B1_B2_CLI_GATE.md`
7. `16_SR03_R3_ADJUDICATION.md`
8. `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`

## Sole permitted repository write

You may modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

No other repository file may change.

# IMMEDIATE MISSION — CHEAP CLI SEPARATION PROOF ONLY

Add explicit real execution modes:

- `--stage-b1`
- `--stage-b2`
- `--checkpoint-dir <path>`

Do not change the accepted shared carrier court, Q00-Q15 truth conditions, candidate set, source hashes, budgets, checkpoint format, or final package schema except for the minimum orchestration needed to invoke the already-accepted functions lawfully.

## Required B1 semantics

`--stage-b1 --source-root <root> --checkpoint-dir <dir> --output-dir <dir>` must:

1. verify exact WVS7/LiTS I bytes;
2. build the real neutral fixture;
3. compute hostile fixture checks, relation digests, and independent oracle;
4. write the checkpoint through the accepted checkpoint writer;
5. read it back through the accepted checkpoint reader;
6. require exact verification;
7. emit a small B1 receipt with token `PRE553_SR04_B1_NEUTRAL_CHECKPOINT_COMPLETE`;
8. record `candidate_execution_started=false`;
9. STOP.

B1 must never invoke `shared_carrier_court`.

## Required B2 semantics

`--stage-b2 --checkpoint-dir <dir> --output-dir <dir>` must:

1. accept no normal raw-source dependency;
2. read/verify the checkpoint through the accepted checkpoint reader;
3. execute the accepted shared carrier court using checkpoint relations/oracle only;
4. apply the accepted selection path;
5. write the exact final Stage-B package and deterministic ZIP through the accepted package writer;
6. emit `PRE553_SR04_CARRIER_BAKEOFF_RECEIPT_COMPLETE` only after final package completion.

B2 must not call the raw decoder/build_fixture path.

## Cheap synthetic CLI proof

Before any real raw-source run, exercise the actual B1/B2 orchestration using only the synthetic fixture/checkpoint path.

The proof must establish:

- `synthetic_b1_checkpoint_created=true`
- `synthetic_b1_candidate_execution_started=false`
- `synthetic_b2_checkpoint_only=true`
- `synthetic_b2_shared_carrier_court_executed=true`
- `synthetic_b2_final_package_path_executed=true`
- `synthetic_b2_corrupted_checkpoint_rejected=true`
- `synthetic_b2_raw_source_decode=false`
- `DATABASE_URL_unused=true`
- no duplicate query/candidate/oracle/checkpoint implementation was introduced.

Required proof token:

`PRE553_SR04_B1_B2_CLI_SEPARATION_PASS`

## Publication after proof

When the cheap proof passes:

1. syntax/static check;
2. verify only `SR04_CARRIER_BAKEOFF.py` changed;
3. commit only that file with message:
   `Separate SR04 B1 and B2 execution modes`
4. push the control branch;
5. RETURN TO HQ:
   - starting exact HEAD;
   - new harness HEAD;
   - harness SHA-256;
   - exact cheap CLI-proof command;
   - complete small proof receipt;
   - success token;
   - final git status;
   - pushed branch HEAD.

**STOP THERE.**

Do not launch real B1.
Do not launch B2.

## Forbidden

Do not:

- decode WVS7/LiTS I during the cheap CLI proof;
- modify live PostgreSQL or use `DATABASE_URL`;
- alter source files;
- change frozen carrier/query semantics;
- change the 5 GiB reserve or time/storage budgets;
- modify `rawlsing_next/**`;
- combine B1 and B2 back into one real execution;
- commit checkpoint or benchmark result data.

Fail closed on ambiguity and return it to HQ.
