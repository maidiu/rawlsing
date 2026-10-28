# SYN02-RRP0-R2 — acceptance and owner gate

**Review status:** `RRP0_R2_REVISE_PRECISE__C12_FORK_RED_REPRODUCED__C12_SIDECAR_NOT_FAIL_CLOSED__C9_OPTION_A_ACCEPT_SCOPED_DIRECTION__OWNER_FREEZE_HELD__F1_1_NOT_AUTHORIZED__NO_NATIVE_GRANT`.

**Owner roles:** C12/BP4/r26e source owner; C9 actor storage owner; C8/world source owner; original CAN008/CAN011/ADP016/017/SCI05 issuers; product/world batch-policy owner; independent implementation reviewer. This review is none of those roles.

## 1. C12 critical blocker — actual RED

The actual imported C12 code loses a perception-only clock-11 row when forking after a clock-10 non-perception cut. The child count is 1 while the parent has 2; both actual `QualifiedC12Store.verify` calls return `ok`; a direct branch-root tamper also returns `ok`. The proposed sidecar detects the original count loss but returns `ok` for same-count substitution, `SYNC_HELD`, and a wrong base root.

**This blocks any clean C12 fork and any C9/C12 actor-mirror freeze.**

### Owner decision A — preferred patch

C12 source owner patches the actual fork/verification path:

```text
fork_cut = max(last_episode_clock, last_world_clock,
               last_checkpoint_clock, last_perception_clock)
```

- Copy exactly parent rows at the full cut, including every perception identity.
- Include a sorted perception identity/hash set in the child `root_hash` and `root_counts`.
- Make branch insert + row copies + root/counter update one transaction or one proven savepoint used by every fork entry point.
- Validate parent/child counts, exact perception set, branch ancestry, root and counts; reject any gap or mismatch.
- Make `QualifiedC12Store.verify` or a mandatory owner guard validate `branch.root_hash`, `root_counts`, and exact perception identity, not only row preimages.
- Test clock-11 perception, same-count substitution, root tamper, cold reopen, partial-fork crash, and no phantom suffix.

**Owner:** C12 BP4/r26e source owner. **First consumer:** C12 fork/open/cold, then actor-aware C12/A0–A5. **Not authorized by this reviewer.**

### Owner decision B — minimum safe guard

If the source patch cannot be owner-qualified immediately, disable clean fork with a hard guard:

```text
if max(perception.clock) > max(episode/world/checkpoint clock):
    FORK_HELD
if exact perception identity/base root/branch ancestry/counts cannot be proved:
    FORK_HELD
```

- Apply at actual `C12Store.fork` and every product wrapper; no alternate clean-fork path.
- Never return `CLEAN` when the cut is incomplete or the exact base perception set is unknown.
- Keep the current C12 data and receipts immutable; do not mutate historical rows.
- The proposed sidecar must not be used as a substitute for this guard until it checks exact base perception identity, base root, `watermark_state`, `mirror_state`, and per-receipt C12 root/clock.
- Test the guard on the actual clock-10/11 case and on a same-count substituted child.

**Owner:** C12 source owner. **First consumer:** C12 fork/open/cold and A0–A5.

**Reviewer decision:** `FORK_HELD` guard now; patch preferred later. The current source must not be called a clean C12 fork.

### Required C12 tests before freeze

| Test | Required result |
|---|---|
| Parent checkpoint/world at clock 10; perception at clock 11; fork | Child has both perceptions and fork cut 11, or `FORK_HELD` |
| Child loses clock-11 perception but gains a different clock-10 perception (same count) | Rejected by identity/root check, never `CLEAN` |
| Direct `branch.root_hash` tamper | Actual verifier/guard rejects |
| Direct `fork` crash between branch insert/copy/root update | No partial clean child; rollback or `FORK_HELD` |
| `mirror_watermark` `SYNC_HELD`/`MIRROR_HELD` | Sidecar refuses `CLEAN` |
| Wrong `base_c12_root_hash` or base perception set | Sidecar refuses |
| Cold reopen after clean/patch/guard | Deterministic same result; no lost perception |

### Sidecar repair (C12 owner)

If the sidecar is retained:

- Store a **base perception identity/hash**, not only `base_c12_perception_count`.
- Check the actual parent base root/perception set, not just the parent watermark.
- Enforce `watermark_state == CLEAN`; reject `SYNC_HELD`, `MIRROR_CONFLICT`, `FORK_HELD`, and `MIRROR_HELD`.
- Check each mirror receipt's C12 root/clock/sequence and C9 receipt/version; do not trust a count or a caller-supplied root.
- Add tests for same-count substitution, wrong base root, held watermark, `MIRROR_HELD`, and duplicate/gap receipts.

The current `probe_c12_mirror.mirror_verify` fails these acceptance requirements; its original count-loss detection is not enough.

## 2. C9 separate actor authority — scoped direction, not owner freeze

**`ACCEPT_SCOPED` design direction:** frozen legacy S36 candidate DB + separate `c9_actor.sqlite` + actual C12 world + read-only C12 mirror. This preserves the seven-table S36 readset and does not put mutable actor head/outbox in the legacy DB. It is one C9 actor authority, not a second psyche, and no cross-database ACID is claimed.

The direction is supported by:

- actual 39 S36 tests and the seven-table probe;
- the bridge mapping old targetless `NO_PROPOSAL` to `HELD_MISSING_RULE`, not true nochange;
- scoped actor target IDs in the probe;
- CAS/held requalification/outbox probes at sourcefree SQL grain.

It is **not** an owner-freezable implementation:

- `probe_actor_authority.publish()` has no positive idempotent replay; same-key/same-digest raises `UNIQUE constraint failed` instead of returning the existing receipt.
- The held path can record `HELD_MISSING_RULE` with `rule_t_status='COMMITTED_CHANGE'`; no cross-axis invariant prevents this.
- The actor writer, legacy bridge adapter, C9 E2 reader, and C12 mirror writer are not implemented.
- The C9 schema is TEST_ONLY and not owner-frozen; `source_grant_hash`, world receipts, and C8 links are test values.
- The proposed outbox/mirror integration has no actual C12 writer and the sidecar false-clean defects above.

### C9 owner freeze conditions

- Freeze exact legacy S36 path and separate `c9_actor.sqlite` path/schema hash.
- Require one exclusive actor writer and a `BEGIN IMMEDIATE` head CAS/version/receipt/attempt/outbox transaction.
- Implement same-key/same-digest exact receipt replay; typed same-key/different-digest conflict; typed finalized-event duplicate; held → new owner-authorized attempt with `prior_attempt_id`.
- Enforce orthogonal status axes: a held decision cannot claim committed Rule T; final change/nochange requires exact rule/readset/semantic hash; SCI05 denied/held cannot finalize.
- Bind actor branch/epoch, scoped target, C12 branch/root/watermark, C8 world receipt and legacy bridge.
- Prove no mutable actor rows affect the frozen legacy seven-table readset; preserve old S36 receipt hashes/rows.
- First consumer: C9 E2 semantic read; no implementation before owner freeze.

## 3. Joint C9/C12 freeze checklist

| Gate | State | Blocker |
|---|---|---|
| C12 source/DDL imported and identified | **DONE (sourcefree)** | Exact class/DDL recovered at JOIN-E `7bf2da3` |
| C12 fork clean/perception identity | **RED** | Actual clock-11 perception loss; no root verification |
| C12 sidecar fail-closed | **RED/REVISE** | Same-count, SYNC_HELD, wrong base return `ok` |
| C12 fork transaction | **REVISE** | Direct `C12Store.fork` is not transactional |
| S36 legacy readset preserved | **ACCEPT_SCOPED** | 7 tables; added actor table changes before-hash; separate actor DB needed |
| C9 Option A actor DB | **ACCEPT_SCOPED design direction** | Not owner-frozen; helper gaps |
| C9 idempotency/status/outbox | **REVISE_PRECISE** | Positive replay absent; held status axis inconsistent; no live implementation |
| C8 independent world/B receipt and C1 recovery | **HOLD / NOT_RUN** | C8 remains TEST_ONLY/process-local |
| CAN008/CAN011 Rule A/T | **HOLD** | Empty production registries |
| SCI05/ADP016/017 memory | **HOLD** | No admission rule; implicit half2 default not operated |
| 3–5 irreversible batch policy | **HOLD** | Owner-undecided |
| Independent implementation review | **THIS REVIEW** | Does not authorize F1.1 |
| Native C11/C12/A5 | **NOT_RUN** | No native grant |

**No storage-owner freeze is issued.** C12 fork/guard and sidecar must be fixed first; C9 actor schema/implementation then reviewed; C8/Rule/SCI05/batch owners remain separate.

## 4. F1.1 gate

**F1.1 is not authorized.** The prerequisite sequence is:

1. C12 original owner selects and freezes patch or `FORK_HELD` guard; adds exact perception identity/root/transaction tests.
2. C12 sidecar is repaired or not used as a guard.
3. C9 storage owner freezes the actor DB schema and implements actual actor writer/CAS/outbox/idempotency/status.
4. C8 world/B and legacy bridge source receipts are qualified; C1 recovery is specified.
5. Original CAN008/CAN011/SCI05 owners issue or explicitly hold Rule A/T and memory admission.
6. Product/world owner selects irreversible batch policy.
7. Separate independent implementation reviewer checks actual code and cold/fork/C0–C7 tests.
8. Only then may a user-selected F1.1 implementation be considered.

Sourcefree SQL/probe success is not F1.1 authorization, a native C12, or a person.

## 5. Science and authority

**SCIENCE — `HOLD`.** The S36 production response/target registries are empty; targetless `NO_PROPOSAL` is not a true evaluated nochange. No Rule A/T, SCI05, memory, formation, care, motive, or learning law is issued. The 39/15 tests and probes are sourcefree technical evidence.

**AUTHORITY — `HOLD / NO_NATIVE_GRANT`.** C9/C12/C8 storage/source owners, original CAN/ADP/SCI05 issuers, Pyat C11/C12/A5, provider account, production permission and user-selected native execution remain separate. This reviewer cannot patch C12, freeze C9/C12, issue Rule A/T or approve F1.1.

## 6. Final disposition

The author's C9 Option A topology is a credible scoped design direction and its S36 compatibility evidence is confirmed. The C12 fork defect is an actual RED, and the proposed mirror verifier is not fail-closed; the C9 helper also has idempotency/status gaps. The correct next owner action is a C12 **`FORK_HELD` guard or owner-qualified patch**, followed by C9/C12 owner freeze review. Do not call any fork clean, do not freeze storage, and do not start F1.1 yet.

**Reviewer token:** `RRP0_R2__C12_FORK_RED_REPRODUCED__SIDECAR_FALSE_CLEAN__C9_OPTION_A_ACCEPT_SCOPED_DIRECTION__OWNER_FREEZE_HELD__F1_1_NOT_AUTHORIZED__NO_NATIVE_GRANT`.
