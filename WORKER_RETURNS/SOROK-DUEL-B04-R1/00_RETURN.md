# SOROK B04 Agent A return — typed purchase

**Task:** B04 parent-funded stock purchase (CG-B), depends B02/B03.
**Code:** `d2a0a4eadab4ba99ae830c8e47013e60295a4632` on `codex/sorok-duel-b04-b05-a-semantic-interleave-20261112-r1`; B locks/rollback retained from `4a3c45c`; B start `15472ca`.
**Full relay handoff:** `AGENT_A_SEMANTIC_INTERLEAVE_HANDOFF.md`; **exact typed parent ABI:** `B04_A_SEMANTIC_ABI.md`; delta/impact: `PROGRAMMA_DELTA.json`, `impact.json`.

## FINDING

The purchase is a real typed `P2_PARENT_PURCHASE` operation: source-qualified market stock must exist; parent cash/free-hours are debited; stock is decremented; ownership is written; one C12 receipt and one checkpoint commit atomically; B01 fixed-A cash is untouched; parent/market/request currencies must be explicitly equal (no conversion), else refusal; refusal does not debit or create stock/ownership; no public event or P3 psychology. B's `P2_PARENT_MATERIAL_ANTECEDENT`/`PURCHASE_MATERIAL_STATE` bridge is **not adopted**: it was a differently typed post-operation material row used to make C02's old history filter green, not typed purchase consumption. After the purchase, C02 `read_parent_material`/`parent_feasible_actions`/parent activity actually refuse `PARENT_MATERIAL_HISTORY_MISMATCH`. `read_purchase` still reads the typed receipt and ownership and reports the exact C02 refusal + the pending typed hook.

## EVIDENCE

- B04 operations + composition: 7 passed in 63.78s (`evidence/b04_a_semantic.log`).
- Combined B01+B03+B02+B04+B05: 42 passed in 399.43s (`../SOROK-DUEL-B05-R1/evidence/a_b04_b05_cross_combined.log`).
- P6 house/P2/actor 15 passed; P6 MII 18 passed.
- Negatives: wrong owner/currency/parent/price/branch/source; funds/time/stock/acoustic refusal no effect; no antecedent bridge row; post-purchase C02 refusal; second purchase refused; crash rollback; cold/severance.

## LIMITS

Typed C02 purchase-history hook is pending Pair3; post-purchase parent material/feasible/activity and second purchase legitimately refuse until it exists. No mother decision/utterance/uptake, public event/Nadia perception, household-funded purchase, fork/cold-fork purchase, general economy/currency conversion, native/science/rights/human/merge, or old P3 root compatibility. One independent nonauthor receiving remains required. Cost UNKNOWN.
