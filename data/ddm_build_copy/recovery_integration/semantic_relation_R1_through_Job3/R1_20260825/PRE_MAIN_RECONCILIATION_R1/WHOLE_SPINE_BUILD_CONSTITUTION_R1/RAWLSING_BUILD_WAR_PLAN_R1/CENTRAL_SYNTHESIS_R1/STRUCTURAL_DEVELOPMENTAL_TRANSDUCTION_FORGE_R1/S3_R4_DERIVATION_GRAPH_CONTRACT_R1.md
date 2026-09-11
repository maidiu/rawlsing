# S3 R4 DERIVATION GRAPH CONTRACT R1

STATUS: `D1_PRIME_DERIVATION_GRAPH_CONTRACT_SPECIFIED__NO_RUNTIME_IMPLEMENTED`

CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`

WORKER: `agent/rabochii-sdtf-r1-r4-s3-derivation-invalidation-replay`

COORDINATOR START: `02d4a75c030ed22da48b64718618242fc10ad858`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

GOVERNING SEMANTIC TARGET: `OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_DERIVATION_CONSTITUTION@1.0.0-CANDIDATE.R4`

This product specifies only the G2 derivation/provenance/replay semantics required to keep D1' safe under changing objective PRE-V3/world conditions. It creates no runtime, D2, D3, D4, P6, V3 ingress solution, or world-writing authority.

---

## 1. Problem

D1' permits chains of governed objective derivation:

```text
OBJECTIVE SOURCE/WORLD FACT
+ ACTOR/POSITION/CONTEXT/TIME BINDING
+ GOVERNED MECHANISM RULE
+ TYPE-COMPATIBLE WITNESS WHEN REQUIRED
-> OBJECTIVE POSITIONED SOCIAL CONSEQUENCE
```

Once consequences can feed later governed D1' applications, broad `DERIVATION_PROVENANCE` is not sufficient unless it can answer two operationally precise semantic questions:

```text
WHY DOES THIS FACT EXIST RIGHT NOW?
WHAT EXACT CURRENT DETERMINANT CHANGE WOULD MAKE IT CEASE TO BE CURRENT?
```

The minimum graph therefore records direct truth-determining dependency, not merely documentary ancestry.

---

## 2. Minimum graph objects

The semantic graph needs only two logical object kinds. Physical storage may reuse existing project carriers.

### 2.1 FACT NODE

A current or historical objective fact already authorized by a competent owner, including source/world facts and D1'-derived facts.

A D1'-derived fact must retain its ordinary R4 output contract plus a reference to its producing rule application.

Minimum derived-fact lifecycle fields:

```text
DERIVED_FACT_REF
PRODUCING_RULE_APPLICATION_ID
VALID_FROM
VALID_TO_OR_CURRENT_STATUS
QUALIFICATION_OR_REALIZATION_STATUS
EVIDENCE_CEILING
SUPERSEDES_REF(S) only when replacement semantics actually applies
```

### 2.2 RULE-APPLICATION NODE

One governed application of one exact rule version to one exact bound determinant set.

Minimum contract:

```text
RULE_APPLICATION_ID
MECHANISM_RULE_REF
RULE_VERSION_OR_IMMUTABLE_RULE_REF
DERIVED_FACT_REF(S)
DIRECT_DETERMINANT_REF(S)
DIRECT_DETERMINANT_ROLE(S)
ACTOR_REF
POSITION_REF(S) when required
CONTEXT_REF(S)
WORLD_REF
VALID_TIME_OR_INTERVAL
COUNTERPART_OR_INSTITUTION_REF(S) when determinant
REALIZATION_WITNESS_REF(S) when required for asserted status
INSTITUTIONAL_CONFIGURATION_REF(S) when constitutive
EVIDENCE_CEILING
APPLICATION_CURRENTNESS_STATUS
```

`DIRECT_DETERMINANT_ROLE` distinguishes why a referenced fact is truth-determining, for example:

```text
SOURCE_STATE
POSITION_BINDING
CONTEXT_BINDING
COUNTERPART_RELATION
INSTITUTIONAL_CONFIGURATION
OBJECTIVE_HISTORY
REALIZATION_WITNESS
RULE_CURRENTNESS
```

This typing is necessary so documentary citations or explanatory notes do not accidentally become invalidation determinants.

---

## 3. Direct antecedent law

Every D1' fact must have a finite set of **direct determinants** sufficient to reconstruct the immediate derivation step.

Binding:

```text
DERIVED_FACT CURRENT
ONLY IF
  PRODUCING RULE APPLICATION CURRENT
  AND EXACT RULE VERSION CURRENT FOR THE ASSERTED INTERVAL
  AND ALL REQUIRED DIRECT DETERMINANTS CURRENT/APPLICABLE
  AND ALL REQUIRED WITNESSES VALID FOR THE ASSERTED INTERVAL
  AND NO COMPETENT SUPERSESSION/TERMINATION/NEGATIVE FACT DEFEATS IT.
```

A generic provenance blob passes only if it is structurally queryable at this grain. An opaque citation bundle or prose lineage fails.

### Minimum answer to “why does this fact exist right now?”

The seam must be able to return:

```text
THIS FACT
was produced by THIS EXACT RULE APPLICATION
of THIS EXACT RULE VERSION
for THIS ACTOR/POSITION/CONTEXT/TIME
from THESE DIRECT TRUTH-DETERMINING FACTS/BINDINGS
with THESE REQUIRED CURRENT WITNESSES
under THIS EVIDENCE CEILING.
```

Nothing stronger is required by S3.

---

## 4. Adjudication of proposed provenance fields

### Required

```text
RULE_APPLICATION_ID
DERIVED_FACT_REF
DIRECT_ANTECEDENT_FACT_REF(S) / DIRECT_DETERMINANT_REF(S)
MECHANISM_RULE_REF + exact version identity
ACTOR/POSITION/CONTEXT/WORLD binding refs as applicable
VALID_TIME_OR_INTERVAL
REALIZATION_WITNESS_REF(S) when required
EVIDENCE_CEILING
```

### Conditionally required

```text
DIRECT_SOURCE_REF(S)
```

Required only when the source-owned fact is a direct determinant not already represented by a resolvable antecedent fact ref.

```text
SUPERSEDES_REF(S)
```

Required only when the new fact/rule treatment explicitly replaces a prior fact rather than merely coexisting or terminating independently.

```text
INSTITUTIONAL_CONFIGURATION_REF(S)
COUNTERPART_OR_INSTITUTION_REF(S)
OBJECTIVE_SOCIAL_HISTORY_REF(S)
```

Required exactly when the rule makes them determinants.

### Not independently required

```text
PARENT_DERIVATION_STEP_REF(S)
DERIVATION_DEPTH
FREE-STANDING_INVALIDATION_KEY(S)
```

Reason: if every derived antecedent resolves to its own `PRODUCING_RULE_APPLICATION_ID`, ancestry is traversable without a duplicate parent-step field or stored depth. Likewise, the determinant refs themselves are the canonical invalidation keys. Implementations may maintain reverse indices/cache keys, but S3 does not constitutionalize a second semantic identifier layer.

---

## 5. Determinant graph and reverse discoverability

The logical graph is bipartite:

```text
FACT/BINDING/WITNESS/RULE-VERSION DETERMINANT
              ↓
       RULE APPLICATION
              ↓
         DERIVED FACT
```

A derived fact may become a determinant of a later rule application, yielding a directed acyclic derivation chain by default.

For invalidation, the system must be able to discover the reverse relation:

```text
DETERMINANT REF
-> ALL CURRENT RULE APPLICATIONS THAT DIRECTLY DEPEND ON IT
-> THEIR DERIVED FACTS
```

This is a semantic discoverability requirement, not a demand for a particular graph database or reverse-index implementation.

---

## 6. Provenance versus dependency

Not every provenance item is an invalidation dependency.

Examples:

```text
SOURCE CITATION supporting why a rule was admitted
!= current actor-fact determinant

THEORY CARD
!= actor-fact determinant

COMMENTARY / explanation
!= actor-fact determinant
```

By contrast:

```text
current job-position fact
current service-capacity state
current counterpart relation
current gate treatment
current realization witness
exact rule version/currentness
```

are determinants when the producing rule requires them.

This distinction prevents both stale facts and needless recomputation.

---

## 7. Historical preservation law

Invalidation never erases lawful historical truth.

A determinant change may cause a D1' fact to cease being current from a boundary time while retaining:

```text
prior validity interval
producing application identity
prior determinants
prior witness state
termination/supersession cause
replacement derivation if any
```

Thus replay creates a before/after chain rather than rewriting history.

---

## 8. Scope and topology verdict

This graph is companion infrastructure semantics for D1'; it does not enlarge D1'.

```text
D1'            UNCHANGED
P1-P5          UNCHANGED
D2 OWNER       NOT CREATED
D3 OWNER       NOT CREATED
D4 / P6        NOT CREATED
OBL062         UNTOUCHED
V3 PRIVATE STATE AS D1' DETERMINANT  FORBIDDEN
DIRECT V3/WORLD WRITE                FORBIDDEN
```

S3 verdict:

`MINIMUM_GRAPH = DIRECT_DETERMINANTS + EXACT_RULE_APPLICATION_IDENTITY + DERIVED_FACT_IDENTITY + CURRENTNESS/TIME + REQUIRED_WITNESS + EVIDENCE_CEILING + REVERSE_DEPENDENCY_DISCOVERABILITY`.
