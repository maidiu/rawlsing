# R95 R06R3 resume

Branch: `agent/opencode-pyat-r95-r06-world-consumer-integration-r1`

Startup: `08fa9a2560ff5a37313434a3edb3d61e702926eb`

Contract: `033efe2b4a636d909fe4def2056aa5c68762e182`

Code: `d0690af0c85fca962a4ac1e08012e869e94cb404`

## Reproduce

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_world_binding.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R95-R06-WORLD-CONSUMER-INTEGRATION-R1/revisions/r3/junit.xml -o addopts=''
```

Expected `14 passed` (~3m).

R06V independent probes are in
`0153d1f9b88ede3f76e5b1658a7441cb2e9a1713:WORKER_RETURNS/PYAT-R95-R06V-INDEPENDENT-WORLD-CONSUMER-REVIEW-R1/independent_probes/test_r06v_world.py`;
expected `5 passed` against this tree.

## Boundary

- Actual P41 execution is invoked by the wrapper from host-retained inputs.
- Cross-unit linkage is typed UNAVAILABLE; no pooling by label.
- CONTEXT promotion requires exact FF structural admission.
- Temporal pair is synthetic modeled-rule evidence, not original F7.
- No self-adoption; distinct reviewer follows.
