# EE-P2R6W — S17 PRETERMINAL VERIFIER ORCHESTRATION + COURT FAILURE-PATH REPAIR

Repository: `maidiu/rawlsing`

## Execution surface
**BROWSER**

## Library access
**NO**

Exact branch:
`agent/rabochii-prev3-ee-p2r6w-s17-orchestration-repair-r1`

Exact base:
`ae8b1db9d8c3288e002950ac01123c70f3138320`

Resolve live HQ first.

Commission-time checkpoint:
`20260919T0327-0400`

Immutable handoff:
`b994ea63d2b9571415677e0d47a16bcd3e8322bf`

Controlling decision:
`HQD-2026-09-19-081`

## Mission

Repair only the exact S17 orchestration mismatch exposed by P2X.

Current driver:
`rawlsing_next/ee_p2x_darwin_court_driver.py`
blob `c3a368270f6f7a6f613efb78e31972e64a092c88`

Current backend:
`rawlsing_next/ee_p2x_darwin_stage_backend.py`
blob `fb30167ebc060939e17eb15c71b93c000033eb4f`

Current driver-bound verifier:
`WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py`
blob `da8f3434f791c9f6495238b28817de4b3e328ad3`

Adopted README law states that when the verifier is invoked as the S17 backend, S00-S16 must be terminal and **S17 itself need not yet exist because the driver writes S17 terminal only after backend returns**.

Current driver violates that by calling `ledger.begin(S17)` before backend invocation.

### Required repair law

For every non-S17 READY stage, ledger BEGIN-before-backend behavior remains unchanged.

For `COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION` only:

1. run existing `_final_ready` first;
2. compute exact input identity/context;
3. invoke backend S17 **without first creating a RUNNING S17 ledger entry**;
4. backend S17 invokes the existing driver-bound verifier unchanged;
5. only after backend PASS does driver terminalize S17 through the existing backend envelope / `ledger.complete`;
6. post-run external `--verify-only` remains required exactly as adopted.

Do not weaken the final verifier.

### Court-scope failure path

If S17 backend verification returns an exact common-court blocker, the backend failure path must not call normal candidate-cell serialization for synthetic `COURT/ALL`.

Repair court-scope failure evidence so it is candidate-neutral and verifier-bindable without `order.index("COURT/ALL")`.

Do not alter ordinary source/candidate failure receipts.

The driver-bound verifier's semantics must remain at least as strict as current authority. Prefer no verifier changes unless qualification proves one is unavoidable.

## Qualification

Prove:

- S17 backend is invoked with no S17 ledger entry present;
- all S00-S16 must be terminal before S17;
- successful S17 verifier call produces exact PASS terminal and driver then terminalizes S17;
- external final verifier can then validate terminal S17;
- failure at S17 returns typed common-court evidence with no ValueError;
- normal candidate/source stages still BEGIN before backend;
- no candidate-local failure is allowed at S17;
- no measurement/carrier access.

Production changes limited to driver/backend unless exact proof requires verifier change.

PASS:
`EE_P2R6W_PASS__S17_PRETERMINAL_VERIFIER_ORDERING_AND_COURT_SCOPE_FAILURE_PATH_REPAIRED__READY_FOR_HQ_SELECTIVE_FANIN`

BLOCK:
`EE_P2R6W_BLOCK__<EXACT_FIRST_S17_DRIVER_BACKEND_VERIFIER_CONTRACT_FAILURE>`

Do not move P2X. Return to HQ.
