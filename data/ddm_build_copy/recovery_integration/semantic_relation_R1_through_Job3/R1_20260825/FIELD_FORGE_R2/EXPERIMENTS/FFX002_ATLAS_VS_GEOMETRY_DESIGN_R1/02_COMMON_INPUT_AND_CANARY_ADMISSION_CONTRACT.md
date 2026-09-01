# FFX002 — COMMON INPUT AND CANARY ADMISSION CONTRACT

Status: `DESIGN_ONLY__BINDINGS_REQUIRED`

## A. Hard common-input manifest

Execution must bind one exact manifest containing all fields below. `UNRESOLVED` in any HARD field means the duel is invalid rather than approximated.

| field | requirement | hardness |
|---|---|---|
| current_starting_sha | exact accepted execution base | HARD |
| respondent_carrier_ref | governed respondent-level carrier | HARD |
| respondent_identity_ref | exact stable respondent identity binding | HARD |
| canary_scope | source family + wave/release + country/context + form/ballot/module/split where applicable | HARD |
| exposure_risk_set_ref | respondent x measurement actual exposure/opportunity authority with predicate provenance | HARD |
| position_role_authority_ref | bounded accepted dispositions for every candidate position variable and analytic-role block | HARD |
| position_measurement_manifest | exact qimpl/source refs + category semantics + ancestry | HARD |
| disposition_measurement_manifest | exact respondent-facing items/complex members + source-structure type + ancestry | HARD |
| estimand | exact representation target | HARD |
| weight_purpose_ref | governed purpose or explicit NONE for unweighted sample-descriptive target | HARD |
| weight_ref | exact carrier if weight_purpose_ref != NONE | HARD |
| design_regime_manifest | mode/form/language/randomization/design strata needed for nuisance controls | HARD where observed |
| train_holdout_manifest | deterministic split after authority bind | HARD |
| lawful_alternate_encodings | only alternate encodings semantically permitted before results | HARD for perturbation use |

Hard equality:

`COMMON_INPUT_HASH_ATLAS == COMMON_INPUT_HASH_GEOMETRY`.

The common-input hash excludes only the representation-specific method specification.

## B. Canary admission — minimum requirements

A source/scope is admitted only if all minimum conditions hold.

### B1. Respondent/exposure authority

- exact governed respondent IDs exist;
- actual exposure/opportunity can be classified without using response missingness as a routing proxy;
- respondent exposure to every active disposition item is either positively established or explicitly excluded from the common risk set;
- form/ballot/module/split/country/prior-answer predicates are conserved where relevant.

This is the absolute gate. Catalog presence, J candidacy, and positive item-routing authority alone are insufficient.

### B2. Position surface

After competent Position Role Authority adjudication, the canary must retain at minimum:

- `>=4` variables admitted `ACTIVE_POSITION` for the primary build;
- those variables must span `>=3` independently authorized analytic role families **if the source lawfully supplies three**;
- no one source/instrument block may be the only source of position heterogeneity;
- at least one further position candidate may be supplementary/conditioning/excluded; the design must remain valid when attractive variables are removed.

Preferred:

- `>=6` active variables across `>=4` role families;
- at least one bounded multi-role variable for the active/supplementary perturbation;
- at least one ordinal/continuous or source-ordered variable for the representation perturbation.

The numerical minima are canary design adequacy rules, not universal social ontology.

### B3. Disposition/repertoire surface

Minimum:

- `>=8` separately respondent-facing disposition measurements;
- actual coexposure authority for the respondent risk set used;
- measurements drawn from `>=2` source/instrument blocks or batteries so block perturbation is identifiable;
- at least one higher-order lawful J subset of order `>=3` with adequate design-set support.

Preferred:

- `12–30` disposition measurements across `>=3` source/instrument blocks;
- multiple empirically nonredundant higher-order J subsets;
- at least one minority complex that is observed but not high-support.

A multi-response answer-slot set does not satisfy the repeated-item requirement merely because it has many coded members.

### B4. Estimand/weight

At least one of the following must be frozen:

1. `UNWEIGHTED_SAMPLE_DESCRIPTIVE_RELATIONAL_SURFACE`; or
2. a source-weight-adjusted relational estimand with exact documented weight purpose and carrier.

If governed weights exist for the chosen scope, preferred execution includes both unweighted and authorized weighted views as an explicit perturbation. Their difference is reported, not resolved by convenience.

### B5. Holdout feasibility

Default when one context supplies enough respondents:

- 70% design / 30% final holdout;
- deterministic hash-based respondent assignment using a stored random salt/seed;
- stratify/hash within exact design or exposure strata when required to avoid violating the risk set;
- all semantic freezes and fixture definitions precede split outcome inspection.

If multi-context evidence exists and a context holdout is substantively lawful, the execution court may preregister a context holdout instead. It may not switch holdout type after observing comparative results.

## C. Support tiers

For conditional-distribution and motif candidate generation:

- `SUPPORTED`: raw n >=25 for unweighted cells, or Kish effective n >=25 for weighted descriptive screening;
- `LOW_SUPPORT`: positive observed support below that threshold;
- `ZERO_OBSERVED_IN_RISK_SET`: zero in the exact lawful risk set;
- `NOT_COMPOSABLE_OR_NOT_EXPOSED`: never converted to zero.

`LOW_SUPPORT` observations remain in respondent/exact-fact carriers and minority-preservation metrics; they are not promoted to stable generalizations absent stronger evidence.

## D. Position/disposition ancestry separation

Before build, recursively expand exact source ancestry of every derived active variable/complex.

Primary cross-space analysis requires zero direct or derived measurement overlap. If one source measurement has plausible roles on both sides, create alternate preregistered builds:

- position-primary: active position / supplementary or excluded disposition;
- disposition-primary: active disposition / supplementary or excluded position.

Never activate it on both sides and then call the resulting association evidence.

## E. Block manifests

Store three different block systems without collapsing them:

- `SOURCE_INSTRUMENT_BLOCK` — questionnaire/battery/module provenance;
- `ANALYTIC_ROLE_BLOCK` — authority-frozen grouping for a declared geometric use;
- `EMPIRICAL_COADMINISTRATION_BLOCK` — exact shared respondent exposure/risk set.

Only `ANALYTIC_ROLE_BLOCK` may be used for method balancing, and only if its semantic authority is explicitly bound. `SOURCE_INSTRUMENT_BLOCK` supplies nuisance perturbations; it does not receive sociological weight by item count.

## F. Rejection states

Return a typed rejection instead of relaxing the experiment:

- `REJECT__NO_GOVERNED_RESPONDENT_IDENTITY`
- `REJECT__ACTUAL_EXPOSURE_NOT_MATERIALIZABLE`
- `REJECT__POSITION_SURFACE_TOO_THIN_AFTER_AUTHORITY`
- `REJECT__DISPOSITION_SURFACE_TOO_THIN_OR_NOT_COEXPOSED`
- `REJECT__ESTIMAND_OR_WEIGHT_PURPOSE_UNRESOLVED`
- `REJECT__ACTIVE_ANCESTRY_CANNOT_BE_SEPARATED`
- `REJECT__HOLDOUT_NOT_FEASIBLE_WITHOUT_DESTROYING_RISK_SET`

The correct successor is another already governed candidate source/scope, not source acquisition and not weakened law.
