# FIRST LAUNCH ORDER SEQUENCE

## ORDER SR01 — SOURCE BYTE CENSUS — HQ/browser
Status: `ACCEPTED`
Output: `SOURCE_BYTE_INVENTORY.csv`.
Observed: 35 governed source files, 31 SAV, 4 DTA. AppleDouble packaging artifacts excluded.
Gate: G-SR01 ACCEPTED.

## ORDER SR02 — LEGACY WRITER + ACTUAL V550 DB DEPENDENCY GENEALOGY — HQ/browser + local read-only receipt
Status: `ACCEPTED__PROVENANCE_CLOSED`
Binding closure: `15_SR02_R3_ADJUDICATION.md`.
No further local SR02 execution is ordered.
Gate: G-SR02 ACCEPTED.

## ORDER SR03 — 35-SOURCE PHYSICAL METADATA EXTRACTION — local Codex + HQ adjudication
Status: `ACCEPTED__35_SOURCE_PHYSICAL_CENSUS_COMPLETE`
Binding closure: `16_SR03_R3_ADJUDICATION.md`.
No further SR03 run is ordered unless source bytes/decoder dependency/config changes.
Gate: G-SR03 ACCEPTED.

## ORDER SR05 — FORMAT-NEUTRAL SOURCE CONSTITUTION — HQ/browser
Status: `ACCEPTED__RECLOSED_AFTER_FULL_CENSUS`
Binding closure: `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`.
Gate: G-SR05 ACCEPTED.

## ORDER SR04 — PHYSICAL CARRIER BAKEOFF — bounded local Codex harness cell
Status: `HARNESS_INVALIDATED__STAGE_A_SYNTHETIC_RETURN_REQUIRED`

Binding authorities, in order:

- `11_PHYSICAL_CARRIER_SELECTION_COURT.md`
- `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
- `19_SR04_PREACCEPTANCE_HARNESS_AUDIT.md`
- `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`
- `SR04_LOCAL_EXECUTION_ORDER.md`

Harness commits through `ea508994a80b9d66bd3729f6641ef5600aa624c4` are PRE-ACCEPTANCE ONLY and cannot produce an acceptable carrier result.

HQ audit proved incorrect frozen-query implementations, missing candidate-output/oracle comparison, non-candidate replay digests, and a PostgreSQL connection-lifecycle defect. Those are implementation defects and carry zero evidence for or against any carrier.

Immediate authorized work is **Stage A only**:

1. repair only `SR04_CARRIER_BAKEOFF.py`;
2. run tiny synthetic Q00-Q15 contract tests;
3. prove wrong-oracle and stored-corruption detection;
4. prove true stored-candidate readback digests;
5. prove disposable PostgreSQL lifecycle;
6. commit/push the repaired harness;
7. return the Stage-A receipt/token to HQ;
8. STOP before another raw WVS7/LiTS I run.

Required Stage-A token:

`PRE553_SR04_SYNTHETIC_CONTRACT_TESTS_PASS`

Only after HQ accepts Stage A will Stage B be authorized. Stage B will use exact WVS7 + LiTS I raw sources. A previously validated neutral fixture may be reused only under exact checkpoint-digest rules in `20_SR04_EXECUTION_DISCIPLINE_ADDENDUM.md`.

Decision priority remains exactly: **flawless effectiveness -> fast -> light**.

Gate: G-SR04 remains OPEN.

## ORDER SR06 — SELECTED CARRIER / C11 DECODER IMPLEMENTATION
Status: `BLOCKED_ON_G_SR04`

No production/runtime implementation worker launches until G-SR04 closes.
