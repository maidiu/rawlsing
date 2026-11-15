# Execution and reuse graph — old V549/V550/V550J → handoff, with modern touchpoint

All edges are SOURCE_ONLY at `25830fe7462bb9e29bc4087e6ae14f3f84cec377` unless marked modern `3e0ed07...`. No historical run log or output file was read.

```text
Postgres response-long relation
  └─[V550 shard] _prefetch_question_rows_by_country  (1 query / country; repository_v550.py 722-798)
       └─ question_row_cache {country -> frame indexed by var_code}
            ├─ _prepare_v550_question_row_cache (1 harmonization / country or 100k chunks; 801-862)
            ├─ [optional] shared respondent substrate write (shard 1391-1433; canonicalize + atomic)
            ├─ per question: _question_rows_from_cache (866-917)
            │     └─ empty? -> _question_rows per-question SQL (679-719) -> harmonize fallback
            ├─ per question analytical families (shard 1591-1661)
            │     ├─ build_distribution_tables -> answer_distribution + country_answer_distribution
            │     ├─ indicator_summary_rows -> position_indicator_summary
            │     ├─ secondary_indicator_summary_rows -> secondary_indicator_summary
            │     ├─ indicator_answer_matrix_rows -> indicator_answer_matrix
            │     ├─ outlier_cohort_rows -> outlier_cohort_summary
            │     ├─ branch_nodes_rows -> recursive_branch_nodes
            │     └─ conditional cloud emission -> attitude cloud + position/relation co-signature
            ├─ per-question checkpoints (parquet) + wave accumulators
            ├─ concat + write ~26 shard tables (1977-2014)
            └─ bridge write (ddm_v550_bridge; imports at shard 61)

V549 source scan (build_branch_co_signature_summary_v549.py)
  ├─ 1 respondents read + 1 wide pivot per source (494-557)
  ├─ V548 tree nodes -> build_branch_mask recursive memo per tree (449-491)
  ├─ per branch mask: summarize_branch vs candidate items (560-608)
  └─ branch_co_signature_summary + question_relation_registry

V549b source scan (build_question_response_attitude_cloud_summary_v549b.py)
  └─ independent wide frame + per-question recursive masks (234-257; 322-376) -> cloud anchors

V550J
  ├─ compile_v550j_joint_response_patterns (compile...py 1607-1960)
  │    ├─ cached country slice (shared cache module) or _prefetch_question_rows_by_country
  │    ├─ load_or_build_v550j_prepared_substrate (per source/wave/country signed cache)
  │    ├─ country_prepared_state reuse across families
  │    └─ compile_v550j_family_tables (joint_patterns.py 4925-4979) -> pattern/index/membership tables
  ├─ V551J packets read V550J pattern/item/relation/manifest (compile_v551j 140-167)
  └─ V551 atoms <- v551_bridge_index (compile_v551 161-207)
       └─ V552 structural <- V551 bundle + optional conditional determinicity parquet (compile_v552 291-309)

Modern 3e0ed07 (#1006 R2 named locality)
  I03 native query -> _ReleaseIndex -> I03GroupedExecutionScope (execution-local)
      -> _GroupCore (risk/denominator/membership/cell resolution, no weights/facts)
      -> _materialize_grouped_evaluation per operation (RAW or GOVERNED_WEIGHTED; weights and facts rebuilt)
  Guard: runtime successor binding -> no sharing; unsealed index -> no sharing; cold DirectEstateI03Session -> no grouped cache.
```

## Reuse boundary summary

| Work item | Old reuse boundary | Fallback | Retained | Cross-run? |
|---|---|---|---|---|
| Country response slice | all questions in shard | per-question SQL if slice empty | memory | no (V550 shard path) |
| Harmonized country frame | all questions in shard | harmonize per-question fallback | memory | no |
| Respondent×variable wide frame (V549) | all questions in one source scan | none | memory | no |
| Branch mask | node tree / question | recompute parent chain | memory per question | no |
| Distribution grouping | per question, pooled+country | n/a | checkpoint | resume only |
| V550J country substrate | all families in run | prefetch or rebuild; fail closed if required | memory + on-disk parquet/manifest | yes, signature checked |
| V550J family indexes | compiled per family-country | no reuse across families except prepared frame | output tables | via outputs |
| Modern grouped I03 core | one execution scope, up to 64 groups / 500k members | native per-operation path | execution-local dict | no (deliberately) |

## Key implied engineering contrast (not a runtime comparison)

Old reuse is **coarse and broad**: country-level raw/harmonized frames and respondent-wide pivots are reused across many questions, but each analytical family then re-derives entropies, masks and groupbys. Modern reuse is **narrow and exact**: risk/denominator membership and cell resolution are shared within one guarded execution scope, while weights and facts are rebuilt per operation. These are different reuse contracts; neither source establishes that one is faster in historical or current practice.
