"""C05 sourcefree proof: dated continuing relations over the actual P2/C12 world.

The caller supplies one illustrative relation change. A later real P2 world
event is read through the accepted C01 actor-relative receipt path, and the
terminal consumer combines that access with only the dated relation entries the
actor was exposed to. No new world/psyche store, autonomous selector, generated
speech, or native claim is used.
"""
from __future__ import annotations

from contextlib import contextmanager
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
    EventProposal, RecursionRefusal, canonical, digest,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND, RELATION_HEAD_KIND, promote_relation,
    read_actor_relative_context, read_relation_history, record_relation_change,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access, read_supporting_actor, register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_PARENT"
P_ALIAS = "P"
O_ID = "TEST_ONLY_C05_NEIGHBOR"
O_ALIAS = "O"
RELATION = "household"
P_SECRET = "c05-parent-private-motive"
O_SECRET = "c05-neighbor-private-motive"
REL_SECRET = "c05-relation-private-note"


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
    }


def relation_counts(session):
    store = session.product.store
    episodes = store.episodes(session.branch_id)
    return {
        "parent_registrations": len([
            row for row in episodes
            if row.get("kind") == "P2_SUPPORTING_ACTOR"
            and (row.get("body") or {}).get("actor_id") == P_ID
        ]),
        "neighbor_registrations": len([
            row for row in episodes
            if row.get("kind") == "P2_SUPPORTING_ACTOR"
            and (row.get("body") or {}).get("actor_id") == O_ID
        ]),
        "relation_changes": len([
            row for row in episodes if row.get("kind") == RELATION_CHANGE_KIND
        ]),
        "relation_heads": len([
            row for row in episodes if row.get("kind") == RELATION_HEAD_KIND
        ]),
        "c04_utterances": len([
            row for row in episodes if row.get("kind") == "P2_PARENT_UTTERANCE"
        ]),
    }


@contextmanager
def world(tmp_path):
    fanin = load_p2().start(tmp_path / "p2")
    session = fanin.session
    focal = session.read_root()["actor_ids"][0]
    register_supporting_actor(
        session, alias=P_ALIAS, actor_id=P_ID, role="parent",
        private_state={"motive": P_SECRET},
    )
    register_supporting_actor(
        session, alias=O_ALIAS, actor_id=O_ID, role="neighbor",
        private_state={"motive": O_SECRET},
    )
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin, case=case, source=fanin.deps["source_for"](case),
        participants=(focal, P_ID, O_ID),
    )
    try:
        yield fanin, session, focal, owner
    finally:
        owner.close()


def later_event(owner, session, participants, *, operation_id, event_id,
                delta=6):
    before = owner.snapshot()
    proposal = EventProposal(
        event_id, before.clock + delta, "ADMIT_EVENT",
        (owner.source_ref,), tuple(participants), {},
    )
    result = owner.realize(operation_id, proposal, before)
    event_id = result.consequences["supporting_participants"][0]["event_id"]
    return result, proposal, before, event_id


def entry(session, *, exposed, operation_id="c05:rel:enter",
          value="guest", private_state=None):
    return record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="ENTER", clock=session.world().clock,
        operation_id=operation_id, exposed_actor_ids=exposed,
        value=value, private_state=private_state,
    )


def change(session, *, exposed, operation_id="c05:rel:change",
           value="member"):
    return record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="CHANGE", clock=session.world().clock,
        operation_id=operation_id, exposed_actor_ids=exposed,
        value=value,
    )


def test_dated_relation_later_shared_event_and_separate_contexts(tmp_path):
    with world(tmp_path) as (fanin, session, focal, owner):
        root = session.read_root()
        prior = next(
            row for row in session.events()
            if read_actor_access(session, focal, row["event_id"])["status"]
            == "PERCEIVED"
            and read_actor_access(session, P_ID, row["event_id"])["status"]
            == "NOT_PERCEIVED"
        )
        start_clock = session.world().clock
        recorded = entry(
            session, exposed=[P_ID, O_ID],
            private_state={"note": REL_SECRET},
        )
        assert recorded["status"] == "RECORDED"
        assert recorded["current_status"] == "ACTIVE"
        assert recorded["representation_depth"] == 1
        claimed = next(
            row for row in session.product.store.episodes(session.branch_id)
            if row["episode_id"] == recorded["primary_episode_id"]
        )
        claimed_body = canonical(claimed["body"])
        baseline = counts(session)
        retried = entry(
            session, exposed=[P_ID, O_ID],
            private_state={"note": REL_SECRET},
        )
        assert retried["status"] == "UNCHANGED"
        assert retried["primary_episode_id"] == recorded["primary_episode_id"]
        assert counts(session) == baseline

        result, proposal, before, event_id = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="c05:op:e1", event_id="c05:e1",
        )
        assert result.status == "REALIZED"
        assert session.event(event_id)["clock"] == proposal.event_time
        assert session.world().clock == proposal.event_time
        assert owner.realize("c05:op:e1", proposal, before) == result
        assert owner.snapshot().actor == focal
        assert session.read_root()["actor_ids"] == root["actor_ids"]

        for actor_id, status in (
            (focal, "PERCEIVED"), (P_ID, "PERCEIVED"),
            (O_ID, "PERCEIVED"),
        ):
            assert read_actor_access(
                session, actor_id, event_id)["status"] == status
        assert read_actor_access(
            session, focal, prior["event_id"])["status"] == "PERCEIVED"
        assert read_actor_access(
            session, P_ID, prior["event_id"])["status"] == "NOT_PERCEIVED"

        parent = read_actor_relative_context(session, P_ID, event_id)
        neighbor = read_actor_relative_context(session, O_ID, event_id)
        child = read_actor_relative_context(session, focal, event_id)
        assert parent["event_access"]["status"] == "PERCEIVED"
        assert neighbor["event_access"]["status"] == "PERCEIVED"
        assert child["event_access"]["status"] == "PERCEIVED"
        assert parent["relation_scope"]["status"] == "QUALIFIED"
        assert neighbor["relation_scope"]["status"] == "QUALIFIED"
        assert child["relation_scope"]["status"] == "HOLD_NOT_EXPOSED"
        assert child["relation_scope"]["relations"] == []
        assert child["relation_scope"]["withheld_relation_count"] == 1
        assert parent["viewer"] != child["viewer"]

        for context, counterpart in (
            (parent, O_ID), (neighbor, P_ID),
        ):
            relation = context["relation_scope"]["relations"][0]
            assert relation["counterpart"]["actor_id"] == counterpart
            assert relation["history_complete"] is True
            assert relation["representation_depth"] == 1
            assert [row["change"] for row in relation["entries"]] == ["ENTER"]
            assert relation["entries"][0]["clock"] == start_clock
            assert context["context_effect"]["relation_aware"] is True
            assert context["context_effect"][
                "both_parties_event_access"] is True

        for context in (parent, neighbor, child):
            blob = canonical(context)
            assert P_SECRET not in blob
            assert O_SECRET not in blob
            assert REL_SECRET not in blob
            assert context["private_state"] == "NOT_READ"
        assert REL_SECRET not in canonical(session.event(event_id))
        assert REL_SECRET not in canonical(session.world().snapshot())

        badges = relation_counts(session)
        assert badges["parent_registrations"] == 1
        assert badges["neighbor_registrations"] == 1
        assert badges["relation_changes"] == 1
        assert badges["relation_heads"] == 1
        assert badges["c04_utterances"] == 0
        assert canonical(
            next(row for row in session.product.store.episodes(
                session.branch_id)
                if row["episode_id"] == recorded["primary_episode_id"])["body"]
        ) == claimed_body


def test_partial_exposure_promotion_and_dated_history_no_retro_fill(tmp_path):
    with world(tmp_path) as (fanin, session, focal, owner):
        start_clock = session.world().clock
        entry(session, exposed=[P_ID, O_ID])
        _, _, _, first_event = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="c05:op:e1", event_id="c05:e1",
        )
        first_parent = read_actor_relative_context(
            session, P_ID, first_event)
        first_child = read_actor_relative_context(
            session, focal, first_event)
        assert first_child["relation_scope"]["status"] == "HOLD_NOT_EXPOSED"

        _, _, _, second_event = later_event(
            owner, session, (focal, P_ID),
            operation_id="c05:op:e2", event_id="c05:e2",
        )
        changed = change(session, exposed=[P_ID, O_ID, focal])
        assert changed["current_status"] == "CHANGED"
        promoted = promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
            depth=2, clock=session.world().clock,
            operation_id="c05:rel:promote",
        )
        assert promoted["status"] == "RECORDED"
        assert promoted["representation_depth"] == 2

        parent = read_actor_relative_context(
            session, P_ID, second_event)
        neighbor = read_actor_relative_context(
            session, O_ID, second_event)
        child = read_actor_relative_context(
            session, focal, second_event)
        assert parent["event_access"]["status"] == "PERCEIVED"
        assert neighbor["event_access"]["status"] == "NOT_PERCEIVED"
        assert child["event_access"]["status"] == "PERCEIVED"
        for context in (parent, neighbor):
            relation = context["relation_scope"]["relations"][0]
            assert relation["history_complete"] is True
            assert relation["representation_depth"] == 2
            assert relation["status"] == "CHANGED"
            assert [row["change"] for row in relation["entries"]] == [
                "ENTER", "CHANGE"]
            assert context["context_effect"][
                "both_parties_event_access"] is False
        child_relation = child["relation_scope"]["relations"][0]
        assert child["relation_scope"]["status"] == "QUALIFIED"
        assert child_relation["history_complete"] is False
        assert child_relation["prior_exposure"] == "HOLD_NOT_EXPOSED"
        assert child_relation["representation_depth"] == 2
        assert [row["change"] for row in child_relation["entries"]] == [
            "CHANGE"]
        assert all(row["change"] != "ENTER"
                   for row in child_relation["entries"])
        assert child["context_effect"]["both_parties_event_access"] is None

        assert read_actor_relative_context(
            session, P_ID, first_event) == first_parent
        assert read_actor_relative_context(
            session, focal, first_event) == first_child
        stored = next(
            row for row in session.product.store.episodes(session.branch_id)
            if row["kind"] == RELATION_CHANGE_KIND
            and (row.get("body") or {}).get("change") == "ENTER"
        )
        assert stored["body"]["clock"] == start_clock

        before_retry = counts(session)
        retried = promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
            depth=2, clock=promoted["clock"],
            operation_id="c05:rel:promote",
        )
        assert retried["status"] == "UNCHANGED"
        assert retried["primary_episode_id"] == promoted[
            "primary_episode_id"]
        assert counts(session) == before_retry


def test_actual_leave_restore_and_sever_hold_without_world_change(tmp_path):
    from unittest.mock import patch

    with world(tmp_path) as (fanin, session, focal, owner):
        entry(session, exposed=[P_ID, O_ID])
        _, _, _, first_event = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="c05:op:e1", event_id="c05:e1",
        )
        _, _, _, second_event = later_event(
            owner, session, (focal, P_ID),
            operation_id="c05:op:e2", event_id="c05:e2",
        )
        changed = change(session, exposed=[P_ID, O_ID, focal])
        promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
            depth=2, clock=session.world().clock,
            operation_id="c05:rel:promote",
        )
        world_before = session.world().snapshot()
        events_before = session.events()
        perceptions_before = session.product.store.perceptions(
            session.branch_id)
        checkpoints_before = session.product.store.checkpoints(
            session.branch_id)
        left = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
            change="LEAVE", clock=session.world().clock,
            operation_id="c05:rel:leave", exposed_actor_ids=[P_ID, O_ID],
        )
        assert left["current_status"] == "LEFT"
        left_parent = read_actor_relative_context(
            session, P_ID, second_event)
        left_child = read_actor_relative_context(
            session, focal, second_event)
        assert left_parent["relation_scope"]["relations"][0]["status"] == "LEFT"
        assert left_parent["relation_scope"]["relations"][0]["entries"][-1][
            "change"] == "LEAVE"
        assert [row["change"] for row in left_child[
            "relation_scope"]["relations"][0]["entries"]] == ["CHANGE"]

        restored = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
            change="ENTER", clock=session.world().clock,
            operation_id="c05:rel:reenter", exposed_actor_ids=[P_ID, O_ID],
            value="member",
        )
        assert restored["current_status"] == "ACTIVE"
        stable = {
            actor_id: read_actor_relative_context(
                session, actor_id, second_event)
            for actor_id in (P_ID, O_ID, focal)
        }
        assert stable[P_ID]["relation_scope"]["relations"][0]["status"] == (
            "ACTIVE")

        store = session.product.store
        original = store.episodes
        severed_id = changed["primary_episode_id"]

        def severed(branch_id):
            return [
                row for row in original(branch_id)
                if row.get("episode_id") != severed_id
            ]

        with patch.object(store, "episodes", side_effect=severed):
            for actor_id, access in (
                (P_ID, "PERCEIVED"), (O_ID, "NOT_PERCEIVED"),
                (focal, "PERCEIVED"),
            ):
                history = read_relation_history(
                    session, actor_id,
                    as_of_clock=session.event(second_event)["clock"])
                assert history["status"] == "HOLD_CUSTODY_SEVERED"
                context = read_actor_relative_context(
                    session, actor_id, second_event)
                assert context["relation_scope"]["status"] == (
                    "HOLD_CUSTODY_SEVERED")
                assert context["relation_scope"]["relations"] == []
                assert context["event_access"]["status"] == access
            assert session.world().snapshot() == world_before
            assert session.events() == events_before
            assert session.product.store.perceptions(
                session.branch_id) == perceptions_before
            assert session.product.store.checkpoints(
                session.branch_id) == checkpoints_before
        for actor_id in (P_ID, O_ID, focal):
            assert read_actor_relative_context(
                session, actor_id, second_event) == stable[actor_id]
        assert read_actor_relative_context(
            session, P_ID, first_event)["relation_scope"]["status"] == (
            "QUALIFIED")


def test_stranger_clock_forgery_operation_reuse_and_private_leak_refuse(
        tmp_path):
    from unittest.mock import patch

    with world(tmp_path) as (fanin, session, focal, owner):
        recorded = entry(
            session, exposed=[P_ID, O_ID],
            private_state={"note": REL_SECRET},
        )
        _, _, _, event_id = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="c05:op:e1", event_id="c05:e1",
        )
        baseline = counts(session)
        world_before = session.world().snapshot()

        with pytest.raises(
                RecursionRefusal, match="RELATION_ACTOR_UNKNOWN"):
            record_relation_change(
                session, actor_id=P_ID,
                other_actor_id="TEST_ONLY_C05_STRANGER",
                relation=RELATION, change="ENTER",
                clock=session.world().clock, operation_id="bad:stranger",
            )
        with pytest.raises(RecursionRefusal, match="RELATION_ACTOR_UNKNOWN"):
            read_relation_history(
                session, P_ID,
                other_actor_id="TEST_ONLY_C05_STRANGER",
                relation=RELATION)
        with pytest.raises(RecursionRefusal, match="RELATION_CLOCK_FUTURE"):
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock + 1,
                operation_id="bad:future", exposed_actor_ids=[P_ID, O_ID],
            )
        with pytest.raises(
                RecursionRefusal, match="RELATION_CLOCK_BACKDATED"):
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock - 1,
                operation_id="bad:backdated",
                exposed_actor_ids=[P_ID, O_ID],
            )
        with pytest.raises(
                RecursionRefusal, match="RELATION_OPERATION_REUSE_MISMATCH"):
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="ENTER",
                clock=recorded["clock"],
                operation_id="c05:rel:enter",
                exposed_actor_ids=[P_ID, O_ID], value="different",
                private_state={"note": REL_SECRET},
            )
        with pytest.raises(
                RecursionRefusal, match="RELATION_EXPOSURE_MISSING_PARTY"):
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock,
                operation_id="bad:exposure",
                exposed_actor_ids=[P_ID],
            )
        with pytest.raises(
                RecursionRefusal, match="RELATION_PRIVATE_STATE_LEAK"):
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock,
                operation_id="bad:leak", exposed_actor_ids=[P_ID, O_ID],
                value=REL_SECRET,
                private_state={"note": REL_SECRET},
            )
        assert counts(session) == baseline
        assert session.world().snapshot() == world_before

        unknown = read_relation_history(
            session, P_ID, other_actor_id=O_ID,
            relation="different-relation")
        assert unknown["status"] == "HOLD_UNKNOWN_SCOPE"

        store = session.product.store
        original = store.episodes
        stored = next(
            row for row in original(session.branch_id)
            if row["episode_id"] == recorded["primary_episode_id"])

        def forged(field, value):
            def patched(branch_id):
                rows = []
                for row in original(branch_id):
                    if row.get("episode_id") == stored["episode_id"]:
                        body = dict(row["body"])
                        body[field] = value
                        row = {**row, "body": body}
                    rows.append(row)
                return rows
            return patched

        for field, value in (
            ("root", "wrong-root"),
            ("branch", "wrong-branch"),
            ("aliases", ["X", "Y"]),
            ("value", "forged-value"),
        ):
            with patch.object(
                    store, "episodes", side_effect=forged(field, value)):
                history = read_relation_history(
                    session, P_ID,
                    as_of_clock=session.event(event_id)["clock"])
                assert history["status"] == "HOLD_CUSTODY_SEVERED"
                context = read_actor_relative_context(
                    session, P_ID, event_id)
                assert context["relation_scope"]["status"] == (
                    "HOLD_CUSTODY_SEVERED")
                assert context["relation_scope"]["relations"] == []
                assert context["event_access"]["status"] == "PERCEIVED"
            assert counts(session) == baseline
            assert read_actor_relative_context(
                session, P_ID, event_id)["relation_scope"]["status"] == (
                "QUALIFIED")


def test_cold_process_reads_same_relations_and_does_not_duplicate_state(
        tmp_path):
    with world(tmp_path) as (fanin, session, focal, owner):
        entry(session, exposed=[P_ID, O_ID],
              private_state={"note": REL_SECRET})
        _, _, _, first_event = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="c05:op:e1", event_id="c05:e1",
        )
        _, _, _, second_event = later_event(
            owner, session, (focal, P_ID),
            operation_id="c05:op:e2", event_id="c05:e2",
        )
        change(session, exposed=[P_ID, O_ID, focal])
        promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
            depth=2, clock=session.world().clock,
            operation_id="c05:rel:promote",
        )
        second_clock = session.event(second_event)["clock"]
        warm = {
            "root": session.read_root()["actor_ids"],
            "clock": session.world().clock,
            "world_hash": digest(session.world().snapshot()),
            "counts": counts(session),
            "relation_counts": relation_counts(session),
            "parent": read_supporting_actor(session, P_ID),
            "neighbor": read_supporting_actor(session, O_ID),
            "history_parent": read_relation_history(
                session, P_ID, as_of_clock=second_clock),
            "contexts": {
                f"{actor_id}|{event}": read_actor_relative_context(
                    session, actor_id, event)
                for actor_id in (P_ID, O_ID, focal)
                for event in (first_event, second_event)
            },
        }
        state_root = str(tmp_path / "p2")

    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.p2_owner import load_p2
from developmental_recursion.supporting_actor import read_supporting_actor
from developmental_recursion.continuing_relations import (
    read_actor_relative_context, read_relation_history, RELATION_CHANGE_KIND,
    RELATION_HEAD_KIND,
)
fanin = load_p2().open(Path(sys.argv[2]))
try:
    s = fanin.session
    store = s.product.store
    episodes = store.episodes(s.branch_id)
    print(json.dumps({
        "root": s.read_root()["actor_ids"],
        "clock": s.world().clock,
        "world_hash": __import__("developmental_recursion.contracts",
                                 fromlist=["digest"]).digest(
                                     s.world().snapshot()),
        "counts": {
            "episodes": len(episodes),
            "world_events": len(store.world_events(s.branch_id)),
            "perceptions": len(store.perceptions(s.branch_id)),
            "checkpoints": len(store.checkpoints(s.branch_id)),
        },
        "relation_counts": {
            "parent_registrations": len([r for r in episodes
                if r.get("kind") == "P2_SUPPORTING_ACTOR"
                and (r.get("body") or {}).get("actor_id") == sys.argv[3]]),
            "neighbor_registrations": len([r for r in episodes
                if r.get("kind") == "P2_SUPPORTING_ACTOR"
                and (r.get("body") or {}).get("actor_id") == sys.argv[4]]),
            "relation_changes": len([r for r in episodes
                if r.get("kind") == RELATION_CHANGE_KIND]),
            "relation_heads": len([r for r in episodes
                if r.get("kind") == RELATION_HEAD_KIND]),
            "c04_utterances": len([r for r in episodes
                if r.get("kind") == "P2_PARENT_UTTERANCE"]),
        },
        "parent": read_supporting_actor(s, sys.argv[3]),
        "neighbor": read_supporting_actor(s, sys.argv[4]),
        "history_parent": read_relation_history(
            s, sys.argv[3], as_of_clock=int(sys.argv[7])),
        "contexts": {
            actor + "|" + event: read_actor_relative_context(s, actor, event)
            for actor in (sys.argv[3], sys.argv[4], sys.argv[5])
            for event in (sys.argv[6], sys.argv[8])
        },
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(REPO), state_root,
         P_ID, O_ID, focal, first_event, str(second_clock), second_event],
        cwd=REPO, capture_output=True, text=True, timeout=180, check=True,
    )
    cold = json.loads(completed.stdout)
    assert cold["root"] == warm["root"]
    assert cold["clock"] == warm["clock"]
    assert cold["world_hash"] == warm["world_hash"]
    assert cold["counts"] == warm["counts"]
    assert cold["relation_counts"] == warm["relation_counts"]
    assert cold["parent"] == warm["parent"]
    assert cold["neighbor"] == warm["neighbor"]
    assert cold["history_parent"] == warm["history_parent"]
    for key, value in warm["contexts"].items():
        assert cold["contexts"][key] == value
    assert P_SECRET not in completed.stdout
    assert O_SECRET not in completed.stdout
    assert REL_SECRET not in completed.stdout
