# R2-06 BENCHMARK PLAN — WHOLE-MACHINE BOUNDARY COURT

Status: `DESIGN_ONLY__REPLACES_RELATIVE_SPEEDUP_SELECTION`

## 1. Purpose

This plan attacks benchmark criteria that reward locally fast but globally worse designs.

A benchmark is not a tournament. It answers one question:

> Does the least-complex candidate satisfy every frozen whole-machine boundary, and if not, what exact boundary remains failed?

Only a failed boundary authorizes a more complex candidate.

## 2. Rejected comparison rule

Do **not** adopt the Round-1 R04 suggested rule:

- `>=2x` on one blocking metric; or
- approximately `>=35%` improvement on two metrics with no hostile regression above approximately `25%`.

R04 explicitly marked that rule nonbinding. R2-06 rejects it because relative percentages can select a more complex design when both candidates already satisfy all requirements, can hide build/audit/replay/integrity costs outside the chosen metrics, and invite workload/metric tuning.

A 2x win on an already acceptable query is architecturally worth zero.

## 3. Freeze before measurement

Before opening any candidate performance result, HQ freezes:

- exact candidate code/config identity;
- exact source/fixture corpus;
- source/decoder/C11/I03/I05/I04/whole-machine authorities;
- R02 FD/geometry/type certificates available to the candidate;
- semantic/integrity/corruption courts;
- candidate tuning-workload disclosure hashes;
- R03 blind-frontier nonce protocol;
- hardware/runtime/dependency versions;
- resource hard/preferred boundaries;
- absolute practical-runtime boundaries for any phase whose latency can justify architecture escalation;
- allowed worker/batch/row-group tuning envelope;
- cache state for the dispositive organization run: **absent**.

If no absolute practical-runtime boundary has been frozen for a metric, that metric can diagnose/tune but cannot justify escalating from a candidate that passes all existing boundaries.

## 4. Frozen resource boundaries already available

Use the accepted envelope unless HQ supersedes it with higher authority before the court:

| Boundary | Preferred | Hard |
|---|---:|---:|
| Peak RSS | `< 2 GiB` | `<= 4 GiB` |
| WVS carrier | `<= 2 GiB` | `<= 4 GiB` |
| LiTS carrier | `<= 1.5 GiB` | `<= 3 GiB` |
| CLOSED_35 carrier | `<= 20 GiB` | `<= 32 GiB` |

Round-1 R06 recorded accepted R4 projection evidence well below these storage/RSS envelopes, but that evidence is burden-of-proof context only, not full-source closure for a future candidate.

## 5. Correctness precedes resources

A candidate receives no performance interpretation until it passes:

- source-native hostile reconstruction;
- full C11 M01-M18 projection/ref/hash equivalence;
- I03 positive and typed-negative suite;
- I05 declared + blind frontier complete coverage;
- I04 admission/precedence parity;
- selected source replay;
- cache deletion correctness;
- corruption/fail-closed publication;
- determinism/re-layout invariance;
- one-copy/no-source-family-semantic-branch law.

One mismatch rejects the candidate for the affected court. There is no semantic pass percentage.

## 6. Dispositive organization runs are cacheless

For organization selection:

```text
persistent caches/indexes = deleted
worker_count = 1 unless the candidate under court is specifically C15
warm materialization cache = absent
precomputed pair/k-way query tables = absent
```

This proves that the canonical organization itself preserves open-world feasibility.

Optional caches can later be evaluated for a separately frozen serving-latency objective, after the organization is already sufficient.

## 7. Candidate order

Court in this order and stop at first sufficient candidate:

1. `LONG_SHARDED`
2. `QUESTION_BLOCKED_LONG` only if LONG fails a projection/read-amplification boundary
3. `HYBRID_DENSE_PLUS_EXPLICIT` only if lower-risk remedies fail and the remaining boundary matches dense-incidence mechanism with exact geometry/grain certificates

Do not benchmark all candidates by default merely to rank them.

## 8. Whole-workflow measurement table

Every candidate emits the same fields:

```text
candidate_id
organization
candidate_commit
physical_config_hash
source_set_hash
build_seconds
build_peak_rss_bytes
seal_seconds
seal_peak_rss_bytes
reopen_seconds
reopen_peak_rss_bytes
full_audit_seconds
full_audit_peak_rss_bytes
i03_suite_seconds
i03_peak_rss_bytes
i05_blind_suite_seconds
i05_peak_rss_bytes
i04_seconds
i04_peak_rss_bytes
replay_seconds
replay_peak_rss_bytes
integrity_court_seconds
integrity_peak_rss_bytes
canonical_steady_state_bytes
atomic_staging_peak_bytes
scratch_execution_peak_bytes
nonauthoritative_cache_bytes
post_success_retained_bytes
authoritative_member_count
physical_profile_count
source_family_semantic_branch_count
persistent_cache_type_count
reconstruction_dependency_count_sample_event
vector_invariant_implementation_count
semantic_mismatch_count
source_reconstruction_mismatch_count
i03_mismatch_count
i05_coverage_mismatch_count
i04_mismatch_count
replay_mismatch_count
integrity_failopen_count
determinism_mismatch_count
```

Report phase distributions/individual case timings where one aggregate suite number would conceal a pathological required workload.

## 9. Required I03 strata

At minimum:

- scalar positive;
- exact negative/no-match;
- low-cardinality predicate;
- uncached high-cardinality/string predicate;
- AND/OR/NOT;
- pair joint;
- 5-way WVS-style joint or equivalent hostile fixture;
- conditioned k-way joint;
- routing/NOT_ASKED/INAPPLICABLE/unresolved;
- typed missing/DK/refusal/source-physical counterexample;
- weighted/design/estimand cases including missing/competing weights;
- coordinate/time case;
- repeated/ranked/ordered target;
- component/MR target;
- multi-universe/source-relation case;
- valid-empty/observed-zero/zero-support/zero-overlap/noncomparable/integrity distinctions.

QBL and HYBRID must include questions spread across multiple blocks/forms.

## 10. Required blind I05 strata

After candidate/tuning freeze, compile at least:

- uncached high-cardinality/string atom;
- pair cotravel;
- 3+ way configuration/conjunction;
- NOT/routing-sensitive atom;
- conditional reversal/Simpson grid;
- recursive subgroup fork;
- branch-conditioned distribution;
- branch-conditioned cotravel;
- co-signature/cloud-like diagnostic path with diagnostics unable to prune factual candidates;
- multi-block/mixed dense+explicit questions where applicable;
- at least one non-WVS/LiTS hostile source-family fixture.

Require exact `candidate_count == covered_candidate_count`.

## 11. LONG-specific diagnostic measurements

Record:

- bytes scanned per I03/I05 case;
- shard fanout;
- decompressed bytes versus relevant target bytes where available;
- exact-event reconstruction cost;
- external sort/merge cost;
- whether whole-member scan or root inventory establishes negative closure.

Do not classify high scan bytes as failure unless a frozen runtime/I/O boundary is missed.

## 12. QBL-specific diagnostic measurements

In addition to common fields:

- question block count/width distribution;
- members opened per query;
- multi-block fanout;
- bytes read for single-question versus k-way cases;
- integrity/member-open overhead;
- block-width relayout determinism;
- whether any query needs a persistent respondent/question index to be feasible.

QBL advances only if it cures LONG's named projection/read-amplification failure and no required multi-block/open-world boundary regresses into failure.

## 13. HYBRID-specific diagnostic measurements

In addition:

- certified dense block count;
- explicit block/event count;
- fraction of logical events in explicit escape;
- number of geometry/grain certificate families;
- dense/explicit reconstruction joins;
- vector validated-fallback incidence;
- total dense + explicit + dimensions/metadata bytes;
- mixed dense/explicit blind-I05 timings;
- profile relayout determinism;
- source-family semantic branch count (must be zero).

Do not report dense payload size without explicit/topology/metadata/root cost.

## 14. Integrity baseline versus Merkle challenger

Flat baseline:

- root manifest;
- exact member inventory;
- whole-member hashes;
- full audit;
- atomic publish/reopen/CAS.

Only if a pre-frozen verification/reopen/fetch/repair boundary fails may a chunk/Merkle challenger run.

Then measure:

- chunk metadata bytes;
- hash operations;
- bytes verified per query;
- query-closure cardinality;
- TOCTOU-safe consume-after-verify path;
- negative/aggregate closure;
- full audit unchanged.

If safe closure typically expands to full member/release or does not cross the failed boundary, delete Merkle.

## 15. Parallelism challenger

Only after serial bounded candidate is semantically/integrity sound and misses a frozen build wall-time boundary.

Run worker counts `1, 2, N` under fixed total memory gates. Record queues/compression buffers/backend memory. Require identical logical receipts and no preferred/hard RSS regression into failure.

If serial already passes its frozen wall-time boundary, parallel speedup earns no architecture credit.

## 16. Optional cache court after organization selection

If a separate serving-latency objective exists:

1. run canonical no-cache baseline;
2. build exactly one proposed cache type;
3. warm run;
4. delete cache entirely;
5. rebuild under different permitted grouping;
6. inject stale-root cache;
7. corrupt cache;
8. require identical semantics/coverage in all states.

Cache bytes/build time/invalidation/recovery states are reported separately.

A cache can be kept if it meets the serving objective with acceptable maintenance cost. It never retroactively makes an otherwise insufficient canonical organization semantically acceptable.

## 17. Complexity is a gate, not a weighted score

Record, do not numerically blend:

- canonical representation count (target `1`);
- persistent cache type count (baseline `0`);
- physical schema/profile count;
- source-family semantic branch count (required `0`);
- independent invariant implementations;
- reconstruction dependencies for one representative event;
- invalidation dependencies per cache;
- publication/recovery states;
- migration/rollback states;
- number of distinct places an event can be materially represented.

A candidate that passes all performance boundaries but contains removable complexity fails the final deletion test until that mechanism is removed.

## 18. Decision rule

For each candidate:

```text
if semantic/oracle/integrity/replay/open-world failure:
    REJECT
elif unbounded or hard resource boundary failure:
    INSUFFICIENT
elif pre-frozen required practical-runtime boundary failure:
    INSUFFICIENT
else:
    SUFFICIENT
```

Selection:

```text
first SUFFICIENT candidate in authorized escalation order
+ final mechanism deletion pass
= winner
```

There is no bonus for being farther under a passing threshold.

## 19. Stop rule

Once a candidate is `SUFFICIENT`:

- freeze it for synthesis;
- do not build a more complex organization merely for comparison;
- remove optional mechanisms one at a time and rerun the relevant bounded court;
- keep only mechanisms whose removal causes an actual frozen boundary to fail;
- return the minimal remaining contract to HQ.

This is the benchmark rule that saves the project from both semantic destruction and architecture-by-leaderboard.
