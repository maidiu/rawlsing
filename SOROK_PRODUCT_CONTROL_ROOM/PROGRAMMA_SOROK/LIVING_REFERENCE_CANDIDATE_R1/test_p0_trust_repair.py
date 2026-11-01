"""P0 trust-boundary tests: fixture isolation, independent acceptance, journal, CAS, restoration."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

import pytest

import evidence_store
import living_reference as lr
import r2_live_transaction

OBSERVED = lr.observe_source_cut(git_enabled=False)


def _source(state: dict, node_id: str) -> dict:
    node = lr._node_map(state).get(node_id, {})
    refs = node.get("source_refs") or []
    if refs and refs[0].get("commit"):
        ref = refs[0]
        return {
            "commit": ref["commit"],
            "path": ref["path"],
            "blob": ref.get("blob") or ref.get("object_id"),
            "object_type": ref.get("object_type", "blob"),
        }
    row = next(r for r in state["source_manifest"]["rows"] if r["id"] == node_id)
    src = lr._normalized_source(row)
    return {
        "commit": src["commit"],
        "path": src["path"],
        "blob": src.get("blob") or src.get("object_id"),
        "object_type": src.get("object_type", "blob"),
    }


def _source_record(state: dict, node_id: str) -> dict:
    return {"kind": "SOURCE_RECORD", "source": _source(state, node_id)}


def _self_review(state: dict, node_id: str) -> dict:
    return {
        "kind": "SOURCEFREE_REVIEW",
        "source": _source(state, node_id),
        "reviewed_sha": lr.STARTUP_SHA,
        "reviewer_role": "INDEPENDENT_I3_ENGINEER",
        "review_scope": [node_id],
        "review_status": "PASS",
        "preimage": lr._digest(lr._node_source(state, node_id)),
    }


def test_demo_isolation_leaves_operating_files_byte_identical():
    result = r2_live_transaction.demo_isolation()
    assert result["result"] == "PASS"
    assert result["operating_files_before"] == result["operating_files_after"]
    assert result["demo"]["cold_readback"]["state_digest_equal"] is True
    assert result["demo"]["tamper"]["detected"] == "STATE_DIGEST_MISMATCH"
    assert result["demo"]["synthetic_requirement"]["status"] == "QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE"


def test_self_declared_review_cannot_promote_review_or_engineering():
    state = lr.build_state(OBSERVED)
    before = copy.deepcopy(state["axes"]["CP-A5-R2"])
    review = lr._apply_transition(state, {
        "node_id": "CP-A5-R2", "dimension": "review", "to": "REVIEW_PASSED_SCOPED",
        "evidence": _self_review(state, "CP-A5-R2"),
    })
    engineering = lr._apply_transition(state, {
        "node_id": "CP-A5-R2", "dimension": "engineering", "to": "INDEPENDENT_ACCEPT_SCOPED",
        "evidence": _self_review(state, "CP-A5-R2"),
    })
    assert review["status"] == "PENDING_INDEPENDENT_ACCEPTANCE"
    assert engineering["status"] == "PENDING_INDEPENDENT_ACCEPTANCE"
    assert state["axes"]["CP-A5-R2"] == before


def test_fixture_origin_cannot_promote_any_dimension():
    state = lr.build_state(OBSERVED)
    for dimension, target in (
        ("review", "REVIEW_PASSED_SCOPED"),
        ("engineering", "INDEPENDENT_ACCEPT_SCOPED"),
        ("authority", "OWNER_ADOPTED"),
        ("human", "PROVEN"),
        ("science", "ORIGINAL_ISSUED"),
        ("consumer", "ACTUAL"),
    ):
        with pytest.raises(ValueError, match="FIXTURE_ORIGIN_CANNOT_PROMOTE_ANY_DIMENSION"):
            lr._apply_transition(state, {
                "node_id": "CP-A5-R2", "dimension": dimension, "to": target,
                "evidence": {"kind": "SYNTHETIC_DEMO", "fixture_origin": True},
            })


def test_genuine_unrelated_sha_and_stale_subject_cannot_accept():
    state = lr.build_state(OBSERVED)
    state["nodes"] = [dict(n) for n in state["nodes"]]
    node = next(n for n in state["nodes"] if n["id"] == "JOIN_E_7BF")
    node["subject_sha"] = "f" * 40
    acceptance = {
        "kind": "ACCEPTANCE_RECORD",
        "reviewed_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
        "acceptance": {
            "reviewer_principal": "JOIN-V",
            "reviewer_role": "INDEPENDENT_HOSTILE_ENGINEERING_REVIEWER",
            "author_principal": "JOIN_E_OWNER",
            "subject_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
            "assertion": "fork atomicity/shared lineage exact scope",
            "scope": ["JOIN_E_7BF"],
            "appointment_ref": "2b8d3067d894941c21ec7fd23d1f883f51b15026",
            "record_ref": "4387dc818a96fda2d5271672505fbd9da1059703:WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md",
            "verdict": "ACCEPT_SCOPED",
        },
    }
    result = lr._apply_transition(state, {
        "node_id": "JOIN_E_7BF", "dimension": "engineering", "to": "INDEPENDENT_ACCEPT_SCOPED",
        "evidence": acceptance,
    })
    assert result["status"] == "PENDING_INDEPENDENT_ACCEPTANCE"
    assert state["axes"]["JOIN_E_7BF"]["engineering"] == "SOURCE_DEFINITION_ONLY"
    stale = copy.deepcopy(acceptance)
    stale["reviewed_sha"] = lr.STARTUP_SHA
    result2 = lr._apply_transition(state, {
        "node_id": "JOIN_E_7BF", "dimension": "engineering", "to": "INDEPENDENT_ACCEPT_SCOPED",
        "evidence": stale,
    })
    assert result2["status"] == "PENDING_INDEPENDENT_ACCEPTANCE"


def test_existing_join_v_record_is_verifiable_at_exact_scope():
    state = lr.build_state(OBSERVED)
    node = lr._node_map(state)["JOIN_V_4387"]
    evidence = {
        "kind": "ACCEPTANCE_RECORD",
        "reviewed_sha": "7bf2da302996491ddf34b9a039fea47ac982d135",
        "acceptance": node["acceptance_record"],
    }
    ok, reason, details = lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", evidence)
    assert ok, reason
    assert details["reviewer_principal"] != details["author_principal"]
    assert details["subject_sha"] == "7bf2da302996491ddf34b9a039fea47ac982d135"


def test_real_return_is_candidate_only_and_survives_cold_rebuild(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state_path = tmp_path / "state.json"
    source = {
        "commit": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7",
        "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
        "blob": "b457bebf63d4ae12d01b8481481368bcd082e269",
        "object_type": "blob",
    }
    fixture = {
        "id": "W1-A-TEST", "sha": source["commit"], "source": source,
        "new_requirement": "W1_A_VISIBLE_REQUIREMENT",
        "tests": {"passed": 0, "native": False},
        "node_updates": [{"id": "W1_A_RETURN", "evidence": {"return_sha": source["commit"]}}],
    }
    state = lr.build_state(OBSERVED)
    result = lr.intake_candidate(state, fixture)
    assert result["status"] == "CANDIDATE_NOT_PROMOTED"
    assert any(g["node"] == "W1_A_VISIBLE_REQUIREMENT" for g in state["gaps"])
    assert state["axes"]["W1_A_RETURN"]["operational"] == "CANDIDATE_EVIDENCE"
    lr._save(state, state_path)
    reloaded = lr._load_state(state_path)
    assert any(g["node"] == "W1_A_VISIBLE_REQUIREMENT" for g in reloaded["gaps"])


def test_journal_duplicate_truncation_and_tamper_detection(tmp_path: Path):
    journal = tmp_path / "journal.jsonl"
    event = lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00")
    first = evidence_store.append_event(journal, event)
    duplicate = evidence_store.append_event(journal, event)
    assert first["status"] == "EVENT_APPENDED"
    assert duplicate["status"] == "DUPLICATE_EVENT_IDEMPOTENT"
    assert len(evidence_store.read_journal(journal)) == 1
    journal.write_text(journal.read_text().rstrip("\n"), encoding="utf-8")
    with pytest.raises(evidence_store.JournalError, match="TRUNCATED"):
        evidence_store.read_journal(journal)


def test_stale_concurrent_journal_append_does_not_lose_evidence(tmp_path: Path):
    journal = tmp_path / "journal.jsonl"
    a = lr._event("GENESIS", {"a": 1}, created_at="2026-11-01T00:00:00+00:00")
    b = lr._event("QUARANTINE", {"b": 2}, created_at="2026-11-01T00:00:01+00:00")
    evidence_store.append_event(journal, a, expected_head=evidence_store.GENESIS)
    second = evidence_store.append_event(journal, b, expected_head=evidence_store.GENESIS)
    assert second["stale_expected_head"] is True
    events = evidence_store.read_journal(journal)
    assert len(events) == 2
    assert [e["kind"] for e in events] == ["GENESIS", "QUARANTINE"]


def test_state_cas_and_interrupted_write_recovery(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state_path = tmp_path / "state.json"
    body = lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00")
    lr.commit_event(body, journal_path=journal, state_path=state_path)
    state = lr._load_state(state_path)
    digest = state["state_digest"]
    with pytest.raises(lr.StaleStateRevision):
        lr._save(copy.deepcopy(state), state_path, expected_revision=999)
    state_path.write_text('{"broken":', encoding="utf-8")
    recovered = lr._load_state(state_path, recover=True)
    assert recovered["state_digest"] == digest
    assert recovered["journal_head"] == lr.rebuild_from_journal(journal)["journal_head"]


def test_cold_replay_is_deterministic(tmp_path: Path):
    journal = tmp_path / "journal.jsonl"
    body = lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00")
    evidence_store.append_event(journal, body)
    first = lr.rebuild_from_journal(journal, operating=True)
    second = lr.rebuild_from_journal(journal, operating=True)
    assert first["state_digest"] == second["state_digest"]
    assert first["journal_head"] == second["journal_head"]


def test_source_withdrawal_and_restore_preserve_second_independent_red():
    state = lr.build_state(OBSERVED)
    unrelated = copy.deepcopy(state["axes"]["Q_GAME_001"])
    baseline = copy.deepcopy(state["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"])
    lr._apply_transition(state, {
        "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "first source withdrawal"},
    })
    lr._apply_transition(state, {
        "node_id": "P1_A_ACCESS_PATH", "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "second independent RED"},
    })
    assert state["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"].startswith("INVALIDATED")
    restored = lr._apply_transition(state, {
        "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery", "to": "SOURCE_VERIFIED",
        "evidence": _source_record(state, "P1_B_MATERIAL_SOURCE"),
    })
    assert "P1_LATER_HELP_CONSUMER" not in restored["restored"]
    assert state["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"].startswith("INVALIDATED")
    assert state["axes"]["Q_GAME_001"] == unrelated
    second = lr._apply_transition(state, {
        "node_id": "P1_A_ACCESS_PATH", "dimension": "source_recovery", "to": "SOURCE_VERIFIED",
        "evidence": _source_record(state, "P1_A_ACCESS_PATH"),
    })
    assert "P1_LATER_HELP_CONSUMER" in second["restored"]
    assert state["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"] == baseline


def test_hypothesis_and_mention_edges_do_not_block():
    state = lr.build_state(OBSERVED)
    assert not any(
        e.get("required") for e in state["edges"]
        if e.get("dependency") in {"HYPOTHESIS", "MENTION", "ALTERNATIVE", "MISSING_EDGE"}
    )
    assert not any(
        e.get("required") for e in state["edges"]
        if "mention" in e.get("relation", "").lower() or "source_location" in e.get("relation", "").lower()
    )


def test_source_refs_verify_against_git_and_local_external_bytes():
    state = lr.build_state(OBSERVED)
    report = lr.verify_source_refs(state)
    assert report["result"] == "PASS", report["failures"][:3]
    assert report["checked_local"] > 50


def test_self_review_event_stays_pending_after_restart(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    events = [
        lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00"),
        lr._event("CANDIDATE_EVIDENCE", {"importer": "OSCIENCE", "patch_file": lr.OSCIENCE_PATCH.name, "patch_digest": lr._digest(lr._load(lr.OSCIENCE_PATCH)), "source_commit": lr.OSCIENCE_CUT}, created_at="2026-11-01T00:00:01+00:00"),
    ]
    state = lr.build_state(OBSERVED)
    fixture = {"node_id": "CP-A5-R2", "dimension": "review", "to": "REVIEW_PASSED_SCOPED", "evidence": _self_review(state, "CP-A5-R2")}
    events.append(lr._event("TRANSITION_REQUEST", {"fixture": fixture}, created_at="2026-11-01T00:00:02+00:00"))
    for event in events:
        evidence_store.append_event(journal, event)
    expected_review = lr.build_state(OBSERVED)["axes"]["CP-A5-R2"]["review"]
    first = lr.rebuild_from_journal(journal, operating=True)
    assert first["axes"]["CP-A5-R2"]["review"] == expected_review
    assert any(h.get("status") == "PENDING_INDEPENDENT_ACCEPTANCE" for h in first["history"])
    second = lr.rebuild_from_journal(journal, operating=True)
    assert second["state_digest"] == first["state_digest"]
    assert second["axes"]["CP-A5-R2"]["review"] == expected_review


def test_fixture_promotion_event_is_refused_on_operating_replay(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    for event in (
        lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00"),
        lr._event("TRANSITION_REQUEST", {"fixture": {"node_id": "CP-A5-R2", "dimension": "engineering", "to": "INDEPENDENT_ACCEPT_SCOPED", "evidence": {"kind": "SYNTHETIC_DEMO", "fixture_origin": True}}}, created_at="2026-11-01T00:00:01+00:00"),
    ):
        evidence_store.append_event(journal, event)
    expected_engineering = lr.build_state(OBSERVED)["axes"]["CP-A5-R2"]["engineering"]
    state = lr.rebuild_from_journal(journal, operating=True)
    assert state["axes"]["CP-A5-R2"]["engineering"] == expected_engineering
    assert any(item.get("status") == "REFUSED" for item in state.get("journal_applied", []))


def test_self_authored_or_selfhashed_acceptance_record_is_refused():
    state = lr.build_state(OBSERVED)
    node = lr._node_map(state)["JOIN_V_4387"]
    same_principal = copy.deepcopy(node["acceptance_record"])
    same_principal["reviewer_principal"] = same_principal["author_principal"]
    evidence = {"kind": "ACCEPTANCE_RECORD", "reviewed_sha": same_principal["subject_sha"], "acceptance": same_principal}
    ok, reason, _ = lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", evidence)
    assert not ok and reason == "SELF_REVIEW_PRINCIPAL_NOT_DISTINCT"
    selfhash = copy.deepcopy(node["acceptance_record"])
    selfhash["record_ref"] = "0" * 40 + ":WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md"
    evidence = {"kind": "ACCEPTANCE_RECORD", "reviewed_sha": selfhash["subject_sha"], "acceptance": selfhash}
    ok, reason, _ = lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", evidence)
    assert not ok and "REVIEW_RECORD_OBJECT_INVALID" in reason


def test_withdrawal_event_supersedes_prior_evidence(tmp_path: Path):
    journal = tmp_path / "journal.jsonl"
    genesis = lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00")
    evidence_store.append_event(journal, genesis)
    quarantine = lr._event("QUARANTINE", {"excluded_history_ids": ["R2_DEMO_H0003"]}, created_at="2026-11-01T00:00:01+00:00")
    appended = evidence_store.append_event(journal, quarantine)
    withdrawal = lr._event("EVIDENCE_WITHDRAWAL", {"withdraws_event_id": appended["event"]["event_id"], "reason": "SUPERSEDED_FOR_TEST"}, created_at="2026-11-01T00:00:02+00:00")
    first = evidence_store.append_event(journal, withdrawal)
    duplicate = evidence_store.append_event(journal, withdrawal)
    assert first["status"] == "EVENT_APPENDED"
    assert duplicate["status"] == "DUPLICATE_EVENT_IDEMPOTENT"
    state = lr.rebuild_from_journal(journal, operating=True)
    assert state.get("quarantine") == {}
    assert state["withdrawals"][0]["withdraws_event_id"] == appended["event"]["event_id"]
    assert state["withdrawals"][0]["reason"] == "SUPERSEDED_FOR_TEST"
