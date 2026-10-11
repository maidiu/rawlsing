# B01C — Reproduction

Source-free, deterministic where claimed, no network, no raw survey data.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01c
git rev-parse HEAD        # 923e2c1d0ff27961233c52c385f672bbd1a4f23c (sealed startup)
python3 --version         # Python 3.11.3  (.pv3-venv)
```

## 1. B01C suite — 35 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py -q
# → 35 passed
# verbose receipt: repro/logs/01_b01c_pytest_verbose.log
```

## 2. Accepted owner + protocol regression

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_rabochii_execution_protocol.py -q
# → 69 passed

python3 -m pytest \
  rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py \
  rawlsing_next/tests/test_pre553_batch_runner.py \
  rawlsing_next/tests/test_pre553_route_b_production.py \
  rawlsing_next/tests/test_pre553_discovery_adaptive.py \
  rawlsing_next/tests/test_pre553_discovery_exact.py \
  rawlsing_next/tests/test_rabochii_execution_protocol.py -q
# → 102 passed
```

## 3. Real process kill / restart + hostile court

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ280-PV3-B01C-DURABLE-CHECKPOINT-CANDIDATE-R1/repro/b01c_evidence_recorder.py
# → 5 kill/resume scenarios, 19 durability cases, all met
# writes repro/b01c_kill_resume_results.json
# writes repro/logs/02_real_kill_resume_transcript.txt
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 4. Reproduce a single real SIGKILL by hand

```bash
D=$(mktemp -d)
W=WORKER_RETURNS/PYAT-HQ280-PV3-B01C-DURABLE-CHECKPOINT-CANDIDATE-R1/repro/b01c_worker.py
python3 "$W" "$D" start ; echo "exit=$?"     # -> exit=137 (real SIGKILL)
python3 "$W" "$D" probe                       # -> 1 durable START intent, held=1
```

The worker calls `os.kill(os.getpid(), SIGKILL)` itself after fsyncing the
intent, so the kill is a genuine uncatchable signal, not a simulated one.

## 5. Owner integrity

```bash
git diff --name-only 923e2c1d0ff27961233c52c385f672bbd1a4f23c -- rawlsing_next/
# → empty
grep -c "open(" rawlsing_next/pre553_batch_runner.py     # → 0  (F-01 re-verified)
find . -name '*.sav' -o -name '*.dta' | wc -l           # → 0  (source-free)
```

## 6. Not reproduced here

The repository-wide suite; B01 F-04/F-05/F-06; any real source, raw SAV/DTA, or
REAL_EXECUTION approval. Out of scope and unauthorized.