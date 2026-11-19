# SRC16 saved Batch predicate-binding repair

## Verdict

**FIXED_SCOPED.** The exact changed-predicate stale-cache defect is repaired in
the existing `execute_saved_batch` patch.

## Exact behavior

Before any cached unit is skipped, every QUERY unit's supplied
`predicate_ref_by_query` must be present in that unit's exact
`semantic_input_refs`. Otherwise the existing saved Batch boundary raises
`SavedC11AdmissionError("SAVED_BATCH_PREDICATE_BINDING_MISMATCH")`.

The validated prior-output cache still uses the existing
`_validate_prior_cache`; no new issuer, no Batch semantics, no I03/I05 edit.

## Independent RED/GREEN

- Prior patch: changed predicate map accepted, exact cached receipts reused,
  `COMPLETED`.
- Fixed patch: changed predicate map **refused** with
  `SAVED_BATCH_PREDICATE_BINDING_MISMATCH`.
- Exact prior outputs and same mapping: **3/3 records equal**, `COMPLETED`.
- Changed prior output: `PRIOR_OUTPUT_KIND_MISMATCH`.
- Partial/deferred receipt: retained; only its unit reexecuted.
- Forged completed receipts: discarded and reexecuted.
- Revoked authority: `DirectEstateError`.
- Normal/no-prior-cache path unchanged.

## Files

- `execute_saved_batch_prior_cache.patch` — pinned final patch.
- `PREDICATE_FIX_GREEN.json` — independent fixed review output.
- `PRIOR_PATCH_CHANGED_MAP_ACCEPTED.json` — prior residual defect.
- `PATCH_APPLY_CHECK.txt` — clean apply check.
- `PREDICATE_FIX_REPORT.json`, `REPORT.json`, `MANIFEST.json`.

Sourcefree only. Original data, live runner, frozen runtime, protected refs,
I03/I05, real GSS and DHIKR untouched.
