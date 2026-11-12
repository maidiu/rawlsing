"""C01 Agent B proof: repaired supporting-actor registration, participation and access.

Each test targets a defect demonstrated against Agent A's cut:
- owner binding lockout after a supporting participant enters the same root;
- alias/stable-ID collision with the root or user namespace;
- non-atomic registration partial states and their cold recovery;
- participation writer accepting a detached/forged event or writing partially;
- actor access from a bare perception row with no participation receipt.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1] / "WORKER_RETURNS"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.contracts import (  # noqa: E402
    EventProposal, RecursionRefusal, canonical, digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    SUPPORTING_ACTOR_SCHEMA, SUPPORTING_GRADE,
    _participation_episode, read_actor_access, read_supporting_actor,
    record_supporting_participation, register_supporting_actor,
    registration_source,
)

PARENT_ID = "TEST_ONLY_C01_PARENT"
PARENT_ALIAS = "P"
SECOND_ID = "TEST_ONLY_C01_PARENT2"
SECOND_ALIAS = "Q"
SECRET = "c01-private-motive-do-not-expose"


def start(tmp_path, name="actual-p2"):
    return load_p2().start(tmp_path / name)


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


def event_for(owner, participants, event_id):
    return EventProposal(
        event_id, owner.snapshot().clock + 6, "ADMIT_EVENT",
        (owner.source_ref,), tuple(participants), {},
    )


def test_owner_binding_composes_across_participant_scopes(tmp_path):
    fanin = start(tmp_path, "compose")
    try:
        session = fanin.session
        root = session.read_root()
        focal = root["actor_ids"][0]
        root_owner = owner_for(fanin, root["actor_ids"])
        assert root_owner.participants == tuple(root["actor_ids"])
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET},
        )
        parent_owner = owner_for(fanin, (focal, PARENT_ID))
        before = root_owner.snapshot()
        proposal = event_for(root_owner, (focal, PARENT_ID), "b:compose:1")
        result = root_owner.realize("b:compose:op", proposal, before)
        assert result.consequences["supporting_participation"] == "RECORDED"
        assert result.after.actor == focal
        assert parent_owner.snapshot() == result.after
        assert parent_owner.realize(
            "b:compose:op", proposal, before) == result
        assert session.read_root()["actor_ids"] == root["actor_ids"]
        assert read_supporting_actor(session, PARENT_ID)["alias"] == PARENT_ALIAS
    finally:
        fanin.close()

    # The ordinary P3 reopen shape (all root actor IDs) must still work after
    # the C01 participant scope has been used on the same root.
    reopened = load_p2().open(tmp_path / "compose")
    try:
        session = reopened.session
        focal = session.read_root()["actor_ids"][0]
        root_owner = owner_for(reopened, session.read_root()["actor_ids"])
        assert root_owner.actor == focal
        assert root_owner.snapshot() == result.after
        assert root_owner.realize("b:compose:op", proposal, before) == result
        parent_owner = owner_for(reopened, (focal, PARENT_ID))
        assert parent_owner.realize(
            "b:compose:op", proposal, before) == result
    finally:
        reopened.close()


def test_identity_namespaces_refuse_root_and_user_collisions(tmp_path):
    fanin = start(tmp_path, "identity")
    try:
        session = fanin.session
        root = session.read_root()
        focal = root["actor_ids"][0]
        baseline = counts(session)
        for kwargs in (
            {"alias": focal, "actor_id": "TEST_ONLY_PARENT_X"},
            {"alias": "TEST_ONLY_R30A_USER_U", "actor_id": "TEST_ONLY_PARENT_Y"},
            {"alias": "Q", "actor_id": "U"},
            {"alias": "R", "actor_id": "A"},
        ):
            with pytest.raises(RecursionRefusal):
                register_supporting_actor(
                    session, role="parent", private_state={}, **kwargs)
            assert counts(session) == baseline
        assert focal not in session.world().actor_state
        assert "TEST_ONLY_R30A_USER_U" not in session.world().actor_state
    finally:
        fanin.close()


def test_registration_transaction_rolls_back_and_recovers_partial_states(
        tmp_path, monkeypatch):
    # In-process failure after branch metadata + episode work began: the C12
    # transaction rolls all of it back, so cold reopen has no ghost alias.
    fanin = start(tmp_path, "atomic")
    try:
        session = fanin.session
        def crash(*_args, **_kwargs):
            raise RuntimeError("injected crash before checkpoint")
        monkeypatch.setattr(session.product, "_checkpoint", crash)
        with pytest.raises(RuntimeError, match="injected crash"):
            register_supporting_actor(
                session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
                role="parent", private_state={"motive": SECRET})
        assert PARENT_ALIAS not in session.product.store.branch(
            session.branch_id)["actor_ids"]
        assert PARENT_ALIAS not in session.world().actor_state
        assert not [
            row for row in session.product.store.episodes(session.branch_id)
            if (row.get("body") or {}).get("alias") == PARENT_ALIAS
        ]
    finally:
        fanin.close()

    reopened = load_p2().open(tmp_path / "atomic")
    try:
        registration = register_supporting_actor(
            reopened.session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
            role="parent", private_state={"motive": SECRET})
        assert registration["status"] == "REGISTERED"
        assert PARENT_ALIAS in reopened.session.world().actor_state
    finally:
        reopened.close()

    # A partial written by the earlier non-atomic cut (branch alias + private
    # episode, no world row) is recovered on cold reopen instead of becoming a
    # permanently reserved ghost alias.
    fanin = start(tmp_path, "partial")
    try:
        session = fanin.session
        root = session.read_root()
        private = {}
        private_hash = digest(private)
        source = registration_source(
            actor_id=PARENT_ID, alias=PARENT_ALIAS, role="parent",
            private_state_hash=private_hash)
        body = {
            "schema": SUPPORTING_ACTOR_SCHEMA, "grade": SUPPORTING_GRADE,
            "root": root["root_hash"], "branch": session.branch_id,
            "epoch": session.world().clock, "actor_id": PARENT_ID,
            "alias": PARENT_ALIAS, "role": "parent", "source": source,
            "private_state_hash": private_hash, "private_state": private,
        }
        store = session.product.store
        actors = sorted(set(store.branch(session.branch_id)["actor_ids"])
                        | {PARENT_ALIAS})
        store.db.execute(
            "UPDATE branch SET actor_ids=? WHERE branch_id=?",
            (json.dumps(actors), session.branch_id))
        store.db.commit()
        store.append_episode(
            session.branch_id, actor_id=PARENT_ALIAS,
            kind="P2_SUPPORTING_ACTOR", clock=session.world().clock,
            body=body)
    finally:
        fanin.close()

    reopened = load_p2().open(tmp_path / "partial")
    try:
        registration = register_supporting_actor(
            reopened.session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
            role="parent", private_state={})
        assert registration["status"] == "RECOVERED"
        assert read_supporting_actor(
            reopened.session, PARENT_ID)["alias"] == PARENT_ALIAS
        assert len([
            row for row in reopened.session.product.store.episodes(
                reopened.session.branch_id)
            if row.get("kind") == "P2_SUPPORTING_ACTOR"
            and (row.get("body") or {}).get("alias") == PARENT_ALIAS
        ]) == 1
    finally:
        reopened.close()

    # A branch-only alias (no episode, no world row) is reclaimed, not left as
    # a ghost when the same identity is registered after cold reopen.
    fanin = start(tmp_path, "branch_only")
    try:
        session = fanin.session
        store = session.product.store
        actors = sorted(set(store.branch(session.branch_id)["actor_ids"])
                        | {PARENT_ALIAS})
        store.db.execute(
            "UPDATE branch SET actor_ids=? WHERE branch_id=?",
            (json.dumps(actors), session.branch_id))
        store.db.commit()
    finally:
        fanin.close()

    reopened = load_p2().open(tmp_path / "branch_only")
    try:
        registration = register_supporting_actor(
            reopened.session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
            role="parent", private_state={})
        assert registration["status"] == "RECOVERED"
        assert PARENT_ALIAS in reopened.session.world().actor_state
        assert reopened.session.product.store.branch(
            reopened.session.branch_id)["actor_ids"].count(PARENT_ALIAS) == 1
    finally:
        reopened.close()


def test_participation_writer_binds_actual_event_and_writes_atomically(
        tmp_path, monkeypatch):
    fanin = start(tmp_path, "participation")
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET})
        register_supporting_actor(
            session, alias=SECOND_ALIAS, actor_id=SECOND_ID, role="parent",
            private_state={})
        owner = owner_for(fanin, (focal, PARENT_ID, SECOND_ID))
        before = owner.snapshot()
        result = owner.realize(
            "b:part:op", event_for(owner, (focal, PARENT_ID), "b:part:1"),
            before)
        event_id = result.consequences["supporting_participants"][0]["event_id"]
        actual = session.event(event_id)
        for forged in (
            dict(actual, hash="f" * 64),
            dict(actual, clock=actual["clock"] + 1),
            dict(actual, body={"forged": "body"}),
        ):
            baseline = counts(session)
            with pytest.raises(RecursionRefusal, match="EVENT_MISMATCH"):
                record_supporting_participation(
                    session, event=forged, participants=(PARENT_ID,))
            assert counts(session) == baseline

        # A leak in a detached event is refused before any receipt or episode
        # is written.
        leak = dict(actual)
        leak["body"] = {**dict(actual.get("body") or {}), "leaked": SECRET}
        baseline = counts(session)
        with pytest.raises(RecursionRefusal, match="PRIVATE_STATE_LEAK"):
            record_supporting_participation(
                session, event=leak, participants=(PARENT_ID,))
        assert counts(session) == baseline

        # Second event with no supporting participant yet: moving the second
        # supporting actor away must refuse before the first actor is recorded.
        second = owner.realize(
            "b:part:op2", event_for(owner, (focal,), "b:part:2"),
            owner.snapshot())
        action_id = second.objective["event"]["action_event_id"]
        action = session.event(action_id)
        world = session.world()
        world.positions[SECOND_ALIAS] = "market"
        session.product._checkpoint(session.branch_id, world.clock, world)
        baseline = counts(session)
        with pytest.raises(RecursionRefusal, match="NOT_COPRESENT"):
            record_supporting_participation(
                session, event=action, participants=(PARENT_ID, SECOND_ID))
        assert counts(session) == baseline
        assert _participation_episode(
            session, actor_id=PARENT_ID, event_id=action_id) is None

        # validate_proposal refuses a caller-controlled proposal field that
        # carries the private value before reserving an operation or event.
        state_before = owner.snapshot()
        leaky = event_for(owner, (focal, PARENT_ID), "b:" + SECRET)
        with pytest.raises(RecursionRefusal, match="PRIVATE_STATE_LEAK"):
            owner.validate_proposal(leaky)
        assert owner.snapshot() == state_before
    finally:
        fanin.close()


def test_actor_access_requires_participation_receipt(tmp_path, monkeypatch):
    fanin = start(tmp_path, "access")
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={})
        owner = owner_for(fanin, (focal, PARENT_ID))
        focal_only = owner.realize(
            "b:access:op1", event_for(owner, (focal,), "b:access:1"),
            owner.snapshot())
        action_id = focal_only.objective["event"]["action_event_id"]
        action = session.event(action_id)
        session.product.store.record_perception(
            session.branch_id, actor_id=PARENT_ALIAS, event_id=action_id,
            clock=action["clock"], channel="co_present")
        with pytest.raises(
                RecursionRefusal, match="PARTICIPATION_SEVERED"):
            read_actor_access(session, PARENT_ID, action_id)

        shared = owner.realize(
            "b:access:op2", event_for(owner, (focal, PARENT_ID), "b:access:2"),
            owner.snapshot())
        shared_id = shared.consequences["supporting_participants"][0]["event_id"]
        assert read_actor_access(session, PARENT_ID, shared_id)["status"] == "PERCEIVED"
        assert read_actor_access(
            session, focal, shared_id)["status"] == "PERCEIVED"

        store = session.product.store
        episode = _participation_episode(
            session, actor_id=PARENT_ID, event_id=shared_id)
        original = store.episodes

        def severed(branch_id):
            return [row for row in original(branch_id)
                    if row.get("episode_id") != episode["episode_id"]]

        monkeypatch.setattr(store, "episodes", severed)
        with pytest.raises(
                RecursionRefusal, match="PARTICIPATION_SEVERED"):
            read_actor_access(session, PARENT_ID, shared_id)
        monkeypatch.undo()
        assert read_actor_access(
            session, PARENT_ID, shared_id)["status"] == "PERCEIVED"
    finally:
        fanin.close()


def test_cold_duplicate_registration_and_owner_reopen(tmp_path):
    fanin = start(tmp_path, "cold")
    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": SECRET})
        owner = owner_for(fanin, (focal, PARENT_ID))
        before = owner.snapshot()
        result = owner.realize(
            "b:cold:op", event_for(owner, (focal, PARENT_ID), "b:cold:1"), before)
        event_id = result.consequences["supporting_participants"][0]["event_id"]
        baseline = counts(session)
    finally:
        fanin.close()

    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.p2_owner import P2Owner, load_p2
from developmental_recursion.supporting_actor import read_actor_access, read_supporting_actor, register_supporting_actor
fanin = load_p2().open(Path(sys.argv[2]))
try:
    session = fanin.session
    before = {"episodes": len(session.product.store.episodes(session.branch_id)),
              "checkpoints": len(session.product.store.checkpoints(session.branch_id)),
              "world_events": len(session.product.store.world_events(session.branch_id)),
              "perceptions": len(session.product.store.perceptions(session.branch_id))}
    registration = register_supporting_actor(session, alias=sys.argv[4], actor_id=sys.argv[3], role="parent", private_state={"motive": sys.argv[5]})
    after = {"episodes": len(session.product.store.episodes(session.branch_id)),
             "checkpoints": len(session.product.store.checkpoints(session.branch_id)),
             "world_events": len(session.product.store.world_events(session.branch_id)),
             "perceptions": len(session.product.store.perceptions(session.branch_id))}
    case = fanin.deps["case_for"](True)
    owner = P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
                    participants=tuple(session.read_root()["actor_ids"]))
    print(json.dumps({
        "registration_status": registration["status"],
        "unchanged_counts": before == after,
        "root_actor_ids": session.read_root()["actor_ids"],
        "branch_actor_ids": session.product.store.branch(session.branch_id)["actor_ids"],
        "owner_actor": owner.actor,
        "parent": read_supporting_actor(session, sys.argv[3]),
        "access": read_actor_access(session, sys.argv[3], sys.argv[6]),
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(RETURNS.parent),
         str(tmp_path / "cold"), PARENT_ID, PARENT_ALIAS, SECRET, event_id],
        cwd=RETURNS.parent, capture_output=True, text=True, timeout=120,
        check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["registration_status"] == "UNCHANGED"
    assert cold["unchanged_counts"] is True
    assert cold["owner_actor"] == cold["root_actor_ids"][0]
    assert cold["parent"]["private_state"] == "NOT_READ"
    assert cold["access"]["status"] == "PERCEIVED"
    assert SECRET not in completed.stdout
    reopened = load_p2().open(tmp_path / "cold")
    try:
        assert counts(reopened.session) == baseline
    finally:
        reopened.close()


def test_legacy_binding_row_migrates_to_root_invariant(tmp_path):
    fanin = start(tmp_path, "legacy")
    try:
        session = fanin.session
        root = session.read_root()
        focal = root["actor_ids"][0]
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={})
        first = owner_for(fanin, root["actor_ids"])
        stored = json.loads(first.db.execute(
            "SELECT value FROM binding WHERE id=1").fetchone()[0])
        assert stored["root_participants"] == list(root["actor_ids"])
        legacy = {
            "root": stored["root"], "branch": stored["branch"],
            "source": stored["source"],
            "participants": [focal, PARENT_ID],
        }
        first.db.execute(
            "UPDATE binding SET value=? WHERE id=1", (canonical(legacy),))
        first.db.commit()
        migrated = owner_for(fanin, root["actor_ids"])
        stored = json.loads(migrated.db.execute(
            "SELECT value FROM binding WHERE id=1").fetchone()[0])
        assert stored["root_participants"] == list(root["actor_ids"])
        assert "participants" not in stored
        parent_owner = owner_for(fanin, (focal, PARENT_ID))
        assert parent_owner.participants == (focal, PARENT_ID)
    finally:
        fanin.close()

def test_fork_copies_registration_but_read_is_not_yet_fork_aware(tmp_path):
    # C01 preserves the exact fork incompatibility instead of pretending a
    # registration written on first_session is branch-free. Pair1 B's later
    # branch_is_ancestor reader is not copied or presumed received here.
    fanin = start(tmp_path, "fork")
    try:
        session = fanin.session
        register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={})
        fork = session.product.fork("fork1")["branch"]
        assert fork["parent_branch_id"] == session.branch_id
        assert PARENT_ALIAS in fork["actor_ids"]
        session.product.use("fork1")
        session.branch_id = "fork1"
        assert PARENT_ALIAS in session.world().actor_state
        with pytest.raises(
                RecursionRefusal, match="ROOT_OR_BRANCH_MISMATCH"):
            read_supporting_actor(session, PARENT_ID)
    finally:
        fanin.close()
