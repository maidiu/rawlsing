# R91 R04_JOINED coverage and limits

| Requirement | Evidence | Status |
|---|---|---|
| Actual R03-issued workloads consumed | `compile_universal_workload` objects in custody tests | PASS |
| Partial sequence checkpoint | first completed workload captured, remaining resumed | PASS |
| No reexecution completed units | source-factory call count == pending count; completed refs retained | PASS |
| Exact uninterrupted equality | combined output refs and receipt materials equal | PASS |
| Fresh-process cold resume | checkpoint loaded, R03 workloads rebuilt, remaining executed | PASS |
| Current grant recheck | revoked record refuses before native | PASS |
| Source identity recheck | wrong source SHA refuses | PASS |
| No double accounting | unique decision refs/checkpoint closure | PASS |
| Byte decoder rewrite | none; accepted R04.byte reused read-only | NOT_APPLICABLE |
| Global durable exactly-once/anti-fork | not claimed | NOT_REACHED |
| R05+/original science/CI/prod/N11/N12/Sorok/J52-W52 | not implemented | HOLD |
