# SOURCE CERT PREP71 — R01 AFROBAROMETER FUTURE EXECUTION ORDER

Status: `PROPOSED_FUTURE_COURT_ORDER__NON_DISPOSITIVE`

This file does not certify any source and does not authorize G-SR09. A later authority must explicitly launch the future court.

## Global order and fail-closed law

For each source, execute exactly this order:

`source SHA -> decoder/config -> hostile physical fixtures -> metadata/topology fixtures -> documentary semantic assertions -> exact carrier/C11 equivalence assertions -> negative/fail-closed fixtures -> future disposition gate`

Global constraints:

1. Open only the exact SHA-256 snapshot listed below. Fail closed on any byte mismatch.
2. Use the frozen SAV decoder contract: strict source-declared UTF-8 (`SPSS extension subtype 20`), preserve system missing, preserve user-missing declarations and raw stored values, and never coerce a value because a label looks like missing/DK/refused/N/A.
3. Universal replay identity is `(source_sha256, zero_based_row_ordinal)`. Native IDs are source attributes unless the exact documentary assertion below says more.
4. Physical facts outrank documentary text. Documentary text may close semantic meaning; it may never erase a raw declaration/value/topology that exists in the exact snapshot.
5. Assert carrier/C11 equivalence field-by-field. No family-level name matching or inferred normalization.
6. Any unresolved authority gap listed in `AUTHORITY_GAPS.csv` must either remain explicitly unknown or be closed by the named later authority. No implicit TODOs.

## Afro Barometer Round 1

### 1. Source SHA

`6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2`

### 2. Decoder/config

`STRICT_UTF8_FROM_SOURCE_SUBTYPE20__PRESERVE_SYSTEM_MISSING__PRESERVE_SPSS_USER_MISSING_DECLARATIONS_AND_RAW_VALUES__NO_LABEL_DRIVEN_COERCION`

### 3. Hostile physical fixtures

Replay `R1_F01` through `R1_F07`. Required physical anchors include:

- `REFNUMB` row 0 = `1`, with accepted 21,531/21,531 global injectivity;
- noninjective `CASENUMB` metadata;
- ordinary stored `SUPDEM=4` and `SUPDEM=97` cells;
- `COUNTRY` row 0 = `3` / raw label `Lesotho`;
- `WITHINWT` row 0 = `1.0`;
- subtype-20 UTF-8 source metadata.

### 4. Metadata/topology assertions

Preserve zero declared user-missing variables, zero user-missing cells, and zero system-missing cells as source facts. Do not manufacture a missing-state topology merely because `SUPDEM` labels include “Missing Data”, “Not applicable”, “Refused”, or “Don't know”.

### 5. Documentary semantic assertions

Using Library `merged_r1_codebook2.pdf` (`file_00000000328471f691257df059dc51ba`):

- bind `REFNUMB` to the documented unique MSU case-reference role;
- bind exact R1 `COUNTRY` codes to the documented 12-country map;
- bind `SUPDEM` special-code meanings and documented country-specific response/routing caveats while keeping the values physically ordinary;
- bind R1 weight carriers to their documented R1 roles (`WITHINWT`, `ACROSSWT`, `COMBINWT`, `AFRICAWT`, `AFCOMBWT`);
- preserve the codebook's explicit warning that national R1 instruments were not standardized and that merged variables may combine similar/conceptually equivalent national questions.

### 6. Exact carrier/C11 equivalence assertions

Compare raw value/state, missing declaration metadata, labels/dictionaries, country coordinate, exact slot/field identity, and each weight carrier independently. C11 must reproduce exact source-side physical states before any governed semantic presentation.

### 7. Negative/fail-closed fixtures

Fail closed on:

- treating `CASENUMB` as global identity;
- asserting `CASENUMB = codebook RESPNUMB` without new authority;
- treating semantic special codes as physical missing;
- assuming all 12 national instruments had identical wording/response options;
- importing R5/R9 country or weight mappings by exact-name coincidence.

### 8. Future disposition gate

Packet-preparation disposition: `PACKET_READY__SOURCE_SPECIFIC_HOSTILE_COURT_REQUIRED`. A later source court may proceed with source-specific hostile fixtures; this Authority-71 return makes no certification decision.

## Afro Barometer Round 5

### 1. Source SHA

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

### 2. Decoder/config

Same strict SAV config. In particular, do not convert declared user-missing `997` values into nulls before replay.

### 3. Hostile physical fixtures

Replay `R5_F01` through `R5_F09`, including:

- `RESPNO` row0 raw bytes/string `ALG0001` and accepted injectivity;
- `Q10B` declared/exercised user-missing `997`;
- `Q47C` system-missing sentinel while its user-missing declaration remains separately present;
- ordinary `Q71A=-1` labeled “Missing”;
- `WEST.AFR` administrative filter carrier;
- raw `COUNTRY=31`/`Algeria`;
- exact `WITHINWT` numeric value;
- UTF-8 metadata;
- Q41D_ARB positive control linking `997=Not asked` to explicit source-native country routing.

### 4. Metadata/topology assertions

Require exact source-wide accepted counts: 84 variables declare discrete user-missing `997`; all 84 exercise it; 1,342,300 user-missing cells; 4,336 system-missing cells across four variables. Keep user-missing and system missing separate.

### 5. Documentary semantic assertions

Using Library `merged_r5_codebook_2.pdf` (`file_00000000520471f6a2c7b8e706e93ab5`):

- bind RESPNO only to the source-native respondent-number role;
- bind Q41D_ARB `997=Not asked` and its exact five-country routing;
- bind WITHINWT/COMBINWT and country technical-form sampling claims where explicitly documented;
- DO NOT bind exact raw `COUNTRY` to `COUNTRY_ALPHA` by convenience;
- DO NOT bind Q10B/Q47C `997` to “Not asked” unless named official authority closes their own entries;
- keep WEST.AFR/R1.ONLY..R4.ONLY semantics opaque unless exact carrier documentation is supplied.

### 6. Exact carrier/C11 equivalence assertions

Assert exact raw declaration, raw value, system/user-missing class, dictionary, and routing-carrier preservation. Semantic presentation of Q10B/Q47C `997` must remain `UNRESOLVED_SOURCE_SEMANTICS` unless R5-G02/R5-G03 are closed by future authority.

### 7. Negative/fail-closed fixtures

Fail closed on:

- dropping or coercing `997` because a codebook entry omits it;
- borrowing `997=Not asked` from Q41D_ARB/Q47D into Q10B/Q47C;
- substituting `COUNTRY_ALPHA` codes for exact raw `COUNTRY`;
- deriving WEST.AFR/R*.ONLY routing semantics solely from names or missingness;
- treating `Q71A=-1` as physical missing because its label says “Missing”.

### 8. Future disposition gate

Packet-preparation disposition: `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION`. Required documentary blockers are enumerated as R5-G01..R5-G03; R5-G04 may remain opaque if future law permits physical-only preservation.

## Afro Barometer Round 9

### 1. Source SHA

`3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8`

### 2. Decoder/config

Same strict SAV config. Declaration metadata and incidence are independent assertions.

### 3. Hostile physical fixtures

Replay `R9_F01` through `R9_F10`, including:

- `RESPNO` row0 `ANG0001`;
- Q78F `-1` user-missing declaration with **zero** exercised user-missing cells;
- ordinary `Q47C=94` raw code;
- Q118 system-missing cell and ordinary `9996` terminator cell;
- `COUNTRY=2`/`Angola`;
- physically distinct old/new weight values;
- exact eleven-slot Q118 topology;
- UTF-8 metadata.

### 4. Metadata/topology assertions

Preserve:

- one and only one declared user-missing variable (`Q78F=-1`) even at zero incidence;
- 583,491 system-missing cells across 32 variables as accepted census/recon evidence;
- eleven separate Q118 slots `Q118_1..Q118_11` with source-native physical ordinals;
- ordinary `9996` in slots 2..11 independently of physical missingness;
- system missing in later Q118 slots independently of 9996.

### 5. Documentary semantic assertions

Using Library `AB_R9.MergeCodebook_25Jun24.final_.pdf` (`file_00000000e7e871f69de0c996a917d962`):

- bind RESPNO and exact COUNTRY to documented data-manager-assigned roles/maps;
- bind Q118 documented slots to the spoken-language, tick-all-that-apply surface and `9996=No further reply` only where the document actually covers them;
- preserve the bounded Q78 family documentary fact: Q78A-E are present and the codebook then proceeds to Q84A; do **not** invent Q78F semantics;
- preserve the bounded Q118 documentary fact: Q118_10 is followed by Q118OTHER; do **not** invent Q118_11 semantics;
- use the documented old/new `withinwt_ea`/`withinwt_hh` concepts only as partial authority; do not assert V397_A/V399_A carrier binding without named later authority;
- do not assign semantic authority to Q47C code94 merely from its raw label because the codebook Q47C entry omits94.

### 6. Exact carrier/C11 equivalence assertions

C11/carrier must preserve the Q78F declaration object even when no row exercises it, the exact eleven Q118 slots/order, ordinary9996 vs system missing, raw country coordinate, and four physically distinct weight carriers. Any semantic binding for the named gaps must be separately sourced.

### 7. Negative/fail-closed fixtures

Fail closed on:

- erasing Q78F declaration because incidence is zero;
- copying Q78E meaning/routing into Q78F;
- flattening Q118 slots or treating slot order as preference/rank;
- treating9996 as physical missing;
- inventing Q118_11 meaning from Q118_10/Q118OTHER adjacency;
- interpreting Q47C=94 as a governed semantic applicability state without source authority;
- equating V397_A/V399_A to documented weight concepts solely from labels/names;
- importing R5/R1 country or weight mappings.

### 8. Future disposition gate

Packet-preparation disposition: `PACKET_READY__DOCUMENTARY_AUTHORITY_REQUIRED_BEFORE_CERTIFICATION`. R9-G01 through R9-G04 require named documentary resolution before semantic certification; R9-G05 can remain topology-only if future authority explicitly forbids rank inference.

## Frozen-contract contradiction gate

No potential contradiction with the frozen generic SAV decoder/source-native contracts was observed during packet preparation. The observed byte/document discrepancies are source-specific documentary gaps: the governing evidence rank already requires exact source bytes/native metadata to prevail. A future court must fail closed only if new evidence would require changing the frozen decoder/source-native laws themselves.
