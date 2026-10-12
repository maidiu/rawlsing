# B01D — Reproduction

Source-free, no network, no raw survey data. Real tmpdirs, real files, real
signals.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01d
git rev-parse HEAD        # d4bb1907dbb1e00fcb6526489d18ad3796c7013e (sealed startup)
python3 --version         # Python 3.11.3 (.pv3-venv)
```

## 1. Candidate suite — 48 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py -q
# → 48 passed
# verbose receipt: repro/logs/01_b01d_pytest_verbose.log
```

## 2. Widest targeted run — 115 tests

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_discovery_adaptive.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_rabochii_execution_protocol.py -q
# → 115 passed
```

## 3. Repair evidence (real kills, side-effect counter, B01CR regression)

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ280-PV3-B01D-IDEMPOTENCE-RECOVERY-REPAIR-R1/repro/b01d_evidence_recorder.py
# → 8 attack variants all HELD; RERUN_SAFE unreachable; counter 1, then 2
#    under the demonstrated old rule; W1–W6 all PASS with W6 defect closed
# writes repro/b01d_repair_evidence.json
# writes repro/logs/02_b01d_crash_side_effect_transcript.txt
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 4. Single real SIGKILL in the crash window, by hand

```bash
D=$(mktemp -d)
W=WORKER_RETURNS/PYAT-HQ280-PV3-B01D-IDEMPOTENCE-RECOVERY-REPAIR-R1/repro/b01d_worker.py
python3 "$W" "$D" side_effect_then_die ; echo "exit=$?"   # → exit=137
cat "$D/side_effect_counter.txt"                          # → 1
python3 "$W" "$D" probe | python3 -m json.tool             # → UNKNOWN_OUTCOME, held=1
python3 "$W" "$D" unsafe_rerun_demo                        # → counter 2 (old-rule duplicate)
```

## 5. Defect reproduction (pre-fix rule, for the record)

```python
plan = cp.plan_recovery(ck, idempotence_proof={key: ""})
# pre-B01D:  RERUN_SAFE / rerunnable  (defect)
# post-B01D: UNKNOWN_OUTCOME / HELD, proof recorded as disregarded
```

## 6. Integrity

```bash
git diff --stat d4bb1907dbb1e00fcb6526489d18ad3796c7013e -- rawlsing_next/
# → exactly the 2 allowed files (candidate + its test)
grep -c "if unit_key in proofs" rawlsing_next/pre553_batch_durable_checkpoint_candidate.py
# → 0 (upgrade path removed)
find . -name '*.sav' -o -name '*.dta' | wc -l   # → 0
```

## 7. Not reproduced here

Repository-wide suite; any real source, raw SAV/DTA, REAL_EXECUTION approval,
or distributed locking. Out of scope and unauthorized.