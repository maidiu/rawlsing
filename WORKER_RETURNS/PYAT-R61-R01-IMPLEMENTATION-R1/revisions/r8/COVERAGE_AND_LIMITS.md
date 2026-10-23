# R61 R01 R8 coverage and limits

| Defect | Repair | Evidence | Status |
|---|---|---|---|
| H1 target label mismatch | target label checked against query/source inventory | create refusal test | PASS |
| H2 query target mismatch | same shared validator | create refusal test | PASS |
| H3 condition key/value/predicate mismatch | response leaf question/value binding | create/restore refusal tests | PASS |
| Question/predicate mismatch | question ref in inventory + occurrence label match | create refusal test | PASS |
| H4 malformed condition key | typed `OccurrenceKey` validation before planning | issue refusal test | PASS |
| H5 duplicate condition refs | typed duplicate refusal; planner ValueError converted | issue refusal test | PASS |
| Form/repeat occurrence variant | same leaf identity allowed with qualified key | variant test | PASS |
| Preserve R7 owner positives | unchanged owner + 32-test suite | JUnit | PASS |
| R03/R04/R09/original science | not implemented/claimed | NOT_REACHED | HOLD |
