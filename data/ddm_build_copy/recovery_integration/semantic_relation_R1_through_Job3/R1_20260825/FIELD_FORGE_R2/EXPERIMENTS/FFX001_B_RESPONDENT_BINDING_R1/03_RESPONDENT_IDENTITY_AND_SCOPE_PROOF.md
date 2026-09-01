# FFX001-B — RESPONDENT IDENTITY AND SCOPE PROOF

## Question-level scope established

For each Q86A–Q86F current C04 row:

- `source_family = Afrobarometer`
- `wave = R5`
- release scope = `MERGED_35_COUNTRY_ROUND_RELEASE`
- release form = `STANDARDIZED_MERGED_ROUND_RELEASE`

These coordinates are current question-level routing authority. They do not themselves identify a respondent.

## Contract@2 identity grain

Current W33/C06 Contract@2 projects question-level identity/provenance coordinates only. Its canonical row projection contains:

`contract_version, question_implementation_id, source_family, wave, source_variable_code, disposition, source_court, source_commit, source_carrier_ref, source_carrier_identity, source_row_selector, source_row_record_sha256, unresolved_token_kind, unresolved_token`.

Therefore the current Contract@2 carrier has no projected field that can serve as:

- respondent ID;
- case/interview ID;
- respondent entity key;
- respondent-country binding;
- respondent-form/split/instrument binding;
- respondent-question administration record.

W33 further constrains the Phase-0 catalog to exact current membership and identity-coordinate validation only; it is never evidence/provenance/predicate authority. Nothing in that role creates respondent identity.

## Required respondent scope relation

A lawful Q86 execution would require, at minimum, an authority-bearing relation equivalent in information content to:

`respondent_key -> Afrobarometer / R5 / exact release/form / COUNTRY_ALPHA3`

plus a governed bridge from that respondent scope to the current Q86 question implementations.

The bounded search established neither a current carrier bearing that relation nor a current canonical pointer that delegates it to a separately governed carrier.

## Why source membership is insufficient

The C04 scope `MERGED_35_COUNTRY_ROUND_RELEASE` describes the release/question implementation universe. It cannot be converted into a respondent join by assuming that every row in a merged release shares identical questionnaire exposure. Q86's native evidence itself proves that administration varies by named country.

Thus:

`SOURCE/WAVE MEMBERSHIP != EXECUTABLE_RESPONDENT_JOIN`

and:

`MERGED_RELEASE_ROW != AUTOMATIC_Q86_EXPOSURE`

## Country scope needed by Q86

The routing predicate requires `COUNTRY_ALPHA3`. The excluded administration set is:

`{ALG, EGY, MRC, SUD, TUN}`.

A country code at source/question metadata grain does not satisfy the proof. The needed value must be bound to the same governed respondent entity whose Q86 exposure is being classified.

No such current governed respondent-country binding was established.

## Historical carrier discipline

Historical V542/V550J/respondent-fact/PostgreSQL lineage references encountered during reconnaissance are not promoted here. Current W33 explicitly preserves an anti-resurrection boundary and does not import historical J membership, historical V550J denominators, or PostgreSQL semantic ownership as current authority.

A historical carrier could only be used if current succession explicitly made its exact bytes, respondent key semantics, scope relation, and question-implementation bridge competent CURRENT authority for this operation. That succession was not established in the bounded search.

Therefore:

`PHYSICAL_DATA_EXISTENCE != CURRENT_AUTHORITY`

`HISTORICAL_EXECUTABLE_CARRIER != CURRENT_CANONICAL_RESPONDENT_BINDING`

## Holding

Question identity and question-level release scope are exact. Respondent identity and respondent-to-scope binding are not canonically reachable at the required current authority grain for this canary.
