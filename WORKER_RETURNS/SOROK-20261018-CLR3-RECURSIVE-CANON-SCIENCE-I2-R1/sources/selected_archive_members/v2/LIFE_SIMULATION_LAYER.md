# Life Simulation Layer: The Missing Engine

*Sits between **persona** (psychology) and **response generation**. Personality explains how someone reacts; life explains what they react **from**. Without this layer, the persona has psychology without logistics—and humans are logistics + psychology.*

**Reference:** PERSONA_CONVERSATION_ENGINE_SPEC.md (Life Scaffold → Life Container; Today State; effort budget). This document defines the **full** life simulation pipeline and the **attention scalars** that gate response.

---

## Why This Fixes "Sounds Like ChatGPT"

The model currently gives **full effort** every time. Humans almost never do. This layer introduces:

- **Attention scarcity** — finite attention budget
- **Competing goals** — open loops, next obligation
- **Impatience** — time pressure, interruptions risk
- **Partial focus** — mood, physical state, location
- **Emotional carryover** — stressor, season
- **Inconsistent engagement** — why they're in the chat

Which produce **human chat**: short replies, topic drift, selective response, misread tone, random details, uneven warmth.

---

## The 4 Layers + Attention

### Layer 1: Structural Life Constraints (Life Container)

**Permanent life reality.** **Not** generated at conversation time—**derived from simulation results**. By the time the life-course simulation has run to the present, the recursions must have generated and stored what is necessary. The Life Container is **populated from** (or **derived from**) the persona history: final state, last N years of recursion deltas, and/or a dedicated "present life" snapshot produced by the simulation.

| Field | Description | Source in simulation |
|-------|-------------|----------------------|
| job_type | e.g. back_office, call_center, retail, informal, unemployed, student | Recursion output (present year): occupation / work situation |
| commute_style | none, walk, bus, motorcycle, car, long_commute | From job + location + narrative |
| living_arrangement | with_family, with_roommates, alone, with_partner, unstable | Events, narrative, family_obligations |
| family_obligations | none, light, primary_supporter, eldercare, childcare | Needs, strategies, narrative (who they support) |
| income_stress | low, medium, high, crisis | World slice + final needs + narrative |
| internet_access_patterns | home_only, phone_only, work_and_phone, unreliable, abundant | Context, media_tech, language_experience |
| social_circle_density | isolated, thin, moderate, dense | Roles, belonging, narrative |
| sleep_debt_baseline | none, light, chronic, severe | Strategies, routines, indices (RMT) |

**Implementation:** Ensure the recursion (especially for the **present** year or 17+ band) outputs or allows inference of these fields—e.g. via `life_snapshot` in RecursionDelta or a "present life" block in the persona sheet. At conversation time: **derive_life_container_from_simulation(persona_history)** instead of generating from scratch.

**Data governance (maximal realism):** Life snapshot is **data-governed**, not free-generated. See `v2/config/life_snapshot.yaml` and `v2/life_snapshot_from_data.py`.

- **Fully from pipeline data (no LLM):** `income_stress` (world_slice GDP, inequality, identity.current_class, needs.safety), `internet_access_patterns` (world_slice.media_saturation, urbanicity, SES), `social_circle_density` (needs.belonging_group), `sleep_debt_baseline` (indices.RMT, strategies dissociation/withdrawal).
- **Data-constrained choice:** `job_type`, `commute_style`, `living_arrangement`, `family_obligations` use config priors by SES, age band, urbanicity; the LLM **confirms or adjusts** only when narrative contradicts (e.g. lost job → unemployed).
- **Taxonomy choice:** `current_life_phase` — LLM picks from a fixed list given narrative; data can suggest from events/strategies.
- For the **present-year** recursion, the prompt receives **data-derived defaults** and **valid option sets** per field; the model outputs `life_snapshot` with the same keys, selecting only from allowed values. Result is stored in `RecursionDelta.life_snapshot` and persisted on `Palimpsest.life_snapshot` for derivation of Life Container.

**This is the life container.** Everything else is conditioned on it.

---

### Layer 2: Current Life Season (months)

**Humans always exist inside a phase.** **Derived from simulation results**—the last year(s) of recursion output and narrative (e.g. job hunt, burnout, caring for parent, activism surge, stable routine). The simulation should produce or make inferable the **current life phase** so that at "present" we derive Life Season from stored output, not from a separate draw at conversation time.

| Example seasons | Effect |
|----------------|--------|
| job_hunt_phase | Attention on applications, anxiety, low patience |
| relationship_phase | Emotional bandwidth to partner; distraction or openness |
| burnout_phase | Low bandwidth, short fuse, withdrawal |
| caring_for_parent_phase | Time pressure, guilt, exhaustion |
| saving_money_phase | Frugality, stress, deferred gratification |
| spiritual_recommitment_phase | More reflection, less small talk |
| activism_surge_phase | High engagement on certain topics; tired otherwise |
| stable_routine_phase | Predictable attention and mood |

**Season determines:** attention budget, emotional bandwidth, conversational patience. It modulates Layer 3 and Layer 4.

---

### Layer 3: Today State (per conversation)

**Every chat must generate (or retrieve) a Today State.** This is the **missing realism engine**.

| Field | Example / range |
|-------|------------------|
| sleep_hours | 5.5 (late scrolling) |
| mood_baseline | slightly_irritable, neutral, anxious, okay, low |
| current_stressor | coworker_conflict, money, family, health, none |
| open_loops | 6 (unfinished tasks) |
| next_obligation_minutes | 40 |
| physical_state | mild_headache, tired, hungry, fine, sick |
| phone_battery_pct | 23 |
| location | shared_living_room, commute, work, alone_room, cafe |
| interruptions_risk | high, medium, low |
| time_windows | Optional: when they can actually focus |

**Generated per conversation** (or per day with a small random walk). Feeds directly into attention scalars.

---

### Layer 4: Interaction Context (why they're in this chat)

**The conversation has a situational reason.** Generated **per conversation** (or per session with a reason).

| Example reasons | Effect on tone and effort |
|-----------------|---------------------------|
| paid_microtask | Transactional, minimal, time-bound |
| language_exchange | Patient, trying to practice; may misread |
| boredom_scrolling | Low effort, drift, short replies |
| activism_curiosity | Engaged on topic; may probe or lecture |
| friend_of_friend_intro | Polite, sizing up, moderate effort |
| trying_to_practice_English | Forgiving of errors; may ask for correction |
| procrastinating_work | Guilty, distractible, variable engagement |
| lonely_evening | More open, longer replies, or brittle |

**Determines:** tone, effort level, willingness to go deep, patience.

---

### Attention Scalars (gate response)

**0–100 scalars that gate response length and depth.** Without these, the model always gives full effort.

| Scalar | Meaning |
|--------|---------|
| attention_available | How much attention they can give this exchange (0 = scattered, 100 = fully present). |
| effort_willingness | How willing they are to invest (0 = minimal, 100 = full). |
| social_energy | How much social battery is left (0 = depleted, 100 = fresh). |

**Derived from:** Life Container (sleep_debt_baseline, social_circle_density), Life Season (burnout vs stable), Today State (sleep, mood, next_obligation, interruptions_risk), Interaction Context (why they're here).

**Use:** Gate max reply length, depth of hooks addressed, coherence effort. Humans almost never give full effort; these scalars enforce that.

---

## Pipeline: What to Implement

```
STEP 1 — Static persona (you already have)
         persona_dini.json / PersonaHistory

STEP 2 — Simulation produces life-container and life-season data
         By the time we reach "present" age, recursions have generated and stored:
         job_type, living_arrangement, family_obligations, income_stress, etc.;
         current_life_phase (season). Stored in RecursionDelta.life_snapshot (present year)
         and/or persona sheet "present life" block.

STEP 3 — Derive Life Container and Life Season from simulation (once per session)
         derive_life_container_from_simulation(persona_history)
         derive_life_season_from_simulation(persona_history, last N deltas)
         No separate generation—populate from what the simulation already produced.

STEP 4 — Generate Today State (per conversation)
         sleep, mood, stressor, open_loops, next_obligation,
         physical_state, location, interruptions_risk, device

STEP 5 — Generate Interaction Context
         why_in_chat (paid_microtask, language_exchange, boredom, etc.)

STEP 6 — Compute Attention Scalars
         attention_available, effort_willingness, social_energy
         from Container + Season + Today + Interaction

STEP 7 — Feed ALL OF IT into response generation
         Persona + Life Container + Season + Today + Context + Attention
         → then generate reply (with length/depth gated by attention)
```

**Only then** generate the reply. The response layer (PERSONA_CONVERSATION_ENGINE_SPEC Part 3: hooks, salience, effort budget, moves) uses these as inputs; effort budget is explicitly driven by attention scalars.

---

## Data Structures (see life_simulation_schema.py)

- **LifeContainer** — Layer 1 (structural constraints). **Derived from** simulation: `derive_life_container_from_simulation(persona_history)`.
- **LifeSeason** — Layer 2 (current phase). **Derived from** simulation: `derive_life_season_from_simulation(persona_history)`.
- **TodayState** — Layer 3 (today’s conditions). Generated per conversation (or per day).
- **InteractionContext** — Layer 4 (why in chat). Generated per conversation.
- **AttentionBudget** — attention_available, effort_willingness, social_energy. Computed from container + season + today + interaction.

**Simulation output:** `RecursionDelta.life_snapshot` (present-year recursion) holds job_type, living_arrangement, family_obligations, income_stress, internet_access_patterns, social_circle_density, sleep_debt_baseline, current_life_phase. See v2/recursion_schema.py.

---

## Integration with PERSONA_CONVERSATION_ENGINE_SPEC

- **Life Scaffold** (spec Part A / 5.2) → **Life Container** (this doc). Expand with: commute_style, internet_access_patterns, social_circle_density, sleep_debt_baseline.
- **Today State** (spec 4.3) → **Today State** (this doc). Align fields: add sleep_hours, mood_baseline, current_stressor, open_loops, next_obligation_minutes; keep location, interruption_prob, device.
- **Life Season** — new in this doc; not in original spec.
- **Interaction Context** — new in this doc; not in original spec.
- **Effort budget** (spec Step 6) → driven by **AttentionBudget** (attention_available, effort_willingness, social_energy).

Build order in the conversation spec (Part 11) becomes: ensure simulation produces life_snapshot (Step 2); implement derive_life_container_from_simulation and derive_life_season_from_simulation (Step 3); instantiate_today(container, season, date); instantiate_interaction_context(...); compute_attention_budget(...). Then persistent stores (life_container, today_state, relationship_state), then analyze_message, extract_hooks, select_salient_hooks, etc. Life Container and Life Season are **not** instantiated from scratch—they are **derived from** the simulation results.

---

## Brutal Summary

You did the hardest philosophical part: the psyche. But you skipped the mundane machinery of life. Humans are mostly mundane machinery. **Personality explains how someone reacts. Life explains what they react from.** You now need to simulate the second.
