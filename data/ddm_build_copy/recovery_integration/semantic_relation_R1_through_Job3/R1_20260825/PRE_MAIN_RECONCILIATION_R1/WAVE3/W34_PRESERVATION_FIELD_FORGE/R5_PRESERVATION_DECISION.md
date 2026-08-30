# R5 PRESERVATION DECISION

Decision: `B__EXACT_IMMUTABLE_REF_PRESERVATION_PLUS_CANONICAL_METADATA`

Status ceiling: `INACTIVE_NON_SERVING`

## Why no physical copy

W26 permits an inert physical copy only if needed to make the preserved capital self-contained. It is not needed here.

The frozen Audit69 head `d6206cd0e351100b64cdf3ace997733153c18eb7` is a direct child of selected V4 `55d4bae445b5eb837aec6f3c67083e131d8e3b0c` and resolves every named minimum source dependency, both dedicated selected-path tests, and the proof receipts. Exact-ref preservation therefore retains the complete selected behavior without creating a new importable module on the canonicalization worker.

Physical copying would create a strictly larger risk surface: a later import scan, selector refactor, package auto-discovery, or accidental module reuse could mistake preserved implementation bytes for installed current runtime. Exact-ref preservation has no such new path.

## Exact source floor at `d6206cd...`

| path | Git blob SHA | preservation |
|---|---|---|
| `rawlsing_next/pre553_r5_codec.py` | `72f8f3c03ed065e86fea4e76bb17f8e06c2bf540` | exact ref |
| `rawlsing_next/pre553_r5_compact_carrier.py` | `92e364b31eaf27be1bca2081eff65f6ffb779c3d` | exact ref |
| `rawlsing_next/pre553_r5_model.py` | `62ce608829c3d9c2fb7c999aefe40188637edf80` | exact ref |
| `rawlsing_next/pre553_r5_serial_turbo66.py` | `ed92f086bba23ad11350f72eb69351123bcfeb31` | exact ref |
| `rawlsing_next/pre553_r5_single_pass_audit69.py` | `ffb063b93c86e215604eecb29a9545c7efdff399` | exact ref |
| `rawlsing_next/test_pre553_r5_serial_turbo66.py` | `e902a712ec8ba478d48f0d498c386bde6124bff3` | exact ref |
| `rawlsing_next/test_pre553_r5_single_pass_audit69.py` | `063d8c3f385b161f0d7b038e92dd9ffd11e38f4e` | exact ref |

The codec itself declares physical-representation ownership only and explicitly refuses to infer C11 semantics, missingness, routing, date/time meaning, labels, or source authority.

## Preserved proof

V4 exact ref `55d4bae...` carries `R5_LONG_COMPACT_V2_SERIAL_TURBO66/COMPLIANCE_CLOSURE.json` with 77 passed / 0 failed / 0 skipped and exact-equivalence closure.

Audit69 exact ref `d6206cd...` carries:

- `R5_SINGLE_PASS_AUDIT69/RESULT.md`;
- `R5_SINGLE_PASS_AUDIT69/RESULT.json`;
- `R5_SINGLE_PASS_AUDIT69/HOSTILE_EQUIVALENCE_RECEIPT.json`;
- `R5_SINGLE_PASS_AUDIT69/RESOURCE_RUNTIME_RECEIPT.json`.

Its terminal receipt records 96 passed / 0 failed / 0 skipped for the complete relevant R5 suite and 19 passed for the hostile equivalence court.

No W34 test rerun is asserted because W34 installs no R5 bytes. The preservation proof is exact identity + historical execution receipt + proof that the W34 diff has no selector/runtime file.

## Authority70 ceiling

Authority70 `daeaaf1d6ba0364aab7fda4643aae1da52ec54d2` revalidated the 96-test/19-hostile prefix but stopped before full-source execution with:

`BLOCKED_POTENTIAL_FROZEN_CONTRACT_CONTRADICTION`

Freeze:

`AUTHORITY70_BLOCKER != FULL_WVS7_CERTIFICATION`

`R5_SELECTED_PHYSICAL_CAPITAL != SERVING_AUTHORITY`

`R5_SELECTED_PHYSICAL_CAPITAL != SEMANTIC_AUTHORITY`

## Hard exclusions

Not copied, not indexed as selected alternatives, not promoted:

- LONG_SHARDED V1 `36bf351dda12f0aa93c9ff426ae54d80143d0bf9`;
- Parallel-12 `7049660a574456b4a4333c97a277f6b3d8a2c1b3`;
- Authority67 alternate `84776b595c6c8cf0bfaf9f1b2a10f5618e8d0857`;
- Authority68 alternate `bdbbdca3b63db236ee8347b9a60fc0d96c2cfea1`;
- Authority70 as a serving/certified release.

Any future promotion requires a separate competent authority court; W34 supplies none.
