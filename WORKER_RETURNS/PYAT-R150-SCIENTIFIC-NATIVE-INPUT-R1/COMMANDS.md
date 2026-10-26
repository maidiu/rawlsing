# R150 commands

## Focused checks (actual: 7 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/tests/test_scientific_native_input.py \
  -q -o addopts='' --basetemp=.r61/r150-test
```

## Regenerate B49 native-input records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/runtime").resolve()))
from scientific_native_input import build_all, write_records
write_records(build_all())
PY
```

## Render one source

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/runtime/render_scientific_native_input.py \
  --source-id SRC27
```
