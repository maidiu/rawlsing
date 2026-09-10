# M10 — CONTRADICTORY CLASS LOCATION COURT R1

STATUS: `COURT_COMPLETE`

QUESTION: Does Wright's contradictory-class-location problem require a new Rawlsing person primitive, or does it demonstrate why an actor needs multiple typed relations?

VERDICT:

`MULTIPLE_TYPED_RELATIONS_REQUIRED__NO_NEW_PERSON_TYPE__NO_CLASS_SCALAR`

## 1. Historical reconstruction

Wright's early solution began by rejecting the assumption that each position must belong to one and only one class. Managers appeared simultaneously subordinate upward and dominant downward. He initially expanded this through control over investment, physical production and labour, and treated professionals/semi-autonomous employees as mixed locations.

Wright later attacks that version. The problems are decisive for Rawlsing:

- `autonomy` is not reliably petty-bourgeois and can vary contingently by work setting;
- domination by itself does not establish opposing material interests;
- the early concept displaced exploitation with domination;
- a position may be heterogeneous without possessing a special contradictory essence.

The later framework reconceives the issue as **intersection of exploitation relations** grounded in different productive assets.

## 2. Runtime court cases

### Case A — expert manager

```text
NO CAPITAL OWNERSHIP SUFFICIENT FOR INDEPENDENT REPRODUCTION
+ SELLS LABOUR TO EMPLOYER
+ EFFECTIVE POLICY/COORDINATION CONTROL
+ DIRECT AUTHORITY OVER SUBORDINATES
+ SCARCE CREDENTIAL MATCHED TO JOB
```

Consequences are relation-specific:

- wage/employer dependency upward;
- policy/control resources;
- task/sanction powers downward;
- credential-based exit/bargaining options;
- potentially divergent objective stakes around capital, organization democratization and credential scarcity.

Nothing here requires `CLASS=CONTRADICTORY`. The label is fully reconstructible.

### Case B — uncredentialled manager

Same capital/wage and organization-control relations, no established credential scarcity. This directly disproves a single generic `middle-class` ecology.

### Case C — non-managerial expert

Wage dependency + credential scarcity, no organization-control relation. Again, a class label would conceal the causal difference from Case A.

### Case D — small employer

Owns productive assets + hires labour + personally works. Runtime needs own-work obligations, employee counterparts, appropriation relation, payroll/market risks and resource control. `Small employer` adds no causal primitive.

### Case E — household member with mixed external/internal relations

A working-class wage relation can coexist with domination/exploitation or dependency inside a household. Actor ecology must preserve each counterpart and domain. One `class` field cannot do so.

## 3. Interest court

A contradictory location does not create an internally conflicted personality by definition.

At most, typed relations generate potentially opposed **objective structural stakes**:

```text
STAKE_CAPITAL_RELATION
STAKE_ORGANIZATION_CONTROL
STAKE_CREDENTIAL_SCARCITY
STAKE_HOUSEHOLD_RESOURCE_CONTROL
...
```

Whether the actor recognizes, ranks, suppresses, moralizes, resists or acts on these stakes belongs to subject formation / action selection downstream.

Therefore:

```text
CONTRADICTORY STRUCTURAL STAKES
!= PSYCHOLOGICAL AMBIVALENCE
!= IDEOLOGICAL CENTRISM
!= CLASS CONSCIOUSNESS
!= BEHAVIOR
```

## 4. Rawlsing primitive test

Existing SDTF candidate semantics already support:

- more than one `POSITION_REF` / relation;
- `RESOURCE_DEPENDENCY`;
- `AUTHORITY_CONTROL_SANCTION`;
- `INSTITUTIONAL_GATE`;
- `ACTIVITY_ORGANIZATION`;
- counterpart bindings;
- histories/transitions.

A derived analytic predicate may be useful:

```text
CONTRADICTORY_RELATION_BUNDLE(actor, interval)
:= EXISTS relation_a, relation_b
   WHERE relation_a and relation_b generate opposed structural stakes
   under distinct typed asset/control dimensions
```

This predicate must retain references to the underlying relations and must never become an input that bypasses them.

## 5. New primitive verdict

**F. Do contradictory locations require any new primitive?**

**NO.** Their exact lesson is the opposite: a one-dimensional person classification is information-destroying. The correct representation is multiplex typed actor-counterpart/institution relations plus optional derived analyst summaries.

## Court terminal

`PASS__CONTRADICTORY_CLASS_LOCATION_DECOMPOSES_TO_MULTIPLEX_TYPED_RELATIONS__NO_NEW_PRIMITIVE`
