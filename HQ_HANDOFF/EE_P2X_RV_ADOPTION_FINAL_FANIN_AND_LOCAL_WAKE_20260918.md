# EE-P2X-RV ADOPTION, FINAL PREPARATION FAN-IN, AND LOCAL DARWIN WAKE — 2026-09-18

Status: `ADOPTED__RECEIPT_VERIFIER_FANIN_COMPLETE__LOCAL_DARWIN_EXECUTION_AUTHORIZED`

Decision: `HQD-2026-09-18-038`

## Predecessor authority

- checkpoint `20260918T0406-0400`
- immutable handoff `6c595d5bcfbe8902dc25679c116edd44fb79a86f`
- semantic PRE-MAIN `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`
- prior P2X head `6d13e1e88643e77ae076336dd8ddb20ee1cd6b3f`

## EE-P2X-RV — adopted PASS

HQ adopts governed EE-P2X-RV PASS at:

`320a7098707d0110db8e59f9638e2057ccb27969`

Terminal:

`EE_P2X_RECEIPT_AND_VERIFIER_SURFACE_READY__LOCAL_EXECUTOR_REDUCED_TO_MEASURE_RUN_VERIFY_COMMIT`

Governed qualification:

- workflow run `35324632723`;
- job `105534740675`;
- evidence execution `d7bcf77768203a10d118f19f0235c02c822087fe`;
- semantic candidate `5540c6c586d5d7ebdbe37814a6e51d64bcc8c06c`;
- protocol self-tests `20/20 PASS`;
- commissioned inner suite `40/40 PASS`;
- governed outer court `1/1 PASS`;
- artifact ID `10539056299`;
- artifact ZIP SHA-256 `8b66f78ef41aa9cae01be03f0d1acde66da194843889870775aa5038fda84eb4`;
- transient PR `#389` closed without merge.

Live GitHub workflow recheck confirmed the run and job completed successfully at the stated evidence execution SHA.

## Qualified receipt/verifier surfaces

Preserved proposal blobs remain exact:

- `09_LOCAL_COURT_FROZEN_EXPECTATIONS.json` -> `1e336d0c7700997819876d6a5faa65389baf5dc3`
- `10_LOCAL_COURT_RECEIPT_CONTRACT.json` -> `7e729e6934fea270bf7d180faeeec33877e89fcf`
- `10A_COURT_RUN_MANIFEST_CONTRACT.json` -> `2d2293171167317338c39c57b848bec33e5f8aac`
- `11_seed_ee_p2x_local_receipts.py` -> `694d751fcb4cbaf59250532ce1261c25fcc4b9e1`
- `12_verify_ee_p2x_local_court.py` -> `4394bb61beba08259349cac3afbfa599f9f1a9aa`
- `13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json` -> `15cc59fe96c00a7178e0d9c318903e64c9e1d118`
- `rawlsing_next/tests/test_ee_p2x_local_court_receipts.py` -> `94cb87c0eaf812a430f73c1aa15e6233d3afa9e7`

Only the executor README changed from the proposal because the prior text predated the now-adopted reducer and driver:

- `LOCAL_EXECUTOR_README.md` -> `b6b9e29cf6bbc19de79fe431672ed33f5d18fd0a`

Additive driver-bound surfaces:

- `10B_DARWIN_DRIVER_RECEIPT_BINDING.json` -> `50c9a53d0d77131df7c619114b476afce0b0bb0f`
- `11A_sync_ee_p2x_driver_manifest.py` -> `1a3124e801654b07d1f2c77af61c9e11ffcc4b40`
- `12A_verify_ee_p2x_driver_bound_local_court.py` -> `da8f3434f791c9f6495238b28817de4b3e328ad3`
- `test_ee_p2x_local_court_driver_integration.py` -> `eb9fe9184e569ced70661d2f9eaf247f53b7267f`

Governed return evidence:

- `WORKER_RETURNS/EE-P2X-RV/00_RETURN.md` -> `23324de71bd900a4eaf32fc67dfe013c6e9b2e42`
- `01_BROWSER_QUALIFICATION_RECEIPT.json` -> `a2f5a5d9dbee0bc91b80d229ae99e1b490e97e5b`
- `02_PROPOSAL_BLOB_REQUALIFICATION.json` -> `b84fafdcd601d5dfeba646aa97aca7a633cd3eb2`

## Selective qualified fan-in to existing P2X

HQ preserves the existing measured-court branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

and advances it by one selective two-parent fan-in commit:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

Parents in order:

1. prior qualified P2X head `6d13e1e88643e77ae076336dd8ddb20ee1cd6b3f`;
2. EE-P2X-RV governed PASS `320a7098707d0110db8e59f9638e2057ccb27969`.

The fan-in imports only the qualified local receipt/verifier surfaces and governed return evidence required by the measured court. Transient qualification court machinery is not imported.

## Local Darwin execution wake

The browser-preparation coordination hold is now satisfied and lifted.

Existing EE-P2X measured execution is authorized to resume from:

`32e224c28d720fce7cdcf6182afb5d327e8a1cf0`

using the existing EE-P2X commission and the exact adopted reducer/driver/receipt-verifier surfaces now present on that branch.

First unfinished measured stage remains:

`LITS_I/A/S02_C11_REACHABILITY`

The local executor must:

- use the exact qualifying Darwin x86_64 / CPython 3.11.3 / `pyreadstat==1.3.6` / `pyarrow==25.0.1` host contract;
- verify exact LiTS-I and WVS7 source SHA-256 before source use;
- use the qualified driver modes and durable stage ledger;
- never repeat the banked LiTS-A qualifying first build;
- never repeat the banked LiTS-B standalone cacheless C11 stage;
- preserve WVS-C as `WVS7_C__CURRENT_PORTABILITY_FAILURE` with no executable fallback;
- run the driver-bound verifier `12A_verify_ee_p2x_driver_bound_local_court.py`;
- capture exact supervisor tokens after measured-host stages and commit/push through the existing bounded P2X protocol;
- stop on the exact smallest typed blocker/failure if encountered;
- never rank or select A/B/C.

Successful final evidence terminal remains:

`PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE`

and lawful complete EE-P2X return wakes:

`HQ_MEASURED_SYNTHESIS`

## Preserved prohibitions

Lock1 and Lock2 remain unchanged. No browser-side carrier access or performance measurement was performed by HQ.

No new WVS accelerator, no third CACC, no golden path, no surrogate performance, no cross-universe pooling, no MAIN mutation, and no semantic PRE-MAIN mutation are authorized.

Measured HQ synthesis remains forbidden until the local EE-P2X court returns complete lawful evidence.

Terminal:

`EE_P2X_BROWSER_PREPARATION_COMPLETE__LOCAL_DARWIN_P2_EXECUTION_AUTHORIZED`
