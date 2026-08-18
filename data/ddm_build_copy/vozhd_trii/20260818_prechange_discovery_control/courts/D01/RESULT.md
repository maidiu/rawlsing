# VOZHD TRII D01 — V526c / V547 → CURRENT V550 DETERMINICITY LINEAGE COURT

**Cell:** `D01`  
**Campaign:** Vozhd Trii Pre-Change Discovery Campaign  
**Repository:** `maidiu/rawlsing`  
**Exact base examined:** `bf9a0434eb2096d5c4725cf483ec757fd319b6af`  
**Authorized branch:** `agent/vozhd-trii-d01-v547-lineage`  
**Production code changed:** `NO`  
**Court type:** capability genealogy, not architecture selection or preservation adjudication  
**Verdict:** `PARTIAL_LINEAGE_WITH_MATERIAL_MATHEMATICAL_AND_SEARCH_GEOMETRY_MUTATION__UNRESTRICTED_V547_PAIR_DISCOVERY_LOST__UNARY_CONDITIONAL_TOPOLOGY_ADDED__DERIVED_LANE_NOT_CANONICALLY_CONSUMED`

---

## 1. Executive verdict

Historical `V526c_DIALECTICAL_DETERMINICITY_MAPPER` did not define one undifferentiated thing called determinicity. Its extracted purpose explicitly named three diagnostic capabilities: **predictor salience**, **interaction salience**, and **shape classes**. Recursive breakage trees were explicitly outside V526c and belonged to adjacent historical V526d; branch co-signature/profile covariance belonged to V526e. The old design therefore already separated single-predictor discovery, interaction discovery, shape diagnosis, recursive branching, and profile covariance even though later prose often grouped them under one conceptual banner.

Executable V547 implemented a narrow but real subset of that design. For each bound question it:

1. coerced the response to numeric values and hard-dropped a fixed missing-code set;
2. computed unweighted discrete mutual information between response and six non-country position predictors;
3. separately computed `MI(country_code; response)`;
4. exhaustively searched every unordered pair among the finite-scored six non-country predictors;
5. selected the pair with the highest **joint pair MI**, then stored its gain over the stronger of its two marginals;
6. classified the question as `sparse`, `flat`, `interaction`, `main_effect`, or `mixed`;
7. emitted one lossy question-level summary row.

That was genuine empirical-discovery intelligence. It was not a conditional-distribution store, it did not retain predictor values or joint cells, it did not retain respondent membership, and it was explicitly unweighted. But it could detect a strong two-field interaction even when neither field was the strongest marginal predictor.

Current V550 is **not** a faithful mathematical continuation of that executable. It preserves the broad objective of discovering response heterogeneity by respondent position, while splitting it across several current functions:

- `position_indicator_summary` / `indicator_summary_rows` — scalar single-field association diagnostics;
- `indicator_answer_matrix` — exact unary `indicator_value × response_value` contingency cells;
- `outlier_cohort_summary` — support-gated subgroup dominant-response comparison;
- `secondary_indicator_summary` — incremental second-field search conditional on one chosen primary;
- `recursive_branch_nodes` — bounded greedy recursive split search.

The current implementation therefore gains a capability V547 did not possess: `indicator_answer_matrix` preserves full one-dimensional response topology and weighted/unweighted cell mass for each searched indicator value. But it also loses a capability V547 did possess: **unrestricted pairwise interaction discovery**. Current `secondary_indicator_summary_rows` first chooses one primary indicator and tests only `primary + each other field`. With twelve current fields, at most eleven primary-star pairs are examined instead of the sixty-six unordered pairs that an exhaustive twelve-field search would contain. This is a search-geometry mutation, not a naming difference.

The mathematics also changed materially. V547 used scikit-learn discrete MI in natural-log units, unweighted and complete-case per candidate. Current V550 calls the field `mutual_information`, but computes it as:

`max(0, H_full(Y) - H(Y | X, X observed))`

where entropy is base 2 and survey weights may be used. Because the baseline is computed on the full response universe while conditional entropy is computed only where the predictor is nonblank, the result is **not generally mutual information when predictor missingness exists**. A hostile fixture can make `X` exactly independent of `Y` on every row where `X` is observed while current V550 reports a large positive value solely because the response mix differs between the X-observed and X-missing populations.

Current `normalized_mutual_information` is another separate diagnostic and is not numerically comparable to either V547 MI or current entropy reduction: it uses sklearn `mutual_info_score` in natural-log units but divides by `distribution_entropy`, which is implemented in bits. A perfect balanced binary relation therefore produces current entropy reduction `1.0`, V547 MI `ln(2) ≈ 0.693147`, and current so-called normalized MI `≈0.693147`, not `1.0`.

The execution grain also changed. V547 wrote `analysis_mode="within_country"`, but the executable `load_question_frame()` filtered the response table only by source and variable code; it did **not** filter by country and did **not** filter by wave. Its score was therefore source-family × variable-code pooled over the returned countries and, where a variable code recurred, potentially pooled waves, even though a canonical wave label was attached from the structure register. Current V550 explicitly builds at source × canonical wave × country × question scope.

Finally, current materialization does not establish a current canonical semantic consumer for the derived determinicity lane. `ddm_v550_bridge.py` directly reads the current determinicity tables and maps the matrix/outlier/secondary/recursive families to `derived_determinicity`, but the canonical V551 compiler accepts only `direct_relation_response` from `answer_distribution` and `country_answer_distribution`. The separate `ddm_v551_conditional.py` helper appears intended to consume the derived lane, but at this exact base it imports `MIN_ATOM_SUPPORT` and `SOURCE_TABLE_PRIORITY` from current `ddm_v551_atoms.py`, where neither symbol exists, and it is not imported by the canonical V551 compiler. D01 therefore records a bridge reader plus an intended-but-unwired/broken helper, not a proved canonical downstream preservation path.

This finding does **not** establish that historical V547 interaction search must be restored, that any current artifact must be retained, or that any current artifact may be deleted. Those are outside D01 jurisdiction.

---

## 2. Source evidence inspected

### 2.1 Pre-change control law — read first

All were read at the exact D01 base before genealogy adjudication:

- `data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/README.md`
- `00_FULL_MACHINE_VISION.md`
- `01_FINDINGS_LEDGER.md`
- `02_RESOURCE_INDEX.md`
- `03_ASSUMPTION_AND_UNKNOWN_REGISTER.md`
- `04_DISCOVERY_COURTS_REGISTER.md`
- `05_DECISION_PROTOCOL.md`
- `06_FIRST_WAVE_LAUNCH_REGISTER.md`
- `evidence/HISTORICAL_DESIGN_EXTRACTS.md`

The control surface makes historical design evidence nonbinding on present architecture and separates empirical population evidence from actor fact/psyche. D01 has obeyed that boundary.

### 2.2 Current binding whole-machine law

Read directly at the exact base:

- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/RAWLSING_GOVERNING_SPIRIT.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/TERMINAL_DEMAND_ENVELOPE.md`
- `data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/ARCHITECTURE_PASS_LAW.md`

These constrain inference: predictor association is not actor belief or identity; historical design is not present authority; typed uncertainty/absence and provenance cannot be silently collapsed.

### 2.3 Historical design evidence

`evidence/HISTORICAL_DESIGN_EXTRACTS.md` is explicitly marked `HISTORICAL_DESIGN_EVIDENCE__NOT_CURRENT_AUTHORITY` and preserves exact extracts plus source-archive hashes.

Relevant extracts:

- V526c: purpose = `predictor salience, interaction salience, shape classes`; required `question_determinicity_summary` and `determinicity_shape_diagnostics`; no runtime; no tree recursion beyond contracts.
- V526d: recursive positional breakage tree, majority-position deviation, branch split evidence.
- V526e: branch co-signature and profile covariance; historical purpose included covariance for profile generation.
- Historical Attitude Cloud Access Contract: distinguished position determinants, anchor responses, and attitude clouds; historical profile-posterior design expected identity/position predictors + likely anchor branch memberships + attitude-cloud co-signatures.
- Historical V547 review: `V547_QUESTION_LEVEL_POSITIONAL_DETERMINICITY`, `row_count: 184`, historical source scopes Afrobarometer, Arab Barometer, Asian Barometer, EVS, Latinobarómetro.

The source archives themselves are hash-addressed external historical evidence. Their old unpacked pack paths are not present as ordinary files on the current repository tree. D01 therefore uses the campaign's extracted evidence rather than pretending the old pack directories are current code.

### 2.4 Executable V547

Directly inspected:

- `data/ddm_build_copy/build_question_determinicity_summary_v547.py`
- blob SHA: `3fc894501ce77c6519a2b32213f3f017465553e5`

### 2.5 Current V550 implementation

Directly inspected:

- `data/ddm_build_copy/ddm_v550_branching.py` — blob `8f6d40e0d016d66e5a3b334b31747eaef752873f`
- `data/ddm_build_copy/ddm_v550_metrics.py` — blob `e7675f4080bb30e6526027a34db747b7be7f85c9`
- `data/ddm_build_copy/ddm_v550_support.py` — blob `1b841139fee051b154dcccd52cd3d866b958dbb5`
- `data/ddm_build_copy/ddm_v550_distributions.py` — blob `43a62723b16f9c800ed7a6ef40a77e70a3f07377`
- `data/ddm_build_copy/build_determinicity_wave_shard_v550.py` — blob `82ffc18df29a8e5ebd78cde97c89d463b3842df6`
- `data/ddm_build_copy/build_determinicity_repository_v550.py` — blob `04f3a3646d8b468660385087d92541f03f860cb0`
- `data/ddm_build_copy/ddm_v550_manifest.py` — blob `161f3244b7d13fece83c200a3aa42570eacda1e5`
- `data/ddm_build_copy/ddm_v550_question_use.py` — blob `8d90a5116fd05b5db17e9b4645638a3aa6fc1131`
- `data/ddm_build_copy/ddm_v550_bridge.py` — blob `29edd5e24f095334683035f2ce1ec95674fe274b`

Also inspected current R1 authority package orientation:

- `data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/00_README_FIRST.md` — blob `0efe718462d3b1f527d8c59a115fe8cb1e0260c1`

D01 records R1 presence but does not adjudicate R1 into a conditional workload law; D06/D07 own that question.

### 2.6 Current direct downstream seams

Directly inspected:

- `data/ddm_build_copy/compile_v551_relation_evidence_atoms.py` — blob `a054247590932e7ac02d0d08485e7c294b618d24`
- `data/ddm_build_copy/ddm_v551_atoms.py` — blob `d07e9a0c8f552b9a53bb1e775281fdf9a68e29e0`
- `data/ddm_build_copy/ddm_v551_conditional.py` — blob `359665297677553a33556ce65c2e3d76b60b2cc1`

### 2.7 Frozen VT3 evidence

Read as evidence about frozen SHA `8c87f7725ba58202b5377c974548140420709fa9`, never as a substitute for current inspection:

- VT3-CM-R00 synthesis;
- corrected R01 conditional-value archaeology;
- R02 information-loss court;
- R05 compute/cardinality court;
- R07 no-loss court;
- R11 workload-authority court.

Where their source descriptions are reused below, D01 independently rechecked the relevant current files at `bf9a043...`.

---

## 3. Historical V526c capability reconstruction

### 3.1 What “determinicity” meant in V526c

The extracted V526c purpose is narrow enough to prove a three-part diagnostic ontology:

1. **Predictor salience** — which available structural/demographic coordinate carries response information?
2. **Interaction salience** — do combinations carry information beyond single predictors?
3. **Shape classes** — what broad pattern does the discovered determinicity take?

V526c required a question summary plus shape diagnostics. It was an offline/schema-or-builder layer, not runtime authority.

### 3.2 What V526c did not itself own

Historical neighboring packs establish boundaries that matter for lineage:

- Recursive branching was separately assigned to V526d. Therefore current `recursive_branch_nodes` should not be described as a literal preservation of a V526c executable feature.
- Co-signature/profile covariance was separately assigned to V526e. Therefore current branch/covariance surfaces may share ancestry with the historical determinicity program, but they are not proof that V526c itself computed them.
- The profile-posterior idea appears in historical design evidence, but this is **HISTORICAL_DESIGN_EVIDENCE**, not current authority to generate actor belief/identity from demographic association.

### 3.3 Required distinctions under the user's primary question

| Concept | Historical status | D01 reconstruction |
|---|---|---|
| response-distribution description | not the named V526c core | V547 did not preserve it; current V550 later adds it through unary matrix/distribution families |
| predictor salience | explicit | implemented in V547; mutated in V550 |
| interaction salience | explicit | implemented as exhaustive pair search in V547; narrowed in V550 secondary search |
| conditional entropy reduction | not proved as V526c formula | current V550 mechanism, not V547 formula |
| demographic/social-position heterogeneity | central input domain | survives, with changed field universe and grain |
| branch discovery | separate V526d historical owner | current recursive branch machinery is an adjacent-lineage successor |
| authoring diagnostic | strongly supported | V526c was offline diagnostic; V547 was exploratory/unweighted |
| structural evidence | not automatically established by salience | current bridge/use authority must separately govern this |
| reverse generative/profile use | historical downstream ambition | current lawful requirement/consumer is `UNKNOWN` in D01; no promotion from history |

---

## 4. Executable V547 behavior

### 4.1 Input respondent grain

V547 loaded respondent position facts keyed by respondent ID from `respondent_position_fact`, including source family, wave, country, survey year, sex, age, education, income, religion, and urbanicity. It derived `age_group` with bins:

- 18–29
- 30–44
- 45–59
- 60+

The executable then loaded question-response rows and joined/aligned them to respondent-level position fields.

### 4.2 Target variable

`normalize_response_values()` coerced `value_raw` to numeric. Nonnumeric responses became missing. It additionally converted these fixed values to missing:

`-2, -1, 8, 9, 98, 99, 101, 999`.

The target passed to MI was the surviving numeric `response_value`, later string-encoded as a categorical class.

This is a major historical semantic boundary: V547 did **not** preserve DK/refusal/IAP/not-asked distinctions and could not analyze source-native nonnumeric categorical answers that failed numeric coercion.

### 4.3 Candidate predictor universe

`POSITION_COLS` was:

- `country_code`
- `sex`
- `age_group`
- `education_level`
- `income_level`
- `urban_rural`
- `religion_label`

`country_code` was scored separately. Pair search used only the remaining six fields.

### 4.4 Single-predictor mutual information

For each predictor:

```text
joined = (feature, target).dropna()
require n >= 300
require >=2 feature classes
require >=2 target classes
label-encode feature and target
score = sklearn.feature_selection.mutual_info_classif(
    X, y,
    discrete_features=True,
    random_state=0
)[0]
```

This is unweighted empirical discrete MI in scikit-learn's natural-log convention.

Historical missingness was predictor-type dependent:

- numeric education/income missing values were NaN and dropped by the MI join;
- string fields such as sex/religion/urbanicity were filled with `""`; blank strings were not converted back to NaN inside `mi_score`, so blank could behave as a category;
- `age_group` missing age became `""` after string conversion and could likewise become a category.

### 4.5 Country handling

V547 calculated `country_code_score = MI(country_code; target)` but normally did **not** let country compete with the six non-country predictors for `top_predictor_1`. If any non-country predictor had a finite score, top predictor came from that set. Country became fallback only when no non-country predictor survived.

### 4.6 Pair search

For every unordered pair among finite-scored non-country predictors:

```text
joint = a + "||" + b
pair_score = MI(joint; target)
base = max(MI(a; target), MI(b; target))
gain = pair_score - base
```

V547 selected the pair with the **highest pair_score**, not necessarily the pair with the highest gain. It persisted:

- `top_interaction_1 = a+b`
- `top_interaction_1_gain = pair_score - max(single_a, single_b)`

It did **not** persist `pair_score` itself, exact pair values, pair-cell response distribution, or exact pair-specific complete-case N.

With all six non-country predictors usable, V547 examined all `C(6,2)=15` unordered pairs.

### 4.7 Shape classifier

The exact order is:

```text
if top_mi invalid or n < 300: sparse
elif top_mi < 0.005: flat
elif pair_gain > max(0.01, 0.25 * top_mi): interaction
elif top_mi >= 0.02: main_effect
else: mixed
```

This ordering contains a historical internal contradiction: a pure XOR pair can have zero marginal MI and maximal pair MI, V547 can discover that pair, yet `shape_class` becomes `flat` because `top_mi < 0.005` is evaluated before interaction gain.

### 4.8 Confidence

V547 confidence was a heuristic:

```text
sample_factor = min(n / 2000, 1)
mi_factor = min(top_mi / 0.05, 1)
confidence = min(0.99, 0.35 + 0.35*sample_factor + 0.30*mi_factor)
```

It was not a standard error, confidence interval, design-based uncertainty estimate, or posterior probability.

### 4.9 Scope bug / grain mismatch

The output says `analysis_mode="within_country"`. The executable response query does not implement that label.

`load_question_frame(conn, source, var_code)` filters by:

- source;
- variable code;
- non-null raw response.

It does not filter by country and does not filter by wave. A `canonical_wave` label is separately looked up from the bound-question register and attached to the output row.

The executable V547 statistic is therefore best described as:

`source-family × var-code pooled response/position association`,

not country-specific determinicity. Where a variable code appears across multiple waves, the absence of a wave predicate creates potential cross-wave pooling as well.

### 4.10 Output grain and information loss

One `SummaryRow` per processed question retained:

- analysis mode;
- source/dataset scope;
- canonical-wave label;
- question ID;
- final driver ID;
- target layer;
- n and `weighted_n` (equal to n);
- country MI;
- top predictor identity and score;
- top interaction identity and gain;
- shape class;
- confidence.

It destroyed or never materialized:

- full response distribution;
- every nonwinning predictor score;
- every nonwinning pair score;
- predictor values;
- joint predictor values;
- pair-specific support;
- weighted statistics;
- respondent membership;
- minority configurations;
- directional subgroup effect shape;
- uncertainty beyond heuristic n/MI confidence.

---

## 5. Current V550 behavior

### 5.1 Current candidate field universe

`ddm_v550_branching.py` hard-codes exactly twelve `INDICATOR_FIELDS`:

1. `sex`
2. `age_group`
3. `education_level`
4. `income_level`
5. `religion_label`
6. `urban_rural`
7. `region`
8. `ethnicity`
9. `language`
10. `employment`
11. `marital`
12. `household_size`

This expands V547's non-country search frontier by six standardized fields: region, ethnicity, language, employment, marital, household size.

It also omits some physically richer respondent-position information recorded elsewhere in current campaign evidence, such as raw `age` and `class_level`. D01 records this availability/search mismatch only. It does not infer that those fields should be searched.

### 5.2 Current execution grain

The V550 shard/repository path constructs explicit question frames at source × wave × country × question scope, with canonical source/wave alias handling and R1-era structural/question authority joined into metadata. This is a real scope repair relative to executable V547 pooling.

### 5.3 Response semantics before branching

Current harmonization/distribution code preserves a much richer response-semantics surface, including:

- `is_substantive`
- `is_missing`
- `is_special`
- `is_dk`
- `is_refusal`
- `is_iap`
- `is_not_asked`
- `is_inapplicable`
- response-semantic status/source/contract hash.

However, `prepare_question_frame()` and the branching functions operate primarily on `response_value_normalized` strings and do not use these flags to remove or separately type special responses inside the determinicity metric formulas. Typed semantics therefore survive **beside** the current determinicity calculations, not as an explicit branch-metric exclusion law.

### 5.4 `indicator_summary_rows`

For each present indicator:

```text
y = full response vector
baseline_h = H(y)                 # weighted if weights supplied
x = indicator as string
mask = x != ""
yx = y[mask]
cond_h = H(yx | x[mask])          # weighted if weights supplied
mi = max(0, baseline_h - cond_h)
nmi = normalized_mutual_information(x[mask], yx)  # unweighted
cramers_v = cramers_v(x[mask], yx)                # unweighted
```

Important consequences:

1. The field called `mutual_information` is entropy reduction, not the V547 sklearn MI formula.
2. Entropy is base 2, while V547 MI was in natural-log units.
3. Weights affect baseline/conditional entropy when a validated weight series exists.
4. NMI and Cramér's V remain unweighted.
5. Baseline entropy is computed before the predictor-nonblank mask; conditional entropy is computed after it. Under predictor missingness, `baseline_h - cond_h` can represent composition shift between observed and missing predictor populations rather than association of X with Y.

The summary emits one row per indicator rather than one winning predictor per question, so alternative unary predictor identities survive more fully than in V547.

The emitted `indicator_value` is **not** a universal exact condition key for the scalar score. In the unweighted path it is the most frequent predictor value. In the weighted path it becomes the predictor value whose subgroup has the highest within-group dominant-response share. The scalar MI/Cramér/NMI describes the full indicator, not that one `indicator_value`.

### 5.5 `indicator_answer_matrix_rows`

This is the strongest current capability added relative to V547.

For every available indicator, V550 creates an unweighted crosstab:

`indicator_value × response_value`

and, when weights are available, a weighted pivot over the same cells. It emits:

- exact `indicator_name`;
- exact `indicator_value`;
- exact `response_value`;
- `n_unweighted`;
- `pct_unweighted` within the indicator-value subgroup;
- `n_weighted`;
- `pct_weighted` within the weighted indicator-value subgroup.

This materially preserves `P(response | indicator=value, current question/scope)` topology that V547 threw away.

It is still unary. It does not materialize `P(response | A=a AND B=b)`.

### 5.6 `secondary_indicator_summary_rows`

Current secondary search first recomputes all single-field candidate scores, then selects exactly one primary:

```text
primary = max(candidate_scores,
              key=(mutual_information, cramers_v, n_unweighted))
```

Every secondary test must contain that primary. For each other candidate:

```text
joint_mask = primary_nonblank & secondary_nonblank
require joint_n >= 50
joint_key = primary_value || secondary_value
joint_cond_h = H(Y | joint_key)
secondary_gain = max(0, primary_cond_h - joint_cond_h)
retain only if gain > 0
```

This is not unrestricted pair discovery.

With twelve candidates, current secondary search can examine at most eleven of sixty-six unordered pairs. It examines **zero** pairs that exclude the selected primary.

A further missingness issue exists: `primary_cond_h` was computed on the primary's own nonblank universe, while `joint_cond_h` uses the intersection of primary and secondary nonblank rows. Therefore `secondary_gain` can also include a population-composition change when the secondary predictor has missingness.

Current secondary rows preserve primary name, secondary name, joint N, and gain. They do not preserve the full joint value × response contingency. The ordinary scalar fields copied into the emitted secondary row (`mutual_information`, `cramers_v`, etc.) are the marginal metrics for the secondary candidate, not a full joint-MI record.

### 5.7 `outlier_cohort_rows`

Current outlier cohorts are a separate diagnostic family:

- compute a global dominant response;
- group by each indicator value;
- require support;
- compare subgroup dominant response/share to baseline;
- label `conforms`, `deviates`, or `minority_converges`.

This can suppress a small stable minority below support while the ungated matrix still retains its cells. Minority preservation is therefore split across current artifacts rather than represented by one common determinicity policy.

### 5.8 `recursive_branch_nodes`

Current recursive branching is a greedy bounded search:

- evaluate remaining indicators at the node by conditional-entropy gain;
- choose the single best positive-gain split;
- stop for purity, max depth, underpower, no remaining indicator, or no gain;
- recurse only into the two most frequent values of the chosen split;
- default maximum depth is 3.

This is historically closer to V526d than to executable V547.

It does not recover exhaustive pair search. If all marginal gains at the root are zero, it stops and cannot discover a pure higher-order interaction such as three-way parity.

### 5.9 Weight state

`classify_weight_status()` recognizes:

- `missing`
- `invalid`
- `unweighted_only`
- `partial`
- `weighted`

Only positive finite weights are valid. Partial weight series preserve missing entries and weighted formulas commonly coerce their contribution to zero.

The branching APIs themselves receive either a weight series or `None`, and summary rows frequently emit `weight_status="weighted"` whenever a series is present, which can flatten the upstream `partial` distinction at this local output layer.

### 5.10 Shared support law

Current shared support threshold:

`ceil(total_respondents × 0.005)` clipped to `[2, 30]`.

But current families do not all use one identical gate:

- indicator summary emits even low-support fields and marks `usable` only at N≥50;
- secondary summary has a hard joint N≥50 gate;
- outlier and recursive branches use support thresholds;
- unary matrix itself emits observed indicator-value cells without the same subgroup suppression logic.

“V550 support” is therefore not one scalar rule.

---

## 6. Function-by-function / formula-by-formula lineage matrix

| Capability / formula | V526c / V547 | Current V550 | Disposition | Exact lineage finding |
|---|---|---|---|---|
| predictor salience | V526c explicit; V547 unweighted discrete MI | weighted/unweighted entropy reduction + unweighted NMI/V | `MUTATED` | broad purpose survives, mathematics does not |
| single-predictor output | only top non-country predictor persisted | one summary row per current indicator | `PRESERVED` | current scalar surface preserves more alternative unary identities |
| unrestricted pair search | all finite-scored non-country pairs | absent | `LOST` | current secondary search is one-primary star |
| pair joint MI | selected pair by highest pair MI | no direct equivalent field | `LOST` | current row stores secondary gain, not V547 pair MI |
| interaction gain | pair MI − stronger marginal MI | primary conditional entropy − joint conditional entropy | `MUTATED` | different formula, units, masks, search geometry |
| shape class | explicit V526c lane; V547 five classes | no direct successor | `LOST` | scalar current outputs do not recreate historical classifier |
| confidence | V547 n/top-MI heuristic | support/confidence tiers | `MUTATED` | labels are not numerically/semantically equivalent |
| country heterogeneity | separate country MI on pooled frame | country is scope | `SUPERSEDED` | current execution no longer needs country as ordinary searched predictor |
| unary conditional topology | not retained by V547 | `indicator_answer_matrix` | `SUPERSEDED` | current V550 preserves substantially richer unary response evidence |
| outlier/minority label | absent | support-gated cohort diagnostic | `DIAGNOSTIC_ONLY` | new current projection |
| recursive branch search | excluded from V526c; separate V526d | bounded greedy recursive tree | `SUPERSEDED` | adjacent historical lineage, not V547 preservation |
| NMI | absent | unweighted mixed-base calculation | `SUPERSEDED` | new current scalar; perfect relation ≠1 under implementation |
| Cramér's V | absent | unweighted contingency association | `SUPERSEDED` | new current scalar |
| weighted salience | V547 none | current entropy lanes can use scalar weights | `MUTATED` | weighted ranking can reverse historical unweighted ranking |
| exact predictor value | V547 not persisted | exact in matrix; representative only in scalar summary | `SPLIT_ACROSS_MULTIPLE_CURRENT_FUNCTIONS` | condition identity is artifact-dependent |
| joint condition cells | absent | absent from secondary summary | `UNKNOWN` | separate respondent/joint machinery exists elsewhere, but this D01 lineage does not equate it with secondary output |
| typed response absence | fixed-code numeric deletion | typed flags in harmonization/distribution, not explicit branching law | `SPLIT_ACROSS_MULTIPLE_CURRENT_FUNCTIONS` | current semantics richer but metric inclusion remains separate |
| respondent IDs in determinicity output | not persisted | not persisted in these outputs | `LOST` | both summary families are aggregate projections |
| three-way parity discovery | pair-only, no triples | greedy tree requires positive preceding split | `LOST` | shared limitation |
| reverse profile generation | historical ambition only | no proved canonical current consumer | `UNKNOWN` | history cannot create current authority |

### 6.1 Exact score-unit incompatibility

For a perfectly balanced binary predictor that exactly equals the response:

- V547 sklearn discrete MI: `0.6931471805599454` (`ln 2` nats)
- current V550 entropy reduction: `1.0` bit
- current V550 `normalized_mutual_information`: `0.6931471805599453`

Therefore historical thresholds such as V547 `0.005` and `0.02` cannot be transferred numerically onto current entropy-reduction values without a separate conversion/authority decision.

---

## 7. Search-space comparison

### 7.1 V547 search geometry

Main non-country candidates:

`sex, age_group, education_level, income_level, urban_rural, religion_label`

Country diagnostic:

`country_code`

Maximum pair search:

`C(6,2)=15` unordered non-country pairs.

A field entered pair search if its marginal MI was finite. Zero MI is finite, so XOR fields remained pair-search candidates.

### 7.2 Current V550 search geometry

Current twelve fields:

`sex, age_group, education_level, income_level, religion_label, urban_rural, region, ethnicity, language, employment, marital, household_size`

Unary summary/matrix/outlier loops can visit all present fields.

Secondary search:

1. score every present field;
2. select one primary;
3. test only that primary with every other field.

At P=12:

- all possible unordered pairs = `66`;
- maximum current secondary pairs examined = `11`;
- maximum fraction of all possible pairs directly evaluated by this function = `11/66 = 16.7%`.

This is a computational/search fact, **not** a claim that all 66 pairs are lawfully authorized or should be computed.

### 7.3 Fields physically available but no longer / not yet searched

Relative to V547:

- `country_code` moved from predictor to scope;
- all six V547 non-country fields remain represented in current `INDICATOR_FIELDS`.

Current V550 newly searches:

- `region`
- `ethnicity`
- `language`
- `employment`
- `marital`
- `household_size`

Current campaign evidence also records richer respondent-position facts beyond this hard-coded list, including raw age and `class_level`. Current question-use code recognizes a broader set of position-coordinate aliases as well. Mere physical availability or semantic recognition does not establish workload authority. D07 must determine the lawful search frontier.

### 7.4 Hostile fixture: strong marginal predictor

Construction: balanced binary `A`; response `Y=A`.

Result:

- V547 MI(A;Y) = `ln(2) ≈ 0.693147`, shape `main_effect`;
- current entropy reduction = `1.0` bit.

Holding: core unary salience survives, but numerical formula/unit changed.

### 7.5 Hostile fixture: weak marginals + strong interaction with a competing primary

Construction: balanced A/B with `Y = A XOR B`; add C that tracks Y weakly enough to have positive marginal MI.

Representative deterministic fixture:

- V547 marginal MI: `A=0`, `B=0`, `C≈0.080216` nats;
- V547 pair MI `A+B≈0.693147`, pair gain ≈`0.693147`;
- pairs containing C carry only tiny additional gain.

V547 exhaustively searches A+B and selects it.

Current V550 chooses C as the primary because it has the largest marginal score, then tests only C+A and C+B. **A+B is never evaluated.**

Holding: unrestricted V547 pair-discovery capability is `LOST` in the current secondary search geometry.

### 7.6 Hostile fixture: pure XOR with tie-order sensitivity

Construction: A/B XOR response plus an irrelevant C, all marginal scores exactly zero.

- V547 keeps zero-MI predictors as finite candidates and exhaustively finds A+B.
- V547 nevertheless labels the question `flat`, because the `<0.005` marginal test occurs before interaction-gain evaluation.
- Current secondary selection resolves the all-zero primary tie by candidate order/secondary tie fields. If C is chosen primary, current tests C+A and C+B and never evaluates A+B.

Holding: historical V547 interaction search was stronger than its own shape classifier; current V550 can lose the interaction even earlier at search selection.

### 7.7 Hostile fixture: Simpson reversal

Construction with strata Easy/Hard and treatment-like position P:

- Easy: P0 success 0.90, P1 success 0.80;
- Hard: P0 success 0.20, P1 success 0.10;
- composition chosen so pooled P0 success ≈0.264 and pooled P1 success ≈0.736.

Within each stratum P1 is worse; pooled P1 is better.

V547 can assign scalar MI to P, scalar MI to stratum S, and discover S+P as a pair. Its output row does not retain the directional joint cells required to reconstruct the reversal.

Current unary `indicator_answer_matrix` preserves `P(response|P)` and `P(response|S)` separately but not `P(response|S,P)`. `secondary_gain` records an incremental scalar, not the joint response topology.

Holding: neither V547 row nor current secondary summary preserves Simpson-reversal semantics. The current unary matrix is richer than V547 but still insufficient for the joint reversal by itself.

### 7.8 Hostile fixture: small stable minority

Construction: N=1000 with a stable minority subgroup N=3 carrying a distinctive response.

Current shared support threshold at N=1000 is `ceil(1000×0.005)=5`.

- V547 had no per-subgroup output/support gate; it could only let the minority influence aggregate MI and then discarded its value identity.
- Current unary matrix can retain the N=3 cells.
- Current outlier cohort can suppress the subgroup below support.
- Current secondary search requires N≥50 for a joint row.

Holding: current minority information is split across artifact families; one cannot infer “V550 preserves/drops the minority” without naming the family.

### 7.9 Hostile fixture: predictor effect reverses inside subgroup

Construction: two equal strata; in S0, `Y=P`; in S1, `Y=1-P`.

Pooled marginal MI(P;Y)=0. Pair `(S,P)` perfectly determines Y.

V547 exhaustive pair search can discover S+P but does not retain the directional cell pattern; its shape classifier can again call the question `flat` because top marginal MI is zero.

Current secondary search may or may not test S+P depending on which zero-scored field wins primary tie-breaking, and its emitted row still lacks the complete joint contingency.

### 7.10 Hostile fixture: three-way interaction

Construction: balanced `Y=A XOR B XOR C`.

Every marginal and every pair carries zero information about Y; the triple determines Y perfectly.

- V547 pair search fails.
- Current secondary search fails.
- Current greedy tree has no positive root split and stops before a triple can emerge.

Holding: three-way parity is a shared limitation, not a capability V547 possessed and V550 uniquely lost.

### 7.11 Hostile fixture: weighted vs unweighted predictor-ranking reversal

Construction:

- 600 low-weight rows (`w=0.1`) where A predicts Y and B is independent;
- 200 high-weight rows (`w=10`) where B predicts Y and A is independent.

Representative scores:

- V547 unweighted MI: A≈`0.316377`, B≈`0.031584`; A wins.
- Current unweighted entropy reduction: A≈`0.456436` bits, B≈`0.045566`; A wins.
- Current weighted entropy reduction: A≈`0.000612` bits, B≈`0.890286`; B wins.

Holding: weighting is not a cosmetic addition. It can reverse predictor ranking. Current NMI and Cramér's V remain unweighted, so one current summary row can simultaneously contain a weighted MI ranking quantity and unweighted association companions.

### 7.12 Hostile fixture: missingness creates false current “MI”

Construction: full response population is balanced. Predictor X is observed on all 400 Y=0 rows and only 40 Y=1 rows; within the 440 X-observed rows, X itself is exactly independent of Y.

- V547 complete-case MI(X;Y) = `0`.
- proper complete-case MI in bits = `0`.
- current full baseline entropy = `1.0` bit.
- current conditional entropy on X-observed subset ≈`0.439497` bit.
- current reported `mutual_information = 1.0 - 0.439497 ≈ 0.560503`.

Holding: under predictor missingness, the current field named `mutual_information` is not generally mutual information. This is an exact formula consequence, not a philosophical objection.

---

## 8. Weight / support / missingness comparison

| Dimension | V547 | Current V550 | Lineage result |
|---|---|---|---|
| survey weights | none; explicitly exploratory unweighted | scalar weights can drive entropy and conditional entropy | `MUTATED` |
| weighted N | output `weighted_n=n` | weighted mass separately computed where weight series exists | `MUTATED` |
| NMI | absent | unweighted even when entropy reduction is weighted | new/mixed lane |
| Cramér's V | absent | unweighted even when entropy reduction is weighted | new/mixed lane |
| minimum question N | hard `MIN_N=300` | question readiness/support handled elsewhere; scalar field summary itself can emit under 50 with weak tier | `MUTATED` |
| secondary pair support | pair score requires complete-case N≥300 | joint secondary requires N≥50 | `MUTATED` |
| generic support | no wave-relative shared law | 0.5% of respondent total, floor 2, cap 30 | `MUTATED` |
| response missingness | numeric coercion + fixed-code deletion | typed response semantics retained in shared frame/distribution | `SPLIT_ACROSS_MULTIPLE_CURRENT_FUNCTIONS` |
| predictor missingness | candidate complete-case MI, but blanks on some string fields can become categories | blank predictor excluded; baseline/conditional universes differ | `MUTATED` |
| DK/refusal/IAP/not asked | collapsed/dropped by old numeric response normalization where mapped to excluded codes | typed flags exist in current response semantics | richer current metadata, but not an explicit branch-metric exclusion law |
| structural zero | no dedicated semantic representation proved | no dedicated branching-formula treatment established by D01 | `UNKNOWN` |

The exact current weight status can be `partial`; missing/invalid weight contributions become zero inside several weighted calculations. Local branching rows may label the result `weighted` whenever a weight series is passed, so downstream consumers must not infer that the local string alone proves fully populated survey weights.

---

## 9. Information-preservation / loss matrix

| Information | V547 output | Current V550 output family | Current preservation verdict |
|---|---|---|---|
| exact question identity | yes | yes | preserved |
| exact source | yes | yes | preserved |
| exact wave as execution filter | no; metadata label only | yes | improved/current scope repair |
| exact country as execution scope | no; pooled, country MI diagnostic | yes | superseded by scoped execution |
| predictor identity | top one only | all unary summary/matrix fields | richer current unary preservation |
| alternative predictor scores | discarded except winner | one summary row per indicator | richer current preservation |
| exact predictor value | no | yes in matrix; representative only in scalar summary | split |
| full response distribution by predictor value | no | yes in unary matrix | added current capability |
| weighted conditional distribution | no | yes in unary matrix when weights exist | added current capability |
| exact pair identity | winner only | primary+secondary for emitted rows | mutated; current search narrower |
| exact pair-specific support | no | joint N for emitted secondary row | improved but only selected star pairs |
| pair joint MI | used for winner, not emitted | no equivalent | lost |
| pair joint response topology | no | no in secondary summary | absent in both traced outputs |
| every alternative pair | not persisted but all searched | neither searched nor persisted outside primary star | capability loss |
| respondent membership | no | no in these determinicity outputs | absent in both |
| minority subgroup identity | no dedicated output | matrix can retain; outlier can suppress | split by family |
| subgroup directional reversal | not reconstructible | not reconstructible from secondary scalar alone | absent in traced scalar lineage |
| three-way parity | undiscoverable | undiscoverable by zero-gain greedy path | shared limitation |
| typed special-response state | collapsed by old numeric target | preserved in surrounding current semantics | current metadata improvement |
| historical `shape_class` | yes | no | lost |
| historical confidence heuristic | yes | no exact equivalent | mutated/lost formula |

Two distinctions are crucial:

1. **Current V550 can preserve more empirical information while possessing a narrower discovery search.** The unary matrix is richer than V547 output, but current secondary search is weaker than V547 pair search.
2. **A current table can preserve information that its bridge representation later loses.** In particular, the matrix retains `indicator_name` and `indicator_value`, but the inspected bridge does not alias them to `position_field` / `position_value`.

---

## 10. Current direct consumers identified

### 10.1 V550 orchestrators

`build_determinicity_wave_shard_v550.py` and `build_determinicity_repository_v550.py` directly invoke the branching/determinicity functions and materialize their tables. They are producer/orchestrator consumers of the shared current functions, not semantic proof of terminal necessity.

### 10.2 V550 → V551 bridge

`ddm_v550_bridge.py` directly reads the V550 table families.

Relevant lane mapping:

- `indicator_answer_matrix` → `derived_determinicity`
- `outlier_cohort_summary` → `derived_determinicity`
- `secondary_indicator_summary` → `derived_determinicity`
- `recursive_branch_nodes` → `derived_determinicity`
- `position_indicator_summary` → `position_context`

The bridge defines `v551_conditional_determinicity_eligible` for derived-lane rows when common relation gates pass, but `v551_eligible` is tied to the direct relation lane.

### 10.3 Exact conditioning-key loss in the bridge

For bridge base rows:

```text
position_field = row.position_field
position_value = row.position_value
```

`indicator_answer_matrix_rows()` emits:

```text
indicator_name
indicator_value
```

and does not emit literal `position_field` / `position_value` fields. No inspected current alias maps `indicator_name → position_field` or `indicator_value → position_value` in `_base_bridge_row`.

Therefore the matrix's exact empirical condition identity is not conserved into the bridge's position identity merely because the bridge row retains response/support mass.

This independently revalidates the narrow corrected VT3 R01 finding at the current base.

### 10.4 Canonical V551 compiler

Current `compile_v551_relation_evidence_atoms.py` imports and uses current `ddm_v551_atoms.py`.

`ddm_v551_atoms.py` defines:

`APPROVED_DIRECT_TABLES = {"answer_distribution", "country_answer_distribution"}`

and candidate construction requires:

- `bridge_evidence_lane == direct_relation_response`;
- source table in approved direct tables;
- substantive/non-special response plus current authority gates.

Thus canonical V551 does **not** consume the V550 `derived_determinicity` lane as canonical atom input.

### 10.5 `ddm_v551_conditional.py`

This helper is explicitly written to compile conditional determinicity from derived bridge rows. At the exact D01 base, however:

```python
from data.ddm_build_copy.ddm_v551_atoms import MIN_ATOM_SUPPORT, SOURCE_TABLE_PRIORITY
```

while current `ddm_v551_atoms.py` defines neither imported symbol.

The canonical V551 compiler also does not import/call this helper.

D01 classification: `INTENDED_BUT_UNWIRED_AND_IMPORT_BROKEN_AT_BASE`.

D01 does not claim no external caller anywhere can exist; it records the directly inspected current repository seam and leaves exhaustive downstream archaeology to D11.

---

## 11. Historical intended consumers separately recorded

### 11.1 Historical Attitude Cloud Access Contract

Historical design evidence expected a profile posterior builder to consume:

- identity/position predictors;
- likely anchor branch memberships;
- attitude-cloud co-signatures.

It also stated that positioned-answer meaning should condition on structural position, authority/target layer, attitude cloud, and power context.

Classification: `HISTORICAL_DESIGN_EVIDENCE`.

It proves a historical intended use for covariance/discovery outputs. It does **not** prove current authority to infer actor belief, identity, psyche, or response from population predictors.

### 11.2 Historical V526e

Historical V526e explicitly targeted branch co-signature and profile covariance for profile generation.

Classification: `HISTORICAL_DESIGN_EVIDENCE`.

It is adjacent downstream design context for why predictor/interaction discovery existed. It does not convert V547's statistical summaries into current runtime law.

### 11.3 Current disposition of historical reverse-use ambition

`UNKNOWN` as a lawful current capability requirement.

No canonical current determinicity→actor-profile consumer was proved by D01. D12 must decide whether any of this historical capability is terminally required, authoring-only, diagnostic, superseded, or unproven.

---

## 12. Contradictions with prior VT3 claims, if any

### 12.1 Corrected VT3 R01

No material contradiction on the rechecked current surfaces.

D01 independently confirms on current base:

- `indicator_answer_matrix` is a unary conditional contingency producer;
- `secondary_indicator_summary` is greedy primary+secondary, not exhaustive pair search;
- recursive branches are bounded greedy diagnostics, not complete joint structure;
- bridge matrix rows do not acquire exact condition identity through an `indicator_name/value → position_field/value` alias;
- canonical V551 excludes derived determinicity;
- `ddm_v551_conditional.py` remains unwired and its import contract remains broken.

**New D01 qualification:** R01 described the current secondary geometry correctly, but did not adjudicate historical V547 genealogy. D01 now proves that V547's pair search was **strictly broader** than the current secondary star search over their respective candidate sets.

### 12.2 VT3 R02 / R07

No contradiction on the rechecked core facts. D01's hostile XOR, Simpson, minority, and three-way fixtures reinforce the prior information-loss distinction between unary conditionals and joint incidence.

New D01 precision:

- V547 itself already possessed an exhaustive pair-discovery diagnostic that the current secondary function does not preserve;
- V547 nevertheless failed to preserve the joint cells needed to reconstruct the semantics of the interaction it discovered.

### 12.3 VT3 R05

No contradiction on the current repeated-scan/search geometry. D01 adds historical pair-search comparison and exact formula-unit discontinuity.

### 12.4 VT3 R11

Frozen R11 concluded that no universal all-question × twelve-field workload authority was demonstrated on the frozen base, with an explicit epistemic caveat.

D01 **does not import that conclusion onto current main**. Current R1 authority was merged after the frozen VT3 base. D01 records that current branching still loops the twelve hard-coded fields, but the legal status of that workload is reopened to current D06/D07 as required by the discovery campaign.

### 12.5 New contradiction found inside historical V547 itself

V547's executable pair search can correctly discover pure XOR, but `explain_shape()` classifies XOR as `flat` because it tests `top_mi < 0.005` before examining pair gain.

Therefore historical `top_interaction_1` and historical `shape_class` can disagree about whether interaction structure exists. These two V547 outputs must not be treated as mutually redundant encodings of one truth.

---

## 13. Unresolved assumptions

1. **Current workload authority:** D01 has not adjudicated whether R1 or another current authority mandates every question × twelve fields, any subset, or any conjunction. D07 owns the decision.
2. **R1 propagation:** D01 inspected current R1 orientation and current question-use machinery, but D06 owns row-by-row R1 → V550 eligibility provenance.
3. **Historical archive completeness:** D01 used the campaign's exact historical extracts and hashes. It did not possess an ordinary current-tree copy of every historical pack file; therefore claims about V526c/V526d/V526e beyond the extracted text are not made.
4. **V547 observed run reproducibility:** the historical review says 184 rows were written. D01 did not rerun the historical production database state, so it does not claim the old 184-row CSV can be byte-reproduced from today's database.
5. **Current noncanonical callers:** D01 established canonical V551 nonconsumption and the broken helper import. D11 must exhaustively inspect all current readers beyond this direct seam.
6. **Typed special responses inside branching:** current shared response semantics preserve typed states, but D01 found no branching-level flag filter. Whether inclusion is intentional authority or implementation residue is unresolved.
7. **Physical predictor frontier:** current respondent-position sources contain or recognize more fields than the fixed twelve. Their existence does not grant search authority.
8. **Structural interpretation:** D01 does not decide whether a particular predictor association lawfully represents class, religion, region, employment, or another V3 structural predicate.
9. **Actor use:** no population association is treated here as an actor belief, identity, disposition, or generated position.

---

## 14. Exact questions opened for D07 / D08 / D12 / D14

### D07 — Governed workload authority court

1. Does any accepted current authority mandate all-question × twelve-`INDICATOR_FIELDS` computation?
2. Which question classes, if any, authorize generic demographic predictor discovery rather than exact named conditions?
3. If pairwise diagnostic discovery is authorized, is the lawful search geometry exhaustive pairs, primary-star pairs, explicitly named pairs, or another governed frontier?
4. Does R1 carry workload-selection semantics, or only question/relation/structural semantics?
5. Does any authority permit automatic conjunction generation from separately permitted fields?
6. Are physically available but unsearched coordinates such as raw age or class-level ever authorized search inputs?

### D08 — Conditional empirical evidence ↔ attitude cloud unification/separation

1. Can `P(response | position=value)`, `P(Y response | X response)`, and `P(Y | position=value AND X=response)` share one predicate algebra while retaining distinct denominator, support, provenance, and semantic-use lanes?
2. Is historical V547 pair MI merely a diagnostic index over a deeper joint respondent fact, or is any scalar pair score semantically irreducible for a current lane?
3. Can historical V526e co-signature/profile-covariance discovery be regenerated from the same deeper incidence substrate without promoting it to actor psyche?
4. What exact joint identity must survive so Simpson/reversal and XOR configurations are reconstructible?

### D12 — Terminal human-capability backward court

1. Does terminal generated life require unrestricted pair discovery, or only exact authorized conditional facts?
2. Is full unary response topology terminally required where scalar salience is not?
3. Are subgroup reversals, Simpson-sensitive joints, and small stable minorities required to avoid flattening historically meaningful heterogeneity?
4. Is three-way/higher-order interaction discovery terminally required, or can it remain diagnostic/authoring-only?
5. Does any lawful terminal capability require historical reverse profile/covariance use, or is that historical ambition superseded/unproven?
6. What concrete human/world capability starves if V547-style unrestricted pair search disappears?

### D14 — Compute/cardinality benchmark court

1. Benchmark each current family separately: unary scalar summaries, matrix, outlier cohorts, secondary-star search, recursive trees.
2. Measure exhaustive historical-style pair search versus current primary-star search under identical respondent fields and semantics.
3. Measure weighting cost and ranking divergence on representative weighted shards.
4. Measure missingness-heavy shards separately because current score calculation can change with X-observed composition.
5. Measure materialized bytes and row counts for unary matrix versus scalar diagnostics.
6. Benchmark only after D07/D08/D12 define lawful semantic-equivalence gates; no cost result may silently choose the architecture.

---

## 15. Finite verdict

The capability genealogy closes as follows.

### `PRESERVED`

- the broad diagnostic capability to discover that question responses vary with social/demographic position coordinates;
- single-predictor identities and salience comparisons, though with materially changed formulas and grain;
- the ability to identify a strong marginal predictor.

### `MUTATED`

- predictor-salience mathematics: V547 unweighted sklearn MI in nats → current base-2 entropy reduction, optionally weighted;
- analysis grain: executable V547 pooled source-family × var-code → current source × wave × country × question;
- candidate universe: six non-country V547 fields plus separate country diagnostic → twelve fixed current fields with country as scope;
- interaction gain formula and support;
- missingness behavior;
- confidence/support semantics;
- pair identity/support representation.

### `LOST`

- V547 unrestricted all-pairs discovery over its finite-scored non-country candidate set;
- V547 pair joint-MI selection quantity as such;
- V547 `shape_class`;
- V547 score-based confidence formula;
- country MI as a pooled predictor diagnostic;
- direct numerical comparability to V547 MI thresholds;
- respondent membership at the published determinicity-artifact level;
- three-way parity discovery, although this last item is a shared historical/current limitation rather than a V550 regression from V547.

### `SUPERSEDED`

- country heterogeneity as an ordinary pooled predictor diagnostic, by explicit country-scoped current production;
- V547's loss of unary response topology, by current `indicator_answer_matrix`;
- the V526c-only nonrecursive boundary, by separately evolved/current recursive machinery historically closer to V526d.

### `SPLIT_ACROSS_MULTIPLE_CURRENT_FUNCTIONS`

The old umbrella of social-position determinicity now resolves into multiple current surfaces:

```text
single-field scalar salience
    -> position_indicator_summary

exact unary response topology
    -> indicator_answer_matrix

support-gated subgroup divergence
    -> outlier_cohort_summary

one-primary incremental pair search
    -> secondary_indicator_summary

greedy deeper branch search
    -> recursive_branch_nodes
```

No one current function is semantically equivalent to V547.

### `DIAGNOSTIC_ONLY`

Historical V526c's named predictor/interaction/shape mission was explicitly offline diagnostic. Current outlier/branch/salience surfaces are diagnostic computations in implementation terms, but D01 does not use that fact to adjudicate their canonical retention status.

### `UNKNOWN`

Historical reverse profile-generation/covariance ambitions as a current lawful requirement. The historical intent is real evidence; a current authority/consumer was not proved.

### Final lineage sentence

**V547 possessed a genuinely broader two-field discovery search than current V550's secondary-indicator function, but a dramatically poorer empirical retention surface; current V550 possesses richer unary conditional evidence, explicit country/wave scope, weights, typed response metadata, and additional diagnostic families, while changing the score mathematics and narrowing pair discovery. The derived determinicity material is bridged, but at this base it is not consumed by canonical V551, and its alternate conditional helper is unwired/import-broken.**

This is the finite D01 genealogy. It creates no replacement architecture, no preservation mandate, no deletion permission, and no actor-level semantic authority.
