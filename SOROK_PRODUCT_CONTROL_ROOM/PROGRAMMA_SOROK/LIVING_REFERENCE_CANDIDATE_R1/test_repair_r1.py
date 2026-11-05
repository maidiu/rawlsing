"""Focused repair tests for PROGRAMMA SOROK P0/P1 repair R1."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import evidence_store
import living_reference as lr

ROOT = Path(__file__).resolve().parent
OBSERVED = lr.observe_source_cut(git_enabled=False)
W1A_SOURCE = {
    "commit": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7",
    "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
    "blob": "b457bebf63d4ae12d01b8481481368bcd082e269",
    "object_type": "blob",
}
W1A_QUOTE = "No single technical milestone or personality description can certify it."


def _source_record(state: dict, node_id: str) -> dict:
    node = lr._node_map(state)[node_id]
    ref = node["source_refs"][0]
    return {
        "kind": "SOURCE_RECORD",
        "source": {
            "commit": ref["commit"],
            "path": ref["path"],
            "blob": ref.get("blob") or ref.get("object_id"),
            "object_type": ref.get("object_type", "blob"),
        },
    }


def test_acceptance_rejects_arbitrary_record_wildcard_and_unrelated_subject():
    state = lr.build_state(OBSERVED)
    node = lr._node_map(state)["JOIN_V_4387"]
    valid = {"kind": "ACCEPTANCE_RECORD", "reviewed_sha": "7bf2da302996491ddf34b9a039fea47ac982d135", "acceptance": node["acceptance_record"]}
    assert lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", valid)[0] is True
    arbitrary = copy.deepcopy(valid)
    arbitrary["acceptance"]["record_ref"] = "54013d1907e5ea55b0d1f54ea9afe07ef6388b11:WORKER_RETURNS/PROGRAMMA_SOROK_P0_P1_LIVING_REFERENCE_ENGINEERING_R1/00_RETURN.md"
    arbitrary["acceptance"]["scope"] = ["*"]
    assert lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", arbitrary)[1] == "REVIEW_RECORD_NOT_A_NODE_SOURCE"
    wildcard = copy.deepcopy(valid)
    wildcard["acceptance"]["scope"] = ["*"]
    assert lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", wildcard)[1] == "WILDCARD_SCOPE_NOT_ACCEPTED"
    stale = copy.deepcopy(state)
    next(n for n in stale["nodes"] if n["id"] == "JOIN_E_7BF")["subject_sha"] = "f" * 40
    assert lr._verify_acceptance_record(stale, "JOIN_E_7BF", "engineering", valid)[1] == "NODE_SUBJECT_NOT_IN_REVIEW_RECORD"
    wrong_assertion_subject = copy.deepcopy(state)
    next(n for n in wrong_assertion_subject["nodes"] if n["id"] == "JOIN_E_7BF")["subject_sha"] = "49022f693c99b6cb58226513f8bad71c26bdac3c"
    assert lr._verify_acceptance_record(wrong_assertion_subject, "JOIN_E_7BF", "engineering", valid)[1] == "NODE_SUBJECT_DOES_NOT_MATCH_ACCEPTING_ASSERTION"
    self_claim = copy.deepcopy(valid)
    self_claim["acceptance"]["reviewer_principal"] = self_claim["acceptance"]["author_principal"]
    assert lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", self_claim)[1] == "CALLER_REVIEWER_DOES_NOT_MATCH_RECORD"
    assert lr._verify_acceptance_record(state, "CP-A5-R2", "engineering", valid)[1] == "REVIEW_RECORD_NOT_A_NODE_SOURCE"


def test_oscience_patch_digest_is_recomputed_before_import_and_duplicate(tmp_path: Path, monkeypatch):
    state = lr.build_state(OBSERVED)
    patch = lr._load(lr.OSCIENCE_PATCH)
    original = lr._digest(patch)
    tampered = copy.deepcopy(patch)
    tampered["workstream_evidence_upserts"][0]["domains"] = ["TAMPERED_BUT_SAME_COUNTS"]
    with pytest.raises(ValueError, match="OSCIENCE_PATCH_DIGEST_MISMATCH"):
        lr.ingest_oscience(state, tampered, patch_digest=original)
    lr.ingest_oscience(state, patch)
    with pytest.raises(ValueError, match="OSCIENCE_PATCH_DIGEST_MISMATCH"):
        lr.ingest_oscience(state, tampered, patch_digest=original)
    temp_root = tmp_path / "root"
    temp_root.mkdir()
    (temp_root / lr.OSCIENCE_PATCH.name).write_text(json.dumps(tampered), encoding="utf-8")
    journal = tmp_path / "evidence" / "journal.jsonl"
    evidence_store.append_event(journal, lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-01T00:00:00+00:00"))
    evidence_store.append_event(journal, lr._event("CANDIDATE_EVIDENCE", {
        "importer": "OSCIENCE", "patch_file": lr.OSCIENCE_PATCH.name,
        "patch_digest": original, "source_commit": lr.OSCIENCE_CUT,
    }, created_at="2026-11-01T00:00:01+00:00"))
    monkeypatch.setattr(lr, "ROOT", temp_root)
    with pytest.raises(ValueError, match="OSCIENCE_PATCH_DIGEST_MISMATCH"):
        lr.rebuild_from_journal(journal, operating=True)


def test_complete_tail_loss_is_refused_without_overwriting_newer_state(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state_path = tmp_path / "state.json"
    lr.commit_event(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-01T00:00:00+00:00"), journal_path=journal, state_path=state_path)
    lr.commit_event(lr._event("QUARANTINE", {"excluded_history_ids": ["X"]}, created_at="2026-11-01T00:00:01+00:00"), journal_path=journal, state_path=state_path)
    before = state_path.read_bytes()
    lines = journal.read_text(encoding="utf-8").splitlines()
    journal.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    with pytest.raises(evidence_store.JournalRegression, match="JOURNAL_PREFIX_OLDER_THAN_KNOWN_STATE"):
        lr._load_state(state_path)
    assert state_path.read_bytes() == before
    journal_before = journal.read_bytes()
    with pytest.raises(evidence_store.JournalRegression, match="JOURNAL_PREFIX_OLDER_THAN_KNOWN_STATE"):
        lr.commit_event(lr._event("QUARANTINE", {"excluded_history_ids": ["Y"]}), journal_path=journal, state_path=state_path)
    assert journal.read_bytes() == journal_before
    recovered = lr._load_state(state_path, recover=True)
    assert recovered["revision"] == 1
    assert recovered["journal_regression_recovery"]["status"] == "EXPLICIT_RECOVERY_FROM_SHORTER_JOURNAL"


def test_concurrent_commit_event_writers_preserve_all_events_and_monotonic_state(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state_path = tmp_path / "state.json"
    lr.commit_event(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-01T00:00:00+00:00"), journal_path=journal, state_path=state_path)
    fixtures = []
    for index, node_id in enumerate(("CP-A5-R2", "B-F1CR-R2")):
        fixture = {
            "node_id": node_id,
            "dimension": "engineering",
            "to": "CANDIDATE_UPGRADED",
            "evidence": {"kind": "SYNTHETIC_DEMO", "note": f"concurrent-{index}"},
        }
        path = tmp_path / f"fixture_{index}.json"
        path.write_text(json.dumps(fixture), encoding="utf-8")
        fixtures.append(path)
    processes = [
        subprocess.Popen(
            [sys.executable, str(ROOT / "living_reference.py"), "--state", str(state_path), "apply-authorized-transition", str(path)],
            cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for path in fixtures
    ]
    outputs = [process.communicate(timeout=60) for process in processes]
    assert [process.returncode for process in processes] == [0, 0], outputs
    events = evidence_store.read_journal(journal)
    assert len(events) == 3
    loaded = lr._load_state(state_path)
    cold = lr.rebuild_from_journal(journal, operating=True)
    assert loaded["revision"] == 3
    assert loaded["journal_head"] == events[-1]["event_id"]
    assert loaded["state_digest"] == cold["state_digest"]


def test_present_source_cannot_prove_withdrawal_or_absence():
    state = lr.build_state(OBSERVED)
    state["operating"] = True
    source = _source_record(state, "P1_B_MATERIAL_SOURCE")
    with pytest.raises(ValueError, match="QUALIFIED_WITHDRAWAL_EVIDENCE_REQUIRED"):
        lr._apply_transition(state, {
            "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery",
            "to": "SOURCE_NOT_FOUND", "evidence": source,
        })
    with pytest.raises(ValueError, match="QUALIFIED_WITHDRAWAL_EVENT_REQUIRED"):
        lr._apply_transition(state, {
            "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery",
            "to": "SOURCE_WITHDRAWN",
            "evidence": {
                "kind": "SOURCE_WITHDRAWAL", "basis": "SOURCE_OWNER_WITHDRAWAL",
                "authority": "SOROK_HQ", "scope": ["P1_B_MATERIAL_SOURCE"],
            },
        })


def test_live_and_cold_withdrawal_restore_preserves_review_and_engineering_negatives(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state_path = tmp_path / "state.json"
    baseline = lr.build_state(OBSERVED)
    gt0 = copy.deepcopy(baseline["axes"]["GT0_END_TO_END"])
    q_game = copy.deepcopy(baseline["axes"]["Q_GAME_001"])
    b = _source_record(baseline, "P1_B_MATERIAL_SOURCE")
    a = _source_record(baseline, "P1_A_ACCESS_PATH")

    def commit(body: dict) -> dict:
        return lr.commit_event(body, journal_path=journal, state_path=state_path)

    commit(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-01T00:00:00+00:00"))
    commit(lr._event("CANDIDATE_EVIDENCE", {
        "importer": "OSCIENCE", "patch_file": lr.OSCIENCE_PATCH.name,
        "patch_digest": lr._digest(lr._load(lr.OSCIENCE_PATCH)), "source_commit": lr.OSCIENCE_CUT,
    }, created_at="2026-11-01T00:00:01+00:00"))
    for index, node_id in enumerate(("P1_B_MATERIAL_SOURCE", "P1_A_ACCESS_PATH"), start=2):
        withdrawal = commit(lr._event("EVIDENCE_WITHDRAWAL", {
            "node_id": node_id, "basis": "QUALIFIED_ABSENCE_VERIFICATION",
            "authority": "SOROK_HQ", "scope": [node_id], "reason": "qualified absence",
        }, created_at=f"2026-11-01T00:00:0{index}+00:00"))
        commit(lr._event("TRANSITION_REQUEST", {"fixture": {
            "node_id": node_id, "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND",
            "evidence": {
                "kind": "SOURCE_WITHDRAWAL", "basis": "QUALIFIED_ABSENCE_VERIFICATION",
                "authority": "SOROK_HQ", "scope": [node_id],
                "withdrawal_event_id": withdrawal["event"]["event_id"],
            },
        }}, created_at=f"2026-11-01T00:00:0{index + 2}+00:00"))
    commit(lr._event("TRANSITION_REQUEST", {"fixture": {
        "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "review", "to": "REVIEW_FAILED",
        "evidence": {
            "kind": "SOURCEFREE_REVIEW", "source": b["source"],
            "reviewed_sha": lr.ENGINEERING_BASELINE, "review_status": "FAIL",
            "reviewer_role": "INDEPENDENT",
        },
    }}, created_at="2026-11-01T00:00:06+00:00"))
    commit(lr._event("TRANSITION_REQUEST", {"fixture": {
        "node_id": "P1_A_ACCESS_PATH", "dimension": "engineering", "to": "FAILED",
        "evidence": a,
    }}, created_at="2026-11-01T00:00:07+00:00"))
    commit(lr._event("TRANSITION_REQUEST", {"fixture": {
        "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED", "evidence": b,
    }}, created_at="2026-11-01T00:00:08+00:00"))
    commit(lr._event("TRANSITION_REQUEST", {"fixture": {
        "node_id": "P1_A_ACCESS_PATH", "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED", "evidence": a,
    }}, created_at="2026-11-01T00:00:09+00:00"))
    live = lr._load_state(state_path)
    cold = lr.rebuild_from_journal(journal, operating=True)
    for state in (live, cold):
        assert state["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"].startswith("INVALIDATED")
        assert state["axes"]["P1_B_MATERIAL_SOURCE"]["review"] == "REVIEW_FAILED"
        assert state["axes"]["P1_A_ACCESS_PATH"]["engineering"] == "FAILED"
        assert state["axes"]["GT0_END_TO_END"] == gt0
        assert state["axes"]["Q_GAME_001"] == q_game


def test_return_intake_requires_real_sha_and_source_locator():
    state = lr.build_state(OBSERVED)
    fake = lr.intake_candidate(state, {"id": "FAKE", "sha": "a" * 40, "source": W1A_SOURCE})
    assert fake["status"] == "QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE"
    mismatch = lr.intake_candidate(state, {"id": "MISMATCH", "sha": lr.ENGINEERING_BASELINE, "source": W1A_SOURCE})
    assert mismatch["status"] == "QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE"
    state = lr.build_state(OBSERVED)
    lr.intake_candidate(state, {
        "id": "UNLOCATED", "sha": W1A_SOURCE["commit"], "source": W1A_SOURCE,
        "new_requirement": "W1_A_UNLOCATED_CLAIM",
        "node_updates": [{"id": "W1_A_RETURN", "evidence": {"return_sha": W1A_SOURCE["commit"]}}],
    })
    gap = next(g for g in state["gaps"] if g["node"] == "W1_A_UNLOCATED_CLAIM")
    assert gap["evidence_status"] == "CALLER_CLAIM_UNVERIFIED"
    assert gap["source_backed"] is False
    assert state["axes"]["W1_A_RETURN"]["operational"] == "CANDIDATE_ONLY"
    assert any(c["gap_id"] == gap["id"] and c["source_backed"] is False for c in state["work_now"]["candidates"])
    state = lr.build_state(OBSERVED)
    lr.intake_candidate(state, {
        "id": "LOCATED", "sha": W1A_SOURCE["commit"], "source": W1A_SOURCE,
        "new_requirement": "W1_A_LOCATED_CLAIM",
        "locator": {"path": W1A_SOURCE["path"], "quote": W1A_QUOTE},
        "node_updates": [{
            "id": "W1_A_RETURN", "evidence": {"return_sha": W1A_SOURCE["commit"]},
            "locator": {"path": W1A_SOURCE["path"], "quote": W1A_QUOTE},
        }],
    })
    gap = next(g for g in state["gaps"] if g["node"] == "W1_A_LOCATED_CLAIM")
    assert gap["evidence_status"] == "SOURCE_LOCATED"
    assert gap["source_backed"] is True
    assert state["axes"]["W1_A_RETURN"]["operational"] == "CANDIDATE_EVIDENCE"
    assert any(c["gap_id"] == gap["id"] and c["source_backed"] is True for c in state["work_now"]["candidates"])


def test_external_witness_reaches_home_focus_maturity_and_gaps():
    state = lr.build_state(OBSERVED)
    node = lr._node_map(state)["V3_RUN_ONE_YEAR"]
    external = Path(node["source_refs"][0]["path"])
    home = lr.home_view(state)
    if external.exists():
        assert state["axes"]["V3_RUN_ONE_YEAR"]["source_recovery"] == "SOURCE_EXACT"
        return
    assert state["axes"]["V3_RUN_ONE_YEAR"]["source_recovery"] == "UNREAD"
    assert any(item["id"] == "V3_RUN_ONE_YEAR" for item in home["source_witness"])
    assert lr.focus_view(state, "V3_RUN_ONE_YEAR")["source_verification"]["status"] == "UNREAD"
    assert lr.maturity_view(state, "V3_RUN_ONE_YEAR")["source_verification"]["status"] == "UNREAD"
    assert any(g["id"] == "GAP_WITNESS_V3_RUN_ONE_YEAR" for g in state["gaps"])


def test_home_is_purpose_first_and_work_now_has_no_descendant_priority():
    state = lr.build_state(OBSERVED)
    home = lr.home_view(state)
    assert list(home)[:4] == ["schema", "purpose", "intended_human_experience", "constraints_100_101"]
    assert home["purpose"]["id"] == "PURPOSE_UNCHOSEN_NEIGHBOR"
    assert home["intended_human_experience"]["astra_b_scene"]["id"] == "ASTRA_B_SCENE"
    assert home["constraints_100_101"]["alpha_100"]["id"] == "SOROK_100_ALPHA"
    work = state["work_now"]
    assert work["no_scalar_priority"] is True
    ordered = sorted(work["candidates"], key=lambda c: (c["parallel_group"], c["domain"], c["gap_id"]))
    assert [c["gap_id"] for c in work["candidates"]] == [c["gap_id"] for c in ordered]
    assert all("terminal_contribution" in c and "uncertainty" in c for c in work["candidates"])


def test_baseline_identity_separates_olive_source_from_engineering_baseline(tmp_path: Path):
    state = lr.build_state(OBSERVED)
    assert state["build_startup"] == lr.ENGINEERING_BASELINE
    assert state["version_vector"]["engineering_baseline"] == lr.ENGINEERING_BASELINE
    assert state["version_vector"]["olive_source"] == lr.OLIVE_SOURCE_SHA
    assert state["history"][0]["source_vector"]["engineering_baseline"] == lr.ENGINEERING_BASELINE
    journal = tmp_path / "journal.jsonl"
    evidence_store.append_event(journal, lr._event("GENESIS", {"baseline_sha": lr.OLIVE_SOURCE_SHA}, created_at="2026-11-01T00:00:00+00:00"))
    rebuilt = lr.rebuild_from_journal(journal, operating=True)
    assert rebuilt["build_startup"] == lr.ENGINEERING_BASELINE
    assert rebuilt["baseline_identity"]["genesis_claim"] == lr.OLIVE_SOURCE_SHA
    assert rebuilt["baseline_identity"]["genesis_claim_interpretation"] == "INHERITED_OLIVE_SOURCE_IDENTITY_NOT_ENGINEERING_BASELINE"
