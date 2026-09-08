# OBL058 — CAUSAL_USE_PERMISSION — R9 FRESH DISTINCT INDEPENDENT REVIEW — GOVERNED EVIDENCE R1

## Evidence result

`GOVERNED_REVIEW_COURT_EXECUTED_SUCCESSFULLY__SEMANTIC_DISPOSITION_FAIL`

The governed review court executed successfully against frozen R9 candidate `9b293aca913cff7f4d52d9e10dc08fcdb99127d9`. The court contains a deliberate reproduction check for the smallest independent blocker, so green workflow execution confirms that finding rather than implying semantic PASS.

## Exact identities

- repository: `maidiu/rawlsing`
- reviewer branch: `agent/rabochii-subv-e-obl058-causal-use-permission-r9-independent-review-r1`
- exact review start: `8abf6a7ecbb72a847c01011f1de253fed0eda558`
- immutable campaign authority: `b948aed197506905f4b5f1cab20a92e3ce6949b9`
- campaign authority tree: `bc11426ddcf8078bfabc1ac59a889bedd1d1f6b1`
- frozen R9 target: `9b293aca913cff7f4d52d9e10dc08fcdb99127d9`
- producer evidence supplied as context: `6d1b1c417d044e9e827f2da61aebaa76fa3d6c14`
- producer run/job supplied as context: `34281455637` / `102246930097`
- independent matrix freeze commit: `a1de412925b90f3729d822a9bd0816d875eefa20`
- independent test-surface commit: `99f41e51b7831d49e2ce0c4f7ad37a529937db1c`
- governed wrapper commit: `ee6a9c00f40ad29fb63b921c59141d700c5744dd`
- governed court-spec bind / evidence execution: `50180ebad36a4296cd6d1488fe5494fc55cf641c`
- execution-only PR: `#326`, closed unmerged
- PR synthetic merge identity recorded by the governed run: `6e9d0b85fc271b64faa29afadc286890f30c0e82`

## Governed court

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

## Independent finding

R9 materially closes the exact R8 pre-existing import-cache finding: a normal Python module placed under `_obl058_r8_native` before candidate import is rejected even when it copies the expected module name, file/origin claims, surface names and return shapes. The genuine accepted native module also exposes the expected C-extension bindings, and post-binding cache replacement plus ordinary Python socket-constructor replacement do not redirect the genuine path.

The review found a smaller remaining source-origin dispatch seam after that genuine binding succeeds.

`validate_receipt()` invokes `receipt._source_validate(...)` through normal Python attribute lookup on the exact Python-defined `IssuedReceipt` subclass. That class is mutable through ordinary Python runtime assignment. The governed review therefore issued a genuine unregistered-basis receipt, first confirmed its genuine decision was `DENY`, then assigned a normal Python function to `IssuedReceipt._source_validate`. The replacement returned `PERMIT` together with the genuine receipt's already-public authority-instance identifier. The unchanged public `validate_receipt()` accepted `PERMIT`, while the native transport-success counter did not increase. Removing the Python class override restored the same receipt to genuine `DENY` behavior.

Thus R9 validates the native module's origin at binding time but does not ensure that the later public validation call is dispatched through the non-rebindable native method descriptor it validated. Correctness is therefore shifted to a caller-mutable Python class callable surface.

Smallest exact blocker:

`BLOCKER__OBL058_R9_PUBLIC_VALIDATOR_DISPATCHES_THROUGH_CALLER_MUTABLE_RECEIPT_CLASS_METHOD_LOOKUP`

Semantic recommendation:

`FAIL__OBL058_R9_INDEPENDENT_REVIEW__MUTABLE_RECEIPT_METHOD_CAN_SUBSTITUTE_NATIVE_DECISION`

Smallest required next property:

`REQUIRES__PUBLIC_VALIDATION_TO_INVOKE_THE_VERIFIED_NATIVE_ENTRY_WITHOUT_CALLER_MUTABLE_PYTHON_CLASS_METHOD_DISPATCH`

## Preserved controls observed by this review

This FAIL is narrow. The independent court separately confirmed genuine synthetic `PERMIT` and unregistered `DENY`; exact R8 import-cache substitute rejection; genuine C-extension module binding; post-binding cache replacement not redirecting the native path; Python socket-constructor replacement remaining irrelevant; explicit close revocation and duplicate-close non-authorization; native lifetime accounting; forked positive/negative copy rejection with parent survival; child close not retiring parent authority; construction/subclass/mapping/proxy/JSON/copy/deepcopy/serialization rejection; exact five-field cross-scope rejection; exact registered-basis scope binding; field-specific `NONCURRENT_SYNTHETIC` and current/project-current-shaped rejection; surrogate-basis denial; distinct authority-instance identities for equal semantic inputs; stable concurrent validation; and no public source-basis registration or project-current effect surface.

## Separation and no-current-effect

`FRESH_DISTINCT_INDEPENDENT_REVIEW_COUNT_FOR_R9_CANDIDATE = 1`

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

A post-evidence tooling slip briefly created an empty placeholder file on the reviewer branch and immediately deleted it. It did not modify the frozen target, review matrix, review test, governed spec, or evidence execution. History was preserved without force update.
