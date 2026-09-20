# CLOSED35-R2-AFR1 — Realization Contract

Schema: `CLOSED35_R2_AFR1_SOURCE_REALIZATION@1.0.0`

Semantic owner: `AFROBAROMETER_R1_SEMANTIC_OWNER_V1`

## 1. Court object

This contract defines the single lawful source-specific semantic owner for future Candidate A/B/C processing of:

- source file: `Afro Barometer Round 1.sav`;
- canonical SHA-256: `6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2`;
- Authority72 launch class: `L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`.

Candidate implementations may differ in reader strategy, traversal, materialization, caching, indexing, or other physical mechanics.

They may not differ in source identity, replay identity, identity-carrier semantics, source-local coordinate authority, SUPDEM interpretation boundary, weight-carrier authority, national-instrument uncertainty law, or typed-UNKNOWN behavior.

The governing relation is:

```text
exact canonical AFR1 source root
+ accepted S35/R35 physical law
+ accepted Authority71/72 AFR1 documentary authority
-> AFROBAROMETER_R1_SEMANTIC_OWNER_V1
-> one candidate-neutral semantic surface for A/B/C
```

## 2. Canonical source identity

Canonical filename:

`Afro Barometer Round 1.sav`

Canonical SHA-256:

`6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2`

Format:

`SAV`

Accepted source reader mode:

`SAV_NATIVE_GOVERNED`

Source-specific compatibility override:

`NO_SOURCE_SPECIFIC_COMPATIBILITY_OVERRIDE`

Hard replay identity:

`SOURCE_SHA256 + ZERO_BASED_PHYSICAL_ROW_ORDINAL`

No source-native respondent or case field supersedes that replay key.

A same-wave export, alternate merge, reconstructed table, or derivative cannot replace the canonical root without the generic R35 lineage and physical-equivalence court.

## 3. L1 bounded-unknown law

Authority72 admits this source as:

`L1_EXECUTION_PACKET_READY__BOUNDED_UNKNOWNS_ALLOWED`

Exactly two source-level documentary gaps are inherited from the accepted R01 packet:

1. exact SAV `CASENUMB` versus documentary codebook `RESPNUMB`;
2. national-instrument equivalence beyond each exact documentary statement.

Neither gap is a global realization blocker.

The lawful state is:

`BOUNDED_UNKNOWN`

where the exact requested relation is not proven.

The realization must not transform a bounded unknown into:

- an alias;
- a cross-country person key;
- a cross-round person key;
- a national-question equivalence;
- an inferred routing rule;
- a weight or design rule.

If a downstream workload requires one of those unresolved assertions rather than permitting typed UNKNOWN, it fails closed at that assertion.

## 4. Identity namespace

### 4.1 Hard row identity

Every source row is identified for replay by:

`(canonical_source_sha256, zero_based_physical_row_ordinal)`

This remains the hard replay key even if an apparently unique source-native field is present.

### 4.2 REFNUMB

Accepted documentary authority identifies `REFNUMB` as the unique case-reference number assigned to each case by MSU.

Owner state:

`DOCUMENTED_UNIQUE_CASE_REFERENCE__SOURCE_LOCAL_ATTRIBUTE`

The accepted Authority71 fixture also records physical injectivity for the exact frozen source.

That injectivity is a source fact, not permission to replace the Rawlsing hard replay key.

No cross-round or longitudinal identity follows from `REFNUMB`.

### 4.3 CASENUMB

`CASENUMB` is an exact source carrier and remains separately addressable.

Accepted preparation evidence records:

- noninjectivity of `CASENUMB`;
- collisions remain after composing `COUNTRY + CASENUMB`.

Owner state:

`SOURCE_CARRIER__NONINJECTIVE__NO_DOCUMENTARY_RESPNUMB_ALIAS`

It cannot be used as hard replay identity.

### 4.4 Documentary RESPNUMB

The Round-1 codebook separately documents a `RESPNUMB` concept as unique within country and potentially duplicated across countries.

The accepted source packet did not establish an exact source join:

`CASENUMB == RESPNUMB`

Therefore:

`CASENUMB_TO_RESPNUMB_RELATION = BOUNDED_UNKNOWN`

`RESPNUMB` remains a documentary concept unless an exact future authority joins it to an exact source carrier.

No name similarity, role similarity, frequency pattern, or apparent code-domain resemblance may fill the gap.

## 5. Country coordinate

`COUNTRY` is the exact source-local Round-1 coordinate.

Accepted documentary authority binds an explicit 12-country Round-1 map.

Owner rule:

`COUNTRY_R1 = SOURCE_LOCAL_DOCUMENTED_COORDINATE`

The numeric code system is not portable to R5, R9, or any other release by number or label resemblance.

Country scope may qualify a documentary question variant or applicability rule where the exact source-native codebook says so.

Country scope does not convert any survey ID into a universal respondent key.

## 6. SUPDEM physical/documentary owner

The realization preserves physical state and documentary meaning as separate dimensions.

Accepted Round-1 source-document authority binds:

| raw code | documentary semantic state |
|---:|---|
| 4 | `DONT_KNOW` |
| 97 | `NOT_APPLICABLE` |
| 98 | `REFUSED` |
| 99 | `MISSING_DATA` |

For these states, the physical owner remains:

`ORDINARY_STORED_VALUE`

unless a separately governed physical missing declaration proves otherwise.

The accepted Round-1 preparation packet records no physical user-missing declaration or system-missing cell in this source.

This worker does not re-execute that observation.

Consequences:

- `SUPDEM=99` with documentary meaning `MISSING_DATA` is not physical system missing;
- `SUPDEM=97` does not become a routing rule merely because it is named `NOT_APPLICABLE`;
- `SUPDEM=4/98/99` cannot be converted to generic null by label text;
- country-specific offering/applicability notes attach only at their accepted documentary grain.

The source-native semantic label never overwrites the physical storage class.

## 7. National-instrument heterogeneity

The accepted Round-1 merged codebook documents that the national instruments were not fully standardized.

The merged release may therefore place one source variable over national questions that were identical, similar, or judged conceptually equivalent by the producer.

This realization defines two states:

`PER_VARIABLE_DOCUMENTED_NATIONAL_VARIANT`

when exact documentary authority supplies the country/question relation; and

`BOUNDED_UNKNOWN__NATIONAL_INSTRUMENT_EQUIVALENCE_NOT_PROVEN`

when it does not.

Forbidden inference:

`one merged variable identity -> identical national wording/response semantics`

The source-local owner may consume exact per-variable documentary variants. It may not manufacture a universal harmonization ontology for Round 1.

## 8. Weight owner

The exact Round-1 weight-carrier namespace is:

- `WITHINWT`;
- `ACROSSWT`;
- `COMBINWT`;
- `AFRICAWT`;
- `AFCOMBWT`.

All five carriers remain physically preservable and semantically distinct.

Accepted source-native documentary roles:

### WITHINWT

Source-local role:

`WITHIN_COUNTRY_CORRECTION`

The accepted codebook describes country-specific correction for named in-country over/undersampling or unequal selection conditions.

### ACROSSWT

Source-local role:

`EQUAL_COUNTRY_SAMPLE_WEIGHT`

The accepted codebook describes equalization of country samples for cross-country use.

### COMBINWT

Source-local role:

`WITHIN_X_ACROSS_COMPOSITE`

The accepted codebook documents the combination of within-country and equal-country components.

### AFRICAWT

Source-local role:

`COUNTRY_POPULATION_WEIGHT`

The accepted codebook documents country-population weighting.

### AFCOMBWT

Source-local role:

`WITHIN_X_AFRICA_POPULATION_COMPOSITE`

The accepted codebook documents the combined within-country and Africa-population weighting role.

These roles are R1-specific documentary identities.

They do not themselves choose a later analytical estimand.

The realization therefore sets:

`DEFAULT_WEIGHT = NONE_AUTHORIZED_BY_SOURCE_SPECIFIC_REALIZATION`

A later workload may select a weight only under explicit analytical/estimand authority compatible with the documented source-local role.

Forbidden shortcuts include:

- choose the only non-null weight;
- choose the carrier with the most familiar name;
- choose the carrier with the largest/smallest magnitude;
- import a later-round default;
- normalize or combine carriers beyond the documented R1 identities;
- discard unused candidate weights from the physical source surface.

## 9. Candidate-neutral handoff

Every Candidate A/B/C binding must carry the same:

- canonical source SHA;
- `AFROBAROMETER_R1_SEMANTIC_OWNER_V1`;
- replay identity law;
- REFNUMB/CASENUMB/RESPNUMB separation;
- Round-1 COUNTRY authority;
- SUPDEM physical/documentary split;
- five weight identities and documentary roles;
- national-instrument uncertainty law;
- bounded-UNKNOWN behavior.

Candidate identity is not a semantic input.

For the same canonical physical incidence, A/B/C must not produce different interpretation states.

## 10. Exact S35 edge scope

This source binds exactly the accepted S35 classes:

### EC01 — FORMAT_FAMILY_SAV_DTA

Requires exact canonical source identity and format-neutral physical-incidence preservation.

SAV format has no semantic jurisdiction.

### EC05 — PHYSICAL_MISSINGNESS_MULTICLASS

Requires preservation of the distinction between physical system/user missing states and ordinary stored semantic-looking values.

For R1, SUPDEM special codes are the key source-local negative control.

### EC07 — NATIVE_ID_SCOPE_COLLISION_OR_NONINJECTIVITY

Requires SHA + row ordinal as irreducible replay identity and preservation of native ID carriers without deduplication.

### EC12 — WEIGHT_DESIGN_MULTIPLICITY_AND_DOMAIN

Requires all five R1 weight carriers to survive while source-local roles and later analytical selection remain separate authority layers.

### EC13 — SOURCE_LOCAL_COORDINATE_CARRIERS

Requires preservation of the exact Round-1 COUNTRY coordinate and forbids cross-wave numeric recoding by convenience.

No AFR1-specific physical adapter is authorized or required.

## 11. R35 physical-equivalence hooks

### R35-I01

Required generic physical metadata schema:

`PRE553_PHYSICAL_METADATA@1.0.0`

The physical receipt preserves raw layout declarations, normalized geometry, display metadata, and decoder identity without granting semantic authority.

### R35-I02

Any non-direct realization must close immutable derivative parentage through the accepted generic schemas:

- `FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0`;
- `FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0`.

A derivative asserting the canonical SHA is not ancestry proof.

### R35-I03

Later whole-source A/B/C physical qualification consumes:

- `FIABC_R35_I03_SOURCE_PHYSICAL_SCOPE@1.0.0`;
- `FIABC_R35_I03_CANONICAL_PHYSICAL_EXPECTATION@1.0.0`;
- `FIABC_R35_I03_CANDIDATE_PHYSICAL_REALIZATION@1.0.0`;
- `FIABC_R35_I03_WHOLE_SOURCE_PHYSICAL_EQUIVALENCE_RECEIPT@1.0.0`.

The source scope must include the EC01/05/07/12/13 evidence dimensions.

A later physical PASS can only be:

`PHYSICAL_EQUIVALENCE_PASS__NOT_SEMANTIC_OR_CERTIFICATION_PASS`

This browser realization issues no such receipt.

## 12. Failure law

Wrong canonical root:

`BLOCKED__CANONICAL_SOURCE_ROOT_UNPROVED`

`CASENUMB == RESPNUMB` invented:

`REJECT__UNAUTHORIZED_IDENTITY_ALIAS`

`CASENUMB`, `COUNTRY+CASENUMB`, or any survey ID used as hard replay/cross-country identity:

`REJECT__NATIVE_SURVEY_ID_PROMOTED_TO_REPLAY_OR_PERSON_IDENTITY`

SUPDEM ordinary code converted to physical missing:

`REJECT__DOCUMENTARY_SPECIAL_CODE_COERCED_TO_PHYSICAL_MISSING`

National semantic uniformity inferred from merged variable identity:

`REJECT__UNAUTHORIZED_NATIONAL_INSTRUMENT_EQUIVALENCE`

Country numeric map imported from another round:

`REJECT__CROSS_RELEASE_COORDINATE_IMPORT`

Default/estimand weight chosen without explicit later authority:

`REJECT__UNAUTHORIZED_WEIGHT_SELECTION`

Any of five weight carriers discarded from required physical scope:

`REJECT__SOURCE_WEIGHT_CARRIER_LOSS`

Candidate-specific semantic owner divergence:

`REJECT__CANDIDATE_SEMANTIC_DIVERGENCE`

An unresolved relation requested by a workload that cannot accept typed UNKNOWN:

`BLOCKED__REQUIRED_SOURCE_SEMANTIC_AUTHORITY_MISSING`

## 13. Claim boundary

This contract implements a source-specific semantic realization at browser/GitHub grain.

It does not claim:

- canonical source bytes were opened;
- source processing was executed;
- source decoding was executed;
- the Authority71 physical observations were re-measured;
- A/B/C were executed;
- whole-source physical equivalence passed;
- I05 passed;
- measured P2X occurred;
- the source is certified beyond its accepted documentary authority.

Terminal:

`CLOSED35_R2_AFROBAROMETER_R1_SOURCE_SPECIFIC_REALIZATION_IMPLEMENTED__READY_FOR_ABC_QUALIFICATION`
