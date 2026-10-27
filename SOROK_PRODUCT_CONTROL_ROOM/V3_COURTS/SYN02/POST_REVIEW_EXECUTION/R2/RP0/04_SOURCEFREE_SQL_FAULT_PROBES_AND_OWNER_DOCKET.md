# RP0-R2 / 04 — sourcefree SQL probes, test receipts and owner freeze docket

**Status:** `PROBES_EXECUTED__C9_ACTOR_CAS_OUTBOX_LEGACY_BRIDGE_PASS__C12_ACTUAL_FORK_PERCEPTION_LOSS_FAIL__C12_OWNER_REPAIR_REQUIRED__OWNER_FREEZE_HELD__NO_NATIVE_GRANT`.

**Evidence boundary:** these are fresh temp SQLite files and actual read-only source imports. No persistent C9/C12 database, source module, production service, provider, or native actor was edited or called. The only non-PASS is a real defect in the actual C12 source, not a failure of the proposed actor schema.

## 1. Commands and exact results

### Actual S36 source tests

```text
cd <extracted S36 return>
python3 -m pytest -q tests
=> 39 passed
```

This is the legacy S36 source suite, not a new actor test.

### Actual BP4/C12 source tests

```text
cd <JOIN_E_RETURN>/vendor/j/candidate/vendor/bp4
PYTHONPATH=/Users/matthewsmith/Desktop/Rawlsing python3 -m pytest -q tests
=> 15 passed
```

The C12 probe uses actual `QualifiedC12Store` and `bp4.store.C12Store`; it is not a mock schema.

### Probe commands

```text
S36_RETURN=<extracted S36> python3 probes/probe_s36_legacy.py
S36_RETURN=<extracted S36> python3 probes/probe_legacy_bridge.py
python3 probes/probe_actor_authority.py
python3 probes/probe_outbox.py
JOIN_E_RETURN=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
  python3 probes/probe_c12_mirror.py
```

### Actual output: S36 legacy domain

```text
PASS s36_legacy: actual targetless receipt committed; old table count=7
PASS s36_legacy: old receipt hash=1cec8633d861959c7d4b744c6770f9720110e977f021f460a1608e1aebbf4ee9
  before=9c5137f214d299bdb627c72ac8ff1880be98822d56082ec8ecce3eea0ba3fe62
  after=07d38064535ec54c9d96a570775dc70b4a4d285453ccdcbe739ecb8ba3df01b6
PASS s36_legacy: same-schema actor table changes readset domain;
  future legacy before=9cfbe2777fa2788e0912d9cf87fd47bbf1b17b6f99f7f0a4b97e68a6c65b8d68
PASS s36_legacy: mutable actor row is non-additive under old all-table row-set invariant
PASS s36_legacy: old receipt/RESPONSE rows remain byte-identical after the counterexample copy
OBSERVED old target_branch=NO_CHANGE reason=NO_PROPOSAL target_id=''
```

### Actual output: legacy bridge

```text
PASS bridge: actual S36 receipt 1cec8633d861959c7d4b744c6770f9720110e977f021f460a1608e1aebbf4ee9
  remains targetless NO_PROPOSAL
PASS bridge: actor authority records HELD_MISSING_RULE; no actor version beyond genesis
PASS bridge: legacy DB table domain remains 7 tables; no actor target/false true-nochange
OBSERVED bridge: actor_head=(0, '14b580db...', '44136fa3...', 1, 0)
  outbox=PENDING decision=HELD_MISSING_RULE
```

### Actual output: actor authority

```text
PASS actor_authority: atomic final/held/requalification, CAS, idempotency,
  target scope, append-only and rollback
PASS actor_head=version=2 receipt_seq=3 finalized_seq=3
```

The probe covers a final change, a HELD receipt, a later final attempt after HELD, duplicate-final rejection, same-key changed-digest rejection, stale-head rejection, two actors with the same local target ID, append-only triggers, outbox state guard and rollback no-ghost.

### Actual output: outbox

```text
PASS outbox: C4 C9 durable actor receipt, no C12 mirror, state=SYNC_HELD, outbox=PENDING
PASS outbox: C5 C12 mirror before ACK, outbox PROJECTED->ACKED, retry creates no new actor version
PASS outbox: duplicate mirror identity refused; existing projection retained
OBSERVED outbox: receipt=b6e5b2e191f300270ce45f966f8a639c6f80e30a4904d19fe69d5adc78a64295
  version=e17b0847ddb6cdc74ef434cdd549f432471ab3b42a332075d857f0b6450e4a8c
  state=ACKED
```

### Actual output: C12 physical probe (contains a real FAIL)

```text
PASS c12: actual QualifiedC12Store imported from r26e.c12_integrity;
  base C12Store from bp4.store
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

The `FAIL` is **actual C12 source behavior**, not a failed actor probe. It is a required C12 owner repair/guard. The sidecar is fail-closed, so the proposed actor product cannot claim a clean fork while this remains.

## 2. What each probe establishes

| Probe | Establishes | Does not establish |
|---|---|---|
| `probe_s36_legacy.py` | Actual S36 seven-table domain; old targetless receipt; adding actor tables changes future readset; mutable rows violate all-table additive invariant; old receipt survives | S37 cold open or native actor |
| `probe_legacy_bridge.py` | Actual S36 `NO_CHANGE/NO_PROPOSAL` maps to actor `HELD_MISSING_RULE`; no fake true-nochange; legacy DB unchanged | Rule T issuance or actor formation |
| `probe_actor_authority.py` | Proposed actor DDL: single writer/CAS/outbox/attempt semantics, held requalification, scoped targets, rollback | Live C9 implementation or owner freeze |
| `probe_outbox.py` | C4/C5 replay/ACK; no second actor version; duplicate mirror refusal | Cross-db ACID or provider behavior |
| `probe_c12_mirror.py` | Actual C12 imported DDL/class, root/fork/cold verification; sidecar anchors; C12 fork perception-loss defect | Native C12 or repaired C12 |

## 3. C0–C7 coverage

| Cut | Probe/status |
|---|---|
| C0 | `SPEC_ONLY`; no B action; no actor |
| C1 | `NOT_RUN`; C8 owner must provide actual act/journal ambiguity recovery; no automatic replay |
| C2 | `SPEC_ONLY`; world committed/actor held; no re-act |
| C3 | `PASS` actor rollback no-ghost; C8 persistence modeled as external |
| C4 | `PASS` actor commit before mirror; PENDING/SYNC_HELD; replay no Rule T |
| C5 | `PASS` mirror before ACK; idempotent ACK; no new version |
| C6 | `PASS/FAIL` actual C12 root/fork/cold; **FAIL** perception-loss fork; sidecar detects; actual C12 owner repair required |
| C7 | `PASS` same key changed digest rejected; committed receipt immutable; actual source-cut race is `NOT_RUN` |

## 4. C12 owner repair docket

**C12 physical owner / storage custodian** must choose and freeze one:

1. **Preferred**: patch actual C12 `fork` cut to include `perception` in the cut calculation, copy exact parent rows at that cut, include perception identity in `root_hash/root_counts`, make fork transactional, and verify branch ancestry. Exact source: `bp4/store.py:135–145,323–367`; `QualifiedC12Store.verify` `c12_integrity.py:31–64`.
2. **Guarded hold**: before every fork, if `max(perception.clock) > last_clock`, return `FORK_HELD`; require an owner checkpoint/cut. No clean fork until resolved.

Regardless, the sidecar must keep `base_c12_perception_count` and `C12_ROOT_MISMATCH` checks; these detect the observed failure.

## 5. Joint C9/C12 storage-owner freeze conditions

Do not call this design frozen until **all** are true:

- [ ] C9 owner approves frozen legacy DB path and separate `c9_actor.sqlite`; exact schema hash and PRAGMAs; one exclusive actor writer; legacy bridge.
- [ ] C12 owner approves actual C12 source cut, sidecar path, C12 root/watermark/branch checks, and fork repair/guard.
- [ ] C8 owner supplies actual independent world/B receipt, effective clock, source scope/as-of and C1 ambiguous-act recovery with no blind replay.
- [ ] CAN008/CAN011 original owners issue or explicitly hold scoped Rule A/T; no test-only rule is promoted.
- [ ] ADP016/017/SCI05 owner approves actor-safe memory and implicit-half2 hold; optional pointer is not proof.
- [ ] C6/C8/C9/C12 product/world owner selects irreversible partial-batch policy; `POLICY_UNDECIDED` remains a stop.
- [ ] C9/C12 owners sign exact schema/owner decision; an independent reviewer checks C0–C7 and actual source.
- [ ] Owner-reviewed F1.1 implementation authorization is separately issued; this RP0-R2 does not self-approve it.

## 6. Finite repair and owner handoff

| Priority | Finding → exact action | Owner | First consumer |
|---|---|---|---|
| **P0** | C12 fork drops perception-only rows; repair/guard and add branch/count/root verification. | C12 storage owner + independent source reviewer | C12 open/fork and actor-aware product |
| **P0** | Freeze Option A legacy/actor split; do not add mutable actor tables to the old all-table readset DB. | C9 storage owner | `C9ActorPublisher` |
| **P0** | Freeze C9 actor schema, CAS/head/receipt/outbox, target scope and idempotency. | C9 storage owner | C9 actor reader/C12 outbox |
| **P1** | C8 source custody/C1 recovery; no BP3 process gate as native proof. | C8/ADP019/world owner | C9 event ingress |
| **P1** | Rule A/T, SCI05, actor-safe memory, batch policy. | CAN/ADP/SCI05/product owners | future E2/N+1 |
| **P1** | Independent review of probes, schema, owner freeze; then F1.1. | HQ + independent reviewer | implementation only if explicitly authorized |
| **P2** | Legacy V3 migration/quarantine and old S36/S37 preservation. | V3/C9 source owner | future actor view |

## 7. Not run / no native

`NOT_RUN`: full S37 targetless/cold suite, current C8 native custody, actual C9/C12 assembled runtime, C12 owner repair, C11/Pyat, A0–A5, provider/model calls, raw surveys, native person.

**No source edit. No production DB. No storage-owner freeze. No science. No native grant.**
