#!/usr/bin/env python3
"""Compile a producer-bound paired-wave preflight for the V552→V557 path."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError, inspect_artifact, read_status_document
from data.ddm_build_copy.ddm_pipeline_final_contracts import (
    state_token,
    verify_v551j_producer_manifest,
    verify_v552_producer_manifest,
    verify_v552j_producer_manifest,
)
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity
from data.ddm_build_copy.ddm_v553_repo_discovery import latest_run_root_for_wave


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _manifest_scope_hint(path: Path, *, source: str, wave: str, country_code: str) -> dict[str, str]:
    document = read_status_document(path)
    if not document.exists or not document.readable:
        raise BoundaryContractError(f"PREFLIGHT_MANIFEST_UNREADABLE:{path}:{document.error}")
    payload = document.payload
    scope_raw = payload.get("producer_scope_identity")
    scope = dict(scope_raw) if isinstance(scope_raw, Mapping) else {}
    actual_source = _text(scope.get("source") or payload.get("source"))
    actual_wave = _text(scope.get("canonical_wave") or scope.get("wave") or payload.get("canonical_wave") or payload.get("wave"))
    actual_country = _text(scope.get("country_code") or payload.get("country_code"))
    actual_shard = _text(scope.get("shard_id") or payload.get("shard_id"))
    if actual_source != source or actual_wave != wave:
        raise BoundaryContractError(
            f"PREFLIGHT_SCOPE_MISMATCH:expected={source}/{wave}:actual={actual_source}/{actual_wave}"
        )
    if actual_country and actual_country != country_code:
        raise BoundaryContractError(
            f"PREFLIGHT_COUNTRY_MISMATCH:expected={country_code}:actual={actual_country}"
        )
    if not actual_country and not actual_shard:
        raise BoundaryContractError("PREFLIGHT_COUNTRY_OR_SHARD_IDENTITY_MISSING")
    return {"country_code": actual_country, "shard_id": actual_shard}


def _declared_artifact(
    manifest_path: Path,
    payload: Mapping[str, Any],
    *,
    artifact_name: str,
) -> dict[str, Any]:
    matches = []
    for row in payload.get("artifacts") or []:
        if not isinstance(row, Mapping):
            continue
        name = _text(row.get("artifact") or row.get("name"))
        rel = _text(row.get("path") or row.get("relative_path"))
        if name == artifact_name:
            matches.append((dict(row), rel))
    canonical = [(row, rel) for row, rel in matches if rel.endswith(".parquet") and _text(row.get("artifact_kind")) == "canonical"]
    if len(canonical) != 1:
        raise BoundaryContractError(
            f"V552_PREFLIGHT_CANONICAL_DECLARATION_COUNT:{artifact_name}:{len(canonical)}"
        )
    row, rel = canonical[0]
    path = (manifest_path.parent / rel).resolve()
    inspected = inspect_artifact(path)
    if not inspected.exists or not inspected.readable:
        raise BoundaryContractError(f"V552_PREFLIGHT_ARTIFACT_UNREADABLE:{artifact_name}:{inspected.error}")
    declared_hash = _text(row.get("artifact_file_sha256")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
        raise BoundaryContractError(f"V552_PREFLIGHT_ARTIFACT_HASH_INVALID:{artifact_name}")
    if inspected.artifact_file_sha256.lower() != declared_hash:
        raise BoundaryContractError(f"V552_PREFLIGHT_ARTIFACT_HASH_MISMATCH:{artifact_name}")
    if row.get("row_count") is not None and int(row["row_count"]) != int(inspected.row_count or 0):
        raise BoundaryContractError(f"V552_PREFLIGHT_ARTIFACT_ROW_COUNT_MISMATCH:{artifact_name}")
    return {
        "artifact": artifact_name,
        "path": str(path),
        "row_count": inspected.row_count,
        "artifact_file_sha256": inspected.artifact_file_sha256,
        "valid_empty": inspected.valid_empty,
    }


def _coherent_roots(
    repo_root: Path,
    source: str,
    wave: str,
    country_code: str,
) -> dict[str, Path | None]:
    identity = require_survey_identity(source, wave, country_code, require_country=True)
    v552j_latest = latest_run_root_for_wave(
        repo_root / "data" / "ddm_repository_copy" / "v552j" / "runs",
        identity.source,
        identity.canonical_wave,
        identity.country_code,
    )
    if not v552j_latest:
        return {"v551j": None, "v552": None, "v552j": None, "v553": None}
    v552j_root = Path(v552j_latest)
    run_id = v552j_root.name
    roots: dict[str, Path | None] = {
        "v551j": repo_root / "data" / "ddm_repository_copy" / "v551j" / "runs" / run_id,
        "v552": repo_root / "data" / "ddm_repository_copy" / "v552" / "runs" / run_id,
        "v552j": v552j_root,
    }
    v553 = latest_run_root_for_wave(
        repo_root / "data" / "ddm_repository_copy" / "v553" / "runs",
        identity.source,
        identity.canonical_wave,
        identity.country_code,
    )
    roots["v553"] = Path(v553) if v553 else None
    return roots


def _wave_report(repo_root: Path, source: str, wave: str, country_code: str) -> dict[str, Any]:
    identity = require_survey_identity(source, wave, country_code, require_country=True)
    roots = _coherent_roots(repo_root, identity.source, identity.canonical_wave, identity.country_code)
    missing: list[str] = []
    failures: list[str] = []
    present: list[str] = []
    contracts: dict[str, Any] = {}

    v552j_root = roots.get("v552j")
    if v552j_root is None:
        missing.append("v552j:coherent_run_root")
        return {
            "source": identity.source,
            "country_code": identity.country_code,
            "wave": identity.canonical_wave,
            "run_id": "",
            "status": "blocked",
            "latest_roots": {layer: "" for layer in ("v551j", "v552", "v552j", "v553")},
            "producer_contracts": {},
            "present_artifacts": [],
            "missing_artifacts": missing,
            "contract_failures": failures,
            "comparison_ready": False,
        }
    run_id = v552j_root.name
    v551j_root = roots["v551j"]
    v552_root = roots["v552"]
    assert v551j_root is not None and v552_root is not None
    v551j_manifest = v551j_root / "manifest" / "manifest.json"
    v552_manifest = v552_root / "manifest.json"
    v552j_manifest = v552j_root / "manifest.json"

    try:
        v551j_scope = _manifest_scope_hint(
            v551j_manifest, source=identity.source, wave=identity.canonical_wave, country_code=identity.country_code
        )
        v551j = verify_v551j_producer_manifest(
            v551j_manifest,
            run_id=run_id,
            source=identity.source,
            wave=identity.canonical_wave,
            country_code=identity.country_code,
            shard_id=v551j_scope["shard_id"],
        )
        contracts["v551j"] = state_token(v551j)
        present.append("v551j:manifest/manifest.json")
    except BoundaryContractError as exc:
        failures.append(f"v551j:{exc}")

    try:
        v552_scope = _manifest_scope_hint(
            v552_manifest, source=identity.source, wave=identity.canonical_wave, country_code=identity.country_code
        )
        v552 = verify_v552_producer_manifest(
            v552_manifest,
            run_id=run_id,
            source=identity.source,
            wave=identity.canonical_wave,
            country_code=identity.country_code,
            shard_id=v552_scope["shard_id"],
        )
        contracts["v552"] = state_token(v552)
        present.append("v552:manifest.json")
        for artifact_name in ("v552_artifact_authority_index", "v552_known_absence_register"):
            artifact = _declared_artifact(v552_manifest, v552.manifest_payload, artifact_name=artifact_name)
            present.append(f"v552:{artifact['path']}")
    except BoundaryContractError as exc:
        failures.append(f"v552:{exc}")

    try:
        v552j_scope = _manifest_scope_hint(
            v552j_manifest, source=identity.source, wave=identity.canonical_wave, country_code=identity.country_code
        )
        v552j = verify_v552j_producer_manifest(
            v552j_manifest,
            run_id=run_id,
            source=identity.source,
            wave=identity.canonical_wave,
            country_code=identity.country_code,
            shard_id=v552j_scope["shard_id"],
            v551j_manifest_path=v551j_manifest,
            v552_manifest_path=v552_manifest,
        )
        contracts["v552j"] = state_token(v552j)
        present.append("v552j:manifest.json")
    except BoundaryContractError as exc:
        failures.append(f"v552j:{exc}")

    v553_required = (
        "manifest/v553_temporal_readiness_report.json",
        "manifest/v553_wave_harmonization_report.json",
    )
    v553_root = roots.get("v553")
    for rel in v553_required:
        token = f"v553:{rel}"
        if v553_root and (v553_root / rel).exists():
            present.append(token)
        else:
            missing.append(token)

    comparison_ready = not failures and not missing
    return {
        "source": identity.source,
        "country_code": identity.country_code,
        "wave": identity.canonical_wave,
        "run_id": run_id,
        "status": "ready" if comparison_ready else "blocked",
        "latest_roots": {layer: str(path) if path else "" for layer, path in roots.items()},
        "producer_contracts": contracts,
        "present_artifacts": present,
        "missing_artifacts": missing,
        "contract_failures": failures,
        "comparison_ready": comparison_ready,
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
    failures = sorted(set(wave_a_report["contract_failures"]) | set(wave_b_report["contract_failures"]))
    comparison_ready = not missing and not failures
    return {
        "repo_root": str(repo_root),
        "created_at": utc_now(),
        "source": wave_a_report["source"],
        "country_code": wave_a_report["country_code"],
        "wave_a": wave_a,
        "wave_b": wave_b,
        "status": "PAIRED_WAVE_READY" if comparison_ready else "PAIRED_WAVE_BLOCKED",
        "comparison_ready": comparison_ready,
        "missing_artifacts": missing,
        "contract_failures": failures,
        "legacy_v552_provenance_sidecar_required": False,
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
        "- V552 contract source: root `manifest.json` + producer-declared canonical artifact hashes",
        "- Legacy V552 provenance sidecar: **not required**",
        "",
        "## Wave Summary",
        "",
        "| Wave | Run ID | Status | Producer contracts | Missing | Contract failures |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for wave_report in report["wave_reports"]:
        lines.append(
            "| {wave} | {run_id} | {status} | {contracts} | {missing} | {failures} |".format(
                wave=wave_report["wave"],
                run_id=wave_report["run_id"],
                status=wave_report["status"],
                contracts=", ".join(f"{k}={v}" for k, v in sorted(wave_report["producer_contracts"].items())) or "none",
                missing=", ".join(wave_report["missing_artifacts"]) or "none",
                failures=", ".join(wave_report["contract_failures"]) or "none",
            )
        )
    lines.extend(["", "## Missing Artifacts", "", *([f"- {item}" for item in report["missing_artifacts"]] or ["- none"])])
    lines.extend(["", "## Contract Failures", "", *([f"- {item}" for item in report["contract_failures"]] or ["- none"])])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a producer-bound paired-wave preflight report.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    parser.add_argument("--wave-a", required=True)
    parser.add_argument("--wave-b", required=True)
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    args = parser.parse_args()
    report = build_paired_wave_preflight(args.repo_root, args.source, args.country_code, args.wave_a, args.wave_b)
    output_dir = Path(args.output_dir)
    _write_json(output_dir / "V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.json", report)
    _write_markdown(output_dir / "V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.md", report)
    print(output_dir / "V552_THROUGH_V557_PAIRED_WAVE_PREFLIGHT_REPORT.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
