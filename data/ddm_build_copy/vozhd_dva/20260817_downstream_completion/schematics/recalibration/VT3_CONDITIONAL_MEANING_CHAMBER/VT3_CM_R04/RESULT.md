# VT3-CM-R04 — Terminal Position-Conditioning Requirements

**Cell:** `VT3-CM-R04`  
**Court:** Vozhd Trii Conditional-Meaning Chamber  
**Repository:** `maidiu/rawlsing`  
**Authorized branch:** `agent/vozhd-trii-vt3-cm-r04`  
**Exact shared launch base / repository head examined:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Mode:** terminal-demand architecture/semantic court only  
**Production code modified:** `NO`  
**Verdict:** `TERMINAL_POSITION_CONDITIONING_REQUIRED__SPARSE_AUTHORITY_FIRST_CONDITIONAL_EVIDENCE`

## 0. Executive holding

Rawlsing terminal runtime does require position-conditioned empirical/structural meaning, but it does **not** require a demographic predictor that turns a generated actor position into an expected belief, response, personality, or life event.

The minimum terminally necessary contract is:

1. producer-governed **position-conditioned empirical distributions/support** must remain available where empirical heterogeneity by structural position is part of the lawful evidence basis;
2. runtime-facing **position-conditioned structural priors/conditions** must preserve the exact structural meaning that changes when an already-generated position binding is supplied;
3. `ContextResolver` must select/defer those structural objects deterministically against exact `V3_GENERATED_POSITION_BINDING@1.0.0` bindings, preserving full lawful multiplicity, native geography, temporal support, uncertainty, negative authority, and provenance;
4. actual opportunity, encounter, exposure, route traversal, response, memory, belief, orientation, and attractor development remain V3-generated history and may diverge for two actors with the same structural position;
5. population position prevalence is a **separate authority class** used only if an accepted ADP-009 rule lawfully needs a `GOVERNED_POSITION_DISTRIBUTION`; prevalence never fills a missing binding and never becomes `P(actor has position)` by convenience;
6. multi-position/intersectional conditioning is required only where separately governed empirical evidence demonstrates that the conjunction carries structural meaning not preserved by independent conditions; no Cartesian-product explosion, greedy best-predictor tree, or naive combination is terminally authorized.

The central noncollapse is:

```text
GENERATED ACTOR POSITION
!= POSITION-CONDITIONED STRUCTURAL WORLD
!= ACTOR OPPORTUNITY / ENCOUNTER / EXPOSURE
!= ACTOR KNOWLEDGE / BELIEF / RESPONSE
```

A conditional survey distribution may be legitimate evidence for the second term. It is never, by itself, evidence for the fourth.

## 1. Governing law directly inspected

All evidence below was inspected at exact repository base `8c87f7725ba58202b5377c974548140420709fa9` unless an authority document records its own historical launch base.

### 1.1 Binding architecture / spirit

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md` — blob `588cf3954c33417665c5f9bac04e8b27e75d7f7c`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/TERMINAL_DEMAND_ENVELOPE.md` — blob `6b698f37c034a2bf87cde0fdc68f217081cbe3fd`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/ARCHITECTURE_PASS_LAW.md` — blob `8f3b2db350109bc0b5839252968e35c8a064aef9`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md` — blob `81fa4881fcdd683e79a781cc23cc44670bf4b0a1`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V557_V558_COMPLETION_IMPLEMENTATION_RULING.md` — blob `fc9952d8492cafaa7acd6324c2a99bf416ffb123`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V3_COMPLETION_IMPLEMENTATION_RULING.md` — blob `49095f763c5c371d98bb57a01aaf5f47dc7b1ae1`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V553_COMPLETION_IMPLEMENTATION_RULING.md` — blob `97a687722f1e3bbef8fac5728343fe2bd81497f1`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V554_COMPLETION_IMPLEMENTATION_RULING.md` — blob `c63c7309b86a68087961a7062e5ea628d0da3f2b`.
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/integration/V556_COMPLETION_IMPLEMENTATION_RULING.md` — blob `512fda8ac1a6e7595b84c0be0897c69e63a8d395`.

### 1.2 Accepted runtime authorities materially constraining this court

- `schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_009_V3_POSITION/AUTHORITY.md` — blob `b30606e10bcb335d5a757638652693e9a540c410`; authority `V3_STRUCTURAL_POSITION_GENERATION_MOBILITY_RULE@1.0.0`.
- `schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.md` — blob `f17e2b6b306c5d3cf58c483fa1185a9c5e01138d`; authority `V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`.
- `schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_017_V3_ACTOR_ACCESS/AUTHORITY.md` — blob `6b4162df27003bec413074178c46fea6360d71a0`; authority `V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0`.
- `schematics/release/W2_AUTHORITY_CONTRACT_COMPLETION/CAN_005_CONTEXT_RESOLVER_POLICY_BINDING/AUTHORITY.md` — blob `2b85f3737b6a14191832ab4cc14b89428ca6c3fb`; authority `V558_CONTEXT_RESOLVER_POLICY@1.0.0`.
- `schematics/release/W2_AUTHORITY_CONTRACT_COMPLETION/CAN_006_GENERATED_POSITION_BINDING/AUTHORITY.md` — blob `225faa69c4f0a25268010fc626e381addd22928a`; authority `V3_GENERATED_POSITION_BINDING_CONTRACT@1.0.0`.

### 1.3 V550 evidence inspected as evidence, not authority

- `data/ddm_build_copy/ddm_v550_position_distribution.py` — blob `651329254244e9f42a8d88c2721ccae6bd768073`.
- `data/ddm_build_copy/ddm_v550_branching.py` — blob `8f6d40e0d016d66e5a3b334b31747eaef752873f`.
- `data/ddm_build_copy/build_determinicity_repository_v550.py` — directly inspected at the launch base; it imports and emits the current V550 conditional/determinicity artifact families.

Directly observed V550 behavior relevant to this court:

- `INDICATOR_FIELDS` is a fixed legacy list of twelve string fields: `sex`, `age_group`, `education_level`, `income_level`, `religion_label`, `urban_rural`, `region`, `ethnicity`, `language`, `employment`, `marital`, `household_size`.
- `indicator_answer_matrix_rows()` creates response counts and shares for every observed `(indicator_name, indicator_value, response_value)` cell, weighted and unweighted where weights exist. This is the closest existing V550 artifact to an explicit empirical conditional distribution.
- `build_position_distribution_rows()` creates marginal prevalence by `position_field` / `position_value` within source/wave/country; its declared `semantic_role` is `POSITION_COORDINATE`.
- `indicator_summary_rows()` and `secondary_indicator_summary_rows()` rank indicator usefulness using entropy reduction / mutual information / Cramér's V and dominant-response quantities.
- `secondary_indicator_summary_rows()` selects one primary indicator by maximum predictive score and reports secondary gain against it.
- `branch_nodes_rows()` is a greedy recursive splitter using entropy gain, bounded depth, support thresholds, and only the first two value branches at each selected split.
- `outlier_cohort_rows()` reduces each cohort to dominant-response comparison against the baseline.

These implementation facts establish that V550 contains real conditional empirical information, but they do not establish that the current ranking/tree/summary artifact shapes are terminal semantics.

## 2. Constitutional separation

The governing spirit requires a person to be causally intelligible without being inevitable and explicitly states that structural priors may constrain developmental possibility but may not become psyche. Whole-machine closure and V3 law make the runtime seam concrete:

```text
Phase A structural context
-> V3 generates actor-specific position fact
-> CAN-006 binding
-> Phase B re-resolution of the SAME immutable repository
-> position-specific structural context
-> V3 opportunity / encounter / exposure / route / response / history
```

Therefore the thing that must vary by generated position at V558 is **the structural field lawfully applicable to that position**, not a precomputed actor destiny.

Two actors may share identical position bindings and receive identical structural context while later diverging because opportunity realization, encounters, exposures, route traversal, responses, relationships, memory, contingency, and governed randomness differ. Conversely, two actors in different positions may receive materially different structural conditions even before either actor has experienced them.

This is the required distinction between:

### A. Actor generated position

Owned by ADP-009 and transported through CAN-006 as immutable `GENERATED_RUNTIME_FACT_REF`. It answers what objective structural position is currently true of this actor under an accepted position rule.

### B. Structural world conditioned on that position

Producer-owned structural evidence/priors whose applicability or value is conditioned by exact governed position predicates. This is the domain of this court's terminal requirement.

### C. Actor knowledge/accessibility

Owned downstream by generated memory/epistemic/access authorities, especially ADP-017. The fact that a structure is position-conditioned and causally operative does not make its mechanism actor-known.

### D. Actor belief/response

Generated only by owning V3 causal rules and history. A survey response distribution for people occupying a position is not a belief record for the generated actor and is not permission to initialize one.

## 3. Court-question verdicts

| Candidate requirement | Verdict | Terminal consumer / causal role |
|---|---|---|
| `P(response | generated position)` | `REQUIRED_AS_EMPIRICAL_SUPPORT_WHEN_RESPONSE_SEMANTICS_ARE_LAWFUL_STRUCTURAL_EVIDENCE__FORBIDDEN_AS_ACTOR_RESPONSE_PRIOR` | Producer structural derivation, V557 publication fidelity, V558 audit/context selection. It preserves heterogeneity and weak alternatives. It does not write actor belief/response. |
| position-specific structural pressure | `REQUIRED_WHERE_GOVERNED_EVIDENCE_SUPPORTS_POSITION_EFFECT` | V3 receives a structural field whose constraints/opportunities/affordances differ lawfully by position; later V3 history determines realization. |
| position-specific opportunity/exposure only | `INSUFFICIENT_AND_JURISDICTIONALLY_WRONG_AS_SUBSTITUTE` | ADP-010 owns opportunity/encounter/exposure. Structural conditioned evidence must exist before lived realization; actual OEE cannot be precomputed from survey conditionals. |
| mere position metadata | `REQUIRED_FOR_BINDING_BUT_NOT_SUFFICIENT_FOR_CONDITIONAL_MEANING` | CAN-006/CAN-005 use exact binding keys; metadata alone contains no empirical structural effect. |
| population position prevalence | `NOT_REQUIRED_FOR_PHASE_B_CONTEXT_RESOLUTION; CONDITIONALLY_REQUIRED_UNDER_SEPARATE_ADP009_AUTHORITY` | Only `GOVERNED_POSITION_DISTRIBUTION` may supply candidate/weight semantics for an ADP-009 rule. Raw prevalence cannot fill actor membership. |
| multi-position conjunctions | `REQUIRED_ONLY_WHERE_SEPARATELY_GOVERNED_AND_EMPIRICALLY_SUPPORTED` | Allows a structural effect genuinely specific to conjunction `A∧B`; no Cartesian materialization or independent-product inference. |
| intersectional conditions | `SAME_AS_MULTI_POSITION_CONJUNCTIONS; NONADDITIVE_EFFECT_REQUIRES_EXACT_CONJUNCTION_AUTHORITY` | Prevents flattening historically meaningful intersections while blocking demographic stereotype synthesis. |
| temporal change in conditional distributions | `REQUIRED_WHERE_EVIDENCE_IS_TIME_VARIANT_OR_WAVE_BOUND` | V553 temporal authority / CAN-005 direct/proxy selection must distinguish evidence time and query time; no stationarity default. |
| country/region-conditioned position effects | `REQUIRED_AT_NATIVE_PRODUCER_SCOPE_WHERE_EVIDENCE_IS_GEOGRAPHICALLY_SCOPED` | Context varies by native geography without country→position or national→local imputation. |
| explicit uncertainty/support | `REQUIRED` | Prevents weak cells and minority alternatives from becoming deterministic facts; supports admissibility, typed underpower, replay and audit. |

## 4. Terminal-demand contract — required semantic object families

The following are **semantic roles required by terminal demand**. They do not imply a new numbered stage. Existing producer families should carry them by exact reference or bounded extension where possible. Direct DAG reuse is preferred over duplication.

### Family R04-F1 — `POSITION_CONDITIONED_EMPIRICAL_DISTRIBUTION`

Purpose: preserve the empirical heterogeneity actually observed under an exact governed position condition.

Minimum semantic content:

```text
conditional_distribution_id
source_evidence_refs[]
question_or_measure_semantic_ref
response_or_measurement_value_ref
conditioning_predicate_ref
conditioning_bindings_required[]
native_geography_scope_ref(s)
evidence_time_or_support_ref
finite_stratum_refs[] where governed
absolute_horizon_ref(s) only where explicitly governed
n_unweighted
n_weighted_or_null
weight_status
conditional_share_unweighted
conditional_share_weighted_or_null
denominator_unweighted
denominator_weighted_or_null
support_state
uncertainty_or_sampling_state
response_semantics_authority_ref
producer_authority_ref/version/hash
negative_missing_noncomparability_refs[]
provenance_refs[]
content_hash
```

Rules:

- The complete lawful outcome distribution must remain recoverable. Modal-only storage is insufficient.
- Minority outcomes with lawful support remain present even if numerically small.
- `response_or_measurement_value_ref` is evidence content, not an actor belief/response fact.
- Counts/shares must identify their denominator and weighting regime.
- Underpowered/unknown/missing/noncomparable states remain typed; they are not normalized into a plausible distribution.
- Conditioning uses exact governed position dimensions/values/predicates, not raw display labels.
- If the evidence is survey response data, a separately governed semantic mapping must establish what structural meaning, if any, can be derived from it.

**No-starvation proof:** without F1 or an exactly equivalent reachable evidence object, a downstream position-conditioned structural assertion can preserve only a dominant summary or opaque scalar. Minority alternatives, support quality, provenance, and the empirical basis for the position effect become irrecoverable.

### Family R04-F2 — `POSITION_CONDITIONED_STRUCTURAL_PRIOR_OR_CONDITION`

Purpose: expose the actual runtime-facing structural meaning that changes when a generated position binding is supplied.

This need should normally be satisfied by existing producer-owned semantic families—V552 structural fact, V553 temporalized object, V554 applicability condition, V555 route condition, V556 F1/F2 condition—carrying or referencing an exact position predicate and its evidence lineage. R04 does **not** justify a duplicate generic pressure stage.

Minimum semantic content when position-conditioned:

```text
producer_object_ref/hash
producer_semantic_family
semantic_resolution_key_ref
structural_source_ref(s)
structural_target_ref(s)
direction_or_relation_refs where governed
position_condition_predicate_ref/version/hash
required_binding_key_ref(s)
condition_cardinality_and_boolean_semantics
conditioned_empirical_support_ref(s) where empirical
native_geography_scope_ref(s)
temporal_support/evidence_ref(s)
finite_stratum_role_refs[] where governed
absolute_horizon_refs[] only where governed
epistemic_class
allowed_use_state
negative/limit/unknown/missing/noncomparability state
producer rule/evaluator refs and versions
provenance refs
```

The position predicate states only when this structural object is applicable or which structural value/distribution is authoritative for the bound position. It does not assert actor experience, belief, orientation, or response.

**No-starvation proof:** if only global structural priors survive, two actors in historically distinct structural positions receive an artificially homogenized world. V3 can no longer reproduce position-specific constraints/opportunities without inventing them downstream.

### Family R04-F3 — `GOVERNED_POSITION_DISTRIBUTION` — separate authority, conditional terminal need

This family is **not** part of ordinary V558 Phase-B context lookup. It exists only when an accepted ADP-009 position rule explicitly requires distributional candidate/weight authority.

Minimum content follows ADP-009's existing requirement: exact candidate position refs, scope, effective time, governed probability/weight semantics, support/provenance, and rule authority sufficient to authorize candidate generation or weights.

Raw V550 `position_distribution` prevalence is not automatically F3. It becomes F3 only through separate accepted authority. ContextResolver may never use F3 to infer a missing actor position.

**No-starvation proof:** some future position-generation rules may need historically grounded candidate distributions. Without a governed F3, those rules must correctly return missing/deferred authority rather than fabricate demographics.

## 5. Exact dimensions / keys required

Terminal conditional semantics must support these key classes where relevant to the producer object:

1. **semantic measure key** — exact question/measure/structural semantic ref, never a display string alone;
2. **generated-position binding key** — exact CAN-006 `binding_key_ref` / ADP-009 position dimension or requirement ref;
3. **position target/value ref** — exact governed target, or exact explicit absence only if position authority supports it;
4. **conditioning predicate identity** — versioned boolean predicate/evaluator with declared cardinality;
5. **native geographic scope** — country/region/locality only at producer-governed grain, with exact scope refs;
6. **time** — source evidence time/support interval, query-compatible granularity, and temporal authority refs;
7. **structural source/target/direction/relation** — whenever the conditioned evidence supports relational pressure meaning;
8. **finite stratum role refs** — `0..n`, role-qualified, never synthesized from the V550 indicator name;
9. **Absolute Horizon refs** — only explicit governed designation, never inferred from religion/ideology fields;
10. **response/measurement outcome** — full set of lawful observed categories/values, not merely the dominant response;
11. **support/weight keys** — numerator, denominator, weighted/unweighted regime, support/admissibility state;
12. **authority/provenance** — source evidence, mapping authority, producer rule/version/hash, exact transitive refs;
13. **typed negative/absence state** — unknown, missing, noncomparable, denied, valid-empty, explicit zero, unbound runtime position, missing evaluator/authority, integrity failure.

There is no terminal warrant for the current V550 twelve generic indicator fields as a fixed ontology. A V550 column becomes a terminal position key only if a governed mapping binds it to an accepted structural-position dimension/requirement. `region` as a string column, for example, cannot silently become an ADP-009 position fact or a CAN-006 binding key.

## 6. Forbidden inferences

The following are terminally forbidden:

1. conditional survey response -> generated actor belief, knowledge, psychology, personality, orientation, memory, or response;
2. modal conditional value -> actor destiny or default state;
3. population prevalence -> actor membership;
4. raw prevalence -> stochastic ADP-009 weights without separate governed authority;
5. geography -> class/sect/party/institution/occupation/household/family/Self position;
6. geography -> actor belief or psyche;
7. position -> guaranteed opportunity, encounter, exposure, route traversal, or response;
8. structural availability/applicability -> lived history;
9. independent one-position effects -> inferred conjunction/intersection effect;
10. absent intersectional evidence -> demographic stereotype fallback;
11. temporal proximity -> direct support;
12. future conditional evidence -> historical lived exposure;
13. national evidence -> local estimate through relabeling or proximity;
14. highest mutual information / Cramér's V / entropy reduction -> semantic authority;
15. greedy branch winner -> canonical intersectional ontology;
16. dominant response -> complete conditional distribution;
17. underpowered cell -> zero/false/neutral/modal fallback;
18. missing weight -> silently weighted estimate;
19. index hit / label match -> semantic applicability;
20. two co-resolved conditional objects -> newly inferred V556 interaction.

## 7. Typed absence / unknown / deferred law

Conditional evidence must preserve the following distinct states or terminally equivalent typed states:

- `VALID_EMPTY_CONDITIONED_SAMPLE_OR_NO_LAWFUL_OUTCOMES` — only when producer authority explicitly establishes valid-empty semantics;
- `POSITION_CONDITION_NOT_APPLICABLE` — supplied binding does not satisfy the exact predicate;
- `UNBOUND_REQUIRES_RUNTIME_POSITION` — required generated position binding is absent;
- `POSITION_BINDING_CURRENTNESS_UNKNOWN` / stale / not-effective states from CAN-006;
- `MISSING_CONDITIONING_AUTHORITY` — no accepted mapping/predicate says this empirical dimension is a structural position condition;
- `MISSING_CONDITIONAL_EVIDENCE` — condition is meaningful but no evidence supports the requested time/scope;
- `UNDERPOWERED_CONDITIONAL_SUPPORT` — observed cell exists but support fails governed active-use threshold; evidence may remain review/context-visible if authority permits;
- `UNKNOWN_CONDITIONAL_VALUE` — evidence cannot establish the distribution/value;
- `NONCOMPARABLE_CONDITIONAL_EVIDENCE` — candidate observations cannot lawfully combine/compare;
- `NEGATIVE_OR_LIMIT_AUTHORITY` — exact producer denial/limit;
- `NO_LAWFUL_TEMPORAL_ANCHOR` — CAN-005 temporal court cannot resolve direct or authorized proxy evidence;
- `DEFERRED_MISSING_PRODUCER_EVALUATOR` — condition exists but evaluator authority is unavailable;
- `AMBIGUOUS_EQUAL_RANK_AUTHORITY` — incompatible same-rank candidates with no governed precedence;
- `INTEGRITY_FAILURE` — ID/hash/schema/reference/provenance corruption;
- explicit numeric `0` — an observation, never missingness.

Fallback to global/unconditioned evidence is lawful only if an explicit producer/resolver rule says the unconditioned object remains separately applicable when a conditioned object is unavailable. Missing conditioned evidence by itself does **not** authorize fallback.

## 8. Intersectionality / multi-position conjunction law

Intersectionality is terminally necessary as a **capability**, not as universal precomputation.

A conjunction such as `(class=A ∧ region=B)` is a distinct condition only when all of the following are governed:

1. exact component binding keys/target refs;
2. exact conjunction predicate identity/version;
3. order/cardinality semantics;
4. empirical support for the joint cell or other accepted structural authority;
5. support/admissibility state and weighting semantics;
6. native geography and time;
7. structural meaning that is not safely reducible to independent single-position applicability;
8. provenance and replay.

No terminal law authorizes:

- generating all pairwise/three-way combinations;
- choosing conjunctions because they maximize predictive power;
- multiplying independent probabilities;
- adding marginal effects;
- using a greedy recursive branch as ontology;
- treating missing joint cells as the modal demographic stereotype.

If A and B each independently govern an object and no interaction semantics are established, the resolver may lawfully return both independent objects. It may not synthesize an `A∧B` object. If the historical effect exists only at the conjunction and no governed joint evidence exists, the correct state is missing/deferred authority, not flattening.

## 9. Temporal requirements

Position-conditioned structural meaning is historical. Terminal support therefore requires:

- exact evidence time or producer-governed support interval;
- source wave/reference time retained separately from query time;
- no implicit stationarity across waves;
- V553 temporal identity/observation/relation/limit preservation where temporalized structural meaning exists;
- CAN-005 precedence: `DIRECT_TEMPORAL_SUPPORT > authorized LATEST_PRIOR > authorized EARLIEST_POST > NO_LAWFUL_TEMPORAL_ANCHOR`;
- proxy authority and signed lag preserved separately from original evidence;
- position binding effective/as-of time verified by CAN-006;
- position transitions trigger prospective re-resolution; earlier contexts/history are not rewritten;
- intersectional evidence must itself be supported at the relevant time, not borrowed from another period merely because the position labels match.

A time-varying conditioned distribution need not be stored as a separate dense time series if V553-style sparse observations plus explicit temporal authority can reconstruct the lawful query-time structural prior without loss.

## 10. Geography requirements

Country/region conditioning is required when it is part of source scope, but geography has two distinct roles:

1. **native scope of the empirical/structural object**;
2. **actor generated position**, if location itself is lawfully generated by an accepted position owner.

These roles may coincide in a query but cannot infer one another.

Rules:

- preserve exact producer native geography;
- no nearest geography, neighboring-region fallback, or down-imputation;
- country-conditioned position effects remain country-scoped unless producer authority supplies a lower-grain applicability relation;
- a national position effect may constrain a local actor only through the producer's governed scope relation; it does not become a locality estimate;
- geography does not satisfy an unrelated generated-position requirement;
- migration may change generated location and trigger re-resolution, but does not automatically change other position dimensions.

## 11. Explicit uncertainty and support requirements

A conditional object is not lawfully usable merely because a cell exists.

At minimum retain/reach:

- unweighted cell numerator and denominator;
- weighted numerator/denominator where lawful weights exist;
- `weight_status` and exact weight authority/provenance;
- support threshold/admissibility rule and result;
- full outcome distribution including minority outcomes;
- missing-response / excluded-response semantics where relevant;
- response-option semantic authority;
- source sample/wave/country provenance;
- uncertainty/confidence interval or other uncertainty state **only when governed**; absence of a formal interval must not be disguised as certainty;
- noncomparability and mapping uncertainty;
- source evidence and derived structural prior as distinct epistemic classes.

Predictive strength is not a substitute for support quality. A high mutual-information split with weak or ungoverned support cannot acquire causal authority merely because it predicts well.

## 12. Population prevalence verdict

Population position prevalence is **not** part of the minimum evidence V558 needs to resolve an already-bound actor's position-conditioned context.

Once CAN-006 supplies an exact current binding, ContextResolver asks: which producer objects are applicable to this exact position? It does not ask: how common is this position?

Population prevalence is separately needed only when an accepted ADP-009 rule declares a `GOVERNED_POSITION_DISTRIBUTION` as candidate/selection authority. ADP-009 already forbids raw prevalence-to-membership and raw prevalence-to-weight conversion.

Therefore current V550 `position_distribution` has no automatic terminal-causal status. It may be valuable source evidence for a future governed position-distribution authority; otherwise it is descriptive/audit material.

## 13. Minimal evidence for lawful V558 position-conditioned resolution

For a position-conditioned structural key, V558 must have all of the following or return the relevant typed failure/deferred state:

1. immutable repository bundle ID/content hash and complete logical index manifest;
2. exact requested semantic resolution key;
3. exact producer object ID/hash/schema and producer authority/version;
4. producer item-use permission compatible with requested use;
5. exact versioned position-condition predicate/evaluator;
6. exact required `binding_key_ref` set and condition cardinality/boolean semantics;
7. caller-supplied, current, integrity-valid CAN-006 generated-position binding set for every required binding;
8. exact native geography applicability refs where geography is required;
9. exact temporal support/evidence time and CAN-005/ADP-006 temporal eligibility where query-time resolution is required;
10. exact empirical support/provenance ref where the structural object's position effect is empirically derived;
11. support/admissibility/uncertainty state sufficient for the producer's requested-use ceiling;
12. exact negative/limit/unknown/missing/noncomparability refs;
13. finite-stratum / Absolute-Horizon refs where producer semantics require them;
14. full provenance/reference closure sufficient to reproduce why the conditioned object was selected, rejected, deferred, or ambiguous;
15. `SelectionRecord` and `ContextResolutionReceipt` preserving binding and evidence lineages separately.

V558 does **not** need to materialize every raw survey cell into `ResolvedStructuralContext` if the runtime-facing producer object is sufficient and the complete conditioned empirical support remains exactly reachable by reference for audit/replay. This is the preferred sparse authority-first model.

## 14. V550 artifact dispositions under terminal demand

These are terminal-demand dispositions, not a claim about what other chamber cells may find as intermediate/diagnostic value.

| Current V550 artifact/mechanism | R04 disposition | Reason |
|---|---|---|
| `indicator_answer_matrix` | `RETAIN_AND_ADAPT_AS_PRIMARY_EMPIRICAL_CORE_CANDIDATE` | Preserves outcome-by-position cells, counts and shares. Must gain/go through governed position-key mapping, exact response semantics, support/uncertainty, time/geography/provenance and no actor-response interpretation. |
| `position_distribution` | `SEPARATE_CONDITIONAL_VALUE_ONLY` | Useful as marginal prevalence evidence; terminally causal only under a separate ADP-009 `GOVERNED_POSITION_DISTRIBUTION` authority. Never ContextResolver membership inference. |
| `position_indicator_summary` | `DIAGNOSTIC_OR_AUTHORING_ONLY_UNLESS_EXACT_CONSUMER_PROVED` | Mutual information / dominant-response summaries do not preserve the full conditional distribution and predictive ranking is not semantic authority. |
| `secondary_indicator_summary` | `DIAGNOSTIC_ONLY_FOR_TERMINAL_POSITION_CONDITIONING` | Best-primary / secondary-gain logic is a predictor-selection heuristic, not governed intersectional semantics. |
| `outlier_cohort_summary` | `DERIVABLE_DIAGNOSTIC` | Dominant cohort comparison loses the full distribution; terminal context requires the underlying conditional evidence if the effect matters. |
| `recursive_branch_nodes` | `NOT_CANONICAL_TERMINAL_CONDITIONAL_OBJECT` | Greedy entropy tree, bounded depth and top-two branch expansion are exploratory compression; they can erase weak alternatives and do not define lawful multi-position conjunctions. |
| branch/co-signature/cloud families | `NO_TERMINAL_REQUIREMENT_PROVED_BY_R04` | They may have other diagnostic/semantic consumers, but R04 finds no need to make them the canonical carrier of position-conditioned structural evidence. |
| fixed `INDICATOR_FIELDS` twelve-field list | `EVIDENCE_NOT_TERMINAL_ONTOLOGY` | Terminal binding keys come from accepted structural-position authority, not a hardcoded demographic column list. |

## 15. Semantic-loss findings

1. **Modal collapse:** any pipeline that retains only dominant response / dominant cohort loses minority lawful alternatives and violates the governing-spirit plurality requirement.
2. **Predictor-authority substitution:** MI/Cramér's V/entropy gain can rank empirical association but cannot say that the conditioning dimension is a lawful structural-position predicate or that its effect is causal/structural.
3. **Greedy intersection loss:** recursive best-split trees can miss non-greedy conjunctions and discard more than two category branches; they cannot be the sole terminal representation of intersectional effects.
4. **Prevalence laundering:** marginal population prevalence cannot become actor identity or stochastic weight without a separate accepted position-distribution authority.
5. **Temporal flattening:** a conditional distribution without evidence time/native wave can silently become timeless stereotype.
6. **Geographic flattening:** country-level conditional evidence relabeled to actor locality fabricates lower-grain knowledge.
7. **Epistemic laundering:** conditional survey response interpreted as actor belief/psyche crosses the structural-prior/runtime-fact/actor-access boundary.
8. **Support erasure:** a percentage without denominator/weight/support state can make a weak cell look authoritative.
9. **Position-label mismatch:** raw V550 field/value strings cannot safely satisfy CAN-006 binding keys absent governed mapping.
10. **Fallback fabrication:** missing conditional evidence cannot silently fall back to an unconditioned/modal demographic default unless producer law explicitly authorizes a distinct fallback object.

## 16. Counterevidence / constraints against overbuilding

The evidence also rejects a maximalist preservation of every V550 determinicity artifact:

1. CAN-005 already provides the exact resolver machinery needed for position requirements, binding evaluation, temporal/geographic filters, multiplicity, typed absence, and replay. R04 does not justify a second resolver or conditional inference engine.
2. CAN-006 already provides exact generated-position transport and currentness. No V550 artifact should duplicate actor position state.
3. V554 already has a lawful `REQUIRES_RUNTIME_POSITION(<exact requirement ref>)` applicability pattern. Position-conditioned structural applicability can often be represented through existing producer predicates rather than a new generic pressure family.
4. V3/ADP-010 already owns actual opportunity/encounter/exposure. Upstream conditional artifacts need not predict or materialize those events.
5. ADP-017 explicitly blocks objective/structural truth from auto-promoting to knowledge/belief. No terminal need exists for a survey-conditioned belief initializer.
6. Direct DAG reuse is binding architecture law. Full conditional evidence may remain reachable by reference while sparse runtime structural objects carry only the exact condition/effect they own.

## 17. Architecture checksum

| Terminal capability | R04 disposition | Position-conditioning contribution |
|---|---|---|
| nine-strata field | `PRESERVE_BY_REFERENCE` | condition keys may bind governed position refs; never infer strata from demographics |
| inter-strata pressure / counter-pressure | `PROVIDE_PREREQUISITE_ONLY` | conditioned structural objects may differ by position; V556 interactions remain separately governed |
| relational source / target / direction | `PRESERVE_BY_REFERENCE` | must survive with conditioned structural prior |
| temporal history / limits | `PRESERVE_BY_REFERENCE` | evidence time and V553 refs required; CAN-005 resolves lawful anchor |
| contradiction / coexisting pressure | `PRESERVE_MULTIPLICITY` | no modal winner or scalar net pressure |
| mediation | `PROVIDE_PREREQUISITE_ONLY` | position-conditioned applicability/route availability may differ; actor traversal downstream |
| buffering/amplification/deflection/blockage/rerouting | `DOWNSTREAM/PRODUCER_OWNED` | conditional evidence cannot invent these semantics |
| orientation-to-strata | `DOWNSTREAM_OWNS` | conditioned world supplies causal field; actor orientation generated later |
| Absolute Horizon | `PRESERVE_EXPLICIT_ONLY` | no religion-field shortcut |
| structural pressure-flow topology | `DIRECT_UPSTREAM_REUSE_PLUS_CONDITION` | V555/V556 objects may carry exact position predicates; no duplicate edge family |
| attractor formation | `DOWNSTREAM_OWNS` | same position can yield divergent developmental trajectories |
| actor developmental causality | `DOWNSTREAM_OWNS` | structural conditional context is prerequisite, not history |
| genealogy | `DOWNSTREAM_OWNS` | actual parent/household facts generated; demographic conditionals never substitute |
| V2 phenomenology/expression | `DOWNSTREAM_OWNS` | no direct V550/V558 personality/belief surface |
| epistemic class/provenance | `REQUIRED` | source evidence, derived prior, generated binding remain distinct |
| uncertainty/absence/noncomparability | `REQUIRED` | typed states; no stereotype fallback |
| population position generation | `SEPARATE_AUTHORITY` | ADP-009 F3 only where explicitly governed |

## 18. Direct observation versus inference

### Directly observed

- Accepted architecture explicitly requires Phase A -> generated position -> Phase B same-repository resolution.
- CAN-005 has a `GENERATED_POSITION_REQUIREMENT` logical index and evaluates exact supplied CAN-006 bindings; it forbids geography/prevalence inference and preserves typed unknown/missing/multiplicity.
- ADP-009 explicitly allows `GOVERNED_POSITION_DISTRIBUTION` only as a separately accepted candidate source and forbids raw prevalence-to-membership/weight conversion.
- ADP-010 separates structural availability from opportunity/encounter/exposure and forbids structural rows from becoming lived events.
- ADP-017 separates objective/structural truth from actor knowledge/belief/claim permission.
- V550 currently computes both marginal position prevalence and response-by-indicator distributions, plus predictor summaries, outlier summaries and greedy recursive branches.

### R04 inference from those authorities

- The minimum terminal empirical core is the **full governed conditional distribution/support plus exact structural-condition mapping**, not V550's ranking/tree/summary suite.
- A runtime-facing conditioned structural prior may remain sparse and reference the full empirical support rather than copying the raw distribution into every downstream object.
- Intersectional materialization should be evidence/authority-driven and sparse rather than generated combinatorially.
- Existing V550 `indicator_answer_matrix` is structurally closest to the needed empirical evidence role, but its current raw string indicator keys are insufficient to satisfy CAN-006 without a governed mapping.

These are architecture/semantic conclusions, not claims that R04 has proved which current V550 artifacts are already consumed or stranded; that belongs to sibling chamber archaeology/recreation courts.

## 19. Unresolved questions

1. **Missing position-key mapping authority:** which upstream authority maps a V550 conditioning field/value to an accepted ADP-009/CAN-006 structural position dimension/target ref? R04 found no generic accepted mapping in the inspected V550 helpers. This is the immediate semantic blocker to promoting raw V550 conditionals into runtime structural authority.
2. **Missing generic survey-response -> structural-effect authority:** R04 cannot infer that every conditional response distribution is structural pressure. The exact semantic mapping must be source/question/measure governed.
3. **Intersection admission authority:** no generic rule inspected here determines which multi-position conjunctions deserve canonical conditional objects, what support threshold governs active use, or whether a joint effect is irreducible. This must remain sparse/missing until governed.
4. **Physical placement:** terminal law does not require the full conditional distribution to be copied into V552/V553/V557 if exact transitive DAG reachability and audit/replay are preserved. Parent adjudication should use R01/R02/R03/R05 evidence to choose whether to retain V550 evidence directly, promote a compact producer object, or both.
5. **Uncertainty model:** V550 exposes counts/weights and simple confidence tiers in inspected helpers, but R04 does not find a universal governed sampling-uncertainty formula. Do not invent confidence intervals or scalar reliability.
6. **Existing downstream recreation:** R04 did not attempt to prove whether V551–V558 currently reconstruct equivalent conditional distributions; that is sibling R03 jurisdiction.

## 20. Recommended parent actions

1. Bind the terminal requirement as: `FULL_GOVERNED_POSITION_CONDITIONAL_EVIDENCE + SPARSE_POSITION_CONDITIONED_STRUCTURAL_OBJECT + EXACT_PROVENANCE`, not “preserve all V550 determinicity artifacts.”
2. Require R01/R02/R03 synthesis to test whether `indicator_answer_matrix` or an equivalent smaller representation preserves the complete empirical conditional distribution, support, weights, semantics, time/geography and provenance.
3. Create or identify the missing **position-key mapping authority** between empirical conditioning dimensions and ADP-009/CAN-006 binding keys before any V550 conditional artifact is active-causal.
4. Create or identify source/question-specific **conditional structural semantic mapping authority**; absent it, conditional response distributions remain evidence/context/review, not pressure or actor belief.
5. Keep population prevalence on the separate ADP-009 authority track; do not let V558 use it as actor binding fallback.
6. Require sparse conjunction admission: materialize intersectional conditional evidence only when exact joint support and semantic authority exist; preserve typed missing otherwise.
7. For V558 implementation, require SelectionRecords to preserve exact conditioned empirical-support refs whenever those refs are part of producer authority, but do not force the entire raw distribution into the resolved context payload.

## 21. Final terminal-demand statement

### THIS COURT FINDS TERMINAL RUNTIME RESPONSIBLE FOR HAVING AVAILABLE

- exact generated-position binding keys and current bindings under CAN-006;
- exact producer-owned structural objects whose applicability/value can be conditioned on those bindings;
- full governed conditional empirical support where the structural position effect is empirical;
- native geography and temporal support;
- full lawful outcome multiplicity / minority alternatives;
- explicit sample support, weighting state, uncertainty/underpower state and provenance;
- sparse governed multi-position conjunctions where irreducible joint meaning exists;
- typed missing/unbound/unknown/noncomparable/negative/integrity states;
- exact replay lineage from conditioned evidence through structural prior, resolver selection and actor binding.

### THIS COURT FINDS TERMINAL RUNTIME NOT RESPONSIBLE FOR INFERRING

- actor position from geography, prevalence or demographic labels;
- actor belief/knowledge/psyche/response from conditional population statistics;
- opportunity/encounter/exposure from structural availability;
- joint/intersection effects from independent marginals;
- temporal or geographic fallback without explicit authority;
- a dominant response as destiny;
- a greedy predictor hierarchy as structural ontology.

### TERMINAL CAPABILITIES PROTECTED

- divergent lawful lives for actors sharing a position;
- historically meaningful differences between actors occupying different positions;
- minority/weak-but-real alternatives;
- stage-blind position-conditioned context resolution;
- structural-prior / experience / belief separation;
- temporal/geographic fidelity;
- recursive genealogy without demographic biography;
- actor opacity and misrecognition;
- replayable, provenance-bearing uncertainty without graceful hallucination.

### OPEN MISSING AUTHORITY

- governed empirical-field -> structural-position binding-key mapping;
- governed conditional survey/measure -> structural-effect mapping where needed;
- sparse multi-position conjunction admission/support rule;
- any formal uncertainty estimator beyond directly supported counts/weights;
- parent synthesis decision on exact physical retention/promotion path after R01–R07 evidence.

**Final token:** `VT3_CM_R04_TERMINAL_POSITION_CONDITIONING_CONTRACT = PASS_WITH_EXPLICIT_MISSING_PRODUCER_AUTHORITIES`
