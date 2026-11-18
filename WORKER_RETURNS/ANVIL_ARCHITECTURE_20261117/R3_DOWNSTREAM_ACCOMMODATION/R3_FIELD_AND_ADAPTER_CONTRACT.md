# R3 FIELD AND ADAPTER CONTRACT — corrected residual G1/G2/G4

**Status:** `CONDITIONAL_EXTENSION`; actual schema inspected at product cut
`cea2d4d3009e9087d2267e9d1f53bec28b730dc7`; no product edit.
**Correction basis:** R3 C recheck `c996cf1a69344efb2e76e92e9adc2b723c6a2503`.
**Research refs:** R3-RES-024, R3-RES-025, R3-RES-026, R3-RES-028–032.
**Purpose:** exact C11/external field map, stable identity vs content, full
exact membership, honest cost, external artifact lookup, and FF01-2/FF01-k
separation.

## 0. Scope and grade

This is a **proposed contract**, not accepted code or a new C11 family. C11
fields are `INSPECTED_CODE`; the external artifact resolver and FF01-k product
are **proposed/owner-held**, not implemented. The existing native evaluator and
v1 fact/replay ABI remain the authority.

## 1. Exact C11 fields versus external/absent

| Requested meaning | Exact C11 field | External artifact / absent |
|---|---|---|
| Native question identity/version | `QuestionVariableBinding.native_question_ref`, `instrument_question_version`; `RespondentEvent.native_question_ref` | external artifact lookup by native ref/version |
| Original-language item/options | none | `ExternalSourceArtifact` codebook/questionnaire content; typed absent/RIGHTS_HELD if unavailable |
| Form/ballot/routing content | `RoutingEligibilityFact.routing_rule_ref`, `applicability_state`, `routing_state`, `parent_predicate_refs`, `member_set_replay_ref`; no form/ballot text | external questionnaire/form/ballot artifact |
| Respondent namespace | `EmpiricalUniverse.respondent_namespace`; `RespondentIdentity.respondent_key` | household/roster namespace is **not canonical**; source-specific external projection or typed absent |
| Event occurrence/repeat/rank | `RespondentEvent.event_group_id`, `response_event_id_or_deterministic_index`, `response_topology_ref`, `multiplicity_order_rank_fields`, `response_state` | no external requirement for occurrence identity |
| Coordinate/time/unit | `EmpiricalCoordinateFact.native_coordinate_ref`, `canonical_coordinate_ref_if_authorized`, `effective_or_reference_time`, `coordinate_state`, `unit_category_taxonomy_ref` | external crosswalk/taxonomy authority where applicable |
| Weight/design/estimand | `WeightMeasureFact` weight basis/value/state/source, `design_authority_ref`, `estimand_authority_ref`, `effective_scope_ref` | PSU/strata/replicate weights/design variance are external design artifact or typed absent; authority ref ≠ variance data |
| Uncertainty | `EmpiricalFact.uncertainty_method_or_typed_state` | numeric variance/interval is external F6 method/product or typed absent |
| Source/wave/country/time | `EmpiricalUniverse` source identity, family, releases, geography, wave, field/reference time, frame/design regime | external source metadata by exact identity |
| Source/codebook tuple identity | `native_question_ref` + `instrument_question_version` + `source_artifact_import_lineage` | external artifact lookup key; no inference from a ref alone |

**Rule:** each requested meaning resolves to exactly one of: C11 field, external
artifact field by exact identity, or typed absent/hold. A reference is not the
referenced data.

## 2. Stable identity keys versus mutable content (G4-A)

Identity keys **exclude** state/value content. State/value are checked content.

| Family | Stable identity key | Mutable content checked for conflict |
|---|---|---|
| `RespondentEvent` | `(universe_ref, respondent_ref, native_question_ref, canonical_question_ref_or_absence, component_ref_or_absence, event_group_id, response_event_id_or_deterministic_index, response_topology_ref, multiplicity_order_rank_fields)` | `raw_response_value`, `canonical_response_value_if_authorized`, `value_transform_authority_ref`, `response_state` |
| `RoutingEligibilityFact` | `(universe_ref, respondent_ref, question_or_target_ref, risk_set_ref, routing_rule_ref)` | `applicability_state`, `routing_state`, `parent_predicate_refs`, `member_set_replay_ref` |
| `EmpiricalCoordinateFact` | `(universe_ref, respondent_ref, native_coordinate_ref, canonical_coordinate_ref_or_absence, effective_or_reference_time)` | raw/canonical value, unit/taxonomy, `coordinate_state`, normalization authority |
| `WeightMeasureFact` | `(universe_ref, respondent_ref, weight_basis_id, effective_scope_ref, weight_source_ref, design_authority_ref, estimand_authority_ref)` | exact weight representation, `weight_state`, normalization rule |
| `QuestionVariableBinding` | `(universe_ref, native_question_ref, instrument_question_version, canonical/component ref or absence)` | semantic/topology authority, option/form external ref |
| `RespondentIdentity` | `(universe_ref, respondent_key)` | native-key ref/absence, identity-map authority |
| `EmpiricalFact` | `(query_ref, universe_refs, target_topology, condition_predicate_ref, risk_set_ref, measure_basis_ref, response_state_semantics_ref)` | numerator/denominator support, weighted support, provenance, replay, typed state |

**Conflict rule:** two records with the same stable identity but differing
checked content → `TYPED_IDENTITY_CONTENT_CONFLICT` refusal unless an exact
declared version/authority distinguishes them. State cannot make a
contradiction into two valid records.

**Legitimate distinctions:**
- repeated/ranked events differ by `event_group_id`/`response_event_id_or_
  deterministic_index`/`response_topology_ref`/`multiplicity_order_rank_fields`;
- different weight basis/effective scope/design/estimand authority is a
  different weight identity;
- different coordinate time is a different coordinate identity;
- different risk set or routing rule is a different routing identity;
- duplicate physical refs with identical identity/content are duplicate rows
  and must be refused, not counted twice.

## 3. Full exact membership (G4-B)

`_build_fact` sets `risk_set_member_refs=evaluation.risk_members` and
`denominator_member_refs=evaluation.denominator_members` (lines 986/987).
These are full exact ordered member refs, not counts.

`SelectionMembership` **must** carry:
- `candidate_member_refs`: exact ordered `ExactRef` stream for the selected
  population;
- `risk_member_refs`: exact ordered refs for the risk population;
- `denominator_member_refs`: exact ordered refs for the denominator population;
- nonselected eligible/answered/weighted state refs/members where the native
  fact requires them;
- counts only as diagnostics.

**Ordering/materialization:** use the exact `_ReleaseIndex` population order
(`native_verified_physical_respondent_order` where applicable); member refs are
the same exact `ExactRef` identities the evaluator would append. Hash/bind the
membership stream to release/universe/query/predicate/risk/measure/authority/
current. Replay re-derives the same refs; counts never construct facts.

**Baseline:** the current full `_ReleaseIndex` route always preserves full
membership and remains valid. A compact membership sidecar is a **proposed,
owner-qualified** option; it cannot exclude needed risk members to save space.
A selected target page may be read selectively, but risk/denominator/routing/
weight population validation and member-ref materialization remain full unless
a qualified exact index proves otherwise.

## 4. Cost accounting (G4-C)

Separate:
- **selected page cost** — selected event/coordinate body bytes;
- **full population validation** — all `R` respondents, routing/eligibility,
  weights, condition/predicate evaluation;
- **full risk/denominator membership** — exact member refs for every included
  respondent;
- **index/refs/output** — `_ReleaseIndex` population, member-ref
  serialization, fact/replay output.

The baseline is `O(R)` population/routing/weight work per operation plus member
refs and output; selected pages do not remove that. A compact index/sidecar may
reduce repeated scan only if it preserves exact full membership and passes
binding/invalidation. **No bounded-RAM or Q-reduction claim** for full-domain
facts before measurement; materializing v1 full risk refs/output may dominate
RSS/O. The 6 GiB guarantee remains unproven.

## 5. ExternalSourceArtifact contract (G2)

Proposed versioned external metadata object; **not** a new canonical C11 family
and not an implemented resolver.

| Field | Requirement |
|---|---|
| `artifact_kind` | `QUESTIONNAIRE`, `CODEBOOK`, `FORM_BALLOT`, `DESIGN_WEIGHT`, `DESIGN_VARIANCE`, `HOUSEHOLD_ROSTER`, `NUMERIC_UNCERTAINTY`, other exact enum |
| `artifact_ref` | proposed versioned exact ref kind/content hash; not a claimed accepted C11/ExactRef authority |
| `bytes_digest` / `version` | exact content hash/version |
| `source_lineage` | source identity, edition, file/member, retrieval authority/receipt |
| `instrument` / `wave` / `country` / `language` | exact scope |
| `native_question_ref` / `instrument_question_version` | exact join key |
| `form` / `ballot` / option content | external bytes or typed absent |
| `design_scope` | weight/design/PSU/strata/replicate/variance scope |
| permission/current issuer | exact rights/current/revocation |
| lookup request | `(native_question_ref, instrument_question_version, source_lineage, artifact_kind, scope)` |
| response/receipt/replay | exact artifact bytes/ref + receipt + replay; no implicit recovery of unrecorded data |
| ambiguity/refusal | multiple matching artifacts without version/authority → refuse; unreleased/rights-held/noncomparable → typed state |

**Mapping examples:** original-language option text → `QUESTIONNAIRE`/
`CODEBOOK`; form/ballot → `FORM_BALLOT`; PSU/strata/replicate/variance →
`DESIGN_WEIGHT`/`DESIGN_VARIANCE`; numeric interval → `NUMERIC_UNCERTAINTY`;
household/roster → `HOUSEHOLD_ROSTER` only if a source-specific released
projection exists, else typed absent.

**Existing producer/registry:** none found for this general external artifact in
the inspected product cut. Status `PROPOSED_OWNER_ROUTE`; no false claim that a
`native_question_ref` recovers option text.

## 6. FF01-2 versus FF01-k (G1)

### 6.1 FF01-2 — existing exact count profile

`ExactConditionalSupportProfile` (product `cea2d4d`):
- fixed `Q86B` conditioner → `Q86A` target;
- `participant_cardinality=2`, target arity 2, `SEMANTIC_ORDERED`;
- conditional **count** profile only; no ratio calculation;
- producer fact/query/risk/universe/permission/replay refs;
- `IMPLEMENTED_NARROW` sourcefree; no k>2/reverse.

### 6.2 FF01-k — proposed versioned derived product

`FF01KProduct` (proposed; not an accepted code object/ref authority):

| Field | Exact role/type |
|---|---|
| `product_version` | `FF01_K_PROPOSED@1.0.0` |
| `release_ref` / `universe_ref` / `time_scope_ref` | exact producer scope |
| `population_ref` | eligible/asked/observed population identity |
| `direction` | `FORWARD` (`P(Y|D)`) or `REVERSE` (`P(D|Y)`) |
| `conditioner_roles` | ordered tuple of `(role_id, source_native_ref, component_ref, domain_ref)` |
| `target_roles` | ordered tuple `k>=2` of same |
| `role_order` | exact ordered role IDs; no set comparison |
| `condition_predicate_ref` / `risk_set_ref` | exact forward or reverse condition/risk |
| `measure_basis_ref` / `weight_basis_id` / `effective_scope_ref` | exact measure/weight/scope |
| `numerator_support` / `denominator_support` | exact native fact supports for this direction |
| `weighted_numerator_if_authorized` / `weighted_denominator_if_authorized` | exact if issued |
| `coverage` | full domain, observed support, minority/remainder/tail |
| `typed_states` | `ZERO_SUPPORT`, `OBSERVED_ZERO`, `ZERO_OVERLAP`, `LOW_SUPPORT`, `NOT_ASKED`, `ROUTING_UNKNOWN`, `UNKNOWN`, `REFUSED`, `INAPPLICABLE` |
| `producer_fact_ref` / `producer_query_ref` / `producer_replay_ref` | exact native inputs |
| `permission_ceiling` / `receipt_ref` / `replay_ref` | no widening; exact receipt/replay |
| `first_consumer` | FF01 science owner/prospective FF-N9 reader; explicit hold |

**Rules:** forward/reverse use different risk/denominator bases; ratios require
an owner-issued method and positive exact denominator; weighted estimand is
owner-held; k≥3 must come from a native exact joint fact, not GT2 widening; no
new metric/science authority. Consumer distinguishes count profile (no ratio)
from distribution/ratio (owner-held).

## 7. Research citations

- Identity vs state contradiction: `R3-RES-028`.
- Full membership: `R3-RES-029`.
- Full cost accounting: `R3-RES-030`.
- External artifact contract: `R3-RES-031`.
- FF01-k contract: `R3-RES-032`.
- C11/external field map: `R3-RES-024`; adapter keys: `R3-RES-025`; F6 external
  inputs: `R3-RES-026`.

## 8. Remaining real holds

External artifact producer/registry/rights; FF01-k method/eligibility/ratio/
weighted estimand and implementation; exact compact membership index; full
H/S/Q/O measurement; source/actor/science/native rights; 100k/6 GiB/1–10–100.
