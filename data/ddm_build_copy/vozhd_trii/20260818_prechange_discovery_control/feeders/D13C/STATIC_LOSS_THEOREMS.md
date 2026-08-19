# D13C — STATIC LOSS THEOREMS

**Court:** `D13C`  
**Status:** `NON_DISPOSITIVE_D13_FEEDER`  
**Base SHA:** `b92d3f3db9faaa962f59d55e61122701df9e53aa`

These are static information-boundary theorems about the current V550/V550J shared respondent-substrate contract. They are not a storage design, final retention ruling, or claim about populated prevalence/completeness.

## T1 — Fixed-projection logical-hash theorem

**Claim.** The shared substrate's logical content hash is authoritative only over `LOGICAL_CONTENT_COLUMNS`, which is exactly the fixed 67-column `SHARED_SUBSTRATE_REQUIRED_COLUMNS` projection.

**Proof.** `logical_shared_substrate_hash(frame)` first performs `frame.reindex(columns=LOGICAL_CONTENT_COLUMNS)` and hashes only that projection. `canonicalize_shared_respondent_substrate()` instead returns the required columns followed by any other columns already present in the input frame. Therefore an extra column may survive physically while never entering the logical hash.

**Collision construction.** Let frames A and B agree on all required columns but differ on one extra column `x`. Their per-row logical projection is identical, hence their logical content hash is identical, while their Parquet serialization can differ.

**Classification.** `PHYSICALLY_PRESENT_BUT_NOT_LOGICAL_HASH_AUTHORITY`.

**Limit.** This proves hash undercoverage for extras, not that every possible extra is semantically required.

---

## T2 — Null-like lexical collapse theorem

**Claim.** The logical hash can equate physically distinct values inside the required projection.

**Proof.** Every projected row value is passed through `_clean()` before row hashing. `_clean()` strips whitespace and maps null-like values and case-insensitive lexical strings `nan`, `none`, and `null` to the empty string.

**Collision construction.** Two otherwise identical projected rows with a string field equal to `"null"` in A and `""` in B produce the same cleaned token for that field and therefore the same row hash.

**Classification.** `GUARANTEED_BY_CONTRACT` as a hash-canonicalization property; semantic distinguishability of a populated lexical token is `UNKNOWN_WITHOUT_POPULATED_DATA`.

**Limit.** The theorem does not claim a governed source currently assigns substantive meaning to those lexical tokens. It proves only that the hash cannot distinguish them if it does.

---

## T3 — Physical row-order erasure theorem

**Claim.** Physical row order cannot affect the logical content hash.

**Proof.** Per-row logical hashes are sorted before the outer hash is computed.

**Classification.** `GUARANTEED_BY_CONTRACT`.

**Limit.** Row-order erasure is harmless for unordered scalar incidence. It becomes lossy only if semantic order exists and is not independently represented. The current required projection has no dedicated response rank/position field, so ordered/ranked response topology is not rescued by a first-class logical identity dimension.

---

## T4 — Duplicate multiplicity versus scalar-key rejection theorem

**Claim.** Logical hashing preserves row multiplicity, but validation rejects a broad class of substantive multiplicities before a substrate can be validly materialized.

**Proof.** The sorted row-hash list retains repeated hashes, so multiplicity changes the logical hash. Separately, `_duplicate_scalar_response_key_count()` filters to `is_substantive` rows and marks duplicates over exactly:

`source_norm, canonical_wave_norm, country_code_norm, respondent_id_norm, var_code_norm`.

With `fail_on_duplicate_scalar_keys=True`, any such duplicates produce `unauthorized_duplicate_scalar_response_keys` and fail validation.

**Classification.** multiplicity hashing `GUARANTEED_BY_CONTRACT`; duplicate substantive scalar topology `REJECTED_BY_VALIDATOR`.

**Limit.** Non-substantive duplicates are not governed by this duplicate rule. A multi-event source can also avoid rejection by upstream scalarization, but injective/lossless scalarization is not demonstrated by this contract.

---

## T5 — Repeated/multiselect topology boundary theorem

**Claim.** The v1 required logical contract cannot directly represent multiple substantive response events/components for the same source/canonical-wave/country/respondent/variable tuple as independently identified rows.

**Proof.** No response-event ID, component occurrence ID, event sequence/time, or response rank/position occurs in the required logical projection. Multiple substantive rows for the same five-field scalar tuple are rejected by T4.

**Classification.** `NOT_REPRESENTED` for first-class event/component/rank identity; `REJECTED_BY_VALIDATOR` for the direct multirow scalar representation.

**Limit.** The theorem is conditional about *representation*. It does not prove actual empirical loss in populated production data because upstream may encode a topology into one scalar row. Whether any such encoding is information-equivalent is `UNKNOWN_WITHOUT_POPULATED_DATA` plus source-specific implementation evidence.

---

## T6 — Default synthesis non-equivalence theorem

**Claim.** A row can satisfy the required prepared shape after semantic fields were synthesized by canonicalization rather than supplied by authoritative upstream preparation.

**Proof.** `canonicalize_shared_respondent_substrate()` adds absent columns from a defaults map before validation. Defaults include unit weight, false missingness/status booleans, unknown/none semantic authority states, unresolved target state, false association/cloud permissions, and other prepared fields. Validation checks the resulting columns and selected invariants; it does not store a per-cell bit distinguishing original, harmonized, and default-synthesized values.

**Classification.** `DEFAULTABLE_NOT_SOURCE_EQUIVALENT`.

**Limit.** A conservative default may be operationally intentional. The theorem says only that the resulting value is not static proof of source-equivalent semantic derivation.

---

## T7 — Unit-weight provenance theorem

**Claim.** Presence of a required hashed weight does not establish authoritative weight provenance.

**Proof.** `weight_value` and `weight_status` are required logical columns, but missing `weight_value` is defaulted to `1.0`. No dedicated respondent-row field binds that value to a source weight variable, transform, estimator, or weighting authority identity.

**Classification.** `DEFAULTABLE_NOT_SOURCE_EQUIVALENT` for the weight value; dedicated provenance `NOT_REPRESENTED`.

**Limit.** Broader manifest contract hashes may provide run-level provenance. They are not an exact per-row weight derivation identity.

---

## T8 — Prepared JOINT_ONLY parity theorem

**Claim.** `JOINT_ONLY` selection authority does not imply semantic-preparation parity with base-selected variables.

**Proof.** Requirement resolution can introduce registry-required joint variables beyond base QSM membership and selection roles distinguish `BASE_ONLY`, `JOINT_ONLY`, and `BASE_AND_JOINT`. The canonicalizer explicitly returns a V550J-compatible substrate “without reharmonizing rows” and can synthesize missing semantic columns by defaults. No validator comparison proves that a joint-only row traversed the same authoritative preparation lineage as a base row.

**Classification.** `SEMANTIC_PARITY_NOT_DEMONSTRATED`.

**Limit.** D06 positively proves joint extraction and direct prepared-required V550J consumption. This theorem does not negate that operational path.

---

## T9 — Question-implementation identity under-hash theorem

**Claim.** The contract does not make all possible source/raw versus canonical question identities first-class logical-hash identity.

**Proof.** The required projection includes `var_code`, `var_code_norm`, `question_id`, and `question_text`, but no typed `raw_question_id`/`canonical_question_id` pair. During joint requirement resolution, `question_implementation_id` can be carried in working rows, yet it is not a required logical-content column. If it survives as an incoming extra, T1 applies.

**Classification.** `SEMANTIC_PARITY_NOT_DEMONSTRATED`; a surviving implementation ID is `PHYSICALLY_PRESENT_BUT_NOT_LOGICAL_HASH_AUTHORITY`.

**Limit.** A given source may define `question_id` or `var_code` as sufficient canonical identity. That source-level equivalence is not proven by this generic contract.

---

## T10 — D08 identity undercoverage theorem

**Claim.** The v1 row contract does not itself encode every identity axis D08 requires for exact governed empirical-fact replay.

**Proof.** D08 makes response topology, condition predicate identity/provenance, denominator/risk-set semantics, branch/cohort provenance where relevant, and replay/admissibility provenance part of empirical fact identity. The shared required projection carries substantial scope, respondent, question/response, typed missingness, weight/status, target and authority metadata, but lacks first-class event/component/rank identity, governed predicate ID, branch/cohort ID, and explicit denominator/risk-set/sample-space ID.

**Classification.** `SEMANTIC_PARITY_NOT_DEMONSTRATED` for full D08 identity; missing first-class axes `NOT_REPRESENTED`.

**Limit.** D08 permits respondent incidence or an information-equivalent exact contingency as a generator. Some missing explicit IDs could be reconstructible from complete retained rows plus independent governed predicates. The current static contract does not prove that completeness or those independent bindings.

---

## T11 — Respondent-incidence sufficiency boundary theorem

**Claim.** Required respondent identity is sufficient to support exact cotravel only over the incidence actually and completely retained; it is not by itself a proof of arbitrary-query replay.

**Proof.** `respondent_id` and `respondent_id_norm` are required logical columns and substantive normalized IDs must be nonblank. Hence exact co-membership can be recomputed for retained scalar rows. But validator row counts and IDs are not compared with a source-universe denominator, routed-out universe, or future unselected coordinate set.

**Classification.** retained-row identity `GUARANTEED_BY_CONTRACT`; source/risk-set completeness `UNKNOWN_WITHOUT_POPULATED_DATA`.

**Limit.** This theorem deliberately preserves D08's positive respondent-incidence insight. It rejects only the stronger inference that presence of respondent IDs proves complete incidence for all future lawful predicates.

---

## T12 — Parquet SHA is not semantic-identity theorem

**Claim.** Passing serialized Parquet integrity does not prove replay-safe semantic identity.

**Proof.** The writer separately records `parquet_file_sha256` over the physical Parquet and `content_hash` over the logical projection. The loader rechecks the Parquet SHA and then logical validation. By T1, two artifacts can differ in extra physical columns yet share the logical hash; conversely their Parquet SHAs will normally differ. Thus the two hashes answer different questions.

**Classification.** `GUARANTEED_BY_CONTRACT` as an integrity separation.

**Limit.** The Parquet SHA is valuable and correctly detects byte changes. The theorem rejects only the inference `byte integrity => semantic completeness`.

---

## T13 — Future-coordinate closure theorem

**Claim.** The current shared substrate does not statically prove replay over every future-authorized empirical coordinate.

**Proof.** Requirement resolution materializes the union of the current base variable set and bounded registry-authorized joint-required variables. The hash authority is fixed to the current required schema. A future coordinate not selected into that union is not guaranteed extracted; an incidental extra coordinate that happens to ride along is outside logical hash authority unless it maps into required fields.

**Classification.** `SEMANTIC_PARITY_NOT_DEMONSTRATED`.

**Limit.** D07 requires reconstructibility for separately authorized future directions, subject to D13 physical proof. This theorem does not determine what future retention mechanism should satisfy that law.

---

## T14 — Branch/predicate provenance theorem

**Claim.** Exact historical branch/cohort replay is not established by the shared scalar-row contract alone.

**Proof.** D08 requires exact branch predicate/membership semantics and provenance for branch-conditioned facts. The v1 required projection has target-resolution and source-structure metadata but no required branch ID, cohort ID, or governed condition-predicate identity. Therefore branch labels or later reconstructed groupings cannot be presumed identical to the historical governed branch without an independent binding proof.

**Classification.** `NOT_REPRESENTED` for first-class branch/predicate identity; reconstruction parity `SEMANTIC_PARITY_NOT_DEMONSTRATED`.

**Limit.** If every generating coordinate and predicate authority exists elsewhere and is exactly replayable, branch membership may be derivable. This court neither proves nor rules out that separate path.

---

## T15 — Direct consumption does not upgrade source semantics theorem

**Claim.** Direct V550J prepared-required consumption of a validated shared substrate proves operational contract compatibility, not source-semantic completeness.

**Proof.** D06 binding law establishes direct prepared-required/no-database V550J consumption. The helper's loader enforces artifact existence, Parquet SHA integrity, current logical validation, and stored pass state. By T6, however, a logically valid prepared shape may contain default-synthesized semantic values; by T8 joint-only source-preparation parity is not demonstrated; by T10 several D08 identity axes remain outside the first-class contract.

**Classification.** direct consumption `GUARANTEED_BY_CONTRACT`; source-semantic parity `SEMANTIC_PARITY_NOT_DEMONSTRATED`.

**Limit.** This is not an allegation that V550J currently computes from corrupt rows. It identifies the proof boundary of the contract that V550J is accepted to consume.

---

## Court boundary

These theorems establish static information and proof limits only.

They do **not** establish:

- actual populated loss rate;
- actual prevalence of repeated/multiselect structures;
- final required physical substrate;
- a replacement architecture;
- permission to delete current artifacts;
- permission to modify production code.

`NO_FINAL_RETENTION_RULING__NO_ARCHITECTURE_SELECTION__NO_PRODUCTION_CHANGE`
