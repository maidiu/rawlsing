# OBL059 POSITIVE_APPLICABILITY — R7 INDEPENDENT REVIEW EVIDENCE R1

Repository:
`maidiu/rawlsing`

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r7-independent-review-r1`

Exact review start:
`845954893d9ab18dc4ed8a6764a6f866a43dc571`

Campaign authority:
`be663a75df53bd973b20b603093127e48badc09e`

Frozen R7 candidate:
`87bb8a7bbdd22085ad0cd759230b9efdc74d3fb5`

Known producer evidence:
`09b3512db3a13a87b03e6168d7f7afb05e035325`
run `34256575217`

Independent matrix freeze / evidence execution:
`7766ff96e80699aa2f11117dd559c773bc7a6c98`

Independent matrix blob:
`b689cc4d88cdf0111b64a12c9cad3e8e56a55d26`

Independent test blob:
`862966203d8c32463259ebbecbc3751a21e1a4cb`

Governed wrapper blob:
`fa53bdd001c6a3c9c84b0d1d59d7972d4899e9b4`

Court-spec blob:
`5b909053713c770ae5ef6a8e9ad06304dd4aa544`

## Governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34257521929`

Run conclusion:
`failure`

Job:
`102166977830`

Job conclusion:
`failure`

Protocol self-test:
`20 passed in 0.11s`

Court-spec validation:
`PASS`

Independent review court:
`3 failed, 14 passed, 10 subtests passed in 0.23s`

Artifact:
`10068486980`

Artifact name:
`rabochii-court-receipt-34257521929`

Artifact size:
`617 bytes`

Artifact ZIP SHA-256:
`99d17e22ce3d13e44dfadaf0b373026b1dfae34682c9cb6df7a8562b32569e7d`

Artifact expired at evidence capture:
`false`

Execution-only PR:
`#303`

PR disposition:
`CLOSED_UNMERGED`

PR synthetic merge identity recorded by governed run:
`853063a3091897ca59132998c62e6876979fafdb`

## Passing preservation controls

The independent matrix confirmed the following remained correct:

- a stable authorized custom `Mapping` carrying the exact positive fixture is semantically equivalent to the exact-dict form;
- stable custom-Mapping negative and project-current controls remain negative;
- outer snapshot failures through the independently exercised carrier paths return deterministic `PACKET_MALFORMED` receipts;
- unused convenience methods are not required when the one snapshot succeeds without them;
- a one-shot carrier can be snapshotted once and is not consulted again during later evaluation;
- a mapping-like object that is not an authorized `Mapping` instance does not gain carrier status by resemblance;
- oversized exact integers inside a stable outer Mapping remain deterministically negative;
- the inherited R6 in-flight integer-setting boundary remains total;
- unrelated deliberate implementation errors after successful snapshot remain visible;
- adjacent narrative/routing/classification fields do not substitute for competent evidence;
- wrong scope, wrong authority, stale evidence, and project-current execution remain negative;
- equivalent successful and failed outer-snapshot cases are deterministic;
- R7 revision identity is exact.

## Blocking result family

The review found one blocker family after the outer snapshot boundary: nested values that are themselves custom `Mapping` objects can still raise from field access used by inherited scope/evidence checks instead of producing a deterministic negative receipt.

### F1 — nested opportunity Mapping

Review case:
`test_09_nested_opportunity_mapping_failure_must_close`

An exact-dict packet supplies a custom `Mapping` at `opportunity`. Inherited exact-scope evaluation calls `opportunity.get(...)`. The nested Mapping raises `RuntimeError("nested-get-failure")`, and that exception escapes instead of returning a negative receipt.

### F2 — top-level evidence Mapping

Review case:
`test_10_nested_evidence_mapping_failure_must_close`

An exact-dict packet supplies a custom `Mapping` at `evidence`. Inherited evidence evaluation calls `evidence.get("subject_classification")`. The nested Mapping raises `RuntimeError("nested-get-failure")`, and that exception escapes instead of returning a negative receipt.

### F3 — nested actor evidence Mapping

Review case:
`test_11_nested_actor_evidence_mapping_failure_must_close`

An exact-dict packet supplies a custom `Mapping` at `evidence.actor_activation`. Inherited evidence evaluation calls `actor.get("semantic_owner")`. The nested Mapping raises `RuntimeError("nested-get-failure")`, and that exception escapes instead of returning a negative receipt.

These three failures are manifestations of the same exact boundary defect. No broader semantic or jurisdictional failure is required for this review result.

## Smallest exact blocker

`BLOCKER__OBL059_R7_NESTED_MAPPING_FIELD_ACCESS_CAN_ESCAPE_AFTER_OUTER_SNAPSHOT`

The R7 outer-carrier snapshot is bounded, but nested Mapping values consumed later by scope/evidence checks are not placed behind an equivalent deterministic field-access boundary. A malformed nested Mapping can therefore raise before a negative receipt is completed.

## Review disposition

`FAIL__OBL059_R7_INDEPENDENT_REVIEW__NESTED_MAPPING_ACCESS_ESCAPES_NEGATIVE_RECEIPT`

`FRESH_INDEPENDENT_REVIEW_COUNT = 1`

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
