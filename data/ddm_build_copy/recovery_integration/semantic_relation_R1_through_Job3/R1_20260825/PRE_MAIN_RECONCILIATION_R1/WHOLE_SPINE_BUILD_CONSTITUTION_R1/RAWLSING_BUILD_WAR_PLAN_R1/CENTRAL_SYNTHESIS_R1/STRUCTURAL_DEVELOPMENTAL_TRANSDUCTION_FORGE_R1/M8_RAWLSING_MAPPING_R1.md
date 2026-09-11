# M8 — RAWLSING MAPPING R1

## Governing interpretation

Elder's useful unit is not "the Depression effect." It is a transduction path in which a historical structure changes concrete social conditions and those conditions are realized differently by actors according to position, relation, age/timing and subsequent history.

## Source construct → Rawlsing semantic mapping

| Elder construct/evidence | Rawlsing family/capability | Required grain | Prohibited collapse |
|---|---|---|---|
| Depression / Oakland economic collapse | PRE-V3 structural/historical source fact | world + historical interval + source provenance | macro event as actor exposure |
| father's occupation/business/labor-market position | D1 `POSITION_BINDING` | actor + role/occupation + time | class label alone |
| layoff/unemployment/underemployment | D1 realized work/resource state + D2 condition/transition | actor + employer/work relation + interval | "Depression victim" |
| household income loss | D1 `RESOURCE_DEPENDENCY` | household + amount/category + baseline + time | generic deprivation mechanism |
| expenditure cuts / consumption reprioritization | D1 resource/time activity consequence | target household domains | undifferentiated hardship |
| mother's employment | D1 activity/resource state + D2 transition/interval | mother + job relation + hours/time | female employment as trait |
| kin money / boarders / relief | D1 network support / institutional gate / counterpart relation | exact provider/institution + transfer | generic support |
| child paid job | D1 `ACTIVITY_ORGANIZATION` + resource/counterpart; D2 recurrent activity | child + employer/task + recurrence + earnings | "work ethic" |
| child domestic chores | D1 `ROLE_OBLIGATION` / `HOUSEHOLD_CARE_DEPENDENCY`; D2 recurrence | task + household counterpart + frequency/time | gender trait |
| marital power shift | D1 `AUTHORITY_CONTROL_SANCTION` + relation-qualified state | mother/father relation + domain + time | family climate scalar |
| paternal withdrawal/warmth/support | D1 active relation / support process | father-child relation + observed behavior + source | inferred father psychology |
| family conflict | D1 active relation/condition | counterpart pair + issue/domain + interval | stress scalar |
| peers/teachers/nonfamily adults | D1 `COUNTERPART_FORMATION` + `NETWORK_INFORMATION_SUPPORT` | actual relation/contact/support | abstract social capital |
| school/work opportunity | D1 `INSTITUTIONAL_GATE` + historical timing | school/employer rule + actor eligibility + period | age-only effect |
| age at shock | `HISTORICAL_TIMING_QUALIFICATION` + D2 | developmental phase + historical time + position | `AGE -> DEVELOPMENT` |
| recurring work/domestic labor | D2 recurrence | stable activity identity + quality/intensity/duration | repeated fake OEE events |
| education/work/marriage/parenthood/military changes | D2 transition rebinding | before/after positions and relations | event list without rebinding |
| ordered adult life course | D2 trajectory | ordered typed transition history | endpoint only |
| "turning point" | D2 derived predicate | sustained post-transition redirection evidence | primitive event type |
| work selection / drinking-employability loop | D3 gated reciprocal update | action → external response/gate → new social fact | bidirectional causality by assertion |
| adult continuity | history-qualified V3 ingress | exact prior realized history + current adult context | permanent childhood stamp |
| resilience/adaptation | derived assessment only | resources/support/actions/outcomes | generic resilience trait |

## D1 implementation-law consequences

A lawful Elder-style derivation is:

```text
STRUCTURAL FACT
+ EXACT ACTOR/HOUSEHOLD POSITION
+ EXACT RELATION/COUNTERPART
+ VALID HISTORICAL TIME
+ MECHANISM RULE
→ QUALIFIED ACTOR-RELATIVE ECOLOGY
+ REALIZATION EVIDENCE
→ ACTIVE SOCIAL FACT
```

### Cross-person update rule

For any parent→child or child→parent mechanism:

```text
source_actor_id
target_actor_id
relation_id/type
household/context_id
source_state_or_transition_ref
target_ecology_dimension
valid_time_or_interval
realization_status
provenance
negative_ceiling
```

must be present.

## D2 implementation-law consequences

Elder requires all of the following temporal forms to remain distinguishable:

```text
condition: father unemployed over interval
relation: father-child authority/support relation
recurrent activity: child job or chores
transition: mother enters labor force
trajectory: education→work→military→marriage→career sequence
turning point: derived only after sustained redirection
```

A transition should rebind all affected ecology dimensions audibly rather than append a disconnected event.

## D3 implementation-law consequences

D3 is not "feedback happened." It requires the bridge:

```text
actor action
→ realized external action
→ counterpart/institutional response or gate
→ objective new relation/resource/position/rule
→ later ecology derivation
```

Elder's unresolved work-selection directions should be represented as competing/limited evidence, not force-minted reciprocal causality.

## Demographic leakage guards

Reject:

```text
CLASS -> PARENT DISTRESS
SEX -> DOMESTICITY
DEPRIVATION -> INDUSTRY
AGE -> VULNERABILITY
DEPRESSION -> RESILIENCE
```

Require:

```text
class position
→ resource/status frame + actual loss
→ particular parent/household condition
→ observed response

gendered role rule + household labor need
→ task assignment/performance
→ activity exposure
→ downstream effect

age/historical time
→ dependency/eligibility/role position
→ mechanism route
→ outcome
```

## Evidence/provenance fields needed by M8

At minimum each mined mechanism claim should be able to retain:

- source bibliographic identity;
- printed page(s);
- evidence mode;
- direct vs retrospective measure;
- temporal-order status;
- mediation/selection status;
- subgroup/context boundary;
- null/negative ceiling;
- causal identification ceiling.

## Smallest architectural consequence

No D4 and no new social-world module.

The only architectural tightening demanded by Elder is to make the already implied D1 cross-person relation tuple **mandatory and testable**, while leaving D2 and D3 as the temporal and reciprocal complements.

This preserves the frozen candidate's minimality while preventing the precise shortcut Elder spent the book dismantling: macro condition or parent state directly becoming a child's psychology.
