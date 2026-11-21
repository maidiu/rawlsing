# B04 parent-funded purchase ABI — B revision

**Status:** `SOURCEFREE_S2_ONLY`; B02/B03-dependent material operation. Not a mother decision, public event, possession-by-narrative, or native science.
**Implementation SHA:** `4a3c45cda7d814df0c60ca4e245499fcfca62162`.
**Frozen composition start:** `2a47fb389b453c2f902b8c13ed52304fb40efd0d` (A result `8de517bd3` + returned Pair3 C02 `4d93685df`; clean automatic merge, not executed/accepted).
**A production:** `62292613aa9210a7d3e944314e36924349337439`.
**Base ABI:** `B04_ABI.md` remains the material-fact/API contract; this revision adds the composition/atomicity bridge and locks.

## Unchanged material facts and purchase checks

```text
p6_market_inventory  SOROK_MARKET_INVENTORY@1
p6_owned_objects     SOROK_OWNED_OBJECTS@1
purchase_drum_kit(session, parent_id, *, operation_id, owner_actor_id,
                  request=None, expected_clock=None)
read_market_inventory / read_owned_objects / read_purchase
```

The object must exist in source-qualified market stock; price/currency must
match; the registered parent must have cash/free-hours; B03 tenancy/space/noise
refuses or UNKNOWN except that household `REFUSED_AFFORDABILITY` is separated
from parent funding. Refusals append a durable receipt with no debit, stock or
ownership change. B01 fixed-A cash/free-hours are not spent. No public event,
Nadia perception, psyche record, or P3 write is created.

## B revision: C02 material-history composition

### The failure on the supplied cut

A's B04 writes `P2_PARENT_PURCHASE` and mutates the parent material document,
but Pair3 C02 `_parent_material_history` recognizes only
`P2_PARENT_MATERIAL_ANTECEDENT`, `P2_PARENT_ACTIVITY`, and
`P2_PARENT_CIRCUMSTANCE`. At frozen composition `2a47fb389`, after one admitted
purchase:

```text
read_parent_material      -> PARENT_MATERIAL_HISTORY_MISMATCH
parent_feasible_actions   -> PARENT_MATERIAL_HISTORY_MISMATCH
read_purchase             -> PARENT_MATERIAL_HISTORY_MISMATCH
B05 parent work/read      -> PARENT_MATERIAL_HISTORY_MISMATCH
```

A's two B04 tests and B05 test fail at this composition cut. A's 32-test claim is
author evidence at a different cut, not a passed composed result.

### Material-side bridge

On admitted purchase, in the same `_StoreWrite` transaction as the purchase
receipt, market decrement, ownership row, parent material update and checkpoint,
B04 appends one C02-recognized parent **material state** record:

```text
kind = P2_PARENT_MATERIAL_ANTECEDENT
body schema = SOROK_P2_PARENT_MATERIAL@1
root, branch, epoch, actor_id, alias, source, source_ref
material_source = post-purchase parent material source
material_before_source, material_after_source
material = exact post-purchase C02 material content
operation_id = purchase operation id
operation_kind = PURCHASE_MATERIAL_STATE
purchase_source = B04 purchase source
```

This is a material-source record, not a WORK/DEBT/CIRCUMSTANCE activity claim. The
separate `P2_PARENT_PURCHASE` receipt remains the operation evidence. C02's
current material history is therefore consistent and `read_parent_material`,
`parent_feasible_actions`, `read_purchase`, and later B05 parent work/read succeed.
The bridge is removed with the transaction on rollback.

### Exact C02 hook still required for full history exposure

`parent_activity._parent_material_history` and `read_parent_history` still ignore
`P2_PARENT_PURCHASE`, so the purchase is not listed as a purchase row in C02
history; it is visible through the bridge material state and through B04
`read_purchase`. The exact Pair3-owned hook for full purchase-history truth is:

```text
input:  C12 episode kind P2_PARENT_PURCHASE with body root, branch, actor_id,
        alias, operation_id, status, receipt, material_after_source
output: the same history source ordering used by _parent_material_history and
        read_parent_history, exposing the purchase kind/operation
consumer: parent_activity.read_parent_material / read_parent_history /
          parent_feasible_actions, and C03/C04 parent decision composition
```

`parent_activity.py` was not edited. The bridge is the B04-owned material-side
contract that keeps current state coherent; the hook is the Pair3 reconciliation
for full historical purchase exposure. If Pair3 later recognizes the purchase
kind directly, the bridge must be reviewed to avoid duplicate history rows.

## B revision: serialization and rollback

- `purchase_drum_kit` now takes a state-root `material_operations.lock` and C02's
  existing `parent_activity.lock` around the read/check/write unit. This prevents
  two purchases or a concurrent C02 parent activity from losing/debiting material.
- `establish_market_inventory` uses the same material-operation lock.
- The admitted write remains one `_StoreWrite` transaction over the purchase
  receipt, the material-history bridge, parent material, market stock, ownership
  and one checkpoint. An injected checkpoint failure leaves no receipt, bridge,
  stock, ownership or debit; a cold reopen returns the pre-purchase state.
- Refusals are durable `P2_PARENT_PURCHASE` receipts with no material bridge and
  no world/stock/ownership change.
- Immediate operation retry is `REPLAY`; a retry after later parent activity is
  `PURCHASE_REPLAY_STALE` without a second debit.

## ABI / downstream impact

- `purchase_drum_kit` signature and receipt schema are unchanged except that the
  receipt can now be followed by a C02-compatible material-history record.
- `P2Owner` constructor/validate/realize/participant methods are untouched.
- No bp4 event vocabulary, P3 file, `parent_activity.py`, `supporting_actor.py`,
  P6 situated file, guide, workflow, Pyat, or protected file was edited.
- D02/C02 active inputs are not rebased; the bridge is additive material history.
- P3 code-pin roots from all prior p2_owner cuts remain incompatible; no migration.

## Proof boundaries

No mother decision/utterance/uptake; no public purchase event/Nadia perception;
no household-funded alternative; no fork/cold-fork purchase; no full household
economy or landlord balance; no native/science/rights/human/merge authority.
The C02 stale `PARENT_B02_HOLD` literal remains Pair3-owned and is not treated as
authority by B04/B05. Full purchase history awaits the exact hook above.
