# OBL058 — CAUSAL_USE_PERMISSION — BOUNDED REPAIR R6 — RETURN TO SUB-VOZHD E

## Terminal

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_BOUNDED_REPAIR_R6__RETURN_TO_SUB_VOZHD_E`

State after terminal: `CLOSURE_ONLY`.

## Recommendation

`PASS__OBL058_R6_BOUNDED_REPAIR__READY_FOR_EXACTLY_ONE_FRESH_DISTINCT_INDEPENDENT_REVIEW`

The commissioned R6 repair is complete at the producer boundary. The new frozen R6 candidate has a green governed bounded-repair court and is returned to SUB-VOZHD E. This worker does not perform, commission, or claim the required independent review.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r6`
- exact working-ancestry start: `c299ab4765d513b45815b19be131e4d5082b397a`
- immutable SUB-VOZHD E R6 command/adjudication: campaign commit `9f3332c369853c5134c074c084f1e9322bf6ea3b`
- failed frozen R5 candidate retained unchanged: `43474152150350c1b5c73374abd24ecebc627b99`
- frozen R6 semantic candidate: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.5.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@6.0.0`
- semantic executable: `causal_use_permission_candidate_r6.py`
- producer court: `test_bounded_repair_r6.py`
- governed wrapper correction / evidence execution: `6d8a7f4cb9a1a3c622eeed9242befe4ae13aa410`
- governed evidence packet: `cbc885b52781ed95c963512eecf76c161dcb0d1e`
- execution-only PR: `#298`, closed unmerged
- final worker tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Exact bounded repair

R5 correctly bound validation to the genuine broker process and one-shot authority child, but broker records still used a bare integer `id(receipt)` without identifying the requester process generation that owned that process-local object.

R6 binds every authoritative broker record to operating-system-observed requester process generation. At issuance, the broker records Unix peer PID/UID plus `/proc/<pid>/stat` start time together with the exact object ID, authoritative body, authority-instance ID, and one-shot child. Validation and close requests are accepted only when the live connection presents the same OS-observed PID/UID/process-start generation.

A forked child therefore cannot reuse the parent's broker record merely because its copied receipt has the same process-local integer address. The child process has a different OS process generation and is rejected before the one-shot authority child is consulted.

R6 also makes normal issued receipts weak-referenceable and registers a finalizer that retires the broker record when the issued object is released. This closes the normal stale-record/object-generation seam without making the finalizer authoritative: the finalizer can only retire an existing record, never create or alter a positive decision.

## Governed evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34253660939`
- job: `102153937299`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.10s`
- court-spec validation: `PASS`
- producer R6 court: `30 passed, 21 subtests passed in 7.34s`
- bounded-court receipt: `PASS`, exit code `0`
- semantic candidate in receipt: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- evidence execution in receipt: `6d8a7f4cb9a1a3c622eeed9242befe4ae13aa410`
- receipt spec SHA-256: `32644bfd64b5e2f8ca71be3487c32378d36f3fd16923b256cf08ab146474e526`
- artifact ID: `10066986830`
- artifact ZIP SHA-256: `8826c21ef9ab2bdef4b7b475a1d1c8fa77dd49ebb00657fb8c5175e70337ec56`

Earlier run `34253584943` is excluded from the evidence of record because a wrapper import-path error stopped collection before the R6 producer tests executed. The semantic candidate was not changed; only the governed wrapper import path was corrected.

## Preservation holding

The governed court confirms preservation of the required R5 semantics and boundaries: genuine broker identity binding; broker/authority-child loss fails closed; one-shot source-owned scope/basis/fixture decision; no caller-built body injection; exact five-field source-basis/scope binding; exact field-specific `NONCURRENT_SYNTHETIC` namespace enforcement; current first-canary and other project-current-shaped identity rejection; exact authority/schema/fixture/basis-proof/authority-instance/content-integrity checks; ordinary reconstruction/fabrication/copy/serialization rejection; cross-scope replay rejection; stable same-process repeated/concurrent validation; independent authority-instance identity for separate receipts; inference-like surrogate denial; valid synthetic `PERMIT` and `DENY`; and no public source-basis registration surface.

## Non-ownership / no-current-effect attestation

This R6 candidate does not own or create actor identity, actor creation/activation, positive applicability, occurrence admission, contact-witness independence, ENCOUNTER, OEE realization, current-positive OBL056 state, or OBL055 execution.

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

`EXECUTION_ONLY_PR_MERGED = NO`

No central, PRE-MAIN, main, SUB-VOZHD campaign, or sibling-lane branch was moved by this R6 repair worker.

## Required next gate

SUB-VOZHD E may now adjudicate this green repair return and, if accepted, commission exactly one fresh distinct independent reviewer against frozen candidate `92418a9e13f55464a91c1c9f1deb96977bc294ef`.

Until that review returns and is adjudicated, OBL058 remains not adopted and OBL061 remains blocked.
