"""Focused S43 historical-language integration tests over one S42 person."""
from __future__ import annotations

import pytest

from s43.bootstrap import install

install()

from language_mediation.artifacts import (  # noqa: E402
    build_native_artifact,
    build_translation_artifact,
)
from language_mediation.equivalence import evaluate_pair  # noqa: E402
from language_mediation.index import LanguageRefusal  # noqa: E402
from language_mediation.plan import competent_languages  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402
from s43.planner import compile_historical_plan  # noqa: E402
from s43.registry import ATOMS, PAIRS  # noqa: E402
from s43.session import S43Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s39.sources import context_records  # noqa: E402


def _count_b_speech(session) -> int:
    return len([
        event for event in session.events()
        if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"
    ])


def _seed(session) -> dict:
    if "es-MX" not in competent_languages(session, "A"):
        session.declare_language_competence("A", "es-MX")
    family_counter = session.admit_language_event(
        "Cada quien por su lado.", speaker_actor="B"
    )
    work_counter = session.admit_language_event(
        "Aquí no se pide, se hace.", speaker_actor="B"
    )
    family = session.admit_language_encounter(
        text="¿Puedo usar la herramienta?",
        concept_id="concept:request-tool",
        milieu_id="family",
        sense_id="sense:family-request",
        relation_label="CONTESTED",
        atoms=["TOOL_REQUEST_WORKSHOP"],
        counterexample_event_ids=[family_counter["event"]["event_id"]],
    )
    work = session.admit_language_encounter(
        text="¿Puedo usar la herramienta?",
        concept_id="concept:request-tool",
        milieu_id="workshop",
        sense_id="sense:workshop-request",
        relation_label="AFFIRMED",
        atoms=["TOOL_REQUEST_WORKSHOP"],
        counterexample_event_ids=[work_counter["event"]["event_id"]],
    )
    refusal_family = session.admit_language_encounter(
        text="No, ahora no.",
        concept_id="concept:refusal",
        milieu_id="family",
        sense_id="sense:family-refusal",
        relation_label="AFFIRMED",
        atoms=["EXPLICIT_REFUSAL_NOW"],
    )
    refusal_work = session.admit_language_encounter(
        text="No, ahora no.",
        concept_id="concept:refusal",
        milieu_id="workshop",
        sense_id="sense:workshop-refusal",
        relation_label="AFFIRMED",
        atoms=["EXPLICIT_REFUSAL_NOW"],
    )
    bench = session.admit_language_encounter(
        text="El banco sigue aquí.",
        concept_id="concept:bench",
        milieu_id="public",
        sense_id="sense:bench-present",
        relation_label="AFFIRMED",
        atoms=["BENCH_PRESENT"],
    )
    return {
        "family": family,
        "work": work,
        "refusal_family": refusal_family,
        "refusal_work": refusal_work,
        "bench": bench,
        "family_counter": family_counter,
        "work_counter": work_counter,
        "family_relation": family["encounter"]["encounter_id"],
        "work_relation": work["encounter"]["encounter_id"],
        "family_source": family["event"]["event_id"],
        "work_source": work["event"]["event_id"],
        "family_receipt": family["encounter"]["access_receipt_id"],
        "work_receipt": work["encounter"]["access_receipt_id"],
        "family_counter_receipt": family_counter["access"]["receipt"]["receipt_id"],
        "work_counter_receipt": work_counter["access"]["receipt"]["receipt_id"],
    }


def _open_with_histories(tmp_path, name="state"):
    state = tmp_path / name
    case = case_for(True)
    session = S43Session.start(state, case=case, source=source_for(case))
    data = _seed(session)
    session.close()
    return state, data


def _admit(session, *, context, history_ordinal=1, share=True,
           source_records=None):
    events = session.read_events()
    return session.admit_event(
        language_context={"milieu_id": context},
        case=case_for(share),
        source=source_for(case_for(share)),
        history_event_refs=(events[history_ordinal - 1]["e1_event_id"],),
        source_records=source_records,
    )


def test_two_context_histories_cold_reopen_and_locale_view(tmp_path):
    state, data = _open_with_histories(tmp_path)
    cold = S43Session.open(state)
    try:
        before_b = _count_b_speech(cold)
        second = _admit(cold, context="family")
        second_read = cold.read_s43_event(second["event"]["e1_event_id"])
        second_s43 = second_read["s43"]
        assert second["status"] == "OK"
        assert second["event"]["selected_option"] == "REQUEST_TOOL"
        assert second["event"]["attempt_status"] == "ADMITTED"
        assert second["event"]["language"]["native_text"] == "¿Puedo usar la herramienta?"
        assert second["event"]["language"]["translation_text"] == "May I use the tool?"
        assert second["event"]["c9"]["target_branch"] == "NO_CHANGE"
        assert second["event"]["c9"]["target_reason"] == "NO_PROPOSAL"
        assert second["event"]["c9"]["target_proposals"] == []
        assert data["family_relation"] in second_s43["selected_relation_ids"]
        assert data["work_relation"] in second_s43["contrary_relation_ids"]
        assert second_s43["contradictions"]
        family_relation = next(
            row for row in second_s43["selected_relations"]
            if row["relation_id"] == data["family_relation"]
        )
        work_relation = next(
            row for row in second_s43["contrary_relations"]
            if row["relation_id"] == data["work_relation"]
        )
        assert family_relation["relation_label"] == "CONTESTED"
        assert family_relation["epistemic"] == "TEST_ONLY_SOURCE_INDEX"
        assert family_relation["source_grade"] == "TEST_ONLY_INVENTED_LANGUAGE_EVENT"
        assert work_relation["relation_label"] == "AFFIRMED"
        assert second_s43["context"] == {"milieu_id": "family"}
        assert second_s43["private_generation_sources_in_plan"] is False
        assert second_s43["currently_available"] is True
        assert set(second_s43["source_grades"]) >= {
            data["family_source"], data["work_source"]
        }
        assert _count_b_speech(cold) == before_b
        event_hash = second["event"]["e1_event_hash"]
        event2_hash = second["event"]["action_event_hash"]
        cold.set_display_locale("es")
        view = cold.language_view(second["event"]["action_event_id"], locale="en")
        assert view["display_mode"] == "LABELED_ENGLISH"
        assert view["translation_text"] == "May I use the tool?"
        assert view["source_event_hash"] == event2_hash
        assert cold.event(second["event"]["action_event_id"])["hash"] == event2_hash
        assert cold.read_event(second["event"]["e1_event_id"])["e1_event_hash"] == event_hash
    finally:
        cold.close()

    cold = S43Session.open(state)
    try:
        third = _admit(cold, context="workshop", share=False)
        third_s43 = cold.read_s43_event(third["event"]["e1_event_id"])["s43"]
        second_s43 = cold.read_s43_event(
            cold.read_events()[1]["e1_event_id"]
        )["s43"]
        assert third["event"]["selected_option"] == "REQUEST_TOOL"
        assert third["event"]["language"]["native_text"] == "¿Puedo usar la herramienta?"
        assert data["work_relation"] in third_s43["selected_relation_ids"]
        assert data["family_relation"] in third_s43["contrary_relation_ids"]
        assert third_s43["repertoire_hash"] != second_s43["repertoire_hash"]
        assert third["event"]["language"]["plan_hash"] != (
            cold.read_event(cold.read_events()[1]["e1_event_id"])["language"]["plan_hash"]
        )
        assert third["event"]["language"]["source_event_id"] == data["work_source"]
        assert cold.read_event(cold.read_events()[1]["e1_event_id"])[
            "language"
        ]["source_event_id"] == data["family_source"]
        assert cold.verify()["ok"] is True
    finally:
        cold.close()

    cold = S43Session.open(state)
    try:
        fourth = _admit(cold, context="family")
        fourth_s43 = cold.read_s43_event(fourth["event"]["e1_event_id"])["s43"]
        second = cold.read_event(cold.read_events()[1]["e1_event_id"])
        assert fourth["status"] == "OK"
        assert fourth["event"]["language"]["source_event_id"] == data["family_source"]
        assert fourth_s43["selected_relation_ids"] == cold.read_s43_event(
            second["e1_event_id"]
        )["s43"]["selected_relation_ids"]
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_source_revocation_refuses_without_replacement_then_restores(tmp_path):
    state, data = _open_with_histories(tmp_path)
    session = S43Session.open(state)
    try:
        second = _admit(session, context="family")
        source_id = second["event"]["language"]["source_event_id"]
        receipt_id = second["event"]["language"]["access_receipt_id"]
        second_hash = second["event"]["action_event_hash"]
        second_s43 = session.read_s43_event(second["event"]["e1_event_id"])["s43"]
        before_b = _count_b_speech(session)
        before_clock = session.clock()
        assert session.language_index()["cache_status"] == "CACHE_VALID"
        session.revoke_language_access(receipt_id, reason="TEST_ONLY_SEVERANCE")
        assert session.clock() == before_clock
        assert session.language_index()["cache_status"] == "CACHE_INVALID"
        bad = _admit(session, context="family")
        assert bad["event"]["attempt_status"] == "DENIED"
        assert bad["event"]["performed"] is False
        assert bad["event"].get("language") is None
        assert session.read_s43_event(bad["event"]["e1_event_id"])["s43_refusal"] == (
            "S43_SOURCE_BOUND_REFUSAL:S43_REQUIRED_SOURCE_UNAVAILABLE"
        )
        assert _count_b_speech(session) == before_b
        assert session.event(second["event"]["action_event_id"])["hash"] == second_hash
        assert session.read_s43_event(
            second["event"]["e1_event_id"]
        )["s43"]["currently_available"] is False
        attempt = binding_episodes(session)[-1]["attempt"]
        assert attempt["reason"] == (
            "S43_SOURCE_BOUND_REFUSAL:S43_REQUIRED_SOURCE_UNAVAILABLE"
        )
        session.restore_language_access(receipt_id, reason="TEST_ONLY_RESTORE")
        restored = _admit(session, context="family")
        restored_s43 = session.read_s43_event(
            restored["event"]["e1_event_id"]
        )["s43"]
        assert restored["event"]["attempt_status"] == "ADMITTED"
        assert restored["event"]["language"]["source_event_id"] == source_id
        assert restored_s43["selected_relation_ids"] == second_s43[
            "selected_relation_ids"
        ]
        assert restored_s43["repertoire_hash"] == second_s43["repertoire_hash"]
        assert restored_s43["currently_available"] is True
        assert session.language_index()["cache_status"] == "CACHE_VALID"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_contrary_source_withdrawal_changes_readset_and_preserves_other(tmp_path):
    state, data = _open_with_histories(tmp_path)
    session = S43Session.open(state)
    try:
        session.revoke_language_access(
            data["family_counter_receipt"], reason="TEST_ONLY_CONTRARY"
        )
        index = session.language_index()
        assert data["family_relation"] not in {
            row["relation_id"] for row in index["relations"]
        }
        assert data["work_relation"] in {
            row["relation_id"] for row in index["relations"]
        }
        work = _admit(session, context="workshop")
        work_s43 = session.read_s43_event(work["event"]["e1_event_id"])["s43"]
        assert work["event"]["attempt_status"] == "ADMITTED"
        assert data["work_relation"] in work_s43["selected_relation_ids"]
        assert data["family_relation"] in work_s43["invalidated_relation_ids"]
        refused = _admit(session, context="family")
        assert refused["event"]["attempt_status"] == "DENIED"
        session.restore_language_access(
            data["family_counter_receipt"], reason="TEST_ONLY_RESTORE_CONTRARY"
        )
        restored = _admit(session, context="family")
        restored_s43 = session.read_s43_event(
            restored["event"]["e1_event_id"]
        )["s43"]
        assert restored["event"]["attempt_status"] == "ADMITTED"
        assert data["family_relation"] in restored_s43["selected_relation_ids"]
        assert data["work_relation"] in restored_s43["contrary_relation_ids"]
    finally:
        session.close()


def test_explicit_refusal_end_to_end_uses_encountered_source(tmp_path):
    state = tmp_path / "refusal"
    case = case_for(False)
    records = context_records(
        actor_id="TEST_ONLY_BP1_R26V_ACTOR_A",
        branch_id="first_session",
        as_of=1,
        prior_b_refusal=True,
    )
    session = S43Session.start(
        state, case=case, source=source_for(case), source_records=records
    )
    try:
        if "es-MX" not in competent_languages(session, "A"):
            session.declare_language_competence("A", "es-MX")
        encounter = session.admit_language_encounter(
            text="No, ahora no.",
            concept_id="concept:refusal",
            milieu_id="family",
            sense_id="sense:family-refusal",
            relation_label="AFFIRMED",
            atoms=["EXPLICIT_REFUSAL_NOW"],
        )
        before_b = _count_b_speech(session)
        session.close()
        session = S43Session.open(state)
        second = session.admit_event(
            language_context={"milieu_id": "family"},
            case=case_for(False),
            source=source_for(case_for(False)),
            history_event_refs=(session.read_events()[0]["e1_event_id"],),
            source_records=[],
        )
        read = session.read_s43_event(second["event"]["e1_event_id"])
        assert second["event"]["selected_option"] == "EXPLICIT_REFUSAL"
        assert second["event"]["attempt_status"] == "ADMITTED"
        assert second["event"]["language"]["native_text"] == "No, ahora no."
        assert second["event"]["language"]["translation_text"] == "No, not now."
        assert encounter["encounter"]["encounter_id"] in read["s43"][
            "selected_relation_ids"
        ]
        assert _count_b_speech(session) == before_b
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_ordinary_language_plan_uses_encountered_bench(tmp_path):
    state, data = _open_with_histories(tmp_path)
    session = S43Session.open(state)
    try:
        index = session.language_index()
        plan, repertoire = compile_historical_plan(
            session,
            intent="ORDINARY_GREETING",
            context={"milieu_id": "public"},
            contract={},
            index=index,
        )
        native = build_native_artifact(plan)
        translation = build_translation_artifact(plan, native)
        receipt = evaluate_pair(
            plan, native, translation, pairs=PAIRS, atom_universe=ATOMS
        )
        assert native["text"] == "El banco sigue aquí."
        assert translation["text"] == "The bench is still here."
        assert receipt["status"] == "ACCEPTED"
        assert data["bench"]["encounter"]["encounter_id"] in (
            repertoire["selected_relation_ids"]
        )
    finally:
        session.close()


def test_missing_competence_refuses_without_fake_speech(tmp_path, monkeypatch):
    import s43.planner as planner
    state, _ = _open_with_histories(tmp_path)
    session = S43Session.open(state)
    try:
        before_b = _count_b_speech(session)
        monkeypatch.setattr(planner, "competent_languages", lambda *args: set())
        result = _admit(session, context="family")
        assert result["event"]["attempt_status"] == "DENIED"
        assert result["event"]["performed"] is False
        attempt = binding_episodes(session)[-1]["attempt"]
        assert attempt["reason"] == (
            "S43_SOURCE_BOUND_REFUSAL:S43_LANGUAGE_COMPETENCE_MISSING"
        )
        assert _count_b_speech(session) == before_b
    finally:
        session.close()


@pytest.mark.parametrize(
    "declared_branch,declared_hash,code",
    [
        ("other-branch", None, "ACCESS_BRANCH_MISMATCH"),
        (None, "0" * 64, "ACCESS_HASH_MISMATCH"),
    ],
)
def test_wrong_access_branch_or_hash_is_refused(
    tmp_path, declared_branch, declared_hash, code
):
    state = tmp_path / "wrong-access"
    case = case_for(True)
    session = S43Session.start(state, case=case, source=source_for(case))
    try:
        session.admit_language_encounter(
            text="¿Puedo usar la herramienta?",
            concept_id="concept:request-tool",
            milieu_id="family",
            sense_id="sense:family-request",
            relation_label="AFFIRMED",
            atoms=["TOOL_REQUEST_WORKSHOP"],
            access_declared_branch=declared_branch,
            access_declared_hash=declared_hash,
        )
        with pytest.raises(LanguageRefusal) as exc:
            session.language_index()
        assert exc.value.code == code
    finally:
        session.close()


def test_wrong_source_hash_and_branch_are_refused(tmp_path):
    state = tmp_path / "wrong-source"
    case = case_for(True)
    session = S43Session.start(state, case=case, source=source_for(case))
    try:
        encounter = session.admit_language_encounter(
            text="¿Puedo usar la herramienta?",
            concept_id="concept:request-tool",
            milieu_id="family",
            sense_id="sense:family-request",
            relation_label="AFFIRMED",
            atoms=["TOOL_REQUEST_WORKSHOP"],
        )
        body = dict(encounter["encounter"])
        body["source_event_hash"] = "0" * 64
        body["encounter_id"] = "S43_TAMPERED_HASH"
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_ENCOUNTER",
            session.clock(), body,
        )
        with pytest.raises(LanguageRefusal) as exc:
            session.language_index()
        assert exc.value.code == "SOURCE_EVENT_HASH_MISMATCH"
    finally:
        session.close()

    state = tmp_path / "wrong-source-branch"
    case = case_for(True)
    session = S43Session.start(state, case=case, source=source_for(case))
    try:
        encounter = session.admit_language_encounter(
            text="¿Puedo usar la herramienta?",
            concept_id="concept:request-tool",
            milieu_id="family",
            sense_id="sense:family-request",
            relation_label="AFFIRMED",
            atoms=["TOOL_REQUEST_WORKSHOP"],
        )
        body = dict(encounter["encounter"])
        body["branch_id"] = "other-branch"
        body["encounter_id"] = "S43_TAMPERED_BRANCH"
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_ENCOUNTER",
            session.clock(), body,
        )
        with pytest.raises(LanguageRefusal) as exc:
            session.language_index()
        assert exc.value.code == "SOURCE_BRANCH_MISMATCH"
    finally:
        session.close()
