# Universal35 D — independent B payload-repair and D boundary review

**ROLE:** existing nonauthor F reviewer; no authoring or repair.
**FROZEN CHECKOUT:** `115fe70e660fb19a65ca49b4a12ffc8876be065c` (tree `c3043d6629fe7155af30d825b685d04cb143768a`).
**IMPLEMENTATION:** `40d490e96170c4c0c28aed6da0c906960ae91179` (tree `610b75a1b294f4ccb8422560beab132dff6d6db0`).
**START:** `d129eebdb0472b0c3625efa281826a858bd0a384`.
**STATUS:** `D_FULL_READINESS_HOLD__B_PAYLOAD_REVISE__AB_JOIN_ACCEPT_SCOPED_SOURCEFREE__NO_NATIVE_ACCEPTANCE__NO_PROTECTED_MERGE`.
**PRIOR REVIEWS PRESERVED:** `ebd20c165bb275f66e4b3e2210535e96eecaf2ac`; `43e5962bbad72501166da59b744d618d10877b22`.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| Finding | Interpretation | Action | Owner |
|---|---|---|---|
| B value/conditioner payload change now changes compilation, emitted jobs, facts and operation ledger; exact restore passes; empty plan is refused. | The previous disconnected short-code path is materially improved for value payload. | Accept this subscope only; do not accept full B F2/F3/F4 yet. | F review / HQ |
| Mutating only an F2 `item_ids` value leaves compilation, facts and ledger identical. | OriginalItemID is still not carried; physical `source_variable_code` is used as `OccurrenceKey.item_id`. | Carry OriginalItemID and physical code as distinct, truthful identities and reject missing planned item IDs. | D/B |
| Frontier occurrences are hardcoded `ADMINISTERED/KNOWN/person/SCALAR_SINGULAR/DEFAULT_FORM` even for SRC01's 126/129 routing-unknown source facts. | Unknown routing and household/rank/repeated topology are silently converted to proven administration/person scalar. | Derive occurrence flags from source config/plan; preserve unknown/held or refuse. | D/B + source owner |
| Actual SRC01 plan `build_frontier_inputs_from_plan` did not complete within the 600s bound. | The repair is demonstrated only on a tiny fixture, not an actual source-plan scale; frontier construction is unbounded. | Bound construction to explicit planned operations and prove source-scale completion. | D/B |
| D `execute_source`/`execute_native_compiler_source` decode directly, and the native wrapper uses `max_items=3`, first-unselected-coordinate fallback, synthetic `source_id:name` item IDs and hardcoded person unit. | Diagnostic code is real but not full supported-operation execution; existing source-read/revocation/replay gate is bypassed. | Keep diagnostic scope explicit; use existing admission or record exact authorized read proof; remove diagnostic assumptions from final path. | D + source-read owner |
| D actual native facts are absent; SRC31 mapping refusal and SRC09/10/11/15 600s eager-decode noncompletion are documented honestly. | The D original-execution job is terminal at NOT_COMPLETED, not native acceptance. | Do not accept D as full goal completion; C stream/A mapping repair remain separate. | D + HQ |
| B counts corrected to HELD 4,655 / INAPPLICABLE 8,131; historical plan_ref preserved. | The old 1,595/11,191 cut is stale superseded evidence. | Preserve both cuts; use corrected counts. | D/B + HQ |

## 2. Separate grades

### B repaired payload — `REVISE`

- Actual F2 value/conditioner payload mutation changes `compile_governed_frontier` compilation, emitted jobs, facts and `operation_ledger`.
- Empty planned payload is refused (`NO_FRONTIER_ITEMS`); exact restore returns baseline.
- OriginalItemID mutation is ignored; route/administration/unit/topology are hardcoded; actual source-plan frontier construction is not bounded within 600s.
- B counts are corrected: `EXECUTABLE_RAW 5,630; HELD 4,655; INAPPLICABLE 8,131; DEFERRED 51; ABSTAIN 0; NOT_REQUESTED 0`; historical plan_ref `3e3a604a…` and recomputed `9ae291ca…` both retained.
- Sourcefree 676 route-qualified / 4,705 unknown / 249 rule-unavailable split preserved; F4 20 deferred.

### A/B joined — `ACCEPT_SCOPED_ENGINEERING_VIA_FULL_CONFIG_PATH`

`SourceConfigLibrary.load_original(sid).document -> build_original35_operation_plan` is the actual working path and reproduces the 35/35 plan. The earlier ABC `select` ABI concern remains a documentary/contract limit; it is not the D path. This does not accept compact `select` as an operation-plan document.

### D manifest/selection — `ACCEPT_SCOPED_SOURCEFREE_DIAGNOSTIC`

- `all35_manifest.jsonl`: 35 `MANIFEST_ONLY` rows, no native facts, 18,276/18,413 accounting.
- SRC31 C11 mapping refusal is typed and honest.
- D execution test file is **2 skipped** in this checkout because the runtime binding is unavailable; the author's 2-pass claim is not independently reproduced. No native fact follows.

### D execution wrapper — `HOLD_SCOPED_DIAGNOSTIC__NOT_FULL_READINESS`

- Direct `decode_sav`/`decode_dta` bypasses the existing `pre553_source_read_admission` current-decision/revocation/replay gate. The user's scoped engineering read is authorized; this is not a request for new admin paperwork, but the existing contract must be closed for final execution.
- `max_items=3` is a diagnostic default, not full supported-operation execution/accounting.
- The first-unselected physical-slot coordinate fallback can invent a coordinate.
- `NativeSourceRule` drops the original item ID and hardcodes `unit="person"`.
- Full eager decode is used before filtering; the bounded C stream is still pending.
- C11 state counts are diagnostic only; no `EmpiricalFact`, E/N10E authentic bind, native replay or provenance receipt is produced.

### D full readiness — `HOLD`

- Actual original I03/I05/Batch `EmpiricalFact` production: `NOT_COMPLETED`.
- SRC31 mapping refusal and 4x600s eager-decode limits are truthful.
- C stream/A mapping are separate dependencies; their absence does not justify rejecting the qualified part of B repair, but D is not full goal completion.

## 3. Exact reproduction highlights

```text
base_ops 66 facts 30 ledger 66
item_id_changed_compilation False facts_same True ledger_same True
value_changed_compilation True facts_same False ledger_same False
restore_compilation True facts_same True ledger_same True

actual SRC01 inventory: 129 occurrences
aidexp ADMINISTERED KNOWN person SCALAR_SINGULAR ('DEFAULT_FORM',) ('1','2','3')
source SRC01 routing: ROUTING_UNKNOWN 126; RULE_UNAVAILABLE 3
```

Actual SRC01 plan frontier construction produced no output before the 600s process bound; this is a sourcefree scale probe, not an original-data read. See `evidence/d_actual_plan_frontier_timeout.txt`.

## 4. Test commands

```text
pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  rawlsing_next/tests/test_programma_pyat_original35_constructor_adapter.py
# 7 passed in 26.95s

pytest -q rawlsing_next/tests/test_pre553_original35_execution.py
# 2 skipped in 0.38s (runtime binding unavailable)

custom small-fixture payload mutation/missing/restore
# item IDs ignored; value changes facts/ledger; restore exact; empty plan refused

actual SRC01 frontier-input flags probe
# 129 ADMINISTERED/KNOWN/person/SCALAR_SINGULAR despite 126 unknown routing
```

No A 35 fixture floor, whole-estate suite, broad hostile court or original data decode was rerun. No product/test/guide/protected file was edited.

## 5. PROGRAMMA_DELTA

See `05_PROGRAMMA_DELTA.json`. Summary: D B-payload repair is scoped-improved but REVISE; A/B full-config join is scoped-accepted; D manifest/selection is scoped diagnostic; D execution wrapper/full readiness are HOLD; no native/scientific/protected acceptance.

## 6. Boundary

Previous F reviews remain exact historical evidence. This is an independent review, not self-acceptance, repair, protected merge, native grant or scientific issuance. Exact published review head is returned in the final chat readback after commit/push.
