# PDEV-01 N10W same-lineage review commands

Root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review`

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 \
  WORKER_RETURNS/PDEV01-N10W-JOIN-INDEPENDENT-SAME-LINEAGE/run_same_lineage_review.py
```

The review reuses the independently built actual J42 receipts from
`e79be4a3d`, executes the c75b identity guard across all 84 views and both cold
receipts, runs R05 mismatch/provider/restore controls, and inspects the exact
D2P3 GSS/NCA producer trace. D2P3 is not fed to N10W.

Evidence: `evidence/same_lineage_review.json`,
`evidence/ENVIRONMENT_PASSPORT.json`, `logs/`, `SOURCE_PINS.json`.
