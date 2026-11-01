# TEST EXECUTION AND FAULT WITNESSES

## Environment

- Host: `mainMac`, macOS 13.2.1 (22D68), x86_64.
- Python 3.11.3, pytest 9.0.2, OpenCode 1.18.34.
- Model surface: `opencode-go/deepseek-v4.1-flash`, local variant `max`; no provider-side MAX attestation.
- All runs: `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.`, `-p no:cacheprovider`.
- No raw survey, native source, original U/E_pre, actor, Field Forge, CAN/ADP, N11/N12, C1/C11 or model-use execution.

## S06G historical candidate

Source tip `0ff13995cc55db00d02b08004e62f75d4c5cb36e`; lifecycle blob `dadf2362f3195c28ebaf97655e28cdba72c04fb3`; release blob `1cb7692399aad8fb272c8c9ce956719527829007`; test blob `23aaf95d315980ea7587373e30188c7f36cb2b73`; historic S06FR review `1b5b6072f855a74864c82d0f1b3923327bfb8b99`.

Exact command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_s06f_native_owner_security.py \
  rawlsing_next/tests/test_pre553_learned_product_lifecycle.py \
  rawlsing_next/tests/test_pre553_learned_product_release.py \
  rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py \
  rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py \
  rawlsing_next/tests/test_pre553_learned_world_composition.py \
  WORKER_RETURNS/PYAT-R3-HQ285-S06G-NATIVE-ATOMIC-INTEGRITY-REPAIR-R1/repro/reviewer_overlay/test_hq284_s06fr_native_review.py
```

**Result: 187 passed, 14 failed, exit 1; no skips, errors or xfails.** Per-suite:

| Suite | Passed | Failed |
|---|---:|---:|
| S06F native authored | 18 | 0 |
| Accepted B5 | 39 | 0 |
| Accepted M2, unchanged | 26 | 2 |
| New S06G repair court | 42 | 0 |
| Exact S06FR reviewer overlay, unchanged | 17 | 12 |
| Adjacent integration (EE14 current/as-of + world composition) | 45 | 0 |

The 14 failures are **not** a green pass and are not hidden:

- **12** are the unchanged S06FR `OBSERVED` defect-presence assertions. They fail because the defect each one demonstrated is no longer present. Exact failure exceptions are in `DEFECT_BY_DEFECT_VERDICTS.jsonl`; the key witnesses are:
  - direct saved B5 `_append_events` now raises `EXTERNAL_ISSUER_HOLD` (old test expected acceptance);
  - direct saved M2 `_insert` now raises `EXTERNAL_ISSUER_HOLD` (old test expected acceptance);
  - rehashed publication `replay_root_ref`, `determinant_set_hash` and `producer_permission_ceiling` now raise checkpoint semantic-replay conflict (old test expected acceptance);
  - torn publish now rolls back to `PRODUCT_REGISTERED` (old test expected torn `PRODUCT_PUBLISHED`/`UNPUBLISHED`);
  - direct M2 `_insert` race now raises `INTERNAL_MUTATION_OUTSIDE_TRANSACTION` (old test expected two writers);
  - concurrent selection barrier now breaks because the second caller cannot enter the locked check (old test expected two receipts);
  - public event payload mutation now raises `TypeError: 'mappingproxy' object does not support item assignment` (old test expected ref drift);
  - cross-release rebuild receipt now raises checkpoint receipt/state conflict (old test expected acceptance).
- **2** are unchanged accepted M2 tests: `test_17_binding_cannot_resolve_different_release` and `test_18_endpoint_failover_only_among_same_release`. They fail at `RELEASE_UNAVAILABLE` because their setup inserts a foreign binding into a repository without lawfully registering the foreign release; S06G raises earlier. This is a **fixture compatibility regression at the accepted test contract**, not a permissive-resolution regression. The new reconciled cases first assert the early refusal, then lawfully register the foreign release/representation and preserve the original `PUBLICATION_BINDING_MISMATCH` oracle.

The S06G return’s `187 passed / 14 deselected` selection is a separate selection, not a green unfiltered court. It excludes exactly the 12 obsolete defect-presence assertions and the 2 accepted M2 fixture setups. This reviewer did not edit any frozen reviewer test or accepted test.

## Independent E2 hostile tests (fresh, written by this reviewer)

File: `reviewer_tests/test_e2_independent_hostile.py` (10 tests).

Exact command against the **S06G candidate overlay on current PRE-MAIN**:

```sh
cd <temp-candidate-root>  # current PREMAIN rawlsing_next + S06G lifecycle/release + S06G/S06F tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT_RRIF_E2_S06G_HOSTILE_20261031_R1/reviewer_tests/test_e2_independent_hostile.py
```

**Result on candidate overlay: 10 passed.** The tests cover:
1. recursive nested payload freeze and detached export;
2. rehashed publication `replay_root_ref`, `determinant_set_hash`, `producer_permission_ceiling` refusal;
3. torn publish rollback + prior checkpoint cold restore;
4. concurrent selection one winner/one conflict + cold restore;
5. saved B5/M2 helper refusal outside an owner transaction;
6. cross-release rebuild receipt rehash refusal;
7. foreign M2 binding early refusal;
8. honest `LOCAL_UNAUTHENTICATED` / `EXTERNAL_ISSUER_HOLD` downgrade.

The same 10 tests against **current unpatched PRE-MAIN**:

```sh
cd <current-PREMAIN-worktree>
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/PYAT_RRIF_E2_S06G_HOSTILE_20261031_R1/reviewer_tests/test_e2_independent_hostile.py
```

**Result on current: 10 failed** (one per test; no skips). This is direct differential evidence that current lacks the S06G repairs at the tested grain: current permits the nested payload mutation/identity drift, accepts rehashed publication/rebuild substitutions, leaves the torn state, allows the direct helper path, and has no `native_security_mode`/`require_external_issuer` API.

## Current-vs-candidate compatibility checks

| Check | Current PRE-MAIN | S06G candidate overlay |
|---|---|---|
| Accepted B5 tests | 39 passed | 39 passed |
| Accepted M2 tests | 28 passed | 26 passed / 2 failed (fixture early refusal) |
| EE14 current/as-of + world composition | 45 passed | 45 passed |
| Independent E2 hostile tests | 10 failed | 10 passed |
| S06G new repair court | n/a (test module absent) | 42 passed |
| S06FR overlay | not runnable on current (S06F test helper absent; reviewer overlay needs S06F) | 17 passed / 12 obsolete-failure |

The S06G production owner files can be overlaid onto current without breaking the 45 adjacent integration tests or the accepted B5 court. The observed production-level regression is limited to the two accepted M2 fixture setups, which call `register_binding` with a foreign release not registered in the repository. The S06G test module also depends on `rawlsing_next/tests/test_pre553_s06f_native_owner_security.py`, which is absent from current; a separate engineer must port/adapt that helper or rewrite the test fixtures.

## Fault-witness integrity

- Exact S06FR overlay bytes were used from S06G’s own return copy; its Git blob `a25cf5a5ecec4b473ccceaec8a032747d804da7d` equals the historic S06FR test blob at `1b5b6072`. It was not edited.
- The 12 old defect assertions were neither deleted nor rewritten.
- No test was xfailed, skipped or deselected in the reported 187/14 run.
- The two accepted M2 tests were not edited.
- The 10 independent E2 tests are new and are the reviewer’s own expectations.
