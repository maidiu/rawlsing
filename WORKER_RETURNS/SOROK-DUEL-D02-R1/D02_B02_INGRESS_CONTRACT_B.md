# D02 → B02 ingress contract — B incremental current-period addendum

**Status:** `B02_SOURCE_PRESENT_INCREMENTAL_CURRENT_PERIOD_IMPLEMENTED__FULL_HISTORICAL_D02_HELD`. This addendum supersedes only the stale “B02 globally unbuilt / whole-plan hold” wording in the A contract. It is not full D02 acceptance, a period writer, a mock calendar or native/actor authority.

**Actual B02 source at this composition:** `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py`, SHA-256 `d1d4171af95f4d87fa9e174159cde46270d12331c728c4462251b488b0cb49c7`.

**Actual selected symbols:** `read_period_plan`, `period_progress`, `read_material_period`, `p3_interval_span`.

## D02 B repair

`p3.situated_context._period_ingress` now:

1. reads the actual B02 plan and validates the declared anchor/ticks basis;
2. selects the current declared period by the current P3/S46 logical clock;
3. reads the actual incremental `period_progress(session, period_id)` and requires its clock/current period to match;
4. uses `progress.current_date` as the current date, not a private anchor-date arithmetic path;
5. reads `read_material_period(session, current_date)` and requires `logical_tick == current P3 clock`;
6. returns the typed `p3_interval_span` read-only seam and includes exact `period_source` and `period_progress` status/currentness/coverage.

The current-period ingress still does **not**:

- advance or materialize the S46 clock;
- treat a historical as-of date as current physical state;
- apply a whole-plan materializer or a P3 interleaving;
- claim the P4/P6 live-root join;
- treat employment/material/period as actor knowledge, parent reason or a mediator.

## Current-period hold/refusal

`period.status = QUALIFIED_CURRENT_PERIOD` only with actual period/employment facts, holder A matching the focal identity, an in-plan day-aligned current clock, matching `period_progress` clock/period and matching `read_material_period.logical_tick`. Missing plan/employment is held; tampered sources refuse; before/outside/non-day-aligned clocks hold; a future employment term is not read as current.

## Still held for full D02/B02

Actual B02-to-P3 interleaving, dated midperiod batch, multi-period cold replay, a later actor decision consuming the period through the interval seam, and the normal P4/P6 live-root consumer remain held. They require the Pair1/B05/Pair3 qualified hooks at a later composition; this addendum does not fabricate them.

## Consumer and first reader

The incremental current-period document is consumed by `p3.situated_context.build_situated_context` and reaches the existing `RecursionCycle` provider context. The provider remains transport; the actual P3 response/consumer remains the separate P3/D03 boundary.
