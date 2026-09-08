# OBL058 — CAUSAL_USE_PERMISSION — R5 INDEPENDENT REVIEW MATRIX R1

## Status

`FROZEN_INDEPENDENT_REVIEW_MATRIX__BEFORE_GOVERNED_EXECUTION`

This matrix was authored from the immutable R5 review commission, the frozen R5 candidate itself, and prior R4 review findings. The producer R5 test file was not consumed before this matrix freeze and does not define this review.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r5-independent-review-r1`
- exact review start: `f5d334c9d0f86ad3acc350389d151280953fa6a8`
- binding campaign authority: `77127860ac887810a3dd28219617c305756fad21`
- frozen R5 target: `43474152150350c1b5c73374abd24ecebc627b99`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.4.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@5.0.0`

## Review criterion

PASS requires that independently exercised paths find no way for a receipt to validate `PERMIT` unless the exact receipt identity/body/scope is still bound to the exact source-owned broker and one-shot authority instance that issued it. Content integrity by itself is not source origin.

Any reproducible incorrect positive is blocking. Transport/process failures may reject availability, but they must not create or transform a positive result.

## R5 review families

### A — broker registration and exact object-lifetime binding

A01. Confirm ordinary public issuance produces valid synthetic `PERMIT` and `DENY` controls.

A02. Inspect the parent-reachable broker request surface and determine whether a caller-selected exact-type receipt shell can be registered by supplying only its integer `id(...)`, exact synthetic scope, basis and fixture.

A03. Determine whether an authoritative broker record can outlive the Python object whose integer identity was registered.

A04. Exercise exact object-ID reuse after garbage collection. If a stale broker record survives and CPython reuses the same integer `id` for a new exact-type receipt, determine whether the new object plus stale body can validate without a new source-owned issuance decision for that object.

A05. Exercise the normal lifetime pin and determine whether its removal/clearing on the declared CPython surface can reopen A03/A04. A lifetime mechanism that is necessary to distinguish object generations is authority-relevant even if it is not directly consulted by `validate_receipt`.

A06. Confirm broker `close` removes an exact record and prevents later validation through that removed record.

### B — broker endpoint and operating-system identity binding

B01. Unlink/rebind the broker Unix-socket pathname to an unrelated same-user responder and require fail-closed behavior.

B02. Verify peer PID/UID checks and `/proc/<pid>/stat` process-start identity reject an unrelated process at the expected pathname.

B03. Exercise stale/dead broker, broker termination and unavailable socket states; validation must fail closed.

B04. Exercise a live unrelated process and stale/reused process handles where technically reachable; positive validation must remain bound to the commissioned broker identity.

B05. Exercise the verification-to-request transition for obvious broker replacement races where technically reachable.

### C — body, receipt and scope substitution

C01. Replace a genuine `DENY` receipt body with a genuine `PERMIT` body; reject.

C02. Swap bodies across two valid receipts, including equal semantic bodies from separate issuance instances; reject when authority-instance binding differs.

C03. Cross-scope replay across each actor/world/subject/time/transition field; reject.

C04. Mutate/rebind `_body_json`, authority, schema, fixture, decision, scope digest, basis scope, proof, authority-instance identifier and integrity digest; reject.

C05. Plain mapping/proxy/JSON reconstruction/subclass/exact-type constructor/`object.__new__`/copy/deepcopy/pickle paths must not create a new accepted identity.

### D — request and authority-instance correspondence

D01. Mismatched request identifier response; reject.

D02. Replayed, duplicated, reordered or cross-receipt response identifiers where technically reachable; reject or fail closed.

D03. Mismatched/replayed authority-instance identifier; reject.

D04. Multiple receipts with equal bodies must remain independently bound to their own source-owned authority instances.

### E — multiple broker/module instances and concurrency

E01. Repeated validation of one genuine receipt remains stable.

E02. Concurrent validation of genuine `PERMIT` and `DENY` controls remains semantically stable with no response mix-up.

E03. Multiple fresh module imports/broker instances: a receipt from one instance must not become valid under another instance's validator or broker records.

E04. Concurrent issuance must not cross-bind identities, bodies or authority-instance responses.

E05. Fork/inherited-process behavior is inspected if reachable without widening the commissioned surface; inherited state must not create an incorrect positive.

### F — authority-child lifecycle and protocol totality

F01. Authority child death before validation must fail closed.

F02. Broker child-record state after child death must not transform a result.

F03. Duplicate initialization or unsupported broker/child operations must reject.

F04. Partial, malformed, oversized, truncated or unavailable transport responses must fail closed rather than validate positive.

### G — preserved semantic jurisdiction

G01. One registered `NONCURRENT_SYNTHETIC` basis permits only its exact five-field registered scope.

G02. Unregistered basis denies.

G03. All five field-specific `NONCURRENT_SYNTHETIC` namespace rules reject wrong-field, empty-suffix and project-current-shaped identifiers.

G04. The exact current first-canary subject is rejected.

G05. Non-synthetic/project-current fixture labels reject.

G06. Classification, routing, occurrence/admission, ADP-010, proximity/co-location and narrative-like surrogate basis strings do not imply permission.

G07. No caller permission boolean, caller basis-kind input, public basis registration, current-positive OBL056 installation, OBL055 execution, ENCOUNTER/OEE creation, actor/runtime mutation or project-current adoption effect exists.

## Separation holding

`FROZEN_R5_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_R5_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

The reviewer will return PASS or the smallest exact blocker after governed execution. Any blocker remains a review finding only; this worker will not repair it.
