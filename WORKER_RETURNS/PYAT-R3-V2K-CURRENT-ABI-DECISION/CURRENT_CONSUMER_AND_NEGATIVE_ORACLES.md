# Current R61 consumer and negative oracles

**Current PRE-MAIN:** `87755f02ec5c37499b09e80db6fbdcc9316a6b15`. **Startup:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`.

## Current consumers

| Consumer | Exact role | Status |
|---|---|---|
| `rawlsing_next/pre553_issued_workload.py::admit` | Issuer/expected-work admission gate: resolver record, scope/currentness, host/purpose, source/science permissions, original/frontier roots, expected job multiset, source edition, full envelope hash, query/role direction, discovery refs. | Current retained contract |
| `rawlsing_next/pre553_issued_workload.py::execute_issued_workload` | Execution through C11 projection, Route B, I03/I05 and Batch after admission; no caller-rehashed prior receipts. | Current retained contract |
| `rawlsing_next/pre553_native_workload_binding.py::build_test_only_workload` | TEST_ONLY `NativeWorkload` + `IssuedWorkloadRecord` builder; descriptor/projection/request binding. | Current sourcefree first consumer |
| `rawlsing_next/pre553_native_workload_binding.py::execute_test_only_workload` | Calls `admit` then `execute_issued_workload` on the TEST_ONLY path. | Current sourcefree execution wrapper |
| `rawlsing_next/pre553_source_native_preimage_adapter.py` | `NativePreimageBundle` sourcefree preimage input. | Current retained sourcefree input |
| `rawlsing_next/pre553_source_backed_c11_facade.py::GovernedC11Projection` | Current source/universe/item/routing/response/weight projection. | Current retained source identity receiver |
| `rawlsing_next/pre553_universal_workload.py` | Universal operation compilation/execution; current alternative, not V2K ABI. | Current retained alternative |

No current consumer imports V2K `OriginalIdentity`, `OriginalExpectedWork`, `FrozenOriginalExpected`, `OwnerScopePlan`, `run_sourcefree`, `V2ExpectedWorkDeclaration`, `v2_bind_semantic_to_dispatch` or `v2_reconcile`.

## Current negative oracles actually run

`tests/test_current_r61_contract_negatives.py` uses the current `admit` / `execute_issued_workload` consumers with a sourcefree fake envelope/catalog/resolver. Result on current PRE-MAIN tree: **8 passed**, exit 0.

| Oracle | Current typed refusal |
|---|---|
| Baseline positive admission | accepted exact TEST_ONLY record |
| Foreign issuer / wrong decision ref | `CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED` |
| Removed held row / extra expected job | `EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH` |
| Mutated expected-work identity / envelope hash | `ENTIRE_EXECUTION_DESCRIPTOR_NOT_THE_ISSUED_ENVELOPE` |
| Wrong role / target-condition direction | `QUERY_TARGET_CONDITION_DIRECTION_MISMATCH` |
| Replay / prior caller receipts | `RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED` |
| Wrong source edition/source factory | `SOURCE_FACTORY_RETURNED_WRONG_EDITION` |
| Severed current resolver | resolver error is not laundered |

These are current-R61 negative checks, not historical V2K tests. They prove the current contract covers the principal counterexamples that motivated V2K recovery. They do **not** prove a full current native positive execution; that remains NOT_TESTED because no qualified source receiver was exercised.

## Historical V2K evidence

Historical V2K four suites with exact restored dependencies: **63 passed** (24 candidate suite included). Exact dependency/owner suites: **50 passed / 1 source-cut check failed**; the failed check compares current tree to historical commit, not V2K semantics. Without dependency: collection error. The 111-test owner aggregate is not available as one exact suite. These receipts are historical evidence only.

## No current first consumer for old V2K

S6 `CURRENT_RECEIVER_FIRST_CONSUMER_MAP.json` records V2K production functions as `CURRENT_PATH_ABSENT_UNRESOLVED` / `NO_REAL_RECEIVER_YET`. The current R61 contract is a different ABI, not a drop-in successor. No historical transplant was made.
