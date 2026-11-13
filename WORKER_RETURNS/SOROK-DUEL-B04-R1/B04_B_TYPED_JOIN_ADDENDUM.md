# B04 typed parent-history join — B revision

**Status:** `SOURCEFREE_S2_ONLY`; actual typed `P2_PARENT_PURCHASE` consumption at frozen composition `46a815643440857ff1185481a5e27ef7023e541f`.
**Implementation SHA:** `ef2129283fff3deffab8cefef6ff94da3045bc58`.
**A production:** `d2a0a4eadab4ba99ae830c8e47013e60295a4632`.
**Pair3 parent hook:** returned C02/C03 `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34`, production `255fd4905990e3c0cab3e2d95ba91b851ea701a8`.
**Base:** `B04_ABI.md`; `B04_A_SEMANTIC_ABI.md` is the pre-hook boundary and its “pending” section is historical. `B04_B_ABI_REVISION_PRE_TYPED.md` is the removed bridge record, retained as history.

## Actual typed join

At this cut Pair3 `parent_activity._parent_material_history` recognizes the typed
`P2_PARENT_PURCHASE` episode via `_purchase_history_source`, validates root,
branch, actor, alias, status, before/after source, possession/event effect,
currency and operation receipt, and includes it in ordered material history.
Therefore, after one admitted B04 purchase:

```text
read_parent_material(..., as_actor=parent)        -> READ, cash/free-hours debited
parent_feasible_actions(...)                     -> READ, typed options
read_parent_history(...)                         -> material_consistent True,
                                                    purchase_episode_count includes
                                                    P2_PARENT_PURCHASE
read_purchase(...)                               -> parent status READ,
                                                    purchase_history_hook
                                                    C02_PARENT_HISTORY_READ
```

The B04 antecedent/`PURCHASE_MATERIAL_STATE` bridge remains removed. No
WORK/DEBT/CIRCUMSTANCE row is fabricated. Exactly one typed purchase-history row
exists per admitted purchase in C02 history; a refused purchase has its typed
REFUSED row with before=after and no debit/stock/ownership.

## Currency rule

`purchase_drum_kit` requires all three declared units to be exactly equal:

```text
parent material currency_unit == market currency_unit == request currency_unit
```

Otherwise `PURCHASE_CURRENCY_INCOMPATIBLE` before debit/stock/ownership; the
receipt records all three and `currency_basis=PARENT_MARKET_REQUEST_CURRENCY_UNIT_EQUAL`.
No conversion, no doubled wealth. The prior default parent unit
(`parent_sourcefree_currency_unit`) versus market unit
(`sourcefree_currency_unit`) mismatch refuses; a matching parent fixture admits.

## Actual downstream sequence proved

B04/B05 tests at this cut execute:

1. B02 current period exists;
2. registered parent fixture in the market unit, market stock;
3. admitted B04 purchase: parent cash/free-hours debited, stock decremented,
   ownership written, one P2/C12 checkpoint;
4. typed C02 parent material/read/options/history consumption;
5. next legitimate parent activity (PAID_WORK), then second purchase (stock/
   ownership/debit), later `read_purchase` historical=True;
6. B05 materialize to completed period, rent on B01 fixed-A household cash;
7. B03 feasibility changes after rent; P3 store head unchanged by B04/B05.

## Serialization/rollback

B04 retains `material_operations.lock` and C02 `_parent_write_lock` around the
read/check/write unit; one `_StoreWrite` covers typed purchase receipt, parent
material, market stock, ownership and checkpoint. Injected checkpoint failure
leaves no receipt/debit/stock/ownership/bridge; cold reopen is pre-purchase.
Immediate retry is REPLAY; later parent material activity makes a stale replay
refuse without a second debit.

## First consumers

```text
material_operations.read_purchase
parent_activity.read_parent_material
parent_activity.parent_feasible_actions
parent_activity.read_parent_history
material_operations.read_market_inventory / read_owned_objects
rolling_reproduction.read_household_obligation
```

## Boundaries

No mother decision/utterance/hidden reason or Nadia uptake; no public purchase
event/Nadia perception; no household-funded alternative; no general economy,
landlord balance/arrears, variable rent or currency conversion; no cold fork/full
P6 live turn; no native/science/rights/human/merge; prior P3 roots incompatible.
One independent nonauthor receiving remains required.
