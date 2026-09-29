# Sorok Interaction Ideation Completeness Audit R2

Status: `COMPLETENESS_AUDIT__R2__PASS_WITH_GAPS_CORRECTED`

Date: 2026-09-29

Purpose: verify that the substantive product/interaction ideas developed in the initial Sorok ideation session are durably serialized, correctly scoped, and not dependent on chat memory.

This is a coverage audit, not a new product-law source. Where the audit identified missing or stale representation, the relevant canonical/provisional Sorok files were corrected separately.

## 1. Audit method

For each salient concept from the ideation sequence, verify:
1. a durable repository home exists;
2. the representation preserves the intended distinction;
3. the concept is classified as provisional law, open question, risk, scenario probe or architecture inheritance rather than flattened into one status;
4. no stale file quietly contradicts the corrected architecture.

## 2. Product-interaction thesis — COVERED

### Idea
The user is dropped into the middle of another person's already-running life rather than entering an empty chatbot chamber.

The person has:
- independent daily pressures;
- needs;
- obligations;
- other relationships;
- ongoing events;
- constraints;
- tasks unrelated to the user.

The user may enter those circumstances and intervene.

### Home
- `08_INTERACTION_SYSTEM_SYNTHESIS_R1.md`
- D002 `01_INTERACTION_CONSTITUTION_R1.md`

### R2 correction
Made explicit that the world/persona are **non-player-centric** and do not owe the user a reaction.

## 3. SAY / DO / ATTEND — COVERED

### Idea
The user can:
- say things;
- attempt embodied actions;
- request more perceptible information about the scene.

### Home
- D002 interaction constitution
- top-level synthesis

### R2 correction
Added an explicit interface-channel law:
- narrator-directed “What's on the fridge?” = ATTEND;
- “I ask Nadia, ‘What's on your fridge?’” = SAY.

Observation requests must not accidentally become diegetic speech.

## 4. Hard surface-only epistemics — COVERED

### Idea
The user receives no access to another person's mind.

Narration should report objective/perceptible details without telling the user:
- that Nadia is annoyed;
- that she is trying to be polite;
- what she really means;
- whether she is lying;
- what hidden state is active.

### Home
- D002 interaction constitution
- reciprocal-observation file
- non-curatorial-world file
- decision SPD-0011
- risk RISK-016

### Coverage quality
Strong.

## 5. Show-not-tell / no suggestive hinting — COVERED

### Idea
Even when hidden state is known, the narrator must not leak it through suggestive prose.

“Her answer is curt” may already over-interpret.
Prefer:
- literal words;
- timing;
- gaze;
- movement;
- task continuation;
- physically observable facts.

### Home
- interaction constitution
- SCE-011 polite annoyance
- non-curatorial-world law

### R2 correction
Added distinction between **perceptual salience** and **hidden psychological salience** so the narrator can still choose finite details without covertly hinting.

## 6. Four simultaneous operational views — CORRECTED / NOW COVERED

### Idea
Interaction reasoning needs the simultaneous distinction:
1. objective world;
2. actor-private state;
3. relational/distributed-knowledge state;
4. user phenomenal surface.

### Prior gap
Previously implicit across multiple documents but not stated as one operational view-set.

### R2 home
D002 interaction constitution §15.

### Important guardrail
These are views, not replacements for the inherited SDTF / durable V3 / CAN-008 / PFF / V2 owner architecture.

## 7. Existing V3 temporal-grain architecture — COVERED AND STALE CONTRADICTION FIXED

### Idea
Do not invent one generic “live V3.”

Preserve the already-developed distinction:
- SDTF/upstream transduction;
- many-recursion durable/formative V3;
- CAN-008 person×event immediate response;
- PFF interaction-fast/session/user-opacity state;
- V2 expression.

### Prior problem
The original D002 event pipeline still contained the stale generic:
`PERSON-STATE RECURSION → DYAD / NETWORK RECURSION`.

### R2 correction
Replaced with:
`PERCEPTION FAN-OUT`
→ `CAN-008 PERSON×EVENT RECEIVABILITY / UPTAKE / APPRAISAL / IMMEDIATE RESPONSE`
→ `PFF INTERACTION-FAST / SESSION / USER-OPACITY STATE`
→ `ACTOR ACTION PROPOSAL + CAUSAL ADMISSION`
→ `OPTIONAL DURABLE-V3 PROMOTION`
→ `WORLD / NETWORK CONSEQUENCE`
→ `V2 / NARRATOR USER-PERCEPTIBLE SURFACE`.

### Home
- D001 inherited temporal-grain architecture
- corrected D002 interaction constitution
- current-system crosswalk
- decision SPD-0024
- risk RISK-022

## 8. User controls attempt, not reality — COVERED

### Idea
The user can specify:
- action;
- words;
- gesture;
- attempted tone;
- presentation;
- concealment;
- intention.

The user cannot specify:
- feasibility;
- interruption;
- success;
- whether Nadia notices;
- whether Nadia believes;
- what Nadia thinks it means;
- downstream impact.

### Home
- interaction constitution
- reciprocal observation
- scenario bank
- SPD-0010 / SPD-0018

## 9. Player-private intention vs impact — CORRECTED / NOW EXPLICIT

### Idea
Rawlsing needs to distinguish:
- user intention;
- outward behavior;
- persona inference;
- later user claims.

The user may:
- genuinely forget;
- knowingly ignore;
- pretend to forget;
- attempt remorse without feeling it.

Nadia can be wrong about the user's actual intention.

### Prior gap
Intention/impact separation existed, but player-private intention and possible deception were not sufficiently explicit.

### R2 home
Interaction constitution §18.

### Open issue retained
When does user-declared intention become binding player-private state, and how do we prevent retroactive self-exonerating rewrites?

## 10. Compound actions are plans, not scripts — COVERED

### Idea
“I enter the bathroom, open the cabinet, search it...” is not guaranteed execution.

Possible interruption:
- occupied bathroom;
- locked door;
- Nadia stops user;
- another event occurs;
- object state differs;
- action fails.

### Home
- interaction constitution
- SCE-001
- SCE-012

## 11. Bathroom / toilet-chain relational example — COVERED

### Idea
Nadia may have idiosyncratic bathroom/privacy habits.

She may warn about a sensitive toilet chain.

If user ignores/forgets:
- chain may detach;
- repair can succeed/fail;
- user may disclose/hide;
- delivery/tone matters;
- Nadia may perform magnanimity while privately annoyed;
- one event may remain a weak datum;
- later events may reactivate it into a pattern.

### Home
- SCE-002
- pattern-memory section in interaction constitution

### Coverage quality
Strong.

## 12. Pattern formation rather than scalar punishment — COVERED

### Idea
Do not model:
`BROKE TOILET AFTER WARNING → TRUST -4`

Model:
- episodic memory;
- salience;
- provisional hypotheses;
- confidence;
- reactivation;
- later consolidation or weakening.

Past occurrence remains fixed while meaning changes.

### Home
- interaction constitution
- D001 inherited temporal architecture
- current state

## 13. Consequence ≠ feedback — COVERED

### Idea
Effects can occur in the world without being surfaced to the user.

Examples:
- theft leads to Nadia blaming Samir;
- family conflict occurs outside user perception;
- anonymous helpful action improves life without relational reward.

### Home
- interaction constitution
- SCE-005 / SCE-006
- SPD-0014

## 14. Intention / impact / actor-specific outcome — COVERED

### Idea
The babysitting example can simultaneously produce:
- practical relief;
- child joy;
- wider aspiration;
- Nadia material anxiety;
- frustration at user influence;
- possible long-run child benefit.

There is no single action valence.

### Home
- interaction constitution
- SCE-004
- SPD-0013

## 15. World completion and binding narrated reality — COVERED

### Idea
User wording does not instantiate reality.

If the narrator says an object/fact exists, it becomes persistent reality.

The user's mention of Percocet creates nothing.

### Home
- interaction constitution
- non-curatorial-world file
- SPD-0012
- RISK-019
- Q-WCOMP-001

### Coverage quality
Strong.

## 16. Query-invariant / anti-summoning reality — COVERED AS OPEN IMPLEMENTATION QUESTION

### Idea
Different phrasings should not cause different convenient worlds.

Unresolved detail must be completed from:
- existing world/history;
- constraints;
- lawful seeded mechanism;
- accepted future completion law.

### Home
- non-curatorial-world file
- Q-WCOMP-001
- RISK-019

## 17. Ordinary objects as dense social evidence — COVERED

### Idea
Fridge contents are not meaningless atmosphere.

Bills, school menus, takeout menus and magnets can support inference about:
- SES/material strain;
- household administration;
- school context;
- food practice;
- budget;
- taste;
- travel;
- family history;
- cultural belonging.

### Home
- non-curatorial-world file
- SCE-007–010
- SPD-0021

## 18. Non-curatorial narration — COVERED

### Idea
The world contains meaningful objects because the world caused them to exist, not because a storyteller planted clues.

The narrator must not say:
> sentimental Myrtle Beach magnet

merely because the engine knows its history.

### Home
- non-curatorial-world file
- SCE-010
- SPD-0019
- RISK-017

## 19. Progressive perceptual resolution — COVERED

### Idea
“What's on the fridge?” gives coarse available detail.

More specific inspection can reveal:
- exact company;
- amount;
- due date;
- school;
- handwriting;
- restaurant;
- prices;
- magnet identity.

### Home
- non-curatorial-world file
- temporal-attention file

## 20. Observation consumes variable time — COVERED AND R2-STRENGTHENED

### Idea
Different observation/action requests consume different amounts of continuous simulated time.

A glance should not cost an hour.

Deep inspection costs more.

### Home
- temporal-attention file
- SPD-0015 / SPD-0016

### R2 correction
Added:
- duration proportionality;
- no punitive time tax;
- cumulative micro-time;
- verbose prompts do not magically alter or compress time.

## 21. Time should ordinarily remain partially opaque — COVERED

### Idea
The user should not ordinarily see:
`READ BILL: 18.4 seconds`

The simulation may know exact enough causal time while user knowledge comes from:
- clocks;
- watches;
- phones;
- speech;
- rough passage.

### Home
- temporal-attention file
- SPD-0016
- RISK-021

## 22. Time pressure makes attention inferential — COVERED

### Idea
The user cannot exhaust every possible detail.

They have to decide:
- what matters;
- what they need to know;
- when they know enough to act;
- what remains unknown.

### Home
- temporal-attention file
- top-level synthesis
- SPD-0020

## 23. No artificial observation quota — CORRECTED / NOW COVERED

### Idea
The user may keep asking for information if it remains available.

Scarcity should come from:
- elapsed time;
- interruption;
- access;
- social visibility;
- privacy;
- opportunity cost.

Not “three inspections per scene.”

### R2 home
Interaction constitution §20.

## 24. Observer is observable — COVERED

### Idea
Looking at Nadia's fridge while she stands beside you is different from doing it while she is elsewhere.

Your gaze, position, handling and dwell time are themselves potentially perceptible.

### Home
- reciprocal-observation file
- SPD-0017
- RISK-020
- SCE-007 / SCE-008

## 25. Covert observation / cover behavior — COVERED

### Idea
User can ask about Rome magnets while covertly trying to read a bill.

Possible outcomes:
- Nadia notices;
- misses it;
- suspects something else;
- thinks user saw more than they did;
- does not care;
- changes position and alters access.

### Home
- reciprocal-observation file
- SCE-007
- SPD-0018

## 26. Reciprocal models and meta-models — COVERED

### Idea
User models Nadia.
Nadia models user.
Each may model what the other thinks they know.

Misunderstanding can occur at every layer.

### Home
- relational ontology
- reciprocal-observation file
- Q-MODEL-001 / Q-OBS-001

## 27. Privacy is situated, not object-labeled — COVERED

### Idea
Physical access does not equal social permission.

The same bill, photo, medicine cabinet, Bible or phone may have different privacy meaning by person/relationship/context.

### Home
- reciprocal-observation file
- Q-PRIV-002

## 28. Attention allocation is relational behavior — COVERED

### Idea
The player model may eventually distinguish:
- attention capacity;
- attention allocation;
- self-evaluative monitoring;
- practical attention;
- status attention;
- ideological attention;
- attention to children/third parties;
- invasive curiosity;
- tolerance of uncertainty.

### Home
- temporal-attention file
- SPD-0023
- Q-ATTEND-002
- RISK-023

## 29. RAWlsing / Rawlsing epistemic-scaffolding modes — COVERED

### Idea
Potentially preserve one underlying world/person simulation while varying how much agency/epistemic scaffolding the user receives.

Harder pole:
- wits;
- contingency;
- minimal preview/help.

Assisted pole:
- reminders;
- approximate action-depth guidance;
- accessible clock;
- resurfacing already-known facts.

No mode gets hidden psychology or future consequence.

### Home
- temporal-attention file
- SPD-0022
- Q-MODE-002

## 30. Persona may conceal state behind performance — COVERED

### Idea
Nadia may be annoyed but perform pure magnanimity.

Surface response is not equivalent to hidden response.

### Home
- interaction constitution
- SCE-011
- hard epistemic wall

## 31. Persona autonomy / non-response — CORRECTED / NOW COVERED

### Idea
The world should not treat every user act as a prompt demanding a response.

Nadia may:
- not notice;
- not care;
- keep cooking;
- prioritize her child;
- answer later;
- leave;
- remain occupied.

### Prior gap
Independent causality was stated, but this was not explicit enough.

### R2 home
Interaction constitution §16.

## 32. Scene observation can itself change the scene — COVERED

### Idea
Standing at the fridge too long can:
- make Nadia wonder what the user is doing;
- consume departure time;
- alter what others notice;
- cause missed transport.

### Home
- reciprocal-observation file
- temporal-attention file
- SCE-009

## 33. User inquiry should remain open-ended but reality-bounded — COVERED

### Idea
The player can ask for more scene detail as much as they want, but the world determines:
- what exists;
- what can be perceived;
- what requires closer inspection;
- how much time passes;
- whether someone interrupts.

### Home
- interaction constitution
- temporal-attention file
- non-curatorial-world file

## 34. Persistent significance without retcon — COVERED

### Idea
An object/event can be seen long before its significance is known.

Later disclosure can change understanding without changing past reality.

### Home
- Myrtle Beach scenario
- pattern-memory law
- non-curatorial-world file

## 35. Remaining genuine gaps after R2

The ideation itself is now substantially banked.

The remaining work is not “remember what we said,” but actual design/adjudication:

1. exact D001 ownership map for relational semantics;
2. exact durable-promotion law from CAN-008/PFF into V3;
3. formal player-private intention semantics and anti-retroactive rewrite law;
4. ATTEND parser/action schema;
5. physically plausible but computationally economical duration model;
6. narrator perceptual-salience algorithm;
7. lawful world-completion mechanism;
8. concrete alpha action ontology;
9. flourishing constitution;
10. prototype/adversarial tests against the scenario bank.

## 36. Audit result

`R2_COMPLETENESS = PASS_WITH_CORRECTIONS_APPLIED`

No major substantive concept from the interaction ideation is known to remain only in chat memory.

The R2 pass materially corrected:
- stale generic live-recurrence pipeline;
- missing four-view operational model;
- missing non-player-centricity law;
- missing SAY-versus-ATTEND channel distinction;
- under-specified player-private intention/deception;
- missing perceptual-salience selection law;
- missing no-artificial-observation-quota law;
- missing plausible/cumulative/query-invariant duration law.

Future ideation should now build forward from the Sorok corpus rather than reconstruct this interaction theory again.
