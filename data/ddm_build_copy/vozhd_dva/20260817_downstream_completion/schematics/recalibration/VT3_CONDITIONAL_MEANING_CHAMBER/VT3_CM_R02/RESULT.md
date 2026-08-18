# VT3-CM-R02 — Conditional Information-Loss Court

**Cell:** `VT3-CM-R02`  
**Mission:** Falsify, if possible, the proposition that V550's valuable determinicity content is substantially smaller than its current artifact surface and may be represented by governed conditional empirical distributions plus provenance.  
**Repository:** `maidiu/rawlsing`  
**Repository head examined:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Publication branch:** `agent/vozhd-trii-vt3-cm-r02-information-loss`  
**Production-code changes:** `NONE`  
**Downstream recreation audit:** deliberately not performed except where needed to distinguish stored convenience from empirical necessity; VT3-CM-R03 owns downstream recreation.

## 1. Governing law applied

Directly inspected binding governing spirit:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- blob SHA: `588cf3954c33417665c5f9bac04e8b27e75d7f7c`

The court applied the binding requirements to preserve heterogeneity, contradiction, uncertainty, typed absence, provenance, replay, and structural constraint without converting population correlations into actor destiny. The same law also requires minimum sufficient machinery and disfavors duplicated semantic ownership. The resulting test is therefore not whether an artifact is interesting or expensive, but whether deleting its materialization while retaining a smaller governed fact destroys empirical distinctions or exact lawful replay.

## 2. Final verdict

**VERDICT: `TARGET_HYPOTHESIS_SUBSTANTIALLY_SURVIVES_WITH_JOINT-STRUCTURE_CORRECTION`.**

The current V550 determinicity output surface contains much more stored analytical product than irreducible empirical information. `position_indicator_summary`, `outlier_cohort_summary`, `secondary_indicator_summary`, `recursive_branch_nodes`, and `branch_position_signature` are deterministic analytical products of a smaller empirical substrate plus versioned algorithm/authority rules. `indicator_answer_matrix` and `position_distribution` contain genuine empirical counts, but their materialized files do not own those facts if the underlying governed population/joint-response substrate remains available.

However, the strongest naive compression claim is false:

- `indicator_answer_matrix` is **not** the irreducible empirical core.
- a conditional-distribution object restricted to one position field at a time is **not** lossless.
- pairwise `P(response | position_field=value)` marginals do not preserve cross-indicator joint structure required by `secondary_indicator_summary` and recursive branching.
- question-conditioned distributions alone do not preserve the question-independent respondent population needed to recreate `position_distribution` exactly.

The minimum defensible empirical authority is therefore a **governed joint empirical substrate** from which a canonical `CONDITIONAL_EMPIRICAL_DISTRIBUTION` view can be generated for arbitrary governed predicates, including conjunctions and typed missingness.

Court tokens:

- `V550_DETERMINICITY_SURFACE_HAS_IRREDUCIBLE_ARTIFACT_VALUE = MOSTLY_FALSE`
- `INDICATOR_ANSWER_MATRIX_IS_IRREDUCIBLE_CORE = FALSE`
- `PAIRWISE_CONDITIONAL_DISTRIBUTIONS_ARE_MINIMUM_SUFFICIENT = FALSE`
- `GOVERNED_JOINT_EMPIRICAL_SUBSTRATE_IS_MINIMUM_SUFFICIENT = PASS`
- `CONDITIONAL_EMPIRICAL_DISTRIBUTION_AS_CANONICAL_VIEW = PASS_WITH_JOINT_PREDICATE_AND_POPULATION_REQUIREMENTS`

## 3. Directly observed implementation evidence

### 3.1 Shared branching substrate

Direct observation from:

- `data/ddm_build_copy/build_determinicity_repository_v550.py`
- blob SHA: `afd2a59e1cdff0024a57acaf1dab8ff30534e565`

The builder creates `branch_df = prepare_question_frame(df)` and passes the same prepared per-question frame and weight series into:

- `indicator_summary_rows`
- `secondary_indicator_summary_rows`
- `indicator_answer_matrix_rows`
- `outlier_cohort_rows`
- `branch_nodes_rows`

This establishes that these files are multiple projections/searches over a common empirical substrate rather than independently sourced facts.

### 3.2 Fixed conditioning fields

Direct observation from:

- `data/ddm_build_copy/ddm_v550_branching.py`
- blob SHA: `8f6d40e0d016d66e5a3b334b31747eaef752873f`

`INDICATOR_FIELDS` is exactly:

`sex`, `age_group`, `education_level`, `income_level`, `religion_label`, `urban_rural`, `region`, `ethnicity`, `language`, `employment`, `marital`, `household_size`.

### 3.3 `indicator_answer_matrix`

Direct observation: `indicator_answer_matrix_rows` loops each `INDICATOR_FIELDS` member, excludes rows where the indicator is empty, and emits one row for every observed `(indicator_name, indicator_value, response_value)` combination with:

- `n_unweighted`
- `pct_unweighted`
- `n_weighted`
- `pct_weighted`

Weighted cells are sums of validated weight values; if no weight series exists, weighted values fall back to unweighted counts.

**Inference:** this artifact is exactly a family of one-indicator contingency tables. It creates no information not already present in the joint respondent/question/position substrate.

### 3.4 `position_indicator_summary`

Direct observation from `indicator_summary_rows`:

- baseline response entropy is calculated over the full response vector `y`;
- for each indicator, missing indicator values are excluded before conditional entropy is calculated;
- if weights exist, baseline and conditional entropy use weights;
- `normalized_mutual_information(x,y)` and `cramers_v(x,y)` are unweighted;
- `mutual_information` is assigned `max(0, baseline_entropy - conditional_entropy)`;
- confidence tier is a support heuristic (`usable` at `mask.sum() >= 50`, otherwise `weak`).

Direct observation from:

- `data/ddm_build_copy/ddm_v550_metrics.py`
- blob SHA: `e7675f4080bb30e6526027a34db747b7be7f85c9`

`conditional_entropy`, `cramers_v`, `normalized_mutual_information`, and `distribution_entropy` are deterministic functions of the corresponding contingency/count distributions.

**Inference:** the scalar summary contains no irreducible empirical information. Exact replay does require preserving the baseline universe, indicator-complete universe, weight lane, and metric implementation/version. In particular, because baseline entropy can be computed on a larger population than indicator conditional entropy when the indicator is missing, the stored field called `mutual_information` is an implementation-defined score and should not be canonized as an empirical primitive.

### 3.5 `outlier_cohort_summary`

Direct observation from `outlier_cohort_rows`:

- the global baseline is the unweighted dominant response and share;
- every sufficiently supported `indicator=value` subgroup is visited;
- branch classification is `conforms`, `deviates`, or `minority_converges` based on dominant-response comparison;
- weights affect `n_weighted`, not the dominant-response classification.

**Inference:** despite its name, this is not a statistical outlier test. It is a deterministic subgroup-label view over baseline plus one-indicator conditional response distributions and a support rule.

### 3.6 `secondary_indicator_summary`

Direct observation from `secondary_indicator_summary_rows`:

- candidate one-indicator scores are first computed;
- one primary indicator is chosen by `(mutual_information, cramers_v, n_unweighted)` maximum;
- every secondary candidate is intersected with the primary candidate's nonmissing mask;
- rows with joint support `< 50` are skipped;
- a concatenated `primary||secondary` joint key is used to compute joint conditional entropy;
- `secondary_gain = max(0, primary_conditional_entropy - joint_conditional_entropy)`.

**Inference:** `secondary_gain` is deterministic, but its reconstruction requires cross-indicator joint response structure. Pairwise `indicator_answer_matrix` marginals are insufficient.

### 3.7 `recursive_branch_nodes`

Direct observation from `branch_nodes_rows`:

- recursion begins with all present `INDICATOR_FIELDS`;
- node response entropy and dominant response are unweighted;
- every remaining indicator is evaluated greedily by conditional-entropy gain;
- the best positive-gain indicator is chosen;
- only the two most frequent values of the selected indicator are recursed;
- defaults are `max_depth=3` and a wave-relative minimum branch support;
- stop reasons include `pure_or_near_pure`, `max_depth`, `underpowered`, `no_remaining_indicators`, and `no_gain`.

**Inference:** the stored tree is a deterministic, truncated search projection. It is necessarily lossy relative to the data that produced it and cannot be an empirical core.

### 3.8 `branch_position_signature`

Direct observation from:

- `data/ddm_build_copy/ddm_v550_clouds.py`
- blob SHA: `dfc878e87d984a1a3d7000a0c726bdc444f9945f`

`build_position_signature_rows`:

- considers only fields classified as `POSITION_COORDINATE`;
- is contract-gated by `allowed_as_branch_position_signature`;
- computes unweighted NMI and Cramér's V;
- ranks by `association_score = max(NMI, Cramér's V)`, then support, then field name;
- emits at most five features;
- explicitly writes `diagnostic_artifact=True`, `not_direct_evidence=True`, `evidence_role="diagnostic_position_signature"`, `artifact_status="enabled_diagnostic"`.

**Inference:** the implementation itself already classifies this artifact as diagnostic rather than direct evidence. Its scores and rank are deterministic from pairwise contingencies plus authority and ranking rules.

### 3.9 `position_distribution`

Direct observation from:

- `data/ddm_build_copy/ddm_v550_position_distribution.py`
- blob SHA: `651329254244e9f42a8d88c2721ccae6bd768073`

`build_position_distribution_rows`:

- operates across country frames, not one question's response distribution;
- creates a respondent slice deduplicated by available `(respondent_id, country_code)` keys;
- computes each position-field marginal after excluding empty values;
- emits unweighted counts/shares;
- emits weighted counts/shares only when weight status is exactly `weighted`.

**Inference:** this artifact is an empirical marginal view, but it cannot be reconstructed from per-question conditional distributions unless respondent-universe overlap or an explicit population-position base is retained.

### 3.10 Weight semantics

Direct observation from `classify_weight_status` in `ddm_v550_metrics.py`:

- states include `missing`, `invalid`, `unweighted_only`, `partial`, and `weighted`;
- partial validated weights preserve valid positive finite entries and leave other entries missing;
- downstream weighted entropy/count functions commonly coerce missing weight contributions to zero.

**Inference:** storing only `sum(weight)` and cell N is insufficient for exact replay where weight validity/status changes admissibility or lane behavior.

### 3.11 Support semantics

Direct observation from:

- `data/ddm_build_copy/ddm_v550_support.py`
- blob SHA: `1b841139fee051b154dcccd52cd3d866b958dbb5`

The shared support threshold defaults are:

- support rate: `0.005`
- support cap: `30`
- support floor: `2`

with threshold `ceil(total * 0.005)` bounded to `[2,30]`.

**Inference:** support/confidence labels are governed deterministic classifications, not empirical primitives.

### 3.12 Response semantics and typed absence

Direct observation from:

- `data/ddm_build_copy/ddm_v550_distributions.py`
- blob SHA: `43a62723b16f9c800ed7a6ef40a77e70a3f07377`

Response authority distinguishes at least:

- substantive response
- missing
- DK
- refusal
- IAP
- not asked
- inapplicable
- special response

and carries response semantics status/source/contract hash.

**Inference:** a replacement fact that collapses these states to generic null is semantically lossy even when substantive percentages remain unchanged.

### 3.13 Question-use / position authority

Direct observation from:

- `data/ddm_build_copy/ddm_v550_question_use.py`
- blob SHA: `8d90a5116fd05b5db17e9b4645638a3aa6fc1131`

The question-use contract separately governs permissions including:

- `allowed_as_response_distribution`
- `allowed_as_position_distribution`
- `allowed_as_context_distribution`
- `allowed_as_demographic_predictor`
- `allowed_as_branch_splitter`
- `allowed_as_branch_position_signature`
- `allowed_as_branch_relation_cosignature`
- `allowed_as_attitude_cloud_anchor`
- `allowed_as_attitude_cloud_feature`
- `allowed_as_v551_relation_evidence`
- `allowed_as_parent_prior_coordinate`

and carries `position_conditioning`, `position_modifiers`, `conditional_strata_weights` and related authority fields in its hash surface.

**Inference:** authority/provenance must survive compression; the current repeated artifact metadata need not remain duplicated if immutable authority references/hashes preserve exact governing semantics.

## 4. Dependency / derivability table

| Artifact | Exact input information | New stored product | Smaller-fact derivability | Required reconstruction authority | Court disposition |
|---|---|---|---|---|---|
| `indicator_answer_matrix` | question response rows; each present indicator; optional weights; question metadata | pairwise `(indicator,value,response)` cells with weighted/unweighted N and within-indicator percentages | **YES** from governed joint empirical fact | indicator missingness policy; response normalization; weight lane; authority | empirical deterministic view |
| `position_indicator_summary` | same response/position rows + weights | entropy, implementation-defined MI, NMI, Cramér's V, uplift, dominant-response/support labels | **YES**, but not always from matrix alone | unconditional baseline universe; indicator-complete mask; weight rules; metric version | diagnostic metric view |
| `outlier_cohort_summary` | baseline response distribution + supported indicator subgroups | subgroup branch labels and dominant responses | **YES** | support rule; unweighted classification rule | diagnostic cohort view |
| `secondary_indicator_summary` | all candidate indicators + response + joint completeness | primary selection, joint entropy, `secondary_gain` | **YES from joint fact; NO from pairwise matrix** | arbitrary two-field conjunctions; missingness; weights; support and tie rules | diagnostic joint-association view |
| `recursive_branch_nodes` | response + all available indicators + algorithm parameters | greedy truncated tree | **YES from joint fact; NO from pairwise matrix** | arbitrary conjunctions; candidate order; support; depth; top-2 rule; tie behavior | diagnostic-only lossy view |
| `branch_position_signature` | response + authority-permitted position fields | top-five ranked association signature | **YES** | contract gating; unweighted metrics; ranking/tie rules | diagnostic-only view |
| `position_distribution` | question-independent respondent population + position fields + weights | population position marginals | **YES from respondent-position base; NO from question CED alone** | respondent/population identity; dedupe; missingness; weight-status policy | empirical population view |

## 5. Minimum sufficient empirical fact candidate

### 5.1 Canonical storage fact

The court's minimum sufficient candidate is a normalized governed joint substrate, conceptually equivalent to:

`GOVERNED_EMPIRICAL_OBSERVATION`

Required information domains:

1. **survey identity** — source, source family, raw wave, canonical wave, country;
2. **population identity** — respondent identity or a losslessly equivalent population-overlap key;
3. **question/response identity** — question ID and exact normalized response category/state;
4. **typed absence** — distinct missing/DK/refusal/IAP/not-asked/inapplicable states where governed;
5. **joint conditioning state** — all governed position coordinates for that respondent with typed present/absent state;
6. **sampling state** — raw/validated weight and weight-validity status; survey-design fields where uncertainty must be preserved;
7. **authority references** — question-use, response semantics, position conditioning, source structure, normalization/transformation versions;
8. **provenance** — source dataset/file and immutable extraction/build identity.

This may be physically normalized into a respondent-position relation plus a respondent-question-response relation. The essential property is that the lawful join/overlap structure remains reconstructable.

### 5.2 Canonical empirical interface

From the joint fact, expose:

`CONDITIONAL_EMPIRICAL_DISTRIBUTION(question, survey_scope, governed_predicate, response_state, counts/support, denominator_scope, authority/provenance)`

The predicate grammar must support:

- unconditional `TRUE`;
- singleton predicates such as `income_level=low`;
- conjunctions such as `income_level=low AND education_level=secondary`;
- deeper conjunctions sufficient to replay currently authorized recursive paths;
- typed-missing predicates where missingness is itself required for replay/audit.

A CED restricted to singleton position predicates is not lossless.

### 5.3 Aggregate-only alternative

If respondent-indexed facts are prohibited, an aggregate-only representation must materialize every governed conjunction that any retained computation may query, plus question-independent population-position distributions and explicit overlap/denominator semantics. That can become a combinatorial cube. Therefore aggregate materialization is not automatically cheaper or conceptually cleaner than retaining a normalized joint respondent substrate and generating distributions on demand.

## 6. NONNEGOTIABLE fields/state for losslessness

1. source/source-family, raw wave, canonical wave, country, question identity;
2. respondent/population-universe identity or a losslessly equivalent overlap representation;
3. exact response category and response-semantics authority;
4. typed absence state;
5. jointly recoverable conditioning values, not only one-field marginals;
6. unweighted support;
7. weighted support and exact weight-status/validity lane;
8. denominator scope/universe identity (all response rows, indicator-complete rows, joint-complete rows, respondent population, weighted-valid population);
9. question-independent population-position base or respondent identity sufficient to rebuild it;
10. immutable authority/provenance hashes/references;
11. algorithm/view version for exact replay of derived products;
12. survey-design sufficient information if the parent architecture intends `uncertainty` to mean design-based uncertainty rather than support heuristics only.

Percentages do not need independent storage when counts and denominator scope are exact. MI, entropy, Cramér's V, uplift, confidence tier, branch labels, rank, and tree topology do not belong in the irreducible empirical fact.

## 7. Artifacts that can become deterministic views

All seven named artifacts can become deterministic views if the strengthened joint substrate is retained:

- `indicator_answer_matrix`
- `position_indicator_summary`
- `outlier_cohort_summary`
- `secondary_indicator_summary`
- `recursive_branch_nodes`
- `branch_position_signature`
- `position_distribution`

`indicator_answer_matrix` and `position_distribution` should remain recognized as empirical distribution views rather than mere diagnostics, because their counts are empirically meaningful. Their materialized files nevertheless need not be independent semantic authorities.

## 8. Diagnostic-only disposition

The following should be diagnostic/search products, not terminal empirical authority:

- `position_indicator_summary`
- `outlier_cohort_summary`
- `secondary_indicator_summary`
- `recursive_branch_nodes`
- `branch_position_signature`

Reasons:

- scalar association metrics collapse plural distributions;
- subgroup labels are deterministic summaries, not new evidence;
- secondary gain depends on a chosen primary and complete-case policy;
- recursive trees are greedy, truncated, top-two-only projections;
- position signatures are explicitly tagged diagnostic and not-direct-evidence in current code.

## 9. Genuine semantic-loss findings

### 9.1 If the strengthened joint empirical core is preserved

Deleting the materialized seven-artifact suite does **not** inherently delete empirical meaning. All seven can be regenerated exactly subject to frozen authority and view/compiler versions.

### 9.2 If replacement is only pairwise CED

Deletion is **not lossless**. Genuine losses include:

1. cross-indicator joint structure;
2. baseline-versus-complete-case population distinctions;
3. respondent overlap across questions and therefore exact population-position reconstruction;
4. typed absence if null states are collapsed;
5. weight-validity topology if only final weighted sums are retained;
6. survey-design uncertainty if only cell counts and weights are retained.

Retaining `secondary_indicator_summary` or a recursive tree does not repair loss of the underlying joint distribution; those products are themselves lossy projections.

## 10. Hostile counterexamples against the minimal representation

### CE-1 — same pairwise matrices, different joint conditional structure

Construct two populations with identical `A × response` and identical `B × response` contingency tables but different allocation of responses inside `(A,B)` cells. Every `indicator_answer_matrix` row remains identical, while `P(response | A,B)`, secondary gain after an `A` primary split, and deeper recursive children differ. Therefore pairwise matrices do not identify joint structure.

### CE-2 — same matrix, different baseline due indicator missingness

Hold the observed `X × response` matrix fixed. Add respondents whose `X` is missing but whose responses differ across two datasets. `indicator_answer_matrix` remains unchanged because empty X is excluded, while global baseline entropy/dominant response changes. `position_indicator_summary` and `outlier_cohort_summary` can therefore differ.

### CE-3 — same per-question distributions, different population overlap

Let Q1 and Q2 each have identical position distributions. In dataset P the same respondents answer both questions; in dataset Q the respondent sets are disjoint. Per-question CEDs are identical, but the deduplicated respondent population used by `position_distribution` differs. Question CED alone is insufficient.

### CE-4 — same weighted distribution, different unweighted support

Ten respondents with weight 10 can equal one hundred respondents with weight 1 in weighted totals. Weighted CEDs can be identical while unweighted N, support status, NMI/Cramér's V inputs, recursive eligibility, and confidence labels differ. Both weighted and unweighted lanes are required.

### CE-5 — same weighted/unweighted cell totals, different weight validity

Two cells can share final weighted sum and unweighted N while one has fully valid weights and the other has partial/invalid weights offset by valid entries. Current V550 distinguishes these states and different artifacts use them differently. Counts alone do not replay weight authority.

### CE-6 — refusal versus not asked

Two datasets can have identical substantive counts and generic null count but differ because the nulls are refusals in one and structurally `not_asked` in the other. Collapsing typed absence destroys admissibility/provenance even if ordinary percentages match.

### CE-7 — identical point estimates, different sampling uncertainty

Two surveys may have identical weighted/unweighted conditional cells while one pattern is dispersed across PSUs and another is concentrated in a single cluster/stratum. Point estimates match; design-based variance does not. A count-only CED cannot preserve uncertainty in the statistical sense.

### CE-8 — recursive tree erases minority configurations by construction

When a chosen split indicator has more than two values, `branch_nodes_rows` recurses only the two most frequent. An empirically extreme third or sixth category can change radically without changing the stored descendants for the top two values. The recursive tree is therefore provably not an irreducible representation of its own source population.

## 11. Special-court answers

### Is `indicator_answer_matrix` the irreducible empirical core?

**NO.** It is a useful pairwise conditional-distribution view, not a sufficient fact base.

### Can a cleaner `CONDITIONAL_EMPIRICAL_DISTRIBUTION` replace it?

**YES, if and only if** the CED is generated from or contains the lawful joint structure and its predicate grammar supports conjunctions, unconditional baseline, typed absence, exact support/denominator scope, weight status, population-position scope, and authority/provenance.

### Do MI, conditional entropy, Cramér's V contain irreducible information?

**NO.** They are deterministic functions of contingency distributions plus algorithm/missingness/weight policy.

### Does outlier status contain irreducible information?

**NO.** Current outlier status is a deterministic supported-subgroup dominant-response classification.

### Does secondary gain contain irreducible information?

**NO as a stored scalar; YES in the sense that its exact regeneration requires joint empirical information not present in pairwise marginals.**

### Do recursive branch trees contain irreducible information?

**NO.** They are deterministic, truncated greedy projections of joint data plus algorithm authority, and are themselves lossy.

## 12. Unresolved questions

1. **Terminal subset unresolved here by jurisdiction.** R02 establishes what is empirically derivable and what information is destroyed by candidate compressions. It does not determine which conditional predicates the terminal runtime truly requires; VT3-CM-R04 owns terminal position-conditioning requirements.
2. **Downstream recreation unresolved here by jurisdiction.** R02 did not establish whether V551–V558/V3 currently reconstruct or substitute for stranded V550 meaning; VT3-CM-R03 owns that question.
3. **Survey-design uncertainty authority requires parent decision.** Current inspected determinicity artifacts mainly expose support/confidence heuristics rather than design-based uncertainty. If the chamber's future canonical fact claims to preserve statistical uncertainty, PSU/stratum/replicate-weight sufficient information or governed variance products must be specified explicitly.
4. **Physical storage optimum unresolved.** Semantic minimization does not itself prove that a fully materialized conditional cube is byte-cheaper than a normalized respondent joint substrate. VT3-CM-R05 owns compute/cardinality cost.
5. **Exact byte-for-byte replay versus semantic replay.** Exact semantic regeneration is possible from joint facts plus frozen rules. Byte-identical historic artifact regeneration may additionally require serialization/order/numeric-version details; parent must decide whether this is required.

## 13. Recommended parent actions

1. Reject `indicator_answer_matrix` as the chamber's canonical irreducible empirical authority.
2. Define the chamber's candidate canonical authority as a governed joint respondent/position/response substrate with CED as the stage-facing distribution interface.
3. Require the CED predicate grammar to support governed conjunctions and typed missingness, not singleton position conditions only.
4. Separate empirical authority from deterministic analytical views; demote MI/entropy/Cramér's V, outlier labels, secondary gain, recursive trees, and position signatures to reproducible diagnostics unless another accepted authority proves terminal necessity.
5. Preserve `position_distribution` semantics through respondent/population identity or an explicit question-independent population-position lane.
6. Make denominator universe, weighted/unweighted lane, weight validity, and authority hashes first-class in any replacement schema.
7. Do not claim uncertainty preservation from counts/support tiers alone; explicitly govern survey-design uncertainty if terminal use requires it.
8. Hand the terminal-needed predicate subset to R04 and the materialization/compute choice to R05 rather than encoding either decision into R02's empirical sufficiency ruling.

## 14. Bottom line

The large V550 determinicity suite is not seven independent bodies of knowledge. Most of it is repeated interrogation of one empirical substrate. The information-loss court therefore favors **preserving the plural joint empirical fact and deleting duplicated ownership by analytical products**. The decisive correction is that the preserved fact must be richer than the current `indicator_answer_matrix`: pairwise correlations cannot stand in for the cross-conditioned historical world any more than scalar metrics can stand in for plural response distributions.
