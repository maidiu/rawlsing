# Sorok — Supporting-Actor Fidelity, Lazy Promotion, and Cost Envelope R1

Status: PROVISIONAL_PRODUCT_ARCHITECTURE_DEMAND__COST-SENSITIVE

Date: 2026-09-30

## 0. Problem

Rawlsing needs a socially populated world without requiring every person in every scene to run as a continuously active full V3+LLM agent.

The central cost question is not:

> How many people exist in the world?

It is:

> **How many actors currently require independent causal state, developmental history, perception, memory and consequential action?**

---

## 1. Do not equate existence with continuous agent execution

A crowd at a fair does not imply hundreds of continuously running LLM loops.

Most world population can exist through:
- structural/world population state;
- place/event attendance distributions;
- group/aggregate dynamics;
- bounded incidental actor generation.

LLM calls should occur at materialization, proposal, rendering or consequential-interaction boundaries—not continuously for every actor.

---

## 2. Candidate actor-fidelity tiers

### Tier 0 — population/background aggregate
No individual actor identity required.

Examples:
- fair crowd;
- commuters;
- customers in a shop;
- congregation/audience aggregate where no individual matters yet.

Owned as world/population context, not synthetic persons.

### Tier 1 — incidental scene actor
Stable enough for current scene continuity, but no assumption of a full continuously simulated life.

Minimum possible state:
- stable scene/local actor ref;
- current role/task;
- location;
- immediately relevant material constraints;
- perceptual access;
- bounded actor-local response state sufficient for current interaction;
- provenance/seed so repeated reference within the scene is stable.

If the user meaningfully engages the actor, materialize enough actor history/state **before** generating consequential response.

### Tier 2 — persistent supporting actor
Used when a person recurs and their independent actions can materially affect focal persona/world.

Needs:
- stable actor identity;
- compact generated historical anchors;
- current causal state;
- independent agenda;
- memory/knowledge state where needed;
- relationship refs;
- event ledger/history cursor;
- lawful future update.

Examples may include:
- recurring coworker;
- neighbor;
- teacher;
- friend;
- community member.

### Tier 3 — relationally formative actor
A person whose history and relationship with Nadia materially shape Nadia's development.

Needs substantial independent V3 history plus ongoing relationship recursion.

Likely examples:
- parent/co-parent;
- partner;
- child;
- household member;
- very close friend;
- long-running high-impact coworker/mentor/rival.

### Tier 4 — focal persona
Full target personhood generation + deep pre-user developmental history + live thin interaction projection.

---

## 3. Promotion law

Actor fidelity should be promoted when the claimed causal burden increases.

`OBSERVED BACKGROUND PERSON`
→ user/persona interaction begins
→ materialize enough actor state before response
→ actor becomes recurrent / consequential
→ persistent actor state/history
→ actor becomes developmentally formative
→ richer V3 history / relation recursion.

Promotion must preserve all already admitted facts/events.

`LAZY ACTOR COMPLETION != RETROACTIVE REWRITING`.

---

## 4. No retrocausal personality invention

If an incidental actor has already performed a consequential act, later promotion may not invent a past that would make that act impossible or silently reinterpret the old event.

Previously admitted:
- actions;
- utterances;
- observable traits;
- relationships;
- timestamps;
- material facts;

become constraints on later materialization.

Where deeper prior state is materialized later, it must be history-compatible and provenance-tagged as lazy completion.

---

## 5. The child case

A focal persona's child is unlikely to be safely representable as a mere incidental NPC if:
- the user can teach/help/hurt/influence the child;
- the child has memory and learning;
- the child affects Nadia's obligations/affect/development;
- the child independently initiates events;
- the child's changing relationship with Nadia matters.

Therefore the child should likely be at least a persistent/relationally formative actor.

Accepted V3 genealogy already supports:

`generated parents`
→ `relationship/household history`
→ `child generation`
→ `child's own initialization/development`.

Sorok should determine the minimum developmental resolution required for alpha—not whether the child is an independent person at all.

---

## 6. Parent/co-parent / partner back-projection

If Nadia's developmental history includes a partner/co-parent who materially shaped household/child/Nadia:

Do not generate that person merely as a descriptive spouse tag.

Candidate route:
- generate independent actor history to sufficient pre-relationship point;
- realize encounter/relationship under V3 rules;
- run bounded relationship/developmental recursion through relevant years;
- allow resulting shared history to shape Nadia, the other actor and the child.

The exact amount of recursion can be compressed/hybrid; it need not mean one expensive LLM call per actor-year.

---

## 7. Hybrid recursion rather than constant simulation

Accepted V3 already permits hybrid scheduling rather than sacred yearly ticks.

For product feasibility:
- long low-change intervals may be compressed;
- significant transitions/events receive higher resolution;
- dormant supporting actors need not be rendered;
- slow processes can update from code-side state;
- LLM proposal/render calls occur only when concrete particulars or natural-language expression are required.

Thus:

`DEVELOPMENTAL REALITY != CONTINUOUS LLM TOKEN BURN`.

---

## 8. Event-time concurrency

Several actors may be causally active in one scene without several free-running agents.

Possible orchestrated turn:
1. objective event/world update;
2. determine actor-specific perception packets;
3. code-side/current-state mediation;
4. bounded LLM render for actors who actually need expression;
5. admit resulting external interaction events;
6. update only affected actor/relation state.

Concurrency is an orchestration problem, not a requirement for permanent autonomous agent processes.

---

## 9. Cost-control principles

1. code owns causal state;
2. store compact structured state, not full prose re-prompts;
3. retrieve only relevant history slices;
4. exploit prompt caching for stable constitutional/profile material;
5. use lower-cost models for bounded candidate generation / routine rendering where validated;
6. reserve higher-capability models for ambiguous high-consequence scenes if needed;
7. batch/offline recomputation where latency is irrelevant;
8. do not render dormant actors;
9. do not continuously simulate inner monologue;
10. promote fidelity only when causal burden demands it.

---

## 10. World event ingestion cost

Present-coupling need not mean per-actor constant web research.

Candidate architecture:
- region/place/time event feed materialized at bounded cadence;
- canonical external-world event store;
- deduplicated relevance routing into affected local worlds;
- actor-specific exposure/admission only when causal paths exist.

One current event can therefore be fetched/admitted once and consumed by many synthetic lives without duplicative research calls.

---

## 11. Feasibility theorem

> **Rawlsing needs many represented people, fewer persistent causal actors, fewer still developmentally formative actors, and only a small number of actively rendered minds at any instant.**

This hierarchy is likely the difference between a feasible product and an uncontrolled multi-agent simulation bill.

---

## 12. Open proof required

Prototype must measure:
- LLM calls per active-user-hour;
- input/output tokens by call class;
- cache hit rate;
- actor promotions per hour/day;
- between-session recomputation cost;
- external-event ingestion cost;
- latency for 2/3/5 concurrently relevant actors;
- quality degradation when candidate/render work is moved to cheaper models.

Do not settle cost feasibility by intuition.