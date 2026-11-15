#!/usr/bin/env python3
"""Rawlsing V5 walking-skeleton contracts and manifest builders.

This is deliberately a thin integration spine, not a runtime/persona compiler.
It proves layer boundaries from V551J through V558 before deep downstream
semantics are built.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover - keeps patch tests runnable outside the full repo
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

SKELETON_SCHEMA_VERSION = "v0.1"
SKELETON_COMPILER_VERSION = "v5_walking_skeleton_0.1"

LAYER_CONTRACTS: list[dict[str, Any]] = [
    {
        "layer": "v552j",
        "name": "runtime_safe_structural_handoff_shell",
        "consumes": ["v551j_certified_packet_index", "v551j_reviewable_evidence_sidecar"],
        "emits": ["v552j_structural_handoff_manifest"],
        "allowed_use_permission_classes": ["structural_context_only", "review_only"],
        "forbidden_inputs": ["raw_v551_atoms", "raw_v550j_association_review_surface", "runtime_persona", "actor_orientation"],
        "forbidden_outputs": ["person_belief", "parent_trait", "household_biography", "carrier_membership", "actor_orientation", "runtime_psyche", "enneagram_type"],
        "stop_condition": "no_certified_packets_and_no_reviewable_sidecar",
    },
    {
        "layer": "v553",
        "name": "temporal_pressure_field_shell",
        "consumes": ["v552j_structural_handoff_manifest"],
        "emits": ["v553_temporal_pressure_field_manifest"],
        "allowed_use_permission_classes": ["structural_context_only"],
        "forbidden_inputs": ["raw_v551j_packets", "review_only_without_adapter"],
        "forbidden_outputs": ["life_event", "person_memory", "parent_orientation", "pressureflow_route", "enneagram_type"],
        "stop_condition": "v552j_handoff_not_ready",
    },
    {
        "layer": "v554",
        "name": "persona_seed_contract_shell",
        "consumes": ["v553_temporal_pressure_field_manifest"],
        "emits": ["v554_persona_seed_contract_manifest"],
        "allowed_use_permission_classes": ["bounded_seed_affordance_only"],
        "forbidden_inputs": ["raw_survey_rows", "raw_v551j_packets"],
        "forbidden_outputs": ["full_person", "chat_voice", "autobiography", "household_story", "enneagram_type"],
        "stop_condition": "temporal_pressure_field_missing",
    },
    {
        "layer": "v555",
        "name": "life_course_mediation_shell",
        "consumes": ["v554_persona_seed_contract_manifest"],
        "emits": ["v555_life_course_mediation_manifest"],
        "allowed_use_permission_classes": ["generated_mediation_only"],
        "forbidden_inputs": ["raw_v551j_packets"],
        "forbidden_outputs": ["unbounded_biography", "source_claim_as_memory", "survey_answer_as_person_fact"],
        "stop_condition": "persona_seed_contract_missing",
    },
    {
        "layer": "v556",
        "name": "pressureflow_attractor_shell",
        "consumes": ["v555_life_course_mediation_manifest"],
        "emits": ["v556_pressureflow_attractor_manifest"],
        "allowed_use_permission_classes": ["generated_psyche_dynamics_only"],
        "forbidden_inputs": ["raw_survey_rows", "raw_v551j_packets", "countrywide_personality"],
        "forbidden_outputs": ["enneagram_from_survey", "enneagram_from_country", "static_trait_assignment"],
        "stop_condition": "life_course_mediation_missing",
    },
    {
        "layer": "v557",
        "name": "phenomenological_renderer_shell",
        "consumes": ["v556_pressureflow_attractor_manifest"],
        "emits": ["v557_renderer_manifest"],
        "allowed_use_permission_classes": ["runtime_surface_after_generation_audit"],
        "forbidden_inputs": ["raw_survey_rows", "raw_v551j_packets", "unmediated_structural_pressure"],
        "forbidden_outputs": ["unaudited_persona", "upstream_evidence_as_dialogue", "source_claim_as_autobiography"],
        "stop_condition": "pressureflow_attractor_missing",
    },
    {
        "layer": "v558",
        "name": "runtime_input_gate_shell",
        "consumes": ["v557_renderer_manifest"],
        "emits": ["v558_runtime_boundary_manifest"],
        "allowed_use_permission_classes": ["review_boundary_only", "graft_readiness_only"],
        "forbidden_inputs": ["raw_survey_rows", "raw_v551j_packets", "runtime_persona", "voice", "dialogue"],
        "forbidden_outputs": ["runtime_persona", "chat_voice", "dialogue", "app_wiring"],
        "stop_condition": "renderer_manifest_missing",
    },
]

REQUIRED_V551J_INPUTS = {
    "certified_packet_index_schema": "schemas/v551j_certified_packet_index.schema.json",
    "review_surface_schema": "schemas/v551j_packet_review_surface.schema.json",
    "reviewable_sidecar_schema": "schemas/v551j_reviewable_evidence_sidecar.schema.json",
    "certification_report": "manifest/v551j_certification_readiness_report.json",
    "review_report": "manifest/v551j_review_readiness_report.json",
    "provenance_manifest": "manifest/v551j_input_provenance_manifest.json",
}


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            value = json.load(f)
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)


def inspect_v551j_run_root(v551j_run_root: str | Path) -> dict[str, Any]:
    root = Path(v551j_run_root)
    files: dict[str, Any] = {}
    missing: list[str] = []
    unreadable: list[str] = []
    for name, rel in REQUIRED_V551J_INPUTS.items():
        path = root / rel
        exists = path.exists()
        payload = _read_json(path) if exists else {}
        if not exists:
            missing.append(name)
        elif not payload:
            unreadable.append(name)
        files[name] = {
            "relative_path": rel,
            "exists": exists,
            "readable_json": bool(payload),
            "payload": payload,
        }
    certified_rows = int(files.get("certification_report", {}).get("payload", {}).get("certified_packet_rows", 0) or 0)
    review_surface_rows = int(files.get("review_report", {}).get("payload", {}).get("review_surface_rows", 0) or 0)
    sidecar_exists = bool(files.get("reviewable_sidecar_schema", {}).get("exists"))
    return {
        "v551j_run_root": str(root),
        "files": files,
        "missing_inputs": missing,
        "unreadable_inputs": unreadable,
        "certified_packet_rows": certified_rows,
        "review_surface_rows": review_surface_rows,
        "reviewable_sidecar_schema_exists": sidecar_exists,
        "input_status": "ready" if not missing and not unreadable else "degraded",
    }


def _forbidden_input_audit_rows(layer_contract: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item in layer_contract.get("forbidden_inputs", []):
        rows.append(
            {
                "layer": layer_contract["layer"],
                "forbidden_input": item,
                "audit_status": "blocked_by_contract",
                "risk_description": f"{item} may collapse evidence/structure into downstream runtime meaning.",
            }
        )
    return rows


def build_walking_skeleton_manifests(
    *,
    run_id: str,
    v551j_run_root: str | Path,
    output_root: str | Path,
) -> dict[str, Any]:
    root = Path(output_root) / run_id
    contract_dir = root / "contracts"
    layers_dir = root / "layers"
    audit_dir = root / "audits"
    manifest_dir = root / "manifest"
    for directory in (contract_dir, layers_dir, audit_dir, manifest_dir):
        directory.mkdir(parents=True, exist_ok=True)

    inspection = inspect_v551j_run_root(v551j_run_root)
    sidecar_missing = "reviewable_sidecar_schema" in inspection["missing_inputs"]
    no_certified = inspection["certified_packet_rows"] <= 0
    current_status = "ready"
    if inspection["input_status"] != "ready":
        current_status = "ready_with_input_gaps"
    if no_certified and sidecar_missing:
        current_status = "not_ready_no_certified_or_sidecar"

    contract_payload = {
        "run_id": run_id,
        "schema_version": SKELETON_SCHEMA_VERSION,
        "compiler_version": SKELETON_COMPILER_VERSION,
        "created_at": utc_now(),
        "doctrine": "thin end-to-end walking skeleton; no runtime/persona semantics emitted",
        "source_layer": "v551j",
        "target_layers": [contract["layer"] for contract in LAYER_CONTRACTS],
        "layer_contracts": LAYER_CONTRACTS,
    }
    _write_json(contract_dir / "v5_walking_skeleton_contract.json", contract_payload)

    layer_manifests: list[dict[str, Any]] = []
    previous_status = current_status
    previous_artifact = "v551j_certified_packet_index+v551j_reviewable_evidence_sidecar"
    for contract in LAYER_CONTRACTS:
        blocked = previous_status.startswith("not_ready")
        status = "SHELL_BLOCKED_UPSTREAM_NOT_READY" if blocked else ("SHELL_READY_WITH_INPUT_GAPS" if "gaps" in previous_status else "SHELL_READY")
        stop_reason = contract["stop_condition"] if blocked else "none"
        manifest = {
            "run_id": run_id,
            "layer": contract["layer"],
            "name": contract["name"],
            "status": status,
            "input_artifact": previous_artifact,
            "consumes": contract["consumes"],
            "emits": contract["emits"],
            "allowed_use_permission_classes": contract["allowed_use_permission_classes"],
            "forbidden_inputs": contract["forbidden_inputs"],
            "forbidden_outputs": contract["forbidden_outputs"],
            "stop_reason": stop_reason,
            "upstream_v551j": {
                "certified_packet_rows": inspection["certified_packet_rows"],
                "review_surface_rows": inspection["review_surface_rows"],
                "reviewable_sidecar_schema_exists": inspection["reviewable_sidecar_schema_exists"],
                "input_status": inspection["input_status"],
            },
            "runtime_packets_written": False,
            "persona_fields_written": False,
            "created_at": utc_now(),
            "schema_version": SKELETON_SCHEMA_VERSION,
        }
        layer_path = layers_dir / contract["layer"] / f"{contract['layer']}_{contract['name']}_manifest.json"
        _write_json(layer_path, manifest)
        layer_manifests.append({**manifest, "path": str(layer_path)})
        previous_status = "not_ready" if blocked else previous_status
        previous_artifact = contract["emits"][0]

    audit_rows = [row for contract in LAYER_CONTRACTS for row in _forbidden_input_audit_rows(contract)]
    audit_payload = {
        "run_id": run_id,
        "rows": audit_rows,
        "row_count": len(audit_rows),
        "created_at": utc_now(),
        "schema_version": SKELETON_SCHEMA_VERSION,
    }
    _write_json(audit_dir / "v5_walking_skeleton_forbidden_input_audit.json", audit_payload)

    final_status = "READY_V5_WALKING_SKELETON"
    warnings: list[str] = []
    if inspection["missing_inputs"] or inspection["unreadable_inputs"]:
        final_status = "READY_V5_WALKING_SKELETON_WITH_INPUT_GAPS"
        warnings.extend(f"missing:{name}" for name in inspection["missing_inputs"])
        warnings.extend(f"unreadable:{name}" for name in inspection["unreadable_inputs"])
    if no_certified and sidecar_missing:
        final_status = "NOT_READY_V5_WALKING_SKELETON_NO_CERTIFIED_OR_SIDECAR"
        warnings.append("no certified V551J packets and no reviewable sidecar schema")

    readiness = {
        "run_id": run_id,
        "final_status": final_status,
        "warnings": warnings,
        "v551j_inspection": {k: v for k, v in inspection.items() if k != "files"},
        "layer_manifest_count": len(layer_manifests),
        "layer_status_counts": {status: sum(1 for item in layer_manifests if item["status"] == status) for status in sorted({item["status"] for item in layer_manifests})},
        "contract_path": str(contract_dir / "v5_walking_skeleton_contract.json"),
        "forbidden_input_audit_path": str(audit_dir / "v5_walking_skeleton_forbidden_input_audit.json"),
        "layer_manifest_paths": [item["path"] for item in layer_manifests],
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "created_at": utc_now(),
        "schema_version": SKELETON_SCHEMA_VERSION,
        "compiler_version": SKELETON_COMPILER_VERSION,
    }
    _write_json(manifest_dir / "v5_walking_skeleton_readiness_report.json", readiness)
    return readiness


def validate_walking_skeleton_output(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("runtime_packets_written"):
        errors.append("runtime_packets_written must be false in walking skeleton")
    if readiness.get("persona_fields_written"):
        errors.append("persona_fields_written must be false in walking skeleton")
    if int(readiness.get("layer_manifest_count", 0) or 0) != len(LAYER_CONTRACTS):
        errors.append("layer manifest count does not match layer contracts")
    if not readiness.get("contract_path"):
        errors.append("missing contract path")
    return errors
