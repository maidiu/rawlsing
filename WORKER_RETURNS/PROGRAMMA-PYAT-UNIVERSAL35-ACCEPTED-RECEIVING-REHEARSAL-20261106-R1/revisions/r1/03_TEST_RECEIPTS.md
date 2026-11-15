# R1 proportional test receipts

All commands used the existing controller venv and worktree; no new venv,
provider, server, config or permission was created.

```sh
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_source_configuration_corrections.py
# 13 passed in 27.47s
```

```sh
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_original35_execution.py
# 5 passed in 188.45s
```

```sh
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider --tb=short -v \
  rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes
# 1 passed in 2.30s
```

```sh
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider --tb=short \
  rawlsing_next/tests/test_pre553_field_forge_empirical_ingress.py
# 20 passed in 1.25s
```

D target observed sourcefree 30 facts / 30 envelopes / 30 typed
`FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED` refusals / 0 profiles; explicit
permission round-trip and default `None` no-artifact behavior; missing query
preserved the prior valid artifact with no staged temp. D r10 final-decision
ordering is covered.

Prior receiving proofs retained: A 49, D 21, E 20. No full estate/full original/
650s run was repeated.
