# PROGRAMMA PYAT — Universal35 D/B r2: exact frontier identity and all35 frontier accounting

**STATUS:** `D_B_R2_EXACT_FRONTIER_REFUSAL_AND_ALL35_ACCOUNTING_REPAIRED__NATIVE_RESIDUALS_HOLD__AUTHOR_EVIDENCE_FOR_F`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**FROZEN INPUT:** `017337a9e1edafcbcdbaf538eac9c2c91f7d0791`
**F R1 REVIEW:** `f2c477cee7535bad6103a5353f220a7eddd73a99`

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R2-1. Supplied frontier must now equal the explicit plan-derived frontier.** `bind_governed_frontier` builds the expected inventory/policy/frontier from the plan and compares content hashes plus per-operation identity/material counters. Extra, substituted, duplicated, missing or incomplete supplied inputs are typed refused. | The prior extra-operation acceptance (`UNEXPECTED_ACCEPT ca89f337…`) is closed without adding a second compiler. Intentional value/conditioner changes still work by rebuilding the corresponding plan/frontier; exact restore returns the baseline hash. | F exact-cut recheck. | D/B + F |
| **R2-2. All35 explicit frontier accounting is now concrete.** `account_all35_frontiers` reports every source: 20 have explicit planned F2/F3/F4 frontiers; 15 have no explicit non-F1 request. Total explicit frontier operations: 991 (21 eligible / 970 held-or-unknown). No requests are invented for the 15 no-request sources and their existing F1 plan path is preserved. | The prior implicit 15-source omission is no longer hidden; it is a typed `NO_EXPLICIT_PLANNED_F2_F3_F4_REQUEST` row in the total account. | Preserve per-source rows; do not demand universal non-F1 requests. | D/B + HQ + F |
| **R2-3. Route evidence labels are corrected.** `candidate_raw_total=5630`; `route_qualified_total=676`; `route_unknown_total=4705`; `route_rule_unavailable_total=249`. Family counts are no longer labelled route-qualified. | 5,630 candidate RAW operations are not 5,630 administratively qualified operations. Unknown route remains explicit and not a denominator-complete release. | Preserve split and 18,467 total plan. | D/B + source owner |
| **R2-4. Native wrapper remains HOLD.** Direct decode/read bypass, `max_items=3`, arbitrary coordinate fallback and synthetic ID/person unit are unchanged. | These are native integration residuals after A/C/source-read dependencies; no fixture substitute is called original fact. | Keep explicit NOT_READY. | D + A/C + source-read owner |

## 2. EXACT PROOFS

- Extra supplied operation → `GOVERNED_FRONTIER_NOT_EXACTLY_PLAN_DERIVED`; duplicate → same refusal; substituted operation material → same refusal; missing operation → same refusal; exact restore → baseline compilation hash.
- Value/conditioner mutation + corresponding rebuilt frontier → changed compilation/jobs/facts; exact restore unchanged (retained from accepted r1 identity/value subscope).
- All35 accounting: 35 sources; 20 explicit fronts; 15 no-explicit-request; 991 frontier operations; 21 eligible; 970 held/unknown; pending/deferred 0.
- Source plan: 18,276 items; 18,413 slots; 18,467 operations; no-drop true.
- Plan counts: `EXECUTABLE_RAW 5630`, `HELD 4655`, `INAPPLICABLE 8131`, `DEFERRED 51`, `ABSTAIN 0`.
- Current identity/occurrence/frontier plan ref: `aae15f52877e4eb0c61bfbfb47efc2d650d3289036ce38d3a76acee1b1e84e20`; historical `3e3a604a…` and status-repair `9ae291ca…` retained.

## 3. TESTS / EVIDENCE

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  -p no:cacheprovider --tb=short
8 passed in 29.26s
```

Evidence:
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/evidence/all35_frontier_accounting.json`
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/evidence/route_qualification.json`
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-B-20261106-R1/evidence/all35_plan.json`

## 4. CHANGED PATHS

`rawlsing_next/pre553_original35_operations.py`, `rawlsing_next/tests/test_pre553_original35_operations.py`, D/B evidence and this r2 return. No A/C/E/grammar/compiler/guide/controller edit.

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D/B r2 exact frontier
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; input 017337a9e.
- Function: explicit plan -> exact plan-derived ScientificFrontier; supplied frontier must match operation identity/material exactly; all35 per-source accounting includes 15 typed no-request rows.
- First consumer: current compile_governed_frontier on exact plan-derived frontier; native original facts remain NOT_RUN.
- Evidence: 8 tests; extra/substitution/duplicate/missing refusals and restore; 20/35 explicit, 15/35 no-request, 991/21/970 frontier counts; route 676/4705/249.
- Limits: D native wrapper HOLD; E authentic bind NOT_RUN; no native/science/protected acceptance.
```

## 6. LIMITS

All original native/I03/I05/Batch facts and E handoff remain `NOT_RUN`. No native/scientific/source grant, protected merge, self-review, provider/human call or global change.
