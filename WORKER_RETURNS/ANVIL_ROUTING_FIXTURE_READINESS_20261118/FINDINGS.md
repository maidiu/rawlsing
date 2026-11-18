# ROUTING FIXTURE READINESS — BOUNDED RETURN

**Answer:** No weighted same-person k>=3 joint with a coordinate predicate exists in the retained sourcefree catalogs. The catalogs contain a true k3 **raw** joint (`f4_three`, A1&B1→C), a **weighted univariate** operation (`selected_weighted`, A1→C), and coordinate predicates only in the discovery/all-predicate path (`G=A/B`), not combined with the weighted k3 joint.

## Reusable saved estates

- **10k/5**: `EXECUTION/fixture_contract_10k.json` SHA-256 `d2a7ffa8...`; estate manifest `e192dc25...`; 10,000 respondents, 5 questions, 32,450 events, 50,000 routing, 10,000 weights, 31,163,472 B retained.
- **128R/600**: `WIDTH128/fixture_contract_width128.json` SHA-256 `89645891...`; estate manifest `4d9604dc...`; 128 respondents, 600 bindings, 68,960 events, 76,800 routing, 128 weights, 55,187,741 B retained.

Exact query/predicate refs and identities are in `FIXTURE_READINESS.json`.

## Smallest actual distinct second operation

Use **`f2_forward_raw` + `f2_reverse_raw`**: changed target (C vs A) and changed predicate (A1 vs C1), both existing on both estates. This pair does not claim weight or k3. For weight/k3 coverage use `selected_weighted` (weight) and `f4_three_raw` (true k3) separately.

Omitted coordinate/weight dimension is covered by existing focused nodes:

- `test_arbitrary_coordinate_conjunction_and_response_position_condition` (coordinate conjunction + response position, univariate target);
- `test_k_way_parity_full_joint_is_not_pairwise_or_unary_synthesis` (true k3 joint);
- `test_raw_and_authorized_weighted_measure_are_distinct_exact_facts` and `test_missing_or_invalid_weight_fails_closed_without_default_one`;
- `test_simpson_reversal_preserves_pooled_and_conditioned_query_identity` (coordinate-conditioned response);
- `test_cold_i03_new_source_content_changes_fact_and_old_root_restores` (changed input → changed fact → restore).

## Harness comparison

One prepared session over the same estate/catalog; capture full fact `as_dict`/`semantic_projection`, cells including observed-zero, raw/weighted masses, risk/denominator member identity sets, provenance/used refs, replay and typed states. Count H/S/Q/O separately, routing objects/materializations, row-group reads/rows/bytes, event/family materializations, selected events, scratch/retained/RSS. Count locator/validation work added to S once vs routing work removed from each Q operation; compare only measured N, no extrapolation. Prior 10k/128R timings are frozen observations, not new measurements.

**No builds, queries, native/SQL execution, fixture rewrites or product changes.** No 100k/full-width/science/source/actor/CURRENT/protected acceptance.
