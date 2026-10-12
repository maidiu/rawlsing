# E03 — Reproduction

Source-free, no network, no raw survey data.

## Environment

```bash
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq281-e03
git rev-parse HEAD        # e79c6a136748c204963d2169c4f64b0c48374437 (sealed startup)
python3 --version         # Python 3.11.3 (.pv3-venv)
```

## 1. Candidate suite — 18 tests

```bash
python3 -m pytest rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py -q
# → 18 passed
# verbose receipt: repro/logs/01_e03_pytest_verbose.log
```

## 2. Widest targeted run — 227 tests

```bash
python3 -m pytest \
  rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py \
  rawlsing_next/tests/test_pre553_analytical_composition.py \
  rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py \
  rawlsing_next/tests/test_pre553_empirical_possibility_provider.py \
  rawlsing_next/tests/test_pre553_empirical_query.py \
  rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py \
  rawlsing_next/tests/test_pre553_service_f8_source_scope_binding_court.py -q
# → 227 passed
```

## 3. Evidence recorder (real chain + hostile refusals)

```bash
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-HQ281-E03-ACTUAL-N9-N10W-PROGRESSIVE-JOIN-R1/repro/e03_evidence_recorder.py
# → 3/3 steps match hand-derived oracle; 11 refusals demonstrated;
#   3 owner absences recorded; writes repro/e03_progressive_runs.json
```

Requires `PYTHONPATH=.` because the script lives under `WORKER_RETURNS/`.

## 4. Single chain run by hand

```python
import sys; sys.path.insert(0, '.')
import rawlsing_next.pre553_n9_n10w_progressive_candidate as pc
chain = pc.run_progressive_chain(pc.build_synthetic_world())
for s in chain.steps:
    print(s.step_id, s.raw_denominator_support, s.consumer_state,
          s.produced_evidence.uncertainty_state)
# P_Y_given_A 32 EXACT_SUPPORTED UNCERTAINTY_UNQUANTIFIED
# P_Y_given_A_B 16 EXACT_SUPPORTED UNCERTAINTY_UNQUANTIFIED
# P_Y_given_A_B_C 8 EXACT_SUPPORTED UNCERTAINTY_UNQUANTIFIED
```

## 5. Integrity

```bash
git diff --name-only e79c6a136748c204963d2169c4f64b0c48374437 -- rawlsing_next/
# → empty (only the 2 NEW files are untracked)
find . -path ./.git -prune -o -name '*.sav' -print -o -name '*.dta' -print | wc -l   # → 0
```

## 6. Not reproduced here

Repository-wide suite; any real source, raw SAV/DTA, N9/N10W implementation,
G0b issuance, CURRENT selection or actor/V3 state. Out of scope and
unauthorized.