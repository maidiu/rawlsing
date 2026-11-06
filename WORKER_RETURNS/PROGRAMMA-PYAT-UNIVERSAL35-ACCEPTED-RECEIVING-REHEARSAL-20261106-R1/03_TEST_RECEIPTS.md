# Integration test receipts

All commands were run from the integration branch on Darwin, using the existing
controller venv `/tmp/rawlsing-oct28-p1r1/venv/bin/python`; no new venv, package,
provider, server or controller was created.

## Component suites

```text
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  rawlsing_next/tests/test_source_configuration_current_port.py \
  rawlsing_next/tests/test_source_configuration_library.py \
  rawlsing_next/tests/test_source_configuration_foundation.py \
  rawlsing_next/tests/test_source_configuration_corrections.py \
  rawlsing_next/tests/test_pre553_source_read_admission.py \
  -p no:cacheprovider --tb=short
49 passed in 141.35s
```

```text
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  rawlsing_next/tests/test_pre553_original35_physical_stream.py \
  rawlsing_next/tests/test_pre553_original35_operations.py \
  rawlsing_next/tests/test_pre553_original35_execution.py \
  rawlsing_next/tests/test_programma_pyat_original35_constructor_adapter.py \
  -p no:cacheprovider --tb=short
21 passed in 281.40s
```

```text
TMPDIR=$PWD/.local-logs/pyat-universal35/tmp PYTHONDONTWRITEBYTECODE=1 \
/tmp/rawlsing-oct28-p1r1/venv/bin/python -m pytest -q \
  rawlsing_next/tests/test_pre553_field_forge_empirical_ingress.py \
  -p no:cacheprovider --tb=short
20 passed in 1.02s
```

Full logs: `evidence/a_component_tests.log`, `evidence/d_component_tests.log`,
`evidence/e_component_tests.log`.

The initial A/D attempts failed only because the selected source-config tests
require `SOURCE_PRE553_PLAN/LANES.json` and
`source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json`.
Those exact A-final resources were added; the same tests then passed with no
production-code changes. Initial and final logs are retained in
`.local-logs/pyat-universal35/review-results/`.

## Joined producer-consumer checks

```text
PYTHONPATH=. TMPDIR=$PWD/.local-logs/pyat-universal35/tmp \
/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  .local-logs/pyat-universal35/review_ab_integration.py
library_ids 35 available 35
... items 18276 ... operations 18467 ...
plan_ref 9b54d62e94f8ff18fa7da549af21d18fb54562a4d88cd40d55a66a492080fb0d
no_drop true
```

```text
PYTHONPATH=. TMPDIR=$PWD/.local-logs/pyat-universal35/tmp \
/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  .local-logs/pyat-universal35/review_d_r1_all35_frontier.py
sources_frontier_rows 7; total_operations 694; total_eligible 683;
total_deferred 0; 28 typed NO_EXPLICIT_PLANNED_FRONTIER
```

```text
PYTHONPATH=. TMPDIR=$PWD/.local-logs/pyat-universal35/tmp \
/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  .local-logs/pyat-universal35/review_d_r4_resolver.py
positive PASS {"facts": 30, "expected_ops": 15,
"expected_candidates": 18, "selected": ["A","B","Y"],
"anti": true, "op_anti": true, "native": false}
revoked_before REFUSED SourceReadAdmissionRefusal SOURCE_READ_REVOKED
changed_after REFUSED Original35ExecutionError SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER
revoked_after REFUSED Original35ExecutionError SOURCE_READ_DECISION_CHANGED_AFTER_CONSUMER
```

The sourcefree harness is evidence-only, uses the test sourcefree fixture, and
contains no private grant or original source material. It is not integrated
production code.

## E handoff status

The E component tests pass, but no authentic D->E cold envelope was constructed or
run. The accepted D wrapper material exposes `fact_refs` and `receipt_refs`, not
the exact fact/query objects or replay/permission fields required by E. The D r7
actual original attempt produced no facts. See
`04_ACTUAL_RUN_NEGATIVE_AND_OWNERS.md`; E is `NOT_RUN`, not complete.
