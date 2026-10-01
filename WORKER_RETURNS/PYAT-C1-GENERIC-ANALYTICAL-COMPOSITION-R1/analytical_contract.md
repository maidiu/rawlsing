# C1-00 analytical-composition contract freeze — R1 + R2 + R3 + R4 corrections

Status: `C1_02_R1_AT08_AT13_EXECUTED__GENERIC_PACKET_SYNCHRONIZED__INDEPENDENT_REVIEW_REQUIRED`

Previous status: `C1_00_R4_EXACT_SELECTION_KEY_SYNCHRONIZATION_READY_FOR_INDEPENDENT_REREVIEW`

This is a **documentary contract/oracle freeze only**. It does not self-approve C1-00, execute C1-01, edit production code, create survey/model/comparability authority, or claim real-source proof.

## 1. Bound identities and authority

- issued commission tip: `2cef3869c16cbd88ce8bc58a5bd4aa073879be50`
- commission blob: `cf161512c618acb71ee6f7e2882a0ad6dbb64b3c`
- commission parent / implementation baseline: `b3b2fa13049513078c301a1f6574b661fcf390c5`
- orchestration authority: `810dbfde9fa5dbe1e3625188f4c13c4c9e7ceeb7`
- C1 execution spec blob: `f6f0e6624f87c631e3c65b9242cc2c2e7203a61b`
- command charter blob: `50a48745dfd9a156268ddce1b3fdcd04899dc731`
- review/integration blob: `ed54e675a073c0e462581c0918f35ac2776d26af`
- frozen C1 binding blob: `dba11969e4e0edc4d3dac82968b418391b3d6a12`

Current producer/consumer owner blobs at the implementation baseline:

| owner | blob |
|---|---|
| `rawlsing_next/pre553_empirical_query.py` | `03facecf70890bfd13b80418620d274cbcd69d02` |
| `rawlsing_next/_pre553_query_common.py` | `938a6b03a63dd34ef4f0f63655ed8f11f65c5d92` |
| `rawlsing_next/_pre553_query_eval.py` | `f808dfcd2008cc71e9203de3cadf1abe14223974` |
| `rawlsing_next/pre553_empirical_objects.py` | `a61365b994e5c3c50de0f598fcf40e90abf757b6` |
| `rawlsing_next/pre553_discovery_exact.py` | `905f24d114419dbdd93879ad2bee5b59dd2f23af` |
| `rawlsing_next/pre553_discovery_adaptive.py` | `58e32770381fa8d901701d6a2c676f28261aa3e3` |
| `rawlsing_next/pre553_recursive_handoff.py` | `868f43bf9869af5501fd67c3de7a2703ba4cb1b4` |
| `rawlsing_next/source_backed_positioned_subject_possibility.py` | `62e5eced47b64512f47b004e3e13a6ef3fe21de7` |
| `rawlsing_next/pre553_learned_product_lifecycle.py` | `a11c9eb73abab9be118ef4f0b6e325e676059f27` |
| denominator-context receipt `WORKER_RETURNS/PYAT-HQ120-J3-DENOMINATOR-CONTEXT-CONSERVATION-R1/05_EXACT_DEREFERENCE_RECEIPT.md` | `acdab4f80aa6ac948eeaca6bbd8ecfc079b34bc6` |

Relevant source-free test-owner blobs inspected:

- `test_pre553_empirical_query.py`: `cc7d93db1f87d9c311170c229dbe3506937b404a`
- `test_pre553_discovery_exact.py`: `b53039aeb95e012993c5233a7575c1dad5a14929`
- `test_pre553_recursive_handoff.py`: `c199acb1a99f26d4e789035dffba55f79bc3a0a0`
- `test_source_backed_positioned_subject_possibility.py`: `c48342fc5b9d7ae6701b5399c656d3c300cc407a`
- `test_pre553_discovery_adaptive.py`: `fb7d00ad0ee2690dede339dd029476b64158824b`

No raw survey source was opened or materialized. Source reads: **0**.

## 2. Exact current public call trace

### Direct empirical route — C1-01 implementation target

1. Caller holds exact `C11Repository`, `EmpiricalQuerySpec`, `EmpiricalPredicate`, `AuthorityRegistry`, and exact `C11LogicalRelease` refs.
2. C1 adapter invokes, not emulates:
   `pre553_empirical_query.execute_empirical_query(repository=..., query=..., predicate=..., authority_registry=..., release_refs=...)`.
3. I03 validates exact query/predicate identities and exact condition-predicate equality; resolves exact releases; parses source scope, risk, measure and target plan; evaluates the risk/condition/target; returns `QueryExecutionResult`.
4. Canonical truth is the returned `EmpiricalFact` preimage(s), not an adapter scalar. The fact carries exact query ref, universe refs, target topology/domain identity and complete cells, condition predicate ref, risk ref/member refs, denominator member refs, raw/weighted support, measure-basis ref, response-state semantics, uncertainty, provenance, replay and authority/dependency refs.
5. C1 constructs a `PossibilitySliceEvidence` **from that fact**, never from handwritten final percentages.
6. Before the consumer call C1 validates the full binding witness described below, source/release, target, denominator/risk, measure, support and state identities.
7. C1 invokes, not emulates:
   `source_backed_positioned_subject_possibility.evaluate_positioned_subject_possibility(query=..., rule=..., evidence=...)`.
8. C1 returns an analytical envelope retaining the original producer state/context plus the actual `PositionedSubjectPossibilityResult`.

### Exact discovery route — later C1-02/C1-03 use

`execute_exact_bounded_discovery` compiles the exact governed frontier and calls `execute_empirical_query` for each candidate query role. `ExactBoundedDiscoveryResult` closes over exact receipts, empirical-fact preimages, executed predicate/query preimages, frontier identity, complete declared-frontier coverage and replay. A C1 adapter may consume only an exact receipt/fact/query/predicate closure; it may not reconstruct a result from a discovery label or score.

### Recursive route — later C1-02/C1-03 use

`execute_exact_bounded_discovery_with_handoffs` delegates to exact discovery and emits positive recursive handoffs only for supported recursive families. `RecursiveBranchHandoff` preserves parent, winning predicate, release set, source/risk/topology/measure scope, coverage/pruning and deterministic parameters. Full negative/coverage truth remains in the attached `ExactBoundedDiscoveryResult`; positive handoffs alone are never treated as complete search evidence. Persist/load plus `replay_recursive_branch_membership` is the required fresh-process ancestry path.

### Adaptive route — coverage side-channel only unless its sealed unit supplies a competent empirical result

`execute_adaptive_exploration` returns `AdaptiveSearchResult` with explicit visited and unvisited unit refs and completeness states. Its own contract forbids global negative claims. C1 must retain `PARTIAL_BUDGET_EXHAUSTED`, `PARTIAL_INTERRUPTED`, or `EXPLORATORY_POLICY_FRONTIER_EXHAUSTED` exactly; unvisited territory is `EXPLICIT_UNKNOWN_UNVISITED`, not a negative empirical fact.

## 3. Proposed C1 public contract for C1-01

Production names below are **proposed**, not implemented in C1-00.

`compose_positioned_subject_possibility(*, repository, empirical_query, predicate, authority_registry, release_refs, consumer_query, model_rule, condition_binding_witness) -> AnalyticalCompositionResult`

Exact inputs:

- `repository: C11Repository`
- `empirical_query: EmpiricalQuerySpec`
- `predicate: EmpiricalPredicate`
- `authority_registry: AuthorityRegistry`
- `release_refs: Iterable[ExactRef]`
- `consumer_query: PositionedSubjectPossibilityQuery`
- `model_rule: PositionedSubjectPossibilityModelRule`
- `condition_binding_witness: ConditionValueBindingWitness` (new C1 custody object, not semantic authority)

C1-01 direct-slice admissibility is deliberately narrow: one exact consumer source universe; one exact consumer release; one target component whose exact target ref equals `consumer_query.target_ref`; actual I03 output; no supplied/preconstructed `PossibilitySliceEvidence`; exact condition witness; exact measure/risk/denominator context retained; no source/release/measure bridging; no inferred subject-to-survey semantics.

Unsupported shapes are typed C1 residual states, not silently widened. C1-02 may add reviewed routes without weakening this contract.

### ConditionValueBindingWitness

This object proves **custody/identity**, not new comparability meaning. Its canonical material must include:

- `consumer_query_ref`;
- canonical full material of every retained `ConditionerBinding`, not only `binding_id`;
- `consumer_binding_fingerprint` = semantic hash of the ordered full binding material;
- `producer_query_ref`;
- `producer_predicate_ref`;
- `producer_predicate_hash`;
- a canonical projection of the exact predicate AST used for the conditioned denominator;
- exact source-universe and release refs;
- the existing `comparability_authority_ref` from each consumer binding;
- `binding_mode = EXPLICIT_EXACT_PAIRING_NO_INFERENCE`.

The adapter recomputes all identity-bearing fields from actual supplied objects. A witness that merely repeats a label is invalid. The witness never declares that a real subject value is survey-comparable on its own; that semantic premise must already be carried by the consumer binding/competent authority. In the C1 source-free court the witness is backed only by explicit synthetic test authority.

### Output

`AnalyticalCompositionResult` must retain:

- `analytical_state`;
- actual `QueryExecutionResult.query_ref`;
- exact selected `EmpiricalFact.ref` and complete producer fact state;
- source universe ref(s) and release ref(s);
- full condition identity: producer predicate ref/hash plus full consumer binding fingerprint;
- exact ordered target refs, arity, component topology, domains, target-domain replay refs, component authority refs, response-semantic refs and producer `target_domain_identity`;
- risk-set ref, risk-set member refs, denominator member refs and exact raw denominator;
- measure kind, measure-basis ref, optional weight-basis id, and—when weighted—the exact used `WeightMeasureFact` refs with weight-source, design-authority, estimand-authority, normalization/recalibration and effective-scope refs dereferenced through `C11Repository.resolve_object_exact`;
- exact complete-cell geometry with raw counts and authorized exact fractions; no float rounding as identity;
- uncertainty/support state;
- producer authority refs, provenance refs, dependency refs and replay refs;
- route coverage state and ancestry refs when discovery/recursive/adaptive routes are used;
- the constructed `PossibilitySliceEvidence`;
- actual `PositionedSubjectPossibilityResult` when a consumer call is lawful;
- consumer query ref and model-rule hash;
- composition determinant refs sufficient for fresh recomputation.

The result envelope is analytical/custodial only. It does not become an admitted structural truth, actor fact, belief, prediction or normative recommendation.

## 4. Conditioner-ID alias: required repair at the C1 adapter boundary

Static inspection proves this collision:

- `PositionedSubjectPossibilityQuery.ref` hashes full `ConditionerBinding.material()`.
- `PositionedSubjectPossibilityQuery.conditioner_ids` retains only sorted `binding_id` strings.
- `PossibilitySliceEvidence` stores only `retained_conditioner_ids`.
- consumer `_find` selects evidence by source universe, release, target and those IDs.

Therefore two consumer queries may have identical conditioner IDs while differing in subject fact, empirical coordinate/value binding, comparability authority or effective time. Their query refs differ, but a pooled evidence set keyed only by the IDs can alias.

C1-01 must **not** modify or broaden the consumer public API. The new adapter must instead:

1. derive a full binding fingerprint from `consumer_query.conditioner_bindings`;
2. bind that fingerprint to exact producer query + predicate in `ConditionValueBindingWitness`;
3. derive the slice only from the just-executed producer fact;
4. attach the strong condition identity to the outer analytical envelope;
5. pass to the consumer only evidence whose strong identity was validated for that exact `consumer_query.ref`;
6. reject cross-query evidence reuse before `evaluate_positioned_subject_possibility`.

Hostile court: two consumer queries use the same `binding_id="position"`, same source/release/target, but distinct value-specific subject-fact refs (`P1` versus `P2`). Reusing the P1-derived slice for the P2 query must fail with a typed C1 condition-identity error before the consumer call.

This is sufficient at the C1 composed-call boundary and does not claim that direct calls to the older consumer are collision-proof.

## 5. Source, target, denominator and measure identity

### Source

Equality requires exact universe ref(s) **and** exact C11 release ref(s). Display-equivalent values from another release are not substitutable. No latest/default/fuzzy selection is allowed.

### Target

For C1-01 scalar composition, the producer query must have arity 1 and `target_refs[0] == consumer_query.target_ref`. C1 still retains the full producer component topology/domain/replay/authority material and fact `target_domain_identity`. Same target ref with different topology/domain material is a different producer query and cannot reuse a slice.

C1-02 may define a composite target identity for non-scalar consumer use only after independent review. C1-00 does not silently scalarize a joint, ranked, multiselect, repeated, routed or componentized target.

### Denominator / risk / eligibility / support

Identity includes all of:

- `risk_set_ref`;
- `risk_set_type`;
- exact `risk_set_member_refs`;
- exact `denominator_member_refs`;
- `raw_denominator_support`;
- exact routing/applicability semantics through producer provenance;
- target resolved support;
- complete cell states.

Equal denominator counts with different exact member sets are different analytical slices.

Observed zero is a supported-risk-set cell state, not zero support: `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` requires positive denominator and cell numerator 0. `ZERO_SUPPORT` / `ZERO_OVERLAP` have no conditioned support and remain distinct from `VALID_EMPTY`.

### Measure / weight / design / estimand

Identity includes `measure_kind`, exact `measure_basis_ref`, and optional exact `weight_basis_id`. For `GOVERNED_WEIGHTED`, C1 must dereference every used `WeightMeasureFact` in the fact provenance and retain its `weight_source_ref`, `design_authority_ref`, `estimand_authority_ref`, `normalization_or_recalibration_rule_ref`, `effective_scope_ref` and exact weight representation. Raw and weighted results never alias merely because their numerical ratios happen to match.

Bidirectional conditioning may reverse condition/target only when the source release, risk-set law and measure identity are explicitly the same. The denominator itself necessarily changes with the conditioning event and is retained exactly.

## 6. State conservation law

The outer C1 envelope owns no replacement semantic vocabulary; it retains owner-native state plus a narrow routing disposition.

Required distinctions: supported positive; supported observed-zero cell; zero support; zero overlap; valid-empty target domain/frontier; underpowered discovery result; unresolved target; unavailable/missing authority/source/risk/measure; noncomparable; not applicable; adaptive unvisited/unknown; adaptive partial interrupted; adaptive partial budget exhausted; blocked by required upstream authority; integrity failure.

The narrower consumer evidence vocabulary may coexist as follows, but never replaces the outer state:

- producer `SUPPORTED` -> consumer evidence `SUPPORTED`;
- producer `VALID_EMPTY` -> `VALID_EMPTY`;
- producer `NONCOMPARABLE` or exact not-applicable scope -> `NONCOMPARABLE` only when producer semantics justify that projection;
- producer `UNAVAILABLE` -> `UNAVAILABLE`;
- producer `UNRESOLVED` -> `UNRESOLVED`;
- discovery underpowered -> `UNDERPOWERED`;
- zero-support/zero-overlap remain explicit outer states and must not be reported as observed zero or generic valid-empty;
- unvisited has **no fabricated evidence slice and no global negative claim**;
- integrity failure raises a typed integrity exception and is retained in the court receipt; it is never laundered into `UNKNOWN`, `UNRESOLVED`, zero or valid-empty.

If the consumer must be called for a negative path that its vocabulary cannot represent without falsification, C1 returns the outer typed analytical state with `consumer_result = null` and records `CONSUMER_NOT_CALLED__STATE_NOT_LOSSLESSLY_REPRESENTABLE`.

## 7. Provenance, dependency and replay closure

Direct C1 determinant closure must include at minimum: empirical query ref; predicate ref; exact release/source-universe refs; selected empirical fact ref; fact replay ref and producer replay root; risk-set ref; measure-basis ref; response-state-semantics ref; target-domain replay ref(s); every fact authority snapshot ref; every fact source provenance ref; full consumer query ref; full conditioner-binding fingerprint; every consumer comparability authority ref; model and walkback authority refs; model-rule hash; any selected proxy evidence and proxy authority refs; and route-specific discovery/frontier/receipt/handoff/checkpoint refs when present.

Replay grades remain separate:

1. `CONSUMER_BOUNDED_REPLAY`: `verify_positioned_subject_possibility_replay`; proves only the consumer over retained inputs.
2. `I03_EXACT_REPLAY`: `replay_empirical_query`; recomputes exact producer fact refs.
3. `DISCOVERY_EXACT_FRONTIER_REPLAY`: exact discovery identities and coverage.
4. `RECURSIVE_HANDOFF_REPLAY`: persisted handoff load plus membership replay and next generation.
5. `ADAPTIVE_RUN_REPLAY`: `verify_adaptive_replay`; preserves visited/unvisited/search policy identity.
6. `FULL_COMPOSITION_FRESH_PROCESS_RECOMPUTE`: starts from retained determinants, reruns the claimed producer route, reconstructs the C1 slice, calls the actual consumer and compares final composed identity.

C1-01 must not report grade 6 merely because grade 1 succeeds.

The current B5 `LearnedProductDeterminantGraph` can express exact determinant and downstream dependency invalidation for lifecycle-governed learned releases. C1 does not impose B5 on a competent direct empirical route. AT19 uses B5 only for families that actually require that owner.

## 8. Frozen AT07 oracle

Synthetic contingency table, 100 respondents, one source universe/release/risk law, RAW measure:

| position | yes | no | row total |
|---|---:|---:|---:|
| P1 | 54 | 6 | 60 |
| P2 | 8 | 32 | 40 |
| column total | 62 | 38 | 100 |

Independent expectations:

- `P(yes | P1) = 54/60 = 9/10`
- `P(no | P1) = 6/60 = 1/10`
- `P(P1 | yes) = 54/62 = 27/31`
- `P(P2 | yes) = 8/62 = 4/31`

Forward and reverse use the same source release, risk-set law and RAW measure. They do **not** share a denominator: the conditioned member set changes from 60 P1 members to 62 yes members. Those member sets are part of identity.

The oracle was fixed from this table before any C1 candidate implementation or output exists.

## 9. Proposed C1-01 execution court

No runtime was executed in C1-00. Runtime identity remains `NOT_YET_FROZEN__NO_EXECUTION_REQUIRED_FOR_DOCUMENTARY_CONTRACT_FREEZE`.

After independent acceptance, HQ may freeze a competent source-free PR-triggered governed bounded court.

Primary command:
`python -m pytest rawlsing_next/tests/test_pre553_analytical_composition.py -q`

Targeted owner regressions:
- `test_pre553_empirical_query.py::test_observed_zero_is_not_zero_support`
- `test_pre553_empirical_query.py::test_raw_and_authorized_weighted_measure_are_distinct_exact_facts`
- `test_source_backed_positioned_subject_possibility.py::test_exact_supported_positioned_subject`
- `test_source_backed_positioned_subject_possibility.py::test_valid_empty_remains_exact_typed_state_and_is_not_broadened`

Mandatory C1-01 assertions:

1. the exact AT07 table yields 54/60 forward and 54/62 reverse from actual I03 fact cells;
2. slice evidence ref/provenance is derived from actual producer output;
3. the actual consumer returns an exact-supported result for the supported path;
4. same conditioner ID + different value-specific binding cannot reuse evidence;
5. observed zero differs from zero support;
6. incompatible source/release/risk/measure fails closed;
7. direct producer replay and bounded consumer replay are distinct receipts;
8. no test imports production implementation from test code.

Full fresh-process recomputation is required before claiming the grade promised by the C1 spec; if the court cannot provide it in C1-01, the return must state the lower replay grade rather than overclaim.

## 10. Minimal future write allowlist for C1-01

Only:

1. `rawlsing_next/pre553_analytical_composition.py` — new;
2. `rawlsing_next/tests/test_pre553_analytical_composition.py` — new;
3. `WORKER_RETURNS/PYAT-C1-GENERIC-ANALYTICAL-COMPOSITION-R1/**` — receipts/return updates.

No existing producer or consumer owner file is authorized for C1-01 by this packet. If independent review demonstrates that the adapter boundary cannot enforce the frozen identity law, HQ must issue a separate bounded owner-repair scope amendment naming the exact owner blob and failure. This worker does not pre-authorize such a repair.

## 11. Unresolved questions / explicit limits

1. **Real-source subject↔survey value alignment owner:** C1 can preserve and verify exact refs it is given, but C1-00 does not create a real-world comparability authority. Source-free fixtures use explicit test-only binding material. Real-source execution must name an already competent owner/authority for the subject fact ↔ empirical condition/value relation.
2. **Multi-target positioned consumer identity:** the current consumer has one `target_ref`; C1-00 therefore freezes scalar direct C1-01 only. C1-02 must independently review any composite-target identity before consuming joint/ranked/multiselect shapes. No scalarization is permitted.
3. **Multi-universe/composite release consumption:** the current consumer query binds one source universe and one release. C1-01 does not bridge `SOURCE_INDEXED_MULTI_UNIVERSE` or `AUTHORIZED_COMPOSITE` facts into one consumer slice without an exact reviewed source identity rule.
4. **Negative consumer-call coverage:** some producer/search states cannot be truthfully represented in `PossibilitySliceEvidence`. The outer C1 result preserves them and may lawfully omit a consumer call rather than fabricate `UNKNOWN` or `VALID_EMPTY`.
5. **Lifecycle universality is rejected:** B5/M1/M2/I4 are conditional family owners, not mandatory wrappers for competent direct empirical composition.

None of these prevents the narrow source-free AT07 C1-01 vertical slice defined above.

## 12. Required independent-review attacks

The reviewer should derive counterexamples before reading any future success narrative, especially:

- same conditioner ID / different binding value or time;
- contaminated evidence pool with same retained IDs;
- same denominator count / different member refs;
- same target ref / changed topology or domain;
- same visible values / different release;
- RAW versus weighted with numerically equal ratios;
- zero-support versus observed-zero versus valid-empty;
- unvisited adaptive work misreported as negative;
- lookalike recursive child with different parent ancestry;
- replay that proves only the consumer but is reported as full recomputation.

This packet is ready for independent review only. It is **not** an approval and does not authorize C1-01 by itself.


## R2 authoritative correction addendum

This addendum is part of the corrected C1-00 contract. Where it is more specific than the R1 text above, **R2 controls**. It corrects exactly the five defects returned by independent review at `8baa2e1e3a6f4f96311fbd660b65933fb4aff6c4`; all previously reviewed PASS holdings remain unchanged.

Exact correction packet:

- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/01_CORRECTION_MATRIX.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/05_STATE_AND_DETERMINANT_CLOSURE.json`

### R2-A — condition/value identity is a value-bearing relation, not co-custody

The R1 `ConditionValueBindingWitness` definition is superseded by `C1_CONDITION_VALUE_BINDING_WITNESS_SCHEMA@2`, schema hash:

`0a881f32dee7142979d76ebf4f3462df16d8a6bad55a23b2e8fc22834ed04f36`.

For every retained conditioner, the witness must include and bind:

- exact full `ConditionerBinding.material()`;
- full consumer-binding fingerprint and `consumer_query.ref`;
- exact source-free subject-condition preimage ref **and material**;
- exact producer query and predicate refs/hash;
- exact normalized value-bearing producer predicate-leaf ref/projection;
- exact fixture-only pairing-ground-truth ref;
- exact pairing/comparability `AuthorityRef`;
- exact source universe, release and effective time;
- `binding_mode = EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE`.

The adapter must deterministically verify, before any `PossibilitySliceEvidence` construction:

1. `ConditionerBinding.subject_fact_ref == subject_condition_preimage_ref`;
2. `ConditionerBinding.empirical_coordinate_ref == subject_preimage.empirical_semantic_ref`;
3. the binding's pairing/comparability authority equals the exact frozen fixture AuthorityRef;
4. binding and witness source/release/effective-time material match exactly;
5. the actual producer predicate contains the exact normalized leaf whose projection hashes to the frozen leaf ref;
6. subject preimage semantic ref equals predicate-leaf semantic ref;
7. subject preimage exact value equals predicate-leaf exact value;
8. the exact frozen pairing-ground-truth ref names **that specific subject-preimage / predicate-leaf pair**.

Failure of any check is `CONDITION_VALUE_RELATION_MISMATCH`, before slice construction and before the consumer call.

The mandatory hostile is now exact: same `binding_id="position"`, same source/release/target, frozen subject preimage `POSITION=P1`, but producer leaf `POSITION==P2` => reject. The adapter may not turn this wrong relation into a stable identity merely by hashing both sides.

The frozen value preimages, leaf preimages and pairings are in `02_VALUE_RELATION_ORACLE.json`. They are fixture/oracle material only and create **no real-source comparability law**. Real-source subject↔survey pairing remains blocked unless an existing competent owner supplies the relation.

### R2-B — complete synthetic authority preimages are frozen

The R1 tag-only authority freeze is superseded by `03_SYNTHETIC_AUTHORITY_FREEZE.json`.

For every synthetic authority needed by C1-01, the packet now freezes:

- complete canonical authority preimage/material;
- class/purpose;
- governed operation(s);
- exact scope;
- version and effective interval;
- governed object families where the existing PRE553 `AuthoritySnapshot` owner applies;
- replay/semantic material where applicable;
- exact expected `AuthorityRef` content hash.

Hash law:

`authority_content_hash = sha256(canonical_json(complete_frozen_authority_preimage))`.

Therefore a changed scope, operation, model rule, pairing set, effective interval or other frozen authority material under the same human-readable label **must** change identity. Reusing an old hash is an oracle failure.

Five entries use existing PRE553 authority kinds for the synthetic I03 fixture. Three `FIXTURE_ONLY_*` entries exist only to satisfy existing consumer `AuthorityRef` inputs at the source-free court; they are **not new production authority kinds** and have zero real-source effect.

### R2-C — UNKNOWN is distinct from UNVISITED and UNRESOLVED

The R1 phrase “adaptive unvisited/unknown” was too coarse. R2 freezes separate owner-native states:

- `UNKNOWN_CURRENTNESS` — existing B5 lifecycle selection owner;
- `NO_CURRENT` — existing explicit B5 no-current receipt;
- `CONFLICTING_CURRENT_SELECTION` — existing B5 conflict;
- `EXPLICIT_UNKNOWN_UNVISITED` — adaptive search territory not visited;
- `UNRESOLVED` — empirical/query/consumer unresolved path;
- `UNAVAILABLE` — missing exact source/authority/risk/measure path.

None may be substituted for another. The explicit UNKNOWN witness is the existing B5 `UNKNOWN_CURRENTNESS` path in baseline blob `a11c9eb73abab9be118ef4f0b6e325e676059f27`. No synonym or new owner is invented.

### R2-D — exact consumer slice projection

C1-01 has exactly one lawful supported-slice projection:

`C1_POSSIBILITY_SLICE_PROJECTION@1`

schema hash:

`c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a`.

Full schema: `04_SLICE_PROJECTION.json`.

For a supported scalar slice, `PossibilitySliceEvidence.geometry` is exactly `C1_POSSIBILITY_SLICE_GEOMETRY@1`, with frozen keys for:

- exact source fact/query/predicate/witness refs;
- exact target ref, arity, joint-order semantics, full component material and target-domain identity;
- exact risk-set ref/type, risk-set member refs and denominator member refs;
- exact raw denominator and authorized weighted denominator;
- exact measure kind/basis, optional weight basis and exact design/estimand context;
- complete producer cell material/state;
- raw numerator per cell and authorized weighted numerator;
- exact reduced-fraction cell probability.

`PossibilitySliceEvidence.raw_support` means **exactly `EmpiricalFact.raw_denominator_support`**. It never means resolved-target support or one cell numerator.

The exact evidence ref is content-addressed over the complete frozen evidence payload including the value-relation witness. Alternate geometry keys or alternate `raw_support` meanings fail the adapter contract.

For AT07:

- forward P1 slice: `raw_support=60`, yes `54/60=9/10`, no `6/60=1/10`;
- reverse yes slice: `raw_support=62`, P1 `54/62=27/31`, P2 `8/62=4/31`.

Producer states that cannot be represented losslessly in the consumer vocabulary remain in the outer envelope and may lawfully produce `consumer_result=null`; they are not fabricated as supported geometry.

### R2-E — determinant, replay and invalidation closure

The direct composition determinant set now necessarily includes, in addition to every R1 determinant:

- condition-value witness ref/hash;
- every subject-condition preimage ref;
- every producer predicate-leaf ref/projection used for conditioning;
- every pairing-ground-truth ref;
- every pairing/comparability AuthorityRef;
- exact risk-set and denominator member refs;
- measure kind as well as measure-basis ref;
- full target component/topology/domain material;
- constructed slice evidence ref;
- slice projection schema hash.

The composed result identity includes these relation determinants. Fresh-process full-composition replay must reload/reconstruct them before it can claim `FULL_COMPOSITION_FRESH_PROCESS_RECOMPUTE`.

Mandatory AT19 R2 mutation: hold producer counts, query/predicate, source/release, risk members, denominator members, measure, target and model rule fixed; mutate only the exact condition-value relation/witness determinant. The composed direct result **must reidentify**. If the family is lifecycle-governed, existing B5 determinant edges must invalidate/reidentify all and only dependent releases. Unrelated releases remain usable. C1 still does not impose B5 on competent direct empirical output.

### R2 preserved PASS holdings

R2 does not weaken or reopen the already accepted C1-00 holdings for:

- exact source universe + release identity;
- target topology/domain/component identity;
- risk/eligibility/denominator/member identity;
- RAW versus governed-weighted measure/design/estimand identity;
- recursive immediate-parent ancestry and positive-handoff/full-coverage distinction;
- replay-grade separation;
- direct versus learned/adjudicated route legitimacy;
- AT07 arithmetic `54/60` forward and `54/62` reverse;
- the narrow C1-01 future write allowlist.

C1-01 remains unimplemented and unauthorized pending independent rereview of this corrected packet.

`C1_00_R2_CORRECTIONS_READY_FOR_INDEPENDENT_REREVIEW`


## R3 authoritative correction overlay

R3 is a bounded documentary overlay on the independently rereviewed R2 packet. It changes no production owner, executes no C1-01 path, accesses no raw survey source, and creates no real-source semantic/comparability/model/pooling/survey authority. The accepted R2 A value-relation repair and E determinant/replay/invalidation repair remain unchanged.

### R3-B — owner-native source scope for the synthetic I03 query authority

The synthetic AT07 universe is now frozen **before** the source-scoped query authority:

`EmpiricalUniverse@1.0.0`
`ca5ee1320b1c0e0685eccb6585b35c1e74094516802545bde42fa11191ea43c2`

The exact source-free C11 release derived from the frozen AT07 rows/current I02 identity law is:

`C11LogicalRelease | REL-c1-at07 | dfd6ca5e08d1abe0f1494b4dc0e38869925739cceb306c62a3540922b12ff5b3`

R8 execution supersedes the historical documentary `8afa807c...d939` value as current executable truth; the historical R3 artifact remains unchanged evidence.

The R2 `C1-AT07-QUERY` material is changed in exactly one owner-native scope dimension: its `scope_envelope` now contains

`source_universe_refs = [<the exact frozen AT07 universe ref>]`.

No unrestricted wildcard and no irrelevant scope dimension is added. The corrected AuthorityRef is:

`C1-AT07-QUERY | 1.0.0 | b59ef578314515268fa7b280a8480b4c95c80c9cfd831c39c2bfc4214b6fd767`.

Current I03 at blob `03facecf70890bfd13b80418620d274cbcd69d02` supplies `source_universe_ref` to `require_positive_authority`; current authority owner blob `ca65a7fd4d52f0c44447434559b1d09412e7aa39` checks the exact `scope_envelope["source_universe_refs"]` key. The frozen R3 authority therefore contains the exact owner-native scope needed for the narrow source-free AT07 public path.

Inspection of the other C1-01 synthetic authorities finds no additional R3 scope mutation required at this grain: SOURCE/ROUTING/COORDINATE/REPLAY are consumed through owner checks that do not supply another source/target/predicate scope dimension here; COMPARABILITY/MODEL/WALKBACK are fixture-only consumer AuthorityRefs, not PRE553 AuthoritySnapshots.

Canonical material, the exact synthetic universe/release spine, and the owner-compatibility oracle are frozen in:

`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json`.

### R3-C — reachable B5 UNKNOWN_CURRENTNESS witness

The state vocabulary remains the R2 vocabulary. Only the defective witness path is superseded.

The exact current owner is:

`rawlsing_next.pre553_learned_product_lifecycle.LearnedProductLifecycleExecutor`
blob `a11c9eb73abab9be118ef4f0b6e325e676059f27`.

The R3 fixture:

1. instantiates a fresh `LearnedProductLifecycleExecutor`;
2. registers the frozen `SelectionKey` through `executor.selection_key(...)`;
3. creates neither a current-selection receipt nor a no-current receipt;
4. calls `executor.current_selection_receipt_ref(selection_key.ref)`;
5. requires exact `LearnedProductLifecycleError("UNKNOWN_CURRENTNESS")`.

The frozen SelectionKey ref is:

`B5Lifecycle:SELECTION_KEY | 53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`.

`resolve_selection_exact` with a fabricated receipt is explicitly not the witness. This remains lifecycle-currentness uncertainty, distinct from `NO_CURRENT`, `CONFLICTING_CURRENT_SELECTION`, adaptive `EXPLICIT_UNKNOWN_UNVISITED`, empirical `UNRESOLVED`, and `UNAVAILABLE`.

Exact fixture:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/03_UNKNOWN_CURRENTNESS_FIXTURE.json`.

### R3-D — noncircular PossibilitySliceEvidence identity

R2's `C1_POSSIBILITY_SLICE_GEOMETRY@1`, exact geometry keys/material, and
`PossibilitySliceEvidence.raw_support = EmpiricalFact.raw_denominator_support`
remain unchanged.

The evidence identity is now frozen over an explicit nonselfreferential preimage:

`C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1`.

The preimage contains exactly:

- schema and contract id;
- source universe ref;
- release ref;
- target ref;
- retained conditioner ids;
- evidence state;
- exact R2 geometry;
- raw support;
- uncertainty state;
- canonical provenance refs;
- canonical authority refs.

It **excludes `evidence_ref` itself**.

Construction law:

`digest = sha256(canonical_json(exact_nonselfreferential_preimage))`

`evidence_ref.kind = C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1`

`evidence_ref.object_id = urn:rawlsing:c1:positioned-subject-slice-evidence:sha256:<digest>`

`evidence_ref.content_hash = <digest>`.

Under the complete frozen source-free AT07 identity spine, expected evidence hashes are:

- forward POSITION=P1: `b2407eeb3d22cc0d71e5d13308b0149338761efc4ef40921ab363c3cd9c78307`;
- reverse ANSWER=yes: `e40c31eaf25c8e4f163ff340f968f0dc5ee650fc8383a586ea251a43ee8851d6`.

Independent documentary recomputation also freezes three hostile reidentifications from the forward baseline:

- changed exact denominator member, same visible 54/60: `f3f33cc8ae6404ea2d463641e42a9a537db577099a1edbee97929f96735ca37f`;
- changed geometry cell: `b6ee0bce50141576f9e186fb92cf1f0d038354b4f3e40509df58fb09142c57b0`;
- changed relation/pairing authority propagated through the witness/provenance/authority material: `08c73ee366f7368408459fc3df3d0e81f589b1da12cf86aa0567d2684507fa72`.

Exact preimages and hostile material:
`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/04_EVIDENCE_IDENTITY_PREIMAGE.json`.

### R3 bookkeeping and proof ceiling

The current superseding worker return lists only C1 packet files actually modified by R3. `family_binding_manifest.json` remains at its previously accepted blob and is not listed as an R3 change.

Deterministic hash/oracle recomputation is recorded in:

`WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/05_RECOMPUTATION_RECEIPT.json`.

This is `STATIC_INSPECTION + DETERMINISTIC DOCUMENTARY HASH/ORACLE FREEZE` only. C1-01 remains unimplemented and unexecuted, and remains blocked pending independent R3 rereview plus HQ adjudication.


## R4 exact UNKNOWN_CURRENTNESS SelectionKey synchronization

R4 corrects one bounded R3 documentary identity contradiction only. It does not reopen R3-B authority scope, R3-D evidence identity, accepted R2 A/E, or any production behavior.

The exact frozen R3 UNKNOWN_CURRENTNESS SelectionKey inputs are:

- `product_family_ref = UNKNOWN-CURRENTNESS-FAMILY | urn:test:c1:r3:UNKNOWN-CURRENTNESS-FAMILY | 17e74d0419dbc1ee5c6c5aed6457bf6ae39bcfa54bdcb127e429727c03f5b1a9`;
- `selection_scope_ref = UNKNOWN-CURRENTNESS-SCOPE | urn:test:c1:r3:UNKNOWN-CURRENTNESS-SCOPE | f8484aa71432f9f3db01fe855d5a67f34e61cde0ab0292072ebd556132d318f4`;
- `selection_purpose_ref = UNKNOWN-CURRENTNESS-PURPOSE | urn:test:c1:r3:UNKNOWN-CURRENTNESS-PURPOSE | ce9057a86c14a0817bd06dd65a0ce7def2efe153cbeaf90f534d4a78095d427b`;
- `consumer_context_partition_ref = null`.

Under the frozen B5 owner law:

`SelectionKey.semantic_projection() -> semantic_hash(...) -> _record_ref("SELECTION_KEY", projection)`

the exact canonical JSON hashes to:

`53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`.

Therefore the one correct fixture ref is:

`B5Lifecycle:SELECTION_KEY | urn:rawlsing:pre553:b5-lifecycle:selection_key:sha256:53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6 | 53683ac6353055af69af9f2d5cb93d889ccc5338b6aa915990c6a541ad942cb6`.

The formerly current packet hash

`a0c54c568eee1351a67ecfee43c297e82aba509daf4bce6932b5ae7331ca03cd`

is stale/wrong for the frozen R3 fixture because it does not equal the owner-native hash of the exact R3 semantic projection.

No R3-B or R3-D identity embeds this SelectionKey ref, so their accepted hashes remain unchanged.

R4 derivation and propagation audit:

- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/01_SELECTION_KEY_IDENTITY_RECOMPUTATION.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/02_PROPAGATION_AUDIT.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R4/03_UPDATED_BLOB_MANIFEST.json`

C1-01 remains unimplemented and unexecuted.


## R6 normative fixture identity completion (HQ132)

R5 established that the historical AT07 consumer-query and condition-value-witness hashes were underdetermined. HQ132 supersedes those fixture-only identities with a complete forward-computable R6 convention; historical hashes remain evidence and are not preimages to recover.

Historical R6/R7 fixture identities (preserved evidence, superseded as current execution truth):
- forward consumer query `8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`
- reverse consumer query `2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`
- forward witness `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
- reverse witness `a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`
- forward evidence `c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`
- reverse evidence `0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

R6 changed fixture identity only. Forward 54/60, reverse 54/62, producer-derived denominator support, value-bearing relation law, source/release/risk/measure/provenance semantics, noncircular evidence construction, and fail-closed ordering remain unchanged. R8 now carries the source-free execution receipt and current executable identity spine.


## C1-02 extension — AT08–AT13 source-free execution

This section is synchronized with `WORKER_RETURNS/PYAT-C1-02-HIGHER-ORDER-RECURSIVE-R1/00_RETURN.md`.

Commission: `88181e69852721f1e29c868ec5f5256095716a19`
Branch: `agent/opencode-pyat-hq139-c1-02-higher-order-recursive-r1`
Accepted C1-01 base: `5fafb499d53dddadaf8a7b4fd46506e91a09d270`

### Extended public contract

`compose_positioned_subject_possibility` accepts three additional optional C1-02 parameters without weakening the C1-01 contract:

- `consumer_binding_materials: Sequence[ConditionerBindingMaterial] | None` — full material of every retained consumer conditioner, used to derive a strong condition identity for multi-conditioner queries;
- `discovery_result: ExactBoundedDiscoveryResult | None` — lawful discovery route input; adapter consumes exact receipts/facts/queries/predicates, never score/label alone;
- `recursive_result: RecursiveHandoffDiscoveryResult | None` — lawful recursive route input; adapter consumes handoff plus attached full discovery coverage record.

At most one producer route is populated per call; an empty producer result with valid identity material is permitted for retained-bundle continuation where the consumer-facing evidence is supplied through the recursive result's replay path.

### New C1-02 routes exercised

1. **DIRECT_EMPIRICAL_MULTI_CONDITIONER** — `execute_empirical_query` with a joint consumer query whose target geometry matches the canonical first producer target ref.
2. **EXACT_DISCOVERY** — `execute_exact_bounded_discovery` consumed as exact receipt/fact/query/predicate closure; XOR/parity and ranked component-vector targets preserved.
3. **RECURSIVE_HANDOFF** — `execute_exact_bounded_discovery_with_handoffs`, `write_recursive_handoff_bundle`, `load_recursive_handoff_bundle`, `replay_recursive_branch_membership` in a fresh Python process, then depth-two continuation and consumer use.

### C1-02 identity preservation

- Exact source universe/release identity;
- Exact condition values (not only labels) in identity/provenance;
- Joint morphology and component topology;
- Exact risk/denominator/member identity;
- Exact measure and support;
- Source-native component ordering;
- Minority/counterpattern alternatives;
- Recursive ancestry and lineage;
- Discovery coverage state;
- Positive versus negative/unvisited distinction;
- Exact producer/query/fact/replay provenance;
- Consumer identity and evidence;
- Authority ceiling.

### C1-02 state additions

New typed residual states introduced in `rawlsing_next/pre553_analytical_composition.py`:

- `JointTargetMismatch` — consumer target geometry cannot be matched to producer output without scalarization;
- `RecursiveLineageMismatch` — supplied recursive handoff does not match expected parent/child lineage;
- `DiscoveryConsumptionMismatch` — discovery result lacks the exact receipt/fact closure required by the consumer query.

### C1-02 execution court

Command:
```
python -m pytest -q rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py rawlsing_next/tests/test_pre553_empirical_query.py rawlsing_next/tests/test_pre553_discovery_exact.py rawlsing_next/tests/test_pre553_recursive_handoff.py rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py
```

Result: 83 passed, 0 failed, 0 errors, 0 skipped.

### C1-02 scope limits

AT08–AT13 only. AT14–AT19 remain explicitly unimplemented. No raw survey files, no Candidate A/B/C, no measured P2X, no real-source C11 execution, no new semantic/comparability/model authority, no V3 actor/person implementation, no C4 work.

This extension preserves all accepted C1-01 behavior and identities.

Current executed R8 fixture identities are frozen in `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8/04_CURRENT_AT07_IDENTITY_SPINE.json`: forward consumer query `0e966cca...61330`, witness `fb3a3b56...84db5`, evidence `b2407eeb...78307`; reverse consumer query `02b3eabf...5f323`, witness `0c75b6ca...bf2df`, evidence `e40c31ea...851d6`. Full predicate custody and supersession classification are in the same R8 packet.


## C1-02 correction R1 — reconciled acceptance state

This section supersedes the earlier C1-02 section above, which was synchronized against a return receipt that cited test names absent from the court file.

Commission tip: `88181e69852721f1e29c868ec5f5256095716a19`
Immutable C1-02 return under review: `21254c57d92c6411282de13450fc2bdfab21d345`
Correction branch: `agent/opencode-pyat-hq139-c1-02-correction-r1`
Accepted C1-01 baseline: `5fafb499d53dddadaf8a7b4fd46506e91a09d270`

### Actual AT07–AT13 state

AT07 remains the accepted R8 source-free execution with its exact forward 54/60 and reverse 54/62 identities and unchanged evidence refs.

AT08–AT13 are now each backed by real executed courts in `rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py` (31 tests). The accepted C1-01 contract is unchanged: the C1 analytical owner was generalized only where a court could not otherwise be expressed, and all 13 accepted C1-01 tests still pass.

Two requirements are explicitly **not** claimed rather than passed silently: the AT10 underpowered/adaptive branch distinct state, and the AT11 adaptive unvisited territory. No exhaustive-coverage claim is made anywhere.

### Owner generalizations added

1. Governed `EMPIRICAL_POSITION_COORDINATE` leaves participate in the condition-value witness relation law alongside `SURVEY_RESPONSE_EVENT` leaves, matched on the semantic-ref key belonging to each leaf type.
2. Discovery consumption selects the candidate fact whose condition predicate is the winning predicate, instead of positionally taking `fact_refs[0]`.
3. Recursive lineage closure absorbs the retained discovered-grammar atom ancestry refs, so the full ancestor chain required by the owner reaches past the immediate parent.

No upstream empirical, discovery, recursive or consumer owner was modified. AT13's required non-scalar grain (RANKED_RESPONSE component vectors) was expressible in existing owners, so neither `EXISTING_OWNER_CHANGE_REQUIRED` nor `AUTHORITY_GAP` applies.

### Wider regression state

Three-tree node-ID attribution across the correction head, the C1-02 return, and the accepted C1-01 baseline yields identical failing sets. Verdict: `NO_WIDER_REGRESSIONS_DETECTED_AT_ACCEPTED_C1_01_BASELINE_GRAIN`. The 45 failed, 7 errored and 9 non-collecting entries in `rawlsing_next/tests` are pre-existing at the accepted baseline and were left untouched. No frozen expectation was edited.

### Documentary correction

The version-1 C1-02 acceptance matrix and oracle freeze are withdrawn. They asserted six AT passes using test names that did not exist, and listed frozen oracles for courts that were never implemented. The withdrawal is recorded in place so the supersession chain remains auditable.
