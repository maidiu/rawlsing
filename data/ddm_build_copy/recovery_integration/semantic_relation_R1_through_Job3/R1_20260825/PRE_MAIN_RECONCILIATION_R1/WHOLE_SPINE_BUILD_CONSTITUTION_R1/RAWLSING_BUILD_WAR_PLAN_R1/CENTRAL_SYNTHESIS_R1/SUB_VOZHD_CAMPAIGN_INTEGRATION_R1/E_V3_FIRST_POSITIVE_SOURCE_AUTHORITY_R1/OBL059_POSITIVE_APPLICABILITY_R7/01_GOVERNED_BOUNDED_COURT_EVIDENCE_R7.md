# OBL059 POSITIVE_APPLICABILITY — R7 GOVERNED BOUNDED COURT EVIDENCE

Campaign authority consumed prospectively:
`07ad7844e5b817615f3ff371e06e2dcef349b0bd`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r7`

Exact worker start:
`6468d775eb15076e8ca243c95180fdfecb41ce27`

Failed frozen R6 candidate retained unchanged:
`5ca7380bd17b3dec271fe5a8c6bf22656f55b647`

R6 review blocker repaired:
`BLOCKER__OBL059_R6_CUSTOM_MAPPING_PACKET_CAN_ESCAPE_VIA_CALLER_CONTROLLED_KEYS_BEFORE_NEGATIVE_RECEIPT`

Frozen R7 candidate:
`87bb8a7bbdd22085ad0cd759230b9efdc74d3fb5`

Candidate executable blob:
`f33a63b25f1a5990a21bd841e1237a10100a4ca3`

Producer court blob:
`89c165eb21de9410240e1a6f76a8df57cc7b545c`

Court-spec blob:
`928b8bdda1c8f4a4d3fbd5b83dc1d3a9d4814cb8`

Corrected governed wrapper blob:
`ab4fe2947cee2c095d8255f5060e228aaea51a56`

Corrected governed evidence execution:
`09b3512db3a13a87b03e6168d7f7afb05e035325`

## Repair holding

Frozen R1 authority permits general `Mapping` carriers, so R7 preserves that carrier law.

R7 introduces one bounded outer-carrier snapshot boundary:

- exact dictionaries continue through frozen R6 unchanged;
- non-Mapping carriers continue through inherited law unchanged;
- a non-exact `Mapping` is snapshotted exactly once;
- if caller-controlled carrier traversal raises an ordinary exception, R7 returns the existing deterministic `PACKET_MALFORMED` negative receipt without consulting the carrier again;
- if snapshotting succeeds, the exact dictionary snapshot is evaluated by frozen R6 unchanged;
- nested custom values remain governed by the existing R4-R6 exact-built-in projection/isolation rules;
- evaluation after a successful snapshot occurs outside the carrier-traversal exception boundary, so unrelated implementation errors remain visible.

The producer court confirms that a well-behaved custom Mapping containing the complete authorized positive fixture remains semantically equivalent to the exact-dict form, while malformed or traversal-failing carriers remain negative and create no current effect.

## Initial governed run — routing mismatch only

Initial evidence execution:
`fc728176df38193c792bba8634a03f3d4ff0d53b`

Initial run/job:
`34256292696` / `102162839576`

Initial result:
`53 failed, 82 passed, 288 subtests passed`

Initial artifact:
`10067998593`

Initial artifact ZIP SHA-256:
`dea658057904a41a97c8a93c63721234bcd6e045e645c2fd7914e668596cc622`

The initial red run exposed only producer-wrapper routing defects: the R7 subclass shadowed an inherited helper with an incompatible signature, and several inherited preservation tests patched a separately loaded R6 module rather than R7's actual frozen R6 delegate. The frozen R7 candidate was not modified. Only the governed wrapper routing was corrected.

## Corrected governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34256575217`

Run conclusion:
`success`

Job:
`102163794223`

Job conclusion:
`success`

Python:
`3.12.14`

Protocol self-test:
`20 passed in 0.07s`

Court-spec validation:
`PASS`

R7 producer court:
`90 passed, 333 subtests passed in 0.23s`

Artifact:
`10068105467`

Artifact name:
`rabochii-court-receipt-34256575217`

Artifact size:
`607 bytes`

Artifact ZIP SHA-256:
`ca4948edc16f959b2e4ff37e936dedc5d1c071e4620bc02274af921d18dc7eac`

Artifact expired at evidence capture:
`false`

Execution-only PR:
`#301`

PR disposition:
`CLOSED_UNMERGED`

PR synthetic merge identity recorded by governed run:
`dc58f1275216ee7e3ab8ecd2738599bdef5e90e9`

## Court coverage holding

The corrected court reruns inherited R1-R6 controls through the R7 public evaluation path and adds direct checks for:

- well-behaved authorized custom Mapping positive equivalence;
- custom outer Mapping traversal failures;
- the reproduced throwing-`keys()` case with hidden oversized malformed binding;
- mapping lookalikes that are not Mapping instances;
- positive-looking but incomplete custom Mapping content remaining negative;
- nested custom Mapping values remaining isolated inside exact-dict malformed bindings;
- deterministic repeated Mapping snapshots for equivalent content;
- exact-dict byte-for-byte preservation against frozen R6 ordinary controls;
- visibility of deliberate unrelated TypeError, ValueError, and RuntimeError after a successful snapshot;
- inherited R6 stable integer-threshold, setting-change, oversized-integer, nested-container, scope, authority, evidence, and current-boundary controls.

## Separation and current-effect attestations

`SELF_REVIEW_PERFORMED = NO`

`INDEPENDENT_REVIEW_PERFORMED_BY_R7_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_APPLICABILITY_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`AUTHORITY_INDEX_MUTATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061 = HARD_BLOCKED`

Court terminal:
`PASS__OBL059_R7_BOUNDED_REPAIR_GOVERNED_COURT_GREEN__NO_SELF_REVIEW`
