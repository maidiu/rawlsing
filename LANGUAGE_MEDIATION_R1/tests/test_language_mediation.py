"""Whole-consumer tests for the TEST_ONLY language-mediation slice.

Every fixture is invented.  The tests exercise the real JoinedSession writer,
C12 episode/world store and R31E expression seam; they do not grant native,
source, human or general translation authority.
"""
from __future__ import annotations

import pytest

from language_mediation import MediatedJoinedSession
from language_mediation import session as session_module
from language_mediation.artifacts import (
    build_native_artifact,
    build_translation_artifact,
    seal_artifact,
)
from language_mediation.atoms import PHRASE_PAIRS
from language_mediation.equivalence import evaluate_pair
from language_mediation.index import LanguageRefusal, build_index
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal

TRIGGER = "What do you say when things get hard?"
NATIVE_SELF = "Uno se arregla."
NATIVE_BENCH = "El banco sigue aquí."


def _build_fixture(state):
    session = MediatedJoinedSession.start(state, perform="omit")
    session.declare_language_competence("A", "es-MX")
    counter_help = session.admit_language_event(
        "A veces hace falta ayuda.", speaker_actor="B")
    counter_alone = session.admit_language_event(
        "Cada quien por su lado.", speaker_actor="B")
    family = session.admit_language_encounter(
        text=NATIVE_SELF,
        concept_id="concept:independence",
        milieu_id="family",
        sense_id="sense:family-self-reliance",
        relation_label="AMBIVALENT",
        atoms=["SELF_RELIANCE_FAMILY"],
        counterexample_event_ids=[counter_help["event"]["event_id"]],
    )
    work = session.admit_language_encounter(
        text="Aquí nos ayudamos.",
        concept_id="concept:independence",
        milieu_id="work",
        sense_id="sense:work-mutual-aid",
        relation_label="AFFIRMED_FOR_OTHERS",
        atoms=["MUTUAL_AID_WORK"],
        counterexample_event_ids=[counter_alone["event"]["event_id"]],
    )
    enabled = session.enable_mediation(trigger_kinds=("SAY",))
    data = {
        "family": family,
        "work": work,
        "counter_help": counter_help,
        "counter_alone": counter_alone,
        "enabled": enabled,
        "family_relation": family["encounter"]["encounter_id"],
        "work_relation": work["encounter"]["encounter_id"],
        "family_receipt": family["encounter"]["access_receipt_id"],
        "work_receipt": work["encounter"]["access_receipt_id"],
        "counter_help_receipt": counter_help["access"]["receipt"]["receipt_id"],
        "counter_alone_receipt": counter_alone["access"]["receipt"]["receipt_id"],
        "family_source": family["event"]["event_id"],
        "work_source": work["event"]["event_id"],
    }
    return session, data


@pytest.fixture
def mediated(tmp_path):
    session, data = _build_fixture(tmp_path / "state")
    try:
        yield session, data
    finally:
        session.close()


def _fresh_session(tmp_path, name="state"):
    session = MediatedJoinedSession.start(tmp_path / name, perform="omit")
    session.declare_language_competence("A", "es-MX")
    return session


def _admit_family(session, **kwargs):
    atoms = kwargs.pop("atoms", ["SELF_RELIANCE_FAMILY"])
    return session.admit_language_encounter(
        text=NATIVE_SELF,
        concept_id="concept:independence",
        milieu_id="family",
        sense_id="sense:family-self-reliance",
        relation_label="AMBIVALENT",
        atoms=atoms,
        **kwargs,
    )


def test_contradictory_histories_feed_the_actual_joined_consumer(mediated):
    session, data = mediated
    assert isinstance(session, JoinedSession)

    index = session.language_index()
    assert index["cache_status"] == "CACHE_VALID"
    assert {row["relation_id"] for row in index["relations"]} == {
        data["family_relation"], data["work_relation"]}
    assert len(index["contradictions_preserved"]) == 1
    contradiction = index["contradictions_preserved"][0]
    assert contradiction["concept_id"] == "concept:independence"
    assert set(contradiction["relation_ids"]) == {
        data["family_relation"], data["work_relation"]}
    assert set(contradiction["milieu_ids"]) == {"family", "work"}

    plan = session.expression_plan(trigger_kind="SAY", text=TRIGGER)
    assert plan.unit["unit_id"] == "SELF_RELIANCE"
    assert plan.supporting_relation_ids == [data["family_relation"]]
    assert set(plan.relation_ids) == {
        data["family_relation"], data["work_relation"]}
    assert plan.readset["contradictions_preserved"][0]["concept_id"] == (
        "concept:independence")

    said = session.say(TRIGGER)
    assert said["admission"]["plan"]["relation_ids"] == plan.relation_ids
    event = session.event(said["admission"]["speech_event_id"])
    lme = event["body"]["lme"]
    assert {row["event_id"] for row in lme["source_event_refs"]} == {
        data["family_source"], data["work_source"]}
    assert set(lme["access_receipt_ids"]) == {
        data["family_receipt"], data["work_receipt"]}
    assert any("labeled English view" in line for line in said["surface"])
    assert session.verify()["ok"] is True


def test_authorized_plan_native_speech_and_english_view_agree(mediated):
    session, _ = mediated
    said = session.say(TRIGGER)
    language = said["language"]
    plan = language["plan"]
    native = language["native_artifact"]
    translation = language["translation_artifact"]
    receipt = language["equivalence"]

    assert plan["unit"]["unit_id"] == "SELF_RELIANCE"
    assert plan["unit"]["native_text"] == native["text"] == NATIVE_SELF
    assert native["atoms"] == translation["atoms"] == plan["authorized_atoms"]
    assert native["plan_hash"] == translation["plan_hash"] == plan["plan_hash"]
    assert receipt["status"] == "ACCEPTED"
    assert all(receipt["checks"].values())
    assert receipt["model_self_judgment_used"] is False

    event_id = said["admission"]["speech_event_id"]
    event = session.event(event_id)
    assert event["body"]["text"] == native["text"]
    assert event["body"]["spans"] == [{
        "language_tag": "es-MX",
        "text": NATIVE_SELF,
        "span_role": "SPOKEN",
    }]
    assert event["body"]["lme"]["native_artifact_hash"] == native["artifact_hash"]
    assert event["body"]["lme"]["translation_artifact_hash"] == (
        translation["artifact_hash"])

    view = session.language_view(event_id, locale="en")
    assert view["status"] == "OK"
    assert view["display_mode"] == "LABELED_ENGLISH"
    assert view["translation_status"] == "AVAILABLE"
    assert view["translation_text"] == translation["text"]
    assert view["source_event_hash"] == event["hash"]
    assert view["native_artifact_hash"] == native["artifact_hash"]
    assert view["translation_artifact_hash"] == translation["artifact_hash"]
    assert view["equivalence"]["plan_hash"] == plan["plan_hash"]
    assert view["source_preserved"] is True
    assert language["product_model_calls"] == 0


def test_cold_reopen_preserves_the_admitted_speech_event(tmp_path):
    state = tmp_path / "cold"
    session, _ = _build_fixture(state)
    try:
        said = session.say(TRIGGER)
        event_id = said["admission"]["speech_event_id"]
        event_hash = said["admission"]["speech_event_hash"]
        plan_hash = said["language"]["plan"]["plan_hash"]
        readset_hash = said["language"]["index_readset_hash"]
        original = session.event(event_id)
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = MediatedJoinedSession.open(state)
    try:
        event = cold.event(event_id)
        assert event is not None
        assert event["hash"] == event_hash
        assert event["body"] == original["body"]
        assert event["body"]["text"] == NATIVE_SELF
        assert event["body"]["lme"]["plan_hash"] == plan_hash
        view = cold.language_view(event_id, locale="en")
        assert view["status"] == "OK"
        assert view["translation_status"] == "AVAILABLE"
        assert view["source_event_hash"] == event_hash
        index = cold.language_index()
        assert index["cache_status"] == "CACHE_VALID"
        assert index["readset_hash"] == readset_hash
        assert cold.status()["multilingual_port"]["bound"] is True
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_access_severance_refuses_dependent_use_and_restoration_works(mediated):
    session, data = mediated
    first = session.say(TRIGGER)
    assert first["strategy"] == "SELF_RELIANCE"
    assert first["candidate"]["speech"] == NATIVE_SELF

    session.revoke_language_access(data["family_receipt"])
    index = session.language_index()
    invalid = {row["relation_id"]: row for row in
               index["invalidated_relations"]}
    assert invalid[data["family_relation"]]["invalid_reason"] == "ACCESS_REVOKED"
    assert [row["relation_id"] for row in index["relations"]] == [
        data["work_relation"]]
    assert index["contradictions_preserved"] == []
    assert index["cache_status"] == "CACHE_INVALID"

    refused = session.say(TRIGGER)
    assert refused["strategy"] == "SAFE_GREETING"
    assert refused["candidate"]["speech"] == NATIVE_BENCH
    assert refused["language"]["source_dependent_refused"] is True
    assert refused["language"]["fallback"] is True
    assert refused["language"]["fallback_reason"] == (
        "SOURCE_DEPENDENT_UNIT_UNAVAILABLE")
    assert data["family_relation"] in refused["language"]["plan"]["readset"][
        "invalidated_relation_ids"]
    assert refused["language"]["plan"]["supporting_relation_ids"] == []

    session.restore_language_access(data["family_receipt"])
    restored_index = session.language_index()
    assert {row["relation_id"] for row in restored_index["relations"]} == {
        data["family_relation"], data["work_relation"]}
    assert restored_index["invalidated_relations"] == []
    assert restored_index["cache_status"] == "CACHE_VALID"

    restored = session.say(TRIGGER)
    assert restored["strategy"] == "SELF_RELIANCE"
    assert restored["candidate"]["speech"] == NATIVE_SELF
    assert restored["language"]["fallback"] is False
    assert session.verify()["ok"] is True


def test_counterexample_severance_invalidates_the_dependent_relation(mediated):
    session, data = mediated
    session.revoke_language_access(data["counter_help_receipt"])

    index = session.language_index()
    invalid = {row["relation_id"]: row for row in
               index["invalidated_relations"]}
    assert invalid[data["family_relation"]]["invalid_reason"] == (
        "COUNTEREXAMPLE_NOT_ACCESSIBLE")
    assert [row["relation_id"] for row in index["relations"]] == [
        data["work_relation"]]

    refused = session.say(TRIGGER)
    assert refused["strategy"] == "SAFE_GREETING"
    assert refused["candidate"]["speech"] == NATIVE_BENCH

    session.restore_language_access(data["counter_help_receipt"])
    restored = session.say(TRIGGER)
    assert restored["strategy"] == "SELF_RELIANCE"
    assert restored["candidate"]["speech"] == NATIVE_SELF
    assert session.verify()["ok"] is True


def test_wrong_access_branch_is_refused(tmp_path):
    session = _fresh_session(tmp_path)
    try:
        _admit_family(session, access_declared_branch="other-branch")
        with pytest.raises(LanguageRefusal) as exc:
            build_index(session)
        assert exc.value.code == "ACCESS_BRANCH_MISMATCH"
    finally:
        session.close()


def test_wrong_access_hash_is_refused(tmp_path):
    session = _fresh_session(tmp_path)
    try:
        _admit_family(session, access_declared_hash="0" * 64)
        with pytest.raises(LanguageRefusal) as exc:
            build_index(session)
        assert exc.value.code == "ACCESS_HASH_MISMATCH"
    finally:
        session.close()


def test_wrong_source_hash_is_refused(tmp_path):
    session = _fresh_session(tmp_path)
    try:
        encounter = _admit_family(session)
        body = dict(encounter["encounter"])
        body["source_event_hash"] = "0" * 64
        body["encounter_id"] = "LME_ENC_WRONG_SOURCE_HASH"
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_ENCOUNTER",
            session.clock(), body)
        with pytest.raises(LanguageRefusal) as exc:
            build_index(session)
        assert exc.value.code == "SOURCE_EVENT_HASH_MISMATCH"
    finally:
        session.close()


def test_foreign_source_branch_is_refused(tmp_path):
    session = _fresh_session(tmp_path)
    try:
        encounter = _admit_family(session)
        body = dict(encounter["encounter"])
        body["branch_id"] = "other-branch"
        body["encounter_id"] = "LME_ENC_FOREIGN_BRANCH"
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_ENCOUNTER",
            session.clock(), body)
        with pytest.raises(LanguageRefusal) as exc:
            build_index(session)
        assert exc.value.code == "SOURCE_BRANCH_MISMATCH"
    finally:
        session.close()


def test_unknown_access_receipt_severance_and_restoration_are_refused(mediated):
    session, _ = mediated
    with pytest.raises(LanguageRefusal) as exc:
        session.revoke_language_access("LME_ACCESS_missing")
    assert exc.value.code == "ACCESS_RECEIPT_UNKNOWN"
    with pytest.raises(LanguageRefusal) as exc:
        session.restore_language_access("LME_ACCESS_missing")
    assert exc.value.code == "ACCESS_RECEIPT_UNKNOWN"


def test_unauthorized_meaning_is_refused_even_when_artifacts_agree(mediated):
    session, _ = mediated
    plan = session.expression_plan(trigger_kind="SAY", text=TRIGGER)

    stronger_atoms = ["SELF_RELIANCE_FAMILY", "CERTAINTY"]
    native = build_native_artifact(plan, atoms=stronger_atoms)
    translation = build_translation_artifact(
        plan, native, atoms=stronger_atoms)
    assert native["atoms"] == translation["atoms"]
    receipt = evaluate_pair(plan, native, translation)
    assert receipt["status"] == "REJECTED"
    assert "UNAUTHORIZED_MEANING_STRENGTHENED" in receipt["codes"]
    assert receipt["checks"]["no_unauthorized_strengthening"] is False

    substituted = build_native_artifact(
        plan,
        text=PHRASE_PAIRS["pair_mutual_aid"]["native_text"],
        atoms=["MUTUAL_AID_WORK"],
    )
    substituted_translation = build_translation_artifact(
        plan,
        substituted,
        text=PHRASE_PAIRS["pair_mutual_aid"]["target_text"],
        atoms=["MUTUAL_AID_WORK"],
    )
    substituted_receipt = evaluate_pair(
        plan, substituted, substituted_translation)
    assert substituted_receipt["status"] == "REJECTED"
    assert "UNAUTHORIZED_MEANING_STRENGTHENED" in substituted_receipt["codes"]


def test_resealed_artifacts_cannot_drop_plan_source_bindings(mediated):
    session, data = mediated
    plan = session.expression_plan(trigger_kind="SAY", text=TRIGGER)
    native = build_native_artifact(plan)
    body = {key: value for key, value in native.items()
            if key != "artifact_hash"}
    body["source_relation_ids"] = ["LME_ENC_not_the_plan"]
    resealed = seal_artifact(body)
    translation = build_translation_artifact(plan, resealed)
    receipt = evaluate_pair(plan, resealed, translation)
    assert receipt["status"] == "REJECTED"
    assert "ARTIFACT_PLAN_BINDING_MISMATCH" in receipt["codes"]
    assert data["family_relation"] not in resealed["source_relation_ids"]


def test_joined_consumer_refuses_matching_stronger_pair_before_admission(
        mediated, monkeypatch):
    session, _ = mediated
    original_native = session_module.build_native_artifact
    original_translation = session_module.build_translation_artifact

    def stronger_native(plan, **kwargs):
        atoms = sorted(set(plan.authorized_atoms) | {"CERTAINTY"})
        return original_native(plan, atoms=atoms, **kwargs)

    def matching_translation(plan, native, **kwargs):
        return original_translation(
            plan, native, atoms=native["atoms"], **kwargs)

    monkeypatch.setattr(
        session_module, "build_native_artifact", stronger_native)
    monkeypatch.setattr(
        session_module, "build_translation_artifact", matching_translation)
    admissions_before = [row for row in session.episodes()
                         if row["kind"] == "EXPRESSION_ADMISSION"]
    events_before = len(session.events())

    with pytest.raises(SessionRefusal) as exc:
        session.say(TRIGGER)
    assert exc.value.code == "LANGUAGE_EQUIVALENCE_REJECTED"
    admissions_after = [row for row in session.episodes()
                        if row["kind"] == "EXPRESSION_ADMISSION"]
    assert admissions_after == admissions_before
    new_events = session.events()[events_before:]
    assert not any(row.get("body", {}).get("lme") for row in new_events)


def test_optional_translation_failure_preserves_admitted_native_speech(mediated):
    session, _ = mediated
    said = session.say(TRIGGER)
    event_id = said["admission"]["speech_event_id"]
    before = session.event(event_id)

    failed = session.language_view(
        event_id, locale="en", fail_translation=True)
    assert failed["status"] == "OK"
    assert failed["display_mode"] == "TRANSLATION_UNAVAILABLE"
    assert failed["translation_status"] == "TRANSLATION_UNAVAILABLE"
    assert failed["translation_failure"] == "EXPLICIT_DISPLAY_FAILURE"
    assert failed["source_text"] == NATIVE_SELF
    assert failed["source_preserved"] is True
    assert "translation_text" not in failed
    assert session.event(event_id)["hash"] == before["hash"]

    available = session.language_view(event_id, locale="en")
    assert available["translation_status"] == "AVAILABLE"
    assert available["translation_text"] == (
        said["language"]["translation_artifact"]["text"])


def test_locale_and_attention_change_presentation_only(mediated):
    session, _ = mediated
    said = session.say(TRIGGER)
    event_id = said["admission"]["speech_event_id"]
    event_hash = said["admission"]["speech_event_hash"]
    plan_hash = said["language"]["plan"]["plan_hash"]
    admission_id = said["admission"]["admission_id"]
    index_hash = session.language_index()["index_hash"]
    events_before = session.events()

    session.set_display_locale("es")
    source_view = session.language_view(event_id)
    assert source_view["locale"] == "es"
    assert source_view["display_mode"] == "SOURCE_ORIGINAL"
    assert source_view["translation_status"] == "NOT_REQUESTED"
    assert source_view["locale_changed_actor"] is False

    session.set_display_locale("dual")
    dual_view = session.language_view(event_id)
    assert dual_view["display_mode"] == "DUAL"
    assert dual_view["translation_status"] == "AVAILABLE"

    session.set_display_locale("en")
    attentive = session.language_view(
        event_id, locale="en", attention="distracted")
    assert attentive["attention"] == "distracted"
    assert attentive["attention_changed_actor"] is False
    assert attentive["plan_hash"] == plan_hash
    assert attentive["source_event_hash"] == event_hash
    assert attentive["translation_status"] == "AVAILABLE"

    assert session.event(event_id)["hash"] == event_hash
    assert session.events() == events_before
    assert session.language_index()["index_hash"] == index_hash
    assert said["admission"]["admission_id"] == admission_id


def test_tampered_projection_is_unresolved_and_source_is_preserved(mediated):
    session, _ = mediated
    said = session.say(TRIGGER)
    event_id = said["admission"]["speech_event_id"]
    before = session.event(event_id)
    real = session._projection(event_id)
    assert real is not None

    fake_text = dict(real)
    fake_text["text"] = "A different meaning."
    session.product._append_episode(
        session.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
        session.clock(), fake_text)
    view = session.language_view(event_id, locale="en")
    assert view["status"] == "UNRESOLVED"
    assert view["translation_status"] == "PROJECTION_TEXT_MISMATCH"
    assert view["source_text"] == NATIVE_SELF
    assert view["source_preserved"] is True

    fake_hash = dict(real)
    fake_hash["source_event_hash"] = "0" * 64
    session.product._append_episode(
        session.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
        session.clock(), fake_hash)
    view = session.language_view(event_id, locale="en")
    assert view["status"] == "UNRESOLVED"
    assert view["translation_status"] == "PROJECTION_SOURCE_HASH_MISMATCH"
    assert session.event(event_id)["hash"] == before["hash"]


@pytest.mark.parametrize("overrides", [
    {"atoms": ["MUTUAL_AID_WORK"]},
    {"language_tag": "fr-FR"},
])
def test_relation_must_match_unit_atoms_and_language(tmp_path, overrides):
    session = _fresh_session(tmp_path / str(len(str(overrides))))
    try:
        _admit_family(session, **overrides)
        session.enable_mediation(trigger_kinds=("SAY",))
        index = session.language_index()
        assert len(index["relations"]) == 1
        plan = session.expression_plan(trigger_kind="SAY", text=TRIGGER)
        assert plan.unit["unit_id"] == "SAFE_BENCH"
        assert plan.fallback is True
        assert plan.fallback_reason == "SOURCE_DEPENDENT_UNIT_UNAVAILABLE"
        assert plan.supporting_relation_ids == []
        said = session.say(TRIGGER)
        assert said["strategy"] == "SAFE_GREETING"
        assert said["candidate"]["speech"] == NATIVE_BENCH
    finally:
        session.close()


def test_existing_template_baseline_remains_intact(tmp_path):
    session = MediatedJoinedSession.start(tmp_path / "baseline", perform="omit")
    try:
        result = session.say("Hello. I just moved in.")
        assert result["strategy"] == "RECIPROCATE"
        assert result["language"] is None
        event = session.event(result["admission"]["speech_event_id"])
        assert "lme" not in event["body"]
        status = session.status()
        assert status["multilingual_port"]["bound"] is False
        assert status["expression_port"] == "R31E_EXPRESSION_PORT@1"
        assert not any(
            row["kind"].startswith("LANGUAGE_") for row in session.episodes())
        assert session.verify()["ok"] is True
    finally:
        session.close()
