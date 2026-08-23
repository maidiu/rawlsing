# HARVEST-001 — QUESTION_STRUCTURE_REGISTER_LINEAGE

Status: `ISSUED__AWAITING_LOCAL_PACKET`

## Exact authority question

Which exact historical/current `question_structure_register.csv` lineage carries the live question-structure semantic capital declared as **18,792 rows / 562 manual-review rows**; how do all distinct CSV, YAML-summary, builder, source-audit, taxonomy and driver-master versions relate; and has any later authority product losslessly absorbed every live decision?

This is recovery/adjudication, **not regeneration**.

## Search roots
- `/Users/matthewsmith/Desktop/Rawlsing`
- `/Users/matthewsmith/Desktop/RawlsingsExcess`

## Known distinct target identities already found

### `question_structure_register.csv`
- `f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84` — 23,612,534 bytes
- `15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b` — 26,582,348 bytes
- `9139c1ab77bf47a872f63ccae7784f3631f03a3e02a936b4ac41e75580c45219` — 26,582,238 bytes

### `build_question_structure_register.py`
- `3cabb94b84e7e498cfc56c4d579d58047744ef545faae2e03586a7d5f0856175` — 13,522 bytes
- `3d271c55e1596973a6e698919372b065ae5c279244aee877fbcddc2787ee0b69` — 11,538 bytes

### `question_structure_register.yaml`
- `0688635931b8fa9bd3461963256c8d71f3c623bdc55cde213d2101f1dbfbe05c` — 1,003 bytes
- `56a344f5149b67ffb53e1f02ed1da5e0c6226b29dd29ebe15965c850b0152e28` — 1,008 bytes

Do **not** assume newest/largest/same-row-count means canonical.

## Exact names / aliases to search
- `question_structure_register.csv`
- `question_structure_register.yaml`
- `question_structure_register.yml`
- `build_question_structure_register.py`
- `source_structure_validation_manifest.csv`
- `build_source_structure_validator.py`
- `question_type_taxonomy.yaml`
- `question_handling_schema_registry.csv`
- `questions_master_drivers.csv`
- `question_family_registry.yaml`
- row-level source-structure audits referenced by builders/manifests
- README/manifests/receipts containing `18792`, `562`, `manual_review`, `manual review`, or an exact target SHA
- bridge/crosswalk/provenance files explicitly claiming FQRA R1 or another later artifact absorbed the structure register

Inspect archives only when a filename/SHA/provenance clue points into them. Do not sweep unrelated gigabytes.

## Mechanical evidence requested

For every occurrence of every distinct target SHA:
- absolute path, SHA-256, size, mtime;
- ordinary file versus archive member;
- archive and member paths/member SHA where applicable.

For each distinct register CSV:
- exact header and row count;
- purely mechanical value/null counts for columns whose names explicitly indicate `manual_review`, `review`, `status`, `authority`, `basis`, `classification`, or `provenance`;
- do not interpret those values.

For each YAML:
- top-level keys;
- declared row/manual-review counts;
- named input/output paths and hashes if present.

For each builder:
- exact mechanically referenced input/output filenames;
- columns read/written;
- explicit filter/join/key column names;
- no semantic adjudication.

For source-structure validation inputs:
- exact header/row counts;
- mechanically stated relationship to register generation.

## Required returned ZIP

One bounded ZIP containing:
- `README.md`
- `EVIDENCE_MANIFEST.csv`
- `SHA256SUMS.txt`
- `SEARCH_RECEIPT.md`
- `SCHEMA_COUNTS.csv`
- `ARCHIVE_MEMBER_MANIFEST.csv` if archives were inspected
- `payload/` exact bytes of every distinct responsive target CSV/YAML/builder and narrow provenance input

`EVIDENCE_MANIFEST.csv` columns:
`archive_relative_path,original_absolute_path,sha256,size_bytes,mtime_local,artifact_name,browser_request_id,collection_reason,exact_duplicate_group_if_known`

`SEARCH_RECEIPT.md` must record roots, exact search patterns, omitted roots, found/not-found results, errors, archives inspected/collected, and transformations (expected: none).

## Forbidden
- no deletion/move/rename/edit/normalization;
- no builder execution/regeneration;
- no raw survey microdata;
- no semantic interpretation;
- no canonical-version selection;
- no lossless-supersession claim from recency, basename, row count or similar columns.

Return the ZIP to HQ for browser adjudication.
