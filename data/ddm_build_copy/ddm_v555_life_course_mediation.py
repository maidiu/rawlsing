#!/usr/bin/env python3
"""Completion-grade V555 life-course mediation contract builder.

This layer receives the bounded V554 seed contract and turns it into explicit
mediation-slot registers, household/parent/co-parent/channel boundary ledgers,
and a lawful V556 handoff index. It does not generate biography, psyche, or
runtime persona content.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v5_build_standard import build_layer_build_record
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text

V555_SCHEMA_VERSION = "v0.1"
V555_COMPILER_VERSION = "v555_life_course_mediation_0.1"


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _bounded_score(value: float, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        score = default
    if pd.isna(score):
        score = default
    return max(0.0, min(1.0, score))


def _json_list(values: list[Any]) -> str:
    cleaned = []
    for value in values:
        text = _clean(value)
        if text:
            cleaned.append(text)
    return json.dumps(cleaned, sort_keys=True)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_optional_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return read_table(path)
    except Exception:
        return pd.DataFrame()


def _summarize_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def _frame_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    if frame.empty:
        return []
    return frame.to_dict(orient="records")


def _seed_affordance_rows(v554_packet: dict[str, Any], seed_df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = _frame_records(seed_df)
    if rows:
        return rows
    preview = v554_packet.get("payload", {}).get("seed_affordance_index_preview", [])
    return [row for row in _summarize_list(preview) if isinstance(row, dict)]


def _slot_rows(seed_rows: list[dict[str, Any]], run_id: str) -> pd.DataFrame:
    slots = [
        ("household_mediation", "household", "shared domestic route", False),
        ("family_mediation", "family", "intergenerational route", False),
        ("parent_transmission", "parent", "parent channel", True),
        ("co_parent_transmission", "co_parent", "co-parent channel", True),
        ("child_absorption_resistance", "child", "child developmental route", True),
        ("carrier_institutional_mediation", "carrier", "institutional route", True),
        ("regional_locality_mediation", "regional", "regional route", True),
    ]
    rows = []
    for slot, channel, label, may_generate_later in slots:
        rows.append(
            {
                "mediation_slot_id": f"{run_id}__slot__{slot}",
                "run_id": run_id,
                "slot_name": slot,
                "slot_channel": channel,
                "slot_label": label,
                "slot_status": "unresolved",
                "may_generate_later": may_generate_later,
                "requires_family_mediation": slot in {"household_mediation", "family_mediation", "parent_transmission", "co_parent_transmission", "child_absorption_resistance"},
                "requires_carrier_mediation": slot == "carrier_institutional_mediation",
                "requires_regional_mediation": slot == "regional_locality_mediation",
                "source_v554_seed_affordance_ids_json": _json_list(
                    [row.get("seed_affordance_id") for row in seed_rows]
                ),
                "created_at": utc_now(),
                "schema_version": V555_SCHEMA_VERSION,
                "compiler_version": V555_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_registers(seed_rows: list[dict[str, Any]], slot_df: pd.DataFrame, run_id: str) -> dict[str, pd.DataFrame]:
    household_rows = [
        {
            "household_register_id": f"{run_id}__household__{idx}",
            "run_id": run_id,
            "household_scope": "unresolved",
            "household_boundary_status": "not_story",
            "source_seed_affordance_id": _clean(seed.get("seed_affordance_id")),
            "requires_family_mediation": True,
            "requires_parent_transmission": True,
            "requires_co_parent_transmission": True,
            "created_at": utc_now(),
            "schema_version": V555_SCHEMA_VERSION,
            "compiler_version": V555_COMPILER_VERSION,
        }
        for idx, seed in enumerate(seed_rows[:5])
    ]

    parent_rows = [
        {
            "parent_transmission_id": f"{run_id}__parent__{idx}",
            "run_id": run_id,
            "parent_channel": "parent",
            "transmission_status": "unresolved_not_parent_psychology",
            "source_seed_affordance_id": _clean(seed.get("seed_affordance_id")),
            "blocked_from_biography": True,
            "created_at": utc_now(),
            "schema_version": V555_SCHEMA_VERSION,
            "compiler_version": V555_COMPILER_VERSION,
        }
        for idx, seed in enumerate(seed_rows[:5])
    ]

    co_parent_rows = [
        {
            "co_parent_transmission_id": f"{run_id}__coparent__{idx}",
            "run_id": run_id,
            "co_parent_channel": "co_parent",
            "transmission_status": "unresolved_not_co_parent_psychology",
            "source_seed_affordance_id": _clean(seed.get("seed_affordance_id")),
            "blocked_from_biography": True,
            "created_at": utc_now(),
            "schema_version": V555_SCHEMA_VERSION,
            "compiler_version": V555_COMPILER_VERSION,
        }
        for idx, seed in enumerate(seed_rows[:5])
    ]

    child_rows = [
        {
            "child_absorption_id": f"{run_id}__child__{idx}",
            "run_id": run_id,
            "child_channel": "child",
            "absorption_status": "unresolved_not_psyche",
            "source_seed_affordance_id": _clean(seed.get("seed_affordance_id")),
            "blocked_from_psyche": True,
            "created_at": utc_now(),
            "schema_version": V555_SCHEMA_VERSION,
            "compiler_version": V555_COMPILER_VERSION,
        }
        for idx, seed in enumerate(seed_rows[:5])
    ]

    carrier_rows = [
        {
            "carrier_mediation_id": f"{run_id}__carrier__{idx}",
            "run_id": run_id,
            "carrier_channel": "carrier",
            "carrier_status": "unresolved_not_membership_fact",
            "source_seed_affordance_id": _clean(seed.get("seed_affordance_id")),
            "blocked_from_fact_claim": True,
            "created_at": utc_now(),
            "schema_version": V555_SCHEMA_VERSION,
            "compiler_version": V555_COMPILER_VERSION,
        }
        for idx, seed in enumerate(seed_rows[:5])
    ]

    stop_rows = []
    for row in slot_df.to_dict(orient="records"):
        stop_rows.append(
            {
                "stop_reason_id": f"{run_id}__stop__{row['slot_name']}",
                "run_id": run_id,
                "slot_name": row["slot_name"],
                "stop_reason": "generated_mediation_only",
                "blocked_downstream_layers": _json_list(["v556", "v557"]),
                "created_at": utc_now(),
                "schema_version": V555_SCHEMA_VERSION,
                "compiler_version": V555_COMPILER_VERSION,
            }
        )

    handoff_rows = []
    for row in slot_df.to_dict(orient="records"):
        handoff_rows.append(
            {
                "v556_handoff_id": f"{run_id}__handoff__{row['slot_name']}",
                "run_id": run_id,
                "slot_name": row["slot_name"],
                "handoff_lane": "bounded_mediation_only" if not row["may_generate_later"] else "reviewable_mediation_context",
                "allowed_v556_use": False,
                "created_at": utc_now(),
                "schema_version": V555_SCHEMA_VERSION,
                "compiler_version": V555_COMPILER_VERSION,
            }
        )

    return {
        "household_register": pd.DataFrame(household_rows),
        "parent_transmission_register": pd.DataFrame(parent_rows),
        "co_parent_transmission_register": pd.DataFrame(co_parent_rows),
        "child_absorption_register": pd.DataFrame(child_rows),
        "carrier_mediation_register": pd.DataFrame(carrier_rows),
        "life_course_stop_reason_ledger": pd.DataFrame(stop_rows),
        "v556_handoff_index": pd.DataFrame(handoff_rows),
    }


def build_v555_life_course_mediation(
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

    v554_readiness_path = input_root / "manifest" / "v554_readiness_report.json"
    v554_packet_path = input_root / "packets" / "v554_bounded_seed_affordance_contract_packet.json"
    v554_seed_affordance_path = input_root / "packets" / "v554_seed_affordance_index.parquet"
    v553_harmonization_report_path = input_root / "manifest" / "v553_wave_harmonization_report.json"
    v553_evidence_path = input_root / "v553_wave_harmonization" / "v553_wave_harmonization_evidence.parquet"
    v553_year_indexed_path = input_root / "packets" / "v553_year_indexed_pressure_over_time.parquet"
    v553_interpolated_path = input_root / "packets" / "v553_interpolated_pressure_over_time.parquet"

    v554_readiness = _load_json(v554_readiness_path)
    v554_packet = _load_json(v554_packet_path)
    v554_seed_affordance_df = _load_optional_frame(v554_seed_affordance_path)
    seed_rows = _seed_affordance_rows(v554_packet, v554_seed_affordance_df)
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

    slot_df = _slot_rows(seed_rows, run_id)
    registers = _build_registers(seed_rows, slot_df, run_id)
    limitations_kind = "boundary_only_not_runtime"
    limitations_reason = [
        "life_course_mediation_is_a_boundary_contract_not_runtime_generation",
        "ready_for_runtime_consumption_is_false",
    ]

    packet_path = root["packets"] / "v555_life_course_mediation_packet.json"
    readiness_path = root["manifest"] / "v555_readiness_report.json"
    input_manifest_path = root["manifest"] / "v555_input_manifest.json"
    handoff_manifest_path = root["manifest"] / "v555_v556_handoff_manifest.json"

    slot_path = root["packets"] / "v555_mediation_slot_contracts.parquet"
    household_path = root["packets"] / "v555_household_mediation_register.parquet"
    parent_path = root["packets"] / "v555_parent_transmission_register.parquet"
    coparent_path = root["packets"] / "v555_co_parent_transmission_register.parquet"
    child_path = root["packets"] / "v555_child_absorption_register.parquet"
    carrier_path = root["packets"] / "v555_carrier_mediation_register.parquet"
    stop_path = root["packets"] / "v555_life_course_stop_reason_ledger.parquet"
    handoff_index_path = root["packets"] / "v555_v556_handoff_index.parquet"

    slot_info = write_frame_artifact(slot_df, path=slot_path, schema_path=root["schemas"] / "v555_mediation_slot_contracts.schema.json", name="v555_mediation_slot_contracts", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    household_info = write_frame_artifact(registers["household_register"], path=household_path, schema_path=root["schemas"] / "v555_household_mediation_register.schema.json", name="v555_household_mediation_register", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    parent_info = write_frame_artifact(registers["parent_transmission_register"], path=parent_path, schema_path=root["schemas"] / "v555_parent_transmission_register.schema.json", name="v555_parent_transmission_register", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    coparent_info = write_frame_artifact(registers["co_parent_transmission_register"], path=coparent_path, schema_path=root["schemas"] / "v555_co_parent_transmission_register.schema.json", name="v555_co_parent_transmission_register", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    child_info = write_frame_artifact(registers["child_absorption_register"], path=child_path, schema_path=root["schemas"] / "v555_child_absorption_register.schema.json", name="v555_child_absorption_register", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    carrier_info = write_frame_artifact(registers["carrier_mediation_register"], path=carrier_path, schema_path=root["schemas"] / "v555_carrier_mediation_register.schema.json", name="v555_carrier_mediation_register", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    stop_info = write_frame_artifact(registers["life_course_stop_reason_ledger"], path=stop_path, schema_path=root["schemas"] / "v555_life_course_stop_reason_ledger.schema.json", name="v555_life_course_stop_reason_ledger", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)
    handoff_info = write_frame_artifact(registers["v556_handoff_index"], path=handoff_index_path, schema_path=root["schemas"] / "v555_v556_handoff_index.schema.json", name="v555_v556_handoff_index", run_id=run_id, write_csv=write_csv, write_parquet=write_parquet)

    packet = {
        "run_id": run_id,
        "source_v554_run_id": _clean(v554_readiness.get("run_id")) or run_id,
        "layer": "v555",
        "title": "Life-course mediation bridge contract",
        "artifact_type": "v555_life_course_mediation_packet",
        "schema_version": V555_SCHEMA_VERSION,
        "compiler_version": V555_COMPILER_VERSION,
        "layer_status": "READY_V555_MEDIATION_WITH_LIMITATIONS",
        "status": "READY_V555_MEDIATION_WITH_LIMITATIONS",
        "ready_for_v556": True,
        "ready_for_runtime_consumption": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "forbidden_outputs_written": False,
        "persona_fields_written": False,
        "biography_fields_written": False,
        "voice_fields_written": False,
        "created_at": utc_now(),
        "input_root": repo_relative_path_text(input_root),
        "input_inspection": input_inspection,
        "runtime_use_class": "generated_mediation_slots_only_not_biography",
        "payload": {
            "upstream_authority_context": {
                "consumes_layer": "v554",
                "consumes_artifact": "v554_bounded_seed_affordance_contract_packet",
                "input_status": _clean(input_inspection.get("input_status")),
            },
            "readiness_report_statuses": input_inspection.get("readiness_report_statuses", {}),
            "v554_authority_context": {
                "readiness_report": v554_readiness,
                "seed_contract_status": _clean(v554_readiness.get("seed_contract_status")),
                "seed_contract_ready": bool(v554_readiness.get("ready_for_v555", False)),
                "seed_contract_blockers": _summarize_list(v554_readiness.get("stop_reasons", [])),
                "seed_affordance_index_path": repo_relative_path_text(v554_seed_affordance_path),
                "seed_affordance_index_exists": v554_seed_affordance_path.exists(),
                "seed_affordance_index_rows": int(len(v554_seed_affordance_df)),
                "seed_affordance_rows_consumed": int(len(seed_rows)),
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
            "mediation_contract": {
                "status": "channelized_and_generated_not_factual",
                "limitations_kind": limitations_kind,
                "limitations_reason": limitations_reason,
                "mediation_slots": slot_df.to_dict(orient="records"),
                "slot_count": int(len(slot_df)),
                "source_seed_affordance_count": int(len(seed_rows)),
            },
            "household_register": registers["household_register"].to_dict(orient="records"),
            "parent_transmission_register": registers["parent_transmission_register"].to_dict(orient="records"),
            "co_parent_transmission_register": registers["co_parent_transmission_register"].to_dict(orient="records"),
            "child_absorption_register": registers["child_absorption_register"].to_dict(orient="records"),
            "carrier_mediation_register": registers["carrier_mediation_register"].to_dict(orient="records"),
            "life_course_stop_reason_ledger": registers["life_course_stop_reason_ledger"].to_dict(orient="records"),
            "v556_handoff_index": registers["v556_handoff_index"].to_dict(orient="records"),
            "mediation_contract_status": "generated_mediation_only",
            "blocked_shortcuts": [
                "skip family mediation and jump to psyche",
                "convert generated mediation into survey fact",
                "collapse co_parent and parent into one slot",
            ],
            "mediation_readiness_score": _bounded_score(0.35 + 0.25 * bool(v554_readiness.get("ready_for_v555", False)) + 0.15 * bool(harmonization_evidence_exists)),
            "v554_readiness_score": _bounded_score(float(v554_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        },
        "mediation_contract_summary": {
            "slot_count": int(len(slot_df)),
            "household_register_rows": int(len(registers["household_register"])),
            "parent_transmission_rows": int(len(registers["parent_transmission_register"])),
            "co_parent_transmission_rows": int(len(registers["co_parent_transmission_register"])),
            "child_absorption_rows": int(len(registers["child_absorption_register"])),
            "carrier_mediation_rows": int(len(registers["carrier_mediation_register"])),
            "source_seed_affordance_rows": int(len(seed_rows)),
        },
    }

    write_json_artifact(packet_path, packet)
    write_json_artifact(input_manifest_path, input_inspection)
    write_json_artifact(
        handoff_manifest_path,
        {
            "run_id": run_id,
            "layer": "v555",
            "created_at": utc_now(),
            "v556_handoff_rows": int(len(registers["v556_handoff_index"])),
            "ready_for_v556": True,
        },
    )

    build_record = build_layer_build_record(
        spec=type("Spec", (), {"layer": "v555", "title": "Life-course mediation bridge adapter", "artifact_slug": "v555_life_course_mediation_packet"})(),
        input_inspection=input_inspection,
        status="THIN_READY" if input_inspection.get("input_status") == "ready" else "THIN_READY_WITH_INPUT_GAPS",
        packet_path=repo_relative_path_text(packet_path),
        schema_path=repo_relative_path_text(root["schemas"] / "v555_life_course_mediation_packet.schema.json"),
        audit_path=repo_relative_path_text(root["audits"] / "v555_forbidden_inference_audit.parquet"),
        readiness_path=repo_relative_path_text(readiness_path),
        input_manifest_path=repo_relative_path_text(input_manifest_path),
        run_id=run_id,
    )

    readiness = {
        "run_id": run_id,
        "layer": "v555",
        "status": packet["status"],
        "ready_for_v556": True,
        "ready_for_runtime_consumption": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "packet_path": repo_relative_path_text(packet_path),
        "schema_path": repo_relative_path_text(root["schemas"] / "v555_life_course_mediation_packet.schema.json"),
        "audit_path": repo_relative_path_text(root["audits"] / "v555_forbidden_inference_audit.parquet"),
        "readiness_path": repo_relative_path_text(readiness_path),
        "input_manifest_path": repo_relative_path_text(input_manifest_path),
        "upstream_requirements": {
            "required_upstream_artifacts": [
                "packets/v554_bounded_seed_affordance_contract_packet.json",
                "packets/v554_seed_affordance_index.parquet",
                "manifest/v554_readiness_report.json",
                "packets/v553_year_indexed_pressure_over_time.parquet",
                "manifest/v553_wave_harmonization_report.json",
                "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
            ]
        },
        "input_status": input_inspection["input_status"],
        "missing_required_inputs": input_inspection["missing_required_inputs"],
        "input_readiness_score": _bounded_score(float(v554_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "upstream_readiness_score": _bounded_score(float(v554_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "boundary_readiness_score": _bounded_score(float(v554_readiness.get("boundary_readiness_score", 0.0) or 0.0)),
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "created_at": utc_now(),
        "schema_version": V555_SCHEMA_VERSION,
        "compiler_version": V555_COMPILER_VERSION,
        "mediation_contract_summary": packet["mediation_contract_summary"],
        "v554_seed_affordance_index_path": repo_relative_path_text(v554_seed_affordance_path),
        "v554_seed_affordance_index_rows": int(len(v554_seed_affordance_df)),
        "source_seed_affordance_rows_consumed": int(len(seed_rows)),
        "v556_handoff_index_path": repo_relative_path_text(handoff_index_path),
        "artifact_paths": {
            "mediation_slot_contracts": repo_relative_path_text(slot_path),
            "household_register": repo_relative_path_text(household_path),
            "parent_transmission_register": repo_relative_path_text(parent_path),
            "co_parent_transmission_register": repo_relative_path_text(coparent_path),
            "child_absorption_register": repo_relative_path_text(child_path),
            "carrier_mediation_register": repo_relative_path_text(carrier_path),
            "life_course_stop_reason_ledger": repo_relative_path_text(stop_path),
            "v556_handoff_index": repo_relative_path_text(handoff_index_path),
        },
        "artifact_infos": {
            "mediation_slot_contracts": slot_info,
            "household_register": household_info,
            "parent_transmission_register": parent_info,
            "co_parent_transmission_register": coparent_info,
            "child_absorption_register": child_info,
            "carrier_mediation_register": carrier_info,
            "life_course_stop_reason_ledger": stop_info,
            "v556_handoff_index": handoff_info,
        },
        "readiness": {
            "status": "READY_V555_MEDIATION_WITH_LIMITATIONS",
            "limitations_kind": limitations_kind,
            "limitations_reason": limitations_reason,
            "ready_for_v556": True,
            "mediation_contract_rows": int(len(slot_df)),
            "household_register_rows": int(len(registers["household_register"])),
            "parent_transmission_rows": int(len(registers["parent_transmission_register"])),
            "co_parent_transmission_rows": int(len(registers["co_parent_transmission_register"])),
            "child_absorption_rows": int(len(registers["child_absorption_register"])),
            "carrier_mediation_rows": int(len(registers["carrier_mediation_register"])),
            "source_seed_affordance_rows": int(len(seed_rows)),
            "v554_readiness_status": _clean(v554_readiness.get("status")),
        },
    }
    write_json_artifact(readiness_path, readiness)
    build_record_path = root["manifest"] / "v555_build_record.json"
    write_json_artifact(build_record_path, build_record)
    return {
        "readiness": readiness,
        "artifact_paths": readiness["artifact_paths"],
        "artifact_infos": readiness["artifact_infos"],
        "build_record": build_record,
        "packet_path": readiness["packet_path"],
        "schema_path": readiness["schema_path"],
        "audit_path": readiness["audit_path"],
        "readiness_path": readiness["readiness_path"],
        "input_manifest_path": readiness["input_manifest_path"],
        "v556_handoff_index_path": readiness["v556_handoff_index_path"],
    }


__all__ = ["build_v555_life_course_mediation", "V555_SCHEMA_VERSION", "V555_COMPILER_VERSION"]
