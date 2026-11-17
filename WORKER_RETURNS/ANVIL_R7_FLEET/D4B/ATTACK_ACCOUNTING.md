# ATTACK_ACCOUNTING — exact H00..H13 reconciliation

Source of truth: `MUTATION_TESTS/REPORT.json` (`accounting` block) and
`HOSTILE_ATTACK_MATRIX.tsv`. No attack was re-executed for this correction;
counts are a reclassification of the preserved 14 rows.

| Class | Rows | Count | Supplied result |
|---|---|---|---|
| Clean baseline | H00 | 1 | PASS at FRAME/DECISION/C |
| Clean restore | H13 | 1 | PASS at FRAME/DECISION/C after all mutations |
| Hostile mutation, gate target | H02–H11 | 10 | **10/10 PASS** |
| Hostile mutation, transfer helper target | H01 | 1 | `PASS_TRANSFERRED` |
| Hostile mutation, defended positive control | H12 | 1 | RED (`FALSE_PROSPECTIVE_ADOPTION`) |
| **Hostile mutations total** | H01–H12 | **12** | **11 pass their target, 1 defended** |
| **All rows** | H00–H13 | **14** | 12 supplied PASS/PASS_TRANSFERRED, 2 RED (H12, and H13 is clean) |

Correct sentence for the return: **"11 of 12 hostile mutations pass the
component they target; 10 of 11 gate-targeted mutations pass; only the literal
K3 NOT_ADOPTED boolean is defended."** The earlier phrases "12 of 13" and "ten
distinct sabotages" were wrong and are withdrawn.

Strict overlay: H01–H12 become RED (12/12); H00 and H13 remain PASS. The overlay
is authored private-package evidence, not independent C.
