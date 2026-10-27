# M14 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `PeakRouting` | `v3/core/state.py:257–272` | loop_topology, solidarity_boundary, harm, rage, theory, coherence, impunity, appetite, hysteresis counters | heterogeneous stored routing bundle | `peak_routing` | JSON; topology/boundary/coherence; persona | no value test |
| `update_loop_topology` | `v3/systems/topology.py:14–99` | state infrastructure/practice/boundary/capacity + derived mis_aim/hostage | evaluates fixed transition requirements; increments consecutive-year counters; switches after 2 years | `loop_topology; topology_hysteresis_years` | yearly_step topology_and_boundary_update | no focused test |
| `update_solidarity_boundary` | `v3/systems/boundary.py:20–80` | events not/repression/hostage + config order/max_step/reversal | last event target; at most one step/year; reversal only if repression>=70, hostage>=70, or shock_override | `solidarity_boundary` | yearly_step topology_and_boundary_update | no focused test |
| `update_coherence` | `v3/systems/coherence.py:18–35` | events coherence_delta | sums deltas, cap 10, clamps | `peak_routing.coherence` | yearly_step topology_and_boundary_update | no focused test |
| `event hints` | `v3/engine/event_engine.py:97–100` | mechanical seed | writes event loop_topology/solidarity_boundary hints | `events_this_year` | boundary consumes latter; topology ignores former | no test |
| `derived peak consumers` | `v3/core/derived.py:135–161` | loop, boundary, coherence, theory | peak regime/Che-Jesus eligibility | `derived` | Pass 1/persona | smoke only |

## What is actually run

- Hysteresis is genuinely implemented for topology: a transition rule must be satisfied for `required_consecutive_years` (2) consecutive calls; counters persist in `peak_routing.topology_hysteresis_years`; a successful transition resets all counters. Probe: network_density=60 and organizing=60 from self_contained gave counter 1 on call 1 and reciprocal on call 2.
- Boundary movement is bounded: `max_step_per_year` is one; an event-requested target is consumed (last event wins) with no actor-access/validity check; downward movement is blocked unless repression>=70, hostage>=70, or a `shock_override` event. Probe: universal -> none stayed universal without a gate; with repression=75 it moved one step to expanding.
- Topology inputs are scalar aggregations: network density, organizing, boundary, money, social support, mis_aim risk, impunity, craft/study, hostage. There are no relation-edge creation, activation/inhibition, cross-link, or scope records. `theory_of_change_style`, `harm_constraint`, `rage_metabolization`, and `appetite_profile` are not maintained by these steps; the event `loop_topology` hint is ignored by `update_loop_topology`.
- The boundary is a five-value global enum. A model-generated event can request a boundary, but the only gate is a config scalar/shock; no evidence that the actor received, interpreted, or could enact the relation is required.
- `PeakRouting` remains a heterogeneous bundle: political-strategy labels, boundary, coherence, impunity, appetite, and hysteresis counters. It is not a representation of dynamically reorganizing interdependent motivations.
- There are no focused topology/boundary/coherence tests. `test_architecture_invariants` checks that the step ID appears in order; it does not execute a transition, reversal, or ping-pong case.

## Real affordance

- Two-year topology hysteresis and one-step boundary movement/reversal gates are real and probe-visible.
- Counter persistence and reset on transition exist.
- Coherence receives bounded event deltas and feeds derived peak eligibility.
- These are genuine techniques worth retaining.

## Source-level REDs

- Global enum cannot represent plural, scoped, condition-dependent configurations.
- Scalar thresholds do not establish an actual relation or a learned causal link.
- Event labels can request boundary movement without actor access/reception.
- Hysteresis is a fixed software regime switch, not a new relation edge.
- `PeakRouting` mixes incompatible semantics and lacks relation-level history.
- No tests cover the claimed behavior.

## Tests actually covering this mechanism

- No focused topology/boundary/coherence behavior test.
- `test_architecture_invariants::test_step_order_immutable` only checks step-ID ordering.
- `test_step_logic::test_event_sampling_produces_events_in_full_run` only checks no crash and year advance.

## Probe evidence

Probe evidence: two-call topology transition; boundary blocked at universal without gate and one-step after repression=75; domains unaffected by frameworks/practice; no focused source test.

## Identity and authority note

TD-R05/card already say prior result understated continuity and the bundle is too heterogeneous. `PLAN_ALIGNMENT` declares hysteresis done, but no test exercises it.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
