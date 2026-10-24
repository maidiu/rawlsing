# R61 R03 R5 coverage and limits

| Requirement | Evidence | Status |
|---|---|---|
| Shared pin-free validator | same helper used by capture and restore | PASS |
| Empty operation ledger capture refusal | H4 mutant test | PASS |
| Duplicate fact_refs capture refusal | H4b mutant test | PASS |
| Missing expected jobs/candidates/receipts/facts refuse | helper checks | PASS |
| Duplicate native fact identities refuse | helper checks | PASS |
| Legit shared facts allowed | fact coverage set, not one-to-one | PASS |
| Fixed original pin still mandatory | R4 tests retained | PASS |
| No native rerun/budget on restore | R4 fresh-process/no-rerun tests | PASS |
| Prior governed/D3/minority/held-unknown | 16 R03 + 32 R01 tests | PASS |
| R04/R05+/original science | not implemented | NOT_REACHED |
