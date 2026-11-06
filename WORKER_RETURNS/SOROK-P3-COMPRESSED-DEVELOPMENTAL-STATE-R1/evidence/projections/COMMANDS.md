# Exact commands

```sh
R=/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-recursion-reuse-r1
S="$R/WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"

PYTHONPATH="$R:$S:$R/WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1" \
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 -B -m pytest -q -p no:cacheprovider "$S/tests/test_projections.py" \
  --junitxml="$S/evidence/projections/test_junit.xml"
```

Observed: **8 passed in 0.09s**.

Only `p3/projections.py`, `tests/test_projections.py` and `evidence/projections/`
were written. No sourcepack, #704/P2, P3Owner, storage, compression, PROGRAMMA or
production registry file was edited.
