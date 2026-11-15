"""S41 actual generation-readset canonical-history regressions."""
from __future__ import annotations

import sqlite3

import pytest

from s41.bootstrap import install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from candidate import seal  # noqa: E402
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
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(tmp_path):
    case = case_for(True)
    return S41Session.start(tmp_path / "state", case=case, source=source_for(case))


def _c9_count(session):
    conn = sqlite3.connect(session._c9_path())
    try:
        return conn.execute("SELECT count(*) FROM response").fetchone()[0]
    finally:
        conn.close()


def _a_actions(session):
    return [
        event for event in session.events()
        if event.get("actor_id") == "A"
        and event.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}
    ]


def _replacement_receipt(receipt):
    return seal({
        key: value for key, value in receipt.items() if key != "hash"
    } | {"source_refs": ["TEST_ONLY_REPLACEMENT_SOURCE"]})


def test_replaced_generation_readset_refused_before_action(tmp_path, monkeypatch):
    session = _start(tmp_path)
    try:
        first = session.read_events()[0]
        before_actions = len(_a_actions(session))
        before_c9 = _c9_count(session)
        original = ContinuationProducer.generate

        def bad_generate(self, **kwargs):
            receipt = original(self, **kwargs)
            replacement = _replacement_receipt(receipt)
            self.generation_receipt = replacement
            return replacement

        monkeypatch.setattr(ContinuationProducer, "generate", bad_generate)
        with pytest.raises(S41EventRefusal) as exc:
            session.continue_event(
                case=case_for(False), source=source_for(case_for(False))
            )
        assert "S41_GENERATION_READSET_INVALID" in str(exc.value)
        assert len(binding_episodes(session)) == 1
        assert len(_a_actions(session)) == before_actions
        assert _c9_count(session) == before_c9
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_persisted_replaced_generation_readset_refused_warm_cold(tmp_path):
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
            receipt = producer.generate(
                source_records=records,
                branch_id=session.branch_id,
                world=world_prerequisites(session),
            )
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
            replacement = _replacement_receipt(receipt)
            replaced_attempt = seal({
                key: value for key, value in attempt.items() if key != "hash"
            } | {"generation_receipt_hash": replacement["hash"]})
            binding = make_continuation_binding(
                session,
                producer=producer,
                generation=replacement,
                attempt=replaced_attempt,
                s36=producer.s36_binding,
                source=second_source,
                first_binding=first_binding,
                history_source=history,
                world_before=session.world().snapshot(),
                world_after=session.world().snapshot(),
                status=replaced_attempt["attempt_status"],
            )
            append_event_binding(session, binding)
        finally:
            producer.close()
        with pytest.raises(S41ReadRefusal) as exc:
            session.read_event(binding["e1_event_id"])
        assert "S41_GENERATION_READSET_INVALID" in str(exc.value)
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S41Session.open(tmp_path / "state")


def _persisted_bad_input_binding(session, *, mode: str):
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
        history = history_record_from_prior(
            session, first_binding=first_binding, as_of=as_of
        )
        contexts = context_records(
            actor_id=session.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
            branch_id=session.branch_id,
            as_of=as_of,
            repair_urgent=True,
            avoid_debt=True,
        )
        receipt = producer.generate(
            source_records=contexts + [history],
            branch_id=session.branch_id,
            world=world_prerequisites(session),
        )
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
        from s39.sources import make_source
        if mode == "replacement":
            replacement = make_source(
                source_ref=history["source_ref"],
                source_class=history["source_class"],
                actor_id=history["actor_id"],
                branch_id=history["branch_id"],
                as_of=history["as_of"],
                predicate=history["predicate"],
                value=history["value"],
                content={
                    "mapping_premise": "REPLACED_ACTUAL_INPUT",
                    "prior_b_event_hash": "0" * 64,
                },
            )
            generation_sources = contexts + [replacement]
        elif mode == "duplicate":
            generation_sources = contexts + [history, dict(history)]
        else:
            raise AssertionError(mode)
        binding = make_continuation_binding(
            session,
            producer=producer,
            generation=receipt,
            attempt=attempt,
            s36=producer.s36_binding,
            source=second_source,
            first_binding=first_binding,
            history_source=history,
            world_before=session.world().snapshot(),
            world_after=session.world().snapshot(),
            status=attempt["attempt_status"],
            generation_sources=generation_sources,
        )
        append_event_binding(session, binding)
        return binding
    finally:
        producer.close()


@pytest.mark.parametrize(
    "mode,detail",
    [
        ("replacement", "S41_GENERATION_CANONICAL_INPUT_REPLACED"),
        ("duplicate", "S41_GENERATION_INPUT_SOURCE_DUPLICATE"),
    ],
)
def test_persisted_generation_input_substitution_refused_warm_cold(
    mode, detail, tmp_path
):
    session = _start(tmp_path)
    try:
        first = session.read_events()[0]
        binding = _persisted_bad_input_binding(session, mode=mode)
        with pytest.raises(S41ReadRefusal) as exc:
            session.read_event(binding["e1_event_id"])
        assert "S41_GENERATION_READSET_INVALID" in str(exc.value)
        assert detail in str(exc.value)
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S41Session.open(tmp_path / "state")
