# CLOSED35-R3-ARAB1 — Hostile Test Protocol

Status:

`TESTS_AUTHORED__NOT_EXECUTED`

Browser/GitHub-only worker. No local Python execution, raw SAV access, source decoding, or measured P2X occurred.

Implementation test file:

`rawlsing_next/tests/test_closed35_r3_arab1_realization.py`

## Court purpose

The tests are rejection tests for semantic overreach. They prove the realization law fails closed when a consumer attempts to convert physical evidence, source-local names, or cross-wave resemblance into authority the accepted Wave-1 documentary packet does not contain.

## T01 — SER uniqueness / replay invention

Fixture:

- same `SER=972`;
- distinct source row ordinals 3021 and 3450.

Required:

- both rows survive;
- hard replay keys remain distinct;
- `SER` is preserved as a source-local attribute.

Reject:

- deduplication by SER;
- SER as replay key;
- COUNTRY+SER promoted to replay authority without stronger source law.

## T02 — literal C1 text preservation

Fixture:

`Q2311 code 98 -> "can\u0092t choose"`

Required:

- literal source string round-trips unchanged.

Reject:

- curly-apostrophe repair;
- ASCII apostrophe replacement;
- title-casing or wording expansion inside source truth.

## T03 — display normalization requires explicit authority

Mutation:

replace literal SAV text with documentary rendering.

Required:

- transformation without separately named authority raises
  `DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN`;
- separately authorized display rendering may exist without rewriting the source string.

## T04 — Morocco routing distinction

Fixtures:

- `COUNTRY=4`;
- non-Morocco country;
- `q715withoutmorocco`;
- `V715onlymorocco`.

Required:

- non-Morocco field is excluded for Morocco;
- Morocco-only source variable remains separate;
- exact dataset-to-printed alias remains bounded UNKNOWN.

Reject:

- collapsing both variables;
- applying one code system universally;
- guessing alias semantics from complementary missingness.

## T05 — routing from missingness

Run the same documented route with different physical missing-state inputs.

Required:

- route result is invariant to observed missingness.

Reject:

`physical missing -> not asked/applicable`

## T06 — undocumented routing

Fixture:

a variable without an accepted W1 route.

Required:

`ROUTING_BOUNDED_UNKNOWN`

Reject:

- routing from variable name;
- routing from layout;
- routing from empirical missingness;
- importing W2/W5/W8 programmer rules.

## T07 — design inference from carrier names

Fixtures may use names such as:

- `WT`;
- `PSU`;
- `STRATUM`.

Required:

- physical value/metadata can be preserved;
- semantic state remains `DESIGN_BOUNDED_UNKNOWN`.

Reject:

- analytical-weight authorization;
- PSU/stratum authority;
- default estimator selection;
- inference from a field label/name/value.

## T08 — absence-of-weight inference

Required law:

absence of an obvious weight carrier does not authorize an unweighted population estimator.

This is a documentary negative admission, not a raw-data claim.

## T09 — cross-wave semantic leakage

Attempt to bind Wave 2/5/8 authority to the Wave-1 source root.

Required:

fail closed with cross-wave semantic leakage.

Reject imported:

- Q101 code semantics;
- country mapping;
- native ID law;
- routing;
- weight/design semantics;
- variable ordinals/dictionaries.

## T10 — candidate-specific semantic divergence

Create A/B/C bindings.

Required:

- exact same source SHA;
- exact same source-specific realization identity.

Mutation:

give C a different realization identity.

Required:

fail closed.

## T11 — S35/R35 freeze

Required exact S35 edge set:

- EC01;
- EC07;
- EC10;
- EC14.

Required R35 seams:

- I01 physical metadata;
- I02 derivative parentage for non-direct raw;
- I03 source scope / canonical expectation / candidate realization / whole-source physical-equivalence receipt.

Required dimensions include:

- physical metadata;
- variable inventory order;
- raw storage values;
- row replay identity;
- native-ID replay evidence;
- routing carriers.

No R35 hook has semantic authority.

## Future real-source qualification court

Later ABC qualification must additionally consume the accepted Authority71 hostile source evidence, including:

- C1-bearing metadata strings;
- duplicate SER rows;
- physical missingness fixture;
- q715 non-Morocco / Morocco-only source variables;
- exact country coordinate;
- source-native topology evidence.

That future court must not claim PASS unless all applicable EC01/EC07/EC10 invariants pass simultaneously under EC14.

## Current execution statement

`TESTS_AUTHORED__NOT_EXECUTED`

No source qualification claim follows from this authored test protocol.
