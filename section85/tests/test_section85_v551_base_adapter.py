from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
DIAGNOSTIC = ROOT / "section85/code/run_section85_diagnostic_smoke_matrix.py"


def load_diagnostic():
    spec = importlib.util.spec_from_file_location("section85_diagnostic", DIAGNOSTIC)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_section85_patch_uses_exact_v551_v3_cli() -> None:
    diagnostic = load_diagnostic()
    calls: list[dict] = []

    def invoke(cmd, timeout_sec, config):
        calls.append({"cmd": cmd, "timeout_sec": timeout_sec, "config": config})
        return {"exit_code": 0}

    impl = SimpleNamespace(
        _abs=lambda path, config: f"/repo/{path}",
        _invoke_run=invoke,
        run_v551=lambda *args, **kwargs: {"exit_code": 99},
        summarize_v551_functional_gate=lambda path: {},
        summarize_v551j_functional_gate=lambda path: {},
        summarize_v552j_functional_gate=lambda path: {},
    )
    base = SimpleNamespace(_impl=impl, run_wave=lambda *args, **kwargs: {"passed": True})
    diagnostic._patch_base_module(base)

    result = impl.run_v551(
        "GSS_2010_US",
        "/tmp/v551_bridge_index.parquet",
        "/tmp/question_use_contract.parquet",
        "/tmp/response_option_map.parquet",
        "/tmp/v551",
        object(),
    )
    assert result["exit_code"] == 0
    cmd = calls[0]["cmd"]
    assert cmd[1].endswith("data/ddm_build_copy/compile_v551_relation_evidence_atoms.py")
    assert cmd[cmd.index("--run-id") + 1] == "GSS_2010_US"
    assert cmd[cmd.index("--bridge-path") + 1] == "/tmp/v551_bridge_index.parquet"
    assert cmd[cmd.index("--output-root") + 1] == "/tmp/v551"
    assert cmd[cmd.index("--v551-compile-mode") + 1] == "canonical"
    assert "--question-use-contract-path" not in cmd
    assert "--response-option-map-path" not in cmd
    assert "--v551-audit-mode" not in cmd
    assert "--no-write-csv" not in cmd


def test_v551_zero_atoms_preserves_integrity_but_denies_evidence_operation(tmp_path: Path) -> None:
    diagnostic = load_diagnostic()
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "contract_version": "rawlsing_pipeline_boundary_v1",
                "schema_version": "v3.0",
                "run_integrity_status": "PASS",
                "evidence_status": "APPLICABLE_UNRESOLVED",
                "downstream_permission_status": "DENY",
                "candidate_count": 3,
                "atom_count": 0,
            }
        ),
        encoding="utf-8",
    )

    diagnostic.verify_v551_artifact_files = lambda payload, root: {
        "contract_version": "rawlsing_pipeline_boundary_v1",
        "schema_version": "v3.0",
        "run_integrity_status": "PASS",
        "evidence_status": "APPLICABLE_UNRESOLVED",
        "downstream_permission_status": "DENY",
        "integrity_pass": True,
        "operation_permitted": False,
        "verified_artifacts": {
            "relation_evidence_atoms": {
                "path": str(tmp_path / "relation_evidence_atoms.parquet"),
                "row_count": 0,
                "artifact_file_sha256": "a" * 64,
            }
        },
    }

    gate = diagnostic.summarize_v551_functional_gate(manifest_path)
    assert gate["run_integrity_status"] == "PASS"
    assert gate["integrity_pass"] is True
    assert gate["atom_rows"] == 0
    assert gate["atom_row_count_is_integrity_gate"] is False
    assert gate["operation_permitted"] is False
    assert gate["passed"] is False
    assert gate["failure_reason"] == "v551_evidence_permission:APPLICABLE_UNRESOLVED/DENY"


def test_wave_result_keeps_integrity_pass_distinct_from_evidence_permission() -> None:
    diagnostic = load_diagnostic()
    result = diagnostic._normalize_typed_wave_result(
        {
            "passed": False,
            "failure_stage": "v551_gate",
            "functional_failure_reason": "v551_evidence_permission:APPLICABLE_UNRESOLVED/DENY",
            "functional_checks": {
                "v551": {
                    "integrity_pass": True,
                    "operation_permitted": False,
                    "evidence_status": "APPLICABLE_UNRESOLVED",
                    "downstream_permission_status": "DENY",
                }
            },
        }
    )
    assert result["passed"] is False
    assert result["run_integrity_status"] == "PASS"
    assert result["evidence_operation_status"] == "NOT_PERMITTED"
    assert result["typed_outcome"] == "INTEGRITY_PASS_EVIDENCE_OPERATION_NOT_PERMITTED"
    assert result["failure_stage"] == "typed_evidence_permission_gate"
