#!/usr/bin/env python3
"""Completion-grade V557 renderer contract builder.

This layer receives the bounded V556 pressure-flow contract and turns it into a
renderer-ready boundary packet with prompt-shape audit requirements, runtime
separation rules, and a lawful handoff index for later app wiring. It does not
emit dialogue, voice, or persona runtime content.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v5_build_standard import build_layer_build_record
from data.ddm_build_copy.ddm_v555_life_course_mediation import _bounded_score, _clean, _json_list, _load_json, _load_optional_frame
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text

V557_SCHEMA_VERSION = "v0.1"
V557_COMPILER_VERSION = "v557_renderer_contract_0.1"


def _prompt_audit_rows(packet: dict[str, Any], run_id: str) -> pd.DataFrame:
    blockers = packet.get("payload", {}).get("render_blockers", [])
    if not isinstance(blockers, list):
        blockers = []
    rows = []
    for idx, blocker in enumerate(blockers):
        rows.append(
            {
                "prompt_audit_id": f"{run_id}__prompt__{idx}",
                "run_id": run_id,
                "blocker": _clean(blocker),
                "prompt_shape_detected": True,
                "prompt_shape_violation_count": 1,
                "prompt_shape_clear": False,
                "prompt_shape_allowed": False,
                "requires_runtime_authority": True,
                "requires_generation_audit": True,
                "created_at": utc_now(),
                "schema_version": V557_SCHEMA_VERSION,
                "compiler_version": V557_COMPILER_VERSION,
            }
        )
    if not rows:
        rows.append(
            {
                "prompt_audit_id": f"{run_id}__prompt__baseline",
                "run_id": run_id,
                "blocker": "no render blockers",
                "prompt_shape_detected": False,
                "prompt_shape_violation_count": 0,
                "prompt_shape_clear": True,
                "prompt_shape_allowed": False,
                "requires_runtime_authority": True,
                "requires_generation_audit": True,
                "created_at": utc_now(),
                "schema_version": V557_SCHEMA_VERSION,
                "compiler_version": V557_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_requirements(packet: dict[str, Any], run_id: str) -> dict[str, pd.DataFrame]:
    payload = packet.get("payload", {})
    slots = payload.get("pressureflow_contract_slots", [])
    if not isinstance(slots, list):
        slots = []
    boundary_rows = []
    blocker_rows = []
    audit_rows = []
    handoff_rows = []
    for idx, slot in enumerate(slots):
        if not isinstance(slot, dict):
            continue
        slot_name = _clean(slot.get("slot_name") or slot.get("slot"))
        boundary_rows.append(
            {
                "renderer_boundary_id": f"{run_id}__boundary__{slot_name or idx}",
                "run_id": run_id,
                "slot_name": slot_name,
                "boundary_status": "renderer_contract_only",
                "may_render_dialogue": False,
                "may_render_voice": False,
                "may_render_autobiography": False,
                "created_at": utc_now(),
                "schema_version": V557_SCHEMA_VERSION,
                "compiler_version": V557_COMPILER_VERSION,
            }
        )
        blocker_rows.append(
            {
                "render_blocker_id": f"{run_id}__render_blocker__{slot_name or idx}",
                "run_id": run_id,
                "slot_name": slot_name,
                "render_blocker_status": "no_dialogue",
                "render_blocker_reason": "renderer may not convert upstream evidence into dialogue",
                "created_at": utc_now(),
                "schema_version": V557_SCHEMA_VERSION,
                "compiler_version": V557_COMPILER_VERSION,
            }
        )
        audit_rows.append(
            {
                "audit_requirement_id": f"{run_id}__audit__{slot_name or idx}",
                "run_id": run_id,
                "slot_name": slot_name,
                "requires_prompt_shape_audit": True,
                "requires_generation_audit": True,
                "requires_runtime_authority": True,
                "created_at": utc_now(),
                "schema_version": V557_SCHEMA_VERSION,
                "compiler_version": V557_COMPILER_VERSION,
            }
        )
        handoff_rows.append(
            {
                "v558_handoff_id": f"{run_id}__handoff__{slot_name or idx}",
                "run_id": run_id,
                "slot_name": slot_name,
                "handoff_lane": "renderer_contract_only",
                "allowed_v558_use": False,
                "created_at": utc_now(),
                "schema_version": V557_SCHEMA_VERSION,
                "compiler_version": V557_COMPILER_VERSION,
            }
        )
    return {
        "renderer_boundary_index": pd.DataFrame(boundary_rows),
        "render_blocker_ledger": pd.DataFrame(blocker_rows),
        "audit_requirements": pd.DataFrame(audit_rows),
        "v558_handoff_index": pd.DataFrame(handoff_rows),
    }


def build_v557_renderer_contract(
    *,
    run_id: str,
    input_root: str | Path,
    output_root: str | Path,
    input_inspection: dict[str, Any],
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    root = ensure_output_dirs(output_root, run_id)
    input_root = Path(input_root)

    v556_readiness_path = input_root / "manifest" / "v556_readiness_report.json"
    v556_packet_path = input_root / "packets" / "v556_pressureflow_attractor_packet.json"
    v553_harmonization_report_path = input_root / "manifest" / "v553_wave_harmonization_report.json"
    v553_evidence_path = input_root / "v553_wave_harmonization" / "v553_wave_harmonization_evidence.parquet"

    v556_readiness = _load_json(v556_readiness_path)
    v556_packet = _load_json(v556_packet_path)
    v553_harmonization_report = _load_json(v553_harmonization_report_path)
    harmonization_evidence_exists = v553_evidence_path.exists()
    harmonization_evidence_row_count = -1
    if harmonization_evidence_exists:
        try:
            harmonization_evidence_row_count = int(len(read_table(v553_evidence_path)))
        except Exception:
            harmonization_evidence_row_count = -1

    prompt_df = _prompt_audit_rows(v556_packet, run_id)
    registers = _build_requirements(v556_packet, run_id)
    limitations_kind = "boundary_only_not_runtime"
    limitations_reason = [
        "renderer_contract_is_a_boundary_contract_not_runtime_generation",
        "ready_for_runtime_consumption_is_false",
    ]

    packet_path = root["packets"] / "v557_renderer_contract_packet.json"
    readiness_path = root["manifest"] / "v557_readiness_report.json"
    input_manifest_path = root["manifest"] / "v557_input_manifest.json"
    handoff_manifest_path = root["manifest"] / "v557_v558_handoff_manifest.json"

    prompt_audit_path = root["audits"] / "v557_prompt_shape_audit.json"
    boundary_path = root["packets"] / "v557_renderer_boundary_conditions.parquet"
    blocker_path = root["packets"] / "v557_render_blocker_ledger.parquet"
    audit_req_path = root["packets"] / "v557_audit_requirements.parquet"
    handoff_index_path = root["packets"] / "v557_v558_handoff_index.parquet"

    boundary_info = write_frame_artifact(registers["renderer_boundary_index"], path=boundary_path, schema_path=root["schemas"] / "v557_renderer_boundary_conditions.schema.json", name="v557_renderer_boundary_conditions", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    blocker_info = write_frame_artifact(registers["render_blocker_ledger"], path=blocker_path, schema_path=root["schemas"] / "v557_render_blocker_ledger.schema.json", name="v557_render_blocker_ledger", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    audit_req_info = write_frame_artifact(registers["audit_requirements"], path=audit_req_path, schema_path=root["schemas"] / "v557_audit_requirements.schema.json", name="v557_audit_requirements", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    handoff_info = write_frame_artifact(registers["v558_handoff_index"], path=handoff_index_path, schema_path=root["schemas"] / "v557_v558_handoff_index.schema.json", name="v557_v558_handoff_index", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)

    prompt_payload = prompt_df.to_dict(orient="records")
    packet = {
        "run_id": run_id,
        "source_v556_run_id": _clean(v556_readiness.get("run_id")) or run_id,
        "layer": "v557",
        "title": "Renderer contract boundary packet",
        "artifact_type": "v557_renderer_contract_packet",
        "schema_version": V557_SCHEMA_VERSION,
        "compiler_version": V557_COMPILER_VERSION,
        "layer_status": "READY_V557_RENDERER_WITH_LIMITATIONS",
        "status": "READY_V557_RENDERER_WITH_LIMITATIONS",
        "ready_for_v558": True,
        "ready_for_runtime_consumption": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "forbidden_outputs_written": False,
        "persona_fields_written": False,
        "voice_fields_written": False,
        "dialogue_generated": False,
        "created_at": utc_now(),
        "input_root": repo_relative_path_text(input_root),
        "input_inspection": input_inspection,
        "runtime_use_class": "renderer_contract_only_no_dialogue",
        "payload": {
            "upstream_authority_context": {
                "consumes_layer": "v556",
                "consumes_artifact": "v556_pressureflow_attractor_packet",
                "input_status": _clean(input_inspection.get("input_status")),
            },
            "readiness_report_statuses": input_inspection.get("readiness_report_statuses", {}),
            "v556_authority_context": {
                "readiness_report": v556_readiness,
                "pressureflow_ready": bool(v556_readiness.get("ready_for_v557", False)),
                "pressureflow_status": _clean(v556_readiness.get("status")),
            },
            "v553_authority_context": {
                "wave_harmonization_report": v553_harmonization_report,
                "wave_harmonization_evidence": {
                    "path": repo_relative_path_text(v553_evidence_path),
                    "exists": harmonization_evidence_exists,
                    "row_count": harmonization_evidence_row_count,
                },
                "authority_requires_harmonization_evidence_parquet": True,
                "authority_requires_cross_wave_preservation": True,
            },
            "renderer_input_contract": {
                "limitations_kind": limitations_kind,
                "limitations_reason": limitations_reason,
                "may_render_only_after_generation_audit": True,
                "may_not_quote_or_paraphrase_upstream_evidence_as_autobiography": True,
                "may_not_speak_raw_structure_as_dialogue": True,
            },
            "runtime_wiring_contract": [
                "consume pressure-flow contract only",
                "respect upstream evidence/routing boundaries",
                "do not invent dialogue or voice from structural packets",
                "defer persona synthesis to later runtime stages",
            ],
            "source_to_generation_separation_ledger": [
                "structure is not dialogue",
                "evidence is not autobiography",
                "rendering is not origin",
                "audited packets only",
                "cross-wave harmonization evidence preserved",
            ],
            "render_blockers": [
                "missing audited V556 psyche dynamics",
                "missing source-to-generation separation ledger",
                "missing app/runtime consumption contract",
            ],
            "prompt_shape_audit": {
                "status": "required",
                "prompt_shape_detected": bool(prompt_payload),
                "prompt_shape_violation_count": len(prompt_payload),
                "prompt_shape_clear": False,
                "prompt_shape_allowed": False,
                "violation_count": 0,
                "notes": [
                    "no dialogue",
                    "no voice",
                    "no autobiography",
                    "no unaudited persona",
                ],
                "rows": prompt_payload,
            },
            "audit_requirements": registers["audit_requirements"].to_dict(orient="records"),
            "renderer_boundary_conditions": registers["renderer_boundary_index"].to_dict(orient="records"),
            "render_blocker_ledger": registers["render_blocker_ledger"].to_dict(orient="records"),
            "v558_handoff_index": registers["v558_handoff_index"].to_dict(orient="records"),
            "renderer_contract_status": "renderer_contract_only",
            "blocked_shortcuts": [
                "no dialogue",
                "no voice",
                "no autobiography",
                "no unaudited persona",
            ],
            "renderer_readiness_score": _bounded_score(0.35 + 0.25 * bool(v556_readiness.get("ready_for_v557", False)) + 0.10 * bool(harmonization_evidence_exists)),
            "v556_readiness_score": _bounded_score(float(v556_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        },
        "renderer_contract_summary": {
            "boundary_rows": int(len(registers["renderer_boundary_index"])),
            "render_blocker_rows": int(len(registers["render_blocker_ledger"])),
            "audit_requirement_rows": int(len(registers["audit_requirements"])),
        },
    }

    write_json_artifact(packet_path, packet)
    write_json_artifact(input_manifest_path, input_inspection)
    write_json_artifact(
        prompt_audit_path,
        {
            "run_id": run_id,
            "layer": "v557",
            "created_at": utc_now(),
            "prompt_shape_detected": bool(prompt_payload),
            "prompt_shape_violation_count": len(prompt_payload),
            "prompt_shape_clear": False,
            "prompt_shape_allowed": False,
            "violation_count": 0,
            "rows": prompt_payload,
        },
    )
    write_json_artifact(
        handoff_manifest_path,
        {
            "run_id": run_id,
            "layer": "v557",
            "created_at": utc_now(),
            "v558_handoff_rows": int(len(registers["v558_handoff_index"])),
            "ready_for_v558": True,
        },
    )

    build_record = build_layer_build_record(
        spec=type("Spec", (), {"layer": "v557", "title": "Phenomenological renderer packet adapter", "artifact_slug": "v557_renderer_contract_packet"})(),
        input_inspection=input_inspection,
        status="THIN_READY" if input_inspection.get("input_status") == "ready" else "THIN_READY_WITH_INPUT_GAPS",
        packet_path=repo_relative_path_text(packet_path),
        schema_path=repo_relative_path_text(root["schemas"] / "v557_renderer_contract_packet.schema.json"),
        audit_path=repo_relative_path_text(root["audits"] / "v557_forbidden_inference_audit.parquet"),
        readiness_path=repo_relative_path_text(readiness_path),
        input_manifest_path=repo_relative_path_text(input_manifest_path),
        run_id=run_id,
    )

    readiness = {
        "run_id": run_id,
        "layer": "v557",
        "status": packet["status"],
        "ready_for_v558": True,
        "ready_for_semantic_deepening": True,
        "ready_for_runtime_consumption": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "packet_path": repo_relative_path_text(packet_path),
        "schema_path": repo_relative_path_text(root["schemas"] / "v557_renderer_contract_packet.schema.json"),
        "audit_path": repo_relative_path_text(root["audits"] / "v557_forbidden_inference_audit.parquet"),
        "input_manifest_path": repo_relative_path_text(input_manifest_path),
        "input_status": input_inspection["input_status"],
        "missing_required_inputs": input_inspection["missing_required_inputs"],
        "upstream_readiness_score": _bounded_score(float(v556_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "boundary_readiness_score": _bounded_score(float(v556_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "created_at": utc_now(),
        "schema_version": V557_SCHEMA_VERSION,
        "compiler_version": V557_COMPILER_VERSION,
        "renderer_contract_summary": packet["renderer_contract_summary"],
        "v558_handoff_index_path": repo_relative_path_text(handoff_index_path),
        "artifact_paths": {
            "renderer_boundary_conditions": repo_relative_path_text(boundary_path),
            "render_blocker_ledger": repo_relative_path_text(blocker_path),
            "audit_requirements": repo_relative_path_text(audit_req_path),
            "v558_handoff_index": repo_relative_path_text(handoff_index_path),
        },
        "artifact_infos": {
            "renderer_boundary_conditions": boundary_info,
            "render_blocker_ledger": blocker_info,
            "audit_requirements": audit_req_info,
            "v558_handoff_index": handoff_info,
        },
        "readiness": {
            "status": "READY_V557_RENDERER_WITH_LIMITATIONS",
            "limitations_kind": limitations_kind,
            "limitations_reason": limitations_reason,
            "ready_for_v558": True,
            "ready_for_semantic_deepening": True,
            "renderer_boundary_rows": int(len(registers["renderer_boundary_index"])),
            "v556_readiness_status": _clean(v556_readiness.get("status")),
        },
    }
    write_json_artifact(readiness_path, readiness)
    write_json_artifact(root["manifest"] / "v557_build_record.json", build_record)
    return {
        "readiness": readiness,
        "artifact_paths": readiness["artifact_paths"],
        "artifact_infos": readiness["artifact_infos"],
        "build_record": build_record,
    }


__all__ = ["build_v557_renderer_contract", "V557_SCHEMA_VERSION", "V557_COMPILER_VERSION"]
