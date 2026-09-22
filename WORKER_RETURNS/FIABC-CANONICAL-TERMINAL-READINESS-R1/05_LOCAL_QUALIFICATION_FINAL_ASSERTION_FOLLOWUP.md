# Local Qualification Final-Assertion Follow-up

User-reported local qualification on worker head:

`c0fa63e0817bca56566049e86bf192934964868a`

reported:

```text
163 passed, 28 subtests passed in 9.49s
```

The pytest court was fully green. The qualification then stopped in the final static cross-lane assertion with:

```text
AttributeError: module 'rawlsing_next.pre553_independent_parity_oracle'
has no attribute 'WVS7_LOCK2_REPLAY'
```

The required green terminal was therefore correctly not emitted. The user reported that no Candidate A/B/C execution and no measured P2X execution occurred.

## Static diagnosis

This is a qualification-script symbol typo only.

The authoritative oracle module exports:

`WVS7_LOCK2_REPLAY_IDENTITY`

with exact successor replay identity:

`9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a`

The live terminal-control module independently exports:

`WVS7_SUCCESSOR_LOCK2_REPLAY`

with the same exact value.

The source-free qualification script incorrectly referenced:

`oracle.WVS7_LOCK2_REPLAY`

which does not exist.

## Repair

Changed only the final static assertion in:

`WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh`

from:

```python
assert oracle.WVS7_LOCK2_REPLAY==WVS7_SUCCESSOR_LOCK2_REPLAY
```

to:

```python
assert oracle.WVS7_LOCK2_REPLAY_IDENTITY==WVS7_SUCCESSOR_LOCK2_REPLAY
```

No production Python module, oracle identity, WVS successor identity, telemetry law, candidate implementation, workload law, or measured-run behavior changed.

## Runtime status

No follow-up runtime qualification was executed by this Browser/GitHub worker.

A fresh local rerun is required:

```bash
bash WORKER_RETURNS/CANONICAL-REINTEGRATION-FIABC-R1/01_SOURCE_FREE_LOCAL_QUALIFICATION.sh
```
