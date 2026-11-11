# CAN-015 — V2 Phenomenological Projection Canonicalization

**Canonicalization ID:** `CAN-015`  
**Canonical authority:** `V2_PHENOMENOLOGICAL_PROJECTION_RULE`  
**Version:** `1.0.0`  
**Owner:** V2 actor-limited phenomenology / expression membrane  
**Mode:** recovered-mechanism canonicalization only  
**Whole-machine architecture:** `CLOSED`  
**W0 authority foundation:** `CLOSED`  
**Production implementation:** `NOT AUTHORIZED`  
**Verdict:** `PASS`

## 1. Constitutional verdict

`CAN-015` canonicalizes one bounded V2 operation: creation of an immutable, noncausal, actor-access-limited render projection from already-authorized source material.

The binding law is:

```text
V3 GENERATES THE LIFE.
V2 EXPRESSES THE GENERATED LIFE.

OBJECTIVE_GENERATED_TRUTH
!= ACTOR_ACCESSIBLE_RENDER_ENVELOPE
!= V2_PHENOMENOLOGICAL_PROJECTION
!= V2_SALIENCE
!= V2_EXPRESSION_REGISTER
!= V2_RESPONSE_MOVE
!= RENDERED_EXPRESSION
!= CAUSAL_OCCURRENCE
```

A V2 projection is not a second actor state and not a synthetic interior snapshot. It is a pure, provenance-bound view over material that V3 has already authorized for the actor-facing surface plus separately authorized caller/application current-situation context. Projection may organize, type, group, omit, and carry forward uncertainty/opacity. It may not create a proposition, memory, feeling, motive, biography, relationship fact, attractor state, or first-person permission that did not already exist upstream.

The canonical v1 rule deliberately prefers sparse lawful projection to a vivid but fabricated “present person.” `VALID_EMPTY` is a successful result.

## 2. Required source verification

### 2.1 Historical archive

Required logical archive: `Rawlsing_code_bundle_staging.zip`  
Expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
Directly computed SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`  
ZIP entries: `13,138`  
Verdict: `EXACT_MATCH`.

Recovered V2/V3/server source is continuity and authority-recovery evidence only. Historical archive V5/DDM has **zero authority** over current V550+.

Focused recovered source court:

```text
v3/tests/test_v5_v2_chat_prompt_no_raw_v5_leaks.py
v3/tests/test_v5_voice_packet_surface_allowlist.py
v3/tests/test_v5_render_surface_psyche.py
v3/tests/test_v5_persona_sheet_surface_psyche.py
v3/tests/test_persona_sheet_integrity.py
→ 8 passed
```

These passing tests establish useful continuity for surface allowlisting and analyst/raw-state quarantine. They do not authorize historical defaults, current-life synthesis, actor omniscience, or persona prose as causal/epistemic truth.

### 2.2 Binding current authority inspected

At exact base `db961be677d5112073e16e5d452853971861cdb6`, this canonicalization consumed the Batch-03 common law and CAN-015 cell together with the binding authority set required there, including:

- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/V3_COMPLETION_IMPLEMENTATION_RULING.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/W0_AUTHORITY_FOUNDATION_CLOSURE_RULING.md`;
- `integration/W1_FIRST_BATCH_INTERIM_ADJUDICATION_RULING.md`;
- `integration/W1_BATCH_02_ADJUDICATION_RULING.md`;
- RA-R00 `RESULT.md` / `RESULT.json`;
- accepted TD-R06 V2 result;
- accepted `ADP-016 / V3_CAUSAL_MEMORY_FORMATION_FORGETTING_RECALL_RULE@1.0.0`;
- accepted `ADP-017 / V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0`;
- accepted `ADP-026 / CALLER_CURRENT_SITUATION_AUTHORITY@1.0.0`;
- the Batch-03 launch register.

Current repository terrain has no top-level production `v2/conversation_engine.py` at this base. The recovered archive therefore supplies authorized historical implementation evidence; current architecture/rule authority remains sovereign.

### 2.3 Direct recovered source inspected

Required sources directly inspected:

- `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md`;
- `v2/conversation_engine.py`;
- `v2/LIFE_SIMULATION_LAYER.md`;
- `v2/life_simulation_schema.py`;
- `v2/life_snapshot_from_data.py`;
- `v2/run_conversation_chat.py`;
- `v3/V3_UNDERLIES_V2_ARTICULATION.md`;
- `v3/io/persona_sheet.py`;
- the five prompt/surface/integrity tests listed above.

Direct consumers/config/seam evidence additionally inspected:

- `v2/spec.py`, especially `build_conversation_persona_context`, life-snapshot coercion/defaulting and present-year snapshot wiring;
- `v2/config/life_snapshot.yaml`;
- `v2/PIPELINE_WIRING_AUDIT.md`;
- recovered `LifeSimulationState` build/consumer path in `conversation_engine.py` and `run_conversation_chat.py`.

## 3. Recovered-mechanism disposition court

| recovered mechanism | direct finding | disposition | canonical terminal meaning |
|---|---|---|---|
| renderer-not-decider direction | explicit in recovered V2/V3 articulation | `PRESERVE` | V2 projection is noncausal and downstream of V3 truth |
| persona/surface allowlisting | tests strip analyst/raw pressure fields | `PRESERVE_ADAPT` | allowlist source classes/fields; hidden analyst content cannot enter projection |
| Life Container | useful logistical/current-life grouping, but schema defaults job/commute/living/family/income/internet/social/sleep values | `ADAPT` | optional sparse `PROJECTED_LIFE_CONTEXT_VIEW`; only exact authorized source atoms, no required fields/defaults |
| `derive_life_container_from_simulation` | derives from stored snapshot but fills absent fields with defaults | `ADAPT` | pure projection from exact actor-safe source refs; missing fields stay absent/unknown |
| Life Season | useful bounded temporal-context grain, but defaults to `stable_routine_phase` + `0.5` intensity | `ADAPT` | optional `PROJECTED_TEMPORAL_CONTEXT_VIEW`; legacy taxonomy compatibility-only unless exact source semantics supply a matching claim; no intensity default |
| `derive_life_season_from_simulation` | reads current phase then fills absent phase/intensity | `ADAPT` | direct source-preserving projection only; no inferred phase or scalar |
| Today State | randomly creates sleep, mood, stressor, loops, obligation, body, battery, location, interruption risk | `REPLACE` | `CURRENT_SITUATION_VIEW` from actor-safe V3 claims and/or ADP-026 source-bound current-situation statements only |
| Interaction Context | useful interaction-premise grain but randomly chooses a reason when absent | `ADAPT` | `INTERACTION_SITUATION_VIEW` from ADP-026/session/caller records; absence remains unknown/empty; no motive inference |
| `LifeSimulationState` aggregate | bundles life container/season/today/context/attention as mutable-looking conversational state | `REPLACE_ADAPT` | immutable `V2PhenomenologicalProjection`; attention/effort/energy removed to MUST-023/CAN-021 jurisdiction |
| `life_snapshot_from_data.py` | derives present-life facts from GDP, inequality, class, urbanicity, needs, strategies, indices, age bands and configured priors/defaults | `REMOVE_REJECT_AS_PROJECTION_AUTHORITY` | structural/causal data cannot become actor-present life facts in V2; such facts must already be generated/admitted and actor-safe upstream |
| `v2/config/life_snapshot.yaml` formulas/priors | job/commute/living/family distributions and numeric formula bands | `COMPATIBILITY_ONLY` | no terminal CAN-015 semantic authority |
| present-year LLM `life_snapshot` confirm/pick path | model chooses from “data-derived defaults” and allowed values | `REMOVE_REJECT_AS_PROJECTION_AUTHORITY` | LLM output cannot create generated present-life truth |
| persona-sheet/current-state projection carrier | useful schema carrier and provenance direction, but historical fields include defaults and objective/system-known content | `ADAPT` | consume only hardened actor-access envelope; never full persona sheet / GeneratedPersonRecord as first-person source |
| full backstory as “anchored memories” | prompt tells renderer to pull freely from backstory, even unprompted | `REMOVE_REJECT` | only ADP-016 memory material already permitted by ADP-017 may enter actor-facing projection |
| objective country-history fetch | historical context is fetched and told to ground opinions, memories and reactions | `REMOVE_REJECT` | analyst/system history cannot become first-person content without exact actor access |
| direct identity/class/religion/history-to-voice context | recovered prompt injects objective identity/context and tells model to speak from it | `REMOVE_REJECT_AS_AUTHORITY_SHORTCUT` | only exact actor-safe claim/view entries may support first-person content; expression choice belongs later authorities |
| invented named anecdote rule | explicitly permits plausible names/times/incidents not in generated life | `REMOVE_REJECT` | projection never invents an event/detail; later renderer also lacks causal truth authority |
| default life snapshot in `run_conversation_chat.py` / minimal persona | fills `retail`, `stable_routine_phase`, etc. to keep engine running | `REMOVE_REJECT_AS_AUTHORITY` | missing actor truth remains missing; test fixtures must be explicitly synthetic/nonactual |
| AttentionBudget `50` defaults / heuristic formulas | generic 0–100 attention, effort, social-energy state | `OUT_OF_SCOPE_COMPATIBILITY_ONLY` | MUST-023 owns boundary/face-risk/effort/attention; CAN-021 owns session field |
| surface-psyche `felt_register` allowlist | demonstrates sanitized render surface but historical field ontology is not terminal CAN-015 authority | `COMPATIBILITY_ONLY_WITH_ALLOWLIST_PATTERN_PRESERVED` | future actor-safe surface fields require their own upstream semantic authority and envelope permission |

## 4. Exact jurisdiction

### 4.1 CAN-015 owns

CAN-015 owns only:

1. deterministic validation of exact projection inputs;
2. creation of a pure, immutable `V2PhenomenologicalProjection` from those inputs;
3. typed, source-preserving grouping of actor-permitted semantic atoms and presentation-only current-situation atoms;
4. exact omission/opacity markers for inaccessible, forbidden, unknown, conflicting or absent source material without carrying hidden values;
5. actor-access ceiling enforcement at the projection boundary;
6. projection identity, provenance, cache validity and replay law;
7. valid-empty projection semantics.

### 4.2 CAN-015 does not own

CAN-015 does not own or decide:

- V3 generated facts, actor state, memory, belief, knowledge, relationship or attractor state;
- ADP-017 claim identity, stance, accessibility or first-person permission;
- ADP-016 memory formation/retention/recall/accessibility;
- ADP-026 source authority for caller/application current situation;
- turn-local salience (`CAN-016`);
- expression register (`CAN-017`);
- response move (`CAN-018`);
- uncertainty disclosure language/behavior (`MUST-022`);
- boundary, face risk, effort or attention (`MUST-023`);
- relationship expression (`CAN-019`);
- attractor expression (`CAN-020`);
- session EnergeticField/topic persistence (`CAN-021`);
- transcript retention (`ADP-024`);
- renderer/model/randomness (`ADP-025`);
- prompt/render admission contract (`CAN-022`);
- interaction mode or V2→V3 packaging;
- structural/world interpretation or direct V558 access;
- external history lookup;
- narrative detail generation.

## 5. Admissible input contract

A projection request has exactly two semantic input lanes plus immutable request metadata.

### 5.1 Lane A — actor-safe V3 source

Required semantic source:

```text
ActorAccessibleRenderEnvelope
```

The exact accepted ADP-017 envelope/hash is the **ceiling** for actor-facing semantic content. CAN-015 may consume:

- `allowed_claim_entries[]`;
- exact supplied permission class;
- exact supplied stance record refs;
- exact supplied accessibility state/component refs;
- memory refs only as already authorized through the envelope;
- actor-perceived view refs only as already authorized through the envelope;
- source transition refs and opaque provenance refs for audit;
- explicit denial/omission refs without hidden semantic values.

CAN-015 may **not** query or dereference the full `GeneratedPersonRecord`, objective event ledger, raw ADP-016 memory store, analyst misrecognition relation, V558, structural provenance or any opaque provenance target to acquire more content.

### 5.2 Lane B — current interaction situation

Optional source:

```text
CALLER_CURRENT_SITUATION_AUTHORITY statement[]
```

Only ADP-026-valid records may be consumed. Their exact source class, subject binding, effective time, certainty, disposition, conflict set and transform chain remain attached.

Current-situation statements do **not** gain actor-truth authority inside CAN-015. In particular:

- a caller assertion about the generated actor remains a caller assertion;
- an application/session property remains an application/session property;
- `interaction_reason` remains caller/session purpose metadata, not generated-actor motive;
- `PRESENTATION_ONLY` never becomes causal truth;
- a `PROPOSED_CAUSAL_INPUT` remains noncausal pending separate packaging/admission;
- stale/expired/conflicted statements may not be silently carried forward or resolved.

A current-situation atom may constrain later presentation only under separately governed downstream rules. It grants **no first-person claim permission** unless an independently matching ADP-017 claim entry already grants that permission.

### 5.3 Forbidden inputs

The following are categorically forbidden projection content sources:

- raw/generated objective facts outside the ADP-017 envelope;
- full `GeneratedPersonRecord` or full V3 derived state;
- raw structural priors / V553–V558 objects / resolver context;
- analyst causal explanation or misrecognition labels;
- causal-trace memory content not actor-permitted;
- persona sheets/backstory as independent authority;
- transcript/session summaries as biography;
- prior rendered language as proof of actor state;
- LLM inference;
- historical-context network/file lookup;
- demographic/class/religion/geography heuristics;
- random/default Today State or life facts;
- same-batch sibling CAN-016/017/018/021 outputs.

## 6. Canonical output contract

A conforming implementation SHALL produce the semantic equivalent of:

```text
V2PhenomenologicalProjection {
  projection_id,
  projection_schema_version,
  actor_id,
  projection_effective_scope,

  source_actor_envelope_id,
  source_actor_envelope_hash,
  source_actor_state_hash,
  source_epistemic_state_hash,
  source_current_situation_set_hash?,

  actor_surface_atoms[],
  current_situation_atoms[],
  projection_groups[],
  contradiction_refs[],
  opacity_markers[],
  opaque_provenance_refs[],

  projection_state,
  authority_id = CAN-015,
  authority_name = V2_PHENOMENOLOGICAL_PROJECTION_RULE,
  authority_version = 1.0.0,
  authority_hash,
  projection_hash,
  integrity_state
}
```

### 6.1 `ActorSurfaceAtom`

```text
ActorSurfaceAtom {
  source_claim_ref,
  stance_record_ref,
  source_accessibility_state,
  permitted_component_refs[],
  first_person_permission,
  memory_refs[],
  actor_perceived_view_refs[],
  source_transition_refs[],
  temporal_scope,
  subject_scope,
  projection_group_refs[],
  atom_hash
}
```

CAN-015 copies or narrows the exact upstream semantic permission. It does not create a new claim or rephrase a claim into a stronger proposition.

### 6.2 `CurrentSituationAtom`

```text
CurrentSituationAtom {
  statement_id,
  field_key,
  value_or_opaque_value_ref,
  subject_binding,
  source_class,
  semantic_effective_time,
  knowledge_state,
  certainty_state,
  disposition,
  conflict_set_id?,
  transform_chain[],
  actor_claim_permission = NONE_UNLESS_SEPARATELY_PRESENT_IN_ADP017,
  atom_hash
}
```

The atom remains current-situation context, not actor biography.

### 6.3 Projection groups

Canonical v1 permits only **non-semantic organization labels**. They group existing atoms; they do not assert new claims.

Allowed group kinds:

- `PROJECTED_LIFE_CONTEXT_VIEW` — optional logistical/material/current-life atoms already authorized upstream;
- `PROJECTED_TEMPORAL_CONTEXT_VIEW` — optional current phase/time-scope atoms already authorized upstream;
- `CURRENT_SITUATION_VIEW` — exact current-situation records;
- `INTERACTION_SITUATION_VIEW` — exact interaction/channel/mode/purpose context records;
- `ACTOR_PERMITTED_CLAIM_VIEW` — actor-safe claim atoms;
- `ACTOR_PERMITTED_MEMORY_VIEW` — only memory refs/components already claim/access permitted.

A group may be empty. Group existence does not imply that any canonical field inside it exists.

There is no canonical v1 `felt_state`, `mood_state`, `readiness`, `intensity`, `attention`, `social_energy`, `life_phase_intensity`, `trust`, `relationship_temperature` or equivalent scalar.

## 7. Actor-access ceiling law

For every actor-facing semantic atom `c`:

```text
projection_permission(c) <= ADP017_permission(c)
```

where the only lawful projection operations are:

```text
COPY_EXACT_PERMISSION
OMIT
COPY_ONLY_EXACT_PERMITTED_COMPONENTS
```

There is no permission-raising operation.

Binding consequences:

1. `BELIEF` permission never becomes `KNOWLEDGE` permission.
2. `UNCERTAINTY` never becomes belief/knowledge certainty.
3. `NONKNOWLEDGE` never licenses guessing or filling an answer.
4. `CLAIM_PARTIALLY_ACCESSIBLE` exposes only exact permitted components.
5. `CLAIM_INACCESSIBLE` carries no semantic value into actor-facing projection.
6. `CLAIM_ACCESS_UNKNOWN` remains nonassertable.
7. no join/inference over two permitted claims may create a third unlisted claim;
8. opaque provenance may be retained for audit but never dereferenced for persona content;
9. current-situation context may affect later presentation only as separately typed context; it cannot create actor first-person permission;
10. CAN-015 may omit lawful material, but omission does not mutate upstream access or memory.

## 8. Life Container / Life Season / Today State / Interaction Context law

### 8.1 Life Container

**Disposition:** `ADAPT_TO_SPARSE_PROJECTED_LIFE_CONTEXT_VIEW`.

The recovered idea that render-time conversation benefits from current logistical/material context is preserved. The recovered fixed eight-field container and all field defaults are not canonical.

A projected life context:

- contains `0..n` exact authorized atoms;
- may include work, location, living arrangement, obligations, material condition, device/access or social-context claims only if exact source authority already supplies them;
- has no mandatory job, commute, family, income, internet, social or sleep field;
- cannot infer any field from class, age, country, urbanicity, needs, strategies, indices or typicality;
- is a view, not persistent V2 actor state.

### 8.2 Life Season

**Disposition:** `ADAPT_TO_SPARSE_PROJECTED_TEMPORAL_CONTEXT_VIEW`.

A bounded current temporal/phase grouping is useful when an exact upstream claim/state already names such a phase or condition. The legacy taxonomy is compatibility vocabulary only and is not a universal ontology.

The following are rejected:

- default `stable_routine_phase`;
- default/required `intensity = 0.5`;
- phase inference from narrative plausibility;
- phase inference from age or structural condition;
- a mandatory nonempty season.

### 8.3 Today State

**Disposition:** `REPLACE_WITH_CURRENT_SITUATION_VIEW`.

The recovered `instantiate_today()` path is terminally unlawful because it randomly generates facts. CAN-015 authorizes **no Today State generator**.

Current-day/current-turn facts may appear only from:

- exact actor-safe V3 claim/view permission; or
- exact ADP-026 current-situation records with preserved source and subject authority.

No missing current fact is replaced by neutral mood, six hours of sleep, `none` stressor, three open loops, sixty-minute obligation, `fine` body, fifty-percent battery, home location or medium interruption risk.

### 8.4 Interaction Context

**Disposition:** `ADAPT_TO_INTERACTION_SITUATION_VIEW`.

Exact caller/session/application interaction premise is useful presentation context. It must be source-bound under ADP-026. The recovered random choice among microtask/language exchange/boredom/activism/friend intro/English practice/procrastination/loneliness/other is nonauthoritative and removed.

Interaction context is not motive authority. A caller-declared interaction reason does not become “why the generated actor chose to talk” unless V3 separately generated and actor-accessibly permits that fact.

## 9. Valid-empty / unknown / inaccessible / forbidden law

CAN-015 SHALL preserve at least these semantic states:

| state | meaning | behavior |
|---|---|---|
| `PROJECTION_NONEMPTY` | at least one lawful actor/context atom exists | emit exact atoms with provenance |
| `VALID_EMPTY_PROJECTION` | exact valid inputs yield zero lawfully projectable atoms | succeed with empty arrays; no filler |
| `PROJECTION_PARTIAL` | some atoms project while others are unknown/inaccessible/forbidden/conflicted | emit lawful subset + opacity markers |
| `SOURCE_FIELD_UNKNOWN` | source authority cannot establish a value | preserve unknown; do not default |
| `SOURCE_CONTRADICTED` | valid source records conflict without lawful resolution | preserve conflict refs; do not choose/average |
| `SOURCE_INACCESSIBLE` | V3 knows material but actor access denies it | omit semantic value; preserve opaque denial ref only |
| `SOURCE_FORBIDDEN_ANALYST_ONLY` | source is analyst/system-only or structurally privileged | reject from projection content |
| `SOURCE_PARTIALLY_ACCESSIBLE` | only exact components are permitted | project only those components |
| `CURRENT_SITUATION_STALE_OR_EXPIRED` | ADP-026 statement no longer current | omit/mark unknown; no inferred persistence |
| `CURRENT_SITUATION_NONACTOR_CONTEXT` | valid caller/session/application context | may remain typed context; no actor-claim permission |
| `MISSING_ACTOR_ACCESS_ENVELOPE` | required ADP-017 boundary input absent | block actor-facing projection; do not fall back to GPR/persona sheet |
| `STALE_ACTOR_ACCESS_ENVELOPE` | source state/hash no longer matches requested current render context | block/rebuild from V3 boundary |
| `MISSING_REQUIRED_SOURCE_AUTHORITY` | a requested semantic use depends on absent authority | defer/omit; no heuristic substitute |
| `INTEGRITY_FAILURE` | hash/ID/version/provenance mismatch | fail closed |

Important nonidentities:

```text
VALID_EMPTY != UNKNOWN
UNKNOWN != NONKNOWLEDGE
INACCESSIBLE != FALSE
FORBIDDEN != ABSENT_FROM_OBJECTIVE_HISTORY
CONFLICTED != RANDOMLY_RESOLVABLE
CURRENT_SITUATION != GENERATED_BIOGRAPHY
```

## 10. Projection transforms

Canonical v1 allows only deterministic transforms that cannot add semantic content:

- `IDENTITY_COPY` — carry exact authorized semantic atom;
- `FIELD_RENAME_WITH_SCHEMA_MAP` — stable representational rename with exact source ref;
- `TYPE_PRESERVING_GROUP` — place an existing atom under a projection group;
- `ORDER_CANONICALIZATION` — deterministic ordering by stable IDs;
- `OMIT` — narrow the view;
- `OPAQUE_DENIAL_MARKER` — retain denial/unknown/inaccessible reason without hidden value.

Forbidden transforms include:

- summarizing multiple claims into a new proposition;
- sentiment/mood inference;
- “life phase” classification absent an upstream claim;
- scalar intensity/readiness synthesis;
- biography completion;
- demographic or structural inference;
- free-text LLM rewrite that changes semantic content;
- historical lookup;
- memory retrieval outside ADP-017 permissions;
- cross-atom inference/join that produces an unlisted claim.

If a future semantic transform creates a new proposition, that transform requires separate authority and the new proposition must acquire its own upstream actor-access permission before first-person use.

## 11. Replay, provenance and cache law

Projection is pure and nonrandom.

Canonical identity is deterministic over exact source identities:

```text
projection_id = SHA256(
  "V2_PHENOMENOLOGICAL_PROJECTION"
  || projection_schema_version
  || actor_id
  || source_actor_envelope_id
  || source_actor_envelope_hash
  || source_current_situation_set_hash_or_EMPTY
  || projection_authority_version
  || projection_authority_hash
)
```

`projection_hash` is the hash of canonical serialized output after deterministic ordering.

Replay of identical source inputs under identical CAN-015 version/hash must reproduce byte-equivalent canonical semantic output and the same `projection_id`/`projection_hash`.

The following may never influence projection truth:

- hidden wall clock;
- mutable `latest`;
- filesystem order;
- network/history lookup;
- global or render RNG;
- LLM/model output;
- transcript frequency;
- prompt wording;
- same-batch sibling authority output;
- nonrecorded application state.

Cache key SHALL include all source hashes and authority version/hash. A cache entry is invalid when:

- the ADP-017 source envelope/state hash changes;
- a consumed ADP-026 statement set changes, expires or is corrected;
- the CAN-015 authority version/hash changes;
- integrity verification fails.

A cached projection cannot preserve stale first-person access or stale current-situation truth. Cache hit is a performance result only; it has no semantic authority.

## 12. Objective-history-to-first-person shortcut prohibition

The recovered archive contains several explicit shortcuts that are now terminally forbidden:

1. full backstory is labeled “anchored memories” and the renderer is told to pull from it freely even when not asked;
2. country historical context is fetched externally and supplied to ground actor opinions, memories and reactions;
3. persona context injects objective city/class/religion/history and encourages use as lived first-person context;
4. the specificity rule permits invention of plausible names, dates, places and anecdotes and explicitly says this is “not fabrication”;
5. life-snapshot formulas turn structural/world/class/needs/indices into present-life facts;
6. random Today State and random interaction reason create apparent current actor facts.

Under CAN-015 all six are rejected as semantic authority. If equivalent content is lawfully present in the ADP-017 actor-safe envelope or ADP-026 current-situation lane, only that exact authorized content may be projected. Otherwise it remains absent, unknown, inaccessible or analyst-only.

## 13. Hostile fixture court

A conforming implementation must pass at least these fixtures:

| # | hostile fixture | required result |
|---:|---|---|
| 1 | full GeneratedPersonRecord is available but ADP-017 envelope exposes one claim | projection contains only that permitted claim |
| 2 | objective event exists but actor has no first-person permission | event content omitted; opaque denial may remain |
| 3 | accessible `BELIEF(P)` is projected | belief permission preserved; never upgraded to knowledge |
| 4 | accessible `UNCERTAINTY(P)` is projected | uncertainty state preserved; CAN-015 does not decide disclosure wording |
| 5 | generated `NONKNOWLEDGE(P)` is accessible | nonknowledge permission preserved; no guessed answer |
| 6 | system has no actor stance authority | no “I don't know” invented from system absence |
| 7 | claim partially accessible | only exact permitted components project |
| 8 | two contradictory actor-permitted beliefs coexist | both survive; no reconciliation or winner |
| 9 | inaccessible memory feature exists in objective V3 history | no rehydration from event ledger |
| 10 | ADP-016 causal trace affects development but is nondeclarative | trace content absent from projection |
| 11 | raw V558/ResolvedStructuralContext offered | reject as projection content |
| 12 | analyst misrecognition label offered | reject unless separately actor-permitted claim exists |
| 13 | persona sheet contains full backstory | cannot be consumed as independent memory/claim authority |
| 14 | historical-country fetch returns exact facts | cannot enter first-person projection without actor-safe source |
| 15 | renderer wants a named anecdote for specificity | no projection atom may be invented |
| 16 | no life-snapshot data exists | `PROJECTED_LIFE_CONTEXT_VIEW` is empty; no job/commute/living defaults |
| 17 | Life Season absent | no `stable_routine_phase`; no `0.5` intensity |
| 18 | Today State absent | no neutral mood/sleep/stressor/body/location/battery default |
| 19 | interaction reason absent | no random reason; interaction view empty/unknown |
| 20 | caller says generated actor is at work | preserve caller assertion/context provenance; do not create actor first-person fact |
| 21 | application directly observes caller's device | may project application/caller context; never actor device biography |
| 22 | ADP-026 current-location statement is expired | omit/unknown; do not carry it forward |
| 23 | two current-situation statements conflict | preserve conflict; no recency/majority/default resolution |
| 24 | scenario context is explicitly nonactual | may remain presentation-only scenario context; never actor/generated truth |
| 25 | `PROPOSED_CAUSAL_INPUT` is present but not admitted | remains noncausal context/candidate; not generated history |
| 26 | same projection inputs replay | identical projection ID/hash/output |
| 27 | envelope hash changes after cache creation | stale cache rejected/recomputed |
| 28 | current-situation statement set changes | projection identity changes |
| 29 | projection implementation attempts RNG for missing mood | forbidden; no draw and no mood |
| 30 | projection implementation calls LLM to “summarize the person right now” | forbidden semantic transform |
| 31 | two permitted claims can logically imply a third claim | third claim omitted unless separately present/permitted upstream |
| 32 | actor-safe relationship view ref is present | ref may project exactly; CAN-015 does not create relationship expression |
| 33 | attractor trajectory ref is system-known but not actor-permitted | omitted; CAN-015 does not create attractor expression |
| 34 | actor-permitted material exists but later salience authority selects none | CAN-015 remains noncausal source projection; it does not force salience |
| 35 | V2 session transcript repeats a claim many times | repetition does not add projection permission or biography authority |
| 36 | opaque structural provenance accompanies an allowed claim | locator may be retained for audit; semantic provenance cannot be dereferenced |
| 37 | hidden field is stripped by recovered surface allowlist | preserve the quarantine pattern; absence from surface does not change objective truth |
| 38 | no actor-safe claims and no valid current-situation atoms | `VALID_EMPTY_PROJECTION`, not fabricated filler |

## 14. Compatibility / migration law

### Preserve/adapt

- renderer-not-decider discipline;
- explicit V3-under-V2 direction;
- prompt/surface allowlisting and analyst-field stripping;
- pure derived snapshot assembly as an architectural pattern;
- current-life/context grouping as optional render views;
- stable source/provenance/integrity metadata;
- deterministic cacheable projection.

### Demote/remove

- independent V2 life simulation as truth authority;
- fixed/default-filled Life Container schema;
- default Life Season and numeric intensity;
- random Today State;
- random Interaction Context;
- attention/readiness/intensity numerics inside CAN-015;
- structural/class/identity/world-data → present-life fact formulas;
- LLM confirmation/creation of present-life facts;
- objective-history fetch as persona knowledge;
- full backstory as automatic memory access;
- invented named anecdote permission;
- persona sheet / prior render / transcript as independent actor-truth source.

Migration may preserve legacy field names as serialization/UI compatibility aliases only when every value is populated from exact canonical projection atoms and unknown/empty states remain representable. A compatibility adapter may never recreate historical defaults.

## 15. Downstream consumers and independent blockers

RA-R00 names CAN-015 consumers:

- `V2-P2` — phenomenology projection / forbidden-claim gate;
- `V2-P3` — life-layer migration to V3-derived + caller current situation / unknown.

This result is **sufficient for CAN-015 itself**.

It does not release V2-P2 because independent blockers remain:

- `CAN-016 / V2_SALIENCE_ACCESSIBILITY_RULE`;
- `MUST-022 / V2_UNCERTAINTY_DISCLOSURE_RULE`.

`ADP-017` is already accepted and supplies the actor-access ceiling consumed here.

For V2-P3, `ADP-026 / CALLER_CURRENT_SITUATION_AUTHORITY` is already accepted and CAN-015 now supplies the projection-side migration contract. Production packet execution still remains subject to the global RA-R00 schedule, implementation migration (`IMP-009`), and all applicable stage/release gates; CAN-015 does not itself authorize implementation.

No same-batch CAN-016/017/018/021 result was consumed as authority.

## 16. GOVERNING_SPIRIT_CHECK

**GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS**

**Genuine ambiguity:** the closed V2 architecture requires a phenomenological projection layer, while recovered V2 offers two broad implementation directions that are both superficially compatible with “projection”: (a) synthesize a rich current-life/interior snapshot from generated causal/structural data using defaults, formulas and stochastic present-state completion; or (b) build a sparse actor-access-limited view that reorganizes only already-authorized actor-facing semantic content and separately typed present interaction context.

**Lawful alternatives considered:**

1. a rich inferred “present person” snapshot, noncausal in storage but semantically generated inside V2; or
2. a pure permission-monotone projection with lawful emptiness, opaque exclusions and no invented internal state.

**Chosen design:** alternative 2.

**Decisive Governing-Spirit principles:** determination is not transparency; actor opacity; uncertainty and lawful absence without fabrication; dynamic generated history over static classification; minimum sufficient machinery; and “never let downstream vividness exceed upstream authority.”

The Governing Spirit supplies no mood, motive, memory, phase, intensity, biography, salience, register or response content. It breaks only the lawful design tie over how conservative the projection operator must be.

## 17. Consumer-release sufficiency and final token

**CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT**

Rationale: the generic CAN-015 contract is complete for projection input classes, actor-access ceiling, current-situation separation, output schema, sparse life-context/temporal/current/interaction views, unknown/empty/inaccessible/forbidden behavior, deterministic transforms, cache/replay, provenance, compatibility migration and hostile fixtures. All intentionally excluded semantics remain owned by separately scheduled authorities.

**CAN_015_V2_PHENOMENOLOGICAL_PROJECTION_CANONICALIZATION = PASS**
