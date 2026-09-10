# M1 — MORTIMER D1 / D2 / D3 CHALLENGE R1

STATUS: `M1_MORTIMER_D1_D2_D3_CHALLENGE_COMPLETE`

SOURCE: Jeylan T. Mortimer, *Working and Growing Up in America* (2003), full-book excavation.

TARGET: frozen synthesis candidate `9cf100a101e92891e2b4d0af0e308d27f7015a6b`.

This file does not ask whether Mortimer can be made to fit D1–D3. It asks whether D1–D3 survive the strongest positive, negative, selection-sensitive, temporal and heterogeneous evidence in the book without distortion.

## 1. D1 — `TYPED_ACTOR_RELATIVE_SOCIAL_ECOLOGY_DERIVATION`

### Challenge

Can D1 represent adolescent work without collapsing it into `EMPLOYED`, `HOURS`, `JOB QUALITY`, or an untyped positive/negative exposure?

### Mortimer pressure

Mortimer makes a scalar work exposure untenable.

The same job/work-investment pattern can simultaneously provide:

- learning and skill opportunity;
- advancement and earnings;
- status among peers;
- supervisory relations/support;
- psychological engagement;
- schedule demands and work-school compatibility;
- role overload, ambiguity, noxious conditions and other stressors.

Table 3.5 is especially diagnostic: more invested workers report more learning, advancement, earnings, engagement and status **and** more stress. Some dimensions—security, perceived good pay, supervisory support—do not vary significantly across investment patterns. Ch. 4 further shows that the work condition changes a broader ecology of family work, homework, extracurriculars, volunteering and social time, but not by a universal crowd-out law.

### D1 verdict

`SUPPORTED__STRENGTHENED__INTERNAL_SCHEMA_MUST_BE_NARROWED_AGAINST_SCALAR_JOB_QUALITY`

Mortimer does not require splitting D1 into multiple top-level capabilities. It requires D1's output to be a **typed vector/set of actor-relative facts**, each with its own provenance and realization status.

Minimum D1 discipline licensed by Mortimer:

```text
STRUCTURAL/ORGANIZATIONAL SOURCE
+ ACTOR POSITION / PHASE / CONTEXT / HISTORY
+ JOB / SCHOOL / FAMILY / LABOR-MARKET RULES
->
TYPED ACTOR-RELATIVE POSSIBILITIES
  learning_opportunity
  advancement_opportunity
  pay/income_resource
  schedule/time_obligation
  supervision/support_relation
  responsibility/control
  stressor/exposure
  school_compatibility/conflict
  peer_status
  other typed condition
->
TYPE-SPECIFIC REALIZATION
->
ACTUAL RECURRENT TASK / RELATION / CONDITION / EVENT
```

### Required D1 separations

```text
FORMAL JOB FEATURE != ENACTED CONDITION
OBJECTIVE CONDITION != SUBJECTIVE APPRAISAL
OPPORTUNITY != ACTUAL PARTICIPATION
PARTICIPATION != UPTAKE
ONE BENEFICIAL DIMENSION != GLOBALLY BENEFICIAL JOB
ONE BURDENSOME DIMENSION != GLOBALLY HARMFUL JOB
```

The frozen D1 already contains the key realization laws—for example, formal autonomy must pass through an enacted task/supervision state before it becomes exercised autonomy; task opportunity must become actual repeated performance before recurrent activity exists. Mortimer therefore **strengthens** rather than defeats D1.

### D1 boundary

Mortimer does not license D1 itself to create self-efficacy, values, depressive affect, identity or durable competence. Those are V3 targets/receivers.

---

## 2. D2 — `INTERVAL_RECURRENCE_AND_TRANSITION_REBINDING`

### Challenge

Does D2 preserve what is causally relevant about timing, duration, recurrence and transitions, or could work simply be represented as event counts/cumulative exposure?

### Mortimer pressure

Mortimer supplies unusually direct evidence that the temporal form is part of the mechanism:

1. current employment is not work history;
2. weekly intensity is not duration;
3. cumulative hours do not identify sequence/pattern;
4. long-duration/moderate-intensity “steady” work differs from long-duration/high-intensity “most invested” work in later educational attainment;
5. paid work can coexist with other recurring activities rather than simply displacing them;
6. contemporaneous problem-behavior differences can disappear after high school;
7. early earnings advantages can converge later;
8. the same adolescent work history has no family-transition association at 21–22 but predicts normatively timed family formation at 24–25;
9. transitions matter because the post-transition actor ecology—schooling, work, household, partner/parent roles, resources and obligations—is rebound.

### D2 verdict

`VERY_STRONGLY_SUPPORTED__GENERALIZE_PARAMETERS__DO_NOT_SPLIT_TOP_LEVEL_CAPABILITY`

Mortimer is among the strongest source tests for D2 because the book itself builds work-investment types from **duration × intensity** and then observes later phase-specific consequences.

Required D2 grain:

```text
ACTIVE_INTERVAL(
  start,
  end,
  intensity,
  typed condition set,
  counterpart/context
)

RECURRENCE(
  episode identity,
  persistence,
  gaps,
  repeated activity parameters
)

REBIND(
  before ecology,
  realized gate/transition,
  after ecology,
  provenance
)

ORDERED_HISTORY(
  interval/episode sequence,
  not merely cumulative scalar
)
```

### D2 negative ceiling

D2 must not automatically classify a long/recurrent exposure as developmental. Mortimer's long-term nulls show that recurrence may yield a transient response or no enduring change. Persistent change remains V3-owned.

---

## 3. D3 — `PROVENANCE_PRESERVING_RECIPROCAL_SOCIAL_WORLD_UPDATE`

### Challenge

Does Mortimer show a genuine person↔position reciprocal mechanism, and if so does it require more than D3's frozen external-gate law?

### Selection half

Ch. 5 strongly establishes that prior person state and social context precede later work pattern/quality:

- grades/educational promise;
- school engagement and motivation;
- problem behavior;
- peer orientation;
- motives for working;
- gendered opportunity sorting;
- family/background circumstances.

But these predictors do not directly manufacture a job. Employer availability, job type, labor-law thresholds, school schedules and other opportunity constraints mediate/gate occupancy.

Thus Mortimer reinforces:

`PERSON STATE -> SEARCH/PREFERENCE/PERSISTENCE/ELIGIBILITY PRESSURE != DIRECT POSITION MUTATION`.

### Socialization/development half

Ch. 6 shows that particular realized work qualities predict later person states under prospective controls:

- learning opportunities relate to occupational values;
- rewards/advancement relate to economic/work efficacy;
- work stress/control can relate to distress;
- intensive work relates to some near-term problem behavior.

Economic efficacy then predicts later educational plans/actions. Educational institutions subsequently gate enrollment/degree attainment.

The strongest defensible composite sequence is therefore:

```text
PRIOR PERSON STATE
-> GATED SELECTION INTO WORK PATTERN/QUALITY
-> REALIZED RECURRENT WORK EXPERIENCE
-> TARGET-SPECIFIC V3 CHANGE, IF EARNED
-> LATER PLAN/ACTION/SELECTION
-> EXTERNAL SCHOOL/EMPLOYER/PARTNER/INSTITUTION GATE
-> NEW POSITION / RELATION / RESOURCE / OBLIGATION
-> NEW ACTOR-RELATIVE ECOLOGY
```

### D3 verdict

`SUPPORTED__STRENGTHENED__EMPIRICALLY_PARTIAL__FROZEN_GATE_LAW_PRESERVED`

Mortimer does **not** demonstrate a single fully identified end-to-end causal loop with every institutional response observed. The book demonstrates component prospective links and makes reciprocity impossible to ignore. Therefore D3 is strengthened as architecture but not “proved” by one structural equation or experiment.

### D3 required provenance discipline

Every update must preserve:

- prior person-state source/time;
- actor action/selection attempt;
- external opportunity/gate/counterpart identity;
- actual gate response;
- resulting social fact/position/relation;
- time/context;
- evidence strength.

A model in which efficacy automatically writes `college_student=true` or motivation writes `high_quality_job=true` would directly violate Mortimer and the frozen D3 law.

---

## 4. Does Mortimer require splitting any candidate?

### D1 split court

**Candidate split:** objective work structure vs enacted work condition vs subjective experience.

**Verdict:** `DO_NOT_SPLIT_TOP_LEVEL D1`; preserve them as typed stages/statuses within D1 plus V3 subject mediation. The frozen D1 already distinguishes structural possibility, actor-relative possibility, realized social fact and V3 receiver.

### D2 split court

**Candidate split:** recurrence/duration versus transition rebinding.

**Verdict:** `DO_NOT_SPLIT TOP LEVEL`; both are temporal connective semantics and the frozen temporal court already composes them through `ACTIVE_INTERVAL`, `RECURRENCE`, `REBIND`, `ORDERED_HISTORY`.

### D3 split court

**Candidate split:** selection versus socialization feedback.

**Verdict:** `DO NOT SPLIT D3 INTO PERSON->WORLD AND WORLD->PERSON OWNERS`. The seam must preserve directionality, but world→person uptake remains V3-owned while person→later-world update requires D3's external gate. D3 exists precisely to prevent either direction from becoming a magical direct mutation.

---

## 5. D4 candidate court

### D4 proposal: `DEVELOPMENTAL_PHASE_QUALIFIED_TRANSDUCTION`

**Evidence for importance:** Ch. 6 adolescent work-quality/mental-health discussion; adolescent self-direction/control does not carry the invariant adult implication; Ch. 7 family-transition implications also change by age/time.

**Architectural verdict:** `REJECT_AS_GENUINELY_NEW_CAPABILITY`.

Reason: phase/history already enter the frozen D1 input; D2 preserves history and transition timing; existing ADP-008/Stage-A phase binding plus V3 prior-state/history are explicitly marked reusable/generalizable in the frozen coverage matrix.

### D4 proposal: `CROSS_DOMAIN_TIME_BUDGET_REBINDING`

**Evidence for importance:** Ch. 4 ecology-of-youthwork time-use findings.

**Architectural verdict:** `REJECT_AS_GENUINELY_NEW_CAPABILITY`.

Reason: D1 already owns typed time/activity ecology derivation and D2 owns interval/transition rebinding. What Mortimer adds is a hard negative ceiling against a universal crowd-out rule.

### D4 final

`NO_GENUINELY_MISSING_FOURTH_CONNECTIVE_CAPABILITY_LICENSED_BY_MORTIMER`.

---

## 6. Strongest challenge that D1–D3 survive

The hardest source result is not a positive coefficient. It is the combined pattern:

```text
EMPLOYMENT/HOURS
  -> little or no consistent mental-health / achievement effect

WORK QUALITY
  -> target-specific effects

HIGH INVESTMENT
  -> learning + advancement + earnings + status
  AND stress

HIGH-INTENSITY ADOLESCENT WORK
  -> some near-term problem behavior / early earnings
  BUT later behavioral and earnings differences attenuate

STEADY MODERATE WORK
  -> stronger B.A. attainment than most-invested work

PRIOR PERSON STATE
  -> selects later work pattern/quality

LATER PERSON STATE/ACTION
  -> still requires external gate to become later position
```

A synthesis that survives this must be typed, temporally explicit, selection-sensitive, nonmonotonic and provenance-preserving. D1–D3 survive **only under those constraints**.

## Terminal

`MORTIMER_STRENGTHENS_D1_D2_D3__NARROWS_THEIR_INTERNAL_CONTRACTS_AGAINST_SCALAR_WORK_PHASE_INVARIANCE_AND_DIRECT_PERSON_POSITION_MUTATION__NO_D4_LICENSED`.
