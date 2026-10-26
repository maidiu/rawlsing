# X02 M03 — psychological/regulatory capacity vector

**Historical code grade:** `HISTORICAL_SOURCE_AUDITED`; `HISTORICAL_RUN` via pressure-flow tests.
**Current integration:** `UNTRACED` outside historical V3.
**Coverage:** `PARTIAL_WRONG_MEANING` for N01/N04.
**Authority:** none; legacy coefficients are not science.

## Direct source map

- `PsychCapacity` dataclass: `v3/core/state.py:40-54` — `vitality, aperture, reality_anchor, binding, coherence, agency, transmutation`, each 0–100 default 50.
- `compute_all_derived`: `v3/core/derived.py:322-359` — computes `agency_capacity_AC`, `insulation_score`, `structural_lucidity_SL`, `mis_aim_risk`, `peak_regime`, `metabolic_style`, `health_level`; writes `state.registers` and `state.metabolic_style`.
- Pressure-flow consumers: `_channel_conductance` (`flow.py:376-403`) reads vitality/agency/aperture; `apply_expression_gating` (`gating.py:159-188`) uses vitality and `inner_load`; `derive_vitality_profile` (`vitality.py:90-181`) computes age/fatigue/horizon/recovery/conductance readouts.
- Other consumers: `compute_agency_capacity_AC` (`derived.py:61-75`) uses material capacity, not psychological capacity; `state_summary_from_backbone`/Pass 1 and persona surfaces use some fields.
- Tests: `test_v5_vitality_fatigue.py` (3), `test_v5_pressure_flow.py` vitality/gating cases, `test_phase3_activation_gate.py` energy gating, `test_step_logic.py` derived ranges. No direct test of `reality_anchor`, `binding`, `coherence`, `transmutation` causal effect in pressure flow.

## Actual behavior

The vector is a set of independent scalar capacities. In pressure flow only `vitality`, `agency`, and `aperture` are read (conductance); `vitality` and `inner_load` gate expression. `derive_vitality_profile` adds age penalty `max(0,(age−30)×.25)`, fatigue `100−vitality + age_penalty + .04·current + .03·internal − .08·insulation`, fatigue bands, recovery cost, future horizon, conductance multiplier. Those profile outputs are **not fed back** into `_channel_conductance`; only raw vitality is. `conductance_multiplier` is a display/memory value.

`compute_agency_capacity_AC` is material: weighted capacity minus .5×hostage; it is not the psych `agency` field. This is a naming/semantic split that can mislead.

## Differential

N01/N04 need a distinction among **fatigue/physiological arousal, assisted self-regulation, practical ability and social power**. The old vector collapses these into seven 0–100 scalars; there is no support/activity/relationship scope, no state-vs-capacity distinction, and no condition-specific accessibility. `reality_anchor` and `transmutation` are largely narrative labels; they do not enter the pressure-flow route. `aperture` enters conductance (aesthetic bonus) and public gate; `binding` enters private gate; `coherence` enters peak/metabolic/stability thresholds; `agency` enters conductance and AC elsewhere.

**Coverage:** `PARTIAL_WRONG_MEANING` — real state and some causal use, but not the differentiated regulation/ability/power ontology required.

## Dispositions

- **Retain:** typed psychological capacity as a compact projection; stored/derived split; the idea of fatigue/future horizon as a readout candidate.
- **Adapt:** separate fatigue/arousal, practical ability, assisted regulation, social power and access; make each causal only under an issued rule; remove age-as-penalty defaults.
- **Replace:** raw scalar `reality_anchor`/`transmutation` as if they were established psychology; use of `agency` as both material AC and psych scalar.
- **Create:** support/activity/relationship-conditioned regulation operators; owner-issued thresholds and scope. No new numeric law is proposed.

## Falsifiers / limits

- If a change in `aperture` or `binding` is claimed to regulate pressure-flow routing, the source only uses aperture for aesthetic conductance and private gate; no general inhibition.
- If fatigue is claimed to reduce charge, the source explicitly does not: low vitality does not reduce current charge; it changes conductance and readouts.
- If `conductance_multiplier` is claimed to affect route, it is not read by `_channel_conductance`; it is a profile readout.

**Owner:** CAN011/CAN009/current V3 implementation owner; science issuance separate.
