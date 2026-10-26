# Existing V3/PFF machine — recover, reuse, adapt, or escalate

**Question:** Does RA-D's “first missing composer” / “needs competent formation rule” conclusion overstate the new software/science required, given the recovered V3/PFF machine and current CAN008/CAN011 owners?

**Answer:** It overstates the *software absence* if read as a blank sheet, but not the *scientific absence*. The recovered machine has a real transactional pressure-flow composer, a real annual developmental scheduler and a real structured LLM contract. It executes historically on a fixture. What is missing for the current person is (a) an event-scoped binding/carry-forward adapter, (b) current-owner mapping and actual actor state, and (c) the concrete CAN008/CAN011 rule/issuance. That is targeted adaptation plus authority, not a new psyche.

**V3 source verification:** historical bundle `Rawlsing_code_bundle_staging`; archive identity `953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086`; 31/31 selected source identities exact; fixture `identity_minimal.json` SHA-256 `ef7008ac0d83e7690bd89e96ec683d25d3b784806857a799da2978ba7aa35673`. Reviewer reproduction: `logs/reviewer_v3_functions.json`, `logs/s50_entrypoint.json`.

## 1. Existing callable machinery

Line references are in the recovered source root. Hashes are in `SOURCE_INDEX.json`.

| Function / object | Exact source | What it actually does | Executed historically? | Current disposition |
|---|---|---|---|---|
| `BackboneState` | `v3/core/state.py:501` | Persistent typed actor state: capacity, psychological capacity, domains, practices, frameworks, cracks, expectation baseline, striving objects, pressure-flow history/memory, surface/analyst accounts, provenance. | Yes, constructed on the fixture and roundtripped exactly. | **REUSE as computational reservoir.** Not the current S52 actor and not native authority. |
| `compute_all_derived` | `v3/core/derived.py:322` | Recomputes derived indices from the current state. | Yes, in the S50 fixture run. | **REUSE** under owner mapping; legacy formulas not law. |
| `run_pressure_flow_cycle` | `v3/psyche/flow.py:753` | Post-year membrane: channel assignment, baseline load, expression gating, charge ledger, vitality profile, transactional route simulation, snapshot/history, memory update, surface and analyst accounts, commit. | Yes, one cycle on the fixture; history 0→1, memory grooves for five domains, surface/analyst for five domains. | **REUSE the transaction/audit composer; ADAPT invocation grain from annual to event/interval.** |
| `_derive_current_charge` | `v3/psyche/flow.py:268` | `baseline_load × inner_load_factor × wound_factor` per domain. | Exercised inside the pressure-flow cycle. | **REUSE mechanism; legacy coefficients/policy not adopted.** |
| `_channel_conductance` | `v3/psyche/flow.py:366` | Base 1.0 plus prior groove, vitality/agency/aperture/social support/network/repression/relational-field terms; clamped 0.65–1.45. | Exercised inside the cycle. | **REUSE as an explicit legacy conductor; do not promote numeric policy.** |
| `_domain_charge_ledger` | `v3/psyche/flow.py:406` | Builds per-domain charge, overt/internal routing, conductance, trace intensity, vessel and insulation hints. | Exercised inside the cycle. | **REUSE; needs event-conditioned inputs, not only baseline/wound.** |
| `_apply_single_domain_route` | `v3/psyche/flow.py:500` | Applies channel-specific trace to practices, style, peak routing, capacities, wounds; clamps. | Exercised inside the transaction. | **REUSE mechanism; per-channel deltas are legacy policy requiring owner review.** |
| `_simulate_domain_routes_transactionally` | `v3/psyche/flow.py:547` | Deep-copies state, applies routes, returns per-domain and aggregate deltas without mutating the original. | Exercised inside the cycle. | **REUSE as the transactional application seam.** |
| `_commit_route_state` | `v3/psyche/flow.py:570` | Commits only the listed mutable objects after successful construction. | Exercised at the cycle commit point. | **REUSE transaction discipline; map targets to CAN011 owner before durable use.** |
| `_update_memory` | `v3/psyche/flow.py:678` | Builds recent/lifetime charge and channel summaries, historical relation, grooves; decays grooves by 0.985 and increments by 0.035 × trace. | Exercised inside the cycle. | **REUSE history→future-conductance loop; coefficients are legacy policy and the result is trace memory, not autobiographical memory.** |
| `update_loop_topology` | `v3/systems/topology.py:50` | Hysteresis over `reciprocal`/`extractive`/`self_contained`; default required consecutive years 2. | Called by the yearly step; no transition observed in the one-year fixture. | **REUSE hysteresis mechanism; three labels/conditions are legacy state machine, not whole-psyche proof.** |
| `run_one_year` | `v3/engine/yearly_step.py:12` | Executes configured steps in order, recomputes scheduled derived indices, increments year/age, runs post-year pressure flow. | Yes, one year on the fixture; year 2000→2001, age 30→31, roundtrip exact. | **ADAPT to event/interval scope; annual cadence is not the settled batch loop.** |
| `state_summary_from_backbone` | `v3/engine/llm_contract.py:518` | Builds structured Pass-1 state summary: identity, field, capacity, wound, frameworks, cracks, practices, domains. | Available; not invoked in the S52 chain. | **REUSE for compact event-specification input; remove fabricated/placeholder defaults.** |
| `build_render_packet` | `v3/engine/llm_contract.py:791` | Builds Pass-2 render packet from selected events/magnets, applied deltas, identity and surface psyche. | Available; not invoked in the S52 chain. | **REUSE render separation; adapt to retrospective half-call at batch boundary.** |
| `run_llm_band_year` | `v3/engine/run_llm_band.py:146` | Pass 1 proposal → selection → apply deltas (lines 268–269) → re-derive → Pass 2 render (line 380). | Historical code; not run by RA-D because it requires an LLM. | **ADAPT timing:** the current implementation applies deltas before render in the same call; the user-settled cycle needs sequential Rawlsing realization and retrospective narration. |

## 2. What is actually executable now

Reviewer one-year independent run:

- Before: pressure-flow history length 0; no memory grooves; no surface/analyst domains.
- After: history length 1; memory grooves for `body_self`, `empire_occupation`, `family_household`, `nation_state`, `sect_class_ethnicity`; surface and analyst domains for the same five; `loop_topology=self_contained`; topology hysteresis counters all zero; state roundtrip exact.
- S50 entrypoint: two-year fixture projection, year 2002, age 32, pressure-flow history and memory present, cold reopen same projection hash, source 31/31 exact.
- The fixture expectation baseline is all `hopeful` and has `striving_count=0`. These are legacy fixture/initialization facts, not current-person facts.

This establishes **historical executable continuity**, not a current integrated person.

## 3. What is unwired or missing

| Layer | Exact status |
|---|---|
| Current person V3 state | S50 actual root returns `SOURCE_OWNER_HOLD`; missing `backbone_state`, `initial_state_provenance`, `expectation_baseline`, `striving_objects`, `pressure_flow_history`, `pressure_flow_memory`, `surface_psyche_profile`, `analyst_pressure_account`, `actor_context_projection`, `actor_owned_source`. |
| S52 actor → V3 | The S52 chain imports S39/S49/S51 only. Its actor state has no `BackboneState`; no V3 pressure-flow call occurs. |
| Event → V3 impression | `run_pressure_flow_cycle` consumes `_compact_event_context`, which only counts `events_this_year`/`micro_trace_this_year` by type. It does not read event identity, access, admitted semantic content or another actor's meaning. |
| V3 → current owner | The recovered `Framework`, `Buffer`, `WoundVector`, `Crack` and `PracticeStack` map conceptually to CAN011 `V3MS_MEDIATOR`/`V3MS_TENSION`/`V3MS_PRACTICE`, but no current-owner target rule or adapter commits them. |
| Current response composer | S44/S45 reach a **test-only** M35 CAN008/CAN011 receiving/commit port; its C9 target is `NO_CHANGE/NO_PROPOSAL`. It is not a current native rule or a durable target transition. |
| Sequential batch | No 3–5-event scheduler, per-event carry-forward, interconnected impression propagation, intervening-time computation or retrospective first-half/second-half implementation exists in the S39–S52 closure. S48 is one-event transport; S52 is one experiment. |
| Memory/meaning | `_update_memory` is aggregate trace/groove memory, not fallible autobiographical or impression-dependent memory. ADP016/ADP017 semantic owners are not integrated into the S52 chain. |

## 4. Current CAN008/CAN011 owner boundary

- **CAN008 R2 semantic adoption exists.** Adopted semantic blob `b80dd6925066510ecbbfec7b427bf9f688475663`; HQ adoption record blob `a6bc1555489271e1adb2271ed02d46bb7f888170`. It constitutes receivability, uptake/appraisal, situated recruitment and multi-stream immediate response, with noncollapse laws. It explicitly has **NO_RUNTIME_IMPLEMENTATION**.
- **Concrete CAN008 rule issuer remains unverified.** C9O (`SOROK-20261019-C9O-ACTOR-RULE-OWNER-SCIENCE-DECISION-R1/01_COMPETENT_OWNER_AND_GRANT_GRAPH.md`) records `CAN008_RULE_ISSUER_UNVERIFIED` and says the adopted semantic shell is not an executable coupling/choice rule.
- **CAN011 target update rule remains unissued.** CAN011 authority blob `1ed04e62a363493bc7032a99139454a3126e6ea0` provides `V3MS_MEDIATOR`, `V3MS_TENSION`, `V3MS_PRACTICE` and requires an exact separate target rule/grant for CREATE/NO_CHANGE. C9O records `CAN011_TARGET_UPDATE_RULE_UNISSUED`.
- **No actor/event admission or later-action consumer is bound.** ADP007/ADP019/source-as-of and a native action-selection/execution entrypoint remain unproved. A test performer label is not an enacted act.

Therefore the scientific blocker is concrete-rule issuance, not absence of a semantic owner. The software blocker is current binding/adaptation, not absence of every V3 function.

## 5. Already executable vs targeted adaptation vs unissued science

**Already executable as historical implementation**

- `BackboneState` construction, typed JSON roundtrip.
- `compute_all_derived`.
- `run_pressure_flow_cycle` with charge ledger, transactional routes, history/memory, surface/analyst split.
- `update_loop_topology`, `run_one_year`.
- `state_summary_from_backbone`, `build_render_packet`.
- S50 fixture projection and cold reopen.

**Requires targeted adaptation to the current person/event/sequential system**

1. Bind an admitted event and actor-local access witness to event-scoped inputs for the existing charge/route computation. The event context currently carries only type counts.
2. Map the recovered mutable targets to current CAN011 owners; do not write legacy `Framework`/`Buffer`/`WoundVector`/`Crack`/`PracticeStack` objects as durable person state by default.
3. Replace the annual scheduler with a per-event realization loop that carries the post-event state and intervening-time computation into the next event.
4. Move the LLM contract from “Pass 1 → apply deltas → Pass 2 render” to the settled “retrospective half of N + sequential 3–5 events/time + prospective half of N+1” boundary.
5. Keep objective causal history and actor memory/interpretation distinct; aggregate trace memory is not autobiographical memory.
6. Preserve the transactional/read-only audit pattern; no LLM-authored arbitrary deltas.

**Requires genuinely unissued scientific rules (HOLD)**

1. Concrete CAN008 person×event coupling: what precipitating occurrence/access, conditioning state and current evidence count; what uptake/appraisal and recruitment is computed; what is valid-empty.
2. Concrete CAN011 target transition: exact semantic object, prestate, readset/causal parents, CREATE/TRANSFORM/NO_CHANGE, target scope and commit/replay.
3. Impression-dependent memory formation, fallible retrospective meaning and intervening-time change.
4. ADP015/016/017/019 effect and access rules where a lasting relationship, memory, belief or event consequence is claimed.
5. Any stochastic/mood/event-frequency policy not already issued. The A/B binary is withdrawn; no new coefficients may be invented.

**Legacy policies not to adopt by recovery alone**

- Demographic→wound/framework/parent-type seeding.
- All-hopeful 50 parent/expectation defaults.
- Blind `run_n_years` on an actual person.
- Years-as-learning multiplier.
- Fixed channel winner / maximum-channel selection as universal psychology.
- Legacy charge/conductance/groove coefficients as native laws.
- Pass-1 fallback event fabrication and first-candidate fallback.
- Two-pass LLM timing as the developmental cycle.
- Fixture-only V3 state as a second psyche or current-person truth.

## 6. Single highest-value next executable implementation operation

**Name:** `EVENT_SCOPED_V3_PRESSURE_FLOW_CARRY_FORWARD_R1`

**What to build (targeted adaptation, not new science):** a bounded adapter that takes one exact admitted event plus actor-local access witness, a current `BackboneState` (or owner-issued equivalent), and the current material/relational state; supplies an explicit, pre-registered event-conditioning mapping into the existing charge/route inputs; calls the existing `run_pressure_flow_cycle`-family computation; and emits a typed, read-only per-event projection containing before/after state, per-domain charge/trace, history/memory delta, surface/analyst separation, causal parents and an explicit `NO_CHANGE` where the mapping is not lawful. Then run one later event through the same adapter to show that the post-event state is read.

**What it must not do:** no durable CAN011 write, no invented coefficients, no new psyche store, no LLM call between the events, no claim of native/actor-owned psychology, no promotion of legacy numbers, no use of the S52 controlled performer as an independent counterpart.

**Why this is the highest-value next operation:** it reuses the existing V3 pressure-flow composer and exposes the actual event input/output contract that the sequential batch needs. It is smaller than a batch engine and larger than another fixture. It produces either a genuine event-scoped carry-forward seam or a precise, falsifiable statement of the missing rule/input. It does not require the unissued CAN011 durable target rule because its output is read-only.

**What to falsify at this sourcefree stage:**

1. Same event identity/access but different event semantics/conditions must change the computed projection, or produce a typed `NO_CHANGE`; a hash/label-only change must not.
2. No access or non-receipt must not produce a positive actor impression.
3. The later event must read the changed projection and change a typed response/option/eligibility/reason, or explicitly `NO_CHANGE`.
4. The adapter must not require arbitrary new coefficients, an LLM-authored delta, a fabricated event, or a test-only counterpart flag to produce its result.
5. If the adapter cannot distinguish these cases, the output is not evidence of event-conditioned psychology; it is evidence that the concrete CAN008/CAN011 rule or event mapping is still unissued.

If the adapter passes those tests, the next gate is the competent CAN008/CAN011 rule issuance and durable-target admission. If it fails, the exact missing input/rule is the deliverable — not a fabricated green path.

## 7. Boundary judgment

- **V3 machine exists and executes historically:** yes.
- **V3 machine already computes the current person's event-conditioned psychological organization:** no.
- **A pressure-flow composer exists:** yes.
- **A current event-scoped composer/admission exists:** no.
- **Concrete CAN008/CAN011 rules are issued:** no.
- **A blank-sheet psyche/specification is required:** no.
- **Targeted adaptation is required:** yes.
- **Native/actor authority is granted by this review:** no.
