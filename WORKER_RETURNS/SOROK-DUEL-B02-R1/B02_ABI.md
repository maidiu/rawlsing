# B02 historical calendar / S46 period ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; B01-dependent bounded period adapter. Not native science, a new scheduler, a P3 psychological batch, a purchase, or a mother action.
**Implementation SHA:** `509784c2850c499d1f640c9f43c569416081d76d`.
**Start/frozen A result:** `5bc29474e769b928d9264f1607bab605e2b1c7e9`.
**Module:** `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py`.

## Explicit bases

```text
calendar_basis = "GREGORIAN_PROLEPTIC_UTC_DATE"
clock_basis    = "S46_TEST_ONLY_LOGICAL_TICK_DAY_V1"
ticks_per_day  = 1
period dates   = inclusive start / exclusive end
```

The period plan stores both the source calendar date and the derived S46 logical
clock. One calendar day maps to one declared S46 tick; this is a sourcefree
mapping, not a claim that S46 natively implements historical years. No workshop
tick is renamed as a year.

## P2 material facts

Two bounded entries in the existing P2 `world.resources` checkpoint, written by
`p2_owner.write_material_fact`:

### `p6_employment`

```text
schema  SOROK_EMPLOYMENT_TERMS@1
grade   SOURCEFREE_FIXTURE
holder_actor_slot "A"
terms   non-empty ordered list, each exactly:
        term_id, term_version, employer_ref, role_ref, workplace_ref,
        effective_from (ISO date), daily_wage_units, currency_unit
binding root, branch, epoch, source
```

Terms must have unique `term_id` and strictly increasing `effective_from`.
`daily_wage_units` is context only; B02 performs no debit, purchase, or recurring
cost. No social-class or trait field exists.

### `p6_historical_period`

```text
schema  SOROK_HISTORICAL_PERIOD_PLAN@1
grade   SOURCEFREE_FIXTURE
calendar_basis, clock_basis, ticks_per_day
anchor_date, anchor_clock
employment_source (content source of p6_employment)
periods  non-empty ordered list, each exactly:
         period_id, start_date, end_date, start_clock, end_clock
binding root, branch, epoch, source
```

Periods must be contiguous, unique, bounded, and each `start_clock`/`end_clock`
must equal the declared calendar-to-clock mapping. The first period starts at
the anchor. The plan references the employment content source; it does not copy
a second employment ledger.

Default fixture:

```text
2026-01-01 -> 2026-07-01   (period:2026-h1, 181 days)
2026-07-01 -> 2027-01-01   (period:2026-h2, 184 days)
term A effective 2026-01-01; term B effective 2026-03-15
```

The first period's S46 domain is split into two segments at the term-B effective
date; the second period has one segment.

## Public API

```text
default_employment_terms() -> editable term content list
default_periods() -> editable date-only period list
period_plan_fixture(session) -> editable plan content fixture (not committed)

establish_period_plan(session, *, employment=None, plan=None) -> plan read
    idempotent for equal existing facts; different existing facts refused.
    Writes p6_employment then p6_historical_period through the P2 material writer.
    Does not advance the clock or produce an interval.

read_employment(session) -> SOROK_EMPLOYMENT_TERMS_READ@1
read_period_plan(session) -> SOROK_HISTORICAL_PERIOD_PLAN_READ@1
materialize_periods(session) -> SOROK_PERIOD_MATERIALIZATION@1
read_material_period(session, as_of_date) -> SOROK_MATERIAL_PERIOD_READ@1
p3_interval_span(session, period_id) -> {"mode": "SCHEDULED_ONLY", "span": int}
```

`materialize_periods` calls the existing `session.produce_interval` S46 producer
with `SCHEDULED_ONLY` domains. It creates no new clock, scheduler, database,
daily-event stream, or P3 psychology. Existing S46 interval states with the exact
domain hash are reused; a retry returns the same state IDs and appends no
duplicate period. A missing interval whose start is already in the past is
refused; the clock is never rewound. `materialize_periods` on an inherited fork
plan is refused because S46 state is not forked.

`read_material_period(as_of_date)` returns:

- the containing dated period and its source/logical clocks;
- the derived `logical_tick`;
- the latest employment term whose `effective_from <= as_of_date`, or
  `employment=None` with `employment_status=UNKNOWN_NO_EFFECTIVE_TERM`;
- the actual S46 interval summary by domain hash, or `interval_status`
  `NOT_MATERIALIZED` / `NOT_AVAILABLE_ON_FORK`;
- `provenance` with `scope=P6_MATERIAL_PERIOD_ONLY`, `stored_branch`,
  `current_branch`, `inherited`, and `fork_state`;
- source hashes and a read boundary: `psyche_store=NOT_READ`,
  `psychology_state=NOT_WRITTEN`, `class_to_trait=NOT_APPLIED`,
  `model_prose=NOT_READ`.

`p3_interval_span` returns only the existing `EventProposal.interval` shape
(`mode`, `span`) for the next P3 cycle. The existing `P2Owner.validate_proposal`
accepts it; it is not a P3 psychological transition.

## Preservation and impact

- Existing S47/P2 material ownership and B01/B03 household/dwelling readers are
  unchanged except for the P2 material-slot allowlist addition.
- Existing S46 producer/state validation is reused; period intervals are
  `SCHEDULED_ONLY` (`NOT_PERFORMED`) and carry no actor psychology.
- B02 is independent of B03; both are B01 children. B02 does not create a
  purchase, possession, mother decision, utterance, or trait.
- Pair2 D02 may consume `read_material_period`/`p3_interval_span` after HQ
  reconciliation; do not silently rebase the active D02 input.
- `p2_owner.py` byte changes alter `P3Owner._code_pins()/config_hash`. Roots from
  `5bc29474e`, A's `993339851`, B's `362719b40`, and earlier cuts refuse cold
  reopen under this final code. Fresh final-code roots are used; no migration or
  pin weakening is performed.

## Proof boundaries

No native/science/rights/human/merge authority. No full P3 cycle execution, no
actual daily work/care/participation, no purchase/debit/refusal operation, no
recurring cost, no multicycle B05, no mother action, no cold fork, and no
same-root psychological fact. S46 `SCHEDULED_ONLY` means a period/clock state, not
that the actor performed workshop work in every interval. The two complete
ChatGPT Library architecture sources remain NOT_INSPECTED locally.
