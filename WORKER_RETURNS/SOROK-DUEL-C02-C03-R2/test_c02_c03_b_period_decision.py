"""C02/C03 Agent B proof: incremental B02 periods, parent decision/action, C04 separation."""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
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
    read_parent_activity,
    read_parent_history,
    read_parent_material,
    parent_feasible_actions,
)
from developmental_recursion.parent_decision import (  # noqa: E402
    admit_parent_decision, parent_request_fixture, perform_parent_decision,
    propose_parent_decision, read_parent_action, read_parent_decision,
)
from developmental_recursion.parent_speech import (  # noqa: E402
    read_child_uptake, read_parent_utterance,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)
import run_p4  # noqa: E402
import run_p6  # noqa: E402

PARENT_ID = "TEST_ONLY_C03_PARENT"
PARENT_ALIAS = "P"
SECRET = "c03-b-private-motive"
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
    return run_p4.run_parent_operation(
        state, operation=operation, request=request)


def _register(state):
    _op(state, "parent-register", {
        "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
        "actor_id": PARENT_ID, "role": "parent",
        "private_state": {"motive": SECRET},
    })


def _fixture(**overrides):
    values = {**BASE, **overrides}
    return parent_material_fixture(actor_id=PARENT_ID, **values)


def _open_direct(tmp_path, name, *, overrides=None, market_items=None,
                 with_plan=True):
    state = _new_state(tmp_path, name)
    owner = run_p6.open_owner(state / "actual-p2")
    session = owner.base_owner.fanin.session
    if with_plan:
        hp = pa.historical_period_module()
        hp.establish_period_plan(session)
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": SECRET})
    pa.establish_parent_material(
        session, PARENT_ID, fixture=_fixture(**(overrides or {})))
    b04 = __import__("developmental_recursion.parent_decision",
                     fromlist=["_b04_module"])._b04_module()
    b04.establish_market_inventory(session, items=market_items)
    return owner, session


def test_two_chronological_parent_periods_on_incremental_b02(tmp_path):
    state = _new_state(tmp_path, "two-period")
    _op(state, "period-establish", {})
    _register(state)
    _op(state, "parent-establish", {"parent_id": PARENT_ID, "fixture": _fixture()})
    _op(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "h1:work",
        "activity": "PAID_WORK", "hours": 2})
    _op(state, "period-materialize", {"as_of_date": "2026-04-01"})
    _op(state, "parent-circumstance", {
        "parent_id": PARENT_ID, "operation_id": "h1:job-loss",
        "changes": {"employment_status": "unemployed",
                    "wage_units_per_hour": 0},
        "source_ref": "sourcefree:parent:job-loss"})
    _op(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "h1:care",
        "activity": "CARE_DEPENDENT", "hours": 2})
    _op(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "h1:debt",
        "activity": "PAY_DEBT", "payment": 4})
    _op(state, "period-materialize", {"as_of_date": "2026-07-01"})
    _op(state, "parent-circumstance", {
        "parent_id": PARENT_ID, "operation_id": "h2:rehire",
        "changes": {"employment_status": "employed",
                    "wage_units_per_hour": 6},
        "source_ref": "sourcefree:parent:rehire"})
    _op(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "h2:work",
        "activity": "PAID_WORK", "hours": 1})
    _op(state, "market-establish", {})
    _op(state, "parent-decide", {
        "parent_id": PARENT_ID, "operation_id": "h2:decision",
        "request": parent_request_fixture(
            kind="junior", owner_actor_id=PARENT_ID)})
    _op(state, "parent-perform", {
        "parent_id": PARENT_ID, "decision_id": "h2:decision"})
    run_p6.experience(state, Namespace(command="view"))

    reopened = load_p2().open(state / "actual-p2")
    try:
        session = reopened.session
        material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert material["period_context"]["period"]["period_id"] == "period:2026-h2"
        assert material["period_context"]["as_of_date"] == "2026-07-01"
        assert material["period_context"]["b02_employment_applied_to_parent"] is False
        assert material["material"]["employment_status"] == "employed"
        assert material["material"]["debt_units"] == 0
        assert material["material"]["care_hours_due"] == 0
        assert material["material"]["cash_units"] == 72
        assert material["material"]["free_hours"] == 2
        options = parent_feasible_actions(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert options["period_qualification"] == "B02_PERIOD_CONTEXT_READ"
        assert "PAID_WORK" in options["admissible"]

        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        by_op = {row["operation_id"]: row for row in history["history"]
                 if row["operation_id"]}
        assert by_op["h1:work"]["period_context"]["period"]["period_id"] == (
            "period:2026-h1")
        assert by_op["h2:work"]["period_context"]["period"]["period_id"] == (
            "period:2026-h2")
        assert history["material_consistent"] is True
        assert history["purchase_episode_count"] == 1

        h1 = read_parent_activity(
            session, PARENT_ID, "h1:work", as_actor=PARENT_ID)
        assert h1["period_context"]["period"]["period_id"] == "period:2026-h1"
        assert h1["period_context"]["as_of_date"] == "2026-01-01"

        # B02's own employment change is not silently the mother's.
        hp = pa.historical_period_module()
        b02 = hp.read_material_period(session, "2026-04-01")
        assert b02["employment"]["term_id"] == "employment:civic-works"
        parent_material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert parent_material["employment_basis"]["source"] == "PARENT_ACTOR_LOCAL"
        assert parent_material["employment_basis"][
            "b02_employment_applied_to_parent"] is False
    finally:
        reopened.close()

    # Source severance: current period qualification is withheld; the committed
    # historical activity receipt keeps its period context; restoration requalifies.
    reopened = load_p2().open(state / "actual-p2")
    try:
        session = reopened.session
        hp = pa.historical_period_module()
        plan_slot = hp.PERIOD_SLOT
        plan_document = dict(session.world().resources[plan_slot])
        world = session.world()
        world.resources.pop(plan_slot)
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID
        )["period_qualification"] == "B02_PERIOD_CONTEXT_UNQUALIFIED"
        held = parent_feasible_actions(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert held["admissible"] == []
        assert all(row["status"] == "HELD" for row in held["options"])
        assert read_parent_activity(
            session, PARENT_ID, "h1:work", as_actor=PARENT_ID
        )["period_context"]["period"]["period_id"] == "period:2026-h1"
        world = session.world()
        world.resources[plan_slot] = plan_document
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored = parent_feasible_actions(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert restored["period_qualification"] == "B02_PERIOD_CONTEXT_READ"
        assert "PAID_WORK" in restored["admissible"]
    finally:
        reopened.close()


@pytest.mark.parametrize("case,overrides,market_items,expected_action,reason", [
    ("baseline", {}, None, "PURCHASE", None),
    ("debt", {"debt_units": 80}, None, "DECLINE", "OBLIGATION_DEBT"),
    ("care", {"care_hours_due": 8}, None, "DECLINE", "OBLIGATION_CARE"),
    ("cash", {"cash_units": 30}, None, "DECLINE", "INSUFFICIENT_PARENT_CASH"),
    ("currency", {"currency_unit": "parent_sourcefree_currency_unit"},
     None, "DECLINE", "CURRENCY_MISMATCH"),
    ("stock", {}, [{"object_id": "object:junior-drum-kit",
                    "kind": "junior_drum_kit", "quantity": 0,
                    "unit_price": 40}], "DECLINE", "STOCK_UNAVAILABLE"),
])
def test_parent_decision_changes_from_actual_obligations_stock_and_currency(
        tmp_path, case, overrides, market_items, expected_action, reason):
    owner, session = _open_direct(
        tmp_path, "decision-" + case, overrides=overrides,
        market_items=market_items)
    try:
        proposal = propose_parent_decision(
            session, PARENT_ID,
            request=parent_request_fixture(
                kind="junior", owner_actor_id=PARENT_ID),
            as_actor=PARENT_ID)
        assert proposal["evaluation"]["action"] == expected_action
        if reason is not None:
            assert reason in proposal["evaluation"]["reasons"]
        assert proposal["evaluation"]["request"]["owner_actor_id"] == PARENT_ID
        assert proposal["nadia_state"] == "NOT_READ"
    finally:
        owner.close()


def test_parent_decision_ignores_nadia_state_and_holds_without_b02(tmp_path):
    owner, session = _open_direct(tmp_path, "decision-nadia")
    try:
        request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
        before = propose_parent_decision(
            session, PARENT_ID, request=request, as_actor=PARENT_ID)
        assert before["evaluation"]["action"] == "PURCHASE"
        world = session.world()
        world.actor_state["A"]["cash"] = 0
        session.product._checkpoint(session.branch_id, world.clock, world)
        after = propose_parent_decision(
            session, PARENT_ID, request=request, as_actor=PARENT_ID)
        assert after["evaluation"]["action"] == "PURCHASE"
        assert after["source"] == before["source"]
    finally:
        owner.close()

    owner, session = _open_direct(
        tmp_path, "decision-no-b02", with_plan=False)
    try:
        held = propose_parent_decision(
            session, PARENT_ID,
            request=parent_request_fixture(
                kind="junior", owner_actor_id=PARENT_ID),
            as_actor=PARENT_ID)
        assert held["evaluation"]["action"] == "HOLD"
        assert "B02_PERIOD_UNAVAILABLE" in held["evaluation"]["unknowns"]
    finally:
        owner.close()


def test_parent_decision_perform_replay_stale_and_cold(tmp_path):
    state = _new_state(tmp_path, "perform")
    _op(state, "period-establish", {})
    _register(state)
    _op(state, "parent-establish", {"parent_id": PARENT_ID, "fixture": _fixture()})
    _op(state, "market-establish", {})
    request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
    decision = _op(state, "parent-decide", {
        "parent_id": PARENT_ID, "operation_id": "decision:1",
        "request": request})
    assert decision["result"]["decision"]["action"] == "PURCHASE"
    owner_before = run_p6.open_owner(state / "actual-p2")
    try:
        holder_cash_before = owner_before.base_owner.fanin.session.world(
        ).actor_state["A"]["cash"]
    finally:
        owner_before.close()
    action = _op(state, "parent-perform", {
        "parent_id": PARENT_ID, "decision_id": "decision:1"})
    assert action["result"]["status"] == "PERFORMED"
    assert action["result"]["performed"] is True
    assert action["result"]["purchase"]["status"] == "ADMITTED"
    assert action["result"]["purchase"]["parent_cash_after"] == 60
    assert action["result"]["purchase"]["parent_free_hours_after"] == 7

    reopened = run_p6.open_owner(state / "actual-p2")
    try:
        session = reopened.base_owner.fanin.session
        material = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        assert material["material"]["cash_units"] == 60
        assert material["material"]["free_hours"] == 7
        assert session.world().actor_state["A"]["cash"] == holder_cash_before
        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        assert history["purchase_episode_count"] == 1
        assert history["material_consistent"] is True
        assert read_parent_decision(
            session, PARENT_ID, "decision:1", as_actor=PARENT_ID
        )["performed"] is True
        assert read_parent_action(
            session, PARENT_ID, "decision:1", as_actor=PARENT_ID
        )["receipt"]["status"] == "PERFORMED"
    finally:
        reopened.close()

    replay = _op(state, "parent-perform", {
        "parent_id": PARENT_ID, "decision_id": "decision:1"})
    assert replay["result"]["status"] == "REPLAY"
    assert replay["recorded_activity"] is False
    reopened = load_p2().open(state / "actual-p2")
    try:
        session = reopened.session
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID
        )["material"]["cash_units"] == 60
    finally:
        reopened.close()

    # A later obligation change invalidates the admitted decision; perform
    # fails closed instead of executing the stale purchase.
    _op(state, "parent-decide", {
        "parent_id": PARENT_ID, "operation_id": "decision:2",
        "request": request})
    _op(state, "parent-circumstance", {
        "parent_id": PARENT_ID, "operation_id": "debt:80",
        "changes": {"debt_units": 80}, "source_ref": "sourcefree:parent:debt"})
    with pytest.raises(RecursionRefusal, match="PARENT_DECISION_STALE"):
        _op(state, "parent-perform", {
            "parent_id": PARENT_ID, "decision_id": "decision:2"})
    reopened = run_p6.open_owner(state / "actual-p2")
    try:
        session = reopened.base_owner.fanin.session
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID
        )["material"]["cash_units"] == 60
        assert read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID
        )["purchase_episode_count"] == 1
    finally:
        reopened.close()
    run_p6.experience(state, Namespace(command="view"))

    # C03 refuses a currency mismatch before B04 can debit.
    owner, session = _open_direct(
        tmp_path, "currency-refusal",
        overrides={"currency_unit": "parent_sourcefree_currency_unit"})
    try:
        proposal = propose_parent_decision(
            session, PARENT_ID,
            request=parent_request_fixture(
                kind="junior", owner_actor_id=PARENT_ID),
            as_actor=PARENT_ID)
        assert proposal["evaluation"]["action"] == "DECLINE"
        assert "CURRENCY_MISMATCH" in proposal["evaluation"]["reasons"]
        assert read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID
        )["purchase_episode_count"] == 0
    finally:
        owner.close()


def test_parent_utterance_hidden_reason_child_uptake_and_severance(tmp_path):
    state = _new_state(tmp_path, "speech")
    _op(state, "period-establish", {})
    _register(state)
    _op(state, "parent-establish", {"parent_id": PARENT_ID, "fixture": _fixture()})
    _op(state, "market-establish", {})
    request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
    _op(state, "parent-decide", {
        "parent_id": PARENT_ID, "operation_id": "decision:speech",
        "request": request})
    first = _op(state, "parent-speak", {
        "parent_id": PARENT_ID, "decision_id": "decision:speech",
        "text": "Not this time.", "hidden_reason": {"reason": HIDDEN_A},
        "operation_id": "speech:1"})
    second = _op(state, "parent-speak", {
        "parent_id": PARENT_ID, "decision_id": "decision:speech",
        "text": "Not this time.", "hidden_reason": {"reason": HIDDEN_B},
        "operation_id": "speech:2"})
    assert first["result"]["child_perception_channel"] == "speech"
    assert first["result"]["event_id"] != second["result"]["event_id"]
    run_p6.experience(state, Namespace(command="view"))
    said = run_p6.experience(state, Namespace(
        command="say", text="hello", request_edge=False, request_id=None))
    assert said.get("admission") == "ADMITTED"

    reopened = run_p6.open_owner(state / "actual-p2")
    try:
        session = reopened.base_owner.fanin.session
        child_id = session.read_root()["actor_ids"][0]
        child_a = read_child_uptake(
            session, child_id, first["result"]["event_id"])
        child_b = read_child_uptake(
            session, child_id, second["result"]["event_id"])
        assert child_a["status"] == "PERCEIVED"
        assert child_b["status"] == "PERCEIVED"
        assert child_a["event"]["body_public"]["text"] == "Not this time."
        assert child_b["event"]["body_public"]["text"] == "Not this time."
        assert HIDDEN_A not in json.dumps(child_a)
        assert HIDDEN_B not in json.dumps(child_b)
        parent_a = read_parent_utterance(
            session, PARENT_ID, "speech:1", as_actor=PARENT_ID)
        parent_b = read_parent_utterance(
            session, PARENT_ID, "speech:2", as_actor=PARENT_ID)
        assert parent_a["hidden_reason"] == {"reason": HIDDEN_A}
        assert parent_b["hidden_reason"] == {"reason": HIDDEN_B}
        assert HIDDEN_A not in json.dumps(
            session.event(first["result"]["event_id"]))

        # Severing the spoken event removes Nadia's uptake, not the parent's
        # prior decision record.
        original_event = session.event
        session.event = lambda event_id: (
            None if event_id == first["result"]["event_id"]
            else original_event(event_id))
        try:
            with pytest.raises(
                    RecursionRefusal, match="CHILD_UPTAKE_EVENT_SEVERED"):
                read_child_uptake(session, child_id, first["result"]["event_id"])
            assert read_parent_decision(
                session, PARENT_ID, "decision:speech", as_actor=PARENT_ID
            )["status"] == "READ"
        finally:
            session.event = original_event
    finally:
        reopened.close()

    # No child receipt is created from co-presence alone when the child is
    # elsewhere; the parent utterance remains a real event.
    reopened = run_p6.open_owner(state / "actual-p2")
    try:
        session = reopened.base_owner.fanin.session
        child_id = session.read_root()["actor_ids"][0]
        child_alias = next(
            alias for alias, row in session.world().actor_state.items()
            if row.get("actor_id") == child_id)
        world = session.world()
        world.positions[child_alias] = "market"
        session.product._checkpoint(session.branch_id, world.clock, world)
        from developmental_recursion.parent_speech import (
            perform_parent_utterance,
        )
        result = perform_parent_utterance(
            session, PARENT_ID, decision_id="decision:speech",
            text="Not this time.", hidden_reason={"reason": HIDDEN_A},
            operation_id="speech:3")
        assert read_child_uptake(
            session, child_id, result["event_id"]
        )["status"] == "NOT_PERCEIVED"
        assert session.event(result["event_id"]) is not None
    finally:
        reopened.close()

def test_admitted_parent_decision_declines_on_real_obligation(tmp_path):
    owner, session = _open_direct(
        tmp_path, "admitted-debt", overrides={"debt_units": 80})
    try:
        request = parent_request_fixture(
            kind="junior", owner_actor_id=PARENT_ID)
        decision = admit_parent_decision(
            session, PARENT_ID, operation_id="admitted:debt",
            request=request, as_actor=PARENT_ID)
        assert decision["decision"]["action"] == "DECLINE"
        assert "OBLIGATION_DEBT" in decision["decision"]["reasons"]
        action = perform_parent_decision(
            session, PARENT_ID, decision_id="admitted:debt",
            as_actor=PARENT_ID)
        assert action["status"] == "VALID_EMPTY"
        assert action["performed"] is False
        assert read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID
        )["purchase_episode_count"] == 0
    finally:
        owner.close()
