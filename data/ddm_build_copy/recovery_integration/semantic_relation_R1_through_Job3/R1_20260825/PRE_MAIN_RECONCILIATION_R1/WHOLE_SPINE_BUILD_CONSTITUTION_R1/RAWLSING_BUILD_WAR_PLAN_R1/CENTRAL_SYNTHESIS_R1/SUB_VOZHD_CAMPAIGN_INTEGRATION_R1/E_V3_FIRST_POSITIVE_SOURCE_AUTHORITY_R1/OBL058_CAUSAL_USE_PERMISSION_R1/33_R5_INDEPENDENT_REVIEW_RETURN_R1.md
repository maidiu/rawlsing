# OBL058 — CAUSAL_USE_PERMISSION — R5 FRESH DISTINCT INDEPENDENT REVIEW R1 — RETURN

## Terminal

`RABOCHII_SUBV_E_OBL058_R5_CAUSAL_USE_PERMISSION_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`

State after terminal: `CLOSURE_ONLY`.

## Recommendation

`FAIL__OBL058_R5_INDEPENDENT_REVIEW__FORKED_PROCESS_RECEIPT_COPY_RETAINS_ACCEPTED_SOURCE_ORIGIN`

Smallest blocker:

`BLOCKER__OBL058_R5_BROKER_OBJECT_ID_BINDING_OMITS_REQUESTER_PROCESS_GENERATION`

The frozen R5 candidate is **not lawful for SUB-VOZHD E adoption adjudication or HQ adoption preparation in its present form**. This review does not repair the candidate, create a replacement candidate, perform a second review, create project-current permission, execute OBL055, or authorize OBL061.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r5-independent-review-r1`
- exact review start: `f5d334c9d0f86ad3acc350389d151280953fa6a8`
- binding campaign authority: `77127860ac887810a3dd28219617c305756fad21`
- frozen R5 candidate reviewed: `43474152150350c1b5c73374abd24ecebc627b99`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.4.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@5.0.0`
- independent matrix freeze: `6232688088a22f17999474b35ffd37dcc6456929`
- independent test-surface commit: `027cf84e75758e6b6d67c6e24cb09e6e214bbf81`
- court-spec bind: `b1fdffbecf3e69e170cdc8cdf59d833c6c6851f3`
- reviewer-harness correction / governed evidence execution: `f36c039fd3d56314f8f95db615a1a90a4c162f78`
- governed evidence packet: `ffb4e7a9fc79c300c309456313054469453ff76a`
- execution-only PR: `#296`, closed unmerged
- final reviewer tip: reported out of band after this return commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Independence holding

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R5_CANDIDATE = 1`

The independent matrix was frozen before the producer R5 test file was consumed. Producer tests were inspected only after matrix freeze as prior evidence and implementation context. The reviewer did not modify the frozen candidate and did not perform a repair.

## Governed independent evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34251098195`
- job: `102145432110`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.08s`
- court-spec validation: `PASS`
- independent review court: `18 passed, 37 subtests passed in 3.06s`
- bounded-court receipt: `PASS`, exit code `0`
- semantic candidate in receipt: `43474152150350c1b5c73374abd24ecebc627b99`
- evidence execution in receipt: `f36c039fd3d56314f8f95db615a1a90a4c162f78`
- artifact ID: `10066017222`
- artifact ZIP SHA-256: `82e3f89b82760001c8ef63713045c2d790272022381c7be19751f453ca37ecf6`

The green court proves the independent checks executed as designed. Because the fork/process-generation checks intentionally assert the reproduced incorrect-positive behavior, the semantic adjudication is FAIL.

The earlier run `34250888918` is not the evidence of record. It exposed only reviewer-harness mechanics: allocator address reuse was not deterministic within the bounded loop, and a dynamic second-module import required `sys.modules` registration. Those mechanics were corrected without changing the matrix, candidate, or blocking process-generation finding.

## Independent finding

R5 materially fixes the R4 parent-transport problem. The validator is bound to the genuine broker by socket pathname, PID, UID and process start-time; unrelated same-user socket replacement fails closed. Broker death and authority-child death also fail closed. Those controls are real.

The remaining source-origin key, however, is still the bare integer `id(receipt)` plus authoritative body/authority-instance state. It does not include the process generation that owns the Python object.

On Linux/CPython, `fork()` copies the parent's address space. The child receives a distinct process-local copy of an already-issued receipt at the same virtual address, so its `id(receipt)` integer is identical to the parent's. The inherited validator remains bound to the same genuine broker. The independent court demonstrated that the fork-child copy of a genuine positive receipt validates as `PERMIT` through the parent's broker record without a new source-owned issuance decision for the child-process object.

Therefore the candidate cannot presently distinguish the exact source-issued parent-process object from a forked process-local copy that presents the same integer ID and body.

This is the smallest remaining blocker:

`BLOCKER__OBL058_R5_BROKER_OBJECT_ID_BINDING_OMITS_REQUESTER_PROCESS_GENERATION`

## Supporting stale-record observation

The review also confirmed that a broker record keyed by a directly supplied integer object ID can remain registered after the corresponding non-pinned Python shell has been released, until an explicit broker `close` occurs. The governed runner did not recycle that exact address within the bounded allocator loop, so allocator-dependent ID reuse is not used as the blocking claim. The deterministic fork finding establishes the process/object-generation defect independently.

## Preserved R5 controls

This FAIL does not discard the R5 repair. The independent court confirmed:

- valid registered synthetic `PERMIT` and unregistered-basis `DENY` controls;
- source-owned broker endpoint/PID/UID/start-time verification;
- unrelated same-user socket replacement rejection;
- broker-death and authority-child-death fail-closed behavior;
- denial-to-positive body substitution rejection;
- cross-receipt equal-body reuse rejection through authority-instance binding;
- ordinary constructor, `object.__new__`, subclass, mapping/proxy, JSON reconstruction, copy/deepcopy and pickle rejection;
- authority/schema/fixture/decision/scope/proof/authority-instance/content-integrity enforcement;
- stable repeated and concurrent validation without result mixing;
- isolation between independently loaded module/broker instances;
- exact five-field source-basis/scope binding and cross-scope replay rejection;
- all commissioned NONCURRENT namespace/current-first-canary/project-current fixture boundaries;
- denial of classification/routing/occurrence/proximity/narrative-like surrogate permission;
- no public source-basis registration or project-current downstream effect.

## Smallest required next property

`REQUIRES__SOURCE_ORIGIN_BINDING_THAT_DISTINGUISHES_REQUESTER_PROCESS_AND_OBJECT_GENERATION_FROM_BARE_PROCESS_LOCAL_ID_REUSE`

This reviewer does not prescribe an architecture. Any changed candidate is a new semantic review target and must follow whatever repair/review sequence SUB-VOZHD E lawfully commissions. This reviewer must not repair R5 or commission a second reviewer.

## Adoption / current-state boundary

Until a newly repaired candidate lawfully passes its required fresh review:

- OBL058 remains lane-blocked;
- SUB-VOZHD E must not prepare an OBL058 HQ adoption packet from `43474152150350c1b5c73374abd24ecebc627b99`;
- OBL061 remains blocked by the campaign gate;
- no project-current positive causal-use permission is authorized.

`FROZEN_R5_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_R5_REVIEWER = NO`

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

No central, PRE-MAIN, main, SUB-VOZHD campaign, sibling-lane, or frozen-candidate branch was moved by this review.

## Return to SUB-VOZHD E

Frozen R5 candidate `43474152150350c1b5c73374abd24ecebc627b99` is returned as **not lawful for adoption consideration in its present form**.

Exact terminal:

`RABOCHII_SUBV_E_OBL058_R5_CAUSAL_USE_PERMISSION_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`
