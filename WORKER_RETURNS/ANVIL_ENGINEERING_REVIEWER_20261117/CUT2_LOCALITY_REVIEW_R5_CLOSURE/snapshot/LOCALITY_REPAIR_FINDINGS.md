# R5 — EXACT TEST-ONLY LOCALITY REVOCATION REPAIR

**Status:** `LOCALITY_REVOCATION_REPAIR_COMPLETE_RED_GREEN_PARITY`  
**Scope:** exact repair of the independent R4 `REVISE_EXACT_DEFECT`; one corrected `f4_three_raw` observation. No product edit, no new estate/build/pair/matrix/repetition/100k.  
**Product:** `347baec696c8b395d750ac3b9e74417a6490c223`; cut1 G5 `092bf29ffa6724d477abb4ccfc770e3bc492250d`; product READONLY.  
**Independent review:** `07c2409e3c15620a6c3eb392ba02549cf3def83b`, `REVISE_EXACT_DEFECT`.

## 1. Exact defect and minimal repair

R4 `locality_adapter.py::physical_order_respondent_family` materialized/sorted routing facts, then yielded them **without** `self._require_live()` in the yield loop. After the first object was yielded and CURRENT was revoked, R4 yielded a second routing fact. The original product method checks CURRENT per row and refuses.

R5 changes only this:

```diff
     for obj in sorted(materialized, key=lambda item: item.ref.key):
+        self._require_live()
         yield obj
```

No other optimization, index, schema, evaluator, store, or validation change. The original method is installed only inside the witness/profile process and restored in `finally`.

## 2. RED → GREEN witness

Same sealed R2 estate, `RoutingEligibilityFact`, consume one yield, revoke CURRENT, request next:

| Case | First ref | Second result |
|---|---|---|
| R4 old adapter | `...000878d6...` | second ref `...000f3b80...`, **no error** (RED) |
| R5 corrected adapter | same | `DirectEstateError: current source/operation authority refused` (GREEN) |
| Original product control | same | `DirectEstateError: current source/operation authority refused` |

`revocation_witness.py` records `all_expected=true`; each adapter restoration assertion is true. Live valid iteration with CURRENT allowed: **600 routing refs**, canonical ref order sorted, **exactly matches original product order**; restoration assertion true. This is the live valid-order check, not only the revoked case.

## 3. One corrected locality observation

Same cProfile + `CourtInstrumentation` settings as R3/R4; admission and index build outside profile; one f4 query; one parity check.

| Metric | R3 baseline | R5 corrected |
|---|---:|---:|
| Profile Q wall | 18.296 s | **7.583 s** |
| Row-group reads | 3,965 | **50** |
| Row-group rows | 2,012,160 | **25,472** |
| Compressed read bytes | 634,219,540 | **7,942,218** |
| Uncompressed read bytes | 6,011,490,388 | **76,150,826** |
| Family rows | 9,600 | 9,600 |
| Event objects | 37 | 37 |
| Object reconstruction (cProfile) | 9,637 | 9,637 |

External: exit 0, no abort; wall 11.3466 s; sampled process-tree RSS 127,127,552 B; scratch 30,368,896 B; caps 120 s / 2 GiB / 2 GiB. Admission outside profile 0.2709 s; index outside 2.7771 s. Profile wall includes cProfile/wrapper overhead; **not** a production speedup.

Full semantic/identity/refs/member/replay parity vs frozen R2/R3/R4 f4: **exact** (`identity c912bcc4...`). Prepared receipt: one operation on the sealed estate.

## 4. Counts / caveat

`CourtInstrumentation.family_object_materializations` is `0` because the test adapter imports `_object_from_row` directly, bypassing the wrapper; this is the known counter blind spot, not zero reconstruction. cProfile records **9,637 `_object_from_row` calls** (9,600 routing + 37 events). Row-group counters are valid. Per-respondent buffering is bounded at **600 routing facts** in this witness; no full-estate materialization is claimed. The adapter still materializes before first yield, so streaming exception timing differs from the original; not separately executed and not changed in R5.

## 5. Immutability / canonical table

R2/R3/R4 raw evidence and the R4 corrected canonical measurement table remain immutable. R5 references `R4_LOCALITY_EXPERIMENT/CORRECTED_MEASUREMENT.md` / `.json`; no historical rewrite. R5 only adds its repair evidence and handoff appendix.

## 6. Owner handoff

Production symbol: `rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session._respondent_family`.  
Required owner-granted change: physical `gid,off` traversal with canonical ref-order restoration **and** `_require_live()` immediately before every yield, plus the revocation-after-first-yield and full parity regressions.  
Owner: S2-C direct-reader + native I03 evaluator owner.  
**Grant status: `REQUESTED_NOT_GRANTED`** — `#1006` comment `6969187403`. Product files remain READONLY.

## 7. Limits

One sourcefree TEST_ONLY f4 query on sealed 16R/600Q geometry; cProfile overhead; per-respondent 600-object buffer; OS cache uncontrolled; no native/original35/100k/6 GiB/science/actor/economics acceptance. No 1/10/100, Batch, or production patch.
