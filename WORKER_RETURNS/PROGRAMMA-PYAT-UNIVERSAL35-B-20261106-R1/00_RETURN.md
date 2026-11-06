# PROGRAMMA PYAT — Universal35 B: source-neutral operation adapter and current-compiler join

**STATUS:** `ALL35_OPERATION_PLAN_READY__CURRENT_UNIVERSAL_AND_GOVERNED_CONSUMER_EXECUTED_SOURCEFREE__ALL35_NATIVE_FACTS_NOT_RUN__AUTHOR_EVIDENCE_FOR_REVIEW`
**BRANCH:** `codex/pyat-universal35-b-20261106-r1`
**BASE:** `d119045f4169439b4ba02d0870bc328f8beb3aaa`
**SOURCE CUT:** R157 `1924499ef52403a0f331b8aff9b7c7eff99bf1e2`
**CUSTODY OBSERVATION:** `b90708f7d79624faae3da2408932829e569e5ae2` (`35/35` exact SHA, `1,319,161,326` bytes; decode/native facts not inferred)
**RUNNER:** `/tmp/rawlsing-oct28-p1r1/venv/bin/python` (Python 3.11.3, pyreadstat 1.3.2, pandas 3.0.6)
**GRADE:** sourcefree author evidence only; no independent acceptance, native/scientific issuance, protected merge, provider call or human A5.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **B1. The recovered P1 constructor is present and its artificial RAW/weight and quadratic accounting defects are repaired.** `programma_pyat_original35_constructor.py` is recovered from `d1278613…`; `_item_refusal` no longer returns `WEIGHT_REF_ABSENT`; processed-item counting and duplicate operation detection now use key sets and `Counter`, preserving no-drop/duplicate/determinism semantics. | Optional weights are additive, not a RAW precondition. The change is a code-shape/perf repair, not a new compiler. | Review the exact diff; old synthetic P1 remains compatibility evidence, not the estate deliverable. | B engineering + D consumer owner |
| **B2. One source-pack-neutral adapter accounts the real 35 R157 packs.** `build_original35_operation_plan` accepts a library/config document, emits 35 source rows, 18,276 item identities, 18,413 physical slots, 18,467 operations, per-operation typed status/reason, and deterministic `plan_ref`. | The plan is grounded in the actual R157 configs, not 70 items/840 synthetic units. `SOURCE_NOT_PRESENT_HERE` is not used: custody is `LOCAL_BYTES_PRESENT_EXACT_SHA`. | Use the frozen adapter ABI for D; no absolute source path is embedded. | B + D + source custodian |
| **B3. F1/F2/F3/F4 are finite and typed, not an all-pairs queue.** F1 distributions emit all substantive response values; F2 selects bounded reciprocal pairs; F3 heterogeneity/recursive alternatives are typed; F4 emits true 3-item same-person joint requests. The plan exposes pair/joint candidate vs selected counts and status totals. | Raw observed-sample operations do not require a population weight or structural meaning. Unknown routing is recorded per operation; missing response mapping holds only the dependent item operation. | Preserve the candidate/selected denominator; no eager 15,576+ pair queue. | B + D + science/source owners |
| **B4. The terminal consumer is the current compiler, not a BatchManifest-only check.** `execute_plan_universal` calls `compile_universal_workload` and `execute_universal_workload`; `bind_governed_frontier` calls `compile_governed_frontier`. Both execute on bounded heterogeneous sourcefree SAV fixtures, produce native facts/receipts, and restore after a source-SHA fault. | This proves the typed join can reach current C11/I03/I05/Batch owners on supported fixtures. It does not prove all35 original decode/native facts. | Continue D on actual source rows using the frozen ABI; independently review this boundary. | B + D + independent reviewer |
| **B5. All35 source bytes are present by custody, but all35 respondent decode/native execution was not run in this lane.** | Presence/custody is not a fact or scientific grant. The plan is complete; native facts remain a separate phase. | Report `ALL35_NATIVE_FACTS_NOT_RUN`, not failure and not PASS. | D / source custodian / independent reviewer |

## 2. FROZEN ABI FOR D

```python
build_original35_operation_plan(
    document, *, source_presence=None, source_root=None,
    pair_budget=6, joint_budget=1, require_all35=True,
    expected_item_count=None, expected_physical_slot_count=None,
) -> Original35OperationPlan

lower_to_universal_workload(plan, *, bundle, as_of, host, purpose)
    -> UniversalLowering

execute_plan_universal(plan, *, bundle, source_factory, as_of, host, purpose)
    -> (UniversalLowering, UniversalWorkloadResult)

bind_governed_frontier(plan, *, bundle, inventory, policy, frontier,
                       as_of, host, purpose)
    -> GovernedFrontierCompilation
```

Plan schema: `PRE553_ORIGINAL35_OPERATIONS@1.0.0`. Source rows carry `source_id`, family/wave, source SHA, presence grade, item IDs, physical-slot ordinals, response/weight slot counts, status counts, operation refs, weight status, pair/joint candidate and selected counts. Operations carry source/event identity, kind, item IDs/codes, response/conditioner values, joint arity, stratum, measure kind (`RAW_OBSERVED_SAMPLE`/`GOVERNED_WEIGHTED`), status, reason, route status, response-state counts and source SHA.

The source root is caller-configured (`USER_ORIGINAL35_DATA_ROOT` alias). No personal absolute path is embedded.

## 3. EXACT COMMANDS AND RESULTS

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  -p no:cacheprovider --tb=short
5 passed in 31.36s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_programma_pyat_original35_constructor_adapter.py \
  -p no:cacheprovider --tb=short
1 passed in 0.29s
```

Whole-estate plan measurement (`evidence/all35_plan.json`):

```text
sources=35
items=18,276
physical_slots=18,413
operations=18,467
universal_operations=43,279
batch_units=43,279
no_drop=True
plan_ref=3e3a604a78c377030bffa39eb62cf065d111746f9bc1588f7dbf33bac0373b9c
elapsed=7.44s
maxrss=878,350,336 bytes (~838 MiB)
status counts: EXECUTABLE_RAW 5,630; HELD 1,595; ABSTAIN 0;
               INAPPLICABLE 11,191; DEFERRED 51; NOT_REQUESTED 0
pairs selected/candidates: 120 / 1,862,592
joints selected/candidates: 20 / 742,250,526
```

Source presence: all 35 rows `LOCAL_BYTES_PRESENT_EXACT_SHA`; no `SOURCE_NOT_PRESENT_HERE` rows. Full 35-row evidence is in `evidence/all35_plan.json`.

Targeted consumer evidence:
- `test_terminal_current_universal_consumer_executes_and_restores`: current `compile_universal_workload` + `execute_universal_workload`, native facts, same-source fault RED and restore PASS.
- `test_terminal_current_governed_frontier_joint_consumer`: current `compile_governed_frontier` + `execute_governed_frontier`, no-drop and joint/co-travel facts.
- `test_missing_optional_weight_does_not_hold_raw_and_missing_slot_holds_only_dependent`: RAW survives weight removal; missing response mapping changes only dependent item operations.
- `test_all35_no_drop_plan_accounts_every_original_item_and_slot`: 35/35, exact 18,276/18,413, F1–F4, determinism, bounded pair/joint frontier.

## 4. CHANGED PATHS

- `rawlsing_next/pre553_original35_operations.py` (new adapter and current-compiler bridges)
- `rawlsing_next/programma_pyat_original35_constructor.py` (recovered P1 + bounded accounting/optional-weight repair)
- `rawlsing_next/tests/test_pre553_original35_operations.py` (new)
- `rawlsing_next/tests/test_programma_pyat_original35_constructor_adapter.py` (new)
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-B-20261106-R1/00_RETURN.md`
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-B-20261106-R1/evidence/all35_plan.json`

No A-owned source-configuration package, current compiler/issued workload, E consumer, global config, provider, or other writer branch was edited.

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 B operation adapter
- Identity: codex/pyat-universal35-b-20261106-r1@<returned-commit>; base d119045f4169439b4ba02d0870bc328f8beb3aaa; R157 source cut 1924499ef52403a0f331b8aff9b7c7eff99bf1e2; custody b90708f7d79624faae3da2408932829e569e5ae2.
- Function/input-transform-typed-output: library/config document -> deterministic 35-source no-drop plan -> per-item/per-operation typed F1/F2/F3/F4 status -> current UniversalOperation/BatchUnitSpec payload -> current compile_universal_workload/compile_governed_frontier -> current I03/I05/Batch consumer on supported fixtures.
- Root/schema/clock/permission: schema PRE553_ORIGINAL35_OPERATIONS@1.0.0; caller-configured source root; no hardcoded personal path; no native/source/science permission issued.
- Actual first consumer: current execute_universal_workload and execute_governed_frontier on sourcefree heterogeneous fixtures (native facts/receipts observed). All35 original native facts NONE_VERIFIED_THIS_RUN.
- Evidence: 5 adapter tests + 1 P1 compatibility test pass; evidence/all35_plan.json.
- Affected existing IDs: S02.2/S02.3/S02.4/GAP-006/GAP-007/GAP-009/GAP-010 candidate evidence only; no protected status overwrite.
- Conditional unlocks: D can consume the frozen plan ABI and read-only source root for actual decode/native execution; independent review still required.
- Next action: independent exact-cut review + D actual original-row execution; retain source/science/native gates.
```

## 6. LIMITS / NOT RUN

- All35 original **respondent decode and native empirical execution**: `NOT_RUN`; only exact byte custody and operation planning are verified.
- All35 source/item/route/permission qualifications remain per-operation; no fabricated native PASS.
- Native C8/C10/C11/C12/KMS, CAN/ADP/Pyat issuance, provider calls, human A5, protected merge: `NOT_RUN`/`HOLD`.
- The all35 plan is a finite metadata/operation plan; it is not a claim that 742M joint or 1.86M pair candidates were executed. Selected/candidate denominators are explicit.
- Independent review is required; this author return cannot self-accept. No protected merge was performed.
