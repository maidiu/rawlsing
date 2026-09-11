# SDTF R4 S1 — SCHEMA SCENARIO COURT R1

STATUS: `PASS__MANDATORY_SCENARIOS_DEFEATED_WITHOUT_SCHEMA_WIDENING`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

This court tests whether the four-record/three-block S1 contract can represent the required seam distinctions without inventing psychology, event laundering, world-writing, D2/D3/D4 or P6.

---

## S1 — eligible but never applies

Facts:

- a competent rule and admitted position establish eligibility;
- the actor never submits/enters the gate.

Required records:

```text
RULE_APPLICATION_RECORD -> qualification satisfied
OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD
  status = CONSTITUTIVELY_TRUE or QUALIFIED_ONLY, according to exact rule semantics
  consequence = eligibility / route availability
  temporal form = CONDITION or DIRECTED_RELATION as appropriate
```

Forbidden:

```text
APPLIED
GATE_ENCOUNTER
EVALUATED
APPROVED
RECEIVED
```

Verdict: `PASS__ELIGIBILITY_DOES_NOT_CREATE_APPLICATION_OR_RECEIPT`.

---

## S2 — entitled but never receives

Facts:

- entitlement is constitutively valid;
- no competent transfer/receipt witness exists.

Lawful outputs:

```text
ENTITLEMENT = CONSTITUTIVELY_TRUE
RECEIPT = NOT_PROVEN_REALIZED / UNKNOWN
```

No missing payment record may become proved nonreceipt unless exact negative authority exists.

Verdict: `PASS__P1_ENTITLEMENT_NE_RECEIPT`.

---

## S3 — supervisor title without authority

Facts:

- actor carries title `supervisor`;
- no competent position/source fact establishes sanction/command/control scope.

The title may be source metadata or lookup index. It cannot satisfy `POSITION_REF` for a P2 authority rule.

Outcome:

```text
RULE_APPLICATION -> FAIL_CLOSED
NO P2 AUTHORITY FACT AUTHORED
```

Verdict: `PASS__TITLE_NE_RELATIONAL_POWER`.

---

## S4 — authority exists but no current exercise

Facts:

- operative source-owned relation establishes authority scope;
- no current exercise/command/performance witness exists.

Lawful:

```text
AUTHORITY_SCOPE = CONSTITUTIVELY_TRUE or ACTIVE
EXERCISE_OF_AUTHORITY = NOT_PROVEN_REALIZED
```

The operative authority state may be the type-compatible witness for authority existence. It does not prove an exercise occurrence.

Verdict: `PASS__P2_SCOPE_NE_EXERCISE`.

---

## S5 — scheduled activity never performed

Facts:

- P3 schedule is current;
- no participation/performance witness exists.

Lawful:

```text
SCHEDULE = CONSTITUTIVELY_TRUE / ACTIVE CONDITION
PERFORMANCE = NOT_PROVEN_REALIZED
```

Forbidden: turning a schedule into attendance or performed task.

Verdict: `PASS__P3_SCHEDULE_NE_ACTIVITY_REALIZATION`.

---

## S6 — recurrent activity witnessed last year but not current

Facts:

- old observation establishes one or more prior performances;
- rule's recurrence witness schema requires current/fresh coverage;
- no current coverage exists.

Lawful:

```text
HISTORICAL_ACTIVITY = valid historical evidence
CURRENT_RECURRENT_ACTIVITY = NOT_PROVEN_REALIZED / UNKNOWN
```

The old witness remains provenance but is not current support.

Verdict: `PASS__RECURRENCE_REQUIRES_FRESHNESS_AND_COVERAGE`.

---

## S7 — active relation terminated by later source

Facts:

- earlier source establishes active relation;
- later competent source terminates it.

The witness lifecycle marks the earlier witness superseded/terminated for current support. The prior fact remains historical.

Lawful:

```text
RELATION_PRIOR_INTERVAL = true
RELATION_CURRENT = terminated / noncurrent
```

If a negative current assertion `relation absent` is authored, it must rest on the explicit competent termination/negative witness, not merely expiry.

Verdict: `PASS__LATER_SOURCE_DEFEATS_CURRENTNESS_WITHOUT_ERASING_HISTORY`.

---

## S8 — network tie without information transfer

Facts:

- P5 tie/channel exists;
- no delivery/contact witness exists.

Lawful:

```text
TIE_OR_CHANNEL = CONSTITUTIVELY_TRUE / ACTIVE
INFORMATION_TRANSFER = NOT_PROVEN_REALIZED
```

Verdict: `PASS__TIE_NE_CHANNEL_USE_NE_TRANSFER`.

---

## S9 — support transfer without perceived support

Facts:

- competent external witness establishes support transfer;
- no claim is made about subjective perception.

Lawful D1' fact:

```text
SUPPORT_TRANSFER = REALIZED
```

Forbidden D1' outputs:

```text
PERCEIVED_SUPPORT
PSYCHOLOGICAL_BENEFIT
MASTERY_CHANGE
DISTRESS_REDUCTION
```

Verdict: `PASS__OBJECTIVE_PROVISION_STOPS_BEFORE_V3_APPRAISAL`.

---

## S10 — class label with different actual relations

Facts:

- actors A and B share a class label;
- their actual resource/control/activity/gate/channel relations differ.

The label cannot be used as `POSITION_REF` or mechanism rule.

D1' must derive from each actor's actual source-owned P1-P5 relevant relations.

Verdict: `PASS__CLASS_LABEL_NE_CONSEQUENCE`.

---

## S11 — hidden classification never shown to gatekeeper

Facts:

- classification exists somewhere in source data;
- it is not presented/recognized in the governed P4 process.

The P4 ladder breaks before evaluation/treatment. No treatment effect may be authored from the hidden classification.

Verdict: `PASS__HIDDEN_ATTRIBUTE_NE_GATE_TREATMENT`.

---

## S12 — gate treatment realized

Facts:

- exact P4 rule is current;
- actor/binding/applicability satisfied;
- gate encounter and relevant presented record are externally witnessed;
- competent decision/treatment witness exists and covers the asserted time.

Lawful:

```text
GATE_TREATMENT = REALIZED
```

Downstream resource/authority/activity/channel consequences still require their own exact rules/evidence if separately asserted.

Verdict: `PASS__P4_REALIZATION_REQUIRES_EXACT_GATE_WITNESS`.

---

## S13 — actor action ignored by institution

Facts:

- actor externalizes an action;
- institution produces no competent response changing the relevant external rule/state.

The action occurrence may become an admitted external fact. It does not itself mutate institution/structure.

Lawful:

```text
EXTERNAL_ACTION_OCCURRENCE = admitted if competent
INSTITUTIONAL_CHANGE = NOT AUTHORIZED / NO NEW FACT
```

D1' reruns only if a competent new external fact exists.

Verdict: `PASS__NO_DIRECT_PERSON_TO_WORLD_WRITE`.

---

## S14 — persistent objective condition with no event

Facts:

- source/state authority supports an ongoing resource constraint or obligation relation;
- no discrete occurrence is needed to make it true.

Lawful consequence:

```text
TEMPORAL_FORM = CONDITION or DIRECTED_RELATION
STATUS = CONSTITUTIVELY_TRUE or ACTIVE
```

Downstream:

```text
D1'_FACT_EXISTS
V3_NON_EVENT_INGRESS = OBL062_OPEN
```

Forbidden: fabricate an event solely to reach CAN-008.

Verdict: `PASS__NON_EVENT_FACT_SURVIVES_WITH_INGRESS_UNPROVED`.

---

## S15 — missing evidence

Facts:

- required positive witness absent.

Lawful result:

```text
UNKNOWN
or
NOT_PROVEN_REALIZED
```

Forbidden:

```text
NEGATIVE FACT
DENIAL
NONOCCURRENCE
ABSENCE
```

unless separately supported.

Verdict: `PASS__MISSING_EVIDENCE_NE_NEGATIVE_TRUTH`.

---

## S16 — explicit denial

Facts:

- competent institution/source records a denial decision or exact negative state.

The unified witness record carries:

```text
WITNESS_POLARITY = NEGATIVE
WITNESS_TYPE = explicit denial / negative decision
COMPETENT_SOURCE_OR_OWNER = exact gate authority
EVENT_TIME or VALID_INTERVAL = exact
```

A negative P4 consequence may then be authored according to the rule.

Verdict: `PASS__NEGATIVE_FACT_HAS_POSITIVE_PROVENANCE_OF_NEGATION`.

---

## S17 — source rule still current while realization witness has expired

Facts:

- rule remains current;
- last positive realization witness no longer covers the asserted current interval.

The currentness firewall requires:

```text
CURRENT(rule,t) = true
CURRENT(witness,t) = false
CURRENT(realized_fact,t) = false / not proved
```

Lawful consequence status:

```text
NOT_PROVEN_REALIZED or UNKNOWN
```

The expired witness does not create a negative fact.

Verdict: `PASS__RULE_CURRENTNESS_CANNOT_EXTEND_WITNESS_OR_FACT_CURRENTNESS`.

---

## S18 — formal obligation current, performance absent

Additional regression from the R3 courts.

A competent rule/relation can establish an active duty without proving performance.

```text
OBLIGATION = CONSTITUTIVELY_TRUE / ACTIVE
PERFORMANCE = NOT_PROVEN_REALIZED
```

Verdict: `PASS__DEONTIC_FACT_NE_PERFORMANCE`.

---

## S19 — population denial rate applied to individual

Facts:

- empirical source reports a group-level denial rate;
- no actor-specific gate decision exists.

The group statistic is evidence/source context only. It cannot be direct antecedent authority for an actor's realized denial outcome unless a separately governed stochastic world/institution owner samples/issues an actor-specific result.

Verdict: `PASS__POPULATION_RATE_NE_ACTOR_OUTCOME`.

---

## S20 — old positive witness plus later missing data

Facts:

- old witness supported prior positive state;
- present source is merely silent, not a competent termination source.

Lawful:

```text
PRIOR FACT = historical true
CURRENT FACT = UNKNOWN / NOT_PROVEN under freshness rule
NEGATIVE CURRENT FACT = not authorized
```

Verdict: `PASS__SILENCE_DOES_NOT_TERMINATE_BY ITSELF`.

---

## S21 — same-time derivation loop attempt

Facts:

```text
FACT_A_t -> FACT_B_t
FACT_B_t -> FACT_A_t
```

No competent fixed-point owner exists.

The companion contract requires direct antecedent provenance and forbids authority-by-cycle. A future runtime must detect/prevent such cycles at G2.

Verdict: `PASS_AT_NORMATIVE_GRAIN__CYCLE_CANNOT_SUPPLY_MISSING_AUTHORITY`; algorithmic enforcement is `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

---

## S22 — counterfactual promotion

Facts:

- model asks what objective consequences would follow if actor entered a hypothetical promoted position;
- promotion is not a current admitted fact.

S1 does not authorize current actor facts from hypothetical bindings. If future simulation support exists, its outputs must remain explicitly noncurrent/projected outside current biography until competent world/position facts are admitted.

Verdict: `PASS__COUNTERFACTUAL_NE_CURRENT_HISTORY`; representation is future simulation grain.

---

## S23 — physical outage changes service capacity

Facts:

- competent material/world source establishes an outage;
- governed rule maps outage to service-capacity consequence;
- further actor-relative access consequence requires exact binding and rule.

The seam permits objective material/world facts as antecedents when the social mechanism rule lawfully consumes them.

Verdict: `PASS__MATERIAL_WORLD_INPUT_NE_ENVIRONMENTAL_SHORTCUT`.

---

## S24 — occupation self-direction score used as actual task state

Facts:

- source contains a construct/score;
- runtime rule needs first-order task/control facts.

Without competent source/measurement semantic binding, the score cannot stand in for actual task/control state.

Verdict: `PASS_WITH_G6_DEPENDENCY__SOURCE_CONSTRUCT_NE_RUNTIME_FACT`.

---

## S25 — D1' semantic adoption with empty rule registry

Facts:

- assume HQ later adopts D1';
- no mechanism rules have separately become current.

Correct output:

```text
CONSTITUTION CURRENT
RULE SET = EMPTY / PARTIAL
NEW APPLICATIONS = NONE
NEW ACTOR FACTS = NONE
```

Verdict: `PASS__SEMANTIC_ADOPTION_AUTORIZES_ZERO_RULES_AND_ZERO_FACTS`.

---

## Court summary

All mandatory user scenarios and additional R3 regression scenarios are representable with the four-record/three-block schema.

No scenario requires:

```text
D2
D3
D4
P6
A PSYCHOLOGY RECORD
A GENERIC WORLD-WRITE RECORD
A FAKE EVENT
A SEPARATE NEGATIVE-WITNESS FAMILY
A SEPARATE BINDING RECORD
A SEPARATE TEMPORAL OWNER
```

The only remaining dependencies are already externalized by R4:

- G1 rule admission/currentness;
- G2 hosting/replay/cycle enforcement;
- G3 concrete witness interfaces;
- G4/OBL062 non-event V3 ingress;
- G5 competent reciprocal world response;
- G6 source/measurement/calibration/causal-use binding.

---

## Scenario terminal

`PASS__S1_R4_SCHEMA_SCENARIO_COURT__MANDATORY_CASES_AND_R3_REGRESSIONS_PASS__NO_TOPOLOGY_WIDENING__OBL062_AND_G1_G6_REMAIN_EXTERNAL`.
