# R01 BENCHMARK / PROOF PLAN

Future implementation proof only. This does not authorize another full CLOSED_35 R4 run and requires no raw-source access now.

## 1. Acceptance order

1. frozen hostile-fixture semantic equivalence;
2. synthetic scaling/backend-memory tests;
3. external-sort/concurrency determinism;
4. exact positive/negative reconstruction;
5. crash/publication fault injection;
6. cache deletion/rebuild invariance;
7. I03/I05/I04 oracle parity;
8. only after HQ/R06 authorization, bounded real-source confirmation.

Failure at an earlier stage blocks escalation. Do not rerun failed full-source R4 for autopsy telemetry.

## 2. Oracle

Use frozen source/C11/I03/I05/I04 authority plus R03, not physical Parquet-byte equality. On bounded accepted fixtures compare exact source/release refs, family counts, exact refs/content hashes, event/topology/routing/weight/authority records, replay manifest/projection hash, M01–M18, I03 positive/negative results, authorized I05 results, I04 results, and frozen invalid-candidate dispositions.

## 3. Synthetic scale matrix

Use physical-only synthetic rows at N = `10^3, 10^4, 10^5, 10^6, 10^7` or until the memory claim is decisively established/falsified. Hold row-size distribution/configuration constant for asymptotic tests.

Exercise narrow rows, medium rows, unique high-cardinality strings, long strings near shard cap, one `Smax` oversize row, duplicate-looking IDs with distinct exact refs, intentionally repeated identical rows, one huge relation plus empty/small relations, huge shard inventories, and run counts far above merge fan-in.

Synthetic data proves resource mechanics only, never source semantics.

## 4. Writer memory proof

Measure process current/peak RSS, Python heap where available, Arrow/Parquet allocator bytes, run rows/bytes, active merge input/output batch bytes, backend dictionary/page/row-group state, queue depths, cache bytes, retained inventory descriptors, open files and temp disk.

Pass: with `Smax`, `B_rows`, `B_payload_bytes`, `F`, `W`, `Q`, `E`, and `C` fixed, peak live memory approaches a stable ceiling as N grows. A structural positive slope is failure even if small.

## 5. Backend cardinality/footer trap

Run unique-string cardinality growth with dictionary encoding enabled/capped, disabled, and any adaptive mode. Pass only a configuration whose live memory and per-shard footer/metadata remain bounded. If the library cannot prove a cap, reject that mode rather than relying on caller batching.

## 6. External sort/merge determinism

For the same logical multiset randomize producer arrival, run worker counts 1/2/4/max, inject delays, vary bounded run boundaries, and force multi-pass merge with run count > `F^2`.

Required invariants: identical canonical logical row/ref stream; identical frozen semantic projection/replay root; identical multiplicity; deterministic failure for ambiguous conflicts; unchanged source-native order/rank fields; no unbounded reorder state.

## 7. Reader/reopen memory proof

At increasing N test root verification, inventory audit, full member/hash audit, semantic/replay closure validation, sequential iteration, first/middle/last exact lookup and absent lookup.

Pass: memory plateaus. Any canonical-path whole `read_table(...).to_pylist()`, corpus tuple/list/table, unbounded member map or whole-directory filename list is automatic R01 failure.

## 8. Exact reconstruction and negatives

Across every logical family/shard position reconstruct exact object, recompute identity/hash, compare every field and authority/dependency ref, and verify occurrence/topology fields.

Negative suite: nonexistent ID, correct ID/wrong hash, correct release ID/wrong semantic hash, wrong source SHA, malformed/path-traversal selector, stale cache from another release. Negative truth requires complete verified search or independently proven exact index.

## 9. Frozen C11 validation parity

Use bounded hostile candidates for declared universe/authority/count mismatch, duplicate respondent key, cross-universe respondent/event, missing question/topology binding, duplicate/invalid event occurrence, missing routing/risk set, unauthorized canonical promotion, invalid weight/design typed absence, invalid source-universe relation/default, replay projection/authority/closure mismatch, semantic-root mismatch, and corrupt/missing physical member.

Streaming may use external sorted joins/multiple passes. It passes only with frozen-equivalent rejection while staying bounded.

## 10. Crash/publication injection

Kill or inject I/O failure during temporary run write, final shard write/hash, inventory append/fsync, root seal write/fsync, before rename, immediately after rename before parent fsync, and optional convenience-pointer update.

Fresh reader after each failure must see either no committed release or one complete sealed immutable release according to proven platform semantics. Orphan staging is noncanonical. Retry is deterministic/idempotent for identical semantic release; conflicting governed identity fails closed.

## 11. Integrity corruption

Mutate one item at a time: shard byte, footer/truncation, filename/ordinal, inventory hash/count/key bound/truncation, root relation descriptor, root schema/version, source/release selector identity, replay root, extra unreferenced file.

Required outcome follows R05-composed fail-closed law. Extra files must never silently alter logical content.

## 12. Cache proof

Run identical exact lookup and I03/I05/I04 workloads with empty, warm, randomly evicted, deleted, rebuilt, and fault-injected corrupt caches. Semantic results/failures/replay identities must be identical. Cache memory must stay under C04 ceiling.

## 13. I03 parity

Test variable selectors, minimum/maximum, allowed, excluded, multi-variable conjunctions, positive matches, zero matches, and cases whose truth depends on physical-missing versus routing/semantic-absence distinction. Compare exact results/failures to frozen I03/R03 oracle under different shard/cache settings.

## 14. I05 parity

Test pair, k-way, conditional, reversal, recursive fork/branch, co-signature/cloud-like authorized workloads plus at least one lawful combination selected only after the physical carrier is frozen. The last test proves the carrier preserved an unforeseen discovery frontier.

## 15. I04 parity

Use admitted/rejected/deferred cases whose evidence and replay bindings span shards. Compare disposition, evidence refs, authority refs and replay identity. Physical layout may not enter admission reasoning.

## 16. Backpressure/telemetry

Slow downstream stages intentionally. Queues must hit finite limits and backpressure producers; futures/reorder state remains finite; telemetry queue is bounded or lossy/nonblocking by policy; telemetry sink failure does not change canonical output; progress totals reconcile with the seal.

## 17. Temporary-disk proof

Measure peak run/merge disk amplification and inject low-disk conditions. Capacity failure must occur before commit, publish nothing partial, and report physical resource failure. Define preflight/safety margin before large real-source execution.

## 18. Compatibility decoder gate

Before any end-to-end boundedness claim, separately prove an equivalent bounded path for exact sources requiring frozen encoding compatibility: same exact SHA/config authority, variable metadata, row count/order, cell incidence, missing declarations/states/raw values, downstream C11/R03 result, and memory plateau.

R01 performs no raw probe now because checked-in evidence suffices for carrier design. Any future source probe needs explicit governing authority and exact SHA scope.

## 19. Automatic rejection

Reject without full-corpus escalation if any of these occurs: whole-relation materialization; memory growth with N under fixed bounds/Smax; backend dictionary/footer growth; concurrency changes logical digest; duplicate multiplicity changes; any source-native/C11 loss; incomplete-scan negative truth; partial release visible after crash; corruption passes; cache deletion changes semantics; any I03/I05/I04 mismatch; compatibility law weakened to get chunking.

## 20. Full-source escalation

Only HQ/R06 may authorize later CLOSED_35 confirmation after fixture/synthetic/crash/oracle gates pass. If authorized, measure the replacement directly; do not turn it into another R4 autopsy.
