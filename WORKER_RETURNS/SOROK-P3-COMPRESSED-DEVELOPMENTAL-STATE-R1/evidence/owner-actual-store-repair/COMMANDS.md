# Commands and observed results — owner actual-store repair

Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-recursion-reuse-r1`

Startup: `8cc2914b1089cfc113ae1737941bd2a9efde622b`

Branch: `agent/sorok-p3-owner-actual-store-repair-20261106-r1`

## Compile

```text
python3 -m py_compile \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py
```

Observed: success (no output).

## Full actual owner test command

```text
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
python3 -m pytest -q -rs \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  -p no:cacheprovider
```

Observed: `4 passed, 4 failed, 1 skipped in 16.75s`
(`TEST_LOG_ACTUAL.txt`).

The four failures are three owner positives plus the crash test, all before any
base effect at the returned store's `PLAN_AUTHORITY_OR_GRADE_MISSING` check.
The crash test now reaches store reservation; it does not yet reach the
intended kill boundary. This is a storage-ABI dependency, not a claim of green
owner integration.

## Actual same-root reopen probe

```text
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
python3 -m pytest -v -q \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_process_reopens_same_actual_p2_root \
  -p no:cacheprovider
```

Observed: `1 passed in 3.57s` (`ROOT_REOPEN_PROBE.txt`).

The subprocess child uses explicit repository-relative P3/engine/repo import
paths and `load_p2().open(...)` on the same existing actual-p2 directory. It
asserts the exact frozen root hash and initial P2 StateIdentity; the parent
reopens the same root and state. No root replacement or manufactured receipt.

## Store dependency status

`STORE_INPUT_DISPOSITION.json` records the actual returned store
`38f04ed627de40258724e006bf227a104bba9300` and 42 mechanical store tests
passing while actual owner positives fail the separate store ABI. The current
store code hash is:
`40b29d96c359de61fcb62937c08f7cdb73cd68b936247ef2e9219348119586a0`.

No store source was edited or bypassed in this repair.
