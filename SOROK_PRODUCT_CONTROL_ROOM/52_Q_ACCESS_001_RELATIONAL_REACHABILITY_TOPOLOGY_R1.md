# Sorok — Q-ACCESS-001 Relational Reachability Topology R1

Status: `PROVISIONAL_PRODUCT_CONSTITUTION__Q_ACCESS_001_CLOSED_FOR_ALPHA_SPEC__NON_DISPOSITIVE_TO_PYAT_PREMAIN`

Date: 2026-09-30

## 0. Question

`Q-ACCESS-001`:

> What exact relational-access topology governs how the user becomes able to enter previously unavailable parts of the persona's life without scalar unlocks or guaranteed disclosure?

This artifact closes the alpha product question. It does not assign final ADP/V3/CAN-008/PFF/world owner placement, storage schema or runtime implementation.

---

## 1. Holding: access is reachability, not relationship level

Rawlsing should not model relational access as:

`CLOSENESS += n -> CONTENT_UNLOCK`

or:

`TRUST >= threshold -> HOME / CHILD / WORK / SECRET becomes available`.

Instead:

> **A person's life is a topology of independently existing domains, people, places, channels, projects, routines and events. Relationship history can create, narrow, reroute or terminate specific lawful routes by which the user can participate in some of them.**

Therefore:

`RELATIONSHIP DEVELOPMENT != ACCESS LEVEL`.

and:

`MORE ACCESS != BETTER RELATIONSHIP`.

and:

`MORE INTIMACY != MORE ACCESS IN EVERY DOMAIN`.

---

## 2. Access is a sparse typed multigraph

Product-level representation should behave as if there are:

### Nodes
Examples:
- focal person;
- home / rooms;
- workplace / work role;
- child / family member;
- friend / coworker;
- community / religious setting;
- project / obligation;
- communication channel;
- recurring activity;
- event;
- resource / entrusted object;
- institution.

### Access routes / edges
A route connects the user to some node in a particular way.

Examples:
- may message through established channel;
- may knock at home;
- may enter when invited;
- has standing permission to enter a room;
- may attend a specific family meal;
- is introduced to a coworker;
- may pick up the child on one occasion;
- is expected at a recurring community activity;
- may borrow a key/tool;
- may be called for a specific practical need;
- may ask about a domain without entitlement to an answer.

There is no single edge called `INTIMACY` that implies the rest.

---

## 3. Minimum semantic dimensions of an access route

At product grain, every meaningful access route needs enough semantics to answer:

1. **TARGET** — what part of life becomes reachable?
2. **MODE** — physical entry, communication, participation, practical agency, information request, resource use, social introduction, etc.
3. **ROUTE / BASIS** — invitation, standing permission, public access, role, routine, joint project, possession, institutional rule, third-party relation, emergency circumstance, other lawful cause.
4. **CONTROLLER / AUTHORITY** — who or what can lawfully grant/withhold/change this route?
5. **SCOPE** — exactly what does the route permit?
6. **CONDITIONS** — time/place/event/purpose/other-person conditions.
7. **TEMPORALITY** — one-shot, bounded interval, recurring, standing, expired, suspended.
8. **REVOCABILITY / CHANGE** — how can the route narrow, disappear or transform?
9. **DEPENDENCIES** — third-party consent, schedule, institution, resource, current relationship fact, physical availability.
10. **PROVENANCE** — what event/history established the current route?

Exact field names/storage remain implementation work.

---

## 4. Controllers matter

Access is not always Nadia's to grant.

Possible controllers include:

### Focal actor
Nadia can invite the user to dinner or permit them into her bedroom.

### Third party
Nadia cannot unilaterally grant unlimited social/physical access to another adult's private life.

### Child / dependent relation
Parenting authority can create some routes, but a child remains an independently modeled actor whose own perception, comfort, privacy and consequences matter.

### Institution
A workplace, school, clinic, religious body or building may control access regardless of Nadia's desire.

### Material world
Locked doors, transport, distance, schedules and resources constrain actual reachability.

### Public/structural rule
Some domains are publicly reachable without relational permission.

Thus:

`NADIA WANTS USER PRESENT != USER CAN LAWFULLY/CAUSALLY BE PRESENT`.

---

## 5. Route existence != current opportunity != realized presence

Preserve at least:

`POSSIBLE ROUTE`
→ `CURRENT ACCESS / PERMISSION / ELIGIBILITY`
→ `CONCRETE OPPORTUNITY OR INVITATION`
→ `USER ACCEPTS / ATTEMPTS`
→ `REALIZED PARTICIPATION OR PRESENCE`.

Examples:

- User has Nadia's number. She is currently asleep.
- User is generally welcome in the kitchen. The household is away.
- User has standing permission to visit. A family conflict makes tonight inappropriate.
- User was invited to a school event. They never attend.
- User is trusted with a spare key. That does not authorize searching drawers.

No stage implies the next.

---

## 6. Access != disclosure != knowledge

Physical/social access and information access are distinct.

The user may:
- be in Nadia's home for years without learning a formative history;
- know a sensitive fact while never meeting her family;
- meet the child while knowing almost nothing about work;
- be invited into a crisis while still being excluded from another domain.

Hard noncollapses:

`ACCESS TO PERSON != ACCESS TO PLACE`

`ACCESS TO PLACE != ACCESS TO OBJECT`

`ACCESS TO OBJECT != PERMISSION TO INSPECT`

`ACCESS TO EVENT != ACCESS TO EVERY PARTICIPANT`

`ACCESS TO ACTOR != ACTOR DISCLOSURE`

`PERMISSION TO ASK != ENTITLEMENT TO ANSWER`

`DISCLOSURE != OBJECTIVE TRUTH`.

Q-DISCLOSE-001 remains actor-owned under its separate constitution.

---

## 7. Access is domain-specific

A relation may have different shapes across domains.

Example Nadia/user state:

- messaging: active and frequent;
- home: generally welcome by invitation;
- child: known acquaintance, no unsupervised care;
- work: stories shared, workplace not open to user;
- family: one sibling met, parents unknown;
- finances: some practical visibility, no delegated control;
- crisis contact: user sometimes called;
- religion/community: not included.

This cannot be represented truthfully by one scalar.

---

## 8. Access is nonmonotonic

Access may:
- expand;
- narrow;
- expire;
- pause;
- become conditional;
- shift mode;
- be rerouted through another person;
- disappear because the underlying activity/institution ends.

Examples:
- rupture closes household access but messaging remains;
- divorce changes family-network routes;
- new job removes workplace access;
- repair restores some prior route but not all;
- increased intimacy creates stronger privacy in one domain;
- a parent becomes more comfortable with conversation but less comfortable with unsupervised child contact;
- a practical routine ends because it is no longer needed.

Therefore:

`ACCESS LOSS != RELATIONSHIP FAILURE`.

and:

`ACCESS GAIN != RELATIONSHIP SUCCESS`.

---

## 9. Access need not be morally earned

Existing shorthand such as "earned access" is useful only if read causally, not morally.

Access may arise because of:
- trust;
- affection;
- habit;
- practical need;
- obligation;
- emergency;
- dependency;
- fear;
- manipulation;
- role;
- institutional assignment;
- convenience;
- third-party request;
- accidental circumstance.

A controlling or unhealthy relationship may produce extensive access.

A respectful healthy acquaintance may retain narrow access.

Thus product law should prefer:

> **historically formed / causally established access**

over a game-reward interpretation of "earned access."

---

## 10. Relationship history changes routes, not reward tiers

Events can alter specific routes.

Examples:

### Reliability
Repeatedly showing up for agreed childcare may make later childcare requests more causally reachable.

It does not automatically increase:
- disclosure;
- home entry;
- financial authority;
- affection.

### Boundary violation
Searching a cabinet may narrow unsupervised household access.

It does not necessarily:
- end messaging;
- eliminate all trust;
- make every future interaction cold.

### Shared activity
Working beside Nadia may create workplace-adjacent introductions or practical routines.

It does not automatically authorize entry into family life.

### Conflict and repair
A rupture may close a route.
Repair may reopen:
- the same route;
- a narrower route;
- a differently conditioned route;
- no route at all.

History matters at the exact affected grain.

---

## 11. Invitation is an event over access topology

An invitation is not the same thing as an access edge or an engagement reward.

Conceptually:

`CURRENT PERSON/WORLD PURPOSE`
+ `LAWFUL ACCESS ROUTE / POSSIBLE ROUTE`
+ `CURRENT RELATIONSHIP HISTORY`
+ `NETWORK / INSTITUTION / SCHEDULE CONDITIONS`
→ possible actor-owned invitation event.

An invitation may:
- instantiate one-time access;
- exercise an existing standing route;
- propose a new recurring route;
- be refused;
- expire;
- be withdrawn;
- fail materially.

This preserves Q-INVITE-001 as validation/runtime work without making invitation itself the progression mechanic.

---

## 12. Access can create obligations and expectations without becoming consent fiction

A route may accumulate social meaning.

Examples:
- being given a key may create an expectation of emergency availability;
- joining a weekly routine may create an expectation of notice before absence;
- being introduced as a trusted helper may alter third-party expectations;
- regular childcare may create reliance.

But:

`ACCESS != BLANKET CONSENT`.

and:

`PAST PERMISSION != PERMANENT PERMISSION`.

and:

`EXPECTATION != USER OBLIGATION UNLESS A LAWFUL COMMITMENT/ROLE EXISTS`.

The exact commitment owner remains implementation work.

---

## 13. Third-party firewall

Nadia's relationship with the user cannot collapse third parties into her possessions.

If access reaches:
- child;
- partner;
- coworker;
- friend;
- family member;
- community member;

then that person must remain an independent center of action at the fidelity required by the encounter.

Nadia may create a route of introduction or situational access.

She cannot guarantee:
- their liking;
- their disclosure;
- their future access;
- their consent;
- their interpretation.

`ACCESS THROUGH NADIA != OWNERSHIP OF THIRD-PARTY RELATION`.

---

## 14. Relational importance and access can diverge

A user may become extremely important while having little direct physical access:
- long-distance relationship;
- estrangement;
- caregiving by message;
- institutional barriers;
- illness;
- family boundary.

A user may have extensive practical access while relational importance remains low:
- coworker;
- landlord;
- assigned helper;
- household employee;
- neighbor with a key.

Therefore access is one visible topology of relation, not a proxy for total significance.

---

## 15. User-facing experience

The topology should normally be learned through the world, not shown as a graph/dashboard.

The user notices:

- "Text me when you get home."
- "Just come in next time."
- "Don't go in there."
- "Can you pick Sami up Thursday?"
- "My sister wants to meet you."
- "I'd rather not have you at work."
- silence after a previously ordinary request;
- a key is returned;
- a recurring invitation stops;
- another person begins contacting the user directly.

These are gameplay facts.

No:
- ACCESS +7;
- HOME DOMAIN UNLOCKED;
- CHILDCARE TRUST TIER 2;
- intimacy progress bar.

---

## 16. Hard hostile cases

Any access constitution should handle:

1. Nadia gives user a key, but only for emergencies.
2. User is welcome in kitchen, not bedroom.
3. User knows child well, but child currently does not want help.
4. Nadia wants user at work, employer forbids it.
5. User has phone access during rupture but no home access.
6. Nadia discloses financial trouble but gives no financial-control permission.
7. User is introduced to sibling; sibling dislikes user and independently narrows contact.
8. High-conflict/manipulative relationship produces broad access without flourishing.
9. Respectful bounded acquaintance never expands beyond occasional coffee.
10. Practical need creates sudden crisis access before high intimacy.
11. Repaired relationship restores messaging but not spare-key access.
12. Existing routine grants expected presence at one recurring event but not generalized household entry.
13. User is invited to a family dinner but not entitled to interrogate family members.
14. Nadia says "come over anytime" but a later contextual boundary overrides literal standing language.
15. Public event is reachable independently of Nadia even if she would prefer the user not attend; relational consequence remains separate from physical/public access.

A scalar model fails these cases.

---

## 17. Alpha topology theorem

The minimum alpha does not need every possible social relation.

It needs enough typed access to support the first relationship's likely domain changes:

- contact channel;
- physical encounter route;
- home/household situational access;
- practical-help/task participation;
- one or more third-party introductions;
- event/outing invitation;
- bounded recurring routine or commitment where generated;
- explicit narrowing/refusal/expiry.

This is enough to test whether the user experiences a life becoming differently reachable through history rather than as unlockable content.

---

## 18. Implementation boundary

Q-ACCESS-001 closes the product law but does not answer:

- which access facts live in ADP-015 relationship entity;
- which belong to world/place/resource authorities;
- which are event-derived;
- how permissions are materialized/indexed;
- how third-party authority is represented;
- how route conditions are cached;
- how current access is computed from commitments/routines/institutions;
- what noncausal relationship view is used for fast runtime.

Those remain architecture questions, principally Q-RELFACT-001 and the implementation successor created by this adjudication.

Do not create a new dyadic sovereign merely because the access graph is useful.

---

## 19. Q-ACCESS-001 disposition

At product-spec grain:

`Q-ACCESS-001 = PROVISIONALLY_ANSWERED / CLOSED_FOR_ALPHA_SPEC`.

The controlling laws are:

1. access is a sparse typed topology, not a scalar;
2. life domains exist independently of user access;
3. access routes have target, mode, basis, controller, scope, conditions, temporality, revocability, dependencies and provenance;
4. route existence, permission, opportunity and realized participation remain distinct;
5. access, disclosure and knowledge remain distinct;
6. access is domain-specific, asymmetric and nonmonotonic;
7. focal actor does not own third-party/institutional access;
8. access can arise through healthy or unhealthy causality and is not a moral reward;
9. visible progression comes from concrete changes in routes/expectations/history, never an unlock meter;
10. exact architecture ownership is deferred to implementation.

Next ALPHA_SPEC blocker:

`Q-INVITEGRAPH-001`.
