# CGA-COLD-LATER-READ evidence

## Commands and outputs

All commands ran from the isolated worktree at `2be0cf25`.

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests
RESULT   71 passed in 278.95s
LOG      evidence/engine71.log
```

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-CG-A-OWNER-REUSE-R1/tests/test_cold_later_recruit.py
RESULT   1 passed in 247.70s
LOG      evidence/cga_cold_later.log
```

The test asserts, in order:

```text
len(formed) == 2
response_for(formation)["status"] == "COMPUTED_TEST_ONLY_RESPONSE"
stream_hashes == formed_hashes
set(recruit["readset"]) & formed_hashes != empty
response["native_action"] == "NOT_ISSUED_BY_P3_RULE"
final["batch_id"] == second["batch_id"]
owner.store.head()["count"] == 2
```

The cold close/reopen occurs between the formation batch and the later recruit. The reopened owner is constructed by `reopen_owner` from the same `state_root`; the journal and cycle store paths are the same; the provider is the same scripted provider.

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider 'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_h_cold_reopen_idempotent_replay_and_source_restore'
RESULT   1 passed in 280.92s
LOG      evidence/p3_owner_cold.log
```

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider 'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py::test_primary_actual_formation_read_later_and_no_mediator_control'
RESULT   1 passed in 445.72s
LOG      evidence/p3_primary.log
```

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py -k 'wrong_root_actor_branch_time_source_rule_version or cross_root_binding or real_process_crash'
RESULT   3 passed in 14.03s
LOG      evidence/p3_negatives.log
```

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py
RESULT   57 passed in 0.63s
LOG      evidence/p3_store_rules.log
```

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-CG-A-OWNER-REUSE-R1/tests/test_selected_common_readset.py
RESULT   3 passed in 0.10s
LOG      evidence/cga_common_readset.log
```

```text
COMMAND  python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_recursion_integration.py -k 'material_antecedent or actual_material_effect'
RESULT   2 passed in 260.26s
LOG      evidence/engine_material_cold.log
```

## Source severance

- `tests/test_rules.py::test_wrong_version_and_exact_source_severance_refuse_and_restore` mutates the B1 source, receives `B1_SOURCE_SEVERED`, restores exact bytes, and then receives the expected `joint_check` record. It is part of the 57-passed command.
- `test_h_cold_reopen_idempotent_replay_and_source_restore` preserves exact owner state through cold reopen, refuses the altered source, and restores it. It is the 1-passed P3 owner command.

## NOT_RUN

```text
full 13-case P3 A-H matrix
full 115-test P3 suite
P6 mother/speech adapter (absent)
actual C9/E2 performed action after P3 response
native CAN/ADP/Pyat issuance
browser execution
GitHub PR/CI and reviews #874 #908 #860 #889 #914 (remote 403/404)
```
