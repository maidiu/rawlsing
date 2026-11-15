# DDM VOSKRES #1059 — Independent First Pass B (REVERSE)

Status: FROZEN FIRST PASS, documentary only. Agent B started from historical output schemas,
manifests/checkpoints and V551/V552/V552J readers and worked backward to V550 table producers,
then to V549/V549b/V550J computation and preparation.

- Spec: `b9325f094b27d28c20006af9780a91b3254dcab8`
- Original source: `25830fe7462bb9e29bc4087e6ae14f3f84cec377`
- Branch: `codex/voskres1059-reverse-b-20261115-r1`
- Session: `ses_e22479e28ffea7wVPUVS5fXrF3`; model `opencode-go/deepseek-v4.1-flash` max; checkpoint PROVIDER_CHECKPOINT_UNVERIFIED.
- Lease: this return only. No production/test/config/source edits, no execution, no raw governed respondent bytes, no other VOSKRES branch read.
- Token/cost: unknown; not invented. Elapsed first pass within the 20-minute hard cap; no extra round.

## Reverse method actually used

1. V552/V551 reader surfaces: `ddm_v552_structural.py`, `compile_v552_structural_ddm.py`,
   `ddm_v551_atoms.py`, `ddm_v551_conditional.py`, `compile_v551_relation_evidence_atoms.py`.
2. V550 output tables named by those readers and by the bridge lane map
   (`ddm_v550_bridge.py:115-123`): `answer_distribution`, `country_answer_distribution`,
   `indicator_answer_matrix`, `outlier_cohort_summary`, `recursive_branch_nodes`,
   `secondary_indicator_summary`, `position_indicator_summary`, cloud tables.
3. Backward to their writers and per-question checkpoint loop
   (`build_determinicity_wave_shard_v550.py:1506-1661`) and to their metric functions
   (`ddm_v550_metrics.py`, `ddm_v550_branching.py`, `ddm_v550_distributions.py`).
4. Adjacent historical producers: V549 `build_branch_co_signature_summary_v549.py`,
   V549b `build_question_response_attitude_cloud_summary_v549b.py`, V550J
   `ddm_v550j_joint_patterns.py`, shared caches/substrates.

## Strongest reverse findings (all source-only unless marked)

1. **V552 accepts `conditional_determinicity` and never uses it.** The CLI reads the parquet and
   passes it into `build_v552_structural_outputs`
   (`compile_v552_structural_ddm.py:299-309`), but the builder references it only in the signature
   and an empty `conditional_determinicity_status_audit` schema row. The V551 derived determinicity
   lane can be indexed, but the inspected V552 producer does not consume that index. This is a
   concrete semantic dead end, not a performance issue. (`ddm_v552_structural.py:253-259`, blob
   `0df56d70cb3880dee723df00aea2207acd525260`; caller blob
   `0f9a28749ed5858a4814ec8e8fa6b53000f343de`.)
2. **V551 promotes only the two direct response distributions.** `APPROVED_DIRECT_TABLES =
   {answer_distribution, country_answer_distribution}`; the derived determinicity tables are
   eligible only for a separate conditional index. Modern exact I03 diagnostics compute MI/entropy
   from an exact arity-2 joint fact (`rawlsing_next/pre553_diagnostics.py:243-365,622-752`, spec HEAD
   blob `32a2d063f3b69fc983b352e69e032dd214a3e8d7`), a different grain from the old indicator-level
   primary/secondary/recursive products.
3. **Old MI is not MI on one population.** Baseline H(Y) uses all question respondents; H(Y|X) uses
   only indicator-observed respondents; `mi = max(0, baseline_h - cond_h)`. NMI recomputes H on the
   masked pair. Same pattern in secondary candidate scoring. This independently reconfirms the
   ZAK02 T0026 defect. (`ddm_v550_branching.py:143-200,203-264`; `ddm_v550_metrics.py:77-140`.)
4. **Old recursive branch selection is unweighted, top-two, depth-3, and conditional on a
   structurally different mask.** `branch_nodes_rows` uses unweighted H, stops at depth 3 /
   support / purity / no-gain, and expands only the two most frequent values. Secondary gain uses
   a joint mask, but the emitted baseline/conditional columns in the secondary row are the
   candidate's own, not the joint pair. (`ddm_v550_branching.py:203-326,372-432`.)
5. **V549 branch masks can be degenerate by construction.** `load_source_frame` initializes
   `sex=""`, `age=nan`, `education_level=nan`, `income_level=nan`, `religion_label=""`,
   `urban_rural=""`, `age_group=""` and does not load the other INDICATOR_FIELDS; the branch-mask
   builder is then called with that respondents frame. Demographic predictor comparisons are
   therefore mostly empty/degenerate. V549b rebuilds the same memoized masks from a respondents
   query that actually loads sex/age/education/income/religion/urban_rural, but still lacks the
   remaining indicator fields. (`build_branch_co_signature_summary_v549.py:449-491,494-557,725`;
   `build_question_response_attitude_cloud_summary_v549b.py:201-231,322-375`.)
6. **V550J preserves multiple same-person denominators but labels a scaled log-ratio as MI.**
   It emits `pattern_member_n_unweighted`, `pattern_member_rows_for_var`,
   `response_overlap_n_unweighted`, `baseline_answered_n_unweighted`,
   `eligible_rows_for_var`, with `denominator_basis=answered_var_within_pattern` and
   `baseline_denominator_basis=eligible_context`; `mutual_information =
   log2(p_given_pattern / baseline_share) * pattern_count / family_count`, which is not the MI of
   the 2×2 joint distribution. (`ddm_v550j_joint_patterns.py:4250-4410`; sample of denominator
   columns at 4384-4405.)
7. **Distribution pooling/country distinction exists; the inspected shard path is country-scoped.**
   `build_distribution_tables` writes a pooled `answer_distribution` with
   `analysis_scope="country"` and a separate `country_answer_distribution`; both are suppressed
   unless `allowed_as_response_distribution` is true. In the inspected wave-shard path the cached
   question frame is keyed/selected by `country_code`
   (`build_determinicity_repository_v550.py:866-897`), so pooled equals country there and the label
   is not observed to lie. The function-level risk remains for any multi-country caller; no such
   caller was proved. (`ddm_v550_distributions.py:220-312`; gate
   `build_determinicity_wave_shard_v550.py:1598-1600`.)
8. **What was genuinely shared is preparation, not derived statistics.** The old V550 path
   prefetches all needed response rows per country once, harmonizes them once (country or chunked),
   then serves each question from that cache with a per-question DB fallback; each question still
   recomputes distributions, all indicator metrics, secondary metrics, branch recursion and cloud
   products from scratch. Per-question parquet checkpoints exist for every table and resume
   verifies a question-use-contract hash. (`build_determinicity_wave_shard_v550.py:1380-1396,
   1506-1661`; `build_determinicity_repository_v550.py:722-862,953-1004`.)
9. **V549/V549b share respondent-level work only inside one source/question tree.** One respondents
   query + one wide-response query per source; per-question recursive masks are memoized in a dict;
   each mask is reused across all candidate items for that branch and scored by Cramér's V.
   Checkpoints are per source slice; CSV and DuckDB are appended incrementally.
   (`build_branch_co_signature_summary_v549.py:494-557,467-607,718-768`.)

## Explicit limits

- No old run logs, manifests or result rows were inspected; no historical runtime is claimed.
  `HISTORICAL_RUNTIME_UNKNOWN`.
- Source-only does not prove executed use. V549/V549b/V550J/V551/V552 fates are limited to the
  inspected objects and lines in `SOURCE_LEDGER.tsv`.
- Modern comparison is limited to the spec HEAD files named above. Merged #684/#686/#707,
  S2-C/D D13 families, `_pre553_query_eval` behavior at `3e0ed...`, and #1006 R2 receipts were
  not independently inspected in this pass.
- NOT_INSPECTED is never converted to NOT_FOUND. No scientific/native/global acceptance is claimed.

## Weak claims / self-identified gaps

- V552's unused parameter conclusion is proven for the inspected producer function; another caller
  could post-process the conditional index outside this file (`NOT_INSPECTED`).
- V549 blank-demographic effect is a code-path inference; no executed tree was observed, and some
  v548 trees may use predictors not initialized in the loader.
- V550J MI formula is proven for the inspected branch; other association lanes may compute
  differently.
