> **Later typed-hook notice:** Pair3 typed `P2_PARENT_PURCHASE` history is now present and consumed. The “pending” state below is historical; see `B04_B_TYPED_JOIN_ADDENDUM.md`.

# B04 typed purchase / C02 parent-history hook ABI — A semantic revision

**Status:** `SOURCEFREE_S2_ONLY`; B04 purchase receipt/stock/ownership is real, but C02 parent current-material consumption is **REFUSED until the typed hook exists**. No antecedent bridge is adopted.
**Final code:** `d2a0a4eadab4ba99ae830c8e47013e60295a4632`; B start `15472ca`; B production `4a3c45c`.
**Base:** `B04_ABI.md`; B's `B04_B_ABI_REVISION.md` bridge is retained as historical evidence but **not adopted**.

## B04 current operation

```text
p6_market_inventory / p6_owned_objects : source-qualified P2 world facts
purchase_drum_kit(session, parent_id, *, operation_id, owner_actor_id,
                  request=None, expected_clock=None)
read_market_inventory / read_owned_objects
read_purchase(session, parent_id, operation_id, *, as_actor)
```

Admission (one `_StoreWrite` under B04 locks):
- validates the registered parent material through C02 **before** the purchase;
- validates market stock, price/currency, parent cash/free-hours, B03 material constraints;
- requires parent material `currency_unit` == market `currency_unit` == request `currency_unit`; mismatch refuses `PURCHASE_CURRENCY_INCOMPATIBLE` with no conversion/doubled wealth; receipt records all three units and `currency_basis=PARENT_MARKET_REQUEST_CURRENCY_UNIT_EQUAL`;
- atomically writes the typed `P2_PARENT_PURCHASE` C12 receipt, parent material document, market decrement, ownership row and one checkpoint;
- no `P2_PARENT_MATERIAL_ANTECEDENT`, `P2_PARENT_ACTIVITY`, `P2_PARENT_CIRCUMSTANCE` bridge, no WORK/DEBT/CIRCUMSTANCE fake, no public event.
- B01 fixed-A cash/free-hours untouched; parent C02 cash/free-hours funding only.

`read_purchase`:
- resolves the parent alias through C01 `read_supporting_actor`;
- reads the typed `P2_PARENT_PURCHASE` episode and ownership acquisition row;
- returns the receipt/owned totals even when C02 current material cannot validate;
- reports `parent_material_status` / `parent_feasible_actions_status` as the actual C02 refusal (currently `REFUSED:PARENT_MATERIAL_HISTORY_MISMATCH`);
- `parent_material=None`, `historical=None`, `purchase_history_hook=C02_PARENT_HISTORY_KIND_PENDING` in that state;
- it does **not** call the purchase an antecedent, does not weaken C02 history, and does not fabricate a parent feasible choice.

## Exact typed hook required in Pair3 C02 (not edited here)

```text
producer: B04 C12 episode kind = P2_PARENT_PURCHASE
body: root, branch, actor_id, alias, operation_id, status, receipt,
      material_after_source (and material_before_source if present)

consumer: parent_activity._parent_material_history / read_parent_history
          / read_parent_material / parent_feasible_actions / C03 composition

required ordering: include the purchase row in the same ordered material
history as antecedent/activity/circumstance, using material_after_source as
the post-operation source; expose kind=P2_PARENT_PURCHASE and operation_id;
validate that the current material source equals the latest ordered source.

required non-behavior: do not accept an arbitrary P2_PARENT_MATERIAL_ANTECEDENT
with operation_kind=PURCHASE_MATERIAL_STATE as purchase history; do not copy
the values into a differently typed row; do not let the bridge bypass the
purchase kind or C02 linkage validation.
```

After this hook, `read_parent_material`, `parent_feasible_actions`, parent
activity and B05 parent work can consume the purchase. Until then, they must
refuse; B04/B05 rent/ownership readers continue independently. If the hook is
added, remove/review B's bridge (already removed here) and verify no duplicate
history row.

## Serialization/rollback preserved

- B04 state-root `material_operations.lock` + C02 `_parent_write_lock` around the
  complete read/check/write unit.
- One `_StoreWrite` transaction over receipt/parent/market/ownership/checkpoint.
- Injected checkpoint failure leaves no receipt, debit, stock or ownership; cold
  reopen pre-purchase.
- Immediate retry REPLAY; later parent material change yields stale/no second
  debit; a second purchase after the first currently refuses
  `PURCHASE_PARENT_UNAVAILABLE` because C02 history does not yet recognize the
  typed purchase (actual join refusal, not a bridge).

## Boundaries

No mother decision/utterance/uptake; no public purchase event/Nadia perception;
no household-funded alternative; no fork/cold-fork purchase; no general economy;
no currency conversion; no native/science/rights/human/merge; no prior P3 root
compatibility. One independent nonauthor receiving remains required.
