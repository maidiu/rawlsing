# LAUNCH — PYAT HQ248 F7 NATIVE DECIDE REFERENCE OWNERSHIP REPAIR R3

**STATUS:** NEW — NEEDS LAUNCH
**AGENT:** Space Bunny / governed OpenCode native C engineering
**MODEL / INTELLIGENCE:** Space Bunny Max (verify installed variant)
**MACHINE:** Governed Mac, CPython 3.11.3 x86_64; isolated shared-store sparse worktree, exact local path NOT PREPARED
**BRANCH:** agent/space-bunny-pyat-hq248-f7-decide-refcount-repair-r3
**IMMUTABLE SUBJECT BASE:** c2c0ab7335a3bcfeabb4297139378e3e657cd432 (HQ247 R2 repair)
**COMMISSION TIP:** verify direct origin HEAD and compare to exact tip supplied by HQ launch.
**DECISION:** HQD-2026-10-08-248
**LIBRARY:** NO
**CHECKOUT:** SPARSE_REQUIRED; never clone, use same checked-out worktree, reset, merge, rebase or broaden sparse scope. If no authorized worktree, request infrastructure/bootstrap.

## WHY THIS COMMISSION IS NARROW

HQ independently inspects rawlsing_next/_p07_native_owner_stage_b.c on R2 branch (blob fb5ed13af78672b9d9870b3132787a29d44b928a), around the ordered-source materialization. Source contains:
`/* PyList_AsTuple CONSUMES the ordered reference */ sources = PyList_AsTuple(ordered); if (!sources) goto fail;`
**This is false.** Python C API PyList_AsTuple RETURNS a NEW tuple reference but does NOT steal a reference to its input list. The locally created `ordered` has a live owned reference which is not Py_DECREF'd on the successful or failed conversion path. This is an independently identified concrete C ownership defect and a strong candidate explanation for the worker's measured ~12 positive/~15 negative PyMalloc blocks per decide() call. It has NOT been runtime confirmed as sole cause and is NOT an accepted repair.

## Task

1. Independently confirm the exact ownership defect from CPython 3.11.3 C API/source and reproduce per-call positive and negative memory growth at the immutable R2 subject SHA under the governed interpreter. Use sensible warmed allocated-block/ASAN/refcount measurements; distinguish harness artifacts from genuine leaks.
2. Repair `PyList_AsTuple(ordered)` ownership with correct decref on BOTH success and failure paths and preserve all other approved boundaries. Audit adjacent temporary references, early errors and module state for any residual leak. Do not merely change comment; require measured before/after trend near the warmed-noise floor, negative and genuine positive.
3. Verify B1–B4/P1/CONFLICTING_AUTHORITY and actual valid P07-vs-native AUTHORIZED remain intact, custody hash, replay, six precedence steps, actual 17-state outcome union, trusted assumption explicitly pinned but NOT an authentic sealed production TCB.
4. Rebuild only governed quarantined synthetic modules; execute existing 397 targeted tests and added hostile reference-ownership tests, positive and negative memory stress, malformed/replay edge cases, module-init OOM feasibility, red fault injection, production baseline digest comparison at same script. Do not claim work ran unless actually executed; show exact command/environment, blobs, digests, tests, limitations.
5. Return exact ref-ownership table for ordered/list/tuple/dict materialization along each exit path. If bug fixed but another leak remains, report PARTIAL and bounded next culprit, not a false READY.
6. No Stage C, no production P07/F7 import or native authority adoption, no source access, no F7-RR-04G closure. Future separate reviewer must independently examine the EXACT R3 SHA and actual F7 four hostile forgery/five lawful positive integrated paths when authorized.
7. T1 missing real production-owned sealed constructor is a **separate** boundary/commission: do not solve it by accepting test-supplied callbacks; do not edit production.

## Permitted writes

ONLY `rawlsing_next/_p07_native_owner_stage_b.c`, optionally `rawlsing_next/_p07_native_owner_stage_a.c` if demonstrably same ownership bug (justify), directly matching new synthetic native tests, and `WORKER_RETURNS/PYAT-HQ248-F7-DECIDE-REFERENCE-OWNERSHIP-REPAIR-R3/`. Preserve existing tests; no .so committed.

## Return

`00_RETURN.md`, `01_OWNERSHIP_TABLE_AND_PATCH.json`, `02_POSITIVE_NEGATIVE_LEAK_MEASUREMENTS.json`, `03_PARITY_REPLAY_REGRESSION.json`, `04_FINAL_DISPOSITION.json`, reproduction scripts if relevant.

One of `F7_R3_MEMORY_REPAIR_READY_FOR_EXACT_SHA_INDEPENDENT_REVIEW`, `F7_R3_MEMORY_REPAIR_PARTIAL__NAMED_DEFECT`, `F7_R3_MEMORY_REPAIR_BLOCKED`. Any READY is candidate-level only and T1 unbuilt. Commit/push own branch, verify remote SHA, report that SHA. Never self-adopt.