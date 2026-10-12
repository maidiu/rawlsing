# A04T — Reproduction

Source-free, no network, no raw survey data. Real tmpdirs, real subprocesses.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04t
git rev-parse HEAD        # b68de0dd35a9885efcb46bcd8ec9cbe41dabf500 (sealed startup)
python3 --version         # Python 3.11.3 (.pv3-venv)
```

## 1. v2 verifier suite — 44 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py -q
# → 44 passed
# verbose receipt: repro/logs/01_a04t_pytest_verbose.log
```

## 2. Independent join + hostile court (blocked-verifier subprocesses)

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ280-PV3-A04T-V2-VERIFIED-INDEPENDENT-JOIN-R1/repro/a04t_evidence_recorder.py
# → 23 cases; 20 must-fail detected; 3 must-pass pass
# writes repro/a04t_verifier_runs.json
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 3. Single join by hand (produce, then blocked verify)

```bash
D=$(mktemp -d)
W=WORKER_RETURNS/PYAT-HQ280-PV3-A04T-V2-VERIFIED-INDEPENDENT-JOIN-R1/repro/a04t_join_worker.py
python3 -c "import json; ..."  # write payload.json (see test _join helper)
PYTHONPATH=. python3 "$W" "$D" produce   # real owner chain -> produced.json
PYTHONPATH=. python3 "$W" "$D" verify    # blocked verifier -> verdict.json
```

The verify phase installs a candidate-import blocker first and records
`candidate_import_blocked: true` in every verdict.

## 4. Inherited suites (rerun, not rewritten)

```bash
# A04S 26 here:
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py -q  # → 26 passed
# A04 41 in its worktree:
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a04
python3 -m pytest rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py -q        # → 41 passed
# A05 18 in its worktree:
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-a05/WORKER_RETURNS/PYAT-HQ280-PV3-A05-INDEPENDENT-NODROP-ORACLE-R1/repro
python3 a05_hostiles.py   # → all_expectations_met: true
```

## 5. Integrity

```bash
git diff --name-only b68de0dd35a9885efcb46bcd8ec9cbe41dabf500 -- rawlsing_next/
# → empty (only the 2 NEW files are untracked)
git hash-object rawlsing_next/pre553_original_workload_contract_v2_candidate.py
# → 08bb75c431d3352cb0d17e9a65f7d855b4d35e59  (== A04S base)
find . -name '*.sav' -o -name '*.dta' | wc -l   # → 0
```

## 6. Not reproduced here

Repository-wide suite; any real source, raw SAV/DTA, real-source issuance,
real downstream consumer invocation, or external issuer/custodian. Out of
scope and unauthorized.