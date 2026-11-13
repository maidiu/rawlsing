"""C03 parent history-conditioned possibilities, without fake choice.

Uses the actual J1 P2/P3/parent world fixture, B02/B03/B04 readers and C02
history. A read-only fixture is *not* treated as autonomous action.
"""
from __future__ import annotations

from pathlib import Path
import json
import sys
import pytest

J1 = Path(__file__).resolve().parents[1] / "SOROK-E01-J1-995-R1"
if str(J1) not in sys.path:
    sys.path.insert(0, str(J1))
from test_j1_three_head_join import (  # noqa: E402
    PARENT_ID, HIDDEN, open_j1_case, _close,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.parent_decision import (  # noqa: E402
    read_parent_material_prospectives,
)


def _read(opened):
    return read_parent_material_prospectives(
        opened["session"], PARENT_ID, as_actor=PARENT_ID)


def _by_name(result):
    return {row["candidate"]: row for row in result["options"]}


def test_five_current_real_world_alternatives_without_fabricated_selection(tmp_path):
    opened = open_j1_case(tmp_path / "default")
    try:
        session = opened["session"]
        before_clock = session.clock()
        before_events = list(session.world().events)
        before_episodes = list(
            session.product.store.episodes(session.branch_id))
        result = _read(opened)
        assert result["status"] == "CANDIDATES_ONLY_ACTOR_SELECTION_UNISSUED"
        assert result["option_count"] == 5
        assert list(_by_name(result)) == [
            "POSSIBLE_JUNIOR_PURCHASE", "PAID_WORK",
            "CARE_DEPENDENT", "PAY_DEBT", "QUIET_NONPURCHASE",
        ]
        assert result["chosen_candidate"] is None
        assert result["performed_event"] is None
        assert result["first_consumer"] == "PARENT_OWNED_PROSPECTIVE_PERFORMER_HELD"
        assert all(not o["chosen"] and not o["performed"]
                   for o in result["options"])
        assert session.clock() == before_clock
        assert session.world().events == before_events
        assert session.product.store.episodes(
            session.branch_id) == before_episodes
        assert HIDDEN not in json.dumps(result)
        assert "hidden_reason" not in json.dumps(result)
        assert "CALLER_SUPPLIED_OBJECTIVE_REQUEST" not in json.dumps(result)
        assert _read(opened) == result
    finally:
        _close(opened)


def test_same_objective_opportunity_different_parent_work_history(tmp_path):
    employed = open_j1_case(tmp_path / "employed", parent_overrides={
        "employment_status": "employed"})
    unemployed = open_j1_case(tmp_path / "unemployed", parent_overrides={
        "employment_status": "unemployed"})
    try:
        a = _read(employed)
        b = _read(unemployed)
        assert _by_name(a)["PAID_WORK"]["status"] == "ELIGIBLE_NOT_SELECTED"
        assert _by_name(b)["PAID_WORK"]["status"] == "MATERIALLY_INELIGIBLE"
        assert "EMPLOYMENT_NOT_AVAILABLE" in _by_name(b)["PAID_WORK"]["reasons"]
        assert a["history_source"] != b["history_source"]
        assert a["source"] != b["source"]
        # Neither history selects a motive, speech, purchase or future.
        assert a["chosen_candidate"] is b["chosen_candidate"] is None
        assert a["performed_event"] is b["performed_event"] is None
    finally:
        _close(employed)
        _close(unemployed)


def test_materially_unavailable_and_quiet_remain_distinct(tmp_path):
    opened = open_j1_case(tmp_path / "no-cash", parent_overrides={
        "cash_units": 0, "employment_status": "unemployed"})
    try:
        result = _read(opened)
        options = _by_name(result)
        assert options["POSSIBLE_JUNIOR_PURCHASE"]["status"] in {
            "MATERIALLY_INELIGIBLE", "MATERIAL_UNKNOWN_HELD"}
        assert options["QUIET_NONPURCHASE"]["status"] == "ELIGIBLE_NOT_SELECTED"
        assert result["chosen_candidate"] is None
        assert result["performed_event"] is None
    finally:
        _close(opened)


def test_wrong_actor_cannot_claim_parent_self_reader(tmp_path):
    opened = open_j1_case(tmp_path / "wrong-actor")
    try:
        with pytest.raises(RecursionRefusal, match="PARENT_SELF_READ_REQUIRED"):
            read_parent_material_prospectives(
                opened["session"], PARENT_ID, as_actor="NADIA")
    finally:
        _close(opened)
