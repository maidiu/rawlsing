# R147 commands

## Focused checks (actual: 6 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/tests/test_current_metadata_reuse.py \
  -q -o addopts='' --basetemp=.r61/r147-test
```

## Regenerate all35 records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime").resolve()))
from current_metadata_reuse import build_all35, write_records
write_records(build_all35())
PY
```

## Render one source

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime/render_current_source_preparation.py \
  --source-id SRC23
```
