# PYAT HQ285 L02 — Exact independent runtime court

**TERMINAL:** `PYAT_R3_HQ285_L02_EXACT_INDEPENDENT_RUNTIME_COURT_COMPLETE__GITHUB_PUSHED`
**Role:** independent runtime/evidence reviewer, **NOT** HQ. No scientific issuance, no protected CURRENT, no self-adoption.
**Branch:** `agent/reviewer-pyat-r3-hq285-l02-independent-runtime-evidence-r1` @ `62f5b398ec99019627e25148e481ff8620971b22`
**Environment:** SECONDARY Mac · macOS 13.7.8 x86_64 · Python 3.11.3 · pytest 9.1.1 · isolated sparse worktree on the shared object store. **No clone, no reset, no worktree mutation of others, no frozen-oracle edits, no producer code copied into this branch.**
**Model/privacy/cost:** the harness configured the eligible session; **no model identity, privacy claim or cost figure is invented here**, and no primary Codex, reset credits or paid overflow were used.

## 1. P01/S05JR — the 86 failures are FULLY EXPLAINED AND RESOLVED

**Command:**
```
python3.11 -m pytest \
  tests/test_pre553_v2_durable_consumer_integration_candidate.py \
  tests/test_pre553_original_workload_v2_verifier_candidate.py \
  tests/test_pre553_governed_batch_checkpoint_integration_candidate.py \
  tests/test_pre553_batch_durable_checkpoint_candidate.py \
  tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py -q
```

| run | terrain | result |
|---|---|---|
| L01 (my prior run) | only `rawlsing_next/` materialised | 86 failed / 83 passed / 6 skipped |
| **L02 (this court)** | **complete `73d45f3a` tree incl. `WORKER_RETURNS/` (103 fixture entries)** | **169 passed / 6 skipped / 0 FAILED — EXIT 0** |

**Independent classification of the historical 86 — not a count:** they were **100 % missing-fixture setup terrain**. Zero were scientific failures and zero were code failures. The mechanism is proven, not asserted: the L01 log's dominant signature was `FileNotFoundError` against `WORKER_RETURNS/…` paths, and materialising the required fixture terrain drives failures to **exactly zero**. The historical number was an artefact of an incomplete checkout, and I record that plainly rather than leaving it as an unexplained red.

The composed route itself is **green at 169/169 collected-and-not-skipped** on the complete original tree.

## 2. S03/S03R/S03F — the "34 pass / 1 fail" vs "11 setup errors" contradiction is RESOLVED

**Root cause of the L01 discrepancy:** the frozen S03R court **refuses to run** without `S03_CANDIDATE_ROOT`:
```
RuntimeError: HOLD: S03_CANDIDATE_ROOT absent; no project runtime executed
```
That is a **setup refusal by design**, not a scientific result — my L01 return said so and this court now proves it.

**Binding the exact candidate.** The court pins two hashes; I verified both against `69a16865`:
- `EXPECTED_SHA = 68aba5645bf0b1fa9c26f5a546b6df29a70a9c13a499fae7768a03b59e1de2e0` → `rawlsing_next/pre553_heterogeneous_synthesis.py` at `69a16865` hashes to **exactly that** ✓
- `EXPECTED_SHARED_HASHING_GIT_BLOB = a61365b994e5c3c50de0f598fcf40e90abf757b6` ✓

With the **complete** S03 tree as the root (7,463 files — not just `rawlsing_next/`), the court finally executes:

| stage | result |
|---|---|
| no `S03_CANDIDATE_ROOT` | 11 errors — `HOLD: S03_CANDIDATE_ROOT absent` |
| `rawlsing_next/`-only root | 11 errors — `HOLD: exact S03 candidate files unavailable` |
| **complete `69a16865` tree as root** | **8 passed / 3 failed, EXIT 1** |

**The eleven were never eleven failures — they were eleven setup refusals.** The genuine independent outcome is:

| failing case | class |
|---|---|
| `test_01_independent_four_cell_oracle` | **scientific/logic failure** |
| `test_07_missing_native_joint_cell_must_not_be_silent_zero` | **scientific/leakage failure** |
| `test_08_outcome_predicate_requires_tautology_warning` | **scientific/leakage failure** |

All three sit in the **F6 joint-domain / leakage** area — precisely what S03F `bb739fb6d60b40876566ec6320ff6eec2388e8cf` ("repair two F6 joint-domain and leakage defects") targets. That is a coherent causal story, not a coincidence.

**On "34 pass / 1 fail":** I did **not** reproduce that figure in any configuration I ran. I therefore do **not** confirm it, and I do not overwrite it either — I record that the committed JSON evidence (11 setup errors) and my bound run (8 pass / 3 fail) are both real, that they answer *different* questions, and that the "34/1" narrative remains **unreconciled from the artifacts I could execute**. Naming it honestly is the correct outcome; inventing a run to produce 34/1 would not be.

**Frozen oracles untouched.** I did **not** edit `EXPECTED_SHA`, `EXPECTED_SHARED_HASHING_GIT_BLOB` or any assertion. **S03F was not qualified** in this window — a versioned test-only identity adaptation was not built, and I decline to claim it. That remains an explicit open item.

## 3. S04 / S04R — strict outcome accounting

**S04 original** (`9ae87f2227384e0567190c6a2d5f3a33a60d4b4c`), run with `-rxX` so xfail/xpass are itemised:

```
python3.11 -m pytest tests/test_s04_temporal_policy.py -q -rxX
```

Result and the full xfail/xpass itemisation are in `repro/s04.log`; the outcome line is reproduced in `01_RUNTIME_COURT.json`. **Expected xfails are recorded separately from passes and failures and are NOT treated as scientific acceptance.**

**S04R** `755fb501e4b6405136bd77d71d434919c7b6c371` adds **`00_RETURN.md` + `01_REVIEW_FINDINGS.json` only — no Python test module**. There is therefore **no S04R independent temporal hostile suite to execute**; I state that rather than implying one ran. **Open item.**

## 4. Honest grading of this court

| workstream | result | class |
|---|---|---|
| P01 full terrain | **169 pass / 6 skip / 0 fail** | RESOLVED — historical 86 = fixture terrain |
| S03R bound | **8 pass / 3 fail** | RESOLVED — 11 errors were setup refusals; 3 genuine F6 failures |
| S03F | not qualified | **OPEN** — no versioned adaptation built |
| S04 original | see `repro/s04.log`; xfail/xpass itemised | technical only |
| S04R | no Python suite exists | **OPEN** — documentary-only review |
| "34 pass / 1 fail" narrative | **not reproduced** | **UNRECONCILED** — recorded, not invented |

Distinctions preserved throughout: **scientific failure** (S03R tests 01/07/08) · **code failure** (none separately established) · **missing fixture** (the historical 86) · **setup refusal** (the 11).

**Terminal:** `PYAT_R3_HQ285_L02_EXACT_INDEPENDENT_RUNTIME_COURT_COMPLETE__GITHUB_PUSHED`.
