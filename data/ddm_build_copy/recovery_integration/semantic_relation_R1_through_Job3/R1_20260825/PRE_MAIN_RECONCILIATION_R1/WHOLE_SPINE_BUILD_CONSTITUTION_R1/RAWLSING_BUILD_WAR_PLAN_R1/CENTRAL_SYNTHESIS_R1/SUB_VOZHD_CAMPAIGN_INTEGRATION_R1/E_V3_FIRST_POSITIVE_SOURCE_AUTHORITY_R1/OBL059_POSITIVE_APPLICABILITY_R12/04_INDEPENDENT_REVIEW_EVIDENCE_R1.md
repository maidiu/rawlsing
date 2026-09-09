# OBL059 POSITIVE_APPLICABILITY — R12 INDEPENDENT REVIEW EVIDENCE R1

ROLE:
`RABOCHII INDEPENDENT REVIEWER`

REPORTS TO:
`SUB-VOZHD E`

Reviewer branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r12-independent-review-r1`

Exact start:
`68ef776638a15b72955bccd587d3fa2b7fde2b11`

Campaign authority:
`2be93091bd5b1b6b479bd9c46686d0fc4ce35b81`

Frozen R12 target:
`6962ab0bdb2f66cc266b0e88b5ff5016b361a9a1`

Candidate executable blob:
`c87f73608472222a4ff7598d9a8a96f186e1cd00`

Producer governed evidence consumed only as prior context:
`759f17c1190971854dc0e0129ba6989a83079bb2`

Producer run/job:
`34299273634` / `102302527312`

Independent review-surface freeze:
`d52171340fa89f829f8a3503a9009c32e787db4d`

Independent review matrix blob:
`f0d87481ed8e4cf1409e2540dd92049ef9294263`

Independent review test blob:
`8c9100a15e58c427b7b2e3b94b7b1dd7a7f527f4`

Governed wrapper blob:
`97ff2fe42857b5a23798950d70ca668724367ef9`

Court-spec blob:
`d5169ac0fdd5553a3ebae8a2ee0408b86cae520e`

## Governed evidence

Workflow:
`Rabochii Governed Bounded Court`

Run/job:
`34304771174` / `102319067039`

Python:
`3.12.14`

Protocol self-test:
`20 passed in 0.12s`

Court-spec validation:
`PASS`

Independent court:
`1 failed, 18 passed, 16 warnings, 59 subtests passed in 2.85s`

Artifact:
`10086240841`

Artifact ZIP SHA-256:
`c2d7fd010e656911d31b2b2e6be96b8fc405228da0d1ecea08b5cad9aca75b42`

Execution-only PR:
`#336`

PR disposition:
`CLOSED_UNMERGED`

## Independent finding

Disposition:
`FAIL__OBL059_R12_INDEPENDENT_REVIEW__NESTED_PATH_RESOLUTION_CAN_REWRITE_INITIAL_NEGATIVE_ENTRY_VIEW`

Smallest blocker:
`BLOCKER__OBL059_R12_CUSTOM_PARENT_PATH_RESOLUTION_CAN_REWRITE_NESTED_ENTRY_VIEW_IN_CHILD`

The independent matrix began with an exact valid synthetic packet, changed the parent entry-state `evidence.actor_activation.semantic_owner` to `WRONG_AUTHORITY`, and then wrapped `evidence` in a custom Mapping whose only semantic-changing behavior occurs when `__getitem__("actor_activation")` is invoked while resolving that nested path.

The parent object remained unchanged because R12 performs the observation in a child process. However, inside each fresh child, resolving the nested path invoked the custom evidence parent's `__getitem__`, which changed the child-local actor owner to the valid ADP-007 owner before the nested actor view was materialized. Both repeated observations therefore agreed on the rewritten positive child-local view. R12 then consumed that view and returned `DIRECT_POSITIVE_APPLICABILITY` with reason `EXACT_SCOPE_AND_REQUIRED_EVIDENCE_PROVED` instead of preserving the initially negative parent entry state.

This is a direct failure of the required coherent observable-entry invariant. Fresh-child isolation prevents state leakage back to the parent, but it does not by itself guarantee that the semantic nested view corresponds to the untouched parent entry state when traversal of the custom parent can change the nested target before it is observed.

The first evidence-parent reproduction was sufficient to establish the blocker. The second planned outer-parent variant in the same test method was not reached after the first assertion failed and is not relied upon for this finding.

## Passing review families

All other 18 frozen test methods passed. Those passing families covered:

- R11 cache warming across all five consumed Mapping positions;
- unrelated memoization, lazy-index and access-counter private-only changes;
- observable key-order variation with normalized equal contents;
- stable `ChainMap`, generic layered composition, precedence/shadowing, read-only proxy-backed layers and tombstone-like semantics;
- outer+nested custom composition;
- shared/aliased carriers;
- actual observable value/key disagreement failing closed;
- cross-carrier changes in both directions remaining child-local;
- cycles, excessive depth, excessive breadth, timeout and invoked Mapping-operation failures;
- exact-dict positive/negative equivalence;
- initially negative authority/scope/source/stale cases under ordinary custom carriers;
- oversized positive/negative integers and threshold neighbors under reviewed runtime integer-conversion settings;
- proof determinism/equality/distinction;
- repeated/concurrent custom evaluation;
- malformed-input handling;
- `NONCURRENT_SYNTHETIC` and `PROJECT_CURRENT` controls;
- deliberate unrelated implementation-error visibility;
- revision identity and no-current-effect flags.

These passes do not cure the reproduced path-resolution blocker.

## Separation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R12_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

No rerun or repair was performed after the candidate blocker reproduced.

## Current-effect attestations

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`CURRENT_POSITIVE_OBL056_ENTRY_CREATED = NO`

`ACTOR_CURRENT_TRANSITION_CREATED = NO`

`ADP008_CURRENT_PHASE_TRANSITION_CREATED = NO`

`ADP019_CURRENT_OCCURRENCE_ADMITTED = NO`

`OBL055_EXECUTION_TRIGGERED = NO`

`ENCOUNTER_OR_OEE_EFFECT_CREATED = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061 = HARD_BLOCKED`

`POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`

`PROJECT_CURRENT_FIRST_CANARY_OEE = NOT_AUTHORIZED`
