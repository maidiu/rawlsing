# SDTF R4 S1 — PRE-V3/V3 SEAM NORMATIVE CONTRACT R1

STATUS: `S1_NORMATIVE_CONTRACT_EXTRACTED__R4_TOPOLOGY_UNCHANGED__NO_RUNTIME_IMPLEMENTATION`

CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`

WORKER: `agent/rabochii-sdtf-r1-r4-s1-seam-normative-schema`

INHERITED COORDINATOR STATE: `02d4a75c030ed22da48b64718618242fc10ad858`

FROZEN R4 SEMANTIC CANDIDATE: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

GOVERNING R4 ARTIFACT: `35_MINIMAL_PREV3_V3_TRANSDUCTION_CONSTITUTION_CANDIDATE_R4.md`

This document extracts the frozen R4 semantics into a normative seam contract. It does not change D1', P1-P5, owner jurisdiction, OBL062, HQ authority, or production runtime.

---

## 0. Normative target

The seam owns exactly this semantic transformation:

```text
ADMITTED ACTOR-INDEPENDENT OBJECTIVE WORLD / SOCIAL / STRUCTURAL FACTS
+ EXACT ACTOR / POSITION / CONTEXT / TIME BINDING
+ EXACT GOVERNED D1' MECHANISM RULE
+ EXACT RELATIONAL / INSTITUTIONAL / OBJECTIVE-HISTORY INPUTS WHEN REQUIRED
        ↓
OBJECTIVE POSITIONED SOCIAL CONSEQUENCE
```

The smallest companion contract needed to make that transformation auditable consists of four top-level record families plus three embedded normative blocks.

### Four top-level record families

```text
1. MECHANISM_RULE_RECORD
2. RULE_APPLICATION_RECORD
3. OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD
4. EVIDENCE_WITNESS_RECORD
```

### Three embedded normative blocks

```text
A. ACTOR_POSITION_CONTEXT_TIME_BINDING_BLOCK
B. TEMPORAL_VALIDITY_BLOCK
C. DERIVATION_PROVENANCE_BLOCK
```

The embedded blocks are normative information requirements, not separately owned runtime objects. They may be physically normalized, embedded, or referenced later. Their storage shape is `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

This four-record/three-block form is smaller than the eight suggested families while preserving every R4 truth-condition distinction.

---

## 1. Why the suggested eight families collapse to four records

### `MECHANISM_RULE_RECORD`

KEEP as a top-level normative record. A P1-P5 class never authorizes an actor fact by itself. Every positive D1' derivation requires an exact separately governed rule identity and version.

### `RULE_APPLICATION_RECORD`

KEEP as a top-level normative record. It is the proof that one exact rule was tested/applied against one exact actor-position-context-time binding and exact admitted antecedents.

### `ACTOR_POSITION_CONTEXT_BINDING`

DO NOT require a separate top-level record. Its content is constitutionally mandatory but is part of `RULE_APPLICATION_RECORD` through the binding block. A separate record would add identity and lifecycle machinery without a semantic need.

### `OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD`

KEEP as a top-level normative record. The consequence has its own temporal form, status, polarity, provenance, evidence ceiling and currentness that cannot be reduced to the rule or application.

### `REALIZATION_WITNESS_RECORD`

KEEP, generalized as `EVIDENCE_WITNESS_RECORD`. It covers positive realization/state witnesses, constitutive source-state witnesses, explicit negative witnesses, and rule-authorized closed-world negative authority. Separate positive and negative record families are unnecessary because polarity and proof mode are typed.

### `NEGATIVE_WITNESS_OR_CLOSED_WORLD_AUTHORITY_RECORD`

DO NOT require a separate record family. Negative truth is represented only through a witness record whose polarity and negative-authority basis are explicit. Missing positive evidence can never instantiate this record by default.

### `TEMPORAL_VALIDITY_BINDING`

KEEP as a mandatory reusable block, not a separate top-level seam object. Rule currentness, application currentness, fact currentness and witness currentness are independently computed from each record's own validity/lifecycle block.

### `DERIVATION_PROVENANCE_RECORD`

KEEP as a mandatory reusable block carried by application and consequence records. A standalone provenance object is optional implementation normalization, not a constitutional semantic requirement.

---

## 2. The four independent currentness predicates

R4's firewall is sharpened without inventing mutable convenience booleans:

```text
CURRENT(D1'_CONSTITUTION, t)
!= CURRENT(MECHANISM_RULE_RECORD, t)
!= CURRENT(RULE_APPLICATION_RECORD, t)
!= CURRENT(OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD, t)
!= CURRENT(EVIDENCE_WITNESS_RECORD, t)
```

The first predicate belongs to project/HQ authority and is not authored by this seam.

The other four predicates are evaluated independently from each record's own authority, interval, supersession/termination/invalidation state, and required supporting records.

Therefore:

```text
D1' ADOPTED
DOES NOT IMPLY
ANY RULE CURRENT
DOES NOT IMPLY
ANY APPLICATION CURRENT
DOES NOT IMPLY
ANY FACT CURRENT
DOES NOT IMPLY
ANY WITNESS CURRENT.
```

A current rule cannot extend an expired witness. A current witness cannot repair an expired rule. A historical application can remain provenance for a historical fact without being a current application now.

---

## 3. Consequence status vocabulary

R4 requires enough status information to distinguish proof modes without creating a new ontology owner.

The consequence record SHALL carry one `QUALIFICATION_OR_REALIZATION_STATUS` drawn from the following semantic set:

```text
QUALIFIED_ONLY
CONSTITUTIVELY_TRUE
ACTIVE
REALIZED
UNKNOWN
NOT_PROVEN_REALIZED
```

Interpretation:

- `QUALIFIED_ONLY`: applicability/reachability is established; contingent realization is not asserted.
- `CONSTITUTIVELY_TRUE`: an operative competent rule/state plus admitted position makes the objective relation true without requiring a discrete occurrence.
- `ACTIVE`: a continuing objective state/relation is asserted current for an interval under a type-compatible state/constitutive witness.
- `REALIZED`: a contingent occurrence/treatment/transfer/contact/performance is asserted to have happened under a type-compatible realization witness.
- `UNKNOWN`: truth cannot be established at the required grain.
- `NOT_PROVEN_REALIZED`: qualification or prior evidence exists, but the required current realization proof is absent/stale/insufficient.

These values are proof/status semantics inside D1'; they are not six owners and do not change R4 topology.

A separate `POLARITY` SHALL state `POSITIVE` or `NEGATIVE` for asserted facts. `UNKNOWN` and `NOT_PROVEN_REALIZED` are not negative polarity.

---

## 4. Temporal-form contract

Every consequence SHALL preserve one exact temporal form:

```text
EVENT
CONDITION
DIRECTED_RELATION
RECURRENT_ACTIVITY
TRANSITION
ORDERED_HISTORY
```

No form may be converted merely to satisfy downstream transport.

In particular:

```text
CONDITION != EVENT
DIRECTED_RELATION != EVENT
RECURRENT_ACTIVITY != EVENT
ORDERED_HISTORY != EVENT
```

A lawful non-event D1' fact may exist while downstream V3 ingress remains unproved under OBL062.

No S1 field or record may claim that OBL062 is solved.

---

## 5. Universal input authority law

Every positive application MUST identify exact admitted antecedent facts. Acceptable antecedents are only competent externally owned facts, including when applicable:

- PRE-V3 admitted structural/social facts;
- generated-world facts;
- material/physical world facts lawfully consumed by a social mechanism rule;
- property/resource/service facts;
- institutional/legal/organizational rules and states;
- actual authority/obligation facts;
- routes/topology;
- exact externally admitted actor actions or prior social history;
- exact counterpart/institution configuration.

The following never count as sufficient antecedent fact authority by themselves:

```text
THEORY NAME
SOURCE CITATION
GROUP RATE
REGRESSION COEFFICIENT
CATEGORY LABEL
ROLE/TITLE LABEL
COUNTRY/SYSTEM LABEL
MODEL PREDICTION
PRIVATE V3 STATE
```

Where a source construct is not semantically identical to the admitted runtime fact type, an exact source/measurement semantic binding remains required at G6. S1 does not invent that implementation interface.

---

## 6. Rule authority law

A rule is usable only if all are true:

```text
EXACT RULE_ID + RULE_VERSION EXIST;
COMPETENT RULE AUTHORITY EXISTS;
RULE IS CURRENT FOR THE APPLICATION INTERVAL;
MECHANISM_CLASS IS P1-P5 OR AN EXPLICIT COMPOSITION OF THEM;
INPUT TYPES MATCH;
REQUIRED BINDINGS ARE PRESENT;
CONTEXT/INSTITUTION/HISTORY VALIDITY MATCHES;
BOUNDARY CONDITIONS HOLD;
OUTPUT TYPE IS AUTHORIZED;
PROOF/WITNESS REQUIREMENT FOR THE ASSERTION STATUS IS SATISFIED;
NEGATIVE CEILING IS NOT BREACHED.
```

`P1-P5` classify rules. They never authorize a rule application or actor truth on their own.

No rule becomes current merely because R4 is current, a theory source supports it, or a plausible implementation exists.

---

## 7. Application law

A `RULE_APPLICATION_RECORD` MUST prove:

1. exact rule version used;
2. exact actor/world/context/time binding;
3. exact source-owned position relation required by the rule;
4. exact admitted direct antecedent facts used;
5. exact counterpart/institution/history/configuration inputs when required;
6. qualification/applicability result;
7. the application interval;
8. provenance sufficient to reconstruct why the consequence followed;
9. no forbidden private-person input crossed into objective-social derivation.

A nominal label may be present only as source metadata or lookup index. It cannot substitute for the actual positional relation required by the rule.

---

## 8. Consequence truth law

The consequence record is lawful only if:

```text
ITS ACTOR/WORLD/CONTEXT/POSITION MATCH THE APPLICATION;
ITS TYPE IS AUTHORIZED BY THE RULE;
ITS STATUS IS SUPPORTED AT THE REQUIRED PROOF MODE;
ITS VALID INTERVAL IS WITHIN THE SUPPORTING AUTHORITY/WITNESS LIFECYCLE;
ITS POLARITY HAS COMPETENT SUPPORT;
ITS EVIDENCE/PORTABILITY CEILING IS NO STRONGER THAN ITS RULE AND ANTECEDENTS;
ITS TEMPORAL FORM IS PRESERVED;
ITS PROVENANCE POINTS TO THE EXACT APPLICATION AND ANTECEDENTS.
```

A derived fact may never gain stronger causal, evidentiary or portability authority by composition.

---

## 9. Realization/witness law

Every `ACTIVE` or `REALIZED` assertion MUST cite at least one type-compatible competent witness whose support overlaps the asserted fact interval and is not expired, superseded, terminated, invalidated, or outside the rule's lifecycle requirements.

For a constitutive/deontic/positional fact, the operative source-owned relation/state may itself be the type-compatible witness when the governed rule makes that relation true.

For contingent facts such as application, treatment, sanction, transfer, information delivery, contact, attendance or performance, a separately competent occurrence/state witness is required.

For `RECURRENT_ACTIVITY` and continuing-state claims, the governing witness schema MUST define interval coverage, freshness/currentness, recurrence coverage where needed, and termination/gap handling.

One old observation cannot sustain present recurrent truth without rule-authorized coverage semantics.

---

## 10. Negation/polarity law

The following are constitutionally forbidden:

```text
MISSING POSITIVE EVIDENCE -> NEGATIVE FACT
EXPIRED POSITIVE WITNESS -> NEGATIVE FACT
SUPERSEDED POSITIVE WITNESS -> NEGATIVE FACT
NO RECORDED TRANSFER -> PROVED NONTRANSFER
NO RECORDED DECISION -> DENIAL
NO OBSERVED CONTACT -> NO CHANNEL
```

A negative fact requires exactly one competent path:

```text
A. EXPLICIT COMPETENT NEGATIVE WITNESS;
B. EXPLICIT DENIAL / TERMINATION / NON-OCCURRENCE WITNESS;
C. RULE-AUTHORIZED CLOSED-WORLD OBSERVATION WITH PROVENANCE-BEARING
   SCOPE, COMPLETENESS AND NEGATIVE SEMANTICS.
```

If none exists, the lawful result is `UNKNOWN` or `NOT_PROVEN_REALIZED`.

---

## 11. PRE-V3/V3 firewall

No seam record may emit, store as a D1' consequence, or use as an objective-social antecedent any of the following private/person-side semantics:

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
SELF-MODEL
ATTRACTOR CHANGE
```

D1' may emit objective burden, resource shortfall, schedule demand, obligation, authority constraint, support channel or witnessed transfer. It may not infer the actor's felt meaning or developmental effect.

Private V3 state may influence later objective social truth only through the existing externalization/world-response route:

```text
PRIVATE/PERSON STATE
-> EXTERNALLY REALIZED ACTION IF ANY
-> COMPETENT WORLD/INSTITUTION RESPONSE
-> COMPETENT SOURCE AUTHORS NEW EXTERNAL FACT
-> ADMISSION / INVALIDATION / RERUN
```

No seam field may bypass that route.

---

## 12. Non-event V3 boundary

The seam's obligation ends at lawful objective fact authorship plus preservation of its temporal form and provenance.

For event-shaped consequences, an existing event/encounter/OEE/CAN-008 path may be used later only if its exact contract is satisfied.

For `CONDITION`, `DIRECTED_RELATION`, `RECURRENT_ACTIVITY`, and other non-event forms, the normative output SHALL remain a non-event fact even when no current V3 ingress path has yet been proved.

Required disposition:

```text
LAWFUL_D1_PRIME_FACT_EXISTS
+
DOWNSTREAM_NON_EVENT_V3_INGRESS_NOT_YET_PROVED
```

This is valid and must not be converted to an event.

---

## 13. Fail-closed master conditions

A seam derivation MUST fail closed to no positive current actor fact if any required condition is absent or mismatched, including:

- missing exact rule/version;
- noncurrent or unauthorized rule;
- absent required actor/position/context/time binding;
- nominal label standing in for actual relation;
- missing required antecedent fact;
- source construct used without competent semantic binding where one is required;
- rule input/output type mismatch;
- boundary-condition failure;
- missing required witness;
- stale, expired, superseded, terminated or invalidated witness;
- witness interval not covering asserted interval;
- recurrent evidence failing the rule's freshness/coverage requirement;
- negative assertion without competent negative authority;
- private V3 state used directly as objective-social history;
- currentness inferred from constitution/rule/application currentness at another layer;
- event laundering of a non-event fact;
- counterfactual/projected material treated as current admitted truth;
- attempted direct person/V3 write to external structure.

Fail-closed does not mean infer the opposite. It means `UNKNOWN`, `NOT_PROVEN_REALIZED`, no current assertion, or rejection of the application as appropriate.

---

## 14. Constitutional versus post-adoption implementation grain

### Constitutional / companion-contract information

Required:

- exact rule identity/version/authority/class/input-output/binding/applicability/witness/lifecycle/context/boundary/source/portability/calibration-if-any/negative-ceiling semantics;
- exact actor/world/context/position/time binding;
- exact admitted direct antecedent refs;
- exact consequence type/value/status/polarity/temporal form/interval;
- exact witness authority/polarity/type/coverage/lifecycle where needed;
- exact derivation provenance and evidence ceiling;
- exact conditional counterpart/institution/history/configuration refs.

### `POST_ADOPTION_IMPLEMENTATION_GRAIN`

Not added to the seam constitution merely for software convenience:

- database table layout;
- separate normalized binding/provenance/validity tables;
- cache fields such as `is_current=true` when currentness can be computed;
- indexes and search keys;
- replay queue mechanics;
- DAG depth counters;
- storage denormalization;
- cycle-detection algorithm choice;
- transport envelopes;
- serializer/versioning format;
- physical host/module choice;
- non-event V3 transport implementation;
- stochastic sampler implementation;
- source measurement adapter implementation.

---

## 15. Terminal answers A-I

### A. Smallest normative seam contract

Four top-level records plus three embedded blocks, under the hard invariants above.

### B. Constitutional versus implementation-only

The semantic identities, authorities, bindings, antecedents, status/polarity, temporal form, witness/lifecycle and provenance are constitutional companion-contract information. Physical normalization, caches, indexes, replay algorithms and transport machinery are implementation-only.

### C. Can any required information be removed?

No. Removing any of: exact rule/version, actor/world/context/time, actual position relation, direct antecedent refs, consequence type/status/interval/form, witness/polarity/lifecycle where required, or derivation provenance reopens an explicit R4 violation class.

### D. Can any field permit psychology or world-write leakage?

No lawful field requires private V3 content. Any generic free-text `actor_state`, `reason`, `appraisal`, `trait`, `person_input`, or `world_mutation` field is forbidden. External actor action may appear only as a competent admitted external fact ref.

### E. Currentness distinctions

Yes. Constitution, rule, application, consequence fact and witness currentness are independent predicates. No one is inherited from another.

### F. Non-event preservation

Yes. `TEMPORAL_FORM` preserves event/condition/relation/recurrent-activity/transition/history identity. No event fabrication is permitted and OBL062 remains open.

### G. Change to D1'/P1-P5?

None.

### H. D2/D3/D4/P6 required?

No.

### I. Smallest improvement to R4's companion specification

Publish this four-record/three-block contract with explicit independent currentness predicates, one unified polarity-aware witness record, exact direct antecedent provenance, and form-preserving V3 boundary invariants. Do not add another architecture owner or primitive.

---

## Normative terminal

`PASS__R4_SEAM_NORMATIVE_CONTRACT_EXTRACTED__FOUR_RECORD_FAMILIES__THREE_EMBEDDED_BLOCKS__CURRENTNESS_POLARITY_AND_NON_EVENT_FIREWALLS_EXPLICIT__NO_TOPOLOGY_CHANGE`.
