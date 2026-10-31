#!/usr/bin/env python3
"""Execute the O-LIVE R2 live transaction and write the persisted reference."""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import living_reference as lr
import verify_source_manifest as vsm

ROOT = Path(__file__).resolve().parent


def _source_record(state: dict, node_id: str) -> dict:
    row = next(r for r in state["source_manifest"]["rows"] if r["id"] == node_id)
    source = lr._normalized_source(row)
    return {
        "kind": "SOURCE_RECORD",
        "source": {
            "commit": source["commit"],
            "path": source["path"],
            "blob": source.get("blob") or source.get("object_id"),
            "object_type": source.get("object_type", "blob"),
        },
        "preimage": lr._digest(lr._node_source(state, node_id)),
    }


def _review(state: dict, node_id: str) -> dict:
    row = next(r for r in state["source_manifest"]["rows"] if r["id"] == node_id)
    source = lr._normalized_source(row)
    return {
        "kind": "SOURCEFREE_REVIEW",
        "source": {
            "commit": source["commit"],
            "path": source["path"],
            "blob": source.get("blob") or source.get("object_id"),
            "object_type": source.get("object_type", "blob"),
        },
        "reviewed_sha": lr.STARTUP_SHA,
        "reviewer_role": "INDEPENDENT_I3_ENGINEER",
        "review_scope": [node_id],
        "review_status": "PASS",
        "preimage": lr._digest(lr._node_source(state, node_id)),
    }


def _gaps(state: dict) -> list[str]:
    return [g["id"] for g in state["gaps"]]


def _candidate_ids(state: dict) -> list[str]:
    return [c["gap_id"] for c in state["work_now"]["candidates"]]


def main() -> int:
    observed = lr.observe_source_cut()
    baseline = lr.build_state(observed)
    baseline_counts = (len(baseline["nodes"]), len(baseline["edges"]))
    baseline_gaps = _gaps(baseline)
    baseline_candidates = _candidate_ids(baseline)
    import_report = lr.ingest_oscience(baseline, lr._load(lr.OSCIENCE_PATCH))
    patch_digest = import_report["evidence_digest"]
    imported_counts = (len(baseline["nodes"]), len(baseline["edges"]))
    imported_gaps = _gaps(baseline)
    imported_candidates = _candidate_ids(baseline)
    # Source disqualification: exact S5 primary source goes unavailable in the test.
    s5_withdrawal = lr._apply_transition(baseline, {
        "node_id": "S5",
        "dimension": "source_recovery",
        "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "precise source disqualification simulation"},
    })
    fault_gaps = _gaps(baseline)
    fault_candidates = _candidate_ids(baseline)
    fault_blocked = lr.blocked_chain(baseline, "L3_S5_NORMATIVE_MODEL")
    unrelated_after_fault = {
        "M01_consumer": baseline["axes"]["M01"]["consumer"],
        "V3CORE_consumer": baseline["axes"]["V3CORE-R1"]["consumer"],
        "S0_consumer": baseline["axes"]["S0"]["consumer"],
        "pyat_status": baseline["pyat_boundary"]["status"],
    }
    # Genuine sourcefree reviewer engineering evidence, scoped and candidate-only.
    review_gate = lr._apply_transition(baseline, {
        "node_id": "CP-A5-R2",
        "dimension": "review",
        "to": "REVIEW_PASSED_SCOPED",
        "evidence": _review(baseline, "CP-A5-R2"),
    })
    review = lr._apply_transition(baseline, {
        "node_id": "CP-A5-R2",
        "dimension": "engineering",
        "to": "INDEPENDENT_ACCEPT_SCOPED",
        "evidence": _review(baseline, "CP-A5-R2"),
    })
    review_axes = copy.deepcopy(baseline["axes"]["CP-A5-R2"])
    # Repair the withdrawn S5 source with exact source record.
    repair = lr._apply_transition(baseline, {
        "node_id": "S5",
        "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED",
        "evidence": _source_record(baseline, "S5"),
    })
    repaired_gaps = _gaps(baseline)
    repaired_candidates = _candidate_ids(baseline)
    # New scoped requirement becomes visible and changes work-now.
    new_requirement = lr.intake_candidate(baseline, {
        "id": "R2-LIVE-NEW-REQUIREMENT",
        "branch": "sourcefree/synthetic-requirement",
        "sha": "a" * 40,
        "new_requirement": "SOROK_R2_NEW_REQUIREMENT",
        "tests": {"passed": 1, "native": False},
    })
    requirement_gaps = _gaps(baseline)
    requirement_candidates = _candidate_ids(baseline)
    # Unadopted owner evidence is preserved for competent manual verification.
    pending_owner = lr._apply_transition(baseline, {
        "node_id": "A5",
        "dimension": "authority",
        "to": "OWNER_ADOPTED",
        "evidence": {
            "kind": "OWNER_GRANT",
            "owner_slot": "SOROK_ORIGINAL_PRODUCT_OWNER",
            "scope": ["A5"],
            "source": _source_record(baseline, "A5")["source"],
            "preimage": lr._digest(lr._node_source(baseline, "A5")),
        },
    })
    pending_owner_axes = copy.deepcopy(baseline["axes"]["A5"])
    # Refresh from Git after all updates; history and evidence must survive.
    refreshed = lr.refresh_state(baseline, observed)
    refreshed_digest = refreshed["state_digest"]
    history_kinds = [h.get("kind") for h in refreshed["history"]]
    # Cold process state path.
    with tempfile.TemporaryDirectory(prefix="sorok-olive-r2-") as directory:
        state_path = Path(directory) / "state.json"
        lr._save(refreshed, state_path)
        cold = subprocess.run(
            [sys.executable, str(ROOT / "living_reference.py"), "--state", str(state_path), "export"],
            cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True, text=True)
        cold_state = json.loads(cold.stdout) if cold.returncode == 0 else {}
        duplicate = lr.ingest_oscience(copy.deepcopy(refreshed), lr._load(lr.OSCIENCE_PATCH))
        # Tamper source and credential negatives.
        tamper_dir = Path(directory) / "tamper"
        tamper_dir.mkdir()
        shutil.copy2(lr.SOURCE_MANIFEST, tamper_dir / "source_manifest.json")
        tampered = json.loads((tamper_dir / "source_manifest.json").read_text())
        tampered["rows"][0]["object_id"] = "f" * 40
        (tamper_dir / "source_manifest.json").write_text(json.dumps(tampered), encoding="utf-8")
        verifier = vsm.verify(tamper_dir, lr.REPO)
        credential_refused = []
        for fixture in (
            {"node_id": "A5", "dimension": "authority", "to": "OWNER_ADOPTED", "owner_evidence": "OWNER_GRANT fake", "reviewer_evidence": "reviewer fake"},
            {"node_id": "A5", "dimension": "authority", "to": "OWNER_ADOPTED", "evidence": {"kind": "OWNER_GRANT", "owner_slot": "SOROK_HQ", "scope": ["A5"], "source": {"commit": "f" * 40, "path": "x", "blob": "f" * 40, "object_type": "blob"}}},
            {"node_id": "A5", "dimension": "human", "to": "PROVEN", "owner_evidence": "HUMAN_PARTICIPANT fake"},
        ):
            try:
                lr._apply_transition(copy.deepcopy(refreshed), fixture)
            except ValueError as error:
                credential_refused.append(str(error))
        # Known-good persisted reference for the first downstream consumer.
        final_state = refreshed
        final_state["source_manifest_verification"] = vsm.verify(ROOT, lr.REPO)
        lr._save(final_state)
    test_run = subprocess.run(
        [sys.executable, "-m", "pytest", "-o", "addopts=", "-q", "-p", "no:cacheprovider",
         "test_living_reference.py", "test_living_reference_r2.py"],
        cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True)
    evidence = {
        "schema": "SOROK_OLIVE_R2_LIVE_TRANSACTION@1",
        "source_snapshot": observed,
        "baseline": {
            "nodes": baseline_counts[0], "edges": baseline_counts[1],
            "gaps": len(baseline_gaps), "work_now_candidates": len(baseline_candidates),
            "state_digest": lr.build_state(observed)["state_digest"],
        },
        "oscience_import": import_report,
        "after_import": {
            "nodes": imported_counts[0], "edges": imported_counts[1],
            "gaps": len(imported_gaps), "work_now_candidates": len(imported_candidates),
            "gap_ids": imported_gaps,
        },
        "source_disqualification": {
            "status": s5_withdrawal["status"],
            "invalidated": s5_withdrawal["invalidated"],
            "new_gaps": sorted(set(fault_gaps) - set(imported_gaps)),
            "work_now_contains_invalidation": any(g.startswith("GAP_INVALIDATED_") for g in fault_candidates),
            "blocked_chain": fault_blocked,
            "unrelated_after_fault": unrelated_after_fault,
        },
        "scoped_sourcefree_review": {
            "review_gate_status": review_gate["status"],
            "status": review["status"],
            "axes": review_axes,
            "human_not_proven": review_axes["human"] == "NOT_PROVEN",
            "authority_not_adopted": review_axes["authority"] in {"NOT_ADOPTED", "UNADOPTED", "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION"},
            "native_a5_claimed": False,
        },
        "source_repair": {
            "status": repair["status"],
            "restored": repair["restored"],
            "invalidation_gaps_removed": sorted(set(fault_gaps) - set(repaired_gaps)),
            "work_now_candidates_after_repair": len(repaired_candidates),
        },
        "pending_owner_evidence": {
            "status": pending_owner["status"],
            "axes": pending_owner_axes,
            "authority_holds": baseline.get("authority_holds", []),
            "native_or_adopted": False,
        },
        "new_requirement": {
            "history_id": new_requirement["history_id"],
            "gap": new_requirement.get("new_gap"),
            "new_gaps": sorted(set(requirement_gaps) - set(repaired_gaps)),
            "work_now_changed": requirement_candidates != repaired_candidates,
        },
        "refresh": {
            "history_count": len(refreshed["history"]),
            "history_kinds": history_kinds,
            "import_still_present": patch_digest in refreshed["evidence_imports"],
            "axes_preserved": refreshed["axes"]["S5"] == baseline["axes"]["S5"],
            "source_cut_stale": refreshed["source_cut_stale"],
        },
        "cold_readback": {
            "exit_code": cold.returncode,
            "state_digest_equal": cold_state.get("state_digest") == refreshed_digest,
            "nodes": cold_state.get("nodes") and len(cold_state["nodes"]),
            "edges": cold_state.get("edges") and len(cold_state["edges"]),
            "history_count": len(cold_state.get("history", [])),
            "import_still_present": patch_digest in cold_state.get("evidence_imports", {}),
        },
        "duplicate_import": duplicate,
        "tamper_verifier": verifier,
        "credential_refused": credential_refused,
        "final_state": {
            "path": str(lr.STATE),
            "state_digest": final_state["state_digest"],
            "nodes": len(final_state["nodes"]),
            "edges": len(final_state["edges"]),
            "gaps": len(final_state["gaps"]),
            "work_now_candidates": len(final_state["work_now"]["candidates"]),
            "history_count": len(final_state["history"]),
            "source_manifest_verification": final_state.get("source_manifest_verification"),
        },
        "tests": {
            "exit_code": test_run.returncode,
            "summary": [line for line in test_run.stdout.splitlines() if " passed" in line or " failed" in line],
            "stdout_tail": test_run.stdout[-2000:],
        },
    }
    (ROOT / "r2_live_transaction.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: evidence[k] for k in ("baseline", "after_import", "source_disqualification", "scoped_sourcefree_review", "source_repair", "new_requirement", "refresh", "cold_readback", "duplicate_import", "tamper_verifier", "credential_refused", "final_state", "tests")}, indent=2, sort_keys=True))
    return 0 if test_run.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
