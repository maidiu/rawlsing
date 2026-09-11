# M6 RECIPROCAL CAUSATION COURT R1

STATUS: `RECIPROCAL_CAUSATION_ADJUDICATED__JOB_TO_PERSON_AND_PERSON_TO_JOB_SEPARATED__EXTERNAL_GATE_REQUIRED`

SOURCE: Melvin L. Kohn and Carmi Schooler et al., *Work and Personality* (1983), especially Chapters 3, 5-7, 9, 13 and Appendices A-C.

FROZEN SYNTHESIS TARGET: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`

## 0. Court question

The source must not be summarized as the slogan `WORK AND PERSONALITY ARE RECIPROCAL`. The court asks what is actually measured in each direction, over what interval, with what identification assumptions, and what unmeasured external process must exist before a psychological state can be said to alter later work.

Required Rawlsing form:

```text
JOB CONDITION_t
-> REALIZED/RECURRENT WORK ACTIVITY_t...t+n
-> PERSON_{t+n}

PERSON_t
-> ACTION / PERFORMANCE / SEARCH / PERSISTENCE / NEGOTIATION
-> ORGANIZATIONAL OR LABOR-MARKET GATE
-> LATER JOB/POSITION/CONDITION_{t+n}
```

No result in the book licenses `PERSON_STATE -> STRUCTURAL_POSITION` as an instantaneous primitive.

## 1. Evidence hierarchy

### Chapter 3 — 1964 cross-sectional reciprocal equations

Chapter 3 estimates simultaneous reciprocal relationships between occupational experience and psychological functioning using one-time data and instrumental restrictions. This is important historically because it rejects a one-way selection-only account, but it cannot establish temporal ordering. M6 therefore grades it:

`CROSS_SECTIONAL_STRUCTURAL_EQUATION__RECIPROCITY_PLAUSIBILITY_ONLY`.

It is not the decisive longitudinal court.

### Chapter 5 — substantive complexity and ideational flexibility

This is the cleanest longitudinal reciprocal model in the book. The design uses 1964 and 1974 measurements plus a pre-1964 measure of substantive complexity. The authors model measurement error and use restrictions/instruments to identify contemporaneous and lagged effects.

Strongest retained findings:

- current substantive complexity -> current ideational flexibility: statistically significant, approximately `.17-.18` in the preferred formulations;
- 1964 substantive complexity -> 1974 ideational flexibility as a direct cross-lag: small, approximately `.05`, and nonsignificant;
- earlier ideational flexibility -> later substantive complexity: large positive lagged path, approximately `.41-.45` in the preferred formulations.

The authors interpret this timing asymmetry as follows: actual intellectual demands of work can affect current intellectual functioning relatively quickly, whereas a person's intellectual flexibility affects job complexity only over time as jobs are changed, selected, or modified.

Evidence grade:

`LONGITUDINAL_SEM__STRONG_OBSERVATIONAL__NOT_RANDOMIZED`.

### Chapter 6 — broad job-condition/personality system

Chapter 6 extends the reciprocal model to fourteen job conditions and multiple psychological dimensions. The identification problem becomes much harder: with two waves separated by ten years, the number of free contemporaneous plus cross-lagged parameters would exceed what the data can identify.

The authors therefore prioritize contemporaneous relations among current job conditions, then test lagged effects selectively when contemporaneous effects are fixed to zero. They explicitly state that a nonsignificant contemporaneous estimate does not prove absence of a lagged effect.

This means:

```text
MODEL-ZEROED PATH != PROVED ABSENCE OF CAUSAL PATH
CONTEMPORANEOUS SEM PATH != INSTANTANEOUS REAL-WORLD EFFECT
LAGGED SEM PATH != OBSERVED TRANSITION MECHANISM
```

### Chapter 7 — occupational self-direction and distinct psychological targets

Chapter 7 reports reciprocal occupational-self-direction models. The pattern is heterogeneous rather than universally reciprocal.

Retained examples from Table 7.4:

| Psychological target | OSD -> person | person -> OSD | M6 reading |
|---|---:|---:|---|
| parental valuation of self-direction | `.14` | `.15` | reciprocal |
| valuation of self-direction for oneself | `.32` | `-.05` ns | work-dominant |
| ideational flexibility | `.27` | `.63` | strongly reciprocal |
| self-directedness of orientation | `.43` | `.28` | reciprocal |
| distress | `-.21` | `-.04` ns | work-dominant |
| alienation | `-.30` | `-.12` | some reciprocity |
| authoritarian-conservatism | `-.29` | `-.21` | some reciprocity |
| trustfulness | `.22` | `.01` ns | work-dominant |
| anxiety | `-.23` | `-.02` ns | work-dominant |

The court therefore rejects a generic rule that every psychological response feeds back into work with equal strength.

## 2. Job -> person court

### 2.1 What is the structural input?

Not occupation title. Not class by itself. The strongest job -> person evidence is for concrete conditions:

- substantive complexity;
- closeness of supervision;
- routinization;
- job protections and loss risk;
- time/physical pressures;
- selected risks/rewards.

### 2.2 What is the mediator?

The source's central interpretation is learning/generalization from what the worker repeatedly has to do. For substantive complexity this is unusually concrete: the actor repeatedly analyzes, coordinates, synthesizes, handles ill-defined contingencies, chooses among alternatives, negotiates, instructs, adjusts, or otherwise exercises independent judgment.

For supervision, the recurring condition is a restriction on what/how/speed and on permissible disagreement. For routinization it is repeated exposure to fixed/predictable task organization. For distress-producing conditions it is chronic exposure to aversive or insecure work conditions.

The book does not directly observe each daily act, so the middle is partly inferred from detailed task measurement plus persistent employment in the measured condition.

### 2.3 Timing

The strongest complexity -> flexibility estimate is contemporaneous in the structural model, not a clean ten-year cross-lag. This matters. The authors' interpretation is that the influence is ongoing/current rather than only delayed by a decade.

Rawlsing must not translate this as a single event at interview date. The natural representation is:

```text
ACTIVE_JOB_CONDITION(interval)
-> RECURRENT_TYPED_ACTIVITY(history over interval)
-> V3 DEVELOPMENTAL CONSEQUENCES IF EARNED
```

### 2.4 Strength

Verdict:

`JOB_TO_PERSON_EVIDENCE = STRONG_OBSERVATIONAL_FOR_SUBSTANTIVE_COMPLEXITY_AND_SELF_DIRECTION_FAMILY__MODERATE/MIXED_FOR_OTHER_FIRST_ORDER_CONDITIONS__NOT_RANDOMIZED`.

The book materially strengthens the recurrent-activity seam but does not identify a precise dose-response function.

## 3. Person -> job court

### 3.1 What is actually demonstrated?

The strongest demonstration is that prior ideational flexibility predicts later substantive complexity, even in longitudinal models controlling prior complexity and multiple background variables. Several self-directed orientations also predict later occupational self-direction. Other targets, including distress, anxiety and trustfulness, show weak or null reverse paths.

Thus person -> later job feedback is real enough to require representation, but it is target-specific.

### 3.2 What is not observed?

The panel does not continuously record:

- job applications;
- employer screening decisions;
- promotions;
- performance evaluations;
- bargaining/negotiation;
- voluntary quits;
- layoffs;
- informal job redesign;
- internal transfers;
- labor-market vacancies;
- institutional eligibility decisions.

The authors therefore infer that, over a sufficiently long interval, people either move to jobs more consonant with their capacities/orientations or modify aspects of their jobs.

M6 treats that as `AUTHOR_INTERPRETATION_SUPPORTED_BY_LAGGED_ASSOCIATION`, not as a directly measured gate mechanism.

### 3.3 Required Rawlsing normalization

The minimum lawful representation is:

```text
PERSON_CAPACITY_OR_ORIENTATION_t
-> ACTOR_ACTION_OR_PERFORMANCE_t...t+n
-> EXTERNAL_ORGANIZATIONAL/LABOR_MARKET_GATE_t...t+n
-> CAUSALLY_ADMITTED_POSITION/JOB_CHANGE
-> NEW_CONCRETE_JOB_CONDITION_{t+n}
```

A model may leave the exact action subtype unresolved when evidence is unavailable, but it may not omit the existence of an external realization step.

### 3.4 Direct structural-position paths

Ownership and hierarchical position are not well supported as direct contemporaneous products of personality. Chapter 6's modeling treats major changes in ownership/hierarchy as job/position changes and therefore structurally different from instantly altering a task condition.

This is strong support for the D3 firewall:

`PERSON_CHANGE != WORLD_CHANGE`.

## 4. Selection versus molding

The source allows two nonexclusive processes:

1. **selection/mobility** — actor moves into another job whose conditions better fit capabilities/orientations;
2. **job molding** — actor gradually changes how an existing job is organized or what tasks are undertaken.

The two-wave panel does not identify their relative contribution. Rawlsing must preserve this uncertainty rather than invent a specific career mechanism.

Normalized gate family:

`GATED_RECIPROCAL_SELECTION_OR_JOB_MODIFICATION`.

## 5. Recurrent reciprocal loop

The book's strongest architectural implication is a loop, not a direct bidirectional edge:

```text
STRUCTURAL/ORGANIZATIONAL POSITION_t
-> CONCRETE WORK CONDITION_t
-> RECURRENT WORK ACTIVITY_t
-> PERSON CHANGE_t+1
-> ACTION/PERFORMANCE/SELECTION_t+1
-> EXTERNAL GATE/ORGANIZATIONAL RESPONSE_t+1
-> LATER POSITION/WORK CONDITION_t+2
-> NEW RECURRENT ACTIVITY_t+2
-> FURTHER PERSON CHANGE_t+3
```

Only a portion of one such cycle is directly observed across the 1964-1974 panel. Multi-cycle amplification is theoretically plausible and explicitly contemplated by the authors, but not empirically followed through several complete cycles.

Verdict:

`RECIPROCAL_LOOP_SUPPORTED_AS_COMPOSITION__MULTI_CYCLE_CUMULATION_NOT_DIRECTLY_IDENTIFIED`.

## 6. Generalization outside work

Chapter 9 materially strengthens the claim that work effects are not confined to an interview-based psychological scale. Substantive complexity predicts the intellectuality of reported leisure activities, and earlier leisure intellectuality predicts later work complexity for men.

This supports a practice-to-practice feedback possibility:

```text
COMPLEX WORK PRACTICE
-> NONWORK INTELLECTUAL PRACTICE
-> LATER WORK SELECTION/COMPLEXITY
```

But the exact transfer process remains interpreted as learning-generalization/facilitation rather than directly observed at the moment of transfer. Ideational flexibility does not fully mediate the work -> leisure relationship, which blocks reduction to a single hidden trait.

## 7. Identification court

### 7.1 What longitudinal SEM earns

It earns substantially more than cross-sectional correlation because it:

- models prior states;
- incorporates repeated measures;
- explicitly tests reciprocal directionality;
- handles measurement error through latent measurement models;
- uses pre-1964 complexity as an instrument in the strongest Chapter 5 model;
- controls a wide set of social-background variables.

### 7.2 What it does not earn

It does not provide:

- random assignment to job conditions;
- immunity from time-varying confounding;
- direct observation of daily activity recurrence;
- exact transition dates;
- direct observation of the person -> organization gate;
- a universal causal coefficient valid across cohorts/sexes/countries;
- a complete model of subjective appraisal;
- a proved dose/duration threshold.

Therefore:

`SEM_PATH_COEFFICIENT != RANDOMIZED_CAUSAL_IDENTIFICATION`.

## 8. Reciprocal nulls and asymmetries

The absence of reverse effects for several outcomes is theoretically important:

- own valuation of self-direction -> later OSD: weak/nonsignificant;
- distress -> later OSD: weak/nonsignificant;
- trustfulness -> later OSD: null;
- anxiety -> later OSD: null;
- reverse effects involving routinization are comparatively weak;
- women lack equivalent longitudinal reciprocal measurement.

These nulls argue for typed feedback channels rather than a generic `PERSONALITY_CAUSES_JOB` rule.

## 9. Court verdicts

```text
JOB_CONDITION -> PERSON:
PASS__STRONG_OBSERVATIONAL_RECIPROCAL_PROGRAM__BEST_FOR_SUBSTANTIVE_COMPLEXITY_AND_OCCUPATIONAL_SELF_DIRECTION

PERSON -> JOB_CONDITION:
PASS__LAGGED_ASSOCIATION_STRONGLY_SUPPORTED_FOR_IDEATIONAL_FLEXIBILITY_TO_LATER_COMPLEXITY__PATHWAY_GATE_NOT_DIRECTLY_OBSERVED

DIRECT_PERSON -> STRUCTURAL_POSITION:
REJECT

RECURRENT_ACTIVITY_MEDIATION:
PASS_AS_REQUIRED_INTERPRETIVE_MIDDLE__ACTIVITY_CONTENT_WELL_MEASURED__RECURRENCE_HISTORY_NOT_CONTINUOUSLY_OBSERVED

MULTI_CYCLE_AMPLIFICATION:
DEFER_AS_COMPOSITIONAL_THEORY_BEYOND_ONE_OBSERVED_LONG_INTERVAL
```

## 10. D3 consequence

The frozen synthesis D3 is `PROVENANCE_PRESERVING_RECIPROCAL_SOCIAL_WORLD_UPDATE`. M6 strongly supports it, with one sharpening:

```text
PERSON_CHANGE
MUST NOT
DIRECTLY UPDATE JOB/POSITION.

PERSON_CHANGE
MAY AFFECT
ACTION/PERFORMANCE/SEARCH/PERSISTENCE/NEGOTIATION,
WHICH MUST PASS THROUGH
AN EXTERNAL ORGANIZATIONAL/LABOR-MARKET GATE
BEFORE LATER POSITION/CONDITION IS ADMITTED.
```

No D4 is required to express the Kohn/Schooler reciprocal loop if D3 preserves this gate and D2 carries the resulting transition/history.