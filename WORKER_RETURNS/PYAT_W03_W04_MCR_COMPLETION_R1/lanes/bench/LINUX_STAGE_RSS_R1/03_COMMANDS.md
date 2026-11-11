# Commands

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2

python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_bench_w03_w04_physical.py

python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_bench_w03_w04_physical.py::test_stage_peak_tracks_post_highwater_allocation \
  rawlsing_next/tests/test_bench_w03_w04_physical.py::test_stage_peak_is_not_aliased_to_process_highwater
```

Result: 22 passed; targeted 2 passed. No 99-suite/smoke/100k rerun.
