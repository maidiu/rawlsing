# PYAT V2K — historical expected-work identity vs current R61

**Role:** independent original U/E/source identity and current-workload ABI reconciler. Not PRE-MAIN integrator, source/semantic issuer, original reviewer or own hostile reviewer.

**Repository:** `maidiu/rawlsing` (private). **Branch:** `agent/pyat-r3-v2k-current-abi-owner-decision-20261031-r1`. **Startup:** `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`. **Current PRE-MAIN at audit close:** `87755f02ec5c37499b09e80db6fbdcc9316a6b15`; relevant R61/V2K paths unchanged between cuts.

**Executor/capability:** OpenCode / `opencode-go/deepseek-v4.1-flash` (DeepSeek V4.1-Flash). MAX requested; actual effort not independently observable. Isolated worktree; no existing V2K-current-ABI worktree displaced. No model/harness switch.

**Write scope:** only `WORKER_RETURNS/PYAT-R3-V2K-CURRENT-ABI-DECISION/`. No PRE-MAIN, production source, actor/science permission or merge was modified.

## FINDING

### 1. Overall decision

`RETIRE_HISTORICAL_V2K_EXACT_IDENTITY_AS_CURRENT_INTERFACE__RETAIN_CURRENT_R61_ISSUED_WORKLOAD__ADAPT_TEST_ONLY_NEGATIVE_ORACLES`.

Historical V2K is real sourcefree evidence, but it is not a current ABI. Current R61 `pre553_issued_workload.py` provides an issuer-bound expected-work envelope and negative checks that supersede the old exact identity keys. No historical V2K module was transplanted.

### 2. Function-by-function result

`HISTORICAL_FUNCTION_VS_R61_CONTRACT.jsonl` has **38** keyed rows:

| Status | Rows |
|---|---:|
| `ALREADY_PROVIDED_BY_CURRENT` | 3 |
| `SUPERSEDED_RETIRED` / `SUPERSEDED_BY_CURRENT` | 13 |
| `PARTIALLY_PROVIDED_EXACT_KEY_RETIRED` | 1 |
| `PARTIALLY_PROVIDED_ORIGINAL_ITEM_ANTI_JOIN_HELD` | 1 |
| `DEPENDENT_ON_UNISSUED_ORIGINAL_AUTHORITY` | 2 |
| `RETIRED_NO_CURRENT_CONSUMER` / `RETIRED_EVIDENCE_ONLY` | 4 |
| `RETAIN_CURRENT` | 13 |
| `ADAPT_TEST_ONLY` | 1 |

- Current `IssuedWorkloadRecord`/`CurrentDecisionResolver` already provide the issuer/custodian role.
- Current `NativeWorkload`/`GovernedC11Projection`/descriptor/requests/discoveries provide expected-work identity at current issuer-bound grain.
- Current `admit`/`execute_issued_workload` provide admission, expected-job multiset, source edition, envelope, role direction and Batch/C11/Route B/I03/I05 execution.
- Historical V2K exact keys, dispatch mapper, executed-workload/reconcile records, owner-scope sourcefree execution and legacy aliases are retired or held as historical evidence.
- `_validate_original_against_c11` item/namespace anti-join is the one partially missing current function; it depends on original U/E/source scopes and remains HOLD, not a reason to transplant old code.

### 3. Current R61 consumer and negative receipts

Current first consumer: `rawlsing_next/pre553_native_workload_binding.py` (`build_test_only_workload`/`execute_test_only_workload`) + `pre553_issued_workload.admit`/`execute_issued_workload`.

`tests/test_current_r61_contract_negatives.py` on current PRE-MAIN tree: **8 passed**, exit 0.

It proves current refusals for:
- foreign issuer/wrong decision;
- removed held row/expected job mismatch;
- mutated identity/envelope;
- wrong role/target-condition direction;
- replay/prior caller receipts;
- wrong source edition/source factory;
- severed resolver dependency.

This is a current R61 negative-oracle suite, not a historical V2K transplant. Full current native positive execution remains **NOT_TESTED** because no qualified current source receiver was exercised.

### 4. Historical V2K receipts

With exact historical dependencies restored only in isolated tree:
- four V2K suites: **63 passed**;
- 24-test candidate suite included;
- exact dependency/owner suites: **50 passed / 1 source-cut check failed**;
- without dependency: collection error;
- 111-test aggregate not available as one exact suite;
- no current consumer.

These are historical evidence only. They do not reopen current integration.

### 5. Source cuts

| Artifact | Cut |
|---|---|
| Historical V2K origin/tip | `d1283fb53b543471fe825e78d64bf5bd19efbf11` / `694fb45085cd5e4891949921a44edb77c3f603f2` |
| V2K source blob | `e3ef9a2469966b8ecfbcd178b971f54c687aef22` |
| V2 contract | `08bb75c431d3352cb0d17e9a65f7d855b4d35e59` |
| Binder | `7d8b3902c3f8f257637b7c07ad9feb5e096d48e5` |
| Durable consumer | `dc146e920909c8577b5c3c316cd9a8631e96ffd8` |
| Verifier | `996c8e907f2befde93af09b60154b610c1ffeb63` |
| Checkpoint | `719c8d878bcfb3b6c61c844c9bf974ada8365929` |
| Current issued workload | `31e84f49d624f5524906e9e7839d2873106f8249` at `87755f02...` |
| Current binding | `dac73e484f8619088f5c6701b2b6991c07540f3b` |
| Current projection | `8a761119e4a8d68eb291fc4edfadb52e027f8284` |
| Source-native preimage adapter | `a6299c1a6e8b26bd055ced1f49e5b757f20ccd8c` |
| Universal workload | `8e7fe00a3ed008361d9f3c501e7782b2de3a636e` |

## INTERPRETATION

The historical V2K module solved a sourcefree expected-work identity/reconciliation problem in its own stranded P01/A04/A05 dependency world. Current R61 solves the same current integration problem with a different, issuer-bound `NativeWorkload`/`IssuedWorkloadRecord` envelope and a real current test-only binder. Keeping both as current interfaces would create a duplicate identity contract and invite foreign-issuer/old-alias admission. Retirement is the correct owner decision, with the original item/namespace C11 anti-join preserved as a source/U-E HOLD rather than a code transplant.

## HQ ACTION

1. Retain current R61 `pre553_issued_workload`/`pre553_native_workload_binding` unchanged.
2. Retire historical V2K exact interface from current integration; preserve source/test blobs as evidence.
3. Keep the current R61 negative oracle tests as active coverage.
4. Do not merge historical V2K or add a duplicate identity module without the reopen conditions in `INTEGRATION_OR_NONADOPTION_PLAN.md`.
5. Route the original item/namespace C11 anti-join HOLD to the original U/E/source owner if a future current consumer requires it.

## OWNER

Original U/E/source and V2K owner, current R61/Pyat workload owner, incumbent Pyat/HQ intake, and a distinct I3 source + negative-oracle reviewer. No self-review.

## Three courts

- **ENGINEERING:** `RETIREMENT_ACCEPTED_SCOPED__CURRENT_R61_NEGATIVE_ORACLES_8_PASS__FULL_POSITIVE_NOT_TESTED`.
- **SCIENCE:** `HOLD__EXPECTED_WORK_IDENTITY_SEPARATE_FROM_OBSERVED_SOURCE_SCIENCE`.
- **AUTHORITY:** `HOLD__SOURCEFREE_DOCUMENTARY_DECISION_ONLY__NO_SOURCE_ACTOR_WORLD_GRANT`.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

**DONE:** 38-row function comparison; current R61 negative oracle suite 8 pass; historical V2K 63-pass receipt; decision and per-function exceptions; no code transplant.

**REMAINING:** original U/E/source decision if the item/namespace anti-join is ever required; full current native positive execution; independent reviewer.

**BLOCKERS:** no qualified current source receiver for a native positive; original U/E/source/science permissions ungranted; 111-test V2K aggregate unavailable; no current V2K consumer.

**LARGEST MOVE:** retain current R61, retire historical V2K exact interface, and keep current R61 negative tests as the active boundary. Reopen only under the documented adapter conditions.

**FLIGHT:** `V2K_RETIRE_HISTORICAL_EXACT_IDENTITY + RETAIN_R61_ISSUED_WORKLOAD + CURRENT_NEGATIVE_ORACLES_8_PASS + SCIENCE_AUTHORITY_HOLD + NO_MERGE`.

**DELTA:** `+` explicit per-function current-vs-historical decision; `+` current R61 negative receipts; `+` source cuts and reopen conditions; `−` no historical transplant; `−` no full native positive; `−` no source/science/actor grant or merge.

## Return artifacts

- `00_RETURN.md`
- `HISTORICAL_FUNCTION_VS_R61_CONTRACT.jsonl`
- `RETAIN_ADAPT_RETIRE_DECISION.md`
- `CURRENT_CONSUMER_AND_NEGATIVE_ORACLES.md`
- `SCIENCE_PERMISSION_MATRIX.md`
- `INTEGRATION_OR_NONADOPTION_PLAN.md`
- `tests/test_current_r61_contract_negatives.py`

**Exact immutable pushed remote SHA:** reported after push/readback; self-reference excluded. Independent I3 source and negative-oracle review required at exact SHA.
