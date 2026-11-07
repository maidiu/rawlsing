# C4 independent review — commands and evidence

All commands ran from:
`/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-j-role-independent-review`

All outputs are confined to:
`WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C4_INDEPENDENT_REVIEW/`

No production, existing-test, author, HQ, peer, protected, original
respondent/SAV/DTA/DB, or raw-asset writes were made.

## Named O14 mechanism tests

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR='.../C4_INDEPENDENT_REVIEW/tmp' \
python3 -m pytest -q -p no:cacheprovider \
  --basetemp='.../C4_INDEPENDENT_REVIEW/tmp/pytest' \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h08_two_relation_components_certify_without_historical_executor \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h10_negative_role_authority_blocks_before_relation_promotion \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h11_changed_role_authority_blocks_and_changes_binding_identity \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h12_missing_successor_mapping_remains_unresolved_no_target_fallback \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h14_component_set_order_mismatch_is_integrity_failure \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_h15_serialized_role_vector_replay_mismatch_is_integrity_failure \
  rawlsing_next/tests/test_pre553_j_role_certification.py::test_exact_current_selection_authority_mismatch_rejected_by_registration
```

Result: **7 passed in 2.69s** (`02_FOCUSED_TEST_LOG.txt`).

These tests exercise the current sourcefree six-token J-role/M1 mechanism:
positive relation components, negative role, changed role authority, missing
successor mapping, component-set/order, replay mismatch, and current-selection
authority mismatch. They do not select an original J release or execute a
historical first reader.

## Source hashes and historical pins

Current source hashes (`04_SOURCE_PINS.txt`):

```text
838e123c3b73932105f3d78b091cac0714c47b9806d3db8630f5e01f4a594e41 pre553_j_role_certification.py
9cbe02009d8b6a0a5d1997462331650406863fc5c050716d935ca0b28d04876e pre553_component_authority_vector.py
40ce648ebb60e87eaab02f526f7c5fd9095d6a9d1e1e3712f0cdb4c2b17ea6a7 pre553_learned_empirical_adjudication.py
```

Historical pins at `9ba4764bef551b1ce498e5772d60b73d69337d4b` verify the author
table exactly:

```text
79dd8d82ccd49cb56d6417adfbceb1429206a9381c5fabd22e8eee37d71f9bbb compile_v551j_joint_evidence_packets.py
bad192143d33d0cce45196310a0afcbcf4b36a8526074866b84e1e44f9604841 ddm_v550j_joint_patterns.py
627f7094a70ad33652fba422536b776d32532b028c84e3fd543a453d25b4687a compile_v550j_joint_response_patterns.py
685fd557c6d430d192be8565a1ddc95497e44c678ef13a7127e8917f65a016d6 ddm_v550j_registry_contract.py
ba202f49bd843cd3be194d8a96765a2f25efc201a84f487ede15be6195ef5f00 compile_v552j_structural_handoff.py
3d16f43524cc68994a96a4ca43477f3ee7a5dd3d3f263f5551599327506db95e ddm_v550_shared_respondent_substrate.py
```

These are static source pins. They do not prove an original selected release,
historical execution, or historical effect/negative.

## Non-test caller and M1 registration search

`03_CALLER_AND_REGISTRATION_SEARCH.txt`:

- literal J role constructor/channel/validator search excluding tests returns
  only definitions in `pre553_j_role_certification.py` at 356, 567, 1257;
- the actual M1 registration builder is
  `build_j_validator_registry` at `pre553_j_role_certification.py:1018-1027`;
  it constructs `M1ValidatorRegistry` with
  `FamilyValidatorRegistration.from_binding(binding,
  j_component_certification_validator)`;
- `M1ValidatorRegistry` is exact, immutable, with no aliases/latest/default/
  fallback (`pre553_learned_empirical_adjudication.py:1112-1140`);
- `compose_learned_world` accepts a caller-supplied exact M1 registry on the
  M01_M1_M2_B5 route and passes it to `adjudicate_learned_empirical`
  (`pre553_learned_world_composition.py:1130,1175-1200`);
- no non-test invocation of `build_j_validator_registry` or J constructors was
  found statically.

Correct evidence label: **NONE_FOUND_IN_STATIC_SOURCE**, not proved absence.
The author’s narrow constructor grep did not cover the registration builder or
bare callable reference.

## Historical dynamic vs current six-token roles

The current O14 `ROLE_VOCABULARY` is six fixed tokens:
`exception_case`, `elective_case`, `social_condition`,
`family_size_condition`, `economic_condition`, `target_case`.

Pinned historical F17 source uses dynamic `family_cfg.item_role_groups`/order,
`target_resolution_rules`, `boundary_rules` and `response_role_rules`; F19
compiles family tables; F20 handles packet/readiness/typed stops; F21 performs
structural handoff. These are different responsibilities. The evidence does not
prove historical equivalence or show that current O14 must reproduce the full
dynamic J surface for an actual current operation. The author wording
“narrower” should be stated as “different responsibility; historical
equivalence UNPROVED; current J demand not established.”

## Bounded historical selection

No selected original J release/row/version reaches O14 in the evidence. The
candidate inputs AR-0051 draft, AR-0052/0053 rules, and AR-0058 conceptual are
not universal proof of absence. F1 callsite/source pins are static leads, not
proof of selected execution. Keep:
`STATIC_CALLSITE_ONLY__HISTORICAL_SELECTION_UNPROVED`,
`old_version_shadow_revoked=NOT_RUN__NO_SELECTED_J_RELEASE`, and
`proven_severance=false`. Do not turn missing current native J/S3 authority into
historical absence or a new gate.

## Test scope and limits

No full suite was repeated. This review ran the seven named O14 mechanism tests
and inspected the actual M1 registration/call-through and exact 9ba source pins.
The tests are sourcefree mechanism evidence only; no original J release,
respondent/SAV/DTA/DB bytes, native/science/actor/current authority, structural
admission, or protected receiving is established.
