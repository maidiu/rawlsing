# PDEV-01 N10W focused clock recheck commands

Root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review`

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 \
  WORKER_RETURNS/PDEV01-N10W-INDEPENDENT-REVIEW/clock-recheck/run_recheck.py
```

The recheck reuses the actual J42 receipts independently built and committed in
review `e79be4a3d`, verifies the pinned W41 artifact SHA, runs all 84 guarded
views and both cold receipt sets, and executes paired clock/snapshot/view
mutations with P41 rehash.

Evidence: `evidence/recheck_evidence.json`, `SOURCE_PINS.json`, `logs/`.
