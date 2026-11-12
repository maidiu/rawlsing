"""B D02 counterstrike: temporal access, event/current separation, source closure."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import types
from pathlib import Path

import pytest

D02_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D02_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P6_ROOT = WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
for _path in (P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests", P6_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
    digest,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
    register_supporting_actor,
)
from p3 import situated_context  # noqa: E402
from p3_fixture_support import build_case  # noqa: E402

PARENT_ID = "TEST_ONLY_D02_PARENT"
PARENT_ALIAS = "P"
SECRET = "d02-b-private-motive-not-for-nadia"


def _setup(path: Path, count: int = 1):
    if path.exists():
        shutil.rmtree(path)
    case = build_case(path)
    session = case.base_owner.fanin.session
    focal = session.read_root()["actor_ids"][0]
    house.establish(session)
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": SECRET},
    )
    for index in range(1, count + 1):
        proposal = EventProposal(
            f"d02-b-event-{index}",
            case.initial.clock + 3 * index,
            "ADMIT_EVENT",
            (case.base_owner.source_ref,),
            (focal, PARENT_ID),
            {},
        )
        case.base_owner.realize(
            f"d02-b-operation-{index}", proposal,
            case.base_owner.snapshot(),
        )
    return case, session, focal


def _rows(session):
    return list(session.read_events())


def _latest(rows):
    return max(
        rows,
        key=lambda row: (
            int(row["event_time"]), int(row["event_ordinal"]),
            str(row["action_event_id"]),
        ),
    )


def _selector(case, event_id=None, **kwargs):
    return situated_context.build_situated_context(
        case.owner, event_id=event_id, **kwargs)


def test_actual_events_select_latest_event_time_not_lexical_action_id(
    tmp_path: Path,
) -> None:
    case, session, _ = _setup(tmp_path / "actual-selection", count=10)
    try:
        rows = _rows(session)
        latest = _latest(rows)
        lexical = max(rows, key=lambda row: str(row["action_event_id"]))
        selector = _selector(case)
        assert selector["observation"]["event_id"] == latest["action_event_id"]
        assert selector["observation"]["selected_event_clock"] == latest["event_time"]
        assert selector["observation"]["selected_event_ordinal"] == (
            latest["event_ordinal"])
        assert selector["observation"]["read_world_clock"] == session.world().clock
        if lexical["action_event_id"] != latest["action_event_id"]:
            assert selector["observation"]["event_id"] != lexical["action_event_id"]
        assert selector["observation"]["selection_basis"] == (
            "EVENT_TIME_THEN_ORDINAL_NOT_READ_TIME")
    finally:
        case.owner.close()


def test_temporal_helper_uses_event_clock_when_world_clock_is_constant(
    monkeypatch,
) -> None:
    class FakeSession:
        def __init__(self, rows):
            self._rows = rows

        def read_events(self):
            return list(self._rows)

    class FakeSupporting:
        @staticmethod
        def read_actor_access(session, actor_id, event_id):
            clock = {"ZZZ": 10, "AAA": 20}[event_id]
            return {
                "status": "PERCEIVED",
                "world_clock": 100,
                "event": {"clock": clock},
                "receipt": {"clock": clock, "channel": "co_present"},
            }

    monkeypatch.setattr(
        situated_context, "_supporting_module", lambda: FakeSupporting)
    rows = [
        {"action_event_id": "ZZZ", "event_time": 10, "event_ordinal": 1},
        {"action_event_id": "AAA", "event_time": 20, "event_ordinal": 2},
    ]
    ref, access, event_time, ordinal = situated_context._latest_perceived(
        FakeSession(rows), "actor", None)
    assert ref == "AAA"
    assert access["status"] == "PERCEIVED"
    assert (event_time, ordinal) == (20, 2)


def test_event_access_hash_is_stable_when_world_clock_advances(
    tmp_path: Path,
) -> None:
    case, session, focal = _setup(tmp_path / "access-stability", count=1)
    try:
        rows = _rows(session)
        selected = _latest(rows)
        first = _selector(case, selected["action_event_id"])
        assert first["observation"]["access_hash"]
        assert first["relations"][0]["access_hash"]
        proposal = EventProposal(
            "d02-b-later-event",
            selected["event_time"] + 3,
            "ADMIT_EVENT",
            (case.base_owner.source_ref,),
            (focal, PARENT_ID),
            {},
        )
        case.base_owner.realize(
            "d02-b-later-operation", proposal, case.base_owner.snapshot())
        later = _selector(case, selected["action_event_id"])
        assert later["observation"]["selected_event_clock"] == (
            first["observation"]["selected_event_clock"])
        assert later["observation"]["read_world_clock"] != (
            first["observation"]["read_world_clock"])
        assert later["observation"]["access_hash"] == (
            first["observation"]["access_hash"])
        assert later["relations"][0]["access_hash"] == (
            first["relations"][0]["access_hash"])
        assert later["hash"] != first["hash"]
    finally:
        case.owner.close()


def test_remembered_event_relation_is_not_current_co_presence(
    tmp_path: Path,
) -> None:
    case, session, _ = _setup(tmp_path / "remembered", count=1)
    try:
        rows = _rows(session)
        selected = _latest(rows)
        baseline = _selector(case, selected["action_event_id"])
        relation = baseline["relations"][0]
        assert relation["event_co_present"] is True
        assert relation["current_co_present"] is True
        assert "ADDRESS_ELIGIBLE_OTHER" in baseline["admissible_options"]

        world = session.world()
        world.positions[PARENT_ALIAS] = "outside-house"
        session.product._checkpoint(session.branch_id, world.clock, world)
        moved = _selector(case, selected["action_event_id"])
        moved_relation = moved["relations"][0]
        assert moved_relation["event_co_present"] is True
        assert moved_relation["current_co_present"] is False
        assert moved_relation["co_present"] is False
        assert moved_relation["current_scope"] == "OBJECTIVE_POSITION_ONLY"
        assert "ADDRESS_ELIGIBLE_OTHER" not in moved["admissible_options"]
        assert moved["observation"]["event_id"] == selected["action_event_id"]
        assert moved["observation"]["access_hash"] == (
            baseline["observation"]["access_hash"])
    finally:
        case.owner.close()


def test_current_co_presence_without_event_perception_is_not_eligible(
    tmp_path: Path,
) -> None:
    case = build_case(tmp_path / "unobserved")
    try:
        session = case.base_owner.fanin.session
        initial = session.read_events()[0]
        event_id = initial.get("action_event_id") or initial.get("e1_event_id")
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        focal_position = situated_context._focal_position(
            session, session.read_root()["actor_ids"][0])
        world = session.world()
        world.positions[PARENT_ALIAS] = focal_position
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_actor_access(session, PARENT_ID, event_id)["status"] == (
            "NOT_PERCEIVED")
        selector = _selector(case, event_id)
        assert selector["relations"] == []
        assert "ADDRESS_ELIGIBLE_OTHER" not in selector["admissible_options"]
        assert SECRET not in json.dumps(selector)
    finally:
        case.owner.close()


def test_source_closure_is_exact_selected_reader_set(tmp_path: Path) -> None:
    case, _, _ = _setup(tmp_path / "closure", count=1)
    try:
        closure = situated_context.source_closure()
        labels = {row["path"] for row in closure["files"]}
        assert any(label.endswith("p3/situated_context.py") for label in labels)
        assert any(label.endswith("p3/__init__.py") for label in labels)
        assert any(label.endswith(
            "developmental_recursion/supporting_actor.py") for label in labels)
        assert any(label.endswith("SOROK-P6-ONE-LIVING-HOUSE-R1/house.py")
                   for label in labels)
        assert any(label.endswith("s45_projection/projection.py")
                   for label in labels)
        for suffix in (
            "p3/p3_owner.py", "p3/state_store.py", "p3/test_rules.py",
            "p3/projections.py", "p3/compression.py", "contracts.py",
            "p2_owner.py",
        ):
            assert any(label.endswith(suffix) for label in labels)
        assert not any(label.endswith("SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py")
                       for label in labels)
        for row in closure["files"]:
            path = WORKER_RETURNS / row["path"]
            assert path.is_file()
            assert hashlib.sha256(path.read_bytes()).hexdigest() == (
                row["sha256"])
        selector = _selector(case, _latest(_rows(
            case.base_owner.fanin.session))["action_event_id"])
        assert selector["source_closure"] == closure
        assert selector["readset"]["source_closure"]["hash"] == closure["hash"]
        assert situated_context.source_closure()["hash"] == closure["hash"]
    finally:
        case.owner.close()


def test_changed_selected_source_refuses_then_restores(
    tmp_path: Path, monkeypatch,
) -> None:
    case, session, _ = _setup(tmp_path / "changed-source", count=1)
    try:
        selected = _latest(_rows(session))
        baseline = _selector(case, selected["action_event_id"])
        baseline_closure = baseline["source_closure"]
        actual = Path(situated_context.__file__).resolve()
        changed = tmp_path / "situated_context_changed.py"
        changed.write_bytes(actual.read_bytes() + b"\n# changed source probe\n")
        files = situated_context._selected_source_files()
        changed_files = [
            (label, changed if Path(path).resolve() == actual else path)
            for label, path in files
        ]
        changed_closure = situated_context._source_closure(files=changed_files)
        assert changed_closure["hash"] != baseline_closure["hash"]
        with monkeypatch.context() as scoped:
            scoped.setattr(
                situated_context, "_selected_source_files",
                lambda: changed_files,
            )
            with pytest.raises(
                RecursionRefusal, match="D02_SOURCE_CLOSURE_CHANGED",
            ):
                _selector(
                    case, selected["action_event_id"],
                    expected_source_closure=baseline_closure,
                )
            rebuilt = _selector(case, selected["action_event_id"])
            assert rebuilt["source_closure"]["hash"] == (
                changed_closure["hash"])
        restored = _selector(
            case, selected["action_event_id"],
            expected_source_closure=baseline_closure,
        )
        assert restored["source_closure"]["hash"] == (
            baseline_closure["hash"])
        assert restored["hash"] == baseline["hash"]
        with pytest.raises(RecursionRefusal, match="D02_SOURCE_MISSING"):
            situated_context._source_closure(
                files=[("missing.py", tmp_path / "missing.py")])
    finally:
        case.owner.close()


def test_foreign_house_module_is_not_the_selected_reader(
    tmp_path: Path, monkeypatch,
) -> None:
    fake = types.SimpleNamespace(__file__=str(tmp_path / "foreign_house.py"))
    monkeypatch.setattr(situated_context, "_house_module", lambda: fake)
    with pytest.raises(RecursionRefusal, match="D02_HOUSE_SOURCE_IDENTITY"):
        situated_context.source_closure()


def test_pending_p3_operation_refuses_a_new_context(tmp_path: Path) -> None:
    case, session, _ = _setup(tmp_path / "pending", count=1)
    try:
        selected = _latest(_rows(session))
        plan = case.plans[0]
        case.owner.store.reserve(
            "d02-b-pending",
            proposal_hash=digest(case.proposals[0].document()),
            expected=case.owner.snapshot().document(),
            plan_hash=plan["hash"],
            base_before=case.base_owner.snapshot().document(),
            psyche_before=case.owner.store.head(),
            plan=plan,
        )
        with pytest.raises(RecursionRefusal, match="D02_PENDING_OPERATION"):
            _selector(case, selected["action_event_id"])
    finally:
        case.owner.close()


def test_b02_ingress_is_an_explicit_unbuilt_hold(tmp_path: Path) -> None:
    case, session, _ = _setup(tmp_path / "b02", count=1)
    try:
        selected = _latest(_rows(session))
        selector = _selector(case, selected["action_event_id"])
        assert selector["date_scope"]["calendar"] == "HELD_B02_NOT_BUILT"
        assert selector["date_scope"]["historical_period"] == "NOT_QUALIFIED"
        assert selector["date_scope"]["logical_clock_only"] is True
        assert selector["b02_ingress"]["status"] == (
            "PREREQUISITE_HELD_NOT_QUALIFIED")
        assert selector["b02_ingress"]["clock_basis"] == (
            "S46_LOGICAL_TICKS_NOT_CALENDAR_YEARS")
        assert selector["readset"]["b02_ingress"]["status"] == (
            "PREREQUISITE_HELD_NOT_QUALIFIED")
        assert "period_id" not in selector["identity"]
        assert "calendar" not in selector["identity"]
    finally:
        case.owner.close()
