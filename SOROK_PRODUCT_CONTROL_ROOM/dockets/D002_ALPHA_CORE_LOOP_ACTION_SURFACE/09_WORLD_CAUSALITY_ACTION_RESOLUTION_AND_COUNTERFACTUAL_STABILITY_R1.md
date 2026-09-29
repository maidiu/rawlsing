# D002 — World Causality, Action Resolution and Counterfactual Stability R1

Status: `PROVISIONAL_PRODUCT_LAW_INPUT__OPEN_ARCHITECTURE_QUESTIONS`

## 1. Core problem

Rawlsing must not let the narration model decide that an event happens merely because the event is plausible, dramatic, morally useful or responsive to the user's wording.

The world needs its own transition authority.

Example:

Nadia warns that the toilet chain is delicate.

If the user later flushes roughly, the chain should come loose because:
- the fixture has an admitted fragile state;
- the realized user action applies a relevant operation/force;
- the world-transition rule resolves the interaction.

It should **not** come loose because the LLM recognizes that this would create a good relational consequence.

## 2. Attempt → realized operation → world transition

A physical DO request should be decomposed into:

`USER ATTEMPT`
→ `FEASIBILITY / REQUIRED MEANS`
→ `REALIZED PHYSICAL OPERATION`
→ `OBJECT / ENVIRONMENT TRANSITION`
→ `OBSERVABLE CONSEQUENCES`

The narrator comes after the transition.

Examples:
- rough flush + fragile chain → possible detachment;
- user tries repair + available access/tools/skill → success/failure/partial repair;
- push locked door → no entry;
- pick up hot pan bare-handed → bodily consequence where modeled;
- read bill from across room → insufficient perceptual resolution rather than silent movement.

## 3. Object state and affordance

Objects that matter causally need sufficient state to support claimed behavior.

Candidate object-state families:
- location;
- ownership/control;
- open/closed/locked;
- intact/damaged;
- contents;
- relevant mechanical condition;
- temperature/power/use state;
- portability;
- visibility/accessibility.

Do not simulate arbitrary physics.

Represent only enough state to make the action surface coherent.

## 4. Deterministic versus stochastic transition

Some transitions may be effectively deterministic.

Others may require bounded uncertainty.

If stochasticity is used:
- the draw must be generated/admitted outside narration;
- it should be reproducible/replayable where necessary;
- the narrator may not reroll because an outcome is boring;
- the user's phrasing should not alter probability unless it changes the realized action.

Exact seeded/randomness law remains open.

## 5. Counterfactual stability

Equivalent world state + equivalent realized action should not yield radically different outcomes merely because:
- the prompt is worded differently;
- the narrator model samples differently;
- another outcome would create a better story.

Rawlsing need not be perfectly deterministic.

It does need **causal stability**.

## 6. No dramaturgical arbitration

Forbidden shortcut:

`USER ACTION → LLM invents a consequence that fits the character arc`

Preferred:

`USER ACTION → WORLD TRANSITION → ACTOR PERCEPTION / RESPONSE → LATER CONSEQUENCE`

The system may still generate unresolved world detail where necessary, but completion must obey the existing world/history constraints.

## 7. Social actions also require realization

The same principle applies beyond mechanics.

Example:
> I babysit her child.

This is not a primitive success statement.

It implies:
- Nadia permits/leaves the child with the user;
- the user remains present;
- child interaction occurs;
- time passes;
- user behavior is realized;
- child separately perceives/responds.

Likewise:
> I apologize.

canonically guarantees an attempted speech act if feasible, not forgiveness or successful repair.

## 8. Parser uncertainty

Natural-language action parsing may be uncertain.

The engine needs a policy for:
- harmless underspecification;
- materially ambiguous target;
- incompatible actions;
- impossible detail;
- ambiguous pronouns;
- unclear intended concurrency.

Candidate responses:
- conservative realization;
- return control with bounded ambiguity;
- request clarification only when materially necessary;
- preserve alternatives until observation resolves them.

Exact policy remains open.

## 9. Causal contribution versus sole cause

Rawlsing should resist monocausal user-credit.

The user's story may contribute to a child's aspiration.

Other causes may include:
- prior interests;
- teacher;
- media;
- family history;
- peers;
- opportunity exposure;
- developmental timing.

The causal graph should be able to represent:
- contribution;
- enabling condition;
- trigger;
- constraint;
- mediator;
- independent concurrent cause.

Avoid:
> the user caused the child's dream

when the evidence supports only:
> the user's interaction became one causal input in the trajectory.

## 10. Alpha implication

The minimum alpha does not need a general physics engine.

It needs a **bounded causal-action resolver** for the action classes the alpha actually supports.

The scenario bank should be used to identify the smallest state/transition vocabulary that makes:
- household objects;
- movement/access;
- practical help;
- damage/repair;
- money/resources;
- invitations/commitments;
- interpersonal acts;

causally credible.
