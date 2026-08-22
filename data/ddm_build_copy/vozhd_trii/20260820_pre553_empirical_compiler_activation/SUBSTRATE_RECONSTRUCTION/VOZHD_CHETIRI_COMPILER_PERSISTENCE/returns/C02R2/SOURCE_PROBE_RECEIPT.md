# C02-R2 source probe receipt

## Frozen execution

Exact command:

```text
python3 data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SR03_SOURCE_NATIVE_METADATA_PROBE.py --inventory data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/SOURCE_BYTE_INVENTORY.csv --source-root /Users/matthewsmith/Desktop/Rawlsing/data/Data --output-dir /private/tmp/SR03_SOURCE_PHYSICAL_MANIFESTS_C02R2.UeJtmj
```

Exit/completion: `0`; completion token: `PRE553_SR03_35_SOURCE_NATIVE_METADATA_RECEIPT_COMPLETE`. Sources decoded: 35/35. Runtime/R5/database writes: none. Source mutation: none.

Configuration was `user_missing=True`, `apply_value_formats=False`, no value-format substitution, and no encoding override except the six exact allowlisted compatibility executions recorded in `DECODER_INVOCATION_RECEIPT.csv`. Each override retains authority status `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

## Physical scope

- source records: 35 (31 SAV, 4 DTA)
- physical source rows across manifests: 887232
- physical source variables across manifests: 18413
- native multiple-response sets: 18 across three SAV files; member declarations: 232
- all-missing physical variables (ordinary=0, system-missing=0, user-missing=0): 0

## Targeted hostile reads

The following narrow reads used the same frozen reader behavior, with `usecols` limited to the named variables:

- WVS7: `D_INTERVIEW`, `Q152`–`Q157`; 97,220 rows. `D_INTERVIEW` had 96,221 distinct values; one value (`858069901.0`) appeared on 1,000 source rows.
- WVS7 ordered pairs with equal nonmissing raw values: Q152/Q153 = 424 rows; Q154/Q155 = 471; Q156/Q157 = 506.
- LiTS I: `id`, `weight_0`, `weight_1`, `weight_2`; 29,002 rows. `id` had 29,002 distinct nonmissing values and zero duplicate keys. Each weight had 29,000 ordinary values and 2 system-missing cells.

These are observations in the executed scope. They are not semantic FD certificates and do not select persistence material.
