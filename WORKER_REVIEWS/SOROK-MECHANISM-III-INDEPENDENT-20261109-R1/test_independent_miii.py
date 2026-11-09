"""Independent sourcefree falsification probes for PR #862 at 2439f36d.

These tests are reviewer-authored and do not grant native scientific semantics.
"""
from argparse import Namespace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
RETURNS = ROOT / "WORKER_RETURNS"
for location in (
    RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1" / "tests",
    RETURNS / "SOROK-P4-FIRST-FULL-MPC-R1",
    RETURNS / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1",
    RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1",
):
    sys.path.insert(0, str(location))

from response import read_response
from run_p4 import new, open_owner
from run_p6 import experience
from speech import admit_speech


def _proposal(event_id, event_hash, text, move, referent):
    return {
        "event_id": event_id, "event_hash": event_hash,
        "hypotheses": [{
            "move": move, "referent": referent,
            "span": [0, len(text)], "uncertain": False,
        }],
    }


def test_no_general_speech_route_at_unconfigured_normal_p6_entry(tmp_path):
    """An ordinary CLI-equivalent SAY has no positive semantic transducer."""
    experience(tmp_path, Namespace(command="new"))
    result = experience(
        tmp_path, Namespace(command="say", text="Could we inspect that edge together?",
                            request_edge=False, request_id="independent-no-provider"),
    )
    ledger = json.loads((tmp_path / "p4_receipts.json").read_text())
    receipt = ledger["turns"][-1]["receipt"]
    assert result["admission"] == "ADMITTED"
    assert receipt["speech"]["performed"]["body"]["text"] == (
        "Could we inspect that edge together?"
    )
    assert receipt["speech"]["actor_access"] is not None
    assert receipt["uptake"]["status"] == "PERCEIVED_NO_INSPECTION_REQUEST"
    assert receipt["expression"] is None


def test_same_committed_utterance_accepts_opposite_fixture_hypotheses(tmp_path):
    """Delimit the claim: schema-bound proposals are not validated semantic truth."""
    ledger_file = tmp_path / "p4_receipts.json"
    new(tmp_path, ledger_file, "recognized_plan")
    scope = json.loads(ledger_file.read_text())["scope"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        actor = owner.snapshot().document()["actor"]
        utterance = "I am explicitly NOT asking you to inspect this edge."
        speech = admit_speech(session, text=utterance, actor_ref=actor,
                              request_edge=False)
        def request(**kwargs):
            return _proposal(**kwargs, move="REQUEST", referent="CURRENT_EDGE")
        def assertion(**kwargs):
            return _proposal(**kwargs, move="ASSERTION", referent=None)

        request_result = read_response(owner, speech, scope, transduce=request)
        assertion_result = read_response(owner, speech, scope, transduce=assertion)
        assert request_result["mode"] == "joint_check"
        assert assertion_result["mode"] is None
        assert assertion_result["status"] == "SEMANTIC_VALID_EMPTY"
        assert request_result["semantic_encounter"]["native_plan"] == (
            "BLOCKED_NAMED_AUTHORITY_REQUIRED"
        )
        assert speech["performed"]["body"]["text"] == utterance
    finally:
        owner.close()


def test_first_reader_qualified_record_ablation_then_restoration(tmp_path, monkeypatch):
    """Sourcefree reader ablation, NOT an authenticated journal source deletion."""
    ledger_file = tmp_path / "p4_receipts.json"
    new(tmp_path, ledger_file, "recognized_plan")
    scope = json.loads(ledger_file.read_text())["scope"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        actor = owner.snapshot().document()["actor"]
        utterance = "Please check the edge with me."
        speech = admit_speech(session, text=utterance, actor_ref=actor,
                              request_edge=False)
        def request(**kwargs):
            return _proposal(**kwargs, move="REQUEST", referent="CURRENT_EDGE")
        first = read_response(owner, speech, scope, transduce=request)
        assert first["mode"] == "joint_check"
        original_query = type(owner.store).query
        with monkeypatch.context() as patch:
            def severed(store, **kwargs):
                assert kwargs["project"] == scope["project"]
                assert kwargs["counterpart"] == scope["counterpart"]
                return []
            patch.setattr(type(owner.store), "query", severed)
            cut = read_response(owner, speech, scope, transduce=request)
            assert cut["mode"] is None
            assert cut["status"] == "NO_EXPRESSION"
        assert type(owner.store).query is original_query
        restored = read_response(owner, speech, scope, transduce=request)
        assert restored == first
    finally:
        owner.close()
