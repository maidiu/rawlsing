#!/usr/bin/env python3
"""Build the V558 numeric runtime graft readiness report.

This stays deliberately non-runtime: it decides whether the current V557
outputs are safe to enter a review path for a future numeric runtime graft.
It does not implement the graft, persona runtime, or any app-facing behavior.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from data.ddm_build_copy.ddm_v5_build_standard import build_review_gate_record
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text

try:
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover - keeps patch tests runnable outside the full repo
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_V558_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v558" / "runs"


def _resolve_default_governance_root() -> Path:
    candidates = [
        ROOT / "rawlsing_current_state_repair_pack_v1" / "04_REVIEW_AND_CI",
        ROOT / "rawlsing_v5_locked_build_pack_v1" / "04_REVIEW_AND_CI",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


DEFAULT_GOVERNANCE_ROOT = _resolve_default_governance_root()

SCHEMA_VERSION = "v558_runtime_graft_readiness_0.1"
COMPILER_VERSION = "v558_runtime_graft_readiness_0.1"


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if isinstance(value, float) and value != value:
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _report_status(report: dict[str, Any]) -> tuple[str, bool | None, bool | None]:
    candidates = [_clean_text(report.get("status")), _clean_text(report.get("final_status")), _clean_text(report.get("input_status"))]
    status = next((value for value in candidates if value), "")
    lower = status.lower()
    ready_semantic = report.get("ready_for_semantic_deepening") if "ready_for_semantic_deepening" in report else None
    ready_runtime = report.get("ready_for_runtime_consumption") if "ready_for_runtime_consumption" in report else None
    if isinstance(ready_semantic, str):
        ready_semantic = ready_semantic.strip().lower() in {"true", "1", "yes", "y"}
    if isinstance(ready_runtime, str):
        ready_runtime = ready_runtime.strip().lower() in {"true", "1", "yes", "y"}
    if any(token in lower for token in ("blocked", "not_ready", "missing_required_input", "missing")):
        return "blocked", False, False
    if ready_semantic is False:
        return "gapped", False, bool(ready_runtime)
    if ready_semantic is True and ready_runtime is False:
        return "review_ready", True, False
    if ready_runtime is False:
        return "gapped", bool(ready_semantic), False
    if any(token in lower for token in ("gap", "provisional", "degraded", "partial")):
        return "gapped", ready_semantic if isinstance(ready_semantic, bool) else False, ready_runtime if isinstance(ready_runtime, bool) else False
    if status:
        return "ready", ready_semantic if isinstance(ready_semantic, bool) else True, ready_runtime if isinstance(ready_runtime, bool) else True
    return "", ready_semantic if isinstance(ready_semantic, bool) else None, ready_runtime if isinstance(ready_runtime, bool) else None


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _read_v557_bundle(v557_run_root: Path) -> dict[str, Any]:
    readiness_path = v557_run_root / "manifest" / "v557_readiness_report.json"
    packet_path = v557_run_root / "packets" / "v557_renderer_contract_packet.json"
    readiness = _read_json(readiness_path) if readiness_path.exists() else {}
    packet = _read_json(packet_path) if packet_path.exists() else {}
    prompt_shape_audit_path = v557_run_root / "audits" / "v557_prompt_shape_audit.json"
    prompt_shape_audit = _read_json(prompt_shape_audit_path) if prompt_shape_audit_path.exists() else {}
    return {
        "readiness_path": repo_relative_path_text(readiness_path),
        "packet_path": repo_relative_path_text(packet_path),
        "prompt_shape_audit_path": repo_relative_path_text(prompt_shape_audit_path),
        "readiness": readiness,
        "packet": packet,
        "prompt_shape_audit": prompt_shape_audit,
    }


def _governance_inventory(governance_root: Path) -> dict[str, Any]:
    if not governance_root.exists():
        return {"root": repo_relative_path_text(governance_root), "present": False, "files": []}
    files = sorted(repo_relative_path_text(path) for path in governance_root.rglob("*") if path.is_file())
    return {"root": repo_relative_path_text(governance_root), "present": bool(files), "files": files}


def build_v558_numeric_runtime_graft_readiness(
    *,
    run_id: str,
    v557_run_root: str | Path,
    output_root: str | Path = DEFAULT_V558_OUTPUT_ROOT,
    governance_root: str | Path | None = None,
) -> dict[str, Any]:
    output_root = Path(output_root)
    root = output_root / run_id
    v557_root = Path(v557_run_root)
    governance_root_path = Path(governance_root) if governance_root is not None else DEFAULT_GOVERNANCE_ROOT

    bundle = _read_v557_bundle(v557_root)
    v557_readiness = bundle["readiness"]
    v557_packet = bundle["packet"]
    v557_prompt_shape = bundle["prompt_shape_audit"]
    governance = _governance_inventory(governance_root_path)

    required_inputs = {
        "v557_readiness_report": bundle["readiness_path"],
        "v557_renderer_contract_packet": bundle["packet_path"],
    }

    missing_inputs: list[str] = []
    for key, path_text in required_inputs.items():
        if not Path(path_text).exists():
            missing_inputs.append(key)

    blockers: list[dict[str, Any]] = []
    if missing_inputs:
        blockers.append(
            {
                "blocker_code": "missing_required_v557_inputs",
                "status": "blocked",
                "details": missing_inputs,
            }
        )

    v557_status, v557_ready_semantic, v557_ready_runtime = _report_status(v557_readiness)
    if v557_status == "blocked":
        blockers.append(
            {
                "blocker_code": "v557_not_ready_for_review",
                "status": "blocked",
                "details": {
                    "v557_status": v557_status,
                    "ready_for_semantic_deepening": v557_ready_semantic,
                    "ready_for_runtime_consumption": v557_ready_runtime,
                },
            }
        )
    elif v557_ready_semantic is False:
        blockers.append(
            {
                "blocker_code": "v557_not_ready_for_semantic_review",
                "status": "blocked",
                "details": {
                    "v557_status": v557_status,
                    "ready_for_semantic_deepening": v557_ready_semantic,
                    "ready_for_runtime_consumption": v557_ready_runtime,
                },
            }
        )

    if not governance["present"]:
        blockers.append(
            {
                "blocker_code": "missing_app_facing_governance_pack",
                "status": "blocked",
                "details": {
                    "governance_root": governance["root"],
                    "required_pack": "rawlsing_current_state_repair_pack_v1/04_REVIEW_AND_CI",
                },
            }
        )

    prompt_shape_detected = bool(v557_prompt_shape.get("prompt_shape_detected", v557_prompt_shape.get("prompt_shape_allowed", False)))
    prompt_shape_violation_count = int(v557_prompt_shape.get("prompt_shape_violation_count", v557_prompt_shape.get("violation_count", 0)) or 0)
    prompt_shape_clear = bool(v557_prompt_shape.get("prompt_shape_clear", not prompt_shape_detected and prompt_shape_violation_count == 0))
    prompt_shape_allowed = False
    if prompt_shape_detected or not prompt_shape_clear or prompt_shape_violation_count > 0:
        blockers.append(
            {
                "blocker_code": "v557_prompt_shape_violation",
                "status": "blocked",
                "details": {
                    "prompt_shape_detected": prompt_shape_detected,
                    "violation_count": prompt_shape_violation_count,
                    "violations": v557_prompt_shape.get("violations", []),
                },
            }
        )

    v557_packet_flags = {
        "runtime_packets_written": bool(v557_packet.get("runtime_packets_written", False)),
        "persona_fields_written": bool(v557_packet.get("persona_fields_written", False)),
        "forbidden_outputs_written": bool(v557_packet.get("forbidden_outputs_written", False)),
        "dialogue_generated": bool(v557_packet.get("payload", {}).get("dialogue_generated", False)),
        "voice_generated": bool(v557_packet.get("payload", {}).get("voice_generated", False)),
    }
    if any(v557_packet_flags.values()):
        blockers.append(
            {
                "blocker_code": "v557_leaks_runtime_material",
                "status": "blocked",
                "details": v557_packet_flags,
            }
        )

    status = "BLOCKED_RUNTIME_GRAFT_NOT_SAFE" if blockers else "READY_FOR_RUNTIME_GRAFT_REVIEW"
    readiness = {
        "run_id": run_id,
        "status": status,
        "final_status": status,
        "schema_version": SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
        "created_at": utc_now(),
        "ready_for_runtime_graft_review": not blockers,
        "ready_for_runtime_graft": False,
        "v557": {
            "root": repo_relative_path_text(v557_root),
            "readiness_path": bundle["readiness_path"],
            "packet_path": bundle["packet_path"],
            "prompt_shape_audit_path": bundle["prompt_shape_audit_path"],
            "status": v557_status,
            "prompt_shape_detected": prompt_shape_detected,
            "prompt_shape_violation_count": prompt_shape_violation_count,
            "prompt_shape_clear": prompt_shape_clear,
            "prompt_shape_allowed": prompt_shape_allowed,
            "flags": v557_packet_flags,
        },
        "governance": governance,
        "required_inputs": required_inputs,
        "missing_inputs": missing_inputs,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "authority_documents": [
            repo_relative_path_text(ROOT / "docs" / "architecture_control" / "RAWLSING_COMPLETION_MAP.md"),
            repo_relative_path_text(ROOT / "docs" / "architecture_control" / "V552_TO_V557_LIVING_SYSTEM_NOTE.md"),
        ],
        "evidence_notes": [
            "V558 is a readiness decision only.",
            "No runtime graft or app-facing code is implemented here.",
            "Missing governance evidence blocks readiness.",
        ],
    }
    missing_authority_docs = [path for path in readiness["authority_documents"] if not Path(path).exists()]
    if missing_authority_docs:
        blockers.append(
            {
                "blocker_code": "missing_authority_documents",
                "status": "blocked",
                "details": missing_authority_docs,
            }
        )
        status = "BLOCKED_RUNTIME_GRAFT_NOT_SAFE"
        readiness["status"] = status
        readiness["final_status"] = status
        readiness["ready_for_runtime_graft_review"] = False
        readiness["blockers"] = blockers
        readiness["blocker_count"] = len(blockers)

    report_path = root / "manifest" / "v558_runtime_graft_readiness_report.json"
    blockers_path = root / "audits" / "v558_runtime_graft_blockers.json"
    input_manifest_path = root / "manifest" / "v558_input_manifest.json"
    schema_path = root / "schemas" / "v558_runtime_graft_readiness_report.schema.json"
    build_ledger_path = root / "manifest" / "v558_runtime_graft_readiness_build_ledger.json"

    build_record = build_review_gate_record(
        run_id=run_id,
        layer="v558",
        title="Numeric runtime graft readiness",
        artifact_type="v558_runtime_graft_readiness_report",
        status=status,
        input_inspection={
            "input_status": "blocked" if blockers else "ready",
            "missing_required_inputs": missing_inputs,
            "stop_missing_inputs": missing_inputs,
        },
        artifact_paths={
            "report_path": repo_relative_path_text(report_path),
            "blockers_path": repo_relative_path_text(blockers_path),
            "input_manifest_path": repo_relative_path_text(input_manifest_path),
            "schema_path": repo_relative_path_text(schema_path),
        },
        how_built=[
            "read the V557 readiness report and renderer contract packet",
            "check governance, prompt-shape, and runtime-leak conditions",
            "record blockers rather than infer runtime graft permission",
            "write the readiness report, blockers audit, input manifest, and schema",
        ],
        continuity_notes=[
            "This is a review boundary, not runtime graft implementation.",
            "Upstream continuity is checked for artifact presence and contract shape only.",
            "Downstream continuity remains intentionally untested here.",
        ],
    )
    build_ledger = {
        "run_id": run_id,
        "build_kind": "v558_runtime_graft_readiness",
        "final_status": status,
        "implementation_standard": {
            "implementation_kind": ["blocked", "reviewable"],
            "provisionality": ["blocked", "provisional"],
            "scaffold_level": ["review_boundary"],
            "continuity_checked_full": False,
        },
        "layer_records": [build_record],
        "counts": {
            "layer_count": 1,
            "blocked_blocker_count": len(blockers),
            "ready_blocker_count": 0 if blockers else 1,
        },
        "build_rules": [
            "Never promote the gate to runtime graft.",
            "Never ignore missing authority documents.",
            "Never mark runtime graft as already complete.",
        ],
        "created_at": utc_now(),
    }

    readiness.update(
        {
            "build_ledger_path": repo_relative_path_text(build_ledger_path),
            "implementation_kind": build_record["implementation_kind"],
            "provisionality": build_record["provisionality"],
            "scaffold_level": build_record["scaffold_level"],
            "input_status": build_record["input_status"],
            "upstream_continuity_scope": build_record["upstream_continuity_scope"],
            "upstream_continuity_result": build_record["upstream_continuity_result"],
            "downstream_continuity_scope": build_record["downstream_continuity_scope"],
            "downstream_continuity_result": build_record["downstream_continuity_result"],
            "full_upstream_and_downstream_continuity_checked": build_record["full_upstream_and_downstream_continuity_checked"],
            "how_built": build_record["how_built"],
            "continuity_notes": build_record["continuity_notes"],
        }
    )

    _write_json(report_path, readiness)
    _write_json(blockers_path, {"run_id": run_id, "blockers": blockers, "blocker_count": len(blockers), "created_at": utc_now()})
    _write_json(
        input_manifest_path,
        {
            "run_id": run_id,
            "v557_run_root": repo_relative_path_text(v557_root),
            "governance_root": governance["root"],
            "required_inputs": required_inputs,
            "present_inputs": {key: Path(path).exists() for key, path in required_inputs.items()},
            "created_at": utc_now(),
        },
    )
    _write_json(
        schema_path,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "v558_runtime_graft_readiness_report",
            "type": "object",
            "required": [
                "run_id",
                "status",
                "ready_for_runtime_graft_review",
                "ready_for_runtime_graft",
                "blockers",
                "implementation_kind",
                "provisionality",
                "scaffold_level",
                "build_ledger_path",
                "upstream_continuity_scope",
                "upstream_continuity_result",
                "downstream_continuity_scope",
                "downstream_continuity_result",
                "full_upstream_and_downstream_continuity_checked",
                "how_built",
                "continuity_notes",
            ],
            "properties": {
                "run_id": {"type": "string"},
                "status": {"type": "string"},
                "ready_for_runtime_graft_review": {"type": "boolean"},
                "ready_for_runtime_graft": {"type": "boolean"},
                "blockers": {"type": "array"},
                "implementation_kind": {"type": "string"},
                "provisionality": {"type": "string"},
                "scaffold_level": {"type": "string"},
                "build_ledger_path": {"type": "string"},
            },
            "additionalProperties": True,
        },
    )
    _write_json(build_ledger_path, build_ledger)

    readiness.update(
        {
            "report_path": repo_relative_path_text(report_path),
            "blockers_path": repo_relative_path_text(blockers_path),
            "input_manifest_path": repo_relative_path_text(input_manifest_path),
            "schema_path": repo_relative_path_text(schema_path),
            "build_ledger_path": repo_relative_path_text(build_ledger_path),
            "implementation_kind": build_record["implementation_kind"],
            "provisionality": build_record["provisionality"],
            "scaffold_level": build_record["scaffold_level"],
            "input_status": build_record["input_status"],
            "upstream_continuity_scope": build_record["upstream_continuity_scope"],
            "upstream_continuity_result": build_record["upstream_continuity_result"],
            "downstream_continuity_scope": build_record["downstream_continuity_scope"],
            "downstream_continuity_result": build_record["downstream_continuity_result"],
            "full_upstream_and_downstream_continuity_checked": build_record["full_upstream_and_downstream_continuity_checked"],
            "how_built": build_record["how_built"],
            "continuity_notes": build_record["continuity_notes"],
        }
    )
    return readiness


def validate_v558_runtime_graft_readiness(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("ready_for_runtime_graft"):
        errors.append("V558 must not mark runtime graft as already complete")
    if "report_path" not in readiness or not Path(str(readiness["report_path"])).exists():
        errors.append("missing runtime graft readiness report")
    if "blockers_path" not in readiness or not Path(str(readiness["blockers_path"])).exists():
        errors.append("missing blockers audit")
    if "input_manifest_path" not in readiness or not Path(str(readiness["input_manifest_path"])).exists():
        errors.append("missing input manifest")
    if "schema_path" not in readiness or not Path(str(readiness["schema_path"])).exists():
        errors.append("missing schema")
    if "build_ledger_path" not in readiness or not Path(str(readiness["build_ledger_path"])).exists():
        errors.append("missing build ledger")
    if readiness.get("blocker_count", 0) < 0:
        errors.append("negative blocker count")
    if readiness.get("status") not in {"BLOCKED_RUNTIME_GRAFT_NOT_SAFE", "READY_FOR_RUNTIME_GRAFT_REVIEW"}:
        errors.append("unexpected V558 status")
    for key in ("implementation_kind", "provisionality", "scaffold_level", "how_built", "continuity_notes"):
        if not readiness.get(key):
            errors.append(f"missing {key}")
    return errors
