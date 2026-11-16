# RAWLSING HQ CHECKPOINT — C1 R6 + C2 REVIEW + D02 ARCHAEOLOGY

Checkpoint: `20260930-PYAT-C1R6-C2R-D02ARCH-BOUND-R1`

Decision:
`HQD-2026-09-30-132`

Status:
`C1_R5_UNDERDETERMINATION_ACCEPTED_R6_CODEX_BOUND__C2_02_RETURNED_REVIEW_BOUND__D02_LOCATOR_ARCHAEOLOGY_BOUND__C3_ADOPTED`

## C1

R5 return:
`73346b423616e9c18b25b110009ba6c8bb14c268`

Disposition:
`PREIMAGE_UNDERDETERMINED__CONTRACT_CORRECTION_REQUIRED`

HQ accepts that the old synthetic query/witness hashes are genuinely underdetermined by accepted historical material and must not be reverse-engineered.

The production implementation remains frozen:
`rawlsing_next/pre553_analytical_composition.py`
blob:
`5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`

R6 normative source-free fixture correction is issued:

- branch: `agent/codex-pyat-hq132-c1-01-normative-identity-r6-r1`
- commission: `8a038b99d432cc13e9342f9073382ec10076b04d`
- base: `73346b423616e9c18b25b110009ba6c8bb14c268`

R6 explicitly freezes new caller-defined synthetic query/binding/witness inputs, recomputes all downstream identities honestly, preserves old underdetermined hashes as historical superseded fixture evidence, and executes the C1 source-free test path.

## C2

C2-02 return:
`6f6ab9dfe5ad8f9359630dd05abf43c3fd11a1b5`

Worker disposition:
`INPUT_OR_CUSTODY_BLOCKER`

Provisional proposed proving set:
`SRC02, SRC06, SRC08, SRC12, SRC14, SRC26, SRC27, SRC35`

Count:
`8`

Exact blocker:
`C2-02-BLOCK-D02-LOCATOR-001`

The eight-source minimality claim is not yet adopted.

Independent C2-02 review:

- branch: `agent/reviewer-pyat-hq132-c2-02-proving-workload-r1`
- commission: `568ec56774f11814af50cea80e834abe0f11f5fa`
- base: `6f6ab9dfe5ad8f9359630dd05abf43c3fd11a1b5`

## D02

A separate retained-evidence archaeology lane is issued for SRC14 EVS 2008.

Source SHA:
`5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379`

Branch:
`agent/rabochii-pyat-hq132-d02-evs2008-locator-archaeology-r1`

Commission:
`57d7ee585f7364383394d067c6aeb871470edda4`

This lane may inspect retained repository/Library evidence only.

It may not open, materialize, decode or infer from the raw EVS 2008 SAV.

Its target is an exact historical D02 locator/native-type witness or an already-governed deterministic traversal oracle independent of future C4 output.

## C3

C3 source-free integration remains adopted:

`integration/pyat-hq130-c3-source-free-accepted-r1`

head:

`30686b185d4ceb2c94f61815ef70d8c8e76255d6`

No further C3 worker is active.

## Active frontier

Three independent productive lanes:

1. C1-01 R6 normative synthetic identity completion + source-free execution.
2. C2-02 independent proving-workload review.
3. D02 EVS-2008 retained locator archaeology.

Held:
- C1-02 until C1-01 R6 accepted and independently reviewed as required;
- C2 proving-set adoption until C2-02 independent review;
- C4 freeze until C1-01 acceptance + C2 review + D02 blocker disposition;
- C4 source execution until a later exact warrant;
- JOIN-01 until C1-R and relevant C2 output;
- OMEGA-1 until scoped source-free join.

No Astra trigger.
No raw-source execution.
No PRE-V3→V3 actor implementation.
