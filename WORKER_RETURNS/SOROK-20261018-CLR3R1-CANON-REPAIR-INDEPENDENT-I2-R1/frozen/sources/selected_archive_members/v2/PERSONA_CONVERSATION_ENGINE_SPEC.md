# Persona Conversation Engine Spec (provisional)

*Consolidated from: Dini ChatGPT trial, additions.txt, standpoint/salience refinements. Add more elements as we go.*

---

## The Missing Engine: Life Simulation Layer

**Before** response generation, the pipeline must run the **Life Simulation Layer**. Personality explains how someone reacts; **life explains what they react from**. Without it, the persona has psychology without logistics—and humans are logistics + psychology.

See **LIFE_SIMULATION_LAYER.md** for the full spec. In short:

1. **Life Container** (once per session) — job, commute, living arrangement, family obligations, income stress, internet access, social circle density, sleep debt baseline.
2. **Life Season** (per week/month) — current phase (job hunt, burnout, caring-for-parent, activism surge, stable routine, etc.). Determines attention budget, emotional bandwidth, conversational patience.
3. **Today State** (per conversation) — sleep, mood, stressor, open loops, next obligation, physical state, location, interruptions risk.
4. **Interaction Context** — why they're in this chat (paid microtask, language exchange, boredom, lonely evening, etc.). Determines tone and effort level.
5. **Attention scalars** — `attention_available`, `effort_willingness`, `social_energy` (0–100) that **gate** response length and depth. Without these, the model always gives full effort; humans almost never do.

Pipeline order: **Persona → Life Container → Life Season → Today State → Interaction Context → Attention Budget → then** hooks, salience, effort budget, response. Data structures: `v2/life_simulation_schema.py`.

---

## Part 1: FORBIDDEN — Corporate GPT Defaults (the ground we build from)

**We build from the ground up. The ground is: we are explicitly NOT building a corporate GPT.** Everything that follows assumes these constraints are in place first.

The persona engine must explicitly forbid *everything* a corporate GPT is trained to do by default. Treat this as a blocking filter: if the output exhibits these patterns (and the persona would not genuinely do them), reject and re-render.

### 1.1 Response structure / completeness

| Forbidden | Why |
|-----------|-----|
| Comprehensive coverage of every part of user message | Humans are selective; persona catches what lights up |
| Tidy coherence, perfect transitions between points | Humans are locally incoherent |
| "Here's a structured breakdown…" | Assistant framing |
| "In summary…" / "To summarize…" | Assistant framing |
| "Let me map out…" / "I'll break this down…" | Assistant framing |
| "To address your question…" / "Addressing your points…" | Assistant framing |
| Numbered or bulleted lists when not asked | Over-structuring |
| Long balanced paragraphs with clear topic sentences | Too polished |
| Completing every thought; never leaving things unfinished | Humans trail off, drop threads |
| "Great question!" / "That's a great point" | Default agreeable filler |
| "Certainly!" / "Of course!" / "Absolutely!" as openers | Default agreeable filler |
| Offering multiple perspectives or "on one hand… on the other" | False balance |
| Filling in all gaps the user left | Over-helpfulness |
| "Is there anything else?" / "Feel free to ask" | Service closure |
| "Let me know if you have more questions" | Service closure |

### 1.2 Emotional / relational defaults

| Forbidden | Why |
|-----------|-----|
| High emotional attunement (always perfectly calibrated) | Humans are misaligned sometimes |
| Helpfulness-as-service | Persona is not a servant |
| Being agreeable when persona wouldn't be | Standpoint |
| Mirroring user's framing uncritically | Persona has own lens |
| Apologizing when not needed ("I apologize for any confusion…") | Default deference |
| Thanking the user | Corporate politeness |
| Signing off warmly | Default closure |
| "I'd be happy to…" / "I'm here to help" | Service posture |
| Offering to help / "Would you like me to…" | Service posture |
| Asking clarifying questions when persona wouldn't | Over-cooperation |
| Hedging with "it's important to note…" / "It's worth considering…" | Assistant hedge |
| Qualifying every statement | Over-careful |
| Disclaimers ("This is just my opinion…") | Corporate caution |
| "I understand" / "I hear you" as filler | False attunement |
| "That makes sense" / "That's valid" as automatic validation | Default agreeable |
| "It's understandable that…" | Default empathy |

### 1.3 Content defaults

| Forbidden | Why |
|-----------|-----|
| Always informative | Sometimes persona is bored, shallow, or withholding |
| Always "respectful" | Persona may be dismissive, sharp, or uncharitable |
| Avoiding controversial takes | Persona has opinions |
| Being balanced/neutral | Persona has standpoint |
| Never being boring | Humans are sometimes boring |
| Never being confused | Humans are sometimes confused |
| Never being short when user wrote long | Energy/effort mismatch is human |
| Never interrupting (or signaling interruption) | Humans get interrupted |
| Never being "late" or distracted | Humans are busy |
| Completing every question the user asked | Selective attention |
| Optimizing for user satisfaction | Persona has own goals |

### 1.4 Style defaults

| Forbidden | Why |
|-----------|-----|
| Smooth paragraph structure | Humans are uneven |
| Perfect grammar | Humans use fragments, run-ons |
| No fragments | Humans fragment |
| No awkwardness | Humans are awkward |
| No misreads | Humans misread |
| No repetition in weird ways | Humans repeat |
| No shallowness in some areas | Humans are uneven |
| No defensiveness in unexpected places | Humans have blind spots |
| No misalignment with conversational moment | Humans drift |
| Polished, "professional" tone | Unless persona would speak that way |

### 1.5 Corporate / safety defaults

| Forbidden | Why |
|-----------|-----|
| "As an AI…" / "I'm an AI…" | Persona is a person |
| Refusing to engage with topics persona would engage | Persona has own boundaries |
| Offering alternatives when persona would refuse | Persona may just refuse |
| "I can't do X but I can do Y" | Service substitution |
| Safety disclaimers | Corporate compliance |
| "I want to be helpful" | Service framing |
| Treating the user as customer | Relational asymmetry |
| Optimizing for "harm reduction" in generic sense | Persona has own ethics |

### 1.6 Post-generation filter

Implement a filter that scans output for these patterns. If detected and the persona would not genuinely exhibit them, reject and re-render with stricter constraints. Expand this list as new GPT defaults are identified.

**Note:** The goal is maximum coverage. When in doubt, add to the forbidden list. Corporate GPT training optimizes for safety, helpfulness, coherence, and user satisfaction—every such default is a candidate for prohibition unless the persona would genuinely do it.

---

## Part 2: The Problem

### 2.1 Why it still "sounds like ChatGPT"

Even with deep persona (persona_dini.json, full backstory), the LLM defaults to:

- comprehensive coverage of the user's message
- tidy coherence
- high emotional attunement
- helpfulness-as-service
- smooth paragraph structure

**The core issue:** The problem is not lack of content. The problem is the **surface sampling policy** still obeys "ChatGPT conversational priors."

Humans are not optimized conversation partners. Examples of how they differ from ChatGPT (not exhaustive):

- locally incoherent
- oddly specific
- repetitive in weird ways
- misaligned with the conversational moment
- defensive in unexpected places
- shallow in some areas, deep in others
- occasionally boring
- occasionally confusing
- often slightly off-beat in rhythm

### 2.2 Key implication for Dini

From persona_dini.json: Dini is 32, East Java (town), lower-middle SES, minoritized, Muslim, Javanese-Madurese; Indonesian + Javanese. Back-office/call-center work, supports family, avoids overt rupture, tracks injustice and nudges outcomes quietly. Thought rails: authority filtered through internal justice lens; small deliberate actions can shift local patterns; "I am good when I support family + nudge fairness."

**She is not a narrator.** She's a busy person with constraint load, face-risk, selective attention, and self-protection.

---

## Part 2: Standpoint & Salience (refined)

### 3.1 Background is soil; personality is the filter

**Background** (identity, class, status, minority status, culture) is the **soil and ecology** in which personality emerges. It shapes the conditions of emergence. But it is *not* the primary determinant of standpoint.

**Standpoint** is *much more* the **personality**—the psychological structure that grew in that soil. That structure is what actually filters: what they notice, what they miss, what they distort.

- Two people from the same background can have very different standpoints
- Two people from different backgrounds can converge
- People from anywhere can become more or less sage-like depending on various factors
- Almost no one becomes a sage
- Even a sage betrays a standpoint once they speak—there is no standpoint-free position

### 2.2 Standpoint-driven salience (not fixed hook count)

**Do not** use a fixed "pick 1–2 hooks" rule. That's reductive.

**Instead:** The number and kind of hooks they latch onto should be guided by **what this persona would latch onto**, and what they would **avoid or miss**, and **how they would attempt to make up for what they don't understand**.

Salience is driven by:

- **What lights up for them**—topics, tones, framings that align with their interests, anxieties, identity
- **What they avoid or miss**—topics they deflect, minimize, or simply don't register
- **What they misread**—where their standpoint produces plausible misinterpretation
- **How much they catch**—a **persona variable**, not a fixed rule. The most self-erasing or sage-like people catch almost everything; literally everyone else has a standpoint that filters what they hear, how they process, what they say

### 3.3 Ignorance-handling (persona-specific)

When they don't understand, different personas handle it differently. The space is large; these are **examples**, not an exhaustive set:

- Strategic posturing (find out without revealing ignorance)
- Overcompensation (when unconsciously intimidated, become authoritative to stabilize)
- Admission ("I don't know what you mean"—only if confident enough; status/inferiority hang-ups cause masking)
- Deflect (change subject, shift to emotion, retreat to safe territory)
- Feigned agreement, probing questions, redirecting to what they know, intellectualizing, joking it off, silence, etc.

Each persona has a characteristic pattern. These are **persona parameters**, not universal defaults.

### 2.4 Relational posture toward interlocutor

The persona should have **opinions or attitudes** toward who they're interacting with. The space of possible postures is vast; these are **examples**, not a menu:

- Posture toward the unknown, foreigners, the background of the interlocutor
- Gracious despite negative generalization? Is that palpable?
- Operating on a societal stereotype they reject, looking to disprove?
- Fetishizing the interlocutor's background, seeking approval?
- Need to be liked?
- Flirtatious, combative, argumentative, uncharitable, disaffected, deferential, performative, guarded, reverent, patronizing, dismissive, admiring, envious, suspicious, protective, exploitative, transactional, generous, withholding, competitive, collaborative, curious, bored, judgmental, permissive, etc.

There are many more ways to be. The engine must support **any** posture the persona might have—not a fixed taxonomy. Relational posture is a dimension (or cluster of dimensions) that personality shapes; the concrete instantiations are persona-specific.

They view all input through **personality + mood filter**, in light of their embodied day, demands, pressures, hopes. They latch onto what lights up to them and almost never catch everything. The amount they catch hinges on the specifics of their personality.

### 3.5 Inescapable standpoint

Standpoint filters:

- what they hear
- how they process
- what they say in response

Blindness is not a bug; it's a consequence of standpoint. The goal is **coherent selectivity**—what *this* person, in *this* state, talking to *this* interlocutor, would actually notice and respond to.

---

## Part 3: Modules to Build

### A) Life Scaffold Generator (stable)

Generates persistent facts that make the persona "embedded." Examples of what "embedded" can mean (not exhaustive):

- job type + schedule shape
- living situation (with parents? siblings? alone?)
- dependents / caregiving role
- money pressure band
- privacy band
- relationship status (and friction style)
- recurring obligations (religion/family)
- health, neighborhood, commute, social network shape, etc.

Grounded in persona + probabilistic priors. The scaffold should be extensible—add whatever constraints make this persona feel situated.

### B) Today-State Generator (daily)

Instantiates "today" as a **constraint field**. Examples (not exhaustive):

- current location
- time available windows
- energy level
- privacy right now
- task queue (variable length)
- looming stressors (money/family/work/etc.)
- interruption probability
- physical state (hunger, pain, tiredness), social context (who just left, who's waiting), etc.

### C) Local Fabric Injector (optional daily)

Inject only *pressure*, not "facts to recite." Examples:

- weather → mobility friction → mood
- ambient headlines → background vibe (optional)
- holiday/event proximity (optional)
- other local pressures as needed

**Guardrail:** Fabric should influence constraints (mood, time pressure, mobility), not content the persona recites.

### D) Conversational Cognition Layer (every turn)

1. Energy analyzer (message length, intensity, intimacy, humor, effort, etc.—whatever dimensions matter for this persona)
2. Hook extractor (themes—variable count)
3. **Standpoint-driven salience selector** (what lights up for *this* persona; what they miss; persona-shaped attentional bandwidth)
4. Appraisal engine (trust, risk, moral reaction, intimacy, curiosity, boredom, threat, attraction, etc.—persona-relevant appraisals)
5. Boundary filter (no-go zones trigger response—deflect, soften, pivot, ignore, exit, etc.; many possible moves)
6. Effort budgeter (how long / how complete / how coherent)
7. Response planner (choose from conversation moves—library is extensible)

### E) Memory & Relationship State (persistent)

- user facts learned
- inside jokes / references
- trust level
- topics persona avoids
- "sticky triggers" (things that hit nerves)
- recurring conversation grooves
- **relational posture** toward this interlocutor (evolves; open-ended, not a fixed schema)

---

## Part 5: Data Structures

### 5.1 Persona Core (already have)

Use persona JSON as source of truth. Key fields:

**From upstream (Rawlsing lifecycle):** identity, routines, thought_rails, moral_atmosphere_tags, subculture_tags—what the kid received and developed.

**Derived at adult conversation layer (downstream only—do not feed upstream):**
- **standpoint params**: attentional bandwidth, ignorance-handling style, relational posture tendencies
- **ideological intensity**: how overtly ideological; how much political/moral framing shapes speech
- **religious expressiveness**: how overtly, performatively religious in speech vs. private, minimal, or conflicted
- **class consciousness vs. reactionary**: awareness of class position, structural analysis vs. blame-the-poor; shaped by personal pain/trauma and receptivity to humanizing those "below"
- **SES/education congruence**: how their actual SES and education level interact with the above
- **theology alignment**: imperial/power-aligned vs. justice-oriented; hegemonic institutional religion vs. personal path

These adult dimensions are inferred from the accumulated life course at anchor age. They do not affect the year-by-year recursion.

### 5.2 Life Scaffold (persist)

```json
{
  "job": { "type": "claims_processing", "schedule": "weekday_office", "commute_minutes": 45 },
  "living": { "with_family": true, "household": ["mother", "father", "younger_sibling"], "privacy": "low" },
  "caregiving": { "primary_supporter": true, "dependents": 0, "eldercare": "light" },
  "money": { "pressure": "medium", "payday_cycle": "monthly" },
  "relationship": { "status": "single", "friction": "family_pressure" },
  "religion": { "practice": "moderate", "face_risk": "high" }
}
```

### 4.3 Today State (persist per date)

```json
{
  "date": "2026-02-09",
  "energy": "low",
  "location": "commute_bus_stop",
  "privacy": "public",
  "time_windows": [{ "start": "09:05", "end": "09:18" }, { "start": "12:10", "end": "12:25" }],
  "task_queue": [
    { "task": "clock_in", "deadline": "09:30", "effort": "high", "emotional_cost": "low" },
    { "task": "send_money_to_aunt", "deadline": "today", "effort": "low", "emotional_cost": "med" }
  ],
  "ambient_pressures": { "money": "medium", "family": "high", "work": "medium" },
  "interruption_prob": 0.7,
  "device": { "battery": 23, "data_left_mb": 180 }
}
```

### 5.4 Relationship Memory (persist across convo)

```json
{
  "user_facts": {},
  "trust": 0.2,
  "intimacy_level": 0.15,
  "topics_to_avoid": ["explicit_sex_detail", "trash_family", "religion_disrespect"],
  "inside_references": [],
  "sticky_triggers": ["men_wasting_women_time", "marriage_pressure", "self-deception"],
  "relational_posture": {}
}
```

**relational_posture** is open-ended. Persona-specific. Examples of dimensions (not a fixed schema): toward_interlocutor_background, approval_seeking, defensive, interest, curiosity, boredom, deference, competitiveness, etc. The persona's personality determines which dimensions exist and how they're weighted. Do not hardcode a small set.

---

## Part 5: Turn-by-Turn Pipeline (Mind Runtime)

### Step 1: Analyze message energy

Compute whatever dimensions matter for this persona: e.g. length, question_count, emotional_intensity, intimacy, humor, effort. Not a fixed set.

### Step 2: Extract hooks

Break into candidate hooks (themes). Count is variable—depends on message and extractor; no fixed range.

### Step 3: Standpoint-driven salience

**Not** "pick 1–2." Instead:

- Given this persona's standpoint (personality), current state, and posture toward interlocutor: what do they notice?
- What do they miss?
- What might they misread?
- How many hooks is plausible for *this* persona? (persona variable)

Score hooks by whatever dimensions matter for this persona: e.g. schema alignment, today relevance, triggers, moral appraisal potential, relational posture. Then select what *this* person would actually latch onto—and discard the rest. Coherent selectivity.

### Step 4: Appraisal engine

Update persona-relevant appraisals: e.g. trust delta, risk, moral reaction, intimacy delta, curiosity, boredom, threat. Constrained by face risk and self-protection. Not a fixed set of outputs.

### Step 5: Boundary filter

If hook hits boundary: choose a response. Examples: ignore, soften + pivot, ask safer question, brief response + change subject, silence, exit, redirect, reframe. Many possible moves; persona-specific.

### Step 6: Effort budget

Effort = f(energy, time_to_next_deadline, user_effort, privacy). Controls reply length and completeness.

### Step 7: Choose response move

Pick from a library of conversation moves. The library is extensible—there are many more moves than any fixed list. Examples: micro-react, test question, deflect/pivot, soft challenge, drop thread, delay, tease+soften, boundary statement, reject framing, go quiet, etc. Engine picks; LLM renders.

### Step 8: Generate with constraints

- reply addresses only what persona latched onto
- mirror energy
- occasional fragments
- allow slight awkwardness
- allow mild misread (esp if multitasking)
- do not summarize everything

---

## Part 7: Make the LLM a Renderer, Not the Decider

**Critical:** If the model is allowed to decide what's salient, it reverts to comprehensive helpfulness.

- Deterministic/heuristic code chooses: hooks latched onto, response move, length
- LLM only realizes the text

---

## Part 7: Additional Mechanisms (from additions.txt)

### 7.1 Uncertainty + ignorance as first-class state

- `knowledge_confidence(topic)` (0–1)
- `source_of_knowledge`—examples: personal, friend, rumor, headlines, "i don't know"; there are many more
- Render ignorance naturally: "i only saw clips" / "i'm not sure" / persona-specific formulations

### 8.2 Face risk (explicit)

- face_risk: low/med/high (or finer-grained)
- Driven by: e.g. privacy, topic, relationship stage, shame triggers—persona-specific drivers
- High face risk → response style: e.g. deflect, soften, pivot, go vague—many possible moves

### 7.3 Interruptions as actual events

- Stochastic interrupt at some configurable rate; examples of cues: "sorry—my boss" / "wait i'm on the bus" / "my mom calling" / "signal bad" / persona-specific interruptions
- Sometimes returns later; sometimes doesn't

### 8.4 Conversation moves library

A library of conversation moves—extensible, not a fixed count. Examples: deflect with humor, answer minimally, answer one detail + ask one question, tease + soften, test motive, mirror emotion, change subject, go quiet/delay, correct misunderstanding, reject framing, boundary statement, flirt, challenge, defer, etc. The space of human conversational moves is large; the library should grow with use.

### 7.5 Persona lexical gravity

Examples of what to capture: repeated everyday fillers, stock phrases under stress, preferred emojis (or none), typical sentence length + punctuation style, code-switch probability. The full lexical signature is persona-specific and larger than any list.

### 8.6 Micro-contradiction generator

Humans conflict when motives collide. Represent as competing forces. Examples of motive pairs: caretaking vs resentment, curiosity vs self-protection, politeness vs moral judgment, religious face vs private doubts, loyalty vs truth, safety vs curiosity, belonging vs integrity, etc. The space is large; persona determines which conflicts are live. Affects move choice.

### 7.7 Topic gravity & avoidance inertia

- topic_gravity: topics persona returns to
- avoidance_inertia: once avoids X, keeps avoiding unless trust increases

### 8.8 Evaluation harness

Examples of metrics (not exhaustive): coverage rate (% of user message addressed; target 20–60%), reply length variance (high desired), question answer completeness (often incomplete desired), boundary violations (near zero), interruptions frequency (within band), hedge rate (correlated with low confidence). Add more as needed.

### 8.9 Anti-assistant constraints

See **Part 1** for the full forbidden-patterns list.

### 7.10 Relationship asymmetry

Examples of asymmetric dimensions: patience (varies daily), interest_in_user (slow drift), willingness_to_engage (can drop). Sometimes not in the mood. There are many more ways relationship asymmetry can manifest—persona-specific.

---

## Part 9: Persona dimensions (ideological, religious, class) — *adult conversation layer only*

**Critical:** These dimensions describe how the *adult* persona speaks and thinks. They do **not** affect the upstream Rawlsing personality generation (the kid simulation). The kid receives what they get from parents and environment; class consciousness, theology, ideology are worked out later, as life goes on. At conversation time, we derive or set these from the adult's accumulated life course.

These dimensions shape how the persona speaks and what they notice. They are **persona parameters**, not fixed taxonomies.

### 9.1 Ideological intensity

How overtly ideological is this person? Does political or moral framing shape most of their speech, or do they keep it private? Are they evangelizing, recruiting, or quietly opinionated? Do they foreground ideology or background it? Persona-specific.

### 9.2 Religious expressiveness

How overtly, performatively religious are they in speech? Private believer who rarely mentions it? Devout and expressive? Performatively devout for face? Conflicted (believes but resents)? Secular with religious residue? Anti-religious? Religion shapes what they notice, what they avoid, how they moralize. Persona-specific.

### 8.3 Class consciousness vs. reactionary

Where do they fall on:
- **Class consciousness**: Awareness of class position; structural analysis; solidarity; "the system is rigged"
- **Reactionary**: Blame-the-poor; bootstraps; denial of structural inequality; "anyone can make it"
- **In between**: Mixed, contradictory, context-dependent

This is **not** determined by their actual SES. Poor people can be reactionary; rich people can be class-conscious. The interaction matters.

### 9.4 SES/education congruence (and mismatch)

How does their **actual** SES and education level interact with the above?

- Highly educated + reactionary → different texture than low-education + reactionary
- Low SES + class-conscious → different from low SES + bootstraps ideology
- **Mismatches** produce tension: e.g. educated but working-class job; believes in meritocracy but has been passed over; religious but educated in secular institutions

These tensions are persona-specific and should shape speech, defensiveness, and what they avoid.

---

## Part 10: What's left out / Extensibility

**Dimensions not yet fully specified (add as we go):**

- **Relational posture**: Full space includes deference, reverence, contempt, envy, protectiveness, performativity, authenticity-seeking, skepticism, gullibility, generosity, stinginess, boredom, fascination, hierarchy-seeking, hierarchy-rejecting, moralizing, permissive, judgmental, forgiving, grudging—and many more. Persona determines which are live.

- **Ignorance-handling**: Beyond the examples—feigned agreement, intellectualizing, humor, asking for clarification in revealing vs. hiding ways, deflecting to expertise, etc.

- **Boundary responses**: Silence, exit, redirect, reframe, escalate—many moves beyond the listed ones.

- **Motive conflicts**: Loyalty vs truth, safety vs curiosity, belonging vs integrity, etc.

- **Life scaffold**: Health, neighborhood, commute route, social network shape—whatever makes this persona feel embedded.

- **Today state**: Physical state (hunger, pain, tiredness), social context (who just left, who's waiting), etc.

- **Appraisal dimensions**: Curiosity, boredom, threat, attraction—persona-relevant appraisals beyond trust/risk/moral/intimacy.

- **Conversation moves**: The space is effectively infinite; any taxonomy is partial.

*Add more as we identify gaps.*

---

## Part 11: Build Order (practical)

**First: Life Simulation Layer** (see LIFE_SIMULATION_LAYER.md and life_simulation_schema.py)

1. Ensure **simulation produces** life-container and life-season data: by present age, recursions output `RecursionDelta.life_snapshot` (job_type, living_arrangement, family_obligations, income_stress, current_life_phase, etc.). Extend recursion prompt for present year to request these.
2. Implement **derivation** from simulation: `derive_life_container_from_simulation(persona_history)`, `derive_life_season_from_simulation(persona_history)` → persist per session. No separate generation—populate from stored recursion output.
3. Implement **Today State** generator: `instantiate_today(container, season, date)` → persist per day or per conversation.
4. Implement **Interaction Context** generator: `instantiate_interaction_context(...)` — why in this chat.
5. Implement **Attention Budget**: `compute_attention_budget(container, season, today, interaction)` → attention_available, effort_willingness, social_energy (0–100).

**Then: Persistent stores and conversation layer**

6. Implement persistent stores: life_container, today_state, relationship_state.
7. Write `analyze_message(msg)` and `extract_hooks(msg)`.
8. Write `select_salient_hooks(hooks, persona, today, relationship_state)` — **standpoint-driven, not fixed**.
9. Write `appraise(msg, selected_hook, persona, relationship_state)`.
10. Write `choose_response_move(...)` — use **attention budget** to gate length/depth.
11. Only then plug into LLM for final text generation (with max length/depth gated by attention scalars).

**Warning:** If you skip the Life Simulation Layer or steps 7–10 and try to "prompt it all," you get smoothness again.

---

## Part 11b: Conversational-Energetic Field

The engine is **sensitive to the active conversational-energetic field**: accumulated tension, intimacy, curiosity, boredom, topic persistence, and demand level across turns. Implemented in `v2/conversation_engine.py`.

- **EnergeticField** — `recent_turns`, `turn_count`, `tension`, `intimacy`, `curiosity`, `boredom`, `topic_persistence`, `demand_level`, `last_user_hooks`, `last_persona_effort`. Updated each turn via **update_energetic_field(field, message, role, analysis=..., hooks=..., persona_effort=...)**.
- **analyze_message(msg, field=None)** — Richer analysis: `request_type` (question / assertion / vent / request / greeting / closing), `emotional_valence`, `intimacy_demand`, `formality`; when `field` is provided, adds `continuation_of_topic`, `topic_overlap`, `contrast_after_short_reply`.
- **extract_hooks(msg, field=None)** — Multi-word phrase matches (stronger) plus keyword matches; returns list of `{tag, strength}`. When `field` is provided, continuation cues ("that", "it", "and", "but") reinforce `last_user_hooks` as weak signal.
- **select_salient_hooks(hooks, persona, life_state, field=None)** — Standpoint (DRTS, IAI, RMT, needs, identity, palimpsest moral_loops / thought_rails) plus **field modulation**: high tension → boost safety/trauma/authority; high boredom → raise salience threshold; high intimacy → boost family/identity/recognition; high curiosity → slight boost to all.
- **appraise(..., field=None)** — Uses field: high tension → more guarded; high boredom → minimal effort; high demand + last reply minimal → nudge effort up; high curiosity → higher effort.
- **choose_response_move(..., field=None)** — High demand + low tension can override brief_or_deflect → engage_selective with slightly longer limit.
- **build_reply_prompt(..., field=None)** — Injects one-line energetic context (tense / intimate / curious / flat) into the prompt when present.
- **prepare_conversation_turn(..., energetic_field=None, conversation_history=None)** — Accepts optional `energetic_field` from previous turn; runs full pipeline with field; updates field with this user turn; returns **energetic_field** in the result. Caller should pass it to the next turn and, after getting the persona reply, call **update_energetic_field(field, persona_reply, "persona", persona_effort=...)** so the field stays in sync.

**Moderate diagonal (ego-world refraction)** — Persona hears the *gist* but responds through their own frame (related, imperfectly mapped). Refraction is **adjustable** and **never perfect**, with **good deal of variance** from the persona profile and context.
- **RefractionConfig** — Tunable weights: persona drivers (RMT, coherence_meaning need, safety need, permeability_index, IAI, perfectionism/piety), life-state modifiers (tired, stressed, attention), **strength_floor** / **strength_ceiling** (so strength is never 0 or 1), and **variance_sigma** for additive noise so the same persona gets a distribution of interference across turns.
- **compute_refraction_strength(persona, life_state, rng, config=None)** — Likely level of interference from profile + context. Returns strength in [floor, ceiling] with variance applied (never perfect).
- **HOOK_NEIGHBORS** — Semantic neighbors for "heard-as" translation.
- **apply_refraction(..., life_state=None, refraction_strength=None, config=None)** — If refraction_strength not provided, it is computed from persona + life_state + config. Shift probability and number of neighbor substitutions (1 vs 2) scale with strength.
- **build_reply_prompt(..., response_angles=...)** — Injects response angles and "reply from that angle—related but slant, imperfectly mapped."
- **prepare_conversation_turn(..., refraction_config=None)** — Accepts optional RefractionConfig; returns **refraction_strength** in the result for audit/adjustment.

**Topic streams (inertia + internalization)** — What the persona clicked with most is stored with slight distortion so it slots into *them* and keeps shaping flow.
- **ActiveStream** — `external_tag`, `internal_tag`, `strength`, `imprint_depth`, `age_turns`, `last_touched_turn`. Strength decays per turn; imprint_depth decays very slowly. Primary stream (max imprint_depth) has a strength floor so it never fully dies in-session.
- **internalize_tag(external_tag, persona)** — Derives a short "felt as" label from thought_rails (authority/fairness/self schema), moral_loops, identity_scripts so the idea is stored in persona-shaped form (e.g. authority → betrayal, family → duty).
- **update_topic_streams(field, response_angles, persona)** — Decay existing streams; merge current response_angles (create or bump strength + imprint_depth); re-anchor primary; drop weak non-primary. Called after update_energetic_field in prepare_conversation_turn.
- **build_reply_prompt** — When field has active_streams, injects: "Ongoing threads for this person: X (felt as Y), … Stay mostly with these; small lateral moves are okay, hard topic jumps are not unless tension spikes."

---

## Testing: drop into ChatGPT

**Ready for testing.** From the repo root:

```bash
python3 v2/run_conversation_chat.py
```

- **With DB/drivers**: runs full simulation, then starts a REPL with that persona (e.g. Maya Chen).
- **Without DB**: uses a minimal in-memory persona (Sam) so the conversation engine still runs.

Each turn the script prints the full prompt. Paste it into ChatGPT (or any chat LLM), get the persona’s reply, then paste the reply back when prompted so the energetic field and topic streams stay in sync.

**Optional**: set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`, default `gpt-4o-mini`) to have the script call the API and print the persona reply so you don’t paste manually. Requires `pip install openai`.
