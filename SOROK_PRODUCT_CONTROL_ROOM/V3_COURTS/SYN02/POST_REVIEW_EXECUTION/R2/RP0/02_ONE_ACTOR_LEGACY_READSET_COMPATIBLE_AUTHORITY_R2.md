# RP0-R2 / 02 — one actor with a frozen legacy readset and a separate versioned authority

**Status:** `ONE_ACTOR_DESIGN__FROZEN_LEGACY_CANDIDATE_DOMAIN__SEPARATE_C9_ACTOR_AUTHORITY__C12_SIDECAR_MIRROR__C12_FORK_REPAIR_REQUIRED__OWNER_FREEZE_HELD__NO_NATIVE_GRANT`.

**Decision:** select **Option A — frozen legacy S36 candidate publication domain plus a separately versioned C9 actor authority, plus a C12 actor-mirror sidecar**. This is one authoritative actor state, not a second psyche. The old CandidateStore remains a legacy receipt/occurrence publication archive. The new C9 actor authority is the sole mutable actor-state head/version/receipt/outbox writer. C12 remains the world/episode/perception/checkpoint store and gets a read-only C9 projection through a sidecar owned by C12, not a second Rule T writer.

This selection is a contract proposal for the competent C9/C12 storage owners. It is not a storage-owner freeze, an implementation, or a native C12 claim.

## 1. Why the legacy domain must be frozen

The actual `CandidateStore._logical_readset()` is not a scoped actor readset. It includes all sqlite_master rows, the database metadata and every table row (`transaction.py:115–126`). `commit()` requires exact schema equality and treats any changed prior row as `PUBLICATION_NONADDITIVE_CHANGE` (`:362–370`). The probe proved the physical consequence:

- Actual legacy targetless commit: 7 tables, receipt `1cec8633...`, before `9c5137...`, after `07d380...`.
- Adding a mutable actor table in a copied legacy DB changes the readset domain; a future legacy receipt before-hash becomes `9cfbe2...`, while the old receipt/response rows remain byte-identical.

Therefore a head/outbox UPDATE in the same legacy DB is physically incompatible with the old all-table additive invariant. A partial edit of `_logical_readset()` would change historical publication meaning and the old test receipt domain. That is rejected.

## 2. Physical topology

| Store | Path/owner | Authority | Mutability |
|---|---|---|---|
| `c9_legacy_candidate.sqlite` | Current S36 CandidateStore path; frozen legacy C9 candidate archive | Candidate occurrence/response/target/receipt publication only | Old S36 append-only behavior; no actor head/outbox; no new actor target rows in the targetless test DB |
| `c9_actor.sqlite` | New file; C9 storage owner | **Sole canonical actor state/head/version/decision/outbox** | One C9 actor writer; append-only versions/receipts/attempts/world receipts/bridge; mutable actor_head watermark/outbox ACK only |
| `c12.sqlite` | Actual `r26e.c12_integrity.QualifiedC12Store` / C12 owner | World/episode/perception/checkpoint authority | Existing C12 rules; no actor Rule T authority |
| `c12_actor_mirror.sqlite` | New C12 sidecar; C12 owner | Read-only actor projection/watermark | Append-only projections; monotone watermark; no actor head |

No cross-database ACID is claimed. `c9_legacy_candidate.sqlite` and `c9_actor.sqlite` are separate physical SQLite files; C12 and its mirror are separate again. The bridge uses immutable receipt identities, authoritative C9 actor transactions, and a C12 outbox/replay. A successful old S36 candidate commit does **not** prove actor state; an actor authority commit does not retroactively make the old candidate a person.

The old S37 targetless product remains a legacy test-only path on its existing DB/C12 geometry. It is not changed into the new actor reader. The old `S37` reader remains a targetless negative, not a positive Rule T.

## 3. Actor, branch and target scope

`c9_actor.sqlite` binds:

```text
actor_id + branch_id + branch_epoch
```

- `(actor_id,branch_id)` is the actor branch row; `(actor_id,branch_epoch)` is unique.
- A branch has `parent_branch_id`, `fork_base_version_hash`, `fork_source_cut_hash`, `fork_c12_branch_id/root/watermark` and `source_grant_hash`.
- A fork creates a **new branch epoch** and an inherited version-0/fork-base state; it never mutates the ancestor head.
- `actor_target` is keyed by `(actor_id,branch_id,branch_epoch,target_id)`, so two actors with the same local target ID have distinct records. The legacy global `target_state` is not used for new actor targets.
- `event_key` is stable and actor-scoped (`actor_id` + source event identity); `event_attempt` is branch/epoch-scoped, so sibling branches can process the same world event independently.
- `world_receipt` is a sealed copy/reference of the C8-independent world occurrence (owner, source cut, root/head, effective clock); C9 consumes it, never owns it.
- `legacy_bridge` pins the old CandidateStore receipt hash, event/response, targetless branch/reason, before/after hashes and the frozen domain hash. It is append-only evidence, not mutable actor state.

Probe evidence: two actors wrote the same local `target-same` identifier; the scoped target table held two records and each actor's read returned only its own. The old global `target_state` remained absent for targetless S36.

## 4. Legacy bridge and no false nochange

The bridge sequence is:

```text
old S36 CandidateStore commit (legacy, unchanged)
   -> verify exact old receipt/response rows and frozen domain
   -> insert/verify legacy_bridge row
   -> C9 actor authority BEGIN IMMEDIATE
      -> CAS expected actor head/version/epoch/last_receipt_seq
      -> idempotency/attempt check
      -> Rule A/T evaluation or typed HOLD
      -> final actor version OR no version for HOLD
      -> immutable decision_receipt + event_attempt
      -> projection_outbox PENDING
      -> update actor_head with CAS
   -> COMMIT c9_actor
   -> C12 mirror outbox (later, separate transaction)
```

The actual targetless S36 receipt is `NO_CHANGE/NO_PROPOSAL` (`target_rules.py:311–313`); it is **not** `TRUE_NO_CHANGE_EVALUATED`. The bridge probe produced:

```text
S36 receipt 1cec8633... remains targetless/no target
actor authority decision = HELD_MISSING_RULE
actor version count = genesis only
outbox = PENDING
no actor_target row
no TRUE_NO_CHANGE_EVALUATED
```

This is the required chain: a source/world event can occur while the actor is held; old targetless “no proposal” cannot manufacture a formed psyche or a true nochange. `TRUE_NO_CHANGE_EVALUATED` requires an actual issued/evaluated Rule T, exact readset, and unchanged **semantic** hash; it may advance an administrative actor version but not the semantic payload.

The bridge is idempotent by `legacy_receipt_hash` plus request/attempt identity. A legacy DB table domain is never altered. If the legacy candidate commit succeeds but actor authority fails, the actor remains old; retry reads the same legacy receipt. If actor authority commits but C12 projection fails, actor head/receipt/outbox are authoritative and C12 is `SYNC_HELD` until replay. No Rule T is re-executed after a committed actor receipt.

## 5. Targetless S37 preservation and new reader

- The old `S37` path remains on `c9_legacy_candidate.sqlite` and its existing C12 geometry, with its zero-target guard (`reader.py:156–165`) and `NO_PROPOSAL` requirement (`producer.py:249–253`). Its old tests remain legacy-scoped.
- The new `ActorAwareProduct`/`ActorE2Reader` opens `c9_actor.sqlite` and reads the exact actor head/version/target/semantic payload. It does not use the old S37 targetless reader as a positive.
- The first future consumer is a **same-person C9 E2 semantic read** of a CAN011 PRACTICE/MEDIATOR/TENSION value stored in the actor version, under equal E2 world/coactor/tool conditions. Severing that exact semantic field must remove/hold the claimed difference; a state hash or prose summary is insufficient.
- The legacy C9 `response`/`receipt` tables are source/event evidence, not actor state. The new actor version is the only canonical state.

## 6. C12 mirror and fork

Actual C12 has no actor mirror. `QualifiedC12Store` only adds row-based `verify`; `C12Store` has `branch`, episode, world_event, perception, checkpoint and no actor head/version. The C12 sidecar therefore records:

- `mirror_branch`: C12 branch id, parent, root hash, fork/created clock, actor branch epoch, C9 base sequence, base C12 branch/root, base perception count, state.
- `mirror_receipt`: one C9 receipt/version/projection per `(C12 branch,C9 seq)`.
- `mirror_watermark`: contiguous C9 sequence and projection hash; `CLEAN` only when matching.
- `mirror_fault`: typed gap/conflict/fork-hold evidence.

C12 remains append-only for its four historical tables; `branch` is mutable by the actual class. The sidecar records the branch root because actual `QualifiedC12Store.verify` does not check `branch.root_hash`; the probe showed `verify` still `ok` after direct branch root mutation while the sidecar returned `C12_ROOT_MISMATCH`.

**C12 fork blocker:** actual `_last_clock` excludes `perception`, and `C12Store.fork` computes `fork_clock` from episode/world_event/checkpoint. A clock-11 perception after a clock-10 checkpoint is not copied by a fork; probe observed parent=2, `alt_bad`=1, both actual `verify` calls `ok`. The C12 sidecar records `base_c12_perception_count` and returns `C12_FORK_PERCEPTION_LOSS:alt_bad`. C12 owner must either:

1. repair `_last_clock`/`fork` to use a complete fork cut and include perception identity in the fork root/count (preferred), plus make fork transactional; or
2. provide a proven owner guard that refuses fork when `max(perception.clock) > last_clock` and forces a qualified checkpoint/cut.

Until one is frozen, actor-aware C12 fork is `FORK_HELD`, never `CLEAN`.

## 7. Alternative comparison

| Option | What it would require | Verdict |
|---|---|---|
| **A — frozen legacy + separate actor authority + C12 sidecar** | New actor DB/schema/adapter; old DB unchanged; sidecar; no cross-DB ACID; C12 fork fix/guard | **SELECTED candidate**. Preserves exact old readset/receipt identity and old targetless reader; one actor authority. |
| **B — add actor tables to old C9 and version/migrate the readset** | Patch `CandidateStore._logical_readset/commit`, old receipt hash domain, old tests/reader and target scoping; possible single C9 physical file | `REVISE_PRECISE`; not selected without owner authority. Probe shows added tables change future legacy before-hash and mutable head/outbox are non-additive. |
| **C — wholly new actor journal with old C9/C12 as consumers** | Migration and two competing psyche/journal authorities; no proven infeasibility of A | `DO_NOT_BUILD` absent a specific failure of A and competent owner decision. |

Option B is not rejected as impossible; it is rejected as the default because it silently changes the accepted legacy publication domain and old receipt/test identity, and no owner froze that migration. Option C duplicates authority and is not needed for the actual separate C12 geometry.

## 8. Source-specific implementation contract

New files only (future isolated implementation; not created here except probes):

| Contract | Purpose | First actual consumer |
|---|---|---|
| `C9ActorAuthorityStore` / `c9_actor.sqlite` | head/version/decision/attempt/outbox/CAS | `C9ActorPublisher` |
| `C9LegacyBridge` | read frozen S36 receipt/response/targetless | actor decision |
| `C9ActorPublisher` | verify C8/legacy, evaluate or hold, one actor transaction | C12 mirror outbox |
| `C12ActorMirrorStore` | sidecar projection/watermark | C12 cold/fork |
| `C12ForkGuard` | check C12 branch root/perception cut; patch/hold | C12 open/fork |
| `ActorAwareReader` | actor head/version/target/semantic read | future C9 E2 |
| `ActorAwareProduct` | C12/C9 product with no native claim | A0–A5 held |

The existing S36/S37/C12 modules are not edited. The C12 fork repair is a separate C12-owner patch or guard. The new actor authority is not a `PersonState` or a second psyche; it extends the C9 responsibility with a versioned receipt/state domain while the legacy candidate DB stays a publication archive.

## 9. Non-negotiable owner freeze questions

1. **C9 owner:** approve the frozen legacy path and separate actor DB, exact paths, exclusive writer, WAL/FULL, actor branch/epoch/target scope, legacy bridge, schema hash and old receipt preservation.
2. **C12 owner:** approve exact C12 source cut and sidecar; repair/guard fork perception loss; approve sidecar branch/root/watermark and cold/fork semantics. No C12 source edit by this author.
3. **C8 owner:** provide actual independent B/world receipt, effective clock, C1 ambiguous-persistence recovery and no-repeat guarantee; BP3 process gate is TEST_ONLY.
4. **CAN008/CAN011 owner:** issue a scoped Rule A and Rule T with exact readset/operands; confirm only MEDIATOR/TENSION/PRACTICE and valid-empty. No test-only rule may be promoted.
5. **ADP/SCI05 owner:** approve actor-safe memory and implicit-half2 quarantine; optional dependency pointers are not proof.
6. **Product/world owner:** select the irreversible partial-batch policy before executing 3–5 events; `POLICY_UNDECIDED` remains a stop.
7. **Independent reviewer:** inspect this design, probe outputs and exact source hashes; no self-freeze.

## 10. Verdict

**ENGINEERING:** `REVISE_PRECISE` — Option A is the compatible one-actor design, and the actor CAS/outbox probes pass, but C12 fork perception loss and owner freeze remain; F1.1 not build-ready.
**SCIENCE:** `HOLD` — no Rule A/T, memory, learning, or no-change law is issued.
**AUTHORITY:** `NO_NATIVE` — no C8/C9/C11/C12/Pyat/CAN/ADP/SCI05 grant or actor freeze.

No source, production, persistent DB, or original registry was edited.
