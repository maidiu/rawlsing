# First fault

The first test execution failed before collection of the N10E/FF01 cases because
three exact historical synthetic-authority fixtures were absent from the sparse
C6 worktree:

- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/02_VALUE_RELATION_ORACLE.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/03_SYNTHETIC_AUTHORITY_FREEZE.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2/04_SLICE_PROJECTION.json`
- `WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3/02_OWNER_NATIVE_AUTHORITY_SCOPE_FREEZE.json`

They were recovered exactly from `refs/anvil-p0/c6` into a scratch/test-only
worktree location. No product file, frozen runtime, protected ref, source data,
or original respondent record was changed. After exact recovery, all 131 tests
passed.

This is a missing test-fixture checkout fault, not a product-code defect.
