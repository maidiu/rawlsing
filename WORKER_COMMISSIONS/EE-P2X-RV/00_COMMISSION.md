# EE-P2X-RV — LOCAL COURT RECEIPT / VERIFIER PREPARATION REQUALIFICATION

Status: `COMMISSIONED__BROWSER_REQUALIFICATION_ONLY__NO_EMPIRICAL_EXECUTION`

Repository: `maidiu/rawlsing`

Exact branch:

`agent/rabochii-prev3-ee-p2x-rv-local-receipt-verifier-preparation-r1`

Materialized proposal base commit:

`a842a067636af2836172222cea9f5b1367bcce63`

Exact inherited P2X base:

`6d13e1e88643e77ae076336dd8ddb20ee1cd6b3f`

This is a browser preparation/requalification lane only. It SHALL NOT execute the measured court, move the active P2X branch, rebase, or replace P2X.

## Controlling inputs

### Adopted continuation map

- reducer return: `eb7595f1030d1861c262dbdb6bb4d7c12d1abd43`
- path: `WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json`
- schema: `RAWLSING_EE_P2X_CONTINUATION_STATE_MACHINE@1.0.0`
- Git blob: `e06e95dd370a4fd44235932088308c3372522ed4`
- exact-byte SHA-256: `ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422`

### Qualified Darwin driver

- EE-P2XD PASS: `2a26306c990b6d16bbe5ca90807ae7db59b687e6`
- fan-in P2X head: `6d13e1e88643e77ae076336dd8ddb20ee1cd6b3f`
- path: `rawlsing_next/ee_p2x_darwin_court_driver.py`
- Git blob: `c3a368270f6f7a6f613efb78e31972e64a092c88`
- hostile test blob: `53ab07f00f23b6d5d8d8b67d8974de7bebc61488`
- browser qualification receipt blob: `15aec674df941a16d77df513d4bd9d571ff1daf6`
- governed run: `35321826151` / job `105525800028` / success

### Prior non-operative receipt/verifier proposal

Original unreferenced tree:

`acf744527f945ec80a2d09c2eb9d054a3c4f23fb`

The exact proposed receipt/verifier blobs were materialized unchanged onto this branch at `a842a067636af2836172222cea9f5b1367bcce63`.

## Mission

Requalify the already-built receipt/schema/verifier packet against the **actual adopted continuation map and actual qualified Darwin driver interface**.

Do not redesign the court or rewrite the packet merely for style. Preserve exact proposal blobs wherever they remain compatible. Change only what is required by a proved interface, authority, or deterministic-verification mismatch.

Required proposal surfaces to inspect and qualify:

- `WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json`
- `WORKER_RETURNS/EE-P2X/10_LOCAL_COURT_RECEIPT_CONTRACT.json`
- `WORKER_RETURNS/EE-P2X/10A_COURT_RUN_MANIFEST_CONTRACT.json`
- `WORKER_RETURNS/EE-P2X/11_seed_ee_p2x_local_receipts.py`
- `WORKER_RETURNS/EE-P2X/12_verify_ee_p2x_local_court.py`
- `WORKER_RETURNS/EE-P2X/13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json`
- `WORKER_RETURNS/EE-P2X/LOCAL_EXECUTOR_README.md`
- `rawlsing_next/tests/test_ee_p2x_local_court_receipts.py`

## Exact requalification burden

Prove that the packet:

1. consumes the exact reducer stage/cell vocabulary and does not invent stage transitions;
2. is compatible with the driver's ledger, receipt, supervisor-token, `--preflight`, `--status`, `--run`, `--resume`, and `--verify-only` surfaces;
3. treats `DONE__PRESERVE` stages as non-executable and rejects attempted repetition of LiTS-A qualifying first build and LiTS-B standalone cacheless C11;
4. handles every attempted cell with a typed source×candidate receipt, including failed cells;
5. uses `NOT_REACHED_AUTHORIZED_STOP` rather than fabricated zeroes for metrics not reached under a lawful stop;
6. preserves WVS-C as non-executed `WVS7_C__CURRENT_PORTABILITY_FAILURE`, with no fallback and no source open for Candidate C;
7. binds the exact LiTS 50-candidate / 77-role learned-product and semantic replay identities;
8. binds exact WVS Lock2, replay, DiscoveryAuthority, candidate grammar, 46-candidate frontier, 11 predicates, 3 queries, and family shape `10/1/10/25`;
9. enforces parity/oracle-before-performance and candidate-neutral oracle identity;
10. enforces B/C P4+P5 deletion with P1/P2/P3 retention and identity-equivalent regeneration where constitutionally applicable;
11. enforces A information-authority vs operational-persistence vs rebuild-cost separation and forbids `EXPENSIVE_TO_REBUILD -> AUTHORITATIVE`;
12. rejects historic-product substitution as fresh output;
13. rejects Lock1/Lock2 drift, post-outcome WVS frontier mutation, ranking, scoring, selection, recommendation, or cross-universe metric pooling;
14. proves final evidence completeness over all six ordered cells while accepting authorized candidate-local terminal failures;
15. emits only `PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE` or the deterministic smallest exact blocker/failure disposition.

Where the driver produces raw stage receipts or ledger entries, the verifier must consume their actual schema/field names rather than a guessed interface.

## Qualification

Run the existing bounded receipt tests and add/repair only the minimum driver-integration tests needed to prove the interface above.

At minimum run:

`PYTHONHASHSEED=0 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3.11 -m pytest -q rawlsing_next/tests/test_ee_p2x_local_court_receipts.py tests/test_ee_p2x_darwin_court_driver.py`

If repository-governed qualification infrastructure is applicable, invoke the canonical governed bounded court and bank its receipt. Do not represent browser timing as candidate performance.

## Outputs

Keep final local-executor receipt/verifier surfaces under:

`WORKER_RETURNS/EE-P2X/`

Write preparation return evidence only under:

`WORKER_RETURNS/EE-P2X-RV/`

Required preparation return:

- `WORKER_RETURNS/EE-P2X-RV/00_RETURN.md`
- exact browser qualification receipt;
- deterministic record of any proposal blobs changed and why.

## Hard prohibitions

- no empirical carrier access;
- no Library carrier bytes;
- no measured P2X execution;
- no synthetic or surrogate candidate performance;
- no pre-populated measured values;
- no Lock1 or Lock2 mutation;
- no candidate/workload redesign;
- no WVS accelerator;
- no third CACC;
- no ranking, scoring, recommendation, or selection;
- no MAIN or semantic PRE-MAIN mutation;
- no P2X branch movement;
- no rebase;
- no replacement branch.

## PASS terminal

`EE_P2X_RECEIPT_AND_VERIFIER_SURFACE_READY__LOCAL_EXECUTOR_REDUCED_TO_MEASURE_RUN_VERIFY_COMMIT`

PASS wakes HQ adjudication and selective fan-in of the qualified receipt/verifier packet to the existing P2X branch. It does not by itself authorize local measured continuation.
