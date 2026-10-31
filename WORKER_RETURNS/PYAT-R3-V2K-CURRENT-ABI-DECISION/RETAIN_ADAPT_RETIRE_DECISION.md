# RETAIN / ADAPT / RETIRE decision — historical V2K vs current R61

**Overall decision: `RETIRE_HISTORICAL_V2K_EXACT_IDENTITY_AS_CURRENT_INTERFACE__RETAIN_CURRENT_R61_ISSUED_WORKLOAD__ADAPT_TEST_ONLY_NEGATIVE_ORACLES`.**

This is a sourcefree owner-decision return, not a merge, source grant or native/science adoption. The old V2K module is retained as historical evidence only. No historical module was transplanted into `rawlsing_next`.

## 1. Current R61 contract retained

Current PRE-MAIN `87755f02...`:

- `rawlsing_next/pre553_issued_workload.py` blob `31e84f49d624f5524906e9e7839d2873106f8249`
  - `OriginalWaveIdentity`
  - `IssuedWorkloadRecord`
  - `CurrentDecisionResolver`
  - `ExpectedWorkloadBinding`
  - `IssuedEstateFrontier`
  - `NativeWorkload`
  - `admit()`
  - `execute_issued_workload()`
  - `NativeWorkloadResult`
- `rawlsing_next/pre553_native_workload_binding.py` blob `dac73e48...` — current TEST_ONLY workload builder and first consumer.
- `rawlsing_next/pre553_source_native_preimage_adapter.py` blob `a6299c1a...` — current sourcefree native preimage source.
- `rawlsing_next/pre553_source_backed_c11_facade.py` blob `8a761119...` — `GovernedC11Projection` source/universe/item/routing identity.
- `rawlsing_next/pre553_universal_workload.py` blob `8e7fe00a...` — current universal workload compilation/execution path.

These are retained unchanged. They provide issuer-bound expected-work envelopes, source/science permission records, expected job multiset checks, source-edition checks, catalog/role direction checks and Batch/C11/Route B/I03/I05 execution.

## 2. Historical V2K exact identity retired

The historical V2K module `694fb450...` / blob `e3ef9a24...` and its restored dependencies (`08bb75c4...`, `7d8b3902...`, `dc146e92...`, `996c8e90...`, `719c8d87...`) are **not a current interface**:

- Current `pre553_issued_workload.py` has no `V2ExpectedWorkDeclaration`, `v2_bind_semantic_to_dispatch`, `V2_SCHEMA_VERSION`, `V2DispatchBinding`, `V2ExecutedWorkload`, `OriginalIdentity`, `OriginalExpectedWork`, `FrozenOriginalExpected`, `OwnerScopePlan` or `run_sourcefree`.
- Current `NativeWorkload`/`GovernedC11Projection` bind source edition, native item ids, release/routing/risk, carrier, country/population, weight/estimand, missing/occurrence and target/conditioner roles at an issuer-bound envelope level. The exact V2K key is not consumed by current R61.
- The old V2K tests pass only after restoring exact historical dependency blobs into an isolated tree; that is historical replay evidence, not a current ABI.
- The original item/namespace C11 anti-join in `_validate_original_against_c11` is not provided by current `admit`; it depends on original U/E/source scopes and remains `HOLD`. It is not needed for the sourcefree current R61 test-only path and does not justify transplanting the old module.

**Per-function status:** see `HISTORICAL_FUNCTION_VS_R61_CONTRACT.jsonl`. Summary:

| Status | Rows | Meaning |
|---|---:|---|
| `ALREADY_PROVIDED_BY_CURRENT` | 3 | Current `IssuedWorkloadRecord`/resolver/frontier provide the current issuer/custodian/frontier function. |
| `SUPERSEDED_RETIRED` / `SUPERSEDED_BY_CURRENT` | 13 | Current envelope/execute/result/catalog path supersedes the old function; no current consumer imports the old key. |
| `PARTIALLY_PROVIDED_EXACT_KEY_RETIRED` | 1 | Current projection/descriptor covers current identity at a different grain; exact old key retired. |
| `PARTIALLY_PROVIDED_ORIGINAL_ITEM_ANTI_JOIN_HELD` | 1 | Original item/namespace C11 anti-join remains a source/U-E HOLD, not current. |
| `DEPENDENT_ON_UNISSUED_ORIGINAL_AUTHORITY` | 2 | `OwnerScopePlan`/`run_sourcefree` rely on original U/E/source authority; not current. |
| `RETIRED_NO_CURRENT_CONSUMER` / `RETIRED_EVIDENCE_ONLY` | 4 | No current consumer or historical/evidence-only helper. |
| `RETAIN_CURRENT` | 13 | Current R61 contract functions retained. |
| `ADAPT_TEST_ONLY` | 1 | Negative oracles adapted as current R61 tests only. |

No row is marked `UNIQUE_USEFUL_READY` for historical code. No historical function is promoted to current production.

## 3. ADAPT exception — test-only negative oracles only

The only adaptation is a sourcefree test file, not historical code:

`tests/test_current_r61_contract_negatives.py` exercises the current `admit()` / `execute_issued_workload()` consumer:

- baseline positive admission;
- foreign issuer / wrong decision record;
- removed held-row/expected-job mismatch;
- mutated expected-work identity/envelope hash;
- wrong role/target-conditioner direction;
- replay/prior-receipt refusal;
- wrong source edition/source factory;
- severed current resolver dependency.

Result on current PRE-MAIN tree: **8 passed**, exit 0.

This proves the current R61 contract already enforces the negative boundaries that motivated historical V2K recovery. It does **not** prove a full native execution positive; that remains NOT_TESTED because no qualified current source receiver was exercised.

## 4. Per-function exceptions

- `V2IssuerRecord` / `V2CustodianRecord`: already represented by current `IssuedWorkloadRecord` + `CurrentDecisionResolver`; no separate historical record needed.
- `V2_SCHEMA_VERSION`, `V2ExpectedWorkDeclaration`, `V2DispatchBinding`, `V2ExecutedWorkload`, `v2_execute_through_a04`, `v2_reconcile`, `v2_to_a05_universe`: retired/superseded by current envelope/execute/result path.
- `OriginalIdentity`: current `GovernedC11Projection` + `NativeWorkload` descriptor provide current identity at a different grain; exact key retired.
- `OriginalExpectedWork` / `FrozenOriginalExpected`: superseded by current `NativeWorkload` + `IssuedEstateFrontier`/`IssuedWorkloadRecord`.
- `OwnerScopePlan` / `_validate_original_against_c11` / `run_sourcefree`: original U/E/source-authority-dependent; `_validate_original_against_c11` item/namespace C11 anti-join remains `HOLD`, not current.
- `legacy_preimage` / `legacy_from_preimage`: historical evidence only.
- Current R61 `NativeWorkload`, `IssuedWorkloadRecord`, `CurrentDecisionResolver`, `admit`, `execute_issued_workload`, `GovernedC11Projection`, `build_test_only_workload`: retained.

## 5. Engineering / science / authority

- **ENGINEERING:** `RETIREMENT_ACCEPTED_SCOPED__CURRENT_R61_NEGATIVE_ORACLES_8_PASS__FULL_POSITIVE_NOT_TESTED`.
- **SCIENCE:** `HOLD__EXPECTED_WORK_IDENTITY_SEPARATE_FROM_OBSERVED_SOURCE_SCIENCE`.
- **AUTHORITY:** `HOLD__SOURCEFREE_DOCUMENTARY_DECISION_ONLY__NO_SOURCE_ACTOR_WORLD_GRANT`.

## 6. Conditions to reopen adaptation

Reopen only if an original U/E/source owner supplies a competent current receiver that requires the granular V2K original identity fields and proves the current `GovernedC11Projection`/descriptor mapping is insufficient. In that case build a small adapter with exact field mapping and same-assertion tests; do not transplant the old module wholesale.
