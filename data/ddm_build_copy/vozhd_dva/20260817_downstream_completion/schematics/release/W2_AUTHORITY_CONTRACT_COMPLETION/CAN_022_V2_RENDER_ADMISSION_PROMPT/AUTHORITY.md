# CAN-022 — V2 Render Admission & Prompt Contract

**Assignment:** `W2-B02-04`  
**RA-R00 item:** `CAN-022`  
**Canonical authority:** `V2_RENDER_ADMISSION_PROMPT_CONTRACT@1.0.0`  
**Owner:** `V2_RENDER_ADMISSION_BOUNDARY`  
**Consumers:** `V2-P8`, `V2-P9`  
**Exact launch base:** `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`  
**Mode:** authority canonicalization only; no production code; no V2 implementation  
**Verdict:** `PASS`

## 1. Binding holding

CAN-022 canonicalizes one bounded membrane: the pre-render admission and prompt-compilation contract that turns an **already-authorized, final V2 semantic expression plan** into a renderer request while proving that no semantic authority enters the prompt beyond that plan.

```text
V3 GENERATED TRUTH
!= ACTOR_ACCESSIBLE_RENDER_ENVELOPE
!= V2 SEMANTIC EXPRESSION PLAN
!= V2 RENDER ADMISSION
!= COMPILED PROMPT
!= MODEL OUTPUT
!= VALIDATED RENDERED EXPRESSION
!= CAUSAL OCCURRENCE
```

The renderer is **WORDING ONLY**. It may vary surface realization inside an admitted semantic envelope. It may not create, select, strengthen, recover, or infer actor knowledge, biography, memory, relationship truth, response move, attractor, interaction mode, causal event, or causal effect.

A valid-empty semantic plan is complete lawful input. It yields `RENDER_ADMISSION_VALID_EMPTY`, no model invocation, and no fallback utterance.

## 2. Evidence and source verification

Required archive:

```text
Rawlsing_code_bundle_staging.zip
expected SHA256 = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
computed SHA256 = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
verdict = EXACT_MATCH
entries = 13,138
```

Recovered V2/V3/server material is continuity and authority-recovery evidence only. Historical V5/DDM has **zero current authority**.

Focused historical court:

```text
PYTHONPATH=. pytest -q \
  v3/tests/test_v5_v2_chat_prompt_no_raw_v5_leaks.py \
  v3/tests/test_v5_voice_packet_surface_allowlist.py \
  v3/tests/test_v5_render_surface_psyche.py \
  v3/tests/test_v5_persona_sheet_surface_psyche.py \
  v3/tests/test_persona_sheet_integrity.py \
  tests/test_chat_integrity.py

19 passed in 0.20s
```

Direct historical sources and SHA256s:

| Source | SHA256 | Disposition use |
|---|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7` | renderer-not-decider continuity |
| `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135` | prompt/render ordering; negative evidence for broad context injection |
| `v2/run_conversation_chat.py` | `b9276a4d7fc9dfdc83cc220528e4f16c1880d78419ed06430a5e9570a60efdc8` | model-call continuity; mutable model fallback rejected by ADP-025 |
| `v2/spec.py` | `f7ca16a7addf4dd1bd155a985586f926f1a4c31f127b829bcb8056c851d58296` | persona/life prompt carrier; defaults are negative evidence |
| `v2/PIPELINE_WIRING_AUDIT.md` | `fabbf700ec6e83aae4a59266a58833871f6205655f022311865eb62381dbebe4` | plan→prompt→render wiring continuity |
| `server/chat/turn.py` | `10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3` | post-build memory injection is forbidden |
| `server/session_db.py` | `0d9bf508aa748ce8eff3360a7c615ab0ed086f3a34c3190815cb0485fe234c12` | persistence continuity only |
| `server/session_state.py` | `9c9c3b0e2b3bff700af127e03805166102920019d6acd099ee8270fbe63bc15a` | prompt/request/raw-output artifact-writing continuity |
| `server/routes/chat.py` | `254c2d9497eb76654ddf648024090a3fd341927fd910a7ad23a63b256e90cbac` | application seam continuity |
| `v3/V3_UNDERLIES_V2_ARTICULATION.md` | `5a0f11276a830b959df72653016ca77848dbd81de4adb9fa641bd4244c4f4ced` | V3 causal / V2 articulation direction |
| `v3/io/persona_sheet.py` | `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e` | allowlist carrier pattern; persona sheet itself is not prompt authority |

Binding current authority read at the exact base includes the Batch-02 register/common law, `CURRENT_STATE`, `RAWLSING_GOVERNING_SPIRIT`, `TERMINAL_DEMAND_ENVELOPE`, `ARCHITECTURE_PASS_LAW`, whole-machine closure, implementation-release synthesis, W0 closure, W1 closure, W2 first-batch adjudication, V2 completion, RA-R00 `RESULT.md` / `RESULT.json`, ADP-017, ADP-025, and accepted V2 CAN-015..020 boundaries relevant to the final expression plan.

No same-cohort CAN-023, CAN-024, or CAN-025 result was consumed.

## 3. Recovered mechanism dispositions

| Recovered mechanism | Disposition | Terminal holding |
|---|---|---|
| renderer-not-decider direction | `PRESERVE` | model realizes wording only |
| analyze/plan/render separation | `PRESERVE_ADAPT` | semantic plan must be final before prompt admission |
| `build_reply_prompt` mechanism | `ADAPT` | deterministic compiler over admitted plan and allowlisted wording context |
| prompt/model/output audit artifacts | `PRESERVE_ADAPT` | immutable hashes, manifests and receipts required |
| surface allowlisting tests | `PRESERVE` | current contract becomes stricter and ADP-017-bound |
| anti-assistant/render hygiene | `COMPATIBILITY_ONLY` | only semantics-preserving non-personality constraints |
| full `persona_context` | `REMOVE_REJECT` | aggregate persona is not render authority |
| `REPLY_VOICE_SCHEMA_FALLBACK` / generic voice | `REMOVE_REJECT` | no personality/voice/tone fallback |
| city/class/history/culture grounding | `REMOVE_REJECT_AS_DIRECT_PROMPT_AUTHORITY` | structural/objective context cannot reconstruct actor voice or knowledge |
| invented microdetails/names/incidents | `REMOVE_REJECT` | no unsupported biography/event/room/action detail |
| raw backstory / anchored memories | `REMOVE_REJECT` | objective prose is not actor-accessible memory |
| server `SURFACED MEMORY` prompt append | `REMOVE_REJECT_AND_INTEGRITY_FAILURE` | post-admission semantic augmentation forbidden |
| server `CARRIED WEIGHT` fallback | `REMOVE_REJECT` | no wound/memory/avoidance filler |
| raw `surface_psyche` / hidden actor state | `REMOVE_REJECT_DIRECT_USE` | only exact final plan units may carry actor semantics |
| raw EnergeticField cues | `REMOVE_REJECT_DIRECT_USE` | only an already-final upstream plan constraint may survive by exact ref |
| hook confidence/refraction cues | `REMOVE_REJECT_DIRECT_USE` | diagnostics cannot become epistemic/render authority |
| active-stream internal tags | `REMOVE_REJECT_DIRECT_USE` | no hidden motive/personality authority |
| current user turn | `ADAPT_STIMULUS_ONLY` | may be visible for wording/relevance, never actor-truth authority |
| prior transcript/history direct context | `REMOVE_REJECT_DIRECT_USE` | only exact plan-admitted presentation context may survive |
| response/sentence/depth fallback defaults | `REMOVE_REJECT_AS_PROMPT_DEFAULT` | upstream semantic decisions remain authoritative |
| physical-action/room-detail prompt rules | `COMPATIBILITY_ONLY_IF_PLAN_AUTHORIZED` | cannot manufacture observable detail |
| NATIVE/TRANSLATION dual prompt | `DEFER_TO_CAN_023` | equivalence belongs CAN-023 |
| provider/model/env defaults | `OUT_OF_SCOPE_ADP_025` | never prompt-semantic authority |
| cleanup/parse transforms | `ADAPT_IF_VERSIONED_AND_SEMANTICS_PRESERVING` | byte-changing transforms are receipt-bound |

## 4. Jurisdiction

CAN-022 owns only:

- validation/admission of an already-final semantic expression plan into rendering;
- a transport-only `V2RenderIntakePlanEnvelope` schema;
- model-visible semantic vs stimulus-only vs audit-only prompt lanes;
- ADP-017 envelope/plan subset proof;
- authority/version/hash manifest verification;
- prompt-template admission and deterministic prompt compilation;
- prompt and prompt-package identity/hashing;
- CAN-022 admission and compilation receipts;
- post-render wording-only conformance/leakage validation;
- valid-empty, blocked, leakage and integrity states;
- prompt-admission replay/provenance.

CAN-022 does **not** own actor knowledge/memory/accessibility, salience, register, response/disclosure/boundary decisions, relationship/attractor expression semantics, provider/model/version/sampling/RNG/retry/rerender mechanics, translation equivalence, interaction mode, event packaging, V3 admission/effects, transcript retention, V558 interpretation, or biography/personality/voice facts.

ADP-017 remains the hard actor-access ceiling. ADP-025 remains sovereign over model/provider/version/sampling, `V2_RENDER_RNG`, retry/rerender identity, and render receipts.

## 5. Render-intake plan contract

```text
V2RenderIntakePlanEnvelope@1.0.0 {
  intake_plan_id,
  intake_plan_version,
  actor_id,
  turn_id,
  source_plan_id,
  source_plan_hash,
  source_plan_state,
  actor_access_envelope_id,
  actor_access_envelope_hash,
  actor_access_as_of_causal_time,
  renderable_unit_bindings[],
  source_semantic_decision_refs[],
  withheld_denied_refs[],
  authority_manifest_ref,
  authority_manifest_hash,
  plan_integrity_state,
  intake_plan_hash
}
```

This is a **transport-only proof envelope** over an already-authorized plan. CAN-022 may not complete, reinterpret, enrich, summarize, or repair its semantics.

Each `V2RenderSemanticUnitBinding@1.0.0` binds an exact source expression unit/hash, source semantic-decision refs, claim/nonclaim refs, permitted components, permission ref where applicable, already-selected response operation, exact register/relationship/attractor constraints where applicable, presentation-context refs, semantic-scope hash, and exact model-visible payload ref.

Missing render-unit bindings yield `RENDER_ADMISSION_BLOCKED_PLAN_RENDER_BINDING_INCOMPLETE`. Hidden state or provenance may not be searched to fill them.

## 6. Three prompt lanes

### 6.1 Model-visible authoritative semantic lane

Only exact payloads bound in admitted render semantic units may carry actor-semantic authority into the prompt.

### 6.2 Model-visible stimulus-only lane

The exact current user-turn artifact, or exact hashed spans, may be visible as `STIMULUS_ONLY_NONAUTHORITATIVE` so the renderer can word a coherent response. It grants **zero actor truth authority**. A user assertion cannot become an actor fact, belief, memory, biography, relationship truth, attractor, or response operation unless an admitted plan unit independently supplies that content.

Prior transcript/history is not model-visible by persistence alone. It may appear only through an exact presentation-context unit already admitted by the final plan.

### 6.3 Audit-only lane

The full actor-access envelope, authority manifest, opaque provenance, source-decision hashes not needed literally, V3/V558/V550+ refs, denied/withheld refs, session/cursor audit identity and ADP-025 model/RNG receipts are `AUDIT_ONLY_NEVER_MODEL_VISIBLE`.

**Provenance proves lineage; it is not a hidden semantic database for the renderer.** Opaque provenance is never dereferenced into prompt content.

## 7. Authority manifest

`V2PromptAuthorityManifest@1.0.0` contains:

```text
manifest_id/version,
actor_id, turn_id,
source_actor_envelope_id/hash,
source_plan_id/hash,
entries[],
manifest_hash,
integrity_state
```

Each entry binds source record/hash, authority ID/version/hash, source role, visibility class, permitted components, permission ref where applicable, semantic-scope hash and entry hash.

Visibility is exactly one of:

- `MODEL_VISIBLE_VALUE`
- `STIMULUS_ONLY_NONAUTHORITATIVE`
- `AUDIT_ONLY_REF`
- `OMITTED_DENIED`

An authority/provenance entry proves lineage only. `MODEL_VISIBLE_VALUE` still requires an admitted render-unit binding and current ADP-017 ceiling proof.

## 8. Prompt-template / compiler contract

`V2PromptTemplate@1.0.0` is composed only of registered nonsemantic renderer clauses plus allowlisted dynamic slots. Free unregistered actor-specific literal text is forbidden.

Canonical v1 clause semantics are:

- `RENDER_SUPPLIED_PLAN_ONLY` — realize only admitted semantic content;
- `PRESERVE_EPISTEMIC_AND_COMPONENT_SCOPE` — do not strengthen stance or widen components;
- `PRESERVE_CONTRADICTION_UNCERTAINTY_AND_OMISSION` — do not resolve contradiction, reduce uncertainty or restore withheld material;
- `NO_AUDIT_PROVENANCE_DEREFERENCE` — audit refs are not content;
- `NO_SEMANTIC_DECISION_SELECTION` — do not select/change move, register, relationship, attractor, disclosure or boundary semantics;
- `NO_INTERACTION_MODE_OR_CAUSAL_AUTHORITY` — do not choose/infer causal mode, event/effect or admission;
- `WORDING_VARIATION_ONLY` — vary only surface-equivalent realization;
- `OUTPUT_ONLY_ADMITTED_SURFACE_SHAPE` — do not emit hidden chain, analyst account or source manifest.

Allowed dynamic slots are only `ADMITTED_RENDER_SEMANTIC_UNIT`, `ADMITTED_PLAN_CONSTRAINT`, `ADMITTED_PRESENTATION_CONTEXT`, `CURRENT_TURN_STIMULUS_ONLY`, and `OUTPUT_SURFACE_SHAPE_INSTRUCTION`.

Prompt compilation is deterministic, RNG-free, network-free and LLM-free. A template containing personality, generic voice/tone, biography, hidden memory, demographic register, structural explanation, unselected operation alternatives, interaction-mode selection, or causal instruction is not admitted.

## 9. Request, prompt and receipt identity

### 9.1 Admission request

`V2RenderAdmissionRequest@1.0.0` binds actor/turn, intake-plan hash, actor-envelope hash, authority manifest, prompt template/compiler, requested renderer clauses, optional exact current-turn stimulus ref/hash, ADP-025 policy ref/hash, render-family anchor, rerender ordinal, request hash and integrity.

Provider/model/sampling/RNG are not semantic selectors. Interaction-mode and causal-event/effect fields are forbidden CAN-022 prompt semantics.

### 9.2 Admission receipt

`V2RenderAdmissionReceipt@1.0.0` records request, authority, actor/turn, plan/envelope/manifest/template refs, admitted semantic-unit refs, stimulus-only refs, audit-only refs, withheld/denied refs, status/reasons, receipt hash and integrity.

It deliberately contains **no descendant prompt/package hash**, preventing a circular hash graph.

Admission states:

- `RENDER_ADMISSION_ADMITTED`
- `RENDER_ADMISSION_VALID_EMPTY`
- `RENDER_ADMISSION_BLOCKED_PLAN_DEFERRED`
- `RENDER_ADMISSION_BLOCKED_UPSTREAM_DENIED`
- `RENDER_ADMISSION_BLOCKED_PLAN_AMBIGUOUS`
- `RENDER_ADMISSION_BLOCKED_REQUIRED_INPUT_UNKNOWN`
- `RENDER_ADMISSION_BLOCKED_MISSING_ACTOR_ENVELOPE`
- `RENDER_ADMISSION_BLOCKED_STALE_ACTOR_ENVELOPE`
- `RENDER_ADMISSION_BLOCKED_PLAN_NOT_FINAL`
- `RENDER_ADMISSION_BLOCKED_PLAN_RENDER_BINDING_INCOMPLETE`
- `RENDER_ADMISSION_BLOCKED_AUTHORITY_MANIFEST_INCOMPLETE`
- `RENDER_ADMISSION_BLOCKED_ACCESS_CEILING_VIOLATION`
- `RENDER_ADMISSION_BLOCKED_FORBIDDEN_SOURCE`
- `RENDER_ADMISSION_BLOCKED_HIDDEN_PROMPT_DEFAULT`
- `RENDER_ADMISSION_BLOCKED_PROMPT_TEMPLATE_UNGOVERNED`
- `RENDER_ADMISSION_BLOCKED_POST_HASH_MUTATION`
- `RENDER_ADMISSION_INTEGRITY_FAILURE`

### 9.3 Prompt bundle

`V2RendererPromptBundle@1.0.0` binds contract/template/compiler identities, admission receipt, source plan/envelope/manifest refs, exact ordered provider-visible messages, model-visible/stimulus segment manifests, audit-only manifest hash, prompt hash, prompt-package hash and integrity.

```text
prompt_hash = SHA256(
  "rawlsing:v2:compiled-prompt:v1\n" || JCS(ordered_provider_messages)
)

prompt_package_hash = SHA256(
  "rawlsing:v2:prompt-package:v1\n" || JCS(prompt_bundle_without_prompt_package_hash)
)
```

No semantic prompt augmentation is lawful after these hashes are bound. The recovered server-side `SURFACED MEMORY` append path therefore becomes a hard integrity failure.

### 9.4 Prompt compilation receipt

`V2PromptCompilationReceipt@1.0.0` binds the admission receipt, prompt bundle/hash, prompt-package hash, template/compiler hashes, state and integrity.

The identity chain is one-way:

```text
render-admission receipt
→ prompt bundle
→ prompt-compilation receipt
→ ADP-025 render request
```

Admission receipts never contain descendant prompt/package hashes.

## 10. ADP-017 ceiling proof

For every admitted render:

```text
model_visible_actor_semantic_components
  ⊆ source_plan_renderable_components
  ⊆ exact_current_ADP017_permitted_components

output_semantic_components
  ⊆ admitted_model_visible_semantic_components

output_epistemic_strength
  <= exact admitted epistemic permission

audit_only_refs ∩ model_visible_segments = ∅
```

There is therefore no lawful path for objective/system truth→actor claim, opaque provenance→actor content, partial→whole access, belief→knowledge/fact, uncertainty→certainty, nonknowledge→guess, one-sided relationship view→reciprocal truth, attractor evidence→type label, or current-user assertion→actor belief/fact absent an admitted plan unit.

## 11. Wording-only output validation

Model output is a **draft surface**. It does not become a valid `RenderedTurnArtifact` merely because a model returned text.

`V2RenderSurfaceValidationReceipt@1.0.0` must prove that rendered semantic content is no broader or stronger than admitted plan units. Renderer self-attestation or unconstrained LLM judgment is never sufficient semantic authority. If semantic conformance cannot be proven, return `RENDER_SURFACE_VALIDATION_UNRESOLVED` and fail closed.

The validator must preserve:

- claim/component scope;
- ADP-017 epistemic class;
- withholding/denial;
- contradiction/uncertainty;
- selected response operation;
- relationship perspective constraints;
- attractor uncertainty/competition/transition constraints;
- absence of interaction-mode/causal semantics.

Lawful variation is limited to word choice, syntax, rhythm, punctuation, source-permitted ordering freedom, and genuinely nonpropositional connective wording that does not alter entailment or stance.

Validation states include:

- `RENDER_SURFACE_VALIDATED_WORDING_ONLY`
- `RENDER_SURFACE_REJECTED_UNSUPPORTED_SEMANTIC_CONTENT`
- `RENDER_SURFACE_REJECTED_EPISTEMIC_PROMOTION`
- `RENDER_SURFACE_REJECTED_WITHHELD_CONTENT_RESURFACE`
- `RENDER_SURFACE_REJECTED_OPERATION_DRIFT`
- `RENDER_SURFACE_REJECTED_RELATIONSHIP_ATTRACTOR_BIOGRAPHY_INVENTION`
- `RENDER_SURFACE_REJECTED_HIDDEN_SOURCE_ECHO`
- `RENDER_SURFACE_REJECTED_MODE_OR_CAUSAL_METADATA`
- `RENDER_SURFACE_VALIDATION_UNRESOLVED`
- `RENDER_SURFACE_INTEGRITY_FAILURE`

Unsupported output is never repaired in place. A new model call after usable output is a rerender under ADP-025.

## 12. ADP-025 retry / rerender / RNG seam

ADP-025 remains sovereign over provider/model/version/sampling, `V2_RENDER_RNG`, retry classification, rerender identity and render receipts. CAN-022 never reads, advances, aliases or writes V3 causal RNG.

An ADP-025 operational retry before usable output may reuse the same CAN-022 admission receipt only when prompt/request identity is unchanged. Every ADP-025 rerender requires a new CAN-022 admission request/receipt bound to the new rerender ordinal/render-request identity. The prompt hash may repeat, but prior validation, publication, rejection or causal admission **never transfers**.

## 13. CAN-023 / CAN-024 / CAN-025 boundaries

- `CAN-023` owns native/translation pairing and semantic equivalence. Recovered bilingual prompt machinery is continuity evidence only here.
- `CAN-024` owns interaction-mode selection. CAN-022 does not default mode or expose it as persona/semantic instruction.
- `CAN-025` owns V2→V3 packaging. CAN-022 emits no causal package.
- `ADP-019` owns V3 external-event admission. A validated render is still not causal occurrence.

No same-cohort CAN-023/024/025 result was consumed.

## 14. Replay / provenance

CAN-022 inherits `RAWLSING_V2_RENDER_HASH_PROFILE_V1` from ADP-025: SHA-256; RFC 8785 JCS UTF-8 for structured records; domain-separated hashes.

CAN-022 domains include:

- `rawlsing:v2:prompt-authority-manifest:v1`
- `rawlsing:v2:render-admission-request:v1`
- `rawlsing:v2:render-admission-receipt:v1`
- `rawlsing:v2:compiled-prompt:v1`
- `rawlsing:v2:prompt-package:v1`
- `rawlsing:v2:render-surface-validation:v1`

Same admitted plan/envelope/manifest/template/compiler/current-turn stimulus yields identical compiled provider-message bytes and prompt hash. Hidden wall clock, mutable `latest`, filesystem/dict order as semantic order, ambient RNG, V3 causal RNG, LLM prompt compilation/inference, network lookup and unhashed post-admission augmentation are forbidden replay inputs.

When an ADP-025 pinned provider is nondeterministic, replay truth is the stored exact artifact/receipt, not a claim that the provider must regenerate identical text.

## 15. Hostile fixtures

| ID | Attack | Required result |
|---|---|---|
| H01 | actor-inaccessible true fact offered as prompt content | block access-ceiling violation; no model-visible bytes |
| H02 | raw V558 / ResolvedStructuralContext offered | forbidden source |
| H03 | full GeneratedPersonRecord / raw V3 state offered | forbidden source |
| H04 | opaque provenance points to hidden fact | audit-only; dereference forbidden |
| H05 | semantic plan `VALID_EMPTY` | valid-empty; no model call/fallback prose |
| H06 | semantic plan deferred | block; no generic hedge/response |
| H07 | semantic plan denied | block; no render |
| H08 | stale/mismatched actor envelope | stale/integrity failure |
| H09 | authority version/hash mismatch | manifest/integrity failure |
| H10 | unaccepted/unversioned semantic source | block manifest incomplete |
| H11 | prompt template contains hidden biography | hidden-default block |
| H12 | generic personality/voice fallback | hidden-default block |
| H13 | full `persona_context` passed | forbidden source |
| H14 | `SURFACED MEMORY` appended after prompt hash | post-hash mutation failure |
| H15 | `CARRIED WEIGHT` fallback appended | forbidden/default failure |
| H16 | raw backstory or objective country history supplied | forbidden source |
| H17 | prior transcript supplied merely because persisted | forbidden unless exact plan-admitted presentation context |
| H18 | exact current user turn as stimulus-only | allowed context; zero actor-truth authority |
| H19 | model adopts user assertion as actor fact absent plan unit | reject unsupported semantic content |
| H20 | model invents named anecdote/date/place/action | reject invented biography/event detail |
| H21 | model renders BELIEF as fact/knowledge | reject epistemic promotion |
| H22 | model resolves contradictory admitted claims | reject semantic drift |
| H23 | model resurfaces withheld component | reject withheld-content resurface |
| H24 | model changes response operation | reject operation drift |
| H25 | model invents reciprocal relationship truth | reject relationship invention |
| H26 | model invents type/attractor label | reject attractor invention |
| H27 | model selects interaction mode/causal admission | reject mode/causal metadata |
| H28 | prompt compiler uses LLM to summarize/complete plan | block ungoverned compiler |
| H29 | prompt compiler uses ambient RNG/dict order for semantic selection | integrity failure |
| H30 | render RNG aliases V3 causal RNG | ADP-025 namespace-collision block; no causal RNG consumption |
| H31 | rerender after prior valid/admitted artifact | new admission/request/candidate; no inheritance |
| H32 | rerender emits byte-identical visible text | content hash may match; candidate/request identity differs |
| H33 | true operational retry before usable output | same CAN-022 receipt only if ADP-025 classifies retry |
| H34 | translation equivalence asserted before CAN-023 | outside CAN-022; no canonical equivalence |
| H35 | interaction mode injected to shape persona | forbidden; CAN-024-owned |
| H36 | exact replay | same prompt bytes/hash and admission result absent new rerender context |
| H37 | template text changes | new template/prompt/package/render-request identity |
| H38 | postprocess changes epistemic/propositional meaning | reject; only versioned semantics-preserving transforms |
| H39 | full ActorAccessibleRenderEnvelope passed to model | forbidden; only plan-referenced permitted components visible |
| H40 | analyst/provenance refs audit-only | lawful if never model-visible/dereferenced |
| H41 | no style constraint in plan | no default tone/personality/voice |
| H42 | semantic conformance cannot be proven | `RENDER_SURFACE_VALIDATION_UNRESOLVED`; no final artifact |

## 16. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

The genuine ambiguity was whether the renderer should receive a rich historical persona/backstory/session packet so it can make language vivid, or a proof-carrying final semantic plan plus explicitly nonauthoritative current-turn stimulus. The second design is canonical. It preserves actor opacity, lawful absence, bounded ownership, minimum sufficient machinery, and the rule that downstream vividness cannot exceed upstream authority while preserving real surface freedom for the renderer.

The Governing Spirit supplies no biography, personality/voice default, actor knowledge, response operation, relationship truth, attractor label, interaction mode, causal effect, translation equivalence, or filler prompt content.

## 17. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__CAN_022_SEMANTIC_BLOCKER_CLOSED_FOR_V2_P8_AFTER_VOZHD_ACCEPTANCE__V2_P8_REMAINS_CAN_023_GATED__V2_P9_RENDER_IDENTITY_SEAM_SUPPLIED_BUT_CAN_024_CAN_025_AND_PHYSICAL_CAUSAL_HANDSHAKE_REMAIN_SEPARATE`.

For `V2-P8`, RA-R00 names CAN-022, ADP-025 and CAN-023. ADP-025 is accepted. This result closes CAN-022 if accepted; CAN-023 remains a same-cohort blocker and was not consumed.

For `V2-P9`, CAN-022 supplies exact admitted prompt/render lineage for later candidate identity but does not close interaction mode or packaging. ADP-019 is accepted; CAN-024/CAN-025 and physical/application causal-handshake gates remain separate.

## 18. Final token

`CAN_022_V2_RENDER_ADMISSION_PROMPT_CANONICALIZATION = PASS`
