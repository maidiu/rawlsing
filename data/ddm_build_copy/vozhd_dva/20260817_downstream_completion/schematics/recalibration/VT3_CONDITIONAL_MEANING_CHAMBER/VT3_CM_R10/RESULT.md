# VT3-CM-R10 — Conditional Weighting, Support & Uncertainty Authority Court

**Court:** VT3-CM-R10  
**Repository:** `maidiu/rawlsing`  
**Exact base audited:** `8c87f7725ba58202b5377c974548140420709fa9`  
**Intended branch:** `agent/vozhd-trii-vt3-cm-r10`  
**Jurisdiction:** conditional weighting, observed support, denominator semantics, survey-design sampling uncertainty, epistemic uncertainty, noncomparability, missing authority, and downstream admissibility.

## Disposition

Rawlsing currently possesses **descriptive conditional sample evidence**, not design-based survey inference.

Its lawful empirical primitives are stronger than a bare percentage and weaker than a confidence interval. The current V550→V552 path can know, depending on artifact lane:

- the observed unweighted row count;
- the weighted mass produced by a single governed respondent-level primary weight;
- the raw and weighted descriptive shares;
- an aggregate weight state (`weighted`, `partial`, `invalid`, `missing`, or the exceptional `unweighted_only`);
- the total respondent count used to derive a wave-relative support threshold;
- support states such as `zero_support`, `underpowered`, `sufficient_support`, `missing_support`, and structural-lane `not_applicable`;
- V551 evidence-lane admissibility separately from observed support;
- V552 measurement-evidence and downstream-permission states separately from the numerical pressure score.

It does **not** carry a governed survey-design variance substrate through the canonical conditional-evidence path. The respondent-facing substrate carries one selected scalar primary weight, but no governed PSU identifier, sampling-stratum identifier, replicate-weight vector, BRR/Fay/jackknife design specification, or variance-estimation rule. Therefore current Rawlsing cannot lawfully emit a design-based standard error, margin of error, confidence interval, design effect, or effective sample size from these artifacts.

A lossless replacement conditional fact must therefore preserve the **observed evidence and its qualification**, not invent inferential precision. In particular, it must preserve raw support independently of weighted mass; weighted numerator and denominator independently of raw numerator and denominator; weight-state/provenance independently of weighted numerical totals; crosstab-completion zero independently of missing observation or missing authority; and stored evidence independently of downstream permission.

A second governing conclusion is equally important: **current V550 does not implement one uniform weighted lane.** `answer_distribution`, `country_answer_distribution`, and branching computations can use the positive finite subset of a `partial` weight series, while `position_distribution` suppresses weighted output unless the entire respondent slice classifies exactly as `weighted`. V552, when presented with component percentages, will consume `pct_weighted` for `partial` weight status so long as the vector is complete and nonnegative; it rejects weighted use for statuses containing `missing`, `unavailable`, `invalid`, `unweighted_only`, or `not_weighted`. Any replacement must make the selected weight basis explicit rather than infer it from the presence of a numeric `n_weighted` or `pct_weighted` field.

---

# A. Current semantics ledger

## A1. Governed respondent weighting substrate

`apply_postgres_facet_ready_substrate.py` establishes the operational weight substrate.

`survey_weight_fact` stores one or more respondent-level weights with:

- `respondent_id`
- `weight_name`
- `weight_value`
- `weight_type`
- `source_var`
- `source`
- `wave`
- `is_primary`
- `notes`

The facet-ready view selects **one primary weight per respondent** and carries:

- `weight_value`
- `weight_name`
- a coarse substrate status:
  - `weighted_available` when a selected weight value is non-null;
  - `unweighted_no_weight_detected` otherwise.

The same file contains explicit GSS and LiTS weight allowlists and source/wave-specific primary-weight ordering. This is weighting authority: Rawlsing does not discover an arbitrary codebook field containing the token “weight”; it selects from governed candidates and marks a single primary respondent scalar.

That substrate does not itself carry a design-variance specification.

## A2. V550 weight validation semantics

`ddm_v550_metrics.py::classify_weight_status(series)` converts a respondent weight series into an aggregate status and, where possible, a validated positive finite series.

Exact state semantics:

| State | Exact current meaning | Validated series returned? |
|---|---|---:|
| `missing` | no series, zero-length series, or no numeric usable weight information | no |
| `invalid` | no positive finite usable weight and the numeric content is nonpositive/invalid as classified by the function | no |
| `unweighted_only` | exceptional no-valid-weight state not classified as wholly missing/nonpositive | no |
| `partial` | at least one positive finite weight exists, but fewer than all rows have a positive finite weight | yes, with unusable rows null |
| `weighted` | every row has a positive finite weight | yes |

A `partial` series is therefore **not** a completed or imputed weight vector. Its unusable rows remain absent from weighted mass. Where downstream code coerces the validated series and fills null with `0.0`, those rows contribute to the raw lane and contribute zero weighted mass.

## A3. Answer distributions

`ddm_v550_distributions.py::build_distribution_tables` computes `answer_distribution` and `country_answer_distribution`.

For each response category in the supplied question frame:

- `n_unweighted` is the number of observed rows in the category;
- `n_weighted` is the sum of the validated positive finite respondent weights in that category when a validated series exists;
- `pct_unweighted` is the category row count divided by the total row count in the relevant frame;
- `pct_weighted` is the category weighted mass divided by total usable weighted mass in the relevant frame;
- `weight_status` is the aggregate status returned by `classify_weight_status`.

Because `partial` returns a validated series, these answer-distribution lanes can compute a weighted estimate from only the valid-weight subset. Missing/invalid rows remain present in `n_unweighted` but carry zero weighted mass.

When no validated weight series exists, `n_weighted`/`pct_weighted` are absent rather than a lawful weighted estimate.

## A4. Position distribution

`ddm_v550_position_distribution.py::build_position_distribution_rows` has stricter behavior.

It first deduplicates the respondent slice by respondent/country where possible. For each nonblank position field, it classifies the respondent weight series, but then sets:

`validated_weights = weight_series if weight_status == "weighted" else None`

Therefore:

- `weighted` → weighted position prevalence is computed;
- `partial` → weighted position prevalence is suppressed;
- `invalid`, `missing`, `unweighted_only` → weighted position prevalence is suppressed.

This is a real lane difference. A future replacement must not silently reinterpret an historically suppressed partial-weight position estimate as though V550 had emitted it.

## A5. Branching / conditional crosstab lane

`build_determinicity_repository_v550.py` takes the `weights` object returned by `build_distribution_tables` and passes it into:

- `indicator_summary_rows`
- `secondary_indicator_summary_rows`
- `indicator_answer_matrix_rows`

Thus a `partial` validated series **does** reach branching computations.

`ddm_v550_branching.py::indicator_answer_matrix_rows` constructs:

- an unweighted crosstab of indicator value × response value;
- a weighted pivot using the validated series when one exists.

Within each indicator value:

- `pct_unweighted = cell raw count / raw count across all response columns for that indicator value`;
- `pct_weighted = cell weighted mass / weighted mass across all response columns for that indicator value`.

When `weights is None`, the code sets `weighted_ct = unweighted_ct.astype(float)`. Therefore `n_weighted` and `pct_weighted` numerically mirror the raw lane even though no lawful weighted estimate exists. Those fields are **not self-authenticating**. The accompanying `weight_status` and an explicit weight-basis state are indispensable.

## A6. Support semantics

`ddm_v550_support.py` defines the current general support formula.

Defaults:

- support rate: `0.005`
- floor: `2`
- cap: `30`

For a valid positive `total_respondents`:

`threshold = min(30, max(2, ceil(total_respondents * 0.005)))`

If total respondent count is unavailable/nonpositive, the threshold defaults to the cap, `30`.

`support_status_from_count` then returns:

- structural lane + missing support count → `not_applicable`;
- nonstructural lane + missing support count → `missing_support`;
- support count `<= 0` → `zero_support`;
- positive support below threshold → `underpowered`;
- support at or above threshold → `sufficient_support`.

Accordingly, `underpowered` does **not** mean “n < 2” and does **not** mean “statistically insignificant.” It means: **positive observed support below the current wave-relative support threshold**.

Example thresholds:

- total respondents 100 → threshold 2;
- total respondents 1,000 → threshold 5;
- total respondents 3,000 → threshold 15;
- total respondents 10,000 → threshold 30 because of the cap.

The code also contains support-derived “confidence” labels. These are heuristic support/readiness labels, not design-based confidence levels and not confidence intervals.

## A7. V551 admission

`ddm_v550_bridge.py` explicitly separates support status from evidence-lane usability.

For `direct_relation_response`, `usable_for_evidence` accepts support status:

- `sufficient_support`
- `supported`
- `underpowered`

For `derived_determinicity`, evidence is usable only when:

- `support_status == "sufficient_support"`

Thus a positive small-n direct observed response may remain evidence, while a derived crosstab/determinicity object with the same support classification is denied derived-evidence promotion.

This is binding evidence that **storage/preservation and downstream admission are different questions**.

`zero_support`, missing support, structural context, audit quarantine, and disabled lanes are not equivalent to underpowered positive observation.

## A8. V552 weight basis and evidence state

`ddm_v552_structural.py::select_v552_distribution_weight_basis` chooses, in order:

1. `pct_weighted`, if every component has a non-null nonnegative value, total mass is positive, and no component `weight_status` contains:
   - `missing`
   - `unavailable`
   - `invalid`
   - `unweighted_only`
   - `not_weighted`
2. otherwise `pct_unweighted`, if complete/nonnegative/positive;
3. otherwise normalized `n_unweighted`, if complete/nonnegative/positive;
4. otherwise no usable distribution basis.

`partial` is **not** in V552's weighted-status exclusion list. Therefore a complete `pct_weighted` vector carrying `weight_status=partial` can be selected as V552's pressure weighting basis.

V552 separately records:

- `measurement_evidence_status`
- `downstream_permission_status`
- `pressure_score_status`
- unresolved mass
- selected-surface completeness
- the actual `distribution_weight_basis`.

Where V551 repair debt exists, V552 uses `APPLICABLE_BUT_UNRESOLVED` and denies downstream pressure linkage. Where no applicable evidence exists, it records `NO_APPLICABLE_EVIDENCE`. A computed score is `OBSERVED_ZERO` or `OBSERVED_NONZERO`.

The V552 `component_signed_intensity_std`, directional entropy, and polarization fields describe **dispersion within the selected response surface**. They are not survey-design sampling variance estimates.

---

# B. Weighting-state machine

## B1. State transition at V550 validation

Input respondent weight series:

1. **No series / empty / all absent**
   → `missing`
   → no validated weighted lane.

2. **No positive finite usable values; classified nonpositive/invalid**
   → `invalid`
   → no validated weighted lane.

3. **Exceptional no-valid-weight state outside the preceding classes**
   → `unweighted_only`
   → no validated weighted lane.

4. **Some but not all rows have positive finite weights**
   → `partial`
   → validated series contains usable positive finite weights and null for unusable rows.

5. **All rows have positive finite weights**
   → `weighted`
   → complete validated series.

## B2. Artifact-specific consequences

| V550/V552 lane | `weighted` | `partial` | `invalid` / `missing` / `unweighted_only` |
|---|---|---|---|
| answer distribution | use weighted | use valid subset | weighted fields absent |
| country answer distribution | use weighted | use valid subset | weighted fields absent |
| indicator/secondary metrics | use weighted | use valid subset | raw-only computation |
| indicator-answer matrix | use weighted | use valid subset | raw matrix mirrored into numerically named weighted columns |
| position distribution | use weighted | **suppress weighted output** | suppress weighted output |
| V552 basis selection | accept complete `pct_weighted` | **accept complete `pct_weighted`** | reject weighted vector and fall back raw if available |

Therefore a replacement cannot represent weighting with only `n_weighted` and `pct_weighted`. It must carry a status/basis contract.

## B3. Minimum lawful distinction among weight defects

Current aggregate V550 semantics distinguish `partial`, `invalid`, and `missing`, but a compact conditional fact that replaces respondent-level substrate should preserve more than the aggregate token if exact future reconstruction matters.

At minimum preserve:

- number of raw rows in the estimator domain;
- number of rows carrying a positive finite usable weight;
- number with missing weight;
- number with present-but-invalid/nonpositive/nonfinite weight;
- aggregate `weight_status`;
- selected weight name/source variable and authority provenance;
- sum of usable weights.

Without these counts, two `partial` cells with radically different weight coverage become observationally indistinguishable once respondent microdata is discarded.

---

# C. Denominator contract

A percentage is meaningless unless its denominator grain survives.

## C1. `answer_distribution`

For a question frame:

`pct_unweighted(response=r) = rows(response=r) / all rows in the supplied question frame`

`pct_weighted(response=r) = usable positive weight mass(response=r) / usable positive weight mass across the supplied question frame`

A partial-weight estimate therefore has a raw denominator containing rows that may contribute no weighted mass.

## C2. `country_answer_distribution`

Same formulas, but the denominator is restricted to the current country slice.

## C3. `indicator_answer_matrix`

For a given indicator field/value pair:

`pct_unweighted(response=r | indicator=v) = cell raw rows / all response rows for indicator=v`

`pct_weighted(response=r | indicator=v) = cell weighted mass / all response weighted mass for indicator=v`

Rows with blank indicator value are excluded before the crosstab.

If no validated weight series exists, the current implementation mirrors raw counts and raw percentages into the fields named `n_weighted` and `pct_weighted`. The denominator contract therefore requires a separate basis/status field.

## C4. `position_distribution`

This is a prevalence distribution of the position coordinate itself, not a response conditional.

Within each country and position field:

`pct_unweighted(position=v) = deduplicated respondents with nonblank field and value v / deduplicated respondents with any nonblank value for that field`

When and only when the whole respondent slice is `weighted`:

`pct_weighted(position=v) = usable weight mass at value v / usable weight mass among respondents with a nonblank value for that position field`

## C5. Diagnostic dominant-response percentages

`position_indicator_summary` and `secondary_indicator_summary` do not provide a clean independent pair of raw and weighted percentages. The implementation calculates a single baseline dominant-response share using whichever lane was passed and writes that value into both `dominant_response_pct_unweighted` and `dominant_response_pct_weighted`.

Those duplicate-named fields are diagnostic implementation evidence, not a trustworthy dual-lane denominator contract. A replacement conditional-fact architecture should preserve the underlying empirical counts/distribution and weight basis rather than canonize this naming accident.

## C6. Required denominator primitives in a replacement

For every conditional estimate, preserve:

- `cell_n_unweighted`
- `denominator_n_unweighted`
- `cell_weight_sum` nullable
- `denominator_weight_sum` nullable
- `weight_basis_status`
- exact conditioning grain
- exact response-surface grain

Percentages are then reconstructible. The percentages themselves need not be canonical if these primitives and their authority/provenance are immutable.

---

# D. Observed support versus survey-design sampling uncertainty versus epistemic uncertainty

These are different authorities and must never collapse.

## D1. Observed sample support

Observed sample support answers:

> How many rows/respondents actually support this empirical cell under the current evidence grain?

Current principal primitive: `n_unweighted`, qualified by `n_respondents` and the support formula.

It can support a lawful statement such as:

> “This conditional cell has 3 observed rows in a question with 1,000 respondents and is classified `underpowered` because the threshold is 5.”

It cannot support:

> “There is a 95% chance the population value lies in this interval.”

## D2. Weighted descriptive estimate

The weighted estimate answers:

> Under the selected respondent weight and this artifact's weighting policy, what share of usable weighted mass lies in this response cell?

It is a descriptive weighted estimator produced from the selected scalar weight. It does not become design-based inference merely because it is weighted.

## D3. Weight-quality state

Weight-quality state answers:

> Was the relevant respondent weight series complete and usable?

This is represented imperfectly but materially by `weighted`, `partial`, `invalid`, `missing`, `unweighted_only`, plus the actual numerical weighted mass.

Weight-quality defect is not survey-design sampling uncertainty.

## D4. Survey-design sampling uncertainty

Survey-design sampling uncertainty asks:

> Given the sample design, what sampling variance should attach to the weighted estimator?

Current V550→V552 does not have the required governed machinery. The canonical path carries a selected scalar primary weight, but no complete design-variance authority containing PSU, sampling stratum, replicate weights, and the appropriate estimator specification.

Therefore no current support label, `confidence_tier`, weighted count, entropy, response-surface standard deviation, or V552 dispersion metric may be re-described as a sampling standard error or confidence interval.

## D5. Epistemic uncertainty

Epistemic uncertainty concerns whether Rawlsing possesses authority to say what a datum means or whether it is comparable/applicable at all.

Examples already recognized in the architecture/governing law include:

- missing support;
- not applicable;
- missing authority;
- unresolved mapping;
- noncomparability;
- repair debt;
- unknown response-category coverage;
- denied downstream permission;
- forbidden inference.

This axis must remain independent from observed sample support. A high-n cell can still lack semantic authority; a low-n cell can still be a real historical observation.

---

# E. Exact survey-design sampling-uncertainty capability currently supported

## E1. What Rawlsing can lawfully state

Current Rawlsing can state:

1. the raw observed count;
2. the respondent total used by the support formula;
3. the support threshold and support class;
4. the selected scalar-weight status;
5. the weighted mass where the relevant artifact law permits it;
6. the raw and/or weighted descriptive proportion;
7. whether V551/V552 has admitted, denied, or left unresolved a downstream use;
8. whether the response surface is complete under V551/V552's own component-conservation rules;
9. descriptive within-surface dispersion/orientation metrics where computed.

The strongest lawful statistical qualification is therefore:

> **A descriptive sample estimate with explicit raw support, selected-weight basis, weight-completeness state, and support/admissibility qualification; no design-based sampling interval is available from the current governed substrate.**

## E2. What Rawlsing cannot lawfully state

Current Rawlsing cannot derive from this path:

- survey-design standard error;
- survey-design variance;
- 90/95/99% design-based confidence interval;
- margin of error;
- design effect;
- effective sample size;
- finite-population correction;
- cluster-robust survey variance;
- replicate-weight variance;
- BRR/Fay/jackknife/bootstrap survey variance;
- population probability that a generated actor holds the measured response.

The repository may contain source-native material outside this path, but the operative V550 conditional substrate does not propagate a governed design specification sufficient for these calculations. Source possession somewhere in an archive is not equivalent to current conditional-evidence authority.

---

# F. Forbidden claims

The following claims are forbidden on current authority:

1. **“Weighted percentage = population truth.”**  
   A weighted descriptive share is not automatically a design-unbiased population estimate, and no current design-variance machinery licenses inferential precision.

2. **“Underpowered = statistically insignificant.”**  
   `underpowered` is a deterministic support-threshold label based on positive raw support below a wave-relative threshold.

3. **“Sufficient support = statistically significant/reliable at 95%.”**  
   `sufficient_support` crosses a support gate only.

4. **“Confidence tier = confidence level.”**  
   Current “confidence” labels are heuristic support/readiness classifications.

5. **“n_weighted is a respondent count.”**  
   It may be a sum of respondent weights. In the no-weight branching fallback it can also merely mirror raw count.

6. **“A numeric pct_weighted proves weighted estimation occurred.”**  
   The branching matrix may populate weighted-named fields from the raw crosstab when no validated weights exist.

7. **“Partial weighting is one stable machine-wide policy.”**  
   It is consumed in some V550/V552 lanes and suppressed in `position_distribution`.

8. **“Zero crosstab cell = structural impossibility.”**  
   Current zero cells can be completion cells generated from observed marginal categories. No structural-zero authority is encoded.

9. **“No row = zero.”**  
   Missing observation, missing authority, not-applicable evidence, and an observed/completed zero are different states.

10. **“V552 component standard deviation = sampling standard error.”**  
    It is response-surface dispersion.

11. **“A weighted conditional response distribution is an actor belief probability.”**  
    Governing spirit forbids turning population/group-conditioned evidence directly into psyche, identity, or destiny.

12. **“Pressure admission authorizes evidence deletion.”**  
    A historically observed but nonpromotable cell remains evidence/provenance even when a derived pressure use is denied.

---

# G. Minimum replacement conditional fact

The smallest lossless replacement should store primitives and authority states, not every derived V550 diagnostic artifact.

## G1. Identity and grain — mandatory

- `source`
- `source_family`
- `canonical_wave`
- `country_code` / governed analysis scope
- `question_id`
- `var_code`
- response identity (`response_value_normalized` plus response-semantics contract identity)
- condition identity:
  - `position_field`
  - `position_value`
  - and/or governed canonical condition signature/path
- empirical distribution/fact identifier
- semantic role / evidence lane

## G2. Raw empirical support — mandatory

- `cell_n_unweighted`
- `denominator_n_unweighted`
- `question_n_respondents` used for the support formula
- `support_threshold`
- `support_status`
- `support_formula_id`
- `support_formula_version`

This prevents equal weighted totals from erasing radically different observed support.

## G3. Weighting primitives — mandatory when a weight authority exists

- `weight_name`
- `weight_source_var`
- `weight_authority_id` or equivalent provenance
- aggregate `weight_status`
- `usable_weight_row_n`
- `missing_weight_row_n`
- `invalid_weight_row_n`
- `cell_weight_sum`
- `denominator_weight_sum`
- explicit `weight_basis_status`, e.g.:
  - `weighted_complete`
  - `weighted_partial_valid_subset`
  - `weighted_suppressed_partial`
  - `unweighted_fallback`
  - `weight_invalid`
  - `weight_missing`
- weighting/calculation policy version

The three row-quality counts are required if respondent-level microdata is no longer retained and future reconstruction must distinguish mild from severe partiality rather than merely replay the aggregate token `partial`.

## G4. Zero / absence state — mandatory

A replacement must carry a typed state such as:

- `observed_positive`
- `crosstab_completion_zero`
- `observed_zero` where a zero-valued measurement is itself observed and authoritative
- `no_observation`
- `missing_authority`
- `not_applicable`
- `noncomparable`
- `unresolved`

**Do not introduce `structural_zero` unless a separate authority actually establishes impossibility. Current V550 crosstab zeros do not.**

## G5. Survey-design sampling-uncertainty authority — mandatory negative state

Until a future governed design substrate exists, carry an explicit status such as:

`survey_design_variance_status = "not_available_in_current_governed_substrate"`

Do not leave a blank that a downstream stage could reinterpret as “not yet calculated despite available authority.”

If a later source genuinely supplies governed PSU/stratum/replicate/design metadata, that must be admitted by a separate authority and versioned variance method; R10 does not authorize inventing it.

## G6. Epistemic/comparability state — mandatory

- semantic authority status
- comparability status and reason
- missing-authority status/reason
- response-surface completeness / unresolved mass where applicable
- forbidden-inference state

High support cannot repair a semantic-authority failure.

## G7. Downstream admission — mandatory and separate

- evidence-lane identity
- admission status (`ALLOW`, `DENY`, `NOT_APPLICABLE`, or stage-native equivalent)
- admission reason
- upstream support state used by the gate
- V551/V552 contract/version identity

The stored empirical fact must survive a denied derived-pressure use.

## G8. Provenance / replay — mandatory

- source/substrate provenance
- source row or aggregate input hash sufficient for replay
- question-use contract hash
- response-semantics contract hash
- weight-authority identity
- compiler/formula version
- creation/run identity

## G9. Fields that need not be canonical if reconstructible

If the preceding primitives are immutable and versioned, the replacement need not canonically store:

- `pct_unweighted`
- `pct_weighted`
- duplicate dominant-response percentages
- entropy reductions
- Cramér's V
- normalized mutual information
- “best predictor” rankings
- other V550 diagnostic summaries

Percentages are pure ratios of preserved numerators/denominators. Diagnostic determinicity metrics are not part of the minimum conditional-evidence authority required by this court.

---

# H. V551/V552 implications without redesign

## H1. V551

Do not redesign the bridge. Feed it a replacement fact that preserves the exact support state and evidence lane.

Existing law already expresses the critical separation:

- direct relation response + positive underpowered support can remain usable evidence;
- derived determinicity requires sufficient support.

Therefore the replacement should not pre-delete underpowered cells. It should let V551 apply its own lane-specific gate.

## H2. V552

Do not make V552 infer weighting basis from a numeric field name.

The replacement/handoff must make available the same distinctions V552 currently relies on:

- raw versus weighted percentages or reconstructible numerator/denominator primitives;
- aggregate weight status;
- response-surface completeness;
- V551 promotability/adjudication state;
- unresolved weighted and unweighted mass;
- explicit distribution weight basis.

V552 may continue to select a partial weighted vector under current law when the vector is complete and `weight_status` is not one of its blocked states. R10 does not authorize changing that policy.

Likewise, R10 does not add a blanket small-n V552 pressure gate. Current support gating occurs upstream and is lane-sensitive. A future policy change would require separate authority.

## H3. Negative authority

V552's `APPLICABLE_BUT_UNRESOLVED`, `NO_APPLICABLE_EVIDENCE`, `OBSERVED_ZERO`, `OBSERVED_NONZERO`, and downstream permission states must not be collapsed into a nullable score.

A missing pressure score can mean different things. The typed status carries the authority.

---

# Exact answers to the ten questions

## 1. What do current weighted conditional cells mean?

They are **descriptive shares of selected respondent weight mass inside a defined empirical slice**.

For `indicator_answer_matrix`, a weighted conditional cell is:

`sum(valid positive finite weights for response r and condition v) / sum(valid positive finite weights for all responses at condition v)`

when a validated weight series exists.

For `partial` series, unusable rows contribute to raw counts but zero weighted mass. This is not a design-based confidence statement, not a causal effect, and not a probability that a generated actor with the matching position has that response.

## 2. How are partial, invalid and missing weights treated?

- `partial`: at least one but not all rows have positive finite weight; a validated sparse series is returned. Answer distributions and branching can use it; position distribution suppresses it; V552 can use a complete partial-weight percentage vector.
- `invalid`: no validated series; answer distributions have no lawful weighted estimate; branching falls back to raw computation even though weighted-named columns may numerically mirror raw; V552 rejects weighted use and falls back raw when available.
- `missing`: no validated series; same no-weight consequences, but authority state differs from invalid.
- `unweighted_only`: another explicit no-validated-weight state; V552 treats it as disqualifying weighted use.

## 3. Where do weighted and unweighted lanes differ?

They differ in numerator/denominator, row participation, and artifact policy.

Raw counts include every row in the relevant frame/slice equally. Weighted estimates include only usable positive finite weight mass. A partial row with no usable weight still exists in the raw lane.

Artifact policy then differs:

- answer/country distributions: partial weighted computation allowed;
- branching: partial weighted computation allowed;
- position distribution: partial weighted computation denied;
- V552: partial weighted percentage can be preferred if complete.

## 4. What denominator does each percentage use?

- `answer_distribution.pct_unweighted`: all rows in the question frame.
- `answer_distribution.pct_weighted`: total usable positive weight mass in the question frame.
- `country_answer_distribution.pct_unweighted`: all rows in that country/question frame.
- `country_answer_distribution.pct_weighted`: total usable positive weight mass in that country/question frame.
- `indicator_answer_matrix.pct_unweighted`: all response rows for the given indicator value.
- `indicator_answer_matrix.pct_weighted`: all weighted response mass for the given indicator value; if no validated weights exist, current code mirrors raw.
- `position_distribution.pct_unweighted`: deduplicated respondents with any nonblank value for that position field, within country.
- `position_distribution.pct_weighted`: weight mass among those respondents, **only when weight status is exactly `weighted`**.
- diagnostic dominant-response pct fields do not constitute a clean separate pair; the implementation can write the same baseline share into both named fields.

## 5. Which zero cells are observed structural zeros versus materialized crosstab completion?

Current V550 does **not** establish structural zeros.

`indicator_answer_matrix` uses `pd.crosstab`, which completes combinations across response and indicator categories that appear in the observed masked data. A cell may therefore have raw count zero because that particular combination is absent while both marginal categories exist.

That is a **crosstab-completion zero**, not evidence that the combination is structurally impossible.

No observation, missing authority, and not-applicable are separate states and must not be encoded as zero.

## 6. What does `underpowered` mean exactly?

For positive support:

`underpowered` means `support_count < min(30, max(2, ceil(total_respondents * 0.005)))`.

If total respondent count is unavailable, the threshold defaults to 30.

Zero support is `zero_support`, not `underpowered`. Missing support is `missing_support` for evidence lanes or `not_applicable` for specified structural lanes.

`underpowered` is a support-gate term only. It is not a significance test.

## 7. Does current Rawlsing possess enough PSU/stratum/replicate-weight information for design-based confidence intervals or variance estimates?

**No, not in the governed V550→V552 conditional-evidence path.**

The operational substrate carries one selected scalar respondent weight and its identity. The canonical conditional path does not propagate a complete governed sample-design record containing PSU, sampling-stratum, replicate weights, and a variance-estimation method.

Therefore current Rawlsing cannot calculate a lawful design-based standard error or confidence interval from these conditional artifacts.

## 8. If not, what is the strongest survey-design sampling-uncertainty claim it may lawfully make?

It may make **no quantitative survey-design sampling-uncertainty claim**.

The strongest lawful statistical qualification is descriptive:

> the estimate is based on `n` observed rows/respondents, uses a named selected weight under a stated complete/partial/no-weight state, has a specified raw/weighted denominator, and crosses or fails the machine's explicit support gate.

Epistemic uncertainty and downstream admissibility may be separately typed, but neither supplies a sampling confidence interval.

## 9. Must underpowered observed evidence remain stored even where structural pressure use is denied?

**Yes.**

Observed evidence and use permission are separate authorities.

Current V551 proves the distinction: `direct_relation_response` can remain usable when support is `underpowered`, while `derived_determinicity` is usable only at `sufficient_support`.

A low-support derived crosstab cell is still part of the historical sample and provenance even when derived pressure promotion is denied. Deleting it would turn an admission policy into an information-destruction policy and would prevent later re-audit or changed lawful use.

## 10. What minimum fields/statuses must a replacement conditional fact preserve?

At minimum:

1. source/wave/country/question/response identity;
2. exact condition identity and evidence lane;
3. raw cell count;
4. raw denominator;
5. total respondent count used for support threshold;
6. support threshold, support status, formula/version;
7. weighted cell mass and weighted denominator where available;
8. weight name/source/authority;
9. aggregate weight status;
10. usable/missing/invalid weight-row counts if respondent microdata will not remain;
11. explicit weight-basis/calculation status;
12. typed zero/absence state;
13. semantic authority and comparability state;
14. explicit survey-design variance availability state;
15. downstream admissibility state and reason;
16. provenance and contract hashes/versioning.

---

# Special hostile tests

## Test 1 — weighted and unweighted direction reverse

Condition `C` has three observed responses:

| row | answer | weight |
|---|---|---:|
| 1 | YES | 1 |
| 2 | YES | 1 |
| 3 | NO | 10 |

Raw:

- YES = 2/3 = 66.7%
- NO = 1/3 = 33.3%

Weighted:

- YES = 2/12 = 16.7%
- NO = 10/12 = 83.3%

The direction reverses. Raw and weighted lanes are irreducible to one percentage.

## Test 2 — equal weighted totals hide radically different raw support

Assume a wave with 1,000 respondents. Support threshold = 5.

Cell A:

- raw support = 1
- one respondent weight = 100
- weighted mass = 100
- support state = `underpowered`

Cell B:

- raw support = 100
- each respondent weight = 1
- weighted mass = 100
- support state = `sufficient_support`

Same weighted mass; radically different observed support. `n_unweighted` cannot be discarded.

## Test 3 — same apparent weighted number under different weight authority

Case A, complete valid weighting:

- 2 rows
- weights 50, 50
- `weight_status=weighted`
- weighted mass = 100

Case B, partial weighting:

- 2 rows
- weights 100, missing
- `weight_status=partial`
- usable weighted mass = 100

Numerically identical weighted mass; different respondent coverage and authority.

Case C, invalid/missing weight lane in `indicator_answer_matrix`:

- 100 raw rows
- no validated weight series
- branching code mirrors the raw crosstab into `n_weighted`
- apparent `n_weighted=100`

Again the number `100` appears, but it is not the same estimator. Without `weight_status` and explicit `weight_basis_status`, the number is semantically unsafe.

## Test 4 — zero observed count versus no observation

Suppose indicator categories `A` and `B` and response categories `YES` and `NO` appear somewhere in the data, but no respondent occupies `(B, YES)`.

`pd.crosstab` can emit:

`B × YES = 0`

That is a crosstab-completion zero inside observed marginal domains.

If a condition `C` has no governed mapping or no authorized observation, no such empirical fact exists. Encoding that absence as zero would fabricate negative evidence.

## Test 5 — small-n evidence historically real but inadmissible for derived pressure

Wave respondents: 1,000. Threshold: 5.

A derived indicator-answer cell has:

- raw support = 3
- support status = `underpowered`
- real source rows and provenance.

V551 derived-determinicity admission requires `sufficient_support`, so this cell is not promotable through that lane.

The correct action is:

- preserve the cell;
- preserve `n=3`;
- preserve `underpowered`;
- preserve the V551 denial reason.

The incorrect action is to delete the cell or rewrite it as `no evidence`.

---

# Final authority ruling

The minimum lawful conditional-evidence architecture is a **qualified empirical-fact store**, not a deterministic-profile store and not a pseudo-survey-inference engine.

Its core unit must say, in effect:

> For this governed source/question/response and this governed empirical condition, Rawlsing observed this many rows out of this denominator; this much selected-weight mass out of this weight denominator under this weight authority and weight-completeness state; the cell has this support status; the zero/absence state means this exact thing; semantic/comparability authority is this; and downstream use is currently allowed/denied/unresolved for this reason.

Anything weaker loses present meaning. Anything stronger that supplies unearned design-based confidence fabricates precision.

This preserves the governing-spirit requirement: the evidence can constrain the world without turning a sample pattern into destiny, and the machine can remain explicit about what it does not know.

---

# Evidence inspected at exact base

Primary code:

- `data/ddm_build_copy/ddm_v550_metrics.py`
  - `classify_weight_status`
  - weighted metric helpers
- `data/ddm_build_copy/ddm_v550_support.py`
  - `support_threshold_from_total`
  - `support_status_from_count`
  - `confidence_tier_from_support`
- `data/ddm_build_copy/ddm_v550_distributions.py`
  - `build_distribution_tables`
- `data/ddm_build_copy/ddm_v550_branching.py`
  - `indicator_summary_rows`
  - `secondary_indicator_summary_rows`
  - `indicator_answer_matrix_rows`
- `data/ddm_build_copy/ddm_v550_position_distribution.py`
  - `build_position_distribution_rows`
- `data/ddm_build_copy/build_determinicity_repository_v550.py`
  - propagation of V550 weight status/validated series into branching
- `data/ddm_build_copy/apply_postgres_facet_ready_substrate.py`
  - `survey_weight_fact`
  - facet-ready primary-weight selection
  - GSS/LiTS weight allowlists and primary ordering
- `data/ddm_build_copy/ddm_v550_schema.py`
- `data/ddm_build_copy/ddm_v550_bridge.py`
  - lane-specific support/admission
- `data/ddm_build_copy/ddm_v552_structural.py`
  - `select_v552_distribution_weight_basis`
  - V552 measurement-evidence/downstream-permission states
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`

Publication-path convention was verified against sibling branch `agent/vozhd-trii-vt3-cm-r01`.
