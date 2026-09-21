# CLOSED35-R3-ASIAN4 — Realization Contract

Schema: `CLOSED35_R3_ASIAN4_REALIZATION_CONTRACT@1.0.0`

## 1. Exact source root

This realization is valid only for:

- filename: `Asian Barometer Wave 4.sav`
- SHA-256: `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200`
- format: `SAV`
- accepted reader mode: `SAV_NATIVE_GOVERNED`
- source-reported encoding in Authority71 packet: `UTF-8`
- replay law: `SOURCE_SHA256+ROW_ORDINAL`

Any source-root or reader-mode drift fails closed.

## 2. Semantic-owner law

The source-specific owner is candidate-neutral:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

Candidate A/B/C must bind the same source-specific realization identity. Candidate identity has no semantic jurisdiction.

## 3. Replay identity

Hard replay key:

`(canonical_source_sha256, zero_based_source_row_ordinal)`

Native `country` and `idnumber` remain source attributes only.

Even where an accepted packet reports local injectivity for a native composite, injectivity is not authority to replace row-ordinal replay, establish longitudinal identity or create cross-wave respondent identity.

## 4. Ordinary stored -1

Wave-4 ordinary `-1` values are preserved as:

- raw storage value: `-1`;
- physical state: `OBSERVED_STORAGE_VALUE`;
- semantic state: `BOUNDED_UNKNOWN` at variable-local grain unless exact documentary authority closes it.

Forbidden transformations:

- `-1 -> SYSTEM_MISSING`;
- `-1 -> USER_MISSING`;
- one global Wave-4 meaning for `-1`;
- `-1 -> NOT_ASKED` without exact authority;
- `-1` frequency/incidence -> routing rule.

Physical missingness and semantic response/routing meaning are separate jurisdictions.

## 5. Geography evidence layers

Two distinct layers survive:

### Merged source layer

Carrier: `country`

Authority: exact source-local physical/data coordinate.

### Instrument layer

Carrier/documentary field: `SE1`

Authority: source-native core questionnaire country coding.

Authority71 documents that merged SAV codes and instrument codes diverge for codes 3–8.

Therefore:

`MERGED_COUNTRY_CODE != INSTRUMENT_SE1_CODE_BY_ASSUMPTION`

The exact release mapping between those layers remains:

`BOUNDED_UNKNOWN`

Forbidden:

- applying SE1 code labels directly to merged SAV values;
- rewriting merged codes to instrument codes;
- silent harmonization;
- importing W1/W5 geography mappings.

## 6. Ranked-slot topology

Exact ordered source structures:

### Q20 family

`q20 -> q21 -> q22`

Ordering/multiplicity are preserved. Item-role refinement beyond accepted physical/ranked evidence remains bounded where not documentarily closed.

### Q99 family

`q99 -> q99a -> q99b`

The recovered Wave-4 core questionnaire supports:

1. first response;
2. second response optional;
3. third response optional.

Forbidden:

- scalar flattening;
- slot reordering;
- deduplication by equal values;
- inferring one slot's semantics from another.

## 7. q172 routing/applicability

Documented instrument rule:

`ASEAN_COUNTRIES_ONLY`

That rule is authoritative at the recovered questionnaire grain.

The following remain `BOUNDED_UNKNOWN`:

- exact merged-source country risk set;
- exact row-level applicability;
- whether every ordinary `-1` value represents inapplicability;
- any routing rule reconstructed solely from observed support or missing-looking values.

Required behavior:

- preserve q172 module/routing topology;
- reject all-country applicability;
- do not infer exact row eligibility from `country` storage or `-1` incidence.

## 8. Weight carriers

Exact distinct carriers:

- `w`
- `w_cross`

Both survive separately.

No default analytical weight is authorized.

For each carrier, these remain `BOUNDED_UNKNOWN` absent exact release authority:

- estimand;
- normalization;
- population/domain;
- default-selection rule;
- PSU/strata relation;
- variance method;
- lawful relationship between `w` and `w_cross`.

Forbidden:

- aliasing `w == w_cross`;
- silently selecting one as default;
- combining or normalizing them by convention;
- importing Wave-1 or Wave-5 weight roles.

## 9. Cross-wave boundary

Only generic structural preservation law may be reused across Asian Barometer waves.

Wave-specific semantic authority may not cross into Wave 4 by variable-name similarity, cleaner text, matching values, family convention or newer documentation.

In particular, do not import:

- Wave 1 BIG-5/missingness rules;
- Wave 5 native MR-set topology;
- Wave 5 respondent-ID collision semantics;
- Wave 5 India/q186 modules;
- any Wave 1/5 geography or weight interpretation.

## 10. S35 edge scope

Exact applicable classes:

- EC01 `FORMAT_FAMILY_SAV_DTA`
- EC05 `PHYSICAL_MISSINGNESS_MULTICLASS`
- EC09 `ORDERED_REPEATED_SLOT_TOPOLOGY`
- EC10 `FORM_MODULE_SKIP_ROUTING_CARRIERS`
- EC12 `WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN`
- EC13 `SOURCE_LOCAL_COORDINATE_CARRIERS`

No EC14 assignment exists for this source in the accepted S35 matrix; this realization does not mint one.

## 11. R35 hooks

Bind:

- `PRE553_PHYSICAL_METADATA@1.0.0`
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` for non-direct raw carriers
- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

Required physical dimensions include:

- physical metadata;
- variable inventory/order;
- raw storage values;
- row replay identity;
- physical missingness;
- ordered/repeated-slot topology;
- module/routing carriers;
- weight/design carriers;
- source-local coordinate carriers.

R35 hooks supply physical/lineage jurisdiction only, never survey semantics.

## 12. Bounded UNKNOWN set

Preserve explicitly:

- merged/instrument geography reconciliation;
- variable-local `-1` semantics where not documented;
- exact q172 merged-source risk set / row routing;
- `w` / `w_cross` estimand, normalization, scope and default use;
- native-ID semantics beyond source-local attribute preservation.

These states do not block realization.

## 13. Claim boundary

This contract means only:

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`

It does not mean:

- canonical SAV executed;
- real-source decode occurred;
- whole-source physical-equivalence receipt passed;
- A/B/C ran;
- I05 passed;
- measured P2X ran;
- source certification occurred;
- unresolved documentary states were closed.
