#!/usr/bin/env python3
"""Compile a final V5 runtime boundary bundle from the latest available roots.

This is intentionally not runtime persona generation. It packages the latest
thin end-to-end chain and V558+ governance into one app-facing review bundle
so downstream work can consume a single concrete boundary artifact.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_latest_run import latest_dir  # noqa: E402
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text  # noqa: E402
from data.ddm_build_copy.ddm_v5_app_handoff import (  # noqa: E402
    DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT,
    build_v5_app_handoff_bundle,
    validate_v5_app_handoff_bundle,
)
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, write_json_artifact, write_frame_artifact  # noqa: E402
from data.ddm_build_copy.ddm_v550_manifest import utc_now  # noqa: E402
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity  # noqa: E402
from data.ddm_build_copy.ddm_v553_repo_discovery import latest_run_root_for_wave  # noqa: E402


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _discover_latest_roots(
    repo_root: Path,
    source: str,
    wave: str,
    country_code: str,
    thin_run_root: str | Path | None,
    v558_plus_run_root: str | Path | None,
) -> tuple[Path | None, Path | None]:
    identity = require_survey_identity(
        source,
        wave,
        country_code,
        require_country=True,
    )
    thin_discovered = latest_run_root_for_wave(
        repo_root / "data" / "ddm_repository_copy" / "v5_thin_end_to_end" / "runs",
        identity.source,
        identity.canonical_wave,
        identity.country_code,
    )
    v558_plus_discovered = latest_run_root_for_wave(
        repo_root / "data" / "ddm_repository_copy" / "v558_plus" / "runs",
        identity.source,
        identity.canonical_wave,
        identity.country_code,
    )
    thin_root = Path(thin_run_root) if thin_run_root else (Path(thin_discovered) if thin_discovered else None)
    v558_plus_root = Path(v558_plus_run_root) if v558_plus_run_root else (Path(v558_plus_discovered) if v558_plus_discovered else None)
    return thin_root, v558_plus_root


def _final_bundle_row(
    *,
    run_id: str,
    source: str,
    country_code: str,
    wave: str,
    thin_run_root: Path,
    v558_plus_run_root: Path,
    app_handoff_readiness: dict[str, Any],
    v558_plus_readiness: dict[str, Any],
    thin_readiness: dict[str, Any],
) -> dict[str, Any]:
    blockers = app_handoff_readiness.get("blockers", []) if isinstance(app_handoff_readiness.get("blockers", []), list) else []
    return {
        "final_runtime_bundle_id": f"{run_id}__{wave}__final_runtime_bundle",
        "run_id": run_id,
        "source": source,
        "country_code": country_code,
        "wave": wave,
        "thin_run_root": repo_relative_path_text(thin_run_root),
        "v558_plus_run_root": repo_relative_path_text(v558_plus_run_root),
        "thin_status": str(thin_readiness.get("final_status") or thin_readiness.get("status") or ""),
        "thin_limitations_kind": str(thin_readiness.get("limitations_kind") or ""),
        "v558_plus_status": str(v558_plus_readiness.get("status") or ""),
        "v558_plus_limitations_kind": str(v558_plus_readiness.get("limitations_kind") or v558_plus_readiness.get("build_ledger", {}).get("limitations_kind") or ""),
        "app_handoff_status": str(app_handoff_readiness.get("status") or ""),
        "status": str(app_handoff_readiness.get("status") or "V5_FINAL_RUNTIME_BUNDLE_BLOCKED"),
        "ready_for_app_integration_review": bool(app_handoff_readiness.get("ready_for_app_integration_review", False)),
        "ready_for_runtime": False,
        "app_integration_authorized": bool(app_handoff_readiness.get("app_integration_authorized", False)),
        "runtime_generation_authorized": False,
        "blocker_count": int(app_handoff_readiness.get("blocker_count", len(blockers)) or 0),
        "blocked_claim_ids_json": str(app_handoff_readiness.get("blocked_claim_ids_json", "[]") or "[]"),
        "created_at": utc_now(),
        "boundary_only_limitations": True,
        "limitations_kind": "boundary_only_not_runtime",
        "limitations_reason": [
            "final_runtime_bundle_is_a_boundary_review_artifact_not_runtime_persona_generation",
            "ready_for_runtime_remains_false",
        ],
        "app_handoff_readiness_report_path": str(app_handoff_readiness.get("readiness_report_path", "")),
    }


def build_v5_final_runtime_bundle(
    *,
    run_id: str,
    source: str,
    country_code: str,
    wave: str,
    repo_root: str | Path = ROOT,
    thin_run_root: str | Path | None = None,
    v558_plus_run_root: str | Path | None = None,
    output_root: str | Path = DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT.parent / "v5_final_runtime_bundle" / "runs",
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    identity = require_survey_identity(
        source,
        wave,
        country_code,
        require_country=True,
    )
    wave = identity.canonical_wave
    source = identity.source
    country_code = identity.country_code
    thin_root, v558_plus_root = _discover_latest_roots(
        repo_root,
        source,
        wave,
        country_code,
        thin_run_root,
        v558_plus_run_root,
    )
    if thin_root is None:
        raise RuntimeError(f"Missing thin run root for wave {wave}")
    if v558_plus_root is None:
        raise RuntimeError(f"Missing V558+ run root for wave {wave}")

    app_handoff = build_v5_app_handoff_bundle(
        run_id=run_id,
        wave=wave,
        thin_run_root=thin_root,
        v558_plus_run_root=v558_plus_root,
        output_root=output_root,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    errors = validate_v5_app_handoff_bundle(app_handoff)
    if errors:
        raise RuntimeError("V5_FINAL_RUNTIME_BUNDLE_APP_HANDOFF_FAILED: " + "; ".join(errors))

    thin_readiness = _read_json(thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json")
    v558_plus_readiness = _read_json(v558_plus_root / "manifest" / "v558_plus_readiness_report.json")

    root = ensure_output_dirs(output_root, run_id)
    packet_row = _final_bundle_row(
        run_id=run_id,
        source=source,
        country_code=country_code,
        wave=wave,
        thin_run_root=thin_root,
        v558_plus_run_root=v558_plus_root,
        app_handoff_readiness=app_handoff,
        v558_plus_readiness=v558_plus_readiness,
        thin_readiness=thin_readiness,
    )
    packet_df = pd.DataFrame([packet_row])

    packet_path = root["packets"] / "v5_final_runtime_bundle_packet.parquet"
    packet_json_path = root["packets"] / "v5_final_runtime_bundle_packet.json"
    readiness_path = root["manifest"] / "v5_final_runtime_bundle_readiness_report.json"
    build_ledger_path = root["manifest"] / "v5_final_runtime_bundle_build_ledger.json"
    input_manifest_path = root["manifest"] / "v5_final_runtime_bundle_inputs.json"
    schema_path = root["schemas"] / "v5_final_runtime_bundle_packet.schema.json"

    packet_info = write_frame_artifact(
        packet_df,
        path=packet_path,
        schema_path=schema_path,
        name="v5_final_runtime_bundle_packet",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    write_json_artifact(packet_json_path, {"run_id": run_id, "rows": [packet_row], "row_count": 1, "created_at": utc_now()})
    write_json_artifact(
        input_manifest_path,
        {
            "run_id": run_id,
            "source": source,
            "country_code": country_code,
            "wave": wave,
            "repo_root": repo_relative_path_text(repo_root),
            "thin_run_root": repo_relative_path_text(thin_root),
            "v558_plus_run_root": repo_relative_path_text(v558_plus_root),
            "app_handoff_readiness_report": app_handoff.get("readiness_report_path", ""),
            "app_handoff_packet_path": app_handoff.get("packet_path", ""),
            "created_at": utc_now(),
        },
    )

    readiness = {
        "run_id": run_id,
        "source": source,
        "country_code": country_code,
        "wave": wave,
        "status": app_handoff["status"],
        "final_status": app_handoff["status"],
        "ready_for_app_integration_review": bool(app_handoff.get("ready_for_app_integration_review", False)),
        "ready_for_runtime": False,
        "runtime_generation_authorized": False,
        "app_integration_authorized": bool(app_handoff.get("app_integration_authorized", False)),
        "blocker_count": int(app_handoff.get("blocker_count", 0) or 0),
        "blockers": app_handoff.get("blockers", []),
        "thin_status": thin_readiness.get("final_status") or thin_readiness.get("status", ""),
        "v558_plus_status": v558_plus_readiness.get("status", ""),
        "thin_limitations_kind": thin_readiness.get("limitations_kind", ""),
        "v558_plus_limitations_kind": v558_plus_readiness.get("limitations_kind") or v558_plus_readiness.get("build_ledger", {}).get("limitations_kind", ""),
        "boundary_only_limitations": True,
        "limitations_kind": "boundary_only_not_runtime",
        "limitations_reason": [
            "final_runtime_bundle_is_a_boundary_review_artifact_not_runtime_persona_generation",
            "ready_for_runtime_remains_false",
        ],
        "packet_path": repo_relative_path_text(packet_path),
        "packet_json_path": repo_relative_path_text(packet_json_path),
        "readiness_report_path": repo_relative_path_text(readiness_path),
        "build_ledger_path": repo_relative_path_text(build_ledger_path),
        "input_manifest_path": repo_relative_path_text(input_manifest_path),
        "artifact_infos": {"v5_final_runtime_bundle_packet": packet_info},
        "app_handoff": app_handoff,
        "created_at": utc_now(),
    }
    write_json_artifact(readiness_path, readiness)
    write_json_artifact(
        build_ledger_path,
        {
            "run_id": run_id,
            "wave": wave,
            "build_kind": "v5_final_runtime_bundle",
            "final_status": readiness["status"],
            "created_at": utc_now(),
            "layer_records": [
                {
                    "layer": "v5_final_runtime_bundle",
                    "status": readiness["status"],
                    "ready_for_app_integration_review": readiness["ready_for_app_integration_review"],
                    "ready_for_runtime": readiness["ready_for_runtime"],
                    "runtime_generation_authorized": readiness["runtime_generation_authorized"],
                    "thin_status": readiness["thin_status"],
                    "v558_plus_status": readiness["v558_plus_status"],
                }
            ],
        },
    )
    return readiness


def validate_v5_final_runtime_bundle(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("status") != readiness.get("final_status"):
        errors.append("final status mismatch")
    if readiness.get("ready_for_runtime"):
        errors.append("runtime must remain false in final runtime bundle")
    if readiness.get("runtime_generation_authorized"):
        errors.append("runtime generation must remain unauthorized")
    if not readiness.get("packet_path"):
        errors.append("missing packet path")
    if not readiness.get("readiness_report_path"):
        errors.append("missing readiness report path")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the final V5 runtime boundary bundle.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--thin-run-root", default=None)
    parser.add_argument("--v558-plus-run-root", default=None)
    parser.add_argument("--output-root", default=str(DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT.parent / "v5_final_runtime_bundle" / "runs"))
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_v5_final_runtime_bundle(
        run_id=args.run_id,
        source=args.source,
        country_code=args.country_code,
        wave=args.wave,
        repo_root=args.repo_root,
        thin_run_root=args.thin_run_root,
        v558_plus_run_root=args.v558_plus_run_root,
        output_root=args.output_root,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    errors = validate_v5_final_runtime_bundle(readiness)
    if errors:
        raise RuntimeError("V5_FINAL_RUNTIME_BUNDLE_VALIDATION_FAILED: " + "; ".join(errors))
    if args.verbose:
        print(f"[V5_FINAL] status={readiness['status']}")
        print(f"[V5_FINAL] report={readiness['readiness_report_path']}")
        print(f"[V5_FINAL] blockers={readiness['blocker_count']}")
        print(f"[V5_FINAL] packet={readiness['packet_path']}")
    else:
        print(readiness["status"])
        print(readiness["readiness_report_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
