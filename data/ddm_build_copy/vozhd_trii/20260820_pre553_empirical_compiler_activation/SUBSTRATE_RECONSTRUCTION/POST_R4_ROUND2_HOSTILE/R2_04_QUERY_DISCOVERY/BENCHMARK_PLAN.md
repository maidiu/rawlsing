# R2-04 BENCHMARK PLAN — OPEN-WORLD QUERY / DISCOVERY PATHOLOGY COURT

Status: `PROPOSED__NON_DISPOSITIVE__AFTER_SEMANTIC_PASS_ONLY`

## 1. Purpose

This plan measures whether a semantically exact P0 physical organization remains practically usable for the workloads most likely to punish question blocking, vector late materialization, and cache-free open-world execution.

It cannot rescue a semantic failure. Compression alone is not a win.

## 2. Mandatory comparators

Run the same exact releases/authorities/workloads under:

A. `LONG_SHARDED_NO_CACHE` — simplest admitted canonical reference organization;

B. `QUESTION_BLOCKED_LONG_NO_CACHE` — if proposed;

C. `HYBRID_DENSE_PLUS_EXPLICIT_NO_CACHE` — if proposed;

D. warm-cache variants only after the corresponding no-cache candidate passes.

No candidate may require a persistent second canonical database.

## 3. Freeze before measurement

Freeze:

- candidate commit/configuration;
- source/release identities;
- authority snapshot set;
- hardware/runtime/dependency versions;
- physical profile/block width/row group;
- tuning workload disclosure;
- blind-frontier nonce and selected exact candidate hashes after tuning disclosure freeze;
- cache state.

## 4. Required I03 workloads

Measure each in no-cache mode first:

1. scalar target + no condition;
2. restrictive low-cardinality predicate;
3. uncached high-cardinality/string predicate;
4. 3+ leaf AND across blocks;
5. OR with one broad and one narrow child;
6. nested NOT over routed risk set;
7. pair target joint;
8. five-way target joint;
9. k-way target + multi-leaf condition;
10. repeated/ranked/componentized target;
11. routing hostile negative;
12. exact governed weighted query;
13. weight failure/unauthorized case;
14. source-indexed multi-universe;
15. authorized composite positive;
16. composite missing-relation/noncomparability negative;
17. exact zero-support / observed-zero / valid-empty cases.

## 5. Required I05 workloads

- pair cotravel frontier;
- k >= 3 configuration frontier;
- conditional reversal/Simpson grid;
- recursive subgroup frontier with at least two levels where authority permits;
- branch-conditioned distribution;
- branch-conditioned cotravel;
- co-signature/joint facts plus diagnostic computation;
- post-freeze blind frontier spanning multiple physical blocks and at least one uncached string/high-cardinality atom.

Candidate count and covered count are semantic gates, not performance metrics.

## 6. Metrics

For each exact workload record:

- wall time;
- peak RSS;
- canonical bytes read;
- member/block/row-group opens;
- number of question blocks touched;
- repeated scans of the same block;
- ephemeral selector peak bytes;
- target materialization bytes;
- exact event rows/values gathered;
- sort/join/hash-table peak bytes;
- spill/scratch bytes and count;
- weight/routing relation bytes read;
- cache hits/misses where caches exist;
- semantic output hash/ref parity.

For I05 additionally record:

- candidate count;
- covered count;
- total exact I03 role executions;
- unique primitive leaves;
- repeated leaf scans;
- block fan-out distribution;
- candidate evaluation order;
- all receipt/fact hashes.

## 7. Join-pathology diagnostics

Question-block/hybrid designs must report:

`block_fanout = number of authoritative physical blocks required by one exact query/candidate`

`scan_amplification = canonical bytes read / canonical bytes containing directly requested primitive/target columns`

`selector_amplification = peak ephemeral selector bytes / scoped respondent count`

`repeat_scan_factor = total block scans / unique blocks touched`

These are physical metrics only. They do not authorize pruning.

## 8. Negative-state latency

Measure hostile negatives separately. A candidate that is fast on positive hits but must scan the whole release to prove exact absence may still be lawful; the measured latency determines whether the physical organization is practical.

Required cases:

- no predicate match;
- missing routing fact;
- unresolved routing;
- missing/unauthorized weight;
- no authorized source composition;
- valid empty discovery candidate;
- no-cache branch member absence.

Never replace these with cache misses for benchmark convenience.

## 9. Cache benefit accounting

After no-cache pass:

1. build declared optional accelerators and record build time/disk/RSS;
2. rerun exact workload;
3. delete all caches and rerun;
4. rebuild from canonical release and rerun;
5. inject stale cache and require rejection before timing semantic execution.

Report speedup net of cache build/maintenance cost where workload reuse is finite. Warm-cache latency alone is not sufficient adoption evidence.

## 10. Minimality decision

R2-04 proposes no new numeric acceptance threshold. HQ/R06 synthesis owns the final practical envelope.

Decision logic:

- semantic mismatch: reject immediately;
- `LONG_SHARDED_NO_CACHE` passes semantic + resource + practical gates comfortably: prefer it and reject extra query planner/profile complexity;
- question-block/hybrid cures a demonstrated blocking metric and passes all blind no-cache workloads without material joint/discovery regression: may advance;
- benefit is mostly disk compression or warm-cache microbenchmark: reject Class-C escalation;
- exact open-world fallback is so slow that required I05 workloads are practically unusable: candidate fails practical sufficiency even though semantics are representable.

## 11. No benchmark-directed semantics

Benchmark results may select physical organization. They may not:

- alter predicate grammar;
- remove a discovery family;
- reduce K/J below exact authority;
- change routing/weight/source relation law;
- authorize diagnostic pruning;
- redefine a negative state;
- make an optional accelerator canonical by convenience.
