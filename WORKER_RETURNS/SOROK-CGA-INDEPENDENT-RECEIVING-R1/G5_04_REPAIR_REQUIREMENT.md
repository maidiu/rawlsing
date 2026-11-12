# Minimal repair acceptance — CGA-G5-D1

The following is the minimum expected behavior for the repaired helper. It is not applied in this receiving branch.

## Defect

`WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py:136` `current_p3_actor_access`:

- accepts an old authentic `source_receipt`;
- trusts a caller-supplied `interval` that includes the old cue event;
- does not require the receipt’s own interval or operation identity to match the current operation.

## Reproduction that must pass after repair

`test_hostile_stale_receipt.py`:

```text
new -> approach (E1 at clock 248) -> wait 4 (clock 253)
current_p3_actor_access(session, {start:247,end:253},
                        packet={cues:[old.outward_cue]},
                        source_receipt=old_receipt) is False
```

## Required properties

1. A receipt from an earlier P4 operation cannot authorize a later interval.
2. The receipt must be bound to the current operation/request identity, not only to its event hash.
3. The receipt interval must be exactly the current interval, or the helper must independently derive the current interval from the receipt and reject a mismatch.
4. Existing valid `approach` current-receipt behavior must remain true.
5. The 37-test suite and the new hostile test must both pass at the repaired exact SHA.

Adding only `event.clock > interval.start` is insufficient: a caller can set `start` before the old event.
