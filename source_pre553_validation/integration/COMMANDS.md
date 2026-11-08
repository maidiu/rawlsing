# R157 P5 portable delivery commands

All commands run from the repository root with `PYTHONPATH=.`; no private
author-worktree path is required.

```sh
# 1. Build/rebuild the portable index and SQLite lookup
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli build-index

# 2. Current readiness: all 35 accepted source configurations available
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli status
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli list

# 3. Inspect / validate one source
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli show SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli validate SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli validate SRC01 --native

# 4. Actual native C11 constructor/validator on the configured nonrespondent fixture
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC04
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC16
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC31

# 5. Separately authorized original operation plan (no bytes opened)
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli original-plan SRC01 \
  --source-path <EXTERNAL_SOURCE_ROOT>/<file> \
  --host <authorized-host> --purpose <authorized-purpose> \
  --consumer-use <authorized-consumer-use> \
  --semantic-scope <authorized-semantic-scope>

# 6. Focused checks, including exact-case path portability
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts=''
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts='' -k exact
```

Expected: index counts `available=35`, `pending=0`; every indexed artifact path
is an actual exact-case directory entry; all35 source-config->native fixture
consumer calls return `C11LogicalRelease` and `source_read_performed=false`.
