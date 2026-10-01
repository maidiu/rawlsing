# Sorok — Population Learning, Research Firewall, and Phenomenal Scene Sampling R1

Status: `PROVISIONAL_PRODUCT_DIRECTION__Q_SALIENCE_Q_SCENE_RESEARCH_REFINEMENT`

Date: 2026-10-01

## 0. Problem

Text simulation cannot give the player a simultaneously scannable visual field.

Every narrated inclusion/exclusion carries an implicit signal:
- if one object is named, the user may infer importance;
- if one object receives more detail, the user may infer importance;
- exhaustive description overwhelms;
- sparse description may hide the ordinary material evidence through which a person becomes knowable.

At the same time, Rawlsing may legitimately learn from aggregate users and optional sociological research.

The design must prevent:
- hidden user psychographics from curating what this user sees;
- personalized dramaturgy;
- self-confirming user models;
- research data from becoming gameplay targeting.

## 1. Four noncollapsed scene layers

`OBJECTIVE WORLD INVENTORY`
!= `CURRENT PERCEPTUAL AVAILABILITY`
!= `NARRATED PHENOMENAL SAMPLE`
!= `USER ATTENTIONAL ACQUISITION`.

### Objective world inventory
What actually exists, independent of whether it is narrated.

### Current perceptual availability
What could presently be perceived from the user's body/position, lighting, occlusion, sound, smell, distance and available time.

### Narrated phenomenal sample
The finite subset surfaced automatically for orientation and ordinary embodied perception.

### User attentional acquisition
What additional information the user obtains by directing `ATTEND`, moving, handling, searching, reading, listening or otherwise spending time/attention.

Narration omission does not mean world absence.

## 2. Non-curatorial scene sampling law

The narrator must not select a detail because:
- it is secretly important to Nadia;
- it will reveal a psychological contradiction;
- it would be narratively dramatic;
- it would tempt this particular user;
- a system praxis hypothesis predicts the user cares about it;
- it would teach the user something morally useful.

Candidate lawful inputs to automatic scene sampling include:
- spatial dominance / orientation value;
- size and visual prominence;
- contrast;
- motion;
- sound;
- smell;
- lighting;
- occlusion;
- proximity;
- obstruction / physical affordance;
- obvious gross disorder or damage;
- current actor activity;
- explicit current user task/attentional target;
- already-established perceptual history;
- time spent in the space with available spare attention.

`HIDDEN SIGNIFICANCE != PERCEPTUAL SALIENCE`.

## 3. Baseline scene frame

A first-entry scene frame should normally contain a compact mixture of:

1. spatial/orienting scaffold;
2. present people and gross ongoing activity;
3. dominant sensory/material state;
4. a small number of physically salient features;
5. a small **non-privileged ambient sample** from other lawfully visible detail.

The ambient sample is chosen without weighting by hidden narrative or psychological importance.

This weakens the "everything named is a clue" convention.

The sampled detail may later become important through real history, but it was not selected because the engine knew that importance in advance.

## 4. Progressive phenomenal coverage

Human vision is not one exhaustive frame. People accumulate detail while remaining in a place.

Rawlsing can imitate this temporally.

As simulated time passes:
- unchanged dominant facts need not be repeated;
- additional low-resolution visible facts may enter awareness when spare attention permits;
- movements/new sounds/obvious changes can become newly salient;
- conversation or divided attention reduces ambient acquisition;
- explicit `ATTEND` accelerates and deepens targeted acquisition.

Thus a kitchen can contain hundreds of facts without producing an entry-wall of text.

## 5. Example: Nadia's kitchen

The world may contain simultaneously:
- a deep sink full of dishes;
- eggs from Nadia's chickens;
- a new stand mixer;
- a high-end blender;
- carefully maintained knives;
- prayer flags;
- floor damage;
- old newspapers;
- records/books/trinkets;
- an almost-hidden french-fry tip under the refrigerator;
- many other ordinary objects.

No universal hierarchy says which one is "the Nadia clue."

On first entry:
- a hole in the floor may be physically unavoidable and therefore baseline salient;
- a mountain of dishes may dominate the room;
- prayer flags across the ceiling may occupy a large visual field;
- a mixer may or may not merit mention depending on sightline/counter prominence;
- the fry tip under the refrigerator is probably low-salience and remains undiscovered unless time/position/attention makes it perceptible.

If the user later looks around the floor or spends enough unoccupied time in the kitchen, the fry may become available.

Do not boost the fry merely because a hidden user model says the user cares intensely about healthy eating.

The user should perform the interpretation.

## 6. Person complexity without clue-authoring

Nadia's world should be generated richly enough that multiple observations can support conflicting or complicating readings.

Example:
- she speaks strongly about healthy eating;
- her kitchen contains high-quality cooking tools;
- she keeps eggs from chickens;
- her sink is overwhelmed;
- an old fry sits under the refrigerator.

These need not be author-planted contradiction clues.

They can be ordinary consequences of:
- routines;
- time scarcity;
- habits;
- projects;
- finances;
- care burdens;
- acquisition patterns;
- self-conception;
- competing strivings;
- past events.

The user is free to notice, ignore, overinterpret, revise or never discover them.

## 7. Hoarding / clutter example

Do not begin from a UI label `HOARDER` and decorate the room to prove it.

Where generated history supports it, represent the material ecology:
- acquisition rate/source;
- discard/retention behavior;
- storage capacity;
- category concentration;
- usable-surface loss;
- circulation paths;
- item condition;
- hygiene separately;
- market/use/sentimental value distribution;
- maintenance;
- conflicts with others;
- fire/access hazards where warranted.

A person with stacked rare books, records and valuable objects may materially differ from a person whose accumulation is dominated by newspapers/clothes/containers.

`ACCUMULATION != FILTH`.
`CLUTTER != ONE PSYCHOLOGICAL ESSENCE`.

The world surface should expose consequences from which the user may form hypotheses.

## 8. Why user-model separation improves algorithm development

The privacy/user-model noncollapse is not only defensive. It improves scientific and engineering validity.

If Rawlsing uses a system hypothesis such as:
> this user attends strongly to hygiene cues

to surface more hygiene cues, and then records that the user noticed hygiene cues, the model creates its own confirming evidence.

This is a **closed-loop observation contamination** problem.

Therefore:

`SYSTEM USER HYPOTHESIS -> SEMANTIC SCENE SALIENCE`

is forbidden by default.

Keeping the layers separate lets Rawlsing distinguish:
- what the world contained;
- what was perceptually available;
- what the narrator sampled;
- what the user actively attended to;
- what the user inferred;
- what Nadia believed the user noticed;
- what the system later hypothesized about user praxis.

That makes later algorithmic evaluation far cleaner.

## 9. Lawful user-facing adaptation

Not all adaptation is corrupting.

Rawlsing may adapt **presentation ergonomics** where transparent and non-semantic, for example:
- requested verbosity;
- accessibility needs;
- explicit preference for more spatial orientation;
- explicit preference for terser prose;
- text size/interface presentation;
- whether the user wants optional orientation aids.

A learned behavioral pattern may justify *offering* such a setting:
> You often ask for more room-layout detail. Want slightly denser spatial orientation by default?

But the system should not silently decide:
> this user cares about status / dirt / religion / food / sex / ideology, so surface more of those details.

`PRESENTATION BANDWIDTH ADAPTATION != SEMANTIC ATTENTION STEERING`.

## 10. Aggregate product learning is lawful

Rawlsing can learn across users without using those learnings to target each individual user.

Aggregate evidence can improve:
- how much baseline text users need to orient;
- which physically grounded salience features are commonly missed;
- whether ambient incidental detail reduces "everything is a clue" behavior;
- how long users tolerate before ATTEND feels necessary;
- which scene-frame structures cause spatial confusion;
- whether progressive phenomenal coverage feels natural;
- accessibility defaults.

These improvements become **global or cohort-validated interface policies**, not secret narrative targeting.

## 11. Optional sociological research plane

A separate opt-in research program is compatible with Rawlsing if its causal direction is explicit.

Possible research inputs:
- user-chosen demographic fields;
- geography at an appropriately coarse grain;
- socioeconomic descriptors;
- cultural/religious background if voluntarily supplied;
- opinion/attitude/value items;
- standardized or project-specific personality/temperament measures;
- separately consented gameplay/praxis variables.

The research plane is:

`OPTIONAL RESEARCH CONSENT`
→ `SEPARATED RESEARCH DATA`
→ `AGGREGATE / POPULATION ANALYSIS`
→ `AUDITED FUTURE GENERATOR / PRIOR / PRODUCT REFINEMENT`.

Not:

`RESEARCH PROFILE OF USER`
→ `THIS USER'S NADIA / WORLD / SCENE SALIENCE`.

## 12. Research data can improve human realism

A research program could improve Rawlsing by refining population-level joint distributions and uncertainty around:
- beliefs/values/tendencies across material and cultural positions;
- correlations and noncorrelations among attitude sets;
- heterogeneity inside demographic categories;
- interaction effects between structural position and personality/relational style;
- which assumed cultural/personality mappings fail;
- where current persona priors are too stereotyped, too flat or too deterministic.

Use this to improve the **generator's population realism**, not to infer a particular user's hidden identity or feed them a tailored counterpart.

Research findings should generally enter as probabilistic priors/constraints, never:
`DEMOGRAPHIC CATEGORY -> FIXED PSYCHE`.

## 13. Research contamination firewall

For valid sociology, preserve experimental provenance.

If a user's gameplay behavior is analyzed, record separately:
- what world/person conditions they encountered;
- what information was actually narrated;
- what they explicitly attended to;
- what they did;
- what system hypotheses existed;
- whether any presentation setting differed.

Otherwise Rawlsing cannot tell whether a behavioral pattern came from the user or from differential exposure produced by the product.

This is another reason not to let hidden user models control semantic narration.

## 14. Sampling limitation

Rawlsing users are a self-selected population.

Research on them may reveal:
- patterns within Rawlsing's user population;
- useful associations;
- failure modes in existing priors;
- hypotheses worth external validation.

It does not automatically establish population prevalence or universal cultural law.

Any broader sociological claim requires appropriate sampling and analysis beyond product convenience data.

## 15. Research transparency

Do not promise:
> Rawlsing never collects personal information

if users may voluntarily provide demographic or attitudinal data.

A more truthful product principle is:

> Rawlsing does not sell your personal information. Optional research contributions are separate from ordinary play, clearly identified by purpose, and are not used to tailor your synthetic relationships unless you separately choose a product function that explicitly requires that information.

Exact privacy/legal copy requires later legal review.

## 16. Data separation

At minimum distinguish:

### PLAY / CAUSAL CONTINUITY
Needed to make this relationship/world historically real.

### USER-FACING PRESENTATION SETTINGS
Explicit ergonomics/accessibility choices.

### SYSTEM PRAXIS HYPOTHESES
Bounded behavior summaries under Q-PRIV/Q-PLAYER law.

### OPTIONAL RESEARCH DATA
Separately consented demographic/attitude/measure data.

### AGGREGATE PRODUCT/GENERATOR FINDINGS
Audited population-level outputs that may inform later versions.

No silent backflow from optional research data into the donor's live continuity.

## 17. Compact theorem

> **Learn from people at the population level; encounter each player through what they actually do.**

And for narration:

> **The world may be rich; the first description may be sparse; attention and time turn latent perceptibility into acquired detail. Selection must follow phenomenal salience, not hidden significance or predicted user interest.**
