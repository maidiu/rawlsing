# Final F6 recheck — exact commands

Review root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6-review`

```sh
REV=WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/final-recheck
CAND=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6
SNAP=$(mktemp -d "${TMPDIR:-/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T}/pdev01-f6-final.XXXXXX")

git -C "$CAND" archive 22d6712090970597e0c161b9f12eaece84bda5c5 \
  WORKER_RETURNS/PDEV01-F6-COMPARISON | tar -x -C "$SNAP"

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest \
  "$SNAP/WORKER_RETURNS/PDEV01-F6-COMPARISON/replay/test_review_corrections.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$REV/logs/correction_seed0_junit.xml"

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python3 -B -m pytest \
  "$SNAP/WORKER_RETURNS/PDEV01-F6-COMPARISON/replay/test_review_corrections.py" \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml="$REV/logs/correction_seed1_junit.xml"

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B \
  "$REV/verify_final_recheck.py"
```

Observed correction tests:

- seed 0: `4 passed in 0.14s`
- seed 1: `4 passed in 0.13s`

The verification script checks the raw exception, diagnostic ownership,
unexecuted-effect fields, exact historical F6C bytes against `c1ebe091f`, the
checkout-root hash limit, and same-checkout seed0/seed1 comparison output.
