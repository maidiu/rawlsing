# M2 PALESTINE — RAWLSING MAPPING R1

STATUS: `SOURCE_TO_ARCHITECTURE_CROSSWALK_COMPLETE`

SCOPE: This mapping is relative to the frozen pre-review candidate at `9cf100a101e92891e2b4d0af0e308d27f7015a6b`. M2 is a source-augmentation lane and does not authorize project-current implementation or adoption.

## Mapping rule

The source is mined for concrete causal functions. Source political/theoretical vocabulary is not converted into Rawlsing ontology. Existing candidate families and implementation grains are reused unless the volume proves a distinct causal operation.

| SOURCE MECHANISM | RAWLSING FAMILY / SURFACE | D1/D2/D3 | FROZEN IMPLEMENTATION GRAIN | DISPOSITION | REQUIRED SPECIFICITY |
|---|---|---|---|---|---|
| work/medical/water/reproductive permit | `INSTITUTIONAL_GATE` | D1 | G1/G4 | `REUSE` | rule != applicability != application != treatment != access |
| classification used by explicit gate | `CLASSIFICATION_TO_REALIZED_TREATMENT` | D1 | G1/G4 | `REUSE` | demographic/religious/age field lawful only through exact rule |
| road/checkpoint/license route | `INSTITUTIONAL_GATE + TIME_ALLOCATION` | D1+D2 | G1/G2/G4 | `REUSE/GENERALIZE TESTS` | route eligibility, wait, delay, open interval, arrival |
| electricity/service windows | `TIME_ALLOCATION + ACTIVITY_ORGANIZATION` | D1+D2 | G1/G2 | `GENERALIZE TESTS` | service interval -> appliance/task feasibility |
| school closure / teacher route | `INSTITUTIONAL_GATE + ACTIVITY_ORGANIZATION` | D1+D2 | G1/G2/G4 | `REUSE` | actual student/teacher/school binding and activity history |
| infrastructure/service-capacity loss | `RESOURCE_DEPENDENCY + CROSS_DOMAIN_PROPAGATION` | D1+D2 | G1/G2/G4 | `GENERALIZE` | infrastructure -> service capacity -> actor access/substitution |
| linked commuter absence -> spouse work | `LINKED_LIFE_TRANSMISSION + HOUSEHOLD_CARE_DEPENDENCY + ROLE_OBLIGATION + TIME_ALLOCATION` | D1+D2 | **G5 + G2** | **`GENERALIZE`** | contribution/presence withdrawal -> persisting need/task -> substitute allocation -> focal ecology |
| family/contact reachability | `COUNTERPART_FORMATION + LINKED_LIFE_TRANSMISSION` | D1+D2 | G1/G2/G5 | `REUSE` | relation label != contact; route + actual contact history |
| displacement/co-residence | `TRANSITION_REBINDING + COUNTERPART_FORMATION` | D1+D2 | G3/G5 | `REUSE/GENERALIZE` | residence transition -> exact new household/counterpart/task facts |
| authority transfer | `AUTHORITY_CONTROL_SANCTION + TRANSITION_REBINDING` | D1+D2 | G3 | `GENERALIZE` | partial authority transfer must rebind only transferred powers |
| repeated destruction/rebuilding | `RESOURCE_DEPENDENCY + CUMULATIVE_ITERATIVE_FEEDBACK` | D1+D2 | G2/G7 | `REUSE/GENERALIZE` | loss -> repair expenditure/debt -> typed resource state_t+1 |
| land route restriction -> noncultivation -> later status | `INSTITUTIONAL_GATE + ACTIVITY_ORGANIZATION + CUMULATIVE_ITERATIVE_FEEDBACK` | D1+D2 | G2/G7 | `GENERALIZE TESTS` | activity history becomes input to later exact rule/gate |
| organization-specific support/care/logistics roles | `ROLE_OBLIGATION + ACTIVITY_ORGANIZATION` | D1+D2 | G1/G2 | `REUSE` | organization/assignment -> task; no gender shortcut |
| messenger/information transfer | `NETWORK_INFORMATION_SUPPORT + COUNTERPART_FORMATION` | D1+D2 | G1/G4/G5 | `REUSE` | channel != transfer != belief/use |
| local cultivation/resource creation | `COLLECTIVE_STRUCTURAL_FEEDBACK + RESOURCE_DEPENDENCY` | D3 then D1 | **G6** | `GENERALIZE` | explicit coordination/resources -> actual produced resource; no rule change required |
| popular/makeshift schools | `COLLECTIVE_STRUCTURAL_FEEDBACK + ACTIVITY_ORGANIZATION + COUNTERPART_FORMATION` | D3+D1+D2 | **G6 + G1/G2** | `GENERALIZE` | alternative institution/practice, suppression, partial persistence |
| teacher strike -> firing/transfer | `COLLECTIVE_STRUCTURAL_FEEDBACK + AUTHORITY_CONTROL_SANCTION` | D3 | G6 | `GENERALIZE` | suppressive feedback and failed objective are first-class |
| temporary market / alternative goods route | `COLLECTIVE_STRUCTURAL_FEEDBACK + NETWORK_INFORMATION_SUPPORT` | D3 then D1+D2 | G6 | `GENERALIZE` | temporary resource/network creation while governing rule persists |
| sperm-smuggling/IVF route | `INSTITUTIONAL_GATE + COUNTERPART_FORMATION + COLLECTIVE/RECIPROCAL_SOCIAL_WORLD_UPDATE` | D1+D2+D3 | G1/G2/G6 | `GENERALIZE` | route circumvention + service counterpart + separate recognition gate |
| Romanian oocyte market chain | `INSTITUTIONAL_GATE + ACTIVITY_ORGANIZATION + NETWORK/COUNTERPART + GATED_RECIPROCAL_SELECTION` | D1+D2(+D3 organizational response) | G1/G3/G4/G6 | `GENERALIZE` | state -> clinic -> recruiter -> provider -> recipient explicit stages |
| posthumous retrieval eligibility | `INSTITUTIONAL_GATE + TRANSITION_REBINDING + COUNTERPART_FORMATION` | D1+D2 | G1/G3/G4 | `REUSE` | relation/eligibility -> request -> retrieval -> later procedure separately |
| care substitution after provider loss | `HOUSEHOLD_CARE_DEPENDENCY + LINKED_LIFE_TRANSMISSION + CROSS_DOMAIN_PROPAGATION` | D1+D2 | G1/G5 | `GENERALIZE` | need persists + formal route loss + actual substitute actor/task |
| actor meaning/fear/hope/commitment/refusal | existing V3 receiving surfaces only where competent | downstream of D1/D2/D3 | G8 conformance | `DEFER/REUSE V3` | no second psychology; participant-specific evidence only |
| generic “social reproduction” | none | none | none | `REJECT AS OPERATOR` | decompose into typed mechanisms |
| generic “resistance” | none | none | none | `REJECT AS OPERATOR` | action + organization + external response + realized result |
| generic “space” | none | none | none | `REJECT AS VARIABLE` | route/boundary/wait/counterpart/resource location |
| generic “cumulative disadvantage” | none | none | none | `REJECT` | typed iterative update only |
| turning-point carrier | existing derived trajectory predicate | D2/history | existing/frozen candidate law | `REJECT NEW CARRIER` | source provides transitions/trajectories, not need for new carrier |

---

# D1 mapping consequences

D1 already provides the correct top-level derivation interface. M2 adds two high-value conformance requirements.

## D1-M2-1 — linked-actor contribution withdrawal and obligation transfer

The frozen G5 form:

```text
source context/person change
--[resource | time | obligation | support | relation | gate linkage]-->
focal actor ecology update
```

is directionally correct but should be made mechanically explicit for Repo's strongest household evidence:

```text
SOURCE_ACTOR_CONSTRAINT
-> SOURCE_ACTOR_PRESENCE/CONTRIBUTION_WITHDRAWAL
+ PERSISTING HOUSEHOLD NEED/TASK
+ EXACT HOUSEHOLD/DEPENDENCY/OBLIGATION RELATION
-> SUBSTITUTE ACTOR ALLOCATION/PERFORMANCE
-> FOCAL ACTOR TIME/ACTIVITY/OBLIGATION UPDATE
```

**Mapping disposition** — `GENERALIZE D1/G5`, not new top-level family.

## D1-M2-2 — service capacity and counterpart availability are intermediate social facts

The source repeatedly shows that legal permission does not ensure a feasible service. D1 chains should preserve:

```text
FORMAL RULE
-> ELIGIBILITY
-> ACTUAL PROVIDER/DONOR/FACILITY/ROUTE CAPACITY
-> GATE TREATMENT
-> REALIZED SERVICE/ACTIVITY
```

This matters for medical permits, fertility treatment, school/teacher access, and damaged health infrastructure.

**Mapping disposition** — `GENERALIZE/TEST existing D1 families`; no new `SERVICE_MODULE`.

---

# D2 mapping consequences

D2 is strongly supported. M2 turns several semantic requirements into mandatory conformance cases:

```text
ACTIVE_INTERVAL                    continuing closure/blockade/imprisonment/service condition
VALIDITY_INTERVAL                  permit/authorization period
WAIT_DURATION                      checkpoint/medical/access queue
DEADLINE                           return-before-expiry; specimen viability
UNCERTAIN_DELAY                    checkpoint/road interruption
RECURRENT_ACTIVITY_IDENTITY        daily commute, care, provisioning, repair
SCHEDULE_COUPLING                  linked spouses/household actors
INTERRUPTION                       school/work/service episode
PARTIAL_REBINDING                  authority transfer / limited reopening
TRANSITION                         displacement / permit cancellation / service restoration
TRAJECTORY                         ordered work/school/resource/contact history
CUMULATIVE_TYPED_UPDATE            loss->repair/debt; noncultivation->later status
```

No new carrier follows from the source. The frozen G2/G3/G7 reuse-first plan remains appropriate.

**Mapping disposition** — `REUSE + GENERALIZE TEST SUITE`.

---

# D3 mapping consequences

The frozen G6 transaction is retained:

```text
actor/collective realized action
-> external counterpart/institution/gate response
-> admitted change in position/relation/rule/resource/network
-> later actor binding/ecology update
```

M2 requires the result to preserve the **exact updated level** and not silently promote every action to rule/structure change.

Required outcome classifications:

```text
RULE_OR_POLICY_CHANGE
POSITION_OR_RELATION_CHANGE
RESOURCE_CREATION_OR_DESTRUCTION
NETWORK_OR_COUNTERPART_CREATION
ALTERNATIVE_INSTITUTION_OR_PRACTICE_CREATION
ROUTE_CREATION_OR_CIRCUMVENTION
PARTIAL_SUCCESS
TEMPORARY_SUCCESS
SUPPRESSION_OR_SANCTION
EXTERNAL_NONRECOGNITION
NO_RELEVANT_SOCIAL_WORLD_CHANGE
```

Examples:

```text
MAKESHIFT SCHOOL != CLOSURE RULE REPEAL
TEMPORARY MARKET != PASS REGIME ABOLITION
SPERM-SMUGGLING ROUTE != PRISON RULE CHANGE
STRIKE -> FIRING can be D3 even if grievance persists
```

**Mapping disposition** — `GENERALIZE D3/G6 outcome grammar`, not D4.

---

# Temporal-form mapping

| TEMPORAL FORM | M2 SOURCE COVERAGE | RAWLSING MAPPING | DISPOSITION |
|---|---|---|---|
| `EVENT` | raid, arrest, gate decision, destruction, birth/procedure | existing discrete occurrence/OEE surfaces where competent | `REUSE`; no new event carrier |
| `CONDITION` | imprisonment, service deprivation, route restriction, displacement, closure | G2 active interval / existing state-binding generalization | `GENERALIZE EXISTING` |
| `RELATION` | household dependency, employment, authority, donor/recipient, prisoner/spouse | directed persistent relation/binding | `GENERALIZE EXISTING` |
| `RECURRENT ACTIVITY/PRACTICE` | commute, care, provisioning, teaching, repair, messenger work | G2 recurrence + CAN-011/history compatibility | `GENERALIZE EXISTING` |
| `TRANSITION` | permit cancellation/reopening, authority transfer, displacement, service loss/restoration | G3 transition rebinding | `GENERALIZE EXISTING` |
| `TRAJECTORY` | schooling/work/resource/contact histories | ordered typed history | `REUSE/GENERALIZE` |
| `TURNING POINT` | source contains potentially consequential transitions but no need for distinct carrier | derived predicate after sustained redirection | `REJECT NEW CARRIER` |
| `CUMULATIVE PROCESS` | rebuilding/debt; activity suppression feeding later rule | G7 typed iteration | `GENERALIZE COMPOSITION` |

---

# V3/psychology boundary mapping

M2 does not alter the frozen candidate's ingress boundary.

Source-grounded objective outputs can include:

```text
REALIZED GATE DENIAL/DELAY
ACTIVE RESOURCE LOSS
ACTIVE HOUSEHOLD OBLIGATION
RECURRENT CARE/WORK/SCHOOL HISTORY
ACTUAL INFORMATION/SUPPORT TRANSFER
ACTUAL CONTACT/SEPARATION
EXTERNAL SANCTION
ALTERNATIVE ROUTE/RESOURCE/NETWORK
```

But the seam does not mint:

```text
MOTIVE
BELIEF
TRAIT
TRAUMA
IDENTITY
MEMORY
LEARNING
COMMITMENT
HOPE
RESILIENCE
DURABLE DEVELOPMENT
```

Participant-reported fear, commitment, refusal, worry, fatigue, humiliation, hope, or strategy may be admitted as source evidence only through an exact downstream V3 owner and with the chapter's evidence ceiling. Group membership cannot substitute.

---

# Reuse / generalize / missing / reject summary

## REUSE

- D1 top-level typed derivation contract.
- D2 top-level non-event temporal semantics.
- D3 top-level external-response/provenance transaction.
- institutional gate, resource/dependency, role/obligation, activity, counterpart, network/information, classification-to-treatment, transition, cumulative typed update families.
- existing downstream V3 boundary.

## GENERALIZE

1. D1/G5 linked-person propagation to explicit `contribution withdrawal -> persisting task/need -> substitute allocation -> focal ecology`.
2. D1 multi-stage service-capacity/counterpart chains so formal eligibility cannot equal actual service.
3. D2 conformance coverage for wait/deadline, linked schedule coupling, partial rebinding, recurrent identity, typed cumulation.
4. D3/G6 exact result taxonomy and update level, including temporary/partial/suppressive/no-change outcomes and alternative route/resource/network/institution creation.

## MISSING

`NO NEW TOP-LEVEL CONNECTIVE FUNCTION PROVED MISSING BY M2.`

Relative to the frozen candidate, the linked-life and D3 outcome semantics are **undergeneralized**, not top-level missing. Because the candidate itself was not yet adopted at the frozen target, M2 does not claim these are project-current production capabilities.

## REJECT

- undifferentiated `SOCIAL_REPRODUCTION` operator;
- generic `SPACE` or `TIME_GRABBING` state as architecture;
- group/category -> work/care/psychology shortcuts;
- infrastructure -> psychology shortcut;
- action/resistance -> structure/success shortcut;
- generic cumulative-disadvantage scalar;
- separate D4 solely for space/time/access;
- collective psychological subject.

## DEFER

- broad political-intent claims not required by the narrower mechanisms;
- general developmental/psychological claims lacking direct longitudinal/developmental support;
- source-theoretical labels whose empirical content cannot be separated at the required causal grain.

---

# Smallest architectural consequence actually licensed

```text
NO NEW TOP-LEVEL D4.
NO NEW SOCIAL_REPRODUCTION OPERATOR.

NARROW THE POST-REVIEW DELTA TO:
  A. D1/G5 linked-actor contribution-withdrawal/task-transfer rule specificity;
  B. D2 conformance tests for schedule coupling/wait/deadline/partial rebinding/typed cumulation;
  C. D3/G6 outcome taxonomy preserving exact update level and failure/suppression/temporary alternatives.
```

These are source-licensed generalizations/tests to be considered by Vozhd/HQ after the independent post-review process, not production authorization.

TERMINAL:

`M2_RAWLSING_MAPPING_COMPLETE__REUSE_D1_D2_D3__GENERALIZE_G5_G6_AND_TEMPORAL_CONFORMANCE__NO_D4`.