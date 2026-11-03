# Independent review — exact commands

Review root:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6-review`

`REV=WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW`

## Independent replay

The reviewer did not invoke the candidate's `run_comparison.py`, because that
script writes the candidate's evidence file. The reviewer script imports the
same staged F6P/F6M code and performs the same structural checks.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B \
  WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/replay_f6_reviewer.py
```

Outputs:
- `evidence/replay_f6_review.json`
- `evidence/wp2_boundary_review.json`
- `evidence/scope_scan_review.json`
- `logs/replay.stdout.log`

## Reviewer tests

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest \
  WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/test_review.py \
  -q -o addopts='' -p no:cacheprovider \
  --junitxml=WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/logs/review_tests_junit.xml
```

Observed: `7 passed`.

## Candidate F6P tests (read-only; bytecode/cache disabled)

```sh
C=WORKER_RETURNS/PDEV01-F6-COMPARISON
IMPL="$C/stage/F6P/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
PUB="$C/stage/F6P-reviewed/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
REVW="$C/stage/reviewer_root"

cd "$IMPL"
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest tests -q -o addopts='' -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python3 -B -m pytest tests -q -o addopts='' -p no:cacheprovider

cd "$PUB"
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest tests -q -o addopts='' -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python3 -B -m pytest tests -q -o addopts='' -p no:cacheprovider

cd "$REVW"
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest evidence/court_b/test_court_b_f6p_independent.py -q -o addopts='' -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=1 python3 -B -m pytest evidence/court_b/test_court_b_f6p_independent.py -q -o addopts='' -p no:cacheprovider
```

Observed: implementation `26 passed` on both seeds; publication `32 passed` on
both seeds; independent reviewer `8 passed` on both seeds.

## Candidate five historical tests

```sh
cd WORKER_RETURNS/PDEV01-F6-COMPARISON
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m pytest \
  replay/test_historical_function_tests.py -q -o addopts='' \
  -p no:cacheprovider \
  --junitxml=../PDEV01-F6-INDEPENDENT-REVIEW/logs/five_tests_review_junit.xml
```

Observed: `5 passed`.

## Pins and exact-tree scan

```sh
git rev-parse HEAD
git show --format= --name-only aa18b6b8547c954d844bb0dcf94f70e2e14f15b0
git hash-object WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py
shasum -a 256 WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py
git grep -n -I F6P_PARTIAL_BOUND_EVIDENCE aa18b6b8547c954d844bb0dcf94f70e2e14f15b0 --
git grep -n -I consume_f6m_evidence aa18b6b8547c954d844bb0dcf94f70e2e14f15b0 --
git grep -n -I uncovered_target_mass aa18b6b8547c954d844bb0dcf94f70e2e14f15b0 --
git grep -n -I f6_sidecars aa18b6b8547c954d844bb0dcf94f70e2e14f15b0 --
git grep -n -I native_bundle aa18b6b8547c954d844bb0dcf94f70e2e14f15b0 --
git ls-tree -r --name-only aa18b6b8547c954d844bb0dcf94f70e2e14f15b0 | grep 'wp2.py'
git show aa18b6b8547c954d844bb0dcf94f70e2e14f15b0:rawlsing_next/pre553_n9_n10w_progressive_candidate.py
git show aa18b6b8547c954d844bb0dcf94f70e2e14f15b0:rawlsing_next/pre553_source_relations.py
```

## F6C historical output check

The copied F6C receipt does not contain the output bodies; the reviewer read the
pinned historical outputs directly:

```sh
git show c1ebe091fa2bd12b254e5599cf37975fe438d462:WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs/wp2_sub_B.json
git show c1ebe091fa2bd12b254e5599cf37975fe438d462:WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs/wp2_sub_A.json
git show c1ebe091fa2bd12b254e5599cf37975fe438d462:WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs/wp2_sub_A0.json
```
