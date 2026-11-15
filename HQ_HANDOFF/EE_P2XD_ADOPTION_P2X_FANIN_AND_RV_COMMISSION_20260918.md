# EE-P2XD ADOPTION, P2X QUALIFIED FAN-IN, AND EE-P2X-RV COMMISSION — 2026-09-18

Status: `ADOPTED__P2XD_QUALIFIED_FANIN_COMPLETE__EE_P2X_RV_COMMISSIONED`

Decision: `HQD-2026-09-18-037`

## Predecessor authority

- checkpoint `20260918T0317-0400`
- immutable handoff `ac722a9952b792e0fd43b5fbf28ca98b6d0c1e87`
- semantic PRE-MAIN `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`
- prior P2X head `a954e2d6676843da8427ef2439b5d1ef33478359`

## EE-P2XD — adopted PASS

HQ adopts governed EE-P2XD PASS at:

`2a26306c990b6d16bbe5ca90807ae7db59b687e6`

Terminal:

`EE_P2X_DARWIN_MECHANICAL_COURT_DRIVER_READY__NO_EMPIRICAL_MEASUREMENT_PERFORMED`

Qualified implementation:

`rawlsing_next/ee_p2x_darwin_court_driver.py`

Git blob:

`c3a368270f6f7a6f613efb78e31972e64a092c88`

Hostile test blob:

`53ab07f00f23b6d5d8d8b67d8974de7bebc61488`

Qualification receipt:

`WORKER_RETURNS/EE-P2XD/01_BROWSER_QUALIFICATION_RECEIPT.json`

blob:

`15aec674df941a16d77df513d4bd9d571ff1daf6`

Governed qualification:

- hostile browser court `19/19 PASS`;
- protocol self-tests `20/20 PASS`;
- governed bounded court `1/1 PASS`;
- workflow run `35321826151`;
- job `105525800028`;
- semantic candidate `d69ebc3767461b110721d6acfcf3b9b373c92bab`;
- evidence execution `10d9920d7ec69d86231acb02a4391155b1da288e`;
- artifact ID `10537033071`;
- artifact ZIP SHA-256 `f8573fa73c1a656e5e0f04aec5416d4dffe07bfba3048e6732253f6597e67e57`;
- transient PR `#387` closed without merge.

Live GitHub workflow recheck confirmed run/job completed successfully at the stated evidence execution SHA.

## Selective qualified fan-in to existing P2X

HQ preserves the existing measured-court branch:

`agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1`

and advances it by one selective multi-parent fan-in commit:

`6d13e1e88643e77ae076336dd8ddb20ee1cd6b3f`

Parents in order:

1. preserved P2X head `a954e2d6676843da8427ef2439b5d1ef33478359`;
2. EE-P2XD governed PASS `2a26306c990b6d16bbe5ca90807ae7db59b687e6`;
3. adopted reducer governed PASS `eb7595f1030d1861c262dbdb6bb4d7c12d1abd43`.

Selective imported surfaces:

- `rawlsing_next/ee_p2x_darwin_court_driver.py` blob `c3a368270f6f7a6f613efb78e31972e64a092c88`;
- `tests/test_ee_p2x_darwin_court_driver.py` blob `53ab07f00f23b6d5d8d8b67d8974de7bebc61488`;
- EE-P2XD governed return/qualification receipt;
- adopted reducer `00_RETURN.md`, continuation map and Darwin guide.

The transient `.rabochii/court_spec.json` and qualification-only bridge were not imported into P2X.

The continuation map remains exact:

- path `WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json`;
- Git blob `e06e95dd370a4fd44235932088308c3372522ed4`;
- exact-byte SHA-256 `ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422`.

## Receipt/verifier proposal preservation and requalification

HQ recovered the prior non-operative receipt/verifier proposal tree:

`acf744527f945ec80a2d09c2eb9d054a3c4f23fb`

and materialized its exact proposed receipt/verifier blobs unchanged on a bounded preparation branch from the new P2X head.

Preparation branch:

`agent/rabochii-prev3-ee-p2x-rv-local-receipt-verifier-preparation-r1`

Materialized proposal commit:

`a842a067636af2836172222cea9f5b1367bcce63`

Commission tip / current head:

`db88478a9ae3f0e73aa9bf6eb7091a6dcc598171`

Commission:

`WORKER_COMMISSIONS/EE-P2X-RV/00_COMMISSION.md`

Grain:

`EE_P2X_LOCAL_COURT_RECEIPT_VERIFIER_PREPARATION_ONLY`

Library/source access:

`NO`

The worker is not to redesign the receipt packet. It must requalify the existing proposal against the actual adopted reducer and actual qualified driver interface, preserving unchanged blobs wherever compatible and repairing only proved interface/authority mismatches.

PASS terminal:

`EE_P2X_RECEIPT_AND_VERIFIER_SURFACE_READY__LOCAL_EXECUTOR_REDUCED_TO_MEASURE_RUN_VERIFY_COMMIT`

## Execution hold

The previous P2XD coordination hold is satisfied by fan-in `6d13e1e...`.

A narrower final browser-preparation hold now applies:

`DO_NOT_BEGIN_NEW_LOCAL_MEASURED_CONTINUATION_UNTIL_EE_P2X_RV_ADJUDICATED_AND_QUALIFIED_RECEIPT_VERIFIER_FANIN_BOUND`

This is not a redesign or new prerequisite on the scientific court. It is an execution-safety coordination hold to finish the already-built deterministic evidence surface before the local runner starts.

Lock1 and Lock2 remain unchanged. No source bytes were accessed and no performance was measured in this HQ action.

Measured HQ synthesis remains forbidden until lawful complete EE-P2X return.

Terminal:

`EE_P2XD_ADOPTED__QUALIFIED_DRIVER_AND_MAP_FANIN_BOUND__EE_P2X_RV_ACTIVE`
