# CLOSED35-R1-GSS1972 — Realization Contract

Schema:

`CLOSED35_GSS1972_SEMANTIC_REALIZATION@1.0.0`

## 1. Purpose

This contract is the candidate-neutral semantic owner for `GSS1972.sav`.

It consumes physical facts; it does not decode them.

It interprets only documentary claims already closed by `CLOSED35-L2-GSS1972`.

The contract must be applied identically by A/B/C.

## 2. Immutable source binding

```text
family              = GSS
release             = 1972
canonical_filename  = GSS1972.sav
canonical_sha256    = e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204
source_format       = SAV
reader_mode         = NATIVE_GOVERNED
edge_classes        = [EC01, EC07, EC10, EC12]
```

No alternate GSS year, cumulative file slice, filename, or same-looking derivative may replace this source without the generic parentage/equivalence contracts.

## 3. Replay and respondent identity

Canonical replay key:

`source_sha256 + source_row_ordinal`

Native field:

`id`

Binding:

`SOURCE_LOCAL_ATTRIBUTE_CHECK_ONLY`

Allowed:

- preserve exact `id`;
- test source-local injectivity if supplied by accepted physical evidence;
- expose it for source-local audit.

Rejected:

- cross-release person join;
- cumulative-person identity;
- row replacement or deduplication;
- replay keyed only by `id`.

Rejection code:

`REJECTED__GSS1972_NATIVE_ID_HAS_NO_CROSS_RELEASE_IDENTITY_AUTHORITY`

## 4. Design semantic surface

`sample` is bound as:

`DESIGN_CLASSIFIER:1960_FRAME_BLOCK_QUOTA`

It is not a weight.

Fixed negative coordinates:

```text
form                 = NOT_APPLICABLE_1972
ballot               = NOT_APPLICABLE_1972
item_rotation        = NOT_APPLICABLE_1972
topical_module       = NOT_APPLICABLE_1972
international_module = NOT_APPLICABLE_1972
```

Any candidate that emits a 1972 form/ballot assignment from later GSS conventions fails semantic equivalence.

## 5. Routing evaluation model

Each routed projection has these inputs:

```text
source_row_replay_identity
source_variable_identity
raw_physical_state
raw_value_if_observed
documentary_route_id
preserved prerequisite field/value evidence
occurrence_role
```

The route evaluator emits:

```text
eligibility_state
occurrence_state
semantic_response_state
route_authority_id
route_provenance
```

### Eligibility vocabulary

- `ELIGIBLE_DOCUMENTED`
- `FILTERED_SKIPPED_DOCUMENTED`
- `NOT_ASKED_DOCUMENTED`
- `NOT_APPLICABLE_DOCUMENTED`
- `ROUTE_EVALUATION_UNRESOLVED`

### Response-state rule

Response semantics are conditional on routing.

A physical missing cell may become a response-missing/nonresponse state only after documentary routing establishes eligibility or after an exact 1972 codebook state directly supplies the semantic meaning.

Physical missingness alone never emits:

- filtered;
- skipped;
- not asked;
- not applicable.

### Contradictory physical/documentary evidence

If a documented route says ineligible but an observed raw value exists, the candidate must:

1. retain the observed raw physical value;
2. retain the documentary route result;
3. emit a contradiction/audit condition;
4. not delete or rewrite either side.

Required audit state:

`ROUTING_PHYSICAL_CONTRADICTION__RAW_PRESERVED`

This protects source truth from semantic cleanup.

## 6. Frozen route rules

### GSS1972-R001 — sample admission

Role:

`RESPONDENT_SELECTION_CONTEXT`

Authority:

1972 questionnaire + Appendix A.

Binding:

block/segment probability selection followed by block quota selection on sex/age/employment.

No downstream item eligibility is inferred merely from this design fact.

### GSS1972-R002 — direct-item authority

The 1972 questionnaire controls direct GSS item routing.

Printed `IF`, `ASK`, `SKIP`, `GO TO`, and substitution instructions are binding.

### GSS1972-R003 — Q51-Q81 omnibus exclusion

State:

`EXCLUDED_NON_GSS_INSTRUMENT_BLOCK`

These paper-questionnaire occurrences do not become GSS1972 semantic occurrences merely because they are printed in the same omnibus instrument.

### GSS1972-R004 — Q3 parental substitution

Q3 controls occurrence of Q4 and Q91 parent-role columns.

Parent roles:

- `father_or_substitute`
- `mother_or_substitute`

No substitute → corresponding later parent occurrence is documentarily suppressed.

### GSS1972-R005 — Q9 work route

Q9 controls Q10-Q12 respondent work-history occurrence.

Never-worked paths skip according to the printed route.

Missingness does not establish never-worked status.

### GSS1972-R006 — Q13-Q16 spouse route

Q13 enters only for currently married respondents.

Spouse work-history fields require the documented spouse-work branch.

Nonmarriage is a documentary route state, not an inference from spouse-field missingness.

### GSS1972-R007 — Q17-Q18 target-person routing

Occurrence target is semantic information.

Allowed target roles:

- `respondent`
- `spouse`

The route chooses the role. Candidates may not merge both into one anonymous supervision response.

### GSS1972-R008 — Q19 household composition

Q19A total-person count controls Q19B-E/Q20 occurrence.

If total household persons = 1, the instrument skips age-band subitems.

These are aggregate household variables, not repeated person occurrences.

### GSS1972-R009 — Q25 explicit not-asked state

Instrument state:

`NOT_ASKED_DOCUMENTED:INAPPROPRIATE`

This semantic state is distinct from:

- system missing;
- user missing;
- refusal;
- unknown eligibility.

### GSS1972-R010 — Q44 staged conditional sequence

Q44A/Q44B/Q44C are staged occurrences.

Later subitem eligibility is controlled by the prior answer route.

Physical sparsity cannot substitute for the predecessor condition.

### GSS1972-R011 — Q82 employment filter

Q82 is eligible only for currently employed respondents under the 1972 questionnaire.

### GSS1972-R012 — Q91 repeated-person matrix

Occurrence set:

```text
respondent
father_or_substitute
mother_or_substitute
spouse_if_currently_married
```

Occurrence identity is mandatory.

Flattening is forbidden.

Parent occurrence eligibility is tied to Q3.

Spouse occurrence is tied to current marriage.

### GSS1972-R013 — technical / derived fields

Technical fields such as:

- YEAR;
- ID;
- SAMPLE;
- weights;
- exact 1972-explicit recodes

are governed by exact source identity plus 1972-explicit cumulative-codebook/method authority.

No direct-question skip rule is invented for them.

## 7. Weight selector contract

Physical carriers are always preserved whether selected or not.

### Intent: raw descriptive / no population claim

```text
selector = NONE
status   = ADMITTED_UNWEIGHTED_NON_GENERALIZING
```

### Intent: person-level population inference

Scope:

historical GSS target adult population represented by current producer guidance for 1972.

```text
selector = WTSSPS
status   = ADMITTED_DEFAULT
```

Required provenance:

`LATER_POSTSTRATIFIED_CUMULATIVE_PERSON_WEIGHT__EXPLICIT_1972_APPLICABILITY`

### Intent: legacy historical adults-in-household reproduction

```text
selector = WTSSALL
status   = ADMITTED_NONDEFAULT_WITH_METHOD_PROVENANCE
```

Required provenance:

`LATER_CUMULATIVE_HISTORICAL_PERSON_WEIGHT__EXPLICIT_1972_APPLICABILITY`

### Unsupported / rejected selector intents

```text
household_population_default
  -> UNSUPPORTED_AT_CURRENT_SCOPE

modern_design_corrected_variance
  -> UNSUPPORTED__NO_AUTHORIZED_1972_VARIANCE_PAIR

form_weighting
  -> NOT_APPLICABLE_1972

ballot_form_weighting
  -> NOT_APPLICABLE_1972

2004plus_nonresponse_weighting
  -> NOT_APPLICABLE_1972
```

No implicit fallback is allowed.

## 8. Variance/design contract

Authorized physical design facts:

- `sample` design classifier;
- exact source physical technical fields if present.

Authorized analytical variance pair:

`NONE`

Explicit unsupported claim:

`GSS1972_MODERN_VPSU_VSTRAT_VARIANCE_DESIGN`

Disposition:

`UNSUPPORTED__DOCUMENTARY_COURT_REJECTED_1972_AUTHORITY`

This is stronger than UNKNOWN.

Candidates must not create placeholder PSU/stratum coordinates.

## 9. Candidate neutrality

The projection function may consume:

- canonical physical source incidence;
- frozen GSS1972 authority pack;
- declared analytical intent.

It may not consume:

- candidate identity;
- candidate performance;
- candidate-local inferred routes;
- later GSS release defaults;
- empirical missingness frequencies as route authority.

For equal inputs and equal declared analytical intent, A/B/C must converge on one semantic projection.

## 10. Qualification boundary

This contract being implemented does not itself prove:

- source execution;
- row-level route realization;
- A/B/C physical equivalence;
- A/B/C semantic parity;
- measured performance.

Those belong to the later qualification court.

This contract is the immutable semantic expectation against which that court runs.
