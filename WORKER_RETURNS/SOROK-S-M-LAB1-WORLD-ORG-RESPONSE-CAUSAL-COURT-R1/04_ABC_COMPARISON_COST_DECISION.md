# 04 — A/B/C comparison, measured cost, and decision-law disposition

Source: `outputs/primary_results.json` (`comparison`, `cost`), `outputs/liveness_controls.json`.

## 1. Correctness comparison (frozen predicates; 12 paired seeds per K per arm)

| K | A | B | C | B−A | C−A |
|---|---|---|---|---|---|
| K1 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| K2 | 1.00 | 0.00 | 0.00 | **−1.00** | **−1.00** |
| K3 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| K4 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| K5 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |
| K6 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 |

Statistical note (frozen): the engine is deterministic with tie-break-only seeds; all 12 seeds produced identical outcomes per cell → paired differences are degenerate point intervals. **No equivalence claim is licensed** (n=12, no prospective power): the ±5pp equivalence margin yields `INDETERMINATE`, not `EQUIVALENT`. No B or C arm reaches the +10pp screening threshold anywhere; B/C are −100pp on K2.

## 2. Mechanism liveness (prereg-declared, executed post-battery, scoring untouched)

- B goal-match mechanism **live**: on synthetic equal-support ties B deterministically prefers the goal-matching route where A rng-ties (`outputs/liveness_controls.json`).
- C relation mechanism **live**: typed index returns the same semantic content as A's reconstruction with zero formation-event scans.
- K2 B/C failure is therefore attributable to the preregistered B scoring term (+goal-match → tie → goal-preferred tie-break), not dead machinery. The diagnosis table records exact candidate scores per arm.

## 3. Measured cost (192 trials per arm; wall-clock of the full battery: 1.75 s)

| Metric | A | B | C | B vs A | C vs A |
|---|---|---|---|---|---|
| durable state bytes / trial | 152 | 152 | 152 | 0% | 0% |
| event-local / index records | none persisted | conation block per receipt | conation + edge per receipt | + | + |
| receipt bytes (mean) | 6 600 | 7 573 | 7 583 | +14.7% | +14.9% |
| retrieval refs (mean) | 3.75 | 3.75 | 3.75 | 0% | 0% |
| retrieval tokens (mean) | 359.8 | 480.1 | 479.4 | **+33.5%** | **+33.3%** |
| relation formation-event scans | 1.88 | 1.88 | **0** | 0% | −100% |
| model calls / tokens | 0 / HOLD | 0 / HOLD | 0 / HOLD | — | — |
| latency p50 / p95 (ms) | 1 / 1 | 1 / 1 | 1 / 1 | 0% | 0% |
| branches (mean candidates) | 2.44 | 2.44 | 2.44 | 0% | 0% |
| cold-replay failures | 0 | 0 | 0 | — | — |
| hold/failure rate | 0.0 | 0.0 | 0.0 | — | — |

Cost guard (frozen ≤25% extra tokens/latency/storage without proportionate gain): **B and C fail** on retrieval tokens (+33%) with zero correctness gain.

## 4. Decision-law disposition (frozen mapping applied to observed numbers)

| Decision-law branch | Applies? | Disposition |
|---|---|---|
| A ≈ B ≈ C → delete/demote richer state | Literally no (K2 differs); operative pattern is **A ≥ B, A ≥ C everywhere with one strict A win** | **Demote/delete richer state**; keep A as the working carrier |
| B > A and C no distinct gain → keep organization event-local | **No** — B is not > A; B is strictly worse on K2 and costlier everywhere | B's **ranking role REJECT**; B's descriptive compilation may remain event-local display only, never a causal parent |
| C improves retrieval only → cache/derived index | **Yes** (0 scans vs 1.88; identical semantics; no causal gain) | C = **DERIVED_CACHE**; require exact rebuild/replay equivalence for any cache product |
| C unique held-out causal discrimination + lifecycle/intervention value + zero violations + acceptable cost → recommend narrow authority commission | **Not met** (no unique discrimination; cost guard failed) | **No promotion**; no self-promotion; C state stays unlicensed |
| All three fail to produce defensible history-conditioned response | **No** — A produced it on all six K | kill-court branch not taken for A; taken for the richer-state hypothesis |

## 5. What would change this disposition

1. Behavioral replication under a pinned model surface where B's goal compilation or C's index improves typed contrast correctness by ≥10pp with paired interval excluding zero (LAB2 scope).
2. A C-lifecycle/intervention experiment showing a lawful effect A's ancestry cannot represent (held, not disproved).
3. A redesigned B ranking that survives K2-type topology/goal alignments (currently unproven; the frozen B term failed).

Until then: A carries the causal chain; B/C add cost, and B adds harm.
