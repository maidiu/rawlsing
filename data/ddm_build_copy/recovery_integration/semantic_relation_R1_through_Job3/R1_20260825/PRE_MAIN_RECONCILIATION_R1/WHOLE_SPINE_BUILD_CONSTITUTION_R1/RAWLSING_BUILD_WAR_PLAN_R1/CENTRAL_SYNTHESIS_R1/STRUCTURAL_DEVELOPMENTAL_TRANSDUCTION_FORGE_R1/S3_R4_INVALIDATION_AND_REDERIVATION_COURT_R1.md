# S3 R4 INVALIDATION AND REDERIVATION COURT R1

STATUS: `DETERMINANT_SCOPED_INVALIDATION_AND_REPLAY_LAW_SPECIFIED`

This court assumes the direct-dependency contract in `S3_R4_DERIVATION_GRAPH_CONTRACT_R1.md` and the R4 truth-condition law in File 35. It specifies semantic behavior only; no runtime is implemented.

---

## 1. Governing invalidation law

```text
A D1' FACT CEASES TO BE CURRENT
WHEN ANY REQUIRED DIRECT DETERMINANT FOR ITS PRODUCING APPLICATION
CEASES TO BE VALID/APPLICABLE FOR THE ASSERTED INTERVAL,
OR WHEN A COMPETENT SUPERSESSION/TERMINATION/NEGATIVE FACT
DEFEATS THE ASSERTION UNDER THE GOVERNING RULE.
```

Invalidation propagates only through actual determinant edges:

```text
CHANGED DETERMINANT
-> DIRECTLY DEPENDENT RULE APPLICATIONS
-> THEIR DERIVED FACTS
-> LATER APPLICATIONS THAT USE THOSE FACTS
```

Unrelated facts survive.

`TRANSITION != GLOBAL ACTOR RESET`.

---

## 2. Invalidation is not deletion

Three different outcomes must remain distinct:

```text
TERMINATE CURRENT VALIDITY
INVALIDATE A PRIOR APPLICATION AS ERRONEOUS/CORRECTED
SUPERSEDE WITH A NEWER COMPETENT RESULT
```

Historical facts that were valid before a real-world transition remain historically valid for their prior interval. A source correction, by contrast, may mark a prior derivation as invalid even for an interval previously thought valid. Supersession preserves both prior and new identities and the replacement relation.

---

## 3. Trigger court

| Trigger | Immediate semantic effect | Rederivation rule |
|---|---|---|
| source fact correction | invalidate applications whose truth depended on corrected content from the correction's competent effective scope | rerun only affected rules against corrected/current determinants |
| source fact expiry | terminate current dependent facts at expiry boundary unless another current determinant replaces it | rerun only if replacement/current source facts satisfy the same or another current rule |
| realization witness expiry/currentness failure | ACTIVE/REALIZED assertion becomes `UNKNOWN/NOT_PROVEN_REALIZED` from failure boundary; constitutive qualification may survive if independently supported | rerun if a new valid type-compatible witness exists; absence of witness never derives a negative fact |
| rule version change | old-version applications cease to authorize new/current output outside old rule validity | rerun affected applications under the newly current rule version if applicable; do not silently mutate old provenance |
| rule invalidation/withdrawal | facts whose truth depends on that rule lose current authority in the invalidated scope | no positive replay until a competent replacement rule exists |
| actor position exit | terminate only facts whose rules require the exited position | rerun rules attached to the new current position/bindings; unrelated household/school/network facts survive |
| context closure | terminate only facts whose applicability depends on that context | rerun in surviving/new contexts only where current bindings exist |
| counterpart relation termination | terminate relation/channel consequences dependent on that counterpart relation | rerun only if another current counterpart relation satisfies a governed rule |
| institutional configuration change | invalidate/terminate only applications for which the changed configuration is constitutive or portability-limiting | rerun with current configuration and current rule authority |
| new superseding treatment | terminate/supersede the exact prior resultant fact(s) under the treatment's governed semantics | derive replacement consequences from the new treatment; no generic domain reset |
| explicit negative witness | defeats a positive realized assertion only where type, polarity, actor, context and time are compatible | may support a separate negative fact only under exact negative semantics/rule authority |

---

## 4. Correction versus transition

### Real-world transition

```text
OLD FACT valid through t0
NEW SOURCE-OWNED WORLD/BINDING FACT at t1
-> terminate affected consequence at t1
-> preserve old derivation as historical
-> compute any new consequence from t1
```

### Retrospective correction

```text
SOURCE OWNER CORRECTS antecedent for interval [a,b]
-> mark dependent applications over [a,b] invalid/corrected
-> retract current/historical assertions that no longer have lawful support
-> recompute only those dependency descendants
```

A correction therefore can revise prior asserted truth; a transition normally closes one valid interval and opens another.

---

## 5. Witness-specific narrowing

R4's witness law creates a particularly important split:

```text
QUALIFIED / CONSTITUTIVE FACT
may remain current
while
ACTIVE / REALIZED FACT
loses current proof.
```

Example:

```text
SERVICE ELIGIBILITY remains true
TRANSFER WITNESS expires
-> eligibility survives
-> current receipt becomes NOT_PROVEN_REALIZED
```

Likewise:

```text
SUPPORT CHANNEL remains current
last support-transfer witness becomes stale
-> channel survives
-> current support receipt does not.
```

This is determinant-scoped narrowing, not whole-fact-family invalidation.

---

## 6. Determinant-scoped recomputation algorithm, semantic form

No generic dependency solver is constitutionalized. The required semantics are only:

```text
1. competent owner publishes a changed/expired/corrected/superseding determinant;
2. resolve all current D1' rule applications with a direct determinant edge to that identity/version;
3. reevaluate those applications' currentness;
4. close/invalidate only outputs that no longer satisfy their exact rule contract;
5. recursively visit applications that directly consume those changed outputs;
6. evaluate exact newly applicable/current rules under new bindings;
7. emit replacement facts with new producing-application identities;
8. preserve untouched facts and all before/after provenance.
```

A reverse index may optimize step 2, but the semantic key is the exact determinant identity, not actor-wide invalidation.

---

## 7. Negative-evidence firewall during invalidation

```text
POSITIVE FACT INVALIDATED
!= NEGATIVE FACT DERIVED
```

If a service-receipt witness expires, the lawful result is `NOT_PROVEN_REALIZED`, not `NONRECEIPT`.

If a network relation ends, that may prove `RELATION_TERMINATED` where the termination witness is competent, but it does not prove that every earlier or parallel information/material/support relation was absent.

If a job position ends, facts tied to that position terminate; unemployment/resource loss requires its own competent source facts/rules rather than being silently inferred beyond the exact termination semantics.

---

## 8. Rule-currentness and replay

Rederivation always uses the rule version current for the target interval/context under competent authority.

```text
REPLAY OLD APPLICATION
!= REUSE OLD RULE AUTOMATICALLY
```

If the rule changed, the new application must cite the new current rule ref/version. If no rule is current, the seam produces no replacement fact merely to maintain continuity.

---

## 9. Court verdict

The minimum safe law is:

```text
INVALIDATE BY DIRECT DETERMINANT IDENTITY,
PROPAGATE THROUGH ACTUAL DEPENDENCY DESCENDANTS,
PRESERVE UNRELATED FACTS,
PRESERVE HISTORICAL INTERVALS,
AND REDERIVE ONLY FROM CURRENT BINDINGS + CURRENT RULE + CURRENT REQUIRED WITNESSES.
```

This is G2 replay semantics inside D1' support. It does not create D2 temporal ownership or D3 world-writing authority.
