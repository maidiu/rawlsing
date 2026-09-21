# CLOSED35-R3-ARAB1 — Arab Barometer Wave 1 Governed Source-Specific Realization

Repository: `maidiu/rawlsing`

Base:

`agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c`

Worker branch:

`agent/rabochii-closed35-r3-arab1-realization-r1`

Canonical source:

`Arab Barometer Wave 1.sav`

Canonical SHA-256:

`2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`

Authority class:

`L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

## Disposition

`IMPLEMENTED__CANDIDATE_NEUTRAL_SOURCE_SPECIFIC_REALIZATION__TESTS_AUTHORED_NOT_EXECUTED`

The accepted Arab Barometer Wave 1 physical/documentary packet is now transposed into one candidate-neutral governed realization law.

Implementation:

- `rawlsing_next/closed35_arab1_realization.py`
- `rawlsing_next/tests/test_closed35_r3_arab1_realization.py`

Return package:

- `01_REALIZATION_CONTRACT.md`
- `02_IDENTITY_TEXT_ROUTING_MAP.csv`
- `03_PHYSICAL_EDGE_BINDING.json`
- `04_TEST_PROTOCOL.md`
- `RETURN.json`

## Source law implemented

### Replay identity

Hard replay identity is:

`SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

`SER` is preserved as a source-local attribute only.

The accepted duplicate-SER hostile pair (`SER=972` at row ordinals 3021 and 3450) remains two distinct respondents. Neither `SER` nor `COUNTRY+SER` may be promoted to hard replay identity.

### Literal source text

C1-bearing decoded SAV text is preserved literally.

The canonical hostile example remains:

`Q2311 code 98 -> can\u0092t choose`

No typography repair, curly-apostrophe substitution, ASCII replacement, or wording expansion is permitted inside source truth.

A separately governed display transformation may exist, but without explicit transformation authority its state is:

`DISPLAY_TEXT_TRANSFORM_BOUNDED_UNKNOWN`

### Morocco routing

The W1 questionnaire explicitly documents `COUNTRY=4` as Morocco and separates Morocco-only from non-Morocco income fields.

The realization preserves:

- `q715withoutmorocco` as non-Morocco scope;
- `V715onlymorocco` as the separate Morocco-only source variable;
- the exact dataset-variable to printed-question alias as bounded UNKNOWN where the accepted packet did not close it.

Routing is determined from documentary authority and governed country state, never from response missingness.

All other undocumented routing remains:

`ROUTING_BOUNDED_UNKNOWN`

### Design / weight boundary

The accepted packet documents broad probability-sample language but does not establish an exact dataset weight field, estimand, normalization rule, PSU/stratum implementation, or lawful default estimator.

Accordingly:

- physical design-like carriers may be preserved;
- carrier names or values do not create survey-design authority;
- absence of an obvious weight does not authorize unweighted population inference;
- unresolved design semantics remain `DESIGN_BOUNDED_UNKNOWN`.

### Cross-wave firewall

No semantics are imported from Arab Barometer Waves 2, 5, or 8.

Same-looking names, codes, labels, ordinals, routing patterns, IDs, or weight/design carriers are not equivalence authority.

## Bounded UNKNOWNs preserved

- display-text normalization beyond accepted source evidence;
- exact weight/design estimand and implementation;
- undocumented routing details;
- exact `V715onlymorocco` -> printed `q715moroccoonly` alias binding;
- cross-wave semantic equivalence.

These states are nonblocking under the L1 realization law.

## S35 edge classes

Exact source scope:

- `EC01 FORMAT_FAMILY_SAV_DTA`
- `EC07 NATIVE_ID_SCOPE_COLLISION_OR_NONINJECTIVITY`
- `EC10 FORM_MODULE_SKIP_ROUTING_CARRIERS`
- `EC14 COMPOUND_EDGE_INTERACTION_COURT`

No Arab-1 special physical adapter was invented.

## R35 hooks

Bound:

- R35-I01 `PRE553_PHYSICAL_METADATA@1.0.0`;
- R35-I02 `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` for non-direct-raw derivatives;
- R35-I03 source-scope / canonical-expectation / candidate-realization / whole-source-equivalence receipt schemas.

Required dimensions include physical metadata, ordered variable inventory, raw storage values, row replay identity, native-ID replay evidence, and routing carriers.

R35 hooks have no semantic jurisdiction.

## Candidate neutrality

A/B/C bind one deterministic source-specific realization identity and one semantic owner surface:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

Candidate-specific semantic divergence is rejected.

## Tests

Eleven source-independent hostile tests are authored covering:

- SER uniqueness/replay invention;
- literal text normalization without authority;
- authorized display transform separation;
- Morocco routing collapse;
- routing from missingness;
- undocumented routing invention;
- design inference from carrier names;
- absence-of-weight overreach;
- cross-wave semantic leakage;
- candidate-specific semantic divergence;
- S35/R35 scope drift.

Execution state:

`TESTS_AUTHORED__NOT_EXECUTED`

## Explicit proof boundary

This worker did not:

- open local/raw survey carriers;
- execute real source processing;
- decode the canonical SAV;
- run measured P2X;
- run ABC qualification;
- run whole-source physical-equivalence;
- claim I05 PASS;
- promote Authority71/72 preparation to source certification.

The implementation is ready for the later exact-source ABC qualification court.

## Terminal

`CLOSED35_R3_ARAB_BAROMETER_W1_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
