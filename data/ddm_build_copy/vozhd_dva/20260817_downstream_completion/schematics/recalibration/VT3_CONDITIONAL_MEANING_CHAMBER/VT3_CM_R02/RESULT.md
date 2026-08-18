# VT3-CM-R02 — Conditional Information-Loss Court

**Cell:** `VT3-CM-R02`  
**Repository:** `maidiu/rawlsing`  
**Authorized branch:** `agent/vozhd-trii-vt3-cm-r02`  
**Exact launch base / repository head examined:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Production-code changes:** `NONE`  
**Mission:** Aggressively test whether V550's determinicity artifact suite contains irreducible terminal empirical value, identify the minimum lossless empirical fact, and determine which artifacts can become deterministic or diagnostic views. Downstream recreation was inspected only where needed to establish terminal necessity; VT3-CM-R03 owns the downstream-recreation court.

## 1. Governing law and evidence basis

The court directly inspected the binding governing spirit and the V550 implementations that create the named determinicity products. The Governing Spirit requires preservation of heterogeneity, contradiction, uncertainty, typed absence, provenance, replay, and structural constraint without converting population correlations into actor destiny. It simultaneously requires minimum sufficient machinery and rejects duplicated semantic ownership. The court therefore treated an artifact as irreducible only if deleting its materialization while preserving a smaller governed fact would destroy empirical distinctions, weighting semantics, uncertainty/support, admissibility, typed absence, provenance, or exact replay.

Direct evidence files and blob SHAs:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md` — `588cf3954c33417665c5f9bac04e8b27e75d7f7c`
- `data/ddm_build_copy/build_determinicity_repository_v550.py` — `afd2a59e1cdff0024a57acaf1dab8ff30534e565`
- `data/ddm_build_copy/ddm_v550_branching.py` — `8f6d40e0d016d66e5a3b334b31747eaef752873f`
- `data/ddm_build_copy/ddm_v550_metrics.py` — `e7675f4080bb30e6526027a34db747b7be7f85c9`
- `data/ddm_build_copy/ddm_v550_position_distribution.py` — `651329254244e9f42a8d88c2721ccae6bd768073`
- `data/ddm_build_copy/ddm_v550_clouds.py` — `dfc878e87d984a1a3d7000a0c726bdc444f9945f`
- `data/ddm_build_copy/ddm_v550_support.py` — `1b841139fee051b154dcccd52cd3d866b958dbb5`
- `data/ddm_build_copy/ddm_v550_distributions.py` — `43a62723b16f9c800ed7a6ef40a77e70a3f07377`
- `data/ddm_build_copy/ddm_v550_question_use.py` — `8d90a5116fd05b5db17e9b4645638a3aa6fc1131`

## 2. Final verdict

**VERDICT: `TARGET_HYPOTHESIS_SUBSTANTIALLY_SURVIVES_WITH_JOINT-STRUCTURE_CORRECTION`.**

The current V550 determinicity output surface contains substantially more stored analytical product than irreducible empirical information. `position_indicator_summary`, `outlier_cohort_summary`, `secondary_indicator_summary`, `recursive_branch_nodes`, and `branch_position_signature` are deterministic analytical products of a smaller empirical substrate plus versioned algorithm/authority rules. `indicator_answer_matrix` and `position_distribution` contain genuine empirical counts, but their materialized files do not own those facts if the underlying governed population/joint-response substrate remains available.

The strongest naive compression claim is false:

- `indicator_answer_matrix` is **not** the irreducible empirical core.
- a conditional-distribution object restricted to one position field at a time is **not** lossless.
- pairwise `P(response | position_field=value)` marginals do not preserve cross-indicator joint structure required by `secondary_indicator_summary` and recursive branching.
- question-conditioned distributions alone do not preserve the question-independent respondent population needed to recreate `position_distribution` exactly.

The minimum defensible empirical authority is a **governed joint empirical substrate** from which a canonical `CONDITIONAL_EMPIRICAL_DISTRIBUTION` view can be generated for arbitrary governed predicates, including conjunctions and typed missingness.

Court tokens:

- `V550_DETERMINICITY_SURFACE_HAS_IRREDUCIBLE_ARTIFACT_VALUE = MOSTLY_FALSE`
- `INDICATOR_ANSWER_MATRIX_IS_IRREDUCIBLE_CORE = FALSE`
- `PAIRWISE_CONDITIONAL_DISTRIBUTIONS_ARE_MINIMUM_SUFFICIENT = FALSE`
- `GOVERNED_JOINT_EMPIRICAL_SUBSTRATE_IS_MINIMUM_SUFFICIENT = PASS`
- `CONDITIONAL_EMPIRICAL_DISTRIBUTION_AS_CANONICAL_VIEW = PASS_WITH_JOINT_PREDICATE_AND_POPULATION_REQUIREMENTS`

## 3. Directly observed implementation evidence

### 3.1 Shared empirical substrate

`build_determinicity_repository_v550.py` constructs `branch_df = prepare_question_frame(df)` and feeds the same prepared per-question frame and weight series into `indicator_summary_rows`, `secondary_indicator_summary_rows`, `indicator_answer_matrix_rows`, `outlier_cohort_rows`, and `branch_nodes_rows`. This is direct evidence that these files are multiple projections/searches over a common empirical substrate rather than independently sourced empirical facts.

### 3.2 Fixed conditioning fields

`ddm_v550_branching.py` defines `INDICATOR_FIELDS` as exactly:

`sex`, `age_group`, `education_level`, `income_level`, `religion_label`, `urban_rural`, `region`, `ethnicity`, `language`, `employment`, `marital`, `household_size`.

### 3.3 `indicator_answer_matrix`

Direct observation from `indicator_answer_matrix_rows`:

- loops each available member of `INDICATOR_FIELDS`;
- excludes rows where the indicator is empty;
- emits one row for each observed `(indicator_name, indicator_value, response_value)` combination;
- carries `n_unweighted`, `pct_unweighted`, `n_weighted`, `pct_weighted`.

Weighted cells are sums of the weight series supplied by the V550 distribution builder; when no weight series exists, weighted values fall back to unweighted values.

**Inference:** the artifact is a family of one-indicator contingency tables. It creates no empirical information not already present in a joint respondent/question/position substrate. It is therefore a deterministic empirical view, not an irreducible fact.

### 3.4 `position_indicator_summary`

Direct observation from `indicator_summary_rows`:

- baseline entropy is computed from the full response vector;
- indicator-empty rows are removed before conditional entropy;
- if weights are present, baseline and conditional entropy use weights;
- `normalized_mutual_information` and `cramers_v` are nevertheless unweighted;
- the field named `mutual_information` is implemented as `max(0, baseline_entropy - conditional_entropy)`;
- confidence tier is a support heuristic (`usable` at 50 rows, otherwise `weak`).

`ddm_v550_metrics.py` confirms that entropy, conditional entropy, Cramér's V, NMI and dominant response are deterministic functions of the supplied empirical distributions.

**Inference:** these scalar summaries contain no irreducible empirical information. Exact replay does require preserving baseline universe, complete-case universe, weighting lane, metric implementation and version. When indicator missingness exists, the stored field named `mutual_information` can subtract entropies computed over different row universes; it is therefore an implementation-defined score, not a fact that should become semantic authority.

### 3.5 `outlier_cohort_summary`

Direct observation from `outlier_cohort_rows`:

- global baseline is the unweighted dominant response and share;
- every sufficiently supported `indicator=value` subgroup is visited;
- subgroup classification is `conforms`, `deviates`, or `minority_converges` according to dominant-response comparison;
- weights affect `n_weighted`, not the classification.

**Inference:** despite the artifact name, no statistical outlier test is performed. This is a deterministic subgroup-label view over baseline plus one-indicator conditional distributions and support authority.

### 3.6 `secondary_indicator_summary`

Direct observation from `secondary_indicator_summary_rows`:

- one-indicator candidate scores are calculated first;
- a primary indicator is selected by maximum `(mutual_information, cramers_v, n_unweighted)`;
- each candidate secondary is intersected with the primary and secondary nonmissing masks;
- joint support below 50 rows is skipped;
- a concatenated `primary||secondary` joint key is used to compute joint conditional entropy;
- `secondary_gain = max(0, primary_conditional_entropy - joint_conditional_entropy)`.

**Inference:** `secondary_gain` itself is deterministic, but recreating it requires cross-indicator joint response structure. Separate one-indicator `indicator_answer_matrix` tables are insufficient.

### 3.7 `recursive_branch_nodes`

Direct observation from `branch_nodes_rows`:

- recursion begins with all available `INDICATOR_FIELDS`;
- node entropy and dominant response are unweighted;
- each remaining indicator is evaluated greedily by conditional-entropy gain;
- the best positive-gain indicator is chosen;
- only the two most frequent values of the chosen indicator are recursed;
- default maximum depth is 3;
- branch support uses the shared wave-relative threshold rule;
- stop reasons include `pure_or_near_pure`, `max_depth`, `underpowered`, `no_remaining_indicators`, and `no_gain`.

**Inference:** the tree is a deterministic and deliberately truncated analytical projection. It loses minority configurations and cannot itself be the empirical core.

### 3.8 `branch_position_signature`

Direct observation from `build_position_signature_rows` in `ddm_v550_clouds.py`:

- candidates must be `POSITION_COORDINATE` fields and pass `allowed_as_branch_position_signature` authority;
- association stats use unweighted NMI and Cramér's V;
- `association_score` is `max(NMI, Cramér's V)`;
- candidates are ranked by score, support and name;
- at most five are emitted;
- rows are explicitly tagged `diagnostic_artifact=True`, `not_direct_evidence=True`, `evidence_role="diagnostic_position_signature"`, `artifact_status="enabled_diagnostic"`.

**Inference:** this artifact is already explicitly diagnostic. Its rank and scalar values are deterministic from pairwise contingencies plus authority and tie rules.

### 3.9 `position_distribution`

Direct observation from `ddm_v550_position_distribution.py`:

- operates from country respondent frames rather than one question's conditional table;
- builds a respondent slice deduplicated by available `(respondent_id, country_code)` keys;
- excludes empty position values and emits each field's marginal distribution;
- emits unweighted counts/shares;
- emits weighted counts/shares only when weight status is exactly `weighted`.

**Inference:** the artifact is a deterministic empirical population view, but it cannot be reconstructed from per-question conditional response distributions unless respondent-universe overlap or an explicit question-independent population-position fact is retained.

### 3.10 Weight semantics

Direct observation from `classify_weight_status` in `ddm_v550_metrics.py`:

- recognized states include `missing`, `invalid`, `unweighted_only`, `partial`, and `weighted`;
- partial weighting retains valid positive finite weight entries while leaving invalid entries unavailable;
- several weighted computations later coerce unavailable weight contributions to zero.

There is a lane asymmetry: question conditional machinery may calculate with a partial validated weight series while `position_distribution` emits weighted values only when status is exactly `weighted`.

**Inference:** weighted cell sums alone cannot preserve exact present behavior. Weight-validity/status state is nonnegotiable provenance.

### 3.11 Support semantics

Direct observation from `ddm_v550_support.py`:

- `DEFAULT_SUPPORT_RATE = 0.005`
- `DEFAULT_SUPPORT_CAP = 30`
- `DEFAULT_SUPPORT_FLOOR = 2`
- threshold is `ceil(total * 0.005)` bounded to `[2,30]`.

**Inference:** support and confidence labels are governed deterministic classifications rather than empirical primitives.

### 3.12 Response semantics and typed absence

Direct observation from `ddm_v550_distributions.py` shows distinct flags/states for substantive response, missing, DK, refusal, IAP, not asked, inapplicable and special response, with response-semantics status/source/contract hash.

**Inference:** a replacement representation that collapses these to generic null is semantically lossy even if substantive percentages remain identical.

### 3.13 Question-use and position authority

Direct observation from `ddm_v550_question_use.py`: the question-use contract separately governs permissions including `allowed_as_response_distribution`, `allowed_as_position_distribution`, `allowed_as_context_distribution`, `allowed_as_demographic_predictor`, `allowed_as_branch_splitter`, `allowed_as_branch_position_signature`, `allowed_as_branch_relation_cosignature`, `allowed_as_attitude_cloud_anchor`, `allowed_as_attitude_cloud_feature`, `allowed_as_v551_relation_evidence`, and `allowed_as_parent_prior_coordinate`. The contract hash surface also includes `position_conditioning`, `position_modifiers`, `conditional_strata_weights` and related authority metadata.

**Inference:** compression may remove duplicated copies of authority metadata, but it must preserve immutable authority/provenance references sufficient to recover exact governing semantics.

## 4. A. Dependency / derivability table

| Artifact | Exact input information | New stored product | Smaller-fact derivability | Required exact-replay authority | Court disposition |
|---|---|---|---|---|---|
| `indicator_answer_matrix` | response rows; each present indicator; optional weights; question metadata | pairwise `(indicator,value,response)` counts/percentages | **YES** from governed joint empirical fact | indicator missingness, response normalization, weight lane, authority | deterministic empirical view |
| `position_indicator_summary` | response/position rows + weights | entropy, implementation-defined MI, NMI, Cramér's V, uplift, dominant response/support labels | **YES**, not always from matrix alone | unconditional baseline, indicator-complete mask, weight rules, metric version | diagnostic metric view |
| `outlier_cohort_summary` | baseline response distribution + supported indicator subgroups | subgroup branch labels and dominant responses | **YES** | support rule and unweighted classification rule | diagnostic cohort view |
| `secondary_indicator_summary` | all candidates + response + joint completeness | primary selection, joint entropy, `secondary_gain` | **YES from joint fact; NO from pairwise matrix** | two-field conjunctions, missingness, weights, support/tie rules | diagnostic joint-association view |
| `recursive_branch_nodes` | response + all available indicators + algorithm parameters | greedy truncated tree | **YES from joint fact; NO from pairwise matrix** | arbitrary conjunctions, candidate order, support, depth, top-two rule, ties | diagnostic-only lossy view |
| `branch_position_signature` | response + authority-permitted position fields | top-five ranked association signature | **YES** | contract gating, unweighted metrics, ranking/ties | diagnostic-only view |
| `position_distribution` | question-independent respondent population + positions + weights | population position marginals | **YES from respondent-position base; NO from question CED alone** | respondent identity/dedupe, missingness, weight-status policy | deterministic empirical population view |

## 5. B. Minimum sufficient empirical fact candidate

The court's minimum sufficient candidate is a normalized governed joint substrate, conceptually `GOVERNED_JOINT_EMPIRICAL_SUBSTRATE` / `GOVERNED_EMPIRICAL_OBSERVATION`.

Required information domains:

1. **Survey identity:** source, source family, raw wave, canonical wave, country.
2. **Population identity:** respondent identity or a losslessly equivalent population-overlap key.
3. **Question/response identity:** question ID and exact normalized response category/state.
4. **Typed absence:** separate missing/DK/refusal/IAP/not-asked/inapplicable states where governed.
5. **Joint conditioning state:** all governed position coordinates for the respondent with typed present/absent state.
6. **Sampling state:** raw/validated weight and weight-validity status; survey-design fields where statistical uncertainty must be preserved.
7. **Authority references:** question-use, response semantics, position-conditioning, source-structure, normalization/transformation versions.
8. **Provenance:** source dataset/file and immutable extraction/build identity.

This can be physically normalized into a respondent-position relation plus a respondent-question-response relation. The essential property is that lawful respondent overlap and cross-position joint structure remain reconstructable.

The canonical empirical interface can then be:

`CONDITIONAL_EMPIRICAL_DISTRIBUTION(question, survey_scope, governed_predicate, response_state, counts/support, denominator_scope, authority/provenance)`.

The predicate grammar must support:

- unconditional `TRUE`;
- singleton predicates such as `income_level=low`;
- conjunctions such as `income_level=low AND education_level=secondary`;
- deeper conjunctions sufficient to replay any retained recursive query;
- typed-missing predicates where governed.

A CED restricted to singleton predicates is not lossless.

If respondent-indexed facts are prohibited, an aggregate-only representation must materialize every governed conjunction any retained computation may query, plus question-independent population-position distributions and explicit overlap/denominator semantics. This risks combinatorial materialization and may cease to be physically smaller even though it is semantically cleaner.

## 6. C. NONNEGOTIABLE fields / distinctions for losslessness

1. `source`, `source_family`, raw wave, canonical wave, country, question identity.
2. Respondent/population overlap identity, or a losslessly equivalent governed joint key.
3. Exact response category plus response-semantics authority.
4. Typed absence: missing, DK, refusal, IAP, not asked, inapplicable, etc.
5. Jointly recoverable position values, not only one-position marginals.
6. `n_unweighted` and weighted support as separate lanes.
7. Weight-validity/status state; aggregate `sum(weight)` alone is insufficient.
8. Explicit denominator universe/scope: all response rows, indicator-complete rows, joint-complete rows, respondent population, weighted-valid population.
9. Unconditional baseline response distribution (`predicate=TRUE`).
10. Question-independent population-position scope sufficient to recreate `position_distribution`.
11. Immutable authority/provenance references and transformation/compiler version.
12. PSU/stratum/replicate-weight sufficient information if design-based statistical uncertainty is a required preserved meaning.
13. Versioned view/compiler rules for exact recreation of current diagnostics: candidate order, metric lane, support threshold, branch depth, top-K branching, tie behavior, confidence rules and numeric policy.

Items 13 are compiler authority, not empirical fields; they should not be duplicated into every empirical cell.

## 7. D. Artifacts that can become deterministic views

All seven named artifacts can become deterministic views if the strengthened governed joint substrate is authoritative:

- `indicator_answer_matrix` — canonical pairwise conditional-distribution view.
- `position_distribution` — canonical population-position marginal view.
- `position_indicator_summary` — deterministic metric view.
- `outlier_cohort_summary` — deterministic cohort-classification view.
- `secondary_indicator_summary` — deterministic joint-association view.
- `recursive_branch_nodes` — deterministic greedy-tree diagnostic view.
- `branch_position_signature` — deterministic ranked-association diagnostic view.

This does **not** mean all seven have equal semantic status. `indicator_answer_matrix` and `position_distribution` expose empirical counts; the others are analytical projections. What disappears is independent semantic ownership by each materialized artifact.

## 8. E. Artifacts that should be diagnostic-only

- `position_indicator_summary`: scalar associations useful for analysis and QA, dangerous as actor-level priors.
- `outlier_cohort_summary`: supported subgroup comparison, not independent evidence.
- `secondary_indicator_summary`: useful for detecting conditional heterogeneity, dangerous if reified into synthetic pseudo-types.
- `recursive_branch_nodes`: strongest diagnostic-only candidate because it greedily selects and truncates a search tree and drops non-top-two branch values from recursion.
- `branch_position_signature`: already explicitly marked diagnostic and not direct evidence in code.

## 9. F. Deletion that would cause genuine semantic loss

If the governed joint substrate described above survives, **none of the seven named files is itself irreducible**. Their stored materializations can be removed and regenerated exactly under frozen authority/compiler rules.

If, however, the replacement is only pairwise `CONDITIONAL_EMPIRICAL_DISTRIBUTION(question, X=x, response, counts...)`, deletion is **not lossless**. It would lose:

1. cross-indicator joint structure needed for secondary and recursive conditioning;
2. baseline/missingness structure unless unconditional `TRUE` and typed missingness are represented;
3. respondent overlap across questions needed for the question-independent population view;
4. design-based sampling uncertainty if survey-design sufficient information is discarded;
5. weight-validity topology if only weighted totals are retained.

Retaining `secondary_indicator_summary` or `recursive_branch_nodes` does not repair that loss: both are lossy summaries of the missing joint structure. A fitted tree is not a substitute for the population that generated it.

## 10. G. Hostile counterexamples against the minimal representation

### CE-1 — Same pairwise matrices, different joint conditional reality

Construct binary response `Y` and binary positions `A`, `B` such that two populations have identical `A×Y` and `B×Y` tables but different `A×B×Y` assignments. The one-indicator `indicator_answer_matrix` is identical, yet `P(Y|A,B)`, secondary gain after conditioning on a primary indicator, and deeper recursive nodes differ. Therefore pairwise CED does not identify the joint empirical state.

### CE-2 — Same matrix, different unconditional baseline through position missingness

Hold all observed `X×Y` cells fixed. Add equal numbers of respondents with `X` missing, assigning their `Y` responses differently between two datasets. `indicator_answer_matrix` remains identical because empty `X` is excluded, but global `P(Y)`, baseline entropy, dominant response and uplift differ. Matrix-only reconstruction fails.

### CE-3 — Same per-question distributions, different `position_distribution`

Let two questions each have the same 50/50 position distribution. In population P the same 100 respondents answer both; in population Q the two questions are answered by disjoint 100-person groups. Every per-question CED can match, but the deduplicated respondent population is 100 versus 200. Question-conditioned distributions cannot recover population overlap.

### CE-4 — Same weighted counts, different unweighted support

Ten respondents each weighted 10 and one hundred respondents each weighted 1 can yield the same weighted cell totals. Unweighted support, NMI/Cramér's-V inputs, recursive support eligibility and confidence differ. Weighted counts alone are insufficient.

### CE-5 — Same weighted/unweighted totals, different weight-status topology

Two cells can share the same `n_unweighted` and total weighted sum while one population has all valid weights and another has partial/invalid weights whose valid entries numerically compensate. V550 lane behavior differs because weight status affects admissibility and `position_distribution` weighted emission. Counts without weight-validity state cannot exactly replay the suite.

### CE-6 — Refusal versus not-asked

Two populations can have identical substantive response counts while twenty non-substantive observations are refusals in one and `not_asked` in another. Collapsing both to NULL preserves percentages but destroys lawful absence semantics and admissibility.

### CE-7 — Same cell counts, different design-based uncertainty

Two surveys can have identical response counts, conditional counts, `n_unweighted` and weighted totals while one difference is dispersed across PSUs and the other concentrated in a single cluster/stratum. Point estimates match; design-based uncertainty does not. A counts-only CED cannot truthfully claim to preserve uncertainty.

### CE-8 — Recursive tree suppresses a minority configuration by construction

Give a selected split indicator six values and place a substantively extreme response distribution in the sixth-most-common category. Because `branch_nodes_rows` recurses only into the two most frequent values, the stored recursive tree can remain unchanged while the minority configuration changes radically. The tree is therefore demonstrably lossy relative to its source population.

## 11. Special-court rulings

### Proposition: `indicator_answer_matrix` is the irreducible empirical core

**FALSIFIED.** It is a useful canonical pairwise view but insufficient as a lossless fact base.

### Proposition: a cleaner `CONDITIONAL_EMPIRICAL_DISTRIBUTION` can replace it

**YES, with qualification.** It can replace the matrix as the canonical empirical interface only if it is backed by or contains sufficient joint structure, unconditional baseline scope, typed absence, weighted and unweighted support, weight-status authority, population overlap, and immutable provenance/authority. Singleton predicates alone are insufficient.

### MI, conditional entropy, Cramér's V

**No irreducible empirical information.** They are deterministic functions of the relevant contingency distributions plus exact missingness/weight/algorithm policy.

### Outlier status

**No irreducible empirical information.** Current status is deterministic supported-subgroup dominant-response classification.

### Secondary gain

**No irreducible empirical information, but it requires irreducible joint structure.** It cannot be regenerated from one-indicator marginals.

### Recursive branch tree

**No irreducible empirical information.** It is a deterministic, bounded, truncated greedy traversal and is itself lossy.

## 12. Unresolved questions

1. **Terminal demand for higher-order joint conditioning:** R02 establishes that pairwise CED is insufficient to reproduce current secondary/tree analyses. It does not establish that terminal architecture actually requires every current secondary/tree query. R03/R06/R00 must decide the required maximum predicate order, if any.
2. **Survey-design uncertainty authority:** current inspected V550 determinicity artifacts primarily preserve counts/support heuristics, not a complete design-based variance representation. If future terminal meaning includes statistical uncertainty rather than only support strength, the parent architecture must decide what PSU/stratum/replicate-weight sufficient information is canonical.
3. **Partial-weight semantics:** present artifact families do not use partial weights uniformly. Parent architecture should decide whether exact compatibility with this asymmetry is required or whether a later authority lawfully supersedes it.
4. **Respondent-level storage versus aggregate closure:** R02 establishes the information requirement, not the physically optimal storage layout. An aggregate conjunction cube can be lossless only over its governed predicate closure; unrestricted future conjunctions favor respondent/joint storage.
5. **Exact byte replay versus semantic replay:** deterministic regeneration of semantic values is established in principle; byte-identical ordering/serialization requires additional frozen storage-format rules if that is a terminal requirement.

No unresolved question rescues scalar metrics, ranked signatures, outlier labels or recursive trees as irreducible empirical facts.

## 13. Recommended parent actions

1. Reject `indicator_answer_matrix` as the canonical irreducible core.
2. Reject any replacement CED whose predicate grammar is singleton-only.
3. Adopt a governed joint empirical substrate as the source of truth, with conditional distributions as canonical empirical views.
4. Preserve typed absence, weighted/unweighted lanes, explicit denominator scope, weight-status authority and provenance.
5. Preserve an explicit question-independent population-position lane or respondent overlap sufficient to regenerate `position_distribution`.
6. Move scalar association metrics, outlier labels, secondary gain, recursive trees and position signatures behind diagnostic/view status unless another authority proves terminal necessity.
7. Do not convert any correlation or branch into actor belief, identity or deterministic persona state.
8. Resolve survey-design uncertainty requirements before claiming a compressed representation preserves uncertainty.
9. Let R03 determine whether any conditional meaning is independently recreated downstream; do not infer downstream equivalence from similar field names.

## 14. Bottom line

The large V550 determinicity suite is not seven independent bodies of knowledge. Most of it is repeated interrogation of one empirical substrate. The information-loss court therefore favors **preserving the plural joint empirical fact and eliminating duplicated semantic ownership by analytical products**. The decisive correction is that the preserved fact must be richer than the current `indicator_answer_matrix`: pairwise correlations cannot stand in for the cross-conditioned empirical world any more than scalar metrics can stand in for plural response distributions.
