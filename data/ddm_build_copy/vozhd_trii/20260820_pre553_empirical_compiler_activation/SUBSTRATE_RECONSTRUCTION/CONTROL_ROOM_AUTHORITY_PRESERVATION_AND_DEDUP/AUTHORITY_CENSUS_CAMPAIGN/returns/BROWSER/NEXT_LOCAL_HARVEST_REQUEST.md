# HARVEST-003 — QUESTION_SEMANTIC_MASTER_AND_DRIVER_FACET_LINEAGE

Status: `ISSUED__AWAITING_LOCAL_PACKET`

## Exact authority question

Which exact historical/current `questions_master_semantic.csv` and `questions_master_drivers.csv` lineage carries the human/manual semantic-classification, driver, facet, scope and triage capital behind the **2,148-row driver-semantic evolution** isolated by HARVEST-001; what exact review/triage/adjudication artifacts caused those changes; and has any later accepted authority losslessly absorbed every live human decision?

This is an authority-recovery and provenance court. It is **not** a request to recompute drivers, infer semantics, or choose a preferred version by recency.

## Why this is now the smallest next request

HARVEST-001 proved that the question-structure/manual core is invariant and recovered. It separately proved that the oldest→June register transition changes 13,330 cells across 2,148 rows, entirely in these driver/semantic fields:

- `final_driver_id`
- `final_driver_scope`
- `final_driver_label`
- `final_driver_origin`
- `semantic_scope`
- `semantic_primary_driver`
- `semantic_secondary_driver`
- `semantic_shared_driver`
- `semantic_notes`

The historical/current driver-master versions are already content-identified, but their human review lineage and lossless supersession are not adjudicated.

HARVEST-002 closed a different question: current-35 identity authority exists, while its accepted SWID repair was not inherited by current control. Do not widen HARVEST-003 back into source-wave identity or itinerary work.

## Search roots

- `/Users/matthewsmith/Desktop/Rawlsing`
- `/Users/matthewsmith/Desktop/RawlsingsExcess`

## Exact target identities

### `questions_master_semantic.csv`

Recover every occurrence and exact bytes for at least these known identities:

- `171d399da7e0f2bbd66dcce08a6c353978e48b69fee8d32ac6b1720d10d70ca5`
  - known size: `6,586,323` bytes
- `6e76965c1e00c90e1ae4a4647f99b851dc558a345c2a2792151143cb35fe2fc0`
  - known size: `3,067,321` bytes

### `questions_master_drivers.csv`

Recover every occurrence and exact bytes for:

- `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`
  - `16,864,669` bytes
- `53feb28296705d2005f8c3d2548c136e2c15fabd62c103694f05caa555063711`
  - `3,683,893` bytes

Known locations include:

- `/Users/matthewsmith/Desktop/Rawlsing/data/final_codebooks/questions_master_drivers.csv`
- `Rawlsing_RETRIEVAL_PACKAGE_20260808/staging/04_QSM_ONTOLOGY_AUTHORITY/data/final_codebooks/questions_master_drivers.csv`
- historical `RawlsingDriverBundle_recovered/{canonical,raw_inputs}/questions_master_drivers.csv`

Do not assume any of these is canonical from its location.

## Narrow provenance / review targets

Search exact names and provenance terms only where they bear on the four target master identities or the nine changed fields:

- `questions_master_semantic.csv`
- `questions_master_drivers.csv`
- files whose names contain `driver` plus `triage`, `review`, `gap`, `adjudication`, `facet`, `assignment`, `mapping`, or `authority`
- files whose names contain `semantic` plus `triage`, `review`, `master`, `adjudication`, or `authority`
- driver/facet registries, taxonomies or mapping tables explicitly read by a target builder/updater
- builders/updaters/scripts that explicitly read one target master and write another target master or write any of the nine fields above
- READMEs/manifests/receipts containing one of the four exact target SHA-256 identities
- READMEs/manifests/receipts explicitly claiming semantic-master/driver-master replacement, promotion, retirement, migration, supersession or preservation
- explicit reviewer/status/basis/provenance surfaces referenced by those builders/updaters

Do **not** collect unrelated QSM/FQRA/V550 artifacts merely because they mention drivers. Follow an exact filename, SHA, path, import/input, output or provenance clue from the target lineage.

Inspect archives only when an exact filename/SHA/provenance clue points inside. Do not sweep unrelated archives or gigabytes.

## Mechanical evidence requested

For every occurrence of every responsive artifact:

- absolute path
- SHA-256
- size
- mtime
- ordinary file versus archive member
- archive/member path and member SHA where applicable
- exact-duplicate group

For each of the four target master CSV identities:

- exact header
- exact row count
- candidate row-key columns mechanically available in the file
- uniqueness/null counts for those candidate keys
- distinct-count/value-count summaries only for columns whose names explicitly indicate driver, facet, semantic, review, status, basis, authority, provenance, source, wave, question or variable identity

For each old→new pair (`questions_master_semantic` and `questions_master_drivers`):

1. determine a **mechanical** stable row-key only if the columns make one exact and unambiguous;
2. if such a key exists, report:
   - rows only old
   - rows only new
   - rows present in both
   - changed rows
   - changed cells by column
   - unchanged cells by column where useful
3. if no exact key is mechanically defensible, say so and do not invent one.

For every responsive builder/updater:

- exact input filenames
- exact output filenames
- exact key/join/filter columns
- exact columns assigned/written
- any explicit manual-review/status/basis/provenance columns read or written
- any explicit file/row selection law
- do not interpret the semantic correctness of assignments.

For every responsive triage/review/adjudication artifact:

- exact header/schema
- exact row count
- mechanically report reviewer/review/status/basis/provenance/date columns
- mechanically report which target row keys/driver/facet fields it references
- do not decide whether a human judgment was right.

## Required returned ZIP

One bounded ZIP containing:

- `README.md`
- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `SEMANTIC_MASTER_MECHANICAL_RECEIPT.json`
- `DRIVER_MASTER_MECHANICAL_RECEIPT.json`
- `MASTER_PAIR_DIFF_RECEIPT.json`
- `BUILDER_UPDATER_LINEAGE_RECEIPT.csv`
- `REVIEW_TRIAGE_LINEAGE_RECEIPT.csv`
- `ARCHIVE_MEMBER_MANIFEST.csv` if archives were inspected
- `payload/` exact bytes of the four target masters plus only narrow responsive provenance/review/build artifacts

`EVIDENCE_MANIFEST.csv` must preserve:

`archive_relative_path,original_absolute_path,sha256,size_bytes,mtime_local,artifact_name,browser_request_id,collection_reason,exact_duplicate_group_if_known`

`SEARCH_RECEIPT.md` must state roots searched, exact patterns/SHAs, omitted roots, found/not-found results, errors, archives inspected, and transformations. Expected transformation of payload bytes: none.

## Forbidden

- no delete/move/rename/edit/normalize;
- no builder/updater execution;
- no regeneration of any semantic or driver master;
- no semantic interpretation;
- no LLM-derived driver/facet assignment;
- no selection of a canonical version by recency, size, path, row count or apparent completeness;
- no claim that a later QSM/FQRA/V550 artifact losslessly supersedes these masters without explicit positive evidence;
- no raw survey microdata;
- do not reopen `EXP-001 QUESTION_STRUCTURE`, whose manual/source-topology core is already recovered.

Return the ZIP to HQ for Browser adjudication.

`AUTHORITY_CENSUS_LOCAL_HARVEST_REQUEST__HARVEST_003`
