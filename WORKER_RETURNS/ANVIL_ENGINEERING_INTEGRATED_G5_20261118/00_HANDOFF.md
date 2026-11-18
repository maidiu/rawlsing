# ANVIL integrated two-edit sourcefree first-consumer G5

**Decision:** `ACCEPT_SCOPED_INTEGRATED_TWO_EDIT_SOURCEFREE_FIRST_CONSUMER`  
**Reviewer:** `ses_e30a442d8ffeYBbXi7rPUpPxoc` — same existing locality/native S1E reviewer; not author of either edit.  
**Branch:** `agent/anvil-engineering-cut1-owner-20261117-r1`  
**Reviewed executable:** `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`  
**Author return:** `7f0366de3ee83b90b9607e278193bd08c4478213`

## Exact integration

Two production files and two new focused tests differ from baseline `347baec…`:

- `rawlsing_next/pre553_direct_estate_i03.py` — `d662fc578a1ecb42d54ec8b4bdab87fd7ecec176`
- `rawlsing_next/pre553_source_postconsumer_receipts.py` — `0a2e7b899ebd392761d38b8ceb175f0bf81c6378`
- `test_anvil_production_locality_20261118.py` — `7373c1704e21bcb4155eb690b17de5ecd8bf22dc`
- `test_anvil_prepared_saved_postconsumer_join.py` — `d555f811353532f6df4b1eed3ea3476e4bb87719`

Cut1 wrapper `c568836b…` and Batch runner `8320f284…` are unchanged. No other production path differs.

I executed an isolated `git archive 68aa7cac… rawlsing_next` snapshot under my own return. Execution blobs resolved to the snapshot; the old OWNER baseline was not used and no locality adapter was installed. The actual production `_respondent_family` source contains `ORDER BY gid,off`, canonical `sorted(materialized, …)`, and per-yield `_require_live`.

## Integrated sourcefree chain

`integrated_parity.py` from the frozen author return, with only its output path changed:

- sourcefree Q2 5-respondent fixture → 13-family saved estate;
- source stats: one source read/snapshot/decode/cell pass, `full_c11_builds=0`, cleanup complete;
- compiler: v1 **0 QUERY / 1 DISCOVERY**, v2 **12 QUERY / 1 DISCOVERY** under `TEST_ONLY_SOURCEFREE`;
- base and prepared admissions: **13** Batch units, all **COMPLETED**; prepared **1** index build;
- **22** operation fates, **8 ELIGIBLE / 14 HELD**, **6** positive-native-linked, **2** eligible pending, **13** native units rechecked, **8** discovery candidates exactly joined, **0** issue grants;
- exact base/prepared parity for full rows, audit, native output refs, Batch provenance, replay and result hash.

The 13 C11 family keys are present, but not all nonempty: 7 nonempty families and 6 zero families (`WeightMeasureFact` plus five binding/relation families); `ReplayManifest=1` is a separate non-family table. This is a small sourcefree fixture, not full-family occupancy.

Per-run source SHA `4a6a08f1…`; fixture SAV identity is timestamp/root-specific. Exact parity is established within-run, not by cross-run hash equality with the author fixture.

Run: exit 0, wall **3.50 s**, max RSS **133,939,200 B**.

## Focused independent courts

`47 passed in 32.93s`:

- new prepared postconsumer: 8
- production locality: 2
- cut1 prepared Batch: 5
- S1E first consumer: 24
- R03 governed query v1/v2: 8

Covers changed valid source → changed native fact → exact restore; fabricated QUERY, root/CURRENT, forged receipt and exact base/prepared subclass refusals; foreign runner/repository; v1 genuine 0Q/1D and v2 TEST_ONLY eligibility/issuer fates. No full 113 rerun, locality profile, 100k or benchmark matrix.

## Component status

The separate postconsumer component G5 has now been independently received at `d2988fdb2e5fd0f47f8080b49aef2c9554a07326`, verdict `ACCEPT_SCOPED_PRODUCTION_POSTCONSUMER_PREPARED_ADMISSION`; I read `REVIEWER/WORKER_RETURNS/.../PRODUCTION_POSTCONSUMER_G5_20261118/REVIEW_VERDICT.json` and did not repeat its courts. My locality component remains accepted at `9ff290fd9…`. This integrated verdict does not promote either component to production service, science, actor, CURRENT or protected grade.

## Limits

Sourcefree TEST_ONLY engineering only. No original35, native science, production service/CURRENT/actor, issuer/writer/schema or protected merge. No 100k/full matrix, no new locality benchmark, no external source authority. Integration `UNMERGED`. Both components are independently received at their scoped test-only grades; broader adoption remains separate.

Evidence: `WORKER_RETURNS/ANVIL_ENGINEERING_INTEGRATED_G5_20261118/`.
