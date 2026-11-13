# CGA-G5-D1 finding and fix

## Finding

The committed G5 evidence at `review/sorok-cga-independent-g5-receiving-20261112-r1` (`c597024bb250f014f9a616006f10172ed53e4357`) demonstrates that `situated.current_p3_actor_access` accepts an old authentic `source_receipt` when the caller supplies a broader interval containing the old cue. The helper checked cue identity, performed-event identity, actor, sensory rederivation and conduct parent, but not receipt currentness.

Failure reproduced before repair:

```text
assert current_p3_actor_access(..., source_receipt=old) is False
AssertionError: assert True is False
```

## Fix

`WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py` adds:

```python
source_interval = (
    source_receipt.get("interval") if isinstance(source_receipt, dict) else None
)
receipt_current = (
    isinstance(source_interval, dict)
    and source_interval == interval
    and interval.get("end") == world.clock
)
```

The outward-cue branch now requires `receipt_current`.

## Why both conditions

- Exact interval equality rejects a broadened caller interval around an old receipt.
- `interval["end"] == world.clock` rejects an old receipt with its unchanged old interval.
- The normal P6 path passes the current receipt and its own interval, so both conditions hold.
- A current receipt remains accepted; the existing current-cue tests still pass.

## Scope

Only D1 is changed. P3/P4/P5/P6 owners, the P3/world readset separation, actor-access negative cases, source custody and scientific holds are unchanged. The pre-existing direct-caller trust boundary (a caller with raw access can forge a receipt) remains; this repair does not claim authenticated receipt provenance.
