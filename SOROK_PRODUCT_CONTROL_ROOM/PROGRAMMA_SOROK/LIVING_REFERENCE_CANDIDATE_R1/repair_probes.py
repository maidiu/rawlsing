#!/usr/bin/env python3
"""Disposable probes for the PROGRAMMA SOROK P0/P1 repair boundaries."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

import evidence_store
import living_reference as lr

ROOT = Path(__file__).resolve().parent
W1A_SOURCE = {
    "commit": "e7787d7f22dfcc9dd1ad786d953755b4f4d410c7",
    "path": "WORKER_RETURNS/PROGRAMMA_SOROK_W1_A_VISION_ASTRA_R1/00_FINDINGS_AND_RECOMMENDATIONS.md",
    "blob": "b457bebf63d4ae12d01b8481481368bcd082e269",
    "object_type": "blob",
}
W1A_QUOTE = "No single technical milestone or personality description can certify it."


def _source_record(state: dict, node_id: str) -> dict:
    ref = lr._node_map(state)[node_id]["source_refs"][0]
    return {
        "kind": "SOURCE_RECORD",
        "source": {
            "commit": ref["commit"],
            "path": ref["path"],
            "blob": ref.get("blob") or ref.get("object_id"),
            "object_type": ref.get("object_type", "blob"),
        },
    }


def acceptance_probe() -> dict:
    state = lr.build_state(lr.observe_source_cut(git_enabled=False))
    record = lr._node_map(state)["JOIN_V_4387"]["acceptance_record"]
    valid = {"kind": "ACCEPTANCE_RECORD", "reviewed_sha": record["subject_sha"], "acceptance": record}
    arbitrary = copy.deepcopy(valid)
    arbitrary["acceptance"]["record_ref"] = "54013d1907e5ea55b0d1f54ea9afe07ef6388b11:WORKER_RETURNS/PROGRAMMA_SOROK_P0_P1_LIVING_REFERENCE_ENGINEERING_R1/00_RETURN.md"
    arbitrary["acceptance"]["scope"] = ["*"]
    wildcard = copy.deepcopy(valid)
    wildcard["acceptance"]["scope"] = ["*"]
    stale = copy.deepcopy(state)
    next(n for n in stale["nodes"] if n["id"] == "JOIN_E_7BF")["subject_sha"] = "f" * 40
    self_claim = copy.deepcopy(valid)
    self_claim["acceptance"]["reviewer_principal"] = self_claim["acceptance"]["author_principal"]
    return {
        "valid_existing_join_v": lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", valid)[:2],
        "arbitrary_unrelated_record": lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", arbitrary)[:2],
        "wildcard_scope": lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", wildcard)[:2],
        "unrelated_subject": lr._verify_acceptance_record(stale, "JOIN_E_7BF", "engineering", valid)[:2],
        "self_claim": lr._verify_acceptance_record(state, "JOIN_E_7BF", "engineering", self_claim)[:2],
        "join_v_does_not_certify_other_node": lr._verify_acceptance_record(state, "CP-A5-R2", "engineering", valid)[:2],
        "join_v_verification": lr._node_map(state)["JOIN_V_4387"].get("acceptance_verification"),
    }


def return_probe() -> dict:
    state = lr.build_state(lr.observe_source_cut(git_enabled=False))
    fake = lr.intake_candidate(state, {"id": "FAKE", "sha": "a" * 40, "source": W1A_SOURCE})
    mismatch = lr.intake_candidate(state, {"id": "MISMATCH", "sha": lr.ENGINEERING_BASELINE, "source": W1A_SOURCE})
    state = lr.build_state(lr.observe_source_cut(git_enabled=False))
    unlocated = lr.intake_candidate(state, {
        "id": "UNLOCATED", "sha": W1A_SOURCE["commit"], "source": W1A_SOURCE,
        "new_requirement": "W1_A_UNLOCATED_CLAIM",
        "node_updates": [{"id": "W1_A_RETURN", "evidence": {"return_sha": W1A_SOURCE["commit"]}}],
    })
    unlocated_gap = next(g for g in state["gaps"] if g["node"] == "W1_A_UNLOCATED_CLAIM")
    unlocated_work = next(c for c in state["work_now"]["candidates"] if c["gap_id"] == unlocated_gap["id"])
    unlocated_operational = state["axes"]["W1_A_RETURN"]["operational"]
    state = lr.build_state(lr.observe_source_cut(git_enabled=False))
    located = lr.intake_candidate(state, {
        "id": "LOCATED", "sha": W1A_SOURCE["commit"], "source": W1A_SOURCE,
        "new_requirement": "W1_A_LOCATED_CLAIM",
        "locator": {"path": W1A_SOURCE["path"], "quote": W1A_QUOTE},
        "node_updates": [{
            "id": "W1_A_RETURN", "evidence": {"return_sha": W1A_SOURCE["commit"]},
            "locator": {"path": W1A_SOURCE["path"], "quote": W1A_QUOTE},
        }],
    })
    located_gap = next(g for g in state["gaps"] if g["node"] == "W1_A_LOCATED_CLAIM")
    located_work = next(c for c in state["work_now"]["candidates"] if c["gap_id"] == located_gap["id"])
    return {
        "fake_repeated_a_sha": fake["status"],
        "sha_source_commit_mismatch": mismatch["status"],
        "unlocated_return": {
            "status": unlocated["status"],
            "gap_status": unlocated_gap["evidence_status"],
            "gap_source_backed": unlocated_gap["source_backed"],
            "work_now_source_backed": unlocated_work["source_backed"],
            "node_operational": unlocated_operational,
        },
        "located_return": {
            "status": located["status"],
            "gap_status": located_gap["evidence_status"],
            "gap_source_backed": located_gap["source_backed"],
            "work_now_source_backed": located_work["source_backed"],
            "node_operational": state["axes"]["W1_A_RETURN"]["operational"],
        },
    }


def withdrawal_probe() -> dict:
    with tempfile.TemporaryDirectory(prefix="sorok-repair-withdrawal-") as directory:
        root = Path(directory)
        journal = root / "evidence" / "journal.jsonl"
        state_path = root / "state.json"
        baseline = lr.build_state(lr.observe_source_cut(git_enabled=False))
        gt0 = copy.deepcopy(baseline["axes"]["GT0_END_TO_END"])
        q_game = copy.deepcopy(baseline["axes"]["Q_GAME_001"])
        b = _source_record(baseline, "P1_B_MATERIAL_SOURCE")
        a = _source_record(baseline, "P1_A_ACCESS_PATH")

        def commit(body: dict) -> dict:
            return lr.commit_event(body, journal_path=journal, state_path=state_path)

        commit(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-01T20:00:00+00:00"))
        commit(lr._event("CANDIDATE_EVIDENCE", {
            "importer": "OSCIENCE", "patch_file": lr.OSCIENCE_PATCH.name,
            "patch_digest": lr._digest(lr._load(lr.OSCIENCE_PATCH)), "source_commit": lr.OSCIENCE_CUT,
        }, created_at="2026-11-01T20:00:01+00:00"))
        for index, node_id in enumerate(("P1_B_MATERIAL_SOURCE", "P1_A_ACCESS_PATH"), start=2):
            withdrawal = commit(lr._event("EVIDENCE_WITHDRAWAL", {
                "node_id": node_id, "basis": "QUALIFIED_ABSENCE_VERIFICATION",
                "authority": "SOROK_HQ", "scope": [node_id], "reason": "qualified absence probe",
            }, created_at=f"2026-11-01T20:00:0{index}+00:00"))
            commit(lr._event("TRANSITION_REQUEST", {"fixture": {
                "node_id": node_id, "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND",
                "evidence": {
                    "kind": "SOURCE_WITHDRAWAL", "basis": "QUALIFIED_ABSENCE_VERIFICATION",
                    "authority": "SOROK_HQ", "scope": [node_id],
                    "withdrawal_event_id": withdrawal["event"]["event_id"],
                },
            }}, created_at=f"2026-11-01T20:00:0{index + 2}+00:00"))
        commit(lr._event("TRANSITION_REQUEST", {"fixture": {
            "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "review", "to": "REVIEW_FAILED",
            "evidence": {"kind": "SOURCEFREE_REVIEW", "source": b["source"], "reviewed_sha": lr.ENGINEERING_BASELINE, "review_status": "FAIL", "reviewer_role": "INDEPENDENT"},
        }}, created_at="2026-11-01T20:00:06+00:00"))
        commit(lr._event("TRANSITION_REQUEST", {"fixture": {
            "node_id": "P1_A_ACCESS_PATH", "dimension": "engineering", "to": "FAILED", "evidence": a,
        }}, created_at="2026-11-01T20:00:07+00:00"))
        commit(lr._event("TRANSITION_REQUEST", {"fixture": {
            "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery", "to": "SOURCE_VERIFIED", "evidence": b,
        }}, created_at="2026-11-01T20:00:08+00:00"))
        commit(lr._event("TRANSITION_REQUEST", {"fixture": {
            "node_id": "P1_A_ACCESS_PATH", "dimension": "source_recovery", "to": "SOURCE_VERIFIED", "evidence": a,
        }}, created_at="2026-11-01T20:00:09+00:00"))
        live = lr._load_state(state_path)
        cold = lr.rebuild_from_journal(journal, operating=True)
        return {
            "live": {
                "consumer": live["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"],
                "review": live["axes"]["P1_B_MATERIAL_SOURCE"]["review"],
                "engineering": live["axes"]["P1_A_ACCESS_PATH"]["engineering"],
                "gt0_unchanged": live["axes"]["GT0_END_TO_END"] == gt0,
                "q_game_unchanged": live["axes"]["Q_GAME_001"] == q_game,
            },
            "cold": {
                "consumer": cold["axes"]["P1_LATER_HELP_CONSUMER"]["consumer"],
                "review": cold["axes"]["P1_B_MATERIAL_SOURCE"]["review"],
                "engineering": cold["axes"]["P1_A_ACCESS_PATH"]["engineering"],
                "gt0_unchanged": cold["axes"]["GT0_END_TO_END"] == gt0,
                "q_game_unchanged": cold["axes"]["Q_GAME_001"] == q_game,
            },
            "present_source_cannot_withdraw": _present_source_probe(),
        }


def _present_source_probe() -> str:
    state = lr.build_state(lr.observe_source_cut(git_enabled=False))
    state["operating"] = True
    try:
        lr._apply_transition(state, {
            "node_id": "P1_B_MATERIAL_SOURCE", "dimension": "source_recovery",
            "to": "SOURCE_NOT_FOUND", "evidence": _source_record(state, "P1_B_MATERIAL_SOURCE"),
        })
    except ValueError as error:
        return str(error)
    return "NOT_REFUSED"


def view_probe() -> dict:
    state = lr.build_state(lr.observe_source_cut(git_enabled=False))
    home = lr.home_view(state)
    work = state["work_now"]
    ordered = sorted(work["candidates"], key=lambda c: (c["parallel_group"], c["domain"], c["gap_id"]))
    witness = state["source_verification"].get("V3_RUN_ONE_YEAR", {})
    with tempfile.TemporaryDirectory(prefix="sorok-repair-html-") as directory:
        html_path = lr.generate_html(state, Path(directory) / "home.html")
        html = html_path.read_text(encoding="utf-8")
    return {
        "home_first_keys": list(home)[:8],
        "purpose": home["purpose"]["title"],
        "experience": [home["intended_human_experience"][k]["title"] for k in ("astra_b_scene", "astra_d_longitudinal", "negative_controls")],
        "constraints": [home["constraints_100_101"][k]["title"] for k in ("alpha_100", "binding_101", "two_call_proposal", "hidden_interiority")],
        "html_purpose_before_terminal": html.index("Purpose: meet an unchosen neighbor") < html.index("Terminal obligations"),
        "work_now_no_scalar_priority": work["no_scalar_priority"],
        "work_now_sorted_by_group_domain_id": [c["gap_id"] for c in work["candidates"]] == [c["gap_id"] for c in ordered],
        "work_now_terminal_contribution_and_uncertainty": all("terminal_contribution" in c and "uncertainty" in c for c in work["candidates"]),
        "witness_status": witness.get("status"),
        "home_witness": [x["id"] for x in home.get("source_witness", [])],
        "maturity_witness": lr.maturity_view(state, "V3_RUN_ONE_YEAR").get("source_verification", {}).get("status"),
        "witness_gap": any(g["id"] == "GAP_WITNESS_V3_RUN_ONE_YEAR" for g in state["gaps"]),
        "baseline": {
            "build_startup": state["build_startup"],
            "olive_source": state["version_vector"]["olive_source"],
            "engineering_baseline": state["version_vector"]["engineering_baseline"],
        },
    }


def main() -> int:
    result = {
        "schema": "SOROK_PROGRAMMA_REPAIR_PROBES@1",
        "acceptance": acceptance_probe(),
        "return_intake": return_probe(),
        "withdrawal_restore": withdrawal_probe(),
        "views": view_probe(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
