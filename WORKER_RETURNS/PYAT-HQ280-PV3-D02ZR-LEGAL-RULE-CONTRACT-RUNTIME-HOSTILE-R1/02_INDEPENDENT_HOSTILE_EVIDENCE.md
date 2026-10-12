# D02ZR — Independent hostile evidence

All 27 hostile tests are in `repro/test_d02zr_hostiles.py`. Each invokes the inherited D02Z candidate module for real and records the actual typed outcome. Nothing is asserted by inspection.

## Hostile classes and what each proves

| class | tests | proves |
|---|---|---|
| Source-identity substitution | `test_wrong_clause_id_refused`, `test_wrong_legal_document_id_refused`, `test_wrong_source_url_refused` | the candidate binds the exact clause, document and source URL; substitution is refused field-by-field |
| Ancestor-wording substitution | `test_wrong_parent_wording_refused`, `test_wrong_grandparent_wording_refused` | the PARENT+GRANDPARENT role set is exact; adding or dropping a role is refused |
| Time-boundary substitution | `test_wrong_time_boundary_refused`, `test_wrong_assent_date_refused` | cohort and assent dates are exact; off-by-one is refused |
| Unsigned issuer metadata | `test_unsigned_issuer_metadata_refused` | a non-null `producer_issuer_ref` is an unproved authority claim and is refused |
| Issued-fact masquerade | `test_issued_fact_ref_masquerade_refused` | a smuggled `issued_fact_ref` is an unauthorized extra key and is refused |
| Local-SHA vs PDF custody | `test_local_sha256_is_not_pdf_custody`, `test_local_sha256_is_not_original_document_identity`, `test_altered_json_identity_changes_hash`, `test_original_pdf_byte_custody_not_custodied` | the canonical hash is a local JSON identity (deterministic, field-sensitive); `source_document_pdf_sha256` is null in every outcome; no PDF bytes are held |
| Operative-state escalation | `test_operative_state_assertion_refused`, `test_n9_current_refused`, `test_n9_historical_refused`, `test_g0b_refused`, `test_empirical_fact_refused`, `test_causal_assertion_refused`, `test_enforcement_assertion_refused`, `test_person_citizenship_assertion_refused`, `test_rule_text_documented_held` | every production operation is held or refused with its exact state; no path yields an issued fact |
| Input-shape hostiles | `test_omitted_required_key_refused`, `test_extra_key_refused`, `test_non_dict_refused` | omitted/extra keys and non-dict inputs are refused with exact reason codes |
| As-enacted vs person-outcome | `test_as_enacted_text_is_not_person_outcome` | an as-enacted textual description carries no person-level outcome and no issuer |
| Fixture execution | `test_35_fixture_cases_all_execute` | all 35 authored fixture cases execute through the documented protocol with exact expected states |

## What the hostiles do NOT prove

Passing hostiles prove the candidate fails closed on the attacked surface. They do not prove the statute's current legal status, the completeness of the amendment chain, actual commencement, or any operative N9/CURRENT state. Those remain held (see `03_SCIENTIFIC_HOLDS.md`).
