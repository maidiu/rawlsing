from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import candidate
import candidate.pipeline as pipeline_module
import firstclass
from candidate import ResponseStatus, TargetBranch, TargetReason, lookup_rule, seal
from candidate.response_rules import DEFAULT_ISSUED_RESPONSE_RULES
from candidate.target_rules import DEFAULT_ISSUED_TARGET_RULES
from r31j.scenarios import evaluated

from bridge import access
from bridge.readback import cold_verify
from bridge.world import S35World

RETURN = Path(__file__).resolve().parents[1]


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


def _perception(world, *, status="ACCESSIBLE", **kwargs):
    return world.perception_receipt(access_status=status, **kwargs)


def _action(world, *, kind="REQUEST_TOOL", performed=True, **kwargs):
    return world.action_receipt(
        action_kind=kind, performed=performed, **kwargs
    )


def _positive_args(world):
    return {
        "perception_receipt": _perception(
            world,
            perception_ref="TEST_ONLY_A_PERCEPTION",
        ),
        "action_receipt": _action(
            world,
            action_ref="TEST_ONLY_A_ACTION_REQUEST",
        ),
    }


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
    assert run.receipt["evidence_grade"] == access.S35_GRADE_CONTROLLED
    assert run.receipt["actual_actor_input"] is False
    assert (
        run.receipt["qualification"]
        == access.S35_QUALIFICATION_CONTROLLED
    )


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
    for field in (
        "root_id",
        "root_branch_hash",
        "root_state_hash",
        "branch_id",
        "branch_hash",
        "branch_parent_id",
        "branch_fork_clock",
        "clock",
    ):
        assert run.receipt[field] == getattr(context, field)
    assert run.receipt["event_ref"] == context.event_ref
    assert run.receipt["event_id"] == context.event_id
    assert run.receipt["actor_id"] == context.actor_id


def _assert_no_b_private_operation(value):
    text = json.dumps(value, sort_keys=True)
    assert "SHARE_TOOL" not in text
    assert "REFUSE_TOOL" not in text


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


def test_missing_actual_a_inputs_are_typed_holds(share_world):
    world, _ = share_world
    run = world.evaluate("actual-a-hold")
    _assert_valid_empty(run, access.A_LOCAL_PERCEPTION_HOLD)
    assert run.receipt["hold_reason"] == "ACTUAL_A_LOCAL_PERCEPTION_UNAVAILABLE"
    assert run.receipt["evidence_grade"] == access.S35_GRADE_UNAVAILABLE
    assert run.receipt["actual_actor_input"] is False
    assert run.receipt["perception_ref"] == ""
    assert run.receipt["action_ref"] == ""
    assert cold_verify(world.root, "actual-a-hold")["ok"]


def test_p1_controlled_positive_zero_target_and_cold_readback(share_world):
    world, _ = share_world
    run = world.evaluate("p1", **_positive_args(world))
    _assert_positive(run)
    _same_world(world, run)
    assert run.receipt["perception_ref"] == "TEST_ONLY_A_PERCEPTION"
    assert run.receipt["action_ref"] == "TEST_ONLY_A_ACTION_REQUEST"
    assert run.receipt["action_kind"] == "REQUEST_TOOL"
    assert run.receipt["action_performed"] is True
    assert run.receipt["perceived_at"] == world.context.event_time
    assert run.receipt["action_time"] == world.context.event_time + 1
    assert run.receipt["objective_material_eligible"] is True
    assert run.receipt["objective_material_refs"]
    _assert_no_b_private_operation(run.receipt)
    run_json = json.loads((run.run_dir / "run.json").read_text(encoding="utf8"))
    _assert_no_b_private_operation(run_json)
    episodes = world.c12.episodes("s35")
    matching = [
        episode
        for episode in episodes
        if (episode.get("body") or {}).get("label") == "p1"
    ]
    assert len(matching) == 1
    _assert_no_b_private_operation(matching[0]["body"])
    cold = cold_verify(world.root, "p1")
    assert cold["ok"], cold["checks"]
    assert cold["observed"]["target_state_rows"] == 0
    assert cold["observed"]["evidence_grade"] == access.S35_GRADE_CONTROLLED


def test_access_severance_same_world_and_restoration(share_world):
    world, _ = share_world
    baseline = world.evaluate("access-baseline", **_positive_args(world))
    fault = world.evaluate(
        "access-fault",
        perception_receipt=_perception(
            world,
            status="NOT_WITNESSED",
            perception_ref="TEST_ONLY_A_PERCEPTION_NOT_WITNESSED",
        ),
        action_receipt=_action(world, action_ref="TEST_ONLY_A_ACTION_ACCESS_FAULT"),
    )
    restored = world.evaluate("access-restored", **_positive_args(world))
    _assert_positive(baseline)
    _assert_valid_empty(fault, access.UNKNOWN_RECEIVABILITY)
    _assert_positive(restored)
    for run in (baseline, fault, restored):
        _same_world(world, run)
    assert fault.receipt["objective_material_eligible"] is True
    assert fault.receipt["perception_ref"] == (
        "TEST_ONLY_A_PERCEPTION_NOT_WITNESSED"
    )
    assert cold_verify(world.root, "access-fault")["ok"]
    assert cold_verify(world.root, "access-restored")["ok"]


def test_action_severance_same_world_and_restoration(share_world):
    world, _ = share_world
    baseline = world.evaluate("action-baseline", **_positive_args(world))
    missing = world.evaluate(
        "action-missing",
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_ACTION_MISSING"
        ),
    )
    not_performed = world.evaluate(
        "action-not-performed",
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_NOT_PERFORMED"
        ),
        action_receipt=_action(
            world,
            kind="NO_OBSERVED_ACTION",
            performed=False,
            action_ref="TEST_ONLY_A_ACTION_NONE",
        ),
    )
    restored = world.evaluate("action-restored", **_positive_args(world))
    _assert_positive(baseline)
    _assert_valid_empty(missing, access.A_OWNED_ACTION_HOLD)
    assert missing.receipt["hold_reason"] == "ACTUAL_A_OWNED_ACTION_UNAVAILABLE"
    _assert_valid_empty(not_performed, access.RECEIVABLE_NO_OBSERVED_UPTAKE)
    _assert_positive(restored)
    for run in (baseline, missing, not_performed, restored):
        _same_world(world, run)
    assert cold_verify(world.root, "action-missing")["ok"]
    assert cold_verify(world.root, "action-not-performed")["ok"]
    assert cold_verify(world.root, "action-restored")["ok"]


def test_no_action_receipt_clock_is_validated(share_world):
    world, _ = share_world
    perception = _perception(
        world, perception_ref="TEST_ONLY_A_PERCEPTION_NO_ACTION_CLOCK"
    )
    for label, action_time in (
        ("no-action-negative-clock", -1),
        ("no-action-future-clock", world.context.clock + 1),
    ):
        action = _action(
            world,
            kind="NO_OBSERVED_ACTION",
            performed=False,
            action_ref="TEST_ONLY_A_ACTION_NO_OBSERVED_" + label,
            action_time=action_time,
        )
        run = world.evaluate(
            label,
            perception_receipt=perception,
            action_receipt=action,
        )
        assert run.refused is True
        assert run.committed is False
        assert run.response.status is ResponseStatus.REFUSED
        assert run.refusal_reason == "ACTION_TIME_INVALID"
        assert not (run.run_dir / "c9.sqlite").exists()
        assert cold_verify(world.root, label)["ok"]


def test_contradictory_context_valid_empty_and_unbound_refusal(share_world):
    world, _ = share_world
    contradictory = world.evaluate(
        "contradictory",
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_CONTRADICTORY"
        ),
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
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_CONTRADICTORY_UNBOUND"
        ),
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
        ("perceived_at", -1),
        ("access_status", "INVALID_STATUS"),
        ("source_ref", "NOT_TEST_ONLY_PERCEPTION"),
        ("owner_ref", "TEST_ONLY_FOREIGN_OWNER"),
        ("revoked", True),
        ("evidence_grade", "UNKNOWN_GRADE"),
        ("actual_actor_input", True),
        ("native", True),
    ),
)
def test_foreign_perception_receipt_refused_without_commit(
    share_world, field, value
):
    world, _ = share_world
    receipt = access.reseal_perception_receipt(
        _perception(world, perception_ref="TEST_ONLY_A_PERCEPTION_FOREIGN"),
        **{field: value},
    )
    run = world.evaluate(
        f"foreign-perception-{field}",
        perception_receipt=receipt,
        action_receipt=_action(
            world, action_ref="TEST_ONLY_A_ACTION_FOREIGN_PERCEPTION"
        ),
    )
    assert run.refused is True
    assert run.committed is False
    assert run.store_path is None
    assert run.response.status is ResponseStatus.REFUSED
    assert run.response.target_proposals == ()
    assert run.refusal_reason
    assert not (run.run_dir / "c9.sqlite").exists()
    assert cold_verify(world.root, f"foreign-perception-{field}")["ok"]


@pytest.mark.parametrize(
    "field,value",
    (
        ("root_id", "TEST_ONLY_FOREIGN_ROOT"),
        ("branch_id", "TEST_ONLY_FOREIGN_BRANCH"),
        ("branch_hash", "d" * 64),
        ("clock", 999999),
        ("actor_id", "TEST_ONLY_FOREIGN_ACTOR"),
        ("event_ref", "0" * 64),
        ("event_id", "TEST_ONLY_FOREIGN_EVENT"),
        ("action_kind", "UNKNOWN_KIND"),
        ("performed", False),
        ("action_ref", ""),
        ("owner_ref", "TEST_ONLY_FOREIGN_OWNER"),
        ("action_time", -1),
        ("revoked", True),
        ("evidence_grade", "UNKNOWN_GRADE"),
        ("actual_actor_input", True),
        ("native", True),
    ),
)
def test_foreign_action_receipt_refused_without_commit(
    share_world, field, value
):
    world, _ = share_world
    receipt = access.reseal_action_receipt(
        _action(world, action_ref="TEST_ONLY_A_ACTION_FOREIGN"),
        **{field: value},
    )
    run = world.evaluate(
        f"foreign-action-{field}",
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_FOREIGN_ACTION"
        ),
        action_receipt=receipt,
    )
    assert run.refused is True
    assert run.committed is False
    assert run.store_path is None
    assert run.response.status is ResponseStatus.REFUSED
    assert run.response.target_proposals == ()
    assert run.refusal_reason
    assert not (run.run_dir / "c9.sqlite").exists()
    assert cold_verify(world.root, f"foreign-action-{field}")["ok"]


def test_broken_receipt_seals_and_source_hashes_are_refused(share_world):
    world, _ = share_world
    perception = _perception(
        world, perception_ref="TEST_ONLY_A_PERCEPTION_BROKEN_SEAL"
    )
    action = _action(world, action_ref="TEST_ONLY_A_ACTION_BROKEN_SEAL")
    broken_perception = {
        key: value
        for key, value in perception.items()
        if key not in {"hash", "source_hash"}
    }
    broken_perception["source_hash"] = "0" * 64
    broken_perception = seal(broken_perception)
    run = world.evaluate(
        "perception-source-hash",
        perception_receipt=broken_perception,
        action_receipt=action,
    )
    assert run.refused is True
    assert run.refusal_reason == "PERCEPTION_SOURCE_HASH_MISMATCH"
    broken_action = {
        key: value
        for key, value in action.items()
        if key not in {"hash", "source_hash"}
    }
    broken_action["source_hash"] = "0" * 64
    broken_action = seal(broken_action)
    run = world.evaluate(
        "action-source-hash",
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_FOR_BROKEN_ACTION"
        ),
        action_receipt=broken_action,
    )
    assert run.refused is True
    assert run.refusal_reason == "ACTION_SOURCE_HASH_MISMATCH"


def test_qualified_owner_paths_hold_or_refuse_without_actual_claim(share_world):
    world, _ = share_world
    perception = world.perception_receipt(
        access_status="ACCESSIBLE",
        perception_ref="TEST_ONLY_A_PERCEPTION_QUALIFIED",
        evidence_grade=access.S35_GRADE_QUALIFIED,
        actual_actor_input=True,
        qualification=access.S35_QUALIFICATION_QUALIFIED,
    )
    action = world.action_receipt(
        action_kind="REQUEST_TOOL",
        performed=True,
        action_ref="TEST_ONLY_A_ACTION_QUALIFIED",
        evidence_grade=access.S35_GRADE_QUALIFIED,
        actual_actor_input=True,
        qualification=access.S35_QUALIFICATION_QUALIFIED,
    )
    hold = world.evaluate(
        "qualified-hold",
        perception_receipt=perception,
        action_receipt=action,
    )
    _assert_valid_empty(hold, access.A_LOCAL_PERCEPTION_HOLD)
    assert hold.receipt["hold_reason"] == (
        "QUALIFIED_A_LOCAL_PERCEPTION_RESOLVER_UNAVAILABLE"
    )
    assert hold.receipt["evidence_grade"] == access.S35_GRADE_UNAVAILABLE
    assert hold.receipt["actual_actor_input"] is False
    assert hold.receipt["qualification"] == access.S35_QUALIFICATION_UNRESOLVED
    perception_refused = world.evaluate(
        "qualified-perception-refused",
        perception_receipt=perception,
        action_receipt=action,
        qualified_owner_resolver=lambda **kwargs: False,
    )
    assert perception_refused.refused is True
    assert perception_refused.refusal_reason == "A_LOCAL_PERCEPTION_UNVERIFIED"
    action_refused = world.evaluate(
        "qualified-action-refused",
        perception_receipt=perception,
        action_receipt=action,
        qualified_owner_resolver=lambda **kwargs: kwargs.get("kind") == "perception",
    )
    assert action_refused.refused is True
    assert action_refused.refusal_reason == "A_OWNED_ACTION_UNVERIFIED"
    assert action_refused.committed is False
    assert not (action_refused.run_dir / "c9.sqlite").exists()
    assert cold_verify(world.root, "qualified-hold")["ok"]
    assert cold_verify(world.root, "qualified-perception-refused")["ok"]
    assert cold_verify(world.root, "qualified-action-refused")["ok"]


def test_refuse_tool_is_observed_current_refusal_without_target(refuse_world):
    world, _ = refuse_world
    run = world.evaluate(
        "refuse",
        perception_receipt=_perception(
            world, perception_ref="TEST_ONLY_A_PERCEPTION_REFUSE"
        ),
        action_receipt=_action(
            world,
            kind="EXPLICIT_REFUSAL",
            action_ref="TEST_ONLY_A_ACTION_REFUSE",
        ),
    )
    assert run.committed is True
    assert run.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert run.response.reason == access.OBSERVED_CURRENT_REFUSAL
    assert run.response.target_proposals == ()
    assert run.decision.branch is TargetBranch.NO_CHANGE
    assert run.decision.reason is TargetReason.NO_PROPOSAL
    assert run.target_state_rows == 0
    assert run.receipt["action_kind"] == "EXPLICIT_REFUSAL"
    assert run.receipt["objective_material_eligible"] is False
    assert run.receipt["target_proposals"] == []
    _assert_no_b_private_operation(run.receipt)
    assert cold_verify(world.root, "refuse")["ok"]


def test_share_and_refuse_share_the_same_public_refusal_surface(
    share_world, refuse_world
):
    share, _ = share_world
    refuse, _ = refuse_world
    share_refusal = share.evaluate(
        "share-explicit-refusal",
        perception_receipt=_perception(
            share, perception_ref="TEST_ONLY_A_PERCEPTION_SHARE_REFUSAL"
        ),
        action_receipt=_action(
            share,
            kind="EXPLICIT_REFUSAL",
            action_ref="TEST_ONLY_A_ACTION_SHARE_REFUSAL",
        ),
    )
    refuse_refusal = refuse.evaluate(
        "refuse-explicit-refusal",
        perception_receipt=_perception(
            refuse, perception_ref="TEST_ONLY_A_PERCEPTION_REFUSE_REFUSAL"
        ),
        action_receipt=_action(
            refuse,
            kind="EXPLICIT_REFUSAL",
            action_ref="TEST_ONLY_A_ACTION_REFUSE_REFUSAL",
        ),
    )
    assert share_refusal.response.reason == access.OBSERVED_CURRENT_REFUSAL
    assert refuse_refusal.response.reason == access.OBSERVED_CURRENT_REFUSAL
    assert share_refusal.response.target_proposals == ()
    assert refuse_refusal.response.target_proposals == ()
    assert share_refusal.receipt["action_kind"] == "EXPLICIT_REFUSAL"
    assert refuse_refusal.receipt["action_kind"] == "EXPLICIT_REFUSAL"
    _assert_no_b_private_operation(share_refusal.receipt)
    _assert_no_b_private_operation(refuse_refusal.receipt)
    assert share_refusal.target_state_rows == 0
    assert refuse_refusal.target_state_rows == 0


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
    baseline = world.evaluate("history-baseline", **_positive_args(world))
    history = world.evaluate(
        "history-refs",
        **_positive_args(world),
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


def test_pipeline_selector_validates_consumer_inputs(share_world):
    world, _ = share_world
    perception = _perception(
        world, perception_ref="TEST_ONLY_A_PERCEPTION_CONSUMER"
    )
    action = _action(world, action_ref="TEST_ONLY_A_ACTION_CONSUMER")
    lookup = lookup_rule(
        world.response_registry,
        authority_id=world.rule.authority_id,
        rule_version=world.rule.rule_version,
        rule_content_hash=world.rule.rule_content_hash,
        subject=world.context.actor_id,
    )
    evaluation = access.evaluate_actor_access_response(
        rule_lookup=lookup,
        event_ref=world.context.event_ref,
        event_time=world.context.event_time,
        subject=world.context.actor_id,
        request=access.S35ActorAccessRequest(
            perception_receipt=perception,
            action_receipt=action,
        ),
        conditioning_readset=world.conditioning.readset_refs,
        context=world.context,
        as_of=world.context.as_of,
        material_eligible=world.material_eligible,
        eligible_material_refs=world.eligible_material_refs,
    )
    expected = {
        "event_time": world.context.event_time,
        "conditioning_readset": world.conditioning.readset_refs,
        "material_eligible": world.material_eligible,
        "eligible_material_refs": world.eligible_material_refs,
        "actor_history_refs": (),
        "other_person_offer_ref": "",
        "material_opportunity_ref": "",
        "prior_response_count": 0,
        "rule_lookup": lookup,
    }
    current = {
        "context": world.context,
        "evaluation": evaluation,
        "expected": expected,
    }
    kwargs = {
        "rule_lookup": lookup,
        "event_ref": world.context.event_ref,
        "event_time": world.context.event_time,
        "subject": world.context.actor_id,
        "conditioning_readset": world.conditioning.readset_refs,
        "actor_history_refs": (),
        "other_person_offer_ref": "",
        "material_opportunity_ref": "",
        "prior_response_count": 0,
        "material_eligible": world.material_eligible,
        "eligible_material_refs": world.eligible_material_refs,
    }
    token = access.set_current_context(current)
    try:
        assert access.pipeline_selector(**kwargs) is evaluation.response
    finally:
        access.reset_current_context(token)
    mutations = (
        ("rule_lookup", replace(lookup, rule_content_hash="0" * 64)),
        ("event_time", world.context.event_time + 1),
        ("conditioning_readset", world.conditioning.readset_refs + ("TEST_ONLY_EXTRA",)),
        ("material_eligible", not world.material_eligible),
        ("eligible_material_refs", ("TEST_ONLY_OTHER_MATERIAL",)),
        ("actor_history_refs", ("TEST_ONLY_HISTORY_EXTRA",)),
        ("other_person_offer_ref", "TEST_ONLY_OTHER_OFFER"),
        ("material_opportunity_ref", "TEST_ONLY_OTHER_OPPORTUNITY"),
        ("prior_response_count", 1),
    )
    for field, value in mutations:
        changed = dict(kwargs)
        changed[field] = value
        token = access.set_current_context(current)
        try:
            with pytest.raises(RuntimeError) as caught:
                access.pipeline_selector(**changed)
            assert str(caught.value) == "S35_CONSUMER_INPUT_MISMATCH:" + field
        finally:
            access.reset_current_context(token)


def test_pipeline_selector_legacy_no_context_delegation(share_world):
    world, _ = share_world
    lookup = lookup_rule(
        world.response_registry,
        authority_id=world.rule.authority_id,
        rule_version=world.rule.rule_version,
        rule_content_hash=world.rule.rule_content_hash,
        subject=world.context.actor_id,
    )
    kwargs = {
        "rule_lookup": lookup,
        "event_ref": world.context.event_ref,
        "event_time": world.context.event_time,
        "subject": world.context.actor_id,
        "conditioning_readset": world.conditioning.readset_refs,
        "actor_history_refs": (),
        "other_person_offer_ref": "",
        "material_opportunity_ref": "",
        "prior_response_count": 0,
        "material_eligible": True,
        "eligible_material_refs": (),
    }
    legacy = candidate.evaluate_response(**kwargs)
    delegated = pipeline_module.evaluate_response(**kwargs)
    assert delegated.status == legacy.status
    assert delegated.reason == legacy.reason
    assert delegated.target_proposals == legacy.target_proposals
    assert delegated.receipt_hash == legacy.receipt_hash
    assert delegated.candidate_route == legacy.candidate_route


def test_production_registries_remain_empty_and_no_native_issuance(share_world):
    world, _ = share_world
    assert dict(DEFAULT_ISSUED_RESPONSE_RULES) == {}
    assert dict(DEFAULT_ISSUED_TARGET_RULES) == {}
    assert world.response_registry.grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    from candidate.target_rules import TargetRuleRegistry

    assert dict(TargetRuleRegistry.production().rules) == {}
    assert world.rule.grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"
    run = world.evaluate("native-check", **_positive_args(world))
    assert run.receipt["native"] is False
    assert run.receipt["target_proposals"] == []
    assert run.target_state_rows == 0


def test_public_projection_and_private_custody(share_world):
    world, _ = share_world
    run = world.evaluate("public-projection", **_positive_args(world))
    _assert_positive(run)
    projection = access.public_source_projection(world.source)
    assert "b_owner" not in projection
    assert "b_event_ref" not in projection
    assert "b_operation" not in projection
    assert projection["operation_disclosed"] is False
    assert access.public_privacy_error(projection) == ""
    world_json = json.loads((world.root / "world.json").read_text(encoding="utf8"))
    assert world_json["custody"]["grade"] == "PRIVATE_TEST_ONLY_WORLD_INPUT"
    assert "b_operation" in world_json["custody"]["source"]
    assert access.public_privacy_error(world_json["public_projection"]) == ""
    run_json = json.loads((run.run_dir / "run.json").read_text(encoding="utf8"))
    assert run_json["source_binding"] == projection
    assert run_json["private_custody_ref"] == "world.json"
    episodes = [
        episode
        for episode in world.c12.episodes("s35")
        if (episode.get("body") or {}).get("label") == "public-projection"
    ]
    assert len(episodes) == 1
    episode_body = episodes[0]["body"]
    assert episode_body["source_binding"] == projection
    assert episode_body["private_custody_ref"] == "world.json"
    for public_value in (run.receipt, run_json, episode_body):
        text = json.dumps(public_value, sort_keys=True)
        assert "TEST_ONLY_OWNER_share" not in text
        assert "TEST_ONLY_OWNER_refuse" not in text
        assert "TEST_ONLY_EVENT_share" not in text
        assert "TEST_ONLY_EVENT_refuse" not in text
    assert cold_verify(world.root, "public-projection")["ok"]


def test_cold_verify_does_not_mutate_store(tmp_path):
    case = _case(True)
    world = S35World.build(tmp_path / "nomutation-world", case=case)
    try:
        run = world.evaluate("nomutation", **_positive_args(world))
        _assert_positive(run)
        run_dir = run.run_dir
        paths = {
            "world.json": world.root / "world.json",
            "c12.sqlite": world.root / "c12.sqlite",
            "c9.sqlite": run_dir / "c9.sqlite",
            "run.json": run_dir / "run.json",
            "s35_receipt.json": run_dir / "s35_receipt.json",
        }
        before = {
            name: hashlib.sha256(path.read_bytes()).hexdigest()
            for name, path in paths.items()
        }
        result = cold_verify(world.root, "nomutation")
        assert result["ok"], result["checks"]
        after = {
            name: hashlib.sha256(path.read_bytes()).hexdigest()
            for name, path in paths.items()
        }
        assert after == before
    finally:
        world.close()


def test_fresh_process_cold_replay(tmp_path):
    case = _case(True)
    world = S35World.build(tmp_path / "fresh-world", case=case)
    try:
        run = world.evaluate("fresh-cold", **_positive_args(world))
        _assert_positive(run)
        world.close()
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(RETURN / "tools" / "cold_replay.py"),
                "--world-root",
                str(world.root),
                "--label",
                "fresh-cold",
            ],
            cwd=str(RETURN),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert completed.returncode == 0, completed.stderr
        payload = json.loads(completed.stdout)
        assert payload["fresh_process"] is True
        assert payload["store_mutated"] is False
        assert payload["ok"] is True
    finally:
        world.close()


def test_cold_readback_after_world_close(tmp_path):
    case = _case(True)
    world = S35World.build(tmp_path / "cold-world", case=case)
    run = world.evaluate("cold", **_positive_args(world))
    _assert_positive(run)
    world.close()
    cold = cold_verify(world.root, "cold")
    assert cold["ok"], cold["checks"]
    assert cold["observed"]["s35_receipt_hash"] == run.receipt["hash"]
    assert cold["observed"]["target_state_rows"] == 0
