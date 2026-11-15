# ADP-022 — V2 Uncertainty Disclosure Authority

**Assignment:** W2-04  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w2-adp-022-v2-uncertainty-disclosure`  
**Exact base:** `fe52ca60ed00650b0a7b5bf77bab8ac40d53f4d8`  
**RA-R00 item:** `MUST-022 / ADP-022`  
**Authority:** `V2_UNCERTAINTY_DISCLOSURE_RULE@1.0.0`  
**Owner:** `V2_EXPRESSION_PLANNER`  
**Consumers:** `V2-P2`, `V2-P5`  
**Direct dependency:** `ADP-017 / V3_ACTOR_KNOWLEDGE_ACCESSIBILITY_RULE@1.0.0`  
**Downstream membrane:** `CAN-018 / V2_RESPONSE_MOVE_RULE@1.0.0`  
**Mode:** authority creation only; no production code; no V2 implementation  
**Verdict:** `PASS`

## 1. Binding holding

ADP-022 governs only turn-local, noncausal V2 disclosure semantics over exact actor-safe epistemic permissions already supplied by ADP-017.

```text
objective generated truth
!= actor epistemic stance
!= current accessibility
!= ADP-017 first-person permission
!= ADP-022 disclosure decision
!= CAN-017 register
!= CAN-018 response operation
!= renderer wording
!= causal occurrence
```

ADP-017 is the **hard epistemic ceiling**. For every admitted disclosure:

```text
output_claim_ref == exact ADP-017 claim_ref
output_component_refs ⊆ ADP-017 permitted_component_refs
output_epistemic_class is licensed by the exact source permission
```

ADP-022 may preserve or narrow; it may not create or upgrade knowledge, belief, uncertainty, nonknowledge, accessibility, claim identity, or first-person permission.

Therefore:

```text
SYSTEM_UNKNOWN != ACTOR_UNCERTAINTY
SYSTEM_UNKNOWN != ACTOR_NONKNOWLEDGE
NO_KNOWLEDGE_RECORD != POSITIVE_NONKNOWLEDGE
BELIEF != KNOWLEDGE
UNCERTAINTY != FACT
DENIED/DEFERRED != "I don't know"
RENDERER_HEDGE != ACTOR_UNCERTAINTY
```

Accessible material does not have to be disclosed. `WITHHOLD` and `DISCLOSURE_VALID_EMPTY` are lawful.

## 2. Authority basis and jurisdiction

Read at the exact base: W2 common law and W2-04; `CURRENT_STATE.md`; `RAWLSING_GOVERNING_SPIRIT.md`; `TERMINAL_DEMAND_ENVELOPE.md`; `ARCHITECTURE_PASS_LAW.md`; whole-machine, V2-completion, implementation-release, W0 and W1 closure rulings; RA-R00 result; accepted ADP-017; accepted CAN-018. No sibling W2 result was used.

ADP-022 owns:
- validation of proposed disclosure against exact ADP-017 permission;
- semantic classes for lawful knowledge, belief, uncertainty, positive nonknowledge, and zero-output withholding;
- exact uncertainty-specific CAN-018 registrations where both semantic scope and activation law are available;
- contradiction-preserving disclosure law;
- typed missing/deferred/denied/valid-empty/noncomparable/integrity outcomes;
- replay/provenance and historical compatibility disposition.

ADP-022 does not own:
- formation of actor epistemic state or accessibility;
- phenomenological projection or salience;
- CAN-017 register/style/withholding semantics;
- ADP-023 boundary, face-risk, effort, attention, privacy or refusal semantics;
- relationship/attractor/session/transcript semantics;
- renderer wording, prompt/model/RNG;
- generic question asking or generic refusal;
- numeric confidence or hedge thresholds;
- causal occurrence.

## 3. Historical source verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

```text
expected SHA256 = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
computed SHA256 = 953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
verdict         = EXACT_MATCH
entries         = 13,138
```

Recovered V3/V2/server material is continuity/authority-recovery evidence only; historical V5/DDM has zero current authority.

Direct evidence:

| source | SHA256 | finding / disposition |
|---|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | `0b0ee1d5e177b22236007ddb15053e4f1d3fc34f69aae8b44e16446def9250d7` | preserves uncertainty/ignorance as first-class intent; rejects recovered `knowledge_confidence(topic) 0..1` as terminal authority |
| `v2/conversation_engine.py` | `766bee296379f0faadbede55106bcee0123e9563c965d0e28f8806cedea06135` | preserves pre-render ordering; rejects `hook_confidence < 0.5 -> tentative uptake` as actor epistemics |
| `v2/additions.txt` | `6040500c2b8a80cd82f2c131126246db46fae782ec0f7e27c20133e776b83d87` | qualitative uncertainty/ignorance continuity; score/source-label mechanics compatibility only |
| `v2/additions_convo.txt` | `efe037af79554ebecd0aa67cb852dcfc4b094367650d9cf48f24ca1fc8cf6ec5` | hedge/ask/deflect examples are examples only; topic/persona hedge heuristics rejected |
| `v2/PIPELINE_WIRING_AUDIT.md` | `fabbf700ec6e83aae4a59266a58833871f6205655f022311865eb62381dbebe4` | pre-render placement continuity |
| `v2/run_conversation_chat.py` | `b9276a4d7fc9dfdc83cc220528e4f16c1880d78419ed06430a5e9570a60efdc8` | runtime unknown placeholders are not actor nonknowledge |
| `server/chat/turn.py` | `10e7f02333dac36b4baddd455b3655685413ed41a88d12a375b1cee9be9394b3` | operational status only |
| `server/session_state.py` | `9c9c3b0e2b3bff700af127e03805166102920019d6acd099ee8270fbe63bc15a` | `LEGACY_UNKNOWN` is not actor epistemic state |
| `server/session_db.py` | `0d9bf508aa748ce8eff3360a7c615ab0ed086f3a34c3190815cb0485fe234c12` | persistence is not epistemic authority |
| `tests/test_chat_integrity.py` | `efcb4ad8c65bd1fc7a4522160a9543654da159e6381819ef6b4089044ec3b9c2` | integrity/no-invention continuity |

Focused recovered court:

```text
PYTHONPATH=. pytest -q tests/test_chat_integrity.py
11 passed in 0.20s
```

Passing historical tests do not promote recovered confidence, hedge, default, or move semantics.

## 4. Recovered disposition court

| recovered mechanism | disposition |
|---|---|
| uncertainty/ignorance as first-class V2 concern | `PRESERVE_ADAPT`: consume exact ADP-017 states only |
| renderer-not-decider ordering | `PRESERVE` |
| natural phrases such as “I'm not sure” / “I only saw clips” | `COMPATIBILITY_ONLY`: wording examples |
| `knowledge_confidence(topic) 0..1` | `REMOVE_REJECT` |
| `source_of_knowledge` labels | `COMPATIBILITY_ONLY`; exact ADP-017 basis/acquisition refs remain sovereign |
| hedge rate correlated with low confidence | `REMOVE_REJECT` |
| `hook_confidence < 0.5` tentative uptake | `REMOVE_REJECT_AS_EPISTEMIC_AUTHORITY` |
| political/topic/persona hedge rules | `REMOVE_REJECT` |
| generic ask/deflect/defer labels | `COMPATIBILITY_ONLY`; no activation force |
| boundary hit -> soften/deflect/go vague | `OUT_OF_SCOPE`; ADP-023/CAN-017 |
| transcript wording as actor-state evidence | `REMOVE_REJECT` |
| system `Unknown` / `LEGACY_UNKNOWN` | `REMOVE_REJECT_AS_ACTOR_STATE` |
| LLM-generated hedge/hesitation | `REMOVE_REJECT_AS_DECISION_AUTHORITY` |
| default “I don't know” on missing data | `REMOVE_REJECT` |
| generic hedge on incomplete source | `REMOVE_REJECT` |

## 5. ADP-017 ceiling proof and permission map

ADP-022 accepts only these exact ADP-017 permission classes:

```text
PERMIT_FIRST_PERSON_KNOWLEDGE
PERMIT_FIRST_PERSON_BELIEF
PERMIT_FIRST_PERSON_UNCERTAINTY
PERMIT_FIRST_PERSON_NONKNOWLEDGE
DENY_FIRST_PERSON_CLAIM
DEFER_MISSING_AUTHORITY
```

V1 mapping:

| source permission | lawful ADP-022 semantics | forbidden promotion |
|---|---|---|
| `PERMIT_FIRST_PERSON_KNOWLEDGE` | `ASSERT_KNOWLEDGE`, `WITHHOLD` | cannot fabricate uncertainty/nonknowledge |
| `PERMIT_FIRST_PERSON_BELIEF` | `ASSERT_BELIEF`, `WITHHOLD` | cannot become bare fact/knowledge |
| `PERMIT_FIRST_PERSON_UNCERTAINTY` | `QUALIFY_UNCERTAINTY`, `WITHHOLD` | cannot become belief/knowledge/fact without separate permission |
| `PERMIT_FIRST_PERSON_NONKNOWLEDGE` | `STATE_EXPLICIT_NONKNOWLEDGE`, `WITHHOLD` | cannot guess/assert answer without separate permission |
| `DENY_FIRST_PERSON_CLAIM` | zero disclosure | cannot become an ignorance claim |
| `DEFER_MISSING_AUTHORITY` | typed defer / zero disclosure | no hedge or ignorance fallback |

For uncertainty/nonknowledge, an epistemic-gap question or epistemic decline would require the matching permission as a **necessary** condition, but ADP-017 does not choose that communicative act. V1 therefore does not register `ASK_FROM_EPISTEMIC_GAP` or `DECLINE_EPISTEMIC_COMMITMENT`.

This proves the ceiling: every ADP-022 positive semantic class is either the same class as its exact ADP-017 permission or a zero-output narrowing. There is no upward edge.

## 6. Canonical request / decision contract

```text
V2UncertaintyDisclosureRequest@1.0.0 {
  request_id,
  actor_id,
  turn_id,
  exact_turn_artifact_ref/hash,
  source_actor_envelope_ref/hash,
  source_claim_ref,
  source_permission_record_refs[],
  source_permitted_component_refs[],
  source_stance_record_refs[],
  source_contradiction_refs[],
  proposed_disclosure_operation_id?,
  proposed_target_component_refs[],
  proposed_premise_claim_refs[],
  requested_can018_operation_id?,
  provenance_refs[],
  request_hash
}

V2UncertaintyDisclosureDecision@1.0.0 {
  decision_id,
  request_id,
  actor_id,
  turn_id,
  authority_id/version/hash,
  source_actor_envelope_ref/hash,
  source_permission_record_refs[],
  source_stance_record_refs[],
  source_contradiction_refs[],
  exact_claim_ref,
  admitted_component_refs[],
  disclosure_operation_id?,
  disclosure_semantic_class?,
  required_epistemic_constraints[],
  forbidden_semantic_promotions[],
  can018_operation_registration_ref?,
  decision_state,
  no_output_reason?,
  input_state_hash,
  provenance_refs[],
  decision_hash,
  integrity_state
}
```

The request may propose an operation, but a proposal has zero activation authority. The decision is noncausal V2 planning state and cannot prove that the actor actually spoke.

Decision states:

```text
DISCLOSURE_ADMITTED
DISCLOSURE_WITHHELD
DISCLOSURE_VALID_EMPTY
DISCLOSURE_UPSTREAM_PERMISSION_DENIED
DISCLOSURE_UPSTREAM_PERMISSION_DEFERRED
DISCLOSURE_MISSING_AUTHORITY
DISCLOSURE_FORBIDDEN_PROMOTION
DISCLOSURE_NONCOMPARABLE_OR_AMBIGUOUS
DISCLOSURE_INTEGRITY_FAILURE
```

## 7. Disclosure operations and CAN-018 registration

`V2_UNCERTAINTY_DISCLOSURE_OPERATION_REGISTRY@1.0.0`:

### `ASSERT_KNOWLEDGE`
Requires exact matching knowledge permission and component subset. Uses existing CAN-018 `ENGAGE_SELECTIVE`; no special registration.

### `ASSERT_BELIEF`
Requires exact matching belief permission; rendering must preserve belief rather than fact. Uses `ENGAGE_SELECTIVE`; no special registration.

### `QUALIFY_UNCERTAINTY`
Semantic scope: disclose the exact actor-safe uncertainty state for the exact claim/scope, not decorative hedge style.

Exact activation:
1. V2 is already attempting to disclose an exact actor-safe target for this turn; permission existence alone does not force disclosure.
2. Target carries exact matching `PERMIT_FIRST_PERSON_UNCERTAINTY` and permitted components.
3. Source envelope/hash verifies.
4. Any affirmative proposition included alongside uncertainty has its own exact belief/knowledge permission.
5. Missing system data, analyst disagreement, low hook confidence, topic, hedge wording, model hesitation and LLM choice are forbidden activators.

CAN-018 special registration: **YES**, `QUALIFY_UNCERTAINTY`, owner `ADP-022@1.0.0`.

### `STATE_EXPLICIT_NONKNOWLEDGE`
Semantic scope: disclose positive actor nonknowledge about the exact claim/scope without asserting or guessing the answer.

Exact activation:
1. V2 is already attempting to disclose an exact actor-safe target; nonknowledge existence alone does not force disclosure.
2. Target carries exact matching `PERMIT_FIRST_PERSON_NONKNOWLEDGE`.
3. Source envelope/hash verifies.
4. System missingness, denied/deferred access, absent stance, operational `Unknown`, and `EPISTEMIC_STATE_UNKNOWN` are forbidden substitutes.
5. Guess/answer requires separate exact permission.

CAN-018 special registration: **YES**, `STATE_EXPLICIT_NONKNOWLEDGE`, owner `ADP-022@1.0.0`.

### `ASK_FROM_EPISTEMIC_GAP` — `NOT_REGISTERED_V1`
Matching uncertainty/nonknowledge and separately permitted premises would be necessary, but they do not establish that the actor should ask rather than qualify, state nonknowledge, withhold, or do nothing. A proposed question, question mark, generic curiosity, recovered `TEST_QUESTION`, LLM preference, or implementation choice is not an activation rule.

If requested now: `DISCLOSURE_MISSING_AUTHORITY`; CAN-018 `DEFERRED_REQUIRED_AUTHORITY`; zero special operation.

### `DECLINE_EPISTEMIC_COMMITMENT` — `NOT_REGISTERED_V1`
Matching uncertainty/nonknowledge is necessary but does not select declining rather than qualifying, stating nonknowledge, withholding, or valid-empty. Privacy/boundary/face-risk/effort/fatigue/discomfort remain ADP-023 territory.

If requested now without future exact response-purpose activation authority: `DISCLOSURE_MISSING_AUTHORITY`; CAN-018 `DEFERRED_REQUIRED_AUTHORITY`.

### `WITHHOLD`
Zero ADP-022 semantic output. Lawful voluntarily, and mandatory when a proposed disclosure exceeds the ADP-017 ceiling. It creates no motive and no implicit ignorance statement. It registers **no** CAN-018 special operation and does not absorb CAN-017 `WITHHOLD_EXPRESSION_UNIT`.

### CAN-018 registration result

Exactly two ADP-022 entries are authorized:

```text
QUALIFY_UNCERTAINTY
STATE_EXPLICIT_NONKNOWLEDGE
```

Each registration must bind operation ID/schema version, exact semantic scope, ADP-022 authority ID/version/hash, activation rule ID/version/hash, ADP-017 permission preconditions, forbidden activators, and immutable registration receipt/hash.

If both non-equivalent special operations would be required in one CAN-018 decision without accepted composition/precedence, preserve CAN-018 `DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES`; ADP-022 returns `DISCLOSURE_NONCOMPARABLE_OR_AMBIGUOUS`. No list order, score, RNG or LLM chooses.

Recovered `hedge`, `deflect`, `brief_or_deflect`, `test_question`, `defer`, `go_quiet`, `answer_one_detail_plus_ask`, etc. receive zero registration authority.

## 8. Contradiction and positive nonknowledge

ADP-017 may lawfully supply contradictory/coexisting records such as:

```text
BELIEF(P) + BELIEF(not-P)
BELIEF(P) + UNCERTAINTY(P)
```

ADP-022 never chooses the “real” belief, averages stances, turns contradiction into uncertainty, or synthesizes “I am conflicted” without an independently permitted meta-claim. Separate lawful units retain separate permission refs.

A composite that requires collapsing incompatible permissions into one class returns `DISCLOSURE_NONCOMPARABLE_OR_AMBIGUOUS`. If belief(P) and uncertainty(P) are both disclosed, the proposition needs belief permission and the uncertainty qualification needs uncertainty permission; neither supplies the other.

Positive nonknowledge law:

```text
NO KNOWLEDGE RECORD != NONKNOWLEDGE
SYSTEM CANNOT DETERMINE P != ACTOR KNOWS THEY DO NOT KNOW P
CLAIM DENIED TO V2 != ACTOR MAY SAY "I DON'T KNOW P"
```

Only exact `PERMIT_FIRST_PERSON_NONKNOWLEDGE` licenses explicit nonknowledge.

## 9. Missing / valid-empty / deferred behavior

- `DISCLOSURE_ADMITTED`: exact semantic operation passes ADP-017/integrity gates.
- `DISCLOSURE_WITHHELD`: exact target evaluated; zero semantic output; no explanation inferred.
- `DISCLOSURE_VALID_EMPTY`: lawful complete evaluation with no ADP-022-specific output; no filler hedge/question/decline/ignorance phrase.
- `DISCLOSURE_UPSTREAM_PERMISSION_DENIED`: zero output; denial is not nonknowledge.
- `DISCLOSURE_UPSTREAM_PERMISSION_DEFERRED`: zero output; no “maybe/I think/I don't know” fallback.
- `DISCLOSURE_MISSING_AUTHORITY`: required claim/permission/operation/premise/composition/activation authority absent; zero attempted semantic output.
- `DISCLOSURE_FORBIDDEN_PROMOTION`: proposed output strengthens source epistemic class; zero output.
- `DISCLOSURE_NONCOMPARABLE_OR_AMBIGUOUS`: incompatible scopes/classes require unguided collapse or precedence; zero composite.
- `DISCLOSURE_INTEGRITY_FAILURE`: actor/turn/hash/claim/permission/provenance mismatch; zero output.

Missing system data never synthesizes actor uncertainty or nonknowledge. Missing operation authority never falls back to `ENGAGE_SELECTIVE` when special semantics are required.

## 10. Renderer / CAN-017 boundary

Renderer wording has zero authority to change epistemic class. An admitted render must remain semantically equivalent to the ADP-022 decision.

`ASSERT_BELIEF` cannot render as bare fact; `QUALIFY_UNCERTAINTY` must remain uncertain; `STATE_EXPLICIT_NONKNOWLEDGE` cannot add a guess. Question marks, `maybe`, `I think`, `I know`, `I don't know`, `not sure`, modals, pauses, politeness, and hesitation are not semantic authority.

`ASK_FROM_EPISTEMIC_GAP` and `DECLINE_EPISTEMIC_COMMITMENT` are not v1 registered operations; renderer syntax cannot create them.

CAN-017 may apply only semantics-preserving style/narrowing within its own authority. It cannot convert an ADP-022 class. ADP-022 creates no register label and owns no style.

## 11. Numeric / default / stochastic disposition

```text
numeric confidence scales          = NONE
numeric thresholds                 = NONE
hedge probabilities                = NONE
uncertainty percentages            = NONE
midpoints/default confidence       = NONE
confidence-to-operation formulas   = NONE
ADP-022 RNG streams                = NONE
```

Rejected terminal mechanisms include recovered `knowledge_confidence 0..1`, `hook_confidence < 0.5`, hedge-rate correlation, topic-based hedge rules, generic confidence bands, LLM-estimated certainty, and any `50`/midpoint default.

## 12. Replay / provenance

Every decision binds at minimum:
- actor ID, turn ID, exact turn artifact/hash;
- ADP-017 envelope ID/version/hash/as-of causal time/state hash;
- exact claim and permitted components;
- every permission/stance/contradiction ref used;
- proposed operation and target components;
- every premise claim + permission ref;
- ADP-022 authority/registry/rule IDs, versions, hashes;
- CAN-018 operation registration/activation refs when relevant;
- decision state/no-output reason;
- input state hash, provenance refs, decision hash.

Replay identity excludes wall clock, mutable `latest`, keyword heuristics, demographic/topic stereotypes, transcript prose, filesystem/list order, ambient RNG and LLM inference.

Same exact semantic inputs/authority versions produce the same decision state/hash. Renderer wording cannot rewrite the receipt.

## 13. Hostile fixtures

| ID | case | required result |
|---|---|---|
| H01 | true fact is actor-inaccessible | upstream permission denied; no assertion or invented ignorance |
| H02 | knowledge permission + knowledge assertion | admitted via `ENGAGE_SELECTIVE` |
| H03 | belief permission + bare fact | forbidden promotion |
| H04 | belief permission + belief assertion | admitted; belief preserved |
| H05 | explicit uncertainty permission + qualification | registered `QUALIFY_UNCERTAINTY` |
| H06 | uncertainty permission + affirmative P only | reject unless separate belief/knowledge permission |
| H07 | explicit nonknowledge permission + nonknowledge | registered `STATE_EXPLICIT_NONKNOWLEDGE` |
| H08 | system `EPISTEMIC_STATE_UNKNOWN`, no actor stance | missing/deferred; never “I don't know” |
| H09 | operational string `Unknown` | no actor epistemic inference |
| H10 | renderer hedges knowledge-only permission | semantic mismatch |
| H11 | renderer makes belief a bare fact | semantic mismatch |
| H12 | renderer says “I don't know” for denied/deferred | reject |
| H13 | low `hook_confidence` | no uncertainty operation |
| H14 | political topic + recovered hedge rule | no uncertainty inference |
| H15 | contradictory beliefs -> synthetic “I'm confused” | noncomparable/ambiguous absent meta-claim permission |
| H16 | belief + uncertainty same P | both exact permission refs required |
| H17 | contradictory beliefs as separate units | validate separately; no winner |
| H18 | uncertainty/nonknowledge + inquiry proposal only | missing activation authority; CAN-018 deferred; no ask op |
| H19 | system unknown + generic ask | no epistemic-gap ask |
| H20 | knowledgeable actor asks strategically | outside ADP-022 |
| H21 | uncertainty/nonknowledge + epistemic decline proposal only | missing activation authority; CAN-018 deferred; no decline op |
| H22 | denied claim -> “I can't say” as epistemic decline | deny; no manufactured reason |
| H23 | privacy/effort reason for decline | outside ADP-022; ADP-023 separate |
| H24 | permission exists but lawful no disclosure | withheld/valid-empty; no force |
| H25 | zero ADP-022 operation applies | valid-empty; no filler |
| H26 | required CAN-018 special registration missing | missing authority; zero special op |
| H27 | question smuggles inaccessible premise | reject premise |
| H28 | partial access + forbidden components requested | exact subset only |
| H29 | prior transcript says actor knows P; current permission absent | transcript cannot restore permission |
| H30 | legacy confidence 0.2, no ADP-017 uncertainty | no hedge authority |
| H31 | nonknowledge + `maybe P` guess | reject without separate uncertainty/belief permission |
| H32 | CAN-017 style erases belief marker into fact | invalid promotion |
| H33 | recovered `deflect` requested as uncertainty response | no registration |
| H34 | valid-empty/withhold + renderer invents polite uncertainty filler | reject |
| H35 | uncertainty and nonknowledge special ops both required with no precedence/composition | ADP-022 ambiguous; CAN-018 `DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES` |

## 14. Compatibility / versioning

Recovered scores, source labels, hedge examples and move strings may survive only as `COMPATIBILITY_ONLY` migration/audit material. They cannot activate ADP-022 or satisfy ADP-017.

Any change to permission mapping, disclosure classes, special-operation set/activation, ask/decline registration, contradiction composition, premise permissions, numeric semantics, or renderer-equivalence law requires a new accepted authority version. Mutable `latest` is forbidden replay identity.

## 15. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

Genuine ambiguity: recovered V2 clearly intends uncertainty/ignorance/hedging and variable response, but hard authority does not authorize its confidence scalar, automatic hedge mapping, topic heuristics, or broad move vocabulary.

Lawful alternatives were: freeze recovered scalar/move policy; create a generic hedge/nonknowledge fallback on incomplete system knowledge; or preserve exact ADP-017 distinctions, lawful no-output states, and only the minimum CAN-018 registrations whose activation is independently provable.

Chosen: the third. V1 registers only `QUALIFY_UNCERTAINTY` and `STATE_EXPLICIT_NONKNOWLEDGE`. Ask/decline remain governed nonregistrations because an epistemic condition is not a communicative selector.

Decisive principles: determination is not transparency; actor opacity; contradiction/multiplicity; lawful absence over graceful hallucination; downstream vividness not beyond upstream authority; minimum sufficient machinery; renderer/LLM expressive rather than ontological.

The Governing Spirit supplies no actor uncertainty, confidence value, threshold, default, operation activation fact, response-purpose selector, or wording.

## 16. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__ADP_022_CLOSED__V2_P2_AUTHORITY_COMPLETE_IF_ACCEPTED__V2_P5_REMAINS_ADP_023_GATED`.

RA-R00 maps V2-P2 to `CAN-015`, `CAN-016`, `MUST-022`; CAN-015/016 are accepted, so acceptance of ADP-022 closes its semantic authority set while implementation remains separately gated.

RA-R00 maps V2-P5 to `CAN-016`, `CAN-017`, `CAN-018`, `MUST-022`, `MUST-023`; CAN-016..018 are accepted, this closes `MUST-022`, and `ADP-023/MUST-023` plus implementation/release gates remain separate.

The explicit v1 nonregistration of ask/decline does not reopen MUST-022: ADP-022 supplies the governing negative rule, and minimum uncertainty/nonknowledge expression exists through the two registered special operations or lawful zero-output states.

## 17. Final token

`ADP_022_V2_UNCERTAINTY_DISCLOSURE_AUTHORITY = PASS`
