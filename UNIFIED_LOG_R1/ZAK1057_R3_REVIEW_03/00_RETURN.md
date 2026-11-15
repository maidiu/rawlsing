# 00_RETURN — ZAK1057 R3 independent review of lane03 round2

**Review ID:** `ZAK1057:R3:REVIEW:03`
**Lane:** 03 / independent nonauthor documentary review
**Frozen target:** `e27154883288a3265844791be0782edeaae61979::UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R2/`
**HQ receiving cut:** `2780d148d695f339f49b4dddbdf70648776e588d`
**Protected PRE-MAIN cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e` (read-only; unchanged)
**Role:** genuinely distinct nonauthor reviewer; no author-return, product, HQ-index, or other-worker edits.
**Output root:** `UNIFIED_LOG_R1/ZAK1057_R3_REVIEW_03/`

## Disposition

`ACCEPT_SCOPED_S1`

The five new source distinctions are accurate at S1 static documentary grade. No exact material documentary defect was found. Existing independently accepted round-one claims are preserved, not re-reviewed. No security defect, missing engine, replacement requirement, runtime invocation, adoption, or protected integration is claimed.

## Frozen target and intake checks

- HQ `ROUND2/03_HQ_RECEIVING_NOTE.md` and `03_INTAKE_DISPOSITION.json` read as receiving context, never as proof.
- The frozen `EVIDENCE.tsv` (24 atomic rows), `00_RETURN.md`, case file, and supporting TSVs were read directly.
- All 19 declared payload files in `03_INTAKE_DISPOSITION.json` match their SHA-256 and byte counts at the frozen target; 19/19 verified locally. In particular `EVIDENCE.tsv` is `76a548956d4b84223bda80e303671c31f4e3a83bc411f5950f327626c0f50031` (13,723 bytes) and `00_RETURN.md` is `1462882ae523f11f7761a7e1b81ea10f935128be25b90c0bdb03b4f4cd515b39` (11,009 bytes).
- The known `00_RETURN.md` paragraph-citation misnumbering was not re-litigated. This review uses the actual `EVIDENCE.tsv` rows and the HQ corrected crosswalk. A sentence-level wording caution remains below, but it is not a material source-claim defect.

## Accepted scope: the five round-two distinctions

### 1. A caller-supplied `StructuralAdmissionRule` is distinguished correctly

`StructuralAdmissionRule` is defined at `6a5c12f0:rawlsing_next/pre553_structural_admission.py`, blob `fe8f706afbb5739d026846952681081b2937e9a8`, L201–L349. Its fields, including `target_use_permission_refs` (L216), `required_authority_bindings` (L224), and `admission_authority_ref` (L204), are supplied by the constructor caller; `verify_content_hash_binding()` (L348–L352) only checks the already-constructed rule against its content hash.

The only direct constructor found at the protected cut is the test fixture `rawlsing_next/tests/test_pre553_structural_admission.py:102–128`, blob `c754382d1c8a96bece0084233bb8ec144425b170`. The module contains no `from_dict`, `to_dict`, JSON loader, or materializer; `semantic_material` (L286–L334) is a hash projection, not an inverse constructor. A whole-tree Python search for `StructuralAdmissionRule` returns only the I04 module (4 hits, definition/annotations/export) and the test fixture (2 hits); no `.py` outside `rawlsing_next` contains the symbol.

**Verdict:** accurate. The negative is bounded to protected Git/Python source and to direct/named constructor, deserializer, and materializer forms; it is not a global absence claim.

### 2. Checked `RequiredAuthorityBinding` versus carried `target_use_permission_refs` is accurate

`RequiredAuthorityBinding` is defined at `pre553_structural_admission.py` L175–L198. A rule must have nonempty `target_use_permission_refs` (L253–L254) and at least one binding of kind `TARGET_USE_PERMISSION` (L278–L284). Evaluation resolves each binding through `_resolve_binding` (L447–L478) and `require_positive_authority`, which checks the binding's `authority_kind`, `operation`, `source_universe_ref`, and `target_use_ref` against the resolved snapshot (L696–L704; authority side `pre553_empirical_authority.py` L162–L203).

The declared `rule.target_use_permission_refs` are copied into the receipt at L740–L742 and L793; `_authority_closure_material` (L514–L526) includes query/fact authority refs, the requested admission ref, resolved snapshots, and the rule's `binding.authority_ref` values, but not the rule's declared permission `ExactRef` tuple. The test fixture uses a permission `ExactRef` `PERM` and a separate permission `AuthorityRef` `pa.authority_ref` (test L32, L89–L96, L102–L128); no I04 code compares them for equality.

**Verdict:** accurate as a carried-ref versus checked-binding provenance distinction. It supports the weaker, exact assertion that the declared refs are not the gate. It does not by itself establish an authorization defect, an alternate granting authority, or a required evaluator edit; the return itself so qualifies. The phrase "declared-ref versus checked-binding gap" must remain provenance-scoped. The `00_RETURN` phrase "same tag" is imprecise (the fixture's `ExactRef` and `AuthorityRef` have different identifiers; what they share is the permission authority kind), but the underlying `EVIDENCE.tsv` row EV006 is correct.

### 3. A real I04 receipt consumer is distinguished from demonstrated operational invocation

`RouteObligation.from_structural_admission` is a real non-test static receiver at `6a5c12f0:rawlsing_next/pre553_analytical_state_and_route.py`, blob `3a5e3db8a0897900d0b2606813bda7c3f586d46e`, L297–L450. It requires an exact `AdmissionEvaluation` and canonical `StructuralEmpiricalAdmission`, reads receipt truth, rejects envelope disagreement, and derives the route obligation. Its callers at the protected cut are tests only (`git grep from_structural_admission` finds the definition and test calls). The supplementary locator L1506–L1593 is the adjacent `assert_route_not_laundered` route-legitimacy verifier, not the receiver body; the receiver claim is supported by L297–L450.

`pre553_carrier_execution.materialize_public_object` is a generic public-object deserializer, `6a5c12f0:rawlsing_next/pre553_carrier_execution.py`, blob `ee9b3af02bfca9238eb72ea45d94073d47769a07`, L73–L147. Its schema map includes `StructuralEmpiricalAdmission` (L86) but not `StructuralAdmissionRule`, and it requires a full canonical public preimage. `execute_issued_workload` (`pre553_issued_workload.py`, blob `28174766f61a15f7296f575d615462d6410cfcb6`, L1–L33, L280–L367) imports and executes Route B/I03/I05/Batch and contains no I04 import or call.

**Verdict:** accurate. The receiver exists and is real; operational invocation remains `NOT_PROVED`. No runtime execution was forced.

### 4. Candidate selected-QSM→I03 binding is distinguished from selected-QSM→I04 production

At candidate `ad17076cc95b9383ab3b28879f471026bcba9ff7`, `rawlsing_next/pre553_zak03s_selected_qsm_reader.py`, blob `07bd2b2c88787e8b2091e652c677864be2ba5244`, `SelectedQsmRequest` binds caller-selected path, file SHA, row hash, authority version, rule id, source family/wave/country/var, native question ref, and a separate target-use triple (L74–L89). `_exact_selection` checks file identity, row identity, source scope, and a unique same-code C11 response slot (L112–L183). `execute_selected_qsm_route_b` requires the target-use triple in each I03 request and calls `execute_route_b_production` (L186–L249). Its actual output is `SelectedQsmRouteResult(route=RouteBProductionResult, binding_receipt=...)` (L92–L97, L257–L282); the binding receipt records `i05_historical_qsm_authority_established: False` (L279). The first consumer in the candidate cut is the test suite at `rawlsing_next/tests/test_pre553_zak03s_selected_qsm_reader.py:136`; no production consumer is demonstrated. The later candidate `0d90c247` keeps the same shape and adds `issued_batch_consumption_of_selected_qsm: False` (L300), still without `StructuralAdmissionRule` or an I04 call.

**Verdict:** accurate. The selected QSM is a gate/provenance binding into Route B/I03, not a producer of an I04 rule or receipt. Candidate-only, unmerged, and unexecuted.

### 5. B49/R157 source/C11 producers and adjacent FF/service producers are distinguished correctly

- B49 `select_source_rules` at `b5600da96358f8526471d635a1befa8daa3f098b:rawlsing_next/pre553_inherited_source_rules.py`, blob `5f6efaceb18d92a362d065d12fdca4076d53fa16`, L255–L326, L409–L503, produces `SelectedSourceRulePackage`/`SelectedItemRule` with source-variable, disposition, direction, status, evidence refs, and exact identity hash; no `target_use_permission_refs` or structural-target fields. Its adapter at `b5600da9:rawlsing_next/pre553_source_native_preimage_adapter.py`, blob `e27c116b9a5654a8709aff1042322dc51d3296d3`, L49–L52, L280–L365, materializes a native preimage/C11 bundle and contains no I04 or structural-admission reference.
- R157 `build_governed_c11_projection` at `d81bc2c67baf933461ae6cfca468f24779cc7e44:rawlsing_next/source_configuration/factory.py`, blob `3f31f20e70a1ddd7c3880d21ecfaa6870b0c699a`, L421–L499, constructs `GovernedC11Projection` and sets `structural_replay=_replay_absence(doc, "structural")` (L487); it does not construct an I04 rule.
- Adjacent FF/service producers are different owners and field shapes, not I04 producers. F07 `6a5c12f0:rawlsing_next/f07_second_canary_prev3_admission.py`, blob `06c312209148ab5bdd2c2077f3c887bdc9f948c8`, L216–L264, L282, constructs a claim-specific receipt with string permission refs `[f"permission:{TARGET_USE}"]`; `wave1_ff_prev3_relation_admission.py`, blob `c5fb675fd6f95cb7dc9e0ad505224803839cc645`, L1–L7 explicitly says it does not call I04/P06 and L439–L464 defines an FF `FieldForgeRelationAdmissionRule`; `gt12_c_to_d_relation_bridge.py` similarly produces FF relation admission, not `StructuralAdmissionRule`.
- Service paths `pre553_service_source_applicability.py` (blob `3e40caca29e8c96ee1f412f919cfc7dba63f96c4`, L307–L330, L342–L364, L381–L397), `pre553_service_f8_source_scope_binding.py` (blob `848d2d0eedb04b792747e9d6aaa49bb39d108a2c`, L270–L300, L527–L532, L700–L730), and `pre553_ee14_c1_owner_authenticated_ingress.py` (blob `74e6ee826e8b6a2adebe84969fedcea5716d5b63`, L342–L364) treat permission refs as bound inputs, not grants, and none constructs an I04 rule or calls the evaluator.

**Verdict:** accurate. B49/R157 are candidate source/C11 producers; FF/service producers are adjacent-owner contracts. None closes the I04 rule provenance edge.

## Round-one preservation

The already independently accepted round-one 03 claims remain intact and are not re-reviewed here: the I04 rule is caller-supplied; `RouteObligation.from_structural_admission` is a real static receipt consumer whose callers are tests; the issued-workload path does not invoke I04; and the candidate source-rule selector is not protected adoption. This review adds only the round-two delta: the historical F03 field evidence, the binding-versus-carried-ref detail, the candidate selected-QSM/I03 edge, and the adjacent FF/service producer map. The round-one verdict `ACCEPT_SCOPED_S1` for lane 03 is preserved.

## Material defects

None. No exact material documentary defect in the round-two source claims was found. The following are non-material notes, recorded so central use does not re-inflate them:

1. `00_RETURN` paragraph citation numbers are misaligned; the HQ note already says to use `EVIDENCE.tsv`. This review did so.
2. `EVIDENCE` EV007's supplementary locator L1506–L1593 is the adjacent anti-laundering verifier, not the body of `from_structural_admission`; the claim is independently supported by L297–L450. The locator is overbroad, not false.
3. `00_RETURN`'s "same tag" wording is imprecise; the fixture uses different `ExactRef`/`AuthorityRef` identifiers with the same permission authority kind. EV006 itself is exact.
4. EV023's "whole-tree" wording should be read as the protected Git/Python tree searched for the class symbol. Documentary/data-inventory mentions exist outside `rawlsing_next` (for example the LW-F16 inventory row and the H046 disposition row), but no code constructor was found. That is a scope clarification, not a global absence claim.
5. The `00_RETURN` body paragraph names F07 and wave1 FF but not `gt12_c_to_d_relation_bridge.py`; the producer/consumer map row does acknowledge "GT12 FF rule". The GT12 bridge constructs an FF relation rule, not an I04 rule, so the distinction is unaffected.

## One bounded omitted-producer challenge

**Challenge:** Could the strongest generic alternative construct a protected non-test `StructuralAdmissionRule`?

Tested alternatives:

- `pre553_carrier_execution.materialize_public_object`: exact source L73–L88 maps public schemas, including `StructuralEmpiricalAdmission`, but not `StructuralAdmissionRule`; L103–L147 re-materializes only a full canonical public preimage. It cannot construct the rule.
- `StructuralAdmissionRule.semantic_material` plus `verify_content_hash_binding` (I04 L286–L352): these hash and verify an already-constructed rule; there is no inverse `semantic_hash` constructor, no `from_dict`, and no JSON loader.
- The LW-F16 current-function inventory row and H046 disposition row mention `PRE553_STRUCTURAL_ADMISSION_RULE@1.0.0` and the GT1/GT2 adopted admission hash `a445e43d...`. Direct inspection shows documentary crosswalk text about FF relation admission, not a code producer; no `.py` outside `rawlsing_next` contains `StructuralAdmissionRule`.
- `gt12_c_to_d_relation_bridge.py` has a non-test `make_gt12_c_to_d_admission_rule` and `admit_gt12_c_relation`; inspected as a concrete adjacent-owner counterexample. It constructs a `FieldForgeRelationAdmissionRule`, not `StructuralAdmissionRule`, and does not import I04.

**Challenge result:** the no-protected-non-test-rule-producer negative survives these bounded alternatives. It remains a bounded named-symbol/direct-constructor negative, not a claim of global or generated-code absence, and it does not require a new engine or an execution run.

## Unresolved edges

- Protected non-test invocation of `evaluate_structural_empirical_admission`: `NOT_PROVED` at the inspected cut; no runtime run.
- Non-test caller of `RouteObligation.from_structural_admission`: `NOT_FOUND` at the inspected cut; callers are tests.
- C11 `StructuralAdmissionReplayBinding` `PRESENT` produced from an `ADMITTED` evaluation: `NOT_PROVED`.
- Selected-QSM→I04 rule/receipt production: `NOT_FOUND` at the inspected protected and candidate cuts; candidate selected-QSM stops at Route B/I03.
- Historical selected QSM exact file/version/row payload and original execution receipt: `UNKNOWN`.
- Adoption of B49, R157, selected-QSM, or FF/service candidates: `NOT_PROVED`; none is protected adoption.
- Generated/dynamic constructors outside Git, or runtime reflection: not visible; no global absence inferred.
- No security defect, missing engine, replacement requirement, or protected integration is claimed.

## Runtime, cost, and publication

- Actual start: `2026-11-14T23:56:42-0500` (`2026-11-15T04:56:42Z`).
- Actual end: recorded in `REVIEW_VERDICT.json` and the commit metadata; the run was packaged within the 30-minute bound.
- Session model context: `opencode-go/deepseek-v4.1-flash`. The `MAX` variant and provider routing are not independently exposed by the local shell/config; actual provider/model settings beyond the session context are `UNKNOWN`. No provider/model change and no subagents.
- Token usage: `UNKNOWN` (not exposed in-session).
- Cost: `UNKNOWN` estimate; no billing/account fields exposed. This is not an invoice or allowance statement.
- Retries: 0 observed command retries; provider-level retries `UNKNOWN`.
- Publication: local branch `docs/zak1057-r3-review-03-mainmac-20261115-r1` from the HQ cut. Push status is recorded in `REVIEW_VERDICT.json`; if authenticated publishing is unavailable, the local commit is preserved and the limitation is stated there.

## Terminal sentence

**Five round-two distinctions are source-accurate at S1; no material documentary defect; round-one accepted claims preserved; rule provenance remains a bounded, honest `NOT_FOUND`/`NOT_PROVED` edge, not a global absence, security defect, missing engine, replacement requirement, or runtime claim.**
