# TEMPORAL_CAUSAL_FORMS_COURT_R1

STATUS: `PHASE_2_TEMPORAL_COURT_COMPLETE_R1`

## Court question

Must Rawlsing create distinct new ontology carriers for EVENT, CONDITION, RELATION, RECURRENT ACTIVITY/PRACTICE, TRANSITION, TRAJECTORY, TURNING POINT and CUMULATIVE PROCESS?

## Verdict table

| FORM | EXAMPLE | EXISTING COVERAGE | R1 VERDICT | REQUIRED LAW |
|---|---|---|---|---|
| `EVENT` | firing, callback, sanction, discrete encounter | OEE/ADP-019/OBL055–061 strongest existing coverage | `REUSE_EXACT_EXISTING_OWNER` | occurrence provenance + actor/world/time/context + downstream response separation |
| `CONDITION` | years of low control, economic strain, eligibility, insecurity | structural pressure/context and V3 state/history fragments | `GENERALIZE_EXISTING_OWNER` | interval identity, start/end/applicability, actor-relative status; condition != repeated event token |
| `RELATION` | worker↔supervisor, caregiver↔dependent, support tie | PRE-V3 topology and V3 relationship/history bookends | `GENERALIZE_EXISTING_OWNER` | typed counterpart identities, direction/power/obligation, persistence and realized relation status |
| `RECURRENT_ACTIVITY/PRACTICE` | complex autonomous work 40h/week, care, study, brokerage | CAN-011 practice/history plus repeated events can approximate | `GENERALIZE_EXISTING_OWNER` | stable recurrence identity + content/quality/intensity/duration/counterparts; do not require conscious appraisal each iteration |
| `TRANSITION` | entering parenthood, promotion, job loss/entry | state/phase changes and events can represent boundary crossing | `GENERALIZE_EXISTING_OWNER` | before/after binding + realized gate + post-transition ecology rebinding |
| `TRAJECTORY` | occupational advancement, changing care/work path | V3 history/path/attractor trajectory semantics | `REUSE_AND_GENERALIZE` | ordered typed state/relation/activity history; trajectory is not trait |
| `TURNING POINT` | transition followed by sustained redirection | no dispositive standalone owner | `NOT_REQUIRED / REJECT_STANDALONE_CARRIER` | derived predicate earned only after sustained trajectory reorganization; event magnitude alone insufficient |
| `CUMULATIVE PROCESS` | years of insecurity, successive gate penalties, accumulating practice | memory/history/path carriers exist | `GENERALIZE + NEW_UPDATE_SEMANTICS_REQUIRED` | typed iterative feedback/update steps; no generic cumulative scalar |

## 1. Governing compositional law

The court rejects eight unrelated storage types. It instead requires a small temporal grammar:

```text
OCCURRENCE(event)
ACTIVE_INTERVAL(condition/relation)
RECURRENCE(activity/practice)
REBIND(transition)
ORDERED_HISTORY(trajectory)
DERIVED_REDIRECTION(turning_point)
ITERATE(update_rule, prior_history)(cumulative_process)
```

These are semantic obligations, not necessarily seven new implementation classes.

## 2. Event firewall

The following are prohibited compressions:

```text
JOB_LOSS_EVENT == ECONOMIC_STRAIN_CONDITION        [FALSE]
SHARED_SETTING_EVENT == SOCIAL_RELATION            [FALSE]
REPEATED_EVENT_TOKENS == RECURRENT_ACTIVITY        [NOT GENERALLY]
TRANSITION == TURNING_POINT                        [FALSE]
EVENT == ACTOR_UPTAKE                              [FALSE]
EVENT == DURABLE_CHANGE                            [FALSE]
```

Pearlin-type event→strain evidence specifically requires propagation from a discrete occurrence to a later persistent condition. Kohn/Schooler and Sève-type activity mechanisms require recurrent task/action structure even when no dramatic event occurs.

## 3. Condition and relation law

An active condition/relation must be capable of existing over an interval with provenance and actor/counterpart scope. It may affect opportunity, time, activity, sanction or material ecology continuously or at specific junctures without being re-minted as a fictional event at every tick.

A condition/relation does not itself create psychological uptake. Its developmental relevance arises only when it changes realized activity, material state, interaction, decision, exposure, or other inputs lawfully received by V3.

## 4. Recurrent activity law

Repeated activity is a first-class causal temporal form because the empirical/theoretical corpus repeatedly identifies activity quality and duration as the transducer:

```text
STRUCTURAL ORGANIZATION
-> ACTOR'S RECURRENT TASK/PRACTICE ECOLOGY
-> ACTUAL REPEATED ACTS
-> V3 LEARNING/PRACTICE/CAPACITY CHANGE IF EARNED
```

Conscious appraisal on every repetition is not required. Actor uptake still matters where the V3 target requires appraisal/motive/meaning, but skill/capacity formation may proceed through repeated performance and feedback.

## 5. Transition and trajectory law

A transition is not just an event label. It is a realized boundary crossing that changes one or more active bindings. Its causal importance comes from what it rebinds afterward: roles, resources, obligations, schedules, institutions, counterparts, activities and opportunities.

A trajectory is an ordered history of those typed states and changes, not a latent destiny class.

## 6. Turning-point law

`TURNING_POINT` is derived, not primitive:

```text
candidate transition/event
+ sustained post-change alteration of relevant trajectory dimensions
+ counterfactual/baseline-sensitive evidence appropriate to use
= TURNING_POINT_PREDICATE_EARNED
```

The predicate may be retrospective and evidence-sensitive. It does not license a new event species whose occurrence automatically causes development.

## 7. Cumulative-process law

Cumulative advantage/disadvantage must be represented as explicit iteration:

```text
prior realized history
-> updated resource/eligibility/relation/opportunity state
-> changed next exposure/choice/gate distribution
-> next realized history
-> repeat
```

Protective support, agency, institutional change and historical shocks may interrupt or reverse the chain. Population-level widening inequality cannot be back-projected as an individual's psychological prior.

## Terminal

`TEMPORAL_FORMS_PROVED_COMPOSABLE_WITH_EXISTING_EVENT_HISTORY_BOOKENDS_PLUS_BOUNDED_GENERALIZATION__NO_EIGHT_CARRIER_ONTOLOGY_REQUIRED__TURNING_POINT_DERIVED__CUMULATIVE_PROCESS_REQUIRES_TYPED_ITERATIVE_UPDATE`.
