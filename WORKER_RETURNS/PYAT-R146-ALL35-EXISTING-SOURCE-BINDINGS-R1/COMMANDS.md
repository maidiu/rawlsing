# R146 commands

## Focused all35 checks (actual: 6 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/tests/test_all35_reuse_binder.py \
  -q -o addopts='' --basetemp=.r61/r146-test
```

## Regenerate all35 records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime").resolve()))
from all35_reuse_binder import build_all35, write_records
write_records(build_all35())
PY
```

## Render one source

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime/render_source_preparation.py \
  --source-id SRC23
```
