# R3 FIELD AND ADAPTER CONTRACT — exact C11 fields and native-evaluator view

**Status:** `CONDITIONAL_EXTENSION`; actual schema inspected at product cut
`cea2d4d3009e9087d2267e9d1f53bec28b730dc7`; no product edit.
**Purpose:** answer G2/G4/G5 with exact field/ref keys and a concrete adapter
into the existing native evaluator.

## 1. Exact C11 fields versus external/hold

| Family | Exact C11 fields (inspected) | Not in this field | Resolution |
|---|---|---|---|
| `EmpiricalUniverse` | `raw_source_identity`, `source_family`, `study_product_release`, `instrument_release`, `country_geography`, `sampling_geography`, `raw_wave`, `canonical_wave_if_governed`, `field_or_reference_time`, `target_population_and_sample_frame`, `sampling_design_regime`, `respondent_namespace`, `source_artifact_import_lineage`, `harmonization_authority_ref`, `source_relation_refs` | household/roster namespace; PSU/strata/replicate weights/design variance; numeric uncertainty | external source/codebook/design artifact by exact universe/source identity; else typed absent/hold |
| `RespondentIdentity` | `empirical_universe_ref`, `respondent_key`, `source_native_respondent_key_ref_or_typed_absence`, `identity_map_authority_ref_or_typed_absence` | household/roster membership | source-specific projection if released; else typed absent; no inferred household |
| `QuestionVariableBinding` | `empirical_universe_ref`, `native_question_ref`, `instrument_question_version`, `canonical_question_ref_or_typed_absence`, `component_subitem_ref_or_typed_absence`, `semantic_authority_ref`, `topology_authority_ref` | original-language item/option/form/ballot content; routing content | external source/codebook/questionnaire artifact by exact native ref/version; routing state in `RoutingEligibilityFact`; typed absent if unavailable |
| `RespondentEvent` | `empirical_universe_ref`, `scoped_respondent_ref`, `native_question_ref`, `canonical_question_ref_if_authorized`, `component_or_subitem_ref`, `event_group_id`, `response_event_id_or_deterministic_index`, `raw_response_value`, `canonical_response_value_if_authorized`, `value_transform_authority_ref`, `response_topology_ref`, `multiplicity_order_rank_fields`, `response_state` | option/form text | native/source codebook by ref; value/state preserved |
| `RoutingEligibilityFact` | `empirical_universe_ref`, `scoped_respondent_ref`, `question_or_target_ref`, `risk_set_ref`, `routing_rule_ref`, `applicability_state`, `routing_state`, `parent_predicate_refs`, `member_set_replay_ref` | original option/form text | routing state/rule refs preserved; option text external |
| `EmpiricalCoordinateFact` | `empirical_universe_ref`, `scoped_respondent_ref`, `native_coordinate_ref`, `canonical_coordinate_ref_if_authorized`, `raw_coordinate_value`, `canonical_coordinate_value_if_authorized`, `unit_category_taxonomy_ref`, `effective_or_reference_time`, `coordinate_state`, `normalization_crosswalk_authority_ref`, `source_semantic_authority_ref` | household/roster, design variance | external/source or typed absent |
| `WeightMeasureFact` | `empirical_universe_ref`, `scoped_respondent_ref`, `weight_basis_id`, `exact_weight_value_representation`, `weight_state`, `weight_source_ref`, `design_authority_ref`, `estimand_authority_ref`, `normalization_or_recalibration_rule_ref`, `effective_scope_ref` | PSU, strata, replicate weights, design variance | external design/weight artifact or typed absent; `design_authority_ref` is an authority ref, not the variance data |
| `EmpiricalFact` | `empirical_query_spec_ref`, `empirical_universe_refs`, `target_topology`, `condition_predicate_ref`, `risk_set_ref`, `raw_numerator_support`, `raw_denominator_support`, `weighted_numerator_support_if_authorized`, `weighted_denominator_support_if_authorized`, `measure_basis_ref`, `response_state_semantics_ref`, `uncertainty_method_or_typed_state`, `source_empirical_provenance_refs`, `replay_ref` | numeric variance/interval | external F6 method/uncertainty product or typed absent; method/state is not a numeric interval |
| `AuthoritySnapshot` | authority id/version/hash/kind, decision state, governed operations/families, scope, time, parents, negatives, supersession, replay protocol | source codebook content | exact authority/revocation lookup |
| `SourceUniverseRelation` | relation id/kind, exact universe refs, relation authority, effective scope, overlap/nonduplication evidence, composition estimand refs, dedup rule, negative limits | direct respondent link | separate relation authority; no inferred person join |

**Rule:** every requested meaning must resolve to exactly one of: C11 exact
field, external immutable source/codebook/questionnaire/design artifact by exact
identity, or typed absent/hold. No generic "source owner will handle it".

## 2. Exact per-family read view keys

### 2.1 Universe/release

`universe_key = ExactRef(EmpiricalUniverse@1.0.0, object_id, content_hash)`.
`release_key = ExactRef(C11LogicalRelease, object_id, content_hash)`. Current
authorization is a separate `current_authorizer` check, not a field.

### 2.2 Respondent

`respondent_key = (universe_key, respondent_key)`; exact `ref` plus native key
ref/typed absence and identity-map authority/typed absence. A household/roster
key is **not** defined by this schema; it must come from a source-specific
external projection or typed absent.

### 2.3 Event/occurrence

`event_key = (universe_key, respondent_ref, native_question_ref,
canonical_question_ref_or_absence, component_ref_or_absence, event_group_id,
response_event_id_or_deterministic_index, response_topology_ref,
multiplicity_order_rank_fields, response_state)`; exact `ref` must match.
Duplicate event key → refusal. No first-value collapse.

### 2.4 Routing

`routing_key = (universe_key, respondent_ref, question_or_target_ref,
risk_set_ref, routing_rule_ref, applicability_state, routing_state,
parent_predicate_refs, member_set_replay_ref)`. Multiple conflicting routing
facts for the same key → typed ambiguity/refusal; missing → typed absence.

### 2.5 Coordinate

`coordinate_key = (universe_key, respondent_ref, native_coordinate_ref,
canonical_coordinate_ref_or_absence, effective_or_reference_time,
coordinate_state)`; exact `ref`, unit/taxonomy, normalization/crosswalk
authority. Multiple values at the same time/key → refusal unless a declared
version/authority distinguishes them.

### 2.6 Weight

`weight_key = (universe_key, respondent_ref, weight_basis_id,
effective_scope_ref, weight_source_ref, design_authority_ref,
estimand_authority_ref, weight_state)`; exact representation. Multiple active
weights for the same operation/scope → refusal; nonpositive/unknown is not 1.0.

### 2.7 Fact

`fact_key = (query_ref, universe_refs, target_topology, condition_predicate_ref,
risk_set_ref, measure_basis_ref, response_state_semantics_ref)`. Exact
numerator/denominator support, provenance, replay; typed state. A fact is not a
weight/design variance or FF01 distribution.

## 3. Adapter into the existing native evaluator

**Already implemented route:** `DirectEstateI03Session.indices_for(query,
release_refs)` returns a tuple of `(universe_ref, _ReleaseIndex)`.
`_ReleaseIndex` carries `release`, `universe`, `respondents`,
`events_by_respondent`, `coordinates_by_respondent`, `routing_by_respondent`,
`weights_by_respondent`, `source_relations`,
`native_verified_physical_respondent_order`. `execute_empirical_query` accepts
`C11Repository` or exact `DirectEstateI03Session`; exact `SavedC11Admission`
remains the wrapper guard.

**Proposed read-only adapter (not implemented):**

```text
R3DerivedReadView
  .release_ref / .universe_ref / .current_authorizer
  .respondents() -> Iterator[RespondentIdentity]
  .events_for(respondent_ref, target_refs, occurrence_scope)
      -> Iterator[RespondentEvent]
  .routing_for(respondent_ref, target_ref, risk_set_ref)
      -> RoutingEligibilityFact
  .coordinates_for(respondent_ref, coordinate_ref, time_scope)
      -> Iterator[EmpiricalCoordinateFact]
  .weights_for(respondent_ref, weight_basis_id, effective_scope_ref)
      -> Iterator[WeightMeasureFact]
  .selection_membership(release_ref, universe_ref, condition_predicate_ref,
      risk_set_ref, ordered_target_refs, direction, routing_states,
      weight_basis_id, measure_basis_ref)
      -> SelectionMembership (candidate refs + nonselected count)
  .indices_for(query, release_refs) -> tuple[(universe_ref, _ReleaseIndex)]
  ._live() / .check_current() -> bool
```

The adapter must yield **exact existing objects/refs**, not new fact rows. It
must expose the full risk population and nonselected members; the native
evaluator still decides eligibility, denominator, weights, typed states and
fact construction. A new exact protocol branch in `execute_empirical_query` is
an owner-qualified extension; it is not implemented here and must not be a
second evaluator.

**Selection membership reuse:** share only when
`(release, universe, condition predicate, risk set, ordered targets, direction,
routing states, weight basis, measure)` is identical. Do not share across
forward/reverse F2, weighted/unweighted, missing/routing states or waves.
Membership is candidate refs, not a fact/denominator/evidence cache.

**Lifetime/cost:** derived view is read-only, per release/universe; in-memory
ephemeral or content-addressed sidecar. Disk/RAM bounded by selected
partition/row groups; no full object graph. Invalidate on source/release/frame/
current/revocation change. Sparse selection uses exact postings; full-domain
k-way uses exact support enumeration. No Q-reduction claim before measurement.

## 4. Explicit holds

- Original-language option/form/ballot content: external source/codebook by
  exact native ref; typed absent/RIGHTS_HELD if unavailable.
- Household/roster identity: source-specific external projection or typed
  absent; not canonical by fiat.
- PSU/strata/replicate weights/design variance/numeric uncertainty: external F6
  design/uncertainty input or typed absent; not in `WeightMeasureFact`/
  `EmpiricalFact`.
- FF01-k method/eligibility/ratio/weighted estimand: owner-held science.
- Native/source/actor rights: separate.
