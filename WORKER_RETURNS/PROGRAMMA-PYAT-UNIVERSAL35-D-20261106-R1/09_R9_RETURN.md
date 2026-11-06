# PROGRAMMA PYAT — Universal35 D r9: explicit transport permission and no-drop corrections

**STATUS:** `D_R9_TRANSPORT_PERMISSION_EXPLICIT__MISSING_QUERY_FAIL_CLOSED__E_ARITY_REFUSALS_EXACT__ORIGINAL_FACTS_HOLD`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `9161ba719f327867db78e084357245e369bc1195` / code `7ff5e8b78c242317f4b9d20d269c48893c38ab41`

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R9-1. Envelope production requires explicit caller permission.** `execute_native_compiler_source` accepts optional `producer_permission_ceiling`, default `None`. `state_root` alone does not write envelopes; `None`, empty or invalid ceiling refuses before artifact write. | No automatic `FIELD_FORGE_RELATION_PRODUCTION` minting and no widening of sourcefree grade. | Preserve explicit caller permission. | D + E |
| **R9-2. Missing exact query refuses before partial artifact.** `write_field_forge_envelopes` collects all fact query refs; if any exact existing query is absent it raises `FIELD_FORGE_QUERY_REF_MISSING` before writing the artifact. | No fact is silently dropped while claiming fail-closed. | Fail before publish, or implement full typed missing-query disposition later if required. | D + E |
| **R9-3. E arity results are exact.** Current governed fixture has 30 facts, all 1-target. All 30 envelopes are written with caller ceiling unchanged; E returns exactly 30 typed `FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED` refusals and `structural_grant=false`. | A 2-target joint producer is still required for a positive E conditional-support profile. No roles/arity are relabeled and no joint facts are fabricated. | Keep 1/3+/weighted facts in transport; accept typed refusal. | D + E |
| **R9-4. Cold CLI and fail-closed checks pass.** JSON persists/reloads; exact cold CLI returns the typed arity refusal; missing permission and changed replay fact ref fail closed. | Sourcefree transport is proven; it is not an authentic original/native handshake. | Continue after A/C original fixes. | D + E + G |

## 2. TESTS

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py::test_governed_facts_queries_become_exact_cold_e_envelopes \
  -p no:cacheprovider --tb=short
1 passed in 2.37s
```

Exact observed: 30 facts / 30 envelopes / 1-target arity 30 / E typed arity refusal 30 / structural grant false. No artifact written for missing/empty ceiling or missing query. Caller ceiling round-trips unchanged in every envelope.

## 3. PRESERVED / LIMITS

- 35 sources; 18,276 items; 18,413 slots; 18,467 operations; route `676/4705/249`; frontier `7/694/683/11`; 28 typed no-route sources.
- Actual original facts remain `NOT_RUN`; A coordinate and D/C scale blockers unchanged. No 650s rerun.
- No new fact/query/statistics/compiler/authority, no E codec edit, no A/C semantic edit, no protected/native/science change.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r9 explicit E transport
- Identity: codex/pyat-universal35-d-20261106-r1@fbc6ca3eb1246aa6a946c558a5f6e30dedafeb45; input 9161ba719.
- Function: existing governed facts/query/replay/provenance + explicit caller producer permission ceiling -> exact E envelopes; missing query fails before artifact; no automatic transport.
- Evidence: 30 facts/30 envelopes/30 typed arity refusals; cold CLI typed refusal; permission/replay fail-closed; caller ceiling unchanged.
- Limits: 2-target positive joint producer still missing; actual original facts/E handshake NOT_RUN; no native/science/protected acceptance.
```

## 5. BOUNDARY

Author evidence only; no fabricated permission/issuer/fact/query, no role/arity relabeling, no protected merge/self-review. Independent focused review requested.
