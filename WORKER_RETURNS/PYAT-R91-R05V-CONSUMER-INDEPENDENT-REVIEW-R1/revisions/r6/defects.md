# R91 R05V R6 independent review — defects

## R6-P1 — Unadmitted executor-only coordinator mints a trusted original

`TrustedNativeGraphCoordinator(executors={...})` without admitted slots still
accepts a request slot, calls the executor, receives a prebuilt
`AnalyticalCompositionResult`, validates fields, and retains a trusted original.
Probe `probes/test_r05v_r6_actual_gap.py::test_unadmitted_executor_cannot_mint_trusted_original`:
actual M01 composition via executor-only coordinator -> trusted consumer
`LEARNED_CONSUMER_EXACT_SUPPORTED`. This violates the High decision's admitted
operation boundary and the R6 contract claim that execution uses admitted slots.

## R6-P2 — Learned M1/M2/B5 not bound to the retained original

The trusted consumer resolves the original components but does not compare the
submitted `learned` M1 disposition/M2 release/B5/currentness to the retained slot
records. Probe `::test_trusted_consumer_binds_learned_m1_m2_b5_to_original`:
capture the actual AT10 discovery trusted call, substitute a second productive
learned product built from the same discovery with a different M1 disposition
(`83220c...` vs `049214...`); the same graph/reader returns
`LEARNED_CONSUMER_EXACT_SUPPORTED`.

## R6-P3 — Actual joint and actual evidence-change routes remain raw-only

Dynamic capture of the R6 actual AT10 discovery test: `raw_joint_calls=1`,
`trusted_joint_calls=0`. The actual joint composition does not use the
coordinator/trusted reader; the added target-arity/order slot fields are not
exercised. The actual evidence-change composition is also raw and has no
trusted-restore path.

## Already-qualified partial

- Author 40/40; prior R1/R2/R3/R5 probes 19/19; provider 43/43; C1 13/13.
- NativeGraphSlot now carries actual fields; actual AT10 discovery/AT11
  recursive coordinator execution and E41 route/receipt reconciliation pass;
  retained-original view mutation and typed axes retained.
- Accepted R08/provider/evaluator bodies unchanged.
