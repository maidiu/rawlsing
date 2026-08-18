# VT3-CM-R01 — Conditional-Value Archaeology Court Record

## Corrective pass

- **Cell:** `VT3-CM-R01`
- **Corrective pass:** `true`
- **Supersedes prior result:** `true`
- **Frozen source SHA:** `8c87f7725ba58202b5377c974548140420709fa9`
- **Worker branch:** `agent/vozhd-trii-vt3-cm-r01`
- **Production code changed:** `NO`
- **Corrected verdict:** `MATERIAL_SEMANTIC_LOSS_NOT_FAITHFULLY_PRESERVED`

This result supersedes the prior R01 record. The larger semantic-loss conclusion survives, but the prior result reached it through two material source-reading errors and one overstatement about recursive branch meaning. This corrective pass re-anchors the archaeology on the exact active source at the frozen SHA and does not import historical implementations into the active seam.

## Corrections to prior R01 result

### Correction 1 — `position_distribution` was misread as question-conditioned response evidence

**Prior claim:** the prior result attributed `compute_position_conditional_distributions`, question/response-bearing `POSITION_DISTRIBUTION_COLUMNS`, and position-value sample support for response distributions to active `data/ddm_build_copy/ddm_v550_position_distribution.py`.

**Why wrong:** those functions and that schema are not present in the pinned active file. The active implementation defines `build_position_distribution_rows`. It first creates a respondent slice by sorting and deduplicating respondents on available `respondent_id`/`country_code`, then emits question-independent prevalence rows over each `INDICATOR_FIELDS` position coordinate. The output columns are `position_field`, `position_value`, unweighted/weighted counts and prevalence shares plus provenance; each row is marked `semantic_role = POSITION_COORDINATE`. There is no `question_id`, response value, or response distribution in this artifact.

**Correcting source:** `data/ddm_build_copy/ddm_v550_position_distribution.py` at the frozen SHA, especially `_respondent_slice`, `POSITION_DISTRIBUTION_COLUMNS`, and `build_position_distribution_rows`.

**Effect on larger conclusion:** the earlier evidentiary basis is retracted. `position_distribution` cannot establish stranded question-conditioned meaning. The larger conclusion survives on the actual question-conditioned producer, `indicator_answer_matrix_rows`, and on exact bridge field loss.

### Correction 2 — active `ddm_v551_conditional.py` was misidentified

**Prior claim:** the prior result described `build_conditional_determinicity_index` as grouping structural atoms by relation/indicator and computing dominant values, alternative counts, ambiguity and coverage.

**Why wrong:** that is not the pinned active implementation. The active `data/ddm_build_copy/ddm_v551_conditional.py` consumes V550 bridge rows, requires the `derived_determinicity` lane, bridge eligibility, joined question-use and source-structure contracts, sufficient support, and deduplicates by source/wave/country/question/var/source-row hash. `_conditional_row` projects each surviving bridge row into a conditional record carrying response semantics, structural mappings, scalar support and provenance.

**Correcting source:** `data/ddm_build_copy/ddm_v551_conditional.py` at the frozen SHA, especially `_conditional_row` and `build_conditional_determinicity_index`.

**Effect on larger conclusion:** the earlier description is fully retracted. The corrected implementation still does not preserve `indicator_name` or `indicator_value`, so it does not restore the conditioning identity of `indicator_answer_matrix` rows.

### Correction 3 — the bridge was credited with conditioning identity it does not alias from the matrix

**Prior claim:** the prior result said the bridge carried position-conditioning-derived indicator/value fragments in a way that could be read as conserving the matrix conditioning key.

**Why wrong:** `_base_bridge_row` obtains `position_field` only from a literal source `position_field` column and `position_value` only from a literal source `position_value` column. `indicator_answer_matrix_rows` emits `indicator_name` and `indicator_value`, not those fields. No active alias `indicator_name -> position_field` or `indicator_value -> position_value` was found. The derived-lane audit view creates `predictor_field` from `driver_id` and `predictor_value` from `driver_facet_id`; those are question/relation authority fields, not aliases for empirical indicator coordinates.

**Correcting source:** `data/ddm_build_copy/ddm_v550_branching.py::indicator_answer_matrix_rows`; `data/ddm_build_copy/ddm_v550_bridge.py::_base_bridge_row`, `BRIDGE_EVIDENCE_LANE_MAP`, gate/audit construction.

**Effect on larger conclusion:** this correction strengthens the exact seam-loss finding. Response and scalar mass fields survive, while the empirical condition that gives those numbers meaning does not survive as an explicit semantic field.

### Correction 4 — recursive branch output was over-promoted from search product to irreducible joint carrier

**Prior claim:** the prior result recommended preserving the current recursive branch-conditioned output as a first-class joint conditional carrier because it represented conjunctive respondent structure.

**Why wrong:** `branch_nodes_rows` is a bounded greedy analysis. At each node it chooses the single available indicator with greatest positive entropy gain; stops at `max_depth` (default 3), low support, no remaining indicators, or no gain; and descends only through the first two values returned by `value_counts()`. Each node stores dominant response and entropy summaries, not a complete joint response contingency over all position combinations. The source respondents contain joint structure, but the current tree is one lossy analytical search over that structure.

**Correcting source:** `data/ddm_build_copy/ddm_v550_branching.py::branch_nodes_rows`.

**Effect on larger conclusion:** the current recursive tree is not itself an irreducible empirical carrier and should not be preserved merely because its source population has joint structure. Its prior proposed preservation is retracted.

### Correction 5 — the conditional helper is not the active canonical V551 publication path

The corrective pass also establishes that `compile_v551_relation_evidence_atoms.py`, the pinned canonical V551 v3 compiler, imports `ddm_v551_atoms` and publishes only `directional_candidate_adjudication`, `relation_evidence_atoms`, and `directional_distribution_coverage`. Its candidate bridge is restricted to `bridge_evidence_lane == direct_relation_response` and approved direct tables. It does not import or call `ddm_v551_conditional.py`.

Separately, pinned `ddm_v551_conditional.py` imports `MIN_ATOM_SUPPORT` and `SOURCE_TABLE_PRIORITY` from pinned `ddm_v551_atoms.py`, but those names are not defined there. The conditional helper therefore has both an active-seam wiring problem and a pinned import-contract problem.

This means the derived conditional product is best classified as `INTENDED_BUT_UNWIRED` at the frozen base, not as the canonical V551 consumer.

## Corrected active V550 empirical archaeology

### 1. `position_distribution`

`build_position_distribution_rows` creates marginal population prevalence for each available position coordinate after respondent deduplication. For each `position_field`/`position_value` it records `n_unweighted`, `n_weighted`, `pct_unweighted`, `pct_weighted`, weight status and provenance. The denominator is the respondent count with a nonblank value for that field. It is question-independent and marked `POSITION_COORDINATE`.

**Meaning:** population prevalence of a respondent coordinate, not a response conditional.

### 2. `position_indicator_summary`

`indicator_summary_rows` operates per question. For each indicator it compares question response entropy before and after conditioning on that indicator, and emits support plus `conditional_entropy`, entropy reduction, mutual information, normalized mutual information, Cramér's V, uplift and dominant-response summaries. It is an association summary over the full indicator variable, not a contingency table retaining every `indicator_value x response_value` cell.

**Meaning:** question-level indicator association/determinicity diagnostic.

### 3. `indicator_answer_matrix`

`indicator_answer_matrix_rows` is the active first-class one-dimensional response-conditioning producer. For each question and each available indicator it builds an unweighted crosstab of `indicator_value x response_value`; where weights are supplied it builds the parallel weighted pivot. It emits one row for each response value within each indicator value:

- `indicator_name`
- `indicator_value`
- `response_value`
- `n_unweighted`
- `pct_unweighted`
- `n_weighted`
- `pct_weighted`

`pct_unweighted` is the cell count divided by the unweighted total for that specific indicator value. `pct_weighted` is the corresponding weighted cell mass divided by the weighted total for that indicator value. With question metadata inherited into each row, this is actual empirical information of the form `P(response | indicator_name = indicator_value, question)` plus support mass.

Important support nuance: `n_unweighted` is the **response-cell count**, while the percentage denominator is the whole indicator-value subgroup. Any later support gate applied to `n_unweighted` is therefore gating response cells, not directly the conditioning subgroup as a whole.

### 4. `outlier_cohort_summary`

`outlier_cohort_rows` groups each indicator value with adequate support, computes the subgroup's dominant response and share, compares it to the question baseline dominant response, and labels the subgroup `conforms`, `deviates`, or `minority_converges`. It retains subgroup identity and support but deliberately reduces the subgroup response distribution to a dominant-response comparison.

**Meaning:** support-gated subgroup divergence diagnostic, not a complete conditional distribution.

### 5. `secondary_indicator_summary`

`secondary_indicator_summary_rows` scores all candidate indicators, greedily chooses the primary indicator with maximum `(mutual_information, cramers_v, n_unweighted)`, then tests each other indicator jointly with that primary. Joint rows require at least 50 respondents and positive incremental entropy gain. The output records a secondary indicator name/value, the chosen primary in `secondary_indicator_name`, `secondary_gain`, support and association summaries.

**Meaning:** greedy incremental-predictor diagnostic; evidence that some two-variable joint structure exists, but not a retained complete joint contingency.

### 6. `recursive_branch_nodes`

`branch_nodes_rows` records a bounded entropy-gain decision tree. It is support-gated, maximum-depth bounded, greedily chooses one best split per node, follows only two most frequent values, and stores dominant-response/entropy summaries.

**Meaning:** diagnostic search topology over respondent joint structure, not the joint structure itself.

### 7. `branch_position_signature`

`build_position_signature_rows` searches `POSITION_COORDINATE` columns, computes association statistics against the current question response, ranks candidates, retains at most five, and explicitly emits `cloud_lane_artifact = True`, `diagnostic_artifact = True`, `not_direct_evidence = True`, `evidence_role = diagnostic_position_signature`, `artifact_status = enabled_diagnostic`. The shard builder independently labels nonempty output `enabled_diagnostic`.

**Meaning:** explicitly diagnostic ranked position-feature signature.

## Exact `indicator_answer_matrix` field conservation through the bridge

The bridge maps `indicator_answer_matrix` to empirical object type `indicator_answer_matrix` and evidence lane `derived_determinicity`.

| V550 matrix field | Bridge behavior | Derived-lane audit | Pinned conditional helper |
|---|---|---|---|
| `indicator_name` | **No alias to `position_field`; no explicit conserved matrix-conditioning field established** | `predictor_field` is populated from `driver_id`, not `indicator_name` | not emitted |
| `indicator_value` | **No alias to `position_value`; no explicit conserved matrix-conditioning field established** | `predictor_value` is populated from `driver_facet_id`, not `indicator_value` | not emitted |
| `response_value` | read by response fallback and becomes bridge response raw/normalized material | `response_value_normalized` retained | `response_value_normalized` retained |
| `n_unweighted` | retained as support and `n_unweighted` | retained | retained after support gate |
| `pct_unweighted` | retained | omitted from compact derived audit view | retained in conditional output |
| `n_weighted` | retained | omitted from compact derived audit view | retained in conditional output |
| `pct_weighted` | retained | omitted from compact derived audit view | retained in conditional output |
| question identity from `question_meta` | retained as `question_id`/`var_code` | retained | retained |

The exact negative finding is therefore narrow and strong: **there is no proved active alias `indicator_name -> position_field` or `indicator_value -> position_value`.** `driver_id`, `driver_facet_id`, `predictor_field`, `predictor_value`, and question-contract `position_conditioning` are separate authority concepts and cannot lawfully substitute merely because they sound position-related.

### Identity consequences

- The empirical source row's meaningful conditioning identity is `(question identity, indicator_name, indicator_value)` together with response value.
- Bridge semantic identity exposes `position_field`/`position_value`, but for matrix rows those fields are not populated from `indicator_name`/`indicator_value` by the inspected code.
- The compact derived-lane audit replaces the idea of a predictor with `driver_id`/`driver_facet_id`, which identifies governed relation structure rather than the respondent indicator condition.
- `_conditional_row` emits no `position_field`, `position_value`, `indicator_name`, `indicator_value`, `predictor_field`, or `predictor_value`.
- `conditional_id` is based on source/wave/country/question/var/source-row hash; it does not make the absent conditioning semantics human- or machine-interpretable as a governed position coordinate.

This is the principal active-seam loss established by R01.

## Bridge and V551 gate behavior

`BRIDGE_EVIDENCE_LANE_MAP` sends these active V550 families to `derived_determinicity`:

- `indicator_answer_matrix`
- `outlier_cohort_summary`
- `secondary_indicator_summary`
- `recursive_branch_nodes`

`position_distribution` and `position_indicator_summary` instead enter `position_context`; `branch_position_signature` also enters `position_context`.

Bridge `v551_conditional_determinicity_eligible` is assigned from `derived_lane & common_relation_gates`. Those common gates require certified relation role/semantics/directionality, complete structural mapping, relation permission, no review requirement, joined contracts/source structure, visibility, substantive/non-special response, response-map match and non-metadata structural identity. This eligibility flag is not by itself the final conditional support decision.

The pinned conditional helper then independently requires:

1. `v551_conditional_determinicity_eligible == true`;
2. `bridge_evidence_lane == derived_determinicity`;
3. `question_use_contract_joined == true`;
4. `source_structure_fields_joined == true`;
5. `support_status == sufficient_support` (or recomputation to that result from `n_unweighted`);
6. uniqueness under its source/wave/country/question/var/source-row-hash key.

For matrix rows, because `n_unweighted` is the response-cell count, this final support gate operates at response-cell granularity. A low-frequency response cell can therefore be excluded even when the conditioning subgroup itself has substantial total support. A gated set of surviving rows cannot be assumed to conserve the original response distribution without an explicit mass-conservation contract.

## Active canonical V551 seam

At the frozen SHA, `compile_v551_relation_evidence_atoms.py` is explicitly the canonical V551 v3 compiler. Its canonical artifacts are:

- `directional_candidate_adjudication`
- `relation_evidence_atoms`
- `directional_distribution_coverage`

`build_v551_certification_candidate_bridge` in `ddm_v551_atoms.py` restricts candidates to `bridge_evidence_lane == direct_relation_response` and source tables `answer_distribution` / `country_answer_distribution`. Derived-determinicity rows are not canonical V551 atom candidates.

Therefore `ddm_v551_conditional.py` is not evidence that the derived lane is canonically preserved downstream. At this base it is a separate, unwired helper, and its own imports are inconsistent with pinned `ddm_v551_atoms.py` (`MIN_ATOM_SUPPORT` and `SOURCE_TABLE_PRIORITY` are imported but not defined there).

## Corrected family classification

### `position_distribution` — `STRANDED_MEANING`
Meaningful marginal respondent-position prevalence is produced and bridged as `position_context`, but no canonical V551 consumer of those prevalence rows was established in this court. It is not conditional response evidence.

### `position_indicator_summary` — `UNRESOLVED`
It carries real per-question association summaries, but the corrected active seam does not establish either a canonical terminal consumer or explicit diagnostic-only authority. Do not promote or discard it solely from naming.

### `indicator_answer_matrix` — `STRANDED_MEANING`
This is the active one-dimensional empirical conditional contingency. Response/support fragments enter the derived bridge lane, but the explicit empirical conditioning key `indicator_name`/`indicator_value` is not conserved into bridge position identity or the pinned conditional output, and the derived lane is not part of canonical V551 v3 publication.

### `outlier_cohort_summary` — `DIAGNOSTIC_ONLY`
A support-gated dominant-response comparison for each indicator cohort. It is a lossy analytical summary of conditional evidence and no canonical consumer was established.

### `secondary_indicator_summary` — `DIAGNOSTIC_ONLY`
A greedy primary/secondary incremental-entropy analysis with a fixed joint-support threshold and positive-gain filter. It is not a complete joint empirical carrier.

### `recursive_branch_nodes` — `DIAGNOSTIC_ONLY`
A bounded greedy search tree over joint respondent structure, not the irreducible joint structure itself.

### `branch_position_signature` — `DIAGNOSTIC_ONLY`
Explicitly labeled diagnostic, cloud-lane, and not-direct-evidence by its producer.

### `derived_determinicity` bridge lane — `INTENDED_BUT_UNWIRED`
The bridge deliberately gathers derived V550 analyses, gates them and exposes a conditional-determinicity eligibility/audit surface, but canonical V551 v3 publication does not consume that lane.

### V551 `conditional_determinicity` product — `INTENDED_BUT_UNWIRED`
The helper defines a projected conditional artifact, but the canonical V551 compiler does not call it, its output omits the empirical matrix conditioning key, and its pinned imports reference absent names in `ddm_v551_atoms.py`.

## Corrected verdict

`MATERIAL_SEMANTIC_LOSS_NOT_FAITHFULLY_PRESERVED`

The defensible semantic-loss claim is now narrower than the prior result and better grounded. V550's active `indicator_answer_matrix` contains genuine respondent response distributions conditioned on actual indicator values. The V550 bridge preserves question/response and scalar count/share fields but does not prove any lawful mapping of `indicator_name`/`indicator_value` into `position_field`/`position_value`. The compact derived audit substitutes relation-authority identifiers for predictor labels, and the separate conditional helper omits the source conditioning fields entirely. Canonical V551 v3 does not consume the derived lane in any case.

Thus shared strings or nearby concepts cannot rescue the seam: a row saying that a particular response has count/share `x` is not the same empirical claim after the condition under which `x` was observed has disappeared.

This does **not** authorize converting demographic/position correlations into actor facts, identity, belief, psyche, biography or destiny.

## What this court retracts

- Any assertion that active `position_distribution` contains question-conditioned response distributions.
- Any assertion that active `ddm_v551_conditional.py` is an atom-dominance/ambiguity compiler.
- Any assertion that `indicator_name`/`indicator_value` are aliased to bridge `position_field`/`position_value` without code proof.
- Any recommendation to preserve the current recursive branch tree itself as the irreducible joint empirical substrate.
- Any implication that the existence of `ddm_v551_conditional.py` proves canonical downstream consumption of the derived lane.

## Unresolved questions / blockers

1. The exact authoritative terminal consumer, if any, for `position_indicator_summary` remains unresolved within R01's bounded seam archaeology.
2. The pinned `ddm_v551_conditional.py` import inconsistency (`MIN_ATOM_SUPPORT`, `SOURCE_TABLE_PRIORITY` absent from pinned `ddm_v551_atoms.py`) prevents treating that helper as an executable canonical path without separate repair/authority.
3. R01 does not determine the minimum replacement architecture or retention substrate; those belong to other Conditional-Meaning Chamber cells.
4. R01 does not claim that the current greedy recursive tree must survive. If joint respondent conditionals are terminally required, their lawful sufficient representation must be adjudicated separately from this tree implementation.
5. No alias from empirical indicator coordinates to generated V3 structural-position coordinates is established here. Shared values or field-like names are not ontology authority.

## Evidence ledger

Directly re-read at exact SHA `8c87f7725ba58202b5377c974548140420709fa9`:

- `data/ddm_build_copy/ddm_v550_position_distribution.py`
  - `POSITION_DISTRIBUTION_COLUMNS`
  - `_respondent_slice`
  - `build_position_distribution_rows`
- `data/ddm_build_copy/ddm_v550_branching.py`
  - `indicator_summary_rows`
  - `secondary_indicator_summary_rows`
  - `indicator_answer_matrix_rows`
  - `branch_nodes_rows`
  - `outlier_cohort_rows`
- `data/ddm_build_copy/ddm_v550_clouds.py`
  - `BRANCH_POSITION_SIGNATURE_COLUMNS`
  - `build_position_signature_rows`
- `data/ddm_build_copy/ddm_v550_bridge.py`
  - `BRIDGE_TABLE_MAP`
  - `BRIDGE_EVIDENCE_LANE_MAP`
  - `_base_bridge_row`
  - `_bridge_lane_usability`
  - V551 gate construction
  - derived-lane audit projection
- `data/ddm_build_copy/ddm_v551_conditional.py`
  - `_conditional_row`
  - `build_conditional_determinicity_index`
- `data/ddm_build_copy/ddm_v551_atoms.py`
  - `APPROVED_DIRECT_TABLES`
  - `build_v551_certification_candidate_bridge`
  - active exported constants/symbols
- `data/ddm_build_copy/compile_v551_relation_evidence_atoms.py`
  - `CANONICAL_ARTIFACTS`
  - `compile_v551_run`
- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py`
  - active producer wiring and diagnostic status for `branch_position_signature`

All implementation claims in this corrected result refer to that frozen source state. Historical or later implementations are not imported into the finding.