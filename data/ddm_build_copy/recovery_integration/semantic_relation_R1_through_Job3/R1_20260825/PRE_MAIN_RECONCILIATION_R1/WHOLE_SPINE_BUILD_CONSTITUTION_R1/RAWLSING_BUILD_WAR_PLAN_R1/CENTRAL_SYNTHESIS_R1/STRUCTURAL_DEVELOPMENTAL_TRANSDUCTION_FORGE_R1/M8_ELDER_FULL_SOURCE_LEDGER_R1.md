# M8 — D1 / D2 / D3 CHALLENGE R1

Frozen candidate challenged: `ACTOR_RELATIVE_SOCIAL_ECOLOGY_TRANSDUCTION_CONSTITUTION@1.0.0-CANDIDATE.R1` at `9cf100a101e92891e2b4d0af0e308d27f7015a6b`.

## D1 — `TYPED_ACTOR_RELATIVE_SOCIAL_ECOLOGY_DERIVATION`

### Attack

Can Elder's evidence be represented by existing D1 without smuggling macro conditions or demographic categories directly into actor states?

### Result

**PASS, with one mandatory relation-schema tightening.**

Elder is direct evidence for D1's distinction:

```text
structural possibility
!= actor/household exposure
!= active social relation/activity
!= actor uptake/development
```

The book's central analytic program explicitly inserts family division of labor, family relations and social strains between economic change and person outcomes (pp. 13–15).

D1's mechanism-family registry already contains the required families:
`RESOURCE_DEPENDENCY`, `ACTIVITY_ORGANIZATION`, `TIME_ALLOCATION`, `ROLE_OBLIGATION`, `HOUSEHOLD_CARE_DEPENDENCY`, `AUTHORITY_CONTROL_SANCTION`, `NETWORK_INFORMATION_SUPPORT`, `PERSISTENT_STRAIN_CONDITION`, `LINKED_LIFE_TRANSMISSION`, `HISTORICAL_TIMING_QUALIFICATION`, `CUMULATIVE_ITERATIVE_FEEDBACK`, and `GATED_RECIPROCAL_SELECTION`.

### Tightening

For `LINKED_LIFE_TRANSMISSION`, require:

```text
SOURCE_ACTOR
TARGET_ACTOR
EXACT_RELATION/HOUSEHOLD_BINDING
SOURCE_REALIZED_STATE_OR_TRANSITION
TARGET_ECOLOGY_DIMENSION
VALID_TIME/INTERVAL
REALIZATION_STATUS
DERIVATION_PROVENANCE
```

This is a D1 rule-schema invariant, **not D4**.

### Reject

Do not add `DEPRIVATION`, `CLASS`, `SEX`, `PARENT_STRESS`, or `RESILIENCE` as generic direct person-producing operators.

---

## D2 — `INTERVAL_RECURRENCE_AND_TRANSITION_REBINDING`

### Attack

Could Elder be represented with event records alone?

### Result

**PASS; event-only representation would materially falsify the source.**

Elder requires:
- prolonged unemployment/resource conditions;
- ongoing parent/child relations;
- recurrent paid and domestic work;
- before/after role changes;
- ordered education/work/marriage/parenthood/military transitions;
- trajectories whose meaning depends on timing and persistence.

A one-off "child worked" event cannot represent duration/repetition; a one-off "father unemployed" event cannot represent chronic family resource conditions; a "marriage" event alone cannot represent the career consequences of timing/order.

### Turning point

Frozen D2 is correct that `TURNING_POINT` is derived after sustained redirection. Elder's wartime/military and marriage examples make this distinction necessary: dramatic events may interrupt or reschedule a trajectory without being its durable redirection.

---

## D3 — `PROVENANCE_PRESERVING_RECIPROCAL_SOCIAL_WORLD_UPDATE`

### Attack

Does Elder require person→world feedback, and can D3 represent it without inventing causal directions the source cannot identify?

### Result

**PASS, but only under evidence-qualified gates.**

Elder provides reciprocal/selection structures:
- father drinking can both follow job loss and increase later unemployability (p. 61);
- independent/industrious/mastery-oriented children may select into jobs, while jobs may then reinforce independence/skill (pp. 70, 75, 78–79);
- child labor contributes to household maintenance, potentially altering later household resource conditions.

D3's law is appropriate where an actor-generated action produces an external event/gate/response and a later objective social fact.

However:

```text
observed reciprocal plausibility
!= authority to instantiate both causal directions
```

When Elder says direction is unresolved, Rawlsing must retain:
- competing causal hypotheses,
- selection warning,
- or undirected/associational evidence,
not a falsely identified reciprocal update.

### Jurisdiction

Household linked-life transfer is usually D1 + D2. D3 is needed only when action meets an external/relational gate and changes subsequent world/social facts.

---

## Does D4 need to exist?

**NO.**

A plausible D4 candidate would be a separate `RELATION_QUALIFIED_LINKED_LIFE_UPDATE`, but that duplicates:
- D1's counterpart binding,
- D1's explicit `LINKED_LIFE_TRANSMISSION` family,
- D2's before/after rebinding.

The minimal architecture remains D1/D2/D3.

## Terminal questions

### D. Does D1 suffice?

**Yes, with mandatory relation qualification for linked-life rules.**

### E. Does D2 suffice?

**Yes.** Elder strongly validates interval/recurrent/transition/trajectory distinctions and derived turning points.

### F. Does D3 capture reciprocal/selection pathways?

**Yes, semantically.** But source uncertainty must cap causal assertion; D3 may not convert an ambiguous association into two causal updates.

### G. Is D4 needed?

**No.**

### H. Does Elder support turning point as derived rather than primitive?

**Yes.**

### I. Smallest architectural consequence?

No new top-level capability. Add/confirm one D1 linked-life schema invariant plus tests that prohibit cross-person updates without exact relation/source-transition/target-delta/time/provenance. Preserve D2's derived turning-point rule and D3's evidence-qualified gate requirement.

## Challenge verdict

`PASS__D1_D2_D3_SURVIVE_ELDER__D1_LINKED_LIFE_RELATION_TUPLE_MUST_BE_MANDATORY__NO_D4`
