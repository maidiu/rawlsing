"""Exact C05 R2 repair: repeated depth-2 promotion must refuse before write."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[2]
REPO = RETURNS.parent
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, canonical,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND, RELATION_HEAD_KIND,
    promote_relation, read_actor_relative_context, read_relation_history,
    record_relation_change,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_R2_PARENT"
O_ID = "TEST_ONLY_C05_R2_NEIGHBOR"
RELATION = "r2-household"


def counts(session):
    store = session.product.store
    episodes = store.episodes(session.branch_id)
    return {
        "episodes": len(episodes),
        "changes": len([
            row for row in episodes if row.get("kind") == RELATION_CHANGE_KIND
        ]),
        "heads": len([
            row for row in episodes if row.get("kind") == RELATION_HEAD_KIND
        ]),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
    }


def test_second_depth2_promotion_refuses_before_any_write(tmp_path):
    fanin = load_p2().start(tmp_path / "p2")
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias="RP", actor_id=P_ID, role="parent",
            private_state={"motive": "r2-parent-private"})
        register_supporting_actor(
            session, alias="RO", actor_id=O_ID, role="neighbor",
            private_state={"motive": "r2-neighbor-private"})
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="ENTER", clock=session.world().clock,
            operation_id="r2:enter", exposed_actor_ids=[P_ID, O_ID],
            value="guest")
        case = fanin.deps["case_for"](True)
        owner = P2Owner(
            fanin, case=case, source=fanin.deps["source_for"](case),
            participants=(focal, P_ID, O_ID))
        try:
            before = owner.snapshot()
            proposal = EventProposal(
                "r2:event", before.clock + 6, "ADMIT_EVENT",
                (owner.source_ref,), (focal, P_ID, O_ID), {})
            result = owner.realize("r2:op", proposal, before)
            event_id = result.consequences[
                "supporting_participants"][0]["event_id"]
            event_clock = session.event(event_id)["clock"]
            first = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=session.world().clock,
                operation_id="r2:promote:1")
            assert first["status"] == "RECORDED"
            assert first["representation_depth"] == 2
            history = read_relation_history(
                session, P_ID, as_of_clock=event_clock)
            context = read_actor_relative_context(
                session, P_ID, event_id)
            assert history["status"] == "QUALIFIED"
            assert history["relations"][0]["representation_depth"] == 2
            assert context["relation_scope"]["status"] == "QUALIFIED"
            assert context["event_access"]["status"] == "PERCEIVED"
            baseline = counts(session)
            assert baseline["changes"] == 2
            assert baseline["heads"] == 2

            retry = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=first["clock"],
                operation_id="r2:promote:1")
            assert retry["status"] == "UNCHANGED"
            assert retry["primary_episode_id"] == first["primary_episode_id"]
            assert counts(session) == baseline

            with pytest.raises(
                    RecursionRefusal, match="RELATION_PROMOTION_NOT_DEEPER"):
                promote_relation(
                    session, actor_id=P_ID, other_actor_id=O_ID,
                    relation=RELATION, depth=2, clock=session.world().clock,
                    operation_id="r2:promote:2")
            assert counts(session) == baseline
            assert read_relation_history(
                session, P_ID, as_of_clock=event_clock) == history
            assert read_actor_relative_context(
                session, P_ID, event_id) == context
            assert session.product.store.verify(session.branch_id)["ok"]

            retry_again = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=first["clock"],
                operation_id="r2:promote:1")
            assert retry_again["status"] == "UNCHANGED"
            assert retry_again["primary_episode_id"] == first[
                "primary_episode_id"]
            assert counts(session) == baseline
            state_root = str(tmp_path / "p2")
            warm = {
                "history": history,
                "context": context,
                "counts": baseline,
                "root": session.read_root()["actor_ids"],
                "clock": session.world().clock,
                "promotion": first["primary_episode_id"],
                "event_clock": event_clock,
            }
        finally:
            owner.close()
    finally:
        pass

    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.continuing_relations import (
    RELATION_CHANGE_KIND, RELATION_HEAD_KIND, promote_relation,
    read_actor_relative_context, read_relation_history,
)
from developmental_recursion.p2_owner import load_p2
fanin = load_p2().open(Path(sys.argv[2]))
try:
    s = fanin.session
    store = s.product.store
    episodes = store.episodes(s.branch_id)
    history = read_relation_history(s, sys.argv[3], as_of_clock=int(sys.argv[6]))
    context = read_actor_relative_context(s, sys.argv[3], sys.argv[5])
    retry = promote_relation(
        s, actor_id=sys.argv[3], other_actor_id=sys.argv[4],
        relation=sys.argv[7], depth=2, clock=int(sys.argv[8]),
        operation_id=sys.argv[9])
    print(json.dumps({
        "history": history,
        "context": context,
        "counts": {
            "episodes": len(episodes),
            "changes": len([r for r in episodes if r.get("kind") == RELATION_CHANGE_KIND]),
            "heads": len([r for r in episodes if r.get("kind") == RELATION_HEAD_KIND]),
            "world_events": len(store.world_events(s.branch_id)),
            "perceptions": len(store.perceptions(s.branch_id)),
            "checkpoints": len(store.checkpoints(s.branch_id)),
        },
        "root": s.read_root()["actor_ids"],
        "clock": s.world().clock,
        "retry_status": retry.get("status"),
        "retry_primary": retry.get("primary_episode_id"),
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(REPO), state_root,
         P_ID, O_ID, event_id, str(warm["event_clock"]), RELATION,
         str(warm["clock"]), "r2:promote:1"],
        cwd=REPO, capture_output=True, text=True, timeout=180, check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["history"] == warm["history"]
    assert cold["context"] == warm["context"]
    assert cold["counts"] == warm["counts"]
    assert cold["root"] == warm["root"]
    assert cold["clock"] == warm["clock"]
    assert cold["retry_status"] == "UNCHANGED"
    assert cold["retry_primary"] == warm["promotion"]
    assert "r2-parent-private" not in completed.stdout
    assert "r2-neighbor-private" not in completed.stdout
