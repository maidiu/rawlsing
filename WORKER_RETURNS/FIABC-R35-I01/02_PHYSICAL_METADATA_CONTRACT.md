# FIABC-R35-I01 — Physical Metadata Contract

Schema:

`PRE553_PHYSICAL_METADATA@1.0.0`

## 1. Purpose

This contract preserves physical source evidence that can be lost even when a candidate produces the same bounded semantic projection.

It exists to prevent:

`SEMANTICALLY_EQUAL_AT_CURRENT_PROJECTION`
from being mistaken for
`PHYSICALLY_EQUIVALENT_AT_REQUIRED_SOURCE_SCOPE`.

It is physical evidence only.

It has no authority to decide:
- survey meaning;
- intended text semantics;
- routing/applicability;
- weight or design use;
- respondent identity;
- population;
- release legitimacy;
- source certification.

## 2. Required evidence domains

A valid metadata receipt contains four distinct domains.

### A. Raw layout declarations

Path:

`file_metadata.raw_layout_declarations`

Contains:

1. reader-declared physical layout fields;
2. format-native raw-header evidence.

For SAV, the generic format plugin preserves the fixed-header declarations when recognizable:
- record type;
- layout code;
- integer endianness;
- `nominal_case_size`;
- compression;
- weight index;
- declared case count.

It also preserves the exact fixed-header-prefix SHA-256.

For DTA, this commission preserves the raw header-prefix SHA-256 and reader-declared layout fields, while marking the native prefix as not semantically interpreted by this contract.

### B. Normalized traversed geometry

Path:

`file_metadata.normalized_geometry`

Contains:
- traversed dictionary variable count;
- traversed stream cell width;
- traversed row count;
- ordered `ordinal/name` variable inventory.

These values describe the decoder's normalized traversal surface.

They are not permitted to overwrite the raw header/layout declarations.

### C. Display metadata

Path:

`file_metadata.display_metadata`

Ordered by variable ordinal.

Each entry binds:
- variable ordinal;
- variable name;
- storage type;
- display metadata.

Display metadata is evidence about representation only.

`display format != raw storage value`

remains a hard physical distinction.

### D. Reader / decoder / configuration identity

Two surfaces bind execution identity:

`reader_configuration`

and:

`file_metadata.decoder_identity`

The current reader configuration contains:
- `reader`;
- `reader_version`;
- `decoder_implementation`;
- `physical_metadata_contract`;
- `user_missing`;
- `apply_value_formats`;
- explicit encoding;
- compatibility authority status.

A compatibility decode remains:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Nothing in this receipt promotes compatibility text to source-text semantics.

## 3. Mismatch law

If two physical witnesses disagree, both are preserved.

Example shape:

```text
raw_layout_declarations.format_native_header.nominal_case_size = 174
normalized_geometry.traversed_dictionary_variable_count = 332
normalized_geometry.traversed_stream_cell_width = 332
```

The contract does not contain a field such as:
- corrected count;
- resolved count;
- authoritative count.

A later source-specific authority court may determine what a declaration means for a specific claim. This decoder contract does not.

## 4. Digest

`PhysicalSourceIncidence.physical_metadata_digest`

is SHA-256 over canonical JSON containing:

```text
schema
source_sha256
source_format
reader_configuration
file_metadata
ordered variable physical metadata
```

Ordered variable physical metadata binds:
- ordinal;
- name;
- storage type;
- physical decoded label evidence;
- value-label dictionary evidence;
- missing declarations;
- display metadata;
- topology metadata.

The digest therefore changes if a required physical witness changes even when a later semantic projection remains equal.

## 5. Fail-closed requirement

Before digest construction, these top-level file metadata witnesses are mandatory:

- `raw_layout_declarations`
- `normalized_geometry`
- `display_metadata`
- `decoder_identity`

Dropping one raises `DecoderError`.

This prevents a candidate from presenting a smaller metadata object and claiming equivalence merely because its remaining fields are internally self-consistent.

## 6. Candidate-neutral use

The schema and digest construction are candidate-neutral.

A/B/C may use different internal representations only if the governing later physical-equivalence court can reproduce the required receipt evidence exactly for the declared scope.

This contract does not itself declare A/B/C equivalent.

R35-I03 owns that whole-source equivalence decision.

## 7. Relation to sibling work

### R35-I02
Owns:
- derivative identity;
- producer/operation/config parent receipt;
- canonical parent SHA proof;
- preserved LiTS R5 ancestry;
- WVS structural-preimage ancestry.

This I01 digest is not parentage.

### R35-I03
Owns:
- applicable edge-class declaration;
- whole-source physical-equivalence receipt;
- candidate closure against canonical expectation.

I03 may consume I01 metadata/digest.

### I05
Owns semantic parity at its declared claim frontier.

I05 equality cannot erase I01 metadata inequality.

## 8. Backward compatibility

Legacy `file_metadata` keys remain:
- `file_encoding`;
- `file_format`;
- `number_columns`;
- `number_rows`.

They continue to expose normalized geometry for existing consumers.

The new raw-layout witness is additional evidence, not a reinterpretation of those legacy keys.

## 9. Prohibited use

Forbidden:

`raw header value -> survey meaning`

`display format -> stored magnitude`

`compatibility decoding -> intended source text`

`metadata digest equality -> source certification`

`metadata digest equality -> derivative ancestry`

`metadata digest inequality -> automatic semantic divergence`
