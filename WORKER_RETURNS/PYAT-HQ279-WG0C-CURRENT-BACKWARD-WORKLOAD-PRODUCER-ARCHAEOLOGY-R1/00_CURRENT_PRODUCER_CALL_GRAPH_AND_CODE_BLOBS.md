# HQ279 WG0-C — CURRENT backward dependency court

**Worker:** WG0-C; independent current-code and authority-graph investigation. **Exact sealed commission:** `96368a4055316d14b275a8356a6d83c2c22774bc` (commission blob `943923f5996ed1d1ef0f1985a44586002f5c128f`). **Frozen inspected control:** `288316c6d9ecac9a92f5fb1c9f1bc1e1c5d5f44c`; branch `agent/rabochii-pyat-hq279-wg0c-current-backward-workload-producer-archaeology-r1`. **Runtime:** static GitHub exact-content/file inspection only; no Python/test execution, source raw reads, output claims, or authority minting. **Actual executor:** GPT-6 via Browser/GitHub connector; user-requested High effort cannot be independently attested by the repository. Machine/worktree not established.

## A. Backward graph: exact calls, producers and first external-origin edges

```text
ORIGINAL instrument instances, response options, route/form, respondent/household,
source-native risk sets, design/weight/estimand, permitted operation classes
  ├─ [NO VERIFIED CLOSED35 qualified original-item/operation factory feeding ALL below]
  └─ physical metadata only: pre553_physical_decoder._decode
          └─ PhysicalSourceIncidence.variables / PhysicalCell stream
                  ├─ source-local universe SourceLocalUniverseSpec [caller specified]
                  │    └─ materialize_source_local_universe -> EmpiricalUniverse
                  └─ GovernedC11Projection [caller/specific qualified projection builder]
                       └─ bind_governed_c11_projection [binds fields, NO inference]
                             └─ project_c11_candidate_from_physical_cells
                                   -> validated C11LogicalRelease + repository
                                        └─ execute_route_b_production
                         [requires separately passed RuntimeObjectCatalog,
                          i03_requests, discovery_authority_ref]
RuntimeObjectCatalog.from_documents [caller provides immutable authority,
  predicate, query, discovery-authority documents; validates exact closure]
  ├─ execute_route_b_production:
  │     each I03ExecutionRequest -> CarrierNeutralResearchExecutor.execute_i03
  │       -> execute_empirical_query(query, predicate, registry, releases)
  │     exact discovery_authority_ref -> CarrierNeutralResearchExecutor.execute_i05
  │       -> execute_exact_bounded_discovery(DiscoveryAuthority,
  │            predicate_catalog, query_template_catalog, registry, releases)
  │            -> _verify_discovery_authority -> _catalog_atoms / _catalog_templates
  │            -> _compile_frontier -> candidates FROZEN BEFORE execute_empirical_query
  │            -> terminal exact scoped facts/receipts + replay graph
  └─ separate public analytic consumers:
       pre553_analytical_composition.compose_positioned_subject_possibility
         [prepared empirical query OR admitted I05 result OR recursive handoff]
       pre553_learned_world_composition.build_m1_bundle_from_m01
         [M01 result -> existing learned M1 route]
Separate, NOT called by M01 and NOT a workload factory:
  pre553_recursive_handoff.execute_exact_bounded_discovery_with_handoffs
       -> caller catalogs -> I05 -> supported winning branches -> handoffs
  pre553_discovery_adaptive.execute_adaptive_exploration
       <- admitted policy + supplied roots + evaluate_unit callback
       -> sealed proposals can extend *exploratory* reachable units only
  pre553_batch_runner.BatchManifest(units=caller BatchUnitSpec tuple)
       -> BatchExecutionRunner(manifest, repository, executors) -> receipts/resume
       [NO observed M01 -> closed35 BatchManifest constructor edge]
```

At every edge **an accepted contract to receive items is not an issuer certifying that all eligible original items exist in that input**. These are separate provenance questions.

## B. Exact source and current-owner code anchors

Every path below was directly retrieved from the frozen HEAD by GitHub `fetch_file(path,ref)`; the SHA is that file's Git blob. Line spans identify decisive functions; no SHA is an execution receipt.

| Current file / Git blob | Exact owner / lines | Inputs → constructed output; scientific/authority ceiling |
| --- | --- | --- |
| `pre553_physical_decoder.py` · `d2a074a41fb556a1cd5928a5fe1421ef3672a4e5` | `_decode` 439–522; `PhysicalSourceIncidence` 69–155 | Enumerates physical source columns, labels, missing declarations, MR metadata from reader; not original questionnaire item/form/option semantic admission. |
| `pre553_source_local_universe_admission.py` · `b968fa16c6620cd06b191ebdb5da7da86f524393` | `SourceLocalUniverseSpec` 189–260; `validate_source_local_admission_authority` 270–358; `materialize_source_local_universe` 359–408 | Caller documents source, instrument, respondent namespace, population/design refs. Exact ALLOW admission produces **SOURCE_LOCAL_ONLY / RAW_ONLY** universe; expressly denies population generalization absent separate authority. |
| `pre553_source_backed_c11_facade.py` · `8a761119e4a8d68eb291fc4edfadb52e027f8284` | `GovernedC11Projection` 264–354; `project_c11_candidate_from_physical_cells` 498–575; `build_source_backed_c11_repository` 642–655 | Projection supplied with full **chosen** response, coordinate, weight, route/row/authority assignments. Physical cell whose slot is not in supplied projected union is **skipped** (line ~517): scoped C11 correctness is not questionnaire-wide coverage. Every projected cell/value is checked; no raw value → meaning inference. |
| `pre553_carrier_execution.py` · `e7cda773e6a2426bfa12b22790fd8e005fe75153` | `bind_governed_c11_projection` 164–189; `RuntimeObjectCatalog.from_documents` 314–344; `CarrierNeutralResearchExecutor.execute_i03/execute_i05` 427–465 | The binder requires every projection field already supplied; docstring forbids source lookup, label interpretation, defaulting. Catalog materializes **caller documents** and validates exact closure, not original-source completeness. Executors invoke existing operators. |
| `pre553_route_b_production.py` · `2385cd327dced3c5b887b59085aa0d21b04d78c3` | `I03ExecutionRequest` 105–130; `_normalize_i03_requests` 226–251; `execute_route_b_production` 494–630 | Validates same source SHA, projection authorization, builds source-backed C11 once, loops **supplied** I03 requests and invokes I05 against **supplied** discovery ref, emits exact object/replay receipts. No closed35 item/operation assembler. |
| `pre553_empirical_query.py` · `03facecf70890bfd13b80418620d274cbcd69d02` | `_require_exact_i03_authority_fitness` 228–371; `execute_empirical_query` 373–540 | Requires query+predicate already constructed, exact source/risk/measure refs and operation/family/source/use authority; returns queried facts or typed nonpositive outcomes, not item enumeration. |
| `_pre553_query_predicate.py` · `8590bacf464b2c61f319f581820a3af76ed1e60c`; `_pre553_query_eval.py` · `f808dfcd2008cc71e9203de3cadf1abe14223974` | Query predicate/evaluator owners | Implements predicate algebra/evaluation; neither establishes an original survey source inventory or supplies exact governed requests by itself. |
| `pre553_empirical_objects.py` · `a61365b994e5c3c50de0f598fcf40e90abf757b6` | `EmpiricalPredicate` 631, `EmpiricalQuerySpec` 677, `DiscoveryAuthority` 727 | Canonical typed object definitions/identity; not independent issuing authorities. |
| `pre553_empirical_authority.py` · `ca65a7fd4d52f0c44447434559b1d09412e7aa39`; `pre553_runtime_authority.py` · `896c7094124a4aaea23eec550178e4bf8e73ac68` | `AuthorityRegistry` 212+; `Pre553RuntimeAuthoritySet` 260+; `authorize_i03_operation_successor` 926+ | Exact existing authority resolution and operation fitness, including successor permissions where warranted. Not a source-science issuer, no arbitrary original measurement admission. |
| `pre553_discovery_exact.py` · `905f24d114419dbdd93879ad2bee5b59dd2f23af` | `_verify_discovery_authority` 289–346; `_catalog_atoms` 348–376; `_catalog_templates` 425–448; `_compile_frontier` 617–813; `execute_exact_bounded_discovery` 1050–1236 | **ACTUAL GENERATOR** of deterministically finite authorized combinatorial frontier: AND, Cartesian, XOR, base query, JOINT_DEPENDENCE and REVERSAL_GRID, from **already declared** atoms/templates and authority; enumerates BEFORE first empirical result, rejects pruning. Its exhaustive claim is restricted to that finite declared grammar. |
| `pre553_discovery_adaptive.py` · `58e32770381fa8d901701d6a2c676f28261aa3e3` | `AdaptiveExplorationUnit` 110–162; `_verify_adaptive_authority` 437–530; `execute_adaptive_exploration` 569–696 | Deterministic scoped **exploratory** schedule with caller supplied roots and callback, bounded result-dependent proposals BETWEEN sealed visits. Retains `UNKNOWN_UNVISITED`, partial/budget status; exhaustive only for reachable policy frontier, not original-source inventory. |
| `pre553_batch_runner.py` · `2d291600b9a10c56d9c6f6de7f7d619f6c52e829` | `BatchUnitSpec` 100–153, `BatchManifest` 155–212, `BatchExecutionRunner` 385–690 | Immutable/content-addressed units and deterministic replay/attempt/result receipt scheduling. **Caller builds BatchUnitSpec list**; canonicalizing it is not constructing source-original items. No observed producer joins C11 releases with all I03/I05 operation refs to close35 manifest. |
| `pre553_recursive_handoff.py` · `868f43bf9869af5501fd67c3de7a2703ba4cb1b4` | `execute_exact_bounded_discovery_with_handoffs` 516–560 | Forwards caller discovery/atom/template catalog into I05; constructs supported recursive branch handoffs with exact ancestry. No all-source item universe expansion. |
| `pre553_source_equivalence.py` · `0e7f9f6d77ef6efe2c66b04f0527bb1ab99f4ef8` | `certify_source_to_c11` 712+ | Certifies bounded source↔C11 dimensions and declared evidence; no proof independent original item/operation roster is exhaustive. |
| `pre553_source_relations.py` · `5b67e3f98a5faf95a6c82700af2346fef6e306a5` | `guard_sample_pooling` 751; `guard_estimand_composition` 794; `guard_i03_authorized_composite_query` 921 | Guards source/estimand composition, not authority-free population/temporal admission. |
| `pre553_authority_maintenance.py` · `547e6bf20354f38179a0e2600de64c7cb2260ea0` | Authority lifecycle | Currentness/revocation/identity controls, not source/question/operation candidate generator. |
| `pre553_runtime_composition.py` · `3753c183ddb25b1b0eb0ce84db1868f39f50d3fa`; `pre553_runtime_context.py` · `4fc50793871e176f164442c04ef2501eba9d5dfa` | `compose_predicates_runtime` 21; `bind_runtime` 33 and wrapper invocations 73–119 | Recombine authorized predicate grammar or bind runtime context; do not manufacture original item source evidence. |
| `pre553_analytical_composition.py` · `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`; `pre553_learned_world_composition.py` · `4a8e27a226a9c06606f5ba493d2cc7356d491a7b` | `compose_positioned_subject_possibility` 1008–1205; `build_m1_bundle_from_m01` 750 | **Implemented downstream actual compositors**, which use a selected qualified empirical query/discovery result or M01 output; not upstream original-item factories. |
| `pre553_analytical_state_and_route.py` · `3a5e3db8a0897900d0b2606813bda7c3f586d46e` | `capture_required_authority_refusal` 1146–1205 | **Real I05 caller**, but passes caller predicates and templates only to create an exact refusal witness, not questionnaire completeness. |
| `pre553_service_source_applicability.py` · `3e40caca29e8c96ee1f412f919cfc7dba63f96c4` | `resolve_service_source_applicability` 684; `assert_complete_coverage` 662 | Checks already-declared service candidate classes, not original measurement option coverage. |

## C. Viable per-source constructing witnesses and why they cannot stand in for the general machine

- `wave1_r5_q86_c11_projection.py` (blob `d96933180d310b4078f23127bb5a97a3677728d1`): `_build` 437–531 creates a real `GovernedC11Projection` 505; `build_r5_q86_c11_projection` 532 and validated release 538. **Selected R5 Q86 source-bound witness**, not a generator enumerating every original questionnaire item/operation of that wave, let alone 35.
- `wave2_r5_q69b_conditioner_projection.py` (blob `751de0dc54dacfeceb08115fe7cda71b75bce110`): builds selected Q69B conditioned C11 with retained transport, not general original-item scope.
- `gt34_q2_q69b_q86a_same_source_materialization.py` (blob `afdf38a7effe72fa1f4af22d545dcfb3b28aa03d`): `build_q69b_q86a_same_source_candidate` 553; selected same-source construction, no universal source roster.
- `fiabc_final_oracle_freeze_producers.py` (blob `9b67df148528fbc35813cac473c27a28485d1f91`) rehydrates selected historical LiTS/WVS comparator/source oracle closure, not claimed as a current generic questionnaire-to-all-operations issuer.
- `fiabc_whole_source_physical_equivalence.py` (blob `acdbc3f99f38d228d20d6a27ab7e89558af354af`) builds physical equivalence expectations; source bytes/column parity does not carry original question meaning or operation grants.
- `data/ddm_registries/materialize_governed_association_registries.py` (blob `fe8e799ae65a08834225c6f95f5edddae3f0dfc5`) materializes bounded governed legacy association registries from supplied source files, not an observed current Route B/BatchManifest original-item-wide caller.

These qualify as **real construction at selected already-governed scopes** or custody operations, not a missing architecture theorem. WG0-L independently handles old V550/J automatic succession; do not treat older registry as permission to reactivate a historical pipeline.

## D. Checked tests and actual proof grade

All test conclusions here are from **reading their checked-in assertions**, not running tests. The test files supply executable fixture-positive and hostile scenarios; none below independently proves all original native items across CLOSED35 were enumerated, admitted, and actually executed in production.

| Test file / blob | What the checked code tests | What it cannot establish |
| --- | --- | --- |
| `test_pre553_route_b_production.py` · `d244eaaa48f878f83d77a305b54e6dcde37244c5` | `_fixture` 73 builds projection 376, catalog 501, requests 508–509; `test_direct_composition_parity_and_complete_object_graph` 548; source mismatch/authority, raw vs weight, replay, typed absences | “Complete object graph” for that **provided** fixture ≠ all native measured columns. |
| `test_pre553_discovery_exact.py` · `b53039aeb95e012993c5233a7575c1dad5a14929` | helper `_atom`, `_qt`, `_grammar`, `_discovery_authority` 33–115 manually define frontend. Tests XOR without unary signal 196, reversal 235, minority 268, recursive 293, joint 322, Cartesian 350, higher-order 380, frozen frontier 483 | Sufficient **algorithm** for supplied frontier; no original native-wide input oracle. |
| `test_pre553_discovery_adaptive.py` · `fb7d00ad0ee2690dede339dd029476b64158824b` | explicit `_unit` 92; partial/unvisited 117, result-driven proposals 142, checkpoint/restart 184 | Partial explored ≠ complete original item/operation coverage. |
| `test_pre553_batch_runner.py` · `d22a1196008233e12f9b04918d417b32e0f53576` | explicit `_unit` 41 and manifest 82/114; deterministic schedule, deferral, resume, no throttle=>fake-complete 208 | No independent workload *construction* from governed source register. |
| `test_pre553_empirical_query.py` · `cc7d93db1f87d9c311170c229dbe3506937b404a` | synthetic `_build_source` 78; true joint, XOR, risk, route/weight, absence/observed zero, operation/family/target use refusal | Correct selected operation, not source-wide original questionnaire inventory or representative estimator warrant. |
| `test_pre553_query_frontier_hostile.py` · `d18f1411e9a3c6f6126e38dd0e3ea2fb4694691e`; fixtures `pre553_query_frontier_fixtures.py` · `597b0189029d98535ecd3ee16d738cf43124d98e` | adversarial source-free respondent/joint/topology/typed absence cases | No complete release×item×operation real execution oracle. |
| `test_pre553_source_backed_c11_facade.py` · `daf9368a0c3ff277da0b46c4f27e4686c1de8b12`; multi-owner · `d3fe1620e1d04694665f25c7dfcd67d375ce168a` | explicit projection, missing slots/semantic values and multi-ownership authority; WVS7 shape representable | A bounded authorized physical→C11 projection can omit other columns without contradicting its declared contract. |
| `test_pre553_source_local_universe_admission.py` · `b2561ba230e956b56c509efc1779b94efef92aa1` | explicit RAW/source-local authority vs forbidden national generalization | Population/design source authority is separately needed for broader estimands. |
| `test_pre553_recursive_handoff.py` · `c199acb1a99f26d4e789035dffba55f79bc3a0a0`; `test_pre553_analytical_composition_higher_order.py` · `c8a83d3deffa6f0a10309e15143d7dcc953a8abe` | positive depth-two handoffs, higher-order conditional and actual composed consumer on specified inputs | Doesn't establish all35 selection/permission/consumer occupancy. |
| `test_pre553_whole_machine_hostile_acceptance.py` · `197b317ae2840b687b7645d783d78d673d54614f` | R15 H10 I04/structural attack matrix (functions 29–219) | Its filename is **not** proof of estate-wide item/operation closure. |

## E. Authority, frozen-frontier and absence distinctions

* **I05 exact:** `_verify_discovery_authority` checks exact positive frontier issuer, content-hashed candidate grammar and `NONE_EXACT_EVALUATE_ALL`. `_compile_frontier` runs before empirical evaluation, so **empirical outcomes cannot remove declared candidates**. It cannot detect legitimate original question forms never declared in `definition["atoms"]` or templates.
* **I05 adaptive:** authority freezes **policy, roots, rules, limits** before execution; proposals between sealed visits *are allowed to depend on observed outcomes*, so it is NOT proof of a fixed, source-exhaustive universe. `UNKNOWN_UNVISITED` and `PARTIAL_BUDGET_EXHAUSTED` remain typed; partial result must not be reported as global observed null or global no-pattern result.
* **C11:** a projected absent/unbound cell is not automatically a respondent's nonresponse or questionnaire-intrinsic inapplicability. `project_c11_candidate_from_physical_cells` fails on unbound values within declared slots but silently does not project slots outside declared projection. Therefore an **external original-item membership/accounting witness** is required to prove which exclusions were competent.
* **I03:** exact `PREDICATE_GRAMMAR` operation/source/target use fitness and query/risk/measure identity; typed nonpositive query result is distinct from missing operation permission.
* **Batch:** a completed batch receipt proves completion over `BatchManifest.units` only. The manifest constructor never checks that all scientifically authorized source/question operations were included.
* **Epistemic bookkeeping required but NOT established by these public constructors:** unsupported vs prohibited vs unresolved vs source-inapplicable vs unvisited vs observed cell-null/zero are not a single boolean; complete estate reconciliation must be a **separate no-drop claim** backed by original instrument/issuer oracle, frozen pre-result.

## F. Exact search boundary; limitations that prevent a global absence theorem

1. Enumerated the exact control-ref `rawlsing_next/` **144 entries**; `rawlsing_next/tests/` **187 entries**; `data/ddm_build_copy/` **189 entries**, `data/ddm_registries/` 3 entries, plus `tests/`. Read the specific current upstream/downstream modules and test assertions above, source-local, physical, runtime, authority, source-equivalence, analytics, scoped named producers and selected retained FIABC current implementations.
2. Retrieved and contrasted governing HQ278+HQ277 source law and Astra implementation map, exact file/blob identities. Revisited source-native/physical and admitted limited source/canary constructors; separated later consumer from upstream factory.
3. GitHub code search queries `execute_route_b_production`, `i03_requests`, `GovernedC11Projection`, `BatchManifest`, `pre553_discovery_exact` were attempted, but search response indexes repository **default branch main** (`25830fe...`), *NOT* frozen PRE-MAIN (`288316...`). They are NOT negative evidence for current branch. No entire recursive Git tree content-index census or execution of the 35 retained source issuers was performed.
4. Did NOT exhaust all 144 current modules, all 187 tests, historical nested archives, privately retained dataset metadata, or active separate WG0-L succession. The narrower justified result is: **every inspected generic input consumer and likely directly adjacent factory stops at caller-supplied source/authority/operation objects; no proved all35 join appeared in this bounded current-owner slice**.
5. Absence of a full original-item issuer, national respondent eligibility, design/calibration permission for any **particular** original item has NOT been universally proved. Do not promote search silence to `SOURCE_PERMISSION_PACKET_MISSING` for all35. Independently verify a source's competence before any scoped real-data grant.

**Finding:** `BOUNDED_MISSING_CONNECTION` at the documented source-qualified original-item/operation inventory → prepared C11/I03/I05/batch contracts; `EXISTING_CURRENT_OWNER_ALREADY_SUFFICES_AT_EXACT_PROVED_GRAIN` for described bounded C11, I03, exact I05, adaptive, batch, analytic local transformations; `UNVERIFIED_NEEDS_EXACT_FOLLOWUP` for possible further current factory and full original-item/operation coverage, and all35 real execution. No exact architecture warrant established. No production edits or raw operations.
