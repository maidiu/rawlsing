# D payload-repair review — findings and exact reproductions

## 1. Actual value/conditioner payload drives compilation, facts and ledger — positive

The repaired D test and an independent small-fixture repro show:

```text
base_ops 66 facts 30 ledger 66
item_id_changed_compilation False facts_same True ledger_same True
value_changed_compilation True facts_same False ledger_same False
restore_compilation True facts_same True ledger_same True
```

- Changing a planned F2 `response_values` / `conditioner_values` changes the current `compile_governed_frontier` compilation hash, emitted jobs, consumed `fact_refs` and `operation_ledger`.
- Restoring the exact plan restores the exact baseline compilation/facts/ledger.
- Removing the whole planned operation payload (`operations=()`) is refused with `NO_FRONTIER_ITEMS`.
- The B counts are corrected in this cut: `EXECUTABLE_RAW 5,630; HELD 4,655; INAPPLICABLE 8,131; DEFERRED 51; ABSTAIN 0; NOT_REQUESTED 0`; historical plan_ref `3e3a604a…` is preserved and the recomputation is recorded separately.

This is a genuine improvement over the earlier disconnected short-code check and is accepted only as a scoped payload-value path.

## 2. OriginalItemID is ignored — REVISE

`build_frontier_inputs_from_plan` uses `source_variable_codes` as `OccurrenceKey.item_id` and nowhere carries `PlanOperation.item_ids` (the planned original implementation IDs):

`rawlsing_next/pre553_original35_operations.py:570-588`.

The independent repro changed only an F2 operation's `item_ids` to `("WRONG_ITEM_ID",)`:

```text
item_id_changed_compilation False facts_same True ledger_same True
```

No refusal, no changed frontier, no changed fact or operation ledger. This violates the required truthful mapping between the original item identity and the physical source code. The plan's actual F2 item IDs are e.g. `question_impl.phase0...`, while the emitted frontier uses short codes such as `c13a`/`d18c`.

**Owner:** D/B. **Action:** carry both identities explicitly through occurrence/inventory/compilation and reject a planned item whose original item ID is missing or altered. Do not use the physical code as a substitute for the original item ID.

## 3. Route, administration, unit and topology are hardcoded — REVISE

`build_frontier_inputs_from_plan` emits every occurrence as:

```python
unit="person"
topology="SCALAR_SINGULAR"
forms=("DEFAULT_FORM",)
administration=ADMINISTERED
route_state="KNOWN"
```

at `rawlsing_next/pre553_original35_operations.py:582-588`, regardless of the plan's actual `route_status`, source subject unit, occurrence/topology, household status, rank/repeated form, or weight/design status.

A sourcefree actual-plan probe on SRC01 produced:

```text
inventory_occurrences 129
aidexp ADMINISTERED KNOWN person SCALAR_SINGULAR ('DEFAULT_FORM',) ('1', '2', '3')
...
```

SRC01's source configuration has 126 `ROUTING_UNKNOWN` and 3 `RULE_UNAVAILABLE` of 129 routing entries. The repaired frontier therefore converts unknown routing into `KNOWN`/`ADMINISTERED`, and would convert household/rank/repeated topology to person/scalar if applied to such a source. This is exactly the source-qualification issue F previously flagged.

**Owner:** D/B + source owner. **Action:** derive occurrence unit/topology/forms/route/administration from the source pack and plan row/operation. If route is unknown, keep it unknown or refuse/hold; do not mark ADMINISTERED/KNOWN. For household/rank/repeated sources, do not silently emit person/scalar.

## 4. Actual source-plan frontier construction is not bounded — HOLD/REVISE

A sourcefree probe loaded the actual SRC01 config/plan, then called `build_frontier_inputs_from_plan(plan, source_id="SRC01")`. It produced no output within the 600s process bound:

`evidence/d_actual_plan_frontier_timeout.txt`.

The author's B/D tests use a tiny fixture. The all35 manifest path does not exercise actual F2/F3/F4 frontier construction for an actual source. SRC01 has 129 occurrence codes and the adapter requests J=3/K=1 classes over the whole 129-domain inventory. This is a scale/boundedness defect, not an original-data read failure.

**Owner:** D/B. **Action:** bound frontier construction to the plan's explicit F2/F3/F4 operations and realistic candidate limits; prove source-scale completion before claiming actual plan-to-frontier readiness.

## 5. D execution wrapper — HOLD for full readiness; diagnostic limits are honest

`rawlsing_next/pre553_original35_execution.py:139-215` and `:225-330`:

- `execute_source` directly calls `decode_sav`/`decode_dta` and builds C11/repository; it does not consult `pre553_source_read_admission` / current decision / revocation / replay. User-authorized scoped engineering read is not new admin paperwork, but the existing source-read contract must not be silently bypassed for a final native run.
- `execute_native_compiler_source(max_items=3)` selects only the first three route-qualified response slots; this is a diagnostic default, not full supported-operation execution/accounting.
- When no coordinate slot exists it falls back to the first physical slot not selected (`:258-269`), potentially inventing a coordinate.
- It creates `NativeSourceRule(implementation_id=source_id + ":" + name, unit="person")` (`:297-300`), losing the original item ID and hardcoding person unit.
- It decodes the full source eagerly and filters cells afterward; the stream is not the bounded C producer requested by D's own return.
- `execute_source` returns C11 state counts (`raw_products`) but no native `EmpiricalFact`, no E/N10E bind and `native=False`. That diagnostic classification is honest.
- SRC31 typed C11 mapping refusal and SRC09/10/11/15 600s eager-decode noncompletion are recorded honestly in `evidence/native_attempts.json`; no native facts are claimed.

`evidence/d_execution_tests.log` shows the D execution tests are **2 skipped** in this checkout because the runtime binding is unavailable. The author's claimed 2 passes are not independently reproduced here; this does not affect the B repair result.

**Owner:** D + existing source-read owner. **Action:** use the existing admission/revocation/replay gate (or record the exact user-authorized engineering grant and replay/revocation proof), remove the diagnostic-only 3-item/fallback/unit assumptions from any final path, and use the bounded C stream once returned.

## 6. Evidence labels are misleading — REVISE (minor)

`WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/evidence/route_qualification.json` has:

```text
route_qualified_total: 5630
```

and B `all35_plan.json` has `route_qualified` totals 5,490/120/20. Those are all `EXECUTABLE_RAW` operations, not route-qualified. The same files correctly show `route_split` 676 `ELIGIBLE_APPLICABLE`, 4,705 `ROUTING_UNKNOWN`, 249 `RULE_UNAVAILABLE`.

**Owner:** D/B + HQ. **Action:** use `route_split`/676, not `route_qualified_total`/5,630, for execution qualification. Preserve the old cut and historical plan_ref.

## 7. A/B joined status

`SourceConfigLibrary.load_original(sid).document -> build_original35_operation_plan` is the actual working full-config path and reproduces the D/B 35-source plan. The previous ABC review's `select` ABI concern remains a documentary/contract note; D's actual use of `load_original` is scoped-accepted. This is not acceptance of the compact `select` ABI as an operation-adapter input.

## 8. Positive/negative boundaries preserved

- No source-ID branch or duplicate compiler found in the repaired path.
- No marginals-as-joint construction observed; F4 remains deferred at `SAME_PERSON_ROW_REQUIRED`.
- B's corrected 4,655/8,131 counts are present; old 1,595/11,191 cut is retained as historical evidence.
- FIABC 144/3, V550/J compare-only, LiTS/WVS country/routing/weight holds, SRC04 no-revival and SRC17 native evidence remain as recorded in F source qualification.
- No original respondent data was read in this review.
