# FIABC-B02 — CONSUMPTION GAPS

These are consumption gaps, not repair proposals. `EXISTS_IN_REPO != LIVE_EXECUTABLE_CONSUMPTION` is applied literally. None is classified `GENUINELY_MISSING`.

## GAP-01 — current PRE553 runtime authority exists, but no post-fan-in court consumption is proved

**Expected owner/resource:** `rawlsing_next/pre553_runtime_authority.py`, with `pre553_runtime_context.bind_runtime` for LiTS I05.

**Current state:** The last governed P2X execution return records LiTS-A S02 and LiTS-B S03 stopping with `ModuleNotFoundError: No module named 'rawlsing_next.pre553_runtime_authority'`. Current P2X tip `617c9c9426db12a3c0f7fea6b68a582c10759553` later adds that module as part of the R6U/R6V/R6W fan-in. The P2R6S LiTS runtime materializer now imports `Pre553RuntimeAuthoritySet`.

**Consumption proof:** No governed post-fan-in P2X stage receipt demonstrates successful import/materialization, a completed P2R1 binding, or I05 under that runtime authority.

**Disposition:** `PRESERVED_BUT_DISCONNECTED`.

## GAP-02 — WVS binding recursion correction exists, but no post-fan-in execution is proved

**Expected owner/resource:** current WVS projection/binding path converging on generic `bind_governed_c11_projection`.

**Current state:** The recorded run stops WVS-A and WVS-B at S01 with `RecursionError: maximum recursion depth exceeded in comparison`. Commit `617c9c9426db12a3c0f7fea6b68a582c10759553` changes the WVS binding implementation so the exact projection binder delegates to the imported carrier binder instead of recursively calling itself.

**Consumption proof:** No later driver stage receipt shows WVS-A or WVS-B consuming the corrected path.

**Disposition:** `PRESERVED_BUT_DISCONNECTED`.

## GAP-03 — common P2R1 carrier-neutral executor is wired, but no qualifying current cell reaches it end to end

**Expected owner/resource:** `rawlsing_next/pre553_carrier_execution.py`, specifically `RuntimeObjectCatalog.from_documents`, `bind_governed_c11_projection`, `bind_repository_builder`, and the resulting `CarrierNeutralResearchExecutor`.

**Current state:** Driver `DriverServices.compose_p2r1_binding` is a concrete call path. LiTS-A/B stop before runtime-package/binding completion; LiTS-C stops under frozen q310/q311 nonqualification; WVS-A/B stop in S01 preparation/binding; WVS-C is a preserved portability failure with no backend path.

**Consumption proof:** No admitted I03/I05 output or learned product exists in the last governed run.

**Disposition:** `PRESERVED_BUT_DISCONNECTED` for the common seam as an executed successor; `PARTIAL_SUCCESSION` for the overall court because upstream conserved functions are live.

## GAP-04 — A/B accepted owners are verified and deployable, but current measured continuation use is not proved

**Expected owner/resource:** accepted A and B repository builders at `OWNER_COMMIT 0b96b8de9aac774566f872cf0630ebd4ddeb70e6`.

**Current state:** The driver verifies exact owner blobs and can deploy/import them from immutable Git objects. Actual builder invocation occurs only inside `compose_p2r1_binding`, which the recorded continuation does not successfully reach. LiTS-A and LiTS-B completed preparatory facts are instead consumed through banked historical P2X stage receipts.

**Disposition:** `PRESERVED_BUT_DISCONNECTED` for current continuation builder execution; `PRESERVED_AND_CONSUMED` for the banked preparatory receipts.

## GAP-05 — Candidate C does not converge on the common executable runner

**Expected owner/resource:** accepted Candidate-C owner only where frozen source/candidate law permits it.

**Current state:** LiTS-C executes lawful preparation then stops at `C_NONQUALIFYING__S02_C11_REACHABILITY__FROZEN_CACC1_STREAM_OMITS_Q310_Q311_REQUIRED_BY_F02_COMPOSITE_PROJECTION`. WVS-C is terminalized from accepted P2R1 zero-accelerator portability adjudication and later stages are frozen-law skips.

**Consumption proof:** No common `bind_repository_builder(C) -> I03/I05` runtime execution is proved for either source.

**Disposition:** `PARTIAL_SUCCESSION`. The negative states themselves are `PRESERVED_AND_CONSUMED`; a generic C runtime path is not invented.

## GAP-06 — current runtime remains dependent on worker-return / archived fan-in packaging

P2X runtime paths directly open or execute P2R6S support files, banked P2X/P2R1 evidence, historical LiTS AS2A/AS2B artifacts, and immutable historical candidate/R5 implementation blobs. Some are explicit conservation/replay law; others are deployment/packaging mechanisms. The graph therefore has not collapsed into a single current-owner-only packaging surface.

**Disposition:** mixed `PRESERVED_AND_CONSUMED`, `PARTIAL_SUCCESSION`, and `PRESERVED_BUT_DISCONNECTED` as enumerated in `03_HISTORICAL_WORKER_RETURN_DEPENDENCIES.csv`.

## GAP-07 — final court completion is not live

**Expected owner/resource:** `WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py` and a terminal S17 driver ledger entry.

**Current state:** The verifier is actually invoked, but the recorded run reports `BLOCKER__DRIVER_STAGE_RUNNING__COURT__S17_FINAL_COMPLETENESS_AND_VERIFICATION`; its failure-reporting path then raises `ValueError: 'COURT/ALL' is not in list`.

**Consumption proof:** verifier invocation is live; successful terminal verification is not.

**Disposition:** `PARTIAL_SUCCESSION`.

## B02 blocker status

These gaps do not block this archaeology from proving the consumption graph. They are the graph's result. There is no unresolved absence requiring `GENUINELY_MISSING`, and no gap is converted into a repair recommendation.
