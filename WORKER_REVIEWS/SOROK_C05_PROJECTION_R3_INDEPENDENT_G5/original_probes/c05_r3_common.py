"""Shared sourcefree fixture helpers for the C05 R3 hostile actor-view court."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ENGINE = REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
SCRATCH = REPO / ".local-logs/sorok-c05-actor-view-temporal-challenge-20261115-r3/scratch"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND,
    RELATION_HEAD_KIND,
    read_actor_relative_context,
    read_relation_history,
)
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    canonical,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
    register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_R3_PARENT"
P_ALIAS = "R3P"
O_ID = "TEST_ONLY_C05_R3_NEIGHBOR"
O_ALIAS = "R3O"
Q_ID = "TEST_ONLY_C05_R3_OBSERVER"
Q_ALIAS = "R3Q"
R_ID = "TEST_ONLY_C05_R3_OUTSIDER"
R_ALIAS = "R3R"


def start_world(prefix: str, *, register_r: bool = True):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    state = Path(tempfile.mkdtemp(prefix=prefix + "-", dir=SCRATCH)) / "p2"
    fanin = load_p2().start(state)
    session = fanin.session
    focal = session.read_root()["actor_ids"][0]
    register_supporting_actor(
        session, alias=P_ALIAS, actor_id=P_ID, role="parent",
        private_state={"motive": "r3-parent-private"})
    register_supporting_actor(
        session, alias=O_ALIAS, actor_id=O_ID, role="neighbor",
        private_state={"motive": "r3-neighbor-private"})
    register_supporting_actor(
        session, alias=Q_ALIAS, actor_id=Q_ID, role="neighbor",
        private_state={"motive": "r3-observer-private"})
    if register_r:
        register_supporting_actor(
            session, alias=R_ALIAS, actor_id=R_ID, role="neighbor",
            private_state={"motive": "r3-outsider-private"})
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin, case=case, source=fanin.deps["source_for"](case),
        participants=(focal, P_ID, O_ID))
    return fanin, session, focal, owner, state


def later_event(owner, session, participants, *, operation_id, proposal_id,
                delta=6):
    before = owner.snapshot()
    proposal = EventProposal(
        proposal_id, before.clock + delta, "ADMIT_EVENT",
        (owner.source_ref,), tuple(participants), {})
    result = owner.realize(operation_id, proposal, before)
    supporting = list(
        (result.consequences or {}).get("supporting_participants") or ())
    event_id = supporting[0]["event_id"] if supporting else None
    if event_id is None:
        candidates = [
            row for row in session.events()
            if row.get("clock") == proposal.event_time
        ]
        event_id = candidates[-1]["event_id"] if candidates else None
    return result, proposal, event_id


def counts(session) -> dict:
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


def relation_episodes(session) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") in (RELATION_CHANGE_KIND, RELATION_HEAD_KIND)
    ]


def store_sequences(session) -> dict:
    db = session.product.store.db
    branch = session.branch_id
    episode_rows = db.execute(
        "SELECT seq, kind, clock FROM episode WHERE branch_id=? ORDER BY seq",
        (branch,)).fetchall()
    event_rows = db.execute(
        "SELECT seq, event_id, clock FROM world_event WHERE branch_id=? "
        "ORDER BY seq", (branch,)).fetchall()
    return {
        "episodes": [
            {"seq": row[0], "kind": row[1], "clock": row[2]}
            for row in episode_rows
            if row[1] in (RELATION_CHANGE_KIND, RELATION_HEAD_KIND)
        ],
        "world_events": [
            {"seq": row[0], "event_id": row[1], "clock": row[2]}
            for row in event_rows
        ],
    }


def owner_operations(owner) -> list[str]:
    rows = owner.db.execute("SELECT id FROM operations ORDER BY id").fetchall()
    return [row[0] for row in rows]


def viewer_document(session, viewer: str, event_id: str,
                    as_of_clock: int) -> dict:
    return {
        "history": read_relation_history(
            session, viewer, as_of_clock=as_of_clock),
        "context": read_actor_relative_context(session, viewer, event_id),
        "event": {
            "event_id": session.event(event_id)["event_id"],
            "hash": session.event(event_id)["hash"],
            "clock": session.event(event_id)["clock"],
            "kind": session.event(event_id)["kind"],
        },
        "access": read_actor_access(session, viewer, event_id),
        "counts": counts(session),
    }


def cold_document(state_root: str, viewer: str, event_id: str,
                  as_of_clock: int) -> dict:
    config = json.dumps({
        "state_root": state_root,
        "viewer": viewer,
        "event_id": event_id,
        "as_of_clock": as_of_clock,
    })
    env = dict()
    env["TMPDIR"] = str(
        REPO / ".local-logs/sorok-c05-actor-view-temporal-challenge-20261115-r3/tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", str(HERE / "c05_r3_cold_child.py"), config],
        cwd=str(REPO), capture_output=True, text=True, timeout=180, env=env,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-2000:])
    return json.loads(completed.stdout)


def document_digest(document) -> str:
    from developmental_recursion.contracts import digest
    return digest(document)


def strip_withheld(document: dict) -> dict:
    value = json.loads(canonical(document))
    if isinstance(value, dict):
        value.pop("withheld_relation_count", None)
        scope = value.get("relation_scope")
        if isinstance(scope, dict):
            scope.pop("withheld_relation_count", None)
    return value
