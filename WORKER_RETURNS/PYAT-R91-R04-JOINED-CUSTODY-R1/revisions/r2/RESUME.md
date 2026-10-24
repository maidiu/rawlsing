# R91 R04_JOINED R2 resume

Branch: `agent/opencode-pyat-r91-r04-joined-custody-r1`

Code commit: `c0c4b9e15a84546ca200d8da85bd3979832e7b1e`

Startup: `a88ccd140f30fe621140ee98841c6ce57ae9cab4`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload_custody.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R91-R04-JOINED-CUSTODY-R1/revisions/r2/junit.xml -o addopts=''
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q -o addopts=''
```

Expected: `5 passed` and `16 passed`.

## Boundary

- Actual R03 governed discovery and real partial multi-unit prefixes are
  retained; original external pin is mandatory.
- Partial fresh-process resume remains to be extended; full-prefix fresh-process
  resume passes.
- R05+/original science remain NOT_REACHED. Distinct reviewer required.
