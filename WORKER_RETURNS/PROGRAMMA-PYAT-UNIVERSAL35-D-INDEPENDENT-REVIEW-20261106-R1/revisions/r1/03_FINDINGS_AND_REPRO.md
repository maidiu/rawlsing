# D r1 — findings and exact reproductions

## 1. OriginalItemID and physical-code identity now work — positive

The repaired path carries both original IDs and physical codes. Independent focused probe:

```text
item_id_wrong REFUSED Original35OperationError ORIGINAL_ID_TO_PHYSICAL_CODE_CONFLICT:B
item_id_missing REFUSED Original35OperationError ORIGINAL_ID_TO_PHYSICAL_CODE_CONFLICT:B
physical_code_wrong REFUSED Original35OperationError ITEM_FACT_ABSENT:NOT_A_PHYSICAL_CODE
bundle_source_mismatch REFUSED WorkloadBindingRefusal INVENTORY_SOURCE_EDITION_MISMATCH
```

This closes the prior cosmetic/ignored-item-ID defect. The 7 B tests pass.

## 2. Value/conditioner payload changes real request/facts/ledger and restores — positive

```text
value_changed_compilation True facts_same False ledger_same False
restore_exact True True True
```

Changing a planned F2 conditioner/domain changes current compilation, emitted jobs, facts and operation ledger; exact restore returns baseline. This is accepted only for this sourcefree payload subscope.

## 3. Extra unplanned operation is accepted — REVISE

`bind_governed_frontier` checks for **missing planned** operations but does not require the supplied frontier to equal the planned frontier. A supplied frontier containing the planned items plus one extra unplanned operation is accepted:

```text
EXTRA_ACCEPTED ca89f337a7e7c0b9e212d61aecfdc5a3c693e12b5090f6d662f96717ff4e0067 ops 15 expected 15
```

The extra operation was a duplicate target/condition with a different claim class (`DIST`), not present in the plan. This violates “only planned requests allowed.” A disconnected frontier that merely lacks required items is refused, but an enriched/disconnected frontier with extra operations is not.

**Action:** compare the supplied frontier operation identity set/material against the plan-derived explicit frontier and refuse extras, substitutions, duplicate identities and mismatched aliases. Owner D/B.

## 4. Actual all35 symbolic frontier coverage is partial — REVISE/limit

Sourcefree actual R157 full-config run:

```text
load_s 26.145; plan_s 6.456; frontier_s 1.185
cpu_user_s 30.990; cpu_system_s 1.124; rss_max_bytes 969,379,840
35 source plan: 18,276 items; 18,413 slots; 18,467 operations
frontier rows: 20/35
total frontier operations: 991 (HELD 970; ELIGIBLE 21)
15 sources: NO_EXPLICIT_PLANNED_FRONTIER
```

- SRC01: 4 occurrences; 32 operations; 0 eligible; 32 held; 0 deferred/pending.
- SRC01 occurrence facts: `administration=UNKNOWN`, `route_state=UNKNOWN`, actual original IDs and physical aliases; no false ADMINISTERED/KNOWN/person for unknown route. The `person` unit is correct for SRC01.
- SRC11: 20 eligible operations; SRC14: 1 eligible; all other source frontier rows are held.
- The old 600s global cartesian path is not used; the planned-request path completed in ~1.2s after loading. But **all35 frontier construction is not complete**: 15 sources return `NO_EXPLICIT_PLANNED_FRONTIER` because the current builder selects only F2/F3H/F3R/F4 and refuses when none are selected.

This is honest typed refusal for sources without explicit planned F2-F4, but it is not an all35 frontier/candidate account. The user-requested all35 symbolic frontier measurement therefore remains partial.

## 5. D execution wrapper — HOLD for full readiness

`pre553_original35_execution.py` remains unchanged from the prior cut:

- Direct `decode_sav`/`decode_dta` bypasses `pre553_source_read_admission` current-decision/revocation/replay.
- `max_items=3` default is diagnostic, not full supported-operation execution.
- First-unselected physical-slot coordinate fallback can invent a coordinate.
- `NativeSourceRule` uses synthetic `source_id:name` original IDs and hardcoded `unit="person"`.
- Full eager decode occurs before filtering; bounded C reader pending.
- C11 state counts are diagnostic only; no `EmpiricalFact`, E/N10E bind or native provenance.
- `pytest test_pre553_original35_execution.py`: **2 skipped** (runtime binding unavailable). The author's 2-pass claim is not independently reproduced; no native fact follows.

The user-authorized scoped engineering read does not require new admin paperwork, but the existing source-read/revocation/replay contract remains open before final native execution.

## 6. Counts and evidence labels

- Corrected B counts are present: `EXECUTABLE_RAW 5,630; HELD 4,655; INAPPLICABLE 8,131; DEFERRED 51; ABSTAIN 0; NOT_REQUESTED 0`; historical plan_ref preserved.
- Route split is 676 `ELIGIBLE_APPLICABLE`, 4,705 `ROUTING_UNKNOWN`, 249 `RULE_UNAVAILABLE`.
- D `route_qualification.json` still labels `route_qualified_total: 5630`; B evidence still labels `route_qualified` 5,490/120/20. Those are executable totals, not route-qualified. Use `route_split` for execution qualification.

## 7. Preserved positives / no overclaim

- A/B full-config join via `load_original().document` remains scoped-accepted; previous `select` ABI note is unchanged.
- B value/conditioner payload path is accepted scoped; no full B/D/native acceptance.
- No source-ID branch, duplicate compiler, marginals-as-joint construction, original data read, protected merge or science/native grant.
- Previous ABC/source review verdicts remain exact historical evidence.
