"""S42 reusable ongoing-event consumer focused tests."""
from __future__ import annotations

import sqlite3

import pytest

from s42.bootstrap import install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from candidate import seal  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402
from s42.reader import S42ReadRefusal  # noqa: E402
from s42.session import S42Session  # noqa: E402
from s39.sources import make_source  # noqa: E402
from s41.event import S41EventRefusal  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(tmp_path):
    case = case_for(True)
    return S42Session.start(tmp_path / "state", case=case, source=source_for(case))


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


def _c8_count(session):
    rows = binding_episodes(session)
    reference = rows[0] if rows else None
    if reference is None:
        from s41.bindings import binding_episodes as s41_bindings
        reference = s41_bindings(session)[0]
    view = C8ReadOnlyConsumer(reference["c8"]["journal_path"]).load()
    return len(view.readset.to_json()["occurrence_ids"])


def _admit(session, *, share: bool, history_ordinals: tuple[int, ...] = ()):
    events = session.read_events()
    refs = tuple(events[index - 1]["e1_event_id"] for index in history_ordinals)
    return session.admit_event(
        case=case_for(share), source=source_for(case_for(share)),
        history_event_refs=refs,
    )


@pytest.mark.parametrize("length", [3, 5])
def test_variable_length_stream_with_cold_reopen(length, tmp_path):
    state = tmp_path / "state"
    case = case_for(True)
    session = S42Session.start(state, case=case, source=source_for(case))
    session.close()
    stream = [
        (False, (1,)),
        (True, (1,)),
        (False, (3,)),
        (True, (3,)),
    ][: length - 1]
    for share, history in stream:
        session = S42Session.open(state)
        try:
            result = _admit(session, share=share, history_ordinals=history)
            assert result["status"] == "OK"
        finally:
            session.close()
    session = S42Session.open(state)
    try:
        events = session.read_events()
        assert len(events) == length
        assert [row["event_ordinal"] for row in events] == list(range(1, length + 1))
        assert len({row["e1_event_id"] for row in events}) == length
        assert len({row["e1_event_hash"] for row in events}) == length
        assert len({row["c8_occurrence_id"] for row in events}) == length
        assert all(
            events[i]["event_time"] < events[i + 1]["event_time"]
            for i in range(length - 1)
        )
        assert sorted(session.product.store.branch("root")["actor_ids"]) == ["A", "B"]
        assert sorted(session.product.store.branch(session.branch_id)["actor_ids"]) == ["A", "B", "U"]
        assert session.world().actor_state["A"]["tools_remaining"] == 1
        assert session.read_latest()["event_ordinal"] == length
        for row in events:
            assert row["status"] == "OK"
            assert row["c9"]["target_branch"] == "NO_CHANGE"
            assert row["c9"]["target_reason"] == "NO_PROPOSAL"
            assert row["c9"]["target_proposals"] == []
            assert row["c9"]["target_state_rows"] == 0
            if row.get("language"):
                assert row["language"]["native_text"] == "¿Puedo usar la herramienta?"
                assert row["language"]["translation_text"] == "May I use the tool?"
        assert session.read_event(events[0]["e1_event_id"])["status"] == "OK"
        assert session.read_event(events[1]["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_open_then_continue_after_open(tmp_path):
    session = _start(tmp_path)
    try:
        result = session.admit_event(
            case=case_for(False), source=source_for(case_for(False)),
            history_event_refs=(),
        )
        assert result["status"] == "OPEN"
        assert result["actor_action_appended"] is False
        open_event = result["event"]
        assert open_event["status"] == "OPEN"
        assert open_event.get("c9") is None
        before_actions = len(_a_actions(session))
        before_c9 = _c9_count(session)
        continued = _admit(session, share=True, history_ordinals=(1,))
        assert continued["status"] == "OK"
        assert len(_a_actions(session)) == before_actions + 1
        assert _c9_count(session) == before_c9 + 1
        events = session.read_events()
        assert [row["event_ordinal"] for row in events] == [1, 2, 3]
        assert events[1]["status"] == "OPEN"
        assert events[2]["status"] == "OK"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_history_ref_reorder_duplicate_missing_refused(tmp_path):
    session = _start(tmp_path)
    try:
        _admit(session, share=False, history_ordinals=(1,))
        _admit(session, share=True, history_ordinals=(1,))
        events = session.read_events()
        before_actions = len(_a_actions(session))
        before_c9 = _c9_count(session)
        before_bindings = len(binding_episodes(session))
        bad_cases = [
            ((events[2]["e1_event_id"], events[0]["e1_event_id"]), "S42_HISTORY_INPUT_OUT_OF_ORDER"),
            ((events[0]["e1_event_id"], events[0]["e1_event_id"]), "S42_HISTORY_REF_DUPLICATE"),
            (("TEST_ONLY_MISSING_HISTORY",), "S42_HISTORY_REF_MISSING"),
            (("0" * 64,), "S42_HISTORY_REF_MISSING"),
        ]
        for refs, code in bad_cases:
            with pytest.raises(S41EventRefusal) as exc:
                session.admit_event(
                    case=case_for(False), source=source_for(case_for(False)),
                    history_event_refs=refs,
                )
            assert exc.value.code == code
            assert len(_a_actions(session)) == before_actions
            assert _c9_count(session) == before_c9
            assert len(binding_episodes(session)) == before_bindings
            assert session.read_event(events[0]["e1_event_id"])["status"] == "OK"
    finally:
        session.close()


def test_incoming_source_replay_at_same_clock_refused(tmp_path):
    session = _start(tmp_path)
    try:
        second = _admit(session, share=False, history_ordinals=(1,))
        event2 = second["event"]
        before_actions = len(_a_actions(session))
        before_c9 = _c9_count(session)
        before_c8 = _c8_count(session)
        with pytest.raises(S41EventRefusal) as exc:
            session.admit_event(
                case=case_for(False), source=source_for(case_for(False)),
                history_event_refs=(event2["e1_event_id"],),
                event_time=event2["event_time"],
            )
        assert exc.value.code in {"S42_EVENT_TIME_NOT_LATER", "S42_INCOMING_SOURCE_REPLAY"}
        assert len(_a_actions(session)) == before_actions
        assert _c9_count(session) == before_c9
        assert _c8_count(session) == before_c8
        assert session.read_event(event2["e1_event_id"])["status"] == "OK"
    finally:
        session.close()


def _replace_binding_input(binding, mode):
    history = (binding.get("history_sources") or [None])[0]
    if not history:
        return binding
    body = {key: value for key, value in binding.items() if key != "hash"}
    sources = [dict(row) for row in body["generation_sources"]]
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
        sources = [
            replacement if row.get("source_ref") == history["source_ref"] else row
            for row in sources
        ]
    elif mode == "duplicate":
        for index, row in enumerate(sources):
            if row.get("source_ref") == history["source_ref"]:
                sources.insert(index + 1, dict(row))
                break
    else:
        raise AssertionError(mode)
    body["generation_sources"] = sources
    return seal(body)


@pytest.mark.parametrize(
    "mode,detail",
    [
        ("replacement", "S41_GENERATION_CANONICAL_INPUT_REPLACED"),
        ("duplicate", "S41_GENERATION_INPUT_SOURCE_DUPLICATE"),
    ],
)
def test_persisted_s42_input_substitution_refused_warm_cold(mode, detail, tmp_path, monkeypatch):
    import s42.session as session_module
    session = _start(tmp_path)
    try:
        original = session_module.make_event_binding

        def bad_binding(*args, **kwargs):
            return _replace_binding_input(original(*args, **kwargs), mode)

        monkeypatch.setattr(session_module, "make_event_binding", bad_binding)
        with pytest.raises(S42ReadRefusal) as exc:
            _admit(session, share=False, history_ordinals=(1,))
        assert detail in str(exc.value)
        from s41.bindings import binding_episodes as s41_binding_episodes
        first_id = s41_binding_episodes(session)[0]["e1_event_id"]
        bad = binding_episodes(session)[0]
        assert session.read_event(first_id)["status"] == "OK"
        with pytest.raises(S42ReadRefusal):
            session.read_event(bad["e1_event_id"])
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        S42Session.open(tmp_path / "state")


def test_older_source_fault_after_later_restores(tmp_path, monkeypatch):
    import s42.session as session_module
    session = _start(tmp_path)
    try:
        _admit(session, share=False, history_ordinals=(1,))
        _admit(session, share=True, history_ordinals=(1,))
        events = session.read_events()
        before_actions = len(_a_actions(session))
        before_c9 = _c9_count(session)
        before_bindings = len(binding_episodes(session))
        original = session_module.make_history_records

        def bad_records(session_arg, history_bindings, as_of):
            records = original(session_arg, history_bindings, as_of)
            if not records:
                return records
            source = dict(records[0])
            content = dict(source["content"])
            content["prior_access_witness_hash"] = "0" * 64
            return [make_source(
                source_ref=source["source_ref"],
                source_class=source["source_class"],
                actor_id=source["actor_id"],
                branch_id=source["branch_id"],
                as_of=source["as_of"],
                predicate=source["predicate"],
                value=source["value"],
                content=content,
            )]

        monkeypatch.setattr(session_module, "make_history_records", bad_records)
        with pytest.raises(S41EventRefusal) as exc:
            session.admit_event(
                case=case_for(False), source=source_for(case_for(False)),
                history_event_refs=(events[0]["e1_event_id"],),
            )
        assert exc.value.code == "S42_HISTORY_BINDING_INVALID"
        assert len(_a_actions(session)) == before_actions
        assert _c9_count(session) == before_c9
        assert len(binding_episodes(session)) == before_bindings
        monkeypatch.setattr(session_module, "make_history_records", original)
        restored = session.admit_event(
            case=case_for(False), source=source_for(case_for(False)),
            history_event_refs=(events[0]["e1_event_id"],),
        )
        assert restored["status"] == "OK"
        assert session.read_event(events[0]["e1_event_id"])["status"] == "OK"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_wrong_branch_history_source_refused(tmp_path):
    from s41.bindings import binding_episodes as s41_bindings
    from s41.event import history_record_from_prior
    from s41.history import S41HistoryRefusal, validate_history_source

    session = _start(tmp_path)
    try:
        first = s41_bindings(session)[0]
        history = history_record_from_prior(
            session, first_binding=first, as_of=session.clock() + 5
        )
        with pytest.raises(S41HistoryRefusal):
            validate_history_source(
                session, history, first,
                branch_id="WRONG_BRANCH", as_of=session.clock() + 5,
            )
        assert session.read_event(first["e1_event_id"])["status"] == "OK"
    finally:
        session.close()
