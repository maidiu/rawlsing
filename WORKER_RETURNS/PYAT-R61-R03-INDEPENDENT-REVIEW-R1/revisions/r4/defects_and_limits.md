# R61-R03V R4 remaining failure and limits — REVISE

Verdict: **REVISE**. The fixed-original-pin cold restore is real and all three
prior cold fact/job fault probes now refuse against the genuine original pin.
The remaining gap is at the live capture boundary: `freeze_restore_checkpoint`
trusts anti-join flags and nonempty refs instead of running the shared
structural/closure/multiplicity validation, so an incomplete/forged result can
acquire a checkpoint.

## Remaining failure — live checkpoint capture is not fully validated (blocking)

**Contract:** R61AV requires the live result capture interface to verify the
actual result has successful candidate/operation no-drop, eligible accounting,
complete expected operation/job/candidate mapping, native receipt/fact closure
and valid multiplicities, then return the canonical whole-result checkpoint. A
failed/incomplete result must not acquire an accepted-completed checkpoint.
Share existing validation rather than trust flags.

**Observed:** `GovernedFrontierResult.freeze_restore_checkpoint()` checks only
`anti_join["no_drop_ok"]`, `operation_anti_join["no_drop_ok"]`, nonempty
expected operation IDs, nonempty issued expected jobs, and nonempty
receipt/fact refs. It does not validate the operation ledger rows, expected
candidate mapping, native receipt/fact closure or fact multiplicity.

**Repro (H4):** take a genuine passing result and replace `operation_ledger`
with `()` while leaving all flags/refs intact; `freeze_restore_checkpoint()`
returns a canonical checkpoint instead of refusing. Repro (H4b): duplicate a
`fact_refs` entry and capture; it also returns a checkpoint. A later restore
with that pin may fail structural validation, but the capture interface has
already blessed an incomplete/invalid result, contrary to the required
failed-result refusal.

**Required minimal function:** before returning the checkpoint, run the same
structural/closure/expected-mapping/multiplicity validator used by the cold
path (or an equivalent shared helper that does not require an external pin) on
`self.ledger()`. Refuse when operation rows, expected candidates/jobs, receipt/
fact closure, duplicate native fact identities or fact multiplicities are
invalid.

## Fixed R3 requirements (retained)

- Genuine original-pin restore passes; missing and wrong pin refuse.
- The three prior coordinated cold probes (single native fact deletion, native
  fact duplication, expected query/predicate job substitution) all refuse
  against the genuine original pin, with genuine restore between faults.
- A content mutation retaining advertised refs refuses against the original
  pin; missing pin refuses before release.
- Author R4 suite 15 passed; retained R01 suite 32 passed.
- Governed joint/conditional/D3/root-parent/minority/pending/source-value and
  HELD/UNKNOWN positives remain; U43 blob
  `31e84f49d624f5524906e9e7839d2873106f8249` exact; four-path scope and
  U43/binding/R01/R02/native owners unchanged.
- Fresh-process genuine restore and no native rerun/budget charge are covered
  by the author suite and the reviewer's fixed-pin positive.

## Limits / not reached

Sourcefree TEST_ONLY local trusted host only; no source respondent access. Both
pin and candidate replaced by a different trusted host is the R61AF excluded
boundary. R04 joined custody/durability, R05 lifecycle/grades, F5-F8 global,
original35/1890 N11, N12/Sorok, protected CI/production and J52/W52 remain
NOT_REACHED. No candidate repair, self-adoption, new worker, cryptographic
issuer or production merge.
