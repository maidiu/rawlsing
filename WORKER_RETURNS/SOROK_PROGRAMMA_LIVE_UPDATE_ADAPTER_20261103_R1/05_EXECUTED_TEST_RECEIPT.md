# SOROK-LIVE-02-R1 — executed test receipt

**Status: `EXECUTION_VERIFIED__READY_FOR_INDEPENDENT_REVIEW` for the scoped sourcefree adapter. Independent review and HQ adoption remain NOT ISSUED. This receipt reports machine execution, not independent acceptance.**

## 1. Exact revision and environment

| Item | Value |
|---|---|
| Private repository | `maidiu/rawlsing` |
| Worker branch | `agent/sorok-programma-live-update-adapter-20261103-r1` |
| Starting SHA (verified HEAD at launch) | `fe7b7c32bfe8aa508f556af649628930c12d9210` |
| Original base | `fa8a2b1f75cd2ee2153a813215f51dea88e16a4b` |
| Frozen W8-R guide | `a9ebf71e62d84e5dcc599662e976eca7fcd0e623` |
| Execution content SHA (C1) | `bbcc46bf3b7aadfc582e284daea61f99060e0fc3` |
| C1 parent | `fe7b7c32bfe8aa508f556af649628930c12d9210` |
| Python | `3.11.3` |
| pytest | `9.1.1` |
| Host | Darwin 22.6.0 x86_64 (`oldMac.lan`) |
| Test worktree | `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/live02-r1-fe7b7c32` |
| Package directory | `SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1` |
| Bytecode policy | `PYTHONDONTWRITEBYTECODE=1` |
| Working tree at C1 test time | clean (`git status --porcelain` empty) |

The exact source commits required by the tests were present in the local object database before execution:

```text
a9ebf71e62d84e5dcc599662e976eca7fcd0e623 commit
7bf2da302996491ddf34b9a039fea47ac982d135 commit
4387dc818a96fda2d5271672505fbd9da1059703 commit
b65c75a9e62618690f7d02265bc9e850af549161 commit
598d9e9eaba5143950c63317705fd09104fbf463 commit
8090a1ea308ab17f302f55bb2639c3e4cd774c7a commit
```

## 2. Exact commands

```sh
cd /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/live02-r1-fe7b7c32/SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1

PYTHONDONTWRITEBYTECODE=1 python3 -m pytest --collect-only -q test_live_update_adapter.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q test_live_update_adapter.py
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q test_living_reference.py test_living_reference_r2.py test_p0_trust_repair.py test_p1_whole_program.py test_repair_r1.py
```

Collection at C1:

```text
35 tests collected in 0.11s
```

## 3. Results at C1

| Suite | Collected / cases | Passed | Failed | Skipped | Errors | Wall time |
|---|---:|---:|---:|---:|---:|---:|
| `test_live_update_adapter.py` | 35 | **35** | 0 | 0 | 0 | 442.32 s |
| P0/P1 regression (`test_living_reference.py`, `test_living_reference_r2.py`, `test_p0_trust_repair.py`, `test_p1_whole_program.py`, `test_repair_r1.py`) | 62 | **62** | 0 | 0 | 0 | 270.59 s |

Raw output:

```text
...................................                                      [100%]
35 passed in 442.32s (0:07:22)
..............................................................           [100%]
62 passed in 270.59s (0:04:30)
```

The committed raw files are `cold_replay/14_committed_live02_pytest.txt` and `cold_replay/15_committed_regression_pytest.txt`.

## 4. Test-function count versus case count

The module contains **25 test functions**. `test_forgery_and_cross_cut_refusals_do_not_append` is parameterized with 11 cases, producing **35 collected cases**. The previously authored module contained **15 functions / 25 cases**; this repair added **10 functions / 10 cases**. The count distinction is explicit and is not a claim that 35 independent functions were written.

The previously authored 15 functions and their 25 cases were run at the starting SHA before mutation:

| Suite at `fe7b7c32...` | Passed | Failed | Skipped | Errors | Wall time |
|---|---:|---:|---:|---:|---:|
| `test_live_update_adapter.py` (25 authored cases) | **25** | 0 | 0 | 0 | 361.25 s |
| P0/P1 regression (62 cases) | **62** | 0 | 0 | 0 | 343.74 s |

No pre-existing suite failure was observed. The authored suite nevertheless missed the source-binding and view-projection defects recorded in `07_ADVERSARIAL_FINDINGS_AND_REPAIRS.md`; those defects were demonstrated by the new tests failing on `fe7b7c32...`.

## 5. Source and test blob identities at C1

| File | Git blob at C1 |
|---|---|
| `live_update_adapter.py` | `10c82da192ccca62e140ba4efee32f1670d6995e` |
| `test_live_update_adapter.py` | `5e2f56d0bc80fac43f985cfbd2998ed722d1cfb1` |
| `living_reference.py` | `a1ee1dade4952cba5420f05b692dffb5aa78c7c1` |
| `fixtures/join_e_scoped_review.json` | `bd8c350aef36dfc5de8abd2830bb2b359b16f328` |
| `fixtures/s35_authored_sourcefree.json` | `f70f14acf7d88b76707095f1169dc616659884b8` |
| `fixtures/rrif_r2_negative.json` | `3661ce4daa99bc997ea8df9d60d3f51ae860a779` |

`living_reference.py` is unchanged from `fe7b7c32...` by this repair; only `live_update_adapter.py` and `test_live_update_adapter.py` changed.

## 6. Baseline defect reproduction

The first six new regression tests were copied into a detached worktree at `fe7b7c32...` and run against the pre-repair adapter. Result: **4 failed, 2 passed, 25 deselected**. The failure transcript is `cold_replay/17_baseline_defect_repro.txt`. The remaining four new tests were added after that baseline capture and pass at C1.

Three additional direct probes against the pre-repair adapter returned `ACCEPTED` for:

| Probe | Starting-SHA result |
|---|---|
| Same-cut but wrong source path (`joined/session.py` instead of the exact JOIN-E return record) | `SCOPED_SOURCEFREE_ACCEPTED` |
| RRIF review document used as the return source | `EXACT_NEGATIVE_REVIEWED` |
| RRIF negative attached to unrelated node `JOIN_E_7BF` | `EXACT_NEGATIVE_REVIEWED` |

The probe transcript is `cold_replay/18_baseline_defect_probe.json`.

## 7. Repair history and regression coverage

| Defect | Repair in C1 | Regression test | Post-repair evidence |
|---|---|---|---|
| `SCOPED_REVIEW` accepted a foreign real source commit while claiming the 7bf subject | `validate_delta` now requires `source.commit == subject_sha` (`SOURCE_COMMIT_SUBJECT_MISMATCH`) | `test_scoped_review_source_cut_must_equal_reviewed_subject` | PASS in the 35-case run |
| `SCOPED_REVIEW` accepted another file at the same 7bf cut | exact JOIN-E source path and JOIN-V review path binding | `test_scoped_review_source_path_must_be_exact_join_e_return` | PASS |
| `REVIEW_REVISE` accepted the review document as its own source and could attach to an unrelated existing node | exact RRIF source/review paths and `node_id == JOIN_C12_HOLD` binding | `test_negative_review_source_cut_and_node_are_exact`; `test_unsupported_negative_review_cut_is_refused` | PASS |
| `work-now` view omitted the reconstructed `programma_live` section | `query("work-now")` now returns `state["work_now"]["programma_live"]` | `test_seven_views_share_one_cold_reconstructed_state`; existing JOIN/S35 test assertion | PASS |
| Direct journal forgery and journal-layer duplicate collision were not exercised | fail-closed replay remains the rule; tests now exercise it | `test_direct_forged_delta_event_fails_closed_on_replay`; `test_direct_duplicate_transition_with_changed_payload_fails_closed` | PASS |
| Order independence covered only JOIN/S35 | three-event permutation added | `test_three_event_order_permutation_preserves_scoped_semantics` | PASS |
| Reviewer-transfer test used only a malformed SHA | real foreign review commit added | `test_real_foreign_reviewer_commit_is_not_transferable` | PASS |
| Forged source commit and quote were only partially covered | both exercised before append | `test_forged_source_commit_and_quote_are_refused_before_append` | PASS |

## 8. Source-grade boundary

The test suite verifies declared sourcefree behavior against exact Git objects, the frozen W8-R guide, the existing P0/P1 journal engine, cold replay, CAS, duplicate identity, withdrawal/restoration, negative-review isolation, and the seven read views. It does **not** create native science, owner adoption, human A5 evidence, an independent reviewer verdict, HQ adoption, a production daemon, or external custody. Passing tests are execution evidence only.

Independent review: **NOT ISSUED**. HQ adoption: **NOT ISSUED**.
