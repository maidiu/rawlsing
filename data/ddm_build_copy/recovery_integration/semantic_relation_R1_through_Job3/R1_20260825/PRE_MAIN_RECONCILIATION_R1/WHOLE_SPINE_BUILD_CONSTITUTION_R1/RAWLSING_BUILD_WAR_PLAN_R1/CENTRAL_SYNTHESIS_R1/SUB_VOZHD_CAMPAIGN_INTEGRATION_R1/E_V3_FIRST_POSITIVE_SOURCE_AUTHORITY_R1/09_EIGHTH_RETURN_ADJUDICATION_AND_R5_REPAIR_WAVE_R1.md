# SUB-VOZHD E — EIGHTH RETURN ADJUDICATION AND R5 REPAIR WAVE R1

Campaign branch: `agent/sub-vozhd-v3-first-positive-source-authority-r1`

Prior campaign tip: `f7618257604c362097edb3c78dae8480a9499c4a`

This adjudication consumes the exactly-one fresh independent reviews of the frozen OBL058 R4 and OBL059 R4 candidates. Both returned FAIL. No second review of either frozen R4 candidate is lawful or commissioned. Any later review must target a newly repaired candidate. OBL060 remains held at its prior SUB-VOZHD E PASS.

## OBL058 — CAUSAL_USE_PERMISSION R4 REVIEW RETURN

Review branch:
`agent/rabochii-subv-e-obl058-causal-use-permission-r4-independent-review-r1`

Final review tip:
`b9ea19aaa74d9e1b3ba2c52b6a4e27056c4e1dee`

Frozen R4 candidate reviewed:
`f02509a25b23365596ccedc7c8bc3a973dce3468`

Governed evidence execution:
`73ed58b10595ecfca32009e44758e4fee7daf372`

Governed run/job:
`34238219350` / `102101357437`

GitHub Actions independently confirms run `34238219350` completed `success`. The court was a reproduction court: green execution confirmed the incorrect-positive transport-response paths.

Review recommendation:
`FAIL__OBL058_R4_INDEPENDENT_REVIEW__CALLER_REBINDABLE_TRANSPORT_RESPONSE_BREAKS_SOURCE_ORIGIN`

Smallest blocker:
`BLOCKER__OBL058_R4_VALIDATOR_TRUSTS_CALLER_REBINDABLE_PARENT_TRANSPORT_RESPONSE`

The one-shot child closes the prior closure-ledger defect, but parent-visible receipt slots still carry `_body_json`, `_write_fd`, `_read_fd`, and `_proc`, and validation does not establish that the descriptors belong to the exact source-owned child initialized for that receipt or that the returned decision came from that child. The review reproduced both an exact-type fabricated receipt accepted through caller-created pipes/unrelated live process and conversion of a legitimate DENY to PERMIT after transport-field replacement. No repair was performed by the reviewer.

Adjudication:
`OBL058_R4_REVIEW_FAIL__DO_NOT_ADOPT__R5_BOUNDED_REPAIR_REQUIRED`

Commission exactly one repair-only continuation:

Branch:
`agent/rabochii-subv-e-obl058-causal-use-permission-bounded-repair-r5`

Exact starting HEAD:
`b9ea19aaa74d9e1b3ba2c52b6a4e27056c4e1dee`

R5 must bind validation to the actual source-owned authority instance and exact receipt identity/body without trusting caller-rebindable receipt transport/process fields. The repair must close both reproduced incorrect-positive paths and equivalent transport/handle substitution or response-spoofing routes while preserving the one-shot child decision, exact basis/scope/fixture controls, and all no-current-effect boundaries. R5 must freeze a new candidate, obtain a governed green bounded-repair court, and stop before independent review.

## OBL059 — POSITIVE_APPLICABILITY R4 REVIEW RETURN

Review branch:
`agent/rabochii-subv-e-obl059-positive-applicability-r4-independent-review-r1`

Final review tip:
`a728990458a4a909186b99520df6bb1cc9a826f1`

Frozen R4 candidate reviewed:
`830cc0442f34e8b28405006c031cc1d256893a17`

Independent matrix/evidence freeze:
`4583df1b72b5ac663b57cf44d9a5a07a2e75a261`

Governed run/job:
`34238158851` / `102101147753`

GitHub Actions independently confirms run `34238158851` completed `failure`, matching the bounded review result `5 failed, 18 passed, 124 subtests passed`.

Review terminal:
`FAIL__OBL059_R4_INDEPENDENT_REVIEW__LARGE_INTEGER_NEGATIVE_RECEIPT_CONSTRUCTION_INCOMPLETE`

Smallest blocker:
`BLOCKER__OBL059_R4_EXACT_INTEGER_JSON_SAFE_CLASSIFICATION_OMITS_ENCODER_CONVERSION_LIMIT`

The review reproduced the same failure at every required-binding field using exact built-in integer `10 ** 5000`. R4 classifies exact integers as structurally JSON-safe and delegates to R3; the malformed-binding fallback then preserves the huge integer and canonical proof encoding raises Python's integer-to-string conversion `ValueError` instead of returning the deterministic negative receipt. No repair was performed by the reviewer.

Adjudication:
`OBL059_R4_REVIEW_FAIL__DO_NOT_ADOPT__R5_BOUNDED_REPAIR_REQUIRED`

Commission exactly one repair-only continuation:

Branch:
`agent/rabochii-subv-e-obl059-positive-applicability-bounded-repair-r5`

Exact starting HEAD:
`a728990458a4a909186b99520df6bb1cc9a826f1`

R5 must make malformed-binding classification/projection total for exact integers whose canonical encoding would exceed the runtime encoder conversion limit, without decimal conversion of unbounded integers, without changing valid applicability semantics, and without masking unrelated programmer errors. It must freeze a new candidate, obtain a governed green bounded-repair court, and stop before independent review.

## OBL060 — CONTACT_WITNESS_INDEPENDENCE

Prior SUB-VOZHD E adjudication remains unchanged:
`PASS__OBL060_R2_CONTACT_WITNESS_INDEPENDENCE__READY_FOR_HQ_ADOPTION_CONSIDERATION_WHEN_FANIN_COMPLETE`

No additional OBL060 worker is commissioned.

## Fan-in state

`OBL058 = R4_REVIEW_FAIL__R5_REPAIR_COMMISSIONED`

`OBL059 = R4_REVIEW_FAIL__R5_REPAIR_COMMISSIONED`

`OBL060 = SUB_VOZHD_E_PASS__HQ_ADOPTION_CONSIDERATION_PENDING_FANIN`

After each R5 repair returns a new frozen candidate with a green governed court, SUB-VOZHD E must commission exactly one fresh distinct independent review for that new candidate. The failed R4 reviewers are not rerun against the old candidates.

No HQ adoption packet is lawful yet.

## Hard gates unchanged

`OBL061 = HARD_BLOCKED`

`POSITIVE_V3_EXECUTION = NOT_AUTHORIZED`

`PROJECT_CURRENT_FIRST_CANARY_OEE = NOT_AUTHORIZED`

Do not create or activate the current actor, execute current ADP-008, admit current ADP-019 occurrence, install current-positive OBL056 entries, execute OBL055, create ENCOUNTER, realize project-current OEE, mutate project-current authority state, or claim HQ adoption.

No comparator, PSEPF, OBL032, architecture/topology selection, or sibling-campaign work.

Terminal:

`SUB_VOZHD_E_EIGHTH_RETURN_ADJUDICATION__OBL058_OBL059_R4_REVIEWS_FAIL__R5_REPAIRS_COMMISSIONED__OBL060_PASS_HELD`
