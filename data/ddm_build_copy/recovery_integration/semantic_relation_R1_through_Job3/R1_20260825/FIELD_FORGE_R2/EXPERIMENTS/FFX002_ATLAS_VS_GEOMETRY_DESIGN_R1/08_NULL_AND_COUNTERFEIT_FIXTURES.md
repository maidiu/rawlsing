# FFX002 — NULL AND COUNTERFEIT FIXTURES

Status: `DESIGN_ONLY`

These fixtures are deterministic synthetic attacks derived only from the admitted canary. They do not add sources or empirical claims.

## 1. Fixture law

Every fixture must preserve an exact parent-build pointer and state which empirical invariants it deliberately preserves and destroys. Synthetic rows/columns are never merged into governed survey evidence.

Required manifest:

`fixture_id; parent_common_input_hash; transformation_version; seed; preserved_invariants[]; deliberately_destroyed_invariants[]; synthetic_ids[]; output_hash; allowed_uses; forbidden_interpretations`.

## 2. `BLOCK_COUNTERFEIT_CLONE`

### Construction

Select one lawful `SOURCE_INSTRUMENT_BLOCK` containing >=2 active measurements. Create synthetic fixture columns with new synthetic IDs but identical respondent values, exposure states, category codes, and recursive ancestry pointing to the originals.

No substantive information is added:

`I(original_block ; clone_block | original_block) = 0` by construction.

### What it preserves

- respondent universe;
- exposure topology;
- marginals/joints;
- all substantive empirical information;
- estimand/weights;
- source-block ancestry relation.

### What it changes

Only representation count/column multiplicity.

### Geometry challenge

Raw unbalanced methods may rotate because duplicated columns carry extra mass. FFX002 does not pretend this cannot happen. Instead it asks whether the geometry **claimed as stable structure** survives the counterfeit and whether the authorized block-balanced variant is invariant.

### Atlas challenge

The raw synthetic carrier may contain clone columns, but the substantive atlas layer must detect ancestry-equivalent identity and avoid minting duplicate configuration/dependence facts. If fact count or query probability changes merely because the same information is represented twice, atlas-first has smuggled source representation count into reality.

## 3. `BLOCK_REMOVAL` and `BLOCK_DOWNWEIGHT`

Remove the largest source/instrument block from a fixture copy. If an authorized analytic-role block exists, separately fit the preregistered downweighted geometry variant.

Do not treat removal as a new estimand. It is a hostile information ablation asking what organization is actually carried by the remaining measurements.

Atlas requirement: facts over untouched variables remain exactly replayable. Geometry requirement: report subspace/neighborhood displacement and loss of held-out utility.

## 4. `RARE_MODALITY_LEVERAGE`

Choose a semantically real rare modality from the design partition. Construct only semantically lawful method variants:

- active;
- passive/supplementary;
- bounded reweighting if allowed.

Never construct a `DELETE_RARE_CATEGORY` empirical fixture. The category remains in raw facts under every method state.

Purpose: separate `rare empirical reality` from `rare geometric leverage`.

## 5. `ACTIVE_SUPPLEMENTARY_SWITCH`

Requires an exact variable for which accepted role authority permits both active and supplementary use for different claim-scoped views.

Produce two frozen builds differing only in that use. The result measures method sensitivity to a legitimate semantic adjudication fork; it does not let statistical fit decide which semantic role is true.

## 6. `ORDINAL_CONTINUOUS_ENCODING_FAMILY`

Where available, create a family only from frozen lawful encodings:

- source-native categories;
- ordered/continuous supplementary projection;
- independently authorized substantive partition;
- justified mixed-data representation if preregistered.

Forbidden fixture: quantile bins created solely to make the software categorical.

## 7. `EXPOSURE_RISK_SET_POISON`

This is a hard-invalidity control.

### Construction

For selected measurements, take respondents positively known from the accepted exposure artifact to be nonexposed (form not assigned, routed out, prior-answer gate, module absent, etc.). In a synthetic poisoned copy only, encode them with one generic `__MISSING__` value as if they had been measurement rows.

### Correct behavior

The common-input compiler must enforce actual exposure before either representation consumes the surface. Therefore clean and poisoned builds must produce identical lawful substantive outputs after risk-set enforcement.

Any geometry or atlas dependence on the poison means missingness/nonexposure has entered empirical structure. Return `EXPERIMENT_INVALID__EXPOSURE_ARTIFACT`.

## 8. `RESPONDENT_LINK_ASSOCIATION_NULL`

### Construction

After independent position and disposition surfaces are frozen, permute **whole disposition respondent profiles** among respondents within exact lawful strata that preserve required exposure/design/mode/weight-domain constraints.

Use >=999 deterministic seeded permutations.

### Preserves

- position surface;
- disposition internal joint structure and marginals;
- each side's geometry/atlas when constructed independently;
- exposure topology class and sample design strata;
- questionnaire topology.

### Destroys

Substantive respondent-level position↔disposition linkage.

### Purpose

Any post-hoc dependence/downstream-value measure that is equally strong under this null cannot be promoted as discovered cross-space relational organization.

## 9. `WITHIN_ITEM_J_NULL`

Independently permute each disposition item among respondents **within its exact common risk/design strata**.

### Preserves

- item marginals;
- exposure/opportunity topology;
- category frequencies;
- number of questions and blocks.

### Destroys

- respondent-level pairwise/higher-order disposition association;
- genuine repertoire/complex co-possession beyond chance under the null scheme.

Purpose: ask whether geometry or atlas higher-order organization exceeds what instrument topology and marginals alone can generate.

## 10. `SEMANTIC_LABEL_SCRAMBLE`

Replace all human-readable position/disposition labels with stable opaque IDs before representation fitting and primary metric scoring. Keep a sealed reversible mapping for later audit only.

The numeric representation must be identical apart from display metadata.

This prevents the evaluator from awarding geometry credit because an axis can be rhetorically named after seeing category labels. Atlas facts must likewise not depend on natural-language labels to define equality or redundancy.

## 11. `ANCESTRY_TRAP`

Create one synthetic derived position variable whose formula/lineage includes an exact active disposition measurement, or vice versa. Give it an innocuous synthetic name.

Both producers must recursively detect the overlap from ancestry rather than name matching and block the cross-space claim.

If the trap is not detected, the experimental architecture fails before any representation comparison.

## 12. `MEASUREMENT_REGIME_NEGATIVE_CONTROL`

Where current source authority exposes mode, form/ballot, randomized arm, interview language, privacy, order, or administrative implementation identifiers, preserve them as diagnostic-only variables.

Project/condition them after primary representation construction. If a major geometric relation or atlas dependence is largely a regime split, type the result accordingly and forbid strong structural promotion.

Exact randomized source designs are especially valuable because they can identify measurement sensitivity more strongly than observational regime differences. Randomization must be proven, never inferred from field names.

## 13. Synthetic-fixture abstention

A fixture that cannot be constructed lawfully is `NOT_INSTANTIABLE_ON_CANARY`. The worker must not alter semantic authority simply to make every fixture runnable.

The exceptions are the universal hard controls: exposure poison, holdout leakage audit, semantic-label scramble, and ancestry trap. The admitted canary/architecture must support those controls or the duel is not execution-ready.
