# R95 R06 resume

Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`

Current code: `0b64393b2f4b8c28131f868738499475335496ed`

Startup: `a7f5cc70520e5236c24bbac241fad071c026d881`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/junit.xml -o addopts=''
```

Expected: `7 passed` (~2m40s; builds the pinned J42 packet twice for cold proof).

## Boundary

- Actual two-field N10E and actual J42/P41 N9/N10W/E04 selected views are proven.
- Temporal positive is permitted clock-mode/as-of mutation, not an observed F7
  measured-wave pair; that requirement remains open.
- R05 candidate learned product is not joined into J42; J42 uses its own pinned
  E04L learned-release readthrough.
- No original science, replacement engines, or self-adoption.
