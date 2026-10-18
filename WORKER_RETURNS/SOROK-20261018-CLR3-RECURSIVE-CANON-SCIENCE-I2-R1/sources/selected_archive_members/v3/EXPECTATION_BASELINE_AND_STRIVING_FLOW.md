# How expectation_baseline and proxy striving slot in (and current gap)

## Intended design (spec / starter_engine)

1. **Expectation baseline**  
   Per NeedAxis (attachment, safety, belonging, status, competence, autonomy, meaning, justice, beauty_play, eros_intimacy), the persona has a baseline: **entitled** | **hopeful** | **forbidden** | **hopeless**.  
   - **Entitled / hopeful:** “This need can be met (or might be).” Direct striving is plausible.  
   - **Forbidden / hopeless:** “This need is not allowed or can’t be met.” Striving often appears **via proxies** (e.g. “perfect obedience” as covert autonomy, “romance fantasy” as safe eros).

2. **Where baseline is set**  
   - **Intended:** `derive_child_expectation_baseline(parent_baseline, regime, environment)` at birth/start from need_axis_rules.yaml (parent warmth, anxiety, shame, coercion, etc.).  
   - **Current:** **Implemented.** `backbone_state_from_identity` in identity_to_backbone.py calls **derive_child_expectation_baseline(...)** when identity has parent_expectation_baseline / transmission_regime / environment and sets state.expectation_baseline. Otherwise baseline is set by seed/load or each year in striving_update (setdefault per axis to "hopeful").

3. **Proxy striving (proxy_striving_map.yaml)**  
   When baseline is **forbidden** or **hopeless** for an axis, the yearly step spawns up to `max_new` **StrivingObjects** from the map (by age bracket): e.g. “Caregiver-pleasing as attachment proxy”, “Perfect obedience as covert autonomy”.  
   - **Entitled / hopeful:** Map has empty `entitled: {}`, `hopeful: {}`; code does not spawn proxies for those baselines. So “entitled/hopeful = direct striving; no proxy” is correct.

4. **How it’s supposed to influence the persona**  
   - Striving objects are **investment targets**: “what this person is going after indirectly.”  
   - Events can **attach** to a `striving_object_id` (GiftShard / DisruptionShard, prediction error).  
   - Pass 1 (candidates) and scoring could **favor or reference** events that align with or touch these strivings.  
   - Persona sheet / narrative could **surface** them (e.g. “invested in X proxy”) so the emerging persona clearly reflects them.

## Current wiring (what actually happens)

| Piece | Status |
|-------|--------|
| `state.expectation_baseline` | Exists; set from seed or defaulted to "hopeful" each year. |
| `state.striving_objects` | Exists; appended to by `striving_update` when baseline is forbidden/hopeless. |
| `derive_child_expectation_baseline()` | **Not called** in identity_to_backbone or run path → no forbidden/hopeless from parents. |
| Pass 1 state summary | **Does not** include expectation_baseline or striving_objects → LLM doesn’t see them. |
| Scoring | **Does not** use baseline or striving_objects. |
| Persona sheet | **Does not** surface striving_objects or baseline (only practice_stack–derived “achievement_striving” etc.). |

So: **spawning behavior is unchanged** and **entitled/hopeful stay empty in the map** by design, but right now the whole chain **barely influences the emerging persona** because:

- Baseline is almost always “hopeful” unless you seed forbidden/hopeless.
- Even when proxy striving objects are spawned (e.g. from seed), nothing downstream (Pass 1, scoring, persona_sheet) reads them.

## What would make it actually influence the persona

1. **Set baseline at start**  
   Call `derive_child_expectation_baseline(...)` when building initial state from parents (or from regime/environment) and assign `state.expectation_baseline` so some axes can be forbidden/hopeless.

2. **Expose to Pass 1**  
   Add to `state_summary_from_backbone`: e.g. `expectation_baseline` (per axis) and a short list of `striving_objects` (id, label, need_axis) so the LLM can propose events that align with or puncture those strivings.

3. **Use in scoring (optional)**  
   E.g. boost events whose `implicated` / tags match an active striving’s need_axis or label; or allow `striving_object_id` on events and prefer events that attach to an existing striving.

4. **Surface in persona_sheet**  
   E.g. in bands/micrograph or a small “active strivings” block so the conversation engine and any narrative see “this person is invested in X, Y (proxy)” and the emerging persona is visibly shaped by them.

Until (1)–(4) (or a subset) are wired, expectation_baseline and proxy striving **do not meaningfully slot in** to the emerging persona; they only exist in state and in saved JSON.

---

## Why is so much state “stored but not in the flow”?

Spec and backlog prioritized **state schema + codec + step logic** (so the engine can persist and step everything). **Downstream wiring** — what gets into the Pass 1 summary, scoring, and persona_sheet surface — was only fully done for a subset of fields. The rest exist in state (and in JSON dump) but were never hooked into:

- **Pass 1 (state_summary_from_backbone)** → what the LLM sees when proposing events/magnets  
- **Scoring** → what the selector uses (only reads from Pass 1 summary)  
- **Persona sheet** → what’s explicitly surfaced for conversation/narrative (not just raw backbone dump)

So we end up with “implemented in state, not in the flow.”

---

## Audit: state in vs out of the flow

| State field | In Pass 1 summary? | In scoring? | In persona_sheet (explicit)? |
|-------------|--------------------|-------------|------------------------------|
| year, age, identity | ✓ | ✓ (age) | ✓ |
| field (hostage_index, affordances) | ✓ (as field) | ✓ | indirect |
| capacity | ✓ (proxied as vitality, etc.) | ✓ | ✓ (needs, strategies) |
| wound_vector | ✓ (as wound) | ✓ | ✓ (moral_loops) |
| frameworks | ✓ (frameworks_active) | ✓ | via backbone |
| cracks | ✓ (active_cracks) | — | ✓ (micrograph norm_conflicts) |
| calibration_regime | ✓ | — | — |
| boundary_map | ✓ | — | — |
| domains | ✓ (domain_axes, latent/expressed_aim) | — | — |
| child_model | ✓ | ✓ (rupture fit) | — |
| strata_salience | ✓ (salient_strata) | — | — |
| **expectation_baseline** | ✓ | — | ✓ |
| **striving_objects** | ✓ | ✓ (striving_bonus, 70/30) | ✓ (active_strivings) |
| active_magnets | ✓ | — | ✓ (micrograph) |
| rupture_shards / metabolization_processes / plasticity_window | ✓ (as rupture_plasticity) | — | ✓ (rupture_status) |
| metabolic_style | ✓ | — | — |
| gift_shards / disruption_shards | — | — | ✓ (recent_gifts, recent_disruptions) |
| registers | ✓ | — | — |
| practice_stack | no (only via capacity proxy) | no | ✓ (strategies, job_type) |
| peak_routing | no (only coherence, rage_metabolization in proxy) | no | ✓ (voice_scripts) |
| style_traits | no | no | ✓ (strategies) |
| intensity_and_capture | no (only intensity → aperture) | no | ✓ (strategies) |
| reproduction_constraints | no (only hostage_index in field) | no | ✓ (needs safety) |
| collective_infrastructure | no | no | no |
| buffers | no | no | no |
| alienation_vector | no (only scalar elsewhere) | no | no |
| strata_stack | no (only strata_salience → salient_strata) | no | no |
| psychological_capacity | no (proxied from capacity + derived) | no | no |

So yes: there are **many** other parts of state that are not in the flow the same way. Expectation_baseline and striving_objects are two of them; rupture/metabolization/plasticity/gift/disruption/registers/active_magnets (for Pass 1) are others. Fixing “why” means either wiring these into Pass 1 + scoring + persona surface where they should shape the persona, or documenting that they are intentionally “state only” for now.
