# Execution record

## Source

- Base implementation: `37c5842e04892421c9ce74a39956c3cdcf57f0f5`.
- Tested: working tree containing only the `situated.py` D1 repair and the two regression tests.
- Exact fix diff: `evidence/DIFF.patch`.
- No protected owner or receiver evidence was modified.

## Full 37-test suite

The four independent receiver probes were copied read-only from the frozen G5 evidence (`c597024`) into this corrective worktree for local verification; the receiver branch itself was not modified. The other five files are the PR #976 author tests.

```bash
python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-G5-D1-REPAIR-R1/test_receiver.py \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

Result: `37 passed in 2422.84s`, exit 0. Log: `evidence/37_tests_fixed.log`.

## D1 regression

```bash
python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-G5-D1-REPAIR-R1/test_g5_stale_receipt.py \
  WORKER_RETURNS/SOROK-CGA-G5-D1-REPAIR-R1/test_receipt_currentness.py
```

Result: `2 passed in 27.73s`, exit 0. Log: `evidence/repair_tests.log`.

`test_g5_stale_receipt.py` is a verbatim local copy of the committed G5 probe. `test_receiver.py` was used only as a temporary verification copy and is not committed in this return.

## Environment

macOS 13.7.8 x86_64, Python 3.11.3, pytest 9.1.1. See `evidence/ENVIRONMENT.txt`.

## Not run / not used

- No GitHub Actions.
- No protected PRE-MAIN merge.
- No provider/model call.
- No native/actor/human authority.
