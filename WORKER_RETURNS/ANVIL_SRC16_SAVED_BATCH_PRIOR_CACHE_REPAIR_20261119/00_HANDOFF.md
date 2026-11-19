# SRC16 saved Batch prior-cache repair

## Verdict

**ACCEPT_SCOPED.** The observed stale/unbound prior-receipt admission is repaired
only in `execute_saved_batch`.

## Patch

`execute_saved_batch_prior_cache.patch` changes
`rawlsing_next/pre553_saved_workload_integration.py`:

- Adds optional exact `prior_outputs`.
- When supplied, invokes the existing `_validate_prior_cache` against the current
  manifest and exact native output refs.
- When trusted prior outputs are absent, completed prior receipts are discarded
  and the units are reexecuted. Partial/absent receipts remain for legitimate
  resume.

No new issuer, no receipt-as-authority shortcut, no Batch semantics change, and
no discovery edits.

## Evidence

- Baseline trace: forged completed prior receipts were retained.
- Patched trace: **all_forged_receipts_retained = false**; three actual execution
  receipts; summary remains `COMPLETED` because the units were genuinely
  reexecuted.
- Same-root exact reuse probe: 3/3 receipt records equal, summary `COMPLETED`.
- Changed prior output: refused with `PRIOR_OUTPUT_KIND_MISMATCH`.
- Patch dry-run against exact base: PASS.

The first discovery discrepancy (`UNRESOLVED` mapped to
`EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY`) remains for the separate discovery
owner and was not edited.

No original source, private census, frozen runtime, real survey, Field Forge, or
DHIKR was used.
