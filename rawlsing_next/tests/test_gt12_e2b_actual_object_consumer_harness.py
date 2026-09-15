from __future__ import annotations

from dataclasses import replace
from itertools import product
import inspect

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.gt12_c_to_d_relation_bridge import GT12CToDBridgeError, admit_gt12_c_relation
from rawlsing_next.gt12_d_to_m4_typed_bridge import (
    GT12TypedBridgeError,
    publish_and_resolve_relation_v554_at_current_m4,
)
from rawlsing_next.gt12_permission_translation_authority import (
    ADOPTED_PRODUCER_ALLOWED_USES,
    ADOPTED_V557_ALLOWED_USES,
    ADOPTED_V558_REQUESTED_USES,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef as M4AuthorityRef,
    M4IntegrityError,
    PermissionWideningError,
    V557DecisionState,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.v3_psepf_zero_positive_guard import GuardOutcome
from rawlsing_next.tests import gt12_e2b_actual_object_consumer_harness as harness


def _h(label: str) -> str:
    return semantic_hash({"gt12-e2b-preflight": label})


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:gt12-e2b-preflight:{label}", _h(f"{kind}:{label}"))


def _auth(label: str) -> AuthorityRef:
    return AuthorityRef(f"GT12-E2B-{label}", "R1", _h(f"authority:{label}"))


def _m4_auth(label: str) -> M4AuthorityRef:
    return M4AuthorityRef(f"GT12-E2B-M4-{label}", "1.0.0", _h(f"m4:{label}"))


def _v554_rule() -> dict[str, str]:
    return {
        "id": "GT12-E2B-PREFLIGHT-V554-RULE",
        "version": "1.0.0",
        "hash": _h("v554-rule"),
    }


def _publication_authority(use: str) -> dict[str, object]:
    return {
        "authority_id": "GT12-E2B-PREFLIGHT-V557-PUBLICATION",
        "authority_version": "1.0.0",
        "authority_hash": _h("publication-authority"),
        "producer": "V554",
        "publisher": "V557",
        "governed_use_id": use,
        "rule_ref": _v554_rule(),
        "decision": "AUTHORIZED",
        "allowed_object_families": ["F1", "F2", "B1"],
    }


def _objects(*, fact_state: str = "SUPPORTED", reverse_targets: bool = False, wrong_risk: bool = False):
    conditioner = _ref("QUESTION", "Q86B")
    target = _ref("QUESTION", "Q86A")
    targets = (target, conditioner) if reverse_targets else (conditioner, target)
    c_domain, t_domain = ("0", "1"), ("1", "2")
    domain_by_ref = {
        conditioner: (c_domain, _ref("TARGET_DOMAIN", "Q86B")),
        target: (t_domain, _ref("TARGET_DOMAIN", "Q86A")),
    }
    auth = _auth("SOURCE")
    risk = (
        _ref("RISK_SET", "WRONG")
        if wrong_risk
        else ExactRef("RISK_SET", adm.GT2_RISK_SET_ID, adm.GT2_RISK_SET_MEMBER_SET_SHA256)
    )
    universe = _ref("UNIVERSE", "AFROBAROMETER-R5")
    predicate = _ref("PREDICATE", "FROZEN-RISK")
    response_semantics = _ref("RESPONSE_STATE_SEMANTICS", "Q86")
    measure = _ref("MEASURE_BASIS", "RAW")
    source = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, adm.GT2_SOURCE_SHA256)
    release = _ref("C11_RELEASE", "R5")

    components = []
    for ref in targets:
        domain, replay = domain_by_ref[ref]
        components.append({
            "target_ref": ref,
            "topology": "SCALAR_SINGULAR",
            "domain": domain,
            "target_domain_replay_ref": replay,
            "topology_authority_refs": (auth,),
            "response_semantic_authority_refs": (auth,),
            "included_states": ("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL"),
        })

    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(auth,),
        dependency_refs=(predicate, source),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "QUERY"),
        target_refs=targets,
        target_arity_and_topology={
            "arity": 2,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": tuple(components),
        },
        condition_predicate_ref=predicate,
        risk_set_ref=risk,
        empirical_universe_refs=(universe,),
        scope_refs=(universe,),
        measure_basis_ref=measure,
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE",
            "measure_kind": "RAW",
            "risk_set_type": "COMMON_ELIGIBLE_RISK_SET",
            "response_state_semantics_ref": response_semantics,
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(auth,),
    )

    domains = tuple(domain_by_ref[ref][0] for ref in targets)
    domain_identity = semantic_hash({
        "components": [
            {
                "target_ref": ref.as_dict(),
                "topology": "SCALAR_SINGULAR",
                "domain": list(domain_by_ref[ref][0]),
                "target_domain_replay_ref": domain_by_ref[ref][1].as_dict(),
            }
            for ref in targets
        ],
        "joint_order_semantics": "SEMANTIC_ORDERED",
        "full_domain": [list(cell) for cell in product(*domains)],
    })
    if fact_state == "SUPPORTED":
        counts = {cell: 0 for cell in product(*domains)}
        if reverse_targets:
            counts[next(iter(counts))] = adm.GT2_RISK_SET_ROWS
        else:
            counts.update({
                ("0", "1"): 5000,
                ("0", "2"): 4000,
                ("1", "1"): 6000,
                ("1", "2"): 4210,
            })
        denominator = numerator = adm.GT2_RISK_SET_ROWS
    elif fact_state == "OBSERVED_ZERO":
        counts = {cell: 0 for cell in product(*domains)}
        denominator, numerator = adm.GT2_RISK_SET_ROWS, 0
    else:
        counts = {cell: 0 for cell in product(*domains)}
        denominator = numerator = 0

    cells = [{
        "cell": list(cell),
        "cell_state": (
            "OBSERVED_POSITIVE" if counts[cell]
            else ("OBSERVED_ZERO_IN_SUPPORTED_RISK_SET" if denominator else "ZERO_SUPPORT")
        ),
        "raw_numerator_support": counts[cell],
        "weighted_numerator_support_if_authorized": None,
    } for cell in product(*domains)]

    replay = _ref("PRE553_I03_QUERY_REPLAY", "GT2")
    provenance = (source, release, universe)
    fact = EmpiricalFact(
        typed_state=fact_state,
        authority_snapshot_refs=(auth,),
        dependency_refs=(query.ref, predicate, replay, *provenance),
        producer_replay_locator_or_reference_root=replay,
        empirical_query_spec_ref=query.ref,
        empirical_universe_refs=(universe,),
        target_topology={
            "arity": 2,
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "target_domain_identity": domain_identity,
            "complete_cell_semantic_projection": cells,
        },
        condition_predicate_ref=predicate,
        risk_set_ref=risk,
        raw_numerator_support=numerator,
        raw_denominator_support=denominator,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=measure,
        response_state_semantics_ref=response_semantics,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
        source_empirical_provenance_refs=provenance,
        replay_ref=replay,
        query_execution_contract_id="PRE553_I03_EXACT_EMPIRICAL_QUERY@PREFLIGHT",
        execution_detail="synthetic ordinary PRE553 objects for E2B harness shape only; not current GT2 evidence",
        source_scope_mode="SINGLE_UNIVERSE",
        measure_kind="RAW",
        risk_set_type="COMMON_ELIGIBLE_RISK_SET",
        target_domain_identity=domain_identity,
        raw_resolved_target_support=numerator,
    )
    return query, fact, conditioner, target


def _run(query=None, fact=None, conditioner=None, target=None):
    if query is None or fact is None:
        query, fact, conditioner, target = _objects()
    use = "GT12_E2B_PREFLIGHT_STRUCTURAL_CONTEXT"
    return harness._run_bounded_chain(
        query,
        fact,
        governed_use_id=use,
        v554_rule_ref=_v554_rule(),
        publication_authority=_publication_authority(use),
        v557_authority_ref=_m4_auth("V557"),
        _expected_conditioner_ref=conditioner,
        _expected_target_ref=target,
    )


def test_future_real_entry_is_hard_current_r1c_boundary_and_synthetic_cannot_impersonate():
    query, fact, _, _ = _objects()
    assert query.content_hash not in {harness.CURRENT_R1C_QUERY_HASH, harness.HISTORICAL_A3_QUERY_HASH}
    assert fact.content_hash not in {harness.CURRENT_R1C_FACT_HASH, harness.HISTORICAL_A3_FACT_HASH}
    with pytest.raises(harness.GT12E2BHarnessError, match="current R1C query"):
        harness.require_current_r1c_actual_objects(query, fact)
    with pytest.raises(harness.GT12E2BHarnessError, match="historical A3"):
        harness._require_current_identity_values(
            query_hash=harness.HISTORICAL_A3_QUERY_HASH,
            fact_hash=harness.HISTORICAL_A3_FACT_HASH,
            replay_hash=harness.HISTORICAL_A3_REPLAY_HASH,
        )
    assert harness.REAL_CHAIN_STATE == "OPEN_PENDING_R4_ACTUAL_REPO_NATIVE_OBJECTS"


def test_future_real_entry_does_not_expose_permission_or_lane_selection():
    params = inspect.signature(harness.run_current_r1c_e2b_actual_objects).parameters
    for forbidden in (
        "producer_permission_ceiling", "relation_permission_ceiling",
        "permission_translation_authority_ref", "permission_translation_adoption_ref",
        "v557_allowed_uses", "requested_resolution_uses", "v557_decision_state",
        "producer_allowed_uses", "review", "active_causal",
    ):
        assert forbidden not in params


def test_synthetic_ordinary_objects_exercise_full_frozen_chain_to_exact_v3_zero_effect():
    result = _run()
    assert result.relation.family == ff.RELATION_FAMILY
    assert result.relation.semantic_owner == ff.SEMANTIC_OWNER
    assert result.relation.typed_state == "SUPPORTED"
    assert result.admission.decision is adm.AdmissionDecision.ADMITTED
    assert result.admission.target_use_permissions == (adm.GT2_TARGET_USE,)
    assert result.m1_evaluation.decision_state.value == "ELIGIBLE"
    assert result.m1_evaluation.direct_v557_handoff["route"] == "V554_TO_V557_DIRECT"
    terminal = result.v558_terminal
    assert {entry.obj.producer_family for entry in terminal.repository.entries} == {"V554"}
    assert all(entry.obj.producer_allowed_uses == ADOPTED_PRODUCER_ALLOWED_USES for entry in terminal.repository.entries)
    assert all(entry.governance.decision_state is V557DecisionState.ALLOW_CONTEXT_ONLY for entry in terminal.repository.entries)
    assert all(entry.governance.v557_allowed_uses == ADOPTED_V557_ALLOWED_USES for entry in terminal.repository.entries)
    assert all(item.resolver_allowed_uses == ADOPTED_V558_REQUESTED_USES for item in terminal.resolution.resolved_entries)
    assert terminal.resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    assert result.v3_decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert result.v3_decision.zero_effect is True


def test_wrong_semantic_order_and_risk_set_fail_closed():
    query, fact, conditioner, target = _objects(reverse_targets=True)
    with pytest.raises(ff.FieldForgeConditionalSupportError, match="target role/order"):
        _run(query, fact, conditioner, target)
    query, fact, conditioner, target = _objects(wrong_risk=True)
    with pytest.raises(GT12CToDBridgeError, match="risk-set"):
        _run(query, fact, conditioner, target)


def test_observed_zero_cannot_promote_to_positive_prev3_or_m1():
    query, fact, conditioner, target = _objects(fact_state="OBSERVED_ZERO")
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )
    admitted = admit_gt12_c_relation(relation)
    assert admitted.admission.decision is adm.AdmissionDecision.UNRESOLVED
    assert admitted.admission.target_use_permissions == ()
    with pytest.raises(harness.GT12E2BHarnessError, match="non-SUPPORTED"):
        _run(query, fact, conditioner, target)


def test_forbidden_substitute_lanes_permissions_and_actor_contamination_fail():
    result = _run()
    entry = result.v558_terminal.repository.entries[0]

    # These hostile mutations are rejected by stronger M4 integrity/permission
    # invariants before an inconsistent repository can reach terminal validation.
    for family in ("V553", "V555", "V556"):
        with pytest.raises(M4IntegrityError, match="producer locator"):
            replace(entry, obj=replace(entry.obj, producer_family=family))
    for uses in (("REVIEW",), ("ACTIVE_CAUSAL",), ("CONTEXT", "REVIEW")):
        with pytest.raises(PermissionWideningError, match="producer ceiling differs"):
            replace(entry, obj=replace(entry.obj, producer_allowed_uses=uses))
    with pytest.raises(M4IntegrityError, match="does not bind exact producer object"):
        replace(entry, obj=replace(entry.obj, semantic_class="ACTOR_STATE"))


def test_wrong_v557_and_v558_use_fail_terminal_validation():
    result = _run()
    with pytest.raises(GT12TypedBridgeError, match="ALLOW_CONTEXT_ONLY"):
        publish_and_resolve_relation_v554_at_current_m4(
            result.admission,
            result.m1_evaluation,
            v557_allowed_uses=("REVIEW",),
            requested_resolution_uses=("CONTEXT",),
            v557_authority_ref=_m4_auth("V557"),
            v557_decision_state=V557DecisionState.ALLOW_REVIEW_ONLY,
        )
    with pytest.raises(GT12TypedBridgeError, match="exact V558 requested uses"):
        publish_and_resolve_relation_v554_at_current_m4(
            result.admission,
            result.m1_evaluation,
            v557_allowed_uses=("CONTEXT",),
            requested_resolution_uses=("REVIEW",),
            v557_authority_ref=_m4_auth("V557"),
            v557_decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
        )


def test_wrong_permission_authority_is_rejected_by_frozen_lower_bridge():
    result = _run()
    with pytest.raises(GT12TypedBridgeError, match="translation authority"):
        publish_and_resolve_relation_v554_at_current_m4(
            result.admission,
            result.m1_evaluation,
            v557_allowed_uses=("CONTEXT",),
            requested_resolution_uses=("CONTEXT",),
            v557_authority_ref=_m4_auth("V557"),
            v557_decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
            permission_translation_authority_ref=_m4_auth("WRONG-PERMISSION"),
        )


def test_any_non_deny_v3_result_is_rejected(monkeypatch):
    query, fact, conditioner, target = _objects()

    class FakeDecision:
        outcome = GuardOutcome.DELEGATE_TO_ACCEPTED_OWNER
        zero_effect = True

    monkeypatch.setattr(harness, "evaluate_psepf_zero_positive_guard", lambda payload: FakeDecision())
    with pytest.raises(harness.GT12E2BHarnessError, match="DENY_ZERO_EFFECT"):
        _run(query, fact, conditioner, target)


@pytest.mark.parametrize("state", ["ZERO_SUPPORT", "VALID_EMPTY", "NONCOMPARABLE", "UNRESOLVED", "INTEGRITY_FAILURE"])
def test_other_nonpositive_states_never_reach_positive_chain(state):
    query, fact, conditioner, target = _objects(fact_state=state)
    with pytest.raises(harness.GT12E2BHarnessError, match="non-SUPPORTED"):
        _run(query, fact, conditioner, target)
