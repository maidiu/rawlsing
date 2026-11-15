# SOROK P2 explicit interval continuation R1

Additive TEST_ONLY continuation over the accepted S45-S47 shipped product at
base `41bf45813fd0adeffd9b54e1306c2022abe96514`.

WAIT/ABSENCE alone are not activity. Continuation occurs only when the caller
explicitly supplies an interval input. The implementation calls the existing
`run_s45_s47.py interval` and `admit` commands, then observes the public
`S45Projection` continued opportunity/read view.

Observation never executes a user DO_HELP attempt and never increments the
encounter count. A user DO_HELP is a separate explicit operation (`do-help`) or
call to `explicit_do_help(...)`; it is never automatic.

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

Explicit user DO_HELP after observation:

```text
<return>/run_explicit_interval_flow.py --base-root <base> do-help \
  --state <state> --request WAIT
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
    explicit_do_help,
)
```

- `continue_after_request(state, request="WAIT", interval_input=None)` — held
  without interval input; otherwise interval + existing admit + public
  opportunity/read view. No automatic DO_HELP.
- `apply_explicit_interval(state, interval_input)` — existing `interval`
  command only.
- `admit_continuation(state, request="WAIT")` — existing `admit`, C9 public
  summary, public continued view/opportunity and cold continuity; observation
  only.
- `explicit_do_help(state, request="WAIT")` — explicit user DO_HELP operation;
  returns the projected result and encounter increment.

Observation results expose the redacted public summaries as `admission_status`
and `c9_public`. The reserved projection keys `admission` and `c9` are not
emitted at the top level; no raw readset, source hash, actor state or root hash
is added.

## Base closure

The base product/projection returns are used unchanged from commit
`41bf45813fd0adeffd9b54e1306c2022abe96514`. For checkout-local runs, stage them
under `.local-logs/p2-explicit-interval-flow/base` and pass that path with
`--base-root` or `SOROK_P2_BASE_ROOT`.

## Boundary

This is not general autonomous absence life, not native psychology, and not a
new actor/motive/B-state producer. It does not edit inherited product, vendor,
projection, PROGRAMMA working files or protected branches.
