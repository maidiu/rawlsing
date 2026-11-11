#!/usr/bin/env python3
"""Standalone V550-V552 extraction audit runner bound to V551 v3.0."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    boundary_state_from_payload,
    sha256_file,
)
from data.ddm_build_copy.v550_552_extraction_audit import (
    V551_CANONICAL_ARTIFACTS,
    V551_COMPILER_VERSION,
    V551_SCHEMA_VERSION,
    build_v550_552_extraction_audit_package,
)


@dataclass(frozen=True)
class ArtifactLoadResult:
    artifact_name: str
    path: Path
    frame: pd.DataFrame
    load_status: str
    error: str = ""
    artifact_file_sha256: str = ""
    expected_artifact_file_sha256: str = ""

    def diagnostic_row(self, *, stage: str) -> dict[str, Any]:
        return {
            "stage": stage,
            "artifact_name": self.artifact_name,
            "path": str(self.path),
            "load_status": self.load_status,
            "row_count": int(len(self.frame)),
            "artifact_file_sha256": self.artifact_file_sha256,
            "expected_artifact_file_sha256": self.expected_artifact_file_sha256,
            "error": self.error,
        }


def _load_parquet_result(
    path: Path,
    *,
    label: str = "",
    verbose: bool = False,
    expected_sha256: str = "",
    expected_row_count: int | None = None,
    expected_schema_version: str = "",
    expected_compiler_version: str = "",
) -> ArtifactLoadResult:
    artifact_name = label or path.stem
    if not path.exists():
        return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), "MISSING", "file missing", expected_artifact_file_sha256=expected_sha256)
    try:
        actual_sha256 = sha256_file(path)
    except Exception as exc:
        return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), "READ_ERROR", f"HASH_ERROR:{type(exc).__name__}:{exc}", expected_artifact_file_sha256=expected_sha256)
    if expected_sha256 and actual_sha256.lower() != expected_sha256.lower():
        return ArtifactLoadResult(
            artifact_name,
            path,
            pd.DataFrame(),
            "HASH_MISMATCH",
            f"expected={expected_sha256.lower()}:actual={actual_sha256.lower()}",
            actual_sha256,
            expected_sha256,
        )
    try:
        frame = pd.read_parquet(path)
    except Exception as exc:
        if verbose:
            print(f"  [{artifact_name}] error loading {path}: {exc}", flush=True)
        return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), "READ_ERROR", f"{type(exc).__name__}:{exc}", actual_sha256, expected_sha256)
    if expected_row_count is not None and len(frame) != expected_row_count:
        return ArtifactLoadResult(
            artifact_name,
            path,
            pd.DataFrame(),
            "ROW_COUNT_MISMATCH",
            f"expected={expected_row_count}:actual={len(frame)}",
            actual_sha256,
            expected_sha256,
        )
    if expected_schema_version:
        if "schema_version" not in frame.columns or (
            not frame.empty and not frame["schema_version"].fillna("").astype(str).eq(expected_schema_version).all()
        ):
            return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), "SCHEMA_MISMATCH", f"schema_version!={expected_schema_version}", actual_sha256, expected_sha256)
    if expected_compiler_version:
        if "compiler_version" not in frame.columns or (
            not frame.empty and not frame["compiler_version"].fillna("").astype(str).eq(expected_compiler_version).all()
        ):
            return ArtifactLoadResult(artifact_name, path, pd.DataFrame(), "SCHEMA_MISMATCH", f"compiler_version!={expected_compiler_version}", actual_sha256, expected_sha256)
    status = "VALID_EMPTY" if frame.empty else "LOADED"
    if verbose:
        print(f"  [{artifact_name}] {status.lower()} {len(frame)} rows from {path}", flush=True)
    return ArtifactLoadResult(artifact_name, path, frame, status, "", actual_sha256, expected_sha256)


def _load_json_result(path: Path, *, label: str = "", verbose: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    artifact_name = label or path.stem
    diagnostic = {
        "stage": "v551",
        "artifact_name": artifact_name,
        "path": str(path),
        "load_status": "MISSING",
        "row_count": None,
        "artifact_file_sha256": "",
        "expected_artifact_file_sha256": "",
        "error": "",
    }
    if not path.exists():
        diagnostic["error"] = "file missing"
        return {}, diagnostic
    try:
        diagnostic["artifact_file_sha256"] = sha256_file(path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("manifest root is not an object")
    except Exception as exc:
        if verbose:
            print(f"  [{artifact_name}] error loading {path}: {exc}", flush=True)
        diagnostic["load_status"] = "READ_ERROR"
        diagnostic["error"] = f"{type(exc).__name__}:{exc}"
        return {}, diagnostic
    diagnostic["load_status"] = "LOADED"
    diagnostic["row_count"] = 1
    return payload, diagnostic


def _manifest_identity_error(
    manifest: dict[str, Any],
    *,
    run_id: str,
    source: str,
    canonical_wave: str,
    country_code: str,
    shard_id: str,
) -> str:
    if str(manifest.get("producer_run_id") or manifest.get("run_id") or "") != run_id:
        return "run_id mismatch"
    if str(manifest.get("source") or "") != source:
        return "source mismatch"
    observed_wave = str(manifest.get("canonical_wave") or manifest.get("wave") or "")
    if observed_wave != canonical_wave:
        return "canonical_wave mismatch"
    scope = manifest.get("producer_scope_identity")
    if not isinstance(scope, dict):
        return "producer_scope_identity missing"
    scope_kind = str(scope.get("scope_kind") or "")
    if scope_kind == "country":
        if country_code and str(scope.get("country_code") or manifest.get("country_code") or "") != country_code:
            return "country_code mismatch"
    elif scope_kind == "shard":
        observed_shard = str(scope.get("shard_id") or manifest.get("shard_id") or "")
        if not observed_shard:
            return "shard_id missing"
        if shard_id and observed_shard != shard_id:
            return "shard_id mismatch"
    else:
        return f"unsupported scope_kind={scope_kind or '<missing>'}"
    return ""


def _artifact_declaration(manifest: dict[str, Any], artifact_name: str) -> dict[str, Any] | None:
    declarations = manifest.get("artifacts")
    if not isinstance(declarations, list):
        return None
    expected_path = f"{artifact_name}.parquet"
    for declaration in declarations:
        if not isinstance(declaration, dict):
            continue
        if declaration.get("artifact") == artifact_name and declaration.get("path") == expected_path:
            return declaration
    return None


def _load_v551_v3_run(
    run_dir: Path,
    *,
    run_id: str,
    source: str,
    canonical_wave: str,
    country_code: str = "",
    shard_id: str = "",
    verbose: bool = False,
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    manifest, manifest_diag = _load_json_result(run_dir / "manifest.json", label="manifest", verbose=verbose)
    diagnostics = [manifest_diag]
    outputs = {name: pd.DataFrame() for name in V551_CANONICAL_ARTIFACTS}
    if manifest_diag["load_status"] != "LOADED":
        return manifest, outputs, diagnostics

    contract_errors: list[str] = []
    try:
        boundary_state_from_payload(manifest)
    except Exception as exc:
        contract_errors.append(f"boundary_state:{type(exc).__name__}:{exc}")
    if str(manifest.get("contract_version") or manifest.get("boundary_contract_version") or "") != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        contract_errors.append("contract_version mismatch")
    if str(manifest.get("schema_version") or "") != V551_SCHEMA_VERSION:
        contract_errors.append("schema_version mismatch")
    if str(manifest.get("compiler_version") or "") != V551_COMPILER_VERSION:
        contract_errors.append("compiler_version mismatch")
    if tuple(manifest.get("canonical_artifact_names") or ()) != V551_CANONICAL_ARTIFACTS:
        contract_errors.append("canonical_artifact_names mismatch")
    identity_error = _manifest_identity_error(
        manifest,
        run_id=run_id,
        source=source,
        canonical_wave=canonical_wave,
        country_code=country_code,
        shard_id=shard_id,
    )
    if identity_error:
        contract_errors.append(identity_error)
    if contract_errors:
        diagnostics[0]["load_status"] = "IDENTITY_ERROR" if identity_error else "CONTRACT_ERROR"
        diagnostics[0]["error"] = "|".join(contract_errors)
        return manifest, outputs, diagnostics

    for artifact_name in V551_CANONICAL_ARTIFACTS:
        declaration = _artifact_declaration(manifest, artifact_name)
        if declaration is None:
            diagnostics.append(
                {
                    "stage": "v551",
                    "artifact_name": artifact_name,
                    "path": str(run_dir / f"{artifact_name}.parquet"),
                    "load_status": "DECLARATION_ERROR",
                    "row_count": 0,
                    "artifact_file_sha256": "",
                    "expected_artifact_file_sha256": "",
                    "error": "canonical artifact declaration missing",
                }
            )
            continue
        expected_hash = str(declaration.get("artifact_file_sha256") or "").lower()
        logical_hash = str(declaration.get("logical_content_sha256") or "").lower()
        if not re.fullmatch(r"[0-9a-f]{64}", logical_hash):
            diagnostics.append(
                {
                    "stage": "v551",
                    "artifact_name": artifact_name,
                    "path": str(run_dir / f"{artifact_name}.parquet"),
                    "load_status": "DECLARATION_ERROR",
                    "row_count": 0,
                    "artifact_file_sha256": "",
                    "expected_artifact_file_sha256": expected_hash,
                    "error": "logical_content_sha256 missing or invalid",
                }
            )
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
            diagnostics.append(
                {
                    "stage": "v551",
                    "artifact_name": artifact_name,
                    "path": str(run_dir / f"{artifact_name}.parquet"),
                    "load_status": "DECLARATION_ERROR",
                    "row_count": 0,
                    "artifact_file_sha256": "",
                    "expected_artifact_file_sha256": expected_hash,
                    "error": "artifact_file_sha256 missing or invalid",
                }
            )
            continue
        if declaration.get("artifact_kind") != "canonical" or declaration.get("schema_version") != V551_SCHEMA_VERSION:
            diagnostics.append(
                {
                    "stage": "v551",
                    "artifact_name": artifact_name,
                    "path": str(run_dir / f"{artifact_name}.parquet"),
                    "load_status": "DECLARATION_ERROR",
                    "row_count": 0,
                    "artifact_file_sha256": "",
                    "expected_artifact_file_sha256": expected_hash,
                    "error": "artifact declaration kind/schema mismatch",
                }
            )
            continue
        try:
            expected_rows = int(declaration.get("row_count"))
        except (TypeError, ValueError):
            expected_rows = None
        result = _load_parquet_result(
            run_dir / f"{artifact_name}.parquet",
            label=artifact_name,
            verbose=verbose,
            expected_sha256=expected_hash,
            expected_row_count=expected_rows,
            expected_schema_version=V551_SCHEMA_VERSION,
            expected_compiler_version=V551_COMPILER_VERSION,
        )
        diagnostics.append(result.diagnostic_row(stage="v551"))
        outputs[artifact_name] = result.frame
    return manifest, outputs, diagnostics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-stage extraction audit for V550/V551/V552/V550J.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--canonical-wave", default=None, help="Defaults to --wave if not set.")
    parser.add_argument("--country-code", default=None, help="Defaults to --country if not set.")
    parser.add_argument("--country", default=None, help="Alias for --country-code.")
    parser.add_argument("--shard-id", default="")
    parser.add_argument("--v550-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v550"))
    parser.add_argument("--v551-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v551" / "runs"))
    parser.add_argument("--v552-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v552" / "runs"))
    parser.add_argument("--v550j-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v550j"))
    parser.add_argument("--output-root", default=None, help="Defaults to <v550-root>/extraction_audit if not set.")
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    run_id = args.run_id
    source = args.source
    wave = args.wave
    canonical_wave = args.canonical_wave or wave
    country_code = args.country_code or args.country or ""
    v550_root = Path(args.v550_root)
    v551_root = Path(args.v551_root)
    v552_root = Path(args.v552_root)
    v550j_root = Path(args.v550j_root)
    output_root = Path(args.output_root or str(v550_root / "extraction_audit"))
    out_dir = output_root / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    load_diagnostics: list[dict[str, Any]] = []

    def load_optional(stage: str, path: Path, name: str) -> pd.DataFrame:
        result = _load_parquet_result(path, label=f"{stage}_{name}", verbose=args.verbose)
        load_diagnostics.append(result.diagnostic_row(stage=stage))
        return result.frame

    v550_run_dir = v550_root / "runs" / run_id
    v550_outputs = {
        "question_carry_forward_summary": load_optional("v550", v550_run_dir / "core" / "question_carry_forward_summary.parquet", "question_carry_forward_summary"),
        "question_response_attitude_cloud": load_optional("v550", v550_run_dir / "clouds" / "question_response_attitude_cloud.parquet", "question_response_attitude_cloud"),
    }

    v551_manifest, v551_outputs, v551_diagnostics = _load_v551_v3_run(
        v551_root / run_id,
        run_id=run_id,
        source=source,
        canonical_wave=canonical_wave,
        country_code=country_code,
        shard_id=args.shard_id,
        verbose=args.verbose,
    )
    load_diagnostics.extend(v551_diagnostics)

    v552_run_dir = v552_root / run_id
    v552_outputs = {
        "v552_directionality_gap_surface": load_optional("v552", v552_run_dir / "audits" / "v552_directionality_gap_surface.parquet", "directionality_gap_surface"),
        "v552_status_pressure_review_surface": load_optional("v552", v552_run_dir / "audits" / "v552_status_pressure_review_surface.parquet", "status_pressure_review_surface"),
    }
    shard = args.shard_id or f"{source}__{canonical_wave}"
    v550j_pattern_dir = v550j_root / "runs" / run_id / shard / "joint_patterns"
    v550j_outputs = {
        "joint_pattern_association_review_surface": load_optional("v550j", v550j_pattern_dir / "joint_pattern_association_review_surface.parquet", "joint_pattern_association_review_surface")
    }

    load_audit = pd.DataFrame(load_diagnostics)
    package = build_v550_552_extraction_audit_package(
        run_id=run_id,
        source=source,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
        v550_outputs=v550_outputs,
        v551_outputs=v551_outputs,
        v552_outputs=v552_outputs,
        v550j_outputs=v550j_outputs,
        v551_manifest=v551_manifest,
        artifact_load_diagnostics=load_audit,
    )

    written: list[dict[str, Any]] = []
    for table_name, frame in package.items():
        if frame is None or frame.empty:
            continue
        parquet_path = out_dir / f"{table_name}.parquet"
        frame.to_parquet(parquet_path, index=False)
        csv_path = out_dir / f"{table_name}.csv"
        if args.write_csv:
            frame.to_csv(csv_path, index=False)
        written.append({
            "table_name": table_name,
            "rows": int(len(frame)),
            "parquet": str(parquet_path),
            "csv": str(csv_path) if args.write_csv else "",
        })

    elapsed = time.monotonic() - started
    readiness = package["readiness_report"].iloc[0].to_dict()
    state_keys = (
        "producer_contract_version",
        "producer_schema_version",
        "producer_run_integrity_status",
        "producer_evidence_status",
        "producer_downstream_permission_status",
        "run_integrity_status",
        "evidence_status",
        "downstream_permission_status",
        "candidate_count",
        "directionally_applicable_count",
        "promotable_count",
        "nonpromotable_count",
        "repair_debt_count",
        "not_applicable_count",
        "relation_evidence_atom_count",
        "observed_zero_atom_count",
        "coverage_status",
        "coverage_conservation_status",
        "audit_contract_status",
        "overall_status",
    )
    state = {key: readiness.get(key) for key in state_keys}
    audit_manifest = {
        "run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        **state,
        "written_tables": written,
        "elapsed_seconds": round(elapsed, 2),
    }
    (out_dir / "v550_552_extraction_audit_manifest.json").write_text(
        json.dumps(audit_manifest, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    profile = {
        "run_id": run_id,
        "compiler_name": "v550_552_extraction_audit",
        "elapsed_seconds": round(elapsed, 2),
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "output_tables": [entry["table_name"] for entry in written],
        "total_output_rows": int(sum(entry["rows"] for entry in written)),
    }
    (out_dir / "v550_552_extraction_audit_performance_profile.json").write_text(
        json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    if args.verbose:
        print(json.dumps(audit_manifest, indent=2, ensure_ascii=False, default=str), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
