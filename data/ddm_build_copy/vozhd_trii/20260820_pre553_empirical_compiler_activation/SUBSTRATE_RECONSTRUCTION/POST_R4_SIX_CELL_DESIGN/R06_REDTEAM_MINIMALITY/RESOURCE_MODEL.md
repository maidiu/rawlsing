# R06 Resource Model

## 0. Purpose and epistemic status

This is an adversarial resource model for synthesis, not a new benchmark return and not a claim that the R4 full-source court is already closed.

It distinguishes:

1. **accepted measured / frozen quantities** from Authorities 49/50;
2. **simple arithmetic headroom indicators** derived from those quantities;
3. **directional candidate effects** where no accepted full-source measurement exists;
4. **proof cost / maintenance cost**, which must be counted as real resource consumption rather than treated as free.

No raw-source probe or new production benchmark was run by R06.

---

## 1. Governing scale and resource envelope

From the accepted R4 / real-source scale authorities:

| Quantity | Governed value | R06 use |
|---|---:|---|
| Full WVS Wave 7 physical cells | 59,595,860 | scale anchor |
| Full LiTS physical cells | 34,744,396 | scale anchor |
| Peak RSS preferred | < 2 GiB | preferred court |
| Peak RSS hard | 4 GiB | hard court |
| WVS carrier preferred | <= 2 GiB | preferred court |
| WVS carrier hard | 4 GiB | hard court |
| LiTS carrier preferred | <= 1.5 GiB | preferred court |
| LiTS carrier hard | 3 GiB | hard court |
| CLOSED_35 carrier preferred | <= 20 GiB | preferred court |
| CLOSED_35 carrier hard | 32 GiB | hard court |

Authority 49 accepted R4 synthetic/scale projections include:

| R4 quantity | Reported value |
|---|---:|
| WVS storage rate | ~17.4 B/event |
| WVS projected carrier | ~0.744 GiB |
| WVS reported peak RSS | ~461.9 MiB |
| LiTS storage rate | ~24.4 B/event |
| LiTS projected carrier | ~0.467 GiB |
| LiTS reported peak RSS | ~690.2 MiB |
| CLOSED_35 projected carrier | ~6.523 GiB |

These figures are **not** promoted here into full-source acceptance. Their role is to establish the current burden of proof: a design already projecting well below budgets should not be replaced by a much more complex Class C carrier merely to improve an already nonbinding storage number.

---

## 2. Arithmetic headroom indicators

Using the reported projections only:

### Storage

- WVS: `0.744 / 2.0 = 37.2%` of preferred carrier budget; `18.6%` of hard budget.
- LiTS: `0.467 / 1.5 ≈ 31.1%` of preferred carrier budget; `≈15.6%` of hard budget.
- CLOSED_35: `6.523 / 20 ≈ 32.6%` of preferred carrier budget; `≈20.4%` of hard budget.

### RSS

Against the preferred `<2 GiB` peak:

- WVS reported ~461.9 MiB is roughly `22.6%` of 2 GiB.
- LiTS reported ~690.2 MiB is roughly `33.7%` of 2 GiB.

Against the hard 4 GiB peak both are substantially lower.

### Adversarial interpretation

This is **headroom, not closure**. A full-source build/reopen/query path could expose nonlinear allocation, eager reopen materialization, Python object retention, join blowups, or slow whole-workflow behavior not present in synthetic/bounded runs.

But the proper inference is asymmetric:

> Before paying Class C complexity, run the full court. If the simple bounded long carrier remains within the governed envelope, theoretical matrix/bitmap savings have no dispositive value.

---

## 3. Whole-workflow resource accounting

The resource court must report at least the following phases separately and end-to-end:

| Phase | Storage / memory risks | Runtime risks | Required receipt |
|---|---|---|---|
| Source open / decoder | reader buffers; string/date decoding; source metadata | format-specific reader cost | peak RSS; decode rows/s; exact reader config |
| Canonical build | Python event retention; override maps; temporary batches; compression buffers | encoding/compression; hashing | peak RSS; temp bytes; final bytes; events/s |
| Seal / publication | duplicate file copies; hash passes | full reread/hash cost | member/root hashes; seal time; bytes copied |
| Reopen | eager tables; relation dictionaries; cache warmup | metadata/Parquet open cost | cold/warm RSS; reopen latency |
| Reconstruction audit | materialized objects/lists; join state | relation/default/override joins | peak RSS; events/s; mismatch count |
| I03 | respondent grouping/indexes; arbitrary joins | conjunction/risk-set scans | representative latency/RSS distribution |
| I05 | candidate search/index state | repeated predicate evaluation | latency/RSS for unforeseen predicates |
| I04 / closure | object graph/index state | exact-ref/authority resolution | latency/RSS; closure mismatch count |
| Replay | source reopen buffers + reconstructed event | random/selected source validation | selected-event latency; mismatch count |
| Integrity verification | hash buffers; duplicate manifests | full vs member/chunk verification | verification latency; bytes read |
| Cache rebuild, if any | duplicate accelerator bytes | construction cost | cache bytes; rebuild latency; deletion/rebuild parity |

A candidate fails the resource model if it lowers canonical storage while moving an unbounded cost into reopen, query joins, caches, or temporary build state.

---

## 4. Resource effect model by candidate family

The labels below are directional until measured by the common runner.

### 4.1 Class A — presumptive low-burden savings

#### C01 — streaming override/build writes

Expected:

- **RSS:** strong reduction where current build retains corpus-scale override/event structures.
- **storage:** neutral.
- **runtime:** neutral to mildly positive/negative depending write batching; should be dominated by boundedness benefit.
- **complexity:** low if ordering/conflict law stays explicit.

Adversarial rule: implement streaming before inventing a new canonical representation if memory is the only failure.

#### C02 — bounded merge-read/audit

Expected:

- **RSS:** strong reduction if reopen/audit is eager.
- **storage:** neutral.
- **runtime:** may trade sequential merge CPU for much lower memory; measure whole workflow.
- **complexity:** low/moderate.

This is the first answer to a reopen-memory failure, not C21.

#### C16 — Parquet row-group/compression tuning

Expected:

- **RSS:** neutral to positive if row groups are bounded sensibly.
- **storage:** positive.
- **runtime:** workload-dependent; pruning vs decompression tradeoff.
- **complexity:** low.

This is precisely the kind of optimization to exhaust before adaptive encoders/matrix redesign.

#### C17 — minimal telemetry

Expected:

- tiny storage/runtime overhead;
- large diagnostic value;
- complexity remains low only if telemetry is a fixed receipt, not a framework.

### 4.2 Narrow Class B — savings with reconstruction cost

#### C03 / C07 — true-grain normalization and defaults+exceptions

Potential storage gain comes from removing repeated release/question/variable-level fields from event rows.

Costs:

- mandatory joins/reconstruction;
- default/exception indexes;
- integrity surface across relations;
- FD certificate/testing burden;
- cache temptation.

Net model:

```text
net_benefit = event_bytes_removed
            - relation_bytes_added
            - exception_bytes_added
            - index/cache_bytes_added
            - extra temp/join memory
            - reopen/query CPU
            - proof/maintenance cost
```

If the determinant requires nearly the whole event key or exception density is high, normalization is ornamental.

#### C05 — typed raw lanes

Can reduce Python/object overhead and improve vector scans. Costs include:

- type-union/tag/null/missing representation;
- reconstruction logic;
- source/type/missingness test cross-product.

It is justified only if the neutral long representation can be reconstructed without lane-specific query semantics.

#### C06 — derivable locators

Byte savings are usually bounded by locator width × event count. Compare that directly with:

- derivation CPU;
- partition-independence tests;
- debugging/replay burden.

If storing an exact compact locator is already cheap, derivation is negative-value complexity.

#### C12 — adaptive encoding

Potentially improves storage beyond ordinary Parquet encoding, but creates policy/test matrices. Required comparison is not “best adaptive codec vs uncompressed”; it is “adaptive policy vs tuned standard Parquet.”

#### C13 — hot/cold split

Can reduce hot-scan bytes but often shifts cost into mandatory side joins for replay/I05. Count cold-store bytes and indexes in canonical total if they are required for exactness.

#### C15 — bounded parallel pipeline

Potential wall-time reduction can increase peak RSS roughly with concurrent batch count plus queues/compression buffers. The resource model must therefore report:

- serial bounded baseline;
- 1/2/N worker peak RSS;
- throughput scaling;
- deterministic receipt equality.

Parallelism is rejected if it turns a practical serial build into an RSS/complexity problem merely to improve already acceptable wall time.

### 4.3 Class C — apparent local wins with large hidden cost surface

#### C08 — vectorized compiler

Potentially excellent ingest CPU/RSS if decoder batches map directly to typed arrays.

Hidden costs:

- heterogeneous coercion/physical-state handling;
- source-local fallback paths;
- vector-to-C11 reconstruction;
- compiler test matrix.

Must beat the best bounded long compiler in **whole-workflow** cost, not only ingest rows/s.

#### C09 — question/columnar partitioning

Potential:

- improved single-question pruning/compression.

Costs:

- cross-question respondent joins for arbitrary conjunctions;
- partition fanout/open files;
- topology/routing/weight side joins;
- identity/index structures.

Report both single-question and hostile k-way I03/I05 workloads. If k-way joins dominate actual machine use, local column benefits are deceptive.

#### C10 — bitmaps

As cache:

- can sharply improve repeated predicate scans;
- storage can be compact for low-cardinality states;
- rebuildable, low semantic authority.

As canonical truth:

- vocabulary explosion for high-cardinality/raw values;
- omitted rare states;
- side metadata requirement;
- unforeseen I05 problem.

Resource model should prefer cache accounting: canonical bytes remain unchanged; bitmap bytes are optional accelerator bytes and must not count as replacing canonical truth unless full Class C acceptance occurs.

#### C11 — late materialization

Potentially reduces object/RSS cost. Hidden costs:

- repeated joins/materialization CPU;
- cache pressure;
- virtual constructor logic;
- unpredictable latency for I05/replay.

Measure cold and warm paths separately. A design that is fast only after a large materialization cache has recreated long-form state has not won.

#### C14 — Merkle/chunk integrity

Resource cost:

- hash metadata per chunk;
- tree construction/verification;
- implementation/versioning burden.

It can save verification I/O only when partial verification/fetch/repair is genuinely used. Otherwise root + member hashes may have lower total cost.

#### C19 — implicit row-position locator

Local byte savings can be excellent; semantic risk is unacceptable if identity migrates with row-group/layout. No amount of byte savings can compensate for replay instability.

#### C20 — source-local compilers

Can improve source-specific encoding but multiplies code/testing/maintenance by source family and exceptional format behavior. Model engineering surface as an explicit cost:

```text
maintenance_surface ~= compiler_paths × type_lanes × missingness_modes × topology_modes × reader_configs
```

This is not a literal performance equation; it is a reminder that code-path cross-products are a project resource.

#### C21 — canonical matrix + virtual long

Potential local optimum:

- lower repeated row metadata;
- vector-friendly scans;
- possible bitmap synergy.

Total cost must include:

- matrix incidence storage;
- all topology/routing/weight/metadata side structures;
- event reconstruction indexes;
- virtual-long facade;
- arbitrary conjunction joins;
- integrity/root structures;
- migration/version code;
- caches required to make I03/I05 practical.

If the total system needs matrix + side relations + bitmap + virtual event cache, compare the **sum** to bounded long, not the matrix file alone.

---

## 5. Complexity budget as a resource gate

R06 recommends HQ record the following per candidate even if not expressed in one scalar score:

| Complexity dimension | Low-burden target | Red flag |
|---|---|---|
| Canonical representations | 1 | 2+ stores requiring synchronization |
| Persistent cache tiers | 0–1 | multiple cache truths/invalidation DAG |
| Reconstruction joins for one event | small fixed chain | source-dependent graph / many optional joins |
| Physical compiler paths | one neutral path + frozen decoder differences | corpus/source-specialized family |
| Encoding policy families | standard/tight fixed set | adaptive per-variable policy engine |
| Integrity mechanisms | minimum root/member scheme | overlapping hash/Merkle/checksum layers without distinct jobs |
| Identity functions | one immutable determinant | physical-position-dependent derivations |
| Downstream source branches | 0 | any |
| Acceptance runners | 1 common runner | candidate-specific favorable court |
| Migration/version rules | small explicit set | representation cross-product |

A design that saves 20–30% storage while doubling these surfaces is presumptively worse when storage already sits comfortably inside preferred margins.

---

## 6. Break-even questions synthesis must answer before admitting complexity

For every mechanism beyond the Class A baseline, HQ should require quantitative answers:

1. **What measured gate fails without it?**
2. **How far over the hard/preferred limit is the simpler candidate?**
3. **How much does this mechanism move that exact whole-workflow number?**
4. **What bytes/RSS/runtime does the mechanism itself add elsewhere?**
5. **Does it create a cache/index/side-table whose bytes must be counted?**
6. **Does it increase cold-query/replay latency while improving a hot path?**
7. **How many additional reconstruction and integrity joins are required?**
8. **What new proof matrix is created across 35 heterogeneous sources?**
9. **Would a standard Parquet/batch-size/streaming change close the same gap?**
10. **If the mechanism is removed later, is canonical truth unchanged?**

If question 1 has no named failure, reject the mechanism under the stop rule.

---

## 7. Recommended benchmark shape for the common runner

Each candidate should emit one comparable table:

```text
candidate_id
source_id
build_seconds
build_peak_rss_bytes
build_temp_bytes
canonical_bytes
optional_cache_bytes
seal_seconds
reopen_seconds_cold
reopen_peak_rss_bytes
reconstruction_events_per_second
reconstruction_peak_rss_bytes
i03_suite_seconds_cold
i03_suite_seconds_warm
i03_peak_rss_bytes
i05_suite_seconds_cold
i05_suite_seconds_warm
i05_peak_rss_bytes
i04_seconds
replay_seconds
integrity_verify_seconds
semantic_mismatch_count
replay_mismatch_count
integrity_failure_count
determinism_mismatch_count
```

For partitioned/parallel candidates add:

```text
batch_size
row_group_size
partition_count
worker_count
```

and require logical receipts to remain invariant across those physical settings.

---

## 8. Resource disposition

### Streaming-long should win

If the full-source common runner confirms the projected headroom and practical I03/I05/replay behavior, then the resource model has no remaining case for Class C. At that point:

- optimize bounded streaming/reopen;
- tune Parquet;
- keep one canonical copy;
- add only a narrowly measured cache if needed;
- stop.

### Class C can enter the court

Only if the measured full-source baseline reveals a hard/practical failure that survives Class A and narrow Class B remedies. The Class C candidate then must report total-system cost including every side relation, cache, index, virtual facade, integrity structure, and cold-path penalty.

### Anti-overengineering conclusion

The correct optimization target is not minimum bytes/event. It is minimum **total burden** subject to exactness and the whole-machine demand envelope:

```text
minimize(
    canonical_storage
  + required_accelerator_storage
  + peak_workflow_memory
  + workflow_runtime
  + reconstruction_complexity
  + integrity/replay_complexity
  + maintenance/proof_surface
)
subject to:
    exact source-native truth
    exact C11 / I03 / I05 / I04 behavior
    deterministic replay
    fail-closed integrity
    governed workstation gates
```

The last two terms are not conveniently measured in GiB, but pretending they are zero is how an optimization campaign turns into a permanent architecture tax.
