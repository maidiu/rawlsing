#!/usr/bin/env python3
"""Compile canonical V552 v3 structural pressure from the V551 v3 producer bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    atomic_write_json,
    boundary_state_from_payload,
    inspect_artifact,
    publish_staged_directory,
    read_status_document,
    require_canonical_parquet,
    sha256_file,
    validate_machine_output_policy,
    verify_exact_identity,
)
from data.ddm_build_copy.ddm_v552_structural import (
    V551_COMPILER_VERSION,
    V551_SCHEMA_VERSION,
    V552_COMPILER_VERSION,
    V552_SCHEMA_VERSION,
    apply_v552_downstream_permission,
    build_v552_structural_outputs,
    validate_v552_v551_input_contract,
)
from data.ddm_build_copy.ddm_v552_validation import validate_v552_v2_1_4_outputs

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v552" / "runs"
V551_CANONICAL_FILES = {
    "directional_candidate_adjudication": "directional_candidate_adjudication.parquet",
    "relation_evidence_atoms": "relation_evidence_atoms.parquet",
    "directional_distribution_coverage": "directional_distribution_coverage.parquet",
}
AUDIT_ARTIFACTS = {
    "v552_intensity_representation_resolution_audit",
    "v552_pressure_observation_audit",
    "v552_directionality_coverage_audit",
    "v552_directionality_gap_surface",
    "v552_status_pressure_review_surface",
    "conditional_determinicity_status_audit",
}
MANIFEST_ARTIFACTS = {
    "v552_readiness_report",
    "v552_to_v552j_handoff_index",
    "v552_to_v552j_pressure_observation_handoff_index",
    "v552_artifact_authority_index",
    "v552_known_absence_register",
}


def _read_frame(path: Path) -> pd.DataFrame:
    require_canonical_parquet(path)
    return pd.read_parquet(path)


def _logical_hash(frame: pd.DataFrame) -> str:
    if frame.empty:
        return hashlib.sha256(b"").hexdigest()
    work = frame.copy()
    for column in work.columns:
        work[column] = work[column].fillna("").astype(str)
    work = work.sort_values(list(work.columns), kind="mergesort").reset_index(drop=True)
    return hashlib.sha256(work.to_csv(index=False).encode("utf-8")).hexdigest()


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


def _artifact_declarations(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("artifacts") or []
    return [dict(row) for row in raw if isinstance(row, dict)] if isinstance(raw, list) else []


def _manifest_parquet_declaration(payload: dict[str, Any], artifact_name: str, filename: str) -> dict[str, Any]:
    matches = []
    for row in _artifact_declarations(payload):
        name = _clean(row.get("artifact") or row.get("name"))
        path = _clean(row.get("path") or row.get("relative_path"))
        if (name == artifact_name or path == filename) and path.endswith(".parquet"):
            matches.append(row)
    if len(matches) != 1:
        raise RuntimeError(f"BLOCKED_V552_V551_ARTIFACT_DECLARATION_COUNT:{artifact_name}:{len(matches)}")
    declaration = matches[0]
    if _clean(declaration.get("path") or declaration.get("relative_path")) != filename:
        raise RuntimeError(f"BLOCKED_V552_V551_ARTIFACT_PATH_MISMATCH:{artifact_name}")
    if _clean(declaration.get("schema_version")) != V551_SCHEMA_VERSION:
        raise RuntimeError(f"BLOCKED_V552_V551_ARTIFACT_SCHEMA_MISMATCH:{artifact_name}")
    return declaration


def _verify_declared_artifact(base: Path, declaration: dict[str, Any]) -> Path:
    rel = _clean(declaration.get("path") or declaration.get("relative_path"))
    path = require_canonical_parquet(base / rel)
    inspection = inspect_artifact(path)
    if not inspection.exists or not inspection.readable:
        raise RuntimeError(f"BLOCKED_V552_V551_ARTIFACT_UNREADABLE:{rel}:{inspection.error}")
    declared_hash = _clean(declaration.get("artifact_file_sha256")).lower()
    if len(declared_hash) != 64 or inspection.artifact_file_sha256.lower() != declared_hash:
        raise RuntimeError(
            f"BLOCKED_V552_V551_ARTIFACT_HASH_MISMATCH:{rel}:expected={declared_hash}:actual={inspection.artifact_file_sha256.lower()}"
        )
    declared_rows = declaration.get("row_count")
    if declared_rows is not None and int(declared_rows) != int(inspection.row_count or 0):
        raise RuntimeError(f"BLOCKED_V552_V551_ARTIFACT_ROW_COUNT_MISMATCH:{rel}")
    return path


def _scope_from_manifest(payload: dict[str, Any]) -> dict[str, str]:
    scope_raw = payload.get("producer_scope_identity")
    scope = dict(scope_raw) if isinstance(scope_raw, dict) else {}
    source = _clean(scope.get("source") or payload.get("source"))
    wave = _clean(scope.get("canonical_wave") or scope.get("wave") or payload.get("canonical_wave") or payload.get("wave"))
    country = _clean(scope.get("country_code") or payload.get("country_code"))
    shard = _clean(scope.get("shard_id") or payload.get("shard_id"))
    if not source or not wave:
        raise RuntimeError("BLOCKED_V552_V551_SCOPE_IDENTITY_INCOMPLETE")
    if not country and not shard:
        raise RuntimeError("BLOCKED_V552_V551_SCOPE_GRAIN_MISSING")
    scope_kind = _clean(scope.get("scope_kind")) or ("shard" if shard else "country")
    if scope_kind == "country" and not country:
        raise RuntimeError("BLOCKED_V552_V551_COUNTRY_SCOPE_IDENTITY_MISSING")
    if scope_kind == "shard" and not shard:
        raise RuntimeError("BLOCKED_V552_V551_SHARD_SCOPE_IDENTITY_MISSING")
    return {"source": source, "wave": wave, "canonical_wave": wave, "country_code": country, "shard_id": shard, "scope_kind": scope_kind}


def _verify_frame_scope(frame: pd.DataFrame, *, run_id: str, scope: dict[str, str], label: str) -> None:
    if frame.empty:
        return
    expected = {"run_id": run_id, "source": scope["source"], "canonical_wave": scope["canonical_wave"]}
    if scope["country_code"]:
        expected["country_code"] = scope["country_code"]
    for column, want in expected.items():
        if column not in frame.columns:
            raise RuntimeError(f"BLOCKED_V552_{label.upper()}_SCOPE_COLUMN_MISSING:{column}")
        observed = {_clean(value) for value in frame[column].tolist() if _clean(value)}
        if observed != {want}:
            raise RuntimeError(f"BLOCKED_V552_{label.upper()}_SCOPE_MISMATCH:{column}:expected={want}:observed={sorted(observed)}")


def verify_v551_producer_bundle(
    *,
    run_id: str,
    manifest_path: Path,
    atoms_path: Path | None = None,
    coverage_path: Path | None = None,
    adjudication_path: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    document = read_status_document(manifest_path)
    if not document.exists or not document.readable:
        raise RuntimeError(f"BLOCKED_V552_V551_MANIFEST_UNREADABLE:{document.error}")
    payload = document.payload
    state = boundary_state_from_payload(payload)
    if state.run_integrity_status != "PASS":
        raise RuntimeError("BLOCKED_V552_V551_RUN_INTEGRITY_NOT_PASS")
    if _clean(payload.get("schema_version")) != V551_SCHEMA_VERSION or _clean(payload.get("compiler_version")) != V551_COMPILER_VERSION:
        raise RuntimeError("BLOCKED_V552_UNSUPPORTED_V551_CONTRACT_VERSION")
    if _clean((payload.get("contract_boundary") or {}).get("canonical_signed_projection_owner")) != "V551":
        raise RuntimeError("BLOCKED_V552_V551_PROJECTION_OWNER_CONTRACT")
    verify_exact_identity(payload, run_id=run_id)
    scope = _scope_from_manifest(payload)
    verify_exact_identity(
        payload,
        run_id=run_id,
        source=scope["source"],
        wave=scope["canonical_wave"],
        country_code=scope["country_code"],
        shard_id=scope["shard_id"],
    )
    base = manifest_path.parent
    declarations = {
        name: _manifest_parquet_declaration(payload, name, filename)
        for name, filename in V551_CANONICAL_FILES.items()
    }
    declared_paths = {name: _verify_declared_artifact(base, declaration) for name, declaration in declarations.items()}
    explicit = {
        "relation_evidence_atoms": atoms_path,
        "directional_distribution_coverage": coverage_path,
        "directional_candidate_adjudication": adjudication_path,
    }
    for name, path in explicit.items():
        if path is not None and path.resolve() != declared_paths[name].resolve():
            raise RuntimeError(f"BLOCKED_V552_EXPLICIT_V551_PATH_NOT_MANIFEST_DECLARED:{name}")
    atoms = _read_frame(declared_paths["relation_evidence_atoms"])
    coverage = _read_frame(declared_paths["directional_distribution_coverage"])
    adjudication = _read_frame(declared_paths["directional_candidate_adjudication"])
    for label, frame in (("atoms", atoms), ("coverage", coverage), ("adjudication", adjudication)):
        _verify_frame_scope(frame, run_id=run_id, scope=scope, label=label)
    contract = validate_v552_v551_input_contract(atoms, coverage, adjudication, run_id=run_id)
    if contract["status"] != "PASS":
        raise RuntimeError(contract["status"] + ":" + "|".join(contract["errors"]))
    if int(payload.get("atom_count", -1)) != len(atoms):
        raise RuntimeError("BLOCKED_V552_V551_MANIFEST_ATOM_COUNT_MISMATCH")
    if int(payload.get("distribution_coverage_rows", -1)) != len(coverage):
        raise RuntimeError("BLOCKED_V552_V551_MANIFEST_COVERAGE_COUNT_MISMATCH")
    if int(payload.get("candidate_count", -1)) != len(adjudication):
        raise RuntimeError("BLOCKED_V552_V551_MANIFEST_ADJUDICATION_COUNT_MISMATCH")
    if state.evidence_status == "NOT_APPLICABLE" and (len(atoms) or len(coverage) or len(adjudication)):
        raise RuntimeError("BLOCKED_V552_V551_NOT_APPLICABLE_WITH_NONEMPTY_CANONICAL_SURFACES")
    if state.evidence_status == "APPLICABLE_UNRESOLVED" and (len(atoms) != 0 or len(coverage) == 0 or len(adjudication) == 0):
        raise RuntimeError("BLOCKED_V552_V551_UNRESOLVED_STATE_SHAPE_MISMATCH")
    return atoms, coverage, adjudication, {
        "manifest": payload,
        "manifest_path": str(manifest_path),
        "manifest_file_sha256": sha256_file(manifest_path),
        "scope": scope,
        "state": {
            "run_integrity_status": state.run_integrity_status,
            "evidence_status": state.evidence_status,
            "downstream_permission_status": state.downstream_permission_status,
        },
        "artifact_paths": {name: str(path) for name, path in declared_paths.items()},
        "artifact_file_sha256": {name: _clean(declarations[name].get("artifact_file_sha256")) for name in declarations},
    }


def _artifact_subdir(name: str) -> str:
    if name in AUDIT_ARTIFACTS or name.endswith("_audit"):
        return "audits"
    if name in MANIFEST_ARTIFACTS:
        return "manifest"
    return "structural"


def _write_parquet(frame: pd.DataFrame, path: Path, name: str) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=False)
    return {
        "artifact": name,
        "path": str(path.relative_to(path.parents[1])),
        "artifact_kind": "canonical",
        "row_count": len(frame),
        "artifact_file_sha256": sha256_file(path),
        "logical_content_sha256": _logical_hash(frame),
        "schema_version": V552_SCHEMA_VERSION,
    }


def _write_csv(frame: pd.DataFrame, path: Path, name: str) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    return {
        "artifact": name,
        "path": str(path.relative_to(path.parents[1])),
        "artifact_kind": "diagnostic_csv",
        "row_count": len(frame),
        "artifact_file_sha256": sha256_file(path),
        "logical_content_sha256": _logical_hash(frame),
        "schema_version": V552_SCHEMA_VERSION,
    }


def compile_v552_run(
    *,
    run_id: str,
    v551_manifest_path: str | Path,
    atoms_path: str | Path | None = None,
    coverage_path: str | Path | None = None,
    adjudication_path: str | Path | None = None,
    conditional_determinicity_path: str | Path | None = None,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    strict_handoff: bool = True,
    write_parquet: bool = True,
    write_csv: bool = False,
) -> dict[str, Any]:
    validate_machine_output_policy(write_parquet=write_parquet, write_csv=write_csv)
    manifest_path = Path(v551_manifest_path)
    atoms, coverage, adjudication, producer = verify_v551_producer_bundle(
        run_id=run_id,
        manifest_path=manifest_path,
        atoms_path=Path(atoms_path) if atoms_path else None,
        coverage_path=Path(coverage_path) if coverage_path else None,
        adjudication_path=Path(adjudication_path) if adjudication_path else None,
    )
    conditional = None
    if conditional_determinicity_path:
        conditional_path = require_canonical_parquet(Path(conditional_determinicity_path))
        conditional = pd.read_parquet(conditional_path)
    outputs = build_v552_structural_outputs(
        atoms,
        coverage,
        adjudication,
        conditional,
        run_id=run_id,
    )
    if isinstance(outputs.get("v552_readiness_report"), pd.DataFrame) and not outputs["v552_readiness_report"].empty:
        outputs["v552_readiness_report"].loc[:, "producer_manifest_sha256"] = producer["manifest_file_sha256"]
        outputs["v552_readiness_report"].loc[:, "boundary_contract_version"] = PIPELINE_BOUNDARY_CONTRACT_VERSION
    apply_v552_downstream_permission(outputs, allow_downstream=strict_handoff)
    issues = validate_v552_v2_1_4_outputs(
        outputs,
        input_atoms=atoms,
        directional_coverage=coverage,
        directional_adjudication=adjudication,
        execution_mode="acceptance" if strict_handoff else "diagnostic",
        written_artifacts=None,
    )
    if issues:
        raise RuntimeError("BLOCKED_V552_OUTPUT_CONTRACT_INVALID:" + ";".join(issue.code for issue in issues))
    readiness = outputs["v552_readiness_report"].iloc[0].to_dict()
    readiness_integrity = _clean(readiness.get("run_integrity_status"))
    if readiness_integrity != "PASS":
        raise RuntimeError("BLOCKED_V552_INTERNAL_RUN_INTEGRITY")
    evidence_status = _clean(readiness.get("evidence_status"))
    permission_status = _clean(readiness.get("downstream_permission_status"))
    if not strict_handoff and permission_status == "ALLOW":
        raise RuntimeError("BLOCKED_V552_DIAGNOSTIC_MODE_PERMISSION_LEAK")

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    final_dir = root / run_id
    staging_dir = Path(tempfile.mkdtemp(prefix=f".{run_id}.v552-stage-", dir=str(root)))
    try:
        artifacts: list[dict[str, Any]] = []
        for name, frame in outputs.items():
            if name.startswith("_") or not isinstance(frame, pd.DataFrame):
                continue
            subdir = _artifact_subdir(name)
            artifacts.append(_write_parquet(frame, staging_dir / subdir / f"{name}.parquet", name))
            if write_csv:
                artifacts.append(_write_csv(frame, staging_dir / subdir / f"{name}.csv", name))
        manifest = {
            "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
            "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
            "producer_run_id": run_id,
            "run_id": run_id,
            "source": producer["scope"]["source"],
            "wave": producer["scope"]["wave"],
            "canonical_wave": producer["scope"]["canonical_wave"],
            "country_code": producer["scope"]["country_code"],
            "shard_id": producer["scope"]["shard_id"],
            "producer_scope_identity": producer["scope"],
            "schema_version": V552_SCHEMA_VERSION,
            "compiler_version": V552_COMPILER_VERSION,
            "run_integrity_status": "PASS",
            "evidence_status": evidence_status,
            "downstream_permission_status": permission_status,
            "execution_mode": "acceptance" if strict_handoff else "diagnostic",
            "artifacts": artifacts,
            "upstream_v551": {
                "manifest_path": producer["manifest_path"],
                "manifest_file_sha256": producer["manifest_file_sha256"],
                "schema_version": V551_SCHEMA_VERSION,
                "compiler_version": V551_COMPILER_VERSION,
                "run_integrity_status": producer["state"]["run_integrity_status"],
                "evidence_status": producer["state"]["evidence_status"],
                "downstream_permission_status": producer["state"]["downstream_permission_status"],
                "artifact_file_sha256": producer["artifact_file_sha256"],
            },
            "contract_boundary": {
                "canonical_signed_projection_owner": "V551",
                "v552_reinterprets_scale_geometry": False,
                "selected_surface_partiality_may_conditionally_normalize_only_when_adjudication_complete": True,
                "unresolved_directional_mass_may_be_renormalized": False,
                "valid_empty_is_run_failure": False,
                "measurement_evidence_independent_of_invocation_permission": True,
            },
        }
        atomic_write_json(staging_dir / "manifest.json", manifest)
        publish_staged_directory(staging_dir, final_dir)
        return manifest
    except Exception:
        if staging_dir.exists():
            shutil.rmtree(staging_dir, ignore_errors=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551-manifest-path")
    parser.add_argument("--atoms-path")
    parser.add_argument("--coverage-path")
    parser.add_argument("--adjudication-path")
    parser.add_argument("--conditional-determinicity-path")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--strict-handoff", dest="strict_handoff", action="store_true", default=True)
    parser.add_argument("--no-strict-handoff", dest="strict_handoff", action="store_false")
    parser.add_argument("--diagnostic-only", action="store_true")
    parser.add_argument("--write-parquet", dest="write_parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--write-csv", dest="write_csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    return parser.parse_args()


def _resolve_manifest_path(args: argparse.Namespace) -> Path:
    if args.v551_manifest_path:
        return Path(args.v551_manifest_path)
    if args.atoms_path:
        return Path(args.atoms_path).resolve().parent / "manifest.json"
    raise RuntimeError("BLOCKED_V552_V551_MANIFEST_PATH_REQUIRED")


def main() -> int:
    args = parse_args()
    manifest = compile_v552_run(
        run_id=args.run_id,
        v551_manifest_path=_resolve_manifest_path(args),
        atoms_path=args.atoms_path,
        coverage_path=args.coverage_path,
        adjudication_path=args.adjudication_path,
        conditional_determinicity_path=args.conditional_determinicity_path,
        output_root=args.output_root,
        strict_handoff=bool(args.strict_handoff and not args.diagnostic_only),
        write_parquet=args.write_parquet,
        write_csv=args.write_csv,
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
