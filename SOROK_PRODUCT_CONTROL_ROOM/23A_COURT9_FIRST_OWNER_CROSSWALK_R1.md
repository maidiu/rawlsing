# Sorok Court 9 — First Owner Crosswalk and Minimum Durable Relationship Set R1

Status: PROVISIONAL_COURT_FINDING__ARCHITECTURE_CROSSWALK_COMPLETE_AT_FIRST_PASS

Date: 2026-09-29

## 0. Court holding

The current Rawlsing architecture already answers a large part of the Court 9 question.

**A relationship is a real canonical entity, but it is deliberately thin.**

ADP-015 already owns:
- stable relationship entity identity;
- participant/role/directionality bindings;
- append-only lifecycle history;
- exact formation/transition/end events;
- objective state-fact refs;
- actor-specific perceived-relationship state records when exact rules emit them.

It explicitly rejects:
- generic trust scores;
- intimacy scores;
- relationship personality;
- one actor's state becoming reciprocal truth;
- V2 session/tone as relationship truth.

Therefore Sorok should not replace ADP-015 with 'relationship is only a derived view.'

Better formulation:

> **The objective relationship object is thin and authoritative; most psychological richness remains distributed across person-owned and neighboring authorities. A product relationship view can then materialize these lawful grains without owning them.**

---

## 1. Existing owner map

| Semantic | Current/Inherited owner | Court 9 disposition |
| --- | --- | --- |
| Relationship identity / participants / roles / lifecycle | ADP-015 | REUSE |
| Objective relationship history | ADP-015 + causal event ledger | REUSE |
| Objective relationship state facts emitted by exact relationship rules | ADP-015 | REUSE, keep sparse |
| One actor's perceived relationship state | ADP-015 actor-specific record | REUSE; never reciprocal truth |
| Episodic/causal memory of relationship events | ADP-016 | REUSE |
| Actor knowledge/belief/uncertainty/access about relation | ADP-017 | REUSE |
| Relation/situation-scoped expectations | CAN-010 via exact `scope_ref` / target refs and lawful causal parents | REUSE; strong fit for domain-specific trust expectations |
| Persistent actor embedding in generated relationship field | CAN-011 `EMBEDDING_RELATION` where exact update authority exists | REUSE where applicable |
| Current person×event uptake/appraisal/response | CAN-008 R2 | REUSE |
| Interaction-fast hypothesis/residue | narrowed PFF | REUSE where causally necessary |
| Relationship expression from one actor's lawful perspective | CAN-019 / V2 | REUSE |
| Objective user/persona interaction occurrence | ADP-019 + exact event authority | REUSE ingress/admission machinery |
| Product convenience relationship summary | no causal owner required | DERIVED / MATERIALIZED VIEW ONLY |

---

## 2. Trust decomposition — first result

Generic objective `trust` is unnecessary and contrary to current authority.

Candidate decomposition:

`OBJECTIVE HISTORY`
+ `ACTOR MEMORY`
+ `ACTOR-SCOPED EXPECTATION`
+ `ACTOR BELIEF / MODEL`
+ `CURRENT RESPONSE`.

Examples of distinct expectation scopes:
- keeps confidences;
- returns money;
- shows up when promised;
- tolerates disagreement;
- respects a boundary;
- safely watches a child;
- remembers practical instructions;
- does not publicly humiliate me.

CAN-010 already requires exact `scope_ref` and explicitly prevents a situation-specific expectation from becoming universal automatically.

This is almost exactly the product requirement Sorok had independently converged on.

---

## 3. Intimacy decomposition — first result

Do not search for one intimacy scalar.

Represent what intimacy **changes**:
- objective access/permissions where world/relationship rules establish them;
- explicit commitments/roles;
- actor-specific expectations;
- relation-scoped need postures;
- actor memories;
- persistent relation embedding/practices where lawfully generated;
- current PFF/CAN-008 mediation;
- network inclusion.

A product can derive a descriptive intimacy view if useful.

That view must not become causal authority.

---

## 4. Commitments, permissions, routines, and joint projects

These require sharper owner adjudication.

### Commitments / explicit agreements
Strong candidate: exact relationship-state facts or separately governed commitment facts referenced by ADP-015.

### Property / space access
Likely world/property/access authority first; relationship may reference the permission but should not own the physical property semantics.

### Repeated routines
Do not automatically store a routine because behavior repeated.

Possible states:
- repeated event pattern only;
- actor expectation that it will recur;
- explicit agreed schedule/commitment;
- separately governed habitual practice.

### Joint projects
May require true shared project entities.

But:

`JOINT PROJECT OBJECT != GENERAL RELATIONSHIP PSYCHE`.

These are remaining owner questions, not evidence for a monolithic dyad state.

---

## 5. Materialized relationship view

Product/runtime convenience may need a fast view such as:

`RELATIONSHIP_VIEW {`
- relationship entity ref;
- current objective roles/agreements/access refs;
- recent shared events;
- unresolved objective commitments;
- actor-A perceived-state refs;
- actor-B/player-model refs where lawful;
- relevant expectation/memory refs;
- network/joint-project refs;
- unknown/deferred fields;
`}`

Law:

`RELATIONSHIP_VIEW != SEMANTIC OWNER`.

It can be cached/indexed for performance but every field must point back to authoritative refs.

---

## 6. Major new starvation case — the human user is not currently a generated V3 actor

ADP-015 formation law requires relationship participants to be already-generated V3 actors with valid history anchors.

That is correct for persona↔persona relationships.

But Sorok's central relationship is often:

`GENERATED PERSON ↔ REAL HUMAN USER`.

Current external-event machinery gets us only partway:

- ADP-019 can admit exact external/user observable interaction events;
- CAN-025 can carry exact participant bindings;
- neither is allowed to manufacture participant identity or actor facts;
- ADP-015 does not currently define a real-human external participant class.

Therefore Sorok has found a genuine seam requirement:

**a stable, governed player-world participant identity/binding that can participate in V3 relationship/event history without pretending V3 generated the human user's psyche.**

---

## 7. Two candidate seam architectures

### Option A — explicit external participant class

Create a governed participant kind such as:

`PLAYER_WORLD_PARTICIPANT_REF`

which may be consumed by:
- external-event participant binding;
- encounter/relationship rules authorized for human-player participation;
- world position/access/resource systems;

while remaining explicitly non-V3-psyche-owned.

Possible fields:
- stable participant ID;
- player-embedding profile ref;
- homologous structural-position refs;
- embodiment/legibility refs;
- resource-envelope refs;
- current in-world existence/effective time;
- event-history anchor;
- provenance/version;
- `agency_source = EXTERNAL_HUMAN_USER`.

Advantages:
- clean ontology;
- does not pretend V3 generated user psychology;
- preserves user opacity.

Cost:
- ADP-015 and neighboring rules need a governed participant-generalization seam.

### Option B — sparse V3 actor shell under external agency

Create a sparse actor entity solely for world identity/position/relationship participation, with:
- zero generated psychology by default;
- no CAN-008 autonomous response generation for user-controlled action;
- external agency source;
- player actions admitted as external events.

Advantages:
- reuses existing actor/position/relationship identities.

Risks:
- 'actor' semantics may silently pull the user into V3 psyche machinery;
- future code may generate needs/memory/response as if user were synthetic;
- blurs generated-person versus real-human epistemic boundary.

Current Court 9 lean:

**Option A is conceptually cleaner.**

Do not adopt before implementation/authority court proves the participant-generalization can be done without duplicating relationship machinery.

---

## 8. Player-side relationship psychology remains asymmetric

The persona may have generated:
- memories of the user;
- expectations about the user;
- beliefs about the user;
- relation-specific needs/defenses;
- perceived relationship state.

Rawlsing should not mirror this into an omniscient synthetic 'user psyche'.

User side may contain:
- canonical realized action history;
- explicit user self-reports;
- optional user-entered relationship model;
- system hypotheses for later praxis reflection;

but these remain epistemically distinct.

Thus:

`PERSONA MODEL OF USER != USER TRUE MIND != SYSTEM PLAYER-MODEL HYPOTHESIS`.

---

## 9. Minimum durable set — first court answer

Current minimum candidate:

1. `V3RelationshipEntity` — thin shared identity/lifecycle/objective state refs.
2. Canonical admitted shared event history.
3. Objective current agreements/roles/access/project refs under exact owners.
4. Actor-specific perceived relationship states where exact rules create them.
5. ADP-016 causal memories.
6. ADP-017 beliefs/knowledge/access states.
7. CAN-010 relation-scoped expectations/strivings.
8. CAN-011 persistent actor middle-state relation/practice refs where lawfully generated.
9. Network/household/joint-project/world facts under their exact owners.
10. Stable player-world participant binding for the external human user — currently missing/open.
11. Derived product relationship view — noncausal convenience only.

Nothing in this first pass justifies a new generic dyad psyche, closeness score, trust score, or intimacy store.

---

## 10. Court 9 provisional verdict

**Reuse the existing thin V3 relationship entity. Distribute psychological richness across existing person-owned authorities. Add no dyad psyche. Treat the external human participant seam as the genuine new product-driven architecture problem.**

---

## 11. Next Court 9 work

1. exact player-participant seam requirements;
2. owner court for commitments/access/routines/joint projects;
3. hostile test: user/persona relationship forms without reciprocal sentiment;
4. hostile test: persona has rich model of user while system remains uncertain about user's mind;
5. build D001 minimum durable-object table with current owner/status/needed extension.