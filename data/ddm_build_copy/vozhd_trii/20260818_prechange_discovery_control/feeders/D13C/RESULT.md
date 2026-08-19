# D13C — CURRENT V550/V550J SHARED-SUBSTRATE STATIC LOSS COURT

**Status:** `NON_DISPOSITIVE_D13_FEEDER`  
**Repository:** `maidiu/rawlsing`  
**Exact base SHA:** `b92d3f3db9faaa962f59d55e61122701df9e53aa`  
**Branch:** `agent/vozhd-trii-d13c-shared-substrate-static-loss`  
**Production code modified:** `NO`  
**Architecture selected:** `NO`  
**Final retention ruling:** `NO`

## 1. Finite feeder disposition

`REPLAY_SAFETY_NOT_PROVEN_BY_CURRENT_SHARED_SUBSTRATE_STATIC_CONTRACT`

The current `v550-v550j-coexecution-v1` shared respondent substrate is a real, operational respondent-row transport and integrity surface. D06 already established that much. Static inspection nevertheless proves that operational existence, a rich prepared schema, a logical-content hash, and a serialized Parquet SHA do **not** establish exact replay sufficiency under D08's empirical-fact identity law.

The strongest positive result is bounded: the contract preserves and hashes a fixed 67-column scalar-row projection containing respondent identity, variable/question fields, raw/normalized response fields, typed DK/refusal/IAP flags, weight value/status, many prepared semantic/status fields, and BASE/JOIN selection metadata. Within that projection, row multiplicity affects the logical hash and physical row order does not.

The strongest negative result is also bounded: the contract does not itself represent exact repeated-event identity, multiselect component identity, response rank/position, governed predicate identity, branch/cohort identity, or explicit denominator/risk-set identity. It additionally allows many missing prepared semantic columns to be synthesized with defaults before validation. Those defaults establish a complete *shape*, not source-equivalent semantic preparation.

Therefore this feeder does not select a replacement substrate and does not decide what must ultimately be retained. It hands D13 a set of proven static boundaries and typed empirical unknowns.

## 2. Governing evidence inspected

Primary executable evidence:

- `data/ddm_build_copy/ddm_v550_shared_respondent_substrate.py` at the exact base SHA.

Binding parent evidence:

- `13_D06_R2_RETURN_ADJUDICATION.md`: accepts shared base+joint extraction, `BASE_ONLY` / `JOINT_ONLY` / `BASE_AND_JOINT` roles, respondent-grain prepared transport, logical and serialized integrity, and direct V550J prepared-required consumption; explicitly leaves unary/pair/arbitrary-joint replay, repeated/multiselect preservation, and joint-only semantic preparation parity unproved.
- `14_D07_D08_D10_D11_RETURN_ADJUDICATION.md`: accepts D08's respondent-incidence algebra and makes response topology, predicate identity/provenance, denominator/risk-set semantics, routing/applicability/missingness, weighting basis, branch/cohort provenance where relevant, and replay/admissibility provenance part of empirical fact identity.

Negative-search boundary:

- the available connector repository code index did not provide a reliable repository-wide symbol search for every external producer/consumer/test call site;
- no claim below promotes that tooling limitation into `ABSENT`;
- where a specific external call site or test could not be established, the prose status is `NOT_LOCATED`.

## 3. Contract anatomy

### 3.1 Fixed logical projection

`PREPARED_SUBSTRATE_REQUIRED_COLUMNS` plus the five shared additive fields form `SHARED_SUBSTRATE_REQUIRED_COLUMNS`; `LOGICAL_CONTENT_COLUMNS` is exactly that required list.

The required logical projection contains 67 columns. Its major identity/semantic families are:

- run/scope: `run_id`, `source`, `source_id`, `wave`, `canonical_wave`, `country_code`;
- respondent: `respondent_id`, `respondent_id_norm`;
- weighting: `weight_value`, `weight_status`;
- question/variable: `var_code`, `var_code_norm`, `question_id`, `question_text`;
- response: raw/normalized values and labels, direction/polarity;
- typed missingness: `is_missing`, `is_dk`, `is_refusal`, `is_iap`, `is_valid_substantive_response`;
- prepared semantic/status/authority fields;
- target-resolution and source-structure fields;
- association/cloud eligibility fields;
- normalized scope fields;
- shared selection fields: `shard_id`, `selection_role`, `base_fixture_selected`, `joint_configuration_selected`, `joint_configuration_ids_json`.

`canonicalize_shared_respondent_substrate()` returns the required columns first **plus any other incoming columns**. Those extra columns can therefore remain physically present in the Parquet while being outside `LOGICAL_CONTENT_COLUMNS`.

### 3.2 Logical hash

`logical_shared_substrate_hash()` reindexes to `LOGICAL_CONTENT_COLUMNS`, hashes each projected row, sorts the row hashes, and hashes the sorted multiset together with schema/execution-contract versions.

Consequences:

1. physical row order is intentionally erased;
2. duplicate row multiplicity remains visible to the logical hash because repeated row hashes remain repeated in the sorted list;
3. any physical extra column is outside logical-content hash authority;
4. `_clean()` is used on every projected logical value before row hashing, so whitespace-only differences and the lexical strings `nan`, `none`, and `null` collapse to the same empty logical token.

That final point gives a direct logical-hash collision construction: two physically different substrates can differ in a required string field only by a literal token that `_clean()` collapses to empty and still receive the same logical hash. Whether any populated governed source lawfully uses such a literal as meaningful content is an empirical/source-semantic question, but the hash itself cannot distinguish it.

### 3.3 Serialized integrity is separate

The writer records `parquet_file_sha256` over the serialized Parquet bytes and `schema_hash` over the schema file. `load_shared_respondent_substrate()` rechecks the Parquet SHA and then recomputes logical validation after reading the Parquet.

Thus byte integrity and logical identity are deliberately different statements:

- equal logical hashes do not require equal Parquet bytes;
- a valid Parquet SHA proves the loaded bytes equal the bytes named by that manifest, not that the logical projection is a complete empirical identity;
- extra physical columns can change the Parquet SHA while leaving the logical hash unchanged.

## 4. Proven static loss / under-specification boundaries

### 4.1 Prepared defaults are not source-equivalent preparation

Before validation, canonicalization creates missing semantic columns with defaults including, among others:

- `weight_value = 1.0`;
- `is_missing/is_dk/is_refusal/is_iap = False`;
- `is_valid_substantive_response = False`;
- response semantic and directionality statuses `unknown` with authority `none`;
- unresolved target state;
- `source_structure_fields_joined = False`;
- `is_substantive = False`;
- `allowed_as_association_feature = False`;
- `allowed_as_attitude_cloud_feature = False`;
- `association_lane = unknown_association_lane`.

The validator verifies required-column presence, selected nonblank scalar keys, source/canonical-wave/country scope, duplicate scalar keys, and logical hash consistency. It does not carry a per-cell provenance bit saying whether a value was observed, authoritatively harmonized, or synthesized by this defaulting step.

Therefore syntactic prepared-contract validity is not proof that missing input semantics were authoritatively recovered. Classification: `DEFAULTABLE_NOT_SOURCE_EQUIVALENT`.

### 4.2 Scalar duplicate policy is topology-hostile unless upstream has already encoded topology losslessly

For substantive rows, `_duplicate_scalar_response_key_count()` defines identity only as:

`(source_norm, canonical_wave_norm, country_code_norm, respondent_id_norm, var_code_norm)`.

If two substantive rows share that tuple, validation fails with `unauthorized_duplicate_scalar_response_keys`.

No event ID, component ID, response position/rank, predicate ID, or branch ID participates in the key because none is part of the required contract. Therefore a lawful repeated response, multiselect component set, or other multi-row topology represented as several substantive rows under one respondent-variable tuple is rejected by this validator. Upstream could instead collapse/encode the topology into one scalar row, but this contract alone does not prove that such an encoding is injective or replay-lossless.

This is a conditional static theorem, not a claim that populated production rows are presently being lost. D05's populated-data block remains inherited.

### 4.3 Exact response topology is not contractually represented

`question_type`, `handling_rule`, source-structure metadata, and response semantics can describe a question or processing class. They are not exact respondent-event/component/rank identity.

The required logical projection has no dedicated:

- response event ID;
- multiselect component/choice occurrence ID;
- ordered/ranked response position;
- repeated measurement/event time or sequence.

Accordingly, exact topology replay is `NOT_REPRESENTED` at the required logical-contract level and `UNKNOWN_WITHOUT_POPULATED_DATA` as to whether upstream scalarization happens to be information-equivalent for any specific source.

### 4.4 Raw versus canonical question identity is incomplete

The contract hashes `var_code`, `var_code_norm`, `question_id`, and `question_text`, but it has no typed `raw_question_id` versus `canonical_question_id` pair.

Requirement resolution can carry `question_implementation_id` in joint-selection working rows, but that field is not a required logical-content column. Because canonicalization retains incoming extras, such an identifier may be physically serialized yet remain outside logical-content hash authority.

Thus the contract does not prove that all raw/source implementation identity distinctions needed for future replay are logical-hash-governed.

### 4.5 Weight value exists; exact weight provenance does not

`weight_value` and `weight_status` are required logical fields, but `weight_value` defaults to `1.0` if missing and no dedicated weight-provenance identifier is required. The manifest carries broader contract/provenance hashes, but the respondent-row contract does not bind each weight value to a source weight variable/transformation/estimator identity.

D08's distinction between raw and governed weighted measure basis is therefore not fully discharged by the static row schema.

### 4.6 Predicate, branch/cohort, and denominator/risk-set identity are not first-class required row identity

The required projection has target and source-structure metadata, but no governed condition-predicate ID, branch ID, cohort membership ID, denominator-rule ID, risk-set ID, or sample-space ID.

For a fixed scalar query, an exact respondent roster plus complete applicability/missingness rows might be information-equivalent to some risk sets. Static schema inspection cannot prove that all necessary respondents—including excluded, IAP, routed-out, and otherwise non-substantive cases—are physically present for every governed query. That is `UNKNOWN_WITHOUT_POPULATED_DATA`.

For branch-conditioned and arbitrary future conjunction replay, respondent IDs alone do not encode which branch/predicate semantics generated membership. D08 explicitly makes that provenance part of fact identity.

### 4.7 JOINT_ONLY extraction role does not prove semantic-preparation parity

Requirement resolution can add joint-required variables beyond base membership and marks union rows as `BASE_ONLY`, `JOINT_ONLY`, or `BASE_AND_JOINT`. This is positive extraction/selection authority.

But selection role is not a proof that every `JOINT_ONLY` variable traversed the same authoritative semantic preparation as a base variable. The canonicalizer's docstring says it returns a V550J-compatible substrate “without reharmonizing rows,” and default synthesis can complete missing prepared fields. Parent D06 therefore correctly leaves joint-only semantic preparation parity `NOT_DEMONSTRATED`.

## 5. Hostile questions answered

### Can semantically different substrates receive the same logical hash?

**Yes, as a static construction.** Any difference confined to extra physical columns is invisible to the logical hash. In addition, `_clean()` collapses certain distinct lexical representations (`null`/`none`/`nan` tokens, null-like values, surrounding whitespace) to the same hash token. Whether a particular collision corresponds to two *lawfully distinct populated empirical facts* remains source/data dependent.

### Can missing semantic columns be defaulted into contract-shaped rows?

**Yes.** Canonicalization supplies defaults before validation. The resulting value is not tagged as “synthesized here rather than source/harmonization derived.”

### Can repeated/multiselect topology be rejected as duplicate scalar responses?

**Yes, conditionally.** Multiple substantive rows sharing the five-field normalized scalar key are rejected. The contract has no event/component/rank dimension in that key. Actual populated loss remains unproved without data/upstream topology evidence.

### Does `JOINT_ONLY` prove equally strong semantic preparation?

**No.** Extraction/selection authority is proven; source-semantic preparation parity is not.

### Are typed routing/missingness distinctions represented?

**Partly and positively.** `is_missing`, `is_dk`, `is_refusal`, `is_iap`, validity/substantive fields, handling/source-structure metadata are logical columns. Their completeness and authoritative derivation across populated sources remain unproved.

### Are all distinctions required by D08 empirical fact identity hashed?

**No.** Several D08 axes are represented (scope, respondent, question/response, typed missingness, weight value/status, authority/status fields), but exact response topology, governed predicate identity/provenance, branch/cohort identity, and explicit denominator/risk-set/sample-space identity are not first-class required logical columns.

### Can branch/cohort facts be reconstructed exactly from this contract alone?

**Not generally proven.** There is no required branch/predicate/cohort identity. Reconstructibility may exist for a particular branch if all generating coordinates are independently retained and governed, but that is outside what this v1 contract guarantees.

### Does this contract prove future arbitrary-conjunction replay?

**No.** It preserves bounded selected scalar respondent-variable rows. Future coordinates outside that selected union may not have been extracted, and any incoming extra columns are outside logical-content hash authority.

### Are respondent IDs enough for cotravel?

**They are a necessary and powerful generator for cotravel over rows actually retained**, and D08 accepts respondent incidence as the common generator. They are not by themselves proof of complete risk sets, exact response topology, predicate/branch provenance, or future-variable coverage.

### Does Parquet byte integrity prove semantic identity?

**No.** It proves byte identity to the recorded serialized artifact. Semantic identity is bounded by the logical projection and its canonicalization rules.

## 6. Mandatory-dimension disposition

All 29 commanded dimensions are individually classified in `SHARED_SUBSTRATE_INFORMATION_MATRIX.csv`. No dimension is silently promoted from static schema presence to populated completeness.

Key groups:

- contract-guaranteed: required projection, logical hash mechanics, byte SHA mechanism, row-order normalization, scalar duplicate-key policy, selection roles;
- physically/logically represented but empirically unproved: respondent incidence for retained rows, typed missingness/routing semantics, raw+normalized response values;
- defaultable rather than source-equivalent: weight and large prepared semantic surface;
- not represented as first-class required identity: exact multiselect/repeated/rank topology, governed predicate/branch/cohort identity, dedicated weight provenance, explicit risk-set/denominator identity;
- parity unknown: joint-only semantic preparation and complete V550/V550J source-equivalence.

## 7. Empirical and search limits

D05's inherited state remains binding: populated counts, completeness, overlap, prevalence, and source-equivalence are `UNKNOWN_WITHOUT_POPULATED_DATA` here.

The following are not asserted absent:

- any external producer-side richer topology encoding;
- any external V550J call site beyond the D06-accepted direct prepared-required path;
- any test outside the inspected/locatable surface that exercises special topologies;
- any extra physical columns carried in a particular materialized Parquet.

Where those could not be established with the available repository search surface, this feeder uses `NOT_LOCATED` in prose rather than converting search failure into an absence claim.

## 8. D13 handoff

D13 may rely on the following finite static facts without adopting an architecture:

1. the v1 logical hash is authoritative only over its fixed required projection;
2. extra physical columns can survive serialization without becoming logical-hash authority;
3. prepared default synthesis is not evidence of source-equivalent semantic preparation;
4. substantive duplicate validation assumes at most one scalar substantive row per source/canonical-wave/country/respondent/variable key;
5. exact event/component/rank/predicate/branch/risk-set identities are not all first-class required logical dimensions;
6. respondent incidence is useful but its populated completeness and exact risk-set sufficiency remain empirical unknowns;
7. Parquet SHA integrity and logical-content identity must not be conflated;
8. D06's operational shared-substrate proof therefore does not close D13 replay sufficiency.

`NO_FINAL_RETENTION_RULING__NO_ARCHITECTURE_SELECTION__NO_PRODUCTION_CHANGE`
