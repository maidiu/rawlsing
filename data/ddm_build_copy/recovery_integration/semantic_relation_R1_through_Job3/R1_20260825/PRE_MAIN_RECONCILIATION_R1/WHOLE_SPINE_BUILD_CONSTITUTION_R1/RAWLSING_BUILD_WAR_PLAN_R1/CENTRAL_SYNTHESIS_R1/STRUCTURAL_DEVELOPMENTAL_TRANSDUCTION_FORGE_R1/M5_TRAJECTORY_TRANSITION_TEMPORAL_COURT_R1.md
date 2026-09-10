# M5_TRAJECTORY_TRANSITION_TEMPORAL_COURT_R1

STATUS: `COURT_COMPLETE`

SOURCE BASIS: Dreier, *Psychotherapy in Everyday Life*, especially Ch. 6 pp. 109–140, Ch. 8 pp. 181–197, and Chs. 9–11 pp. 198–286.

## 1. Court question

Does Dreier require a new trajectory carrier, or can his temporal machinery be represented through existing history plus D2 rebinding?

**VERDICT:** `NO_NEW_TRAJECTORY_OWNER_PROVED__D2_MUST_SUPPORT_OVERLAPPING_INTERVALS_RECURRENCES_AND_CONTEXTUAL_TRANSITIONS`.

Dreier strengthens D2 substantially. He does not justify reifying `TRAJECTORY` as an independent causal substance.

## 2. Mandatory temporal distinctions

The source requires at least:

```text
OCCURRENCE / EVENT
CONDITION
RELATION
RECURRENT ACTIVITY / ROUTINE
VARIATION
SHIFT
TRANSITION
TRAJECTORY
TURNING POINT
CUMULATIVE / DEVELOPING PROCESS
```

The most important addition to the frozen temporal court is Dreier’s warning that **variation and periodic shift are not automatically change**.

## 3. Event

A discrete event is a bounded occurrence: a session, quarrel, gate decision, move, school entry, encounter, etc.

**Dreier ceiling:** a life cannot be reduced to events. Persistent arrangements and recurrent practices organize what events mean and what is possible around them.

**Rawlsing:** reuse OEE/event machinery where competent.

## 4. Condition

Conditions include ongoing arrangements such as living situations, recurring schedule constraints, persistent access limitations and continuing dependency relations.

**Dreier ceiling:** a condition does not have to “fire” as a salient event to matter.

**Rawlsing:** D2 active interval semantics.

## 5. Relation

Relations connect actors in directed social positions: parent/child, therapist/client, spouse/spouse, worker/supervisor, friend/friend, etc. They persist through intervals but are enacted variably.

**Dreier ceiling:** relation is not equivalent to contact; a continuing relation can exist while copresence fluctuates.

**Rawlsing:** persistent directed relation semantics + D2 validity interval.

## 6. Recurrent activity / routine

Dreier’s everyday life is patterned by recurring practices and routines across multiple frequencies.

Required representation:

```text
RECURRENCE_IDENTITY
+ CONTEXT/POSITION
+ PERIOD OR TRIGGER
+ ACTUAL OCCURRENCES / PARTICIPATION
+ QUALITY/INTENSITY WHERE RELEVANT
+ START/END/INTERRUPTION
```

Daily, weekly, fortnightly, monthly and seasonal rhythms all appear in the analysis. Temporary treatment is itself inserted as a recurrent context for an interval.

**Rawlsing:** D2 must not fictionalize recurrence as unrelated OEE events.

## 7. Variation

Chapter 6 distinguishes ordinary variation in participation/experience across contexts and occasions from actual change.

Examples:

- more/less conflict at home on different days;
- different modes of participation at school and home;
- weekday/weekend or seasonal differences;
- symptom flare/subsidence by context.

**Binding law:**

```text
CONTEXTUAL OR PERIODIC VARIATION != PERSONAL CHANGE
```

This matters for any model trying to infer development from observed behavioral differences.

## 8. Shift

A pronounced periodic alteration or temporary reorganization can occur without a durable structural/person change.

Examples include illness, holidays, temporary absence, treatment period, exceptional work demands or seasonal activities.

**Binding law:**

```text
SHIFT != TRANSITION != DURABLE CHANGE
```

A shift can nevertheless become part of a later transition if it changes subsequent bindings.

## 9. Transition

A transition changes one or more bindings: school, work, living arrangement, relationship, treatment status, mobility, family task allocation, etc.

Dreier’s material strongly supports the frozen D2 law:

```text
BEFORE BINDINGS
-> TRANSITION
-> DEACTIVATE / MODIFY / ADD BINDINGS
-> AFTER BINDINGS
```

But M5 adds two constraints:

1. one transition may alter several context-position relations while leaving others continuous;
2. persons normally retain multiple concurrent contexts before and after, so rebinding must not reset the actor’s whole life state.

Hence transition update should be **partial and typed**, not actor-global replacement.

## 10. Institutional trajectory

Institutions organize possible/expected pathways through:

- entry criteria;
- age/status rules;
- expected duration;
- required prior participation;
- allowed successors;
- entitlements/accomplishments;
- treatment/education/work schedules.

This is a PRE-V3/social possibility structure.

```text
INSTITUTIONAL_ROUTE POSSIBILITY
!= EXPECTED TRANSITION
!= ACTUAL TRANSITION
!= PERSONAL TRAJECTORY
```

Dreier especially notes that children/youth often face tighter age-sequenced institutional trajectory regulation than adults.

## 11. Personal trajectory

Dreier’s strongest temporal correction is that a life trajectory is not “just a process in time.” It extends across **times and places** because the person unfolds it through participation in several contexts.

The court resolves trajectory at three grains.

### Grain T1 — stored realized history

```text
ORDERED TYPED RECORD OF
CONTEXTS / POSITIONS / RELATIONS / PARTICIPATIONS / TRANSITIONS
```

This is biography/history storage and provenance.

### Grain T2 — derived present trajectory view

A current view can summarize where the actor has come from, present direction/pursuits, expected/possible future routes and discontinuities.

For the objective/social side, this can be a derived query/view over history + current institutional routes.

For first-person meaning/orientation, V3 owns the actor’s understanding/stance toward that trajectory.

### Grain T3 — causal process

Trajectory has causal force only when prior sequence/timing/duration has produced a **current mediating fact**, for example:

- current credential/eligibility;
- established relationship;
- practiced ability;
- depleted/accumulated resource;
- current expectation/belief in V3;
- current institutional mark;
- current dependency;
- currently reachable network/context.

Therefore:

```text
TRAJECTORY LABEL ALONE -> EFFECT
```

is forbidden.

Required:

```text
PRIOR ORDERED HISTORY
-> CURRENT TYPED MEDIATOR
-> CURRENT POSSIBILITY / ACTION / DEVELOPMENTAL CONSEQUENCE
```

### Trajectory verdict

`ALL_THREE_AT_DISTINCT_GRAINS`.

But only T1 requires stored history. T2 is derived. T3 must unpack to a typed mediator. No monolithic `TRAJECTORY_STATE` is required.

## 12. Turning point

Dreier’s cases contain events/transitions that can later be interpreted as major redirections, but his analysis does not warrant a standalone turning-point carrier.

A transition becomes a turning point only retrospectively/analytically when subsequent trajectory shows sustained redirection.

```text
TRANSITION/EVENT
+ LATER SUSTAINED CHANGE IN PARTICIPATION/ROUTE
-> TURNING_POINT PREDICATE
```

**Rawlsing:** retain frozen synthesis decision: derived predicate, no owner.

## 13. Cumulative/developing process

Changes in conduct, relationships, abilities and arrangements often accrue through repeated participation and mutual adjustment rather than one decisive event.

However, Dreier gives no reason for a generic cumulative scalar.

Required:

```text
TYPED HISTORY_t
+ CURRENT PRACTICE/RELATION_t
-> CURRENT UPDATE_t+1
```

with domain-specific state and possible reversals/interruptions.

## 14. Multi-context rhythms court

### Required representation

One actor may simultaneously have:

```text
school weekdays
work evenings
therapy every second week
family care daily but varying
friend activity weekends
seasonal riding/sport
periodic institutional appointments
```

These patterns can overlap, conflict and alter one another.

### D2 adequacy test

D2 is adequate **if and only if** implementation permits:

```text
MULTIPLE CONCURRENT VALID INTERVALS
+ MULTIPLE RECURRENCE IDENTITIES
+ CONTEXT-SPECIFIC POSITION BINDINGS
+ PARTIAL TRANSITION UPDATES
+ BEFORE/AFTER PROVENANCE
+ CROSS-CONTEXT TEMPORAL CONSTRAINT EDGES
```

If D2 were implemented as a single actor-global phase/context slot, it would fail Dreier.

This is a requirement on D2’s shape, not proof of D4.

## 15. Stability court

Dreier offers a powerful anti-trait caution: stability in personal functioning may be produced by stability in the person’s conducted arrangement of life.

Therefore:

```text
REPEATED SIMILAR BEHAVIOR
+ STABLE RECURRING CONTEXT ARRANGEMENT
DOES NOT BY ITSELF PROVE
CONTEXT-FREE DURABLE TRAIT
```

V3 must earn generalization beyond the realized contexts.

## 16. Transition examples normalized from the case material

### School transition

```text
OLD SCHOOL / PEER / RULE BINDINGS
-> SCHOOL CHANGE
-> NEW SCHOOL / PEER / RULE BINDINGS
-> NEW PARTICIPATION POSSIBILITIES
```

Not automatically a turning point; later sustained redirection decides.

### Therapy entry/exit

```text
ORDINARY LIFE
-> ADD TEMPORARY RECURRING THERAPY CONTEXT
-> CROSS-CONTEXT USE/NONUSE DURING INTERVAL
-> THERAPY ENDS
-> ORDINARY CONTEXTS CONTINUE, POSSIBLY CHANGED
```

Therapy does not become a total life phase.

### Child mobility expansion

```text
DEPENDENT TRANSPORT / LIMITED REACH
-> ABILITY/ACCESS CHANGE + ROUTE USE
-> EXPANDED REACHABLE CONTEXT SET
-> NEW FRIEND/ACTIVITY PARTICIPATION
```

Part social ecology, part V3 acquired capacity; must preserve jurisdiction.

### Family task/permission reorganization

```text
MEMBER TRAJECTORY CHANGE
-> FAMILY OBLIGATION/PERMISSION/TIME ARRANGEMENT UPDATE
-> LATER MULTI-MEMBER ECOLOGY REBINDING
```

D3 establishes changed arrangement; D2 carries new interval.

## 17. Temporal negative ceilings

```text
EVENT != CONDITION
RELATION != CONTACT
RECURRENCE != EVENT PILE
VARIATION != CHANGE
SHIFT != TRANSITION
TRANSITION != TURNING_POINT
INSTITUTIONAL ROUTE != ACTUAL TRAJECTORY
AGE-SEQUENCED INSTITUTIONAL PASSAGE != NATURAL DEVELOPMENTAL STAGE
TRAJECTORY HISTORY != ACTOR'S INTERPRETATION OF TRAJECTORY
TRAJECTORY LABEL != CAUSAL FORCE
STABLE CONDUCT != INVARIANT TRAIT
```

## 18. Court terminal

`PASS__D2_CAN_HOST_DREIER_IF_GENERALIZED_FOR_CONCURRENT_INTERVALS_RECURRENCE_IDENTITIES_PARTIAL_REBINDING_AND_ORDERED_TYPED_HISTORY__TRAJECTORY_IS_HISTORY_PLUS_DERIVED_VIEW_PLUS_TYPED_CAUSAL_PROCESS_AT_DISTINCT_GRAINS__NO_NEW_CARRIER_PROVED`