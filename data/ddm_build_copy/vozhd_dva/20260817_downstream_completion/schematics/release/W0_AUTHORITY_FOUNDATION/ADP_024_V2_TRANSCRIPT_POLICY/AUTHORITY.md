# MUST-024 — V2/Application Transcript Retention & Summarization Authority

**Authority ID:** `V2_TRANSCRIPT_RETENTION_SUMMARIZATION_POLICY`  
**Authority:** `MUST-024` / `ADP-024`  
**Version:** `1.0.0` (`MUST-024@1.0.0`)  
**Owner:** V2/application persistence boundary  
**Architecture:** `CLOSED__NOT_REOPENED`  
**Historical archive SHA256:** `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086` — `EXACT_MATCH`

## 1. Decision

V2/application transcript persistence is a **noncausal persistence and audit namespace**. Retaining, summarizing, compacting, deleting, or closing a V2 session never creates or changes V3 memory, belief, biography, relationship truth, generated history, or a V3 causal cursor.

`PRESENTATION_NONCAUSAL` is the default transcript lane. An in-world transcript occurrence exists only after V3 admits the **exact observable artifact/hash** under separately governed V3 admission authority. MUST-024 preserves that identity and evidence but does not perform admission.

A transcript summary is always a separately typed `V2_TRANSCRIPT_SUMMARY`. It cannot silently replace an exact message/artifact where exact identity is required. Missing/deleted transcript content means only that V2/application payload is unavailable; it does **not** mean the actor forgot.

## 2. Jurisdiction

MUST-024 owns only: artifact retention classes/states; exact vs lossless-compacted vs derived-summary representations; cursor stability; hash/provenance lineage; summary provenance; deletion eligibility; immutable audit preservation; session close; missing/unknown/integrity behavior; hostile retention fixtures.

It does **not** own V3 causal memory/recall/accessibility (`MUST-016`), actor belief/claim accessibility, V3 event admission/effects/cursors (`MUST-019`), V2 interaction-mode semantics (`CAN-024`), V2→V3 packaging (`CAN-025`), EnergeticField semantics (`CAN-021`), render RNG/model policy (`MUST-025`), caller-current-situation authority (`MUST-026`), or legal/statutory retention periods.

A later accepted privacy/replay/storage authority may narrow deletion eligibility, but cannot make retention state psychologically causal or erase V3-owned admission/history obligations.

## 3. Evidence disposition

Binding evidence inspected: `state/CURRENT_STATE.md`; whole-machine closure ruling; implementation-release synthesis ruling; RA-R00 `RESULT.md`/`RESULT.json`; V2 completion ruling; TD-R06 V2 result; TD-R07 whole-machine result; V3/V2 recovery-priority ruling; W0 launch register.

The required archive was recomputed before inspection and matched the expected SHA exactly. Directly inspected recovered sources include `server/session_db.py`, `server/session_state.py`, `server/routes/chat.py`, `server/chat/turn.py`, `server/routes/session_bootstrap.py`, `server/routes/session_summary.py`, `scripts/migrate_app_sessions.py`, `v2/conversation_engine.py`, and `v2/PERSONA_CONVERSATION_ENGINE_SPEC.md`. They show full transcript persistence, monotonic turn IDs, bounded recent-history prompt use, EnergeticField/topic continuity, and per-turn render artifacts, but **no terminal retention/summarization/compaction/deletion authority**. Historical monolithic “Relationship Memory” is superseded by the binding V3-memory/V2-session split.

At exact base `655da47b9e03ab310ed4b7fa65ceec9b9d04d3bc`, no current `server/session_db.py`, `server/session_state.py`, `v2/conversation_engine.py`, or equivalent transcript runtime implementation was present. Therefore recovered source is continuity evidence only. Historical V5/DDM supplied zero authority.

## 4. Artifact classes

| Class | Meaning | Causal by persistence? |
|---|---|---|
| `V2_TRANSCRIPT_MESSAGE` | exact user/visible transcript item | no |
| `RENDERED_TURN_ARTIFACT` | immutable V2 rendered candidate/output | no; exact identity is pin-required when used in causal mode |
| `V2_SESSION_STATE` | V2 transcript cursor + application/session metadata | no |
| `V2_SESSION_DERIVED_CONTINUITY` | EnergeticField/topic-stream-like session state | no; no psychological authority |
| `V2_RENDER_AUDIT_REF` | render/audit receipt reference | no |
| `EXTERNAL_INTERACTION_PROPOSAL_REF` | V2/app→V3 proposal reference | pending, not causal |
| `V3_ADMISSION_RECEIPT_REF` | V3-owned admission/rejection evidence preserved by V2/app | V3 owns semantics |
| `V2_TRANSCRIPT_SUMMARY` | explicitly derived noncausal summary | no |
| `V2_COMPACTION_MANIFEST` | compaction/deletion lineage | no |
| `V2_DELETION_TOMBSTONE` | proof payload was deleted under policy | no |
| `V2_SESSION_CLOSE_RECEIPT` | final V2 cursor/lineage closure receipt | no |

## 5. Representations and retention states

Representations:

- `RAW_EXACT`: original exact payload.
- `LOSSLESS_COMPACTED_EXACT`: compressed/packed form from which the exact original payload is recoverable without semantic reconstruction. Artifact identity/cursor/hash identity do not change.
- `SUMMARY_DERIVED`: separate, noncausal summary with its own ID/hash. It never inherits source IDs/cursors and never satisfies exact artifact/event/admission identity.
- `LINEAGE_ONLY_TOMBSTONE`: payload deleted; immutable identity/hash/cursor/provenance/deletion receipt survive. It cannot exact-replay or later enter causal admission under the deleted identity.

Canonical retention states are `ACTIVE_EXACT`, `SEALED_EXACT`, `LOSSLESS_COMPACTED_EXACT`, `AUDIT_PINNED_EXACT`, `DELETION_ELIGIBLE`, `LINEAGE_ONLY_TOMBSTONE`, `MISSING_UNKNOWN`, and `INTEGRITY_FAILED`. `SUMMARY_DERIVED` is orthogonal and may coexist with source states.

Allowed transitions:

```text
ACTIVE_EXACT -> SEALED_EXACT
SEALED_EXACT -> LOSSLESS_COMPACTED_EXACT
SEALED_EXACT -> DELETION_ELIGIBLE
LOSSLESS_COMPACTED_EXACT -> DELETION_ELIGIBLE
DELETION_ELIGIBLE -> LINEAGE_ONLY_TOMBSTONE
SEALED_EXACT -> AUDIT_PINNED_EXACT
LOSSLESS_COMPACTED_EXACT -> AUDIT_PINNED_EXACT
```

Forbidden: `AUDIT_PINNED_EXACT -> LINEAGE_ONLY_TOMBSTONE`; summary→source exact identity; tombstone→causal admission under deleted identity.

Any causal-mode candidate in status pending V3 admission, rejected by V3, or admitted by V3 is `AUDIT_PINNED_EXACT`. It may be losslessly compacted while exact recoverability survives, but cannot become summary-only/hash-only/lineage-only under V2-local policy. Unknown admission status also retains exact and fails closed. A rerender is a new artifact/hash and cannot inherit another candidate's admission.

## 6. Cursor, hash, compaction, and summary lineage

V2 logical identity is `{session_id, transcript_cursor, artifact_id}`. Transcript cursors are monotonic/order-stable within the session namespace, never renumbered or reused after compaction/deletion, and preserve tombstoned positions as addressable gaps. Summaries never occupy source cursors.

The V3 causal/event cursor is a **different namespace**. V2 may preserve V3-returned cursor/event/receipt refs; V2 must never derive, advance, infer, or reconstruct a V3 causal cursor from V2 transcript position.

For every compacted/deleted artifact, preserve: session ID; artifact ID/class; transcript cursor; exact payload hash + hash algorithm/version; interaction mode; causal/admission status if known; source/producer ref; render/creation receipt ref where applicable; V3 context/snapshot hash where accepted replay requires it; policy/version and decision receipt.

Every `V2_COMPACTION_MANIFEST` must bind manifest ID/hash, session, source cursor range(s), ordered source artifact IDs+payload hashes (or immutable ordered manifest ref), source/result representations, lossless/lossy flag, encoding/version, `MUST-024@1.0.0`, policy trigger/basis, hold/pin evaluation, and summary ID/hash if one exists.

Every summary must bind its own ID/hash, source session/cursor ranges, ordered source artifact/hash lineage or immutable manifest ref, summary rule/type/version, summarizer/model identity/version where applicable, generation receipt/hash where applicable, policy version, explicit `NONCAUSAL_DERIVED_SUMMARY`, and verification state. It must preserve claim attribution: “user asserted X” may not become “X happened.” `UNVERIFIED_SUMMARY` cannot authorize deletion or exact substitution.

## 7. Deletion eligibility and immutable audit subset

Exact payload deletion is lawful only when **all** are true:

1. artifact is within V2/application transcript/session jurisdiction;
2. it is no longer required as `ACTIVE_EXACT`;
3. it is explicitly `PRESENTATION_NONCAUSAL`;
4. no pending, rejected, or admitted V3 proposal/receipt pins exact identity;
5. no stronger accepted replay/audit authority pins exact payload;
6. identity/hash/cursor/provenance lineage verifies and is sealed;
7. any surviving summary used for readable continuity is verified;
8. manifest+tombstone can commit atomically;
9. an explicit governed deletion trigger exists (e.g. accepted expiry rule, user/privacy request, administrator/governed decision); and
10. no hold/pin applies.

Any unknown predicate blocks deletion. No TTL, expiry, “reasonable retention,” or default storage horizon may be invented. No directive means retain the current representation.

Precedence: integrity/unresolved causal status > causal audit pin > stronger exact replay/audit hold > explicit retain/hold > explicit delete trigger with every eligibility predicate > retain current representation.

The immutable audit subset is: session ID; cursors/artifact IDs/classes; exact payload hashes for compacted/deleted artifacts; manifests/tombstones; summary provenance; interaction mode + causal/admission status; required render artifact/receipt IDs/hashes; proposal IDs + exact candidate hash; V3 admission/rejection receipt refs and available V3 event/checkpoint/cursor refs; session-close receipt; integrity-failure records. For pending/rejected/admitted causal artifacts, **exact recoverability itself** is immutable.

## 8. Session close and missing/unknown behavior

A formal close emits `V2_SESSION_CLOSE_RECEIPT` containing session ID, final V2 transcript cursor, final lineage hash/digest, interaction mode, outstanding pending causal proposals, authority/version, and close-integrity state. Close freezes that session cursor namespace, seals exact non-pending artifacts, leaves pending causal candidates audit-pinned, and creates no V3 memory/relationship/biography or causal-cursor movement. Disconnect/restart/browser unload is not a formal close unless such a receipt is recorded.

Fail closed:

- `UNKNOWN_ARTIFACT_CLASS` / `UNKNOWN_RETENTION_POLICY`: retain; do not invent deletion authority.
- `UNKNOWN_CAUSAL_STATUS`: retain exact.
- `MISSING_TRANSCRIPT_ARTIFACT`: surface missing/unknown; never infer forgetting.
- `EXACT_ARTIFACT_UNAVAILABLE`: exact replay/admission identity unavailable; no summary substitution.
- cursor gap without tombstone, cursor reuse/renumber, payload-hash mismatch, broken compaction lineage, or admission-hash mismatch: `INTEGRITY_FAILED`; no deletion or causal use.
- `UNVERIFIED_SUMMARY`: cannot authorize deletion/substitution.
- missing admission receipt: causal occurrence is not established.
- delete request on `AUDIT_PINNED_EXACT`: `DELETE_BLOCKED_IMMUTABLE_AUDIT`.
- tombstoned artifact requested for later causal admission: reject old identity; summary cannot resurrect it.

## 9. V3-memory separation law

```text
V2 namespace:
  transcript/session persistence
  summaries / compaction / tombstones
  V2 continuity state
  application/audit lineage

V3 namespace:
  generated/admitted causal events
  memory formation / forgetting / recall / accessibility
  belief/knowledge/relationship/biography truth where governed
  causal event/cursor history
```

V2 may preserve references/receipts emitted by V3. No V2 retention state may create, update, delete, infer, or prove V3 memory/accessibility. Neither retention nor deletion has psychological meaning.

## 10. Exact consumers and sufficiency

Exact semantic consumers from RA-R00 are `V2-P4`, `V2-P6`, and `V2-P10`.

- `V2-P4`: typed noncausal session/turn substrate, cursor/state/manifest/summary/tombstone/close handling.
- `V2-P6`: enforce causal-memory/relationship vs V2-session separation.
- `V2-P10`: enforce application retention/privacy behavior, immutable audit subset, causal pinning, and hostile fixtures.

V2-P9/V3 seam may reference exact retained candidates because separate accepted authority requires exact admission identity; it cannot widen MUST-024.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`: MUST-024 is complete for its named semantic consumers. This does not independently release those packets; their other RA-R00 blockers remain binding.

## 11. Hostile fixtures

| ID | Attack | Required outcome |
|---|---|---|
| H024-01 | presentation transcript → V3 memory | reject noncausal-session→memory |
| H024-02 | deleted turn → actor forgot | reject psychological inference |
| H024-03/04 | summary → relationship truth / objective fact | reject semantic laundering |
| H024-05 | admitted utterance deleted because hash+summary remain | `DELETE_BLOCKED_IMMUTABLE_AUDIT` |
| H024-06/07 | rejected/pending causal candidate discarded or summary-only | `AUDIT_PINNED_EXACT` |
| H024-08/09 | compaction renumbers cursor / summary takes source cursor | integrity/identity failure |
| H024-10/11 | hash mismatch or unprovenanced summary authorizes delete | no delete; fail closed |
| H024-12 | claimed causal event missing receipt | not established causal; retain exact |
| H024-13 | rerender inherits prior admission | new hash requires new admission |
| H024-14/15 | session close or EnergeticField creates biography/psychology | reject V2→V3 semantic promotion |
| H024-16 | deleted cursor silently shifted | `INTEGRITY_FAILED`; preserve gap |
| H024-17 | unknown class auto-deleted by generic TTL | fail closed retain |
| H024-18 | tombstone reconstructed from summary under old identity | reject identity resurrection |
| H024-19 | V2 cursor advances V3 causal cursor | reject namespace collapse |
| H024-20 | delete request targets audit-pinned exact | `DELETE_BLOCKED_IMMUTABLE_AUDIT` |
| H024-21 | summary labeled as exact transcript | reject silent substitution |
| H024-22 | absent directive causes invented TTL | retain; no heuristic TTL |

## 12. Final verdict

No production code is modified. No V2 application is implemented. No V3 causal-memory/admission semantics are created. Whole-machine architecture remains closed.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`

`ADP_024_V2_TRANSCRIPT_POLICY_AUTHORITY = PASS`
