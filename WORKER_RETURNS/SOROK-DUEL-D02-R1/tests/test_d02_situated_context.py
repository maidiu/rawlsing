"""D02 read-only situated-context differential and negative court."""
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
P6_ROOT = WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
for _path in (D01_ROOT, P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests", P6_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
    register_supporting_actor,
)
from p3 import situated_context  # noqa: E402
from p3_fixture_support import build_case  # noqa: E402

PARENT_ID = "TEST_ONLY_D02_PARENT"
PARENT_ALIAS = "P"
SECRET = "d02-private-motive-not-for-nadia"


def _setup(path: Path, *, parent: bool, tool: bool | None,
           observed_event: str | None = None):
    if path.exists():
        shutil.rmtree(path)
    case = build_case(path)
    session = case.base_owner.fanin.session
    focal = session.read_root()["actor_ids"][0]
    house.establish(session)
    if tool is not None:
        world = session.world()
        world.resources["workshop"]["tool_available"] = tool
        session.product._checkpoint(session.branch_id, world.clock, world)
    event_id = observed_event
    if parent:
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        proposal = EventProposal(
            "d02-parent-event", case.initial.clock + 3, "ADMIT_EVENT",
            (case.base_owner.source_ref,), (focal, PARENT_ID), {},
        )
        result = case.base_owner.realize(
            "d02-parent-operation", proposal, case.base_owner.snapshot())
        event_id = result.consequences["supporting_participants"][0]["event_id"]
    return case, session, event_id


def _selector(case, event_id=None):
    return situated_context.build_situated_context(
        case.owner, event_id=event_id)


def _close(case):
    case.owner.close()


def test_material_and_eligible_relation_change_actual_provider_context(
    tmp_path: Path,
) -> None:
    path = tmp_path / "actual-p2"

    base_case, _, base_event = _setup(path, parent=True, tool=True)
    try:
        base_selector = _selector(base_case, base_event)
        base_case.cycle.bootstrap(context=base_selector)
        base_request = base_case.provider.calls[0]["context"]
        assert base_request == base_selector
        assert "ATTEND_HOUSEHOLD_MATERIAL" in base_request["admissible_options"]
        assert "ADDRESS_ELIGIBLE_OTHER" in base_request["admissible_options"]
        assert "USE_HOUSEHOLD_TOOL" in base_request["admissible_options"]
    finally:
        _close(base_case)

    changed_case, _, changed_event = _setup(path, parent=True, tool=False)
    try:
        changed_selector = _selector(changed_case, changed_event)
        changed_case.cycle.bootstrap(context=changed_selector)
        changed_request = changed_case.provider.calls[0]["context"]
        assert changed_request == changed_selector
        assert changed_selector["material"]["source"] == (
            base_selector["material"]["source"])
        assert changed_selector["material"]["material_hash"] != (
            base_selector["material"]["material_hash"])
        assert "USE_HOUSEHOLD_TOOL" not in (
            changed_selector["admissible_options"])
        assert changed_selector["hash"] != base_selector["hash"]
        assert changed_request["hash"] != base_request["hash"]
        assert changed_request["admissible_options"] != (
            base_request["admissible_options"])
    finally:
        _close(changed_case)

    relationless_case, _, _ = _setup(path, parent=False, tool=True)
    try:
        relationless_selector = _selector(relationless_case)
        relationless_case.cycle.bootstrap(context=relationless_selector)
        relationless_request = relationless_case.provider.calls[0]["context"]
        assert relationless_request == relationless_selector
        assert relationless_selector["relations"] == []
        assert "ADDRESS_ELIGIBLE_OTHER" not in (
            relationless_selector["admissible_options"])
        assert relationless_selector["hash"] != base_selector["hash"]
        assert relationless_request["hash"] != base_request["hash"]
    finally:
        _close(relationless_case)


def test_selector_excludes_private_state_and_portal_gaze(tmp_path: Path) -> None:
    case, session, event_id = _setup(tmp_path / "private", parent=True, tool=True)
    try:
        selector = _selector(case, event_id)
        assert SECRET not in json.dumps(selector)
        assert "private_state" not in json.dumps(selector["relations"])
        assert "perceived_by_user" not in json.dumps(selector)
        assert selector["read_boundary"]["parent_private_state"] == "NOT_READ"
        assert selector["read_boundary"]["portal_user_view"] == "NOT_READ"
        assert selector["relations"][0]["access_scope"] == (
            "PUBLIC_SHARED_PERCEPTION")
        assert "fanin_view" not in json.dumps(selector)
    finally:
        _close(case)


def test_selector_stale_foreign_and_source_severance(tmp_path: Path) -> None:
    case, session, event_id = _setup(tmp_path / "severance", parent=True, tool=True)
    try:
        baseline = _selector(case, event_id)
        old = case.owner.snapshot()
        world = session.world()
        world.resources["workshop"]["tool_available"] = False
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="D02_STALE_STATE"):
            situated_context.build_situated_context(
                case.owner, expected=old, event_id=event_id)
        foreign = old.document()
        foreign["root"] = "foreign-root"
        with pytest.raises(RecursionRefusal, match="D02_FOREIGN_STATE:root"):
            situated_context.build_situated_context(
                case.owner, expected=foreign, event_id=event_id)
        world = session.world()
        world.resources["workshop"]["tool_available"] = True
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert _selector(case, event_id)["hash"] == baseline["hash"]

        world = session.world()
        saved = copy.deepcopy(world.resources["p6_household"])
        world.resources.pop("p6_household")
        session.product._checkpoint(session.branch_id, world.clock, world)
        held = _selector(case, event_id)
        assert held["material"]["status"] == "HELD"
        assert "ATTEND_HOUSEHOLD_MATERIAL" not in held["admissible_options"]
        assert held["hash"] != baseline["hash"]
        world = session.world()
        world.resources["p6_household"] = saved
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert _selector(case, event_id)["hash"] == baseline["hash"]

        world = session.world()
        tampered = copy.deepcopy(world.resources["p6_household"])
        tampered["source"] = "0" * 64
        world.resources["p6_household"] = tampered
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(
            RecursionRefusal, match="P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH"):
            _selector(case, event_id)
        world = session.world()
        world.resources["p6_household"] = saved
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert _selector(case, event_id)["hash"] == baseline["hash"]
    finally:
        _close(case)


def test_unobserved_parent_is_not_an_eligible_relation(tmp_path: Path) -> None:
    case, session, _ = _setup(tmp_path / "unobserved", parent=False, tool=True)
    try:
        initial = session.read_events()[0]
        initial_event_id = initial.get("action_event_id") or initial.get(
            "e1_event_id")
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        parent_access = read_actor_access(
            session, PARENT_ID, initial_event_id)
        assert parent_access["status"] == "NOT_PERCEIVED"
        selector = _selector(case, initial_event_id)
        assert selector["relations"] == []
        assert "ADDRESS_ELIGIBLE_OTHER" not in selector["admissible_options"]
        assert SECRET not in json.dumps(selector)
    finally:
        _close(case)


def test_objective_material_is_not_actor_accessible_by_default(
    tmp_path: Path,
) -> None:
    case, session, event_id = _setup(
        tmp_path / "access", parent=True, tool=True)
    try:
        baseline = _selector(case, event_id)
        assert baseline["material"]["status"] == "AVAILABLE"
        assert baseline["material"]["actor_accessible"]["status"] == "PRESENT"
        assert "ATTEND_HOUSEHOLD_MATERIAL" in baseline["admissible_options"]
        assert baseline["relations"][0]["co_present"] is True
        world = session.world()
        world.positions["A"] = "outside-house"
        session.product._checkpoint(session.branch_id, world.clock, world)
        elsewhere = _selector(case, event_id)
        assert elsewhere["material"]["status"] == "AVAILABLE"
        assert elsewhere["material"]["actor_accessible"]["status"] == "ELSEWHERE"
        assert "ATTEND_HOUSEHOLD_MATERIAL" not in (
            elsewhere["admissible_options"])
        assert "USE_HOUSEHOLD_TOOL" not in elsewhere["admissible_options"]
        assert elsewhere["hash"] != baseline["hash"]
        world = session.world()
        world.positions["A"] = "workshop"
        world.positions["P"] = "outside-house"
        session.product._checkpoint(session.branch_id, world.clock, world)
        moved = _selector(case, event_id)
        assert moved["relations"][0]["co_present"] is False
        assert "ADDRESS_ELIGIBLE_OTHER" not in moved["admissible_options"]
        world = session.world()
        world.positions["P"] = "workshop"
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert _selector(case, event_id)["hash"] == baseline["hash"]
    finally:
        _close(case)
