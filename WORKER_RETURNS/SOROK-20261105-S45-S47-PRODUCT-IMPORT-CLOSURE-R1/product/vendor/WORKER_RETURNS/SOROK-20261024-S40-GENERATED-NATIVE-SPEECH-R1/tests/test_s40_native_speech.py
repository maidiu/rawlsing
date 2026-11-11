"""S40 generated request/refusal own native speech and English view."""
from __future__ import annotations

import json

import pytest

from s40.bootstrap import install

install()

from s40.language import (  # noqa: E402
    S40_ATOMS,
    S40_PAIRS,
    S40_UNITS,
)
from s40.session import S40GeneratedSession  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from language_mediation.artifacts import (  # noqa: E402
    build_native_artifact,
    build_translation_artifact,
)
from language_mediation.equivalence import evaluate_pair  # noqa: E402
from language_mediation.plan import ExpressionPlan  # noqa: E402


def _context_for(tmp_path, share: bool, **flags):
    from s39.producer import GeneratedProducer

    case = case_for(share)
    source = source_for(case)
    probe = GeneratedProducer(tmp_path / "probe", case=case, source=source)
    try:
        probe.stage_m35()
        records = context_records(
            actor_id=probe.occurrence.actor_id,
            branch_id="first_session",
            as_of=probe.as_of,
            **flags,
        )
    finally:
        probe.close()
    return case, source, records


def test_generated_request_has_own_native_speech_and_english_view(tmp_path):
    case = case_for(True)
    session = S40GeneratedSession.start(
        tmp_path / "request", case=case, source=source_for(case)
    )
    try:
        s40 = session.read_s40()
        assert s40["selected_option"] == "REQUEST_TOOL"
        assert s40["language_status"] == "ACCEPTED"
        assert s40["native_text"] == "¿Puedo usar la herramienta?"
        assert s40["translation_text"] == "May I use the tool?"
        assert s40["language_tag"] == "es-MX"
        assert s40["target_language_tag"] == "en"
        assert s40["s36"]["outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
        assert s40["s36"]["response_kind"] == "REQUEST_TOOL"
        assert s40["s36"]["target_branch"] == "NO_CHANGE"
        assert s40["s36"]["target_reason"] == "NO_PROPOSAL"
        assert s40["s36"]["target_proposals"] == []
        assert s40["s36"]["target_state_rows"] == 0
        event = session.event(s40["speech_event_id"])
        assert event["kind"] == "SPEECH"
        assert event["body"]["text"] == "¿Puedo usar la herramienta?"
        assert event["body"]["spans"][0]["language_tag"] == "es-MX"
        view = session.language_view(s40["speech_event_id"], locale="en")
        assert view["status"] == "OK"
        assert view["display_mode"] == "LABELED_ENGLISH"
        assert view["translation_text"] == "May I use the tool?"
        assert view["plan_hash"] == s40["plan_hash"]
        assert view["equivalence"]["status"] == "ACCEPTED"
        generation = session.read_generation()["generation"]
        assert any(
            row["predicate"] == "AVOID_DEBT"
            for row in generation["contrary_reasons"]
        )
        lme_refs = event["body"]["lme"]["source_event_refs"]
        assert not set(generation["source_refs"]).intersection(
            {row.get("event_id", "") for row in lme_refs}
        )
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = S40GeneratedSession.open(tmp_path / "request")
    try:
        cold_s40 = cold.read_s40()
        assert cold_s40["speech_event_hash"] == s40["speech_event_hash"]
        assert cold_s40["native_text"] == s40["native_text"]
        assert cold_s40["translation_text"] == s40["translation_text"]
        assert cold_s40["plan_hash"] == s40["plan_hash"]
        assert cold.language_view(cold_s40["speech_event_id"], locale="en")[
            "translation_text"
        ] == "May I use the tool?"
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_generated_explicit_refusal_has_own_native_speech(tmp_path):
    case, source, records = _context_for(tmp_path, True, prior_b_refusal=True)
    session = S40GeneratedSession.start(
        tmp_path / "refusal", case=case, source=source, source_records=records
    )
    try:
        s40 = session.read_s40()
        assert s40["selected_option"] == "EXPLICIT_REFUSAL"
        assert s40["language_status"] == "ACCEPTED"
        assert s40["native_text"] == "No, ahora no."
        assert s40["translation_text"] == "No, not now."
        assert s40["s36"]["outcome"] == "OBSERVED_CURRENT_REFUSAL"
        assert s40["s36"]["response_kind"] == "EXPLICIT_REFUSAL"
        assert s40["s36"]["target_branch"] == "NO_CHANGE"
        assert s40["s36"]["target_proposals"] == []
        assert session.language_view(
            s40["speech_event_id"], locale="en"
        )["translation_text"] == "No, not now."
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = S40GeneratedSession.open(tmp_path / "refusal")
    try:
        assert cold.read_s40()["native_text"] == "No, ahora no."
        assert cold.read_s40()["translation_text"] == "No, not now."
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_unauthorized_stronger_meaning_fails_against_unchanged_plan(tmp_path):
    unit = S40_UNITS["REQUEST_TOOL"]
    pair = S40_PAIRS[unit["pair_id"]]
    plan = ExpressionPlan(
        schema="LME_ACTOR_EXPRESSION_PLAN@1",
        grade="TEST_ONLY_S40_TEST",
        native=False,
        actor_id="A",
        branch_id="first_session",
        unit=unit,
        pair=pair,
        intent="REQUEST_TOOL",
        authorized_atoms=sorted(pair["atoms"]),
        relation_ids=[],
        supporting_relation_ids=[],
        readset={
            "index_hash": "x",
            "index_readset_hash": "x",
            "source_event_refs": [],
            "access_receipt_ids": [],
            "counterexamples": [],
            "contradictions_preserved": [],
            "invalidated_relation_ids": [],
        },
        contract_hash="contract",
        trigger_kind="GENERATED_ATTEMPT",
        trigger_text="",
        fallback=False,
        fallback_reason="",
        requested_unit_id=unit["unit_id"],
    )
    plan._seal()
    native = build_native_artifact(
        plan, atoms=["TOOL_REQUEST_WORKSHOP", "EXPLICIT_REFUSAL_NOW"]
    )
    translation = build_translation_artifact(
        plan, native, atoms=["TOOL_REQUEST_WORKSHOP", "EXPLICIT_REFUSAL_NOW"]
    )
    receipt = evaluate_pair(
        plan, native, translation, pairs=S40_PAIRS, atom_universe=S40_ATOMS
    )
    assert receipt["status"] == "REJECTED"
    assert "UNAUTHORIZED_MEANING_STRENGTHENED" in receipt["codes"]
