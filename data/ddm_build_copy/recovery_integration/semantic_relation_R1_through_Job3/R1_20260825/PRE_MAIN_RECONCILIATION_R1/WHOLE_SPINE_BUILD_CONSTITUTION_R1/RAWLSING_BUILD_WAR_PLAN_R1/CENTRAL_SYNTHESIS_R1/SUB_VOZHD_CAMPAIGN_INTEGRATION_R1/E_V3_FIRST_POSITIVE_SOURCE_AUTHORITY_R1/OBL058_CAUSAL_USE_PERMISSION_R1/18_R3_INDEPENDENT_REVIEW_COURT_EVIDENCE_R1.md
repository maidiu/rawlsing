# OBL058 — CAUSAL_USE_PERMISSION — R3 FRESH DISTINCT INDEPENDENT REVIEW COURT EVIDENCE R1

## Review disposition

`SEMANTIC_REVIEW_HOLDING = FAIL`

The governed bounded court is green because the blocking probes intentionally assert that the discovered caller-reproducible provenance bypasses are accepted. The green execution proves those observations are reproducible; it does not convert them into semantic PASS.

Exact blocker:

`BLOCKER__OBL058_R3_SOURCE_ORIGIN_CAPABILITY_REMAINS_CALLER_RECOVERABLE_VIA_PYTHON_FUNCTION_CLOSURES`

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r3-independent-review-r1`
- exact reviewer start: `3d306a67e369b1b312f81ee6061c359dd66f9d31`
- campaign adjudication ref: `c7f221d3c07453eebae36e448a52b2e7789ae13c`
- campaign adjudication tree: `1fdf0ccf143942bf4b009c15cabfe2f5c41871e9`
- frozen semantic candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0`
- candidate executable blob at review execution: `7560b4dc2d10f323c398ca62a335dd7ac8f0cce2`
- independent matrix freeze: `41c417dfd706fff13ff62d9a269749dedfe53304`
- independent test commit: `74a8cbf1e5ba4b8324792494698abbfa3b8e65ea`
- governed wrapper commit: `9c06da1ff08c6be7d5c9cb9b30528321f0f81718`
- governed evidence execution: `5613e3a25f44011e0ebafbf39b7f56ed008f5dd6`
- execution-only PR: `#285`, closed unmerged
- PR synthetic merge identity: `12f13a688cddccb50fcbbe427cc6dc78759c6fc6`

## Independence

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R3_CANDIDATE = 1`

The failure-mode matrix was frozen before the producer R3 test file was consumed. Required governance, R2 failure history, the frozen R3 definition, candidate implementation, and the current campaign adjudication were consumed as required context. The reviewer authored a new R3 matrix and did not modify the frozen candidate.

From exact reviewer start through governed evidence execution, the branch is four commits ahead and changes only:

1. `.rabochii/court_spec.json` — one test-target line;
2. `17_R3_INDEPENDENT_REVIEW_FAILURE_MODE_MATRIX_R1.json`;
3. `test_independent_review_r3.py`;
4. `rawlsing_next/tests/test_subv_e_obl058_r3_independent_review.py`.

The candidate executable blob remains exactly `7560b4dc2d10f323c398ca62a335dd7ac8f0cce2`.

## Governed evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34199559502`
- job: `101974996241`
- run/job conclusion: `success`
- Python: `3.12.14` / `CPython`
- determinism: `EXACT`
- protocol self-tests: `20 passed in 0.12s`
- court-spec validation: `PASS`
- independent review court: `26 passed, 42 subtests passed in 0.11s`
- bounded-court receipt result: `PASS`
- bounded-court receipt exit code: `0`
- bounded-court spec SHA-256: `c2c8124f5400eea7f5010eafc3f47ed25e6e9c8feb3819e044bd9c023ebd95d5`
- receipt semantic candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- receipt evidence execution: `5613e3a25f44011e0ebafbf39b7f56ed008f5dd6`
- receipt PR synthetic merge SHA: `12f13a688cddccb50fcbbe427cc6dc78759c6fc6`
- artifact ID: `10045246427`
- artifact name: `rabochii-court-receipt-34199559502`
- artifact ZIP size: `598 bytes`
- artifact ZIP SHA-256: `95112758baef1612d6112d1ef8894a80b2f3d4a20b68f390590f660df569a758`

## Blocking findings

### B1 — exported issuer exposes the internal mint helper through its closure

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

`issue_noncurrent_synthetic_receipt` is an exported nested Python function. Its caller-readable `__closure__` contains `_new_issued_receipt`. The independent court recovers that callable from the exported issuer and invokes it directly on a caller-assembled positive receipt body. `_new_issued_receipt` then creates the exact closure-local concrete type and appends that exact object/body pair to the source ledger. `validate_receipt()` returns `PERMIT`.

This bypass never passes through the source-owned `issue(...)` basis decision. The R3 source-origin boundary is therefore caller-reproducible at the supported repository-local Python object surface.

### B2 — validator closure exposes the mutable ledger, permitting fabricated exact identity insertion

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

`validate_receipt` retains `_lookup_exact_issued_body` in its caller-readable closure; that nested helper in turn retains `issued_ledger`, an ordinary mutable list. A caller can recover the exact receipt type from a legitimate receipt, allocate a new exact-type object with `object.__new__`, append `(fabricated_object, caller_positive_body)` directly to the recovered ledger, and obtain `PERMIT` from `validate_receipt()`.

Exact-type checking plus Python object identity is not an origin boundary if the identity ledger itself is caller-recoverable and mutable.

### B3 — recovered ledger permits authoritative-body rebinding for a genuine issued DENY identity

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

The independent court first obtains a genuine source-issued `DENY`, verifies it as `DENY`, then recovers `issued_ledger` from the validator closure and replaces that exact identity's ledger tuple with caller-built positive content. The same genuine receipt identity subsequently validates as `PERMIT`.

R3 moved mutable authority state off the receipt object, but did not make that authority state non-caller-reproducible; the mutable state remains reachable through function closure cells.

## Preserved controls

The FAIL is narrow to source-origin capability confinement. The independent matrix also confirmed that ordinary paths preserve substantial R3 controls:

- the registered NONCURRENT_SYNTHETIC positive control validates `PERMIT`;
- an unregistered basis validates `DENY`;
- ordinary dict copies, proxy wrappers, unledgered exact-type construction, `object.__new__` fabrication, and subclasses are rejected;
- public scope copies do not mutate the authoritative ledger body;
- repeated legitimate issuance preserves distinct identities;
- registered positive basis is bound to all five exact scope fields;
- replay against changed actor/world/subject/time/transition is rejected;
- project-current-shaped identifiers are rejected across all five fields;
- empty namespace suffixes and wrong-field NONCURRENT_SYNTHETIC namespaces are rejected;
- the exact first-canary subject is rejected from the noncurrent synthetic fixture surface;
- non-synthetic fixture labels are rejected;
- classification, ADP-010, ADP-019 occurrence/admission, routing, co-location and narrative-like basis strings do not infer positive permission;
- wrong authority/schema/fixture/decision, malformed key sets, scope digests, basis-scope digests, basis proofs, receipt integrity and denial proofs fail closed when exercised against the authoritative validation logic.

These controls do not cure B1-B3 because the claimed decisive R3 property is non-caller-reproducible source origin.

## Semantic adjudication

The R3 contract claims that accepted origin is tied to an exact object identity recorded by the source-owned issuance decision and to immutable source-owned ledger content. B1-B3 show that a caller can invoke the internal ledger-minting helper or directly mutate the ledger through ordinary Python closure introspection. Therefore an accepted exact identity/body need not originate from the source-owned issuance decision.

The smallest required repair property is:

`REQUIRES__NON_CALLER_RECOVERABLE_ISSUANCE_CAPABILITY_AND_NON_CALLER_MUTABLE_AUTHORITATIVE_LEDGER`

This reviewer does not prescribe architecture and does not repair the candidate. A changed candidate is a new semantic target requiring its own governed producer court and the review sequence authorized by SUB-VOZHD E.

## No-current-effect / no-repair attestation

- `FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`
- `REPAIR_PERFORMED_BY_REVIEWER = NO`
- `SECOND_REVIEWER_CREATED = NO`
- `PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`
- `PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`
- `OBL055_EXECUTED = NO`
- `PROJECT_CURRENT_OEE_REALIZED = NO`
- `ENCOUNTER_CREATED = NO`
- `CURRENT_ACTOR_OR_RUNTIME_MUTATION = NO`
- `AUTHORITY_INDEX_EFFECT_CREATED = NO`
- `HQ_ADOPTION_CLAIMED = NO`
- `OBL061_UNBLOCKED = NO`
- `EXECUTION_ONLY_PR_MERGED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration, or sibling-lane branch was moved by this review.
