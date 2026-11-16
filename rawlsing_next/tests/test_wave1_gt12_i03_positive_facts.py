from dataclasses import replace

import pytest

import rawlsing_next.wave1_gt12_i03_positive_facts as gt12b
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, EmpiricalFact, exact_ref
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source,
    _h,
    _query_authority,
    _ref,
)


def _target_use_authority(source, tag, target_use_ref, operation):
    content_hash = _h(f"gt12b-target-use:{tag}")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"gt12b-target-use-{tag}"),
        authority_id=f"GT12B-TARGET-USE-{tag}",
        authority_version="1.0.0",
        authority_content_hash=content_hash,
        authority_kind="TARGET_USE_PERMISSION",
        decision_state="ALLOW",
        governed_operations=(operation,),
        governed_object_families=("EmpiricalFact@1.0.0",),
        scope_envelope={
            "source_universe_refs": (source["universe"].ref.as_dict(),),
            "target_use_refs": (target_use_ref.as_dict(),),
        },
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"gt12b-target-use-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", f"gt12b-target-use-{tag}"),
    )


def _fixture(monkeypatch, *, risk_sets=None):
    rows = [
        {"id": "R1", "responses": {"Q86A": 1, "Q86B": 0}},
        {"id": "R2", "responses": {"Q86A": 0, "Q86B": 1}},
        {"id": "R3", "responses": {"Q86A": 1, "Q86B": 1}},
    ]
    source = _build_source("gt12b-r5", rows, risk_sets=risk_sets)
    release = source["repo"].resolve_release_exact(source["release_ref"])

    # The positive execution test is deliberately a small nonauthoritative fixture.
    # Frozen-literal tests below separately pin the production R5 constants.
    monkeypatch.setattr(gt12b, "FROZEN_R5_SOURCE_SHA256", release.source_artifact_ref.content_hash)
    monkeypatch.setattr(gt12b, "FROZEN_RISK_SET_MEMBER_COUNT", 3)
    monkeypatch.setattr(gt12b, "FROZEN_RISK_MEMBER_SET_SHA256", _h("gt12b-fixture-risk-members"))

    query_auth = _query_authority("gt12b-r5")
    query_operation = tuple(query_auth.governed_operations)[0]
    gt1_use_ref = _ref("TARGET_USE", "gt12b-gt1")
    gt2_use_ref = _ref("TARGET_USE", "gt12b-gt2")
    gt1_use_operation = "GT12B-GT1-TARGET-USE"
    gt2_use_operation = "GT12B-GT2-TARGET-USE"
    gt1_use_auth = _target_use_authority(source, "GT1", gt1_use_ref, gt1_use_operation)
    gt2_use_auth = _target_use_authority(source, "GT2", gt2_use_ref, gt2_use_operation)

    q86a = gt12b.R5Q86TargetBinding(
        source_native_variable="Q86A",
        question_impl_id=gt12b.FROZEN_Q86A_QIMPL,
        current_source_structure_id=gt12b.FROZEN_Q86A_SOURCE_STRUCTURE,
        native_question_ref=source["qrefs"]["Q86A"],
        domain=("0", "1"),
        target_domain_replay_ref=_ref("TARGET_DOMAIN", "gt12b-q86a"),
        topology_authority_refs=(source["source_auth"].authority_ref,),
        response_semantic_authority_refs=(source["source_auth"].authority_ref,),
        included_states=("SUBSTANTIVE_RESPONSE",),
    )
    q86b = gt12b.R5Q86TargetBinding(
        source_native_variable="Q86B",
        question_impl_id=gt12b.FROZEN_Q86B_QIMPL,
        current_source_structure_id="cssu.r1.afrobarometer.r5.fixtureq86b",
        native_question_ref=source["qrefs"]["Q86B"],
        domain=("0", "1"),
        target_domain_replay_ref=_ref("TARGET_DOMAIN", "gt12b-q86b"),
        topology_authority_refs=(source["source_auth"].authority_ref,),
        response_semantic_authority_refs=(source["source_auth"].authority_ref,),
        included_states=("SUBSTANTIVE_RESPONSE",),
    )
    binding = gt12b.R5Q86I03ExecutionBinding(
        release_ref=release.release_ref,
        empirical_universe_ref=source["universe"].ref,
        risk_set_ref=source["risk_refs"]["R"],
        risk_set_identity=gt12b.FROZEN_RISK_SET_ID,
        risk_set_semantic_member_set_sha256=gt12b.FROZEN_RISK_MEMBER_SET_SHA256,
        response_state_semantics_ref=_ref("RESPONSE_STATE_SEMANTICS", "gt12b-source-native"),
        query_authority_ref=query_auth.authority_ref,
        gt1_query_operation=query_operation,
        gt2_query_operation=query_operation,
        gt1_target_use=gt12b.ExactTargetUseBinding(
            gt1_use_ref,
            gt1_use_auth.authority_ref,
            gt1_use_operation,
            gt12b.GT1_TARGET_USE_CEILING,
        ),
        gt2_target_use=gt12b.ExactTargetUseBinding(
            gt2_use_ref,
            gt2_use_auth.authority_ref,
            gt2_use_operation,
            "GT2_EMPIRICAL_JOINT_INPUT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION",
        ),
        q86a=q86a,
        q86b=q86b,
    )
    registry = AuthorityRegistry((*source["authorities"], query_auth, gt1_use_auth, gt2_use_auth))
    return source, release, binding, registry, query_auth, gt1_use_auth, gt2_use_auth


def test_frozen_production_literals_are_exact():
    assert gt12b.FROZEN_R5_SOURCE_SHA256 == "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
    assert gt12b.FROZEN_RISK_SET_ID == "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1"
    assert gt12b.FROZEN_RISK_SET_MEMBER_COUNT == 19_210
    assert gt12b.FROZEN_RISK_MEMBER_SET_SHA256 == "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
    assert gt12b.GT1_CLAIM_ID == "GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1"
    assert gt12b.GT2_CLAIM_ID == "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1"


def test_lawful_current_i03_fixture_yields_gt1_and_gt2_positive_empirical_facts_and_replays(monkeypatch):
    _, release, binding, registry, _, _, _ = _fixture(monkeypatch)

    gt1_plan = gt12b.build_gt1_q86a_i03_plan(
        release=release, binding=binding, authority_registry=registry
    )
    gt1 = gt12b.execute_gt12b_i03_plan(
        release=release, plan=gt1_plan, authority_registry=registry
    )
    assert isinstance(gt1.fact, EmpiricalFact)
    assert gt1.fact.typed_state == "SUPPORTED"
    assert gt1.fact.raw_denominator_support == 3
    assert binding.gt1_target_use.authority_ref in gt1.fact.authority_snapshot_refs
    assert gt1.plan.query.requested_output_grain["measure_kind"] == "RAW"
    assert gt1.plan.query.requested_output_grain["source_scope_mode"] == "SINGLE_UNIVERSE"
    assert gt1.plan.query.requested_output_grain["target_use_ref"] == binding.gt1_target_use.target_use_ref.as_dict()
    assert gt12b.replay_gt12b_i03_execution(
        release=release, execution=gt1, authority_registry=registry
    ) == gt1.result

    gt2_plan = gt12b.build_gt2_q86a_q86b_i03_plan(
        release=release, binding=binding, authority_registry=registry
    )
    target_refs = tuple(exact_ref(ref, "target") for ref in gt2_plan.query.target_refs)
    assert target_refs == (binding.q86b.native_question_ref, binding.q86a.native_question_ref)
    gt2 = gt12b.execute_gt12b_i03_plan(
        release=release, plan=gt2_plan, authority_registry=registry
    )
    assert isinstance(gt2.fact, EmpiricalFact)
    assert gt2.fact.typed_state == "SUPPORTED"
    assert gt2.fact.raw_denominator_support == 3
    assert gt2.fact.schema_id == "EmpiricalFact"
    assert gt12b.replay_gt12b_i03_execution(
        release=release, execution=gt2, authority_registry=registry
    ) == gt2.result


def test_domain_tamper_fails_closed_before_i03(monkeypatch):
    _, release, binding, registry, _, _, _ = _fixture(monkeypatch)
    bad = replace(binding, q86a=replace(binding.q86a, domain=("0",)))
    with pytest.raises(gt12b.GT12BI03BindingError, match="domain omits"):
        gt12b.build_gt1_q86a_i03_plan(
            release=release, binding=bad, authority_registry=registry
        )


def test_risk_set_ref_tamper_fails_closed(monkeypatch):
    _, release, binding, registry, _, _, _ = _fixture(monkeypatch)
    bad = replace(binding, risk_set_ref=_ref("RISK_SET", "wrong-gt12b-risk"))
    with pytest.raises(gt12b.GT12BI03BindingError, match="routing facts must cover"):
        gt12b.build_gt2_q86a_q86b_i03_plan(
            release=release, binding=bad, authority_registry=registry
        )


def test_q86a_q86b_jointability_requires_exact_common_routing_members(monkeypatch):
    risk_sets = {
        "R": {
            "Q86A": {"R1", "R2", "R3"},
            "Q86B": {"R1", "R2"},
        }
    }
    _, release, binding, registry, _, _, _ = _fixture(monkeypatch, risk_sets=risk_sets)
    with pytest.raises(gt12b.GT12BI03BindingError, match="eligible member sets differ"):
        gt12b.build_gt2_q86a_q86b_i03_plan(
            release=release, binding=binding, authority_registry=registry
        )


def test_missing_exact_query_authority_fails_closed(monkeypatch):
    source, release, binding, _, _, gt1_use_auth, gt2_use_auth = _fixture(monkeypatch)
    missing_query = AuthorityRegistry((*source["authorities"], gt1_use_auth, gt2_use_auth))
    with pytest.raises(gt12b.GT12BI03BindingError, match="query authority"):
        gt12b.build_gt1_q86a_i03_plan(
            release=release, binding=binding, authority_registry=missing_query
        )


def test_i03_typed_unavailable_is_preserved_when_target_source_authority_disappears_after_plan(monkeypatch):
    source, release, binding, registry, query_auth, gt1_use_auth, gt2_use_auth = _fixture(monkeypatch)
    plan = gt12b.build_gt1_q86a_i03_plan(
        release=release, binding=binding, authority_registry=registry
    )
    missing_source = AuthorityRegistry((
        *tuple(auth for auth in source["authorities"] if auth != source["source_auth"]),
        query_auth,
        gt1_use_auth,
        gt2_use_auth,
    ))
    execution = gt12b.execute_gt12b_i03_plan(
        release=release, plan=plan, authority_registry=missing_source
    )
    assert execution.fact.typed_state == "UNAVAILABLE"
    assert execution.fact.raw_denominator_support == 0


def test_gt1_permission_ceiling_cannot_widen(monkeypatch):
    _, release, binding, registry, _, _, _ = _fixture(monkeypatch)
    bad_use = replace(binding.gt1_target_use, permission_ceiling="GENERAL_STRUCTURAL_OR_ACTOR_USE")
    bad = replace(binding, gt1_target_use=bad_use)
    with pytest.raises(gt12b.GT12BI03BindingError, match="GT1 target-use permission ceiling drift"):
        gt12b.build_gt1_q86a_i03_plan(
            release=release, binding=bad, authority_registry=registry
        )
