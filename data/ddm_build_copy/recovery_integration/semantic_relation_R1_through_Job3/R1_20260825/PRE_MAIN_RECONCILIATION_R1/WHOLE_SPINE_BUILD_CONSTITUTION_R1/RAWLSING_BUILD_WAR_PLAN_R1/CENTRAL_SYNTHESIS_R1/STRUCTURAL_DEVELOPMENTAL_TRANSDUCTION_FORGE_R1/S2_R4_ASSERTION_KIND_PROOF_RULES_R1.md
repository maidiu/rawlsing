# S2 R4 ASSERTION KIND PROOF RULES R1

STATUS: `S2_R4_ASSERTION_KIND_PROOF_RULES_COMPLETE`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

## 1. Court question

R4 correctly hardened realization currentness and polarity after final R3 review. S2 asks whether one universal `ACTIVE/REALIZED -> overlapping realization witness` formula is, by itself, the minimum truth proof law for all seam assertions.

Verdict: **the polarity/currentness correction is binding, but proof must be scoped by assertion kind.** The same epistemic standard does not imply the same witness form.

## 2. K1 — CONSTITUTIVE_POSITIONAL proof law

A constitutive/deontic/positional proposition is true when the competent external rule/state itself makes it true for the exactly bound actor/position over the queried interval.

Required proof bundle:

```text
CURRENT COMPETENT CONSTITUTIVE RULE / SOURCE-OWNED STATE
+ EXACT ACTOR BINDING
+ EXACT POSITION / COUNTERPART / INSTITUTION BINDING WHEN REQUIRED
+ RULE APPLICABILITY AT QUERY TIME
+ RULE/STATE VALIDITY OVERLAPPING ASSERTED INTERVAL
+ NO DEFEATING SUPERSESSION / TERMINATION / INVALIDATION
= K1 CONSTITUTIVE_POSITIONAL FACT
```

No separate event occurrence is required merely to prove entitlement, authority scope, an operative duty, a valid restriction, or another proposition whose governing source/state constitutes the fact.

Binding ceilings:

```text
ENTITLED != RECEIVED
HAS AUTHORITY SCOPE != EXERCISED AUTHORITY
OWES DUTY != PERFORMED DUTY
VALID RESTRICTION != SANCTION IMPOSED
```

An operative source-owned relation/state may itself be the type-compatible witness. This preserves R4 §5.5.

## 3. K2 — QUALIFIED_POSSIBILITY proof law

A qualified possibility/applicability/reachability proposition is true only if an admitted structural/world possibility is lawfully bound to this actor's exact current position/context under a governed rule.

Required proof bundle:

```text
ADMITTED STRUCTURAL / SOCIAL / WORLD INPUT
+ CURRENT ACTOR / POSITION / CONTEXT / TIME BINDINGS
+ CURRENT GOVERNED MECHANISM RULE
+ APPLICABILITY / REACHABILITY / ELIGIBILITY CONDITIONS SATISFIED
+ VALIDITY / PROVENANCE
= K2 QUALIFIED_POSSIBILITY FACT
```

K2 does not need an occurrence witness because occurrence is not what K2 claims. It also does not authorize K3/K4 by implication.

Examples:

```text
ELIGIBLE != APPLIED
ROUTE AVAILABLE != ROUTE USED
CHANNEL AVAILABLE != TRANSFER
COUNTERPART REACHABLE != CONTACT
TASK OPPORTUNITY != TASK PERFORMANCE
```

## 4. K3 — REALIZED_OCCURRENCE proof law

A contingent occurrence/treatment/transfer/exercise/decision is true only from a type-compatible competent occurrence witness or equivalent competent source-owned event/state that proves the exact event claimed.

Required proof bundle:

```text
K1/K2 INPUTS WHERE RULE REQUIRES THEM
+ TYPE-COMPATIBLE COMPETENT OCCURRENCE / TREATMENT / TRANSFER WITNESS
+ ACTOR / COUNTERPART / INSTITUTION / CONTEXT / TIME MATCH
+ WITNESS VALIDITY AND PROVENANCE
+ NO INVALIDATION / SUPERSESSION OF THE EVENT CLAIM
= K3 REALIZED_OCCURRENCE FACT
```

A K3 event may remain historically true indefinitely as an event that occurred. That historical truth does not prove a resultant K4 condition is still current.

## 5. K4 — ACTIVE_DURATIVE proof law

A current state/relation/condition/recurrent-activity claim requires currentness proof at the exact interval asserted. S2 admits two lawful proof forms.

### K4-A direct-current witness

```text
TYPE-COMPATIBLE COMPETENT STATE / RELATION / ACTIVITY WITNESS
+ WITNESS VALIDITY OVERLAPS ASSERTED INTERVAL
+ REQUIRED RECURRENCE / FRESHNESS COVERAGE
+ NO TERMINATION / SUPERSESSION / INVALIDATION
= CURRENT K4
```

This is the direct reading of R4 §5.

### K4-B governed persistence-to-termination proof

A continuing state can also be current without a fresh observation at every instant when—and only when—the competent owner semantics make state persistence explicit.

Required proof bundle:

```text
COMPETENT ESTABLISHMENT / START WITNESS
+ GOVERNED STATE-PERSISTENCE SEMANTICS FOR THIS EXACT FACT TYPE
+ EXPLICIT TERMINATION / SUPERSESSION / INVALIDATION EVENT TYPES
+ AUTHORITATIVE CURRENTNESS CHECK OVER THE GOVERNED EVENT/STATE UNIVERSE
+ COMPLETE COVERAGE THROUGH QUERY TIME AT THAT EXACT GRAIN
+ NO COMPETENT CLOSING EVENT
= CURRENT K4
```

This is not ordinary absence-of-record reasoning. It is positive currentness proof from a governed persistent-state model whose event/state universe and closure semantics are authoritative at the exact grain.

If any completeness, coverage, owner, identity, or termination guarantee is absent, K4-B fails to `UNKNOWN_NOT_PROVEN`.

## 6. Universal witness law verdict

R4's final-review correction must not be weakened:

```text
RULE VALIDITY ALONE != CURRENT REALIZATION
STALE WITNESS != CURRENT FACT
MISSING WITNESS != NEGATIVE
SUPERSEDED WITNESS != CURRENT FACT
```

But the sentence `every ACTIVE/REALIZED assertion must cite a witness whose validity overlaps the asserted interval` is not sufficient as the entire S2 proof grammar.

### Too broad for constitutive/qualified facts if misread

K1 and K2 facts do not require occurrence-style realization witnesses. Their truth is proved by competent operative rules/states plus exact bindings/applicability. R4 §5.5 already partially recognizes this.

### Too narrow for some continuing states if read literally

A persistent externally governed relation/state can remain current from a competent establishment event plus authoritative persistence-to-termination semantics even when the initiating event witness is point-in-time and does not itself overlap the later query instant.

S2 therefore narrows the universal law to:

> **ASSERTION-KIND-SCOPED WITNESS / PROOF LAW.** Every positive or negative seam assertion must cite a type-compatible competent proof bundle for its assertion kind and exact asserted interval. K3 realized occurrences require competent occurrence proof. K4 current durative facts require either a direct overlapping current witness or a governed persistence-to-termination proof whose source universe and closing-event semantics are authoritative and complete at the exact grain. K1 constitutive facts and K2 qualifications use their separately governed operative-rule/state and applicability proof. In no case may rule validity, stale evidence, or ordinary missing records extend a realization or manufacture negative truth.

## 7. Negative proof is not merely failed positive proof

For every K1-K4 proposition:

```text
FAIL(POSITIVE_PROOF) -> UNKNOWN_NOT_PROVEN
```

unless a separately licensed negative proof succeeds.

Negative proof therefore requires its own competent witness/rule, as adjudicated in `S2_R4_NEGATION_AND_CLOSED_WORLD_COURT_R1.md`.

## 8. Conflicting evidence

When competent evidence conflicts and current authority does not supply a lawful precedence/supersession rule:

```text
CONFLICT != CHOOSE CONVENIENT FACT
CONFLICT != NEGATIVE
```

The exact claim remains `UNKNOWN_NOT_PROVEN` pending lawful adjudication. Historical versions may remain retained with provenance.

## 9. Proof-rule metadata requirement

Every governed D1' rule that can emit a fact must define the applicable proof contract, including where relevant:

```text
ASSERTION_KIND(S) AUTHORIZED
PROOF / WITNESS TYPE(S)
POLARITY AUTHORIZED
COMPETENT SOURCE / OWNER
VALIDITY / CURRENTNESS LAW
PERSISTENCE LAW IF ANY
TERMINATION / SUPERSESSION / INVALIDATION LAW
RECURRENCE / FRESHNESS COVERAGE
CLOSED-WORLD AUTHORIZATION IF ANY
BOUNDARY CONDITIONS
NEGATIVE CEILING
```

This is semantic specification, not runtime implementation.

## Terminal

`WITNESS_LAW_VALID_IN_INTENT_BUT_REQUIRES_ASSERTION_KIND_SCOPING__K4_MAY_USE_DIRECT_CURRENT_WITNESS_OR_STRICT_GOVERNED_PERSISTENCE_TO_TERMINATION__POLARITY_CURRENTNESS_CORRECTION_PRESERVED`
