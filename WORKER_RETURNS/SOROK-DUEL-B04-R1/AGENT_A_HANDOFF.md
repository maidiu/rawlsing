> **Later same-pair semantic revision:** this file describes the pre-B04/B05-bridge A cut. The current code `4959596dd2e130a3856cc3b9d7ce24f8d0261400` removes B's antecedent bridge, keeps B's locks/rollback, and exposes the actual C02 typed-purchase refusal. See `AGENT_A_SEMANTIC_INTERLEAVE_HANDOFF.md` and `B04_A_SEMANTIC_ABI.md`; this file is retained as historical.

# SOROK B04 AGENT A — parent-funded stock purchase handoff

**Packet:** B04 `Implement consequential household work/care/resource and acquisition/refusal operations` (CG-B), depends B02/B03.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, or protected merge. Constructive author evidence, not independent receiving.
**Composition start:** `046f0f3be85cf13d6cab5acc1a5cd3e90dce17c5`.
**Branch:** `codex/sorok-duel-b02-a-relay-b04-b05-20261112-r1`.
**Code:** final code SHA `62292613aa9210a7d3e944314e36924349337439`; feature commit `a3f74693b70cb09f0e8bac4a7ca094812173db3a`.
**Running contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Module:** `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py`.
**ABI:** `B04_ABI.md`. **Delta/impact:** `PROGRAMMA_DELTA.json`, `impact.json`.

## 1. Exact artifact

Changed code:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py` | Source-qualified market inventory and ownership facts; parent-funded purchase/refusal; stock/ownership/parent material atomic write; later readers. |
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | Added `p6_market_inventory`/`p6_owned_objects` to the material-fact slot allowlist. No constructor/validate/realize/participant edit. |
| `WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py` | Positive/refusal/stock/ownership/funding/currency/owner/branch/source/cold/severance tests. |

Untouched: `parent_activity.py`, `supporting_actor.py`, P3, `situated.py`, P6 `house.py`, B01/B03 production, guides/workflows/Pyat/config.

Commands:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_same_root_psyche.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_incremental.py \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py
```

## 2. Governing contract

B04 requires a paid obligation/job change/purchase/refusal to change actual resources, ownership and next-action feasibility; the negative is a negative balance, an unavailable apartment instrument admitted, a refusal silently debiting, or a rendered object conjured without a writer; restoration must preserve one debit and one world receipt. It reuses the existing world/event/material writer and C02 paid-work/care/debt kernel; no separate household database.

The B03 dwelling/acoustics/space/tenancy facts and B02 dated period are the actual material context. The buyer is the registered C02 parent; B01 fixed-A household cash/free-hours must not be silently spent as the mother's. The B04 terminal consumer is the later objective stock/ownership/time and parent feasible choice; C03 actual parent decision/utterance remains future. The two Library architecture records remain NOT_INSPECTED locally.

## 3. Strongest achieved result

Two new source-qualified P2 world facts:

```text
p6_market_inventory   SOROK_MARKET_INVENTORY@1
    currency_unit=sourcefree_currency_unit
    items: object_id, kind, quantity, unit_price
p6_owned_objects      SOROK_OWNED_OBJECTS@1
    objects: acquisition_id, object_id, kind, owner_actor_id, quantity,
             market_source, purchase_source, currency_unit, unit_price
```

`establish_market_inventory` writes a real default stock: junior drum kit quantity 2 at 40, acoustic kit quantity 1 at 180. `read_market_inventory` verifies source/root/branch/epoch/currency/items. `read_owned_objects` aggregates ownership totals and carries provenance.

`purchase_drum_kit(session, parent_id, operation_id, owner_actor_id, request)`:
- reads the registered parent material via C02 (`_read_material`, self-only), the real market stock, B01 household, B03 dwelling and B03 `material_feasibility`;
- separates B03 household `REFUSED_AFFORDABILITY` from the parent's own funding; any other B03 material reason or `UNKNOWN` refuses;
- requires the exact object/kind in market stock, matching price/currency, parent cash >= price and parent free_hours >= 1;
- debits **parent** cash and free_hours, decrements **market** stock, adds an **ownership** row for the explicit owner (household holder A or the parent), and appends one C12 `P2_PARENT_PURCHASE` receipt plus one checkpoint in a single `_StoreWrite` transaction;
- proves the B01 household source/material_hash and B03 dwelling source are unchanged;
- emits no world event or perception: `public_event=NOT_EMITTED_HELD_PAIR3_VOCABULARY`, `event_effect=NONE`;
- includes the actual B02 period reference when the plan exists (`period_id`, `as_of_date`, `as_of_relation`, `interval_status`);
- returns a durable REFUSED receipt for stock/funds/time/material-constraint refusals with no debit/stock/ownership change;
- is idempotent by operation ID; immediate retry returns REPLAY; later-state retry refuses stale rather than re-debiting.

Demonstrated: parent cash 120/free 8 buys two junior kits (cash 80 then 40, free 7 then 6, stock 2→1→0, ownership 1→2); third purchase REFUSED stock with no debit; wrong owner/currency/parent/price/market branch/parent branch refuse; acoustic kit REFUSED noise with no debit; missing object REFUSED stock; parent no-time REFUSED time; B05 composition buys despite household affordability because the parent funds it; cold subprocess exact; market severance/restore exact.

Evidence: `evidence/a_relay_b04.log` 2 passed in 21.31s; combined 32 passed in 229.33s in `WORKER_RETURNS/SOROK-DUEL-B05-R1/evidence/a_relay_b01_b02_b03_b04_b05.log`. P6 `test_house` 8/8, `test_mii` 18/18, adjacent 9/9.

## 4. Own hostile findings

1. **Pair3-owned parent material helpers.** B04 reuses `parent_activity._read_material`, `_material_content`, `_material_document`, `_StoreWrite` and the same actor material document; it does not edit `parent_activity.py`. The purchase is a new B04 operation, not a second parent owner. If Pair3 B's live contract rejects this operation shape, the exact symbols are `_StoreWrite`, `_material_content`, `_material_document`, `_read_material`, `PARENT_MATERIAL_SCHEMA`, `PARENT_GRADE`; HQ must reconcile the new `P2_PARENT_PURCHASE` operation.
2. **No public event.** The purchase is an objective stock/ownership operation at its real consumer, not a performed outward event. The `bp4` event vocabulary/projection hook is Pair3-leased; the receipt truthfully holds it. No Nadia perception is fabricated.
3. **Refusal records are C12 episodes, not world events.** A refusal appends a durable receipt with no checkpoint/world change; a retry returns the refusal. This is a receipt, not a claimed action.
4. **Parent cash unit is declared, not converted.** C02 parent material has no currency field; B04 declares `PARENT_MATERIAL_CASH_UNIT_AS_SOURCEFREE_CURRENCY_UNIT` and refuses a market/request currency mismatch. It does not guess a conversion.
5. **Later-state retry is stale.** A purchase replayed after a later parent activity refuses `PURCHASE_REPLAY_STALE` rather than returning a historical receipt; the immediate retry is REPLAY. This is conservative and consistent with C02.
6. **No fork/cold parent purchase.** C02 parent material is branch-bound; a child-fork purchase is refused. No cold fork is claimed.
7. **B02 period reference depends on the plan.** Without an established B02 plan, the receipt says `B02_NOT_AVAILABLE`; it does not invent a date. With the plan, it names the actual period.
8. **C02 stale B02 qualification.** `parent_activity.py` still says `HELD_B02_CALENDAR_ABSENT`; B04's receipt uses the actual B02 period, but the C02/C03 owner must reconcile `PARENT_B02_HOLD`. I did not edit Pair3.
9. **C02 `read_parent_history` does not include the B04 purchase.** `parent_activity.read_parent_history` filters `P2_PARENT_MATERIAL_ANTECEDENT`, `P2_PARENT_ACTIVITY`, and `P2_PARENT_CIRCUMSTANCE`; the new `P2_PARENT_PURCHASE` episode is readable only through `material_operations.read_purchase`. C03/C04 or the C02 owner must compose that kind deliberately; I did not edit Pair3 `parent_activity.py`.
10. **My first B04 test hit stock exhaustion before the price-mismatch and no-time checks.** I reordered the test to the stock/price/time states; production behavior was not weakened.

## 5. Unresolved challenges

- **C03/C04:** no mother decision, performed utterance, hidden reason or Nadia uptake. B04 is an objective purchase/refusal; C03 must decide whether/how the parent purchases.
- **B01 household/A cash:** the purchase deliberately does not debit it; the mother may later choose a household-funded purchase, but that operation is not built. One funding source is proven, not a general household budget.
- **Public event/Nadia perception:** held; no outward purchase event or qualified perception.
- **Fork/cold:** no child-fork purchase; cold same-branch subprocess only.
- **B05:** the recurring rent/parent-work composition is in B05, not B04; B04 does not charge rent.
- **P3 code-pin:** final `p2_owner` slots change the P3 pin; old roots incompatible, no migration.
- **Native/science/rights/human/merge:** held.
- **Cost:** UNKNOWN.

## 6. Likely attack surfaces for SAME B

1. Make a purchase on a child fork or with a foreign branch/source; require refusal.
2. Tamper parent material, market stock, ownership, or price/currency; require exact refusal and no debit.
3. Retry a purchase after a later parent activity or after a second purchase; require no second debit and a truthful historical/stale result.
4. Make the B03 household affordability refusal and the parent's own funding disagree; require the parent-funded path to remain explicit, with no B01 cash spend.
5. Try a purchase with no B02 plan, a future as-of, a past period, or a period boundary; require the period reference to be truthful or absent.
6. Attack the `_StoreWrite` transaction by failing after the episode append but before the checkpoint (test injection) and prove rollback; the current tests cover cold/severance, not every injected failure.
7. Reconcile `PARENT_B02_HOLD` in C02/C03 without editing Pair3 live files.

**Hardest constructive challenge for SAME B:** prove the same parent-funded purchase across a real P3 `BatchEngine` cycle and a B02 midperiod employment change, with a failure injected between the C12 receipt and the P2 checkpoint, then cold-recover exactly one debit and one ownership row; and extend the funding model to a household-funded alternative without double-spending or unit conversion.

## 7. Rejected alternatives

- **Use B01 actor-A household cash for the mother's purchase.** Rejected: silently spends the focal household's money as the mother's. The registered parent's cash/free-hours are the funding source; B01 cash is proven untouched.
- **Call `record_parent_activity(PAY_DEBT)` and relabel it a purchase.** Rejected: a purchase is not debt payment; receipt/event labels must match the operation.
- **Emit an `OFFSCREEN_REPAIR` event for the purchase.** Rejected: the event vocabulary/projection hook is Pair3-leased and a purchase is not a repair; the actual stock/ownership consumer proves the effect without a false outward event.
- **Add a second household/market database.** Rejected: two new P2 world resources inside the existing checkpoint; no second ledger.
- **Conjure a drum kit when stock is absent or on refusal.** Rejected: stock/ownership only after all checks; refused paths leave both unchanged.
- **Treat B03 `REFUSED_AFFORDABILITY` as the parent's funding refusal.** Rejected: it is a household-cash constraint; the parent funding check is separate. Other B03 material reasons remain hard refusals.
- **Guess a currency conversion.** Rejected: declared sourcefree unit; mismatch refuses.

## 8. Proof boundaries

Do not claim: a mother decision/utterance/uptake; a household-funded purchase; a public purchase event or Nadia perception; a fork/cold-fork purchase; a general household economy or landlord balance; native actor/world science, rights, human validation, or protected merge; P3 old-root compatibility; full-estate coverage. B04 is executed author evidence at the code cut above, with one independent nonauthor receiving still required. Cost UNKNOWN.
