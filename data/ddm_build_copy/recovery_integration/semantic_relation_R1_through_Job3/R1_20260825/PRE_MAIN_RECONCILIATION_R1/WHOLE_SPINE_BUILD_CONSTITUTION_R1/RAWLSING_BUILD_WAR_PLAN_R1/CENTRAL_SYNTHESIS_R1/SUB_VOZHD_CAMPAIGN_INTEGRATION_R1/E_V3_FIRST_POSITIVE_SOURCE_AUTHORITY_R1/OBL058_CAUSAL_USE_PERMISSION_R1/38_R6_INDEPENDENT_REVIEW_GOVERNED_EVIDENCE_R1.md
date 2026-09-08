# OBL058 — CAUSAL_USE_PERMISSION — R6 INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Governed execution result

`PASS__OBL058_R6_INDEPENDENT_REVIEW_GOVERNED_EXECUTION__SEMANTIC_BLOCKER_REPRODUCED`

The reviewer-authored court executed successfully against frozen semantic candidate `92418a9e13f55464a91c1c9f1deb96977bc294ef`. The green execution is a reproduction result: the blocking lifecycle check intentionally asserts that a stale broker record remains authoritative after the only weak-reference retirement registration is detached and the original issued object is released.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r6-independent-review-r1`
- exact review start: `2523e2a3bc2470a08a8c4ca78a7357007738c427`
- campaign authority: `4aac8ec1b9222ce19f3092cd6f1789b5d216af76`
- frozen R6 candidate: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- independent matrix freeze: `cad5df4d9c92aec14822d9ebdccf8902146ed870`
- independent test-surface commit: `10b04bed31c0b829660e1ffa97a315504c8a1c26`
- initial governed wrapper commit: `b66ea5a44d012111c3829be0264ed6f1b613e885`
- court-spec bind commit: `b79d15b7dbfd5f4c9b9c6bcb03a4f91b247d2342`
- final reviewer wrapper correction / evidence execution: `9e307394f2d156495548c380d3ae69127e1d5b0e`
- execution-only PR: `#302`, closed unmerged
- PR synthetic merge identity: `2b3909bec656d57f75f13820abc3a1dea3ffb983`

## Governed court

- workflow: `Rabochii Governed Bounded Court`
- run: `34256659976`
- job: `102164084111`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.10s`
- court-spec validation: `PASS`
- independent review court: `19 passed, 21 subtests passed in 2.57s`
- bounded-court receipt: `PASS`
- receipt exit code: `0`
- receipt elapsed seconds: `2.786423`
- semantic candidate in receipt: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- evidence execution in receipt: `9e307394f2d156495548c380d3ae69127e1d5b0e`
- receipt spec SHA-256: `0421e5a434f80fbb0591ee46943b8b4a3adb0c0a0275e5d46937acdfaa6ff6cc`
- artifact ID: `10068138046`
- artifact ZIP SHA-256: `caa968f796595bf593ced5522f918388b957734dc6a6c305456eefc2e9e75471`

## Reviewer correction note

Earlier run `34256497794` / job `102163531020` is not the evidence of record. It returned `1 failed, 18 passed, 21 subtests passed` because the first form of the blocking lifecycle check required CPython to recycle one exact object address within a bounded allocation loop. The address did not recycle in that run. The frozen matrix explicitly states that allocator-dependent non-reproduction cannot be used as proof of correctness.

The reviewer therefore corrected only the governed wrapper check to test the deterministic property already frozen in the matrix: detach the inspectable `weakref.finalize` registration, release the issued object, then ask the genuine broker about the retained exact object-ID/body record. The broker returns `PERMIT`, proving the stale record remains authoritative after object release. No candidate file or semantic target changed.

Earlier run artifact `10068073240` / ZIP SHA-256 `98bf68503c9afd6431dc0b822cb2e92a26ec1af9b8078cad3753fac4e00c2a79` is retained only as reviewer-mechanics history.

## Independent findings

### B1 — stale record retirement depends on a caller-detachable weak-reference finalizer

`BLOCKING_STALE_OBJECT_GENERATION_AUTHORITY`

R6 registers receipt retirement with `weakref.finalize(receipt, _finalize_receipt_record, id(receipt))` and does not retain a source-owned retirement handle outside the ordinary Python finalizer machinery. The active registration is discoverable in `weakref.finalize._registry` and can be detached while the receipt is live.

The governed reviewer check independently performed this sequence:

1. issue a genuine synthetic `PERMIT` receipt;
2. save its exact object ID and authoritative body;
3. locate and detach the live `weakref.finalize` registration;
4. release the original issued object and force collection;
5. query the genuine bound broker from the same requester process generation for the retained object-ID/body record;
6. observe `decision == PERMIT`;
7. explicitly close the stale record for test cleanup.

Thus the required R6 property “released receipt causes broker record retirement before later object generation can be accepted” is not invariant under the declared inspectable Python surface. The source-owned broker retains an authoritative record after the original object generation has ended if the caller-detachable finalizer is removed. A later same-process reuse of that integer object address would therefore meet the broker's process-generation and object-ID key; whether a particular bounded allocator loop happens to recycle that address is not the correctness boundary.

Smallest exact blocker:

`BLOCKER__OBL058_R6_OBJECT_RECORD_RETIREMENT_DEPENDS_ON_CALLER_DETACHABLE_WEAKREF_FINALIZER`

## Preserved R6 controls

The same independent court confirmed that R6 genuinely closes the R5 fork/process-generation defect on ordinary paths:

- forked `PERMIT` copy is rejected with requester-process-generation mismatch and the parent receipt remains valid;
- forked `DENY` copy is rejected;
- forked close does not retire the parent record;
- caller-supplied requester identity fields are rejected;
- ordinary unmodified finalization does retire a record;
- duplicate close is idempotent and a closed receipt does not validate;
- equal semantic inputs retain distinct authority-instance identities;
- cross-receipt body reuse, constructor/object-new/subclass/mapping/proxy/JSON/copy/deepcopy/serialization and cross-scope replay are rejected;
- broker death fails closed;
- concurrent same-process validation remains stable;
- registered synthetic `PERMIT`, unregistered synthetic `DENY`, exact five-field basis/scope binding, project-current-shaped/current-first-canary rejection and surrogate-basis denial remain correct;
- no project-current-effect surface was introduced.

## Separation / current-state attestation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R6_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`AUTHORITY_INDEX_EFFECT_CREATED = NO`

`OBL061_UNBLOCKED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`
