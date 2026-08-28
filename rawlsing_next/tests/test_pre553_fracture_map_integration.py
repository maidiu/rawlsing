from __future__ import annotations

import pytest

from rawlsing_next.pre553_cosignature_composition import (
    BranchCosignatureContext,
    CosignatureCompositionPolicy,
    compose_branch_cosignatures,
)
from rawlsing_next.pre553_fracture_map_contract import (
    EmpiricalFractureMapReceipt,
    FractureMapControllerPolicy,
)
from rawlsing_next.pre553_empirical_objects import authority_ref, exact_ref
from rawlsing_next.pre553_fracture_map_controller import (
    FractureMapController,
    FractureMapControllerError,
    FractureMapReceiptAccumulator,
    OperationalRefEnvelope,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _build_source,
    _query_authority,
    _ref,
    _registry,
)


def _policy(tag: str = "z02") -> FractureMapControllerPolicy:
    authority = _auth(
        f"{tag}-policy",
        "FRACTURE_MAP_CONTROLLER_POLICY",
        families=("DiscoveryAuthority@1.0.0",),
    )
    return FractureMapControllerPolicy(
        policy_authority_ref=authority.authority_ref,
        policy_id=f"Z02_TEST_POLICY_{tag}",
        policy_version="1.0.0",
        minimum_split_raw_n=50,
        minimum_report_raw_n=25,
        maximum_depth=4,
    )


def test_controller_requires_i01_exact_policy_owner_and_emits_typed_stop_law():
    with pytest.raises(FractureMapControllerError, match="exact controller policy owner"):
        FractureMapController(policy=object())  # type: ignore[arg-type]

    source = _build_source("z02-stop", [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
    ])
    qauth = _query_authority("z02-stop-q")
    branch = _branch_predicate(source, qauth, tag="root")
    accumulator = FractureMapReceiptAccumulator(policy=_policy("stop"))
    controller = FractureMapController(policy=accumulator.policy, receipt_sink=accumulator)

    low = controller.continuation_decision(
        branch_predicate=branch,
        producer_state_bindings=((_ref("DISCOVERY_RESULT", "low"), "INSUFFICIENT_SUPPORT"),),
        raw_n=24,
        depth=0,
        remaining_candidates=3,
    )
    assert low.retention_disposition == "RETAIN_LOW_SUPPORT_STATE"
    assert low.continuation_disposition == "RETAIN_REPORT_ONLY_STOP"
    assert low.stop_reason == "LOW_N_OR_INSUFFICIENT_SUPPORT"
    assert low.controller_policy_ref == accumulator.policy.ref
    assert low.controller_policy_authority_ref == accumulator.policy.policy_authority_ref

    cont = controller.continuation_decision(
        branch_predicate=branch,
        producer_state_bindings=((_ref("DISCOVERY_RESULT", "supported"), "DISCOVERED_RESULT_SUPPORTED"),),
        raw_n=50,
        depth=1,
        remaining_candidates=2,
    )
    assert cont.retention_disposition == "RETAIN_EXACT_BRANCH"
    assert cont.continuation_disposition == "RETAIN_AND_CONTINUE_ELIGIBLE"
    assert cont.stop_reason == "NONE"


def test_i04_direct_j3_closure_wires_ref_only_into_i01_public_map_receipt():
    source = _build_source("z02-j3", [
        {"id": "R00", "responses": {"A": 0, "B": 0, "C": 0}},
        {"id": "R01", "responses": {"A": 0, "B": 1, "C": 1}},
        {"id": "R10", "responses": {"A": 1, "B": 0, "C": 1}},
        {"id": "R11", "responses": {"A": 1, "B": 1, "C": 0}},
    ])
    qauth = _query_authority("z02-j3-q", max_target_arity_J=3)
    branch = _branch_predicate(source, qauth, tag="branch")
    context = BranchCosignatureContext(
        branch_predicate=branch,
        branch_replay_ref=branch.predicate_ast["branch_membership_replay_ref"],
        immediate_parent_ref=branch.predicate_ast["parent_ancestry_ref"],
        ancestry_refs=(branch.predicate_ast["parent_ancestry_ref"],),
        source_release_refs=(source["release_ref"],),
        universe_refs=(source["universe"].ref,),
        risk_set_ref=source["risk_refs"]["R"],
    )
    composition_policy = CosignatureCompositionPolicy(
        topology_authority_ref=source["source_auth"].authority_ref,
        query_authority_refs=(qauth.authority_ref,),
        authority_maximum_target_arity_J=3,
        measure_kind="RAW",
        measure_basis_ref=_ref("MEASURE_BASIS", "RAW"),
        response_state_semantics_ref=_ref("RESPONSE_STATE_SEMANTICS", "SOURCE_NATIVE_TYPED_STATES"),
    )
    result = compose_branch_cosignatures(
        repository=source["repo"],
        context=context,
        authority_registry=_registry(source, qauth),
        policy=composition_policy,
    )
    assert len(result.marginal_queries) == 3
    assert len(result.joint_queries) == 3
    assert len(result.triple_queries) == 1
    triple = result.triple_queries[0].fact
    assert triple.target_topology["higher_order_evidence_semantics"] == (
        "DIRECT_EXACT_SAME_RESPONDENT_THREE_WAY_JOINT"
    )
    assert triple.target_topology["pairwise_projection_not_identity_equivalent"] is True
    assert result.closure_receipt.coverage_state == (
        "COMPLETE_FOR_AUTHORIZED_J1_TO_J3_TARGET_FRONTIER"
    )

    policy = _policy("receipt")
    accumulator = FractureMapReceiptAccumulator(policy=policy)
    envelope = OperationalRefEnvelope(
        controller_policy_id=policy.policy_id,
        controller_policy_ref=policy.ref,
        controller_policy_authority_ref=policy.policy_authority_ref,
        root_query_ref=result.marginal_queries[0].query.ref,
        parent_predicate_ref=branch.ref,
        source_release_refs=(source["release_ref"],),
        candidate_grammar_ref=_ref("PRE553_I05_CANDIDATE_GRAMMAR", "generation-0"),
        evaluated_frontier_ref=_ref("PRE553_I05_EVALUATED_FRONTIER", "generation-0"),
        discovery_authority_ref=_ref("DiscoveryAuthority@1.0.0", "generation-0"),
        receipt_refs=(_ref("DiscoveryResultReceipt@1.0.0", "generation-0"),),
        empirical_fact_refs=tuple(
            item.fact.ref
            for item in (
                *result.marginal_queries,
                *result.joint_queries,
                *result.triple_queries,
            )
        ),
        handoff_refs=(),
        depth=0,
    )
    accumulator.record(envelope)
    accumulator.record_cosignature_closure(result.closure_receipt.ref)
    decision = FractureMapController(
        policy=policy,
        receipt_sink=accumulator,
    ).continuation_decision(
        branch_predicate=branch,
        producer_state_bindings=((envelope.receipt_refs[0], "DISCOVERED_RESULT_SUPPORTED"),),
        raw_n=50,
        depth=0,
        remaining_candidates=1,
    )
    final_replay = _ref("PRE553_FRACTURE_MAP_REPLAY", "z02-final")
    receipt = accumulator.seal(
        root_query_ref=envelope.root_query_ref,
        branch_predicate_refs=(branch.ref,),
        branch_ancestry_refs=context.ancestry_refs,
        final_replay_ref=final_replay,
        additional_authority_snapshot_refs=(
            source["source_auth"].authority_ref,
            qauth.authority_ref,
        ),
    )
    assert isinstance(receipt, EmpiricalFractureMapReceipt)
    assert receipt.FAMILY == "EmpiricalFractureMapReceipt@1.0.0"
    assert exact_ref(receipt.controller_policy_ref) == policy.ref
    assert authority_ref(receipt.controller_policy_authority_ref) == policy.policy_authority_ref
    assert result.closure_receipt.ref in receipt.branch_cosignature_topology_closure_refs
    assert decision.ref in receipt.continuation_decision_refs
    assert triple.ref in receipt.empirical_fact_refs
    assert receipt.copied_empirical_payload is False
    assert receipt.actor_state_effect is False
    assert receipt.v3_state_effect is False
