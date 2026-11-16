# P3 owner actual-store repair — bounded return

## Status

**BOUNDED OWNER REPAIR BANKED; ACTUAL STORE ABI STILL BLOCKS FULL POSITIVE.**

This turn repairs the actual process-reopen/crash fixture and executes the
owner tests against the returned normalized store. The returned store is
present, but its current `PLAN_AUTHORITY_OR_GRADE_MISSING` check still refuses
the frozen actual owner plans before any base effect. Storage and rule/kind
repair belong to the separate store-author return; this return does not patch,
bypass, wrap or replace that store.

This is not full owner acceptance, not independent review and not proof that
the six durable cases all pass.

## Exact source and scope

- Worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-recursion-reuse-r1`
- Integrated startup: `8cc2914b1089cfc113ae1737941bd2a9efde622b`
- Branch: `agent/sorok-p3-owner-actual-store-repair-20261106-r1`
- Protected base: `c852d7516e23fcb6cf2215e9be7c5fa268503516`
- Returned store intake: `38f04ed627de40258724e006bf227a104bba9300`
  (`STORE_INPUT_DISPOSITION.json`; mechanical store suite reported 42 passed)
- Store code hash used:
  `40b29d96c359de61fcb62937c08f7cdb73cd68b936247ef2e9219348119586a0`
- Owner code hash used:
  `b7b508637258907e4d18df3030b45e040fff83dc6adc992985922e50a9e009f7`
- Owner test hash:
  `4f627eba7ae61a8a670523f1e8ac612c14207649b21b4d93545405827475d660`

Exclusive writes in this repair:

- `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py`
- `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/evidence/owner-actual-store-repair/`

`p3/p3_owner.py`, `p3/state_store.py`, and the prior `evidence/owner/`
directory were not edited. The prior owner evidence remains byte-identical
(`git diff` against startup for `evidence/owner` is empty).

## Independently actionable defect repaired

The child process previously called `load_p2().start(...)` on an already
frozen actual P2 root, and depended on an inherited module path. The observed
failure was `S44_ROOT_ALREADY_FROZEN` (with the earlier build also producing
`ModuleNotFoundError developmental_recursion` before reaching the intended
crash boundary).

The test now:

- adds repository-relative P3, engine and repository roots to the child
  `sys.path` and `PYTHONPATH`;
- opens the exact existing root with `P2ProductFanin.open`, never `.start`;
- asserts the child's `state_root`, frozen root hash and exact initial
  `StateSnapshot` match the parent's persisted actual P2 root;
- closes the parent's P2 handle before the cold child;
- retains the actual `P3Owner` realization path and the intended
  after-base-effect `os._exit(17)` boundary.

The new actual probe `test_process_reopens_same_actual_p2_root` passed:
the child opened the same persisted actual P2 root, asserted the same root hash
and initial state, and the parent reopened the same root/state afterward. The
probe log is `ROOT_REOPEN_PROBE.txt`.

## Executed actual results

Command:

```text
PYTHONPATH=WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1:WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1 \
python3 -m pytest -q -rs \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  -p no:cacheprovider
```

Observed: **4 passed, 4 failed, 1 skipped in 16.75s**
(`TEST_LOG_ACTUAL.txt`).

Passed:

- `test_non_test_only_refuses_before_base_or_store_access`
- `test_process_reopens_same_actual_p2_root`
- `test_actual_p2_root_configuration_and_combined_statehash`
- `test_wrong_source_rule_version_and_config_change_refuse_before_new_effects`

Skipped explicitly by the existing checker because the returned store is now
present:

- `test_missing_returned_store_is_explicit_not_a_fallback`

Failed, all at the returned store's
`PLAN_AUTHORITY_OR_GRADE_MISSING`:

- `test_formation_stored_records_pure_views_and_later_response`
- `test_later_no_mediator_control_uses_inspect_alone`
- `test_idempotent_replay_and_reopened_owner_return_immutable_result`
- `test_real_subprocess_crash_boundary_recovers_prepared_base`

The crash child now gets past import, `.open`, root/state assertion and
`P3Owner` construction. It fails at `P3Owner.realize -> store.reserve ->
store._plan_authority` with
`PLAN_AUTHORITY_OR_GRADE_MISSING`; therefore it does **not** yet reach the
intended post-base-effect kill, and no recovery completion is claimed. The
full failure trace is preserved in `TEST_LOG_ACTUAL.txt`; the log contains no
`ModuleNotFoundError` and no `S44_ROOT_ALREADY_FROZEN`.

`python3 -m py_compile` of the changed test file passed.

## Remaining dependency and exact limits

Required before resuming this same task:

1. The separately owned store repair must accept the frozen actual owner plan
   grade `SOURCEFREE_TEST_ONLY` without a redundant authority field, while
   retaining conflicting/native/production denial.
2. The separately owned store repair must preserve exact `V3MS_MEDIATOR`
   kind/hash spellings losslessly.
3. Then rerun this owner file against the exact integrated store; all six
   durable cases must genuinely execute, including the actual PREPARED ->
   base effect -> cold kill/recovery path. Only then can this owner return be
   considered functionally exercised.

Still not demonstrated/claimed: full positive owner chain, all original six
durable cases, cold/crash completion, native psychology, compression positive,
ADP016/017 memory or claims, independent review, acceptance, merge or
production authority. No fake store, fallback, alternative engine, silent
assertion weakening or peer in-flight import was used.

## Next action

HQ/store owner merges the exact storage ABI/kind repair, then resumes this same
session/branch to rerun the owner tests and execute the actual crash recovery.
