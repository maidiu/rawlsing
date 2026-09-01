# FFX002 — DECISION RULE

Status: `PREREGISTERED_DESIGN__NO_WINNER_SELECTED`

## 1. Order of adjudication

Decision occurs in this order only:

1. common-input lawfulness;
2. hard experimental-validity gates;
3. atlas adequacy profile;
4. geometry adequacy profile;
5. comparative preservation / stability / compression / downstream value;
6. terminal state.

A later favorable metric cannot cure an earlier hard invalidity.

## 2. Gate 0 — common-input validity

Require:

- governed respondent carrier/identity;
- exact actual-exposure/risk-set authority;
- same common-input hash on both sides;
- frozen Position Role Authority;
- frozen position/disposition ancestry separation;
- exact estimand/weight purpose;
- frozen design/holdout manifest.

Failure ->

`EXPERIMENT_INVALID__COMMON_INPUT_OR_ESTIMAND_NOT_LAWFUL`

with a typed subreason.

## 3. Gate 1 — hard validity attacks

All must pass:

- M13 exposure-risk-set poison invariance;
- M14 zero active direct/derived cross-space ancestry overlap + successful ancestry-trap detection;
- FFP008 holdout leakage audit;
- M18 provenance/replayability;
- M19 uncertainty-posture correctness;
- disconnected components not forced into one metric;
- no ungoverned category recode or weight use.

Any failure -> `EXPERIMENT_INVALID__<typed_reason>`.

Do not call a representation the loser when the experiment itself is invalid.

## 4. Atlas adequacy profile

`ATLAS_ADEQUATE` requires all hard atlas properties:

- M01 exact high-support fact/configuration recall = 1.0 at the lossless floor;
- M02 exact minority fact existence/support recall = 1.0 at the lossless floor;
- FFP001 counterfeit clone does not multiply substantive facts or change substantive query results;
- exact raw facts survive compact-pruning and pooling variants;
- motif/candidate generation is holdout-clean and preregistered;
- M18 replay passes;
- no hidden distance/similarity metric is used for equivalence/pruning.

Compact-atlas quality is then profiled rather than hard-won:

- M03/M04 held-out query performance;
- M05/M06 higher-order/counterpattern preservation;
- M08 motif stability;
- M15/M16 complexity/compression;
- FFP012/013 explosion/pruning sensitivity.

If the lossless floor is valid but compact atlas is operationally intractable, type `ATLAS_EMPIRICALLY_VALID__COMPACT_REPRESENTATION_INADEQUATE` rather than erasing its empirical advantage.

## 5. Geometry adequacy profile

`GEOMETRY_ADEQUATE` requires:

- no hard gate failure;
- a stable retained subspace exists on the design partition;
- for each geometry relation claimed as robust, M07/M10/M11 pass the preregistered nuisance thresholds;
- M20 counterfeit-block test passes for the authorized block-balanced build where available, and claimed G0 structure remains within robustness thresholds;
- strong cross-space/downstream relation value is >99th percentile of respondent-link null under M12;
- geometry output/value does not depend on semantic axis labels;
- final holdout projection/reconstruction is computed without refit.

A geometry may be `GEOMETRY_METHOD_SENSITIVE` and still be useful as a derived diagnostic view. That is not identical to `GEOMETRY_ADEQUATE_FOR_PRIMARY_ROLE`.

## 6. Primary-role preservation floor for geometry

Geometry cannot earn primary representational role if compression destroys empirical structure beyond these bounded canary tolerances while atlas preserves it:

- M01 high-support configuration recall >=.95;
- M02 minority configuration recall >=.90;
- M05 higher-order J/motif recall >=.90 on frozen high-support targets;
- M06 median nonmodal/counterpattern probability-mass error <=.02;
- M03 held-out median TV no worse than atlas by >.02.

These are loss-tolerance gates for this duel, not claims that 5% or 10% loss is ontologically harmless.

## 7. Material comparative advantages

A `MATERIAL_GEOMETRY_ADVANTAGE` exists when geometry is lawful/adequate and at least one holds:

1. A3 `ATLAS_PLUS_GEOMETRY` improves held-out log loss over A1 `ATLAS_ONLY` by >=10%, paired 95% descriptive bootstrap interval excluding 0;
2. geometry achieves equivalent query fidelity within the preservation floor at >=4x lower serialized representation size;
3. geometry supplies a stable neighborhood/rank relation that is intrinsically unavailable to the nonmetric atlas, survives all nuisance/null tests, and yields measurable held-out downstream gain.

A `MATERIAL_ATLAS_ADVANTAGE` exists when atlas is lawful/adequate and at least one holds:

1. A3/A4 improves held-out log loss over `GEOMETRY_ONLY` by >=10%, paired interval excluding 0;
2. geometry violates any primary-role minority/high-order/counterpattern preservation floor while atlas preserves those facts;
3. atlas answers an exact conditional/J query with materially lower M03/M05 error not recoverable from geometry at equivalent cost;
4. geometry is method-sensitive where atlas substantive query results are invariant under the corresponding nuisance change.

No advantage is created by a metric on which the other representation is intentionally undefined unless a downstream consumer has a preregistered need for that capability.

## 8. Terminal decision states

### `GEOMETRY_EARNS_PRIMARY_REPRESENTATIONAL_ROLE`

Require **all**:

- `GEOMETRY_ADEQUATE`;
- geometry passes the primary-role preservation floor;
- `MATERIAL_GEOMETRY_ADVANTAGE` exists;
- atlas compact representation is materially inferior on economy, sparse-query interpolation, or downstream value;
- no `MATERIAL_ATLAS_ADVANTAGE` remains on a required empirical invariant that primary geometry would erase.

This state still requires exact/raw empirical provenance beneath geometry. “Primary” does not mean geometry replaces source facts.

### `GEOMETRY_EARNS_DERIVED_CLAIM_SCOPED_VIEW_ROLE`

Use when geometry is lawful and supplies some stable useful view/compression/diagnostic, but one or more of the following prevents primary status:

- material incremental value is limited;
- method sensitivity remains bounded but real;
- atlas retains required exact/minority/higher-order facts not recoverable inside geometry;
- geometry's distinctive value is neighborhood/visual/diagnostic rather than foundational representation.

### `ATLAS_FIRST_SUFFICIENT__GEOMETRY_ADDS_NO_MATERIAL_VALUE`

Require:

- `ATLAS_ADEQUATE`;
- compact atlas is operationally viable on the canary;
- no `MATERIAL_GEOMETRY_ADVANTAGE` under frozen holdout/complexity metrics;
- geometry either duplicates atlas-recoverable organization or is materially method-sensitive/null-indistinct.

Geometry may still be retained as a nonessential exploratory visualization, but the experiment provides no evidence it deserves architectural weight.

### `NON_SUBSTITUTABLE_MULTI_REPRESENTATION_ARCHITECTURE_SUPPORTED`

Require:

- both representations are lawful/adequate at their claimed roles;
- both `MATERIAL_GEOMETRY_ADVANTAGE` and `MATERIAL_ATLAS_ADVANTAGE` exist on nonredundant invariants/capabilities;
- combined A3/A4 supplies material value beyond either alone or each is necessary for different required downstream queries;
- neither advantage is an artifact of semantic labeling or metric aggregation.

Canonical example pattern: atlas uniquely preserves exact minority/contradictory higher-order structure while geometry uniquely supplies stable economical local neighborhoods/interpolation.

### `BOTH_FAIL__REPRESENTATION_PRIMITIVES_REQUIRE_REDESIGN`

Use only when the experiment is valid but:

- compact atlas fails through explosion/pruning brittleness/consumer unusability; **and**
- geometry fails through instability/null-indistinction/information destruction;
- no bounded role assignment salvages either representation family.

Preserve exact respondent facts and all negative results for redesign.

### `EXPERIMENT_INVALID__COMMON_INPUT_OR_ESTIMAND_NOT_LAWFUL`

Use whenever Gate 0 fails. More precise invalid states from Gate 1 may be returned under the same invalid family.

## 9. Tie/ambiguity rule

If both representations are lawful but confidence intervals/perturbation profiles do not separate their material value, do not break the tie by preference, theoretical pedigree, or elegance.

Return:

`INCONCLUSIVE__BOTH_LAWFUL__NO_MATERIAL_ROLE_SEPARATION_ON_CANARY`

and state which additional **already governed** canary contrast would be informative. Do not acquire a new source.

## 10. Forbidden master score

Never compute:

`w1*stability + w2*compression + w3*minority + ... = architecture_quality`.

That merely moves ontology into arbitrary metric weights. The terminal decision must expose which gates and distinct material advantages were satisfied.
