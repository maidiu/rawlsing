#!/usr/bin/env python3
"""Compile a downstream requirements report for V552 through V558."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_thin_end_to_end import LAYER_REQUIREMENTS  # noqa: E402
from data.ddm_build_copy.ddm_latest_run import latest_dir  # noqa: E402
from data.ddm_build_copy.ddm_v553_harmonization import build_v553_wave_harmonization, validate_v553_wave_harmonization_report  # noqa: E402
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity  # noqa: E402
from data.ddm_build_copy.ddm_v553_repo_discovery import (  # noqa: E402
    build_wave_descriptors_from_repo,
    latest_run_root_for_wave,
)


def _exists(root: Path, relative_path: str) -> bool:
    path = root / relative_path
    return path.exists()


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def _thin_layer_roots(thin_root: Path | None) -> dict[str, Path]:
    if thin_root is None:
        return {}
    readiness = _read_json(thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json")
    roots: dict[str, Path] = {}
    for row in readiness.get("layer_reports", []) if isinstance(readiness.get("layer_reports", []), list) else []:
        if not isinstance(row, dict):
            continue
        layer = str(row.get("layer", "")).strip()
        layer_root = str(row.get("layer_output_root", "")).strip()
        if layer and layer_root:
            roots[layer] = Path(layer_root)
    return roots


def _layer_status(
    layer: str,
    *,
    repo_root: Path,
    v551j_root: Path | None,
    v552j_root: Path | None,
    v552_root: Path | None,
    v553_wave_report: dict[str, Any],
    v553_temporal_root: Path | None,
    thin_root: Path | None,
    thin_layer_roots: dict[str, Path],
) -> dict[str, Any]:
    requirements = LAYER_REQUIREMENTS.get(layer, {})
    if layer == "v552j":
        base = v551j_root
    elif layer == "v553":
        base = v552j_root
    elif layer in {"v554", "v555", "v556", "v557", "v558"}:
        base = thin_layer_roots.get(layer)
    else:
        base = None

    missing: list[str] = []
    present: list[str] = []
    for rel in requirements.get("required_upstream_artifacts", []):
        exists = False
        if layer == "v553":
            if v552j_root is not None:
                exists = _exists(v552j_root, rel)
        elif base is not None:
            exists = _exists(base, rel)
        if exists:
            present.append(rel)
        else:
            missing.append(rel)

    if layer == "v552j":
        status = "ready" if not missing else "blocked"
        runtime_ready = False
    elif layer == "v553":
        status = str(v553_wave_report.get("overall_status", "STATUS: UNKNOWN"))
        runtime_ready = bool(v553_wave_report.get("ready_for_v553", False))
        if v553_temporal_root is None:
            missing.extend(["v553_temporal_pressure_field packet root"])
    else:
        readiness_path = None if base is None else base / "manifest" / f"{layer}_readiness_report.json"
        readiness = _read_json(readiness_path) if readiness_path else {}
        status = str(readiness.get("status", "THIN_BLOCKED_MISSING_REQUIRED_INPUT")) if readiness else "THIN_BLOCKED_MISSING_REQUIRED_INPUT"
        runtime_ready = bool(readiness.get("ready_for_runtime_consumption", False))
        if readiness_path is None or not readiness_path.exists():
            missing.append(f"manifest/{layer}_readiness_report.json")

    return {
        "layer": layer,
        "status": status,
        "runtime_ready": runtime_ready,
        "required_upstream_artifacts": list(requirements.get("required_upstream_artifacts", [])),
        "required_upstream_authority": list(requirements.get("required_upstream_authority", [])),
        "downstream_outputs_expected": list(requirements.get("downstream_outputs_expected", [])),
        "present_requirements": present,
        "missing_requirements": missing,
        "buildable_from_repo_state": len(missing) == 0,
        "upstream_root": str(base) if base is not None else "",
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# V552 Through V557 Downstream Requirements Report",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- V551J latest root: `{report['latest_v551j_root']}`",
        f"- V552J latest root: `{report['latest_v552j_root']}`",
        f"- V552J readiness status: `{report.get('latest_v552j_readiness', {}).get('status', '')}`",
        f"- V552 latest root: `{report['latest_v552_root']}`",
        f"- V553 harmonization status: `{report['v553_wave_harmonization']['overall_status']}`",
        f"- V553 temporal root: `{report['latest_v553_temporal_root']}`",
        f"- Thin end-to-end root: `{report['latest_thin_root']}`",
        "",
        "## Layer Summary",
        "",
        "| Layer | Status | Buildable From Repo State | Runtime Ready | Missing Requirements |",
        "| --- | --- | --- | --- | --- |",
    ]
    for layer in report["layers"]:
        lines.append(
            "| {layer} | {status} | {buildable} | {runtime_ready} | {missing} |".format(
                layer=layer["layer"],
                status=layer["status"],
                buildable="yes" if layer["buildable_from_repo_state"] else "no",
                runtime_ready="yes" if layer["runtime_ready"] else "no",
                missing=", ".join(layer["missing_requirements"]) if layer["missing_requirements"] else "none",
            )
        )
    lines.extend([
        "",
        "## Notes",
        "",
        "- `v552` remains the conservative structural handoff.",
        "- `v552j` now exposes blocker summaries explicitly; missing comparability is informational, not a required blocker.",
        "- `v553` becomes meaningful only when multiple waves and shared authority overlays are present.",
        "- `v554` through `v558` are scaffold layers and intentionally remain non-runtime.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a downstream requirements report for V552 through V558.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--wave", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    output_dir = Path(args.output_dir)
    identity = require_survey_identity(
        args.source,
        args.wave,
        args.country_code,
        require_country=True,
    )

    def selected_root(directory: str) -> Path | None:
        resolved = latest_run_root_for_wave(
            repo_root / "data" / "ddm_repository_copy" / directory / "runs",
            identity.source,
            identity.canonical_wave,
            identity.country_code,
        )
        return Path(resolved) if resolved else None

    latest_v551j_root = selected_root("v551j")
    latest_v552j_root = selected_root("v552j")
    latest_v552_root = selected_root("v552")
    latest_v553_temporal_root = selected_root("v553")
    latest_thin_root = selected_root("v5_thin_end_to_end")
    thin_layer_roots = _thin_layer_roots(latest_thin_root)
    latest_v552j_readiness = _read_json(latest_v552j_root / "manifest" / "v552j_readiness_report.json") if latest_v552j_root else {}

    wave_descriptors, wave_discovery = build_wave_descriptors_from_repo(
        repo_root=repo_root,
        survey_family=identity.source,
        country_code=identity.country_code,
    )
    wave_harmonization_table, wave_harmonization_report = build_v553_wave_harmonization(wave_descriptors)
    wave_harmonization_errors = validate_v553_wave_harmonization_report(wave_harmonization_report)

    layers = []
    for layer in ("v552j", "v553", "v554", "v555", "v556", "v557", "v558"):
        layers.append(
            _layer_status(
                layer,
                repo_root=repo_root,
                v551j_root=latest_v551j_root,
                v552j_root=latest_v552j_root,
                v552_root=latest_v552_root,
                v553_wave_report=wave_harmonization_report,
                v553_temporal_root=latest_v553_temporal_root,
                thin_root=latest_thin_root,
                thin_layer_roots=thin_layer_roots,
            )
        )

    report = {
        "repo_root": str(repo_root),
        "source": identity.source,
        "country_code": identity.country_code,
        "wave": identity.canonical_wave,
        "created_at": wave_harmonization_report.get("created_at", ""),
        "latest_v551j_root": str(latest_v551j_root) if latest_v551j_root else "",
        "latest_v552j_root": str(latest_v552j_root) if latest_v552j_root else "",
        "latest_v552j_readiness": latest_v552j_readiness,
        "latest_v552_root": str(latest_v552_root) if latest_v552_root else "",
        "latest_v553_temporal_root": str(latest_v553_temporal_root) if latest_v553_temporal_root else "",
        "latest_thin_root": str(latest_thin_root) if latest_thin_root else "",
        "latest_thin_layer_roots": {layer: str(path) for layer, path in thin_layer_roots.items()},
        "v553_repo_discovery": wave_discovery,
        "v553_wave_harmonization": wave_harmonization_report,
        "v553_wave_harmonization_validation_errors": wave_harmonization_errors,
        "layers": layers,
    }

    _write_json(output_dir / "V552_THROUGH_V558_DOWNSTREAM_REQUIREMENTS_REPORT.json", report)
    _write_markdown(output_dir / "V552_THROUGH_V558_DOWNSTREAM_REQUIREMENTS_REPORT.md", report)
    print(output_dir / "V552_THROUGH_V558_DOWNSTREAM_REQUIREMENTS_REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
