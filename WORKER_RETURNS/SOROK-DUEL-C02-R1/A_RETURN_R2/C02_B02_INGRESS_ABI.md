# C02 B02 current-period ingress ABI

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; current-period B02 ingress implemented. Full two-period/incremental C02 remains held.
**Implementation SHA:** `9ac1ac71cdbc8dd2c832b2980b501b4031e163e8`.
**B02 source:** `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py` at composition `ea1f8d75b894c28d8a7bdb2d667761af2b67e310` (not edited or copied).
**B frozen C02 return:** `4d93685df4c5abdfbd09f44510a24a41c850b6a8`; B implementation `3f9d1079bc3b1f09a318afc80bd5aa63d7ccdecf`.
**Contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.

## Qualification

`parent_activity._period_context(session)` loads the actual B02 module and calls its public readers:

```text
historical_period.read_period_plan(session)
historical_period.read_material_period(session, current_date)
```

The current date is derived from the committed B02 plan's `anchor_date`, `anchor_clock` and `ticks_per_day` and the actual current S46 clock. The result must satisfy:

```text
period_context.status = B02_PERIOD_CONTEXT_READ
period_context.logical_tick = session.clock()
period_context.period = current B02 dated period
```

If no B02 plan is established on the root, status is `B02_PERIOD_PLAN_ABSENT_ON_ROOT` (current-clock parent activity remains possible with no dated claim). If a plan exists but the current clock is before/discontinuous/outside the plan, status is `B02_PERIOD_CONTEXT_UNQUALIFIED`, parent options are `HELD` with `B02_PERIOD_UNAVAILABLE`, and parent writes refuse `PARENT_ACTIVITY_B02_PERIOD_UNAVAILABLE`.

`PARENT_B02_HOLD` now means only `B02_PERIOD_PLAN_ABSENT_ON_ROOT`; the old global `HELD_B02_CALENDAR_ABSENT` claim is superseded. `PARENT_B02_QUALIFIED` is the current-period qualified state.

## Time, employment and currency bases

A qualified context carries:

```text
plan_source, employment_source, period, as_of_date, logical_tick,
calendar_basis, clock_basis, ticks_per_day, interval_status, provenance
```

B02's default employment holder is actor `A`. It is **never** applied to the parent:

```text
b02_employment_holder_actor_slot = "A"
b02_employment_applied_to_parent = False
parent_employment_source = "PARENT_ACTOR_LOCAL"
```

Parent wage/rate/currency come from the registered parent material, which carries its own `currency_unit` (`parent_sourcefree_currency_unit` by default). B03 household/dwelling currency is not read or converted:

```text
material_boundary.household_cash = NOT_READ
material_boundary.household_spend_permission = C03_B04_HELD
material_boundary.currency_conversion = NOT_APPLIED
material_boundary.double_counting = NO_HOUSEHOLD_EFFECT_APPLIED
```

## Bindings

- `read_parent_material` and `parent_feasible_actions` return the **current** period context at read time.
- `establish_parent_material`, `commit_parent_circumstances` and `record_parent_activity` capture the current period context in their C12 episodes/receipts; activity event bodies carry the same context and bind the activity source to the period plan/period ID.
- `read_parent_activity` validates the stored period context and logical clock against the actual event; it does not substitute a later current period for the historical receipt.
- `read_parent_history` returns each row's stored period context plus the current period context.
- A B02 period-source severance makes current material/options unqualified/held but does not erase or retcon a committed activity receipt; restoring the exact plan material restores current qualification.

## Held full-dated proof

The existing B02 `materialize_periods` advances the entire plan and `p3_interval_span` returns full spans. This return does **not** call that full-plan interleaver and does not claim two dated periods, split-period cold replay, or incremental interval materialization.

Required finite hook for the B02/Pair1 owner:

```text
historical_period.current_material_period(session)
  -> exact current period, logical tick, employment-as-of and
     incremental interval state (or explicit NOT_MATERIALIZED)
     without materialize_periods advancing the entire plan
```

Until that exact incremental/current-period API exists and is independently composed, `historical_ingress.full_dated_proof` remains:

```text
HELD_INCREMENTAL_CURRENT_PERIOD_API_MISSING
```

The live-root proof uses the actual B02 plan/current-period context and records `interval_status=NOT_MATERIALIZED`; it is not a two-period claim.

## Explicit limits

- No B02 source edit, copy, rebase or full-plan materialization.
- No false global B02-not-built claim: B02 exists and is read when a plan is present.
- No two-period/cold/severance-complete C02 proof yet.
- No C03 decision/utterance or C04 Nadia uptake.
- No shared parent/household cash reconciliation, currency conversion or spending permission.
- No native/science/rights/actor/human/protected authority.
