"""B05 PeriodInterleaveOwner restart/retry: no wrong next date or duplicate span."""
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
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, digest,
)
from developmental_recursion.engine import BatchEngine  # noqa: E402


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def proposal(owner, event_id, event_time):
    return EventProposal(
        event_id, event_time, "ADMIT_EVENT",
        (owner.base_owner.source_ref,), owner.base_owner.participants, {},
    )


def test_interleave_retry_uses_event_keyed_dates_not_in_memory_index(tmp_path, monkeypatch):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        terms = hp.default_employment_terms()
        terms[1]["effective_from"] = "2026-01-20"
        hp.establish_period_plan(
            session,
            employment={
                "schema": hp.EMPLOYMENT_SCHEMA,
                "grade": hp.GRADE,
                "holder_actor_slot": "A",
                "terms": terms,
            },
        )
        hp.materialize_to(session, "2026-01-16")
        proposals = [proposal(owner, f"vertical:event:{index}",
                              264 + 6 * (index - 4))
                     for index in (4, 5, 6)]
        dates = {
            "vertical:event:4": "2026-01-22",
            "vertical:event:5": "2026-01-26",
            "vertical:event:6": "2026-02-01",
        }
        real_materialize = hp.materialize_to
        failed = {"done": False}

        def fail_after_materialize(session, target):
            result = real_materialize(session, target)
            if target == "2026-01-22" and not failed["done"]:
                failed["done"] = True
                raise RuntimeError("injected post-materialize failure")
            return result

        monkeypatch.setattr(hp, "materialize_to", fail_after_materialize)
        wrapped = rr.PeriodInterleaveOwner(owner, session, dates)
        engine = BatchEngine(wrapped, state / "b05-retry.sqlite")
        with pytest.raises(RecursionRefusal, match="OWNER_REALIZE_FAILED"):
            engine.run_batch("b05-retry", proposals)
        assert failed["done"] is True
        assert session.clock() >= 264

        monkeypatch.setattr(hp, "materialize_to", real_materialize)
        retry = rr.PeriodInterleaveOwner(owner, session, dates)
        engine2 = BatchEngine(retry, state / "b05-retry.sqlite")
        result = engine2.run_batch("b05-retry", proposals)
        assert len(result["records"]) == 3
        assert [row["event_id"] for row in retry.materializations] == [
            "vertical:event:4", "vertical:event:5", "vertical:event:6",
        ]
        assert [row["target_date"] for row in retry.materializations] == [
            "2026-01-22", "2026-01-26", "2026-02-01",
        ]
        assert retry.materializations[0]["status"] == "ALREADY_CURRENT"
        assert retry.materializations[1]["status"] == "MATERIALIZED"
        assert retry.materializations[2]["status"] == "MATERIALIZED"
        assert hp.period_progress(session, "period:2026-h1")["clock"] >= 264
        receipts = hp._receipt_rows(session, hp.read_period_plan(session)["source"],
                                    "period:2026-h1")
        event4_targets = [row for row in receipts
                          if row.get("target_date") == "2026-01-22"]
        assert len(event4_targets) == 1
        event_ids = [row["event_id"] for row in result["records"]]
        assert event_ids == ["vertical:event:4", "vertical:event:5",
                             "vertical:event:6"]
        assert len(set(event_ids)) == 3
        for record in result["records"]:
            assert record["receipt_ref"].startswith("P3_PSYCH:")
            assert record["readset"]
    finally:
        owner.close()
