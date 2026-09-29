# Sorok Interaction Ideation Completeness Audit R4

Status: `COMPLETENESS_AUDIT__R4__PASS_WITH_CAUSAL_MECHANICS_CORRECTIONS`

Date: 2026-09-29

Purpose: perform a fourth independent pass over the interaction ideation, now targeting causal-mechanics gaps rather than missing UX/epistemic concepts.

## 1. R4 result

R3 established:
- player embodiment;
- lawful access;
- epistemic provenance;
- lazy-world consistency;
- concurrency;
- control return;
- third-party independence.

R4 found the next deeper layer:

**the corpus still needed a stricter account of who/what actually determines physical outcomes, how each actor perceives an event, how private appraisal differs from outward presentation, how actor memory differs from event history, and how delayed effects retain causal provenance without turning the player into the protagonist of everything.**

R4 therefore adds/clarifies:
- world/object transition authority;
- causal stability;
- bounded object affordance/state;
- parser uncertainty;
- actor-specific sensory packets;
- finite actor attention;
- internal response versus outward expression;
- partial self-access;
- selective memory / forgetting / reconsolidation;
- pattern-confidence and counterevidence;
- causal lineage across delayed consequences;
- actual causation versus actor attribution;
- multi-causal contribution;
- anti-user-credit law;
- non-teleological event generation;
- no guaranteed moral legibility.

## 2. Physical outcome authority — PREVIOUSLY UNDER-SPECIFIED / NOW BANKED

### Problem
The toilet-chain example assumes:
- the chain is fragile;
- the user flushes roughly;
- the chain comes loose.

Without explicit transition authority, the LLM could make the chain break simply because that outcome is narratively useful.

### R4 law
Physical/world outcomes should be resolved from:
`ADMITTED STATE + REALIZED OPERATION + GOVERNING TRANSITION RULE`

Narration comes after.

### Home
D002 `09_WORLD_CAUSALITY_ACTION_RESOLUTION_AND_COUNTERFACTUAL_STABILITY_R1.md`
SCE-027
SPD-0040
RISK-038

## 3. Counterfactual / causal stability — NEW EXPLICIT REQUIREMENT

Equivalent world state + equivalent realized action should not radically change outcome because:
- wording changed;
- narrator sample changed;
- another result would be more dramatic.

Rawlsing may use bounded stochasticity, but the stochasticity itself must be governed and not rerolled for story quality.

### Home
world-causality file
SPD-0041
Q-RAND-001
RISK-039

## 4. Bounded object state — NEW EXPLICIT REQUIREMENT

The product does not need a universal physics engine.

It does need enough object state for the action classes it claims to simulate:
- open/closed/locked;
- intact/damaged;
- contents;
- relevant mechanical condition;
- location;
- portability;
- ownership/control;
- temperature/power/use where necessary.

### Home
Q-PHYS-001
world-causality file

## 5. Natural-language ambiguity — NEW REGISTERED QUESTION

The parser must not confidently invent a materially consequential target or action where the user's language is genuinely ambiguous.

Possible policies remain open:
- bounded clarification;
- conservative realization;
- preserve alternatives;
- fail closed.

### Home
Q-PARSER-002
SCE-034
RISK-046

## 6. Actor-specific perception packets — PREVIOUSLY IMPLIED / NOW EXPLICIT

### Problem
Objective event cannot be directly handed in full to every actor.

Example:
Nadia may hear:
- cabinet noise;
- shouted speech;

without knowing:
- exact cabinet;
- exact touched bottle;
- full visual detail.

### Required path
`OBJECTIVE EVENT → SENSORY ACCESS → ATTENTIONAL UPTAKE → APPRAISAL`

### Home
D002 `10_ACTOR_PERCEPTION_APPRAISAL_EXPRESSION_AND_MEMORY_R1.md`
SCE-028 / SCE-035
SPD-0042
Q-PERCEPT-001
RISK-040

## 7. Finite actor attention — NEW EXPLICIT LAW

Nadia is not an omnidirectional recorder.

Current task and competing stimuli may cause:
- half-hearing;
- delayed noticing;
- missing a glance;
- ignoring low-salience input;
- prioritizing child/pot/phone/work.

### Home
actor-perception file
SPD-0043
Q-ATTNACTOR-001

## 8. Internal response versus outward presentation — STRONGER / NOW EXPLICIT

### Example
Nadia may simultaneously:
- feel annoyed;
- believe the user probably forgot;
- appreciate forthrightness;
- choose not to escalate;
- outwardly reassure them.

The user sees only the outward surface.

### Home
actor-perception file
SCE-029
SPD-0044
Q-EXPR-002
RISK-041

## 9. Partial self-access — NEWLY EXPLICIT

The persona need not be perfectly introspectively transparent to themselves.

A person may:
- know they are irritated but not fully know why;
- consciously forgive while a weak pattern trace remains;
- later recognize an accumulated pattern;
- misattribute a feeling.

This is a bounded design possibility, not permission for arbitrary hidden psychology.

### Home
actor-perception file

## 10. Actor memory versus event history — PREVIOUSLY TOO COARSE / NOW BANKED

Objective event history is not the same as what a person remembers.

Actor memory may:
- fade;
- retain gist;
- lose detail;
- be reactivated;
- reconsolidate;
- be reinterpreted.

### Home
actor-perception file
SCE-030
SPD-0045
Q-MEM-002
RISK-042

## 11. Pattern hypotheses need confidence and counterevidence — NOW EXPLICIT

A hypothesis such as:
> this user does not listen to practical instructions

should support:
- weak evidence;
- context specificity;
- confidence increase;
- counterevidence;
- decay;
- possible later weakening.

This preserves the user's toilet-chain example without turning one incident into a trait flag.

## 12. Causal provenance — PREVIOUSLY INCOMPLETE / NOW BANKED

Chronological event order is not enough.

The system needs enough causal lineage to distinguish:
- caused;
- contributed;
- enabled;
- triggered;
- mediated;
- constrained;
- amplified;
- attenuated;

at whatever grain the alpha actually needs.

### Home
D002 `11_CAUSAL_PROVENANCE_DELAYED_EFFECTS_AND_NONTELEOLOGICAL_WORLD_R1.md`
SCE-036
SPD-0046
Q-CAUSAL-001
RISK-043

## 13. Actual causation versus attribution — STRONGER / NOW EXPLICIT

The theft example may contain:
- actual theft → missing cash → Nadia suspicion → argument;
- Nadia belief: Samir stole it;
- Samir belief: Nadia never trusts me;
- user knowledge: I took it.

All can coexist.

Causal provenance and actor belief remain separate.

## 14. Multi-causality / anti-user-credit — NEW EXPLICIT LAW

The child may become ambitious because of:
- user stories;
- teacher;
- preexisting interest;
- media;
- peers;
- opportunity.

The user may be one contributor rather than sole cause.

Rawlsing should not over-credit the player merely because the player action is the narratively visible one.

### Home
world-causality file
causal-provenance file
SCE-031 / SCE-033
SPD-0047
Q-MULTICAUSE-001
RISK-044

## 15. Third-party processing fan-out — STRONGER / NOW EXPLICIT

If a joke/event reaches:
- Nadia;
- child;
- guest;

each receives independent:
- sensory access;
- uptake;
- appraisal;
- memory;
- later action.

Third parties are not merely scalar effects on Nadia.

### Home
actor-perception file
SCE-035
SPD-0049

## 16. Non-teleological world generation — NEW EXPLICIT LAW

### Problem
Even with independent personas, a product could still secretly manufacture:
- crises;
- moral tests;
- drama;
- neediness;

because engagement is low or because the system wants to teach the user something.

That would undermine the “live life” premise.

### R4 law
World events should arise from:
- actor projects;
- obligations;
- institutions;
- material constraints;
- schedules;
- relationships;
- prior consequences;
- governed stochasticity.

Not from:
- “test kindness”;
- “teach lesson”;
- “relationship needs drama”;
- “increase retention.”

### Home
causal-provenance/non-teleological file
SCE-032
SPD-0048
Q-WORLDEV-001
RISK-045

## 17. No guaranteed moral legibility — NOW EXPLICIT

The user may never learn:
- whether an action mattered;
- why someone withdrew;
- what happened downstream;
- what caused a later change.

The world does not owe the player a moral accounting.

Retrospective feedback, if later designed, is a separate product layer.

## 18. Flourishing impact cannot assume clean causal credit — NEW D003 CONSTRAINT

A health/flourishing system must not automatically debit/credit every later person-state change to the user.

It should distinguish:
- user action;
- demonstrable contribution;
- repeated praxis;
- multi-causal world change;
- unresolved causal weight.

This is now registered through Q-MULTICAUSE-001 and the causal-provenance law.

## 19. Scenario coverage added

R4 extends the scenario bank through SCE-036:
- fragile chain mechanics;
- half-heard cabinet event;
- magnanimity over private annoyance;
- memory fade/reactivation;
- multi-causal child aspiration;
- institution-caused event with no moral function;
- user falsely believes they caused change;
- ambiguous action parse;
- actor-specific processing fan-out;
- delayed causal chain with no user feedback.

## 20. Remaining genuine work after R4

The remaining frontier is increasingly implementation/design rather than memory recovery:

1. minimal object-state/transition system;
2. deterministic/seeded stochasticity law;
3. action-parser ambiguity policy;
4. actor perception packet schema;
5. finite actor-attention model;
6. CAN-008/PFF internal-response-to-expression ownership;
7. actor memory/significance model;
8. causal provenance representation;
9. multi-causal contribution model;
10. independent world-event generation;
11. all prior R3/R2 open contracts;
12. exact D001 ownership table;
13. D003 flourishing constitution;
14. alpha prototype proving these laws can be fun rather than merely correct.

## 21. Audit result

`R4_COMPLETENESS = PASS_WITH_CAUSAL_MECHANICS_CORRECTIONS_APPLIED`

No known major concept from the current interaction ideation remains only in chat.

R4's contribution is that Rawlsing now has an explicit design obligation for **causal authority**:
the world determines what happens, each actor separately determines what they perceive/process, and narration reports only the lawful surface.
