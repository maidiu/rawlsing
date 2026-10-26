# R151 — repair hardcoded pending states; grounded native occurrences

**Status:** `R150_PENDING_FIELDS_REPAIRED_WITH_GROUNDED_NATIVE_OCCURRENCES_WHERE_SUPPORTED`
**Base:** `2e6ca20d307d7f96afdf2c103be06ca77cbe1656` (R150 preserved)
**Scope:** metadata/authority-only. No survey file was opened, stat'ed, hashed or decoded; no current source/science/access grant.

## Defect repaired

R150's `_pending_item` hardcoded unit, topology, risk, domain and scientific role as pending for every item. R151 now resolves them item-by-item from exact evidence:

- **38/38 typed surfaces consumed** from the inherited corpus.
- 18 exact typed-surface domains; 17 raw codebook native-option domains; 3 exact representation-only surfaces with empty declared domain.
- 4 units resolved from source-specific evidence: LiTS-I D03 selected-respondent unit and WVS7 exact respondent-row unit.
- 2 topologies resolved (source-specific WVS7 `SCALAR_SINGULAR`).
- 4 risk sets resolved: LiTS-I D03 risk set and the WVS7 exact risk-set binding.
- B49 disposition/direction/routing/response/relation evidence is preserved; no module/measure guess is used.

## Actual native objects

- **2 actual `Occurrence` objects** and **2 actual `NativeSourceRule` objects** for WVS7 `Q291G5`/`Q291P5`, using the existing WVS7 runtime package's exact response topology, risk set, respondent-row unit and question bindings.
- **1 actual `SourceInventory`** for that WVS7 grounded subset. It is explicitly `inventory_complete=false`, holds only the 2 grounded occurrences and states exact gaps for the remaining items.
- No planner/lowerer invocation is made: the partial inventory is incomplete and scientific roles/frontier/Epre are not current. `planner_invocation_status=NOT_INVOKED__PARTIAL_INVENTORY_INCOMPLETE_AND_FRONTIER_ROLES_PENDING`.

LiTS-I `q301_2`/`q301_7` gain exact typed domain, D03 risk set and selected-respondent unit, but topology remains an exact item-level unknown owner; therefore no `Occurrence` is constructed for them. This is field-level, not a source-wide blanket unknown.

## Conservation and lanes

- R150 B49 records: **4,460** preserved exactly.
- Additional typed-surface-only items: **33**; preparation items: **4,493**.
- 3,804 non-U material/demographic/position items remain in the conditioner/context lane and are not promoted to target measurements.
- 26 unmatched relation IDs remain exact holds.
- All 35 source cells retained; official source grant remains null and no blind metadata-derived source execution is claimed.

## Next calls

```sh
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime/render_grounded_native_input.py --source-id SRC35
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime/render_grounded_native_input.py --source-id SRC27
PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/runtime/render_grounded_native_input.py --source-id SRC04
```

Actual source-read/workload execution still requires exact current source identity/edition, a source-response grant/current resolver, complete U/Epre and grounded scientific roles/frontier. The WVS7 partial inventory is not a complete U or Epre.

## Verification

- Focused checks: **6 passed** (`evidence/focused.log`).
- Verified: 38-surface consumption, field-level resolution counts, actual WVS7 Occurrence/Rule/Inventory types, LiTS partial field resolution, context retention, 26 unmatched holds, 4460 B49 + 33 typed-only conservation, no decoder/survey call, no current grant.
- CLI probes: SRC04, SRC27, SRC35 under `evidence/`.
- Receipt: `evidence/PROOF_RECEIPT.json`.

## Limits

No source/respondent access, current administered U, Epre, empirical/learned/FF execution or adoption. Full35/1890/F1–F8/global/LongMemory/C5 and all R09/CI/prod/N11/N12/Sorok/J52/W52/actor holds remain. Native core read-only at `44e7ace44d9e1b023a15d14ee1ead9b176d0e522`.
