# Cold C12, fork and actor-limited M6

## Persisted populated episode

`R29PProduct.observe_verified` reads through `QualifiedC12Store`. A baseline run with one SAY episode and one independent B offscreen life yields:

```text
episode=4  world_event=4  checkpoint=3  perception=6  ok=true
```

The episode rows include the actor SAY and the actor WAIT. The B offscreen life produces B `OFFSCREEN` episodes and the A2 `OFFSCREEN_REPAIR` observable. The pinned upstream `C12Store.verify` returns false on the same populated database because of its self-hash defect; the R26E qualified verifier returns true.

## Cold reopen

`evidence/r29p_cold.json` is produced by `tools/run_evidence.py` in a **new subprocess**:

- `R29PProduct.reopen(root)` opens the same `product/c12.sqlite`;
- `observe_verified` returns `OK` and the same A0 claims/tools;
- `c12_verify` returns `ok=true` with the same counts;
- no producer is run and no second root is created.

The test `test_baseline_reaches_persisted_cold_c12_and_a0_a2` repeats this through `subprocess.run` and asserts the same persisted DB.

## Fork

The fork run writes a shared SAY and WAIT, forks `alt`, then writes a post-fork SAY only on `alt`.

- `shared_before.equal=true` and `shared_after.equal=true` for the pre-fork rows;
- root has 4 episodes, alt has 5;
- root and alt both verify;
- cold reopen of `root` and `alt` returns different episode lists with the shared prefix preserved.

The branch metadata update is not append-only history; the episode/world/checkpoint/perception rows remain fixed.

## Actor-limited M6

Before ATTEND, A sees `ARRIVAL` and its own `SPEECH`, but not B's `OFFSCREEN_REPAIR`. After TRAVEL to market and ATTEND, A sees:

```text
OFFSCREEN_REPAIR  READY_FULL_CLAIM_SCOPE  PERMIT_FIRST_PERSON_KNOWLEDGE
```

The cold reopen of the post-ATTEND root preserves that permission. B's private fields are not exposed by `other()`; the product only exposes B's public position, role, completed units and public work events.

## Residual custody limits

- Raw SQLite access can drop the append-only trigger and delete rows; the R26E external witness detects deletion only against a separately held checkpoint.
- A same-user attacker who rewrites both the DB and the witness/key defeats the witness.
- The C12 store is not a production KMS, not power-loss durable and not an exactly-once boundary.
- C8 D1/D2/D3, Pyat N11/N12, C11 and native C12 remain held.

These are typed `TRUST_CUSTODY_HOLD` residuals, not native claims.
