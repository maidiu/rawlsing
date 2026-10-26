# R154 commands

## Compile / rebuild store

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime").resolve()))
from r154_compile import build, build_store, write_exports
r = build()
build_store(r)
write_exports(r)
print(r["summary"]["status"])
PY
```

## Validate + cold load

```sh
PYTHONPATH=. /usr/local/bin/python3 -m pytest \
  WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/tests/test_r154_store.py \
  -q -o addopts='' --basetemp=.r61/r154-test
```

## Load native inputs

```sh
PYTHONPATH=. /usr/local/bin/python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime").resolve()))
from r154_load import load_source, build_native_workload
p = load_source("SRC23")
print(p.source_id, p.native_source_identity.declared_sha256, p.codebook_row_count)
try:
    build_native_workload("SRC23")
except Exception as e:
    print("blocked:", e)
PY
```

## Actual response execution

Not runnable in this job. It stops at exact current source-read grant/resolver,
grounded occurrence/scientific issuance, U/Epre, and downstream authority.
