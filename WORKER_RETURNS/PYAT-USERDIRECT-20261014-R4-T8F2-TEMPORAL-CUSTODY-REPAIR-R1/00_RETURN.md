# R4 T8F2 — Temporal Custody Repair Return

**Branch:** `agent/userdirect-pyat-20261014-r4-t8f2-temporal-custody-repair-r1`
**Sealed startup:** `4c2adb8717f9f2679fba5f53b1ffc56ccf1fc17a`
**T8I court:** `cbbaf051cf5df72f6d32b8de6755b5eec0c10a51`
**T8F author:** `76cbd9b447bf7525a6831b339117870399b1f8f4`
**T8C original:** `059d7ce1b35a08fa4fe735ffccc1a5dddbfe5899`

## All ten T8I REDs closed

| RED | Defect | Repair | Test |
|---|---|---|---|
| R1 | Variance-only change collides identity | content_hash covers all 18 WaveFact fields | distinct_valid_variance_no_identity_collision |
| R2 | (same class: claim fields outside digest) | variance/method/weight/selector/population/sample in digest | old_ref_retains_original_fact |
| R3 | Forged ref.year accepted | retrieve() checks stored.year == ref.year (FACT_YEAR_MISMATCH) | wave_ref_year_bound_to_fact |
| R4 | Extraneous ref fields | frozen WaveFactRef + _check_ref_schema | schema enforced |
| R5 | Mutable list alias corrupts fact | __post_init__ tuple-normalize + registry stores tuples | mutable_category_list_defensively_copied |
| R6 | Self-resigned forged delta accepted | recompute delta from registry facts (TEMPORAL_DELTA_ARITHMETIC_MISMATCH) | self_resigned_forged_delta_refused |
| R7 | Self-resigned forged variance delta accepted | recompute variance sum (VARIANCE_DELTA_ARITHMETIC_MISMATCH) | self_resigned_forged_variance_delta_refused |
| R8 | Coherent rewrite without verified refs | two-ref dereference + per-category/per-special/weight verification | consistent_numerical_source_rewrite_refused |
| R9 | Forged publication accepted | AUTHORITATIVE_PUBLICATIONS clock (SOURCE_PUBLICATION_CLOCK_MISMATCH) | rewritten_historical_publication_refused |
| R10 | Rewritten eligible risk accepted | eligible/asked recomputed from facts | rewritten_eligible_risk_refused |
| +0 | Native category-0 omission | explicit 5-key presence check (NATIVE_CATEGORY_ZERO_MISSING) | forged_semantics_native_code_omission_refused |

## Execution evidence

| Suite | Result |
|---|---|
| T8F2 custody (16 T8I-adapted + 5 extras) | 21/21 PASS |
| Original T8C 19 untouched (historical control) | 19/19 PASS |
| T8R 3 mandatory untouched (RED expected) | 3 FAILED as expected |

The 19 are not counted as T8F2 acceptance; the T8R 3 REDs reproduce against original T8C.

## Preserved

Ghana native category 0, R5=998/R9=8, independent cross-sections, original 2015/2024 clocks, unknown 2017 gap. No invented trend, no same-person joins.

## HQ214 reuse

`rawlsing_next/pre553_temporal_comparability.py` absent at this read cut and at canonical `7f29aec36`. Classified TECH_BLOCKER (missing implementation), not an authority grant. Local scalar delta/variance arithmetic used instead, labeled test-double method.

## Holds

No EE12, no N8E/N9, no N8S, no V3. Test-only trusted registry authority.

## Terminal

`R4_T8F2_TEMPORAL_CUSTODY_REPAIR__TEN_REDS_CLOSED__21_TESTS_PASS__AWAITING_INDEPENDENT_REVIEW`
