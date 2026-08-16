from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIAGNOSTIC = ROOT / "section85/code/run_section85_diagnostic_smoke_matrix.py"


def load_diagnostic():
    spec = importlib.util.spec_from_file_location("section85_diagnostic", DIAGNOSTIC)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_legacy_v551j_ready_boolean_is_diagnostic_only(tmp_path: Path) -> None:
    diagnostic = load_diagnostic()
    root = tmp_path / "v551j"
    write_json(root / "manifest/manifest.json", {"final_status": "READY_V551J"})
    write_json(
        root / "manifest/v551j_readiness_report.json",
        {
            "ready_for_v552j_joint_evidence": True,
            "candidate_packet_count": 4,
            "certified_packet_count": 4,
        },
    )
    gate = diagnostic.current_v551j_gate(root)
    assert gate["typed_contract_valid"] is False
    assert gate["integrity_pass"] is False
    assert gate["operation_permitted"] is False
    assert gate["hook_status"] == "AWAITING_G3B_PRODUCER_HOOK"
    assert gate["candidate_packet_count"] == 4
    assert gate["certified_packet_count"] == 4


def test_typed_v551j_state_is_authoritative_independent_of_packet_cardinality(tmp_path: Path) -> None:
    diagnostic = load_diagnostic()
    root = tmp_path / "v551j"
    write_json(
        root / "manifest/manifest.json",
        {
            "contract_version": "rawlsing_pipeline_boundary_v1",
            "run_integrity_status": "PASS",
            "evidence_status": "PRESENT",
            "downstream_permission_status": "ALLOW",
            "row_counts": {"candidate": 0, "component": 0, "certified": 0},
        },
    )
    write_json(
        root / "manifest/v551j_readiness_report.json",
        {
            "candidate_packet_count": 0,
            "component_row_count": 0,
            "certified_packet_count": 0,
            "review_required_packet_count": 0,
        },
    )
    gate = diagnostic.current_v551j_gate(root)
    assert gate["typed_contract_valid"] is True
    assert gate["run_integrity_status"] == "PASS"
    assert gate["evidence_status"] == "PRESENT"
    assert gate["downstream_permission_status"] == "ALLOW"
    assert gate["operation_permitted"] is True
    assert gate["candidate_packet_count"] == 0
    assert gate["certified_packet_count"] == 0
