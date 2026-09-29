# C1-00 analytical-composition contract freeze — R1

Status: `C1_00_CONTRACT_ORACLE_PACKET_READY_FOR_INDEPENDENT_REVIEW`

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
