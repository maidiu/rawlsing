# Reproducible return

## Changed files

```text
rawlsing_next/bench_w03_w04_physical.py
rawlsing_next/tests/test_bench_w03_w04_physical.py
```

No production facade/ingest/repository/cache/carrier change. Existing W03/W04 workflow is reused; no workflow diff in this repair.

## Exact code blobs

```text
1789450f9a2f3cdf79265478c4103920a8e2f2bc  rawlsing_next/bench_w03_w04_physical.py
1ca91502a30ea6af2bb983a71e465dd613cdbf1a  rawlsing_next/tests/test_bench_w03_w04_physical.py
```

## Commands and results

```text
pytest bench + test_pre553_w03_w04_cold + test_pre553_w03_w04_completion
40 passed

pytest benchmark-only
13 passed
```

```text
bench --scenario cold --profiles narrow,wide,repeat --rows 64 --repetitions 1 \
  --source-root current|frozen46b|protected4f
```

```text
bench --scenario cold,full-matrix --profiles narrow,wide,repeat --rows 64 \
  --repetitions 1 --baseline-json baseline_protected_4f_64_both.json
```

Raw and compact evidence files are in this sublease. No 100000 matrix was run. Final economic receiving must rerun at an HQ-pinned final candidate SHA with the corrected method, all three profiles, 100000 rows, three repetitions, protected 4f baseline, and independent same-method review.

## Residual

Whole 12-ID contract, final candidate/economic receiving, external MCR block/verifier and protected adoption remain open. Quota `UNKNOWN`; goal checks paused.
