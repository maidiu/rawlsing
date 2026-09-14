# M03 — LiTS-I q301 R2/R7/R27 exact record-ID materialization — governed return

Status: `BLOCKED__EXACT_CARRIER_AND_IDENTITY_LAW_PINNED__DTA_DERIVATION_EXECUTION_SURFACE_UNAVAILABLE__NO_RECORD_SET_FABRICATION`

Branch: `agent/rabochii-prev3-w11-m03-lits-record-id-materialization-r1`

Commission tip: `5fd4d4610da0cc539a0503427bb2a0f706ce5e9c`

Exact grain:

`LITS_I_Q301_R2_R7_R27_EXACT_RECORD_ID_EXTENSION_MATERIALIZATION_R1_ONLY`

## Holding

M03 does not claim PASS and does not fabricate R2/R7/R27 member-ID extensions from the already-known cardinalities.

The exact authorized LiTS-I carrier was successfully materialized from Library:

- Library file id: `file_0000000036dc81f8b8b546e356590a03`
- version: `1`
- source artifact: `LITS-2006-data.dta`
- accepted byte length: `139531180`
- accepted SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- accepted row count: `29002`

Accepted LiTS replay identity law is also pinned. Existing HQ authority explicitly preserves source-SHA + row-ordinal replay identity and keeps native `id` separate. The frozen PRE553 physical decoder assigns physical source row ordinals one-based: `enumerate(..., 1)` and emits `row_offset + local_row`. Therefore M03's lawful record identity coordinate is the exact tuple:

`(source_sha256, one_based_source_row_ordinal)`

M03 does not mint a durable cross-release/native-person identity from this coordinate.

## Required extensional sets

Frozen K03/L03 authority remains:

- `R2`: q301_2 native substantive target states `1..5`; expected cardinality `24897`;
- `R7`: q301_7 native substantive target states `1..5`; expected cardinality `28325`;
- `R27`: exact set intersection `R2 ∩ R7`; cardinality and exact member extension must be derived mechanically from the carrier;
- every one of the 29,002 source rows must be accounted exactly once per target variable as denominator member or exact pre-query exclusion;
- no learned outcome may be inspected.

## Exact blocker

After exact carrier materialization, the available local execution surfaces failed before user code execution when invoked for the required DTA decode/derivation. No lawful DTA scan completed in this M03 run.

Because the exact extension cannot be reconstructed from aggregate counts alone, M03 refuses to create:

- an R2 member list/root;
- an R7 member list/root;
- an R27 member list/root or cardinality;
- a fake replay receipt derived from counts rather than exact row identities.

This is an execution-surface blocker, not a new source-semantic, denominator-authority, or identity-authority defect.

Terminal blocker:

`M03_BLOCK__EXACT_LITS_CARRIER_AVAILABLE__SOURCE_SHA_PLUS_ONE_BASED_ROW_ORDINAL_IDENTITY_PINNED__DTA_DERIVATION_DID_NOT_EXECUTE__R2_R7_R27_EXTENSIONS_NOT_FABRICATED`

## Successor gate

Re-run this same bounded derivation on an execution surface that can decode the exact authorized DTA bytes. The successor must mechanically emit exact R2/R7/R27 member-coordinate extensions, canonical roots, cardinalities, complete 29,002-row accounting, and fresh same-input replay. No semantic redesign or new identity scheme is authorized.

No MAIN/PRE-MAIN mutation. No learned outcomes. No OBL063 revival. PRE-V3 remains objective-world only.
