from __future__ import annotations

import ast
import inspect
from dataclasses import replace

import pytest

import rawlsing_next.pre553_j_role_certification as j
import rawlsing_next.pre553_learned_empirical_adjudication as m1
from rawlsing_next.pre553_component_authority_vector import (
    ComponentAuthorityBinding,
    authoritative_value_digest,
    build_component_authority_vector_receipt,
    reload_component_authority_vector_receipt,
)
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _allowed_states,
    _coverage_contract,
)
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute as execute_m01,
    _fixture as m01_fixture,
)


def _snapshot(authority_id: str, tag: str) -> AuthoritySnapshot:
    base = _auth(
        tag,
        "TARGET_USE_PERMISSION",
        families=("EmpiricalFact@1.0.0",),
    )
    fields = dict(base.semantic_fields)
    fields.update({
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_content_hash": _h(f"j-authority:{authority_id}:{tag}"),
    })
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            base.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def _material(
    *,
    role_tag: str = "role-a",
    missing_mapping: frozenset[str] = frozenset(),
    negative_role: str | None = None,
):
    m01 = execute_m01(m01_fixture())
    role_authority = _snapshot(j.ROLE_AUTHORITY_ID, role_tag)
    validator_authority = _snapshot("PRE553-J-VALIDATOR-AUTHORITY", "validator")
    selection_authority = _snapshot("PRE553-J-CURRENT-SELECTION", "selection")
    subject_authority = _snapshot("CURRENT-JOINT-SUBJECT-AUTHORITY", "subject")
    evidence_authority = _snapshot("PRE553-J-EVIDENCE-AUTHORITY", "evidence")
    role_contract = _ref("J_ROLE_CONTRACT", "role-contract")
    mapping_contract = _ref("J_ROLE_MAPPING_CONTRACT", "mapping-contract")
    replay_contract = _ref("J_REPLAY_CONTRACT", "replay-contract")
    uncertainty_policy = _ref("J_UNCERTAINTY_POLICY", "uncertainty")
    subject = _ref("J_CURRENT_SUBJECT", "subject")
    component_ids = ("c1", "c2", "c3")
    component_refs = {
        component_id: _ref("J_COMPONENT", component_id)
        for component_id in component_ids
    }
    mapping_refs = {
        component_id: (
            None
            if component_id in missing_mapping
            else _ref("J_COMPONENT_MAPPING", component_id)
        )
        for component_id in component_ids
    }
    roles = {
        "c1": "target_case",
        "c2": "social_condition",
        "c3": "economic_condition",
    }
    assignments = []
    for ordinal, component_id in enumerate(component_ids, 1):
        state = "DENIED" if component_id == negative_role else "VALUE"
        assignments.append(
            j.JFamilyRoleAssignment(
                component_id=component_id,
                component_ref=component_refs[component_id],
                ordinal=ordinal,
                authority_state=state,
                role_token=roles[component_id] if state == "VALUE" else None,
                value_authority_ref=role_authority.authority_ref,
                succession_invoked=True,
                predecessor_current_mapping_ref=mapping_refs[component_id],
                dependency_refs=(
                    _ref("J_ROLE_DEPENDENCY", component_id),
                ),
                negative_or_limit_refs=(
                    (_ref("J_ROLE_DENIAL", component_id),)
                    if state == "DENIED"
                    else ()
                ),
            )
        )
    vector = j.build_j_family_item_role_vector(
        vector_subject_ref=subject,
        governed_component_ids=component_ids,
        role_contract_ref=role_contract,
        mapping_contract_ref=mapping_contract,
        role_authority_ref=role_authority.authority_ref,
        role_assignments=assignments,
        replay_contract_ref=replay_contract,
        dependency_refs=(_ref("J_ROLE_VECTOR_DEP", role_tag),),
    )
    return {
        "m01": m01,
        "role_authority": role_authority,
        "validator_authority": validator_authority,
        "selection_authority": selection_authority,
        "subject_authority": subject_authority,
        "evidence_authority": evidence_authority,
        "role_contract": role_contract,
        "mapping_contract": mapping_contract,
        "replay_contract": replay_contract,
        "uncertainty_policy": uncertainty_policy,
        "subject": subject,
        "component_ids": component_ids,
        "component_refs": component_refs,
        "mapping_refs": mapping_refs,
        "vector": vector,
    }


def _channel(
    material,
    *,
    vector=None,
    expected_ids=None,
    expected_role_authority=None,
    replay_refs=None,
):
    vector = material["vector"] if vector is None else vector
    expected_ids = (
        material["component_ids"] if expected_ids is None else expected_ids
    )
    role_authority = (
        material["role_authority"]
        if expected_role_authority is None
        else expected_role_authority
    )
    if replay_refs is None:
        replay_refs = (
            (
                vector.producer_replay_locator_or_reference_root,
            )
            if hasattr(vector, "producer_replay_locator_or_reference_root")
            else (
                material["vector"].producer_replay_locator_or_reference_root,
            )
        )
    mapping_refs = {
        component_id: material["mapping_refs"].get(component_id)
        for component_id in expected_ids
    }
    return j.build_j_family_item_role_channel(
        role_vector=vector,
        expected_subject_ref=material["subject"],
        expected_component_ids=expected_ids,
        role_contract_ref=material["role_contract"],
        mapping_contract_ref=material["mapping_contract"],
        expected_role_authority_ref=role_authority.authority_ref,
        current_subject_family_authority_ref=(
            material["subject_authority"].authority_ref
        ),
        component_mapping_refs=mapping_refs,
        succession_component_ids=expected_ids,
        replay_contract_ref=material["replay_contract"],
        replay_refs=replay_refs,
    )


def _premise(material, component_id: str, ordinal: int, mode: str):
    match = "ACCEPTED_MATCH"
    eligibility = "ELIGIBLE_RELATION"
    special = False
    explained = False
    if mode == "context":
        eligibility = "CONTEXT_OR_NONRELATION"
    elif mode == "special":
        match = "NO_ACCEPTED_MATCH"
        eligibility = "NOT_REQUIRED"
        special = True
    elif mode == "explained":
        match = "NO_ACCEPTED_MATCH"
        eligibility = "CONTEXT_OR_NONRELATION"
        explained = True
    elif mode == "ambiguous":
        match = "AMBIGUOUS_MATCH"
        eligibility = "CONTEXT_OR_NONRELATION"
    elif mode == "unresolved":
        match = "UNRESOLVED_MATCH"
        eligibility = "UNRESOLVED"
    elif mode != "relation":
        raise AssertionError(mode)
    return j.JComponentCertificationPremise(
        component_id=component_id,
        component_ref=material["component_refs"][component_id],
        ordinal=ordinal,
        evidence_match_disposition=match,
        relation_eligibility_disposition=eligibility,
        special_or_missing_response=special,
        governed_nonrelation_explained=explained,
        authority_refs=(material["evidence_authority"].authority_ref,),
        dependency_refs=(_ref("J_EVIDENCE_DEP", component_id + "-" + mode),),
        negative_or_limit_refs=(
            (_ref("J_EVIDENCE_LIMIT", component_id),)
            if mode in {"ambiguous", "unresolved"}
            else ()
        ),
    )


def _binding(
    material,
    *,
    role_authority=None,
    selection_authority=None,
):
    role_authority = (
        material["role_authority"]
        if role_authority is None
        else role_authority
    )
    selection_authority = (
        material["selection_authority"]
        if selection_authority is None
        else selection_authority
    )
    return j.build_j_family_rule_binding(
        validator_authority_ref=material["validator_authority"].authority_ref,
        current_selection_authority_ref=selection_authority.authority_ref,
        role_authority_ref=role_authority.authority_ref,
        role_contract_ref=material["role_contract"],
        mapping_contract_ref=material["mapping_contract"],
        uncertainty_policy_ref=material["uncertainty_policy"],
        replay_contract_ref=material["replay_contract"],
        allowed_input_object_families_and_states=_allowed_states(),
        required_coverage_strength=_coverage_contract(),
    )


def _bundle(material, channel, modes, *, binding=None, extra_authorities=()):
    m01_result = material["m01"]
    premises = tuple(
        _premise(material, component_id, ordinal, mode)
        for ordinal, (component_id, mode) in enumerate(
            zip(material["component_ids"], modes), 1
        )
    )
    scope = j.build_j_component_premise_scope(
        premises,
        base_scope={"fixture": "J_ROLE_CERTIFICATION_SOURCE_FREE"},
    )
    snapshots = (
        tuple(m01_result.object_graph.authority_snapshots)
        + (
            material["validator_authority"],
            material["selection_authority"],
            material["role_authority"],
            material["subject_authority"],
            material["evidence_authority"],
        )
        + tuple(extra_authorities)
    )
    return m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=j.CLAIM_FAMILY_ID,
        requested_claim_rule_id=j.CLAIM_RULE_ID,
        selected_discovery_receipts=m01_result.i05_result.receipts,
        discovery_authority_catalog=(
            m01_result.object_graph.discovery_authorities
        ),
        empirical_fact_catalog=m01_result.object_graph.empirical_facts,
        empirical_query_catalog=m01_result.object_graph.executed_queries,
        empirical_predicate_catalog=(
            m01_result.object_graph.executed_predicates
        ),
        authority_snapshots=snapshots,
        requested_scope=scope,
        prerequisite_channels=(channel,),
        additional_dependency_refs=(m01_result.c11_release.release_ref,),
    )


def _adjudicate(material, modes, *, channel=None, binding=None, registry=None):
    channel = _channel(material) if channel is None else channel
    binding = _binding(material) if binding is None else binding
    bundle = _bundle(material, channel, modes, binding=binding)
    registry = (
        j.build_j_validator_registry(binding)
        if registry is None
        else registry
    )
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=registry,
    )
    return disposition, bundle, binding, registry


def _determinant(disposition):
    return disposition.determinant_explanation_receipt.determinant_manifest[
        "validator_determinants"
    ]


def _manual_vector(material, bindings, tag: str):
    replay = _ref("J_MANUAL_ROLE_REPLAY", tag)
    vector = build_component_authority_vector_receipt(
        vector_subject_ref=material["subject"],
        authority_dimension_contract_ref=material["role_contract"],
        vector_rule_authority_ref=(
            material["role_authority"].authority_ref
        ),
        governed_component_ids=material["component_ids"],
        component_bindings=bindings,
        producer_replay_locator_or_reference_root=replay,
    )
    return vector, replay


def test_role_vector_reload_is_exact_and_role_metadata_is_nonsemantic():
    material = _material()
    vector = material["vector"]
    reloaded = reload_component_authority_vector_receipt(vector.as_dict())
    assert reloaded.ref == vector.ref
    assert reloaded.as_dict() == vector.as_dict()
    assert {
        binding.role for binding in vector.component_bindings
    } == {j.ROLE_BINDING_METADATA}
    assert {
        binding.authoritative_value_digest
        for binding in vector.component_bindings
    } == {
        authoritative_value_digest("target_case"),
        authoritative_value_digest("social_condition"),
        authoritative_value_digest("economic_condition"),
    }


def test_h01_relation_bearing_match_is_relation_component():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "relation")
    )
    det = _determinant(result)
    assert det["ordered_contributions"][0]["contribution_token"] == (
        "relation_component"
    )
    assert result.adjudication_outcome == "RULE_SATISFIED"


def test_h02_matched_context_is_context_not_relation():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "context")
    )
    det = _determinant(result)
    assert det["ordered_contributions"][2]["contribution_token"] == (
        "context_component"
    )
    assert det["relation_count"] == 2
    assert result.reason_code == "J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT"


def test_h03_special_missing_is_preserved_as_context_like():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "special")
    )
    det = _determinant(result)
    assert det["ordered_contributions"][2]["contribution_token"] == (
        "special_or_missing_component"
    )
    assert det["context_count"] == 1
    assert result.reason_code == "J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT"


def test_h04_explained_nonrelation_is_preserved_as_context_like():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "explained")
    )
    det = _determinant(result)
    assert det["ordered_contributions"][2]["contribution_token"] == (
        "explained_nonrelation_component"
    )
    assert det["context_count"] == 1


def test_h05_ambiguous_match_blocks_without_first_or_nearest_choice():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "ambiguous")
    )
    det = _determinant(result)
    assert det["ordered_contributions"][2]["contribution_token"] == (
        "blocked_component"
    )
    assert result.adjudication_outcome == "BLOCKED"
    assert result.reason_code == "J_AMBIGUOUS_COMPONENT_MATCH"


def test_h06_unresolved_match_stays_unresolved():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "unresolved")
    )
    det = _determinant(result)
    assert det["ordered_contributions"][2]["contribution_token"] == (
        "unresolved_component"
    )
    assert result.adjudication_outcome == "UNRESOLVED"
    assert result.reason_code == "J_COMPONENT_CONTRIBUTION_UNRESOLVED"


def test_h07_one_relation_component_does_not_certify_joint_relation():
    result, *_ = _adjudicate(
        _material(), ("relation", "context", "context")
    )
    assert result.adjudication_outcome == "RULE_NOT_SATISFIED"
    assert result.reason_code == "INSUFFICIENT_JOINT_RELATION_COMPONENTS"
    assert _determinant(result)["relation_count"] == 1


def test_h08_two_relation_components_certify_without_historical_executor():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "context")
    )
    assert result.adjudication_outcome == "RULE_SATISFIED"
    assert _determinant(result)["relation_count"] == 2


def test_h09_relation_plus_context_gets_exact_with_context_shape():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "context")
    )
    assert result.reason_code == "J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT"
    assert _determinant(result)["context_count"] == 1


def test_h10_negative_role_authority_blocks_before_relation_promotion():
    material = _material(negative_role="c1")
    channel = _channel(material)
    assert channel.state == "BLOCKED"
    assert channel.detail["terminal_reason_code"] == (
        "J_ROLE_PREREQUISITE_BLOCKED"
    )
    result, *_ = _adjudicate(
        material,
        ("relation", "relation", "relation"),
        channel=channel,
    )
    assert result.adjudication_outcome == "BLOCKED"
    assert result.reason_code == "J_ROLE_PREREQUISITE_BLOCKED"


def test_h11_changed_role_authority_blocks_and_changes_binding_identity():
    material = _material()
    changed_role = _snapshot(j.ROLE_AUTHORITY_ID, "role-b")
    channel = _channel(
        material,
        expected_role_authority=changed_role,
    )
    assert channel.state == "BLOCKED"
    binding_a = _binding(material)
    binding_b = _binding(material, role_authority=changed_role)
    assert binding_a.ref != binding_b.ref
    assert (
        binding_a.validator_contract_fingerprint
        != binding_b.validator_contract_fingerprint
    )
    registry = j.build_j_validator_registry(binding_a)
    with pytest.raises(m1.M1BlockedError):
        registry.resolve_exact(binding_b)


def test_h12_missing_successor_mapping_remains_unresolved_no_target_fallback():
    material = _material(missing_mapping=frozenset({"c1"}))
    vector = material["vector"]
    first = next(
        row for row in vector.component_bindings if row.component_id == "c1"
    )
    assert first.authority_state == "UNRESOLVED"
    assert first.authoritative_value_digest is None
    channel = _channel(material)
    assert channel.state == "UNRESOLVED"
    result, *_ = _adjudicate(
        material,
        ("relation", "relation", "relation"),
        channel=channel,
    )
    assert result.adjudication_outcome == "UNRESOLVED"
    assert result.reason_code == "J_ROLE_PREREQUISITE_UNRESOLVED"


def test_h13_unknown_positive_role_digest_is_integrity_failure_even_if_metadata_says_target():
    material = _material()
    bindings = []
    for ordinal, component_id in enumerate(material["component_ids"], 1):
        token = "unknown_role" if component_id == "c1" else (
            "social_condition" if component_id == "c2" else "economic_condition"
        )
        bindings.append(
            ComponentAuthorityBinding(
                component_id=component_id,
                component_ref=material["component_refs"][component_id],
                producer_family=j.ROLE_SUCCESSION_CONTRACT_ID,
                role=(
                    "target_case"
                    if component_id == "c1"
                    else j.ROLE_BINDING_METADATA
                ),
                ordinal_or_null=ordinal,
                multiplicity_index=0,
                authority_state="VALUE",
                authoritative_value_digest=authoritative_value_digest(token),
                value_authority_ref=(
                    material["role_authority"].authority_ref
                ),
            )
        )
    vector, replay = _manual_vector(material, bindings, "unknown-role")
    channel = _channel(material, vector=vector, replay_refs=(replay,))
    assert channel.state == "INTEGRITY_FAILURE"
    assert channel.detail["terminal_reason_code"] == (
        "UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE"
    )
    result, *_ = _adjudicate(
        material,
        ("relation", "relation", "relation"),
        channel=channel,
    )
    assert result.adjudication_outcome == "INTEGRITY_FAILURE"
    assert result.reason_code == "UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE"


def test_duplicate_role_binding_fails_closed():
    material = _material()
    bindings = []
    for ordinal, component_id in enumerate(material["component_ids"], 1):
        bindings.append(
            ComponentAuthorityBinding(
                component_id=component_id,
                component_ref=material["component_refs"][component_id],
                producer_family=j.ROLE_SUCCESSION_CONTRACT_ID,
                role=j.ROLE_BINDING_METADATA,
                ordinal_or_null=ordinal,
                multiplicity_index=0,
                authority_state="VALUE",
                authoritative_value_digest=authoritative_value_digest(
                    "target_case"
                    if component_id == "c1"
                    else (
                        "social_condition"
                        if component_id == "c2"
                        else "economic_condition"
                    )
                ),
                value_authority_ref=material["role_authority"].authority_ref,
            )
        )
    bindings.append(
        replace(bindings[0], multiplicity_index=1)
    )
    vector, replay = _manual_vector(material, bindings, "duplicate-role")
    channel = _channel(material, vector=vector, replay_refs=(replay,))
    assert channel.state == "BLOCKED"
    assert channel.detail["terminal_reason_code"] == (
        "J_ROLE_PREREQUISITE_BLOCKED"
    )


def test_h14_component_set_order_mismatch_is_integrity_failure():
    material = _material()
    reversed_ids = tuple(reversed(material["component_ids"]))
    channel = _channel(material, expected_ids=reversed_ids)
    assert channel.state == "INTEGRITY_FAILURE"
    assert channel.detail["terminal_reason_code"] == (
        "J_COMPONENT_SET_MISMATCH"
    )
    result, *_ = _adjudicate(
        material,
        ("relation", "relation", "relation"),
        channel=channel,
    )
    assert result.adjudication_outcome == "INTEGRITY_FAILURE"
    assert result.reason_code == "J_COMPONENT_SET_MISMATCH"


def test_h15_serialized_role_vector_replay_mismatch_is_integrity_failure():
    material = _material()
    serialized = material["vector"].as_dict()
    serialized["coverage_proof_hash"] = "0" * 64
    channel = _channel(material, vector=serialized)
    assert channel.state == "INTEGRITY_FAILURE"
    assert channel.detail["terminal_reason_code"] == (
        "J_ROLE_VECTOR_REPLAY_MISMATCH"
    )


def test_exact_validator_registration_mismatch_rejected():
    material = _material()
    binding = _binding(material)
    registry = j.build_j_validator_registry(binding)
    wrong = replace(
        binding,
        validator_parameters_ref=_ref(
            "M1ValidatorParameters", "wrong-j-params"
        ),
    )
    with pytest.raises(m1.M1BlockedError):
        registry.resolve_exact(wrong)


def test_exact_current_selection_authority_mismatch_rejected_by_registration():
    material = _material()
    binding_a = _binding(material)
    changed_selection = _snapshot(
        "PRE553-J-CURRENT-SELECTION", "selection-b"
    )
    binding_b = _binding(
        material, selection_authority=changed_selection
    )
    assert (
        binding_a.validator_contract_fingerprint
        != binding_b.validator_contract_fingerprint
    )
    registry = j.build_j_validator_registry(binding_a)
    with pytest.raises(m1.M1BlockedError):
        registry.resolve_exact(binding_b)


def test_deterministic_m1_replay_equality_and_exact_determinant_shape():
    material = _material()
    channel = _channel(material)
    binding = _binding(material)
    bundle = _bundle(
        material,
        channel,
        ("relation", "relation", "context"),
        binding=binding,
    )
    registry = j.build_j_validator_registry(binding)
    first = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=registry
    )
    second = m1.adjudicate_learned_empirical(
        bundle, binding, validator_registry=registry
    )
    assert first.ref == second.ref
    assert first.replay_ref == second.replay_ref
    assert (
        first.determinant_explanation_receipt.as_dict()
        == second.determinant_explanation_receipt.as_dict()
    )
    det = _determinant(first)
    assert set(det) == {
        "ordered_contributions",
        "relation_count",
        "context_count",
        "blocked_count",
        "unresolved_count",
        "role_vector_ref",
        "role_vector_coverage_proof_hash",
        "contribution_rule_id",
        "prerequisite_channel_ref",
        "replay_contract_ref",
    }
    assert [row["ordinal"] for row in det["ordered_contributions"]] == [
        1,
        2,
        3,
    ]


def test_two_relation_components_without_context_get_exact_relation_only_shape():
    material = _material()
    # Use only two governed components to exercise exact no-context branch.
    ids = ("c1", "c2")
    assignments = []
    for ordinal, component_id in enumerate(ids, 1):
        assignments.append(
            j.JFamilyRoleAssignment(
                component_id=component_id,
                component_ref=material["component_refs"][component_id],
                ordinal=ordinal,
                authority_state="VALUE",
                role_token=(
                    "target_case"
                    if component_id == "c1"
                    else "social_condition"
                ),
                value_authority_ref=(
                    material["role_authority"].authority_ref
                ),
                succession_invoked=True,
                predecessor_current_mapping_ref=(
                    material["mapping_refs"][component_id]
                ),
            )
        )
    vector = j.build_j_family_item_role_vector(
        vector_subject_ref=material["subject"],
        governed_component_ids=ids,
        role_contract_ref=material["role_contract"],
        mapping_contract_ref=material["mapping_contract"],
        role_authority_ref=material["role_authority"].authority_ref,
        role_assignments=assignments,
        replay_contract_ref=material["replay_contract"],
    )
    material = dict(material)
    material["component_ids"] = ids
    material["vector"] = vector
    material["mapping_refs"] = {
        component_id: material["mapping_refs"][component_id]
        for component_id in ids
    }
    channel = _channel(material)
    result, *_ = _adjudicate(
        material,
        ("relation", "relation"),
        channel=channel,
    )
    assert result.adjudication_outcome == "RULE_SATISFIED"
    assert result.reason_code == "J_JOINT_RELATION_EVIDENCE"
    assert _determinant(result)["context_count"] == 0


def test_zero_downstream_effects_and_no_forbidden_dependencies_or_source_access():
    result, *_ = _adjudicate(
        _material(), ("relation", "relation", "context")
    )
    assert dict(result.effects) == dict(m1._FALSE_EFFECTS)

    tree = ast.parse(inspect.getsource(j))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    forbidden = (
        "field_forge",
        "learned_product_lifecycle",
        "ddm_v550j",
        "ddm_v551j",
        "ddm_v552j",
        "pyreadstat",
        "pandas",
    )
    assert not any(
        token in module
        for module in imports
        for token in forbidden
    )
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }
    assert "open" not in calls
