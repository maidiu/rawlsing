#!/usr/bin/env python3
"""Compile a full-chain status report for the current V5 upper stack.

This report is intentionally observational: it summarizes the latest roots,
readiness reports, and downstream coverage for one explicit survey scope
without attempting to rerun the pipeline itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_latest_run import latest_dir  # noqa: E402
from data.ddm_build_copy.ddm_v550_manifest import utc_now  # noqa: E402
from data.ddm_build_copy.compile_v5_paired_wave_preflight import build_paired_wave_preflight  # noqa: E402
from data.ddm_build_copy.ddm_v5_thin_end_to_end import LAYER_REQUIREMENTS  # noqa: E402
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


def _status_from_readiness(root: Path | None, rel_path: str) -> str:
    if root is None:
        return ""
    payload = _read_json(root / rel_path)
    return str(payload.get("status") or payload.get("final_status") or "")


def _wave_status(
    repo_root: Path,
    source: str,
    country_code: str,
    wave: str,
) -> dict[str, Any]:
    identity = require_survey_identity(
        source,
        wave,
        country_code,
        require_country=True,
    )
    roots: dict[str, Path | None] = {}
    for layer, directory in {
        "v551": "v551",
        "v551j": "v551j",
        "v552": "v552",
        "v552j": "v552j",
        "v553": "v553",
        "v554": "v554",
        "v555": "v555",
        "v556": "v556",
        "v557": "v557",
        "v558": "v558",
        "v558_plus": "v558_plus",
        "thin": "v5_thin_end_to_end",
        "v5_app_handoff": "v5_app_handoff",
    }.items():
        resolved = latest_run_root_for_wave(
            repo_root / "data" / "ddm_repository_copy" / directory / "runs",
            identity.source,
            identity.canonical_wave,
            identity.country_code,
        )
        roots[layer] = Path(resolved) if resolved else None

    readiness_paths = {
        "v551": "",
        "v551j": "manifest/v551j_readiness_report.json",
        "v552j": "manifest/v552j_readiness_report.json",
        "v552": "manifest/v552_readiness_report.json",
        "v553": "manifest/v553_temporal_readiness_report.json",
        "v554": "manifest/v554_readiness_report.json",
        "v555": "manifest/v555_readiness_report.json",
        "v556": "manifest/v556_readiness_report.json",
        "v557": "manifest/v557_readiness_report.json",
        "v558": "manifest/v558_runtime_input_gate_report.json",
        "v558_plus": "manifest/v558_plus_readiness_report.json",
        "thin": "manifest/v5_thin_end_to_end_readiness_report.json",
        "v5_app_handoff": "manifest/v5_app_handoff_readiness_report.json",
    }

    readiness = {}
    for layer, root in roots.items():
        if not root:
            readiness[layer] = ""
        elif layer == "v551":
            readiness[layer] = "present"
        else:
            readiness[layer] = _status_from_readiness(root, readiness_paths[layer])

    layer_outputs = {}
    for layer in ("v552j", "v553", "v554", "v555", "v556", "v557", "v558", "v5_app_handoff"):
        layer_outputs[layer] = {
            "required_upstream_artifacts": list(LAYER_REQUIREMENTS.get(layer, {}).get("required_upstream_artifacts", [])),
            "required_upstream_authority": list(LAYER_REQUIREMENTS.get(layer, {}).get("required_upstream_authority", [])),
            "downstream_outputs_expected": list(LAYER_REQUIREMENTS.get(layer, {}).get("downstream_outputs_expected", [])),
        }

    thin_root = roots["thin"]
    thin_readiness = _read_json(thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json") if thin_root else {}
    v558_plus_root = roots["v558_plus"]
    v558_plus_readiness = _read_json(v558_plus_root / "manifest" / "v558_plus_readiness_report.json") if v558_plus_root else {}
    app_handoff_root = roots["v5_app_handoff"]
    app_handoff_readiness = _read_json(app_handoff_root / "manifest" / "v5_app_handoff_readiness_report.json") if app_handoff_root else {}

    return {
        "source": identity.source,
        "country_code": identity.country_code,
        "wave": identity.canonical_wave,
        "latest_roots": {layer: str(path) if path else "" for layer, path in roots.items()},
        "latest_readiness_status": readiness,
        "v558_plus_status": v558_plus_readiness.get("status", ""),
        "thin_status": thin_readiness.get("final_status", thin_readiness.get("status", "")),
        "app_handoff_status": app_handoff_readiness.get("status", ""),
        "layer_outputs": layer_outputs,
        "buildable": bool(roots["v551"] and roots["v551j"] and roots["v552"] and roots["v552j"] and roots["v553"] and roots["v5_app_handoff"]),
        "runtime_boundary_ready": bool(v558_plus_readiness.get("status", "").startswith("V558_")),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# V5 Full Chain Status Report",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Waves: `{report['waves']}`",
        "",
        "## Wave Summary",
        "",
        "| Wave | Buildable | Thin Status | App Handoff | V558+ Status | V551J | V552J | V552 | V553 | V554 | V555 | V556 | V557 | V558 | V558+ |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for wave in report["wave_reports"]:
        status = wave["latest_readiness_status"]
        lines.append(
            "| {wave} | {buildable} | {thin} | {app_handoff} | {v558p} | {v551j} | {v552j} | {v552} | {v553} | {v554} | {v555} | {v556} | {v557} | {v558} | {v558p_root} |".format(
                wave=wave["wave"],
                buildable="yes" if wave["buildable"] else "no",
                thin=wave["thin_status"] or "missing",
                app_handoff=wave["app_handoff_status"] or "missing",
                v558p=wave["v558_plus_status"] or "missing",
                v551j=status.get("v551j", "") or "missing",
                v552j=status.get("v552j", "") or "missing",
                v552=status.get("v552", "") or "missing",
                v553=status.get("v553", "") or "missing",
                v554=status.get("v554", "") or "missing",
                v555=status.get("v555", "") or "missing",
                v556=status.get("v556", "") or "missing",
                v557=status.get("v557", "") or "missing",
                v558=status.get("v558", "") or "missing",
                v558p_root=status.get("v558_plus", "") or "missing",
            )
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `v558_plus` remains governance-only.",
            "- `thin` means the V551J→V557 thin end-to-end span.",
            "- `v5_app_handoff` is the app-facing review bundle that bridges thin + V558+ governance without enabling runtime.",
            "- `v558` means the runtime input gate and graft readiness layer.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a full-chain status report for the current V5 upper stack.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--waves", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    waves = args.waves.split()
    wave_reports = [
        _wave_status(repo_root, args.source, args.country_code, wave)
        for wave in waves
    ]
    paired_preflight = (
        build_paired_wave_preflight(
            repo_root,
            args.source,
            args.country_code,
            waves[0],
            waves[1],
        )
        if len(waves) >= 2
        else {}
    )
    report = {
        "repo_root": str(repo_root),
        "created_at": utc_now(),
        "source": wave_reports[0]["source"] if wave_reports else args.source,
        "country_code": (
            wave_reports[0]["country_code"]
            if wave_reports
            else args.country_code
        ),
        "waves": waves,
        "wave_reports": wave_reports,
        "paired_preflight": paired_preflight,
    }

    output_dir = Path(args.output_dir)
    _write_json(output_dir / "V5_FULL_CHAIN_STATUS_REPORT.json", report)
    _write_markdown(output_dir / "V5_FULL_CHAIN_STATUS_REPORT.md", report)
    print(output_dir / "V5_FULL_CHAIN_STATUS_REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
