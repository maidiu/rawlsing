# R91 R04_JOINED R2 coverage and limits

| Defect | Repair | Status |
|---|---|---|
| Actual R03 governed discovery rejected | capture accepts NativeDiscoveryExecution with facts/receipts/manifest | PASS |
| Self-hashed forged checkpoint accepted | original external pin required on restore/resume | PASS |
| Completed resume loses outputs/facts/manifest | original manifest + completed fact objects retained/rehydrated | PASS |
| No real partial multi-unit | partial max_units prefix captured/resumed, completed units not rerun | PASS |
| Revoked/wrong source | current admission/source checks before pending work | PASS |
| Fresh-process actual N+1 | full-prefix fresh-process resume retained; partial is in-process | PARTIAL |
| R03 positives | 16 passed | PASS |
| R05+/originals/CI/prod/N11/N12/Sorok | not implemented | NOT_REACHED |
