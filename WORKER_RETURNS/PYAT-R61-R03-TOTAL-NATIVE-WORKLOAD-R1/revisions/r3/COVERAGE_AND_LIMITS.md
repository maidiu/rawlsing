# R61 R03 R3 coverage and limits

| Defect | Repair | Test | Status |
|---|---|---|---|
| 1 cold stripped ledger | expected jobs/candidates/compilation/native identity closure | strip/rehash refusal | PASS |
| 2 live fact ref removal | adapter fact closure; owner unchanged | removed fact ledger refusal; adapter closure | PASS at R03 consumer |
| 3 expected jobs/typed rows restore | ledger fields + restore checks | persistence/deletion test | PASS |
| 4 recursive root release severance | snapshot/root/release equality | severance refusal, baseline pass | PASS |
| 5 HELD/UNKNOWN collapse | eligibility_field + typed result states | live and cold row test | PASS |
| Retained native positives | unchanged governed D3 | R03 13 + R01 32 | PASS |
| Owner anti-join direct H2 | owner unchanged by commission | old direct probe still old result | DECLARED BOUNDARY |
| R04/R05/R06/R07/N11/N12 | not implemented | NOT_REACHED | HOLD |
