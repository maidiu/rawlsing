# S3 R4 TRANSITION SCENARIO REPLAY R1

STATUS: `MANDATORY_TRANSITION_CHAINS_REPLAYED__DETERMINANT_SCOPED_SURVIVAL_CONFIRMED`

This replay tests the requested chains against the R4 D1' constitution plus the S3 direct-dependency, invalidation, cycle, and evidence-ceiling contracts. It does not claim any concrete mechanism rule is currently executable.

---

## Scenario 1 — infrastructure outage -> access/wait/activity

### Initial derivation

```text
SOURCE F1: infrastructure/service input current
RULE A [objective world/service configuration]
-> F2 service capacity current

F2 service capacity
+ actor location/service relation binding
+ RULE B [P1/P4 as exact case requires]
-> F3 actor-specific access constraint

F3 access constraint
+ route/topology facts
+ RULE C [P1/P3]
-> F4 substitute route / wait-time consequence

F4 time consequence
+ household activity binding
+ RULE D [P3]
-> F5 household activity/time consequence
```

### Outage begins

New competent source fact `F1' = outage/degraded state` invalidates only applications whose determinant set included the prior infrastructure/service state. `F2-F5` are reevaluated through actual descendant edges. Unrelated employment, school, household-resource, or network facts survive.

### Service restored

Restoration is a new source-owned state, not deletion of the outage history. Prior outage consequences close at the restoration boundary; exact affected rules rerun. If normal capacity returns, access/wait/activity facts are newly derived or terminated as the rules warrant.

### Verdict

`PASS__NO_GLOBAL_RESET__PHYSICAL/WORLD INPUT MAY ROUTE THROUGH GOVERNED SOCIAL CONSEQUENCE RULES`.

---

## Scenario 2 — institutional record -> gate -> employment/resource/household

### Initial derivation chain

```text
F1 institutional record/mark
+ F2 gate encounter/presentation witness
+ current governed P4 rule
-> F3 gate treatment/decision

F3 treatment
+ employment-access rule
-> F4 employment nonaccess/resultant state

F4
+ exact wage/resource relation
+ P1 rule
-> F5 resource/income consequence

F5
+ household transfer/dependency relation
+ exact P1/P5 rule
-> F6 household transfer consequence
```

Each arrow has a distinct rule application. `RULE != APPLICABILITY != PRESENTATION != TREATMENT != DOWNSTREAM RESULT` remains preserved.

### Record corrected

If the source owner corrects `F1`, applications directly dependent on that record are invalidated for the correction's effective interval. Descendants `F3-F6` become candidates for scoped recomputation. The gate encounter `F2` can remain historical/current if independently true.

### New superseding treatment

If a later competent gate decision supersedes `F3`, only descendants whose rule contract depends on the old treatment are rederived. Other actor facts survive.

### Missing decision record

Missing/stale `F3` witness yields `NOT_PROVEN_REALIZED`; it does not imply denial. Downstream realized nonaccess cannot remain current solely from the missing witness unless another competent state source directly establishes the nonaccess fact.

### Verdict

`PASS__MULTI_STEP_P4_TO_P1_CHAIN_REQUIRES_EXACT_DIRECT_ANTECEDENTS_AND_WITNESS_CURRENTNESS`.

---

## Scenario 3 — job position -> authority/task/time -> termination

### Before termination

```text
JOB_POSITION J
+ supervisory/organizational configuration
+ P2 rule
-> authority/control consequence A

JOB_POSITION J
+ task/schedule configuration
+ P3 rule
-> task/time consequence T

JOB_POSITION J
+ wage/resource relation
+ P1 rule
-> wage/resource consequence W
```

Household relation `H`, child's school position `S`, and unrelated network relation `N` have independent producing applications without `J` as a determinant.

### Job termination at t1

A competent job-termination/position-exit fact closes `J` at `t1`.

Required behavior:

```text
invalidate/terminate A, T, W only to the extent their applications require J;
preserve H, S, N;
preserve pre-t1 A/T/W as historical where they were lawful;
rerun rules associated with any newly sourced unemployment/resource/household facts;
do not infer every consequence of job loss from the position exit alone.
```

A new resource loss, benefit eligibility, schedule release, or household task change requires its exact source/rule chain.

### Verdict

`PASS__TRANSITION_IS_DETERMINANT_SCOPED_REBINDING_NOT_ACTOR_RESET`.

---

## Scenario 4 — parent job loss -> resource -> household task -> child time obligation

### Chain

```text
F1 parent employment termination / income state
+ exact wage/resource rule
-> F2 household resource change

F2
+ household dependency/care relation
+ governed allocation rule
-> F3 household task-allocation consequence

F3
+ child household position/obligation rule
-> F4 child objective time obligation
```

No step permits:

```text
PARENT DISTRESS/MOTIVE/BELIEF
-> CHILD OBJECTIVE OBLIGATION
```

unless private state first produces an external action and competent world/household response that becomes a source-owned fact.

### Parent reemployment

New employment/resource state invalidates only descendants whose determinant set includes the prior resource/job state. If the task allocation remains independently source-owned despite reemployment, it may survive; S3 does not assume automatic reversal.

### Child's subjective response

F4 remains an objective D1' condition. How the child experiences or develops from it remains downstream V3/OBL062 territory and is not solved here.

### Verdict

`PASS__LINKED_LIFE_CHAIN_REQUIRES_EXTERNAL_FACTS_AND_EXACT_RELATIONAL_RULES`.

---

## Scenario 5 — network relation termination -> channel ends, material facts survive

### Before termination

```text
F1 exact network/counterpart relation
+ P5 rule
-> F2 information-channel consequence

F3 independently sourced material entitlement/resource state
+ P1 rule
-> F4 material-resource consequence
```

### Relation terminates

Competent termination of `F1` closes/invalidate `F2` from the termination boundary. It does not touch `F4` because `F1` is not a direct determinant of the P1 application.

If a separate resource flow was actually carried through the network relation, that flow fact would have its own determinant edge and could terminate; the independent entitlement/resource state still would not be deleted unless its own determinants change.

`CHANNEL ENDS` also does not establish that no information was ever transferred or that all other channels are absent.

### Verdict

`PASS__P5_TERMINATION_DOES_NOT PROPAGATE ACROSS UNCONNECTED P1 FACTS`.

---

## Cross-scenario transition law

All five chains support the same minimum transition grammar:

```text
COMPETENT SOURCE/BINDING/WORLD CHANGE
-> identify exact determinant identity/version
-> discover current direct dependent applications
-> close/invalidate only unsupported derived facts
-> recursively propagate only through actual descendants
-> preserve unaffected actor facts
-> preserve before/after provenance
-> evaluate newly applicable current rules under new determinants
-> emit new fact/application identities rather than rewriting old history.
```

---

## World-write firewall replay

None of the scenarios licenses:

```text
V3 PRIVATE STATE OR ACTION
-> DIRECT D1' INVALIDATION
or
V3 ACTION
-> NEW WORLD FACT BY D1'
```

Required route remains:

```text
V3 ACTION
-> EXTERNAL ACTION OCCURRENCE
-> COMPETENT EXTERNAL RESPONSE
-> COMPETENT SOURCE OWNER AUTHORS NEW WORLD FACT
-> NORMAL D1' INVALIDATION/REDERIVATION.
```

Verdict:

`WORLD_WRITE_FIREWALL_PASSES__NO_D3_OWNER_CREATED`.
