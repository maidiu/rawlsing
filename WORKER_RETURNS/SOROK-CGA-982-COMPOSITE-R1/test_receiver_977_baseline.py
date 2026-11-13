"""Independent receiver probes for CG-A @ 37c5842, separate from Agent A/B.

These are actual P6 executions and P2 cold opens. They intentionally distinguish
a sourced world event, sensory eligibility, an exact conduct parent, a current
operation, and the unissued psychological relevance rule. They cannot grant
native psychology or production authority.
"""
from argparse import Namespace
from copy import deepcopy
import json
from pathlib import Path
import sys

P6 = Path(__file__).resolve().parents[2] / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6
from house import read_house
from situated import current_p3_actor_access
from sourcefree_p3_bridge import qualified_p3_read


def _case(tmp_path):
    root = tmp_path / "real"
    run_p6.experience(root, Namespace(command="new", request_id=None, situated_house=True))
    run_p6.experience(root, Namespace(command="approach", request_id="r1"))
    record = json.loads((root / "p4_receipts.json").read_text())["turns"][-1]["receipt"]
    owner = run_p6.open_owner(root / "actual-p2")
    session = owner.base_owner.fanin.session
    world, house = read_house(session)
    packet = {"cues": [record["outward_cue"]], "recent_self_actions": [], "recent_speech": []}
    return root, owner, session, world, house, record, packet


def test_real_current_cue_requires_issuer_parent_not_just_event_identity(tmp_path, monkeypatch):
    root, owner, session, world, house, receipt, packet = _case(tmp_path)
    try:
        expected = current_p3_actor_access(session, receipt["interval"], world, house,
                                            packet, source_receipt=receipt)
        assert expected is True
        user = session.meta["user_actor"]
        with monkeypatch.context() as patch:
            original = session.episodes
            patch.setattr(session, "episodes", lambda actor: [] if actor == user else original(actor))
            assert current_p3_actor_access(session, receipt["interval"], world, house,
                                            packet, source_receipt=receipt) is False
        assert current_p3_actor_access(session, receipt["interval"], world, house,
                                        packet, source_receipt=receipt) is True
    finally:
        owner.close()


def test_source_authentic_event_cannot_survive_source_condition_severance(tmp_path):
    root, owner, session, world, house, receipt, packet = _case(tmp_path)
    try:
        before = owner.store.head()
        assert current_p3_actor_access(session, receipt["interval"], world, house,
                                        packet, source_receipt=receipt) is True
        no_audibility = deepcopy(house)
        no_audibility["situated_conditions"]["hearing"] = "unavailable"
        assert current_p3_actor_access(session, receipt["interval"], world,
                                        no_audibility, packet, source_receipt=receipt) is False
        malformed_receipt = deepcopy(receipt)
        malformed_receipt["outward_cue"]["condition_source"] = "f" * 64
        assert current_p3_actor_access(session, receipt["interval"], world, house,
                                        packet, source_receipt=malformed_receipt) is False
        assert owner.store.head() == before
    finally:
        owner.close()


def test_independent_cold_receipt_provenance_and_separate_history_readsets(tmp_path):
    root = tmp_path / "cold"
    run_p6.experience(root, Namespace(command="new", request_id=None, situated_house=True))
    seen = []
    def interpret(packet):
        seen.append(packet)
        return {"attention": "uncertain", "interpretation": "Test only",
                "action": "continue", "cue_event_id": None, "channel": None}
    public = run_p6.experience(root, Namespace(command="approach", request_id="r2"),
                              interpret=interpret, sourcefree_p3_bridge=True)
    assert seen and "sourcefree_p3" in seen[0]
    internal = json.loads((root / "p4_receipts.json").read_text())["turns"][-1]["receipt"]["situated"]["sourcefree_p3_receipt"]
    assert internal["current_world_readset"] and internal["p3_record_readset"]
    assert set(internal["current_world_readset"]).isdisjoint(internal["p3_record_readset"])
    assert internal["stimulus_to_mediator_relevance"] == "UNISSUED_NATIVE_RULE"
    assert "sourcefree_p3_receipt" not in json.dumps(public)
    owner = run_p6.open_owner(root / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert all(
            session.event(r["event_id"])["hash"] == r["event_hash"]
            for r in internal["actor_access_evidence"]
        )
        assert owner.store.head()["count"] == 1
    finally:
        owner.close()


def test_explicit_internal_trust_boundary_not_mistaken_for_protected_source(tmp_path):
    """Negative knowledge: internal caller can supply actor_observed=True.

    This is a scope/authority HOLD, not a successful protected scientific guard.
    It should be excluded from any claim of a general actor-access API.
    """
    root, owner, session, world, house, receipt, packet = _case(tmp_path)
    try:
        ledger = json.loads((root / "p4_receipts.json").read_text())
        scope = ledger["scope"]
        common = dict(project=scope["project"], counterpart=scope["counterpart"],
                      as_of=world.clock, interlocutor_role=scope["interlocutor_role"],
                      relation_ref=scope["relation_ref"])
        absent = qualified_p3_read(owner, session, **common, actor_observed=False)
        present = qualified_p3_read(owner, session, **common, actor_observed=True)
        assert absent["records"] == []
        assert present["records"] and present["grade"] == "SOURCEFREE_TEST_ONLY"
        assert present["native_memory"] == "MISSING_RULE"
        assert present["native_action"] == "NOT_ISSUED_BY_P3_RULE"
    finally:
        owner.close()
