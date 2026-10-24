# R91 R04_JOINED resume

Branch: `agent/opencode-pyat-r91-r04-joined-custody-r1`

Code commit: `ef1e71628c0a89753c0c6aeea3c35c5fb06e29eb`

Startup: `c912497b25411ebbd3d796db139f32f5bebb6c4c`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload_custody.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R91-R04-JOINED-CUSTODY-R1/junit.xml -o addopts=''
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q -o addopts=''
```

Expected: `3 passed` and `16 passed`.

## Boundary

- Joined resume at workload granularity; completed units are not rerun.
- No byte-decoder rewrite, R05+ or original science.
- Distinct reviewer required; no self-adoption.
