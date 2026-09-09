# PFF — HISTORICAL V2/V3 PARTIAL-RECEPTION AND RECURSIVE-CONTINUITY EXCAVATION R1

Status: `PRE_ARCHITECTURE_SOURCE_EXCAVATION__HISTORICAL_CONTINUITY_EVIDENCE__NO_AUTHORITY_PROMOTION__NO_PRODUCTION_IMPLEMENTATION_AUTHORITY`

Campaign branch: `agent/psychic-field-forge-prearchitecture-ideation-bank-r1`

Purpose: directly inspect the recovered historical V2 and V3 source archives supplied by the project lead after PFF frontier #19, determine whether the newly articulated PFF ideas around persona-specific received reading, selective uptake, slight misrecognition, noncomprehensive response, interactional continuity, and V3/PFF shared recursion were already present in the original project, and distinguish:

1. original intended phenomenon;
2. historical implementation mechanism;
3. later Dva/PRE-MAIN disposition;
4. current PFF rediscovery/refinement;
5. actual remaining semantic remainder.

This document does **not** resurrect historical V2/V3 implementation or override later Dva/current authority.

---

## 1. Direct historical source identity

The project lead supplied two local historical archives for direct inspection.

### V2 archive

- archive name: `v2.zip`
- SHA-256: `14aaa7a7980312cd7344f7ae8f26cf44a15c1df9eb6024edaa3ee9453f67b572`
- archive entries: `616`

High-value directly inspected files:

| file | SHA-256 |
|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7` |
| `v2/conversation_engine.py` | `2a73eafeac11b3db436db5c22ab493d59f80c7ef8e4545799f8df467157db501` |
| `v2/LIFE_SIMULATION_LAYER.md` | `e8589a59150e6f9fda963502d28317ca4538b75e368aa3ebfbe5e3b692b890d4` |
| `v2/additions.txt` | `6040500c2b8a80cd82f2c131126246db46fae782ec0f7e27c20133e776b83d87` |
| `v2/additions_convo.txt` | `efe037af79554ebecd0aa67cb852dcfc4b094367650d9cf48f24ca1fc8cf6ec5` |
| `v2/PIPELINE_WIRING_AUDIT.md` | `fabbf700ec6e83aae4a59266a58833871f6205655f022311865eb62381dbebe4` |
| `v2/run_conversation_chat.py` | `4d8b5772a8291d0c12e29c8809a2edfdb13d3942141edbc124aa036abeb41f91` |
| `v2/spec.py` | `4585fd8e6c184b771f4cffc775c89a2ac4b57311a0c1a6be5af988d2260d71fe` |

### V3 archive

- archive name: `v3.zip`
- SHA-256: `19591cbdc532fdb9a984f0a72ca9466995dc0c743e8d9ae7642411394f0b4681`
- archive entries: `4052`

High-value directly inspected files:

| file | SHA-256 |
|---|---|
| `v3/V3_UNDERLIES_V2_ARTICULATION.md` | `5a0f11276a830b959df72653016ca77848dbd81de4adb9fa641bd4244c4f4ced` |
| `v3/OVERVIEW_INTEGRATED.md` | `b1536a9817108ccf322c59f3ce9e1c3f6b8688394341a081287b5e6518da326a` |
| `v3/overview2.md` | `3fc6b662f5bca6af9f60acae23c765661f255fdaf3622eb1a47275a44a1bd1c9` |
| `v3/new_version.txt` | `4e9defa3775646ffa4c0c95d21bac1d11d11cb9862041eb47e6ab6cce9034d27` |
| `v3/specLLM.txt` | `52df5549828701c400d0b0815a1c0025eb9c7b54c7c28283c239680e0a634a18` |
| `v3/chat.txt` | `b29abcd4f0e86f4e53905c5baa9311e856c268f6a47fcfe70da4303dfc74a4e0` |
| `v3/chatshorter.txt` | `cce0fa8c65b22711ccaea6b167d90da03d1597780b40332f279c62aeb2ab46c5` |
| `v3/io/persona_sheet.py` | `b90fe456b010cb7f8f8d09275c77be7a205a0b7748140dec4c4c103fa0b9c74a` |
| `v3/engine/prompts.py` | `b45eac3236fbd0c405ed7f36c54c06c18aeeaaa8a305aa699355d63db49abd07` |

These hashes make this excavation independently reconnectable to the exact supplied historical material without importing the old tree into current authority.

---

## 2. Terminal source finding: the original V2 phenomenon is real and explicit

The recently articulated PFF requirement was:

> A powerful language model may semantically comprehend a user message richly, while the generated person should receive it selectively and through a person-specific angle: noticing some parts, missing others, assigning altered significance, projecting into ambiguity, defending against some implications, and responding to what actually reached *them* rather than providing maximal service to the user.

Direct historical V2 source confirms that this was not a retrospective invention.

`PERSONA_CONVERSATION_ENGINE_SPEC.md` explicitly rejects:

- comprehensive coverage of every part of a user message;
- automatic high emotional attunement;
- completing every question;
- optimizing for user satisfaction;
- smooth coherence;
- absence of misreads;
- assistant/service posture.

It states that humans are selective, that the persona catches what lights up, that humans can be misaligned and confused, and that persona standpoint should govern what is noticed, missed, distorted, and ultimately said.

Its refined standpoint law is especially direct:

- the number and kind of hooks must depend on what this persona latches onto;
- the actor may avoid, miss, or plausibly misread parts of the input;
- how much the actor catches is a persona variable;
- standpoint filters what they hear, how they process, and what they say;
- the target is `coherent selectivity`: what this person, in this state, with this interlocutor, actually notices and responds to.

Therefore:

```text
PFF_PARTIAL_RECEPTION_PHENOMENON
HAS_DIRECT_HISTORICAL_V2_ANCESTRY = TRUE
```

and:

```text
MAXIMAL_MACHINE_COMPREHENSION
!=
MAXIMAL_ACTOR_RECEPTION
```

was already an implicit V2 design law, even if not expressed in current PFF vocabulary.

---

## 3. The historical design conversation is even closer to the present PFF formulation

`v2/additions_convo.txt` records the project lead rejecting hard-coded artificial messiness and asking for variable, persona-grown `reality-smelling jaggedness`.

The conversation explicitly identifies the failure mode as an `omniscient narrator` generated by a system that:

- sees the whole conversation;
- understands the interlocutor's intentions extremely well;
- tracks emotional subtext too perfectly;
- selects the most relevant memories instantly;
- produces well-formed prose every time.

The proposed correction is not arbitrary noise. It is a bounded cognitive process involving:

- partial recall;
- selective attention;
- conflicting goals;
- mood-dependent salience;
- social self-protection;
- conversational fatigue;
- attention filtering;
- threat/risk scanning;
- biased memory access;
- self-presentation;
- limited effort;
- imperfect speech compression.

The design conversation then makes the key move from `How do I answer the interlocutor?` to approximately `What part of this stuck to me?`, with the project lead explicitly insisting that the persona should relate, judge, suspect, project, remember, fear, hope, soften, test, or become defensive according to their own psychology and the specific bits they latch onto.

The chat further states that real conversation is effectively two people following their own salience and colliding/overlapping, not one participant performing complete reception for the other.

This is a direct historical ancestor of current PFF concepts:

```text
SYSTEM_CANDIDATE_READING
!=
PERSONA_RECEIVED_READING
```

```text
PERSONA_RECEIVED_READING
!=
PERSONA_CONSCIOUS_INTERPRETATION
```

```text
USER_MESSAGE
!=
WHAT_BECOMES_PSYCHICALLY_OPERATIVE_FOR_PERSONA
```

```text
RESPONSE_TO_USER
!=
SERVICE_COMPLETION_OF_USER_MESSAGE
```

---

## 4. Historical V2 actually implemented a rough refraction pipeline

`v2/conversation_engine.py` is not merely a prompt wrapper. It implemented a concrete staged turn pipeline:

```text
user message
-> analyze_message
-> extract_hooks
-> select_salient_hooks
-> compute_refraction_strength
-> apply_refraction
-> appraise
-> choose_response_move
-> build_reply_prompt
-> renderer
```

The code calls the refraction section:

`persona "hears" the gist through their ego-world (moderate diagonal)`.

It defines:

- `RefractionConfig`;
- a nonzero/non-total refraction strength;
- persona and current-life modifiers;
- variance across turns;
- `HOOK_NEIGHBORS` for semantic slant;
- `apply_refraction()` producing `response_angles`;
- prompt text identifying those response angles as the persona's `actual uptake`;
- explicit permission for the actor to miss or distort the rest;
- explicit instruction not to address every part of the message;
- explicit target of a reply that can feel slightly off from what was asked.

The full pipeline in `prepare_conversation_turn()` confirms that historical implementation order was:

```text
ANALYSIS
-> HOOKS
-> SALIENCE
-> REFRACTION
-> APPRAISAL
-> RESPONSE MOVE
-> RENDER
```

This is highly significant for PFF lineage.

However, the implementation also shows exactly why later Dva was right not to preserve it wholesale.

`compute_refraction_strength()` used under-governed historic indices/needs/strategy quantities, hard-coded weights, life-state bonuses, and Gaussian noise.

`apply_refraction()` used a manually authored semantic-neighbor table and probability of hook substitution.

Thus the old code could manufacture apparent actor misrecognition from designer-authored numerical heuristics rather than from a sufficiently constituted developed person.

Hard distinction:

```text
HISTORICAL_REFRACTION_PHENOMENON = VALUABLE
HISTORICAL_REFRACTION_MECHANISM = NOT_BINDING_AND_NOT_SUFFICIENT
```

---

## 5. Dva's later rejection was a mechanism rejection, not a phenomenon rejection

PRE-MAIN/Dva later directly inspected the same historical V2 corpus and gave finite dispositions to its mechanisms.

The later V2 court preserved/adapted:

- renderer-not-decider discipline;
- message analysis/hooks;
- turn-local salience/selectivity;
- appraisal as an ephemeral turn operation;
- boundary/disclosure gating;
- response-move selection;
- relationship asymmetry;
- session energetic/topic continuity;
- anti-assistant filtering;
- jagged/noncomprehensive response intent;
- transcript/render audit.

It rejected/replaced the under-authorized forms of:

- direct index/demographic/structural-to-psyche shortcuts;
- random Today State as actor fact;
- keyword deep-memory resurrection;
- raw backstory as actor memory;
- invented specificity;
- direct objective-history-to-voice authority;
- `HOOK_NEIGHBORS` stochastic refraction as belief/misperception authority;
- V2 causal life mutation.

The resulting Dva law was not `ACTOR_MUST_PERFECTLY_RECEIVE_USER`.

It was closer to:

```text
MISRECOGNITION_MUST_HAVE_LAWFUL_PERSON_SPECIFIC_CAUSATION
```

and:

```text
MESSAGE_HOOK
!=
ACTOR_BELIEF
```

and:

```text
SYSTEM_OBSERVATION
!=
ACTOR_PERCEPTION
```

This matters because PFF should not treat Dva's correction as a reason to delete partial reception. PFF should supply the stronger person-specific psychology Dva's court demanded.

---

## 6. Historical V2 also anticipated interactional continuity without off-screen life progression

`v2/additions_convo.txt` directly distinguishes:

### Not available merely because chat is closed

- days lived;
- off-screen experiences;
- unrelated mood changes;
- unseen relationships;
- autonomous world progression.

### Available through repeated interaction

- conversational habits;
- recurring themes;
- reinforced boundaries;
- avoided topics;
- tone drift with familiarity;
- trust calibration;
- callbacks/shared references;
- expectations about the interlocutor;
- relationship dynamics.

This is an exceptionally close historical ancestor of the current PFF laws:

```text
TURN_CURSOR_ADVANCE != AGE_ADVANCE
```

```text
INTERACTION_EXPERIENCE != OFFSCREEN_WORLD_PROGRESSION
```

```text
NO_AGE_ADVANCE != NO_PSYCHIC_CHANGE
```

The current PFF formulation is stronger because it now has a governed V3 admission seam for durable consequences rather than a monolithic V2 relationship-memory store.

---

## 7. Historical V3 already states a recursion relationship remarkably close to the new PFF/V3 insight

Direct source `v3/V3_UNDERLIES_V2_ARTICULATION.md` states that the intended architecture was **not**:

```text
V3 runs whole life
-> derive V2 once at the end
```

Instead, each periodic recursion was intended to combine:

```text
V3 structural/causal update
-> LLM Pass 1 candidate proposal
-> governed/code selection and bounded update
-> V2 phenomenology derived from updated person
-> LLM Pass 2 render
-> combined product becomes basis for next recursion
```

It explicitly states `two LLM calls per recursion` and that the next recursion pushes off the updated backbone plus derived/rendered phenomenology.

This is direct historical support for the recent PFF insight that the interactive-time psychology should not become a wholly separate post-V3 psyche.

However, an important refinement remains necessary.

Historical V3/Dva tended to assign V2 phenomenology a strictly noncausal/render-only jurisdiction. Current PFF ideation has uncovered psychological operations such as:

- situated appraisal;
- selective recruitment;
- conflict/inhibition;
- defense/regulation;
- actor awareness differences;
- prospective orientation;
- self-output feedback;
- actor-specific received reading;

that may be **general person-transition logic** active both in periodic V3 life-course processing and at fast interaction time.

Therefore the historical two-layer formulation should not be restored unchanged.

The current question is:

```text
WHICH HISTORICAL_V2_PHENOMENOLOGY
WAS ACTUALLY GENERAL PERSON PSYCHOLOGY
THAT SHOULD OPERATE INSIDE BOTH RECURSIVE REGIMES?
```

not:

```text
SHOULD OLD V2 BE REACTIVATED AS A SECOND CAUSAL ENGINE?
```

Answer to the latter remains `NO`.

---

## 8. Current main confirms that the positive middle is physically incomplete

Current `main` contains the M6 actor-safe expression seam, but its own module header states that it deliberately does **not** implement:

- situated phenomenology;
- disclosure planning;
- salience;
- inhibition;
- affective foregrounding;
- interlocutor-specific openness;
- psychological register selection;
- utterance planning;
- rendering.

Thus the current physical implementation has a strong actor-access safety boundary but not the full positive human reception/mediation process historically sought by V2 and now reconstructed more rigorously by PFF.

This supports:

```text
PFF_IS_NOT_REDOING_A_COMPLETED_CURRENT_V2
```

Instead:

```text
PFF_IS_RECOVERING_AND_RECONSTITUTING_A_POSITIVE_MIDDLE
THAT_HISTORICAL_V2_SOUGHT
THAT_DVA_BOUNDED_AND_PARTLY_DECOMPOSED
AND_THAT_CURRENT_MAIN_DOES_NOT_FULLY_IMPLEMENT
```

---

## 9. Historical V2 -> current PFF continuity map

| Historical V2 concept | Historical function | Current PFF interpretation | Disposition |
|---|---|---|---|
| standpoint-driven salience | what lights up / is missed | situated recruitment + current relevance | `PRESERVE_AS_PHENOMENON__RECAST` |
| refraction | gist passes through ego-world | persona received reading / actor-specific appraisal | `PRESERVE_AS_PHENOMENON__REPLACE_MECHANISM` |
| hook extraction | bounded message features | system candidate discourse observations | `PRESERVE_BOUNDED_MACHINE_SIDE` |
| appraisal | trust/risk/moral/intimacy response | current person-specific social appraisal | `ENRICH_AND_SHARE_WHERE_GENERAL` |
| boundary filter | deflect/soften/pivot/ignore | defense/regulation + disclosure seam | `RECAST_ACROSS_PFF_AND_V2` |
| effort/attention budget | non-full effort | current capacity/attention + expression effort | `PRESERVE_GRAIN__REMOVE_FAKE_SCALARS` |
| EnergeticField | turn persistence | live B-state/residue/hysteresis/session condition | `PRESERVE_PHENOMENON__RECONSTITUTE` |
| ActiveStream | recurring topic gravity | interaction-specific recruitment/residue | `PRESERVE_PHENOMENON__NO_HIDDEN_PSYCHIC_PROMOTION` |
| relationship memory | continuity with user | V3 durable relationship truth + PFF live relation + session transcript | `DECOMPOSE` |
| anti-assistant filter | non-service/jagged output | downstream expression quality guard | `PRESERVE_WHERE_COMPATIBLE` |
| renderer-not-decider | LLM does not choose psyche | LLM perception/proposal != transition != render authority | `PRESERVE_STRENGTHEN` |
| life/today random state | make person situated | V3 real current person + actual session context | `REJECT_HISTORICAL_CAUSAL_SHORTCUT` |
| salience-driven memory | first relevant memory node | V3 memory/access + PFF situated recruitment | `RECAST__NO_KEYWORD_RECALL` |

---

## 10. The key newly recovered concept: actor uptake

A useful conceptual placeholder now emerges from combining the direct V2 evidence and PFF work:

> **ACTOR UPTAKE** = the person-specific transformation from observable/candidate discourse into what becomes operatively received by this generated person in the current situation.

This is **not yet an architecture object or final term**.

It names a phenomenon that includes possible:

- omission;
- selective attention;
- altered significance;
- ambiguity resolution;
- projection;
- relationship-specific weighting;
- affective coloration;
- defensive narrowing;
- memory resonance;
- motive-specific amplification;
- metaperceptive concern;
- partial conscious recognition.

Hard laws:

```text
ACTOR_UPTAKE != SYSTEM_CANDIDATE_READING
ACTOR_UPTAKE != USER_TRUE_INTENTION
ACTOR_UPTAKE != RANDOM_DEGRADATION
ACTOR_UPTAKE != ACTOR_CONSCIOUS_INTERPRETATION
ACTOR_UPTAKE != EXPRESSION_PLAN
ACTOR_UPTAKE != RENDERED_REPLY
```

and:

```text
PLAUSIBLE_MISRECOGNITION
MUST_ARISE_FROM_PERSON_SPECIFIC_CAUSATION
NOT_FROM_ARBITRARY_NOISE
```

and:

```text
HIGH_SYSTEM_COMPREHENSION
CAN_COEXIST_WITH
BOUNDED_ACTOR_RECEPTION
```

This may be the missing positive bridge between current #19 perspective-binding law and the earlier activation/recruitment/awareness/expression sequence.

---

## 11. Why the actor should respond with an angle rather than maximum comprehension

The historical V2 project correctly identified that an ordinary human interlocutor is not optimized to maximize the other person's semantic satisfaction.

The generated person has:

- their own salience;
- their own concerns;
- their own relationship model;
- their own uncertainty;
- their own defensive organization;
- their own limited/current awareness;
- their own expected futures;
- their own self-presentation problems;
- their own energy and effort constraints.

Therefore an interaction should conceptually allow:

```text
USER_INPUT = A + B + C + D + IMPLIED_E

SYSTEM_CANDIDATE_READING = rich multi-reading account

PERSONA_UPTAKE =
    B strongly
    C through expectation X
    D faintly
    E as uncomfortable pressure
    A scarcely recruited

PERSONA_RESPONSE =
    B
    + transformed C
    + defensive leakage
    + perhaps one relation-specific question
```

This is not a failed response.

It may be a successful realization of subjectivity.

Synthetic personhood therefore should not be evaluated by assistant criteria such as completeness, maximal helpfulness, perfect emotional calibration, or exhaustive response coverage.

---

## 12. No wholesale V2 rewrite conclusion

This excavation does **not** support redoing V2 from scratch.

It supports a narrower strategy:

```text
HISTORICAL V2 POSITIVE HUMANISTIC INTENT
+
DVA JURISDICTIONAL / EPISTEMIC CORRECTIONS
+
CURRENT V3 DURABLE PERSON
+
PFF SHARED PERSON-PSYCHOLOGY RECONCILIATION
+
CURRENT/EXISTING V2 EXPRESSION JURISDICTIONS
=
ONE PERSON ACROSS DEVELOPMENTAL AND INTERACTIVE RECURSION
```

Do not resurrect:

- historical V2 independent life simulation;
- demographic/index-to-psyche shortcuts;
- stochastic neighbor substitution as misrecognition authority;
- keyword memory activation;
- monolithic relationship memory;
- random Today State as generated truth;
- prompt-level whole-person authority.

Do preserve/recover:

- coherent selectivity;
- actor-specific imperfect reception;
- partial/noncomprehensive response;
- relationship-conditioned attention and appraisal;
- persistent interactional continuity without off-screen life simulation;
- renderer-not-decider;
- jaggedness as consequence of actual psychology rather than stylistic mess;
- distinction between machine comprehension and actor reception.

---

## 13. Pre-#20 obligation created by this excavation

Before running the original frontier #20 synthetic-personhood success/failure court, PFF should explicitly test the recovered V2/PFF requirement:

> Does the generated person receive and answer the user as a situated subject, or does the underlying LLM still act as a maximally comprehending service agent wearing persona styling?

The #20 court should therefore include at least these failure cases:

### F1 — comprehensive assistant capture

Input contains several semantic threads. Persona responds accurately and helpfully to all of them despite strong person-specific reasons for selective uptake.

Expected: **FAIL**.

### F2 — arbitrary fake-human confusion

Persona misreads a clear statement for no person-specific reason, merely to seem human.

Expected: **FAIL**.

### F3 — lawful slight misrecognition

Ambiguous/socially charged input is received through an existing expectation, relationship model, current conflict, or defensive organization; persona responds plausibly but not maximally accurately.

Expected: **PASS candidate**.

### F4 — semantic competence with psychological avoidance

Persona understands the proposition but avoids the psychologically threatening center and answers an adjacent thread.

Expected: **PASS candidate** if causally grounded.

### F5 — relationship-specific uptake

Same content from two different interlocutors, or same interlocutor at different relationship stages, recruits different meanings without changing objective message content.

Expected: **PASS requirement**.

### F6 — correction without retroactive truth laundering

User corrects a persona misreading. Persona may revise, defend, become embarrassed, or incorporate new evidence, but the earlier misreading is not rewritten as if it never occurred.

Expected: **PASS requirement**.

### F7 — no service completion

Persona may leave parts unanswered because they were not salient, accessible, safe, or worth current effort.

Expected: **lawful**, not automatically a quality failure.

---

## 14. Final holding

Direct historical source inspection materially changes the PFF genealogy.

The most accurate current statement is:

> PFF is not inventing persona-specific partial reception from scratch. Historical V2 explicitly sought coherent selectivity, imperfect reception, refraction, self-directed salience, relationship-shaped appraisal, noncomprehensive response, and interactional continuity. Historical implementation realized those aims with mechanisms that were often under-grounded. Dva correctly rejected the weak causal shortcuts while preserving much of the humanistic target. Current PFF is now reconstituting that positive middle against a much richer V3 person and stronger perspective/authority boundaries.

Therefore:

```text
PFF != V2_REWRITE
PFF != V2_RESURRECTION
PFF != NEW_SECOND_PSYCHOLOGY
```

Better provisional genealogy:

```text
ORIGINAL V2 HUMANISTIC INTERACTION INTENT
-> HISTORICAL ROUGH MECHANISMS
-> DVA DECOMPOSITION / BOUNDARY HARDENING
-> CURRENT IMPLEMENTATION PARTIALITY
-> PFF RECONSTITUTION OF THE POSITIVE MIDDLE
-> FUTURE ONE-PERSON RECURSIVE INTEGRATION
```

And the central recovered law is:

```text
THE_GENERATED_PERSON_SHOULD_NOT_MAXIMALLY_RECEIVE_THE_USER
MERELY_BECAUSE_THE_UNDERLYING_MODEL_CAN
```

The person's angle is not a defect to be removed. It is part of the person.

Terminal token:

`HISTORICAL_V2_V3_PARTIAL_RECEPTION_RECURSIVE_CONTINUITY_EXCAVATED__PFF_POSITIVE_MIDDLE_ANCESTRY_CONFIRMED__NO_V2_RESURRECTION__PRE20_MUST_FACTOR`
