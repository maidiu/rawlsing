#!/usr/bin/env python3
"""Build the V558 runtime input gate and normalized runtime input object.

This is the first V558+ implementation pass. It does not implement runtime
generation, app wiring, or persona synthesis. It only validates the V557
renderer contract, normalizes the admissible runtime input, and emits audit
artifacts for the next pass.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

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

SCHEMA_VERSION = "v558_runtime_input_gate_0.1"
COMPILER_VERSION = "v558_runtime_input_gate_0.1"


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


def _write_parquet(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    frame.to_parquet(path, index=False)


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    except Exception:
        return _clean_text(value)


def _read_v557_bundle(v557_run_root: Path) -> dict[str, Any]:
    readiness_path = v557_run_root / "manifest" / "v557_readiness_report.json"
    packet_path = v557_run_root / "packets" / "v557_renderer_contract_packet.json"
    prompt_shape_audit_path = v557_run_root / "audits" / "v557_prompt_shape_audit.json"
    forbidden_audit_path = v557_run_root / "audits" / "v557_forbidden_inference_audit.json"
    input_manifest_path = v557_run_root / "manifest" / "v557_input_manifest.json"
    readiness = _read_json(readiness_path) if readiness_path.exists() else {}
    packet = _read_json(packet_path) if packet_path.exists() else {}
    prompt_shape_audit = _read_json(prompt_shape_audit_path) if prompt_shape_audit_path.exists() else {}
    forbidden_audit = _read_json(forbidden_audit_path) if forbidden_audit_path.exists() else {}
    input_manifest = _read_json(input_manifest_path) if input_manifest_path.exists() else {}
    return {
        "readiness_path": repo_relative_path_text(readiness_path),
        "packet_path": repo_relative_path_text(packet_path),
        "prompt_shape_audit_path": repo_relative_path_text(prompt_shape_audit_path),
        "forbidden_audit_path": repo_relative_path_text(forbidden_audit_path),
        "input_manifest_path": repo_relative_path_text(input_manifest_path),
        "readiness": readiness,
        "packet": packet,
        "prompt_shape_audit": prompt_shape_audit,
        "forbidden_audit": forbidden_audit,
        "input_manifest": input_manifest,
    }


def _governance_inventory(governance_root: Path) -> dict[str, Any]:
    if not governance_root.exists():
        return {"root": repo_relative_path_text(governance_root), "present": False, "files": []}
    files = sorted(repo_relative_path_text(path) for path in governance_root.rglob("*") if path.is_file())
    return {"root": repo_relative_path_text(governance_root), "present": bool(files), "files": files}


def _input_field_audit(field_name: str, source_path: str, source_value: Any, normalized_value: Any, rule: str, status: str, reason: str = "") -> dict[str, Any]:
    return {
        "field_name": field_name,
        "source_path": source_path,
        "source_value": _stringify(source_value),
        "normalized_value": _stringify(normalized_value),
        "normalization_rule": rule,
        "audit_status": status,
        "reason": reason,
    }


def build_v558_runtime_input_gate(
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
    v557_forbidden = bundle["forbidden_audit"]
    governance = _governance_inventory(governance_root_path)

    required_inputs = {
        "v557_readiness_report": bundle["readiness_path"],
        "v557_renderer_contract_packet": bundle["packet_path"],
        "v557_prompt_shape_audit": bundle["prompt_shape_audit_path"],
        "v557_forbidden_inference_audit": bundle["forbidden_audit_path"],
    }
    missing_inputs = [key for key, path_text in required_inputs.items() if not Path(path_text).exists()]

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
                "blocker_code": "v557_not_ready_for_v558",
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

    payload = v557_packet.get("payload", {}) if isinstance(v557_packet, dict) else {}
    source_to_generation_ledger = payload.get("source_to_generation_separation_ledger", [])
    if not source_to_generation_ledger:
        blockers.append(
            {
                "blocker_code": "missing_source_to_generation_separation_ledger",
                "status": "blocked",
                "details": "V557 packet payload did not expose a source-to-generation separation ledger.",
            }
        )

    render_blockers = payload.get("render_blockers", [])
    runtime_wiring_contract = payload.get("runtime_wiring_contract", [])
    renderer_input_contract = payload.get("renderer_input_contract", {})

    handoff_requirements_present = all(
        [
            bool(renderer_input_contract),
            bool(runtime_wiring_contract),
            bool(source_to_generation_ledger),
            bool(payload.get("future_consumer_notes", [])),
            bool(payload.get("app_wiring_boundaries", [])),
        ]
    )

    normalized_runtime_input = {
        "run_id": run_id,
        "v557_run_root": repo_relative_path_text(v557_root),
        "v557_status": v557_status or "unknown",
        "v557_readiness_status": _clean_text(v557_readiness.get("status")),
        "v557_final_status": _clean_text(v557_readiness.get("final_status")),
        "prompt_shape_detected": prompt_shape_detected,
        "prompt_shape_violation_count": prompt_shape_violation_count,
        "prompt_shape_clear": prompt_shape_clear,
        "prompt_shape_allowed": prompt_shape_allowed,
        "v557_packet_flags": v557_packet_flags,
        "renderer_input_contract": renderer_input_contract,
        "runtime_wiring_contract": runtime_wiring_contract,
        "source_to_generation_separation_ledger": source_to_generation_ledger,
        "render_blockers": render_blockers,
        "memory_governance_requirements": payload.get("future_consumer_notes", []),
        "narrative_governance_requirements": payload.get("app_wiring_boundaries", []),
        "v558_handoff_ready": False,
        "v558_handoff_requirements_present": handoff_requirements_present,
        "permission_lane": "v558_runtime_input_gate",
        "render_permission_state": "blocked" if blockers else "context_only_not_renderable",
        "source_to_generation_separation_status": "present" if source_to_generation_ledger else "missing",
        "authority_status": "blocked" if blockers else "ready",
        "authority_source": "v557_renderer_contract_packet",
        "memory_write_permission": "forbidden",
        "narrative_continuity_permission": "forbidden",
        "generated_not_evidenced_flag": False,
        "blocked_reason": blockers[0]["blocker_code"] if blockers else "",
        "blocked_claim_ids_json": "[]",
        "normalized_at": utc_now(),
    }

    gate_status = "BLOCKED_V558_RUNTIME_INPUT_GATE" if blockers else "READY_V558_RUNTIME_INPUT_GATE"
    readiness = {
        "run_id": run_id,
        "status": gate_status,
        "final_status": gate_status,
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
            "forbidden_audit_path": bundle["forbidden_audit_path"],
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
        "normalized_runtime_input": normalized_runtime_input,
        "authority_documents": [
            repo_relative_path_text(ROOT / "docs" / "architecture_control" / "RAWLSING_COMPLETION_MAP.md"),
            repo_relative_path_text(ROOT / "docs" / "architecture_control" / "V552_TO_V557_LIVING_SYSTEM_NOTE.md"),
        ],
        "evidence_notes": [
            "V558 Pass 1 is a runtime-input normalization gate only.",
            "No runtime graft or app-facing code is implemented here.",
            "Missing governance evidence blocks readiness.",
        ],
    }

    report_path = root / "manifest" / "v558_runtime_input_gate_report.json"
    gate_packet_path = root / "packets" / "v558_runtime_input_gate.json"
    gate_parquet_path = root / "packets" / "v558_runtime_input_gate.parquet"
    audit_path = root / "audits" / "v558_runtime_input_normalization_audit.json"
    audit_parquet_path = root / "audits" / "v558_runtime_input_normalization_audit.parquet"
    validation_path = root / "manifest" / "v558_v557_contract_validation_report.json"
    schema_path = root / "schemas" / "v558_runtime_input_gate.schema.json"
    build_ledger_path = root / "manifest" / "v558_runtime_input_gate_build_ledger.json"

    build_record = build_review_gate_record(
        run_id=run_id,
        layer="v558",
        title="Runtime input gate",
        artifact_type="v558_runtime_input_gate",
        status=gate_status,
        input_inspection={
            "input_status": "blocked" if blockers else "ready",
            "missing_required_inputs": missing_inputs,
            "stop_missing_inputs": missing_inputs,
        },
        artifact_paths={
            "report_path": repo_relative_path_text(report_path),
            "gate_packet_path": repo_relative_path_text(gate_packet_path),
            "gate_parquet_path": repo_relative_path_text(gate_parquet_path),
            "audit_path": repo_relative_path_text(audit_path),
            "audit_parquet_path": repo_relative_path_text(audit_parquet_path),
            "validation_path": repo_relative_path_text(validation_path),
            "schema_path": repo_relative_path_text(schema_path),
        },
        how_built=[
            "read the V557 renderer-contract bundle",
            "normalize readiness, prompt-shape, and governance inputs",
            "record explicit blockers instead of inferring runtime permission",
            "write the runtime input gate, audit, validation report, and schema",
        ],
        continuity_notes=[
            "This is a review gate, not a runtime graft.",
            "Upstream continuity is checked for artifact presence and contract shape only.",
            "Downstream continuity remains intentionally untested here.",
        ],
    )
    build_ledger = {
        "run_id": run_id,
        "build_kind": "v558_runtime_input_gate",
        "final_status": gate_status,
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
            "Never claim runtime graft readiness when only review-gate normalization has been done.",
            "Never silence missing governance evidence.",
            "Never treat V557 prompt-shape or runtime-leak violations as admissible.",
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

    normalization_rows = [
        _input_field_audit(
            "v557_status",
            bundle["readiness_path"],
            v557_readiness.get("status"),
            v557_status,
            "_report_status(readiness_report)",
            "blocked" if v557_status == "blocked" else "pass",
            "V557 readiness state normalized for V558 gate.",
        ),
        _input_field_audit(
            "prompt_shape_detected",
            bundle["prompt_shape_audit_path"],
            v557_prompt_shape.get("prompt_shape_detected", v557_prompt_shape.get("prompt_shape_allowed")),
            prompt_shape_detected,
            "bool(prompt_shape_detected)",
            "blocked" if prompt_shape_detected else "pass",
            "Prompt-shape detection must remain explicit before any V558 pass.",
        ),
        _input_field_audit(
            "prompt_shape_violation_count",
            bundle["prompt_shape_audit_path"],
            v557_prompt_shape.get("prompt_shape_violation_count", v557_prompt_shape.get("violation_count")),
            prompt_shape_violation_count,
            "int(violation_count)",
            "blocked" if prompt_shape_violation_count else "pass",
            "Any prompt-shape violation blocks runtime input gating.",
        ),
        _input_field_audit(
            "prompt_shape_clear",
            bundle["prompt_shape_audit_path"],
            v557_prompt_shape.get("prompt_shape_clear"),
            prompt_shape_clear,
            "bool(prompt_shape_clear)",
            "blocked" if not prompt_shape_clear else "pass",
            "Prompt-shape clarity must be explicit before any V558 pass.",
        ),
        _input_field_audit(
            "prompt_shape_allowed",
            bundle["prompt_shape_audit_path"],
            v557_prompt_shape.get("prompt_shape_allowed"),
            prompt_shape_allowed,
            "always false; prompt-shape gating uses explicit detection flags",
            "blocked",
            "Prompt-shape allowed is never asserted positive in V558.",
        ),
        _input_field_audit(
            "runtime_packets_written",
            bundle["packet_path"],
            v557_packet_flags["runtime_packets_written"],
            False,
            "runtime packets are forbidden in V557 pass-through",
            "blocked" if v557_packet_flags["runtime_packets_written"] else "pass",
            "V557 must not leak runtime packets.",
        ),
        _input_field_audit(
            "persona_fields_written",
            bundle["packet_path"],
            v557_packet_flags["persona_fields_written"],
            False,
            "persona fields are forbidden in V557 pass-through",
            "blocked" if v557_packet_flags["persona_fields_written"] else "pass",
            "V557 must not leak persona fields.",
        ),
        _input_field_audit(
            "forbidden_outputs_written",
            bundle["packet_path"],
            v557_packet_flags["forbidden_outputs_written"],
            False,
            "forbidden outputs are forbidden in V557 pass-through",
            "blocked" if v557_packet_flags["forbidden_outputs_written"] else "pass",
            "Forbidden outputs cannot be passed into V558.",
        ),
        _input_field_audit(
            "dialogue_generated",
            bundle["packet_path"],
            v557_packet_flags["dialogue_generated"],
            False,
            "dialogue generation is not a V557 pass-through permission",
            "blocked" if v557_packet_flags["dialogue_generated"] else "pass",
            "Dialogue is a V558+ concern only after explicit authorization.",
        ),
        _input_field_audit(
            "voice_generated",
            bundle["packet_path"],
            v557_packet_flags["voice_generated"],
            False,
            "voice generation is not a V557 pass-through permission",
            "blocked" if v557_packet_flags["voice_generated"] else "pass",
            "Voice is a V558+ concern only after explicit authorization.",
        ),
        _input_field_audit(
            "source_to_generation_separation_ledger",
            bundle["packet_path"],
            bool(source_to_generation_ledger),
            bool(source_to_generation_ledger),
            "presence check on V557 source-to-generation ledger",
            "blocked" if not source_to_generation_ledger else "pass",
            "The runtime gate must see a source-to-generation separation ledger.",
        ),
        _input_field_audit(
            "governance_pack_present",
            governance["root"],
            governance["present"],
            governance["present"],
            "governance inventory check",
            "blocked" if not governance["present"] else "pass",
            "App-facing governance is required for runtime-graft review.",
        ),
        _input_field_audit(
            "v558_handoff_requirements_present",
            bundle["packet_path"],
            handoff_requirements_present,
            handoff_requirements_present,
            "normalize renderer contract requirements before pass 2",
            "blocked" if not handoff_requirements_present else "pass",
            "The normalized runtime input must expose handoff requirements.",
        ),
    ]

    gate_rows = [
        {
            "run_id": run_id,
            "status": gate_status,
            "final_status": gate_status,
            "ready_for_runtime_graft_review": not blockers,
            "ready_for_runtime_graft": False,
            "blocker_count": len(blockers),
            "missing_inputs_json": json.dumps(missing_inputs, sort_keys=True),
            "blockers_json": json.dumps(blockers, sort_keys=True),
            "normalized_permission_lane": normalized_runtime_input["permission_lane"],
            "render_permission_state": normalized_runtime_input["render_permission_state"],
            "source_to_generation_separation_status": normalized_runtime_input["source_to_generation_separation_status"],
            "prompt_shape_allowed": prompt_shape_allowed,
            "prompt_shape_violation_count": prompt_shape_violation_count,
            "governance_present": governance["present"],
            "v557_status": v557_status,
            "v558_handoff_ready": normalized_runtime_input["v558_handoff_ready"],
            "v558_handoff_requirements_present": normalized_runtime_input["v558_handoff_requirements_present"],
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]

    _write_json(report_path, readiness)
    _write_json(gate_packet_path, normalized_runtime_input)
    _write_parquet(gate_parquet_path, gate_rows)
    _write_json(audit_path, {"run_id": run_id, "rows": normalization_rows, "row_count": len(normalization_rows), "created_at": utc_now()})
    _write_parquet(audit_parquet_path, normalization_rows)
    _write_json(validation_path, {"run_id": run_id, "valid": not blockers, "errors": [blocker["blocker_code"] for blocker in blockers], "blockers": blockers, "created_at": utc_now()})
    _write_json(
        schema_path,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "v558_runtime_input_gate",
            "type": "object",
            "required": [
                "run_id",
                "status",
                "ready_for_runtime_graft_review",
                "normalized_runtime_input",
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
                "normalized_runtime_input": {"type": "object"},
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
            "gate_packet_path": repo_relative_path_text(gate_packet_path),
            "gate_parquet_path": repo_relative_path_text(gate_parquet_path),
            "audit_path": repo_relative_path_text(audit_path),
            "audit_parquet_path": repo_relative_path_text(audit_parquet_path),
            "validation_path": repo_relative_path_text(validation_path),
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


def validate_v558_runtime_input_gate(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("ready_for_runtime_graft"):
        errors.append("V558 must not mark runtime graft as already complete")
    for key in ("report_path", "gate_packet_path", "audit_path", "validation_path", "schema_path", "build_ledger_path"):
        value = readiness.get(key)
        if not value or not Path(str(value)).exists():
            errors.append(f"missing {key}")
    if readiness.get("blocker_count", 0) < 0:
        errors.append("negative blocker count")
    normalized = readiness.get("normalized_runtime_input", {})
    if not isinstance(normalized, dict) or not normalized:
        errors.append("missing normalized runtime input")
    else:
        if normalized.get("render_permission_state") == "blocked" and not readiness.get("blockers"):
            errors.append("blocked render permission state requires blockers")
        if normalized.get("v558_handoff_ready"):
            errors.append("v558_handoff_ready must remain false in pass 1")
    for key in ("implementation_kind", "provisionality", "scaffold_level", "how_built", "continuity_notes"):
        if not readiness.get(key):
            errors.append(f"missing {key}")
    return errors


__all__ = [
    "COMPILER_VERSION",
    "DEFAULT_GOVERNANCE_ROOT",
    "DEFAULT_V558_OUTPUT_ROOT",
    "SCHEMA_VERSION",
    "build_v558_runtime_input_gate",
    "validate_v558_runtime_input_gate",
]
