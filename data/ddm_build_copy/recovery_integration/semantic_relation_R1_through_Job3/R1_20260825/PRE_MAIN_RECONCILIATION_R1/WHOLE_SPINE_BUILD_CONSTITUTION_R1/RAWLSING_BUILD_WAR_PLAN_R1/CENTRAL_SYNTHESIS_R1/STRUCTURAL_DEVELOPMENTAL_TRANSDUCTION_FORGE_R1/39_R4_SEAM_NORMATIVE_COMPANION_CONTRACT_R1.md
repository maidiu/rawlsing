# R4 SEAM NORMATIVE COMPANION CONTRACT R1

STATUS: `CANONICAL_COMPANION_SPECIFICATION__FROZEN_R4_TOPOLOGY_PRESERVED__NOT_HQ_ADOPTION__NO_RUNTIME_IMPLEMENTATION`

COMPANION IDENTITY:
`OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_SEAM_CONTRACT@1.0.0-CANDIDATE.R1`

GOVERNING SEMANTIC CANDIDATE:
`OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_DERIVATION_CONSTITUTION@1.0.0-CANDIDATE.R4`

FROZEN R4 COMMIT:
`dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

SOURCE RETURNS:
- S1 `4367e756e1473aa72c7f1b834fe5069e98ecc2b4`
- S2 `192c2496c4163f04b3437cd25fca7e8618b7809d`
- S3 `fbef94da7cda9729a590d87feb3e27ab40bf19a8`
- S4 `979bca2f29c9224dbf992867ac3573a1435c914c`
- S5 `8ad68cd5731db6a4c4c75f5cc1bddbf95018f882`

---

## 0. Purpose

This companion makes frozen R4 difficult to misread or misimplement.

It does not create a new semantic owner.
It does not alter the five mechanism-rule classes.
It does not solve OBL062.
It does not authorize executable mechanism rules, production calibration, actor facts or runtime code.

The seam remains:

```text
ADMITTED OBJECTIVE PRE-V3 / WORLD FACTS
+ EXACT ACTOR / POSITION / CONTEXT / TIME BINDINGS
+ EXACT GOVERNED MECHANISM RULE
+ EXACT COUNTERPART / INSTITUTION / OBJECTIVE-HISTORY INPUTS WHEN REQUIRED
        ↓
D1' OBJECTIVE POSITIONED SOCIAL CONSEQUENCE
        ↓
FORM- AND PROOF-CORRECT OBJECTIVE FACT
        ↓
DOWNSTREAM V3 INTERFACE ONLY THROUGH EXISTING/SEPARATELY PROVED OWNERS
```

The companion exists to answer four questions for every proposed D1' fact:

1. **Why may this rule be used?**
2. **Why does this rule apply to this actor here and now?**
3. **What exact objective proposition has been proved, and by what proof kind?**
4. **Why is that proposition current, historical, negative, projected, or not proved?**

---

## 1. Constitutional record topology

The minimum top-level seam record families are:

```text
R1 MECHANISM_RULE_RECORD
R2 RULE_APPLICATION_RECORD
R3 OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD
R4 EVIDENCE_WITNESS_RECORD
```

Required reusable embedded blocks:

```text
B1 ACTOR_POSITION_CONTEXT_TIME_BINDING_BLOCK
B2 TEMPORAL_VALIDITY_BLOCK
B3 DERIVATION_PROVENANCE_BLOCK
```

A separate source/rule traceability record is governance/admission companion material and is specified outside this core record topology.

No requirement follows for four physical tables/classes/services. These are semantic record contracts only.

---

## 2. `MECHANISM_RULE_RECORD`

### 2.1 Required fields

```text
RULE_ID
RULE_VERSION
COMPETENT_OWNER_OR_AUTHORITY_REF
MECHANISM_CLASS
ALLOWED_INPUT_TYPES
REQUIRED_BINDINGS
OUTPUT_CONSEQUENCE_TYPES
QUALIFICATION_OR_APPLICABILITY_LAW
ASSERTION_KIND_OR_PROOF_CONTRACT_ALLOWED
REALIZATION_OR_CURRENTNESS_WITNESS_SCHEMA
TEMPORAL_OR_LIFECYCLE_REQUIREMENTS
CONTEXT_INSTITUTION_HISTORICAL_VALIDITY
BOUNDARY_CONDITIONS
SOURCE_OR_CLAIM_STATUS
PORTABILITY_SCOPE
CALIBRATION_STATUS_IF_ANY
NEGATIVE_CEILING
```

### 2.2 Conditional fields

```text
INSTITUTIONAL_CONFIGURATION_REQUIREMENT
CLOSED_WORLD_NEGATION_AUTHORITY
RECURRENCE_OR_FRESHNESS_REQUIREMENT
PERSISTENCE_TO_TERMINATION_AUTHORITY
COUNTERPART_OR_INSTITUTION_REQUIREMENT
OBJECTIVE_HISTORY_REQUIREMENT
```

### 2.3 Hard laws

```text
MECHANISM_CLASS != MECHANISM_RULE
RULE_ID WITHOUT CURRENT AUTHORITY != CURRENT RULE
SOURCE CITATION != RULE AUTHORITY
SOURCE EFFECT SIZE != CALIBRATION AUTHORITY
RULE VALIDITY != ACTOR APPLICABILITY
RULE APPLICABILITY != CONTINGENT REALIZATION
```

A rule record may never contain a direct person-side output type such as appraisal, distress, mastery, premise, belief, motive, memory, trait, learning or durable development.

---

## 3. `RULE_APPLICATION_RECORD`

### 3.1 Required fields

```text
RULE_APPLICATION_ID
MECHANISM_RULE_REF
ACTOR_REF
WORLD_REF
CONTEXT_REF(S)
POSITION_REF(S)
VALID_TIME_OR_INTERVAL
DIRECT_DETERMINANT_REF(S)
ASSERTION_KIND_PROPOSED
QUALIFICATION_RESULT
DERIVATION_PROVENANCE
```

### 3.2 Conditional fields

```text
COUNTERPART_OR_INSTITUTION_REF(S)
OBJECTIVE_SOCIAL_HISTORY_REF(S)
INSTITUTIONAL_CONFIGURATION_REF(S)
EXTERNAL_ACTION_OCCURRENCE_REF(S) only after competent external admission
EVIDENCE_WITNESS_REF(S)
CLOSED_WORLD_SCOPE_REF
PROJECTED_SCENARIO_REF when modality is PROJECTED_COUNTERFACTUAL
```

### 3.3 Determinant law

Each `DIRECT_DETERMINANT_REF` must identify an exact truth-bearing input or binding on which the application directly depends.

A generic provenance narrative is insufficient if it cannot answer:

```text
WHY DOES THIS APPLICATION HOLD?
WHICH CURRENT DERIVED FACTS DEPEND DIRECTLY ON THIS DETERMINANT?
```

The set may include:

- exact source/world fact;
- exact actor/context/position binding;
- exact counterpart/institution relation;
- exact objective-history fact;
- exact institutional configuration;
- exact required witness;
- exact current rule version.

Private V3 psychology is never a direct determinant.

---

## 4. `OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD`

### 4.1 Required fields

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
ASSERTION_KIND
POLARITY
CURRENTNESS
MODALITY
TEMPORAL_FORM
DERIVATION_PROVENANCE
BOUNDARY_CONDITIONS
EVIDENCE_CEILING
NEGATIVE_CEILING
```

### 4.2 Conditional/resolvable fields

```text
MECHANISM_CLASS(ES)
STRUCTURAL_OR_WORLD_SOURCE_REF(S)
EVIDENCE_WITNESS_REF(S)
COUNTERPART_OR_INSTITUTION_REF(S)
OBJECTIVE_SOCIAL_HISTORY_REF(S)
INSTITUTIONAL_CONFIGURATION_REF(S)
SUPERSEDES_OR_INVALIDATES_REF(S)
```

These may be resolved transitively through immutable application/rule/provenance records if the resolution is exact and auditably stable.

### 4.3 Adjudication non-fact

`UNKNOWN_NOT_PROVEN` is **not** a value of `CONSEQUENCE_VALUE_OR_STATE` and is not emitted as an objective actor fact.

If proof fails at the exact proposition/grain and no independently valid opposite proposition is proved, adjudication is:

`UNKNOWN_NOT_PROVEN`

and no consequence record asserting that proposition or its negation is authored.

---

## 5. `EVIDENCE_WITNESS_RECORD`

### 5.1 Required fields

```text
WITNESS_ID
WITNESS_TYPE
WITNESS_POLARITY
COMPETENT_SOURCE_OR_OWNER
SUPPORTED_CONSEQUENCE_TYPE(S)
VALIDITY_OR_EVENT_TIME
ASSERTED_OR_SUPPORTABLE_INTERVAL
SUPERSESSION_TERMINATION_INVALIDATION_STATE
```

### 5.2 Conditional fields

```text
CURRENTNESS_OR_FRESHNESS_REQUIREMENT
RECURRENCE_COVERAGE
GAP_OR_TERMINATION_HANDLING
CLOSED_WORLD_SCOPE
CLOSED_WORLD_COMPLETENESS_AUTHORITY_REF
CONSTITUTIVE_STATE_REF
PERSISTENCE_TO_TERMINATION_AUTHORITY_REF
SOURCE_HEALTH_OR_COMPLETENESS_STATUS
```

### 5.3 Witness semantics

A witness proves only the proposition type and interval licensed by its competent owner and witness schema.

```text
WITNESS EXISTS != ALL RELATED FACTS TRUE
EVENT WITNESS != CONTINUING STATE WITHOUT PERSISTENCE LAW
OLD POSITIVE WITNESS != CURRENT POSITIVE FACT
MISSING POSITIVE WITNESS != NEGATIVE FACT
```

---

## 6. Assertion-kind contract

Every proved seam fact must use exactly one proof-bearing assertion kind:

```text
K1 CONSTITUTIVE_POSITIONAL
K2 QUALIFIED_POSSIBILITY
K3 REALIZED_OCCURRENCE
K4 ACTIVE_DURATIVE
```

These are not P1-P5 mechanism classes.
They answer **how the proposition becomes objectively true**, not **what type of social consequence it is**.

### 6.1 K1 — `CONSTITUTIVE_POSITIONAL`

The proposition is made true by a competent operative rule/state plus exact actor/position/context applicability over the asserted interval.

Examples:

- legal eligibility;
- entitlement;
- valid restriction;
- authority scope;
- active duty/obligation;
- relation-defined dependency where the competent relation/rule itself constitutes the dependency.

Proof requires:

```text
CURRENT COMPETENT CONSTITUTIVE RULE/STATE
+ EXACT APPLICABLE POSITION/BINDING
+ VALIDITY OVER ASSERTED INTERVAL
+ NO DEFEATING SUPERSESSION/TERMINATION/INVALIDATION
```

No performance/exercise event is required unless performance/exercise is itself the proposition asserted.

### 6.2 K2 — `QUALIFIED_POSSIBILITY`

The proposition establishes actor-relative applicability, route, opportunity, reachability or channel availability but not contingent occurrence/use/receipt.

Examples:

- eligible route available;
- counterpart reachable;
- channel available;
- permitted application route;
- task opportunity under exact rule.

Proof requires the exact actor/position/context plus rule-defined qualification/reachability conditions.

### 6.3 K3 — `REALIZED_OCCURRENCE`

The proposition asserts that an external occurrence/treatment/transfer/exercise actually happened.

Examples:

- application submitted;
- gate decision rendered;
- sanction imposed;
- transfer delivered;
- contact occurred;
- information delivered;
- task attended/performed.

Proof requires a competent type-compatible occurrence/treatment/transfer witness at the exact relevant time/grain.

### 6.4 K4 — `ACTIVE_DURATIVE`

The proposition asserts a currently or historically continuing state/relation/condition/recurrent activity over an interval.

Proof requires either:

**Path A — direct interval/current proof**

A competent witness/state record whose validity/currentness directly covers the asserted interval.

or

**Path B — governed persistence-to-termination proof**

```text
COMPETENT ESTABLISHMENT WITNESS/STATE
+ EXPLICIT OWNER-AUTHORIZED PERSISTENCE SEMANTICS
+ COMPLETE AUTHORITATIVE TERMINATION/SUPERSESSION/INVALIDATION COVERAGE THROUGH QUERY TIME
+ NO COMPETENT CLOSING FACT
```

Path B is lawful only when the competent owner explicitly defines such persistence. An old event plus continuing rule validity is not enough.

For recurrent activity, recurrence identity/coverage/freshness requirements remain rule-defined; a single old observation does not become current recurrent activity by persistence convention unless the competent rule/schema explicitly and lawfully defines the recurrence state that way.

---

## 7. Orthogonal truth axes

### 7.1 `POLARITY`

```text
POSITIVE
NEGATIVE
```

Polarity exists only for a proved proposition.

Negative truth requires its own competent proof. Failed positive proof is not negative proof.

### 7.2 `CURRENTNESS`

```text
CURRENT
HISTORICAL_NONCURRENT
```

Currentness is evaluated at the query/claim time under the assertion-kind proof law.

A formerly true proposition can remain historically true over its proved interval while no longer being current.

### 7.3 `MODALITY`

```text
ACTUAL
PROJECTED_COUNTERFACTUAL
```

Projected/counterfactual facts must be stored/handled so they cannot enter current biography or current V3 input as actual truth.

If projected antecedents later become actual, D1' performs a fresh actual derivation against then-current rules, sources, bindings and witnesses. Projection is never promoted in place.

---

## 8. Negation and closed-world law

A negative actor proposition may be emitted only through one of:

1. explicit competent negative evidence;
2. explicit competent denial/rejection/termination/non-occurrence evidence whose semantics prove that exact negative proposition;
3. a current rule-authorized closed-world inference whose exact observation universe and negative semantics are themselves provenance-bearing.

A closed-world negative requires at minimum proof of:

```text
EXACT PROPOSITION / FACT TYPE
EXACT ACTOR / CONTEXT / TIME GRAIN
COMPLETE OBSERVATION UNIVERSE AT THAT GRAIN
MANDATORY POSITIVE RECORDING IF POSITIVE STATE OCCURS
REPORTING/RECONCILIATION CLOSURE THROUGH ASSERTED TIME
IDENTITY INTEGRITY
CHANNEL/SOURCE SCOPE COMPLETENESS
SOURCE HEALTH / VERSION CURRENTNESS
COMPETENT CLOSED_WORLD_AUTHORITY_REF
```

Any unresolved prerequisite yields `UNKNOWN_NOT_PROVEN`.

Binding:

```text
NO RECORD != NEGATIVE
EXPIRED POSITIVE != NEGATIVE
SUPERSEDED POSITIVE != NEGATIVE
TERMINATED PRIOR FACT != OPPOSITE FACT
INAPPLICABLE != NEGATIVE
UNKNOWN != NEGATIVE
```

---

## 9. Independent currentness firewall

The following predicates are independent:

```text
CURRENT(D1'_CONSTITUTION,t)
CURRENT(MECHANISM_RULE,t)
CURRENT(RULE_APPLICATION,t)
CURRENT(CONSEQUENCE_FACT,t)
CURRENT(WITNESS,t)
```

No implication exists merely because the item to the left is current.

In particular:

```text
CONSTITUTION CURRENT -X-> RULE CURRENT
RULE CURRENT -X-> APPLICATION CURRENT
APPLICATION CURRENT -X-> FACT CURRENT
FACT HISTORICALLY TRUE -X-> FACT CURRENT
RULE CURRENT -X-> WITNESS CURRENT
```

HQ semantic adoption of R4/this companion automatically creates zero concrete mechanism rules and zero actor facts.

---

## 10. Temporal-form contract

Each fact preserves its objective temporal form independently of assertion kind:

```text
EVENT
CONDITION
DIRECTED_RELATION
RECURRENT_ACTIVITY
TRANSITION
ORDERED_HISTORY
```

This set is a seam-conformance classification, not a D2 owner.

Examples:

- K3 gate decision may have `EVENT` form;
- K1 authority relation may have `DIRECTED_RELATION` form;
- K4 resource deprivation may have `CONDITION` form;
- K4 ongoing work may have `RECURRENT_ACTIVITY` form.

A lawful condition/relation/recurrent activity remains lawful upstream even when generic non-event V3 ingress is not proved.

```text
LAWFUL NON_EVENT D1' FACT
!= PROVED GENERAL V3 INGRESS
```

OBL062 remains open.

---

## 11. PRE-V3/V3 jurisdiction firewall

No record or proof contract in this companion may directly author:

```text
SUBJECTIVE PREMISE
REASON / GROUND
APPRAISAL
MOTIVE
EXPECTATION / STRIVING
BELIEF / KNOWLEDGE
DISTRESS
MASTERY
PERCEIVED SUPPORT
PRIVATE MEMORY
LEARNING
CAPACITY CHANGE
TRAIT
SELF-MODEL
DURABLE DEVELOPMENT
```

Objective support transfer != perceived support.
Objective demand/load != felt strain.
Objective authority/task discretion != subjective autonomy experience.
Objective occurrence != actor uptake.

Private V3 state can influence later objective social truth only through:

```text
V3-OWNED ACTION/EXTERNALIZATION
-> COMPETENT EXTERNAL OCCURRENCE
-> COMPETENT WORLD/COUNTERPART/INSTITUTION RESPONSE
-> COMPETENT SOURCE-OWNED NEW EXTERNAL FACT
-> NORMAL D1' RE-EVALUATION
```

---

## 12. P1-P5 relation

The five frozen mechanism-rule classes remain:

```text
P1 MATERIAL_ACCESS_DEPENDENCY
P2 DIRECTED_AUTHORITY_OBLIGATION_SANCTION
P3 ORGANIZED_ACTIVITY_TIME
P4 INSTITUTIONAL_GATE_TREATMENT
P5 COUNTERPART_CHANNEL_RELATION
```

Assertion kind is independent of mechanism class.

Examples:

```text
P1 + K1 = benefit entitlement
P1 + K3 = benefit transfer occurrence
P1 + K4 = current wage dependency/resource state

P2 + K1 = authority scope / obligation
P2 + K3 = sanction imposition
P2 + K4 = continuing authority/obligation relation

P3 + K2 = available task/activity opportunity
P3 + K3 = task performance occurrence
P3 + K4 = recurrent activity

P4 + K1/K2 = exact gate eligibility/applicability
P4 + K3 = gate treatment/decision
P4 + K4 = continuing treatment/status state where exact rule/source supports it

P5 + K2 = counterpart/channel reachability
P5 + K3 = contact/transfer
P5 + K4 = active relation/channel state where exact owner proves persistence
```

No additional class is implied.

---

## 13. Fail-closed rules

A proposed fact is not authored when any required item is unresolved, including:

```text
unresolved rule authority/version
missing required actor/position/context binding
unresolved institutional configuration where constitutive
unresolved required counterpart relation
missing required K3 occurrence witness
insufficient K4 currentness/persistence proof
stale/superseded/invalidated witness
unresolved competent source conflict
insufficient closed-world completeness for negative inference
population coefficient offered as actor fact
source construct offered as runtime fact without governed mapping
private psychology offered as objective determinant
projected antecedent offered as actual
```

Default result is `UNKNOWN_NOT_PROVEN` at the attempted proposition/grain unless a separately competent opposite proposition is proved.

---

## 14. What this companion does not specify

The following remain separate post-adoption/implementation grains:

- physical data-store layout;
- serialization/API formats;
- runtime query planner;
- reverse-dependency index implementation;
- source adapters;
- calibration implementation;
- exact physical host/module;
- V3 routing/target-owner fields;
- non-event V3 ingress solution under OBL062;
- generic fixed-point engine;
- generic world writer.

---

## 15. Companion terminal

`R4_SEAM_NORMATIVE_COMPANION_CONTRACT_READY__FOUR_RECORD_FAMILIES__FOUR_ASSERTION_KINDS__ORTHOGONAL_POLARITY_CURRENTNESS_MODALITY__UNKNOWN_IS_NONFACT__GOVERNED_K4_PERSISTENCE_ALLOWED__NEGATION_FAILS_CLOSED__R4_TOPOLOGY_UNCHANGED__OBL062_OPEN`
