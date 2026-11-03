from __future__ import annotations

from copy import deepcopy

import pytest

import firstclass
from candidate import ResponseStatus, TargetBranch, TargetReason
from candidate.response_rules import DEFAULT_ISSUED_RESPONSE_RULES
from candidate.target_rules import DEFAULT_ISSUED_TARGET_RULES
from r31j.scenarios import evaluated

from bridge import access
from bridge.readback import cold_verify
from bridge.world import S35World


def _case(share: bool) -> dict:
    return evaluated(share=share, e2=False)["case"]


@pytest.fixture
def share_world(tmp_path):
    case = _case(True)
    world = S35World.build(tmp_path / "share-world", case=case)
    try:
        yield world, case
    finally:
        world.close()


@pytest.fixture
def refuse_world(tmp_path):
    case = _case(False)
    world = S35World.build(tmp_path / "refuse-world", case=case)
    try:
        yield world, case
    finally:
        world.close()


def _assert_positive(run):
    assert run.committed is True
    assert run.refused is False
    assert run.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert run.response.reason == access.OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    assert run.response.target_proposals == ()
    assert run.decision.branch is TargetBranch.NO_CHANGE
    assert run.decision.reason is TargetReason.NO_PROPOSAL
    assert run.decision.target_id == ""
    assert run.target_state_rows == 0
    assert run.target_ids == ()
    assert run.receipt["outcome"] == access.OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    assert run.receipt["target_proposals"] == []
    assert run.receipt["objective_material_implies_uptake"] is False
    assert run.receipt["native"] is False


def _assert_valid_empty(run, outcome: str):
    assert run.committed is True
    assert run.refused is False
    assert run.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
    assert run.response.reason == outcome
    assert run.response.target_proposals == ()
    assert run.decision.branch is TargetBranch.NO_CHANGE
    assert run.decision.reason is TargetReason.NO_PROPOSAL
    assert run.decision.target_id == ""
    assert run.target_state_rows == 0
    assert run.receipt["outcome"] == outcome
    assert run.receipt["target_proposals"] == []


def _same_world(world, run):
    context = world.context
    assert run.context == context
    assert run.receipt["root_id"] == context.root_id
    assert run.receipt["root_branch_hash"] == context.root_branch_hash
    assert run.receipt["root_state_hash"] == context.root_state_hash
    assert run.receipt["branch_id"] == context.branch_id
    assert run.receipt["branch_hash"] == context.branch_hash
    assert run.receipt["branch_parent_id"] == context.branch_parent_id
    assert run.receipt["branch_fork_clock"] == context.branch_fork_clock
    assert run.receipt["clock"] == context.clock


def test_m35_exact_source_validation_and_lawful_change():
    case = _case(True)
    source = firstclass.source_from_case(case)
    typed = firstclass.validate_source(source, case)
    assert typed["b_operation"] == "SHARE_TOOL"
    assert typed["b_quantity"] == 1
    assert typed["b_performed"] is True
    for field, value in (
        ("b_owner", "TEST_ONLY_OTHER_OWNER"),
        ("b_event_ref", "TEST_ONLY_EVENT_OTHER"),
        ("b_event_hash", "1" * 64),
        ("b_quantity", 2),
        ("b_clock", 6),
        ("b_to_actor", "TEST_ONLY_OTHER_A"),
        ("a_e1_ref", "TEST_ONLY_EVENT_OTHER_E1"),
        ("a_e1_hash", "0" * 64),
        ("a_e1_clock", 7),
    ):
        mutated = dict(source)
        mutated[field] = value
        with pytest.raises(firstclass.MaterialSourceRefusal) as caught:
            firstclass.validate_source(mutated, case)
        assert caught.value.code == "MATERIAL_SOURCE_PREIMAGE_MISMATCH"
    wrong_operation = dict(source)
    wrong_operation["b_operation"] = "REFUSE_TOOL"
    with pytest.raises(firstclass.MaterialSourceRefusal):
        firstclass.validate_source(wrong_operation, case)
    refuse_case = _case(False)
    refuse_source = firstclass.source_from_case(refuse_case)
    assert firstclass.validate_source(refuse_source, refuse_case)["b_operation"] == (
        "REFUSE_TOOL"
    )


def test_p1_positive_zero_target_and_cold_readback(share_world):
    world, _ = share_world
    run = world.evaluate("p1")
    _assert_positive(run)
    _same_world(world, run)
    assert run.receipt["response_kind"] == "REQUEST_TOOL"
    assert run.receipt["response_performed"] is True
    assert run.receipt["access_status"] == "ACCESSIBLE"
    assert run.receipt["access_time"] == world.context.event_time
    assert run.receipt["response_time"] == world.context.event_time + 1
    assert run.receipt["objective_material_eligible"] is True
    assert run.receipt["objective_material_refs"]
    assert run.response.eligible_material_refs == world.eligible_material_refs
    cold = cold_verify(world.root, "p1")
    assert cold["ok"], cold["checks"]
    assert cold["observed"]["target_state_rows"] == 0


def test_access_severance_same_world_and_restoration(share_world):
    world, _ = share_world
    baseline = world.evaluate("access-baseline")
    fault = world.evaluate("access-fault", access_witness=None)
    restored = world.evaluate("access-restored")
    _assert_positive(baseline)
    _assert_valid_empty(fault, access.UNKNOWN_RECEIVABILITY)
    _assert_positive(restored)
    for run in (baseline, fault, restored):
        _same_world(world, run)
    assert fault.receipt["objective_material_eligible"] is True
    assert fault.receipt["access_source_ref"] == ""
    assert fault.receipt["objective_material_implies_uptake"] is False
    assert cold_verify(world.root, "access-fault")["ok"]
    assert cold_verify(world.root, "access-restored")["ok"]


def test_request_severance_same_world_and_restoration(share_world):
    world, _ = share_world
    baseline = world.evaluate("request-baseline")
    fault = world.evaluate("request-fault", response_witness=None)
    restored = world.evaluate("request-restored")
    _assert_positive(baseline)
    _assert_valid_empty(fault, access.RECEIVABLE_NO_OBSERVED_UPTAKE)
    _assert_positive(restored)
    for run in (baseline, fault, restored):
        _same_world(world, run)
    assert fault.receipt["access_status"] == "ACCESSIBLE"
    assert fault.receipt["response_ref"] == ""
    assert cold_verify(world.root, "request-fault")["ok"]
    assert cold_verify(world.root, "request-restored")["ok"]


def test_contradictory_context_valid_empty_and_unbound_refusal(share_world):
    world, _ = share_world
    contradictory = world.evaluate(
        "contradictory",
        response_witness=None,
        contradictory_context=True,
        contradictory_refs=("TEST_ONLY_S35_CONTRADICTION_A",),
    )
    _assert_valid_empty(contradictory, access.AMBIGUOUS_CONTRADICTORY)
    assert contradictory.receipt["contradictory_context"] is True
    assert contradictory.receipt["contradictory_refs"] == [
        "TEST_ONLY_S35_CONTRADICTION_A"
    ]
    unbound = world.evaluate(
        "contradictory-unbound",
        response_witness=None,
        contradictory_context=True,
    )
    assert unbound.refused is True
    assert unbound.committed is False
    assert unbound.response.status is ResponseStatus.REFUSED
    assert unbound.refusal_reason == "S35_CONTRADICTORY_CONTEXT_UNBOUND"
    assert not (unbound.run_dir / "c9.sqlite").exists()
    assert cold_verify(world.root, "contradictory")["ok"]
    assert cold_verify(world.root, "contradictory-unbound")["ok"]


@pytest.mark.parametrize(
    "field,value",
    (
        ("root_id", "TEST_ONLY_FOREIGN_ROOT"),
        ("root_branch_hash", "f" * 64),
        ("root_state_hash", "e" * 64),
        ("branch_id", "TEST_ONLY_FOREIGN_BRANCH"),
        ("branch_hash", "d" * 64),
        ("branch_parent_id", "TEST_ONLY_FOREIGN_PARENT"),
        ("branch_fork_clock", -1),
        ("clock", 999999),
        ("actor_id", "TEST_ONLY_FOREIGN_ACTOR"),
        ("event_ref", "0" * 64),
        ("event_id", "TEST_ONLY_FOREIGN_EVENT"),
        ("source_ref", "NOT_TEST_ONLY_ACCESS"),
        ("revoked", True),
    ),
)
def test_foreign_access_witness_refused_without_commit(share_world, field, value):
    world, _ = share_world
    witness = access.reseal_access_witness(world.make_access(), **{field: value})
    run = world.evaluate(f"foreign-access-{field}", access_witness=witness)
    assert run.refused is True
    assert run.committed is False
    assert run.store_path is None
    assert run.response.status is ResponseStatus.REFUSED
    assert run.response.target_proposals == ()
    assert run.refusal_reason
    assert not (run.run_dir / "c9.sqlite").exists()
    assert cold_verify(world.root, f"foreign-access-{field}")["ok"]


@pytest.mark.parametrize(
    "field,value",
    (
        ("root_id", "TEST_ONLY_FOREIGN_ROOT"),
        ("branch_id", "TEST_ONLY_FOREIGN_BRANCH"),
        ("clock", 999999),
        ("actor_id", "TEST_ONLY_FOREIGN_ACTOR"),
        ("event_ref", "0" * 64),
        ("response_kind", "UNKNOWN_KIND"),
        ("performed", False),
        ("revoked", True),
    ),
)
def test_foreign_response_witness_refused_without_commit(share_world, field, value):
    world, _ = share_world
    witness = access.reseal_response_witness(
        world.make_response(), **{field: value}
    )
    run = world.evaluate(f"foreign-response-{field}", response_witness=witness)
    assert run.refused is True
    assert run.committed is False
    assert run.store_path is None
    assert run.response.status is ResponseStatus.REFUSED
    assert run.response.target_proposals == ()
    assert run.refusal_reason
    assert not (run.run_dir / "c9.sqlite").exists()
    assert cold_verify(world.root, f"foreign-response-{field}")["ok"]


def test_refuse_tool_is_observed_current_refusal_without_target(refuse_world):
    world, _ = refuse_world
    run = world.evaluate("refuse")
    assert run.committed is True
    assert run.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert run.response.reason == access.OBSERVED_CURRENT_REFUSAL
    assert run.response.target_proposals == ()
    assert run.decision.branch is TargetBranch.NO_CHANGE
    assert run.decision.reason is TargetReason.NO_PROPOSAL
    assert run.target_state_rows == 0
    assert run.receipt["response_kind"] == "EXPLICIT_REFUSAL"
    assert run.receipt["objective_material_eligible"] is False
    assert run.receipt["target_proposals"] == []
    assert cold_verify(world.root, "refuse")["ok"]


def test_labels_do_not_enter_the_m35_source_preimage():
    case = _case(True)
    altered = deepcopy(case)
    altered["social_role"] = "TEST_ONLY_ALTERED_ROLE"
    altered["demographic_label"] = "TEST_ONLY_ALTERED_LABEL"
    altered["records"] = deepcopy(case["records"])
    assert firstclass.case_preimage(altered) == firstclass.case_preimage(case)
    assert firstclass.source_from_case(altered) == firstclass.source_from_case(case)


def test_history_refs_do_not_create_practice_or_target(share_world):
    world, _ = share_world
    baseline = world.evaluate("history-baseline")
    history = world.evaluate(
        "history-refs",
        enacted_history_refs=(
            "TEST_ONLY_HISTORY_ACT_ONE",
            "TEST_ONLY_HISTORY_ACT_TWO",
        ),
    )
    _assert_positive(baseline)
    _assert_positive(history)
    assert history.response.reason == baseline.response.reason
    assert history.receipt["hash"] == baseline.receipt["hash"]
    assert history.receipt["target_proposals"] == []
    assert history.target_state_rows == 0


def test_share_and_refuse_share_the_same_public_refusal_surface(share_world, refuse_world):
    share, _ = share_world
    refuse, _ = refuse_world
    share_refusal = share.evaluate(
        "share-explicit-refusal",
        response_witness=share.make_response(response_kind="EXPLICIT_REFUSAL"),
    )
    refuse_refusal = refuse.evaluate("refuse-explicit-refusal")
    assert share_refusal.response.reason == access.OBSERVED_CURRENT_REFUSAL
    assert refuse_refusal.response.reason == access.OBSERVED_CURRENT_REFUSAL
    assert share_refusal.response.target_proposals == ()
    assert refuse_refusal.response.target_proposals == ()
    assert share_refusal.receipt["response_kind"] == "EXPLICIT_REFUSAL"
    assert refuse_refusal.receipt["response_kind"] == "EXPLICIT_REFUSAL"
    assert "b_operation" not in share_refusal.receipt
    assert share_refusal.target_state_rows == 0
    assert refuse_refusal.target_state_rows == 0


def test_production_registries_remain_empty_and_no_native_issuance(share_world):
    world, _ = share_world
    assert dict(DEFAULT_ISSUED_RESPONSE_RULES) == {}
    assert dict(DEFAULT_ISSUED_TARGET_RULES) == {}
    assert world.response_registry.grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    from candidate.target_rules import TargetRuleRegistry

    assert dict(TargetRuleRegistry.production().rules) == {}
    assert world.rule.grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    run = world.evaluate("native-check")
    assert run.receipt["native"] is False
    assert run.receipt["target_proposals"] == []
    assert run.target_state_rows == 0


def test_cold_readback_after_world_close(tmp_path):
    case = _case(True)
    world = S35World.build(tmp_path / "cold-world", case=case)
    run = world.evaluate("cold")
    _assert_positive(run)
    world.close()
    cold = cold_verify(world.root, "cold")
    assert cold["ok"], cold["checks"]
    assert cold["observed"]["s35_receipt_hash"] == run.receipt["hash"]
    assert cold["observed"]["target_state_rows"] == 0
