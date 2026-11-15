# SOROK P6 — history query-order / unpursued-detail proof

**RESULT: PASS.** Frozen P6 runtime `41b21babf72c4c8b0b4b012d3c8b7d7f6247791f`.

- **Branch:** `codex/sorok-p6-history-order-proof-20261107-r1`
- **Proof:** `WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py`
- **Environment:** `/private/tmp/rawlsing-oct28-p1r1/venv/bin/python`
- **Prior gaze proof preserved:** branch parent `a075232f56b55bcce138df755db20e77e3ec5f3c`.

## Command / result

```sh
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  WORKER_RETURNS/SOROK-P6-HISTORY-ORDER-PROOF-20261107-R1/test_history_order_proof.py
```

```text
.                                                                        [100%]
1 passed in 203.37s
exit status 0
```

## Method

One exact P6 state was created, snapshotted, and restored at the **same path**
for each trace. Starting world, actor, clock and ordinary P6 entry points were
therefore identical.

Traces:

1. `go living room -> look photo -> look sandals`
2. `go living room -> look sandals -> look photo`
3. `go living room -> view -> go workshop` (leave before pursuing close detail)

Objective history was read independently before and after both inspections
through `read_house`, and through P6 `view` for cold restore.

## Assertions observed

- Before inspection: stored history is `bench-installation`, `strap-repair`;
  `photo-exposure` exists in objective `facts` with offset `-4`, clock `244`,
  and dependency `["strap-repair"]`, but is absent from stored history.
- Both inspection orders add the same fixed `photo-exposure` fact. After both,
  stored history, objective facts, source/root/branch, object identities,
  dependency links and scene equal exactly.
- The first exposed close fact is order-specific; after both inspections the
  later exposed detail is stable. This is real action order, not a changed
  objective fact.
- Cold `view` after both preserves the same stored history, objective facts and
  roots.
- Leave trace: `photo-exposure` remains in objective facts but is not stored in
  history; ordinary visible objects remain `coaster`, `photo`, `sandals`; no
  forced `photo-exposure` reveal appears in `leave_view`. After leaving, stored
  history is only `bench-installation`, `strap-repair`.
- Clocks, actor episodes and ledger are recorded as real effects and are
  deliberately **not compared across order traces**. Both order traces reached
  clock `255` in this run, but equality is not asserted; the leave trace reached
  `250` and its different conduct/effect history is preserved.

The chronology worker's tamper rejection/restoration is a separate proof. This
proof specifically varies real inspection order and checks objective history
query invariance plus lawful non-pursuit.

## Scope

P6 only. Runtime, shared progress, protected state and PR #779 author files were
read-only. P5 #775 and P6 #779 remain unreceived candidates. Sourcefree only; no
native/scientific/human claim.
