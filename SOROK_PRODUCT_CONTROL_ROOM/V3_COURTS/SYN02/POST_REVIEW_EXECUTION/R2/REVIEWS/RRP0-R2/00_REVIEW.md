# SYN02-RRP0-R2 — independent hostile C9/C12 actor authority and fork-loss court

**Review status:** `RRP0_R2_REVISE_PRECISE__C12_FORK_RED_REPRODUCED__C12_SIDECAR_NOT_FAIL_CLOSED__C9_OPTION_A_ACCEPT_SCOPED_DIRECTION__OWNER_FREEZE_HELD__F1_1_NOT_AUTHORIZED__NO_NATIVE_GRANT`.

**Reviewer:** fresh independent RRP0-R2 I3 reviewer; not RP0-R2 author, prior RRP0/RRM40/RF0 reviewer, Sorok/Pyat HQ, original C9/C12/C8/SCI05 issuer, production editor, implementer or self-reviewer.
**Immutable author target:** `f13f74d3f92ef0732dc33e5d3ebc314b6d0c70df` (parent `2da83f77d820b327169673386d52c4acefbbdd46`), 12 authored files.
**Exclusive review branch/startup:** `agent/sorok-syn02-review-rrp0-r2-c12-fork-storage-r1` at `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d`; remote ref matched before writing.
**Actual source cut:** S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`; S37 code at `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`; effective imported C12/JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`.
**Host:** Darwin 22.6.0 x86_64; Python 3.11.3; SQLite 3.40.1; local sourcefree pytest/sqlite only.
**Evidence grade:** own sourcefree test/probe execution; no native C8/C9/C11/C12/A5, no real B/world, no paid provider, no raw survey, no production database, no source edit.

## 0. Three court verdicts

| Court | Verdict | Independent disposition |
|---|---|---|
| **ENGINEERING** | `REVISE_PRECISE / C12_FORK_RED / C12_SIDECAR_NOT_FAIL_CLOSED / C9_OPTION_A_ACCEPT_SCOPED_DIRECTION / OWNER_FREEZE_HELD` | Actual C12 `fork` drops a clock-11 perception after a clock-10 cut while `QualifiedC12Store.verify` returns `ok`; the proposed sidecar detects that original case but returns `ok` for a same-count substituted child, a `SYNC_HELD` watermark, and a wrong base root. The separate C9 actor DB direction is compatible with the frozen S36 readset, but its SQL/probe helper is not an owner-frozen implementation. |
| **SCIENCE** | `HOLD / RULE_A_T_SCI05_UNISSUED` | No CAN008/CAN011 Rule A/T, SCI05 admission, memory/formation law, true-nochange law, or actor-person result is issued or proved. The S36 production registries remain empty; targetless `NO_PROPOSAL` is correctly held rather than promoted. |
| **AUTHORITY** | `HOLD / NO_NATIVE_GRANT` | No C9/C12/C8/C11/Pyat/CAN/ADP/SCI05 storage or source-owner authority, native C12 release, A0–A5 person, provider account, or production permission is granted. F1.1 is not authorized. |

The author's `REVISE_PRECISE` headline is directionally right but too weak for two claims: the actual C12 fork is a **reproduced RED source defect**, and the proposed C12 sidecar is **not currently a fail-closed guard**. The C9 Option A *topology* remains the best scoped design direction, but its actor contract and probe helper are not owner-freezable.

## 1. What was independently executed

| Check | Own result | Evidence level |
|---|---|---|
| S36 source tests at `8da78d8` | **39 passed** | Own sourcefree pytest; not native C9 |
| BP4/C12 source tests at JOIN-E `7bf2da3` | **15 passed** | Own sourcefree pytest; not native C12 |
| `probe_s36_legacy.py` | PASS; 7 tables; old receipt preserved; added table changes future before-hash | Own rerun of author probe |
| `probe_legacy_bridge.py` | PASS; S36 targetless → actor `HELD_MISSING_RULE`; no false true-nochange | Own rerun |
| `probe_actor_authority.py` | PASS for its written cases; **same-key same-digest positive replay is not implemented**; HELD status axes can be inconsistent | Own rerun + adversarial audit |
| `probe_outbox.py` | PASS for its written C4/C5 cases; direct SQL, not a live C12 mirror | Own rerun |
| `probe_c12_mirror.py` | PASS except actual **C12 fork loss**; sidecar detects the original count loss | Own rerun |
| Own C12/fork/sidecar probe | Parent 2 perceptions; fork clock 10; child 1; both actual verifies `ok`; child root tamper still `ok`; same-count child sidecar `ok`; `SYNC_HELD` watermark sidecar `ok`; wrong base root sidecar `ok` | Own actual-source execution |
| C9 idempotency/status probe | same key+same digest raises raw `UNIQUE constraint failed`; HELD receipt records `HELD_MISSING_RULE` + `COMMITTED_CHANGE` + `HELD` | Own audit of author helper |
| Full S37 targetless/cold suite, native C8/C9/C12, C11/A5, real B, paid provider | **NOT_RUN** | Not a pass |

No worker PASS was accepted solely from its return. The author's 39/15 counts and original C12 failure are independently confirmed; the sidecar false-clean and C9 helper gaps are additional independent findings.

## 2. C12 fork perception loss — RED reproduced

**Actual source:** `bp4/store.py` at JOIN-E `7bf2da3`, SHA-256 `bb7bd721fa6b021a5b5163427495fd308236788d1738b8326f9f1093159b3c8b`; `r26e/c12_integrity.py`, SHA-256 `534780fe4631caadacac73e457afbb86bcc207686b1ebb433087ad6270abf710`.

- `C12Store._last_clock()` (`store.py:135-143`) scans only `episode`, `world_event`, and `checkpoint`; it excludes `perception`.
- `record_perception()` (`store.py:195-214`) allows a perception at a clock greater than the last non-perception clock.
- `fork()` (`store.py:323-367`) derives `fork_clock = self.last_clock(parent)` and copies perception rows only with `clock <= fork_clock` (`:333-351`).
- The child `root_hash` includes copied episode/world/checkpoint hashes only (`:353-360`); perception identity is absent.
- `branch.root_hash` is mutable because append-only triggers cover only episode/world/perception/checkpoint (`:83-84`), and `fork` updates the child branch row (`:361-364`).
- `QualifiedC12Store.verify()` (`c12_integrity.py:31-64`) checks row preimages and sequence contiguity, not `branch.root_hash`, `root_counts`, fork ancestry, or perception-cut identity.
- Direct `C12Store.fork()` has no transaction; `joined/lineage.py:129-152` adds a SAVEPOINT in one wrapper, but the store API is directly callable.

Own actual-source output:

```text
root_last_clock 10
root_perceptions 2 [10, 11]
fork_clock 10
child_perceptions 1 [10]
parent_verify True
child_verify True
parent_root_hash ''
child_root_hash c5146b7a4b917d90e11b3b77b72dc5cb831a614113e35e7c23cccde993ed23e4
child_verify_after_root_tamper True
```

**Rival:** the clock-11 perception is an invalid append, or the fork correctly inherits only the causal cut. Both fail: `record_perception` accepts clock 11 because it compares against the last non-perception clock, and the child carries a lost actor-visible impression while the actual C12 verifier calls the branch clean. This is a source-level **RED**, not a fixture artifact.

**Repair/owner:** C12 original source owner must patch `fork`/verification or install a hard guard. No reviewer edit is authorized.

## 3. C12 sidecar is not fail-closed — RED/REVISE_PRECISE

The author's proposed `mirror_verify` (`probe_c12_mirror.py:38-95`) is not sufficient as a guard:

- `:63-64` only checks `len(child perceptions) < base_c12_perception_count`; it does not compare perception identity or the full base set. A child can lose the parent's clock-11 perception and add a different clock-10 perception, keeping the same count.
- `:66-71` reads `watermark_state` but never checks that it equals `CLEAN`; `SYNC_HELD` can still return `ok`.
- `:61-62` rejects only `FORK_HELD`, not `MIRROR_HELD`.
- `:84-90` checks only a parent watermark, not `base_c12_root_hash`, the base perception set, or the parent count/identity.
- `schema_mirror.sql:27-30` stores only `base_c12_perception_count`, not a base perception identity/hash; `:63-79` allows non-CLEAN watermark states; `:99-104` makes mirror branch rows immutable but does not prevent a wrong row being inserted.
- Mirror receipt `c12_root_hash`/`c12_last_clock` are not validated against actual C12 in `mirror_verify`.

Own actual-source/author-sidecar outputs:

```text
same_count_sidecar_ok True []
sync_held_watermark_sidecar_ok True []
wrong_base_root_sidecar_ok True []
```

The same-count child was produced by taking the bad fork (parent 2, child 1), adding a different clock-10 world event/perception to the child (count 2, parent clock-11 perception absent), and leaving the child branch root unchanged; actual C12 `verify` remained `ok` and the author's sidecar also returned `ok`.

**Rival:** the sidecar is only a detector, not a guard. That is exactly why it cannot be used to freeze clean forks: a detector that returns `CLEAN` for substitution, held watermark, and wrong base is not fail-closed. The owner guard must compare exact base perception identity/root and must inspect all held states.

**Repair/owner:** C12 owner must add exact base-perception identity/hash, base-root and watermark-state checks, and per-receipt C12 root/clock checks if the sidecar is retained. The actual C12 fork guard must not depend on the current count-only sidecar.

## 4. S36 readset and the C9 Option A topology

**Actual source:** `S36/candidate/transaction.py` at `8da78d8`, SHA-256 `d8d5d36ff68a1fa254c829ffa07a8d19699533769791a6d49b0cdfdd23baa803`.

- `CandidateStore.__init__` creates exactly seven tables (`transaction.py:73-89`): `occurrence`, `event_identity`, `response`, `target_state`, `target_journal`, `receipt`, `clock`.
- `_logical_readset()` (`:115-126`) captures all `sqlite_master` schema rows, `schema_version`/`user_version`/`application_id`, and every row of every table.
- `commit()` takes the before-snapshot before `BEGIN IMMEDIATE` (`:288-292`), requires exact schema equality (`:362-364`), preserves `user_version`/`application_id` (`:365-367`), and rejects any non-additive row set (`:368-370`).
- `target_state.id` and `event_identity.event_id` are global, not actor/branch scoped (`:81-88`).
- The production S36 Rule A/T registries are empty; absent a proposal, `evaluate_target` returns `NO_CHANGE/NO_PROPOSAL` (`target_rules.py:311-313`), which is not an evaluated `TRUE_NO_CHANGE_EVALUATED`.

Own S36 probe output:

```text
PASS s36_legacy: actual targetless receipt committed; old table count=7
PASS s36_legacy: old receipt hash=1cec8633d861959c7d4b744c6770f9720110e977f021f460a1608e1aebbf4ee9
PASS s36_legacy: same-schema actor table changes readset domain;
  future legacy before=9cfbe2777fa2788e0912d9cf87fd47bbf1b17b6f99f7f0a4b97e68a6c65b8d68
PASS s36_legacy: mutable actor row is non-additive under old all-table row-set invariant
PASS s36_legacy: old receipt/RESPONSE rows remain byte-identical
```

The author's **Option A direction — frozen legacy S36 candidate publication DB + separate versioned `c9_actor.sqlite` + C12 world + read-only mirror** is **`ACCEPT_SCOPED` as a topology**. It preserves the old seven-table receipt domain, avoids putting mutable actor head/outbox in the legacy DB, and need not create a second psyche. The `probe_legacy_bridge` mapping of old `NO_PROPOSAL` to actor `HELD_MISSING_RULE` is correct; it does not fabricate `TRUE_NO_CHANGE_EVALUATED`.

This acceptance is architectural only. It does not freeze the C9 schema, does not implement a C9 actor writer, and does not cure the C12 fork defect.

## 5. C9 actor authority — scoped direction, not owner-freezable

`probe_actor_authority.py` demonstrates useful sourcefree SQL behavior: `BEGIN IMMEDIATE`, head CAS, version/receipt/attempt/outbox, scoped target IDs, held → new attempt, append-only triggers, and rollback. The output is:

```text
PASS actor_authority: atomic final/held/requalification, CAS, idempotency,
  target scope, append-only and rollback
PASS actor_head=version=2 receipt_seq=3 finalized_seq=3
```

`probe_outbox.py` demonstrates C4/C5-shaped PENDING/PROJECTED/ACKED and duplicate mirror rejection at the SQL level, but it is a direct SQL probe, not an actual C9/C12 adapter.

Independent gaps:

1. **Idempotent positive replay is not implemented.** `probe_actor_authority.publish()` (`:95-203`) computes `seq` and inserts; it never looks up `event_attempt.idempotency_key` before insertion. Own run of the author helper:

```text
same_key_same_digest_error IntegrityError UNIQUE constraint failed: event_attempt.idempotency_key
```

The contract text says a same-key/same-digest retry returns the exact existing receipt and never reruns Rule T. The SQL unique constraint rejects the retry instead; the application path is absent and the probe's “idempotency” claim is unproven.

2. **HELD status axes can be contradictory.** The same helper wrote:

```text
held_status_axes ('HELD_MISSING_RULE', 'COMMITTED_CHANGE', 'HELD')
```

`decision_receipt` (`schema_actor.sql:153-247`) constrains final kinds but does not reject a `HELD_MISSING_RULE` decision carrying `rule_t_status='COMMITTED_CHANGE'`. A held event must not look like a committed Rule T; the owner must enforce the cross-axis invariant or write explicit raw source statuses.

3. **No actual C9 implementation.** The helper is a sourcefree test harness; there is no `C9ActorPublisher`, no live legacy adapter, no actual C9 source edit, and no `ActorAwareProduct`. The C9 schema is TEST_ONLY and `NOT_OWNER_FROZEN`.

4. **No actual C12 mirror writer.** `probe_outbox` inserts mirror rows directly; `mirror_verify` has the false-clean defects in §3. The C9 → C12 outbox contract remains a proposal.

5. **Legacy/target scope is directionally right.** The scoped `actor_target` and frozen legacy DB solve the prior `target_state`/readset conflict in principle; the author probe did write the same target ID for A and B and read only the scoped row. This supports `ACCEPT_SCOPED` for the topology, not for a production storage freeze.

## 6. Science and authority

**Science — `HOLD`.** S36 production response and target registries are empty (`response_rules.py:122-129`, `target_rules.py:109-116`); the targetless path is `NO_PROPOSAL`, not a true evaluated nochange. The bridge correctly maps it to `HELD_MISSING_RULE`. No Rule A/T, SCI05, memory, formation, care, motive, or learning law is issued by these probes or tests. The 39/15 tests are sourcefree technical tests, not a person.

**Authority — `HOLD / NO_NATIVE_GRANT`.** No C9/C12/C8/Pyat/CAN/ADP/SCI05 owner approval or native C11/C12/A5 release is present. The C9 and C12 source owners are distinct from this reviewer and the RP0-R2 author. C8 remains TEST_ONLY/process-local; no actual independent B or world receipt was run. The proposed C12 sidecar is not a source authority and cannot make a fork clean.

## 7. C12 owner decision: patch vs guard

**The actual C12 defect is reproduced and cannot remain a “clean fork” behavior.** The owner must choose and freeze one:

### Preferred patch

- Add perception to the fork-cut calculation: `cut = max(last_episode, last_world, last_checkpoint, last_perception)`.
- Copy all rows at the exact cut; include perception identity (event_id, actor_id, clock, channel, sequence/hash) in `root_hash`/`root_counts`.
- Make branch insert + copies + root/counters one transaction (or a proven owner savepoint wrapper used by every fork path).
- Validate parent/child counts, exact perception set, branch ancestry, root/root_counts, and deterministic cold reopen.
- Add tests for clock-11-only perception, same-count substitution, root tamper, cold reopen, partial-fork crash, and no phantom suffix.
- Owner: C12 BP4/r26e source owner. First consumer: C12 fork/open and later A0–A5.

### Safe fallback guard

- If any `max(perception.clock) > last_nonperception_clock`, return `FORK_HELD`; do not copy or claim `CLEAN`.
- If exact perception identity, base root, branch root/counts, or parent ancestry cannot be proved, `FORK_HELD`.
- Apply to direct `C12Store.fork` and every product wrapper; no clean fork through another API.
- The sidecar must compare exact base perception identity/hash, base root, `watermark_state`, `mirror_state`, and per-receipt C12 root/clock; the current count-only `mirror_verify` is not sufficient.
- Owner: C12 source owner. First consumer: C12 fork/open/cold and A0–A5.

**Reviewer recommendation:** use **`FORK_HELD` now** as the minimum safe owner guard, and do **not** rely on the current sidecar. A patch is preferable after owner source review, but this reviewer does not authorize it. The original C12 owner, not RRP0-R2, must select the exact code/branch.

## 8. Joint C9/C12 storage-owner freeze blockers

No storage-owner freeze is issued. Before F1.1:

1. **C12:** actual fork patch or hard `FORK_HELD` guard; transactional fork; perception-inclusive cut/root/count; branch root/count verification; exact perception identity; sidecar false-clean defects repaired.
2. **C9:** owner-approved actor schema hash, actual actor-writer implementation, same-key/same-digest replay, typed conflicts, status-axis cross-checks, scoped target, append-only receipts, outbox and C12 branch binding; legacy S36 remains frozen.
3. **C8/world:** actual independent B/world receipt, source cut/as-of, C1 ambiguous-act recovery/no blind replay; BP3/C8O remain TEST_ONLY.
4. **Rules/memory:** original CAN008/CAN011 Rule A/T or explicit hold; SCI05 half2 implicit-dependence default hold; ADP016/017 actor-safe memory.
5. **Product/world:** irreversible 3–5 partial-batch policy remains undecided.
6. **Independent review:** this RRP0-R2 is not acceptance; a separate owner-reviewed implementation and reviewer are required.

**F1.1 remains not authorized.** The C9 separate actor authority is a good scoped direction; the C12 fork/sidecar blockers are critical and prevent any clean actor-aware fork or C9/C12 freeze.

**Reviewer token:** `RRP0_R2__C12_FORK_RED_REPRODUCED__SIDECAR_FALSE_CLEAN__C9_OPTION_A_ACCEPT_SCOPED_DIRECTION__OWNER_FREEZE_HELD__F1_1_NOT_AUTHORIZED__NO_NATIVE_GRANT`.
