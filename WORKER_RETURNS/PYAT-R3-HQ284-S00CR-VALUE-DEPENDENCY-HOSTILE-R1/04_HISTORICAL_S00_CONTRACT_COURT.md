# Historical S00 source-contract contamination court

**Frozen historical:** `WORKER_RETURNS/PYAT-R3-S00-S02-SELECTED-WORLD-SEAM-R1/s00_target_contract.json`, Git blob `9be28b2e2df93d1b9c207a207866be1595f22aeb`. This review did not change it.

## Exact wrong claims in the existing artifact
- `required_channels[0]` `CH_01_DEMOCRACY_SUPPORT` claims `Q86B` 1–4 ordinal Likert "strongly disagree ... strongly agree" democracy support.
- `required_channels[1]` `CH_02_INSTITUTIONAL_TRUST` claims `Q86A` identical 1–4 ordinal Likert trust.
- `required_channels[2]` `CH_03_DEMOCRATIC_ATTITUDES` claims a measured/transformed democratic-attitudes joint derived from Q86A/B.
- `world_scope.structural_position` says democracy-support/trust cross-classification; `world_scope.eligibility` says "complete Q86A/Q86B responses"; `world_scope.status` and `evidence_boundary.strongest_output_status` claim `RETAINED_SOURCE_CONDITIONED`, and inherited scope advertises 19,210 coexposures.

## Correct canonical source contracts
Canonical `rawlsing_next/wave1_r5_q86_c11_projection.py` freezes codes `0 No`, `1 Yes`, `9 DK`, `997 NOT_ASKED`, `998 REFUSAL`, `-1 MISSING`; it explicitly states codebook order gives no metric/ordinal meaning. Canonical `rawlsing_next/field_forge_conditional_support.py` freezes `Q86B` CONDITIONER and `Q86A` TARGET with identity-only topology and raw count relation. Q86B and Q86A separately ask normative citizenship inclusion (two noncitizen vs one citizen and one noncitizen parent); not objective rules or democratic/institutional trust.

## Consumer exposure analysis
- S00C's `r3_s02_seam_witness.py` imports P04 and PRE553 typed refs, **not** `s00_target_contract.json`, so current code path does not directly load its false source labels. `build_sociological_bundle` advertises P04 synthetic sourcefree test. `run_seam_witness` returns `historic_s00_source_contract=REJECTED_FALSE_Q86_DEMOCRACY_TRUST_SEMANTICS`.
- The author test `test_s00_contract_manifest_exists_and_is_valid` still loads the false contract and asserts its `strongest_output_status` equals `RETAINED_SOURCE_CONDITIONED` as a *positive "is valid"* test. Therefore complete materialization could produce a misleading green test for a scientifically false assertion.
- `compute_scenario` guards on case-sensitive substrings of caller-provided scenario_id, not on a validated contract ID or semantic type; `s00_high_democracy_support` evades the guard while computation remains P04 synthetic and correct numerically. A downstream presentation layer using the scenario label rather than the explicit synthetic status could launder the construct. It is a potential downstream pathway, **not evidence that any actual V3 consumer has been invoked**.

## Required safe disposition
**INVALID_SEMANTICS, HISTORICAL REFERENCE ONLY, NO SCIENTIFIC SOURCE ISSUANCE.** A separate authorized contract/plan owner must publish replacement version with correct native citizenship-opinion semantics and all admitted-source/permission limits, supersession link/explicit incompatibility with old contract. Gate downstream consumer accepts exact new target-contract ref and evidence/permissions, not caller text alone. Old contract shall remain evidence of the historical error, never an active source issuer. Original artifact and frozen S00R oracles remain untouched by S00CR.
