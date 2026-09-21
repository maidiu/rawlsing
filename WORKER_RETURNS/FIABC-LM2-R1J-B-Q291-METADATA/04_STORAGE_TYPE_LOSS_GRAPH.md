# FIABC-LM2-R1J-B — Storage-Type Loss Graph

## Holding

The Q291 storage type was **captured and persisted**, then discarded in the R6S structural-preimage representation.

It was not "never captured."

## Graph

```text
Exact WVS7 SAV
SHA256 2bd2a20f...09af7d
        |
        | pyreadstat 1.3.6 metadata-only
        v
rawlsing_next/pre553_physical_decoder.py
blob 86109c4a...34bfb48f03f78
        |
        | metadata.readstat_variable_types[name]
        |              -> PhysicalVariable.storage_type
        | metadata.original_variable_types[name]
        |              -> display_metadata.format
        v
R35/FIABC physical incidence / ordered variable inventory
        |
        | Q291G5 @ 388 storage_type = "double"
        | Q291P5 @ 394 storage_type = "double"
        v
WORKER_RETURNS/FIABC-LM2/wvs7_physical_evidence_material.json
blob 0b4012e8...d68e4e8
        |
        | variable_inventory_order digest
        | c157802e...748886e66
        v
FIABC-LM2 canonical physical expectation
identity 9845c24d...48d02390
status PASS_PHYSICAL_ONLY
        |
        | independent parallel structural path
        +------------------------------------------+
                                                   |
                                                   v
EE-P2R6S 05_WVS7_PROJECTION_MATERIALIZER.py
blob d1dfe705...69d4ad
                                                   |
                                                   | metadata-only SAV read occurs,
                                                   | but PhysicalVariable is built with
                                                   | storage_type = None
                                                   v
projection_structural_input(...)
                                                   |
                                                   | serializes ordinal/name/
                                                   | missing_declarations only
                                                   | storage_type omitted
                                                   v
EE_P2R6S_WVS7_PROJECTION_STRUCTURAL_INPUT@1.0.0
                                                   |
                                                   | materialize_from_structural_input
                                                   | reconstructs PhysicalVariable(..., None, ...)
                                                   v
R1I structural replay sees storage_type = null
```

## Exact loss boundaries

### Physical decoder: type captured

`rawlsing_next/pre553_physical_decoder.py` blob
`86109c4a0b7ebd9b66e3b531b6334bfb48f03f78`

Relevant implementation:

- display metadata takes `metadata.original_variable_types[name]`;
- `PhysicalVariable.storage_type` takes `metadata.readstat_variable_types[name]`.

This is the source of the persisted `"double"` declarations.

### R6S inspection: type discarded immediately

`WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py` blob
`d1dfe705fa4da56036bd472af18536da1f69d4ad`

The function `inspect_wvs_sav_structure_and_country` performs:

`pyreadstat.read_sav(..., metadataonly=True, apply_value_formats=False, user_missing=True)`

but then creates each variable with:

`storage_type=None`.

The loss therefore occurs **after metadata acquisition and before structural-variable construction**.

### Structural serialization: omission made durable

The same file's `projection_structural_input` serializes each variable as only:

- `ordinal`;
- `name`;
- `missing_declarations`.

No `storage_type`, original format, display metadata, or topology metadata is serialized.

### Structural replay: null reconstituted

`materialize_from_structural_input` reconstructs each variable with the third positional field `None`, preserving the information loss.

## Why R1I's null is not contradictory evidence

R1I correctly reported that its **structural replay** had `storage_type = null`. That replay is a deliberately reduced derivative. It is not the only persisted physical artifact.

The sealed lineage simultaneously contains the separately governed R35/FIABC physical evidence object with exact type metadata. The two artifacts answer different questions:

- R35/FIABC physical evidence: what physical decoder metadata was observed and frozen?
- R6S structural input: what reduced fields were retained for projection materialization?

The first retains type; the second discards it.

## Authority limit

Recovering this loss does not by itself create an A→B representation authority.

The exact lawful fan-in remains:

```text
Worker B:
exact Q291 SAV variable metadata = double
+
Worker A:
upstream SAV/ReadStat/pyreadstat representation law
and 1.3.2 / 1.3.6 parity
+
Worker C/HQ:
bounded Rawlsing representation authority
=
possible lawful physical->native representation repair
```

No global float/int equivalence follows.
