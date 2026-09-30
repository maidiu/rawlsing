# Sorok — PFF/SDTF Lineage Correction, Learned-World Prior, and Two-Call Per-Actor Live Pipeline R1

Status: PROVISIONAL_PRODUCT_ARCHITECTURE_DEMAND__CORRECTS_OLDER_V3_ANCHORING

Date: 2026-09-30

## 0. Lineage correction

Do not describe current Sorok live-interactional work as merely extending the older accepted V3/V2 architecture.

The closer immediate ancestor is the later PFF/SDTF-era theorization.

Recovered PFF interaction-side work already establishes:
- one durable generated person rather than a second interaction psychology;
- actual user interaction occurrence + discourse/pragmatic evidence + session context;
- CAN-008 person×event uptake/appraisal/recruitment/metabolism;
- only minimal non-durable fast interaction carryover;
- durable effects proposed back to exact V3 owners;
- V2 surface realization downstream;
- emitted output becomes a possible next actor-facing event;
- user opacity and actor-specific interpretation.

Recovered SDTF work from the same period separately develops objective world-rule / world-population / structural→developmental transduction constraints.

Therefore Sorok's current move is:

`OLDER V3/V2`
→ `PFF/SDTF-ERA LIVE PERSON×EVENT + OBJECTIVE WORLD TRANSDUCTION`
→ `SOROK LIVE WORLD-FLESH RECURSION / PRODUCT INTERACTION`.

Sorok is a further development from the PFF/SDTF-era layer, not the invention of that layer.

---

## 1. Two kinds of world knowledge

Separate:

### A. PRESENT EXTERNAL FACT
Facts that must actually track the historical present:
- current public event;
- current law/rule;
- current weather/disaster;
- current named institution change;
- current transport disruption;
- current conflict/economic shock;
- current public schedule/closure where material.

These require governed present-world ingress when used.

### B. LEARNED-WORLD PRIOR / COMMON-WORLD GENERALIZATION
Model-learned regularities such as:
- ordinary job pressures;
- plausible coworker distributions;
- common routines;
- likely sources of boredom/satisfaction/abrasion;
- social interactions typical of an occupation/institution class;
- ordinary household/practical patterns;
- local-context-conditioned social texture where the model has adequate learned knowledge.

These should normally come from the model's training-derived world model, not fresh search.

---

## 2. Learned-world prior is proposal authority only

The LLM's training-derived world model may propose plausible concrete flesh.

It is not objective current-fact authority.

Candidate conditioning:

`PERSONA COMPUTABLE STATE`
+ `GENERATED HISTORY`
+ `RELATIONSHIP STATE`
+ `PLACE / TIME / INSTITUTION TYPE`
+ `CURRENT ADMITTED WORLD FACTS`
+ `MODEL LEARNED-WORLD PRIOR`
→ `BOUNDED PARTICULAR CANDIDATES`.

Example:
A private-clinic desk receptionist role can be fleshed using model knowledge of:
- interruption frequency;
- appointment scheduling pressure;
- patient frustration;
- clinician/admin hierarchy;
- emotional labor;
- repetitive clerical work;
- insurance/payment friction where context supports it;
- coworker role ecology;
- possible satisfactions in competence/helpfulness/routine;
- possible boredom/status abrasion.

Which of those becomes causally important for Nadia is conditioned by Nadia's generated personhood and actual events.

Do not web-search merely to narrate generic occupational texture.

---

## 3. Context binding

The learned-world prior should be sharply context-bound.

Strong context inputs may include:
- locality/country;
- historical date;
- occupation/institution class;
- economic/resource context;
- household structure;
- religion/community where already generated;
- role/status;
- known workplace particulars;
- actual current-world admitted facts.

The model may generalize only inside the allowed context envelope.

Unknown/current named facts remain unknown rather than being hallucinated from training data.

---

## 4. Every interacted-with person must be a person before response

Correction to the earlier actor-tier language:

The relevant boundary is not every person merely visible in a crowd.

It is every **synthetic person with whom the user or another active actor actually interacts consequentially**.

Before such a person generates a consequential response, Rawlsing must instantiate an independently owned actor state sufficient for:
- current history/context;
- perception;
- event-time uptake/appraisal;
- actor-specific response;
- memory/history return if the encounter matters.

Exact implementation may be a minimal V3 initialization/recursion or another governed equivalent.

But:

`INTERACTED PERSON != STATELESS NPC PROP`.

---

## 5. Close relations recursively shape Nadia too

Genealogy/relationship recursion is not merely:

`PARENTS → CHILD`.

After the child exists:

`NADIA ↔ CHILD`
`NADIA ↔ PARTNER/CO-PARENT`
`CHILD ↔ PARTNER/CO-PARENT`
`HOUSEHOLD ↔ EACH PERSON`

continue recursively through time.

The child develops through Nadia/household history; Nadia simultaneously develops through:
- caregiving burden;
- child's temperament/development;
- attachment/conflict;
- pride/fear/shame;
- school/institutional events;
- changed time/resources;
- partner/co-parent dynamics;
- child's changing agency.

A child must therefore be an independent causal person partly because **the child is one of the forces making Nadia become Nadia**.

---

## 6. Two-call per involved synthetic actor per turn

Current Sorok product requirement:

> **Every synthetic actor causally participating in a live interaction receives a two-LLM-call pass for that turn.**

This is semantic architecture, not a specific vendor commitment.

### Call A — analytic / person×event transduction

Candidate low-cost/high-throughput model (e.g. GPT Luna class or DeepSeek Flash class after benchmarking).

Consumes:
- exact actor computable slice;
- actor-accessible memory/knowledge;
- relationship state;
- perception packet;
- current event/user input;
- PFF fast state/session context;
- current world/task state.

Produces structured, non-user-visible candidate material:
- received meaning / uptake;
- appraisal;
- recruited needs/expectations/mediators/tensions;
- current response dynamics;
- possible action/response move;
- truth/withhold/lie/evasion posture where applicable;
- world-flesh slots that require realization;
- durable-effect proposals.

Code/rule authority validates/adopts what is allowed.

### Call B — flesh / voice / phenomenal realization

Candidate Claude-class model selected specifically for stylistic control, voice fidelity, natural prose and erasure of generic LLM voice.

Consumes only admitted/authorized actor/world state plus bounded unresolved flesh slots.

Produces:
- concrete phenomenal detail;
- actor action/expression;
- dialogue/voice;
- narrator-visible world flesh;
- structured sidecar for any newly proposed concrete particulars.

No output is emitted until required sidecar validation/admission passes.

Actual emitted output then becomes a possible next event.

---

## 7. Baseline call count

If one synthetic actor is actively involved:
`2 LLM calls / user turn`.

If Nadia + child are both actively participating:
`4 calls / user turn`.

If Nadia + child + coworker:
`6 calls / user turn`.

Actors merely visible but causally inactive require no live call.

This actor-count multiplier must be treated as a first-class cost/latency variable.

---

## 8. Physical batching may not collapse actor separation

Providers may support batch/concurrent invocation.

Rawlsing may parallelize actor Call-A passes where causal ordering allows.

But semantic state remains actor-specific.

Do not save cost by asking one model call to synthesize a single shared subjective response for multiple persons.

`BATCHED EXECUTION != MERGED PSYCHE`.

---

## 9. Call-B flesh admission issue

Because the flesh/voice model may introduce concrete particulars, its output must carry machine-readable candidate particulars alongside prose.

Nominal two-call path:
1. Call A + code admission establishes response envelope;
2. Call B returns text + structured particular sidecar;
3. deterministic/rule validation checks sidecar before user-visible emission;
4. valid particulars become generated history/world facts;
5. output is emitted;
6. occurrence returns into actor/world computation.

Malformed/out-of-authority outputs may require repair/retry, but repair is exceptional and should be measured separately from baseline two-call semantics.

---

## 10. Current model-market note

As of 2026-09-30:
- DeepSeek's current low-cost Flash endpoint is V4.1-Flash (`deepseek-flash`), with legacy V4-Flash names temporarily routing to it;
- Anthropic's current Sonnet 5.5 is positioned as the lower-cost/faster complement to Opus 5.5 and is available at $2/M input and $10/M output tokens, with prompt-caching support;
- Claude Haiku 5.5 has been announced but is not yet generally released.

Therefore the exact Call-A/Call-B vendor choices should be benchmarked, not frozen from naming assumptions.

---

## 11. Product theorem

> **Rawlsing's live person is not generated by prose. A causally owned person enters an event, is transduced through a structured actor-specific pass, and only then receives flesh and voice.**

And:

> **The model's knowledge of ordinary human worlds is useful as a constrained generative prior precisely because it is downstream of the person computation, not a substitute for it.**