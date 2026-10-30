# H06 hostile execution and replay

## Executed commands

All commands were run from the H06 worktree root with `PYTHONPATH=.` and `PYTHONDONTWRITEBYTECODE=1`.

| Command | Result |
|---|---|
| `python3 -m pytest rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py -q` | **35 passed**, 0 failed/errors/skipped, 7.12 s |
| `python3 -m pytest rawlsing_next/tests/test_pre553_analytical_composition.py rawlsing_next/tests/test_pre553_analytical_replay_dependency.py -q` | **56 passed**, 0 failed/errors/skipped, 46.39 s |
| `python3 WORKER_RETURNS/PYAT-H06-DDM-COMPOSITION-REAL-CONSUMER-R1/repro/run_receipt.py` | Receipt written; AT10 3/3 branches `EXACT_SUPPORTED`; AT11 `SUPPORTED` / `EXACT_SUPPORTED`; two fresh-process replays equal |

No test was edited, skipped or weakened. No failure was converted to a pass. The H03 A2 RED is outside this path and was not run here.

## Hostile coverage exercised by the 35-test higher-order court

| Attack / discriminator | Exact test | Observed |
|---|---|---|
| Wrong conditioning direction / wrong joint predicate | `test_at08_direct_two_conditioner_composition_requires_joint_predicate` | Passed; wrong predicate refused |
| Incompatible release context | `test_at08_incompatible_release_context_fails_closed` | Passed; refused |
| Incompatible universe context | `test_at08_incompatible_universe_context_fails_closed` | Passed; refused |
| Incompatible measure context | `test_at08_incompatible_measure_context_fails_closed` | Passed; refused |
| Marginal-only shortcut cannot represent joint | `test_at09_marginal_only_shortcut_cannot_represent_the_joint_outcome` | Passed; refused |
| Equal marginals, different joints | `test_at09_equal_marginals_different_joints_reidentify` | Passed; distinct identities |
| XOR joint signal | `test_at09_xor_unary_marginals_flat_but_joint_configuration_decisive` | Passed; joint preserved |
| Missing minority branch | `test_at10_minority_and_counterpattern_branches_are_supported`, `test_at10_minority_branch_survives_c1_composition`, `test_at10_no_supported_discovery_branch_is_silently_deleted` | Passed; 10/8/2 branches, no deletion |
| Broken recursive ancestry / wrong handoff predicate | `test_at11_recursive_handoff_rejects_predicate_mismatch`, `test_at11_lookalike_child_under_different_lineage_does_not_alias` | Passed; refused/anti-aliased |
| Recursive depth-two continuation | `test_at11_depth_two_continuation_reaches_the_recursive_owner_twice` | Passed; owner reached twice |
| Incomplete joint target/count mismatch | `test_at12_joint_target_count_mismatch_fails_closed`, `test_at13_witness_binding_count_mismatch_fails_closed` | Passed; refused |
| Same-respondent co-travel and no semantic-relation authority | `test_at12_cotravel_reaches_consumer_at_its_direct_empirical_grade`, `test_at12_lack_of_semantic_relation_authority_does_not_erase_cotravel` | Passed; co-travel retained, semantic authority absent |
| Non-scalar ranked component order | `test_at13_ranked_component_order_and_topology_are_preserved`, `test_at13_missing_component_vector_may_not_be_scalarized`, `test_at13_heterogeneous_component_authority_is_fail_closed_not_universal` | Passed; preserved/refused |
| Fabricated consumer input / preconstructed slice | `test_composer_has_no_preconstructed_possibility_slice_input`, `test_relation_guard_is_before_evidence_construction_and_consumer_invocation` | Passed; no bypass |
| Relation/denominator mismatch | `test_relation_mismatch_fails_before_evidence_and_consumer`, `test_r7_denominator_member_identity_hostile_preserves_visible_54_over_60` | Passed; refused/preserved |
| Stale dependency / replay invalidation | `test_pre553_analytical_replay_dependency.py` suite | 56 passed with the analytical composition court |

## Fresh-process replay

The H06 harness writes the recursive handoff bundle and invokes:

`python3 -m rawlsing_next.tests.c1_at08_at13_fresh_process_runner <bundle> <output>`

twice in separate processes. The two outputs are identical. Observed replay facts:

- `producer_route`: `MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT`
- `analytical_state`: `SUPPORTED`
- `coverage_state`: `RECURSIVE_DEPTH_CONTINUATION`
- `handoff_ref`: `3900f7b2cbc87c56b617548e7573ceb9a79527d2ed0475200fd553e1b640d577`
- `consumer_result_state`: `EXACT_SUPPORTED`

The receipt records both outputs under `replay.outputs` and `fresh_process_equal: true`.

## AT10 branch oracle

The AT10 product preserves the frozen fixture oracle:

- group sizes `A=10`, `B=8`, `C=2`;
- support counts `A=3`, `B=8`, `C=2`;
- modal, minority and counterpattern branches all supported;
- denominators and distinct composed identities retained.

No branch was pruned, pooled or replaced by the modal alternative.

## Skips / failures / limits

- Skips: none in the H06 selected suites.
- Failures: none in the H06 selected suites.
- A2 RED: not part of this path; not run here.
- No original survey, source-native I03, SAV, respondent corpus, source-native 35-wave run or native actor execution.
- No new semantic, model-use, pairing or actor authority.
- The 35/56 tests are existing owner courts; the H06 contribution is the independent receipt/replay execution, not new production semantics.
