# FORGE fates and counterexamples (finite inspected region)

Modern evidence commit: `3e0ed0794498506520ae62c997a5c852ac672061`. Source label/name is not equivalence. Old source: `25830fe7462bb9e29bc4087e6ae14f3f84cec377`.

## Fates that are source-supported

| Old capability/mechanism | Modern inspected fate | Disposition | Counterexample / caution |
|---|---|---|---|
| Country response prefetch + harmonized question cache (V550) | No exact successor in the inspected V550 sense; modern relies on sealed C11 release index and exact refs | PRESENT_PARTIAL / REPLACED_PATH | Modern grouped core shares membership cores, but grouped reuse is forbidden on cold `DirectEstateI03Session` (`pre553_empirical_query.py:756-757`) and under runtime successor binding (`_pre553_query_eval.py:420-431`). Cannot claim loss or parity. |
| Per-question SQL fallback; empty means skip and checkpoint | Modern typed states distinguish zero denominator, empty risk set, unresolved target, inapplicable routing (`_pre553_query_eval.py:505-530`) | PRESENT_STRONGER | Old “no rows -> skipped” conflates not-asked, missing data and empty cell (shard `1527-1534`). Do not port the old skip semantics. |
| Content-addressed on-disk parquet cache with signature (V550 shared cache, V550J prepared substrate) | No inspected general cross-run semantic cache; grouped I03 scope is execution-local and nonauthoritative (`pre553_empirical_query.py:490-503`) | REVIEWED_UNMERGED / COMPARE_UNKNOWN | A durable cache is not automatically authority; modern deliberately refuses cache hits as authority (`pre553_batch_runner.py:386-391`). Old cache correctness/authority is unproved. |
| V549/V549b recursive branch masks | No exact successor inspected | COMPARE_UNKNOWN | Old source duplicates the mask builder in two files; do not infer a modern absence from I03 alone. |
| Entropy/MI/NMI/Cramer V indicator scoring | Modern I03 computes exact conditionals/joints; current I05 diagnostics referenced by controlling doc were not inspected here | PRESENT_PARTIAL at mathematical-fact level; SCORE/USE UNKNOWN | Old MI is **not** generally MI on one population: baseline over all rows vs conditional over indicator-observed rows (`ddm_v550_branching.py:145-161`); secondary gain mixes primary and intersection masks (`:269-289`). Modern exact facts are not proof that old ranking/use was conserved. |
| Recursive top-two branch tree / minority classification | No exact modern consumer inspected | COMPARE_UNKNOWN | The old recursion is deliberately greedy and top-two-only (`branching.py:424-429`); it is not a normative target. |
| Pooled vs country answer distributions with specials and weights | Modern exact risk/denominator/weight reasoning is stronger in the inspected I03 path (`_pre553_query_eval.py:505-623`) | PRESENT_PARTIAL / STRONGER MATH | Pooled and country denominators are genuinely distinct (`ddm_v550_distributions.py:255-309`); same marginals do not imply same joint/denominator. |
| V550J prepared country substrate and family pattern compilation | Related modern same-respondent joint facts exist but were not inspected at the family/pattern grain | COMPARE_UNKNOWN | Do not equate I03 joint truth with old signed/certified vector handoff. |
| Signed atom / conditional determinicity lane separation (V551 bridge) | Modern evidence kinds/authority states are separate | FUNCTION_ONLY | Performance sharing is separable from lane semantics. A bridge identity reduction (`ddm_v550_bridge.py:804-860`) can lose distinctions independent of speed. |

## Counterexamples to candidate common-cause stories

1. **“Old shared everything, modern lost it.”** False as stated: old per-question functions recompute baseline entropy, indicator conditionals, groupbys and masks repeatedly; V549 and V549b duplicate branch-mask logic. Modern has a real exact grouped-core cache. The common cause, if any, is a **different reuse boundary**, not simple presence/absence. Tag: `RELATED_UNPROVED`.
2. **“Old MI machinery was scientifically sound.”** False as stated: the indicator MI and secondary gain have population/denominator inconsistencies (`branching.py:145-161,269-289`). Preserving the old computation would preserve a defect. Tag: `INDEPENDENT` (correctness issue separable from performance).
3. **“Grouped core exists, so #1006 performance is solved.”** False: grouped core is opt-in, sealed-index only, execution-local, and explicitly blocked for cold S2-C direct estate (`_pre553_query_eval.py:404-431`; `pre553_empirical_query.py:756-757`). The R2 543.026 s → 294.087 s figure is sourcefree TEST_ONLY at the named commit, not production. Tag: `PERFORMANCE_ONLY`.
4. **“Bridge row loss is proved.”** Not in this pass: the reduced payload demonstrably omits branch/secondary-specific fields, but actual producer-row collapse and any current native drop were not observed. Tag: `RELATED_UNPROVED`; exact follow-up is a hash-collision audit on historical bridge rows, which requires governed output access not held here.
5. **“V550 question cache equals modern release index.”** False in mechanism and authority: old cache is a raw PostgreSQL slice keyed by source/wave/country; modern exact refs are versioned C11 objects with authority and replay. Similar amortization purpose, not semantic equivalence. Tag: `FUNCTION_ONLY`.

## Common-cause adjudication in the finite region

- **Economics link:** the old pattern “prepare respondent-aligned membership/denominator once, reuse across operations” is genuinely present and the modern grouped core implements a guarded analogue. Whether restoring/expanding it would materially reduce FORGE S1–S5 cost is `RELATED_UNPROVED` without a matched batch measurement. No `SHARED_CAUSAL_LOSS_PROVED`.
- **Analytical-function link:** old secondary gain, recursive branch tree, outlier classification, and signed/certified handoffs are **not** shown to be conserved or lost by the grouped-core evidence. These remain `COMPARE_UNKNOWN`/`FUNCTION_ONLY`, not performance casualties.
- **Correctness link:** the old population-mixing defect is independent of the cache and must not be conserved.
