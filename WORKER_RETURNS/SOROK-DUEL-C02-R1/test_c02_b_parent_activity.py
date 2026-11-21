"""C02 Agent B proof: truthful parent activity, history-bound material, held B02.

Targets defects established against Agent A's C02 cut:
- an ordinary parent activity was carried by the OFFSCREEN_REPAIR kind and an
  owner receipt that literally attested a repair;
- current parent material was not bound to the latest C12 parent history, so a
  recomputed or tampered material source could survive a read;
- read_parent_activity trusted an event mapping without validating the author,
  body, owner receipt or own_action perception;
- the parent-local material boundary was not explicit for C03/B04.
"""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
REPO = RETURNS.parent
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
PROJECTION = RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
for _path in (P6, PROJECTION, ENGINE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import load_p2  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    PARENT_ACTIVITY_EVENT_KIND,
    PARENT_B02_HOLD,
    _material_source,
    commit_parent_circumstances,
    establish_parent_material,
    parent_feasible_actions,
    parent_material_fixture,
    read_parent_activity,
    read_parent_history,
    read_parent_material,
    record_parent_activity,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
    read_supporting_actor,
    register_supporting_actor,
)
from s45_projection.projection import project_event  # noqa: E402

PARENT_ID = "TEST_ONLY_C02_B_PARENT"
PARENT_ALIAS = "P"
SECRET = "c02-b-private-motive-do-not-expose"
BASELINE = {
    "employment_status": "employed",
    "wage_units_per_hour": 5,
    "debt_units": 4,
    "care_hours_due": 2,
    "cash_units": 20,
    "free_hours": 8,
    "source_ref": "sourcefree:parent:antecedent:baseline",
}


def start(tmp_path, name="actual-p2"):
    return load_p2().start(tmp_path / name)


def register(fanin):
    return register_supporting_actor(
        fanin.session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": SECRET},
    )


def establish(session, **overrides):
    values = {**BASELINE, **overrides}
    fixture = parent_material_fixture(actor_id=PARENT_ID, **values)
    return establish_parent_material(session, PARENT_ID, fixture=fixture)


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def options(session):
    return parent_feasible_actions(session, PARENT_ID, as_actor=PARENT_ID)


def by_activity(result):
    return {row["activity"]: row for row in result["options"]}


def test_parent_activity_truthful_event_and_actual_consumers(tmp_path):
    fanin = start(tmp_path, "truth")
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register(fanin)
        establish(session)
        receipt = record_parent_activity(
            session, PARENT_ID, operation_id="c02b:truth:work",
            activity="PAID_WORK", hours=2)
        event = session.event(receipt["event_id"])
        assert receipt["status"] == "ADMITTED"
        assert receipt["event_kind"] == PARENT_ACTIVITY_EVENT_KIND
        assert receipt["event_authored_by"] == PARENT_ALIAS
        assert event["kind"] == PARENT_ACTIVITY_EVENT_KIND
        assert event["owner_receipt"]["act"] == PARENT_ACTIVITY_EVENT_KIND
        assert event["actor_id"] == PARENT_ALIAS
        assert event["body"]["activity"] == "PAID_WORK"
        assert event["body"]["household_effect"] == "NONE_PARENT_LOCAL_ONLY"
        assert "OFFSCREEN_REPAIR" not in json.dumps(event)

        projected = project_event(event)
        assert projected["kind"] == PARENT_ACTIVITY_EVENT_KIND
        assert projected["summary"] == "The parent works a paid shift."
        # The existing projection whitelist does not expose activity params;
        # the truthful receipt below is the actual consumer input.
        self_read = read_parent_activity(
            session, PARENT_ID, "c02b:truth:work", as_actor=PARENT_ID)
        assert self_read["event_kind"] == PARENT_ACTIVITY_EVENT_KIND
        assert self_read["event_authored_by"] == PARENT_ALIAS
        assert self_read["receipt"]["activity"] == "PAID_WORK"
        assert self_read["receipt"]["parameters"] == {"hours": 2}
        assert self_read["material_boundary"]["household_cash"] == "NOT_READ"
        assert self_read["material_boundary"]["household_spend_permission"] == (
            "C03_B04_HELD")
        assert self_read["material_boundary"]["currency_conversion"] == (
            "NOT_APPLIED")
        material_read = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert material_read["material"]["currency_unit"] == (
            "parent_sourcefree_currency_unit")
        assert material_read["material_boundary"]["parent_currency_unit"] == (
            "parent_sourcefree_currency_unit")
        assert material_read["material_boundary"]["household_currency_unit"] == (
            "NOT_READ")
        assert self_read["period_qualification"] == PARENT_B02_HOLD
        assert SECRET not in json.dumps(self_read)

        # Actual objective visibility remains separate: Nadia did not perceive
        # the parent's activity, and C01's focal-event access does not invent it.
        assert read_actor_access(
            session, focal, receipt["event_id"])["status"] == "NOT_PERCEIVED"
        with pytest.raises(
                RecursionRefusal, match="PARTICIPATION_SEVERED"):
            read_actor_access(session, PARENT_ID, receipt["event_id"])

        # The actual existing ipb4/C12 world verifier accepts the new vocabulary
        # only because the owner receipt names the same truthful act.
        from bp4.c10 import _verify_world
        _verify_world(session.product.store.latest_state(session.branch_id))
    finally:
        fanin.close()


def test_current_material_is_bound_to_parent_history_and_severance(tmp_path,
                                                                  monkeypatch):
    fanin = start(tmp_path, "history")
    try:
        session = fanin.session
        register(fanin)
        establish(session)
        receipt = record_parent_activity(
            session, PARENT_ID, operation_id="c02b:history:work",
            activity="PAID_WORK", hours=2)
        alias = read_supporting_actor(session, PARENT_ID)["alias"]
        before = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        before_options = options(session)
        assert before["material_boundary"]["double_counting"] == (
            "NO_HOUSEHOLD_EFFECT_APPLIED")
        assert before["historical_ingress"]["status"] == PARENT_B02_HOLD
        assert before["historical_ingress"]["dates_claimed"] is False

        # A recomputed content address cannot substitute for a C12 history row.
        world = session.world()
        document = dict(world.actor_state[alias]["material"])
        tampered = dict(
            document, cash_units=999999,
            source=_material_source({**document, "cash_units": 999999}))
        world.actor_state[alias]["material"] = tampered
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(
                RecursionRefusal, match="MATERIAL_HISTORY_MISMATCH"):
            read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        with pytest.raises(
                RecursionRefusal, match="MATERIAL_HISTORY_MISMATCH"):
            options(session)
        world = session.world()
        world.actor_state[alias]["material"] = document
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["source"] == before["source"]
        assert options(session)["options"] == before_options["options"]

        # Sever the activity episode: the past world event remains, but the
        # parent's later material/options read fails closed instead of silently
        # trusting a detached material document.
        episode = next(
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "P2_PARENT_ACTIVITY"
            and (row.get("body") or {}).get("operation_id") == "c02b:history:work")
        original = session.product.store.episodes

        def severed(branch_id):
            return [row for row in original(branch_id)
                    if row.get("episode_id") != episode["episode_id"]]

        monkeypatch.setattr(session.product.store, "episodes", severed)
        with pytest.raises(
                RecursionRefusal, match="MATERIAL_HISTORY_MISMATCH"):
            read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        with pytest.raises(
                RecursionRefusal, match="MATERIAL_HISTORY_MISMATCH"):
            options(session)
        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        assert history["material_consistent"] is False
        assert all(row["operation_id"] != "c02b:history:work"
                   for row in history["history"])
        assert session.event(receipt["event_id"]) is not None
        with pytest.raises(
                RecursionRefusal, match="ACTIVITY_NOT_FOUND"):
            read_parent_activity(
                session, PARENT_ID, "c02b:history:work", as_actor=PARENT_ID)
        monkeypatch.undo()
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["source"] == before["source"]
        assert read_parent_activity(
            session, PARENT_ID, "c02b:history:work", as_actor=PARENT_ID
        )["event_kind"] == PARENT_ACTIVITY_EVENT_KIND
    finally:
        fanin.close()


def test_activity_read_validates_author_body_receipt_and_perception(tmp_path,
                                                                   monkeypatch):
    fanin = start(tmp_path, "validate")
    try:
        session = fanin.session
        register(fanin)
        establish(session)
        record_parent_activity(
            session, PARENT_ID, operation_id="c02b:validate:work",
            activity="PAID_WORK", hours=2)
        original_event = session.event

        def forged_author(event_id):
            event = original_event(event_id)
            return dict(event, actor_id="A")

        monkeypatch.setattr(session, "event", forged_author)
        with pytest.raises(
                RecursionRefusal, match="ACTIVITY_EVENT_MISMATCH"):
            read_parent_activity(
                session, PARENT_ID, "c02b:validate:work", as_actor=PARENT_ID)
        monkeypatch.undo()

        def forged_body(event_id):
            event = original_event(event_id)
            body = dict(event.get("body") or {}, activity="PAY_DEBT")
            return dict(event, body=body)

        monkeypatch.setattr(session, "event", forged_body)
        with pytest.raises(
                RecursionRefusal, match="ACTIVITY_EVENT_MISMATCH"):
            read_parent_activity(
                session, PARENT_ID, "c02b:validate:work", as_actor=PARENT_ID)
        monkeypatch.undo()

        def forged_receipt(event_id):
            event = original_event(event_id)
            receipt = dict(event.get("owner_receipt") or {},
                           act="OFFSCREEN_REPAIR")
            return dict(event, owner_receipt=receipt)

        monkeypatch.setattr(session, "event", forged_receipt)
        with pytest.raises(
                RecursionRefusal, match="OWNER_RECEIPT_INVALID"):
            read_parent_activity(
                session, PARENT_ID, "c02b:validate:work", as_actor=PARENT_ID)
        monkeypatch.undo()

        store = session.product.store
        original_perceptions = store.perceptions

        def severed(branch_id, actor_id=None):
            rows = original_perceptions(branch_id, actor_id)
            return [row for row in rows if row.get("channel") != "own_action"]

        monkeypatch.setattr(store, "perceptions", severed)
        with pytest.raises(
                RecursionRefusal, match="PERCEPTION_SEVERED"):
            read_parent_activity(
                session, PARENT_ID, "c02b:validate:work", as_actor=PARENT_ID)
        monkeypatch.undo()
        assert read_parent_activity(
            session, PARENT_ID, "c02b:validate:work",
            as_actor=PARENT_ID)["status"] == "READ"
    finally:
        fanin.close()


def test_options_change_independently_before_any_child_request(tmp_path):
    fanin = start(tmp_path, "options")
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register(fanin)
        establish(session)
        assert by_activity(options(session))["PAID_WORK"]["status"] == "ADMISSIBLE"

        with pytest.raises(RecursionRefusal, match="CIRCUMSTANCE_SCHEMA"):
            commit_parent_circumstances(
                session, PARENT_ID, operation_id="c02b:circumstance:currency",
                changes={"currency_unit": "household_currency_unit"},
                source_ref="sourcefree:parent:currency-conversion")
        changed = commit_parent_circumstances(
            session, PARENT_ID, operation_id="c02b:circumstance:job-loss",
            changes={"employment_status": "unemployed",
                     "wage_units_per_hour": 0},
            source_ref="sourcefree:parent:job-loss")
        assert changed["status"] == "CHANGED"
        assert changed["event_effect"] == "NONE"
        after = by_activity(options(session))
        assert after["PAID_WORK"]["status"] == "REFUSED"
        assert "EMPLOYMENT_NOT_AVAILABLE" in after["PAID_WORK"]["reasons"]

        assert record_parent_activity(
            session, PARENT_ID, operation_id="c02b:options:debt",
            activity="PAY_DEBT", payment=4)["status"] == "ADMITTED"
        assert by_activity(options(session))["PAY_DEBT"]["reasons"] == ["NO_DEBT"]
        with pytest.raises(RecursionRefusal, match="NO_DEBT"):
            record_parent_activity(
                session, PARENT_ID, operation_id="c02b:options:debt-zero",
                activity="PAY_DEBT")
        assert record_parent_activity(
            session, PARENT_ID, operation_id="c02b:options:care",
            activity="CARE_DEPENDENT", hours=2)["status"] == "ADMITTED"
        assert by_activity(options(session))["CARE_DEPENDENT"]["reasons"] == [
            "NO_CARE_OBLIGATION"]
        with pytest.raises(RecursionRefusal, match="NO_CARE_OBLIGATION"):
            record_parent_activity(
                session, PARENT_ID, operation_id="c02b:options:care-zero",
                activity="CARE_DEPENDENT")

        # The parent reads never evaluate a child request or Nadia state.
        material = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        assert material["child_request"] == "NOT_EVALUATED"
        assert material["nadia_state"] == "NOT_READ"
        with pytest.raises(RecursionRefusal, match="PARENT_SELF_READ_REQUIRED"):
            read_parent_material(session, PARENT_ID, as_actor=focal)
        with pytest.raises(RecursionRefusal, match="PARENT_SELF_READ_REQUIRED"):
            parent_feasible_actions(session, PARENT_ID, as_actor=focal)
    finally:
        fanin.close()


def test_parent_activity_does_not_touch_nadia_or_household_stocks(tmp_path):
    import house
    import run_p6

    state = tmp_path / "state"
    run_p6.experience(state, Namespace(command="new"))
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        world = session.world()
        nadia_before = dict(world.actor_state["A"])
        household_before = house.read_household(session)
        dwelling_before = house.read_dwelling(session)
        feasibility_before = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        resources_before = dict(world.resources)
        register(fanin)
        establish(session)
        options_before = options(session)

        assert record_parent_activity(
            session, PARENT_ID, operation_id="c02b:join:work",
            activity="PAID_WORK", hours=2)["status"] == "ADMITTED"
        assert record_parent_activity(
            session, PARENT_ID, operation_id="c02b:join:debt",
            activity="PAY_DEBT", payment=1)["status"] == "ADMITTED"
        assert record_parent_activity(
            session, PARENT_ID, operation_id="c02b:join:care",
            activity="CARE_DEPENDENT", hours=1)["status"] == "ADMITTED"

        after = session.world()
        assert after.actor_state["A"] == nadia_before
        assert after.resources == resources_before
        assert house.read_household(session)["source"] == household_before["source"]
        assert house.read_dwelling(session)["source"] == dwelling_before["source"]
        assert house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])["status"] == (
                feasibility_before["status"])
        parent_after = options(session)
        assert parent_after["options"] != options_before["options"]
        assert parent_after["material_boundary"]["household_cash"] == "NOT_READ"
        assert parent_after["material_boundary"]["household_spend_permission"] == (
            "C03_B04_HELD")
        assert parent_after["material_boundary"]["currency_conversion"] == (
            "NOT_APPLIED")
        assert parent_after["material"]["currency_unit"] == (
            "parent_sourcefree_currency_unit")
    finally:
        owner.close()


def test_p6_view_after_direct_parent_write_is_held_by_p4_ledger(tmp_path):
    # Actual P6 product boundary: a direct C12/P2 write (even C01 registration,
    # verified separately) is outside the P4 turn ledger, so a later P6 view
    # refuses P4_COLD_STATE_MISMATCH. C02 does not claim a P6 live-turn join;
    # the static B01/B03/P6 house-read composition is the proven boundary.
    import run_p6

    state = tmp_path / "state"
    run_p6.experience(state, Namespace(command="new"))
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        fanin = owner.base_owner.fanin
        session = fanin.session
        register(fanin)
        establish(session)
        record_parent_activity(
            session, PARENT_ID, operation_id="c02b:p6:work",
            activity="PAID_WORK", hours=2)
    finally:
        owner.close()
    with pytest.raises(RecursionRefusal, match="P4_COLD_STATE_MISMATCH"):
        run_p6.experience(state, Namespace(command="view"))


def test_truthful_activity_cold_replay_and_no_duplicate_effects(tmp_path):
    fanin = start(tmp_path, "cold")
    try:
        session = fanin.session
        register(fanin)
        establish(session)
        first = record_parent_activity(
            session, PARENT_ID, operation_id="c02b:cold:work",
            activity="PAID_WORK", hours=2)
        material = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        baseline = counts(session)
        replay = record_parent_activity(
            session, PARENT_ID, operation_id="c02b:cold:work",
            activity="PAID_WORK", hours=2)
        assert replay["status"] == "REPLAY"
        assert replay["event_id"] == first["event_id"]
        assert counts(session) == baseline
        after_replay = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert after_replay["source"] == material["source"]
        assert after_replay["material"]["cash_units"] == 30
        assert after_replay["material"]["free_hours"] == 6
        # A later state must refuse the old operation instead of duplicating
        # its cash effect.
        assert record_parent_activity(
            session, PARENT_ID, operation_id="c02b:cold:care",
            activity="CARE_DEPENDENT", hours=1)["status"] == "ADMITTED"
        with pytest.raises(RecursionRefusal, match="REPLAY_STALE"):
            record_parent_activity(
                session, PARENT_ID, operation_id="c02b:cold:work",
                activity="PAID_WORK", hours=2)
        counts_before_close = counts(session)
        source_before_close = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["source"]
    finally:
        fanin.close()

    reopened = load_p2().open(tmp_path / "cold")
    try:
        session = reopened.session
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["source"] == source_before_close
        assert read_parent_activity(
            session, PARENT_ID, "c02b:cold:work",
            as_actor=PARENT_ID)["event_kind"] == PARENT_ACTIVITY_EVENT_KIND
        replay = record_parent_activity(
            session, PARENT_ID, operation_id="c02b:cold:care",
            activity="CARE_DEPENDENT", hours=1)
        assert replay["status"] == "REPLAY"
        assert counts(session) == counts_before_close
    finally:
        reopened.close()

    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.p2_owner import load_p2
from developmental_recursion.parent_activity import parent_feasible_actions, read_parent_history, read_parent_material, read_parent_activity
fanin = load_p2().open(Path(sys.argv[2]))
try:
    session = fanin.session
    print(json.dumps({
        "material": read_parent_material(session, sys.argv[3], as_actor=sys.argv[3]),
        "options": parent_feasible_actions(session, sys.argv[3], as_actor=sys.argv[3]),
        "history": read_parent_history(session, sys.argv[3], as_actor=sys.argv[3]),
        "activity": read_parent_activity(session, sys.argv[3], "c02b:cold:work", as_actor=sys.argv[3]),
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(REPO),
         str(tmp_path / "cold"), PARENT_ID],
        cwd=REPO, capture_output=True, text=True, timeout=120, check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["material"]["source"] == source_before_close
    assert cold["activity"]["event_kind"] == PARENT_ACTIVITY_EVENT_KIND
    assert cold["history"]["material_consistent"] is True
    assert cold["material"]["period_qualification"] == PARENT_B02_HOLD
    assert SECRET not in completed.stdout
