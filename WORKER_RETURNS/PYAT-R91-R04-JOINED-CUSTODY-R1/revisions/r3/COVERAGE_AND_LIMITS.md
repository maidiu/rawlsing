# R91 R04_JOINED R3 coverage and limits

| Requirement | Evidence | Status |
|---|---|---|
| Query output identity retained | restored QueryExecutionResult query_ref/facts/releases equal original | PASS |
| Discovery output identity retained | RetainedDiscoveryResultView frontier/replay/fact/receipt equality | PASS |
| Checked immutable view | frozen dataclass, ordering/closure validation, mutation raises | PASS |
| Partial output restoration | same constructors feed prior_outputs/Batch resume | PASS |
| External pin/manifest/no rerun | R2 tests retained | PASS |
| R03 positives | 16 passed | PASS |
| R05+/original science/CI/prod/N11/N12/Sorok | not implemented | NOT_REACHED |
