# CLOSED35-R3-EVS1981 — EVS 1981 Governed Source-Specific Realization

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c`

Worker branch: `agent/rabochii-closed35-r3-evs1981-realization-r1`

Return: `WORKER_RETURNS/CLOSED35-R3-EVS1981/`

Canonical source: `EVS 1981.sav`

Canonical SHA-256: `5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2`

Authority class: `L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

Accepted decoder condition: `SAV_SOURCE_DECLARED_WINDOWS1252`

Candidate-neutral semantic owner: `EVS1981_SEMANTIC_OWNER_V1`

Downstream semantic surface: `PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

## Disposition

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__TESTS_AUTHORED_NOT_EXECUTED`

This return realizes the accepted EVS 1981 Authority71/72 packet at browser implementation grain. It does not open the canonical SAV, re-run the accepted source probes, execute Candidate A/B/C, issue a whole-source physical-equivalence receipt, run I05, or run measured P2X.

The realization is exact-source-bound and candidate-neutral. A/B/C may differ in physical implementation only after later qualification; they may not differ in source semantics, replay identity, missing-state treatment, ranked topology, coordinate scope, weight authority, or bounded-UNKNOWN behavior.

## Accepted authority inputs

- CLOSED_35 canonical source registry at base `da33eb6a8225c14eee9490633a3263388dc5536c`;
- S35 source-to-edge matrix at that base;
- Authority71 EVS R04 packet at `3bc063aa7bf461caf5baf581ff32a434ba9e09a3`;
- Authority72 R10 synthesis at `3356b26f2dc518043ffde171c2dca0470b5ac79f`;
- accepted SR09-PRE EVS source-specific burden surfaces already consumed by Authority71.

No neighboring EVS wave is semantic authority for EVS 1981.

## Implemented law

### 1. Exact source and replay identity

The only hard replay identity is:

`SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

The accepted packet preserves `id_cocas` and `caseno` as source attributes. Their injectivity, cross-country scope, cross-wave scope, and identity semantics are not established strongly enough to replace row replay.

Native IDs therefore remain preserved but non-authoritative for replay identity.

### 2. Source-declared Windows-1252 is physical metadata, not semantic license

The exact source declares `windows-1252` with machine character code `1252`.

This release does not inherit the EVS 1999/2008 latin1 compatibility path and does not inherit later-wave UTF-8 behavior.

The realization preserves the source-declared encoding metadata as an exact physical reader/config obligation. Readability of text does not create additional questionnaire/codebook/routing authority.

### 3. Positive-valued user-missing declaration on v308

Accepted source metadata declares `v308` missing over both:

- numeric range `-5..-1`; and
- discrete positive value `3`.

The realization therefore separates three layers:

1. **raw storage value** — the physical stored number is preserved verbatim;
2. **physical missing class** — a value covered by the source user-missing declaration is `USER_MISSING`;
3. **semantic reason** — the reason/meaning of positive missing code `3` remains `BOUNDED_UNKNOWN__V308_CODE3_REASON` unless later exact documentary authority closes it.

A positive number does not become a substantive response merely because it is positive.

Semantic missing classification must not erase or replace the raw stored value.

The accepted aggregate packet does not claim observed code-3 incidence; it proves the declaration. This worker does not invent an observed count.

### 4. Ranked-slot topology

The accepted ranked structure is preserved exactly as the ordered source-local triplet:

- ordinal 270: `v460`;
- ordinal 271: `f460`;
- ordinal 272: `v461`.

The topology is retained as first-slot / flag / second-slot structure at accepted packet grain.

It may not be flattened, deduplicated, reordered, or replaced by a later EVS ranked structure.

### 5. Release-specific coordinate tuple

The EVS 1981 source-local coordinate carriers are preserved independently:

- `studyno` (ordinal 0);
- `studynoc` (1);
- `version` (2);
- `versionc` (3);
- `year` (6);
- `country` (7);
- `c_abrv` (8);
- `cntry_y` (10).

No `country1`, `c_abrv1`, or `cntry1_y` split-up companions are imported from EVS 1990/1999/2008.

Coordinate presence is physical authority. Cross-release code equivalence or harmonization is not inferred.

### 6. weight_g remains a carrier, not an estimator command

`weight_g` at source ordinal 9 is preserved as the EVS 1981 weight carrier.

No default-weight selection, estimand, normalization, target-population meaning, or design role is created from the variable name or presence.

Exact weight estimand remains:

`BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`

until downstream statistical use obtains stronger exact authority.

### 7. Candidate-neutral semantic law

Candidates A, B and C must bind the same:

- canonical source SHA;
- replay identity law;
- source-declared encoding condition;
- v308 raw/declaration/semantic-state separation;
- ranked-slot topology;
- release-specific coordinate tuple;
- weight-carrier law;
- bounded UNKNOWN set;
- S35 edge set;
- R35 hooks;
- semantic owner `EVS1981_SEMANTIC_OWNER_V1`.

Candidate-specific semantic divergence is rejected.

## Bounded UNKNOWN set preserved

The realization deliberately retains:

- `BOUNDED_UNKNOWN__NATIVE_ID_SCOPE`;
- `BOUNDED_UNKNOWN__V308_CODE3_REASON`;
- `BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`;
- `BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`.

These are valid governed states. They do not block source-specific realization and may not be filled by analogy, sign, variable name, cross-wave reuse, or observed missingness.

## S35 edge classes bound

Exact matrix scope:

- `EC01` — FORMAT_FAMILY_SAV_DTA;
- `EC02` — EXPLICIT_TEXT_DECODING_MODE;
- `EC05` — PHYSICAL_MISSINGNESS_MULTICLASS;
- `EC09` — ORDERED_REPEATED_SLOT_TOPOLOGY;
- `EC12` — WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN;
- `EC13` — SOURCE_LOCAL_COORDINATE_CARRIERS.

No EVS1981-specific edge class and no compound EC14 claim are invented.

## R35 hooks bound

The realization binds the accepted generic seams:

- R35-I01: `PRE553_PHYSICAL_METADATA@1.0.0`;
- R35-I02: `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0` where a non-direct-raw or persisted derivative is used;
- R35-I03:
  - `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`;
  - `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`;
  - `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`;
  - `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`.

A later I03 PASS, if obtained, remains:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

The R35 seams carry no semantic authority.

## Implementation files

No runtime Python/source-processing implementation file is added by this browser-only realization.

The realization is implemented declaratively in the governed return packet:

- `00_RETURN.md`;
- `01_REALIZATION_CONTRACT.md`;
- `02_MISSING_RANK_COORDINATE_MAP.csv`;
- `03_PHYSICAL_EDGE_BINDING.json`;
- `04_TEST_PROTOCOL.md`;
- `RETURN.json`.

This matches the accepted declarative R2 realization pattern: source-specific law can be frozen without pretending browser code executed the real carrier.

## Test status

Rejection tests are authored in `04_TEST_PROTOCOL.md`.

Execution status:

`TESTS_AUTHORED__NOT_EXECUTED`

No browser-side PASS is fabricated.

## Explicit proof boundary

This worker does **not** claim:

- local/raw SAV opened;
- real-source decoding or processing;
- remeasurement of Authority71 fixtures;
- whole-source physical-equivalence PASS;
- Candidate A/B/C execution PASS;
- I05 PASS;
- measured P2X;
- weight-estimand authority;
- native-ID identity authority;
- semantic reason for v308 code 3;
- source certification beyond accepted Authority71/72 evidence.

## Terminal

`CLOSED35_R3_EVS1981_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
