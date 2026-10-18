# v3 Structural Persona Engine — Integrated Overview

Single reference merging OVERVIEW.md, overview2.md, and v3config.yaml. Coherent structure; authority and source order at the end.

---

## 1. Purpose, governing question, deliverable

v3 is a **structural persona simulation engine**: longitudinal persona state under structural and psychological constraints. Ontological shift from needs/strategy-centered psychology to **structure/strata-centered political engine** (domain matrix, alienation, cracks, frameworks as metabolic operators, peak routing).

**Governing question (every simulated year):**

**Given this person’s constraints, capacity, wounds, buffers, and environment, how does vitality circulate between self and world?**

Everything in the model exists to make that question computable. The simulation is not judging good/bad/revolutionary/selfish; it is modeling **how a life organizes itself under pressure over time.**

- **Deliverable:** persona_sheet.json (or equivalent) compatible with `run_conversation_chat.py --persona-json`.
- **Ground rule:** Do not refactor v2. v3 is a parallel module. Runnable without DB or survey data by seeding a persona JSON.

---

## 2. Two-layer architecture: Backbone vs Phenomenology

**Layer A — Backbone (v3)**  
The causal physics. Updates the person each year. Contains: constraints, capacity, buffers, cracks, alienation, domains, collective_infrastructure, practice_stack, peak-routing variables (loop_topology, solidarity_boundary, harm_constraint, etc.). Produces **state changes**.

**Layer B — Phenomenology (v2)**  
The rich persona layer. **Renders** the person after the yearly update: needs, strategies, symbols, narrative voice, Enneagram patterns, beliefs and identity language. Produces **expression**, not causality.

v2 is not replaced. v3 is the **engine underneath it**. The LLM renders phenomenology from backbone state; it may propose candidate deltas but must not apply them. Code enforces caps, hysteresis, and gates.

---

## 3. Stored vs derived (discipline)

**Only slow-changing real things are stored.** Summary indicators are computed each year.

**Stored state** persists year-to-year (see §5 for full schema). **Derived indices** are thermometers, computed yearly: Hostage Index, Agency Capacity (AC), Insulation Score, Structural Lucidity (SL), mis_aim_risk, peak-regime eligibility. They are not persisted unless cached.

---

## 4. Closed ontology and pillars

No further conceptual primitives before code. Pillars:

| Pillar | Description |
|--------|-------------|
| **Strata stack** | Planetary → … → self; field pressures (provision, coercion, contradiction, visibility of complicity) and salience. |
| **Framework set** | Metabolic operators (weights, acute/chronic deltas, half-life, failure modes, institutional affinities). Max N active (e.g. 3–6); cold storage and merge rules. |
| **Domain matrix (A/S/V/Aim)** | Per-domain: Awareness, Solidarity, Viscerality, Aim (latent vs expressed). Aim mostly latent; expressed aim gated by registers + hostage + coercion. |
| **Alienation** | Tracked or derived from capacity + domain mismatches. |
| **Crack register** | Persistent tensions; no resolution — persist, suppress, or displace. |
| **Reproduction constraints** | Dependents, housing, legal status, debt, job insecurity, caregiving load → Hostage Index. |
| **Loop topology** | **reciprocal** \| **extractive** \| **self_contained**. Where vitality comes from and goes. |
| **Solidarity boundary** | **none** \| **transactional** \| **in_group** \| **expanding** \| **universal**. Who counts as “us.” |
| **Peak-routing extensions** | **harm_constraint** (willingness to use lethal force; Jesus vs Che split); **rage_metabolization** (rage → discipline vs mis-aim); **theory_of_change_style** (witness_exposure, mass_nonviolent_disruption, armed_deterrence, armed_insurrection, institution_building). |
| **Intensity and capture** | **intensity** (fuel; ≠ structural alignment); **craft_talent**, **opportunity_access**, **attention_field_exposure**, **capture_pressure** (institutions steering the person). |

---

## 5. Cloud, crystallization, intensity

**Cloud:** Default human state — mixed motives, partial care, contradictions managed by buffers, ego + goodness + complicity coexist. The engine must produce **a world full of lively, passionate, thoughtful people in the cloud**, not sleepy moderates or default saints/monsters.

**Crystallization:** Under sustained pressure, trajectories stabilize. Requires repeated routing of contradiction the same way, rising coherence, sufficient capacity and infrastructure. Only a tiny subset crystallizes into world-bearing, predatory, or deeply self-contained roles. Slow and rare.

**Intensity ≠ structural alignment:** **intensity** = emotional vividness, urgency, aliveness, rhetorical fire, existential energy. Widely distributed. Crystallization is rare. Mass movements **reorganize** intensity; they do not create new souls. Crystallization probability rises when intensity is high and structural lucidity, agency capacity, and collective infrastructure rise.

---

## 6. Stored state schema (merged)

**Design decision — capacity (resolve before Wave 3):** The spec mixes two “capacity” notions. This is intentional (two traditions in the docs) but **must be resolved before implementing real system logic (Wave 3)**. Not urgent for Wave 1–2 (stubs can use either); everything else can proceed until then.

| Model | Fields | Source |
|-------|--------|--------|
| **Material capacity** | time, money, health, social_support, skill, mobility, risk_tolerance, legitimacy | v3config, overview2; feeds AC, hostage penalty, insulation. |
| **Psychological capacity** | vitality, aperture, reality_anchor, binding, coherence, agency, transmutation | spec/OVERVIEW; “chronic shaping substrate”; feeds domains, buffers, metabolic style. |

**Decision (implemented):** We **store both vectors**. `state.capacity` = material; `state.psychological_capacity` = vitality, aperture, reality_anchor, binding, coherence, agency, transmutation. State summary and scoring use psychological_capacity; AC in summary comes from derived. When loading JSON that lacks `psychological_capacity`, the codec derives it from material + peak_routing + intensity. See `core/state.py` (PsychologicalCapacity) and `io/json_codec.py` (_derive_psychological_from_material).

**Material / structural**  
- **Capacity** (0–100 each): time, money, health, social_support, skill, mobility, risk_tolerance, legitimacy.
- **Psychological capacity** (0–100 each): vitality, aperture, reality_anchor, binding, coherence, agency, transmutation. Stored in `state.psychological_capacity`.  
- **Reproduction constraints:** dependents, housing_insecurity, legal_insecurity (0=secure, 100=precarious), debt, job_insecurity, caregiving_load.

**Psychological / adaptive**  
- **Buffers** (type, strength, cost_profile: time/money/relational/truth cost). Max total 8. Types: piety, ideology, craft, intimacy, work, intoxication, status, family_role, health_regimen, escapism.  
- **Cracks** (type, intensity, latent_pressure, active, origin_year). Max total 8, max active 3. Types: shame_core, rage_core, dissociation, nihilism, intimacy_avoidance, authority_fixation, performance_compulsion, moral_alibi.  
- **Alienation** (0–100).  
- **Domains** (per domain): A, S, V, Aim (0–100). Domain names for SL baseline: e.g. empire_occupation, nation_state, sect_class_ethnicity.

**Collective**  
- **Collective infrastructure:** network_density, org_discipline, resource_pool, repression_pressure, elite_splits.  
- **Practice stack:** study, care, organizing, craft, spiritual, risk_training.

**Peak routing (stored)**  
- loop_topology, solidarity_boundary, harm_constraint, rage_metabolization, theory_of_change_style, coherence, impunity_access, appetite_profile (status, control, sensuality, care).

**Intensity and capture**  
- intensity, craft_talent, opportunity_access, attention_field_exposure, capture_pressure.

**Other (from spec/OVERVIEW)**  
- **Wound vector:** sensitivities (shame, fear, anger, abandonment, control, recognition, loss); default coping channels; optional type_label (never drive logic by label alone).  
- **Registers:** public_expression_gate, private_expression_gate, inner_load.  
- **Calibration regime / boundary maps** (per nation/sect_class/domain).  
- **YearRecord / history:** deltas + narrative snapshot.

---

## 7. Derived indices (computed yearly)

- **Hostage index:** weighted sum of reproduction_constraints (dependents, housing_insecurity, legal_insecurity, debt, job_insecurity, caregiving_load); higher = more constraint.  
- **Insulation score:** e.g. top-k buffer strengths + money.  
- **Structural Lucidity (SL):** e.g. domain lucidity average over key domains (A minus insulation plus viscerality component).  
- **Agency Capacity (AC):** weighted sum of capacity components minus hostage penalty.  
- **mis_aim_risk:** e.g. alienation, hostage_index, organizing_deficit.  
- **Peak-regime eligibility:** SL ≥ threshold, AC ≥ threshold, hostage_index ≤ threshold, coherence ≥ threshold for N consecutive years.

---

## 8. Peak routing in detail

When **SL** and **AC** are both high, outcome is determined by **(loop_topology, solidarity_boundary)** plus **harm_constraint** and **theory_of_change_style**.

**Loop topology:** reciprocal (nourish/be nourished; only loop that produces world-bearing roles); extractive (domination/consumption; predatory integration); self_contained (mastery/art/meaning; can feed reciprocal or stay insulated).

**Solidarity boundary:** none → only self; transactional → family/partners as exchange; in_group → tribe, nation, religion, class; expanding → widening empathy; universal → humanity as kin. Determines whether lucidity becomes revolutionary, nationalist, sectarian, managerial, or predatory.

**Jesus + Che = one attractor:** world-bearing reciprocal integration (high SL, high AC, reciprocal loop, expanding or universal boundary, high coherence, rage metabolized into discipline). They diverge in **harm_constraint** (very high → will not kill; moderate → violence under disciplined necessity) and **theory_of_change_style** (witness_exposure, mass_nonviolent_disruption, armed_deterrence, armed_insurrection, institution_building). Violence vs nonviolence is a **strategic branch**, not a moral category.

**rage_metabolization (0–100):** Low → rage becomes mis-aim, scapegoating, expressive violence, factionalism. High → rage becomes clarity, discipline, strategic patience. Separates crude activism from disciplined revolutionary work.

**Predator gating:** Predatory integration requires high AC, high impunity_access, low/none solidarity boundary, extractive loop stabilized, high coherence, appetite toward control/consumption. Rare.

**Base-rate discipline:** High SL uncommon; high AC uncommon; high SL + high AC very uncommon; high SL + high AC + liberatory orientation extremely uncommon. Engine must produce extractive/self-contained/insulation more often than revolutionary attractors. “No saint factory” via gates, hostage penalty, topology hysteresis, coherence requirement, capture pressure increasing mis-aim unless stabilized.

---

## 9. Strategy, signal, attention and capture

**Actions as signals:** Every meaningful action produces field effects (morale, recruitment, legitimacy, fear, defections, repression_justification, myth-making). Violence and nonviolence both function as communication channels. **signal_power** from attention exposure, network size, collective infrastructure, craft, role.

**theory_of_change_style** (see §8) maps to default **signal profiles** per audience (in_group, neutral_public, out_group, security_apparatus, international); signal vectors (morale, recruitment, legitimacy, fear, defections, repression_justification) feed back into infrastructure and person (e.g. recruitment → network_density, repression_justification → repression_pressure).

**Attention and capture:** **intensity** (fuel) is distinct from **craft_talent**, **opportunity_access**, **attention_field_exposure**. High attention alters signal power, AC, temptation gradients, surveillance, ego/paranoia, handler systems. **capture_pressure** = how strongly institutions steer the person. Attention pushes loop topology away from reciprocal unless stabilized (practice stack, collective infrastructure, coherence, rage_metabolization, expanding boundary). Celebrity is structurally hostile to world-bearing reciprocity; movements boost AC differently (network, discipline, protection, meaning) and can hone ordinary people without turning them into brands.

**Repression** shapes burnout risk, solidarity, radicalization, martyrdom, mis-aim. **Collective infrastructure** provides emotional regulation, shared meaning, distributed leadership, protection, skill development, stamina — increasing AC, coherence, discipline, reciprocal loop stability.

---

## 10. Need axes, baselines, and proxy strivings

Source: need_axis_rules.yaml, proxy_striving_map.yaml.

**Need axes (10):** attachment, safety, belonging, status, competence, autonomy, meaning, justice, beauty_play, eros_intimacy.

**Expectation baseline per axis:** Score [-2, +2] from parent(s) + env + regime → **entitled** (+1,+2), **hopeful** (0), **forbidden** (-1), **hopeless** (-2). Derivation uses seed weights, global modifiers (warmth+consistency, anxiety, shame, openness), per-axis and conditional modifiers, optional flags (volatility, brittle). **meaning_frame:** integrative \| authoritarian \| absent \| cynical. Contradiction across axes is allowed (e.g. belonging entitled, autonomy forbidden).

**Baselines drive striving:** Entitled → early spawn, high investment; hopeful → normal; forbidden → proxy/secret striving; hopeless → fewer objects, low investment until “gift shard.” Proxies become later rupture sites.

**Proxy striving map:** (NeedAxis, BaselineState, age_bracket) → proxy objects. Age brackets: 3, 7, 11, 14, 17, 24, 35. Each proxy: id, label, tags, default_investment, default_identity_load, secrecy, costs, likely_gift_shard. Axes: autonomy, eros_intimacy, beauty_play, meaning, justice, competence, belonging, safety, status.

---

## 11. Rupture and event system

**Rupture templates** (e.g. engine/effects/rupture_templates.yaml): violated_assumption, domain, strata_levels, cluster_candidates, mode_priors, narrator_priors by age, severity_prior by age.

**Clusters (5):** hardening_protection, sensitivity_exposure, meaning_rebinding, cynicism_sealing, justice_engagement. **Modes (6):** assimilation, accommodation, sealing, collapse, transmutation, mis_aim. **Age brackets:** 3, 7, 11, 14, 17, 24, 35. **Domains (examples):** family_household, body_self, sect_class, nation, empire_occupation.

Scoring: rupture candidate → template → cluster/mode shortlist + priors → score against state (hostage, coercion, capacity, wound, support). **Delta scheduling:** e.g. 60/30/10 split; burnout/rebound for justice_engagement; Malheur multiplier; clamp deltas.

**Cracks rules (v3config):** spawn (intensity_on_spawn, spawn_if_room); annual update (intensify_range, latent_decay_if_insulated, activation/deactivation thresholds); brittleness (allow_low_active_if_insulation high, require latent_pressure).

---

## 12. Yearly causal loop (step order)

**Canonical sequence:** `v3_yearly_step_order.yaml`. Mechanical contract: prevent circular causality, prevent LLM from mutating backbone, make module ordering explicit and testable. Timestep = year; max 3 events/year; clamp after each step. **Invariants:** events do not directly set domains or topology; LLM does not mutate backbone; derived indices computed only from stored state; sequence must be executed in order.

**Derived indices** are computed after the step that provides their inputs: hostage_index (after 3); agency_capacity_AC (after 4); insulation_score (after 5); structural_lucidity_SL (after 7); mis_aim_risk (after 8); peak_regime (after 10).

| # | Step id | Mutates | Derived |
|---|---------|---------|---------|
| 1 | **field_update** | state.field | — |
| 2 | **event_sampling** | state.events_this_year | — |
| 3 | **reproduction_constraints_update** | state.reproduction_constraints | hostage_index |
| 4 | **capacity_update** | state.capacity | agency_capacity_AC |
| 5 | **buffers_update** | state.buffers, state.capacity | insulation_score |
| 6 | **frameworks_update** | state.frameworks | — |
| 7 | **domains_update** | state.domains | structural_lucidity_SL |
| 8 | **cracks_and_alienation_update** | state.cracks, state.alienation | mis_aim_risk |
| 9 | **practice_and_infrastructure_update** | state.practice_stack, state.collective_infrastructure | — |
| 10 | **topology_and_boundary_update** | state.peak_routing (loop_topology, solidarity_boundary, coherence) | peak_regime |
| 11 | **attention_and_capture_update** | state.intensity_and_capture, optionally state.capacity | — |
| 12 | **strategy_and_signal_effects** | state.collective_infrastructure | — |
| 13 | **style_trait_drift** | state.style_traits | — |
| 14 | **render_layer** | state.rendered_output only | — |

Each step declares **inputs**, **outputs_mutate**, **prohibits_mutation_of** (e.g. early steps prohibit mutating domains/peak_routing; domains and cracks steps prohibit mutating loop_topology/solidarity_boundary; render_layer prohibits mutating entire backbone), and **modules** (e.g. `systems/field.py::update_field`). **Delta caps** (v3config) limit annual change per field unless shock overrides. **Tests** (in the YAML): step order enforced; no direct domain/topology/boundary set by events; LLM no backbone mutation; caps respected; hysteresis respected.

---

## 13. Pipeline: Propose → Score → Apply → Render

- **LLM proposes:** Candidate events and magnets in strict schema (kind, channels, implications, offers/costs, hooks). No numerical deltas; causal hypotheses only. Caps: e.g. 0–6 event candidates, 0–4 magnet candidates, 0–3 branch hypotheses.  
- **Code scores:** age_fit, channel_available, salience_fit, hostage_fit, capacity_fit, wound_fit, novelty_penalty, coercion_penalty. Select: ≤2 major (including shock), ≤2 minor, ≤1 surprise with probability.  
- **Code applies:** Event/magnet → delta templates (bounded); enforce invariants. LLM never sets deltas.  
- **LLM renders:** Selected events + applied deltas + updated state summary → scene, texture, dialogue, consistency with state. Optional: ParticularityBlock, jaggedness, PersonStub.

Two-pass contract: **Pass 1** CandidatePacket (LLM → candidates); **Pass 2** RenderPacket (code → LLM) and RenderOutput (narrative_snapshot, consistency_check).

---

## 14. Enneagram and style traits (phenomenology only)

**Enneagram** is not the engine; it is **parameterization**. It biases how a person metabolizes the same constraints: buffer preferences, crack styles, mis-aim tendencies, topology friction, strategy attractors, appetite_profile weights. Implemented as coefficients in update functions. Does not decide history, override constraints, or create saints.

**Style traits** (orthogonal to backbone; render layer only): playfulness, novelty_seeking, conscientiousness, social_energy, absurdist_humor, aesthetic_sensitivity, impulsivity. Used for voice/behavior tendencies (render_guidelines). Style drift: slow annual delta; event modifiers (burnout, recovery, new_romance, parenting, humiliation, etc.). **Render contract:** Backbone variables must not be referenced unless contextually triggered. At least 3 style-trait behaviors in ordinary scenes. ≥70% of daily-life scenes with no political/structural language. Humor, relationships, hobbies, mundane concerns dominate. Structural lucidity appears primarily during stress, conflict, or reflection.

---

## 15. Invariants, tests, rendering contract

**Hard invariants:** All numeric fields clamped (e.g. 0–100); len(cracks) ≤ max_total; active_cracks ≤ max_active; len(buffers) ≤ max_total; derived indices not persisted unless cached; events do not directly set domains or topology; yearly_step order respected.

**Policy invariants:** At least 2 cracks active unless explicitly insulated (then record brittleness). At least 2 frameworks above threshold OR mono-framework insulation. Expressed aim non-empty in public only if coercion below threshold OR defiance channel + low hostage + high agency/binding. No over-rage: high hostage/coercion → expressed aim usually empty. No resolution: cracks persist, suppress, or displace. Peak-regime rate under target (e.g. &lt;1% in population runs) as soft check.

**Rendering contract (v3config):** LLM may render narrative and phenomenology from backbone state; may propose candidate deltas but must not apply them. Prohibited: direct mutation of backbone by LLM; bypassing caps, hysteresis, or gates.

**Tests:** test_step_sanity (10 years, no NaNs/runaway); test_distribution (e.g. 500 agents, public rage in target band); test_postmodernism_half_life; test_compartmentalizer.

---

## 16. Module layout, phases, integration

**Module layout (spec):**  
v3/ — schema/ (persona_state, enums, invariants), field/ (strata, calibration, affordances, reproduction), psyche/ (vitality, wound, metabolism, registers, channels), frameworks/, domains/, engine/ (step, events, deltas, narrative), io/, tests/.

**Phases:**  
1) State model only (no world data). 2) Recursion engine (event → stratum, framework, awareness, cracks). 3) Field injection (driver_model, civic_soul, imperial_block). 4) Micro layer optional (needs/strategies from v2 or derived).

**Phase 1 deliverable (overview2):** Runnable simulation that steps year by year, updates backbone state deterministically, passes invariants, outputs stable JSON each year. Minimal skeleton: core/enums.py, core/state.py, core/derived.py, engine/yearly_step.py, systems/*, tests/test_invariants.py.

**Integration:** Output = persona_sheet.json for `run_conversation_chat.py --persona-json`. Input = seed persona JSON. Harmonization layer (harmonized/) provides field conditions when integrated. v2 remains; conversation engine consumes v3 output.

---

## 17. What’s next

Ontology is closed. Next step: philosophy → code (file structure, dataclasses, JSON schema, recursion engine, delta contract, invariants/tests). Tuning via **v3config.yaml** (enums, caps, formulas, hysteresis, cracks_rules, attention_system, strategy_and_signal). Build map / task plan in a separate YAML as needed.

---

## Source hierarchy

This overview merges:

- **OVERVIEW.md** — starter_engine-final ontology, capacity vector (vitality/aperture/…), need axes, proxy strivings, rupture system, spec/specLLM pipeline.  
- **overview2.md** — Governing question; two-layer backbone/phenomenology; stored vs derived; cloud/crystallization; intensity ≠ alignment; peak routing (Jesus/Che as one attractor, harm_constraint, theory_of_change_style, rage_metabolization); strategy/signal; attention/capture; Enneagram as parameterization; minimal v3 backbone block; Phase 1 skeleton.  
- **v3config.yaml** — Stored state schema, derived index formulas, peak_gates, delta_caps, hysteresis, cracks_rules, attention_system, strategy_and_signal (audiences, default_profiles, signal_application), invariants, rendering_contract, style_traits, render_guidelines.

**Canonical text order (oldest → newest):** new_version.txt → spec.txt → specLLM.txt → starter_engine.txt. **Authority:** The way starter_engine.txt ends is the final statement on v3. **Branch docs:** overview2.md, v3config.yaml, **v3_yearly_step_order.yaml** (canonical 14-step sequence and derived-index schedule; see §12), need_axis_rules.yaml, proxy_striving_map.yaml. If any branch conflicts with starter_engine.txt, starter_engine.txt wins.
