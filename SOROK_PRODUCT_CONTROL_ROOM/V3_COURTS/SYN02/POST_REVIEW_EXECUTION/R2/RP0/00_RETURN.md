# SYN02-RP0-R2 — physical C9/C12 contract compatibility return

**Return status:** `RP0_R2_FIVE_FILES_DELIVERED__C12_IMPORTED_SOURCE_AND_DDL_RECOVERED__C9_FROZEN_LEGACY_PLUS_SEPARATE_ACTOR_AUTHORITY_SELECTED__C12_FORK_PERCEPTION_LOSS_RED__C12_OWNER_REPAIR_OR_GUARD_REQUIRED__ACTOR_CAS_OUTBOX_PROBES_PASS__OWNER_FREEZE_HELD__NO_NATIVE_GRANT`.

**Branch:** `agent/sorok-syn02-rp0-r2-physical-c9-c12-contract-r1`.

**Sealed startup:** `2da83f77d820b327169673386d52c4acefbbdd46`.

**Role:** independent source/engineering repair author; not C9/C12 storage owner, C8/world owner, original CAN/ADP/SCI05 issuer, HQ, production editor or own reviewer.

**Source cut:** actual S36/C9 and S37 code at `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`; effective imported C12 at JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`, `vendor/j/r26e/c12_integrity.py` plus `vendor/j/candidate/vendor/bp4/bp4/store.py`; actual S36 file hash `d8d5d36...`/blob `1a9c15b...`; actual C12 class hash `534780fe...`/blob `0c51c9d...`; actual C12 base store hash `bb7bd721...`/blob `69a58f43...`.

## 1. Three court verdicts

| Court | Verdict | Meaning |
|---|---|---|
| **ENGINEERING** | `REVISE_PRECISE / C9_OPTION_A_COMPATIBLE / C12_PHYSICAL_FORK_RED / OWNER_FREEZE_NOT_READY` | One C9 actor authority with a frozen legacy candidate domain and C12 sidecar is the compatible topology. Actor CAS/outbox/legacy bridge probes pass. Actual C12 fork has a perception-loss defect and must be repaired or guarded by its owner. F1.1 is not build-ready. |
| **SCIENCE** | `HOLD / RULE_A_T_SCI05_UNISSUED` | No need, motive, care, expectation, practice, memory, no-change or learning law is issued. All test rules are TEST_ONLY. |
| **AUTHORITY** | `NO_NATIVE_GRANT / FREEZE_HELD` | No C8/C9/C11/C12/Pyat/CAN/ADP/SCI05 or actor-storage owner approval is issued. The owner freeze remains a separate competent act. |

## 2. Five deliverables

All under `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_REVIEW_EXECUTION/R2/RP0/`:

1. `01_REAL_S36_C9_AND_IMPORTED_C12_DDL_FORENSICS.md` — actual C12 class/DDL, S36 seven-table readset, S37 targetless path, C8 boundary, probe evidence.
2. `02_ONE_ACTOR_LEGACY_READSET_COMPATIBLE_AUTHORITY_R2.md` — selected Option A, target/branch/epoch scope, legacy bridge, C12 sidecar, alternative comparison, source-specific implementation contract.
3. `03_VERSIONED_SQL_CAS_OUTBOX_RECOVERY_CONTRACT_R2.md` — C9 actor DDL/CAS/outbox/held requalification, C12 mirror, SCI05/status axes, C0–C7, migration and acceptance gate.
4. `04_SOURCEFREE_SQL_FAULT_PROBES_AND_OWNER_DOCKET.md` — executed commands/results, actual C12 failure, owner repair/freeze docket.
5. `00_RETURN.md` — this return.

`probes/schema_actor.sql`, `probes/schema_mirror.sql`, and the four probe scripts are sourcefree evidence/test fixtures, not production code.

## 3. What physically changed the decision

### C12 is now physically known

The effective import is not missing. `QualifiedC12Store` is a subclass of `bp4.store.C12Store` and overrides only `verify`. Actual C12 DDL has `meta`, `branch`, `episode`, `world_event`, `perception`, `checkpoint`; append-only triggers cover only the last four, `branch` is mutable, and no actor mirror/head/version/watermark/C9 receipt exists. Actual probe PRAGMAs: `journal_mode='delete'`, `synchronous=2` (FULL), `foreign_keys=1`.

### Actual C12 fork defect — RED

Actual `C12Store.fork` computes `fork_clock` from episode/world_event/checkpoint, not perception. In the probe, root had perceptions at clock 10 and 11; `fork_clock=10`; the child received only one perception. Actual `QualifiedC12Store.verify` returned `ok` for both branches. The sidecar detects the loss as `C12_FORK_PERCEPTION_LOSS:alt_bad`. C12 owner must include perception in the fork cut/root/count and make fork transactional, or enforce a pre-fork `FORK_HELD` guard. Until then clean actor-aware fork is prohibited.

### Legacy S36 readset is not mutable

Actual `CandidateStore._logical_readset()` captures all schema/tables/rows and `commit()` rejects non-additive row changes. The probe confirmed 7 legacy tables and a targetless receipt; adding actor tables to a copy changed the future legacy before-hash while old rows remained byte-identical. Therefore mutable actor head/outbox cannot be added to the legacy schema. The selected contract freezes the legacy candidate publication DB and uses a separate versioned `c9_actor.sqlite` as the single canonical actor authority.

## 4. Executed evidence

| Check | Result |
|---|---|
| Actual S36 tests | **39 passed** |
| Actual BP4/C12 tests | **15 passed** |
| `probe_s36_legacy.py` | PASS: actual targetless receipt, old 7-table domain, added-table counterexample, old rows unchanged |
| `probe_legacy_bridge.py` | PASS: actual S36 receipt → actor `HELD_MISSING_RULE`, no false true-nochange, no actor target, old DB unchanged |
| `probe_actor_authority.py` | PASS: final/held/requalification, CAS, idempotency, scoped targets, append-only, rollback |
| `probe_outbox.py` | PASS: C4/C5 outbox, duplicate mirror rejection, no new actor version |
| `probe_c12_mirror.py` | PASS on actual C12 root/fork/cold and sidecar anchors; **FAIL actual C12 perception-loss fork**, sidecar detects; branch-root tamper detected |
| `probe_c12_mirror.py` C12 PRAGMAs | `journal_mode=delete`, `synchronous=FULL`, `foreign_keys=ON` |

The C12 `FAIL` is a source finding, not a failure of the actor DDL. It blocks a clean C12 freeze.

## 5. Selected compatible architecture

```text
frozen S36 candidate DB  = legacy occurrence/response/target/receipt publication
c9_actor.sqlite          = sole canonical actor head/version/decision/outbox authority
c12.sqlite               = actual QualifiedC12Store world/episode/perception/checkpoint
c12_actor_mirror.sqlite  = C12-owned read-only actor projection + watermark
```

The legacy DB is not modified. The actor authority is not a second psyche. C12 does not write Rule T. No cross-database ACID is claimed. The bridge uses immutable old receipt identity, actor CAS, a C12 outbox and fail-closed reconciliation.

The C9 actor schema is in `probes/schema_actor.sql`; C12 sidecar in `probes/schema_mirror.sql`; exact transaction/recovery text in `03`. C9 actor authority uses one `BEGIN IMMEDIATE` for head CAS + version + receipt + attempt + outbox. HELD receipts advance operational sequence but not semantic actor version. FINALIZED event identity is unique per branch/epoch; a held attempt can be requalified by a new owner-authorized attempt, but a final decision is never silently rerun.

## 6. C12 owner repair docket

C12 owner must choose and freeze one before F1.1:

1. **Patch:** fork cut includes perception, copies exact parent rows, includes perception in root/count, uses one transaction, verifies parent/child counts and branch ancestry.
2. **Guard:** reject fork when `max(perception.clock) > last_clock`; require a qualified checkpoint/cut; return `FORK_HELD`, never `CLEAN`.

Sidecar `base_c12_perception_count` and `C12_ROOT_MISMATCH` checks remain mandatory. C12 `branch.root_hash` is mutable and actual `QualifiedC12Store.verify` does not validate it.

## 7. Joint storage-owner freeze conditions

No owner freeze is issued. Before implementation, C9 and C12 owners must jointly approve:

- exact C9 legacy path and separate actor DB path, schema hash, PRAGMAs and exclusive actor writer;
- exact C12 source/DDL, sidecar path, fork repair/guard, root/watermark/branch checks and transactional fork;
- legacy receipt/hash domain preservation and old S37 targetless behavior;
- actor branch/epoch, target scope, CAS, idempotency, outbox and recovery;
- C8 actual world receipt/C1 source recovery; no BP3 process gate as native proof;
- CAN008/CAN011 Rule A/T, ADP016/017/SCI05 and product/world batch policy;
- independent review of this return and exact probes.

C8, CAN, ADP, SCI05 and Pyat owners remain separate. No reviewer or author here can issue their grant.

## 8. NOT_RUN

Full S37 targetless/cold suite, current C8 native custody, actual C9/C12 assembled runtime, C12 owner repair, C11/Pyat, A0–A5, paid provider/model calls, native person. These are not passes.

## 9. Next qualified gate

1. C12 owner repairs/guards actual fork perception loss and freezes exact source.
2. C9 owner reviews/accepts or rejects Option A and schema hash.
3. C8/CAN/ADP/SCI05/product owners answer their finite gates in parallel.
4. Independent storage/reviewer checks C0–C7 and source-specific output.
5. Only after that may a separately authorized F1.1 worker implement.

**Remote SHA:** deliberately not embedded in this self-modifying return; the committing worker must read back the final remote branch SHA after push and report it externally.

**No source edit. No production DB. No storage-owner freeze. No Rule A/T. No science. No native C12/A5. STOP.**
