"""D03 actual parent speech -> sourcefree immediate uptake vs durable formation."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

D03_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D03_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
D02_ROOT = WORKER_RETURNS / "SOROK-DUEL-D02-R1"
for _path in (D03_ROOT / "tests", P3_ROOT, P3_ROOT / "tests",
              ENGINE_ROOT, D02_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from d03_support import (  # noqa: E402
    HIDDEN,
    PARENT_ID,
    open_speech_case,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.model_cycle import RecursionCycle  # noqa: E402
from developmental_recursion.parent_decision import read_parent_decision  # noqa: E402
from developmental_recursion.parent_speech import read_parent_utterance  # noqa: E402
from p3 import immediate_uptake  # noqa: E402


def _uptake(case, receipt, plan):
    return immediate_uptake.build_immediate_uptake(
        case["case"].owner,
        speech_event_id=receipt["event_id"],
        child_id=case["focal"],
        utterance_receipt=receipt,
        plan=plan,
    )


def test_same_actual_speech_two_histories_yield_different_immediate_modes(
    tmp_path: Path,
) -> None:
    path = tmp_path / "same-speech"
    recognized = open_speech_case(path, outcome="recognized_plan")
    try:
        recognized_out = _uptake(
            recognized, recognized["receipt"], recognized["plan"])
        recognized_head = dict(recognized["case"].owner.store.head())
        assert recognized["uptake"]["status"] == "PERCEIVED"
        assert recognized["uptake"]["event"]["body_public"]["text"] == (
            "Not this time.")
    finally:
        recognized["case"].owner.close()

    imposed = open_speech_case(path, outcome="imposed_plan")
    try:
        imposed_out = _uptake(imposed, imposed["receipt"], imposed["plan"])
        imposed_head = dict(imposed["case"].owner.store.head())
    finally:
        imposed["case"].owner.close()

    assert recognized["receipt"]["event_hash"] == imposed["receipt"][
        "event_hash"]
    assert recognized["receipt"]["event_id"] == imposed["receipt"]["event_id"]
    assert recognized_out["speech_scope"]["text"] == imposed_out[
        "speech_scope"]["text"]
    assert recognized_out["immediate_response"]["eligible_modes"] == [
        "joint_check"]
    assert imposed_out["immediate_response"]["eligible_modes"] == [
        "private_check"]
    assert recognized_out["immediate_response"]["streams"][0]["mode"] == (
        "joint_check")
    assert imposed_out["immediate_response"]["streams"][0]["mode"] == (
        "private_check")
    assert recognized_out["immediate_response"]["status"] == (
        "COMPUTED_TEST_ONLY_IMMEDIATE")
    assert recognized_out["immediate_response"]["rule"]["rule_id"] == (
        "TEST_ONLY_P3_B1_SCOPED_RESPONSE")
    assert recognized_out["durable_formation"]["status"] == "MISSING_RULE"
    assert recognized_out["durable_formation"]["written"] is False
    assert recognized_out["durable_formation"]["records"] == []
    assert recognized_out["durable_formation"]["target_candidate"] is None
    assert recognized_out["durable_formation"]["status"] == "MISSING_RULE"
    assert recognized_out["store_head"]["before"] == (
        recognized_out["store_head"]["after"])
    assert imposed_out["store_head"]["before"] == imposed_out[
        "store_head"]["after"]
    assert recognized_out["store_head"]["before"] != imposed_out[
        "store_head"]["before"]
    assert recognized_head["count"] == imposed_head["count"] == 1

    assert recognized_out["speech_scope"]["speaker_actor_id"] == PARENT_ID
    assert recognized_out["speech_scope"]["role"] == "parent"
    assert recognized_out["prior_organization_scope"]["counterpart"] == (
        "vertical:counterpart")
    assert recognized_out["prior_organization_scope"]["scope_kind"] == (
        "SOURCEFREE_P3_PLAN_SCOPE_NOT_PARENT_IDENTITY")
    assert HIDDEN not in json.dumps(recognized_out)
    assert HIDDEN not in json.dumps(imposed_out)
    assert "hidden_reason" in recognized_out["speech_scope"]
    assert recognized_out["speech_scope"]["hidden_reason"] == "NOT_READ"
    labels = {row["path"] for row in recognized_out["source_closure"]["files"]}
    assert any(label.endswith("p3/immediate_uptake.py") for label in labels)
    assert any(label.endswith(
        "developmental_recursion/parent_speech.py") for label in labels)
    assert any(label.endswith("s45_projection/projection.py")
               for label in labels)


def test_severed_speech_event_keeps_parent_prior_choice(tmp_path: Path) -> None:
    case = open_speech_case(tmp_path / "severed")
    try:
        head = dict(case["case"].owner.store.head())
        original = case["session"].event
        case["session"].event = lambda event_id: (
            None if event_id == case["receipt"]["event_id"]
            else original(event_id))
        try:
            with pytest.raises(
                    RecursionRefusal, match="CHILD_UPTAKE_EVENT_SEVERED"):
                _uptake(case, case["receipt"], case["plan"])
            assert read_parent_decision(
                case["session"], PARENT_ID, "d03-decision",
                as_actor=PARENT_ID,
            )["status"] == "READ"
        finally:
            case["session"].event = original
        assert case["case"].owner.store.head() == head
    finally:
        case["case"].owner.close()


def test_self_only_parent_receipt_is_refused_not_read(tmp_path: Path) -> None:
    case = open_speech_case(tmp_path / "private-receipt")
    try:
        private = read_parent_utterance(
            case["session"], PARENT_ID, "d03-speech", as_actor=PARENT_ID)
        assert private["hidden_reason"] == {"reason": HIDDEN}
        with pytest.raises(RecursionRefusal, match="D03_PRIVATE_INPUT"):
            immediate_uptake.build_immediate_uptake(
                case["case"].owner,
                speech_event_id=case["receipt"]["event_id"],
                child_id=case["focal"],
                utterance_receipt=private,
                plan=case["plan"],
            )
        assert read_parent_decision(
            case["session"], PARENT_ID, "d03-decision",
            as_actor=PARENT_ID,
        )["status"] == "READ"
    finally:
        case["case"].owner.close()


def test_altered_speaker_identity_refuses_without_a_response(
    tmp_path: Path,
) -> None:
    case = open_speech_case(tmp_path / "altered-speaker")
    try:
        altered = copy.deepcopy(case["receipt"])
        altered["event_authored_by"] = "Q"
        with pytest.raises(RecursionRefusal, match="D03_SPEAKER_EVENT_MISMATCH"):
            _uptake(case, altered, case["plan"])
        altered = copy.deepcopy(case["receipt"])
        altered["alias"] = "Q"
        altered["event_authored_by"] = "Q"
        with pytest.raises(RecursionRefusal, match="D03_SPEAKER"):
            _uptake(case, altered, case["plan"])
        with pytest.raises(
                RecursionRefusal, match="D03_SPEAKER_EXPECTED_MISMATCH"):
            immediate_uptake.build_immediate_uptake(
                case["case"].owner,
                speech_event_id=case["receipt"]["event_id"],
                child_id=case["focal"],
                utterance_receipt=case["receipt"],
                plan=case["plan"],
                expected_speaker_actor_id="TEST_ONLY_OTHER_PARENT",
            )
        bound = immediate_uptake.build_immediate_uptake(
            case["case"].owner,
            speech_event_id=case["receipt"]["event_id"],
            child_id=case["focal"],
            utterance_receipt=case["receipt"],
            plan=case["plan"],
            expected_speaker_actor_id=PARENT_ID,
        )
        assert bound["speech_scope"]["expected_speaker_bound"] is True
    finally:
        case["case"].owner.close()


def test_material_infeasibility_is_not_actor_hearing_or_response_bar(
    tmp_path: Path,
) -> None:
    case = open_speech_case(
        tmp_path / "infeasible", debt_units=80)
    try:
        decision = read_parent_decision(
            case["session"], PARENT_ID, "d03-decision", as_actor=PARENT_ID)
        assert decision["decision"]["action"] == "DECLINE"
        out = _uptake(case, case["receipt"], case["plan"])
        assert out["immediate_response"]["status"] == (
            "COMPUTED_TEST_ONLY_IMMEDIATE")
        assert out["immediate_response"]["eligible_modes"] == ["joint_check"]
        assert out["immediate_response"]["material_feasibility"] == (
            "NOT_EVALUATED_WORLD_PROPOSAL_SEPARATE")
        assert out["immediate_response"]["streams"][0][
            "material_eligible"] is None
        assert "cash_units" not in json.dumps(out)
        assert "parent_decision" in out["read_boundary"]
        assert out["read_boundary"]["parent_decision"] == "NOT_READ"
    finally:
        case["case"].owner.close()


def test_source_closure_exact_and_expected_binding(tmp_path: Path) -> None:
    case = open_speech_case(tmp_path / "source-closure")
    try:
        closure = immediate_uptake.source_closure()
        labels = {row["path"] for row in closure["files"]}
        for suffix in (
            "p3/immediate_uptake.py", "p3/__init__.py",
            "p3/p3_owner.py", "p3/state_store.py", "p3/test_rules.py",
            "p3/projections.py", "developmental_recursion/parent_speech.py",
            "developmental_recursion/supporting_actor.py",
            "s45_projection/projection.py",
        ):
            assert any(label.endswith(suffix) for label in labels)
        out = immediate_uptake.build_immediate_uptake(
            case["case"].owner,
            speech_event_id=case["receipt"]["event_id"],
            child_id=case["focal"],
            utterance_receipt=case["receipt"],
            plan=case["plan"],
            expected_source_closure=closure,
        )
        assert out["source_closure"]["hash"] == closure["hash"]
        assert out["readset"]["source_closure"]["hash"] == closure["hash"]
        with pytest.raises(
                RecursionRefusal, match="D03_SOURCE_CLOSURE_CHANGED"):
            immediate_uptake.build_immediate_uptake(
                case["case"].owner,
                speech_event_id=case["receipt"]["event_id"],
                child_id=case["focal"],
                utterance_receipt=case["receipt"],
                plan=case["plan"],
                expected_source_closure={"hash": "0" * 64},
            )
    finally:
        case["case"].owner.close()


def test_d03_output_enters_existing_provider_and_later_p3_response(
    tmp_path: Path,
) -> None:
    case = open_speech_case(tmp_path / "provider")
    try:
        owner = case["case"].owner
        d03 = _uptake(case, case["receipt"], case["plan"])
        head_before = dict(owner.store.head())

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

        provider = Provider(case["case"].proposals[1:4])
        engine = BatchEngine(owner, tmp_path / "journal.sqlite")
        cycle = RecursionCycle(engine, provider, tmp_path / "cycle.json")
        batch = cycle.bootstrap(context=d03)
        assert provider.calls[0]["context"] == d03
        assert len(batch["records"]) == 3
        expected_mode = d03["immediate_response"]["eligible_modes"][0]
        expected_hash = d03["readset"]["eligible_record_hashes"][0]
        for row in batch["records"]:
            response = row["consequences"]["test_only_psychological"]
            assert [stream["mode"] for stream in response["streams"]] == [
                expected_mode]
            assert [stream["record_hash"] for stream in response["streams"]] == [
                expected_hash]
            assert response["native_rule"] == "MISSING_RULE"
            assert response["memory_formation"] == "MISSING_RULE"
        assert owner.store.head()["count"] == head_before["count"]
    finally:
        case["case"].owner.close()
