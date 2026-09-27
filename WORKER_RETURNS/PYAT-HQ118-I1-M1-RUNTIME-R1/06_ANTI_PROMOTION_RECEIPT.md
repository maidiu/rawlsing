# Anti-Promotion Receipt

## Runtime import boundary

The M1 production module imports only generic PRE553 integrity/authority/empirical object machinery.

It does not import:

- M01 compositor implementation;
- FIABC;
- ASTRA;
- Candidate A/B/C;
- structural-admission runtime;
- Field Forge;
- M2 learned-product release runtime;
- B5 learned-product lifecycle runtime;
- actor/V3 runtime.

The M01 interface is proven only in tests by supplying exact M01 graph objects to the neutral M1 bundle builder.

## Fixed downstream-effect firewall

Every M1 disposition and determinant receipt fixes these effects to false:

- `product_release_effect`
- `current_selection_effect`
- `structural_admission_effect`
- `consumer_permission_effect`
- `causal_truth_effect`
- `actor_v3_effect`

If a family validator requests any positive downstream effect, M1 returns `INTEGRITY_FAILURE`; it does not propagate the request.

## Semantic claim firewall

M1 itself never constructs semantic polarity from empirical patterns.

A family validator may emit a separately identified P1 truth-bearing claim only when the exact binding's `output_semantic_contract` says:

`truth_bearing_claim_emission = EXPLICITLY_AUTHORIZED`

Otherwise claim emission is an integrity failure.

`RULE_SATISFIED` alone does not create structural, causal, current, released, consumer-authorized or actor truth.

`RULE_NOT_SATISFIED` alone does not create negative semantic truth.

## State-conservation firewall

M1 preserves distinct upstream states and does not collapse:

- OBSERVED_ZERO -> ZERO_SUPPORT;
- ZERO_SUPPORT -> VALID_EMPTY;
- VALID_EMPTY -> RULE_NOT_SATISFIED;
- NONCOMPARABLE -> negative truth;
- COVERAGE_LIMITED -> complete/global absence;
- BLOCKED -> false;
- UNKNOWN/UNRESOLVED -> denied;
- INTEGRITY_FAILURE -> valid empty.

The hostile court serializes VALID_EMPTY, OBSERVED_ZERO and ZERO_SUPPORT into distinct M1 dispositions and proves distinct disposition identities.

## No universal substantive validator

There is no generic implementation of:

- significance;
- minimum support;
- effect-size threshold;
- association strength;
- weighting rule;
- missingness rule;
- comparability;
- pooling/composition;
- estimator;
- semantic polarity;
- causal or structural interpretation.

The generic runtime can only execute a separately registered validator whose immutable registration exactly matches the explicit family-rule binding.

## Currentness boundary

`EXACT_PINNED_REPLAY` forbids a currentness claim.

`CURRENT_GOVERNED_USE` requires an exact current-selection AuthorityRef in the binding and its exact positive snapshot in the input authority closure.

M1 consumes this premise; M1 does not maintain or infer currentness.

## Freeze

`M1_DISPOSITION_IDENTITY != M2_RELEASE_IDENTITY != B5_CURRENT_SELECTION_IDENTITY != I04_STRUCTURAL_ADMISSION_IDENTITY`

I1 therefore closes the generic M1 runtime mechanics only. It does not complete M2, B5 lifecycle runtime, post-execution learned-product dispatch, live source proving, or Field Forge.
