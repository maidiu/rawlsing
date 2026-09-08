# OBL058 — CAUSAL_USE_PERMISSION — GOVERNED BOUNDED REPAIR COURT EVIDENCE R5

## Court terminal

`PASS__OBL058_R5_BOUNDED_REPAIR_GREEN__FROZEN_CANDIDATE_AWAITS_FRESH_DISTINCT_INDEPENDENT_REVIEW`

This is producer-side bounded repair evidence only. It does not perform or substitute for the required fresh distinct independent review of the frozen R5 candidate.

## Exact identities

- repository: `maidiu/rawlsing`
- worker branch: `agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r5`
- exact working-ancestry start: `b9ea19aaa74d9e1b3ba2c52b6a4e27056c4e1dee`
- immutable SUB-VOZHD E adjudication/command: `1c0f767126cc479c31ddcdc521fa64fa26efbe4f`
- failed frozen R4 candidate: `f02509a25b23365596ccedc7c8bc3a973dce3468`
- frozen R5 semantic candidate: `43474152150350c1b5c73374abd24ecebc627b99`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.4.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@5.0.0`
- candidate executable blob: `31091b75b8aa82f78e5f4791ec1dc83dd30c051c`
- producer court blob: `5d5ca52d32790d9c3ebea05b7d48bb9da5b5ab3b`
- candidate authority document blob: `838e92516411c4028f01e8274580a812a01cf786`
- governed wrapper commit: `88d1064260b5d5044ac1e7b9550ffe02ff50da3e`
- governed evidence execution / court-spec bind: `c03e63ed9c84146b5ff42f338e76ea146023bd5d`
- execution-only PR: `#293`, closed unmerged
- PR synthetic merge identity: `8d386e87eb70180415002262a3ac8e18572467be`

## Repair holding

R4's one-shot child semantic decision was preserved. R5 removes parent receipt transport/process authority state and binds validation to the exact source-owned authority channel instead of trusting caller-rebindable receipt fields.

The R5 receipt exposes only caller-visible receipt content. It does not carry a child process handle, read descriptor, write descriptor, broker handle, socket object, source decision token, or other parent transport capability.

A separate broker process owns the exact receipt-identity to one-shot-child association. The parent validator is generated with the broker endpoint plus exact broker process identity and verifies the connected peer before accepting a response. Each request carries a fresh request identity and authority-instance identity, and validation requires exact response correspondence.

Thus the two R4 incorrect-positive paths are closed at the producer court boundary:

1. an exact-type fabricated receipt cannot become valid merely by attaching a different responder;
2. a legitimate source-issued `DENY` cannot become `PERMIT` by replacing parent transport/process state, because that state is no longer carried by the receipt and the validator is bound to the source-owned broker instance.

## Governed evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34245050101`
- job: `102124781396`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.10s`
- court-spec validation: `PASS`
- R5 producer court: `30 passed, 33 subtests passed in 3.25s`
- bounded-court receipt result: `PASS`
- bounded-court receipt exit code: `0`
- receipt semantic candidate: `43474152150350c1b5c73374abd24ecebc627b99`
- receipt evidence execution: `c03e63ed9c84146b5ff42f338e76ea146023bd5d`
- receipt spec SHA-256: `31bce13a258c184d4086067ee2e4830e0ae1faaa4a363e61a1c229f96f818e2f`
- artifact ID: `10063619163`
- artifact ZIP SHA-256: `001b002cbe17bf9447511bcc0f977da556ad513ed46a5a2f191552d5790c421d`

## Direct R5 regression coverage

The governed court confirms all 30 commissioned producer checks, including:

- valid source-owned synthetic `PERMIT` and `DENY` controls;
- exact authority/schema revision identities;
- absence of parent receipt transport/process slots;
- exact-type fabrication rejection even with a real positive body;
- `DENY` body rebinding rejection;
- cross-receipt positive-body reuse rejection;
- parent request-helper substitution not changing the bound validator;
- validator has no closure/default-bound caller state and is bound to one broker identity;
- broker issue protocol rejects caller-built body fields;
- duplicate issue for an existing identity is rejected;
- no post-issue append/replace/rebind/delete/reinsert/register/mint operations;
- one-shot child rejection of caller-body initialization, validate-before-initialize, and duplicate initialization;
- stale/closed authority rejection;
- repeated validation stability;
- concurrent validation without cross-response consumption;
- constructor, `object.__new__`, subclass, plain mapping and proxy reconstruction rejection;
- copy/deep-copy/pickle/JSON reconstruction rejection;
- public scope-copy mutation isolation;
- exact five-field basis binding and cross-scope replay rejection;
- all field-specific `NONCURRENT_SYNTHETIC` boundaries and exact current first-canary rejection;
- wrong-field namespace, empty suffix, fixture and basis fail-closed behavior;
- classification/routing/occurrence/proximity/narrative surrogate basis denial;
- authority/schema/fixture/decision/authority-instance and integrity/proof/scope tamper rejection;
- no caller permission boolean, caller basis-kind input, or source-registration surface;
- broker peer-identity replacement rejection in an isolated process;
- exact request-ID and authority-instance-ID response binding.

## Preservation / no-current-effect holding

The R4 controls independently confirmed correct remain preserved at this producer boundary:

- one-shot source-owned semantic decision;
- exact five-field scope binding;
- exact source basis and proof binding;
- exact fixture restrictions;
- no inference from adjacent facts;
- no project-current positive permission;
- no current-positive OBL056 installation;
- no OBL055 execution;
- no ENCOUNTER or OEE realization;
- no authority-index effect;
- no adoption claim.

`INDEPENDENT_REVIEW_PERFORMED_BY_R5_REPAIR_WORKER = NO`

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

## Pre-freeze tooling note

A tooling mishap created six transient placeholder-only commits before the semantic freeze, from `1466412e88c5c1b085ef3bcd0196105328148bc7` through `3a273e672b43b7ab728a791ac2a13e735a58380b`. The frozen candidate commit `43474152150350c1b5c73374abd24ecebc627b99` restores the exact commissioning tree and adds only the three R5 candidate artifacts named above; none of the placeholder files is present in the frozen candidate tree or the governed evidence execution tree. No force-push or history rewrite was performed.

## Next gate

Return frozen R5 candidate `43474152150350c1b5c73374abd24ecebc627b99` to SUB-VOZHD E for exactly one fresh distinct independent review.
