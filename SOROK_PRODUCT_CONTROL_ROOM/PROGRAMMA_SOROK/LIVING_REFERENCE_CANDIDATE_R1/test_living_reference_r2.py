"""R2 persistence, science ingest, authority and causal-regrade tests."""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import living_reference as lr
import verify_source_manifest as vsm

ROOT = Path(__file__).resolve().parent
OBSERVED = lr.observe_source_cut(git_enabled=False)


def _source(state: dict, node_id: str) -> dict:
    row = next(r for r in state["source_manifest"]["rows"] if r["id"] == node_id)
    source = lr._normalized_source(row)
    return {
        "commit": source["commit"],
        "path": source["path"],
        "blob": source.get("blob") or source.get("object_id"),
        "object_type": source.get("object_type", "blob"),
    }


def _source_record(state: dict, node_id: str) -> dict:
    source = _source(state, node_id)
    return {
        "kind": "SOURCE_RECORD",
        "source": source,
        "preimage": lr._digest(lr._node_source(state, node_id)),
    }


def _review(state: dict, node_id: str, status: str = "PASS") -> dict:
    return {
        "kind": "SOURCEFREE_REVIEW",
        "source": _source(state, node_id),
        "reviewed_sha": lr.STARTUP_SHA,
        "reviewer_role": "INDEPENDENT_I3_ENGINEER",
        "review_scope": [node_id],
        "review_status": status,
        "preimage": lr._digest(lr._node_source(state, node_id)),
    }


def _imported(state: dict) -> dict:
    return lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))


def test_oscience_patch_is_complete_typed_and_idempotent():
    state = lr.build_state(OBSERVED)
    assert (len(state["nodes"]), len(state["edges"])) == (lr.BASE_NODE_COUNT, lr.BASE_EDGE_COUNT)
    report = _imported(state)
    assert report["status"] == "CANDIDATE_EVIDENCE_IMPORTED"
    assert report["counts"] == {
        "workstream_upserts": 17,
        "legacy_records": 102,
        "legacy_source_grounded": 102,
        "new_nodes": 14,
        "typed_edges": 226,
    }
    assert (len(state["nodes"]), len(state["edges"])) == (lr.IMPORTED_NODE_COUNT, lr.IMPORTED_EDGE_COUNT)
    assert len(state["workstreams"]) == 17
    assert len(state["legacy_records"]) == 102
    assert len(state["missing_functions"]) == 14
    assert len({e["edge_id"] for e in state["edges"]}) == len(state["edges"])
    assert all(e["from"] in {n["id"] for n in state["nodes"]} and e["to"] in {n["id"] for n in state["nodes"]} for e in state["edges"])
    imported_edges = [e for e in state["edges"] if e.get("source", {}).get("commit") == "865b5b01e1a27e99020cf2bb389af8cd4c874b57"]
    assert len(imported_edges) == 226
    assert all(e["hypothetical"] for e in imported_edges)
    assert all(e["dependency_type"] in {"HYPOTHETICAL_PRODUCT_REQUISITE", "CANDIDATE_MISSING_FUNCTION_REQUIREMENT"} for e in imported_edges)
    # Original S question/output remains exact and science remains candidate, not issued.
    registry = {r["id"]: r for r in lr._load(lr.SEED_REGISTRY)["rows"]}
    for workstream in state["workstreams"]:
        row = registry[workstream["id"]]
        assert workstream["question"] == row.get("question")
        assert workstream["output"] == row.get("output")
        assert state["axes"][workstream["id"]]["science"] == "CANDIDATE_EVIDENCE_NOT_ISSUED"
        assert state["axes"][workstream["id"]]["authority"] != "OWNER_ADOPTED"
    # All 102 source records are exact, not empty.
    for record in state["legacy_records"]:
        assert record["source_grounding"] == "R3_KEYED_EXACT"
        assert record["source"]["commit"]
        assert record["source"]["path"]
        assert record["source"]["git_blob"]
    # Duplicate import does not add nodes or edges.
    before = (len(state["nodes"]), len(state["edges"]), len(state["legacy_records"]))
    duplicate = lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    assert duplicate["status"] == "DUPLICATE_IMPORT_IDEMPOTENT"
    assert (len(state["nodes"]), len(state["edges"]), len(state["legacy_records"])) == before


def test_refresh_preserves_history_axes_and_evidence_across_cold_reload(tmp_path: Path):
    state = lr.build_state(OBSERVED)
    import_report = lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    transition = lr._apply_transition(state, {
        "node_id": "S5",
        "dimension": "engineering",
        "to": "CANDIDATE_UPGRADED",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "candidate only"},
    })
    before_history = list(state["history"])
    before_axes = copy.deepcopy(state["axes"])
    before_evidence = dict(state["evidence_imports"])
    state_path = tmp_path / "state.json"
    lr._save(state, state_path)
    loaded = lr._load_state(state_path)
    assert loaded["state_digest"] == state["state_digest"]
    refreshed = lr.refresh_state(loaded, OBSERVED)
    assert refreshed["source_cut_stale"] is False
    assert len(refreshed["history"]) >= len(before_history)
    assert any(h["history_id"] == import_report["evidence_digest"] or h.get("kind") == "OSCIENCE_PATCH_IMPORTED" for h in refreshed["history"])
    assert any(h.get("history_id") == transition["history_id"] for h in refreshed["history"])
    assert refreshed["axes"]["S5"] == before_axes["S5"]
    assert refreshed["evidence_imports"].keys() == before_evidence.keys()
    assert (len(refreshed["nodes"]), len(refreshed["edges"])) == (lr.IMPORTED_NODE_COUNT, lr.IMPORTED_EDGE_COUNT)
    lr._save(refreshed, state_path)
    cold = subprocess.run(
        [sys.executable, "living_reference.py", "--state", str(state_path), "export"],
        cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True)
    assert cold.returncode == 0, cold.stderr
    cold_state = json.loads(cold.stdout)
    assert cold_state["state_digest"] == refreshed["state_digest"]
    assert cold_state["axes"]["S5"]["engineering"] == "CANDIDATE_UPGRADED"
    assert len(cold_state["legacy_records"]) == 102
    # Replay ingestion after refresh stays idempotent.
    assert lr.ingest_oscience(refreshed, lr._load(lr.OSCIENCE_PATCH))["status"] == "DUPLICATE_IMPORT_IDEMPOTENT"


def test_source_cut_change_is_visible_and_does_not_reset_state():
    state = lr.build_state(OBSERVED)
    changed = copy.deepcopy(OBSERVED)
    changed["read_at"] = "2026-10-31T12:00:00+00:00"
    changed["heads"]["premain"]["sha"] = "a" * 40
    refreshed = lr.refresh_state(state, changed)
    assert refreshed["source_cut_stale"] is True
    assert any(h.get("kind") == "SOURCE_CUT_CHANGED" for h in refreshed["history"])
    assert any(g["id"] == "GAP_SOURCE_CUT_STALE" for g in refreshed["gaps"])
    assert refreshed["axes"] == state["axes"]
    assert len(refreshed["history"]) > len(state["history"])


def test_positive_transition_does_not_mass_invalidate():
    state = lr.build_state(OBSERVED)
    before = copy.deepcopy(state["axes"])
    result = lr._apply_transition(state, {
        "node_id": "B-F1CR-R2",
        "dimension": "engineering",
        "to": "CANDIDATE_UPGRADED",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "candidate only"},
    })
    assert result["status"] == "SIMULATED_NOT_ADOPTED"
    assert result["invalidated"] == []
    assert not any(str(v.get("consumer", "")).startswith("INVALIDATED") for v in state["axes"].values())
    assert state["axes"]["M01"]["consumer"] == before["M01"]["consumer"]
    assert state["axes"]["B-F1CR-R2"]["human"] == before["B-F1CR-R2"]["human"]
    assert state["axes"]["B-F1CR-R2"]["authority"] == before["B-F1CR-R2"]["authority"]
    assert state["pyat_boundary"]["status"] == "EXTERNAL_OWNER_HELD"


def test_source_withdrawal_invalidates_only_required_dependent_then_repair_restores():
    state = lr.build_state(OBSERVED)
    unrelated = state["axes"]["M01"]["consumer"]
    withdrawal = lr._apply_transition(state, {
        "node_id": "B-F1CR-R2",
        "dimension": "source_recovery",
        "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "source withdrawal simulation"},
    })
    assert withdrawal["status"] == "SIMULATED_NOT_ADOPTED"
    assert withdrawal["invalidated"]
    assert any("L4_I1_TARGETLESS" == x or "L4_NAMED_FIRST_CONSUMER" == x for x in withdrawal["invalidated"])
    assert state["axes"]["M01"]["consumer"] == unrelated
    assert state["pyat_boundary"]["status"] == "EXTERNAL_OWNER_HELD"
    assert any(g["id"].startswith("GAP_INVALIDATED_") for g in state["gaps"])
    repair = lr._apply_transition(state, {
        "node_id": "B-F1CR-R2",
        "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED",
        "evidence": _source_record(state, "B-F1CR-R2"),
    })
    assert repair["status"] == "APPLIED_CANDIDATE_ONLY"
    assert repair["restored"]
    assert all(not state["axes"][x]["consumer"].startswith("INVALIDATED") for x in repair["restored"])
    assert all(state["axes"][x]["consumer"] == state["consumer_baseline"].get(x, state["axes"][x]["consumer"]) for x in repair["restored"])
    assert not any(g["id"] in {"GAP_INVALIDATED_" + x for x in repair["restored"]} for g in state["gaps"])


def test_fake_owner_grant_and_human_participant_do_not_green_authority():
    state = lr.build_state(OBSERVED)
    with pytest.raises(ValueError):
        lr._apply_transition(state, {
            "node_id": "A5", "dimension": "authority", "to": "OWNER_ADOPTED",
            "owner_evidence": "OWNER_GRANT fake", "reviewer_evidence": "reviewer fake",
        })
    with pytest.raises(ValueError):
        lr._apply_transition(state, {
            "node_id": "A5", "dimension": "authority", "to": "OWNER_ADOPTED",
            "evidence": {"kind": "OWNER_GRANT", "owner_slot": "SOROK_HQ", "scope": ["A5"], "source": {"commit": "f" * 40, "path": "x", "blob": "f" * 40, "object_type": "blob"}},
        })
    pending = lr._apply_transition(state, {
        "node_id": "A5", "dimension": "authority", "to": "OWNER_ADOPTED",
        "evidence": {"kind": "OWNER_GRANT", "owner_slot": "SOROK_HQ", "scope": ["A5"], "source": _source(state, "A5"), "preimage": lr._digest(lr._node_source(state, "A5"))},
    })
    assert pending["status"] == "PENDING_MANUAL_VERIFICATION"
    assert state["axes"]["A5"]["authority"] == "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION"
    assert state["authority_holds"]
    with pytest.raises(ValueError):
        lr._apply_transition(state, {"node_id": "A5", "dimension": "human", "to": "PROVEN", "owner_evidence": "HUMAN_PARTICIPANT fake"})
    simulated = lr._apply_transition(state, {
        "node_id": "A5", "dimension": "human", "to": "PROVEN",
        "evidence": {"kind": "HUMAN_PARTICIPANT", "participant_record_hash": "a" * 64, "consent_record": "consent", "protocol": "protocol", "reviewer_role": "INDEPENDENT"},
    })
    assert simulated["status"] == "SIMULATED_NOT_ADOPTED"
    assert state["axes"]["A5"]["human"] == "CANDIDATE_LAB_DEMO_NOT_HUMAN_A5"
    assert state["axes"]["A5"]["human"] != "PROVEN"


def test_imported_candidate_grades_do_not_change_native_or_owner_status():
    state = lr.build_state(OBSERVED)
    lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    assert state["axes"]["A5"]["human"] == "NOT_PROVEN"
    assert state["axes"]["A5"]["authority"] == "NOT_ADOPTED"
    assert state["axes"]["C11"]["authority"] == "NOT_ADOPTED"
    assert state["axes"]["N10"]["science"] != "ORIGINAL_ISSUED"
    lr._apply_transition(state, {"node_id": "CP-A5-R2", "dimension": "engineering", "to": "CANDIDATE_UPGRADED", "evidence": {"kind": "SYNTHETIC_DEMO", "note": "author-test only"}})
    assert state["axes"]["CP-A5-R2"]["human"] == "NOT_PROVEN"
    assert state["axes"]["A5"]["human"] == "NOT_PROVEN"


def test_dynamic_gaps_work_now_and_blocked_chain_react_to_import_and_withdrawal():
    state = lr.build_state(OBSERVED)
    baseline_s0 = next(g for g in state["gaps"] if g["id"] == "GAP_WORKSTREAM_S0")
    assert baseline_s0["status"] == "SOURCE_DEFINED_CONSUMER_MISSING"
    assert any(c["gap_id"] == "GAP_WORKSTREAM_S0" for c in state["work_now"]["candidates"])
    lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    imported_s0 = next(g for g in state["gaps"] if g["id"] == "GAP_WORKSTREAM_S0")
    assert imported_s0["status"] == "CANDIDATE_EVIDENCE_CONSUMER_MISSING"
    assert any(c["gap_id"] == "GAP_WORKSTREAM_S0" for c in state["work_now"]["candidates"])
    blocked = lr.blocked_chain(state, "A5")
    assert blocked["kind"] == "TYPED_BLOCKED_CHAIN"
    assert any(b["node"] == "A5" and any(x["axis"] == "human" for x in b["blockers"]) for b in blocked["blocked"])
    withdrawal = lr._apply_transition(state, {"node_id": "S5", "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND", "evidence": {"kind": "SYNTHETIC_DEMO", "note": "source withdrawal"}})
    assert withdrawal["invalidated"]
    assert any(g["id"].startswith("GAP_INVALIDATED_") for g in state["gaps"])
    assert any(c["gap_id"].startswith("GAP_INVALIDATED_") for c in state["work_now"]["candidates"])
    repair = lr._apply_transition(state, {"node_id": "S5", "dimension": "source_recovery", "to": "SOURCE_VERIFIED", "evidence": _source_record(state, "S5")})
    assert repair["restored"]
    assert not any(g["id"] in {"GAP_INVALIDATED_" + x for x in repair["restored"]} for g in state["gaps"])
    assert any(g["id"] == "GAP_S5_NORMATIVE_OUTPUT" for g in state["gaps"])


def test_external_pyat_boundary_is_not_locally_mutable():
    state = lr.build_state(OBSERVED)
    with pytest.raises(ValueError):
        lr._apply_transition(state, {
            "node_id": "PYAT_EXTERNAL_BOUNDARY",
            "dimension": "authority",
            "to": "CANDIDATE_ONLY",
            "evidence": {"kind": "SYNTHETIC_DEMO"},
        })
    assert state["pyat_boundary"]["status"] == "EXTERNAL_OWNER_HELD"


def test_blocked_chain_excludes_hypothesis_edges_and_source_identity_alone():
    state = lr.build_state(OBSERVED)
    lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    blocked = lr.blocked_chain(state, "C12")
    assert blocked["hypothetical_edges_excluded"] >= 226
    assert blocked["kind"] == "TYPED_BLOCKED_CHAIN"
    s0_gap = next(g for g in state["gaps"] if g["id"] == "GAP_WORKSTREAM_S0")
    assert s0_gap["source_grade"] == "SOURCE_EXACT"
    assert s0_gap["status"] == "CANDIDATE_EVIDENCE_CONSUMER_MISSING"
    assert state["axes"]["S0"]["consumer"] != "ACTUAL"


def test_source_manifest_verifier_remains_independent_of_author_digest():
    report = vsm.verify(lr.ROOT, lr.REPO)
    assert report["result"] == "PASS", report
    assert report["rows"] == 144
    assert report["references"] == 3


def test_actual_source_cut_does_not_call_old_negative_r3_review_acceptance():
    observed = lr.observe_source_cut(git_enabled=True)
    if observed["status"] == "OBSERVED_LOCAL_GIT_REFS":
        assert observed["heads"]["r3_review"]["sha"] != lr.R3_REVIEW_OLD_NEGATIVE
        assert observed["heads"]["r3_review"]["sha"] != "UNKNOWN"
        assert observed["heads"]["premain"]["sha"] != "UNKNOWN"
