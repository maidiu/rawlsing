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
- exact reader configuration, including any explicit source-specific encoding override.

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

### 3.1 Source-specific reader encoding compatibility

A frozen source may require an explicit reader encoding to decode source-native metadata. This is lawful only when all of the following hold:

1. the source bytes are already fixed by exact SHA-256;
2. default decoding fails or is otherwise proven non-replayable;
3. HQ freezes one exact compatibility encoding for that exact source snapshot;
4. the decoder uses that encoding deterministically for both metadata and data reads;
5. the manifest records the override, reason, source SHA, decoder/dependency version, and resulting file-reported encoding metadata;
6. no automatic encoding guessing or silent fallback sequence is used.

A reader encoding override changes only byte-to-text decoding. It does not authorize semantic normalization, source-value changes, canonical mapping, routing inference, or survey interpretation.

Current frozen compatibility ruling:

- `EVS 1999.sav`
- SHA-256 `6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8`
- reader encoding override: `latin1`
- reason: default pyreadstat metadata decode fails on an invalid byte sequence; the exact frozen source reads successfully under Latin-1. The override must be recorded in every physical manifest/replay receipt.

If any other source fails default decoding, execution stops and returns that source to HQ. Executors may not add ad hoc encoding guesses.

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
- automatically guesses or cycles through text encodings without an HQ-frozen source-specific override.

## 6. Required hostile fixtures

Before implementation acceptance, tests must include at least:

### SAV / WVS7
- user-missing values remain physically present;
- source missing declarations remain recoverable;
- Q152-Q157 positive and user-missing rows remain associated with their exact source rows;
- I_PSU source missing/design states remain present;
- D_INTERVIEW duplicates do not alter source-row identity;
- ordered question slots remain distinct.

### SAV / EVS 1999
- exact frozen SHA is required;
- default reader failure is not silently swallowed;
- the HQ-frozen `latin1` reader override reproduces the full physical manifest;
- the override is explicit in the manifest and replay receipt;
- no source codes or missing-state declarations are altered by the encoding override.

### DTA / LiTS I
- system missing remains distinct from ordinary labeled semantic codes;
- ordinary labeled numeric DK/refusal/not-applicable codes remain observed raw values at decoder layer;
- native `id` is retained but source-row replay identity remains independent;
- all three weight candidates remain raw source variables until authority classifies their use.

## 7. Version/replay contract

Every extraction receipt records:

- exact source SHA-256;
- decoder implementation hash/version;
- dependency versions;
- exact decoder configuration, including source-specific encoding override where used;
- case/variable counts;
- counts by physical missing-state class;
- deterministic manifest/repository digest.

A dependency upgrade or reader-configuration change that changes decoded source incidence requires a new extraction identity and equivalence review; it may not silently replace prior certified material.
