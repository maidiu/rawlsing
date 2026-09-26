# PYAT R1-D — EVIDENCE MAP

Exact launch base: `8b8597542af5d24dec4fe92adad4c7bb1147850d`.

## Binding baseline

Primary Dva architecture / seam / release surfaces:
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`
- `.../SEAM_INTEGRITY_CLOSURE_RULING.md`
- `.../V553_COMPLETION_IMPLEMENTATION_RULING.md`
- `.../V554_COMPLETION_IMPLEMENTATION_RULING.md`
- `.../V555_COMPLETION_IMPLEMENTATION_RULING.md`
- `.../V556_COMPLETION_IMPLEMENTATION_RULING.md`
- `.../V557_V558_COMPLETION_IMPLEMENTATION_RULING.md`
- `.../IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`
- `.../W0_AUTHORITY_FOUNDATION_CLOSURE_RULING.md`
- `.../W1_AUTHORITY_EXPANSION_CLOSURE_RULING.md`
- `.../W2_FINAL_BATCH_ADJUDICATION_RULING.md`

Current inheritance/currentness:
- `PYAT_CONTROL_ROOM/02_GOVERNING_INHERITANCE.md`
- `PYAT_CONTROL_ROOM/03_RECONNAISSANCE_DAG.md`
- `PYAT_CONTROL_ROOM/07_PREDECESSOR_HQ_SYNTHESIS.md`
- W42 Dva inheritance `CONCEPTUAL_CONTRIBUTIONS.tsv`, `PROBLEM_LEDGER.tsv`, `RETURN_REQUIRED.tsv`, `SUCCESSION_AND_CHALLENGE.tsv`.

## Current implementation blobs at launch base

| Surface | Blob SHA | Current finding |
|---|---|---|
| `rawlsing_next/m1_temporal_v554_admission_dedup.py` | `e8bd6376720a2de132b384e7771d71d8d39cf261` | exact direct/V553 basis intake; F1/F2/B1; valid-empty/negative/integrity separation |
| `rawlsing_next/m1_admitted_field_forge_relation_v554_ingress.py` | `0aeacd9e66c7e4340b36e1b622bb5c9bf2865fd5` | current admitted Field Forge relation→V554 ingress |
| `rawlsing_next/m2_v555_atomic_route.py` | `deef8a60613635a10faf7d89cd8cdf0c3b8a0710` | one-F1 atomic route; seven-field identity; F2 reference-only; actor-independent |
| `rawlsing_next/m3_v556_higher_order_structural.py` | `9a4b26b214686364a43d108dabf0d57dac0ed3b2` | R2 exact-rule/result-contract firewall; 2..n role/order/cardinality/multiplicity |
| `rawlsing_next/m4_v557_v558_publication_repository.py` | `8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360` | V557 governance + immutable V558 repository + exact-key resolver |
| `rawlsing_next/m5_runtime_rsc_peer_prior.py` | `18735bdb31a220aed032aa722574d685e2bdddf5` | RSC materialization/validation/currentness + structural peer use |
| `rawlsing_next/tests/test_whole_machine_integration.py` | `e5fb1c4f5cc1979bbd0bbc38b48a2f03d318f72d` | import/composition-oriented proof surface |
| `rawlsing_next/tests/pre553_reservoir_harness.py` | `c2c9752d745b06fa34c4e1c3345d90de7e66feea` | explicitly test-only PRE553→V558 fixture wiring |

Focused proof blobs:
- M1 tests: `e6471ace122466988bb17019f70816a59a04f1f7`
- Field Forge M1 tests: `e6a456865470fe587aae9480a81eb2ccbc8b7b51`
- M2 tests: `8c641da532889f0a43e6bd4a5dbb5f8f0fb711ce`
- M3 tests: `0276bd18282216853ba1f92e558db767d8c1f9ec`
- M4 tests: `f29a06ba2d3e43786a5562cae86a356721c6b922`
- M5 tests: `ef4faaa84b24b9b6ca62ae7eaa29018d57439c0c`

## Exact current authority succession used

- ADP-001 / `V554_AFFORDANCE_RULE_REGISTRY`: accepted in W0.
- CAN-001 / V554 applicability predicate/evaluator canonicalization: W1 closure records 18/18 accepted.
- ADP-002 / `V555_MEDIATION_ROUTE_RULE_REGISTRY@1.0.0`: accepted in W1; first tranche exact upstream structural-channel route.
- ADP-003 / V555 route-predicate authority: accepted by W2/current inheritance.
- CAN-003 / V557 runtime-use governance: accepted W0.
- ADP-006 / temporal-proxy eligibility: accepted W0.
- CAN-004 / immutable V557→V558 bundle policy: accepted W2.
- CAN-005 / `V558_CONTEXT_RESOLVER_POLICY@1.0.0`: accepted W2.
- CAN-007 / static next-context-change vs generated-life requery: accepted W2.
- Dva W3 ADP-004 / CAN-002 / ADP-005: inherited W42 records them as stranded/unreturned; do not treat launch registers as accepted production authority.

## Proof versus composition rule used

A unit/hostile fixture proving that a module rejects fuzzy authority or preserves n-ary cardinality establishes code behavior only. It does not establish that a real current producer supplies the necessary authority/object at production grain.

The clearest explicit warning is `rawlsing_next/tests/pre553_reservoir_harness.py`: it declares `semantic_authority=False`, `runtime_authority=False`, `admission_decision_service=False`, and `fixture_content_is_authority=False`.

## Concrete code differential

### Dva laws now materially implemented
- exact one-affordance-per-route;
- no `seed_rows[:5]`/universal slot semantic authority;
- inherited V554 F2 reference-only;
- V555 route reused as V556 participant/base identity;
- no implicit cross-source composition;
- n-ary participant roles/order/cardinality/multiplicity preserved;
- producer permission ≥ V557 permission ≥ resolver permission;
- positive/negative required dependency closure;
- immutable producer-preserving repository locators;
- no `latest/default/*` fuzzy identity in M4;
- structural peer context has `actor_state_effect=False`.

### Current residual implementation mismatch
M3 R2:
`SCR556_CONTRACT_ID = "SCR556_V556_INTERACTION_TOPOLOGY_EXACT_CONTRACT@scr556.v2"`.

M4 `structural_object_from_m3`:
`schema_id=SCR556_CONTRACT_ID` but `schema_version="scr556.v1"`.

That combination is internally contradictory provenance/version metadata.

### Current partial V558 resolver
M4 declares mandatory logical indexes including TEMPORAL, GEOGRAPHIC, FINITE_STRATUM, GENERATED_POSITION_REQUIREMENT and NEGATIVE_LIMIT, but its active `resolve_v558` lookup loop consumes only the OBJECT_IDENTITY index and item permissions/closure. The accepted CAN-005 temporal precedence and CAN-007 refresh behavior therefore remain unimplemented in this resolver surface.
