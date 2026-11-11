# PRE553 SUBSTRATE RECONSTRUCTION — SR03 R3 ADJUDICATION

Status: `ACCEPTED__35_SOURCE_PHYSICAL_CENSUS_COMPLETE`

Frozen parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`
SR03 execution HEAD: `d3d6169dc93754533987673cdb44f2dbc72b9c4f`
Returned checkout package SHA-256: `e58fd7cdd6e8587573e8cb94ca1df4cd8949cee5fdbc39042b739df6add1c232`
Returned deterministic SR03 archive size: `40016081` bytes
Returned deterministic SR03 archive SHA-256: `8d06a436b7148d86273e5ae35a887252198ce8ae984902a4a38f05ad11a0e9cc`
Completion token: `PRE553_SR03_35_SOURCE_NATIVE_METADATA_RECEIPT_COMPLETE`

## 1. Court holding

The exact governed CLOSED_35 raw-source universe is now physically censused at source-byte grain under the format-neutral decoder contract.

All 35 inventory members produced manifests from their exact frozen SHA-256 source bytes. No source was substituted. No manifest failed row/cell count conservation.

G-SR03 is accepted as a **physical source census**, not as source-semantic certification. Source-specific authority packs remain responsible for semantic interpretation of labels, routing, estimands, topology and other governed meaning.

## 2. Corpus-wide physical accounting

Across the 35 source files SR03 observed:

- `486174936` total physical source cells;
- `326652033` ordinary-present cells;
- `112031914` system-missing cells;
- `47490989` SPSS user-missing cells;
- exact component conservation: ordinary + system-missing + user-missing = total cells;
- `0` per-variable row-count conservation failures;
- `22` source files with at least one observed SPSS user-missing cell;
- `18` source multiple-response sets physically declared across three files (`Asian Barometer Wave 5`, `EVS 2008`, `EVS 2017`).

These counts are source-physical facts. They are not claims that every SPSS user-missing code has the same semantic meaning.

## 3. Cross-source loss implication

The census materially strengthens the historical-loader risk finding.

Twenty-two CLOSED_35 source files physically contain SPSS user-missing-valued cells. Historical SAV-reading code found in the ETL/backfill archaeology does not explicitly request preservation of SPSS user-missing values. Therefore source-native typed/special states are a **cross-source loss surface**, not a WVS-only concern.

Only WVS7 is already proven source-vs-legacy at exact variable/count grain. Other sources require their scheduled source-equivalence comparison before claiming exact realized legacy loss counts.

Disposition:

`SAV_USER_MISSING_CROSS_SOURCE_RISK = PROVEN_PHYSICAL_EXPOSURE__PER_SOURCE_LEGACY_LOSS_QUANTIFICATION_DEFERRED_TO_G_SR09`

This is a scheduled gate dependency, not a loose investigation.

## 4. WVS7 hostile-fixture acceptance

The SR03 WVS7 manifest reproduces the prior independent source forensics exactly for the critical hostile variables:

- Q152 user-missing = `2557` (`-1=1620`, `-2=501`, `-5=436`);
- Q153 user-missing = `4877` (`-1=957`, `-2=1480`, `-3=2388`, `-5=52`);
- Q154 user-missing = `1802`;
- Q155 user-missing = `3777`;
- Q156 user-missing = `1745`;
- Q157 user-missing = `3626`;
- `I_PSU=-4` user-missing = `31137`;
- D_INTERVIEW remains physically present for all `97220` source rows;
- W_WEIGHT and S018 remain physically distinct variables.

This independently confirms the WVS legacy typed-absence deletion diagnosis and validates the SAV physical decoder boundary.

## 5. LiTS I hostile-fixture acceptance and correction

The exact LiTS I DTA manifest reports:

- `29002` source rows;
- `1198` variables;
- no Stata extended missing values observed;
- ordinary labeled semantic codes remain ordinary physical values;
- `weight_0`, `weight_1`, and `weight_2` each contain `29000` ordinary values plus `2` Stata system-missing values.

This corrects any prior shorthand that all three weights were populated on all 29002 source rows. The authoritative physical fact is 29000 present + 2 system missing for each weight candidate.

The legacy DB contains only 28002 LiTS 2006 respondents; SR02 adjudication separately proves the historical country-map defect responsible for the 1000-row loss and broader country misclassification.

## 6. SAV/DTA format-neutral boundary confirmed

The proving pair and full census validate the architectural separation:

`SOURCE BYTES -> FORMAT PHYSICAL DECODER -> FORMAT-NEUTRAL RAW INCIDENCE -> SOURCE AUTHORITY PACK -> GOVERNED C11 STATE`

In particular:

- SAV user-missing declarations must remain physical facts even before semantic classification;
- DTA ordinary values such as numeric DK/refusal/not-applicable codes must not be converted into physical missingness;
- source-row ordinal remains replay identity independent of native respondent IDs;
- source multiple-response metadata must survive when physically declared;
- source-reported file encoding and reader configuration must be recorded separately from semantic authority.

No change to the frozen C11 semantic architecture is required.

## 7. Reader compatibility overrides

Six exact source snapshots use the frozen pyreadstat compatibility execution path:

- EVS 1999 SAV;
- EVS 2008 SAV;
- LiTS I DTA;
- LiTS II DTA;
- LiTS III DTA;
- LiTS IV DTA.

Each carries:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

These overrides permit deterministic physical extraction. They do **not** establish that Latin-1 is the source's intended textual encoding and may not independently certify source-label semantics.

The six-source encoding/label authority question terminates at the appropriate source authority packs. It does not block physical C11 carrier selection.

## 8. Identity/topology observations

The census confirms source heterogeneity anticipated by C11:

- native respondent identifiers cannot be assumed universally injective or even universally present;
- WVS D_INTERVIEW is retained as source data but not hard replay identity;
- LiTS I native `id` is retained but source-snapshot + row ordinal remains the irreducible replay key;
- multiple-response-set metadata exists in the corpus and must not be erased by a flat question-only representation.

## 9. Closure

SR03 has completed its mission. No additional physical-census rerun is authorized unless source bytes, decoder implementation, dependency version, or frozen reader configuration changes.

Per-source semantic/source-equivalence certification remains scheduled under G-SR07/G-SR08/G-SR09.

G-SR03 is closed.

Token:

`PRE553_SR03_R3_ACCEPTED__35_SOURCE_PHYSICAL_CENSUS_COMPLETE`
