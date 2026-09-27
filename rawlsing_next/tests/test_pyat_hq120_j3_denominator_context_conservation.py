from __future__ import annotations

from dataclasses import replace

import pytest

import rawlsing_next.pre553_learned_empirical_adjudication as m1
import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_component_authority_vector import (
    ComponentAuthorityBinding,
    authoritative_value_digest,
    build_component_authority_vector_receipt,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleExecutor,
)
from rawlsing_next.pre553_learned_product_release import (
    M2Repository,
    publish_binding,
    register_representation,
    resolve_release_exact,
)
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import _query
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding,
    _m1_authority,
    _receipt_with_fact,
    _registry,
    _validator,
)
from rawlsing_next.tests.test_pre553_learned_world_composition import (
    _contract,
    _disposition,
)
from rawlsing_next.tests.test_pre553_route_b_production import (
    _execute as execute_m01,
    _fixture as m01_fixture,
)


def _ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"court": "PYAT-HQ120-J3", "kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:j3:{kind.lower()}:{tag}:sha256:{digest}", digest)


def _component_vector(joint_fact: EmpiricalFact, joint_query: EmpiricalQuerySpec, source_authority: AuthorityRef):
    components = tuple(joint_query.target_arity_and_topology["components"])
    bindings = []
    for index, component in enumerate(components, start=1):
        target_ref = exact_ref(component["target_ref"], "component target ref")
        bindings.append(
            ComponentAuthorityBinding(
                component_id=f"J3-COMP-{index}",
                component_ref=target_ref,
                producer_family="RespondentEvent@1.0.0",
                role=f"JOINT_TARGET_COMPONENT_{index}",
                ordinal_or_null=index,
                multiplicity_index=0,
                authority_state="VALUE",
                authoritative_value_digest=authoritative_value_digest(
                    {"component": index, "target_ref": target_ref.as_dict()}
                ),
                value_authority_ref=source_authority,
            )
        )
    vector_rule = AuthorityRef(
        "MX02R2_J3_COMPONENT_VECTOR_RULE",
        "1.0.0",
        semantic_hash({"authority": "MX02R2_J3_COMPONENT_VECTOR_RULE", "v": "1.0.0"}),
    )
    return build_component_authority_vector_receipt(
        vector_subject_ref=joint_fact.ref,
        authority_dimension_contract_ref=_ref("ComponentDimensionContract", "j3"),
        vector_rule_authority_ref=vector_rule,
        governed_component_ids=tuple(binding.component_id for binding in bindings),
        component_bindings=tuple(bindings),
        producer_replay_locator_or_reference_root=_ref("ComponentVectorReplay", "j3"),
    )


def _j_shaped_m01():
    fx = m01_fixture()
    universe = fx["projection"].universes[0]
    source_view = {
        "universe": universe,
        "qrefs": fx["qrefs"],
        "risk_refs": {"R": fx["risk"]},
    }
    topology_authority = fx["projection"].questions[0].topology_authority_ref
    joint = _query(
        source_view,
        fx["qauth"],
        fx["all_p"],
        ("X", "Y"),
        risk="R",
        measure="RAW",
        tag="j3-joint",
        target_authority_refs=(topology_authority,),
    )
    grammar = _grammar(
        operation=fx["dauth"].governed_operations[0],
        atoms=[_atom("ALL", fx["all_p"], "BRANCH")],
        templates=[_qt("J", joint)],
        rules=[
            _rule(
                "j3-joint-cells",
                "BOUNDED_K_WAY_RESPONSE_CONFIGURATION",
                "BASE_QUERY",
                baseline_atom_id="ALL",
                query_template_id="J",
                target_cells=(("0", "0"), ("0", "1"), ("1", "0"), ("1", "1")),
                validation={"kind": "TARGET_CELL_SUPPORTED"},
            )
        ],
        k=2,
        j=2,
    )
    discovery = _discovery_authority(source_view, grammar, fx["dauth"], tag="j3")
    catalog = RuntimeObjectCatalog(
        authorities=fx["catalog"].authorities,
        predicates=(fx["all_p"],),
        queries=(joint,),
        discovery_authorities=(discovery,),
    )
    result = execute_m01(
        fx,
        catalog=catalog,
        requests=(I03ExecutionRequest(joint.ref, fx["all_p"].ref),),
        discovery_ref=discovery.ref,
    )
    supported = next(
        receipt for receipt in result.i05_result.receipts
        if receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    )
    role_query_ref = exact_ref(
        supported.candidate_identity["query_roles"][0]["query_ref"],
        "supported candidate query ref",
    )
    executed_joint = next(
        query for query in result.object_graph.executed_queries
        if query.ref == role_query_ref
    )
    fact_ref = exact_ref(supported.empirical_fact_refs[0], "supported fact ref")
    joint_fact = next(
        fact for fact in result.object_graph.empirical_facts
        if fact.ref == fact_ref
    )
    predicate = next(
        pred for pred in result.object_graph.executed_predicates
        if pred.ref == exact_ref(executed_joint.condition_predicate_ref)
    )
    return fx, result, supported, executed_joint, joint_fact, predicate


@pytest.fixture(scope="module")
def j3():
    fx, m01_result, receipt, joint_query, joint_fact, predicate = _j_shaped_m01()
    validator_auth = _m1_authority("j3")
    binding = _binding(validator_auth)
    vector = _component_vector(
        joint_fact,
        joint_query,
        fx["projection"].questions[0].semantic_authority_ref,
    )
    role_dependency_ref = _ref("JComponentRoleDependency", "non-scalar-role")
    contract = _contract(
        route="M01_M1_M2_B5",
        binding=binding,
        tag="j3",
    )
    repo = M2Repository()
    executor = LearnedProductLifecycleExecutor()
    result = i4.compose_learned_world(
        contract,
        m2_repository=repo,
        lifecycle_executor=executor,
        m01_result=m01_result,
        selected_discovery_receipt_refs=(receipt.ref,),
        requested_scope={"fixture": "J3_EXACT_J_SHAPED"},
        m1_family_rule_binding=binding,
        validator_registry=_registry(binding),
        m1_authority_snapshots=(validator_auth,),
        additional_dependency_refs=(vector.ref, role_dependency_ref),
    )
    assert result.receipt.terminal_state == "RULE_SATISFIED"
    return {
        "fx": fx,
        "m01": m01_result,
        "receipt": receipt,
        "query": joint_query,
        "fact": joint_fact,
        "predicate": predicate,
        "validator_auth": validator_auth,
        "binding": binding,
        "vector": vector,
        "role_ref": role_dependency_ref,
        "contract": contract,
        "repo": repo,
        "executor": executor,
        "result": result,
    }


def _denominator_refs(fact: EmpiricalFact) -> tuple[ExactRef, ...]:
    return tuple(exact_ref(value, "denominator member") for value in fact.denominator_member_refs)


def _risk_members(fact: EmpiricalFact) -> tuple[ExactRef, ...]:
    return tuple(exact_ref(value, "risk member") for value in fact.risk_set_member_refs)


def _mutated_fact(j3, *, tag: str, drop_denominator: bool = True) -> EmpiricalFact:
    fact = j3["fact"]
    fields = dict(fact.semantic_fields)
    old_denoms = list(_denominator_refs(fact))
    new_denoms = tuple(old_denoms[:-1] if drop_denominator and old_denoms else old_denoms)
    new_replay = _ref("PRE553_I03_QUERY_REPLAY", tag)
    fields["denominator_member_refs"] = new_denoms
    fields["raw_denominator_support"] = len(new_denoms)
    fields["raw_resolved_target_support"] = min(
        int(fields["raw_resolved_target_support"]), len(new_denoms)
    )
    fields["raw_numerator_support"] = min(
        int(fields["raw_numerator_support"]), len(new_denoms)
    )
    fields["replay_ref"] = new_replay
    deps = tuple(
        new_replay if ref == exact_ref(fact.replay_ref) else ref
        for ref in fact.dependency_refs
    )
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=new_replay,
        **fields,
    )


def _mutated_disposition(j3, *, tag: str = "mutated-denominator"):
    old = j3["fact"]
    new = _mutated_fact(j3, tag=tag)
    receipt = _receipt_with_fact(
        j3["receipt"], old, new, tag=f"{tag}-receipt"
    )
    facts = tuple(
        new if fact.ref == old.ref else fact
        for fact in j3["m01"].object_graph.empirical_facts
    )
    bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=j3["binding"].claim_family_id,
        requested_claim_rule_id=j3["binding"].claim_rule_id,
        selected_discovery_receipts=(receipt,),
        discovery_authority_catalog=j3["m01"].object_graph.discovery_authorities,
        empirical_fact_catalog=facts,
        empirical_query_catalog=j3["m01"].object_graph.executed_queries,
        empirical_predicate_catalog=j3["m01"].object_graph.executed_predicates,
        authority_snapshots=(
            *j3["m01"].object_graph.authority_snapshots,
            j3["validator_auth"],
        ),
        requested_scope={"fixture": "J3_MUTATED_DENOMINATOR"},
        additional_dependency_refs=(j3["vector"].ref, j3["role_ref"]),
    )
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        j3["binding"],
        validator_registry=_registry(j3["binding"]),
    )
    return new, receipt, bundle, disposition


def test_j3_h01_denominator_refs_preserved_m01_i03_to_m1(j3):
    fact = j3["fact"]
    disposition = j3["result"].m1_disposition
    assert fact.ref in disposition.empirical_fact_refs
    assert exact_ref(fact.risk_set_ref) in disposition.risk_set_refs
    assert fact.raw_denominator_support == len(_denominator_refs(fact))
    assert _denominator_refs(fact)


def test_j3_h02_risk_set_ref_preserved(j3):
    fact = j3["fact"]
    query = j3["query"]
    disposition = j3["result"].m1_disposition
    risk = exact_ref(fact.risk_set_ref)
    assert risk == exact_ref(query.risk_set_ref)
    assert risk in disposition.risk_set_refs


def test_j3_h03_same_respondent_premise_preserved(j3):
    assert j3["predicate"].same_respondent_binding_semantics == "EXACT_SCOPED_RESPONDENT"
    assert j3["predicate"].ref in j3["result"].m1_disposition.empirical_predicate_refs


def test_j3_h04_target_topology_and_order_preserved(j3):
    query = j3["query"]
    fact = j3["fact"]
    disposition = j3["result"].m1_disposition
    assert query.target_arity_and_topology["arity"] == 2
    assert query.target_arity_and_topology["joint_order_semantics"] == "SEMANTIC_ORDERED"
    assert fact.target_topology["arity"] == 2
    assert fact.target_topology["joint_order_semantics"] == "SEMANTIC_ORDERED"
    assert any(
        material.get("joint_order_semantics") == "SEMANTIC_ORDERED"
        for material in disposition.topology_scope_material
        if hasattr(material, "get")
    )


def test_j3_h05_component_vector_ref_is_exact_dependency(j3):
    disposition = j3["result"].m1_disposition
    assert j3["vector"].ref in disposition.dependency_refs
    assert j3["role_ref"] in disposition.dependency_refs


def test_j3_h06_context_dependency_preserved_m1_to_m2_dependency_closure(j3):
    disposition = j3["result"].m1_disposition
    closure = j3["result"].m2_artifacts.dependency_closure
    assert closure.member_refs == tuple(sorted(set(disposition.dependency_refs), key=lambda ref: ref.key))
    assert j3["fact"].ref in closure.member_refs
    assert j3["vector"].ref in closure.member_refs
    assert j3["role_ref"] in closure.member_refs


def test_j3_h07_determinant_identity_changes_with_denominator_context(j3):
    new_fact, _, _, changed = _mutated_disposition(j3)
    original = j3["result"].m1_disposition
    assert new_fact.ref != j3["fact"].ref
    assert _denominator_refs(new_fact) != _denominator_refs(j3["fact"])
    assert changed.determinant_manifest_ref != original.determinant_manifest_ref
    assert changed.ref != original.ref


def test_j3_h08_context_preserved_m2_to_b5_protocol(j3):
    result = j3["result"]
    assert result.b5_protocol_view.direct_dependency_refs == result.m2_artifacts.dependency_closure.member_refs
    assert j3["fact"].ref in result.b5_protocol_view.direct_dependency_refs
    assert j3["vector"].ref in result.b5_protocol_view.direct_dependency_refs
    assert result.b5_protocol_view.determinant_refs == result.m2_artifacts.determinant_closure.member_refs


def test_j3_h09_i4_receipt_points_to_exact_context_closures(j3):
    result = j3["result"]
    receipt = result.receipt
    assert receipt.m2_dependency_closure_ref == result.m2_artifacts.dependency_closure.ref
    assert receipt.m2_determinant_closure_ref == result.m2_artifacts.determinant_closure.ref
    assert receipt.determinant_root_ref == result.m1_disposition.determinant_manifest_ref
    assert receipt.replay_root_ref == result.m1_disposition.replay_ref


def test_j3_h10_final_exact_dereference_recovers_native_context(j3):
    result = j3["result"]
    dep = j3["repo"].closure_exact(result.receipt.m2_dependency_closure_ref)
    assert j3["fact"].ref in dep.member_refs
    assert j3["vector"].ref in dep.member_refs
    graph_facts = {fact.ref.key: fact for fact in j3["m01"].object_graph.empirical_facts}
    recovered = graph_facts[j3["fact"].ref.key]
    assert _denominator_refs(recovered) == _denominator_refs(j3["fact"])
    assert exact_ref(recovered.risk_set_ref) == exact_ref(j3["fact"].risk_set_ref)


def test_j3_h11_no_readiness_or_support_scalar_replaces_context(j3):
    closure = j3["result"].m2_artifacts.dependency_closure
    material = repr((closure.closure_kind, closure.member_refs, closure.metadata)).upper()
    assert j3["fact"].ref in closure.member_refs
    assert j3["vector"].ref in closure.member_refs
    assert "READINESS_SCORE" not in material
    assert "SUPPORT_SCORE" not in material


def test_j3_h12_denominator_is_exact_member_count_not_source_row_count(j3):
    fact = j3["fact"]
    assert fact.raw_denominator_support == len(_denominator_refs(fact))
    assert len(_risk_members(fact)) >= len(_denominator_refs(fact))
    assert "ROW_COUNT" not in repr(fact.semantic_fields).upper()


def test_j3_h13_missing_weight_never_defaults_to_one():
    fx = m01_fixture(missing_weight=True)
    result = execute_m01(fx)
    weighted = next(
        fact for fact in result.object_graph.empirical_facts
        if fact.measure_kind == "GOVERNED_WEIGHTED"
    )
    assert weighted.typed_state == "UNAVAILABLE"
    assert weighted.weighted_denominator_support_if_authorized is None
    assert "WEIGHT_MISSING" in weighted.execution_detail


def test_j3_h14_component_scalarization_requires_exact_vector_law(j3):
    assert j3["vector"].projection_disposition == "VECTOR_HETEROGENEOUS_COMPLETE"
    assert j3["vector"].scalar_value_digest is None
    target = exact_ref(j3["query"].target_arity_and_topology["components"][0]["target_ref"])
    digest = authoritative_value_digest({"same": "authorized"})
    rule = AuthorityRef(
        "MX02R2_J3_UNANIMOUS_RULE",
        "1.0.0",
        semantic_hash({"authority": "MX02R2_J3_UNANIMOUS_RULE"}),
    )
    unanimous = build_component_authority_vector_receipt(
        vector_subject_ref=j3["fact"].ref,
        authority_dimension_contract_ref=_ref("ComponentDimensionContract", "j3-unanimous"),
        vector_rule_authority_ref=rule,
        governed_component_ids=("A", "B"),
        component_bindings=(
            ComponentAuthorityBinding(
                "A", target, "RespondentEvent@1.0.0", "JOINT_COMPONENT", 1, 0,
                "VALUE", digest, j3["fx"]["projection"].questions[0].semantic_authority_ref,
            ),
            ComponentAuthorityBinding(
                "B", exact_ref(j3["query"].target_arity_and_topology["components"][1]["target_ref"]),
                "RespondentEvent@1.0.0", "JOINT_COMPONENT", 2, 0,
                "VALUE", digest, j3["fx"]["projection"].questions[0].semantic_authority_ref,
            ),
        ),
        producer_replay_locator_or_reference_root=_ref("ComponentVectorReplay", "j3-unanimous"),
    )
    assert unanimous.projection_disposition == "SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY"
    assert unanimous.scalar_value_digest == digest


def test_j3_h15_typed_valid_empty_blocked_and_review_like_states_survive():
    valid_empty, _, _ = _disposition("j3-valid-empty", valid_empty=True, outcome="ABSTAINED")
    valid_result = i4.compose_learned_world(
        _contract(tag="j3-valid-empty"),
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=valid_empty,
    )
    states = {
        row["state"] if isinstance(row, dict) else row["state"]
        for row in valid_result.receipt.conserved_state_material["conserved_empirical_states"]
    }
    assert "VALID_EMPTY" in states

    blocked, _, _ = _disposition("j3-blocked", channel_state="BLOCKED")
    blocked_result = i4.compose_learned_world(
        _contract(tag="j3-blocked"),
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=blocked,
    )
    assert blocked_result.receipt.terminal_state == "BLOCKED"
    assert "BLOCKED" in blocked_result.receipt.conserved_state_material["required_prerequisite_channel_states"].values()

    review_like, _, _ = _disposition("j3-review", channel_state="UNKNOWN")
    review_result = i4.compose_learned_world(
        _contract(tag="j3-review"),
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=review_like,
    )
    assert review_result.receipt.terminal_state == "UNRESOLVED"
    assert "UNKNOWN" in review_result.receipt.conserved_state_material["required_prerequisite_channel_states"].values()


def test_j3_h16_publication_and_current_selection_do_not_mutate_context(j3):
    contract = _contract(
        route="M1_M2_B5",
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="j3-lifecycle",
    )
    repo = M2Repository()
    executor = LearnedProductLifecycleExecutor()
    result = i4.compose_learned_world(
        contract,
        m2_repository=repo,
        lifecycle_executor=executor,
        m1_disposition=j3["result"].m1_disposition,
    )
    assert result.receipt.side_effects["b5_current_selection_effect"] is True
    assert result.b5_protocol_view.direct_dependency_refs == j3["result"].b5_protocol_view.direct_dependency_refs
    assert result.b5_protocol_view.determinant_refs == j3["result"].b5_protocol_view.determinant_refs


def test_j3_h17_m2_physical_relayout_does_not_mutate_context(j3):
    result = j3["result"]
    repo = j3["repo"]
    before = result.m2_artifacts.dependency_closure
    release = result.m2_artifacts.release
    locator = _ref("RepresentationLocator", "j3-relayout")
    integrity = _ref("RepresentationIntegrity", "j3-relayout")
    register_representation(
        repo,
        release_ref=release.ref,
        resolution_mode="DIRECT_PRODUCER_REF",
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
        resolved_subject_ref=release.release_subject_ref,
        producer_contract_ref=release.semantic_producer_contract_ref,
    )
    binding = publish_binding(
        repo,
        release_ref=release.ref,
        resolution_mode="DIRECT_PRODUCER_REF",
        resolver_or_locator_ref=locator,
        representation_integrity_ref=integrity,
    )
    resolved = resolve_release_exact(repo, release.ref, publication_binding_refs=(binding.ref,))
    after = repo.closure_exact(release.dependency_closure_ref)
    assert before.ref == after.ref
    assert before.member_refs == after.member_refs
    assert j3["fact"].ref in after.member_refs
    assert resolved.release_core.ref == release.ref


def test_j3_h18_tampered_denominator_fails_exact_m1_closure(j3):
    tampered = _mutated_fact(j3, tag="tamper")
    original_bundle = j3["result"].m1_input_bundle
    broken = m1.M1AdjudicationInputBundle(
        requested_claim_family_id=original_bundle.requested_claim_family_id,
        requested_claim_rule_id=original_bundle.requested_claim_rule_id,
        discovery_receipts=original_bundle.discovery_receipts,
        discovery_authorities=original_bundle.discovery_authorities,
        empirical_facts=(tampered,),
        empirical_queries=original_bundle.empirical_queries,
        empirical_predicates=original_bundle.empirical_predicates,
        authority_snapshots=original_bundle.authority_snapshots,
        evaluated_frontier_refs=original_bundle.evaluated_frontier_refs,
        discovery_replay_refs=original_bundle.discovery_replay_refs,
        requested_scope=original_bundle.requested_scope,
        prerequisite_channels=original_bundle.prerequisite_channels,
        additional_dependency_refs=original_bundle.additional_dependency_refs,
    )
    disposition = m1.adjudicate_learned_empirical(
        broken,
        j3["binding"],
        validator_registry=_registry(j3["binding"]),
    )
    assert disposition.adjudication_outcome == "INTEGRITY_FAILURE"


def test_j3_h19_unrelated_lifecycle_event_leaves_j_determinant_closure_unchanged(j3):
    before_ref = j3["result"].m2_artifacts.determinant_closure.ref
    before_members = j3["result"].m2_artifacts.determinant_closure.member_refs
    other_disposition, _, _ = _disposition("j3-unrelated")
    executor = LearnedProductLifecycleExecutor()
    i4.compose_learned_world(
        _contract(actions=("REGISTER",), tag="j3-unrelated"),
        m2_repository=M2Repository(),
        lifecycle_executor=executor,
        m1_disposition=other_disposition,
    )
    assert j3["result"].m2_artifacts.determinant_closure.ref == before_ref
    assert j3["result"].m2_artifacts.determinant_closure.member_refs == before_members


def test_j3_h20_no_field_forge_or_prev3_permission_implication(j3):
    effects = j3["result"].receipt.side_effects
    assert effects["consumer_permission_effect"] is False
    assert effects["structural_admission_effect"] is False
    assert effects["causal_truth_effect"] is False
    assert effects["field_forge_effect"] is False
    assert effects["actor_v3_effect"] is False
    assert j3["result"].receipt.semantic_ceiling == j3["result"].m1_disposition.semantic_ceiling
