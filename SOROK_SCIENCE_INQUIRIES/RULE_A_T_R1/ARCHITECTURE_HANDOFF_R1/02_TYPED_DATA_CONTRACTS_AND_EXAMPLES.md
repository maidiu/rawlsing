# 02 — Typed sourcefree data contracts, authority matrix, reference episodes

**Interpretation:** These are *candidate inter-component DTOs*; exact field/API mapping, spelling and authorization must be reconciled to live Sorok/ADP/V3 code by competent Codex HQ. A JSON field `state_link` does **not** create a psychological fact or grant a CAN011 update. `06_SOURCEFREE_CONTRACT.schema.json` is deliberately partial, validates boundary shape rather than scientific semantics. Constraints below require semantic/integration verification beyond JSON Schema.

## 0. Source and authority typing convention
For every object attach:
```text
identity:     schema/version, stable ID, branch ID, person/actor ID, source ID/version/hash
temporality:  effective_at, observed_at or discovered_at, event_clock, causal parent refs
jurisdiction: owning authority, permitted read role, recipient/visibility class
epistemics:   OBSERVED | ACTOR_REPORTED | THIRD_PARTY_ATTRIBUTION |
              INFERRED_HYPOTHESIS | DERIVED_CACHE | ADOPTED_CAUSAL_EFFECT | UNKNOWN
grade:        TEST_ONLY | DOCUMENTARY | ADOPTED_SEMANTIC | NATIVE_ISSUED_EXACT
uncertainty:  explicit no-access, missing, ambiguous, contradiction and NO_CHANGE
```
`source_event_ref` always identifies actual event body and holder, never a paragraph summary. Human/actual user records require privacy/purpose/retention controls from competent owners; DTO is not permission to profile or expose inferred traits.

## 1. Persistent object families and write permissions
| Object / proposed store | Required content and relation | Writer | Consumer |
|---|---|---|---|
| `SocialLanguageWorldRef` (reference/index) | `world_id, version, source_grain, milieu, speech_practices, register/convention evidence, community/time/situation, discourse_sense_refs`; may be incomplete/uncontested/contested | generated world/social source or lawful curated reference, NOT output renderer | linguistic discovery/compilation only; never direct psyche seed |
| `ConceptSenseRef` (versioned reference) | `concept_id, sense_id, source_discourse_id, gloss, scope, contestation_refs`; cross-language mappings many-to-many | legitimate reference/corpus index owner | concept relation analysis |
| `LexemeRef` (reference) | `lexeme_id, BCP47 language tag, orthography/transliteration if justified, pragmatic functions/sense candidates, fixed expression vs quote status` | legitimate language/actor exposure index | retrieval and translation, not identity prediction |
| `LanguageEncounterEvent` (immutable) | actual speaker, actor recipients, exact multilingual span(s) or lawful media, language access, situation, objective auditory/visual exposure, temporal refs | actual event/world/ADP19/C8 owner | actor knowledge/perception; later index |
| `ActorConceptRelationCandidate` (nonauthoritative index) | actor, concept/sense/lexeme, milieu and source speaker, personal-relation hypotheses (multiple), source refs, conflicting evidence, confidence **epistemic grade** | semantic extractor *as proposal*; index compiler after validation | source retrieval/provisional expression, never CAN011 target |
| `ActorLanguageKnowledge` (owner-referenced) | available language comprehension/expression, learned discourses/registers, actual episode evidence, partial/unknown limits | competent actor knowledge/ADP17/16 owner ONLY where already authorized; else TEST_ONLY evidence projection | actor-only speech feasibility |
| `ActorSelfAccountEvent` (immutable) | exact utterance/text, professed belief/description, addressee, circumstances, truth-claim status `ACTOR_SAYS` | admitted actor speech/world owner | self-model and hypothesis; not authoritative psyche |
| `SocialAttributionEvent` (immutable) | external named speaker says subject is X, actual recipients/hearing, contestedness, quote scope | admitted external actor speech owner | listener's perspective/memory only |
| `RepertoireSnapshot` (derived cache) | one person branch, state/source digest, multiple milieu-specific language-world slots, current expression tendencies, contradictions, negative cases, illustrative examples, cache TTL/invalidation | background/foreground deterministic index/compiler + optional LLM abstractor; **CACHE_ONLY** | actor expression prompt projection only |
| `RelevantMediationPacket` (ephemeral) | actor-accessible current event and history refs, qualified state links, nonauthoritative candidate concept relationships, rival readings/NO_CHANGE; perspective-limited | transduction/composer request router | owner adjudicators, actor realization |
| `ActorExpressionCandidate` (ephemeral) | exact proposed speech spans & language, audience/addressee, act/gesture/world occurrence slots, intended pragmatic function (interpretation, not source truth) | actor realization LLM | V2/admission gate, then writer |
| `AdmittedSpeechOccurrence` (immutable) | exact committed actor words and language spans, timing/audibility, physical co-event, source hash, branch/time | competent actor world/V2/ADP19/C8 writer | actual future history; user projection |
| `TranslationProjection` (derived) | source occurrence ID/hash and span offsets, target language, projection text, retained/omitted address/pragmatics, confidence/loss markers | authorized read-only translation/composition service | user presentation; NEVER source actor speech |
| `UserPhenomenalView` (derived/binding where actually emitted) | admitted observable event IDs, user's actual sensory/linguistic access, permitted attention selection, exact dialogue or labeled translation, no actor hidden state | user-facing compositor governed by Sorok101 | user only; emitted particulars constrain future record |

Do not create independent canonical stores for CAN010/011/ADP15/16/17. Language index uses **references** to those owners, not copies of their hidden mutable psychological contents.

## 2. `LanguageEncounterEvent` and lexical uptake states
**Candidate shape:**
```json
{
  "schema": "LME_LANGUAGE_ENCOUNTER@1",
  "event_id": "evt-001",
  "branch_id": "root-or-user-branch",
  "effective_at": "2031-04-08T14:05:00Z",
  "speaker_actor_id": "B",
  "audience_actor_ids": ["Nadia"],
  "kind": "ACTUAL_SPEECH",
  "utterance": {
    "spans": [
      {"language_tag": "es-MX", "text": "Primero terminemos esto. Luego hablamos.", "span_role": "SPOKEN"}
    ],
    "speech_act_candidate": "DEFER_DISCUSSION",
    "register_candidate": "WORKPLACE_PRACTICAL"
  },
  "source": {"owner": "ADP19_TEST_ONLY", "ref": "receipt-evt-001", "content_hash": "verified-at-runtime"},
  "perception": {"actor_id": "Nadia", "perceived": "SOURCE_REQUIRED", "actor_access_receipt_ref": null},
  "epistemic": "OBSERVED"
}
```
The sample text is an invented fixture for a hypothetical Spanish-speaking actor; no normative claim about Mexican Spanish or Nadia's real biography. `speech_act_candidate` and `register_candidate` cannot prove motives. A source-language utterance can contain multiple spans; if quoted foreign words are *quoted*, tag `QUOTED`, not spontaneous code-switch. `perceived` is independently proved, not freely set true by an LLM proposal.

The occurrence does not by itself imply the recipient learned those words, understood them, agreed or remembered. Qualified owners may separately emit `OBSERVED_HEARING`, `KNOWN`, `UNKNOWN`, `EXPOSED_NOT_COMPREHENDED`, `ACTOR_REPORTED`, etc. No one universal proficiency rating or ethnic first-language rule.

## 3. `ActorConceptRelationCandidate` (sparse many-to-many, not one score)
```json
{
  "schema": "LME_ACTOR_CONCEPT_RELATION@1",
  "candidate_id": "acr-001",
  "actor_id": "Nadia",
  "branch_id": "root-or-user-branch",
  "concept_id": "concept:independence",
  "sense_id": "sense:familial-competence",
  "source_discourse_id": "milieu:nadia-family-at-period-P",
  "context_scope": ["FAMILY", "SELF-ASSESSMENT"],
  "relation_labels": ["FAMILIAR", "AMBIVALENT", "SELF_APPLIED"],
  "evidence_refs": ["evt-parent-maxim", "evt-nadia-self-description"],
  "contrary_evidence_refs": ["evt-a-accepts-help", "evt-a-defends-others-dependence"],
  "status": "INFERRED_HYPOTHESIS",
  "owner_effect_ref": null,
  "declared_not": ["GLOBAL_IDEOLOGY", "CAN011_ACQUIRED_PRACTICE", "PRIVATE_MOTIVE_FACT"]
}
```
The same actor/concept simultaneously permits:
- `sense:family-self-reliance` with `AMBIVALENT,SELF_APPLIED`;
- `sense:civic-autonomy` with `AFFIRMED_FOR_OTHERS`;
- `sense:class-critique-of-individualism` with `EXPOSED,CONTESTED`;
- `sense:work-competence` with `PRACTICED` **only where actually supported**.
These are *different relations/senses*, not duplicate normalized weights or a conflicting-value bug. `unknown` and `absent` remain different.

## 4. `RepertoireSnapshot`: compiler output and validity
```json
{
  "schema": "LME_REPERTOIRE_SNAPSHOT@1",
  "snapshot_id": "rep-01",
  "actor_id": "Nadia",
  "branch_id": "branch-U",
  "compiled_from": {
    "person_state_digest": "validated-digest",
    "event_ref_set_digest": "validated-digest",
    "source_ref_ids": ["evt-parent-maxim", "evt-class-lesson", "evt-work-episode"],
    "lexical_relation_index_version": "test-v1",
    "compiler_contract": "LME_COMPILER@1",
    "language_model_identity": "recorded-if-used"
  },
  "worlds": [
    {"milieu_id": "family", "register": "FAMILIAL", "availability": "CONTEXTUAL",
     "ordinary_expression": "practical indirectness", "tension_refs": ["acr-001"],
     "source_event_refs": ["evt-parent-maxim"], "exception_refs": ["evt-a-accepts-help"]},
    {"milieu_id": "work", "register": "TASK_PRACTICAL", "availability": "CONTEXTUAL",
     "ordinary_expression": "short task-centered directives", "tension_refs": [],
     "source_event_refs": ["evt-work-episode"], "exception_refs": []}
  ],
  "charged_concept_refs": ["acr-001"],
  "counterexamples_preserved": ["evt-a-defends-others-dependence"],
  "not_authorized_for": ["CAN008_CAUSAL_RULE", "CAN011_DURABLE_WRITE", "ACTOR_HIDDEN_SELF_TRUTH", "USER_FACING_PRIVATE_PSYCHOLOGY"],
  "status": "DERIVED_CACHE"
}
```
`ordinary_expression` text is a compiler hypothesis used at qualified actor realization grade; never becomes direct psychology. Source-linked exceptions are first-class. For same branch/time/source state, deterministic compiler input canonicalization and recorded model/config must make snapshot reproductions attributable, even if stochastic compiler output is not bit-identical. On source contradiction, state update, or invalid dependency, invalidate/recompile without changing earlier events.

**Functional requirement:** current whole-person **expressive** substrate is retained (Sorok101 §19), not replaced by a sparse top-k retrieval. The repertoire slot is one element of a larger sufficient actor packet; omission must pass conditional counterexample tests.

## 5. Proposal and owner-decision boundary
```text
Rawlsing transduction model candidate packet:
  proposed_world_refs[] (not true until world authority)
  candidate_relevances[]  {
    concept/sense, person_state_refs, history refs,
    applicability hypothesis, positive/negative evidence, uncertainty,
    proposed_owner_and_read_role
  }
  request_to_CAN008? (current coupling, no automatic response)
  request_to_CAN011? (only admissible source/owner precondition,
                       no automatic learning)
  actor_knowledge_requirements[]
  user_perception_requirements[]
```
Owner router verifies referenced source bodies, granted role, valid time, actor knowledge, qualified rule ID and exact ownership. Reject fabricated refs and transitions. An authorized current CAN008 result may be UNKNOWN or VALID_EMPTY. A CAN011 denial retains exact NO_CHANGE, not a ghost middle state. Actor realization receives only actual admitted response, permitted relevant repertoire, actor-accessible knowledge and context; do not provide "possible hidden motive" as narrative fact.

## 6. Actor expression and user display contracts
```json
{
  "schema": "LME_ACTOR_EXPRESSION@1",
  "candidate_id": "speech-001",
  "actor_id": "Nadia",
  "branch_id": "branch-U",
  "audience_actor_ids": ["U"],
  "source_context_ids": ["scene-1"],
  "speech_spans": [
    {"language_tag": "es-MX", "text": "Primero terminemos esto. Luego hablamos.", "role": "SPOKEN"}
  ],
  "observable_gestures": [],
  "actual_code_switch": false,
  "pragmatic_intent_hypothesis": "TASK_FIRST",
  "epistemic": "INFERRED_HYPOTHESIS",
  "admission_ref": null
}
```
After authorized V2/external occurrence admission, the exact speech text becomes binding. If later displayed to an English user:
```json
{
  "schema": "LME_TRANSLATION_PROJECTION@1",
  "source_admitted_speech_ref": "admitted-speech-001",
  "source_utterance_digest": "actual-speech-digest",
  "target_language_tag": "en",
  "text": "Let's finish this first. Then we can talk.",
  "source_language_tags": ["es-MX"],
  "render_mode": "ENGLISH_TRANSLATION",
  "loss_notes": [],
  "status": "DERIVED_CACHE"
}
```
This is a read-only display projection; do not append it as a new actor speech, or hallucinate that Nadia knows English. English itself might be Nadia's actual utterance if actor evidence shows genuine bilingual speech: then `speech_spans.language_tag="en"`, and it is NOT tagged as a translation.

If Nadia speaks source language with multiple linguistic fragments, preserve boundaries; code switching is actor-selected and source-authorized. Different English renderings of *the same* utterance may be compared, but they may not introduce contradictory speech acts, invented political vocabulary, unspoken honorifics, emotion or interlocutor effects.

## 7. Branch and speaker-model segregation (security tests)
```text
Nadia expressive packet MAY contain:
  her actual person state or admitted actor-safe projection,
  her accessible repertoire and relevant source utterances,
  her model of U, relation history, metaperception,
  her intended audience and current situation, user speech she heard.
MUST NOT include for Nadia:
  Rawlsing's private inference about U presented as verified U beliefs,
  U's unspoken thoughts, other actors' inaccessible accounts,
  a future translation intended for U as a constraint on her "real" language.

User phenomenal packet MAY contain:
  objective admitted Nadia speech/actions and event timing,
  U's actual sensory/linguistic competence and prior observed record,
  bounded Rawlsing U-model for selection *without asserting it as fact*.
MUST NOT contain:
  private Nadia motivational records, her inaccessible intentions,
  unspoken mental accounts or unperceived third-person B intention,
  exact English translation as if physical Nadia speech.
```

## 8. Cross-turn cache, compaction and anti-fantasy controls
- Index candidate concept relation only after `source_ref`/person relation proven authentic. A language source may be kept even if no new psychological owner effect permitted.
- Before recompilation: read current whole-person expressive substrate and relevant lineage index; retrieve contested exceptions; compile plurality **without** requiring a single synthesis/summary worldview.
- Compile by *source + version*, not previous compilation. Retain historical source ID and compiler config; replace invalid caches atomically.
- A cache can expire based on clear world change, a new encountered discourse, concept reformulation, observed audience sanction or actor ownership update. Engineering cap may trigger recompilation, but cap is not a psychological decay law.
- When cache compiler omits material expression difference across a significant source-severance pair, enlarge or partition the cache, or return `EXPRESSION_CONTEXT_INSUFFICIENT`; never repair by declaring person "simple" or rewriting source history.
- Explicit NOT_RUN/UNKNOWN on scientific warrant and model fidelity metrics. LLM structured output invalid or source/privilege check failure -> reject; no partial durable write.
