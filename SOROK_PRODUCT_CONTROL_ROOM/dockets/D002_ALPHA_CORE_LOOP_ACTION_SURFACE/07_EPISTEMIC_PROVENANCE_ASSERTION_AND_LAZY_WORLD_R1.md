# D002 — Epistemic Provenance, Assertion Types and Lazy World R1

Status: `PROVISIONAL_PRODUCT_LAW_INPUT__OPEN_ARCHITECTURE_QUESTIONS`

## 1. Why “narrated fact becomes reality” needs typing

The binding-reality law must distinguish **what kind of statement occurred**.

Not every sentence displayed to the user is an objective-world assertion.

Examples:

Narrator:
> There is a red electricity bill under the magnet.

This may assert an objective perceptible fact.

Nadia:
> “I've paid that already.”

This canonically establishes that Nadia **said** she paid it.

It does not necessarily establish that the bill was actually paid.

User inference:
> She must be broke.

This establishes, at most, a user hypothesis.

It does not establish Nadia's financial state.

## 2. Required assertion classes

At minimum, investigate distinct records for:

### Objective narrator observation
A lawfully accessible surface fact grounded in admitted world state.

### Actor testimony
A canonical speech act whose propositional content may be:
- true;
- false;
- mistaken;
- incomplete;
- deceptive;
- unverifiable.

### User observation
What the user actually perceived.

### User hypothesis / inference
What the user concludes from evidence.

### Actor belief
What an actor believes, whether or not true.

### System-analytic truth
Objective/hidden state available to causal machinery but not necessarily any actor.

These must not silently promote into one another.

## 3. User knowledge needs provenance

The system should distinguish:
- seen directly;
- heard directly;
- told by Nadia;
- told by someone else;
- read from an object;
- inferred;
- assumed;
- remembered;
- forgotten;
- contradicted;
- later reinterpreted.

This matters for both:
- user assistance/memory UX;
- later player-model analysis.

An assisted Rawlsing mode may resurface:
> Nadia told you she went to Rome.

It should not rewrite that as:
> Nadia went to Rome.

unless the proposition has independent objective authority.

## 4. Narrator must not canonicalize user inference

If the user asks:

> So she's poor?

the narrator should not convert the inference into fact merely because evidence points that way.

It may return additional available evidence or state that the requested conclusion is not directly knowable from the current surface.

Likewise:
> Is she annoyed?

should return observable evidence, not hidden-state confirmation.

## 5. Ontically unresolved ≠ absent

A detail not yet materialized in storage is not necessarily absent from the world.

Example:
The exact contents of a kitchen drawer may never have been computed because no event required them.

If later inspection requires resolution, the implementation may lawfully complete the detail.

But from the diegetic perspective, the drawer did not come into existence when the user looked.

Thus distinguish:
- `NOT_MATERIALIZED_YET` implementation state;
- `ABSENT` in-world state;
- `PRESENT_BUT_UNOBSERVED` in-world state.

The user should never see implementation laziness as ontological popping-in.

## 6. Lazy completion must be history-compatible

A newly materialized detail must not contradict:
- previously narrated facts;
- prior object use;
- actor memories already admitted;
- material constraints;
- earlier events;
- established schedules/ownership;
- causal consequences.

If Nadia previously used a specific pan from a cabinet, later cabinet completion cannot decide that the household owns no pans.

## 7. Actor knowledge can force completion before user observation

The user is not the only reason the world becomes specific.

If Nadia:
- opens a drawer;
- uses an object;
- refers to a document;
- remembers a place;
- texts someone;

the relevant world/actor fact may need lawful completion/admission even if the user never inspects it.

World specificity follows causal need, not user curiosity alone.

## 8. Effective-time law

When lazy completion determines a fact that must already have been true before observation, persistence machinery needs a lawful way to represent its temporal status.

Example:
The Myrtle Beach magnet is first inspected on day 30, but it has been on the fridge since before the user met Nadia.

The engine must not treat:
`first materialized at day 30`
as equivalent to:
`came into existence at day 30`.

Exact implementation is open:
- seeded latent facts;
- constraint-driven backdated effective time;
- pre-generated object layer;
- another replay-safe mechanism.

## 9. No retroactive convenience

Lazy completion may fill an unresolved gap.

It may not rewrite a settled past merely because a later story would be more interesting.

The later meaning of an old object may change.

The object's established historical facts may not be silently retconned.

## 10. D001 implication

The relational ontology needs explicit epistemic/provenance objects sufficient to keep apart:
- truth;
- utterance;
- belief;
- perception;
- inference;
- memory;
- narration.

Otherwise the hard epistemic wall will collapse through storage even if the prose narrator behaves correctly.
