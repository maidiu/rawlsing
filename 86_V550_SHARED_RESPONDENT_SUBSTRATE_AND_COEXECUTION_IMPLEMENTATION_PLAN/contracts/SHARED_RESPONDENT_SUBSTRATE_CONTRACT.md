# Shared respondent substrate contract

## Contract name and version

```text
V550_SHARED_RESPONDENT_SUBSTRATE
schema_version: v1
execution_contract_version: v550-v550j-coexecution-v1
```

## Canonical storage location

Within each V550 shard:

```text
<shard_path>/checkpoints/respondent_substrate/
  source=<source_slug>/
    wave=<canonical_wave_slug>/
      country_code=<country_code_slug>/
        v550_shared_respondent_substrate.parquet
        v550_shared_respondent_substrate.schema.json
        v550_shared_respondent_substrate_manifest.json
        v550_shared_respondent_substrate_validation.json
        COMPLETE
```

Temporary writes use sibling files prefixed with `.` and suffixed `.tmp`. `COMPLETE` is written last and atomically.

## Row surface

The row surface must be compatible with V550J's existing `PREPARED_SUBSTRATE_REQUIRED_COLUMNS`. Do not create a second, incompatible respondent schema.

The implementation should move or re-export the shared schema through a neutral module so V550 and V550J can both import it without a circular dependency.

Recommended new neutral module:

```text
35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/
  runtime_reproducibility_code/data/ddm_build_copy/
    ddm_v550_shared_respondent_substrate.py
```

Required compatibility rule:

- existing imports of `PREPARED_SUBSTRATE_REQUIRED_COLUMNS` and existing public functions in `build_v550j_prepared_substrate.py` must continue to work;
- compatibility wrappers or re-exports are preferred over breaking moves.

## Required row columns

At minimum, retain every existing V550J prepared-substrate required column, including:

- run/source/wave/country identity;
- `respondent_id` and `respondent_id_norm`;
- weight fields;
- `var_code`, `var_code_norm`, `question_id`, `question_text`;
- raw and normalized response fields;
- missingness flags;
- semantic response role and directionality authority;
- target/condition resolution;
- source-structure and question-use fields;
- normalized source/wave/country fields.

Additive row columns are permitted only where they are row-specific. Recommended additions:

```text
shard_id
selection_role                  # BASE_ONLY | JOINT_ONLY | BASE_AND_JOINT
base_fixture_selected           # boolean
joint_configuration_selected    # boolean
joint_configuration_ids_json    # sorted JSON array, empty for base-only rows
```

Do not duplicate release-wide hashes in every row; store them in the manifest.

## Question selection surfaces

The manifest must carry sorted exact lists and hashes for:

```text
base_question_ids
base_var_codes
joint_required_question_ids
joint_required_var_codes
union_question_ids
union_var_codes
base_only_var_codes
joint_only_var_codes
overlap_var_codes
```

Required invariants:

```text
union = base ∪ joint_required
base_only = base - joint_required
joint_only = joint_required - base
overlap = base ∩ joint_required
```

No question may enter the SQL extraction unless it is in the union surface.

No question may enter ordinary V550 per-question processing unless it is in the base surface.

No joint configuration may be compiled unless all of its required applicable items are represented in the joint-required surface or explicitly governed as unavailable/not-applicable.

## Manifest fields

The manifest must include at least:

```text
schema_version
execution_contract_version
run_id
shard_id
source
source_id
wave
canonical_wave
country_code
respondent_relation
respondent_relation_schema_hash
postgres_server_version
transaction_isolation
transaction_snapshot                 # when available
query_signature_hash
query_parameter_hash
base_selection_hash
joint_selection_hash
union_selection_hash
response_semantics_contract_hash
question_family_registry_hash
joint_configuration_authority_release_id
joint_configuration_adjudication_set_hash
p3_authority_release_id
authority_compendium_hash
row_count
respondent_count
var_count
substantive_row_count
missing_row_count
duplicate_scalar_response_key_count
content_hash
schema_hash
parquet_file_sha256
created_at_utc
cache_valid
validation_status
```

`created_at_utc`, server version, and snapshot metadata are audit fields and must not contaminate the logical content hash.

## Logical content hash

Do not use the Parquet byte hash as the sole content identity because Parquet encoding metadata can vary by library version.

Compute a logical content hash from canonical row values:

1. Select a fixed ordered list of content columns.
2. Normalize nulls and scalar representations deterministically.
3. Serialize each row as canonical JSON with sorted keys.
4. Hash each row.
5. Sort the row hashes lexicographically, preserving multiplicity.
6. Hash the canonical list of row hashes plus schema version.

This makes the logical hash independent of row order while still detecting duplicate multiplicity and content changes.

The Parquet file SHA-256 remains a transport/integrity checksum.

## Duplicate policy

Do not blindly deduplicate.

- Scalar-response questions should ordinarily have no more than one substantive row per `(source, wave, country, respondent_id_norm, var_code_norm)`.
- Explicit multiselect child representations may legitimately produce multiple distinct child rows.
- The validator must classify duplicates by question mapping type and fail only on unauthorized duplicate scalar response keys.

## Atomicity

The write sequence is:

1. create parent directories;
2. write temporary Parquet;
3. write temporary schema;
4. compute file and logical hashes;
5. write temporary manifest;
6. load temporary Parquet back;
7. run full validation against manifest;
8. write temporary validation return;
9. atomically rename all four artifacts;
10. atomically write `COMPLETE` last.

A substrate without `COMPLETE` is unusable.

## Cache validity

A cache is valid only when all of the following match:

- schema version;
- source/wave/country;
- union selection hash;
- response semantics contract hash;
- registry hash;
- Section 85 joint authority release and adjudication-set hash;
- P3 authority release;
- respondent relation schema hash;
- compiler/execution contract version;
- file SHA-256;
- logical content hash;
- validation status `pass`;
- `COMPLETE` marker present.

Any mismatch causes fail-closed rebuild or fail-closed refusal according to the selected substrate mode.

## Sensitive-data handling

The shared respondent substrate must not be written through `--write-csv`.

Required protections:

- directory mode `0700` and file mode `0600` where supported;
- clear `.gitignore` coverage;
- package builders must explicitly exclude `checkpoints/respondent_substrate/**`;
- logs may include counts and paths, never raw respondent IDs or response rows;
- validation returns may include only aggregate diagnostics and bounded example hashes, never raw records.
