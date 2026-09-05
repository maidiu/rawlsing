# GT3/GT4 N2 — CHECKPOINT 1 — EXACT SOURCE VERIFIED

Status:

`PASS__GT34_N2_CHECKPOINT1_EXACT_ACCEPTED_R5_SOURCE_BYTES_VERIFIED__NO_ROW_VALUES_READ`

Exact working ancestry start:

`bca519e3d39b7c3886210958800a4b47ecb50440`

Evidence execution commit:

`4439afb47f620a1da6b229fe68e2386d77119510`

Governed court run:

`33997340315`

Governed court job:

`101390055906`

## Exact checkpoint material

```json
{"expected_rows":51587,"metadata_columns":348,"metadata_rows":51587,"official_url":"https://www.afrobarometer.org/wp-content/uploads/2022/02/merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav","parser":"pyreadstat","parser_version":"1.3.6","python_version":"3.12.14","required_variable_inventory":{"COUNTRY":0,"DATEINTR":36,"Q69B":226,"RESPNO":4},"row_values_committed":false,"row_values_read":false,"schema_id":"GT34_N2_Q69B_SOURCE_CHECKPOINT1@1.0.0","source_byte_count":49689458,"source_route":"OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION","source_sha256":"c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"}
```

## Court result

`1 passed, 1 warning in 7.50s`

The warning is the machine-readable checkpoint payload above.

## Frozen source identity

- route: `OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION`
- byte count: `49,689,458`
- SHA-256: `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`
- metadata rows: `51,587`
- metadata columns: `348`
- parser: `pyreadstat 1.3.6`
- runtime: `CPython 3.12.14`

Required variable inventory, zero-based parser ordinals:

- `COUNTRY = 0`
- `RESPNO = 4`
- `DATEINTR = 36`
- `Q69B = 226`

## Write-ahead boundary

At this checkpoint:

- no source row values were read;
- no source row values were committed;
- no Q69B mapping was executed;
- no DATEINTR row value was inspected;
- no transport was created;
- no C11 release was created;
- no comparator was created;
- no accepted GT1/GT2 object was modified.

Checkpoint 1 is durable. N2 may now proceed to the authorized five-column source read.
