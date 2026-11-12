"""C01 sourcefree proof: stable supporting parent participation in the P2 root."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
REPO = RETURNS.parent
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.contracts import EventProposal, RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
    read_supporting_actor,
    record_supporting_participation,
    register_supporting_actor,
)

PARENT_ID = "TEST_ONLY_C01_PARENT"
PARENT_ALIAS = "P"
SECRET = "c01-private-motive-do-not-expose"


def start(tmp_path):
    return load_p2().start(tmp_path / "actual-p2")


def owner_for(fanin, participants):
    case = fanin.deps["case_for"](True)
    return P2Owner(
        fanin, case=case, source=fanin.deps["source_for"](case),
        participants=tuple(participants),
    )


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def parent_alias(session):
    return read_supporting_actor(session, PARENT_ID)["alias"]


def event_for(owner, participants, event_id="c01:event:1"):
    return EventProposal(
        event_id, owner.snapshot().clock + 6, "ADMIT_EVENT",
        (owner.source_ref,), tuple(participants), {},
    )


def test_supporting_parent_participates_without_replacing_nadia_and_cold_reopens(
        tmp_path):
    fanin = start(tmp_path)
    try:
        session = fanin.session
        root = session.read_root()
        focal = root["actor_ids"][0]
        registered = register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        assert registered["status"] == "REGISTERED"
        assert registered["private_state"] == "NOT_READ"
        assert session.read_root()["actor_ids"] == root["actor_ids"]
        assert parent_alias(session) == PARENT_ALIAS
        assert PARENT_ALIAS in session.product.store.branch(
            session.branch_id)["actor_ids"]
        assert session.world().actor_state[PARENT_ALIAS]["actor_id"] == PARENT_ID
        before_counts = counts(session)

        duplicate = register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        assert duplicate["status"] == "UNCHANGED"
        assert counts(session) == before_counts

        owner = owner_for(fanin, (focal, PARENT_ID))
        try:
            assert owner.actor == focal
            before = owner.snapshot()
            proposal = event_for(owner, (focal, PARENT_ID))
            result = owner.realize("c01:op:1", proposal, before)
            assert result.status == "REALIZED"
            assert result.after.clock == proposal.event_time
            assert result.consequences["focal_actor"] == focal
            assert result.consequences["supporting_participation"] == "RECORDED"
            participation = result.consequences["supporting_participants"]
            assert len(participation) == 1
            assert participation[0]["actor_id"] == PARENT_ID
            assert participation[0]["alias"] == PARENT_ALIAS
            assert participation[0]["private_state"] == "NOT_READ"
            event_id = participation[0]["event_id"]
            committed = session.event(event_id)
            assert committed is not None
            assert SECRET not in json.dumps(committed)
            assert SECRET not in json.dumps(result.accessible)
            assert SECRET not in json.dumps(result.objective)
            assert SECRET not in json.dumps(result.consequences)
            assert SECRET not in json.dumps(session.world().snapshot())

            focal_access = read_actor_access(session, focal, event_id)
            parent_access = read_actor_access(session, PARENT_ID, event_id)
            assert focal_access["status"] == "PERCEIVED"
            assert parent_access["status"] == "PERCEIVED"
            assert focal_access["viewer"] != parent_access["viewer"]
            assert SECRET not in json.dumps(focal_access)
            assert SECRET not in json.dumps(parent_access)
            assert focal_access["event"]["event_id"] == event_id
            assert parent_access["event"]["event_id"] == event_id

            public = read_supporting_actor(session, PARENT_ID)
            private = read_supporting_actor(
                session, PARENT_ID, as_actor=PARENT_ID)
            assert public["private_state"] == "NOT_READ"
            assert SECRET not in json.dumps(public)
            assert private["private_state"] == {"motive": SECRET}
            assert session.read_root()["actor_ids"] == root["actor_ids"]
            assert owner.snapshot().actor == focal
            after = result.after
            after_counts = counts(session)
        finally:
            owner.close()

        reopened = load_p2().open(tmp_path / "actual-p2")
        try:
            session2 = reopened.session
            assert read_supporting_actor(
                session2, PARENT_ID)["alias"] == PARENT_ALIAS
            assert parent_alias(session2) == PARENT_ALIAS
            assert SECRET not in json.dumps(
                read_actor_access(session2, focal, event_id))
            assert read_actor_access(
                session2, PARENT_ID, event_id)["status"] == "PERCEIVED"
            duplicate2 = register_supporting_actor(
                session2, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
                private_state={"motive": SECRET},
            )
            assert duplicate2["status"] == "UNCHANGED"
            owner2 = owner_for(reopened, (focal, PARENT_ID))
            try:
                assert owner2.snapshot() == after
                assert owner2.realize("c01:op:1", proposal, before) == result
                assert counts(session2) == after_counts
            finally:
                owner2.close()
        finally:
            pass
    finally:
        fanin.close()


def test_ghost_reserved_and_absent_participants_refuse_without_mutation(tmp_path):
    fanin = start(tmp_path)
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        owner = owner_for(fanin, (focal, PARENT_ID))
        try:
            before = owner.snapshot()
            baseline = counts(session)
            for changed in (
                event_for(owner, (focal, "TEST_ONLY_GHOST_PARENT")),
                event_for(owner, (PARENT_ID,)),
                event_for(owner, (focal, PARENT_ID, PARENT_ID)),
            ):
                with pytest.raises(RecursionRefusal):
                    owner.realize("c01:negative", changed, before)
                assert owner.snapshot() == before
                assert counts(session) == baseline
            with pytest.raises(RecursionRefusal, match="FOCAL_PARTICIPANT"):
                P2Owner(
                    fanin, case=owner.case, source=owner.source,
                    participants=(PARENT_ID,),
                )
            with pytest.raises(RecursionRefusal, match="NOT_REGISTERED"):
                P2Owner(
                    fanin, case=owner.case, source=owner.source,
                    participants=(focal, "TEST_ONLY_GHOST_PARENT"),
                )

            for kwargs in (
                {"alias": "A", "actor_id": "TEST_ONLY_OTHER_PARENT"},
                {"alias": "Q", "actor_id": focal},
                {"alias": "Q", "actor_id": PARENT_ID},
                {"alias": PARENT_ALIAS, "actor_id": "TEST_ONLY_OTHER_PARENT"},
                {"alias": PARENT_ALIAS, "actor_id": PARENT_ID,
                 "private_state": {"motive": "different-private-state"}},
            ):
                with pytest.raises(RecursionRefusal):
                    register_supporting_actor(
                        session, role="parent",
                        private_state=kwargs.pop("private_state", {"motive": SECRET}),
                        **kwargs,
                    )
                assert owner.snapshot() == before
                assert counts(session) == baseline

            proposal = event_for(owner, (focal, PARENT_ID))
            world = session.world()
            world.positions[PARENT_ALIAS] = "market"
            session.product._checkpoint(session.branch_id, world.clock, world)
            with pytest.raises(RecursionRefusal, match="NOT_COPRESENT"):
                owner.validate_proposal(proposal)
            world.positions[PARENT_ALIAS] = "workshop"
            session.product._checkpoint(session.branch_id, world.clock, world)
            owner.validate_proposal(proposal)
        finally:
            owner.close()
    finally:
        fanin.close()


def test_actor_access_is_separate_and_private_state_leak_refuses(tmp_path):
    fanin = start(tmp_path)
    try:
        session = fanin.session
        root = session.read_root()
        focal = root["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        owner = owner_for(fanin, (focal, PARENT_ID))
        try:
            before = owner.snapshot()
            result = owner.realize(
                "c01:op:access", event_for(owner, (focal, PARENT_ID)), before)
            participation = result.consequences["supporting_participants"][0]
            event_id = participation["event_id"]

            prior = session.world().events[0]
            focal_prior = read_actor_access(
                session, focal, prior["event_id"])
            parent_prior = read_actor_access(
                session, PARENT_ID, prior["event_id"])
            assert focal_prior["status"] == "PERCEIVED"
            assert parent_prior["status"] == "NOT_PERCEIVED"
            assert parent_prior["event"] is None

            leak_event = dict(session.event(event_id))
            leak_event["body"] = {
                **dict(leak_event.get("body") or {}),
                "leaked": SECRET,
            }
            before_counts = counts(session)
            with pytest.raises(RecursionRefusal, match="PRIVATE_STATE_LEAK"):
                record_supporting_participation(
                    session, event=leak_event, participants=(PARENT_ID,))
            assert counts(session) == before_counts
        finally:
            owner.close()
    finally:
        fanin.close()


def test_replay_refuses_severed_supporting_perception_and_restores(tmp_path):
    from unittest.mock import patch

    fanin = start(tmp_path)
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        owner = owner_for(fanin, (focal, PARENT_ID))
        try:
            before = owner.snapshot()
            proposal = event_for(owner, (focal, PARENT_ID))
            result = owner.realize("c01:op:sever", proposal, before)
            event_id = result.consequences["supporting_participants"][0]["event_id"]
            store = session.product.store
            original = store.perceptions

            def severed(branch_id, actor_id=None):
                rows = original(branch_id, actor_id)
                if actor_id is None:
                    return [row for row in rows if not (
                        row["actor_id"] == PARENT_ALIAS
                        and row["event_id"] == event_id)]
                return rows

            with patch.object(store, "perceptions", side_effect=severed):
                with pytest.raises(
                        RecursionRefusal, match="PARTICIPATION_SEVERED"):
                    owner.realize("c01:op:sever", proposal, before)
            assert owner.realize("c01:op:sever", proposal, before) == result
        finally:
            owner.close()
    finally:
        fanin.close()


def test_private_state_episode_severance_refuses(tmp_path):
    from unittest.mock import patch

    fanin = start(tmp_path)
    try:
        session = fanin.session
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        episode_id = session.world().actor_state[
            PARENT_ALIAS]["private_episode_id"]
        store = session.product.store
        original = store.episodes

        def severed(branch_id):
            return [row for row in original(branch_id)
                    if row.get("episode_id") != episode_id]

        assert read_supporting_actor(session, PARENT_ID)["role"] == "parent"
        with patch.object(store, "episodes", side_effect=severed):
            with pytest.raises(
                    RecursionRefusal, match="PRIVATE_STATE_SEVERED"):
                read_supporting_actor(session, PARENT_ID)
        assert read_supporting_actor(session, PARENT_ID)["role"] == "parent"
    finally:
        fanin.close()


def test_cold_process_reads_same_parent_participation(tmp_path):
    fanin = start(tmp_path)
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        owner = owner_for(fanin, (focal, PARENT_ID))
        try:
            before = owner.snapshot()
            result = owner.realize(
                "c01:op:cold", event_for(owner, (focal, PARENT_ID)), before)
            event_id = result.consequences["supporting_participants"][0]["event_id"]
        finally:
            owner.close()
    finally:
        pass

    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.p2_owner import load_p2
from developmental_recursion.supporting_actor import read_actor_access, read_supporting_actor
fanin = load_p2().open(Path(sys.argv[2]))
try:
    session = fanin.session
    parent = read_supporting_actor(session, sys.argv[3])
    focal = session.read_root()["actor_ids"][0]
    print(json.dumps({
        "root_actor_ids": session.read_root()["actor_ids"],
        "branch_actor_ids": session.product.store.branch(session.branch_id)["actor_ids"],
        "parent": {key: parent[key] for key in ("actor_id", "alias", "role", "private_state")},
        "focal_access": read_actor_access(session, focal, sys.argv[4]),
        "parent_access": read_actor_access(session, sys.argv[3], sys.argv[4]),
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(REPO),
         str(tmp_path / "actual-p2"), PARENT_ID, event_id],
        cwd=REPO, capture_output=True, text=True, timeout=120, check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["parent"]["actor_id"] == PARENT_ID
    assert cold["parent"]["alias"] == PARENT_ALIAS
    assert cold["parent"]["private_state"] == "NOT_READ"
    assert cold["focal_access"]["status"] == "PERCEIVED"
    assert cold["parent_access"]["status"] == "PERCEIVED"
    assert cold["focal_access"]["viewer"] != cold["parent_access"]["viewer"]
    assert SECRET not in completed.stdout
