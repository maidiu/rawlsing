# A04S — Reproduction

Source-free, deterministic where claimed, no network, no raw survey data.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04s
git rev-parse HEAD        # 0f8c6d085513588c5fdfcf371c1e8fe1e7927059 (sealed startup)
python3 --version         # Python 3.11.3 (.pv3-venv)
```

## 1. v2 suite — 26 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py -q
# → 26 passed
# verbose receipt: repro/logs/01_a04s_pytest_verbose.log
```

## 2. Widest targeted run — 103 tests

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py -q
# → 103 passed
```

## 3. Old suites (other worktrees, unmodified)

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py -q
# → 41 passed
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a05/WORKER_RETURNS/PYAT-HQ280-PV3-A05-INDEPENDENT-NODROP-ORACLE-R1/repro
python3 a05_hostiles.py   # → all_expectations_met: true (18/18)
```

## 4. Measured owner → oracle chain + hostile court

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ280-PV3-A04S-A05-V2-WORKLOAD-CONTRACT-R1/repro/a04s_evidence_recorder.py
# → 19 cases; 16 must-fail detected; 3 must-pass pass
# writes repro/a04s_owner_oracle_runs.json
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 5. Owner and A04/A05 integrity

```bash
git diff --name-only 0f8c6d085513588c5fdfcf371c1e8fe1e7927059 -- rawlsing_next/
# → empty
git hash-object rawlsing_next/pre553_original_workload_binder_candidate.py
# → 7d8b3902c3f8f257637b7c07ad9feb5e096d48e5  (== cbe047cf)
git hash-object rawlsing_next/pre553_route_b_production.py
# → 2385cd327dced3c5b887b59085aa0d21b04d78c3  (== E18)
git hash-object rawlsing_next/pre553_discovery_exact.py
# → 905f24d114419dbdd93879ad2bee5b59dd2f23af  (== E19)
find . -name '*.sav' -o -name '*.dta' | wc -l   # → 0
```

## 6. Not reproduced here

Repository-wide suite; any real source, raw SAV/DTA, real-source issuance,
or real downstream consumer invocation. Out of scope and unauthorized.