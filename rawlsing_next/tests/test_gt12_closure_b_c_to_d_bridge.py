from __future__ import annotations

from dataclasses import replace
from itertools import product
import inspect

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as bridge
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.pre553_empirical_objects import AuthorityRef, EmpiricalFact, EmpiricalQuerySpec, ExactRef, semantic_hash


def _h(label: str) -> str:
    return semantic_hash({"gt12-closure-b": label})


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:gt12-closure-b:{label}", _h(label))


def _fixture(*, fact_state: str = "SUPPORTED", relation_permissions=None):
    conditioner = _ref("QUESTION", "Q86B")
    target = _ref("QUESTION", "Q86A")
    c_domain, t_domain = ("0", "1"), ("1", "2")
    auth = AuthorityRef("GT12-CLOSURE-B-SOURCE", "R1", _h("source-authority"))
    risk = ExactRef("RISK_SET", adm.GT2_RISK_SET_ID, adm.GT2_RISK_SET_MEMBER_SET_SHA256)
    universe = _ref("UNIVERSE", "AFROBAROMETER-R5")
    predicate = _ref("PREDICATE", "ALL-FROZEN-RISK-MEMBERS")
    response_semantics = _ref("RESPONSE_STATE_SEMANTICS", "Q86-SOURCE-NATIVE")
    measure = _ref("MEASURE_BASIS", "RAW")
    c_domain_ref, t_domain_ref = _ref("TARGET_DOMAIN", "Q86B-DOMAIN"), _ref("TARGET_DOMAIN", "Q86A-DOMAIN")
    source = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, adm.GT2_SOURCE_SHA256)
    release = _ref("C11_RELEASE", "R5-Q86")
    components = (
        {"target_ref": conditioner, "topology": "SCALAR_SINGULAR", "domain": c_domain, "target_domain_replay_ref": c_domain_ref,
         "topology_authority_refs": (auth,), "response_semantic_authority_refs": (auth,), "included_states": ("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL")},
        {"target_ref": target, "topology": "SCALAR_SINGULAR", "domain": t_domain, "target_domain_replay_ref": t_domain_ref,
         "topology_authority_refs": (auth,), "response_semantic_authority_refs": (auth,), "included_states": ("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL")},
    )
    query = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE", authority_snapshot_refs=(auth,), dependency_refs=(predicate, source),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "QUERY"), target_refs=(conditioner, target),
        target_arity_and_topology={"arity": 2, "joint_order_semantics": "SEMANTIC_ORDERED", "components": components},
        condition_predicate_ref=predicate, risk_set_ref=risk, empirical_universe_refs=(universe,), scope_refs=(universe,), measure_basis_ref=measure,
        requested_output_grain={"source_scope_mode": "SINGLE_UNIVERSE", "measure_kind": "RAW", "risk_set_type": "COMMON_ELIGIBLE_RISK_SET",
                                "response_state_semantics_ref": response_semantics, "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED"},
        query_authority_refs=(auth,),
    )
    domain_identity = semantic_hash({
        "components": [
            {"target_ref": conditioner.as_dict(), "topology": "SCALAR_SINGULAR", "domain": list(c_domain), "target_domain_replay_ref": c_domain_ref.as_dict()},
            {"target_ref": target.as_dict(), "topology": "SCALAR_SINGULAR", "domain": list(t_domain), "target_domain_replay_ref": t_domain_ref.as_dict()},
        ],
        "joint_order_semantics": "SEMANTIC_ORDERED", "full_domain": [list(v) for v in product(c_domain, t_domain)],
    })
    if fact_state == "SUPPORTED":
        counts = {("0", "1"): 5000, ("0", "2"): 4000, ("1", "1"): 6000, ("1", "2"): 4210}; denominator = numerator = adm.GT2_RISK_SET_ROWS
    elif fact_state == "OBSERVED_ZERO":
        counts = {cell: 0 for cell in product(c_domain, t_domain)}; denominator, numerator = adm.GT2_RISK_SET_ROWS, 0
    else:
        counts = {cell: 0 for cell in product(c_domain, t_domain)}; denominator = numerator = 0
    cells = [{"cell": list(cell), "cell_state": ("OBSERVED_POSITIVE" if counts[cell] else ("OBSERVED_ZERO_IN_SUPPORTED_RISK_SET" if denominator else "ZERO_SUPPORT")),
              "raw_numerator_support": counts[cell], "weighted_numerator_support_if_authorized": None} for cell in product(c_domain, t_domain)]
    replay = _ref("PRE553_I03_QUERY_REPLAY", "GT2")
    provenance = (source, release, universe)
    fact = EmpiricalFact(
        typed_state=fact_state, authority_snapshot_refs=(auth,), dependency_refs=(query.ref, predicate, replay, *provenance),
        producer_replay_locator_or_reference_root=replay, empirical_query_spec_ref=query.ref, empirical_universe_refs=(universe,),
        target_topology={"arity": 2, "joint_order_semantics": "SEMANTIC_ORDERED", "target_domain_identity": domain_identity,
                         "complete_cell_semantic_projection": cells}, condition_predicate_ref=predicate, risk_set_ref=risk,
        raw_numerator_support=numerator, raw_denominator_support=denominator, weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None, measure_basis_ref=measure, response_state_semantics_ref=response_semantics,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED", source_empirical_provenance_refs=provenance, replay_ref=replay,
        query_execution_contract_id="PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0",
        execution_detail="GT12 closure B exact typed fixture; not genuine execution evidence", source_scope_mode="SINGLE_UNIVERSE", measure_kind="RAW",
        risk_set_type="COMMON_ELIGIBLE_RISK_SET", target_domain_identity=domain_identity, raw_resolved_target_support=numerator,
    )
    producer_permissions = ("FIELD_FORGE_RELATION_PRODUCTION", adm.GT2_TARGET_USE)
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact, joint_query=query, conditioner_ref=conditioner, target_ref=target,
        producer_permission_ceiling=producer_permissions,
        relation_permission_ceiling=(adm.GT2_TARGET_USE,) if relation_permissions is None else relation_permissions,
    )
    return relation, fact


def test_actual_c_relation_admits_without_reownership_and_is_lossless():
    relation, _ = _fixture()
    result = bridge.admit_gt12_c_relation(relation)
    assert result.admission.decision is adm.AdmissionDecision.ADMITTED
    assert result.evidence.relation_ref == result.admission.relation_ref == relation.ref
    assert result.evidence.relation_owner == result.admission.relation_owner == ff.SEMANTIC_OWNER == adm.GT2_RELATION_OWNER
    assert result.admission.material()["owner"] == adm.OWNER != result.admission.relation_owner
    assert result.admission.target_use_permissions == (adm.GT2_TARGET_USE,)
    assert set(result.admission.target_use_permissions) <= set(relation.relation_permission_ceiling)
    assert [p.role for p in result.evidence.participants] == ["CONDITIONER", "TARGET"]
    assert [p.native_variable for p in result.evidence.participants] == ["Q86B", "Q86A"]
    assert [p.participant_ref for p in result.evidence.participants] == [relation.conditioner_ref, relation.target_ref]
    assert result.evidence.risk_set_ref == relation.risk_set_ref
    assert result.evidence.source_universe_refs == relation.empirical_universe_refs
    assert result.evidence.relation_authority_refs == relation.producer_authority_refs
    for ref in (relation.producer_fact_ref, relation.producer_query_ref, relation.producer_replay_ref, *relation.producer_provenance_refs):
        assert ref in result.evidence.relation_dependency_refs
    assert result.admission.relation_information_loss_declaration == result.admission.admission_information_loss_declaration == ff.INFORMATION_LOSS


def test_owner_substitution_is_rejected(monkeypatch):
    relation, _ = _fixture()
    monkeypatch.setattr(ff, "SEMANTIC_OWNER", "ATTACKER_REOWNER")
    with pytest.raises(bridge.GT12CToDBridgeError, match="owner substitution"):
        bridge.bridge_gt12_c_relation_to_d_evidence(relation)


def test_role_reversal_is_rejected_by_d_integrity():
    relation, _ = _fixture(); evidence = bridge.bridge_gt12_c_relation_to_d_evidence(relation); rule = bridge.make_gt12_c_to_d_admission_rule(relation)
    c, t = evidence.participants
    tampered = replace(evidence, participants=(replace(t, ordinal=0), replace(c, ordinal=1)))
    receipt = adm.evaluate_gt2_relation_admission(adm.RelationAdmissionRequest(tampered), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "PARTICIPANT_ROLE_ORDER_IDENTITY_MISMATCH"


def test_permission_widening_or_missing_permission_fails_closed():
    relation, _ = _fixture(); rule = bridge.make_gt12_c_to_d_admission_rule(relation)
    with pytest.raises(adm.RelationAdmissionError):
        replace(rule, output_permission_subset=(adm.GT2_TARGET_USE, "GENERAL_PREV3"))
    narrow, _ = _fixture(relation_permissions=("FIELD_FORGE_RELATION_PRODUCTION",))
    result = bridge.admit_gt12_c_relation(narrow)
    assert result.admission.decision is adm.AdmissionDecision.DENIED
    assert result.admission.target_use_permissions == ()


def test_ref_hash_rule_source_and_risk_tamper_fail_closed():
    relation, _ = _fixture(); object.__setattr__(relation, "content_hash", "0" * 64)
    with pytest.raises(bridge.GT12CToDBridgeError, match="hash"):
        bridge.bridge_gt12_c_relation_to_d_evidence(relation)
    relation, _ = _fixture(); evidence = bridge.bridge_gt12_c_relation_to_d_evidence(relation); rule = bridge.make_gt12_c_to_d_admission_rule(relation)
    other_rule = _ref("FIELD_FORGE_RELATION_RULE", "OTHER")
    receipt = adm.evaluate_gt2_relation_admission(adm.RelationAdmissionRequest(replace(evidence, relation_rule_ref=other_rule, relation_rule_content_hash_echo=other_rule.content_hash)), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE and receipt.reason_code == "RELATION_RULE_REF_MISMATCH"
    bad_source = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, _h("wrong-source"))
    receipt = adm.evaluate_gt2_relation_admission(adm.RelationAdmissionRequest(replace(evidence, source_artifact_ref=bad_source)), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE and receipt.reason_code == "SOURCE_ARTIFACT_IDENTITY_MISMATCH"
    bad_risk = ExactRef("RISK_SET", adm.GT2_RISK_SET_ID, _h("wrong-risk"))
    receipt = adm.evaluate_gt2_relation_admission(adm.RelationAdmissionRequest(replace(evidence, risk_set_ref=bad_risk)), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE and receipt.reason_code == "RISK_SET_IDENTITY_MISMATCH"


def test_c_observed_zero_blocker_cannot_be_laundered_to_admitted():
    relation, _ = _fixture(fact_state="OBSERVED_ZERO")
    assert relation.typed_state == "OBSERVED_ZERO" and relation.producer_state_blocking and not relation.conditional_count_profile
    result = bridge.admit_gt12_c_relation(relation)
    assert result.evidence.relation_typed_state == "OBSERVED_ZERO"
    assert result.evidence.relation_negative_or_limit_refs
    assert result.admission.decision is adm.AdmissionDecision.UNRESOLVED
    assert result.admission.reason_code == "UPSTREAM_RELATION_OBSERVED_ZERO"
    assert result.admission.target_use_permissions == ()
    assert result.admission.relation_typed_state == "OBSERVED_ZERO"


def test_c_observed_zero_remains_nonpositive_when_blocker_ref_is_stripped():
    relation, _ = _fixture(fact_state="OBSERVED_ZERO")
    evidence = bridge.bridge_gt12_c_relation_to_d_evidence(relation)
    rule = bridge.make_gt12_c_to_d_admission_rule(relation)
    assert evidence.relation_negative_or_limit_refs
    stripped = replace(evidence, relation_negative_or_limit_refs=())
    receipt = adm.evaluate_gt2_relation_admission(adm.RelationAdmissionRequest(stripped), rule)
    assert receipt.decision is adm.AdmissionDecision.UNRESOLVED
    assert receipt.reason_code == "UPSTREAM_RELATION_OBSERVED_ZERO"
    assert receipt.relation_typed_state == "OBSERVED_ZERO"
    assert receipt.target_use_permissions == ()
    assert receipt.applicable_negative_denial_noncomparability_refs == ()


def test_c_typed_state_tamper_changes_exact_identity_and_fails_bridge_closure():
    relation, _ = _fixture()
    original_ref = relation.ref
    object.__setattr__(relation, "typed_state", "OBSERVED_ZERO")
    assert semantic_hash(relation.semantic_projection()) != original_ref.content_hash
    with pytest.raises(bridge.GT12CToDBridgeError, match="hash"):
        bridge.bridge_gt12_c_relation_to_d_evidence(relation)


@pytest.mark.parametrize("state", ["VALID_EMPTY", "NONCOMPARABLE", "UNRESOLVED", "INTEGRITY_FAILURE"])
def test_other_typed_negatives_remain_nonpositive(state):
    relation, _ = _fixture(fact_state=state); result = bridge.admit_gt12_c_relation(relation)
    assert result.admission.decision is not adm.AdmissionDecision.ADMITTED
    assert result.admission.target_use_permissions == () and result.admission.relation_typed_state == state


def test_no_i04_empirical_fact_or_duck_coercion():
    _, fact = _fixture()
    with pytest.raises(bridge.GT12CToDBridgeTypeError): bridge.bridge_gt12_c_relation_to_d_evidence(fact)
    with pytest.raises(bridge.GT12CToDBridgeTypeError): bridge.bridge_gt12_c_relation_to_d_evidence(object())
    source = inspect.getsource(bridge)
    assert "pre553_structural_admission" not in source
    assert "evaluate_structural_empirical_admission" not in source
    assert "StructuralEmpiricalAdmission" not in source


def test_bridge_and_admission_replay_are_deterministic():
    relation, _ = _fixture(); first = bridge.admit_gt12_c_relation(relation); second = bridge.admit_gt12_c_relation(relation)
    assert first.evidence == second.evidence and first.rule.ref == second.rule.ref and first.admission.ref == second.admission.ref
    assert bridge.replay_gt12_c_to_d_admission(relation, first.admission).ref == first.admission.ref
