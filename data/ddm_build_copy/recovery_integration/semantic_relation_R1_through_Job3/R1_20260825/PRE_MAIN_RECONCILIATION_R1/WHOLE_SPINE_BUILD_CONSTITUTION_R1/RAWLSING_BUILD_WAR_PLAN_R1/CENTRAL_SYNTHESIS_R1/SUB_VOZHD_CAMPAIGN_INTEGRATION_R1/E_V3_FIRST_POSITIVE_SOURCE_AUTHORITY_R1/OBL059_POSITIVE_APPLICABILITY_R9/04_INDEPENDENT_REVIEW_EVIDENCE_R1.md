# OBL059 POSITIVE_APPLICABILITY — R9 FRESH DISTINCT INDEPENDENT REVIEW EVIDENCE R1

## Exact identities

Repository:
`maidiu/rawlsing`

Reviewer branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r9-independent-review-r1`

Exact review start:
`568bd4973934f34c93838e9334759666057baa2a`

Campaign authority:
`90adb6897b804ea0b18ea893f509db6051c5bc2d`

Campaign tree:
`4e1029e7b0db11f5b14b071b81d3b2196d1f3c71`

Frozen R9 target:
`222b027c4a92767c0a206faef2314bbd4b16ca7c`

Producer governed evidence consumed as prior context only:
`097349010d96d217a445050eb76b364dc27c13a4`

Producer run/job:
`34271784800` / `102214872620`

Independent review matrix/evidence freeze:
`19434a2763385810eccc96139690dae900497dd1`

Independent matrix blob:
`8496709845c556727a8c79cab93a07487427c901`

Independent test blob:
`c3eb79486945a6adaf6774ae003a2ab01536aa24`

Governed wrapper blob:
`60e373ddcf006ce87e1e7fa3351bd6867b63838c`

Court-spec blob:
`e4999846016191ba22acfd8ebb97c4a85f8e221b`

## Governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34278508906`

Job:
`102237337231`

Protocol self-test:
`20 passed in 0.11s`

Court-spec validation:
`PASS`

Independent review court:
`3 failed, 13 passed, 27 subtests passed in 0.29s`

Workflow conclusion:
`failure`

Artifact:
`10076663213`

Artifact name:
`rabochii-court-receipt-34278508906`

Artifact ZIP SHA-256:
`b3217979b9f8bca99a9fa8d6b0de49acd3eccfabcc58a0dd8e45e96025ae28c0`

Execution-only PR:
`#318`

PR disposition:
`CLOSED_UNMERGED`

PR synthetic merge identity:
`f6002a0aa1765f7482bb7cb3565464ed91b31b50`

## Independent finding

The fresh matrix found one remaining coherent-view blocker, reproduced in three independently frozen directions.

R9 captures references to custom consumed Mapping carriers before nested traversal. That prevents a carrier from replacing a later parent slot, but the captured object itself remains mutable until its own snapshot occurs. An earlier consumed carrier can therefore change the internal contents of a later captured custom carrier before that later carrier is snapshotted.

### F1 — evidence snapshot changes captured opportunity contents

The opportunity carrier initially contains a wrong `world_id` and is therefore semantically negative. A custom top-level evidence carrier changes that captured opportunity carrier's internal `world_id` to the correct value while evidence is being snapshotted. R9 later snapshots the now-changed opportunity carrier and returns:

`DIRECT_POSITIVE_APPLICABILITY`

instead of the required negative result:

`OPPORTUNITY_SCOPE_MISMATCH:world_id`

### F2 — opportunity snapshot changes captured actor contents

The captured actor-activation carrier initially has `semantic_owner = WRONG_AUTHORITY`. A custom opportunity carrier changes that captured actor carrier's internal owner to the competent ADP-007 owner during opportunity snapshot. R9 later snapshots the changed actor carrier and returns `DIRECT_POSITIVE_APPLICABILITY` instead of:

`ACTOR_ACTIVATION_WRONG_AUTHORITY`

### F3 — earlier component snapshot changes later component contents

The captured actor-activation carrier again initially has the wrong authority. A custom subject-classification carrier changes the actor carrier's internal owner during its earlier snapshot. The later actor snapshot observes the changed value and R9 returns `DIRECT_POSITIVE_APPLICABILITY` instead of the required negative result.

All three incorrect-positive cases produced proof SHA-256:
`61e90bf3942ccefb627cdc0fc49dfa9ad22e0c494c470dd7a7fd7fe4bfba6ae4`

## Smallest blocker

`BLOCKER__OBL059_R9_CAPTURED_CUSTOM_MAPPING_REFERENCES_REMAIN_MUTABLE_UNTIL_LATER_SNAPSHOT`

The repair must establish a coherent immutable semantic view of each consumed custom carrier before any other consumed carrier can change that carrier's later-observed contents. Merely capturing object references is insufficient.

## Passing preservation findings

The same independent matrix confirmed:

- the exact R8 parent-slot replacement case remains negative;
- mutation of an already-frozen earlier component by a later component does not rewrite the earlier result;
- shared/aliased custom carriers are snapshotted once;
- stable custom Mapping carriers preserve exact-dict meaning at all five consumed nodes;
- outer and nested custom Mapping composition remains lawful;
- actually invoked `keys()` and indexing snapshot failures produce deterministic field-specific negative receipts;
- the nested `actor_activation.actor_id = 10 ** 5000` case returns deterministic JSON-safe negative receipts under supported integer-conversion settings;
- positive/negative threshold neighbors and oversized exact integers inside nested built-in structures remain total under inherited stable projection;
- wrong scope, wrong authority/source, stale evidence and adjacent narrative/routing/classification fields remain negative;
- unrelated deliberate implementation errors after successful preparation remain visible;
- repeated and concurrent exact-dict evaluation is deterministic;
- exact R9 revision identity is preserved;
- all reviewed positive and negative paths retain every no-current-effect flag.

Therefore the R8 nested oversized-integer finding is independently closed by R9. The terminal FAIL is solely required by the remaining coherent-view internal-mutation blocker above.

## Separation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R9_CANDIDATE = 1`

`FROZEN_R9_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

## No-current-effect attestation

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
