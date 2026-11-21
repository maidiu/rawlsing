"""B02 sourcefree proof: dated periods over the existing S46 logical clock."""
from __future__ import annotations

from argparse import Namespace
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
B02 = Path(__file__).resolve().parent
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (B02, P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, digest,
)
from developmental_recursion.p2_owner import material_fact_source, write_material_fact  # noqa: E402


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def by_period(materialized):
    return {row["period_id"]: row for row in materialized["periods"]}


def test_two_dated_periods_midperiod_job_change_and_later_state_read(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        clock = session.clock()
        plan = hp.establish_period_plan(session)
        employment = hp.read_employment(session)

        assert plan["schema"] == "SOROK_HISTORICAL_PERIOD_PLAN_READ@1"
        assert plan["calendar_basis"] == "GREGORIAN_PROLEPTIC_UTC_DATE"
        assert plan["clock_basis"] == "S46_TEST_ONLY_LOGICAL_TICK_DAY_V1"
        assert plan["ticks_per_day"] == 1
        assert plan["anchor_date"] == "2026-01-01"
        assert plan["anchor_clock"] == clock
        assert plan["employment_source"] == employment["source"]
        assert [p["period_id"] for p in plan["periods"]] == [
            "period:2026-h1", "period:2026-h2",
        ]
        first, second = plan["periods"]
        assert first["start_clock"] == clock
        assert first["end_clock"] - first["start_clock"] == 181
        assert second["start_clock"] == first["end_clock"]
        assert second["end_clock"] - second["start_clock"] == 184
        assert employment["terms"][0]["effective_from"] == "2026-01-01"
        assert employment["terms"][1]["effective_from"] == "2026-03-15"
        assert [term["employer_ref"] for term in employment["terms"]] == [
            "employer:workshop-cooperative", "employer:civic-works",
        ]

        before_materialize = hp.read_material_period(session, "2026-02-01")
        assert before_materialize["interval_status"] == "NOT_MATERIALIZED"
        assert before_materialize["interval"] is None

        assert hp.p3_interval_span(session, "period:2026-h1") == {
            "mode": "SCHEDULED_ONLY", "span": 181,
        }
        assert hp.p3_interval_span(session, "period:2026-h2") == {
            "mode": "SCHEDULED_ONLY", "span": 184,
        }
        interval = hp.p3_interval_span(session, "period:2026-h1")
        owner.base_owner.validate_proposal(EventProposal(
            "b02:period-proposal", session.clock() + interval["span"] + 1,
            "ADMIT_EVENT", (owner.base_owner.source_ref,),
            owner.base_owner.participants, {}, interval=interval,
        ))

        materialized = hp.materialize_periods(session)
        rows = by_period(materialized)
        assert materialized["status"] == "MATERIALIZED"
        assert materialized["produced_states"] == 2
        assert materialized["clock"] == clock + 181 + 184
        assert rows["period:2026-h1"]["start"] == clock
        assert rows["period:2026-h1"]["end"] == clock + 181
        assert rows["period:2026-h1"]["status"] == "NOT_PERFORMED"
        assert rows["period:2026-h2"]["status"] == "NOT_PERFORMED"
        first_segments = rows["period:2026-h1"]["segments"]
        second_segments = rows["period:2026-h2"]["segments"]
        assert len(first_segments) == 2
        assert [(row["start"], row["end"]) for row in first_segments] == [
            (clock, clock + 73), (clock + 73, clock + 181),
        ]
        assert len(second_segments) == 1
        assert (second_segments[0]["start"], second_segments[0]["end"]) == (
            clock + 181, clock + 181 + 184,
        )
        assert all(row["attempt"]["attempt"] == "NOT_ATTEMPTED"
                   for row in first_segments + second_segments)
        assert all(row["world"]["status"] == "NOT_PERFORMED"
                   for row in first_segments + second_segments)

        early = hp.read_material_period(session, "2026-02-01")
        changed = hp.read_material_period(session, "2026-04-01")
        later = hp.read_material_period(session, "2026-08-01")
        assert early["period"]["period_id"] == "period:2026-h1"
        assert early["logical_tick"] == clock + 31
        assert early["employment"]["term_id"] == "employment:workshop-cooperative"
        assert changed["period"]["period_id"] == "period:2026-h1"
        assert changed["logical_tick"] == clock + 90
        assert changed["employment"]["term_id"] == "employment:civic-works"
        assert later["period"]["period_id"] == "period:2026-h2"
        assert later["employment"]["term_id"] == "employment:civic-works"
        assert early["interval"]["state_id"] == rows["period:2026-h1"]["state_id"]
        assert changed["interval"]["state_id"] == rows["period:2026-h1"]["state_id"]
        assert later["interval"]["state_id"] == rows["period:2026-h2"]["state_id"]
        assert early["interval_status"] == changed["interval_status"] == (
            later["interval_status"]
        ) == "MATERIALIZED"
        assert early["provenance"]["fork_state"] == "CURRENT_BRANCH"
        assert early["read_boundary"] == hp.READ_BOUNDARY

        assert hp.p3_interval_span(session, "period:2026-h1")["span"] == 0
        assert hp.p3_interval_span(session, "period:2026-h2")["span"] == 0

        p2_employment = owner.base_owner.material_fact(hp.EMPLOYMENT_SLOT)
        p2_period = owner.base_owner.material_fact(hp.PERIOD_SLOT)
        assert p2_employment["source"] == employment["source"]
        assert p2_period["source"] == plan["source"]
        assert "state_scope" not in p2_employment
        assert "state_scope" not in p2_period

        before = counts(session)
        hp.read_material_period(session, "2026-02-01")
        hp.read_material_period(session, "2026-04-01")
        hp.read_material_period(session, "2026-08-01")
        assert counts(session) == before
        assert materialized["read_boundary"] == hp.READ_BOUNDARY
        assert materialized["read_boundary"]["psyche_store"] == "NOT_READ"
        assert materialized["read_boundary"]["psychology_state"] == "NOT_WRITTEN"
    finally:
        owner.close()


def test_retry_and_cold_replay_do_not_duplicate_periods(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        first = hp.materialize_periods(session)
        first_ids = {row["period_id"]: row["state_id"] for row in first["periods"]}
        first_counts = counts(session)
        early = hp.read_material_period(session, "2026-02-01")
        changed = hp.read_material_period(session, "2026-04-01")
        plan_source = hp.read_period_plan(session)["source"]
        employment_source = hp.read_employment(session)["source"]

        second = hp.materialize_periods(session)
        assert second["status"] == "REPLAYED"
        assert second["produced_states"] == 0
        assert {row["period_id"]: row["state_id"] for row in second["periods"]} == first_ids
        assert counts(session) == first_counts
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        assert session.clock() == 613
        assert hp.read_period_plan(session)["source"] == plan_source
        assert hp.read_employment(session)["source"] == employment_source
        cold_early = hp.read_material_period(session, "2026-02-01")
        cold_changed = hp.read_material_period(session, "2026-04-01")
        assert cold_early == early
        assert cold_changed == changed
        retry = hp.materialize_periods(session)
        assert retry["status"] == "REPLAYED"
        assert retry["produced_states"] == 0
        assert counts(session) == first_counts
    finally:
        owner.close()

    script = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "sys.path.insert(0, sys.argv[2])\n"
        "sys.path.insert(0, sys.argv[3])\n"
        "sys.path.insert(0, sys.argv[4])\n"
        "import run_p6\n"
        "import historical_period as hp\n"
        "state = Path(sys.argv[5])\n"
        "owner = run_p6.open_owner(state / 'actual-p2')\n"
        "try:\n"
        "    session = owner.base_owner.fanin.session\n"
        "    print(json.dumps({\n"
        "        'early': hp.read_material_period(session, '2026-02-01'),\n"
        "        'changed': hp.read_material_period(session, '2026-04-01'),\n"
        "        'plan': hp.read_period_plan(session),\n"
        "        'employment': hp.read_employment(session),\n"
        "    }, sort_keys=True))\n"
        "finally:\n"
        "    owner.close()\n"
    )
    cold = subprocess.run(
        [sys.executable, "-B", "-c", script, str(B02), str(P6), str(ENGINE), str(P3), str(state)],
        capture_output=True, text=True, timeout=120,
    )
    assert cold.returncode == 0, cold.stdout + cold.stderr
    reopened = json.loads(cold.stdout)
    assert reopened["early"] == early
    assert reopened["changed"] == changed
    assert reopened["plan"]["source"] == plan_source
    assert reopened["employment"]["source"] == employment_source


def test_employment_changes_as_of_date_and_severance_restores(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_periods(session)
        early = hp.read_material_period(session, "2026-02-01")
        changed = hp.read_material_period(session, "2026-04-01")
        later = hp.read_material_period(session, "2026-08-01")
        assert early["employment"]["term_id"] == "employment:workshop-cooperative"
        assert changed["employment"]["term_id"] == "employment:civic-works"
        assert later["employment"]["term_id"] == "employment:civic-works"
        assert changed["employment"] != early["employment"]

        employment = copy.deepcopy(session.world().resources[hp.EMPLOYMENT_SLOT])
        plan = copy.deepcopy(session.world().resources[hp.PERIOD_SLOT])
        world = session.world()
        world.resources.pop(hp.EMPLOYMENT_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_EMPLOYMENT_ABSENT"):
            hp.read_period_plan(session)
        with pytest.raises(RecursionRefusal, match="P6_EMPLOYMENT_ABSENT"):
            hp.read_material_period(session, "2026-04-01")
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ABSENT"):
            owner.base_owner.material_fact(hp.EMPLOYMENT_SLOT)
        write_material_fact(session, slot=hp.EMPLOYMENT_SLOT, document=employment)
        assert hp.read_material_period(session, "2026-04-01") == changed

        world = session.world()
        world.resources.pop(hp.PERIOD_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_ABSENT"):
            hp.read_period_plan(session)
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_ABSENT"):
            hp.read_material_period(session, "2026-04-01")
        write_material_fact(session, slot=hp.PERIOD_SLOT, document=plan)
        assert hp.read_material_period(session, "2026-02-01") == early
        assert hp.read_material_period(session, "2026-04-01") == changed
        assert hp.read_material_period(session, "2026-08-01") == later
    finally:
        owner.close()


def test_clock_and_term_tampering_refuses_and_restores(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_periods(session)
        baseline = hp.read_material_period(session, "2026-04-01")
        plan = copy.deepcopy(session.world().resources[hp.PERIOD_SLOT])
        employment = copy.deepcopy(session.world().resources[hp.EMPLOYMENT_SLOT])

        tampered_plan = copy.deepcopy(plan)
        tampered_plan["periods"][0]["start_clock"] += 1
        tampered_plan["source"] = material_fact_source(tampered_plan)
        write_material_fact(session, slot=hp.PERIOD_SLOT, document=tampered_plan)
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_CLOCK_MISMATCH"):
            hp.read_period_plan(session)
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_CLOCK_MISMATCH"):
            hp.read_material_period(session, "2026-04-01")
        write_material_fact(session, slot=hp.PERIOD_SLOT, document=plan)
        assert hp.read_material_period(session, "2026-04-01") == baseline

        tampered_terms = copy.deepcopy(employment)
        tampered_terms["terms"][0]["social_class"] = "poor"
        tampered_terms["source"] = material_fact_source(tampered_terms)
        write_material_fact(session, slot=hp.EMPLOYMENT_SLOT, document=tampered_terms)
        with pytest.raises(RecursionRefusal, match="P6_EMPLOYMENT_TERM_SCHEMA"):
            hp.read_employment(session)
        with pytest.raises(RecursionRefusal, match="P6_EMPLOYMENT_TERM_SCHEMA"):
            hp.read_material_period(session, "2026-04-01")

        bad_terms = copy.deepcopy(hp.default_employment_terms())
        bad_terms.reverse()
        bad_employment = {
            "schema": hp.EMPLOYMENT_SCHEMA,
            "grade": hp.GRADE,
            "holder_actor_slot": "A",
            "terms": bad_terms,
        }
        with pytest.raises(RecursionRefusal, match="P6_EMPLOYMENT_EFFECTIVE_ORDER"):
            hp.establish_period_plan(session, employment=bad_employment)

        write_material_fact(session, slot=hp.EMPLOYMENT_SLOT, document=employment)
        assert hp.read_material_period(session, "2026-04-01") == baseline
    finally:
        owner.close()


def test_fork_reads_material_only_and_refuses_new_materialization(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_periods(session)
        parent_plan = hp.read_period_plan(session)
        parent_employment = hp.read_employment(session)
        session.fork_alt("child")
        before = counts(session)
        child_plan = hp.read_period_plan(session)
        child_employment = hp.read_employment(session)
        child_period = hp.read_material_period(session, "2026-04-01")
        assert child_plan["provenance"]["stored_branch"] == "first_session"
        assert child_plan["provenance"]["current_branch"] == "child"
        assert child_plan["provenance"]["inherited"] is True
        assert child_employment["provenance"]["inherited"] is True
        assert child_period["employment"]["term_id"] == "employment:civic-works"
        assert child_period["interval_status"] == "NOT_AVAILABLE_ON_FORK"
        assert child_period["interval"] is None
        assert child_period["provenance"]["fork_state"] == (
            "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
        )
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_FORK_MATERIALIZATION_NOT_SUPPORTED"):
            hp.materialize_periods(session)
        assert counts(session) == before
        assert child_plan["source"] == parent_plan["source"]
        assert child_employment["source"] == parent_employment["source"]
    finally:
        owner.close()


def test_before_first_term_is_unknown_and_outside_plan_refuses(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        terms = hp.default_employment_terms()
        terms[0]["effective_from"] = "2026-02-01"
        employment = {
            "schema": hp.EMPLOYMENT_SCHEMA,
            "grade": hp.GRADE,
            "holder_actor_slot": "A",
            "terms": terms,
        }
        hp.establish_period_plan(session, employment=employment)
        hp.materialize_periods(session)
        before = hp.read_material_period(session, "2026-01-15")
        after = hp.read_material_period(session, "2026-02-15")
        assert before["employment"] is None
        assert before["employment_status"] == "UNKNOWN_NO_EFFECTIVE_TERM"
        assert before["period"]["period_id"] == "period:2026-h1"
        assert after["employment"]["term_id"] == "employment:workshop-cooperative"
        assert after["employment_status"] == "EFFECTIVE"
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_OUTSIDE_PLAN"):
            hp.read_material_period(session, "2025-12-31")
        with pytest.raises(RecursionRefusal, match="P6_PERIOD_OUTSIDE_PLAN"):
            hp.read_material_period(session, "2027-01-01")
    finally:
        owner.close()


def test_custom_dated_plan_freezes_anchor_and_clock_mapping(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        anchor_clock = session.clock()
        plan = hp.period_plan_fixture(session)
        plan["anchor_date"] = "2026-02-01"
        plan["anchor_clock"] = anchor_clock
        plan["periods"] = [
            {"period_id": "custom:p1", "start_date": "2026-02-01",
             "end_date": "2026-04-01"},
            {"period_id": "custom:p2", "start_date": "2026-04-01",
             "end_date": "2026-06-01"},
        ]
        established = hp.establish_period_plan(session, plan=plan)
        assert established["anchor_date"] == "2026-02-01"
        assert established["anchor_clock"] == anchor_clock
        assert [(p["period_id"], p["start_clock"], p["end_clock"])
                for p in established["periods"]] == [
            ("custom:p1", anchor_clock, anchor_clock + 59),
            ("custom:p2", anchor_clock + 59, anchor_clock + 120),
        ]
        materialized = hp.materialize_periods(session)
        assert materialized["status"] == "MATERIALIZED"
        row = hp.read_material_period(session, "2026-03-20")
        assert row["period"]["period_id"] == "custom:p1"
        assert row["employment"]["term_id"] == "employment:civic-works"
        assert row["logical_tick"] == anchor_clock + 47
    finally:
        owner.close()
