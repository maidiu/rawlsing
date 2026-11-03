# PDEV-01 F6 comparison — exact execution calls

Run root: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6`
Evidence root: `WORKER_RETURNS/PDEV01-F6-COMPARISON/`
Corrects independent review `23edffb32141c133c8b45b723bb23f092928115c`.

## Source staging (read-only Git blobs)

```sh
git archive 7d7ed1cb0 WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1 \
  | tar -x -C WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/F6P
git archive 912467aa WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1 \
  | tar -x -C WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/F6P-reviewed
git cat-file -p 55e567e4d0780c251bf949268d3d477abdc76a9b \
  > WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py
git show c1ebe091f:WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs/wp2_consumer_substitution_receipt.json \
  > WORKER_RETURNS/PDEV01-F6-COMPARISON/evidence/f6c/wp2_consumer_substitution_receipt.json
for k in A A0 B; do
  git show c1ebe091f:WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs/wp2_sub_${k}.json \
    > WORKER_RETURNS/PDEV01-F6-COMPARISON/evidence/f6c/wp2_sub_${k}.json
done
```

The copied substitution receipt is not self-contained; the three exact
`wp2_sub_{A,A0,B}.json` outputs are embedded separately and hashed in
`evidence/f6c/F6C_OUTPUT_MANIFEST.json`.

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

## Actual F6P output and exact WP2 expression

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON
PYTHONHASHSEED=0 python3 run_comparison.py
PYTHONHASHSEED=1 python3 run_comparison.py
cmp -s evidence/run-comparison.seed0.json evidence/run-comparison.seed1.json
# identical within this checkout root
```

The executable check builds the actual F6M bundle through the staged F6P
consumer. For W2 it yields `PARTIAL_IDENTIFICATION`, uncovered `1/4`, and no
point. It applies only the exact WP2 sidecar expression:

```python
{"bundle_hash": value["native_bundle"]["content_hash"],
 "conditional": value["native_conditional_consumer"]}
```

The observed receiver exception is raw:

```text
KeyError: 'native_bundle'
args = ("native_bundle",)
```

The string `COMPARISON_LOCAL_BOUNDARY_SHAPE_DIFFERENCE__NOT_EMITTED_BY_F6P_OR_WP2`
is authored by the comparison harness. It is not emitted by F6P or WP2. WP2
`product()` was not executed and no receiver effect is claimed.

## Five historical-function and review-correction tests

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON
PYTHONHASHSEED=0 python3 -m pytest replay/test_historical_function_tests.py replay/test_review_corrections.py -q \
  -o addopts='' --junitxml=logs/review_correction_and_five_tests_junit.xml
# 9 passed
```
