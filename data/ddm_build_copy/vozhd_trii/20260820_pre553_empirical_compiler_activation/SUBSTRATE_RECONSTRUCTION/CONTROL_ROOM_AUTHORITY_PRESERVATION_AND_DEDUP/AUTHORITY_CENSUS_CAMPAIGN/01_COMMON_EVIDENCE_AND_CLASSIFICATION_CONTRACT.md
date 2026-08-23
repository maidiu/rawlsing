# AUTHORITY CENSUS CAMPAIGN — COMMON EVIDENCE & CLASSIFICATION CONTRACT

Status: `BINDING_COMMON_CONTRACT`

## 1. Authority expectation universe

The browser lane must first build `AUTHORITY_EXPECTATION_UNIVERSE.csv` from accepted Dva/Trii/Chetiri architecture and known consumers.

Each row represents an authority obligation, not a filename.

Minimum fields:

- `expectation_id`
- `authority_family`
- `semantic_obligation`
- `scope_kind`
- `scope_id`
- `known_consumer`
- `governing_authority_ref`
- `required_for_current_35`
- `required_for_new_survey_admission`
- `search_status`
- `final_disposition`

## 2. Located authority object identity

Each distinct content object receives an `authority_object_id` and at minimum:

- exact SHA-256 where bytes are available;
- filename/basename;
- byte size;
- format;
- semantic scope;
- authority family;
- physical locations;
- enclosing package(s);
- provenance refs;
- known builders/installers;
- downstream consumers;
- accepted/review/execution status.

Distinct byte identities must not be collapsed merely because names match.

Exact duplicate bytes may share one authority-object identity only after browser adjudication proves they represent the same epistemic object rather than path-specific package roles.

## 3. Epistemic classes

Every authority object must receive one primary class:

- `MANUAL_ADJUDICATION`
- `MANUAL_REVIEW_WITH_MECHANICAL_PACKAGING`
- `DOCUMENTARY_SOURCE_AUTHORITY`
- `FROZEN_ACCEPTED_PRECEDENT`
- `MECHANICALLY_DERIVED_FROM_NAMED_AUTHORITY`
- `COMPOSITE_MANUAL_AND_DERIVED`
- `REVIEW_ONLY_CANDIDATE`
- `NEGATIVE_OR_EXCLUSION_AUTHORITY`
- `PROVENANCE_OR_AUDIT_ONLY`
- `REGENERABLE_MACHINE_STATE`
- `UNRESOLVED_EPISTEMIC_CLASS`

A machine-readable CSV remains manual authority if its substantive judgments were manually created.

## 4. Quality / execution statuses

Use only the following unless HQ extends the vocabulary:

- `ACCEPTED_EXECUTION_AUTHORITY`
- `ACCEPTED_NONEXECUTION_AUTHORITY`
- `FROZEN_ACCEPTED_PRECEDENT`
- `REVIEW_ONLY__NOT_EXECUTION_ELIGIBLE`
- `PARTIAL_SCOPE_AUTHORITY`
- `PRESERVED_NOT_CERTIFIED`
- `SUPERSEDED__LOSSLESS_SUCCESSOR_PROVED`
- `SUPERSEDED__PARTIAL_OR_UNPROVED`
- `HISTORICAL_WITNESS_ONLY`
- `CONFLICTING_AUTHORITY__ADJUDICATION_REQUIRED`
- `QUALITY_INSUFFICIENT__REPAIR_OR_NEW_AUTHORITY_REQUIRED`
- `STATUS_UNRESOLVED`

## 5. Gap statuses

An expectation may progress through:

- `NOT_SEARCHED`
- `SEARCH_IN_PROGRESS`
- `LOCATED__NOT_ADJUDICATED`
- `LOCATED__PARTIAL_SCOPE_ONLY`
- `LOCATED__REVIEW_ONLY`
- `LOCATED__SUPERSESSION_NOT_PROVED`
- `PHYSICAL_PAYLOAD_RECOVERY_REQUIRED`
- `DOCUMENTARY_AUTHORITY_RECOVERY_REQUIRED`
- `CONFLICTING_EXISTING_AUTHORITY_REQUIRES_ADJUDICATION`
- `EXISTS__ACCEPTED_AUTHORITY_MAPPED`
- `NOT_LOCATED__SEARCH_BURDEN_INCOMPLETE`
- `MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED`

`MISSING_PROVED__NEW_AUTHORITY_CREATION_REQUIRED` is terminal and requires the missingness proof below.

## 6. Missingness proof

No authority obligation may be classified MISSING_PROVED until all relevant surfaces are searched and recorded:

1. current control branch and accepted Git history/authority spine;
2. Dva accepted artifacts and returns;
3. Trii authorities/packets/returns;
4. Chetiri returns and G1A inventory;
5. ChatGPT Library relevant authority/documentary sources;
6. local `/Desktop/Rawlsing` SHA/path manifest;
7. local `/Desktop/RawlsingsExcess` SHA/path manifest;
8. targeted local Codex filesystem search for aliases, historical names, enclosing ZIPs/bundles and likely predecessor directories;
9. known authority packages/installers/builders that may embed or generate the object;
10. provenance/supersession search for an accepted successor that may already absorb the obligation.

Negative search must be recorded in `AUTHORITY_GAP_LEDGER.csv` and linked harvest/search receipts.

## 7. Supersession proof

`SUPERSEDED__LOSSLESS_SUCCESSOR_PROVED` requires positive evidence of semantic preservation.

Acceptable proof may include:

- accepted authority explicitly declaring lossless absorption;
- exact row/key/content crosswalk proving all governed decisions survive;
- deterministic accepted derivation with all inputs preserved;
- accepted installer/build provenance plus exact output parity sufficient for the semantic obligation.

Recency, filename similarity, overlapping row counts, or downstream use alone are insufficient.

## 8. Browser/local packet contract

Each local harvest request gets a stable ID:

`HARVEST-###`

Browser request records:

- exact search question;
- named target authority family;
- known filenames/aliases;
- expected provenance clues;
- roots to search;
- requested mechanical inspections;
- files/categories explicitly forbidden from modification;
- maximum reasonable packet scope.

Local return ZIP contains at minimum:

- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- requested raw candidate files in preserved relative-path folders;
- `ARCHIVE_MEMBER_MANIFEST.csv` where archives are inspected;
- optional mechanical `SCHEMA_COUNTS.csv` only when requested.

The local worker must not rewrite source files, normalize encodings, or regenerate substantive authority.

## 9. Adjudication rule

Browser HQ must inspect the returned bytes and classify each candidate independently. It may request follow-up harvests rather than force a premature conclusion.

A harvest packet is evidence, not authority by virtue of packaging.

## 10. Hygiene lock

During this campaign:

`NO_DELETION__NO_MOVE__NO_RENAME__NO_IN_PLACE_NORMALIZATION`

except temporary copies created inside worker scratch/output folders.

The future dedup campaign remains governed by the parent desk and exact-dedup law.
