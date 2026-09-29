# Sorok Interaction Ideation Completeness Audit R3

Status: `COMPLETENESS_AUDIT__R3__PASS_WITH_ADDITIONAL_GAPS_CORRECTED`

Date: 2026-09-29

Purpose: perform a third independent completeness pass over the interaction/product ideation and identify concepts still only implicit after R2.

## 1. R3 result

R2 captured the explicit interaction laws well, but R3 found a deeper missing layer:

**the simulation had not yet adequately specified the user's own diegetic presence, the provenance of displayed claims, or the mechanics by which a partially observed world remains coherent before/after observation.**

R3 therefore adds/clarifies:
- player embodiment and world position;
- lawful encounter/access;
- player resources/capabilities;
- ATTEND not silently performing DO;
- typed epistemic assertions;
- user-knowledge provenance;
- lazy-world versus diegetic existence;
- history-compatible world completion;
- baseline scene framing;
- ambient versus focused perception;
- concurrent SAY/DO/ATTEND;
- interruptible observation;
- partial information and control return;
- sufficient third-party actor independence;
- future cross-language interaction question;
- retry/save semantics as an explicitly deferred product question.

## 2. Player embodiment — PREVIOUSLY UNDER-SPECIFIED / NOW BANKED

### Problem
The examples assume the user can:
- stand in a kitchen;
- move toward a bathroom;
- sit next to a child;
- read a bill;
- pick up objects;
- offer transport/resources.

Without player world-state, DO/ATTEND can silently become omnipotent prose.

### R3 law
“No avatar” does not mean “disembodied.”

A physical scene requires enough player-presence state to govern:
- position;
- sensory access;
- reach;
- possessions/resources;
- action affordance;
- what other actors can perceive about the user.

### Home
D002 `06_PLAYER_EMBODIMENT_ENTRY_AND_AFFORDANCE_R1.md`
SPD-0030 / SPD-0039
RISK-029 / RISK-036

## 3. ATTEND may not smuggle physical action — NEW EXPLICIT LAW

### Example
From six feet away:
> What exactly does the bill say?

must not silently move the user closer.

Possible answer:
> You can make out the utility logo and a red mark, but not the smaller print from here.

If the user wants more:
> I step closer and read it.

### Home
Player-embodiment file
SCE-016
SPD-0032

## 4. Random person versus lawful access — PREVIOUSLY MISSING / NOW BANKED

### Problem
“Unchosen neighbor” does not justify magical presence inside a stranger's apartment.

### R3 distinction
Keep separate:
- non-selected person;
- causal encounter route;
- current relationship role;
- current physical/social permission.

A later home scene must have been earned/caused by relationship history.

### Home
Player-embodiment file
SCE-017
SPD-0031
Q-ENTRY-001
RISK-030

## 5. Player resources and capabilities — PREVIOUSLY MISSING / NOW BANKED

User prose cannot create:
- a car;
- $500;
- repair tools;
- physical skill;
- access credentials;

merely by saying:
> I drive her.
> I pay it.
> I fix it.

Exact player-resource modeling remains open.

### Home
Player-embodiment file
SCE-023
SPD-0039
Q-PLAYERRES-001

## 6. Typed displayed claims — PREVIOUSLY INSUFFICIENT / NOW BANKED

### Problem
“Anything the LLM says becomes binding reality” needs a precise boundary.

Narrator:
> There is a bill on the refrigerator.

may establish an objective surface fact.

Nadia:
> “I paid that already.”

establishes that Nadia said it—not necessarily that payment happened.

User:
> She must be broke.

is an inference—not objective truth.

### Required distinction
At minimum:
- objective narrator observation;
- actor testimony;
- user observation;
- user inference;
- actor belief;
- system-analytic truth.

### Home
D002 `07_EPISTEMIC_PROVENANCE_ASSERTION_AND_LAZY_WORLD_R1.md`
SCE-018
SPD-0033
Q-ASSERT-001 / Q-KNOW-001
RISK-031 / RISK-037

## 7. User knowledge provenance — NEW EXPLICIT REQUIREMENT

The system should know whether a claim was:
- directly seen;
- heard;
- told by Nadia;
- told by another actor;
- read;
- inferred;
- assumed;
- remembered;
- contradicted;
- later reinterpreted.

Assisted memory must preserve provenance.

Bad:
> Nadia went to Rome.

When the only authority is testimony:
> Nadia told you she went to Rome.

This is necessary for lying, error and uncertainty to remain real.

## 8. Lazy completion versus in-world absence — NEW EXPLICIT REQUIREMENT

### Problem
The implementation may not have materialized every drawer/object/fact.

That does not mean the world lacked those things before inspection.

### Required distinction
- implementation `NOT_MATERIALIZED_YET`;
- diegetic `ABSENT`;
- diegetic `PRESENT_BUT_UNOBSERVED`.

### Law
Lazy completion must be compatible with:
- prior narration;
- actor use;
- actor memories;
- material constraints;
- earlier events;
- effective time.

### Home
Epistemic/lazy-world file
SCE-019
SPD-0034
Q-LAZY-001
RISK-032

## 9. World specificity is not user-centered — NEW EXPLICIT DETAIL

The world may need to become specific because Nadia or another actor interacts with something before the user observes it.

User curiosity is not the sole materialization trigger.

This follows the broader non-player-centricity law.

## 10. Baseline scene frame — PREVIOUSLY MISSING / NOW BANKED

### Problem
A hard phenomenological narrator can become unusably sparse.

The user should not have to ask:
- what room am I in?
- is Nadia visible?
- is the child here?
- is she cooking?

when these would be immediately obvious.

### R3 model
Distinguish:
- **ambient coarse perception**;
- **focused ATTEND**.

Scene entry gives enough immediately perceptible information to orient and act.

Focused ATTEND gives additional resolution.

### Home
D002 `08_SCENE_FRAME_CONCURRENCY_INTERRUPTION_AND_CONTROL_RETURN_R1.md`
SCE-022
SPD-0035
Q-SCENE-001
RISK-033

## 11. Concurrency — PREVIOUSLY PARTLY IMPLIED / NOW EXPLICIT

The Rome-cover example requires actual overlap:

`SAY + ATTEND + attempted presentation`

not:
`complete speech → separately inspect bill`.

Concurrent actions share:
- time;
- gaze;
- hands;
- posture;
- attention.

Not every combination is compatible.

### Home
Scene/concurrency file
SCE-020 / SCE-026
SPD-0036
Q-CONCUR-001
RISK-034

## 12. ATTEND is interruptible — NEW EXPLICIT LAW

A long observation may be interrupted by:
- speech;
- another actor;
- moving target;
- boiling pot;
- phone;
- user choice to stop.

The user can receive partial information.

### Home
Scene/concurrency file
SCE-021
SPD-0037

## 13. Control-return cadence — NEW OPEN UX QUESTION

The system should return control when:
- an action completes;
- a new observation changes the decision surface;
- another actor intervenes;
- feasibility fails;
- interruption occurs;
- continuing requires a new user decision.

Exact granularity is not yet settled.

### Home
Q-CONTROL-001
Scene/concurrency file

## 14. Third-party actor independence — PREVIOUSLY IMPLIED / NOW EXPLICIT

The child in the aspirational-babysitting example cannot merely be a puppet generating Nadia consequences.

If the simulation claims:
- changed aspirations;
- remembered stories;
- later behavior;
- conflict with Nadia;

then the child needs sufficient independent actor state for that causal scope.

### Home
SCE-024
SPD-0038
Q-THIRDPARTY-001
RISK-035

## 15. Cross-language interaction — NEW REGISTERED QUESTION

The project's cross-cultural purpose makes language a real future requirement.

R3 does not decide translation mechanics.

It registers:
- literal translation;
- dialect/register;
- honorifics;
- indirectness;
- pragmatic misunderstanding;
- whether translation is diegetic/UI/absent.

### Home
Q-LANG-001
player-embodiment file

## 16. Retry / undo / save-scumming — NEW DEFERRED QUESTION

If users can freely replay every branch, contingency and consequence may collapse into optimization.

If there is no retry/undo at all, experimentation may become punitive.

R3 registers this as a P2 product/UX question, not current law.

### Home
Q-RETRY-001

## 17. Scenario coverage added

R3 extends the scenario bank through SCE-026 with:
- too-far-to-read;
- lawful access to home;
- actor testimony versus truth;
- lazy drawer consistency;
- simultaneous cover;
- interrupted reading;
- initial scene frame;
- conjured car;
- child as independent actor;
- no bespoke reaction;
- verbose prompt packing.

## 18. Remaining unknowns after R3

The remaining gaps are now primarily genuine design/architecture work:

1. exact player-presence schema;
2. user identity/privacy policy;
3. exact encounter-generation law;
4. player inventory/resource model;
5. language mediation;
6. epistemic/provenance schema;
7. lazy-world/effective-time implementation;
8. ambient-perception algorithm;
9. concurrency/resource model;
10. control-return cadence;
11. third-party actor fidelity strategy;
12. save/retry semantics;
13. prior R2 questions: duration, salience, action ontology, V3/PFF promotion, flourishing.

## 19. Audit result

`R3_COMPLETENESS = PASS_WITH_ADDITIONAL_CORRECTIONS_APPLIED`

No known major concept from the current interaction ideation remains only in chat.

R3's major contribution is that the interaction design now has not only:
- a person/world;
- a narrator;
- causal consequences;

but also a disciplined account of **the user's presence inside that world and the epistemic status of what the interface says**.
