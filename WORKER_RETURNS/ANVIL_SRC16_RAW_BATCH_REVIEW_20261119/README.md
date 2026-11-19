# SRC16 saved Batch independent review

Sourcefree independent review of OWNER's exact saved-Batch patch.

## Pinned inputs

- IMPLEMENTER `0dcd75749e5c186842a70dec777096b3f22086d8`
- MEASUREMENT_PREP trace `aa9e91d58b24ea4366a902fb16ba110b566edd5d`
- OWNER return `e3d911364b06ac1d4dec28801d1db56eb6bcf389`
- OWNER patch SHA-256:
  `9cda4d5bba659f6b0b69990d6b66f85451471355d773798fb9bb7b8e075a29e4`

The patch was applied unchanged to an isolated copy of
`rawlsing_next/pre553_saved_workload_integration.py` from the pinned
IMPLEMENTER commit. No product tree, live runner, frozen runtime, original
data, or DHIKR was touched. No discovery/I05 patch was applied for this review.

## RED

On the unpatched pinned tree, three completed prior receipts whose
`result_refs` were replaced with an `EmpiricalPredicate@1.0.0` ref were all
retained. Batch returned `COMPLETED` without reexecution.

## GREEN

On the patched isolated copy, the same forged completed prior receipts were
discarded and all three units were genuinely reexecuted. The summary remained
`COMPLETED` because execution occurred.

## Exact cache reuse

Supplying the exact prior outputs keyed by current unit hashes passed
`_validate_prior_cache`; the same three receipt hashes were returned with no
changed records and `COMPLETED` coverage.

Reuse is bound by:

- current manifest hash and exact batch-unit refs;
- exact prior output keys equal to current unit hashes;
- exact native result refs matching the supplied prior output facts/receipts;
- current saved-estate/operation authority (`DirectEstateError` on revocation).

Changed prior output is refused: `PRIOR_OUTPUT_KIND_MISMATCH`.

## Exact residual defect

A changed `predicate_ref_by_query` mapping was accepted while exact prior
outputs and receipts caused every completed unit to be skipped. The returned
receipts were the old positive results, and Batch reported `COMPLETED`; the
changed predicate was not validated or reexecuted. The saved Batch unit does
carry predicate refs in `semantic_input_refs`, but `execute_saved_batch` does
not compare the supplied mapping to those refs before accepting the prior
cache.

## Legitimate partial resume

A DEFERRED prior receipt was retained; only that unit was reexecuted on
attempt 2. The summary completed with the deferred receipt preserved. No
defect was observed on that path.

## Verdict

`ACCEPT_SCOPED_WITH_EXACT_RESIDUAL_DEFECT`: OWNER's patch fixes forged
completed-receipt reuse, exact validated cache reuse, changed-output refusal,
and genuine partial resume. The changed-mapping reuse remains an exact defect
outside the patch's current validation.
