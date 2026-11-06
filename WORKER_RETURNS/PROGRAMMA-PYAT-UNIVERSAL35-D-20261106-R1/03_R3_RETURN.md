# PROGRAMMA PYAT — Universal35 D r3: native execution bridge with C bounded stream and source-read admission

**STATUS:** `D_R3_NATIVE_BRIDGE_INTEGRATED__C_BOUNDED_STREAM_RECEIVED__SOURCE_READ_DECISION_TYPED_HOLD__NO_NATIVE_FACTS_CLAIMED`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**INPUT:** `a31175cbd1371c599e2855e150ba3beb877c4ed4`
**C RECEIVED:** module/test from `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a`; C head `12d44c9d2418d7ab0cbcb92b4daa48d6a2cf20f3`; G `a66e4a628f3e6e7b819097a15ace86cc1877022e` ACCEPT_SCOPED_ENGINEERING
**A MAPPING:** `ef43bbbb…` remains F review pending; `df229973…` accepts SRC31 factual mapping/source neutrality scoped while mechanism binding-contract remains REVISE. No A source_configuration edits.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **R3-1. C bounded physical stream is now the D selected-column transport.** `execute_native_compiler_source` uses `bounded_physical_cell_stream(incidence, include_variables=selected_plan_codes+coordinate)` instead of decode-then-filter-every-cell. | The C module/test was selectively received from the accepted C cut. No C source edit was made. | Use C after its independent scope remains preserved. | D + C + G |
| **R3-2. Direct decode bypass is removed from the final path.** The function accepts either a caller-admitted `PhysicalSourceIncidence` or a caller-supplied current source-read `resolver`; otherwise it refuses `CURRENT_SOURCE_READ_DECISION_REQUIRED_BEFORE_IO` before response I/O. | This runs the existing `decode_config_with_source_read_permission` admission path, not a fabricated permission. A test-only resolver is not treated as original authorization. | Keep typed no-current-decision as a finite blocker; supply a real current decision from its owner for actual original facts. | D + source-read owner |
| **R3-3. Final-path assumptions are removed.** No default 3-item cap; `max_items` is explicit diagnostic only. Coordinate must come from an exact config coordinate slot or the source is typed held. Original IDs come from the B plan; physical codes remain separate aliases. Household topology is typed held, not converted to person. | Diagnostic probes remain labeled and do not substitute for full coverage. | Continue actual source execution when admission is supplied. | D + A/C |
| **R3-4. Current compiler consumer is still the R03 path.** The bridge compiles/executes the selected package through `compile_universal_workload`/`execute_universal_workload`; no second compiler or custom state counter is used as a fact. | Actual original I03/I05/Batch facts were not produced because no current source-read decision was available in this run. | Do not claim native facts/E handoff. | D + E reviewer |

## 2. COMMANDS / RESULTS

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_physical_stream.py \
  -p no:cacheprovider --tb=short
7 passed in 1.43s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py \
  -p no:cacheprovider --tb=short
3 passed in 121.24s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  -p no:cacheprovider --tb=short
8 passed in 29.26s
```

Evidence: `evidence/native_bridge.json`.

## 3. PRESERVED ACCOUNTING

- 35 sources; 18,276 original items; 18,413 physical slots; 18,467 operations; no-drop true.
- `EXECUTABLE_RAW 5630` candidate RAW = `676` route-qualified + `4705` route-unknown + `249` rule-unavailable.
- Explicit frontier account: 20 sources with planned non-F1 frontier; 15 typed no-request; 991 total frontier ops (21 eligible / 970 held-or-unknown).
- F4 remains 20 deferred pending actual same-person current reader proof.

## 4. CHANGED PATHS

- `rawlsing_next/pre553_original35_execution.py` — admission/C-stream bridge, no default3/arbitrary coordinate/synthetic ID/person assumptions.
- `rawlsing_next/tests/test_pre553_original35_execution.py` — no-current-decision refusal and manifest checks.
- `rawlsing_next/pre553_original35_physical_stream.py` — C module received from exact C commit.
- `rawlsing_next/tests/test_pre553_original35_physical_stream.py` — C test received.
- D `03_R3_RETURN.md`, `evidence/native_bridge.json`.

No A source_configuration, B operation/grammar, C semantics beyond received file, E consumer, guide/controller or protected file edit.

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D r3 native bridge
- Identity: codex/pyat-universal35-d-20261106-r1@0e36e9a7c6567bfda3395d08bcb32dc386ea8e78; input a31175cb.
- Function: admitted incidence/resolver -> C bounded selected-column ExactPhysicalCellStream -> NativeSourcePackage (original IDs + physical aliases) -> current compile_universal_workload/execute_universal_workload.
- First consumer: current R03 universal compiler; actual original facts NOT_RUN because no current source-read decision in this run.
- Evidence: C stream 7 tests; D execution 3 tests; B 8 tests; all35 accounting preserved.
- Limits: source-read decision owner required for actual original run; E authentic handshake NOT_RUN; native/science/protected authority unchanged.
```

## 6. LIMITS

Actual original native facts, E/N10E/FF handoff and full wrapper readiness remain `NOT_RUN`/`HOLD`. No fabricated source grant, resolver, native/science authority, protected merge or self-review.
