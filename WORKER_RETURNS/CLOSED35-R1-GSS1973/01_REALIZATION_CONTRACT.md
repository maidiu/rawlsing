# GSS1973_SEMANTIC_OWNER_V1 — Realization Contract

## 1. Purpose

`GSS1973_SEMANTIC_OWNER_V1` is the single candidate-neutral semantic owner for future A/B/C processing of the exact canonical source:

```
source_file  = GSS1973.sav
source_sha256 = 59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2
```

Candidate implementations may expose different physical readers or execution strategies, but every candidate must consume the same owner output at the same semantic boundary.

No candidate-local semantic interpretation is permitted.

## 2. Owner schema

The owner must materialize, for every exact source variable admitted downstream:

```text
SourceIdentity
  source_file
  source_sha256
  physical_row_ordinal

FormAuthority
  questionnaire_form ∈ {FORM_1_X, FORM_2_Y}
  form_membership_authority
  form_assignment_authority

VariableAuthority
  variable_name
  variable_identity
  question_identity
  form_membership ∈ {X_ONLY, Y_ONLY, BOTH_FORMS, UNKNOWN}
  response_dictionary_identity
  documentary_authority

EligibilityState
  FORM_NOT_ADMINISTERED
  ROUTED_SKIP
  ELIGIBLE

ResponseState
  SUBSTANTIVE_RESPONSE
  SUBSTANTIVE_NONRESPONSE
  PHYSICAL_MISSING_UNCLASSIFIED

WeightAuthority
  general_weight = WTSSPS | UNAVAILABLE_FAIL_CLOSED
  form_weight = NONE_AUTHORIZED
  forbidden_weights = {FORMWT, BALLOTFORMWT, WTSSNRPS}

DesignAuthority
  sample_frame = 1970_SAMPLE_FRAME
  sample_type = BLOCK_QUOTA
  variance_strata_clustering = NOT_USED_FOR_1973_PER_MR137

CrossReleaseRelation
  INCOME72@1972 != INCOME@1973

AuxiliaryExperiment
  Q105_CARD_XY = SEPARATE_COORDINATE__NO_FORM_JOIN_AUTHORIZED
```

## 3. Questionnaire FORM owner

The only authorized questionnaire-form coordinate is producer `FORM`.

- `FORM=1 -> FORM_1_X -> STANDARD`
- `FORM=2 -> FORM_2_Y -> Y_VARIANT`

No Form 3 authority exists for 1973.

The documentary assignment mechanism is `RANDOMIZED_WITHIN_QUOTA_TYPE`.

The exact realized count of FORM=1 and FORM=2 rows is intentionally absent from this contract. That count belongs to later exact-carrier observation.

## 4. Form-specific question membership

Membership is governed by the producer's 1973 column of Appendix P Table P.1.

The realization rule is:

```text
if exact variable is registered FORM=1 for 1973:
    membership = X_ONLY
elif exact variable is registered FORM=2 for 1973:
    membership = Y_ONLY
elif exact variable is absent from the 1973 form-difference registry:
    membership = BOTH_FORMS
    subject to any independent questionnaire routing rule
else:
    membership = UNKNOWN
```

Membership must be joined by exact documentary variable identity. Name suffixes, observed missingness, equal value vectors, and neighboring variables are not membership authority.

The accepted explicit Q56 bindings are:

- `CLASS -> X_ONLY -> FORM=1`
- `CLASSY -> Y_ONLY -> FORM=2`

Their response spaces remain distinct:

- `CLASS`: lower / working / middle / upper.
- `CLASSY`: lower / working / middle / upper-middle / upper.

`CLASS` and `CLASSY` are therefore not aliases and must never share one response dictionary.

## 5. Eligibility and missing-state owner

Physical missingness is not semantic routing evidence.

Classification precedence is mandatory:

1. **FORM_NOT_ADMINISTERED**  
   Exact FORM plus producer form-membership registry proves the respondent was never administered that item.

2. **ROUTED_SKIP**  
   An explicit questionnaire instruction proves ineligibility independently of FORM.

3. **SUBSTANTIVE_NONRESPONSE**  
   The respondent was eligible and a producer-defined state such as don't know, no answer, or refused applies.

4. **PHYSICAL_MISSING_UNCLASSIFIED**  
   Physical/system missingness exists but no documentary cause is proven.

No state may be promoted upward by observing a raw missing value.

For form-specific variables, form eligibility is decided before route/response interpretation.

## 6. CLASS / CLASSY owner

`CLASS` and `CLASSY` represent two producer-governed 1973 experimental wordings.

The owner must preserve:

```text
CLASS:
  question = Q56
  form = X_ONLY
  form_code = 1
  dictionary = CLASS_4_CATEGORY_1973

CLASSY:
  question = Q56
  form = Y_ONLY
  form_code = 2
  dictionary = CLASSY_5_CATEGORY_1973
```

Forbidden:

```text
CLASSY := CLASS
CLASS := CLASSY
coalesce(CLASS, CLASSY) as one raw variable
dictionary(CLASS) == dictionary(CLASSY)
```

A later analytical harmonization may be separately authorized, but it cannot alter the source-native owner surface.

## 7. Weight owner

The owner records **authority**, not observed field existence.

### Authorized

`WTSSPS` is the current producer-authorized general weight for 1973.

Binding rule:

```text
if exact canonical carrier exposes WTSSPS:
    bind WTSSPS
else:
    general_weight = UNAVAILABLE_FAIL_CLOSED
```

Never synthesize the field.

### Not authorized for 1973

- `FORMWT`
- `BALLOTFORMWT`
- `WTSSNRPS`

A form-specific analysis must first restrict to the form-eligible risk set and then apply any authorized general weight. A general weight never makes the complement form eligible.

No equal-form rescaling may be invented from realized form counts.

## 8. Design owner

The governed source design is:

```text
sample_frame = 1970_SAMPLE_FRAME
sample_type = BLOCK_QUOTA
probability_selection_through = BLOCK_OR_SEGMENT
quota_dimensions = SEX, AGE, EMPLOYMENT_STATUS
form_assignment = RANDOMIZED_WITHIN_QUOTA_TYPE
```

Per accepted MR137 authority, survey-estimation strata/clustering are not used for 1973.

This is not authority to relabel the block-quota design as a simple probability sample. It is only the accepted estimation treatment.

Later-year `VPSU` / `VSTRAT` logic must not be imported.

## 9. Income owner

The source-native relation is:

```text
GSS1972.INCOME72 != GSS1973.INCOME
```

The 1972→1973 response-category revision is producer-documented.

Therefore raw response codes, dictionaries, and variable identities must remain distinct.

Any harmonized income construct requires separate producer or analytical transformation authority and must be represented as a derivative, not a source-identity merge.

## 10. Q105 Card X/Y boundary

Q105 Card X/Y is a separate auxiliary experimental/routing coordinate.

The owner must represent:

```text
questionnaire_form_xy = FORM
q105_card_xy = SEPARATE_UNKNOWN_ASSIGNMENT_COORDINATE
join_authority = NONE
```

No equality, functional dependency, correlation-based mapping, or missingness-based mapping is authorized.

The exact Q105 birth-year-last-digit execution rule remains non-executable until the accepted documentary ambiguity is visually resolved. That unresolved detail does not block the questionnaire FORM realization.

## 11. Candidate-neutral handoff

Future A/B/C qualification order:

```text
SOURCE IDENTITY FREEZE
-> GSS1973_SEMANTIC_OWNER_V1 FREEZE
-> PHYSICAL CARRIER OBSERVATION
-> OWNER/CARRIER CONSISTENCY CHECK
-> CANDIDATE START
-> CANDIDATE PROCESSING
-> COMMON TERMINAL COMPARISON
```

A candidate that constructs its own source semantics before or outside the owner freeze is non-conforming.

## 12. Fail-closed unknowns

The owner preserves as unresolved until later exact-carrier or documentary authority:

- exact realized X/Y counts;
- exact physical source code(s) corresponding to each missing-state class;
- Q105 Card X/Y relation to FORM;
- Q105 exact birth-year digit set;
- any raw `INCOME72` / `INCOME` semantic equivalence;
- any producer-registry membership that cannot be joined by exact variable identity.

These unknowns are explicit states, not defects to be guessed around.
