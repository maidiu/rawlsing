# RP0/03 — Proposed executable-grade SQL and C0–C7 fault recovery

**Status: SPEC/NO EXECUTION.** All SQL below is NEW proposed migration DDL, **not** SQL present in S36 or S37. It is an owner-approval candidate for a single SQLite C9 actor authority plus separate C8 world and C12 projection. Existing C9 CandidateStore tables (occurrence, event_identity, response, target_state, target_journal, receipt, clock) MUST be preserved with their exact full-record hashes and semantics. S36 source at e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9, transaction.py blob 1a9c15b88f0dfc130e895f33ac536487f601aadd lines 73–89/128–158/278–423; C12 original QualifiedC12Store DDL not directly retrieved, therefore the proposed C12 schema MUST be adapted only after independent source inspection and owner acceptance. SQLite version/JSON1, journal/synchronous/foreign key settings and actual shared-storage boundaries need live verification; do not call proposed constraints tested.

## 1. C9 additive DDL proposal, revision 1

Use canonical JSON encoding with explicit schema, stable key order and length/digest domain separators. Hash/signature and authority verification occur in reviewed application code over exact bytes, NOT through SQL CHECK alone. Hash columns are named opaque SHA-256 hex strings in this candidate; no claim their content is cryptographically verified by SQLite. All timestamps with '_us' are source-owned integer microseconds, nullable where no effective source. Database admin write time separate from real-world time.

~~~sql
PRAGMA foreign_keys = ON;
-- EXPLICIT OWNER DECISION: WAL + synchronous=FULL or more restrictive;
-- verify actual deployment durability, filesystem and single-writer custody.
-- MIGRATION inside BEGIN IMMEDIATE; preserve old tables verbatim.

CREATE TABLE actor_branch (
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 branch_epoch TEXT NOT NULL,
 parent_branch_id TEXT,
 fork_actor_version_hash TEXT,
 fork_world_receipt_hash TEXT,
 fork_c12_watermark INTEGER,
 source_grant_hash TEXT NOT NULL,
 created_admin_us INTEGER NOT NULL,
 PRIMARY KEY(actor_id, branch_id),
 UNIQUE(actor_id, branch_epoch)
);
CREATE TABLE actor_version (
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 branch_epoch TEXT NOT NULL,
 version_no INTEGER NOT NULL CHECK(version_no>=0),
 version_hash TEXT NOT NULL,
 parent_version_hash TEXT,
 semantic_hash TEXT NOT NULL,
 canonical_state_json TEXT NOT NULL,
 state_grade TEXT NOT NULL CHECK(state_grade IN ('VALID_EMPTY','VERSIONED_PRESENT','MIGRATION_HELD')),
 source_cut_hash TEXT NOT NULL,
 event_effective_us INTEGER,
 decision_receipt_hash TEXT,
 PRIMARY KEY(actor_id,branch_id,version_no),
 UNIQUE(actor_id,branch_id,version_hash),
 FOREIGN KEY(actor_id,branch_id) REFERENCES actor_branch(actor_id,branch_id),
 CHECK((version_no=0 AND parent_version_hash IS NULL)
   OR (version_no>0 AND parent_version_hash IS NOT NULL))
);
CREATE TABLE actor_head (
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 branch_epoch TEXT NOT NULL,
 head_version_no INTEGER NOT NULL,
 head_version_hash TEXT NOT NULL,
 last_finalized_seq INTEGER NOT NULL DEFAULT 0 CHECK(last_finalized_seq>=0),
 PRIMARY KEY(actor_id,branch_id),
 FOREIGN KEY(actor_id,branch_id,head_version_no)
   REFERENCES actor_version(actor_id,branch_id,version_no)
);
CREATE TABLE decision_receipt_v1 (
 receipt_hash TEXT PRIMARY KEY,
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 branch_epoch TEXT NOT NULL,
 c9_commit_seq INTEGER NOT NULL,
 decision_kind TEXT NOT NULL CHECK(decision_kind IN
  ('COMMITTED_CHANGE','TRUE_NO_CHANGE_EVALUATED','HELD_MISSING_RULE',
   'HELD_MISSING_SOURCE','SOURCE_DENIED','DEFERRED',
   'NOT_APPLICABLE_BY_ISSUED_RULE','INTEGRITY_FAILED')),
 world_receipt_hash TEXT,
 world_event_id TEXT,
 access_receipt_hash TEXT,
 before_version_hash TEXT NOT NULL,
 result_version_hash TEXT,
 before_semantic_hash TEXT NOT NULL,
 after_semantic_hash TEXT,
 source_cut_hash TEXT NOT NULL,
 rule_a_hash TEXT,
 rule_a_status TEXT NOT NULL,
 rule_t_hash TEXT,
 rule_t_status TEXT NOT NULL,
 evaluated_readset_hash TEXT NOT NULL,
 permission_hash TEXT,
 exact_reason TEXT NOT NULL,
 canonical_receipt_json TEXT NOT NULL,
 effective_us INTEGER,
 admin_committed_us INTEGER NOT NULL,
 UNIQUE(actor_id,branch_id,branch_epoch,c9_commit_seq),
 FOREIGN KEY(actor_id,branch_id) REFERENCES actor_branch(actor_id,branch_id),
 CHECK((decision_kind IN ('COMMITTED_CHANGE','TRUE_NO_CHANGE_EVALUATED')
           AND result_version_hash IS NOT NULL AND rule_t_hash IS NOT NULL)
       OR (decision_kind NOT IN ('COMMITTED_CHANGE','TRUE_NO_CHANGE_EVALUATED')
           AND result_version_hash IS NULL))
);
CREATE TABLE processed_event_v1 (
 idempotency_key TEXT PRIMARY KEY,
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 branch_epoch TEXT NOT NULL,
 world_event_id TEXT,
 world_receipt_hash TEXT,
 expected_parent_version_hash TEXT NOT NULL,
 source_cut_hash TEXT NOT NULL,
 request_digest TEXT NOT NULL,
 receipt_hash TEXT NOT NULL UNIQUE,
 attempt_grade TEXT NOT NULL,
 FOREIGN KEY(receipt_hash) REFERENCES decision_receipt_v1(receipt_hash)
);
CREATE UNIQUE INDEX ux_processed_world_event_final
 ON processed_event_v1(actor_id,branch_id,branch_epoch,world_receipt_hash)
 WHERE world_receipt_hash IS NOT NULL AND attempt_grade='FINALIZED';
CREATE TABLE projection_outbox_v1 (
 receipt_hash TEXT PRIMARY KEY,
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 branch_epoch TEXT NOT NULL,
 c9_commit_seq INTEGER NOT NULL,
 actor_result_hash TEXT,
 world_receipt_hash TEXT,
 payload_digest TEXT NOT NULL,
 envelope_json TEXT NOT NULL,
 projection_state TEXT NOT NULL CHECK(projection_state IN ('PENDING','PROJECTED','ACKED')),
 projected_c12_hash TEXT,
 acked_admin_us INTEGER,
 attempt_count INTEGER NOT NULL DEFAULT 0 CHECK(attempt_count>=0),
 last_error_code TEXT,
 FOREIGN KEY(receipt_hash) REFERENCES decision_receipt_v1(receipt_hash),
 UNIQUE(actor_id,branch_id,branch_epoch,c9_commit_seq),
 CHECK(projection_state!='ACKED' OR (projected_c12_hash IS NOT NULL AND acked_admin_us IS NOT NULL))
);
CREATE TABLE reconciliation_fault_v1 (
 fault_id TEXT PRIMARY KEY,
 actor_id TEXT NOT NULL,
 branch_id TEXT NOT NULL,
 world_receipt_hash TEXT,
 actor_receipt_hash TEXT,
 cut_code TEXT NOT NULL,
 source_snapshot_hash TEXT,
 observed_digest TEXT,
 status TEXT NOT NULL CHECK(status IN ('OPEN','RECONCILED','INTEGRITY_HELD')),
 evidence_json TEXT NOT NULL
);
CREATE TABLE migration_receipt_v1 (
 old_archive_blob_hash TEXT NOT NULL,
 old_field_path TEXT NOT NULL,
 mapping_kind TEXT NOT NULL CHECK(mapping_kind IN
  ('SOURCE_VERIFIED','CARRIER_ONLY','DERIVED_VIEW_ONLY','UNSAFE_HISTORICAL','UNKNOWN','SOURCE_HELD')),
 owner_decision_hash TEXT,
 new_actor_ref TEXT,
 reason TEXT NOT NULL,
 PRIMARY KEY(old_archive_blob_hash,old_field_path)
);
~~~

Required application invariants beyond SQL: every finalized decision must reference a persisted matching actor_version with exact version/parent hash and state bytes; every version after genesis references one decision receipt (back reference cycle resolved by insert order/deferred app verification); every decision has one outbox; head update cannot occur without them. Commit sequence allocated under BEGIN IMMEDIATE for each branch, including held receipts, using max committed decision sequence + 1 rather than last_finalized_seq alone. An opaque source-safe world-only held receipt may have no world_event_id when source never qualified. New kind not registered CAN011: only V3MS_MEDIATOR/TENSION/PRACTICE allowed inside canonical state, verified in application with exact formation rule or valid-empty. Held receipts record before_semantic_hash and require no after semantic mutation; evaluated nochange requires identical before/after semantic hash, actual rule and readset, an administrative new actor revision; positive change requires different semantics and original rule. Source-cut hash and issuer qualification NEVER optional when positive.

Migration: FIRST freeze schema + inspect current SQLite PRAGMAs, C9 reader and QualifiedC12Store real definitions. Copy old DB immutably/checksum; record migration journal and schema version, refuse nonempty duplicate genesis or an existing actor head under different archive hash; wrap C9 additions/seed in one transaction, rollback and restore snapshot on any invalidity. Do not mutate old tables, delete old receipts, change old row hashes or reclassify test-only rows as native. Old V3 type/age/50 parent, M26 derived metabolic_style/registers and M19 narrator content quarantined as UNSAFE_HISTORICAL or DERIVED_VIEW_ONLY. Verified objective class/material facts may migrate *only* via separate source-qualified owner decision. Re-run same migration identity idempotently; changed old SHA held for fresh authorization. Reversal leaves original schema/table rows and archive usable, but never erases C8 real world facts.

## 2. Proposed C12 mirror DDL — adapter, NOT verified existing class schema

**Important:** No directly inspected QualifiedC12Store body at examined branch. Do NOT execute these CREATE statements into its database before owner verifies current schema, table naming, branch/fork/episode writers and opens. Either place in a reviewed sidecar DB bound to existing store or additive owner-approved tables under same C12 transaction as its checkpoint.

~~~sql
CREATE TABLE c9_actor_mirror_v1 (
 actor_id TEXT NOT NULL, branch_id TEXT NOT NULL, branch_epoch TEXT NOT NULL,
 c9_commit_seq INTEGER NOT NULL, c9_receipt_hash TEXT NOT NULL,
 actor_version_no INTEGER, actor_version_hash TEXT, semantic_hash TEXT,
 c8_world_receipt_hash TEXT, canonical_projection_json TEXT NOT NULL,
 projection_hash TEXT NOT NULL,
 PRIMARY KEY(actor_id,branch_id,branch_epoch,c9_commit_seq),
 UNIQUE(c9_receipt_hash)
);
CREATE TABLE c9_mirror_watermark_v1 (
 actor_id TEXT NOT NULL, branch_id TEXT NOT NULL, branch_epoch TEXT NOT NULL,
 acknowledged_c9_seq INTEGER NOT NULL CHECK(acknowledged_c9_seq>=0),
 last_c9_receipt_hash TEXT NOT NULL,
 last_projection_hash TEXT NOT NULL,
 PRIMARY KEY(actor_id,branch_id,branch_epoch)
);
~~~

C12 mirror MUST be an append-only projection with monotonic contiguous sequence. Commit rule under its own local transaction: if receipt already present compare exact projection digest; if next seq = watermark+1 and same branch/epoch/parent chain, insert mirror and set watermark; if seq > watermark+1 => GAP_HOLD; if seq <= watermark and digest differs => MIRROR_CONFLICT; if branch epoch mismatches => FORK_HOLD; no automatic rollback/delete. For held world events, projection records operational hold and no psychological payload delta. If C8 world journal is ahead or missing, C12 may render objective qualified reality but marks combined actor product not CLEAN until C8/C9 reconciliation.

## 3. Exact transaction / CAS / idempotency pseudocode

~~~text
commit_actor(input):
 verify_c8_receipt_durable_and_source_qualified(input.world_ref)
 d := hash_canonical(domain="RP0_REQ_V1", actor, branch_epoch, world_receipt,
                     world_parent, expected_actor_version_hash, source_cut,
                     ruleA_hash, ruleT_hash, access_ref, exact_inputs)
 BEGIN IMMEDIATE on exclusive C9 writer
   old := SELECT request_digest, receipt_hash FROM processed_event_v1 WHERE key=k
   IF old exists:
       IF old.digest != d: ROLLBACK -> IDEMPOTENCY_PAYLOAD_CONFLICT
       ELSE: COMMIT read-only -> return exact existing receipt, never run RuleT
   head := SELECT branch_epoch,head_version_no,head_version_hash FROM actor_head
   IF head != expected EXACT tuple: ROLLBACK -> STALE_ACTOR_PARENT
   verify actor_version previous hash; world causal parent/clock; source/as-of;
          authority permissions, issuer roles, rule readset; evidence grade
   decision := qualified original RuleA/RuleT evaluation OR typed explicit HOLD
   seq := SELECT MAX(c9_commit_seq)+1 for actor/branch/epoch
   INSERT immutable decision_receipt_v1
   IF decision qualified finalized:
       INSERT actor_version(v+1, parent=head.hash, payload, receipt)
       UPDATE actor_head ... WHERE head_version_no=v AND head_version_hash=old
       IF rows_changed!=1: ROLLBACK -> CAS_CONFLICT
   INSERT processed_event_v1 (k,d,receipt ...)
   INSERT projection_outbox_v1 (receipt,PENDING,...)
 COMMIT
 return receipt

reconcile(receipt):
 read immutable C9 decision+outbox; validate source snapshot and C8 reference
 IF outbox already ACKED: verify C12 watermark/projection; return
 BEGIN transaction on C12 (separate from C9)
   if identical projection exists: verify hash and watermark
   else require seq==last_watermark+1 and matching epoch; insert+advance
 COMMIT C12; reread exact mirror/seq/hash from C12
 UPDATE C9 projection_outbox to PROJECTED with proven digest, then
 UPDATE to ACKED with proven digest and ack_time (idempotent CAS)
 On fault leave PENDING/PROJECTED; never call RuleT again

cold_or_fork_open(cut):
 compare C8 branch real world hash/effective clock, C9 head+receipts/outbox,
 C12 mirror watermark; drain authorized pending outbox; verify contiguous chain
 if impossible return SYNC_HELD or FORK_HELD_INTEGRITY, no CLEAN/V2/A5
 pin fork C9 actor version/hash, C8 world anchor and C12 exact watermark
 create new branch epoch via qualified owner authorization, no ancestor mutation
~~~

Exactly-once actor publication is achieved by exclusive C9 transaction + unique idempotency and CAS, not by pretending C8 external action or C12 replication is atomic. At-least-once outbox delivery is safe because C12 mirror unique identity/digest comparison. Source mismatch on a never-committed retry must HOLD and may require a new original decision; a committed receipt is replayed *only for projection* against its preserved immutable historical cut. No altered payload under same idempotency identity. Concurrent branches cannot reuse ancestor event identity to overwrite world state; two conflicting updates on same branch return stale conflict, no automatic arithmetic commutation or arrival-order Rule T.

## 4. Crash matrix C0–C7 — required separate injection points

| Cut | At physical boundary and durable remainder | Restart action / future E2 & cold/fork |
|---|---|---|
| **C0** | Candidate qualified but **before real B action**; perhaps only proposal/attempt log. No C8 OCCURRED. | Re-evaluate source clock and batch policy before any action; cannot claim event happened, Rule A/T/nochange. E2 sees only old actor and actual prior world. |
| **C1** | **B performed independently**, C8 journal fsync/anchor not yet confirmed. External act may be irreversible; durable journal may be absent. | Record UNKNOWN_PERSISTENCE in reconciliation evidence; query qualified source/B execution receipt or external idempotency outcome. **Never blindly re-execute B action**. If source proves fact, append once with original effective time/causal parent; if not, HOLD, not NO_EVENT or rollback. E2 must not assume psyche change, world remains uncertain in dependent domain. |
| **C2** | C8 world occurrence durably committed, actor reception/Rule T/C9 not committed. World action/care/interval remains. | Rehydrate from exact C8 event and actor head; if source/rule absent produce world-committed actor-held operational result. Retry actor separately without replaying B. E2 reads old qualified actor and new qualified external world separately; no false inferred internal ability. |
| **C3** | C9 BEGIN IMMEDIATE started, before COMMIT, possible uncommitted actor_version/receipt/outbox writes. | SQLite rollback transaction; C8 event persists, no C9 finalized receipt/version visible. Retry exact world and actor prestate after checking source/currentness and idempotency. No ghost Rule T or stale C12 clean. |
| **C4** | C9 COMMIT durable with new version or HELD receipt + PENDING outbox, **before C12 projection**. | One C9 receipt is authoritative, do not execute Rule T again. Reconciler projects once; until C12 catches up CLEAN forbidden. E2 direct C9 read may use committed semantic payload, while C12/open/fork requires watermark. |
| **C5** | C12 mirror transaction committed, C9 ACK not yet committed (PENDING/PROJECTED). | Re-read matching C12 projection hash, idempotently mark PROJECTED/ACKED in C9. Never create second version or mirror. Full user-facing CLEAN only after validated C8/C9/C12 cut. |
| **C6** | Cold/fork during source DB open, mid-outbox scan, during branch root/checkpoint or at intermediate watermark. | Verify complete C8 world anchor, C9 version and receipt chain, C12 contiguous watermark; drain recoverable outbox, else SYNC_HELD/FORK_HELD_INTEGRITY. Fork only from exact immutable triple cut; reject stale mirror and branch epoch conflict. No sourcefree test fixture treated native. |
| **C7** | On retry, a C8/source/RuleA/RuleT/permission hash, grade or effective clock differs from stored request snapshot. | Same idempotency key + different payload -> IDEMPOTENCY_PAYLOAD_CONFLICT. Already committed receipt stays immutable for mirror replay (no reevaluation), new causal attempt requires fresh owner/source authorization. Uncommitted case -> SOURCE_CHANGED_REQUALIFY_HELD, never silent takeover or overwrite. |

Additional physical injection substeps to distinguish C1 ambiguous I/O: during world append before durable rename/fsync; after world commit before actor ingress; before C9 insert; after C9 receipt insert but before COMMIT; immediately after C9 COMMIT; before/after C12 mirror COMMIT; after mirror readback before each C9 ACK state; during fork ancestor pin; changed source replay. A process kill, I/O error or timeout is not evidence that no B act happened.

**All-at-every-cut assertions:** at most one actor version and one terminal decision receipt per exact qualified event/epoch; world receipt preserved if action truly occurred; no ghost suffix; no repeated Rule T after C9 COMMIT; actor semantic state equals C9; C12 fails closed unless mirror matches C9; no C8 writer bypass accepted as native; subsequent E2 reads previously committed semantics or explicit HOLD, never sidecar prose. These are demanded falsifiers, **NOT_RUN**.

## 5. Full-life and material-world counterexamples

Beyond a toy E1->E2, exercise age-spanning care and dependency, independently acting B and another carer, school-to-work transitions, actual housework/paid work and shortages, ordinary rest and nonencounters, source-refused opportunities, actor's mistaken later testimony, sustained stable adulthood, context-gated practice when a tool disappears, external help wrongly attributed as skill, N 3–5 proposal batches with real intervals and off-plan world act, later marriage/care and civic/institutional meaning, qualified NO_CHANGE, source loss and recovered cold/fork. Real C11/Pyat and original human-science causality are separately held until issued. An unissued learning rule must remain HELD even if the full-life fixture is aesthetically compelling.

## 6. Storage threat model and explicit blocking facts

D1 trusted C8 exclusive write/security anchor from BP3/C8O is not proved native; source-owner event receipts may be unavailable. QualifiedC12Store definition/DDL was not directly accessed at the inspected branch. SQL provided here is a candidate, not run, schema-validated or safe against every trigger/foreign-key migration failure. Single C9 writer requires process and file lock discipline not yet measured. SQLite transaction durability setting on actual FS unverified. Cross-DB rollback cannot undo external action. If independent owner cannot verify these, stop F1.1 as RED and design proven topology, not inferred ACID. No raw survey/paid inference/native code executed by RP0.
