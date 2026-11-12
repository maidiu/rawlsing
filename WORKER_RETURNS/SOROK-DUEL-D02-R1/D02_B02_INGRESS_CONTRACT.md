# D02 → B02 ingress contract

**Status:** `B02_SOURCE_PRESENT_CURRENT_PERIOD_INGRESS_IMPLEMENTED__FULL_HISTORICAL_D02_STILL_HELD`. The B02 reader is no longer globally unbuilt at this composition. D02 now consumes the actual B02 `read_period_plan`/`read_material_period`/`p3_interval_span` source for a **current logical-clock period only**. Historical as-of queries, historical period interleaving and full D02 acceptance remain held.

**B02 source at this composition:** `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py`, SHA-256 `78e33649ed7c2a50d1cdea1692f04ea79ddb841748f7532d576c0436647ded22`; symbols `read_period_plan`, `read_material_period`, `p3_interval_span`.

**B02 source declaration:** Gregorian proleptic UTC date plus declared S46 logical tick-days; `ticks_per_day` is read from the actual plan. No workshop tick is renamed as a calendar year. This document is not a period, mock calendar, writer or acceptance.

## What D02 now supplies

`p3.situated_context.build_situated_context` supplies a read-only decision input with:

- exact P3/S47 root/actor/branch/logical-clock/state identity;
- objective P6/B01 household material through `house.read_household`;
- qualified focal-actor perception through C01 `read_actor_access`, selected by actual event time/ordinal;
- event-time shared perception separated from current objective position co-presence;
- an optional **current B02 period read**: current logical clock is mapped through the actual B02 plan's `anchor_date`/`anchor_clock`/`ticks_per_day` to `as_of_date`; `read_material_period` must return the same logical tick; the selected period, employment term and typed `p3_interval_span` are bounded read-only fields;
- exact `period_source` SHA-256 for the B02 reader in the body/readset/hash;
- exact D02 source closure and acquired-state readset;
- no raw PsycheStore payload, memory/narrative, parent private state or portal user view.

The B02 employment holder is checked against the focal actor: holder slot `A` must resolve to the D02 identity actor. D02 never silently applies holder-A employment to a registered parent or any other actor. Employment is objective household-period material, not actor knowledge, a trait, a decision or a parent action.

## Current-period ingress shape

`period.status = QUALIFIED_CURRENT_PERIOD` only when all of the following hold:

- actual `p6_employment` and `p6_historical_period` facts exist and validate;
- the current session clock is at or after the plan anchor;
- `(clock - anchor_clock) % ticks_per_day == 0`;
- the derived date lies inside a declared period;
- `read_material_period` returns `logical_tick == current P3 clock`;
- employment holder slot `A` resolves to the focal identity actor.

Returned fields include `as_of_date`, `logical_tick`, `period`, `employment`, `employment_status`, `holder_actor_slot`, `holder_actor_id`, `interval`/`interval_status`, `interval_span` (`SCHEDULED_ONLY`, typed only), `plan_source`, `employment_source`, `provenance`, exact `period_source`, and `date_scope.calendar = B02_CURRENT_LOGICAL_PERIOD`.

If the plan is absent, the current clock is before/outside the plan, the clock is not day-aligned, or the holder is not focal, the selector returns `period.status = HELD` with the exact reason. It does not invent a period or advance a clock.

**A historical as-of query is not current physical state.** D02 derives only the date corresponding to the current logical clock. It does not expose a historical-date selector and does not read future employment as current. Historical B02 dates are a separate future operation.

## Still held for full D02/B02 coupling

The B02 materializer is still a whole-plan S46 scheduling operation, not actual P3 interleaving. D02 has not applied `p3_interval_span` to a real P3 proposal, has not run a dated midperiod P3 batch, and has not proved the B02 period split against an actual later actor decision. Pair1 A is counterstriking the materializer/interleaving API; B04/B05 own purchase/duration.

Full D02 remains held until a qualified cut demonstrates on actual dated periods:

1. two periods plus a midperiod consequential change split at the effective event;
2. preserved source clocks and no duplicated/overlapping period;
3. cold replay with identical period sequence/readset;
4. a later actual P3 consumer reading the period/material input through its interval seam;
5. an explicit no-change/silence case and wrong-clock/overlap refusal;
6. exact selected-reader source closure including any changed B02/P3 source.

## Refusal conditions

D02 refuses or holds before using a period when:

- the employment/period material fact is missing (held);
- source/root/branch/clock/identity is stale or foreign (refuse);
- a stored fact source is tampered (B02 refusal propagates);
- period bounds or the logical tick do not match the current clock (hold/refuse);
- current clock is outside the plan or not day-aligned (hold);
- holder slot A is not the focal identity actor (hold);
- a mock, narration-derived or curated period is presented as B02 (not part of this interface);
- a period would be used as actor knowledge, parent private reason, trait, possession, decision or performed action (forbidden).

## Consumer and first reader

The B02 current-period document and the acquired-state activation read are consumed by `p3.situated_context.build_situated_context` and reach the existing `RecursionCycle` provider context for a later actual P3 proposal input. The provider remains transport; no provider choice is treated as actor cognition.

## Evidence already produced

- `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_a_acquired_period.py` establishes the plan on a fresh actual root; reads period `period:2026-h1`, term `employment:workshop-cooperative`, logical tick 222, `NOT_MATERIALIZED`, typed span 181; advances the actual P2 clock to 312 with a real event and reads `2026-04-01`/`employment:civic-works`; severs/restores the period fact and exact baseline hash; tampers/restores employment source and refuses.
- The fresh-root composition test establishes B02, B01 household, C01 parent access, D01 retention and D02 acquired state on one root.
- B02's own materialization/split/cold evidence remains B02's candidate evidence, not D02 acceptance.

This is sourcefree current-period engineering. It does not claim full historical recursion, P3 interleaving, native science, actor/human rights or protected acceptance.
