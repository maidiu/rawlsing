"""A relay: qualified acquired state and current B02 period ingress."""
from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path

import pytest

D02_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D02_ROOT.parent
D01_ROOT = WORKER_RETURNS / "SOROK-DUEL-D01-R1"
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
B02_ROOT = WORKER_RETURNS / "SOROK-DUEL-B02-R1"
for _path in (D01_ROOT, P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests", B02_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as b02  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
    digest,
)
from p3 import situated_context  # noqa: E402
from p3_fixture_support import batch_events, build_case  # noqa: E402


def _structural_plan(case, *, project=None, counterpart=None, role=None):
    plan = copy.deepcopy(case.plans[3])
    if project is not None:
        plan["project"] = project
    if counterpart is not None:
        plan["counterpart"] = counterpart
    if role is not None:
        plan["activation_roles"] = [role]
        plan["interlocutor_role"] = role
    plan["hash"] = digest({key: value for key, value in plan.items()
                           if key != "hash"})
    return plan


def _run_acquired(path: Path, outcome: str) -> dict:
    if path.exists():
        shutil.rmtree(path)
    case = build_case(path, history_outcomes=(outcome,))
    try:
        bootstrap = case.cycle.bootstrap(context={"fixture": "acquired-bootstrap"})
        formation = batch_events(bootstrap)[0]
        event_id = formation["objective"]["event"]["action_event_id"]
        head_before = dict(case.owner.store.head())
        selector = situated_context.build_situated_context(
            case.owner, event_id=event_id, plan=case.plans[3],
        )
        assert case.owner.store.head() == head_before
        acquired = selector["acquired_state"]
        boundary = selector["recipient_boundary"]
        assert boundary["provider_role"] == (
            "WORLD_PROPOSAL_TRANSPORT_NOT_ACTOR_COGNITION")
        assert boundary["options_are_exhaustive"] is False
        assert "acquired_state" in boundary["actor_qualified_input"]
        assert "material" in boundary["world_proposal_input"]
        assert "material" not in boundary["actor_qualified_input"]
        assert acquired["status"] == "ELIGIBLE"
        assert acquired["native_rule"] == "MISSING_RULE"
        assert acquired["memory_formation"] == "MISSING_RULE"
        assert acquired["first_person_claims"] == []
        assert "payload" not in json.dumps(acquired)
        assert "origin_access" not in json.dumps(acquired)
        second = case.cycle.advance(context=selector)
        provider_context = case.provider.calls[1]["context"]
        assert provider_context == selector
        later = batch_events(second)[0]
        response = later["consequences"]["test_only_psychological"]
        assert case.owner.store.head() == head_before
        return {
            "formation_event": formation["objective"]["event"]["e1_event_hash"],
            "formation_mode": acquired["eligible_modes"],
            "record_hashes": list(acquired["eligible_record_hashes"]),
            "provider_acquired": provider_context["acquired_state"],
            "later_streams": [
                (row.get("mode"), row.get("record_hash"))
                for row in response["streams"]
            ],
            "selector_hash": selector["hash"],
        }
    finally:
        case.owner.close()


def test_acquired_state_changes_actual_provider_input_same_world_seed(
    tmp_path: Path,
) -> None:
    path = tmp_path / "actual-p2"
    recognized = _run_acquired(path, "recognized_plan")
    imposed = _run_acquired(path, "imposed_plan")

    assert recognized["formation_event"] == imposed["formation_event"]
    assert recognized["formation_mode"] == ["joint_check"]
    assert imposed["formation_mode"] == ["private_check"]
    assert recognized["record_hashes"] != imposed["record_hashes"]
    assert recognized["selector_hash"] != imposed["selector_hash"]

    recognized_provider = recognized["provider_acquired"]
    imposed_provider = imposed["provider_acquired"]
    assert recognized_provider["status"] == "ELIGIBLE"
    assert imposed_provider["status"] == "ELIGIBLE"
    assert recognized_provider["eligible_modes"] == ["joint_check"]
    assert imposed_provider["eligible_modes"] == ["private_check"]
    assert recognized_provider["eligible_record_hashes"] == (
        recognized["record_hashes"])
    assert imposed_provider["eligible_record_hashes"] == (
        imposed["record_hashes"])
    assert recognized_provider["eligible_modes"] != imposed_provider[
        "eligible_modes"]
    assert recognized["later_streams"] == [
        ("joint_check", recognized_provider["eligible_record_hashes"][0])]
    assert imposed["later_streams"] == [
        ("private_check", imposed_provider["eligible_record_hashes"][0])]
    assert recognized["later_streams"][0][0] != imposed["later_streams"][0][0]


def test_acquired_state_withholds_wrong_scope_role_and_contradiction(
    tmp_path: Path,
) -> None:
    case = build_case(
        tmp_path / "acquired-negatives",
        history_outcomes=("recognized_plan", "imposed_plan"),
    )
    try:
        bootstrap = case.cycle.bootstrap(context={"fixture": "neg-bootstrap"})
        formation = batch_events(bootstrap)[0]
        event_id = formation["objective"]["event"]["action_event_id"]
        head = dict(case.owner.store.head())

        baseline = situated_context.build_situated_context(
            case.owner, event_id=event_id, plan=case.plans[3])
        acquired = baseline["acquired_state"]
        assert acquired["status"] == "CONTRADICTION"
        assert acquired["eligible_modes"] == ["joint_check", "private_check"]
        assert acquired["contradictions"]
        assert case.owner.store.head() == head

        unrelated = situated_context.build_situated_context(
            case.owner, event_id=event_id,
            plan=_structural_plan(case, project="unrelated-project"))
        assert unrelated["acquired_state"]["status"] == "NO_RECORDS"
        assert unrelated["acquired_state"]["eligible_modes"] == []
        assert unrelated["acquired_state"]["withheld"] == []

        inhibited = situated_context.build_situated_context(
            case.owner, event_id=event_id,
            plan=_structural_plan(case, role="official"))
        state = inhibited["acquired_state"]
        assert state["status"] == "HELD_NO_ELIGIBLE_RECORD"
        assert state["eligible_modes"] == []
        assert len(state["withheld"]) == 2
        assert {row["activation"] for row in state["withheld"]} == {"INHIBITED"}

        bypass = _structural_plan(case)
        bypass["actor_observed"] = True
        with pytest.raises(RecursionRefusal, match="D02_PLAN_OVERRIDE_FORBIDDEN"):
            situated_context.build_situated_context(
                case.owner, event_id=event_id, plan=bypass)
        assert case.owner.store.head() == head
    finally:
        case.owner.close()


def test_current_b02_period_ingress_and_current_employment(tmp_path: Path) -> None:
    case = build_case(tmp_path / "period")
    try:
        session = case.base_owner.fanin.session
        plan = b02.establish_period_plan(session)
        assert plan["anchor_clock"] == session.clock()
        first = situated_context.build_situated_context(case.owner)
        period = first["period"]
        assert period["status"] == "QUALIFIED_CURRENT_PERIOD"
        assert period["as_of_date"] == "2026-01-01"
        assert period["logical_tick"] == session.clock()
        assert period["period"]["period_id"] == "period:2026-h1"
        assert period["employment"]["term_id"] == (
            "employment:workshop-cooperative")
        assert period["employment_status"] == "EFFECTIVE"
        assert period["holder_actor_slot"] == "A"
        assert period["interval_status"] == "NOT_MATERIALIZED"
        assert period["interval_span"]["mode"] == "SCHEDULED_ONLY"
        assert period["interval_span"]["span"] == 181
        assert first["date_scope"]["calendar"] == "B02_CURRENT_LOGICAL_PERIOD"
        assert first["date_scope"]["historical_period"] == (
            "CURRENT_STATE_ONLY_NOT_HISTORICAL_QUERY")
        assert first["source_closure"]["hash"]
        assert first["period"]["source"]["sha256"] == (
            first["period_source"]["sha256"])

        focal = session.read_root()["actor_ids"][0]
        proposal = EventProposal(
            "d02-period-advance", session.clock() + 90, "ADMIT_EVENT",
            (case.base_owner.source_ref,),
            tuple(session.read_root()["actor_ids"]), {},
        )
        result = case.base_owner.realize(
            "d02-period-advance-operation", proposal,
            case.base_owner.snapshot())
        assert result.after.clock == 312
        changed = situated_context.build_situated_context(case.owner)
        changed_period = changed["period"]
        assert changed_period["as_of_date"] == "2026-04-01"
        assert changed_period["logical_tick"] == 312
        assert changed_period["period"]["period_id"] == "period:2026-h1"
        assert changed_period["employment"]["term_id"] == (
            "employment:civic-works")
        assert changed_period["employment"]["effective_from"] == "2026-03-15"
        assert changed_period["employment_status"] == "EFFECTIVE"
        assert changed_period["holder_actor_id"] == focal
        assert changed_period["interval_status"] == "NOT_MATERIALIZED"
        assert changed["hash"] != first["hash"]

        world = session.world()
        saved_plan = world.resources["p6_historical_period"]
        saved_employment = world.resources["p6_employment"]
        world.resources.pop("p6_historical_period")
        session.product._checkpoint(session.branch_id, world.clock, world)
        held = situated_context.build_situated_context(case.owner)
        assert held["period"]["status"] == "HELD"
        assert held["date_scope"]["calendar"] == (
            "B02_READER_PRESENT_NO_CURRENT_PERIOD")
        world = session.world()
        world.resources["p6_historical_period"] = saved_plan
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert situated_context.build_situated_context(
            case.owner)["hash"] == changed["hash"]

        world = session.world()
        tampered = copy.deepcopy(world.resources["p6_employment"])
        tampered["source"] = "0" * 64
        world.resources["p6_employment"] = tampered
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(
            RecursionRefusal, match="P6_EMPLOYMENT_SOURCE_OR_ROOT_MISMATCH"):
            situated_context.build_situated_context(case.owner)
        world = session.world()
        world.resources["p6_employment"] = saved_employment
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert situated_context.build_situated_context(
            case.owner)["hash"] == changed["hash"]
    finally:
        case.owner.close()


def test_acquired_state_zero_record_provider_control(tmp_path: Path) -> None:
    case = build_case(tmp_path / "zero-record", history_outcomes=())
    try:
        bootstrap = case.cycle.bootstrap(context={"fixture": "zero-bootstrap"})
        formation = batch_events(bootstrap)[0]
        event_id = formation["objective"]["event"]["action_event_id"]
        assert case.owner.store.head()["count"] == 0
        selector = situated_context.build_situated_context(
            case.owner, event_id=event_id, plan=case.plans[3])
        acquired = selector["acquired_state"]
        assert acquired["status"] == "NO_RECORDS"
        assert acquired["eligible_modes"] == []
        assert acquired["eligible_record_hashes"] == []
        assert acquired["stored_count"] == 0
        second = case.cycle.advance(context=selector)
        provider_context = case.provider.calls[1]["context"]
        assert provider_context["acquired_state"]["status"] == "NO_RECORDS"
        assert provider_context["acquired_state"]["eligible_modes"] == []
        later = batch_events(second)[0]
        response = later["consequences"]["test_only_psychological"]
        assert [row["mode"] for row in response["streams"]] == ["inspect_alone"]
        assert case.owner.store.head()["count"] == 0
    finally:
        case.owner.close()
