"""Independent Agent B: P4-foreground scope is not a P3 source authority.

A source-authentic world and psyche can be paired with a mutated, unsealed
p4_receipts.json scope. The optional P6 bridge must not quietly reinterpret
that altered caller/ledger context as an original P3 plan.
"""
from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6
from developmental_recursion.contracts import RecursionRefusal


def _new(state):
    return run_p6.experience(
        state, Namespace(command="new", request_id=None, situated_house=True)
    )


def _approach(state, sink):
    def interpret(packet):
        sink.append(packet)
        return {"attention": "uncertain", "interpretation": "no assertion",
                "action": "continue", "cue_event_id": None, "channel": None}
    return run_p6.experience(
        state, Namespace(command="approach", request_id="scope-probe"),
        interpret=interpret, sourcefree_p3_bridge=True,
    )


def _owner_state(state):
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        return (owner.snapshot().document(), owner.store.head(),
                session.world().snapshot(), list(session.events()))
    finally:
        owner.close()


def test_exact_original_scope_still_reaches_real_p3_p6_consumer(tmp_path):
    state = tmp_path / "valid"
    _new(state)
    sink = []
    _approach(state, sink)
    assert len(sink) == 1
    assert sink[0]["sourcefree_p3"]["status"] == "PRIOR_P3_CANDIDATES"
    assert len(sink[0]["sourcefree_p3"]["records"]) == 1
    turns = json.loads((state / "p4_receipts.json").read_text())["turns"]
    assert turns[-1]["receipt"]["situated"]["sourcefree_p3_receipt"]["p3_record_readset"]


@pytest.mark.parametrize("field,forgery", [
    ("project", "forged:project"),
    ("counterpart", "forged:counterpart"),
    ("interlocutor_role", "forged:role"),
    ("relation_ref", "forged:relation"),
])
def test_foreground_scope_rewrite_refuses_before_any_world_or_p4_write(tmp_path, field, forgery):
    state = tmp_path / ("forged-" + field)
    _new(state)
    ledger_file = state / "p4_receipts.json"
    ledger = json.loads(ledger_file.read_text())
    assert field in ledger["scope"]
    ledger["scope"][field] = forgery
    ledger_file.write_text(json.dumps(ledger, sort_keys=True))
    prior_bytes = ledger_file.read_bytes()
    prior_owner = _owner_state(state)
    sink = []
    with pytest.raises(RecursionRefusal, match="P6_P3_SCOPE_NOT_SOURCE_BOUND"):
        _approach(state, sink)
    # Refusal must precede P4 pending and the performed outward conduct.
    assert sink == []
    assert ledger_file.read_bytes() == prior_bytes
    assert _owner_state(state) == prior_owner


def test_unauthorized_extra_scope_field_is_not_permitted(tmp_path):
    state = tmp_path / "extra"
    _new(state)
    ledger_file = state / "p4_receipts.json"
    ledger = json.loads(ledger_file.read_text())
    ledger["scope"]["model_injected_authority"] = "not issued"
    ledger_file.write_text(json.dumps(ledger))
    before = ledger_file.read_bytes()
    with pytest.raises(RecursionRefusal, match="P6_P3_SCOPE_NOT_SOURCE_BOUND"):
        _approach(state, [])
    assert ledger_file.read_bytes() == before
