# R151 commands

## Focused checks (actual: 6 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/tests/test_grounded_occurrences.py \
  -q -o addopts='' --basetemp=.r61/r151-test
```

## Regenerate records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime").resolve()))
from grounded_occurrences import build_all, write_records
write_records(build_all())
PY
```

## Render one source

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime/render_grounded_native_input.py \
  --source-id SRC35
```
