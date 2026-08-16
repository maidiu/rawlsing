#!/usr/bin/env python3
"""Typed-state entrypoint for the bounded Section 85 diagnostic smoke matrix.

The pre-G2 diagnostic implementation is preserved byte-for-byte in
`_legacy_run_section85_diagnostic_smoke_matrix.py` so its inventory, privacy,
packaging and database-diagnostic behavior does not drift during W01-B. This
entrypoint replaces only Section85's obsolete producer-consumer assumptions:
V551 uses the frozen G2 v3.0 CLI/manifest/artifact contract, while V551J and
V552J use the shared typed boundary and fail closed until their final producer
hooks merge.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from section85_typed_state import typed_stage_gate, verify_v551_artifact_files  # noqa: E402

LEGACY_IMPLEMENTATION = CODE_DIR / "_legacy_run_section85_diagnostic_smoke_matrix.py"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _typed_operation_summary(payload: dict[str, Any], *, stage: str) -> dict[str, Any]:
    typed = typed_stage_gate(payload, stage=stage)
    passed = bool(typed["typed_contract_valid"] and typed["integrity_pass"] and typed["operation_permitted"])
    if not typed["typed_contract_valid"]:
        reason = typed.get("failure_reason", f"{stage}_typed_contract_invalid")
    elif not typed["integrity_pass"]:
        reason = f"{stage}_run_integrity_failed"
    elif not typed["operation_permitted"]:
        reason = (
            f"{stage}_evidence_permission:"
            f"{typed['evidence_status']}/{typed['downstream_permission_status']}"
        )
    else:
        reason = ""
    return {**typed, "passed": passed, "failure_reason": reason}


def summarize_v551_functional_gate(path: str | Path) -> dict[str, Any]:
    """Section85 V551 v3.0 gate: bytes/integrity first, typed evidence second."""
    manifest_path = Path(path)
    payload = _load_json(manifest_path)
    if not payload:
        return {
            "manifest_path": str(manifest_path),
            "manifest_exists": manifest_path.exists(),
            "run_integrity_status": "FAIL",
            "evidence_status": "APPLICABLE_UNRESOLVED",
            "downstream_permission_status": "DENY",
            "integrity_pass": False,
            "operation_permitted": False,
            "candidate_bridge_rows": 0,
            "atom_rows": 0,
            "passed": False,
            "failure_reason": "missing_v551_manifest",
        }
    try:
        contract = verify_v551_artifact_files(payload, manifest_path.parent)
    except Exception as exc:
        return {
            "manifest_path": str(manifest_path),
            "manifest_exists": manifest_path.exists(),
            "run_integrity_status": "FAIL",
            "evidence_status": str(payload.get("evidence_status") or "APPLICABLE_UNRESOLVED"),
            "downstream_permission_status": "DENY",
            "integrity_pass": False,
            "operation_permitted": False,
            "candidate_bridge_rows": int(payload.get("candidate_count") or 0),
            "atom_rows": int(payload.get("atom_count") or 0),
            "passed": False,
            "failure_reason": f"v551_producer_contract_or_artifact_integrity:{exc}",
        }

    verified_atoms = contract["verified_artifacts"]["relation_evidence_atoms"]
    passed = bool(contract["integrity_pass"] and contract["operation_permitted"])
    if not contract["integrity_pass"]:
        reason = "v551_run_integrity_failed"
    elif not contract["operation_permitted"]:
        reason = (
            "v551_evidence_permission:"
            f"{contract['evidence_status']}/{contract['downstream_permission_status']}"
        )
    else:
        reason = ""
    return {
        "manifest_path": str(manifest_path),
        "manifest_exists": True,
        "contract_version": contract["contract_version"],
        "schema_version": contract["schema_version"],
        "run_integrity_status": contract["run_integrity_status"],
        "evidence_status": contract["evidence_status"],
        "downstream_permission_status": contract["downstream_permission_status"],
        "integrity_pass": contract["integrity_pass"],
        "operation_permitted": contract["operation_permitted"],
        "candidate_bridge_rows": int(payload.get("candidate_count") or 0),
        "atom_rows": int(verified_atoms.get("row_count") or 0),
        "atom_row_count_is_integrity_gate": False,
        "verified_artifacts": contract["verified_artifacts"],
        "passed": passed,
        "failure_reason": reason,
    }


def current_v551j_gate(v551j_root: Path) -> dict[str, Any]:
    """Consume only typed V551J producer state as executable acceptance.

    Legacy counts and validation reports remain diagnostic context. They cannot
    establish run integrity or downstream permission. Until W03-B merges a
    rawlsing_pipeline_boundary_v1 V551J manifest, this gate fails closed with an
    explicit G3B hook requirement.
    """
    manifest = _load_json(v551j_root / "manifest/manifest.json")
    readiness = _load_json(v551j_root / "manifest/v551j_readiness_report.json")
    validation = _load_json(v551j_root / "manifest/v551j_packet_contract_validation_report.json")
    typed = _typed_operation_summary(manifest, stage="v551j")

    candidate_count = readiness.get("candidate_packet_count", manifest.get("row_counts", {}).get("candidate", 0))
    component_count = readiness.get("component_row_count", manifest.get("row_counts", {}).get("component", 0))
    certified_count = readiness.get("certified_packet_count", manifest.get("row_counts", {}).get("certified", 0))
    issues_json = validation.get("issues_json", "[]")
    return {
        **typed,
        "hook_status": "ACTIVE_TYPED_PRODUCER_CONTRACT" if typed["typed_contract_valid"] else "AWAITING_G3B_PRODUCER_HOOK",
        "candidate_packet_count": candidate_count,
        "component_row_count": component_count,
        "certified_packet_count": certified_count,
        "certified_packet_rows": certified_count,
        "review_required_packet_count": readiness.get("review_required_packet_count", 0),
        "blocked_packet_count": readiness.get("blocked_packet_count", 0),
        "issues_json": issues_json,
        "legacy_diagnostics": {
            "final_status": readiness.get("final_status") or manifest.get("final_status", ""),
            "candidate_contract_valid": readiness.get("candidate_contract_valid", validation.get("candidate_contract_valid", False)),
            "component_contract_valid": readiness.get("component_contract_valid", validation.get("component_contract_valid", False)),
            "issues_json": issues_json,
        },
    }


def summarize_v551j_functional_gate(root: str | Path) -> dict[str, Any]:
    return current_v551j_gate(Path(root))


def summarize_v552j_functional_gate(path: str | Path) -> dict[str, Any]:
    readiness_path = Path(path)
    typed = _typed_operation_summary(_load_json(readiness_path), stage="v552j")
    return {
        **typed,
        "readiness_path": str(readiness_path),
        "readiness_exists": readiness_path.exists(),
        "status": (
            f"{typed['run_integrity_status']}/"
            f"{typed['evidence_status']}/"
            f"{typed['downstream_permission_status']}"
        ),
        "hook_status": "ACTIVE_TYPED_PRODUCER_CONTRACT" if typed["typed_contract_valid"] else "AWAITING_G4_PRODUCER_HOOK",
    }


def _patch_base_module(base):
    """Patch only the module instance loaded by Section85; never mutate W05 source."""
    impl = getattr(base, "_impl", None)
    if impl is None:
        raise RuntimeError("SECTION85_BASE_SMOKE_IMPLEMENTATION_MODULE_MISSING")

    def run_v551_v3(
        shard_id: str,
        bridge_path: str,
        quc_path: str,
        response_map_path: str,
        output_root: str,
        config,
    ) -> dict[str, Any]:
        del quc_path, response_map_path  # V551 v3.0 consumes the frozen bridge contract directly.
        cmd = [
            sys.executable,
            impl._abs("data/ddm_build_copy/compile_v551_relation_evidence_atoms.py", config),
            "--run-id", shard_id,
            "--bridge-path", bridge_path,
            "--output-root", output_root,
            "--v551-compile-mode", "canonical",
        ]
        return impl._invoke_run(cmd, timeout_sec=1800, config=config)

    impl.run_v551 = run_v551_v3
    impl.summarize_v551_functional_gate = summarize_v551_functional_gate
    impl.summarize_v551j_functional_gate = summarize_v551j_functional_gate
    impl.summarize_v552j_functional_gate = summarize_v552j_functional_gate
    base.run_v551 = run_v551_v3
    base.summarize_v551_functional_gate = summarize_v551_functional_gate
    base.summarize_v551j_functional_gate = summarize_v551j_functional_gate
    base.summarize_v552j_functional_gate = summarize_v552j_functional_gate
    return base


def load_implementation():
    spec = importlib.util.spec_from_file_location("section85_diagnostic_legacy", LEGACY_IMPLEMENTATION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"SECTION85_DIAGNOSTIC_IMPLEMENTATION_UNLOADABLE:{LEGACY_IMPLEMENTATION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    original_load_base = module.load_base

    def typed_load_base(repo_root: Path):
        return _patch_base_module(original_load_base(repo_root))

    module.load_base = typed_load_base
    module.current_v551j_gate = current_v551j_gate
    return module


def main() -> int:
    return int(load_implementation().main())


if __name__ == "__main__":
    raise SystemExit(main())
