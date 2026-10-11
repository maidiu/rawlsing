# A04 — Reproduction

Source-free, deterministic, no network, no raw survey data.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04
git rev-parse HEAD     # ce2d85a087aff43c45981e00ab822446d69daed9 (sealed startup)
python3 --version      # Python 3.11.3  (.pv3-venv)
python3 -c "import pytest; print(pytest.__version__)"   # 9.1.1
```

## 1. A04 suite — 41 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py -q
# → 41 passed
# verbose receipt: repro/a04_pytest_verbose.log
```

## 2. Targeted owner regression — 118 tests

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py -q
# → 118 passed in 6.88s
```

## 3. Measured source-free run + hostile court

```bash
PYTHONPATH=. python3 repro/a04_sourcefree_binder_repro.py
# → wrote repro/a04_sourcefree_runs.json
# → {"case_count": 21, "must_fail_cases": 17, "must_pass_cases": 4,
#    "failures_observed_with_expected_code": 17}
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 4. Determinism

```bash
PYTHONPATH=. python3 repro/a04_sourcefree_binder_repro.py
cp repro/a04_sourcefree_runs.json /tmp/run1.json
PYTHONPATH=. python3 repro/a04_sourcefree_binder_repro.py
diff /tmp/run1.json repro/a04_sourcefree_runs.json && echo IDENTICAL
# → byte-identical
```

## 5. Owner integrity check

```bash
git diff --stat HEAD          # empty: no tracked file modified
git hash-object rawlsing_next/pre553_route_b_production.py
# → 2385cd327dced3c5b887b59085aa0d21b04d78c3   == HQ280 evidence E18
git hash-object rawlsing_next/pre553_discovery_exact.py
# → 905f24d114419dbdd93879ad2bee5b59dd2f23af   == HQ280 evidence E19
```

## 6. Reading the fixture honestly

The synthetic source-free fixture is **reused unchanged** from the accepted
corpus: `rawlsing_next/tests/test_pre553_route_b_production.py::_fixture`.
A04 adds only extra `EmpiricalQuerySpec` objects built by the accepted
`_query` factory and puts them in a caller-issued `RuntimeObjectCatalog`.
The I05 discovery authority and its grammar are the fixture's own, untouched.

## 7. Not reproduced here

- Repository-wide suite — **INCONCLUSIVE**, see `04_TYPED_ISSUER_AND_PRODUCTION_HOLDS.md` §4.
- Any real source, WGC/WGD/WGE replay, raw SAV/DTA, or downstream consumer
  invocation. Out of scope and unauthorized.