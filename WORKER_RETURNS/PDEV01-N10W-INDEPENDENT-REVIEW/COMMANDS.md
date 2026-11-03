# PDEV-01 N10W independent review commands

Root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review`

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join-review
PYTHONHASHSEED=0 python3 WORKER_RETURNS/PDEV01-N10W-INDEPENDENT-REVIEW/run_review.py
```

The script performs two independent actual J42 builds from pinned commit
`f53cb0d2bce52640268c844c398bbd8007d28edc` and packet
`WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1`
using `runtime/j42_build.py`, then runs the candidate guard for all 84 views and
the five rehashed mutations, stale-hash, missing-parent and clock tests.

Evidence files:

- `evidence/J42_RECEIPTS_actual_1.json` / `_2.json`
- `evidence/review_evidence.json`
- `logs/j42_build_{1,2}.stdout.log`
- `logs/run_review.stdout.log`
- `SOURCE_PINS.json`
