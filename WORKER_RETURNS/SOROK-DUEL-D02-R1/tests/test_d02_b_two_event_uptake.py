"""D02 counterstrike: prior acquired state must not leak into unperceived speech."""
from __future__ import annotations

import json
import sys
from pathlib import Path

D02_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D02_ROOT.parent
D03_ROOT = WORKER_RETURNS / "SOROK-DUEL-D03-R1"
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
B02_ROOT = WORKER_RETURNS / "SOROK-DUEL-B02-R1"
for _path in (D03_ROOT / "tests", P3_ROOT, P3_ROOT / "tests",
              ENGINE_ROOT, B02_ROOT, D02_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as b02  # noqa: E402
from d03_support import HIDDEN, PARENT_ID, open_speech_case  # noqa: E402
from developmental_recursion.contracts import EventProposal  # noqa: E402
from developmental_recursion.parent_decision import read_parent_decision  # noqa: E402
from p3 import immediate_uptake, situated_context  # noqa: E402
from p3_fixture_support import build_case  # noqa: E402


def test_prior_acquired_modes_do_not_enter_unobserved_parent_speech_response(
    tmp_path: Path,
) -> None:
    case = open_speech_case(tmp_path / "two-event", child_present=False)
    try:
        owner = case["case"].owner
        session = case["session"]
        selector = situated_context.build_situated_context(
            owner, plan=case["plan"])
        acquired = selector["acquired_state"]
        assert acquired["status"] == "ELIGIBLE"
        assert acquired["eligible_modes"] == ["joint_check"]
        assert acquired["activation_context"]["actor_observed"] is True
        assert case["uptake"]["status"] == "NOT_PERCEIVED"
        assert case["receipt"]["child_perception_channel"] == "NOT_PERCEIVED"
        head_before = dict(owner.store.head())

        out = immediate_uptake.build_immediate_uptake(
            owner,
            speech_event_id=case["receipt"]["event_id"],
            child_id=case["focal"],
            utterance_receipt=case["receipt"],
            plan=case["plan"],
        )
        assert out["status"] == "HELD_NOT_PERCEIVED"
        assert out["immediate_response"]["status"] == "HELD_NOT_PERCEIVED"
        assert out["immediate_response"]["eligible_modes"] == []
        assert out["immediate_response"]["streams"] == []
        assert out["prior_organization_scope"] is None
        assert out["activation_context"] is None
        assert out["speech_scope"]["text"] == "NOT_READ"
        assert out["durable_formation"]["status"] == "MISSING_RULE"
        assert out["durable_formation"]["written"] is False
        assert out["store_head"]["before"] == out["store_head"]["after"]
        assert owner.store.head() == head_before
        assert HIDDEN not in json.dumps(out)
        assert read_parent_decision(
            session, PARENT_ID, "d03-decision", as_actor=PARENT_ID,
        )["status"] == "READ"
    finally:
        case["case"].owner.close()


def test_current_period_uses_incremental_progress_fields(tmp_path: Path) -> None:
    case = build_case(tmp_path / "period-progress")
    try:
        session = case.base_owner.fanin.session
        b02.establish_period_plan(session)
        first = situated_context.build_situated_context(case.owner)
        period = first["period"]
        assert period["status"] == "QUALIFIED_CURRENT_PERIOD"
        assert period["period_progress"]["period_id"] == "period:2026-h1"
        assert period["period_progress"]["clock"] == session.clock()
        assert period["period_progress"]["current_date"] == period["as_of_date"]
        assert "period_progress" in period["source"]["symbols"]
        assert period["period_progress"]["status"] in {
            "BEFORE", "PARTIAL", "COMPLETE"}
        proposal = EventProposal(
            "d02-b-period-advance", session.clock() + 90, "ADMIT_EVENT",
            (case.base_owner.source_ref,),
            tuple(session.read_root()["actor_ids"]), {},
        )
        case.base_owner.realize(
            "d02-b-period-advance-operation", proposal,
            case.base_owner.snapshot())
        changed = situated_context.build_situated_context(case.owner)
        changed_period = changed["period"]
        assert changed_period["as_of_date"] == "2026-04-01"
        assert changed_period["period_progress"]["current_date"] == (
            "2026-04-01")
        assert changed_period["period_progress"]["clock"] == session.clock()
        assert changed_period["employment"]["term_id"] == (
            "employment:civic-works")
        assert changed["hash"] != first["hash"]
    finally:
        case.owner.close()
