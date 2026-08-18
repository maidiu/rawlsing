# CAN-018 — V2 Response-Move Canonicalization

**Assignment:** `W1-B03-04`  
**Canonicalization ID:** `CAN-018`  
**Canonical authority:** `V2_RESPONSE_MOVE_RULE@1.0.0`  
**Owner:** `V2_EXPRESSION_PLANNER`  
**Repository / branch:** `maidiu/rawlsing` / `agent/vozhd-dva-w1-can-018-v2-response-move`  
**Exact launch base:** `db961be677d5112073e16e5d452853971861cdb6`  
**Continuation reviewed head:** `56ce30888e05e5ceeb7a44edc1b2c2e57d428fdc`  
**Vozhd disposition comment:** `5325834137`  
**Mode:** authority canonicalization only; no production code; no V2 implementation  
**Verdict:** `PASS`

## 1. Holding and preserved authority

A V2 response move is a **turn-level surface/presentation operation over already-lawful expression material**. It is not a causal life action, relationship mutation, actor knowledge, memory formation, boundary development, attractor change, or proof that rendered output occurred.

The generic CAN-018 architecture from the reviewed result is preserved:

- `V2ResponseMoveDecision` / receipt contract;
- ADP-017 actor-accessibility ceiling;
- exact activation and constraint receipts;
- deterministic replay/provenance;
- typed `VALID_EMPTY`, deferred, denied and integrity outcomes;
- no keyword, numeric, default, RNG or LLM semantic winner;
- rendering != causal occurrence;
- exact-artifact V3 admission in `IN_WORLD_CAUSAL` mode.

The narrow correction is ontological: recovered historical move labels are **not** a terminal move taxonomy merely because they existed in the old implementation or design prose.

Binding noncollapse remains:

`ACTOR_ACCESSIBLE_TRUTH != V2_SALIENCE != V2_EXPRESSION_REGISTER != V2_RESPONSE_MOVE != RENDERED_EXPRESSION != CAUSAL_OCCURRENCE`.

## 2. Historical source evidence remains verified

Required archive `Rawlsing_code_bundle_staging.zip` was directly verified before the original result. Expected and computed SHA256 are both:

`953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`

Verdict: `EXACT_MATCH`; ZIP entries: `13,138`.

Directly inspected continuity/negative evidence remains:

- `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` — broad/extensible move vocabulary and renderer-not-decider direction;
- `v2/conversation_engine.py` — executable `engage_selective` / `deflect` / `brief_or_deflect` selector plus keyword/numeric overrides;
- `v2/additions.txt` and `v2/PIPELINE_WIRING_AUDIT.md` — earlier move-vocabulary and keyword-override continuity;
- `v2/run_conversation_chat.py` and `server/chat/turn.py` — direct turn callers;
- `v2/life_simulation_schema.py` — legacy AttentionBudget numeric/default machinery;
- `server/session_state.py` / `server/session_db.py` — session continuity only;
- `v3/io/persona_sheet.py` / `v3/V3_UNDERLIES_V2_ARTICULATION.md` — V3→V2 surface continuity only;
- `tests/test_chat_integrity.py` — focused recovered-source court: **11 passed**.

Those sources establish historical continuity and negative evidence. They do **not** register terminal special-operation semantics.

## 3. Recovered vocabulary disposition

`ENGAGE_SELECTIVE` is the sole v1 canonical operation.

Every other recovered label is:

`COMPATIBILITY_ONLY_RECOVERED_VOCABULARY`

including, without semantic promotion:

- `MICRO_REACT`;
- `TEST_QUESTION`;
- `ANSWER_MINIMALLY`;
- `ANSWER_ONE_DETAIL_ASK_ONE_QUESTION`;
- `DEFLECT`;
- `PIVOT`;
- `REDIRECT`;
- `CHANGE_SUBJECT`;
- `DROP_THREAD`;
- `DELAY`;
- `SILENCE`;
- `CHALLENGE`;
- `REJECT_FRAMING`;
- `CORRECT_MISUNDERSTANDING`;
- `REFRAME`;
- `BOUNDARY_STATEMENT`;
- `ASK_SAFER_QUESTION`;
- `EXIT`;
- `flirt`;
- `test motive`;
- `mirror emotion`;
- compound historical labels such as `tease+soften`, `deflect with humor`, `soften+pivot`, `brief response+change subject`, and `brief_or_deflect`.

Historical string identity, prose gloss, intuitive usefulness, or prior executable use does not make any of these canonical. Near-synonyms and compounds are not resolved by CAN-018.

`MUST-022` remains owner of uncertainty-specific assert / hedge / withhold / ask / decline semantics.  
`MUST-023` remains owner of boundary / face-risk / effort / attention constrained semantics.  
`CAN-019` remains owner of relationship-specific expression semantics.

CAN-018 supplies a generic registration/selection membrane only; it pre-registers none of those downstream semantic inventories.

## 4. Minimal canonical operation registry

Canonical registry:

`V2_RESPONSE_MOVE_OPERATION_REGISTRY@1.0.0`

### 4.1 Base operation

The v1 base-operation set contains exactly one entry:

`ENGAGE_SELECTIVE`

owned here under:

`CAN018_BASE_ENGAGE_RULE@1.0.0`.

Its bounded semantic scope is only:

> address one or more already-lawful expression targets as ordinary turn-level presentation, without implying completeness and without acquiring any special uncertainty, boundary, relationship, topic-shift, silence, challenge, correction, delay, or exit meaning.

### 4.2 Special-operation registry

`SPECIAL_OPERATION_REGISTRY = VALID_EMPTY_SPECIAL_OPERATION_REGISTRY`

Current special-operation count: **0**.

No recovered label is a registered special operation in v1.

### 4.3 Future registration schema

A future special operation becomes canonical only after a **separately accepted owning authority** supplies both its distinct semantics and its exact activation/constraint rule. Registration requires at minimum:

- `operation_id`;
- `operation_schema_version`;
- exact semantic scope;
- owning authority ID/version/hash;
- activation rule ID/version/hash;
- relevant constraint-domain refs;
- immutable registration receipt/hash.

Forbidden registration bases include historical string presence, intuitive synonymy, compound names, keyword/topic matches, LLM suggestions, numeric scores/thresholds, or implementation convenience.

Aliases may be retained for migration/audit only. An alias has zero activation force.

## 5. Base-operation justification

`ENGAGE_SELECTIVE` is retained **not** because the legacy selector defaulted to it, but because V2-P5 requires one minimum positive operation for the ordinary case in which lawful expression material exists and no separately governed special operation is required.

It adds no new actor truth and no special discourse semantics. It means only that V2 may address some already-lawful expression targets. Without one such positive base operation, ordinary lawful expression would be semantically starved even when all downstream special-operation domains are irrelevant.

Exact positive rule:

If:

1. at least one lawful expression target exists;
2. the ADP-017 access envelope verifies;
3. all required constraint domains are satisfied or explicitly `NOT_APPLICABLE`;
4. no separately accepted authority requires a special operation; and
5. no accepted constraint forbids ordinary engagement;

then `CAN018_BASE_ENGAGE_RULE@1.0.0` selects `ENGAGE_SELECTIVE`.

This is a positive rule, never a missing-data fallback.

If a special semantic is required but its owning authority/registration is missing, return `DEFERRED_REQUIRED_AUTHORITY`; do **not** reinterpret `ENGAGE_SELECTIVE` as that special move.

## 6. Canonical response-move decision contract

`V2ResponseMoveDecision` carries:

- decision ID;
- exact actor-access envelope ref/hash;
- exact turn artifact ref/hash;
- lawful expression-target refs;
- accepted constraint receipt refs;
- registry and selector-rule IDs/versions/hashes;
- status;
- optional selected registered operation ID;
- exact selection-basis refs;
- decision hash.

Statuses remain:

- `MOVE_SELECTED`;
- `VALID_EMPTY_NO_LAWFUL_MOVE`;
- `DEFERRED_REQUIRED_AUTHORITY`;
- `DEFERRED_REQUIRED_INPUT`;
- `DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES`;
- `DENIED_ACTOR_ACCESS_VIOLATION`;
- `DENIED_FORBIDDEN_HEURISTIC_PATH`;
- `INTEGRITY_FAILURE`.

CAN-018 may narrow or omit lawful expression. It may never increase the set of claims/content the actor may access or assert.

## 7. Selector and no-lawful-move law

Required selector inputs remain:

- verified ADP-017 actor-access envelope;
- exact current-turn artifact;
- `0..n` already-lawful expression targets;
- applicable accepted constraint receipts or exact `NOT_APPLICABLE`;
- exact registry/rule versions and hashes.

Only **registered operations** are selector candidates.

An unregistered recovered label cannot become a candidate by exact string match, fuzzy match, topic match, LLM suggestion, configuration key, or compatibility alias.

If two or more registered non-equivalent operations are someday active and no accepted precedence orders them, return `DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES`. List order, lexical order, first-candidate choice, RNG, LLM judgment and scores remain forbidden winner rules.

Zero lawful operation candidates after all gates yields:

`VALID_EMPTY_NO_LAWFUL_MOVE`.

No arbitrary fallback is synthesized. Historical `SILENCE` is not a canonical v1 operation and cannot be used as a disguised fallback.

## 8. Keyword / numeric / default disposition

Historical `_POLITICAL_STRUCTURAL_KEYWORDS`, `_DISMISSIVE_PATTERNS`, topic labels and keyword deep-memory surfacing have zero semantic authority. They may not register or activate a response operation or widen actor accessibility.

Quarantined numeric/default policy includes legacy AttentionBudget `0..100`, default `50`, thresholds `25/50/75`, sentence caps `2/4/6/8/12`, tension/demand thresholds `.5/.6/.75`, and any move score/weight.

Rejected defaults include `move.get(..., "engage_selective")`, `brief_or_deflect`, default `50/moderate/6`, and filler question/decline/exit/silence behavior.

MUST-025 render RNG may vary wording after a move decision; it cannot choose or register semantic operations.

## 9. Noncausal boundary

In `PRESENTATION_NONCAUSAL`, move/plan/render may be displayed or persisted as V2/session/audit state and cannot mutate V3 life, memory, relationship, boundary or attractor state.

In `IN_WORLD_CAUSAL`, the rendered response remains:

`CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`.

Only exact V3 admission under MUST-019 of the exact rendered artifact/hash makes it something the generated actor actually said/did. The move decision itself is not the admitted event. A rerender is a new artifact/hash and never inherits prior admission.

## 10. Replay and provenance

CAN-018 v1 move selection is deterministic. Replay identity binds:

- actor-access-envelope hash;
- turn-artifact hash;
- lawful target refs/hashes;
- accepted constraint receipt refs/hashes;
- registry/rule IDs/versions/hashes;
- selection-basis refs.

Wall clock, filesystem/dict/list order, mutable `latest`, keyword side channels, LLM/model choice, V3 causal RNG and V2 render RNG are forbidden semantic entropy.

The later render request/receipt must reference the exact move-decision hash.

## 11. Hostile fixtures

- `H01` — actor-inaccessible claim exists elsewhere → **DENY; selector cannot widen actor access.**
- `H02` — exact string `PIVOT` appears with no registration → **no activation; no canonicalization by string match.**
- `H03` — plausible `CORRECT_MISUNDERSTANDING` requested without owning authority → **DEFERRED_REQUIRED_AUTHORITY; plausible name is not canonical.**
- `H04` — boundary-like situation requires special semantics while MUST-023 is missing → **DEFERRED_REQUIRED_AUTHORITY; ENGAGE_SELECTIVE does not acquire boundary/exit/silence meaning.**
- `H05` — compatibility `TEST_QUESTION` is used to implement uncertainty-specific ask semantics without MUST-022 → **blocked/deferred; compatibility vocabulary cannot bypass MUST-022.**
- `H06` — compatibility `EXIT` / `BOUNDARY_STATEMENT` used without MUST-023 → **blocked/deferred; compatibility vocabulary cannot bypass MUST-023.**
- `H07` — compatibility `flirt` / `test motive` / `mirror emotion` used without CAN-019 → **blocked/deferred; compatibility vocabulary cannot bypass CAN-019.**
- `H08` — zero lawful targets and no registered special operation → **VALID_EMPTY_NO_LAWFUL_MOVE; no fallback and no synthetic SILENCE.**
- `H09` — political/structural keyword match → **no operation override or registration.**
- `H10` — legacy numeric threshold crosses → **no operation change absent exact authority.**
- `H11` — legacy `brief_or_deflect` token → **compatibility-only; never executable by token alone.**
- `H12` — two future registered non-equivalent operations activate without precedence → **DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES.**
- `H13` — keyword deep-memory path surfaces inaccessible material → **reject input; ADP-017 ceiling wins.**
- `H14` — renderer changes selected operation → **validation/audit failure.**
- `H15` — causal-mode artifact not admitted by V3 → **pending noncausal candidate; no occurrence.**
- `H16` — rerender after prior admission → **new artifact/hash requires new admission.**
- `H17` — exact replay inputs → **identical status/operation/decision hash.**
- `H18` — ungoverned move score/weight introduced → **reject/missing authority.**
- `H19` — class/religion/nationality/structure directly selects operation → **forbidden structural/persona shortcut.**
- `H20` — >=1 lawful target, no special operation required, constraints satisfied/NA → **CAN018_BASE_ENGAGE_RULE selects ENGAGE_SELECTIVE.**
- `H21` — recovered `SILENCE` string with no registration → **no activation; valid-empty or typed deferral applies.**
- `H22` — historical compound `ANSWER_ONE_DETAIL_ASK_ONE_QUESTION` appears → **no compound semantics; remains compatibility vocabulary until separately registered.**

## 12. Governing Spirit / consumers

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

The continuation resolves one lawful ambiguity: whether a rich recovered label inventory should become terminal ontology or remain compatibility/candidate vocabulary behind minimum sufficient machinery. The corrected choice is the latter. V1 keeps only the independently justified ordinary-expression base operation and a valid-empty special-operation registry. This preserves lawful absence, bounded jurisdiction and downstream authority without starving ordinary V2 expression. The Governing Spirit supplies no special operation, trigger, psychology, boundary, relationship state, uncertainty state, score, threshold or causal effect.

Primary consumer remains `V2-P5`. CAN-018 closes its own semantic blocker after Vozhd acceptance. V2-P5 still independently waits on `CAN-016`, `CAN-017`, `MUST-022`, `MUST-023`, `IMP-009` and release/physical gates. CAN-019/CAN-021 and causal/render seams remain separate.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__CAN_018_SEMANTIC_BLOCKER_CLOSED_FOR_V2_P5_AFTER_VOZHD_ACCEPTANCE__V2_P5_REMAINS_BLOCKED_BY_CAN_016_CAN_017_MUST_022_MUST_023_AND_PACKET_GATES`

## 13. Final token

`CAN_018_V2_RESPONSE_MOVE_CANONICALIZATION = PASS`
