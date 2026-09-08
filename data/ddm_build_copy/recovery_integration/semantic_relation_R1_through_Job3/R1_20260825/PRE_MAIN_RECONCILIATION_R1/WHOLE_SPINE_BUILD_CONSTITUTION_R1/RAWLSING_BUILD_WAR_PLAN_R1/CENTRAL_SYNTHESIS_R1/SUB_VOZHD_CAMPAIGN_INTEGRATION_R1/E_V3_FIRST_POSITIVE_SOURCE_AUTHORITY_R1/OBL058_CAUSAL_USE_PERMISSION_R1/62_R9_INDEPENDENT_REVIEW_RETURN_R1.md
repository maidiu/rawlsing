# OBL058 — CAUSAL_USE_PERMISSION — R9 FRESH DISTINCT INDEPENDENT REVIEW R1 — RETURN TO SUB-VOZHD E

## Terminal

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R9_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`

State after terminal: `CLOSURE_ONLY`.

## Recommendation

`FAIL__OBL058_R9_INDEPENDENT_REVIEW__MUTABLE_RECEIPT_METHOD_CAN_SUBSTITUTE_NATIVE_DECISION`

Smallest exact blocker:

`BLOCKER__OBL058_R9_PUBLIC_VALIDATOR_DISPATCHES_THROUGH_CALLER_MUTABLE_RECEIPT_CLASS_METHOD_LOOKUP`

Frozen R9 candidate `9b293aca913cff7f4d52d9e10dc08fcdb99127d9` is not yet lawful for SUB-VOZHD E adoption consideration. R9 does close the exact R8 pre-existing import-cache source-origin finding, but the public validation path still resolves the correctness-relevant native method through a mutable Python class attribute lookup.

No repair was performed by this reviewer.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r9-independent-review-r1`
- exact review start: `8abf6a7ecbb72a847c01011f1de253fed0eda558`
- immutable campaign authority: `b948aed197506905f4b5f1cab20a92e3ce6949b9`
- campaign authority tree: `bc11426ddcf8078bfabc1ac59a889bedd1d1f6b1`
- frozen R9 target reviewed unchanged: `9b293aca913cff7f4d52d9e10dc08fcdb99127d9`
- producer evidence supplied as context: `6d1b1c417d044e9e827f2da61aebaa76fa3d6c14`
- producer run/job supplied as context: `34281455637` / `102246930097`
- independent matrix freeze commit: `a1de412925b90f3729d822a9bd0816d875eefa20`
- independent matrix blob: `ffad7aa6dd38b4e4037e8bd08bb83c4b048884ad`
- independent test-surface commit: `99f41e51b7831d49e2ce0c4f7ad37a529937db1c`
- independent test-surface blob: `98d1eb8216d1236393c1d781d37f82117b758680`
- governed wrapper commit: `ee6a9c00f40ad29fb63b921c59141d700c5744dd`
- governed wrapper blob: `4511b9c73334fd5ee02333169521acec744e4eda`
- governed court-spec bind / evidence execution: `50180ebad36a4296cd6d1488fe5494fc55cf641c`
- governed court-spec blob: `ccec548323c16ade0ac359641caf1a6ef6bace50`
- governed evidence packet commit: `5dc0e8820afe3003c82a38c796ce525d1b638187`
- governed evidence packet blob: `b4580033d24827c717d5c6c9b8a4970cecac46ca`
- execution-only PR: `#326`, closed unmerged
- governed-run PR synthetic merge identity: `6e9d0b85fc271b64faa29afadc286890f30c0e82`
- final reviewer tip: reported out of band after this terminal commit because a file cannot contain its own immutable commit SHA without changing that SHA.

## Independent finding

R9 genuinely rejects the exact R8 pre-existing import-cache substitute. A normal Python module under `_obl058_r8_native` is rejected even when it copies the expected module name, surface names, return shapes and claimed file/origin path. The genuine accepted module exposes C-extension functions bound to the exact module object, and ordinary post-binding cache replacement or Python socket-constructor replacement does not redirect the genuine native transport.

The remaining seam is later dispatch from the original public validator. `validate_receipt()` calls `receipt._source_validate(...)` through ordinary Python attribute lookup on the Python-defined `IssuedReceipt` subclass. That subclass is mutable at runtime.

The governed independent court issued a genuine unregistered-basis receipt and first confirmed its source decision was `DENY`. It then assigned a normal Python function to `IssuedReceipt._source_validate`. That function returned `PERMIT` plus the genuine receipt's public authority-instance identifier. Without changing `validate_receipt()` or the frozen receipt body, the original public validator returned `PERMIT`; the native transport-success counter did not increase. Deleting the class override immediately restored the same receipt to genuine `DENY` behavior.

Therefore R9 verifies the native module at binding time but does not guarantee that the later public validation call reaches the verified non-rebindable native method descriptor. Correctness has shifted from the R8 import-cache key to a caller-mutable Python class callable surface.

Smallest required next property:

`REQUIRES__PUBLIC_VALIDATION_TO_INVOKE_THE_VERIFIED_NATIVE_ENTRY_WITHOUT_CALLER_MUTABLE_PYTHON_CLASS_METHOD_DISPATCH`

This reviewer does not prescribe an implementation. Any changed candidate is a new semantic target and must follow whatever bounded repair/review sequence SUB-VOZHD E lawfully commissions.

## Governed independent evidence

- workflow: `Rabochii Governed Bounded Court`
- run: `34284481630`
- job: `102256751005`
- workflow conclusion: `success`
- runner: Ubuntu `24.04.5`
- Python / implementation: `3.12.14` / `CPython`
- protocol self-tests: `20 passed in 0.07s`
- court-spec validation: `PASS`
- independent review court: `24 passed, 42 subtests passed in 6.04s`
- bounded-court receipt: `PASS`, exit code `0`
- receipt elapsed seconds: `6.221884`
- receipt semantic candidate: `9b293aca913cff7f4d52d9e10dc08fcdb99127d9`
- receipt evidence execution: `50180ebad36a4296cd6d1488fe5494fc55cf641c`
- receipt spec SHA-256: `50df0adf31f9441233df77dca1ca7951ee74eb60165bdc8c66963e2742d0d2bf`
- artifact ID: `10078911864`
- artifact ZIP SHA-256: `e8658332e6e7298af1a761cb1d1bfb2c55e3155f1c2dca684e1ea052f2c058f1`

The green workflow is a reproduction court for the blocker. The blocking check intentionally asserts the observed incorrect-positive class-method dispatch behavior, so green execution confirms semantic FAIL rather than PASS.

## Preserved R9 controls

This FAIL is narrow. The independent court separately confirmed genuine synthetic `PERMIT` and unregistered-basis `DENY`; exact R8 import-cache substitute rejection; genuine C-extension module binding; post-binding cache replacement not redirecting the native path; Python socket-constructor replacement remaining irrelevant; explicit close revocation and duplicate-close non-authorization; native lifetime accounting; forked positive/negative copy rejection with parent survival; child close not retiring parent authority; construction/subclass/mapping/proxy/JSON/copy/deepcopy/serialization rejection; exact five-field cross-scope rejection; exact registered-basis scope binding; field-specific `NONCURRENT_SYNTHETIC` and current/project-current-shaped rejection; surrogate-basis denial; distinct authority-instance identities for equal semantic inputs; stable concurrent validation; and no public source-basis registration or project-current effect surface.

## Review count / separation

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R9_CANDIDATE = 1`

`FROZEN_CANDIDATE_MODIFIED_BY_REVIEWER = NO`

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`EXECUTION_ONLY_PR_MERGED = NO`

## No-current-effect attestation

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

No central, PRE-MAIN, main, campaign, sibling-lane, or frozen-candidate branch was moved by this reviewer.

A post-evidence tooling slip briefly created an empty placeholder file on the reviewer branch and immediately deleted it. It did not modify the frozen candidate, review matrix, review test, governed spec, or evidence execution, and no force update was used.

## Return Beacon completion

The accompanying `.rabochii/return_manifest.json` is committed in the same final branch-tip commit as this return packet. It truthfully declares `FAIL`, `CLOSURE_ONLY`, durable required outputs, completed governed evidence, no required/background work remaining, and review/repair separation under `RABOCHII_RETURN_MANIFEST@1.0.0`.

Exact terminal:

`RABOCHII_SUBV_E_OBL058_CAUSAL_USE_PERMISSION_R9_INDEPENDENT_REVIEW__RETURN_TO_SUB_VOZHD_E`
