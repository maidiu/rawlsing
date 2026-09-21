# CLOSED35-R3-ASIAN4 — Asian Barometer Wave 4 Governed Source-Specific Realization

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c`

Branch: `agent/rabochii-closed35-r3-asian4-realization-r1`

Source: `Asian Barometer Wave 4.sav`

Canonical SHA-256: `4d914817509d0e5f3adde49707df148f696992055937f085080a016002a39200`

Authority class: `L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

Candidate-neutral semantic owner: `PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

## Disposition

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`

The accepted Asian Barometer Wave 4 packet is now represented by one candidate-neutral governed realization in:

- `rawlsing_next/closed35_asian4_realization.py`
- `rawlsing_next/tests/test_closed35_r3_asian4_realization.py`

Required return materials are in this directory.

No raw survey carrier was opened. No real source processing was executed. No measured P2X was run. Candidate A/B/C were not executed.

Synthetic tests were authored but not executed on the GitHub/browser surface:

`TESTS_AUTHORED__NOT_EXECUTED`

## Authority basis

The realization binds the accepted CLOSED_35/S35 canonical root and Authority71/72 preparation law for this exact source.

Authority71 R03 establishes the Wave-4 source-specific physical/documentary packet: ordinary stored `-1`, merged-data versus core-instrument country-code drift, ordered q20/q21/q22 and q99/q99a/q99b structures, q172 marked `ASEAN countries only`, and distinct `w` / `w_cross` carriers.

Authority72 classifies this source as:

`L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

with hard replay identity:

`SOURCE_SHA256+ROW_ORDINAL`

Authority71/72 preparation is not source certification.

## Governing realization law

### Replay identity

Hard replay identity is exactly:

`(canonical_source_sha256, zero_based_source_row_ordinal)`

Native `country` and `idnumber` may survive as source attributes. They do not replace row-ordinal replay authority and do not create cross-wave identity.

### Ordinary -1 versus physical missingness

The accepted packet records Wave-4 `-1` as ordinary stored values with zero physical typed-missing cells in the prepared snapshot.

The realization therefore preserves all three layers separately:

1. physical stored value: `-1`;
2. physical class: `OBSERVED_STORAGE_VALUE`;
3. semantic state: variable-local `BOUNDED_UNKNOWN` unless exact documentary authority closes that variable.

Forbidden:

- `-1 == SYSTEM_MISSING`;
- `-1 == USER_MISSING`;
- one universal semantic assignment for all Wave-4 `-1` values;
- routing derived from `-1` incidence.

### Merged-data geography versus instrument geography

The merged SAV `country` carrier and questionnaire/instrument `SE1` coding are preserved as distinct evidence layers.

The accepted authority packet proves a concrete coding drift for codes 3–8. Therefore:

- raw merged-data coordinates remain source-local replay evidence;
- instrument codes remain documentary instrument evidence;
- the relationship between the two remains `BOUNDED_UNKNOWN`;
- no silent harmonization or cross-wave recoding is authorized.

### Ranked-slot topology

Two ordered structures are preserved:

- `q20 / q21 / q22`;
- `q99 / q99a / q99b`.

For q99, the recovered core questionnaire explicitly supports first response / optional second / optional third ordering.

Ordered multiplicity is physical/topological information. Flattening, reordering or deduplication is rejected.

### q172 routing

The recovered core questionnaire marks q172:

`ASEAN countries only`

That documentary grain is preserved exactly.

The realization does **not** manufacture an exact merged-source country/row risk set and does not interpret ordinary `-1` incidence as routing authority. Exact row-level applicability remains:

`BOUNDED_UNKNOWN__EXACT_SOURCE_RISK_SET_NOT_CLOSED`

Applying q172 as an all-country module is rejected.

### w and w_cross

`w` and `w_cross` survive as two distinct physical/documentary carriers.

No alias, default weight, estimand, normalization, population/domain, PSU/strata relation or variance method is invented.

Those roles remain `BOUNDED_UNKNOWN`.

### Cross-wave boundary

Wave 1 and Wave 5 may supply structural examples only. Their encoding, MR sets, IDs, routing rules, geography, dictionaries and weight semantics are not imported into Wave 4.

## Bounded UNKNOWN set preserved

The implementation preserves these accepted unresolved states:

- merged-data versus instrument geography reconciliation;
- variable-local semantic meaning of ordinary `-1` values where not documented;
- exact q172 merged-source risk set / row routing;
- weight-role/estimand/normalization/default-use semantics for `w` and `w_cross`;
- any native-ID semantics beyond source-local attribute preservation.

These are governed unknowns, not blockers to source-specific realization.

## S35 edge classes bound

Exact Wave-4 edge tuple from the accepted S35 matrix:

`EC01; EC05; EC09; EC10; EC12; EC13`

- EC01 — format family SAV/DTA;
- EC05 — physical missingness multiclass;
- EC09 — ordered/repeated slot topology;
- EC10 — form/module/skip/routing carriers;
- EC12 — weight/design multiplicity and domain;
- EC13 — source-local coordinate carriers.

EC14 is **not** assigned to Asian Barometer Wave 4 by the canonical S35 matrix and is not invented here.

## R35 hooks bound

- I01: `PRE553_PHYSICAL_METADATA@1.0.0`
- I02: `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` for any non-direct raw carrier
- I03:
  - `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
  - `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
  - `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
  - `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

These hooks are physical/lineage contracts only and confer no survey semantics.

## Candidate neutrality

A, B and C must bind one deterministic source-specific realization identity.

Candidate-local implementation strategy may differ later. Candidate identity may not alter:

- source root;
- replay identity;
- ordinary `-1` physical classification;
- variable-local UNKNOWN semantics;
- ranked topology;
- q172 documentary scope / unresolved exact risk set;
- merged/instrument geography separation;
- `w` / `w_cross` distinctness or unresolved roles;
- R35 physical-boundary meaning.

Different source semantics are candidate divergence.

## Tests authored

The synthetic rejection court covers:

- native ID promoted to replay identity;
- source-SHA drift;
- `-1 == SYSTEM_MISSING`;
- global semantic assignment to all `-1`;
- merged/instrument geography collapse;
- q172 application outside documented ASEAN-only scope;
- routing inferred from missingness/country storage;
- ranked-slot flattening/reordering;
- `w`/`w_cross` aliasing;
- default-weight invention;
- cross-wave semantic leakage;
- candidate-specific semantic divergence;
- S35/R35 scope drift.

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

## Explicit proof boundary

This browser implementation proves only:

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED`

It does **not** claim:

- real-source execution;
- source decoding on the canonical SAV;
- whole-source physical-equivalence PASS;
- Candidate A/B/C execution or parity;
- I05 PASS;
- measured P2X;
- source certification beyond accepted authority;
- exact q172 row risk set;
- survey-design/weight estimands;
- merged/instrument geography reconciliation.

## Terminal

`CLOSED35_R3_ASIAN_BAROMETER_W4_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
