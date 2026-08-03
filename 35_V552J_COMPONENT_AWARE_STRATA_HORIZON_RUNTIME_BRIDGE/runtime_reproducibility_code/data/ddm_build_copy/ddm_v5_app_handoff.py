#!/usr/bin/env python3
"""Build an app-facing handoff bundle from the thin V5 chain and V558+ governance.

This bundle is intentionally non-runtime. It packages the latest thin chain and
V558+ governance outputs into a single app-review surface that can be inspected
without exposing raw evidence tables or generating persona content.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, write_frame_artifact, write_json_artifact

try:  # pragma: no cover
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v5_app_handoff" / "runs"

SCHEMA_VERSION = "v5_app_handoff_0.1"
COMPILER_VERSION = "v5_app_handoff_0.1"


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


def _load_thin_bundle(thin_run_root: Path) -> dict[str, Any]:
    manifest = thin_run_root / "manifest"
    packet = thin_run_root / "layers"
    readiness_path = manifest / "v5_thin_end_to_end_readiness_report.json"
    return {
        "readiness_path": repo_relative_path_text(readiness_path),
        "readiness": _read_json(readiness_path),
        "root": repo_relative_path_text(thin_run_root),
        "exists": thin_run_root.exists(),
    }


def _load_v558_plus_bundle(v558_plus_run_root: Path) -> dict[str, Any]:
    manifest = v558_plus_run_root / "manifest"
    packet = v558_plus_run_root / "packets"
    readiness_path = manifest / "v558_plus_readiness_report.json"
    build_ledger_path = manifest / "v558_plus_build_ledger.json"
    app_packet_path = packet / "v558_app_runtime_handoff_packet.json"
    app_readiness_path = manifest / "v558_app_runtime_handoff_readiness_report.json"
    return {
        "readiness_path": repo_relative_path_text(readiness_path),
        "build_ledger_path": repo_relative_path_text(build_ledger_path),
        "app_packet_path": repo_relative_path_text(app_packet_path),
        "app_readiness_path": repo_relative_path_text(app_readiness_path),
        "readiness": _read_json(readiness_path),
        "build_ledger": _read_json(build_ledger_path),
        "app_packet": _read_json(app_packet_path),
        "app_readiness": _read_json(app_readiness_path),
        "root": repo_relative_path_text(v558_plus_run_root),
        "exists": v558_plus_run_root.exists(),
    }


def _status_from_inputs(thin_bundle: dict[str, Any], v558_plus_bundle: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    blockers: list[dict[str, Any]] = []
    thin_status = _clean(thin_bundle.get("readiness", {}).get("final_status") or thin_bundle.get("readiness", {}).get("status"))
    v558_plus_status = _clean(v558_plus_bundle.get("readiness", {}).get("status") or v558_plus_bundle.get("build_ledger", {}).get("final_status"))
    app_handoff_status = _clean(v558_plus_bundle.get("app_readiness", {}).get("status"))

    if not thin_bundle.get("exists") or not thin_bundle.get("readiness"):
        blockers.append({"blocker_code": "missing_thin_end_to_end_readiness", "status": "blocked"})
    if not v558_plus_bundle.get("exists") or not v558_plus_bundle.get("readiness"):
        blockers.append({"blocker_code": "missing_v558_plus_readiness", "status": "blocked"})
    if thin_status.startswith("BLOCKED"):
        blockers.append({"blocker_code": "thin_chain_blocked", "status": "blocked", "details": {"thin_status": thin_status}})
    if v558_plus_status.startswith("BLOCKED"):
        blockers.append({"blocker_code": "v558_plus_blocked", "status": "blocked", "details": {"v558_plus_status": v558_plus_status}})
    if app_handoff_status.startswith("BLOCKED"):
        blockers.append({"blocker_code": "v558_plus_app_handoff_blocked", "status": "blocked", "details": {"app_handoff_status": app_handoff_status}})

    if blockers:
        return "V5_APP_HANDOFF_BLOCKED", blockers
    return "V5_APP_HANDOFF_READY_FOR_REVIEW", blockers


def _packet_row(
    *,
    run_id: str,
    wave: str,
    thin_bundle: dict[str, Any],
    v558_plus_bundle: dict[str, Any],
    status: str,
    blockers: list[dict[str, Any]],
) -> dict[str, Any]:
    thin_status = _clean(thin_bundle.get("readiness", {}).get("final_status") or thin_bundle.get("readiness", {}).get("status"))
    v558_plus_status = _clean(v558_plus_bundle.get("readiness", {}).get("status"))
    thin_limitations_kind = _clean(thin_bundle.get("readiness", {}).get("limitations_kind"))
    v558_plus_limitations_kind = _clean(v558_plus_bundle.get("readiness", {}).get("limitations_kind") or v558_plus_bundle.get("build_ledger", {}).get("limitations_kind"))
    return {
        "app_handoff_id": f"{run_id}__{wave}__app_handoff",
        "run_id": run_id,
        "wave": wave,
        "thin_run_root": thin_bundle.get("root", ""),
        "v558_plus_run_root": v558_plus_bundle.get("root", ""),
        "thin_status": thin_status,
        "thin_limitations_kind": thin_limitations_kind,
        "v558_plus_status": v558_plus_status,
        "v558_plus_limitations_kind": v558_plus_limitations_kind,
        "status": status,
        "ready_for_app_integration_review": status == "V5_APP_HANDOFF_READY_FOR_REVIEW",
        "ready_for_runtime": False,
        "app_integration_authorized": status == "V5_APP_HANDOFF_READY_FOR_REVIEW",
        "runtime_generation_authorized": False,
        "blocker_count": len(blockers),
        "blocked_claim_ids_json": json.dumps(
            sorted({_clean(item.get("blocker_code") or item.get("reason")) for item in blockers if _clean(item.get("blocker_code") or item.get("reason"))}),
            ensure_ascii=False,
        ),
        "allowed_use": "app_integration_review_only",
        "forbidden_use": "runtime_persona_generation",
        "created_at": utc_now(),
        "schema_version": SCHEMA_VERSION,
        "compiler_version": COMPILER_VERSION,
    }


def build_v5_app_handoff_bundle(
    *,
    run_id: str,
    wave: str,
    thin_run_root: str | Path,
    v558_plus_run_root: str | Path,
    output_root: str | Path = DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT,
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    thin_root = Path(thin_run_root)
    v558_plus_root = Path(v558_plus_run_root)
    output_root = Path(output_root)
    output_dirs = ensure_output_dirs(output_root, run_id)

    thin_bundle = _load_thin_bundle(thin_root)
    v558_plus_bundle = _load_v558_plus_bundle(v558_plus_root)
    status, blockers = _status_from_inputs(thin_bundle, v558_plus_bundle)
    packet_row = _packet_row(run_id=run_id, wave=wave, thin_bundle=thin_bundle, v558_plus_bundle=v558_plus_bundle, status=status, blockers=blockers)

    packet_df = pd.DataFrame([packet_row])
    blocker_df = pd.DataFrame(blockers) if blockers else pd.DataFrame([{"blocker_code": "", "status": "pass"}])
    inputs_df = pd.DataFrame(
        [
            {
                "run_id": run_id,
                "wave": wave,
                "thin_run_root": thin_bundle.get("root", ""),
                "v558_plus_run_root": v558_plus_bundle.get("root", ""),
                "thin_readiness_path": thin_bundle.get("readiness_path", ""),
                "v558_plus_readiness_path": v558_plus_bundle.get("readiness_path", ""),
                "v558_plus_app_packet_path": v558_plus_bundle.get("app_packet_path", ""),
                "v558_plus_app_readiness_path": v558_plus_bundle.get("app_readiness_path", ""),
                "created_at": utc_now(),
            }
        ]
    )

    packet_info = write_frame_artifact(
        packet_df,
        path=output_dirs["packets"] / "v5_app_handoff_packet.parquet",
        schema_path=output_dirs["schemas"] / "v5_app_handoff_packet.schema.json",
        name="v5_app_handoff_packet",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    blocker_info = write_frame_artifact(
        blocker_df,
        path=output_dirs["audits"] / "v5_app_handoff_blockers.parquet",
        schema_path=output_dirs["schemas"] / "v5_app_handoff_blockers.schema.json",
        name="v5_app_handoff_blockers",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    inputs_info = write_frame_artifact(
        inputs_df,
        path=output_dirs["manifest"] / "v5_app_handoff_inputs.parquet",
        schema_path=output_dirs["schemas"] / "v5_app_handoff_inputs.schema.json",
        name="v5_app_handoff_inputs",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )

    readiness = {
        "run_id": run_id,
        "wave": wave,
        "status": status,
        "ready_for_app_integration_review": status == "V5_APP_HANDOFF_READY_FOR_REVIEW",
        "ready_for_runtime": False,
        "app_integration_authorized": status == "V5_APP_HANDOFF_READY_FOR_REVIEW",
        "runtime_generation_authorized": False,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "thin": thin_bundle,
        "v558_plus": v558_plus_bundle,
        "thin_limitations_kind": _clean(thin_bundle.get("readiness", {}).get("limitations_kind")),
        "v558_plus_limitations_kind": _clean(v558_plus_bundle.get("readiness", {}).get("limitations_kind") or v558_plus_bundle.get("build_ledger", {}).get("limitations_kind")),
        "packet_path": repo_relative_path_text(output_dirs["packets"] / "v5_app_handoff_packet.parquet"),
        "blockers_path": repo_relative_path_text(output_dirs["audits"] / "v5_app_handoff_blockers.parquet"),
        "inputs_path": repo_relative_path_text(output_dirs["manifest"] / "v5_app_handoff_inputs.parquet"),
        "readiness_report_path": repo_relative_path_text(output_dirs["manifest"] / "v5_app_handoff_readiness_report.json"),
        "build_ledger_path": repo_relative_path_text(output_dirs["manifest"] / "v5_app_handoff_build_ledger.json"),
        "artifact_paths": {
            "packet": packet_info,
            "blockers": blocker_info,
            "inputs": inputs_info,
        },
    }

    write_json_artifact(output_dirs["manifest"] / "v5_app_handoff_readiness_report.json", readiness)
    write_json_artifact(
        output_dirs["manifest"] / "v5_app_handoff_build_ledger.json",
        {
            "run_id": run_id,
            "wave": wave,
            "build_kind": "v5_app_handoff_bundle",
            "status": status,
            "readiness_report_path": readiness["readiness_report_path"],
            "packet_path": readiness["packet_path"],
            "blockers_path": readiness["blockers_path"],
            "inputs_path": readiness["inputs_path"],
            "created_at": utc_now(),
            "schema_version": SCHEMA_VERSION,
            "compiler_version": COMPILER_VERSION,
            "input_roots": {
                "thin_run_root": thin_bundle.get("root", ""),
                "v558_plus_run_root": v558_plus_bundle.get("root", ""),
            },
        },
    )

    return readiness


def validate_v5_app_handoff_bundle(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not readiness.get("packet_path"):
        errors.append("missing packet path")
    if not readiness.get("readiness_report_path"):
        errors.append("missing readiness report path")
    if readiness.get("status") not in {"V5_APP_HANDOFF_READY_FOR_REVIEW", "V5_APP_HANDOFF_BLOCKED"}:
        errors.append("unexpected app handoff status")
    if readiness.get("ready_for_runtime"):
        errors.append("runtime must remain false")
    return errors


__all__ = [
    "DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT",
    "SCHEMA_VERSION",
    "COMPILER_VERSION",
    "build_v5_app_handoff_bundle",
    "validate_v5_app_handoff_bundle",
]
