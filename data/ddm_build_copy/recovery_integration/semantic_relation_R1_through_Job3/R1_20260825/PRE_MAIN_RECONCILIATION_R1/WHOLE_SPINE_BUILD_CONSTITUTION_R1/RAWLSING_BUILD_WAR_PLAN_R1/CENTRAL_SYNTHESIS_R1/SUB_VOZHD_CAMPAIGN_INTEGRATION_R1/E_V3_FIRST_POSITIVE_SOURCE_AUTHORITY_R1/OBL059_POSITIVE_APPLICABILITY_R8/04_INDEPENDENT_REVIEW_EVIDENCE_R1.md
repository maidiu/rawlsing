# OBL059 R8 — INDEPENDENT REVIEW EVIDENCE R1

## Exact identities

Repository:
`maidiu/rawlsing`

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r8-independent-review-r1`

Exact review start:
`8049c2e3e24cd6f6c0e2e45b65ad29131082261c`

Campaign authority consumed prospectively:
`e02d410ab89a8cc969272cacdb395a2ae2b7a489`

Campaign tree:
`5a510aa6ec3f3144aaabf749dcf6ccccc4c849b2`

Frozen R8 candidate:
`9298b13533d45b885d422ce5d89907406b90d97f`

Independent review-surface freeze / evidence execution:
`f63f9eca64c0afaecd14ff9e24a5cc9ee43cdd90`

Independent matrix blob:
`5430302e0f884c5b1cf6e03ef64816e206669390`

Independent test blob:
`a2ad745ad0373e651e8bb095ee7713e0d0aab3d6`

Governed wrapper blob:
`99b42d6c85a2fbaafcc50a05d9d71d1947fc9153`

Court-spec blob:
`589dabeb0344b837cb8e10bbec06ba8eab0d1c53`

## Governed execution

Workflow run:
`34264425959`

Job:
`102190115470`

Protocol self-test:
`20 passed in 0.10s`

Court-spec validation:
`PASS`

Independent review court:
`12 failed, 11 passed, 34 subtests passed in 0.32s`

Workflow conclusion:
`failure`

Artifact:
`10071207765`

Artifact name:
`rabochii-court-receipt-34264425959`

Artifact size:
`617 bytes`

Artifact ZIP SHA-256:
`bea510a74e36912acec0af8a31517498ec00fa63f51c252c2c87909d044f2276`

Execution-only PR:
`#309`

PR disposition:
`CLOSED_UNMERGED`

PR synthetic merge identity recorded by the governed run:
`2667f576f43b1f8ff35cdf7fa1c02f98ebdabbb8`

## Interpretation of the reported failures

Ten subfailures came from the generic `iter` / `len` variants of the review helper. In that helper shape, `dict(mapping)` selected the available `keys()` + `__getitem__()` snapshot path, so the deliberately throwing `__iter__` or `__len__` methods were not consulted. The resulting positive receipts therefore do not establish a candidate defect and are not counted as semantic blockers.

The `keys()` and `__getitem__()` failure variants at the five consumed nodes did close through the R8 snapshot boundary, which is consistent with the intended one-shot snapshot law.

Two independently meaningful failures remain and are sufficient for semantic FAIL.

## F1 — sequential nested snapshots lack cross-node consistency

The matrix began with an exact-dict packet whose `evidence.actor_activation.semantic_owner` was deliberately wrong. The inherited exact-dict disposition was correctly negative:

`ACTOR_ACTIVATION_WRONG_AUTHORITY`

The packet then used a custom `opportunity` Mapping whose snapshot content itself was valid but whose first snapshot step replaced the later, not-yet-snapshotted `actor_activation` node with valid content.

R8 snapshots `opportunity` first and only then copies/continues the working packet. The later evidence read therefore consumed the changed actor node, and the final disposition became:

`DIRECT_POSITIVE_APPLICABILITY`

Thus an initially negative packet can become positive solely because an earlier nested snapshot changes a later consumed node during sequential preparation.

Smallest blocker:

`BLOCKER__OBL059_R8_EARLIER_NESTED_SNAPSHOT_CAN_REWRITE_LATER_CONSUMED_NODE_INTO_POSITIVE`

This is the smallest blocking finding required for the review terminal.

## F2 — nested oversized evidence value can still reopen receipt construction failure

A stable custom `actor_activation` Mapping was successfully snapshotted to an exact dict whose nested `actor_id` was `10 ** 5000`, while the top-level required `actor_id` remained valid.

The semantic evaluator correctly reached:

`ACTOR_ACTIVATION_SCOPE_MISMATCH:actor_id`

but negative receipt proof hashing later attempted canonical JSON encoding of the nested oversized integer and raised Python's integer-to-string conversion `ValueError` instead of returning the negative receipt.

This is a separate real finding. It does not change the smallest blocker chosen above because F1 already produces an incorrect positive result directly within the newly repaired sequential nested-snapshot boundary.

## Passing preservation findings

The governed review also confirmed the ordinary exact-dict positive/negative controls, stable custom Mapping equivalence across the five consumed nodes, one-shot nested snapshots, outer-plus-nested snapshot composition, deterministic shared one-shot negative handling, top-level oversized required-binding closure across supported integer settings, scope/source/stale/adjacent-field negatives, unrelated post-snapshot implementation-error visibility, exact R8 revision identity, and all no-current-effect fields for passing cases.

## Review disposition

Recommendation:
`FAIL__DO_NOT_ADOPT_OBL059_R8_CANDIDATE`

Review terminal:
`FAIL__OBL059_R8_INDEPENDENT_REVIEW__SEQUENTIAL_NESTED_SNAPSHOT_CROSS_NODE_CONSISTENCY_NOT_CLOSED`

## Separation and no-current-effect attestations

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R8_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ACTOR_CREATED_OR_ACTIVATED = NO`

`ADP008_PHASE_TRANSITION_EXECUTED = NO`

`ADP019_OCCURRENCE_ADMITTED = NO`

`CAUSAL_USE_PERMISSION_OWNED = NO`

`CONTACT_WITNESS_INDEPENDENCE_OWNED = NO`

`ENCOUNTER_CREATED = NO`

`AUTHORITY_INDEX_MUTATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061 = HARD_BLOCKED`
