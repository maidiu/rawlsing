# R61 R03 R4 coverage and limits

| Requirement | Evidence | Status |
|---|---|---|
| Live validated capture | `freeze_restore_checkpoint`; failed result refusal | PASS |
| Mandatory external original pin | missing-pin refusal; genuine pinned restore | PASS |
| Pin equals canonical whole-result hash | self-hash + pin equality | PASS |
| Fact deletion/duplication refuse with original pin | hostile tests | PASS |
| Expected job/predicate substitution refuses | both mutable copies + recomputed hashes | PASS |
| No native rerun/new budget on restore | restore-only path; fresh-process test | PASS |
| Prior governed/native positives | 15 R03 + 32 R01 tests | PASS |
| Owner `native_receipt_anti_join` unchanged | exact U43/native blobs | PASS |
| R04/R05+/original science | not implemented | NOT_REACHED |
