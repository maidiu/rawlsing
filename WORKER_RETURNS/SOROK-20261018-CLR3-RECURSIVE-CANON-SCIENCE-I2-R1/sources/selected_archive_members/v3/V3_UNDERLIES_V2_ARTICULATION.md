# How v3 Underlies and Deepens v2 — Articulation

This doc pulls from **new_version.txt**, **spec.txt**, **specLLM.txt**, **PIPELINE_PLACE.md**, and **OVERVIEW_INTEGRATED.md** to state explicitly how v3 is supposed to relate to v2 and where the current implementation diverges.

---

## 1. Intended architecture (from the docs)

### Two-layer split

- **Layer A — Backbone (v3):** The causal physics. Updates the person each year: constraints, capacity, buffers, cracks, alienation, domains, collective_infrastructure, practice_stack, peak_routing (loop_topology, solidarity_boundary, harm_constraint, etc.). Produces **state changes**.
- **Layer B — Phenomenology (v2):** The rich persona layer. **Renders** the person **from** backbone state: needs, strategies, symbols, narrative voice, Enneagram patterns, beliefs. Produces **expression**, not causality.

**Quote (OVERVIEW_INTEGRATED §2):**  
"v2 is not replaced. v3 is the **engine underneath it**. The LLM renders phenomenology from backbone state; it may propose candidate deltas but must not apply them."

So: **Backbone (v3)** does causal state updates each year; **Phenomenology (v2)** renders the person (needs, strategies, voice, beliefs) **from that state**. The v2 “surface” is not a separate simulation; it is **derived from** v3 state.

### Spine comparison (new_version.txt)

- **v2 spine:** `world_slice → driver_vector → needs → strategies → indices → persona`
- **v3 spine:** `world_slice → strata stack → frameworks → domain matrix (A/S/V/Aim) → alienation vector → [optional] micro-psych regulation`

v3 is a **different causal graph**. Needs/strategies are not the driver; structure (strata, frameworks, domains, capacity) is. So when v3 “underlies” v2:

1. **Identity** (who the person is: country, region, place, ethnicity, religion, language) comes from the **identity pipeline** (v2: parents, EPR, people_groups). That pipeline is the source of truth for “who”; v3 does not invent identity.
2. **Dynamics** are v3 only: strata, frameworks, domains, capacity, events, deltas. v3 is the single source of truth for what happens each year.
3. **Phenomenology** (needs, strategies, indices, voice) should be **derived from** v3 state — i.e. an explicit derivation layer that turns backbone (capacity, frameworks, domains, cracks, peak_routing, etc.) into the v2-compatible surface, not a separate year-loop that “also” runs.

### Phase 4 micro layer (new_version.txt)

"Decide whether: to port needs/strategies from v2, **or treat micro-psych as derived from frameworks**. This decision should come last."

So the spec explicitly allows (and leans toward) **micro-psych (needs/strategies) as derived from the backbone**, not as a parallel v2 sim.

---

## 2. Identity: parents → child; religion can change later

Identity fields (religion, ethnicity, language) are **not** “fill with country default when Unknown.” They are:

- **Sourced from the identity pipeline:** parents-first → household ethnicity, religion, language (from EPR/people_groups / country defaults when data is thin). The child **inherits** those; the pipeline must ensure the household (and thus the child) always gets concrete values from that pipeline, not “Unknown” as a valid output.
- **Life-course changes:** e.g. religion can change later in life (conversion, deconversion); that would be an event/state change in the backbone or a tracked identity update, not “we never had a religion to start with.”

So the fix is: **ensure the identity pipeline (and any v2→v3 handoff) always populates religion, ethnicity, and language from the real source (parents/household, with country fallbacks only when the pipeline truly has no data).** Never treat “Unknown” as acceptable for a shipped persona; if the pipeline can’t determine a value, it should use a country-level default at the **pipeline** stage so the child is never created with Unknown. The persona sheet then reflects what the pipeline produced (and any later-life changes if we model them).

---

## 3. Why the current setup feels wrong

Today:

- We run the **v3 year loop** (code-sampled events, no Pass 1 LLM) and get backbone state.
- We then **map** backbone → needs/strategies/indices in `build_persona_sheet` with **thin formulas** (capacity, practice_stack, style_traits → needs/strategies). Many backbone dimensions stay at default (0 or 50) because only code events touch them, so the derived surface is mostly 50s and 0s.

That is **not** the intended “v3 underlies v2”:

- **Intended:** v3 is the causal spine; phenomenology (needs, strategies, voice) is **derived from** that spine via a proper derivation (and/or LLM render from state). So either:
  - **Derivation path:** A defined module derives needs, strategies, indices, thought_rails from backbone (capacity, frameworks, domains, cracks, peak_routing, practice_stack, etc.) with explicit, documentable rules so the surface reflects the backbone; or
  - **LLM render path:** The LLM is given backbone state (and selected events/deltas) and produces narrative + phenomenology consistent with that state (specLLM Pass 2, “render from state”).
- **Not intended:** Running v3 as a separate “engine” and then applying a minimal stub map so that the surface is flat whenever the backbone is underpopulated. The “underlying” relation means the surface **comes from** the backbone in a substantive way.

So the gap is: we have the backbone and a stub map, but we do **not** yet have either (a) a full **derivation** from backbone → needs/strategies/indices that uses the full ontology (frameworks, domains, cracks, loop_topology, solidarity_boundary, etc.), or (b) the full **Propose → Score → Apply → Render** loop (Pass 1 + scoring + deltas + Pass 2) so that backbone and narrative/phenomenology are aligned and the surface is rich.

---

## 4. Per-year recursion: structure first, then v2 on top; two LLM calls per recursion

The intended flow is **not** “v3 runs 43 years, then derive surface once.” It is:

- **Each recursion (each year):**
  1. **v3 runs:** structure/causal update (field, events, capacity, domains, cracks, peak_routing, etc.).
  2. **First LLM call (Pass 1 — “on v3”):** LLM proposes **candidates** (events, magnets, framing shifts) given current state summary. Code **scores and selects** (0–2 major, 1–3 minor, optional surprise), then **applies bounded deltas** to backbone. So the backbone is updated using LLM-proposed candidates, but code controls selection and deltas.
  3. **v2 runs on top:** phenomenology derived from the **updated** backbone (needs, strategies, voice from structure).
  4. **Second LLM call (Pass 2 — “on v2”):** LLM **renders** narrative/phenomenology from the updated state (selected events + applied deltas + state summary) → narrative_snapshot, dialogue_snippets, consistency_check. No backbone mutation; render only.
  5. The **product** of that step (updated backbone + derived phenomenology + Pass 2 narrative) is the state the **next** recursion pushes off of.

So: **two LLM calls per recursion** — one for v3 (propose candidates → code score/apply → backbone update), one for v2 (render scene/person from that backbone). Structure first, then v2 and both LLM passes run together each time; next year pushes off that product. Spec: **specLLM.txt** (Propose → Score → Apply → Render); **v3/engine/llm_contract.py** (Pass 1 CandidatePacket, Pass 2 RenderPacket/RenderOutput).

**When using band ages only:** The LLM is not *generating* the band age in isolation. It is **updating the gap that *ends* in the band age**. So the call at band age 12 gets context: "State at previous band (7) was X; state at *now* (12) is Y; code ran years 8–12 with these events. Propose/Render the *interval* 8→12 — the trajectory across the gap — with the band age (12) as the endpoint." So one (or two) LLM call(s) per band covers the *span* from the previous band to this one; you don't lose the in-between years, you summarize/narrate them as a chunk ending at the milestone.

---

## 5. Harmonizing into and deepening v2 — one sentence

**v3 is the causal spine; each year v3 runs, then v2 runs on top (phenomenology derived from backbone + LLM); the next year pushes off that combined product, with code and LLM interwoven every recursion.**

---

## 6. What to build next (from the docs)

- **Identity:** Ensure the identity pipeline (parents-first, EPR/people_groups, country defaults only when data is missing) always outputs concrete religion, ethnicity, language for the child; no persona shipped with “Unknown” for those; model religion change later in life if desired.
- **Backbone → phenomenology:** Each recursion: v3 step → **Pass 1 LLM** (propose candidates) → code score/apply → backbone update → derive v2 surface → **Pass 2 LLM** (render narrative). Wire the full **Pass 1 → Score → Apply → Pass 2** loop so that each year backbone is updated, then v2 derives/renders from it, and the next year pushes off that product. Two LLM calls per recursion; code and LLM interwoven.

---

## 7. Modality / project-scale (how to work when you can’t hold it all)

The project is large; no one can hold it all in their head. Suggestions so you (and any agent) can recover context quickly:

- **This doc as recursion/LLM canonical:** **V3_UNDERLIES_V2_ARTICULATION.md** = single place for “how v3 underlies v2,” “two LLM calls per recursion (Pass 1 on v3, Pass 2 on v2),” and “what’s missing.” Point Cursor (or yourself) here when you need the big picture.
- **One “current state” map:** Keep a short **CURRENT_STATE.md** (or a section in WHAT_RUNS_AND_ABSENT.md) that you update when you change wiring: “As of [date]: what runs (X), what’s stubbed (Y), what’s not wired (Z).” Then each session you can refresh from that instead of re-deriving.
- **Layer → file map:** One-pager that lists: identity pipeline → v2/identity_generator, create_persona_identity_from_parents; backbone step → v3/engine/yearly_step, run_one_year; Pass 1/2 → v3/engine/llm_contract, prompts, phenomenology.render_year; recursion driver → v2/run_full_simulation_with_llm_log (v3 backbone path). So “where does X live?” is one lookup.
- **Decision log:** When you lock a design choice (e.g. “2 LLM calls per recursion”), add one line to a **DECISIONS.md** or to this doc: “Two LLM calls per recursion: Pass 1 (candidates → v3), Pass 2 (render → v2). Source: specLLM.txt.” So later you can recover “why” without re-reading the spec.
- **Cursor rules:** Put the two-LLM-per-recursion flow and “v3 then v2 each year” in `.cursorrules` or a user rule so any agent sees it at the start of a session.
- **Chunk by concern:** Keep docs small and cross-linked (identity, step order, LLM contract, articulation) rather than one giant doc. This doc stays “recursion + how v3 underlies v2”; WHAT_RUNS_AND_ABSENT stays “what’s wired vs absent”; specLLM stays the full contract.
