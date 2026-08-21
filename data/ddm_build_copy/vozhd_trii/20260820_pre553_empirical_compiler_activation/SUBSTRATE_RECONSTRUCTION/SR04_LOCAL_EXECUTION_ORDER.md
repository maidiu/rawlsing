# SR04 — PHYSICAL CARRIER BAKEOFF — REVISION 3 SHARED-PATH ACCEPTANCE

Repository: `maidiu/rawlsing`
Frozen semantic parent: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
Control branch: `agent/vozhd-trii-pre553-substrate-reconstruction-control`

The exact launch HEAD is supplied by HQ. Verify it before doing anything.

## Current status

Stage A synthetic contract testing is accepted at harness HEAD:

`a5874b3a8bc371ae3a2baebf31f3cce6fe9bb298`

Binding acceptance/gate:

`21_SR04_STAGE_A_ACCEPTANCE_AND_STAGE_B_WIRING_GATE.md`

Stage B is NOT authorized.

Static HQ review proved that the real-source CLI path still invokes older candidate/query functions different from the functions exercised by the accepted Stage-A synthetic suite.

## Read first, in order

1. `11_PHYSICAL_CARRIER_SELECTION_COURT.md`
2. `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
3. `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md`
4. `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`
5. `21_SR04_STAGE_A_ACCEPTANCE_AND_STAGE_B_WIRING_GATE.md`
6. `16_SR03_R3_ADJUDICATION.md`
7. `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`
8. accepted I02/I03/I05 reference code/tests only as needed; READ ONLY.

## Sole permitted repository write

You may modify only:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR04_CARRIER_BAKEOFF.py`

No other repository file may change.

# IMMEDIATE MISSION — STAGE A.1 ONLY

Refactor the harness so Stage A and Stage B use ONE shared carrier-court execution path.

The only lawful difference between the stages is fixture provider:

- Stage A: tiny deterministic synthetic fixture;
- Stage B: exact WVS7/LiTS I neutral fixture.

The shared path must own all of:

- one frozen Q00-Q15 SQL map;
- candidate materialization;
- candidate query execution;
- result normalization;
- independent-oracle comparison;
- true stored-candidate read-back digest computation;
- correctness disposition;
- warm-up + scored timing;
- cold/open timing;
- separate index timing where applicable;
- peak-RSS measurement;
- disk budget enforcement;
- build/query time ceilings;
- candidate cleanup confinement;
- provisional selection.

Remove/retire duplicated Stage-A-only versus Stage-B-only truth implementations. Do not leave a second dormant candidate/query path that main() can invoke.

## Required Stage-A.1 synthetic acceptance

Run the tiny synthetic fixture through the exact shared code path Stage B would invoke.

The receipt must prove at minimum:

- `shared_query_map = true`
- `shared_candidate_execution_path = true`
- `shared_oracle_comparison_path = true`
- `shared_stored_readback_path = true`
- `shared_budget_enforcement_path = true`
- all four candidates compare equal to the independent oracle;
- all four stored-candidate replay digests compare equal to fixture digests;
- wrong-oracle negative test is detected;
- stored-data corruption negative test is detected;
- PostgreSQL lifecycle is open through query/readback and cleanly stops;
- `DATABASE_URL` is never used;
- cleanup is confined to the disposable root;
- no WVS7/LiTS I bytes are decoded;
- no candidate may report `MEASURED_CORRECT` without both oracle equality and stored-readback digest equality.

Required token:

`PRE553_SR04_SHARED_EXECUTION_PATH_CONTRACT_PASS`

## Publication after Stage A.1

When Stage A.1 passes:

1. syntax-check and static-audit the harness;
2. verify the sole repo change is `SR04_CARRIER_BAKEOFF.py`;
3. commit only that file with message:
   `Unify SR04 carrier bakeoff execution path`
4. push the control branch;
5. RETURN TO HQ:
   - starting exact HEAD;
   - new harness HEAD;
   - harness SHA-256;
   - exact Stage-A.1 command;
   - complete tiny Stage-A.1 receipt;
   - Stage-A.1 token;
   - final git status;
   - pushed branch HEAD.

**STOP THERE.**

Do not decode WVS7 or LiTS I.
Do not launch Stage B.

## Later Stage B — not currently authorized

Only after HQ accepts Stage A.1 will Stage B be authorized.

Stage B will use exact raw WVS7/LiTS I bytes to build a neutral fixture checkpoint once, freeze exact source/harness/fixture/oracle identities, and then execute the four candidates through the same accepted shared path.

A later candidate-implementation-only retry may reuse an exact checkpoint only under the identity/digest rules in `21_SR04_STAGE_A_ACCEPTANCE_AND_STAGE_B_WIRING_GATE.md`.

## Forbidden

Do not:

- launch any raw-source Stage B run;
- touch the live Rawlsing PostgreSQL database or `DATABASE_URL`;
- change source bytes;
- change the four-candidate set;
- change Q00-Q15 truth conditions;
- weaken correctness gates;
- modify `rawlsing_next/**`;
- change the 5 GiB reserve or frozen disk/time ceilings;
- treat successful SQL execution as correctness;
- calculate replay digests from the neutral dataframe instead of the stored candidate;
- maintain separate Stage-A and Stage-B candidate/query truth implementations.

Fail closed on ambiguity and return it to HQ.
