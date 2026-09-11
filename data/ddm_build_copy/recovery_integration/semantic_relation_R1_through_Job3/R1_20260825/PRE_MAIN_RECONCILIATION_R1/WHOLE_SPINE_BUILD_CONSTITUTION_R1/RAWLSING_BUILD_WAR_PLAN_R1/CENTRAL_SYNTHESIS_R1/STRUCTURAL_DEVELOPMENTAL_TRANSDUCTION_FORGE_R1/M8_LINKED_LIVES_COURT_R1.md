# M8 — LINKED LIVES COURT R1

## Issue

Does frozen-candidate D1 (`TYPED_ACTOR_RELATIVE_SOCIAL_ECOLOGY_DERIVATION`) adequately represent person-to-person transduction, or does Elder require a new capability?

## Elder's strongest linked-life mechanism

The clearest chain is not psychological contagion. It is a material-relational transfer of workload and obligation:

```text
family economic loss
→ mother's paid-employment transition and/or father's work incapacity/absence
→ parental time/resource/contribution pattern changes
→ household task requirement remains or grows
→ child is assigned/assumes specific domestic/economic responsibility
→ child repeatedly performs the activity
→ child's time, dependence, authority relations, counterpart set and opportunities change
→ later development is conditioned through those realized activities
```

Source basis: pp. 62, 67–70, 114–115.

Page 67 is especially probative: Elder says change in parental roles **typically preceded** a shift in responsibilities to children. Page 69 explicitly treats mother's role change as an example of family interdependence: change in mother's role initiates change in children's household role.

A second linked-life chain concerns father:

```text
father unemployment/status loss
→ altered contribution/authority and, in some cases, withdrawal/distress
→ changed marital power / paternal control / paternal availability
→ child's actual parent relation changes
→ child's use of mother, peers, teachers, and other adults changes
```

Source basis: ch. 5, especially pp. 95–106, with substantial evidence ceilings.

## D1 hostile test

Frozen D1 already requires:

- exact actor binding;
- exact position binding;
- counterpart/household/institution binding where relational;
- a typed mechanism rule;
- history where applicable;
- typed Stage-A and Stage-B social facts;
- `LINKED_LIFE_TRANSMISSION` as an admitted mechanism family;
- an explicit example: linked person's transition + dependency relation → focal actor resource/time/obligation update applicability.

That is the correct jurisdiction.

### Failure mode if D1 is implemented too loosely

A generic representation such as:

```text
PARENT_JOB_LOSS
→ CHILD_STRESS
```

would be unlawful even if empirically correlated. Elder requires at least:

```text
SOURCE_ACTOR = father
SOURCE_REALIZED_STATE/TRANSITION = unemployment/job loss
RELATION = father-of / provider-in household H
HOUSEHOLD_RESOURCE/ROLE CONSEQUENCE = specified
TARGET_ACTOR = child C
TARGET ECOLOGY DIMENSION = time/resource/obligation/authority/support/etc.
REALIZATION = exact child activity/relation if it occurred
TIME/INTERVAL = explicit
PROVENANCE = source evidence
```

The linked person is not just provenance metadata; the relation is part of the causal rule.

## Is a separate relation-qualified D4 required?

**No.**

Elder requires a **relation-qualified invariant inside D1**, not a fourth capability. The frozen candidate already has the necessary semantic hooks. Adding a separate `D4_LINKED_LIFE` would duplicate D1's counterpart/relation binding and its explicit `LINKED_LIFE_TRANSMISSION` family.

The required narrowing is implementation-level:

> A D1 linked-life derivation MUST NOT emit a target-actor update from another person's state unless the rule carries `(source_actor, target_actor, exact_relation/household binding, source realized state/transition, target ecology dimension, valid interval, realization status, provenance)`.

If a source transition changes several target dimensions across time, D1 composes with D2's transition rebinding.

## Relation to D2

Linked life is often temporal rebinding:

```text
mother begins paid work at t
→ prior household labor allocation deactivates/modifies
→ child obligation activates at t/t+1
→ recurrent domestic activity persists over interval
```

That is not a new causal family; it is D1 mechanism + D2 temporal realization.

## Relation to D3

Most Elder household-linked-life mechanisms do **not** require D3. D3 should be reserved for cases where an actor's realized action encounters an external counterpart/institutional gate and changes later social-world facts.

Example where D3 may apply:

```text
boy seeks job
→ employer gate hires him
→ new wage/resource + employer relation
→ later household/child ecology changes
```

But if the source cannot distinguish whether preexisting independence caused job acquisition or job experience caused independence, D3 must preserve that identification uncertainty rather than assert both arrows.

## Court answer B

**Strongest linked-life mechanism:** parent work/resource transition → household labor/resource reallocation → child obligation/activity → changed child time/resource/authority/counterpart ecology.

## Court answer D

**D1 suffices semantically, provided relation qualification is mandatory.** No D4 is needed.

## Smallest architectural consequence

Add no new top-level capability. Tighten the D1 mechanism-rule schema/tests so linked-life transmissions cannot be expressed without exact source actor, target actor, binding relation, source realized condition/transition, time, target ecology delta, and provenance.
