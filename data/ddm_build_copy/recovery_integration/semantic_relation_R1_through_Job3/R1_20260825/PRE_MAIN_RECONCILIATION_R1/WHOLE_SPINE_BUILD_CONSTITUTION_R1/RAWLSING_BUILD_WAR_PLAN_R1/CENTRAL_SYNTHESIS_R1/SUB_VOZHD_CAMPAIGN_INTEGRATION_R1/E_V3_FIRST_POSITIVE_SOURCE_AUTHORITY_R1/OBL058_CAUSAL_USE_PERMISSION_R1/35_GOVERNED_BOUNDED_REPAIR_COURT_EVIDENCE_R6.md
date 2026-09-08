# OBL058 — CAUSAL_USE_PERMISSION — GOVERNED BOUNDED REPAIR COURT EVIDENCE R6

## Result

`PASS__OBL058_R6_GOVERNED_BOUNDED_REPAIR_COURT`

The governed producer court executed successfully against the exact frozen R6 semantic candidate. This evidence is producer-side verification only and is not the required fresh distinct independent review.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r6`
- exact working-ancestry start: `c299ab4765d513b45815b19be131e4d5082b397a`
- frozen R6 semantic candidate: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- governed wrapper correction / evidence execution: `6d8a7f4cb9a1a3c622eeed9242befe4ae13aa410`
- PR synthetic merge identity: `57462c567e6b21e1ecce74cf33491cd42bc705fb`
- execution-only PR: `#298`, closed unmerged

## Governed court

- workflow: `Rabochii Governed Bounded Court`
- run: `34253660939`
- job: `102153937299`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.10s`
- court-spec validation: `PASS`
- R6 producer court: `30 passed, 21 subtests passed in 7.34s`
- bounded-court receipt: `PASS`
- receipt exit code: `0`
- receipt elapsed seconds: `7.573578`
- semantic candidate in receipt: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- evidence execution in receipt: `6d8a7f4cb9a1a3c622eeed9242befe4ae13aa410`
- receipt spec SHA-256: `32644bfd64b5e2f8ca71be3487c32378d36f3fd16923b256cf08ab146474e526`
- artifact ID: `10066986830`
- artifact ZIP SHA-256: `8826c21ef9ab2bdef4b7b475a1d1c8fa77dd49ebb00657fb8c5175e70337ec56`

## Mechanical first-run note

Earlier run `34253584943` is not the evidence of record. It stopped during test collection because the governed wrapper did not add the lane directory to `sys.path`, producing `ModuleNotFoundError` before any R6 producer test executed. The frozen semantic candidate `92418a9e13f55464a91c1c9f1deb96977bc294ef` was not changed. Commit `6d8a7f4cb9a1a3c622eeed9242befe4ae13aa410` corrects only the wrapper import path.

## R6 repair holding

The governed court confirms the R5 process-generation defect is closed at the producer boundary:

- a forked process-local copy of a parent-issued synthetic `PERMIT` is rejected because the broker observes a different requester process generation;
- a forked process-local copy of a parent-issued synthetic `DENY` is likewise rejected;
- repeated validation from the forked process remains rejected while the original parent-process receipt remains valid;
- a forked process cannot retire the parent process's broker record;
- requester PID/UID/process-start generation is derived from operating-system peer state, not from caller-supplied requester fields;
- weak-reference finalization retires the normal issued-object broker record after object release;
- duplicate close is idempotent and a duplicate issue for a live object identity is rejected;
- ordinary same-process repeated and concurrent validation remains functional.

## Preservation holding

The governed court also confirms preservation of required R5 controls: genuine broker identity binding; fail-closed broker/authority-child loss; exact five-field source-basis/scope binding; exact `NONCURRENT_SYNTHETIC` namespace boundaries; current first-canary and project-current-shaped identity rejection; exact authority/schema/fixture/basis-proof/authority-instance/content-integrity checks; reconstruction/fabrication/copy/serialization rejection; cross-scope replay rejection; multiple-receipt authority-instance separation; inference-like surrogate denial; valid synthetic `PERMIT` and `DENY`; and no public source-basis registration surface.

## No-current-effect / separation attestation

`INDEPENDENT_REVIEW_PERFORMED_BY_R6_REPAIR_WORKER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`CURRENT_ACTOR_OR_RUNTIME_MUTATION = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061_UNBLOCKED = NO`

No central, PRE-MAIN, main, SUB-VOZHD campaign, or sibling-lane branch was moved by this producer court.
