# 01 — exact source / owner / authority tree (HQ295 W10)

Tree base: `1616b299f97ae3b4e2b8003659f59439fcc0c77a` (sealed startup of `agent/rabochii-pyat-r3-hq295-w10-world-consumer-probe-r1`). All blobs below are the exact HEAD blobs of that commit. Owner code was imported read-only; nothing under `rawlsing_next/` was written.

## A. Reused owners actually executed by the probe

| Role in probe | Owner module (blob at HEAD) | Public symbol(s) used | Authority carried |
|---|---|---|---|
| N10E provider seam | `rawlsing_next/pre553_empirical_possibility_provider.py` (`23167aa25291fb148b1e3cf210ac33fe7769b783`) | `provide_empirical_possibility_slice`, `replay_empirical_possibility_slice`, `assert_provider_public_api_excludes_handwritten_slice`, `EmpiricalPossibilitySliceProviderReceipt/Result` | Provider contract `N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER@1.0.0`; input mode `EXACT_DETERMINANTS_ONLY__NO_PRECOMPUTED_SLICE_GEOMETRY`; refusal states `MISSING_EXACT_MODEL_OR_PRODUCER_AUTHORITY`, `SLICE_NOT_SUPPORTED_UNDER_EXACT_MODEL_LAW`, `OWNER_TYPED_REFUSAL` |
| Accepted C1 analytical composition | `rawlsing_next/pre553_analytical_composition.py` (`604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`) | `compose_positioned_subject_possibility`, `ConditionValueBindingWitness` | Producer route `DIRECT_I03_TO_POSITIONED_SUBJECT`; slice geometry schema `SLICE_GEOMETRY_SCHEMA`; no caller-supplied geometry |
| Public positioned-subject consumer | `rawlsing_next/source_backed_positioned_subject_possibility.py` (`62e5eced47b64512f47b004e3e13a6ef3fe21de7`) | `evaluate_positioned_subject_possibility`, `verify_positioned_subject_possibility_replay`, `PositionedSubjectPossibilityQuery/ModelRule/PossibilitySliceEvidence` | Purpose hard-locked `EMPIRICAL_POSSIBILITY_ONLY`; model rule rejects smoothing/interpolation; walkback requires positively listed proxy authority |
| M4 selected repository/resolver | `rawlsing_next/m4_v557_v558_publication_repository.py` (`8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360`) | `make_structural_object`, `govern_v557`, `make_producer_locator`, `build_v557_publication_bundle`, `build_v558_repository_bundle`, `make_context_query`, `exact_resolution_key`, `resolve_v558` | V557 decision `ALLOW_CONTEXT_ONLY` + permission atom `CONTEXT` only; resolver policy `V558_CONTEXT_RESOLVER_POLICY@1.0.0` (hash `4e34517b…9f6f2f`); denied/unresolved states preserved |
| M5 structural currentness / peer-prior | `rawlsing_next/m5_runtime_rsc_peer_prior.py` (`18735bdb31a220aed032aa722574d685e2bdddf5`) | `make_structural_currentness_receipt`, `materialize_resolved_structural_context`, `validate_resolved_structural_context`, `refresh_structural_currentness`, `StructuralCurrentnessState` | RSC schema `SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0`; machine signature `M4_TO_M5_RSC_MACHINE_SIGNATURE@1.0.0`; ceiling `STRUCTURAL_CONTEXT_ELIGIBILITY_ONLY__NOT_V3_MUTATION_PERMISSION`; non-CURRENT fails closed `FAIL_CLOSED_ZERO_STRUCTURAL_PEER_EFFECT` |
| Semantic identity helpers | `rawlsing_next/pre553_empirical_objects.py` (`a61365b994e5c3c50de0f598fcf40e90abf757b6`) | `canonicalize`, `semantic_hash`, `ExactRef`, `AuthorityRef` | Float/NaN-free canonical identity |
| Exact accepted empirical fixture law | `rawlsing_next/tests/n10e_empirical_slice_fixture.py` (`0e384f72fa615dc72a0dcb08a36472a64b7b1e4a`) | `build_provider_case`, `changed_source_rows`, `CHANGED_SOURCE_VARIANT` | Frozen R2/R3/R8 spine identities; AT07 bidirectional 60-row source law + `CHANGED_SOURCE_LAW` variant (70-row law) |

## B. TEST_ONLY modeled world layer (probe-owned, not owner code)

`probe/modeled_selected_world.py` builds one V558 repository per variant from 9 `W10_MODELED_ROUTE_FACT` structural objects (`producer_family=V555`, `semantic_class=W10_MODELED_ROUTE_FACT`, `typed_state=SUPPORTED`, `producer_allowed_uses=('CONTEXT',)`, governance `ALLOW_CONTEXT_ONLY`). Premise keys and families:

- institutional (drives C1): `education_institution.public_school_seat`, `education_institution.fee_barrier`, `education_institution.administrative_access`
- household/care (drives C2): `household_care.daily_time_obligation`, `household_care.support_network`
- care/time (drives C2): `labor.paid_apprenticeship`, `labor.time_cost`, `civil_routes.peer_nonformal_study`
- invariant alternative (drives C2): `civil_routes.mutual_aid`

World grade `TEST_ONLY_MODELED_SELECTED_WORLD__NOT_N9_OPERATIVE_CURRENT__NOT_OBSERVED`; declared year 2008; declared unit `ANONYMOUS_SYNTHETIC_TEST_REGION__INDIVIDUAL_OPPORTUNITY_STRUCTURE`. Variant id, premise states and grade are inside every fact payload (`spec_hash`-bound), so identity is content-addressed and rebuild-stable.

## C. Authority / permission tree actually exercised

```
TEST_ONLY modeled world facts (probe, no issuer)
  └─ V557 governance: ALLOW_CONTEXT_ONLY, v557_allowed_uses = (CONTEXT,)
       authority_ref = urn:rawlsing:hq295-w10:test-only-modeled-world-authority:r1:*  (TEST_ONLY@1.0.0)
     └─ V558 repository + OBJECT_IDENTITY index (actual M4 build)
          └─ resolve_v558(ContextQuery, requested_uses=('CONTEXT',)) -> RESOLUTION_COMPLETE
               └─ make_structural_currentness_receipt(state=CURRENT, as-of 2008 ref)
                    └─ materialize_resolved_structural_context -> RSC + validate receipt
                         └─ N10W adapter candidate (probe): C0 -> C1 -> C2 + consumer receipt
N10E lane (separate true grain)
  AT07 fixture empirical rows (synthetic source universe)
    └─ execute_empirical_query (I03) -> EmpiricalFact
         └─ compose_positioned_subject_possibility (C1) -> PossibilitySliceEvidence (computed geometry)
              └─ evaluate_positioned_subject_possibility (public consumer)
                   └─ provider receipt N10E_EMPIRICAL_SLICE_PROVIDER_RECEIPT@1
                        └─ bound into the same N10W consumer receipt (no cross-grain probability merge)
```

Separate true source and model-use grants: **none exist and none were created**. The AT07 fixture lane is a synthetic test universe; the modeled world is declared synthetic modeling. Both are labeled as such in every receipt (`epistemic_ceiling` block).

## D. Absent / blocked owners (exact missing callable boundaries)

| Boundary | State at HEAD | Evidence | Repair route (not executed here) |
|---|---|---|---|
| N10W progressive world-conditioned parent/coparent consumer | **ABSENT** — no owner module exists | `grep -r "N10W" rawlsing_next/` matches only a negating docstring in the N10E provider; ASTRA `nodes/N10W.md` status `PROPOSED_NOT_COMMISSIONED` | Smallest interface/adapter candidate in `probe/n10w_progressive_adapter.py` + `probe/test_world_consumer_probe.py`; adoption needs an authorized owner commission |
| Objective-context (J04 objective-position serving) `prev3_objective_position_v557_v558_publication.py` (`7d2a5dbb3e0979c599632645867aa48a336a8e79`) | **NOT IMPORTABLE** at this tree | `ModuleNotFoundError: No module named 'rawlsing_next.prev3_objective_position_materializer'` | Materializer exists only on `agent/rabochii-prev3-*` lanes: `8fc2a8d859a67fff81ff829c8acc2729064a12f7` (implement), `9b773a592` (replay/firewall tests), `c40a634b3` (fixture semantics), `2b3038f01` (succession/typed control); materializer blob `3c7527d3129387e8fd010b56dc981cf2e12542f7`. Owner-authorized merge of that module into this lineage is required before the J04 carrier can run |

## E. Negative / firewall owners inspected (not executed as production)

- `rawlsing_next/wsc_gt0_end_to_end.py` — GT0 harness terminal `BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS` (actor path stays blocked; probe never calls it).
- `rawlsing_next/m6_actor_safe_expression.py` — V2 claim firewall, not a persona voice engine; not invoked.
- `rawlsing_next/v3_adp010_oee_executor.py` — V3 developmental runtime; **never invoked** (actor OFF).

## F. Governance documents read (not adopted)

At exact HQ ref `0f4a798fb8d8f10a0afa494cebd8043f1582267d`: `PYAT_CONTROL_ROOM/00_INCOMING_HQ_VALIDITY_AND_PERSONA_END_PRODUCT_GATE_R1.md`, `PYAT_CONTROL_ROOM/00_WHOLE_MACHINE_AUTOMATION_DOCTRINE_R1.md`, `PYAT_CONTROL_ROOM/WHOLE_MACHINE_ASSESSMENT_AND_PLAN_20261011_R1/ACTION_PLAN.md`. ASTRA node/acceptance law read from the branch tree: `nodes/N9.md`, `nodes/N10E.md`, `nodes/N10W.md`, `acceptance/AT33.md`, `acceptance/AT34.md`, `acceptance/AT35.md`. This return creates no HQ status, no acceptance, and no estate change.
