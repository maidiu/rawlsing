# FIABC-R35-I01 — Implementation Diff Inventory

## Production

### `rawlsing_next/pre553_physical_decoder.py`

#### Added physical-metadata contract constants
- `PHYSICAL_METADATA_CONTRACT = PRE553_PHYSICAL_METADATA@1.0.0`
- `DECODER_IMPLEMENTATION_ID = rawlsing_next/pre553_physical_decoder.py`

#### Extended `PhysicalSourceIncidence`
- property `physical_metadata_digest`
- method `require_physical_metadata_digest(expected_digest)`

The existing six constructor fields remain in their prior order. No source-specific constructor fork was introduced.

#### Added canonical metadata receipt functions
- `build_physical_metadata_payload(...)`
- `compute_physical_metadata_digest(...)`
- `_canonical_json_sha256(...)`
- `_validate_file_metadata_contract(...)`

Digest preimage binds:
- exact canonical source SHA supplied by the incidence;
- source format;
- exact reader configuration;
- full file metadata contract;
- ordered per-variable physical metadata:
  - ordinal/name;
  - storage type;
  - decoded physical label/dictionary evidence;
  - missing declarations;
  - display metadata;
  - topology metadata.

This is metadata-only and intentionally does not substitute for a raw-cell stream digest or derivative ancestry receipt.

#### Added raw-layout extraction
- `_raw_layout_declarations(...)`
- `_sav_header_layout(...)`
- `_reader_declared_layout(...)`

SAV fixed-header fields retained when recognizable:
- record type;
- integer endianness;
- layout code;
- nominal case size;
- compression;
- weight index;
- declared case count;
- exact fixed-header prefix digest.

DTA currently retains:
- exact raw header-prefix digest;
- header-prefix length;
- explicit no-semantic-inference parse status;
- reader-declared physical layout fields.

Unknown/truncated SAV headers are preserved as raw fingerprints with fail-explicit parse status. They are not guessed.

#### Replaced flat-only `file_metadata` construction with a backward-compatible contract

Legacy keys remain:
- `file_encoding`
- `file_format`
- `number_columns`
- `number_rows`

New required keys:
- `contract_schema`
- `raw_layout_declarations`
- `normalized_geometry`
- `display_metadata`
- `decoder_identity`

`raw_layout_declarations` and `normalized_geometry` are deliberately separate, so internal disagreements survive.

#### Reader configuration strengthened
Now binds:
- reader name;
- reader version;
- decoder implementation identity;
- physical metadata contract version;
- `user_missing=True`;
- `apply_value_formats=False`;
- exact encoding override;
- compatibility authority status.

## Tests

### `rawlsing_next/tests/test_r35_i01_physical_metadata.py`

Synthetic-only hostile court. No canonical raw carriers.

Cases:
- `test_nominal_header_count_and_traversed_stream_width_both_survive`
- `test_metadata_mismatch_is_preserved_not_normalized`
- `test_display_format_remains_distinct_from_stored_magnitude`
- `test_candidate_representation_dropping_physical_witness_is_rejected`
- `test_equal_semantic_projection_can_have_unequal_required_physical_metadata_digest`
- `test_reader_config_is_bound_into_physical_metadata_digest`

## Reports

Added:
- `WORKER_RETURNS/FIABC-R35-I01/00_RETURN.md`
- `WORKER_RETURNS/FIABC-R35-I01/01_IMPLEMENTATION_DIFF_INVENTORY.md`
- `WORKER_RETURNS/FIABC-R35-I01/02_PHYSICAL_METADATA_CONTRACT.md`
- `WORKER_RETURNS/FIABC-R35-I01/03_TEST_PROTOCOL.md`
- `WORKER_RETURNS/FIABC-R35-I01/RETURN.json`

## Explicitly untouched
- derivative ancestry / preserved-carrier parentage;
- WVS structural preimage parentage;
- Candidate A/B/C source binding;
- I05 semantic parity;
- source-specific projection authority;
- measured P2X execution;
- canonical raw sources.
