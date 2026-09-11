# R4 COMPANION FINAL REVIEW — NEGATION / DERIVATION COURT R1

STATUS: `PASS__NEGATION_FAILS_CLOSED__DETERMINANT_SCOPED_REPLAY_CYCLE_AND_EVIDENCE_CEILING_SOUND`

FROZEN R4: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

FROZEN COMPANION: `d5c92b09549b52aace9e1384c1b11955d947f5a7`

## 1. Negation governing law

The companion correctly preserves the R4 polarity firewall:

```text
FAIL(POSITIVE_PROOF)
!= PROVE(NEGATIVE)

MISSING RECORD
!= DENIAL

EXPIRED/SUPERSEDED/INVALIDATED POSITIVE WITNESS
!= NEGATIVE FACT

TERMINATED PRIOR FACT
!= OPPOSITE FACT
```

A negative actor proposition may be authored only from:

1. explicit competent negative evidence;
2. an explicit competent denial/rejection/termination/non-occurrence witness whose semantics prove the exact negative proposition; or
3. an exact rule-authorized closed-world inference with provenance-bearing completeness semantics.

Anything less produces `UNKNOWN_NOT_PROVEN`, which remains a non-fact.

## 2. Closed-world counterfeit court

For every absence-based negative the companion requires the right minimum protections:

```text
COMPETENT OWNER
EXACT PROPOSITION/GRAIN
COMPLETE OBSERVATION UNIVERSE
MANDATORY POSITIVE RECORDING
FULL TEMPORAL COVERAGE
REPORTING/RECONCILIATION/LATENCY CLOSURE
IDENTITY INTEGRITY
CHANNEL/SOURCE SCOPE COMPLETENESS
NO COVERAGE/SOURCE-HEALTH GAP
CURRENT COMPLETENESS/RULE VERSION
EXPLICIT ABSENCE-TO-NEGATIVE AUTHORIZATION
PROVENANCE
```

### No payment record

Ordinary result: `UNKNOWN_NOT_PROVEN`.

A negative is lawful only in an exact authoritative exhaustive payment universe for the claimed payment type/actor/period, after reconciliation closure, with alternate channels included or the proposition explicitly source-scoped.

### No contact record

Ordinary result: `UNKNOWN_NOT_PROVEN`.

A relationship or channel cannot be negated because an incomplete contact log is silent.

### No gate-decision record

Ordinary result: `UNKNOWN_NOT_PROVEN`.

Only an exhaustive mandatory decision ledger at the exact gate/actor/window can support a source-bounded negative.

### No task/performance record

Ordinary result: `UNKNOWN_NOT_PROVEN`.

Schedule/assignment does not prove performance; silence does not prove nonperformance absent exhaustive performance authority.

### No command record

Ordinary result: `UNKNOWN_NOT_PROVEN`.

No-command can be proved only where all commands of the exact type are obligatorily and exhaustively recorded and no off-system channel defeats closure.

### No support record

Ordinary result: `UNKNOWN_NOT_PROVEN`.

Informal support ordinarily defeats closed-world completeness. A complete program ledger may prove only the narrower source-bounded proposition it owns.

`NEGATION/UNKNOWN VERDICT: PASS__ONLY_EXPLICIT_NEGATIVE_OR_EXACT_AUTHORIZED_CLOSED_WORLD_PROOF_CAN_AUTHOR_NEGATIVE_TRUTH`

## 3. Termination polarity court

A termination witness can prove:

```text
F was current before t, if historical proof remains valid
F is no longer current after t, under exact termination semantics
```

It does not prove:

```text
OPPOSITE(F) is current
F never existed
all related relations are absent
```

A terminated authority relation does not create the opposite authority relation. A terminated obligation does not prove a contrary duty. A closed channel does not prove no social relation exists.

Verdict: `PASS`.

## 4. Direct-determinant provenance

File 40's semantic requirement is justified by frozen R4 rather than merely by implementation convenience.

R4 requires determinant-scoped invalidation/rederivation after competent changes and preservation of exact before/after provenance. To obey that law the companion must be able to recover, for each current derived fact:

```text
PRODUCING RULE_APPLICATION_ID
EXACT MECHANISM_RULE_REF + VERSION
DIRECT_DETERMINANT_REF(S)
ACTOR/WORLD/CONTEXT/POSITION BINDINGS
VALID TIME/INTERVAL
REQUIRED WITNESS REF(S)
EFFECTIVE EVIDENCE CEILING
```

A prose citation bundle that cannot identify exact direct dependencies is insufficient.

What is not constitutionally required is any particular physical graph database, reverse index, cache, queue or traversal implementation.

`DERIVATION/INVALIDATION VERDICT: PASS__DIRECT_DEPENDENCY_IDENTITY_AND_REVERSE_DISCOVERABILITY_ARE_SEMANTIC_REQUIREMENTS__PHYSICAL_GRAPH_IS_NOT`

## 5. Invalidation/replay attacks

### Job termination

Changed position/employment determinants close or invalidate only facts that depend on them. Household, school and unrelated network facts survive unless they have their own changed determinant.

### Household relation change

Only applications directly depending on the changed household relation/obligation/task allocation are reevaluated. Work facts do not reset globally.

### Network relation termination

P5 reachability/channel facts and descendants are reevaluated. Material/property facts remain unless linked through explicit rule applications.

### Institutional-mark correction

The corrected mark invalidates only applications/descendants that consumed that mark. Prior gate treatment may remain historical if independently valid, or be corrected only under competent retroactive authority.

### Infrastructure restoration

Restored capacity invalidates/recomputes access constraints that depend on outage/capacity. It does not erase unrelated biography.

### Witness expiry

Current fact support is removed/reconsidered according to proof kind. Expiry alone creates no negative. Historical event truth survives only if historical evidence remains valid.

### Rule-version replacement

Applications depending on the replaced version are reevaluated prospectively or retroactively only according to competent rule/version authority. A new rule does not invent a contingent occurrence.

Verdict: `PASS__DETERMINANT_SCOPED_NOT_ACTOR_WIDE_RESET`.

## 6. Cycle court

Default companion law:

```text
NO D1'-DERIVED FACT
AT THE SAME WORLD/STATE VERSION AND VALID-TIME SLICE
MAY BE ITS OWN ANCESTOR.
```

This is sufficient as a default conformance law.

### Direct cycle

```text
A(t) -> B(t) -> A(t)
```

Rejected if the second A depends on the first A through the same factual state/time slice.

### Longer cycle

```text
A(t) -> B(t) -> C(t) -> A(t)
```

Rejected under the same ancestor test.

### Legitimate same-time constitutive chain

```text
SOURCE FACT A(t)
-> DERIVED B(t)
-> DERIVED C(t)
```

is lawful when acyclic. The anti-self-ancestry law does not reject it.

### Iteration over change

A later application may lawfully consume an earlier result when at least one competent semantic advancement exists, such as:

```text
NEW TIME/INTERVAL
NEW STATE/SOURCE VERSION
NEW EXTERNAL SOURCE-OWNED FACT
NEW COMPETENT WITNESS
EXPLICIT COMPETENT ITERATION/FIXED-POINT AUTHORITY
```

The companion creates no generic fixed-point or cumulative-process owner.

`CYCLE VERDICT: PASS__SAME_STATE_SELF_ANCESTRY_FORBIDDEN__ACYCLIC_CONSTITUTIVE_CHAINS_AND_GENUINE_STATE_ADVANCEMENT_PRESERVED`

## 7. Evidence-ceiling court

File 40 correctly prevents inference laundering. A derived fact cannot have stronger authority than the exact rule plus all truth-determining antecedents/witnesses permit.

Required interpretation:

```text
DERIVED EVIDENCE/AUTHORITY CEILING
<= RULE CAUSAL-USE AUTHORITY
AND
<= REQUIRED DETERMINANT/WITNESS AUTHORITY
```

with historical, contextual, institutional, portability, identification, currentness and calibration limitations preserved as a vector/conjunction, not falsely upgraded into one scalar confidence score.

Counterfeits rejected:

```text
OBSERVATIONAL ASSOCIATION -> RANDOMIZED CAUSAL CERTAINTY
SOURCE CITATION -> EXECUTABLE CAUSAL AUTHORITY
STALE WITNESS -> CURRENT FACT
GROUP RATE -> ACTOR OUTCOME
COMPOSITION -> STRONGER PORTABILITY THAN ANTECEDENTS
```

`EVIDENCE-CEILING VERDICT: PASS__NO_DERIVATION_STEP_MAY_STRENGTHEN_CAUSAL_CURRENTNESS_PORTABILITY_OR_CALIBRATION_AUTHORITY`

## 8. Required scenario replay — negation/derivation subset

### Scenario 9 — no callback, incomplete dataset

`UNKNOWN_NOT_PROVEN`. No denial/noncallback fact is authored.

### Scenario 10 — no callback, exact complete closed-world ledger

A negative at the exact callback proposition/grain is lawful only after mandatory recording, complete interval, reconciliation closure, exact identity/channel scope, healthy current source and explicit closed-world authorization are proved.

### Scenario 11 — explicit denial

Lawful negative at the exact denial proposition/grain; no subjective awareness/appraisal follows.

### Scenario 12 — terminated authority relation

Prior relation closes. Historical interval retained. Current opposite authority is not inferred.

### Scenario 13 — termination without opposite proof

Exactly demonstrates `NOT CURRENT(P) != CURRENT(OPPOSITE(P))`.

### Scenario 16 — private distress, no external action

No D1' determinant changes. Private V3 state cannot invalidate or author objective social facts.

### Scenario 17 — external household-task withdrawal

If withdrawal is externally admitted and exact household task/obligation rule applies, target actor's objective task/time consequence may change. Private motive/distress is not required or inferred.

### Scenario 18 — job exit, household facts preserved

Only descendants of changed work/position/resource determinants are reevaluated. Unrelated household facts persist under their own proof.

### Scenario 19 — upstream correction invalidates descendants only

Direct/reverse dependency identity gives the exact descendant cone. No global actor reset.

### Scenario 20 — same-state circular derivation

Rejected by no-self-ancestry law unless a separately competent iterative/fixed-point authority exists; none is created by the companion.

## 9. World-write regression

Nothing in replay permits:

```text
V3 PRIVATE STATE -> D1' WORLD FACT
V3 ACTION -> DIRECT STRUCTURAL MUTATION
D1' DERIVATION -> NEW EXTERNAL SOURCE TRUTH
```

Lawful reciprocal route remains:

```text
EXTERNALIZED ACTION
-> COMPETENT WORLD/INSTITUTION RESPONSE
-> COMPETENT SOURCE AUTHORS NEW EXTERNAL FACT
-> ORDINARY INVALIDATION/REDERIVATION
```

No D3 world writer is created.

## 10. Court terminal

```text
NEGATION/UNKNOWN: PASS
DERIVATION/INVALIDATION: PASS
CYCLE: PASS
EVIDENCE CEILING: PASS
```

No narrowing beyond the separate K4 Path B / `ACTIVE` corrections is required by this court.