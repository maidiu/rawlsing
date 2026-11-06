# SOROK P2 explicit interval continuation R1

Additive TEST_ONLY continuation over the accepted S45-S47 shipped product at
base `41bf45813fd0adeffd9b54e1306c2022abe96514`.

WAIT/ABSENCE alone are not activity. Continuation occurs only when the caller
explicitly supplies an interval input. The implementation calls the existing
`run_s45_s47.py interval` and `admit` commands, then consumes the public
`S45Projection` encounter/DO_HELP surface.

## Run

```text
python3 WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1/run_explicit_interval_flow.py \
  --base-root <candidate-root-containing-WORKER_RETURNS> \
  continue --state <state> --request WAIT
```

The command above returns a typed WAIT hold and does not advance. Explicit
continuation:

```text
python3 WORKER_RETURNS/SOROK-P2-EXPLICIT-INTERVAL-FLOW-20261105-R1/run_explicit_interval_flow.py \
  --base-root <candidate-root-containing-WORKER_RETURNS> \
  continue --state <state> --request WAIT --mode ACTUAL --span 4
```

`--mode` is required for any advance and accepts the existing S46 modes:
`ACTUAL`, `SCHEDULED_ONLY`, `DECLINED`, `CONSTRAINED`, `BLOCKED`, `UNKNOWN`.
No default mode is selected and no activity is inferred from WAIT or ABSENCE.

Input may also be supplied as JSON:

```text
--interval-json '{"schema":"SOROK_P2_EXPLICIT_INTERVAL_INPUT@1","mode":"SCHEDULED_ONLY","span":4}'
```

## Callable API

```python
from p2_explicit_interval_flow import (
    apply_explicit_interval,
    admit_continuation,
    continue_after_request,
)
```

- `continue_after_request(state, request="WAIT", interval_input=None)` — held
  without interval input; otherwise interval + existing admit + public
  encounter/DO_HELP.
- `apply_explicit_interval(state, interval_input)` — existing `interval`
  command only.
- `admit_continuation(state, request="WAIT")` — existing `admit`, C9 public
  summary, public continued view/DO_HELP and cold continuity.

## Base closure

The base product/projection returns are used unchanged from commit
`41bf45813fd0adeffd9b54e1306c2022abe96514`. For checkout-local runs, stage them
under `.local-logs/p2-explicit-interval-flow/base` and pass that path with
`--base-root` or `SOROK_P2_BASE_ROOT`.

## Boundary

This is not general autonomous absence life, not native psychology, and not a
new actor/motive/B-state producer. It does not edit inherited product, vendor,
projection, PROGRAMMA working files or protected branches.
