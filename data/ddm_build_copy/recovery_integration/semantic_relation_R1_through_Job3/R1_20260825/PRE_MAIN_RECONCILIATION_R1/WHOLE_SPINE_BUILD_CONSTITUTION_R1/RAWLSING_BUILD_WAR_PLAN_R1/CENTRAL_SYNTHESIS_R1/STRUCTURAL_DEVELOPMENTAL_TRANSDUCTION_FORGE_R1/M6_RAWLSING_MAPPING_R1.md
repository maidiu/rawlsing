# M6 RAWLSING MAPPING R1

STATUS: `FULL_SOURCE_TO_FROZEN_SEAM_MAPPING_COMPLETE__NO_V3_OWNER_SEIZURE__NO_NEW_D4`

PRIMARY SOURCE: Kohn & Schooler et al., *Work and Personality* (1983).

FROZEN SYNTHESIS TARGET: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`.

This file maps M6 findings to the frozen candidate only. It does not alter the frozen target, consume sibling excavations, or authorize project-current architecture.

## 0. Frozen seam recalled

The frozen candidate requires three positive connective capabilities:

```text
D1 TYPED_ACTOR_RELATIVE_SOCIAL_ECOLOGY_DERIVATION
D2 INTERVAL_RECURRENCE_AND_TRANSITION_REBINDING
D3 PROVENANCE_PRESERVING_RECIPROCAL_SOCIAL_WORLD_UPDATE
```

M6 tests those against a full-book empirical program whose mature causal logic is:

```text
SOCIAL/ORGANIZATIONAL POSITION
-> CONCRETE JOB CONDITIONS
-> ACTUAL/RECURRENT WORK ACTIVITY OR PERSISTENT EXPOSURE
-> DISTINCT PSYCHOLOGICAL/BEHAVIORAL CHANGE
-> DELAYED PERSON-DEPENDENT ACTION/SELECTION
-> EXTERNAL ORGANIZATIONAL/LABOR-MARKET GATE
-> LATER JOB CONDITION
```

## 1. Source object -> Rawlsing seam mapping

| Kohn/Schooler object | Source semantics | Rawlsing mapping | Verdict |
|---|---|---|---|
| social class | ownership/control relation; not status | PRE-V3 structural fact/position input | `REUSE_INPUT__NO_DIRECT_PSYCHOLOGY` |
| social stratification | status hierarchy, education/status/income covariance | admitted empirical/structural descriptor, not mechanism | `EVIDENCE_OR_POSITION_INPUT` |
| occupation title | nominal occupational locator | possible search/qualification evidence only | `REJECT_AS_WORK_CONTENT` |
| occupational status | prestige/status location | position/empirical descriptor | `REJECT_AS_JOB_CONDITION` |
| ownership | organizational/class position | D1 `RESOURCE_DEPENDENCY` / structural-position input as applicable | `REUSE/GENERALIZE` |
| bureaucratization | organization size/formal levels | D1 structural input affecting typed work ecology | `GENERALIZE__NO_DIRECT_TRAIT_EDGE` |
| hierarchical position | supervisory authority location | D1 `AUTHORITY_CONTROL_SANCTION` input | `GENERALIZE` |
| substantive complexity | actor-specific task demand for thought/judgment | D1 `ACTIVITY_ORGANIZATION` qualified/active condition -> D2 recurrent activity | `STRONG_SUPPORT` |
| closeness of supervision | active discretion/obedience/speed-control relation | D1 `AUTHORITY_CONTROL_SANCTION` -> D2 recurrent constrained/exercised control history | `STRONG_SUPPORT` |
| routinization | repetitive/predictable task organization | D1 `ACTIVITY_ORGANIZATION` -> D2 typed recurrence | `SUPPORT_WITH_MEASUREMENT_CAUTION` |
| time pressure/hours | work-time demand | D1 `TIME_ALLOCATION`; D2 interval exposure | `GENERALIZE` |
| heaviness/dirtiness | physical work condition | D1 activity/condition ecology; existing embodied/event receivers only if type-compatible | `GENERALIZE_TYPED` |
| job loss risk/protections | security/resource/risk condition | D1 `RESOURCE_DEPENDENCY` / `PERSISTENT_STRAIN_CONDITION` | `GENERALIZE` |
| job income | material reward/resource | D1 `RESOURCE_DEPENDENCY`; keep distinct from complexity | `GENERALIZE` |
| occupational self-direction | second-order composite of complexity, low supervision, low routine | measurement summary only; decompose into D1/D2 first-order facts | `DO_NOT_MINT_AS_BLACK_BOX_OWNER` |
| ideational flexibility | psychological functioning target | existing V3 development/learning/cognition jurisdiction | `NO_SEAM_OWNERSHIP` |
| self-directed orientation | psychological orientation target | existing V3 target | `NO_SEAM_OWNERSHIP` |
| distress/anxiety/etc. | distinct psychological/affective targets | existing V3 targets | `NO_SEAM_OWNERSHIP` |
| leisure intellectuality | realized nonwork activity pattern | actor-indexed realized practice/history; D2 if social ecology carrier needed, V3 practice/learning downstream | `COMPOSITION` |
| person -> later job association | delayed selection/molding | D3 gated reciprocal social-world update | `STRONG_SUPPORT_WITH_GATE` |

## 2. D1 mapping in detail

### 2.1 Structural source facts

M6 supplies empirical support for using admitted structural position as an input rather than a psychological prior. Relevant position facts include:

- ownership/nonownership;
- formal hierarchy and supervisory authority;
- organization size/bureaucratic structure;
- occupational placement/status;
- education and income where they affect eligibility/resources/placement.

No one of these directly yields a psychological state.

### 2.2 Typed actor-relative ecology outputs

D1 should be able to derive work-domain facts such as:

```text
ACTIVITY_TASK_COMPLEXITY_REQUIREMENT
SUPERVISORY_DISCRETION_CONSTRAINT
TASK_ROUTINIZATION_PREDICTABILITY
JOB_SECURITY_OR_LOSS_RISK
JOB_PROTECTION_RESOURCE
TIME_PRESSURE_OR_HOURS_CONSTRAINT
PHYSICAL_WORK_DEMAND
JOB_INCOME_RESOURCE
RESPONSIBILITY_OUTSIDE_CONTROL
```

These are actor-relative because the worker actually occupies the job/role to which they apply.

### 2.3 Realization rule

For Kohn/Schooler, occupation category does not realize the condition. The realization must bind the actor to actual job content and, where activity is concerned, to actual performance.

Canonical M6 D1 rule:

```text
ADMITTED ORGANIZATIONAL/CLASS POSITION
+ ACTOR JOB/POSITION BINDING
+ WORK-ORGANIZATION RULE / ACTUAL JOB-CONTENT EVIDENCE
-> TYPED ACTOR-RELATIVE WORK CONDITION
```

For exercised control:

```text
FORMAL/RELATIONAL AUTHORITY CONFIGURATION
+ ACTUAL TASK/SUPERVISION ARRANGEMENT
-> ACTOR-SPECIFIC DISCRETION/CONTROL CONDITION
```

Not yet psychological uptake.

## 3. D2 mapping in detail

### 3.1 Why event-only is insufficient

The source's principal explanatory object is an ongoing job. Its influence is tied to what the actor repeatedly does or endures across time.

Examples:

- complex task demand is a persistent condition;
- solving complex problems is recurrent activity;
- supervision is an active relation plus recurrent constraint episodes;
- routinization is recurrent/predictable activity organization;
- insecurity/protection is a persistent condition;
- job change/promotion is a transition requiring rebinding.

### 3.2 Required recurrent-activity representation

For the strongest source mechanism:

```text
ACTIVE_SUBSTANTIVE_COMPLEXITY(interval)
-> RECURRENT_ACTIVITY {
     analysis,
     synthesis,
     coordination,
     independent judgment,
     ill-defined problem solving,
     negotiation/instruction/adjustment
   }
-> typed realized history
```

D2 must preserve activity quality. It may not treat `100 repetitions` of a fixed routine as semantically equivalent to `100 episodes` of complex judgment.

### 3.3 Duration uncertainty

The source requires duration/recurrence to be representable but does not supply a universal dose law. Therefore D2 fields may be factual/provenance-bearing without hard-coded causal coefficients.

### 3.4 Transition rebinding

When an actor changes job or hierarchical/ownership position, the old job conditions must not persist by inertia. Required sequence:

```text
ADMITTED JOB/POSITION TRANSITION
-> CLOSE/ALTER OLD WORK-CONDITION INTERVALS
-> BIND NEW POSITION/JOB
-> D1 RE-DERIVE NEW TYPED CONDITIONS
-> D2 BEGIN NEW RECURRENT/PERSISTENT HISTORY
```

This directly matches the frozen transition-rebinding law.

## 4. D3 mapping in detail

### 4.1 Source evidence

Prior ideational flexibility predicts later substantive complexity strongly; some self-directed orientations predict later occupational self-direction. Reverse paths are heterogeneous rather than universal.

### 4.2 Rawlsing-safe normalization

Required D3 work-domain form:

```text
V3 PERSON STATE/CAPACITY/ORIENTATION
-> REALIZED ACTOR ACTION/PERFORMANCE/SEARCH/NEGOTIATION/EXIT/PERSISTENCE
-> ORGANIZATION / EMPLOYER / LABOR-MARKET GATE OR RESPONSE
-> ADMITTED JOB/POSITION/TASK CHANGE
-> NEW PROVENANCE-BEARING SOCIAL FACT
-> D1/D2 REBINDING
```

The exact action/gate subtype is not supplied by the panel and must not be invented when source evidence is absent.

### 4.3 Selection versus molding

D3 must permit both:

- transition into a different job;
- modification of current work content through an externally realized organizational process.

M6 cannot choose between them for an individual case.

## 5. Existing V3 boundary

M6 provides no reason to mint a second psychology in the seam.

The seam may publish realized work/social facts and recurrent histories. Existing V3 authority remains responsible for:

- subjective appraisal/perception;
- response/recruitment;
- learning;
- memory;
- motive/striving;
- durable capacity change;
- value/orientation change;
- distress/affective consequence;
- practice generalization;
- biography/path dependence.

M6 source support for a causal relation does not authorize the seam to own the downstream psychological target.

## 6. Special invariant court — OCCUPATION TITLE != WORK CONTENT

### Source basis

The book asks respondents what they actually do, with what data/people/things, what operations they perform, how complex the contingencies are, how they are supervised, and how repetitive/predictable the work is. Later review explicitly warns that occupation-average DOT complexity underestimates relationships relative to actor-specific job content.

### Proposed binding Rawlsing invariant

```text
NOMINAL OCCUPATION OR OCCUPATIONAL STATUS
MAY NOT, BY ITSELF, CAUSALLY ADMIT
ACTOR-SPECIFIC TASK COMPLEXITY,
SUPERVISION,
ROUTINIZATION,
EXERCISED CONTROL,
OR RECURRENT ACTIVITY HISTORY.
```

An occupation may narrow a possibility set or serve as empirical evidence under governed authority; realization still requires a position/content derivation.

Verdict: `ADOPT_CANDIDATE_INVARIANT_FOR_VOZHD_ADJUDICATION`.

## 7. Special court — STRUCTURAL CONTROL -> EXERCISED CONTROL HISTORY

M6 finds this distinction necessary but compositional.

```text
D1:
FORMAL AUTHORITY / SUPERVISORY RELATION
-> ACTOR-SPECIFIC DISCRETION/TASK CONDITION

D2:
ACTOR-SPECIFIC DISCRETION/TASK CONDITION
-> ACTUAL RECURRENT EXERCISE/CONSTRAINT HISTORY

V3:
REALIZED HISTORY
-> PSYCHOLOGICAL CONSEQUENCE IF EARNED
```

Verdict: `REQUIRED_SEMANTIC DISTINCTION__NO_D4`.

## 8. Special court — recurrent activity seam

The source supports the recurrent-activity seam more strongly than an event-only rendering because its substantive-complexity measure describes the intellectual/practical acts repeatedly demanded by work. The longitudinal work/person findings are consistent with developmental influence of such repeated exercise.

But:

- actual daily acts were not directly logged;
- exact frequency/dose is unknown;
- temporal onset is unresolved.

Verdict:

`PASS__RECURRENT_ACTIVITY_IS_REQUIRED_CAUSAL_FORM__MICRO_DOSAGE_NOT_IDENTIFIED`.

## 9. Special court — reciprocal loop

Minimum representation:

```text
WORK_CONDITION_t
-> RECURRENT_ACTIVITY_t
-> PERSON_CHANGE_t+1
-> ACTOR_ACTION_t+1
-> EXTERNAL_GATE_t+1
-> LATER_WORK_CONDITION_t+2
-> RECURRENT_ACTIVITY_t+2
-> ...
```

This is D1 + D2 + D3 composition. No new loop owner is necessary.

Verdict: `PASS__COMPOSITION_SUFFICIENT`.

## 10. Family/intergenerational mapping

The source does not justify direct parent/class inheritance. Any use of parental work effects must remain relational and realized:

```text
PARENT WORK/SOCIAL CONDITION
-> PARENT PERSON CHANGE
-> ACTUAL FAMILY PRACTICES / EXPECTATIONS / INTERACTIONS
+ SCHOOL/PEER/INSTITUTIONAL CONTEXT
-> CHILD REALIZED EXPERIENCE
-> CHILD UPTAKE/DEVELOPMENT IF EARNED
```

Chapter 11's serfdom legacy is `DEFER/EVIDENCE_ONLY` for architecture because intermediate mechanisms are not measured.

## 11. Class/stratification decomposition mapping

M6 does not conclude that class or stratification are causally irrelevant. It concludes that their developmental use must proceed through concrete actor-relative conditions.

Substantial portions of class/status associations with:

- valuation of self-direction;
- ideational flexibility;
- self-directedness of orientation;

are accounted for by occupational self-direction. Some education/income and other effects remain.

Rawlsing mapping:

`CLASS/STRATIFICATION -> D1-TYPED CONDITIONS`, not `CLASS/STRATIFICATION -> V3 TRAIT`.

## 12. Evidence-grade mapping

| Source evidence | Architectural use |
|---|---|
| detailed work-content measurement | strong semantic evidence for typed D1 outputs |
| 1964 cross-sectional associations | supporting evidence, not causal authority alone |
| Chapter 3 simultaneous equations | reciprocity hypothesis support only |
| Chapter 5 longitudinal SEM | strongest evidence for complexity <-> flexibility timing asymmetry |
| Chapter 6 broad longitudinal SEM | typed work-condition/person relations with identification caveats |
| Chapter 7 mediation/decomposition | strong support against class/status shortcut |
| Chapter 9 leisure behavior | supports cross-domain practice generalization, downstream V3 |
| women/housework extensions | generalization evidence with weaker design and measurement failures |
| cross-national review | mechanism plausibility/generalization, not universal law |
| Chapter 13 unresolved issues | binding negative ceilings and future evidence requirements |

## 13. D1-D3 coverage verdict

```text
D1: STRONGLY SUPPORTED; ADD OCCUPATION-TITLE INVARIANT AND FIRST-ORDER WORK-CONDITION PROVENANCE.

D2: STRONGLY SUPPORTED; RECURRENCE MUST CARRY ACTIVITY QUALITY, CONTROL AND INTERVAL, NOT EVENT COUNT ALONE.

D3: STRONGLY SUPPORTED; REQUIRE EXPLICIT ACTOR ACTION + EXTERNAL ORGANIZATIONAL/LABOR-MARKET GATE BEFORE WORLD UPDATE.

D4: NOT REQUIRED BY THIS SOURCE.
```

## 14. Smallest architectural consequence

M6's smallest consequence for post-review Vozhd adjudication is not a new module. It is four constraints on the frozen three-delta candidate:

1. **Bind `OCCUPATION_TITLE != WORK_CONTENT`.**
2. **Require D1 work outputs to remain typed and first-order** rather than collapsing into OSD/job-quality/status.
3. **Require D2 recurrent histories to retain activity quality/control/duration**, while allowing exact dose to remain unknown.
4. **Require D3 person-driven work change to traverse an external gate** before D1/D2 are rebound.

Everything psychological remains downstream under existing V3 authority.