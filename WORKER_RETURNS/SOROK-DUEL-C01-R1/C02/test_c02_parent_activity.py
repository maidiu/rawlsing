"""C02 sourcefree proof: independent parent material history and feasible activity."""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[2]
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
for _path in (P6, ENGINE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import load_p2  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    PARENT_B02_HOLD,
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

PARENT_ID = "TEST_ONLY_C02_PARENT"
PARENT_ALIAS = "P"
SECRET = "c02-private-motive-do-not-expose"
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
    return parent_feasible_actions(
        session, PARENT_ID, as_actor=PARENT_ID)


def by_activity(result):
    return {row["activity"]: row for row in result["options"]}


def test_parent_antecedent_and_activities_change_feasible_options(tmp_path):
    fanin = start(tmp_path)
    try:
        session = fanin.session
        root = session.read_root()
        focal = root["actor_ids"][0]
        register(fanin)
        established = establish(session)
        assert established["status"] == "REGISTERED"
        assert established["period_qualification"] == PARENT_B02_HOLD
        assert established["historical_dates"] == "NOT_AVAILABLE"
        assert "date" not in established
        assert "historical_dates" in established

        baseline = options(session)
        baseline_options = by_activity(baseline)
        assert baseline["admissible"] == ["PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"]
        assert all(row["status"] == "ADMISSIBLE"
                   for row in baseline_options.values())

        with pytest.raises(RecursionRefusal, match="PARENT_SELF_READ_REQUIRED"):
            read_parent_material(session, PARENT_ID, as_actor=focal)
        with pytest.raises(RecursionRefusal, match="PARENT_SELF_READ_REQUIRED"):
            parent_feasible_actions(session, PARENT_ID, as_actor=focal)

        debt = record_parent_activity(
            session, PARENT_ID, operation_id="c02:activity:debt",
            activity="PAY_DEBT", payment=4)
        assert debt["status"] == "ADMITTED"
        assert debt["event_authored_by"] == PARENT_ALIAS
        assert debt["period_qualification"] == PARENT_B02_HOLD
        debt_event = session.event(debt["event_id"])
        assert debt_event["actor_id"] == PARENT_ALIAS
        assert debt_event["kind"] == "OFFSCREEN_REPAIR"
        assert read_actor_access(
            session, focal, debt["event_id"])["status"] == "NOT_PERCEIVED"
        assert SECRET not in json.dumps(debt_event)
        assert SECRET not in json.dumps(debt)
        activity_read = read_parent_activity(
            session, PARENT_ID, "c02:activity:debt", as_actor=PARENT_ID)
        assert activity_read["event"]["event_id"] == debt["event_id"]
        assert activity_read["period_qualification"] == PARENT_B02_HOLD
        assert SECRET not in json.dumps(activity_read)
        after_debt = by_activity(options(session))
        assert after_debt["PAY_DEBT"]["status"] == "REFUSED"
        assert after_debt["PAY_DEBT"]["reasons"] == ["NO_DEBT"]

        care = record_parent_activity(
            session, PARENT_ID, operation_id="c02:activity:care",
            activity="CARE_DEPENDENT", hours=2)
        assert care["status"] == "ADMITTED"
        after_care = by_activity(options(session))
        assert after_care["CARE_DEPENDENT"]["status"] == "REFUSED"
        assert after_care["CARE_DEPENDENT"]["reasons"] == ["NO_CARE_OBLIGATION"]

        work = record_parent_activity(
            session, PARENT_ID, operation_id="c02:activity:work",
            activity="PAID_WORK", hours=6)
        assert work["status"] == "ADMITTED"
        after_work = by_activity(options(session))
        assert after_work["PAID_WORK"]["status"] == "REFUSED"
        assert after_work["PAID_WORK"]["reasons"] == ["NO_FREE_HOURS"]

        changed = commit_parent_circumstances(
            session, PARENT_ID, operation_id="c02:circumstance:job-loss",
            changes={"employment_status": "unemployed",
                     "wage_units_per_hour": 0},
            source_ref="sourcefree:parent:job-loss")
        assert changed["status"] == "CHANGED"
        assert changed["event_effect"] == "NONE"
        final_options = by_activity(options(session))
        assert final_options["PAID_WORK"]["status"] == "REFUSED"
        assert "EMPLOYMENT_NOT_AVAILABLE" in final_options["PAID_WORK"]["reasons"]

        material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert material["material"] == {
            "employment_status": "unemployed",
            "wage_units_per_hour": 0,
            "debt_units": 0,
            "care_hours_due": 0,
            "cash_units": 46,
            "free_hours": 0,
        }
        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        assert [row["operation_id"] for row in history["history"]
                if row["operation_id"]] == [
            "c02:activity:debt", "c02:activity:care", "c02:activity:work",
            "c02:circumstance:job-loss"]
        assert SECRET not in json.dumps(history)
        assert SECRET not in json.dumps(result_public(session, debt["event_id"]))
        assert session.read_root()["actor_ids"] == root["actor_ids"]
        assert read_supporting_actor(
            session, PARENT_ID)["private_state"] == "NOT_READ"
    finally:
        fanin.close()


def result_public(session, event_id):
    return read_actor_access(session, session.read_root()["actor_ids"][0], event_id)


def test_parent_activity_replay_cold_and_no_duplicates(tmp_path):
    fanin = start(tmp_path, "replay")
    try:
        session = fanin.session
        register(fanin)
        establish(session)
        first = record_parent_activity(
            session, PARENT_ID, operation_id="c02:replay:1",
            activity="PAID_WORK", hours=2)
        counts_after_first = counts(session)
        replay = record_parent_activity(
            session, PARENT_ID, operation_id="c02:replay:1",
            activity="PAID_WORK", hours=2)
        assert replay["status"] == "REPLAY"
        assert replay["event_id"] == first["event_id"]
        assert counts(session) == counts_after_first
        second = record_parent_activity(
            session, PARENT_ID, operation_id="c02:replay:2",
            activity="CARE_DEPENDENT", hours=1)
        with pytest.raises(RecursionRefusal, match="REPLAY_STALE"):
            record_parent_activity(
                session, PARENT_ID, operation_id="c02:replay:1",
                activity="PAID_WORK", hours=2)
        world = session.world()
        alias = read_supporting_actor(session, PARENT_ID)["alias"]
        current_material = dict(world.actor_state[alias]["material"])
        world.actor_state[alias].pop("material")
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="RECOVERY_STALE"):
            establish(session)
        world.actor_state[alias]["material"] = current_material
        session.product._checkpoint(session.branch_id, world.clock, world)
        material_source = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["source"]
        history = read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID)
        counts_before_close = counts(session)
    finally:
        fanin.close()

    reopened = load_p2().open(tmp_path / "replay")
    try:
        material = read_parent_material(
            reopened.session, PARENT_ID, as_actor=PARENT_ID)
        assert material["source"] == material_source
        assert read_parent_history(
            reopened.session, PARENT_ID, as_actor=PARENT_ID)["history"] == (
                history["history"])
        replay2 = record_parent_activity(
            reopened.session, PARENT_ID, operation_id="c02:replay:2",
            activity="CARE_DEPENDENT", hours=1)
        assert replay2["status"] == "REPLAY"
        assert replay2["event_id"] == second["event_id"]
        assert counts(reopened.session) == counts_before_close
    finally:
        reopened.close()

    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.p2_owner import load_p2
from developmental_recursion.parent_activity import parent_feasible_actions, read_parent_history, read_parent_material
fanin = load_p2().open(Path(sys.argv[2]))
try:
    session = fanin.session
    print(json.dumps({
        "material": read_parent_material(session, sys.argv[3], as_actor=sys.argv[3]),
        "options": parent_feasible_actions(session, sys.argv[3], as_actor=sys.argv[3]),
        "history": read_parent_history(session, sys.argv[3], as_actor=sys.argv[3]),
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(RETURNS.parent),
         str(tmp_path / "replay"), PARENT_ID],
        cwd=RETURNS.parent, capture_output=True, text=True, timeout=120,
        check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["material"]["source"] == material_source
    assert cold["material"]["period_qualification"] == PARENT_B02_HOLD
    assert cold["options"]["admissible"] == [
        "PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"]
    assert SECRET not in completed.stdout


def test_parent_activity_refuses_infeasible_clock_source_and_severance(tmp_path):
    fanin = start(tmp_path, "negative")
    try:
        session = fanin.session
        with pytest.raises(RecursionRefusal):
            read_parent_material(session, "TEST_ONLY_GHOST_PARENT",
                                 as_actor="TEST_ONLY_GHOST_PARENT")
        register(fanin)
        establish(session)
        baseline = counts(session)
        with pytest.raises(RecursionRefusal, match="NOT_FEASIBLE"):
            record_parent_activity(
                session, PARENT_ID, operation_id="c02:bad:debt",
                activity="PAY_DEBT", payment=5)
        assert counts(session) == baseline
        with pytest.raises(RecursionRefusal, match="CLOCK_MISMATCH"):
            record_parent_activity(
                session, PARENT_ID, operation_id="c02:bad:clock",
                activity="PAID_WORK", hours=1,
                expected_clock=session.world().clock + 99)
        assert counts(session) == baseline
        with pytest.raises(RecursionRefusal, match="SCHEMA"):
            commit_parent_circumstances(
                session, PARENT_ID, operation_id="c02:bad:source",
                changes={"debt_units": 0}, source_ref="")
        assert counts(session) == baseline
        with pytest.raises(RecursionRefusal, match="CASH_REQUIRES_ACTIVITY"):
            commit_parent_circumstances(
                session, PARENT_ID, operation_id="c02:bad:cash",
                changes={"cash_units": 999999},
                source_ref="sourcefree:parent:cash-conjure")
        assert counts(session) == baseline

        world = session.world()
        alias = read_supporting_actor(session, PARENT_ID)["alias"]
        document = dict(world.actor_state[alias]["material"])
        tampered = dict(document, source="0" * 64)
        world.actor_state[alias]["material"] = tampered
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="SOURCE_OR_ROOT_MISMATCH"):
            read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        world.actor_state[alias]["material"] = document
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["status"] == "READ"

        world.actor_state[alias].pop("material")
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="MATERIAL_ABSENT"):
            read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        restored = establish(session)
        assert restored["status"] == "RECOVERED"
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["status"] == "READ"
        assert session.world().actor_state[alias]["material"]["actor_id"] == (
            PARENT_ID)
        assert session.world().actor_state[alias]["material"]["actor_id"] != (
            session.read_root()["actor_ids"][0])
    finally:
        fanin.close()


def test_c02_composes_with_p6_b01_b03_on_fresh_final_cut(tmp_path):
    import house
    import run_p6

    state = tmp_path / "state"
    run_p6.experience(state, Namespace(command="new"))
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        household_before = house.read_household(session)
        dwelling_before = house.read_dwelling(session)
        feasibility_before = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        register(owner.base_owner.fanin)
        establish(session)
        options_result = options(session)
        assert options_result["period_qualification"] == PARENT_B02_HOLD
        assert options_result["admissible"] == [
            "PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"]
        activity = record_parent_activity(
            session, PARENT_ID, operation_id="c02:integration:work",
            activity="PAID_WORK", hours=2)
        assert activity["status"] == "ADMITTED"
        assert house.read_household(session)["source"] == household_before["source"]
        assert house.read_dwelling(session)["source"] == dwelling_before["source"]
        assert house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])["status"] == (
                feasibility_before["status"])
        assert house.read_dwelling(session)["provenance"]["fork_state"] == (
            "CURRENT_BRANCH")
    finally:
        owner.close()
