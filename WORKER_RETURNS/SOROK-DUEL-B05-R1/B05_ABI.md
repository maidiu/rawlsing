# B05 rolling household rent ABI

**Status:** `SOURCEFREE_S2_ONLY`; depends B02/B04. Not a mother decision, public event, landlord ledger, or native science.
**Code:** final SHA `62292613aa9210a7d3e944314e36924349337439` (feature commit `a3f74693b70cb09f0e8bac4a7ca094812173db3a`).
**Module:** `WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py`.

## API

```text
apply_household_rent(session, *, operation_id, period_id,
                     expected_clock=None) -> SOROK_HOUSEHOLD_RENT_RECEIPT@1
read_household_obligation(session, operation_id)
    -> SOROK_HOUSEHOLD_OBLIGATION_READ@1
```

`apply_household_rent`:
- reads B02 `period_progress`; requires `status=COMPLETE`;
- reads B03 `read_dwelling`/`read_household`; uses `costs.monthly_rent`;
- one rent per period; a different operation for the same period refuses
  `B05_RENT_ALREADY_RECORDED`;
- debits only B01 fixed-A household cash; parent C02 cash is untouched;
- cash < rent -> durable REFUSED receipt `B05_INSUFFICIENT_HOUSEHOLD_CASH`, no debit;
- rent = 0 -> `UNCHANGED`, no debit;
- admitted: one `_StoreWrite` transaction with the actor-A cash update, one
  checkpoint and one C12 `P2_HOUSEHOLD_RENT` receipt;
- no world event/perception, no P3 psychology; `scheduled_participation=NOT_PERFORMED`,
  `event_effect=NONE`, `public_event=NOT_EMITTED`;
- idempotent operation ID; immediate/historical retry returns `REPLAY` with no
  second debit; a different operation for the same period refuses.

The receipt carries:

```text
operation_id, period_id, period_status, monthly_rent
household_cash_before/after
household_document_source
household_material_hash_before/after
dwelling_source, dwelling_material_hash
reasons, scheduled_participation, event_effect, public_event
psychology_state=NOT_WRITTEN
actual_reader=rolling_reproduction.read_household_obligation
read_boundary={psyche_store:NOT_READ, psychology_state:NOT_WRITTEN,
               class_to_trait:NOT_APPLIED, model_prose:NOT_READ}
```

`read_household_obligation` verifies the stable household document source and
dwelling source and the rent arithmetic. It returns the durable receipt,
current household cash, current household material hash and `historical`
(current cash differs from the receipt's after cash). A severed/changed
household or dwelling source refuses `B05_RENT_SOURCE_STALE`. It does not
modify the world.

## Composition

B05 composes with actual B02 periods, C02 `PAID_WORK`/`CARE_DEPENDENT`/`PAY_DEBT`
and B04 parent-funded stock purchase. It never charges parent cash for household
rent and never charges household cash for the parent's purchase. The later
reader exposes the changed household cash and B03 material feasibility; the
parent's own feasible actions are read through C02.

## Invariants

- One rent per completed dated period; no duplicate cost.
- No negative household balance; refusal does not debit.
- No parent-cash debit for household rent; no household-cash debit for parent purchase.
- No elapsed-time trait, memory, automatic psyche or performed-work claim.
- No public event/perception, landlord ledger, variable rent/arrears, or currency conversion.
- No new scheduler, clock or database; the receipt is a C12 episode, cash is the existing P2 actor state.
