# SOURCE CERT PREP71 — COMMON PACKET CONTRACT

Status: `FROZEN__NON_DISPOSITIVE_PACKET_SCHEMA`

Parent: `../71_REMAINING_34_SOURCE_CERTIFICATION_PACKET_PREPARATION_AUTHORITY.md`

## Worker role

Prepare future source-certification evidence. Measure, cite, and package. Do not certify, redesign, or invent semantics.

## Mandatory workflow

1. Verify exact worker branch/start HEAD and current Authority 71.
2. Read the accepted family SR09-PRE return plus R10 exception queue before touching raw bytes.
3. Locate required Library raw bundle(s) by exact filename; materialize to worker-private scratch; verify frozen bundle identity; extract only assigned members; verify each source SHA against `SOURCE_BYTE_INVENTORY.csv`.
4. Search Library for source-native codebooks/questionnaires/methodology/documentation relevant to named burdens. Prefer source-native documentation over general web material. Web research is allowed only to locate authoritative source documentation when Library/repository evidence is absent; clearly mark it external and do not let it silently outrank exact source bytes.
5. Use targeted raw probes only to make hostile fixtures executable or resolve named physical ambiguity. Do not blindly full-scan files already covered by SR03.
6. Separate measured physical fact, documentary semantic authority, Rawlsing governing interpretation, inference, and unresolved authority gap.
7. Produce required outputs and commit only small evidence/receipts.

## Required ledger columns

`SOURCE_CERTIFICATION_LEDGER.csv`:

`worker_id,family,source_file,source_sha256,format,decoder_config,compatibility_status,sr03_anchor,sr09_burden_summary,documentary_authority_status,hostile_fixture_count,family_reuse_status,future_court_requirements,packet_disposition,notes`

`HOSTILE_FIXTURES.csv`:

`worker_id,family,source_file,source_sha256,fixture_id,fixture_kind,row_ordinal,var_ordinal,var_name,physical_state_expected,raw_value_expected_json,metadata_expected_json,documentary_expected_json,assertion_scope,purpose,authority_status`

`DOCUMENTARY_AUTHORITY_MAP.csv`:

`worker_id,family,source_file,topic,document_name,library_file_id_or_repo_path,location,authority_claim,authority_strength,unresolved_caveat`

`AUTHORITY_GAPS.csv`:

`worker_id,family,source_file,gap_id,gap_class,affected_entities,what_source_bytes_prove,what_documents_prove,what_remains_unknown,why_it_matters,later_authority_needed,blocking_level`

`FAMILY_REUSE_AND_DRIFT.csv`:

`worker_id,family,rule_or_fixture,source_a,source_b,reuse_or_drift,evidence,bounded_reuse_law,source_specific_exception`

## Fixture kinds

Use one of:

- `CELL_PHYSICAL_STATE`
- `CELL_RAW_VALUE`
- `VARIABLE_MISSING_DECLARATION`
- `VALUE_LABEL_DICTIONARY`
- `VARIABLE_LABEL`
- `VARIABLE_TYPE_FORMAT`
- `SOURCE_ENCODING_READER_CONFIG`
- `MULTIPLE_RESPONSE_TOPOLOGY`
- `REPEATED_RANKED_SLOT_TOPOLOGY`
- `ROW_IDENTITY_REPLAY`
- `COUNTRY_REGION_COORDINATE`
- `WEIGHT_DESIGN_CANDIDATE`
- `ROUTING_MODULE_TOPOLOGY`
- `RAW_HEADER_DICTIONARY_STRUCTURE`
- `DISPLAY_STORAGE_SEPARATION`
- `OTHER_NAMED_METADATA_ASSERTION`

A metadata fixture may have blank row/variable ordinals.

## Documentary authority strength

Use:

- `SOURCE_NATIVE_EXPLICIT`
- `SOURCE_NATIVE_PARTIAL`
- `REPOSITORY_GOVERNED`
- `EXTERNAL_OFFICIAL_SUPPORTING`
- `INSUFFICIENT_FOR_SEMANTIC_AUTHORITY`

Do not elevate compatibility decoding, a label string, a variable name, or a distribution to source-native semantic authority.

## Future execution order

`FUTURE_EXECUTION_ORDER.md` must specify, per source:

`source SHA -> decoder/config -> hostile physical fixtures -> metadata/topology fixtures -> documentary semantic assertions -> exact carrier/C11 equivalence assertions -> negative/fail-closed fixtures -> future disposition gate`

It is a proposed future court order only. Do not execute certification or promote anything under Authority 71.

## Packet quality gate

A packet is ready only when a future executor would know:

- exactly which bytes to open;
- exactly which decoder/config to use;
- exactly what source-side facts must survive;
- exactly which semantic claims are supported by named documentary authority;
- exactly what must remain unknown;
- exactly what hostile fixtures to replay;
- exactly what causes fail-closed return.

## Git isolation

Write only in your assigned `SOURCE_CERT_PREP71/RETURNS/<RXX>/` directory. Do not modify shared law, runtime, other worker returns, or source files.

Required tokens:

- R01 `PRE553_SOURCE_CERT_PREP71_R01_RETURNED`
- R02 `PRE553_SOURCE_CERT_PREP71_R02_RETURNED`
- R03 `PRE553_SOURCE_CERT_PREP71_R03_RETURNED`
- R04 `PRE553_SOURCE_CERT_PREP71_R04_RETURNED`
- R05 `PRE553_SOURCE_CERT_PREP71_R05_RETURNED`
- R06 `PRE553_SOURCE_CERT_PREP71_R06_RETURNED`
- R07 `PRE553_SOURCE_CERT_PREP71_R07_RETURNED`
- R08 `PRE553_SOURCE_CERT_PREP71_R08_RETURNED`
- R09 `PRE553_SOURCE_CERT_PREP71_R09_RETURNED`
