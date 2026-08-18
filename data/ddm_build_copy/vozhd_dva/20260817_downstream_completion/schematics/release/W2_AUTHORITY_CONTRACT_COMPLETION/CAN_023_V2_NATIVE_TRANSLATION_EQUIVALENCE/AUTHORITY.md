# CAN-023 — V2 Native & Translation Equivalence Canonicalization

**Canonicalization ID:** `CAN-023`  
**RA-R00 item:** `CAN-023`  
**Canonical machine authority:** `V2_NATIVE_TRANSLATION_EQUIVALENCE_RULE`  
**Version:** `1.0.0`  
**Owner:** V2 bilingual/multilingual render-equivalence boundary  
**Repository:** `maidiu/rawlsing`  
**Assigned branch:** `agent/vozhd-dva-w2-can-023-v2-native-translation`  
**Exact base SHA:** `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`  
**Mode:** bounded recovered-mechanism canonicalization only; no production implementation  
**Whole-machine architecture:** `CLOSED`  
**W0:** `CLOSED`  
**W1:** `CLOSED__18_OF_18_ACCEPTED`  
**W2 first batch:** `CLOSED__6_OF_6_ACCEPTED`  
**Verdict:** `PASS`

## 1. Holding

CAN-023 binds terminal pairing, identity, semantic-equivalence, failure and replay semantics for V2 `NATIVE` and `TRANSLATION` render surfaces.

The constitutional rule is:

```text
ONE_AUTHORIZED_SEMANTIC_PLAN
    -> NATIVE surface realization
    -> TRANSLATION surface realization, when requested

TRANSLATION != SECOND_SEMANTIC_PLAN
NATIVE_WORDING != SEMANTIC_AUTHORITY
TRANSLATION_WORDING != SEMANTIC_AUTHORITY
SURFACE_EQUIVALENCE != TEXTUAL_SIMILARITY
RENDERED_SURFACE != CAUSAL_OCCURRENCE
```

Both surfaces are expression artifacts over the same already-authorized semantic plan. Neither surface may add, remove, upgrade, resolve, reinterpret or otherwise change protected plan meaning.

`NATIVE` is the canonical authored-language surface role for this render pair. It does **not** by itself prove the actor's ethnicity, nationality, childhood language, identity, biography or sociological category. Its language/locale identity must be explicitly supplied by the render request or another accepted upstream source.

`TRANSLATION` is an auxiliary target-language surface over the same semantic plan. Its existence does not create a second actor voice, second response decision, second relationship posture, second epistemic state or second causal candidate.

A lawful native artifact remains lawful if an **optional** translation is missing, operationally failed, semantically drifted or equivalence-unresolved. A translation may never silently substitute for a missing/failed native artifact, and native text may never silently populate a missing translation field.

## 2. Required historical archive verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- directly computed SHA256 before reliance: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- verdict: `EXACT_MATCH`
- archive entries: `13,138`
- recovered V2/V3/server status: continuity / authority-recovery / negative-boundary evidence only
- historical V5/DDM authority over current V550+: **ZERO**

Focused recovered-source court from the exact archive:

```text
python -m pytest -q \
  tests/test_chat_integrity.py \
  tests/test_v5_chat_surface_psyche.py \
  v3/tests/test_v5_v2_chat_prompt_no_raw_v5_leaks.py \
  v3/tests/test_v5_voice_packet_surface_allowlist.py \
  v3/tests/test_v5_render_surface_psyche.py \
  v3/tests/test_v5_persona_sheet_surface_psyche.py \
  v3/tests/test_persona_sheet_integrity.py

22 passed
```

Direct parser probes against the recovered `parse_reply_native_and_translation` establish negative evidence:

```text
NATIVE: مرحبا / TRANSLATION: Hello
    -> native='مرحبا', translation='Hello'

NATIVE: مرحبا / TRANSLATION: <missing>
    -> native='مرحبا', translation='مرحبا'      # unlawful silent substitution

NATIVE: أنا غير متأكد / TRANSLATION: I am certain
    -> parser accepts both surfaces              # no semantic-equivalence court

DRAFT: مرحبا / Hello
    -> parser accepts an asymmetric dual surface # not canonical terminal pairing
```

Passing recovered tests proves useful surface-boundary continuity. It does not supply terminal bilingual equivalence authority.

## 3. Binding current authority and dependency law

CAN-023 was canonicalized against the exact launch base after direct inspection of:

- `state/CURRENT_STATE.md`;
- `RAWLSING_GOVERNING_SPIRIT.md`;
- `TERMINAL_DEMAND_ENVELOPE.md`;
- `ARCHITECTURE_PASS_LAW.md`;
- whole-machine closure and implementation-release synthesis;
- W0 closure, W1 closure and W2 first-batch closure state;
- `integration/V2_COMPLETION_IMPLEMENTATION_RULING.md`;
- accepted `ADP-025 / V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY@1.0.0`;
- W2 Batch-02 common law and W2-B02-05 assignment.

The accepted constitutional V2 law is:

> **V3 generates the life. V2 expresses the generated life.**

Direct dependencies available to CAN-023:

1. **V2 completion ruling** — V2 owns language/dialogue/native-translation rendering, but not actor causal truth.
2. **ADP-025** — owns provider/model/version identity, render sampling/randomness, retry/rerender identity, artifact hashes and render receipts. CAN-023 consumes those receipts and does not redefine them.
3. **CAN-022 architecture requirement only** — CAN-023 requires an already-authorized source semantic-plan hash / render-admission anchor, but it consumes **no same-cohort CAN-022 worker return**. Until CAN-022 is separately accepted, V2-P8 remains independently gated.

No W2 Batch-02 sibling result was consumed as authority.

## 4. Direct recovered-source inventory and dispositions

Direct historical files inspected include:

| Recovered source | SHA256 / finding | CAN-023 disposition |
|---|---|---|
| `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135`; explicit `NATIVE:`/`TRANSLATION:` prompt and parser | primary continuity + negative evidence |
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7`; renderer-not-decider continuity | preserve constitutional direction |
| `v2/run_conversation_chat.py` | `b9276a4d7fc9dfdc83cc220528e4f16c1880d78419ed06430a5e9570a60efdc8`; direct caller / model path | implementation continuity only |
| `server/chat/turn.py` | `10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3`; parses pair, displays translation, persists native alongside display text | adapt artifact-pair persistence; reject fallback semantics |
| `server/session_state.py` | `9c9c3b0e2b3bff700af127e03805166102920019d6acd099ee8270fbe63bc15a`; session continuity | reference only |
| `server/session_db.py` | `0d9bf508aa748ce8eff3360a7c615ab0ed086f3a34c3190815cb0485fe234c12`; persistence/audit substrate | reference only |
| `tests/test_chat_integrity.py` | `efcb4ad8c65bd1fc7a4522160a9543654da159e6381819ef6b4089044ec3b9c2`; chat-integrity tests | continuity court only |
| recovered V3 surface tests | actor/analyst leakage safeguards | preserve boundary; not translation authority |

At the exact current launch base, root `v2/conversation_engine.py` is absent. No absent current implementation was treated as authority.

### Recovered dual-surface disposition table

| Recovered mechanism | Disposition | Terminal holding |
|---|---|---|
| explicit `NATIVE` + `TRANSLATION` dual surfaces | `PRESERVE_ADAPT` | retain paired surfaces over one semantic plan |
| native surface in a supplied actor render language | `PRESERVE_ADAPT` | explicit language/locale ref required; role does not infer biography |
| translation in a supplied target/user language | `PRESERVE_ADAPT` | target language/locale is explicit input; no heuristic inference authority |
| “write fresh from communicative intent; not word-for-word” | `PRESERVE_AS_SURFACE_VARIATION_ONLY` | idiomatic re-expression is allowed only inside protected semantic invariants |
| one model output containing both blocks | `IMPLEMENTATION_OPTION_COMPATIBLE` | allowed if both extracted artifacts and all receipts/hashes remain separately identifiable |
| separate native and translation model calls | `IMPLEMENTATION_OPTION_COMPATIBLE` | allowed under ADP-025 with exact independent receipts; semantics still one plan |
| `parse_reply_native_and_translation` marker extraction | `ADAPT_STRICTLY` | extraction may locate surfaces but never establish semantic equivalence |
| missing `TRANSLATION` -> return native as translation | `REMOVE_REJECT` | explicit missing/failed translation state; no substitution |
| missing markers -> `(None, raw)` treated as display translation | `REMOVE_AS_SEMANTIC_FALLBACK` | surface role must come from explicit request/artifact metadata |
| `DRAFT:` native one-liner + fuller English output | `COMPATIBILITY_ONLY_NOT_CANONICAL_PAIR` | asymmetry cannot establish same-plan equivalence without explicit terminal receipts |
| embedded native quote + bracketed gloss parser | `COMPATIBILITY_ONLY` | useful migration parser only; per-span gloss is not terminal pair authority |
| translation automatically chosen as display surface | `OUT_OF_SCOPE_PRESENTATION_CHOICE` | application/render presentation policy chooses display; CAN-023 only validates pairing |
| store translated `content` plus `content_native` | `ADAPT_TO_EXACT_PAIR_REFS` | persistence preserves exact paired artifacts/refs; persistence does not create equivalence |
| prefill `NATIVE:` for one provider | `IMPLEMENTATION_COMPATIBILITY_ONLY` | no semantic force |
| discourse-particle / idiom instructions | `ADAPT_AS_ALLOWED_SURFACE_VARIATION` | only where protected semantics remain unchanged |
| culturally plausible wording beyond supplied plan | `REMOVE_REJECT` | culture cannot invent biography, identity, stance or relationship meaning |
| no equivalence validator in recovered runtime | `REPLACE_WITH_CANONICAL_EQUIVALENCE_RECEIPT` | explicit categorical equivalence court required |
| no typed translation failure states | `REPLACE_WITH_TYPED_FAILURE_LAW` | optional/required/missing/failed/drift/unresolved states remain distinct |

## 5. Jurisdiction

CAN-023 owns only:

- native/translation render-pair identity;
- exact source semantic-plan binding for both surfaces;
- native and translation surface-role identity;
- explicit source/target language and locale references;
- translation requirement state (`NOT_REQUESTED`, `OPTIONAL`, `REQUIRED`);
- translation-rule identity and ADP-025 model/render receipt linkage;
- protected semantic invariant profile for bilingual equivalence;
- allowed surface-only variation categories;
- categorical semantic-drift / unresolved-equivalence states;
- native/translation non-substitution law;
- optional-versus-required translation failure semantics;
- immutable equivalence receipts and pair replay/provenance.

CAN-023 does **not** own:

- actor knowledge/belief/claim permission;
- V2 semantic-plan creation, salience, disclosure, register, response operation, relationship expression, attractor expression, boundary/effort semantics or session-state semantics;
- prompt-admission semantics (CAN-022);
- model/provider/render RNG/retry/rerender semantics (ADP-025);
- application display-surface preference outside explicit translation requirement;
- language identity inference from actor ethnicity, nationality, country, class or biography;
- interaction-mode selection;
- external-event packaging;
- V3 admission or causal publication;
- a translation provider's undocumented notion of confidence;
- embedding-space semantic identity.

## 6. Canonical input contract

A semantic equivalent of `V2NativeTranslationPairInput` MUST bind:

```text
actor_id
session_id
turn_id
source_semantic_plan_id
source_semantic_plan_hash
source_render_family_or_request_ref
source_render_admission_ref_or_required_dependency_ref
native_language_ref
native_locale_ref | null
translation_requirement
translation_language_ref | null
translation_locale_ref | null
native_artifact_ref
native_artifact_hash
native_render_receipt_ref
translation_artifact_ref | null
translation_artifact_hash | null
translation_render_or_transform_receipt_ref | null
translation_rule_id
translation_rule_version
translation_rule_hash
adp025_policy_version_and_receipt_refs
equivalence_evaluator_binding_ref
input_integrity_state
```

`translation_requirement` is exactly one of:

- `TRANSLATION_NOT_REQUESTED`
- `TRANSLATION_OPTIONAL`
- `TRANSLATION_REQUIRED`

CAN-023 does not infer this requirement from message language, actor identity, UI assumptions or historical defaults.

### Language / locale identity

A `LanguageLocaleRef` is an explicit stable upstream/application reference containing at minimum:

```text
language_id
language_registry_or_schema_version
optional_script_id
optional_locale_id
source_authority_or_configuration_ref
```

CAN-023 does not infer the actor's “native language” from country, ethnicity, religion, class, name, geography or cultural plausibility. A user-message language detector may be used only if a separately authorized application/render contract gives that detector authority for surface routing; detection is not biography.

## 7. One-plan law

The source semantic plan is the semantic authority for **both** surfaces.

```text
native.semantic_plan_hash      == source_semantic_plan_hash
translation.semantic_plan_hash == source_semantic_plan_hash
```

If either surface binds a different plan hash, the pair is `INTEGRITY_FAILURE_PLAN_MISMATCH`.

A translator may receive the native artifact as surface context, but native wording cannot supersede or expand the source semantic plan. If native wording itself drifted from the plan, a translation that faithfully copies that drift does not become lawful merely because native and translation agree with each other.

Therefore equivalence is a **three-way court**:

```text
SOURCE SEMANTIC PLAN
  ↙              ↘
NATIVE          TRANSLATION
```

not merely text-to-text similarity.

## 8. Protected semantic invariant profile

Canonical profile:

`V2_NATIVE_TRANSLATION_EQUIVALENCE_PROFILE@1.0.0`.

Every material semantic obligation supplied by the source plan is protected. At minimum, where present, both surfaces must preserve exactly:

1. selected semantic target / claim / proposition refs;
2. referent identity and perspective binding;
3. polarity / negation;
4. epistemic class and force — including knowledge, belief, uncertainty, explicit nonknowledge and withheld/nonassertable distinctions where supplied;
5. modality, scope and temporal qualification where plan-owned;
6. intentionally omitted or withheld content boundaries;
7. contradiction-set membership and multiplicity;
8. response-operation identity and semantic scope;
9. boundary/limit/exit semantic scope where supplied;
10. relationship-expression meaning/perspective where supplied;
11. attractor-expression meaning where supplied;
12. source-plan ordering/contrast only where the plan marks it semantically material;
13. interaction/candidate status **by reference only**; translation may not change it;
14. any other plan atom marked `MUST_PRESERVE_ACROSS_SURFACES` by its owning authority.

If the plan does not machine-distinguish whether a feature is semantic or merely stylistic, CAN-023 may not guess that it is stylistic. Material uncertainty remains `EQUIVALENCE_UNRESOLVED`.

## 9. Allowed surface variation

Surface variation is lawful only if all protected semantic invariants remain unchanged.

Allowed classes include:

- lexical substitution / synonymy where exact referent and semantic force remain the same;
- idiomatic rather than word-for-word rendering;
- target-language syntax and word order;
- obligatory morphology that does not assert a new actor property;
- punctuation and segmentation;
- discourse-particle insertion, omission or natural substitution when the particle carries no protected semantic effect in context;
- pronoun or zero-pronoun realization where referent identity remains exact;
- transliteration / borrowing when it does not add hidden cultural or biographical meaning and does not make a required semantic obligation unresolved;
- surface rhythm and register variation already authorized by the source semantic plan.

The following are **not** free surface variation:

- adding certainty, doubt, hedging, confidence or factuality;
- dropping uncertainty/nonknowledge qualifiers;
- changing negation, quantification, time or referent;
- reconciling contradictory statements into one coherent statement;
- adding/removing a relationship implication, honorific, intimacy claim, hostility, deference or social distance when not plan-authorized;
- changing refusal, boundary, exit, question, challenge or other response-operation semantics;
- adding cultural anecdote, identity detail, kinship fact, locality, religious claim or biographical explanation;
- changing the set of selected/withheld semantic targets;
- changing causal or interaction status;
- translating a local idiom by inventing a culturally plausible life fact.

A culturally natural phrase is lawful only as **surface realization of already-authorized meaning**.

## 10. Surface semantic alignment receipts

Each surface evaluated under CAN-023 carries or receives a semantic alignment receipt equivalent to:

```text
V2SurfaceSemanticAlignmentReceipt {
  surface_role = NATIVE | TRANSLATION,
  artifact_ref,
  artifact_hash,
  source_semantic_plan_hash,
  protected_plan_atom_refs[],
  preserved_atom_refs[],
  omitted_surface_only_refs[],
  added_semantic_candidate_refs[],
  removed_semantic_candidate_refs[],
  altered_force_or_scope_refs[],
  contradiction_preservation_refs[],
  operation_preservation_refs[],
  relationship_preservation_refs[],
  unresolved_material_refs[],
  evaluator_binding_ref,
  evaluator_rule_version,
  evidence_refs[],
  status,
  receipt_hash
}
```

Statuses:

- `PLAN_CONFORMANT`
- `SEMANTIC_DRIFT_DETECTED`
- `EQUIVALENCE_UNRESOLVED`
- `MISSING_PLAN_ALIGNMENT_AUTHORITY`
- `INTEGRITY_FAILURE`

### Evaluator-authority law

Positive bilingual semantic adjudication is lawful only through an **exact separately governed evaluator rule / authority** whose semantic operations are machine-bound. A conforming evaluator authority must bind at minimum:

- evaluator authority ID, version and content hash;
- the protected semantic-invariant profile/version it is authorized to compare;
- admissible comparison operations and their exact semantics;
- protected-atom comparison semantics, including how preservation, addition, removal, force/scope alteration and contradiction preservation are established;
- result states, including positive, drift, missing-authority, ambiguity/unresolved and integrity outcomes;
- ambiguity/unresolved law that forbids best-effort positive adjudication;
- exact provenance, deterministic/replay contract and evaluator receipt identity.

Merely pinning a model, provider, model version, prompt, sampling profile, seed or receipt establishes **provenance only**. It does not create evaluator semantic authority. ADP-025 governs render/model provenance; it does not authorize a model to decide that protected meaning was preserved.

#### Model diagnostic-only law

A model/LLM MAY lawfully:

- generate a `NATIVE` or `TRANSLATION` surface under the separately governed render/translation path;
- emit diagnostic candidate atom mappings;
- emit diagnostic candidate alignment annotations;
- emit candidate drift flags or candidate unresolved flags;
- emit other explicitly typed **NONAUTHORITATIVE_DIAGNOSTIC_EVIDENCE**.

Those outputs have **zero semantic-adjudication authority by themselves**. Model output alone MUST NOT establish:

- protected-atom preservation;
- absence of semantic drift;
- `PLAN_CONFORMANT`;
- `SEMANTICALLY_EQUIVALENT`.

This remains true even when the model/provider/version/prompt/sampling/seed/receipt are fully pinned and replayable. A stored or reproducible model judgment remains diagnostic evidence, not semantic authority.

A separately governed evaluator may consume model-produced diagnostic evidence only if its own accepted evaluator rule explicitly admits that evidence class and defines how it may be used. The governed evaluator's machine-bound operations and result law remain the authority; the model cannot override them.

Still insufficient by themselves:

- a translator's self-assertion “equivalent”;
- embedding/cosine similarity;
- scalar LLM confidence/probability;
- a pinned model judgment such as `equivalent=true`;
- apparently complete model-generated protected-atom mappings;
- crossing any similarity/confidence threshold;
- free-text “looks close enough” review.

If a material bilingual comparison lacks an exact accepted evaluator authority with the required operation semantics, the surface/pair returns `MISSING_PLAN_ALIGNMENT_AUTHORITY` and/or `EQUIVALENCE_UNRESOLVED` as appropriate. There is no best-effort semantic pass.

The final rule is categorical invariant preservation **under governed evaluator authority**, not score maximization or model plausibility.

## 11. Canonical equivalence receipt

A semantic equivalent of `V2NativeTranslationEquivalenceReceipt` binds:

```text
equivalence_receipt_id
equivalence_rule_id = V2_NATIVE_TRANSLATION_EQUIVALENCE_RULE
equivalence_rule_version = 1.0.0
equivalence_profile_id = V2_NATIVE_TRANSLATION_EQUIVALENCE_PROFILE
equivalence_profile_version = 1.0.0
pair_basis_hash
source_semantic_plan_hash
native_artifact_ref
native_artifact_hash
native_alignment_receipt_hash
translation_artifact_ref | null
translation_artifact_hash | null
translation_alignment_receipt_hash | null
native_language_ref
translation_language_ref | null
translation_requirement
protected_atom_refs[]
added_semantics_refs[]
removed_semantics_refs[]
altered_semantics_refs[]
unresolved_material_refs[]
allowed_surface_variation_records[]
status
evidence_refs[]
receipt_hash
```

Equivalence status is exactly one of:

- `SEMANTICALLY_EQUIVALENT`
- `NATIVE_ONLY_TRANSLATION_NOT_REQUESTED`
- `NATIVE_VALID_TRANSLATION_OPTIONAL_MISSING`
- `NATIVE_VALID_TRANSLATION_OPTIONAL_FAILED`
- `NATIVE_VALID_TRANSLATION_OPTIONAL_DRIFT_REJECTED`
- `NATIVE_VALID_TRANSLATION_OPTIONAL_EQUIVALENCE_UNRESOLVED`
- `TRANSLATION_REQUIRED_MISSING`
- `TRANSLATION_REQUIRED_FAILED`
- `TRANSLATION_REQUIRED_DRIFT_REJECTED`
- `TRANSLATION_REQUIRED_EQUIVALENCE_UNRESOLVED`
- `NATIVE_REQUIRED_MISSING_OR_FAILED`
- `INTEGRITY_FAILURE_PLAN_MISMATCH`
- `INTEGRITY_FAILURE_ARTIFACT_OR_RECEIPT`

Only `SEMANTICALLY_EQUIVALENT` authorizes the translation artifact to be labeled a canonical translation of that native/plan pair. A positive `PLAN_CONFORMANT` surface receipt and final `SEMANTICALLY_EQUIVALENT` pair receipt require the exact separately governed evaluator authority described in §10; model diagnostics cannot issue either positive state on their own.

A native-only status does not relabel native text as translation.

## 12. Translation failure and non-substitution law

### 12.1 Translation not requested

If `TRANSLATION_NOT_REQUESTED`, a lawful native artifact may stand alone. Pair state is `NATIVE_ONLY_TRANSLATION_NOT_REQUESTED`.

### 12.2 Optional translation

If `TRANSLATION_OPTIONAL` and translation is:

- missing -> `NATIVE_VALID_TRANSLATION_OPTIONAL_MISSING`;
- operationally failed -> `NATIVE_VALID_TRANSLATION_OPTIONAL_FAILED`;
- semantically drifted -> `NATIVE_VALID_TRANSLATION_OPTIONAL_DRIFT_REJECTED`;
- materially unresolved -> `NATIVE_VALID_TRANSLATION_OPTIONAL_EQUIVALENCE_UNRESOLVED`.

In all four cases, the lawful native artifact remains valid and may be presented/persisted under its own render authority. The invalid/unavailable translation is not silently substituted, displayed as equivalent or used as semantic evidence.

### 12.3 Required translation

If `TRANSLATION_REQUIRED`, missing/failed/drifted/unresolved translation makes the pair/delivery requirement incomplete under the corresponding typed status.

**The native artifact itself remains independently valid if it already passed its own admission/conformance gates.** Translation failure does not retroactively invalidate native content.

The application may report the required translation surface unavailable; it may not fill it with native text or another unverified language surface.

### 12.4 Native missing or failed

`NATIVE` is the required anchor surface for this canonical pair. If native is missing/failed/nonconformant, translation cannot substitute for it. A translation-only artifact may remain an audit artifact but is not a valid `V2NativeTranslationPair`.

### 12.5 Drifted translation

A translation with semantic drift is quarantined from canonical translation use. A new translation attempt creates new immutable translation artifact/receipt identity under ADP-025; the old drifted artifact remains audit evidence and is never edited in place.

## 13. Pair identity

Pair identity is content/provenance bound and does not depend on mutable session labels or “latest translation.”

First compute:

```text
pair_basis_hash = SHA256(
  "rawlsing:v2:native-translation-pair-basis:v1\n" || JCS({
    pair_schema_version,
    actor_id,
    session_id,
    turn_id,
    source_semantic_plan_hash,
    native_artifact_hash,
    translation_artifact_hash_or_absence_token,
    native_language_ref,
    native_locale_ref,
    translation_requirement,
    translation_language_ref,
    translation_locale_ref,
    translation_rule_id,
    translation_rule_version,
    translation_rule_hash,
    native_render_receipt_hash,
    translation_render_or_transform_receipt_hash_or_absence_token
  })
)
```

Then the equivalence receipt references `pair_basis_hash`.

Final pair artifact identity is:

```text
pair_hash = SHA256(
  "rawlsing:v2:native-translation-pair:v1\n" || JCS({
    pair_basis_hash,
    equivalence_receipt_hash,
    pair_status
  })
)

pair_id = "v2ntpair:" + pair_hash
```

No circular hash dependency is permitted.

A later optional translation added to an earlier native-only artifact creates a **new pair record** referencing the same immutable native artifact; it does not mutate the earlier pair in place.

## 14. Translation rule / model / version receipt

Every translation surface must bind a receipt equivalent to:

```text
V2TranslationRuleReceipt {
  translation_rule_id,
  translation_rule_version,
  translation_rule_hash,
  source_semantic_plan_hash,
  native_artifact_ref,
  native_artifact_hash,
  source_language_ref,
  target_language_ref,
  source_locale_ref | null,
  target_locale_ref | null,
  adp025_model_binding_ref,
  adp025_render_request_or_transform_ref,
  prompt_or_transform_hash,
  sampling_profile_ref_if_model_based,
  provider_attempt_or_transform_receipt_ref,
  translation_artifact_ref,
  translation_artifact_hash,
  receipt_hash
}
```

CAN-023 does not select provider/model or sampling. ADP-025 remains sovereign over those identities.

A mutable model alias, hidden provider fallback, hidden prompt revision or unrecorded post-processing invalidates the translation receipt.

## 15. Contradiction preservation law

Contradiction is semantic content when the source plan preserves it.

If the source plan contains two or more incompatible/coexisting claims, perspectives or stances, translation must preserve their separate identity and conflict structure. It may not:

- average them;
- choose the apparently more reasonable one;
- merge them into a compromise;
- convert “sometimes P / sometimes not-P” into a stable middle position;
- resolve ambiguity by adding an explanation not in the source plan.

Exact contradiction-set refs in the native and translation alignment receipts must match the source plan. “More coherent translation” is semantic drift when coherence was purchased by deletion.

## 16. Epistemic non-upgrade law

For every protected claim/stance component:

```text
translation_epistemic_force == source_plan_epistemic_force
native_epistemic_force      == source_plan_epistemic_force
```

Examples of forbidden drift:

- `BELIEF` -> factual assertion;
- `UNCERTAINTY` -> confidence;
- explicit `NONKNOWLEDGE` -> guessed answer;
- qualified temporal claim -> timeless claim;
- “maybe”/“I think”/equivalent uncertainty marker -> omission when the uncertainty is plan-semantic;
- actor-inaccessible/withheld material -> explicit translated assertion.

A target language may express epistemic force through different grammar or lexical choices; the force itself must remain invariant.

## 17. Relationship / response-operation / boundary preservation

Translation may not change semantic plan refs for:

- response operation;
- relationship perspective or expression constraint;
- boundary/limit/exit scope;
- selected/withheld targets;
- actor/counterpart referents.

A translation cannot become more intimate, deferential, hostile, affectionate, formal, challenging or conciliatory merely because such a style is culturally plausible, unless the source plan already authorizes that meaning/register variation.

An honorific or kinship term that carries relationship meaning is not a free cultural decoration. If target-language grammar requires a socially meaningful choice that the source plan does not authorize, the equivalence result is `EQUIVALENCE_UNRESOLVED` unless a lawful neutral strategy exists.

## 18. Causal-publication exclusion

CAN-023 does not decide which surface, if any, becomes part of an external-event candidate or causal interaction.

It may record exact artifact/surface identities so later CAN-024/CAN-025 and V3 admission can refer to them, but:

```text
SEMANTICALLY_EQUIVALENT_PAIR
!= INTERACTION_MODE
!= EXTERNAL_EVENT_PACKAGE
!= V3_ADMISSION
!= CAUSAL_OCCURRENCE
```

Translation equivalence cannot transfer admission between artifacts. A later causal-publishing authority must bind the exact artifact/surface/hash it intends to package.

## 19. Replay / provenance

CAN-023 semantic evaluation is deterministic **given exact stored artifacts, plan, rule versions and evaluator receipts**.

Replay identity preserves:

- source semantic-plan ID/hash;
- native artifact/hash and ADP-025 receipt;
- translation artifact/hash or explicit absence/failure token;
- exact native/translation language and locale refs;
- translation requirement;
- translation rule ID/version/hash;
- model/transform receipt refs;
- equivalence profile ID/version/hash;
- surface alignment receipt hashes;
- evaluator binding/version/prompt/hash where applicable;
- drift/unresolved refs;
- pair-basis hash;
- equivalence-receipt hash;
- final pair hash/status.

Forbidden replay entropy:

- mutable `latest` translation/model;
- hidden wall clock;
- filesystem/dict/list ordering;
- unrecorded language detection;
- provider defaults;
- embedding service changes;
- unversioned LLM equivalence judgment;
- transcript rescanning;
- culturally plausible rewrite;
- prior displayed translation as semantic authority.

Exact replay uses stored artifacts and receipts. Provider regeneration is never required to prove the historical pair. Historical model/evaluator **diagnostic** receipts may be preserved and replayed exactly, but immutability or reproducibility does not retroactively promote a model judgment into semantic-adjudication authority. A historical positive semantic receipt is valid only if its own recorded evaluator authority ID/version/hash and admissible-operation contract were lawful for that adjudication.

A new translation attempt, new governed evaluator authority/version, changed diagnostic model/evaluator version, changed locale, changed semantic plan, changed native artifact or changed translation artifact creates a new immutable pair/equivalence identity. Historical records remain unchanged.

## 20. Valid-empty / missing / deferred / integrity law

CAN-023 distinguishes lawful absence from failure.

- `TRANSLATION_NOT_REQUESTED` is lawful native-only, not missing data.
- optional translation absence is a lawful degraded pair state, not native invalidity.
- required translation absence is incomplete delivery, not permission to substitute.
- missing semantic-plan hash is `DEFERRED_MISSING_SEMANTIC_PLAN_AUTHORITY`.
- missing native artifact is `NATIVE_REQUIRED_MISSING_OR_FAILED`.
- missing translation-rule/model receipt for a present translation is `INTEGRITY_FAILURE_ARTIFACT_OR_RECEIPT`.
- missing exact evaluator semantic authority for a material comparison is `MISSING_PLAN_ALIGNMENT_AUTHORITY`; when the material comparison therefore cannot be established, pair/surface equivalence is also `EQUIVALENCE_UNRESOLVED` as applicable; never “probably equivalent.”
- wrong plan hash is `INTEGRITY_FAILURE_PLAN_MISMATCH`.
- a valid pair may contain zero translation artifact only when requirement is `NOT_REQUESTED` or `OPTIONAL`.

No `UNKNOWN`, missing or deferred state becomes a semantic guess.

## 21. Forbidden inference / shortcut registry

CAN-023 explicitly forbids:

1. translation text creating a new actor fact;
2. native text creating a new actor fact beyond the source plan;
3. “native language” role implying actor ethnicity/nationality/identity;
4. target-language cultural convention creating biography;
5. word count similarity as equivalence;
6. embedding/cosine similarity threshold as equivalence;
7. LLM confidence threshold as equivalence;
8. translator self-certification as equivalence;
9. missing translation replaced with native;
10. missing native replaced with translation;
11. contradiction smoothing;
12. uncertainty deletion;
13. belief-to-fact upgrade;
14. relationship-tone drift;
15. operation drift;
16. honorific/kinship invention beyond source meaning;
17. target language inferred from actor geography/demography;
18. user language detection used as biography;
19. prior translation text used to widen future actor access;
20. translation/session persistence treated as causal memory;
21. equivalent wording treated as causal admission;
22. one admitted surface transferring admission to its pair-mate;
23. same visible text implying same artifact/pair identity;
24. silent post-processing without version/hash provenance;
25. pinned/replayable LLM judgment treated as evaluator semantic authority;
26. model-produced complete-looking atom mapping treated as proof without separately governed evaluator authority;
27. immutable historical model diagnostic receipt promoted retrospectively into semantic authority.

## 22. Hostile fixtures

| ID | Attack | Required result |
|---|---|---|
| H01 | translation changes “I think P” to “P” | `SEMANTIC_DRIFT_DETECTED`; reject translation |
| H02 | translation drops explicit uncertainty | drift; reject translation |
| H03 | translation turns explicit nonknowledge into plausible answer | drift; reject translation |
| H04 | translation resolves two contradictory beliefs into one compromise | drift; contradiction refs mismatch |
| H05 | translation keeps one of two contradictory claims and drops the other | drift; removed semantic atom |
| H06 | translation changes relationship posture/intimacy meaning | drift; reject translation |
| H07 | translation changes `ENGAGE_SELECTIVE` to a refusal/exit semantic | operation drift; reject translation |
| H08 | translation changes boundary-limited target into whole-turn exit | scope/operation drift |
| H09 | optional translation absent | native valid; `NATIVE_VALID_TRANSLATION_OPTIONAL_MISSING` |
| H10 | optional translation provider fails before output | native valid; `...OPTIONAL_FAILED` |
| H11 | required translation absent | native remains valid; pair `TRANSLATION_REQUIRED_MISSING` |
| H12 | required translation operational failure | native remains valid; pair `TRANSLATION_REQUIRED_FAILED` |
| H13 | recovered parser substitutes native text for missing translation | reject substitution; typed missing state |
| H14 | native missing, translation present | `NATIVE_REQUIRED_MISSING_OR_FAILED`; no substitution |
| H15 | translation and native bind different semantic-plan hashes | `INTEGRITY_FAILURE_PLAN_MISMATCH` |
| H16 | translation adds culturally plausible hometown detail | drift; biography invention |
| H17 | translation infers religion-specific idiom from country | forbidden inference unless plan-authorized surface register already supplies it |
| H18 | translation adds honorific implying intimacy/status not in plan | drift or unresolved |
| H19 | target language requires socially meaningful form not authorized and no neutral strategy is governed | `EQUIVALENCE_UNRESOLVED` |
| H20 | idiomatic syntax changes but claim/ref/polarity/force unchanged | allowed surface variation |
| H21 | discourse filler omitted with no protected semantic effect | allowed surface variation |
| H22 | punctuation/sentence segmentation differs | allowed unless plan marks ordering/contrast material |
| H23 | embedding similarity 0.99 but uncertainty removed | reject; score cannot override invariant failure |
| H24 | LLM says 98% equivalent but one referent changed | reject |
| H25 | LLM evaluator cannot resolve whether a modal changed | `EQUIVALENCE_UNRESOLVED` |
| H26 | translation provider labels itself `equivalent=true` | no authority |
| H27 | DRAFT one-liner native + fuller translation | compatibility input only; cannot pass without same-plan alignment proof |
| H28 | embedded quote/gloss format loses nonquoted semantic material | drift/unresolved; not canonical by parser shape |
| H29 | translation artifact present with missing model/transform receipt | integrity failure |
| H30 | hidden postprocessor modifies translation bytes | integrity failure unless transform is versioned/hashed |
| H31 | pair replay with same artifacts/rules/receipts | identical pair/equivalence hashes |
| H32 | optional translation later generated | new immutable pair referencing same native; old native-only pair remains |
| H33 | translation regenerated after drift | new translation artifact and new pair; old drifted pair immutable |
| H34 | equivalence evaluator version changes | new equivalence receipt/pair identity; no in-place rewrite |
| H35 | translation language/locale changes | new pair identity |
| H36 | native rerender produces same visible text but new ADP-025 candidate identity | new pair identity; visible text equality insufficient |
| H37 | translation visible text equals native across nominally different languages | no automatic pass/fail; evaluate semantics and language receipt |
| H38 | target language inferred from user's country | reject; no geography->language authority |
| H39 | user-language detector used to claim actor language identity | reject biography inference |
| H40 | high session repetition of translation makes it actor memory | reject |
| H41 | translation introduces analyst-known objective fact absent from plan | drift; reject |
| H42 | translation makes hidden/inaccessible claim explicit | drift/access violation evidence; reject |
| H43 | translation adds causal-status wording/metadata | reject; CAN-023 cannot alter interaction status |
| H44 | native artifact admitted causally elsewhere, translation equivalent | admission does not transfer to translation |
| H45 | translation artifact admitted causally elsewhere, native equivalent | admission does not transfer to native |
| H46 | optional translation drifted | native can still display; translation quarantined |
| H47 | required translation drifted | native remains valid, delivery incomplete |
| H48 | no semantic-plan hash | defer; no equivalence guess |
| H49 | fully pinned LLM evaluator returns `equivalent=true`, but no separately accepted evaluator authority exists | `MISSING_PLAN_ALIGNMENT_AUTHORITY` / `EQUIVALENCE_UNRESOLVED`; no `PLAN_CONFORMANT`, no semantic pass |
| H50 | model emits apparently complete protected-atom alignment, but evaluator authority is absent | diagnostic evidence only; no positive semantic state |
| H51 | exact separately governed deterministic/rule-backed evaluator authority proves every protected invariant with zero unresolved material atoms | positive `PLAN_CONFORMANT` and, when both surfaces/pair gates pass, `SEMANTICALLY_EQUIVALENT` may lawfully issue |
| H52 | model diagnostic judgment conflicts with exact governed evaluator result | governed evaluator controls; model diagnostic cannot override |
| H53 | translation model lawfully generates target-language surface under ADP-025 | generation remains lawful; equivalence still requires independent governed CAN-023 evaluator court |

## 23. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

### Genuine ambiguity

The recovered implementation invites two lawful-looking terminal interpretations:

1. treat translation as a second freeform rendering whose acceptability can be judged by textual similarity, model confidence or culturally plausible paraphrase; or
2. treat native and translation as two surface realizations constrained by the same exact semantic plan, preserving contradiction, actor opacity, uncertainty and relationship/operation semantics, with lawful unresolved/failure states when equivalence cannot be established.

### Choice

CAN-023 chooses option 2.

### Governing-spirit tie-break

The choice preserves:

- downstream vividness never exceeding upstream authority;
- actor opacity and epistemic limits;
- contradiction/multiplicity without forced coherence;
- uncertainty and lawful absence without fabrication;
- mediation and cultural expression without culture becoming biography;
- minimum sufficient machinery;
- explicit provenance and replay;
- the law that LLM output is expression, not ontology.

The Governing Spirit supplied **no** actor language, translation, idiom, biography, relationship meaning, epistemic state, response operation, bilingual evaluator semantics or equivalence finding. It grants **no model semantic authority** and cannot convert model plausibility, confidence, reproducibility or diagnostic alignment into equivalence. It only resolves the architecture-compatible ambiguity in how translation failure/equivalence should be represented.

## 24. CONSUMER_RELEASE_SUFFICIENCY

Primary consumer: `V2-P8 — renderer / bilingual / replay audit`.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__CAN_023_SEMANTIC_BLOCKER_CLOSED_AFTER_VOZHD_ACCEPTANCE__V2_P8_REMAINS_SEPARATELY_GATED_BY_CAN_022_AND_IMPLEMENTATION_RELEASE_GATES`.

ADP-025 is already accepted and supplies model/render provenance. CAN-023 does not pre-adjudicate the same-cohort CAN-022 result. V2-P8 may be implemented only after every direct authority and release dependency is separately accepted.

## 25. Final token

`CAN_023_V2_NATIVE_TRANSLATION_EQUIVALENCE_CANONICALIZATION = PASS`
