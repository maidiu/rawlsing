# FIABC-LM2-R1A — Minimal Repair Holding

## Disposition

`LAWFUL_BOUNDED_REPAIR_PROVED__NO_NEW_WVS7_MAPPING_AUTHORITY_REQUIRED_FOR_NATIVE_ONLY_C11`

The LM2 failure must not be repaired by authority relabeling.

The lawful minimum is to stop making the unsupported canonical-response claim.

## What is wrong

For substantive WVS7 Q291G5/Q291P5 codes 1–5, the accepted R6S materializer currently builds a `ResponseValueRule` with:

- source-native/raw code: accepted;
- source-local semantic meaning: accepted;
- typed state `SUBSTANTIVE_RESPONSE`: accepted;
- `canonical_value = str(code)`;
- `transform_authority_ref = EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY`.

The first three claims belong to source semantics/topology.

The fourth claim is native→canonical mapping.

The fifth reference has the wrong semantic jurisdiction for the fourth claim.

C11 correctly rejects that promotion.

## Rejected repairs

### 1. Relabel the source authority

Reject.

Changing the authority kind from:

`SOURCE_SEMANTICS_TOPOLOGY`

to:

`NATIVE_CANONICAL_MAPPING_HARMONIZATION`

without new mapping evidence would not create a mapping. It would only rename A/B as C.

### 2. Broaden C11 to accept source semantics for canonical fields

Reject.

That would erase the intended ontology boundary between interpreting source meaning and mapping it into canonical material.

### 3. Treat the current kind name as requiring cross-source harmonization

Reject.

The underlying ontology does not support that reading. Native→canonical mapping and cross-source equivalence are separate claims. The broad name does not authorize importing D into C.

### 4. Mint a derived mapping authority from the existing source authority alone

Reject on the current evidence.

A deterministic derived mapping receipt could be lawful only where a canonical target/crosswalk is independently accepted. The relevant WVS7 authority chain establishes source-specific WVS7 response identities and exact source-local values, but not a separately accepted Rawlsing canonical target/crosswalk for the R6S `str(code)` promotion.

A+B alone cannot generate C.

### 5. Populate a canonical question identity

Reject as unnecessary and unsupported.

R6S already does the correct thing:

`canonical_question_ref_or_typed_absence = NOT_AUTHORIZED`.

Keep it.

## Surviving repair

For substantive source codes 1–5, construct the candidate-neutral C11 projection as native/source-local material only:

- preserve physical/raw value;
- preserve `SUBSTANTIVE_RESPONSE`;
- preserve the exact source semantic/topology authority closure;
- preserve exact Q291G5/Q291P5 native question bindings;
- preserve response topology and occurrence identity;
- set `canonical_response_value_if_authorized = None`;
- set `value_transform_authority_ref = None`.

Special source response states remain as already governed.

Canonical question remains absent.

No mapping authority is required when no canonical mapping claim is made.

## Why this does not starve the existing WVS7 predicate court

Current PRE553 query law evaluates a response event's semantic value as:

1. `canonical_response_value_if_authorized`, if present;
2. otherwise `raw_response_value`.

The accepted WVS7 predicates are source-local `SURVEY_RESPONSE_EVENT` predicates carrying exact WVS7 question/value refs and exact source response/topology authority.

Therefore removing an unauthorized canonical response value does not erase the source-native value needed by those predicates.

The repair narrows the claim. It does not alter the source evidence.

## Question mapping and response mapping

They do not require one indivisible semantic authority claim.

The current ontology kind can own both identifier mapping and value mapping, but those are distinct operations and exact scopes.

For this repair:

- canonical question mapping: not claimed;
- canonical response mapping: not claimed;
- source-native question semantics: retained;
- source-native response semantics: retained.

If future work wants canonical question or response material, it must present exact positive mapping authority for that specific mapping.

## What remains frozen

This adjudication gives no determinant to reopen:

- canonical WVS7 source identity;
- raw source bytes;
- R6S structural materializer blob as historical evidence;
- structural preimage identity;
- derivative-parentage receipt;
- parentage bundle;
- Lock2 authority/workload freeze;
- canonical physical expectation;
- WVS7 physical metadata.

The later implementation/recovery worker may need to reissue semantic projection/C11-derived identities after removing unsupported canonical response material. That is not a physical-source reread requirement and is outside this worker's execution authority.

## Recovery boundary released by this holding

The next lawful implementation step begins at:

`CANDIDATE_NEUTRAL_COMMON_C11_BUILD`

using the already frozen source/physical/structural evidence, with a corrected source-native-only response projection.

No Candidate A/B/C process may begin before the corrected common C11 build validates and the independent oracle is lawfully frozen.

## Explicit authority boundary

This worker creates **no** new semantic authority snapshot.

This worker does not declare `NATIVE_CANONICAL_MAPPING_HARMONIZATION` authority for WVS7.

This worker adjudicates that such authority is unnecessary for the native-only representation and remains required if canonical response/question fields are later positively populated.

Terminal:

`FIABC_LM2_R1A_WVS7_MAPPING_AUTHORITY_ADJUDICATED__MINIMAL_REPAIR_HOLDING_READY`
