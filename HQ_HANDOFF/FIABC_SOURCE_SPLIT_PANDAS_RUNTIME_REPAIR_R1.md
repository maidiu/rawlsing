# FIABC Source-Split Pandas Runtime Repair — R1

Status:

`SOURCE_FREE_REQUALIFICATION_REQUIRED__NO_MEASURED_USE_YET`

Base qualified control:

`1e701f10258831b6f453db8ad9d7ddbcba0bf247`

Protected execution remains unchanged:

`3d8f2ad62600b6777dcb23a28404a067502e77a0`

Governing adjudication:

`HQD-2026-09-25-096`

## Proven defect

The first WVS7 source-local measured block reached all three A/B/C candidate cells, but each terminated on the same shared runtime exception:

`PyreadstatError: You requested pandas as output_format but cannot import pandas`

The governed physical decoder was not changed. It uses pyreadstat's pandas-returning surface.

The split runtime gate had omitted pandas even though pandas is a real decoder execution dependency.

## Recovered exact working runtime authority

LiTS host persistent runtime:

- CPython 3.11.3
- pyreadstat 1.3.6
- pyarrow 25.0.1
- pandas 2.3.1
- numpy 2.3.2
- Darwin x86_64

Combined imports of pyreadstat + pandas + numpy succeed in that runtime.

## Repair scope

Only source-split control/runtime surfaces are changed:

1. `RUN_FIABC_SOURCE_LOCAL_SPLIT.sh`
   - requires pandas 2.3.1;
   - requires numpy 2.3.2.

2. `FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py`
   - records pandas/numpy in the source-local host/runtime fingerprint.

3. source-free qualification harness/tests
   - pins the expanded runtime;
   - adds hostile merge rejection for pandas-version drift.

No protected execution/candidate/decoder code is modified.

No source is opened or decoded by this repair.

## Required requalification

Run the source-free qualifier from this exact repair branch using:

- exact protected execution checkout at `3d8f2ad62600b6777dcb23a28404a067502e77a0`;
- current clean PRE-MAIN checkout at `cbfbdd76e5a51dee1c267b2856d6946a3e6bb479`;
- the persistent LiTS runtime containing the exact expanded package tuple.

The qualification must prove zero:

- raw-source opens;
- survey-source hash passes;
- decoder calls;
- candidate-process launch attempts;
- candidate outputs;
- measured execution.

Do not promote or launch measured work until HQ reviews the resulting packet.
