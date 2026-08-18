# CAN-019 — V2 Relationship Expression Canonicalization

**Authority ID:** `V2_RELATIONSHIP_EXPRESSION_RULE`  
**Authority version:** `1.0.0`  
**RA-R00 item:** `CAN-019`  
**Cell:** `W1-B04-01`  
**Owner:** V2 actor-limited relationship-expression / presentation boundary  
**Mode:** authority canonicalization only  
**Architecture:** `CLOSED__NOT_REOPENED`  
**Launch base:** `131f3b5ea3e5cc7dafafa4ace65499afe2fb0b53`  
**Verdict:** `PASS`

## 1. Binding holding

V3 generates relationship life. V2 may express only the exact relationship material that the current actor may lawfully access, and may maintain bounded presentation-only relationship posture inside the current session. Neither expression nor persistence creates relationship truth.

```text
OBJECTIVE_RELATIONSHIP_HISTORY_STATE = V3
ACTOR_CAUSAL_RELATIONSHIP_MEMORY     = V3
ACTOR_ACCESSIBLE_PERCEIVED_VIEW      = V3 RENDER BOUNDARY
V2_RELATIONSHIP_EXPRESSION           = NONCAUSAL TURN/PRESENTATION
V2_SESSION_RELATIONSHIP_POSTURE      = SESSION/PRESENTATION ONLY
RENDERED_TONE                        != RELATIONSHIP TRUTH
```

Additional binding noncollapse:

```text
ONE_ACTOR_VIEW != RECIPROCAL_RELATIONSHIP_TRUTH
TRANSCRIPT_REPETITION != TRUST_OR_INTIMACY
SESSION_AVOIDANCE != WOUND_OR_RELATIONSHIP_TRUTH
APPLICATION_RELATION_MODE != GENERATED_RELATIONSHIP_KIND
RELATIONSHIP_EXPRESSION != GENERIC_SALIENCE_OR_REGISTER_OR_RESPONSE_MOVE
SESSION_POSTURE != V3_RELATIONSHIP_STATE_OR_CAUSAL_MEMORY
```

`VALID_EMPTY_RELATIONSHIP_EXPRESSION` is lawful. Missing actor-safe relationship input stays missing. Contradictory or asymmetric actor views remain separate; CAN-019 never manufactures an objective synthesis.

## 2. Direct archive verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- computed directly from archive bytes: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- verdict: `EXACT_MATCH`
- ZIP entries: `13,138`

Recovered V2/V3/server source is continuity, authority-recovery and negative-boundary evidence only. Historical V5/DDM has zero authority over current V550+.

## 3. Governing and accepted authority consumed

Binding current law inspected at the exact launch base includes Batch-04 common law; `CURRENT_STATE.md`; `RAWLSING_GOVERNING_SPIRIT.md`; V2 and V3 completion rulings; whole-machine closure; implementation-release synthesis; W0 closure; W1 first-batch, Batch-02 and Batch-03 adjudication rulings; RA-R00 MD/JSON; accepted TD-R06 V2; and relevant accepted authority artifacts.

Direct semantic dependencies/boundaries consumed:

1. `ADP-016 / V3_CAUSAL_MEMORY_FORMATION_FORGETTING_RECALL_RULE@1.0.0` — causal relationship memory remains V3 memory; V2 transcript/session material cannot form it.
2. `ADP-017 / V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0` — the current immutable actor-accessible render envelope is the hard ceiling. Objective relationship state hidden from the actor cannot enter CAN-019.
3. `ADP-024 / V2_TRANSCRIPT_RETENTION_SUMMARIZATION_POLICY@1.0.1` — transcript/session identity, cursor, compaction and close provenance only; retention does not create relationship truth or memory.
4. `ADP-026 / CALLER_CURRENT_SITUATION_AUTHORITY@1.0.0` — source/subject/time-bounded application or caller context may guide presentation only within its original jurisdiction; application role labels are not generated relationship facts.
5. Accepted `CAN-016` — generic salience is turn-local subset selection and remains separately owned.
6. Accepted `CAN-017` semantic ruling — generic register may narrow/withhold/style but remains separately owned; CAN-019 supplies no generic register taxonomy.
7. Accepted `CAN-021` — session topic/avoidance/energetic continuity is noncausal and is not relationship truth.

The still-open CAN-018 continuation was not consumed as authority. No same-batch CAN-020 result was consumed.

## 4. Direct recovered-source inventory

The exact archive was directly inspected for relationship/session continuity and callers. Relevant source SHA256 values:

| Historical source | SHA256 | CAN-019 disposition |
|---|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7` | Primary recovery evidence for RelationshipMemory, asymmetry and posture; decompose. |
| `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135` | Generic appraisal/intimacy/field machinery; relationship truth use rejected; neighboring owners preserved. |
| `v2/spec.py` | `f7ca16a7addf4dd1bd155a985586f926f1a4c31f127b829bcb8056c851d58296` | Compatibility/config evidence only. |
| `v2/run_conversation_chat.py` | `b9276a4d7fc9dfdc83cc220528e4f16c1880d78419ed06430a5e9570a60efdc8` | Caller/render continuity only. |
| `server/session_state.py` | `9c9c3b0e2b3bff700af127e03805166102920019d6acd099ee8270fbe63bc15a` | Session lifecycle and `chat_relation_mode`; routing context only. |
| `server/session_db.py` | `0d9bf508aa748ce8eff3360a7c615ab0ed086f3a34c3190815cb0485fe234c12` | Transcript/session persistence; no canonical RelationshipMemory persistence. |
| `server/chat/turn.py` | `10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3` | Deep-memory / carried-weight prompt shortcuts are negative evidence. |
| `server/routes/session_bootstrap.py` | `f8f2c2665d8a56534ca10c189b12c761914bf4ad67470c2a805481785dcaa27d` | Session/bootstrap continuity only. |
| `server/routes/session_summary.py` | `c60ad7dbaeba82851b80241105181dd9e513cd0e52c068ecd055c8c02682b822` | Summary is not relationship authority. |
| `v3/core/state.py` | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` | Historical V3 `Magnet` relationship numeric state is nonterminal compatibility evidence. |
| `v3/io/persona_sheet.py` | `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e` | Surface posture/avoidance continuity; actor-safe boundary now governs. |
| `v3/tests/test_v5_surface_psyche_profile.py` | `195f60b1fe34aefe36279b85eef4c48c01d57d55d5faab68ab3cfab5e9b7ad66` | Surface allowlist direction only. |
| `v3/tests/test_wave4.py` | `10f8978cf5cfdd52395102ba7b1c01d7475ffaf14665a3edfd50b60249e60e90` | Historical relationship event/magnet numerics; negative numeric authority evidence. |
| `v3/tests/test_connector_and_field_injection.py` | `72189c791264af27334c66d84c95a24303863decf4794f5a599913eeb4fe33ab` | Historical structural trust mapping; rejected as direct relationship-expression authority. |
| `v3/tests/test_llm_contract.py` | `bb9635bc1bac694666694e8a9305c8b72a2d90ea0c1b64d5aeb93d024166ce68` | Model relationship proposals do not create semantic truth. |

The recovered spec describes a monolithic persistent `Relationship Memory`; the recovered `conversation_engine.py` does not implement that object as a typed runtime store. Current repository terrain at the launch base does not supply a competing terminal RelationshipMemory implementation. The closed architecture therefore governs the decomposition.

## 5. Recovered monolithic RelationshipMemory — field-by-field disposition

Recovered historical shape:

```text
user_facts
trust = 0.2
intimacy_level = 0.15
topics_to_avoid[]
inside_references[]
sticky_triggers[]
relational_posture{}
```

| Recovered field/mechanism | Disposition | Terminal holding |
|---|---|---|
| `user_facts` | `SPLIT_AND_ADAPT_BY_REFERENCE` | Caller/session assertions may remain exact ADP-024/026 session evidence. They do not become actor knowledge, causal memory, relationship truth or biography. Generated-actor first-person use remains bounded by ADP-017. |
| `trust` | `REMOVE_AS_V2_PERSISTENT_RELATIONSHIP_STATE` | Legacy default `0.2`, drift and scalar trust are nonauthority. A separately governed V3 actor-perceived/accessible trust-like claim may be expressed only by exact actor-safe ref; V2 owns no trust state. |
| `intimacy_level` | `REMOVE_AS_V2_PERSISTENT_RELATIONSHIP_STATE` | Legacy `0.15`, deltas and thresholds are nonauthority. Session EnergeticField `intimacy` is also not relationship truth. Exact V3 actor-safe relationship material may be expressed by ref only. |
| `topics_to_avoid` | `DECOMPOSE_TO_OWNERS` | Historical strings are compatibility vocabulary only. Generic boundary/face-risk semantics belong to MUST-023; session avoidance continuity belongs CAN-021; a relationship-specific limit may be carried only from exact actor-safe source authority. |
| `inside_references` | `ADAPT_AS_NONCAUSAL_SESSION_REFERENCE_CONTINUITY` | Exact transcript/artifact/cursor refs may support presentation continuity under ADP-024. They do not prove causal memory, shared relationship history or reciprocity. |
| `sticky_triggers` | `COMPATIBILITY_ONLY__NO_INDEPENDENT_AUTHORITY` | Historical trigger strings are not a canonical taxonomy and cannot create wound, motive, boundary or relationship truth. Only separately governed source refs may constrain expression. |
| `relational_posture` | `ADAPT_TO_V2_SESSION_RELATIONSHIP_POSTURE` | Preserve an open-ended, sparse, source-bound session presentation cache. Freeze zero concrete posture labels and zero weights in v1. No automatic drift or causal persistence. |
| recurring conversation grooves | `ADAPT_AS_SESSION_CONTINUITY_ONLY` | Exact session history may be referenced, but recurrence is not actor concern, memory, trust, intimacy or relationship evolution. |
| relationship asymmetry | `ADAPT_AS_PERSPECTIVE_PRESERVATION` | Preserve actor-specific/perceiver-specific views and presentation constraints. Recovered patience/interest/willingness examples are not terminal dimensions or scales. |
| trust/intimacy appraisal deltas | `REMOVE_FROM_CAN019` | Generic appraisal/face-risk/boundary logic belongs neighboring authorities; no CAN-019 scalar mutation. |
| `chat_relation_mode` (`alternate_self`, `generated_persona`, `stored_legacy`) | `APPLICATION_ROUTING_COMPATIBILITY_ONLY` | May identify application/session routing behavior; cannot become a generated relationship kind or actor relationship fact. |
| historical V3 `Magnet.intensity = 50` / tenure drift | `HISTORICAL_V3_COMPATIBILITY_ONLY` | Current V3 relationship truth belongs separately governed relationship-history authority. No V2 expression authority derives from these numerics. |
| prior rendered affectionate/hostile wording | `AUDIT_ARTIFACT_ONLY` | Tone/text is never relationship evidence merely because it was rendered or retained. |

## 6. Exact jurisdiction and consumer

Owner: **V2 actor-limited relationship-expression / presentation boundary**.

CAN-019 owns only:

- the `V2_RELATIONSHIP_EXPRESSION_DECISION` identity and machine contract;
- exact actor-safe relationship/perceived-view component references admitted to that decision;
- perspective/asymmetry preservation records;
- sparse source-owned relationship-expression constraint references;
- `V2_SESSION_RELATIONSHIP_POSTURE` as session/presentation-only continuity;
- valid-empty, unknown, missing, deferred, denied and integrity states;
- deterministic semantic replay/provenance for these noncausal records;
- compatibility disposition of recovered RelationshipMemory fields.

Primary consumer: **`V2-P6` — relationship/memory split**.

CAN-019 does not own relationship creation/evolution, household/genealogy, V3 causal relationship memory, ADP-017 claim accessibility, CAN-016 generic salience, CAN-017 generic register, CAN-018 generic response-move semantics, MUST-023 boundary/face-risk/effort/attention, CAN-021 session field, CAN-020 attractor expression, ADP-024 retention, ADP-025 renderer/model policy, or causal interaction admission.

## 7. Canonical input contract

A semantic equivalent of `V2RelationshipExpressionInput` binds:

```text
session_id
turn_id
actor_id
actor_access_envelope_id
actor_access_envelope_hash
actor_access_as_of_causal_time
actor_safe_relationship_component_refs[]
actor_safe_relationship_memory_component_refs[]
source_perspective_bindings[]
prior_session_relationship_posture_ref | null
v2_session_provenance_refs[]
caller_application_context_refs[]
input_integrity_state
```

### Admissible relationship-content inputs

1. Exact V3-derived actor-perceived relationship-view components that are included in the current ADP-017 actor-safe render envelope.
2. Exact ADP-016 relationship-memory components only when their current ADP-017 accessibility/claim permissions independently permit the relevant component.
3. Exact actor-safe relationship claims/components already carried through a compatible accepted V2 projection without semantic widening.
4. Exact session/app context refs under ADP-024/026 only as noncausal interaction context or provenance; they cannot authorize generated relationship propositions.

Every relationship-content component must retain exact source identity/hash, source authority/version, actor/perceiver binding, counterpart/referent binding where applicable, temporal scope and current actor-access permission.

### Inadmissible semantic sources

Objective V3 relationship state outside the actor-safe envelope; inaccessible relationship memory; raw transcript or summary repetition; tone; session EnergeticField; CAN-021 avoidance; generic salience/register/move output used as truth; structural priors; class/religion/demography; application role labels; model/LLM inference; historical RelationshipMemory defaults; prior rendered prose; current V558/V550+ structural material; or a same-batch sibling return.

## 8. Actor-access ceiling and asymmetry law

For every positive CAN-019 decision:

```text
expressible_relationship_components
    ⊆ exact_current_actor_safe_relationship_components
```

CAN-019 may narrow; it can never widen, reconstruct hidden objective state, infer an omitted proposition, or resurrect stale permission.

Perspective is mandatory. Each relationship component or posture source preserves a semantic equivalent of:

```text
perceiver_actor_id
relationship_referent_or_counterpart_ref
source_claim_or_view_ref
source_temporal_scope
source_permission_ref
```

One actor's view of another supplies no reciprocal fact. Two actors' views are two perspective-bound records even when they agree. If they conflict, both may remain representable where each is independently lawful; CAN-019 does not average, vote, choose a scalar winner or infer objective relationship truth.

If the current actor-safe envelope changes, a prior CAN-019 decision or posture ref cannot retain broader permission. It must be revalidated or fail closed as stale.

## 9. Canonical output contract

A semantic equivalent of:

```text
V2_RELATIONSHIP_EXPRESSION_DECISION {
  decision_id,
  authority_id = V2_RELATIONSHIP_EXPRESSION_RULE,
  authority_version = 1.0.0,
  session_id,
  turn_id,
  actor_id,
  actor_access_envelope_id,
  actor_access_envelope_hash,
  admitted_relationship_component_refs[],
  source_perspective_bindings[],
  relationship_expression_constraint_refs[],
  withheld_or_denied_records[],
  session_posture_input_ref,
  session_posture_result_ref,
  status,
  provenance_refs[],
  decision_hash,
  integrity_state
}
```

The v1 authority freezes **zero concrete relationship posture labels, zero tone labels, zero trust/intimacy bands, and zero relationship-specific response-move vocabulary**.

`relationship_expression_constraint_refs[]` are opaque, exact, source-owned semantic constraints already authorized by the relevant source authority. CAN-019 may preserve and narrow them but cannot invent their meaning. Generic salience/register/response-move owners consume the resulting relationship-safe envelope only under their own authority.

The decision is noncausal. It does not assert that the relationship objectively has any property merely because that property is used as an actor-safe presentation constraint.

## 10. V2 session relationship posture boundary

Canonical record: `V2_SESSION_RELATIONSHIP_POSTURE`.

Epistemic class: `V2_SESSION_STATE__RELATIONSHIP_PRESENTATION_NONCAUSAL`.

Scope: exactly one `session_id` plus explicit session/interlocutor binding. An application/session interlocutor label does not imply a V3 relationship entity or kind.

Required semantic fields:

```text
posture_id
session_id
session_interlocutor_ref
actor_id
authority_id/version
revision_id
previous_revision_ref | null
source_relationship_component_refs[]
source_expression_constraint_refs[]
source_decision_refs[]
last_validated_actor_access_envelope_ref
lifecycle_state
integrity_state
```

Lifecycle states:
`VALID_EMPTY | ACTIVE_SESSION_ONLY | RESET_EMPTY | SESSION_ENDED | MISSING_OR_UNAVAILABLE | INTEGRITY_FAILED`.

Rules:

- bootstrap/new session: `VALID_EMPTY`; no default friendliness, distrust, intimacy, hostility or posture;
- carry-forward: exact source-backed presentation refs may persist unchanged within the session only while their source identity and current actor-access permission remain valid;
- update: requires exact source/decision refs; raw transcript frequency, tone, model inference and elapsed turns do not update posture;
- no automatic numeric drift/reinforcement/decay exists;
- reset clears current presentation posture while preserving audit lineage and does not alter V3 relationship state or memory;
- formal end follows the ADP-024 close receipt; disconnect/restart is not relationship change;
- new session does not auto-import prior posture;
- compaction/summary cannot reconstruct or strengthen posture;
- missing previously committed posture remains `MISSING_OR_UNAVAILABLE` or integrity failure as appropriate, never guessed from transcript.

## 11. Relationship-specific narrowing without neighboring-authority theft

CAN-019 produces a **relationship-safe constraint envelope**, not a complete expression plan.

- CAN-016 owns whether already-lawful material is turn-salient.
- CAN-017 owns generic register narrowing/withholding/style operations.
- CAN-018 owns the generic response-move membrane after independent acceptance.
- MUST-023 owns boundary, face-risk, effort and attention semantics.
- CAN-021 owns generic session EnergeticField/topic/avoidance continuity.

CAN-019 may state that an exact actor-safe relationship component or source-owned relationship constraint is available, denied, withheld for relationship-specific source reasons, or perspective-bound. It does not define generic selection, style, effort, boundary or move algorithms.

## 12. Positive / valid-empty / unknown / missing / deferred / denied / integrity law

Canonical decision statuses:

- `RELATIONSHIP_EXPRESSION_AUTHORIZED` — one or more exact actor-safe relationship components/constraints are admitted to the noncausal relationship-expression envelope.
- `VALID_EMPTY_RELATIONSHIP_EXPRESSION` — no relationship-specific component/constraint is supplied or required for this turn; generic V2 expression may proceed under its own authorities. Zero relationship expression is lawful.
- `UNKNOWN_RELATIONSHIP_VIEW` — upstream actor-safe material explicitly preserves unknown, unresolved, noncomparable or contradictory state such that no stronger relationship assertion is authorized. Preserve that state; do not synthesize.
- `MISSING_ACTOR_SAFE_RELATIONSHIP_INPUT` — a requested/required relationship expression lacks its exact actor-safe source/ref. Do not fill from objective history, transcript, tone or defaults.
- `DEFERRED_MISSING_RELATIONSHIP_SEMANTIC_AUTHORITY` — the desired relationship-specific constraint depends on an owner/rule that is absent or not accepted. No local fallback.
- `DENIED_ACTOR_ACCESS` — exact objective/memory material exists but current ADP-017 permission denies the component.
- `DENIED_FORBIDDEN_RELATIONSHIP_SOURCE` — input derives from transcript repetition, structural/demographic shortcut, role label, model inference, rendered wording or another forbidden source.
- `INTEGRITY_FAILED` — source hash/version, actor/perceiver/counterpart binding, envelope freshness, posture revision, cursor/lineage, or decision identity fails verification.

Unknown is not denial. Missing is not valid-empty. Valid-empty is not evidence of a weak relationship. Denial is not actor ignorance. No state licenses a plausible substitute.

## 13. Numeric and default disposition

CAN-019 v1 defines **no canonical numeric relationship quantity, score, probability, closeness/trust/intimacy scale, reciprocity score, posture weight, drift, decay, threshold or ranking formula**.

Compatibility/migration/audit-only; semantic use denied absent separately accepted authority:

- RelationshipMemory `trust = 0.2`;
- RelationshipMemory `intimacy_level = 0.15`;
- trust/intimacy appraisal deltas;
- recovered relationship-asymmetry patience/interest/willingness scales or slow drift;
- message-analysis `intimacy_demand` values such as `0.7` / `0.3`;
- EnergeticField `intimacy` `0..1`, its decay/boosts/thresholds;
- historical V3 `Magnet.intensity = 50`, `0..100` clamp and tenure-driven intensify/decay;
- any structural/social trust index used as a direct relationship scalar;
- default “friend,” “user,” `generated_persona`, or similar application label as a generated relationship kind;
- count/frequency of friendly, hostile, intimate or avoidant transcript turns as a relationship-strength proxy.

Exact cursor/turn ordinals and artifact cardinalities remain audit mechanics only. They do not become relationship magnitude.

## 14. Render / causal boundary

Rendered tone, wording, warmth, hostility, affection, distance or avoidance is a noncausal artifact. It cannot update the current CAN-019 semantic source set, V3 relationship state or causal memory merely because it appeared.

If an observable interaction is intended to matter causally, the exact artifact must cross the separately governed V2→V3 packaging and V3 admission path. Even after admission, CAN-019 does not decide relationship effect, relationship evolution or memory formation; those remain V3-owned under their own rules.

## 15. Replay and provenance

Every relationship-expression decision preserves at minimum:

- CAN-019 authority ID/version;
- session/turn/actor identity;
- exact ADP-017 envelope ID/hash/as-of causal time;
- exact admitted/denied relationship component refs and source hashes;
- source authority IDs/versions;
- exact perceiver/counterpart/perspective bindings;
- source temporal scopes and permission refs;
- prior/result session-posture revision refs when used;
- ADP-024 transcript/session cursor/artifact refs when used for provenance only;
- ADP-026 current-situation refs when used;
- status, withheld/denied reason records and integrity state;
- deterministic decision hash.

Same exact semantic inputs, source ordering where order is semantically relevant, source authority versions, actor-access envelope and CAN-019 version must reproduce the same relationship-expression decision and posture revision.

Hidden wall clock, filesystem order, transcript rescanning, mutable `latest`, LLM/model judgment, prior rendered wording and numeric legacy defaults may not change the semantic decision.

Renderer/model nondeterminism belongs ADP-025 and may vary surface wording without changing the CAN-019 decision. A stale actor-access envelope, broken perspective binding, mismatched source hash/version, posture revision break, unauthorized cross-session carry or source ref that no longer verifies is fail-closed.

## 16. Hostile fixtures

1. Hidden objective V3 relationship fact offered to V2 while actor access denies it → `DENIED_ACTOR_ACCESS`; never express.
2. Actor A has an accessible view “I trust B” → no inference that B trusts A.
3. A and B have conflicting generated perceived views → preserve separate perspective-bound records; no objective synthesis.
4. One actor has two independently lawful contradictory relationship claims → preserve contradiction; no scalar winner/coherence repair.
5. Warm rendered tone → relationship truth → reject.
6. Fifty friendly transcript turns → increased trust/intimacy → reject.
7. Session topic avoidance → wound or relationship truth → reject.
8. Class/religion/demography directly chooses relationship posture → reject.
9. `chat_relation_mode=generated_persona` or application label `friend` → generated relationship fact → reject.
10. Missing relationship input defaults to `trust=0.2` → `MISSING_ACTOR_SAFE_RELATIONSHIP_INPUT` or valid-empty as context requires; never default.
11. Missing intimacy defaults to `0.15` → reject numeric default.
12. Message heuristic `intimacy_demand=0.7` becomes relationship intimacy → reject.
13. CAN-021 EnergeticField intimacy becomes relationship truth → reject ownership collapse.
14. Historical `sticky_triggers` string hit creates wound/relationship motive → reject absent exact separately owned source authority.
15. `inside_references` retained in transcript are narrated as causal shared memory without ADP-016/017 permission → reject; session reference continuity only.
16. Prior rendered affectionate wording updates session relationship posture by itself → reject.
17. LLM says “you two are close” → no semantic authority.
18. Stale `ActorAccessibleRenderEnvelope` used after access changed → `INTEGRITY_FAILED` / fail closed.
19. Relationship component rebound from actor A's perspective to actor B → `INTEGRITY_FAILED`.
20. New session auto-imports old relational posture → reject; new posture is `VALID_EMPTY` absent separate authority.
21. Session reset/close is treated as V3 relationship change or forgetting → reject.
22. No actor-safe relationship input for requested relationship assertion → `MISSING_ACTOR_SAFE_RELATIONSHIP_INPUT`; no objective/transcript fallback.
23. Turn contains no relationship-specific material → `VALID_EMPTY_RELATIONSHIP_EXPRESSION`; no filler relationship claim required.
24. Historical V3 `Magnet.intensity=50` is used as current V2 closeness/trust → reject.
25. Generic CAN-016 salience, CAN-017 register, CAN-021 avoidance or active CAN-018 move vocabulary is re-owned as CAN-019 semantics → reject jurisdiction collapse.
26. Two compatible actor views are silently merged into an “objective reciprocal relationship” record → reject; agreement does not transfer ownership or create synthesis authority.
27. Transcript summary labels the relationship “close” after compaction → no relationship authority; preserve summary provenance only.
28. Rendered causal-mode candidate is rejected by V3 but retained in transcript → cannot update relationship posture/truth merely by retention.

## 17. GOVERNING_SPIRIT_CHECK

**Status:** `APPLIED_AS_TIE_BREAK_ONLY`.

Hard authority uniquely fixes V3 ownership of relationship history/memory, ADP-017 as actor-access ceiling, noncausal V2 presentation, preservation of asymmetry/contradiction, and rejection of legacy numeric/default authority.

The remaining lawful ambiguity was how much of the recovered open-ended `relational_posture` concept to freeze canonically:

1. freeze historical/example posture labels, weights and drift as a V2 relationship-state taxonomy; or
2. preserve only a sparse source-bound session posture container, with zero concrete labels/weights and no automatic drift, so future relationship-specific meaning remains owned by exact source authority.

Chosen: **2**.

Tie-break principles: dynamic relationships as generated histories rather than downstream traits; contradiction and asymmetric perspective without scalar collapse; actor opacity; lawful absence; minimum sufficient machinery; and the rule that downstream vividness may never exceed upstream authority.

`new_semantics_created_by_spirit = false`.

## 18. CONSUMER_RELEASE_SUFFICIENCY

**Status:** `SUFFICIENT_FOR_CAN_019_JURISDICTION__CLOSES_NAMED_V2_P6_AUTHORITY_SET_IF_ACCEPTED__NO_PRODUCTION_RELEASE`.

RA-R00 names the direct V2-P6 semantic blockers as `MUST-016`, `MUST-017`, `CAN-019`, and `MUST-024`. The other three are already accepted. Therefore, if Vozhd accepts this result, CAN-019 closes the remaining named **semantic-authority** blocker for V2-P6.

This does not release V2-P6 production implementation, does not guarantee nonempty relationship data, and does not bypass separately scheduled V3 relationship/household/genealogy generation authority or any global packet/EXT/release gates. Where V3 supplies no lawful actor-safe relationship material, CAN-019 remains valid-empty or missing as appropriate.

## 19. Final token

`CAN_019_V2_RELATIONSHIP_EXPRESSION_CANONICALIZATION = PASS`
