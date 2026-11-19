# SOROK REMONT SR-P005 R1 — reproducible material bugs, bounded source repair

**Parent:** PR #1165 \`480d3595ef744779cbfce186cd1696d8e8f61e36\` (latest SR-P004 candidate at verified cut), not earlier PR #1166.
**SEAM context:** Constitutive Organism R2 documentary synthesis PR #1161 \`b91d857202d8f84a4721cbc185b6d3aeac3349e3\`.
**Protected:** \`integration/pre-main-reconciliation-r1\` \`5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e\` as observed. No mutation.

## Reproduced sourcefree failures before repair
- At \`workshop\`, actor \`intruder\` used \`REPAIR\`: \`REPAIR_PERFORMED\`, stock 5→4 despite no material-use grant.
- At \`hall\`, board institution \`controls=hall\` but site lacked a \`controller\` label: \`REPAIR_PERFORMED\` and stock 2→1 for an ungranted visitor.
- With \`food_price=-3\`, \`BUY_FOOD\` produced \`FOOD_PURCHASED\` and credited +3 to the purchaser.
- With \`wage=-5\`, \`WORK\` produced controlled goods, debited worker -5 and credited employer +5.
- A mismatched controller site/issuer relation could be mistaken for unowned production.

## Fix at first material owner
- \`world.py\`: site and institutional controller reconciliation; ambiguous/mismatched controller fails closed; institutional stock consumption depends on \`material_use_grants\` held in objective world, not a cognitive claim or \`public\` site entry.
- \`world.py\`: finite nonnegative price/wage/controller-funds validation happens before any transfer or added stock.
- \`tests/test_sr005_material_guard.py\`: 8 regressions, including full runtime blocked \`REPAIR\` world+actor ledger/chain, positive authorized use, negative value side effects and failed controller reconciliation.

## Executed evidence
Before fix: independent direct reproductions of the three listed faults, plus hall omission; first test draft also had an **invalid test fixture** (empty pseudo-respondent answers), which was corrected and never counted as production error.
After fix: from original R2 package with the unchanged \`world.py\` base and 8 new regression tests, \`python -m unittest discover -s tests -v\`: **42 PASS / 0 FAIL**. Local world source Git blob \`2c122822d4bf115dbb4741b7fa75f43e1b0e4f04\`, test blob \`4d20203adc5681f7dec1f526c464a13bcb4e09c4\`, both exact GitHub blob readbacks. **Not a test run of stacked PR #1165 + patch together**; inherited #1165 39-test author result remains a separate statement. Native/independent tests pending.

## Open defects and authority
SR-P005 **PARTIAL**: actual wage arrears/owed compensation, formal worker/employment/grants, shift schedule and enforceable collective/institutional rights not yet modeled; this patch does not generate world authority for granting material use. Actor psychological uptake still subjective and not guaranteed to infer objective owner. The SEAM conceptual solution is not fully executable. All SR-P001..020, T0, E001..005 continue intact. No earned PYAT/source/P2–P6/CAN/ADP rights, independent review, science issuance or protected receiving; no paired CURRENT_PROGRESS rewrite without the authorized owner lease.
