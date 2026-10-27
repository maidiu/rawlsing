# X04 M25 — yearly ordered causal spine

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `PARTIAL_WRONG_MEANING` for the yearly unit; `MEANINGFUL_COVERAGE` for explicit dependency order, fail-fast derived scheduling and replay hashes.
**Authority:** historical source only; no native rule/source grant.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `run_one_year` | `v3/engine/yearly_step.py:12-99` | state, derived, config, step order → mutated state/derived | Executes configured steps, clamps, derives, increments year/age, pressure flow |
| `step_one_year` | `yearly_step.py:102-110` | same → derived | Convenience wrapper |
| `_run_step` | `yearly_step.py:113-151` | step id → module call | Dispatch table |
| `_compute_derived_after_step` | `yearly_step.py:173-191` | step/schedule → derived updates | Checks schedule equality and computes all derived |
| `run_n_years` | `v3/engine/step_runner.py:13-29` | state, n → final state + optional JSON per year | Loops annual `run_one_year`; no event/interval loop |
| `v3_yearly_step_order.yaml` | `v3/v3_yearly_step_order.yaml` | config | 19 core steps; 20 actual configured steps (appends `active_magnets_update`) |

**Reads/writes:** `run_one_year` reads `state` and the passed `DerivedIndices`; resets `micro_trace_this_year`/`yearly_integrity`; calls every step in order; clamps after each; writes `year/age`; runs pressure flow; may write `rendered_output` via `render_layer`; writes `yearly_integrity` diagnostics. It does not read a real event clock.

## 2. Actual order

The configured steps are:

`field_update → autonomy_safety_micro_drift → event_sampling → reproduction_constraints_update → capacity_update → health_drift_update → buffers_update → frameworks_update → domains_update → cracks_and_alienation_update → plasticity_and_metabolization_update → stability_inertia_dissipation → striving_update → practice_and_infrastructure_update → topology_and_boundary_update → attention_and_capture_update → strategy_and_signal_effects → style_trait_drift → render_layer → active_magnets_update`.

`core_steps` has **19** entries and excludes the appended `active_magnets_update`; `test_architecture_invariants.py:89-120` asserts the core as an ordered subsequence and `extension_policy=append_only`. This is a real explicit order, but the actual list is 20 steps, not 19.

After the loop, `state.year += 1; state.age += 1` (`yearly_step.py:56-57`), then `run_pressure_flow_cycle(state)` (`:68-70`). `render_layer` therefore executes before age increment and before pressure flow; `active_magnets_update` executes after render. The server/runner calls `run_llm_band_year` **after** `run_one_year` at selected ages (`server/generation/simulation.py:538-549`; `v3/run_and_print.py:123,130-139`).

## 3. Temporal violations / limits

- **Year is the single causal unit.** `run_one_year` has no event timestamp, interval, event ordinal, actor-access clock or between-event computation. All events in `events_this_year` are consumed by annual steps.
- **Mechanical event sampler inside the year:** `event_sampling` writes 0–3 generic events; later steps read them. There is no event-by-event resolution.
- **LLM events outside the year ledger:** `run_llm_band_year` applies selected LLM events after the annual step and after `year/age` increment, but does not append them to `state.events_this_year`; the server's `year_record["event_ledger"]` is the mechanical event list, while LLM selections live only in `llm_band_ledger`. This is a two-ledger temporal defect.
- **Render timing:** `render_layer` inside the year calls `render_year` without packet (minimal output); the server may call `render_year` again for non-LLM years and can overwrite a structural annotation scene. `run_llm_band_year` renders again after deltas.
- **Derived side effects:** `_compute_derived_after_step` calls `compute_all_derived`, which writes `state.registers` and `state.metabolic_style` (see M38), outside the declared step mutation set.
- **No legitimate interval/no-event semantics:** a 0-event year still runs all annual steps, increments age/year and runs pressure flow; there is no typed no-change/continuity record.
- **Secretarial ordering vs causal order:** `render_layer` and `active_magnets_update` are in the annual step list, not in a retrospective call; the old schedule conflates state transition, annotation and rendering.

## 4. N06/N11 differential

N06 needs activity/time/participation and interstitial life. N11 needs a batch of 3–5 conditional events resolved sequentially with independent coactors and intervening time. The old scheduler supplies **explicit ordering, derived-schedule discipline, clamping, hashes and a runnable annual slow loop**, but not the event/interval causal unit. The scheduler must be retained as a **slow-process integrator** around a new event/interval scheduler, not used as the batch itself.

**Coverage:** `PARTIAL_WRONG_MEANING`; retain ordering/fail-fast/replay, adapt clocks, create batch/event/interval spine.

## 5. Tests / first consumer

Reviewer focused evidence: `test_architecture_invariants.py` 4 passed, `test_step_logic.py` 12 passed, `test_step_sanity.py` 3 passed, `test_distribution_smoke.py` 1 passed (50 agents × 20 years). Tests assert order, event non-mutation of domains/peak routing, derived non-storage (fixed list only), run stability, not event/interval semantics.

Current/historical consumer: `server/generation/simulation.py` and `v3/run_and_print.py` call `run_one_year`; no current C9/C12 person loop. First actual consumer is the annual server runner and `year_record` writer; no event-level consumer.

## 6. Disposition

**Retain:** explicit step order, core subsequence test, clamp/fail-fast, derived-schedule equality, year-record hashes. **Adapt:** `run_one_year` into a slow-time/interval integrator driven by canonical event/interval clocks; make render/annotation separate. **Create:** `BatchScheduler`, `CanonicalEventLedger`, event/interval clocks, sequential per-event carry-forward.

**Owner:** C6/C8/C9/C12 scheduler owner after scientific/current-source decisions. **Negative:** a 0-event year changes age/year/pressure flow, so it is not a continuity/no-change interval; event-1 alteration cannot affect event-2 reception because there is no event sequence.
