# M02 — material capacity: X05 direct-source dossier

**Court:** X05 historical source / material-actor-world bridge. **Evidence grade:** `HISTORICAL_SOURCE_AUDITED` (local read-only source; sourcefree probes); `CURRENT_INTEGRATION: UNTRACED`; `THEORY: PROPOSED_NOT_ISSUED`; `AUTHORITY: NO_NATIVE_GRANT`.  
**Direct source:** `v3/core/state.py` `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`; `v3/systems/capacity.py` `cae31ffd4006601aa860fbb011d1a23697a07a8cc1f0dc8e2897d5f2ed1531c3`; `v3/systems/health_drift.py` `ba4608b7b9ab5dc758085ea90ed6eef64b4e40cc20790508e6623e51dc13995b`; `v3/io/identity_to_backbone.py` `cb29c9595ac495c3b69b693d4c58a278e9ef1f63a7a8917d8e407920fbd3bdda`.  
**Surface:** S2 local Mac; no production edit; no current C9/C12 execution.

## 1. Exact as-built map

| Element | Source | Inputs / state reads | Operation | State writes / outputs | Callers / first consumers |
|---|---|---|---|---|---|
| `Capacity` | `v3/core/state.py:17-32` | eight scalar fields: `time, money, health, social_support, skill, mobility, risk_tolerance, legitimacy` | dataclass, clamp 0–100 | stored `state.capacity` | `backbone_state_from_identity`; all yearly steps; `state_to_dict` |
| `update_capacity` | `v3/systems/capacity.py:10-60` | `state.events_this_year[].capacity_deltas`; `v3config.delta_caps.capacity_fields` (default 20) | sum each field's event deltas, cap summed per-field delta to `±cap`, add, clamp | `state.capacity.*` | `run_one_year` at `capacity_update` (`v3/engine/yearly_step.py:132`); `_compute_derived_after_step` then recomputes AC |
| `update_health_drift` | `v3/systems/health_drift.py:15-96` | `derived.stability_threshold`, `derived.insulation_score`, `capacity.social_support`, `capacity.health`, wound vector, `reproduction_constraints.job_insecurity`, active magnets, practice stack | formula drift: `down = stability/100*0.8`; `up = (insulation/100*0.5)+(support/100*0.4)` if stability<70; delta capped ±1.5; wound decay; impunity/intensity/craft/opportunity drift | `capacity.health`, `wound_vector`, `peak_routing.impunity_access`, `intensity_and_capture.*`, `practice_stack.*` | `run_one_year` at `health_drift_update` (`yearly_step.py:133`) |
| Initial material facts | `v3/io/identity_to_backbone.py:13-43,247-280` | identity `current_class`, `class_origin`, `urbanicity`, `minority_status` | class constants: money/underclass 18 … elite 88; job insecurity 75 … 5; debt 70 … 8; urban mobility rural 35 … megacity 78; minority legitimacy dominant 58 / minoritized 38 | `state.capacity` and `initial_state_provenance` | server generation (`server/generation/simulation.py`), v2→v3 connector |
| Material visibility to LLM | `v3/engine/llm_contract.py:659-676` | derived `hostage_index`, psychological capacity | summary exposes **only** `field.hostage_index` plus psychological capacity; material `money/time/health/support/skill/mobility/legitimacy` are not in the Pass-1 summary | LLM candidate plausibility | event proposal only; not a state write |

**Defaults and hidden laws.** `Capacity` defaults every material field to `50.0` (`state.py:20-27`). `time`, `health`, `social_support`, `skill`, `risk_tolerance` are seeded as hardcoded `50.0`; only `money`, `mobility`, `legitimacy` are class/urbanicity/minority lookups (`identity_to_backbone.py:247-280`). There is no hourly work schedule, no caregiving calendar, no household roster, no travel time, no realised care transaction, and no distinction between a person's own constraints and the constraints of a co-caregiver. `capacity.time` is a 0–100 scalar, not available hours. `capacity.social_support` is a scalar, not actual care received or caregiver conduct. `capacity.health` is a scalar, not diagnosed condition or functional limitation.

The mechanical event sampler can emit a `capacity_deltas` event (`v3/engine/event_engine.py:31-124`): for example, one event flavour subtracts `money` and moves `time`; this is a deterministic pseudo-random arithmetic event, not a labour-market or care schedule. LLM Pass 1 can also propose capacity-delta events; those are admitted only through code-side delta templates and caps (`v3/engine/effects/delta_templates.py:17-158,254-365`).

## 2. What this actually models, and what it does not

The code models **bounded material capacity state** at yearly grain. It does not model:

- actual hours of work, commuting, school, sleep, care, or rest;
- the difference between objective availability and a child's experienced care;
- a parent's love/intention versus practical availability;
- co-care substitution (another caregiver supplying missing care);
- coercive parenting while material provision is high;
- whether low money or low time changes a child's feasible encounter with a specific caregiver.

The old code can move `capacity.time` and `capacity.money`, and can feed derived `hostage_index` and `agency_capacity_AC`, but it cannot represent *who was actually present*, what they did, or how the child received it. It is therefore a material **carrier**, not a social-reproduction or actor-world operation.

## 3. Coverage and disposition

| Target | Coverage | Reason |
|---|---|---|
| N01 needs/motives/objects | `INFRASTRUCTURE_ONLY` | capacity is not a need, object, desire or motive; it can only be a precondition |
| N06 activity/time/stages/social reproduction | `PARTIAL_WRONG_MEANING` | annual scalar capacity and caps exist; no actual activity/time-use, care schedule, co-care, or stage-attainable participation |
| N07 independent others/power/love | `INFRASTRUCTURE_ONLY` | no other actor; capacity belongs to one actor only |
| N12 actual C12 person | `UNKNOWN` | no current C9/C12 consumer proved; readiness/consumer is separate |

**Disposition: ADAPT.** Keep the typed objective capacity carrier and the annual cap/clamp discipline. Replace missing-as-50 and class-only seeding with explicit unknown/source-qualified facts. Add a world/actor operation that resolves actual work, care, travel, school, rest and co-care intervals and exposes **feasible means** to encounters. Do not let `capacity` alone stand in for experienced care or parental love.

## 4. Harmful defaults / defects to remove

1. **Missing = midpoint.** `time/health/social_support/skill/risk_tolerance = 50` are hardcoded and recorded as `hardcoded_default` (`identity_to_backbone.py:247-280`). Unknown must not become a neutral truth.
2. **Class constants as income/debt/job insecurity.** `_CLASS_MONEY`, `_CLASS_JOB_INSECURITY`, `_CLASS_DEBT` are policy constants with no labour-market source or household composition.
3. **`time` is not a schedule.** No hours, no work shifts, no care blocks; `health` is not functional capacity; `social_support` is not care.
4. **Material state is nearly invisible to Pass 1.** The LLM sees `hostage_index` and psychological capacity, but not actual money/time/health; event proposals cannot reason from the material situation in the summary.
5. **Magnet lexical side effects in health drift.** `health_drift.py:98-162` converts magnet label keywords (`art`, `music`, `community`, `famil`) into practice increments, and magnet count into `intensity`. This is a lexical hidden law, not actual participation (also M20).
6. **No first consumer beyond derived/persona.** No C9/C12 semantic consumer is proved.

## 5. Proposed typed seam (nonissuing)

```text
ObjectiveMaterialInterval {
  actor_id; clock_start/end; source_ref;
  work_hours; care_hours; travel_hours; school_hours; rest_hours;
  money_available; housing_status; health_function; legal_status;
  co_care_refs[]; dependents[]; unknown_fields[];
  provenance; rule_version;
}
```
`ObjectiveMaterialInterval` is produced/owned by the world/SDTF/ADP019 source, not inferred from a demographic class. It feeds only:
1. `FeasibleActivitySet` (what the actor can actually do in the interval);
2. `CareAvailability` (who can provide care, when, under what cost);
3. `CapacityEvidence` (an evidence record, not a 50 default).

The first legitimate C9/C12 consumer must read a source-qualified material interval or feasible-activity record; it must not read a scalar `time=50` as truth. **Owner:** world/SDTF/ADP019 for objective facts; CAN008/CAN011 for actor uptake; current C9/C12 implementer for consumption. **Not issued by X05.**

## 6. Counterexample and hostile alternative

**Discriminating case (loving but work-constrained caregiver).** Hold parent warmth high, material provision low, and add a grandmother who provides daily care. The old code can set `capacity.money` low and `capacity.time` low, but it has no `co_care_refs` and no actual care schedule; the child model and parent baseline are computed from parent behaviour/defaults, not from the grandmother's realised care. The old machine cannot produce “warm parent + insufficient parental time + adequate co-care” as one lived arrangement.

**Hostile alternative.** Observed child differences may be caused by the LLM's narrative selection or by parent warmth, not by the capacity arithmetic. A test that changes only `capacity.money/time` and observes a changed scene does **not** prove material causation. The required discriminator holds the narrative/event stream fixed and varies only a source-qualified work/care interval, then checks a semantic actor consumer.

**Falsifier.** If two actors with identical source-qualified work/care/co-care intervals but different `capacity.time` scalars produce different C9 semantics, `time` is not the material fact being consumed. Conversely, if changing the actual interval changes nothing while changing a scalar does, the old code is using a policy constant, not the world.

## 7. Tests and limits

- Sourcefree probe (X05): event capacity `-100` from 50 moved `money` to 30, not 0, because the per-field annual cap is 20 (`capacity.py:24-50`). This confirms cap arithmetic, not human feasibility.
- Historical test entry: `v3/tests/test_step_logic.py:65-75` (`test_capacity_update_applies_event_deltas`). It tests arithmetic only.
- **NOT_RUN:** full old suite; `health_drift` full-year behaviour; any current C9/C12 consumer; any native person.
- **No native rule, coefficient, or source permission is issued.**

**Required future reviewer:** independent V3 source/consumer reviewer for M02/N06; world/SDTF/ADP019 owner for material facts; current C9/C12 implementer for first semantic read. X05 does not self-adopt.
