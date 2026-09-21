# FIABC-LM2-R1A — WVS7 Native/Canonical Mapping Authority Ontology Adjudication

Status: `ADJUDICATED__MINIMAL_REPAIR_HOLDING_READY`

Repository: `maidiu/rawlsing`

Base:

`agent/rabochii-premain-fiabc-lm2-wvs-parentage-oracle-physical-r1@bf0f4ebb00e7304e1cda29f7ca9b6595fff248dc`

Worker branch:

`agent/rabochii-premain-fiabc-lm2-r1a-mapping-authority-adjudication-r1`

## Holding

The LM2 governance stop is valid at the claim level.

`SOURCE_SEMANTICS_TOPOLOGY` authorizes source-native semantic interpretation, special-state interpretation, and response topology. It does **not** authorize a source-native identifier/value to be written into a C11 field explicitly designated canonical.

`NATIVE_CANONICAL_MAPPING_HARMONIZATION` is the ontology class for a positive native→canonical mapping claim. Despite the broad word `HARMONIZATION`, its semantic ceiling is not cross-source equivalence. The original PRE553 authority implementation separated:

- `SOURCE_SEMANTICS_TOPOLOGY`:
  - `INTERPRET_SOURCE_SEMANTICS`
  - `INTERPRET_RESPONSE_TOPOLOGY`
  - `INTERPRET_SPECIAL_STATES`
- `NATIVE_CANONICAL_MAPPING_HARMONIZATION`:
  - `MAP_NATIVE_CANONICAL_IDENTIFIER`
  - `MAP_NATIVE_CANONICAL_VALUE`

Cross-source equivalence/relation is separately owned by source-relation/equivalence authority. Therefore C and D are distinct.

The current C11 validator is not requiring cross-source harmonization merely because it requires the mapping kind. Its substantive rule is narrower and correct:

> canonical question/response material requires an exact positive native→canonical mapping authority.

The validator is coarse in that one RespondentEvent field, `value_transform_authority_ref`, is used to close either canonical-question or canonical-response material, but that coarseness does not make source semantics sufficient for canonical mapping.

## A. Source-native semantic identity

Claim:

> This WVS7 source variable/code has this source-local meaning.

Required authority:

`SOURCE_SEMANTICS_TOPOLOGY`

Accepted WVS7 evidence supplies this for the frozen P2 pair through:

`EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY@1.0.0`

content hash:

`c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f`

The accepted P2F2 runtime package binds WVS7 question identities, WVS7ResponseValue identities for substantive values, response-state semantics, and exact source-local predicates under that authority.

This authority is sufficient to interpret source-local WVS7 response events. It is not a mapping crosswalk.

## B. Source topology

Claim:

> This response occupies this source-native slot/component/order/routing position.

Required authority:

`SOURCE_SEMANTICS_TOPOLOGY` for source response topology, plus routing authority where eligibility/risk-set semantics are involved.

R6S correctly uses the source authority for Q291G5/Q291P5 scalar topology and the separate routing authority for the 13-country risk-set route.

A+B do not imply C.

## C. Native-to-canonical mapping

Claim:

> This source-native question/value is lawfully represented as a C11 canonical question/value.

Required authority when the canonical C11 field is populated:

`NATIVE_CANONICAL_MAPPING_HARMONIZATION`

at exact claim scope.

The mapping authority must be positive, exact, and independently support the transformation. It cannot be obtained by changing the `authority_kind` label on an existing source-semantic snapshot.

### C1. Canonical question

R6S does **not** make this claim.

Its `QuestionVariableBinding` for Q291G5 and Q291P5 sets:

`canonical_question_ref_or_typed_absence = TypedAbsence("NOT_AUTHORIZED")`

The source-backed facade therefore emits no canonical question ref for these events.

No question-mapping repair is currently required.

If a canonical question identity is introduced later, that would be an identifier-mapping claim. It requires positive mapping authority independently of source semantics.

### C2. Canonical response value

R6S **does** currently make this claim for substantive codes 1–5.

Its `ResponseValueRule` constructs:

- `canonical_value = str(code)`
- `transform_authority_ref = SOURCE_AUTH_REF`

where `SOURCE_AUTH_REF` resolves to `SOURCE_SEMANTICS_TOPOLOGY`.

The facade then writes that value into:

`RespondentEvent.canonical_response_value_if_authorized`

and writes the source-semantic ref into:

`RespondentEvent.value_transform_authority_ref`.

That is exactly the mismatch rejected by C11.

The accepted source semantics establish the native response meaning. They do not, by themselves, establish that the native value may occupy a canonical response field.

## D. Cross-source harmonization

Claim:

> A canonical identity is equivalent/comparable across multiple source universes.

This is stronger than C and is not implied by `NATIVE_CANONICAL_MAPPING_HARMONIZATION`.

The PRE553 ontology separately represents source relations/equivalence. The empirical-object hostile law also prevents a `HARMONIZATION_ALIAS` source relation from becoming authorized merely because labels/keys match.

HB01 is explicit on this boundary. Its source-local adoption and final closure did not promote pooling, harmonization, population generalization, or estimand authority. The accepted WVS7 source-backed C11 release was therefore source-local evidence, not cross-source harmonization authority.

R6S also freezes:

`DISTINCT_BY_DEFAULT__NO_CROSS_SOURCE_PROJECTION`

as its source-relation law.

## Exact C11 validator meaning

For a `RespondentEvent`, current C11 integrity law computes:

`has_canonical = canonical_question_ref_if_authorized != None OR canonical_response_value_if_authorized != None`

If `has_canonical` is true:

1. `value_transform_authority_ref` must exist;
2. it must resolve exactly;
3. the resolved authority must be positive;
4. its kind must be `NATIVE_CANONICAL_MAPPING_HARMONIZATION`.

This rule existed in the original C11 carrier-integrity implementation, commit:

`e6cb975e1b2e401279c5580955464f6976929804`

The authority-kind separation itself existed in the original PRE553 immutable authority implementation, commit:

`2faacc3f084cf65e61843f1692b947177a617013`.

Therefore the LM2 mismatch is not merely an accidental string mismatch introduced by R6S. The two semantic jurisdictions were separated deliberately.

## Does C11 require cross-source harmonization?

No.

The kind name is linguistically broader than the actual ontology claim. The original authority ceiling owns native→canonical identifier/value mapping, while cross-source semantic equivalence has separate authority ownership.

Accordingly, changing C11 to accept `SOURCE_SEMANTICS_TOPOLOGY` for canonical material would weaken a real semantic boundary. It would authorize A+B to manufacture C.

That repair is rejected.

## Is R6S incorrectly populating canonical material?

Yes, but only on the response-value side.

Question identity:
- native question: authorized;
- canonical question: explicitly NOT_AUTHORIZED;
- no defect.

Substantive response values 1–5:
- native raw value: authorized;
- source-local semantic interpretation: authorized;
- canonical response field: populated;
- exact mapping authority: absent;
- defect: canonical promotion without C authority.

Special response states:
- canonical value: absent;
- typed source state retained;
- no mapping defect at this field.

## Does an already-accepted positive WVS7 mapping authority exist?

No accepted positive WVS7 `NATIVE_CANONICAL_MAPPING_HARMONIZATION` authority was found in the exact authority chain relevant to this build:

- the accepted P2F2 runtime package contains source-semantics, routing/risk-set, source-universe, predicate-grammar, discovery, and replay authority snapshots, but no native→canonical mapping snapshot;
- R6S adds coordinate/projection authority but uses `SOURCE_SEMANTICS_TOPOLOGY` for the response transform;
- HB01 final closure explicitly withholds harmonization promotion;
- LM2 reaches the validator with the source-semantic ref and fails closed.

No existing positive mapping object can simply be substituted.

## May a derived mapping authority be constructed from current premises?

Not from A+B alone.

A lawful derived mapping authority would require, at minimum:

1. accepted source-native semantic identity;
2. an independently accepted canonical target identity/value law;
3. an exact deterministic crosswalk between them;
4. explicit scope;
5. provenance to the accepted premises;
6. explicit negative limits against cross-source equivalence if not separately authorized.

The current WVS7 estate proves (1), but the material inspected for the R6S response rule does not contain a separately accepted Rawlsing-canonical target/crosswalk that turns `str(code)` into a positive C mapping. The WVS7ResponseValue objects are source-specific WVS7 semantic identities used by the accepted predicates; they do not themselves prove a native→generic-canonical mapping.

Constructing a `NATIVE_CANONICAL_MAPPING_HARMONIZATION` snapshot directly from source semantics/topology would therefore be semantic authority laundering.

If HQ later admits an independently accepted canonical target/crosswalk, a deterministic derived receipt could be lawful. That premise is not established by this court.

## Question mapping vs response-value mapping

They are distinct semantic claims.

The ontology kind may be the same because it owns both native→canonical identifier and native→canonical value transformations, but the exact authority object/scope need not and should not be assumed identical.

For WVS7 R6S now:

- question mapping required: **NO**, because canonical question is explicitly absent;
- response-value mapping required: **ONLY IF canonical response values remain populated**;
- source-native response semantics required: **YES**, already accepted;
- cross-source harmonization required: **NO**.

## Native-only path is lawful and sufficient for the current predicate language

The current query evaluator defines semantic event value as:

- canonical response value if positively present;
- otherwise raw response value.

The WVS7 predicates are source-local `SURVEY_RESPONSE_EVENT` predicates carrying exact WVS7 question/value refs and source semantic/topology authority.

Therefore a RespondentEvent may lawfully retain:

- native question ref;
- raw response value;
- typed response state;
- source semantics/topology authority;
- canonical question = absent;
- canonical response = absent;
- mapping authority = absent.

This is not a loss of source semantics. It is the correct representation when C is unproved.

## Adjudicated minimum

Do not relabel the accepted source-semantic authority.

Do not broaden the C11 validator.

Do not mint a derived mapping authority from source semantics alone.

Repair the R6S candidate-neutral C11 projection so substantive codes 1–5 remain source-native/raw and do not populate `canonical_response_value_if_authorized` absent positive mapping authority.

Preserve the already correct canonical-question typed absence.

This resolves the ontology contradiction without changing WVS7 physical truth, structural parentage, source semantics, topology, routing, or cross-source posture.

Terminal:

`FIABC_LM2_R1A_WVS7_MAPPING_AUTHORITY_ADJUDICATED__MINIMAL_REPAIR_HOLDING_READY`
