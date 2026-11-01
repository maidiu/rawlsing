#!/usr/bin/env python3
"""Disposable O-LIVE/R3 demonstration transaction.

Default behavior writes only inside a fresh temporary directory.  It never
writes the operating state, snapshot, canonical journal or the historical root
receipt.  Synthetic review/promotion attempts are expected to remain pending or
quarantined; they are demonstrations, not acceptance.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import living_reference as lr

ROOT = Path(__file__).resolve().parent
OPERATING_FILES = (lr.STATE, lr.SNAPSHOT, lr.JOURNAL, ROOT / "r2_live_transaction.json")


def _sha256(path: Path) -> str:
    if not path.exists():
        return "ABSENT"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def operating_hashes() -> dict:
    return {str(path.relative_to(ROOT)): _sha256(path) for path in OPERATING_FILES}


def _source_record(state: dict, node_id: str) -> dict:
    node = lr._node_map(state).get(node_id, {})
    refs = node.get("source_refs") or []
    if refs and refs[0].get("commit"):
        ref = refs[0]
        return {
            "kind": "SOURCE_RECORD",
            "source": {
                "commit": ref["commit"],
                "path": ref["path"],
                "blob": ref.get("blob") or ref.get("object_id"),
                "object_type": ref.get("object_type", "blob"),
            },
        }
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


def _self_review(state: dict, node_id: str) -> dict:
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


def run(temp: Path) -> dict:
    observed = lr.observe_source_cut(git_enabled=False)
    state = lr.build_state(observed)
    import_report = lr.ingest_oscience(state, lr._load(lr.OSCIENCE_PATCH))
    baseline_axes = copy.deepcopy(state["axes"])
    self_review = lr._apply_transition(state, {
        "node_id": "CP-A5-R2",
        "dimension": "review",
        "to": "REVIEW_PASSED_SCOPED",
        "evidence": _self_review(state, "CP-A5-R2"),
    })
    self_accept = lr._apply_transition(state, {
        "node_id": "CP-A5-R2",
        "dimension": "engineering",
        "to": "INDEPENDENT_ACCEPT_SCOPED",
        "evidence": _self_review(state, "CP-A5-R2"),
    })
    synthetic_requirement = lr.intake_candidate(state, {
        "id": "R2-LIVE-NEW-REQUIREMENT",
        "branch": "sourcefree/synthetic-requirement",
        "sha": "a" * 40,
        "new_requirement": "SOROK_R2_NEW_REQUIREMENT",
        "tests": {"passed": 1, "native": False},
        "fixture_origin": True,
    })
    source_b = _source_record(state, "P1_B_MATERIAL_SOURCE")
    source_a = _source_record(state, "P1_A_ACCESS_PATH")
    withdrawal = lr._apply_transition(state, {
        "node_id": "P1_B_MATERIAL_SOURCE",
        "dimension": "source_recovery",
        "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "disposable source disqualification"},
    })
    second_withdrawal = lr._apply_transition(state, {
        "node_id": "P1_A_ACCESS_PATH",
        "dimension": "source_recovery",
        "to": "SOURCE_NOT_FOUND",
        "evidence": {"kind": "SYNTHETIC_DEMO", "note": "second independent RED"},
    })
    second_red = copy.deepcopy(state["axes"]["P1_LATER_HELP_CONSUMER"])
    restore = lr._apply_transition(state, {
        "node_id": "P1_B_MATERIAL_SOURCE",
        "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED",
        "evidence": source_b,
    })
    second_red_after_restore = copy.deepcopy(state["axes"]["P1_LATER_HELP_CONSUMER"])
    restore_second = lr._apply_transition(state, {
        "node_id": "P1_A_ACCESS_PATH",
        "dimension": "source_recovery",
        "to": "SOURCE_VERIFIED",
        "evidence": source_a,
    })
    unrelated_after = {
        "Q_GAME_001": state["axes"]["Q_GAME_001"]["consumer"],
        "A5_human": state["axes"]["A5"]["human"],
        "S0_consumer": state["axes"]["S0"]["consumer"],
        "pyat_status": state["pyat_boundary"]["status"],
    }
    source_provenance = {"P1_A_ACCESS_PATH": source_a["source"], "P1_B_MATERIAL_SOURCE": source_b["source"]}
    state_path = temp / "state.json"
    snapshot_path = temp / "SNAPSHOT.json"
    lr._save(state, state_path, snapshot_path)
    cold = subprocess.run(
        [sys.executable, str(ROOT / "living_reference.py"), "--state", str(state_path), "export"],
        cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True, text=True)
    cold_state = json.loads(cold.stdout) if cold.returncode == 0 else {}
    tamper = copy.deepcopy(state)
    tamper_path = temp / "tampered.json"
    lr._save(tamper, tamper_path)
    tampered_text = tamper_path.read_text(encoding="utf-8").replace(str(tamper["nodes"][0]["title"]), "TAMPERED", 1)
    tamper_path.write_text(tampered_text, encoding="utf-8")
    tamper_detected = None
    try:
        lr._load_state(tamper_path)
    except lr.TamperedState as error:
        tamper_detected = str(error)
    receipt = {
        "schema": "SOROK_OLIVE_R3_DISPOSABLE_DEMO@1",
        "mode": "DISPOSABLE_TEMP_ONLY",
        "baseline": {"nodes": lr.BASE_NODE_COUNT, "edges": lr.BASE_EDGE_COUNT},
        "oscience_import": import_report,
        "self_declared_review": {
            "review_status": self_review["status"],
            "engineering_status": self_accept["status"],
            "review_axis_unchanged": state["axes"]["CP-A5-R2"]["review"] == baseline_axes["CP-A5-R2"]["review"],
            "engineering_axis_unchanged": state["axes"]["CP-A5-R2"]["engineering"] == baseline_axes["CP-A5-R2"]["engineering"],
            "promotion_pending": self_review["status"] == "PENDING_INDEPENDENT_ACCEPTANCE" and self_accept["status"] == "PENDING_INDEPENDENT_ACCEPTANCE",
        },
        "synthetic_requirement": {
            "status": synthetic_requirement["status"],
            "operating_gap_created": synthetic_requirement["status"] != "QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE",
        },
        "source_withdrawal": {
            "status": withdrawal["status"],
            "invalidated": withdrawal["invalidated"],
            "second_independent_red": second_red,
        },
        "source_restore": {
            "status": restore["status"],
            "restored": restore["restored"],
            "second_red_preserved": str(second_red_after_restore["consumer"]).startswith("INVALIDATED"),
            "second_restore": restore_second["status"],
            "unrelated_after": unrelated_after,
        },
        "source_provenance": source_provenance,
        "cold_readback": {
            "exit_code": cold.returncode,
            "state_digest_equal": cold_state.get("state_digest") == state["state_digest"],
            "nodes": len(cold_state.get("nodes", [])),
            "edges": len(cold_state.get("edges", [])),
        },
        "tamper": {"detected": tamper_detected},
        "receipt_path": str(temp / "r2_live_transaction.json"),
        "operating_files_written": False,
    }
    (temp / "r2_live_transaction.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    before = operating_hashes()
    with tempfile.TemporaryDirectory(prefix="sorok-olive-r3-demo-") as directory:
        receipt = run(Path(directory))
    after = operating_hashes()
    result = {
        "receipt": receipt,
        "operating_files_before": before,
        "operating_files_after": after,
        "operating_files_unchanged": before == after,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if before == after else 1


def demo_isolation() -> dict:
    before = operating_hashes()
    with tempfile.TemporaryDirectory(prefix="sorok-olive-r3-isolation-") as directory:
        receipt = run(Path(directory))
    after = operating_hashes()
    return {
        "demo": receipt,
        "operating_files_before": before,
        "operating_files_after": after,
        "operating_files_unchanged": before == after,
        "result": "PASS" if before == after else "FAIL",
    }


if __name__ == "__main__":
    raise SystemExit(main())
