"""C02 A relay: normal live-root parent background + B02 current-period ingress."""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[2]
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P5 = RETURNS / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
P4 = RETURNS / "SOROK-P4-FIRST-FULL-MPC-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (P6, P5, P4, ENGINE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import run_p4  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import load_p2  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    PARENT_B02_FULL_PROOF,
    PARENT_B02_QUALIFIED,
    PARENT_B02_UNQUALIFIED,
    parent_feasible_actions,
    parent_material_fixture,
    read_parent_activity,
    read_parent_history,
    read_parent_material,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
)

PARENT_ID = "TEST_ONLY_LIVE_PARENT"
PARENT_ALIAS = "P"
SECRET = "live-root-private-motive"
BASELINE = {
    "employment_status": "employed",
    "wage_units_per_hour": 5,
    "debt_units": 4,
    "care_hours_due": 2,
    "cash_units": 20,
    "free_hours": 8,
    "source_ref": "sourcefree:live:parent:baseline",
}


def new_state(state):
    return run_p6.experience(state, Namespace(command="new"))


def background(state, operation, request):
    return run_p6.parent_background_operation(
        state, operation=operation, request=request)


def ledger(state):
    return json.loads((state / "p4_receipts.json").read_text())


def open_read(state):
    return load_p2().open(state / "actual-p2")


def test_normal_live_root_parent_b02_view_and_user_turn_cold(tmp_path):
    state = tmp_path / "live"
    new_state(state)
    owner_before = run_p6.open_owner(state / "actual-p2")
    try:
        psychology_head = owner_before.store.head()
    finally:
        owner_before.close()
    period = background(state, "period-establish", {})
    assert period["recorded_activity"] is True
    assert period["result"]["periods"][0]["period_id"] == "period:2026-h1"
    assert ledger(state)["pending"] is None

    registered = background(state, "parent-register", {
        "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
        "actor_id": PARENT_ID, "role": "parent",
        "private_state": {"motive": SECRET},
    })
    assert registered["result"]["status"] == "REGISTERED"
    registered_view = run_p6.experience(state, Namespace(command="view"))
    assert registered_view["room"] == "workshop"
    assert "status" not in registered_view or (
        registered_view.get("status") != "REFUSED")
    fixture = parent_material_fixture(actor_id=PARENT_ID, **BASELINE)
    established = background(state, "parent-establish", {
        "parent_id": PARENT_ID, "fixture": fixture,
    })
    assert established["result"]["status"] == "REGISTERED"
    assert established["result"]["period_qualification"] == PARENT_B02_QUALIFIED
    assert established["result"]["period_context"]["period"]["period_id"] == (
        "period:2026-h1")
    assert established["result"]["period_context"][
        "b02_employment_applied_to_parent"] is False
    assert established["result"]["period_context"]["full_dated_proof"] == (
        PARENT_B02_FULL_PROOF)

    activity = background(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "live:activity:1",
        "activity": "PAID_WORK", "hours": 2,
    })
    assert activity["result"]["status"] == "ADMITTED"
    assert activity["result"]["event_kind"] == "MATERIAL_ACTIVITY"
    assert activity["result"]["period_qualification"] == PARENT_B02_QUALIFIED
    assert activity["result"]["period_context"]["logical_tick"] == (
        activity["result"]["clock"])
    assert activity["result"]["period_context"]["period"]["period_id"] == (
        "period:2026-h1")
    assert activity["result"]["period_context"]["source_binding"][
        "employment_applied_to_parent"] is False
    assert ledger(state)["pending"] is None
    assert len(ledger(state)["activity_turns"]) == 4
    assert len(ledger(state)["turns"]) == 0
    activity_turns = len(ledger(state)["activity_turns"])
    replay = background(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "live:activity:1",
        "activity": "PAID_WORK", "hours": 2,
    })
    assert replay["result"]["status"] == "REPLAY"
    assert replay["recorded_activity"] is False
    assert len(ledger(state)["activity_turns"]) == activity_turns
    owner_after = run_p6.open_owner(state / "actual-p2")
    try:
        assert owner_after.store.head() == psychology_head
    finally:
        owner_after.close()

    view = run_p6.experience(state, Namespace(command="view"))
    assert view["room"] == "workshop"
    assert "The parent works a paid shift." not in json.dumps(view)
    assert SECRET not in json.dumps(view)
    assert "status" not in view or view.get("status") != "REFUSED"

    say = run_p6.experience(state, Namespace(
        command="say", text="hello", request_edge=False, request_id=None))
    assert say.get("admission") == "ADMITTED"
    assert "status" not in say or say.get("status") != "REFUSED"
    assert len(ledger(state)["turns"]) == 1
    assert ledger(state)["pending"] is None
    assert "The parent works a paid shift." not in json.dumps(say)
    assert SECRET not in json.dumps(say)

    reopened = open_read(state)
    try:
        session = reopened.session
        material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        options = parent_feasible_actions(
            session, PARENT_ID, as_actor=PARENT_ID)
        evidence = read_parent_activity(
            session, PARENT_ID, "live:activity:1", as_actor=PARENT_ID)
        history = read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert material["period_qualification"] == PARENT_B02_QUALIFIED
        assert material["period_context"]["period"]["period_id"] == (
            "period:2026-h1")
        assert material["material"]["currency_unit"] == (
            "parent_sourcefree_currency_unit")
        assert options["admissible"] == [
            "PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"]
        assert options["period_qualification"] == PARENT_B02_QUALIFIED
        assert evidence["event_kind"] == "MATERIAL_ACTIVITY"
        assert evidence["period_context"]["logical_tick"] == (
            evidence["clock"])
        assert history["period_context"]["period"]["period_id"] == (
            "period:2026-h1")
        assert any(row["period_context"]["period"]["period_id"] == (
            "period:2026-h1") for row in history["history"])
        assert SECRET not in json.dumps(material)
        assert SECRET not in json.dumps(options)
        assert SECRET not in json.dumps(evidence)
        focal = session.read_root()["actor_ids"][0]
        assert read_actor_access(
            session, focal, evidence["event"]["event_id"])["status"] == (
                "NOT_PERCEIVED")
        assert evidence["event"]["event_id"] not in session.user_perceived_ids()
    finally:
        reopened.close()


def test_cold_process_view_and_user_turn_after_parent_activity(tmp_path):
    state = tmp_path / "cold-process"
    new_state(state)
    background(state, "period-establish", {})
    background(state, "parent-register", {
        "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
        "actor_id": PARENT_ID, "role": "parent",
        "private_state": {"motive": SECRET},
    })
    background(state, "parent-establish", {
        "parent_id": PARENT_ID,
        "fixture": parent_material_fixture(actor_id=PARENT_ID, **BASELINE),
    })
    background(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "cold:activity:1",
        "activity": "PAID_WORK", "hours": 2,
    })
    script = r"""
import json, sys
from argparse import Namespace
from pathlib import Path
repo = Path(sys.argv[1])
for rel in ("WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1",
            "WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1",
            "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1",
            "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"):
    sys.path.insert(0, str(repo / rel))
import run_p6
view = run_p6.experience(Path(sys.argv[2]), Namespace(command="view"))
say = run_p6.experience(Path(sys.argv[2]), Namespace(
    command="say", text="hello", request_edge=False, request_id=None))
print(json.dumps({"view": view, "say": say}, sort_keys=True))
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(RETURNS.parent), str(state)],
        cwd=RETURNS.parent, capture_output=True, text=True, timeout=180,
        check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["view"]["room"] == "workshop"
    assert cold["say"].get("admission") == "ADMITTED"
    assert SECRET not in completed.stdout
    assert "The parent works a paid shift." not in completed.stdout
    saved = ledger(state)
    assert saved["pending"] is None
    assert len(saved["turns"]) == 1


def test_corrupted_root_still_refuses_and_pending_refuses(tmp_path):
    state = tmp_path / "corrupt"
    new_state(state)
    fanin = load_p2().open(state / "actual-p2")
    try:
        from developmental_recursion.supporting_actor import (
            register_supporting_actor,
        )
        register_supporting_actor(
            fanin.session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
            role="parent", private_state={})
    finally:
        fanin.close()
    baseline_activity = len(ledger(state).get("activity_turns", []))
    with pytest.raises(RecursionRefusal, match="P4_COLD_STATE_MISMATCH"):
        run_p6.experience(state, Namespace(command="view"))
    with pytest.raises(RecursionRefusal, match="P4_COLD_STATE_MISMATCH"):
        background(state, "parent-establish", {
            "parent_id": PARENT_ID,
            "fixture": parent_material_fixture(actor_id=PARENT_ID, **BASELINE),
        })
    assert len(ledger(state).get("activity_turns", [])) == baseline_activity

    pending_state = tmp_path / "pending"
    new_state(pending_state)
    pending_ledger = ledger(pending_state)
    pending_ledger["pending"] = {
        "kind": "parent_background",
        "operation": "parent-register",
        "request": {},
    }
    (pending_state / "p4_receipts.json").write_text(
        json.dumps(pending_ledger, sort_keys=True))
    with pytest.raises(RecursionRefusal, match="PENDING_OPERATION"):
        background(pending_state, "parent-register", {
            "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
            "actor_id": PARENT_ID, "role": "parent",
            "private_state": {},
        })
    with pytest.raises(RecursionRefusal, match="PENDING_OPERATION"):
        run_p6.experience(pending_state, Namespace(command="view"))


def test_post_mutation_failure_leaves_pending_fail_stop(tmp_path, monkeypatch):
    state = tmp_path / "failstop"
    new_state(state)

    def mutate_then_fail(session, operation, request):
        from developmental_recursion.supporting_actor import (
            register_supporting_actor,
        )
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
            role="parent", private_state={})
        raise RuntimeError("injected post-write failure")

    monkeypatch.setattr(
        run_p4, "_parent_background_dispatch", mutate_then_fail)
    with pytest.raises(RuntimeError, match="injected post-write failure"):
        background(state, "parent-register", {
            "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
            "actor_id": PARENT_ID, "role": "parent", "private_state": {},
        })
    saved = ledger(state)
    assert saved["pending"]["kind"] == "parent_background"
    assert saved["pending"]["operation"] == "parent-register"
    with pytest.raises(RecursionRefusal, match="PENDING_OPERATION"):
        run_p6.experience(state, Namespace(command="view"))
    with pytest.raises(RecursionRefusal, match="PENDING_OPERATION"):
        background(state, "parent-register", {
            "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
            "actor_id": PARENT_ID, "role": "parent", "private_state": {},
        })


def test_read_only_period_context_and_no_false_b02_absent_claim(tmp_path):
    state = tmp_path / "period"
    new_state(state)
    background(state, "period-establish", {})
    background(state, "parent-register", {
        "parent_id": PARENT_ID, "alias": PARENT_ALIAS,
        "actor_id": PARENT_ID, "role": "parent", "private_state": {},
    })
    background(state, "parent-establish", {
        "parent_id": PARENT_ID,
        "fixture": parent_material_fixture(actor_id=PARENT_ID, **BASELINE),
    })
    background(state, "parent-activity", {
        "parent_id": PARENT_ID, "operation_id": "period:activity:1",
        "activity": "PAID_WORK", "hours": 2,
    })
    fanin = open_read(state)
    try:
        material = read_parent_material(
            fanin.session, PARENT_ID, as_actor=PARENT_ID)
        assert material["historical_ingress"]["status"] == PARENT_B02_QUALIFIED
        assert material["historical_ingress"]["dates_claimed"] is True
        assert material["historical_ingress"]["full_dated_proof"] == (
            PARENT_B02_FULL_PROOF)
        assert material["historical_ingress"]["required_hook"]
        assert material["historical_ingress"][
            "b02_employment_applied_to_parent"] is False
        assert material["historical_ingress"][
            "parent_employment_source"] == "PARENT_ACTOR_LOCAL"
        assert material["historical_dates"] == "B02_CURRENT_PERIOD_ONLY"
        assert material["period_context"]["as_of_date"] == "2026-01-01"
        assert material["period_context"]["interval_status"] == (
            "NOT_MATERIALIZED")
        assert material["period_context"]["full_dated_proof"] == (
            PARENT_B02_FULL_PROOF)
        activity = read_parent_activity(
            fanin.session, PARENT_ID, "period:activity:1",
            as_actor=PARENT_ID)
        assert activity["period_context"]["period"]["period_id"] == (
            "period:2026-h1")
        world = fanin.session.world()
        plan_document = world.resources.pop("p6_historical_period")
        fanin.session.product._checkpoint(
            fanin.session.branch_id, world.clock, world)
        severed = read_parent_material(
            fanin.session, PARENT_ID, as_actor=PARENT_ID)
        assert severed["period_qualification"] == PARENT_B02_UNQUALIFIED
        severed_options = parent_feasible_actions(
            fanin.session, PARENT_ID, as_actor=PARENT_ID)
        assert severed_options["admissible"] == []
        assert all(row["status"] == "HELD"
                   and row["reasons"] == ["B02_PERIOD_UNAVAILABLE"]
                   for row in severed_options["options"])
        past = read_parent_activity(
            fanin.session, PARENT_ID, "period:activity:1",
            as_actor=PARENT_ID)
        assert past["period_context"]["period"]["period_id"] == (
            "period:2026-h1")
        world = fanin.session.world()
        world.resources["p6_historical_period"] = plan_document
        fanin.session.product._checkpoint(
            fanin.session.branch_id, world.clock, world)
        restored = read_parent_material(
            fanin.session, PARENT_ID, as_actor=PARENT_ID)
        assert restored["period_qualification"] == PARENT_B02_QUALIFIED
    finally:
        fanin.close()
