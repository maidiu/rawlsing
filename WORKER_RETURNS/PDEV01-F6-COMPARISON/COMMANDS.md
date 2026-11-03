# PDEV-01 F6 comparison — exact execution calls

Run root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6`
Evidence root: `WORKER_RETURNS/PDEV01-F6-COMPARISON/`

## Source staging (read-only Git blobs)

```sh
git archive 7d7ed1cb0 WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1 \
  | tar -x -C WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/F6P
git archive 912467aa WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1 \
  | tar -x -C WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/F6P-reviewed
git cat-file -p 55e567e4d0780c251bf949268d3d477abdc76a9b \
  > WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py
git show c1ebe091f:WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs/wp2_consumer_substitution_receipt.json \
  > WORKER_RETURNS/PDEV01-F6-COMPARISON/evidence/f6c-wp2-substitution-receipt.json
```

## Exact F6P tests

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/F6P/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1
PYTHONHASHSEED=0 python3 -m pytest tests -q -o addopts=''
PYTHONHASHSEED=1 python3 -m pytest tests -q -o addopts=''
# 26 passed each at implementation 7d7ed1cb0

cd WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/F6P-reviewed/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1
PYTHONHASHSEED=0 python3 -m pytest tests -q -o addopts=''
PYTHONHASHSEED=1 python3 -m pytest tests -q -o addopts=''
# 32 passed each at publication 912467aa / reviewed target
```

## Independent reviewer tests (2e00c8c9e)

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/reviewer_root
PYTHONHASHSEED=0 python3 -m pytest evidence/court_b/test_court_b_f6p_independent.py -q -o addopts=''
PYTHONHASHSEED=1 python3 -m pytest evidence/court_b/test_court_b_f6p_independent.py -q -o addopts=''
# 8 passed each
```

## Actual F6P output and current-receiver shape check

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON
PYTHONHASHSEED=0 python3 run_comparison.py
PYTHONHASHSEED=1 python3 run_comparison.py
cmp -s evidence/run-comparison.seed0.json evidence/run-comparison.seed1.json
# identical
```

The executable check builds the actual F6M bundle through the staged F6P
consumer. For W2 it yields `PARTIAL_IDENTIFICATION`, uncovered `1/4`, and no
point. It then applies the exact current WP2 sidecar expression:

```python
{
  "bundle_hash": value["native_bundle"]["content_hash"],
  "conditional": value["native_conditional_consumer"],
}
```

F6P supplies `F6P_PARTIAL_BOUND_EVIDENCE@1`, not F6M's `native_bundle` sidecar;
the first mismatch is `KeyError: 'native_bundle'`, recorded as
`F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR`. There is no `NONPARENT_OPTIONS`
read and no F6M→E04 join.

## Five historical-function tests

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON
PYTHONHASHSEED=0 python3 -m pytest replay/test_historical_function_tests.py -q -o addopts='' \
  --junitxml=logs/five_tests_junit.xml
# 5 passed
```
