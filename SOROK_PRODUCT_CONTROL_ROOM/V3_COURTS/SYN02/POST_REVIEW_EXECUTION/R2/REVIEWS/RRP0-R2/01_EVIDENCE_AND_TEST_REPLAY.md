# SYN02-RRP0-R2 — evidence and test replay

**Review branch/startup:** `agent/sorok-syn02-review-rrp0-r2-c12-fork-storage-r1` at `a7a6c781e158cd1317c0ecd0d6e1e542a4fd633d` (remote ref matched before writing).
**Immutable author target:** `f13f74d3f92ef0732dc33e5d3ebc314b6d0c70df`, parent `2da83f77d820b327169673386d52c4acefbbdd46`.
**Host:** Darwin 22.6.0 x86_64; Python 3.11.3; SQLite 3.40.1.
**Execution grade:** own sourcefree Python/pytest/sqlite; no native C8/C9/C11/C12/A5, real B/world, raw survey, paid provider or production DB.
**Source edit:** none by this reviewer.

## 1. Target custody

`git show --stat f13f74...` reports 12 added files, 2,238 insertions, all under `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_REVIEW_EXECUTION/R2/RP0/`. The author target is one commit ahead of its parent `2da83...`. Review branch startup is `a7a6c...`; the target source was materialized only as a detached read-only worktree.

Author file SHA-256:

| File | SHA-256 |
|---|---|
| `RP0/00_RETURN.md` | `baf15e8477a35b6eb772e89c58e3a102a2d04f372e76b1d552282b78dd245b7e` |
| `RP0/01_REAL_S36_C9_AND_IMPORTED_C12_DDL_FORENSICS.md` | `c6b69ff2f0e678f7ea26aa2a65d18f0af3b230b0c4915426638dbfc114faca66` |
| `RP0/02_ONE_ACTOR_LEGACY_READSET_COMPATIBLE_AUTHORITY_R2.md` | `a44c1d1571bbdf835a7a2fa24b17ded03dd3c6e61e75a18d342066ee737edbe1` |
| `RP0/03_VERSIONED_SQL_CAS_OUTBOX_RECOVERY_CONTRACT_R2.md` | `6c7901da3f835c30715de883b2c043121d155e0e17f4f15e0618018e36495bd0` |
| `RP0/04_SOURCEFREE_SQL_FAULT_PROBES_AND_OWNER_DOCKET.md` | `5b10ebda31269159e08aa88027ef1778e91358172d381d7c8336b20d96b7c7b8` |
| `RP0/probes/probe_actor_authority.py` | `446cc9dee5d63d09bf7544298ee7f76f458eec8b91ad5e452dd1a69fccc26e5c` |
| `RP0/probes/probe_c12_mirror.py` | `35f9285672c73a1ddc9fdcb2ad2ceb0a76fad9be7c7b7f1af47f5bbb38918282` |
| `RP0/probes/probe_legacy_bridge.py` | `d34cbad018e0f224721d84d460396fac912f6b44ba0d7b7d38d9e3d91b4f52fc` |
| `RP0/probes/probe_outbox.py` | `53e0945a39256bb133b698e5065ecd2dad6e27027b9f77a3a60e966aabf69991` |
| `RP0/probes/probe_s36_legacy.py` | `3ca8c1040f3e3cc0e09e6da9c9b90c5f4c5873fce7ad18e878f2fcca9d549eff` |
| `RP0/probes/schema_actor.sql` | `05edec71c2fc139a02066307a515a1d17a46c53ed1c2d7aeac1c1f4c65c9f80b` |
| `RP0/probes/schema_mirror.sql` | `8b0e9f4c3859bc5756db3d56ba7686a54cbcfb7368363a8cb2981e0a3976d299` |

### Actual external source identity

| Source | Cut / SHA-256 |
|---|---|
| S36 `candidate/transaction.py` | `8da78d8031a06a4bd7e1297fd713e573299c0860`; `d8d5d36ff68a1fa254c829ffa07a8d19699533769791a6d49b0cdfdd23baa803` |
| S36 `candidate/pipeline.py` | same cut; `ba8577ae77ed9f3ec291da91caebae1b2a809edb970d22f29db1173747ce05b6` |
| S36 `candidate/target_rules.py` | same cut; `e5d38865d2a4d50a904a387b2a8770bda55567dcef670e97c0dd696c8f7475a5` |
| S36 `candidate/response_rules.py` | same cut; `a1067e97b7309c543029406035e2233dcefb38d571ca198d38f17d86b024889c` |
| `bp4/store.py` | JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`; `bb7bd721fa6b021a5b5163427495fd308236788d1738b8326f9f1093159b3c8b` |
| `r26e/c12_integrity.py` | same JOIN-E cut; `534780fe4631caadacac73e457afbb86bcc207686b1ebb433087ad6270abf710` |
| `joined/lineage.py` | same JOIN-E cut; `5578951d4dcce3839a114036684336fa759f537b62d8ed1174b0a6a0b03d7383` |

`inspect.getfile` independently resolves `QualifiedC12Store` to `.../vendor/j/r26e/c12_integrity.py` and its base to `.../vendor/j/candidate/vendor/bp4/bp4/store.py`.

Prior custody read: RP0 `00ffb...`, RRP0 `529433...`, RM40 `653d...`, RRM40 `0c181...`, F0 `9903...`, RF0 `fb852...`, SYN02-S `321fa...`, S-R `ac55...`. The previous RRP0 was documentary and explicitly held C12 physical source; this review executed the recovered imported source on a qualified host.

## 2. S36 and BP4 test replay

### S36 actual source suite

```text
cd /private/var/folders/.../syn02-s36-r2-wt/WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp \
  python3 -B -m pytest -q -p no:cacheprovider tests
```

**Own result:** `39 passed in 0.89s`. `pytest --collect-only -q tests` reports 39 tests. This is the actual S36 source suite, not a new native C9 suite.

### BP4 actual source suite

```text
cd /Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/
  SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j/candidate/vendor/bp4
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing \
  python3 -B -m pytest -q -p no:cacheprovider tests
```

**Own result:** `15 passed in 2.57s`. This is the actual BP4/C12 source suite, not proof of a native C12 or assembled actor.

## 3. Author probes — own rerun

Commands used (actual target probe files, actual S36/C12 sources):

```text
S36_RETURN=<S36 return> python3 -B probes/probe_s36_legacy.py
S36_RETURN=<S36 return> python3 -B probes/probe_legacy_bridge.py
python3 -B probes/probe_actor_authority.py
python3 -B probes/probe_outbox.py
JOIN_E_RETURN=<JOIN-E return> python3 -B probes/probe_c12_mirror.py
```

### S36 legacy

```text
PASS s36_legacy: actual targetless receipt committed; old table count=7
PASS s36_legacy: old receipt hash=1cec8633d861959c7d4b744c6770f9720110e977f021f460a1608e1aebbf4ee9
PASS s36_legacy: same-schema actor table changes readset domain;
  future legacy before=9cfbe2777fa2788e0912d9cf87fd47bbf1b17b6f99f7f0a4b97e68a6c65b8d68
PASS s36_legacy: mutable actor row is non-additive under old all-table row-set invariant
PASS s36_legacy: old receipt/RESPONSE rows remain byte-identical
OBSERVED old target_branch=NO_CHANGE reason=NO_PROPOSAL target_id=''
```

This confirms the seven-table domain and the incompatibility of adding mutable actor tables to the same legacy DB. It does not prove an actor implementation.

### Legacy bridge

```text
PASS bridge: actual S36 receipt ... remains targetless NO_PROPOSAL
PASS bridge: actor authority records HELD_MISSING_RULE; no actor version beyond genesis
PASS bridge: legacy DB table domain remains 7 tables; no actor target/false true-nochange
OBSERVED bridge: actor_head=(0, '14b580db...', '44136fa3...', 1, 0)
  outbox=PENDING decision=HELD_MISSING_RULE
```

### Actor authority

```text
PASS actor_authority: atomic final/held/requalification, CAS, idempotency,
  target scope, append-only and rollback
PASS actor_head=version=2 receipt_seq=3 finalized_seq=3
```

### Outbox

```text
PASS outbox: C4 C9 durable actor receipt, no C12 mirror, state=SYNC_HELD, outbox=PENDING
PASS outbox: C5 C12 mirror before ACK, outbox PROJECTED->ACKED, retry creates no new actor version
PASS outbox: duplicate mirror identity refused; existing projection retained
OBSERVED outbox: receipt=b6e5b2e191f300270ce45f966f8a639c6f80e30a4904d19fe69d5adc78a64295
  version=e17b0847ddb6cdc74ef434cdd549f432471ab3b42a332075d857f0b6450e4a8c state=ACKED
```

### C12 mirror probe

```text
PASS c12: actual QualifiedC12Store imported from r26e.c12_integrity; base C12Store from bp4.store
PASS c12: actual root/fork/cold row verify; root='' alt_ok_root=034033b...
PASS c12: sidecar root/watermark/alt_ok mirror verified; duplicate rejected
OBSERVED c12: exact tables=['branch','checkpoint','episode','meta','perception','world_event']
OBSERVED c12: PRAGMA journal_mode='delete' synchronous=2 foreign_keys=1
FAIL c12_physical: fork_clock=10 dropped clock-11 perception
  (parent=2 alt_bad=1); actual C12 verify still ok
PASS c12: sidecar fails closed with C12_FORK_PERCEPTION_LOSS:alt_bad
PASS c12: actual C12 verify does not validate branch root;
  sidecar does (C12_ROOT_MISMATCH:alt_ok)
PASS c12: missing fork mirror is fail-closed (C12_BRANCH_NOT_MIRRORED:alt_ok)
```

The FAIL is actual source behavior; it is not a failure of the proposed C9 SQL. The sidecar’s original count-loss case is detected, but §5 below shows it is not a general fail-closed guard.

## 4. Independent C12 fork probe

Reviewer-owned script (actual imported `QualifiedC12Store`, actual `bp4.world.make_event`; no author C12 code altered):

```python
from r26e.c12_integrity import QualifiedC12Store
from bp4.world import make_event
c = QualifiedC12Store(path)
c.create_root("root", clock=10, actor_ids=["A","B"], state={...})
e1 = make_event(clock=10, kind="NO_CHANGE", actor_id="A", ...)
c.append_world_event("root", e1); c.record_perception("root", actor_id="A", event_id=e1["event_id"], clock=10, channel="co_present")
e2 = make_event(clock=10, kind="NO_CHANGE", actor_id="A", ...)
c.append_world_event("root", e2); c.record_perception("root", actor_id="A", event_id=e2["event_id"], clock=11, channel="co_present")
bad = c.fork("root", "alt_bad")
# then add a different clock-10 event/perception to alt_bad; build author sidecar rows
```

Own output:

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
child_same_count 2 [False, False]
child_verify_same_count True
same_count_sidecar_ok True []
sync_held_watermark_sidecar_ok True []
wrong_base_root_sidecar_ok True []
```

The same-count child has a different clock-10 perception and no clock-11 parent perception; count remains 2. `mirror_verify` returned `ok`. The `SYNC_HELD` watermark and a wrong `base_c12_root_hash` also returned `ok`. This falsifies the claim that the proposed sidecar is a general fail-closed guard.

## 5. C9 helper adversarial audit

Reviewer-owned command/audit of the author helper:

```text
publish(... idempotency_key='same-key', request_digest='same-digest',
        decision_kind='HELD_MISSING_RULE', ...)
publish(... exact same arguments ...)
```

Own output:

```text
first_receipt 67494d1775d6e2508d4011ecde2dbfeb3e78c040d2ce4a42952148bf0c1d8f78
same_key_same_digest_error IntegrityError UNIQUE constraint failed: event_attempt.idempotency_key
held_status_axes ('HELD_MISSING_RULE', 'COMMITTED_CHANGE', 'HELD')
```

The contract says same key/same digest should return the exact existing receipt without rerunning Rule T. The helper relies on a raw unique constraint and does not implement that path. It also permits a held decision with a committed Rule T status axis because `schema_actor.sql:216-247` checks only final decision kinds.

## 6. Source-line evidence

| Finding | Exact source |
|---|---|
| C12 `_last_clock` excludes perception | `bp4/store.py:135-143` |
| C12 `record_perception` allows clock 11 after clock 10 | `store.py:195-214` |
| C12 `fork` uses non-perception clock and copies only `clock<=fork_clock` | `store.py:323-351` |
| C12 fork root hash excludes perception | `store.py:353-360` |
| C12 branch table mutable; only four history tables have append-only triggers | `store.py:83-84`, `:361-364` |
| `QualifiedC12Store.verify` excludes branch root/count/ancestry | `r26e/c12_integrity.py:31-64` |
| Direct C12 fork has no transaction; lineage wrapper is optional | `bp4/store.py:323-367`; `joined/lineage.py:129-152` |
| Sidecar count-only check | `probe_c12_mirror.py:63-64` |
| Sidecar watermark state selected but not enforced | `probe_c12_mirror.py:66-71` |
| Sidecar base root/perception identity not checked | `probe_c12_mirror.py:84-90`; `schema_mirror.sql:27-30` |
| Sidecar rejects only FORK_HELD, not MIRROR_HELD | `probe_c12_mirror.py:61-62` |
| S36 all-schema/all-table readset | `S36/candidate/transaction.py:115-126` |
| S36 before-snapshot before `BEGIN IMMEDIATE` | `transaction.py:288-292` |
| S36 schema/additive checks | `transaction.py:362-370` |
| S36 targetless `NO_PROPOSAL` | `S36/candidate/target_rules.py:311-313` |
| C9 helper lacks pre-insert idempotent replay | `probe_actor_authority.py:95-203` |
| C9 schema does not constrain non-final status axes | `schema_actor.sql:153-247` |

## 7. Evidence-grade ledger

| Claim | Worker | Own RRP0-R2 | Disposition |
|---|---|---|---|
| S36 actual tests 39 | reported | **39 passed** | confirmed |
| BP4 actual tests 15 | reported | **15 passed** | confirmed |
| S36 seven-table/readset incompatibility | reported | reproduced | `ACCEPT_SCOPED` for Option A |
| Actual C12 clock-10 fork drops clock-11 perception | reported | reproduced | **RED** |
| Actual C12 verify returns ok after loss/root tamper | reported | reproduced | **RED verifier gap** |
| Sidecar detects original count loss | reported | reproduced | confirmed narrowly |
| Sidecar is generally fail-closed | not claimed as full proof | **falsified**: same-count, SYNC_HELD, wrong base return ok | **REVISE_PRECISE / not a guard** |
| C9 idempotent positive replay | reported as tested | **falsified** by same-key/same-digest raw unique error | **REVISE_PRECISE** |
| C9 held status axes | not examined | contradictory `HELD_MISSING_RULE` + `COMMITTED_CHANGE` + `HELD` accepted | **REVISE_PRECISE** |
| C9 actor implementation | explicitly sourcefree probe | no live C9 writer | `NOT_IMPLEMENTED / owner freeze held` |
| Full S37 targetless/cold, C8 native, C11/A5, real B | NOT_RUN | NOT_RUN | **HOLD** |

## 8. No native/paid claims

No paid provider, model, raw survey, native C8/C9/C11/C12/A5, real B/world actor, production DB, source edit, force push or reviewer self-adoption was used. The 39+15 tests and sourcefree probes do not prove a person, Rule A/T, SCI05 admission, memory, care, or a clean native fork.

**Reviewer token:** `RRP0_R2__C12_FORK_RED_REPRODUCED__SIDECAR_FALSE_CLEAN__C9_OPTION_A_ACCEPT_SCOPED_DIRECTION__OWNER_FREEZE_HELD__NO_NATIVE_GRANT`.
