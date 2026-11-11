# Commands

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2

python3 -m pytest -q -o addopts='' -p no:cacheprovider \
  rawlsing_next/tests/test_bench_w03_w04_physical.py

python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold,full-matrix --profiles narrow,wide,repeat \
  --rows 8 --repetitions 3 --root <temp> \
  --source-root <protected-4f> \
  --jsonpath <baseline>

python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold,full-matrix --profiles narrow,wide,repeat \
  --rows 8 --repetitions 3 --root <temp> \
  --source-root <candidate> \
  --baseline-json <baseline> \
  --jsonpath <current>

python3 CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py changed \
  --base 287f5e18ffaf09acb54dea31b60f8486f845f334 \
  --head 9a71d0a0825c142372e56ac5d6bd34847ce6f227 --root .
```

The full 100k matrix and economic receiving remain unrun.
