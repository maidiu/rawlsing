"""C03/C04 A relay: purchase history, lock composition, and Nadia experience consumer."""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[2]
REPO = RETURNS.parent
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P4 = RETURNS / "SOROK-P4-FIRST-FULL-MPC-R1"
for _path in (P6, P4, ENGINE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion import parent_activity as pa  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import load_p2  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    parent_material_fixture,
    read_parent_history,
    read_parent_material,
)
from developmental_recursion.parent_decision import (  # noqa: E402
    admit_parent_decision,
    parent_request_fixture,
    perform_parent_decision,
    propose_parent_decision,
    read_parent_decision,
)
from developmental_recursion.parent_speech import (  # noqa: E402
    perform_parent_utterance,
    read_child_experience,
    read_parent_utterance,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)
import run_p4  # noqa: E402
import run_p6  # noqa: E402

PARENT_ID = "TEST_ONLY_C03C04_PARENT"
PARENT_ALIAS = "P"
SECRET = "c03c04-private-motive"
HIDDEN_A = "c04-hidden-reason-alpha"
HIDDEN_B = "c04-hidden-reason-beta"
BASE = {
    "employment_status": "employed",
    "wage_units_per_hour": 5,
    "debt_units": 4,
    "care_hours_due": 2,
    "cash_units": 100,
    "free_hours": 8,
    "currency_unit": "sourcefree_currency_unit",
    "source_ref": "sourcefree:parent:antecedent:baseline",
}


def _new_state(tmp_path, name):
    state = tmp_path / name
    run_p6.experience(state, Namespace(command="new"))
    return state


def _op(state, operation, request):
    return run_p4.run_parent_operation(state, operation=operation, request=request)


def _register(state):
    _op(state, "parent-register", {
        "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
        "actor_id": PARENT_ID, "role": "parent",
        "private_state": {"motive": SECRET},
    })


def _fixture(**overrides):
    values = {**BASE, **overrides}
    return parent_material_fixture(actor_id=PARENT_ID, **values)


def _open_direct(tmp_path, name, *, overrides=None):
    state = _new_state(tmp_path, name)
    owner = run_p6.open_owner(state / "actual-p2")
    session = owner.base_owner.fanin.session
    hp = pa.historical_period_module()
    hp.establish_period_plan(session)
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": SECRET})
    pa.establish_parent_material(
        session, PARENT_ID, fixture=_fixture(**(overrides or {})))
    b04 = __import__("developmental_recursion.parent_decision",
                     fromlist=["_b04_module"])._b04_module()
    b04.establish_market_inventory(session)
    return owner, session


def _p3_head(state):
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        return owner.store.head()
    finally:
        owner.close()


def test_normal_live_parent_decision_action_speech_and_child_experience(tmp_path):
    state = _new_state(tmp_path, "normal")
    head_before = _p3_head(state)
    _op(state, "period-establish", {})
    _register(state)
    _op(state, "parent-establish", {
        "parent_id": PARENT_ID, "fixture": _fixture()})
    _op(state, "market-establish", {})
    request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
    decision = _op(state, "parent-decide", {
        "parent_id": PARENT_ID, "operation_id": "decision:c04",
        "request": request})
    assert decision["result"]["decision"]["action"] == "PURCHASE"
    assert decision["result"]["request_source"] == "CALLER_SUPPLIED_OBJECTIVE_REQUEST"
    assert decision["result"]["decision_evidence"] == (
        "EXPLICIT_SOURCEFREE_RULE_NOT_NATIVE")
    assert decision["result"]["physical_admission"] == "NOT_YET_PERFORMED"

    action = _op(state, "parent-perform", {
        "parent_id": PARENT_ID, "decision_id": "decision:c04"})
    assert action["result"]["status"] == "PERFORMED"
    assert action["result"]["performed"] is True
    assert action["result"]["physical_admission"] == "PERFORMED"
    assert action["result"]["purchase"]["status"] == "ADMITTED"

    first = _op(state, "parent-speak", {
        "parent_id": PARENT_ID, "decision_id": "decision:c04",
        "text": "Not this time.", "hidden_reason": {"reason": HIDDEN_A},
        "operation_id": "speech:c04:1"})
    assert first["result"]["status"] == "ADMITTED"
    assert first["result"]["text_source"] == "CALLER_SUPPLIED_NOT_GENERATED"
    assert first["result"]["hidden_reason_source"] == (
        "CALLER_SUPPLIED_NOT_GENERATED")
    assert first["result"]["language_generation_owner"] == "NOT_IMPLEMENTED"
    second = _op(state, "parent-speak", {
        "parent_id": PARENT_ID, "decision_id": "decision:c04",
        "text": "Not this time.", "hidden_reason": {"reason": HIDDEN_B},
        "operation_id": "speech:c04:2"})
    assert second["result"]["event_id"] != first["result"]["event_id"]

    child = run_p6.experience(state, Namespace(
        command="child-experience", event_id=None,
        operation_id="speech:c04:1"))
    assert child["status"] == "PERCEIVED"
    assert child["p6_experience_source"] == "situated.recent_speech"
    assert child["user_view"] == "NOT_EXPOSED"
    assert child["event"]["body_public"]["text"] == "Not this time."
    assert child["response_input"]["public_text"] == "Not this time."
    assert child["response_input"]["perception_channel"] == "speech"
    assert child["response_input"]["occurrence_clock"] == child["occurrence_clock"]
    assert child["response_input"]["read_clock"] >= child["occurrence_clock"]
    assert child["access_condition"] == "SAME_ROOM_AT_ADMISSION"
    assert child["access_owner"] == "C12_SPEECH_PERCEPTION_RECEIPT"
    assert child["event_hash"] == first["result"]["event_hash"]
    assert child["speaker_actor_id"] == PARENT_ID
    assert child["speaker_alias"] == PARENT_ALIAS
    assert HIDDEN_A not in json.dumps(child)
    assert HIDDEN_B not in json.dumps(child)
    assert "hidden_reason_hash" not in json.dumps(child)
    assert "PURCHASE" not in json.dumps(child)
    assert "decision_id" not in json.dumps(child["response_input"])
    assert child["response_input"]["decision_state"] == "NOT_READ"
    assert child["durable_acquisition"] == "MISSING_RULE"
    assert child["response_input"]["text_source"] == (
        "CALLER_SUPPLIED_NOT_GENERATED")
    assert child["response_input"]["language_generation_owner"] == (
        "NOT_IMPLEMENTED")

    second_child = run_p6.experience(state, Namespace(
        command="child-experience", event_id=None,
        operation_id="speech:c04:2"))
    assert second_child["status"] == "PERCEIVED"
    assert second_child["response_input"]["public_text"] == (
        child["response_input"]["public_text"])
    for key in ("access_condition", "access_owner", "perception_channel",
                "text_source", "language_generation_owner"):
        assert second_child["response_input"][key] == (
            child["response_input"][key])
    assert HIDDEN_A not in json.dumps(second_child)
    assert HIDDEN_B not in json.dumps(second_child)

    view = run_p6.experience(state, Namespace(command="view"))
    say = run_p6.experience(state, Namespace(
        command="say", text="hello", request_edge=False, request_id=None))
    assert view["room"] == "workshop"
    assert say.get("admission") == "ADMITTED"
    assert "Not this time." not in json.dumps(view)
    assert "Not this time." not in json.dumps(say)
    assert SECRET not in json.dumps(view)
    assert SECRET not in json.dumps(say)
    assert _p3_head(state) == head_before

    reopened = run_p6.open_owner(state / "actual-p2")
    try:
        session = reopened.base_owner.fanin.session
        parent_a = read_parent_utterance(
            session, PARENT_ID, "speech:c04:1", as_actor=PARENT_ID)
        parent_b = read_parent_utterance(
            session, PARENT_ID, "speech:c04:2", as_actor=PARENT_ID)
        assert parent_a["hidden_reason"] == {"reason": HIDDEN_A}
        assert parent_b["hidden_reason"] == {"reason": HIDDEN_B}
        history = read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert history["purchase_episode_count"] == 1
        assert history["material_consistent"] is True
        purchase_rows = [row for row in history["history"]
                         if row["kind"] == "P2_PARENT_PURCHASE"]
        assert len(purchase_rows) == 1
        assert purchase_rows[0]["action_provenance"] == "P2_PARENT_PURCHASE"
        assert not [row for row in history["history"]
                    if row.get("action_provenance")
                    == "P2_PARENT_MATERIAL_ANTECEDENT"
                    and row.get("operation_id") == "decision:c04:purchase"]
        assert read_parent_decision(
            session, PARENT_ID, "decision:c04", as_actor=PARENT_ID
        )["performed"] is True
    finally:
        reopened.close()


def test_remote_unheard_and_source_severed_child_experience(tmp_path):
    owner, session = _open_direct(tmp_path, "remote")
    try:
        request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
        decision = admit_parent_decision(
            session, PARENT_ID, operation_id="decision:remote",
            request=request, as_actor=PARENT_ID)
        assert decision["decision"]["action"] == "PURCHASE"
        child_id = session.read_root()["actor_ids"][0]
        child_alias = next(
            alias for alias, row in session.world().actor_state.items()
            if row.get("actor_id") == child_id)
        world = session.world()
        world.positions[child_alias] = "market"
        session.product._checkpoint(session.branch_id, world.clock, world)
        utterance = perform_parent_utterance(
            session, PARENT_ID, decision_id="decision:remote",
            text="Not this time.", hidden_reason={"reason": HIDDEN_A},
            operation_id="speech:remote")
        assert utterance["child_perception_channel"] == "NOT_PERCEIVED"
        child = read_child_experience(
            session, child_id, operation_id="speech:remote")
        assert child["status"] == "NOT_PERCEIVED"
        assert child["event"] is None
        assert child["response_input"] is None
        assert HIDDEN_A not in json.dumps(child)
        assert session.event(utterance["event_id"]) is not None
        p6_remote = run_p6.child_speech_experience(
            session, operation_id="speech:remote")
        assert p6_remote["status"] == "NOT_PERCEIVED"
        assert p6_remote["event"] is None
        assert "Not this time." not in json.dumps(p6_remote)
        assert HIDDEN_A not in json.dumps(p6_remote)

        original = session.event
        session.event = lambda event_id: (
            None if event_id == utterance["event_id"] else original(event_id))
        try:
            with pytest.raises(RecursionRefusal, match="CHILD_UPTAKE_EVENT_SEVERED"):
                read_child_experience(
                    session, child_id, operation_id="speech:remote")
            assert read_parent_decision(
                session, PARENT_ID, "decision:remote",
                as_actor=PARENT_ID)["status"] == "READ"
        finally:
            session.event = original
    finally:
        owner.close()

    owner2, session2 = _open_direct(tmp_path, "own-speech")
    try:
        request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
        admit_parent_decision(
            session2, PARENT_ID, operation_id="decision:own",
            request=request, as_actor=PARENT_ID)
        utterance = perform_parent_utterance(
            session2, PARENT_ID, decision_id="decision:own",
            text="Not this time.", hidden_reason={"reason": HIDDEN_A},
            operation_id="speech:own")
        child_id = session2.read_root()["actor_ids"][0]
        assert read_child_experience(
            session2, child_id, operation_id="speech:own")["status"] == (
                "PERCEIVED")
        store = session2.product.store
        original = store.perceptions

        def missing_parent_receipt(branch_id, actor_id=None):
            rows = original(branch_id, actor_id)
            if actor_id == PARENT_ALIAS:
                return [row for row in rows
                        if not (row.get("event_id") == utterance["event_id"]
                                and row.get("channel") == "own_speech")]
            return rows

        store.perceptions = missing_parent_receipt
        try:
            with pytest.raises(
                    RecursionRefusal,
                    match="CHILD_EXPERIENCE_PARENT_RECEIPT_MISSING"):
                read_child_experience(
                    session2, child_id, operation_id="speech:own")
        finally:
            store.perceptions = original
        assert read_child_experience(
            session2, child_id, operation_id="speech:own")["status"] == (
                "PERCEIVED")
    finally:
        owner2.close()


def test_currency_mismatch_refuses_before_b04_and_no_purchase_history(tmp_path):
    owner, session = _open_direct(
        tmp_path, "currency",
        overrides={"currency_unit": "parent_sourcefree_currency_unit"})
    try:
        request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
        proposal = propose_parent_decision(
            session, PARENT_ID, request=request, as_actor=PARENT_ID)
        assert proposal["evaluation"]["action"] == "DECLINE"
        assert "CURRENCY_MISMATCH" in proposal["evaluation"]["reasons"]
        assert read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID
        )["purchase_episode_count"] == 0
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID
        )["material"]["cash_units"] == 100

        material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        registration = __import__(
            "developmental_recursion.supporting_actor",
            fromlist=["read_supporting_actor"]).read_supporting_actor(
                session, PARENT_ID)
        fake_bridge = {
            "schema": "SOROK_P2_PARENT_MATERIAL@1",
            "grade": "SOURCEFREE_S2_ONLY",
            "root": session.read_root()["root_hash"],
            "branch": session.branch_id,
            "epoch": session.clock(),
            "actor_id": PARENT_ID,
            "alias": registration["alias"],
            "source": material["source"],
            "material_source": material["source"],
            "material_before_source": material["source"],
            "material_after_source": material["source"],
            "purchase_source": "0" * 64,
            "operation_id": "ghost:purchase",
            "operation_kind": "PURCHASE_MATERIAL_STATE",
        }
        session.product.store.append_episode(
            session.branch_id, actor_id=registration["alias"],
            kind="P2_PARENT_MATERIAL_ANTECEDENT",
            clock=session.clock(), body=fake_bridge)
        with pytest.raises(
                RecursionRefusal, match="BRIDGE_NOT_ADOPTED"):
            read_parent_material(
                session, PARENT_ID, as_actor=PARENT_ID)
    finally:
        owner.close()
