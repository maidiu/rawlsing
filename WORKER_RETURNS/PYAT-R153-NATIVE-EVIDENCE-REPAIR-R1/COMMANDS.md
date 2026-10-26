# R153 commands

## Focused checks (actual: 5 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R153-NATIVE-EVIDENCE-REPAIR-R1/tests/test_native_evidence_repair.py \
  -q -o addopts='' --basetemp=.r61/r153-test
```

## Regenerate repaired records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R153-NATIVE-EVIDENCE-REPAIR-R1/runtime").resolve()))
from native_evidence_repair import build_all, write_records
write_records(build_all())
PY
```

## Render one source

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R153-NATIVE-EVIDENCE-REPAIR-R1/runtime/render_r153_native_input.py \
  --source-id SRC35
```
