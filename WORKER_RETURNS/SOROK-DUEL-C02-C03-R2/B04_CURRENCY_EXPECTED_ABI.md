# B04 currency/parent-history expected ABI (for Pair1 B owner)

**Status:** exact requested change from the C02/C03 parent owner; B04 code was
not edited here. Evidence: `evidence/b04_b05_currency_boundary.log`.

## Observed gap

B04 `purchase_drum_kit` currently admits a parent-funded purchase regardless of
the parent material's `currency_unit`. The default C02 parent material is
`parent_sourcefree_currency_unit`; the B04 market/household currency is
`sourcefree_currency_unit`. B04 records the purchase as `ADMITTED`, debits
parent cash, decrements stock and adds ownership, then its receipt
`currency_basis` declares the parent cash unit equivalent to the sourcefree
currency. C02's history-bound parent reader correctly refuses that admitted
purchase with `PARENT_PURCHASE_CURRENCY_MISMATCH`, because no conversion or
equivalence was issued. B04's two tests and the B05 rolling test therefore fail
at their default parent fixture after a purchase. This is a real typed conflict,
not a C02 reader defect.

## Expected B04 change (smallest, in B04's own writer)

1. In `purchase_drum_kit`, before any debit/stock/ownership/receipt:
   ```text
   parent_currency = material["material"]["currency_unit"]
   request_currency = request["currency_unit"]
   market_currency = market["currency_unit"]
   require parent_currency == request_currency == market_currency
   ```
   On mismatch return a durable B04 `REFUSED` receipt with
   `reasons=["CURRENCY_MISMATCH"]`, `parent_material_source_before == after`,
   no debit/stock/ownership, and `possession="NONE"`; or raise
   `PURCHASE_CURRENCY_MISMATCH` before effects. A durable refusal is preferred
   so C02 history can show the refused attempt.
2. Receipt fields:
   ```text
   parent_currency_unit_before
   market_currency_unit
   currency_match: true | false
   ```
   Remove or replace `currency_basis=PARENT_MATERIAL_CASH_UNIT_AS_SOURCEFREE_CURRENCY_UNIT`;
   do not assert parent/market currency equivalence without an issued conversion.
3. `read_purchase` must validate the same currency equality and parent material
   source; no conversion or shared household cash.
4. B04/B05 test fixtures should establish parent material with
   `currency_unit="sourcefree_currency_unit"` when they intend a purchase, or
   exercise the new `CURRENCY_MISMATCH` refusal. They should not rely on the
   removed equivalence declaration.
5. B05 rent remains household actor-A cash and is separate from parent cash;
   its fixture must not mix units.

## C02/C03 side already implemented

- `parent_activity._parent_material_history` accepts only the exact
  `P2_PARENT_PURCHASE` receipt schema/identity/root/branch/sources/status.
- An admitted purchase is accepted only when its `currency_unit` equals the
  current parent material currency; otherwise
  `PARENT_PURCHASE_CURRENCY_MISMATCH`.
- A refused purchase is accepted only when before == after and no possession.
- C03 `propose/admit_parent_decision` refuses `CURRENCY_MISMATCH` before B04 is
  called, so the parent decision path never invokes the unsafe B04 debit.
- A matching parent (`sourcefree_currency_unit`) purchase is accepted and
  exercised by `test_parent_decision_perform_replay_stale_and_cold`.
