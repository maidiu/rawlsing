# EE-R2E — governed return

Status: `PASS__EE_W4_ABC_HARNESS_INDEPENDENTLY_QUALIFIED`

Worker: `EE-R2E`  
Branch: `agent/rabochii-prev3-ee-r2e-abc-harness-independent-qualification-r1`  
Commission tip: `e6e7c8cf5d24a76814d04f63fe9ae6c1d4e6a993`  
Grain: `INDEPENDENTLY_QUALIFY_EXACT_EE_W4_CANDIDATE_NEUTRAL_MANIFEST_DRIVEN_ABC_HARNESS_ONLY`

## Authority and exact subject

Canonical HQ pointer resolved to checkpoint `20260916T0219-0400`, sealed at handoff commit `d3d96e0c753707ee8615cc25c77d2fcb45adb950`, with semantic PRE-MAIN tip `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`.

Exact EE-W4 return head independently qualified: `b74b7cf0b8cb3f7e5fae80094a7db7d26ce20457`.

Immutable implementation/test Git blobs reconstructed byte-for-byte and re-hashed as Git blobs:

- `rawlsing_next/ee_w4_harness_contract.py` — `e8b0fa484fad2a93937b83808204dc58a93d2b70`
- `rawlsing_next/ee_w4_harness_runtime.py` — `2e04ebe391f90e3e00ceae0841464adc58617cea`
- `rawlsing_next/ee_w4_abc_hostile_measurement_harness.py` — `1c5e2e9f4933effee60dce31482424661d6a2252`
- `tests/test_ee_w4_abc_hostile_measurement_harness.py` — `1d314c762cf35253577a1d927ab192be7786bf26`

Supporting governed EE-W4 identities checked at the same immutable return head:

- harness contract — `8bbf860e073cc061f4f4364d06214d4f2059241b`
- hostile fixture/oracle index — `3054935af8bc7a146cb201c2c78603a3f2508437`
- authority/validation receipt — `36e3d86ae72962007c25c1c41d75c087b4ef56f0`

## Exact upstream test replay

Environment: Python `3.13.5`, Linux x86_64.

The exact six EE-W4 tests from blob `1d314c762cf35253577a1d927ab192be7786bf26` were executed without modifying the implementation. They were run in two deterministic partitions and all six passed:

1. `test_equal_work_ineligible_not_failure_and_no_universe_pooling`
2. `test_semantic_mismatch_fails_regardless_of_speed`
3. `test_candidate_order_does_not_change_logical_receipt`
4. `test_repeat_delete_rebuild_invalidate_replay_preserve_declared_order_and_identity`
5. `test_omitted_or_incomplete_work_cannot_score_as_win`
6. `test_all_frozen_hostile_ids_are_supported`

Observed results: first partition `3 passed`; second partition `3 passed`; total `6 passed`.

## Independent qualification

A separate synthetic-mechanics qualification was then executed against the exact reconstructed EE-W4 blobs. It used no real A/B/C candidate and made no semantic decisions.

Proved independently:

- every invoked eligible candidate-action request file was byte-identical across A/B/C, and all candidates traversed the same frozen step order;
- semantic-oracle mismatch and identity-oracle mismatch independently force `performance_eligible=false`;
- `MISSING_AUTHORITY`, `INELIGIBLE`, and `NONCOMPARABLE` cells create no candidate request and remain typed non-failures;
- nonzero/omitted work and incomplete required telemetry cannot become performance-eligible;
- A/B/C receive disjoint scratch/durable/log/request/response roots across cold/warm/repeat/action phases; candidate-owned durable markers remained confined to their own roots;
- metric group keys and payloads retain exact `universe_id`; no cross-universe aggregation was produced;
- cold/warm_1/warm_2/warm_5, delete-durable/rebuild, selective source invalidation, selective authority invalidation, and replay were exercised in one frozen order with identity-oracle PASS throughout eligible candidate actions;
- all 20 exact hostile IDs from `3054935af8bc7a146cb201c2c78603a3f2508437` were accepted and preserved verbatim in typed `NONCOMPARABLE` records while `/bin/false` candidate adapters were never invoked; the harness only validates membership/passes the case ID through and does not derive semantic meaning or expected outputs from it;
- no score/winner/ranking variable surface was present in the executable harness AST, no ranking field was emitted, and candidate identity selects only physical root/argv while every candidate iterates the same `plan["steps"]` workload path.

Independent core logical receipt SHA-256: `f4a7daf583a6e366d8c21a6d5403e7c2fdde57a0b8768ebccfa7f1af1a9f61cc`.

## Boundaries

- repair/redesign: `NONE`
- real A/B/C execution: `NONE`
- final comparison/ranking: `NONE`
- architecture selection/retirement: `NONE`
- semantic reinterpretation: `NONE`
- Library use: `NONE`
- MAIN mutation: `NONE`
- semantic PRE-MAIN mutation: `NONE`

Terminal: `PASS__EXACT_EE_W4_CANDIDATE_NEUTRAL_MANIFEST_DRIVEN_ABC_HARNESS_INDEPENDENTLY_QUALIFIED`
