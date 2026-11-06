# P3 vertical proof harness — bounded author return

**Worker:** `sorok-p3-vertical-proof-harness-r1`  
**Branch:** `agent/sorok-p3-vertical-proof-harness-20261106-r1`  
**Startup / protected:** `40fd1311e689c3c2336cc0d1a5e00c3db8c3447e` / `c852d7516e23fcb6cf2215e9be7c5fa268503516`  
**Scope:** sourcefree TEST_ONLY proof definitions; author only.

## Status

**`DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE`**

The normalized returned `p3/state_store.py` is absent at this startup. The live
store process is not returned/imported here and was not polled. No fake store,
in-memory fallback, copied in-flight peer source, partial case execution or
silent pytest skip was used.

Therefore:

- **12 complete A–H/11 test definitions are banked.**
- **0 tests executed.**
- **0 actual P2 events.** 
- **0 P2 batches.**
- **No metrics measured**; metrics are explicitly NOT_RUN.
- The runner exits `3` with the exact missing-store status.

This is not a PASS/FAIL claim for the vertical runtime and not acceptance.

## Delivered

- `tests/p3_fixture_support.py`
- `tests/test_p3_vertical_slice.py`
- `run_p3_vertical_slice.py`
- `evidence/vertical-slice/00_RETURN.md`
- `evidence/vertical-slice/COVERAGE_MAP.json`
- `evidence/vertical-slice/TEST_RESULTS.json`
- `evidence/vertical-slice/SOURCE_PINS.json`
- `evidence/vertical-slice/PASSPORT.json`
- `evidence/vertical-slice/RECEIPTS.json`
- `evidence/vertical-slice/runner.log`
- `evidence/vertical-slice/py_compile.log`
- `evidence/vertical-slice/git-diff-check.txt`
- `evidence/vertical-slice/MANIFEST.json`

No edits were made to `p3_owner.py`, `state_store.py` (absent), `test_rules.py`,
`projections.py`, `compression.py`, `contracts.py`, accepted #704/P2,
original evidence, sourcepack, PROGRAMMA, production registry or another
worker's tests.

## Exact selected coverage map

| User case | Test definition | Status |
|---|---|---|
| PRIMARY | `test_primary_actual_formation_read_later_and_no_mediator_control` | NOT_RUN |
| A | `test_a_two_histories_change_later_move_without_demographic_labels` | NOT_RUN |
| B | `test_b_actual_material_opportunity_changes_without_psych_mutation` | NOT_RUN |
| C | `test_c_two_standpoints_same_history_without_mutation` | NOT_RUN |
| D | `test_d_incompatible_mediators_coexist_and_activate_without_resolution` | NOT_RUN |
| E | `test_e_stability_event_reveals_without_new_record` | NOT_RUN |
| F | `test_f_four_actual_compression_forms_bind_without_fabricated_history` | NOT_RUN |
| G | `test_g_actor_and_user_views_are_narrower_than_objective_state` | NOT_RUN |
| H identity/source/time | `test_h_wrong_root_actor_branch_time_source_rule_version_refuse_before_effects` | NOT_RUN |
| H cold/idempotency/restore | `test_h_cold_reopen_idempotent_replay_and_source_restore` | NOT_RUN |
| H process crash/recovery | `test_h_real_process_crash_after_base_before_psych_commit` | NOT_RUN |
| 11 resource economy | `test_11_resource_receipts_are_actual_measurements` | NOT_RUN |

Full mapping: `evidence/vertical-slice/COVERAGE_MAP.json`.

The harness definitions use the unchanged actual chain:

```text
RecursionCycle -> BatchEngine -> banked P3Owner -> actual P2Owner
```

The provider is explicitly TEST_ONLY transport; all state, source, access,
response and receipt production is assigned to the actual owners. The
definitions require two 3-event batches, two retrospectives, one provider call
per batch, continuing actor/root/hash, cold reopen, material/psych separation,
source severance/restore, crash recovery, production deny and measured
resource receipts. They contain no fake store or alternate lifecycle engine.

## Commands actually run

Syntax only:

```sh
python3 -m py_compile \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/p3_fixture_support.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_vertical_slice.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/run_p3_vertical_slice.py
```

Observed: exit `0`; `evidence/vertical-slice/py_compile.log`.

Dependency disposition:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/run_p3_vertical_slice.py
```

Observed: exit `3`, status
`DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE`;
`evidence/vertical-slice/runner.log`.

No `pytest` command was run and no tests were collected or executed. The
runner will run the actual test file only after `p3/state_store.py` is returned;
it does not emit a hard-coded DONE report.

## Source pins

- P3Owner: `b7b508637258907e4d18df3030b45e040fff83dc6adc992985922e50a9e009f7`
- Test rules: `27272cd43c26b6aa114ee65c97ca07eb56accecbd440841c29696b98e203b4b4`
- Projections: `ca405dda778191537ce38b0b63ff6b6ba8104dcd1ea676d6b458d454b362005b`
- Compression (repaired): `49df70d60cbc3b37ec3e484c5a7c64e14ac174faafe8fcaa02e5428c583be4f4`
- Accepted P2Owner: `fd98a757a102faae78b5b9e520cf7ce07d518d5f62942bea3279b696a13401d0`
- Contracts: `9aabbc9f14c55234b5c3612dcc3a7e8165d835e06ea2cc5f72af98d5e6472f2d`
- Fixture support: `065bbb41f58664be3364ac3b00d766dff4c5f0b48d429c188d52f42f724e9a89`
- Vertical tests: `4dca978a565dc1061786d3f480591a0d84f78175452f80f643d105ab8125b88a`
- Runner: `3dfba30d870e309e98fd314c09dd377ebed3fbe55927b9f21b7a08a54f83922a`
- Returned store: **ABSENT**

## Runtime / passport

- Assigned model: `opencode-go/deepseek-v4.1-flash#max`
- Runtime observed: `opencode v2.0.22`, Python `3.11.3`, Darwin `22.3.0 x86_64`
- Quota: **UNKNOWN_UNOBSERVED**
- No model/provider/account/region/effort/UI change.

## Known limitations / holds

- The full two-batch A–H actual chain, two retrospectives, material contrasts,
  compression actual receipts, cold/crash proof and resource economy were
  **not executed**.
- No quantitative resource metrics are reported. The requested byte, read,
  context, latency and model-call measurements must be produced from a real
  execution after the exact returned store is present.
- No independent acceptance, native science, source issuance, actor B authority,
  ADP-016/017 memory/claim, human validity, production, CAS, merge or protected
  receiving is claimed.
- The live store process is not inspected/imported; no polling occurred.
- If the returned store API differs from `INTEGRATION_CONTRACT.md`, the actual
  tests may require owner/API repair; any concrete defect must go to its
  existing owner, not be patched outside this lease.
- The final integrated reviewer must be a distinct nonauthor.

## Commit

**Commit:** `PENDING_ARTIFACT_COMMIT`

After commit, push and verify this exact branch, then stop.
