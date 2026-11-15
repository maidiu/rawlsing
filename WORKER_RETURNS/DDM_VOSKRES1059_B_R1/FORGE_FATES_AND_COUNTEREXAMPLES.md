# FORGE fates and counterexamples — reverse first pass

Modern inspection is limited to spec HEAD `b9325f094b27d28c20006af9780a91b3254dcab8`:
`rawlsing_next/pre553_diagnostics.py` (blob `32a2d063f3b69fc983b352e69e032dd214a3e8d7`) and
`rawlsing_next/_pre553_query_eval.py` (blob `9808a6b72c716e26ebce5cbd76ef5ef6f3b5c920`).
No merged #684/#686/#707, S2-C/D D13 family, `_pre553_query_eval.py` at `3e0ed...`, or #1006
receipt was independently inspected. No equivalence is claimed from names.

## Fates in the inspected modern files

| Old product | Modern inspected representation | Fate (inspected scope) |
|---|---|---|
| Indicator-level H/MI/NMI/Cramér V summary (T01) | exact H/MI/NMI from arity-2 joint fact with complete cell projection, diagnostic-only (`pre553_diagnostics.py:243-365,622-752`) | PRESENT_PARTIAL / different grain; old indicator-masked MI not reproduced |
| Secondary joint gain (T02) | none located | NOT_INSPECTED outside files; cannot say NOT_FOUND |
| Recursive branch topology (T03) | none located; `_pre553_query_eval` materializes groups, not trees | NOT_INSPECTED outside files |
| Minority/outlier classification (T04) | none located | NOT_INSPECTED outside files |
| Direct answer distributions (T05) | I03 empirical facts and exact marginal/joint evaluation exist; not compared output-by-output | RELATED_UNPROVED |
| Same-person joint patterns/denominators (T09) | grouped I03 group core caches routing/risk membership, condition truth and target configuration per compatible group (`_pre553_query_eval.py:315-430,552-626`); exact ordered/repeated semantics at :123-150 | mechanism related; old pattern/denominator parity NOT_PROVED |
| V551/V552 signed pressure (T10/T11) | no counterpart inspected | FUNCTION_ONLY_GAP in inspected scope |
| Conditional determinicity (T12) | no counterpart inspected; old V552 itself dead-ends | FUNCTION_ONLY_GAP in inspected scope |

## Strongest counterexamples to naive equivalence

1. **Same name, different population.** Old `mutual_information` in
   `ddm_v550_branching.py:159` is a clipped difference between full-sample H(Y) and
   indicator-observed H(Y|X). Modern `pre553_diagnostics.py:324-361` computes H/MI from one
   contingency table with cell totals. Numerically and epistemically different.
2. **A field named MI that is not MI.** V550J `mutual_information` at
   `ddm_v550j_joint_patterns.py:4285` is `log2(p_given_pattern/baseline_share) * pattern_count /
   family_count`; no joint entropy term. Do not treat old V550J MI columns as MI.
3. **A typed channel that goes nowhere.** V551 builds a conditional determinicity index; V552
   accepts `conditional_determinicity` and does not use it (`ddm_v552_structural.py:253-259`).
   An index existing is not a consumer.
4. **Branch masks can be empty by construction.** V549's loader blanks the demographic columns
   that `build_branch_mask` later compares (`build_branch_co_signature_summary_v549.py:518-524`
   vs `:449-491`). V549b partially repairs this by loading six indicator fields. A historical
   branch summary therefore cannot be assumed to have had usable demographic splits.
5. **Distributions can be pooled but labelled country — function-level risk only.** 
   `build_distribution_tables` writes `analysis_scope="country"` on the pooled table
   (`ddm_v550_distributions.py:267`) and a separate country table (`:281-312`). In the inspected
   wave-shard path the question frame is selected from a per-country cache
   (`build_determinicity_repository_v550.py:866-897`), so pooled equals country there. The risk
   applies only to an unproved multi-country caller.
6. **V552 cannot express heterogeneous respondent bases.** It accepts a denominator only when
   exactly one positive `n_respondents` value exists (`ddm_v552_structural.py:182`); otherwise the
   pressure observation is unresolved. Old tables could carry multiple denominators; the modern
   bridge may lose that distinction.
7. **Ordered/repeated same-person semantics are modern-exact.** `_pre553_query_eval.py:123-150`
   fails closed when ordered/repeated targets lack exact multiplicity/order/rank fields. This is a
   modern positive relative to old V549/V549b mask builders, which had no such typed guard in the
   inspected code.

## Common-cause tags (documentary only)

| Relation | Tag | Basis |
|---|---|---|
| Old prepared country cache / wide pivot → current repeated query cost | PERFORMANCE_ONLY | source-only reuse pattern; no runtime measurement |
| Old derived determinicity lane → V552 pressure cost/absence | FUNCTION_ONLY | conditional index unconsumed; no evidence it explains query cost |
| Old MI estimator defect → modern diagnostic differences | INDEPENDENT | metric defect is mathematical, not a cost mechanism |
| Old branch/cloud computation → modern grouped I03 absence of tree products | RELATED_UNPROVED | both involve respondent masks, but no matched output comparison |
| Old same-person joints → modern grouped core | RELATED_UNPROVED | conceptual overlap; parity untested |
| Loss of shared preparation → both cost and lost function | NOT_TAGGED | no supporting matched evidence; SHARED_CAUSAL_LOSS_PROVED not claimed |

## Smallest engineering recommendations routed to existing owners (no new engine)

1. **#960 / W05 / P03 / #1006**: measure old-style question-local derived fan-out vs a shared
   respondent-aligned derived cache at 100/1000 query scale; do not infer old speed.
2. **Existing I03/C11 owners**: add a conditional-determinicity receiving check: if V551
   conditional index remains intentionally unsupported, record an explicit retirement/hand-off
   rather than an accepted-but-unused parameter.
3. **Existing diagnostics owner**: require population identity in any MI/NMI output (same
   denominator for H(Y), H(Y|X), MI) and forbid the V550J "MI" formula from being cited as MI.
4. **Existing S2/S04 owners**: test pooled-vs-country distribution labels and multiple
   denominators on a multi-country fixture; preserve typed special states.
5. **V549/V549b archaeology-only**: do not port branch summaries until predictor-column
   availability is proved; the V549 loader blanking is a counterexample, not a performance fact.

8. **Downstream permission is not downstream consumption.** V552J emits a V553 *probe* permission
   with `v553_temporal_field_allowed=False` and requires both producer permissions ALLOW plus
   observed pressure (`ddm_v552j_handoff.py:131-140`). A join index row is not evidence that a V553
   consumer exists or that signed pressure becomes a structural fact.
