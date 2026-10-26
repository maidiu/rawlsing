# X02 M21 — pressure-flow history / memory / grooves / conductance

**Court:** HISTORICAL_V3 / EXACT_MECHANISM.
**Historical code grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN` (direct read; 82 focused tests passed).
**Current Sorok integration:** `UNTRACED` — historical V3 `run_one_year`/`run_llm_band` only; not a current person consumer.
**Scientific grade:** `PARTIAL_WRONG_MEANING` overall; `MEANINGFUL_COVERAGE` for transactional accounting/provenance; `MISSING` for event-conditioned multi-stream psychology.
**Authority:** no native/source/rule grant.

## 01 Direct source map

| Function | Source | Role |
|---|---|---|
| `run_pressure_flow_cycle` | `v3/psyche/flow.py:753-843` | Post-year membrane; assigns channels, computes load/gating/charge/routes/memory/surface; commits |
| `_derive_current_charge` | `flow.py:268-284` | Structural load × inner-load factor × wound factor |
| `_domain_charge_ledger` | `flow.py:406-465` | Per-domain current/overt/internal charge, conductance, trace, vessel/insulation labels |
| `_channel_conductance` | `flow.py:366-403` | Bounded multiplier from groove, vitality, agency, aperture, support, network/repression, practice, relational field |
| `_prior_groove` | `flow.py:262-265` | Reads prior channel groove |
| `_update_memory` | `flow.py:678-750` | Aggregate trace memory, dominant/recent channels, historical relation, groove decay/increment |
| `_simulate_domain_routes_transactionally` | `flow.py:547-567` | Deep-copy route application |
| `_apply_single_domain_route` | `flow.py:500-544` | Channel-specific scalar/categorical writes |
| `_commit_route_state` | `flow.py:570-573` | Commit seven route objects |
| `_pick_channel` | `v3/psyche/channels.py:190-191` | One winning channel per domain |

Callers: `v3/engine/yearly_step.py:68-70` (post-year); `v3/run_and_print.py:123,130-139` (yearly then optional LLM band); tests listed in the shared atlas.

**Reads:** `domains` baseline_load/A/S/V/expressed_aim/affect_channel/buffer_type, `registers.inner_load`, 7 wounds, psych capacity, material capacity, practice, peak routing, collective infrastructure, strata stack/salience, pressure_flow_memory/history, year/age, events_this_year/micro_trace counts.

**Writes:** pre-route: `domain.affect_channel`, `domain.baseline_load`, `domain.expression_rate`, `domain.expressed_aim`; route: capacity/psych capacity/practice/peak routing/intensity/style/wound; memory/history/surface/analyst; yearly integrity/diagnostics.

**Does not write:** `domains.A/S/V/Aim`, strata, frameworks, buffers, cracks, striving objects, active magnets.

## 02 Actual formulae and conditions

- `current_charge = clamp(baseline_load × (0.90 + inner_load/500) × (0.92 + mean_wound/625), 0, 100)`.
- `overt = min(expressed_aim, current)`; `internal = current − overt`; `trace = internal × conductance`.
- Conductance: base 1.0 + min(.35, groove/250) + vitality/channel terms + social/network/repression/practice/aperture/agency terms + relational-field bonus; clamp .65–1.45.
- Route coefficients: see shared atlas §3.6; `r = trace_intensity`.
- Memory: cap 120 snapshots; recent window 5; groove decay .985; increment .035×trace; historical relation ±10 vs prior average.
- `_compact_event_context` only counts event/micro-trace types; no event identity/access/meaning.

**Probe confirmation:** baseline 80, inner 60, wound 50 → current 81.6; internal 71.6, conductance 1.062, trace 76.039; groove 100 raises conductance to 1.413 without changing current; prior groove 10 + trace 50 → 11.6.

## 03 Scientific claim and limit

The module describes a hydraulic/accounting membrane: structural pressure plus chronic wound becomes “charge,” a gated portion becomes overt expression, the remainder routes through one fixed channel, and trace changes practices/styles/wounds and future conductance.

**Limits:**

- “Conservation” is per-domain bookkeeping, not a psychological law; no global conservation; trace is not conserved.
- One channel per domain; simultaneous/contradictory channels are collapsed by `_pick_channel` (fixed priority tie-break).
- Event context is counts only; there is no event impression/appraisal/access.
- History changes conductance/effect strength and descriptive labels; it does **not** change channel selection (grooves are not read by `assign_sublimation_channels`) or relation scope/access.
- Route effects are scalar/categorical writes; no new relation/edge/rule is learned.
- Categorical conspiracy effect (`theory_of_change_style`) is committed but absent from numeric trace audit.
- Pre-route writes are live before the transactional route commit; a later failure leaves them changed.
- `derive_vitality_profile` fatigue/recovery/conductance-multiplier/horizon are readouts, not route inputs.
- `derive_insulation_profile`/buffers are metadata/cost, not inhibitory routing; buffer strength alone leaves charge/conductance/trace identical.

## 04 Differential to N02/N03/N04/N05/N08

| Target | Old coverage | Gap |
|---|---|---|
| N02 scoped expectations/care | wound/groove/aggregate labels | no relationship/scope/care/repair/access; no scoped memory |
| N03 challenge/complication/threat/repair | structural load + counts; rupture elsewhere | no actor-specific appraisal; no challenge/threat distinction; no repair in flow |
| N04 multiple interpressures | five domains one channel each; scalar wounds | no multi-stream/vector, no conflict/regulation relation, no context recruitment |
| N05 durable rewiring | route scalar/categorical writes; framework/metabolization/topology elsewhere | no CAN011 typed transition, causal parents, scope, changed relation, loss/repair |
| N08 impression/salience/NO_CHANGE | charge/trace/surface bands | no event impression, no explicit NO_CHANGE, no irrelevant/support-withdrawn controls |

**Coverage:** `MEANINGFUL_COVERAGE` for transaction/provenance/surface/analyst separation; `PARTIAL_WRONG_MEANING` for charge/conductance/history; `MISSING` for event-conditioned multi-stream and scoped durable psychology.

## 05 Retain / adapt / replace / create

**Retain:** state/derived separation; working-copy/commit for route objects; per-domain trace/delta; surface/analyst separation; history cap; failure diagnostic.

**Adapt:** charge inputs to event/access/appraisal/relationship/support; conductance to scoped conditions; memory to event/relation memory; gating to one canonical constraint index; cycle to event/interval grain; audit to include categorical/pre-route writes.

**Replace:** winner-take-all `_pick_channel`; fixed channel taxonomy/priority; fixed coefficients/decay; “conserved charge” claim; `route_unexpressed_load` duplicate; demographic wound seeding.

**Create:** CAN008 concrete impression/uptake; multi-stream situated recruitment/conflict/regulation; CAN011 typed durable transition; relationship/scope/access; intervening-time; fallible memory; explicit valid NO_CHANGE.

## 06 Court return / falsifiers

**Engineering:** source exact at file level, 82 focused historical tests; historical run. No current integration.

**Science:** `PARTIAL_WRONG_MEANING`; do not treat as established pressure psychology or conservation law.

**Authority:** no native grant; CAN008/CAN011 issuance remains with owners.

**Negative cases that falsify overclaims:**

1. Grooves 0 vs 100 leave selected channel and current charge identical; only conductance/trace changes → history is not selection/scope.
2. Buffer strength 0 vs 100 leaves charge/conductance/trace identical → buffer strength is not regulation in this route.
3. Event label/ID-only change with same type leaves charge/trace/memory identical → event semantics are not read.
4. Forced post-route failure with defaults changes live `affect_channel`/`baseline_load` → transaction is partial.
5. Conspiracy categorical effect appears in state but not numeric trace → audit is incomplete.

**Owner/action:** historical V3 implementation owner and competent science owners. **Do not repair in place**; this is a research finding.
