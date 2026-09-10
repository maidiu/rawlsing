# M5_RAWLSING_MAPPING_R1

STATUS: `MAPPING_COMPLETE__NO_FROZEN_SYNTHESIS_MUTATION`

SOURCE: Ole Dreier, *Psychotherapy in Everyday Life*.

FROZEN COMPARISON TARGET: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`.

## 1. Mapping principle

Dreier does not justify a `DREIER_OBJECT`, a generic `CONTEXT` object, a `CONDUCT_OF_LIFE_MODULE`, or a new psychology. His contribution is normalized as typed relations among already-separated Rawlsing jurisdictions.

The lawful chain is:

```text
PRE-V3 STRUCTURAL / INSTITUTIONAL / RELATIONAL POSSIBILITY
        ↓
D1 EXACT CONTEXT + POSITION -> TYPED ACTOR-RELATIVE ECOLOGY
        ↓
D2 VALID INTERVALS / RECURRENCES / PARTIAL TRANSITIONS / ORDERED HISTORY
        ↓
TYPE-SPECIFIC REALIZED PARTICIPATION / CONTACT / PRACTICE
        ↓
V3 STANCE / PREMISE / CONCERN / COORDINATION / ACTION / LEARNING
        ↓
EXTERNAL ACTION / COPARTICIPANT OR INSTITUTION RESPONSE
        ↓
D3 ADMITTED SOCIAL-WORLD UPDATE
        ↓
LATER D1/D2 RE-DERIVATION
```

## 2. Dreier concept -> normalized function -> Rawlsing owner

| Dreier source concept | Normalized causal/semantic function | Rawlsing mapping | Disposition |
|---|---|---|---|
| social context of action | local structured practice configuration | existing context/world binding + D1 typed facts | `GENERALIZE/TYPE` |
| location | sociomaterial place/coproximity/access fact | context/location reference where causally relevant | `PRESERVE DISTINCT FROM POSITION` |
| position | structured rights/obligations/scope/counterpart relation | D1 `POSITION_BINDING` | `REUSE` |
| scope of possibilities | actor-relative accessible/blocked/required social possibilities | D1 Stage A ecology qualification | `REUSE` |
| power | concrete authority/access/resource/dependency/sanction/influence asymmetry | D1 typed mechanism families | `DECOMPOSE; NO POWER SCALAR` |
| participation | realized actor activity in context | type-specific realization / OEE when discrete / recurrent activity when persistent | `GENERALIZE` |
| perspective | situated access/view from position | objective access may be D1; subjective interpretation V3 | `SPLIT` |
| premise/reason | subjective basis for action | V3 | `REUSE V3` |
| personal stance | cross-context actor orientation | V3 | `REUSE V3` |
| pursuit | actor-side cross-context directional practice | V3 striving/practice/action | `REUSE V3` |
| personal practice | actor’s situated cross-context participation pattern | D1+D2 inputs, V3 coordination, realized history | `COMPOSE` |
| conduct of everyday life | practical coordination of multiple contexts | D1+D2 + V3 composition | `NO NEW D4` |
| institutional trajectory | structured possible/expected sequence | PRE-V3 route/eligibility + D2 transition rules | `GENERALIZE` |
| personal trajectory | ordered realized cross-context history + actor orientation | history + D2; subjective view V3 | `SPLIT GRAINS` |
| routine/rhythm | recurrent activity/condition pattern | D2 recurrence identity | `GENERALIZE` |
| family conduct | overlapping member practices + arrangements | person/relation facts + D1/D2/D3; no family mind | `COMPOSE` |
| change of practice | realized change in participation/arrangement | V3 action + external realization; D3 if world fact changes | `REUSE` |

## 3. D1 mapping

Dreier directly supports the frozen Stage-A classes and sharpens their context sensitivity.

### D1 outputs strongly supported

```text
RESOURCE_ENTITLEMENT_OR_ACCESS
DEPENDENCY_OR_EXIT_CONSTRAINT
AUTHORITY_OR_CONTROL_APPLICABILITY
OBLIGATION_OR_SANCTION_APPLICABILITY
ACTIVITY_OR_TASK_OPPORTUNITY_REQUIREMENT
INSTITUTIONAL_ELIGIBILITY_OR_GATE_APPLICABILITY
COUNTERPART_REACHABILITY
INFORMATION_CHANNEL_OPPORTUNITY
SUPPORT_OR_OBLIGATION_CHANNEL
TIME_OR_SCHEDULE_CONSTRAINT
```

### M5 additions as semantic constraints, not new output classes

Every derived fact should preserve where applicable:

```text
CONTEXT/PRACTICE REF
POSITION REF
LOCATION REF IF CAUSALLY RELEVANT
COUNTERPART/INSTITUTION REF
VALID INTERVAL OR RECURRENCE REF
```

A single actor may have several simultaneously valid D1 facts from different contexts.

### D1 negative ceilings

```text
CONTEXT != PERSON STATE
LOCATION != POSITION
ROLE LABEL != TYPED SCOPE
POSITION != STANCE
POSITION != ACTION
FORMAL POSSIBILITY != PERSONAL CAPABILITY
POSSIBILITY != PARTICIPATION
```

## 4. D2 mapping

Dreier strongly supports the frozen temporal forms but requires a multi-context implementation.

### Required D2 features

```text
ACTIVE INTERVALS
DIRECTED PERSISTENT RELATIONS
RECURRENCE IDENTITIES
MULTIPLE PERIODS/RHYTHMS
OVERLAPPING CONTEXT BINDINGS
INTERRUPTION / RETURN
PARTIAL TRANSITION UPDATE
BEFORE/AFTER PROVENANCE
ORDERED TYPED HISTORY WITH CONTEXT/POSITION
```

### Transition rebinding refinement

Do not model:

```text
ACTOR_STATE_OLD -> GLOBAL REPLACE -> ACTOR_STATE_NEW
```

unless a case truly warrants total replacement.

Default Dreier-compatible form:

```text
TRANSITION T
-> END/MODIFY selected bindings
-> ADD selected new bindings
-> PRESERVE unaffected ongoing bindings
-> UPDATE typed cross-context dependencies
```

### Trajectory mapping

```text
STORED HISTORY       -> existing ordered typed history
DERIVED TRAJECTORY   -> query/view over history + institutional routes
ACTOR TRAJECTORY VIEW/MEANING -> V3
CAUSAL TRAJECTORY EFFECT -> must resolve to current typed mediator
TURNING POINT        -> derived after sustained redirection
```

No new trajectory carrier is required.

## 5. Type-specific realization mapping

Dreier’s participation theory strengthens the existing frozen distinction:

```text
QUALIFIED != REALIZED
```

Required ladder:

```text
membership/access
-> possible participation
-> actual participation
-> recurrent participation if applicable
-> actor uptake/stance
-> durable change if earned
```

### Discrete forms

Use existing ADP-019 / OBL055–061 / OEE surfaces where competent for contact/event/decision occurrences.

### Persistent/recurrent forms

Do not force:

- dependency relation;
- family obligation;
- recurring school/work/care practice;
- schedule constraint;
- continuing participation relation

into fake discrete events. D2 + practice/history carriers must preserve their temporal form.

## 6. What belongs in V3

Dreier is unusually useful for drawing the seam ceiling.

The following are **not D1 ecology outputs** merely because a position/context makes them likely:

```text
PERSONAL CONCERN
SUBJECTIVE PREMISE
REASON FOR ACTION
STANCE
MEANING
INTERPRETATION
ATTENTION
MOTIVE
PLAN
PRIORITIZATION
CONDUCT-OF-LIFE COORDINATION
RESISTANCE / ACCEPTANCE
PERSONAL PRACTICE AS ACTOR ORGANIZATION
LEARNING
SELF-UNDERSTANDING
DURABLE CAPABILITY CHANGE
MEMORY
BELIEF
```

These belong to existing V3 owners according to exact current authority. M5 does not allocate a new owner among CAN/ADP/TD rules; it preserves V3 jurisdiction.

### Objective activity vs subjective practice

An `ACTIVE_RECURRENT_ACTIVITY` may be emitted/recorded as an objective realized social fact. The actor’s meaning, stance, reason and learned consequences from that activity remain V3.

## 7. Cross-context mapping

The frozen candidate already includes `CROSS_DOMAIN_PROPAGATION`. Dreier gives the required typing discipline.

### Objective propagation

```text
A schedule/resource/obligation/relation change
-> typed actor-relative consequence in B
```

may occur before actor interpretation.

### Actor-mediated propagation

```text
A experience
-> V3 uptake/learning/stance
-> actor action in B
```

must cross V3.

### Forbidden form

```text
CONTEXT A -> SPILLOVER -> CONTEXT B
```

without typed carrier/provenance.

## 8. D3 mapping

Dreier strongly validates the frozen reciprocal-update form.

### Required path

```text
V3-GENERATED ACTION
-> REALIZED EXTERNAL ACTION
-> COPARTICIPANT / FAMILY / ORGANIZATION / INSTITUTION RESPONSE
-> ADMITTED CHANGE IN RULE / POSITION / PERMISSION / RESOURCE / RELATION / TASK DISTRIBUTION
-> NEW SOCIAL FACT WITH PROVENANCE
-> D2 VALIDITY/TRANSITION UPDATE
-> LATER D1 ECOLOGY RE-DERIVATION
```

### Concrete Dreier-compatible update types

- changed household permission;
- changed task/care distribution;
- changed schedule arrangement;
- changed therapy participation arrangement;
- changed school/work/family link;
- changed counterpart relation;
- changed mobility/access arrangement.

### D3 negative ceilings

```text
DESIRE != ACTION
ACTION != SOCIAL RESPONSE
SOCIAL RESPONSE != STRUCTURAL/PRACTICE CHANGE
PERSONAL CHANGE != FAMILY CHANGE
FAMILY JOINT ACTION != COLLECTIVE MIND
```

## 9. Multi-context person representation

M5’s strongest architectural challenge is representational rather than ontological.

Required invariant:

```text
FOR ACTOR A:
  SET OF ACTIVE/QUALIFIED BINDINGS B = {b1...bn}
  WHERE EACH b_i MAY HAVE DISTINCT:
    context
    location
    position
    counterpart set
    resource/obligation/activity facts
    interval/recurrence
    realization status
```

Cross-context edges may connect facts among `b_i`.

Rawlsing must not collapse this to one scalar `SOCIAL_ECOLOGY` or one actor-global context.

## 10. Conduct-of-life mapping

### Is a dedicated cross-context representation required?

`NO MONOLITHIC OWNER REQUIRED`.

A useful implementation may expose a **derived view** over the actor’s active bindings and current V3 commitments/actions for query/planning/debugging, but this view should not itself become an authoritative causal state unless exact semantics are proven.

### Compositional account

```text
D1/D2 publish the structured active possibility/condition field
V3 coordinates action across it
realized actions update history
D3 handles external social update
```

This exactly preserves Dreier’s combination of structured dependence and subject agency.

## 11. D4 court

Potential D4:

`GENERAL_CROSS_CONTEXT_CONDUCT_MECHANISM`

**Ruling:** `REJECT_AS_NEW_SEAM_CAPABILITY`.

Reason:

- upstream component duplicates D1/D2;
- subjective coordination would seize V3;
- external update duplicates D3;
- an untyped middle operator would recreate the black-box seam the campaign is trying to eliminate.

What is required instead is a composability law/test suite.

## 12. Proposed post-review conformance tests

These are recommendations to Vozhd, not mutations of frozen synthesis.

### CTX-01

Two actors co-present in one location but different positions derive different D1 ecology facts.

### CTX-02

One actor holds at least three overlapping context-position bindings with distinct obligations and schedules.

### CTX-03

A weekly recurring activity is preserved as one recurrence identity, not unrelated events.

### CTX-04

A school/job/therapy transition updates only affected bindings; unrelated context bindings persist.

### CTX-05

A context-A schedule change produces a context-B time/obligation update with explicit provenance.

### CTX-06

A context-A experience does **not** change context-B action until V3 uptake/action occurs.

### CTX-07

Actor action does not alter external context unless counterpart/institutional response admits a new fact.

### CTX-08

Formal membership/presence does not imply actual participation.

### CTX-09

Stable repeated behavior under stable arrangements is not minted as a trait without V3 durability/generalization evidence.

### CTX-10

Trajectory query can be reconstructed from ordered context-bearing history; causal use resolves to a current typed mediator.

## 13. Reuse / generalize / missing / reject summary

### REUSE

- exact position binding;
- typed D1 ecology outputs;
- world/context/time binding;
- OEE for discrete realization;
- V3 uptake/action/learning/history;
- D3 gated reciprocal update.

### GENERALIZE / SHARPEN

- context/location/position typing;
- simultaneous actor bindings;
- recurrence identities and overlapping rhythms;
- partial transition rebinding;
- typed cross-domain propagation;
- context-bearing trajectory history.

### MISSING

No new positive D4 mechanism is proved.

The smallest missing **implementation-level guarantee**, if not already present, is:

`CONCURRENT_MULTI_CONTEXT_BINDING_AND_CROSS_CONTEXT_EDGE_COMPOSABILITY`.

This is a conformance requirement on D1+D2+V3 composition, not a new semantic owner.

### REJECT

```text
CONTEXT black box
POWER scalar
SPILLOVER operator
TRAJECTORY causal black box
ONE_ACTOR_ONE_CONTEXT
family collective mind
conduct-of-life seam module
role/category -> stance/action
```

## 14. Mapping terminal

`M5_MAPPING_COMPLETE__DREIER_SHARPENS_D1_D2_AND_SUPPORTS_D3__V3_RETAINS_PERSONAL_CONDUCT_STANCE_AND_ACTION__NO_D4__SMALLEST_CONSEQUENCE_IS_MULTI_CONTEXT_COMPOSABILITY_PLUS_LOCATION_POSITION_FIREWALL`