# M6 MEASUREMENT AND CONSTRUCT LEDGER R1

STATUS: `CONSTRUCT_DECOMPOSITION_COMPLETE__NO_LATENT_COMPOSITE_TREATED_AS_MECHANISM`

SOURCE: Kohn & Schooler, *Work and Personality* (1983), especially chs. 1, 5-7 and apps. A-D.

## 0. Governing separations

```text
OCCUPATION TITLE != OCCUPATIONAL STATUS != WORK CONTENT
SOCIAL STRATIFICATION != SOCIAL CLASS
ORGANIZATIONAL POSITION != OCCUPATIONAL SELF-DIRECTION
FORMAL FREEDOM FROM SUPERVISION != ACTUAL EXERCISE OF JUDGMENT
SUBSTANTIVE COMPLEXITY != ROUTINIZATION != CLOSENESS OF SUPERVISION
OCCUPATIONAL SELF-DIRECTION != ANY ONE OF ITS FIRST-ORDER CONDITIONS
JOB CONDITION != SUBJECTIVE APPRAISAL
PSYCHOLOGICAL FUNCTIONING != ONE GENERIC PERSONALITY VARIABLE
```

## 1. Occupation title

**Measurement role:** locator/name of principal occupation and institutional locus; used to orient the interview.

**Not used as:** a sufficient measure of what the respondent actually does.

Immediately after title/locus, the interview probes actual tasks, time allocation, materials, tools, data and interactions (ch. 1, pp. 23-26). Appendix B classifies those activities by complexity. Chapter 12 warns that occupation-level DOT approximations to substantive complexity may be useful when individual job data are absent, but they seriously underestimate relationships relative to person-specific job descriptions (p. 289 n.5).

**M6 verdict:** occupation title is a lossy proxy for actor-specific job content.

**Binding candidate:** `OCCUPATION_TITLE != WORK_CONTENT`.

## 2. Occupational status

**Meaning:** hierarchical/prestige location of an occupation in the stratification order, represented using Hollingshead and, later, several occupational-status classifications.

**Role in chapter 7:** indicator of social-stratification position and, with job income, of occupational position.

**Negative ceiling:** status does not tell us the actor's substantive complexity, supervision, routinization, protections, task demands or actual autonomy. When concrete occupational self-direction conditions are modeled, much apparent status -> psychology association is absorbed or even changes sign.

## 3. Social-stratification position

**Chapter 1:** continuous hierarchy primarily represented by education and occupational status.

**Chapter 7 measurement model (pp. 155-157):** second-order latent factor inferred from shared variance of occupational status, education and job income.

**Important warning:** occupational-status classifications themselves partly encode education/income requirements, so the status loading may be exaggerated.

**Negative ceiling:** shared variance is a descriptive/statistical construct, not a social mechanism. It cannot produce actor psychology without mediation.

## 4. Social class

**Definition in the mature book:** groups defined by relationship to ownership and control of the means of production; intentionally distinguished from a status hierarchy (ch. 7, p. 155).

**Operational ingredients:** ownership/nonownership and control/hierarchical relations, with categories developed to avoid defining class by occupational self-direction itself.

**Critical conceptual law:** if autonomy/self-direction were built into the class definition, it could not then function as the mechanism by which class position affects work experience and psychological functioning.

**Negative ceiling:** class category does not itself specify task complexity, supervision, routinization, income risk or realized action.

## 5. Occupational position

**Chapter 7 usage:** a latent summary of occupational status and job income, separated from education for some analyses.

**Not the same as:** the structure of actual job conditions.

**Negative ceiling:** occupational position is a placement/status construct, not the activity history.

## 6. Ownership

**Operationalization:** dichotomy contrasting men with full/partial ownership of the employing firm with nonowners (ch. 1 n.18; ch. 6 p. 129 n.4).

**Causal role:** organizational/class position that may alter complexity, hierarchy, risks/rewards and other conditions.

**Reciprocal result:** later ownership is only weakly predicted directly by prior psychological functioning; the strongest person -> work path is through job conditions rather than a direct psychology -> ownership jump.

**Negative ceiling:** owner/nonowner does not tell us actual occupational self-direction.

## 7. Bureaucratization

**Operationalization:** size and supervisory complexity/number of formal levels in the employing organization (ch. 6 p. 129 n.4; ch. 2).

**Causal role:** organizational structure that affects more proximal job conditions.

**Negative ceiling:** `BUREAUCRATIC_ORGANIZATION != CLOSE_SUPERVISION != LOW_SELF_DIRECTION` for any given actor. The book finds effects mediated and sometimes contrary to simple “bureaucratic man” expectations.

## 8. Hierarchical position

**Operationalization:** number of people over whom respondent reports direct/indirect supervisory authority (ch. 6 p. 129 n.4).

**Causal role:** organizational location affecting job conditions, particularly complexity and supervision.

**Temporal point:** a substantial change in hierarchical position is treated as a job/structural transition, so the SEM disallows instantaneous contemporaneous psychological-state -> hierarchy updates.

**Negative ceiling:** hierarchical rank is not the same as actual discretion or task complexity.

## 9. Substantive complexity

**Definition:** degree to which performance of work requires thought and independent judgment; complex work requires decisions under ill-defined/apparently conflicting contingencies (ch. 5 pp. 105-109; ch. 6 p. 127).

**Measurement:** multiple indicators from detailed job description:

- overall job complexity;
- complexity of work with data, people, things;
- time spent in those domains;
- pre-1964, 1964, 1974 versions where available.

**Appendix B operational content:** upper categories explicitly involve analyzing, coordinating, synthesizing, complex problem-solving, multiple variables, unpredictable contingencies, originality/insight, negotiation/instruction/mentoring, precision control and adjustment.

**Mechanism-bearing content:** it indexes what the worker repeatedly has to *do* intellectually and practically.

**Negative ceiling:** it is not occupation prestige, formal autonomy, education, general intelligence or a class label.

## 10. Closeness of supervision

**Chapter 1 five-item scale (pp. 23-25):** who decides what/how; whether supervisor tells versus discusses; freedom to disagree; who controls work speed; importance of doing what one is told.

**Chapter 6 longitudinal model:** subjective reports of freedom/disagreement/instruction and importance of obedience.

**Causal semantics:** close supervision restricts opportunity to exercise occupational self-direction.

**Asymmetry:** absence of close supervision is necessary/facilitative but not sufficient for actual self-direction. A worker can be left alone while doing mechanically fixed work.

**M6 invariant:** `FREEDOM_FROM_SUPERVISION != EXERCISED_JUDGMENT`.

## 11. Routinization

**Meaning:** repetitive/predictable organization of tasks; ranges from same task same way repeatedly to varied/unpredictable tasks.

**Longitudinal measurement limitation:** the earlier “unit of work” indicator cross-loaded on complexity and supervision, so ch. 6 reduces routinization to essentially one item enriched by predictability information.

**Causal interpretation:** repetitive/predictable work reduces occasions that call for initiative/thought/judgment; varied/unpredictable work creates them.

**Negative ceiling:** routinization is not merely frequency/repetition. Repetition of *complex judgment* and repetition of a fixed mechanical procedure have opposite theoretical implications. Rawlsing must preserve activity quality as well as recurrence.

## 12. Occupational self-direction

**Definition:** use of initiative, thought and independent judgment in work.

**Measurement model:** second-order concept reflected by substantive complexity (+), freedom from close supervision, and low routinization (ch. 6 pp. 127-129; app. C).

**Interpretive role:** major mediator between social structure and multiple psychological outcomes.

**Negative ceiling:** occupational self-direction cannot be inserted into Rawlsing as a black-box mechanism. It must be unpackable into the concrete conditions and realized activity that make self-direction possible/actual.

## 13. Formal autonomy versus actual exercised judgment

The source does not use a single “formal autonomy” scale equivalent to exercised self-direction. Its architecture instead forces a separation:

```text
LESS SUPERVISION
+ COMPLEX/DEMANDING TASK CONTENT
+ NONROUTINIZED TASK ORGANIZATION
-> GREATER OPPORTUNITY/REQUIREMENT TO EXERCISE
   INITIATIVE, THOUGHT, JUDGMENT
```

This is the source basis for the M6 question `STRUCTURAL_CONTROL -> EXERCISED_CONTROL_HISTORY`.

M6 verdict: the book requires the distinction, but it does not require a new D4 if D1 can produce enacted control/task conditions and D2 can preserve the recurrent exercise history.

## 14. Fourteen job conditions (“structural imperatives”)

Chapter 6 (pp. 126-129) distinguishes four groups:

| Family | First-order condition | Measurement/meaning |
|---|---|---|
| Organizational position | ownership | full/partial owner vs nonowner |
| Organizational position | bureaucratization | size + formal supervisory levels |
| Organizational position | hierarchical position | supervisory authority over others |
| Self-direction | substantive complexity | task demands for thought/judgment |
| Self-direction | closeness of supervision | supervisory restriction/discretion |
| Self-direction | routinization | repetitive/predictable task organization |
| Job pressure | time pressure | respondent-reported frequency |
| Job pressure | heaviness | analyst appraisal from work-with-things description |
| Job pressure | dirtiness | respondent report |
| Job pressure | hours worked | average work week |
| Risk/reward | responsibility outside control | perceived likelihood |
| Risk/reward | job/business loss risk | perceived likelihood |
| Risk/reward | job protections | security/sick leave etc. additive index |
| Risk/reward | job income | reported income |

**M6 rule:** these conditions must remain typed. A scalar “job quality” would erase mechanisms that the book shows have different psychological consequences.

## 15. Education

**Role:** antecedent of occupational position/self-direction and direct predictor of earlier psychological functioning; in chapter 7 education has few defensible direct effects on *change* in psychological functioning once prior functioning is controlled, except parental values.

**Identification caveat:** the longitudinal models treat education as unidirectional because most men had completed school before baseline; the authors explicitly state that earlier psychological functioning must also have affected educational attainment.

**Negative ceiling:** education is not a pure exogenous cause and cannot be treated as a psychological prior.

## 16. Job income

**Role:** stratification indicator and one of the chapter 6 extrinsic rewards. It has some independent effects but is not the central mechanism behind the complexity/self-direction findings.

**Important distinction:** income as resource/reward and substantive complexity as recurrent activity demand are causally different. Rawlsing must not collapse them into “SES.”

## 17. Psychological targets: keep disaggregated

### Ideational/intellectual flexibility

Measured from actual performance in interview-based cognitive tasks; authors interpret it as current intellectual functioning rather than innate capacity. It is highly stable but still shows longitudinal relationship with complexity.

### Parental valuation of self-direction

Preference for self-direction versus conformity to external authority in children. Not identical to respondent's own self-directedness.

### Valuation of self-direction for oneself

A separate value construct. Reciprocal effects differ from parental values.

### Self-directedness of orientation

Second-order orientation concerning personal responsibility/agency and whether the social world is seen as allowing self-direction. It is distinct from cognitive flexibility and from job self-direction.

### Authoritarian-conservatism / idea-conformity / moral standards / trustfulness / fatalism / self-confidence / self-deprecation / anxiety

First-order components with heterogeneous path patterns. They cannot be collapsed into one personality score without loss.

### Distress

A separate dimension of discomfort/pain/well-being, with different work-condition predictors and weaker cross-national generality than the core self-direction/flexibility findings.

### Alienation

Alternative orientation construct overlapping some items with self-directedness/distress; useful but not identical.

### Leisure-time intellectuality

Reported nonwork activity pattern, not an intrapsychic trait. It is especially important as evidence of work-experience generalization into actual behavior.

## 18. Occupation-title court

### Evidence

1. Detailed task interview follows occupational title rather than deriving content from title (ch. 1 pp. 23-26).
2. Substantive complexity is measured from actual task description/time allocation (chs. 5-6).
3. Appendix B classifies activity demands, not occupational prestige.
4. Chapter 12 states occupation-level DOT proxies are only approximations and seriously attenuate relationships (p. 289 n.5).
5. Chapter 7 shows occupational status loses much apparent psychological force when concrete self-direction conditions are modeled.

### Verdict

`PASS_INVARIANT__OCCUPATION_TITLE_IS_NOT_WORK_CONTENT`.

Proposed Rawlsing invariant:

```text
OCCUPATION/OCCUPATIONAL_STATUS MAY QUALIFY A SEARCH OR PRIOR
FOR POSSIBLE TASK CONDITIONS,
BUT MAY NOT ITSELF instantiate ACTOR-SPECIFIC
SUBSTANTIVE_COMPLEXITY, SUPERVISION, ROUTINIZATION,
EXERCISED_CONTROL, OR RECURRENT_ACTIVITY.
```

## 19. Measurement-model court

The book's latent constructs are valuable for measurement error and covariance structure. They do **not** license ontology by factor name.

```text
LATENT_FACTOR != CAUSAL_MECHANISM
FACTOR_LOADING != REALIZATION_LAW
COMPOSITE_SELF_DIRECTION != EXERCISED_CONTROL_HISTORY
```

Rawlsing should retain first-order provenance whenever using a normalized mechanism family.
