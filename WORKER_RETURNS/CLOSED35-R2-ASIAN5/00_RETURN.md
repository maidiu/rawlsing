# CLOSED35-R2-ASIAN5 — Asian Barometer Wave 5 Governed Source-Specific Realization

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c`

Branch: `agent/rabochii-closed35-r2-asian5-realization-r1`

Source: `Asian Barometer Wave 5.sav`

Canonical SHA-256: `2576e428ff8de3c8d93a418c9120a1c2955ab7b1f35961d8c18fa562bc4b5e63`

Authority class: `L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

## Disposition

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`

The accepted Asian Barometer Wave 5 source packet is now represented by one candidate-neutral governed realization in:

- `rawlsing_next/closed35_asian5_realization.py`
- `rawlsing_next/tests/test_closed35_r2_asian5_realization.py`

No raw survey carrier was opened. No real source processing was executed. No measured P2X was run. A/B/C were not executed.

Synthetic tests were authored but browser tooling did not execute them:

`TESTS_AUTHORED__NOT_EXECUTED`

## Governing realization law

### Replay identity

The hard replay identity is exactly:

`(canonical_source_sha256, zero_based_source_row_ordinal)`

`COUNTRY + IDnumber` remains source-local evidence only. The accepted packet contains duplicate Hong Kong country+ID pairs, so native IDs cannot replace row-ordinal replay identity or support deduplication/cross-wave identity.

### Native multiple-response topology

All three native MR sets are preserved as distinct source identities:

- `IR3a`: dichotomy; counted value 1; `IR3a_1..IR3a_5`;
- `Q112`: dichotomy; counted value 1; `SE15A..SE15M`;
- `SE15`: dichotomy; counted value 1; `SE15A..SE15O`.

The exact overlap is:

`Q112 ∩ SE15 = SE15A..SE15M`

Overlap does not authorize set collapse or semantic aliasing. The native MR-set name `Q112` is explicitly not treated as questionnaire item 112 semantics. Its exact merged-data semantic alias remains `BOUNDED_UNKNOWN`.

### Routing

The source-specific owner preserves:

- India-specific `Q106c/Q106d/Q106e` module topology;
- `q186` ASEAN-only documentary topology.

It does not derive applicability from ordinary `-1`, missingness, observed support, or geopolitical inference.

The India country-team semantics/routing and exact q186 source risk set remain bounded documentary unknowns.

### Geography

Raw source `COUNTRY` remains a source-local coordinate carrier.

The relationship between the merged SAV geography dictionary and the generic W5 core-instrument country coding remains `BOUNDED_UNKNOWN`. No cross-wave or instrument-to-merged recoding is synthesized.

### Weight

The raw `w` carrier is preserved.

Its exact estimand, normalization, scope, default use and variance design remain `BOUNDED_UNKNOWN`. Presence of `w` does not authorize default weighting.

### Candidate neutrality

A, B and C must consume one immutable source-specific realization identity. Candidate identity may not alter:

- replay identity;
- MR-set identity/membership/overlap;
- routing topology or unresolved state;
- geography authority;
- weight meaning;
- bounded-unknown state.

Different physical realization strategies may be qualified later. Different source semantics are divergence.

## S35 / R35 binding

Applicable S35 edge classes are frozen to:

`EC01; EC07; EC08; EC10; EC12; EC13; EC14`

EC14 is composition only and introduces no special source adapter or semantic authority.

The realization binds the accepted R35 schema seams:

- I01 physical metadata;
- I02 derivative parentage for any non-direct raw carrier;
- I03 whole-source physical-equivalence scope/expectation/candidate/receipt schemas.

Required physical dimensions include physical metadata, variable order, raw storage, row replay, native-ID evidence, native MR sets, routing carriers, weight/design carriers and source-local coordinates.

This browser implementation does not materialize an R35 physical-equivalence receipt and does not claim real-source equivalence.

## Terminal

`CLOSED35_R2_ASIAN_BAROMETER_W5_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
