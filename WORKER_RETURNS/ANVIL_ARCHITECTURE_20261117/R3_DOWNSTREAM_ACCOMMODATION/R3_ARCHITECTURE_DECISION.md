# R3 ARCHITECTURE DECISION — corrected downstream accommodation

**Status:** `AUTHOR_CONDITIONAL_ACCOMMODATION_CANDIDATE_G1_G5_CORRECTED_PENDING_SAME_C`.
**Branch:** `agent/anvil-r3-downstream-accommodation-20261117-r1`.
**Predecessor:** `c548ef10bc2276cbe6016a53b8a39b9728cbc922` (preserved).
**Inherited candidate:** `06e88a5ac7e4c14362a97a046f44e25d8eec4162`.
**Prior R2 C:** `d109ffa9fa8d88f60b6d8c11f3885428555c7bcd` (scoped direction only).
**R3 focused C:** `e4cda70a66af241297c230362a61b03e77bb13bc` (`REVISE_EXACT_CONSEQUENTIAL_GAP`).
**Product cut:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`.
**Protected currentness observed:** `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e`, paired rev11, read-only.
**No** product code, native/100k, raw source, source/science/actor grant,
protected adoption or H1.

## 0. What this correction changes

C found five exact consequential gaps. This version does not defend the old
wording:

- **G1:** The existing `ExactConditionalSupportProfile` is a fixed **Q86B→Q86A,
  two-participant, count-only** relation. It is **not** a k>2 or reverse
  distribution. Split `FF01-2` (existing exact count profile) from a proposed
  versioned `FF01-k` derived-product contract. [R3-RES-023]
- **G2:** C11 does **not** itself persist original-language option/form/ballot
  content, household/roster namespace, PSU/strata/replicate weights/design
  variance or numeric uncertainty. Add an exact field map: C11 exact field,
  external source/codebook artifact, or typed absent/hold. [R3-RES-024]
- **G3:** Add `research_refs` to capability rows and explicit R3-RES citations
  in the decision/falsifiers. The ledger is not parallel decoration. [R3-RES-027]
- **G4:** Supply exact per-family key/ref/binding map and a concrete native-
  evaluator adapter contract; grade the typed views `CONDITIONAL_EXTENSION`,
  not already accommodated. [R3-RES-025]
- **G5:** State explicitly that PSU/strata/replicate weights/design variance and
  numeric uncertainty are external F6 inputs or typed absent, not in
  `WeightMeasureFact`/`EmpiricalFact`. [R3-RES-026]

The canonical 13-family body, prepared-first, conditional Q2/full proof with
second-certificate fallback, recovery repair and durable-index hold are
unchanged.

## 1. Selected direction

**Retain the 13-family canonical body. Amend the access/derivation
architecture with an explicit, versioned, conditional derived-access contract.**

The contract has three parts:

1. **Respondent-major event/material view** — exact events, occurrences,
   routing, coordinates, weights and universe refs keyed by exact family fields.
2. **Question-major selector/denominator view** — exact question/version,
   routing/risk, weights/design refs and direction-specific condition/target
   memberships.
3. **Derived-product manifests** — content-addressed products for F1–F4,
   F6/F7 owner products, FF01-2/FF01-k, FF02/N9/N10E/N10W/PRE-V3/SEAM/SOROK,
   each with exact input refs, method/authority, typed states, negative,
   replay, owner and invalidation.

The existing native `execute_empirical_query` / `execute_exact_bounded_discovery`
remain the scientific authority. The views are **candidate/selection and
exact-object access**; they do not replace the evaluator, denominator logic or
fact/replay output.

## 2. Five grades used

| Grade | Meaning |
|---|---|
| `PRESERVED_BYTES` | exact source/body/ref/state bytes remain in C11 or an immutable source artifact |
| `NOT_PRECLUDED` | no current field/contract forbids a future authorized computation |
| `CONCEPTUALLY_ACCOMMODATED` | concrete information→C11/external→access→derived-product→consumer route at known maturity |
| `IMPLEMENTED_FIRST_CONSUMER` | actual code executes that route at the stated scope |
| `SCIENTIFICALLY_OR_ACTOR_AUTHORIZED` | separate owner issuance; never inferred |

`OWNER_HELD` is only for genuinely unissued science/source/actor authority. It
does not hide an access/derivation decision.

## 3. R3-DERIVED-ACCESS — exact contract

### 3.1 Family keys and exact refs

The exact per-family key/ref/binding map and adapter are in
`R3_FIELD_AND_ADAPTER_CONTRACT.md`. Summary:

- **EmpiricalUniverse**: exact `ref`; `raw_source_identity`, `source_family`,
  `study_product_release`, `instrument_release`, `country_geography`,
  `sampling_geography`, `raw_wave`, `canonical_wave_if_governed`,
  `field_or_reference_time`, `target_population_and_sample_frame`,
  `sampling_design_regime`, `respondent_namespace`,
  `source_artifact_import_lineage`, `harmonization_authority_ref`,
  `source_relation_refs`.
- **RespondentIdentity**: `(universe_ref, respondent_key)` with
  `source_native_respondent_key_ref_or_typed_absence`,
  `identity_map_authority_ref_or_typed_absence`.
- **QuestionVariableBinding**: `(universe_ref, native_question_ref,
  instrument_question_version, canonical/component ref or typed absence)`;
  semantic/topology authority refs. No option/form/ballot content.
- **RespondentEvent**: stable identity `(universe_ref, scoped_respondent_ref,
  native_question_ref, canonical/component refs, event_group_id,
  response_event_id_or_deterministic_index, response_topology_ref,
  multiplicity_order_rank_fields)`; **state/value are checked content**, not
  identity.
- **RoutingEligibilityFact**: stable identity `(universe_ref, respondent_ref,
  question_or_target_ref, risk_set_ref, routing_rule_ref)`; state/parents/
  member-set replay are checked content.
- **EmpiricalCoordinateFact**: stable identity `(universe_ref, respondent_ref,
  native_coordinate_ref, canonical_coordinate_ref_if_authorized,
  effective_or_reference_time)`; value/unit/state/normalization are content.
- **WeightMeasureFact**: stable identity `(universe_ref, respondent_ref,
  weight_basis_id, effective_scope_ref, weight_source_ref, design_authority_ref,
  estimand_authority_ref)`; exact value/state/normalization rule are content.
- **EmpiricalFact**: exact `ref`; query/condition/risk/measure refs, universe
  refs, raw/weighted support, typed uncertainty method/state, provenance,
  replay. No numeric variance/interval field.

**Conflict rule:** same stable identity with differing checked content →
`TYPED_IDENTITY_CONTENT_CONFLICT` refusal unless an exact declared
version/authority distinguishes it. State cannot make a contradiction into two
valid records. Legitimate repeated events differ by event group/id/topology;
different weight basis/scope/design/estimand authority, coordinate time, or
routing rule/risk set are legitimate distinct identities. Duplicate physical
refs with identical identity/content are duplicate rows and refuse.

**External route:** original-language option/form/ballot, household/roster,
PSU/strata/replicate weights/design variance and numeric uncertainty resolve
through the proposed `ExternalSourceArtifact` contract by exact native/
instrument/source-lineage identity, or typed absent/RIGHTS_HELD. A reference is
not the referenced data. [R3-RES-024/031]

### 3.2 Native-evaluator adapter

The existing accepted route is `DirectEstateI03Session.indices_for` returning
`_ReleaseIndex` with `release`, `universe`, `respondents`,
`events_by_respondent`, `coordinates_by_respondent`, `routing_by_respondent`,
`weights_by_respondent`, `source_relations` and
`native_verified_physical_respondent_order`. `execute_empirical_query` accepts
`C11Repository` or exact `DirectEstateI03Session`; group scope is refused for
the cold sourcefree session.

The proposed extension is a **read-only adapter** that either:

- materializes the exact existing `_ReleaseIndex` from the typed views and
  presents it through an owner-qualified exact session type; or
- adds a narrow owner-approved protocol branch accepting an exact
  `R3DerivedReadView` whose `indices_for(query, release_refs)` returns the same
  exact `_ReleaseIndex` and whose `_live()`/current checks are equivalent.

**Status:** `CONDITIONAL_EXTENSION`; not implemented. It must yield exact
`RespondentIdentity`/`RespondentEvent`/`RoutingEligibilityFact`/
`EmpiricalCoordinateFact`/`WeightMeasureFact` objects/refs, not a new fact
format. The adapter must expose the full risk population and nonselected
members; it may not pre-decide denominator or fact identity. The native
evaluator remains the authority.

### 3.3 Reusable selection membership

A reusable selection/membership object is keyed by:
`(release_ref, universe_ref, condition_predicate_ref, risk_set_ref,
ordered target_refs, direction/role, routing state set, weight_basis_id,
measure_basis_ref, source_scope)`.

It may be shared across different operations only when that whole identity is
identical. It stores exact ordered **candidate, risk and denominator member
refs** plus nonselected eligible/answered/weighted typed states; counts are
diagnostic only. It never substitutes for `_build_fact`’s
`risk_set_member_refs=evaluation.risk_members` /
`denominator_member_refs=evaluation.denominator_members` (lines 986/987).
Invalidation is on source/release/frame/current/revocation change. The baseline
full `_ReleaseIndex` always preserves exact membership; a compact exact
membership sidecar is proposed/owner-qualified. Selected event-page reads do not
remove full universe/routing/weight/denominator validation or member-ref
materialization. No bounded-RAM or Q-reduction claim before measurement;
v1 full risk refs/output may dominate RSS/O and 6 GiB remains unproven.
[R3-RES-029/030]

## 4. Strongest-alternative court

- **Prepared-session-first only:** retained as the first step; insufficient for
  fresh-open S, full Q/O and explicit downstream access.
- **Demand-driven typed access + derived products:** selected access
  architecture, but the typed view itself is `CONDITIONAL_EXTENSION` until the
  exact adapter/one-build proof exists. [R3-RES-025]
- **Compact durable/secondary access:** genuinely competitive and held; only
  route to remove fresh-open S, but 1.30 GB cited retained cost and
  invalidation/rebuild economics are unproven. [R3-RES-014]
- **New primary DB / full object graph / precompute-all:** rejected; new
  body/authority surface, duplication, staleness or cost.

## 5. Six capability envelopes — corrected claims

### 5.1 Source observability and native meaning — `CONCEPTUALLY_ACCOMMODATED`

C11 preserves exact native question **refs**, instrument version, routing
state/refs, raw/canonical values, respondent namespace, occurrence/repeat,
weights/design authority refs, source/time/authority. It does **not** itself
carry original-language option/form/ballot content, household/roster namespace,
PSU/strata/replicate weights/design variance or numeric uncertainty. Those are
resolved through the proposed `ExternalSourceArtifact` contract (kind/ref/
bytes/version/source-lineage/instrument/wave/country/language/native-question-
version/form/ballot/design-scope/permission/current/lookup/receipt/replay,
ambiguity/refusal) or typed absent/RIGHTS_HELD. No existing general resolver was
found in the inspected product; this is `PROPOSED_OWNER_ROUTE`, not a recovered
datum. [R3-RES-024/031]

Observability classes remain `OBSERVED_RESPONDENT`, `SAMPLE_DESIGN_ONLY`,
`COLLECTED_BUT_NOT_RELEASED`, `EXTERNAL_GROUP_CONTEXT`, `PROXY_OBSERVED`,
`MEASUREMENT_NONCOMPARABLE`, `RIGHTS_HELD`. A stratum is not an individual
sect/ancestry. [R3-RES-005]

### 5.2 Respondent-coherent DDM, F1–F4, I03/I05 — `CONCEPTUALLY_ACCOMMODATED` (native route) + `CONDITIONAL_EXTENSION` (typed view)

Native `execute_empirical_query`, `execute_exact_bounded_discovery` and
`AnalyticalCompositionResult` preserve true same-person k≥3, F2 direction-
specific bases, F3 minority/recursive and occurrence/repeat. The typed views
must supply exact candidate streams through the adapter in §3.2; without that,
the view is conditional. Pairwise substitution is refused. [R3-RES-001/
002/003/004/021/025]

### 5.3 F6/F7 numerical and historical comparison — `EXTERNAL_OWNER_HELD`

C11 preserves separate releases/universes/waves/time/instrument/design
authority refs and source relations. It does **not** contain F6 numeric
intervals, uncovered mass, PSU/strata/replicate weights, design variance or a
numeric uncertainty interval. `EmpiricalFact.uncertainty_method_or_typed_state`
is a method/state, not a variance. F6/F7 are separate owner-held derived
products; no pooling, fake longitudinal person or I07-as-numeric substitution.
[R3-RES-006/007/026]

### 5.4 FF01 and Field Forge — `FF01-2 IMPLEMENTED_NARROW`, `FF01-k CONDITIONAL_EXTENSION`

**FF01-2:** the existing `ExactConditionalSupportProfile` is a fixed
**two-target Q86B→Q86A** count relation (`participant_cardinality=2`) and
explicitly does not calculate ratios. It is an exact count profile, not a
general conditional distribution. [R3-RES-023]

**FF01-k (proposed, not implemented):** a versioned derived-product contract
for ordered k≥2 conditioner/target roles and a separate reverse direction. The
exact field/receipt/consumer schema is in `R3_FIELD_AND_ADAPTER_CONTRACT.md` §6
(`FF01KProduct`). Summary:
- exact keys: release/universe/time/population/conditioner roles/target
  roles/order/risk-set/measure/direction;
- direction-specific numerator/denominator/routing/weights/coverage/zero/
  unknown/refused/inapplicable states;
- producer inputs: exact native I03/F1–F4 facts; no ratio unless the existing
  native qualified fact and owner permission support it;
- relation permission ceiling cannot widen producer;
- first consumer: FF01 science owner / prospective FF/N9 reader, exact hold;
- method/eligibility/ratio/weighted-estimand issuance remains `OWNER_HELD`.
No new metric/science authority is created.

### 5.5 FF02/material power, N9/N10E/N10W, PRE-V3, SEAM/SOROK — `OWNER_HELD` with nonpreclusion

C11 supplies exact source facts, positions, time, occurrence and universe
relations. FF02 must add independent institutional/legal/economic power;
N9/N10W add separately issued world possibility; SEAM adds encounter/access;
SOROK owns actor-specific access/interpretation/identification/action.
Availability ≠ access ≠ comprehension ≠ identification ≠ action. No invented
power, contact probability, psyche or longitudinal person. [R3-RES-008/009/
010/022]

### 5.6 Construction, query and evidence economics — retained/conditional/held

Prepared-first retains repeated-S removal within one process; fresh-open S, Q
and O remain. Conditional one-journal/source-derived Q2 with full physical
proof and second-certificate fallback; recovery claim/lease conditional;
durable index held. Evidence output is 30–50 MB/fact at 100k before provenance;
100 facts is 3–5 GB. Exact set-ref sharing only under identical identity;
replay re-executes. [R3-RES-002/013/014/015/016/020]

## 6. K1-CAP-08/17/23/27 — corrected specific routes

- **K1-CAP-08 signed neutral/nonneutral:** source value/role/authority and
  structural admission exist; signed/nonneutral meaning is **not** a standalone
  canonical field. FF02 owner issues sign/power; neutral0 is not missing,
  nonneutral is not causal power. `CONCEPTUALLY_ACCOMMODATED at admission;
  FF02 OWNER_HELD`. [R3-RES-012]
- **K1-CAP-17 F6 numeric:** no dedicated F6 numeric C11 family/method; I07/I04
  is structural admission, effective-N is F018. C11 preserves source/frame/
  design/weight authority material; F6 interval/uncovered mass are external
  owner-held derived products. [R3-RES-006/026]
- **K1-CAP-23 N9 vs SOROK:** `run_progressive_chain` /
  `provide_empirical_possibility_slice` produce world/possibility material;
  `HistoricalWorld` is separate actor. Route conceptually accommodated; actual
  N9/SOROK first reader owner-held. [R3-RES-010]
- **K1-CAP-27 J→FF:** `j_component_certification_validator` + J role/component
  objects + `build_m1_bundle_from_m01`/`adapt_m1_disposition_to_m2` provide a
  scoped manifest path; selected J→FF first reader and certification remain
  owner-held. [R3-RES-011]

## 7. Dispositions

- **RETAIN** 13-family canonical body, prepared-first, conditional Q2/full
  proof/fallback, conditional recovery.
- **MODIFY** access/derivation: typed views are `CONDITIONAL_EXTENSION` pending
  exact adapter; derived products are versioned/owner-held.
- **HOLD** durable index, F6 numeric, F7 comparability, FF02/N9/N10W/PRE-V3/
  SEAM/SOROK, F26, native/source/science/actor rights, 100k/6 GiB/1–10–100.
- **PROPOSED_NOT_WIRED** Batch prepared path.

## 8. Terminal statement

At present conceptual maturity, the R3 package demonstrates a credible
**information-preservation and derived-access design** for the six envelopes,
with exact C11/external/hold field boundaries, direction-specific semantics and
owner routes. It does **not** demonstrate a complete implemented first consumer
for FF01-k, F6/F7, FF02/N9/N10W/SEAM/SOROK, typed-view Q reduction, native
100k/6 GiB/1–10–100 or source/actor/science authorization. Those are precise
remaining gaps, not hidden under a generic hold.


## 9. Exact research citation index

The following R3-RES entries are relied upon by this decision:

| Decision section | Research IDs | Use |
|---|---|---|
| §3/§5.2 native F1-F4 and typed view | R3-RES-001, R3-RES-002, R3-RES-003, R3-RES-004, R3-RES-021, R3-RES-025 | storage/access distinction; prepared S only; true joint; F2 denominators; conditional typed view |
| §5.1 source observability | R3-RES-005, R3-RES-024 | observability classes; exact C11/external/absent field map |
| §5.3 F6/F7 | R3-RES-006, R3-RES-007, R3-RES-026 | numeric vs guard; crosswave comparability; PSU/strata/variance external |
| §5.4 FF01 | R3-RES-008, R3-RES-023 | FF01/FF02 firewall; FF01-2 vs FF01-k correction |
| §5.5 FF02/N9/SOROK | R3-RES-008, R3-RES-009, R3-RES-010, R3-RES-022 | power/encounter/actor boundaries; documentary status |
| §5.6 construction/economics | R3-RES-002, R3-RES-013, R3-RES-014, R3-RES-015, R3-RES-016, R3-RES-020 | S/Q/O; Q2 source; durable index; evidence; Batch; recovery |
| §6 K1-CAP-08/17/23/27 | R3-RES-012, R3-RES-006, R3-RES-026, R3-RES-010, R3-RES-011 | signed atom; F6; design variance; N9/SOROK; J/FF |
| G3 linkage | R3-RES-027 | decision-to-ledger reverse link |
| Residual G4-A/B/C | R3-RES-028, R3-RES-029, R3-RES-030 | identity/content, full membership, full cost |
| External artifact / FF01-k | R3-RES-031, R3-RES-032 | external lookup; product contract |


## 10. Residual G4-A/B/C and G2/G1 corrections (this descendant)

This descendant corrects the same-C residuals without changing the selected
physical direction:

- **G4-A identity vs content:** stable keys exclude mutable state/value.
  Same stable identity with differing checked content →
  `TYPED_IDENTITY_CONTENT_CONFLICT` unless exact version/authority distinguishes
  it. Repeated events/weights/times/routing rules are legitimate distinct
  identities only through their actual identity fields. [R3-RES-028]
- **G4-B full membership:** `SelectionMembership` now carries exact ordered
  candidate/risk/denominator member refs and nonselected typed states; counts
  are diagnostic. The existing full `_ReleaseIndex` baseline always preserves
  membership; a compact sidecar is proposed/owner-qualified and cannot exclude
  needed risk members. v1 `risk_set_member_refs`/`denominator_member_refs`
  remain exact (lines 986/987). [R3-RES-029]
- **G4-C cost:** selected event-page reads are separate from full-universe
  routing/weight/denominator validation, membership refs and output. Remove the
  blanket bounded-RAM/Q claim; baseline is O(R) population work plus refs/output.
  v1 full risk refs/output may dominate RSS/O; 6 GiB remains unproven.
  [R3-RES-030]
- **G2 external artifact:** proposed versioned `ExternalSourceArtifact` with
  exact kind/ref/bytes/version/source-lineage/instrument/wave/country/language/
  native-question-version/form/ballot/design-scope/permission/current/lookup/
  receipt/replay and ambiguity/refusal. No general resolver found; status
  `PROPOSED_OWNER_ROUTE`, not accepted code. A ref is not the referenced data.
  [R3-RES-031]
- **G1 FF01-k:** exact `FF01KProduct` field/receipt/consumer table added in
  `R3_FIELD_AND_ADAPTER_CONTRACT.md` §6. FF01-2 remains fixed Q86B→Q86A two-
  target count/no-ratio; FF01-k is proposed/owner-held for method/eligibility/
  ratio/weighted estimand. [R3-RES-032]

The field/adapter contract now cites R3-RES-024/025/026/028–032 directly.
No new C11 body/family, product code, science/actor grant or native 100k claim.
