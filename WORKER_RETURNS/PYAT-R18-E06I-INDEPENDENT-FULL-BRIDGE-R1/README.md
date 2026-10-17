# E06I — independent full-bridge court (reproduction kit)

Verdict: `ACCEPT_SOURCEFREE_NONINSTALLING_JOINED_BRIDGE_METHOD_ONLY` — see
`00_INDEPENDENT_VERDICT.md`.

Reviewed candidate:
`agent/userdirect-pyat-20261016-r17-e06-e04e05-native-bridge-r1`
@ `f9c52113de38caececc450f0e54c980f64ed3981`.

## Layout

| Path | Meaning |
| --- | --- |
| `00_INDEPENDENT_VERDICT.md` | verdict, identities, court table, residuals |
| `01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json` | expectations frozen before the court ran |
| `02_EXECUTED_ORIGINAL_OWNER_AND_BOTH_CLIENTS.json` | reviewer execution record (imports, frames, F8, clients) |
| `03_CROSS_BOUNDARY_GRANT_CLOCK_COLD_ATTACKS.md` | attack log with per-case dispositions |
| `04_METHOD_RIGHTS_HQ_NEXT_EDGE.md` | method rights, residual list, next competent edge |
| `tests/test_e06i_independent_court.py` | 48 independent hostile cases |
| `tests/conftest.py` | locates the staged candidate via `E06_CANDIDATE_ROOT` |
| `repro/freeze_precommitted_oracle.py` | derives the numerical oracle from raw native rows |
| `repro/run_court.py` | author-40 regression + independent-48 court |
| `repro/observe_court.py` | reviewer profiler / execution record |
| `repro/cold_independent.py` | one cold OS process replay |
| `repro/verify_source_closure.py` | independent 402/401/E04T preimage verification |
| `observations/` | JUnit, stdout, cold ledgers/outputs, source-closure proof |

## How to run

The court imports the candidate read-only. First materialise the candidate at its
exact commit and run **its own** staging (which populates its gitignored
`runtime/`):

```sh
git worktree add --detach /tmp/e06i-court f9c52113de38caececc450f0e54c980f64ed3981
cd /tmp/e06i-court/WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1
PYTHONDONTWRITEBYTECODE=1 python3 repro/stage_sources.py
export E06_CANDIDATE_ROOT="$PWD"
```

Then, from this return:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 repro/verify_source_closure.py   # source identity
PYTHONDONTWRITEBYTECODE=1 python3 repro/run_court.py              # 40 regression + 48 independent
PYTHONDONTWRITEBYTECODE=1 python3 repro/observe_court.py          # execution record
```

`run_court.py` executes the author suite **inside the candidate checkout**
(because that suite resolves its root from its own location and rewrites its own
cold-process observation files). Run it only against a scratch worktree, never
against a checkout you intend to keep clean.

## Independence

* Expectations in `01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json` are derived only
  from the raw native source rows and from the commission's hostile list, not
  from candidate products, and were written before the independent court ran.
* The author's 40 cases are executed separately and labelled regression grade;
  the acceptance basis is the 48 independent cases.
* No candidate, frozen test, accepted E04T/E05R module, canonical file, original
  source or issuer artifact is modified by this return.
