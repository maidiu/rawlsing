# VT3-CM-R01 — Conditional-Value Archaeology Court Record

## Court metadata

- **Cell:** `VT3-CM-R01`
- **Mission:** determine whether meaningful respondent-position-conditioned empirical information computed in V550 is faithfully preserved through V551/V552; distinguish naming debt from evidence-loss debt; identify a lawful non-demographic repair path without modifying production code.
- **Launch base SHA examined:** `8c87f7725ba58202b5377c974548140420709fa9`
- **Launch base tree SHA:** `b016a5bc07b6aa17f1db08df91ed0b77d1055af7`
- **Assigned branch:** `agent/vozhd-trii-vt3-cm-r01`
- **Authorized write domain:** this `VT3_CM_R01/RESULT.md` and sibling `RESULT.json` only.
- **Production code changed:** `NO`

## Governing law applied

`data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md` at the pinned launch SHA is treated as binding interpretive law beneath explicit source semantics, accepted semantic authority, and closed jurisdiction. The controlling engineering implications for this court are:

1. downstream vividness may not exceed upstream authority;
2. structural evidence may constrain a world but may not silently become biography or psyche;
3. unknown, missing, unresolved, and forbidden inference are lawful states;
4. provenance and stage ownership must remain explicit;
5. convenience does not justify semantic flattening;
6. the lawful target is enough causal information to constrain later possibility without turning structure into mechanical predetermination.

The present question is therefore not whether downstream code contains *something named conditional*, but whether the empirical meaning established upstream survives with enough identity, conditioning keys, denominators, response distributions, and provenance to remain the same evidence.

# Final verdict

**`MATERIAL_SEMANTIC_LOSS_NOT_FAITHFULLY_PRESERVED`**

V550 contains first-class respondent-level empirical conditional evidence: observed answer distributions conditioned on respondent position-field values, plus recursive conjunctive branch conditioning over actual respondent rows. V551/V552 preserve some provenance fragments and create other legitimate conditional/position-related structural summaries, but those downstream objects change the unit of analysis, conditioning key, denominator, and target quantity. They therefore do **not** faithfully preserve V550's respondent-position-conditioned empirical meaning.

`conditional_determinicity_index.csv` is not intrinsically invalid on its own structural-atom terms. The debt is twofold:

- **naming debt:** its name can be mistaken for the respondent-conditioned evidence already computed in V550;
- **evidence-loss debt:** it is not a substitute for that V550 evidence, and V552 currently accepts the V551 conditional artifact at the compile interface but explicitly discards it during structural construction.

The correct repair is to preserve respondent position-conditioned and branch-conditioned evidence as distinct first-class carriers, without demographic reconstruction or demographic inference, and without overloading structural-atom determinicity or V552's item/region observation rollups.

# Evidence boundary and method

This court directly inspected source at the exact launch base SHA. Findings below are labeled **DIRECT OBSERVATION** where visible in pinned source, **INFERENCE** where semantic consequences follow from those observations, and **UNRESOLVED** where a launch-listed exact symbol was not independently located and therefore is not silently equated with similarly named code.

Primary files examined:

- `data/ddm_build_copy/ddm_v550_position_distribution.py`
- `data/ddm_build_copy/ddm_v550_branching.py`
- `data/ddm_build_copy/ddm_v550_bridge.py`
- `data/ddm_build_copy/ddm_v551_conditional.py`
- `data/ddm_build_copy/ddm_v551_atoms.py`
- `data/ddm_build_copy/compile_v552_structural_ddm.py`
- `data/ddm_build_copy/ddm_v552_structural.py`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`

No production file was edited.

# Findings

## F01 — V550 computes one-dimensional respondent-position-conditioned answer distributions

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v550_position_distribution.py`

`POSITION_DISTRIBUTION_COLUMNS` is:

`position_field, position_value, question_id, question_number, response_code, frequency, percentage`

`POSITION_VALUE_COUNTS_COLUMNS` is:

`position_field, position_value, sample_size`

`compute_position_conditional_distributions(df, fields=POSITION_FIELDS)` iterates observed values of each configured position field, filters the respondent dataframe to the matching value, groups observed responses question-by-question, and records response `frequency` and `percentage` for that position-conditioned respondent subset.

`compute_position_value_counts(...)` supplies the sample-size support for the conditioning value.

**INFERENCE**

The semantic object is an empirical conditional response distribution of the form:

`P(observed response to question Q | respondent position_field = position_value)`

with explicit respondent counts/percentages and a recoverable conditioning denominator. This is not merely a label, association, structural relation, or descriptive tag.

## F02 — V550 also computes joint/conjunctive branch-conditioned respondent evidence

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v550_branching.py`

`evaluate_branch(df, branch_path, question_id, ...)` constructs a conjunctive mask over branch conditions and computes base and branch-filtered response counts/percentages plus branch sample size.

`branch_metrics(...)` computes branch-filtered sample size and response detail.

`recursive_branch_scan(...)` recursively enumerates branch values/depth, filters actual respondent rows, respects `min_sample`, and returns branch response distributions.

**INFERENCE**

This evidence is stronger than a collection of independent one-dimensional conditionals. A normalized branch path represents a joint predicate over respondent-position conditions, and its meaning includes path identity, branch depth, sample-size eligibility, and branch-specific response distributions. Flattening it into independent indicator/value fragments destroys interaction structure.

## F03 — V550's bridge preserves provenance fragments, not the full respondent-conditional semantics

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v550_bridge.py`

`make_v550_evidence_bridge_rows(...)` accepts `position_conditioning_rows` and `position_profiles` and can emit bridge/index rows sourced from position-conditioning material. It maps fields such as `position_field` toward indicator identity and carries source-table/source-row provenance and selected value/response fragments where available.

**INFERENCE**

This is meaningful preservation: position-conditioned source identity is not wholly erased. But bridge rows are not demonstrated to preserve the complete V550 empirical object: respondent frequency, percentage, conditioning denominator, question-specific distribution identity, and recursive joint branch path semantics together. Provenance fragments are therefore counterevidence to a claim of *total erasure*, not evidence of faithful semantic preservation.

## F04 — V551 `conditional_determinicity_index` is a structurally different conditional object

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v551_conditional.py`

`build_conditional_determinicity_index(atom_registry, direct_relation_edges)` emits rows with schema:

`relation_id, atom_id, indicator_name, dominant_value, dominant_value_share, alternative_value_count, ambiguity_rate, response_coverage_count, gap_policy, coverage_trace_ids`

The implementation groups deterministic structural atom participants by `(relation_id, indicator_name)`, counts atom `value` occurrences, and derives dominant atom value/share, alternative-value count, ambiguity, distinct atom-response coverage, and coverage trace IDs.

**INFERENCE**

The index answers a structural question about concentration/ambiguity among atom values participating in a relation/indicator grouping. It does not reproduce the V550 question-answer distribution conditioned on a respondent's position-field value.

The following semantic axes differ:

| Axis | V550 respondent conditional evidence | V551 conditional determinicity |
|---|---|---|
| Unit | respondent observations | structural atoms / relation participants |
| Conditioning identity | `position_field`, `position_value` | `relation_id`, `indicator_name` |
| Target | answer distribution for a question | dominant atom value / ambiguity |
| Denominator | respondent subset/sample size | atom-value occurrence population |
| Primary measures | frequency, percentage | dominant share, alternatives, ambiguity, coverage |
| Joint paths | recursive conjunctive respondent branches available upstream | not equivalent to branch-path respondent conditioning |

Therefore the V551 artifact is not semantically wrong merely because it differs; it is wrong **only if treated as the carrier or replacement for V550 respondent-conditional evidence**.

## F05 — V551 atom registry preserves evidence lineage but does not cure the unit-of-analysis change

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v551_atoms.py`

The atom registry carries structural identity and provenance fields including relation/hub/indicator/value/response/source-table/source-row information, and source prioritization includes V550-derived evidence material.

**INFERENCE**

Atom-level lineage can preserve where a structural fact came from. It cannot, by itself, reconstruct a respondent-conditioned probability/frequency object whose meaning depends on respondent counts, conditioning denominators, question response distributions, and potentially conjunctive branch paths. Atom provenance is therefore evidence-bearing but non-substitutive.

## F06 — V552's compile interface can transport the V551 conditional artifact, but the structural builder explicitly discards it

**DIRECT OBSERVATION** — `data/ddm_build_copy/compile_v552_structural_ddm.py`

`compile_v552_structural_ddm(...)` accepts an optional `conditional_determinicity_path`, reads that CSV when supplied, passes the dataframe to `build_v552_structural_outputs(...)`, and records the conditional input path in compiler/manifest input handling.

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v552_structural.py`

`build_v552_structural_outputs(..., conditional_determinicity: pd.DataFrame | None = None, ...)` explicitly executes a deletion statement that includes `conditional_determinicity` among unused inputs:

`del relation_coverage, relation_spread, indicator_crosswalk, conditional_determinicity, atom_registry`

The builder also emits `conditional_determinicity_status_audit` as an empty dataframe initialized only with `CONDITIONAL_DETERMINICITY_STATUS_AUDIT_COLUMNS`.

**INFERENCE**

There is an interface-level transport path without semantic consumption. Even V551's *different* structural conditional artifact is not used to shape V552 structural output at this pinned implementation. The empty status-audit output does not preserve the underlying evidence.

## F07 — V552 recomputes a legitimate but non-equivalent position-conditioning profile

**DIRECT OBSERVATION** — `data/ddm_build_copy/ddm_v552_structural.py`

`build_position_conditioning_profile_from_observations(base, observations)` rolls observation records up by `region_value` and derives aggregate measures over fields including `money_scale`, `comfort`, and `target_to_money_ratio`.

**INFERENCE**

This is evidence-bearing for the question it asks: how item/observation metrics vary by region/value. It does not represent arbitrary V550 `(position_field, position_value)` respondent conditioning, per-question respondent answer frequencies/percentages, or recursive conjunctive branch paths. Similar vocabulary (`position`, `conditioning`) must not be used to erase the semantic boundary.

## F08 — The loss is semantic, not merely a filename problem

**INFERENCE from F01–F07**

The seam contains at least five independent losses/drifts:

1. **Unit-of-analysis drift:** respondents → structural atoms → item/observation aggregates.
2. **Conditioning-key drift:** arbitrary respondent `position_field/position_value` and joint branch predicates → relation/indicator atom grouping or `region_value` rollup.
3. **Denominator drift/loss:** respondent subset sample sizes and response frequencies/percentages are not preserved as the same quantity.
4. **Target-variable drift:** question-answer distributions → dominant structural values/ambiguity or observation metric means.
5. **Joint-branch loss:** conjunctive branch-path identity, depth, minimum-sample support, and branch-specific response distributions are not represented as first-class downstream semantics.

A rename alone cannot repair these differences.

# Launch-target symbol ledger

The launch asked this court to enumerate/classify several exact V550 names. The pinned inspection supports the following disposition:

- `compute_position_conditional_distributions` — **DIRECTLY LOCATED; substantive empirical evidence producer.**
- `recursive_branch_scan`, `evaluate_branch`, `branch_metrics` — **DIRECTLY LOCATED; substantive branch-conditioned empirical evidence producers/support.**
- `compute_position_conditional_answer_distributions` — **UNRESOLVED EXACT SYMBOL LOCATION.** No independent exact-symbol location was established during this court's pinned-source inspection. Its intended semantic role must not be silently inferred from `compute_position_conditional_distributions`.
- `compute_indicator_answer_matrix` — **UNRESOLVED EXACT SYMBOL LOCATION.** No independent exact-symbol location was established during this court's pinned-source inspection.
- `build_branch_position_signatures` — **UNRESOLVED EXACT SYMBOL LOCATION.** Branch-conditioned machinery was directly observed, but this exact helper name was not independently located.
- within-dimension tags / exact relation evidence — **PARTIALLY OBSERVED THROUGH BRIDGE/atom provenance; exact launch-referenced producer inventory remains unresolved.**
- branch-display/render support tied to position conditioning — **display/helper semantics must remain separate from empirical branch evidence; exact helper inventory remains unresolved.**

These unresolved entries are evidence-boundary findings, not a claim that the symbols or artifacts do not exist elsewhere. A graceful guess would violate the governing spirit's explicit treatment of unresolved state.

# Artifact dispositions

## Evidence-bearing and semantically substantive

1. **V550 respondent position-conditional distribution rows** — first-class empirical evidence; materially stranded as a downstream semantic object.
2. **V550 position-value counts/sample sizes** — denominator evidence necessary to interpret the conditional distributions.
3. **V550 recursive branch-conditioned response evidence** — first-class joint/conjunctive respondent evidence; materially stranded as a downstream semantic object.
4. **V550 bridge rows derived from position conditioning** — derivative evidence/provenance carriers; useful but not a faithful substitute for the complete conditional distributions.
5. **V551 atom registry** — evidence/provenance-bearing structural carrier; not a respondent-conditional distribution carrier.
6. **V551 `conditional_determinicity_index.csv`** — evidence-bearing structural-atom summary on its own terms; semantically non-equivalent to V550 respondent conditionality.
7. **V552 `position_conditioning_profile`** — evidence-bearing item/region observation rollup on its own terms; semantically non-equivalent to V550 respondent conditionality.

## Helper/status/display only for the present question

1. **V552 `conditional_determinicity_status_audit`** — schema/status placeholder in the pinned builder; emitted empty and not an evidence carrier for V550 conditionals.
2. **Pure branch display/render helpers** — presentation only unless they themselves carry an independently specified evidence contract. Display cannot substitute for the underlying branch-conditioned empirical rows.

# Naming debt versus evidence-loss debt

## Naming debt

`conditional_determinicity_index.csv` uses vocabulary broad enough to suggest a general conditional-evidence index. Its actual implementation is a structural-atom dominant-value/ambiguity summary. The name is therefore hazardous at the V550→V551 seam because an auditor can plausibly mistake it for preservation of V550 respondent conditionality.

## Evidence-loss debt

The deeper problem remains even if the file is renamed. The downstream graph lacks a demonstrated first-class carrier preserving:

- respondent `position_field`;
- respondent `position_value`;
- question identity;
- response code;
- response frequency;
- response percentage;
- conditioning/sample denominator;
- normalized joint branch path where applicable;
- branch sample size/depth/min-sample provenance;
- direct trace back to upstream empirical source rows.

This is a semantic preservation gap, not nomenclature alone.

# Lawful non-demographic repair path

No production repair is performed by this court. The parent architecture should preserve the following separation of semantic ownership.

## Carrier A — respondent position-conditioned empirical distributions

A first-class artifact should preserve, at minimum:

- `position_field`
- `position_value`
- `question_id`
- `question_number` where authoritative
- `response_code`
- `frequency`
- `percentage`
- explicit conditioning denominator / `sample_size`
- source trace/provenance IDs sufficient for replay and verification
- explicit unknown/valid-empty states rather than synthetic completion

This carrier should mean only observed respondent conditioning on authorized position variables. It must not be upgraded into actor biography, psyche, or deterministic assignment.

## Carrier B — respondent branch-conditioned empirical distributions

A separate first-class artifact should preserve, at minimum:

- normalized ordered/conjunctive branch predicates;
- branch depth;
- branch sample size;
- `min_sample`/eligibility provenance where relevant;
- question identity;
- response code/count/percentage;
- traceability to the respondent evidence and branch-evaluation rule.

Joint branch evidence must not be reconstructed by multiplying or composing independent one-dimensional conditionals unless explicit authority establishes such a model.

## Keep distinct from

- V551 structural-atom determinicity/ambiguity;
- V552 item/region observation conditioning;
- demographic inference or demographic synthesis;
- actor knowledge, actor belief, psyche, trait, or biography.

The safe repair principle is **preserve empirical constraints without converting them into personhood claims**.

# Counterevidence considered

The verdict is not based on a false claim of total disappearance.

1. V550 bridge machinery does carry position-conditioning-derived source identity/provenance fragments.
2. V551 atoms preserve source table/row and structural indicator/value/response fragments.
3. V552 compiler has an input path for V551 conditional determinicity and passes the loaded dataframe into the structural builder.
4. V552 has a position-conditioning profile that is genuinely evidence-bearing for its own observation-level quantities.

These facts narrow the verdict: the seam preserves lineage and other conditional summaries, but not the same respondent-conditioned empirical object.

# Unresolved questions

1. Where, at exact launch base SHA, are the launch-listed exact symbols `compute_position_conditional_answer_distributions`, `compute_indicator_answer_matrix`, and `build_branch_position_signatures`, if they exist under those names?
2. What is the complete pinned inventory of within-dimension tag/exact-relation artifacts whose semantics derive from respondent position conditioning?
3. What is the complete pinned inventory of branch-display helpers, and which are strictly display versus evidence-producing wrappers?
4. Is there a generated-data artifact outside the directly inspected source set that already serializes the complete V550 respondent conditional distributions or branch distributions for downstream reuse despite the source-level seam described here? No such faithful downstream consumer was established by this court.
5. Which future stage should own consumption of the preserved respondent conditional evidence after the carrier is restored? This court recommends preservation and semantic separation but does not reopen closed downstream jurisdiction.

None of these unresolved questions reverses F01–F08. They constrain the completeness of the exact producer/helper inventory and the placement of any eventual repair.

# Recommended parent actions

1. **Accept the verdict that V550 respondent-position-conditioned evidence is not faithfully preserved as a first-class downstream semantic object.**
2. **Do not treat `conditional_determinicity_index.csv` as the V550 conditional carrier.** Preserve its structural-atom meaning or rename it to reduce ambiguity.
3. **Authorize a dedicated non-demographic preservation contract** for respondent position-conditioned distributions and a separate contract for joint branch-conditioned distributions.
4. **Require explicit denominator and branch-path preservation.** Frequencies/percentages without their conditioning population, or branch fragments without normalized path identity, are insufficient.
5. **Resolve the launch-listed exact-symbol inventory before implementation** so no hidden V550 artifact is duplicated or contradicted.
6. **Keep V552's item/region `position_conditioning_profile` semantically separate.** It is useful evidence for a different question and should not be repurposed as respondent conditioning.
7. **Revisit the V552 conditional input seam.** A compile interface that reads/passes `conditional_determinicity` while the builder explicitly discards it should either acquire a lawful consuming contract or be made semantically explicit as transport/status only; do not infer meaning from presence at the interface.
8. **Prohibit demographic backfilling.** No repair should infer missing demographic identity, convert structural categories into psyche, or treat conditional empirical patterns as deterministic actor traits.

# Court closure

At launch base `8c87f7725ba58202b5377c974548140420709fa9`, the R01 court finds a genuine V550→V551/V552 conditional-meaning preservation seam. The machine retains pieces of lineage and constructs downstream summaries that are valid in their own jurisdictions, but the respondent-conditioned empirical distributions and recursive joint branch evidence change meaning or cease to exist as first-class downstream evidence. The appropriate action is preservation with bounded jurisdiction, not demographic synthesis and not semantic overloading.

**Final verdict: `MATERIAL_SEMANTIC_LOSS_NOT_FAITHFULLY_PRESERVED`.**
