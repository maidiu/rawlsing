# Evidence index

```text
CI_RUN_42984252993_failed.log       exact preserved CI log
CI_RUN_42984252993_run.json         run/job/step status
CI_RUN_42984252993_junit.xml        99 tests, 98 pass, 1 failure
tests_22_affected_file.out          22 passed affected benchmark file
targeted_stage_tests.out            2 passed exact stage tests
stage_counter_severance.json        deterministic old-RED/new-GREEN counter proof
```

The only test change is in `rawlsing_next/tests/test_bench_w03_w04_physical.py`; production benchmark bytes and all thresholds remain untouched.
