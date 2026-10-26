# X02 M05 — A/S/V/Aim domains and latent/expressed Aim

**Historical code grade:** `HISTORICAL_SOURCE_AUDITED`; `HISTORICAL_RUN` via pressure-flow/baseline/gating tests.
**Current integration:** `UNTRACED` outside historical V3.
**Coverage:** `PARTIAL_WRONG_MEANING` for N03/N04.
**Authority:** none; domain taxonomy is historical policy.

## Direct source map

- `DomainState`: `v3/core/state.py:72-91` — `A, S, V, Aim, latent_aim, expressed_aim, baseline_load, expression_rate, activation_threshold, affect_channel, buffer_type`, puncture counters.
- `update_domains`: `v3/systems/domains.py:50-56` — applies event `domain_deltas` to A/S/V/Aim with per-component caps (default 10), clamps.
- `compute_baseline_load`: `v3/psyche/gating.py:122-149` — structural strata → domain load using A/V labels and fixed domain weights; writes `baseline_load`; preserves expression_rate/threshold.
- `apply_expression_gating`: `gating.py:152-188` — computes `expressed_aim` from load × rate, hostage/energy brakes, activation threshold; writes `expression_rate` (no reset).
- `assign_sublimation_channels`: `channels.py:194-201` — one channel from domain A/S/V/buffer_type + global wounds/practice.
- `run_pressure_flow_cycle`: `flow.py:753-843` — uses `baseline_load`, `expressed_aim`, `affect_channel`; route does **not** mutate domain A/S/V/Aim.

Tests: `test_v5_baseline_load.py` (8), `test_phase3_activation_gate.py` (5), `test_v5_pressure_flow.py` 23 (domain/charge), `test_step_logic.py` domain deltas. No test of simultaneous contradictory Aim orientations; no direct event-semantic baseline test.

## Actual behavior

Each of five domains (`empire_occupation`, `nation_state`, `sect_class_ethnicity`, `family_household`, `body_self`) has one A/S/V/Aim tuple and one `affect_channel`. `baseline_load` is a structural projection from 9-stratum pressure, weighted by domain, with A/V-label weights and buffer penalties. `expressed_aim` is a gated scalar; `latent_aim` is a stored field but pressure flow uses only `expressed_aim` and `baseline_load`; `Aim` is not used in pressure flow.

`update_domains` can change A/S/V/Aim from event `domain_deltas` with caps; pressure-flow route does **not** change A/S/V/Aim. `assign_sublimation_channels` reads A/S/V and buffer_type but not S? It uses A/S/V in `_seed_domain_scores`; yes.

## Differential

N03/N04 need challenge/complication/threat/repair and simultaneous contradictory recruitment. Old domains are analytic compartments, not causal needs/objects/relations. Five domains are a fixed taxonomy; A/S/V are scalar axes; one channel per domain; no multi-stream/contradiction. `latent_aim` is stored but not used by pressure flow; `Aim` is not used. Structural position enters baseline load, but there is no exact event/access/appraisal; event deltas are additive and capped.

**Coverage:** `PARTIAL_WRONG_MEANING` — real structural projection and gating, but not the required multi-stream/relational semantics.

## Dispositions

- **Retain:** domain A/S/V/Aim as **optional projections**, not universal compartments; stored/derived separation; expression-rate/threshold idea.
- **Adapt:** re-key baseline inputs to exact current V555/V556/stratum refs; make latent/expressed Aim access-dependent; separate structural position from event impression; use a canonical constraint index.
- **Replace:** one-channel-per-domain as psychological claim; fixed five-domain compartment ontology; fixed pressure weights; expression-rate ratchet.
- **Create:** multi-stream recruited orientations and relation-scoped access; challenge/complication/threat/repair operators (CAN008 concrete).

## Falsifiers / limits

- If `Affect_channel` is claimed to represent a person’s full emotional orientation, source shows one fixed string chosen by max score with a priority tie-break; no secondary channels.
- If `latent_aim` is claimed to drive pressure flow, it is not read by `_domain_charge_ledger`/`_apply_single_domain_route`.
- If event semantics are claimed to shape `baseline_load`, source only uses strata/domain A/V; event context is counts.
- If `expressed_aim` is claimed to be stable, `expression_rate` can ratchet under constant high hostage.

**Owner:** V3 implementation owner; CAN008/PFF science owner.
