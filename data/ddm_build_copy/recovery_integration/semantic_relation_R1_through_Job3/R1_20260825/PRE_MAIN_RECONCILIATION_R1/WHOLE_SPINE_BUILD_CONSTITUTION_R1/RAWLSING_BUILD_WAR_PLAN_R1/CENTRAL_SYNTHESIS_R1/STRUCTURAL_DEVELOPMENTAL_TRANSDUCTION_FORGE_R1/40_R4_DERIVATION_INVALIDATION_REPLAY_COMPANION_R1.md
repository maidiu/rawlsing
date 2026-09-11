# R4 DERIVATION / INVALIDATION / REPLAY COMPANION R1

STATUS: `CANONICAL_G2_COMPANION_SPECIFICATION__DIRECT_DETERMINANT_PROVENANCE_AND_SCOPED_REPLAY_REQUIRED__R4_TOPOLOGY_UNCHANGED`

GOVERNING R4:
`dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

PRIMARY INDEPENDENT RETURN:
S3 `fbef94da7cda9729a590d87feb3e27ab40bf19a8`

RELATED COMPANION:
`39_R4_SEAM_NORMATIVE_COMPANION_CONTRACT_R1.md`

---

## 0. Purpose

This companion defines the minimum semantic dependency/replay law necessary for D1' facts to remain correct when PRE-V3/world facts, positions, rules, relations or witnesses change.

It is not a generic graph architecture and creates no new temporal or world-writing owner.

The governing question is:

> When an objective determinant changes, exactly which D1' facts cease to be supported, which survive, and which must be rederived?

---

## 1. Canonical derivation shape

```text
EXACT DIRECT DETERMINANT(S)
        ↓
EXACT RULE APPLICATION
        ↓
OBJECTIVE POSITIONED CONSEQUENCE FACT
        ↓ if consumed by a later rule
LATER EXACT RULE APPLICATION
```

The semantic graph is bipartite at rule-application grain:

```text
FACT/BINDING/WITNESS/RULE-VERSION NODES
        -> RULE_APPLICATION NODE
        -> DERIVED CONSEQUENCE NODE
```

A physical graph database is not required.

---

## 2. Minimum application provenance

Every rule application must make the following exactly recoverable:

```text
RULE_APPLICATION_ID
DERIVED_FACT_REF
MECHANISM_RULE_REF + RULE_VERSION
DIRECT_DETERMINANT_REF(S)
DETERMINANT_ROLE(S)
ACTOR_REF
WORLD_REF
CONTEXT_REF(S)
POSITION_REF(S)
VALID_TIME_OR_INTERVAL
REQUIRED WITNESS REF(S) where applicable
EFFECTIVE_EVIDENCE_CEILING
CURRENTNESS / LIFECYCLE STATE
```

A determinant role should identify why an antecedent matters, e.g.:

```text
STRUCTURAL_SOURCE
POSITION_BINDING
CONTEXT_BINDING
COUNTERPART_BINDING
INSTITUTIONAL_CONFIGURATION
OBJECTIVE_HISTORY
REALIZATION_WITNESS
NEGATIVE_WITNESS
CLOSED_WORLD_SCOPE
RULE_VERSION
```

Names are nonbinding; direct dependency identity is mandatory.

---

## 3. Reverse dependency discoverability

For any determinant D, the system must be able to discover every current rule application that directly depends on D.

This is a semantic requirement, not a prescribed index implementation.

Required query answer:

```text
GIVEN CHANGED DETERMINANT D
WHICH CURRENT D1' APPLICATIONS DIRECTLY CONSUME D?
```

If the system cannot answer that without an actor-wide/domain-wide reset, the proposed hosting does not conform.

---

## 4. Invalidation triggers

A current D1' application/fact must be reevaluated when a required determinant ceases to satisfy the exact rule contract for the asserted interval.

Canonical triggers include:

```text
SOURCE FACT CORRECTION
SOURCE FACT EXPIRY
REQUIRED WITNESS EXPIRY / CURRENTNESS FAILURE
RULE VERSION CHANGE
RULE WITHDRAWAL / INVALIDATION
ACTOR POSITION EXIT
CONTEXT CLOSURE
COUNTERPART RELATION TERMINATION
CONSTITUTIVE INSTITUTIONAL-CONFIGURATION CHANGE
NEW GOVERNED SUPERSEDING TREATMENT
EXPLICIT TYPE-COMPATIBLE NEGATIVE / TERMINATION WITNESS
CLOSED-WORLD SCOPE LOSS OR SOURCE-HEALTH FAILURE
```

Missing evidence alone does not produce a negative fact.

---

## 5. Determinant-scoped replay law

```text
CHANGED DETERMINANT ID/VERSION
-> locate directly dependent current applications
-> reevaluate each exact rule contract
-> close/invalidate unsupported outputs
-> preserve prior lawful historical interval/provenance where appropriate
-> recursively visit only later applications that consume changed outputs
-> rerun only newly/currently applicable governed rules
-> preserve all unrelated facts.
```

Forbidden:

```text
JOB CHANGE -> RESET WHOLE ACTOR
HOUSEHOLD CHANGE -> RESET ALL CONTEXTS
WITNESS EXPIRY -> DELETE UNRELATED POSITION FACTS
RULE CHANGE -> RECOMPUTE EVERY SOCIAL FACT WITHOUT DEPENDENCY PROOF
```

---

## 6. Transition law

A transition is a competent admitted binding/world-state change, not an SDTF D2 owner.

Canonical composition:

```text
COMPETENT CHANGE
-> changed determinant identity
-> close affected current intervals
-> preserve before-state provenance
-> invalidate only dependent D1' assertions
-> establish/rebind new actual determinants
-> apply current rules under new bindings
-> issue new application/fact identities as required.
```

Unrelated contexts survive.

Example:

```text
JOB EXIT
-> close job-position binding
-> close/rederive job authority/task/wage/channel consequences
-X-> delete household relation
-X-> delete school position
-X-> delete unrelated network relation
```

---

## 7. Assertion-kind interaction

Replay respects the proof kinds defined in File 39.

### K1 constitutive

A rule/position/configuration change may terminate or alter constitutive truth even without a contingent event.

### K2 qualified possibility

A route/eligibility/reachability change removes qualification; it does not prove the opposite unless negative truth is independently licensed.

### K3 realized occurrence

A historical occurrence remains historically true if validly witnessed even when later facts change. Later correction to the source/witness may retrospectively invalidate the claim at the corrected grain.

### K4 active durative

A determinant/witness/termination change may close currentness while preserving the prior lawful interval. Loss of current proof yields no automatic opposite fact.

---

## 8. Cycle law

Default R4 D1' derivation is acyclic within one factual state/version and valid-time slice.

Binding:

```text
NO D1'-DERIVED FACT MAY BE ITS OWN ANCESTOR
AT THE SAME WORLD/STATE VERSION AND VALID-TIME SLICE.
```

Forbidden default:

```text
A(t) -> B(t) -> A(t)
```

merely because both pairwise rules appear plausible.

Same-time acyclic constitutive chains remain lawful.

---

## 9. Iterative/fixed-point law

A repeated process is lawful only when progress is grounded by at least one of:

```text
ADVANCED TIME
ADVANCED STATE/SOURCE VERSION
NEW EXTERNAL SOURCE-OWNED FACT
NEW COMPETENT WITNESS
EXPLICIT COMPETENT ITERATION/FIXED-POINT AUTHORITY
```

No generic fixed-point owner is created here.

Any future explicit iteration contract must define:

- state identity/version;
- termination/convergence semantics;
- provenance per step;
- cycle legality;
- evidence/currentness handling.

`CUMULATIVE DISADVANTAGE` or another theory label cannot serve as iteration authority.

---

## 10. Evidence/authority ceiling propagation

A derived fact cannot acquire stronger authority than the conjunction of the exact governed rule and all truth-determining inputs/witnesses.

Binding:

```text
DERIVED_EVIDENCE_AUTHORITY
<= RULE_CAUSAL_USE_AUTHORITY
AND
<= REQUIRED_DETERMINANT/WITNESS AUTHORITY
```

Preserve all relevant:

```text
CONTEXT CEILINGS
HISTORICAL CEILINGS
PORTABILITY CEILINGS
IDENTIFICATION CEILINGS
CURRENTNESS CEILINGS
CALIBRATION CEILINGS
```

When evidence dimensions are incomparable, preserve them as a structured conjunction/vector rather than converting them to a stronger scalar certainty.

Forbidden upgrades:

```text
OBSERVATIONAL ASSOCIATION -> RANDOMIZED CERTAINTY
SOURCE CITATION -> CAUSAL-USE AUTHORITY
GROUP RATE -> ACTOR FACT
STALE WITNESS -> CURRENT FACT
MISSING POSITIVE -> NEGATIVE
MULTIPLE WEAK LINKS -> STRONGER CLAIM
```

---

## 11. World-change firewall

D1' derivation/replay consumes competent external facts. It does not author social-world change directly from private person state or intention.

Required route:

```text
V3 PERSON/COLLECTIVE ACTION
-> COMPETENTLY ADMITTED EXTERNAL ACTION OCCURRENCE
-> COMPETENT COUNTERPART / INSTITUTION / WORLD RESPONSE
-> COMPETENT SOURCE OWNER AUTHORS NEW EXTERNAL FACT
-> STRUCTURAL ADMISSION IF STRUCTURAL MEANING IS CLAIMED
-> NORMAL D1' INVALIDATION / REDERIVATION
```

Forbidden:

```text
V3 PRIVATE STATE -> INVALIDATE D1' FACT
V3 INTENTION -> WORLD FACT
V3 ACTION -> STRUCTURAL CHANGE WITHOUT EXTERNAL RESPONSE
D1' DERIVED FACT -> NEW STRUCTURAL FACT BY SELF-REFERENCE
```

---

## 12. Canonical replay examples

### Infrastructure chain

```text
POWER/INFRASTRUCTURE OUTAGE
-> SERVICE CAPACITY REDUCTION
-> ACTOR ACCESS CONSTRAINT
-> WAIT/SUBSTITUTE-ROUTE CONSEQUENCE
-> ACTIVITY/TIME CONSEQUENCE
```

Restore the upstream capacity fact:
only descendants depending on the outage/capacity constraint are reevaluated.

### Institutional mark chain

```text
PRIOR SOURCE-OWNED RECORD
-> GATE PRESENTATION
-> GATE TREATMENT
-> EMPLOYMENT ACCESS RESULT
-> RESOURCE/INCOME STATE
-> HOUSEHOLD TRANSFER/TASK CONSEQUENCE
```

Correct or supersede the prior record:
replay begins at the first application whose determinant changed, not at a global actor reset.

### Linked-life chain

```text
PARENT JOB LOSS
-> HOUSEHOLD RESOURCE CHANGE
-> GOVERNED TASK ALLOCATION CHANGE
-> CHILD OBJECTIVE TIME OBLIGATION
```

Parent private distress alone is not a determinant.

---

## 13. Relationship to G1/G3/G4

This companion supplies G2 derivation/replay semantics only.

It depends on:

```text
G1 exact mechanism-rule admission/currentness
G3 type-specific witness/currentness/termination contracts
```

and remains agnostic about:

`G4 / OBL062 non-event V3 ingress`.

A lawful D1' fact can be derivable/current while its generic V3 ingress remains open.

---

## 14. Conformance terminal

Any proposed D1' host/replay implementation fails R4 conformance if it cannot:

1. expose exact direct determinants;
2. locate direct dependents;
3. invalidate/rederive only dependent facts;
4. preserve unrelated facts and historical provenance;
5. block same-time self-ancestry absent explicit authority;
6. preserve evidence/authority ceilings;
7. prevent V3/private-state direct world writes.

---

## Companion terminal

`R4_DERIVATION_INVALIDATION_REPLAY_COMPANION_READY__DIRECT_DETERMINANT_GRAPH_REQUIRED__SCOPED_REPLAY_REQUIRED__SAME_STATE_SELF_ANCESTRY_FORBIDDEN__EVIDENCE_AUTHORITY_CANNOT_STRENGTHEN__NO_D2_D3_D4_P6__OBL062_OPEN`
