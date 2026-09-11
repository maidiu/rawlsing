# R4 SEAM COMPANION SPECIFICATION FINAL R2

STATUS: `FINAL_REVIEWED_COMPANION_SPECIFICATION__READY_FOR_HQ_CONSIDERATION__R4_TOPOLOGY_UNCHANGED`

CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`

FROZEN R4 SEMANTIC TARGET:
`dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

PRE-REVIEW COMPANION SYNTHESIS:
`d5c92b09549b52aace9e1384c1b11955d947f5a7`

FINAL REVIEW TIP:
`ee9f1c559fcbe7804dd7ebcc239d7b591662779e`

FINAL REVIEW ADJUDICATION:
`47_R4_COMPANION_FINAL_REVIEW_ADJUDICATION_R1.md`

---

## 1. Purpose

This file is the final reviewed companion specification for the frozen R4 PRE-V3 -> D1' -> V3 seam constitution.

It does not alter frozen R4.
It does not perform HQ adoption.
It does not authorize production runtime.
It does not solve OBL062.

It makes R4 mechanically/auditably harder to misread by fixing the normative proof, provenance, invalidation, source-traceability, terminology and semantic-conformance obligations that any future implementation must preserve.

---

## 2. Positive seam topology

Exactly one positive semantic function:

`D1' OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_DERIVATION`

Exactly five constitutional mechanism-rule classes:

```text
P1 MATERIAL_ACCESS_DEPENDENCY
P2 DIRECTED_AUTHORITY_OBLIGATION_SANCTION
P3 ORGANIZED_ACTIVITY_TIME
P4 INSTITUTIONAL_GATE_TREATMENT
P5 COUNTERPART_CHANNEL_RELATION
```

No D2, D3, D4 or P6 is created.

---

## 3. Normative record topology

The smallest companion record set is:

```text
MECHANISM_RULE_RECORD
RULE_APPLICATION_RECORD
OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD
EVIDENCE_WITNESS_RECORD
```

with reusable embedded blocks equivalent to:

```text
ACTOR_POSITION_CONTEXT_TIME_BINDING_BLOCK
TEMPORAL_VALIDITY_BLOCK
DERIVATION_PROVENANCE_BLOCK
```

No physical storage/module architecture is implied.

---

## 4. Proof grammar

Every proposition is governed by an assertion kind plus orthogonal axes:

```text
ASSERTION_KIND
  K1 CONSTITUTIVE_POSITIONAL
  K2 QUALIFIED_POSSIBILITY
  K3 REALIZED_OCCURRENCE
  K4 ACTIVE_DURATIVE

POLARITY
  POSITIVE | NEGATIVE

CURRENTNESS
  CURRENT | HISTORICAL_NONCURRENT

MODALITY
  ACTUAL | PROJECTED_COUNTERFACTUAL

PROOF_ADJUDICATION
  PROVEN | UNKNOWN_NOT_PROVEN
```

`UNKNOWN_NOT_PROVEN` is a no-fact adjudication result, never an objective social state of the actor.

Bare `ACTIVE` remains a frozen-R4 umbrella current/operative descriptor and is not K4-exclusive.

---

## 5. Assertion-kind proof law

### K1 CONSTITUTIVE_POSITIONAL

A K1 fact may be proved by a competent operative source-owned rule/state plus exact actor/position/context binding and current validity over the asserted interval.

Examples include entitlement, eligibility, obligation, authority scope, restriction and other rule-constituted relations.

K1 does not prove exercise, use, performance, receipt or enforcement unless those propositions are separately established.

### K2 QUALIFIED_POSSIBILITY

A K2 fact requires an admitted objective possibility/route/channel/gate plus exact actor applicability/reachability.

K2 does not promote to K3 or K4 by itself.

### K3 REALIZED_OCCURRENCE

A K3 fact requires exact type-compatible competent actor/context/time evidence of the contingent occurrence, decision, treatment, transfer, exercise, contact, attendance or other realized event/process step asserted.

### K4 ACTIVE_DURATIVE

A K4 fact requires one of two lawful proof paths.

Path A:

A competent current/interval witness directly covers the asserted interval and required freshness/recurrence semantics.

Path B:

```text
COMPETENT OWNER SEMANTICS DECLARE A CONTINUING STATE
+
TYPE-COMPATIBLE STATE SUPPORT HAS A LAWFULLY SUPPORTABLE VALIDITY INTERVAL
OVERLAPPING THE ASSERTED/QUERIED INTERVAL
+
COMPLETE AUTHORITATIVE TERMINATION / SUPERSESSION /
INVALIDATION COVERAGE THROUGH QUERY TIME
+
NO DEFEATING CLOSING FACT.
```

A point-in-time establishment event remains historical evidence; it is not itself made current by silence.

If Path B cannot establish overlapping continuing-state support, result = `UNKNOWN_NOT_PROVEN`.

---

## 6. Negation and unknown law

Binding:

```text
FAILED POSITIVE PROOF != NEGATIVE PROOF
NO RECORD != NEGATIVE FACT
STALE POSITIVE != NEGATIVE FACT
EXPIRED POSITIVE != NEGATIVE FACT
TERMINATION OF P != OPPOSITE(P)
UNKNOWN_NOT_PROVEN != ACTOR FACT
```

Negative truth requires:

1. explicit competent negative evidence; or
2. explicit competent denial/rejection/termination/non-occurrence evidence proving the exact proposition; or
3. exact provenance-bearing rule-authorized closed-world semantics with proved completeness at actor/context/type/time/channel grain.

Otherwise no negative fact is emitted.

---

## 7. Currentness firewall

Always preserve:

```text
CURRENT(D1' CONSTITUTION)
!= CURRENT(MECHANISM RULE)
!= CURRENT(RULE APPLICATION)
!= CURRENT(CONSEQUENCE FACT)
!= CURRENT(WITNESS/STATE SUPPORT)
```

Semantic adoption authorizes zero concrete rules and zero actor facts automatically.

---

## 8. Derivation / invalidation / replay law

Every current derived D1' fact must be addressable through:

```text
EXACT DIRECT DETERMINANT(S)
-> EXACT RULE_APPLICATION_ID / RULE_VERSION
-> DERIVED CONSEQUENCE FACT
```

Direct determinants include exact source facts, bindings, witness/state support and rule/configuration versions required by the rule.

Reverse dependency discoverability is mandatory.

When a determinant changes:

```text
identify affected applications
-> reevaluate only those exact contracts
-> close/invalidate unsupported outputs
-> propagate only through dependent derived facts
-> rerun only newly/currently applicable rules
-> preserve unrelated facts and historical provenance.
```

No global actor reset.

---

## 9. Cycle / iteration law

Default:

```text
NO D1' FACT AT THE SAME WORLD/STATE VERSION AND VALID-TIME SLICE
MAY BE ITS OWN ANCESTOR.
```

Lawful iterative processes must advance through time/state/source version/new external fact/new witness or explicit competent iteration/fixed-point authority.

No generic cumulative scalar or solver is created.

---

## 10. Evidence / authority ceiling law

A derived fact may not become stronger through composition than the exact governed rule and required determinant/witness authorities permit.

Preserve separately where relevant:

- causal-use authority;
- identification strength;
- calibration authority;
- portability scope;
- historical/institutional validity;
- currentness/coverage.

`SOURCE CITATION != CAUSAL-USE AUTHORITY`.

---

## 11. Source -> mechanism -> rule traceability law

Every future concrete executable D1' rule requires an auditable trace equivalent to:

```text
SOURCE / CLAIM
-> CLAIM & EVIDENCE STATUS
-> NORMALIZED MECHANISM
-> P1-P5 CLASS OR COMPOSITION
-> PERMITTED RULE SHAPE
-> REQUIRED OBJECTIVE INPUTS/BINDINGS
-> QUALIFICATION/REALIZATION PROOF CONTRACT
-> TEMPORAL/CURRENTNESS CONTRACT
-> PORTABILITY/BOUNDARY CONDITIONS
-> NEGATIVE CEILING
-> V3 STOP BOUNDARY
-> COMPETENT CAUSAL-USE AUTHORITY
-> CALIBRATION AUTHORITY IF NUMERIC.
```

Source evidence can ground rule shape and ceilings without automatically licensing executable use.

Source/theory constructs do not automatically become runtime fact types or operators.

---

## 12. PRE-V3 / V3 firewall

D1' may emit only objective positioned social/world consequences.

It must not emit or infer:

```text
SUBJECTIVE PREMISE
REASON / GROUND
APPRAISAL / UPTAKE
MOTIVE / BELIEF
DISTRESS / MASTERY / PERCEIVED SUPPORT
MEMORY / LEARNING
CAPACITY / TRAIT
DURABLE DEVELOPMENT
```

Private V3 state may not directly author objective-social history.

Person action may affect later D1' facts only through externalized occurrence, competent counterpart/world response, competent source authorship/admission and ordinary invalidation/rederivation.

---

## 13. Temporal-form integrity / OBL062

Preserve distinct objective temporal forms:

```text
EVENT
CONDITION
DIRECTED_RELATION
RECURRENT_ACTIVITY
TRANSITION
ORDERED_HISTORY
```

A lawful non-event D1' fact may exist even when its generic V3 ingress route is unresolved.

Expected status remains:

`NON_EVENT_INGRESS_OPEN`

where applicable.

Never manufacture an event merely to obtain V3 ingress.

OBL062 remains open.

---

## 14. Canonical semantic conformance baseline

Preserve S5 immutable baseline:

`8ad68cd5731db6a4c4c75f5cc1bddbf95018f882`

comprising:

```text
90 canonical semantic vectors
30 metamorphic relations
```

Augment companion conformance with explicit K4 Path-B cases:

1. owner-declared continuing state + supportable interval overlap + complete closure coverage + no closing fact -> K4 may remain current;
2. old establishment event + silence only -> `UNKNOWN_NOT_PROVEN`;
3. owner persistence semantics but incomplete termination/supersession coverage -> `UNKNOWN_NOT_PROVEN`;
4. historical event token alone must not be relabeled current;
5. bare ACTIVE applied to current K1 must not force reclassification to K4.

No frozen S5 vector is deleted.

---

## 15. Terminology firewall

Critical noncollapses include:

```text
ACTIVE [umbrella current/operative adjective] != K4 ACTIVE_DURATIVE
K1 CURRENT OPERATIVE OBLIGATION != OBLIGATION PERFORMANCE
ELIGIBLE != APPLIED
ENTITLED != RECEIVED
AUTHORITY SCOPE != AUTHORITY EXERCISED
CHANNEL EXISTS != CONTACT != TRANSFER != PERCEIVED SUPPORT
ROLE/TITLE != POSITION/RELATION/SCOPE/ACTIVITY
OBJECTIVE STRAIN/BURDEN != FELT STRAIN
STRUCTURAL POSSIBILITY != SUBJECTIVE PREMISE
CURRENT FACT != HISTORICAL FACT
ACTUAL != PROJECTED_COUNTERFACTUAL
UNKNOWN_NOT_PROVEN != NEGATIVE
```

---

## 16. Final companion status

The full companion package is now internally reviewed and narrowed.

It changes no R4 topology and creates no new semantic owner.

No additional broad theory/source/specification review is warranted by the campaign unless HQ or implementation work later exposes a concrete contradiction.

HQ may consider frozen R4 together with this reviewed companion package as the semantic/specification basis for adoption.

---

## Final terminal

`R4_SEAM_COMPANION_SPECIFICATION_FINAL_R2__FINAL_REVIEW_CONSUMED__K4_OVERLAP_AND_ACTIVE_TERMINOLOGY_NARROWINGS_APPLIED__D1_PRIME_P1_P5_UNCHANGED__NO_D2_D3_D4_P6__OBL062_OPEN__READY_FOR_HQ_CONSIDERATION__NOT_ADOPTED`
