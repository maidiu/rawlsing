# Exact commands

Run root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007`

```sh
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B WORKER_RETURNS/PDEV01-GAP007/occurrence-binding/replay_occurrence.py

PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 -B -m pytest \
  WORKER_RETURNS/PDEV01-GAP007/occurrence-binding/test_occurrence.py \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PDEV01-GAP007/occurrence-binding/test_occurrence_junit.xml
```

Observed `test_occurrence.py`: **3 passed**.

The attempt uses the existing P1 constructor and test input, the accepted
GAP007 `repair/replay_repair.py` frozen-source guard and C11 build path, and the
existing R03 `OccurrenceKey` type. It does not execute P1 conditional/joint
operations.
