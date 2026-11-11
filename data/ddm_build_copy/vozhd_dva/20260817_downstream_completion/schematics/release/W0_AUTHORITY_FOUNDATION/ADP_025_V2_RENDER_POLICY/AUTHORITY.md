# ADP-025 — V2 Render Model, Randomness & Version Authority

**Authority:** `V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY`  
**Authority version:** `1.0.0`  
**RA-R00 authority:** `MUST-025`  
**Decision packet:** `ADP-025`  
**Owner:** V2 render boundary  
**Mode:** authority creation only; no production implementation  
**Status:** `AUTHORITY_CREATED_PENDING_VOZHD_ADJUDICATION`  
**CONSUMER_RELEASE_SUFFICIENCY:** `SUFFICIENT`

## 1. Disposition

`PASS`.

This authority closes the bounded missing authority identified by RA-R00 as `MUST-025`: V2 model/provider/version identity, render-policy/prompt provenance, render-only randomness identity, sampling/seed metadata, retry/rerender identity, candidate/artifact hashes, render receipts, replay/audit behavior, and the categorical separation between expression variation and causal truth.

It does **not** implement the renderer. It does **not** define V3 causal RNG, prompt semantics, actor-accessibility semantics, expression-plan semantics, interaction-mode policy, V3 external-event admission/effects, or transcript-retention duration. It consumes those separately governed authorities where applicable and fails closed when they are missing.

The governing constitutional statement remains:

> **V3 generates the life. V2 expresses the generated life.**

A model may realize expression. It may not decide the hidden life it is expressing.

## 2. Evidence and authority boundary

The required historical archive was directly hashed before use:

- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`;
- computed SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`;
- verdict: `EXACT_MATCH`.

The archive is continuity/authority-recovery evidence only. Its historical V5/DDM content has zero authority over current V550+.

Binding current authority inspected:

- `state/CURRENT_STATE.md`;
- `integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md`;
- `integration/IMPLEMENTATION_RELEASE_SYNTHESIS_RULING.md`;
- `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`;
- TD-R06 `schematics/recalibration/TD_R06_V2_PHENOMENOLOGY_EXPRESSION/RESULT.json`;
- TD-R07 `schematics/closure/TD_R07_WHOLE_MACHINE_SYNTHETIC_LIFE/RESULT.json`;
- RA-R00 `schematics/release/RA_R00_RULE_AUTHORITY_IMPLEMENTATION_RELEASE/RESULT.md` and `RESULT.json`;
- W0 launch register/common law.

Recovered archive sources directly inspected:

- `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md`;
- `v2/conversation_engine.py`;
- `v2/run_conversation_chat.py`;
- `v2/spec.py`;
- `server/chat/turn.py`;
- `server/session_state.py`;
- `server/session_db.py`;
- `server/routes/chat.py`;
- `server/routes/session_bootstrap.py`;
- `server/routes/session_summary.py`;
- `run_v3_then_chat.py`.

At the exact current base, root `v2/conversation_engine.py`, `server/chat/turn.py`, and `server/session_state.py` were checked and were not present. No absent current V2 runtime code was treated as authority.

### Recovered continuity — useful but insufficient

Recovered V2/server machinery already contains a real renderer-not-decider instinct, prompt/model/output audit artifacts, native/translation rendering, and session continuity. It also demonstrates why terminal authority is missing:

- `v2/run_conversation_chat.py` selects `OPENAI_MODEL` with a mutable `gpt-4o-mini` fallback;
- `server/chat/turn.py` selects `CHAT_MODEL`/`OPENAI_MODEL` with a mutable `gpt-4o` fallback;
- provider is inferred from whether the model string begins with `claude`;
- request sampling is only partially explicit (`temperature=0.82` on one path; provider/default behavior elsewhere);
- no terminal provider/model revision binding exists;
- no terminal render-seed identity exists;
- prompt/request/raw-output/transform files are recorded but not bound by candidate/content/receipt hashes;
- retry versus rerender is not a machine identity distinction;
- recovered V2 refraction code can fall back to module-global `random`, which is negative evidence and does not become lawful render or causal authority.

Therefore historical defaults are **not grandfathered**.

## 3. Jurisdiction and consumers

### Owner

V2 owns this authority only at the **render boundary**.

It governs:

- provider/model/version binding;
- render-policy and prompt-contract provenance identity;
- V2 render RNG namespace and seed/sampling metadata;
- provider-call retry identity;
- deliberate rerender identity;
- raw-output, visible-content, candidate-artifact and receipt hashing;
- render receipts;
- artifact replay and expression-process audit;
- admission noninheritance across candidate hashes.

It does not govern:

- V3 causal RNG;
- generated biography or causal state;
- actor knowledge, belief, memory or accessibility;
- V2 salience/disclosure/response-move semantics owned elsewhere;
- V3 external-event admission/effects;
- transcript retention/compaction/deletion duration;
- the application rule choosing `PRESENTATION_NONCAUSAL` versus `IN_WORLD_CAUSAL`.

### Exact consumers

RA-R00 names `MUST-025` as a direct blocker for:

1. **V2-P8 — renderer / bilingual / replay audit**: consumes the full model-binding, render-RNG, sampling, hash and receipt law.
2. **V2-P9 — causal interaction handshake**: consumes exact candidate/artifact identity and the law that admission never transfers to a rerender/new hash. V2-P9 still does not own admission.

Downstream application/audit and the V3 admission interface may read the immutable candidate/receipt identity. They may not widen this authority.

`SUFFICIENT` means this document fully resolves `MUST-025` if Vozhd accepts it. It does not by itself release V2-P8 or V2-P9 because their separately listed RA-R00 dependencies remain separate.

## 4. Required render input envelope

Before any model invocation, the render request MUST bind, directly or by immutable hash/reference:

- actor-accessible render envelope or equivalent boundary hash;
- V2 phenomenological projection hash or equivalent;
- V2 expression-plan hash;
- session ID and session cursor hash;
- supplied interaction mode;
- `V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY@1.0.0`;
- accepted prompt-contract ID, version and content hash;
- concrete compiled prompt/message-bundle hash;
- explicit `V2RenderModelBinding`;
- explicit `V2RenderSamplingProfile`;
- explicit `V2_RENDER_RNG` identity;
- render-family anchor and `rerender_ordinal`;
- applicable transform/validator/native-translation rule identity/version/hash.

The renderer may not compensate for a missing upstream field by inventing a plausible biography, memory, relationship, belief, current situation, hidden fact or causal event. Missing authority blocks rendering.

Raw V558 lookup, analyst-only V3 truth outside the actor-accessible boundary, V3 causal RNG state, hidden wall clock, filesystem order, mutable provider/model defaults, and prior rendered prose are forbidden as render authority.

## 5. Model / provider / version law

Every render uses a versioned `V2RenderModelBinding` containing at minimum:

- `binding_id` and `binding_version`;
- `provider_id`;
- `provider_api_family`;
- provider API/endpoint version or revision;
- `requested_model_id`;
- immutable model snapshot/revision/artifact digest;
- runtime/SDK version;
- revision-visibility class;
- seed-support class;
- authorized sampling-field set.

### 5.1 No mutable model authority

The following are forbidden:

- environment or credential presence deciding provider authority;
- model-name prefix deciding provider authority;
- `latest` or equivalent moving aliases;
- unversioned `CHAT_MODEL` / `OPENAI_MODEL` fallback semantics;
- silent provider fallback after outage;
- an implementation-local default becoming authority because it happened to work historically.

For hosted models, the binding MUST pin a provider-published immutable snapshot/revision identifier. For local/self-hosted models, it MUST pin the model artifact digest and runtime/container digest. If the chosen provider cannot expose or honor a policy-authorized immutable revision, return `BLOCKED_MODEL_VERSION_UNPINNED`.

Any provider/model/revision/API/runtime binding change creates a new binding version and a new render request identity.

## 6. Render-rule / prompt-policy provenance law

This authority governs **identity and provenance**, not the semantics of the prompt contract itself.

The receipt MUST record:

- `render_policy_id = V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY`;
- `render_policy_version = 1.0.0`;
- accepted prompt-contract ID/version/content hash (`CAN-022` owns prompt semantics);
- compiled system/user/message bundle hash;
- output-transform pipeline ID/version/hash if used;
- constraint-validator ID/version/hash if used;
- native/translation rule ID/version/hash if used (`CAN-023` owns equivalence semantics).

Any prompt-contract, compiled-prompt, transform, validator, translation-rule or render-policy change capable of affecting output must be audit-visible and must change the render request identity. An unchanged turn number/session ID cannot conceal a changed prompt or model.

## 7. V2 render RNG law

The sole namespace defined here is:

`V2_RENDER_RNG`

with domain:

`v2.render.surface`

It is categorically disjoint from every V3 causal RNG stream. V2 render code MUST NOT read, advance, alias, reseed or write V3 causal RNG state.

Render randomness may govern only:

- provider text sampling;
- surface-realization-equivalent variation already permitted by a governed expression plan.

It may not decide:

- biography;
- actor knowledge/belief/memory;
- hidden facts;
- causal events/effects;
- relationship truth;
- attractor formation/classification;
- missing salience/disclosure/response-move semantics;
- any missing authority.

### 7.1 Required RNG identity

Every stochastic render receipt records:

- `rng_namespace = V2_RENDER_RNG`;
- `render_stream_id`;
- a V2-only `render_nonce` fixed before provider invocation;
- `provider_seed_status`;
- explicit provider seed when supported;
- sampling-profile hash.

`render_nonce` is noncausal identity material. It may be random or deterministically issued inside V2, but its source cannot be a V3 causal stream, hidden wall clock, or filesystem order.

A provider binding may declare either:

- `SUPPORTED_EXPLICIT` — provider seed is recorded; or
- `UNSUPPORTED_BY_PINNED_BINDING` — no provider seed control exists.

Lack of provider seed support does **not** itself block a noncausal render if the pinned binding explicitly declares it. In that case deterministic provider regeneration is `UNGUARANTEED`; exact replay is the stored artifact, not a claim that the provider must regenerate identical text.

## 8. Sampling identity law

Every model request uses a versioned `V2RenderSamplingProfile`. It records, explicitly or as `EXPLICIT_UNSUPPORTED` for the pinned binding:

- temperature;
- top-p;
- top-k;
- max output tokens;
- stop sequences;
- frequency penalty;
- presence penalty;
- response format;
- tool policy;
- provider seed status/seed;
- a canonical map of every other provider-specific request parameter capable of affecting generation.

A request-affecting field supported by the chosen binding may not silently fall through to a mutable provider default. Such omission is `BLOCKED_SAMPLING_PROFILE_INCOMPLETE`.

## 9. Retry versus rerender identity

The machine MUST distinguish three levels:

1. **render family** — one immutable session/turn + actor-accessible boundary + expression-plan anchor;
2. **render request** — one exact provider/model/prompt/sampling/RNG/constraint realization within that family;
3. **provider attempt** — one actual call under that request.

### 9.1 Retry

A `RETRY` is lawful only when an operational/provider failure produced **no usable model output bytes or structured payload**.

A retry:

- preserves the same `render_request_id`;
- preserves model/prompt/sampling/seed/constraint identity exactly;
- increments `retry_ordinal`;
- creates a new `provider_attempt_id`.

If a timeout leaves provider-side completion unknown, record the prior attempt as `UNKNOWN_PROVIDER_COMPLETION`; no candidate exists unless output later arrives and is captured. A later-arriving output is separately hashed and never overwrites another attempt/candidate.

### 9.2 Rerender

A `RERENDER` is any new model call after model output was received, **or** any new call that intentionally changes provider/model/prompt/sampling/seed/constraints/surface-variation request.

A rerender:

- increments `rerender_ordinal`;
- receives a new V2-only render nonce;
- receives a new `render_request_id`;
- can never reuse a prior candidate identity;
- never inherits prior admission/rejection/publication status.

A validator failure after output exists followed by another model call is therefore a rerender, not a retry.

If two rerenders produce byte-identical visible text, their `rendered_content_hash` may match, but their candidate artifact hashes and candidate IDs **must differ**, because their request/attempt provenance differs.

## 10. Canonical hash and identity profile

Hash profile:

`RAWLSING_V2_RENDER_HASH_PROFILE_V1`

Algorithm: `SHA-256`.

Structured serialization: RFC 8785 JSON Canonicalization Scheme (JCS), UTF-8.

Raw text: UTF-8 encoding of the exact Unicode string received by the application, with **no Unicode, whitespace, newline or case normalization before hashing**.

Every hash uses an explicit domain prefix.

### 10.1 Required hashes

```text
model_binding_hash =
  SHA256("rawlsing:v2:model-binding:v1\n" || JCS(model_binding_without_hash))

sampling_profile_hash =
  SHA256("rawlsing:v2:sampling-profile:v1\n" || JCS(sampling_profile_without_hash))

render_request_hash =
  SHA256("rawlsing:v2:render-request:v1\n" || JCS(render_request_identity))

raw_output_hash =
  SHA256("rawlsing:v2:raw-output:v1\n" || exact_raw_output)

rendered_content_hash =
  SHA256("rawlsing:v2:rendered-content:v1\n" || JCS(application_visible_content_payload))

candidate_artifact_hash =
  SHA256("rawlsing:v2:candidate-artifact:v1\n" || JCS(candidate_artifact_without_candidate_id_and_artifact_hash))

render_receipt_hash =
  SHA256("rawlsing:v2:render-receipt:v1\n" || JCS(render_receipt_without_render_receipt_hash))
```

### 10.2 IDs

`render_request_id = v2rrq:<render_request_hash>`.

`provider_attempt_id = v2ratt:<sha256(JCS({render_request_id,retry_ordinal}))>` under the same profile/domain discipline.

`candidate_id = v2cand:<candidate_artifact_hash>`.

The candidate-artifact hash preimage contains at minimum:

- render request ID;
- provider attempt ID;
- retry ordinal;
- rerender ordinal;
- raw-output hash;
- rendered-content hash;
- transform-chain hash;
- interaction mode;
- candidate status.

**Causal admission binds `candidate_artifact_hash`, never `rendered_content_hash` alone.** Content identity and candidate identity are deliberately different so that a rerender remains a distinct candidate even when visible text is identical.

## 11. Artifact law

Every provider invocation creates an immutable `V2RenderAttemptArtifact` recording request/attempt identity, provider-response metadata, operational status, and raw-output hash when output exists.

Only an output that passes the governed actor-accessible truth/expression constraints may finalize as an immutable `RenderedTurnArtifact`.

Initial statuses:

- `PRESENTATION_NONCAUSAL_RENDERED` in presentation mode;
- `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION` in in-world causal mode.

Raw provider output and final application-visible content are separately hashed. Every deterministic parser/cleanup/native-translation transform that changes bytes or structured fields must have a version/hash in the receipt.

A candidate artifact is never edited in place. Any correction that changes output creates a rerender and new candidate. Later admission/rejection metadata is linked by a separate receipt/reference; it does not rewrite the historical render artifact.

Retention duration belongs to the separate transcript/session retention authority. This authority requires only that surviving hashes/refs cannot be silently changed and that a causal admission reference cannot be retargeted to different content.

## 12. `V2RenderReceipt`

Every provider attempt emits a receipt, including failures.

Minimum receipt fields:

- receipt schema version;
- render policy ID/version;
- render family ID;
- render request ID;
- provider attempt ID;
- retry/rerender ordinals;
- actor-accessible boundary hash;
- V2 projection and expression-plan hashes;
- session ID and cursor hash;
- interaction mode;
- prompt-contract ID/version/content hash;
- compiled prompt/messages hash;
- full model binding + model-binding hash;
- full sampling profile + sampling-profile hash;
- render RNG identity;
- provider request metadata hash;
- provider response metadata hash/status;
- raw-output hash or `NO_OUTPUT`;
- transform chain + hash;
- rendered-content hash or `NO_CANDIDATE`;
- candidate-artifact hash/ID or `NO_CANDIDATE`;
- candidate status;
- constraint-validation status;
- operational status;
- render-receipt hash.

API keys, credentials and other secrets are forbidden from the receipt.

Operational failures, constraint rejection, ambiguous timeouts and integrity failures still emit typed receipts with hashes for every artifact actually received.

## 13. Replay / audit semantics

Three operations remain distinct.

### 13.1 Artifact replay

Exact replay of an existing render means retrieving the immutable candidate by `candidate_artifact_hash` and verifying content/artifact/receipt hashes. **No model call occurs.**

### 13.2 Process re-execution

A diagnostic re-execution may call the exact pinned model with the recorded prompt/sampling/seed identity. It is a new audit execution, never the identity of the original artifact.

If provider nondeterminism returns different output, record `REEXECUTION_MISMATCH`. Do not overwrite the original; do not mutate V3; do not reinterpret the historical admitted event.

### 13.3 Causal replay

V3 causal replay never depends on regenerating V2 text. It replays V3 events and the exact admitted candidate artifact hash/admission receipt. Render model availability, render RNG, or a later provider output cannot change causal truth.

This is the core separation: **expression-process reproducibility is desirable and auditable; causal-state reproducibility is not allowed to depend on it.**

## 14. Causal-admission separation law

A rendered model output is never causal authority.

Render variation cannot alter:

- generated biography;
- V3 causal state;
- generated causal memory/accessibility;
- relationship/household/genealogy truth;
- attractor trajectory/state;
- external-event effects.

The LLM may realize wording only inside the actor-accessible truth and governed expression constraints supplied to it. If it invents hidden facts, analyst-only facts, causal facts, inaccessible memories, unsupported beliefs, relationship history or attractor claims, the result is `RENDER_REJECTED_CONSTRAINT_VIOLATION` and is audit-only.

In `IN_WORLD_CAUSAL` mode, a valid `RenderedTurnArtifact` begins as:

`CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`.

Only a separate V3 admission receipt for **that exact `candidate_artifact_hash`** may authorize the application to:

- expose/commit it as an in-world utterance/action that actually occurred;
- advance the causal-session cursor.

A rerender has a new artifact hash and therefore requires a new admission. Prior admission never transfers.

If an already-admitted utterance is later rerendered, the new render does not rewrite the admitted historical event. Any new in-world utterance would itself require new V3 admission under the separate external-event authority.

`PRESENTATION_NONCAUSAL` may display without V3 admission because its status is explicitly noncausal; persistence/display does not promote it into generated history.

## 15. Precedence and fail-closed states

Precedence is strict:

1. missing actor-accessible/expression authority → block before model call;
2. missing prompt/render/model/sampling/RNG authority → block before model call;
3. no-output operational failure → same-request retry may be attempted;
4. received output → validate against supplied truth/expression constraints;
5. constraint violation → audit-only rejected attempt; any new model call is a rerender;
6. valid output → immutable candidate + receipt;
7. presentation mode may display noncausally; causal mode remains pending exact V3 admission;
8. any hash/provenance mismatch outranks display/publication/admission reuse and becomes integrity failure.

Machine fail/negative states are defined in `AUTHORITY.json`, including:

- `BLOCKED_MISSING_RENDER_POLICY`;
- `BLOCKED_MISSING_PROMPT_CONTRACT`;
- `BLOCKED_MODEL_BINDING_MISSING`;
- `BLOCKED_MODEL_VERSION_UNPINNED`;
- `BLOCKED_PROVIDER_IDENTITY_AMBIGUOUS`;
- `BLOCKED_SAMPLING_PROFILE_INCOMPLETE`;
- `BLOCKED_RENDER_RNG_IDENTITY_MISSING`;
- `BLOCKED_RENDER_RNG_NAMESPACE_COLLISION`;
- `BLOCKED_INPUT_BOUNDARY_INCOMPLETE`;
- `RENDER_REJECTED_CONSTRAINT_VIOLATION`;
- `RENDER_FAILED_OPERATIONAL_RETRYABLE`;
- `BLOCKED_RECEIPT_INCOMPLETE`;
- `BLOCKED_HASH_MISMATCH`;
- `BLOCKED_RETRY_MISCLASSIFIED`;
- `BLOCKED_RERENDER_ADMISSION_INHERITANCE`;
- `BLOCKED_CAUSAL_PUBLICATION_BEFORE_EXACT_ADMISSION`.

## 16. Forbidden behavior

Forbidden under this authority:

- mutable/default provider/model/version selection;
- provider inference from model name or credentials;
- `latest` model authority;
- implicit request-affecting provider sampling defaults;
- V3 causal RNG use for V2 rendering;
- render RNG deciding semantic/causal facts;
- model output inventing hidden facts or filling missing authority;
- rendered text serving as evidence of V3 belief/memory/relationship/attractor state;
- in-place candidate edits;
- rerender mislabeled as retry;
- causal admission inherited by new candidate hash;
- causal publication before exact V3 admission;
- regeneration overwriting historical artifact identity;
- fallback provider/model substitutions hidden inside one receipt/request identity.

## 17. Hostile fixtures

The machine contract includes eighteen hostile fixtures in `AUTHORITY.json`. They cover mutable model defaults, provider inference, hidden sampling defaults, V3/V2 RNG collision, seed-unsupported providers, operational retries, validator repair rerenders, identical-text rerenders, admission inheritance, hidden-fact invention, hidden prompt/model changes, unversioned transforms, content-hash-only causal proposals, replay with unavailable providers, nondeterministic re-execution, tampering, provider fallback and premature causal publication.

Required invariant across all fixtures:

> A different render may change expression. It may never change what happened unless V3 separately admits that exact new observable artifact under its own causal authority.

## 18. Compatibility constraints

- `CAN-022` owns render-admission/prompt semantics; this policy records and verifies its exact version/hash.
- `CAN-023` owns native/translation equivalence; this policy records its version/hash when used.
- V3 external-event authority owns admit/reject/effects; this policy only supplies exact immutable candidate identity and preserves the already-closed no-admission-inheritance law.
- transcript/session retention authority owns deletion/compaction duration; this policy fixes identity/hash invariants.
- interaction-mode authority owns mode selection; this policy obeys the supplied mode.
- no historical model/provider/default is grandfathered.

## 19. Release sufficiency

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`.

If accepted, this authority fully resolves `MUST-025`. V2-P8 and V2-P9 remain gated by their other separately scheduled RA-R00 authorities and implementation dependencies; this verdict does not collapse those dependencies or release production code.

`ADP_025_V2_RENDER_POLICY_AUTHORITY = PASS`
