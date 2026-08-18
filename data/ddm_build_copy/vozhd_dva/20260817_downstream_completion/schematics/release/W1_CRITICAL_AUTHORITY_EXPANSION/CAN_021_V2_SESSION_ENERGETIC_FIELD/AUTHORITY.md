# CAN-021 — V2 Session Energetic-Field Canonicalization

**Authority ID:** `V2_SESSION_ENERGETIC_FIELD_RULE`  
**Authority version:** `1.0.0`  
**RA-R00 item:** `CAN-021`  
**Cell:** `W1-B03-05`  
**Owner:** V2/application session-presentation boundary  
**Mode:** authority canonicalization only  
**Status:** `CANONICALIZED__ARCHITECTURE_UNCHANGED`  
**Verdict:** `PASS`  
**Launch base:** `db961be677d5112073e16e5d452853971861cdb6`

## 1. Bounded disposition

This canonicalization preserves the recovered V2 idea that a conversation may carry **session-only continuity** across turns: an EnergeticField, active topic streams, topic gravity/continuity, avoidance inertia, and directly related presentation/session state. It binds that continuity to a typed noncausal V2/application session contract.

It does not create V3 memory, generated biography, relationship truth, actor psychology, organismic vitality, salience, expression register, response moves, face-risk/effort/attention, transcript retention policy, or causal conversation semantics.

```text
V2_SESSION_STATE != V3_CAUSAL_MEMORY
SESSION_TOPIC_STREAM != ACTOR_PERSISTENT_CONCERN
SESSION_AVOIDANCE_INERTIA != WOUND_OR_RELATIONSHIP_TRUTH
SESSION_ENERGETIC_FIELD != ORGANISMIC_VITALITY
SESSION_PERSISTENCE_OR_REPETITION != GENERATED_BIOGRAPHY
```

`VALID_EMPTY` is lawful.

## 2. Direct archive verification

Required archive: `Rawlsing_code_bundle_staging.zip`.

- expected SHA256: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- computed directly from the archive bytes: `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`
- verdict: `EXACT_MATCH`
- entries: `13,138`

Recovered V2/V3/server source is continuity and authority-recovery evidence only. Historical V5/DDM has zero authority over current V550+.

## 3. Governing and accepted authority consumed

Binding evidence inspected: Batch-03 launch register; `CURRENT_STATE.md`; `RAWLSING_GOVERNING_SPIRIT.md`; V2/V3 completion rulings; whole-machine closure; implementation-release synthesis; W0 closure; first-batch and Batch-02 adjudication rulings; RA-R00; accepted TD-R06; and relevant accepted W0 authority.

Exact accepted dependencies consumed:

1. `ADP-024 / V2_TRANSCRIPT_RETENTION_SUMMARIZATION_POLICY@1.0.1` — transcript/session identity, V2 cursor, compaction/summary lineage, retention decisions and formal session close. CAN-021 does not re-own retention or compaction.
2. `ADP-025 / V2_RENDER_MODEL_RANDOMNESS_VERSION_POLICY@1.0.0` — opaque render receipt/request/artifact provenance refs only. CAN-021 does not re-own rendering.
3. `ADP-026 / CALLER_CURRENT_SITUATION_AUTHORITY@1.0.0` — exact source/subject/effective-time bounded current-situation refs may be retained as session context; persistence cannot promote them into generated truth.
4. Accepted V2 constitutional law: **V3 generates the life; V2 expresses the generated life.**

Accepted `ADP-016` was inspected for noncollapse: V3 causal memory explicitly excludes V2 transcript/session state as a direct memory source.

No Batch-03 sibling return was used as authority. The active/unadjudicated CAN-009 repair was not consumed; only already accepted V3 stage jurisdiction and the Batch-02 ruling that organismic/vitality semantics are a separate V3 lane were used.

## 4. Recovered source inventory and dispositions

| Source/mechanism | Direct finding | Disposition |
|---|---|---|
| `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md` | EnergeticField across turns; topic gravity, avoidance inertia, ActiveStream continuity. | **ADAPT** to session-only noncausal contract. |
| `v2/conversation_engine.py::EnergeticField` | Per-turn field plus recent turns/hooks/effort and active streams. | **ADAPT** container/continuity; quarantine numeric/default semantics. |
| `ActiveStream` / `update_topic_streams` | strength/imprint decay, primary ranking/floor, internalized tags, five-stream cap. | Preserve stream continuity only; **remove canonical rank/strength/primary/psyche inference**. |
| `server/chat/turn.py` | Carries field in memory across turns; hard-codes `persona_effort="medium"` on one path. | **ADAPT** continuity; reject effort default. |
| `server/session_state.py` | In-memory session and resume/persist substrate. | **ADAPT** lifecycle substrate only. |
| `server/session_db.py` | Serializer explicitly drops `energetic_field`; loader has a restore hook although SELECT/INSERT omit it. | **REPLACE** with typed persistence and fail-closed restore. |
| `server/routes/session_bootstrap.py` | `energetic_field` optional in new session record. | Bootstrap = `VALID_EMPTY`, not zero-filled state. |
| `server/routes/session_summary.py` | Public summary omits field. | Preserve nonpublic session boundary. |
| `server/routes/start.py`, `discovery.py` | Session creation/persistence; no terminal field reset/end rule. | Lifecycle continuity evidence only. |
| accepted TD-R06 | EnergeticField/topic gravity/avoidance/active streams are V2 session continuity; causal truth remains V3. | Binding architecture continuity. |

Current-terrain checks at the launch base found no present root `v2/conversation_engine.py` or `server/session_state.py`; historical implementation is not current production authority.

## 5. Exact owner and consumer

`owner = V2/application session-presentation boundary`.

CAN-021 owns only the typed `V2_SESSION_ENERGETIC_FIELD`, session-only topic-stream and avoidance-continuity records, sparse exact refs to recovered session presentation-signal slots, and field bootstrap/update/reset/restore/end/replay semantics.

Primary consumer: **`V2-P4` — typed noncausal session/turn substrate**.

CAN-021 does **not** own CAN-016 salience, CAN-019 relationship expression, MUST-023 boundary/face-risk/effort/attention, ADP-024 retention/compaction, ADP-025 render policy, ADP-026 caller truth, V3 causal memory, or V3 material/organismic/vitality state.

## 6. Canonical session field / stream contract

### `V2_SESSION_ENERGETIC_FIELD`

Epistemic class: `V2_SESSION_STATE__PRESENTATION_NONCAUSAL`. Scope: exactly one `session_id`; never actor-global and never silently portable across sessions.

Required fields or semantic equivalents:

```text
field_id
session_id
authority_id = V2_SESSION_ENERGETIC_FIELD_RULE
authority_version = 1.0.0
lifecycle_state
revision_id
previous_revision_ref | null
last_v2_cursor_ref | null
topic_stream_refs[]
avoidance_continuity_refs[]
presentation_signal_refs[]
caller_current_situation_refs[]
render_receipt_refs[]
update_receipt_refs[]
integrity_state
```

Lifecycle states:
`VALID_EMPTY | ACTIVE_SESSION_ONLY | RESET_EMPTY | SESSION_ENDED | MISSING_OR_UNAVAILABLE | INTEGRITY_FAILED`.

Absence of a signal is not numeric zero and not a neutral psychological fact.

### `V2_SESSION_TOPIC_STREAM`

A topic stream means only that a stable topic identity was lawfully recorded/touched as presentation-session continuity in this exact session.

Required fields: `stream_id`, `session_id`, `topic_key`, exact `topic_key_source_ref`, first/last V2 cursor refs, ordered touch refs, state, authority ID/version.

States: `ACTIVE_SESSION_ONLY | RESET_CLEARED | SESSION_ENDED`.

There is **no canonical strength, imprint depth, primary stream, ranking, decay, floor, TTL or maximum stream count**. Repetition is session evidence only; it is not persistent concern and cannot choose future salience.

### Topic gravity

Canonical topic gravity is **continuity evidence only**: exact repeated/touched topic-stream provenance may be retained. CAN-021 supplies no numeric gravity, priority, salience multiplier or concern inference.

### `V2_SESSION_AVOIDANCE_CONTINUITY`

An avoidance record means only that a **separately governed V2 presentation disposition** previously marked avoidance/deflection for a topic in this session. It carries exact source-disposition and cursor refs.

No numeric inertia or decay exists. Persistence is not wound, fear, shame, relationship truth, memory, belief, or generated motive.

### Recovered EnergeticField signal slots

The recovered dimensions remain canonical only as sparse **source-owned reference slots**:

- `SESSION_TENSION_CONTEXT`
- `SESSION_INTIMACY_CONTEXT`
- `SESSION_CURIOSITY_CONTEXT`
- `SESSION_BOREDOM_CONTEXT`
- `SESSION_TOPIC_PERSISTENCE_CONTEXT`
- `SESSION_DEMAND_CONTEXT`

CAN-021 defines no scalar value, threshold, decay, comparison or downstream effect. A slot may carry an exact signal ref only when a separately accepted producer owns that value. Otherwise it is absent/unknown.

`last_user_hooks` are not re-extracted here. `last_persona_effort` is not owned here; MUST-023 owns effort semantics.

## 7. Admissible inputs / fail-closed source law

Admissible:

- ADP-024 transcript/session cursor or artifact refs for ordering/provenance only;
- ADP-024 compaction/tombstone refs and formal close receipt;
- ADP-025 render receipt refs for provenance only;
- ADP-026 current-situation refs under original subject/source/effective-time scope;
- exact output refs from an **already accepted** V2 presentation-semantic owner supplying a lawful topic touch, avoidance disposition or session signal;
- explicit application session lifecycle event for bootstrap/reset/restore.

Inadmissible as semantic authority: raw transcript/summary scans; keyword frequency/repetition as psyche; structural priors; analyst-only V3 truth; V3 causal memory copied into session state; generated relationship truth converted to avoidance; organismic vitality renamed as session energy; rendered prose as self-authorizing truth; same-batch sibling returns; legacy numeric field/stream values.

If an update requires an unaccepted owner, the field stays unchanged/valid-empty. Missing authority is not repaired locally.

## 8. Update / reset / end / compaction law

**Bootstrap:** create/bind `VALID_EMPTY`. No zero tension/intimacy/boredom, default effort, default topic or primary stream.

**Turn update:** only exact admitted noncausal session update inputs may create/touch records. Every semantic change emits a `V2_SESSION_FIELD_UPDATE_RECEIPT` (or equivalent) binding session ID, prior/result revision, V2 cursor, update kind, ordered source refs, source authority versions, CAN-021 version and integrity state. No admitted update means no semantic change.

**Reset:** explicit application/session reset may clear current materialized continuity to `RESET_EMPTY`/`VALID_EMPTY`, preserving prior revision lineage and a reset receipt. It does not delete transcript and is never V3 forgetting.

**Restore:** restore exact/losslessly recoverable field state and provenance. If prior field state is known to have existed but cannot be recovered, return `MISSING_OR_UNAVAILABLE`; never rebuild it from transcript, summary, repetition or current prompt. This rejects the recovered DB loss mode.

**End:** only verified ADP-024 `V2_SESSION_CLOSE_RECEIPT` seals the field as `SESSION_ENDED`. Browser disconnect/restart/unload is not semantic end. No updates after seal.

**Compaction:** ADP-024 exclusively controls retention/deletion/compaction. CAN-021 follows exact manifest/tombstone refs. Summary or compacted prose can never create/recompute topic, avoidance or energetic state. Compaction/reset never imply V3 forgetting.

**Cross-session:** a new session starts `VALID_EMPTY`, even for the same actor/caller/persona. No old stream/avoidance state auto-imports without separate authority.

## 9. Transcript-policy boundary

ADP-024 owns retention/deletion/compaction, cursor/tombstone identity, exact-content holds, summary lineage and formal close. CAN-021 may reference those records but may not choose TTLs, delete/summarize content, renumber cursors, convert retention duration into concern, or convert deletion into forgetting.

A committed field revision is a `V2_SESSION_STATE` / `V2_SESSION_DERIVED_CONTINUITY` artifact under ADP-024 retention law. CAN-021 creates no second retention policy.

## 10. Numeric/default disposition

No canonical numeric semantics exist in CAN-021 v1 for energy, topic gravity, avoidance inertia or stream strength.

Compatibility/migration/audit-only; semantic use denied:

- recovered 0..1 energetic scalars and zero defaults;
- `DECAY = 0.85` and additive thresholds/bumps/clamps;
- `MAX_RECENT_TURNS = 8` as semantic memory horizon;
- ActiveStream strength/imprint values/defaults;
- stream decays `0.78` / `0.97`;
- `PRIMARY_STRENGTH_FLOOR = 0.25`;
- `IMPRINT_BUMP_ON_TOUCH = 0.06`;
- `MAX_ACTIVE_STREAMS = 5`;
- weak-stream cutoff `0.12`;
- new-stream defaults `0.7 / 0.25`;
- `primary_stream_index` as semantic priority;
- default/hard-coded `last_persona_effort = "medium"`.

V2 cursor/turn ordinals remain session mechanics under their owner. Exact cardinality may be audited but cannot become strength, rank, salience, concern or psychology without separate authority.

## 11. Causal-memory / relationship / vitality noncollapse

`V2_SESSION_STATE != V3_CAUSAL_MEMORY`: session continuity cannot form, erase, degrade, recall or prove V3 memory. Repetition is not memory formation. If V3 later admits an exact interaction and separately forms memory under ADP-016, that memory remains V3-owned.

`SESSION_AVOIDANCE_INERTIA != WOUND_OR_RELATIONSHIP_TRUTH`: session avoidance cannot assert trust, wound, attachment, relationship history or actor motive. CAN-019 and V3 relationship truth remain separate.

`SESSION_ENERGETIC_FIELD != ORGANISMIC_VITALITY`: “energetic” is presentation/session terminology only. No session scalar may alias, overwrite or back-propagate V3/CAN-009 embodied state.

Session state can matter causally only through separately governed exact V2→V3 packaging and V3 admission. CAN-021 neither packages nor admits it.

## 12. Replay / provenance

Each field revision preserves stable session/field identity; CAN-021 version; prior/result revision refs; exact V2 cursor when turn-bound; ordered source refs and source authority versions; ADP-025 receipt refs where used; ADP-026 statement refs where used; reset/restore/close refs; integrity state.

Same ordered admitted session inputs + lifecycle events + CAN-021 version must reproduce the same materialized field without hidden wall clock, filesystem order, transcript rescanning, mutable “latest” state or invented defaults.

If ADP-024 lawfully removes exact noncausal source bytes, the committed field revision and immutable lineage may remain audit evidence. Missing exact replay input must be disclosed; summaries cannot reconstruct it.

Broken session identity, cursor/source mismatch, revision-chain break, missing source authority, update after close, unauthorized cross-session import, lost-known-state→valid-empty collapse, or prose reconstruction is `INTEGRITY_FAILED`.

## 13. Hostile fixtures

1. New session zero-fills legacy scalars / default effort → `VALID_EMPTY`, reject defaults.
2. Repeated “family” text creates actor concern/topic stream without governed topic source → reject.
3. 100-turn lawful stream becomes V3 memory/belief → reject.
4. Repeated avoidance proves wound/relationship truth → reject.
5. Legacy tension/strength/primary-floor promoted canonically → quarantine.
6. Hard-coded `medium` becomes actor effort → reject; MUST-023 owns effort.
7. Known field lost on DB restore and rebuilt from transcript → `MISSING_OR_UNAVAILABLE`, no reconstruction.
8. Field reset deletes transcript or causes V3 forgetting → reject.
9. Disconnect/restart treated as formal close → reject without ADP-024 close receipt.
10. Transcript summary creates topic gravity after compaction → reject.
11. Repeated caller “I am exhausted” depletes organismic vitality → preserve source-bound ADP-026 context only; no V3 mutation.
12. Rendered text self-updates topic/avoidance → reject absent governed presentation disposition.
13. Same actor starts new session and old streams auto-import → reject; new field `VALID_EMPTY`.
14. Structural/analyst-only truth seeds field → reject.
15. Compaction breaks cursor/source lineage and field continues → `INTEGRITY_FAILED`.
16. V3-admitted utterance makes session field the actor memory → reject; ADP-016 owns memory formation.
17. Legacy strongest/primary stream bypasses CAN-016 salience → reject.
18. Update after formal close receipt → reject / `INTEGRITY_FAILED`.

## 14. GOVERNING_SPIRIT_CHECK

**Status:** `APPLIED_AS_TIE_BREAK_ONLY`.

Hard authority fixes noncollapse and forbids automatic promotion of legacy numeric/default behavior. It leaves a machine-shape choice: retain a scored historical vector as canonical scaffolding, or bind the recovered meaning through sparse exact session records and leave unsupported magnitude/rank semantics absent.

Chosen: **sparse exact-reference/event continuity**. Legacy scored payload may survive only as compatibility/audit data with semantic use denied.

Decisive principles: minimum sufficient machinery; lawful absence/valid-empty; provenance/replay over reconstruction; presentation must not become psyche or causal truth; no duplicated semantic ownership.

`new_semantics_created_by_spirit = false`.

## 15. CONSUMER_RELEASE_SUFFICIENCY

**Status:** `PARTIAL`.

If Vozhd accepts this result, the bounded CAN-021 semantic blocker is closed for `V2-P4`. V2-P4 remains independently blocked on:

- `MUST-023 / V2_BOUNDARY_FACE_RISK_EFFORT_ATTENTION_RULE`.

ADP-024 and ADP-026 are already accepted. This authority does not release V2 production by itself.

## 16. Final token

`CAN_021_V2_SESSION_FIELD_CANONICALIZATION = PASS`
