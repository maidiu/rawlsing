# COMMANDS AND EVIDENCE — W03/W04 economics methodology review

All local work was performed with:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
```

Read-only author/baseline inspection used `git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1 ...` or read-only `cp` into this review lease. No command wrote to the author, completion, HQ, protected, existing-test, or peer worktrees.

The review lease is:

```text
WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics/
```

## 1. Exact refs and contract source

```text
git rev-parse HEAD
git rev-parse --abbrev-ref HEAD
git rev-parse 46b7325637e68f78ccc7487d4b1abc7009c5ac0b
git rev-parse 4f3413fc5c37b589be3412f826bf8f68ee617d4a
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1 rev-parse HEAD
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-completion-r1 rev-parse HEAD
git show 5a891a311c70f4cb8c09864008b33405362f7c7c:WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv
git rev-parse 5a891a311c70f4cb8c09864008b33405362f7c7c:WORKER_COMMISSIONS/PYAT_W03_W04_MCR_COMPLETION_R1/REQUIRED_OBLIGATIONS.tsv
```

Recorded in `EVIDENCE/REFS_AT_REVIEW.txt`, `EVIDENCE/source_5a891a31_rev.txt`, `EVIDENCE/source_5a891a31_obligations_blob.txt`, and `EVIDENCE/REQUIRED_OBLIGATIONS.tsv` (sha256 in `EVIDENCE/REQUIRED_OBLIGATIONS.sha256`).

The TSV enumerated exactly 12 unique IDs:

```text
W03-PREVIOUS-CAPITAL
W03-COLD-HIGHWATER
W03-SELECTED-CELLS-CANON
W03-SEMANTIC-TOPOLOGY
W03-FIRST-CONSUMERS
W04-COLD-PERSIST-REOPEN
W04-GOVERNED-DEFAULT
W04-AUTHORITY-INVALIDATION
W04-ATOMIC-LIFECYCLE
W34-RESOURCE-ECONOMY
W34-PRODUCT-BOUNDARIES
W34-REPRODUCIBLE-RETURN
```

## 2. Bench draft snapshot (uncommitted)

```text
B=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1
L=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics
cp "$B/rawlsing_next/bench_w03_w04_physical.py" "$L/BENCH_DRAFT_SNAPSHOT/bench_w03_w04_physical.py"
cp "$B/rawlsing_next/tests/test_bench_w03_w04_physical.py" "$L/BENCH_DRAFT_SNAPSHOT/test_bench_w03_w04_physical.py"
cp "$B/.github/workflows/pyat-w03-w04-physical-economy.yml" "$L/BENCH_DRAFT_SNAPSHOT/pyat-w03-w04-physical-economy.yml"
git -C "$B" diff -- .github/workflows/pyat-w03-w04-physical-economy.yml > "$L/BENCH_DRAFT_SNAPSHOT/workflow.diff"
git -C "$B" status --porcelain=v1 > "$L/BENCH_DRAFT_SNAPSHOT/bench_status.txt"
git -C "$B" log --oneline -5 > "$L/BENCH_DRAFT_SNAPSHOT/bench_log.txt"
shasum -a 256 "$L/BENCH_DRAFT_SNAPSHOT/bench_w03_w04_physical.py" \
              "$L/BENCH_DRAFT_SNAPSHOT/test_bench_w03_w04_physical.py" \
              "$L/BENCH_DRAFT_SNAPSHOT/pyat-w03-w04-physical-economy.yml" \
              "$L/BENCH_DRAFT_SNAPSHOT/workflow.diff" > "$L/BENCH_DRAFT_SNAPSHOT/SHA256SUMS.txt"
```

Live draft head at first read: `1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc`.
Live author head at the later read-consistency check: `c44cf09fb9ca5cbc235763d8bd5df9b0074de289`.
The c44 exact committed bench/test/workflow snapshot is in `BENCH_LIVE_C44_SNAPSHOT/`; the earlier uncommitted snapshot is in `BENCH_DRAFT_SNAPSHOT/`. The bench implementation hash is unchanged (`b00cf324...`); the c44 test added one cells-and-hash case (`01eb49d3...`).

Snapshot sha256:

```text
b00cf3245ac4305ed527b38f9e899d2dc3c0edcc6410aeaae084aaaaecc8eb37  bench_w03_w04_physical.py
dc9385fed4d057a8e877b7fa90493a63157e22ae80aef084d892fbe8bcdf7b49  test_bench_w03_w04_physical.py
a277f84b374ae211a2fc69afaceb293f6d958b00a94c8a28f6faa32f262c47e2  pyat-w03-w04-physical-economy.yml
a981c7639d21b2978d091265cbdd341fb83d83d7ae8395fd8685b1d600230353  workflow.diff
```

Read-consistency check at first read: live and snapshot files were byte-identical (`cmp` returned 0 for all three files). The live branch later advanced to c44cf09f; the exact c44 files are snapshotted with:

```text
B=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1
L=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics
S="$L/BENCH_LIVE_C44_SNAPSHOT"
git -C "$B" show c44cf09fb9ca5cbc235763d8bd5df9b0074de289:rawlsing_next/bench_w03_w04_physical.py > "$S/bench_w03_w04_physical.py"
git -C "$B" show c44cf09fb9ca5cbc235763d8bd5df9b0074de289:rawlsing_next/tests/test_bench_w03_w04_physical.py > "$S/test_bench_w03_w04_physical.py"
git -C "$B" show c44cf09fb9ca5cbc235763d8bd5df9b0074de289:.github/workflows/pyat-w03-w04-physical-economy.yml > "$S/pyat-w03-w04-physical-economy.yml"
git -C "$B" show --stat --oneline c44cf09fb9ca5cbc235763d8bd5df9b0074de289 > "$S/COMMIT_STAT.txt"
shasum -a 256 "$S"/bench_w03_w04_physical.py "$S"/test_bench_w03_w04_physical.py "$S"/pyat-w03-w04-physical-economy.yml > "$S/SHA256SUMS.txt"
```

The c44 and earlier snapshots are point-in-time `UNCOMMITTED_DRAFT_AT_READ` / `LIVE_AUTHOR_COMMIT_NOT_FINAL` evidence only; neither is a final same-SHA candidate.

## 3. Author partial metrics snapshot (uncommitted)

```text
B=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1
L=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/economics
cp -R "$B/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench" "$L/AUTHOR_PARTIAL_METRICS_SNAPSHOT/bench"
find "$L/AUTHOR_PARTIAL_METRICS_SNAPSHOT/bench" -type f -print0 | sort -z | xargs -0 shasum -a 256 > "$L/AUTHOR_PARTIAL_METRICS_SNAPSHOT/SHA256SUMS.txt"
```

These were author partial measurements, explicitly marked `UNCOMMITTED_DRAFT_AT_READ` in `AUTHOR_PARTIAL_METRICS_SNAPSHOT/MANIFEST.md`; the live author lane later committed them in c44cf09f. They are not independent evidence, not final, and not whole acceptance.

Relevant author partial facts read from the snapshot:

- `00_RETURN.md`: author status `INCOMPLETE`.
- `02_resource_economy.md`: 100k narrow current `46b73256` 777.53 s / 5,923,426,304 B vs protected `4f3413fc` 997.04 s / 5,240,467,456 B; RSS ratio 1.1303 (+13.0% regression); target >=15% improvement not met; `cap_enforced: false` in the proof.
- `proof_02_resource_comparison.json`: 100k narrow `status: CURRENT_46b_RSS_REGRESSION_VS_PROTECTED__NO_PASS`, `target_met: false`; 1000-row matrix used one process per section; 100k wide/repeat not run.
- Because the `cold` scenario persists, this author 100k cold RSS is cache-inclusive; it is not an isolated W03 I02-to-first-I03 peak.

## 4. Focused test run

A temporary import-only shim was created in this lease so the snapshot could be imported as `rawlsing_next.bench_w03_w04_physical` over the review-head package. It was removed after the runs. Logs are retained at `SMALL_PROBE/bench_pytest.log` (earlier 1b0c8dc4 snapshot) and `SMALL_PROBE/bench_pytest_c44.log` (c44).

The c44 test command shape was:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
TMPDIR="$L/TMP" PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$L/C44_TEST_SHIM" \
python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  "$L/C44_TEST_SHIM/test_bench_w03_w04_physical.py"
```

The test shim contained `rawlsing_next/__init__.py` setting its `__path__` to the review-head package plus the shim directory, and an exact copy of the snapshotted c44 bench/test. It did not modify the review-head package.

Observed results:

```text
earlier 1b0c8dc4 snapshot: 6 passed in 10.16s
live c44 committed bench: 7 passed in 9.91s
```

The c44 test has 7 collected cases (3 parametrized profile cases plus 4 functions); the earlier snapshot had 6. The additional c44 test is a cells-and-hash actual-consumer test, not a baseline/cap/stage/threshold fix. The author's larger `50 passed` selected-test claim was not independently run; it is not the full 43-case/12-ID acceptance.

## 5. Small bounded probes (not 100k acceptance)

All probes used the exact snapshot bench file and sourcefree synthetic fixtures. They did not read original respondents/source/SAV/DTA/DB and did not run a heavy benchmark. The candidate probes used the review worktree at `16fd5f7b`, not PR895 `46b73256`; they are method probes only, not exact-PR895 performance evidence. The author's separate 100k 46b partial is cited as an author partial, not reproduced here.

Candidate cold 16:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R" \
python3 "$L/BENCH_DRAFT_SNAPSHOT/bench_w03_w04_physical.py" \
  --scenario cold --profiles narrow --rows 16 --repetitions 1 \
  --source-root "$R" --root "$P/candidate_cold_cache" \
  --jsonpath "$P/candidate_cold_16.json"
```

Protected 4f3413fc cold 16 (exact code extracted read-only to a temporary snapshot, then removed; commit and file hashes retained):

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$D" \
python3 "$L/BENCH_DRAFT_SNAPSHOT/bench_w03_w04_physical.py" \
  --scenario cold --profiles narrow --rows 16 --repetitions 1 \
  --source-root "$D" --root "$P/protected_cache" \
  --jsonpath "$P/protected_cold_16.json"
```

Candidate 24-row full matrix:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R" \
python3 "$L/BENCH_DRAFT_SNAPSHOT/bench_w03_w04_physical.py" \
  --scenario full-matrix --profiles narrow --rows 24 --repetitions 1 \
  --root "$P/cache" --jsonpath "$P/full_matrix_24.json"
```

Observed values are in `SMALL_PROBE/candidate_cold_16.json`, `SMALL_PROBE/protected_cold_16.json`, and `SMALL_PROBE/full_matrix_24.json`. The key values used in the findings:

```text
candidate cold 16 aggregate RSS: 103,653,376 B
candidate cold 16 i02_validation_seal: 42,455,040 B / delta 0
candidate cold 16 firstconsumer: 64,802,816 B / delta 307,200
candidate cold 16 persist: 103,653,376 B / delta 38,850,560

protected cold 16 aggregate RSS: 104,046,592 B
protected cold 16 i02_validation_seal: 40,001,536 B / delta 0
protected cold 16 firstconsumer: 99,500,032 B / delta 421,888
protected cold 16 persist: 104,046,592 B / delta 4,546,560
```

These are small nonacceptance probes. They demonstrate the method-attribution problem, not a 100k pass or fail.

## 6. Cold-only baseline pairing failure

Exact bounded command:

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-economics-review-r1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$R" \
python3 "$L/BENCH_DRAFT_SNAPSHOT/bench_w03_w04_physical.py" \
  --scenario cold --profiles narrow --rows 16 --repetitions 1 \
  --source-root "$R" \
  --baseline-json "$P/protected_cold_16.json" \
  --root "$P/paired_cold_cache" \
  --jsonpath "$P/paired_cold_16.json"
```

Observed failure (`SMALL_PROBE/paired_cold_16.stderr`):

```text
File ".../bench_w03_w04_physical.py", line 684, in _run_scenario
  "warm_vs_baseline": _compare((baseline_for or {}).get("warm", {}).get("aggregate") ...
AttributeError: 'NoneType' object has no attribute 'get'
```

The cold-only baseline had `"warm": null`, so the benchmark crashed before producing candidate JSON. This is exactly the W03 cold-only path; the defect is recorded as `ECON-M4`.

## 7. Protected/PR895 comparison

```text
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-r1 diff --stat \
  4f3413fc5c37b589be3412f826bf8f68ee617d4a \
  46b7325637e68f78ccc7487d4b1abc7009c5ac0b \
  -- rawlsing_next/_pre553_c11_execution_view.py \
     rawlsing_next/tests/test_pre553_c11_execution_view.py \
     rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py \
     .github/workflows/pyat-w03-w04-physical-economy.yml
```

Observed: PR895 changes 4 files (+377/-36); both protected and PR895 export `_compact_public_objects`, `ExactPhysicalCellStream`, `project_c11_candidate_from_physical_cells`, `source_backed_facade_key`, `CONTRACT_ID`, and `R5_CODEC_VERSION`. The protected 4f3413fc import and 16-row cold probe succeeded, so a protected baseline API is available; the failure is in the bench's cold-only baseline handling and methodology, not a missing protected symbol.

## 8. Commands explicitly not run

- No 100k benchmark or full matrix by this reviewer.
- No wide/repeat 100k.
- No original-source/respondent/SAV/DTA/DB read.
- No native/S3/science/actor workload.
- No full 12-ID, full 43-case, or 50-test author receipt reproduction.
- No CI job, merge, protected adoption, patch, post, new worker, model/provider/account/effort change.
