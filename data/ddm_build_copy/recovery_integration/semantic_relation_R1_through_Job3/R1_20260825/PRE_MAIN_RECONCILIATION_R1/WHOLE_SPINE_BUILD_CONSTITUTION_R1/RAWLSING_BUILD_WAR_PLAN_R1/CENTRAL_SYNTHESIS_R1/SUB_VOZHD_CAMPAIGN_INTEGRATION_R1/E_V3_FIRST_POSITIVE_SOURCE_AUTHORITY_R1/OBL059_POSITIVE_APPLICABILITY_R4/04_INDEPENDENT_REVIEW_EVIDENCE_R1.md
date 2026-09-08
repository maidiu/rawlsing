# OBL059 R4 — INDEPENDENT REVIEW EVIDENCE R1

## Exact identities

Repository: `maidiu/rawlsing`

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r4-independent-review-r1`

Exact start:
`8715c131dd102d5952aa76b6f2549dfbba58cbee`

Frozen R4 candidate:
`830cc0442f34e8b28405006c031cc1d256893a17`

Known producer governed run:
`34230793386` — `success`

Prospective campaign instruction/adjudication:
`f7618257604c362097edb3c78dae8480a9499c4a`

Campaign adjudication tree:
`4f327169d238af9f42a274a5ce30f58ad8436d22`

Independent matrix/evidence freeze:
`4583df1b72b5ac663b57cf44d9a5a07a2e75a261`

Matrix blob:
`8a321db6a30d5c10963e90fd6bd02c7b3fc0ded7`

Independent test blob:
`79c3540f50542930339d519f1bd66e9776a3f314`

Governed wrapper blob:
`5b8a1d99e511255d5c6028d163ed1d13658befc2`

Court-spec blob:
`a8866869a19ce03574ae0d0e7debb10976ad18c4`

## Governed execution

Workflow run:
`34238158851` — `failure`

Job:
`102101147753` — `failure`

Protocol self-test:
`20 passed in 0.08s`

Court-spec validation:
`PASS`

Independent bounded review:
`5 failed, 18 passed, 124 subtests passed in 0.43s`

Artifact:
`10060765067`

Artifact ZIP SHA-256:
`e10aa524da47f00e459de29e3ba47ca6a936d4ddb7fa984d7239c54f477c4601`

Execution-only PR:
`#290` — closed unmerged after evidence capture.

## Passing findings

The independently frozen matrix passed the commissioned custom-Mapping and custom-protocol cases, built-in nested custom-object cases, heterogeneous non-JSON mapping keys, cycle/shared-reference/depth/breadth cases, nested bytes/set/frozenset/opaque combinations, deterministic equivalent-class receipts, structural distinction checks, ordinary R3 preservation, scope/authority/evidence/project-current rejection, adjacent-field non-substitution, unrelated internal-error visibility, and revision identity.

No positive applicability semantics were broadened by the review surface, and no current-effect flag was observed in passing controls.

## Blocking finding

A malformed required binding set to the exact built-in integer `10 ** 5000` fails at every required-binding position:

- `actor_id`;
- `subject_id`;
- `world_id`;
- `time_id`;
- `adp010_opportunity_id`.

R4 classifies every exact `int` as structurally JSON-safe. Because the surrounding packet is likewise classified structurally safe, R4 delegates to R3 rather than using R4's total diagnostic projection.

R3 correctly recognizes the binding as malformed and enters its serialization-safe negative-receipt path, but its projection preserves the large integer unchanged. Canonical proof encoding then raises:

`ValueError: Exceeds the limit (4300 digits) for integer string conversion`

instead of returning the required deterministic JSON-safe `NOT_DIRECTLY_APPLICABLE` / `MALFORMED_BINDING:<field>` receipt.

## Smallest exact blocker

`BLOCKER__OBL059_R4_EXACT_INTEGER_JSON_SAFE_CLASSIFICATION_OMITS_ENCODER_CONVERSION_LIMIT`

No broader semantic or jurisdictional claim is required for this FAIL.

## Review disposition

`FAIL__OBL059_R4_INDEPENDENT_REVIEW__LARGE_INTEGER_NEGATIVE_RECEIPT_CONSTRUCTION_INCOMPLETE`

Recommendation:
`FAIL__DO_NOT_ADOPT_OBL059_R4_CANDIDATE`

## Separation and no-current-effect attestation

`FRESH_INDEPENDENT_REVIEW_COUNT = 1`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`HQ_ADOPTION_CLAIMED = NO`

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
