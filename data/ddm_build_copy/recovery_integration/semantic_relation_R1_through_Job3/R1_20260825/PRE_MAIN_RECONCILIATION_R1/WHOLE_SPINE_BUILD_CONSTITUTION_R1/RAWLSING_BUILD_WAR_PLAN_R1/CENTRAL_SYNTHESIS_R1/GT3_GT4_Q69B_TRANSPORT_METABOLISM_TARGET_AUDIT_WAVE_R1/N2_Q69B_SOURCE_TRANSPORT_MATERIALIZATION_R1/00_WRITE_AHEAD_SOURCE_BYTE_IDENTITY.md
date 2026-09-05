# N2 WRITE-AHEAD — EXACT R5 SOURCE BYTE IDENTITY

Status:

`SOURCE_BYTES_EXACTLY_VERIFIED__PARSER_INVENTORY_CHECK_PENDING`

Exact working start:

`bca519e3d39b7c3886210958800a4b47ecb50440`

Evidence execution commit:

`24001834b540d4d311ac5c1a1b842309ed47af38`

Governed court run:

`33997291575`

Governed court job:

`101389926791`

Source route:

`OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION`

Official URL:

`https://www.afrobarometer.org/wp-content/uploads/2022/02/merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav`

Required byte count:

`49,689,458`

Required SHA-256:

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

## Court evidence

The N2 checkpoint test streamed the official SAV into runner-local scratch while computing SHA-256.

The test then executed, in order:

1. assertion `byte_count == 49_689_458`;
2. assertion `source_sha256 == c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
3. installation/import of `pyreadstat==1.3.6`;
4. metadata-only `read_sav` invocation.

The court log failed inside step 4 only because pyreadstat's default output format attempted to import pandas, which was not installed.

Therefore both source byte assertions necessarily passed before the parser-output dependency failure.

Observed runner:

- Ubuntu 24.04.4;
- CPython 3.12.14;
- pyreadstat 1.3.6 installed successfully.

No source row value was read or committed.

No Q69B or DATEINTR semantic claim is made by this write-ahead checkpoint.

The next legal action is a metadata-only rerun using pyreadstat's non-pandas dict output to complete the required variable-inventory portion of checkpoint 1.
