# OBL058 — CAUSAL_USE_PERMISSION — R5 INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Evidence status

`GOVERNED_INDEPENDENT_REVIEW_EXECUTED__SEMANTIC_ADJUDICATION_FAIL`

The governed court is green because the independent checks executed as authored, including checks that intentionally assert reproduced incorrect-positive source-origin behavior. Green execution therefore confirms the review finding; it does not convert the semantic result to PASS.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r5-independent-review-r1`
- exact review start: `f5d334c9d0f86ad3acc350389d151280953fa6a8`
- binding campaign authority: `77127860ac887810a3dd28219617c305756fad21`
- frozen R5 semantic candidate: `43474152150350c1b5c73374abd24ecebc627b99`
- authority: `OBL058_CAUSAL_USE_PERMISSION_SOURCE_AUTHORITY_R1@1.4.0`
- receipt schema: `OBL058_CAUSAL_USE_PERMISSION_RECEIPT@5.0.0`
- independent matrix freeze: `6232688088a22f17999474b35ffd37dcc6456929`
- independent test-surface commit: `027cf84e75758e6b6d67c6e24cb09e6e214bbf81`
- governed wrapper commit: `49e4ea2c986bd6fdae52f849d62176e9f223be94`
- court-spec bind commit: `b1fdffbecf3e69e170cdc8cdf59d833c6c6851f3`
- reviewer-harness correction: `f36c039fd3d56314f8f95db615a1a90a4c162f78`
- governed evidence execution: `f36c039fd3d56314f8f95db615a1a90a4c162f78`
- post-evidence documentary annotation: `9e2b8fd12cefd2486766a59a4eaf7fa03cddcf10`
- execution-only PR: `#296`, closed unmerged
- evidence-run PR synthetic merge identity: `9fa92510c2cae30828eed4dc9544856c9f84523b`

## Governed run

- workflow: `Rabochii Governed Bounded Court`
- run: `34251098195`
- job: `102145432110`
- conclusion: `success`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.08s`
- court-spec validation: `PASS`
- independent R5 court: `18 passed, 37 subtests passed in 3.06s`
- bounded-court receipt: `PASS`, exit code `0`
- receipt semantic candidate: `43474152150350c1b5c73374abd24ecebc627b99`
- receipt evidence execution: `f36c039fd3d56314f8f95db615a1a90a4c162f78`
- receipt spec SHA-256: `c31aa7b2bc52b08a87a642e47a885b735c9f36376a796d0f2655554ccc4bc6f7`
- artifact ID: `10066017222`
- artifact ZIP SHA-256: `82e3f89b82760001c8ef63713045c2d790272022381c7be19751f453ca37ecf6`

## Reviewer-harness correction note

The first governed execution, run `34250888918`, reached the independent court but ended `failure` because three review-harness mechanics were too runner-specific: two checks required CPython allocator address reuse within a bounded loop, and one dynamic second-module import omitted registration in `sys.modules` before executing a dataclass definition. That run was not used as semantic evidence of candidate failure.

The reviewer corrected only those mechanics in the governed wrapper. The frozen matrix, independent test surface, frozen candidate, and deterministic process-generation finding were not weakened or repaired. In the first run, the deterministic forked-process-copy check had already passed. The corrected evidence run above is the evidence of record.

## Blocking independent finding

### B1 — broker source-origin key omits requesting process generation

`BLOCKING_INCORRECT_POSITIVE_ACCEPTANCE`

R5 binds broker authority records by the integer `id(receipt)` and authoritative body/authority-instance state. The parent validator is correctly bound to the authentic broker by socket pathname, broker PID, UID and process start-time checks. However, the broker does not bind the receipt record to the process generation that owns the Python object.

On the declared Linux/CPython surface, `fork()` copies the parent address space. The child therefore receives a distinct process-local copy of the genuine positive receipt at the same virtual address, so `id(receipt)` is the same integer in parent and child. The child also inherits the validator whose broker identity constants point to the genuine parent-owned broker.

The independent court forked after genuine positive issuance and then called `validate_receipt()` inside the child. The child-side copied receipt validated as `PERMIT` through the genuine broker without a new source-owned issuance decision for that child-process object.

This contradicts the R5 review requirement that source origin remain tied to the exact receipt identity/body and exact source-owned broker/authority relationship, and it is inconsistent with the candidate's rejection of ordinary copy/deepcopy/serialization/reconstruction as new source-issued identities.

Smallest blocker:

`BLOCKER__OBL058_R5_BROKER_OBJECT_ID_BINDING_OMITS_REQUESTER_PROCESS_GENERATION`

### Supporting observation — stale integer identity records

The parent-reachable broker request surface accepts an exact synthetic issuance request keyed by a caller-supplied integer object ID. An independently created exact-type shell can therefore be registered by the authentic broker and receive an authentic source-owned body.

After such a non-pinned shell is released, the broker record remains occupied until explicit `close`; the corrected court verifies that the stale integer identity remains registered even though the Python object is gone. CPython address recycling was not observed within the bounded allocator loop on the governed runner, so address reuse itself is not used as the blocking evidence. The deterministic fork finding above is sufficient and demonstrates the same missing process/object-generation dimension without depending on allocator timing.

## Controls independently confirmed

The review separately confirmed the following R5 controls:

- valid registered `NONCURRENT_SYNTHETIC` positive and unregistered-basis negative controls remain functional;
- replacing the module-level broker request helper does not redirect the bound validator;
- unlinking/rebinding the broker pathname to an unrelated same-user server fails closed because the peer PID/start-time identity does not match;
- broker death fails closed;
- one-shot authority-child death fails closed;
- DENY-to-PERMIT body substitution is rejected;
- cross-receipt equal-positive-body reuse is rejected by exact record/authority-instance binding;
- constructor, `object.__new__`, subclass, mapping/proxy, JSON reconstruction, copy/deepcopy and pickle paths do not create accepted identities on the ordinary parent-process path;
- authority/schema/fixture/decision/basis-scope/basis-proof/authority-instance/integrity mutations fail closed;
- repeated and concurrent genuine validation keeps PERMIT/DENY results separated;
- a fresh second module/broker instance does not accept the first module instance's receipt;
- the registered positive basis is exact-scope bound across actor/world/subject/time/transition;
- cross-scope replay rejects;
- project-current-shaped, wrong-field, empty-suffix and exact current first-canary identifiers reject;
- project-current fixture rejects;
- classification/routing/occurrence/proximity/narrative-like surrogate basis strings deny;
- no current-positive OBL056, OBL055 execution, ENCOUNTER, OEE, actor/runtime mutation, public basis registration or adoption-effect surface was created.

## Separation / no-current-effect holding

`FROZEN_R5_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_R5_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`PROJECT_CURRENT_POSITIVE_CAUSAL_USE_PERMISSION_CREATED = NO`

`PROJECT_CURRENT_OBL056_POSITIVE_ENTRY_INSTALLED = NO`

`OBL055_EXECUTED = NO`

`ENCOUNTER_CREATED = NO`

`PROJECT_CURRENT_OEE_REALIZED = NO`

`OBL061_UNBLOCKED = NO`

`SUB_VOZHD_E_ADOPTION_CLAIMED = NO`

`HQ_ADOPTION_CLAIMED = NO`

No campaign, central, PRE-MAIN, main, sibling-lane, or frozen-candidate branch was moved by this review.
