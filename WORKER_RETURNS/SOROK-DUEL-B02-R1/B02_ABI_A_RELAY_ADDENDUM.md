# B02 ABI — Agent A relay addendum

**Base:** B's `B02_ABI.md` remains the B02 material-period contract.
**Adds:** incremental dated advancement, durable period receipts, progress, crash recovery, and as-of currentness.
**Grade:** `SOURCEFREE_S2_ONLY`; no native calendar or psychology.

## Incremental API

```text
materialize_to(session, as_of_date) -> SOROK_PERIOD_MATERIALIZATION@1
    advances only current_clock .. target_clock
    target outside plan or < current clock refused
    no rewind, no duplicate interval, no all-period pre-advance
    one SCHEDULED_ONLY state and one P2_B02_PERIOD_MATERIALIZATION receipt
    per newly advanced slice; splits at employment changes only inside the slice

period_progress(session, period_id) -> progress document
    status BEFORE|PARTIAL|COMPLETE
    elapsed_ticks, remaining_ticks, current_date
    b02_coverage, b02_covered_ticks
    state_coverage, state_covered_ticks (including ACTUAL P3 intervals)
    uncovered, uncovered_ticks
    b02_state_ids, other_state_ids
    remaining_segments, next_p3_span

remaining_span(session, period_id, to_date=None) -> span document
    current-progress-subtracted; 0 for a completed period

p3_interval_span(session, period_id, to_date=None) -> {"mode","span"}
    exact P3 EventProposal.interval shape; span is NOT the full period
    once time has elapsed

materialize_periods(session) -> whole-plan wrapper over materialize_to
```

`P2_B02_PERIOD_MATERIALIZATION` receipts are C12 episodes carrying plan/employment sources, period, target, state/domain identity, start/end, segments, public_event=NOT_EMITTED and the read boundary. `_recover_missing_receipts` appends a `RECOVERED` receipt exactly once when a matching `SCHEDULED_ONLY` state exists without a receipt (the state-before-receipt crash window). Retry does not duplicate a receipt.

## As-of currentness

`read_material_period(session, as_of_date)` retains B's period/employment/interval fields and adds:

```text
as_of_relation              PAST | CURRENT | FUTURE
employment_is_current       bool
employment_currentness      CURRENT_AS_OF | PAST_AS_OF | FUTURE_NOT_CURRENT
current_employment          employment effective at the current world clock
current_employment_status
interval_status_detail      MATERIALIZED_AT_AS_OF |
                            MATERIALIZED_RETROSPECTIVELY |
                            ELAPSED_BY_OTHER_OWNER |
                            FUTURE_NOT_MATERIALIZED |
                            NOT_MATERIALIZED_AT_AS_OF |
                            CURRENT_NOT_MATERIALIZED
state_admitted_clock
state_available_at_as_of
retrospective
current_interval
current_interval_status
period_progress
```

A future as-of date may plan/read a future term under `employment`, but it is
never `employment_is_current` and `current_employment` is the term at the
current clock. A past as-of read of a state produced later is `retrospective`
and `MATERIALIZED_RETROSPECTIVELY`. A P3 ACTUAL interval covering the as-of tick
is `ELAPSED_BY_OTHER_OWNER`, never a B02 period state.

## P3 interleave

`P3Owner.realize` is an actual P3 DevelopmentOwner cycle; B02 does not run a full 3–5 event `BatchEngine` batch. B02 period states remain `SCHEDULED_ONLY` (`NOT_PERFORMED`). An ACTUAL P3 interval is distinct from B02 receipt states and appears in `other_state_ids`/`state_coverage`; event-tick gaps between an interval end and an event clock are reported in `uncovered`, not fabricated.

## Invariants

- No second clock, scheduler, ledger, P3 psychology, or performed work claim.
- No duplicate period, receipt, state, or P3 span after progress.
- No rewind to a past target.
- No future employment claimed as current.
- No past as-of presented as a current snapshot.
- Calendar/S46 mapping remains the declared sourcefree hypothesis, not native historical time.
