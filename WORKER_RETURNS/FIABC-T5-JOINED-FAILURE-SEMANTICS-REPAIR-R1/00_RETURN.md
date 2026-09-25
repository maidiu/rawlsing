# FIABC T5 JOINED FAILURE SEMANTICS REPAIR — R1

## Terminal

`PASS__FIABC_T5_JOINED_FAILURE_SEMANTICS_SOURCE_FREE_QUALIFIED__HQ_PROMOTION_REQUIRED`

## Exact branch / base

- Repair branch: `agent/rabochii-fiabc-t5-joined-failure-semantics-repair-r1`
- Commission commit: `56a8958b4e2ee9fa4f5096b6922ca390f69f9442`
- Exact protected base: `3d8f2ad62600b6777dcb23a28404a067502e77a0`
- Exact qualified implementation head: `41eea54d7610a47f1adc342c6caacaf11324a40c`
- Protected execution branch mutated: **NO**
- Raw LiTS/WVS opened/hashed/decoded: **NO**
- Candidate A/B/C launched: **NO**
- Measured P2X run: **NO**

## What was broken

The joined court had a real post-backend failure-semantics hole.

If A or B failed candidate-locally before or at S05, there was lawfully no same-source
`fiabc_t5_candidate_observation.json` for that failed candidate. Later C could pass its own backend S05, after which the driver called `admit_post_i05_oracle_match()`. The old T5 helper unconditionally loaded A, B, and C observations for the three-way gate. The missing peer raised `LiveTerminalControlError` **after** `backend.run_stage()` had already returned, outside the driver's typed backend exception surface.

That produced an untyped orchestration crash. It also left C's process in the awkward state Worker C identified: backend PASS had retained the C child for S06, but the outer T5 crash happened before a lawful stage terminal/transition could stop it.

## Repaired C/S05 law

The repair keeps individual candidate truth and three-way source qualification distinct.

Every candidate first undergoes its own comparison to the already-frozen candidate-neutral oracle. An own-oracle mismatch is now an existing governed:

- `CANDIDATE_LOCAL_FAILURE`
- `PARITY_ORACLE_FAILURE`
- `CANDIDATE_ONLY`

For C, three-way PASS is possible only when **three actual same-source passing observations** exist. If A or B is missing/malformed because an earlier candidate failed, or if three-way parity itself rejects:

- C's own independent match is retained when it passed;
- no missing observation is synthesized;
- no three-way PASS is written;
- no C qualifying cell terminal is fabricated;
- the exact existing governed disposition is:
  - `COMMON_SOURCE_BLOCKER`
  - `PARITY_ORACLE_FAILURE`
  - `SOURCE_ONLY`
  - candidate `null`.

The remaining same-source stages are propagated as `BLOCKED_BY_COMMON_SOURCE_AUTHORITY`. A later source remains eligible. T5 still has no cross-source live dependency before S17.

See:
- `01_FAILURE_SEMANTICS_MATRIX.json`
- `02_C_S05_THREE_WAY_ADJUDICATION.json`

## Whole post-backend typed path

The repair does not special-case only C/S05. The driver now audits the full post-backend T4/T5 seam:

- T4 `LiveAccountingError` after backend PASS becomes a typed `COMMON_COURT_BLOCKER / COMMON_COURT_AUTHORITY_FAILURE / COURT_UNTIL_RESUME`.
- Expected T5 post-I05 candidate mismatch/source three-way failure is returned as the typed existing candidate/source disposition described above.
- A residual T5 control-plane `LiveTerminalControlError` becomes a common-court authority blocker.
- S16 cell-terminal qualification `LiveTerminalControlError` becomes a typed candidate-local correctness failure.
- Unrelated programming exceptions such as `ValueError` are **not** swallowed by a broad catch and still escape as programming failures.

Outer-control non-PASS now gets the same failure-evidence roles required by the driver-bound verifier:
`cell_receipt` and `failure_receipt`, with no synthetic fallback.

See `04_POSTBACKEND_TYPED_EXCEPTION_AUDIT.json`.

## Process lifecycle closure

A backend PASS may retain a same-cell child for an authorized warm transition. Therefore an outer T4/T5 gate that later reclassifies that stage as non-PASS must terminate that retained process lawfully.

The repair adds a reusable exact-cell stop interface through:

- `ProcessIsolationController.stop_after_outer_nonpass(...)`
- `ee_p2x_process_isolated_backend.stop_after_outer_nonpass(...)`
- joined driver helper `_stop_backend_after_posthook_nonpass(...)`.

It uses the existing graceful STOP path, rejects cross-cell attribution, and does not change the ordinary PASS warm-retention law. At S05, an outer non-PASS with no retained process is itself treated as a control error rather than silently tolerated.

## S17 / final non-PASS law

Success S17 remains success-only.

If any candidate-local failure survives to the final gate, S17's success backend is not invoked. The court emits:

`COURT_SEQUENCE_COMPLETE__CANDIDATE_LOCAL_FAILURES_RECORDED__S17_SUCCESS_VERIFIER_NOT_RUN`

with an explicit `RAWLSING_FIABC_T5_LIVE_FINAL_NONPASS@1.0.0` receipt.

If a common-source blocker survives, the final court preserves the **smallest real scope** instead of upgrading it to a made-up court-wide blocker:

`COURT_SEQUENCE_COMPLETE__COMMON_SOURCE_BLOCKERS_RECORDED__S17_SUCCESS_VERIFIER_NOT_RUN`

with `BLOCKED_BY_COMMON_SOURCE_AUTHORITY`.

A genuine common-court blocker still stops immediately as court-wide and requires resume.

Every final non-PASS receipt states, explicitly:

- `s17_success_backend_invoked=false`
- `s17_success_claimed=false`
- `six_cell_pass_claimed=false`
- `terminal_bundle_fabricated=false`
- `missing_success_evidence_synthesized=false`.

See `03_S17_NONPASS_TERMINAL_ADJUDICATION.json`.

## Source-free matrix

The dedicated test file is:

`rawlsing_next/tests/test_fiabc_t5_joined_failure_semantics_repair.py`

It contains **67 source-free cases**, including the required actual-manifest matrix:

- both LiTS and WVS;
- A/B/C;
- S01;
- before S05;
- at S05;
- after S05;
- S16;
- common-source blockers early/middle/late on both sources;
- common-court blockers early/middle/late on both sources;
- C/S05 missing A/B observations after peer failure;
- same-source-only dependency proof with foreign-source observations present but ineligible;
- individual oracle mismatch typing;
- outer T4/T5 typed conversion;
- S16 terminal qualification failure;
- programming-error non-swallowing;
- retained-process graceful stop;
- final non-PASS anti-fabrication;
- all-PASS C/S05 and driver transition conservation.

The one requested matrix coordinate that cannot lawfully execute under the current manifest is **LiTS-B/S01**: it is `DONE__PRESERVE`. The test covers that coordinate by proving execution/failure origination there is forbidden rather than fabricating a candidate failure on a preserved stage.

## Executed qualification

A disposable qualification branch and draft PR were used only to obtain GitHub-hosted source-free execution. They were not merged; PR **#447** was closed after qualification.

Exact green run:

- workflow: `Rabochii Governed Bounded Court`
- run: `36187125580`
- evidence execution SHA: `cc8f0c83138fc515cad32083063e29d546b23227`
- semantic candidate SHA: `41eea54d7610a47f1adc342c6caacaf11324a40c`
- protocol self-test: **20/20 PASS**
- repair + adjacent T3/T4/T5 court: **103/103 PASS**
- bounded-court receipt: `PASS`
- artifact: `10887225909`
- artifact digest: `sha256:19c3b0d1529b7584288587f7a74c617339d47b0875f8956091557fe40181bcce`

The qualification passed without raw survey sources or measured P2X.

See `05_SOURCE_FREE_QUALIFICATION.json`.

## Historical driver binding: expected promotion debt, not hidden failure

A first broader qualification run deliberately included
`test_ee_p2x_local_court_driver_integration.py`.

Result:

- **108 passed**
- **5 failed**

All five failures stop on the same historical binding check:

`FAILURE__QUALIFIED_DRIVER_BLOB_DRIFT`

because existing protected
`WORKER_RETURNS/EE-P2X/10B_DARWIN_DRIVER_RECEIPT_BINDING.json`
still pins the old driver blob:

`02ca7cc9f5bf8665de712980a05fdcc059b93331`

while the repaired driver blob is:

`70bf233492b543d3d728cedfdda36218504ef3d4`.

Worker did **not** rewrite historical qualification evidence in place. That binding must be reissued/requalified by HQ if this protected-code repair is promoted. This is why the success terminal explicitly ends in `HQ_PROMOTION_REQUIRED`.

The T2 execution manifest itself remains byte-identical to protected base.

See:
- `06_PROTECTED_BASE_NO_UNRELATED_DRIFT.json`
- `07_IMPLEMENTATION_HEAD.json`

## Split reuse

This exact protected base predates the later source-local split driver, so this branch does not import or patch later split-control history.

The repair is nevertheless intentionally reusable rather than joined-only. Later split fan-in must use the same:

1. `admit_post_i05_oracle_match`
2. `_backend_terminal`
3. `_stop_backend_after_posthook_nonpass`

sequence, with the stop helper called immediately after terminal adjudication and before failure propagation.

No split-specific failure vocabulary is needed or permitted.

See `08_SPLIT_REUSE_INTERFACE.json`.

## HQ promotion requirements

Before any measured use of this repair:

1. review/promote exact implementation head `41eea54d7610a47f1adc342c6caacaf11324a40c`;
2. reissue/requalify the driver-bound 10B binding (or lawful successor) against repaired driver blob `70bf233492b543d3d728cedfdda36218504ef3d4`;
3. if later split fan-in consumes the repair, wire the shared posthook-stop helper exactly as documented;
4. rerun the full source-free driver-bound court against the promoted/rebound head.

No measured execution is authorized by this worker return alone.

## Exact terminal

`PASS__FIABC_T5_JOINED_FAILURE_SEMANTICS_SOURCE_FREE_QUALIFIED__HQ_PROMOTION_REQUIRED`
