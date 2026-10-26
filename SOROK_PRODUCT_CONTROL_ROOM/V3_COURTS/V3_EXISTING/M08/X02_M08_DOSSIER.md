# X02 M08 — wound/sensitivity state

**Historical code grade:** `HISTORICAL_SOURCE_AUDITED`; `HISTORICAL_RUN` via channel/gating/pressure-flow tests.
**Current integration:** `UNTRACED` outside historical V3.
**Coverage:** `PARTIAL_WRONG_MEANING` for N02/N03/N05/N08.
**Authority:** none; demographic seeding is explicitly non-terminal legacy policy.

## Direct source map

- `WoundVector`: `v3/core/state.py:130-147` — seven scalar sensitivities `shame, fear, anger, abandonment, control, recognition, loss`, default 50; default coping channels `["withdraw","intellectualize"]`.
- `seed_wound_vector_from_identity`: `v3/psyche/channels.py:36-95` — class/current class lookup, minority status, religiosity, age; numeric deltas; clamps 0–100.
- `_seed_wound_scores`: `channels.py:103-150` — maps wound excess over 50 into channel scores with fixed coefficients; spiritual practice also contributes.
- `_wound_mean`: `v3/psyche/flow.py:226-230` — mean of seven wounds.
- `_derive_current_charge`: `flow.py:268-284` — wound mean factor 0.92 + mean/625.
- `compute_registers_from_state`: `derived.py:272-318` — inner_load = 50 + sum(max(0,w−50))/4.
- `_apply_single_domain_route` somatic branch: `flow.py:533-535` — anger +0.05×trace, health −0.02×trace.
- `update_wound_vector_from_rupture` lives in `v3/engine/effects/metabolization_effects.py` (outside pressure flow; not executed here).

Tests: `test_phase3_activation_gate.py` identity seeding/channel differentiation; `test_v5_pressure_flow.py` wound factor/charge; `test_v5_sublimation_channels.py` anger/route bounds. No test for repair, scope, relationship specificity, or trauma-category validity.

## Actual behavior

Wounds are seven 0–100 scalars seeded from **demographic/structural categories** (class, minority, religiosity, age) and updated by rupture elsewhere. Pressure flow uses the mean wound for charge and maps wound excess to fixed channel scores; somatic routing can increase anger. `inner_load` rises with excess wounds. Wounds are not scoped by person/relationship/context, have no support/repair field, no event history, no contradiction representation, and no accessibility/forgetting.

The identity seeding is direct: e.g. working class → fear +10, abandonment +9, loss +8, shame +6; minoritized → shame +12, fear +10, etc.; age <18 → abandonment +8, fear +5, loss +4. These are historical heuristics, not empirical laws, and the source itself does not cite a rule issuer.

## Differential

N02/N03/N05/N08 require sensitivities to originate through **warranted situations and responses**, be scoped, repairable, capable of contradiction/loss, and not automatically assigned by demographic category. Old code has persistent scalar susceptibility but:
- no relationship/context scope;
- no repair or support record;
- no distinction between ordinary consolidation and intense disruption in this family (rupture/metabolization elsewhere);
- no explicit NO_CHANGE/irrelevance;
- demographic seeding conflates structural position with psychological sensitivity.

**Coverage:** `PARTIAL_WRONG_MEANING` — persistent susceptibility exists; the required origin/scope/repair semantics do not.

## Dispositions

- **Retain:** persistent sensitivity as a candidate state family; scalar dimensions only if owner-issued; inner-load as a readout candidate.
- **Adapt:** originate from actual event/relationship/support history; add scope, repair, mitigation, contradiction; allow multiple sensitivities; independent owner targets.
- **Replace:** demographic/age seeding as psychological truth; fixed 7 dimensions as universal ontology; fixed channel mapping coefficients.
- **Create:** warranted sensitivity-formation/repair rules (CAN011/ADP), relationship-specific sensitivity, fallible memory/access; no new coefficient proposed.

## Falsifiers / limits

- If a class/minority label is claimed to establish a wound, source is a hard-coded lookup, not evidence; Neo-V3 forbids this as default psychological truth.
- If a single wound is claimed to select one channel, source sums multiple wound contributions into scores and picks one; no one-to-one mapping.
- If repair is claimed, pressure flow has no repair operator; rupture/metabolization is separate and not executed here.

**Owner:** original science/CAN011/ADP015/016; historical V3 implementation owner.
