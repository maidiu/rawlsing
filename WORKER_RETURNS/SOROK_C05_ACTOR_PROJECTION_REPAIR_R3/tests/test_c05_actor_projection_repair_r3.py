"""C05 R3 actor-facing projection and retrospective temporal repair tests."""
from __future__ import annotations

import json
import os
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
    EventProposal, RecursionRefusal,
)
from developmental_recursion.continuing_relations import (  # noqa: E402
    promote_relation, read_actor_relative_context, read_relation_history,
    record_relation_change,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access, register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_R3_PARENT"
O_ID = "TEST_ONLY_C05_R3_NEIGHBOR"
Q_ID = "TEST_ONLY_C05_R3_OBSERVER"
R_ID = "TEST_ONLY_C05_R3_OUTSIDER"
HIDDEN = "r3-hidden-relation"
VISIBLE = "r3-visible-relation"
REL_ONE = "r3-known-one"
REL_TWO = "r3-known-two"
RELATION = "r3-temporal-relation"


def start_world(tmp_path, *, register_r=False):
    fanin = load_p2().start(tmp_path / "p2")
    session = fanin.session
    focal = session.read_root()["actor_ids"][0]
    for alias, actor_id in (("R3P", P_ID), ("R3O", O_ID), ("R3Q", Q_ID)):
        register_supporting_actor(
            session, alias=alias, actor_id=actor_id, role="neighbor",
            private_state={"motive": actor_id + "-private"})
    if register_r:
        register_supporting_actor(
            session, alias="R3R", actor_id=R_ID, role="neighbor",
            private_state={"motive": R_ID + "-private"})
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin, case=case, source=fanin.deps["source_for"](case),
        participants=(focal, P_ID, O_ID))
    return fanin, session, focal, owner


def later_event(owner, session, participants, *, operation_id, event_id,
                delta=6):
    before = owner.snapshot()
    proposal = EventProposal(
        event_id, before.clock + delta, "ADMIT_EVENT",
        (owner.source_ref,), tuple(participants), {})
    result = owner.realize(operation_id, proposal, before)
    supporting = list(
        (result.consequences or {}).get("supporting_participants") or ())
    event_id = supporting[0]["event_id"] if supporting else None
    return result, proposal, event_id


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
    }


def viewer_document(session, viewer, event_id):
    return {
        "history": read_relation_history(session, viewer),
        "context": read_actor_relative_context(session, viewer, event_id),
        "event": session.event(event_id),
        "access": read_actor_access(session, viewer, event_id),
    }


def assert_no_withheld(value):
    if isinstance(value, dict):
        assert "withheld_relation_count" not in value
        for item in value.values():
            assert_no_withheld(item)
    elif isinstance(value, list):
        for item in value:
            assert_no_withheld(item)


def cold_document(state_root, viewer, event_id):
    script = r"""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
from developmental_recursion.continuing_relations import (
    read_actor_relative_context, read_relation_history,
)
from developmental_recursion.p2_owner import load_p2
from developmental_recursion.supporting_actor import read_actor_access
fanin = load_p2().open(Path(sys.argv[2]))
try:
    s = fanin.session
    event = s.event(sys.argv[4])
    print(json.dumps({
        "history": read_relation_history(s, sys.argv[3]),
        "context": read_actor_relative_context(s, sys.argv[3], sys.argv[4]),
        "event": event,
        "access": read_actor_access(s, sys.argv[3], sys.argv[4]),
        "root": s.read_root()["actor_ids"],
        "clock": s.world().clock,
    }, sort_keys=True))
finally:
    fanin.close()
"""
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(REPO), state_root,
         viewer, event_id],
        cwd=REPO, capture_output=True, text=True, timeout=180,
        env=os.environ.copy(), check=True)
    return json.loads(completed.stdout)


def test_hidden_relation_noninterference_named_scope_cold_and_sever(tmp_path):
    fanin, session, focal, owner = start_world(tmp_path, register_r=True)
    try:
        _, _, event_id = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:ch1:event", event_id="r3:ch1:event")
        a_doc = viewer_document(session, Q_ID, event_id)
        state_root = str(tmp_path / "p2")
        a_cold = cold_document(state_root, Q_ID, event_id)
        hidden = record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=HIDDEN, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch1:hidden", exposed_actor_ids=[P_ID, O_ID],
            value="hidden-guest")
        b_doc = viewer_document(session, Q_ID, event_id)
        b_cold = cold_document(state_root, Q_ID, event_id)
        assert a_doc == b_doc
        assert a_cold["history"] == a_doc["history"]
        assert a_cold["context"] == a_doc["context"]
        assert a_cold["event"] == a_doc["event"]
        assert a_cold["access"] == a_doc["access"]
        assert b_cold["history"] == b_doc["history"]
        assert b_cold["context"] == b_doc["context"]
        assert_no_withheld(a_doc)
        assert_no_withheld(b_doc)
        assert a_doc["history"]["status"] == "HOLD_NOT_EXPOSED"
        assert b_doc["history"]["status"] == "HOLD_NOT_EXPOSED"
        assert a_doc["context"]["relation_scope"]["status"] == (
            "HOLD_NOT_EXPOSED")
        assert b_doc["context"]["relation_scope"]["status"] == (
            "HOLD_NOT_EXPOSED")

        missing = read_relation_history(
            session, Q_ID, other_actor_id=P_ID, relation="r3-missing")
        hidden_named = read_relation_history(
            session, Q_ID, other_actor_id=P_ID, relation=HIDDEN)
        assert missing == hidden_named
        assert missing["status"] == "HOLD_NOT_EXPOSED"

        store = session.product.store
        original = store.episodes
        hidden_id = hidden["primary_episode_id"]

        def hide_hidden(branch_id):
            return [
                row for row in original(branch_id)
                if row.get("episode_id") != hidden_id
            ]

        from unittest.mock import patch
        with patch.object(store, "episodes", side_effect=hide_hidden):
            hidden_sever = viewer_document(session, Q_ID, event_id)
        assert hidden_sever == b_doc

        visible = record_relation_change(
            session, actor_id=P_ID, other_actor_id=R_ID,
            relation=VISIBLE, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch1:visible",
            exposed_actor_ids=[P_ID, R_ID, Q_ID], value="visible-guest")
        c_doc = viewer_document(session, Q_ID, event_id)
        assert c_doc["history"]["status"] == "QUALIFIED"
        assert c_doc["access"]["status"] == "NOT_PERCEIVED"
        relations = c_doc["context"]["relation_scope"]["relations"]
        assert [row["relation"] for row in relations] == [VISIBLE]
        assert c_doc["context"]["context_effect"]["relation_aware"] is True
        assert c_doc["context"]["context_effect"]["event_perception"] == (
            "NOT_PERCEIVED")
        assert "C12_EVENT_PERCEPTION" not in c_doc[
            "context"]["context_effect"]["basis"]
        assert_no_withheld(c_doc)

        visible_id = visible["primary_episode_id"]

        def hide_visible(branch_id):
            return [
                row for row in original(branch_id)
                if row.get("episode_id") != visible_id
            ]

        with patch.object(store, "episodes", side_effect=hide_visible):
            visible_sever = viewer_document(session, Q_ID, event_id)
        assert visible_sever["history"]["status"] == "HOLD_CUSTODY_SEVERED"
        assert visible_sever["context"]["relation_scope"]["status"] == (
            "HOLD_CUSTODY_SEVERED")
        assert visible_sever["access"]["status"] == "NOT_PERCEIVED"
        assert viewer_document(session, Q_ID, event_id) == c_doc
    finally:
        owner.close()


def test_viewer_specific_context_effect_and_plural_relations(tmp_path):
    fanin, session, focal, owner = start_world(tmp_path, register_r=True)
    try:
        for relation, other, operation in (
            (REL_ONE, O_ID, "r3:ch3:one"),
            (REL_TWO, R_ID, "r3:ch3:two"),
        ):
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=other,
                relation=relation, change="ENTER",
                clock=session.world().clock, operation_id=operation,
                exposed_actor_ids=[P_ID, other], value=relation)
        _, _, first_event = later_event(
            owner, session, (focal, O_ID),
            operation_id="r3:ch3:event1", event_id="r3:ch3:event1")
        first = read_actor_relative_context(session, P_ID, first_event)
        assert first["event_access"]["status"] == "NOT_PERCEIVED"
        assert first["relation_scope"]["status"] == "QUALIFIED"
        assert len(first["relation_scope"]["relations"]) == 2
        effect = first["context_effect"]
        assert effect["relation_aware"] is True
        assert effect["event_perception"] == "NOT_PERCEIVED"
        assert effect["event_perception_source"] == "VIEWER_EVENT_ACCESS"
        assert effect["event_perception_scope"] == "VIEWER_ONLY"
        assert effect["basis"] == ["DATED_RELATION_HISTORY"]
        assert "C12_EVENT_PERCEPTION" not in effect["basis"]
        assert effect["relation_count"] == 2
        assert effect["summary_selection"] == (
            "MECHANICAL_FIRST_SORTED_RELATION_KEY")
        assert effect["summary_is_salience_or_psychology"] is False
        assert effect["summary_relation_key"] == (
            first["relation_scope"]["relations"][0]["relation_key"])
        assert effect["both_parties_event_access"] is False
        assert effect["both_parties_event_access_scope"] == (
            "RELATION_PARTIES_ONLY")
        assert_no_withheld(first)

        _, _, second_event = later_event(
            owner, session, (focal, P_ID),
            operation_id="r3:ch3:event2", event_id="r3:ch3:event2")
        second = read_actor_relative_context(session, P_ID, second_event)
        assert second["event_access"]["status"] == "PERCEIVED"
        assert second["context_effect"]["event_perception"] == "PERCEIVED"
        assert "C12_EVENT_PERCEPTION" in second["context_effect"]["basis"]
        assert second["context_effect"]["relation_aware"] is True
        assert len(second["relation_scope"]["relations"]) == 2
        assert second["context_effect"]["relation_count"] == 2
        assert_no_withheld(second)
    finally:
        owner.close()


def test_retrospective_as_of_event_clock_and_event_time_hold(tmp_path):
    fanin, session, focal, owner = start_world(tmp_path)
    try:
        _, _, event1 = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:ch2:event1", event_id="r3:ch2:event1")
        event_before = session.event(event1)
        access_before = read_actor_access(session, P_ID, event1)
        before = read_actor_relative_context(session, P_ID, event1)
        assert before["relation_scope"]["status"] == "HOLD_NOT_EXPOSED"
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="ENTER", clock=session.world().clock,
            operation_id="r3:ch2:enter", exposed_actor_ids=[P_ID, O_ID],
            value="guest")
        promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, depth=2, clock=session.world().clock,
            operation_id="r3:ch2:promote")
        after_same_clock = read_actor_relative_context(
            session, P_ID, event1)
        assert session.event(event1) == event_before
        assert read_actor_access(session, P_ID, event1) == access_before
        assert after_same_clock["relation_scope"]["status"] == "QUALIFIED"
        assert after_same_clock["relation_scope"][
            "temporal_scope"] == "RETROSPECTIVE_AS_OF_EVENT_CLOCK"
        temporal = after_same_clock["relation_temporal"]
        assert temporal["relation_projection"] == (
            "RETROSPECTIVE_AS_OF_EVENT_CLOCK")
        assert temporal["event_time_relation_knowledge"] == "NOT_AVAILABLE"
        assert temporal["event_time_relation_status"] == (
            "HOLD_SOURCE_AUTHORITY")
        assert temporal["within_clock_cutoff"] == "UNAVAILABLE"
        assert temporal["usable_as_prior_event_cause"] is False
        relation = after_same_clock["relation_scope"]["relations"][0]
        assert relation["representation_depth"] == 2
        assert [row["change"] for row in relation["entries"]] == ["ENTER"]
        assert len(relation["promotions"]) == 1
        assert after_same_clock["context_effect"]["event_perception"] == (
            "PERCEIVED")
        assert "C12_EVENT_PERCEPTION" in after_same_clock[
            "context_effect"]["basis"]

        _, _, event2 = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:ch2:event2", event_id="r3:ch2:event2")
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="CHANGE", clock=session.world().clock,
            operation_id="r3:ch2:change", exposed_actor_ids=[P_ID, O_ID],
            value="later")
        after_later = read_actor_relative_context(session, P_ID, event1)
        assert after_later["relation_scope"] == after_same_clock[
            "relation_scope"]
        assert [row["change"] for row in after_later[
            "relation_scope"]["relations"][0]["entries"]] == ["ENTER"]
        assert after_later["event_access"] == before["event_access"]
        later_access = read_actor_access(session, P_ID, event1)
        assert later_access["status"] == access_before["status"]
        assert later_access["event"] == access_before["event"]
        assert later_access["receipt"] == access_before["receipt"]
        assert session.event(event1) == event_before
        cold = cold_document(str(tmp_path / "p2"), P_ID, event1)
        assert cold["context"] == after_later
        assert cold["event"] == event_before
        assert cold["access"]["status"] == access_before["status"]
        assert cold["access"]["event"] == access_before["event"]
        assert cold["access"]["receipt"] == access_before["receipt"]
        assert_no_withheld(after_later)
    finally:
        owner.close()


def test_preserved_relation_mechanics_under_new_projection(tmp_path):
    fanin, session, focal, owner = start_world(tmp_path)
    try:
        _, _, event_id = later_event(
            owner, session, (focal, P_ID, O_ID),
            operation_id="r3:keep:event", event_id="r3:keep:event")
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="ENTER", clock=session.world().clock,
            operation_id="r3:keep:enter", exposed_actor_ids=[P_ID, O_ID],
            value="guest")
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="CHANGE", clock=session.world().clock,
            operation_id="r3:keep:change", exposed_actor_ids=[P_ID, O_ID],
            value="member")
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="LEAVE", clock=session.world().clock,
            operation_id="r3:keep:leave", exposed_actor_ids=[P_ID, O_ID])
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, change="ENTER", clock=session.world().clock,
            operation_id="r3:keep:reenter", exposed_actor_ids=[P_ID, O_ID],
            value="member")
        promoted = promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, depth=2, clock=session.world().clock,
            operation_id="r3:keep:promote")
        history = read_relation_history(session, P_ID)
        relation = history["relations"][0]
        assert history["status"] == "QUALIFIED"
        assert relation["status"] == "ACTIVE"
        assert relation["representation_depth"] == 2
        assert [row["change"] for row in relation["entries"]] == [
            "ENTER", "CHANGE", "LEAVE", "ENTER"]
        baseline = counts(session)
        retry = promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID,
            relation=RELATION, depth=2, clock=promoted["clock"],
            operation_id="r3:keep:promote")
        assert retry["status"] == "UNCHANGED"
        assert retry["primary_episode_id"] == promoted["primary_episode_id"]
        assert counts(session) == baseline
        with pytest.raises(
                RecursionRefusal, match="RELATION_PROMOTION_NOT_DEEPER"):
            promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=session.world().clock,
                operation_id="r3:keep:promote2")
        assert counts(session) == baseline
        context = read_actor_relative_context(session, P_ID, event_id)
        assert context["event_access"]["status"] == "PERCEIVED"
        assert context["relation_scope"]["status"] == "QUALIFIED"
        assert context["context_effect"]["event_perception"] == "PERCEIVED"
        assert "C12_EVENT_PERCEPTION" in context["context_effect"]["basis"]
        assert context["private_state"] == "NOT_READ"
        for row in context["relation_scope"]["relations"]:
            assert row["private_state"] == "NOT_READ"
        assert_no_withheld(context)
    finally:
        owner.close()
