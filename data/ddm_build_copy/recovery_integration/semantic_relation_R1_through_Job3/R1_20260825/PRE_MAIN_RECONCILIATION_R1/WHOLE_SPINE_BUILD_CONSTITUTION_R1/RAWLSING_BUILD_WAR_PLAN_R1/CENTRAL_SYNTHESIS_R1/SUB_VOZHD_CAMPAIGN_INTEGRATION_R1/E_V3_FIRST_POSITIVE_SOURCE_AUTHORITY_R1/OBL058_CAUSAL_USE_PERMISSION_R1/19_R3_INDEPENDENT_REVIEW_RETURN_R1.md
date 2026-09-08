# OBL058 — CAUSAL_USE_PERMISSION — R3 FRESH DISTINCT INDEPENDENT REVIEW R1 — RETURN

## Terminal

`FAIL__OBL058_R3_INDEPENDENT_REVIEW__CALLER_RECOVERABLE_CLOSURE_CAPABILITY_BREAKS_SOURCE_ORIGIN_BOUNDARY`

State after terminal: `CLOSURE_ONLY`.

The frozen R3 candidate is **not lawful for SUB-VOZHD E adoption adjudication or HQ adoption preparation in its present form**. This review does not repair the candidate, adopt OBL058, create current-positive permission, execute OBL055, or authorize OBL061.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r3-independent-review-r1`
- exact working-ancestry start: `3d306a67e369b1b312f81ee6061c359dd66f9d31`
- campaign adjudication: `c7f221d3c07453eebae36e448a52b2e7789ae13c`
- frozen R3 semantic candidate: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.2.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@3.0.0`
- candidate executable blob at evidence execution: `7560b4dc2d10f323c398ca62a335dd7ac8f0cce2`
- independent failure-mode matrix freeze: `41c417dfd706fff13ff62d9a269749dedfe53304`
- independent test commit: `74a8cbf1e5ba4b8324792494698abbfa3b8e65ea`
- governed wrapper commit: `9c06da1ff08c6be7d5c9cb9b30528321f0f81718`
- governed evidence execution: `5613e3a25f44011e0ebafbf39b7f56ed008f5dd6`
- governed evidence packet commit: `caaa525a47b215a6a6c0b753d6d45abfff060127`
- execution-only PR: `#285`, closed unmerged
- PR synthetic merge identity: `12f13a688cddccb50fcbbe427cc6dc78759c6fc6`
- final worker tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Independence holding

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R3_CANDIDATE = 1`

The independent matrix was frozen before the producer R3 test file was consumed. The reviewer did not modify the frozen candidate and did not perform a repair.

## Governed evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34199559502`
- job: `101974996241`
- conclusion: `success`
- Python: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.12s`
- court-spec validation: `PASS`
- independent review court: `26 passed, 42 subtests passed in 0.11s`
- bounded-court receipt: `PASS`, exit code `0`
- semantic candidate in receipt: `c5fa3a8cece8b3444671b2528aa88947a10cc539`
- evidence execution in receipt: `5613e3a25f44011e0ebafbf39b7f56ed008f5dd6`
- artifact ID: `10045246427`
- artifact ZIP SHA-256: `95112758baef1612d6112d1ef8894a80b2f3d4a20b68f390590f660df569a758`

The green court proves the independent probes executed as designed. Because B1-B3 intentionally assert reproducible incorrect-positive paths, the semantic adjudication is FAIL.

## Blocking findings

### B1 — caller can recover and invoke the internal ledger-minting helper

`issue_noncurrent_synthetic_receipt.__closure__` exposes `_new_issued_receipt`. The independent court recovers this callable and gives it a caller-built positive body. The helper creates the exact closure-local receipt type, records that identity/body in the ledger, and `validate_receipt()` returns `PERMIT` without the source-owned `issue(...)` basis decision having produced that receipt.

### B2 — caller can recover the mutable ledger and append a fabricated exact-type identity

`validate_receipt.__closure__` exposes `_lookup_exact_issued_body`; that helper's closure exposes the mutable `issued_ledger`. The independent court recovers the exact receipt type, constructs a new object with `object.__new__`, appends the fabricated identity with caller-built positive content to the ledger, and obtains `PERMIT`.

### B3 — caller can rebind the authoritative ledger body for an issued DENY identity

The independent court obtains a legitimate `DENY`, replaces that exact identity's tuple in the recovered mutable ledger with caller-built positive content, and the same receipt subsequently validates as `PERMIT`.

These are three manifestations of one smallest blocker:

`BLOCKER__OBL058_R3_SOURCE_ORIGIN_CAPABILITY_REMAINS_CALLER_RECOVERABLE_VIA_PYTHON_FUNCTION_CLOSURES`

R3 moved authority-bearing state from the receipt object into a closure, but on the declared repository-local Python surface the closure cells themselves are caller-readable and the ledger remains caller-mutable. Therefore exact type + exact identity does not establish that the accepted identity/body was produced only by the source-owned issuance decision.

## Preserved R3 controls

This FAIL does not discard R3's real improvements. The independent court confirmed ordinary-path rejection of plain copies, proxies, unledgered exact-type `object.__new__` fabrication and subclasses; exact five-field scope/basis binding; all five NONCURRENT_SYNTHETIC namespace boundaries; empty/wrong-field/project-current namespace rejection; exact first-canary subject rejection; unregistered-basis denial; valid synthetic PERMIT and DENY controls; replay rejection; and authority/schema/fixture/digest/proof/integrity fail-closed checks.

The blocker is specifically caller confinement of the source-origin capability and authoritative ledger.

## Smallest required repair property

`REQUIRES__NON_CALLER_RECOVERABLE_ISSUANCE_CAPABILITY_AND_NON_CALLER_MUTABLE_AUTHORITATIVE_LEDGER`

The independent reviewer does not prescribe an architecture. Any changed candidate is a new semantic review target and must follow whatever next repair/review sequence SUB-VOZHD E lawfully commissions. This reviewer must not repair R3 or create a second reviewer.

## Adoption / current-state boundary

Until a repaired candidate lawfully passes its required review:

- OBL058 remains lane-blocked;
- SUB-VOZHD E must not prepare an OBL058 HQ adoption packet from `c5fa3a8cece8b3444671b2528aa88947a10cc539`;
- OBL061 remains blocked by the campaign gate;
- no project-current positive causal-use permission is authorized.

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`ENCOUNTER_CREATED = NO`

`CURRENT_ACTOR_OR_RUNTIME_MUTATION = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`HQ_ADOPTION_CLAIMED = NO`

`OBL061_UNBLOCKED = NO`

`EXECUTION_ONLY_PR_MERGED = NO`

No central, PRE-MAIN, main, SUB-VOZHD integration, or sibling-lane branch was moved by this review.

## Return to SUB-VOZHD E

Frozen R3 candidate `c5fa3a8cece8b3444671b2528aa88947a10cc539` is returned as **not lawful for adoption consideration in its present form**.

Recommendation: retain the ordinary R3 scope/basis/fixture controls, but return OBL058 for a bounded repair whose source-origin issuance capability and authoritative ledger are not caller-recoverable/mutable through the declared Python authority surface.

Exact terminal:

`RABOCHII_SUBV_E_OBL058_R3_CAUSAL_USE_PERMISSION_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`
