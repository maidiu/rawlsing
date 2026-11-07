# C4 test receipts

All commands run from `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer` with `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, and `TMPDIR`/`--basetemp` inside `C4_J_ROLE_FIRST_CONSUMER/tmp`.

## Non-test caller search

```bash
grep -RIn 'JFamilyRoleAssignment(\|build_j_family_item_role_vector(\|build_j_family_item_role_channel(\|j_component_certification_validator(' rawlsing_next --include='*.py' | grep -v '/tests/'
```

Observed prior narrow constructor search: only definitions inside `pre553_j_role_certification.py` (lines 356, 567, 1257). This log is preserved as a **historical incomplete search**; it omitted `build_j_validator_registry` and bare-callable registration.

Corrected C4-R1 evidence (from independent review, no new investigation):
- `build_j_validator_registry` at `pre553_j_role_certification.py:1018-1027` is an actual non-test M1 registration builder.
- It constructs `FamilyValidatorRegistration.from_binding(binding, j_component_certification_validator)` into an exact `M1ValidatorRegistry`.
- `M1ValidatorRegistry` is exact/immutable with no aliases/latest/default/fallback (`pre553_learned_empirical_adjudication.py:1112-1140`).
- `compose_learned_world` accepts the caller-supplied exact registry on the M01_M1_M2_B5 route and dispatches through M1.
- No non-test **invocation/call-through** of the registration builder or J constructors was found statically: `NONE_FOUND_IN_STATIC_SOURCE`, not proof of absence and not a generic producer finding.

## Named O14 mechanism tests

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR=... python3 -m pytest -q -p no:cacheprovider \
  --basetemp=.../tmp/pytest2 \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h08_two_relation_components_certify_without_historical_executor \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h10_negative_role_authority_blocks_before_relation_promotion \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h11_changed_role_authority_blocks_and_changes_binding_identity \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h12_missing_successor_mapping_remains_unresolved_no_target_fallback \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h14_component_set_order_mismatch_is_integrity_failure \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h15_serialized_role_vector_replay_mismatch_is_integrity_failure \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_exact_current_selection_authority_mismatch_rejected_by_registration
```

- Exit: `0`
- Result: `7 passed in 2.23s` (`logs/pytest_j_role_o14.log`; independent review 7 passed in 2.69s)
- Positive: h08 two relation components certify without historical executor.
- Negative: h10 negative role; h11 changed role authority; h12 missing successor mapping; h14 component-set/order; h15 serialized replay; exact current-selection authority mismatch.
- These are **current synthetic mechanism tests only**. They do not establish selected original J release, historical first reader, historical effects/negative rules, or a real non-test consumer.

## Source hashes

| Source | SHA-256 |
|---|---|
| `pre553_j_role_certification.py` | `838e123c3b73932105f3d78b091cac0714c47b9806d3db8630f5e01f4a594e41` |
| `pre553_component_authority_vector.py` | `9cbe02009d8b6a0a5d1997462331650406863fc5c050716d935ca0b28d04876e` |
| `pre553_learned_empirical_adjudication.py` | `40ce648ebb60e87eaab02f526f7c5fd9095d6a9d1e1e3712f0cdb4c2b17ea6a7` |
| historical `compile_v551j_joint_evidence_packets.py` @9ba | `79dd8d82ccd49cb56d6417adfbceb1429206a9381c5fabd22e8eee37d71f9bbb` |
| historical `ddm_v550j_joint_patterns.py` @9ba | `bad192143d33d0cce45196310a0afcbcf4b36a8526074866b84e1e44f9604841` |
| historical `compile_v550j_joint_response_patterns.py` @9ba | `627f7094a70ad33652fba422536b776d32532b028c84e3fd543a453d25b4687a` |
| historical `ddm_v550j_registry_contract.py` @9ba | `685fd557c6d430d192be8565a1ddc95497e44c678ef13a7127e8917f65a016d6` |
| historical `compile_v552j_structural_handoff.py` @9ba | `ba202f49bd843cd3be194d8a96765a2f25efc201a84f487ede15be6195ef5f00` |
| historical `ddm_v550_shared_respondent_substrate.py` @9ba | `3d16f43524cc68994a96a4ca43477f3ee7a5dd3d3f263f5551599327506db95e` |

## Output hashes

| Output | SHA-256 |
|---|---|
| `00_RETURN.md` | `744eaf6ecb3eab1baff8e4f8ee24732aeaf5b91290701851f41a28a6cfa5241d` |
| `01_CASES.jsonl` | `db426c5d26bba398a7fe32f77632d75cf58724a710c8fbb617f64b267f5c5117` |
| `02_CASES.tsv` | `2a35616f528b2a535ac7376f359ed0c7ccd7a5b3e515e6e4704cee767bb0c7b6` |
| `04_MINIMAL_OWNER_ACTIONS.tsv` | `b8cedc4e506310771380550f2ac2924471be68b1a4ccebd5908fa0645e762ec0` |
| `05_REGISTER_ANTIJOIN.tsv` | `d212bad2171ec66379ddb4d44eb6429fc9feb7c96571dd06f1c8f11afdb9e392` |
| `logs/pytest_j_role_o14.log` | `488b8212ba6338aaf0c98f27e098cbe13c33de80dc3e101c9fe8c1bf511d204d` |
| `logs/non_test_caller_search.txt` | `d06400b5d988bededcc75794ec988a606037dd8f1688ca5ed456e50e1b3efab2` |
| `06_REPORTING_CORRECTIONS.md` | `2e986a419e58855ead60fa3924df32b4c967854c452f027f826f6c13fe4e6161` |

`03_TEST_RECEIPTS.md` is this document and is not self-hashed.

## NOT_RUN / exact blockers

- Selected original J release/row: `NOT_RUN__NO_SELECTED_ORIGINAL_J_RELEASE`; historical static pins/calls are proved, but selected release is UNPROVED, not historical absence.
- Historical first-reader execution/effects: `NOT_RUN__STATIC_CALLSITE_ONLY`.
- Original old-version/shadow/revocation/scope at O14: `NOT_RUN__NO_SELECTED_J_RELEASE`; explicit, not an absence claim or new authority gate.
- Native/science/actor/current grant: `NOT_RUN`.
- No original respondent/SAV/DTA/DB read; no asset copy/upload; no production/test-existing/HQ/peer/protected writes.
- C3 FF/post-FF and Q86/T01/R9 owners untouched; F21/M3 handoff only.
