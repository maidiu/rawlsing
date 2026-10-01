# Sorok — Post-Banking Omission Audit R1

Status: `PASS_WITH_FOUR_CORRECTIONS__NO_OTHER_MATERIAL_CHAT_ONLY_PRODUCT_CONCLUSION_FOUND`

Date: 2026-10-01

## 0. Purpose

This is a second-pass omission audit over the late 2026-10-01 Sorok conversation after the first banking receipt.

The audit compares the live chat concepts against:
- artifacts 59–64;
- decisions SPD-0160..SPD-0187;
- risks RISK-132..RISK-144;
- relevant question crosslinks;
- STATUS.json;
- state/CURRENT_STATE.md.

The first receipt was substantially correct but missed or under-promoted four product conclusions.

## 1. Corrections made

### C1 — abandoned seed person cannot be reacquired at fresh T0

The chat explicitly established:

> restart means the user has ditched that person; they do not get to meet a fresh copy of that same seed person again as though nothing happened.

Artifact 61 contained this in prose, but the decision register did not.

Corrected by:
- `SPD-0184 PROVISIONAL_ABANDONED_SEED_PERSON_NONREENTRY_LAW`
- `RISK-142`
- crosslink to `Q-RETRY-001`.

### C2 — compiled seed-person runtime direction

The chat made a strategic alpha-serving point:

> a small prebuilt seed-person pool may let the hot path serve compiled person/world state plus V3/V2/LLM/user-relation machinery rather than dragging the entire PRE-V3 source/artifact universe into live serving.

Artifact 62 recorded the economic hypothesis, but it was not a first-class decision.

Corrected by:
- `SPD-0185 PROVISIONAL_COMPILED_SEED_RUNTIME_DIRECTION`
- `RISK-143`
- crosslink to `Q-COST-001`.

This does **not** erase upstream source/provenance authority. It only separates build/provenance burden from hot-path serving unless runtime law proves direct access necessary.

### C3 — material detail must be person-specific, not decorative theming

The chat explicitly required that every layer of environmental/object/backstory proliferation be intensely constrained by the persona's V3 specificity and life/world history.

Artifacts 60/61 implied this, but no dedicated decision made the requirement hard enough.

Corrected by:
- `SPD-0186 PROVISIONAL_V3_CONSTRAINED_MATERIALIZATION_LAW`
- `RISK-144`
- crosslinks to `Q-FLESH-001`, `Q-LAZY-001`, and `Q-V3-001`.

### C4 — attention firewall ambiguity

`SPD-0162` could be read as forbidding any user-specific semantic perceptual weighting, while `SPD-0164` explicitly permits a bounded user attention regime.

The intended distinction was present in artifact 60 but under-specified in the decision layer.

Corrected by:
- `SPD-0187 PROVISIONAL_ATTENTION_PERSONALIZATION_REFINEMENT`
- crosslinks to `Q-PLAYER-001`, `Q-ATTEND-002`, `Q-NARR-001`, `Q-SALIENCE-001`, and `Q-SCENE-001`.

Final law:
- praxis/psychographic/moral/engagement/retention models may not curate meaningful content;
- a separately governed perceptual-attention model may weight which already-perceptible details the user would plausibly register;
- world truth and narrative usefulness remain independent.

## 2. Coverage matrix

### User-data noncollapse and sociological research
Covered by:
- artifact 58;
- artifact 59;
- SPD-0153..0159;
- SPD-0163.

Includes:
- external human != player state != user-supplied facts != event history != actor-local user model != system praxis hypothesis;
- optional demographic/attitude research;
- aggregate population learning;
- no donor-specific live backflow;
- self-selected-sample caveat;
- truthful privacy framing.

Audit result: `COVERED`.

### Text-surface inclusion/exclusion problem
Covered by:
- artifact 59;
- SPD-0160/0161.

Includes:
- finite scene frame;
- world richer than narration;
- progressive phenomenal coverage;
- ordinary ambient details not authored clues;
- hoarding/clutter represented materially rather than as one essence.

Audit result: `COVERED`.

### User-specific regimes of attention
Covered by:
- artifact 60;
- SPD-0164/0165/0167/0169/0187.

Includes:
- different attentive users notice different things;
- personalized perception != personalized reality;
- feedback loop permitted but provenance-controlled;
- exploration mass prevents lock-in;
- user attention model is contextual/uncertain.

Audit result: `COVERED_AFTER_C4`.

### Recognition repertoire
Covered by:
- artifact 60;
- SPD-0166.

Includes:
- visible form != readable mark != identification != domain knowledge != interpretation;
- Vitamix/knife/book/style examples.

Audit result: `COVERED`.

### Shared coarse gestalt versus local particulars
Covered by:
- artifact 63;
- SPD-0181.

Includes:
- Samia-style immediately legible sparse/immaculate/deliberate/expensive-feeling gestalt;
- expertise-dependent object/style recognition held back to later layers.

Audit result: `COVERED`.

### Ahead-of-attention world depth
Covered by:
- artifact 60;
- SPD-0168.

Includes:
- rolling causal overhang;
- layered L0–L5 depth;
- query chooses locus of resolution, not answer;
- hidden details can causally affect Nadia before user knows them.

Audit result: `COVERED`.

### V3-guided detail proliferation
Covered by:
- artifacts 60/61;
- SPD-0186.

Includes:
- house/object/body/backstory detail strongly constrained by durable V3 specificity plus life/material/world history;
- anti-stereotype / anti-aesthetic-theming rule.

Audit result: `COVERED_AFTER_C3`.

### Same root Nadia, different phenomenal Nadia
Covered by:
- artifacts 60/61/62;
- SPD-0169/0170/0180.

Includes:
- same pre-contact person;
- different user perceptual paths;
- different post-contact histories;
- cross-user discourse/pedagogy.

Audit result: `COVERED`.

### Small deeply prebuilt introductory persona pool
Covered by:
- artifact 61;
- SPD-0170;
- artifact 62 runtime hypothesis.

Includes:
- deep amortized person generation;
- stronger benchmark reproducibility;
- lower first-session compute;
- user-specific copy-on-write relation branches.

Audit result: `COVERED`.

### Shared pre-contact back-data
Covered by:
- artifact 61;
- SPD-0171;
- RISK-134/RISK-140.

Includes:
- globally shareable pre-contact facts;
- deterministic/keyed query-invariant completion;
- no first-user authorship;
- cross-branch compatibility law.

Audit result: `COVERED`.

### Compiled live-serving simplification
Covered by:
- artifact 62;
- SPD-0185.

Includes:
- compiled seed-person/world package on hot path;
- V3/V2/LLM/user-relation runtime focus;
- PRE-V3/source artifacts remain governed build/provenance concerns unless runtime requires them.

Audit result: `COVERED_AFTER_C2`.

### Restart / no save-scumming / irreversible relation time
Covered by:
- artifacts 61/63;
- SPD-0172/0173/0184.

Includes:
- restart is abandonment;
- cancel restart returns to current changed relation;
- no T0 replay;
- same abandoned seed root not reissued fresh to same user;
- repair/revision possible; undo impossible.

Audit result: `COVERED_AFTER_C1`.

### Cryptic first warning and fuller restart disclosure
Covered by:
- artifact 63;
- SPD-0182/0183;
- RISK-139.

Includes:
- pre-first-persona cryptic attention warning;
- fuller explanation at restart attempt;
- no guilt/churn manipulation;
- ATTEND as deliberate widening beyond default habits.

Audit result: `COVERED`.

### Adult-life possibility without theme-park fences
Covered by:
- artifact 62;
- SPD-0174.

Includes:
- sex;
- substance use;
- crime;
- exploitation;
- serious violence;
- injury;
- death;
- bad behavior;
- ordinary life.

Audit result: `COVERED`.

### Anti-porn / anti-commodification thesis
Covered by:
- artifact 62;
- SPD-0174/0175/0179;
- RISK-136/RISK-141.

Includes:
- possible human act != product goal/content category/reward/commodity;
- the person remains more real than the user's use of them;
- event truth/consequence/rendering separated;
- intensity cannot become consumable spectacle.

The etymological/philological aside about `porneia` was conversational genealogy, not separately banked as semantic product authority; the substantive anti-commodification thesis it motivated is fully banked.

Audit result: `COVERED`.

### Ordinary-life aftermath
Covered by:
- artifact 62;
- SPD-0175.

Includes:
- sex/violence/intensity do not suspend work, children, illness, chores, family, money, projects or other relationships;
- no event consumes the person who participated in it.

Audit result: `COVERED`.

### Nadia's own relational gravity
Covered by:
- artifact 62;
- SPD-0176/0177/0178;
- RISK-137/RISK-138.

Includes:
- persona-caused increased availability/affection/sexual responsiveness/dependency/exclusivity/sacrifice/reprioritization may be lawful;
- independent life is not an artificial anti-attachment counterweight;
- emergent love/attachment allowed;
- platform retention engineering forbidden.

Audit result: `COVERED`.

### Shared-person game/discourse culture
Covered by:
- artifact 62;
- SPD-0180;
- RISK-135.

Includes:
- "I got Nadia" as common starting-person discourse;
- different observations and relationships;
- pedagogical comparative value;
- risk of walkthrough/tier-list/sexual-conquest optimization culture.

Audit result: `COVERED`.

## 3. Deliberately not frozen yet

The audit found no missing product conclusion in these areas; they remain intentionally open/prototype-bound:

### Exact seed pool size
"Five" is a strong alpha candidate, not constitutional law.

### Exact first-use and restart copy
The timing/function is banked.
Exact wording remains UX/prototype work.

### Exact rendering explicitness for sex/violence
Event truth != consequence != rendering is banked.
Exact renderer policy remains to be specified/tested.

### One shared multi-user Nadia
Artifact 60 distinguishes true shared-person multiplayer from independent seed forks.
Shared live Nadia remains post-alpha and is not being smuggled into current architecture.

### Exact PRE-V3 artifact/package implementation
The hot-path compiled-person direction is banked.
The exact build artifact schema, versioning, provenance, storage and PRE-V3→V3 compilation contract remain implementation/architecture work.

### Exact attention-model estimator
The constitutional inputs/provenance/firewalls are banked.
The actual estimator/scoring/update algorithm remains prototype/implementation work.

### Exact research protocol
Optional research purpose/firewall/sample limitation are banked.
Consent form, retention schedule, de-identification mechanics, statistical protocol and legal copy remain future research/privacy implementation.

## 4. Question accounting

No new question rows were required by the corrections; they sharpen existing frontiers.

Accounting therefore remains:
- 117 total questions;
- 1 ALPHA_SPEC blocker;
- 43 ALPHA_IMPLEMENTATION blockers;
- 25 ALPHA_VALIDATION;
- 18 POST_ALPHA;
- 30 NONE/nonblocking answered-or-closed.

The sole ALPHA_SPEC blocker remains:
- `Q-ALPHA-001`.

## 5. Audit verdict

The first receipt missed or under-promoted four material items. Those four are now corrected in the decision/risk/question layers.

After this second pass, no other important product conclusion from the late conversation remains only in chat.

Terminal:

`PASS_WITH_CORRECTIONS__LATE_2026_10_01_CHAT_TO_REPO_OMISSION_AUDIT_COMPLETE__NO_OTHER_MATERIAL_CHAT_ONLY_PRODUCT_CONCLUSION_FOUND`
