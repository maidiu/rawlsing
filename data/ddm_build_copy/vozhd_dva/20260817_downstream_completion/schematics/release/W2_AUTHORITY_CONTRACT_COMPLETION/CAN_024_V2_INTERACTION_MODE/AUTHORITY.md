# CAN-024 — V2 Interaction-Mode Policy Canonicalization

**Assignment:** W2-B02-06 — CAN-024 / V2 Interaction-Mode Policy  
**Repository:** `maidiu/rawlsing`  
**Branch:** `agent/vozhd-dva-w2-can-024-v2-interaction-mode`  
**Exact base:** `ad5806a1bb8b5f106372aa5cfd40f1eebc2bf969`  
**Authority:** `V2_INTERACTION_MODE_POLICY@1.0.0`  
**Owner:** `V2_APPLICATION_INTERACTION_MODE_BOUNDARY`  
**Schemas:** `V2_INTERACTION_MODE_DIRECTIVE@1.0.0`, `V2_INTERACTION_MODE_SESSION_STATE@1.0.0`, `V2_INTERACTION_MODE_RECEIPT@1.0.0`  
**Historical ZIP:** `NOT_AUTHORIZED_NOT_USED`  
**Verdict:** `PASS`

## 1. Binding holding

CAN-024 answers only whether an exact V2/application interaction is presentation-only or explicitly eligible for the separately governed causal-interaction handshake.

```text
PRESENTATION_NONCAUSAL  = constitutional default; render/session only; no V3 submission
IN_WORLD_CAUSAL         = explicit; exact render may become a candidate; no occurrence until ADP-019 ADMIT
```

Constitutional separations:

```text
mode != rendered artifact != package != V3 admission != V3 event != V3 effect
V2 session/transcript cursor != V3 event cursor != V3 causal-session cursor
render/session persistence != actor history
```

`IN_WORLD_CAUSAL` never means admitted. Its outbound artifact begins as `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`. `PRESENTATION_NONCAUSAL` begins as `PRESENTATION_NONCAUSAL_RENDERED` and is ineligible for V3 submission through this lane.

## 2. Evidence and jurisdiction

Directly inspected at the exact base: W2 Batch-02 launch law; `CURRENT_STATE`; Governing Spirit; Terminal Demand; Architecture Pass Law; whole-machine, implementation-synthesis, W0, W1, W2-first-batch and V2 completion rulings; RA-R00 MD/JSON; accepted ADP-019 external admission; accepted ADP-026 caller-current-situation; adjacent accepted ADP-024 transcript/cursor and ADP-025 render/rerender authorities. Current `v2/conversation_engine.py` and `server/chat/turn.py` are absent at this base and therefore supply no current authority. No sibling W2 Batch-02 return was consumed.

CAN-024 owns only mode IDs/default, directive intake/source validation, TURN/SESSION scope, V2-cursor binding, explicit override/update/clear semantics, session-mode state identity, resolution precedence, mode receipt/hash, packaging eligibility and fail-closed behavior.

It does **not** own V3 admission/event/effect/cursor semantics, CAN-025 packaging, CAN-022 prompt admission, CAN-023 translation equivalence, ADP-025 renderer/RNG/rerender semantics, ADP-024 cursor creation/retention, ADP-026 source truth, or actor history.

Exact consumers: `V2-P9`, `V2-P10`.

## 3. Canonical registry and default

`V2_INTERACTION_MODE_REGISTRY@1.0.0` has exactly two entries:

| mode | default? | packaging eligible? | initial outbound status |
|---|---:|---:|---|
| `PRESENTATION_NONCAUSAL` | yes | no | `PRESENTATION_NONCAUSAL_RENDERED` |
| `IN_WORLD_CAUSAL` | no; explicit only | yes, subject to separate CAN-025/ADP-019 | `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION` |

No aliases, scores, confidence levels, semi-causal modes or heuristic modes exist.

With no valid active explicit directive:

```text
effective_mode = PRESENTATION_NONCAUSAL
source = CAN024_CONSTITUTIONAL_DEFAULT
```

This is a complete lawful result, not missing authority.

## 4. Mode authority/source contract

The only v1 external directive source is an exact valid ADP-026 statement:

```text
CALLER_CURRENT_SITUATION_AUTHORITY@1.0.0
field_key = interaction.mode_context
```

Allowed source classes remain `CALLER_ASSERTED`, `SESSION_RECORDED`, `SCENARIO_DECLARED_NONACTUAL`.

Additional restrictions:
- `SCENARIO_DECLARED_NONACTUAL` may select only `PRESENTATION_NONCAUSAL`;
- `SESSION_RECORDED` may carry causal session mode only with exact provenance to an explicitly authorized session directive/state;
- caller assertion proves the mode declaration only, not other message propositions;
- renderer/model output, wording, emotion, topic, relationship framing, transcript summaries, EnergeticField, keywords, mutable defaults and `latest mode` are forbidden mode authority.

`interaction.mode_context` itself is presentation/session metadata, never a V3 event candidate.

## 5. Directive / scope / update law

`V2InteractionModeDirective` requires: `directive_id/schema_version`, `session_id`, subject ref/hash, `mode`, `operation`, `scope_kind`, effective turn cursor, exact V2 session-cursor ref/hash, ADP-026 statement ref/hash, source authority ID/version/hash, source class, expected prior session-mode-state ref/hash when applicable, provenance, and directive hash.

Enums:

```text
mode       = PRESENTATION_NONCAUSAL | IN_WORLD_CAUSAL
operation  = SET_MODE | CLEAR_TO_DEFAULT
scope_kind = TURN | SESSION
```

`CLEAR_TO_DEFAULT` resolves to `PRESENTATION_NONCAUSAL`.

Hash profile: SHA-256 over RFC8785/JCS UTF-8 with domain `rawlsing:v2:interaction-mode-directive:v1`; ID prefix `v2imd:`. Same ID/different content is `INTERACTION_MODE_DIRECTIVE_ID_COLLISION`.

### TURN
A TURN directive applies only to its exact session + turn + V2 cursor identity. It never mutates session mode state. Thus one causal turn does not make the next causal.

### SESSION
A SESSION directive is lawful only when its source explicitly authorizes session persistence. It applies prospectively from its exact effective cursor until a later valid session `SET_MODE`, `CLEAR_TO_DEFAULT`, or formal session close. It never rewrites earlier turns or crosses session IDs.

A TURN directive overrides an active SESSION directive for that turn only; the underlying session state survives.

### Session-state update
`V2InteractionModeSessionState` binds session ID, active session directive ref/hash or null, explicit session mode or null, effective-from cursor, last-update V2 cursor ref/hash, prior-state hash, status, provenance and state hash. Null active directive is lawful and means default presentation.

SESSION mutation requires exact expected prior-state ref/hash. Mismatch is `INTERACTION_MODE_UPDATE_CONFLICT`; no mutation occurs.

## 6. Cursor and precedence law

CAN-024 consumes the existing V2 session/transcript cursor by exact ref/hash. It does not create, advance, renumber, reuse or derive it. A stale/bad cursor yields `INTERACTION_MODE_STALE_CURSOR` or integrity failure and **never** falls back to an earlier causal mode.

Resolution precedence:

1. validate policy/source/subject/session/cursor integrity;
2. exact valid TURN directive;
3. exact active SESSION directive;
4. constitutional default `PRESENTATION_NONCAUSAL`.

Nonidentical same-rank directives with no governed resolution produce `INTERACTION_MODE_CONFLICT`; execution posture is fail-closed presentation/noncausal and causal packaging eligibility is false. Stable ordering is serialization only.

## 7. Mode receipt

`V2InteractionModeReceipt` binds: receipt ID/schema; policy ID/version/hash; session/turn/V2-cursor refs/hashes; resolution state; effective mode; execution posture; selected directive ref/hash or null; scope/source/source-statement/authority identity; active session-state ref/hash; turn-override flag; `causal_packaging_eligible`; required initial outbound artifact status; ADP-019 authority ref; rejected/conflicting directive refs; provenance; receipt hash.

Receipt hash uses SHA-256 + RFC8785/JCS with domain `rawlsing:v2:interaction-mode-receipt:v1`; ID prefix `v2imr:`. Receipts are immutable and turn-bound. A prior receipt is replay evidence, not automatic next-turn authority.

## 8. Artifact / admission / rerender law

Presentation mode:

```text
RenderedTurnArtifact.status = PRESENTATION_NONCAUSAL_RENDERED
causal_packaging_eligible = false
```

Causal mode:

```text
RenderedTurnArtifact.status = CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION
causal_packaging_eligible = true
```

Eligibility is not occurrence. CAN-025 remains the separate packaging authority and was not consumed here. ADP-019 alone decides `ADMIT | REJECT | DEFER | INVALID` and alone may create an event/advance V3 causal cursors.

Under accepted ADP-025, every rerender is a new candidate artifact identity/hash. Admission/rejection never transfers, even when visible text is byte-identical. The same CAN-024 mode receipt may remain provenance for multiple rerenders only if the mode decision itself is unchanged.

## 9. Caller-current-situation relation

CAN-024 consumes ADP-026 `interaction.mode_context` only; it never upgrades the truth/disposition of any caller-situation statement.

- ADP-026 `PRESENTATION_ONLY` remains presentation-only even in causal mode.
- Independently lawful `PROPOSED_CAUSAL_INPUT` in presentation mode is not submitted through this lane.
- The same state in causal mode may be eligible for separate packaging/admission, but remains noncausal and gains no epistemic authority.
- Transcript/session persistence never manufactures actor history.

## 10. Fail-closed states

Successful states:
`MODE_RESOLVED_DEFAULT_PRESENTATION_NONCAUSAL`, `MODE_RESOLVED_EXPLICIT_PRESENTATION_NONCAUSAL`, `MODE_RESOLVED_EXPLICIT_IN_WORLD_CAUSAL`, `MODE_RESOLVED_TURN_OVERRIDE`, `MODE_RESOLVED_ACTIVE_SESSION_DIRECTIVE`, `VALID_EMPTY_EXPLICIT_MODE_DIRECTIVE_SET`.

Missing/unknown/conflict states:
`INTERACTION_MODE_SOURCE_MISSING`, `INTERACTION_MODE_SOURCE_AUTHORITY_UNKNOWN`, `INTERACTION_MODE_VALUE_UNKNOWN`, `INTERACTION_MODE_SCOPE_UNKNOWN`, `INTERACTION_MODE_CURRENT_STATE_UNKNOWN`, `INTERACTION_MODE_STALE_CURSOR`, `INTERACTION_MODE_UPDATE_CONFLICT`, `INTERACTION_MODE_CONFLICT`.

Integrity/forbidden states:
`INTERACTION_MODE_DIRECTIVE_ID_COLLISION`, `INTERACTION_MODE_SUBJECT_MISMATCH`, `INTERACTION_MODE_SESSION_MISMATCH`, `INTERACTION_MODE_CURSOR_INTEGRITY_FAILURE`, `INTERACTION_MODE_SOURCE_HASH_MISMATCH`, `INTERACTION_MODE_RECEIPT_HASH_MISMATCH`, `INTERACTION_MODE_INTEGRITY_FAILURE`, `FORBIDDEN_RENDERER_MODE_SELECTION`, `FORBIDDEN_MODEL_MODE_SELECTION`, `FORBIDDEN_CONTENT_TO_CAUSAL_MODE_INFERENCE`, `FORBIDDEN_PRIOR_TURN_MODE_INHERITANCE`, `FORBIDDEN_NONACTUAL_SCENARIO_CAUSAL_MODE`, `FORBIDDEN_NONCAUSAL_V3_SUBMISSION`, `FORBIDDEN_MODE_TO_ADMISSION_COLLAPSE`, `FORBIDDEN_RERENDER_ADMISSION_TRANSFER`, `FORBIDDEN_SESSION_TO_CAUSAL_HISTORY_PROMOTION`, `FORBIDDEN_V2_CURSOR_TO_V3_CAUSAL_CURSOR_PROMOTION`.

Every unresolved/error state fails closed against causal eligibility; diagnostic state remains explicit.

## 11. Replay/provenance

Replay binds policy/registry hashes; session/turn/V2-cursor identity; active session-state ref/hash; explicit turn directive if any; all same-rank considered directives needed for conflict proof; ADP-026 statement/authority/source/subject/effective-time provenance; scope/operation; expected prior session state for updates; resolution/effective mode/execution posture; packaging eligibility; required outbound status; receipt hash; formal session-close ref when relevant; integrity outcome.

Forbidden replay inputs: wall clock, mutable latest, transcript keyword search, model output, topic/emotion/relationship inference, filesystem/list order, unstored defaults, prior receipt as next-turn authority, or a V3 causal cursor inferred from a V2 cursor.

## 12. Hostile fixtures

1. omitted mode -> default noncausal; 2. explicit noncausal TURN -> no submission; 3. explicit causal TURN -> pending candidate only; 4. prior causal turn + no new/session directive -> next default noncausal; 5. explicit causal SESSION -> lawful prospective carry; 6. causal SESSION + presentation TURN override -> this turn noncausal; 7. presentation SESSION + causal TURN override -> this turn eligible only; 8. stale cursor -> no causal eligibility; 9. prospective mode change -> new receipt, no rewrite; 10. wrong expected prior session hash -> update conflict; 11. conflicting same-rank directives -> conflict/noncausal posture; 12. renderer escalates mode -> reject; 13. emotion selects causal -> forbidden; 14. relationship framing selects causal -> forbidden; 15. topic keyword selects causal -> forbidden; 16. noncausal artifact submitted to V3 -> forbidden; 17. causal mode treated as ADMIT -> forbidden; 18. ADP-019 rejects candidate -> audit-only noncausal; 19. ADP-019 defers -> pending noncausal; 20. rerender after admission -> new candidate; 21. byte-identical rerender -> distinct candidate/new court; 22. persisted noncausal transcript -> no V3 history/memory; 23. summary claims presentation text really occurred -> no authority; 24. prior mode receipt used as next-turn authority -> forbidden; 25. nonactual scenario requests causal -> forbidden; 26. causal source lacks ADP-026 authority/hash -> fail closed; 27. wrong session/subject -> mismatch; 28. directive/receipt tamper -> integrity failure; 29. V2 cursor used as V3 causal cursor -> reject; 30. ADP-026 PRESENTATION_ONLY in causal mode -> no upgrade; 31. ADP-026 PROPOSED_CAUSAL_INPUT in presentation mode -> no lane submission; 32. same in causal mode -> packaging eligibility only; 33. session close then old causal directive -> stale; 34. mutable `last_mode=causal` after restart -> reject; 35. causal mode but no valid rendered artifact -> no forced candidate; 36. same mode receipt across rerenders -> mode provenance only, admission artifact-specific.

## 13. GOVERNING_SPIRIT_CHECK

`GOVERNING_SPIRIT_CHECK = APPLICABLE__PASS`

Hard authority fixes two modes, default noncausal, explicit causal eligibility, exact-artifact admission and V3 sovereignty. Genuine ambiguity remained over multi-turn causality: require a fresh declaration every turn; carry prior causal turns implicitly; or permit **explicit session-scoped state with turn-local overrides**. Choice: the third. It is minimum sufficient machinery for deliberate causal sessions while preventing conversational momentum from becoming causal authority. The Governing Spirit supplied no new mode, event or effect semantics.

## 14. CONSUMER_RELEASE_SUFFICIENCY

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT_FOR_CAN_024_JURISDICTION__NOT_STANDALONE_V2_P9_OR_V2_P10_RELEASE`

CAN-024 fully supplies its mode/default/source/scope/cursor/update/receipt/fail-closed contract. V2-P9 still requires separately governed CAN-025 plus implementation/physical ADP-019 wiring and packet acceptance. No sibling Batch-02 result was consumed. V2-P10 receives the application-visible mode receipt/hostile invariants but remains downstream of broader application and V3 terminal/order gates.

## 15. Final verdict

No production code was modified. V2/V3 were not implemented. No historical ZIP was used. No sibling W2 Batch-02 return was consumed.

`CAN_024_V2_INTERACTION_MODE_CANONICALIZATION = PASS`
