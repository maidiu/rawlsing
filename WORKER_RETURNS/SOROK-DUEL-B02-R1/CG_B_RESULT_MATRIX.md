# CG-B result matrix and independent receiving request

**Sourcefree candidate head:** `ef2129283fff3deffab8cefef6ff94da3045bc58` (B02 production inherited `d2a0a4eadab4ba99ae830c8e47013e60295a4632`).
**Frozen composition:** `46a815643440857ff1185481a5e27ef7023e541f` (clean auto-merge, unaccepted).
**Grade:** `SOURCEFREE_S2_ONLY`; native/science/rights/actor/human/protected authority not issued.
**Receiving status:** **NOT_ACCEPTED**. A/B are competing authors; one independent nonauthor receiving is requested for this coherent CG-B tranche.

## Packet matrix

| Packet | Status | Actual first consumer / evidence | Limits |
|---|---|---|---|
| B01 | `ACHIEVED_SOURCEFREE_CANDIDATE` | P2/S47 household material -> P6 `read_household`/`parent_choice_input`; B01 tests; fork provenance. | No parent first consumer; P3 code-pin roots incompatible. |
| B02 | `ACHIEVED_SOURCEFREE_CANDIDATE` | Dated P2 employment/period facts -> S46 `materialize_to` -> `read_material_period`/`period_progress`; actual 3-event `BatchEngine` across split; 9 tests. | Full 5-event cross-boundary batch and crash between B02 materialize and next event not proved; `period_uncovered` gaps reported. |
| B03 | `ACHIEVED_SOURCEFREE_CANDIDATE` | P2 dwelling/tenancy/space/acoustics/cost -> `read_dwelling`/`material_feasibility`; same-root PsycheStore negative. | Child new occupancy, owned/other tenure, cold fork limited. |
| B04 | `ACHIEVED_SOURCEFREE_CANDIDATE` | Typed `P2_PARENT_PURCHASE` -> C02 typed parent material/options/history/read -> second purchase/read_purchase -> B05 rent/B03 feasibility. | No public event/Nadia perception, household-funded alternative, fork/cold-fork; no general economy. |
| B05 | `ACHIEVED_SOURCEFREE_CANDIDATE` | One rent per completed B02 period -> B01 household cash/B03 feasibility; cross-boundary batch; 7 tests. | No 5-event batch, arrears/landlord/variable rent/currency conversion, full P6 live/fork. |
| C/D/E/F/G | `NOT_EXECUTED` | Downstream 27-task programme remains. | Full 22 remaining packets not done. |

## Actual join proved

```text
B02 current period
-> typed B04 parent-funded purchase (currency equal; parent debit/stock/ownership/checkpoint)
-> C02 read_parent_material / parent_feasible_actions / read_parent_history (typed purchase row, no bridge)
-> next parent PAID_WORK
-> second B04 purchase (stock/ownership/debit) -> read_purchase historical
-> B02 complete period -> B05 rent (fixed-A household cash 55->43)
-> B03 feasibility REFUSED_AFFORDABILITY
```

Separately, a real three-event `BatchEngine` crosses the B02 employment split with B02 `materialize_to` after each event; P3 records preserve `MISSING_RULE`. Interleave retry is event-id keyed and recovers a committed P3 result after B02 advance without a second action.

## Commands / evidence

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py \
  WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_composition.py
# 7 passed in 111.82s — evidence/b04_b_typed.log
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_cross_batch.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_batch_cycle.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rollback.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_zero_and_held.py \
  WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_interleave_retry.py
# 7 passed in 283.62s — evidence/b05_b_typed.log
# combined B01+B02+B03+B04+B05: 43 passed in 613.49s — evidence/b01_b02_b03_b04_b05_b_typed_combined.log
```

## Negative/source/consumer boundaries for the receiver

- Typed purchase: no antecedent bridge, no WORK/DEBT/CIRCUMSTANCE fake, one admitted purchase row per admitted operation, refused purchase before=after/no possession.
- Currency: parent == market == request unit; mismatch refuses before debit; no conversion.
- B04/B05 crash: injected checkpoint failure rolls back receipt/material/stock/ownership/rent; cold reopen.
- B02: past/outside target refused; no duplicate period/receipt; future employment not current; retrospective/other-owner labels.
- Interleave: event-id keyed; failure after B02 advance before BatchEngine record recovered once; no duplicate span/receipt/event.
- No public event/Nadia perception, no mother decision/utterance/uptake, no P3 psychology/trait, no second scheduler/ledger.
- P3 code-pin roots from prior cuts incompatible; no migration/weakening.
- Full Library conceptual/operational sources remain NOT_INSPECTED locally.

## Receiving request

Request one genuinely independent nonauthor exact-source receiving of the coherent CG-B tranche at/after `ef2129283fff3deffab8cefef6ff94da3045bc58`, including code/test/source ancestry, both-class material negatives, actual parent/P6 consumers, cold/restore/severance, and this matrix. Do not treat the written handoffs, passing tests, or A/B mutual checks as terminal acceptance. Preserve native/science/rights/actor/human/protected holds.
