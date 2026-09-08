# OBL059 R2 — GOVERNED BOUNDED COURT EVIDENCE

## Frozen target

Frozen R2 bounded-repair candidate:
`ff4f7c8a135997a4e4dd0b9dcb405a143fc6f749`

Exact R2 commission start:
`3892f32912dba21177f9663797e3f847822f4c7b`

Governed-court routing/evidence execution commit:
`eef570773198f31eaba190136fc63805b6ef6c72`

The frozen R1 candidate remains unchanged at:
`8f209b52f81a5c1bf5ed158782f25f56153ac68e`

## Exact governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34189982653`

Job:
`101945881980`

Python:
`3.12.14 / CPython`

Protocol self-test:
`20 passed in 0.08s`

Bounded-court spec validation:
`PASS`

R2 governed court:
`34 passed, 13 subtests passed in 0.11s`

Execution commit checked out by the court:
`eef570773198f31eaba190136fc63805b6ef6c72`

Frozen semantic candidate bound by the court spec:
`ff4f7c8a135997a4e4dd0b9dcb405a143fc6f749`

## Court coverage

The R2 court reruns the complete 30-test R1 governed bounded court through the R2 evaluator, then adds four exact repair/boundedness checks:

1. bytes in `actor_id` return a negative JSON-serializable receipt rather than raising;
2. a set in `world_id` returns a negative JSON-serializable receipt rather than raising;
3. an opaque object in `adp010_opportunity_id` returns a negative JSON-serializable receipt rather than raising;
4. ordinary JSON-safe positive and negative outputs are exactly equal to the frozen R1 evaluator outputs.

The three malformed binding cases retain their exact `MALFORMED_BINDING:<field>` negative reason and all no-current-effect attestations.

## Evidence artifact

Artifact ID:
`10041848360`

Artifact name:
`rabochii-court-receipt-34189982653`

Artifact ZIP SHA-256:
`ae35bfa9748e86b80b9d3fbc066fd396c27a914eca128eceaf2228c97278dc3c`

Artifact size:
`608 bytes`

Execution-only PR:
`#276`

PR state:
`CLOSED_UNMERGED`

PR synthetic merge identity used by the governed runner:
`78a18a8f7e073a23a78312d98e0dc2ad6b3ef1a6`

## Scope / non-action attestation

`INDEPENDENT_REVIEW_PERFORMED = NO`

`SELF_REVIEW_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ACTOR_CREATED_OR_ACTIVATED = NO`

`ADP008_PHASE_TRANSITION_EXECUTED = NO`

`ADP019_OCCURRENCE_ADMITTED = NO`

The green governed court proves only the commissioned bounded R2 repair. It does not substitute for any later distinct independent review or HQ adoption gate.
