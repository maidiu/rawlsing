# FFIF006 — HARD-ZERO VS BOUNDED LOSS RULES

## Typed criticality states

Every claim-invariant/dimension pair receives exactly one state before comparison:

1. `CRITICAL_INVARIANT__ZERO_UNAUTHORIZED_LOSS`
2. `BOUNDED_APPROXIMATION_ALLOWED`
3. `INFORMATION_NOT_REQUIRED_BY_CLAIM`
4. `TOLERANCE_AUTHORITY_UNRESOLVED`
5. `NOT_APPLICABLE_TO_ASSERTION_SLOT`

No missing value defaults to bounded approximation.

## Zero means zero after the lawful semantic boundary

`ZERO_UNAUTHORIZED_LOSS` is evaluated relative to the frozen common semantic input. A lawful lossy TTAR may already have produced a claim-specific post-transform state universe, with source-native ancestry preserved. Once the CIM binds that universe, no view may introduce further unregistered loss.

Always hard-zero for same-claim comparison:

- empirical-unit identity;
- risk-set identity;
- estimand identity;
- semantic-input hash and ordered TTAR sequence;
- source-native ancestry/replayability;
- special-state distinctions constitutive of the claim;
- assertion-slot and scale identity;
- PRA role identity where the operand depends on it.

Failure is invalidity, not a large loss score.

## Claim-derived hard zero

Some invariants become hard-zero only because of the proposition:

- `EXACT_STATE_EXISTENCE`: one lost lawful state fails;
- `EXACT_CONFIGURATION_EXISTENCE`: one lost constitutive branch fails;
- exact minority-branch retention: low prevalence does not relax existence;
- exact topology/connectivity: one unauthorized bridge or deleted component fails;
- exact higher-order J: pairwise approximation cannot satisfy the slot.

No prevalence threshold may be selected after observing how small the branch is.

## Bounded approximation

Approximation is lawful only when all are true:

1. the assertion slot is approximate rather than exact;
2. the loss dimension is registered and measurable;
3. the unit/scale and direction of worse performance are declared;
4. the tolerance has an authority/evidence basis;
5. uncertainty interaction is declared;
6. the tolerance and evaluation procedure are frozen before compared outputs;
7. hard-zero invariants remain vetoes;
8. source-native replay remains possible.

Eligible examples include conditional-distribution error, neighborhood distortion, target-specific predictive degradation, calibrated reconstruction error, and bounded compression fidelity.

## Information not required

`INFORMATION_NOT_REQUIRED_BY_CLAIM` means a view is not penalized for lacking that invariant when adjudicating this claim. It does not mean the information is nonexistent or globally disposable. The loss remains visible in the view's general loss manifest.

`UNDEFINED_FOR_VIEW` is also not `FALSE`.

## No compensatory scalar

Hard-zero failures are noncompensatory. A large predictive gain cannot offset minority erasure, risk-set drift, or ancestry loss. Bounded dimensions remain a vector unless an authority contract explicitly licenses aggregation among commensurable units for the same proposition. Engineering cost and downstream utility may never be added to empirical-information loss as one score.

## Fail states

- `INVALID__CRITICAL_INVARIANT_LOSS`
- `INVALID__UNREGISTERED_LOSS_DIMENSION`
- `INVALID__TOLERANCE_NOT_FROZEN`
- `INVALID__TOLERANCE_AUTHORITY_MISSING`
- `LOSS_WITHIN_AUTHORIZED_BOUND`
- `LOSS_EXCEEDS_AUTHORIZED_BOUND`
- `LOSS_UNRESOLVED_DUE_TO_UNCERTAINTY`
- `INFORMATION_NOT_REQUIRED__NO_SUFFICIENCY_PENALTY`

