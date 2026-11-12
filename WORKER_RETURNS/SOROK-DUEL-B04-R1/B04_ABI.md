> **B revision (`4a3c45cda7d814df0c60ca4e245499fcfca62162`):** admitted purchase now appends a C02-recognized material-state bridge in the same transaction and serializes with parent/material locks. The base purchase/rent schemas are unchanged; see `B04_B_ABI_REVISION.md` for the exact C02 composition/hook and crash boundary.

# B04 parent-funded stock purchase ABI

**Status:** `SOURCEFREE_S2_ONLY`; depends B02/B03. Not a mother decision, public event, or native science.
**Code:** final SHA `62292613aa9210a7d3e944314e36924349337439` (feature commit `a3f74693b70cb09f0e8bac4a7ca094812173db3a`).
**Module:** `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py`.

## World material facts

```text
p6_market_inventory   SOROK_MARKET_INVENTORY@1
  currency_unit = sourcefree_currency_unit
  items: object_id, kind, quantity (>=0 int), unit_price (>=0 int)
  binding: root, branch, epoch, source

p6_owned_objects      SOROK_OWNED_OBJECTS@1
  objects: acquisition_id, object_id, kind, owner_actor_id, quantity (>=1),
           market_source, purchase_source, currency_unit, unit_price
  binding: root, branch, epoch, source
```

The default market stocks junior drum kit x2 at 40 and acoustic kit x1 at 180.
Both are one P2 `world.resources` entry via the existing checkpoint; no second
household database.

## API

```text
establish_market_inventory(session, items=None) -> market read
read_market_inventory(session) -> market read
read_owned_objects(session) -> owned read (ABSENT if never purchased)
purchase_drum_kit(session, parent_id, *, operation_id, owner_actor_id,
                  request=None, expected_clock=None) -> purchase receipt
read_purchase(session, parent_id, operation_id, *, as_actor) -> receipt read
```

`purchase_drum_kit` requires:
- registered parent material via C02 `read_parent_material` (self-only);
- B02/B03 period/dwelling/household context when established;
- B03 `material_feasibility`; only `REFUSED_AFFORDABILITY` is separated as a
  household-cash constraint; `UNKNOWN` or any other reason refuses;
- exact market object/kind, matching request price and currency;
- explicit owner `owner_actor_id` in {fixed-A household holder, parent_id};
- parent cash >= price and parent free_hours >= 1.

On admission it atomically (one `_StoreWrite`):
1. debits parent material cash/free_hours through the exact C02 material document;
2. decrements market stock;
3. appends an ownership row for the explicit owner;
4. appends one C12 `P2_PARENT_PURCHASE` receipt;
5. writes one P2 checkpoint.

It does **not** debit B01 fixed-A cash/free_hours, emit a world event or
perception, or alter any P3 psychology. `public_event=NOT_EMITTED_HELD_PAIR3_VOCABULARY`,
`event_effect=NONE`, `possession=OBJECT_STOCK_AND_OWNERSHIP_WRITTEN`.

Refusals (stock, parent funds, parent time, B03 material constraint) append a
durable REFUSED receipt with before/after sources equal and no world change.
Wrong owner/parent/currency/price/branch/source raises before effects.

Immediate operation retry returns `REPLAY` with no new debit/stock/ownership;
a retry after a later parent/material state refuses `PURCHASE_REPLAY_STALE`.
`read_purchase` verifies the current parent/market/owned sources against the
admitted after state (or the refused before state) and returns
`parent_feasible_actions`.

The receipt carries the actual B02 period reference when the plan exists:
`period_id`, `as_of_date`, `as_of_relation`, `interval_status`,
`interval_status_detail`; otherwise `B02_NOT_AVAILABLE`. It declares
`currency_basis=PARENT_MATERIAL_CASH_UNIT_AS_SOURCEFREE_CURRENCY_UNIT` and does
not convert units. It carries the B01 household and B03 dwelling source/hash as
unchanged reconciliation evidence.

## Invariants

- No object without source-qualified stock.
- No ownership without an admitted stock transfer.
- No refusal debit, negative balance, or double retry.
- No B01 fixed-A cash spent as the parent's; no duplicated parent cash.
- No public event, Nadia perception, psyche record, or mother decision.
- No fork purchase; C02 parent material is branch-bound.
- No currency conversion.
- No native/science/rights/human/merge authority.
