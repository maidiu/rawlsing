# PRE553 SUBSTRATE RECONSTRUCTION — FORMAT DECODER CONTRACT

Status: `FROZEN_BROWSER_AUTHORITY__IMPLEMENTATION_BLOCKED`

## 1. Architectural boundary

The physical decoder is a dumb byte-to-source-incidence adapter. It may expose facts encoded by the file format. It may not interpret survey meaning, map to structural ontology, choose canonical questions, select weights, infer routing, repair data, or consult legacy Postgres as truth.

The generic interface is format-neutral. SAV and DTA are plugins under the same interface.

## 2. Required generic decoder output

A decoder must expose, without destructive coercion:

- exact source snapshot hash;
- physical row ordinal;
- source variable ordinal/name;
- raw value or explicit system-missing state;
- physical missing-state class;
- source user-missing declaration/value/range if applicable;
- source extended-missing value if applicable;
- variable label;
- value-label set and selected raw label where available;
- storage/type/format metadata;
- source multiple-response/topology metadata where physically encoded;
- source file metadata required for deterministic replay;
- exact reader configuration, including any explicit source-specific compatibility encoding override and its authority status.

All outputs must be deterministic for identical bytes + decoder version/config.

## 3. SAV decoder contract

The SAV decoder must preserve at minimum:

- SPSS system missing;
- SPSS user-missing discrete values;
- SPSS user-missing ranges;
- raw numeric/string values before value-format substitution;
- variable labels;
- value labels;
- measure/display metadata available from the reader;
- multiple-response set definitions where available;
- file encoding/format metadata needed for replay.

The reader configuration must preserve user-missing values rather than coercing them to generic NaN. A code path that reads SAV with user-missing preservation disabled is noncompliant for source certification.

The decoder does not translate `-1`, `-2`, `-3`, etc. into semantic states by itself. Their meanings belong to the source authority pack.

### 3.1 Source-specific reader compatibility encoding

A frozen source may require an explicit reader encoding for a particular reader implementation to decode source-native metadata or complete the physical census. This is lawful only when all of the following hold:

1. the source bytes are fixed by exact SHA-256 in `SOURCE_BYTE_INVENTORY.csv`;
2. the compatibility behavior is measured against those exact bytes;
3. HQ freezes one exact compatibility encoding for that exact source snapshot and reader path;
4. the decoder uses that encoding deterministically for metadata and data reads;
5. the manifest records the override, reason, source SHA, decoder/dependency version, and resulting file-reported encoding metadata;
6. no automatic encoding guessing or silent fallback sequence is used.

A compatibility encoding override changes only byte-to-text decoding for that reader execution. It does not authorize semantic normalization, source-value changes, canonical mapping, routing inference, or survey interpretation.

**Critical distinction:** `reader compatibility encoding` is not automatically `authoritative source text encoding`.

For SR03 physical census purposes, an override may be frozen with authority status:

`COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`

Under that status:

- raw numeric/string storage values, physical missing declarations, row/variable counts, and other format-native non-semantic facts may be inventoried;
- text labels/notes decoded through the override are retained exactly as reader output but remain provisional for source-semantic authority;
- later source authority work must confirm intended text encoding/documentary semantics before decoded text becomes certification authority;
- no C11 semantic state may be certified solely from a compatibility-decoded label whose source-text authority remains unresolved.

### 3.2 Frozen SR03 compatibility-execution allowlist

The following exact snapshots may use `latin1` in SR03 because default/chunked pyreadstat execution has proved non-replayable or the compatibility path is required by the frozen disposable physical-census implementation. Every entry has authority status `COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY`.

| source | exact SHA-256 | compatibility encoding | execution basis |
|---|---|---|---|
| `EVS 1999.sav` | `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a` | `latin1` | default pyreadstat metadata decode fails on invalid byte sequence; exact source reads under Latin-1 |
| `EVS 2008.sav` | `5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379` | `latin1` | default pyreadstat metadata decode fails on invalid byte sequence; exact source reads under Latin-1 |
| `LiTS_I.dta` | `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09` | `latin1` | frozen pyreadstat compatibility execution path; not a ruling that Latin-1 is the source's intended text encoding |
| `LiTS_II.dta` | `c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9` | `latin1` | default pyreadstat DTA decode fails on invalid byte sequence; exact source reads under Latin-1 |
| `LiTS_III.dta` | `368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8` | `latin1` | default chunked pyreadstat execution fails; exact source completes under Latin-1 full-read compatibility path |
| `LiTS_IV.dta` | `14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c` | `latin1` | frozen pyreadstat compatibility execution path; not a ruling that Latin-1 is the source's intended text encoding |

The browser/HQ independently confirmed that all four LiTS files are structurally readable as Stata files using pandas' Stata reader. That establishes file-format readability; it does **not** establish the intended character encoding for source text and does not supersede the compatibility-only status above.

If any source outside this exact allowlist fails default decoding, SR03 stops and returns that source to HQ. Executors may not add ad hoc encoding guesses.

## 4. DTA decoder contract

The DTA decoder must preserve at minimum:

- Stata ordinary observed numeric/string values;
- Stata system missing `.`;
- Stata extended missings `.a` through `.z` when present;
- variable labels;
- value-label set assignments and dictionaries;
- storage/display format metadata;
- file format/version metadata required for replay.

Ordinary numeric values carrying labels such as `don't know`, `refused`, or `not applicable` remain ordinary observed storage values at the decoder layer. Semantic classification occurs only under source authority.

## 5. Forbidden decoder behavior

A decoder fails immediately if it:

- drops rows/cells because they are missing/user-missing;
- replaces source row identity after filtering/sorting;
- emits only formatted labels and loses raw codes;
- emits only raw codes and discards source labels/metadata available in the file;
- maps numeric codes to generic semantic states without source authority;
- collapses all missing mechanisms into one null;
- assumes a native respondent ID is unique without measurement;
- writes Postgres/C11 during physical extraction;
- uses legacy database values to overwrite source-file values;
- silently substitutes another source file when a frozen SHA is absent;
- automatically guesses or cycles through text encodings without an HQ-frozen source-specific compatibility override;
- upgrades a compatibility-reader encoding into source-text semantic authority without separate evidence.

## 6. Required hostile fixtures

Before implementation acceptance, tests must include at least:

### SAV / WVS7
- user-missing values remain physically present;
- source missing declarations remain recoverable;
- Q152-Q157 positive and user-missing rows remain associated with their exact source rows;
- I_PSU source missing/design states remain present;
- D_INTERVIEW duplicates do not alter source-row identity;
- ordered question slots remain distinct.

### SAV / legacy EVS compatibility
- exact frozen SHA is required;
- default reader failure is not silently swallowed;
- the frozen compatibility override reproduces the full physical manifest;
- the override and compatibility-only authority status are explicit in the manifest and replay receipt;
- no source codes or missing-state declarations are altered by the encoding override;
- decoded source text remains nonauthoritative until intended source encoding/documentary semantics are separately closed.

### DTA / LiTS
- system missing remains distinct from ordinary labeled semantic codes;
- ordinary labeled numeric DK/refusal/not-applicable codes remain observed raw values at decoder layer;
- native respondent identifiers are retained but source-row replay identity remains independent;
- all source weight candidates remain raw source variables until authority classifies their use;
- a pyreadstat compatibility encoding never becomes semantic text authority by implication.

## 7. Version/replay contract

Every extraction receipt records:

- exact source SHA-256;
- decoder implementation hash/version;
- dependency versions;
- exact decoder configuration, including source-specific compatibility encoding and authority status where used;
- case/variable counts;
- counts by physical missing-state class;
- deterministic manifest/repository digest.

A dependency upgrade or reader-configuration change that changes decoded source incidence requires a new extraction identity and equivalence review; it may not silently replace prior certified material.
