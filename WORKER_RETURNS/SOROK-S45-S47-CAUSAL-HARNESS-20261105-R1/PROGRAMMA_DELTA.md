# PROGRAMMA_DELTA — S45-S47 causal harness R1

**Delta ID:** `SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1`
**Commission base:** `078d9c57bc835a34e90b3671bdef6c28a0f43747`
**Result:** `PASS` engineering causal regression at exact pins.
**Grade:** `TEST_ONLY_ENGINEERING_CAUSAL_REGRESSION_NOT_INDEPENDENT_FINAL_REVIEW`.

## Delta

Added only:

- `run_causal_harness.py` — callable harness accepting source root and explicit pinned paths.
- `harness/pins.py` — exact pin table, in-checkout staging and blob verification.
- `harness/scenarios.py` — same-root ACTUAL vs SCHEDULED_ONLY, S47 C9, S45
  DO_HELP, sever/restore, cold replay and wrong-root negative.
- `README.md`, `00_RETURN.md`, `evidence/`, `logs/` — interface, results and receipts.

## Not changed

- No PROGRAMMA canonical product, function identity, seam register, gate
  register or protected PRE-MAIN content.
- No product code, expected psychology, S45/S46/S47 source, S37/S42 seam source
  or any other worker return.
- No native C8/C9/C12, CAN008/CAN011, ADP, Pyat or human authority.
- No new independent acceptance or receiving decision.

## Receiving value

The delta gives the receiving lead a reproducible, fail-closed engineering check
that the already-executed S45-S47 sourcefree spine still produces the specified
same-root causal consequence at the exact pins:

- ACTUAL performed interval -> material `0`, S47 C9 material ineligible, S45
  `DO_HELP` refused.
- SCHEDULED_ONLY -> material `1`, S47 C9 material eligible, S45 `DO_HELP`
  accepted.
- Dependency cut -> RED `S46_INTERVAL_CONDITION_REVOKED`; restore -> PASS.
- Cold reopen -> same root, event-bound source, eligibility and encounter chain.
- Foreign-root source -> refused by the supported S47 qualification seam.

## Next owner action

An independent qualified reviewer may rerun the same harness at the same pins.
The receiving lead may cite `evidence/harness_run.json` as engineering evidence.
No PROGRAMMA promotion follows automatically from this delta.
