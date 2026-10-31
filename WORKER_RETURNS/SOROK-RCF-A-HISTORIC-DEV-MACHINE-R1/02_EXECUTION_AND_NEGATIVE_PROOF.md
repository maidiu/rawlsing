# Execution and negative proof

## 1. Archive and runtime

- Archive: `/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging.zip`.
- Observed container SHA-256: `3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289`.
- TD-R05 expected container SHA-256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`.
- **Status: container hash mismatch.** The archive contents were nevertheless checked against the TD-R05 selected-file manifest: 36 of 40 M rows have at least one exact TD-R05 file-hash match; the key `v3/core/state.py`, `derived.py`, `invariants.py`, `yearly_step.py`, `step_runner.py`, `psyche/flow.py` and selected V2 files match. This is selected-file provenance, not whole-archive provenance.
- Python 3.11.3; pytest 9.1.1. The host lacked PyYAML; `PyYAML 6.0.3` was installed into a temporary target only, satisfying the archive’s `pyyaml>=6.0` requirement. No source file was edited.

## 2. Actual tests run

```sh
cd /Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging
PYTHONPATH=<tmp-pyyaml>:<archive> PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest v3/tests/test_architecture_invariants.py -q -p no:cacheprovider -o addopts=''
# 4 passed

PYTHONPATH=<tmp-pyyaml>:<archive> PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest v3/tests/test_step_logic.py -q -p no:cacheprovider -o addopts=''
# 12 passed

PYTHONPATH=<tmp-pyyaml>:<archive> PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest v3/tests/test_v5_pressure_flow.py v3/tests/test_v5_pressureflow_golden_run.py -q -p no:cacheprovider -o addopts=''
# 24 passed
```

Selected total: **40 passed**, 0 failed/errors/skips. These are real unchanged archive tests. TD-R05’s reported **80-test aggregate was not rerun** and is not claimed.

### Named mutation severance

A copied V3 tree (not the archive) changed only `steps` order in `v3/v3_yearly_step_order.yaml`: `render_layer` moved before `field_update`. The unchanged assertion was:

```sh
PYTHONPATH=<tmp-pyyaml>:<copied-v3> python3 -m pytest \
  v3/tests/test_architecture_invariants.py::test_step_order_immutable -q -p no:cacheprovider -o addopts=''
```

Result: **1 failed**, with `AssertionError: Core step id 'render_layer' missing or out of order in steps...`. This is the named core-spine subsequence failure, not an import/setup exception. The original archive and source were unchanged.

## 3. Central historical functions inspected

| Function/file | Actual role | Source evidence |
|---|---|---|
| `BackboneState` `v3/core/state.py:501` | persistent actor/world state bag; 50+ fields including derived-adjacent, registers, pressure-flow, readiness | dataclass fields at lines 501–566; `clamp_all` 568+ |
| `YearRecord` `v3/core/year_record.py` | year hash/event/micro-trace persistence | file SHA `4bbd7518…`; selected manifest match |
| `run_one_year` `v3/engine/yearly_step.py:12` | config-driven 19-step execution, clamp, derived schedule, post-year pressure flow | 19 core IDs in `v3_yearly_step_order.yaml`; `run_n_years` in `step_runner.py:13` |
| `compute_all_derived` `v3/core/derived.py:322` | computes indices from stored state and writes only `metabolic_style`/`registers` per contract | 322–370; test `test_no_derived_fields_in_backbone_state` |
| `_domain_charge_ledger` `v3/psyche/flow.py:406` | per-domain charge/route/conductance/insulation ledger | 406–460 |
| `_channel_conductance` `v3/psyche/flow.py:366` | bounded groove/capacity/support/repression trace effect | 366–404; no extra conserved charge by docstring |
| `_update_memory` `v3/psyche/flow.py:678` | lifetime/recent averages, dominant channels, groove decay | 678–751 |
| `run_pressure_flow_cycle` `v3/psyche/flow.py:753` | transactional post-year membrane; snapshot/history/memory/surface/analyst built before live commit | 753–850; `PressureFlowError` diagnostic/re-raise |
| `render_year` `v3/render/phenomenology.py:55` | render-only output; no backbone mutation | test `test_llm_no_backbone_mutation` passed |
| `prepare_conversation_turn` `v2/conversation_engine.py:2079` | V2 person context → analysis → hooks → appraisal → move → prompt | V3-under-V2 one-way membrane; no direct C9 writer |

## 4. Preserved positive machinery

- **M01/M26:** explicit persistent state and stored-versus-derived separation are real; `DerivedIndices` is computed, not stored; `test_no_derived_fields_in_backbone_state` passes.
- **M25:** the 19-step core spine is real and config-driven; `test_step_order_immutable` passes unchanged; a copied order mutation fails the same assertion.
- **M21:** pressure-flow is a real transactional membrane with charge ledger, conductance, memory and analyst/surface separation; 24 pressure-flow tests pass.
- **M29/M30:** render is nonmutating; V2 conversation is a downstream surface; `test_llm_no_backbone_mutation` passes.
- **M38:** derived schedule is declared twice but fails fast on mismatch; `yearly_step.py:120–135` (see `_compute_derived_after_step`) preserves consistency.
- **M40:** clean_ready/degraded_ready/blocked readiness exists in `server/generation/store.py:245–320`; `GenerationIntegrityAccumulator` and `_generation_state_is_ready` are real.
- **M37:** structural stub scenes are explicitly excluded from persona scenes and memory distillation; the stub is quarantined, not narrativized.

## 5. Invalid or scientifically overclaimed mechanisms

### M08 identity-seeded wound

`v3/psyche/channels.py:36` `seed_wound_vector_from_identity` reads `class_origin`/`current_class`, `minority_status`, `religiosity_level` and age, then applies class-based wound deltas. This makes demographic/structural identity determine sensitivity. Quarantine the seed; sensitivity must come from warranted situations and responses.

### M15/M36 missing-parent and hopeful defaults

`v3/io/parent_baseline_from_behavior.py:25–67` defaults absent warmth/authority/material support to `50.0`, then maps low/high values to expectation labels; `v3/engine/expectation_baseline.py:107–142` defaults parent axes to `hopeful`. This converts unknown care into normal/medium/hopeful defaults. Deep rework/remove; unknown must stay unknown/held.

### M34 fabricated fallback

`v3/engine/llm_contract.py:159–207` creates a fallback practice/relationship event when the candidate packet is empty; `v3/engine/run_llm_band.py:242–252` takes the first candidate when scoring selected nothing. This manufactures a year of development. Remove; no event/insufficient evidence must remain explicit.

### M35 placeholder personality

`v3/core/invariants.py:253–297` appends placeholder cracks/frameworks (`type="placeholder"`, weight 5.0) and marks placeholder repair degraded; `yearly_step.py:24–30` calls the repair before every year. Preserve degraded diagnosis, but never treat placeholders as lived content.

### M39 random rupture injection

`v3/engine/effects/metabolization_effects.py:273–332` uses module-global `random.random()` and `random.choices()` at age bands to create `RuptureShard`/`MetabolizationProcess` outside the year event ledger. Replace with admitted C8/world event provenance; no arbitrary age ritual.

### M31 type-determines-person

Old Enneagram/type inference is present in `v2/enneagram_wisdom.py`/`parent_type_inference.py` but has no current authoritative developmental engine in this cut. Quarantine; do not treat type as person.

### M37/M38/M40 boundaries

M37 stubs remain excluded from persona reconstruction; M38 fail-fast is preserved; M40 readiness is real but is not native source authorization or a science grade. The invalid part is any promotion of readiness to personhood.

## 6. Targetless/contemporary interfaces

No old V3 code is directly imported into current BP2P4J, R31J, C9/C12 or Pyat R15. `R31JProduct`/`JoinedProduct` are comparative current sourcefree consumers, not old-V3 call sites. The current Pyat R15 apparatus is not the old V3 M25 scheduler; no cross-cut acceptance is borrowed. The first current consumer is **UNPROVEN**; historical first consumers are `run_one_year` (scheduler), `compute_all_derived` (derived), `run_pressure_flow_cycle` (flow), `render_year` (render) and `prepare_conversation_turn` (V2).

## 7. Scientific anchors

No primary texts for Leontiev, Sève, Lahire, Dreier, Holzkamp, Archer, Kohn/Schooler, Elder or social reproduction were present in the archive. The repository documentary references do not supply passages. **No primary passage was read and no scientific claim is issued.** The old code’s psychological content remains a historical/contingent hypothesis, not an authorized machine rule.

## 8. FINDING / INTERPRETATION / ACTION / OWNER

**FINDING:** the archive provides real state/derived/scheduler/flow/render machinery, but several mechanisms encode demographic determinism, missing-as-normal defaults, fabricated fallback events, placeholder personality and random ruptures.

**INTERPRETATION:** the recoverable asset is a portable computational skeleton plus a quarantine map, not a validated developmental science.

**ACTION:** owner selects the skeleton and approves/rejects quarantines and N11 coexistence; no direct integration.

**OWNER:** original V3/V2 owner; CAN/ADP/CAN011/ADP016/017 owners; Sorok HQ; separate reviewer.
