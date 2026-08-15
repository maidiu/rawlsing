#!/usr/bin/env python3
"""Compile a paired-wave preflight report for the V552 -> V557 path."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_latest_run import latest_dir
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity
from data.ddm_build_copy.ddm_v553_repo_discovery import latest_run_root_for_wave


def _exists(root: Path | None, relative_path: str) -> bool:
    return bool(root and (root / relative_path).exists())


def _wave_roots(
    repo_root: Path,
    source: str,
    wave: str,
    country_code: str,
) -> dict[str, Path | None]:
    identity = require_survey_identity(
        source,
        wave,
        country_code,
        require_country=True,
    )
    roots: dict[str, Path | None] = {}
    for layer in ("v551j", "v552j", "v552", "v553"):
        resolved = latest_run_root_for_wave(
            repo_root / "data" / "ddm_repository_copy" / layer / "runs",
            identity.source,
            identity.canonical_wave,
            identity.country_code,
        )
        roots[layer] = Path(resolved) if resolved else None
    return roots


def _wave_report(
    repo_root: Path,
    source: str,
    wave: str,
    country_code: str,
) -> dict[str, Any]:
    identity = require_survey_identity(
        source,
        wave,
        country_code,
        require_country=True,
    )
    roots = _wave_roots(
        repo_root,
        identity.source,
        identity.canonical_wave,
        identity.country_code,
    )
    required_artifacts = {
        "v551j": [
            "manifest/v551j_readiness_report.json",
            "manifest/v551j_input_provenance_manifest.json",
        ],
        "v552j": [
            "manifest/v552j_readiness_report.json",
            "packets/v552j_structural_handoff_packet.json",
        ],
        "v552": [
            "manifest/v552_input_provenance_manifest.json",
            "structural/v552_artifact_authority_index.parquet",
            "structural/v552_known_absence_register.parquet",
        ],
        "v553": [
            "manifest/v553_temporal_readiness_report.json",
            "manifest/v553_wave_harmonization_report.json",
        ],
    }
    missing: list[str] = []
    present: list[str] = []
    for layer, rel_paths in required_artifacts.items():
        for rel_path in rel_paths:
            token = f"{layer}:{rel_path}"
            if _exists(roots.get(layer), rel_path):
                present.append(token)
            else:
                missing.append(token)
    status = "ready" if not missing else "blocked"
    return {
        "source": identity.source,
        "country_code": identity.country_code,
        "wave": identity.canonical_wave,
        "status": status,
        "latest_roots": {layer: str(path) if path else "" for layer, path in roots.items()},
        "required_artifacts": required_artifacts,
        "present_artifacts": present,
        "missing_artifacts": missing,
        "comparison_ready": not missing,
    }


def build_paired_wave_preflight(
    repo_root: str | Path,
    source: str,
    country_code: str,
    wave_a: str,
    wave_b: str,
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    wave_a_report = _wave_report(repo_root, source, wave_a, country_code)
    wave_b_report = _wave_report(repo_root, source, wave_b, country_code)
    missing = sorted(set(wave_a_report["missing_artifacts"]) | set(wave_b_report["missing_artifacts"]))
    comparison_ready = not missing
    status = "PAIRED_WAVE_READY" if comparison_ready else "PAIRED_WAVE_BLOCKED"
    return {
        "repo_root": str(repo_root),
        "created_at": utc_now(),
        "source": wave_a_report["source"],
        "country_code": wave_a_report["country_code"],
        "wave_a": wave_a,
        "wave_b": wave_b,
        "status": status,
        "comparison_ready": comparison_ready,
        "missing_artifacts": missing,
        "wave_reports": [wave_a_report, wave_b_report],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Paired Wave Preflight Report",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Wave A: `{report['wave_a']}`",
        f"- Wave B: `{report['wave_b']}`",
        f"- Status: `{report['status']}`",
        f"- Comparison ready: `{report['comparison_ready']}`",
        "",
        "## Wave Summary",
        "",
        "| Wave | Status | Missing Artifacts |",
        "| --- | --- | --- |",
    ]
    for wave_report in report["wave_reports"]:
        lines.append(
            "| {wave} | {status} | {missing} |".format(
                wave=wave_report["wave"],
                status=wave_report["status"],
                missing=", ".join(wave_report["missing_artifacts"]) if wave_report["missing_artifacts"] else "none",
            )
        )
    lines.extend(
        [
            "",
            "## Missing Artifacts",
            "",
            *([f"- {item}" for item in report["missing_artifacts"]] or ["- none"]),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a paired-wave preflight report.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--wave-a", required=True)
    parser.add_argument("--wave-b", required=True)
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    args = parser.parse_args()

    report = build_paired_wave_preflight(
        args.repo_root,
        args.source,
        args.country_code,
        args.wave_a,
        args.wave_b,
    )
    output_dir = Path(args.output_dir)
    _write_json(output_dir / "V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.json", report)
    _write_markdown(output_dir / "V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.md", report)
    print(output_dir / "V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
