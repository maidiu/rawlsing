# SDTF R4 S1 — RETURN TO VOZHD R1

TERMINAL STATUS: `PASS__S1_R4_SEAM_NORMATIVE_SCHEMA_READY_FOR_VOZHD_RECONCILIATION`

WORKER BRANCH: `agent/rabochii-sdtf-r1-r4-s1-seam-normative-schema`

INHERITED COORDINATOR STATE: `02d4a75c030ed22da48b64718618242fc10ad858`

FROZEN R4 SEMANTIC CANDIDATE: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

No HQ adoption performed. No production runtime implemented. No S2-S5 returns inspected. R4 candidate not altered.

---

## 1. Products

```text
S1_R4_SEAM_NORMATIVE_CONTRACT_R1.md
S1_R4_RECORD_AND_FIELD_SCHEMA_R1.md
S1_R4_PREV3_V3_BOUNDARY_CONFORMANCE_R1.md
S1_R4_SCHEMA_SCENARIO_COURT_R1.md
S1_R4_OVERBUILD_AND_UNDERBUILD_AUDIT_R1.md
S1_RETURN_TO_VOZHD_R1.md
```

---

## 2. Normative record set

Smallest top-level set:

```text
1. MECHANISM_RULE_RECORD
2. RULE_APPLICATION_RECORD
3. OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD
4. EVIDENCE_WITNESS_RECORD
```

Required embedded normative blocks:

```text
A. ACTOR_POSITION_CONTEXT_TIME_BINDING_BLOCK
B. TEMPORAL_VALIDITY_BLOCK
C. DERIVATION_PROVENANCE_BLOCK
```

The following suggested families are therefore not separate top-level records:

```text
ACTOR_POSITION_CONTEXT_BINDING        -> embedded in RULE_APPLICATION_RECORD
NEGATIVE_WITNESS/CLOSED_WORLD_RECORD  -> unified under EVIDENCE_WITNESS_RECORD polarity/authority
TEMPORAL_VALIDITY_BINDING             -> reusable block
DERIVATION_PROVENANCE_RECORD          -> reusable block in application/consequence
```

This is the smallest record topology found that preserves all R4 distinctions.

---

## 3. Required field set

### `MECHANISM_RULE_RECORD`

```text
RULE_ID
RULE_VERSION
COMPETENT_OWNER_OR_AUTHORITY_REF
MECHANISM_CLASS
ALLOWED_INPUT_TYPES
REQUIRED_BINDINGS
OUTPUT_CONSEQUENCE_TYPES
QUALIFICATION_OR_APPLICABILITY_LAW
REALIZATION_WITNESS_SCHEMA
TEMPORAL_OR_LIFECYCLE_REQUIREMENTS
CONTEXT_INSTITUTION_HISTORICAL_VALIDITY
BOUNDARY_CONDITIONS
SOURCE_OR_CLAIM_STATUS
PORTABILITY_SCOPE
CALIBRATION_STATUS_IF_ANY
NEGATIVE_CEILING
```

Conditional when applicable:

```text
INSTITUTIONAL_CONFIGURATION_REQUIREMENT
CLOSED_WORLD_NEGATION_AUTHORITY
RECURRENCE_OR_FRESHNESS_REQUIREMENT
```

No universal extra `INPUT_FACT_SCHEMA_REF`, `SEMANTIC_BINDING_AUTHORITY_REF`, or `CAUSAL_USE_AUTHORITY_REF` is required as a distinct field. Their semantics become mandatory at G6 when a concrete rule uses a nonidentity source/runtime mapping or requires separate causal-use admission.

### `RULE_APPLICATION_RECORD`

```text
RULE_APPLICATION_ID
MECHANISM_RULE_REF
ACTOR_REF
WORLD_REF
CONTEXT_REF(S)
POSITION_REF(S)
VALID_TIME_OR_INTERVAL
DIRECT_ANTECEDENT_FACT_REF(S)
QUALIFICATION_RESULT
DERIVATION_PROVENANCE
```

Conditional:

```text
COUNTERPART_OR_INSTITUTION_REF(S)
OBJECTIVE_SOCIAL_HISTORY_REF(S)
INSTITUTIONAL_CONFIGURATION_REF(S)
EXTERNAL_ACTION_OCCURRENCE_REF(S) only after competent external admission
CLOSED_WORLD_SCOPE_REF when negative closed-world semantics are used
```

### `OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD`

Required semantic information:

```text
CONSEQUENCE_ID
ACTOR_REF
WORLD_REF
CONTEXT_REF(S)
POSITION_REF(S)
VALID_TIME_OR_INTERVAL
CONSEQUENCE_TYPE
CONSEQUENCE_VALUE_OR_STATE
MECHANISM_RULE_REF(S)
QUALIFICATION_OR_REALIZATION_STATUS
POLARITY
TEMPORAL_FORM
DERIVATION_PROVENANCE
BOUNDARY_CONDITIONS
EVIDENCE_CEILING
NEGATIVE_CEILING
```

Required when applicable/resolvable by reference:

```text
MECHANISM_CLASS(ES)
STRUCTURAL_OR_WORLD_SOURCE_REF(S)
REALIZATION_WITNESS_REF(S) for ACTIVE/REALIZED
COUNTERPART_OR_INSTITUTION_REF(S)
OBJECTIVE_SOCIAL_HISTORY_REF(S)
INSTITUTIONAL_CONFIGURATION_REF(S)
SUPERSEDES_OR_INVALIDATES_REF(S)
```

The class/source/ceiling material need not be physically duplicated if exactly resolvable through immutable rule/application/provenance references.

### `EVIDENCE_WITNESS_RECORD`

```text
WITNESS_ID
WITNESS_TYPE
WITNESS_POLARITY
COMPETENT_SOURCE_OR_OWNER
SUPPORTED_CONSEQUENCE_TYPE(S)
VALIDITY_OR_EVENT_TIME
ASSERTED_CONSEQUENCE_INTERVAL
SUPERSESSION_TERMINATION_INVALIDATION_STATE
```

Conditional:

```text
CURRENTNESS_OR_FRESHNESS_REQUIREMENT
RECURRENCE_COVERAGE
GAP_OR_TERMINATION_HANDLING
CLOSED_WORLD_SCOPE
CLOSED_WORLD_COMPLETENESS_AUTHORITY_REF
CONSTITUTIVE_STATE_REF
```

---

## 4. Status and polarity contract

One normalized consequence status field is sufficient:

```text
QUALIFIED_ONLY
CONSTITUTIVELY_TRUE
ACTIVE
REALIZED
UNKNOWN
NOT_PROVEN_REALIZED
```

`POLARITY = POSITIVE | NEGATIVE` applies only to asserted truth. `UNKNOWN` and `NOT_PROVEN_REALIZED` are not negative facts.

This makes qualification, constitutive truth, active current state, contingent realization, and underproof distinguishable without creating a new owner/status ontology.

---

## 5. Currentness verdict

`PASS`.

The normative contract requires independent predicates:

```text
CURRENT(D1'_CONSTITUTION,t)
!= CURRENT(MECHANISM_RULE,t)
!= CURRENT(RULE_APPLICATION,t)
!= CURRENT(CONSEQUENCE_FACT,t)
!= CURRENT(WITNESS,t)
```

Semantic adoption of D1' automatically authorizes zero mechanism rules, zero rule applications, zero actor facts and zero realization witnesses.

A current rule cannot extend a stale witness. A current application cannot by itself keep a fact current. A historical witness may remain provenance without supporting present truth.

---

## 6. PRE-V3/V3 boundary verdict

`PASS__OBJECTIVE_FACT_ONLY`.

No required field admits or emits:

```text
SUBJECTIVE PREMISE
REASON
GROUND
APPRAISAL
MOTIVE
BELIEF
KNOWLEDGE
DISTRESS
MASTERY
PERCEIVED SUPPORT
MEMORY
LEARNING
CAPACITY CHANGE
TRAIT
DURABLE DEVELOPMENT
```

Private V3 state cannot enter objective-social history directly. It may matter only after externalized action and competent world/source admission.

No direct person/V3 -> structure write is authorized.

---

## 7. Non-event ingress verdict

`PASS__NON_EVENT_FACTS_PRESERVED__OBL062_REMAINS_OPEN`.

Every consequence preserves exactly one temporal form:

```text
EVENT
CONDITION
DIRECTED_RELATION
RECURRENT_ACTIVITY
TRANSITION
ORDERED_HISTORY
```

A lawful non-event D1' fact may exist while downstream V3 ingress is unproved. S1 does not fabricate events and does not claim to solve OBL062.

No universal `V3_INGRESS_STATUS` or `V3_TARGET_OWNER` field is required; adding one at seam grain risks D4 creep. Routing remains downstream.

---

## 8. Negation/witness verdict

`PASS`.

For every `ACTIVE` or `REALIZED` assertion, type-compatible competent evidence must overlap the asserted interval and satisfy freshness/coverage/supersession rules.

Missing, expired, superseded, terminated, invalidated or insufficiently current positive evidence yields:

```text
UNKNOWN
or
NOT_PROVEN_REALIZED
```

never a negative fact.

Negative truth requires:

```text
EXPLICIT COMPETENT NEGATIVE WITNESS
or
EXPLICIT DENIAL/TERMINATION/NON-OCCURRENCE WITNESS
or
PROVENANCE-BEARING RULE-AUTHORIZED CLOSED-WORLD NEGATIVE SEMANTICS.
```

---

## 9. Overbuild verdict

`PASS__NO_GENERIC_DATA_MODEL_OVERBUILD`.

Rejected as universal constitutional requirements:

```text
separate binding record
separate negative-witness family
separate temporal-validity record
separate provenance record
currentness cache booleans
V3 ingress routing field
V3 target owner field
executable formula field
derivation depth counter
replay queue/index fields
physical DAG representation
database normalization choices
serializer/transport fields
source adapter fields
runtime host/module choice
```

These are either redundant or `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

---

## 10. Underbuild verdict

No missing information requires a topology change.

The smallest companion-spec hardenings needed to make R4 mechanically difficult to violate are:

```text
EXACT DIRECT ANTECEDENT REFS AT APPLICATION/PROVENANCE GRAIN
EXPLICIT POLARITY
ONE NORMALIZED QUALIFICATION/CONSTITUTIVE/ACTIVE/REALIZED/UNKNOWN STATUS
INDEPENDENT CURRENTNESS PREDICATES
FORM-PRESERVING SIX-WAY TEMPORAL TYPE
```

These are extractions of existing R4 truth/provenance requirements, not new D-lanes or primitives.

---

## 11. R4 topology verdict

```text
D1' OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_DERIVATION: UNCHANGED
P1 MATERIAL_ACCESS_DEPENDENCY: UNCHANGED
P2 DIRECTED_AUTHORITY_OBLIGATION_SANCTION: UNCHANGED
P3 ORGANIZED_ACTIVITY_TIME: UNCHANGED
P4 INSTITUTIONAL_GATE_TREATMENT: UNCHANGED
P5 COUNTERPART_CHANNEL_RELATION: UNCHANGED
D2: NOT REQUIRED
D3: NOT REQUIRED
D4: NOT REQUIRED
P6: NOT REQUIRED
```

`R4 TOPOLOGY VERDICT: PASS__NO_CHANGE`.

---

## 12. Exact required companion specification

Recommend Vozhd reconcile S1 as one bounded normative companion specification with this exact semantic identity:

`OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_SEAM_CONTRACT@1.0.0-S1.R1`

Its minimum contents are:

```text
FOUR TOP-LEVEL RECORD FAMILIES
  MECHANISM_RULE_RECORD
  RULE_APPLICATION_RECORD
  OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD
  EVIDENCE_WITNESS_RECORD

THREE REQUIRED EMBEDDED BLOCKS
  ACTOR_POSITION_CONTEXT_TIME_BINDING_BLOCK
  TEMPORAL_VALIDITY_BLOCK
  DERIVATION_PROVENANCE_BLOCK

HARD INVARIANTS
  RULE CLASS != RULE AUTHORITY
  RULE CURRENT != APPLICATION CURRENT != FACT CURRENT != WITNESS CURRENT
  QUALIFICATION != CONSTITUTIVE TRUTH != ACTIVE STATE != CONTINGENT REALIZATION
  MISSING POSITIVE EVIDENCE != NEGATIVE TRUTH
  DIRECT ANTECEDENTS MUST BE PROVENANCE-ADDRESSABLE
  PRIVATE V3 STATE CANNOT BE OBJECTIVE-SOCIAL INPUT
  D1' OUTPUT CANNOT CONTAIN PERSON-SIDE SEMANTICS
  PERSON ACTION CANNOT WRITE STRUCTURE DIRECTLY
  EVENT != CONDITION != RELATION != RECURRENT ACTIVITY != TRANSITION != ORDERED HISTORY
  NON-EVENT D1' FACT MAY EXIST WHILE OBL062 INGRESS REMAINS OPEN
  P1-P5 ARE RULE CLASSES ONLY
  NO D2 / D3 / D4 / P6
```

No additional universal record family or field is required at S1 semantic grain.

---

## 13. Exact blocker if any

`NONE`.

Open G1-G6 and OBL062 are downstream governance/implementation/interface dependencies, not blockers to this S1 normative schema extraction.

---

## Return terminal

`PASS__S1_R4_SEAM_NORMATIVE_SCHEMA_READY_FOR_VOZHD_RECONCILIATION`.
