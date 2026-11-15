# ZAK1057-REVIEW-03 — who produces StructuralAdmissionRule and its target-use refs?

**Review case ID:** `ZAK1057:R2:CASE:03`
**Reviewed seam:** `ZAK03:T:0004`-linked protected I04 structural-admission seam (not a new T)
**Frozen return:** `0098b058b569471e140710f11d0efe029ecb0c50::UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R1`
**Verdict:** **ACCEPT_SCOPED_S1**
**Execution:** `NOT_RUN`; S0–S1 static source/documentary only.

## Claim under review

The return claims that I04 is a real structural-admission mechanism, not a generic target-use flag; that its `StructuralAdmissionRule` is caller-supplied and has no protected selected-QSM producer; that `RouteObligation.from_structural_admission` is a real non-test static receipt consumer whose own callers are tests; that the issued-workload path executes I03/I05/Batch without I04; and that candidate selected-rule/R157 code is not protected adoption.

## Exact field-by-field producer/consumer map

### `StructuralAdmissionRule`

- Definition: `rawlsing_next/pre553_structural_admission.py`, blob `fe8f706afbb5739d026846952681081b2937e9a8`, L201–L330.
- Required fields include `admission_authority_ref`, `admission_operation`, `target_use`, allowed fact/query families, exact predicate/target semantics refs, `structural_target_identity_refs`, `focal_structural_proposition_ref`, `structural_semantic_identity_refs`, interpretation/transformation semantics, directionality/role semantics, `target_use_permission_refs`, native scope/time/estimand/measure refs, uncertainty states, disagreement policy, negative authority refs, `required_authority_bindings`, applicability, effective period, downstream producer/use, and replay semantics.
- Direct constructor at the protected cut: `rawlsing_next/tests/test_pre553_structural_admission.py:103` only.
- No non-test protected producer that derives a rule from an F03/QSM row was found. No `from_dict`/canonical materializer factory was found in the module.

### `target_use_permission_refs`

- In I04, the field is copied from the caller-supplied rule into the admission receipt at `pre553_structural_admission.py` L735–L793. The receipt records it; it does not select or create it.
- The same field name exists in distinct non-I04 paths:
  - `rawlsing_next/f07_second_canary_prev3_admission.py`, blob `06c312209148ab5bdd2c2077f3c887bdc9f948c8`, L238: a second-canary relation-admission receipt sets `[f"permission:{TARGET_USE}"]`.
  - `rawlsing_next/pre553_ee14_c1_owner_authenticated_ingress.py`, blob `74e6ee826e8b6a2adebe84969fedcea5716d5b63`, L851/L886: C1 owner-authenticated ingress relays `target_use_permission_refs` from owner-held applicability material into the service-applicability/F8 binding request.
  - `rawlsing_next/gt12_d_to_m4_typed_bridge.py`, blob `ca3d6b8d832d7ca8d959bd19e19a23b08cabde76`, L241: a GT12-D-to-M4 bridge copies `admission.target_use_permissions` into the M4 projection.
- These are field-name family members, not `StructuralAdmissionRule` provenance. Joining them to I04 by name would be a category error.

### `evaluate_structural_empirical_admission` consumer

- Definition: `pre553_structural_admission.py` L529.
- Exact call sites at protected cut: the definition plus `rawlsing_next/tests/c1_at14_at16_fixture.py`, `test_pre553_analytical_state_and_route.py`, `test_pre553_diagnostics.py`, `test_pre553_structural_admission.py`, `test_pre553_whole_machine_hostile_acceptance.py`.
- No non-test direct invocation located by name. This is a bounded negative, not global absence.

### `RouteObligation.from_structural_admission`

- Definition: `rawlsing_next/pre553_analytical_state_and_route.py`, blob `3a5e3db8a0897900d0b2606813bda7c3f586d46e`, L298–L360.
- It requires an exact `AdmissionEvaluation`, a canonical `StructuralEmpiricalAdmission` receipt, a receipt exact ref, and semantic fields; it reads decision/reason/target-use/authority/fact refs from the receipt; it rejects a hand-built evaluation whose duplicate fields disagree; and it requires a module-private trust token.
- Its own callers at the frozen cut are tests only. It is a real non-test static consumer, not a production invocation.

### Issued-workload path

- `rawlsing_next/pre553_issued_workload.py`, blob `28174766f61a15f7296f575d615462d6410cfcb6`, L1–L40 imports I03/I05/Batch/carrier/route machinery and no structural-admission module. `git grep structural_admission|StructuralAdmission` over issued-workload, native-workload binding, and source-native preimage adapter returns nothing.
- Protected B49 (`pre553_native_workload_binding.py`, blob `dac73e484f8619088f5c6701b2b6991c07540f3b`) is explicitly `TEST_ONLY_SOURCEFREE`. The protected adapter (`dd0d6960368bbac84f1711c0e496017056c343b7`) sets structural replay to typed absence and has no selected-rule import.

### Candidate boundary

- `b5600da96358f8526471d635a1befa8daa3f098b:rawlsing_next/pre553_inherited_source_rules.py`, blob `5f6efaceb18d92a362d065d12fdca4076d53fa16`, is a source-rule selector/compiler (`PRE553_SELECTED_SOURCE_RULE_PACKAGE@1.0.0`) that never constructs `StructuralAdmissionRule`.
- `d81bc2c67baf933461ae6cfca468f24779cc7e44:rawlsing_next/source_configuration/factory.py`, blob `3f31f20e70a1ddd7c3880d21ecfaa6870b0c699a`, builds `GovernedC11Projection`/C11 releases from config; its `structural_replay` is a config-supplied typed absence or replay value, not an I04 admission rule.
- Neither candidate is protected adoption.

## Findings

1. **The I04 mechanism is real and exact.** The return's structural vocabulary, precedence, and receipt fields are supported by source.
2. **The rule is caller-supplied.** No non-test protected producer or selected-QSM binding exists at the frozen cut. The only direct constructor is a test fixture.
3. **The receipt consumer is real but not a production invoker.** `RouteObligation.from_structural_admission` is a genuine non-test static consumer; its callers are tests, so the return's `NOT_PROVED` for production invocation is honest.
4. **The issued-workload path does not reach I04.** No import/call edge exists in the named files. This is not evidence that I04 is missing, only that the inspected production path does not use it.
5. **Candidate code is not protected adoption.** The candidate selector and R157 factory do different things than I04 and do not close the rule-provenance gap.
6. **Bounded omission.** `target_use_permission_refs` appears in F07/EE14/GT12 paths. These are parallel admission/materialization contracts. They do not produce a selected-QSM `StructuralAdmissionRule`, but a future field search must compare contracts, not names.
7. **Documentary lead, not a producer.** `data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/73_TRII_MANUAL_AUTHORITY_AND_STRUCTURAL_REENTRY_SCOPE_CORRECTION.md`, blob `de40588f959c09b5aff636f9965ce9e30e6cab4e`, L100–L165, states that exact I04 `StructuralAdmissionRule` authorities and their structural semantic/target-use permissions are part of the binding structural re-entry law. It names the required authority class, not a producer or selected QSM row. It is the right next documentary lead, not a counterexample to the no-producer finding.

## Verdict and smallest revision

**ACCEPT_SCOPED_S1.** No revision required. The author's next question is correctly stated: identify the exact code or documentary producer that constructs each `StructuralAdmissionRule` instance and whether it cites a selected historical QSM row/version, rather than a caller-supplied content hash. A negative answer is a typed provenance gap, not a missing engine.

## Evidence

`ZAK1057R2:EV:012`–`ZAK1057R2:EV:018`; searches `ZAK1057R2:S:007`–`S:011`.
