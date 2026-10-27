# RP0-R2 / 03 — versioned SQL, CAS, outbox, mirror and C0–C7 recovery contract

**Status:** `PROPOSED_SOURCEFREE_CONTRACT__C9_ACTOR_SINGLE_WRITER__LEGACY_DOMAIN_FROZEN__C12_SIDECAR__C12_FORK_GUARD_OR_PATCH_REQUIRED__NOT_OWNER_FROZEN__NO_NATIVE_GRANT`.

**Normative DDL/probe files:** `probes/schema_actor.sql`, `probes/schema_mirror.sql`, and the four probe scripts in this folder. The SQL is TEST_ONLY sourcefree DDL, not a real C9/C12 migration. It is the candidate for a competent storage-owner freeze; it hasn't been applied to a live DB.

## 1. Topology and non-negotiable boundaries

```text
legacy S36 CandidateStore DB  = frozen candidate publication archive
                                 (occurrence/response/target/receipt; old readset)
c9_actor.sqlite               = single canonical actor authority
                                 (branch/head/version/decision/attempt/outbox)
c12.sqlite                    = actual QualifiedC12Store world/episode/perception/checkpoint
c12_actor_mirror.sqlite       = C12-owned read-only actor projection/watermark
```

- The legacy DB is **not** the actor authority. It is never given actor_head/outbox/version tables.
- `c9_actor.sqlite` is the sole mutable actor state writer. It is not a second psyche; it is the versioned C9 state/receipt domain.
- C12 remains the world/history store and never performs Rule T.
- The sidecar is append-only projection, not a second actor authority.
- No cross-database ACID is claimed. Legacy->actor and actor->C12 are explicitly separate transactions with typed recovery.
- The actual legacy S36 public APIs (`admit_occurrence`, `commit`, old targetless path) remain unchanged; the actual S37 targetless tests remain legacy-scoped.
- No C8 world action is rolled back by any C9/C12 failure.

## 2. C9 actor authority DDL

The complete executable candidate is `probes/schema_actor.sql`. It creates:

| Table | Purpose | Mutability |
|---|---|---|
| `actor_meta` | schema/namespace/legacy domain | seed only |
| `actor_branch` | actor, branch, branch epoch, parent, fork cut, C12 branch | append only |
| `actor_version` | version 0/fork/change/nochange canonical actor payload | append only |
| `actor_head` | current version/hash, `last_receipt_seq`, `last_finalized_seq` | CAS update only |
| `actor_target` | target scoped by actor+branch+epoch | append only |
| `world_receipt` | sealed external C8 world occurrence reference | append only |
| `legacy_bridge` | frozen S36 receipt/response/domain identity | append only |
| `decision_receipt` | orthogonal statuses, Rule A/T, semantic hashes | append only |
| `event_attempt` | stable event, attempt, idempotency, held/final state | append only |
| `projection_outbox` | per-receipt PENDING/PROJECTED/ACKED | transactional state update |
| `reconciliation_fault` | C0–C7 typed fault evidence | append/state |
| `migration_receipt` | old V3 field quarantine/mapping | append only |

Core physical invariants:

```text
actor_version:
  PRIMARY KEY(actor_id,branch_id,version_no)
  UNIQUE(actor_id,branch_id,branch_epoch,version_no)
  UNIQUE(actor_id,branch_id,branch_epoch,version_hash)
  version_kind: GENESIS_VALID_EMPTY | FORK_INHERITED | SEMANTIC_CHANGE
                | ADMINISTRATIVE_NOCHANGE | MIGRATION
  version_hash != semantic_hash in general; a semantic nochange gets a new
  administrative version hash while semantic_hash remains identical

actor_head:
  PRIMARY KEY(actor_id,branch_id)
  FK includes actor_id+branch_id+branch_epoch
  last_finalized_seq <= last_receipt_seq
  trigger blocks epoch change and any monotone regression

event_attempt:
  UNIQUE(actor_id,branch_id,branch_epoch,event_key,attempt_no)
  UNIQUE(idempotency_key)
  partial UNIQUE(actor_id,branch_id,branch_epoch,event_key)
    WHERE attempt_state='FINALIZED'
  a HELD attempt may be followed by a new attempt; a FINALIZED event cannot
  be finalized again on that branch/epoch

decision_receipt:
  FINALIZED kinds require result_version_hash, rule_t_hash and evaluated_readset_hash
  TRUE_NO_CHANGE_EVALUATED requires unchanged semantic hash
  COMMITTED_CHANGE requires changed semantic hash
  HELD kinds have no result version
  SCI05 DENIED/HELD/INTEGRITY_FAILED cannot finalize without an authorized state
```

Append-only triggers exist on actor_version, decision_receipt, event_attempt, world_receipt, legacy_bridge, actor_branch and actor_target. `actor_head` and outbox have monotone/state-transition triggers. SQL constraints are not cryptographic signatures; application verdicts/receipt hashes still require reviewed code and source-owner evidence.

## 3. C9 transaction and CAS

The exact semantic sequence is:

```text
publish(actor_request):
  verify frozen legacy receipt/response/domain if present
  verify external C8 world receipt, source owner/cut/as-of, permission
  BEGIN IMMEDIATE on c9_actor.sqlite
    head = SELECT actor_head WHERE actor_id+branch_id
    if head.epoch/version/hash/last_receipt_seq != expected:
        ROLLBACK -> STALE_ACTOR_PARENT
    if idempotency key exists:
        same request digest -> return exact existing receipt; no Rule T rerun
        changed digest -> ROLLBACK -> IDEMPOTENCY_PAYLOAD_CONFLICT
    if a FINALIZED attempt exists for event_key:
        ROLLBACK -> EVENT_ALREADY_FINALIZED
    seq = head.last_receipt_seq + 1
    evaluate authorized Rule A/T or produce typed HOLD
    insert immutable decision_receipt(seq,...)
    if final:
        insert actor_version(parent=head.version_hash, version_no+1,...)
    insert event_attempt(state=HELD/FINALIZED,...)
    insert projection_outbox(receipt, PENDING)
    UPDATE actor_head
      SET version/hash/semantic (if final), last_receipt_seq=seq,
          last_finalized_seq=seq if final
      WHERE expected epoch/version/hash/last_receipt_seq
    if rowcount != 1: ROLLBACK -> CAS_CONFLICT
  COMMIT
```

The actor version, receipt, attempt and PENDING outbox are one transaction. A HOLD inserts a receipt/attempt/outbox and advances `last_receipt_seq`, but does not advance the actor semantic version. A final true-nochange creates an administrative `ADMINISTRATIVE_NOCHANGE` version with the same semantic hash. A crash before COMMIT rolls back all of them; the independent C8 world fact remains.

The unpublished legacy bridge is separate: a committed legacy receipt cannot be rolled back or rewritten by an actor failure. If legacy succeeds and actor fails, retry uses the same legacy identity; if actor succeeds, C12 projection is outbox work only.

## 4. Target scope, branch and fork

- New actor targets are in `actor_target` keyed by `(actor_id,branch_id,branch_epoch,target_id)`; legacy `target_state.id` is not used for new actor target identity.
- A fork creates a new branch row/epoch with `parent_branch_id`, `fork_base_version_hash`, `fork_source_cut_hash`, `fork_c12_branch_id/root/watermark`; the ancestor is immutable.
- Child version 0 may be `FORK_INHERITED` with a parent hash; genesis valid-empty is the only parentless version 0.
- A target ID can therefore repeat across actors/forks without a shared psyche; the probe wrote the same `target-same` for A and B and read only the scoped row.
- The old `S37` targetless reader keeps its zero-target contract; the new actor reader is separate.

## 5. C12 sidecar and actual C12 constraints

The complete candidate is `probes/schema_mirror.sql`:

```text
mirror_branch(c12_branch_id, actor_id, actor_branch_epoch,
              c12_parent_branch_id, c12_root_hash, c12_fork_clock,
              c12_created_clock, c9_start_seq, c9_start_receipt_hash,
              base_c12_branch_id, base_c12_root_hash,
              base_c12_perception_count, mirror_state, ...)
mirror_receipt(c12_branch_id, c9_seq, c9_receipt_hash, version hash,
               decision kind, semantic, projection hash/json, C12 root/clock,
               C8 receipt, ...)
mirror_watermark(c12_branch_id, last_seq, last_receipt_hash,
                 last_projection_hash, watermark_state, ...)
mirror_fault(...)
```

Invariants:

1. `(c12_branch_id,c9_seq)` unique; `(c12_branch_id,c9_receipt_hash)` unique.
2. Receipts are append-only; sequence starts `c9_start_seq+1`; a gap, duplicate with a different digest, or watermark regression is `SYNC_HELD`/`MIRROR_CONFLICT`.
3. Watermark `CLEAN` only if C12 root/clock and every C9 receipt projection match.
4. Missing mirror branch is never clean.
5. `base_c12_perception_count` records the parent count at the fork cut; if actual C12 child has fewer perceptions than its base, the result is `C12_FORK_PERCEPTION_LOSS`/`FORK_HELD`.
6. C12 branch root is recorded because actual `QualifiedC12Store.verify` does not validate `branch.root_hash`; direct branch-root tamper was accepted by actual verify but rejected by the sidecar.
7. C12's original `branch` table is mutable; sidecar anchor/count checks are mandatory.
8. C12 `fork` must be owner-frozen as transactional. Actual `C12Store.fork` is not transactional by itself; `joined/lineage.py` supplies a SAVEPOINT wrapper, but the store API is directly callable.

### C12 owner repair contract

The probe found a real actual-source failure: a perception at clock 11 after a clock-10 checkpoint is not included in `fork_clock` and is dropped by `C12Store.fork`; actual `verify` still returns `ok`. The C12 owner must implement one of:

```text
Preferred:
  fork_cut = max(last_episode_clock, last_world_clock, last_checkpoint_clock,
                 last_perception_clock)
  copy all rows at the exact cut; include perception identity in root_hash/
  root_counts; fork branch+copy+root+counters in one transaction;
  verify parent/child counts, root and branch ancestry.

Fallback owner guard:
  before fork, if max(perception.clock) > last_clock, return FORK_HELD;
  require a qualified checkpoint/cut before fork. Never claim CLEAN.
```

Until one is frozen, `C12ForkGuard` must refuse/hold; the sidecar must not paper over the missing perception.

## 6. C0–C7 recovery matrix

| Cut | Durable state / exact outcome |
|---|---|
| **C0** proposal only, no B act | no C8 occurrence; no actor version; proposal cannot create event/actor; world remains prior. |
| **C1** B acted, C8 journal/anchor ambiguous | no automatic B replay; `OCCURRENCE_UNKNOWN`/`SOURCE_HELD`; C8 owner obtains external receipt or holds. Never infer NO_EVENT. |
| **C2** C8 committed, C9 not | world fact persists; `WORLD_COMMITTED_ACTOR_HELD`; actor stays prior; retry actor with same world receipt; no re-act. |
| **C3** C9 transaction before COMMIT | SQLite rollback; no actor version/receipt/outbox visible; C8 remains; retry exact prestate. Probe rollback passed. |
| **C4** C9 committed, C12 mirror absent | actor head/version/receipt/outbox authoritative; `SYNC_HELD`, outbox PENDING; mirror replay once; no Rule T rerun; no second actor version. Probe passed. |
| **C5** C12 mirror committed, C9 ACK absent | read back exact mirror projection; update outbox PROJECTED->ACKED idempotently; no new actor version; duplicate mirror identity refused. Probe passed. |
| **C6** cold/fork stale/gap | C12 verify + sidecar root/watermark/branch base; C9 head/receipt chain; stale/gap => `SYNC_HELD`/`FORK_HELD`; actual C12 perception loss => `FORK_HELD`; actual C12 fork must be fixed/guarded. Probe found defect. |
| **C7** source/rule/permission changed on retry | same idempotency key changed payload -> `IDEMPOTENCY_PAYLOAD_CONFLICT`; uncommitted source changed -> `SOURCE_CHANGED_REQUALIFY_HELD`; committed receipt is immutable and may be replayed for mirror only, never re-evaluated. |

C1/C2/C7 live external boundaries are `NOT_RUN`; C3/C4/C5/C6 are sourcefree probes. Passing these probes is not proof of actual B, care, memory, or native C12.

## 7. Idempotent held and requalification

The stable event identity is `event_key` (actor + world event identity). The attempt identity is `(actor_id,branch_id,branch_epoch,event_key,attempt_no,idempotency_key)`. `settled_scope_hash` includes the world receipt/source cut/as-of and Rule A/T/permission identity.

Rules:

- A first evaluation with no Rule T/source produces a HELD receipt and attempt; no actor version.
- The HELD attempt is immutable. A later owner-authorized source/rule creates a **new attempt**, with a new idempotency key, `prior_attempt_id`, and a new settled scope. It may finalize once.
- A final positive/true-nochange cannot be finalized again for the same branch/epoch/event; the partial unique index rejects it. A new source/rule does not silently rewrite the old executed decision; any supersession requires a new branch/epoch or an expressly authorized owner procedure not issued here.
- Same key+same digest returns the existing receipt; same key+different digest rejects. No blind “return prior HELD forever”, and no silent new Rule T on a committed event.

## 8. Orthogonal status and SCI05

The actor decision stores orthogonal axes rather than one event flag:

| Axis | Values (adapter, preserve raw source codes separately) |
|---|---|
| `source_status` | QUALIFIED, SOURCE_HELD, SOURCE_DENIED, INTEGRITY_FAILED, UNKNOWN |
| `world_occurrence` | PROPOSED_ONLY, OCCURRED, NOT_REALIZED, NO_EVENT, NOT_YET_OBSERVED, OCCURRENCE_UNKNOWN |
| `actor_presence` | CO_PRESENT, NOT_PRESENT, UNKNOWN, NOT_APPLICABLE |
| `actor_reception` | RECEIVED, PARTIAL, NOT_WITNESSED, TESTIMONY, UNKNOWN, NOT_APPLICABLE |
| `rule_a_status` | APPLIED_WITH_RESPONSE, APPLIED_VALID_EMPTY, HELD_MISSING_RULE, HELD_SOURCE, NOT_APPLICABLE_BY_ISSUED_RULE, INTEGRITY_FAILED |
| `rule_t_status` | COMMITTED_CHANGE, TRUE_NO_CHANGE_EVALUATED, HELD_MISSING_RULE, HELD_MISSING_SOURCE, DEFERRED, NOT_APPLICABLE_BY_ISSUED_RULE, INTEGRITY_FAILED |
| `actor_state_status` | VALID_EMPTY, VERSIONED_PRESENT, UNAVAILABLE_PENDING_RECONCILIATION, MIGRATION_HELD |
| `memory_evidence` | ACTOR_ACCESSIBLE, PARTIAL_TRACE, BELIEF_WITH_SOURCE, ACTOR_UNKNOWN, ANALYST_ONLY, NOT_APPLICABLE |
| `sci05_status` | ADMITTED, DENIED, HELD, INTEGRITY_FAILED, NOT_APPLICABLE |

`TRUE_NO_CHANGE_EVALUATED` is legal only with a concrete issued/evaluated Rule T, exact readset/hash, and unchanged semantic hash. S36 `NO_PROPOSAL`, a missing rule, source denial, unseen world, no encounter, and valid-empty actor state are different. `TESTIMONY` is a later event/source, with a separate testimony clock, not a substitute scalar.

The DDL enforces the SCI05 fail-closed rule: a decision with `sci05_status` DENIED/HELD/INTEGRITY_FAILED cannot be COMMITTED_CHANGE/TRUE_NO_CHANGE, and no denial certificate is accepted. The application must quarantine all 3–5 half2 proposals on a denied/held same-call self-account absent an independently authorized pre-existing basis; an optional model-authored dependency pointer is never proof.

## 9. Migration and legacy archive

- Copy the old C9/C12 DBs read-only and hash them before any migration.
- Do not add actor tables to the frozen legacy DB.
- `legacy_bridge` preserves the exact old receipt/response/event/targetless identity, old before/after and frozen domain hash; old rows are not deleted or rehashed.
- Old V3 M26 derived writes, M19 narrator feedback, 50/hopeful/type/age/demographic/placeholder data are `UNSAFE_HISTORICAL`/`DERIVED_VIEW_ONLY`; only source-qualified material facts may migrate by owner decision.
- C12 rows are not rewritten by the actor migration; sidecar starts at the owner-approved cut.
- Migration is idempotent by archive hash/domain; changed archive identity is held for fresh authorization.
- A migration rollback restores old schema/rows; it never erases an independent C8 world fact.

## 10. Acceptance gate

F1.1 implementation is **not** permitted by this artifact. Before a separately authorized review:

1. C9/C12 joint owners select Option A and sign exact DB paths, schema hashes, C12 source cut, fork repair/guard, PRAGMAs and writer custody.
2. C8 owner provides actual world receipt/C1 recovery; no BP3 process-local gate is native proof.
3. CAN008/CAN011 owner issues scoped Rule A/T or explicitly holds; no test-only rule may be promoted.
4. ADP/SCI05 and product/world policy owners approve the memory and irreversible-batch gates.
5. Independent reviewer verifies C0–C7, actual C12 fork fix, old S36 preserved, source/status axes and no native grant.
6. Only then can a separate user-selected F1.1 worker implement; actor freeze is not self-issued.

**No implementation. No owner freeze. No science. No native grant.**
