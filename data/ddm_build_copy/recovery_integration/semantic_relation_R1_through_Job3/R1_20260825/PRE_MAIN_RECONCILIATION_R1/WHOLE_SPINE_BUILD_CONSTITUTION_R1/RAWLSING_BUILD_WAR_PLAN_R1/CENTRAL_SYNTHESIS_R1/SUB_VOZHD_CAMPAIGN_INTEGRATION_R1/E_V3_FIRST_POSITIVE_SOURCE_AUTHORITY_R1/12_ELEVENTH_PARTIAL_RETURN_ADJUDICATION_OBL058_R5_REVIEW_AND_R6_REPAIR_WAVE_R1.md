# SUB-VOZHD E — ELEVENTH PARTIAL RETURN ADJUDICATION — OBL058 R5 REVIEW + R6 REPAIR WAVE R1

Campaign branch: `agent/sub-vozhd-v3-first-positive-source-authority-r1`

Prior campaign tip: `77127860ac887810a3dd28219617c305756fad21`

This adjudication consumes the exactly-one fresh distinct independent review of frozen OBL058 R5 candidate `43474152150350c1b5c73374abd24ecebc627b99` from review tip `c299ab4765d513b45815b19be131e4d5082b397a`.

## OBL058 — CAUSAL_USE_PERMISSION R5 REVIEW RETURN

Review branch:
`agent/rabochii-subv-e-obl058-causal-use-permission-r5-independent-review-r1`

Exact review start:
`f5d334c9d0f86ad3acc350389d151280953fa6a8`

Final reviewer tip:
`c299ab4765d513b45815b19be131e4d5082b397a`

Frozen R5 candidate reviewed:
`43474152150350c1b5c73374abd24ecebc627b99`

Governed evidence execution:
`f36c039fd3d56314f8f95db615a1a90a4c162f78`

Governed run/job:
`34251098195` / `102145432110`

Independent court:
`18 passed, 37 subtests passed in 3.06s`

Artifact:
`10066017222`

Artifact ZIP SHA-256:
`82e3f89b82760001c8ef63713045c2d790272022381c7be19751f453ca37ecf6`

Review recommendation:
`FAIL__OBL058_R5_INDEPENDENT_REVIEW__FORKED_PROCESS_RECEIPT_COPY_RETAINS_ACCEPTED_SOURCE_ORIGIN`

Smallest blocker:
`BLOCKER__OBL058_R5_BROKER_OBJECT_ID_BINDING_OMITS_REQUESTER_PROCESS_GENERATION`

The review confirmed that R5 materially closes the R4 parent-transport substitution defect. The remaining defect is narrower: broker authority is keyed by the bare process-local integer object ID plus body/authority-instance state, without binding the requester process generation that owns the Python object. A forked child receives a process-local copy at the same virtual address, so the copied receipt can present the same integer ID/body to the genuine broker and be accepted without a new source-owned issuance decision for the child-process object.

The review also observed a stale broker record can remain after a directly registered non-pinned shell is released until explicit close. Allocator-dependent same-process ID reuse was not used as the blocking claim, but the next repair should close object-generation staleness as part of the same exact boundary where practical.

Preserved R5 controls remain valid and must not be reopened: broker endpoint/PID/UID/start-time verification; unrelated same-user endpoint replacement rejection; broker/authority-child death fail-closed; exact five-field basis/scope binding; NONCURRENT namespace and first-canary/current-shaped rejection; body/proof/schema/fixture/integrity checks; reconstruction/fabrication/copy/serialization rejection on ordinary paths; replay and concurrent-validation controls; inference-like surrogate denial; and no project-current effects.

Adjudication:
`OBL058_R5_REVIEW_FAIL__DO_NOT_ADOPT__R6_BOUNDED_REPAIR_REQUIRED`

Exactly one repair-only continuation is commissioned.

Branch:
`agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r6`

Exact starting HEAD:
`c299ab4765d513b45815b19be131e4d5082b397a`

R6 must bind source-origin validation to the actual requester process generation and exact issued object generation rather than the bare integer `id(receipt)` alone. The deterministic forked-copy path must fail closed. The same bounded repair should ensure stale broker records cannot authorize a later object generation after the issued object is gone.

R6 must freeze a new candidate, obtain a green governed producer court, and stop before independent review.

## Other lanes

OBL059 remains exactly as stated at campaign tip `77127860ac887810a3dd28219617c305756fad21`; this adjudication does not enter or modify that lane.

OBL060 remains held at:
`PASS__OBL060_R2_CONTACT_WITNESS_INDEPENDENCE__READY_FOR_HQ_ADOPTION_CONSIDERATION_WHEN_FANIN_COMPLETE`

No HQ adoption packet is lawful yet.

## Hard gates unchanged

`OBL061 = HARD_BLOCKED`

`POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`

`PROJECT_CURRENT_FIRST_CANARY_OEE = NOT_AUTHORIZED`

No project-current actor/runtime mutation, current-positive OBL056 installation, OBL055 execution, ENCOUNTER, OEE realization, authority-index mutation, PRE-MAIN/main movement, or HQ-adoption claim is authorized.

Terminal:

`SUB_VOZHD_E_ELEVENTH_PARTIAL_RETURN_ADJUDICATION__OBL058_R5_REVIEW_FAIL__R6_REPAIR_COMMISSIONED`