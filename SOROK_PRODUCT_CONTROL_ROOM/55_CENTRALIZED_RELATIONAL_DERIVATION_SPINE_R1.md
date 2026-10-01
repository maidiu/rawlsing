# Sorok — Centralized Relational Derivation Spine R1

Status: PROVISIONAL_PRODUCT_ARCHITECTURE_DIRECTION

Date: 2026-10-01

## 0. Correction

Artifacts 53–54 should not be read as requiring large parallel durable subsystems for "relational grammar" or "object-value grammar."

The stronger Rawlsing direction is:

> Rewrite V3 as a sufficiently relational, historically grounded causal person model that many specific questions of meaning can be derived from the same canonical spine with only thin domain adapters and bounded additional state where genuinely necessary.

Examples of questions that should become derivable rather than separately engineered:

- What does this object mean to this actor?
- What does sharing it with this particular other mean?
- What does entering this room mean with this counterpart?
- What does being fed / lending money / giving help / refusing help mean here?
- What does this ritual, place, project, practice, institution or possession signify in this relation?
- What does this actor expect another person of this role to understand without explanation?
- Why does the same act mean something different with another person?

## 1. Central law

Prefer:

CANONICAL RELATIONALLY CONSTITUTED V3 STATE
+ CANONICAL WORLD / TARGET HISTORY
+ SPECIFIC COUNTERPART / DYAD STATE
+ CURRENT EVENT / CONTEXT
-> DERIVED ACTOR-LOCAL RELATIONAL MEANING

over:

OBJECT MEANING ENGINE
+ HOSPITALITY ENGINE
+ MONEY MEANING ENGINE
+ PLACE MEANING ENGINE
+ RITUAL MEANING ENGINE
+ ...

Do not create new semantic owners merely because a product question can be phrased in a new noun domain.

## 2. What belongs in the canonical spine

The V3 rewrite should preferentially store/update causally durable material such as:

- relationally formed need / expectation organization;
- relation-class and role-conditioned priors;
- durable models of particular others;
- models of relationship and meta-perception where warranted;
- specific dyadic history and conventions;
- developmental histories of care, dependence, authority, recognition, conflict, absence and loss;
- strivings / investments / commitments and their support/cost histories;
- alienation / integration relations where governed;
- practices and recurring activity organization;
- material/security/dependency constraints;
- relational magnets / attachment-relevance to actual generated entities;
- memory, significance, rupture, metabolization and pattern evidence;
- self-model and accessibility organization;
- network and third-party relations;
- provenance-linked history of materially consequential encounters with objects, places, institutions, projects and practices.

The exact final field/schema decomposition remains architecture work.

## 3. General target relation, not object exceptionalism

Objects should be one kind of target in a more general actor-to-world relational field.

A generic target may be:
- person;
- object;
- place;
- project;
- role;
- practice;
- ritual;
- institution;
- group/community;
- resource;
- commitment;
- memory-bearing artifact.

The person's relation to a target can be historically constituted through:
- use;
- labor/care;
- dependence;
- investment;
- striving;
- recognition;
- obligation;
- scarcity;
- loss;
- exchange;
- status;
- memory;
- other-person linkage;
- routine/practice.

Do not necessarily store a bespoke "meaning object" for every target.

Where the necessary inputs already exist, derive the current meaning on demand.

## 4. Thin domain adapters

Centralization does not mean pretending all targets are identical.

Different target classes contribute domain-specific facts.

Examples:

OBJECT adapter:
- provenance;
- ownership;
- use;
- material affordance;
- replaceability;
- exchange price;
- wear/repair;
- gift/inheritance history.

PLACE adapter:
- control/access;
- dwelling/work/community role;
- memories/events;
- privacy/publicness;
- routine use.

MONEY / RESOURCE adapter:
- scarcity;
- ownership/control;
- debt;
- exchange;
- obligation;
- survival dependency.

RITUAL / PRACTICE adapter:
- recurrence;
- role;
- community;
- discipline;
- sacred/profane or identity-bearing history where generated.

These adapters provide target facts into the same relational derivation spine. They do not become independent psychic engines.

## 5. Standard derivation query

A general relational interpretation query can be conceptualized as:

RELATIONAL_MEANING(
  actor,
  target,
  counterpart,
  operation_or_event,
  current_context
)

drawing from:
- durable actor V3 state;
- actor-target history;
- counterpart model;
- dyadic history/conventions;
- network context;
- target/world provenance;
- current event-time state.

Output:
- actor-local meaning hypotheses;
- expected relational implications;
- likely expectation/boundary/obligation changes;
- uncertainty / competing interpretations;
- relevant provenance.

The result is derived current-state material unless an actual event and governed promotion process causes durable change.

## 6. Stored-versus-derived discipline

Preserve the inherited V3 principle:

STORED CAUSAL STATE != DERIVED VIEW.

Therefore:
- do not precompute/store every possible meaning of every object/person/place;
- do not persist a derived interpretation merely because the UI queried it;
- do persist history when the actor actually experiences, uses, gives, loses, discusses, reinterprets or otherwise forms a causally durable relation with the target;
- materialize/cache derived views only for runtime efficiency with exact authoritative refs.

This is especially important for curiosity invariance: asking what something means must not create its meaning.

## 7. Central relational primitives should travel across domains

The rewrite should search for well-founded primitives that recur across many domains, such as:

- investment;
- dependence;
- recognition;
- obligation;
- expected reciprocity;
- control / authority;
- exposure / vulnerability;
- familiarity;
- access;
- scarcity / replaceability;
- care / labor contribution;
- identity/self-model relevance;
- striving relevance;
- memory/significance;
- network linkage;
- expected cost of loss or refusal.

These are not one scalar vector that determines everything.

They are reusable causal dimensions whose configuration can support many derived questions.

## 8. Existing V3 continuity

Recovered V3 already contains substantial reusable machinery:
- persistent causal state;
- stored-versus-derived discipline;
- need axes and expectation baseline;
- StrivingObjects;
- Gift / Disruption / Rupture shards;
- multi-year metabolization;
- relational magnets;
- pressure-flow history, grooves and conductance;
- alienation;
- public/private/inner registers;
- buffers and costs;
- practices;
- collective infrastructure;
- autonomy/safety;
- self-model / memory pathways.

The relational rewrite should prefer re-keying and deepening these mechanisms around actual counterpart/target/history relations over replacing them with multiple new semantic engines.

## 9. Derivation families

Product design should define families of queries that reuse the same spine.

Examples:

### Access / boundary
What does granting, exercising or refusing access mean here?

### Object / material value
What does using, lending, gifting, damaging, selling or withholding this thing mean here?

### Care / help
What does giving, receiving, refusing or failing care mean with this counterpart?

### Money / exchange
What does payment, gift, debt, borrowing, splitting cost or refusing money mean here?

### Space / hospitality
What does entry, feeding, staying overnight, privacy or helping oneself mean here?

### Disclosure / information
What does telling, withholding, asking, snooping or being entrusted with information mean here?

### Time / availability
What does waiting, making time, lateness, spontaneous contact or expected presence mean here?

### Ritual / practice
What does inclusion, exclusion, participation, teaching or desecration mean here?

### Work / project
What does collaboration, delegation, criticism, credit or abandonment mean here?

These are derivation approaches over shared causal state, not nine separate psychologies.

## 10. Failure boundary

Centralization fails if it becomes an unconstrained generic LLM prompt:

"Given the persona, what does X mean?"

The central spine must provide typed, provenance-bearing causal inputs and domain facts.

The model may propose/render bounded interpretations, but it cannot invent missing durable history or overwrite canonical state merely to make an answer psychologically satisfying.

## 11. Product consequence

The desired capability is not that Rawlsing stores an encyclopedia of what everything means to Nadia.

It is that Nadia is computationally constituted richly enough that many meanings become deducible consequences of who she has become, what this thing has been in her life, who this other person is to her, and what has happened between them.

Compact law:

RICH CENTRAL PERSON / RELATION / WORLD STATE
-> MANY LAWFUL DERIVED MEANINGS.

Add specialized state only where repeated hostile cases prove the central state underdetermines behavior.
