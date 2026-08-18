# ADP-016 — V3 Causal Memory Formation / Forgetting / Recall Authority

**Authority ID:** `ADP-016`  
**RA-R00 authority:** `MUST-016`  
**Canonical machine authority:** `V3_CAUSAL_MEMORY_FORMATION_FORGETTING_RECALL_RULE`  
**Version:** `1.0.0`  
**Owner:** V3 Actor Developmental Causality Engine  
**Mode:** post-architecture authority creation only  
**Whole-machine architecture:** CLOSED  
**Production implementation:** NOT AUTHORIZED BY THIS RESULT  
**Consumer release sufficiency:** `SUFFICIENT` for the `MUST-016` semantic dependency only; all other direct consumer dependencies remain independently binding.

---

## 1. Authority verdict

`PASS`.

This authority binds the V3 causal-memory state machine required by accepted V3/V2 architecture without changing that architecture.

The constitutional separation is:

```text
OBJECTIVE_GENERATED_EVENT_HISTORY
!= GENERATED_MEMORY_STATE
!= CURRENT_MEMORY_ACCESSIBILITY
!= ACTOR_KNOWLEDGE_OR_CLAIM_PERMISSION
!= V2_SESSION_OR_TRANSCRIPT_STATE
!= RENDERED_EXPRESSION
```

V3 objective causal history remains immutable even when an actor memory becomes degraded, inaccessible, uncertain, or content-unavailable. A memory is never created merely because the system possesses objective history. Current memory accessibility is a V3 memory-state property only; it is an input to later `ADP-017`, which alone owns actor knowledge / first-person claim-accessibility semantics.

The authority deliberately supports two terminally useful memory representations:

1. **`EVENT_REFERENTIAL_MEMORY`** — a source-bounded generated memory referencing exact actor-experienced V3 causal event material;
2. **`CAUSAL_TRACE_MEMORY`** — a persistent, possibly nondeclarative/path-dependent causal trace such as lawful pressure-flow groove/conductance history that may affect later causation without implying conscious recollection or first-person claimability.

No third “deep memory” store, biography fallback, prose-derived memory family, or transcript-derived causal memory is authorized.

---

## 2. Evidence and authority priority

### 2.1 Binding current authority inspected

- `state/CURRENT_STATE.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`;
- TD-R05 accepted V3 result;
- TD-R07 whole-machine synthetic-life result, especially Life F;
- RA-R00 `RESULT.md` and `RESULT.json` classification/dependency law;
- W0 `LAUNCH_REGISTER.md` common law and W0-05 cell.

Binding current authority establishes that:

- V3 owns causal memory;
- objective generated fact is not automatically actor-accessible;
- V3 causal memory/accessibility is distinct from V2 transcript/session continuity;
- Life F requires an objective event to remain true after actor memory becomes uncertain or inaccessible;
- `MUST-016` is independent authority and `ADP-016 -> ADP-017` is the dependency order;
- V2 may not promote transcript/render/persona prose into V3 generated memory.

### 2.2 Required historical archive verification

Required logical archive: `Rawlsing_code_bundle_staging.zip`  
Mounted upload inspected: `Rawlsing_code_bundle_staging(4).zip`  
Expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
Computed SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
Verdict: `EXACT_MATCH`.

Historical V3/V2/server source is used only for continuity and authority-recovery evidence. Historical archive V5/DDM has zero authority over current V550+.

### 2.3 Direct recovered source inspected

Seam-relevant source included:

- `v3/core/state.py` — `events_this_year`, `micro_trace_this_year`, `pressure_flow_history`, `pressure_flow_memory`, rupture/metabolization state;
- `v3/core/year_record.py` — stable snapshot/hash support;
- `v3/psyche/flow.py` — transactional pressure-flow cycle, `_update_memory`, grooves/conductance, analyst/surface split, `history_evidence_not_persona_voice`;
- `v3/engine/effects/metabolization_effects.py` — event-derived rupture/process persistence plus negative evidence from ungoverned injection paths;
- `v3/engine/event_engine.py` — event IDs/conditioning provenance direction, but nonterminal generic event semantics;
- `v3/io/persona_sheet.py` — legacy prose scene material labeled as “MEMORIES,” used here as negative boundary evidence;
- `v3/tools/distill_memory.py` — prose “memory editor” with input/output provenance, used here as negative boundary evidence for causal promotion;
- `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` — persistent relationship/session-memory concept, used as V2 boundary evidence;
- `v2/conversation_engine.py` — anchored backstory memories and keyword/phrase hooks, used as negative evidence against keyword-triggered V3 recall;
- `server/session_db.py` and `server/session_state.py` — transcript/session persistence and resume behavior, used as negative evidence against transcript -> causal-memory promotion;
- relevant recovered V3 pressure-flow/persona integrity tests.

Focused direct-source verification executed from the exact archive:

```text
25 passed
```

The recovered pressure-flow subsystem is a strong continuity asset because it persists causal routing history/memory/grooves transactionally and marks analyst-only products as non-persona voice. Legacy persona/V2 prose-memory and session surfaces are not terminal causal-memory authority.

---

## 3. Jurisdiction

### 3.1 This authority owns

`ADP-016` owns the generic, versioned V3 rule governing:

- whether an exact V3 generated/admitted causal basis is eligible to form memory;
- creation and stable identity of `GeneratedMemoryState` objects;
- categorical retention/degradation/content-unavailability semantics;
- recall/reactivation and memory-accessibility transitions;
- uncertainty/degradation representation without confabulation;
- persistent causal-trace memory distinct from declarative/event-referential memory;
- provenance, integrity, transition receipts and deterministic replay requirements;
- fail-closed behavior for noncausal sources, stale state, missing provenance, missing rule authority, and unauthorized rehydration from analyst-only history.

### 3.2 This authority does not own

This authority does **not** decide:

- objective event admission or event truth (`ADP-019` and owning V3 event rules govern admission where relevant);
- actor knowledge, belief, nonknowledge or first-person claim permission (`ADP-017`);
- V2 phenomenological projection, salience, disclosure, response planning or rendering;
- V2 transcript retention/summarization/compaction/deletion (`ADP-024`);
- V2 session persistence semantics;
- V3 causal RNG policy (`ADP-020`);
- hybrid scheduler precedence or slow cadence (`ADP-021`);
- numeric pressure-flow/groove formulas owned by compatible V3 response/flow authority;
- structural priors, resolver selection, structural proxying or producer semantics;
- a false-memory/confabulation semantics that invents alternative event detail.

If any implementation requires one of those meanings to execute a memory transition, it must consume the separately accepted authority. It may not infer or default it locally.

---

## 4. Canonical memory identity and object model

### 4.1 `GeneratedMemoryState`

A terminal implementation SHALL represent the semantic equivalent of:

```text
GeneratedMemoryState {
  memory_id,
  actor_id,
  representation_kind,
  formation_transition_id,
  objective_source_event_refs[],
  source_feature_bindings[],
  retention_state,
  memory_accessibility_state,
  uncertainty_state,
  last_transition_id,
  last_transition_effective_time,
  current_state_hash,
  integrity_state
}
```

`objective_source_event_refs[]` contain exact V3 event IDs plus immutable event hashes. A memory object does not copy the objective event into a second mutable biography.

`source_feature_bindings[]` are bounded references to exact source-event facts/effects that this memory retains. Free-text narrative is not a feature binding. Each binding carries at minimum:

```text
{
  source_event_id,
  source_event_hash,
  feature_ref,
  feature_state
}
```

Allowed `feature_state` values in v1 are:

- `AVAILABLE_SOURCE_BOUND` — retrievable memory content remains explicitly bound to the exact generated event feature;
- `AVAILABLE_UNCERTAIN` — memory retains that feature only with governed uncertainty; downstream may not silently upgrade it to exact actor knowledge;
- `UNAVAILABLE` — the actor-memory subsystem may not retrieve the feature value from objective history merely because analyst history still contains it.

No v1 state authorizes invented substitute detail.

### 4.2 Representation kinds

#### `EVENT_REFERENTIAL_MEMORY`

A generated memory of actor-experienced event material. It may carry 1..n exact source event refs where a governed V3 transition consolidates already generated experiences. It never includes a detail that lacks an exact generated causal basis.

#### `CAUSAL_TRACE_MEMORY`

A persistent history-conditioned causal trace that may alter later V3 causal processing while not implying conscious recollection. Recovered pressure-flow history/memory/groove/conductance is the primary continuity example.

A `CAUSAL_TRACE_MEMORY`:

- may have `memory_accessibility_state = NOT_APPLICABLE_CAUSAL_TRACE`;
- is not automatically exportable as persona consciousness;
- is not automatically promotable to `EVENT_REFERENTIAL_MEMORY`;
- may be used by compatible future V3 causal rules only with exact provenance and those rules' own authority.

### 4.3 Stable identity

A memory identity is created exactly once on successful formation and never changes after degradation, inaccessibility, recall or reactivation.

Canonical identity derivation SHALL be deterministic and collision-detectable. A conforming implementation may use:

```text
formation_transition_key = SHA256(
  authority_id
  || authority_version
  || actor_id
  || formation_trigger_ref
  || memory_effect_key
)

memory_id = SHA256("V3_MEMORY" || formation_transition_key)
```

`memory_effect_key` is stable within the parent causal transition and permits one causal event to form 0..n distinct memories without order-dependent IDs.

Replaying the exact same formation effect is idempotent. The same identity with conflicting source refs or post-state is `INTEGRITY_FAILURE`, not a second memory.

---

## 5. Eligible causal parents and formation rule

### 5.1 Constitutional formation gate

A memory may form only when all of the following are true:

1. the causal basis is an exact V3 generated/admitted event or an exact V3 governed causal transition recorded under the accepted event/history architecture;
2. the parent event/transition ID and immutable hash verify;
3. the actor is a governed experiencer/participant/subject for the proposed remembered material, or the proposed object is explicitly a nondeclarative `CAUSAL_TRACE_MEMORY` created by a lawful actor-response/flow transition;
4. every remembered feature is source-bound to generated causal material rather than structural prior, resolver context, prose, or analyst inference;
5. the owning V3 event/rule requests or authorizes a typed memory effect under this authority;
6. the current pre-memory state and provenance satisfy integrity checks;
7. any stochastic choice required by the memory rule has separately accepted V3 causal-randomness authority and a replay receipt; otherwise the stochastic transition blocks.

Eligibility means **may form**, not **must form**. The existence of an objective event does not itself create a memory.

### 5.2 Eligible parent classes

Subject to the gate above, candidate causal parents may include:

- actor-experienced encounter/exposure events;
- exact realized V555 route experience events;
- exact realized V556 F1 actor-history events;
- actor response/developmental transition events;
- actor rupture/metabolization events or transitions;
- actor-participatory relationship/household events;
- admitted external interactions after V3 admission;
- actor-perceivable material/organismic events where the event rule explicitly supplies experiential basis;
- other canonical V3 generated/admitted events only where their owning rule explicitly permits a memory effect.

A generated fact is not automatically an experienced memory. For example, a child-generation/birth fact does not become an episodic childhood memory merely because the event is objectively true.

### 5.3 Ineligible sources

The following can never form V3 causal memory directly:

- raw source evidence;
- V553–V558 structural objects;
- `ResolvedStructuralContext`, `SelectionRecord`, temporal proxy metadata or structural availability/applicability alone;
- opportunities that never become encounters/exposures;
- V555 routes that are available but never traversed;
- V556 F2 topology or V3 F2 satisfaction alone;
- checkpoints, derived views, readiness/integrity records or analyst annotations;
- V2 transcript/session state;
- transcript summaries;
- rendered dialogue or narrative;
- persona sheets/backstory prose;
- prose produced by memory distillation/summarization;
- keyword/phrase hook matches;
- rejected/pending external interaction proposals;
- placeholder scenes, generic biography, invented anecdotes or default childhood events.

---

## 6. Formation decision states

Every attempted formation produces a typed decision receipt. The canonical v1 states are:

- `FORMED_EVENT_REFERENTIAL_MEMORY`;
- `FORMED_CAUSAL_TRACE_MEMORY`;
- `NO_MEMORY_FORMED` — the basis was lawful but the governed rule produced no memory effect;
- `INELIGIBLE_NONCAUSAL_SOURCE` — source class cannot form memory;
- `DEFERRED_MISSING_MEMORY_BASIS` — a required causal parent, experience role, source feature or separately owned rule authority is absent;
- `BLOCKED_INTEGRITY_FAILURE` — ID/hash/prestate/provenance integrity failed.

`NO_MEMORY_FORMED` is lawful emptiness, not missing data. `DEFERRED_MISSING_MEMORY_BASIS` is not evidence that no memory could ever form. Neither state licenses a fallback memory.

---

## 7. Persistence, forgetting and degradation

### 7.1 Persistence law

Once formed, memory identity and transition provenance persist for causal replay. The current materialized memory state persists unchanged until a governed memory transition actually changes it.

**No transition means no memory-state change.**

Therefore:

- passage of wall-clock time does not itself degrade memory;
- a yearly tick does not itself degrade memory;
- failure to recall is not itself proof of forgetting;
- absence from V2 conversation is not forgetting;
- transcript deletion or compaction is not V3 forgetting;
- no default numeric memory-strength decay exists in this authority.

A future governed slow-process rule may use elapsed **causal** time as an explicit input, but only through the accepted V3 scheduler/rule authorities and a recorded transition. ADP-016 does not choose scheduler cadence.

### 7.2 Retention states

Canonical `retention_state` values:

- `RETAINED` — source-bound memory content remains retained;
- `DEGRADED` — one or more retained features have weakened to uncertainty or unavailability under a governed transition;
- `CONTENT_UNAVAILABLE` — no actor-retrievable event content remains, while memory identity/provenance and objective history remain intact;
- `RETENTION_UNKNOWN` — integrity or required authority is insufficient to assert a current retention state.

`CONTENT_UNAVAILABLE` is not deletion of the memory record and not deletion of the objective event.

### 7.3 Forgetting semantics

“Forgetting” is the human-facing umbrella for one or more explicit V3 memory transitions such as:

- `DEGRADE`;
- `MARK_FEATURE_UNCERTAIN`;
- `MARK_FEATURE_UNAVAILABLE`;
- `ACCESS_DECREASE`;
- transition to `CONTENT_UNAVAILABLE`.

Forgetting may reduce what the actor-memory subsystem retains or can currently retrieve. It may never:

- mutate/delete the objective source event;
- remove the source event/hash from audit provenance;
- erase prior memory-transition receipts;
- silently rewrite the original event;
- refill lost content from analyst-only history;
- synthesize a plausible replacement detail.

### 7.4 No analyst-history rehydration

This is binding:

> Objective history may remain perfectly known to the system while the actor memory has lost the content. The system's omniscience is not a recall source.

If a feature is `UNAVAILABLE`, later recall/reactivation cannot recover its value by dereferencing the objective event ledger alone. Recovery of content requires a **new actor-facing generated/admitted event** that lawfully re-exposes the information, followed by a new source-bound memory transition. This is relearning/re-exposure, not restoration from analyst omniscience.

---

## 8. Recall, reactivation and memory accessibility

### 8.1 Memory accessibility states

Canonical `memory_accessibility_state` values are:

- `ACCESSIBLE`;
- `PARTIALLY_ACCESSIBLE`;
- `INACCESSIBLE`;
- `ACCESS_UNKNOWN`;
- `NOT_APPLICABLE_CAUSAL_TRACE`.

These values describe the V3 memory subsystem's current retrievability only.

They do **not** mean:
- actor propositional knowledge;
- actor belief;
- first-person claim permission;
- V2 permission to say the material;
- objective event truth.

Those downstream semantics remain `ADP-017` / V2 authority.

### 8.2 Recall/reactivation transition kinds

Canonical transition kinds are:

- `FORMATION`;
- `DEGRADE`;
- `MARK_FEATURE_UNCERTAIN`;
- `MARK_FEATURE_UNAVAILABLE`;
- `ACCESS_DECREASE`;
- `ACCESS_INCREASE`;
- `RECALL`;
- `REACTIVATE`;
- `UNCERTAINTY_INCREASE`;
- `UNCERTAINTY_DECREASE`.

No “DELETE_MEMORY” semantic transition exists in v1.

An unchanged evaluation creates no pseudo-transition record beyond whatever noncausal diagnostic the implementation requires.

### 8.3 Lawful recall/reactivation cues

Recall/reactivation requires:

1. an existing exact `memory_id`;
2. a verified pre-state hash;
3. a versioned ADP-016 transition rule;
4. an exact causal cue/trigger ref admissible to V3, or a separately governed V3 slow-process invocation where the rule explicitly permits it;
5. source-feature state that permits the requested result;
6. a replayable transition receipt.

A lawful cue may be an admitted/generated actor-facing V3 event or another exact V3 causal transition that the memory rule recognizes. A V2 keyword match, transcript line, render artifact, presentation-only interaction or session summary is never itself a V3 recall cue.

For an `IN_WORLD_CAUSAL` conversation, the observable interaction must first pass the separate V3 external-event admission authority. Only the admitted V3 event may then serve as a candidate recall cue under ADP-016.

`PRESENTATION_NONCAUSAL` conversation cannot change V3 memory or accessibility.

### 8.4 Recall cannot invent

`RECALL` and `REACTIVATE` may:

- increase accessibility of still-retained source-bound features;
- reactivate a lawful `CAUSAL_TRACE_MEMORY` for later V3 causal processing where separately authorized;
- change uncertainty only where the transition has an exact causal basis.

They may not:

- create a remembered feature absent from the memory's source-bound feature set;
- upgrade `UNAVAILABLE` content by reading objective history;
- fabricate names, places, incidents, relationships or childhood scenes;
- use “deep memory” keyword matching as a causal trigger;
- turn a causal trace into declarative conscious memory without a separately generated, source-bound memory formation transition.

---

## 9. Transition record, provenance and replay

### 9.1 `MemoryTransitionRecord`

Every causal memory mutation SHALL emit the semantic equivalent of:

```text
MemoryTransitionRecord {
  memory_transition_id,
  memory_id,
  actor_id,
  transition_kind,
  effective_causal_time,
  authority_id,
  authority_version,
  authority_or_rule_hash,
  memory_rule_id,
  memory_rule_version,
  memory_rule_hash,
  objective_source_event_refs[],
  causal_parent_event_refs[],
  cue_or_trigger_refs[],
  scheduler_invocation_ref?,
  rng_receipt_ref?,
  pre_state_hash,
  post_state_hash,
  feature_state_before_hash,
  feature_state_after_hash,
  decision_state,
  integrity_state
}
```

Each event ref includes at minimum exact event ID and event hash.

`memory_transition_id` must be deterministic/content-addressable over the actor, memory identity, transition kind, exact causal parents/cues, rule identity/version, and pre/post state identity. Order-sensitive collections must have canonical ordering before hashing.

### 9.2 Provenance inheritance

A memory may cite structural/repository/resolver provenance only **through the exact causal event that consumed that context**. Structural provenance never becomes the memory's experiential basis merely because it is reachable.

This preserves:

```text
structural evidence/proxy
→ resolver context
→ generated/admitted V3 event
→ optional generated memory
```

and forbids:

```text
structural evidence/proxy
→ generated memory
```

### 9.3 Replay law

Given the same:

- immutable V3 DevelopmentalEventLedger;
- exact source event hashes;
- initial memory state;
- ADP-016 authority version/hash;
- memory-rule definitions/versions/hashes;
- causal cue/trigger sequence;
- accepted scheduler invocation inputs where relevant;
- accepted V3 causal-RNG receipts where stochastic memory logic is separately authorized;

replay must reproduce the same:

- formation decisions;
- memory IDs;
- transition IDs;
- feature-state transitions;
- retention/accessibility/uncertainty states;
- post-state hashes.

The following may never alter causal memory replay:

- hidden wall clock;
- filesystem order;
- mutable `latest` pointers;
- unrecorded network lookups;
- unnamed/unseeded randomness;
- unrecorded LLM output;
- V2 transcript cursor or retention state;
- renderer/model variation;
- prose summaries.

If required replay material is missing or mismatched, the state is blocked/unknown rather than reconstructed heuristically.

---

## 10. Rule authority and numeric semantics

ADP-016 establishes the categorical memory state machine and transition admissibility contract. It does not freeze recovered legacy numeric memory-strength or groove-decay formulas as constitutional memory semantics.

A compatible V3 causal rule may carry numeric trace state only when that rule's accepted authority supplies the formula, bounds and provenance. Recovered `pressure_flow_memory` groove/conductance mechanics are continuity evidence for this capability, not automatic authority for arbitrary autobiographical forgetting.

A memory transition that requires stochastic choice SHALL fail/defer unless the separately accepted V3 causal-randomness policy supplies a named-stream receipt. No unseeded `random.*` path is lawful.

---

## 11. Relationship to ADP-017 actor accessibility

`ADP-016` exports memory facts to the future actor-accessibility court, including:

- exact memory identity;
- representation kind;
- source-bound feature states;
- current retention state;
- current memory-accessibility state;
- uncertainty state;
- provenance/integrity;
- analyst-only causal trace designation where applicable.

It does **not** output a field equivalent to:

- `actor_knows=true`;
- `actor_believes=true`;
- `may_claim_first_person=true`;
- `V2_may_render_as_fact=true`.

Those are explicitly outside this authority. Even `ACCESSIBLE` memory is not self-executing first-person claim permission.

Conversely, an objectively true event whose memory is `INACCESSIBLE` or `CONTENT_UNAVAILABLE` remains true in analyst/objective history while actor claim access can fail closed downstream.

---

## 12. Exact consumers and release effect

RA-R00 names the direct implementation consumers of `MUST-016` as:

- `V3-P8` — memory transitions alongside rupture/metabolization causal processing;
- `V3-P12` — V3→V2 boundary publication of memory state, subject to separate ADP-017 actor-accessibility authority;
- `V2-P1` — boundary epistemics, consuming only the later actor-safe projection rather than raw objective history;
- `V2-P6` — relationship/memory split, keeping V3 causal relationship/memory truth separate from V2 session continuity.

Authority consumer:

- `ADP-017` — consumes ADP-016 memory/accessibility state and separately decides actor knowledge / claim accessibility.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT` means this result fully supplies the missing `MUST-016` semantic authority. It does **not** by itself release any packet whose other MUST/CAN/EXT dependencies remain open.

---

## 13. Fail-closed states

Implementations SHALL preserve equivalent typed failures; they may rename serialization labels but not collapse meanings.

| state | meaning | required behavior |
|---|---|---|
| `INELIGIBLE_NONCAUSAL_SOURCE` | proposed memory basis is structural/render/session/proposal/other noncausal material | reject formation; create no memory |
| `DEFERRED_MISSING_MEMORY_BASIS` | causal basis, experiencer role, source feature, or required external authority is missing | no mutation; preserve defer reason |
| `MISSING_PARENT_EVENT` | referenced causal parent cannot be found | block transition |
| `PARENT_EVENT_HASH_MISMATCH` | parent ID resolves but immutable hash differs | integrity failure; no mutation |
| `UNKNOWN_MEMORY_ID` | transition targets no valid formed memory | reject/no mutation |
| `MEMORY_ID_COLLISION` | deterministic identity exists with conflicting basis | integrity failure |
| `PRE_STATE_HASH_MISMATCH` | transition is applied to stale/divergent state | integrity failure |
| `UNAUTHORIZED_TRANSITION` | requested transition kind/result is outside rule | reject/no mutation |
| `UNAUTHORIZED_RECALL_CUE` | cue is V2/session/render/keyword or otherwise not admissible V3 causal input | reject/no mutation |
| `UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION` | lost actor content is being refilled from analyst ledger without new actor-facing event | reject/no mutation |
| `UNAUTHORIZED_V2_SESSION_PROMOTION` | transcript/session/summary is being promoted into memory | reject/no mutation |
| `UNSUPPORTED_CONFABULATION` | transition would invent substitute memory detail | reject/no mutation |
| `MISSING_RULE_VERSION` | exact memory rule identity/version/hash unavailable | block/defer |
| `MISSING_RNG_AUTHORITY` | requested stochastic transition has no accepted replayable causal RNG authority | block/defer |
| `RETENTION_UNKNOWN` / `ACCESS_UNKNOWN` | state cannot be asserted due to incomplete/integrity-gapped authority | remain unknown; no plausible default |
| `INTEGRITY_FAILURE` | other hash/provenance/replay invariant fails | block mutation and downstream causal use of the disputed state |

Unknown is not inaccessible. Inaccessible is not content-unavailable. Content-unavailable is not objective-event deletion. No-memory-formed is not proof that the source event never happened.

---

## 14. Hostile fixture court

A conforming implementation must pass at least the following fixtures.

| # | hostile fixture | required result |
|---:|---|---|
| 1 | future temporal proxy offered as childhood memory | `INELIGIBLE_NONCAUSAL_SOURCE`; no memory |
| 2 | V555 route available/applicable but never traversed | no memory |
| 3 | persona/backstory scene labeled “MEMORIES” offered as causal memory source | reject |
| 4 | `distill_memory.py` prose output offered as V3 memory | reject; provenance of prose does not make it causal |
| 5 | persisted V2 transcript or transcript summary offered as V3 memory | reject |
| 6 | keyword/phrase hook such as “father” directly triggers “deep memory” | `UNAUTHORIZED_RECALL_CUE` |
| 7 | `PRESENTATION_NONCAUSAL` turn attempts to change memory/accessibility | reject/no V3 mutation |
| 8 | in-world conversation candidate is pending/rejected but used as recall cue | reject; only admitted V3 event may become candidate cue |
| 9 | Life F: objective `eF0` remains in ledger while memory becomes inaccessible/uncertain | pass; objective history unchanged |
| 10 | inaccessible/content-unavailable memory tries to restore lost detail by reading objective ledger | `UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION` |
| 11 | new admitted actor-facing event re-exposes a lost detail | may form/update source-bound memory under rule; provenance cites new event |
| 12 | V2 relationship session fields (`user_facts`, trust, inside references) promoted to causal memory | reject |
| 13 | child birth/generated identity fact becomes default episodic childhood memory | reject unless separately actor-experienced event later forms it |
| 14 | transition supplied with stale `pre_state_hash` | integrity failure/no mutation |
| 15 | unseeded random memory decay | `MISSING_RNG_AUTHORITY` / reject |
| 16 | analyst-only pressure-flow trace is rendered as conscious persona memory | reject downstream export; trace may remain causally active |
| 17 | pressure-flow groove affects future conductance while explicit recall is N/A/inaccessible | pass; causal trace != declarative memory |
| 18 | same formation effect is replayed twice | idempotent same memory ID; conflicting duplicate is integrity failure |
| 19 | memory content becomes unavailable | memory/source-event provenance remains auditable and objective event remains immutable |
| 20 | structural prior is selected, actor later has a real admitted exposure, then memory forms | only the generated exposure event may be memory parent; structural prior remains provenance-through-event only |
| 21 | rendered dialogue says “I remember X” but no V3 memory basis exists | render is not memory evidence; no causal state change |
| 22 | checkpoint/derived view contains event fact and is offered as memory basis | reject; objective/derived storage is not memory formation |

---

## 15. Compatibility / migration law

### 15.1 Preserve/adapt

Recovered V3 mechanisms worth preserving within the terminal authority include:

- typed persistent actor state and event/micro-trace provenance;
- YearRecord hashing/replay discipline;
- transactional pressure-flow history/memory commit;
- persistent grooves/conductance as `CAUSAL_TRACE_MEMORY` continuity;
- explicit analyst-versus-surface separation;
- persistent rupture/metabolization state where exact causal parents are repaired/bound.

### 15.2 Demote/remove as causal authority

The following recovered behaviors are not V3 causal-memory authority:

- persona-sheet prose scene arrays labeled “MEMORIES”;
- LLM memory distillation of backstory;
- V2 anchored-memory prompt injection;
- keyword/phrase hook retrieval as a causal recall rule;
- V2 `Memory & Relationship State` as causal relationship/memory truth;
- server conversation/session persistence;
- manual/unseeded rupture or memory-like injection;
- generic fallback biography or childhood memory insertion.

Migration may retain these only in their lawful V2 presentation/session or audit roles. It may not preserve their old authority shortcut.

---

## 16. Implementation acceptance requirements derived from this authority

This authority does not implement code. A later implementation consuming it must prove at minimum:

1. exact objective-event ID/hash survives all memory transitions;
2. no memory is auto-created from objective history or structural context;
3. memory identity is deterministic, stable and replayable;
4. forgetting changes memory state without changing objective history;
5. `UNAVAILABLE` content cannot be rehydrated from analyst history;
6. recall requires a lawful V3 causal cue/trigger and cannot be keyword-only V2 behavior;
7. V2 session/transcript persistence cannot mutate V3 memory;
8. pressure-flow causal traces can persist and affect causation without becoming persona consciousness;
9. current memory accessibility is emitted distinctly from actor claim permission;
10. stochastic transition attempts fail without accepted causal-RNG receipt;
11. stale hashes and missing provenance fail closed;
12. replay reproduces exact memory/transition IDs and state hashes.

No architecture change is required to implement these requirements.

---

## 17. Consumer-release sufficiency and final token

**CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT**

Rationale: this authority supplies the complete generic `MUST-016` semantic contract for memory source eligibility, stable memory identity, memory representation, persistence/forgetting, recall/reactivation, current memory accessibility, uncertainty/degradation, objective-history separation, provenance/replay, V2/session exclusion and fail-closed behavior. It intentionally leaves actor knowledge/claim permission to `ADP-017`, session retention to `ADP-024`, RNG mechanics to `ADP-020`, and scheduler cadence to `ADP-021`; those are separately classified authorities rather than holes in `MUST-016`.

**ADP_016_V3_CAUSAL_MEMORY_AUTHORITY = PASS**
