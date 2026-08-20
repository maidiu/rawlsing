# PRE553 SUBSTRATE RECONSTRUCTION — SOURCE-NATIVE CONSTITUTION

Status: `FROZEN_BROWSER_AUTHORITY__AWAITING_35_SOURCE_PHYSICAL_RECEIPT`

Parent machine: `9188dc9fb7a8b92b981f3d3f94754cd6137d17b1`

## 1. Purpose

This constitution defines the information-preservation boundary between immutable survey source bytes and C11. It is format-neutral and source-neutral. SAV/DTA decoders may expose source-format facts; source authority packs may interpret documented source semantics; neither may destroy source-native information required by D13 M01-M18.

The rebuild architecture is not reopened here. This document governs faithful physical instantiation of the already-selected C11 frontier.

## 2. Supreme rules

1. Source bytes are primary physical evidence until positive source-equivalence certification and separate retirement authority.
2. `physical_missing_state` and `semantic_response_state` are independent dimensions.
3. A semantic state may be encoded as a format-declared missing value, an ordinary labeled numeric/string value, a structural/routing condition, or remain unknown.
4. No decoder may infer semantic meaning from numeric code, label wording, row absence, variable name, or neighboring values.
5. No source authority pack may erase the original physical representation it interprets.
6. Row absence is never an adequate substitute for a typed source-native state when the source represents that state.
7. Exact respondent incidence is mandatory. Filtering missing rows before respondent alignment is prohibited.
8. Native respondent identifiers are attributes unless source authority proves their identity semantics and injectivity at the relevant scope.
9. Source snapshot + physical row ordinal is always retained as a replay identity even when a lawful native respondent ID also exists.
10. Topology, multiplicity, order and rank are information, not presentation metadata.
11. Weight values are not weight authority. Weight purpose, estimand, population, design and lawful combination require separate authority.
12. Routing/applicability/risk-set meaning is never inferred from observed missingness alone.
13. Unknown remains typed `UNKNOWN`; missing documentation never licenses reconstruction by convenience.
14. Canonicalization is additive. Raw variable identity, raw value/state and source labels remain recoverable after canonical mapping.
15. Caches, derived aggregates and legacy database tables are nonauthoritative unless separately certified for a named use.

## 3. Immutable source snapshot

Every source release admitted to reconstruction must have a content-addressed snapshot manifest containing at minimum:

- source family/study;
- wave/release/version where evidenced;
- original filename;
- byte size;
- SHA-256 of exact bytes;
- file format and version where available;
- physical case count;
- physical variable/column count;
- source documentation references available to the campaign;
- extraction tool/version/configuration;
- extraction receipt hash.

Path/name or database `source_file` fields are never substitutes for the byte hash.

## 4. Format-neutral raw source incidence

The physical decoder must be capable of yielding an information-equivalent representation containing at least:

### Source row identity
- source_snapshot_id;
- source_row_ordinal;
- any native respondent-ID candidate(s), unmodified;
- source-scope coordinates required to interpret native IDs.

### Source variable identity
- source_variable_name;
- source_variable_ordinal;
- source storage/type information;
- source variable label;
- source value-label dictionary/reference;
- source display/measure metadata where encoded;
- source multiple-response/topology metadata where encoded.

### Source cell/event identity
- source_row_ordinal;
- source_variable_ordinal/name;
- raw storage value or explicit system-missing marker;
- physical missing class;
- source-declared missing code/range/extended value where applicable;
- raw value label if available;
- occurrence/event/slot identity where the source format permits repeated or ordered events.

A source cell must not vanish merely because an analysis library would normally coerce it to NA/NaN.

## 5. Physical missing-state vocabulary

The cross-format physical vocabulary must distinguish at least:

- `OBSERVED_STORAGE_VALUE`;
- `SYSTEM_MISSING`;
- `FORMAT_USER_MISSING_VALUE`;
- `FORMAT_USER_MISSING_RANGE`;
- `FORMAT_EXTENDED_MISSING`;
- `SOURCE_CELL_ABSENT_OR_UNREPRESENTED` when genuinely required;
- `PHYSICAL_STATE_UNKNOWN`.

This vocabulary says what the file physically encodes, not what the respondent meant.

## 6. Semantic response-state vocabulary

Source authority packs may bind physical states or ordinary observed values to documented semantic states such as:

- substantive response;
- don't know;
- refusal/no answer;
- not asked;
- not applicable;
- filtered/skipped;
- no first/second answer;
- not delivered;
- source-specific typed state;
- unknown/unresolved.

The exact C11 runtime enumeration remains controlled by accepted I01/I02. Source packs bind into that accepted object model; they do not invent a parallel semantic runtime.

## 7. Respondent identity law

For every source:

1. `(source_snapshot_id, source_row_ordinal)` is retained as the irreducible replay identity.
2. Native IDs are preserved verbatim.
3. Injectivity/uniqueness is measured, not assumed.
4. Composite native identity may be authorized only by source evidence.
5. Any Rawlsing respondent ID generated during ingestion must have an exact reversible mapping receipt to the source-row identity.
6. Sorting, filtering, dropping missing rows or reindexing may never alter respondent association.

## 8. Question/event topology law

The source layer must preserve enough information to distinguish:

- scalar single-response;
- multiple-response/check-all-that-apply;
- repeated event/occurrence;
- ordered/ranked slots;
- first/second/third choice identity;
- matrix/battery member identity;
- country/local-category systems;
- source-defined branches/forms/modules;
- other source-native multiplicity.

A `(respondent, canonical_question)` uniqueness constraint is forbidden unless source authority proves that topology for the source/question.

## 9. Routing/applicability/risk-set law

Routing authority may come from source questionnaire, codebook, format metadata, explicit routing variable, or other named source authority. It may not be inferred solely from the empirical fact that a cell is missing.

The carrier must allow separate representation of:

- respondent received/was eligible for question;
- respondent did not receive/was ineligible;
- applicability unresolved;
- answer state conditional on eligibility.

Risk set remains independent of empirical condition per D08/I03 law.

## 10. Weights and design

Retain physically:

- every candidate weight/design variable;
- raw value;
- source labels/metadata;
- PSU/stratum/cluster variables;
- source missing/design states.

Authorize separately:

- weight role/name;
- estimand/target population;
- wave/country scope;
- whether normalization is lawful;
- whether multiple weights may be combined;
- variance/design method.

No implicit `default weight` exists.

## 11. Canonical mapping and interpretation

Source→canonical mapping must preserve:

- source snapshot;
- source variable/event identity;
- canonical target identity;
- exact mapping authority/hash/version;
- transformation rule;
- raw value/state;
- canonical value/state if one exists;
- unresolved/ambiguous status when no lawful mapping exists.

Mapping may enrich; it may not rewrite history.

## 12. Source certification rule

A source/release may be `CERTIFIED` only when replay proves that the C11 representation is information-equivalent for every source-native information class relevant under this constitution and accepted M01-M18 law.

Count parity, schema parity, aggregate parity, selected-query parity, or successful execution alone is insufficient.

Every source terminates as exactly one of:

- `CERTIFIED`;
- `FAILED` with exact mismatch classes;
- `BLOCKED` with exact missing authority/evidence.

## 13. Implementation prohibition until gate closure

No generic decoder or C11 source adapter implementation is accepted until:

- SR02 legacy/database genealogy has bounded legacy trust;
- SR03 physical manifests exist for all 35 source bytes;
- this constitution is reconciled against those manifests;
- WVS7 SAV and LiTS I DTA hostile fixtures demonstrate both format families can be represented without semantic collapse;
- physical carrier selection is separately adjudicated.
