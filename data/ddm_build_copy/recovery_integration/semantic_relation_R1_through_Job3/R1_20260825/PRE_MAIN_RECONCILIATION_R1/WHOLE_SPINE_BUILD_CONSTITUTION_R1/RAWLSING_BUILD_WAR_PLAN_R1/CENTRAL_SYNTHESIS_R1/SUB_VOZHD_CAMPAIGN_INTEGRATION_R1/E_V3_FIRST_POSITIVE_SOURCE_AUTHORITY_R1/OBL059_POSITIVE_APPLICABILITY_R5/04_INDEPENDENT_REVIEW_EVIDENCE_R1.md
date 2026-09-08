# OBL059 R5 FRESH INDEPENDENT REVIEW — EVIDENCE R1

Review role: `RABOCHII INDEPENDENT REVIEWER`

Worker branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r5-independent-review-r1`

Exact starting HEAD:
`87ca2d0d1944d5db8ac4512581fef3648946a487`

Frozen R5 candidate reviewed:
`9f7e965fbba64ce94239e36f011f7936681b605a`

Candidate executable blob:
`04cb331af0d7e0d4d14db901ecf79eb0d736bfe3`

Prospective campaign instruction/adjudication:
`dc831f6879c3e037968e5d583974a94edf92ddfb`

Campaign tree:
`a892d56bd18952097583d72aebbbed8bd174d83b`

Known producer evidence only:
`2be8ec089c103fad61710387678c7a09e9d72652`, run `34242233223`.

## Independent matrix freeze

Matrix/test/wrapper/spec were frozen before governed execution.

Independent matrix blob:
`2bacd5d83e5263aca4e5208f74b04334b02c6516`

Independent test blob:
`86375dfb7683ebd497f66db10e85297b1416761b`

Governed wrapper blob:
`c0bc5ab0430d889a5b1c00e46adedec1355a9f77`

Court spec blob:
`f01dd8ddf4e78fee298fc50c4773a4d26dbdbe7a`

Independent matrix freeze / governed evidence execution:
`000f993191c278ac727fb6401996829836b17630`

No review test or candidate file was changed after this freeze.

## Governed execution

Workflow:
`Rabochii Governed Bounded Court`

Run:
`34245551693` → `failure`

Job:
`102126481302` → `failure`

Protocol self-test:
`20 passed in 0.09s`

Independent review court:
`1 failed, 15 passed, 155 subtests passed in 0.15s`

Artifact:
`10063815997`

Artifact ZIP SHA-256:
`e58b30126c88baab64dee2b206585c91454356b43f2dabf63757e65ddc70fa03`

Execution-only PR:
`#294` — closed unmerged.

## Exact blocker reproduced

Failing review case:
`test_04_setting_change_after_structural_classification_remains_total`

The case uses malformed required binding `actor_id = 10 ** 5000` and a controlled synchronization barrier required by the review commission.

1. The process integer conversion setting is first set to `0` / unlimited.
2. R5 completes `_requires_total_projection(...)` for the malformed packet and returns `False`, meaning the value is classified as safe for the delegated path under that setting.
3. The review barrier holds the same in-flight evaluation immediately after that classification.
4. A second thread changes the process-global integer conversion setting to the supported minimum nonzero value, `640`.
5. The original evaluation resumes without reclassifying the integer under the new setting and delegates into the inherited R4/R3 receipt path.
6. Later canonical proof construction attempts decimal conversion of the same `10 ** 5000` value under the now-active 640-digit limit.
7. Python raises:
   `ValueError: Exceeds the limit (640 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit`
8. The malformed binding therefore does not produce the required deterministic negative receipt.

The review restores the process-global integer conversion setting and all temporary review instrumentation in `finally` cleanup.

## Holding

R5 correctly closes the producer's fixed-setting large-integer case and the remaining independent matrix cases were green, including threshold neighbors, supported setting states and cache reuse, bounded large configured limit, diagnostic sign/bit-length/binary digest, repeated and nearby-value proof behavior, exact built-in containers, cycles/shared/depth combinations, custom protocol isolation, primitive boundaries, scope/source/evidence/current controls, adjacent-claim non-substitution, and deliberate unrelated programmer-error visibility.

However, the frozen R5 candidate makes a time-separated decision using mutable process-global configuration and later delegates to code whose canonical encoder observes that same configuration again. A legitimate setting change in the classification-to-encoding window can therefore reopen the exact malformed-binding exception class R5 is required to keep closed.

Smallest blocker:
`BLOCKER__OBL059_R5_RUNTIME_INTEGER_LIMIT_CHANGE_AFTER_CLASSIFICATION_CAN_REOPEN_VALUEERROR`

Semantic review terminal:
`FAIL__OBL059_R5_INDEPENDENT_REVIEW__RUNTIME_INTEGER_LIMIT_CHANGE_REOPENS_NEGATIVE_RECEIPT_EXCEPTION`

Recommendation:
`FAIL__DO_NOT_ADOPT_OBL059_R5_CANDIDATE`

## Separation and no-current-effect attestations

`REPAIR_PERFORMED_BY_REVIEWER = NO`

`SECOND_REVIEW_COMMISSIONED = NO`

`INDEPENDENT_REVIEW_COUNT_FOR_FROZEN_R5_CANDIDATE = 1`

No actor was created or activated. No ADP-008 transition was executed. No ADP-019 occurrence was admitted. No current-positive OBL056 entry was installed. OBL055 was not executed. No ENCOUNTER or OEE was created. No project-current positive applicability or authority-index mutation occurred. No SUB-VOZHD E or HQ adoption is claimed. OBL058 was not modified by this lane-local review.
