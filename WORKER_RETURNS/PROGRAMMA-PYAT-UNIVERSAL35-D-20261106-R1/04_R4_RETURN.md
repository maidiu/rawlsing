# PROGRAMMA PYAT — Universal35 D r4: governed non-F1 execution bridge and source-read currentness

**STATUS:** `D_R4_FULL_PLAN_GOVERNED_BRIDGE_INTEGRATED__SOURCE_READ_DECISION_TYPED_HOLD__NO_NATIVE_FACTS_CLAIMED`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `3fc9af676ec1ad695c3a3f55a009aa26ae4e3c18`; code `0e36e9a7c6567bfda3395d08bcb32dc386ea8e78`
**C:** `12d44c9d2418d7ab0cbcb92b4daa48d6a2cf20f3` / code `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a`; G `a66e4a628f3e6e7b819097a15ace86cc1877022e`
**E:** cold envelope `bddef0b5ca40b750fd51770d47df22f2973679b4` / code `f708b4688f6aebd408510aa33faca453bd213749`; G review active; not accepted native handoff.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R4-1. Native execution now consumes the full explicit plan, not F1-only.** The bridge selects route-qualified F1/F2/F3H operations, builds the native bundle/catalog, and calls the existing `bind_governed_frontier` → `compile_governed_frontier` → `execute_governed_frontier` path. | The accepted non-F1 plan path is connected to the current governed compiler/consumer. F4 remains deferred for same-person current-reader proof. | Keep exact plan-frontier identity checks and route split. | D/B + F |
| **R4-2. Source-read admission is mandatory.** `incidence` no longer bypasses admission. A caller-supplied current resolver is required; source bytes are opened only through `decode_config_with_source_read_permission`. Pre- and post-execution currentness/revocation are checked. No resolver refuses before response I/O. | No fabricated resolver, issuer or authority refs. A test/fixture resolver would be engineering only and cannot stand for original permission. | Actual original run waits for a genuine current decision. | D + source-read owner |
| **R4-3. Unit/occurrence/ID/coordinate are source-derived.** Package rules use original item IDs and physical codes from the plan, unit from the plan's source fact, and exact config/respondent coordinate facts. There is no hardcoded person unit, arbitrary coordinate fallback, synthetic ID, or default 3-item final cap. `max_items` is explicit diagnostic only. | Household/repeated facts remain typed; no conversion to person or silent truncation. | Preserve sourcefacts and typed holds. | D + A/C |
| **R4-4. All35 accounting separates plan scope from executable frontier.** Every source has full F1/F2/F3/F4 plan counts. 20 sources have non-F1 planned requests; 15 have none. Route-qualified executable frontier currently covers 7 sources (694 operations: 683 eligible / 11 held-or-unknown); 28 sources have no route-qualified explicit frontier and retain typed plan-only accounting. | The earlier 20/35, 991-operation result remains historical. It is not replaced by an invented all35 candidate fact set. | Report both scopes; do not invent F2-F4 or route qualification. | D/B + HQ + F |
| **R4-5. Actual original facts remain unrun.** No current source-read decision was supplied for the original root; the bridge therefore typed-refused before I/O. | Local original engineering authorization is not a fabricated native/S3 issuance. Code/accounting tests proceed independently. | Source-read owner input required for actual original facts; E handshake only on authentic two-target RAW fact/query. | source-read owner + D + E |

## 2. EXACT RESULTS

```text
C physical stream tests: 7 passed in 1.43s
D execution tests:       3 passed in 118.86s
B operations/accounting: 8 passed in 30.05s
```

- Plan: 35 sources; 18,276 items; 18,413 slots; 18,467 operations; no-drop true.
- Counts: `EXECUTABLE_RAW 5630`, `HELD 4655`, `INAPPLICABLE 8131`, `DEFERRED 51`, `ABSTAIN 0`.
- Route: `676` qualified / `4705` unknown / `249` rule-unavailable.
- Plan ref: `aae15f52877e4eb0c61bfbfb47efc2d650d3289036ce38d3a76acee1b1e84e20`.
- Current route-qualified frontier account: 7 explicit sources; 694 frontier ops; 683 eligible; 11 held-or-unknown.

Evidence: `evidence/all35_frontier_accounting.json`, `evidence/route_qualification.json`, `evidence/native_bridge.json`.

## 3. CHANGED PATHS

`rawlsing_next/pre553_original35_execution.py`, `rawlsing_next/tests/test_pre553_original35_execution.py`, C received module/test, D evidence/returns. No A source_configuration, B operation/grammar, C semantics beyond received file, E consumer, guide/controller or protected edit.

## 4. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r4 governed bridge
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; input 3fc9af676.
- Function: full explicit route-qualified F1/F2/F3H plan -> native bundle/catalog -> current bind_governed_frontier/compile_governed_frontier -> execute_governed_frontier facts; source bytes only through current source-read resolver.
- Evidence: C 7 tests; D 3; B 8; plan 18276/18413/18467; route 676/4705/249; frontier 7 sources/694 ops.
- Limits: no current original source-read decision -> actual original facts NOT_RUN; F4/3+ same-person current-reader proof deferred; E authentic two-target handshake NOT_RUN; native/science/protected authority unchanged.
```

## 5. LIMITS

No fabricated original resolver/permission, native/science grant, protected merge, self-review or global change. Actual original facts, E/N10E/FF handoff and full wrapper readiness remain `NOT_RUN`/`HOLD`.
