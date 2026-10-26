# X02 — Neo-V3 interpressure and history-retention requirements differential

**Status:** `PROVISIONAL_REQUIREMENTS__NOT_ISSUED_SCIENCE__NOT_IMPLEMENTATION`.
**Assigned target nodes:** N02 thick relational baselines; N03 challenge/complication/threat/repair; N04 simultaneous recruitment/tension/regulation; N05 durable transition/contradiction; N08 impression/salience/NO_CHANGE.
**Primary old mechanisms:** M03, M05, M08, M10, M21, M23, M24.

This document states what the old pressure-flow family can and cannot supply. It does not issue a new psychological law, coefficient, taxonomy or native grant.

---

## 1. What the old family actually supplies

| Requirement | Old affordance | Actual source grain | Gap |
|---|---|---|---|
| N02 thick, scoped expectations / early care | wound scalars, `buffer_type`, aggregate groove/dominant channel, expectation baseline outside pressure flow | `WoundVector` 7 scalars; `Buffer` strength/cost; `pressure_flow_memory` aggregate | No relationship ID/scope, no care/repair record, no conditional access, no rival expectation, no event-linked memory |
| N03 challenge/complication/threat/repair | structural `baseline_load`, wound mean, generic event types, rupture/metabolization elsewhere | `compute_baseline_load` uses strata + A/V; `_compact_event_context` counts event types only | No actor-specific appraisal of an exact encounter; objective event and subjective impression collapse; no challenge vs threat distinction; no repair operator in this family |
| N04 simultaneous recruitment/tension/regulation | up to five domain loads; one `affect_channel` per domain; one internal route; wound dimensions | `_pick_channel` winner-take-all; `_domain_charge_ledger` one channel/domain | No multi-stream vector, no conflicting channel recruitment, no relation-specific inhibition/amplification, no regulation as activity |
| N05 durable transition/contradiction | route writes to practices/styles/wounds/capacities; frameworks/metabolization/topology elsewhere | scalar/categorical writes; fixed thresholds; no CAN011 transaction | No durable typed operation/relation with causal parents and target-owner admission; no contradiction that changes a mapping; no scope/loss/repair |
| N08 impression/salience/NO_CHANGE | `current_charge`, `trace_intensity`, surface labels, `charge_band`/`overt_aim_band` | derived from structural load + wounds + channel conductance | No event-specific impression/salience; `NO_CHANGE` is not a typed decision; no irrelevant/support-withdrawn/not-received controls; trace can be large without an event |

**Overall:** old pressure flow gives a **transactional scalar accounting substrate**. It does not give the Neo-V3 relational/causal semantics.

---

## 2. Required typed input → operation → output

### 2.1 Event / encounter input

A Neo-V3 event input must keep separate:

```text
OccurrenceInput:
  occurrence_id, occurrence_hash, effective_time, source_owner
  world_event: objective_conditions, participants, action/utterance, material facts
  actor_access: received? channel? as_of? access witness? (not inference from presence)
  other_actor: independent intention/action? (not assumed from outcome)
  relationship_scope: relationship_id / role / history ref
  current_condition: support, material resources, time, health, competing activity
```

The old source has none of these as pressure-flow inputs. `events_this_year` may carry arbitrary dicts, but `_compact_event_context` reduces them to counts by type/label; charge/route never read the content.

### 2.2 Impression / appraisal

A concrete CAN008 R2 coupling rule must produce, at minimum:

```text
Impression:
  occurrence_ref, actor_ref, as_of
  receivability / access
  uptake / appraisal (actor-relative)
  relevance to specific expectation/need/object/practice
  valence / salience / uncertainty / novelty (only if issued)
  supported by: source refs, causal parents, readset, access witness
  valid_empty / NO_CHANGE reason
```

The old `current_charge` is not this object. It is a scalar derived from structural baseline and chronic wound; it has no occurrence_ref, access, expectation, relationship or meaning.

### 2.3 Situated recruitment / interpressure

The old single `affect_channel` must be replaced or wrapped by a typed set of active relations:

```text
ActivePressure:
  source_ref: expectation/need/object/practice/relationship/memory
  target: response/practice/operation/regulation/access
  relation: SUPPORTS | CONFLICTS | BLOCKS | AMPLIFIES | DEFLECTS | REROUTES | TRANSFORMS
  activation_basis: current access + appraisal + support/condition
  strength/priority: only under an issued rule, not a universal scalar
  interaction_refs: other pressures it conditions
  scope: actor/relationship/context/time
  uncertainty/valid_empty
```

This is **not** the same as “one winning channel.” The old code can keep multiple domain loads, but it cannot keep multiple recruited channels/operations for one domain, nor represent their interaction. A new relational operator is required if N04 is to be genuine.

### 2.4 Durable transition

If a lasting change is claimed, the competent CAN011 target owner must issue a rule for:

```text
TransitionCandidate:
  target_kind: V3MS_MEDIATOR | V3MS_TENSION | V3MS_PRACTICE (or exact current owner)
  semantic_object, scope, prestate/hash
  operation: CREATE | TRANSFORM | NO_CHANGE
  readset, causal parents, occurrence refs
  support/access/context bounds
  permitted ADP016 memory / ADP017 belief/access effects
  atomic commit + replay receipt
```

The old route writes to `priority` fields (practice/style/wound/capacity) without a target-owner rule, causal parent, or CAN011 operation. It cannot be promoted to durable change merely because a field changed.

### 2.5 Later consumer

A later same-person event must read the semantic value, not a hash/label/summary:

```text
LaterOccurrence:
  reads target state/relation by exact ref + as_of + permission
  changes a typed option/eligibility/reason/operation
  or explicit NO_CHANGE
```

The old `pressure_flow_memory` is read only for conductance/labels; later pressure flow does not read a prior event's semantic content.

---

## 3. Component-value modification vs changed causal relation

**Old:** route writes values (`practice_stack.organizing += ...`, `wound.anger += ...`, `theory_of_change_style = ...`). A later fixed formula consumes those values. This is value-mediated feedback.

**Required for N04/N05:** a change in the **mapping** from current occurrence/relation to response, e.g.:

- a specific relationship’s support now conditions whether an expectation can recruit a response;
- a repaired relationship changes the access/meaning of a later act without simply adding +x to a scalar;
- a contradiction changes which operation is selected under a context, not just raises a generic “load”;
- a practice becomes available/inhibited for a scope, not just a higher `practice_stack` number.

Without such a changed relation/operator, a scalar increase is not evidence of rewiring. The reviewer found **no such operator** in M03/M05/M08/M10/M21/M23/M24.

---

## 4. Ordinary consolidation vs intense disruption

| Form | Old source | Neo-V3 requirement |
|---|---|---|
| Ordinary repetition / consolidation | trace intensity → groove (0.985 decay, 0.035 increment); small route deltas | Scoped expectation/practice/repertoire stabilization under support and routine; no dramatic event memory required; lawful no-change for non-memorable repetition |
| Intense disruption | `RuptureShard`/`MetabolizationProcess` exist in M18/M19, not pressure flow; `stability_delta` can raise inertia | Distinguish objective severity from actor impression; support/repair can stabilize without resetting event; durable target change only under CAN011; possible chronic/sealed/mis-aim outcomes are not automatic |
| Routine confirmation | small charge/route changes; no explicit confirmation event | Confirmation can maintain a scoped baseline without producing a new trait or a memory narrative |
| Repair | no pressure-flow repair operator; `insulation`/buffers are labels/costs | Repair as activity/relation with timing, source, and scope; it may reduce future susceptibility without deleting the event |

The old `trace_intensity` conflates “amount of effect” with “importance”; N08 requires a differentiated impression/salience and lawful no-change. A large trace is not automatically a meaningful event.

---

## 5. Context-specific recruitment vs competing pressure

- **Context-specific recruitment:** the same person/relation can recruit different operations depending on actual access, current support, competing activity and relationship history. The old code uses global current state and one channel; no event/access.
- **Competing pressure:** multiple pressures may coexist and conflict; the old code keeps multiple domain loads but collapses each domain to one channel; no explicit conflict/regulation relation.
- **Required distinction:** “competing pressure” is not “the highest scalar wins.” A lawful operator must say which pressure is recruited, blocked, amplified, deflected or left inactive, under what source/access/support conditions. The old `max` selector is a convenience, not a rule.
- **Contradictory orientations:** old wound/domain values can coexist as scalars, but there is no representation of two incompatible recruited orientations under one situation. N05 needs a typed contradiction with scope and possible unresolved state.

---

## 6. Legitimate NO_CHANGE

Neo-V3 needs an explicit typed no-change result, not merely zero arithmetic. Legitimate reasons include:

- event not received / no actor access;
- event irrelevant to the current expectation/need/object/practice;
- source withdrawn, inaccessible, or contradicted;
- below a lawfully issued threshold;
- already consolidated; repetition is routine and non-memorable;
- no competent rule issued for this target;
- contradiction unresolved without a lawful resolution;
- support/repair changes conditions but does not create a new durable target.

The old flow has no explicit `NO_CHANGE` object. With zero load it produces zero charge and an empty-ish ledger; with `route_internal_charge=False` it still records history/memory/surface. That is bookkeeping, not a decision. A valid empty/no-change must be represented and auditable.

---

## 7. Proposed falsifiable downstream dependency

**Dependency to test (not issued as a rule):**

> A first admitted event E1 with actual actor access and a concrete expectation/relationship/support condition changes a typed recruited operation or durable target; a later same-person event E2 reads that target and changes a typed option/eligibility/reason; E1 without access, with support withdrawn, or with irrelevant content yields explicit NO_CHANGE; a label/ID-only E1 with identical semantics does not change E2.

**Controls:**

1. Same actor/world/E2, E1 with access vs E1 not received → positive vs no-change.
2. E1 with the relevant relationship/support vs same objective event with support withdrawn → scoped difference or no-change.
3. E1 semantic content changed while label/hash/length changed only → no difference; a real semantic change → difference.
4. E1 with source withdrawn/inaccessible → no durable state.
5. E2 with the prior state vs state hash changed without semantic change → no difference; a real target change → difference.
6. Ordinary repetition vs intense disruption: small confirmation → no new durable target; disruptive event under support → possible target/recovery difference, not automatic.
7. Competing pressure: two pressures with a lawfully issued conflict relation → different recruitment than either alone; without the relation → coexistence/no forced winner.

**Falsified if:** label-only changes move the result; no-access produces a positive impression; support withdrawal does not matter when the rule says it should; a scalar delta is called a changed relation; or the later event cannot distinguish the changed state from a hash-only change.

---

## 8. Disposition by target/source

| Target | Old source affordance | Coverage | Required change | Owner / gate |
|---|---|---|---|---|
| N02 thick baselines | wound scalars, groove, buffer labels | `MISSING` for scoped care/expectation; `PARTIAL_WRONG_MEANING` for susceptibility | add relationship/scope/care/repair/access; no demographic seed | CAN011/ADP015/016/017; scientific issuance |
| N03 challenge/complication/threat/repair | structural load + generic event counts | `MISSING` for appraisal; `INFRASTRUCTURE_ONLY` for event pipeline | event occurrence + access + appraisal + repair | CAN008 R2 concrete rule; ADP019/010 |
| N04 multiple interpressures | five domains × one channel; scalar wounds | `PARTIAL_WRONG_MEANING` | multi-stream recruitment, conflict/regulation, relation scope | CAN008 R2/PFF; exact rule |
| N05 persistent rewiring | route writes; framework/metabolization/topology elsewhere | `PARTIAL_WRONG_MEANING` / `INFRASTRUCTURE_ONLY` | CAN011 typed transition, changed relation, scope, repair/loss | CAN011 target owner; separate rule |
| N08 impression/salience/NO_CHANGE | charge/trace/surface labels | `PARTIAL_WRONG_MEANING` | impression object, salience, explicit no-change, negative controls | CAN008/CAN011 owners |

---

## 9. What to retain from old code

- Stored/derived separation and typed state.
- Transactional working-copy/commit for route application (with the caveat that pre-route writes are not covered).
- Per-domain numeric trace/delta provenance and analyst/surface separation.
- History cap and explicit memory structure as a starting data shape.
- Topology hysteresis and framework acute/chronic/dormant operators as **candidate** mechanisms, not adopted laws.
- `stability_inertia` as a candidate persistence mechanism.
- Failure diagnostics and `PressureFlowError` (with owner review).

## 10. What to rework

- Charge inputs: event/access/appraisal/relationship/support, not only structural load + chronic wound.
- Channel selection: multi-stream recruitment/conflict; no winner-take-all by fixed order.
- Memory: scoped event/relation/practice memory; not only aggregate grooves/conductance.
- Gating: one canonical constraint index; no duplicate hostage; no ratchet without a rule.
- Buffers/insulation/vitality: either make a warranted causal contribution or label as readout; do not claim regulation from a top-3 buffer scalar.
- Audit: include categorical changes and all pre-route writes, or make the transaction truly all-or-nothing.

## 11. What to replace or create

- **Replace:** demographic→wound seeding; fixed channel taxonomy/priority; fixed coefficients/decays; duplicate hostage; `route_unexpressed_load` duplicate; “conservation” claim.
- **Create:** event impression/uptake (CAN008 concrete); multi-stream situated recruitment; relationship/scope/access state; CAN011 durable transition; intervening-time; fallible memory/meaning; explicit NO_CHANGE.

## 12. Authority and HOLDs

- **No native rule, source grant, CAN/ADP/Pyat/C8/C9/C11/C12 permission, or production adoption** is issued here.
- **CAN008 R2** has semantic adoption but no runtime implementation; concrete issuer remains unverified (C9O).
- **CAN011** target update rule remains unissued.
- **ADP015/016/017/019** effect/access rules remain owned elsewhere.
- **Actual current-person integration** is untraced; S50 actual root is held.
- **Archive-wide source identity** is not claimed because the local staging zip hash differs from the TD-R05 archive; selected file bytes are exact.

**Reviewer trigger:** independent I2/I3 source/scientific reviewer after this immutable return. No self-review, no self-adoption.
