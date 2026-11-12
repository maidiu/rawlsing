# CGA-P3-ABI — current P3 owner/root/actor/branch/clock/material ABI

**Obligation:** `CGA-P3-ABI`
**Result:** `PASS_SOURCE_CONTENT__EXACT_DECLARED_COMMIT_IDENTITY_HOLD`
**Source cut:** `2be0cf252662ad021571db6f0d38b12c205c56ae`
**Declared cut:** `1f77f2036427a410429184780ef884ec4f253ad0` (absent locally and remotely)

The four declared source blobs are exact at `2be0cf25`; the declared commit object is absent. This report therefore distinguishes the generic engine contract from the local P2/P3/P6 adapters at the source-equivalent cut. It does not claim the literal startup identity.

## 1. Exact source comparison

| Source | Blob at `2be0cf25` | SHA-256 | Declared blob |
|---|---|---|---|
| `developmental_recursion/contracts.py` | `c4ce557c...` | `9aabbc9f...` | `c4ce557c...` exact |
| `developmental_recursion/p2_owner.py` | `3160eb15...` | `fd98a757...` | `3160eb15...` exact |
| `developmental_recursion/engine.py` | `a7776927...` | `ba6caa74...` | not separately pinned; current |
| `developmental_recursion/model_cycle.py` | `231cab97...` | `af83f8f1...` | not separately pinned; current |
| `p3/p3_owner.py` | `e735ada7...` | `e735ada7...` | current candidate |
| `p3/state_store.py` | `173d4d6d...` | `173d4d6d...` | current candidate |
| `SOROK-P6-ONE-LIVING-HOUSE-R1/house.py` | `af556c14...` | `7d78d48d...` | `af556c14...` exact |
| sourcepack 09 | `c3cdc7c1...` | `64746865...` | `c3cdc7c1...` exact |

See `CGA-P3-ABI_EVIDENCE.md` for line-level symbols.

## 2. Generic contract

The engine protocol is content-addressed and story-free:

```text
StateIdentity(root, actor, branch, clock, state_hash)
EventProposal(event_id, event_time, operation, source_refs,
              participants, circumstances, interval)
RealizedEvent(operation_id, proposal_hash, before, after, status,
              objective, accessible, consequences, readset, receipt_ref)
DevelopmentOwner.snapshot / validate_proposal / realize
BatchEngine(owner, journal_path).run_batch / history / verify
RecursionCycle(engine, provider, store_path).bootstrap / advance / finish
```

`BatchEngine` binds the journal to the first `(root, actor, branch)`, requires 3–5 proposals, rejects non-forward event times before the first reservation, validates all proposals before any effect, checks every owner result's `before`/`after` identity and clock, and keeps a durable per-event reservation. `RecursionCycle` reserves the provider call, refuses provider mutation of owner state, binds the retrospective to the pending `batch_id`/`history_hash`/event order, and calls no provider between events.

## 3. P2 adapter is local, not universal

`P2Owner` is a controlled P2 workshop adapter at `TEST_ONLY_S47_OWNER_NOT_NATIVE_DEVELOPMENTAL_SCIENCE` grade. Its constraints are:

- `participants == tuple(root["actor_ids"])` and `actor = root["actor_ids"][0]` (`p2_owner.py:45-47`);
- operation `ADMIT_EVENT` only;
- interval modes `ACTUAL` and `SCHEDULED_ONLY`, span positive and not crossing the event clock;
- history refs must resolve to native event IDs/hashes in actor/branch order without duplicates;
- snapshot material is `{world, events, intervals, encounters}`; the actor is the first root actor;
- repeated operation IDs must resolve from the owner receipt or raise an ambiguous HOLD; native effects are never reissued blindly.

This fixed roster is a **P2 workshop adapter**, not the generic P3 root contract. It must not be copied into CG-B/C/D as if it were a universal multi-actor policy.

## 4. P3 owner and store

`P3Owner` composes one `P2Owner` and one `PsycheStore`. It binds the source root/actor/branch exactly to the base snapshot, freezes source/history/plans/catalog/standpoints/code pins, and uses one `PsycheStore` bound to the same single actor. The store adds:

- exact record binding to root/actor/branch, source hash, registry hash, rule version/hash and causal event hash;
- `effective_from <= as_of` query by exact `project`/`counterpart`;
- immutable head chain, rollback on any bad target, exact replay, and cold reopen refusal on wrong binding/source/registry/schema/first head;
- phases `PREPARED`, `WORLD_COMMITTED`, `PSYCH_COMMITTED`, `COMPLETE`, with pending-operation blocking and durable reservation.

The later reading edge is `P3Owner._effect`: it calls `store.query(project, counterpart, as_of)` and passes the returned records into the sourcefree rule/projection layer. The resulting `RealizedEvent.readset` includes the record hashes. This is the selected common readset.

## 5. P6 material

`house.py` establishes `world.resources["p6_house"]` with `root`, `branch`, `source`, `epoch`, `rooms`, `objects`, `presentation_conditions` and `history`. `read_house` refuses a wrong root, branch, source hash, object material or provenance. The resource is inside the P2 world and therefore contributes to the P2 `snapshot.state_hash`.

It does not provide:

- a dated `home_period` with `from_clock`/`to_clock`/`home_ref`;
- an independent second actor;
- a speech admission for a speaker other than the existing actor path.

Those are exact extension points, not reasons to replace the writer.

## 6. Verdict

`PASS_SOURCE_CONTENT` for the declared P3 owner/root/actor/branch/clock and P2 material boundaries at `2be0cf25`; `HOLD` for the literal declared startup identity; `BUILD/HOLD` for the multi-actor, dated home-period and independent-speech extensions. The existing generic engine and `P3Owner`/`PsycheStore` are sufficient for the single-actor path and are the selected base for CG-B/C/D.
