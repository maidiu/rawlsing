# Tests, economics and finite residuals

## Test result at `30bd02a10feb1b5b97bcbe70e3981f482d2a412c`

| Command group | Result |
|---|---|
| 11 current ABI/compact/grouping/route/discovery/batch/custody test files | **148 passed in 30.08 s** |
| merged L01/L02 current ABI regression | **19 passed in 5.82 s** |
| compact view file | **10 passed** |
| fault/restore subset | **8 passed, 17 deselected in 11.62 s** |

Fault/restore cases, all with RED before restore and exact baseline restored:

- `test_cache_hit_delete_and_rehashed_same_key_poison_rebuild`: warm exact hit; forged same-key body rejected; delete and rebuild restore identical bytes/material.
- `test_stale_cache_and_torn_publication_keep_previous_complete_slot`: interrupted publication and stale member fail closed; previous complete slot remains.
- `test_revoked_workload_never_opens_warmed_accelerator`: revoked issuance raises admission error before cache read.
- `test_compressed_event_bodies_exact_bounded_chunks_and_old_cache_read`: old raw-row-group cache read still yields exact compressed chunks.
- `test_compressed_bodies_exact_across_routed_state_topology_and_weight_shapes`: five synthetic shapes plus routed/missing-weight physical shapes.

Logs: `results/targeted_tests.log`, `results/fault_restore_tests.log`.

## Physical cold/warm comparison

Driver: `bench_compact_current.py --mode compare`; sourcefree synthetic physical stream; one timed process per variant; co-tenant.

| N | Variant | Compact conversion wall / CPU | Cache | Facts/release/source exact |
|---:|---|---|---|---|
| 200 | v1 in-memory | 0.689 / 1.308 s | none | true |
| 200 | v2 cold | 0.971 / 1.595 s | 1 miss, 1 write, 429,814 B | true |
| 200 | v2 warm | 0.297 / 1.103 s | 1 hit, 0 writes | true |
| 1,000 | v1 in-memory | 1.672 / 2.481 s | none | true |
| 1,000 | v2 cold | 2.296 / 3.089 s | 1 miss, 1 write, 2,184,216 B | true |
| 1,000 | v2 warm | 0.714 / 1.485 s | 1 hit, 0 writes | true |

Whole-process `ru_maxrss` at N=200: v0 60.3 MB, v1 86.8 MB, v2-cold 135.4 MB, v2-warm 92.7 MB. At N=1,000: v0 152.5 MB, v1 177.3 MB, v2-cold 228.9 MB, v2-warm 189.9 MB. These are process-wide, not cache-attributed RSS.

Interpretation: the explicit persistent cache buys warm compaction/read cost and costs cold write/space. It should activate only for an explicitly reused release/projection workload; no default/global cache is warranted. N=1,000 cache is about 2.2 MB on this synthetic shape. No 16-GiB operational test was run.

## Multi-shape compact probe

`multi_shape_probe.py`, synthetic/sourcefree, co-tenant.

| Shape | Events | Chunks | Compressed / raw bytes | Cache B | Cold wall / CPU | Warm wall / CPU |
|---|---:|---:|---:|---:|---:|---:|
| weighted-routed-kway | 560 | 3 | 41,550 / 1,053,920 | 66,424 | 0.503 / 1.305 s | 0.027 / 0.027 s |
| typed-states-and-routing | 6 | 1 | 1,610 / 10,958 | 9,588 | 0.002 / 0.002 s | 0.001 / 0.001 s |
| ordered-ranked-repeated | 6 | 1 | 1,529 / 11,293 | 9,780 | 0.002 / 0.002 s | 0.001 / 0.001 s |
| raw-weighted-divergence | 2 | 1 | 1,032 / 3,680 | 9,120 | 0.001 / 0.001 s | 0.001 / 0.001 s |
| country-zz-scalar | 2 | 1 | 1,048 / 3,784 | 9,341 | 0.001 / 0.001 s | 0.001 / 0.001 s |

All exact body/group/chunk checks passed; warm cache never reserialized.

## Multi-shape actual first consumer

`multi_shape_first_consumer.py`, synthetic/sourcefree, grouped vs ungrouped `execute_i03`; full `as_dict`, fact refs, replay refs, query refs and release refs exact for every operation.

| Shape | Country | Ops | All exact | Core builds/hits/fallbacks |
|---|---|---:|---|---|
| weighted-routed-kway | US | 7 | true | 5 / 2 / 0 |
| country-zz-scalar | ZZ | 2 | true | 2 / 0 / 0 |
| typed-states-and-routing | US | 1 | true | 1 / 0 / 0 |
| ordered-ranked-repeated | US | 1 | true | 1 / 0 / 0 |
| raw-weighted-divergence | US | 2 | true | 1 / 1 / 0 |

## Finite residuals

1. These are not all35 or original-source performance results. All35 bytes are in custody per `b90708f…`, but real-source decode/C11/native first-consumer qualification requires A/D current adapters and the runtime-only root alias `USER_ORIGINAL35_DATA_ROOT`.
2. No 16-GiB operational suitability test was run (**NOT_RUN**, not PASS).
3. No clean/uncontended benchmark window; all timings are co-tenant.
4. No distinct nonauthor review of the current-base integration or new author test.
5. No protected merge, all35 native fact, source/science/actor grant, or self-acceptance.
