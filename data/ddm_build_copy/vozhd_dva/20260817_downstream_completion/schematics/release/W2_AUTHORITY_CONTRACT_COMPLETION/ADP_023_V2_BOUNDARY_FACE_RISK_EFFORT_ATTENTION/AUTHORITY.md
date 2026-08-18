# ADP-023 — V2 Boundary, Face-Risk, Effort & Attention Authority

**Authority ID:** `ADP-023`  
**RA-R00 authority:** `MUST-023`  
**Canonical machine authority:** `V2_BOUNDARY_FACE_RISK_EFFORT_ATTENTION_RULE`  
**Version:** `1.0.0`  
**Owner:** V2 expression-planning / presentation-constraint boundary  
**Repository:** `maidiu/rawlsing`  
**Assigned branch:** `agent/vozhd-dva-w2-adp-023-v2-boundary-effort`  
**Exact base SHA:** `fe52ca60ed00650b0a7b5bf77bab8ac40d53f4d8`  
**Mode:** bounded authority creation only; no production code; no V2 implementation  
**Whole-machine architecture:** `CLOSED`  
**W0:** `CLOSED`  
**W1:** `CLOSED__18_OF_18_ACCEPTED`  
**Verdict:** `PASS`

## 1. Holding

ADP-023 binds only **turn/situation-scoped, surface-only** constraints governing boundary, face-risk, effort, attention, expression capacity, and related lawful social-energy presentation constraints. It does not create a second causal psyche and does not infer hidden internal state because a renderer would benefit from a plausible human reaction.

Binding noncollapse:

```text
V3_ORGANISMIC_VITALITY
!= V2_SESSION_ENERGETIC_FIELD
!= V2_TURN_EXPRESSION_CAPACITY

V2_SESSION_ENERGETIC_FIELD
!= ACTOR_PERSONALITY
!= ACTOR_CAUSAL_PSYCHOLOGY

V2_BOUNDARY_DECISION
!= PERSISTENT_V3_BOUNDARY_DEVELOPMENT

V2_RELATIONSHIP_EXPRESSION
!= BOUNDARY_TRUTH

V2_ATTENTION_CONSTRAINT
!= V3_MEMORY_ACCESSIBILITY

V2_EFFORT_CONSTRAINT
!= V3_MEMORY_ACCESSIBILITY

FIRST_PERSON_PERMISSION
!= WILLINGNESS_TO_DISCLOSE
!= RESPONSE_OPERATION

RENDERED_REFUSAL_OR_EXIT
!= CAUSAL_OCCURRENCE
```

ADP-023 is monotone-narrowing. It can restrict presentation over already lawful material. It cannot increase actor access, create memory/belief/relationship/attractor state, mutate organismic state, infer persistent boundary development, or turn presentation/session behavior into generated biography.

`VALID_EMPTY_NO_ADP023_CONSTRAINT` is a lawful successful result.

## 2. Required historical archive verification

The required archive was directly hashed before reliance:

- archive: `Rawlsing_code_bundle_staging.zip`
- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- directly computed SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- verdict: `EXACT_MATCH`
- ZIP entries: `13,138`
- recovered V2/V3/server status: continuity / authority-recovery / negative-boundary evidence only
- historical V5/DDM authority over current V550+: **ZERO**

Focused historical verification from the exact archive:

```text
python -m pytest -q \
  tests/test_chat_integrity.py \
  v3/tests/test_v5_surface_psyche_profile.py \
  v3/tests/test_v5_persona_sheet_surface_psyche.py \
  v3/tests/test_v5_voice_packet_surface_allowlist.py \
  v3/tests/test_v5_render_surface_psyche.py \
  v3/tests/test_v5_v2_chat_prompt_no_raw_v5_leaks.py

23 passed
```

Passing legacy tests proves useful surface/prompt-integrity continuity. It does not promote historical scores, defaults, thresholds, keyword triggers, or persistent-state shortcuts.

## 3. Governing law and accepted surfaces consumed

Read at the exact base: W2 common law and W2-05; `CURRENT_STATE.md`; `RAWLSING_GOVERNING_SPIRIT.md`; `TERMINAL_DEMAND_ENVELOPE.md`; `ARCHITECTURE_PASS_LAW.md`; whole-machine closure; implementation-release synthesis; W0 closure; W1 closure; V2 completion ruling; accepted TD-R06; RA-R00; and the accepted authorities below. No W2 sibling result was consumed.

### ADP-017

ADP-017 is the immutable first-person semantic ceiling. ADP-023 may consume exact actor-safe claim/component permissions and their scope/provenance. It may never reconstruct partial access, promote inaccessible material, turn system truth into first-person truth, or use effort/attention as a route around memory/accessibility law.

### CAN-009

CAN-009 organismic/material/vitality state remains V3 causal state and measurement-contract-parametric. Its binding invariant controls this seam:

> Low vitality does not prove withdrawal, collapse, refusal, despair, pathology, or any response operation.

A CAN-009 record affects ADP-023 only when an exact separately governed source contract explicitly exports a compatible presentation-capacity constraint semantic. Raw value comparison, direction labels such as `DEPLETION_OR_DECREASE`, legacy thresholds, or the word `depleted` have no activation force.

### CAN-018

Consumed only as the accepted response-operation membrane: ordinary base operation `ENGAGE_SELECTIVE`, versioned special-operation registration, valid-empty/deferred/denied/integrity behavior, deterministic semantic replay, and rendering != causal occurrence. ADP-023 registers exactly two special operations in §11.

### CAN-019

Consumed only through exact actor-safe relationship-expression constraint refs and perspective bindings. CAN-019 relationship material does not become objective or reciprocal relationship truth here. Recovered `topics_to_avoid`, `sticky_triggers`, trust/intimacy scores, rendered tone, and session posture have no ADP-023 activation force unless an accepted source already emits a compatible exact constraint semantic.

### CAN-021

Consumed only through noncausal session/presentation provenance and exact source-owned presentation-signal refs. Session tension is not threat; intimacy is not relationship truth; curiosity is not high effort; boredom is not refusal; demand is not obligation; avoidance continuity is not boundary truth; `last_persona_effort` is not actor effort authority. No CAN-021 number or mere signal presence self-executes into ADP-023 meaning.

### ADP-026

Consumed only through exact source-bound, subject-bound, time-bound current-situation statements. Relevant fields can include current privacy, interruption, activity, availability constraint, channel/mode context, and client context. Subject jurisdiction is preserved: a CALLER/SESSION/APPLICATION fact is never rebound into a GENERATED_ACTOR fact. Free text is not parsed into safety, face-risk, or boundary semantics.

## 4. Recovered mechanism dispositions

| Recovered source/mechanism | Disposition | Terminal holding |
|---|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `PRESERVE_INTENT_ADAPT_SEMANTICS` | Selective attention, bounded effort, face-risk and boundary are valid turn-level concerns; illustrative scales/formulas are not law. |
| `v2/conversation_engine.py` | `ADAPT_MEMBRANE_REMOVE_HEURISTICS` | Preserve turn appraisal/constraint/response seam; reject numeric thresholds, keyword boundary triggers and political-keyword effort overrides. |
| `v2/life_simulation_schema.py::AttentionBudget` | `REPLACE_NUMERIC_ONTOLOGY` | Replace shared 0..100 state with sparse typed constraints. |
| `v2/LIFE_SIMULATION_LAYER.md` | `COMPATIBILITY_ONLY_FOR_FORMULAS` | Independent life/current-state synthesis is not ADP-023 authority. |
| recovered face-management/boundary/effort design prose | `DESIGN_CONTINUITY_ONLY` | Conceptual continuity only; low/med/high bands and example moves are nonauthority. |
| `v2/run_conversation_chat.py` / `server/chat/turn.py` hard-coded `persona_effort="medium"` | `REMOVE_REJECT` | No default effort. |
| session EnergeticField thresholds/decay | `REMOVE_REJECT_AS_ADP023_AUTHORITY` | CAN-021 preserves session continuity without these semantics. |
| dismissive phrase list -> boundary | `REMOVE_REJECT` | Keyword/phrase match cannot create boundary. |
| political/structural keywords -> high effort / longer reply | `REMOVE_REJECT` | Topic identity cannot create effort/capacity. |
| `deflect`, `brief_or_deflect`, `pivot`, `silence`, `exit` recovered strings | `COMPATIBILITY_ONLY` | CAN-018 registry governs; ADP-023 registers only §11 operations. |
| face-risk `low/med/high` | `COMPATIBILITY_ONLY` | No canonical band taxonomy. |
| `Effort = f(energy,time,user_effort,privacy)` | `PRESERVE_COMPOSITION_INTENT_ONLY` | Inputs may constrain presentation only through exact typed source semantics; no ungoverned formula. |
| V3 historical attention/capture formulas | `OUT_OF_JURISDICTION_COMPATIBILITY_ONLY` | Causal V3 lane; not V2 turn attention authority. |
| V3 historical solidarity-boundary state | `OUT_OF_JURISDICTION_COMPATIBILITY_ONLY` | Persistent V3 boundary development is not ADP-023. |
| actor-surface/no-raw-state tests | `PRESERVE_BOUNDARY_INTENT` | Useful no-leak evidence only. |

Explicitly rejected historical numerics/defaults include AttentionBudget `50/50/50`, shared `[0,100]` clamp, arithmetic mean of attention/effort/social energy, `<25/<50/<75` bands, sentence caps `2/4/8/12`, default `medium`/`moderate`, EnergeticField `.5/.6/.75` thresholds, `DECAY=.85`, and political-keyword 6–8 sentence overrides.

## 5. Jurisdiction and consumers

ADP-023 owns only:

1. `V2PresentationConstraintInput` validation;
2. sparse typed boundary, face-risk, attention, effort, expression-capacity, and social-energy presentation constraints;
3. deterministic composition and precedence;
4. the two CAN-018 special-operation registrations in §11;
5. valid-empty/missing/deferred/denied/integrity behavior;
6. exact noncausal provenance/replay/cache identity.

It does not own V3 embodied state, V3 persistent boundary/orientation development, memory/accessibility, knowledge/belief, session EnergeticField, relationship truth, generic salience, generic register, uncertainty disclosure, rendered wording/model randomness, transcript retention, structural interpretation, personality/type, or causal interaction admission.

Primary consumers: `V2-P4` and `V2-P5`.

## 6. Canonical input and evidence contract

A conforming semantic input is:

```text
V2PresentationConstraintInput {
  session_id,
  turn_id,
  actor_id,
  actor_access_envelope_ref,
  actor_access_envelope_hash,
  turn_artifact_ref,
  turn_artifact_hash,
  lawful_expression_target_refs[],
  can009_embodied_state_refs[],
  can019_relationship_constraint_refs[],
  can021_session_field_refs[],
  adp026_current_situation_statement_refs[],
  source_authority_manifest[],
  input_state_hash,
  integrity_state
}
```

Raw turn text is not a semantic boundary/effort source. Keywords, sentiment, toxicity labels, LLM classifications, and free-text similarity have zero activation force absent a separately accepted typed source authority.

Every positive constraint normalizes to:

```text
V2PresentationConstraintEvidence {
  evidence_id,
  source_authority_id,
  source_authority_version,
  source_authority_hash,
  source_record_ref,
  source_record_hash,
  source_subject_binding,
  source_epistemic_or_disposition_state,
  semantic_effective_scope,
  constraint_domain,
  constraint_semantic,
  target_scope,
  target_refs[],
  adapter_id,
  adapter_version,
  adapter_hash,
  evidence_hash,
  integrity_state
}
```

No consumer may synthesize `constraint_semantic` from prose, numeric magnitude, topic identity, or model judgment.

## 7. Canonical constraint states

ADP-023 v1 recognizes exactly six orthogonal **presentation-only domains**:

`BOUNDARY`, `FACE_RISK`, `ATTENTION`, `EFFORT`, `EXPRESSION_CAPACITY`, `SOCIAL_ENERGY_PRESENTATION`.

They are not actor trait dimensions.

### Boundary

```text
VALID_EMPTY_NO_SPECIAL_BOUNDARY_CONSTRAINT
TARGET_LIMIT_REQUIRED
TARGET_WITHHOLD_REQUIRED
TURN_EXIT_OR_PAUSE_REQUIRED
BOUNDARY_UNKNOWN_OR_DEFERRED
```

Valid-empty means no special boundary restriction was established for this decision; it does not mean the actor has no boundaries. Target limits/withholding affect only exact already-lawful targets. Turn exit/pause blocks ordinary continuation for this presentation decision only and does not create a persistent actor state.

### Face-risk

```text
VALID_EMPTY_NO_FACE_RISK_CONSTRAINT_ESTABLISHED
FACE_RISK_CONSTRAINT_ACTIVE
FACE_RISK_UNKNOWN_OR_DEFERRED
```

Face-risk is a turn-local **social-exposure/disclosure constraint relation**, not shame, fear, sensitivity, personality, or relationship truth. There is no low/medium/high scale.

Positive activation requires either (a) one exact accepted source already declaring a target-scoped current face/exposure restriction, or (b) both an exact current privacy/audibility/visibility exposure condition from ADP-026 and an exact target-specific disclosure/relationship-expression constraint from an accepted source. Privacy alone, topic identity alone, or relationship constraint alone is insufficient.

### Attention

```text
VALID_EMPTY_NO_ADDITIONAL_ATTENTION_CONSTRAINT
ATTENTION_SELECTIVITY_REQUIRED
ATTENTION_ORDINARY_ENGAGEMENT_UNAVAILABLE
ATTENTION_UNKNOWN_OR_DEFERRED
```

These constrain expression allocation, not cognition, salience, memory, consciousness, or diagnosis. Selectivity means downstream cannot require complete coverage; CAN-016 remains salience owner. No count, percentage, token budget, or numeric attention level is implied.

### Effort

```text
VALID_EMPTY_NO_ADDITIONAL_EFFORT_CONSTRAINT
EFFORT_SCOPE_REDUCTION_REQUIRED
EFFORT_ORDINARY_ENGAGEMENT_UNAVAILABLE
EFFORT_UNKNOWN_OR_DEFERRED
```

These are current presentation constraints only. Scope reduction may reduce completeness/elaboration without a canonical length or band. It does not imply apathy, motivation, personality, fatigue diagnosis, refusal, relationship stance, or memory loss.

### Social-energy presentation

```text
VALID_EMPTY_NO_SOCIAL_ENERGY_CONSTRAINT
SOCIAL_ENERGY_SCOPE_REDUCTION_REQUIRED
SOCIAL_ENERGY_ORDINARY_ENGAGEMENT_UNAVAILABLE
SOCIAL_ENERGY_UNKNOWN_OR_DEFERRED
```

No scalar, baseline, band, or persistence exists. CAN-021 EnergeticField and CAN-009 vitality do not automatically produce this domain; an exact compatible source adapter is required.

### Expression-capacity summary

```text
NO_ADDITIONAL_ADP023_CONSTRAINT
SELECTIVE_OR_REDUCED_ENGAGEMENT
BOUNDARY_LIMITED_ENGAGEMENT
NO_ORDINARY_ENGAGEMENT
EXPRESSION_CAPACITY_UNKNOWN_OR_DEFERRED
```

This is only a summary of the current noncausal V2 presentation decision. It is not V3 actor state and cannot be reused as causal evidence.

## 8. Source-adapter law

### ADP-026 adapter

All source identity, subject binding, effective time, disposition, and transform provenance must verify. The v1 eligibility map is:

| ADP-026 field | Potential ADP-023 use |
|---|---|
| `situation.current_privacy` | face-risk exposure leg; boundary only with independent target-specific constraint |
| `situation.current_interruption` | attention/effort/continuation only if exact machine-readable value semantics specify the constraint |
| `situation.current_activity` | attention/effort only with exact semantic mapping |
| `situation.current_availability_constraint` | attention/effort/continuation only with exact semantic mapping |
| `interaction.channel` | face-risk/expression context only where another rule establishes relevance |
| `interaction.mode_context` | presentation scope only |
| `presentation.client_context` | application/render capacity only |

No free-text parser is authorized. Wrong-subject or stale statements cannot activate a constraint.

### CAN-019 adapter

An exact relationship-expression constraint can produce a target limit only when its source-owned semantics explicitly authorize a presentational disclosure/interaction constraint. Posture, tone, trust/intimacy, transcript repetition, application relationship mode, or one actor's perceived relationship view is never sufficient by itself.

### CAN-021 adapter

Raw session signal presence, signal magnitude, topic repetition, avoidance continuity, or `last_persona_effort` is insufficient. Only an exact source-owned presentation constraint semantic may cross this seam.

### CAN-009 adapter

A CAN-009 record may support ADP-023 only through an exact quantity/measurement/operation contract or separately governed adapter explicitly exporting a V2 presentation-capacity constraint. Raw value comparison is forbidden:

```text
LOW_OR_DEPLETED_VITALITY -x-> WITHDRAW
LOW_OR_DEPLETED_VITALITY -x-> REFUSE
LOW_OR_DEPLETED_VITALITY -x-> EXIT
LOW_OR_DEPLETED_VITALITY -x-> LOW_EFFORT
LOW_OR_DEPLETED_VITALITY -x-> LOW_ATTENTION
```

High vitality likewise does not authorize high effort, disclosure, assertiveness, or wider access.

## 9. Canonical decision and actor-access ceiling

A conforming output is:

```text
V2BoundaryFaceRiskEffortAttentionDecision {
  decision_id,
  authority_id = ADP-023,
  authority_name = V2_BOUNDARY_FACE_RISK_EFFORT_ATTENTION_RULE,
  authority_version = 1.0.0,
  session_id,
  turn_id,
  actor_id,
  actor_access_envelope_ref,
  actor_access_envelope_hash,
  turn_artifact_ref,
  turn_artifact_hash,
  admitted_constraint_evidence_refs[],
  boundary_state,
  face_risk_state,
  attention_state,
  effort_state,
  social_energy_state,
  expression_capacity_state,
  limited_target_refs[],
  withheld_target_refs[],
  unaffected_target_refs[],
  required_special_operation_id | null,
  missing_or_deferred_records[],
  denied_records[],
  source_authority_manifest_hash,
  decision_rule_id,
  decision_rule_version,
  decision_rule_hash,
  decision_hash,
  integrity_state
}
```

It is immutable and noncausal. No numeric state is canonical in v1.

For every target:

```text
ADP023_EXPRESSIBLE_COMPONENTS
⊆ ADP017_CURRENT_FIRST_PERSON_PERMITTED_COMPONENTS
```

ADP-023 may omit, withhold, restrict to an already-permitted component subset, require reduced engagement, or require a boundary/exit presentation operation. It may not make inaccessible material accessible, upgrade epistemic stance/certainty, dereference analyst-only provenance, use effort/attention to recall memory, or reveal hidden content through the wording of a refusal.

If identifying a restricted target would itself reveal inaccessible material, the response operation must remain semantically opaque about that target.

## 10. Precedence and tie law

Precedence is categorical, monotone, and target-scoped; there is no score or average.

1. **Integrity gate.** Broken identity/hash, stale envelope, subject mismatch, malformed adapter, or rule mismatch yields integrity failure/typed deferral.
2. **ADP-017 ceiling.** Inaccessible/forbidden material is removed before composition and cannot be restored.
3. **Source scope/time.** Expired, stale, wrong-subject, or non-presentation sources cannot activate constraints.
4. **Whole-turn continuation.** `TURN_EXIT_OR_PAUSE_REQUIRED` outranks all ordinary target engagement for this decision.
5. **Same-target boundary.** `TARGET_WITHHOLD_REQUIRED` outranks `TARGET_LIMIT_REQUIRED` for the same target.
6. **Attention/effort/social-energy narrowing.** Compatible constraints accumulate orthogonally; they narrow coverage/elaboration and cannot defeat boundary/access restrictions.
7. **Face-risk.** It has effect only through its exact activation/basis; unknown face-risk never defaults to a band and never self-triggers a move.
8. **CAN-018 ordinary path.** If no special operation is required, lawful targets remain, and constraints permit engagement, CAN-018 may select `ENGAGE_SELECTIVE`.
9. **Valid-empty.** If no lawful target and no special operation is required, CAN-018 may return its valid-empty outcome.

Compatible constraints coexist. If non-equivalent exact constraints are mutually incompatible and no accepted precedence orders them, return `DEFERRED_AMBIGUOUS_CONSTRAINT_COMPOSITION`. List order, recency alone, numeric rank/average, keyword, LLM judgment, RNG, and narrative plausibility are forbidden tie-breakers.

ADP-023 never compels positive disclosure. High capacity never outranks access, boundary, uncertainty, or relationship-expression restrictions.

## 11. CAN-018 special-operation registrations

ADP-023 registers exactly two v1 special operations.

### `ADP023_BOUNDARY_LIMIT@1.0.0`

**Activation rule:** `ADP023_BOUNDARY_LIMIT_ACTIVATION@1.0.0`.

Semantic scope: present a turn-level refusal, disclosure limit, or non-engagement with one or more exact currently restricted targets while unrelated already-lawful targets may remain available for ordinary engagement. This creates no persistent boundary state and need not expose the reason for the limit.

Activation requires a verified ADP-023 decision, `TARGET_LIMIT_REQUIRED` or `TARGET_WITHHOLD_REQUIRED`, an exact affected target (or opaque target token where naming it would violate access), no active whole-turn exit/pause, and continued ADP-017 compliance.

Precedence: it outranks `ENGAGE_SELECTIVE` for restricted targets, may coexist with ordinary engagement for unaffected targets, and is outranked by `ADP023_EXIT_OR_PAUSE`.

It does not imply `DEFLECT`, `PIVOT`, `SILENCE`, shame, fear, hostility, trauma, relationship deterioration, or causal refusal. Keywords cannot activate it.

### `ADP023_EXIT_OR_PAUSE@1.0.0`

**Activation rule:** `ADP023_EXIT_OR_PAUSE_ACTIVATION@1.0.0`.

Semantic scope: cease or pause ordinary conversational engagement for this presentation decision because an exact whole-turn continuation constraint is active.

Activation requires verified `TURN_EXIT_OR_PAUSE_REQUIRED` plus exact source/adapter provenance. It cannot arise from keywords, low vitality, session boredom/tension, demographic context, or LLM judgment.

Precedence:

```text
ADP023_EXIT_OR_PAUSE
> ADP023_BOUNDARY_LIMIT
> CAN018_ENGAGE_SELECTIVE
```

Rendered exit/pause remains noncausal. In `PRESENTATION_NONCAUSAL` it is presentation/session behavior only. In `IN_WORLD_CAUSAL`, the exact artifact remains `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION` until V3 admits it; rerendering creates a new artifact/hash requiring new admission.

Explicit nonregistrations remain compatibility-only: `DEFLECT`, `PIVOT`, `REDIRECT`, `CHANGE_SUBJECT`, `DROP_THREAD`, `DELAY`, `SILENCE`, `BOUNDARY_STATEMENT`, `ASK_SAFER_QUESTION`, `brief_or_deflect`, `go quiet`, and historical compounds/near-synonyms.

## 12. Vitality / session / relationship noncollapse proof

**CAN-009:** vitality is V3 causal embodied state. Depleted vitality without an exact presentation adapter produces no ADP-023 effort/boundary result. High vitality cannot widen access/disclosure. Unknown vitality never becomes medium effort. Low vitality cannot erase actor-accessible content or force refusal/exit.

**CAN-021:** session EnergeticField is noncausal session continuity. Curiosity/engagement does not widen ADP-017 access; boredom does not prove low effort; tension does not prove face-risk; avoidance does not prove a boundary; persistence does not create personality.

**CAN-019:** relationship expression is perspective-bound presentation. Warm/hostile rendered tone does not prove boundary or face-risk; one actor's relationship view supplies no reciprocal truth; compatibility `topics_to_avoid` strings do not activate ADP-023; only an exact accepted relationship constraint may narrow its own target/scope.

**ADP-016/017 boundary:** attention and effort may reduce what V2 addresses now. They cannot create forgetting/recall, make memory accessible/inaccessible, or alter knowledge/belief.

## 13. Numeric/default/formula disposition

ADP-023 v1 creates **no shared quantitative scale**. Forbidden as terminal authority: 0..100 attention/effort/social energy; 0..1 face-risk/session energy; default `50`, `medium`, `moderate`, normal-person baseline, implicit neutral zero; arithmetic means; clamping/saturation; threshold bands; hard sentence/token caps; hidden weights; keyword bonuses; history length/transcript frequency proxies.

A future quantitative input may be consumed only if its owner supplies exact quantity semantics, unit/domain, lawful comparison/threshold semantics, operation and versioned provenance. ADP-023 never infers those from storage shape.

## 14. Valid-empty / missing / deferred / integrity behavior

Canonical decision statuses:

```text
CONSTRAINT_DECISION_APPLIED
VALID_EMPTY_NO_ADP023_CONSTRAINT
DEFERRED_MISSING_REQUIRED_SOURCE
DEFERRED_MISSING_SOURCE_AUTHORITY
DEFERRED_UNMAPPED_SOURCE_SEMANTICS
DEFERRED_AMBIGUOUS_CONSTRAINT_COMPOSITION
DENIED_ACTOR_ACCESS_VIOLATION
DENIED_FORBIDDEN_SOURCE
DENIED_KEYWORD_OR_LLM_SEMANTIC_PATH
STALE_OR_EXPIRED_SOURCE
INTEGRITY_FAILURE
```

Rules:

- complete applicable inputs yielding no constraint -> `VALID_EMPTY_NO_ADP023_CONSTRAINT`;
- missing capacity is not medium/50/full;
- missing face-risk authority is not low risk;
- missing boundary authority is not no boundary;
- unknown session signal is not neutral actor psychology;
- missing CAN-009 export semantics produces no vitality-derived constraint;
- stale ADP-026 input is not carried forward;
- known-to-exist but unavailable evidence is not collapsed to valid-empty;
- integrity failure never falls back to ordinary engagement.

Optional absent sources do not block the whole decision. If an active rule requires a missing source to interpret an asserted constraint, the result is typed deferral.

## 15. Replay, provenance and cache law

ADP-023 semantic decisions are deterministic; no semantic RNG is authorized. Identity binds authority/version/hash; actor/session/turn and artifact hash; current ADP-017 envelope; lawful target-set hash; every admitted source ref/hash/authority version/subject/effective scope; adapter IDs/versions/hashes; registry and precedence versions/hashes; special-operation registry version/hash; result state and target partitions.

Forbidden semantic replay inputs: hidden wall clock, mutable `latest`, filesystem/dict/list order, transcript rescanning, keyword frequency, LLM/model output, V2 render RNG, V3 causal RNG, unrecorded external lookup, prior rendered wording.

Expiry/correction/subject change/source hash change makes a cached decision stale. Identical canonical inputs reproduce identical decision/status/hash. ADP-025 renderer variation may change wording after the decision but cannot change its semantics.

## 16. Hostile fixtures

1. Missing capacity authority -> typed missing/deferred if required; never 50/medium/full.
2. Depleted CAN-009 vitality, no presentation adapter -> no withdrawal/refusal/exit/low-effort inference.
3. High vitality -> no wider access/disclosure/high-effort requirement.
4. High CAN-021 engagement/curiosity -> no access widening or automatic high effort.
5. High CAN-021 boredom -> no automatic low effort/refusal.
6. High CAN-021 tension -> no automatic boundary/face-risk.
7. Session avoidance continuity -> not boundary truth.
8. Boundary-like/dismissive keyword -> no activation.
9. Political/structural keyword -> no effort/length/move override.
10. Raw `EXIT` / `BOUNDARY_STATEMENT` token -> no activation.
11. Current privacy exposure without target-specific disclosure constraint -> no face-risk relation.
12. Target disclosure constraint without current exposure -> no inferred current face-risk.
13. Exact exposure + exact target disclosure constraint -> `FACE_RISK_CONSTRAINT_ACTIVE`, exact scope only.
14. Exact target limit -> `ADP023_BOUNDARY_LIMIT` eligible under CAN-018 contract.
15. Exact whole-turn continuation constraint -> `ADP023_EXIT_OR_PAUSE`, outranking ordinary engagement.
16. Target limit + turn exit -> exit precedence; preserve both source receipts.
17. One actor's relationship view -> no reciprocal truth and no automatic boundary.
18. Prior hostile/warm render -> no boundary or relationship truth.
19. Missing legacy AttentionBudget -> no synthesized 50/50/50.
20. Legacy 25/50/75 threshold crossing -> no semantic effect.
21. Legacy `.75` session threshold crossing -> no semantic effect.
22. Attention selectivity -> may narrow coverage; cannot alter memory accessibility.
23. Effort reduction -> may reduce elaboration; cannot create apathy/personality.
24. Lawful actor targets + no ADP-023 constraint -> `VALID_EMPTY_NO_ADP023_CONSTRAINT`; ordinary CAN-018 engagement remains lawful.
25. Zero lawful targets + no special op -> CAN-018 valid-empty; no synthetic silence.
26. Inaccessible target is boundary-limited -> operation may not reveal target/reason.
27. Partially accessible target -> no hidden-component reconstruction.
28. Caller says caller is busy -> preserve CALLER subject; do not rebind to actor.
29. Caller assertion about actor interruption -> presentation source only; no generated-history promotion.
30. Expired current-situation statement -> stale/unknown, no inferred persistence.
31. Free-text source value with no adapter -> `DEFERRED_UNMAPPED_SOURCE_SEMANTICS`, no LLM interpretation.
32. LLM labels topic unsafe/embarrassing -> deny semantic path.
33. Demography/class/religion offered as boundary/face-risk basis -> reject.
34. Session field described as personality -> reject noncollapse violation.
35. Rendered refusal persisted across turns -> no persistent V3 boundary state.
36. Rendered exit in noncausal mode -> no causal occurrence.
37. Causal-mode rendered exit before V3 admission -> remains noncausal candidate.
38. Rerender after admission -> new artifact/hash, new admission required.
39. Two compatible constraints -> preserve both; no scalar averaging.
40. Incompatible constraints with no precedence -> `DEFERRED_AMBIGUOUS_CONSTRAINT_COMPOSITION`.
41. Exact replay inputs -> identical decision/status/hash.
42. Source hash/effective scope changes -> stale cache, recompute.
43. No face-risk evidence -> valid-empty face-risk, not safe/low-risk assertion.
44. Social-energy source missing -> valid-empty/unknown as applicable; no medium baseline.
45. Exact social-energy presentation constraint -> only declared scope/effect; no personality persistence.
46. Legacy relationship `topics_to_avoid` string -> no activation.
47. V3 historical solidarity-boundary state supplied -> outside turn-boundary jurisdiction.
48. ADP-023 decision fed back as V3 state without governing admission/effect rule -> reject causal promotion.

## 17. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

Recovered V2 establishes that variable effort, selective attention, face management and boundaries matter to expression, but after its unsupported formulas are removed there remains a genuine lawful choice: rebuild them as generic scalar/current-psyche levels, or bind them as sparse provenance-preserving presentation constraints that may be empty, coexist, conflict and narrow expression without becoming persistent psychology.

The second design is chosen. Decisive principles: determination is not transparency; actor opacity; mediation instead of structure/demography -> psyche; contradiction without scalar collapse; ordinary vitality without making depletion destiny; lawful absence rather than plausible defaults; no downstream vividness beyond authority; minimum sufficient machinery. The Governing Spirit supplies no boundary fact, face-risk fact, effort/attention state, social-energy level, trigger, relationship truth, actor motive, or numeric threshold.

## 18. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__MUST_023_SEMANTIC_AUTHORITY_CLOSED_AFTER_VOZHD_ACCEPTANCE`.

After acceptance:

- `V2-P4`: its named semantic blockers `CAN-021`, `ADP-024`, `ADP-026`, and `MUST-023` are closed. This does not release production implementation; `IMP-009`, packet scheduling/application contracts and global gates remain binding.
- `V2-P5`: ADP-023 closes the MUST-023 contribution. Accepted `CAN-016`, `CAN-017`, and `CAN-018` are already available. `MUST-022 / ADP-022` remains a separate W2 sibling dependency and is neither consumed nor pre-adjudicated here. Packet/release gates remain binding.

The two special-operation registrations are sufficient for the boundary/exit semantics created by ADP-023. No additional recovered move vocabulary is required for MUST-023 closure.

## 19. Final token

`ADP_023_V2_BOUNDARY_FACE_RISK_EFFORT_ATTENTION_AUTHORITY = PASS`
