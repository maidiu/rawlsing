"""Construct one reference dimension through the existing B02/C02/C04 owners.

Supply the SOROK owner tree at ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9.
All working roots are disposable fictional sessions. No source identities.
"""
import argparse
from datetime import date, timedelta
from functools import lru_cache
import json
from pathlib import Path
from random import Random
import sys
import subprocess
from tempfile import TemporaryDirectory

HOURS = range(13)
START = date(2026, 1, 5)
REFERENCE = START + timedelta(days=7)
PARENT = "TEST_ONLY_INVERSE_PARENT"


@lru_cache(maxsize=None)
def completions(days, remaining):
    if remaining < 0 or remaining > days * max(HOURS):
        return 0
    if not days:
        return int(remaining == 0)
    return sum(completions(days - 1, remaining - h) for h in HOURS)


def propose(hours, seed):
    remaining = hours
    rng = Random(seed)
    schedule = []
    for days in range(7, 0, -1):
        count = completions(days, remaining)
        if not count:
            raise ValueError("Target unreachable in this schedule family")
        index = rng.randrange(count)
        for h in HOURS:
            weight = completions(days - 1, remaining - h)
            if index < weight:
                schedule.append(h)
                remaining -= h
                break
            index -= weight
    return schedule


def observe_hours(activity, session):
    # The test world has one job, covers this entire week and assumes exact recall.
    # The reader has no target or proposed schedule argument.
    total = 0
    for row in activity.read_parent_history(session, PARENT, as_actor=PARENT)["history"]:
        if row["kind"] != activity.PARENT_ACTIVITY_KIND:
            continue
        receipt = activity.read_parent_activity(session, PARENT, row["operation_id"], as_actor=PARENT)
        day = date.fromisoformat(receipt["period_context"]["as_of_date"])
        if START <= day < REFERENCE:
            body = session.event(row["event_id"])["body"]
            if body["activity"] == "PAID_WORK":
                total += body["parameters"]["hours"]
    return total


def run_case(owner, directory, target, debt, seed):
    from developmental_recursion import parent_activity as activity, parent_decision as decision
    from developmental_recursion.p2_owner import load_p2

    schedule = propose(target, seed)
    fanin = load_p2().start(directory)
    try:
        session = fanin.session
        owner.house.establish(session)
        owner.house.establish_dwelling(session)
        period = activity.historical_period_module()
        period.establish_period_plan(session)
        owner.register_supporting_actor(session, alias="P", actor_id=PARENT, role="parent",
                                        private_state={})
        fixture = activity.parent_material_fixture(actor_id=PARENT, employment_status="employed",
                    wage_units_per_hour=1, debt_units=debt, cash_units=100, free_hours=100,
                    care_hours_due=2, currency_unit="sourcefree_currency_unit",
                    source_ref="sourcefree:reference-week:opening")
        activity.establish_parent_material(session, PARENT, fixture=fixture)
        for offset, hours in enumerate(schedule):
            day = START + timedelta(days=offset)
            period.materialize_to(session, day.isoformat())
            if hours:
                work = activity.record_parent_activity(session, PARENT, operation_id=str(day),
                                                       activity="PAID_WORK", hours=hours)
                if work["status"] != "ADMITTED":
                    raise ValueError("Proposed work was refused")
        period.materialize_to(session, REFERENCE.isoformat())
        response = observe_hours(activity, session)
        assert response == target
        decision._b04_module().establish_market_inventory(session)
        request = decision.parent_request_fixture(kind="junior", owner_actor_id=PARENT)
        decision.admit_parent_decision(session, PARENT, operation_id="offer",
                                       request=request, as_actor=PARENT)
        action = decision.perform_parent_decision(session, PARENT, decision_id="offer", as_actor=PARENT)
        return dict(target_hours=target, opening_debt=debt, schedule=schedule, recalled_hours=response,
                    purchase_decision=action["decision_action"], purchase_status=action["status"],
                    possible_schedules=completions(7, target))
    finally:
        fanin.close()


def run(owner_root, sampled):
    pin = "ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9"
    # Resolve the actual owner tree, including its test bootstrap and transitive owners.
    subprocess.run(["git", "diff", "--quiet", pin, "--",
                    ":(glob)WORKER_RETURNS/SOROK-*/**", "rawlsing_next"],
                   cwd=owner_root, check=True)
    support = owner_root / "WORKER_RETURNS/SOROK-DUEL-D03-R1/tests"
    sys.path.insert(0, str(support))
    import d03_support as owner
    target = sampled.read_constraint("hrs1")
    price = owner.house.DRUM_KIT_REQUESTS["junior"]["purchase_price"]
    debt = 100 + target - price - 4
    cases = [(target, debt, 11), (target, 210, 11), (target, debt, 12), (target - 8, debt, 11)]
    with TemporaryDirectory() as tmp:
        results = [run_case(owner, Path(tmp) / str(i), *args) for i, args in enumerate(cases)]
    assert results[0]["purchase_decision"] != results[1]["purchase_decision"]
    assert results[0]["purchase_decision"] != results[3]["purchase_decision"]
    assert results[0]["schedule"] != results[2]["schedule"]
    return {"owner_pin": pin, "first_candidate_reference_comparison":
            sampled.compare_emissions({"hrs1": results[0]["recalled_hours"]}),
            "reference": REFERENCE.isoformat(), "source_year": 2010,
            "fixture_calendar_transport": "UNVALIDATED", "complete_parent": False,
            "last_case": "counterfactual target, not another empirical draw", "cases": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner_root", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    from reference_target import run as draw_targets
    _, draws = draw_targets(args.archive)
    print(json.dumps(run(args.owner_root.resolve(), draws["female_profile"]), indent=2))
