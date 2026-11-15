# Optimization and simplification ledger

Ranked by expected value, semantic risk and implementation cost. These are three material opportunities, not a micro-optimization inventory. They overlap the finding ledger and are not extra findings.

## 1. Keep exact provenance compact through seal/rehydration

**current_cost:** 3,108,906 compact manifest/inventory bytes expand to an inferred 47,238,068 canonical document bytes, 192,109 repeated exact-ref occurrences in four arrays and 2,884 default 16,384-character shards. Full text/parse/canonical constructor intermediates recur.

**evidence:** ASTRA-005; [02_CONSTRUCTOR_COMPLETE_MANIFEST.json](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/02_CONSTRUCTOR_COMPLETE_MANIFEST.json); [pre553_repo_native_seal.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/pre553_repo_native_seal.py)

**proposed_change_class:** IDENTITY_PRESERVING_OPTIMIZATION

**expected_value:** VERY_HIGH

**semantic_risk:** LOW

**implementation_cost:** MEDIUM

**identity_effect:** PRESERVING

**authority_effect:** NONE

**recommended_timing:** HIGH_VALUE_AFTER_GT12

**verification_required:** Preserve every canonical query/fact byte, authority/ref/order commitment and current pin; reject hostile transport corruption; benchmark the same actual input for wall time and peak memory. Use streaming or dictionary-backed views without changing semantic projection.

## 2. One tested exact-reference conversion contract at each semantic boundary

**current_cost:** Hand-maintained ref/projection conversions repeat across PRE553, FF, admission, M1, M4 and the active consumer; ASTRA-003 is a concrete recurring defect class rather than a style concern.

**evidence:** ASTRA-003; [pre553_empirical_objects.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_empirical_objects.py); [gt12_d_to_m4_typed_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/gt12_d_to_m4_typed_bridge.py); [gt12_e2b_actual_object_consumer_harness.py](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py)

**proposed_change_class:** SAFE_REFACTOR

**expected_value:** HIGH

**semantic_risk:** LOW

**implementation_cost:** MEDIUM

**identity_effect:** PRESERVING

**authority_effect:** NONE

**recommended_timing:** Fix ASTRA-003 during GT12; consolidate proven mechanical conversions after closure.

**verification_required:** Golden roundtrip tests distinguish ordered refs from canonical sets and PRE553 kind refs from M4 schema refs. Preserve every field/version/hash. Do not unify semantic roles just because their dictionaries look similar.

## 3. Validate immutable evidence once per exact operation scope

**current_cost:** Canonicalization, integrity checks and large closure traversals repeat across constructors and bridges; current nested mutability prevents safely treating a ref as a permanent validation-cache key.

**evidence:** ASTRA-001; ASTRA-002; [pre553_empirical_objects.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/pre553_empirical_objects.py); [gt12_c_to_d_relation_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/gt12_c_to_d_relation_bridge.py); [gt12_d_to_m4_typed_bridge.py](https://github.com/maidiu/rawlsing/blob/abd0b5ff2ffcf235b67140641f88cc61ca45c12c/rawlsing_next/gt12_d_to_m4_typed_bridge.py)

**proposed_change_class:** IDENTITY_PRESERVING_OPTIMIZATION

**expected_value:** HIGH

**semantic_risk:** MEDIUM

**implementation_cost:** MEDIUM

**identity_effect:** PRESERVING

**authority_effect:** NONE

**recommended_timing:** After ASTRA-001 and ASTRA-002; bank until a measured hot path justifies caching.

**verification_required:** Prove deep immutability first. Cache keys must include exact authority/adoption, operation, family, source and other relevant scope; content hash alone is not operation fitness. Reuse only the same proof proposition, never a broader authority decision.

## Quantified representation calculation

```json
{
  "calculation": "exact UTF-8 length inferred from committed templates/counts; not a full fact materialization benchmark",
  "fact_as_dict_canonical_bytes": 47230656,
  "query_as_dict_canonical_bytes": 7329,
  "B_constructor_document_canonical_bytes": 47238068,
  "B_default_16384_char_shard_count": 2884,
  "A_compact_manifest_plus_binary_bytes": 3108906,
  "B_to_A_byte_ratio": 15.194,
  "fact_exact_ref_occurrences_in_four_large_arrays": 192109
}
```

The committed fact declaration has 76,846 dependency refs, 76,843 provenance refs, 19,210 risk members and 19,210 denominator members: 192,109 exact-ref occurrences across those four arrays. It also declares 36 joint cells and five authority refs. The packed respondent/event/routing inventories total 3,073,600 bytes; the manifest is 35,306 bytes. Fixed ASCII object-id templates and fixed-length hashes determine exact rendered reference lengths. Substituting declared counts into that grammar yields 47,230,656 bytes for fact.as_dict canonical JSON, 7,329 for query.as_dict, and 47,238,068 for the B constructor document envelope. Default sharding gives ceiling(47,238,068 / 16,384) = 2,884.

This is a calculation from the manifest and [serializer grammar](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/pre553_repo_native_seal.py), not a benchmark of a materialized current fact. Binary body contents were not independently verified; their sizes and declared commitments were inspected. The 15.194× ratio describes representation bytes and says nothing by itself about a runtime speedup or peak-RAM multiplier.

## Preserve the expensive meaning; remove unnecessary residence

Source event/provenance closure and exact risk membership protect distinctions that count-only summaries cannot. This audit finds no evidence that those semantic commitments should be removed. A streaming writer can hash the same exact canonical bytes without constructing every repeated dictionary simultaneously; a packed format can reconstruct those bytes without changing the semantic identity.

Replacing exact member/provenance arrays with only count or a new digest in the semantic projection would change identity law: **SEMANTIC_CHANGE_REQUIRES_HQ_DECISION**, identity CHANGING, authority effect UNCLEAR until adjudicated. That is excluded from the identity-preserving recommendations. Similarly, merging producer, transport, admission and owner roles is not a mechanical refactor.

The active [I03 accumulation/dedup changes](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/_pre553_query_eval.py) and [equivalence tests](https://github.com/maidiu/rawlsing/blob/a1630969f8e0b1003e657a38f77abbc413f83f2e/rawlsing_next/tests/test_pre553_i03_scale_equivalence_repair.py) already address a known scaling class. They were inspected and their focused tests passed; the audit does not recommend doing that repair again. R4A already has compact constructor-complete transport; the remaining opportunity is carrying that economy through B and later exact projection boundaries.
