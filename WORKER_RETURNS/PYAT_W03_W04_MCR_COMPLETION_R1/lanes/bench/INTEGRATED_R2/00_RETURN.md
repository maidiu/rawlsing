# Bench integrated-R2 method repair return

**Author status:** `DELIVERED_PENDING_RECEIVING` for the bounded benchmark-method repair only; whole MCR/economics remains `INCOMPLETE`.
**Source head:** `81a4f4cd314bd236d8f742e3fde343363a73168a`
**Branch:** `agent/pyat-w03-w04-mcr-bench-integrated-r2`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-bench-integrated-r2`
**Prior bench:** `c44cf09fb9ca5cbc235763d8bd5df9b0074de289` (preserved; its 13% pre-integration RSS regression remains diagnostic RED, not erased).
**Coupled source pins:** `2709733e` (cold/policy coupling); `558f4169` (persistence policy candidate).

## Defect corrected

Previous bench `_build_release` called `project_c11_candidate_from_physical_cells` → `validate_c11_source_release` → `_compact_public_objects` directly and used `ParquetC11Carrier.reopen` as “cache hit.” It therefore did not exercise the new normal streaming cold caller or the governed derived accelerator.

The repaired benchmark now calls the actual normal current caller:

```text
build_source_backed_c11_repository(stream, projection, current_authorities=...)
```

with the explicit governed private policy from the actual cache module, creating the real derived `c11-events-*.parquet` cache. Canonical `ParquetC11Carrier` persist/reopen is measured and reported separately. The old path is no longer used.

## Delivered method

- Actual streaming cold + I02/C11 validation/seal + governed derived-cache attachment is one transparent `normal_current_cold_build`/`cold_combined` boundary; no fake per-I02 split.
- Derived cache miss/write/hit is determined from actual cache files, mtime, size and the authenticated envelope (schema `PRE553_I02_EVENT_ACCELERATOR@2`), not from canonical Parquet.
- Canonical carrier persist/reopen has separate stages and files; it is never labeled derived hit.
- `narrow`, `wide`, `repeat` use exact physical cells, governed projection, real I03/I05. No statistical oracle.
- `rows` and actual event counts are both reported; small runs are explicitly `NON_FINAL_DIAGNOSTIC`, and `full-matrix` is only eligible at 100000 rows, all three profiles, 3 repetitions.
- Full-matrix rebuild now re-persists canonical and derived roots.
- Corrupt derived cache is tested as safe miss/rewrite, not a false hit.

## Small proof (64 rows)

Three sources — current 81a4, frozen 46b, protected 4f3413 — produced **identical full I03/I05 consumer fingerprints** for narrow/wide/repeat:

```text
narrow  97c93ac1...  events 128
repeat  adca1205...  events 384
wide    4acb0294...  events 384
```

Current normal path wrote exactly one governed derived cache file. Small full-matrix:

- cold: derived miss/write, canonical persist
- warm: derived hit (same envelope/mtime), canonical reopen hit separately
- consumer fingerprint parity between normal streaming path and canonical reopen: **true**
- delete/rebuild: derived rewrite and separate canonical rebuild
- final matrix eligibility: **false** at 64 rows/1 repetition; no pass claimed

## Remaining

- Required 100000 × 3-repetition full matrix is **NOT_RUN**; independent same-method economic check and final pinned SHA are prerequisites.
- Previous 46b-vs-4f 100k narrow numbers remain preintegration diagnostics: RSS +13.0% RED, not final candidate proof.
- Production code/ABI was not changed. No new engine, QUC reader, resolver, source permission, native/S3/science/actor effect, worker, install, or model/provider/effort change.
- Whole 12-ID MCR, independent code/economic receiving, external block/verifier and protected receiving remain outside this lane. `goal_complete=false`.
- Quota `UNKNOWN`.

## Evidence

- `01_HARNESS_METHOD_REPAIR.md` — exact old/new call path and instrumentation boundary.
- `02_PARITY_AND_CACHE.md` — small parity, derived/canonical separation and refusal receipts.
- `03_REPRODUCIBLE_RETURN.md` — commands, tests, blobs and remaining final matrix.
- `parity_summary.json`, `parity_*_64_cold.json`, `current_64_full_matrix.json`.
