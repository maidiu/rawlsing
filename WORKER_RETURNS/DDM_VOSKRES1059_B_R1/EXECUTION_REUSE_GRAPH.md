# Execution reuse graph — reverse reconstruction

Source: original `25830fe7462bb9e29bc4087e6ae14f3f84cec377`; paths/blobs in `SOURCE_LEDGER.tsv`.
Arrows are producer → reader from actual imports/paths inspected. No execution performed.

## A. V550 main path

```
Postgres respondents + responses
  └─ _prefetch_question_rows_by_country            (repository_v550:722-862)
       one long response frame per country for the union of question vars
  └─ _prepare_v550_question_row_cache               (repository_v550:801-862)
       harmonize response semantics once per country (or chunked), index by var_code
  └─ per question: _question_rows_from_cache        (shard:1519)
       fallback _question_rows DB query only when cache miss/empty (shard:1521-1549)
       |
       ├─ build_distribution_tables                 (distributions:220-312)
       │    ├─ answer_distribution        (pooled; written only if allowed flag)  -> bridge direct_relation_response
       │    ├─ country_answer_distribution                                        -> bridge direct_relation_response
       │    ├─ mapping_gap_report / underpowered_quarantine
       ├─ indicator_summary_rows                    (branching:143-200)
       │    └─ position_indicator_summary                                         -> bridge position_context
       ├─ secondary_indicator_summary_rows          (branching:203-326)
       │    └─ secondary_indicator_summary                                        -> bridge derived_determinicity
       ├─ indicator_answer_matrix_rows              (branching:329-369)
       │    └─ indicator_answer_matrix                                            -> bridge derived_determinicity
       ├─ outlier_cohort_rows                       (branching:435-466)
       │    └─ outlier_cohort_summary                                             -> bridge derived_determinicity
       ├─ branch_nodes_rows                         (branching:372-432)
       │    └─ recursive_branch_nodes                                             -> bridge derived_determinicity
       ├─ cloud builders (conditional on cloud gates) (shard:1645-1660)
       │    ├─ branch_position_signature                                          -> bridge position_context
       │    ├─ branch_relation_co_signature                                       -> bridge position_context
       │    └─ question_response_attitude_cloud
       └─ _write_question_checkpoint per table      (repository_v550:995-1001)
            complete marker + question_use_contract hash (repository_v550:953-993)
  └─ combine checkpoint tables per shard            (repository_v550:1005-1035)
  └─ merge shards + manifests                       (merge_determinicity_shards_v550.py; ddm_v550_manifest.py)
  └─ V551 bridge index for shard                    (ddm_v550_bridge.py:115-123,1402+)

V551: bridge -> direct atoms only
  APPROVED_DIRECT_TABLES = {answer_distribution, country_answer_distribution}
  (ddm_v551_atoms.py:21,153-158; compile_v551_relation_evidence_atoms.py:176-185)
  derived_determinicity bridge rows -> conditional_determinicity index
  (ddm_v551_conditional.py:157-235)
  signed atoms (canonical -1..1 components) -> V552
  (ddm_v552_structural.py:100-128,148-199)

V552: atoms -> pressure -> structural facts
  v552_pressure_component_index -> v552_pressure_observation_index
  -> structural_fact_index / temporal_key_source_index / to-V552J handoff
  (ddm_v552_structural.py:148-259)
  conditional_determinicity parameter accepted at :253 but unused; empty audit at :257-258
  CLI reads the parquet and passes it (compile_v552_structural_ddm.py:299-309); builder ignores it
  V552 input-provenance manifest still requires conditional path/hash/row count
  (ddm_v550_schema.py:1617-1631) -> provenance-only

V551J: atoms + V550J pattern/item/relation/association indexes -> packets
  joint_relation_evidence_packet only if atom_joined AND pattern_joined
  (ddm_v551j_packets.py:244-253,631-642); no conditional-determinicity index input
V552J: V551J certified/review packets + V552 structural facts/temporal keys -> join
  permission ALLOW only certified + both producer permissions ALLOW + observed pressure
  V553 temporal field always false (ddm_v552j_handoff.py:131-140)
```

### Reuse boundaries actually present

- **Shared**: source extraction per country union; harmonization per country union; question rows
  looked up from a prepared cache; memoized question-use-contract hash for resume.
- **Not shared across questions**: indicator entropies, MI/NMI/Cramér V, secondary-gain joints,
  recursive branch search, outlier cohorts, distributions, cloud signatures. Each question frame
  is independent.
- **Not shared across stages**: V551 re-reads V550 bridge/atoms; V552 re-derives pressure from
  atoms; conditional determinicity is not merged into pressure.

## B. V549 / V549b legacy path

```
V549: Postgres respondents (demographics blanked) + responses for all source questions
  └─ load_source_frame: one respondents query, one wide pivot per source (V549:494-557)
  └─ v548 branch trees per question
       └─ build_branch_mask: memoized recursive respondent masks (V549:449-491,718-727)
            predictor columns compared against respondents frame
       └─ summarize_branch: per branch × candidate item Cramér V + direction + confidence
            top-N per branch (V549:560-607)
  └─ CSV append + DuckDB append + per-source parquet checkpoint (V549:610-630,747-768)

V549b: Postgres respondents (demographics loaded) + responses per source
  └─ load_respondents / load_wide_responses (V549b:201-256)
  └─ v548 trees -> build_branch_masks_for_question: memoized recursive masks (V549b:322-375)
  └─ anchor builders: single-answer, answer-presence, branch-node anchors (V549b:421-771)
       Cramér V, direction, confidence, dedupe/rank (V549b:259-297,773-781)
  └─ slice checkpoints + parquet combine + DuckDB (V549b:783-846)
```

### Duplication / divergence

- V549 and V549b implement the same four branch types and the same parent-condition recursion
  independently. V549 anchors root on `anchor_target.notna()`; V549b root on
  `wide[question_var].notna()`.
- V549's loader blanks demographic predictor columns; V549b's loads six of twelve INDICATOR_FIELDS.
- Both memoize masks per `node_id` inside a question; neither shares masks across questions/sources.

## C. V550J same-person substrate

```
shared respondent substrate (per source/wave/country)
  canonicalize -> validate -> atomic promhesis (shared_respondent_substrate.py:332-637)
  prepared substrate cache: long harmonized rows, exact respondent id, manifest hash
  (build_v550j_prepared_substrate.py:316-403,433-521)
       |
       └─ compile_v550j_family_tables (joint_patterns:4925+)
            respondent pattern summary -> pattern counts
            per pattern × outside-family var × response:
              pattern_member_n, answered_var_within_pattern, response_overlap,
              baseline answered (eligible_context), distinct denominators
            association candidate trace / suppression reasons
            (joint_patterns:4250-4410)
```

## D. Reverse-reader observations

- V551 `APPROVED_DIRECT_TABLES` excludes every old derived determinicity table from signed atoms.
- V552's structural output is a signed component mean per empirical distribution, with the
  respondent denominator accepted only when exactly one positive `n_respondents` value exists
  (`ddm_v552_structural.py:182`); heterogeneous denominators become `None` and pressure is
  unresolved rather than summed.
- V551J joint packets consume V550J pattern index/item index/relation signature/manifest/readiness
  (`compile_v551j_joint_evidence_packets.py:150-166`); V552J consumes V551J + V552 manifests and
  emits V553 handoff indexes (`compile_v552j_structural_handoff.py:90-158`). No V553 reader was
  inspected in this pass.
