"""Focused S44 sampled-root generation and actual-consumer tests."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from s44.bootstrap import install

install()

from s44.bundle import default_bundle, normalize_bundle  # noqa: E402
from s44.errors import S44Refusal  # noqa: E402
from s44.root import generate_root  # noqa: E402
from s44.session import ROOT_FILE, S44Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _bundle(seed: str = "00" * 32) -> dict:
    return default_bundle(root_seed=seed)


def _reverse_candidates(bundle: dict) -> dict:
    body = deepcopy(bundle)
    for rule in body["rules"].values():
        if isinstance(rule.get("candidates"), list):
            rule["candidates"] = list(reversed(rule["candidates"]))
    body.pop("bundle_hash", None)
    return normalize_bundle(body)


def _start(state, *, seed="00" * 32, bundle=None, attention="focused",
           context="workshop"):
    case = case_for(True)
    return S44Session.start(
        state,
        bundle=bundle or _bundle(seed),
        case=case,
        source=source_for(case),
        attention=attention,
        language_context={"milieu_id": context},
    )


def _count_b_speech(session):
    return len([
        event for event in session.events()
        if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"
    ])


def test_same_seed_replays_and_seed_divergence_is_nonzero():
    first = generate_root(_bundle("11" * 32))
    again = generate_root(_bundle("11" * 32))
    assert first.root_hash == again.root_hash
    assert first.receipt["event_refs"] == again.receipt["event_refs"]
    assert first.receipt["draw_receipts"] == again.receipt["draw_receipts"]

    hashes = set()
    selected = set()
    for index in range(16):
        root = generate_root(_bundle(f"{index:02x}" * 32))
        hashes.add(root.root_hash)
        selected.add(tuple(
            (row["rule_name"], str(row.get("selected_value")))
            for row in root.receipt["draw_receipts"]
        ))
    assert len(hashes) > 1
    assert len(selected) > 1


def test_candidate_order_and_unrelated_stream_do_not_perturb_decisions():
    baseline = generate_root(_bundle("22" * 32))
    reordered = generate_root(_reverse_candidates(_bundle("22" * 32)))
    assert reordered.root_hash == baseline.root_hash
    assert reordered.receipt["draw_receipts"] == baseline.receipt["draw_receipts"]

    extra = _bundle("22" * 32)
    extra["rules"]["unused_observation"] = {
        "rule_id": "S44_UNUSED_OBSERVATION",
        "rule_version": "1",
        "registry_hash": "TEST_ONLY_UNUSED",
        "stream": "v3.causal.s44.unused.observation",
        "scope_kind": "RUN",
        "scope_id": "S44_ROOT",
        "operation": "WEIGHTED_CANDIDATE_INTEGER",
        "candidate_owner_authority": "TEST_ONLY_UNUSED",
        "candidates": [{
            "candidate_id": "unused_1", "value": 1, "weight_units": 1,
            "source_ref": "TEST_ONLY_UNUSED_SOURCE",
        }],
    }
    with_extra = generate_root(extra)
    assert with_extra.root_hash != baseline.root_hash
    assert with_extra.receipt["event_refs"] == baseline.receipt["event_refs"]
    assert with_extra.receipt["snapshot_hashes"] == baseline.receipt["snapshot_hashes"]
    assert [
        (row["rule_name"], row.get("selected_value"))
        for row in with_extra.receipt["draw_receipts"]
    ] == [
        (row["rule_name"], row.get("selected_value"))
        for row in baseline.receipt["draw_receipts"]
    ]


def test_conditional_receipts_consume_named_generated_predecessors():
    root = generate_root(_bundle("33" * 32))
    receipt = root.receipt
    assert receipt["selected_branches"]["conditions"]["b_extra_refusal"][
        "value"
    ] == receipt["initial_facts"]["a_material"]
    assert receipt["selected_branches"]["conditions"]["a_optional_decline"][
        "value"
    ] == receipt["joint"]["effective_index"]
    names = {row["rule_name"] for row in receipt["draw_receipts"]}
    assert {"b_extra_refusal", "a_optional_decline"} <= names
    for draw in receipt["draw_receipts"]:
        assert draw["semantic_rule_id"]
        assert draw["decision_replay_identity_hash"]
        if draw["operation"] == "WEIGHTED_CANDIDATE_INTEGER":
            assert draw["candidate_set_hash"]
            assert draw["selected_candidate_id"]
    assert receipt["selected_finished_life"] is False
    assert receipt["event_refs"]
    assert receipt["g18_history_refs"]["a"]
    assert receipt["g18_history_refs"]["b"]


def test_missing_rule_and_empty_candidates_are_typed_no_draw():
    missing = _bundle("44" * 32)
    del missing["rules"]["a_material"]
    with pytest.raises(S44Refusal) as exc:
        generate_root(missing)
    assert exc.value.code == "S44_RULE_MISSING"

    empty = _bundle("44" * 32)
    empty["rules"]["a_material"]["candidates"] = []
    with pytest.raises(S44Refusal) as exc:
        generate_root(empty)
    assert exc.value.code == "S44_CANDIDATE_SET_EMPTY"


def test_actual_consumer_uses_root_language_without_new_b_source(tmp_path):
    state = tmp_path / "person"
    session = _start(state)
    try:
        root = session.read_root()
        assert len(root["language_evidence"]) == 2
        root_source = root["language_evidence"][1]["source_event_id"]
        before_b = _count_b_speech(session)
        events = session.read_events()
        first = session.read_event(events[0]["e1_event_id"])
        assert first["language"]["source_event_id"] == root_source
        second = session.admit_event(
            language_context={"milieu_id": "workshop"},
            case=case_for(True),
            source=source_for(case_for(True)),
            history_event_refs=(events[0]["e1_event_id"],),
        )
        assert second["event"]["selected_option"] == "REQUEST_TOOL"
        assert second["event"]["attempt_status"] == "ADMITTED"
        language = second["event"]["language"]
        assert language["native_text"] == "¿Puedo usar la herramienta?"
        assert language["translation_text"] == "May I use the tool?"
        assert language["source_event_id"] == root_source
        assert _count_b_speech(session) == before_b
        second_s43 = session.read_s43_event(second["event"]["e1_event_id"])["s43"]
        assert second_s43["contrary_relations"]
        assert second_s43["contradictions"]
        assert second["event"]["c9"]["target_branch"] == "NO_CHANGE"
        assert second["event"]["c9"]["target_proposals"] == []
        assert session.verify()["ok"] is True
        actor_ids = root["actor_ids"]
        root_hash = root["root_hash"]
    finally:
        session.close()

    cold = S44Session.open(state)
    try:
        assert cold.read_root()["root_hash"] == root_hash
        assert cold.read_root()["actor_ids"] == actor_ids
        assert len(cold.read_events()) == 2
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_missing_initial_root_language_is_a_typed_no_source_refusal(tmp_path):
    state = tmp_path / "no-language"
    bundle = _bundle("55" * 32)
    bundle["language_evidence"] = []
    with pytest.raises(S44Refusal) as exc:
        _start(state, bundle=bundle)
    assert exc.value.code == "S44_INITIAL_LANGUAGE_EVIDENCE_MISSING"
    assert not (state / ROOT_FILE).exists()


def test_changed_root_rule_is_refused_at_actual_reader_then_restored(tmp_path):
    state = tmp_path / "rule-fault"
    session = _start(state, seed="66" * 32)
    root_hash = session.read_root()["root_hash"]
    session.close()
    root_path = state / ROOT_FILE
    original = root_path.read_text(encoding="utf8")
    document = json.loads(original)
    document["bundle"]["rules"]["a_material"]["candidates"][0][
        "weight_units"
    ] = 99
    root_path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n",
                         encoding="utf8")
    with pytest.raises(S44Refusal) as exc:
        S44Session.open(state)
    assert exc.value.code == "S44_ROOT_REPLAY_MISMATCH"
    root_path.write_text(original, encoding="utf8")
    restored = S44Session.open(state)
    try:
        assert restored.read_root()["root_hash"] == root_hash
        assert restored.verify()["ok"] is True
    finally:
        restored.close()


def test_frozen_root_survives_attention_change(tmp_path):
    state = tmp_path / "attention"
    session = _start(state, seed="77" * 32, attention="focused")
    root_hash = session.read_root()["root_hash"]
    first_hash = session.read_events()[0]["e1_event_hash"]
    session.close()
    changed = S44Session.open(state, attention="distracted")
    try:
        assert changed.read_root()["root_hash"] == root_hash
        assert changed.read_events()[0]["e1_event_hash"] == first_hash
        assert changed.verify()["ok"] is True
    finally:
        changed.close()
