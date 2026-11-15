# PSYCHIC FIELD FORGE R1 — ZERO-LOSS CONVERSATIONAL VISION APPENDIX

**Status:** `VISION_PRESERVATION_APPENDIX__MUST_FACTOR__NOT_ARCHITECTURE_ADOPTION`

## Purpose

This appendix preserves the full set of user-directed and conversationally converged Psychic Field Forge ideas from the originating design exchange, including nuances that were compressed, normalized or only implicit in `00_VISION_BANK_R1.md`.

It is deliberately redundant.

The future PFF Vozhd must treat this as a zero-loss requirements reservoir, not as a preselected implementation.

## 1. Four simultaneously real depth bands

The actor is not one flat prompt-visible personality.

At minimum preserve:

### D. Everything they are and have ever been

The whole generated person, including what remains inaccessible or unknown to the actor:

- all generated history;
- disposition topology;
- causal traces;
- wounds;
- habits;
- defenses;
- latent motives;
- inaccessible memories;
- attractors;
- contradictions;
- organismic/body/material organization;
- relationships and learned relational patterns.

This entire layer may remain causally active without being consciously known.

### C. Who they consciously are to themself most of the time

The relatively stable ordinary self-model, influenced by lived habitus and immediate life organization:

- family;
- friend group;
- job/work situation;
- partner;
- living situation;
- goals;
- burdens;
- optimism/pessimism about the future;
- consciously endorsed identity;
- autobiographical story;
- values and recognized motives.

This self can be dramatically destabilized or turned inside out by generated events such as a catastrophic breakup, psychedelic/drug experience, grief, humiliation, conversion/deconversion, illness, war, migration, love, parenthood, status collapse or other rupture. Such events can expose material the actor ordinarily denies, suppresses or does not know about themself -- their "shadow"/"demons" in colloquial phenomenological terms, without freezing those metaphors as ontology.

### B. What this particular relation and interaction draws out

The active configuration is specifically relational.

It depends on:

`actor × this interlocutor × relationship history × the interlocutor's moves × what they say × the topics they raise × how they say it × the current situation × the actor's current state`.

The interlocutor is not merely a string supplier. They are a specific relational object.

The same words from a lover, parent, boss, stranger, rival, desired person, critic, doctor or someone associated with past hurt can constitute different psychic events.

The interaction may draw out one side, several prongs, contradictory subsystems, or material not normally central to the actor's standing self.

### A. What actually comes out

Expression includes more than chosen disclosure.

It may be:

- intentional;
- strategic;
- spontaneous;
- defended;
- inhibited;
- exaggerated;
- softened;
- disguised;
- postured;
- fronted;
- cool/coy/tough;
- pious;
- status-performing;
- narcissistically performing;
- ironic;
- intellectualizing;
- aggressive;
- confessing;
- silent;
- unexpectedly tender;
- involuntarily leaking.

The actor may give something off without knowing they are giving it off.

Examples that must remain representable:

- attraction produces accidental innuendo the actor does not recognize as flirtation;
- the actor becomes oddly attentive, playful or verbose without recognizing attraction;
- the actor tells a story about a past asshole because the current interlocutor has activated a structural/affective resonance with that person, while the actor consciously experiences the story as merely relevant to the topic;
- an unexpected utterance gives away more than the actor consciously intended;
- the actor hears themself say it and only afterward realizes something about their own state.

## 2. The interaction is a coupled dyadic dynamical system

Conversation must not be modeled as:

`static persona + current user message -> response`.

It is closer to:

```text
interlocutor expression at t
-> actor perception
-> actor activation
-> actor conscious field
-> actor defense/presentation
-> actor observable response
-> interlocutor's next response
-> actor's changed perception/activation at t+1
-> ...
```

This is where relational "chemistry" and anti-chemistry live.

A flint-like pairing may repeatedly recruit and amplify particular parts of each participant.

A wet-blanket pairing may repeatedly inhibit, flatten, derail or extinguish attempted activation.

The same actor can therefore have highly different conversational dynamics with different interlocutors without changing underlying identity.

The PFF architecture must be able to represent both positive resonance and suppression/dampening produced by the specific dyad.

## 3. Surface discourse must first be translated into machine-defined interaction coordinates

The first LLM-facing stage is not allowed to invent free-form psychological ontology.

The persona-state machine / PFF ontology predetermines the legal categories/dimensions.

The LLM translates the actual utterance-in-context into those categories.

The encoder must be able to consume:

- lexical substance;
- discourse history;
- topic;
- speech act;
- conversational move;
- tone/style where available;
- intimacy/distance;
- teasing/criticism;
- assertion/presumption;
- status positioning;
- vulnerability bids;
- ambiguity;
- who/what is being targeted;
- how the message relates to the previously described situation rather than simply to the actor.

The sentence:

`Oh come on, you know you loved the attention.`

may, depending on context, be:

- heavily flirtatious;
- playfully teasing;
- critical;
- face-threatening;
- a claim of familiarity/intimacy;
- an accusation of hidden motive;
- mostly commentary on the situation previously described rather than an attack on the person;
- or a mixture of several readings.

The encoder must preserve those alternatives rather than force a single intuitive winner.

## 4. Numerical / dimensional / directional / scoped / multiple-reading encoding

The desired interaction representation is pre-registered and machine-readable.

Where the final ontology warrants it, a dimension may carry separately:

- magnitude/intensity;
- direction/polarity;
- confidence;
- probability/interpretive weight;
- target binding;
- participant role;
- discourse scope;
- temporal scope;
- relational scope;
- ambiguity;
- multiplicity.

Do not collapse intensity into confidence.

A strong-but-uncertain flirtation reading differs from a mild-but-high-confidence flirtation reading.

A single message may produce a distribution over several non-equivalent readings.

The exact numeric systems, scales, priors, calibration and update equations remain PFF architecture work and are not adopted by this appendix.

## 5. Encoder output is candidate measurement, never direct psyche mutation

The discourse encoder may nominate/measure only within the registered PFF coordinate system.

It may not write:

- attraction;
- shame;
- anger;
- trust;
- attachment state;
- memory access;
- self-model;
- RAW state;
- durable V3 state.

It returns an `InteractionSignalCandidate` / mixture or terminal equivalent.

Only the governed receiver/perception and psyche-transition machinery may alter live person state.

`LLM_ENCODER_OUTPUT != PSYCHIC_STATE_CHANGE`.

## 6. Signal-as-sent, signal-as-discursively-observed, speaker-intention and receiver-perception are distinct

Preserve:

```text
utterance bytes
!= surface/discourse interaction encoding
!= actual speaker intention
!= receiver perception
!= receiver psychic effect
```

The first LLM's output should represent the interaction as inferable from available discourse evidence, not omniscient access to the human user's true intention.

Ambiguity about the sender remains ambiguity.

## 7. Persona-specific perceptiveness / responsiveness / distortion / friction

How the message "is" is not how it necessarily hits.

The receiver's own generated organization transforms incoming interaction coordinates.

The transform may depend on:

- perceptual sensitivity;
- perceptual blindness;
- learned expectations;
- standing self-model;
- relationship history;
- current affect;
- active defenses;
- current RAW state;
- attraction/aversion;
- shame;
- rejection sensitivity;
- status sensitivity;
- prior memory/resonance;
- current bodily/organismic condition.

The transformation may:

- amplify;
- attenuate;
- reweight;
- redirect;
- cross-convert;
- preserve uncertainty;
- produce competing received readings.

Examples:

```text
care -> control pressure
curiosity -> intrusion
teasing -> humiliation
weak distance -> strong rejection
deference -> insincerity
ambiguous friendliness -> flirtation
flirtatious ambiguity -> mockery/threat
```

Different actors may receive the same encoded interaction very differently.

This receiver transformation is part of personality.

## 8. "Friction charges" / psyche-substance transduction

The originating intuition must be preserved even if the final machine uses different terminology:

surface conversational substance is translated into bounded, typed "psyche substance" / perturbations; those perturbations interact with the already-active psyche state; the psyche performs the substantive transformation; then a changed directional/trajectorial state is translated back into surface discourse.

In abstract form:

```text
CONVERSATIONAL SUBSTANCE
-> CANONICAL PSYCHIC PERTURBATION SPACE
-> PERSON-SPECIFIC STATE ALCHEMY / TRANSITION
-> DIRECTIONAL EXPRESSION TRAJECTORY
-> CONVERSATIONAL SUBSTANCE
```

The middle computation must not operate merely as paraphrased conversational semantics.

It must operate on PFF-defined psychic coordinates and state relations.

The metaphors "friction charge", "psyche substance" and "alchemy" are conceptual aids, not frozen ontology.

## 9. Real mutable and stored RAW live state

There must be an actual state that is changed, stored and active.

The system must not reset to a personality baseline every turn.

A current turn strikes the state produced by prior turns.

RAW must support:

- activation;
- inhibition;
- unresolved tension;
- relational charge;
- attraction/aversion where governed;
- active memory/resonance;
- defensive configuration;
- conscious/peripheral availability;
- presentation posture;
- leakage pressure;
- activation origins;
- persistence/hysteresis;
- reinforcement;
- suppression;
- rebound potential;
- cross-activation.

A state may linger after the semantic topic changes.

Jealousy activated three turns ago need not vanish merely because the interlocutor changes topic.

## 10. Multiple persistence timescales

At least distinguish:

### Turn-ephemeral state

Examples:

- focal attention;
- immediate affect;
- current conversational move;
- momentary expression pressure.

### Session / relationship-live RAW state

Examples:

- accumulated tension;
- playfulness;
- guardedness;
- unresolved activation;
- lingering shame/anger;
- active echoes;
- current defense configuration;
- current presentation posture.

This is mutable every turn and stored across turns.

### Durable V3 person state

Examples:

- lasting relationship change;
- generated memory;
- belief/self-model change;
- disposition update;
- durable wound/reinforcement;
- attractor change.

A session may strongly alter RAW without creating durable life history.

Conversely, one interaction may sometimes be significant enough to pass through V3 admission and produce lasting change.

## 11. The psyche transition must be nonlinear and relational

The received perturbation does not merely add independent scalar values.

Existing states interact.

Conceptual examples:

```text
perceived intimacy × attraction -> approach activation
perceived intimacy × shame-of-need -> inhibition
being seen × desire-to-be-seen -> reward
being seen × self-concealment -> threat
attachment need × rejection cue -> reassurance pressure
attachment need × shame × counterdependence -> anger / coolness / denial
```

Activation and inhibition can coexist.

A high underlying motive may therefore produce low explicit disclosure plus high leakage.

Personality resides partly in these characteristic transformation dynamics, not only in stored trait levels.

## 12. Present conscious field is computed from altered live state

After RAW changes, the machine computes what is available to the actor right now.

Potential distinctions include:

- focal;
- peripheral;
- felt but unnamed;
- bodily felt;
- remembered;
- conceptually recognized;
- consciously interpreted;
- self-recognized;
- uncertain;
- intrusive;
- suppressed;
- inaccessible despite activation.

The actor's own conscious explanation may be partial, defensive or wrong.

Examples:

```text
causal activation: attraction
conscious experience: nervous excitement
self-interpretation: "they're annoying / I'm just joking"
explicit attraction-recognition: absent
```

or:

```text
deep resonance with past person: active
story memory: consciously available
recognition that current interlocutor resembles old person: absent
```

## 13. Expression/defense mediation occurs after consciousness

What is consciously available does not automatically become speech.

Preserve distinct operations for:

- deliberate disclosure;
- concealment;
- suppression;
- defensive transformation;
- impression management;
- posture;
- status display;
- coyness;
- bravado;
- piety;
- intellectualization;
- irony;
- deflection;
- strategic silence;
- emotional exposure;
- involuntary leakage.

Some defenses/presentations may themselves be only partly conscious.

The actor may sincerely experience a defensive rationalization as the obvious reason they are responding.

## 14. Hidden cause quarantine and surface consequence translation

The deep mediator may know hidden causal material that the final renderer must not receive as actor-known content.

The system may translate:

```text
hidden:
latent attraction active
actor does not recognize it
old relational echo active
```

into renderer-visible consequences:

```text
slightly increased playfulness
unusual attentiveness
greater spontaneous elaboration
possible unintended double meaning
avoid explicit romantic admission
do not explain hidden causal dynamics
```

The final renderer enacts consequences without narrating omniscient psychology.

## 15. The final renderer must again receive the actual surface discourse context

The system does not render from psyche coordinates alone.

After the deep state computation, the renderer must again be grounded in the actual current conversational substance so that it can produce a semantically coherent answer to what the interlocutor actually said.

Conceptually:

```text
actual discourse context
        + bounded actor-conscious material
        + current relationship/situation
        + expression trajectory / leakage constraints
        -> final LLM surface realization
```

The deep state changes direction and style; it does not replace the conversational semantics the response must answer.

## 16. Context limits: whole person outside prompt

The entire person must not be serialized into every render prompt.

The persistent stores and retrieval system know the person.

Each turn constructs a bounded "this person right now" working packet.

Analogy:

```text
whole durable person = disk
RAW live state       = RAM
compiled prompt      = cache
LLM                  = realization engine
```

The renderer need not contain the entire person to express the whole person correctly if upstream retrieval/activation determines which pieces matter now.

## 17. Multi-channel depth retrieval

Do not rely on simple semantic nearest-neighbor retrieval.

Candidate retrieval should independently consider, where governed:

- immediate discourse semantics;
- interlocutor identity;
- relationship history;
- standing self-model;
- current live session state;
- associative memory;
- affective/relational structural resonance;
- defensive/threatened material;
- attractor/motif organization;
- contradiction/compartment activation;
- current goals and burdens.

This permits non-obvious but person-specific resonances.

## 18. Memory is reconstructive in actor-side organization

Preserve the useful intuition associated with Inside Out without literalizing the movie.

Objective generated history remains immutable.

Actor-side memory can change in:

- accessibility;
- certainty;
- affective coloring;
- associative links;
- self-relevance;
- interpretation;
- relation to present motives/self-model.

A retrieved memory can "change character" when touched by new present experience without rewriting what objectively happened.

A standing self-organization may destabilize enough that previously integrated "personality islands" or self-model subsystems crumble/reorganize.

Depression-like states may make classes of memories difficult to access or retrieve specifically without deleting objective history.

## 19. Current self and deep person exert two-way pressure

Do not model only:

`deep person -> self-model -> expression`.

Also preserve:

```text
interaction
-> relational activation
-> temporary conscious/self-model reorganization
-> recruits/suppresses/exposes deeper material
```

and across sufficiently significant admitted life events:

```text
repeated/strong activation
-> self-model destabilization
-> memory reinterpretation
-> motif/relationship topology change
-> durable V3 person change
```

## 20. Own-output self-observation

The actor observes themself speaking/acting.

An unexpected rendered utterance can itself become a perceptual input.

Therefore:

```text
actor observable output
-> self-observation
-> RAW / conscious-field update
```

In causal mode, durable consequences still require exact V3 admission.

## 21. LLM stages may reuse a technical model while remaining authority-separated

The discourse encoder and surface renderer may technically use the same underlying model/provider, but they are separate calls with different:

- schemas;
- allowed input;
- allowed output;
- authority;
- visibility into hidden state;
- randomness/replay receipts.

A future architecture may add an additional LLM-mediated nomination stage if justified, but no LLM stage may become the hidden psyche state machine.

## 22. Core negative test

If the system can be replaced without meaningful loss by:

`persona dossier + conversation history + one roleplay prompt`

then PFF has failed.

If the LLM can directly decide hidden psychological state, PFF has failed.

If changing interlocutors does not lawfully change which parts of the same generated person activate, PFF has failed.

If an unconscious cause can only affect expression by being explicitly revealed to the renderer as actor knowledge, PFF has failed.

If the live state does not persist across turns, PFF has failed.

If ambiguity is forced into one reading because the model prefers it, PFF has failed.

## 23. Authority ceiling

This appendix banks requirements and design intuitions only.

It does not:

- adopt final categories;
- adopt numerical scales;
- adopt formulas;
- claim psychological science has uniquely fixed the machine;
- authorize implementation;
- authorize V2 or an LLM to mutate durable V3 personhood;
- supersede existing authority without explicit PFF/HQ architecture return.

The PFF Vozhd must preserve these requirements while deriving the actual governed architecture.
