# CLOSED35-R3-ARAB1 — Governed Source-Specific Realization Contract

Status: `IMPLEMENTED__READY_FOR_ABC_QUALIFICATION__TESTS_AUTHORED_NOT_EXECUTED`

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c`

Worker branch: `agent/rabochii-closed35-r3-arab1-realization-r1`

Canonical source: `Arab Barometer Wave 1.sav`

Canonical SHA-256:

`2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`

Authority class:

`L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

Semantic owner surface:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

## 1. Contract purpose

This package transposes the accepted Arab Barometer Wave 1 Authority71/72 preparation packet into one candidate-neutral source-specific realization law.

It does not read, decode, or execute the canonical SAV. It does not perform measured P2X. It does not claim whole-source physical-equivalence or ABC execution.

A/B/C may differ in physical implementation. They may not differ in source identity, replay identity, literal-text preservation, documentary routing scope, bounded-UNKNOWN handling, or source-specific semantic law.

## 2. Exact source root and physical reader state

The realization is bound to exactly:

- filename: `Arab Barometer Wave 1.sav`;
- SHA-256: `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`;
- format: SAV;
- decoder state: `SAV_NATIVE_GOVERNED`;
- source-reported character code: 65001 / UTF-8;
- compatibility override: none;
- semantic authority from decoding mode: none.

No alternate source, transport member, filename match, or cross-wave carrier may substitute for the exact canonical root.

## 3. Replay identity and native SER

Hard replay identity is:

`(canonical_source_sha256, zero_based_source_row_ordinal)`

`SER` remains a source-local respondent attribute only.

Accepted Authority71 evidence includes duplicate SER value 972 at distinct row ordinals 3021 and 3450. The realization therefore permits duplicate SER and rejects any deduplication, reindexing, or respondent merge that would collapse those rows.

Neither `SER` nor `COUNTRY+SER` is promoted to hard replay identity.

## 4. Literal source text

The exact decoded SAV text is a physical/source-native artifact and must survive unchanged.

The canonical hostile example is Q2311 code 98:

`can\u0092t choose`

The source-native questionnaire renders the corresponding response differently. That documentary difference does not authorize silent normalization of the SAV text.

Law:

1. preserve the literal decoded source string exactly;
2. never replace U+0092/U+0093 or other C1-bearing text by typography repair in the source record;
3. any display normalization must be a separate versioned transformation with explicit authority;
4. absent such authority, the display-transform state is `DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN`.

The transformation layer may produce an authorized display rendering without rewriting the source text.

## 5. Morocco routing law

The source-native questionnaire explicitly separates income fields for Morocco and non-Morocco respondents.

Accepted source-local country code:

`COUNTRY=4 -> Morocco`

The realization binds only the documented grain:

- `q715withoutmorocco` is a non-Morocco field;
- `V715onlymorocco` preserves the Morocco-only source variable distinction;
- the exact dataset alias relation between `V715onlymorocco` and printed `q715moroccoonly` remains bounded UNKNOWN;
- row applicability is evaluated from the governed country coordinate, not from missingness.

Therefore:

`physical missingness -/-> routing authority`

For any route not documentarily closed by the accepted W1 packet, the realization returns `ROUTING_BOUNDED_UNKNOWN`.

## 6. Physical design-like carriers

The questionnaire documents a broad probability-sample frame, but the accepted packet does not establish:

- an exact analytical weight field;
- a weight estimand;
- normalization;
- PSU/stratum implementation;
- clustering/stratification rules;
- a lawful default estimator.

The realization therefore permits physical preservation of any design-like carrier encountered by later execution while fixing its semantic state to:

`DESIGN_BOUNDED_UNKNOWN`

Carrier names, labels, values, or apparent design vocabulary cannot mint survey-design authority.

Absence of an obvious weight field likewise does not authorize unweighted population inference.

## 7. Bounded UNKNOWN set

The following are deliberately nonblocking and remain governed:

- display-text normalization beyond accepted source evidence;
- exact weight/design estimand and implementation;
- undocumented routing details;
- exact `V715onlymorocco` -> printed `q715moroccoonly` alias binding;
- cross-wave semantic equivalence.

`BOUNDED_UNKNOWN` is not failure. It is the required semantic state where the documentary estate does not close the assertion.

## 8. Cross-wave firewall

Wave 2, Wave 5, and Wave 8 may be structural examples only.

No W2/W5/W8 country-code meaning, respondent-ID law, Q101 special-code semantics, routing rule, weight/design role, variable ordinal, or response dictionary may be imported into Wave 1.

Same-looking names, codes, labels, or vectors do not establish equivalence.

## 9. S35 edge-class binding

Arab Barometer Wave 1 binds exactly:

- `EC01 FORMAT_FAMILY_SAV_DTA`;
- `EC07 NATIVE_ID_SCOPE_COLLISION_OR_NONINJECTIVITY`;
- `EC10 FORM_MODULE_SKIP_ROUTING_CARRIERS`;
- `EC14 COMPOUND_EDGE_INTERACTION_COURT`.

EC14 is composition only. It authorizes no source-special adapter and weakens none of the atomic invariants.

## 10. R35 physical seams

The realization binds the accepted generic contracts:

- R35-I01 `PRE553_PHYSICAL_METADATA@1.0.0`;
- R35-I02 `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` for any non-direct-raw derivative;
- R35-I03 source-scope, expectation, candidate-realization, and whole-source physical-equivalence receipt schemas.

Required physical dimensions for this source are:

- physical metadata;
- variable inventory order;
- raw storage values;
- source-SHA + row-ordinal replay identity;
- native-ID replay evidence;
- form/module/skip/routing carriers.

These hooks are physical/governance seams. They supply no source semantics.

## 11. Candidate-neutrality

One deterministic realization identity is derived from the frozen source-specific contract.

A, B, and C must carry the same:

- canonical source SHA;
- realization identity;
- literal-text law;
- replay identity law;
- routing law;
- design-UNKNOWN law;
- bounded-UNKNOWN set;
- S35/R35 binding.

Candidate identity may never select a different semantic interpretation.

## 12. Implementation

Implementation module:

`rawlsing_next/closed35_arab1_realization.py`

Authored hostile tests:

`rawlsing_next/tests/test_closed35_r3_arab1_realization.py`

The test suite is source-independent and does not open the SAV.

Browser-only worker state:

`TESTS_AUTHORED__NOT_EXECUTED`

## 13. Proof boundary

Not claimed:

- real-source execution;
- source decoding;
- whole-source physical-equivalence PASS;
- ABC execution PASS;
- I05 PASS;
- measured P2X;
- source certification beyond accepted Authority71/72 preparation;
- display-text repair authority;
- weight/design estimand authority;
- undocumented routing closure.

Terminal:

`CLOSED35_R3_ARAB_BAROMETER_W1_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
