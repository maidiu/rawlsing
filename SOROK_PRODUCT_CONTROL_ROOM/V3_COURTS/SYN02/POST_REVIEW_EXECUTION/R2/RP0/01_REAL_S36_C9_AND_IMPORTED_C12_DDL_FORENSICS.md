# RP0-R2 / 01 — real S36/C9 and effective imported C12 physical forensics

**Status:** `DIRECT_PHYSICAL_SOURCE_AUDIT__C9_LEGACY_DOMAIN_MEASURED__C12_IMPORTED_CLASS_AND_DDL_RECOVERED__C12_FORK_PERCEPTION_LOSS_RED__NO_SOURCE_EDIT__NO_NATIVE_GRANT`.

**Role:** independent source/engineering repair author; not C9/C12 owner, original CAN/ADP/SCI05 issuer, HQ, production editor, or self-reviewer.

**Sealed subject:** review target `2da83f77d820b327169673386d52c4acefbbdd46`; governing commission `SOROK_SYN02/POST_REVIEW_EXECUTION/R2/COMMISSIONS/RP0-R2/00_COMMISSION.md`.

## 1. Exact source custody

| Subject | Exact cut / path | Blob | SHA-256 | Evidence |
|---|---|---|---|---|
| S36 candidate | `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`, `WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1/candidate/transaction.py` | `1a9c15b88f0dfc130e895f33ac536487f601aadd` | `d8d5d36ff68a1fa254c829ffa07a8d19699533769791a6d49b0cdfdd23baa803` | Direct extracted source; actual S36 tests 39 passed |
| S36 pipeline | same cut, `candidate/pipeline.py` | `80f6c5dc29693de8eb301109272d326ca9b8b5aa` | `ba8577ae77ed9f3ec291da91caebae1b2a809edb970d22f29db1173747ce05b6` | Direct source; `run_candidate_path` consumer |
| S36 producer contract | S37 `bootstrap.py` cut `8da78d8031a06a4bd7e1297fd713e573299c0860` | external S36 return | n/a | `CUTS["s36"]` at S37 bootstrap lines 42–47 |
| S37 product | `e1f3c1d...`, `s37/product.py` | `ef2830c443b89d3e46cb97305449adeb1a663829` | n/a | Direct source; imports qualified C12 at line 23 |
| S37 session | `e1f3c1d...`, `s37/session.py` | `5f769a00ed6899431c63a8c1c2b3cf9edaf00c6e` | n/a | Direct source; cold open lines 155–218 |
| S37 reader | `e1f3c1d...`, `s37/reader.py` | `8bbd8a93ee69def9e78ab343f007f58eb10dfcc4` | n/a | Direct source; targetless and zero-target checks lines 156–165 |
| S37 producer | `e1f3c1d...`, `s37/producer.py` | `223e399a224b49876b4f13dbdaf81140da17b3a0` | n/a | Direct source; targetless `NO_PROPOSAL` path lines 236–256 |
| Effective C12 module | JOIN-E `codex/sorok-join-e-20261022` `7bf2da302996491ddf34b9a039fea47ac982d135`, `vendor/j/r26e/c12_integrity.py` | `0c51c9d13f1065c41b16813f9827a21338e2d6cf` | `534780fe4631caadacac73e457afbb86bcc207686b1ebb433087ad6270abf710` | Direct import and `inspect.getfile` |
| Effective C12 base class | `vendor/j/candidate/vendor/bp4/bp4/store.py` | `69a58f43dc70d320f2fc476eeac324c82c37ee59` | `bb7bd721fa6b021a5b5163427495fd308236788d1738b8326f9f1093159b3c8b` | Direct source; DDL/fork/verify |
| JOIN-E lineage | `joined/lineage.py` | `deb55c6768f2d4fdcd0757c6e47a59b08a96a4ec` | n/a | Direct source; fork savepoint/validation |
| C8 BP3 | `vendor/j/candidate/vendor/bp2/vendor/bp3/c8_exclusive_writer.py` | `3632e1ef785041bc2612acbd31c3f01b7cff4341` | `334e591779dcd2f409f5afcf87cda26341ce4407da2a77b604c65c212d9c4263` | Direct source; TEST_ONLY process gate |
| C8O | `.../vendor/bp3/vendor/c8o_trusted_outbox.py` | `7d785d35be09ab2ca5877a89a7880c70f2fe488c` | `e872862baf85d9508ee70eaf70492cbab65242e1ae98f251503a3ce7b708d691` | Direct source; unpinned legacy writer/trust hold |

The S37 bootstrap resolves `S36_RETURN` to the S36 return and `JOIN_E_RETURN` to the warm JOIN-E closure; `joined/imports.py` places `vendor/j` and `vendor/j/candidate` on the path before `S37/product.py` imports `r26e.c12_integrity`. Direct import proof:

```text
QualifiedC12Store -> .../vendor/j/r26e/c12_integrity.py
base C12Store      -> .../vendor/j/candidate/vendor/bp4/bp4/store.py
r26e module        -> r26e.c12_integrity
```

This resolves the RRP0-source hold: the imported definition **is** physically available in the warm JOIN-E cut; it is not missing globally. It remains a TEST_ONLY source cut, not a native C12 release.

## 2. Actual C12 physical schema

`QualifiedC12Store` subclasses `bp4.store.C12Store` and overrides only `verify` (`r26e/c12_integrity.py:28–64`). It does **not** define `_ensure_root`, `fork`, or a mirror. `C12Store.__init__` (`bp4/store.py:38–87`) creates:

```text
meta(key,value)
branch(branch_id,parent_branch_id,fork_clock,root_hash,root_counts,
       created_clock,actor_ids)
episode(branch_id,seq,episode_id,actor_id,kind,clock,body,hash)
world_event(branch_id,seq,event_id,clock,body,hash)
perception(branch_id,seq,actor_id,event_id,clock,channel)
checkpoint(branch_id,seq,clock,state,hash)
```

Physical facts:

- `sqlite3.connect(..., isolation_level=None)` — autocommit connection, no explicit `PRAGMA journal_mode` or `synchronous` in C12 (`store.py:39–43`). Probe observed `journal_mode='delete'`, `synchronous=2` (FULL), `foreign_keys=1`.
- `PRAGMA foreign_keys=ON` only; no WAL set by this class (`store.py:45`).
- `branch` has **no** append-only update/delete trigger; `_append_only_triggers` is applied only to `episode`, `world_event`, `perception`, `checkpoint` (`store.py:83–84`). `fork` updates `branch.root_hash/root_counts` (`store.py:361–364`).
- No actor-version, actor-head, decision-receipt, outbox, C9 watermark, branch-epoch, or C9 receipt table. The actual C12 is a world/episode/perception/checkpoint store with an actor-id list, not an actor-state authority.
- `create_root` inserts a branch and one checkpoint (`store.py:99–109`). `_ensure_root` is in `bp4.product.BP4Product` (`bp4/product.py:74–91`) and is called by `S37TargetlessProduct`; it is not a C12 method.
- `QualifiedC12Store.verify` checks row body preimages, stored hashes and sequence contiguity for episode/world/checkpoint/perception (`c12_integrity.py:31–64`). It does **not** check branch root, root_counts, parent/fork ancestry, actor mirror, C9 watermark, or C12 world head.
- `C12Store.fork` copies rows by `clock<=fork_clock`, derives `fork_clock` from `_last_clock()` over episode/world/checkpoint only, updates root hash from copied episode/world/checkpoint hashes, and does not include perception hashes in `root_hash` (`store.py:323–367`). It is not itself a transaction; `joined/lineage.create_fork` wraps it in a SAVEPOINT (`lineage.py:129–152`), but the C12 class API can be called directly.

### C12 fork/perception physical defect — actual probe

The actual API permits a perception clock greater than the last episode/world/checkpoint clock. `C12Store.fork` then computes a lower `fork_clock` and drops that perception. Probe result:

```text
root: 2 perceptions (clock 10 and clock 11)
fork alt_bad: fork_clock=10
alt_bad perceptions=1
actual QualifiedC12Store.verify(root) = ok
actual QualifiedC12Store.verify(alt_bad) = ok
sidecar verifier: C12_FORK_PERCEPTION_LOSS:alt_bad
```

This is a source-level RED for clean fork: a real C12 fork can be internally “verified” while losing an actor-visible perception row. It is not fixed by the proposed actor sidecar; the sidecar detects the loss and must fail closed. Required C12-owner repair is in `03`/`04`; until the repair or a proven owner guard, C12 fork is `FORK_HELD`, never `CLEAN`.

## 3. Actual S36/C9 physical schema and readset

`CandidateStore` (`transaction.py:73–89`) has exactly seven tables:

```text
occurrence(hash PRIMARY KEY, body)
event_identity(event_id PRIMARY KEY, hash)
response(hash PRIMARY KEY, body)
target_state(id PRIMARY KEY, body)
target_journal(id PRIMARY KEY, body)
receipt(hash PRIMARY KEY, body)
clock(clock PRIMARY KEY)
```

`target_state.id` and `event_identity.event_id` are unscoped by actor/branch. `_logical_readset()` (`transaction.py:115–126`) captures **all** sqlite_master schema rows, `schema_version/user_version/application_id`, and every row of every table. `commit()` takes this `before` snapshot before `BEGIN IMMEDIATE`, writes response/target/receipt, then checks:

- schema exactly equal (`:363–364`);
- `user_version` and `application_id` unchanged (`:365–367`; `schema_version` is captured but not checked here);
- every before table row is a subset of the after rows (`:368–370`), so UPDATE/DELETE of any existing row is non-additive and rejected.

Consequences:

1. Adding mutable actor tables to the **same legacy DB** changes `sqlite_master`, so old/new publication readset domains differ. A new legacy receipt's `before_hash` includes the new schema/tables; old receipt rows remain but new legacy receipts are in a different domain.
2. Updating `actor_head`/`outbox` rows in the same DB would fail the additive row-set check whenever the old `commit` observed the before row.
3. The `before` snapshot is taken before `BEGIN IMMEDIATE` (`:288–292`), so a writer change between snapshot and lock is not a stable transaction snapshot.
4. `admit_occurrence` is a separate transaction from `commit` (`:128–158`, `:278–397`); the occurrence/event identity is not committed with the actor receipt.
5. S36 targetless `NO_CHANGE/NO_PROPOSAL` is not an evaluated Rule T: `evaluate_target` returns `_no_change(NO_PROPOSAL)` when proposal is absent (`target_rules.py:311–313`); S37 requires that exact branch/reason and zero target rows (`producer.py:247–256`, `reader.py:156–165`).

The actual S36 probe committed a targetless receipt (`1cec8633...`), table count 7, `before_hash=9c5137...`, `after_hash=07d380...`. A second physical copy with an added actor table produced a different future `before_hash` (`9cfbe2...`) while the old receipt/response bytes remained identical. This is the direct compatibility reason to keep the legacy domain frozen.

## 4. S37 effective product geometry

- `S37TargetlessProduct.__init__` constructs `QualifiedC12Store(root / "c12.sqlite")` (`product.py:23,79–87`) and calls the BP4 `_ensure_root` inherited path.
- `S37TargetlessProduct` has no actor version/head; it stores a `S36_TARGETLESS_RESPONSE` episode, a C12 checkpoint, and a `targetless.json` sidecar.
- `S37IntegratedSession.open` validates session metadata, branch lineage, S37 provenance, C12 root/branch verification, and S36 readback (`session.py:155–218`). It does **not** check a C9 actor receipt/outbox/watermark because none exists in the imported C12/current S37 path.
- `read_committed_s36` opens the C9 DB read-only, requires `target_branch=NO_CHANGE`, `target_reason=NO_PROPOSAL`, `target_id=''`, zero `target_state` rows, and a sealed S35 receipt (`reader.py:142–220`). It is a legacy targetless reader, not an actor-version-aware E2 reader.
- `S37Producer.stage_s36` requires a committed positive response with zero target proposals and `NO_PROPOSAL` (`producer.py:236–256`).

Therefore the current S37 “success” is a targetless technical product. It cannot be cited as a positive Rule T, a formed actor target, or an actor-state mirror.

## 5. C8 boundary

The inspected C8 source is TEST_ONLY:

- BP3 installs a **process-local** old-writer gate (`c8_exclusive_writer.py:1–18,95–119`); loading the module can close legacy methods only in that process.
- C8O explicitly documents the accepted unkeyed legacy writer bypass and unissued trusted anchor/capability (`c8o_trusted_outbox.py:1–36`).
- No C8 production anchor, independent B issuer, or recovery receipt is proved here. The proposed C9 design must consume a typed C8 receipt and must not replay a real B act; C1 remains a source-owner decision.

## 6. Actual tests and probes

### Executed

- S36 extracted source: `python3 -m pytest -q tests` → **39 passed**.
- BP4/C12 vendor tests: `PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing python3 -m pytest -q tests` → **15 passed**.
- `probe_s36_legacy.py`: targetless actual S36 receipt; old 7-table domain; added-table readset counterexample; old receipt unchanged.
- `probe_legacy_bridge.py`: actual S36 targetless receipt → actor `HELD_MISSING_RULE`; no actor version beyond genesis; outbox PENDING; no false true-nochange.
- `probe_actor_authority.py`: final/held/requalification, CAS, idempotency, target scope, append-only and rollback.
- `probe_outbox.py`: C4/C5 outbox and duplicate mirror rejection.
- `probe_c12_mirror.py`: actual C12 root/fork/cold; sidecar; **actual C12 fork perception loss**; root tamper detection; missing mirror fail-closed.

### Not run

- Full S37 targetless suite/cold open; current C8 native custody; actual C9/C12 production assembled runtime; native C11/C12/A0–A5; paid model/provider calls.
- C12 fork repair is not implemented; only detected and held.

## 7. Findings

| ID | Finding | Exact evidence | Status |
|---|---|---|---|
| **F01** | C12 imported class/DDL recovered; it is not missing. | `r26e/c12_integrity.py`, `bp4/store.py`; `inspect.getfile` probe | `ACCEPT_SCOPED_SOURCE` |
| **F02** | Actual C12 has no actor mirror/epoch/watermark; C12 `verify` does not validate branch root. | DDL `store.py:43–87`; verify `c12_integrity.py:31–64`; probe root tamper | `RED_FOR_ACTOR_MIRROR_WITHOUT_SIDECAR` |
| **F03** | Actual C12 fork drops perception-only clock rows; fork_clock excludes perception. | `store.py:135–145,323–367`; probe parent=2/alt_bad=1 | `RED_C12_FORK_PERCEPTION_LOSS`; owner repair/guard required |
| **F04** | S36 all-table additive readset conflicts with mutable actor head/outbox in the same schema. | `transaction.py:100–126,288–292,362–370`; probe old 7 tables, added-table new before hash | `REVISE_PRECISE`; choose frozen legacy + separate actor domain |
| **F05** | S36 target_state/event identity are global; old S37 requires zero target rows. | `transaction.py:81–88,319–320`; `reader.py:156–165`; `producer.py:247–256` | `REVISE_PRECISE`; scoped actor target + legacy targetless preservation |
| **F06** | C12 `fork` itself is not transactional; `joined.lineage` wrapper is separate. | `store.py:323–367`; `lineage.py:129–152` | `REVISE_PRECISE`; owner transaction/guard |
| **F07** | S36 no-proposal is not true nochange. | `target_rules.py:311–313`; `producer.py:249–253`; bridge probe | `ACCEPT_SCOPED`; map to HELD, not TRUE_NO_CHANGE |
| **F08** | C8 remains TEST_ONLY/process-local and cannot be called native. | BP3/C8O source above | `HOLD`; C8 owner |

**No source file, persistent DB, S36/S37/C12 module, or original science registry was edited by this work.**
