# Scope and coverage

The audit is pinned to accepted `abd0b5ff2ffcf235b67140641f88cc61ca45c12c` (tree `196e81b7c8a284304b9aa7998e79590439b19524`) and, separately, active `a1630969f8e0b1003e657a38f77abbc413f83f2e` (tree `3c33be9c92443fa558c14753a456b0e1ec27d3bc`). No branch name, newest commit, or worker PASS was used as current semantic authority. Later changes are outside this disposition.

All findings concern the commissioned vertical slice. Governance was read for intended law, never treated as conformance proof. No project overview, historical re-adjudication, FIELD FORGE redesign, current real-source rerun, or production repair was undertaken.

## Exact coverage

The bounded mirror contains 54 accepted files: 20 requested production surfaces, 9 direct dependencies, 16 test modules, and 9 governing/evidence documents. The active mirror contains 11 files: 7 code/test surfaces and 4 R4A transport documents. These 65 versioned reads are not 65 exhaustively audited modules. Depth and purpose follow; the complete blob inventory is in [10_MACHINE_SUMMARY.json](10_MACHINE_SUMMARY.json).

Every materialized source body was checked against its Git blob SHA before use and rechecked before package generation. No source mirror drift occurred. The accepted root and scoped source trees exposed no applicable AGENTS.md. No unrelated subsystem was opened after the stop rule was reached.

| Requested accepted surface | Audit depth / proposition |
|---|---|
| [pre553_empirical_objects.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_empirical_objects.py) | Deep: canonical identity, freezing, typed states, public projection and exact refs. |
| [_pre553_query_common.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/_pre553_query_common.py) | Target topology/authority parsing and typed-state propagation. |
| [_pre553_query_predicate.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/_pre553_query_predicate.py) | Deep: sealed release indexing, authority closure and predicate interpretation. |
| [_pre553_query_eval.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/_pre553_query_eval.py) | Deep: source-indexed counting, risk membership, provenance and fact construction. |
| [pre553_authority_maintenance.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_authority_maintenance.py) | Targeted: exact authority maintenance/replay; governing focused tests. Not every operation exhaustively audited. |
| [pre553_batch_runner.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_batch_runner.py) | Targeted: exact batch/query selection, receipts, nonpositive results and replay tests. |
| [pre553_c11_ingest.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_c11_ingest.py) | Seal/validation boundary, public records, atomic commit and M01-M18 carrier integrity. |
| [wave1_r5_q86_c11_projection.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/wave1_r5_q86_c11_projection.py) | Frozen Q86 source projection, row/routing/order bindings and focused tests. |
| [wave1_gt12_i03_positive_facts.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/wave1_gt12_i03_positive_facts.py) | Deep: frozen source/risk binding, authority fitness, plan construction and I03 composition. |
| [wave1_gt12_a2_real_gt1.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/wave1_gt12_a2_real_gt1.py) | GT1 plan/fact currentness and permission ceiling; focused fixture tests. |
| [field_forge_conditional_support.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/field_forge_conditional_support.py) | Deep: query/fact closure, ordered conditional support, typed-negative preservation and replay. |
| [wave1_ff_prev3_relation_admission.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/wave1_ff_prev3_relation_admission.py) | Deep: exact authority/admission, relation lineage, typed-positive gate and replay. |
| [gt12_c_to_d_relation_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/gt12_c_to_d_relation_bridge.py) | Exact FIELD FORGE ownership, identity, participant order and PRE-V3 translation. |
| [m1_admitted_field_forge_relation_v554_ingress.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py) | Relation-specific preparation, exact lineage, SIG004 evaluation and substitute-lane rejection. |
| [m1_temporal_v554_admission_dedup.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/m1_temporal_v554_admission_dedup.py) | Direct dependency: shared evaluation type, relation/empirical dedup separation and tests. |
| [gt12_permission_translation_authority.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/gt12_permission_translation_authority.py) | Deep: adopted exact authority/adoption and singleton CONTEXT projection. |
| [gt12_d_to_m4_typed_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/gt12_d_to_m4_typed_bridge.py) | Deep: D/E identity conservation, M1 correspondence, adopted permission and M4 wrapper. |
| [m4_m1_evaluation_binding.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/m4_m1_evaluation_binding.py) | Deep: shared empirical/relation API, producer permission parameter and exact payload checks. |
| [m4_v557_v558_publication_repository.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/m4_v557_v558_publication_repository.py) | Publication, metadata/edge identity, repository closure, exact resolver and itemwise permissions. |
| [v3_psepf_zero_positive_guard.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/v3_psepf_zero_positive_guard.py) | Deep: production empty registry, authority claims, internal delegation binding and effect assertions. |

## One-hop expansion

| Direct dependency | Why it was needed |
|---|---|
| [pre553_empirical_authority.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_empirical_authority.py) | Direct authority semantics and exact registry resolution needed to decide ASTRA-002. |
| [pre553_empirical_query.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_empirical_query.py) | Public execution/replay boundary needed to decide ASTRA-001/002. |
| [pre553_c11_integrity.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_c11_integrity.py) | Carrier identity verifier needed to test the strongest counterexample to ASTRA-001. |
| [pre553_c11_repository.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_c11_repository.py) | Sealed read identity and object ownership needed to decide ASTRA-001. |
| [m2_v555_atomic_route.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/m2_v555_atomic_route.py) | Materialized for direct M4 import/test closure; no deep M2 subsystem audit. |
| [m3_v556_higher_order_structural.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/m3_v556_higher_order_structural.py) | Materialized for direct M4 import/test closure; no deep M3 subsystem audit. |
| [pre553_source_backed_c11_facade.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_source_backed_c11_facade.py) | Direct import closure for scoped source/batch tests; targeted reads only. |
| [pre553_physical_decoder.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_physical_decoder.py) | Direct import closure for scoped source/batch tests; no carrier re-execution. |
| [pre553_physical_c11_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_physical_c11_bridge.py) | Direct import closure for scoped source/batch tests; no broad physical-source audit. |

## Tests inspected and executed

Sixteen accepted modules, selected by direct governance of the audited surfaces:

- [test_field_forge_conditional_support.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_field_forge_conditional_support.py)
- [test_gt12_closure_b_c_to_d_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py)
- [test_gt12_d_to_m4_typed_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_gt12_d_to_m4_typed_bridge.py)
- [test_m1_admitted_field_forge_relation_v554_ingress.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_m1_admitted_field_forge_relation_v554_ingress.py)
- [test_m1_temporal_v554_admission_dedup.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py)
- [test_m4_v557_v558_publication_repository.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_m4_v557_v558_publication_repository.py)
- [test_pre553_authority_maintenance.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_authority_maintenance.py)
- [test_pre553_batch_runner.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_batch_runner.py)
- [test_pre553_c11_repository_ingest.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_c11_repository_ingest.py)
- [test_pre553_empirical_objects_authority.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_empirical_objects_authority.py)
- [test_pre553_empirical_query.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_pre553_empirical_query.py)
- [test_psepf_zero_positive_guard.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_psepf_zero_positive_guard.py)
- [test_wave1_ff_prev3_relation_admission.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_wave1_ff_prev3_relation_admission.py)
- [test_wave1_gt12_a2_real_gt1.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py)
- [test_wave1_gt12_i03_positive_facts.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py)
- [test_wave1_r5_q86_c11_projection.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py)

## Active candidate appendix

The seven active code surfaces were inspected against their accepted counterparts where present. Only the active changed files were overlaid into the isolated test runtime; inherited dependencies retained accepted source identities. The scoped code-tree comparison identified these relevant changes. The payload placeholder is unfinished candidate work, not a newly discovered implementation failure.

- [00_RETURN.md](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/00_RETURN.md)
- [01_EXECUTION_EVIDENCE.json](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/01_EXECUTION_EVIDENCE.json)
- [02_CONSTRUCTOR_COMPLETE_MANIFEST.json](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/02_CONSTRUCTOR_COMPLETE_MANIFEST.json)
- [04_SEAL_INPUT.json](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/04_SEAL_INPUT.json)
- [_pre553_query_eval.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/_pre553_query_eval.py)
- [pre553_repo_native_current_payload.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/pre553_repo_native_current_payload.py)
- [pre553_repo_native_seal.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/pre553_repo_native_seal.py)
- [gt12_e2b_actual_object_consumer_harness.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py)
- [test_gt12_e2b_actual_object_consumer_harness.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py)
- [test_pre553_i03_scale_equivalence_repair.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/test_pre553_i03_scale_equivalence_repair.py)
- [test_pre553_repo_native_seal.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/test_pre553_repo_native_seal.py)

## Governing/evidence documents

- [01_DOWNSTREAM_INPUT_RECEIPT.json](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT12_FINAL_E2A_REAL_GT2_RERUN_R1/01_DOWNSTREAM_INPUT_RECEIPT.json)
- [00_DISPOSITION.md](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT12_R1C_INTEGRATED_GT2_IDENTITY_AUTHORITY_DISPOSITION_R1/00_DISPOSITION.md)
- [00_AUTHORITY_CANDIDATE.json](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/00_AUTHORITY_CANDIDATE.json)
- [01_CONSTITUTION.md](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/01_CONSTITUTION.md)
- [03_VOZHD_ADOPTION.json](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/03_VOZHD_ADOPTION.json)
- [04_ADOPTION.md](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/04_ADOPTION.md)
- [00_RETURN.md](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/FINAL_E2B_REAL_INTEGRATED_GT2_POSITIVE_CHAIN_R1/00_RETURN.md)
- [00_RETURN.md](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_IMPLEMENTATION_WAVE_R1/D_FF_PREV3_ADMISSION_R1/00_RETURN.md)
- [00_RETURN.md](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_IMPLEMENTATION_WAVE_R1/E_M1_RELATION_INGRESS_R1/00_RETURN.md)

The R3 constitution/candidate wording is read with the explicit adoption documents; the earlier candidate status does not override adoption. The final E2B blocked return and active R4A constructor manifest are evidence of their own bounded states. Historical A3 execution remains genuine but is not substituted for current R1C. No later closure claim is adjudicated here.

## Evidence classes and limits

- **SOURCE:** exact versioned code and governing documents; full file/blob inventory in the machine summary.
- **TEST:** 298 accepted focused tests and 33 active focused tests passed under Python 3.12.13, pytest 9.1.1 with external plugins disabled. This is not a repository-wide test run or accepted-project verdict.
- **PROBE:** isolated synthetic contract checks use ordinary constructors and existing test fixtures. They demonstrate reachable local behavior but are not the real 19,210-member execution.
- **CURRENT QUERY CONSTRUCTION:** ordinary construction from the committed active manifest recomputed exactly `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`. This proves its representation and identity; it does not prove full current fact materialization or complete E2B execution.
- **COST INFERENCE:** canonical UTF-8 sizes calculated from committed templates/counts and serializer grammar. Binary hash-inventory bodies and the full current fact were not materialized. No measured peak-memory or time speedup is claimed.
- **OPEN QUESTION:** dependency-role ownership after an actual accepted codec/consumer roundtrip is not settled by the bounded slice.

The source physical carriers, full current EmpiricalFact, and R4A binary bodies were not downloaded for this audit. Their declared commitments are evidence, not independently reproduced execution. No actual positive owner, actor runtime, V2 expression, scheduler integration, or production mutation was executed. Zero effects are scoped to the pure audited paths and their tests.

## Exact frozen identities

| Identity | SHA-256 |
|---|---|
| predicate | `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3` |
| query | `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0` |
| fact | `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46` |
| replay | `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f` |
| risk_set | `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b` |
| permission_translation_authority | `d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c` |
| permission_adoption | `fe527dd7d6f5163edd5867adf9da2b03ea581c7d78758fe07bf6857c3fd4c46f` |

Risk membership: 19,210. Ordered targets: Q86B -> Q86A. Authority: `GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY@1.0.0`; adoption commit `5ce90e304a25359672591ed2b4a2dd605e3175c0`. Exact producer/V558 uses: `("CONTEXT",)`; V557: `ALLOW_CONTEXT_ONLY`; GT12 V3: `DENY_ZERO_EFFECT`.

## Persistence and authorized change boundary

Audit branch: `agent/astra-rawlsing-deep-system-audit-r1`, created from `abd0b5ff2ffcf235b67140641f88cc61ca45c12c`. An audit-only interim checkpoint was persisted at `8f2b411db0beeef930b2bb97d6d5653d5f3dacf0` with that anchor as its parent. The final audit package follows that checkpoint; its exact terminal SHA is reported in the delivery because a commit cannot embed its own SHA without changing it.

Only the eleven commissioned files under `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/ASTRA_DEEP_SYSTEM_AUDIT_R1/` are included in the audit commit. Local mirrors, dependency installation, synthetic probe scripts, and package assembly helpers are disposable audit machinery and are not production changes. No main/PRE-MAIN move, merge, project acceptance, or repair is part of this work.
