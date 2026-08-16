#!/usr/bin/env python3
"""G4 exact-producer entrypoint for the bounded Section 85 J-chain canary.

The G2 implementation is retained in
`_g2_run_bounded_nine_v550j_v551j_v552j.py`.  This entrypoint changes only the
producer/consumer contract surface now frozen at G4: V551J consumes the exact
V551 v3 manifest and V552J consumes exact V551J + V552 producer manifests;
functional acceptance verifies exact producer versions, identity, canonical
Parquet bytes and producer-declared serialized SHA-256 values.
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

LEGACY_IMPLEMENTATION = CODE_DIR / "_g2_run_bounded_nine_v550j_v551j_v552j.py"


def _load_implementation():
    spec = importlib.util.spec_from_file_location("section85_bounded_g2", LEGACY_IMPLEMENTATION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"SECTION85_BOUNDED_G2_IMPLEMENTATION_UNLOADABLE:{LEGACY_IMPLEMENTATION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _resolve_manifest(run_root: Path, stage: str) -> Path:
    candidates = [run_root / "manifest.json", run_root / "manifest" / "manifest.json"]
    existing = [path.resolve() for path in candidates if path.exists()]
    unique = list(dict.fromkeys(existing))
    if len(unique) != 1:
        raise RuntimeError(
            f"SECTION85_{stage.upper()}_EXACT_MANIFEST_REQUIRED:root={run_root}:candidates={unique}"
        )
    return unique[0]


def _run_root_for_manifest(manifest_path: Path) -> Path:
    return manifest_path.parent.parent if manifest_path.parent.name == "manifest" else manifest_path.parent


def _flag_value(command: list[str], flag: str) -> str:
    try:
        index = command.index(flag)
        return command[index + 1]
    except (ValueError, IndexError) as exc:
        raise RuntimeError(f"SECTION85_COMMAND_FLAG_MISSING:{flag}") from exc


def _expected_identity(entry: dict[str, Any], run_id: str) -> dict[str, str]:
    return {
        "run_id": run_id,
        "source": str(entry.get("source_family") or ""),
        "wave": str(entry.get("wave") or ""),
        "country_code": str(entry.get("country_code") or ""),
        "shard_id": str(entry.get("shard_id") or ""),
    }


def _assert_v551_identity(contract: dict[str, Any], expected: dict[str, str]) -> None:
    for key in ("producer_run_id", "source", "wave"):
        want_key = "run_id" if key == "producer_run_id" else key
        if expected[want_key] and str(contract.get(key) or "") != expected[want_key]:
            raise RuntimeError(
                f"SECTION85_V551_SCOPE_MISMATCH:{want_key}:"
                f"expected={expected[want_key]}:actual={contract.get(key, '')}"
            )
    if expected["country_code"]:
        if str(contract.get("country_code") or "") != expected["country_code"]:
            raise RuntimeError("SECTION85_V551_SCOPE_MISMATCH:country_code")
    elif expected["shard_id"] and str(contract.get("shard_id") or "") != expected["shard_id"]:
        raise RuntimeError("SECTION85_V551_SCOPE_MISMATCH:shard_id")


def build_plan(args, *, legacy=None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Rebind the retained G2 plan to the exact merged G4 producer CLIs."""
    legacy = legacy or _load_implementation()
    plan, preflight = legacy.build_plan(args)
    repo = args.repo_root.resolve()

    for entry in plan:
        # The V550 shard parent is the inherited pipeline run identity.  The old
        # G2 runner used shard_id as a temporary J-stage run id; G4 producers do
        # not permit that alias.
        inherited_run_id = str(entry["run_id"])
        expected = _expected_identity(entry, inherited_run_id)

        v551_scope = Path(entry["v551_atoms_path"]).resolve().parent
        v551_manifest = _resolve_manifest(v551_scope, "v551")
        v551_payload = _load_json(v551_manifest)
        if not v551_payload:
            raise RuntimeError(f"SECTION85_V551_MANIFEST_UNREADABLE:{v551_manifest}")
        v551_contract = verify_v551_artifact_files(v551_payload, _run_root_for_manifest(v551_manifest))
        _assert_v551_identity(v551_contract, expected)
        v551_atoms = Path(v551_contract["verified_artifacts"]["relation_evidence_atoms"]["path"]).resolve()

        v552_scope = Path(entry["v552_structural_context_dir"]).resolve().parent
        v552_manifest = _resolve_manifest(v552_scope, "v552")

        old_v551j = entry["commands"]["v551j"]
        v551j_output_root = Path(_flag_value(old_v551j, "--output-root")).resolve()
        v551j_manifest = v551j_output_root / inherited_run_id / "manifest" / "manifest.json"

        v551j = [
            sys.executable,
            str(legacy.find_script(repo, "compile_v551j_joint_evidence_packets.py")),
            "--run-id", inherited_run_id,
            "--v551-atoms-path", str(v551_atoms),
            "--v551-manifest-path", str(v551_manifest),
            "--v550j-pattern-index-path", _flag_value(old_v551j, "--v550j-pattern-index-path"),
            "--v550j-pattern-item-index-path", _flag_value(old_v551j, "--v550j-pattern-item-index-path"),
            "--v550j-relation-signature-path", _flag_value(old_v551j, "--v550j-relation-signature-path"),
            "--v550j-manifest-path", _flag_value(old_v551j, "--v550j-manifest-path"),
            "--v550j-readiness-report-path", _flag_value(old_v551j, "--v550j-readiness-report-path"),
            "--v550j-meaning-summary-path", _flag_value(old_v551j, "--v550j-meaning-summary-path"),
            "--registry-path", _flag_value(old_v551j, "--registry-path"),
            "--output-root", str(v551j_output_root),
            "--emit-review-surface", "--emit-certified-index",
            "--no-write-csv", "--write-parquet", "--strict",
        ]

        old_v552j = entry["commands"]["v552j"]
        v552j_output_root = Path(_flag_value(old_v552j, "--output-root")).resolve()
        v552j_manifest = v552j_output_root / inherited_run_id / "manifest.json"
        v552j_readiness = v552j_output_root / inherited_run_id / "manifest" / "v552j_readiness_report.json"
        v552j = [
            sys.executable,
            str(legacy.find_script(repo, "compile_v552j_structural_handoff.py")),
            "--run-id", inherited_run_id,
            "--v551j-manifest-path", str(v551j_manifest),
            "--v552-manifest-path", str(v552_manifest),
            "--output-root", str(v552j_output_root),
            "--write-parquet", "--no-write-csv",
        ]

        entry["commands"]["v551j"] = v551j
        entry["commands"]["v552j"] = v552j
        entry["v551_atoms_path"] = str(v551_atoms)
        entry["v551_manifest_path"] = str(v551_manifest)
        entry["v552_manifest_path"] = str(v552_manifest)
        entry["producer_run_id"] = inherited_run_id
        entry["expected_producer_identity"] = expected
        entry["expected_outputs"]["v551j_manifest"] = str(v551j_manifest)
        entry["expected_outputs"]["v552j_manifest"] = str(v552j_manifest)
        entry["expected_outputs"]["v552j_readiness"] = str(v552j_readiness)

    preflight.update(
        {
            "section85_typed_state_contract": "rawlsing_pipeline_boundary_v1",
            "v551j_acceptance_hook": "ACTIVE_G4_EXACT_PRODUCER_CONTRACT",
            "v551j_schema_version": V551J_SCHEMA_VERSION,
            "v551j_compiler_version": V551J_COMPILER_VERSION,
            "v552j_acceptance_hook": "ACTIVE_G4_EXACT_PRODUCER_CONTRACT",
            "v552j_schema_version": V552J_SCHEMA_VERSION,
            "v552j_compiler_version": V552J_COMPILER_VERSION,
        }
    )
    return plan, preflight


def _typed_functional_gate(entry: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, bool]]:
    """Exact G4 gate: typed state + version + identity + manifest-declared bytes."""
    outputs = entry["expected_outputs"]
    v550j_manifest = _load_json(Path(outputs["v550j_manifest"]))
    v550j_ready = _load_json(Path(outputs["v550j_readiness"]))
    expected = entry.get("expected_producer_identity") or _expected_identity(
        entry, str(entry.get("producer_run_id") or entry.get("run_id") or "")
    )

    v551j_state = exact_producer_gate(
        outputs["v551j_manifest"], stage="v551j", expected_identity=expected
    )
    v552j_state = exact_producer_gate(
        outputs["v552j_manifest"], stage="v552j", expected_identity=expected
    )
    checks = {
        "v550j_success": bool(v550j_manifest.get("success")),
        "v550j_validation_pass": str(v550j_manifest.get("validation_status", "")).lower() == "pass",
        "v550j_registry_applicable": v550j_ready.get("family_registry_status") == "applicable",
        "v550j_not_blocked": not v550j_ready.get("blocking_issues"),
        "v551j_exact_producer_contract_valid": bool(v551j_state["typed_contract_valid"]),
        "v551j_run_integrity_pass": bool(v551j_state["integrity_pass"]),
        "v552j_exact_producer_contract_valid": bool(v552j_state["typed_contract_valid"]),
        "v552j_run_integrity_pass": bool(v552j_state["integrity_pass"]),
    }
    return v551j_state, v552j_state, checks


def main() -> int:
    legacy = _load_implementation()
    legacy_build_plan = legacy.build_plan

    def g4_build_plan(args):
        shim = type("LegacyShim", (), {})()
        shim.build_plan = legacy_build_plan
        shim.find_script = legacy.find_script
        return build_plan(args, legacy=shim)

    legacy.build_plan = g4_build_plan
    legacy._typed_functional_gate = _typed_functional_gate
    return int(legacy.main())


if __name__ == "__main__":
    raise SystemExit(main())
