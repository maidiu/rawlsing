# FIABC-LM2-R1J-B — Q291 Variable-Type / Metadata Archaeology

Status: `PASS`

Terminal:

`FIABC_LM2_R1J_B_Q291_METADATA_PASS__EXACT_BROWSER_ACCESSIBLE_Q291_VARIABLE_TYPE_EVIDENCE_RECOVERED`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-premain-fiabc-lm2-r1j-b-q291-metadata-archaeology-r1`

Exact base: `74205b23f546d78fed449c2f351a714be184ed8c`

## Holding

The missing Q291 physical/source-variable type fact is already persisted in the sealed FIABC-LM2 lineage.

The exact candidate-neutral physical evidence artifact:

`WORKER_RETURNS/FIABC-LM2/wvs7_physical_evidence_material.json`

Git blob:

`0b4012e85c65440df36475153a8ce0cd6d68e4e8`

was returned in commit:

`bf0f4ebb00e7304e1cda29f7ca9b6595fff248dc` — `Return FIABC-LM2 WVS7 source and physical blocker`.

Under:

`evidence_material.variable_inventory_order.ordered_inventory`

it persists the exact 613-variable physical inventory. The two commissioned variables are:

- `Q291G5`, ordinal `388`: `storage_type = "double"`, original/display format `F3.0`, storage width `8`, measure `nominal`, missing declaration `-5..-1`.
- `Q291P5`, ordinal `394`: `storage_type = "double"`, original/display format `F3.0`, storage width `8`, measure `nominal`, missing declaration `-5..-1`.

This is not inferred from carrier cells, value resemblance, labels, or frequencies.

## Why the type field is source/decoder metadata

The exact decoder blob bound by the physical expectation is:

`rawlsing_next/pre553_physical_decoder.py`
blob `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`.

At the generic decoder boundary, the physical variable constructor assigns:

- `metadata.readstat_variable_types[name]` -> `PhysicalVariable.storage_type`;
- `metadata.original_variable_types[name]` -> display/original format metadata.

Therefore the persisted `"double"` values are decoder metadata declarations, not deductions from observed respondent values.

## Exact source and decoder binding

`WORKER_RETURNS/FIABC-LM2/01_WVS7_CANONICAL_SOURCE_RECEIPT.json`
binds the metadata read to:

- source: `WVS Wave 7.sav`;
- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- bytes: `185163494`;
- rows: `97220`;
- variables: `613`;
- reader: `pyreadstat 1.3.6`;
- `metadataonly=true`;
- `apply_value_formats=false`;
- `user_missing=true`;
- no compatibility encoding override.

`WORKER_RETURNS/FIABC-LM2/04_WVS7_CANONICAL_PHYSICAL_EXPECTATION.json`
then freezes:

- expectation identity `9845c24da0c03adb4dfd65118b7c8c39a60a30337f33cc4177ffc6c848d02390`;
- physical metadata digest `ac24f5a7a624587c0072b9af937cd3d10abc7fdcd3537e7a2d2b98480d187110`;
- variable-inventory-order digest `c157802e0016b2c9045177f3ed76e8369db47ad433b0489cfeee4de748886e66`;
- decoder blob `86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`;
- reader/config identity above;
- verification state `VERIFIED`.

The FIABC-LM2 command ledger records this R35-I03 physical expectation as `PASS_PHYSICAL_ONLY`.

## Authority ceiling

This evidence is exact physical metadata and is sufficient for Worker B's burden:

> the exact SAV variables Q291G5 and Q291P5 are declared `double` by the accepted physical decoder metadata under the frozen pyreadstat 1.3.6 execution contract.

It does **not** prove:

- that a decoded Python `float 1.0` means WVS native code `1`;
- a global int/float equivalence;
- source-native response semantics;
- native-to-program mapping;
- cross-source relation;
- pyreadstat 1.3.2 / 1.3.6 parity.

The last item remains Worker A's independent burden.

## Historical loss archaeology

The type was **captured and persisted**, then discarded on the R6S structural-preimage path.

In `WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py`
blob `d1dfe705fa4da56036bd472af18536da1f69d4ad`:

1. `inspect_wvs_sav_structure_and_country` performs a metadata-only SAV read but constructs every `PhysicalVariable` with `storage_type=None`.
2. `projection_structural_input` serializes only `ordinal`, `name`, and `missing_declarations`; it omits `storage_type`.
3. `materialize_from_structural_input` reconstructs `PhysicalVariable(..., None, ...)`.

Thus R1I's observation that the structural replay has `storage_type = null` is correct for that structural derivative, but it is not evidence that source physical type was never captured. The independent R35/FIABC physical evidence retained it.

## Other searched surfaces

- EE-R6A: exact Q291 native semantics and source identity, but no physical type declaration.
- EE-P2F2: mechanical authority/objectization without SAV access; no physical type declaration.
- GSR07/HB01 source-backed certification: exact source identity/613-slot certification, but no exact Q291 type field in the returned receipts.
- GSR07 Actions run `34646731515`: two successful jobs; uploaded artifacts were tiny court receipts and logs exposed no Q291/readstat/storage-type metadata.
- historical SR03: implementation explicitly captured `readstat_variable_types` and `original_variable_types`, and HQ accepted a 35-source physical census; the returned ~40 MB manifest archive was not committed into the browser-accessible tree. It is therefore corroborating but not needed for this PASS.
- R35-I01: defines the generic physical-metadata contract and proves storage type is a required ordered-variable physical witness; no WVS semantics are issued by that contract.

## Actions boundary

No PR-triggered GitHub Actions workflow run is associated with the FIABC-LM2 return commit `bf0f4ebb00e7304e1cda29f7ca9b6595fff248dc`. The decisive evidence is the committed sealed artifact itself, not an ephemeral Actions artifact.

## Local fallback

No local fallback is required because the exact browser-accessible evidence exists. A metadata-only fallback is nevertheless frozen in `06_MINIMAL_METADATA_ONLY_FALLBACK.json` solely as a contingency; it was not executed.

No WVS SAV/ZIP was opened or materialized by this worker. No Candidate A/B/C, I03, I05, or measured P2X execution occurred.
