# Execution and Frozen Oracles

## Commands

```
python3 -m pytest WORKER_RETURNS/.../R4-T8F2-.../repro/test_t8f2_temporal_custody.py -q
# exit 0, 21 passed
python3 -m pytest <t8c-control-copy>/test_hq297_t8c.py -q
# exit 0, 19 passed (untouched historical control, not acceptance)
python3 -m pytest <t8r-control-copy>/test_review_mandatory_guards_red.py -q
# exit 1, 3 failed as expected (RED reproduced)
```

## Frozen oracles unchanged

- T8I `test_t8i_independent_hostiles.py` blob `3911420d…0eb6ff6`: adapted to
  the versioned T8F2 interface in a separate file; original assertions preserved.
- T8C 19 and T8R 3 executed byte-identical from their commits; not modified.
- T8F 29 author behaviors covered by the 21 T8F2 tests through the new
  two-ref interface (adapted interface separate, per commission).

## Host

Python 3.11.3, pytest 9.0.2, macOS Darwin, local OpenCode session.
Model/quota: UNKNOWN (local execution only, no paid calls).
