# Evidence map

## Control / currentness

- `HQ_HANDOFF/LATEST.json` at live base `bc207de1db6c1e48b81c7b27b2633ad1177077ff`
- `PYAT_CONTROL_ROOM/14_R2_1_GROK_ACCEPTANCE_AND_FORWARD_PROGRAM.md`
- `HQ_HANDOFF/DECISION_LEDGER.jsonl`
  - HQD-2026-09-26-112
  - HQD-2026-09-26-115

## Adopted Field Forge

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/FIELD_FORGE_R2_ADOPTED_AUTHORITY_R1/`

Read:

- `00_RETURN.md`
- `01_ADOPTED_AUTHORITY_CAPSULE.md`
- `02_OWNER_AND_NEGATIVE_CEILINGS.md`
- `03_EVIDENCE_AND_AUDIT_POINTERS.tsv`
- `04_REINTEGRATION_DIFF_RECEIPT.json`
- `05_EXACT_INDEPENDENT_AUDIT_HANDOFF.md`

Adoption authority: `096b419ed8fd3d07c87cb74bcc4890c2f1a8ec54`.

## Post-R2 current authority

Read current HQ adoption surfaces:

- `FIELD_FORGE_OBL040_HQ_ADOPTION_R1/00_VOZHD_ADOPTION.md`
- `FIELD_FORGE_OBL041_042_HQ_ADOPTION_R1/00_OBL041_VOZHD_ADOPTION.md`
- `FIELD_FORGE_OBL041_042_HQ_ADOPTION_R1/01_OBL042_VOZHD_ADOPTION.md`
- `FIELD_FORGE_OBL005_HQ_ADOPTION_R1/00_VOZHD_ADOPTION.md`
- `FIELD_FORGE_OBL043_HQ_ADOPTION_R1/00_VOZHD_ADOPTION.md`
- `FIELD_FORGE_OBL020_POST_R2_TERMINAL_SYNTHESIS_R1/00_VOZHD_SYNTHESIS_AND_DISPOSITION.md`

## Current code blobs

- `pre553_structural_admission.py` — `fe8f706afbb5739d026846952681081b2937e9a8`
- `field_forge_conditional_support.py` — `a70decb20747d84cbcbe27d1280babc6de88ef33`
- `wsc_gt0_field_forge_ingress.py` — `08550918a64504772f4df26373a36ff2767e8b57`
- `wave1_ff_prev3_relation_admission.py` — `c5fb675fd6f95cb7dc9e0ad505224803839cc645`
- `gt12_c_to_d_relation_bridge.py` — `ea04ec079e8d60e6e5c7236ec5b54898876be4b3`
- `m1_admitted_field_forge_relation_v554_ingress.py` — `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5`
- `m1_temporal_v554_admission_dedup.py` — `e8bd6376720a2de132b384e7771d71d8d39cf261`
- `gt12_permission_translation_authority.py` — `2eb1441e0ee5be3eef2567f8ffb57819fc47f0d6`
- `pre553_repo_native_current_payload.py` — `b850e7794f387000afe4a6dfd49ca5092426f895`
- `f07_second_canary_prev3_admission.py` — `06c312209148ab5bdd2c2077f3c887bdc9f948c8`

## Exact current tests inspected

- `test_field_forge_conditional_support.py` — `e0c4a041ab26254823ac5608177aa593d5f3a1ab`
- `test_wave1_ff_prev3_relation_admission.py` — `943e0b01e04919d347281b72894dc1e874ecb83e`
- `test_m1_admitted_field_forge_relation_v554_ingress.py` — `e6a456865470fe587aae9480a81eb2ccbc8b7b51`
- `test_pre553_structural_admission.py` — `c754382d1c8a96bece0084233bb8ec144425b170`
- `test_gt12_d_to_m4_typed_bridge.py` — `7bcd4a7c15c29ccc869166038cdadad9f7140f6a`
- `test_wsc_gt0_end_to_end_integrated.py` — `53846ce7b5778756c952371f31dc3bb2661b0e1f`
- `test_f07_second_canary_prev3_admission.py` — `7772e9cd4726e6b513a2e2a809ecb9f02ea30f28`

This lane did not execute these tests; it consumed their current source and accepted prior qualification evidence.

## GT2 / GT12 real populated evidence

Read:

- `GT1_GT2_IMPLEMENTATION_WAVE_R1/D_FF_PREV3_ADMISSION_R1/00_RETURN.md`
- `GT1_GT2_IMPLEMENTATION_WAVE_R1/E_M1_RELATION_INGRESS_R1/00_RETURN.md`
- `GT1_GT2_IMPLEMENTATION_WAVE_R1/F_GT1_GT2_E2E_HARNESS_R1/00_RETURN.md`
- `GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/E1_INTEGRATED_REGRESSION_COURT_R1/00_RETURN.md`
- `GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/GT1_GT2_FINAL_HQ_ADOPTION_R1/00_VOZHD_ADOPTION.md`
- `GT12_R1C_INTEGRATED_GT2_IDENTITY_AUTHORITY_DISPOSITION_R1/00_DISPOSITION.md`

Final adopted real canary:
- 19,210 denominator;
- current relation hash `1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19`;
- PREV3 admission `a445e43da99405e0f8181f7ab6c428d9b0dd14fefc7fc5091f21f2d21f00b08d`;
- V3 terminal `DENY_ZERO_EFFECT`;
- real probe PASS;
- terminal court 221 passes + 20 protocol self-tests; exact determinism.

## Final LiTS source-free evidence

Current successful evidence:

`WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/source_retry_evidence/`

Key files:
- `00_RETURN.md`
- `ff02_readiness_disposition.json`
- `canonical_object_inventory.json`
- `authority_closure_receipt.json`
- `zero_source_resume_receipt.json`
- `oracle_verification_receipt.json`

Current terminal:

`PASS__FINAL_LITS_RETRY_BANKED_COMPLETE_CANONICAL_EMPIRICAL_CLOSURE__ZERO_SOURCE_RESUME_GREEN__FIABC_ORACLE_FROZEN__FF02_READY__NO_CANDIDATES_RUN`

## Forensic negative finding: F07 live dependency

`f07_second_canary_prev3_admission.py` hard-codes source records under ASTRA E10/D09 paths. Direct live-base content lookup of those exact paths returned NOT_FOUND, while the module/test remain physically present.

This finding is deliberately classified as:

`PHYSICAL_IMPLEMENTATION_PRECEDENT__NOT_CURRENT_SERVING_PROOF`

It does not invalidate the accepted GT12 path or Field Forge R2 authority.
