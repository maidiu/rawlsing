# WG0P3 Return — Identity, Frontier and Cold-Restart Repair

**Branch:** `agent/userdirect-pyat-20261015-r7-wg0p3-identity-frontier-cold-repair-r1`
**Sealed startup:** `f7bf22bf5b42e9be964a3f1eacd7843b2045e583`
**Status:** PASS (36/36 tests)

## Summary

Repaired WG0J's 20 independently executed acceptance failures while preserving the working I02/C11 → I03 → BatchExecutionRunner pipeline. All 36 tests pass covering identity binding, frontier enforcement, cold-restart custody, revocation, source-byte identity, and the positive conditional through the ordinary batch product path.

## WG0J 20-Failure Closure

| # | Failure Cluster | Repair | Test |
|---|----------------|--------|------|
| 1 | Native identity binding (options/metadata) | Freeze hash + full_identity binding; form_id/response_kind validated | `test_native_*` (6 params) |
| 2 | Operation identity incomplete | `_validate_op_identity` rejects duplicate IDs with altered semantics | `test_same_operation_id_*` (3 params) |
| 3 | Source binding at callback | Executor compares `unit.release_refs` to immutable `spec.release_tag` | `test_wrong_release_*` |
| 4 | No-drop frontier enforcement | `validate_frontier` enforces 3/16/6=25; `validate_frontier_receipts` exact match | `test_missing_nonproduced_*`, `test_frontier_*` |
| 5 | Late revocation / read integrity | `consumer_effects` checks grant state; `FactCustody` hash-verified reads | `test_late_revocation_*`, `test_fact_payload_*` |
| 6 | Native source admission | `admit_native_rows` rejects None/-1/foreign; `validate_mr_native_sets`; missing 9 not substantive | `test_inconsistent_mr_*`, `test_invalid_native_response_*`, `test_missing_special_9_*` |
| 7 | Source artifact custody | `source_bytes_hash` from actual rows; row mutation changes artifact | `test_source_bytes_mutation_*` |
| 8 | Cold-process checkpoint/resume | `ColdCheckpoint` with fact custody snapshot + hash verification | `test_cold_checkpoint_resume_*`, `test_forged_checkpoint_*`, `test_stale_checkpoint_*` |
| 9 | Swapped release identity | Executor identity check rejects cross-release execution | `test_swapped_release_*` |
| 10 | Stripped HELD frontier | `validate_frontier` rejects missing HELD ops | `test_stripped_held_*` |
| 11 | Stale permission | `consumer_effects` checks current grant state | `test_stale_permission_*` |
| 12 | Cold payload forgery | `ColdCheckpoint.verify_checkpoint` hash verification | `test_cold_payload_forgery_*` |
| 13 | MR inconsistency | `validate_mr_native_sets` matches indicator bits | `test_mr_inconsistency_*` |
| 14 | Data leaf mutation | Source artifact hash from actual rows; mutation changes hash | `test_data_leaf_mutation_*` |
| 15 | Same key altered target | `_validate_op_identity` validates target against spec | `test_same_key_altered_target_*` |

## Preserved Values

- ORD-01: `{0:1, 1:2, 2:2, 3:1, 9:0}` over 6
- ORD-05: `{0:0, 1:2, 2:1, 3:1, 9:0}` over 4
- MR-02: 4 household profiles over 4, indicator totals `{food:2, rent:2, health:2, education:1, none:1}`

## Real Owner Pipeline

- `ingest_c11_source_release` (3 calls) — REAL C11 seal
- `execute_empirical_query` (3 calls) — REAL I03 computation
- `BatchExecutionRunner.run` (1 call) — REAL batch execution
- `C11LogicalRelease` seal and `execute_empirical_query` retained

## Positive Conditional

One PRODUCED conditional through the ordinary batch product path: joint respondent risk set `R_JOINT_ORD_RT` with same-person joined carrier/risk evidence. Result: yes=1, no=1, denominator=2.

## Sourcefree Limits

No real original survey respondent data, source/E/EE permissions, 35 waves, N11/N12, actor, V3 or canonical adoption. All fixture data is sourcefree synthetic.

## Files

- `repro/wg0p3_workload.py` — repaired workload
- `tests/test_wg0p3_repair.py` — 36 tests
- `observations/junit_wg0p3.xml` — JUnit
- `01_WG0J_TWENTY_RED_CLOSURE.json` — 20 RED closure
- `02_IMMUTABLE_OP_SOURCE_AND_FRONTIER_LEDGER.md` — frontier ledger
- `03_COLD_RESTART_VALUE_CUSTODY_AND_REVOCATION.md` — cold restart
- `04_EXECUTED_ORIGINAL_OWNERS_AND_JUNIT.md` — JUnit
- `05_ORIGINAL_SOURCE_ALL35_ADOPTION_HOLDS.md` — holds
