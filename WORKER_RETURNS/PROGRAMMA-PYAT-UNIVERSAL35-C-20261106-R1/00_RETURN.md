# UNIVERSAL35 C — current-base hybrid physical fan-in return

**FINDING:** The accepted L03 compressed event-body slice (`02c1200…`, review `9999c0af…`) applies exactly to current protected base `d119045…` without replacing current P2, capacity, #702, or other newer-owner code. The selected production view blob is byte-identical to the accepted donor view. Current-base integration tests and bounded multi-shape sourcefree probes pass.

**INTERPRETATION:** This is a sourcefree engineering candidate at exact implementation commit `30bd02a10feb1b5b97bcbe70e3981f482d2a412c`. It does not prove all35/native/original-source performance, protected adoption, or independent review of the current-base integration. All35 original bytes are present in custody per `b90708f…`, but this lane did not read them and did not claim synthetic results as all35.

**ACTION:** HQ may send this isolated branch to a distinct nonauthor reviewer for the current-base integration. Real-source cold/warm qualification remains a downstream A/D-adapter task using the runtime root alias `USER_ORIGINAL35_DATA_ROOT`; do not hardcode its absolute path in engine code.

**OWNER:** HQ plus later distinct nonauthor reviewer for engineering receiving; original source/science owners for any native use; protected integrator for any protected CAS. This return does not self-accept or merge.

## Exact source identity

- Branch: `codex/pyat-universal35-c-20261106-r1`
- Base: `d119045f4169439b4ba02d0870bc328f8beb3aaa`
- Implementation/evidence candidate commit: `30bd02a10feb1b5b97bcbe70e3981f482d2a412c`
- Accepted compressed donor: `02c1200b82b8397e551817e8e4cf2c6763413189`
- Donor independent review: `9999c0afac5d7d7eb72ad0df602da4b232a49565`
- Selected files:
  - `rawlsing_next/_pre553_c11_execution_view.py` blob `986f327aa18053edc61bd837cdded02bbf8388d9` — exact accepted donor blob.
  - `rawlsing_next/tests/test_pre553_c11_execution_view.py` blob `e6c002334724aefff7d61e0165577a30d8dc3a8d` — donor test plus author cross-shape coverage.
- Diff from base: 2 files, 329 insertions, 36 deletions; view `194` changed lines; test `171` added lines.
- P2/capacity files are unchanged from base and remain the received `409be32…`/`9a5cfd…` implementation. No donor test or historical control-room document was bulk cherry-picked.

## What was selected

- Bounded `_CompressedBodies` chunks with exact 256-event boundaries and on-demand Zstd decompression (`_pre553_c11_execution_view.py:83`).
- Streaming `_BodyCacheWriter` preserving the existing Parquet/Zstd cache format (`:262`), chunked read compatibility (`:221`), and exact old-cache read support.
- Existing opt-in private cache policy unchanged: `RAWLSING_C11_ACCELERATOR_DIR`; no global/home default, no second persistent truth.
- Exact selector, event materialization, cache key, authority/release/risk/weight/replay checks preserved.
- Author cross-shape test: weighted/routed 560-event shape, typed states/routing, ordered/ranked/repeated topology, RAW-vs-weighted divergence, country `ZZ`, and physical routed plus missing-weight shapes; cold and warm cache; exact chunk/body/group checks.

## Actual first consumers

- `CarrierNeutralResearchExecutor.execute_i03` — `rawlsing_next/pre553_carrier_execution.py:430`.
- Route B production — `rawlsing_next/pre553_route_b_production.py:495`.
- Issued workload — `rawlsing_next/pre553_issued_workload.py:280`.
- Test-only source adapter — `rawlsing_next/pre553_native_workload_binding.py:423`.

## Test evidence

- Targeted current ABI/compact/grouping/route/discovery/batch/custody suite: **148 passed**.
- Current merged L01/L02 ABI regression check: **19 passed**.
- Compact view file: **10 passed**.
- Fault/restore subset: **8 passed, 17 deselected**.
  - rehashed same-key cache poison -> exact rebuild; delete -> rebuild; stale/torn publication -> previous complete slot; revoked issuance -> cache never opened; exact baseline restored.
- Full command text: `results/commands.jsonl`; test logs: `results/targeted_tests.log`, `results/fault_restore_tests.log`.

## Bounded economics

- Physical compact comparison N=200 and N=1,000: `facts_exact_equal`, `release_identity_equal`, and `source_identity_equal` all true for v1/v2-cold/v2-warm.
- Cache: N=200 cold miss+write then warm hit; file total 429,814 bytes. N=1,000 cold miss+write then warm hit; file total 2,184,216 bytes.
- Whole-process `ru_maxrss` was 60.3/86.8/135.4/92.7 MB at N=200 and 152.5/177.3/228.9/189.9 MB at N=1,000 for v0/v1/v2-cold/v2-warm. These are process-wide, not attributed cache RSS.
- 560-event shape: 3 chunks; 41,550 compressed bytes from 1,053,920 raw bytes; 66,424-byte cache; cold 0.503 s wall / 1.305 s CPU; warm 0.027 s wall / 0.027 s CPU in the co-tenant probe.
- All timings are co-tenant and not a clean benchmark window. No 16-GiB operational test was run.

## Source custody update

All35 original files are reported present and exact-hash verified by HQ evidence commit `b90708f7d79624faae3da2408932829e569e5ae2`, `WORKER_COMMISSIONS/PROGRAMMA_PYAT_UNIVERSAL35_20261106_R1/01_LOCAL_SOURCE_CUSTODY_OBSERVATION.json`: 35 exact matches, 1,319,161,326 bytes, root alias `USER_ORIGINAL35_DATA_ROOT`. HQ separately observed physical headers readable, with SRC13/SRC14 requiring their exact R157 source-bound latin1 compatibility configurations and default failure preserved. These are byte/header custody facts only: response decode `NOT_RUN`, native empirical execution `NOT_RUN`, no scientific/structural grant. This C lane did not read original files.

## Grades

- **ENGINEERING:** Author evidence meets the named current ABI/first-consumer and fault/restore tests at `30bd02a…`; **HOLD for HQ plus distinct nonauthor current-base review**. Not self-accepted.
- **SCIENTIFIC:** No new source/science/structural meaning; sourcefree exactness only. Native/original35 scientific acceptance is **NOT_GRANTED**.
- **AUTHORITY:** Sourcefree engineering only. No protected merge, no all35 native fact, no source bytes published, no actor grant, no reviewer substitution. **HOLD**.

## Remaining finite proofs

1. Distinct nonauthor review of current-base compressed integration and the added cross-shape author test at `30bd02a…`.
2. Real-source cold/warm multi-shape qualification through A/D current adapters with runtime-only `USER_ORIGINAL35_DATA_ROOT`; **NOT_RUN** here.
3. Bounded 16-GiB operational suitability and clean uncontended benchmark window; **NOT_RUN** here.
4. Protected receiving decision after review; **no protected merge by this worker**.
