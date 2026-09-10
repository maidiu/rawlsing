# T3_NEGATIVE_CEILINGS_AND_OPEN_QUESTIONS_R1

STATUS: `T3_NEGATIVE_CEILINGS_FROZEN__OPEN_QUESTIONS_NONBLOCKING`

## 1. Absolute semantic ceilings

The T3 lane rejects every shortcut below regardless of whether a population-level association points in the expected direction.

```text
CLASS != PERSONALITY
CLASS != BELIEF
CLASS != DISTRESS
CLASS != MOTIVATION

PROPERTY POSITION != ACTUAL MATERIAL DEPRIVATION
WAGE-LABOUR POSSIBILITY != ACTUAL EMPLOYMENT
EMPLOYMENT != ACTUAL JOB CONDITIONS
OCCUPATION LABEL != TASK / AUTONOMY / COMPLEXITY / PACE

MANAGER TITLE != ACTUAL AUTHORITY
SUPERVISOR TITLE != SANCTION POWER
FORMAL RIGHT != ACCESS / USE / ENFORCEMENT / OUTCOME
FORMAL OPPORTUNITY != ENCOUNTER / PERCEPTION / USE
CREDENTIAL != COMPETENCE
CREDENTIAL != LABOUR-MARKET POWER WITHOUT SCARCITY / RECOGNITION / DEMAND

GENDER != CAREGIVER
HOUSEHOLD MEMBERSHIP != CARE OBLIGATION
SOCIAL REPRODUCTION NEED != ONE FAMILY FORM
PAID EMPLOYMENT != HOUSEHOLD CARE DIVISION
CARE CRISIS != ACTOR-SPECIFIC CARE BURDEN

HEGEMONY != CONSENT
WORK GAME PARTICIPATION != DURABLE IDEOLOGICAL ENDORSEMENT
RESISTANCE != EMANCIPATION
RESISTANCE != REPRODUCTION
WORKING-CLASS ORIGIN != COUNTER-SCHOOL CULTURE

STRUCTURAL POSSIBILITY != REALIZED EXPERIENCE
REALIZED EXPERIENCE != ACTOR UPTAKE
ACTOR UPTAKE != DURABLE CHANGE
DURABLE CHANGE != DIRECT DEMOGRAPHIC PRIOR
GROUP ASSOCIATION != INDIVIDUAL CAUSAL HISTORY
```

## 2. Source-specific negative ceilings

### Marx

- Property separation establishes a relation of material dependence only when the actor actually lacks alternative means/resources and confronts a relevant labour market.
- The struggle over the working day demonstrates that legal equality and market exchange do not themselves fix actual time use, but it does not imply identical hours or responses across workers.
- Machinery and factory organization do not license technological determinism: technical form, capitalist use, law, organization and worker action must remain separable.
- Reproduction of the capital relation is not reproduction of a fixed individual personality.

### Braverman

- Do not encode a universal deskilling theorem.
- Do not infer task fragmentation, low discretion or knowledge exclusion from occupation/industry labels.
- Separation of conception/execution is a work-organization mechanism, not a direct cognitive-development law.
- Any capacity effect requires actual repeated practice/nonpractice and lawful V3 development.

### Burawoy

- “Consent” must not be read as user/actor true internal state from observed cooperation.
- Internal labour markets both enable and constrain; seniority benefits do not prove loyalty.
- Grievance/bargaining machinery can constrain managerial discretion while stabilizing the employment relation; neither direction may erase the other.
- A factory ethnography does not establish a universal regime of production.

### Willis

- No universal working-class culture may be inferred from a narrow 1970s male English sample.
- Peer resistance is actor activity, not passive class socialization, and can have nonmodal outcomes.
- Class origin cannot stand in for exact school, peer, credential, household and labour-market mechanisms.
- “Self-damnation” is retained only as a warning that active choices under structured possibilities may close later routes; it is not an actor-blaming law.

### Wright

- “Class location” must be decomposed into actual property, authority and skill/credential relations before causal use.
- Manager/supervisor labels cannot substitute for measured delegated authority.
- Scarce skill/credential assets produce power only under real scarcity, institutional recognition and demand.
- Authority or class location does not directly determine consciousness or personality.

### Vogel

- The requirement to maintain/replace bearers of labour-power does not imply an invariant nuclear family, a female caregiver, or a functionally guaranteed social arrangement.
- The household is one historically variable site among others.
- Abstract reproduction requirements cannot be applied to an actor until concrete relations and obligations are bound.

### Fraser / ILO care evidence

- “Financialized capitalism,” “two-earner household,” or population gender differences are macro descriptions, not actor exposures.
- Cross-national time-use averages cannot become demographic priors.
- Care burden, marketization and migration must be represented through actual policy, wage, household, service and counterpart relations.

## 3. Architecture ceilings

T3 is prohibited from creating:

```text
MARX_OBJECT
BRAVERMAN_DESKILLING_STATE
BURAWOY_CONSENT_STATE
WILLIS_WORKING_CLASS_CULTURE_STATE
WRIGHT_CLASS_PERSONALITY
VOGEL_REPRODUCTION_STATE
FRASER_CARE_CRISIS_STATE
BOURDIEU_HABITUS_OBJECT
GRAMSCI_HEGEMONY_OBJECT
GENERIC_SOCIOLOGY_MODULE
```

No T3 mechanism may seize PRE-V3 authority over actor-independent empirical/structural possibility.

No T3 mechanism may seize V3 authority over actor uptake, motive, memory, relationship, knowledge, practice, tension, personality or attractor movement.

A future implementation may normalize source concepts into typed social relations/functions only if HQ adopts them after cross-lane review.

## 4. Temporal ceilings

```text
CONDITION != EVENT REPEATED ONCE
RELATION != CONTACT EVENT
RECURRENT PRACTICE != SET OF UNRELATED EVENTS
TRANSITION != TURNING POINT
TRAJECTORY != CURRENT POSITION
CUMULATIVE PROCESS != ONE SALIENT EVENT
```

Specific constraints:

1. Wage dependence can persist when no hiring/firing event occurs.
2. Authority can persist between explicit commands.
3. Care obligation can structure time between discrete care episodes.
4. A work practice can matter through repetition without conscious appraisal on every repetition.
5. A promotion is a transition; it becomes a turning point only if the later trajectory is demonstrably redirected.
6. Cumulative load or skill practice requires time-indexed accumulation, not a post-hoc label.

## 5. Agency / reciprocity ceilings

Avoid both determinism and voluntarism.

```text
STRUCTURAL CONSTRAINT != ACTION DETERMINATION
ACTOR CHOICE != UNCONSTRAINED OPTION SET
RESISTANCE != AUTOMATIC STRUCTURAL CHANGE
COLLECTIVE ACTION != GUARANTEED SUCCESS
```

A lawful reciprocal path requires:

```text
ACTUAL ACTOR / COLLECTIVE ACTION
+ ACTUAL TARGET / COUNTERPART / INSTITUTION
+ CAUSAL ROUTE
+ SUFFICIENT EFFICACY / RESPONSE
→ CHANGED LATER RULE / RELATION / POSITION / EXPOSURE
```

## 6. Open questions returned to Vozhd — nonblocking for T3 R1

### OQ-T3-01 — Can existing opportunity/constraint owners losslessly carry persistent relation/condition state?

Exact question: can existing actor-relative opportunity/constraint machinery represent duration-bearing wage dependency, authority, care obligation and time control without converting them to synthetic events?

Why nonblocking: T3 proves the needed semantics; repository lane R and coordinator synthesis decide owner sufficiency.

### OQ-T3-02 — Is a distinct recurrent-activity carrier needed?

Exact question: can repeated task/care/peer practices be represented by existing event history + practice/memory owners while preserving frequency, organization and continuity, or is a typed activity-state carrier required?

Why nonblocking: T3 does not invent a carrier without the repository court.

### OQ-T3-03 — Where should directed social power/dependency edges live?

Exact question: can existing interaction topology / relation machinery encode directed rights, obligations, authority and dependency (`A can sanction B`, `A owes care to B`, `A represents B`) with actor/world/time binding and provenance?

Why nonblocking: source corpus establishes the relation requirement, not owner identity.

### OQ-T3-04 — How is collective action represented without inventing a collective mind?

Exact question: what existing owner can represent coordinated multi-actor action that changes a rule/contract/policy while keeping individual actor states separate?

Why nonblocking: working-day, grievance and care-policy mechanisms make reciprocity mandatory, but T3 need not solve group-agent architecture.

### OQ-T3-05 — What is the minimal type system for actor-relative social ecology outputs?

At minimum T3 requires distinguishable outputs for:

```text
RESOURCE
DEPENDENCY
OBLIGATION
AUTHORITY
RIGHT
SANCTION
TIME_CONTROL
ACTIVITY_FORM
INFORMATION_ACCESS
SKILL_USE_OPPORTUNITY
ELIGIBILITY
INSTITUTIONAL_GATE
MOBILITY_ROUTE
COUNTERPART_RELATION
CARE_RELATION
PERSISTENT_CONDITION
```

Exact question: which are already existing Rawlsing types/owners and which are properties of a generalized relation/opportunity object?

### OQ-T3-06 — What provenance is required for a structural relation→actor ecology derivation?

T3 recommends that every positive transduction retain:

```text
source structural relation/rule identity
actor/position binding
world/phase/time binding
mechanism identity
counterpart/institution identity where applicable
output ecology fact
realization status
negative ceiling
```

Repository lane R should decide which provenance contracts already exist.

### OQ-T3-07 — How should historical regime claims be bounded?

Fraser, Marx, Willis, Braverman and Burawoy all analyze historically specific institutional forms. Rawlsing should require explicit world/time/institution context and prevent a mechanism fitted to one regime from becoming transhistorical by default.

## 7. Exact blocker court

No exact source or irreducible theory contradiction blocks the T3 R1 return.

The open questions above are **integration questions**, not missing-source blockers. The source frontier is sufficient to hand the mechanism corpus to the Vozhd for normalization against T1–T6 and lane R.

Therefore the only lawful T3 terminal is:

`PASS__T3_MECHANISM_CORPUS_READY_FOR_VOZHD_NORMALIZATION`