# CGA-COLD-LATER-READ — executed cold/later owner witness

**Obligation:** `CGA-COLD-LATER-READ`
**Result:** `PASS_S2_AT_SOURCE_EQUIVALENT_CUT`
**Frozen positive oracle:** owner-held formation records survive cold reopen and a later distinct decision consumes their exact hashes; a no-record control differs; source removal refuses and exact restore resumes.
**Frozen negative court:** wrong identity, cross-root, stale clock, partial rollout, crash and `MISSING_RULE` preservation are exercised by the recorded tests.

## 1. Required command

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests
```

Observed: **71 passed in 278.95 s** (`evidence/engine71.log`).

This full engine suite includes the cold/retry, provider custody, material/C9, chronology, duplicate-effect, `MISSING_RULE`, and wrong-identity courts. It is the inherited accepted engine suite, not a new broad claim.

## 2. Direct cold-later witness

New author test: `tests/test_cold_later_recruit.py`.

Sequence:

1. `build_case` creates an actual P2 root and the banked P3 owner/store at TEST_ONLY grade.
2. `bootstrap` realizes three events; the formation event writes two `V3MS_MEDIATOR` records.
3. The author queries the store and records the exact two hashes.
4. `case.owner.close()` closes the P3 store and P2 session.
5. `reopen_owner` opens the same P2 root and the same P3 sidecar on the same root/actor/branch/clock lineage.
6. A new `BatchEngine` and `RecursionCycle` read the same journal/cycle store.
7. `advance` produces a later recruit. Its response streams are exactly the two formation hashes; its `readset` intersects them.
8. The recruit response is `NOT_ISSUED_BY_P3_RULE`; no new record is fabricated.
9. `finish` completes the terminal retrospective; the store head remains two records.

Observed: **1 passed in 247.70 s** (`evidence/cga_cold_later.log`).

This is the direct S2 positive: the exact owner-held state is reopened cold and later consumed by a distinct decision.

## 3. Existing owner cold/replay/source-restore witness

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore'
```

Observed: **1 passed in 280.92 s** (`evidence/p3_owner_cold.log`).

It covers exact owner reopen, idempotent replay, and source severance/restore at the same P3 owner boundary.

## 4. Existing formation→later-response/control witness

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control'
```

Observed: **1 passed in 445.72 s** (`evidence/p3_primary.log`).

It proves the sourcefree formation records condition a later recruit response, while the no-mediator control chooses `inspect_alone`; the control store head remains zero. It is not itself a cold test; the cold-later test above adds the restart.

## 5. Material and C9 later reader

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_recursion_integration.py \
  -k 'material_antecedent or actual_material_effect'
```

Observed: **2 passed in 260.26 s** (`evidence/engine_material_cold.log`).

`test_material_antecedent_changes_later_native_c9_result` proves ACTUAL versus SCHEDULED_ONLY interval participation changes the later native C9 result. `test_actual_material_effect_reaches_c9_and_owner_receipt_survives_reopen` covers cold owner receipt survival.

## 6. Store-level later read and source binding

New author test: `tests/test_selected_common_readset.py`.

Observed: **3 passed in 0.10 s** (`evidence/cga_common_readset.log`).

It writes a home-period record through `PsycheStore`, closes, reopens, and a later `ENTER_KITCHEN` decision consumes the exact record hash. The same root with a different actor returns `HOLD_NO_QUALIFIED_HOME`; `as_of` before `effective_from` returns HOLD; reopening with a removed source hash or wrong root refuses; exact replay remains COMPLETE.

This is a store-level proof of the selected common readset, not a substitute for the owner-level cold-later test.

## 7. Negative court

```bash
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  -k 'wrong_root_actor_branch_time_source_rule_version or cross_root_binding or real_process_crash'
```

Observed: **3 passed in 14.03 s** (`evidence/p3_negatives.log`).

The full store/rules command also passed 57 tests in 0.63 s, including:

- `test_reopen_rejects_wrong_binding_registry_source_and_schema`
- `test_reserve_reuse_mismatch_stale_head_and_bad_plans`
- `test_one_bad_target_rolls_back_all_records`
- `test_bad_record_targets_do_not_mutate`
- `test_contradictory_records_coexist_and_cas_refuses_stale_commit`
- `test_record_json_tamper_is_detected_by_query_and_verify`
- `test_operation_phase_and_result_tamper_is_detected`
- `test_cold_reopen_preserves_head_records_operations_and_pending`

The full engine suite additionally covers held/MISSING_RULE preservation, ambiguous retry, interrupted progress, duplicate-effect prevention, provider mutation refusal, and wrong source/clock/state.

## 8. NOT_RUN

- Full P3 A–H vertical matrix (13 cases): only the primary, cold/replay, wrong-identity/cross-root/crash, and store-level commands above were run. The all-case matrix was not rerun.
- Full P3 115-test suite: not run.
- P6 speech/cold/independent-mother tests: no such current adapter exists; not run.
- Actual C9/E2 performed action after a P3 response: not run; P3 response is `NOT_ISSUED_BY_P3_RULE`.
- Native CAN/ADP/Pyat issuance: not run and not authorized.
- Browser or GitHub CI: not used; remote returned 403/404.
- PR checks and reviews #874/#908/#860/#889/#914: inaccessible; untouched.

## 9. Verdict

`PASS_S2` for the frozen positive oracle at the source-equivalent cut: exact owner-held formation survives a cold close/reopen and is consumed by a later distinct recruit, with control and source-severance behavior. `PASS` for the selected store-level later read. `HOLD` for the multi-actor/home-period/mother-speech extensions and for the literal declared startup identity.
