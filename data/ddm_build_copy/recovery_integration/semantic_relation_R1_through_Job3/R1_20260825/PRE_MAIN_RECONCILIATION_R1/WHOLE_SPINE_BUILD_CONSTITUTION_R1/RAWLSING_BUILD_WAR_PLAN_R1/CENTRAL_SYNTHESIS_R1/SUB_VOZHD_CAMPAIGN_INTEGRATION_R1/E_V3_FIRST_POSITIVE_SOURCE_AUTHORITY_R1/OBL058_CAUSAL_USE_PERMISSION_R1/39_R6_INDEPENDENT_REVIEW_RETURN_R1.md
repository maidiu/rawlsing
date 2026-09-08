# OBL058 — CAUSAL_USE_PERMISSION — R6 INDEPENDENT REVIEW — RETURN TO SUB-VOZHD E

## Terminal

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R6_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`

State after terminal: `CLOSURE_ONLY`.

## Recommendation

`FAIL__OBL058_R6_INDEPENDENT_REVIEW__STALE_OBJECT_RECORD_RETIREMENT_NOT_INVARIANT`

Smallest exact blocker:

`BLOCKER__OBL058_R6_OBJECT_RECORD_RETIREMENT_DEPENDS_ON_CALLER_DETACHABLE_WEAKREF_FINALIZER`

The frozen R6 candidate is not yet lawful for SUB-VOZHD E adoption consideration. R6 correctly closes the R5 fork/process-generation defect on ordinary paths, but its stale object-generation boundary depends on an inspectable and detachable Python weak-reference finalizer registration. After that retirement registration is detached and the original issued object is released, the genuine broker still treats the old object-ID/body record as authoritative and returns `PERMIT`.

No repair was performed by this reviewer.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r6-independent-review-r1`
- exact review start: `2523e2a3bc2470a08a8c4ca78a7357007738c427`
- campaign authority: `4aac8ec1b9222ce19f3092cd6f1789b5d216af76`
- campaign authority tree: `c5559904b930a79ca9cd7b0155d71f265f1cb950`
- frozen R6 candidate reviewed: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- independent matrix freeze: `cad5df4d9c92aec14822d9ebdccf8902146ed870`
- independent test-surface commit: `10b04bed31c0b829660e1ffa97a315504c8a1c26`
- initial governed wrapper commit: `b66ea5a44d012111c3829be0264ed6f1b613e885`
- court-spec bind commit: `b79d15b7dbfd5f4c9b9c6bcb03a4f91b247d2342`
- final reviewer wrapper correction / governed evidence execution: `9e307394f2d156495548c380d3ae69127e1d5b0e`
- governed evidence packet: `e9c7d2d6b02143fdb8f402c80a5bbb12657a710e`
- execution-only PR: `#302`, closed unmerged
- PR synthetic merge identity: `2b3909bec656d57f75f13820abc3a1dea3ffb983`
- final reviewer tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Governed review court

- workflow: `Rabochii Governed Bounded Court`
- evidence run: `34256659976`
- job: `102164084111`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.10s`
- court-spec validation: `PASS`
- independent review court: `19 passed, 21 subtests passed in 2.57s`
- bounded-court receipt: `PASS`, exit code `0`
- receipt elapsed seconds: `2.786423`
- receipt semantic candidate: `92418a9e13f55464a91c1c9f1deb96977bc294ef`
- receipt evidence execution: `9e307394f2d156495548c380d3ae69127e1d5b0e`
- receipt spec SHA-256: `0421e5a434f80fbb0591ee46943b8b4a3adb0c0a0275e5d46937acdfaa6ff6cc`
- artifact ID: `10068138046`
- artifact ZIP SHA-256: `caa968f796595bf593ced5522f918388b957734dc6a6c305456eefc2e9e75471`

The green governed court is a reproduction court. The lifecycle blocking check intentionally asserts the retained stale authority response, so green execution confirms the semantic blocker rather than implying semantic PASS.

Earlier run `34256497794` / job `102163531020` is not the evidence of record. It failed only because the first reviewer form required CPython allocator reuse within a bounded loop. That nondeterministic allocation outcome was removed from the decision criterion without changing the frozen matrix or candidate. The corrected reviewer check proves the underlying stale-record property directly.

## Independent finding

R6 creates a weak-reference finalizer for every issued receipt and relies on that callback to send broker `close` for the exact integer object ID after the object is released. The registration is present in the ordinary inspectable `weakref.finalize` registry and can be detached while the receipt remains live.

The independent governed check showed:

1. a genuine synthetic `PERMIT` receipt is issued;
2. its object ID and authoritative body are retained for observation;
3. the corresponding weak-reference finalizer registration is located and detached;
4. the original receipt object is released and collection is forced;
5. the genuine source-owned broker is queried for the old object-ID/body record from the original requester process generation;
6. the broker returns `PERMIT`;
7. the stale record is then explicitly closed only for reviewer cleanup.

Therefore the required R6 object-generation retirement property is not invariant. The old authority record can survive the end of the issued object generation. A later same-process reuse of that integer address would match the broker's process-generation/object-ID key; allocator timing does not constitute an authority boundary and need not reproduce in a bounded loop to establish that the stale record remains authoritative.

## Preserved R6 controls

This FAIL is narrow. The independent court separately confirmed:

- forked `PERMIT` and `DENY` copies are rejected by requester process-generation checks;
- child close does not retire the parent record and the parent remains valid;
- caller-supplied requester identity fields are rejected;
- ordinary unmodified finalization retires records;
- duplicate close is idempotent;
- equal semantic inputs have distinct authority-instance identities;
- cross-receipt body reuse and cross-scope replay are rejected;
- constructor, `object.__new__`, subclass, Mapping/proxy, JSON reconstruction, copy/deepcopy and serialization cases are rejected;
- broker death fails closed;
- repeated/concurrent same-process validation remains stable;
- registered source basis and exact five-field scope binding remain correct;
- field-specific `NONCURRENT_SYNTHETIC` and exact current first-canary/project-current-shaped boundaries remain correct;
- inference-like surrogate basis strings deny;
- valid synthetic `PERMIT` and `DENY` controls remain functional;
- no project-current effect was created.

## Review-count / separation / current-state attestation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R6_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

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

No campaign, central, PRE-MAIN, main, sibling-lane, or frozen candidate branch was moved by this reviewer.

## Required next gate

Return this FAIL to SUB-VOZHD E. Do not commission a second review of frozen R6 candidate `92418a9e13f55464a91c1c9f1deb96977bc294ef`.

Any successor must be a newly commissioned bounded repair that makes object-generation retirement source-owned and non-bypassable on the declared inspectable Python surface while preserving the R6 process-generation and semantic controls, followed by exactly one fresh independent review of that new frozen candidate.
