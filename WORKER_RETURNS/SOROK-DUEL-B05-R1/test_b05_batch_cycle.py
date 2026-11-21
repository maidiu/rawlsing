"""B02/B04/B05 integration: a real three-event P3 batch after the employment split."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
B05 = Path(__file__).resolve().parent
B04 = RETURNS / "SOROK-DUEL-B04-R1"
B02 = RETURNS / "SOROK-DUEL-B02-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (B05, B04, B02, P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import house  # noqa: E402
import material_operations as mo  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import EventProposal, digest  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material, parent_material_fixture,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_B05_BATCH_PARENT"
PARENT_ALIAS = "P"


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def proposal(owner, event_id, event_time):
    return EventProposal(
        event_id, event_time, "ADMIT_EVENT",
        (owner.base_owner.source_ref,), owner.base_owner.participants, {},
    )


def test_three_event_batch_after_employment_split_then_purchase_and_rent(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        anchor = session.clock()
        terms = hp.default_employment_terms()
        terms[1]["effective_from"] = "2026-01-15"
        hp.establish_period_plan(
            session,
            employment={
                "schema": hp.EMPLOYMENT_SCHEMA,
                "grade": hp.GRADE,
                "holder_actor_slot": "A",
                "terms": terms,
            },
        )
        first = hp.materialize_to(session, "2026-01-16")
        assert first["clock"] == anchor + 15
        assert hp.read_material_period(session, "2026-01-20")["employment"][
            "term_id"] == "employment:civic-works"

        proposals = [proposal(owner, f"vertical:event:{index}",
                              264 + 6 * (index - 4))
                     for index in (4, 5, 6)]
        for row in proposals:
            plan = next(p for p in owner.plans if p["event_id"] == row.event_id)
            assert digest(row.document()) == plan["proposal_hash"]
        engine = BatchEngine(owner, state / "b05-batch.sqlite")
        result = engine.run_batch("b05-three-event", proposals)
        assert len(result["records"]) == 3
        assert session.clock() == anchor + 28
        assert all(record["consequences"]["durable_psychological_transition"] ==
                   "MISSING_RULE" for record in result["records"])
        p3_head = owner.store.head()

        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": "b05-batch-private"},
        )
        establish_parent_material(
            session, PARENT_ID,
            fixture=parent_material_fixture(
                actor_id=PARENT_ID, source_ref="sourcefree:parent:b05-batch",
                employment_status="employed", wage_units_per_hour=5,
                debt_units=4, care_hours_due=2, cash_units=60, free_hours=8, currency_unit=mo.CURRENCY,
            ),
        )
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]
        purchase = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b05-batch:buy",
            owner_actor_id=holder)
        assert purchase["status"] == "ADMITTED"
        assert purchase["period"]["period_id"] == "period:2026-h1"
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 1

        second = hp.materialize_to(session, "2026-07-01")
        assert second["status"] == "MATERIALIZED"
        assert hp.period_progress(session, "period:2026-h1")["status"] == "COMPLETE"
        rent = rr.apply_household_rent(
            session, operation_id="b05-batch:rent", period_id="period:2026-h1")
        assert rent["status"] == "ADMITTED"
        assert rent["household_cash_before"] == 55
        assert rent["household_cash_after"] == 43
        assert rent["scheduled_participation"] == "NOT_PERFORMED"
        assert owner.store.head() == p3_head

        april = hp.read_material_period(session, "2026-04-01")
        assert april["as_of_relation"] == "PAST"
        assert april["employment"]["term_id"] == "employment:civic-works"
        assert april["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 43
        assert house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])["status"] == "REFUSED"
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 1
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 1
        assert owner.store.head() == p3_head
    finally:
        owner.close()
