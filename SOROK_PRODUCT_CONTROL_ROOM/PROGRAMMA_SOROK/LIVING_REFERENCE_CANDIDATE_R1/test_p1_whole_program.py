"""P1 whole-program navigation, maturity and gap-intelligence tests."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import evidence_store
import living_reference as lr

OBSERVED = lr.observe_source_cut(git_enabled=False)


def _state() -> dict:
    state = lr.build_state(OBSERVED)
    lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    return state


def _reachable(state: dict, start: str, target: str, depth: int = 12) -> bool:
    nodes, _ = lr._neighbors(state, start, depth)
    return target in {n["id"] for n in nodes}


def _source_ref(node: dict) -> dict:
    ref = node["source_refs"][0]
    return {
        "commit": ref["commit"],
        "path": ref["path"],
        "blob": ref.get("blob") or ref.get("object_id"),
        "object_type": ref.get("object_type", "blob"),
    }


def _record(node: dict) -> dict:
    return {"kind": "SOURCE_RECORD", "source": _source_ref(node)}


def test_demo1_unchosen_neighbor_to_astra_to_100_101_to_code_or_missing_to_a5():
    state = _state()
    for target in ("ASTRA_B_SCENE", "ASTRA_D_LONGITUDINAL", "SOROK_100_ALPHA", "SOROK_101_BINDING", "P1_RETURN", "P1_CONSUMER_CODE", "A5", "CAN011_RULE_T_MISSING"):
        assert _reachable(state, "PURPOSE_UNCHOSEN_NEIGHBOR", target, 10), target
    assert _reachable(state, "P1_CONSUMER_CODE", "PURPOSE_UNCHOSEN_NEIGHBOR", 10)
    assert state["axes"]["A5"]["human"] == "NOT_PROVEN"
    assert any(e.get("dependency") == "MISSING_EDGE" for e in state["edges"] if e["from"] == "P1_RETURN")


def test_demo2_q_game_and_q_action_keep_open_text_and_closed_for_alpha():
    state = _state()
    nodes = lr._node_map(state)
    for node_id in ("Q_GAME_001", "Q_ACTION_001"):
        assert nodes[node_id]["status"] == "OPEN_TEXT__CLOSED_FOR_ALPHA"
        assert "status OPEN" in nodes[node_id]["source_refs"][0]["quote"]
        assert "CLOSED_FOR_ALPHA" in nodes[node_id]["source_refs"][0]["quote"]
        assert any(e["from"] == node_id and "closed_for_alpha" in e["relation"] for e in state["edges"])
    gaps = lr.whole_program_gaps(state)
    assert not any(g.get("node") in {"Q_GAME_001", "Q_ACTION_001"} for group in gaps["groups"] for g in group["gaps"])


def test_demo3_q_health_links_incentives_privacy_and_attachment_counterexample():
    state = _state()
    for target in ("S5", "S13", "S14", "S15"):
        assert _reachable(state, "Q_HEALTH_001", target, 3), target
    assert _reachable(state, "FLOURISHING_ALT_ATTACHMENT", "Q_HEALTH_001", 2)
    assert lr.maturity_view(state, "Q_HEALTH_001")["stages"]["T"]["status"] == "CONTESTED"
    gap = next(g for g in state["p1_gap_records"] if g["id"] == "GAP-Q-HEALTH-FLOURISHING")
    assert "T" in gap["missing_stages"] and "V" in gap["missing_stages"]
    assert "attachment" in " ".join(gap["alternatives"]).lower()
    assert "health_score.py" in gap["smallest_useful_next_action"]


def test_demo4_historical_v3_external_consumers_vs_current_blocked():
    state = _state()
    nodes = lr._node_map(state)
    assert nodes["V3_RUN_ONE_YEAR"]["status"] == "HISTORICAL_EXTERNAL_SOURCE"
    assert nodes["V3_EXTERNAL_SIMULATION"]["status"] == "HISTORICAL_EXTERNAL_CONSUMER"
    assert nodes["V3_SERVER_TURN"]["status"] == "HISTORICAL_EXTERNAL_CONSUMER"
    assert nodes["V3_V2_LOADER"]["status"] == "HISTORICAL_EXTERNAL_CONSUMER"
    assert nodes["M6_ACTOR_SAFE"]["status"] == "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    assert nodes["GT0_END_TO_END"]["status"] == "TESTED_NEGATIVE"
    assert lr.code_consumer_view(state, "V3_RUN_ONE_YEAR")["current_importer"] == "NONE_VERIFIED"
    assert any(e["from"] == "V3_RUN_ONE_YEAR" and e["dependency"] == "HISTORICAL" for e in state["edges"])
    assert not any(e["from"] == "V3_RUN_ONE_YEAR" and "currently_imported" in e["relation"] for e in state["edges"])


def test_demo5_same_b_share_and_distinct_help_refuse_causes():
    state = _state()
    a = next(e for e in state["edges"] if e["from"] == "P1_LIFE_A_SHARE_ACCESS" and e["to"] == "P1_B_MATERIAL_SOURCE")
    b = next(e for e in state["edges"] if e["from"] == "P1_LIFE_B_SHARE_NO_ACCESS" and e["to"] == "P1_B_MATERIAL_SOURCE")
    assert a["relation"] == b["relation"] == "uses_same_b_share_source"
    c = next(e for e in state["edges"] if e["from"] == "P1_LIFE_C_REFUSE" and e["to"] == "P1_B_MATERIAL_SOURCE")
    assert c["relation"] == "uses_b_refusal_source"
    assert lr._node_map(state)["P1_SAME_SPEECH_DIFFERENT_CAUSE"]["status"] == "TEST_ONLY"
    assert lr._node_map(state)["P1_RETURN"]["status"] == "TEST_ONLY_SOURCEFREE_NOT_NATIVE"
    assert any(e["from"] == "P1_RETURN" and e["to"] == "CAN011_RULE_T_MISSING" for e in state["edges"])


def test_demo6_join_v_scope_acceptance_coexists_with_native_holds():
    state = _state()
    assert lr._node_map(state)["JOIN_E_7BF"]["status"] == "INDEPENDENT_ACCEPT_SCOPED"
    assert lr._node_map(state)["JOIN_V_SCOPE_ACCEPTANCE"]["status"] == "ACCEPT_SCOPED"
    assert lr._node_map(state)["JOIN_C9_HOLD"]["status"] == "HELD"
    assert lr._node_map(state)["JOIN_C12_HOLD"]["status"] == "HELD"
    node = lr._node_map(state)["JOIN_V_4387"]
    evidence = {"kind": "ACCEPTANCE_RECORD", "reviewed_sha": "7bf2da302996491ddf34b9a039fea47ac982d135", "acceptance": node["acceptance_record"]}
    ok, reason, _ = lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", evidence)
    assert ok, reason
    assert not any(e["from"] == "JOIN_E_7BF" and e["to"] == "CURRENT_V3_IMPORTER_MISSING" for e in state["edges"])


def test_demo7_rrif_f1_to_f2_repair_to_partial_consumer():
    state = _state()
    nodes = lr._node_map(state)
    assert nodes["RRIF_F1_DEFECT"]["status"] == "REVISE_ONE_EXACT_PACKET_DEFECT"
    assert nodes["RRIF_F2_REPAIR"]["status"] == "AUTHOR_TESTED_SOURCEFREE"
    assert nodes["RRIF_F2_FIRST_CONSUMER"]["status"] == "PASS_PARTIAL"
    assert nodes["RRIF_NATIVE_HOLD"]["status"] == "HELD"
    assert any(e["from"] == "RRIF_F1_DEFECT" and e["to"] == "RRIF_F2_REPAIR" for e in state["edges"])
    assert any(e["from"] == "RRIF_F2_FIRST_CONSUMER" and e["to"] == "JOIN_C9_HOLD" for e in state["edges"])


def test_demo8_withdrawal_restoration_live_and_cold(tmp_path: Path):
    journal = tmp_path / "evidence" / "journal.jsonl"
    state = lr.build_state(OBSERVED)
    b = _record(lr._node_map(state)["P1_B_MATERIAL_SOURCE"])
    a = _record(lr._node_map(state)["P1_A_ACCESS_PATH"])
    events = [
        lr._event("GENESIS", {"baseline_sha": lr.STARTUP_SHA}, created_at="2026-11-01T00:00:00+00:00"),
        lr._event("CANDIDATE_EVIDENCE", {"importer": "OSCIENCE", "patch_file": lr.OSCIENCE_PATCH.name, "patch_digest": lr._digest(lr._load(lr.OSCIENCE_PATCH)), "source_commit": lr.OSCIENCE_CUT}, created_at="2026-11-01T00:00:01+00:00"),
        lr._event("TRANSITION_REQUEST", {"fixture": {"node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND", "evidence": b}}, created_at="2026-11-01T00:00:02+00:00"),
        lr._event("TRANSITION_REQUEST", {"fixture": {"node_id": "P1_A_ACCESS_PATH", "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND", "evidence": a}}, created_at="2026-11-01T00:00:03+00:00"),
        lr._event("TRANSITION_REQUEST", {"fixture": {"node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery", "to": "SOURCE_VERIFIED", "evidence": b}}, created_at="2026-11-01T00:00:04+00:00"),
    ]
    for event in events:
        evidence_store.append_event(journal, event)
    cold = lr.rebuild_from_journal(journal, operating=True)
    assert cold["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"].startswith("INVALIDATED")
    assert cold["axes"]["Q_GAME_001"]["consumer"] == "NONE_PROVEN_AT_PREMAIN"
    again = lr.rebuild_from_journal(journal, operating=True)
    assert again["state_digest"] == cold["state_digest"]


def test_demo11_sorok101_occurrence_vs_perception_and_call_alternatives():
    state = _state()
    assert any(e["from"] == "SOROK_101_OUTWARD_OCCURRENCE" and e["to"] == "SOROK_101_USER_PHENOMENAL" for e in state["edges"])
    assert any(e["from"] == "SOROK_101_HIDDEN_INTERIORITY" and e["to"] == "SOROK_101_USER_PHENOMENAL" for e in state["edges"])
    assert any(e["from"] == "SOROK_101_TWO_CALL_PROPOSAL" and e["to"] == "SOROK_101_BATCHING_ALT" for e in state["edges"])
    assert lr._node_map(state)["SOROK_101_TWO_CALL_PROPOSAL"]["status"] == "PROPOSED"
    assert lr._node_map(state)["SOROK_101_BATCHING_ALT"]["status"] == "PROPOSED_SCOPED_ALTERNATIVE"


def test_demo12_queued_high_is_not_observed_high_and_ready_is_not_running():
    state = _state()
    nodes = lr._node_map(state)
    assert nodes["CONTROLLER_R63_QUEUE"]["status"] == "QUEUED_HIGH"
    assert nodes["CONTROLLER_R63_OBSERVED"]["status"] == "OBSERVED_LOW"
    assert nodes["CONTROLLER_R63_HOLD"]["status"] == "HELD"
    assert nodes["LIBRARY_LATEST_20261031"]["status"] == "REPORTED_NOT_ACCESSED_NOW"
    assert nodes["WORKER_BRANCH_READY"]["status"] == "PUBLISHED_NOT_LAUNCHED"
    assert nodes["WORKER_RUNNING_UNKNOWN"]["status"] == "UNKNOWN"
    assert nodes["NO_AUTO_REDISPATCH"]["status"] == "CONSTRAINT"
    assert any(e["from"] == "PREMAIN_PROGRESS_MD" and e["to"] == "PREMAIN_PROGRESS_JSON" and e["dependency"] == "STALE_CROSS_CUT" for e in state["edges"])
    assert not any(n["status"] == "RUNNING" for n in state["nodes"] if n.get("programma_p1"))


def test_maturity_lens_and_whole_program_gaps_filters():
    state = _state()
    health = lr.maturity_view(state, "Q_HEALTH_001")["stages"]
    assert health["T"]["status"] == "CONTESTED"
    can = lr.maturity_view(state, "CAN011_RULE_T_MISSING")["stages"]
    assert can["T"]["status"] == "MISSING"
    theory = lr.whole_program_gaps(state, stage="T")
    ids = {g["id"] for group in theory["groups"] for g in group["gaps"]}
    assert "GAP-Q-HEALTH-FLOURISHING" in ids
    assert "GAP-CAN011-PRACTICE-ACQUISITION" in ids
    for gap in state["p1_gap_records"]:
        for key in ("parent_obligation", "owner", "smallest_useful_next_action", "falsifier"):
            assert gap.get(key), (gap["id"], key)
    assert any(g["id"].startswith("GAP-S13") for g in state["p1_gap_records"])
    assert any(g["id"].startswith("GAP-S14") for g in state["p1_gap_records"])
    assert any(g["id"].startswith("GAP-S11") for g in state["p1_gap_records"])
    assert any(g["id"].startswith("GAP-A5") for g in state["p1_gap_records"])


def test_home_focus_lateral_and_html_actual_output(tmp_path: Path):
    state = _state()
    home = lr.home_view(state)
    assert home["whole_scope"] == "WHOLE_SCOPE_NOT_YET_PROVEN"
    assert home["kernel"] == "KERNEL_UNRESOLVED"
    assert home["terminal_obligations"]
    focus = lr.focus_view(state, "Q_HEALTH_001", 2)
    assert focus["node"]["id"] == "Q_HEALTH_001"
    assert focus["maturity"]["stages"]["T"]["status"] == "CONTESTED"
    lateral = lr.lateral_view(state, "Q_HEALTH_001")
    assert lateral["alternatives"]
    output = tmp_path / "home.html"
    path = lr.generate_html(state, output)
    text = path.read_text(encoding="utf-8")
    assert "PROGRAMMA SOROK" in text
    assert "Q_HEALTH_001" in text
    assert "GAP-Q-HEALTH-FLOURISHING" in text
    assert "WHOLE_SCOPE_NOT_YET_PROVEN" in text
