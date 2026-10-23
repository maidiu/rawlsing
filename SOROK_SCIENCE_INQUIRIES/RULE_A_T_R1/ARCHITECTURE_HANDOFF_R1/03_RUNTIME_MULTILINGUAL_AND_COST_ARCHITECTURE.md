# 03 — Runtime recursion, native/translated speech, call budget and failure semantics

**Proposed workflow only.** Reconciles Sorok101 (§§2,7–8,12–13,15–19,21–25), 100 app-local continuity and 00E person-first demands. Zero native issuances, zero provider calls and zero runtime tests in this packet. A `MUST` here states a **candidate engineering acceptance invariant**, not a new controlling project law until HQ acceptance.

## 1. Every-turn execution: same owner machine, different minimum competent grain
```text
PRECONTACT PERSON + BRANCH-CURRENT NADIA + USER-NADIA RELATION
                                      │
EXACT USER SAY/DO/ATTEND ────────────┤
                                      ▼
[M1 semantic transduction; ~one normal LLM call]
  parse actual user words/attempted action/attention
  propose structured world/actor events and relevance hypotheses
  retrieve source-linked linguistic concepts and historical counterexamples
  propose owner operations without factual/source/psychology promotions
                                      │
                                      ▼
[deterministic owner router/admission and relevant retrieval]
  validate source/rights/time/branch/object/sensory and actor access
  admit real permitted user/world event
  distinguish Nadia's actor model of U from system model of U
  fetch current whole-person expressive substrate + bounded linguistic cache
  owner-specific CAN008 or other lawful grain → response/unknown/no-effect
  if eligible durable rule/permission exists, owner may evaluate separately;
  otherwise NO_CHANGE; *never* invent missing CAN011 T
                                      │
                                      ▼
[M2 actor realization; ~one normal LLM call]
  context: actor-owned Nadia + actor-limited relations + current lawful event
  + relevant plural repertoire, exceptions and multiple social languages
  propose chosen action, exact native/multilingual speech and observable detail
  not user's private psychology, not compelled cultural marker/stereotype
                                      │
                                      ▼
[typed actual-world/V2/admission gate]
  validate physical feasibility and original actor speech identity/language
  freeze objective occurrence and enacted source refs, admissible actor effects
  invalid candidate → controlled bounded failure; no silent narrative write
                                      │
                          ┌───────────┴───────────┐
                          ▼                       ▼
[USER VIEW SELECTOR]                    [FUTURE CAUSAL HISTORY]
  exact speech / approved                 append source event,
  faithful display translation            audience reactions,
  sensory/attention projection            actual conceptual encounter,
  with no private leakage                 source-justified effects only
                          │                       │
                          ▼                       ▼
USER-OBSERVED TURN             [SELECTIVE INDEX + CACHE INVALIDATION]
                                updates provenance, optional *derived* repertoire,
                                preserving unobserved histories and dissent
```

The screen text becomes binding if it asserts physical occurrence beyond the typed event, per Sorok101 §8. Prefer typed outward occurrence first; any text-flesh co-realization must pass event/body equivalence. In the sourcefree alpha, truthful no-action/no-speech/uncertain behavior is valid. A missing original T must not block a real word from being spoken where actor-expression sourcefree rights exist.

## 2. Two fundamental loops, not two independent psychologies
**LIFE RECURSION** (historical/offscreen): independently generated persons encounter actual institutional, material, intimate, linguistic and cultural relations over meaningful time; source-admitted events and actor actions accumulate. Repertoire index may evolve through lawful exposure, interpretation and acts. Durable psychological organization changes **only** via active competent rule/owner (else NO_CHANGE). This can be batched; no required on-screen user.

**USER TURN** (live): current spoken/acted user contribution enters Nadia's own perceptual/relational history; actor expression is generated from the current whole person plus relevant tail; user surface is then selected/transliterated/translated without rewriting Nadia's act. App-local branch effects stay branch-local; precontact canon is not rewritten to flatter the user.

Both loops share the same `event → owner validation → current bounded response → independently enacted action → optional owner-sanctioned durable effect → source-linked memory/index` contracts, but use distinct scheduling, costs and source permissions.

### Per turn stage table
| Stage | Owner/type | Output | Non-negotiable negative |
|---|---|---|---|
| U0 User exact utterance/act | interaction/ADP19 gate | quote/attempt/perception condition | no inferred user intention becomes fact |
| U1 Relevance proposals | transduction LLM, `CANDIDATE` | target source refs + hypothesis + alternatives | no CAN008/T update by tool arguments |
| U2 Objective admission | proper event/world owner | admitted event/time/hash or DENY | no pre-event C9 evaluation on a fantasy event |
| U3 Actor receiver | Nadia allowed actor knowledge & relevant history | reception/access allowed/unknown | objective B act not Nadia thought |
| U4 Current response | CAN008 exact concrete rule if issued, else typed permitted baseline/unknown | actual current response/NO_CHANGE | cannot invent durable practice |
| U5 Expression selection | V2/actor source | actual speech/action/gesture candidate | no user-model secret driving Nadia's act |
| U6 Exact admission | actor occurrence writer | hash-stable visible occurrence | no changed actor dialogue in final rendering |
| U7 Display selection | user lens + translation | source or labeled translation + lawful observed detail | no hidden motive reveal; no dialect/nationality caricature |
| U8 Historical accrual | actual event/knowledge/linguistic index owners | event refs + selective invalidation | no "summary says so" event |
| U9 Durable eligibility | independently governed CAN011/ADP where actually eligible | committed effect or typed NO_CHANGE | no event-label-to-psyche shortcut |

**U4** absent concrete A rule may mean no claimed subjective uptake. V2/sourcefree constraints must keep this honest; no arbitrary new actor psychological inference slips through linguistic machinery.

## 3. Linguistic repertoire compiler: when and how
Input:
- versioned accepted current actor/person snapshots, all relevant plurality/contradiction source links;
- source-grounded vocabulary/acquisition and register evidence;
- socially located discourse references and histories of accommodation, sanction and ironic resistance;
- actor's currently accessible languages and domain competencies;
- one or more recent relevant counterexamples where a generic summary would be false.

Output:
- `RepertoireSnapshot`: 2–N meaningful independently indexed linguistic worlds **without forced coherence**; contextual availability and potential audience/register differences, charged concept links, source exceptions, expression examples, distributional guards.
- signed/cache-hashed source digests; `NOT_A_CAUSAL_RULE`; permits retrieval by actor and current context.

**Compiler discipline**
- Trigger on evidence/version changes materially relevant to expression; never unconditionally regenerate on every turn.
- Compile from primary source and current governed state, not the previous LLM paraphrase. Repeated compiler passes without new source must not increment invented personality attributes.
- Keep references to contested terms, sources of terms (who said it, in what milieu), actor stance evidence, contradictory self accounts, different code/translation contexts.
- Caches may be regenerated deterministically for record selection. If LLM abstractor involved, preserve model/provider/parameters/version, snapshot input digest, and audit outputs; stochastic outputs need not be exact-string stable but semantically invariant claims must be source-checked.
- Under finite token budget, prioritize whole-person expression substrate, then context-relevant repertoire and disconfirming sources; avoid merely `top-k similarities`. Cache omission must be tested against meaningful alternate histories.

**Provisional pilot budgets only, not hard limits on the person:** 3–7 prominent register/milieu slots; 10–30 indexed charged concepts; 2–4 episode anchors per live use; ~300–600 tokens of cached repertoire, plus current whole-person and relation context. No fixed universal quotas and no commitment these suffice until tested. Smaller baseline may outperform larger cache for ordinary speech.

## 4. Native-language fidelity: source speech, translation, and actual bilingualism
Three different axes must be modeled, not a mutually exclusive nationality-style switch:
- **Speaker competence**: exact linguistic history/ability and situated practice; possibly multilingual, receptive-only, partial, uneven across topics/settings; no "native" as single immutable trait. Historical life-context and actor knowledge own this.
- **Actor speech choice**: language/register/code-switch within exact objective admitted utterance. Real code switch can involve a mixed span and is an actual Nadia action; no compulsory ethnic token and no invented English competence just because UI locale is English.
- **User display mode**: `SOURCE_ORIGINAL` or `LABELED_ENGLISH_TRANSLATION` or `DUAL`. Display preference **cannot alter actor speech truth**. Translation is a presentational mediation service, not what Nadia said, and may affect user's comprehension only as a user-facing app affordance.

**Source speech representation**
```text
speech_occurrence_id, speaker_id, situation, speech_act/action identity,
source_spans[]: [{language_tag, verbatim, quoted|spoken|borrowed, offsets}],
timing, addressee, audibility, provenance, actor_language_competence_refs,
actual_code_switch_status, objective gestures and co-occurred events
```
All fields tied to actual admitted source. If culturally specific phrase arose from real Nadia repertoire, preserve; do not inject a "marker" at display layer. Borrowed words (“habibi,” “hombre”), formulaic religious phrases, kinship address and lexicalized everyday expressions require **pragmatic-context-sensitive** retention/translation, not fixed dictionary substitution. Their literal translations may sound elevated, exoticized or oddly intimate when original sounds ordinary. Translating *alhamdulillah* as an obligatory “praise be to God” ignores ordinary discourse uses. A speaker can also choose conspicuous phrases intentionally; do not suppress a genuinely warranted marker simply to appear neutral.

**Read-only projection**
- Choose source original when source speech is requested; for English display translate from **the exact admitted source text**, not inferred intent/hidden psychology.
- Mark displayed text as a translation where necessary, preserve links to original and distinguish accessibility through app translation from user's actual native listening comprehension.
- Preserve speech act, stance, degree of certainty, politeness, formality, address function, irony and pragmatic markedness; preserve ambiguity when warranted instead of resolving it in English.
- Never replace a Russian rough's speech with working-class London vernacular or a Mexican working-class speaker with American regional slang by default. Express sociolect using stable pragmatic/register choices rather than a surrogate geography.
- Do not decorate every sentence with original-language terms, exotic vowels, religious formulas or accent misspellings.
- If certain word has no clean equivalent, allow the original form or a restrained footnote/hover explanation *where user requested and available*; don't fabricate a claim of perfect equivalence.
- If translation confidence insufficient, return typed partial/uncertain translation, retain original; never modify original utterance to fit an English rendering.

**Call budget tradeoff**
Sorok101 §15 target is transduction ×1 + actor realization ×1 ordinary turn. Candidate tactics:
1. produce native actor text/typed occurrence in M2; use local/simple translation when qualified, with no additional high-capability model call;
2. optionally obtain a *provisional* English gloss in same M2 structured output, but it is never actor speech and must be independently consistency-gated against committed native text before display;
3. if serious source-language/pragmatic fidelity cannot be met, benchmark a separate **read-only** translation call as a scoped fidelity frontier, measure delay/cost, and seek HQ design deviation; not a compulsory third turn call by fiat.
No mandate for English-first generation followed by invented “original” foreign speech. That risks English-conceptual contamination; treat as alternative with explicit comparative tests, not invisible fallback.

**Sorok101 §13 compatibility question:** original law says exact actor speech preserved in phenomenal view. Translation must be a **typed display affordance over exact speech** and may require a narrow 101 clarification if the governing interface forbids all text substitution, even explicitly labeled translations. Do not silently override 101 by claiming English paraphrase *is* the source speech. This is one specific *engineer/authority integration decision* for Codex HQ.

## 5. Situated ideology and disclosure without caricature
The `repertoire` is not an instruction to announce Nadia's ideology. The expression context can retrieve:
- actor-supported ideological conceptual distinctions, expressed as practical judgments, not keyword quotas;
- contested/ironic/avoidance relations, her own self-accounts distinct from observed commitment;
- which discourses are ordinary in current milieu versus marked in this audience;
- genuine code-switch habits and audience accommodation versus non-deliberative habitual speech;
- actor's own model of what U believes, whether it is erroneous/uncertain;
- actual social stakes/sanctions and source-owned physical/attention constraints.

Do not treat `what audience will reward` as final objective; Nadia may refuse to conform, misjudge interlocutor, reveal more than intended or speak unremarkably. If U has ability to notice a distinctive cue, U phenomenal layer can SELECT a previously admitted objective cue, not generate the cue to make the user feel perceptive. A private ideology has no automatic entitlement to be described explicitly by omniscient narrator.

## 6. Errors, degradation and abstention
```text
CANDIDATE_SOURCE_REF_INVALID          => REJECT PROPOSAL; no writer mutation
ACTOR_LINGUISTIC_COMPETENCE_UNKNOWN  => UNKNOWN; use evidenced plain linguistic ability,
                                        never auto ethnicity/accent stereotype
LME_COMPILER_STALE / CONTRADICTED     => INVALIDATE; rebuild from source or
                                        use verifiably sufficient previous snapshot
CONCEPT_PERSONAL_SENSE_UNSUPPORTED  => omit/relegate to UNVERIFIED, never add trait
CAN008_RULE_NOT_ISSUED               => no invented A effect, valid-empty/unknown
CAN011_TARGET_RULE_NOT_ISSUED        => NO_CHANGE, no ghost target/memory
TRANSLATION_UNCERTAIN                => source text preserved, typed caveat/dual mode
SURFACE_VS_OBJECTIVE_MISMATCH        => withhold offending sentence/refuse admission,
                                        bounded repair in owner scope, not rewrite past
USER_PROFILE_OR_NADIA_PRIVATE_LEAK   => reject/out-of-bounds, no render
FULL_HISTORY_CONTEXT_EXCEEDS_BUDGET => retrieve precise dependency; if impossible,
                                        stop `EXPRESSION_CONTEXT_INSUFFICIENT`
```
No infinite LLM regenerate/rejudge cycle. Any proposed repair path must have capped attempts and a fail-closed result. For sourcefree feasibility demo, a test-only plain utterance or truthful non-response is better than fabricating backstory or physiological diagnostics.

## 7. Latency and scheduling
- Per-turn pathway has 1 semantic proposal call, 1 actor expression call **target**, lawful local/typed routing, 0 mandatory cache LLM calls, 0 mandatory original T loop.
- Compile profile on actual update trigger; use digest validation and memoization for unchanged sources, incrementally index linguistic events.
- For long life recursions batch independent semantic indexing/compilation at checkpoints; do not discard exact event histories or treat summaries as causes.
- Monitor stage latency, provider calls/turn, cache hit/miss, retry count, exact dialogue consistency, translation loss score *as measured design diagnostics*; no claimed current performance numbers.
- If user changes English display language, recompute translated view only; **do not** rerun actor causal choices or commit a different speech event.
- If actor belief/milieu/source changed, retrieve versioned source and invalidate the affected repertoire only; use dependencies, not global recompile on every edit.
- Native live first-neighbor positive is still held by original proof/authority; no sham “shipping done” until all product/custody/human gates with own owners.
