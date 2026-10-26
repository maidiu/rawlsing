# X02 M24 — stability-threshold inertia

**Historical code grade:** `HISTORICAL_SOURCE_AUDITED`; `HISTORICAL_RUN` only indirectly; no dedicated behavioral test.
**Current integration:** `UNTRACED` outside historical V3.
**Coverage:** `PARTIAL_WRONG_MEANING` for N02/N05/N08.
**Authority:** none; legacy thresholds/coefficients are policy.

## Direct source map

- State fields: `v3/core/state.py:559-561` — `stability_threshold_inertia` 0–100, `stability_delta_applied_this_year`.
- Event spike: `v3/engine/effects/delta_templates.py:273-279,333-354` — `stability_delta` capped (default 10); trauma kinds puncture/humiliation/violence/epistemic_rupture; minor +3, major +5, shock +8; reactivation bump 0.5× min(cap, |stab|) if event matches a process trigger; one bump per event.
- Derived: `v3/core/derived.py:217-236` — `stability_threshold = .25·gap_pressure + .25·hostage + .25·mis_aim − .15·insulation − .05·(100−health) − .05·coherence + inertia`; clamp 0–100.
- Drain: `v3/systems/stability_inertia.py:17-83` — integration 5/provisionally narrated 3 (cap 12); IRR drop 1.5 (cap 3) if drop ≥5 and support_quality ≥55; holding 0.6×(.35 insulation+.35 social+.30 coherence) when no delta and no high IRR; mid IRR halves; sealed/chronic leak .15 if support_quality ≥60. Clears `stability_delta_applied_this_year`.
- Consumer: `compute_stability_threshold` → `autonomy_safety_micro_drift` (drift bias), `compute_health_level`; not pressure-flow charge/route.
- Tests: no dedicated behavioral test found; only step order/JSON roundtrip.

## Actual behavior

Inertia is a persistent 0–100 scalar raised by selected trauma events and drained by metabolization status, IRR decline, holding/support/coherence. It raises the derived stability threshold, which feeds autonomy micro-drift and health level. It does not directly gate pressure-flow charge, channel selection or route. The drain is annual/process-based, not event-time; support quality is a simple `warmth+accuracy−coercion` from narration support; no relationship scope or actual repair action.

## Differential

N02/N05/N08 require history-dependent persistence/hysteresis with **relational consolidation, intense/novel counterexamples, buffering and delayed change**, not generic age/year thresholds. Old code provides:
- a real persistent inertia and event spike/drain;
- but no event-time/relationship scope;
- no distinction between ordinary consolidation and intense disruption beyond event kind and process status;
- no actual support/repair action; support is an aggregate narration quality;
- no direct pressure-flow or later semantic consumer;
- fixed constants and process thresholds.

**Coverage:** `PARTIAL_WRONG_MEANING` — a candidate hysteresis mechanism exists; required relational/event semantics are missing.

## Dispositions

- **Retain:** persistent inertia as a candidate; event spike/drain; metabolization/IRR/support as conditioning inputs; separate `stability_delta_applied_this_year`.
- **Adapt:** event-time/scope; actual support/repair; distinguish transient activation, persistent target change and relation change; link to CAN011; remove universal constants/age defaults; define delayed change/relapse.
- **Replace:** year-bound drain as psychological law; fixed support-quality formula; vague “holding” as if it were a relationship process.
- **Create:** event-scoped consolidation/repair and durable transition rules under CAN011; later consumer. No new coefficient proposed.

## Falsifiers / limits

- If inertia is claimed to change pressure-flow routing, source reads it only via derived stability/autonomy/health; not charge/channel.
- If support is claimed to be a caregiver repair, source is a narration-support aggregate; no caregiver action.
- If a single trauma label is claimed to create a durable trait, source adds a bounded scalar spike and later drain; no trait/relation rewrite.

**Owner:** V3 implementation/M24; CAN011/ADP016 science owners.
