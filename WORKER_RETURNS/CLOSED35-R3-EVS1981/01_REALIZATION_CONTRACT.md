# CLOSED35-R3-EVS1981 — Realization Contract

Schema: `CLOSED35_R3_EVS1981_SOURCE_REALIZATION@1.0.0`

## 1. Court object

This contract defines the one lawful EVS 1981 source-specific realization that Candidates A, B, and C must share.

Physical implementation may differ later if separately qualified. Source identity, replay identity, missing-state law, ranked-slot topology, coordinate scope, weight nonauthority, bounded-UNKNOWN behavior, and downstream semantic ownership may not differ by candidate.

Candidate-neutral semantic owner:

`EVS1981_SEMANTIC_OWNER_V1`

Downstream semantic surface:

`PRE553_SOURCE_BACKED_C11_FACADE@1.0.0`

## 2. Canonical source identity

Canonical filename: `EVS 1981.sav`

Canonical SHA-256:

`5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2`

Format: `SAV`

Authority class:

`L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

Hard replay identity:

`SOURCE_SHA256 + ZERO_BASED_SOURCE_ROW_ORDINAL`

The accepted packet records 19,378 rows and 370 variables. Those figures are inherited Authority71 evidence; this browser worker did not remeasure them.

`id_cocas` and `caseno` are source attributes only. They are not promoted to replay identity because injectivity and intended identity scope remain unresolved.

## 3. Source-declared text/reader condition

Accepted decoder condition:

`SAV_SOURCE_DECLARED_WINDOWS1252`

Accepted source metadata states:

- source-native character encoding: `windows-1252`;
- machine character code: `1252`;
- source-specific compatibility override: none.

This is release-specific physical/configuration authority. EVS 1981 does not inherit the later EVS 1999/2008 UTF-8-declared latin1 compatibility rule.

A later executable qualification must bind the exact reader/decoder/version/config used to the canonical source SHA. This browser realization does not invent a new reader-version pin.

Readable source text does not, by itself, authorize additional questionnaire, routing, weight, or cross-release semantics.

## 4. v308 positive-valued user-missing law

Accepted source metadata for `v308`, source ordinal 141, declares user-missing over:

- numeric range `-5..-1`; and
- discrete numeric value `3`.

The realization preserves four distinct fields of fact:

1. `raw_storage_value` — exact stored value, never erased;
2. `source_missing_declaration` — the SAV declaration covering the value;
3. `physical_missing_class` — whether the stored value is physically ordinary, user-missing, or system-missing;
4. `governed_semantic_state` — semantic classification permitted by accepted authority.

For a stored `3` covered by the v308 declaration:

- `raw_storage_value = 3`;
- `physical_missing_class = USER_MISSING`;
- `governed_semantic_state = SEMANTIC_MISSING__REASON_BOUNDED_UNKNOWN`;
- reason detail = `BOUNDED_UNKNOWN__V308_CODE3_REASON`.

The positive sign of `3` is irrelevant to its physical missing classification. A sign-based missing rule is rejected.

Semantic classification must not replace, null out, rewrite, or otherwise destroy the stored `3`.

The accepted packet proves the declaration. Its recorded observed user-missing counts identify `-1` and `-5` observations, not an observed code-3 incidence. This realization therefore makes no claim about how many rows actually store `3`.

No semantic meaning for any missing code is inferred merely from its numeric value.

## 5. Ranked-slot topology

The accepted source-local ranked structure is:

| source ordinal | variable | governed role |
|---:|---|---|
| 270 | `v460` | ordered first slot |
| 271 | `f460` | interposed source flag |
| 272 | `v461` | ordered second slot |

The exact ordered triplet is preserved as topology.

Forbidden transformations include:

- flattening it into an unordered set;
- dropping `f460`;
- swapping first and second slot identity;
- deduplicating apparently similar values;
- substituting another EVS wave's ranked-variable names or ordinals.

Physical adjacency is preserved as evidence but does not create semantics beyond the accepted ranked-slot relation.

## 6. Release-specific coordinate law

The accepted EVS 1981 coordinate tuple is:

| ordinal | variable | accepted source-local descriptor |
|---:|---|---|
| 0 | `studyno` | GESIS study number (EVS wave) |
| 1 | `studynoc` | GESIS study number (EVS national datasets) |
| 2 | `version` | GESIS archive version |
| 3 | `versionc` | GESIS archive version (EVS national datasets) |
| 6 | `year` | survey year |
| 7 | `country` | country code |
| 8 | `c_abrv` | country abbreviation |
| 10 | `cntry_y` | country_year |

These carriers remain separate source variables.

EVS 1981 does not acquire the later-wave split-up companions `country1`, `c_abrv1`, or `cntry1_y`.

No cross-release code-system equivalence, harmonization, or coordinate alias is inferred from similar names.

Cross-release coordinate equivalence remains:

`BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`

## 7. weight_g law

Accepted source-local weight carrier:

- source ordinal 9;
- variable `weight_g`.

The realization preserves `weight_g` as a physical/documentary carrier.

It does not select `weight_g` as a default analytical weight and does not infer:

- target population;
- estimand;
- normalization;
- variance-design role;
- lawful combination with any other release;
- cross-wave equivalence.

Exact weight use remains:

`BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`

until stronger authority is supplied at the point of statistical use.

## 8. Native-ID law

Accepted source-local ID candidates:

- ordinal 4: `id_cocas`;
- ordinal 5: `caseno`.

They survive as source attributes.

The following remain unresolved:

- injectivity;
- intended identity scope;
- cross-country stability;
- cross-wave stability.

Therefore:

`BOUNDED_UNKNOWN__NATIVE_ID_SCOPE`

and replay remains canonical source SHA + zero-based source-row ordinal.

## 9. Candidate neutrality

A/B/C must consume one shared semantic owner:

`EVS1981_SEMANTIC_OWNER_V1`

Candidate-specific semantics are forbidden.

Every candidate must preserve the same:

- canonical source SHA;
- source-row replay identity;
- Windows-1252 source declaration;
- v308 stored-value / declaration / physical-class / semantic-state separation;
- ranked triplet;
- coordinate tuple;
- weight carrier and weight nonauthority;
- bounded UNKNOWN set;
- S35 edge scope;
- R35 receipt seams.

## 10. Bounded UNKNOWN set

The governed unresolved set is:

- `BOUNDED_UNKNOWN__NATIVE_ID_SCOPE`;
- `BOUNDED_UNKNOWN__V308_CODE3_REASON`;
- `BOUNDED_UNKNOWN__WEIGHT_G_ESTIMAND`;
- `BOUNDED_UNKNOWN__CROSS_RELEASE_COORDINATE_EQUIVALENCE`.

These states are lawful terminal semantic states at this realization grain. They are not blockers and must not be filled by analogy, sign, source-variable name, physical missingness, or another EVS release.

## 11. S35 physical edge scope

Exact accepted edge classes:

- `EC01` — FORMAT_FAMILY_SAV_DTA;
- `EC02` — EXPLICIT_TEXT_DECODING_MODE;
- `EC05` — PHYSICAL_MISSINGNESS_MULTICLASS;
- `EC09` — ORDERED_REPEATED_SLOT_TOPOLOGY;
- `EC12` — WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN;
- `EC13` — SOURCE_LOCAL_COORDINATE_CARRIERS.

No EC14 compound-court membership is invented for EVS 1981.

## 12. R35 binding

### I01 — physical metadata

Schema:

`PRE553_PHYSICAL_METADATA@1.0.0`

Later qualification must preserve generic file/layout/decoder metadata required by the applicable edge classes.

Semantic authority: false.

### I02 — derivative parentage

Schemas:

- `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`.

Required for non-direct-raw or persisted derivative carriers.

A derivative's internal assertion of the canonical SHA is not parentage proof.

Semantic authority: false.

### I03 — whole-source physical equivalence

Schemas:

- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`;
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`;
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`;
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`.

A later PASS state is exactly:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

Browser implementation does not materialize that receipt.

## 13. Implementation boundary

Implemented here:

- exact-source realization contract;
- candidate-neutral semantic owner;
- v308 positive user-missing preservation law;
- ranked-slot topology law;
- release-specific coordinate law;
- weight nonauthority law;
- bounded UNKNOWN law;
- exact S35 edge binding;
- R35 receipt hooks;
- source-independent rejection protocol.

Not performed:

- raw SAV open;
- real-source decoding;
- real-source processing;
- fixture remeasurement;
- A/B/C execution;
- whole-source physical-equivalence PASS;
- I05;
- measured P2X.

Test execution status:

`TESTS_AUTHORED__NOT_EXECUTED`
