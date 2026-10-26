# R148 commands

## Focused checks (actual: 6 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/tests/test_all35_complete_metadata.py \
  -q -o addopts='' --basetemp=.r61/r148-test
```

## Regenerate all35 records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/runtime").resolve()))
from all35_complete_metadata import build_all35, write_records
write_records(build_all35())
PY
```

## Render one source

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/runtime/render_all35_current_preparation.py \
  --source-id SRC13
```
