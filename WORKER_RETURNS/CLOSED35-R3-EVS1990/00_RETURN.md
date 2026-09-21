# CLOSED35-R3-EVS1990 — EVS 1990 Governed Source-Specific Realization

Repository: `maidiu/rawlsing`

Base: `agent/vozhd-closed35-l2r-r1-fanin-r1@da33eb6a8225c14eee9490633a3263388dc5536c`

Worker branch: `agent/rabochii-closed35-r3-evs1990-realization-r1`

Return: `WORKER_RETURNS/CLOSED35-R3-EVS1990/`

Canonical source: `EVS 1990.sav`

Canonical SHA-256: `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec`

Authority class: `L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

Accepted decoder condition: `SAV_SOURCE_DECLARED_WINDOWS1252`

Candidate-neutral semantic owner: `EVS1990_SEMANTIC_OWNER_V1`

Downstream semantic surface: `PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

## Disposition

`SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__TESTS_AUTHORED_NOT_EXECUTED`

Terminal:

`CLOSED35_R3_EVS1990_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`

This worker is GitHub/browser-only. It did not open the canonical SAV, execute real source processing, remeasure Authority71 fixtures, execute Candidate A/B/C, materialize a whole-source physical-equivalence receipt, run I05, or run measured P2X.

## Governing accepted facts

The accepted Authority71/72 and SR09-PRE EVS packet establishes, at inherited evidence grain:

- 38,213 rows and 390 source variables;
- source-native Windows-1252 declaration with machine character code 1252;
- `q745` at source ordinal 389 is physically present and all 38,213 cells are source user-missing code `-5`;
- `q745` has a user-missing declaration covering `-5..-1`;
- ranked topology consists of two ordered triplets:
  - ordinals 271–273: `q530a | f530a | q531b`;
  - ordinals 274–276: `q532a | f532a | q533b`;
- source-native weight candidates are distinct:
  - ordinal 11: `weight_g`;
  - ordinal 12: `weight_s`;
- source-local coordinates include the ordinary EVS study/year/country carriers plus the 1990 split-up companion family `country1`, `c_abrv1`, and `cntry1_y`;
- `id_cocas` and `caseno` are source attributes, not hard replay identity.

No neighboring EVS release is semantic authority for EVS 1990.

## Realization law

### q745 all-user-missing variable retention

`q745` remains a real source variable even though it contains no ordinary substantive response in the accepted source census.

The realization preserves separately:

1. variable identity and source ordinal;
2. raw stored value;
3. source user-missing declaration;
4. physical missing class;
5. row incidence.

An all-user-missing column is not absent, irrelevant, or disposable. No candidate may drop `q745`, rewrite it as a nonexistent field, or replace the physical `-5` source witness with a generic null.

### Ranked triplet topology

The two ranked triplets remain ordered source topology:

- `q530a -> f530a -> q531b`;
- `q532a -> f532a -> q533b`.

They may not be flattened, reordered, deduplicated, or replaced by ranked structures from another EVS release.

### Release-specific coordinates

The realization preserves EVS 1990's own coordinate family, including the split-up companions documented for the 1990–2008 releases.

No cross-release harmonization, ISO recoding, coordinate aliasing, or import from EVS 1981/1999/2008/2017 is authorized by similar names.

### Distinct weight carriers

`weight_g` and `weight_s` remain distinct physical/documentary carriers.

The realization does not infer:

- a default primary weight;
- equality or aliasing between the two weights;
- a target estimand;
- normalization;
- population domain;
- variance/design role;
- a composition rule.

No fallback to weight=1 is minted as semantic repair.

### Replay identity

Hard replay identity remains:

`SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

Neither `id_cocas` nor `caseno` is promoted to replay identity.

## Bounded UNKNOWN set preserved

- `BOUNDED_UNKNOWN__NATIVE_ID_SCOPE`
- `BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`
- `BOUNDED_UNKNOWN__WEIGHT_S_ESTIMAND`
- `BOUNDED_UNKNOWN__WEIGHT_G_WEIGHT_S_RELATION_AND_DEFAULT_USE`
- `BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`

These are lawful governed states, not blockers. They may not be filled by variable names, numeric values, cross-wave analogy, or convenience.

## S35 physical edge classes bound

Exact accepted matrix scope:

- `EC01` — FORMAT_FAMILY_SAV_DTA
- `EC02` — EXPLICIT_TEXT_DECODING_MODE
- `EC05` — PHYSICAL_MISSINGNESS_MULTICLASS
- `EC06` — ALL_MISSING_COLUMN_RETENTION
- `EC09` — ORDERED_REPEATED_SLOT_TOPOLOGY
- `EC12` — WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN
- `EC13` — SOURCE_LOCAL_COORDINATE_CARRIERS

No EVS1990-specific semantic edge and no EC14 compound membership is invented.

## R35 hooks bound

- I01: `PRE553_PHYSICAL_METADATA@1.0.0`
- I02:
  - `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`
  - `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`
  - `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`
- I03:
  - `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
  - `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
  - `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
  - `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

All R35 hooks have `semantic_authority=false`.

A later I03 PASS remains exactly:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

## Implementation files

No runtime source-processing implementation file is added by this browser-only realization.

The source-specific realization is frozen declaratively in this return packet:

- `00_RETURN.md`
- `01_REALIZATION_CONTRACT.md`
- `02_MISSING_RANK_WEIGHT_MAP.csv`
- `03_PHYSICAL_EDGE_BINDING.json`
- `04_TEST_PROTOCOL.md`
- `RETURN.json`

## Test status

`TESTS_AUTHORED__NOT_EXECUTED`

No test PASS is fabricated.

## Explicit proof boundary

This worker does **not** claim:

- raw SAV opened;
- real-source processing or decoding re-executed;
- whole-source physical-equivalence PASS;
- Candidate A/B/C execution PASS;
- I05 PASS;
- measured P2X;
- native-ID authority;
- weight estimand/default-use authority;
- cross-release coordinate equivalence;
- source certification beyond accepted Authority71/72 evidence.

## Terminal

`CLOSED35_R3_EVS1990_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
