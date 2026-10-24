# R91 R04_JOINED R3 resume

Branch: `agent/opencode-pyat-r91-r04-joined-custody-r1`

Code commit: `6068ab9e53b652ab603b30f8db55738393daff9b`

Startup: `dfeaab23998291be81abe4caecd08de663053eaa`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload_custody.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R91-R04-JOINED-CUSTODY-R1/revisions/r3/junit.xml -o addopts=''
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q -o addopts=''
```

Expected: `6 passed` and `16 passed`.

## Boundary

- Restored query/discovery outputs preserve native identity; discovery view is
  frozen/checked.
- Fixed external pin, original manifest and partial restart retained.
- R05+/original science remain NOT_REACHED. Distinct reviewer required.
