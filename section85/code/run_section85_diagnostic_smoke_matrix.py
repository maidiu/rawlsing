#!/usr/bin/env python3
"""G4 exact-producer entrypoint for the bounded Section 85 diagnostic matrix.

The pre-G2 diagnostic implementation remains delegated to
`_legacy_run_section85_diagnostic_smoke_matrix.py` for inventory, privacy,
packaging and database diagnostics.  Section85 overrides only its owned
producer-consumer boundary: V551 stays on the resolved v3 contract, while
V551J and V552J now bind the exact G4 producer versions, scope identity,
manifest-declared canonical Parquet bytes and serialized SHA-256 values.
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

from section85_exact_producer_state import (  # noqa: E402
    V551J_COMPILER_VERSION,
    V551J_SCHEMA_VERSION,
    V552J_COMPILER_VERSION,
    V552J_SCHEMA_VERSION,
    exact_producer_gate,
)
from section85_typed_state import verify_v551_artifact_files  # noqa: E402

LEGACY_IMPLEMENTATION = CODE_DIR / "_legacy_run_section85_diagnostic_smoke_matrix.py"
_ACTIVE_EXPECTED_IDENTITY: dict[str, str] | None = None


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _exact_operation_summary(
    manifest_path: str | Path,
    *,
    stage: str,
    expected_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    typed = exact_producer_gate(
        manifest_path,
        stage=stage,
        expected_identity=expected_identity,
    )
    passed = bool(
        typed.get("typed_contract_valid")
        and typed.get("integrity_pass")
        and typed.get("operation_permitted")
    )
    if not typed.get("typed_contract_valid"):
        reason = typed.get("failure_reason", f"{stage}_exact_producer_contract_invalid")
    elif not typed.get("integrity_pass"):
        reason = f"{stage}_run_integrity_failed"
    elif not typed.get("operation_permitted"):
        reason = (
            f"{stage}_evidence_permission:"
            f"{typed.get('evidence_status', '')}/{typed.get('downstream_permission_status', '')}"
        )
    else:
        reason = ""
    return {**typed, "passed": passed, "failure_reason": reason}


def summarize_v551_functional_gate(path: str | Path) -> dict[str, Any]:
    """Preserve the already-resolved Section85 V551 v3.0 boundary."""
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
    reason = ""
    if not contract["integrity_pass"]:
        reason = "v551_run_integrity_failed"
    elif not contract["operation_permitted"]:
        reason = (
            "v551_evidence_permission:"
            f"{contract['evidence_status']}/{contract['downstream_permission_status']}"
        )
    return {
        "manifest_path": str(manifest_path),
        "manifest_exists": True,
        "contract_version": contract["contract_version"],
        "schema_version": contract["schema_version"],
        "compiler_version": contract.get("compiler_version", ""),
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


def current_v551j_gate(
    v551j_root: Path,
    *,
    expected_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Exact V551J v2.2.3 producer gate; legacy reports are diagnostics only."""
    manifest_path = v551j_root / "manifest" / "manifest.json"
    readiness = _load_json(v551j_root / "manifest" / "v551j_readiness_report.json")
    validation = _load_json(v551j_root / "manifest" / "v551j_packet_contract_validation_report.json")
    typed = _exact_operation_summary(
        manifest_path,
        stage="v551j",
        expected_identity=expected_identity or _ACTIVE_EXPECTED_IDENTITY,
    )
    manifest = _load_json(manifest_path)
    row_counts = manifest.get("row_counts", {}) if isinstance(manifest.get("row_counts"), dict) else {}
    candidate_count = readiness.get("candidate_packet_count", row_counts.get("candidate", 0))
    component_count = readiness.get("component_row_count", row_counts.get("component", 0))
    certified_count = readiness.get("certified_packet_count", row_counts.get("certified", 0))
    issues_json = validation.get("issues_json", "[]")
    return {
        **typed,
        "hook_status": "ACTIVE_G4_EXACT_PRODUCER_CONTRACT",
        "expected_schema_version": V551J_SCHEMA_VERSION,
        "expected_compiler_version": V551J_COMPILER_VERSION,
        "candidate_packet_count": candidate_count,
        "component_row_count": component_count,
        "certified_packet_count": certified_count,
        "certified_packet_rows": certified_count,
        "review_required_packet_count": readiness.get("review_required_packet_count", 0),
        "blocked_packet_count": readiness.get("blocked_packet_count", 0),
        "issues_json": issues_json,
        "legacy_diagnostics": {
            "final_status": readiness.get("final_status") or manifest.get("final_status", ""),
            "ready_for_review": readiness.get("ready_for_review"),
            "ready_for_v552j_joint_evidence": readiness.get("ready_for_v552j_joint_evidence"),
            "candidate_contract_valid": readiness.get(
                "candidate_contract_valid", validation.get("candidate_contract_valid", False)
            ),
            "component_contract_valid": readiness.get(
                "component_contract_valid", validation.get("component_contract_valid", False)
            ),
            "issues_json": issues_json,
        },
    }


def summarize_v551j_functional_gate(root: str | Path) -> dict[str, Any]:
    return current_v551j_gate(Path(root))


def _v552j_manifest_from_gate_path(path: str | Path) -> Path:
    supplied = Path(path)
    if supplied.name == "manifest.json" and supplied.parent.name != "manifest":
        return supplied
    if supplied.parent.name == "manifest":
        return supplied.parent.parent / "manifest.json"
    if supplied.is_dir():
        return supplied / "manifest.json"
    return supplied.parent / "manifest.json"


def summarize_v552j_functional_gate(
    path: str | Path,
    *,
    expected_identity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest_path = _v552j_manifest_from_gate_path(path)
    typed = _exact_operation_summary(
        manifest_path,
        stage="v552j",
        expected_identity=expected_identity or _ACTIVE_EXPECTED_IDENTITY,
    )
    return {
        **typed,
        "manifest_path": str(manifest_path),
        "manifest_exists": manifest_path.exists(),
        "status": (
            f"{typed.get('run_integrity_status', '')}/"
            f"{typed.get('evidence_status', '')}/"
            f"{typed.get('downstream_permission_status', '')}"
        ),
        "hook_status": "ACTIVE_G4_EXACT_PRODUCER_CONTRACT",
        "expected_schema_version": V552J_SCHEMA_VERSION,
        "expected_compiler_version": V552J_COMPILER_VERSION,
        "observed_zero_count": typed.get("observed_zero_count", 0),
        "measurement_state": typed.get("measurement_state", typed.get("evidence_status", "")),
    }


def _normalize_typed_wave_result(result: dict[str, Any]) -> dict[str, Any]:
    """Keep producer integrity distinct from evidence-operation permission."""
    failure_stage = str(result.get("failure_stage") or "")
    check_name = {
        "v551_gate": "v551",
        "v551j_gate": "v551j",
        "v552j_gate": "v552j",
    }.get(failure_stage)
    if not check_name:
        if result.get("passed"):
            result.setdefault("run_integrity_status", "PASS")
        return result

    gate = (result.get("functional_checks") or {}).get(check_name) or {}
    if gate.get("integrity_pass") is True and gate.get("operation_permitted") is False:
        result["run_integrity_status"] = "PASS"
        result["evidence_status"] = gate.get("evidence_status", "")
        result["downstream_permission_status"] = gate.get("downstream_permission_status", "")
        result["evidence_operation_status"] = "NOT_PERMITTED"
        result["typed_outcome"] = "INTEGRITY_PASS_EVIDENCE_OPERATION_NOT_PERMITTED"
        result["failure_stage"] = "typed_evidence_permission_gate"
    elif gate.get("integrity_pass") is False:
        result["run_integrity_status"] = "FAIL"
    return result


def _patch_base_module(base):
    """Patch only the module instance loaded by Section85; W05 source is untouched."""
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
        # Preserved W01-B adapter.  This is not expanded into W05-final work.
        del quc_path, response_map_path
        cmd = [
            sys.executable,
            impl._abs("data/ddm_build_copy/compile_v551_relation_evidence_atoms.py", config),
            "--run-id", shard_id,
            "--bridge-path", bridge_path,
            "--output-root", output_root,
            "--v551-compile-mode", "canonical",
        ]
        return impl._invoke_run(cmd, timeout_sec=1800, config=config)

    def run_v551j_g4(
        shard_id: str, atoms_path: str, pattern_index_path: str, meaning_summary_path: str,
        output_root: str, v552_structural_dir: str, config, registry_path: str | None = None,
    ) -> dict[str, Any]:
        del v552_structural_dir
        pattern_root = Path(pattern_index_path).parent
        v551_manifest = Path(atoms_path).parent / "manifest.json"
        cmd = [
            sys.executable, impl._abs("data/ddm_build_copy/compile_v551j_joint_evidence_packets.py", config),
            "--run-id", shard_id,
            "--v551-atoms-path", atoms_path,
            "--v551-manifest-path", str(v551_manifest),
            "--v550j-pattern-index-path", pattern_index_path,
            "--v550j-pattern-item-index-path", str(pattern_root / "joint_response_pattern_item_index.parquet"),
            "--v550j-relation-signature-path", str(pattern_root / "joint_pattern_relation_signature.parquet"),
            "--v550j-manifest-path", str(pattern_root / "v550j_manifest.json"),
            "--v550j-readiness-report-path", str(pattern_root / "v550j_source_wave_readiness_report.json"),
            "--v550j-meaning-summary-path", meaning_summary_path,
            "--registry-path", str(registry_path or impl.DEFAULT_JOINT_REGISTRY),
            "--output-root", output_root,
            "--emit-review-surface", "--emit-certified-index",
            "--no-write-csv", "--write-parquet", "--strict",
        ]
        return impl._invoke_run(cmd, timeout_sec=1800, config=config)

    def run_v552j_g4(
        shard_id: str, v551j_run_root: str, output_root: str, v552_structural_dir: str, config,
    ) -> dict[str, Any]:
        cmd = [
            sys.executable, impl._abs("data/ddm_build_copy/compile_v552j_structural_handoff.py", config),
            "--run-id", shard_id,
            "--v551j-manifest-path", str(Path(v551j_run_root) / "manifest" / "manifest.json"),
            "--v552-manifest-path", str(Path(v552_structural_dir).parent / "manifest.json"),
            "--output-root", output_root,
            "--write-parquet", "--no-write-csv",
        ]
        return impl._invoke_run(cmd, timeout_sec=1800, config=config)

    original_run_wave = base.run_wave

    def typed_run_wave(*args, **kwargs):
        global _ACTIVE_EXPECTED_IDENTITY
        family = str(args[0] if len(args) > 0 else kwargs.get("family", ""))
        wave = str(args[1] if len(args) > 1 else kwargs.get("wave", ""))
        country = str(args[2] if len(args) > 2 else kwargs.get("country", ""))
        run_id = f"{family}_{wave}" + (f"_{country}" if country else "")
        previous = _ACTIVE_EXPECTED_IDENTITY
        _ACTIVE_EXPECTED_IDENTITY = {
            "run_id": run_id, "source": family, "wave": wave,
            "country_code": country, "shard_id": "",
        }
        try:
            return _normalize_typed_wave_result(original_run_wave(*args, **kwargs))
        finally:
            _ACTIVE_EXPECTED_IDENTITY = previous

    impl.run_v551 = run_v551_v3
    impl.run_v551j = run_v551j_g4
    impl.run_v552j = run_v552j_g4
    impl.summarize_v551_functional_gate = summarize_v551_functional_gate
    impl.summarize_v551j_functional_gate = summarize_v551j_functional_gate
    impl.summarize_v552j_functional_gate = summarize_v552j_functional_gate
    base.run_v551 = run_v551_v3
    base.run_v551j = run_v551j_g4
    base.run_v552j = run_v552j_g4
    base.summarize_v551_functional_gate = summarize_v551_functional_gate
    base.summarize_v551j_functional_gate = summarize_v551j_functional_gate
    base.summarize_v552j_functional_gate = summarize_v552j_functional_gate
    base.run_wave = typed_run_wave
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
