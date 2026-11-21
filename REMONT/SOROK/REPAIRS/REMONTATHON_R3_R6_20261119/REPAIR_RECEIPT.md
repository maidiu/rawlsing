# SOROK REMONTATHON — R6 SOURCEFREE MATERIAL CONSERVATION

- **Date:** 2026-11-19 (America/Chicago project clock).
- **Exact base:** draft PR #1171, author HEAD `52fcbe5f36952fe671e9c941c85896e5f6149078` over executable ORACLE R3 `3dba91136870ab5e766ca14faacd847531dea075`.
- **Scope:** current R3 `um_sorok_organism/world.py` only plus actual integrated regression tests. NOT native P2/P3/P6 or a new money/economics ontology.
- **Tests:** initial complete R5 corpus independently rerun 111 PASS normally and 111 PASS under Python -O. New `tests/test_remontathon_r6.py` adds **20 cases**; complete R3 R6 corpus 131 PASS / 0 FAIL, normal and optimized. Before correction 13 R6 targeted tests were red on old source; additional self-owned-goods and rejected-meal partial mutation defects were red during construction. All inherited tests remain green, including R4 `test_p049_self_sale_does_not_mint_money`.

## Reproduced defects (LOCAL AUTHOR R6, NOT INDEPENDENTLY RECEIVED)

- **SR-P053 / Buyer–seller money-unit loss or overflow**: individually valid float cash claims could fail to debit a very large purchaser, fail to credit a very large seller, or overflow seller credit to `inf`, while the world marked goods bought. Repair uses decimal-space prospective sums and requires exact representability through the existing stored float material claim. It does not replace the world currency architecture.
- **SR-P054 / Wage-payer and worker-account changes lost or overflowed**: producer stock and wages were committed despite no matching real debit/credit on large accounts. Repair qualifies both resulting balances *before* changing any material stock or claim.
- **SR-P055 / Physical goods conservation**: adding 1 good to enormous holdings or adding 2 stock units to enormous stock had no representable change; removing 1 from enormous physical stock or holdings also had no effect. Repair requires true representable material deltas before purchase, eating, repair and work. Ordinary material transfers continue to work.
- **SR-P056 / Same owner self-trade and self-wage**: a same-account worker/employer formerly minted wages because successive writes to one key overwrote each other. Same-owner food allocation recorded positive `price_paid` despite no buyer/seller monetary exchange. Repair preserves R4's permitted performance for self-owned goods, with real inventory reallocation, zero paid transfer and precise classification. Sourcefree self-controlled goods production records no fabricated wage, remains actor-performed, and preserves real stock. Self-owner stock retrieval no longer depends on fictitious cash needed for a self-purchase. **This is a bounded first-source accounting decision, not law of self-employment or permitted native SOROK ownership.**
- **SR-P057 / Rejected EAT partial world mutation**: after guarding unrepresentable shared food, an `EAT` exception still left a phantom empty holdings dictionary through eager `setdefault`. No inventory is created until the material transfer has qualified; failed acts leave no partially changed world state.

## Executed evidence

- `RED_R6.txt`: original 15 new probes, 13 red on original R5, 2 green.
- `R6_SELF_OWNED_RED.txt`: actual no-cash self-owned retrieval failed while being developed.
- `R6_GREEN_ALL.txt`: final full 131/131 green verbose unittest transcript.
- `R6_GREEN_OPTIMIZED.txt`: final full 131/131 green `python -O` unittest transcript.
- `REMONTATHON_R6_FILE_IDENTITIES.json`: executed Python/test file exact SHA and byte counts; archive preserves all R3+REMONT preceding source/tests.

## Continuing qualifications

No claim that these tests imply general econometric, institution or psychodynamic truth; no new prohibition on self-controlled work; no protected merge or other owner mutation; no independent review/receiving; older E holds unchanged. Preserve prior sourcefree R3 base tests and identity ledger. Exact source choices remain provisional and reversible as Constitutive Organism is developed.
