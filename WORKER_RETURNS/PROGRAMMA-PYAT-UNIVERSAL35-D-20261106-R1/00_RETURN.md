# PROGRAMMA PYAT — Universal35 D: A/B/C integration, B payload repair, original execution boundary

**STATUS:** `D_ABC_CANDIDATE_INTEGRATED__B_NONF1_PAYLOAD_WIRED__ALL35_MANIFEST_AND_ROUTE_SPLIT_READY__NATIVE_FACTS_NOT_COMPLETED__AUTHOR_RETURN_FOR_REVIEW`
**BRANCH:** `codex/pyat-universal35-d-20261106-r1`
**START:** `d129eebdb0472b0c3625efa281826a858bd0a384`
**INTEGRATED CANDIDATES:** A `51f39988863e049b09daf9cf4aeb30c09d5e84c2`, B `dd0249a0fc8588f9fa1a10fb9702295e5aabaa1a`, C `da5df57b237641bcf8597f6ba9ebfecf6b784e61`
**F REVIEW:** `ebd20c165bb275f66e4b3e2210535e96eecaf2ac` (B non-F1 REVISE; A/C ACCEPT_SCOPED; AB/ABC join REVISE)
**F SOURCE QUALIFICATION:** `43e5962bbad72501166da59b744d618d10877b22`
**E CONTRACTS READ:** E r1 `15da2b8bf71d1ee61d6b3040996436f8be537e06`; narrow repair `7d1aadfd4f655930ca2e65ea64cfa3df180a5f7b`; independent ACCEPT `6334063ab290d6497e7b8047eb1292b69661f51e`
**SOURCE ROOT:** runtime-only `USER_ORIGINAL35_DATA_ROOT`; no absolute path embedded in code or Git evidence
**RUNNER:** `/tmp/rawlsing-oct28-p1r1/venv/bin/python`; Python 3.11.3; pyreadstat 1.3.2; pandas 3.0.6
**GRADE:** sourcefree integration author evidence; no native/protected/science acceptance.

## 1. FINDING | INTERPRETATION | ACTION | OWNER

| FINDING | INTERPRETATION | ACTION | OWNER |
|---|---|---|---|
| **D1. Mandatory B non-F1 payload repair is implemented.** `build_frontier_inputs_from_plan` constructs CURRENT `SourceInventory`/`GrammarPolicy`/`ScientificFrontier` from actual planned F2/F3/F4 item codes, domains, conditioner values, joint arity and source SHA. `bind_governed_frontier` no longer accepts a disconnected synthetic frontier as proof; it checks planned payload presence and passes those exact preimages to `compile_governed_frontier`. | The previous code checked only physical short codes against a caller frontier. The repaired test removes the plan payload → RED; changes a planned domain value → different frontier/compilation/jobs; restores → exact original compilation hash. | F independent closure on this corrected head; do not mark F2–F4 consumed until accepted. | D/B author + F reviewer |
| **D2. B return counts are corrected to F's exact rebuild.** Current plan: `EXECUTABLE_RAW 5630`, `HELD 4655`, `INAPPLICABLE 8131`, `DEFERRED 51`, `ABSTAIN 0`, total `18467`. Historical `plan_ref` remains `3e3a604a78c377030bffa39eb62cf065d111746f9bc1588f7dbf33bac0373b9c`; status-repair recomputation is recorded as `9ae291ca403e3d26fd0e4af9b6c536fac9509be878e0d9cc43a589f293d14ff7`. | The old B return's `HELD 1595 / INAPPLICABLE 11191` is stale and superseded. | Preserve both exact references; do not rewrite the historical cut. | D/B + HQ |
| **D3. Route qualification is split before original execution.** Of 5,630 executable-RAW operations, only 676 are `ELIGIBLE_APPLICABLE`; 4,705 are `ROUTING_UNKNOWN`, 249 are `RULE_UNAVAILABLE`. F1 split is 663/4,583/244; F2 11/105/4; F3H 2/17/1. F4 remains 20 deferred. | Unknown routing is not administratively proven and cannot be a complete denominator. Observed response values may remain under explicitly scoped `ROUTING_UNKNOWN`; they are not a substitute for an administered estimate. | Keep 676 route-qualified operations moving; hold denominator-dependent unknown/rule-unavailable claims; preserve every observed value. | D + source/science owner |
| **D4. All35 manifest and source-path selection execute.** `SourceConfigLibrary.load_original(...).document` feeds the B plan; `select` is used only for compact runtime resolution metadata. All 35 resolve under the effective root; 18,276 items and 18,413 slots are accounted; no synthetic two-item substitution. | A's compact `select` is not the operation-plan document; use `load_original().document` as A's corrected ABI description says. | D consumes the full config document; A description repair only. | D + A |
| **D5. Native empirical facts are not yet produced.** SRC31 original SAV decode reached the current C11 factory but was typed-refused on unbound response values (exact source values absent from the current config response mapping). Selected route-qualified native-compiler attempts on SRC09/10/11/15 exceeded the 600s eager-decode bound before producing facts. | The state-count scaffold is not an `EmpiricalFact` and is not E/FF handoff. A bounded filtered `ExactPhysicalCellStream` is indispensable to avoid repeated full-frame decode and duplicate C11 build. C is now receiving that separate adapter task; its actual first consumer is the current factory stream API. | Do not claim I03/I05/Batch or N10E/FF facts. C stream adapter or an equivalent bounded current-owner stream is the exact dependency. | C stream owner + D + E reviewer |

## 2. FROZEN CURRENT INTERFACES

- B plan: `build_original35_operation_plan(document, *, source_presence=None, source_root=None, pair_budget=6, joint_budget=1, require_all35=True, expected_item_count=None, expected_physical_slot_count=None) -> Original35OperationPlan`.
- B frontier repair: `build_frontier_inputs_from_plan(plan, *, source_id=None) -> (SourceInventory, GrammarPolicy, ScientificFrontier)`; `bind_governed_frontier(plan, *, bundle, inventory=None, policy=None, frontier=None, source_id=None, as_of, host, purpose)`.
- D manifest/selection: `execute_source(source_id, *, library, source_root, state_root=None, allow_decode=True) -> SourceExecutionResult`.
- D current native path: `execute_native_compiler_source(source_id, *, library, source_root, host, purpose, as_of, max_items=3, state_root=None) -> dict`.
- Required stream contract: `ExactPhysicalCellStream(source_sha256, row_count, cell_iter_factory, decoder_metadata_digest)` over selected response + coordinate columns, preserving full declared row count and exact source SHA, without eager full-frame materialization.

## 3. EXACT COMMANDS AND RESULTS

```text
PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_operations.py \
  -p no:cacheprovider --tb=short
6 passed in 26.53s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_pre553_original35_execution.py \
  -p no:cacheprovider --tb=short
2 passed in 114.61s

PYTHONDONTWRITEBYTECODE=1 /tmp/rawlsing-oct28-p1r1/venv/bin/python -B \
  -m pytest -q rawlsing_next/tests/test_programma_pyat_original35_constructor_adapter.py \
  -p no:cacheprovider --tb=short
1 passed in 0.29s
```

Evidence:
- `evidence/all35_manifest.jsonl` — 35 source manifest rows, runtime root resolved, no decode.
- `evidence/route_qualification.json` — exact 676/4,705/249 split and F4 deferral.
- `evidence/native_attempts.json` — SRC31 typed C11 refusal and SRC09/10/11/15 600s eager-decode noncompletion; exact stream need.
- B evidence updated: `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-B-20261106-R1/evidence/all35_plan.json`.

## 4. CHANGED PATHS

- `rawlsing_next/pre553_original35_operations.py` — B non-F1 actual payload → current frontier/compiler; route-aware test.
- `rawlsing_next/programma_pyat_original35_constructor.py` — recovered P1 optional-weight and bounded accounting repairs.
- `rawlsing_next/pre553_original35_execution.py` — new D manifest/C11/bounded current-compiler bridge.
- `rawlsing_next/tests/test_pre553_original35_operations.py`
- `rawlsing_next/tests/test_pre553_original35_execution.py`
- `rawlsing_next/tests/test_programma_pyat_original35_constructor_adapter.py`
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-B-20261106-R1/evidence/all35_plan.json`
- `WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/**`

No A source_configuration, C kernel/stream adapter, E consumer, guide, protected file, global config, provider or other writer branch was edited.

## 5. PROGRAMMA_DELTA

```text
PROGRAMMA_DELTA — Universal35 D integration
- Identity: codex/pyat-universal35-d-20261106-r1@<returned-commit>; start d129eebdb0472b0c3625efa281826a858bd0a384; A/B/C candidates integrated sourcefree.
- Function/input-transform-typed-output: R157 full config document -> B 35-source no-drop plan -> route-qualified/unknown/rule-unavailable split -> actual planned F2/F3/F4 inventory/policy/frontier -> current compile_governed_frontier/compile_universal_workload. Manifest/selection and typed source residuals are real; native fact production awaits bounded current stream.
- Root/schema/clock/permission: runtime source root alias only; B plan PRE553_ORIGINAL35_OPERATIONS@1.0.0; no native/source/science grant.
- Actual first consumer: current R03 compiler payload for B actual F2/F3/F4 (sourcefree fixture); current C11 factory reached on SRC31 but typed-refused unbound mapping. No I03/I05/Batch EmpiricalFact or N10E/FF handoff claimed.
- Evidence: B 6 tests, D 2 tests, P1 1 test; route 676/4705/249; all35 18276/18413; native attempts typed.
- Affected IDs: S02.2/S02.3/S02.4/GAP-006/007/009/010 candidate evidence only; no protected status overwrite.
- Next action: C bounded stream adapter / D actual route-qualified original fact run; F exact-cut closure of B repair; E repaired ingress only after authentic fact/query.
```

## 6. LIMITS

- Native I03/I05/Batch facts, replay/checkpoint on original source, N10E/FF handoff: `NOT_RUN`/`NOT_COMPLETED`.
- SRC31 C11 mapping refusal is an exact source-config residual, not source unavailability and not a native product.
- All35 source bytes are present by custody; no `SOURCE_NOT_PRESENT_HERE` claim.
- E independent ACCEPT is preserved; D did not produce the authentic E bind and does not mark E source-ready.
- No self-review, protected merge, native grant, provider/human call or new science/structural authority.
