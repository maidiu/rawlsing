"""S41 canonical prior-history binding regressions."""
from __future__ import annotations

import sqlite3

import pytest

from s41.bootstrap import install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from s41.bindings import append_event_binding, binding_episodes, make_continuation_binding  # noqa: E402
from s41.event import (  # noqa: E402
    ContinuationProducer,
    S41EventRefusal,
    build_second_occurrence,
    history_record_from_prior,
    world_prerequisites,
)
from s41.performer import perform_continuation_attempt  # noqa: E402
from s41.reader import S41ReadRefusal  # noqa: E402
from s41.session import S41Session  # noqa: E402
from s39.sources import make_source  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(tmp_path):
    case = case_for(True)
    return S41Session.start(tmp_path / "state", case=case, source=source_for(case))


def _bad_history(good, case: str):
    content = dict(good["content"])
    source_ref = good["source_ref"]
    if case == "unrelated_source_ref":
        source_ref = "TEST_ONLY_UNRELATED_SELFSEALED"
        content["prior_b_event_hash"] = "0" * 64
    elif case == "wrong_b_hash":
        content["prior_b_event_hash"] = "0" * 64
    elif case == "wrong_c8_content_hash":
        content["prior_c8_content_hash"] = "0" * 64
    elif case == "wrong_access_witness_hash":
        content["prior_access_witness_hash"] = "0" * 64
    elif case == "wrong_e1_hash":
        content["prior_e1_event_hash"] = "0" * 64
    elif case == "wrong_actor":
        content["prior_actor_id"] = "TEST_ONLY_WRONG_ACTOR"
    elif case == "wrong_branch":
        content["prior_branch_id"] = "WRONG_BRANCH"
    elif case == "wrong_event_time":
        content["prior_event_time"] = int(content["prior_event_time"]) + 1
    else:
        raise AssertionError(case)
    return make_source(
        source_ref=source_ref,
        source_class=good["source_class"],
        actor_id=good["actor_id"],
        branch_id=good["branch_id"] if case != "wrong_branch" else "WRONG_BRANCH",
        as_of=good["as_of"],
        predicate=good["predicate"],
        value=good["value"],
        content=content,
    )


@pytest.mark.parametrize(
    "case",
    [
        "unrelated_source_ref",
        "wrong_b_hash",
        "wrong_c8_content_hash",
        "wrong_access_witness_hash",
        "wrong_e1_hash",
        "wrong_actor",
        "wrong_branch",
        "wrong_event_time",
    ],
)
def test_wrong_history_refused_before_second_c8(case, tmp_path, monkeypatch):
    session = _start(tmp_path)
    try:
        first = session.read_events()[0]
        first_binding = binding_episodes(session)[0]
        original = history_record_from_prior

        def bad_history(session_arg, *, first_binding, as_of):
            good = original(session_arg, first_binding=first_binding, as_of=as_of)
            return _bad_history(good, case)

        import s41.session as session_module
        monkeypatch.setattr(session_module, "history_record_from_prior", bad_history)
        with pytest.raises(S41EventRefusal) as exc:
            session.continue_event(
                case=case_for(False), source=source_for(case_for(False))
            )
        assert "S41_HISTORY" in str(exc.value)
        assert len(binding_episodes(session)) == 1
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_persisted_wrong_b_hash_rejected_by_event_reader_and_cold(tmp_path):
    session = _start(tmp_path)
    try:
        first = session.read_events()[0]
        first_binding = binding_episodes(session)[0]
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
            good = history_record_from_prior(
                session, first_binding=first_binding, as_of=as_of
            )
            bad = _bad_history(good, "wrong_b_hash")
            from s39.sources import context_records
            records = context_records(
                actor_id=session.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
                branch_id=session.branch_id,
                as_of=as_of,
                repair_urgent=True,
                avoid_debt=True,
            ) + [bad]
            receipt = producer.generate(
                source_records=records,
                branch_id=session.branch_id,
                world=world_prerequisites(session),
            )
            assert receipt["selected_option"] == "REQUEST_TOOL"
            world = session.world()
            world.advance(occurrence.event_time)
            session.product._checkpoint(session.branch_id, world.clock, world)
            attempt = perform_continuation_attempt(
                session,
                receipt["attempt_request"],
                generation_receipt=receipt,
                e1_identity={
                    "event_id": producer.e1_event["event_id"],
                    "event_hash": producer.e1_event["hash"],
                    "c8_occurrence_id": producer.out9.occurrence_id,
                    "c8_state_digest": producer.out9.readset["state_digest"],
                },
            )
            producer.finalize_s36(attempt_result=attempt)
            binding = make_continuation_binding(
                session,
                producer=producer,
                generation=receipt,
                attempt=attempt,
                s36=producer.s36_binding,
                source=second_source,
                first_binding=first_binding,
                history_source=bad,
                world_before=session.world().snapshot(),
                world_after=session.world().snapshot(),
                status=attempt["attempt_status"],
            )
            append_event_binding(session, binding)
        finally:
            producer.close()
        with pytest.raises(S41ReadRefusal) as exc:
            session.read_event(binding["e1_event_id"])
        assert "S41_HISTORY" in str(exc.value)
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S41Session.open(tmp_path / "state")
