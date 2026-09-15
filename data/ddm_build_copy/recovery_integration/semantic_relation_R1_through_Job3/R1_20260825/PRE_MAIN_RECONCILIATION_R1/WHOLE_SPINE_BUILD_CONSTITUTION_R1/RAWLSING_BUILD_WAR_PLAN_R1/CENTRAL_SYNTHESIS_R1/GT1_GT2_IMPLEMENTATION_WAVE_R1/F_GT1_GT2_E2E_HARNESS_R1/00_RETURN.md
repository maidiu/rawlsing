# RAWLSING GT12-F — GT1/GT2 END-TO-END ACCEPTANCE HARNESS R1

Status:

`PASS__GT12F_E2E_HARNESS_READY_FOR_CENTRAL_INTEGRATION`

## Identity

- repository: `maidiu/rawlsing`
- branch: `agent/rabochii-warplan-gt12-f-e2e-harness-r1`
- exact working ancestry: `2c95e64b9be9eb9c730028c840e04596dc556893`
- immutable implementation-wave instruction/evidence ref: `17b9abc5c8c3038d14670c6e68136bb868f5073a`
- frozen GT1/GT2 canary contract ref: `a9416094cbb4653dd2de2e4aa7b67577a355560c`
- worker lane: F only
- sibling GT12 implementation branches consumed: `NONE`
- PRE-MAIN/main movement: `NONE`

## Mission result

Implemented the focused merge-ready acceptance harness at:

`rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py`

This branch does not contain A-E's positive production implementations and, by law, does not consume those sibling branches.

Accordingly the harness has two deliberately distinct layers:

1. **actual integrated acceptance assertions**, which require real A-E objects and reject the old empirical M1 contract as a substitute for the new admitted-relation M1 authority;
2. **clearly labeled nonauthoritative interface fixtures**, used only to exercise current M4/M5/V3 plumbing and hostile failure behavior before fan-in.

Every stand-in is labeled:

`NONAUTHORITATIVE_INTERFACE_FIXTURE__NO_SEMANTIC_ACCEPTANCE_EFFECT`.

No stand-in is presented as a positive FIELD FORGE relation, PRE-V3 admission, relation-specific V554 authority, or GT1/GT2 acceptance result.

## Frozen acceptance constants bound in the harness

The test binds the frozen identifiers:

- GT1: `GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1`
- GT2: `GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1`
- risk set: `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`
- risk-set row count: `19,210`
- risk-set semantic member-set SHA-256: `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`
- relation: `EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0`
- admission rule: `FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0`
- admission receipt family: `PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0`
- relation M1 ingress: `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`
- basis: `ADMITTED_FIELD_FORGE_RELATION`
- signature: `V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT`
- target use: `STRUCTURAL_MEDIATION_INPUT`
- GT1 terminal: `POSITIVE_EMPIRICAL_FACT__NO_STRUCTURAL_OR_ACTOR_PROMOTION_PASS`
- GT2 terminal: `POSITIVE_PREV3_STRUCTURAL_WORLD__V3_ZERO_EFFECT_PASS`

## Integrated GT1 acceptance assertion

`assert_gt1_positive_fact(...)` requires an actual current `EmpiricalFact` and proves at the harness grain:

- positive `SUPPORTED` fact state;
- exact 19,210 denominator;
- RAW/unweighted shape by requiring no weighted numerator/denominator material;
- optional exact query-ref and risk-set-ref equality;
- PRE553 empirical object has exact zero actor/V3/V2 effect;
- no `StructuralEmpiricalAdmission` substitution;
- no strong-noun semantic promotion.

The final central integration test must supply the actual GT1 fact produced by current I03 after A+B integration.

## Integrated GT2 acceptance assertion

`assert_integrated_gt2_acceptance(IntegratedGT2Artifacts(...))` is intentionally stricter than the pre-fan-in interface fixture.

It requires:

- actual positive GT2 joint `EmpiricalFact`;
- FIELD FORGE relation and PRE-V3 admission are neither `EmpiricalFact` nor `StructuralEmpiricalAdmission`;
- no blocked FIELD/CAPITAL/HEGEMONY/HOMOLOGY/PRESSURE/MECHANISM semantic class;
- actual `M1Evaluation`;
- exact contract `M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0`;
- exact basis `ADMITTED_FIELD_FORGE_RELATION`;
- `M1DecisionState.ELIGIBLE`;
- one canonical positive basis;
- F1 and B1 present;
- direct `V554_TO_V557_DIRECT` handoff;
- exact M1 object-id/hash preservation into V557 publication and V558 repository;
- publication/repository producer family remains exactly V554;
- no V555 or V556 objects;
- deterministic actual `resolve_v558(...)` replay equals the supplied resolution;
- exact permission subset conservation:
  `resolver_allowed_uses ⊆ v557_allowed_uses ⊆ producer_allowed_uses`;
- optional actual M5 `ResolvedStructuralContext` remains free of belief/memory/persona/actor-causal-state fields;
- actual production `evaluate_psepf_zero_positive_guard(...)` is traversed;
- production positive-transition registry remains exactly empty;
- terminal guard outcome is `DENY_ZERO_EFFECT`;
- no delegated positive owner;
- zero actor-state effect;
- zero causal-ledger append;
- zero causal-cursor delta;
- zero RNG mutation;
- zero scheduler mutation;
- exact pre/post guard fingerprint equality.

The helper returns the frozen GT2 acceptance terminal only after all those checks pass.

## Deliberate pre-fan-in rejection

The local nonauthoritative downstream fixture uses the old current empirical M1 contract only to exercise existing M4/M5/V3 APIs.

The test:

`test_integrated_acceptance_rejects_empirical_contract_as_relation_m1_authority`

proves that this fixture cannot accidentally satisfy the integrated GT2 acceptance assertion.

Therefore:

`CURRENT_EMPIRICAL_M1_INTERFACE_FIXTURE != GT2_RELATION_M1_AUTHORITY`.

Central fan-in must wire the real E output before the GT2 terminal can be claimed.

## Current downstream APIs exercised by the fixture

The test uses the actual current:

- `M1Evaluation` shape;
- `m4.structural_objects_from_m1(...)`;
- `m4.govern_v557(...)`;
- `m4.build_v557_publication_bundle(...)`;
- `m4.make_producer_locator(...)`;
- `m4.build_v558_repository_bundle(...)`;
- `m4.make_context_query(...)`;
- `m4.resolve_v558(...)`;
- `m5.make_structural_currentness_receipt(...)`;
- `m5.materialize_resolved_structural_context(...)`;
- `m5.validate_resolved_structural_context(...)`;
- `v3.evaluate_psepf_zero_positive_guard(...)`.

No V555/V556 API is invoked.

## Hostile matrix implemented

Nine focused tests are present.

1. interface fixture carries explicit no-authority marker;
2. GT1 assertion accepts only a positive empirical fact and rejects a non-fact;
3. downstream fixture traverses actual M4→M5→V3 and proves zero effect with no V555/V556;
4. V557 permission widening fails closed;
5. V558 repository hash corruption fails closed;
6. V558 exact query hash corruption fails closed;
7. reverse-lane V3/actor structural object is rejected by actual M4 publication;
8. I04 coercion and blocked strong-noun promotion are rejected;
9. integrated GT2 assertion rejects the old empirical M1 contract as relation authority.

This covers the required hostile classes:

- I04/M1 coercion;
- strong-noun promotion;
- actor leakage;
- permission widening;
- exact-ref/hash corruption.

## Changed files

Exactly two files are intended on this branch:

1. `rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py`
2. `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_IMPLEMENTATION_WAVE_R1/F_GT1_GT2_E2E_HARNESS_R1/00_RETURN.md`

No production runtime module is changed by F.

## Test execution status

The harness source was syntax-validated before commit.

A real repository checkout/pytest executor is not available through this connected GitHub execution surface, so this worker does **not** fabricate a pytest PASS count.

At central integration, run the focused path:

`python -m pytest -q rawlsing_next/tests/test_wave1_gt1_gt2_positive_prev3_integration.py`

under W1G's frozen environment law, then include the W1F inherited regression subset:

- `rawlsing_next/tests/test_m1_temporal_v554_admission_dedup.py`
- `rawlsing_next/tests/test_m4_v557_v558_publication_repository.py`
- `rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py`
- `rawlsing_next/tests/test_psepf_zero_positive_guard.py`
- `rawlsing_next/tests/test_whole_machine_integration.py`

and the claim-triggered I03/source-backed/I04 tests selected by central integration.

The GT1 and GT2 acceptance terminals must not be reported from this sibling-blind F branch; they become executable claims only after actual A-E integration.

## Terminal

`PASS__GT12F_E2E_HARNESS_READY_FOR_CENTRAL_INTEGRATION`
