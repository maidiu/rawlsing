# CLOSED35-R2-ASIAN5 — Realization Contract

Schema: `CLOSED35_R2_ASIAN5_REALIZATION_CONTRACT@1.0.0`

## 1. Source root

The realization is valid only for:

- filename: `Asian Barometer Wave 5.sav`
- SHA-256: `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63`
- format: `SAV`
- accepted reader mode: `SAV_NATIVE_GOVERNED`
- replay law: `SOURCE_SHA256+ROW_ORDINAL`

Any source-root drift fails closed.

## 2. Semantic-owner law

The source-specific owner surface is candidate-neutral:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

A/B/C bind the same realization identity. Candidate identity has no semantic jurisdiction.

## 3. Native respondent identity

`COUNTRY` and `IDnumber` are preserved as source-local attributes.

They are not the hard replay key. The accepted packet proves `COUNTRY+IDnumber` is noninjective for two Hong Kong pairs. No deduplication, respondent merging, longitudinal continuity or cross-wave identity may be inferred from native IDs.

## 4. Native MR sets

The exact source topology is normative:

| Set | Kind | Counted value | Members | Semantic state |
|---|---|---:|---|---|
| IR3a | DICHOTOMY | 1 | IR3a_1..IR3a_5 | Core questionnaire supports multiple-answer topology |
| Q112 | DICHOTOMY | 1 | SE15A..SE15M | `BOUNDED_UNKNOWN` semantic alias; not questionnaire Q112 by name |
| SE15 | DICHOTOMY | 1 | SE15A..SE15O | Core questionnaire supports SE15 A–O asset battery |

Required overlap:

`Q112 ∩ SE15 = SE15A..SE15M`

Forbidden:

- flattening MR sets into scalar variables;
- merging Q112 and SE15 because their members overlap;
- aliasing Q112 to SE15 by equal vectors/names;
- aliasing native MR `Q112` to questionnaire item 112 by string equality;
- changing counted value or member order/identity.

## 5. Routing and applicability

Preserved module surfaces:

### India module
Variables: `Q106c`, `Q106d`, `Q106e`.

The source packet identifies an India-specific module, but exact eligibility, wording provenance and routing semantics require country-team authority. Those details remain `BOUNDED_UNKNOWN`.

### ASEAN q186
The core questionnaire marks q186 ASEAN-only.

The exact source risk set and the meaning of merged ordinary `-1` values remain `BOUNDED_UNKNOWN`.

For both modules:

`physical/ordinary missing-looking storage -/-> routing authority`

Routing cannot be inferred from missingness, sentinel frequency, country-code guesses, or candidate behavior.

## 6. Geography

The raw SAV geography carrier remains physical source-local authority.

The generic instrument country-code list and merged SAV country dictionary are two evidence layers. Their exact reconciliation is not authorized here.

No automatic recoding, harmonization or cross-wave geography identity is permitted.

## 7. Weight

The source carrier `w` is preserved exactly as a candidate weight/design variable.

No default analytical use is authorized.

The following remain `BOUNDED_UNKNOWN`:

- estimand;
- normalization;
- population/domain;
- default-selection rule;
- PSU/strata relation;
- variance method.

## 8. Ordinary sentinel preservation

The accepted source packet records ordinary `-1` storage with zero physical typed-missing cells.

This realization preserves the law that ordinary stored values are not promoted to physical system/user missing or semantic not-asked states by label/name alone.

No new variable-level semantic meaning for `-1` is minted here.

## 9. S35 edge scope

Exact applicable classes:

- EC01 `FORMAT_FAMILY_SAV_DTA`
- EC07 `NATIVE_ID_SCOPE_COLLISION_OR_NONINJECTIVITY`
- EC08 `NATIVE_MULTIPLE_RESPONSE_SET_TOPOLOGY`
- EC10 `FORM_MODULE_SKIP_ROUTING_CARRIERS`
- EC12 `WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN`
- EC13 `SOURCE_LOCAL_COORDINATE_CARRIERS`
- EC14 `COMPOUND_EDGE_INTERACTION_COURT`

EC14 composes the atomic obligations. It is not an adapter and adds no semantics.

## 10. R35 hooks

Bind:

- `PRE553_PHYSICAL_METADATA@1.0.0`
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` for non-direct raw carriers
- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

These are physical/lineage contracts only. They do not supply survey meaning.

## 11. Claim boundary

This contract means only:

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`

It does not mean source bytes were executed, physical equivalence passed, A/B/C ran, I05 passed, or measured P2X occurred.
