# B01E — Reproduction

Source-free, no network, no raw survey data. Real tmpdirs, real files, real
signals against the REAL accepted owners.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01e
git rev-parse HEAD        # 2fb5e8cc9971fe05899bbbeff837cd6cd049a969 (sealed startup)
python3 --version         # Python 3.11.3 (.pv3-venv)
```

## 1. Integration suite — 29 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_governed_batch_checkpoint_integration_candidate.py -q
# → 29 passed
# verbose receipt: repro/logs/01_b01e_pytest_verbose.log
```

## 2. Widest targeted run — 180 tests

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_governed_batch_checkpoint_integration_candidate.py \
  rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_pre553_discovery_adaptive.py \
  rawlsing_next/tests/test_rabochii_execution_protocol.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_pre553_carrier_execution.py -q
# → 180 passed
```

## 3. Evidence recorder (real kills, hostiles, reconciliation)

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ280-PV3-B01E-BATCH-DURABLE-INTEGRATION-R1/repro/b01e_evidence_recorder.py
# → positive COMPLETED + 3 real SIGKILLS + 7/7 hostiles detected
# writes repro/b01e_integration_evidence.json
# writes repro/logs/02_b01e_kill_resume_hostile_transcript.txt
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 4. Single real SIGKILL in the crash window, by hand

```bash
D=$(mktemp -d)
W=WORKER_RETURNS/PYAT-HQ280-PV3-B01E-BATCH-DURABLE-INTEGRATION-R1/repro/b01e_worker.py
python3 "$W" "$D" kill_in_window ; echo "exit=$?"   # → exit=137 (real SIGKILL)
python3 "$W" "$D" probe                             # → held=1, journal=1
python3 "$W" "$D" resume                            # → executed=0, blocked=2, journal stays 1
```

## 5. Integrity

```bash
git diff --name-only 2fb5e8cc9971fe05899bbbeff837cd6cd049a969 -- rawlsing_next/
# → exactly the 2 allowed files (adapter + its test)
grep -c "open(" rawlsing_next/pre553_batch_runner.py     # → 0  (F-01 re-verified)
grep -rn "execute_route_b_production" rawlsing_next/pre553_batch_durable_checkpoint_candidate.py | wc -l  # → 0 (B01D never touches the chain)
find . -path ./.git -prune -o -name '*.sav' -print -o -name '*.dta' -print | wc -l  # → 0
```

## 6. Not reproduced here

Repository-wide suite; any real source, raw SAV/DTA, REAL_EXECUTION
approval, distributed locking, or large-manifest performance. Out of scope
and unauthorized.