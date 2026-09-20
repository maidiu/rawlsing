# FIABC-R35-I01 — Generic Raw Layout / Physical Metadata Preservation

Branch: `agent/rabochii-premain-fiabc-r35-i01-raw-layout-metadata-r1`

Base: `agent/vozhd-premain-fiabc-s35-fanin-r1@770d95c1a604ea1f47ac2971b923673c14c42984`

## Holding

The S35-3 EC04 gap is closed at the generic decoder-contract grain.

`PhysicalSourceIncidence` now preserves four independent physical witnesses without reconciling them:

1. raw format-native header/layout declarations;
2. normalized decoder traversal geometry;
3. per-variable display metadata distinct from raw storage;
4. exact reader/decoder/config identity.

A canonical metadata-only SHA-256 receipt is exposed as `PhysicalSourceIncidence.physical_metadata_digest`.

The receipt is candidate-neutral in schema and comparison law. It does **not** authorize survey semantics, source certification, routing, weight choice, respondent identity, or documentary interpretation.

## Implemented law

`RAW HEADER/LAYOUT WITNESS`
+
`NORMALIZED TRAVERSED GEOMETRY`
+
`DISPLAY METADATA`
+
`READER/DECODER/CONFIG IDENTITY`
→
`CANONICAL PHYSICAL METADATA DIGEST`

No side of a physical mismatch is corrected to the other.

For SAV inputs, the decoder preserves the fixed format-native header declarations separately from reader-normalized metadata. The SAV parser is generic: it reads the standard fixed header record, determines integer endianness from the layout code, and records `nominal_case_size`, compression, weight index, and declared case count when the header is recognizable. Unknown/truncated headers remain fingerprinted and explicitly unparsed rather than guessed.

For DTA inputs, the same contract preserves the exact raw header-prefix fingerprint plus reader-declared layout fields without inventing a format-semantic interpretation that this commission did not authorize.

## Positive hostile witness

The contract can simultaneously represent the accepted Latinobarometro 2024 condition:

- raw SAV `nominal_case_size = 174`;
- normalized dictionary / traversed cell width `= 332`.

Those values occupy different receipt paths and cannot overwrite one another.

This is not a Latinobarometro-specific adapter. Any SAV with an internal header-vs-traversal mismatch exercises the same path.

## Display-vs-storage witness

Per-variable display metadata remains preserved while raw cell extraction continues under `apply_value_formats=False`.

A display declaration such as `F2.0` therefore remains metadata and cannot truncate, rescale, or replace a 9-10 digit stored magnitude.

## Mechanical rejection surface

`build_physical_metadata_payload(...)` validates the metadata contract before digesting it.

A candidate representation that drops any required top-level witness:

- `raw_layout_declarations`;
- `normalized_geometry`;
- `display_metadata`;
- `decoder_identity`;

fails closed with `DecoderError`.

A candidate that retains the schema but changes any required physical witness receives a different SHA-256 digest.

Thus equal semantic projection does not imply equal required physical metadata.

## Changed production surface

- `rawlsing_next/pre553_physical_decoder.py`

Added:

- `PHYSICAL_METADATA_CONTRACT`;
- `DECODER_IMPLEMENTATION_ID`;
- generic SAV fixed-header physical parser;
- raw-layout receipt builder;
- normalized geometry receipt;
- ordered display metadata receipt;
- canonical physical metadata payload/digest;
- `PhysicalSourceIncidence.physical_metadata_digest`;
- `PhysicalSourceIncidence.require_physical_metadata_digest(...)`.

No source-specific semantic branch was added.

## Hostile tests

Added:

`rawlsing_next/tests/test_r35_i01_physical_metadata.py`

The court covers:

1. raw nominal/header count `174` versus traversed width `332`;
2. mismatch preserved rather than normalized;
3. display format distinct from stored magnitude;
4. candidate drops one required physical witness;
5. equal semantic projection with unequal physical metadata digest;
6. reader/config drift changes the digest.

The fixtures are synthetic and open no canonical raw source carrier.

## Execution boundary

No measured P2X was run.

This GitHub/browser worker did not open any local canonical raw source carrier.

No GitHub Actions status was attached to the implementation/test commit at inspection time. The tests are committed for fan-in/hostile qualification; no local execution result is claimed.

## Non-claims

This return does not:

- certify Latinobarometro 2024 semantics;
- make `174` or `332` semantically authoritative;
- implement derivative parentage (R35-I02);
- implement whole-source physical equivalence (R35-I03);
- replace I05 semantic parity;
- claim CLOSED_35 A/B/C execution.

Terminal:

`FIABC_R35_I01_GENERIC_RAW_LAYOUT_METADATA_PRESERVATION_IMPLEMENTED__READY_FOR_FANIN`
