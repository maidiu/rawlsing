# B05 rolling household reproduction ABI — B revision

**Status:** `SOURCEFREE_S2_ONLY`; B02/B04-dependent recurring material obligation. Not a mother decision, public event, landlord ledger, or native science.
**Implementation SHA:** `4a3c45cda7d814df0c60ca4e245499fcfca62162`.
**Frozen composition start:** `2a47fb389b453c2f902b8c13ed52304fb40efd0d`.
**A production:** `62292613aa9210a7d3e944314e36924349337439`.
**Base ABI:** `B05_ABI.md` remains the receipt/reader contract; this revision adds serialization, rollback proof and the B02/B04/P3 integration.

## API (unchanged shape)

```text
apply_household_rent(session, *, operation_id, period_id,
                     expected_clock=None) -> SOROK_HOUSEHOLD_RENT_RECEIPT@1
read_household_obligation(session, operation_id)
    -> SOROK_HOUSEHOLD_OBLIGATION_READ@1
```

Rent is charged only on a `COMPLETE` B02 period, one rent per period, against
B01 fixed-A household cash, using the B03 dwelling `monthly_rent`. Parent C02
cash is untouched. An insufficient-cash period is a durable REFUSED receipt with
no debit; a duplicate operation replays; a different operation for the same
period refuses `B05_RENT_ALREADY_RECORDED`. No world event/perception, P3
psychology, automatic trait, or scheduled-work claim is created.

## B revision: one-rent serialization

`apply_household_rent` now takes a state-root `rolling_reproduction.lock` around
the complete read/check/write unit. This is a file lock over the existing P2/C12
writers, not a scheduler or ledger. It prevents two callers from both observing
no rent for a period and each appending a debit/receipt. A per-operation retry
remains REPLAY; a different operation on the same period remains
`B05_RENT_ALREADY_RECORDED`.

## B revision: crash rollback

The admitted path remains one `_StoreWrite` transaction:

1. update fixed-A household cash;
2. checkpoint the existing P2 world;
3. re-read the household after state;
4. append the C12 `P2_HOUSEHOLD_RENT` receipt.

An injected failure at the checkpoint leaves no cash update and no receipt; cold
reopen returns the pre-rent cash and `B05_RENT_NOT_FOUND`. A subsequent valid rent
then debits exactly once.

## B revision: actual material/P3 cycle

The B integration test now runs:

```text
B02 custom employment split at 2026-01-15
-> materialize_to 2026-01-16
-> actual P3 BatchEngine 3-event batch (events 4-6)
-> B04 parent-funded purchase
-> materialize_to 2026-07-01
-> B05 rent period:2026-h1
```

The batch is a real three-event `BatchEngine` run with exact existing plan
proposal hashes; it is not a fixture masquerading as actor acquisition. The
purchase and rent are real P2 material operations after the batch. The B02
employment split is read as `civic-works`; the purchase is parent-funded and
ownership/stock change; the rent changes household cash 55→43; B03 junior-kit
feasibility becomes `REFUSED_AFFORDABILITY`; the P3 store head is unchanged by
purchase/rent. B02's `period_progress` may report P3 event-tick gaps; the B05
receipt carries `period_uncovered` rather than pretending full scheduled
participation. B05 does not charge rent inside a B02 period before `COMPLETE`.

## Downstream composition

- B04 must retain its C02 material-history bridge (see `B04_B_ABI_REVISION.md`);
  without it, B05 parent reads fail at the frozen C02 composition.
- C02 `PARENT_B02_HOLD` and `historical_dates=NOT_AVAILABLE` remain stale
  Pair3-owned literals. B05 uses actual B02 periods and does not treat the
  literal as authority. Exact hooks: see B04 revision and main handoff.
- D02/C02 active inputs are not rebased; B02/B04/B05 ABI is frozen at this cut.
- P3 code-pin roots from all prior p2_owner cuts remain incompatible; no migration.

## Proof boundaries

No landlord balance, arrears settlement, variable rent, multi-currency
conversion, public event/Nadia perception, mother decision/utterance, full
household economy, cold fork, native/science/rights/human/merge authority. One
rent per completed period is bounded; a refused rent blocks a different
operation for that period (no arrears model). Full B02 schedule coverage is not
claimed when P3 event ticks create gaps; those gaps are reported.
