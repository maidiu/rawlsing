# B05 interleave/restart ABI — B revision

**Status:** `SOURCEFREE_S2_ONLY`; actual `BatchEngine` cross-boundary material interleave with typed parent join at frozen composition `46a815643440857ff1185481a5e27ef7023e541f`.
**Implementation SHA:** `ef2129283fff3deffab8cefef6ff94da3045bc58`.
**A production:** `d2a0a4eadab4ba99ae830c8e47013e60295a4632`.
**Base:** `B05_ABI.md`; `B05_A_SEMANTIC_ADDENDUM.md` is superseded where it says the typed parent hook is pending. `B05_B_ABI_REVISION_PRE_TYPED.md` is historical.

## PeriodInterleaveOwner (revised)

```text
rolling_reproduction.PeriodInterleaveOwner(owner, session, after_event_dates)
    after_event_dates: Mapping[exact P3 event_id -> target ISO date]
    snapshot/validate_proposal delegate to the real P3Owner
    realize:
      - validate the target date is inside the B02 plan before calling owner
      - delegate to the real P3Owner
      - advance B02 materialization only for that event id
      - return RealizedEvent with after = current post-material owner snapshot
      - objective.b02_materialized_after_event carries target/status/clock
```

The mapping is **event-id keyed**, not an in-memory position. A restarted adapter
therefore cannot assign event 5's date to event 4 or skip/duplicate a period
because an index was lost. `_index` is removed from the control path.

### Retry after a committed event and B02 advance

P3Owner's normal replay checks that its recorded after state is the current
composite state. After this adapter legitimately advances B02 following an
event, that check can refuse `P3_REPLAY_STATE_MISMATCH`. `PeriodInterleaveOwner`
recovers only when the P3 store has a `COMPLETE` operation for the same
operation id/proposal hash and its recorded `before` equals the expected state.
It returns that durable P3 result—receipt_ref, readset, objective, accessible,
consequences copied—without calling the owner again or writing P3. It then
reports the target as `ALREADY_CURRENT`/`ALREADY_ELAPSED` if B02 already covers
it, or performs the single missing B02 advance. This is finite reconciliation of
one committed event, not a second action or fabricated receipt.

A target already elapsed before the adapter call is `ALREADY_ELAPSED`; no B02
rewind and no new span. A target outside the plan is refused before the P3 event
is delegated.

## Proved batch

Actual `BatchEngine` three-event run (events 4–6) with exact existing plan
hashes, custom B02 employment change 2026-01-20, pre-batch materialize to
2026-01-16, then B02 advances after each event (2026-01-22, 2026-01-26,
2026-02-01), crossing the split. The test asserts:

- 3 actual P3 records with `MISSING_RULE`;
- B02 split/currentness: old term at 2026-01-19, `civic-works` at 2026-01-21;
- exact target/status/clock per event; no wrong next date;
- B02 receipt for the 2026-01-22 target appears once;
- post-batch B04 typed purchase; C02 parent read/options/history READ;
- B05 completed-period rent; B03 feasibility change; P3 head unchanged;
- `period_uncovered` reports event-tick gaps; no scheduled-work/psyche claim.

Restart/retry test `test_b05_interleave_retry.py` injects a failure after the
first B02 target is committed but before the BatchEngine event record, then
resumes on the same journal with a fresh adapter. It proves event 4's target is
not reused, no duplicate 2026-01-22 receipt/span is created, events 4–6 each have
one record, and receipt_ref/readset remain the durable P3 values.

## Preserved rent/parent rules

- rent only on a COMPLETE B02 period; one rent per period; duplicate operation
  REPLAY; different operation refused;
- B01 fixed-A household cash only; parent C02 cash untouched by rent;
- refusal/no cash no debit; state-root rent lock and one `_StoreWrite`;
- typed C02 parent purchase history now consumed by parent material/options/
  history; no bridge or fake activity;
- no public event/perception, psyche, trait, scheduled-work or currency
  conversion; no landlord/arrears model; no cold fork/P6 live claim;
  native/science/rights/human/merge held; prior P3 roots incompatible.
