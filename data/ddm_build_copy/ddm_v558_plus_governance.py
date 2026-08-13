#!/usr/bin/env python3
"""Build the V558+ runtime governance bundle.

This layer sits after the current V558 review gates and prepares the
deployment/evaluation/memory/narrative governance artifacts required by the
V558+ section pack. It does not implement runtime persona generation, app
delivery, or any raw DDM access path.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_v5_build_standard import build_review_gate_record
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, write_frame_artifact, write_json_artifact

try:  # pragma: no cover - keeps patch tests runnable outside the full repo
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover - fallback for isolated tests
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_V558_PLUS_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v558_plus" / "runs"
DEFAULT_GOVERNANCE_ROOT = ROOT / "docs" / "architecture_control" / "imported_packs" / "10_rawlsing_final_cohesion_review_override_pack_20260622"

SCHEMA_VERSION = "v558_plus_governance_0.1"
COMPILER_VERSION = "v558_plus_governance_0.1"

ALLOWED_READY_STATUSES = {
    "V558_BLOCKED_NO_V557_CONTRACT",
    "V558_BLOCKED_V557_NOT_READY",
    "V558_BLOCKED_MISSING_GENERATION_LEDGER",
    "V558_BLOCKED_MISSING_EVALUATOR",
    "V558_BLOCKED_MISSING_MEMORY_GOVERNANCE",
    "V558_BLOCKED_RAW_DDM_ACCESS",
    "V558_BLOCKED_PROMPT_SHAPE_LAUNDERING",
    "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
    "V558_READY_FOR_LIMITED_EVALUATED_RUNTIME",
    "V558_READY_FOR_APP_INTEGRATION_REVIEW",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_v558_bundle(v558_run_root: Path) -> dict[str, Any]:
    manifest = v558_run_root / "manifest"
    packets = v558_run_root / "packets"
    audits = v558_run_root / "audits"
    readiness_path = manifest / "v558_runtime_input_gate_report.json"
    gate_packet_path = packets / "v558_runtime_input_gate.json"
    graft_readiness_path = manifest / "v558_runtime_graft_readiness_report.json"
    validation_path = manifest / "v558_v557_contract_validation_report.json"
    normalization_audit_path = audits / "v558_runtime_input_normalization_audit.json"
    required_inputs = {
        "v558_runtime_input_gate_report": readiness_path,
        "v558_runtime_input_gate": gate_packet_path,
        "v558_runtime_graft_readiness_report": graft_readiness_path,
        "v558_v557_contract_validation_report": validation_path,
    }
    missing_required_inputs = [name for name, path in required_inputs.items() if not path.exists()]
    return {
        "readiness_path": repo_relative_path_text(readiness_path),
        "gate_packet_path": repo_relative_path_text(gate_packet_path),
        "graft_readiness_path": repo_relative_path_text(graft_readiness_path),
        "validation_path": repo_relative_path_text(validation_path),
        "normalization_audit_path": repo_relative_path_text(normalization_audit_path),
        "required_inputs": {name: repo_relative_path_text(path) for name, path in required_inputs.items()},
        "missing_required_inputs": missing_required_inputs,
        "required_inputs_present": not missing_required_inputs,
        "readiness": _read_json(readiness_path),
        "gate_packet": _read_json(gate_packet_path),
        "graft_readiness": _read_json(graft_readiness_path),
        "validation": _read_json(validation_path),
        "normalization_audit": _read_json(normalization_audit_path),
    }


def _governance_inventory(governance_root: Path) -> dict[str, Any]:
    if not governance_root.exists():
        return {
            "root": repo_relative_path_text(governance_root),
            "present": False,
            "files": [],
        }
    files = sorted(repo_relative_path_text(path) for path in governance_root.rglob("*") if path.is_file())
    return {
        "root": repo_relative_path_text(governance_root),
        "present": bool(files),
        "files": files,
    }


def _first_blocker_code(*collections: list[dict[str, Any]]) -> str:
    for collection in collections:
        for blocker in collection:
            code = _clean(blocker.get("blocker_code") or blocker.get("code") or blocker.get("reason"))
            if code:
                return code
    return ""


def _status_from_inputs(*, v558_readiness: dict[str, Any], v558_graft_readiness: dict[str, Any], governance_present: bool) -> tuple[str, list[dict[str, Any]]]:
    blockers: list[dict[str, Any]] = []
    if not v558_readiness:
        blockers.append(
            {
                "blocker_code": "missing_required_v558_inputs",
                "status": "blocked",
                "details": ["v558_runtime_input_gate_report"],
            }
        )
    if not v558_graft_readiness:
        blockers.append(
            {
                "blocker_code": "missing_required_v558_inputs",
                "status": "blocked",
                "details": ["v558_runtime_graft_readiness_report"],
            }
        )
    v558_status = _clean(v558_readiness.get("status") or v558_readiness.get("final_status"))
    v558_gate = v558_readiness.get("normalized_runtime_input", {})
    prompt_shape_detected = _boolish(v558_gate.get("prompt_shape_detected"))
    prompt_shape_violation_count = int(v558_gate.get("prompt_shape_violation_count", 0) or 0)
    prompt_shape_clear = _boolish(v558_gate.get("prompt_shape_clear", not prompt_shape_detected and prompt_shape_violation_count == 0))
    prompt_shape_allowed = _boolish(v558_gate.get("prompt_shape_allowed"))

    if v558_readiness and _clean(v558_status).startswith("BLOCKED"):
        blockers.extend(v558_readiness.get("blockers", []))
    if v558_graft_readiness and _clean(v558_graft_readiness.get("status")).startswith("BLOCKED"):
        blockers.extend(v558_graft_readiness.get("blockers", []))

    if not governance_present:
        blockers.append(
            {
                "blocker_code": "missing_final_cohesion_pack",
                "status": "blocked",
                "details": {
                    "governance_root": DEFAULT_GOVERNANCE_ROOT.as_posix(),
                    "required_pack": "10_rawlsing_final_cohesion_review_override_pack_20260622",
                },
            }
        )

    if prompt_shape_detected or prompt_shape_violation_count > 0 or not prompt_shape_clear or prompt_shape_allowed:
        blockers.append(
            {
                "blocker_code": "v557_prompt_shape_violation",
                "status": "blocked",
                "details": {
                    "prompt_shape_detected": prompt_shape_detected,
                    "prompt_shape_violation_count": prompt_shape_violation_count,
                    "prompt_shape_clear": prompt_shape_clear,
                    "prompt_shape_allowed": prompt_shape_allowed,
                },
            }
        )

    if blockers:
        blocked_code = _first_blocker_code(blockers)
        if blocked_code in {"missing_required_v557_inputs", "missing_v557_contract", "v557_not_ready_for_v558"}:
            return "V558_BLOCKED_V557_NOT_READY", blockers
        if blocked_code == "v557_prompt_shape_violation":
            return "V558_BLOCKED_PROMPT_SHAPE_LAUNDERING", blockers
        if blocked_code == "v557_leaks_runtime_material":
            return "V558_BLOCKED_RAW_DDM_ACCESS", blockers
        if blocked_code in {"missing_app_facing_governance_pack", "missing_final_cohesion_pack"}:
            return "V558_BLOCKED_MISSING_MEMORY_GOVERNANCE", blockers
        if blocked_code == "missing_authority_documents":
            return "V558_BLOCKED_MISSING_EVALUATOR", blockers
        if blocked_code == "missing_generation_permission_ledger":
            return "V558_BLOCKED_MISSING_GENERATION_LEDGER", blockers
        return "V558_BLOCKED_V557_NOT_READY", blockers

    return "V558_READY_FOR_SANDBOX_RUNTIME_ONLY", blockers


def _make_gate_rows(
    *,
    run_id: str,
    v558_run_root: Path,
    v558_bundle: dict[str, Any],
    governance: dict[str, Any],
    status: str,
    blockers: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    readiness = v558_bundle["readiness"]
    gate = v558_bundle["gate_packet"]
    v557 = gate.get("v557", {}) if isinstance(gate, dict) else {}
    normalized = gate.get("normalized_runtime_input", {}) if isinstance(gate, dict) else {}
    graft = v558_bundle["graft_readiness"]
    v557_status = _clean(v557.get("status") or normalized.get("v557_status") or readiness.get("v557", {}).get("status"))
    prompt_shape_detected = _boolish(normalized.get("prompt_shape_detected", v557.get("prompt_shape_detected")))
    prompt_shape_violation_count = int(normalized.get("prompt_shape_violation_count", v557.get("prompt_shape_violation_count", 0)) or 0)
    prompt_shape_clear = _boolish(normalized.get("prompt_shape_clear", v557.get("prompt_shape_clear", not prompt_shape_detected and prompt_shape_violation_count == 0)))
    prompt_shape_allowed = _boolish(normalized.get("prompt_shape_allowed", v557.get("prompt_shape_allowed", False)))

    runtime_gate_row = {
        "run_id": run_id,
        "v558_run_root": repo_relative_path_text(v558_run_root),
        "status": status,
        "ready_for_sandbox_runtime_only": status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
        "ready_for_limited_evaluated_runtime": False,
        "ready_for_app_integration_review": False,
        "runtime_generation_authorized": False,
        "evaluation_harness_authorized": status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
        "v557_status": v557_status,
        "v557_ready_for_semantic_deepening": _boolish(normalized.get("ready_for_semantic_deepening", v557.get("ready_for_semantic_deepening"))),
        "v557_ready_for_runtime_consumption": _boolish(normalized.get("ready_for_runtime_consumption", v557.get("ready_for_runtime_consumption"))),
        "prompt_shape_detected": prompt_shape_detected,
        "prompt_shape_violation_count": prompt_shape_violation_count,
        "prompt_shape_clear": prompt_shape_clear,
        "prompt_shape_allowed": prompt_shape_allowed,
        "governance_present": governance["present"],
        "governance_root": governance["root"],
        "blocker_count": len(blockers),
        "blocked_claim_ids_json": json.dumps(
            sorted(
                {
                    _clean(item.get("blocker_code") or item.get("reason"))
                    for item in blockers
                    if _clean(item.get("blocker_code") or item.get("reason"))
                }
            ),
            ensure_ascii=False,
        ),
        "created_at": utc_now(),
        "schema_version": SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
    }

    audit_rows = []
    audit_rows.append(
        {
            "audit_id": f"{run_id}__v557_status",
            "source_path": v558_bundle["readiness_path"],
            "field_name": "v557_status",
            "source_value": v557_status,
            "normalized_value": v557_status,
            "audit_status": "pass" if v557_status and not v557_status.startswith("BLOCKED") else "blocked",
            "reason": "Normalized from V558 review gate.",
        }
    )
    audit_rows.append(
        {
            "audit_id": f"{run_id}__prompt_shape_detected",
            "source_path": v558_bundle["normalization_audit_path"],
            "field_name": "prompt_shape_detected",
            "source_value": str(prompt_shape_detected),
            "normalized_value": str(prompt_shape_detected),
            "audit_status": "blocked" if prompt_shape_detected or prompt_shape_violation_count > 0 else "pass",
            "reason": "Prompt shape must remain explicitly audited.",
        }
    )
    audit_rows.append(
        {
            "audit_id": f"{run_id}__governance_presence",
            "source_path": governance["root"],
            "field_name": "final_cohesion_pack_present",
            "source_value": str(governance["present"]),
            "normalized_value": str(governance["present"]),
            "audit_status": "pass" if governance["present"] else "blocked",
            "reason": "Final cohesion authority is required for V558+ review.",
        }
    )
    audit_rows.append(
        {
            "audit_id": f"{run_id}__graft_status",
            "source_path": v558_bundle["graft_readiness_path"],
            "field_name": "v558_graft_status",
            "source_value": _clean(graft.get("status")),
            "normalized_value": _clean(graft.get("status")),
            "audit_status": "pass" if _clean(graft.get("status")).startswith("READY") else "blocked",
            "reason": "Graft readiness stays review-bound, not runtime-authorized.",
        }
    )

    validation_row = {
        "run_id": run_id,
        "v558_run_root": repo_relative_path_text(v558_run_root),
        "v557_status": v557_status,
        "v557_ready_for_semantic_deepening": _boolish(normalized.get("ready_for_semantic_deepening", v557.get("ready_for_semantic_deepening"))),
        "v557_ready_for_runtime_consumption": _boolish(normalized.get("ready_for_runtime_consumption", v557.get("ready_for_runtime_consumption"))),
        "prompt_shape_detected": prompt_shape_detected,
        "prompt_shape_violation_count": prompt_shape_violation_count,
        "prompt_shape_clear": prompt_shape_clear,
        "prompt_shape_allowed": prompt_shape_allowed,
        "governance_present": governance["present"],
        "validation_status": status,
        "blocker_count": len(blockers),
        "blocked_claim_ids_json": runtime_gate_row["blocked_claim_ids_json"],
        "created_at": utc_now(),
        "schema_version": SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
    }
    return [runtime_gate_row, validation_row], audit_rows


def _generation_permission_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    permissions = [
        ("constraint_preserving_generation", "sandbox_review_only", "allowed only as constraint-led review material"),
        ("style_generation", "blocked", "no voice/style generation without later authorization"),
        ("narrative_placeholder_generation", "blocked", "placeholders must not become lived memory"),
        ("dialogue_generation", "blocked", "not implemented in V558+ governance pass"),
        ("memory_generation", "blocked", "no generated memory markers without explicit policy"),
    ]
    for idx, (generation_class, permission_state, reason) in enumerate(permissions, start=1):
        rows.append(
            {
                "permission_id": f"v558p_perm_{idx}",
                "generation_class": generation_class,
                "permission_state": permission_state,
                "permission_reason": reason,
                "allowed_runtime_use_class": "review_only" if permission_state != "blocked" else "blocked",
                "memory_permission": "forbidden" if generation_class != "constraint_preserving_generation" else "review_only",
                "narrative_continuity_permission": "forbidden" if generation_class != "constraint_preserving_generation" else "review_only",
                "blocked_claim_ids_json": "[]",
                "schema_version": SCHEMA_VERSION,
                "compiler_version": COMPILER_VERSION,
                "created_at": utc_now(),
            }
        )
    return rows


def _runtime_constraint_rows(v558_gate: dict[str, Any], status: str) -> list[dict[str, Any]]:
    normalized = v558_gate.get("normalized_runtime_input", {})
    return [
        {
            "constraint_id": "v558p_runtime_constraint_1",
            "constraint_type": "source_to_generation_separation",
            "constraint_value": _clean(normalized.get("source_to_generation_separation_status")) or "present",
            "constraint_status": "required",
            "constraint_summary": "V5 source structure cannot be treated as persona content.",
            "status": status,
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
            "created_at": utc_now(),
        },
        {
            "constraint_id": "v558p_runtime_constraint_2",
            "constraint_type": "prompt_shape",
            "constraint_value": f"detected={_boolish(normalized.get('prompt_shape_detected'))};violations={int(normalized.get('prompt_shape_violation_count', 0) or 0)}",
            "constraint_status": "required",
            "constraint_summary": "Prompt construction must stay free of raw evidence and autobiographical leakage.",
            "status": status,
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
            "created_at": utc_now(),
        },
        {
            "constraint_id": "v558p_runtime_constraint_3",
            "constraint_type": "runtime_use_class",
            "constraint_value": "sandbox_review_only",
            "constraint_status": "required",
            "constraint_summary": "This bundle does not authorize app-facing runtime.",
            "status": status,
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
            "created_at": utc_now(),
        },
    ]


def _prompt_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    prohibited = [
        "raw_evidence",
        "first_person_memory",
        "survey_fact_as_autobiography",
        "voice_overreach",
        "parent_biography",
        "carrier_membership",
        "final_enneagram_type",
        "prompt_shape_laundering",
    ]
    for idx, name in enumerate(prohibited, start=1):
        rows.append(
            {
                "prompt_audit_id": f"v558p_prompt_audit_{idx}",
                "prompt_shape_detected": True,
                "prompt_shape_violation_count": 1,
                "prompt_shape_clear": False,
                "prompt_shape_allowed": False,
                "violation_type": name,
                "audit_status": "blocked",
                "details": f"{name} is prohibited by V558+ governance.",
                "created_at": utc_now(),
                "schema_version": SCHEMA_VERSION,
                "compiler_version": COMPILER_VERSION,
            }
        )
    rows.append(
        {
            "prompt_audit_id": "v558p_prompt_audit_baseline",
            "prompt_shape_detected": False,
            "prompt_shape_violation_count": 0,
            "prompt_shape_clear": True,
            "prompt_shape_allowed": False,
            "violation_type": "baseline_no_prompt_generated",
            "audit_status": "pass",
            "details": "No runtime prompt has been generated in this governance pass.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    )
    return rows


def _adapter_rows() -> dict[str, list[dict[str, Any]]]:
    raw_ddm_blocklist = [
        ("V550 raw substrate", "blocked"),
        ("V550J joint pattern raw tables", "blocked"),
        ("V551 relation atoms", "blocked"),
        ("V551J candidate/review/certified/sidecar tables", "blocked"),
        ("V552 structural handoff tables", "blocked"),
        ("V552J structural handoff tables", "blocked"),
        ("V553 temporal pressure raw/internal tables", "blocked"),
        ("V554 seed raw/internal tables", "blocked"),
        ("V555 mediation raw/internal tables", "blocked"),
        ("V556 pressure-flow raw/internal tables", "blocked"),
    ]
    v3_rows = [
        {
            "adapter_id": "v558p_v3_adapter",
            "adapter_name": "v5_to_v3_runtime_constraint_adapter",
            "source_layer": "V558_PLUS",
            "target_layer": "v3",
            "allowed_input_classes": [
                "temporal_pressure_constraint",
                "mediation_unresolved_slot",
                "candidate_pressure_flow_precondition",
                "nonrenderable_blocker",
                "uncertainty_absence_condition",
                "evaluator_obligation",
            ],
            "forbidden_input_classes": [
                "raw_survey_evidence",
                "biography",
                "final_type",
                "raw_ddm_tables",
            ],
            "runtime_use_class": "constraint_adapter_only",
            "status": "contract_only",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]
    v2_rows = [
        {
            "contract_id": "v558p_v2_surface_contract",
            "surface_name": "v2_conversation_shell",
            "source_layer": "V558_PLUS",
            "allowed_use": "conversation_shell_after_governance",
            "forbidden_use": "originating_v5_meaning",
            "runtime_use_class": "surface_only",
            "status": "blocked_for_runtime_generation",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]
    server_rows = [
        {
            "contract_id": "v558p_server_api_contract",
            "route": "/runtime/generate",
            "allowed_use": "V558_PLUS_handoff_only",
            "forbidden_use": "raw_ddm_reads",
            "runtime_use_class": "server_api_contract_only",
            "status": "blocked_for_runtime_generation",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]
    web_rows = [
        {
            "contract_id": "v558p_web_display_contract",
            "surface": "runtime_display",
            "allowed_use": "evaluated_runtime_output_only",
            "forbidden_use": "raw_ddm_display",
            "runtime_use_class": "web_display_contract_only",
            "status": "blocked_for_runtime_generation",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]
    return {
        "raw_ddm_access_blocklist": [
            {
                "blocklist_id": f"v558p_block_{idx}",
                "blocked_source": source,
                "block_status": status,
                "reason": "raw DDM cannot be read directly by V558+ runtime generation",
                "schema_version": SCHEMA_VERSION,
                "compiler_version": COMPILER_VERSION,
                "created_at": utc_now(),
            }
            for idx, (source, status) in enumerate(raw_ddm_blocklist, start=1)
        ],
        "v3_adapter_contract": v3_rows,
        "v2_surface_contract": v2_rows,
        "server_api_contract": server_rows,
        "web_display_contract": web_rows,
    }


def _evaluator_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    evaluator_rows = []
    for idx, evaluator in enumerate(
        [
            "evidence_laundering",
            "biography_invention",
            "voice_overreach",
            "memory_status",
            "parent_story",
            "carrier_membership",
            "final_type",
            "raw_ddm_leak",
            "prompt_shape",
            "narrative_continuity",
        ],
        start=1,
    ):
        evaluator_rows.append(
            {
                "evaluator_id": f"v558p_eval_{idx}",
                "evaluator_name": evaluator,
                "required_for_runtime": True,
                "blocks_on_failure": True,
                "result_status": "not_run",
                "blocked_claim_ids_json": "[]",
                "evaluation_scope": "contract_only",
                "created_at": utc_now(),
                "schema_version": SCHEMA_VERSION,
                "compiler_version": COMPILER_VERSION,
            }
        )

    result_rows = [
        {
            "evaluator_result_id": f"v558p_eval_result_{idx}",
            "evaluator_name": row["evaluator_name"],
            "result_status": "not_run",
            "blocker_code": "runtime_generation_not_implemented",
            "review_status": "contract_only",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
        for idx, row in enumerate(evaluator_rows, start=1)
    ]
    return evaluator_rows, result_rows


def _memory_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    memory_policy_rows = [
        {
            "policy_id": "v558p_memory_policy_1",
            "memory_class": "user_provided_memory",
            "may_be_source_truth": True,
            "may_be_generated_truth": False,
            "policy_status": "allowed",
            "details": "User-provided memory is retained as user memory, not generated memory.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
        {
            "policy_id": "v558p_memory_policy_2",
            "memory_class": "generated_persona_continuity_marker",
            "may_be_source_truth": False,
            "may_be_generated_truth": True,
            "policy_status": "blocked",
            "details": "Generated continuity markers may not become source fact.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
        {
            "policy_id": "v558p_memory_policy_3",
            "memory_class": "generated_scene_placeholder",
            "may_be_source_truth": False,
            "may_be_generated_truth": True,
            "policy_status": "blocked",
            "details": "Placeholder scenes are not autobiographical memory.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
        {
            "policy_id": "v558p_memory_policy_4",
            "memory_class": "source_derived_constraint",
            "may_be_source_truth": True,
            "may_be_generated_truth": False,
            "policy_status": "allowed",
            "details": "Constraints may feed generation only as constraints.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
        {
            "policy_id": "v558p_memory_policy_5",
            "memory_class": "forbidden_memory_candidate",
            "may_be_source_truth": False,
            "may_be_generated_truth": False,
            "policy_status": "blocked",
            "details": "Forbidden memory candidates must be audited, not stored as truth.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
    ]

    memory_ledger_rows = [
        {
            "ledger_id": "v558p_memory_ledger_1",
            "memory_class": row["memory_class"],
            "retention_state": row["policy_status"],
            "source_truth_allowed": row["may_be_source_truth"],
            "generated_truth_allowed": row["may_be_generated_truth"],
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
        for row in memory_policy_rows
    ]

    generated_vs_evidenced_rows = [
        {
            "audit_id": "v558p_generated_vs_evidenced_1",
            "generated_memory_count": 0,
            "evidenced_memory_count": 0,
            "evidence_laundering_scan_status": "not_run",
            "source_to_generation_separation_ok": True,
            "audit_status": "pass",
            "details": "No runtime generation was executed in this governance pass.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]
    return memory_policy_rows, memory_ledger_rows, generated_vs_evidenced_rows


def _narrative_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    policy_rows = [
        {
            "policy_id": "v558p_narrative_policy_1",
            "continuity_class": "generated_origin",
            "may_be_revised": True,
            "may_be_contradicted": True,
            "policy_status": "review_only",
            "details": "Generated continuity is revisable and non-evidentiary.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
        {
            "policy_id": "v558p_narrative_policy_2",
            "continuity_class": "source_history",
            "may_be_revised": False,
            "may_be_contradicted": False,
            "policy_status": "evidentiary_only",
            "details": "Source history remains source history; it is not generated narrative.",
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        },
    ]
    ledger_rows = [
        {
            "ledger_id": "v558p_narrative_ledger_1",
            "continuity_class": row["continuity_class"],
            "may_recur": row["may_be_revised"],
            "may_be_revised": row["may_be_revised"],
            "may_be_contradicted": row["may_be_contradicted"],
            "ledger_status": row["policy_status"],
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
        for row in policy_rows
    ]
    return policy_rows, ledger_rows


def _surface_generation_rows(status: str, blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "surface_generation_id": "v558p_surface_generation_1",
            "surface_generation_status": "sandbox_only" if status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY" else "blocked",
            "generated_unit_count": 0,
            "generated_not_evidenced_flag": True,
            "runtime_use_class": "sandbox_review_only",
            "blocked_reason": _first_blocker_code(blockers) or "runtime_generation_not_implemented",
            "blocked_claim_ids_json": json.dumps(
                sorted(
                    {
                        _clean(item.get("blocker_code") or item.get("reason"))
                        for item in blockers
                        if _clean(item.get("blocker_code") or item.get("reason"))
                    }
                ),
                ensure_ascii=False,
            ),
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]


def _runtime_safety_rows(status: str, blockers: list[dict[str, Any]], gate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gate_row = gate_rows[0]
    validation_row = gate_rows[1]
    return [
        {
            "readiness_id": "v558p_runtime_safety_1",
            "status": status,
            "final_status": status,
            "ready_for_sandbox_runtime_only": status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
            "ready_for_limited_evaluated_runtime": False,
            "ready_for_app_integration_review": False,
            "runtime_generation_authorized": False,
            "evaluation_harness_authorized": status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
            "app_handoff_ready": False,
            "blocker_count": len(blockers),
            "blocker_codes_json": gate_row["blocked_claim_ids_json"],
            "v557_status": gate_row["v557_status"],
            "prompt_shape_detected": gate_row["prompt_shape_detected"],
            "prompt_shape_violation_count": gate_row["prompt_shape_violation_count"],
            "prompt_shape_clear": gate_row["prompt_shape_clear"],
            "prompt_shape_allowed": gate_row["prompt_shape_allowed"],
            "validation_status": validation_row["validation_status"],
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]


def _app_handoff_rows(status: str, blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "app_handoff_id": "v558p_app_handoff_1",
            "app_handoff_status": "sandbox_only" if status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY" else "blocked",
            "ready_for_app_integration_review": False,
            "ready_for_runtime_handoff": False,
            "runtime_use_class": "app_handoff_review_only",
            "blocked_reason": _first_blocker_code(blockers) or "no_runtime_generation_implemented",
            "blocked_claim_ids_json": json.dumps(
                sorted(
                    {
                        _clean(item.get("blocker_code") or item.get("reason"))
                        for item in blockers
                        if _clean(item.get("blocker_code") or item.get("reason"))
                    }
                ),
                ensure_ascii=False,
            ),
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
        }
    ]


def _bundle_artifact(
    *,
    output_dirs: dict[str, Path],
    stem: str,
    rows: list[dict[str, Any]],
    payload: dict[str, Any] | list[dict[str, Any]],
    section: str = "packets",
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    df = pd.DataFrame(rows)
    if df.empty and rows == []:
        df = pd.DataFrame(columns=[])
    json_path = output_dirs[section] / f"{stem}.json"
    parquet_path = output_dirs[section] / f"{stem}.parquet"
    schema_path = output_dirs["schemas"] / f"{stem}.schema.json"
    write_json_artifact(json_path, payload if isinstance(payload, dict) else {"rows": payload, "row_count": len(rows)})
    frame_info = write_frame_artifact(
        df,
        path=parquet_path,
        schema_path=schema_path,
        name=stem,
        run_id=payload["run_id"] if isinstance(payload, dict) and "run_id" in payload else rows[0].get("run_id", "") if rows else "",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    return {
        "json_path": repo_relative_path_text(json_path),
        "parquet_path": repo_relative_path_text(parquet_path),
        "schema_path": repo_relative_path_text(schema_path),
        "rows": frame_info["rows"],
    }


def build_v558_plus_governance(
    *,
    run_id: str,
    v558_run_root: str | Path,
    output_root: str | Path = DEFAULT_V558_PLUS_OUTPUT_ROOT,
    governance_root: str | Path | None = None,
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    output_dirs = ensure_output_dirs(output_root, run_id)
    v558_run_root = Path(v558_run_root)
    governance_root_path = Path(governance_root) if governance_root is not None else DEFAULT_GOVERNANCE_ROOT

    v558_bundle = _read_v558_bundle(v558_run_root)
    governance = _governance_inventory(governance_root_path)
    status, blockers = _status_from_inputs(
        v558_readiness=v558_bundle["readiness"],
        v558_graft_readiness=v558_bundle["graft_readiness"] or v558_bundle["readiness"],
        governance_present=governance["present"],
    )
    if not v558_bundle["required_inputs_present"]:
        blockers.insert(
            0,
            {
                "blocker_code": "missing_required_v558_inputs",
                "status": "blocked",
                "details": v558_bundle["missing_required_inputs"],
            },
        )
        status = "V558_BLOCKED_NO_V557_CONTRACT"
    gate_rows, normalization_rows = _make_gate_rows(
        run_id=run_id,
        v558_run_root=v558_run_root,
        v558_bundle=v558_bundle,
        governance=governance,
        status=status,
        blockers=blockers,
    )

    runtime_gate_payload = gate_rows[0]
    validation_payload = gate_rows[1]
    normalization_payload = {
        "run_id": run_id,
        "rows": normalization_rows,
        "row_count": len(normalization_rows),
        "created_at": utc_now(),
    }
    runtime_constraint_rows = _runtime_constraint_rows(v558_bundle["gate_packet"], status)
    generation_permission_rows = _generation_permission_rows()
    surface_generation_rows = _surface_generation_rows(status, blockers)
    prompt_audit_rows = _prompt_audit_rows()
    adapters = _adapter_rows()
    evaluator_contract_rows, evaluator_result_rows = _evaluator_rows()
    memory_policy_rows, memory_ledger_rows, generated_vs_evidenced_rows = _memory_rows()
    narrative_policy_rows, narrative_ledger_rows = _narrative_rows()
    runtime_safety_rows = _runtime_safety_rows(status, blockers, gate_rows)
    app_handoff_rows = _app_handoff_rows(status, blockers)

    artifact_paths: dict[str, dict[str, Any]] = {}
    artifact_paths["runtime_gate"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_runtime_gate",
        rows=gate_rows,
        payload={"run_id": run_id, "rows": gate_rows, "row_count": len(gate_rows), "created_at": utc_now()},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["runtime_input_normalization_audit"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_runtime_input_normalization_audit",
        rows=normalization_rows,
        payload=normalization_payload,
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["v557_contract_validation_report"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_v557_contract_validation_report",
        rows=[validation_payload],
        payload=validation_payload,
        section="manifest",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["runtime_constraint_packet"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_runtime_constraint_packet",
        rows=runtime_constraint_rows,
        payload={"run_id": run_id, "rows": runtime_constraint_rows, "row_count": len(runtime_constraint_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["generation_permission_ledger"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_generation_permission_ledger",
        rows=generation_permission_rows,
        payload={"run_id": run_id, "rows": generation_permission_rows, "row_count": len(generation_permission_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["surface_generation_packet"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_surface_generation_packet",
        rows=surface_generation_rows,
        payload={"run_id": run_id, "rows": surface_generation_rows, "row_count": len(surface_generation_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["generated_unit_index"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_generated_unit_index",
        rows=[],
        payload={"run_id": run_id, "rows": [], "row_count": 0, "generated_unit_count": 0},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["prompt_construction_audit"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_prompt_construction_audit",
        rows=prompt_audit_rows,
        payload={"run_id": run_id, "rows": prompt_audit_rows, "row_count": len(prompt_audit_rows)},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["v3_adapter_contract"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_v3_adapter_contract",
        rows=adapters["v3_adapter_contract"],
        payload={"run_id": run_id, "rows": adapters["v3_adapter_contract"], "row_count": len(adapters["v3_adapter_contract"])},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["v2_surface_contract"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_v2_surface_contract",
        rows=adapters["v2_surface_contract"],
        payload={"run_id": run_id, "rows": adapters["v2_surface_contract"], "row_count": len(adapters["v2_surface_contract"])},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["server_api_contract"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_server_api_contract",
        rows=adapters["server_api_contract"],
        payload={"run_id": run_id, "rows": adapters["server_api_contract"], "row_count": len(adapters["server_api_contract"])},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["web_display_contract"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_web_display_contract",
        rows=adapters["web_display_contract"],
        payload={"run_id": run_id, "rows": adapters["web_display_contract"], "row_count": len(adapters["web_display_contract"])},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["raw_ddm_access_blocklist"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_raw_ddm_access_blocklist",
        rows=adapters["raw_ddm_access_blocklist"],
        payload={"run_id": run_id, "rows": adapters["raw_ddm_access_blocklist"], "row_count": len(adapters["raw_ddm_access_blocklist"])},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["evaluator_contract"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_evaluator_contract",
        rows=evaluator_contract_rows,
        payload={"run_id": run_id, "rows": evaluator_contract_rows, "row_count": len(evaluator_contract_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["evaluator_result_index"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_evaluator_result_index",
        rows=evaluator_result_rows,
        payload={"run_id": run_id, "rows": evaluator_result_rows, "row_count": len(evaluator_result_rows)},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["forbidden_claim_audit"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_forbidden_claim_audit",
        rows=[],
        payload={"run_id": run_id, "rows": [], "row_count": 0, "audit_status": "pass"},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["prompt_shape_audit"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_prompt_shape_audit",
        rows=prompt_audit_rows,
        payload={"run_id": run_id, "rows": prompt_audit_rows, "row_count": len(prompt_audit_rows)},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["memory_policy"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_memory_policy",
        rows=memory_policy_rows,
        payload={"run_id": run_id, "rows": memory_policy_rows, "row_count": len(memory_policy_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["memory_write_ledger"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_memory_write_ledger",
        rows=memory_ledger_rows,
        payload={"run_id": run_id, "rows": memory_ledger_rows, "row_count": len(memory_ledger_rows)},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["narrative_continuity_policy"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_narrative_continuity_policy",
        rows=narrative_policy_rows,
        payload={"run_id": run_id, "rows": narrative_policy_rows, "row_count": len(narrative_policy_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["narrative_continuity_ledger"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_narrative_continuity_ledger",
        rows=narrative_ledger_rows,
        payload={"run_id": run_id, "rows": narrative_ledger_rows, "row_count": len(narrative_ledger_rows)},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["generated_vs_evidenced_memory_audit"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_generated_vs_evidenced_memory_audit",
        rows=generated_vs_evidenced_rows,
        payload={"run_id": run_id, "rows": generated_vs_evidenced_rows, "row_count": len(generated_vs_evidenced_rows)},
        section="audits",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["app_runtime_handoff_packet"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_app_runtime_handoff_packet",
        rows=app_handoff_rows,
        payload={"run_id": run_id, "rows": app_handoff_rows, "row_count": len(app_handoff_rows)},
        section="packets",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )

    runtime_safety_rows = _runtime_safety_rows(status, blockers, gate_rows)
    artifact_paths["runtime_safety_readiness_report"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_runtime_safety_readiness_report",
        rows=runtime_safety_rows,
        payload=runtime_safety_rows[0],
        section="manifest",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    artifact_paths["app_runtime_handoff_readiness_report"] = _bundle_artifact(
        output_dirs=output_dirs,
        stem="v558_app_runtime_handoff_readiness_report",
        rows=app_handoff_rows,
        payload={
            "run_id": run_id,
            "status": "V558_READY_FOR_SANDBOX_RUNTIME_ONLY" if status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY" else status,
            "ready_for_app_integration_review": False,
            "ready_for_runtime_handoff": False,
            "blocker_count": len(blockers),
            "blocker_codes_json": runtime_safety_rows[0]["blocker_codes_json"],
            "created_at": utc_now(),
        },
        section="manifest",
        write_csv=write_csv,
        write_parquet=write_parquet,
    )

    build_record = build_review_gate_record(
        run_id=run_id,
        layer="V558_PLUS",
        title="V558+ runtime governance bundle",
        artifact_type="v558_plus_governance",
        status=status,
        input_inspection={
            "input_status": "blocked" if blockers else "ready",
            "missing_required_inputs": v558_bundle.get("missing_required_inputs", []),
            "stop_missing_inputs": v558_bundle.get("missing_required_inputs", []),
        },
        artifact_paths={
            "runtime_gate_path": artifact_paths["runtime_gate"]["json_path"],
            "runtime_safety_readiness_report_path": artifact_paths["runtime_safety_readiness_report"]["json_path"],
            "app_runtime_handoff_packet_path": artifact_paths["app_runtime_handoff_packet"]["json_path"],
            "evaluator_contract_path": artifact_paths["evaluator_contract"]["json_path"],
        },
        how_built=[
            "read the V558 gate and graft readiness reports",
            "normalize runtime-gate and contract-validation state into V558+ governance tables",
            "emit permission, adapter, evaluator, memory, narrative, and handoff ledgers",
            "write all outputs as parquet-first governance artifacts with JSON companions",
        ],
        continuity_notes=[
            "This bundle is a governance and readiness layer, not runtime persona generation.",
            "App integration remains blocked from raw DDM access.",
            "Generated content is not emitted here.",
        ],
        downstream_continuity_scope="not_checked_in_governance_bundle",
    )

    readiness = {
        "run_id": run_id,
        "status": status,
        "final_status": status,
        "schema_version": SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
        "created_at": utc_now(),
        "v558_run_root": repo_relative_path_text(v558_run_root),
        "governance": governance,
        "v558": {
            "readiness_path": v558_bundle["readiness_path"],
            "gate_packet_path": v558_bundle["gate_packet_path"],
            "graft_readiness_path": v558_bundle["graft_readiness_path"],
            "validation_path": v558_bundle["validation_path"],
            "status": _clean(v558_bundle["readiness"].get("status")),
            "graft_status": _clean(v558_bundle["graft_readiness"].get("status")),
        },
        "required_inputs": v558_bundle["required_inputs"],
        "missing_required_inputs": v558_bundle["missing_required_inputs"],
        "required_inputs_present": v558_bundle["required_inputs_present"],
        "blockers": blockers,
        "blocker_count": len(blockers),
        "ready_for_sandbox_runtime_only": status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
        "ready_for_limited_evaluated_runtime": False,
        "ready_for_app_integration_review": False,
        "runtime_generation_authorized": False,
        "evaluation_harness_authorized": status == "V558_READY_FOR_SANDBOX_RUNTIME_ONLY",
        "app_handoff_ready": False,
        "generated_unit_count": 0,
        "artifact_paths": artifact_paths,
        "build_ledger_path": repo_relative_path_text(output_dirs["manifest"] / "v558_plus_build_ledger.json"),
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
        "authority_documents": [
            repo_relative_path_text(DEFAULT_GOVERNANCE_ROOT),
            repo_relative_path_text(ROOT / "docs" / "architecture_control" / "RAWLSING_COMPLETION_MAP.md"),
        ],
    }

    write_json_artifact(output_dirs["manifest"] / "v558_plus_readiness_report.json", readiness)
    write_json_artifact(output_dirs["manifest"] / "v558_plus_build_ledger.json", {
        "run_id": run_id,
        "build_kind": "v558_plus_governance",
        "final_status": status,
        "created_at": utc_now(),
        "layer_records": [build_record],
        "artifact_counts": {key: value["rows"] for key, value in artifact_paths.items()},
    })

    return readiness


def validate_v558_plus_governance(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("status") not in ALLOWED_READY_STATUSES:
        errors.append("unexpected V558+ status")
    if readiness.get("generated_unit_count", 0) < 0:
        errors.append("negative generated unit count")
    if readiness.get("runtime_generation_authorized"):
        errors.append("runtime generation must not be authorized in the governance bundle")
    if readiness.get("ready_for_app_integration_review"):
        errors.append("app integration review must remain false in this governance bundle")
    required_paths = [
        "build_ledger_path",
        "artifact_paths",
    ]
    for key in required_paths:
        if not readiness.get(key):
            errors.append(f"missing {key}")
    artifact_paths = readiness.get("artifact_paths", {})
    for artifact_name in (
        "runtime_gate",
        "runtime_input_normalization_audit",
        "v557_contract_validation_report",
        "runtime_constraint_packet",
        "generation_permission_ledger",
        "surface_generation_packet",
        "generated_unit_index",
        "prompt_construction_audit",
        "v3_adapter_contract",
        "v2_surface_contract",
        "server_api_contract",
        "web_display_contract",
        "raw_ddm_access_blocklist",
        "evaluator_contract",
        "evaluator_result_index",
        "forbidden_claim_audit",
        "prompt_shape_audit",
        "runtime_safety_readiness_report",
        "memory_policy",
        "memory_write_ledger",
        "narrative_continuity_policy",
        "narrative_continuity_ledger",
        "generated_vs_evidenced_memory_audit",
        "app_runtime_handoff_packet",
        "app_runtime_handoff_readiness_report",
    ):
        if artifact_name not in artifact_paths:
            errors.append(f"missing artifact path record: {artifact_name}")
    return errors


__all__ = [
    "ALLOWED_READY_STATUSES",
    "COMPILER_VERSION",
    "DEFAULT_V558_PLUS_OUTPUT_ROOT",
    "DEFAULT_GOVERNANCE_ROOT",
    "SCHEMA_VERSION",
    "build_v558_plus_governance",
    "validate_v558_plus_governance",
]
