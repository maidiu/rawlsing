# Resource and economy findings

**Measured on:** macOS 13.7.8 x86_64, CPython 3.11.3, pytest 9.1.1, local SSD. These are sourcefree probe measurements, not production forecasts. Bytes are file sizes or canonical JSON lengths. Wall times are single-run observations and are not a benchmark gate.

## 1. B1 three-event batch

| Measure | Positive | Journal-only control |
|---|---:|---:|
| Batch wall time | 0.050829 s | 0.041056 s |
| Owner SQLite file | 94,208 B | 86,016 B |
| Engine journal SQLite | 98,304 B | 94,208 B |
| State JSON | 15,220 B | 8,501 B |
| Records JSON | 23,239 B | 21,746 B |
| History JSON | 23,361 B | 21,867 B |
| Mediator records | 1 | 0 |
| Responses | 3 | 3 |
| Transitions | 1 | 0 |
| Occurrence rows | 3 | 3 |
| Joint receipt rows | 3 | 3 |
| Adapter operation rows | 3 | 3 |
| Cold history read | 0.005953 s | 0.004826 s |
| Model calls | 0 | 0 |
| Provider calls | 0 | 0 |

The positive/control difference is almost entirely the mediator/transition and the larger state/records/history JSON. The journal itself is ~96 KB for a 3-event batch; much of that is SQLite page allocation, not logical payload.

## 2. B1 scaling (direct owner, repeated offered events)

The scaling probe keeps one mediator and appends one response per event. It measures the cost of B1's full checkpoint rewrite and its growing `responses` scan, not a new mediator per event.

| Events | Owner DB | State JSON | Responses | Mediators | Transitions | Total wall | Per event |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 94,208 B | 15,334 B | 3 | 1 | 1 | 0.029214 s | 9.738 ms |
| 10 | 217,088 B | 28,713 B | 10 | 1 | 1 | 0.121503 s | 12.150 ms |
| 30 | 548,864 B | 66,953 B | 30 | 1 | 1 | 0.507245 s | 16.908 ms |
| 60 | 1,064,960 B | 124,313 B | 60 | 1 | 1 | 1.421667 s | 23.694 ms |

Observed shape:

- State JSON grows ~2.0 KB per event after the first mediator (15.3 KB → 28.7 KB → 67.0 KB → 124.3 KB).
- Owner DB grows ~17 KB per event in this small sample (94 KB → 217 KB → 549 KB → 1,065 KB); the SQLite page overhead dominates at these sizes.
- Per-event wall time grows from 9.7 ms to 23.7 ms because `propose()` scans `responses` and the full checkpoint is rewritten on each commit.
- This is acceptable for a 3–5-event selected batch. It is **not** suitable for storing thousands of hidden microevents in one checkpoint.

## 3. What these numbers mean for sparse-event P3

The user-settled design uses 3–5 selected events per batch, not a full lifetime of microevents. B1's 3-event footprint (94 KB owner DB, 98 KB journal, 15 KB state, ~51 ms batch) is inexpensive. The risk is architectural, not raw size:

- B1 rewrites the whole checkpoint on every event. A growing `responses`/`transitions` history makes every later commit more expensive.
- B1's mediator is a single JSON record inside the checkpoint. A P3 store with many selected records should use normalized rows and targeted reads, not a full-state rewrite per event.
- A 60-event B1 run already shows ~24 ms/event and 1.06 MB owner DB for only one mediator. A 1,000-event hidden simulation would be both slow and large, and is not required by the product purpose.
- The sparse-event strategy should store **compact causal records with provenance** and retrieve only the records relevant to the current event, not a latent autobiography of thousands of memories.

## 4. Components not measured here

| Component | Observed/known | Unmeasured fields |
|---|---|---|
| #704 `BatchEngine`/`P2Owner` | inherited author suite 71/71 in 279.35 s; journal/owner SQLite per event | actual per-event bytes/ms on this host; P2 full suite NOT_RUN |
| B3A | whole-DB staging via SQLite backup; 9-episode author loop; 71/63/42/33 author tests | actual staging time/bytes, per-episode DB growth, readset cost |
| HQ300 | in-memory `ChainEventLedger`; author reports 0.5 ms chain | durable bytes (none), later retrieval cost, model calls (none in candidate) |
| M01 | in-memory `FixtureOwnerState`; 36-arm factorial; 413 tests | durable bytes (none), per-arm memory, cold replay |
| BP2P4J | full BP2/BP4 product with C12 SQLite; 98 author tests; 7+3 severances | per-run artifact bytes, C12 growth, staging/replay time |
| V3 local copy | 0–100 state, yearly pressure-flow; local archive not exact | exact protected archive bytes/closure; old tests NOT_RUN |
| Production P2 with a provider | #704 provider calls only between batches | per-call tokens/latency/cash: UNKNOWN |

## 5. Per-event and per-batch cost model (from measured B1 only)

For the B1 probe, each event writes:

- 1 occurrence row (`occurrence`);
- 1 joint receipt row (`joint_receipt`);
- 1 adapter operation row (`b1_operations`);
- 1 response record inside the checkpoint;
- on a CREATE: 1 transition and 1 mediator record inside the checkpoint.

The checkpoint is rewritten in full on every commit. Logical state JSON is ~2 KB/event in this fixture; physical DB growth is ~17 KB/event at small N. The engine journal is ~32 KB per event in the 3-event batch (98 KB total), again dominated by SQLite pages.

A P3 implementation should target:

- **per-actor persistent bytes:** a small record set (mediators, tensions, practices, selected memories) with normalized rows and indexes; no full checkpoint rewrite per event;
- **per-event new state records:** at most the selected effect + receipt + provenance; no generic full-person delta;
- **per-batch context volume:** the 3–5 event documents + accessible history; no full lifetime transcript;
- **repeated history reads:** index by `(root, branch, actor, kind, target_refs, effective_from)` and read only the active/relevant records;
- **model invocations:** one provider call per batch half, never one per event; the B1 probe itself has zero;
- **cold replay:** store operation receipts and records; replay reads only the batch's records and the owner snapshot.

## 6. Recommendations

1. **Reuse B1's transaction shape, not its full-checkpoint storage.** The reservation/HOLD/result pattern is portable; the JSON rewrite is not the right P3 storage.
2. **Keep the 3–5-event batch.** Do not simulate thousands of hidden microevents to make one selected event meaningful. The user-directed compression explicitly rejects that economy.
3. **Store compact causal state.** A mediator/tension/practice/memory record with target refs, rule/source hashes, causal parents, effective time and receipt is enough for later retrieval.
4. **Retrieve selectively.** The later consumer should query the active records for the current actor/project/relation/context, not load an autobiography.
5. **Measure the P2 slice after implementation.** This probe measures B1; P2's S47 SQLite and journal may have different constants. Add the same counters (DB bytes, state bytes, records bytes, cold time, model calls) to the P2 extension tests.
6. **Do not use B1's 60-event scaling as a P3 requirement.** It is a warning about full-state rewrite, not a target workload.

## 7. Reproduction

```bash
cd WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe
python3 -B -m pytest -q -p no:cacheprovider test_b1_owner_adapter.py
python3 -B run_probe.py
```

The probe writes `probe/receipts/PROBE_RECEIPT.json` and `probe/receipts/junit.xml`. The scaling section is regenerated by the same command. Runtime DBs are created under a temporary directory and removed; only the receipt and JUnit remain.
