# D02 → B02 ingress contract

**Status:** `PREREQUISITE_HELD_NOT_QUALIFIED`. B02 is not built at this cut. This document is the exact finite ingress D02 will require at the next reconciliation; it is not a period, calendar, date, mock fixture, writer or acceptance.

## What D02 already supplies

`p3.situated_context.build_situated_context` supplies a current-logical-clock, read-only situated input:

- exact P3/S47 root/actor/branch/clock/state identity;
- objective P6/B01 household material through `house.read_household`;
- qualified focal-actor perception through C01 `read_actor_access`, selected by actual event time/ordinal;
- event-time shared perception separated from current objective position co-presence;
- explicit `date_scope.calendar = HELD_B02_NOT_BUILT`;
- exact D02 source closure and a readset/hash;
- no `period`, `as_of` date, calendar year, historical split or parent-private/portal read.

## Required B02 ingress (exact finite shape)

B02 must be the existing P3 `DevelopmentOwner`/S46 logical clock plus the existing P2 objective world, not a new scheduler, database or calendar owner. At its qualified cut it must supply one validated document with these exact semantic fields:

| Field | Required meaning |
|---|---|
| `schema` | a declared B02 ingress schema version |
| `root`, `actor`, `branch` | exact P3/P2 identity, no derived or foreign root |
| `clock_basis` | `S46_LOGICAL` and the exact source clock units; no implicit year mapping |
| `as_of` | one logical clock and one period id for the read |
| `period.effective_from`, `period.effective_to` | same S46/P2 units, ordered, non-overlapping with the next accepted period |
| `period.split` | the actual event id/effective clock and reason for any midperiod job/move/resource change |
| `source` | B02 implementation/source identity plus world/source hashes |
| `world` | exact world root/branch/state hash at `as_of` |
| `material_as_of` | household/material source and world hash at `as_of` |
| `actor_as_of` | actor participation/access epoch at `as_of` |
| `evidence` | source refs, split evidence, cold replay receipt and later first-consumer reference |

Any calendar mapping must be separately declared and sourced. Workshop logical ticks must not be relabelled as calendar years. D02 will not infer a period from event counts, elapsed logical ticks, filesystem time, prompt prose or the current clock.

## Refusal conditions for B02 ingress

D02 must refuse, before reading material or actor access:

- missing/ambiguous root/actor/branch or as-of clock;
- period bounds in a different unit from the selected P3/P2 clock;
- overlapping periods, unsorted bounds, or a split not bound to an actual event/effective clock;
- stale world/material/actor-as-of hash versus the exact current root state;
- a mock, curated or narration-derived period presented as B02;
- a source identity that cannot be pinned to the selected B02 implementation.

## Consumer and first reader

The B02-qualified document must be consumed by `p3.situated_context.build_situated_context` and reach the existing `RecursionCycle` provider context for a later actual P3 proposal input. D02 will not treat the period document as a decision, trait, memory, parent private reason or performed act.

## Reconciliation evidence required

Before D02 can drop `PREREQUISITE_HELD`, B02 must demonstrate on actual dated periods:

1. two periods and a midperiod consequential change split at the effective event;
2. preserved source clocks and no duplicated period;
3. cold replay with the identical period sequence/readset;
4. a later actual P3 consumer reading the qualified period/material input;
5. an explicit no-change/silence case and a wrong-clock/overlap refusal.

Until then, the current-clock selector, source closure and this ingress hold are the strongest lawful D02 result.
