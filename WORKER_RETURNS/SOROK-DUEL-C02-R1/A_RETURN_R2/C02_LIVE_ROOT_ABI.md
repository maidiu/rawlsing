# C02 live-root parent background entry ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; normal P4/P6 live-root composition. Not independent acceptance or protected adoption.
**Implementation SHA:** `9ac1ac71cdbc8dd2c832b2980b501b4031e163e8`.
**Composition start:** `ea1f8d75b894c28d8a7bdb2d667761af2b67e310`.
**B frozen return:** `4d93685df4c5abdfbd09f44510a24a41c850b6a8`; B implementation `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf`.
**Contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## Entry

```text
run_p4.run_parent_operation(state, *, operation, request)
run_p6.parent_background_operation(state, *, operation, request)  # internal seam
```

`operation` is one of:

```text
period-establish       historical_period.establish_period_plan (B02 API, not edited)
parent-register        supporting_actor.register_supporting_actor
parent-establish       parent_activity.establish_parent_material
parent-circumstance    parent_activity.commit_parent_circumstances
parent-activity        parent_activity.record_parent_activity
```

The entry is a closed operation enum, not an arbitrary callback. It checks the ordinary P4 foreground boundary before any write, records a durable `pending` fail-stop marker, executes the existing owner API, and records the actual after snapshot and owner receipt through the existing `run_p4.record_activity` protocol (`ledger.activity_turns`, `last_boundary`, `foreground_witness`).

## Order of operations

```text
foreground_lock(state)
  -> load existing p4_receipts.json
  -> refuse if ledger.pending is set
  -> open_owner(state/actual-p2)
  -> check_source(owner)
  -> check_boundary(owner, ledger)                       # before any parent/B02 write
  -> before = owner.snapshot()
  -> ledger.pending = {kind: parent_background, operation, request}; save
  -> existing parent/world/B02 owner operation
  -> after = owner.snapshot()
  -> if after == before: clear pending, save, no activity turn
     else: clear pending, record_activity(owner, ledger_file, ledger, before, result)
  -> close owner
```

No user turn is created. No parent material or activity is placed on the user-visible P6 scene surface. `record_activity` is the existing independent-activity protocol; there is no second ledger, scheduler, owner, callback, or snapshot-anchor rewrite.

## Failure semantics

- A clean refusal before mutation clears `pending` and raises; no activity turn.
- A mutation followed by an exception leaves `pending` set; the next normal command refuses `P4_PENDING_OPERATION_REQUIRES_RECONCILIATION`. This is fail-stop, not full crash reconciliation. E03 owns composite recovery.
- A root mutated by direct/unrecorded C12/P2 writes still fails `check_boundary` with `P4_COLD_STATE_MISMATCH`; the entry cannot re-bless it.
- Repeating a successful parent operation returns the owner-level `UNCHANGED`/`REPLAY` result with no new activity turn; no duplicate world/perception/episode effect.
- A successful parent registration/material/activity is followed by ordinary P6 `view` and an ordinary lawful user `say` after cold reopen, because the last P4 boundary now matches the actual after snapshot.

## Evidence boundary

The normal live-root test creates a fresh P6 root, uses the entry from B02 plan establishment through parent registration/establishment/activity, then runs ordinary `run_p6.experience` view and say. The parent activity changes the P2 world and C12 receipt history but leaves the P3 psychology head unchanged, adds no Nadia percept, and does not expose the parent private motive or activity summary on the user surface.

## Explicit limits

- Full C02 dated C02 proof remains held pending an exact incremental B02 current-period/two-period API; see the B02 ingress ABI.
- C03 decision/utterance and C04 qualified uptake remain future.
- Full SIGKILL/crash reconciliation is not proved; only pending fail-stop and no-duplicate retry semantics are proved.
- No native/C4/ADP-015/CAN/ADP/Pyat/actor/human/source right or protected merge.
