# J05 — C09 exact WVS7 carrier recovery / materialization R1 — governed return

Status: **PASS**

Terminal:

`J05_PASS__EXACT_WVS7_LIBRARY_PACKAGE_CURRENTLY_MATERIALIZABLE__FROZEN_SAV_185163494_BYTES_SHA256_2BD2A20F_RECOVERED__97220_X_613_DOUBLE_DECODE_PROVED__SEPARATE_C09_RERUN_READY`

Exact grain:

`C09_EXACT_WVS7_CARRIER_RECOVERY_MATERIALIZATION_AND_IDENTITY_RECEIPT_R1_ONLY`

Branch:

`agent/rabochii-prev3-w8-j05-wvs7-carrier-recovery-r1`

Commission tip verified before mutation:

`49daa83a3f46e59a56e0adf341fce9207ddad1b9`

No replacement branch was created and no rebase was performed.

## Holding

The exact WVS7 raw carrier required by C09 is currently recoverable and materializable from the authorized Library package. J05 recovered Library file `WVS Wave 7.sav.zip`, file id `file_00000000386c820d8760e748b25ad7e1`, version `1`, size `26,200,230` bytes, package SHA-256 `ce92993a022edbe39823f4a95d3f33522179ce4f388e2de2c1778c4ae6f1059a`.

The package archive test passed with no errors. Its exact selected member is `WVS Wave 7.sav`; the only other member is the 312-byte macOS resource fork `__MACOSX/._WVS Wave 7.sav`, which is explicitly excluded from source selection.

The extracted carrier matches the frozen C09 identity exactly:

- filename: `WVS Wave 7.sav`;
- bytes: `185163494`;
- SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`;
- ZIP CRC32: `d0308f1a`;
- decoded dimensions: `97220 x 613`.

Two fresh extractions independently produced the exact byte count and SHA-256 and were bytewise identical. A separate Python `hashlib.sha256` pass reproduced the same SHA-256.

Two independent fresh-process SPSS SAV header/dictionary decoders also reproduced the dimensions exactly. Each saw 97,220 cases, 645 nominal case elements, 645 variable records, 32 string-continuation records, and therefore 613 primary variables; both reached the first non-variable dictionary record (`type 3`) at byte offset 62,360. `pyreadstat` was unavailable in this execution environment and external installation was unavailable, so J05 did not claim a pyreadstat full-data decode; the exact SAV dimension metadata was independently decoded twice from the recovered carrier itself.

## Governed artifacts

| Artifact | Git blob | File SHA-256 | Semantic/content-addressed identity |
|---|---|---|---|
| `01_WVS7_PACKAGE_RECOVERY_RECEIPT.json` | `26f5f3ec36b2daba1148afe143399727b1a6cade` | `75b775e22d6d0227e1b8a17b0c2d15c6096f41242c434e599efbe14b5ac1840c` | `1310c03ca7bdbcceec38682cb5f2cb1cd5951a15b61d4242443eb5d2786e5342` |
| `02_WVS7_EXTRACTED_CARRIER_IDENTITY_RECEIPT.json` | `652f1664954f66f88418b1ec6a320cea88840878` | `1547747264944d695714b5819badbe9b07f53f724ec0271444196bbc5c2f4711` | `93674d39f2b4179d800a33320d5bbead54f6f07d9528a46c11bc2921c9dd44be` |
| `03_WVS7_DOUBLE_IDENTITY_AND_DIMENSION_REPLAY_RECEIPT.json` | `2ad7ffbfc56644fd4b14fe2193d15c46941c44b1` | `ff9c3c1a4dfabda9e87c650624d8ca95d36832c68522dfa11f0302a9de9b487e` | `2e9ee5662f3f19cd5fc911c500f5a96de2ab886d53663e756b7fe6eca7f42c77` |
| `04_C09_WVS7_SOURCE_MATERIALIZATION_CONTRACT.json` | `69701b9b444e6877072a5083faf46e4a0c7f7808` | `24e4a50a54973b20dc9eda57f98e87d53d38e61d5d9007d3c462301fba0dfeb0` | `c550c7fa64881c26f5a011f61c14256640410adbb63cafe6cdb47769eee0365b` |

## Reusable downstream materialization law

A separate C09 rerun may consume only this exact source path:

1. materialize Library `file_00000000386c820d8760e748b25ad7e1`, version `1`, as raw bytes;
2. verify package name, 26,200,230-byte size, and package SHA-256 `ce92993a...`;
3. extract only member `WVS Wave 7.sav`;
4. before any candidate launch verify 185,163,494 bytes and SHA-256 `2bd2a20f...`;
5. verify `97220 x 613` dimensions;
6. fail closed on any mismatch. No substitute WVS7 release or derived CSV/parquet/shard/codebook is admissible.

## Scope audit

J05 performed **zero C09 candidate executions**, **zero Candidate A/B/C launches**, **zero performance measurements**, **zero architecture ranking/selection**, and **zero source substitution**. It did not mutate HB05/HB06/HB07/C09 truth, MAIN, or PRE-MAIN.

No production code or test file was required or modified at this carrier-recovery grain. Qualification evidence is the current Library materialization, archive integrity test, independent extraction/hash replay, and independent dimension-decode replay captured in the governed receipts above.

## Successor

`J05_PASS_WAKES_SEPARATE_C09_RERUN = READY`

J05 does **not** run that successor.
