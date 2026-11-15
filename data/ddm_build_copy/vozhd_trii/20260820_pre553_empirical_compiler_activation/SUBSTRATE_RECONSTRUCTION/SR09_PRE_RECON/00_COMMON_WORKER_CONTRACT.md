# SR09-PRE — COMMON WORKER CONTRACT

Status: `FROZEN_NON_DISPOSITIVE_RECON_CONTRACT__LIBRARY_FIRST`

Parent authority: `../29_SR09_PREPARATORY_RAW_SOURCE_RECONNAISSANCE_AUTHORITY.md`

Binding raw-input authority: `02_LIBRARY_RAW_INPUT_LAW.md`

## 1. Role

You are a bounded reconnaissance worker preparing evidence for later G-SR07/G-SR08/G-SR09 source certification.

You may measure and report. You may not decide architecture, semantic truth, source certification, or production behavior.

The raw source bytes remain immutable physical evidence.

## 2. Inputs

Use only:

- exact source files assigned in your worker task;
- the ChatGPT Library raw-source transport bundles frozen in `02_LIBRARY_RAW_INPUT_LAW.md`;
- `../SOURCE_BYTE_INVENTORY.csv`;
- accepted SR03 physical manifests / summary / receipt;
- `../09_SOURCE_NATIVE_CONSTITUTION.md`;
- `../10_FORMAT_DECODER_CONTRACT.md`;
- `../16_SR03_R3_ADJUDICATION.md`;
- `../17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`;
- checked-in source documentation or metadata already available in the repository.

Library-first procedure is mandatory: locate the named Library ZIP, materialize it into worker-private scratch, verify the frozen ZIP identity, extract only assigned substantive members, then verify every extracted member against the exact source SHA-256 before probing. STOP on mismatch.

Do not require or assume a `/Users/...` local source directory for SR09-PRE.
Do not use legacy PostgreSQL as source truth.

## 3. Read economy

Start with accepted SR03 census evidence. Do not rescan all cells merely because the source exists.

Target raw reads toward named burdens:

- physical missing-state examples;
- user-missing declarations/ranges;
- extended/system missing behavior;
- raw value + value-label coexistence;
- native ID candidate behavior;
- country/wave/region coding;
- weights/design variables;
- routing/applicability clues encoded physically;
- multiple-response sets;
- repeated/ranked/ordered slot topology;
- unusual encoding/Unicode metadata;
- cross-wave schema/coding drift;
- exact hostile sentinel cells.

If a full source scan is required, record the reason in `PROBE_RECEIPT.json`.

## 4. Required hazard taxonomy

Every nontrivial finding must use one or more of these stable classes:

- `PHYSICAL_MISSINGNESS`
- `SEMANTIC_CODE_CANDIDATE`
- `RESPONDENT_IDENTITY`
- `SOURCE_SCOPE_COORDINATE`
- `COUNTRY_REGION_CODING`
- `WEIGHT_DESIGN`
- `ROUTING_APPLICABILITY`
- `MULTIPLE_RESPONSE_TOPOLOGY`
- `REPEATED_RANKED_SLOT_TOPOLOGY`
- `ENCODING_TEXT_AUTHORITY`
- `VARIABLE_SCHEMA_DRIFT`
- `VALUE_CODING_DRIFT`
- `LABEL_METADATA_DRIFT`
- `FORMAT_READER_COMPATIBILITY`
- `LEGACY_LOSS_RISK`
- `OTHER_NAMED_PHYSICAL_HAZARD`

Do not create a semantic state merely from a label such as DK/refused/not applicable. Record it as `SEMANTIC_CODE_CANDIDATE` unless a checked-in source authority explicitly closes the meaning.

## 5. Reconnaissance dispositions

Only these are permitted:

- `NO_NOVEL_BURDEN_OBSERVED`
- `KNOWN_HAZARD_CLASS__SOURCE_SPECIFIC_FIXTURE_REQUIRED`
- `NEW_HAZARD_CLASS__HQ_ADJUDICATION_REQUIRED`
- `DOCUMENTARY_AUTHORITY_GAP`
- `PROBABLE_CERTIFICATION_BLOCKER`
- `RECONNAISSANCE_INCOMPLETE`

Never write `CERTIFIED`, `FAILED`, or certification-level `BLOCKED`.

## 6. Required output files

Write only under the exact worker directory assigned by your task.

### `RESULT.md`
Human-readable findings. Separate measured source facts from inference and unresolved authority.

### `RESULT.json`
Machine-readable summary containing:

- worker ID;
- family;
- exact source inventory;
- commands/probes executed;
- source-level reconnaissance dispositions;
- hazard-class counts;
- novel hazard classes, if any;
- documentary authority gaps;
- hostile sentinel count per source;
- whether any full scans were performed and why;
- explicit `non_dispositive=true`.

### `SOURCE_BURDEN.csv`
Columns exactly:

`worker_id,family,source_file,source_sha256,hazard_class,evidence_type,evidence_locator,measured_fact,certification_burden,recon_disposition,full_scan_required,notes`

### `HOSTILE_SENTINELS.csv`
Choose a small exact set of source-side facts that later C11 certification can replay.

Columns exactly:

`worker_id,family,source_file,source_sha256,sentinel_id,row_ordinal,var_ordinal,var_name,physical_state_expected,raw_value_expected_json,metadata_expected_json,purpose,authority_status`

Rules:

- row ordinals are source physical row ordinals, zero-based unless the source reader proves otherwise and that basis is recorded;
- variable ordinals are source-native physical ordinals;
- prefer exact cells that exercise a hazard rather than generic counts;
- also include non-cell metadata sentinels when necessary by using blank row ordinal and an exact metadata locator in `metadata_expected_json`;
- never infer semantic meaning solely to fill a sentinel.

### `CROSS_WAVE_DRIFT.csv`
Columns exactly:

`worker_id,family,source_a,source_b,drift_class,entity_or_variable,evidence,likely_certification_impact,authority_status`

### `AUTHORITY_GAPS.csv`
Columns exactly:

`worker_id,family,source_file,gap_class,affected_entities,evidence_present,evidence_missing,why_raw_bytes_insufficient,later_authority_needed`

### `PROBE_RECEIPT.json`
Record:

- exact checkout HEAD;
- Library bundle filename(s), byte size(s), and SHA-256;
- exact materialized scratch path(s);
- exact archive member names used;
- exact extracted source SHA-256 before probing;
- tool/dependency versions;
- exact commands/scripts;
- sources fully scanned, if any;
- target reason for every full scan;
- output-file SHA-256 values;
- Library/raw source files unchanged;
- `DATABASE_URL_used=false`;
- `legacy_postgres_used_as_truth=false`;
- `production_runtime_modified=false`;
- final git status.

## 7. Family comparison burden

Do not treat releases as independent bags of variables.

Measure within-family drift in at least:

- variable names/ordinals;
- source case counts;
- candidate respondent IDs;
- country/region/wave coordinates;
- missing-value declarations;
- labels/value-label dictionaries;
- weight/design candidates;
- multiple-response/repeated/ranked topology;
- encoding/reader configuration;
- obvious routing/form/module structures where physically represented.

The purpose is to identify which later certifications can reuse one family fixture law and which releases require source-specific hostile fixtures.

## 8. Forbidden

Do not:

- modify or upload-overwrite Library raw bundles;
- modify extracted raw source bytes;
- write C11 or runtime code;
- modify SR04/SR06 code or governance;
- modify production database contents;
- use `DATABASE_URL`;
- treat legacy database rows as correction authority;
- normalize values for convenience;
- drop missing/user-missing cells;
- guess encodings not frozen by authority;
- silently substitute source files;
- add a new source to CLOSED_35;
- certify a source;
- commit large extracted datasets.

## 9. Publication

Commit only your assigned output directory to your assigned worker branch.

Large temporary tables/extracts remain outside Git and are referenced in the receipt by path/hash only.

Return the worker branch name, exact commit SHA, summary disposition per source, novel hazards, authority gaps, sentinel counts, and `PROBE_RECEIPT.json` to HQ.
