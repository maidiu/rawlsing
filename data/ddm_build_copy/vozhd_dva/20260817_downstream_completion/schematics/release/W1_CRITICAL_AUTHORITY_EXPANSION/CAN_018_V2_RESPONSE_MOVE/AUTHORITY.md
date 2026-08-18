# CAN-018 — V2 Response-Move Canonicalization

**Assignment:** `W1-B03-04`  
**Canonicalization ID:** `CAN-018`  
**Canonical authority:** `V2_RESPONSE_MOVE_RULE@1.0.0`  
**Owner:** `V2_EXPRESSION_PLANNER`  
**Repository / branch:** `maidiu/rawlsing` / `agent/vozhd-dva-w1-can-018-v2-response-move`  
**Exact base SHA:** `db961be677d5112073e16e5d452853971861cdb6`  
**Mode:** authority canonicalization only; no production code; no V2 implementation  
**Verdict:** `PASS`

## 1. Holding and archive verification

A V2 response move is a **turn-level surface/presentation operation over already-lawful expression material**. It is not a causal life action, relationship mutation, actor knowledge, memory formation, boundary development, attractor change, or proof that rendered output occurred.

Required archive `Rawlsing_code_bundle_staging.zip` was directly verified before reliance. Expected and computed SHA256 are both `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`; verdict `EXACT_MATCH`; ZIP entries `13,138`. The assigned branch was identical to the exact launch base before writing.

Binding separation:

`ACTOR_ACCESSIBLE_TRUTH != V2_SALIENCE != V2_EXPRESSION_REGISTER != V2_RESPONSE_MOVE != RENDERED_EXPRESSION != CAUSAL_OCCURRENCE`.

V3 generates life; V2 expresses it. ADP-017 is the hard actor-access ceiling. CAN-018 does not absorb CAN-016, CAN-017, MUST-022, MUST-023, CAN-019, CAN-021, MUST-019 or MUST-025.

## 2. Direct recovered-source court

| Source | Finding / disposition |
|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` (`0b0ee1d5e177…`) | extensible move library; pivot/deflect/ignore/exit/boundary-like paths; renderer-not-decider. |
| `v2/conversation_engine.py` (`766bee296379…`) | executable selector; engage_selective/deflect/brief_or_deflect; keyword and numeric overrides. |
| `v2/additions.txt` (`6040500c2b8a…`) | earlier move-vocabulary continuity. |
| `v2/PIPELINE_WIRING_AUDIT.md` (`fabbf700ec6e…`) | documents political-keyword override wiring. |
| `v2/run_conversation_chat.py` (`b9276a4d7fc9…`) | direct turn caller. |
| `v2/life_simulation_schema.py` (`e7adf11fe6db…`) | legacy AttentionBudget 0..100/default-50/threshold machinery. |
| `server/chat/turn.py` (`10e7f02333da…`) | application caller; keyword deep-memory surfacing negative evidence. |
| `server/session_state.py` (`9c9c3b0e2b3b…`) | session continuity only. |
| `server/session_db.py` (`0d9bf508aa74…`) | session persistence only. |
| `tests/test_chat_integrity.py` (`efcb4ad8c65b…`) | focused historical court: 11 passed. |
| `v3/io/persona_sheet.py` (`4a0009533443…`) | V3→V2 surface continuity only. |
| `v3/V3_UNDERLIES_V2_ARTICULATION.md` (`5a0f11276a83…`) | V3-causal/V2-articulation continuity. |

Focused historical court: `PYTHONPATH=. python -m pytest -q tests/test_chat_integrity.py` → **11 passed**. This establishes implementation continuity only.

Recovered design vocabulary is broad and explicitly extensible. It includes micro-react, test question, deflect/pivot, soft challenge, drop thread, delay, minimal answer, one-detail-plus-question, redirect/change subject, go quiet/silence, correct misunderstanding, reject framing, boundary statement, reframe, challenge and exit-like operations. The executable selector instead collapses output to `engage_selective`, `deflect`, or ambiguous `brief_or_deflect`, then changes behavior from political/dismissive keywords, attention defaults, and demand/tension thresholds. Those shortcuts are negative evidence, not terminal authority.

## 3. Recovered vocabulary dispositions

- **PRESERVE/ADAPT:** `ENGAGE_SELECTIVE`, `MICRO_REACT`, `TEST_QUESTION`, `ANSWER_MINIMALLY`, `ANSWER_ONE_DETAIL_ASK_ONE_QUESTION`, `DEFLECT`, `PIVOT`, `REDIRECT`, `CHANGE_SUBJECT`, `DROP_THREAD`, `DELAY`, `SILENCE`, `CHALLENGE`, `REJECT_FRAMING`, `CORRECT_MISUNDERSTANDING`, `REFRAME`.
- **PRESERVE but require MUST-023 constraint receipt:** `BOUNDARY_STATEMENT`, `ASK_SAFER_QUESTION`, `EXIT`.
- **COMPATIBILITY_ONLY pending CAN-019:** `flirt`, `test motive`, `mirror emotion`.
- **Composition/style only:** `tease+soften`, `deflect with humor`, `soften+pivot`, `brief response+change subject`; renderer/style layers may combine atomic moves only under separate authority.
- **REMOVE/REJECT:** `brief_or_deflect` as unresolved compound, fixed `25–40` move cardinality, keyword/topic override, numeric/default selector policy.

The canonical registry is extensible and currently contains **19 atomic move kinds**. Registry membership never activates a move by itself.

## 4. Canonical response-move contract

`V2ResponseMoveDecision` carries: decision ID; exact actor-access envelope and turn artifact hashes; lawful expression-target refs; accepted constraint receipts; move-registry and selector-rule IDs/versions/hashes; status; optional selected move; selection-basis refs; decision hash.

Statuses:

- `MOVE_SELECTED`;
- `VALID_EMPTY_NO_LAWFUL_MOVE`;
- `DEFERRED_REQUIRED_AUTHORITY`;
- `DEFERRED_REQUIRED_INPUT`;
- `DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES`;
- `DENIED_ACTOR_ACCESS_VIOLATION`;
- `DENIED_FORBIDDEN_HEURISTIC_PATH`;
- `INTEGRITY_FAILURE`.

CAN-018 may narrow, omit, redirect, question, challenge, delay or silence lawful material. It may never increase the set of claims/content the actor may access or assert.

## 5. Selector input / precondition law

Required inputs are: verified ADP-017 actor-access envelope; exact current-turn artifact; `0..n` already-lawful expression targets; applicable accepted constraint receipts or exact `NOT_APPLICABLE`; exact registry/rule versions and hashes.

**Positive base rule:** when at least one lawful expression target exists, all required constraint domains are satisfied or not applicable, no accepted constraint requires another move, and none forbids engagement, `CAN018_BASE_ENGAGE_RULE@1.0.0` selects `ENGAGE_SELECTIVE`. This is a positive rule, never a missing-data fallback.

Every special move requires an exact activation/constraint basis. `MUST-022` owns uncertainty-specific assert/hedge/withhold/ask/decline semantics. `MUST-023` owns boundary/face-risk/effort/attention. `CAN-019` owns relationship-specific expression. Same-batch results are not consumed as accepted authority here.

If two or more non-equivalent moves remain activated and no accepted precedence orders them, return `DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES`. List order, lexical order, first candidate, random choice, LLM judgment, keyword counts and ungoverned scores are forbidden winner rules.

## 6. No-lawful-move / keyword / numeric / default law

Zero lawful targets/candidates after all gates yields `VALID_EMPTY_NO_LAWFUL_MOVE`; no arbitrary move is synthesized. Intentional `SILENCE` is a positively selected move and remains distinct from valid-empty.

Historical `_POLITICAL_STRUCTURAL_KEYWORDS`, `_DISMISSIVE_PATTERNS`, topic labels and keyword deep-memory surfacing have zero semantic authority. They may not activate a move or widen actor accessibility.

Quarantined numeric/default policy includes legacy AttentionBudget `0..100`, default `50`, thresholds `25/50/75`, sentence caps `2/4/6/8/12`, tension/demand thresholds `.5/.6/.75`, and any move score/weight. Future quantity semantics require exact independent formula authority, especially MUST-023 where applicable.

Rejected defaults include `move.get(..., "engage_selective")`, `brief_or_deflect`, default `50/moderate/6`, and filler question/decline/exit/silence. MUST-025 render RNG may vary wording after a move is selected; it may not choose semantic move kind.

## 7. Noncausal boundary

In `PRESENTATION_NONCAUSAL`, move/plan/render may be displayed or persisted as V2/session/audit state and cannot mutate V3 life, memory, relationship, boundary or attractor state.

In `IN_WORLD_CAUSAL`, the rendered response remains `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`. Only exact V3 admission under MUST-019 of the exact rendered artifact/hash makes it something the generated actor actually said/did. The move decision itself is not the admitted event. A rerender is a new artifact/hash and never inherits prior admission.

## 8. Replay and provenance

CAN-018 v1 move selection is deterministic. Replay identity binds actor-access-envelope hash, turn-artifact hash, lawful target refs/hashes, accepted constraint receipt refs/hashes, registry/rule IDs/versions/hashes and selection-basis refs. Same exact inputs and versions yield the same status/move/decision hash.

Wall clock, filesystem/dict/list order, mutable `latest`, keyword side channels, LLM/model choice, V3 causal RNG and V2 render RNG are forbidden semantic entropy. The later render request/receipt must reference the exact move-decision hash.

## 9. Hostile fixtures

- `H01` — Actor-inaccessible claim elsewhere in system → **DENY; selector cannot widen actor access.**
- `H02` — Political/structural keyword match → **No move override.**
- `H03` — Dismissive keyword with no MUST-023 receipt → **No automatic deflect/boundary; defer if boundary authority required.**
- `H04` — Legacy attention/tension/demand threshold crosses → **No move change absent exact formula authority.**
- `H05` — Zero lawful expression targets → **VALID_EMPTY_NO_LAWFUL_MOVE; no fallback.**
- `H06` — Two non-equivalent activated moves without precedence → **DEFERRED_AMBIGUOUS_NON_EQUIVALENT_MOVES.**
- `H07` — Legacy brief_or_deflect token → **Reject ambiguous compound.**
- `H08` — Uncertainty/nonknowledge without MUST-022 → **DEFERRED_REQUIRED_AUTHORITY; CAN-018 does not choose hedge/withhold/ask/decline.**
- `H09` — Boundary/exit move without MUST-023 → **DEFERRED_REQUIRED_AUTHORITY.**
- `H10` — Flirt/test-motive/mirror-emotion without CAN-019 → **Compatibility-only; no canonical activation.**
- `H11` — Session topic/energy suggests move → **Only accepted noncausal interface may constrain; persistence is not actor truth.**
- `H12` — Keyword deep-memory path surfaces inaccessible material → **Reject input; ADP-017 ceiling wins.**
- `H13` — Renderer changes semantic move → **Validation/audit failure.**
- `H14` — Causal-mode artifact not admitted by V3 → **CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION; no occurrence.**
- `H15` — Rerender after prior admission → **New artifact/hash requires new admission.**
- `H16` — Replay exact decision inputs → **Identical status/move/decision hash.**
- `H17` — Ungoverned move score/weight introduced → **Reject/missing authority.**
- `H18` — Authorized SILENCE selected → **MOVE_SELECTED:SILENCE, distinct from valid-empty.**
- `H19` — Class/religion/nationality/structure directly selects move → **Forbidden structural/persona shortcut.**
- `H20` — >=1 lawful target; no special constraint → **CAN018_BASE_RULE selects ENGAGE_SELECTIVE.**

## 10. Governing Spirit / consumers

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`.

The lawful ambiguity was broad/extensible historical move semantics versus the coarse executable three-token selector plus convenience heuristics. The chosen design preserves atomic/versioned surface operations, one evidence-backed nonempty base-engage rule, exact activation for special moves, lawful empty/ambiguity, and quarantines heuristic/numeric/default policy. Tie-break: downstream vividness cannot exceed upstream authority; actor opacity/accessibility is a ceiling; lawful absence and minimum sufficient machinery outrank plausible filler; expression is not occurrence. The Governing Spirit supplies no trigger, psychology, boundary, relationship state, uncertainty state, score, threshold or causal effect.

Primary consumer is `V2-P5`. CAN-018 closes its own semantic blocker after Vozhd acceptance. V2-P5 still independently waits on `CAN-016`, `CAN-017`, `MUST-022`, `MUST-023`, `IMP-009` and release/physical gates. Later CAN-019/CAN-021 and causal/render seams remain separate.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT__CAN_018_SEMANTIC_BLOCKER_CLOSED_FOR_V2_P5_AFTER_VOZHD_ACCEPTANCE__V2_P5_REMAINS_BLOCKED_BY_CAN_016_CAN_017_MUST_022_MUST_023_AND_PACKET_GATES`

## 11. Final token

`CAN_018_V2_RESPONSE_MOVE_CANONICALIZATION = PASS`
