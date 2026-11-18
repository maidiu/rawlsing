# ANVIL 10k respondents / 5-role scale — independent receiving

**Decision:** `ACCEPT_SCOPED_10K_FIVE_ROLE_RESOURCE_OBSERVATION`  
**Proof grade:** denominator/state for all five + full f4 cells/member set; **not full five-operation semantic proof**  
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc` · **Integrated cut:** `68aa7cac…` / G5 `d74b641f8…`  
**Author execution:** `19afff9758dcba1eb31dc47426bfca6c11ea6e9c`

## Manifest and source

All **19** author payload hashes in `MANIFEST.json` verify exactly. Source pins match the frozen 68aa snapshot: product `d662fc578…`, postconsumer `0a2e7b899…`, fixture_1006 `1487ad233…`, query_1006 `5a1527204…`. The retained estate manifest is `e192dc25…`; 10,000 respondents, 5 native questions, 32,450 events, 50,000 routing facts, 10,000 weights, retained **31,163,472 B**.

The first harness attempt failed for **0.285 s** before product import due a duplicate `WORKER_RETURNS` vendor path. It is not a second build. One successful build followed.

## Actual costs

| Phase | Actual |
|---|---:|
| Build wall | **210.423 s** |
| Build sampled process-tree RSS | **234,422,272 B** |
| Build sampled scratch | **535,740,432 B** |
| Query admission H | **0.361 s** |
| Prepared index S | **12.618 s** |
| Five Q operation sum | **110.741 s** |
| Serialization/other O residual (derived) | **6.568 s** |
| Query external child wall | **130.864 s** |
| Query sampled RSS | **568,688,640 B** |
| Query sampled scratch | **163,660,060 B** |
| Combined build + query | **341.287 s** (<900 s) |
| Completed operations | **5/5** |

Caps 600 s build/query, 6 GiB RSS, 4 GiB scratch, 900 s total; no abort. The five per-op walls are 25.543, 21.840, 21.239, 26.150, 15.969 s. **O was not separately timed**; the 6.568 s is a derived residual, not a measured serialization bucket.

## Expected truth and independent f4

`EXPECTED_FIXTURE_TRUTH.json` proves only denominators and `SUPPORTED`:
5000 / 5000 / 3333 / 3137 / 385. `scale_result.json` exports semantic/identity/member/ref/replay **digests**, not full cells or member sets for all five. Therefore full five-operation semantic correctness is **not independently proven** by the current export.

I ran exactly **one** independent f4 query on the retained estate from the exact 68aa snapshot, with no build:

- fact `ebf31f71…`; replay `4ef55ad4…`; state `SUPPORTED`
- expected and actual f4 cells: `{0: 3137, 1: 0}` — exact
- denominator members: **3137**, full identity set equals the fixture-derived set; hash `99834e01…`
- risk members: **10000**, full set equals all fixture respondents
- independent Q wall **26.058 s**, index **12.953 s**, **428** row-group reads, 217,350 rows, 82,450 family objects, 33,138 event objects
- independent one-f4 RSS was not separately sampled; the author's five-op process-group RSS is above.

The fixture pattern independently gives the f4 denominator (A=1, B=1, B not missing) and target C=0 for all valid members. This verifies full f4 cell/member semantics, not the other four ops' cells.

## Counters / nesting

- `c11_repository_tripwire_hits=0`; `read_table_calls=0`; `session_builds=1`; `session_opens=1`.
- Author materialization: 287,450 family objects, 78,011 event objects, 1,126 row-group reads, 572,192 rows.
- `source_opens` is **declared zero** by the saved binding receipt (`DECLARED_ZERO__NOT_A_MEASUREMENT`), not an independently measured open counter.
- Retained 31,163,472 B is distinct from build scratch 535,740,432 B and query scratch 163,660,060 B.

## Scope / next

This is 10k respondents × **5 questions**, not 600-column width, 100k, native/original35 science, production service/CURRENT/actor or protected acceptance. One fresh process is not an OS-cold proof.

**Smallest next engineering action:** on the retained 10k estate, export full facts/member sets and add a genuine O timer and source-open counter for the four remaining operations (no rebuild); then ask one bounded 600-column full-width question at the smallest existing width fixture/count. Do not linearly extrapolate 10k×5 to 100k or full width.

Evidence: `WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_G5_20261118/`.
