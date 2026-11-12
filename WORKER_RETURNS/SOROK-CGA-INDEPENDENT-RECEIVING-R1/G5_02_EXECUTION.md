# G5 execution record

## Exact source state

```text
tested checkout HEAD   9d3d8ae419998a3e13d88f58147756149e3dddb5
PR #976 head           37c5842e04892421c9ce74a39956c3cdcf57f0f5
merge base             37c5842e04892421c9ce74a39956c3cdcf57f0f5
review delta           two added files only
implementation diff    none
tracked worktree diff  empty during test run
```

The review branch is exactly PR #976 plus the independent receiver probe and its workflow. The implementation under test is therefore the PR head, not a rewritten branch.

## Full 37-test run

Command:

```bash
python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_receiver.py \
  WORKER_RETURNS/SOROK-CGA-AGENT-A-RELAY-R1/test_cue_issuer.py \
  WORKER_RETURNS/SOROK-CGA-CAUSAL-BRIDGE-R1/test_bridge.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1/test_response.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py
```

Exact output (`G5_EVIDENCE/37_tests.log`):

```text
.....................................                                    [100%]
37 passed in 2330.68s (0:38:50)
```

No failed attempt was dropped. The four pre-existing receiving probes are included, but they are not treated as the new G5 hostile variation.

## New hostile probe

Command:

```bash
python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-CGA-INDEPENDENT-RECEIVING-R1/test_hostile_stale_receipt.py
```

Exact result: `1 failed in 12.72s`; assertion `assert True is False` at test line 33. Full traceback is in `G5_EVIDENCE/hostile_stale_receipt.log`.

## Environment

See `G5_EVIDENCE/ENVIRONMENT.txt`. macOS 13.7.8, Python 3.11.3, pytest 9.1.1, local x86_64 host.

## Interpretation

The 37-test suite passes the existing P3/P4/P6 and A/B regression surface. The new probe fails at the exported actor-access helper, not at the ordinary P6 CLI call. That distinction is recorded in the verdict: the scoped P6 path remains green, but the helper is not safe for general integration until it binds the receipt to the current operation.
