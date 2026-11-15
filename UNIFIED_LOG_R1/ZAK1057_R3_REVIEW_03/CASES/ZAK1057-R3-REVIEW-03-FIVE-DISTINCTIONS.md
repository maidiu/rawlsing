# ZAK1057-R3-REVIEW-03 — five round-two distinctions

**Review case ID:** `ZAK1057:R3:CASE:03`
**Frozen target:** `e27154883288a3265844791be0782edeaae61979::UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R2/`
**HQ receiving cut:** `2780d148d695f339f49b4dddbdf70648776e588d`
**Protected cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e`
**Verdict:** `ACCEPT_SCOPED_S1`
**Grade:** S1 static documentary only; `NOT_RUN`.

## Incoming claims

The round-two return claims: (1) the I04 `StructuralAdmissionRule` is caller-supplied and has no protected non-test producer at the declared cut; (2) checked `RequiredAuthorityBinding` resolution is distinct from carried `target_use_permission_refs`; (3) `RouteObligation.from_structural_admission` is a real receipt consumer but no operational invocation is proved; (4) the selected-QSM candidate binds to I03/Route B, not to I04; (5) B49/R157 are candidate source/C11 producers and FF/service producers are adjacent owners, not I04 producers.

## 1. Caller-supplied rule

- Definition: `6a5c12f0:rawlsing_next/pre553_structural_admission.py`, blob `fe8f706afbb5739d026846952681081b2937e9a8`, L201–L349.
- Required caller fields include `admission_authority_ref` (L204), `target_use_permission_refs` (L216), and `required_authority_bindings` (L224).
- The class verifies its own content hash at L348–L352; it does not construct itself from external material.
- Only direct constructor found: test fixture `rawlsing_next/tests/test_pre553_structural_admission.py:102–128`, blob `c754382d1c8a96bece0084233bb8ec144425b170`.
- No `from_dict`, `to_dict`, JSON loader, or materializer in the I04 module. `semantic_material` (L286–L334) is a projection, not a parser.
- Whole-tree Python symbol search: only the I04 module (4 hits) and test (2 hits); no `.py` outside `rawlsing_next`.

**Disposition:** accurate, bounded.

## 2. Checked binding versus carried permission refs

- `RequiredAuthorityBinding`: `pre553_structural_admission.py` L175–L198; fields `authority_ref`, `authority_kind`, `operation`, `source_universe_ref`, `target_use_ref`.
- Rule requirements: nonempty `target_use_permission_refs` (L253–L254); at least one binding of kind `TARGET_USE_PERMISSION` (L278–L284).
- Gate: `_resolve_binding` (L447–L478) calls `require_positive_authority` (`pre553_empirical_authority.py` L162–L203), which checks kind, operation, source-universe scope, and target-use scope against the resolved snapshot.
- Evaluator resolves every binding at L696–L704.
- `_authority_closure_material` (L514–L526) includes query/fact authority refs, requested admission ref, resolved snapshots, and `binding.authority_ref`; it does not add `rule.target_use_permission_refs`.
- Receipt copies the declared refs at L740–L742 and L793; the receipt's closure field is built at L803–L809.
- Test fixture: `PERM` is an `ExactRef` (L32); the permission authority is a separate `AuthorityRef` `pa.authority_ref` (L89–L96); the rule is built with `target_use_permission_refs=(PERM,)` (L113). No equality check between the declared `ExactRef` and the permission `AuthorityRef`.

**Disposition:** accurate as a carried-versus-checked provenance distinction. It does not prove an authorization defect or an alternate grant. The return's own qualification ("not proof that the receipt's permission refs were the granting authority") is the correct ceiling.

## 3. Real receiver versus operational invocation

- `RouteObligation.from_structural_admission`: `6a5c12f0:rawlsing_next/pre553_analytical_state_and_route.py`, blob `3a5e3db8a0897900d0b2606813bda7c3f586d46e`, L297–L450. Requires exact `AdmissionEvaluation` and canonical `StructuralEmpiricalAdmission`; reads receipt truth; rejects envelope disagreement; derives route obligation.
- Callers: `git grep from_structural_admission` finds the definition and tests only (`rawlsing_next/tests/test_pre553_analytical_state_and_route.py` L431–L1588).
- Supplementary locator L1506–L1593 is the adjacent `assert_route_not_laundered` route-legitimacy verifier, not the receiver body; the claim is supported by L297–L450.
- Generic deserializer: `pre553_carrier_execution.materialize_public_object`, blob `ee9b3af02bfca9238eb72ea45d94073d47769a07`, L73–L147. Public schema map includes `StructuralEmpiricalAdmission` at L86, not `StructuralAdmissionRule`; exact canonical preimage required.
- Issued workload: `pre553_issued_workload.py`, blob `28174766f61a15f7296f575d615462d6410cfcb6`, L1–L33, L280–L367. Imports/executes Route B/I03/I05/Batch; no I04 reference.

**Disposition:** accurate; operational invocation remains `NOT_PROVED`.

## 4. Selected-QSM candidate: I03 binding, not I04 production

- `ad17076cc95b9383ab3b28879f471026bcba9ff7:rawlsing_next/pre553_zak03s_selected_qsm_reader.py`, blob `07bd2b2c88787e8b2091e652c677864be2ba5244`.
- `SelectedQsmRequest` L74–L89; `_exact_selection` L112–L183; `execute_selected_qsm_route_b` L186–L282.
- Actual output: `SelectedQsmRouteResult(route=RouteBProductionResult, binding_receipt=...)` L92–L97, L257–L282.
- First consumer: `execute_route_b_production` L241–L249 (the real Route B producer), then the test at `tests/test_pre553_zak03s_selected_qsm_reader.py:136`; no production consumer.
- Binding receipt records `i05_historical_qsm_authority_established: False` (L279).
- Later candidate `0d90c247` keeps the same shape and adds `issued_batch_consumption_of_selected_qsm: False` (L300); still no `StructuralAdmissionRule` and no I04 call.

**Disposition:** accurate; candidate-only, unmerged, unexecuted, and not selected-QSM→I04.

## 5. B49/R157 and adjacent FF/service producers

- B49 `select_source_rules`: `b5600da96358f8526471d635a1befa8daa3f098b:rawlsing_next/pre553_inherited_source_rules.py`, blob `5f6efaceb18d92a362d065d12fdca4076d53fa16`, L255–L326, L409–L503. Produces `SelectedSourceRulePackage`/`SelectedItemRule`; no permission refs or structural-target fields.
- B49 adapter: `b5600da9:rawlsing_next/pre553_source_native_preimage_adapter.py`, blob `e27c116b9a5654a8709aff1042322dc51d3296d3`, L49–L52, L280–L365. Materializes native preimage/C11; no I04.
- R157 factory: `d81bc2c67baf933461ae6cfca468f24779cc7e44:rawlsing_next/source_configuration/factory.py`, blob `3f31f20e70a1ddd7c3880d21ecfaa6870b0c699a`, L421–L499; `structural_replay=_replay_absence(doc, "structural")` L487; no I04.
- F07: `6a5c12f0:rawlsing_next/f07_second_canary_prev3_admission.py`, blob `06c312209148ab5bdd2c2077f3c887bdc9f948c8`, L216–L264, L282; string permission refs; no I04.
- Wave1 FF: `6a5c12f0:rawlsing_next/wave1_ff_prev3_relation_admission.py`, blob `c5fb675fd6f95cb7dc9e0ad505224803839cc645`, L1–L7, L439–L464; explicitly no I04/P06; FF rule class.
- GT12 bridge: `6a5c12f0:rawlsing_next/gt12_c_to_d_relation_bridge.py`; non-test `make_gt12_c_to_d_admission_rule` and `admit_gt12_c_relation`; FF relation admission, not I04.
- Service: `pre553_service_source_applicability.py` blob `3e40caca29e8c96ee1f412f919cfc7dba63f96c4` L307–L330, L342–L364, L381–L397; `pre553_service_f8_source_scope_binding.py` blob `848d2d0eedb04b792747e9d6aaa49bb39d108a2c` L270–L300, L527–L532, L700–L730; `pre553_ee14_c1_owner_authenticated_ingress.py` blob `74e6ee826e8b6a2adebe84969fedcea5716d5b63` L342–L364. Bound inputs, not grants; no I04 construction or call.

**Disposition:** accurate; all are different owners/shapes and none closes I04 provenance.

## Omission challenge

Tested `materialize_public_object`, the `semantic_material`/hash-binding path, documentary inventory mentions of `PRE553_STRUCTURAL_ADMISSION_RULE@1.0.0`, and the GT12 FF rule producer. None constructs a protected non-test `StructuralAdmissionRule`. The negative is bounded, not global.

## Smallest revision

None required for the five distinctions. Central use should retain the return's own qualifications: bounded named-symbol absence, no security defect, no missing engine, no replacement requirement, and no runtime proof.
