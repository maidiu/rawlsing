#!/usr/bin/env python3
"""Paired-wave preflight for the exact integrated V550→V552J runtime path.

This W05-B preflight does not inspect or activate V553+.  It resolves each wave
through the W01 UID catalog, invokes the same manifest-based lineage resolver
used by replay, and validates the exact compiler paths used by the supported
smoke runner.
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

from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity
from data.ddm_build_copy.resolve_pipeline_lineage import resolve_stage_roots
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import (
    RuntimeConfig,
    runtime_compiler_paths,
)


def _stage_value(stages: dict[str, Any], stage: str, field: str, default: Any = "") -> Any:
    value = stages.get(stage)
    return getattr(value, field, default) if value is not None else default


def _wave_report(repo: Path, source: str, wave: str, country_code: str) -> dict[str, Any]:
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    stages = resolve_stage_roots(repo, identity.canonical_display_source, identity.canonical_display_wave)
    stage_rows = {
        name: {
            "root": _stage_value(stages, name, "root"),
            "usable": bool(_stage_value(stages, name, "usable", False)),
            "status": _stage_value(stages, name, "status"),
            "reason": _stage_value(stages, name, "reason"),
            "identity": dict((_stage_value(stages, name, "metrics", {}) or {}).get("identity") or {}),
        }
        for name in ("v550", "v550j", "v551", "v551j", "v552", "v552j")
    }
    base_ready = all(stage_rows[name]["usable"] for name in ("v550", "v551", "v552"))
    j_traversed = all(stage_rows[name]["usable"] for name in ("v550j", "v551j", "v552j"))
    full_ready = base_ready and j_traversed
    uid_mismatches = [
        name
        for name, row in stage_rows.items()
        if row["usable"]
        and (
            row["identity"].get("source_family_uid") != identity.source_family_uid
            or row["identity"].get("wave_uid") != identity.wave_uid
        )
    ]
    country_mismatches = [
        name
        for name, row in stage_rows.items()
        if row["usable"]
        and row["identity"].get("country_code")
        and row["identity"].get("country_code") != country_code
    ]
    if uid_mismatches or country_mismatches:
        full_ready = False
    return {
        "source": identity.canonical_display_source,
        "wave": identity.canonical_display_wave,
        "country_code": country_code,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "run_id": (stages["v550"].metrics or {}).get("run_id", "") if stages["v550"].usable else "",
        "shard_id": (stages["v550"].metrics or {}).get("shard_id", "") if stages["v550"].usable else "",
        "base_spine_ready": base_ready,
        "j_branch_traversed": j_traversed,
        "full_v550_to_v552j_ready": full_ready,
        "uid_mismatch_stages": uid_mismatches,
        "country_mismatch_stages": country_mismatches,
        "stages": stage_rows,
    }


def build_paired_wave_preflight(
    repo_root: str | Path,
    source: str,
    country_code: str,
    wave_a: str,
    wave_b: str,
) -> dict[str, Any]:
    repo = Path(repo_root)
    identity_a = resolve_source_wave_identity(source, wave_a, require_closed_35=True)
    identity_b = resolve_source_wave_identity(source, wave_b, require_closed_35=True)
    if identity_a.source_family_uid != identity_b.source_family_uid:
        raise ValueError(
            "paired-wave preflight requires one governed source family:"
            f"{identity_a.source_family_uid}!={identity_b.source_family_uid}"
        )

    runtime = RuntimeConfig(repo_root=repo)
    compiler_paths = runtime_compiler_paths(runtime)
    compiler_checks = {
        stage: {"path": str(path), "exists": path.exists()}
        for stage, path in compiler_paths.items()
    }
    missing_compilers = [
        f"{stage}:{row['path']}" for stage, row in compiler_checks.items() if not row["exists"]
    ]

    reports = [
        _wave_report(repo, identity_a.canonical_display_source, identity_a.canonical_display_wave, country_code),
        _wave_report(repo, identity_b.canonical_display_source, identity_b.canonical_display_wave, country_code),
    ]
    full_ready = not missing_compilers and all(row["full_v550_to_v552j_ready"] for row in reports)
    base_ready = all(row["base_spine_ready"] for row in reports)
    j_traversed = all(row["j_branch_traversed"] for row in reports)
    return {
        "repo_root": str(repo),
        "source": identity_a.canonical_display_source,
        "source_family_uid": identity_a.source_family_uid,
        "country_code": country_code,
        "wave_a": identity_a.canonical_display_wave,
        "wave_a_uid": identity_a.wave_uid,
        "wave_b": identity_b.canonical_display_wave,
        "wave_b_uid": identity_b.wave_uid,
        "runtime_path": ["v550", "v550j", "v551", "v551j", "v552", "v552j"],
        "base_spine": ["v550", "v551", "v552"],
        "j_branch": ["v550j", "v551j", "v552j"],
        "runtime_compilers": compiler_checks,
        "missing_runtime_compilers": missing_compilers,
        "base_spine_ready": base_ready,
        "j_branch_traversed": j_traversed,
        "comparison_ready": full_ready,
        "status": "PAIRED_WAVE_READY_V550_TO_V552J" if full_ready else "PAIRED_WAVE_BLOCKED_V550_TO_V552J",
        "wave_reports": reports,
        "v553_plus_checked": False,
        "v553_plus_activation_claimed": False,
    }


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# V550→V552J Paired-Wave Preflight",
        "",
        f"- Source: `{report['source']}`",
        f"- Source UID: `{report['source_family_uid']}`",
        f"- Wave A: `{report['wave_a']}` / `{report['wave_a_uid']}`",
        f"- Wave B: `{report['wave_b']}` / `{report['wave_b_uid']}`",
        f"- Base spine ready: `{report['base_spine_ready']}`",
        f"- J branch traversed for both waves: `{report['j_branch_traversed']}`",
        f"- Full comparison ready: `{report['comparison_ready']}`",
        f"- Status: `{report['status']}`",
        "",
        "This preflight stops at V552J. It performs no V553+ discovery or activation.",
        "",
        "## Runtime compilers",
        "",
    ]
    for stage, row in report["runtime_compilers"].items():
        lines.append(f"- `{stage}`: `{row['path']}` — {'present' if row['exists'] else 'MISSING'}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="V550→V552J paired-wave UID preflight")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--wave-a", required=True)
    parser.add_argument("--wave-b", required=True)
    parser.add_argument("--output-dir", default=str(ROOT / "docs/architecture_control/reports"))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_paired_wave_preflight(
        args.repo_root,
        args.source,
        args.country_code,
        args.wave_a,
        args.wave_b,
    )
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "V550_THROUGH_V552J_PAIRED_WAVE_PREFLIGHT_REPORT.json"
    md_path = output / "V550_THROUGH_V552J_PAIRED_WAVE_PREFLIGHT_REPORT.md"
    json_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    _write_markdown(md_path, report)
    print(md_path)
    return 0 if report["comparison_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
