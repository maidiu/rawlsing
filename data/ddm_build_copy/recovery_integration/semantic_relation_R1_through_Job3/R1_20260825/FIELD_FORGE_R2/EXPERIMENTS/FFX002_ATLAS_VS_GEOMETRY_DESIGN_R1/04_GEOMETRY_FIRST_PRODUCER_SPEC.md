# FFX002 — GEOMETRY-FIRST PRODUCER SPEC

Status: `EXPLORATORY_PRODUCER_DESIGN__NOT_CURRENT_ARCHITECTURE`

## 1. Purpose

Construct the strongest defensible **claim-scoped local geometric representation** of the same common respondent surface while exposing, rather than hiding, every methodological degree of freedom that can manufacture geometry.

The producer does not emit a universal social space. It emits a family of independently constructed local geometric views and their stability diagnostics.

## 2. Primary representation family

### 2.1 `POSITION_GEOMETRIC_VIEW`

Constructed only from Position Role Authority-admitted active position measurements.

### 2.2 `DISPOSITION_GEOMETRIC_VIEW`

Constructed only from exact lawfully coexposed disposition measurements with active ancestry disjoint from the position view.

### 2.3 `POSITION_DISPOSITION_DEPENDENCE_PROFILE`

Constructed **after** both spaces are frozen and only through exact respondent linkage in the common risk set. It may report region/coordinate-conditioned distributions, mutual information, neighborhood composition, or downstream predictive value. It is not named `HOMOLOGY` and does not re-optimize the spaces to maximize correspondence.

## 3. Method family and preregistration

The canary does not choose a method because one gives the cleanest picture.

### G0 — specific MCA baseline

If all primary active variables are categorical/source-categorical, fit specific MCA separately to position and disposition surfaces. Non-substantive states that should not create social distance may be passive **only** under exact semantic/exposure rules; they remain preserved in provenance and exact response facts.

### G1 — authorized block-balanced sensitivity build

If accepted Position Role Authority includes an exact `ANALYTIC_ROLE_BLOCK` manifest, fit an MFA/block-balanced categorical view in which authorized analytic blocks receive equal first-singular-value normalization or another preregistered standard MFA normalization.

This is a sensitivity/anti-questionnaire-dominance build, not proof that blocks have equal sociological importance.

### Geometry admissibility rule

Primary geometric claims may rely only on relational structure stable across all **lawfully applicable** preregistered builds. G0 and G1 are not cherry-picked after inspection.

If analytic block authority does not exist, G1 is `NOT_AUTHORIZED`, not improvised from questionnaire modules.

## 4. Exact estimand

Every build states exactly one of:

- `UNWEIGHTED_SAMPLE_RELATIONAL_VIEW`;
- `SOURCE_WEIGHT_ADJUSTED_RELATIONAL_VIEW` with exact weight-purpose authority;
- another explicitly governed target named by the execution court.

If a lawful source weight exists, run unweighted and authorized weighted views as separate preregistered estimand/weight perturbations when feasible. Do not call either the singular true geometry.

## 5. Active vs supplementary variables

- `ACTIVE_POSITION` variables construct only the position view.
- `ACTIVE_DISPOSITION` measurements construct only the disposition view.
- `SUPPLEMENTARY` variables/categories may be projected but do not create distances.
- `CONDITIONING_ONLY` variables define risk/context partitions or comparison strata and do not create distances.
- `EXCLUDED` variables are absent except for provenance/negative-control audits where specifically authorized.

A source measurement may not be active on both sides of the same cross-space analysis, including through derived ancestry.

## 6. Rare modality handling

Frequency alone never authorizes semantic collapse.

For each modality:

- active when role authority permits and design-set support is adequate for stable distance contribution;
- passive/supplementary when semantically real but too sparse for stable active leverage;
- collapsed only when source/semantic authority independently licenses the collapse;
- otherwise preserve as `LOW_SUPPORT_MODALITY` outside active geometry.

The rare-modality perturbation must compare active/passive/reweighted variants only when each variant is semantically lawful.

## 7. Routed / nonapplicable / missing states

The producer consumes actual exposure authority upstream.

Hard rule:

- nonexposed respondents do not receive a synthetic active `missing` modality;
- `NOT_ASKED_BY_DESIGN`, routed out, form not assigned, refusal, DK, source-missing, and unresolved exposure remain distinct;
- non-substantive response states may be passive or excluded from active distances under a frozen method rule, but never semantically deleted;
- unresolved exposure cannot enter the common risk set.

## 8. Ordinal and continuous variables

No arbitrary quantile binning.

Where such variables exist, preregister only semantically lawful alternatives, for example:

1. source-native ordered categories active;
2. continuous/ordered score supplementary to a categorical primary geometry;
3. an independently authorized substantive partition;
4. a mixed-data local method only if the execution court can state its estimand and distance assumptions before results.

A geometric relation that disappears across lawful encodings is `REPRESENTATION_SENSITIVE`.

## 9. Disconnected measurement rule

Build an exposure/coadministration graph from the exact common input.

If disposition measurements do not share a connected same-respondent empirical component at the required grain:

- build separate local component geometries;
- emit `NO_COMMON_METRIC_ACROSS_COMPONENTS`;
- never impute cross-component respondents merely to construct one space;
- never use semantic similarity of item labels as a bridge.

The same rule applies to materially disconnected position surfaces if the respondent/risk-set topology demands it.

## 10. Dimension retention

Do not retain dimensions by inertia/variance threshold alone.

On the **design partition only**:

1. evaluate `d = 1..d_max`, with `d_max = min(10, algebraic_rank)` for the bounded canary;
2. supplementary-project internal validation folds into bases learned without them;
3. calculate frozen query reconstruction/log-loss and neighborhood stability;
4. choose the smallest d whose validation error is within one standard error of the minimum and whose subspace stability passes the preregistered stability screen;
5. freeze d before final holdout evaluation.

If no d passes stability, emit `NO_STABLE_LOW_DIMENSIONAL_VIEW` rather than retaining an attractive unstable axis.

## 11. Stability diagnostics

For comparable builds, align subspaces by orthogonal Procrustes/principal-angle methods. For a claim to be `GEOMETRY_ROBUST` under a nuisance perturbation, target all applicable canary thresholds:

- largest principal angle for retained subspace <= 15 degrees;
- Spearman correlation of pairwise respondent distances >= 0.90;
- median Jaccard overlap of k-nearest neighborhoods >= 0.85;
- 10th-percentile neighborhood Jaccard >= 0.70;
- retained dimension count changes by <=1;
- >=80% of 200 design-set bootstrap replicates meet the same qualitative relation/stability condition.

Use `k = max(10, min(50, round(sqrt(N_design))))`, frozen from design N.

These are canary engineering thresholds, not universal sociological constants. They must be preregistered and reported individually.

## 12. Axis interpretation prohibition

Primary FFX002 comparison receives:

- numeric dimension IDs only (`D1`, `D2`, ...);
- inertia/eigenvalue diagnostics;
- modality and block contributions;
- coordinates/distances/neighborhoods;
- stability reports;
- supplementary projections;
- negative-control associations.

It does **not** receive or score labels such as `CAPITAL_VOLUME`, `LEFT_RIGHT`, `TRADITIONALISM`, `CLASS`, or `RELIGIOSITY`.

A geometry that requires narrative axis labeling to show value has failed the representation duel.

## 13. Output object

`GEOMETRIC_VIEW {
 build_id; representation_side; common_input_hash; estimand; method_family; active_measurement_ancestry; supplementary_refs; passive_modalities; block_manifest_ref; weight_ref; retained_d; basis; respondent_coordinates; modality_coordinates; contributions; pairwise/neighborhood_index; reconstruction_decoder_ref; stability_profile; regime_sensitivity_profile; negative_control_profile; provenance; allowed_claims; forbidden_claims
}`

## 14. Failure states

- `NO_STABLE_LOW_DIMENSIONAL_VIEW`
- `GEOMETRY_METHOD_SENSITIVE`
- `BLOCK_DOMINATED_GEOMETRY`
- `RARE_MODALITY_LEVERAGED_GEOMETRY`
- `EXPOSURE_ARTIFACT_GEOMETRY`
- `WEIGHT_ESTIMAND_SENSITIVE`
- `DISCONNECTED__NO_COMMON_METRIC`
- `ANCESTRY_CONTAMINATED__BLOCK_CROSS_SPACE_CLAIM`
- `NULL_NOT_DISTINCT`

Any of these may still leave a limited diagnostic geometry useful; none automatically makes the atlas win.
