# OBL059 R3 — GOVERNED BOUNDED COURT EVIDENCE

## Exact identities

Repository:
`maidiu/rawlsing`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r3`

Exact starting HEAD:
`917ee1655f7a4c26277896ef12d788acce15a1c9`

Campaign adjudication consumed prospectively:
`9695eab9fa5b31db4bfc6c7bb977e5af95bbc66c`

Failed frozen R2 candidate retained unchanged:
`ff4f7c8a135997a4e4dd0b9dcb405a143fc6f749`

Frozen R3 candidate:
`4fdb897e8a089787d7407197fd49bbd1ef51f2ef`

Governed evidence execution:
`860078598cd1376c368177c51b183f651b9c8f45`

Candidate implementation blob:
`782fa22158435cc37330652d592b2be594d938c7`

Governed court blob:
`e4261f1b36d61daac3909427dc0b0a8daef97686`

Governed wrapper blob:
`5112eb503af9efccb4c712d507376d6aab212dbb`

Court-spec blob:
`e4a47b33e0465d65cddcbf217a85c7f75adb4555`

## Governed execution

Workflow run:
`34197429485`

Job:
`101968185230`

Protocol self-test:
`20 passed in 0.09s`

Court-spec validation:
`PASS`

R3 governed court:
`44 passed, 61 subtests passed in 0.21s`

Artifact:
`10044437787`

Artifact ZIP SHA-256:
`f847ddd0dc8568a6253944bd5560a4842bcc46e46c547d7db51d10fba78e24d2`

Execution-only PR:
`#284`

PR disposition:
`CLOSED_UNMERGED`

Court terminal:
`PASS__OBL059_R3_BOUNDED_REPAIR_GOVERNED_COURT_GREEN__NO_SELF_REVIEW`

## Exact repair evidence

The court reruns the full inherited R2 court, which itself reruns the complete 30-test R1 court, and then adds the R3 regressions.

Direct R3 coverage proves:

1. malformed mappings with `bytes` keys return `MALFORMED_BINDING:<field>` negative receipts at each of the five required-binding positions;
2. circular lists return deterministic negative receipts at each required-binding position;
3. circular mappings return deterministic negative receipts at each required-binding position;
4. the original `bytes`, `set`, `frozenset`, and opaque-object malformed shapes close at every required-binding position;
5. nested non-serializable and cyclic structures close at every required-binding position;
6. repeated equivalent malformed semantic classes yield deterministic receipt/proof results;
7. each fallback receipt is itself JSON serializable and keeps the malformed diagnostic binding structured rather than coercing it into a valid string identifier;
8. valid JSON-safe positive, negative, and JSON-safe malformed controls remain exactly equal to frozen R2 behavior;
9. wrong opportunity scope, forbidden authority alias, and `PROJECT_CURRENT` controls remain negative with all forbidden effects false;
10. deliberate internal `TypeError` and `ValueError` raised outside the commissioned malformed-receipt boundary propagate rather than being converted into semantic negatives;
11. the R3 revision identity is exact.

The R3 implementation does not key correctness to exception-message text. Serialization exceptions are handled only inside a dedicated JSON-serialization probe after a required binding has already been semantically classified malformed.

## Separation of duties

`INDEPENDENT_REVIEW_PERFORMED_BY_R3_REPAIR_WORKER = NO`

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_TERMINAL = NOT_CLAIMED`

The green court proves only the commissioned R3 bounded repair. SUB-VOZHD E retains authority to commission exactly one fresh distinct review against the frozen R3 candidate.

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
