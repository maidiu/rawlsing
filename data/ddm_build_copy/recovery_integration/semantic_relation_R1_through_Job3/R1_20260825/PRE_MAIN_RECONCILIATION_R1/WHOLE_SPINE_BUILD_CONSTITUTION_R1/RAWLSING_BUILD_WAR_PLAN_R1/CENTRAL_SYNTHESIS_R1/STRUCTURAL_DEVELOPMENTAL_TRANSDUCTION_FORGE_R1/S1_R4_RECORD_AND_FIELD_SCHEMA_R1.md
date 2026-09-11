# SDTF R4 S1 — RECORD AND FIELD SCHEMA R1

STATUS: `S1_SCHEMA_COMPLETE__NORMATIVE_NOT_PHYSICAL__NO_RUNTIME_HOST_ASSUMED`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

This is a normative semantic schema. It does not prescribe database layout, serialization, class hierarchy, storage normalization, transport, or runtime host.

---

# 1. MECHANISM_RULE_RECORD

## PURPOSE

Identify the exact separately governed social mechanism rule that authorizes one D1' derivation. A P1-P5 class is never sufficient.

## JURISDICTION

Objective PRE-V3/world-to-positioned-consequence rule authority only. No person-side semantics and no world-write authority.

## REQUIRED FIELDS

| FIELD | NORMATIVE MEANING | SOURCE / OWNER |
|---|---|---|
| `RULE_ID` | stable identity of this governed rule | competent rule registry/admission authority |
| `RULE_VERSION` | exact semantic version applied | competent rule authority |
| `COMPETENT_OWNER_OR_AUTHORITY_REF` | authority that admits and governs this rule | existing competent governance/source owner; never theory card alone |
| `MECHANISM_CLASS` | one of P1-P5 or explicit composition | D1' constitutional classification only |
| `ALLOWED_INPUT_TYPES` | admissible antecedent fact types | rule authority, constrained by existing source/type authority |
| `REQUIRED_BINDINGS` | actor/world/context/position/time and conditional relational bindings required | rule authority |
| `OUTPUT_CONSEQUENCE_TYPES` | exact objective consequence types this rule may author | rule authority |
| `QUALIFICATION_OR_APPLICABILITY_LAW` | conditions under which the rule is applicable | rule authority |
| `REALIZATION_WITNESS_SCHEMA` | type-compatible proof requirements for statuses beyond qualification | rule authority constrained by R4 witness law |
| `TEMPORAL_OR_LIFECYCLE_REQUIREMENTS` | rule-validity and output/witness lifecycle constraints | rule authority |
| `CONTEXT_INSTITUTION_HISTORICAL_VALIDITY` | contexts/configurations/eras for which rule is valid | rule authority plus competent institutional/source authority |
| `BOUNDARY_CONDITIONS` | conditions that limit or defeat use | rule authority |
| `SOURCE_OR_CLAIM_STATUS` | exact evidentiary/source posture; not itself causal-use permission | source/provenance authority |
| `PORTABILITY_SCOPE` | exact contexts across which same typed rule may be used | rule authority; cannot exceed source/configuration support |
| `NEGATIVE_CEILING` | explicit outputs/inferences forbidden to this rule | R4 constitution + rule authority |

## CONDITIONAL FIELDS

| FIELD | CONDITION | SOURCE / OWNER |
|---|---|---|
| `CALIBRATION_STATUS` | only when calibrated/quantitative operation is claimed | competent calibration/measurement authority |
| `INSTITUTIONAL_CONFIGURATION_REQUIREMENT` | when configuration constitutes validity/portability | competent institutional/source authority |
| `CLOSED_WORLD_NEGATION_AUTHORITY` | only if the rule authorizes exact closed-world negative inference | competent rule + source completeness authority |
| `RECURRENCE_OR_FRESHNESS_REQUIREMENT` | when continuing/recurrent truth may be asserted | rule authority constrained by R4 witness law |

`INPUT_FACT_SCHEMA_REF`, `SEMANTIC_BINDING_AUTHORITY_REF`, and `CAUSAL_USE_AUTHORITY_REF` are not universally mandated as separate fields. Their semantics are required whenever source constructs or evidence need a nonidentity mapping into runtime fact types or executable rule authority. Physical representation belongs to G6 / `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

## FORBIDDEN FIELDS

No field may encode or authorize:

```text
SUBJECTIVE_PREMISE
REASON
GROUND
APPRAISAL
MOTIVE
BELIEF
KNOWLEDGE
DISTRESS
MASTERY
PERCEIVED_SUPPORT
MEMORY
LEARNING
CAPACITY_CHANGE
TRAIT
DURABLE_DEVELOPMENT
DIRECT_WORLD_WRITE
CATEGORY_EFFECT_SCALAR
THEORY_NAME_CAUSAL_SCALAR
SOCIAL_ECOLOGY_SCORE
```

A generic free-text executable formula that bypasses `ALLOWED_INPUT_TYPES`, `REQUIRED_BINDINGS`, applicability, witness and boundary contracts is forbidden.

## VALIDITY RULE

A rule is valid for an application only if its authority is competent, its exact version is admitted, the application falls inside its temporal/context/institution/historical validity, and none of its boundary conditions or supersession rules defeat use.

## CURRENTNESS RULE

`CURRENT(rule,t)` is evaluated from the rule's own authority/version/lifecycle. It is not inherited from D1' constitutional currentness and does not imply any application/fact/witness currentness.

## VERSION / CURRENT-AUTHORITY RULE

A later rule version does not silently rewrite historical applications. Each application cites the exact version used. Superseded versions may remain historical provenance while no longer authorizing new applications.

## NEGATION / POLARITY RULE

A rule may define negative outputs only if their proof basis is explicit. Closed-world negative semantics require exact scope/completeness authority. A rule may not define ordinary missing positive evidence as negative truth.

## PROVENANCE REQUIREMENT

The rule must identify competent authority and source/claim status sufficient to distinguish:

```text
SOURCE EVIDENCE
!= RULE ADMISSION/CURRENTNESS
!= APPLICATION
!= ACTOR FACT.
```

## TEMPORAL FORM

A rule may authorize one or more output temporal forms, but the form of any consequence must remain explicit at fact level.

## P1-P5 RELEVANCE

Required. `MECHANISM_CLASS` is P1, P2, P3, P4, P5, or an explicit composition. No P6.

## PRE-V3 INPUT BOUNDARY

Consumes only admitted external/world/social/structural facts and exact source-owned bindings.

## V3 OUTPUT BOUNDARY

Outputs only an objective consequence type. It cannot authorize person-side uptake, appraisal, response or development.

## FAIL-CLOSED CONDITIONS

Reject use when rule identity/version/authority is absent, rule is not current for the interval, input types/bindings mismatch, configuration validity is not proved, output type is not authorized, witness contract cannot be satisfied for asserted status, or negative ceiling would be breached.

---

# 2. RULE_APPLICATION_RECORD

## PURPOSE

Prove that one exact governed rule was applied to one exact actor-position-context-time configuration using exact admitted antecedents.

## JURISDICTION

The seam's application/derivation act. It does not own source facts, world mutation, downstream psychology, or witness truth.

## REQUIRED FIELDS

| FIELD | NORMATIVE MEANING | SOURCE / OWNER |
|---|---|---|
| `RULE_APPLICATION_ID` | stable identity for this application | seam application authority |
| `MECHANISM_RULE_REF` | exact `RULE_ID@RULE_VERSION` | current governed rule record |
| `ACTOR_REF` | exact actor to whom positioned consequence pertains | existing actor identity authority |
| `WORLD_REF` | exact world/scenario/world-state identity | existing world authority |
| `CONTEXT_REF(S)` | exact relevant context(s) | source/context authority |
| `POSITION_REF(S)` | actual externally grounded positional relation(s), not title label | competent source/position authority |
| `VALID_TIME_OR_INTERVAL` | interval at which applicability/derivation is evaluated | source/time authority + application contract |
| `DIRECT_ANTECEDENT_FACT_REF(S)` | exact admitted facts actually used | competent PRE-V3/world/source owners |
| `QUALIFICATION_RESULT` | whether required rule conditions are satisfied | derived by exact rule from bound inputs |
| `DERIVATION_PROVENANCE` | enough information to reconstruct the rule/input/binding basis | application record itself, referencing all competent owners |

`DIRECT_ANTECEDENT_FACT_REF(S)` is constitutionally required at companion-spec grain because Rawlsing must be able to prove which objective facts were used. A separate DAG object, depth counter or replay index is not required here.

## CONDITIONAL FIELDS

| FIELD | CONDITION | SOURCE / OWNER |
|---|---|---|
| `COUNTERPART_OR_INSTITUTION_REF(S)` | relational/institutional rule requires them | competent external relation/institution authority |
| `OBJECTIVE_SOCIAL_HISTORY_REF(S)` | rule explicitly depends on prior external history | existing external history/source authority |
| `INSTITUTIONAL_CONFIGURATION_REF(S)` | configuration constitutes or limits rule | competent institutional/configuration authority |
| `EXTERNAL_ACTION_OCCURRENCE_REF(S)` | an actor/collective externalized action is an antecedent | competent external event/world admission owner; never private V3 state itself |
| `CLOSED_WORLD_SCOPE_REF` | application relies on closed-world negative semantics | competent completeness/scope authority |

## FORBIDDEN FIELDS

Forbidden direct antecedents include:

```text
PRIVATE_BELIEF
PRIVATE_MOTIVE
PRIVATE_APPRAISAL
DISTRESS
TRAIT
SELF_MODEL
PRIVATE_CAPACITY
SUBJECTIVE_PREMISE
PRIVATE_MEMORY
PERCEIVED_SUPPORT
PERSON_SIDE_LEARNING
```

Also forbidden as substitutes for required relation facts:

```text
ROLE_TITLE_ONLY
OCCUPATION_TITLE_ONLY
CLASS_LABEL_ONLY
COUNTRY_SYSTEM_LABEL_ONLY
KINSHIP_LABEL_ONLY
GROUP_RATE_ONLY
```

## VALIDITY RULE

The application is valid only if the cited rule version is valid for the application interval, all required bindings exist, each antecedent is admitted and type-compatible, and all rule boundary conditions are satisfied.

## CURRENTNESS RULE

`CURRENT(application,t)` is its own predicate. A historical application can remain valid historical provenance while not being a current application at `t`. Currentness is not inherited from the rule or resulting fact.

## VERSION / CURRENT-AUTHORITY RULE

The application is permanently tied to the exact rule version and exact antecedent versions/identities used. Later source or rule changes trigger invalidation/re-evaluation requirements but do not silently rewrite provenance.

## NEGATION / POLARITY RULE

An application that lacks proof does not emit the opposite. An application using a closed-world negative antecedent must cite the exact negative authority and scope.

## PROVENANCE REQUIREMENT

Must preserve exact direct antecedent refs, rule ref and binding refs. This is the normative minimum required to prevent inference laundering in compositions.

Algorithmic dependency indexes, replay queues, cycle-detection structures and derivation-depth counters are `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

## TEMPORAL FORM

The application has an evaluation interval; it does not itself determine the consequence's temporal form.

## P1-P5 RELEVANCE

Inherited only through the exact referenced mechanism rule. The application cannot change class membership ad hoc.

## PRE-V3 INPUT BOUNDARY

All inputs must be external/admitted facts or exact bindings under competent authority.

## V3 OUTPUT BOUNDARY

No private V3 state may be consumed directly. No person-side fact may be emitted by the application.

## FAIL-CLOSED CONDITIONS

Fail closed on any missing/mismatched required binding, stale or invalid antecedent for the application interval, noncurrent rule, unsupported closed-world inference, forbidden private input, type mismatch, unresolved required counterpart/configuration, or boundary-condition failure.

---

# 3. OBJECTIVE_POSITIONED_CONSEQUENCE_RECORD

## PURPOSE

Represent the exact objective actor-relative social/world consequence authored by D1'.

## JURISDICTION

Objective positioned social consequence only. This record is the PRE-V3 side of the seam and stops before phenomenal/person-side uptake.

## REQUIRED FIELDS

| FIELD | NORMATIVE MEANING | SOURCE / OWNER |
|---|---|---|
| `CONSEQUENCE_ID` | stable identity of the authored objective fact | D1' consequence authority |
| `ACTOR_REF` | focal actor | inherited from valid application |
| `WORLD_REF` | world identity | inherited from valid application |
| `CONTEXT_REF(S)` | relevant context(s) | inherited from valid application |
| `POSITION_REF(S)` | actual relevant positional relations | inherited from valid application |
| `VALID_TIME_OR_INTERVAL` | exact interval of asserted truth | consequence lifecycle under rule/witness support |
| `CONSEQUENCE_TYPE` | exact objective fact type | authorized by mechanism rule |
| `CONSEQUENCE_VALUE_OR_STATE` | exact objective value/state | derived under the rule |
| `MECHANISM_CLASS(ES)` | P1-P5 classification | referenced rule(s) |
| `MECHANISM_RULE_REF(S)` | exact rule version(s) authorizing fact | governed rule authority |
| `STRUCTURAL_OR_WORLD_SOURCE_REF(S)` | direct source/world facts supporting derivation | competent antecedent owners via application provenance |
| `QUALIFICATION_OR_REALIZATION_STATUS` | `QUALIFIED_ONLY`, `CONSTITUTIVELY_TRUE`, `ACTIVE`, `REALIZED`, `UNKNOWN`, or `NOT_PROVEN_REALIZED` | rule proof mode + witness/lifecycle law |
| `POLARITY` | `POSITIVE` or `NEGATIVE` when a fact is asserted | exact witness/closed-world authority |
| `TEMPORAL_FORM` | `EVENT`, `CONDITION`, `DIRECTED_RELATION`, `RECURRENT_ACTIVITY`, `TRANSITION`, or `ORDERED_HISTORY` | consequence semantics; cannot be changed for transport |
| `DERIVATION_PROVENANCE` | application ref + direct antecedent refs + rule refs | application/consequence authority |
| `BOUNDARY_CONDITIONS` | exact carried rule/fact limits relevant to this assertion | rule authority |
| `EVIDENCE_CEILING` | maximum evidentiary/causal/portability strength the fact may claim | no stronger than rule + antecedents + witnesses |
| `NEGATIVE_CEILING` | prohibited interpretation/use | R4 + rule authority |

## CONDITIONAL FIELDS

| FIELD | CONDITION | SOURCE / OWNER |
|---|---|---|
| `REALIZATION_WITNESS_REF(S)` | required for every `ACTIVE` or `REALIZED` assertion; may also point to operative constitutive state where type-compatible | evidence witness authority |
| `COUNTERPART_OR_INSTITUTION_REF(S)` | relational/institutional consequence | inherited from application |
| `OBJECTIVE_SOCIAL_HISTORY_REF(S)` | prior external history is constitutive to the consequence | inherited from application/history owner |
| `INSTITUTIONAL_CONFIGURATION_REF(S)` | configuration constitutes fact/rule validity | competent configuration authority |
| `SUPERSEDES_OR_INVALIDATES_REF(S)` | this fact determinately replaces/terminates another | competent lifecycle/source authority |

## FORBIDDEN FIELDS

Never valid as consequence fields/values:

```text
SUBJECTIVE_PREMISE
REASON
GROUND
APPRAISAL
MOTIVE
BELIEF
KNOWLEDGE
DISTRESS
MASTERY
PERCEIVED_SUPPORT
MEMORY
LEARNING
CAPACITY_CHANGE
TRAIT
DURABLE_DEVELOPMENT
SELF_MODEL
ATTRACTOR_CHANGE
```

Also forbidden: `social_ecology_score`, unexplained class/category effect scalar, theory-name scalar, or any field that treats group probability as actor truth.

## VALIDITY RULE

The fact must be authorized by a valid application and rule, match the allowed output type, preserve all boundary/evidence ceilings, and satisfy the proof requirement for its status/polarity over its exact interval.

## CURRENTNESS RULE

`CURRENT(fact,t)` is evaluated independently from the fact's interval, lifecycle state, supersession/termination/invalidation, and required supporting witness currentness. Rule/application currentness alone cannot keep the fact current.

## VERSION / CURRENT-AUTHORITY RULE

A fact points to exact rule/application identities. Re-adjudication under a later rule may author a new/superseding fact; it does not mutate historical provenance silently.

## NEGATION / POLARITY RULE

Negative polarity requires explicit negative witness or exact rule-authorized closed-world authority. `UNKNOWN` and `NOT_PROVEN_REALIZED` are nonassertions, not negative facts.

## PROVENANCE REQUIREMENT

Must point to the exact rule application and direct antecedent facts. Provenance must remain sufficient to discover why a fact exists and which authority ceiling constrains it.

## TEMPORAL FORM

Required and form-preserving. A condition/relation/recurrent activity remains non-event even if downstream transport is open.

## P1-P5 RELEVANCE

The fact carries the rule class(es) that actually produced it. A domain label such as class, work, household, care, network or social reproduction is not a primitive mechanism class.

## PRE-V3 INPUT BOUNDARY

Inputs are only those carried through the valid application record.

## V3 OUTPUT BOUNDARY

This record may approach V3 only as an objective fact. It has no fields for receivability, premise, appraisal, uptake, response or development. Non-event ingress may remain unproved under OBL062.

## FAIL-CLOSED CONDITIONS

Do not assert positive current truth if provenance, rule/app authority, required witness, interval overlap, recurrence coverage, or source fact currentness is insufficient. Do not infer negative truth from failure.

---

# 4. EVIDENCE_WITNESS_RECORD

## PURPOSE

Provide type-compatible competent proof for constitutive state, active state, contingent realization, or explicit negative truth while enforcing currentness, supersession and polarity.

## JURISDICTION

Evidence/proof of objective external fact only. This record is not a mechanism rule and not a person-state record.

## REQUIRED FIELDS

| FIELD | NORMATIVE MEANING | SOURCE / OWNER |
|---|---|---|
| `WITNESS_ID` | stable identity of evidence/witness claim | competent evidence/source owner |
| `WITNESS_TYPE` | exact proof type compatible with consequence assertion | competent source owner + rule witness schema |
| `WITNESS_POLARITY` | `POSITIVE` or `NEGATIVE` | competent source/evidence authority |
| `COMPETENT_SOURCE_OR_OWNER` | owner able to author this external evidence | existing source/world/institution authority |
| `SUPPORTED_CONSEQUENCE_TYPE(S)` | exact consequence types this witness can establish | rule witness schema + source semantics |
| `VALIDITY_OR_EVENT_TIME` | `VALID_FROM/VALID_TO` or exact event time | source/event/state authority |
| `ASSERTED_CONSEQUENCE_INTERVAL` | interval this witness is being used to support | application/consequence use context |
| `SUPERSESSION_TERMINATION_INVALIDATION_STATE` | whether later authority defeats current use | competent source/lifecycle authority |

## CONDITIONAL FIELDS

| FIELD | CONDITION | SOURCE / OWNER |
|---|---|---|
| `CURRENTNESS_OR_FRESHNESS_REQUIREMENT` | witness type can become stale or rule demands recency | rule witness schema |
| `RECURRENCE_COVERAGE` | recurrent activity truth is asserted | rule witness schema + occurrence/state evidence |
| `GAP_OR_TERMINATION_HANDLING` | continuing/recurrent state can lapse | rule witness schema |
| `CLOSED_WORLD_SCOPE` | witness represents authorized exhaustive observation | competent source/scope authority |
| `CLOSED_WORLD_COMPLETENESS_AUTHORITY_REF` | negative inference depends on source completeness | competent source/rule authority |
| `CONSTITUTIVE_STATE_REF` | operative rule/state itself is the type-compatible witness | competent external rule/state owner |

## FORBIDDEN FIELDS

No private mental report may be treated as proof of an objective social relation merely because it exists. A subjective belief that authority exists is not an authority witness; perceived support is not proof of support transfer.

A source citation without an externally competent witnessed fact is not a witness.

## VALIDITY RULE

The witness must be type-compatible, competent, within its own lifecycle, applicable to the asserted consequence interval, and satisfy the exact rule witness schema.

## CURRENTNESS RULE

`CURRENT(witness,t)` is independent. For interval assertions, witness support must overlap/cover the asserted interval as required. For recurrence, coverage/freshness rules must be met. A source rule remaining current cannot extend witness currentness.

## VERSION / CURRENT-AUTHORITY RULE

Later competent evidence may supersede, terminate or invalidate earlier evidence. Historical evidence remains provenance but cannot sustain a current assertion once defeated.

## NEGATION / POLARITY RULE

Negative witnesses must explicitly carry negative semantics. Closed-world negative inference requires exact scope and completeness authority. Missing positive evidence never autogenerates a negative witness.

## PROVENANCE REQUIREMENT

Must identify the competent source/owner, time/interval, proof type, polarity and any completeness authority used.

## TEMPORAL FORM

A witness may itself be event-shaped or state-shaped. Witness shape does not force the consequence into the same temporal form unless the rule says so.

## P1-P5 RELEVANCE

Potentially all classes. Type compatibility is rule-specific.

## PRE-V3 INPUT BOUNDARY

Witness proves external/objective truth only.

## V3 OUTPUT BOUNDARY

Witness does not establish phenomenal availability, appraisal, uptake, response or development.

## FAIL-CLOSED CONDITIONS

Reject support if source competence is absent, polarity is ambiguous, witness is stale/expired/superseded/terminated/invalidated, interval coverage is insufficient, recurrence freshness fails, or closed-world completeness is not proved.

---

# 5. Embedded normative block A — ACTOR_POSITION_CONTEXT_TIME_BINDING_BLOCK

Required inside every rule application:

```text
ACTOR_REF
WORLD_REF
CONTEXT_REF(S)
POSITION_REF(S)
VALID_TIME_OR_INTERVAL
```

Conditional exact bindings:

```text
COUNTERPART_OR_INSTITUTION_REF(S)
OBJECTIVE_SOCIAL_HISTORY_REF(S)
INSTITUTIONAL_CONFIGURATION_REF(S)
```

`POSITION_REF` must denote an actual source-owned/admitted relation. A title or category may index lookup only when a governed mapping proves the actual relation.

Age/phase is admitted here only when the objective social rule itself is age/phase dependent. If age/phase only changes uptake or development, it remains downstream V3 context.

---

# 6. Embedded normative block B — TEMPORAL_VALIDITY_BLOCK

Every rule, application, consequence and witness must expose enough lifecycle information to evaluate its own currentness predicate. The normative block requires, as applicable:

```text
VALID_FROM
VALID_TO_OR_EVENT_TIME
LIFECYCLE_STATUS_OR_TERMINATION_REF
SUPERSEDES_REF(S)
INVALIDATES_REF(S)
CURRENTNESS/FRESHNESS REQUIREMENT where type-sensitive
RECURRENCE_COVERAGE where recurrent truth is claimed
```

Not every field must be stored in every record if exact existing authority already supplies the same information by reference. The semantic information must nonetheless be available.

Do not add a duplicate mutable `IS_CURRENT` field merely for convenience. That is optional implementation grain and risks drift.

---

# 7. Embedded normative block C — DERIVATION_PROVENANCE_BLOCK

At minimum:

```text
MECHANISM_RULE_REF(S)
RULE_APPLICATION_REF
DIRECT_ANTECEDENT_FACT_REF(S)
STRUCTURAL_OR_WORLD_SOURCE_REF(S)
REALIZATION_WITNESS_REF(S) when required
CONDITIONAL COUNTERPART/INSTITUTION/HISTORY/CONFIGURATION REF(S)
EVIDENCE_CEILING
BOUNDARY_CONDITIONS
```

This block is enough to prove which objective facts and rule were used. Physical dependency indexing, replay queues, graph depth, cycle-detection algorithm and invalidation scheduling are `POST_ADOPTION_IMPLEMENTATION_GRAIN`.

Same-time circular self-support remains forbidden by default; an implementation must not permit provenance cycles to manufacture authority.

---

# 8. Required-field minimality test

Each required semantic field/block closes a known R4 violation:

| REQUIRED INFORMATION | VIOLATION REOPENED IF REMOVED |
|---|---|
| exact `RULE_ID` + `RULE_VERSION` | class/theory/card can masquerade as rule authority |
| competent rule authority | source citation/plausibility can become executable truth |
| allowed input/output types | semantic type laundering |
| exact binding requirements | actor/category shortcut and context universalization |
| applicability law | possibility/applicability collapse |
| witness schema | qualification becomes realization |
| lifecycle/context validity | stale/timeless rule use |
| negative ceiling | person-side/category/group leakage |
| actor/world/context/position/time binding | no exact positioned subject derivation |
| direct antecedent refs | provenance/inference laundering |
| consequence type/value/status | no proof of what D1' actually authored |
| temporal form | event laundering / D2 creep |
| witness type/polarity/time/authority | stale or missing evidence can become realization/negative truth |
| evidence ceiling | composition can strengthen authority illegitimately |

No additional universal field is constitutionally justified in S1.

---

# Schema terminal

`PASS__S1_R4_SCHEMA_MINIMAL__FOUR_RECORDS_THREE_EMBEDDED_BLOCKS__NO_PSYCHOLOGY_NO_WORLD_WRITE_NO_EVENT_LAUNDERING__POST_ADOPTION_PHYSICAL_GRAIN_DEFERRED`.
