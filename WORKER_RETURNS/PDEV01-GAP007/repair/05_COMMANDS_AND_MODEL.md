# GAP-007 final repair — commands, model metadata, guard

**Repair base:** `023534c7f3f7fc5411ed52676490a1a0f70cd864`
**Review read:** `bff80e2a7` (`PDEV01 GAP007 cold recheck: record artifact commit`)
**Author model metadata:** `opencode-go/deepseek-v4.1-flash#max` from the
existing controller job; no model switch was made.

## Stable replay after the guard

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007
ROOT=WORKER_RETURNS/PDEV01-GAP007/repair
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$ROOT/replay_repair.py" > "$ROOT/replay_after_guard_1.json"
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B "$ROOT/replay_repair.py" > "$ROOT/replay_after_guard_2.json"
cmp -s "$ROOT/actual_trace.json" "$ROOT/replay_after_guard_1.json"
cmp -s "$ROOT/replay_after_guard_1.json" "$ROOT/replay_after_guard_2.json"
```

Observed: both comparisons exact; the transient outputs and committed
`actual_trace.json` all had SHA-256
`bba0de8231ea50b46c1f5d5f73c434d64af2d9bcd9c5ef610876e7955b1256ab`.
The transient outputs were removed; the committed cold receipts are
`cold_replay_1.json` and `cold_replay_2.json`, both equal to `actual_trace.json`.

## Tests

```sh
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest "$ROOT/test_repair.py" -q -o addopts='' \
  -p no:cacheprovider --junitxml="$ROOT/test_repair_junit.xml"
```

Observed: **9 passed** in 47.81s. `test_08` creates a changed copy of the frozen
SAV in a temporary path, invokes:

```sh
python3 "$ROOT/replay_repair.py" --source <changed-copy>
```

and requires a nonzero exit, empty stdout, and stderr containing
`FROZEN_SOURCE_SHA256_MISMATCH`, the expected SHA, and the changed-file SHA.
No changed bytes are committed.

## Receipt reconciliation

`04_RECEIPT_RECONCILIATION.json` records:

- `actual_trace.json` = `01_ACTUAL_RECEIPT.json` = `cold_replay_1.json` =
  `cold_replay_2.json`, all SHA-256
  `bba0de8231ea50b46c1f5d5f73c434d64af2d9bcd9c5ef610876e7955b1256ab`
- source `5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f`
- release `64cf774b408686394c8caf9969f442b518e365d04c924bafefb6204239c9bf03`
- manifest `6fd0f47cde582407a6afb6f21d3fb5c7d001cc14b03f688f34cce87770eef8ab`
- I05 compilation `78568e5e47b086d9f537a6359b8e729ab2d8e42305981075d21aa613e0b31dc9`
- 210 executed / 210 `SUPPORTED`; 630 typed refusals; 840 total.

## Scope

No original SAV/DTA, source rights, new science, production edit, compiler
replacement, CI, merge, authority expansion or downstream wake. Other workers
and their worktrees were not modified. Distinct independent review remains
required.
