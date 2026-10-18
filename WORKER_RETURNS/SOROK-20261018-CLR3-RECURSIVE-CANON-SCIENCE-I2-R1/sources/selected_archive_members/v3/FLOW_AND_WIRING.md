# How the v3 pieces inter-flow (wiring)

Single document for: **where state comes from**, **how each year runs**, **where the LLM plugs in**, and **how summary → propose → score → apply → render → persona** connect. All file/function names are the ones actually used in the runner and engine.

---

## 1. Seed: identity → backbone state → derived

| Step | Where | What |
|------|--------|------|
| Identity | Caller (e.g. v2 runner) | `identity_dict` = identity_skeleton_to_dict(identity) or similar. May contain parent_expectation_baseline, transmission_regime, environment, country_code, etc. |
| Backbone | `v3/io/identity_to_backbone.py` → **backbone_state_from_identity(identity_dict, year, age)** | Builds initial `BackboneState`: capacity, domains, field, reproduction_constraints, wound_vector, frameworks, cracks, etc. If identity has parent_expectation_baseline / transmission_regime / environment, calls **derive_child_expectation_baseline(...)** and sets **state.expectation_baseline**. Injects field from **field_injection** (country, year, age, gender) when available. |
| Derived | `v3/core/derived.py` → **compute_all_derived(state)** | Returns **DerivedIndices** (hostage_index, agency_capacity_AC, structural_lucidity_SL, peak_regime, etc.) from current state. No mutation. |

So: **identity → backbone_state_from_identity → state**; then **derived = compute_all_derived(state)**. State and derived are what the yearly loop and Pass 1 use.

---

## 2. Runner: the yearly loop (v2/run_full_simulation_with_llm_log.py)

The v3 path does:

```text
state = backbone_state_from_identity(identity_dict, birth_year, 0)
derived = compute_all_derived(state)
config = load_v3config()
step_order = load_step_order()

for t in range(num_years):
    # 2a. Mechanical year step (order from v3_yearly_step_order.yaml)
    run_one_year(state, derived, config, step_order)

    # 2b. At “band” ages only: 2-pass LLM (propose → select → apply → render)
    if state.age in llm_ages:
        # … Pass 1 summary, LLM, select, apply deltas + magnets, build render packet, Pass 2 render
        …
    else:
        render_year(state, derived, config)   # minimal output, no LLM

# After loop: persona sheet from final state
sheet = v3_build_persona_sheet(state, derived, identity_override=identity_dict, include_backbone=True)
```

So each iteration: **first** run_one_year (advances year/age and runs all steps), **then** optionally the 2-pass LLM at band ages. Persona sheet is built once after the loop from the final state.

---

## 3. run_one_year: what runs and in what order

**File:** `v3/engine/yearly_step.py` → **run_one_year(state, derived, v3config, step_order)**

**Order** comes from **v3/v3_yearly_step_order.yaml** → `steps` (via config_loader get_step_list). Core sequence:

1. field_update  
2. event_sampling  
3. reproduction_constraints_update  
4. capacity_update  
5. buffers_update  
6. frameworks_update  
7. domains_update  
8. cracks_and_alienation_update  
9. **plasticity_and_metabolization_update** (metabolization_effects.update_metabolization_and_plasticity_step)  
10. **striving_update** (striving_objects.update_striving_step: spawn proxy strivings from proxy_striving_map by age/expectation_baseline)  
11. practice_and_infrastructure_update  
12. topology_and_boundary_update  
13. attention_and_capture_update  
14. strategy_and_signal_effects  
15. style_trait_drift  
16. **render_layer** (phenomenology.render_year **without** render_packet/llm_callback → minimal rendered_output)  
17. **active_magnets_update** (active_magnets.update_active_magnets_step: decay intensity, floor, cap)

Then: **state.year += 1**, **state.age += 1**.

So: **expectation_baseline** (from seed) and **striving_update** (yearly) and **active_magnets_update** (yearly decay) and **plasticity_and_metabolization_update** (yearly plasticity/metabolization) are all inside this one year step. The LLM is **not** called here; it’s called by the runner **after** run_one_year when age is in llm_ages.

---

## 4. At band ages: 2-pass LLM flow (same file, inside “if state.age in llm_ages”)

### 4.1 Pass 1: state → summary → prompt → LLM → packet → select → apply

| Step | Where | What |
|------|--------|------|
| Summary | `v3/engine/llm_contract.py` → **state_summary_from_backbone(state, derived, identity_override)** | Builds the dict the LLM sees: year, age, identity, field (affordances, hostage_index, salient_strata), capacity (vitality, aperture, …), wound, frameworks_active, active_cracks, calibration_regime, **boundary_map**, domain_axes, child_model, **expectation_baseline**, **striving_objects**, **active_magnets**, **rupture_plasticity**, **registers**, **metabolic_style**, etc. |
| Prompt | `v3/engine/prompts.py` → **build_pass1_prompt(state_summary, suggested_event_targets=...)** + **pass1_response_instruction()** | User message = state summary as JSON; optional suggested_event_targets from get_suggested_event_targets(summary). System + instructions tell the model to output a CandidatePacket (event_candidates, magnet_candidates, branch_hypotheses). |
| LLM | Runner’s _get_llm_response("pass1", …) | Returns raw string (expected JSON). |
| Parse | `v3/engine/llm_contract.py` → **parse_candidate_packet_with_fallback(raw1)** | Parses JSON; if empty/malformed, fallback adds one minimal event. Output: packet with event_candidates, magnet_candidates. |
| Select | `v3/engine/scoring.py` → **select_candidates(packet, state_summary, rng)** | Scores events (age_fit, channel_available, salience_fit, hostage_fit, capacity_fit, wound_fit, boundary_fit, rupture_assumption_fit, striving_bonus) and magnets; returns **(selected_events, selected_magnets)** (≤2 major, ≤2 minor, ≤1 surprise, ≤2 magnets). |
| Deltas | `v3/engine/effects/delta_templates.py` → **delta_from_event(ev, config)** per event, **delta_from_magnet(mg, config)** per magnet | Each selected event/magnet → one delta dict. |
| Merge | `v3/engine/effects/delta_templates.py` → **merge_deltas(deltas_list)** | Single merged delta dict. |
| Apply deltas + rupture + gift/disruption | `v3/engine/effects/delta_templates.py` → **apply_deltas_to_state(state, merged_deltas, config, selected_events=selected_events)** | Applies capacity, domains, alienation, coherence, practice; for each **epistemic_rupture** calls **create_rupture_shard_from_event**; then **apply_gift_disruption_shards_from_events(state, selected_events)** (GiftShard/DisruptionShard from expectation_type + striving_object_id; malheur_risk when violation + high identity_load). |
| Apply magnets | `v3/engine/active_magnets.py` → **apply_selected_magnets_to_state(state, selected_magnets, config)** | Converts selected magnet_candidates to **Magnet** and appends to **state.active_magnets** (respects max, skips duplicate id). |
| Re-derive | **compute_all_derived(state)** | So derived is up to date for render and persona. |

So: **state + derived** → **state_summary_from_backbone** → **state_summary** → **build_pass1_prompt** → LLM → **parse_candidate_packet_with_fallback** → **select_candidates** → **merge_deltas** → **apply_deltas_to_state(..., selected_events)** (deltas + rupture) → **apply_selected_magnets_to_state** → **compute_all_derived(state)**.

### 4.2 Pass 2: render packet → prompt → LLM → parse → state.rendered_output

| Step | Where | What |
|------|--------|------|
| Render packet | `v3/engine/llm_contract.py` → **build_render_packet(year, age, selected_events, selected_magnets, state_deltas_applied, constraints)** | Dict with events, magnets, deltas summary, constraints (e.g. no_resolution). |
| Prompt | `v3/engine/prompts.py` → **build_pass2_prompt(render_packet)** + **pass2_response_instruction()** | Asks for RenderOutput (narrative_snapshot, dialogue_snippets, consistency_check, particularity, etc.). |
| LLM | Runner’s _get_llm_response via **llm_callback** passed to render_year | Returns raw string. |
| Parse / validate | `v3/render/phenomenology.py` → **render_year(state, derived, config, render_packet=..., llm_callback=...)** | **parse_render_output(raw)**, **validate_render_output**; optional retry with **pass2_corrective_instruction** on failure. |
| Write output | Same **render_year** | Sets **state.rendered_output** (narrative_snapshot, dialogue_snippets, consistency_check, particularity, …). Does **not** mutate other backbone state. |

So: **selected_events + selected_magnets + state_deltas_applied** → **build_render_packet** → **build_pass2_prompt** → LLM → **render_year(..., render_packet, llm_callback)** → **state.rendered_output**.

---

## 5. Persona sheet (after the loop)

| Step | Where | What |
|------|--------|------|
| Sheet | `v3/io/persona_sheet.py` → **build_persona_sheet(state, derived, identity_override=..., include_backbone=...)** | Builds the v2-compatible persona dict: identity, current_state (needs, strategies, indices), bands, voice_profile, backstory, life_snapshot, **expectation_baseline**, **active_strivings**, **rupture_status**, **recent_gifts**, **recent_disruptions**; optionally backbone and rendered_output. Runner then may overwrite **backstory** with band narratives. |

So: **state** and **derived** (after all years and LLM applications) → **build_persona_sheet** → persona dict (and optionally dumped to persona_sheet.json).

---

## 6. Data flow diagram (concise)

```text
identity_dict
    → backbone_state_from_identity()     → state (optional expectation_baseline from derive_child)
    → compute_all_derived(state)         → derived

for each year:
    run_one_year(state, derived, config, step_order)
        → field_update, event_sampling, … , plasticity_and_metabolization_update,
          striving_update, … , render_layer (minimal), active_magnets_update
        → state.year++, state.age++

    if state.age in llm_ages:
        state_summary = state_summary_from_backbone(state, derived, identity_dict)
        packet = parse_candidate_packet_with_fallback(LLM(build_pass1_prompt(state_summary)))
        selected_events, selected_magnets = select_candidates(packet, state_summary)
        apply_deltas_to_state(state, merge_deltas(...), config, selected_events=selected_events)
        apply_selected_magnets_to_state(state, selected_magnets, config)
        derived = compute_all_derived(state)
        render_packet = build_render_packet(..., selected_events, selected_magnets, state_deltas_applied, ...)
        render_year(state, derived, config, render_packet=render_packet, llm_callback=...)
            → state.rendered_output

sheet = build_persona_sheet(state, derived, identity_override=identity_dict, include_backbone=True)
```

---

## 7. Where each “layer” gets into the flow

| Layer | Enters state / summary / persona |
|-------|----------------------------------|
| **expectation_baseline** | Set at seed in **backbone_state_from_identity** (derive_child when identity has parent/regime/env). Filled by **striving_update** (setdefault per axis). In Pass 1 summary via **state_summary_from_backbone**. In persona via **build_persona_sheet** (expectation_baseline, active_strivings, rupture_status). |
| **striving_objects** | Appended yearly by **striving_update** (spawn_striving_objects_for_age from proxy_striving_map by age/expectation_baseline). In Pass 1 summary. In persona as **active_strivings**. |
| **active_magnets** | Appended when **apply_selected_magnets_to_state** runs (after Pass 1 select). Decayed/trimmed yearly by **active_magnets_update** inside run_one_year. In Pass 1 summary. In persona via micrograph (caregivers/peers/institutions). |
| **rupture_shards / metabolization_processes / plasticity_window** | Created in **apply_deltas_to_state** when **selected_events** contains an **epistemic_rupture** (create_rupture_shard_from_event). Updated yearly by **plasticity_and_metabolization_update** inside run_one_year. In Pass 1 summary as **rupture_plasticity**. In persona as **rupture_status**. |
| **boundary_map** | In state (from load/seed). In Pass 1 summary from **state_summary_from_backbone**. Used in **score_event_candidate** for **boundary_fit** (event.implicated.positions vs discouraged/incentivized). |

This is how the pieces are wired end-to-end.
