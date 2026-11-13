# Independent G5 re-receiving handoff

**Authoritative subject:** the exact HEAD containing this return and the D1 fix. Verify with `git rev-parse HEAD`; do not use the prior PR #976 head as the repaired subject.

## Required independent checks

1. Verify the HEAD is the base `37c5842e04892421c9ce74a39956c3cdcf57f0f5` plus the D1 fix and return files only.
2. Verify `git diff 37c5842e0 HEAD -- WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1` contains only the `situated.py` binding.
3. Run the full 37-test suite using the receiver's own frozen probes, not a copied file.
4. Run the committed G5 stale-receipt probe and the author regression `test_receipt_currentness.py`.
5. Try at least one independent variation of the stale receipt (for example old interval unchanged, or a forged receipt with a changed interval) and classify it separately.
6. Decide whether the residual direct-caller receipt-forgery boundary is an integration hold. The author only claims D1 fixed, not authenticated receipt provenance.

## Expected

- 37/37 pass.
- G5 stale-receipt probe passes after the repair.
- Author regression passes.
- A current receipt still authorizes; an old authentic receipt does not.
- No owner, readset, source-custody or scientific claim changes.

## Evidence

`evidence/37_tests_fixed.log`, `evidence/repair_tests.log`, `evidence/DIFF.patch`, `evidence/SHA256SUMS`. The receiver's frozen evidence at `c597024` is unchanged.
