# PROGRAMMA PYAT — Universal35 D r1: OriginalItemID, occurrence facts, finite planned frontier

**STATUS:** `D_R1_IDENTITY_OCCURRENCE_AND_EXPLICIT_FRONTIER_REPAIRED__NATIVE_WRAPPER_RESIDUALS_PRESERVED__AUTHOR_EVIDENCE_FOR_F_REVIEW`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**FROZEN INPUT:** `115fe70e660fb19a65ca49b4a12ffc8876be065c`; code `40d490e96170c4c0c28aed6da0c906960ae91179`
**F REVIEW:** `dd2158e4b89976310632f722239a0da3a352f14a` — B_PAYLOAD_REVISE; AB full-config join ACCEPT_SCOPED; D readiness HOLD

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R1-1. OriginalItemID and physical source variable are now distinct and bound.** Plan operations retain aligned original IDs and physical codes. `build_frontier_inputs_from_plan` puts the original ID in `OccurrenceKey.item_id` and carries the physical code as the validated lookup alias. `_bundle_with_plan_aliases` maps original ID → verified bundle question ref through the physical code. | The old F2 `item_ids` mutation was ignored because only physical codes entered the frontier. Now wrong/cross-source/missing original IDs and physical codes absent from the bundle are typed refused; the exact unchanged plan restores the same compilation hash. | F exact-cut check; no source facts claimed complete. | D/B + F |
| **R1-2. Occurrence administration/unit/topology/form/routing are source-config facts.** Plan operations now carry `administration`, `unit`, `topology`, `forms` and exact `route_status`. `UNKNOWN`/held routing is not converted to `KNOWN`, person or scalar. `scalar` maps to the current grammar token `SCALAR_SINGULAR` only because that is the exact config topology fact; other topologies remain their original token and become typed unsupported/held. | SRC01 unknown-route occurrences remain `UNKNOWN` and are not `ELIGIBLE`; household/repeated facts remain household/non-scalar; no fake `DEFAULT_FORM` or personal fallback is introduced. Missing optional weights still do not block RAW. | Preserve exact 676/4,705/249 route split and held/unvisited accounting. | D/B + source owner |
| **R1-3. Frontier construction is now only explicit planned F2/F3/F4 requests.** `build_frontier_inputs_from_plan` no longer calls `enumerate_frontier` over inventory combinations. It builds exact `ScientificOperation`/`ScientificFrontier` entries with `make_operation`, `role_disposition`, inventory ledger, canonical hashes and plan-operation aliases. | The 600s SRC01 combinatorial path is not used. Scale is planned-request count, not n-choose-3. Planned conditioner values and joint membership drive the current compiler; removing the plan payload is RED, changing a planned conditioner/domain changes compilation/jobs, restore returns the exact baseline. | F closure on this exact head. | D/B + F |
| **R1-4. All35 symbolic accounting remains intact.** 35 sources, 18,276 items, 18,413 slots, 18,467 operations, no-drop true. Counts remain `EXECUTABLE_RAW 5630`, `HELD 4655`, `INAPPLICABLE 8131`, `DEFERRED 51`, `ABSTAIN 0`. Route split remains 676/4,705/249. | The repair changes identity/occurrence/frontier construction, not the source denominator or route facts. | Preserve historical and current refs separately. | D/B + HQ |
| **R1-5. Native wrapper remains not ready.** Direct decode/read-decision bypass, `max_items=3` diagnostic cap, arbitrary coordinate fallback and synthetic ID/unit/person behavior remain in `pre553_original35_execution.py`. | These are subsequent D/A/C integration residuals; they do not block this sourcefree contract repair and are not advertised as native facts. | Keep explicit NOT_READY; use C bounded reader after nonauthor qualification. | D + A/C + F |

## 2. EXACT PROOFS

- Original ID conflict: mutating an F2 target original ID → `ORIGINAL_ID_TO_PHYSICAL_CODE_CONFLICT`; restore → same compilation hash.
- Missing original ID → `ORIGINAL_ITEM_ID_ABSENT`/conflict refusal; wrong physical code → `PHYSICAL_CODE_NOT_IN_BUNDLE`; no fixture substitution.
- F2 conditioner/domain mutation → changed `ScientificFrontier`/compilation/jobs; restore → exact baseline hash.
- Removing the planned frontier payload → `NO_EXPLICIT_PLANNED_FRONTIER`; disconnected synthetic frontier is not accepted as the proof path.
- SRC01 unknown route occurrence → `administration=UNKNOWN`, `route_state=UNKNOWN`, no `ELIGIBLE` operation for that occurrence.
- All35 plan contains household units and non-scalar topology facts; F4 remains 20 deferred with `SAME_PERSON_ROW_REQUIRED`.
- Current plan refs: historical `3e3a604a78c377030bffa39eb62cf065d111746f9bc1588f7dbf33bac0373b9c`; status-repair `9ae291ca403e3d26fd0e4af9b6c536fac9509be878e0d9cc43a589f293d14ff7`; r1 identity/occurrence/frontier `aae15f52877e4eb0c61bfbfb47efc2d650d3289036ce38d3a76acee1b1e84e20`.

## 3. TESTS / EVIDENCE

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  -p no:cacheprovider --tb=short
7 passed in 27.33s
```

Evidence refreshed: `evidence/route_qualification.json`; B `evidence/all35_plan.json`.

## 4. CHANGED PATHS

`rawlsing_next/pre553_original35_operations.py`, `rawlsing_next/tests/test_pre553_original35_operations.py`, B evidence/return counts, D `01_R1_RETURN.md`. No A/C/E/grammar/compiler/guide/controller edit.

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r1 identity/occurrence/frontier repair
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; frozen input 115fe70e6.
- Function: full R157 config document -> B no-drop plan with OriginalItemID+physical-code binding and exact occurrence facts -> ONLY explicit planned F2/F3/F4 ScientificOperation/ScientificFrontier -> current compile_governed_frontier through verified original-ID aliases.
- First consumer: current governed-frontier compilation/requests on sourcefree fixture; actual native facts remain NOT_RUN.
- Evidence: 7 B tests; wrong/missing/cross-source ID refusal; value/conditioner mutation RED and restore; SRC01 unknown route non-eligible; all35 18276/18413/18467 counts.
- Limits: native original wrapper HOLD; E authentic bind NOT_RUN; no native/science/protected acceptance.
```

## 6. LIMITS

The C bounded reader is not yet integrated; original native/I03/I05/Batch facts and E handoff remain `NOT_RUN`. No native/scientific/source grant, protected merge, self-review, provider/human call or global change is claimed.
