# No-drop and typed outcome evidence

`operation-status-inventory.json` was computed from the actual full generated
four-item frontier ledgers. Original operation identities were retained.

| Direction | All operations | SUPPORTED results | VALID_EMPTY results | HELD results | UNSUPPORTED results |
| --- | ---: | ---: | ---: | ---: | ---: |
| Forward | 177 | 39 | 42 | 93 | 3 |
| Reverse | 499 | 1 | 246 | 251 | 1 |

Both exact operation anti-joins have `no_drop_ok=true`; native reverse facts
include 72 ZERO_SUPPORT facts. A VALID_EMPTY discovery-validation result is not
a declaration that the underlying measured conditional fact lacks support;
the two typed layers remain separately recorded. No empty result is counted as
positive downstream evidence.

The retained 48-test grammar/workload suite additionally exercises explicit
budget PENDING operations, NOT_ELIGIBLE lowering, UNSUPPORTED_RUNTIME, held and
UNKNOWN ledger preservation, wrong edition and count-preserving substitution,
source-value mutation and restoration, minority/D3 and cold checkpoint checks.
`baseline.log`: 48 passed. The source projection suite: 31 passed, including
administered=false hold, respondent/exposure tuple identity, duplicate/ambiguous
occurrence maps, normalized identities, source-label alternatives, missingness,
MR/rank/form consumption and same-consumer mutation/restore.

These retained tests do not waive the new C1 joint-fact selection RED or prove
that every L02 hostile mutation has reached the final N10E assertion. That
combined-chain matrix remains outstanding.
