# PYAT C1-01 — AT07 PREIMAGE COMPLETION AND IMPLEMENTATION CONTINUATION — R1

Status: ISSUED__USER_MEDIATED_BROWSER_SOL_HIGH_LAUNCH_REQUIRED

Role: Browser/GitHub implementation + documentary correction worker, GPT-5.6 Sol High

Branch:
`agent/rabochii-pyat-hq131-c1-01-preimage-completion-r1`

Exact base:
`d20466c21ec62e62c3abbf6f83481984aa113000`

This base contains the banked C1-01 implementation and its exact blocker:
`BLOCKED_CONTRACT_COUNTEREXAMPLE`.

## Governing holding

C1-00 remains approved at its declared grain. The blocker is narrower: four canonical fixture preimages were not exposed even though their resulting hashes were frozen.

You are authorized to complete that missing fixture identity material only.

Do NOT change the accepted semantic law, evidence hashes, witness schema, source/release/risk/measure law, or owner APIs.

## Exact missing preimages

Reconstruct and freeze, if and only if exact recomputation succeeds:

1. forward `PositionedSubjectPossibilityQuery.material()`
   expected hash:
   `83727ca59eaf43085324ee7dc7db5ce4ecf4e4bf1f1284692cd3ad3f192df027`

2. reverse `PositionedSubjectPossibilityQuery.material()`
   expected hash:
   `cb2d085675c137848bb40f191ba8992100513eaa904a09cd54064f6ef51d3d8a`

3. forward complete `C1_CONDITION_VALUE_BINDING_WITNESS@2` material
   expected hash:
   `c93e840c06da9ab8de9ca237863d52858fe6765d5bfd7c7efb42b879440663c9`

4. reverse complete `C1_CONDITION_VALUE_BINDING_WITNESS@2` material
   expected hash:
   `e81c4e19144a749877a6f6e7e48a213e869bfe5d04ba81372ca5384b7cf5e700`

## Reconstruction law

Use only already-frozen accepted inputs:

- C1-00 R2 relation oracle and witness schema;
- R3 exact evidence identity spine and evidence preimages;
- R4 exact owner-native synchronization;
- accepted current C1 analytical contract and fixture oracle;
- current public `PositionedSubjectPossibilityQuery.material()` owner;
- exact AT07 source/release/subject/target/predicate/risk/measure/authority refs.

Do not brute-force arbitrary unconstrained material merely to hit a hash.

A lawful reconstruction must be semantically forced by the accepted fixture/owner contracts and must independently recompute the expected hash.

If the accepted artifacts underdetermine one or more fields such that multiple semantically distinct preimages remain possible, STOP and return that exact underdetermination. Do not invent a historical preimage.

## Historical immutability

Do not edit R2, R3, or R4 historical correction artifacts.

Freeze the completion in a new R5 directory.

## Write allowlist

You may write only:

1. `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R5/**`
2. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/analytical_contract.md`
3. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/fixture_oracle_manifest.json`
4. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/worker_return.json`
5. `rawlsing_next/tests/test_pre553_analytical_composition.py`
6. `WORKER_RETURNS/PYAT-C1-01-VERTICAL-SLICE-R2/**`

The banked production implementation:
`rawlsing_next/pre553_analytical_composition.py`

is FROZEN at blob:
`5c85d33987d7dc78efe98ceb5e78afe1ddc89b20`

Do not edit it in this commission.

Do not edit any existing owner.

## Required successful correction

If all four preimages reconstruct exactly:

1. bank complete canonical materials under R5;
2. include an independent recomputation receipt for all four hashes;
3. update only the active current C1 packet to point to R5 completion while preserving historical R2/R3/R4;
4. replace the red missing-preimage contract assertion in `test_pre553_analytical_composition.py` with exact recomputation assertions from R5;
5. complete the AT07 forward/reverse test construction from the frozen materials;
6. require the public producer → banked C1 adapter → actual public consumer path;
7. require forward 54/60 and reverse 54/62;
8. require exact forward evidence hash
   `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`;
9. require exact reverse evidence hash
   `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`;
10. preserve every mandatory hostile from the C1-01 commission.

No supplied/prebuilt final slice is allowed.

## Execution

Source-free only.

Do not access raw survey sources.
Do not run Candidate A/B/C.
Do not run measured P2X.
Do not run real-source C11 materialization.

Do not use the user's Mac unless the user explicitly authorizes that in the actual worker conversation.

If a lawful execution surface is available, run:

`python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py`

Record exact environment and pass/fail/error/skip counts.

If no lawful runtime is available after a successful patch, return a typed execution-capability block with the exact patch frozen. Do not manufacture PASS.

## Required returns

R5:
- `00_RETURN.md`
- `01_FORWARD_QUERY_PREIMAGE.json`
- `02_REVERSE_QUERY_PREIMAGE.json`
- `03_FORWARD_WITNESS_PREIMAGE.json`
- `04_REVERSE_WITNESS_PREIMAGE.json`
- `05_RECOMPUTATION_RECEIPT.json`

C1-01 R2:
- `00_RETURN.md`
- `01_SCOPE_AND_DIFF.json`
- `02_AT07_ASSERTION_MATRIX.json`
- `03_HOSTILE_CASE_MATRIX.json`
- `04_EXECUTION_RECEIPT.json`
- `05_FINAL_DISPOSITION.json`

Allowed dispositions:

- `PREIMAGES_RECONSTRUCTED__C1_01_SOURCE_FREE_PASS`
- `PREIMAGES_RECONSTRUCTED__PATCH_READY_EXECUTION_BLOCKED`
- `PREIMAGE_UNDERDETERMINED__CONTRACT_CORRECTION_REQUIRED`
- `PREIMAGE_HASH_MISMATCH__COUNTEREXAMPLE`
- `CHANGES_REQUIRED_BY_EXISTING_OWNER`

Do not begin C1-02.

Terminal:
`C1_01_PREIMAGE_COMPLETION_RETURNED__HQ_ADJUDICATION_REQUIRED`
