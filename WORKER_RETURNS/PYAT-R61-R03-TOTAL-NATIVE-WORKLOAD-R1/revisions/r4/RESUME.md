# R03 R4 resume

Branch: `agent/opencode-pyat-r61-r03-total-native-workload-r1`

Code commit: `61ce7975d822688edd9525a10ad7fa9048f69455`

Startup: `5b28d09602a35d4c5d5f060f450956c612ab3580`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_workload.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R03-TOTAL-NATIVE-WORKLOAD-R1/revisions/r4/junit.xml \
  -o addopts=''
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q -o addopts=''
```

Expected: `15 passed` and `32 passed`.

## Boundary

- Restore requires the separately provisioned original checkpoint pin; no
  unpinned fallback.
- Native owners/U43 unchanged; no R04+ or original science.
- Distinct reviewer required; no self-adoption.
