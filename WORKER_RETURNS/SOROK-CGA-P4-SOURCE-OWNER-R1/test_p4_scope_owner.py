"""P4 first consumer: foreground scope must be the source-issued formation plan."""

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P4 = ROOT / "WORKER_RETURNS/SOROK-P4-FIRST-FULL-MPC-R1"
if str(P4) not in sys.path:
    sys.path.insert(0, str(P4))

import run_p4
from developmental_recursion.contracts import RecursionRefusal
from response import read_response
from speech import admit_speech


def _new(state):
    return run_p4.new(state, state / "p4_receipts.json", "recognized_plan")


def _say(state, text="Look at this edge with me.", request_id="p4-scope"):
    ledger_file = state / "p4_receipts.json"
    ledger = json.loads(ledger_file.read_text())
    owner = run_p4.open_owner(state / "actual-p2")
    try:
        return run_p4.act(
            owner, ledger_file, ledger,
            Namespace(command="say", text=text, request_edge=True,
                      request_id=request_id),
        )
    finally:
        owner.close()


def _state(state):
    owner = run_p4.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        return {
            "identity": owner.snapshot().document(),
            "head": owner.store.head(),
            "world": session.world().snapshot(),
            "events": list(session.events()),
            "perceived": list(session.user_perceived_ids()),
            "episodes": list(session.episodes(session.meta["user_actor"])),
        }
    finally:
        owner.close()


def _tamper(state, field, value):
    ledger_file = state / "p4_receipts.json"
    ledger = json.loads(ledger_file.read_text())
    original = dict(ledger["scope"])
    ledger["scope"][field] = value
    ledger_file.write_text(json.dumps(ledger, sort_keys=True))
    return ledger_file, original


def test_p4_say_uses_exact_source_formation_and_prior_p3_records(tmp_path):
    state = tmp_path / "positive"
    _new(state)
    before = _state(state)
    public = _say(state)
    assert public["admission"] == "ADMITTED" and public["performed"] is True
    ledger = json.loads((state / "p4_receipts.json").read_text())
    turn = ledger["turns"][0]
    uptake = turn["receipt"]["uptake"]
    assert uptake["status"] == "UPTAKE" and uptake["mode"] == "joint_check"
    assert turn["receipt"]["speech"]["performed"]["body"]["request_edge"] is True
    after = _state(state)
    assert after["head"] == before["head"]
    owner = run_p4.open_owner(state / "actual-p2")
    try:
        records = owner.store.query(
            project=ledger["scope"]["project"],
            counterpart=ledger["scope"]["counterpart"],
            as_of=before["identity"]["clock"] - 1,
        )
        assert records
        assert {row["hash"] for row in records} <= set(uptake["readset"])
    finally:
        owner.close()


@pytest.mark.parametrize("field,forgery", [
    ("project", "forged:project"),
    ("counterpart", "forged:counterpart"),
    ("interlocutor_role", "forged:role"),
    ("relation_ref", "forged:relation"),
])
def test_p4_say_refuses_tampered_scope_before_pending_or_speech(tmp_path, field, forgery):
    state = tmp_path / ("tamper-" + field)
    _new(state)
    ledger_file, original = _tamper(state, field, forgery)
    tampered = ledger_file.read_bytes()
    before = _state(state)
    with pytest.raises(RecursionRefusal, match="P4_SCOPE_NOT_SOURCE_BOUND"):
        _say(state)
    assert ledger_file.read_bytes() == tampered
    ledger = json.loads(ledger_file.read_text())
    assert ledger["pending"] is None and ledger["turns"] == []
    assert _state(state) == before
    ledger["scope"] = original
    ledger_file.write_text(json.dumps(ledger, sort_keys=True))
    public = _say(state)
    assert public["performed"] is True
    restored = json.loads(ledger_file.read_text())["turns"][-1]["receipt"]["uptake"]
    assert restored["status"] == "UPTAKE" and restored["mode"] == "joint_check"


def test_p4_say_refuses_extra_foreground_scope_field(tmp_path):
    state = tmp_path / "extra"
    _new(state)
    ledger_file, _original = _tamper(state, "model_injected_authority", "not issued")
    tampered = ledger_file.read_bytes()
    before = _state(state)
    with pytest.raises(RecursionRefusal, match="P4_SCOPE_NOT_SOURCE_BOUND"):
        _say(state)
    assert ledger_file.read_bytes() == tampered
    assert json.loads(ledger_file.read_text())["pending"] is None
    assert _state(state) == before


def test_direct_read_response_refuses_substituted_scope_before_p3_read(tmp_path, monkeypatch):
    state = tmp_path / "direct"
    _new(state)
    ledger = json.loads((state / "p4_receipts.json").read_text())
    owner = run_p4.open_owner(state / "actual-p2")
    queries = []
    try:
        session = owner.base_owner.fanin.session
        speech = admit_speech(
            session, text="Look at this edge with me.",
            actor_ref=owner.snapshot().document()["actor"], request_edge=True,
        )
        original_query = owner.store.query

        def query(**kwargs):
            queries.append(kwargs)
            return original_query(**kwargs)

        monkeypatch.setattr(owner.store, "query", query)
        forged = dict(ledger["scope"], project="forged:project")
        with pytest.raises(RecursionRefusal, match="P4_SCOPE_NOT_SOURCE_BOUND"):
            read_response(owner, speech, forged)
        assert queries == []
        plan = next(row for row in owner.plans if row["phase"] == "FORMATION")
        direct_scope = dict(plan, relation_ref=plan["relation_refs"][0])
        uptake = read_response(owner, speech, direct_scope)
        assert queries and uptake["status"] == "UPTAKE"
    finally:
        owner.close()
