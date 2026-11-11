# Reproducible return

**Source head:** `81a4f4cd314bd236d8f742e3fde343363a73168a`
**Branch:** `agent/pyat-w03-w04-mcr-bench-integrated-r2`
**Prior bench evidence:** `c44cf09fb9ca5cbc235763d8bd5df9b0074de289`

## Changed files (bench only)

```text
rawlsing_next/bench_w03_w04_physical.py
rawlsing_next/tests/test_bench_w03_w04_physical.py
```

The existing W03/W04 workflow at this integrated head already carries the selected test and smoke-benchmark steps; it was read and reused, not changed in this repair. No production facade/ingest/repository/cache/carrier changes.

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -o addopts='' \
  -p no:cacheprovider \
  rawlsing_next/tests/test_bench_w03_w04_physical.py \
  rawlsing_next/tests/test_pre553_w03_w04_cold.py \
  rawlsing_next/tests/test_pre553_w03_w04_completion.py
# 35 passed
```

```text
python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold --profiles narrow,wide,repeat --rows 64 --repetitions 1 \
  --root <temp-root> --source-root <current|frozen46b|protected4f> \
  --jsonpath INTEGRATED_R2/parity_<source>_64_cold.json
```

```text
python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario full-matrix --profiles narrow,wide,repeat --rows 64 --repetitions 1 \
  --root <temp-root> --source-root <current> \
  --jsonpath INTEGRATED_R2/current_64_full_matrix.json
```

## Exact source pins

- current integrated: `81a4f4cd314bd236d8f742e3fde343363a73168a`
- cold/policy coupling: `2709733e`
- persistence candidate: `558f4169`
- frozen PR895: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`
- protected baseline: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`

Reviewed prior compact blobs `986f327a...` / `8e8effa5...` remain retained; no silent production source change.

## Remaining

- Full 100000 × 3-repetition matrix (`full-matrix` and required profiles) not launched.
- Independent same-method economic check and final pinned candidate SHA required before that measurement.
- Final 15% cold-RSS / 90% repeat-wall target not evaluated here.
- All 12 MCR obligations, independent code/economic receiving, external block/verifier and protected receiving remain open. No full-goal acceptance.
- Quota UNKNOWN; automatic goal checks paused.

## Exact benchmark blobs

```text
6c1bcd3fc3be36bbd68f07ab55d629613f778912  rawlsing_next/bench_w03_w04_physical.py
71ae118bd11989949ad02b1b51bbe09b93e816d1  rawlsing_next/tests/test_bench_w03_w04_physical.py
a12f5dcde35f4d89ff281f1ec2f02200c4ac2e36  .github/workflows/pyat-w03-w04-physical-economy.yml
```

## Small-validation outputs

`parity_current_64_cold.json`, `parity_frozen46b_64_cold.json`, `parity_protected4f_64_cold.json`, `current_64_full_matrix.json`, `parity_summary.json`, `small_tests.out` are committed under this sublease. `final_matrix_eligible` is false in the 64-row run and `acceptance_status` explicitly says `NON_FINAL_DIAGNOSTIC__DO_NOT_REPORT_AS_FULL_MATRIX_PASS`.
