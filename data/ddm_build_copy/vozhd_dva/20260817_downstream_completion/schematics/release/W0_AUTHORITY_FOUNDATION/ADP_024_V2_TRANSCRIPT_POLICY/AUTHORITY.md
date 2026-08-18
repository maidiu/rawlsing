# MUST-024 — V2/Application Transcript Retention & Summarization Authority

**Authority ID:** `V2_TRANSCRIPT_RETENTION_SUMMARIZATION_POLICY`  
**Authority:** `MUST-024` / `ADP-024`  
**Version:** `1.0.1` (`MUST-024@1.0.1`)  
**Owner:** V2/application persistence boundary  
**Architecture:** `CLOSED__NOT_REOPENED`  
**Historical archive SHA256:** `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086` — `EXACT_MATCH`

## 1. Constitutional law

V2/application transcript persistence is a **noncausal persistence and audit namespace**. Retention, summarization, compaction, deletion, or session close never creates or changes V3 memory, belief, biography, relationship truth, generated history, or a V3 causal cursor. Transcript deletion is not actor forgetting; transcript retention is not actor memory.

`PRESENTATION_NONCAUSAL` is the default transcript lane. An in-world occurrence exists only after V3 admits the **exact artifact/hash** under separately governed V3 admission authority. MUST-024 preserves required artifact/ref/receipt evidence but does not perform admission or own causal history.

A summary is always a separately typed `V2_TRANSCRIPT_SUMMARY`, with its own ID/hash and source lineage. It cannot create memory, belief, biography, relationship truth, or generated fact; it cannot silently replace exact source identity.

```text
artifact identity immutability != physical exact-content retention duration
```

Immutability means an existing artifact cannot be edited, replaced, renumbered, or reused under the same identity. Retention policy separately determines whether exact bytes must remain recoverable. Deletion never permits identity reuse or historical rewriting.

## 2. Jurisdiction and evidence

MUST-024 owns artifact/representation classes; immutable identity; exact-content requirements/holds; cursor stability; hash/provenance lineage; summary/compaction provenance; deletion eligibility; retention/privacy/delete decision receipts; immutable audit subset; session-close and fail-closed behavior.

It does not own V3 causal memory (`MUST-016`), V3 admission/effects/cursors (`MUST-019`), V2 interaction mode (`CAN-024`), V2→V3 packaging (`CAN-025`), EnergeticField semantics (`CAN-021`), render RNG/model policy (`MUST-025`), caller-situation authority (`MUST-026`), or legal/statutory retention periods.

Binding evidence inspected: current state; whole-machine closure; implementation-release synthesis; RA-R00 MD/JSON; V2 completion ruling; TD-R06; TD-R07 conversation/replay findings; V3/V2 recovery-priority ruling; W0 launch register. The required archive was recomputed for this continuation and exactly matched the expected SHA. Direct recovered-source inspection included `server/session_db.py`, `server/session_state.py`, chat/session routes, `scripts/migrate_app_sessions.py`, `v2/conversation_engine.py`, and the V2 conversation spec. Those sources show transcript persistence, monotonic turn IDs, bounded prompt-history use, session continuity and render artifacts, but no terminal retention/summarization/compaction/deletion authority. Historical V5/DDM has zero authority.

## 3. Artifact and representation model

Required classes include `V2_TRANSCRIPT_MESSAGE`, `RENDERED_TURN_ARTIFACT`, `V2_SESSION_STATE`, `V2_SESSION_DERIVED_CONTINUITY`, `V2_RENDER_AUDIT_REF`, `EXTERNAL_INTERACTION_PROPOSAL_REF`, `V3_ADMISSION_RECEIPT_REF`, `V2_TRANSCRIPT_SUMMARY`, `V2_COMPACTION_MANIFEST`, `V2_DELETION_TOMBSTONE`, `V2_REJECTION_AUDIT_TOMBSTONE`, `V2_RETENTION_DECISION_RECEIPT`, and `V2_SESSION_CLOSE_RECEIPT`.

Representations:

- `RAW_EXACT` — original exact payload.
- `LOSSLESS_COMPACTED_EXACT` — exact original recoverable without semantic reconstruction; identity/cursor/hash unchanged.
- `SUMMARY_DERIVED` — separate noncausal artifact; never exact-source identity.
- `LINEAGE_ONLY_TOMBSTONE` — exact payload absent; immutable identity/hash/cursor/provenance/deletion receipt survive.

Every created source/render artifact is `IDENTITY_IMMUTABLE`.

Exact-content requirement is a separate axis:

- `EXACT_REQUIRED_PENDING_ADMISSION`;
- `EXACT_REQUIRED_CAUSAL_REPLAY`;
- `EXACT_REQUIRED_SEPARATE_HOLD`;
- `EXACT_NOT_INTRINSICALLY_REQUIRED`;
- `EXACT_REQUIREMENT_UNKNOWN`.

Content states are `ACTIVE_EXACT`, `SEALED_EXACT`, `LOSSLESS_COMPACTED_EXACT`, `DELETION_ELIGIBLE`, `LINEAGE_ONLY_TOMBSTONE`, `MISSING_UNKNOWN`, and `INTEGRITY_FAILED`. Summary state is orthogonal.

## 4. Causal-status retention law

### A. Pending causal candidate

While status is `CANDIDATE_NONCAUSAL_PENDING_V3_ADMISSION`, exact content is `EXACT_REQUIRED_PENDING_ADMISSION`.

- exact artifact/content MUST remain recoverable;
- lossless compaction is allowed only if exact recovery verifies;
- summary-only, hash-only, or tombstone-only disposition is forbidden;
- delete/privacy request cannot erase it before terminal admission/rejection;
- unknown admission status fails closed against deletion and retains exact content.

### B. Admitted causal artifact

After V3 admits the exact artifact:

- artifact identity/hash plus V3 admission/event/receipt provenance remain bound to V3-owned causal history;
- exact recoverability required by causal replay is `EXACT_REQUIRED_CAUSAL_REPLAY`;
- a V2 summary cannot substitute for the admitted utterance/action;
- ordinary transcript cleanup cannot erase the only exact recoverable causal artifact.

V2 does not thereby own causal history. If separately accepted V3/replay/storage authority proves that the same exact artifact is durably recoverable from a canonical causal store/ref, a redundant V2-local physical copy may be removed; exact causal recoverability may not be reduced to summary/hash-only.

### C. Terminally rejected noncausal candidate

Once terminal V3 rejection is verified, the candidate remains permanently `NONCAUSAL`, `IDENTITY_IMMUTABLE`, audit-addressable, cryptographically lineage-preserved, and never admissible under that rejected identity.

Rejection **does not** intrinsically impose permanent exact-byte retention. Its MUST-024 requirement becomes `EXACT_NOT_INTRINSICALLY_REQUIRED` unless a separate exact-content hold applies.

Exact rejected content MAY become `DELETION_ELIGIBLE` only when all are true:

1. terminal rejection is verified by the V3 rejection/admission-court receipt;
2. no pending causal decision remains for that identity;
3. no separate exact-content audit/legal/operational/replay hold applies;
4. immutable rejection provenance is complete and verified;
5. an explicit governed retention/privacy/delete directive authorizes deletion;
6. no unknown/conflicting hold state remains; and
7. rejection tombstone + deletion decision receipt can commit atomically.

After deletion, `V2_REJECTION_AUDIT_TOMBSTONE` survives. The old identity can never later be admitted/reused. A summary/prose reconstruction has no exact-candidate or admission authority, and visible-text similarity cannot resurrect identity. Any rerender/resubmission is a new artifact ID/hash requiring its own admission court.

## 5. Minimum immutable rejection audit record

If exact bytes of a terminally rejected candidate are deleted, preserve at minimum equivalent fields:

- candidate artifact ID;
- original candidate artifact hash + algorithm/version;
- render receipt ID/hash;
- rejection/admission-court receipt ID/hash;
- verified terminal `REJECTED` state and governed reason/status code where supplied;
- interaction/session identity and relevant V2 cursor identity;
- interaction mode;
- render authority ID/version and admission authority ID/version;
- proposal ID/ref where applicable;
- compaction manifest ID/hash where applicable;
- deletion/retention decision receipt ID/hash;
- MUST-024 policy ID/version;
- final content-availability/representation state;
- provenance proving terminal rejection and permanent no-resurrection/no-admission under that identity.

This record is immutable audit lineage, not exact content, causal memory, biography, or an admitted event.

## 6. Cursor, hash, compaction, and summary lineage

V2 logical identity is `{session_id, transcript_cursor, artifact_id}`. V2 transcript cursors are monotonic/order-stable, never renumbered or reused, and preserve deleted positions as tombstoned gaps. Summaries never occupy source cursors. The V3 causal/event cursor is a separate V3-owned namespace; V2 may preserve returned refs but never derive or advance it from transcript position.

Every compacted/deleted artifact preserves session/artifact/class/cursor identity, original exact payload hash + hash algorithm/version, interaction mode, known terminal admission status, source/render/proposal/receipt refs, replay-required V3 refs, policy/version, and decision receipt.

Every `V2_COMPACTION_MANIFEST` binds source cursor ranges, ordered source artifact IDs/hashes, source/result representation, lossless/lossy flag, encoding/version, `MUST-024@1.0.1`, policy basis, exact-content-requirement/hold evaluation, and summary ref if any.

Every summary binds its own ID/hash; source session/cursor ranges; ordered source artifact/hash lineage or immutable manifest ref; summary rule/type/version; summarizer/model and generation receipt where applicable; policy version; `NONCAUSAL_DERIVED_SUMMARY`; and verification state. Claim attribution must survive. `UNVERIFIED_SUMMARY` cannot authorize deletion or exact substitution.

## 7. Privacy / retention / deletion directive law

MUST-024 defines a decision contract, not a universal TTL. Keep separately representable:

- ordinary retention requirement;
- exact-content audit hold;
- causal-replay exact-content requirement;
- privacy/deletion directive;
- legal/operational hold if separately supplied;
- immutable lineage requirement.

A `V2_RETENTION_DECISION_RECEIPT` records target artifact/range, directive source/ref, policy/version, exact-content requirement, known causal status, active holds, unknown/conflicting hold state, decision, resulting representation, tombstone/manifest refs, and integrity result.

Unknown/conflicting hold or causal state fails closed **against deletion** until resolved. No TTL, expiry, “reasonable retention,” or default storage horizon may be invented. Absence of a delete directive means no destructive authority was supplied; it does **not** mean terminally rejected bytes are intrinsically forever undeletable.

Destructive-disposition precedence:

`integrity/unresolved causal status > pending exact requirement > admitted causal-replay requirement > separate exact-content hold > explicit retain/hold > explicit delete directive + complete eligibility > otherwise retain current representation`.

## 8. Immutable audit subset and session close

The immutable audit subset includes session/artifact/cursor identity; original hashes; manifests/tombstones; summary provenance; interaction/admission status; required render/proposal/receipt IDs/hashes; available V3 event/checkpoint/cursor refs; retention/deletion receipts; session-close receipt; and integrity-failure records.

**Exact recoverability is immutable only while an exact-content requirement/hold requires it. Immutable identity/hash/provenance survive after lawfully eligible exact bytes are deleted.**

Formal close emits `V2_SESSION_CLOSE_RECEIPT` with session ID, final V2 cursor, lineage digest, interaction mode, outstanding pending proposals, authority/version, and close-integrity state. It freezes the cursor namespace, preserves pending exact requirements, and creates no V3 memory/relationship/biography or causal-cursor movement. Disconnect/restart/browser unload is not formal close without a receipt.

## 9. Fail-closed behavior

- unknown artifact/policy: retain current representation; invent no deletion authority;
- unknown admission/rejection status: retain exact, block deletion;
- unknown/conflicting hold: block deletion;
- missing transcript: surface missing/unknown; never infer forgetting;
- exact content unavailable where required: no summary substitution or causal/replay use;
- cursor gap without tombstone, cursor reuse/renumber, hash mismatch, broken lineage, admission-hash mismatch: `INTEGRITY_FAILED`;
- missing admission/rejection receipt: terminal status not established where needed for deletion;
- pending delete request: `DELETE_BLOCKED_PENDING_ADMISSION_EXACT_REQUIRED`;
- admitted cleanup that destroys exact causal recoverability: `DELETE_BLOCKED_CAUSAL_REPLAY_EXACT_REQUIRED`;
- tombstoned rejected identity submitted for admission: `REJECT_REJECTED_IDENTITY_RESURRECTION`;
- summary reconstruction submitted as exact rejected candidate: `NO_EXACT_OR_ADMISSION_AUTHORITY`.

## 10. V3-memory separation and consumers

```text
V2: transcript/session persistence; summaries/compaction/tombstones; session continuity; audit + retention/delete receipts
V3: admitted/generated causal events; memory/forgetting/recall/accessibility; governed belief/relationship/biography truth; causal cursors
```

V2 may preserve V3 refs/receipts. No V2 retention state creates, updates, deletes, infers, or proves V3 memory/accessibility.

Exact semantic consumers remain `V2-P4`, `V2-P6`, and `V2-P10`. V2-P9/V3 may reference exact retained candidates only under its own accepted admission/packaging authority.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`: MUST-024 now fully distinguishes causal exact-content retention requirements, noncausal retention/deletion, immutable audit lineage, summary/compaction, explicit privacy/deletion decisions, and V3-memory nonownership. Other RA-R00 blockers for those consumers remain binding.

## 11. Hostile fixtures

| ID | Attack | Required outcome |
|---|---|---|
| H024-01 | pending candidate + delete request | block deletion; exact candidate remains recoverable |
| H024-02 | admitted candidate + ordinary cleanup | cannot destroy exact causal recoverability |
| H024-03 | terminal rejected + verified rejection + no stronger hold + lawful delete directive | exact bytes may delete; immutable rejection tombstone survives |
| H024-04 | deleted rejected identity resubmitted | reject resurrection |
| H024-05 | deleted rejected candidate reconstructed from summary | no exact/candidate/admission authority |
| H024-06 | unknown rejection/admission status + delete request | fail closed; retain exact |
| H024-07 | transcript deletion → V3 forgetting | reject |
| H024-08 | transcript retention → V3 memory | reject |
| H024-09 | summary → relationship truth | reject |
| H024-10 | summary → generated/objective fact | reject |
| H024-11 | lossless compaction renumbers cursor | `INTEGRITY_FAILED` |
| H024-12 | summary takes source ID/cursor | reject identity substitution |
| H024-13 | hash mismatch or unverified summary authorizes delete | no delete; fail closed |
| H024-14 | missing terminal receipt used to delete candidate | retain exact until status verified |
| H024-15 | rerender inherits prior admission/rejection identity | new ID/hash; new admission court |
| H024-16 | session close/EnergeticField creates biography or relationship truth | reject V2→V3 semantic promotion |
| H024-17 | deleted cursor silently shifted/reused | `INTEGRITY_FAILED`; preserve gap |
| H024-18 | unknown class deleted by generic TTL | fail closed retain |
| H024-19 | rejected bytes treated as intrinsically undeletable despite lawful directive/no hold | reject immutability→forever-storage collapse |
| H024-20 | rejected-byte deletion erases rejection identity/hash/receipt | reject; immutable rejection record required |
| H024-21 | V2 cursor advances V3 cursor | reject namespace collapse |
| H024-22 | absent directive causes invented TTL | retain current representation; no heuristic TTL |
| H024-23 | legal/operational hold status unknown + delete request | block deletion until resolved |
| H024-24 | admitted V2-local duplicate removed after verified canonical V3 exact store/ref exists | allowed only if exact causal recoverability remains proven |

## 12. Final verdict

No production code is modified. No V2 application is implemented. No V3 causal-memory/admission semantics are created. Whole-machine architecture remains closed.

`CONSUMER_RELEASE_SUFFICIENCY = SUFFICIENT`

`ADP_024_V2_TRANSCRIPT_POLICY_AUTHORITY = PASS`
