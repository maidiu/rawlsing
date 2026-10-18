# How expectation_baseline, striving_objects, active_magnets, and rupture context are determined

Summary of **where** each is set/updated and **what drives their variability** in the current codebase.

---

## 1. Expectation baseline (`state.expectation_baseline`)

**What it is:** `dict[NeedAxis, str]` → each axis is one of `entitled | hopeful | forbidden | hopeless`.

**Where it’s set/updated:**

| When | Where | What happens |
|------|--------|--------------|
| **Seed** | `identity_to_backbone.py` | If identity has `parent_expectation_baseline`, `transmission_regime`, or `environment`, calls `derive_child_expectation_baseline(...)` and assigns to `state.expectation_baseline`. |
| **Yearly** | `striving_objects.update_striving_step` | For each `NeedAxis`, `state.expectation_baseline.setdefault(ax, "hopeful")`. So any axis not yet set becomes `"hopeful"`. |

**What determines variability:**

- **At seed:**  
  - **Parent baseline** (per-axis category) → mapped to an internal score via `need_axis_rules.yaml` `parent_category_to_score` (entitled→+1, hopeful→0, forbidden→-1, hopeless→-2).  
  - **Transmission regime + environment** (warmth, coercion, anxiety, shame, modeling_consistency, openness, external_threat, economic_precarity, institutional_reliability, status_competition, collective_solidarity, etc.) → **global_modifiers** and **axis_rules** in `need_axis_rules.yaml` apply deltas to that score (e.g. warmth_gte 70 → +1 on all axes; anxiety_gte 80 → -1 on attachment/safety).  
  - Final score per axis is clamped to [-2..+2] and mapped back to category via `SCORE_TO_BASELINE` in `expectation_baseline.py`.  
- **If identity has no parent/regime/env:** `expectation_baseline` stays `{}` until the yearly step, which then fills every axis with `"hopeful"`.  
- **After seed:** No other code rewrites baseline; only setdefaults in the striving step. So **variability is entirely from (1) identity inputs at seed and (2) the rules YAML.**

---

## 2. Striving objects (`state.striving_objects`)

**What they are:** List of `StrivingObject` (id, label, need_axis, investment, identity_load, feasibility_belief, etc.).

**Where they’re set/updated:**

| When | Where | What happens |
|------|--------|--------------|
| **Yearly** | `striving_objects.update_striving_step` (called from yearly step) | Calls `spawn_striving_objects_for_age(state.age, state.expectation_baseline, existing_ids, state.year, max_new=config)` and **appends** new objects to `state.striving_objects`. No retirement or decay yet. |

**What determines variability:**

- **Age:** `spawn_striving_objects_for_age` uses `PROXY_STRIVING_AGE_BRACKETS = (3, 7, 11, 14, 17, 24, 35)` and picks the **nearest bracket** to current age.  
- **Expectation baseline:** New strivings are spawned **only for axes whose baseline is `forbidden` or `hopeless`**. For `entitled` or `hopeful`, the map returns no proxy strivings (direct striving not modeled).  
- **proxy_striving_map.yaml:** Structure is `proxies[need_axis][baseline][age_bracket]` → list of entries (id, label, default_investment, default_identity_load, tags, costs, likely_gift_shard). So the **exact labels and counts** come from this YAML.  
- **Existing IDs:** Duplicate ids are skipped; `existing_ids` is built from current `state.striving_objects`.  
- **Config:** `(config.get("striving") or {}).get("max_new_per_year", 2)` caps new objects per year (clamped 0..5).  

So **variability = age (bracket) + expectation_baseline (which axes are forbidden/hopeless) + proxy_striving_map content + max_new_per_year**. No randomness; deterministic given state and config.

---

## 3. Active magnets (`state.active_magnets`)

**What they are:** List of `Magnet` (id, magnet_type, label, intensity, tenure_years). Used in persona micrograph (caregivers/peers/institutions) and in Pass 1 summary.

**Where they’re set/updated:**

| When | Where | What happens |
|------|--------|--------------|
| **Yearly** | `active_magnets.update_active_magnets_step` | For each magnet: `intensity -= decay` (default 2), `tenure_years += 1`; remove if intensity < floor (default 15); keep list length ≤ `max_active_magnets` (default 12). **No code path adds new magnets to state.** |
| **Load** | `json_codec` | When restoring state from dict, `active_magnets` are rebuilt from `d["active_magnets"]`. |

**What determines variability:**

- **Addition:** There is **no** code that appends selected magnet_candidates to `state.active_magnets`. The runner selects up to 2 magnets per year and passes them into `build_render_packet` (for Pass 2 / narrative), but they are **never written back into state**. So the only way to have non-empty `active_magnets` is (1) initial state from JSON/backbone that already has magnets, or (2) a seed path that populates them (none found).  
- **Change over time:** Only the yearly step: intensity decay, floor removal, cap. So **variability is only from initial state + decay/trim**; no LLM-driven addition.

---

## 4. Rupture context (rupture_shards, metabolization_processes, plasticity_window)

**What they are:**  
- `rupture_shards`: list of `RuptureShard` (violated assumption, domain, opacity, prediction_error, status, …).  
- `metabolization_processes`: list of `MetabolizationProcess` (domain, severity, mode, status, cluster, plasticity_years_left, …).  
- `plasticity_window`: dict with `years_left`, `framework_switch_sensitivity`, `magnet_susceptibility`, etc.

**Where they’re set/updated:**

| When | Where | What happens |
|------|--------|--------------|
| **Event application** | `delta_templates.apply_deltas_to_state(..., selected_events=...)` | For each item in `selected_events` with `kind == "epistemic_rupture"`, calls `create_rupture_shard_from_event(state, ev)`, which: appends a `RuptureShard`, appends a `MetabolizationProcess`, and sets `state.plasticity_window` (e.g. years_left 1–3). The runner passes `selected_events` so rupture creation runs when such events are selected. |
| **Yearly** | `metabolization_effects.plasticity_step` (if wired) | Decrements `plasticity_window.years_left` and each process’s `plasticity_years_left`; derives `narration_support` from narrators; applies cluster deltas to psychological_capacity and process `downstream_biases`; updates `plasticity_window.framework_switch_sensitivity` from years_left. |

**What would determine variability (once rupture creation is wired):**

- **Whether rupture exists:** LLM proposes an event with `kind: "epistemic_rupture"` and a `rupture` sub-dict (violated_assumption, opacity, prediction_error); scoring selects it; runner must pass `selected_events` into apply_deltas (or into a helper that calls `create_rupture_shard_from_event`).  
- **Content of shard/process:** From the event: domain (from implicated.domains), violated_assumption, opacity, prediction_error, intensity → severity (major vs micro). Cluster comes from `load_rupture_templates()` + `get_template_for_age(templates, state.age)`. plasticity_years_left from opacity (e.g. 1–3 years).  
- **After creation:** plasticity_step drives decay of years_left, narration_support, and cluster-based capacity/bias deltas.

**Current state:** The runner passes `selected_events` into `apply_deltas_to_state`; when the LLM proposes and scoring selects an epistemic_rupture event, rupture shard, process, and plasticity_window are created. Variability is from (1) LLM proposals + selection, (2) event content and rupture templates, (3) plasticity_step (years_left, cluster deltas).

---

## Summary table (variability)

| Layer | Primary variability source | Secondary | Note |
|-------|----------------------------|-----------|------|
| **expectation_baseline** | Identity at seed: parent_baseline, transmission_regime, environment + `need_axis_rules.yaml` | Yearly setdefault(ax,"hopeful") for missing axes | No other updates. |
| **striving_objects** | Age (bracket), expectation_baseline (forbidden/hopeless axes), `proxy_striving_map.yaml`, max_new_per_year | Existing ids (no duplicates) | Append-only; no retirement. |
| **active_magnets** | Initial state (e.g. from JSON) only | Yearly decay/floor/cap | **Selected magnets are never added to state.** |
| **rupture context** | LLM epistemic_rupture events + scoring + apply_deltas_to_state(selected_events=...) | plasticity_step (years_left, cluster deltas) | Rupture creation wired; runner passes selected_events. |

---

## Fixes implied

1. **Magnets:** Add a step (in the runner or inside a new “apply selections” function) that converts `selected_magnets` (dicts) into `Magnet` instances and appends them to `state.active_magnets` (with sensible default intensity/tenure).  
2. **Rupture:** Done. `apply_deltas_to_state` now takes `selected_events`; the runner passes it and rupture shards/processes/plasticity_window are created for each selected epistemic_rupture event.
