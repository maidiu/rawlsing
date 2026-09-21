# CLOSED35-R3-EVS1990 — Realization Contract

Schema: `CLOSED35_R3_EVS1990_SOURCE_REALIZATION@1.0.0`

## 1. Court object

This contract defines the one lawful EVS 1990 source-specific realization shared by Candidates A, B, and C.

Candidate-neutral semantic owner:

`EVS1990_SEMANTIC_OWNER_V1`

Downstream semantic surface:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

Physical implementations may later differ only if separately qualified. Source identity, replay law, q745 retention, ranked topology, coordinate scope, weight nonauthority, bounded UNKNOWNs, and semantic ownership may not differ by candidate.

## 2. Canonical source identity

- canonical filename: `EVS 1990.sav`
- canonical SHA-256: `66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec`
- format: `SAV`
- authority class: `L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`
- accepted decoder condition: `SAV_SOURCE_DECLARED_WINDOWS1252`
- source-native encoding declaration: `windows-1252`
- machine character code: `1252`
- inherited source geometry: 38,213 rows × 390 variables

Hard replay identity:

`SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

`id_cocas` and `caseno` survive as source attributes only. Their injectivity and intended identity scope remain unresolved.

## 3. q745 all-user-missing law

Accepted source fixture:

- variable: `q745`
- source ordinal: 389
- rows seen: 38,213
- ordinary present count: 0
- system missing count: 0
- user-missing count: 38,213
- observed source code: `-5` on all rows
- declared user-missing range: `-5..-1`

Required realization fields remain distinct:

1. `variable_identity = q745`
2. `source_ordinal = 389`
3. `raw_storage_value = -5` for the accepted all-row fixture
4. `source_missing_declaration = -5..-1`
5. `physical_missing_class = USER_MISSING`
6. `source_cell_presence = PRESENT`

No semantic reason is inferred from the numeric code by this realization.

Forbidden transformations:

- delete the variable because all cells are user-missing;
- represent q745 as a nonexistent source column;
- collapse the source `-5` physical witness to an untyped null;
- use q745's lack of ordinary responses to infer routing or applicability;
- import q745 semantics from another EVS release.

## 4. Ranked topology

Accepted ordered source topology:

| ordinal | variable | role |
|---:|---|---|
| 271 | `q530a` | ranked triplet 1, first slot |
| 272 | `f530a` | ranked triplet 1, source flag |
| 273 | `q531b` | ranked triplet 1, second slot |
| 274 | `q532a` | ranked triplet 2, first slot |
| 275 | `f532a` | ranked triplet 2, source flag |
| 276 | `q533b` | ranked triplet 2, second slot |

The two triplets remain distinct and ordered. Flattening, set conversion, flag deletion, slot reordering, or cross-wave substitution is forbidden.

## 5. Release-specific coordinate law

EVS 1990 preserves its release-local study/year/country carriers and the split-up coordinate companions accepted for the 1990–2008 release family.

At minimum, the governed release-specific coordinate namespace retains the base EVS coordinate carriers plus:

- `country1`
- `c_abrv1`
- `cntry1_y`

The split-up carriers remain separate from their unsplit counterparts.

No rule in this realization authorizes:

- aliasing `country` and `country1`;
- aliasing `c_abrv` and `c_abrv1`;
- harmonizing codes to another EVS wave;
- importing 2017 ISO-labelled coordinate semantics;
- inferring cross-release equivalence from vector or label similarity.

Cross-release equivalence remains:

`BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`

## 6. Distinct weight-carrier law

Accepted physical topology:

- ordinal 11: `weight_g`
- ordinal 12: `weight_s`

Both carriers must survive independently.

The realization forbids:

- collapsing `weight_g` and `weight_s`;
- selecting either as a default primary weight;
- inferring a default estimand or population domain;
- inferring normalization or variance-design semantics;
- reconstructing a weight from the other;
- substituting weight=1 when authority is absent.

Governed unresolved states:

- `BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`
- `BOUNDED_UNKNOWN__WEIGHT_S_ESTIMAND`
- `BOUNDED_UNKNOWN__WEIGHT_G_WEIGHT_S_RELATION_AND_DEFAULT_USE`

## 7. Native-ID law

Accepted source-local ID candidates include:

- `id_cocas`
- `caseno`

They remain source attributes.

Unresolved:

- injectivity;
- intended identity scope;
- cross-country stability;
- cross-wave stability.

State:

`BOUNDED_UNKNOWN__NATIVE_ID_SCOPE`

No candidate may replace source SHA + row ordinal with either native ID.

## 8. Windows-1252 reader/config boundary

The exact source declares Windows-1252. No EVS 1999/2008 latin1 compatibility exception is inherited backward.

Reader/configuration is physical execution metadata only.

Readable source text does not create additional semantic authority, and no automatic encoding fallback is authorized as source meaning.

A later physical qualification must pin exact reader/decoder/version/config to the source SHA.

## 9. Candidate neutrality

A/B/C must share:

- `EVS1990_SEMANTIC_OWNER_V1`;
- canonical source SHA;
- replay identity law;
- q745 retention law;
- ranked triplet topology;
- release-specific coordinate law;
- distinct weight-carrier law;
- bounded UNKNOWN set;
- exact S35 edge set;
- R35 hooks.

Any candidate-specific semantic divergence fails closed.

## 10. S35 physical edge scope

Exact edge set:

`EC01; EC02; EC05; EC06; EC09; EC12; EC13`

Meanings:

- EC01 — format family
- EC02 — explicit text decoding mode
- EC05 — physical missingness multiclass
- EC06 — all-missing column retention
- EC09 — ordered repeated/ranked topology
- EC12 — weight/design multiplicity and domain
- EC13 — source-local coordinate carriers

## 11. R35 binding

### I01

Schema:

`PRE553_PHYSICAL_METADATA@1.0.0`

Semantic authority: false.

### I02

Schemas:

- `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`
- `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`

Required for any non-direct-raw or persisted derivative.

A derivative asserting the canonical SHA internally is not sufficient parentage proof.

Semantic authority: false.

### I03

Schemas:

- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`

Required source-local dimensions include:

- physical metadata;
- variable inventory/order;
- raw storage values;
- typed missingness;
- source missing declarations;
- all-column presence including q745;
- row replay identity;
- reader/configuration digest;
- ranked-slot topology;
- weight/design carriers;
- source-local coordinate carriers.

A later PASS means only:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

## 12. Bounded UNKNOWN set

- `BOUNDED_UNKNOWN__NATIVE_ID_SCOPE`
- `BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`
- `BOUNDED_UNKNOWN__WEIGHT_S_ESTIMAND`
- `BOUNDED_UNKNOWN__WEIGHT_G_WEIGHT_S_RELATION_AND_DEFAULT_USE`
- `BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`

These are valid governed terminal states at this grain.

## 13. Implementation boundary

Implemented declaratively:

- exact-source realization contract;
- q745 retention;
- ranked topology;
- coordinate nonharmonization;
- distinct weight carriers and weight nonauthority;
- replay identity;
- candidate neutrality;
- S35/R35 bindings;
- source-independent rejection protocol.

Not performed:

- raw SAV open;
- real-source decoding or source processing;
- Authority71 fixture remeasurement;
- A/B/C execution;
- whole-source physical-equivalence PASS;
- I05;
- measured P2X.

Test execution status:

`TESTS_AUTHORED__NOT_EXECUTED`
