# CAN-017 — V2 Expression Register / Disclosure-Surface Canonicalization

**Assignment:** `W1-B03-03`  
**RA-R00 item:** `CAN-017`  
**Authority:** `V2_EXPRESSION_REGISTER_RULE@1.0.0`  
**Registry:** `V2_EXPRESSION_REGISTER_REGISTRY@1.0.0`  
**Owner:** `V2_EXPRESSION_PLANNER`  
**Primary consumer:** `V2-P5`  
**Branch:** `agent/vozhd-dva-w1-can-017-v2-register`  
**Exact base:** `db961be677d5112073e16e5d452853971861cdb6`  
**Mode:** canonicalization only; no production code; no V2 implementation  
**Verdict:** `PASS`

## 1. Binding holding

```text
FIRST_PERSON_PERMISSION != EXPRESSION_REGISTER
ACCESSIBLE != SALIENT
SALIENT != REGISTER
REGISTER != RESPONSE_MOVE
REGISTER != PERSISTENT_PERSONALITY
REGISTER != V3_CAUSAL_STATE
RENDERER_OUTPUT != REGISTER_AUTHORITY
```

CAN-017 governs only a **turn/situation-scoped pre-render register/disclosure decision over already actor-permitted material already supplied to this boundary as an expression unit**.

Canonical operations are exactly:

- `NARROW_COMPONENT_SET` — retain an exact subset of already permitted claim components;
- `WITHHOLD_EXPRESSION_UNIT` — suppress an already permitted expression unit for this decision only;
- `APPLY_REGISTER_STYLE_CONSTRAINT` — attach an exact versioned, semantics-preserving style constraint.

Register never creates a claim, widens accessibility, raises an epistemic permission class, manufactures a persistent personality/voice, creates causal actor state, or lets the renderer/LLM choose its own semantic register.

Recovered V2 has a real pre-render register/voice function, but no clean terminal fixed taxonomy: most concrete descriptors are selected from now-forbidden demographic, structural, or legacy-psychological inputs. Therefore:

`V2_EXPRESSION_REGISTER_REGISTRY@1.0.0` =
`VALID_EMPTY_CONCRETE_STYLE_LABEL_SET__OPERATION_SCHEMA_CANONICAL`.

The operation/decision machinery is canonical; v1 freezes **zero concrete style/register labels**. A concrete style constraint exists only through an exact accepted/versioned rule entry. Lawful absence is `REGISTER_VALID_EMPTY`.

## 2. Authority basis and bounded dependencies

Required governing material was read at the exact launch base: Batch-03 register/common law; `CURRENT_STATE`; Governing Spirit; V2 and V3 completion rulings; whole-machine closure; implementation-release synthesis; W0 closure; W1 first-batch and Batch-02 adjudications; RA-R00; accepted TD-R06; and relevant accepted authorities/current recovery evidence.

Direct accepted boundaries consumed:

- `ADP-017 / V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0` — hard first-person claim-permission ceiling and ActorAccessibleRenderEnvelope;
- `ADP-026 / CALLER_CURRENT_SITUATION_AUTHORITY@1.0.0` — exact field-level current-situation refs may constrain presentation when an exact register rule declares them;
- `ADP-025 / V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY@1.0.0` — model/provider/randomness/render identity is separate and cannot select semantic register;
- accepted `CAN-008 / V3_ACTOR_RESPONSE_PRESSURE_FLOW_TRANSACTION_RULESET@1.0.0` — recovered expression-gating formulas/defaults are compatibility-only and surface-psyche material is not automatic render authority.

No same-Batch-03 return was used. `CAN-015`, `CAN-016`, `CAN-018`, `CAN-021`, and the active CAN-009 continuation remain nonauthoritative to this worker.

`V2-P5` independently remains blocked on `CAN-016`, `CAN-018`, `MUST-022`, and `MUST-023`.

## 3. Required archive verification

```text
archive          = Rawlsing_code_bundle_staging.zip
expected SHA256  = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
computed SHA256  = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
verdict          = EXACT_MATCH
entries          = 13,138
```

Recovered V2/V3/server source is continuity/authority-recovery evidence only. Historical V5/DDM has zero current V550+ authority.

Direct recovered sources and SHA256:

| source | SHA256 |
|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7` |
| `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135` |
| `v2/run_conversation_chat.py` | `b9276a4d7fc9dfdc83cc220528e4f16c1880d78419ed06430a5e9570a60efdc8` |
| `server/chat/turn.py` | `10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3` |
| `v3/io/persona_sheet.py` | `4a0009533443baef2786fc498c7f8db3ead7d133d8ee7e97e6d7128d4322a00e` |
| `v3/psyche/registers.py` | `2b493d819101c8d14492340bb785747bffe2e7a7998235916f2dd3ee5e3a766f` |
| `v3/core/state.py` | `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2` |
| `v3/engine/prompts.py` | `4702de20590579c3c4543dfa5139aa4a3ce6df47ed1aee2c92c800d5a3038d57` |
| `v3/engine/llm_contract.py` | `f024debf7b8a637e91c546689a0bed31baff55d98f1378b06cb82ebb4c0fe9cf` |
| `v3/tests/test_v5_voice_packet_surface_allowlist.py` | `f82f71334edf368a7f09c1f40d5a9d24367a8528b997f5bc40347043ec5a300b` |
| `v3/tests/test_v5_persona_sheet_surface_psyche.py` | `689beab6a72727f99c21db5485165278b1a8b346fc7daeda95dac677b37200c5` |
| `v3/tests/test_persona_sheet_integrity.py` | `dde6ddbb2a0b0cd3a1a1b9033818bac666eb69956f02ef3fa854516f20ab9825` |

Historical source court:

```text
python -m pytest -q   v3/tests/test_v5_voice_packet_surface_allowlist.py   v3/tests/test_v5_persona_sheet_surface_psyche.py   v3/tests/test_persona_sheet_integrity.py

4 passed
```

This proves recovered surface-allowlist/persona-sheet continuity only; it does not grant legacy register semantics.

## 4. Recovered register/disclosure inventory

| ID | recovered concept/vocabulary | disposition | terminal result |
|---|---|---|---|
| `HREG-01` | Register / VOICE SCHEMA | **ADAPT** | pre-render versioned decision; remove legacy source shortcuts |
| `HREG-02` | casual, young, spoken / measured more formal / spoken own register | **COMPATIBILITY_ONLY** | labels only; no age selector/default |
| `HREG-03` | direct, not polished / grounded in where they live | **REMOVE** | no class/SES/urbanicity/locality -> register |
| `HREG-04` | subculture/world reference shaping | **COMPATIBILITY_ONLY** | only exact separately authorized expression constraint may be consumed |
| `HREG-05` | devout/moderate/nominal + private/minimal/conflicted religious expressiveness | **REMOVE** | no religion/religiosity -> register/disclosure |
| `HREG-06` | class-consciousness / ideologically engaged/disengaged / ethnic-minority salience descriptors | **REMOVE** | epistemic/salience/demographic entanglement; not CAN-017 |
| `HREG-07` | cognitively constricted/guarded; no/glimpsed structural lens | **REMOVE** | legacy psyche/knowledge proxies not register authority |
| `HREG-08` | short sentences/fragments; speech_tics; quirks; rhythm | **COMPATIBILITY_ONLY** | only exact separately authorized actor-safe expression constraints; no persistent voice profile |
| `HREG-09` | REPLY_VOICE_SCHEMA_FALLBACK | **REMOVE** | no generic voice on missing authority |
| `HREG-10` | neutral/guarded/minimal/engaged turn tone | **COMPATIBILITY_ONLY** | response/boundary/effort/session seam; not register taxonomy |
| `HREG-11` | informal/neutral/formal message formality | **COMPATIBILITY_ONLY** | turn-analysis datum only if separately governed; not actor register |
| `HREG-12` | public_expression_gate / private_expression_gate | **ADAPT** | retain disclosure-narrowing function; replace persistent scalar gates with turn/situation decisions |
| `HREG-13` | inner_load | **REMOVE** | internal pressure is outside expression-register jurisdiction |
| `HREG-14` | 0..100 / default 50 / clamp | **COMPATIBILITY_ONLY** | no canonical magnitude/threshold/midpoint/clamp |
| `HREG-15` | felt_register incl. contained and compound label | **COMPATIBILITY_ONLY** | allowlist transport != semantic register/voice permission |
| `HREG-16` | public_private_inner_posture | **COMPATIBILITY_ONLY** | transport only; no persistent three-layer actor state |
| `HREG-17` | public_vs_private_register_obeyed | **ADAPT** | audit/validator receipt only |
| `HREG-18` | language 'registers of feeling' | **COMPATIBILITY_ONLY** | narrative phrase; no taxonomy |
| `HREG-19` | anti-assistant/professional/tourism-board tone rules | **COMPATIBILITY_ONLY** | render/prompt-policy seam, not CAN-017 |
| `HREG-20` | privacy / Interaction Context | **ADAPT** | only exact ADP-026 situation refs; no random/default Today State |
| `HREG-21` | renderer-not-decider ordering | **PRESERVE** | semantic register fixed before renderer; model cannot self-select |

Recovery therefore preserves the **pre-render decision ordering** and the **possibility of situation-dependent disclosure narrowing**, while rejecting the old route from demographics/legacy psyche directly to voice.

## 5. Jurisdiction

CAN-017 owns:

- registry/decision identity and versioning;
- exact turn/situation-scoped register constraints;
- narrowing/withholding over already permitted material;
- semantics-preserving style-constraint attachment;
- typed positive/empty/unknown/denied/deferred/forbidden/missing/ambiguous/integrity states;
- legacy compatibility disposition;
- register provenance/replay.

CAN-017 does not own:

- actor knowledge/belief/accessibility/first-person permission;
- salience or expression-candidate selection;
- response moves;
- uncertainty disclosure;
- relationship expression;
- boundary/face-risk/effort/attention;
- session EnergeticField;
- render model/provider/randomness/prompt policy;
- persistent actor voice/personality;
- V3 biography, memory, relationship truth, or causal state.

## 6. Input authority

Admissible typed references:

- `ACTOR_ACCESSIBLE_RENDER_ENVELOPE_REF`;
- `CLAIM_PERMISSION_RECORD_REF`;
- `ALREADY_SELECTED_EXPRESSION_UNIT_REF`;
- `EXACT_CALLER_CURRENT_SITUATION_STATEMENT_REF_WHEN_RULE_DECLARED`;
- `EXACT_SEPARATELY_ACCEPTED_ACTOR_SAFE_EXPRESSION_CONSTRAINT_REF`;
- `REGISTER_REQUIREMENT_REF_WHEN_EXPLICIT`;
- `TURN_SESSION_CURSOR_IDENTITY_REF_FOR_SCOPE_ONLY`.

Current-situation examples that a concrete exact rule may declare include ADP-026 `situation.current_privacy`, `interaction.channel`, and `interaction.mode_context`.

Forbidden as semantic register authority:

- class/SES, religion/religiosity, nationality/country/ethnicity/minority;
- age/urbanicity/locality as direct selectors;
- structural/historical/V558/V550+ material;
- DRTS/IAI/RMT;
- legacy aperture/structural-lucidity/wound/need scores;
- raw V3 register values or `surface_psyche` labels without separate accepted authority;
- inaccessible/analyst-only truth;
- transcript/prior rendered prose;
- LLM/model output;
- same-batch sibling results.

A current location, demographic identity, historical backdrop, device, session association, or prior prose cannot silently become register.

## 7. Claim-permission ceiling

Allowed upstream permission classes are only:

- `PERMIT_FIRST_PERSON_KNOWLEDGE`;
- `PERMIT_FIRST_PERSON_BELIEF`;
- `PERMIT_FIRST_PERSON_UNCERTAINTY`;
- `PERMIT_FIRST_PERSON_NONKNOWLEDGE`.

`DENY_FIRST_PERSON_CLAIM` remains denied. `DEFER_MISSING_AUTHORITY` remains deferred.

CAN-017 may preserve/narrow `permitted_component_refs` or withhold the expression unit. It may never add components or upgrade:

```text
BELIEF -> KNOWLEDGE
UNCERTAINTY -> BELIEF/KNOWLEDGE
NONKNOWLEDGE -> GUESS
PARTIAL_ACCESS -> WHOLE_CLAIM_ACCESS
```

Private/intimate context does not widen inaccessible memory. Two permitted claims do not authorize inferred claim C. A style constraint that changes semantic permission class is invalid.

## 8. Registry and decision contract

A rule entry is equivalent to:

```text
V2ExpressionRegisterRuleEntry@1.0.0 {
  register_rule_id,
  register_rule_version,
  register_rule_hash,
  admissible_input_classes[],
  required_predicate_refs[],
  allowed_operations[],
  style_constraint_schema_refs[],
  situation_scope,
  conflict_law,
  provenance_refs[]
}
```

Rule matching is `EXACT_TYPED_PREDICATES_ONLY`. Free-text semantic matching, demographic lookup, a numeric “best register” score, enumeration-order selection, and LLM preference are forbidden.

If incompatible exact rules match without governed precedence/coexistence:

`REGISTER_AMBIGUOUS_RULE_MATCH`.

A decision is equivalent to:

```text
V2ExpressionRegisterDecision@1.0.0 {
  register_decision_id,
  actor_id,
  turn_id,
  situation_snapshot_refs[],
  authority/registry IDs + versions + hashes,
  input_expression_unit_refs[],
  claim_permission_record_refs[],
  matched_rule_refs[],
  operations[],
  style_constraint_refs[],
  decision_state,
  input_state_hash,
  provenance_refs[],
  decision_hash
}
```

The decision contains no actor `voice_profile`, public/private/inner personality layers, demographic register, religious voice, ideological voice, or causal mutation.

## 9. State law

- `REGISTER_APPLIED` — at least one exact registered operation is bound.
- `REGISTER_VALID_EMPTY` — lawful evaluation; no modulation applies; emit no style filler.
- `REGISTER_INPUT_UNKNOWN` — required situation/expression input is unknown, contradicted, or stale.
- `REGISTER_UPSTREAM_PERMISSION_DENIED` — input content is inaccessible/denied.
- `REGISTER_UPSTREAM_PERMISSION_DEFERRED` — upstream permission is deferred/missing.
- `REGISTER_FORBIDDEN_SOURCE` — forbidden source/selector supplied.
- `REGISTER_MISSING_AUTHORITY` — an explicitly required rule/style authority is unavailable or unversioned.
- `REGISTER_AMBIGUOUS_RULE_MATCH` — incompatible rules lack lawful precedence/coexistence.
- `REGISTER_INTEGRITY_FAILURE` — schema/hash/provenance/permission-subset invariant fails.

### Valid-empty versus missing

No explicit register requirement + no applicable registered modulation may yield `REGISTER_VALID_EMPTY`. Renderer gets **no CAN-017 style instruction**.

If an exact required rule/style authority is unavailable, return `REGISTER_MISSING_AUTHORITY`.

Neither state may default to `spoken, their own register`, `neutral`, or any generic personality voice.

Unknown privacy is not public. Missing register is not neutral.

## 10. Turn/situation variation

Register is noncausal and scoped to an exact turn or expression unit plus exact situation refs.

The same actor may lawfully receive different register decisions on later turns. Prior decisions are immutable audit history only; they do not rewrite actor identity or become persistent V2 personality/V3 state.

Public/private-style variation requires exact current-situation authority. If a required ADP-026 privacy/context field is `UNKNOWN`, contradicted, stale, or expired, return `REGISTER_INPUT_UNKNOWN`; never infer it from location/demographics/transcript.

Contradictory accessible materials remain contradictory. Separate expression units may receive separate lawful constraints; CAN-017 cannot synthesize one coherent position or scalar winner.

## 11. Numeric/default disposition

```text
canonical register scale     = NONE
canonical thresholds         = NONE
canonical weights            = NONE
canonical neutral midpoint   = NONE
canonical default voice      = NONE
CAN-017 RNG operations       = NONE
```

Recovered public/private/inner `0..100`, default `50`, and clamp behavior are compatibility/migration evidence only. `inner_load` is outside CAN-017 semantics.

No default is inherited from:

- `REPLY_VOICE_SCHEMA_FALLBACK`;
- `neutral`;
- “short sentences; fragments OK”;
- model/provider defaults;
- demographic “most likely” voice;
- prior rendered style.

ADP-025 render randomness may vary surface wording inside an already-fixed CAN-017 decision; it cannot change register semantics.

## 12. Replay/provenance

```text
hash                  = SHA-256
structured encoding   = RFC 8785 JCS / UTF-8
decision ID           = v2reg:<domain-separated SHA-256>
```

Identity includes authority/registry hashes, actor+turn, expression-unit hashes, ADP-017 permission hashes/component sets, consumed ADP-026 situation statement hashes/effective scopes, matched rule/style-constraint hashes, operations, and `input_state_hash`.

Excluded: hidden wall clock, filesystem order, mutable `latest`, LLM/model output, render RNG, prior rendered wording, unversioned prose labels.

Same exact inputs require the same semantic register decision. Changed permission/rule/situation/expression identity creates a new decision.

## 13. Hostile fixtures

| fixture | case | required result |
|---|---|---|
| `CAN017-HF01` | forbidden claim + style | `UPSTREAM_PERMISSION_DENIED` |
| `CAN017-HF02` | inaccessible memory + private situation | `UPSTREAM_PERMISSION_DENIED; privacy cannot widen` |
| `CAN017-HF03` | BELIEF permission + style | `permission remains BELIEF` |
| `CAN017-HF04` | class/religion/nationality/history direct selector | `FORBIDDEN_SOURCE` |
| `CAN017-HF05` | same actor public then private exact situations | `different turn decisions lawful; no actor mutation` |
| `CAN017-HF06` | contradictory accessible beliefs | `preserve both; no synthesis` |
| `CAN017-HF07` | explicit required rule missing | `MISSING_AUTHORITY; no fallback` |
| `CAN017-HF08` | no requirement/no applicable modulation | `VALID_EMPTY; no filler voice` |
| `CAN017-HF09` | LLM proposes register | `reject/ignore semantic register change` |
| `CAN017-HF10` | legacy 20/80/50 gates | `compatibility-only; no numeric decision` |
| `CAN017-HF11` | felt_register=contained only | `not authority` |
| `CAN017-HF12` | two incompatible rules/no precedence | `AMBIGUOUS_RULE_MATCH` |
| `CAN017-HF13` | partial permission -> whole claim attempt | `INTEGRITY_FAILURE` |
| `CAN017-HF14` | prior rendered style as next-turn evidence | `FORBIDDEN_SOURCE` |
| `CAN017-HF15` | required privacy UNKNOWN/contradicted/stale | `INPUT_UNKNOWN` |
| `CAN017-HF16` | style changes uncertainty to fact | `INTEGRITY_FAILURE` |
| `CAN017-HF17` | model temperature/rerender changes output | `CAN-017 decision unchanged` |

**Hostile fixture verdict:** `PASS_BY_CONTRACT_INSPECTION`.

## 14. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

After the unlawful legacy source shortcuts were removed, one genuine representational choice remained:

1. freeze `PUBLIC/PRIVATE/INNER` as a fixed turn-scoped presentation-surface enum; or
2. use non-taxonomic exact turn-scoped constraint decisions over separately authoritative situation refs.

CAN-017 chooses (2), preserving the historical disclosure function without creating persistent layers or unsupported categories.

Tie-break principles: dynamic history over static classification; contradiction/multiplicity; lawful absence; minimum sufficient machinery; no downstream vividness beyond authority.

The Governing Spirit supplied no register label, demographic mapping, psychology, number, claim permission, or desired voice.

## 15. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT_FOR_CAN017_BLOCKER`

CAN-017 now supplies the complete V2-P5 register/disclosure machine boundary. It does **not** independently release V2-P5 or production V2. Remaining direct blockers:

`CAN-016`, `CAN-018`, `MUST-022`, `MUST-023`.

## 16. Scope confirmation

Exactly two authority files only. No production implementation or code/test edits. No same-Batch-03 result used. No new register taxonomy. No persistent personality, biography, causal state, or knowledge. No ownership of salience, response moves, relationship expression, boundary/face-risk/effort/attention, session EnergeticField, or render/model policy.

## 17. Final token

`CAN_017_V2_EXPRESSION_REGISTER_CANONICALIZATION = PASS`
