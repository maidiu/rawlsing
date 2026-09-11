# SDTF R4 S1 — OVERBUILD AND UNDERBUILD AUDIT R1

STATUS: `PASS__MINIMAL_SEMANTIC_INFORMATION_PRESERVED__PHYSICAL_AND_DOWNSTREAM_GRAIN_DEFERRED`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

This audit tries to delete fields/records and also tries to find missing information that would allow an R4 violation.

---

## 1. Record-family deletion court

### Delete `MECHANISM_RULE_RECORD`?

FAIL.

Without a separately governed rule record, P1-P5 class membership, source citation, theory card, correlation or analyst interpretation could become actor truth.

`MECHANISM_RULE_RECORD: REQUIRED`.

### Delete `RULE_APPLICATION_RECORD`?

FAIL.

Without an application identity, Rawlsing cannot prove which exact actor/position/context/time binding and direct antecedents were used with which exact rule version. Rule authority and fact truth would collapse.

`RULE_APPLICATION_RECORD: REQUIRED`.

### Delete `OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD`?

FAIL.

Without a separately represented consequence, application/qualification and actor fact truth collapse; fact-specific interval/status/polarity/form/currentness cannot be represented.

`OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD: REQUIRED`.

### Delete `EVIDENCE_WITNESS_RECORD`?

FAIL.

Without a proof object/contract, qualification could become realization, stale evidence could sustain current truth, and missing evidence could drift into negative truth.

`EVIDENCE_WITNESS_RECORD: REQUIRED`.

### Add a fifth top-level `ACTOR_POSITION_CONTEXT_BINDING_RECORD`?

REJECT.

The binding is required information but has no independent seam meaning beyond a rule application. Separate identity/lifecycle would be architectural neatness, not a demonstrated semantic need.

### Add separate `NEGATIVE_WITNESS_RECORD`?

REJECT.

Polarity plus explicit negative/closed-world authority inside the unified witness contract is sufficient and safer. A separate family could tempt the runtime to synthesize one from absence.

### Add separate `TEMPORAL_VALIDITY_RECORD`?

REJECT AS UNIVERSAL REQUIREMENT.

Each record needs its own validity semantics; a reusable block/reference suffices. Physical normalization is implementation grain.

### Add separate `DERIVATION_PROVENANCE_RECORD`?

REJECT AS UNIVERSAL REQUIREMENT.

Application and consequence must expose exact provenance, but provenance does not need its own top-level semantic owner.

`RECORD_SET VERDICT: FOUR TOP-LEVEL RECORD FAMILIES ARE MINIMAL`.

---

## 2. Mechanism-rule field deletion court

The R4 minimum is retained exactly in semantic substance:

```text
RULE_ID
RULE_VERSION
COMPETENT_OWNER / AUTHORITY_REF
MECHANISM_CLASS
ALLOWED_INPUT_TYPES
REQUIRED_BINDINGS
OUTPUT_CONSEQUENCE_TYPE(S)
QUALIFICATION / APPLICABILITY LAW
REALIZATION_WITNESS_SCHEMA
TEMPORAL / LIFECYCLE REQUIREMENTS
CONTEXT / INSTITUTION / HISTORICAL VALIDITY
BOUNDARY CONDITIONS
SOURCE / CLAIM STATUS
PORTABILITY SCOPE
CALIBRATION STATUS IF ANY
NEGATIVE CEILING
```

Deletion findings:

- remove identity/version -> historical/current rule ambiguity;
- remove authority -> evidence citation can become executable rule;
- remove mechanism class -> five-class constitutional constraint becomes unverifiable;
- remove input/output types -> type laundering;
- remove bindings/applicability -> category/position shortcut;
- remove witness schema -> qualification/realization collapse;
- remove lifecycle/context validity -> stale/timeless use;
- remove boundary/negative ceiling -> psychology/category/group leakage;
- remove source/claim/portability -> evidence ceiling and overgeneralization become unauditable;
- remove calibration status when calibration is claimed -> quantitative authority becomes ambiguous.

`RULE_FIELD_SET: MINIMAL IN SEMANTIC SUBSTANCE`.

---

## 3. Should S1 add universal rule fields beyond R4?

### `INPUT_FACT_SCHEMA_REF(S)`

NOT universally required as a distinct field.

Need: source construct/runtime fact mapping must be exact where nonidentity mapping exists.

Disposition: `CONDITIONAL SEMANTIC REQUIREMENT / G6`, not a universal R4 field.

### `SEMANTIC_BINDING_AUTHORITY_REF(S)`

NOT universally required as a distinct field.

Need arises only where a source indicator/construct requires mapping authority.

Disposition: `POST_ADOPTION_IMPLEMENTATION_GRAIN__G6` unless a concrete rule needs it.

### `CAUSAL_USE_AUTHORITY_REF`

NOT universally required as a second authority field.

The competent rule `AUTHORITY_REF` must semantically be rule-admission/causal-use authority rather than mere source citation. Physical separation into multiple refs is G1/G6 design.

### `RULE_CURRENTNESS` cached boolean

REJECT.

Currentness is a predicate of exact version/authority/lifecycle at time `t`. A duplicated mutable flag risks contradiction.

### `EXECUTABLE_FORMULA`

REJECT as constitutional field.

Execution representation is runtime grain and could smuggle free-form semantics around the normative rule contract.

---

## 4. Application-field deletion court

### `RULE_APPLICATION_ID`

KEEP. Needed for exact derivation provenance/reference.

### `MECHANISM_RULE_REF`

KEEP. Otherwise rule class/source card can substitute for exact authority.

### `ACTOR_REF`, `WORLD_REF`, `CONTEXT_REF(S)`, `POSITION_REF(S)`, `VALID_TIME_OR_INTERVAL`

KEEP. Removing any permits universalization, nominal position shortcuts, or timeless derivation.

### `DIRECT_ANTECEDENT_FACT_REF(S)`

KEEP.

This is the smallest companion-spec strengthening justified by the central proof question and R4 `DERIVATION_PROVENANCE`. Without exact direct antecedents, multi-step composition can launder source/evidence authority.

This does not require a new D1' field in the frozen candidate itself and does not mandate a physical DAG store.

### `QUALIFICATION_RESULT`

KEEP in semantic substance. Without it, exact application eligibility cannot be separated from consequent realization.

### Conditional counterpart/institution/history/configuration refs

KEEP only when required by the exact rule. Making them universal would overbuild.

### `DERIVATION_DEPTH`, `PARENT_STEP_REF`, replay index, dependency index

DO NOT require constitutionally.

These may be useful for G2 execution/invalidation, but direct antecedent provenance is the semantic need. Graph optimization belongs to `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

---

## 5. Consequence-field deletion court

Required semantic information:

```text
identity
actor/world/context/position binding
valid interval
consequence type/value
exact rule ref(s)
qualification/realization status
polarity
required witness refs
exact temporal form
exact provenance
boundary/evidence/negative ceilings
conditional counterpart/history/configuration refs
```

The following are semantically required but need not be physically duplicated if exactly resolvable by immutable references:

```text
MECHANISM_CLASS(ES)              may resolve through MECHANISM_RULE_REF(S)
STRUCTURAL/WORLD SOURCE_REF(S)   may resolve through application direct antecedents
BOUNDARY_CONDITIONS              may resolve through exact rule/application provenance
EVIDENCE_CEILING                 may be computed/resolved from rule + antecedents + witness
NEGATIVE_CEILING                 may resolve through R4 + exact rule
```

Therefore the companion specification requires **availability**, not denormalized duplicate storage.

This distinction removes software-oriented overbuild without weakening the semantic contract.

---

## 6. Status-vocabulary audit

Could S1 omit explicit status and infer everything from witness shape?

NO.

Rawlsing must distinguish:

```text
QUALIFIED_ONLY
CONSTITUTIVELY_TRUE
ACTIVE
REALIZED
UNKNOWN
NOT_PROVEN_REALIZED
```

Otherwise a valid rule/state could be confused with contingent occurrence, or missing current proof could become negative truth.

Could S1 add a second `CONSEQUENCE_ASSERTION_KIND` field?

NOT REQUIRED.

The normalized status vocabulary plus `TEMPORAL_FORM`, `POLARITY`, and rule witness schema already encode the required distinction. A second universal assertion-kind field would be redundant unless later implementation proves a concrete ambiguity.

`STATUS VERDICT: ONE NORMALIZED STATUS FIELD IS ENOUGH`.

---

## 7. Polarity-field audit

Could `POLARITY` be inferred from the value string?

NO.

Negative truth has special authority requirements. Polarity must be explicit enough to trigger the negative-evidence/closed-world contract.

Could `UNKNOWN` be encoded as negative polarity?

NO.

`UNKNOWN` and `NOT_PROVEN_REALIZED` are proof states, not negative facts.

`POLARITY VERDICT: REQUIRED AND ORTHOGONAL TO STATUS`.

---

## 8. Witness-field deletion court

Required semantic information for a witness:

```text
WITNESS_ID
WITNESS_TYPE
WITNESS_POLARITY
COMPETENT_SOURCE_OR_OWNER
SUPPORTED_CONSEQUENCE_TYPE(S)
VALID_FROM/VALID_TO or EVENT_TIME
ASSERTED_CONSEQUENCE_INTERVAL
SUPERSESSION/TERMINATION/INVALIDATION STATE
```

Conditional but mandatory when applicable:

```text
CURRENTNESS/FRESHNESS REQUIREMENT
RECURRENCE_COVERAGE
GAP/TERMINATION HANDLING
CLOSED_WORLD_SCOPE
CLOSED_WORLD_COMPLETENESS AUTHORITY
CONSTITUTIVE STATE REF
```

Any deletion that hides source competence, polarity, interval support or supersession reopens the exact R3 final-review defect.

---

## 9. Currentness-field overbuild audit

S1 intentionally does not require five mutable `IS_CURRENT` booleans.

It requires five separate **predicates**:

```text
CURRENT(CONSTITUTION,t)
CURRENT(RULE,t)
CURRENT(APPLICATION,t)
CURRENT(FACT,t)
CURRENT(WITNESS,t)
```

Each is computed/resolved from the correct authority/lifecycle information.

This both satisfies the user-required firewall and avoids cache inconsistency.

`CURRENTNESS VERDICT: SEMANTIC DISTINCTION REQUIRED; DUPLICATE STORAGE NOT REQUIRED`.

---

## 10. V3-boundary field audit

Should the consequence add `V3_INGRESS_STATUS`?

NO universal field is necessary.

`TEMPORAL_FORM` plus the hard boundary law is enough to know that:

- event-shaped facts may only use exact existing event ingress contracts;
- non-event facts remain non-event and OBL062 remains open.

Adding a seam-owned ingress state risks D4 creep.

Should the consequence carry `V3_TARGET_OWNER`?

NO at constitutional seam grain.

Routing is downstream interface/implementation responsibility and can change without changing objective fact truth.

`NON_EVENT VERDICT: FORM-PRESERVING FACT TYPE IS REQUIRED; DOWNSTREAM ROUTING FIELDS ARE NOT`.

---

## 11. Psychology-leak field audit

Any generic field named or semantically equivalent to the following is rejected:

```text
ACTOR_INTERNAL_STATE
PERSON_STATE
SUBJECTIVE_MEANING
PREMISE
REASON
APPRAISAL
MOTIVE
DISTRESS
MASTERY
PERCEIVED_SUPPORT
TRAIT
LEARNING
DEVELOPMENTAL_EFFECT
```

Likewise no application field may directly reference a V3 private-state object as an objective antecedent.

An externalized action may enter only after competent external admission.

`PSYCHOLOGY OVERBUILD VERDICT: ZERO PERSON-SIDE FIELDS REQUIRED`.

---

## 12. World-write field audit

No `WORLD_MUTATION`, `STRUCTURE_WRITE`, `INSTITUTION_UPDATE`, or equivalent field belongs in the D1' seam contract.

The application may cite a newly admitted external world fact authored by competent owners. It cannot author that fact merely because a person acted.

`WORLD-WRITE VERDICT: ZERO D3 FIELDS REQUIRED`.

---

## 13. Non-event underbuild audit

Would storing only `EVENT` be enough?

NO.

The following must remain distinguishable:

```text
EVENT
CONDITION
DIRECTED_RELATION
RECURRENT_ACTIVITY
TRANSITION
ORDERED_HISTORY
```

Without this field, implementation pressure could launder conditions/relations/recurrent activities into fake events.

The six forms do not create D2. They bind existing lifecycle/history semantics.

`TEMPORAL_FORM VERDICT: REQUIRED; D2 STILL REJECTED`.

---

## 14. Open-grain discipline

The following are real needs but not S1 constitutional fields merely because they will be needed later:

```text
G1 rule registry implementation and admission workflow
G2 physical hosting, dependency indexes, replay/invalidation engine, cycle algorithm
G3 concrete event/state/relation/recurrent witness adapters
G4 OBL062 non-event V3 ingress
G5 domain-specific external reciprocal response machinery
G6 source measurement/calibration/semantic mapping and causal-use admission
```

All are marked `POST_ADOPTION_IMPLEMENTATION_GRAIN` except where their semantic constraints are already expressed by references/invariants in S1.

---

## 15. Underbuild search conclusion

No missing field was found that requires changing D1' or P1-P5.

The only companion-spec information not explicit as a single R4 output field but required to prove the user's central questions is:

1. exact direct antecedent refs at application/provenance grain;
2. explicit polarity;
3. a normalized proof/status vocabulary resolving qualification, constitutive truth, active state, realization, unknown and not-proven-realized;
4. explicit independent currentness predicates for rule/application/fact/witness;
5. explicit six-way temporal form preservation.

All five are extractions/hardenings of R4's existing semantic requirements, not new architecture.

---

## Audit terminal

`PASS__S1_R4_OVERBUILD_UNDERBUILD_AUDIT__FOUR_RECORDS_MINIMAL__REQUIRED_INFORMATION_IRREDUCIBLE__DUPLICATE_PHYSICAL_FIELDS_NOT_MANDATED__NO_D1_P1_P5_CHANGE__NO_D2_D3_D4_P6`.
