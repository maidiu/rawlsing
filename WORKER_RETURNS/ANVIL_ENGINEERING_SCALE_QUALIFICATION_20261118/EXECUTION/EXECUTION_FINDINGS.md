# SCALE QUALIFICATION EXECUTION — 10K RESPONDENTS, 5 ROLES

**Status:** `MEASURED_10K_RESPONDENT_5ROLE_SOURCEFREE`  
**Scope:** one 10,000-respondent/5-native-question sourcefree estate build + one fresh prepared five-operation run on integrated `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`.  
**Not:** 600-column/full-width, 100k, native/original35/science/actor/CURRENT, production service or accepted economics.

## 1. Build actuals

| Metric | Actual |
|---|---:|
| Respondents | 10,000 |
| Native questions | 5 |
| RespondentEvent | **32,450** (not the 32,448 prep estimate) |
| RoutingEligibilityFact | 50,000 |
| WeightMeasureFact | 10,000 |
| QuestionVariableBinding | 5 |
| Retained estate | **31,163,472 B** (~31.2 MB; prep estimate ~164 MB was high) |
| Build external wall | **210.423 s** |
| Build process-tree RSS peak sampled | 234,422,272 B |
| Build scratch peak sampled | 535,740,432 B |
| Build exit / abort | 0 / none |
| Manifest SHA-256 | `e192dc25e55528101b6116f81aa7bce49c170a9a72f61386e97d20a9f9e09619` |

The 10k fixture is respondent-scale with only five native questions; it is **not** 600-column width. Build_context materializes the fixture eagerly; this cost is included in the 210.423 s build, not in query H/S/Q/O.

## 2. Query actuals (one fresh process, one prepared session)

| Phase | Actual |
|---|---:|
| Admission H | 0.361 s |
| Prepared index S | 12.618 s |
| Five positive ops total wall | 129.927 s |
| External child wall | 130.864 s |
| Process-tree RSS peak sampled | 568,688,640 B |
| Scratch peak sampled | 163,660,060 B |
| Completed operations | **5 / 5** |
| Source opens / full C11 repositories in query | 0 / 0 |

Per operation:

| Op | Wall s | Fact | State | Denominator |
|---|---:|---:|---|---:|
| selected_weighted | 25.543 | 1 | SUPPORTED | 5000 |
| f2_forward_raw | 21.840 | 1 | SUPPORTED | 5000 |
| f2_reverse_raw | 21.239 | 1 | SUPPORTED | 3333 |
| f4_three_raw | 26.150 | 1 | SUPPORTED | 3137 |
| repeated_mr_raw | 15.969 | 1 | SUPPORTED | 385 |

Controlled fixture expectation matches for all five: `EXPECTED_FIXTURE_TRUTH.json` (`all_expected_match=true`). Full semantic/identity/member/ref/replay hashes are pinned in `EXECUTION/scale_result.json` for the reviewer. No native oracle rerun is claimed.

Counters: row-group reads 1,126; rows 572,192; compressed 132,332,989 B; uncompressed 1,686,816,826 B; family objects 287,450; event objects 78,011; selected events 68,010; session builds 1; no whole-table read; no legacy C11Repository.

## 3. Budget / caps

Build 210.423 s + query external 130.864 s = **341.287 s** sequential, under 900 s. Build child cap 600 s; query child cap 600 s; RSS cap 6 GiB; scratch cap 4 GiB; free-space gate ≥8 GiB passed. External 0.25 s process-group sampling; no abort. The estate is retained at `EXECUTION/.local-data-10k` for reuse; not committed.

**Cold vs cache:** one fresh process; OS page cache is uncontrolled. No warm-cache claim. Productive state is one prepared session; index S is outside Q.

## 4. Harness correction / first failure

The first build attempt exited 1 in 0.285 s with:

`VENDOR_PATH_MISSING: .../WORKER_RETURNS/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/vendor`

Cause: `build_10k_estate.py` used `Path(__file__).parents[2]` (WORKER_RETURNS) and then appended `WORKER_RETURNS` again. Corrected to `parents[3]` (MEASUREMENT_PREP) and verified vendor path. The successful build followed. This is an own-harness defect, not a product failure. `HARNESS_CORRECTION.diff` records it.

## 5. Product/source pins

- integrated `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`; G5 `d74b641f8ec0c3a94da8ea90e9f5e7b5dc97a0ab`
- product `pre553_direct_estate_i03.py` `d662fc578a1ecb42d54ec8b4bdab87fd7ecec176`; postconsumer `0a2e7b899ebd392761d38b8ceb175f0bf81c6378`
- snapshot temp `EXECUTION/SNAPSHOT_PATH.txt`; exact execution blobs verified before build
- fixture `fixture_1006.py` `1487ad233c871d973b2a64c9649c37f100c46832`; `query_1006.py` `5a15272043246e5293a51e2390adc038bd280e47`

## 6. Limits

Only one positive five-operation run; no old baseline, profiler, test-only adapter, repetitions or matrix. Accepted G5 negative/revocation contracts are preserved and were not rerun. No original35/raw respondent/source/science/actor/CURRENT/protected grant. This is not 100k/full-width/economic acceptance.
