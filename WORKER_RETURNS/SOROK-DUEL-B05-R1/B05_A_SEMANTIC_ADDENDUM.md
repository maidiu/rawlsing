# B05 ABI — Agent A semantic interleave addendum

**Base:** `B05_ABI.md` remains the rent receipt/reader contract. B's `B05_B_ABI_REVISION.md` is historical; its B04 bridge dependency is not adopted.
**Code:** `d2a0a4eadab4ba99ae830c8e47013e60295a4632`; B lock/rollback from `4a3c45c` retained.
**Grade:** `SOURCEFREE_S2_ONLY`.

## Cross-boundary BatchEngine adapter

```text
rolling_reproduction.PeriodInterleaveOwner(owner, session, after_event_dates)
    snapshot() / validate_proposal(proposal) delegate to the real P3Owner
    realize(operation_id, proposal, expected):
        result = owner.realize(...)
        hp.materialize_to(session, next_after_event_date)
        return RealizedEvent(..., after=owner.snapshot(), ...)
```

This is a thin orchestration adapter, not a P3 owner/scheduler. The real
`BatchEngine` still owns batching/reservation/replay/record validation. B02
materialization occurs after selected real events; the next event sees the
advanced period. The adapter reports `objective.b02_materialized_after_event`.

Proved three-event cross-boundary cycle:

```text
B02 custom employment change 2026-01-20
-> materialize_to 2026-01-16
-> BatchEngine events 4–6 (real P3 owner)
-> materialize_to 2026-01-22 after event 4 (crosses split)
-> materialize_to 2026-01-26 after event 5
-> materialize_to 2026-02-01 after event 6
-> parent-funded B04 purchase
-> materialize_to 2026-07-01; B05 rent period 1
```

Reads: 2026-01-19 old employment term, 2026-01-21 `civic-works`; B02 state
segments split at the change; 3 batch records with `MISSING_RULE`; P3 head
unchanged by B04/B05; rent 55→43; B03 feasibility REFUSED_AFFORDABILITY;
`period_uncovered` reports event-tick gaps; no scheduled-work/psyche claim.

## Parent work and the typed purchase boundary

Parent C02 material is declared in the same `sourcefree_currency_unit` as the
B04 market/request in the B05 tests; a different parent unit would make the
purchase refuse, not convert. Parent C02 `PAID_WORK` is performed **before**
the B04 purchase in the B05 test. After the admitted purchase, C02 parent material/feasible/activity reads
refuse `PARENT_MATERIAL_HISTORY_MISMATCH` because the typed
`P2_PARENT_PURCHASE` history hook is pending. B05 rent continues (it uses B01
household cash and B03 dwelling, not parent material). No antecedent bridge,
WORK/DEBT/CIRCUMSTANCE fake, or second purchase is used to make the test green.

After Pair3 adds the typed hook (see `SOROK-DUEL-B04-R1/B04_A_SEMANTIC_ABI.md`),
post-purchase parent work/feasible actions and a second purchase can be tested;
the bridge must remain removed.

## Zero and held rent

`test_b05_zero_and_held.py` proves a completed period with insufficient household cash produces a durable REFUSED `B05_INSUFFICIENT_HOUSEHOLD_CASH` receipt and no debit, and a zero `monthly_rent` produces `UNCHANGED` with no debit. A later different operation for the same period is `B05_RENT_ALREADY_RECORDED`; there is no arrears model.

## Preserved rent invariants

- rent only on a `COMPLETE` B02 period;
- one rent per period; duplicate operation REPLAY; different operation refused;
- B01 fixed-A cash only; parent C02 cash untouched;
- refusal/insufficient cash no debit; no negative balance;
- B05 state-root lock and one `_StoreWrite` checkpoint/receipt rollback;
- no public event/perception, P3 psychology, trait, or scheduled-work claim;
- historical receipt arithmetic/stable source check; cold exact.

## Limits

Three-event bounded cross-boundary batch, not five; no crash between a B02
materialize and the next P3 event; typed C02 purchase hook pending; no mother
decision/utterance/uptake, public event/Nadia perception, arrears/landlord/
variable rent/currency conversion, cold fork, full P6 live turn, native/science/
rights/human/merge, or old P3 root compatibility.
