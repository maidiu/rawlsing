"""S41 two-event continuation over one persistent person."""
from __future__ import annotations

import json
import sqlite3

import pytest

from s41.bootstrap import install

install()

from candidate import seal  # noqa: E402
from candidate.actor_access_response import (  # noqa: E402
    make_actor_local_access_witness,
)
from s41.bindings import binding_episodes  # noqa: E402
from s41.event import (  # noqa: E402
    ContinuationProducer,
    S41EventRefusal,
    build_second_occurrence,
    history_record_from_prior,
    world_prerequisites,
)
from s41.session import S41Session  # noqa: E402
from s39.model import S39GenerationRefusal  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(tmp_path, *, share=True):
    case = case_for(share)
    return S41Session.start(tmp_path / "state", case=case, source=source_for(case))


def _c9_response_count(session) -> int:
    conn = sqlite3.connect(session._c9_path())
    try:
        return conn.execute("SELECT count(*) FROM response").fetchone()[0]
    finally:
        conn.close()


def _a_action_events(session):
    return [
        event for event in session.events()
        if event.get("actor_id") == "A"
        and event.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}
    ]


def test_two_event_same_person_root_branch_cold(tmp_path):
    session = _start(tmp_path, share=True)
    try:
        first = session.read_events()[0]
        first_response = first["c9"]["response_ref"]
        first_action = first["action_event_id"]
        first_clock = session.clock()
        root_actors = sorted(session.product.store.branch("root")["actor_ids"])
        branch_actors = sorted(session.product.store.branch(session.branch_id)["actor_ids"])
    finally:
        session.close()

    session = S41Session.open(tmp_path / "state")
    try:
        assert session.read_event(first["e1_event_id"])["c9"]["response_ref"] == first_response
        result = session.continue_event(
            case=case_for(False), source=source_for(case_for(False))
        )
        assert result["status"] == "OK"
        assert result["actor_action_appended"] is True
        events = session.read_events()
        assert [row["event_ordinal"] for row in events] == [1, 2]
        e1, e2 = events
        assert e1["e1_event_id"] != e2["e1_event_id"]
        assert e1["e1_event_hash"] != e2["e1_event_hash"]
        assert e1["c8_occurrence_id"] != e2["c8_occurrence_id"]
        assert e2["event_time"] > e1["event_time"]
        assert session.clock() > first_clock
        assert session.world().actor_state["A"]["tools_remaining"] == 1
        assert sorted(session.product.store.branch("root")["actor_ids"]) == root_actors
        assert sorted(session.product.store.branch(session.branch_id)["actor_ids"]) == branch_actors
        assert session.event(first_action) is not None
        assert session.read_event(e1["e1_event_id"])["status"] == "OK"
        assert session.read_event(e1["e1_event_id"])["c9"]["response_ref"] == first_response
        assert e2["source_operation"] == "REFUSE_TOOL"
        assert e2["selected_option"] == "REQUEST_TOOL"
        assert e2["attempt_status"] == "ADMITTED"
        assert e2["language"]["native_text"] == "¿Puedo usar la herramienta?"
        view = session.language_view(e2["action_event_id"], locale="en")
        assert view["status"] == "OK"
        assert view["translation_text"] == "May I use the tool?"
        assert session.read_latest()["event_ordinal"] == 2
        assert e2["c9"]["target_branch"] == "NO_CHANGE"
        assert e2["c9"]["target_reason"] == "NO_PROPOSAL"
        assert e2["c9"]["target_proposals"] == []
        assert e2["c9"]["target_state_rows"] == 0
        assert e2["history_refs"][0]["e1_event_id"] == e1["e1_event_id"]
        assert e2["history_predicate"] == "PRIOR_B_SHARE"
        assert any(
            ref.startswith("TEST_ONLY_S41_HIST_")
            for ref in e2["generation_source_refs"]
        )
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = S41Session.open(tmp_path / "state")
    try:
        cold_events = cold.read_events()
        assert [row["event_ordinal"] for row in cold_events] == [1, 2]
        assert cold_events[0]["c9"]["response_ref"] == first_response
        assert cold_events[1]["event_ordinal"] == 2
        assert cold_events[1]["language"]["translation_text"] == "May I use the tool?"
        assert cold.read_latest()["event_ordinal"] == 2
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_open_second_event_no_actor_action_and_duplicate_replay(tmp_path):
    session = _start(tmp_path, share=True)
    try:
        before_actions = len(_a_action_events(session))
        before_responses = _c9_response_count(session)
        result = session.continue_event(
            case=case_for(False), source=source_for(case_for(False)),
            source_records=[],
        )
        assert result["status"] == "OPEN"
        assert result["actor_action_appended"] is False
        e2 = result["event"]
        assert e2["status"] == "OPEN"
        assert e2["generation_status"] == "OPEN_CHOICE_SET"
        assert e2["actor_action_appended"] is False
        assert "c9" not in e2 or e2.get("c9") is None
        assert len(_a_action_events(session)) == before_actions
        assert _c9_response_count(session) == before_responses
        assert len(binding_episodes(session)) == 2
        with pytest.raises(S41EventRefusal) as exc:
            session.continue_event(
                case=case_for(False), source=source_for(case_for(False))
            )
        assert exc.value.code == "S41_ALREADY_CONTINUED"
        assert len(binding_episodes(session)) == 2
        assert len(_a_action_events(session)) == before_actions
        assert _c9_response_count(session) == before_responses
    finally:
        session.close()


def test_denied_second_event_uses_current_world_without_success(tmp_path):
    session = _start(tmp_path, share=True)
    try:
        take = session.product.take_tool("A")
        assert take["status"] == "OK"
        assert session.world().resources["workshop"]["tool_available"] is False
        result = session.continue_event(
            case=case_for(False), source=source_for(case_for(False))
        )
        e2 = result["event"]
        assert e2["attempt_status"] == "DENIED"
        assert e2["performed"] is False
        assert e2["language"] is None
        assert e2["action_event_id"] == ""
        assert e2["c9"]["outcome"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
        assert e2["c9"]["target_branch"] == "NO_CHANGE"
        assert e2["c9"]["target_proposals"] == []
        assert e2["world_tools_remaining"] == 1
        assert e2["world_after"]["resources"]["workshop"]["tool_available"] is False
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_wrong_second_source_and_duplicate_do_not_append_action(tmp_path):
    session = _start(tmp_path, share=True)
    try:
        first = session.read_events()[0]
        before_actions = len(_a_action_events(session))
        before_responses = _c9_response_count(session)
        base = source_for(case_for(False))
        mutations = {
            "wrong_owner": {"b_owner": "FAKE_OWNER"},
            "wrong_actor": {"b_actor": "TEST_ONLY_WRONG_B"},
            "wrong_recipient": {"b_to_actor": "TEST_ONLY_WRONG_A"},
            "wrong_hash": {"b_event_hash": "0" * 64},
            "wrong_clock": {"b_clock": 999},
            "wrong_operation": {"b_operation": "SHARE_TOOL", "b_quantity": 1},
        }
        for label, mutation in mutations.items():
            mutated = dict(base)
            mutated.update(mutation)
            with pytest.raises(Exception):
                session.continue_event(case=case_for(False), source=mutated)
            assert len(_a_action_events(session)) == before_actions, label
            assert _c9_response_count(session) == before_responses, label
            assert len(binding_episodes(session)) == 1, label
            assert session.read_event(first["e1_event_id"])["status"] == "OK", label
        with pytest.raises(S41EventRefusal) as exc:
            session.continue_event(
                case=case_for(False), source=base,
                event_time=first["event_time"],
            )
        assert exc.value.code == "S41_EVENT_TIME_NOT_LATER"
        assert len(_a_action_events(session)) == before_actions
        assert _c9_response_count(session) == before_responses
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_tampered_actual_prior_history_and_access_refuse_then_restore(tmp_path):
    session = _start(tmp_path, share=True)
    try:
        first = session.read_events()[0]
        first_binding = binding_episodes(session)[0]
        # The first event is a C8 occurrence, not a C12 world event.
        from c8_readonly_consumer import C8ReadOnlyConsumer
        c8_event = C8ReadOnlyConsumer(
            first_binding["c8"]["journal_path"]
        ).load().get(first_binding["c8"]["occurrence_id"])
        second_case = case_for(False)
        second_source = source_for(second_case)
        occurrence, _ = build_second_occurrence(
            session,
            first_binding=first_binding,
            first_payload=c8_event["payload"],
            second_source=second_source,
            event_time=session.clock() + 1,
        )
        producer = ContinuationProducer(
            session.state_root / "source",
            case=second_case,
            source=second_source,
            occurrence=occurrence,
            current_tools=session.world().actor_state["A"]["tools_remaining"],
        )
        try:
            producer.commit_incoming()
            as_of = occurrence.event_time + 5
            history = history_record_from_prior(
                session, first_binding=first_binding, as_of=as_of
            )
            records = context_records(
                actor_id=session.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
                branch_id=session.branch_id,
                as_of=as_of,
                repair_urgent=True,
                avoid_debt=True,
            ) + [history]
            tampered = dict(history)
            tampered["content"] = {"mapped_from_e1_event_id": "WRONG"}
            with pytest.raises(S39GenerationRefusal):
                producer.generate(
                    source_records=records[:-1] + [tampered],
                    branch_id=session.branch_id,
                    world=world_prerequisites(session),
                )
            restored = producer.generate(
                source_records=records,
                branch_id=session.branch_id,
                world=world_prerequisites(session),
            )
            assert restored["selected_option"] == "REQUEST_TOOL"
            access = make_actor_local_access_witness(
                actor_id=producer.occurrence.actor_id,
                event_ref=producer.e1_event["hash"],
                access_time=producer.event_time,
                source_ref="TEST_ONLY_ADP017_ACCESS_S41_WRONG",
                access_status="ACCESSIBLE",
                scene="workshop",
                revoked=True,
            )
            with pytest.raises(S39GenerationRefusal):
                producer.generate(
                    source_records=records,
                    branch_id=session.branch_id,
                    world=world_prerequisites(session),
                    access_witness=access,
                )
            restored_again = producer.generate(
                source_records=records,
                branch_id=session.branch_id,
                world=world_prerequisites(session),
            )
            assert restored_again["selected_option"] == "REQUEST_TOOL"
        finally:
            producer.close()
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert len(binding_episodes(session)) == 1
        assert _c9_response_count(session) == 1
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_second_event_plan_projection_mismatch_refused_but_first_intact(tmp_path):
    session = _start(tmp_path, share=True)
    try:
        session.continue_event(case=case_for(False), source=source_for(case_for(False)))
        first, second = session.read_events()
        rows = [
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "LANGUAGE_TRANSLATION_PROJECTION"
            and (row.get("body") or {}).get("source_speech_event_id")
            == second["action_event_id"]
        ]
        assert len(rows) == 1
        body = dict(rows[0]["body"])
        body["plan_hash"] = "0" * 64
        body["tamper_note"] = "s41-second-plan-mismatch"
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
            session.clock(), body,
        )
        from s41.reader import S41ReadRefusal
        with pytest.raises(S41ReadRefusal):
            session.read_event(second["e1_event_id"])
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S41Session.open(tmp_path / "state")
