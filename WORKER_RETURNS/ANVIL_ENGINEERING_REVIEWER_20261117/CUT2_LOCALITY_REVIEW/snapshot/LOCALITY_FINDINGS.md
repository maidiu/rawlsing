# R4 TEST-ONLY LOCALITY EXPERIMENT — FINDINGS

**Status:** `LOCALITY_PROFILE_COMPLETE_PARITY_MATCH`  
**Scope:** ONE changed test-only execution of existing native `f4_three_raw` on the sealed R2 estate. No build, no new pair, no matrix, no repetition, no 100k.  
**Product:** `347baec696c8b395d750ac3b9e74417a6490c223`; cut1 G5 `092bf29ffa6724d477abb4ccfc770e3bc492250d`. Product files READONLY.

## 1. Changed mechanism (test-only)

`R4_LOCALITY_EXPERIMENT/locality_adapter.py` temporarily replaces `DirectEstateI03Session._respondent_family` in the profiling process only:

- baseline: `SELECT ref,gid,off FROM members WHERE family=? AND respondent=? ORDER BY ref`;
- test-only: **`ORDER BY gid,off`**, then materialize and **sort by `obj.ref.key` before yielding** to restore the externally observable canonical order;
- same `_object_from_row`, exact ref/body/respondent/universe checks, same `_require_live`, same one-row-group cache, same `members` table, no whole-estate materialization (one respondent/family at a time);
- original method restored in `finally`. No product edit, no new store/evaluator/index.

Source symbols:
- `rawlsing_next/pre553_direct_estate_i03.py:398(DirectEstateI03Session._respondent_family)`; SQL at lines 412–414; cache at 418–426.
- `rawlsing_next/_pre553_query_eval.py:51(_routing_fact_for)`; the downstream filter that materializes all routing facts per respondent.
- `rawlsing_next/pre553_parquet_carrier.py:131(_object_from_row)`; exact body reconstruction/validation.

## 2. One profile, baseline comparator

Same cProfile + `CourtInstrumentation` settings as R3; one fresh child; admission and index build outside profile; one query; one parity check.

| Metric | R3 baseline | R4 physical-order | Change |
|---|---:|---:|---:|
| Profile Q wall | 18.296 s | **7.690 s** | -10.606 s (58.0% profiled) |
| Row-group reads | 3,965 | **50** | -3,915 (98.7%) |
| Row-group rows | 2,012,160 | **25,472** | -1,986,688 (98.7%) |
| Compressed read bytes | 634,219,540 | **7,942,218** | -626,277,322 (98.7%) |
| Uncompressed read bytes | 6,011,490,388 | **76,150,826** | -5,935,339,562 (98.7%) |
| Family rows yielded | 9,600 | **9,600** | same |
| Event objects | 37 | **37** | same |
| Object reconstruction (cProfile) | 9,637 | **9,637** | same |
| Row-group cache clears | 3,964 | **50** | -3,914 |
| External child wall | 22.57 s | **11.93 s** | profiler/wrapper context |
| Sampled process-tree RSS | 172,122,112 B | **128,036,864 B** | external sample |
| Sampled scratch | 30,390,928 B | **30,368,896 B** | external sample |

The profile wall reduction is not a production speedup: cProfile/wrapper overhead remains and this is one test-only condition. It shows the measured row-group-read thrash was the dominant locality defect.

## 3. Exact parity

Full semantic/identity/refs/member/replay parity against frozen R2/R3 `f4_three_raw`: **exact** (`identity c912bcc4...`). Prepared receipt records exactly one operation on the frozen estate. No validation, CURRENT/release/integrity, routing/negative semantics or member list was changed or skipped.

## 4. Counter caveat

`CourtInstrumentation.family_object_materializations` reports `0` for this run because the test adapter imports `_object_from_row` directly from `pre553_parquet_carrier`, bypassing the instrumentation wrapper. This is a harness blind spot, not zero reconstruction. cProfile records **9,637 `_object_from_row` calls** (9,600 routing family objects + 37 event objects); row-group and row counters are unaffected. The adapter's exact validation is present.

## 5. Production handoff (not performed)

Minimum product handoff: owner grant for `rawlsing_next/pre553_direct_estate_i03.py` `DirectEstateI03Session._respondent_family` to use physical `gid,off` traversal and restore canonical ref order before yield (or an equivalent covering order), with exact fact/parity tests. Owner: S2-C direct-reader + native I03 evaluator owner. No grant asserted; product remains READONLY.

If the canonical-order restoration cannot be proven for every consumer, the exact defect/hold is: the ref-ordered member query with single-row-group cache is the hot path; do not change order without a complete ordering/parity contract. R4 restored order before yield and matched all full digests, but production acceptance still needs owner review.

## 6. Alternatives ruled out by actual data

- SQLite query/index tuning alone: `sqlite3.execute` was 0.011 s / 53 calls; not the bottleneck.
- Numerical rewrite: not the hotspot.
- Disable validation/hash: would break exact body/ref/parity; rejected.
- New store/engine: not needed for this locality defect.
- 1/10/100 or fresh Batch: not justified by one profile; no rerun.

## 7. Limits

One test-only query, 16R/600Q sourcefree geometry, one sealed estate; cProfile overhead; OS cache uncontrolled; no native/original35/100k/6GiB/science/actor/economics acceptance. R2/R3 raw evidence and old report remain frozen.
