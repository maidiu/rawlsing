# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 2 STAGED EXECUTION

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

All SR04 harness revisions through `ea508994a80b9d66bd3729f6641ef5600aa624c4` are invalidated as PRE-ACCEPTANCE IMPLEMENTATION by `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md`.

Do not execute another full WVS7/LiTS I bakeoff until the staged acceptance below passes.

## Read first, in order

1. `11_PHYSICAL_CARRIER_SELECTION_COURT.md`
2. `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
3. `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md`
4. `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`
5. `16_SR03_R3_ADJUDICATION.md`
6. `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`
7. accepted I02/I03/I05 reference code/tests only as needed; READ ONLY.

## Sole permitted repository write

You may create/modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

No other repository file may change.

## Immediate mission — Stage A only

Repair the harness mechanically to close every defect in `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md` and satisfy `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`.

Before any raw WVS7/LiTS I decode, run the tiny synthetic contract test suite.

The synthetic suite must prove:

- exact Q00-Q15 query shapes;
- exact candidate result normalization and comparison to an independent oracle;
- deliberate wrong-oracle detection;
- true stored-candidate read-back digest equality for every available candidate;
- deliberate stored-data corruption detection;
- PostgreSQL disposable-cluster connection lifecycle;
- no DATABASE_URL use;
- cleanup confinement;
- disk-safety handling.

Required Stage-A token:

`PRE553_SR04_SYNTHETIC_CONTRACT_TESTS_PASS`

## Publication after Stage A

When Stage A passes:

1. syntax-check and static-audit the harness;
2. verify the sole repo change is `SR04_CARRIER_BAKEOFF.py`;
3. commit only that file with message:
   `Repair SR04 carrier bakeoff correctness harness`
4. push the control branch;
5. return to HQ BEFORE launching Stage B:
   - starting HEAD;
   - new committed harness HEAD;
   - harness SHA-256;
   - exact Stage-A command;
   - complete tiny Stage-A receipt;
   - Stage-A token;
   - final git status;
   - pushed branch HEAD.

**STOP THERE.**

Do not launch the expensive real-source Stage B until HQ accepts the committed harness/Stage-A receipt and issues a separate Stage-B order.

## Stage B — not currently authorized

After separate HQ authorization, Stage B will:

- use exact raw WVS7/LiTS I files;
- build or lawfully reuse an exact-digest neutral fixture checkpoint;
- execute all four candidates sequentially under the frozen disk/time budgets;
- compare every candidate query output to the real independent oracle;
- compute every replay digest from the stored candidate itself;
- return the frozen small result package and final SR04 completion token.

## Forbidden

Do not:

- execute the current `ea508994...` full run as evidence;
- repeatedly rebuild raw-source fixtures while debugging Stage A;
- alter raw source files;
- touch live Postgres or DATABASE_URL;
- change the candidate set;
- change query truth conditions;
- change disk/time budgets;
- modify `rawlsing_next/**`;
- treat successful SQL execution as correctness;
- compute candidate replay digests from the neutral in-memory fixture.

Fail closed on ambiguity and return it to HQ.
