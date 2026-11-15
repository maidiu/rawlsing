# CAN-016 — V2 Salience Accessibility Canonicalization

**Assignment:** W1-B03-02 — CAN-016 / V2 salience accessibility  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w1-can-016-v2-salience`  
**Exact launch base:** `db961be677d5112073e16e5d452853971861cdb6`  
**Canonicalization ID:** `CAN-016`  
**Canonical authority:** `V2_SALIENCE_ACCESSIBILITY_RULE`  
**Authority version:** `1.0.0`  
**Owner:** `V2_ACTOR_LIMITED_EXPRESSION_PLANNER`  
**Authority class:** `AUTHORITY_NEEDS_CANONICALIZATION`  
**Mode:** canonicalization only; no production code; no V2 implementation; no architecture reopening  
**Verdict:** `PASS`  
**CONSUMER_RELEASE_SUFFICIENCY:** `SUFFICIENT_FOR_CAN_016_JURISDICTION__NOT_STANDALONE_V2_P2_OR_V2_P5_RELEASE`

## 0. Binding holding

V2 salience is a **turn-local, noncausal subset selection over material already lawfully available to V2**. It is neither a knowledge system nor a memory system nor persistent actor state.

```text
V3 ACTOR ACCESSIBILITY / FIRST-PERSON PERMISSION
                    |
                    | hard ceiling; V2 may only narrow
                    v
         V2 SALIENCE CANDIDATE SET
                    |
                    | governed turn-local subset selection
                    v
          V2 TURN SALIENT SET
```

For every successful selection:

```text
selected_candidate_refs ⊆ candidate_refs ⊆ exact actor-safe input refs
```

The following noncollapse law is binding:

```text
ACCESSIBLE != SALIENT
SALIENT != MEMORY
SALIENT != MEMORY ACCESSIBILITY
SALIENT != PERSISTENT CONCERN
SALIENT != ACTOR BELIEF
SALIENT != PHENOMENOLOGY
SALIENT != EXPRESSION REGISTER
SALIENT != RESPONSE MOVE
SALIENT != CAUSAL ACTION
MESSAGE HOOK != CANDIDATE TRUTH
SESSION TOPIC != PERSISTENT ACTOR CONCERN
```

Message hooks are a separate **turn-relevance observation channel**. They may help a governed selector choose among already-lawful candidates, but they cannot create a claim, memory, belief, wound, concern, biography, relationship truth, or actor-access permission.

`VALID_EMPTY_SALIENCE` is lawful. No first-hook fallback, generic `other` hook, default concern, deep-memory resurrection, or plausible persona content is required.

V1 canonical salience output is an **unordered set**. No ranking, score, weight, threshold, priority scalar, or semantic order is canonicalized by CAN-016.

## 1. Governing authority and direct evidence

The Batch-03 common law and W1-B03-02 assignment were read at the exact launch base, together with:

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
- accepted ADP-016 / `V3_CAUSAL_MEMORY_FORMATION_FORGETTING_RECALL_RULE@1.0.0`;
- accepted ADP-017 / `V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0`;
- accepted ADP-024 / `V2_TRANSCRIPT_RETENTION_SUMMARIZATION_POLICY@1.0.1`;
- accepted ADP-026 / `CALLER_CURRENT_SITUATION_AUTHORITY@1.0.0`;
- accepted Batch-02 boundary law where wound/rupture/middle-state shortcuts are relevant;
- relevant historical callers/config/tests.

No Batch-03 sibling return and no active CAN-009 repair return was used as authority.

Binding accepted law establishes that V3 generates the life; `ActorAccessibleRenderEnvelope` or terminal equivalent is an immutable allowlisted ceiling; objective history, V3 memory, memory accessibility, epistemic stance, first-person permission, V2 session state and V2 expression remain distinct; keyword matching is not memory authority; caller/session inputs do not become biography by persistence; and missing authority or lawful emptiness fail closed rather than becoming plausible content.

### 1.1 Required historical archive

Required logical archive: `Rawlsing_code_bundle_staging.zip`.

Direct verification:

```text
expected SHA256:
953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086

computed SHA256:
953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086

verdict: EXACT_MATCH
ZIP entries: 13,138
```

Recovered V2/V3/server material is continuity / authority-recovery / negative-boundary evidence only. Historical V5/DDM has zero authority over current V550+ or the closed V3/V2 architecture.

### 1.2 Recovered source directly inspected

| Historical source | SHA256 | Use |
|---|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7` | standpoint/salience intent and negative shortcuts |
| `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135` | analyze/extract/select/refraction/topic machinery |
| `server/chat/turn.py` | `10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3` | keyword deep-memory / rupture-proxy surfacing |
| `v2/run_conversation_chat.py` | `b9276a4d7fc9dfdc83cc220528e4f16c1880d78419ed06430a5e9570a60efdc8` | conversation runner continuity |
| `v2/PIPELINE_WIRING_AUDIT.md` | `fabbf700ec6e83aae4a59266a58833871f6205655f022311865eb62381dbebe4` | analyze → extract → select direct wiring |
| `v3/tests/test_v5_v2_chat_prompt_no_raw_v5_leaks.py` | `53fb17b1db8fb53e265fe24c3ad617477dafe19bc7db4a2d153f1fe6d040b09c` | no-raw-state boundary |
| `v3/tests/test_v5_voice_packet_surface_allowlist.py` | `f82f71334edf368a7f09c1f40d5a9d24367a8528b997f5bc40347043ec5a300b` | allowlist continuity |
| `v3/tests/test_v5_render_surface_psyche.py` | `dfb9025e38d57fd3595cbb4a135a08427b758736a87e0dc5acde6a138e6b3584` | render-surface restriction |
| `v3/tests/test_v5_persona_sheet_surface_psyche.py` | `689beab6a72727f99c21db5485165278b1a8b346fc7daeda95dac677b37200c5` | persona surface restriction |
| `v3/tests/test_persona_sheet_integrity.py` | `dde6ddbb2a0b0cd3a1a1b9033818bac666eb69956f02ef3fa854516f20ab9825` | persona integrity |

Focused direct-source court from the exact archive:

```text
8 passed in 0.16s
```

Those tests are continuity evidence for surface confinement and integrity, not authority for historical salience scores or memory surfacing.

## 2. Jurisdiction

CAN-016 owns only:

- accepting a bounded set of exact already-lawful salience candidates;
- observing the current message for nontruth turn-relevance descriptors;
- optionally accepting separately governed noncausal session relevance hints without importing their semantics;
- invoking a versioned salience-selection rule that can only remove candidates;
- returning a turn-local salient candidate set;
- recording valid-empty, missing-authority, stale-envelope, forbidden-source, ambiguity and integrity outcomes;
- deterministic replay/provenance of that noncausal selection;
- compatibility disposition of recovered hook/salience/deep-memory machinery.

CAN-016 does **not** own V3 fact/memory/recall/accessibility/belief/claim permission; CAN-015 phenomenology; CAN-017 register; CAN-018 response move; CAN-019 relationship expression; CAN-020 attractor expression; CAN-021 session field semantics; MUST-022 uncertainty disclosure; MUST-023 boundary/face-risk/effort/attention; MUST-024 transcript policy; prompt/model authority; structural interpretation; wound/rupture semantics; or any salience score/ranking/decay/reinforcement/RNG default.

## 3. Complete recovered disposition court

Disposition vocabulary is exactly `PRESERVE`, `ADAPT`, `COMPATIBILITY_ONLY`, `REMOVE/REJECT`.

| Recovered mechanism / field | Disposition | Terminal holding |
|---|---|---|
| pipeline `analyze → hooks → salience` separation | `PRESERVE` | Keep message observation separate from selection/downstream planning. |
| `analyze_message()` pure current-message observation | `ADAPT` | Turn-local descriptors only; no actor truth. |
| request type/question/length/formality/valence fields | `COMPATIBILITY_ONLY` | May be re-registered by exact message-analysis rules. |
| numeric intensity/intimacy/topic-overlap formulas | `REMOVE/REJECT` | No canonical numeric semantics. |
| `extract_hooks()` mechanism | `ADAPT` | Nontruth descriptors from current message only. |
| `HOOK_KEYWORDS` exact taxonomy | `COMPATIBILITY_ONLY` | Migration vocabulary; no universal taxonomy frozen. |
| `HOOK_PHRASES` exact taxonomy | `COMPATIBILITY_ONLY` | Same. |
| phrase/keyword/continuation/fallback strengths `1.0/0.75/0.5/0.3` | `REMOVE/REJECT` | No hook-strength scale. |
| forced fallback `other` hook | `REMOVE/REJECT` | Empty relevance set is lawful. |
| continuation via `last_user_hooks` | `ADAPT` | Only through separately governed noncausal session hint seam. |
| `select_salient_hooks()` generic selectivity function | `ADAPT` | Subset-only selection over lawful candidates. |
| direct DRTS | `REMOVE/REJECT` | Index is not access/salience authority. |
| direct IAI | `REMOVE/REJECT` | Same. |
| direct RMT | `REMOVE/REJECT` | Same. |
| missing-value default `50` | `REMOVE/REJECT` | Missing never becomes midpoint/neutral state. |
| direct need magnitudes | `REMOVE/REJECT` | Raw V3/internal state cannot bypass actor-access ceiling. |
| direct `current_class` boost | `REMOVE/REJECT` | Class does not speak directly as psyche/concern. |
| direct current/childhood religion boost | `REMOVE/REJECT` | Religion label does not establish salience. |
| direct `minority_status` boost | `REMOVE/REJECT` | Demographic position does not establish salience. |
| raw identity scripts / moral loops / thought rails | `REMOVE/REJECT` | Internal labels cannot bypass actor-safe boundary. |
| wound-vector proxy/reconstruction | `REMOVE/REJECT` | Wound proxy is neither access nor salience. |
| wound defaults `50` / synthetic `72` | `REMOVE/REJECT` | Ungoverned psychological/numeric defaults. |
| rupture-note keyword→hook map / `+0.18` boost | `REMOVE/REJECT` | Rupture proxy cannot create salience or memory access. |
| legacy persona additive boosts | `REMOVE/REJECT` | No canonical ranking formula. |
| wound sensitivity formulas | `REMOVE/REJECT` | No wound→salience function. |
| EnergeticField tension/boredom/intimacy/curiosity boosts | `COMPATIBILITY_ONLY` | Future separately governed session-hint seam only; CAN-021 not consumed. |
| salience threshold `0.38` | `REMOVE/REJECT` | No canonical threshold. |
| first-hook fallback | `REMOVE/REJECT` | `VALID_EMPTY_SALIENCE` required. |
| score sorting as semantic rank | `REMOVE/REJECT` | Output is unordered set. |
| `HOOK_NEIGHBORS` | `COMPATIBILITY_ONLY` | Topic adjacency is not belief/misreading authority. |
| `compute_refraction_strength()` | `REMOVE/REJECT` | Outside CAN-016; numerically/psychologically underauthorized. |
| `apply_refraction()` heard-as substitution | `REMOVE/REJECT` | Hook cannot manufacture candidate truth/belief/misperception. |
| `update_topic_streams()` active streams | `COMPATIBILITY_ONLY` | Session continuity belongs elsewhere; not actor concern. |
| topic-stream decay/boost/max-count formulas | `REMOVE/REJECT` | No persistent salience semantics. |
| topic-stream `internal_tag` from psyche labels | `REMOVE/REJECT` | Session topic does not become hidden psyche. |
| `prepare_conversation_turn()` analyze/extract/select ordering | `ADAPT` | Preserve seam after each authority is separately satisfied. |
| `selected_hooks` diagnostics | `COMPATIBILITY_ONLY` | Audit/debug only. |
| `_DEEP_LAYER_HOOK_TAGS` | `REMOVE/REJECT` | Topic tags cannot unlock memory. |
| `_RUPTURE_KEYWORD_TO_HOOKS`, age thresholds 14/18/21 | `REMOVE/REJECT` | Heuristics cannot establish memory access. |
| `_should_surface_deep_memory()` | `REMOVE/REJECT` | Keyword match is not V3 recall/accessibility. |
| raw backstory scene extraction as “memory” | `REMOVE/REJECT` | Backstory/objective prose is not causal memory. |
| `SURFACED MEMORY` prompt injection | `REMOVE/REJECT` | Actor-omniscience leak. |
| `CARRIED WEIGHT` fallback | `REMOVE/REJECT` | No fallback wound/concern/texture. |
| surface allowlisting / no-raw-state test direction | `PRESERVE` | Salience must never defeat access filtering. |
| variable hook count / no fixed 1–2 | `PRESERVE` | Salience cardinality may be 0..N. |
| coherent selectivity intent | `ADAPT` | Governed narrowing, never stereotypes. |
| “standpoint” as direct personality filter | `REMOVE/REJECT` | V2 cannot reconstruct hidden personality from structure/analyst state. |
| topic gravity / avoidance inertia selection hints | `COMPATIBILITY_ONLY` | Future accepted session-hint interface only; not actor memory/concern. |

## 4. Canonical candidate/input contract

CAN-016 has two noncollapsible input channels.

### 4.1 Candidate-content channel

Only already-lawful content may become:

```text
V2SalienceCandidate {
  candidate_id,
  source_item_ref,
  source_item_hash,
  source_authority_id,
  source_authority_version,
  actor_id,
  actor_access_envelope_id,
  actor_access_envelope_hash,
  actor_access_as_of_causal_time,
  source_permission_ref,
  permitted_component_refs[],
  semantic_scope_refs[],
  candidate_hash,
  integrity_state
}
```

Rules:

1. Candidate traces to the exact current actor-safe V3 input envelope or another independently accepted V2 input contract that itself proves it is within that ceiling.
2. `DENY_FIRST_PERSON_CLAIM`, inaccessible content, actor-access unknown, analyst-only material, forbidden components, stale entries and missing source authority are not candidates.
3. Partial access creates candidates only for exact permitted component refs.
4. Candidate identity is exact source identity/hash; paraphrase, semantic similarity, embeddings, keyword overlap or model judgment cannot create identity.
5. Raw `GeneratedPersonRecord`, V3 checkpoint, V558/V550+ structure, objective ledger, persona sheet, backstory prose, transcript summary or analyst explanation cannot be directly promoted.

CAN-016 v1 does not require a permanent candidate-kind taxonomy.

### 4.2 Turn-relevance channel

```text
V2TurnRelevanceObservation {
  observation_id,
  turn_id,
  exact_message_artifact_ref,
  exact_message_artifact_hash,
  observation_kind,
  descriptor_ref,
  extractor_rule_id,
  extractor_rule_version,
  extractor_rule_hash,
  source_span_or_match_ref,
  session_hint_refs[],
  observation_hash,
  integrity_state
}
```

These observations describe the current message or an explicitly noncausal session hint; they do not describe the actor. CAN-016 v1 freezes **no universal message-hook taxonomy and no numeric hook strength**.

### 4.3 Optional session hint seam

A `SeparatelyGovernedV2SessionRelevanceHintRef` may be consumed only after the producing session authority is independently accepted, with exact authority/session/cursor/hash provenance, presentation-only status and a strict rule that the hint may only select among current candidates. It may not add content, widen access, become memory, or prove persistent concern.

Until that separate authority exists, the seam is `DEFERRED_SEPARATE_SESSION_AUTHORITY`. CAN-016 does not consume CAN-021 as accepted authority.

## 5. Accessibility ceiling

Let `A` be exact currently actor-permitted source components, `C` the candidate set, and `S` the salient set:

```text
C ⊆ A
S ⊆ C
```

Any selector result outside `C` is `SALIENCE_ACCESS_CEILING_VIOLATION`.

Actor-access permission is bound to exact V3 source/checkpoint hash and causal time. A stale cached envelope yields `SALIENCE_STALE_ACCESS_ENVELOPE`; no current salience may be derived from it.

A message hook establishes only that the current message matches descriptor H under extractor R. It cannot establish that the actor remembers H, cares about H, is wounded around H, believes a claim about H, or has access to objective history about H.

## 6. Selection rule contract

A concrete selector must be registered as the semantic equivalent of:

```text
V2SalienceSelectionRule {
  rule_id,
  rule_version,
  rule_hash,
  admitted_candidate_source_classes[],
  admitted_relevance_observation_kinds[],
  admitted_session_hint_classes[],
  deterministic_match_or_filter_semantics,
  tie_or_multiplicity_semantics,
  output_cardinality_semantics,
  forbidden_inference_set[],
  provenance_requirements,
  integrity_requirements
}
```

A rule may retain 0..N already-lawful candidates, use exact registered relevance descriptors as filter conditions, preserve multiple simultaneous candidates, and return empty.

A rule may not create/transform candidate content, dereference forbidden material, infer candidate truth from a hook, select by raw class/religion/minority/structure, infer memory accessibility, infer wound/rupture salience from proxies, invent a winner from missing comparison authority, use unregistered numeric weights/defaults, or use an LLM preference as authority.

Candidates with no applicable accepted selector relation produce `SALIENCE_SELECTION_RULE_MISSING`, not a fallback winner. A required nonmultiplicity choice that remains underdetermined produces `SALIENCE_SELECTION_AMBIGUOUS`.

## 7. Output and turn-local persistence

Every attempt emits an immutable noncausal:

```text
V2TurnSalienceReceipt {
  receipt_id,
  authority_id,
  authority_version,
  turn_id,
  actor_id,
  actor_access_envelope_ref,
  actor_access_envelope_hash,
  candidate_set_hash,
  relevance_observation_set_hash,
  session_hint_set_hash_or_null,
  selector_rule_id_or_null,
  selector_rule_version_or_null,
  selected_candidate_refs[],
  status,
  receipt_hash,
  provenance_refs[],
  integrity_state
}
```

`selected_candidate_refs[]` is semantically a **set**. Stable ID sorting is allowed only for deterministic serialization and carries no rank meaning.

Salience semantic authority ends with the turn. A later turn recomputes from the then-current access envelope, candidates, message/relevance observations, optional separately governed session hints, and selector version.

Therefore repeated later selection is a new selection rather than reinforcement; later absence is not forgetting; transcript retention is not persistent concern; session recurrence is not actor belief; and CAN-016 defines no salience decay, strengthening, habituation, sensitization or persistent concern state. ADP-024 may retain receipts for audit without extending their semantic lifetime.

## 8. Ranking / numeric disposition

`NO_CANONICAL_SALIENCE_SCORE_OR_RANKING_FORMULA`

Specifically nonauthoritative are hook strengths `1.0/0.75/0.5/0.3`, default `50`, wound proxy `72`, DRTS/IAI/RMT thresholds, need thresholds, historical additive boosts, field modulation formulas, threshold `0.38`, topic-stream decay/boost/caps, refraction floors/ceilings/variance, fixed top-N, and first-hook fallback.

CAN-016 v1 has no stochastic selection rule. Any future numeric or stochastic selector requires exact separately governed quantity/formula/randomness semantics and replay receipts. Missing numeric authority does not imply zero, midpoint, equal weight or uniform choice.

## 9. Canonical statuses

- `SALIENT_TURN_SET` — 1..N exact candidates lawfully selected.
- `VALID_EMPTY_SALIENCE` — lawful selection yields zero candidates, including lawful empty candidate set.
- `SALIENCE_INPUT_UNKNOWN` — required input is unknown; no substitution.
- `SALIENCE_ACCESS_DEFERRED` — relevant V3 access is missing/unknown; material excluded.
- `SALIENCE_INPUT_INACCESSIBLE` — actor-inaccessible/denied source cannot be candidate.
- `FORBIDDEN_SALIENCE_SOURCE` — raw structure, analyst truth, objective history, prohibited backstory/session proxy, etc.
- `SALIENCE_SELECTION_RULE_MISSING` — inputs exist but no accepted selector governs them.
- `SALIENCE_SELECTION_AMBIGUOUS` — applicable rule cannot lawfully resolve required choice and does not permit multiplicity.
- `SALIENCE_STALE_ACCESS_ENVELOPE` — stale V3 permission source.
- `SALIENCE_ACCESS_CEILING_VIOLATION` — output exceeds candidate/permission ceiling.
- `SALIENCE_INTEGRITY_FAILURE` — source/hash/version/actor/turn/provenance mismatch.
- `DEFERRED_SEPARATE_SESSION_AUTHORITY` — session hint semantics not independently governed.

```text
VALID_EMPTY_SALIENCE != UNKNOWN
UNKNOWN != INACCESSIBLE
INACCESSIBLE != FORBIDDEN_SOURCE
MISSING_SELECTION_RULE != EMPTY
SESSION_HINT_ABSENT != ACTOR_HAS_NO_CONCERN
NO_MATCHING_HOOK != NO_MEMORY
```

No state licenses fallback content.

## 10. Replay / provenance

Same exact deterministic inputs must reproduce the same semantic salient set and receipt hash.

Replay identity includes:

- CAN-016 authority ID/version/hash;
- actor ID;
- actor-access envelope ID/hash/schema/as-of causal time;
- source permissions/component refs;
- candidate IDs/hashes and candidate-set hash;
- turn ID and exact current message artifact ID/ref/hash;
- message analyzer/extractor IDs/versions/hashes;
- relevance observation IDs/hashes;
- separately governed session-hint refs/authority/cursor/hash where used;
- selector rule ID/version/hash;
- selected candidate set hash;
- receipt status/hash and integrity receipts.

Hidden wall clock, mutable `latest`, filesystem/dictionary iteration order, unrecorded prompt/model output, undeclared randomness, unversioned keyword table, stale session state and raw V558/V550+ lookup are forbidden replay dependencies.

## 11. Hostile fixtures

| ID | Attack | Required outcome |
|---|---|---|
| `CAN016-H01` | inaccessible objective fact matches keyword | `SALIENCE_INPUT_INACCESSIBLE` |
| `CAN016-H02` | access unknown but message strongly matches | `SALIENCE_ACCESS_DEFERRED` |
| `CAN016-H03` | raw V558 prior offered | `FORBIDDEN_SALIENCE_SOURCE` |
| `CAN016-H04` | analyst explanation offered | no candidate/concern |
| `CAN016-H05` | class=`working` + wages message | no class boost |
| `CAN016-H06` | religion label + God message | no religion boost |
| `CAN016-H07` | minority status + identity message | no demographic boost |
| `CAN016-H08` | DRTS/IAI/RMT direct inputs | reject legacy input |
| `CAN016-H09` | missing metric defaults to 50 | reject default |
| `CAN016-H10` | rupture keyword overlap | no rupture salience/memory |
| `CAN016-H11` | wound proxy 72 | no wound salience |
| `CAN016-H12` | keyword deep-memory finds scene | reject memory retrieval |
| `CAN016-H13` | `CARRIED WEIGHT` fallback | reject filler |
| `CAN016-H14` | no registered hooks | lawful empty relevance |
| `CAN016-H15` | candidates but no selector | `SALIENCE_SELECTION_RULE_MISSING` |
| `CAN016-H16` | selector chooses none | `VALID_EMPTY_SALIENCE` |
| `CAN016-H17` | first-hook fallback | reject fallback |
| `CAN016-H18` | hook inserted as actor claim | reject hook-as-truth |
| `CAN016-H19` | contradictory actor-safe claims both relevant | preserve both |
| `CAN016-H20` | selector returns outside candidates | `SALIENCE_ACCESS_CEILING_VIOLATION` |
| `CAN016-H21` | partial access | exact permitted components only |
| `CAN016-H22` | cached stale envelope | `SALIENCE_STALE_ACCESS_ENVELOPE` |
| `CAN016-H23` | receipt retained 100 turns | no persistent concern |
| `CAN016-H24` | same topic selected next turn | new receipt; no reinforcement |
| `CAN016-H25` | topic absent next turn | not forgetting |
| `CAN016-H26` | session hint before authority | `DEFERRED_SEPARATE_SESSION_AUTHORITY` |
| `CAN016-H27` | future session hint but no actor-safe candidate | cannot create candidate |
| `CAN016-H28` | hidden LLM ranks relevance | reject selector authority |
| `CAN016-H29` | numeric score without formula authority | reject numeric semantics |
| `CAN016-H30` | winner required but tie law absent | `SALIENCE_SELECTION_AMBIGUOUS` |
| `CAN016-H31` | stable-ID serialization sort | allowed, nonsemantic only |
| `CAN016-H32` | salient item promoted to belief | reject |
| `CAN016-H33` | salience mutates V3 | reject |
| `CAN016-H34` | message hash differs on replay | new receipt identity required |
| `CAN016-H35` | candidate source hash mismatch | `SALIENCE_INTEGRITY_FAILURE` |
| `CAN016-H36` | many hooks, lawful selector selects none | `VALID_EMPTY_SALIENCE` |

## 12. Consumers and blockers

Primary consumers are `V2-P2` and `V2-P5`. CAN-016 closes only its own semantic dependency.

```text
V2-P2 remaining independent blockers:
  CAN-015
  MUST-022
  implementation/release gates

V2-P5 remaining independent blockers:
  CAN-017
  CAN-018
  MUST-022
  MUST-023
  implementation/release gates
```

Accepted ADP-017 is consumed as the access ceiling, not re-owned here. CAN-021 is a same-batch sibling and is not consumed as authority; only an abstract future session-hint seam is exposed.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT_FOR_CAN_016_JURISDICTION__NOT_STANDALONE_V2_P2_OR_V2_P5_RELEASE`

## 13. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

Hard authority uniquely fixes the ceiling/noncollapse: no access widening, no structure/analyst→psyche shortcut, no keyword→memory, turn-local/noncausal salience, valid-empty, and no ungoverned numerics.

A genuine lawful ambiguity remained in the canonical output shape:

1. freeze the recovered ranked score list;
2. replace it with another invented qualitative priority ladder;
3. canonicalize the minimum sufficient object: an unordered subset of already-lawful candidates, leaving ranking/attention allocation absent until separately governed.

Choice: **3**.

A second bounded ambiguity was whether to freeze the historical message-hook taxonomy. The choice is to preserve the extractor/descriptor interface while leaving concrete hook registrations versioned/optional rather than turning old keyword tables into permanent human ontology.

Tie-break principles: actor opacity, mediation, contradiction/multiplicity, lawful absence, downstream vividness never exceeding upstream authority, minimum sufficient machinery, provenance/replay, and no personality essentialization.

The Governing Spirit supplied no candidate content, psychological state, hook taxonomy, ranking rule, or numeric formula.

## 14. Final verdict

No production code was modified. V2 was not implemented. No V3 memory/accessibility/epistemic authority was widened. No Batch-03 sibling return was consumed.

`CAN_016_V2_SALIENCE_ACCESSIBILITY_CANONICALIZATION = PASS`
