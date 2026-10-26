# R145 commands

## Focused binder checks (actual: 6 passed)

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/tests/test_source_package_binder.py \
  -q -o addopts='' --basetemp=.r61/r145-test
```

## Regenerate metadata-only preparation/records

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/runtime").resolve()))
from source_package_binder import build_all
print(build_all(".r61/r145-current-source-packages/inputs/METADATA_INPUTS.json",
                "WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1")["status"])
PY
```

## Authorized metadata receipt probe (synthetic; not a grant)

```sh
PYTHONPATH=. /usr/local/bin/python3 \
  WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/runtime/bind_authorized_metadata_receipt.py \
  --scope .r61/r145-current-source-packages/inputs/METADATA_INPUTS.json \
  --source-id SRC23 \
  --receipt .r61/r145-current-source-packages/test-authorized-receipt.json
```
