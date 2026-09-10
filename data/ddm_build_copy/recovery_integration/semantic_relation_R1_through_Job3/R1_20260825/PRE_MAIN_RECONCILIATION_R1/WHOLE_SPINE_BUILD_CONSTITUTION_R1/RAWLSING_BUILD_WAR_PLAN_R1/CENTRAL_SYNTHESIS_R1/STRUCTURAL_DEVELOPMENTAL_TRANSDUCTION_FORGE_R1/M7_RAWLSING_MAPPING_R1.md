# M7_RAWLSING_MAPPING_R1

STATUS: `M7_RAWLSING_MAPPING_COMPLETE_R1`

SOURCE: Kohn & Słomczyński, *Social Structure and Self-Direction* (1990), full supplied source.  
FROZEN SYNTHESIS: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`.

## 0. Mapping rule

This mapping does not import a sociology package, a class psychology, or a self-direction trait prior.

It asks only what exact Rawlsing connective semantics are required to preserve the source's strongest comparative result:

```text
SYSTEM / INSTITUTIONAL CONFIGURATION
-> ACTOR'S EXACT RELATIONAL POSITION
-> CONCRETE WORK/LIFE CONDITION OR RECURRENT ACTIVITY
-> EXISTING V3 RECEIVER IF PSYCHOLOGICAL CONSEQUENCE IS EARNED
```

## 1. Source constructs -> Rawlsing structural inputs

### 1.1 Ownership and production relations

Source constructs:

- employer/self-employed ownership;
- state/cooperative enterprise location;
- centralized productive core versus secondary/support sectors;
- control over labor power.

Rawlsing mapping:

```text
STRUCTURAL_SOURCE_FACTS
+ INSTITUTION / ENTERPRISE REF
+ PROPERTY / OWNERSHIP RULE
+ ACTOR POSITION_BINDING
+ VALID_TIME
```

Possible mechanism families:

- `RESOURCE_DEPENDENCY`;
- `AUTHORITY_CONTROL_SANCTION`;
- `ACTIVITY_ORGANIZATION`.

No direct `CLASS -> ACTOR PSYCHOLOGY` edge.

### 1.2 Hierarchical authority

Source constructs:

- manager;
- first-line supervisor;
- number of subordinate layers;
- direct supervisory span;
- closeness of supervision.

Rawlsing mapping:

```text
INSTITUTIONAL / ORGANIZATIONAL RULE
+ EXACT DIRECTED SUPERVISOR<->WORKER RELATION
+ AUTHORITY_SCOPE
+ ACTOR POSITION_BINDING
-> AUTHORITY/CONTROL APPLICABILITY
-> IF ENACTED: ACTIVE SUPERVISION RELATION / CONDITION
```

Mechanism families:

- `AUTHORITY_CONTROL_SANCTION`;
- `ROLE_OBLIGATION`.

Important firewall:

```text
FORMAL TITLE != ACTUAL SUPERVISION
FORMAL AUTHORITY != ENACTED CONTROL
```

### 1.3 Division of labor and task complexity

Source constructs:

- substantive complexity of work;
- work with data/ideas/people/things;
- task variability/predictability;
- routinization;
- actual use of initiative/judgment.

Rawlsing mapping:

```text
DIVISION_OF_LABOUR / WORKFLOW / TASK_ASSIGNMENT
-> ACTOR-RELATIVE TASK OPPORTUNITY / REQUIREMENT
-> ACTUAL RECURRENT TASK PERFORMANCE
-> RECURRENT_ACTIVITY HISTORY
```

Mechanism family:

- `ACTIVITY_ORGANIZATION`.

Temporal owner requirement:

- D2 condition + recurrent activity, not event spam.

### 1.4 Education / credentialing / occupational allocation

Source constructs:

- educational attainment;
- credentials;
- formal education during occupational career;
- centralized allocation of personnel;
- occupational status.

Rawlsing mapping:

```text
CREDENTIAL / EDUCATIONAL RULE
+ INSTITUTIONAL GATE
+ ACTOR EDUCATION HISTORY
+ OCCUPATIONAL POSITION / APPLICATION / ASSIGNMENT
-> ELIGIBILITY / POSITION POSSIBILITY
-> REALIZED POSITION / CONTINUED-EDUCATION PATH IF ACTUAL
```

Mechanism families:

- `INSTITUTIONAL_GATE`;
- `HISTORICAL_TIMING_QUALIFICATION`;
- `TRANSITION_REBINDING` where a realized position transition actually occurs.

### 1.5 Job protection and security

Source constructs:

- union/contract/Civil Service protection;
- grievance procedure;
- sick pay;
- employment-security law;
- vacation/legal protections;
- class-linked benefits.

Rawlsing mapping:

```text
LEGAL / CONTRACT / ORGANIZATIONAL PROTECTION RULE
+ ACTOR'S EXACT EMPLOYMENT RELATION
-> PROTECTION ENTITLEMENT / APPLICABILITY
-> REALIZED PROTECTION STATE / GATE OUTCOME AS EVIDENCED
```

Mechanism families:

- `RESOURCE_DEPENDENCY`;
- `INSTITUTIONAL_GATE`;
- `PERSISTENT_STRAIN_CONDITION` only downstream where actual insecurity/security changes lived condition.

Firewall:

```text
SYSTEM-WIDE LAW != ACTOR USED/BENEFITED FROM PROTECTION
```

unless the target claim only concerns universal legal entitlement and the actor is proven to be in the covered class.

## 2. D1 mapping: actor-relative derivation

The source is one of the clearest empirical arguments for D1's positive connective function.

A compliant derivation should look like:

```text
DERIVE(
  admitted_structural_fact,
  actor_binding,
  exact relational position,
  mechanism_rule,
  institutional_configuration_ref,
  valid_time/history,
  counterpart/institution refs
)
-> typed_actor_relative_condition
```

### Examples

```text
state-sector employment-security law
+ actor employed in covered nationalized-sector position
-> JOB_PROTECTION_ENTITLEMENT_APPLICABILITY
```

```text
enterprise supervisory hierarchy
+ actor bound as subordinate to supervisor S
+ enacted close-monitoring rule/practice
-> ACTIVE_CLOSE_SUPERVISION_RELATION
```

```text
task allocation requiring complex work with data/people/things
+ actor actually assigned/performing role
-> COMPLEX_TASK_REQUIREMENT
-> ACTIVE_RECURRENT_COMPLEX_WORK
```

```text
central credential/allocation rule
+ actor placed in technical role before full credential completion
-> CONTINUED_EDUCATION_REQUIREMENT/OPPORTUNITY
-> if pursued: ACTIVE_EDUCATIONAL_SELF_DIRECTION HISTORY
```

### Required M7 provenance addition

For system-dependent rules, D1 must not stop at generic structural fact. Preserve:

```text
INSTITUTIONAL_CONFIGURATION_REF(S)
VALID_HISTORICAL_INTERVAL
RULE / ORGANIZATIONAL SOURCE REF(S)
PORTABILITY_BOUNDARY / EVIDENCE_SCOPE
```

These can be governed fields within existing provenance rather than new classes.

## 3. D2 mapping: conditions, relations, recurrence, history

The source's causal grain demands temporal forms beyond discrete encounter/event.

### 3.1 Condition

Examples:

- long-term job insecurity/security;
- sustained low/high self-direction;
- continuing credential requirement;
- persistent class/organizational position.

Represent as active intervals, not repeated event tokens.

### 3.2 Relation

Examples:

- worker -> supervisor;
- manager -> subordinate hierarchy;
- parent -> child linked-life relation;
- employee -> employer/state-enterprise relation.

Carry counterpart identity, direction, authority/obligation scope and validity interval.

### 3.3 Recurrent activity

Most important source form:

```text
ACTIVE_RECURRENT_COMPLEX_WORK
ACTIVE_RECURRENT_ROUTINE_WORK
ACTIVE_RECURRENT_WORK_UNDER_CLOSE_SUPERVISION
```

A recurrence record must preserve enough to distinguish:

- content/quality;
- intensity/frequency/duration;
- supervision/control conditions;
- institutional/role provenance.

The book's evidence does not require conscious appraisal on every iteration.

### 3.4 Transition and rebinding

Examples potentially requiring rebinding:

- change in job;
- move into managerial/supervisory position;
- occupational entry before credential completion;
- later advancement;
- change in family linked-life role.

M7 does **not** independently prove the full rebinding transaction semantics, but it confirms that comparing before/after occupational conditions cannot be reduced to an isolated event label.

### 3.5 Trajectory/history

Store ordered earlier/later job/self-direction states where available. Do not infer dense trajectories from two-wave data.

## 4. V3 ingress mapping

Kohn/Słomczyński's measured psychological endpoints include:

- valuation of self-direction/conformity;
- intellectual/ideational flexibility;
- self-directed orientation;
- distress/well-being.

The M7 source does not authorize the SDTF seam to mint these directly.

Required boundary:

```text
PRE-V3 / D1-D2 OUTPUT
  objective/actor-relative condition,
  relation,
  recurrent activity,
  protection/gate state,
  linked-life input

-> EXISTING V3 RECEIVER

-> only if V3 earns it:
  value/orientation/cognitive/affective change
```

The source strengthens the frozen candidate's claim that social conditions are inputs to development, not already development.

## 5. Subject mediation mapping

The book cannot tell Rawlsing exactly how a worker:

- interprets close supervision;
- understands a complex task;
- converts repeated work into a generalized value;
- forms motive/reason from a condition;
- perceives or misperceives objective job protection;
- transmits a parental value in microinteraction.

Therefore no M7-specific `INTERNALIZATION`, `SOCIALIZATION`, `APPRAISAL`, `MOTIVE`, or `MEANING` operator should be added.

Where existing V3 owns subject-relative premises, grounds, motive, memory, practice or attractor change, M7 supplies only lawful social-world inputs with exact provenance.

## 6. Mapping to frozen mechanism-family registry

| M7 source mechanism | Frozen family mapping | M7 ruling |
|---|---|---|
| ownership/resource dependence | `RESOURCE_DEPENDENCY` | `REUSE/GENERALIZE`; exact institutional relation required |
| supervision/hierarchy/control | `AUTHORITY_CONTROL_SANCTION` | strongly supported |
| task complexity/routinization | `ACTIVITY_ORGANIZATION` | strongly supported |
| credential/job allocation | `INSTITUTIONAL_GATE` | supported; system-qualified |
| family-role obligations | `ROLE_OBLIGATION` | supported, counterpart-specific |
| parent-child transmission | `LINKED_LIFE_TRANSMISSION` | supported at broad chain; microcarrier unresolved |
| historical labor-law configuration | `HISTORICAL_TIMING_QUALIFICATION` | strongly required as provenance/boundary |
| psychological functioning -> later job condition | `GATED_RECIPROCAL_SELECTION` | supported narrowly |
| distress under insecurity/protection | `PERSISTENT_STRAIN_CONDITION` | partial, especially Poland |
| repeated complex/self-directed work | `ACTIVITY_ORGANIZATION` + D2 recurrence | strongest temporal support |
| actor action -> changed social rule/world | `COLLECTIVE_STRUCTURAL_FEEDBACK` / D3 | not independently supported by this source |

No new family is required solely from M7.

## 7. Class/stratification mapping rule

Rawlsing should **not** store a broad class association as if the class label itself were the causal input to V3.

For causal use, decompose wherever evidence supports it into:

```text
OWNERSHIP
AUTHORITY / HIERARCHICAL POSITION
SUBSTANTIVE COMPLEXITY
CLOSENESS OF SUPERVISION
ROUTINIZATION
ORGANIZATIONAL / BUREAUCRATIC LOCATION
EDUCATION / CREDENTIAL HISTORY
OCCUPATIONAL STATUS
INCOME
JOB PROTECTION / SECURITY
SECTOR LOCATION
LABOR-DEMAND / BARGAINING POSITION
OTHER CONCRETE CONDITION
```

Any direct residual not decomposed remains `UNEXPLAINED_RESIDUAL`.

## 8. Comparative-invariance mapping rule

Mechanism metadata must distinguish at least:

```text
MECHANISM_REPLICATES
MECHANISM_CHANGES_MAGNITUDE
MECHANISM_REVERSES
MECHANISM_DISAPPEARS
MEASUREMENT_DOES_NOT_TRANSLATE
EVIDENCE_INCONCLUSIVE
```

This does **not** necessarily mean a new runtime enum. It is a governance/evidence obligation so that the system does not turn one-country evidence into universal causal law.

## 9. System configuration as provenance, not actor trait

M7's most important architectural distinction:

```text
SYSTEM CONFIGURATION
IS UPSTREAM CAUSAL PROVENANCE / BOUNDARY CONDITION
NOT AN ACTOR ATTRIBUTE
```

Correct:

```text
POLISH_1978_NATIONALIZED_SECTOR_LABOR_LAW
-> covered actor employment relation
-> protection entitlement
```

Incorrect:

```text
actor.country = Poland
-> protected = true
```

Correct:

```text
CENTRALIZED_ENTERPRISE_AUTHORITY_CONFIGURATION
-> exact supervisor/subordinate relation
-> close-supervision condition
```

Incorrect:

```text
actor.country = Poland
-> authoritarian_experience = high
```

This distinction is the smallest way to preserve the book's comparative intelligence inside Rawlsing.

## 10. Residual handling mapping

When a broad association survives tested mediators, retain a visible negative result:

```text
UNEXPLAINED_RESIDUAL
```

with:

- observed association source;
- mechanisms already tested;
- possible but unmeasured mechanisms;
- measurement ceiling;
- temporal ceiling;
- prohibition on actor-level inference from the residual itself.

No runtime scalar is demanded; the requirement can remain in evidence/provenance governance.

## 11. Evidence-scope mapping

For each imported mechanism, preserve source scope:

- industrialized societies are the book's intended general domain;
- principal direct comparison is employed men in US/urban Poland;
- family findings use selected intact families/children in sampled ages;
- women appear in family/US work-housework evidence but not as the main comparable baseline population;
- Poland lacks a true male longitudinal panel comparable to the US;
- nonindustrial/partially industrialized portability is not established.

A mechanism family may be architecture-general while its **empirical authorization** remains bounded.

## 12. Smallest architectural consequence

M7 recommends **no D4** and no new sociology module.

Smallest consequence:

1. retain D1;
2. make explicit that D1's provenance carries system/institutional configuration when causally constitutive;
3. retain D2's interval/recurrent-activity/history grammar with source-appropriate temporal ceilings;
4. do not cite M7 as authority for full D3 social-world update;
5. preserve portability/evidence status and unexplained residuals in governance metadata.

In compact form:

```text
D1+
  TYPED_ACTOR_RELATIVE_SOCIAL_ECOLOGY_DERIVATION
  + INSTITUTIONAL_CONFIGURATION_PROVENANCE
  + PORTABILITY/EVIDENCE_BOUNDARY

D2
  RETAIN, SOURCE-QUALIFIED

D3
  NO M7 INDEPENDENT VALIDATION

D4
  NONE
```

## Terminal

`PASS__M7_RAWLSING_MAPPING__D1_INSTITUTIONAL_PROVENANCE_EXPLICIT__D2_RECURRENCE_PRESERVED__D3_SOURCE_CEILING_PRESERVED__NO_NEW_PSYCHOLOGY_OR_D4`.
