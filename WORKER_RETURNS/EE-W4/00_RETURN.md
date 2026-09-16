# EE-W4 — governed return

Status: `PASS__CANDIDATE_NEUTRAL_MANIFEST_DRIVEN_ABC_HARNESS_READY__FINAL_BAKEOFF_NOT_RUN`

Worker: `EE-W4`  
Branch: `agent/rabochii-prev3-ee-w4-abc-hostile-measurement-harness-r1`  
Commission tip: `29d39f3d37100eda692ece6a28de3ca2c9ecc4b8`  
Grain: `IMPLEMENT_CANDIDATE_NEUTRAL_MANIFEST_DRIVEN_ABC_MEASUREMENT_AND_HOSTILE_NON_LOSS_HARNESS_ONLY`

## Holding

A reusable candidate-neutral execution/measurement harness is implemented. It consumes a frozen, fully-unrolled workload execution profile without choosing semantic content. A/B/C receive byte-identical logical step requests and the exact same declared step order. Authority-limited cells are represented explicitly and do not invoke a candidate. Semantic and identity oracles gate measurement eligibility before physical metrics can be used.

The implementation supports the common contract's 20 hostile conservation cases, cold/warm repetition labels including `cold`, `warm_1`, `warm_2`, `warm_5`, isolated scratch/durable state, source open/decode accounting, CPU/RSS/wall accounting, delete/rebuild, replay, source invalidation, semantic/routing-authority invalidation, durable/scratch bytes, rewrite/cache telemetry, and deterministic logical receipts.

Metric aggregation is keyed by `(candidate_id, universe_id, operation_id, phase)`. There is no cross-universe pooling and no score/ranking surface.

## Validation

Local deterministic synthetic harness tests: `6 passed` under Python `3.13.5` on Linux. The tests prove:

- omitted/failed/incomplete semantic work cannot be performance-eligible;
- missing authority is typed ineligible rather than candidate failure;
- a semantic-oracle mismatch fails a cell regardless of speed;
- candidate execution ordering does not alter canonical logical receipt identity;
- warm/repeat state is isolated by candidate;
- delete/rebuild, source invalidation, authority invalidation and replay preserve the declared identity-oracle contract;
- metric grouping retains exact universe identity;
- all 20 frozen hostile case IDs are accepted by the harness.

No real A/B/C candidate was executed by this return. Synthetic adapters were used only to validate harness mechanics.

## Boundaries

- final A/B/C comparison: `NOT_RUN`
- candidate ranking: `NONE`
- architecture retirement: `NONE`
- workload-definition semantic decisions: `NONE`
- survey/source semantic inference: `NONE`
- MAIN mutation: `NONE`
- semantic PRE-MAIN mutation: `NONE`
- candidate-specific workload weakening: `NONE`

Terminal: `PASS__EE_W4_HARNESS_CAN_CONSUME_FROZEN_EE_W1_WORKLOAD_WITHOUT_NEW_SEMANTIC_DECISIONS`
