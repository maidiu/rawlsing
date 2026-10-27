# X04 M38 — dual derived-schedule declaration and stored/derived ordering

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `PARTIAL_WRONG_MEANING`; fail-fast equality is real, but `compute_all_derived` writes persistent backbone fields.
**Authority:** historical scheduler policy; no native rule.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `derived_indices_schedule` | `v3/v3_yearly_step_order.yaml:21-36` | index → step | Top-level schedule |
| step-local `derived_compute` | YAML steps (e.g. `:148-149,165-166,181-182`) | step → index list | Second declaration |
| `get_derived_schedule` | `v3/core/config_loader.py:61-67` | YAML → dict | Loads top-level schedule |
| `_compute_derived_after_step` | `v3/engine/yearly_step.py:173-191` | step/schedule/derived → updates | Equality assertion + computes all derived; copies selected fields |
| `compute_all_derived` | `v3/core/derived.py:322-359` | state → DerivedIndices | **Writes** `state.metabolic_style` and `state.registers` |
| `state_to_json/state_from_json` | `v3/io/json_codec.py` | state ↔ JSON | Persists `registers`, `metabolic_style` |
| `assert_no_derived_fields_in_backbone` | `v3/core/invariants.py:346-350` | class fields | Only checks a fixed `DERIVED_INDEX_NAMES` set |

## 2. Actual behavior

- Two schedule surfaces exist. `_compute_derived_after_step` compares `compute_after` from the top-level schedule with the step's `derived_compute`; mismatch raises `AssertionError` (reviewer probe: `step-local=[] schedule=['hostage_index']`).
- It calls `compute_all_derived(state)` for any scheduled field; `compute_all_derived` recomputes all indices **and writes** `state.metabolic_style` and `state.registers` (`derived.py:332-334`). These are stored BackboneState fields and survive JSON roundtrip.
- The equality test is real and useful, but it does not prevent hidden derived writes; `assert_no_derived_fields_in_backbone` excludes `registers`/`metabolic_style` from its fixed name set.
- `derived` object is not stored as a separate cache (`store_derived_cache:false`); only selected fields are copied into the passed `DerivedIndices`; `state.registers`/`metabolic_style` are de facto derived caches in backbone.
- Tests: `test_architecture_invariants.py::test_step_order_immutable` 4 tests; no test of schedule mismatch or hidden derived writes; reviewer probe.
- `run_n_years` computes derived at start and after scheduled steps; it does not recompute after arbitrary non-scheduled steps; `derived` can be stale for unscheduled fields.

## 3. N06/N11 differential

N06/N11 need an event/interval scheduler with a canonical derived registry and no accidental causal overwrite. M38 provides:
- a real fail-fast consistency check between two schedule surfaces;
- selected derived computation at declared steps;
- but hidden writes (`registers`, `metabolic_style`) and a fixed-name invariant that misses them.

**Coverage:** `PARTIAL_WRONG_MEANING`; retain fail-fast equality and explicit derived schedule; adapt to a canonical registry/event clock; remove hidden writes or declare them explicitly.

## 4. Disposition / first consumer / owner

**Retain:** schedule equality assertion, explicit derived order, no persisted `DerivedIndices` cache.
**Adapt:** one canonical registry; include `registers`/`metabolic_style` in stored/derived classification or stop writing them in `compute_all_derived`; map to event/interval.
**Create:** `DerivedRegistry` with event/interval triggers and fail-closed provenance.

First consumer: `run_one_year`/`run_n_years`; `derived` passed to steps and summary; no current C9/C12.

**Owner:** V3/Pyat/C9 scheduler owner; no native grant.

**Negative/fault:** a schedule mismatch raises (good), but a `compute_all_derived` call during a step changes registers/inner load that pressure flow later reads; this is a hidden causal write not represented in the step contract.
