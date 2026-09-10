# M10 — CLASS RELATION DECOMPOSITION LEDGER R1

STATUS: `CLASS_CATEGORY_DECOMPOSITION_COMPLETE`

RULE:

```text
CATEGORY
-> UNDERLYING STRUCTURAL RELATIONS
-> ACTOR-RELATIVE ECOLOGY CONSEQUENCES
-> REALIZATION REQUIREMENTS
```

A category is runtime-worthy only if it contributes information not already present in the underlying typed relations. In nearly every Wright case, it does not.

## A. Capitalist-society categories

| Wright category | Underlying structural relations | Actor-relative ecology consequences | Runtime verdict |
|---|---|---|---|
| **Capitalist / bourgeoisie** | Effective ownership/control of substantial means of production; ability to hire labour; claim over residual/surplus; market access; often organization control. | Does not depend on selling own labour for subsistence; hiring options; investment/disinvestment power; counterpart dependency from employees; control over allocation of surplus; exposure to market/credit/competition. | Category derived only. Execute ownership, claims, hiring, investment, counterpart and organization relations. |
| **Worker / proletarian** | Lacks sufficient means of production; sells labour power; employer controls capital asset; specific employment contract and organizational assignment. | Income/subsistence dependence on wage relation; bounded exit options; task/authority exposure; schedule/time demands; dismissal risk; possible bargaining/collective organization channels. | Category derived only. `WAGE_DEPENDENCY` and concrete employment/authority relations are runtime facts. |
| **Semi-proletarian** | Owns some productive assets but insufficient for reproduction; also sells labour power. | Multiple income/resource channels; partial exit from employer; time allocation conflict; market risk plus wage dependence. | No new primitive: simultaneous ownership + wage relation. |
| **Petty bourgeois / self-employed producer** | Owns/controls productive assets around self-reproduction level; works own production; little/no hired labour. | Greater formal control over work but market/credit/customer dependence; capital-loss risk; no automatic autonomy in practice. | Category derived. Runtime requires ownership, debt/credit, contracts, customers, work demands. |
| **Small employer** | Owns productive assets; works in enterprise; hires a small number of workers; appropriates some surplus. | Both own-work requirement and employer power; employee counterparts; payroll/market obligations; partial ability to convert others' labour into income; potentially constrained exit. | Multiple typed relations; no special type. |
| **Manager** | Effective control over organization assets: policy/coordination decision rights plus authority over subordinates; usually non-owner wage-earner. | Decision scope; access to organizational information/resources; authority/sanction applicability; responsibility/obligation; dependence on superior/owner; possible surplus claim/rent. | Runtime must store specific decision and authority edges. `MANAGER` is derived analyst label. |
| **Supervisor** | Effective task and/or sanction authority over subordinates without core policy control. | Can assign tasks/procedures/pace and/or affect warnings, promotion, suspension, firing depending on actual scope; simultaneously subordinate upward. | No scalar authority. Store directed rights and sanctions by scope. |
| **Nominal/formal supervisor** | Title or formal hierarchy position without proven effective task/sanction control. | Potential expectation/role but no earned coercive power until rights are evidenced/realized. | Do not treat title as active authority. |
| **Expert / credential asset holder** | Scarce skill and/or credential; institutional rule limits supply; job actually requires/deploys it. | Eligibility to restricted jobs; bargaining leverage/rent opportunity; differentiated replacement risk; access to task complexity/autonomy may follow assignment. | Split credential, skill, scarcity, job requirement, deployment, bargaining consequence. |
| **Marginally credentialled / skilled employee** | Ambiguous or partial credential/skill evidence; sometimes autonomy used as proxy. | Only probabilistic/measurement-level implication. | Measurement category only; never structural primitive. |
| **Non-managerial expert** | Wage dependence + credential/skill scarcity relation; no proven organization control. | Employer dependency coexists with restricted-labour-supply bargaining power; no supervision edge by default. | Multiple relations; no new primitive. |
| **Expert manager** | Wage/nonownership relation + organization control + skill/credential scarcity. | Upward dependence, downward authority, policy access, high bargaining power, multiple possible surplus/rent channels. | Canonical evidence for multiplex actor relations. Do not collapse to one class score. |
| **Uncredentialled manager** | Wage/nonownership + organization control without established credential scarcity. | Authority/policy powers with less credential-based exit/bargaining leverage. | Typed intersection only. |
| **`Middle class`** | Heterogeneous collection of the preceding intersections. | No single causal ecology. | **REJECT AS RUNTIME OBJECT.** Analyst/public-language label only. |
| **Contradictory class location** | Actor is exploited along one relation and exploiter/advantaged along another, or simultaneously dominant/subordinate across typed relations. | Mixed objective stakes, multiple possible alliances, variable exit/bargaining/control powers. | Derived relation-pattern predicate, not person type. |

## B. Abstract comparative categories in Wright's general typology

| Category | Relation | Executable kernel | Runtime verdict |
|---|---|---|---|
| **Feudal lord / serf** | Unequal effective rights over labour power; personal bondage; compelled dues/exit restriction. | labour-power right + obligation + mobility constraint + extraction relation. | Execute kernel; historical class label optional metadata. |
| **Statist manager/bureaucrat / non-management** | Unequal effective control of organization assets through planning hierarchy. | planning/coordination decision right + hierarchical allocation + surplus disposition. | Execute control hierarchy; category derived. |
| **Expert / worker in Wright's `socialism` abstraction** | Skill scarcity can generate rents after capital/organization equalization. | skill/credential scarcity + restricted supply + remuneration/rent. | Skill mechanism retained with Wright's own caveat that it may not constitute a class relation in the strong sense. |

## C. Household/family decomposition

Wright's household discussion is useful precisely where it stops assigning one automatic household class.

```text
HOUSEHOLD MEMBER A EMPLOYMENT/ASSET RELATIONS
+ HOUSEHOLD MEMBER B EMPLOYMENT/ASSET RELATIONS
+ INCOME POOLING / TRANSFER RULES
+ CONTROL OF INCOME / ASSETS
+ UNPAID LABOUR / CARE OBLIGATIONS
+ TIME ALLOCATION
+ DEPENDENCY / EXIT OPTIONS
-> MEMBER-SPECIFIC RESOURCE AND OBLIGATION ECOLOGIES
```

A spouse's class location may alter another person's resources, risks or political exposure only through these transfer/dependency/interaction relations. Wright explicitly makes domestic class assessment depend on real control over assets, income and labour time, not merely spouse category.

## D. `CLASS` after decomposition

What remains is a useful **analyst-level derived map** over:

- productive asset ownership/effective control;
- labour-power dependence and exit;
- organization/decision control;
- directed authority and sanctions;
- skill/credential scarcity and institutional closure;
- appropriation and counterpart dependence;
- household transfer/dependency intersections;
- histories/transitions among these relations.

For causal execution Rawlsing does not need `CLASS` as a primitive. A class label may be emitted as a derived descriptive summary when useful for reporting, comparison, source alignment or empirical measurement, but it must never replace the relations from which it was derived.

## E. Court terminal

`PASS__CLASS_CATEGORIES_DECOMPOSE_TO_TYPED_RELATIONS__NO_CLASS_SCALAR_OR_PERSON_TYPE_REQUIRED`
