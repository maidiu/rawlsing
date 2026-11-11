# Bench lane — W34-REPRODUCIBLE-RETURN

**Author status:** `INCOMPLETE` — benchmark implementation/harness/baselines delivered; final 100k candidate matrix and independent economic receiving remain pending an HQ-pinned integrated candidate head.

## Changed files (code lease)

```text
rawlsing_next/bench_w03_w04_physical.py
rawlsing_next/tests/test_bench_w03_w04_physical.py
.github/workflows/pyat-w03-w04-physical-economy.yml
```

No production facade/ingest/repository/execution-view/carrier edits.

## Actual commands and results

```text
# focused benchmark tests
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... PYTHONPATH=. python3 -m pytest -q -o addopts='' -p no:cacheprovider rawlsing_next/tests/test_bench_w03_w04_physical.py
7 passed

# selected W03/W04 regression set
pytest test_bench_w03_w04_physical.py test_pre553_c11_execution_view.py \
  test_pre553_c11_cold_reopen_i03.py test_pre553_source_backed_c11_facade.py \
  test_pre553_carrier_execution.py test_pre553_i03_grouping.py
50 passed (7 benchmark tests + 43 selected W03/W04 regressions)
```

`current_46b_1000_full_matrix.summary.json`, `protected_4f3413_1000_full_matrix.summary.json`, `current_46b_100000_narrow_cold.summary.json`, `protected_4f3413_100000_narrow_cold.summary.json`, and `proof_02_resource_comparison.json` are committed in this lane as compact machine receipts; the raw full-consumer JSON hashes are recorded in `proof_02_resource_comparison.json` and the raw files are not committed because of size. The 100k narrow child succeeded under the 6 GiB cap; the wide/repeat 100k and final three-repetition matrix are explicitly `NOT_RUN` pending integrated candidate.

## PR and review pins

- PR895 head: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`; remote pull ref unchanged at readback.
- Contract source: `5a891a311c70f4cb8c09864008b33405362f7c7c`.
- Protected baseline: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`.
- Prior reviewed compact blobs: `986f327a...` / `8e8effa5...`; retained.
- Starting anchor `a5f21266...` was contract-only/source-less; exact frozen source restored via source anchor `1b0c8dc4...` with no `rawlsing_next` diff against `46b73256`.

## CI

`.github/workflows/pyat-w03-w04-physical-economy.yml` now runs the selected W03/W04 tests plus a 256-row sourcefree full-matrix smoke benchmark. The smoke is explicitly not 100k acceptance; it exercises cold/warm/delete/rebuild and actual I03/I05.

## Remaining boundary

- Final candidate matrix must run at the HQ-pinned integrated candidate head with 100k rows and 3 repetitions; not this lane's pre-integration 46b source.
- At least one profile must achieve >=15% cold median RSS improvement and repeat-heavy warm wall <=90% baseline; current 100k narrow shows a 13.0% RSS regression, so no target PASS.
- Preserve the narrow cold wall regression and all paired receipts; no replacement baseline or invented source performance.
- Independent code/economic review at final immutable head remains required. Whole 12-ID MCR coverage is an HQ/integration responsibility; this lane does not claim it.
