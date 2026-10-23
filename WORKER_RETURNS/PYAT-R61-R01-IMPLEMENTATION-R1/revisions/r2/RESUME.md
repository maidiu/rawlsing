# R01 R2 resume

Branch: `agent/opencode-pyat-r61-r01-generic-grammar-r1`

R2 code commit: `d56e53301aaa0203e83fc1b60a0bcafb86b17892`

Startup for this repair: `fcf9fe9f8662c9e98801e670d0d4357072d8d453`

## Reproduce author suite

```sh
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r01
/usr/local/bin/python3 -m pytest rawlsing_next/tests/test_universal_grammar.py -q \
  --junitxml=WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r2/junit.xml \
  -o addopts=''
```

Expected: exit `0`, `18 passed`, no skips.

## Replay reviewer blocking defects D1-D8

The disposable reviewer probe was copied outside the immutable reviewer tree for
replay only:

```sh
PYTHONPATH="$PWD:$PWD/.r61/tmp" PYTHONDONTWRITEBYTECODE=1 \
  /usr/local/bin/python3 -m pytest .r61/tmp/test_r01v_independent.py -q \
  -o addopts='' -k 'DEFECT and not topology'
```

Expected: `9 passed`. The excluded D9 probe asserts the old frontier
pre-classification behavior that R2 intentionally repairs; the committed
catalog-promotion test covers the repaired behavior.

## Boundary

- V1 and reviewer returns are immutable; do not edit them.
- R03 is NOT_STARTED. This return supplies pre-execution lowering only.
- No serialized cold restore (R04), original source/science, F6/F7/F8, N11/N12,
  production/CI or J52/W52 claim.
- A fresh distinct reviewer session must independently qualify the exact pushed
  R2 candidate. The author does not self-adopt.
