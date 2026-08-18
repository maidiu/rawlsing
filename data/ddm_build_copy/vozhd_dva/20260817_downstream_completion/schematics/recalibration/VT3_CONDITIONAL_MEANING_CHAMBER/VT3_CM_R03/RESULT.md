# VT3-CM-R03 — Downstream Recreation Court — Corrective Result

**Cell:** `VT3-CM-R03`  
**Repository:** `maidiu/rawlsing`  
**Frozen source base:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Worker branch:** `agent/vozhd-trii-vt3-cm-r03`  
**Mode:** hostile semantic-equivalence / downstream-recreation court  
**Corrective pass:** `TRUE`  
**Original mission completed:** `TRUE`  
**Production code changed:** `NO`

## 0. Corrective verdict

`UNARY_NOT_FAITHFULLY_RECREATED__JOINT_NOT_FAITHFULLY_RECREATED__APPARENT_RECREATION_IS_METADATA_OR_LOSSY_DERIVATION__MICRODATA_RECOMPUTATION_REQUIRED_WHEN_EXACT_OBJECT_NOT_RETAINED__DIRECT_DAG_IS_TRANSPORT_NOT_REPAIR`

The hostile hypothesis was:

> Perhaps V550 position-conditioned empirical meaning is recreated, reconstructed, regenerated, approximated, or substituted downstream.

The hypothesis fails as a claim of **faithful downstream recreation**.

At the frozen base, V550 contains an actual respondent-derived unary condition-response surface in `indicator_answer_matrix`: for a source/wave/geography/question and exact indicator value, it emits response-cell unweighted and weighted counts and shares. That is the closest concrete implementation of:

`P(response = r | exact observed conditioning predicate, source, wave/time, geography)`.

The canonical V551 signed-atom path does not admit that surface. The alternate `ddm_v551_conditional.py` path consumes derived-determinicity rows but drops the explicit conditioning predicate identity from its emitted semantic row/ID. V552 accepts a `conditional_determinicity` argument but does not use it. V552J only links packets to structural facts. V553–V558 transform, publish, index, or resolve already-authoritative structural objects; they do not estimate a missing respondent conditional. V3 generates actor positions and lived history under authorities that explicitly forbid prevalence/geography/demographic association from manufacturing missing position or psychological meaning.

Higher-order conditional meaning fails even more strongly. V550's secondary-indicator analysis computes joint conditional entropy/gain, not the full response distribution for an exact intersection `A ∧ B`. V551J creates joint evidence packets/pattern objects of a different semantic grain; it does not reconstruct `P(response | A ∧ B)` from structural-position predicates. No later stage restores the missing joint response topology, denominators, counts, support, typed absence and provenance.

Exact recovery has only two lawful routes:

1. **EXACT_DIRECT_REUSE** of the exact original authoritative conditional object, if it is preserved, admitted, published, reachable and permissioned; or
2. **POTENTIALLY_RECOMPUTABLE_FROM_RETAINED_MICRODATA** by returning to respondent-grain rows that still jointly retain the exact conditioning variable(s), response, respondent alignment, weights, source/wave/geography and semantic/provenance authority, then compiling a new governed conditional object.

Accepted 553+ direct-DAG law supplies route (1) as a transport/reuse possibility. It does not create the object, does not fill a missing predicate, and does not turn metadata into a conditional distribution.

---

## 1. Required self-correction

The prior R03 pass answered a broader and useful question: which downstream artifact families are execution-critical, adjudication-critical, forensic, duplicate, or superseded. That work remains supporting evidence in four respects:

1. it correctly identified direct-DAG reuse as distinct from serial republishing;
2. it correctly identified producer identity, permission/negative authority, provenance and reference closure as non-negotiable;
3. it correctly identified V557/V558 as a producer-preserving publication/resolver boundary rather than a semantic recreation engine;
4. it correctly warned that current artifact existence is not proof of terminal authority.

But it did **not** complete the assigned hostile recreation mission. Specifically, it had not answered:

- whether an actual V550 `P(response | position)` survives/reappears in V551;
- whether `ddm_v551_conditional.py` is semantically equivalent to the V550 conditional object;
- whether V551J reconstructs unary or intersectional position-response distributions;
- whether V552 actually consumes its optional conditional-determinicity input;
- whether `position_conditioning_profile` preserves the original empirical response distribution;
- whether V553+ direct reuse means the required conditional object is actually present and reachable;
- whether V3 generated positions can lawfully substitute for missing empirical conditionals;
- the required unary and `A ∧ B` indistinguishability tests.

This corrective pass answers those questions directly. The former A/B/C/D artifact-consumption classification is no longer the primary verdict system for R03; the required recreation classes below are.

---

## 2. Canonical semantic test object

For this court, a faithful unary empirical conditional must preserve enough exact authority to distinguish:

```text
ConditionalResponseDistribution {
  condition_predicate_identity:
    exact field / exact value / exact governed predicate,
  source,
  wave_or_time,
  geography,
  question_or_response_semantic_identity,
  response_topology[],
  response_cells[] {
    response_value,
    n_unweighted,
    n_weighted,
    pct_unweighted,
    pct_weighted
  },
  denominator_unweighted,
  denominator_weighted_or_weight_status,
  support_and_uncertainty_state,
  typed_absence_or_missing_state,
  provenance_and_authority_refs
}
```

An exact intersectional conditional additionally requires a canonical conjunction identity such as:

`condition_predicate = A ∧ B`

with the same response topology/count/support/provenance obligations.

Similar vocabulary is not equivalence. In particular:

- `position_conditioning = "income"` is not `P(response | income=low)`;
- `position_field = "income_level"` without a response distribution is not a conditional;
- a pressure score grouped by `position_conditioning` is not a respondent distribution;
- a V3 generated actor position is not survey evidence about respondents occupying that position;
- a V551J joint response pattern is not automatically a structural-position intersection.

---

## 3. V550 source object and loss baseline

### 3.1 `indicator_answer_matrix` is the concrete unary test object

Pinned implementation: `data/ddm_build_copy/ddm_v550_branching.py`.

`indicator_answer_matrix_rows()` iterates the V550 `INDICATOR_FIELDS`, groups respondent rows by exact `indicator_value`, cross-tabulates `response_value_normalized`, and emits for each exact `(indicator_name, indicator_value, response_value)` cell:

- `n_unweighted`;
- `pct_unweighted`;
- `n_weighted`;
- `pct_weighted`.

The source/wave/country/question/semantic context enters through `question_meta` and the enclosing V550 artifact grain. The denominator for a given condition is the corresponding row-total across the response topology; weighted denominator is the weighted row-total when weights are available.

This is not merely dependence metadata. It distinguishes different empirical distributions for the same position predicate.

**Classification relative to downstream:** the V550 object itself can only be `EXACT_DIRECT_REUSE`; it is not a downstream recreation.

### 3.2 `position_distribution` is not the conditional

Pinned implementation: `ddm_v550_position_distribution.py`.

It emits marginal position-coordinate counts/shares by `(position_field, position_value)`:

`P(position=value | source,wave,country)`.

It does not cross the position value with response topology.

**Class:** `DIFFERENT_SEMANTIC_OBJECT`.

### 3.3 Indicator and secondary summaries are insufficient substitutes

`indicator_summary_rows()` emits entropy, mutual information, Cramer's V, uplift, dominant-response summaries and support. Those can demonstrate association but do not retain all condition-value × response cells.

`secondary_indicator_summary_rows()` forms a joint key from a primary and secondary indicator and calculates joint conditional entropy / `secondary_gain`, but emits summary statistics rather than the full distribution `P(Y | A=a ∧ B=b)` for each exact joint predicate and response category.

**Unary summary class:** `LOSSY_APPROXIMATION`.  
**Intersection summary class:** `LOSSY_APPROXIMATION`.

A scalar entropy reduction cannot identify the original response topology.

---

## 4. V550 → V551 bridge

Pinned bridge implementation assigns the relevant source tables to distinct evidence lanes:

- `answer_distribution` / `country_answer_distribution` → `direct_relation_response`;
- `indicator_answer_matrix`, `outlier_cohort_summary`, `recursive_branch_nodes`, `secondary_indicator_summary` → `derived_determinicity`;
- `position_distribution`, `position_indicator_summary`, `branch_position_signature` → `position_context`.

Bridge rows may also carry fields such as:

- `position_conditioning`;
- `position_modifiers`;
- `conditional_strata_weights`;
- `subject_position_signature`;
- structural relation/target/driver metadata.

Those fields describe semantic/contextual conditions or intended use. They do not, by themselves, preserve respondent conditional response topology.

**Class for those fields:** `METADATA_ONLY`.

---

## 5. V551 canonical signed-atom path

Pinned implementation: `ddm_v551_atoms.py`.

### 5.1 Gate that matters

The canonical compiler declares:

```text
APPROVED_DIRECT_TABLES = {
  "answer_distribution",
  "country_answer_distribution"
}
```

and its certification candidate bridge requires simultaneously:

- `bridge_evidence_lane == "direct_relation_response"`;
- `source_table ∈ APPROVED_DIRECT_TABLES`;
- substantive/nonmissing/nonspecial response;
- certified applicability/semantic authority.

V550 `indicator_answer_matrix` is routed as `derived_determinicity`, not `direct_relation_response`. Therefore its dedicated position-conditioned response rows are not admitted into the canonical V551 signed-atom path.

### 5.2 Why similar V551 fields do not repair this

The V551 atom schema contains fields including:

- `position_field`;
- `position_value`;
- `strata_path`;
- `subject_position_signature`;
- `position_conditioning`;
- `position_modifiers`;
- `conditional_strata_weights`;
- response counts/shares and topology fields.

This proves the schema can *carry* position-related information. It does not prove that the V550 conditional matrix is admitted. The actual source-table/lane gate excludes the dedicated matrix.

If a future governed direct-table object already contained the exact condition predicate and distribution, a V551 atom family could preserve it. That would be preservation/direct reuse of an already-existing exact object, not recreation of the omitted IAM conditional.

**Actual frozen-path class for V550 IAM → canonical V551 atoms:** `NO_RECREATION`.

**Position vocabulary carried on canonical atoms without the omitted IAM distribution:** `METADATA_ONLY` for the missing conditional meaning.

---

## 6. V551 dormant/alternate `ddm_v551_conditional.py`

This is the strongest apparent downstream recreation candidate and therefore the central hostile test.

### 6.1 Exact input lane

`build_conditional_determinicity_index()` requires:

- `v551_conditional_determinicity_eligible == True`;
- `bridge_evidence_lane == "derived_determinicity"`;
- joined question-use contract;
- joined source-structure fields;
- `support_status == "sufficient_support"`.

Thus it can consume derived-determinicity rows including the lane in which V550 position-conditioned analysis lives.

### 6.2 What it emits

Its `_conditional_row()` preserves:

- source/wave/canonical-wave/country/question/var/source-table;
- response value/label/family/direction/intensity;
- response-semantics authority metadata;
- `n_unweighted`, `n_weighted`, `pct_unweighted`, `pct_weighted`;
- support/compiler status;
- structural relation/target/driver fields;
- `source_row_hash` and source-run provenance.

But it does **not** emit the exact observed condition identity needed by this court:

- no `position_field`;
- no `position_value`;
- no `indicator_name`;
- no `indicator_value`;
- no canonical conjunction/predicate object;
- no `position_conditioning` binding that specifies an exact value.

Its `conditional_id` hashes:

`source, wave, country_code, question_id, var_code, source_row_hash`

rather than the explicit condition predicate. Its dedupe key likewise omits the condition field/value as named semantic components.

### 6.3 Ruling

This mechanism can retain numeric measurements from a derived source row while losing the machine-readable statement **what exact respondent condition those measurements are conditional on**.

A `source_row_hash` may allow forensic dereference to the original V550 row if that original remains available. If so, exact semantics come from the original row reached by provenance — that is direct reference/reuse, not recreation by `ddm_v551_conditional.py`.

Without such dereference, the emitted row is not a self-contained exact conditional authority.

**Class:** `LOSSY_APPROXIMATION`.

It is **not** `EXACT_RECREATION`.

---

## 7. V551J

Pinned implementation: `ddm_v551j_packets.py`.

V551J assembles packet/component identities over V551 atom evidence, V550J joint response patterns, association/context rows and related structural context. Packet types include joint relation evidence, joint pattern context, conditional support, contradiction candidate and known absence.

### 7.1 Component/packet identity

V551J preserves exact input atom IDs, pattern IDs, association IDs, source artifacts/runs, question IDs, variable codes and structural/provenance references. That is valuable evidence linkage.

It does not recreate the omitted V550 structural predicate × response crosstab merely because a packet is called `conditional_support_packet`.

**Class:** `METADATA_ONLY` relative to the missing V550 position conditional.

### 7.2 Joint response patterns are a different joint object

A V550J/V551J joint response pattern represents a governed joint evidence pattern over component/question response material. It is not automatically:

`P(Y | structural_position_A ∧ structural_position_B)`.

There is no lawful equivalence from “joint packet” or “joint response pattern” to a conjunction of respondent structural-position predicates.

**Class:** `DIFFERENT_SEMANTIC_OBJECT`.

### 7.3 Higher-order position conditional

No inspected V551J mechanism reconstructs the exact intersectional response topology, weighted/unweighted condition-cell denominators, support/uncertainty and condition identity for `A ∧ B`.

**Class:** `NO_RECREATION`.

---

## 8. V552

Pinned implementation: `ddm_v552_structural.py`.

### 8.1 Canonical pressure construction

V552 consumes V551 v3 signed atoms, directional coverage and adjudication. Its canonical pressure objects are transformations of the signed response distribution into structural pressure components/observations and rollups.

These preserve different meaning:

- structural pressure value/status;
- structural identity;
- signed component lineage;
- selected-surface completeness;
- measurement provenance.

They are not respondent conditional response distributions.

**Class:** `DIFFERENT_SEMANTIC_OBJECT`.

### 8.2 The optional conditional input is actually unused

The exact function signature is:

```text
build_v552_structural_outputs(
  atoms,
  directional_coverage=None,
  directional_adjudication=None,
  conditional_determinicity=None,
  *, run_id=...
)
```

Inside the function, output construction uses atoms, coverage and adjudication. `conditional_determinicity` is never consumed. The output named `conditional_determinicity_status_audit` is instantiated as an empty schema surface.

Therefore two executions with identical canonical atoms/coverage/adjudication and different conditional-determinicity inputs necessarily produce the same canonical V552 semantic outputs.

**Class:** `NO_RECREATION`.

This is decisive against the claim that the V551 alternate conditional lane is silently folded into structural pressure downstream.

### 8.3 `position_conditioning_profile`

`build_position_conditioning_profile_from_observations()` filters already-created V552 pressure observations on nonblank `subject_position_signature` or `position_conditioning`, then rolls those **pressure observations** up by:

`source, wave, canonical_wave, country_code, subject_position_signature, position_conditioning`.

It does not return the original response categories and condition-cell counts.

**Class:** `LOSSY_APPROXIMATION` for any attempt to use it as a proxy for the empirical conditional.

The presence of the word `position_conditioning` is not equivalence.

---

## 9. V552J

V552J owns packet↔structural-fact association, exact-scope admission/use permission, blockers, readiness and lineage. Its job is to establish which already-created packet/fact objects may lawfully associate and move forward.

It does not reopen respondent data, cross-tab structural positions against responses, or derive a new conditional distribution.

**Class:** `METADATA_ONLY` for the missing empirical conditional.  
**Recreation result:** `NO_RECREATION`.

---

## 10. V553

### 10.1 Current pinned implementation

The inspected V553 canonical intake discovers and harmonizes V552/V552J structural/handoff material: structural facts, packet/fact identity, temporal source identity and structural relation/target/driver/channel fields.

The current canonical path does not consume V550 `indicator_answer_matrix` or the V551 conditional-determinicity index as a conditional-response authority.

**Class:** `NO_RECREATION`.

### 10.2 Accepted V553 architecture

Accepted architecture explicitly permits later stages to directly reuse earlier governed producer objects where the earlier producer still owns the needed meaning. It also requires exact reference preservation and forbids reconstructing authority later from strings, aggregates or semantic resemblance.

That rule is crucial but limited:

```text
DIRECT_REUSE_ALLOWED
!= REQUIRED_OBJECT_EXISTS
!= REQUIRED_OBJECT_WAS_PUBLISHED
!= REQUIRED_OBJECT_IS_RUNTIME_ADMITTED
!= MISSING_OBJECT_RECREATED
```

For the canonical conditional test object, V553+ law can support `EXACT_DIRECT_REUSE` only if the exact V550/V551 conditional object is itself authoritative, retained, referenced, admitted and reachable.

The law alone is not an estimator.

---

## 11. V554

Pinned current V554 converts V553 structural material into bounded seed/affordance/applicability terrain. Accepted V554 architecture likewise owns mediation-input applicability, not survey estimation.

A structural affordance or condition may refer to a required position, temporal state or structural basis. It does not state the respondent distribution conditional on that position.

**Class:** `DIFFERENT_SEMANTIC_OBJECT`.

No exact recreation occurs.

---

## 12. V555

Pinned current V555 constructs mediation-slot/register terrain; accepted terminal V555 replaces that with exact structural mediation-route candidates and route-born conditions.

Both current and accepted meanings answer a different question: through what actor-independent structural mediation route may an already-authorized structural affordance pass?

They do not estimate `P(response | position)`.

**Class:** `DIFFERENT_SEMANTIC_OBJECT`.

No recreation occurs.

---

## 13. V556

Pinned current V556 produces pressure-flow scaffold/route-axis terrain. Accepted V556 owns governed cross-route/cross-pressure interaction relations and attractor-prerequisite topology while preserving V555 route IDs.

Interaction topology cannot recover respondent conditional distributions lost before V552. Shared source, target, sign, time, route coexistence or topology never implies a response conditional.

**Class:** `DIFFERENT_SEMANTIC_OBJECT`.

No recreation occurs.

---

## 14. V557 / V558

### 14.1 Current pinned implementations

Current V557 renderer-boundary and V558 runtime-input-gate code operate over downstream packets/readiness/governance surfaces. Neither reads respondent-grain data or reconstructs V550 condition-response distributions.

**Current implementations:** `NO_RECREATION`.

### 14.2 Accepted producer-preserving repository law

Accepted TD-R04, CAN-003 and CAN-004 establish:

- V557 does not create a structural-domain semantic family;
- V557 may admit/preserve an exact producer object under item-level governance;
- V558 links and indexes already-valid publication;
- V558 may not repair an invalid publication, infer a missing semantic dependency, replace producer identity, or widen authority;
- repository locators/indexes are administrative access paths, not new semantic objects.

CAN-004 is generic enough to package an admitted earlier producer object if governed publication supplies it. But generic packaging authority does not mean every possible V550/V551 object is automatically a runtime root or transitive dependency. The accepted terminal mixed-producer architecture explicitly centers V552 facts, V553 temporal objects, V554 affordances, V555 routes and V556 topology; the inspected chain does not establish the V550 IAM conditional as an automatically published repository collection.

Therefore:

- existing exact conditional, explicitly admitted/published/reachable → `EXACT_DIRECT_REUSE`;
- missing/unpublished conditional → `NO_RECREATION`;
- resolver query against generated position → selection of existing governed objects only, never statistical reconstruction.

---

## 15. V3 / ADP-009 / CAN-006 / ADP-010 / ADP-017

### 15.1 ADP-009 generated position is not empirical respondent meaning

Accepted ADP-009 makes the nonidentity explicit:

```text
STRUCTURAL PRIOR
!= RESOLVED STRUCTURAL CONTEXT
!= POSITION CANDIDATE
!= GENERATED ACTOR POSITION FACT
!= ACTOR KNOWLEDGE / IDENTITY / PSYCHE
```

ADP-009 forbids manufacturing actor position because it is:

- geographically plausible;
- statistically prevalent;
- demographically associated;
- convenient.

It separately forbids:

- raw structural prevalence/frequency → actor membership/probability;
- country/region → class, sect, party, occupation, institution, household, family or Self;
- demographic category → position;
- nearest/most-common/default fallback.

A governed actor-position distribution can be consumed only if a separately accepted authority explicitly supplies those candidate/weight semantics.

### 15.2 CAN-006 generated-position binding does not reconstruct a conditional

CAN-006 allows an **already-lawful generated V3 position fact** to be supplied as a Phase-B ContextResolver query binding against the same immutable repository.

The resolver evaluates already-governed predicates and may select additional existing position-conditioned structural material. It may not create or backfill the position, and it cannot manufacture a missing producer conditional.

Thus CAN-006 can enable `EXACT_DIRECT_REUSE` **only if** an authoritative position-conditioned producer object is already present in the repository.

### 15.3 Opportunity/exposure and actor knowledge are downstream life semantics

ADP-010 keeps `AVAILABLE`, `OPPORTUNITY`, `ENCOUNTER`, and `EXPOSURE` distinct and forbids resolver selection from becoming lived occurrence by itself.

ADP-017 keeps structural causation distinct from actor causal interpretation/knowledge and forbids objective structural truth from automatically becoming actor belief.

Neither mechanism is statistical evidence about upstream respondents.

### 15.4 Required ADP-009 reconstruction ruling

Attempt to infer missing `P(response | position)` from:

- generated actor position → `FORBIDDEN_RECONSTRUCTION`;
- raw prevalence → `FORBIDDEN_RECONSTRUCTION`;
- geographic plausibility → `FORBIDDEN_RECONSTRUCTION`;
- demographic association → `FORBIDDEN_RECONSTRUCTION`;
- structural metadata / resolver labels → `FORBIDDEN_RECONSTRUCTION`.

V3 is a developmental causal runtime, not an empirical survey estimator or semantic repair layer.

---

## 16. Respondent-grain recomputation court

Pinned V550 respondent-substrate code establishes a respondent-grain evidence terrain with stable source/wave/country/respondent identity, response values, weights and response semantics/provenance. V550's position computations demonstrate that respondent frames can also contain structural/demographic indicator fields.

However, the declared shared-substrate required-column contract does not itself guarantee that every V550 `INDICATOR_FIELD` survives as a published downstream microdata column. Therefore this court does not pretend that “microdata exists somewhere” equals terminal reachability.

Exact recomputation is lawful in principle only when a retained respondent-grain surface jointly preserves, for the same respondents:

- exact conditioning field(s) and values;
- response variable/value and semantic topology;
- respondent identity/alignment;
- source/wave/geography;
- weight values and weight validity state;
- missing/special-response treatment;
- provenance/authority necessary to interpret the rows.

If those survive, unary and joint conditionals are:

`POTENTIALLY_RECOMPUTABLE_FROM_RETAINED_MICRODATA`.

That is **not** the same finding as `EXACT_RECREATION`. A new governed compiler would have to compute, identify, support-gate, provenance-bind and publish the resulting conditional object.

If the exact original sufficient-stat conditional table and the needed respondent-grain conditioning variables are both lost, the downstream V551–V3 objects inspected here do not contain enough information to recover the distribution.

---

## 17. Required equivalence tests

### 17.1 Unary indistinguishability test

Construct two populations with identical source, wave, geography, question, marginal response distribution and marginal position prevalence.

Let each population have 200 respondents; 100 occupy position `P`, 100 do not. Overall response `Y=1` is 100/200 in both.

**Population U-A**

```text
P:      Y=1 90, Y=0 10
not P:  Y=1 10, Y=0 90
```

So:

`P(Y=1 | P) = 0.90`.

**Population U-B**

```text
P:      Y=1 10, Y=0 90
not P:  Y=1 90, Y=0 10
```

So:

`P(Y=1 | P) = 0.10`.

Yet both have identical:

- `P(Y=1)=0.50`;
- `P(P)=0.50`;
- source/wave/geography/question identity;
- any structural metadata that does not include the response×position crosstab.

Consequences:

- V550 `indicator_answer_matrix` necessarily distinguishes U-A and U-B.
- V550 `position_distribution` does not.
- `position_conditioning="P"` metadata alone does not.
- V552 canonical output can remain identical when canonical atom inputs are held identical because its optional conditional input is unused.
- V554–V558/V3 cannot distinguish the populations unless an exact conditional object is directly retained/reused as an explicit input.

Therefore those mechanisms are not exact recreation.

### 17.2 Intersectional indistinguishability test

Construct four equally sized `A/B` cells, 100 respondents each.

**Population J-A**

```text
A∧B:       Y=1 90, Y=0 10
A∧¬B:      Y=1 10, Y=0 90
¬A∧B:      Y=1 10, Y=0 90
¬A∧¬B:     Y=1 90, Y=0 10
```

**Population J-B**

```text
A∧B:       Y=1 10, Y=0 90
A∧¬B:      Y=1 90, Y=0 10
¬A∧B:      Y=1 90, Y=0 10
¬A∧¬B:     Y=1 10, Y=0 90
```

Both populations have:

- `P(Y=1)=0.50`;
- `P(Y=1 | A)=0.50`;
- `P(Y=1 | B)=0.50`;
- identical `A` and `B` marginals.

But:

- J-A: `P(Y=1 | A∧B)=0.90`;
- J-B: `P(Y=1 | A∧B)=0.10`.

Therefore unary conditionals cannot identify the intersectional conditional. Nor can association metadata, entropy/gain summaries, packet co-membership, generated actor positions, or structural topology.

Exact recovery requires the joint respondent crosstab (or a lossless equivalent sufficient-stat object) for `A ∧ B`.

### 17.3 Predicate-identity test for `ddm_v551_conditional.py`

Take two source rows with identical source/wave/country/question/response/count values but different exact conditioning predicates. If the emitted downstream semantic fields do not carry those predicate identities, a consumer cannot know which population slice a row describes without dereferencing external source provenance.

`ddm_v551_conditional.py` omits the explicit position/indicator predicate fields. Hence any exact interpretation depends on external recovery of the original row through `source_row_hash`; the compiler itself has not recreated the conditional semantic object.

**Result:** `LOSSY_APPROXIMATION`, with possible exact provenance dereference to the original V550 object.

---

## 18. Candidate recreation mechanism ledger

| Candidate mechanism | Required class | Court ruling |
|---|---|---|
| V550 `indicator_answer_matrix` retained/reused | `EXACT_DIRECT_REUSE` | Exact positive unary sufficient-stat surface if preserved with authority/provenance; not downstream recreation |
| V550 `position_distribution` | `DIFFERENT_SEMANTIC_OBJECT` | Marginal position distribution only |
| V550 `position_indicator_summary` | `LOSSY_APPROXIMATION` | Association/determinicity summary, not full response conditional |
| V550 `secondary_indicator_summary` | `LOSSY_APPROXIMATION` | Joint entropy/gain summary, not `P(Y|A∧B)` topology |
| V550 respondent-grain rows with aligned condition/response/weights | `POTENTIALLY_RECOMPUTABLE_FROM_RETAINED_MICRODATA` | Requires new governed recomputation; not current downstream authority |
| V551 canonical signed atoms for omitted IAM | `NO_RECREATION` | IAM is excluded by direct-table/lane gate |
| V551 `position_field/value`, `position_conditioning`, modifiers/weights/signature | `METADATA_ONLY` | Similar vocabulary does not encode conditional distribution |
| V551 `ddm_v551_conditional.py` | `LOSSY_APPROXIMATION` | Retains measurement row but drops explicit condition predicate identity |
| V551J packet/component linkage | `METADATA_ONLY` | Evidence linkage, not conditional estimation |
| V551J joint response pattern | `DIFFERENT_SEMANTIC_OBJECT` | Joint pattern ≠ structural-position conjunction conditional |
| V551J `P(Y|A∧B)` recreation | `NO_RECREATION` | No exact joint position-response distribution rebuilt |
| V552 optional `conditional_determinicity` input | `NO_RECREATION` | Function parameter is unused |
| V552 pressure components/observations | `DIFFERENT_SEMANTIC_OBJECT` | Signed structural pressure transformation |
| V552 `position_conditioning_profile` | `LOSSY_APPROXIMATION` | Rollup of pressure observations, not original response topology |
| V552J packet↔fact association | `METADATA_ONLY` | Links existing objects; no respondent recomputation |
| V553 current canonical intake | `NO_RECREATION` | Consumes V552/V552J structural material, not conditional respondents |
| Accepted V553+ direct-DAG | `EXACT_DIRECT_REUSE` conditional on object existence/admission | Transport/reuse law only; cannot recreate missing object |
| V554 affordance/applicability | `DIFFERENT_SEMANTIC_OBJECT` | Structural use possibility |
| V555 mediation route | `DIFFERENT_SEMANTIC_OBJECT` | Actor-independent route semantics |
| V556 interaction/topology | `DIFFERENT_SEMANTIC_OBJECT` | Cross-route structural topology |
| V557 current renderer boundary | `NO_RECREATION` | No conditional estimator |
| V557 accepted publication | `EXACT_DIRECT_REUSE` only for admitted existing producer object | Governance/preservation only |
| V558 current runtime gate | `NO_RECREATION` | Readiness/governance normalization only |
| V558 accepted repository/resolver | `EXACT_DIRECT_REUSE` for existing indexed object; otherwise `NO_RECREATION` | Selection/indexing cannot create missing semantics |
| V3 ADP-009 generated position | `DIFFERENT_SEMANTIC_OBJECT` | Generated actor fact, not respondent evidence |
| V3 infer conditional from generated position/prevalence/geography/demography/metadata | `FORBIDDEN_RECONSTRUCTION` | Explicit authority prohibition |
| V3 opportunity/exposure/knowledge/development | `DIFFERENT_SEMANTIC_OBJECT` | Lived causal/epistemic semantics, not survey reconstruction |

---

## 19. Direct-DAG transport versus semantic existence

This distinction is the central architecture result.

Accepted law says later stages may reach backward to an earlier producer for meaning that producer still owns. CAN-003/CAN-004 then preserve producer identity and can publish/link exact admitted objects without semantic re-ID.

But five independent conditions must hold before that becomes exact conditional reuse:

1. the exact conditional object must **exist**;
2. its condition predicate identity and response topology/count/support/provenance must be **losslessly retained**;
3. it must be within a governed producer collection/reference closure that is **published**;
4. item-level permission must permit the intended use and the repository must make it **reachable**;
5. the resolver must select it only under its already-governed predicates; it may not infer what is absent.

If condition (1) fails, direct-DAG law has nothing to transport.  
If (2) fails, a hash/prose/summary is not a semantic substitute.  
If (3) or (4) fails, theoretical earlier availability is not terminal reachability.  
If (5) fails, the resolver would be inventing authority.

Thus direct-DAG law prevents unnecessary serial copying. It does not repair upstream information loss.

---

## 20. Final required answers

### 1. Is unary V550 conditional response meaning faithfully recreated later?

**NO.**

The exact V550 `indicator_answer_matrix` can be **directly reused** if preserved and governed, but the inspected downstream V551→V558/V3 mechanisms do not faithfully recreate it after omission. Canonical V551 excludes the IAM lane; alternate V551 conditional output loses explicit predicate identity; V552 ignores that conditional input; later stages transform different semantic objects.

### 2. Is higher-order/joint conditional meaning faithfully recreated later?

**NO.**

V550 secondary-indicator analysis retains joint dependence summaries, not the full `P(response | A ∧ B)` distribution. V551J joint packets/patterns are different joint evidence objects. The intersectional equivalence fixture proves unary marginals and downstream metadata cannot recover the joint conditional.

### 3. Is any apparent recreation merely metadata?

**YES, substantial apparent recreation is metadata, and one important path is lossy derivation rather than metadata alone.**

`position_field`, `position_value`, `position_conditioning`, `position_modifiers`, `conditional_strata_weights`, `subject_position_signature`, V551J packet↔component identities, V552J packet↔fact association, and V3 generated-position bindings can preserve condition-related identity or selection context without preserving the empirical response distribution. V552 `position_conditioning_profile` is a lossy pressure rollup. `ddm_v551_conditional.py` preserves numeric derived-row measurements but loses explicit predicate identity, so it is `LOSSY_APPROXIMATION`, not merely metadata and not exact recreation.

### 4. Is any lost meaning recoverable only by returning to respondent-grain data?

**YES, when the exact original conditional sufficient-stat object is not retained.**

Recovery then requires respondent-grain evidence — or another lossless equivalent sufficient-stat table — that jointly retains exact condition variable(s), response, respondent alignment, weights, source/wave/geography and provenance. This is `POTENTIALLY_RECOMPUTABLE_FROM_RETAINED_MICRODATA`, not current downstream recreation. If neither the exact conditional table nor the required respondent-grain condition-response alignment survives, the inspected downstream objects are insufficient to reconstruct it.

### 5. Does accepted 553+ direct-DAG law solve the semantic loss automatically, or only provide a transport mechanism if an authoritative object exists?

**ONLY A TRANSPORT / DIRECT-REUSE MECHANISM IF AN AUTHORITATIVE OBJECT EXISTS.**

It does not solve semantic loss automatically. CAN-003/CAN-004 and the accepted V557/V558 architecture preserve and index producer-owned objects; they explicitly do not infer or repair missing semantic dependencies. An exact V550 conditional must first exist, remain lossless, be admitted/published and be reachable under permission. Otherwise the DAG carries nothing equivalent.

---

## 21. Final hostile ruling

The downstream system contains many objects that are **about positions**, **conditioned by structural metadata**, **joint**, **pressure-bearing**, **position-bindable**, or **resolver-selectable**. None of those labels supplies the missing empirical operation.

The exact question is whether downstream state contains enough information to distinguish two respondent populations that differ only in the conditional distribution of responses within an exact position predicate while sharing the candidate downstream marginals/metadata. For the inspected canonical path, the answer is no.

Likewise, two populations can share every unary `P(Y|A)` and `P(Y|B)` while differing radically in `P(Y|A∧B)`. No V551J packet name, V552 pressure profile, V556 topology, V558 resolver binding or V3 generated actor position closes that information-theoretic gap.

Therefore the hostile recreation hypothesis is rejected:

`V550 conditional empirical meaning is not faithfully recreated downstream.`

Where it survives exactly, it survives because the original authoritative object is **directly reused**. Where it does not survive, exact recovery requires **return to lossless respondent/sufficient-stat evidence and a governed recomputation**. Where V3 might otherwise be tempted to fill the gap from prevalence, geography, demographic association or generated position, current authority makes that reconstruction explicitly **forbidden**.