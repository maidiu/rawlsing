#!/usr/bin/env python3
"""Completion-grade V556 pressure-flow / attractor contract builder.

This layer receives the bounded V555 mediation contract and turns it into
pressure-flow registers, attractor requirements, blocker ledgers, and a lawful
V557 renderer handoff index. It does not generate psyche, enneagram labels,
voice, or dialogue.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v5_build_standard import build_layer_build_record
from data.ddm_build_copy.ddm_v555_life_course_mediation import _bounded_score, _clean, _json_list, _load_json, _load_optional_frame, _summarize_list

V556_SCHEMA_VERSION = "v0.1"
V556_COMPILER_VERSION = "v556_pressureflow_0.1"


def _pressureflow_rows(v555_packet: dict[str, Any], run_id: str) -> pd.DataFrame:
    payload = v555_packet.get("payload", {})
    mediation_contract = payload.get("mediation_contract", {})
    slots = mediation_contract.get("mediation_slots", []) if isinstance(mediation_contract, dict) else []
    if not slots:
        slots = payload.get("mediation_slot_contracts", [])
    rows = []
    if not isinstance(slots, list):
        slots = []
    for idx, slot in enumerate(slots):
        if not isinstance(slot, dict):
            continue
        slot_name = _clean(slot.get("slot_name") or slot.get("slot"))
        rows.append(
            {
                "pressureflow_slot_id": f"{run_id}__slot__{slot_name or idx}",
                "run_id": run_id,
                "slot_name": slot_name,
                "slot_channel": _clean(slot.get("slot_channel") or slot.get("channel")),
                "pressure_status": "candidate_dynamics_only",
                "pressure_family": "pressureflow",
                "blocked_from_runtime_psyche": True,
                "blocked_from_enneagram_assignment": True,
                "source_v555_mediation_slot_status": _clean(slot.get("slot_status") or slot.get("status")),
                "created_at": utc_now(),
                "schema_version": V556_SCHEMA_VERSION,
                "compiler_version": V556_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_registers(v555_packet: dict[str, Any], slot_df: pd.DataFrame, run_id: str) -> dict[str, pd.DataFrame]:
    rows = slot_df.to_dict(orient="records")
    attractor_rows = []
    blocker_rows = []
    stop_rows = []
    handoff_rows = []
    for row in rows:
        slot_name = _clean(row.get("slot_name"))
        attractor_rows.append(
            {
                "attractor_requirement_id": f"{run_id}__attractor__{slot_name}",
                "run_id": run_id,
                "slot_name": slot_name,
                "requirement_status": "requires_v555_mediated_history",
                "candidate_dynamics": _json_list(["route_axis_1", "route_axis_2", "route_axis_3", "route_axis_4", "route_axis_5", "route_axis_6"]),
                "created_at": utc_now(),
                "schema_version": V556_SCHEMA_VERSION,
                "compiler_version": V556_COMPILER_VERSION,
            }
        )
        blocker_rows.append(
            {
                "blocker_id": f"{run_id}__blocker__{slot_name}",
                "run_id": run_id,
                "slot_name": slot_name,
                "blocker_type": "candidate_dynamics_only",
                "blocker_reason": "no finished psyche profile",
                "blocked_from_v557": True,
                "created_at": utc_now(),
                "schema_version": V556_SCHEMA_VERSION,
                "compiler_version": V556_COMPILER_VERSION,
            }
        )
        stop_rows.append(
            {
                "stop_reason_id": f"{run_id}__stop__{slot_name}",
                "run_id": run_id,
                "slot_name": slot_name,
                "stop_reason": "no finished psyche profile",
                "blocked_downstream_layers": _json_list(["v557"]),
                "created_at": utc_now(),
                "schema_version": V556_SCHEMA_VERSION,
                "compiler_version": V556_COMPILER_VERSION,
            }
        )
        handoff_rows.append(
            {
                "v557_handoff_id": f"{run_id}__handoff__{slot_name}",
                "run_id": run_id,
                "slot_name": slot_name,
                "handoff_lane": "pressureflow_contract_only",
                "allowed_v557_use": False,
                "created_at": utc_now(),
                "schema_version": V556_SCHEMA_VERSION,
                "compiler_version": V556_COMPILER_VERSION,
            }
        )
    return {
        "attractor_requirement_index": pd.DataFrame(attractor_rows),
        "psyche_generation_absence_register": pd.DataFrame(blocker_rows),
        "pressureflow_stop_reason_ledger": pd.DataFrame(stop_rows),
        "v557_handoff_index": pd.DataFrame(handoff_rows),
    }


def build_v556_pressureflow_attractor(
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

    v555_readiness_path = input_root / "manifest" / "v555_readiness_report.json"
    v555_packet_path = input_root / "packets" / "v555_life_course_mediation_packet.json"
    v553_harmonization_report_path = input_root / "manifest" / "v553_wave_harmonization_report.json"
    v553_evidence_path = input_root / "v553_wave_harmonization" / "v553_wave_harmonization_evidence.parquet"
    v553_year_indexed_path = input_root / "packets" / "v553_year_indexed_pressure_over_time.parquet"
    v553_interpolated_path = input_root / "packets" / "v553_interpolated_pressure_over_time.parquet"

    v555_readiness = _load_json(v555_readiness_path)
    v555_packet = _load_json(v555_packet_path)
    v553_harmonization_report = _load_json(v553_harmonization_report_path)
    v553_year_indexed = _load_optional_frame(v553_year_indexed_path)
    v553_interpolated = _load_optional_frame(v553_interpolated_path)
    harmonization_evidence_exists = v553_evidence_path.exists()
    harmonization_evidence_row_count = -1
    if harmonization_evidence_exists:
        try:
            harmonization_evidence_row_count = int(len(read_table(v553_evidence_path)))
        except Exception:
            harmonization_evidence_row_count = -1

    slot_df = _pressureflow_rows(v555_packet, run_id)
    registers = _build_registers(v555_packet, slot_df, run_id)
    limitations_kind = "boundary_only_not_runtime"
    limitations_reason = [
        "pressureflow_is_a_boundary_contract_not_runtime_generation",
        "ready_for_runtime_consumption_is_false",
    ]

    packet_path = root["packets"] / "v556_pressureflow_attractor_packet.json"
    readiness_path = root["manifest"] / "v556_readiness_report.json"
    input_manifest_path = root["manifest"] / "v556_input_manifest.json"
    handoff_manifest_path = root["manifest"] / "v556_v557_handoff_manifest.json"

    slot_path = root["packets"] / "v556_pressureflow_contract_slots.parquet"
    attractor_path = root["packets"] / "v556_attractor_generation_requirements.parquet"
    absence_path = root["packets"] / "v556_psyche_generation_absence_register.parquet"
    stop_path = root["packets"] / "v556_pressureflow_stop_reason_ledger.parquet"
    handoff_index_path = root["packets"] / "v556_v557_handoff_index.parquet"

    slot_info = write_frame_artifact(slot_df, path=slot_path, schema_path=root["schemas"] / "v556_pressureflow_contract_slots.schema.json", name="v556_pressureflow_contract_slots", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    attractor_info = write_frame_artifact(registers["attractor_requirement_index"], path=attractor_path, schema_path=root["schemas"] / "v556_attractor_generation_requirements.schema.json", name="v556_attractor_generation_requirements", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    absence_info = write_frame_artifact(registers["psyche_generation_absence_register"], path=absence_path, schema_path=root["schemas"] / "v556_psyche_generation_absence_register.schema.json", name="v556_psyche_generation_absence_register", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    stop_info = write_frame_artifact(registers["pressureflow_stop_reason_ledger"], path=stop_path, schema_path=root["schemas"] / "v556_pressureflow_stop_reason_ledger.schema.json", name="v556_pressureflow_stop_reason_ledger", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    handoff_info = write_frame_artifact(registers["v557_handoff_index"], path=handoff_index_path, schema_path=root["schemas"] / "v556_v557_handoff_index.schema.json", name="v556_v557_handoff_index", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)

    packet = {
        "run_id": run_id,
        "source_v555_run_id": _clean(v555_readiness.get("run_id")) or run_id,
        "layer": "v556",
        "title": "Pressure-flow / attractor contract",
        "artifact_type": "v556_pressureflow_attractor_packet",
        "schema_version": V556_SCHEMA_VERSION,
        "compiler_version": V556_COMPILER_VERSION,
        "layer_status": "READY_V556_PRESSUREFLOW_WITH_LIMITATIONS",
        "status": "READY_V556_PRESSUREFLOW_WITH_LIMITATIONS",
        "ready_for_v557": True,
        "ready_for_runtime_consumption": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "forbidden_outputs_written": False,
        "persona_fields_written": False,
        "biography_fields_written": False,
        "voice_fields_written": False,
        "created_at": utc_now(),
        "input_root": str(input_root),
        "input_inspection": input_inspection,
        "runtime_use_class": "generated_psyche_dynamics_contract_only",
        "payload": {
            "upstream_authority_context": {
                "consumes_layer": "v555",
                "consumes_artifact": "v555_life_course_mediation_packet",
                "input_status": _clean(input_inspection.get("input_status")),
            },
            "readiness_report_statuses": input_inspection.get("readiness_report_statuses", {}),
            "v555_authority_context": {
                "readiness_report": v555_readiness,
                "mediation_contract_ready": bool(v555_readiness.get("ready_for_v556", False)),
                "mediation_contract_status": _clean(v555_readiness.get("status")),
            },
            "v553_authority_context": {
                "wave_harmonization_report": v553_harmonization_report,
                "wave_harmonization_evidence": {
                    "path": str(v553_evidence_path),
                    "exists": harmonization_evidence_exists,
                    "row_count": harmonization_evidence_row_count,
                },
                "authority_requires_harmonization_evidence_parquet": True,
                "authority_requires_cross_wave_preservation": True,
            },
            "pressureflow_contract": {
                "status": "candidate_dynamics_only",
                "limitations_kind": limitations_kind,
                "limitations_reason": limitations_reason,
                "preconditions": [
                    "v555 mediated history present",
                    "v553 temporal pressure present",
                    "no finished psyche profile",
                ],
                "candidate_dynamics": ["route_axis_1", "route_axis_2", "route_axis_3", "route_axis_4", "route_axis_5", "route_axis_6"],
            },
            "pressureflow_contract_slots": slot_df.to_dict(orient="records"),
            "attractor_generation_requirements": registers["attractor_requirement_index"].to_dict(orient="records"),
            "psyche_generation_absence_register": registers["psyche_generation_absence_register"].to_dict(orient="records"),
            "pressureflow_stop_reason_ledger": registers["pressureflow_stop_reason_ledger"].to_dict(orient="records"),
            "v557_handoff_index": registers["v557_handoff_index"].to_dict(orient="records"),
            "pressureflow_contract_status": "generated_pressureflow_only",
            "blocked_shortcuts": [
                "direct survey-to-Enneagram assignment",
                "static trait inference",
                "render attractor as final identity",
            ],
            "pressureflow_readiness_score": _bounded_score(0.30 + 0.25 * bool(v555_readiness.get("ready_for_v556", False)) + 0.15 * bool(harmonization_evidence_exists)),
            "v555_readiness_score": _bounded_score(float(v555_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        },
        "pressureflow_contract_summary": {
            "slot_count": int(len(slot_df)),
            "attractor_requirement_rows": int(len(registers["attractor_requirement_index"])),
            "psyche_absence_rows": int(len(registers["psyche_generation_absence_register"])),
        },
    }

    write_json_artifact(packet_path, packet)
    write_json_artifact(input_manifest_path, input_inspection)
    write_json_artifact(
        handoff_manifest_path,
        {
            "run_id": run_id,
            "layer": "v556",
            "created_at": utc_now(),
            "v557_handoff_rows": int(len(registers["v557_handoff_index"])),
            "ready_for_v557": True,
        },
    )

    build_record = build_layer_build_record(
        spec=type("Spec", (), {"layer": "v556", "title": "Pressure-flow / attractor formation adapter", "artifact_slug": "v556_pressureflow_attractor_packet"})(),
        input_inspection=input_inspection,
        status="THIN_READY" if input_inspection.get("input_status") == "ready" else "THIN_READY_WITH_INPUT_GAPS",
        packet_path=str(packet_path),
        schema_path=str(root["schemas"] / "v556_pressureflow_attractor_packet.schema.json"),
        audit_path=str(root["audits"] / "v556_forbidden_inference_audit.parquet"),
        readiness_path=str(readiness_path),
        input_manifest_path=str(input_manifest_path),
        run_id=run_id,
    )

    readiness = {
        "run_id": run_id,
        "layer": "v556",
        "status": packet["status"],
        "ready_for_v557": True,
        "ready_for_runtime_consumption": False,
        "packet_path": str(packet_path),
        "schema_path": str(root["schemas"] / "v556_pressureflow_attractor_packet.schema.json"),
        "audit_path": str(root["audits"] / "v556_forbidden_inference_audit.parquet"),
        "input_manifest_path": str(input_manifest_path),
        "input_status": input_inspection["input_status"],
        "missing_required_inputs": input_inspection["missing_required_inputs"],
        "upstream_readiness_score": _bounded_score(float(v555_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "boundary_readiness_score": _bounded_score(float(v555_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "created_at": utc_now(),
        "schema_version": V556_SCHEMA_VERSION,
        "compiler_version": V556_COMPILER_VERSION,
        "pressureflow_contract_summary": packet["pressureflow_contract_summary"],
        "v557_handoff_index_path": str(handoff_index_path),
        "artifact_paths": {
            "pressureflow_contract_slots": str(slot_path),
            "attractor_generation_requirements": str(attractor_path),
            "psyche_generation_absence_register": str(absence_path),
            "pressureflow_stop_reason_ledger": str(stop_path),
            "v557_handoff_index": str(handoff_index_path),
        },
        "artifact_infos": {
            "pressureflow_contract_slots": slot_info,
            "attractor_generation_requirements": attractor_info,
            "psyche_generation_absence_register": absence_info,
            "pressureflow_stop_reason_ledger": stop_info,
            "v557_handoff_index": handoff_info,
        },
        "readiness": {
            "status": "READY_V556_PRESSUREFLOW_WITH_LIMITATIONS",
            "limitations_kind": limitations_kind,
            "limitations_reason": limitations_reason,
            "ready_for_v557": True,
            "pressureflow_slot_rows": int(len(slot_df)),
            "v555_readiness_status": _clean(v555_readiness.get("status")),
        },
    }
    write_json_artifact(readiness_path, readiness)
    write_json_artifact(root["manifest"] / "v556_build_record.json", build_record)
    return {
        "readiness": readiness,
        "artifact_paths": readiness["artifact_paths"],
        "artifact_infos": readiness["artifact_infos"],
        "build_record": build_record,
    }


__all__ = ["build_v556_pressureflow_attractor", "V556_SCHEMA_VERSION", "V556_COMPILER_VERSION"]
