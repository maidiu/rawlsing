"""E01/J1: objective parent act -> speech -> Nadia perception -> D03 -> held act."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

J1_ROOT = Path(__file__).resolve().parent
WORKER_RETURNS = J1_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
B02_ROOT = WORKER_RETURNS / "SOROK-DUEL-B02-R1"
B04_ROOT = WORKER_RETURNS / "SOROK-DUEL-B04-R1"
B05_ROOT = WORKER_RETURNS / "SOROK-DUEL-B05-R1"
P6_ROOT = WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P4_ROOT = WORKER_RETURNS / "SOROK-P4-FIRST-FULL-MPC-R1"
PROJECTION_ROOT = WORKER_RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
D03_ROOT = WORKER_RETURNS / "SOROK-DUEL-D03-R1"
for _path in (J1_ROOT, D03_ROOT / "tests", P3_ROOT, P3_ROOT / "tests",
              ENGINE_ROOT, B02_ROOT, B04_ROOT, B05_ROOT, P6_ROOT, P4_ROOT,
              PROJECTION_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import house  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.model_cycle import RecursionCycle  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material,
    historical_period_module,
    parent_material_fixture,
    read_parent_history,
    read_parent_material,
)
from developmental_recursion.parent_decision import (  # noqa: E402
    admit_parent_decision,
    parent_request_fixture,
    perform_parent_decision,
    propose_parent_decision,
    read_parent_decision,
)
from developmental_recursion.parent_speech import (  # noqa: E402
    perform_parent_utterance,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)
from p3_fixture_support import build_case, reopen_owner  # noqa: E402

import j1_join  # noqa: E402

PARENT_ID = "TEST_ONLY_E01_J1_PARENT"
PARENT_ALIAS = "P"
HIDDEN = "e01-j1-private-motive-not-for-nadia"
BASE = {
    "employment_status": "employed",
    "wage_units_per_hour": 5,
    "debt_units": 4,
    "care_hours_due": 2,
    "cash_units": 100,
    "free_hours": 8,
    "currency_unit": "sourcefree_currency_unit",
    "source_ref": "sourcefree:parent:antecedent:j1-baseline",
}
TEXT = "Not this time."


def _dwelling_facts(session, scenario):
    facts = copy.deepcopy(house.dwelling_fixture(session))
    if scenario == "tight_space":
        facts["space"]["floor_area_m2"] = 1.0
        facts["space"]["clearance_m2"] = 1.0
    elif scenario == "noise":
        facts["acoustics"]["max_indoor_loudness_db"] = 60
    elif scenario == "unknown_acoustics":
        facts["acoustics"]["max_indoor_loudness_db"] = "UNKNOWN"
    else:
        raise AssertionError("unknown dwelling scenario")
    return facts


def open_j1_case(
    path: Path,
    *,
    outcome: str = "recognized_plan",
    dwelling_scenario: str | None = None,
    parent_overrides: dict | None = None,
    household_cash: int | None = None,
    child_present: bool = True,
    decision_id: str = "j1-decision",
    speech_operation: str = "j1-speech",
    text: str = TEXT,
    hidden: str = HIDDEN,
) -> dict:
    path = Path(path)
    case = build_case(path, history_outcomes=(outcome,))
    session = case.base_owner.fanin.session
    focal = session.read_root()["actor_ids"][0]
    case.owner.realize(
        "j1-formation", case.proposals[0], case.owner.snapshot())
    house.establish(session)
    house.establish_dwelling(session)
    historical_period_module().establish_period_plan(session)
    if household_cash is not None:
        world = session.world()
        world.actor_state["A"]["cash"] = household_cash
        session.product._checkpoint(session.branch_id, world.clock, world)
    if dwelling_scenario is not None:
        house.commit_dwelling(
            session, facts=_dwelling_facts(session, dwelling_scenario))
    household_before = house.read_household(
        session)["resources"][1]["fields"]["cash"]
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": hidden},
    )
    values = {**BASE, **(parent_overrides or {})}
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(actor_id=PARENT_ID, **values),
    )
    parent_cash_before = read_parent_material(
        session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"]
    b04 = __import__(
        "developmental_recursion.parent_decision",
        fromlist=["_b04_module"],
    )._b04_module()
    b04.establish_market_inventory(session)
    request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
    admission = admit_parent_decision(
        session, PARENT_ID, operation_id=decision_id,
        request=request, as_actor=PARENT_ID,
    )
    action = perform_parent_decision(
        session, PARENT_ID, decision_id=decision_id, as_actor=PARENT_ID)
    if not child_present:
        child_alias = next(
            alias for alias, row in session.world().actor_state.items()
            if row.get("actor_id") == focal)
        world = session.world()
        world.positions[child_alias] = "market"
        session.product._checkpoint(session.branch_id, world.clock, world)
    receipt = perform_parent_utterance(
        session, PARENT_ID, decision_id=decision_id, text=text,
        hidden_reason={"reason": hidden}, operation_id=speech_operation,
    )
    return {
        "case": case,
        "session": session,
        "focal": focal,
        "admission": admission,
        "action": action,
        "receipt": receipt,
        "plan": case.plans[1],
        "path": path,
        "household_before": household_before,
        "parent_cash_before": parent_cash_before,
    }


def _joined(opened, **overrides):
    arguments = {
        "child_id": opened["focal"],
        "speech_event_id": opened["receipt"]["event_id"],
        "utterance_receipt": opened["receipt"],
        "plan": opened["plan"],
    }
    arguments.update(overrides)
    return j1_join.compose_j1(
        opened["case"].owner, opened["session"], **arguments)


def _close(opened):
    opened["case"].owner.close()


def test_j1_full_chain_and_cold_reopen(tmp_path: Path) -> None:
    opened = open_j1_case(tmp_path / "full")
    owner = opened["case"].owner
    session = opened["session"]
    try:
        admission = opened["admission"]
        action = opened["action"]
        feasibility = admission["proposal"]["evaluation"]["b03_feasibility"]
        assert admission["decision"]["action"] == "PURCHASE"
        assert feasibility["status"] == "ADMISSIBLE"
        assert action["status"] == "PERFORMED"
        assert action["performed"] is True
        assert action["physical_admission"] == "PERFORMED"
        assert action["purchase"]["status"] == "ADMITTED"
        assert action["purchase"]["possession"] == (
            "OBJECT_STOCK_AND_OWNERSHIP_WRITTEN")
        material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert material["material"]["cash_units"] == 60
        history = read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID)
        assert history["purchase_episode_count"] == 1
        household = house.read_household(session)
        assert household["resources"][1]["fields"]["cash"] == (
            opened["household_before"])

        p3_head = dict(owner.store.head())
        episode_count = len(session.product.store.episodes(session.branch_id))
        joined = _joined(opened)
        assert joined["status"] == j1_join.UPSTREAM_PROVEN
        d03 = joined["immediate_uptake"]
        child = joined["child_experience"]
        assert child["status"] == "PERCEIVED"
        assert child["p6_experience_source"] == "situated.recent_speech"
        assert child["event_id"] == opened["receipt"]["event_id"]
        assert child["event_hash"] == opened["receipt"]["event_hash"]
        assert child["response_input"]["public_text"] == TEXT
        assert child["response_input"]["perception_channel"] == "speech"
        assert d03["status"] == "COMPUTED_TEST_ONLY_IMMEDIATE"
        assert d03["speech_scope"]["text"] == TEXT
        assert d03["speech_scope"]["speaker_actor_id"] == PARENT_ID
        assert d03["immediate_response"]["eligible_modes"] == ["joint_check"]
        assert d03["durable_formation"]["status"] == "MISSING_RULE"
        assert d03["durable_formation"]["written"] is False
        assert d03["durable_formation"]["target_candidate"] is None
        assert d03["store_head"]["before"] == d03["store_head"]["after"]
        assert owner.store.head() == p3_head
        assert joined["parent_decision"]["performed"] is True
        assert joined["parent_decision"]["objective_feasibility"]["status"] == (
            "ADMISSIBLE")
        subsequent = joined["subsequent_event"]
        assert subsequent["status"] == j1_join.HELD_JOIN
        assert subsequent["performed"] is False
        assert subsequent["admitted_event"] is None
        assert subsequent["eligible_modes_are_candidates_not_actions"] is True
        assert subsequent["durable_formation"] == "MISSING_RULE"
        assert "D04" in subsequent["missing_owner"]
        assert HIDDEN not in json.dumps(child)
        assert HIDDEN not in json.dumps(d03)
        assert "cash_units" not in json.dumps(child)
        assert "cash_units" not in json.dumps(d03)
        assert "PURCHASE" not in json.dumps(child)
        assert "PURCHASE" not in json.dumps(d03)
        closure = j1_join.source_closure()
        assert joined["source_closure"]["hash"] == closure["hash"]
        labels = {row["path"] for row in closure["files"]}
        for suffix in (
            "p3/immediate_uptake.py", "SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py",
            "SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py",
            "SOROK-P6-ONE-LIVING-HOUSE-R1/house.py",
            "SOROK-DUEL-B02-R1/historical_period.py",
            "SOROK-DUEL-B04-R1/material_operations.py",
            "developmental_recursion/parent_decision.py",
            "developmental_recursion/parent_speech.py",
        ):
            assert any(label.endswith(suffix) for label in labels)
        with pytest.raises(
                RecursionRefusal, match="J1_SOURCE_CLOSURE_CHANGED"):
            _joined(opened, expected_source_closure={"hash": "0" * 64})
    finally:
        _close(opened)

    base2, owner2 = reopen_owner(opened["case"])
    try:
        session2 = base2.fanin.session
        assert owner2.store.head() == p3_head
        assert len(session2.product.store.episodes(session2.branch_id)) == (
            episode_count)
        history2 = read_parent_history(
            session2, PARENT_ID, as_actor=PARENT_ID)
        assert history2["purchase_episode_count"] == 1
        assert read_parent_decision(
            session2, PARENT_ID, "j1-decision", as_actor=PARENT_ID
        )["performed"] is True
        reopened = j1_join.compose_j1(
            owner2, session2, child_id=opened["focal"],
            speech_event_id=opened["receipt"]["event_id"],
            utterance_receipt=opened["receipt"], plan=opened["plan"],
        )
        assert reopened["child_experience"]["status"] == "PERCEIVED"
        assert reopened["immediate_uptake"]["immediate_response"][
            "eligible_modes"] == ["joint_check"]
        assert reopened["immediate_uptake"]["store_head"]["before"] == (
            reopened["immediate_uptake"]["store_head"]["after"])
        assert owner2.store.head() == p3_head
        assert len(session2.product.store.episodes(session2.branch_id)) == (
            episode_count)
        assert reopened["subsequent_event"]["status"] == j1_join.HELD_JOIN
    finally:
        owner2.close()


def test_same_actual_speech_two_prior_histories_and_later_p3_response(
    tmp_path: Path,
) -> None:
    recognized = open_j1_case(tmp_path / "recognized", outcome="recognized_plan")
    imposed = open_j1_case(tmp_path / "imposed", outcome="imposed_plan")
    try:
        recognized_join = _joined(recognized)
        imposed_join = _joined(imposed)
        assert recognized["receipt"]["event_id"] == (
            imposed["receipt"]["event_id"])
        assert recognized["receipt"]["event_hash"] == (
            imposed["receipt"]["event_hash"])
        assert recognized_join["child_experience"]["response_input"][
            "public_text"] == imposed_join["child_experience"][
                "response_input"]["public_text"]
        assert recognized_join["immediate_uptake"]["immediate_response"][
            "eligible_modes"] == ["joint_check"]
        assert imposed_join["immediate_uptake"]["immediate_response"][
            "eligible_modes"] == ["private_check"]

        class Provider:
            def __init__(self, proposals):
                self.proposals = proposals
                self.calls = []

            def call(self, request):
                self.calls.append(request)
                return {
                    "retrospective": None,
                    "prospective": [
                        proposal.document() for proposal in self.proposals],
                }

        for label, opened, joined in (
            ("recognized", recognized, recognized_join),
            ("imposed", imposed, imposed_join),
        ):
            owner = opened["case"].owner
            provider = Provider(opened["case"].proposals[1:4])
            engine = BatchEngine(owner, tmp_path / (label + "-journal.sqlite"))
            cycle = RecursionCycle(
                engine, provider, tmp_path / (label + "-cycle.json"))
            batch = cycle.bootstrap(context=joined["immediate_uptake"])
            assert provider.calls[0]["context"] == joined["immediate_uptake"]
            expected_mode = joined["immediate_uptake"]["immediate_response"][
                "eligible_modes"][0]
            expected_hash = joined["immediate_uptake"]["readset"][
                "eligible_record_hashes"][0]
            assert len(batch["records"]) == 3
            for row in batch["records"]:
                response = row["consequences"]["test_only_psychological"]
                assert [stream["mode"] for stream in response["streams"]] == [
                    expected_mode]
                assert [stream["record_hash"]
                        for stream in response["streams"]] == [expected_hash]
                assert response["native_rule"] == "MISSING_RULE"
                assert response["memory_formation"] == "MISSING_RULE"
            assert joined["subsequent_event"]["performed"] is False
    finally:
        _close(recognized)
        _close(imposed)


@pytest.mark.parametrize(
    "scenario,overrides,household_cash,dwelling,decision_action,decision_status,"
    "reason,feasibility_status,action_status,performed,purchase_count",
    [
        ("tight_space", None, None, "tight_space", "DECLINE", "REFUSED",
         "REFUSED_SPACE", "REFUSED", "VALID_EMPTY", False, 0),
        ("noise", None, None, "noise", "DECLINE", "REFUSED",
         "REFUSED_NOISE", "REFUSED", "VALID_EMPTY", False, 0),
        ("unknown_acoustics", None, None, "unknown_acoustics", "HOLD", "HELD",
         "UNKNOWN_ACOUSTICS", "UNKNOWN", "HELD", False, 0),
        ("insufficient_parent_cash", {"cash_units": 30}, None, None, "DECLINE",
         "REFUSED", "INSUFFICIENT_PARENT_CASH", "ADMISSIBLE", "VALID_EMPTY",
         False, 0),
        ("low_household_cash", None, 5, None, "PURCHASE", "ADMISSIBLE", None,
         "REFUSED", "PERFORMED", True, 1),
        ("currency_mismatch",
         {"currency_unit": "parent_sourcefree_currency_unit"}, None, None,
         "DECLINE", "REFUSED", "CURRENCY_MISMATCH", "ADMISSIBLE",
         "VALID_EMPTY", False, 0),
    ],
)
def test_objective_feasibility_binds_parent_act_then_speech_and_d03(
    tmp_path: Path, scenario: str, overrides, household_cash, dwelling,
    decision_action: str, decision_status: str, reason: str | None,
    feasibility_status: str, action_status: str, performed: bool,
    purchase_count: int,
) -> None:
    opened = open_j1_case(
        tmp_path / scenario, dwelling_scenario=dwelling,
        parent_overrides=overrides, household_cash=household_cash,
    )
    try:
        admission = opened["admission"]
        action = opened["action"]
        evaluation = admission["proposal"]["evaluation"]
        assert admission["decision"]["action"] == decision_action
        assert admission["decision"]["status"] == decision_status
        assert evaluation["b03_feasibility"]["status"] == feasibility_status
        if reason is not None:
            if reason.startswith("UNKNOWN_"):
                assert reason in evaluation["b03_feasibility"]["unknowns"]
            else:
                assert reason in evaluation["reasons"] or reason in (
                    evaluation["b03_feasibility"]["reasons"])
        assert action["status"] == action_status
        assert action["performed"] is performed
        assert action["physical_admission"] == (
            "PERFORMED" if performed else
            "VALID_EMPTY" if action_status == "VALID_EMPTY" else "HELD")
        cash = read_parent_material(
            opened["session"], PARENT_ID, as_actor=PARENT_ID
        )["material"]["cash_units"]
        assert cash == (
            opened["parent_cash_before"] - 40 if performed
            else opened["parent_cash_before"])
        history = read_parent_history(
            opened["session"], PARENT_ID, as_actor=PARENT_ID)
        assert history["purchase_episode_count"] == purchase_count
        joined = _joined(opened)
        assert joined["child_experience"]["status"] == "PERCEIVED"
        assert joined["child_experience"]["response_input"]["public_text"] == (
            TEXT)
        assert joined["immediate_uptake"]["status"] == (
            "COMPUTED_TEST_ONLY_IMMEDIATE")
        assert joined["immediate_uptake"]["immediate_response"][
            "material_feasibility"] == "NOT_EVALUATED_WORLD_PROPOSAL_SEPARATE"
        assert joined["subsequent_event"]["performed"] is False
        assert HIDDEN not in json.dumps(joined["child_experience"])
        assert HIDDEN not in json.dumps(joined["immediate_uptake"])
    finally:
        _close(opened)


def test_unheard_speech_tamper_and_severance_hold_without_recruitment(
    tmp_path: Path,
) -> None:
    remote = open_j1_case(tmp_path / "remote", child_present=False)
    try:
        assert remote["receipt"]["child_perception_channel"] == "NOT_PERCEIVED"
        owner = remote["case"].owner
        head = dict(owner.store.head())
        joined = _joined(remote)
        assert joined["status"] == "HELD_NOT_PERCEIVED"
        assert joined["child_experience"]["status"] == "NOT_PERCEIVED"
        assert joined["child_experience"]["event"] is None
        assert joined["immediate_uptake"]["status"] == "HELD_NOT_PERCEIVED"
        assert joined["immediate_uptake"]["immediate_response"][
            "eligible_modes"] == []
        assert joined["subsequent_event"]["performed"] is False
        assert "Not this time." not in json.dumps(joined["child_experience"])
        assert "Not this time." not in json.dumps(joined["immediate_uptake"])
        assert owner.store.head() == head
    finally:
        _close(remote)

    tampered = open_j1_case(tmp_path / "tampered")
    try:
        owner = tampered["case"].owner
        session = tampered["session"]
        head = dict(owner.store.head())
        altered = copy.deepcopy(tampered["receipt"])
        altered["event_id"] = "other-event"
        with pytest.raises(
                RecursionRefusal, match="J1_UTTERANCE_EVENT_MISMATCH"):
            _joined(tampered, utterance_receipt=altered)
        altered = copy.deepcopy(tampered["receipt"])
        altered["text"] = "A different public sentence."
        with pytest.raises(
                RecursionRefusal, match="J1_UTTERANCE_TEXT_MISMATCH"):
            _joined(tampered, utterance_receipt=altered)
        altered = copy.deepcopy(tampered["receipt"])
        altered["event_authored_by"] = "NOT_THE_PARENT"
        with pytest.raises(
                RecursionRefusal, match="D03_SPEAKER_EVENT_MISMATCH"):
            _joined(tampered, utterance_receipt=altered)
        original = session.event
        session.event = lambda event_id: (
            None if event_id == tampered["receipt"]["event_id"]
            else original(event_id))
        try:
            with pytest.raises(
                    RecursionRefusal, match="CHILD_UPTAKE_EVENT_SEVERED"):
                _joined(tampered)
        finally:
            session.event = original
        assert owner.store.head() == head
        assert read_parent_decision(
            session, PARENT_ID, "j1-decision", as_actor=PARENT_ID
        )["status"] == "READ"
    finally:
        _close(tampered)


def test_period_rent_cadence_keeps_parent_and_household_funds_distinct(
    tmp_path: Path,
) -> None:
    opened = open_j1_case(tmp_path / "rent")
    session = opened["session"]
    try:
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID
        )["material"]["cash_units"] == 60
        household_before = house.read_household(
            session)["resources"][1]["fields"]["cash"]
        assert household_before == opened["household_before"]
        hp.materialize_to(session, "2026-07-01")
        assert hp.period_progress(
            session, "period:2026-h1")["status"] == "COMPLETE"
        receipt = rr.apply_household_rent(
            session, operation_id="j1:rent", period_id="period:2026-h1")
        assert receipt["status"] == "ADMITTED"
        assert receipt["monthly_rent"] == 12
        assert receipt["household_cash_before"] == household_before
        assert receipt["household_cash_after"] == household_before - 12
        assert house.read_household(session)["resources"][1]["fields"][
            "cash"] == household_before - 12
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID
        )["material"]["cash_units"] == 60
        feasibility = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        assert feasibility["status"] == "REFUSED"
        assert feasibility["reasons"] == ["REFUSED_AFFORDABILITY"]
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_ALREADY_RECORDED"):
            rr.apply_household_rent(
                session, operation_id="j1:rent-late",
                period_id="period:2026-h1")
        proposed = propose_parent_decision(
            session, PARENT_ID,
            request=parent_request_fixture(
                kind="junior", owner_actor_id=PARENT_ID),
            as_actor=PARENT_ID,
        )
        assert proposed["evaluation"]["action"] == "PURCHASE"
        assert proposed["evaluation"]["b03_feasibility"]["status"] == "REFUSED"
        assert proposed["evaluation"]["b03_feasibility"]["reasons"] == [
            "REFUSED_AFFORDABILITY"]
    finally:
        _close(opened)
