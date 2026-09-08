# OBL059 R2 — INDEPENDENT BOUNDED REVIEW EVIDENCE R1

## Exact identities

Repository: `maidiu/rawlsing`

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r2-independent-review-r1`

Exact start:
`63ef0f1096c47b0f80471c2477d33aa4e3233c21`

Frozen R2 candidate:
`ff4f7c8a135997a4e4dd0b9dcb405a143fc6f749`

Independent review-surface freeze:
`d3e4853017eed3bf6767645aec7553fdd9103065`

Review role:
`RABOCHII_INDEPENDENT_REVIEWER_OBL059_R2_R1`

Candidate modification authority: `NONE`

## Governed execution

Workflow run: `34193469052`

Job: `101956110511`

Protocol self-test: `20 passed in 0.10s`

Court-spec validation: `PASS`

Independent bounded review: `2 failed, 2 passed in 0.18s`

Artifact: `10043014619`

Artifact ZIP SHA-256:
`0fce4838ad4555224fced0c277aa12c3fdae6d681cf4c468213d1f14fc91ec3e`

Execution-only PR: `#277`, closed unmerged.

## Passing controls

The already-covered malformed `bytes` required-binding case returned a JSON-safe negative receipt, and the frozen R2 revision identity was exact.

## Blocking results

### F1 — malformed mapping key form still escapes

A malformed `actor_id` value containing a mapping with a `bytes` key should fail closed as `MALFORMED_BINDING:actor_id`.

Instead, R1 receipt hashing raises:

`TypeError: keys must be str, int, float, bool or None, not bytes`

R2 catches `TypeError`, but its fallback is conditional on the exception text containing `is not JSON serializable`. This standard JSON failure message does not contain that phrase, so R2 re-raises instead of returning a negative receipt.

### F2 — circular malformed binding still escapes

A malformed circular-list `world_id` should fail closed as `MALFORMED_BINDING:world_id`.

Instead, R1 receipt hashing raises:

`ValueError: Circular reference detected`

R2 catches only `TypeError`, so this standard non-JSON-serializable malformed binding also escapes instead of returning a negative receipt.

## Smallest exact blocker

`BLOCKER__OBL059_R2_NEGATIVE_RECEIPT_FALLBACK_COVERS_ONLY_ONE_JSON_ERROR_SHAPE`

The frozen R2 candidate claims a serialization-safe negative-receipt repair for malformed non-JSON values, but the outer evaluator recognizes only `TypeError` whose text contains `is not JSON serializable`. Standard JSON serialization failures with other `TypeError` messages or `ValueError` are outside that gate.

No broader semantic or jurisdictional defect is required for this FAIL.

## Review disposition

`FAIL__OBL059_R2_INDEPENDENT_REVIEW__NON_JSON_MALFORMED_BINDING_FALLBACK_INCOMPLETE`

No repair was performed. No second review was commissioned or run.

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

`HQ_ADOPTION_CLAIMED = NO`
