#!/usr/bin/env python3
"""Compile V551 v3 canonical directional adjudication, atoms and coverage."""
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

from data.ddm_build_copy.ddm_v551_atoms import (
    V551_COMPILER_VERSION,
    V551_SCHEMA_VERSION,
    build_v551_directional_candidate_adjudication,
    build_v551_directional_distribution_coverage,
    build_v551_relation_evidence_atoms,
    validate_v551_adjudication_contract,
    validate_v551_atom_contract,
    validate_v551_bridge_input_contract,
    validate_v551_coverage_contract,
)
from data.ddm_build_copy.ddm_v551_directionality_expectation import (
    build_v551_directionality_stamp_audit,
    summarize_v551_directionality_stamp_coverage,
)

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v551" / "runs"
CANONICAL_ARTIFACTS = (
    "directional_candidate_adjudication",
    "relation_evidence_atoms",
    "directional_distribution_coverage",
)


def _boundary_api():
    """Load the frozen shared boundary/publication contract from W05.

    W04 does not duplicate or vendor W05-owned infrastructure. Until W05-A is
    merged into the integration branch, invoking publication fails closed.
    """
    try:
        from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
            PIPELINE_BOUNDARY_CONTRACT_VERSION,
            atomic_write_json,
            publish_staged_directory,
            validate_machine_output_policy,
        )
    except ModuleNotFoundError as exc:
        raise RuntimeError("BLOCKED_SHARED_PIPELINE_BOUNDARY_CONTRACT_MISSING") from exc
    return (
        PIPELINE_BOUNDARY_CONTRACT_VERSION,
        atomic_write_json,
        publish_staged_directory,
        validate_machine_output_policy,
    )


def _read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False) if path.suffix.lower() == ".csv" else pd.read_parquet(path)


def _logical_hash(df: pd.DataFrame) -> str:
    if df.empty:
        return hashlib.sha256(b"").hexdigest()
    work = df.copy()
    for column in work.columns:
        work[column] = work[column].fillna("").astype(str)
    work = work.sort_values(list(work.columns), kind="mergesort").reset_index(drop=True)
    return hashlib.sha256(work.to_csv(index=False).encode()).hexdigest()


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def _unique_nonblank(frame: pd.DataFrame, column: str) -> list[str]:
    if column not in frame.columns:
        return []
    return sorted({_clean(value) for value in frame[column].tolist() if _clean(value)})


def _producer_scope_identity(bridge: pd.DataFrame) -> dict[str, str]:
    sources = _unique_nonblank(bridge, "source")
    waves = _unique_nonblank(bridge, "canonical_wave")
    countries = _unique_nonblank(bridge, "country_code")
    shards = _unique_nonblank(bridge, "shard_id")
    if len(sources) != 1:
        raise RuntimeError(f"BLOCKED_V551_SOURCE_SCOPE_NOT_SINGULAR observed={sources}")
    if len(waves) != 1:
        raise RuntimeError(f"BLOCKED_V551_WAVE_SCOPE_NOT_SINGULAR observed={waves}")
    if len(shards) > 1:
        raise RuntimeError(f"BLOCKED_V551_SHARD_SCOPE_NOT_SINGULAR observed={shards}")
    if not shards and len(countries) != 1:
        raise RuntimeError(f"BLOCKED_V551_COUNTRY_SCOPE_NOT_SINGULAR observed={countries}")
    return {
        "source": sources[0],
        "wave": waves[0],
        "canonical_wave": waves[0],
        "country_code": countries[0] if len(countries) == 1 else "",
        "shard_id": shards[0] if shards else "",
        "scope_kind": "shard" if shards else "country",
    }


def _boundary_statuses(candidate_count: int, promotable_count: int) -> tuple[str, str, str, str]:
    if promotable_count > 0:
        return "PASS", "PRESENT", "ALLOW", "PROMOTABLE_EVIDENCE_PRESENT"
    if candidate_count > 0:
        return "PASS", "APPLICABLE_UNRESOLVED", "DENY", "APPLICABLE_REPAIR_DEBT_ONLY"
    return "PASS", "NOT_APPLICABLE", "NOT_APPLICABLE", "NO_APPLICABLE_DIRECTIONAL_EVIDENCE"


def _write_parquet(df: pd.DataFrame, path: Path, *, artifact_name: str) -> dict[str, Any]:
    df.to_parquet(path, index=False)
    return {
        "artifact": artifact_name,
        "path": path.name,
        "artifact_kind": "canonical",
        "row_count": len(df),
        "artifact_file_sha256": _file_hash(path),
        "logical_content_sha256": _logical_hash(df),
        "schema_version": V551_SCHEMA_VERSION,
    }


def _write_csv(df: pd.DataFrame, path: Path, *, artifact_name: str) -> dict[str, Any]:
    df.to_csv(path, index=False)
    return {
        "artifact": artifact_name,
        "path": path.name,
        "artifact_kind": "diagnostic_csv",
        "row_count": len(df),
        "artifact_file_sha256": _file_hash(path),
        "logical_content_sha256": _logical_hash(df),
        "schema_version": V551_SCHEMA_VERSION,
    }


def compile_v551_run(
    bridge: pd.DataFrame,
    *,
    run_id: str,
    bridge_path: str | Path,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    write_csv: bool = False,
) -> dict[str, Any]:
    (
        boundary_contract_version,
        atomic_write_json,
        publish_staged_directory,
        validate_machine_output_policy,
    ) = _boundary_api()
    validate_machine_output_policy(write_parquet=True, write_csv=write_csv)

    contract = validate_v551_bridge_input_contract(bridge)
    if contract["status"] != "PASS":
        raise RuntimeError(contract["status"] + ":" + ",".join(contract["missing_columns"]))
    run_ids = sorted({_clean(value) for value in bridge["run_id"].tolist() if _clean(value)})
    if len(run_ids) != 1 or run_ids[0] != run_id:
        raise RuntimeError(f"BLOCKED_V551_RUN_IDENTITY_MISMATCH expected={run_id} observed={run_ids}")
    scope = _producer_scope_identity(bridge)

    adjudication = build_v551_directional_candidate_adjudication(bridge)
    atoms, nonpromotable = build_v551_relation_evidence_atoms(bridge)
    coverage = build_v551_directional_distribution_coverage(adjudication)
    stamp = build_v551_directionality_stamp_audit(bridge)
    issues = (
        validate_v551_adjudication_contract(adjudication)
        + validate_v551_atom_contract(atoms)
        + validate_v551_coverage_contract(coverage)
    )
    if issues:
        raise RuntimeError("BLOCKED_V551_CONTRACT_INVALID:" + ";".join(issues))

    candidate_count = len(adjudication)
    promotable_count = int(adjudication["promotable"].map(bool).sum()) if not adjudication.empty else 0
    nonpromotable_count = candidate_count - promotable_count
    if candidate_count != promotable_count + nonpromotable_count:
        raise RuntimeError("BLOCKED_V551_CANDIDATE_CONSERVATION")

    integrity, evidence, permission, evidence_detail = _boundary_statuses(candidate_count, promotable_count)
    output_root_path = Path(output_root)
    output_root_path.mkdir(parents=True, exist_ok=True)
    final_dir = output_root_path / run_id
    staging_dir = Path(tempfile.mkdtemp(prefix=f".{run_id}.v551-stage-", dir=str(output_root_path)))
    bridge_path_obj = Path(bridge_path)
    try:
        artifacts: list[dict[str, Any]] = []
        frames = [
            (CANONICAL_ARTIFACTS[0], adjudication),
            (CANONICAL_ARTIFACTS[1], atoms),
            (CANONICAL_ARTIFACTS[2], coverage),
        ]
        for name, frame in frames:
            artifacts.append(_write_parquet(frame, staging_dir / f"{name}.parquet", artifact_name=name))
            if write_csv:
                artifacts.append(_write_csv(frame, staging_dir / f"{name}.csv", artifact_name=name))

        manifest = {
            "contract_version": boundary_contract_version,
            "boundary_contract_version": boundary_contract_version,
            "producer_run_id": run_id,
            "run_id": run_id,
            "source": scope["source"],
            "wave": scope["wave"],
            "canonical_wave": scope["canonical_wave"],
            "country_code": scope["country_code"],
            "shard_id": scope["shard_id"],
            "producer_scope_identity": scope,
            "schema_version": V551_SCHEMA_VERSION,
            "compiler_version": V551_COMPILER_VERSION,
            "run_integrity_status": integrity,
            "evidence_status": evidence,
            "downstream_permission_status": permission,
            "v551_evidence_detail": evidence_detail,
            "candidate_count": candidate_count,
            "promotable_candidate_count": promotable_count,
            "nonpromotable_candidate_count": nonpromotable_count,
            "atom_count": len(atoms),
            "distribution_coverage_rows": len(coverage),
            "directionality_stamp_coverage": summarize_v551_directionality_stamp_coverage(stamp),
            "artifacts": artifacts,
            "canonical_artifact_names": list(CANONICAL_ARTIFACTS),
            "nonpromotable_directional_candidate_ids": (
                nonpromotable["candidate_id"].tolist() if not nonpromotable.empty else []
            ),
            "contract_boundary": {
                "canonical_signed_projection_owner": "V551",
                "v552_pressure_decisions_present": False,
                "auxiliary_semantic_inputs_rehashed_by_v551": False,
            },
            "producer_bridge_path": str(bridge_path_obj),
            "producer_bridge_file_sha256": _file_hash(bridge_path_obj),
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
    parser.add_argument("--bridge-path", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--write-csv", action="store_true")
    parser.add_argument("--v551-compile-mode", choices=("canonical",), default="canonical")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bridge_path = Path(args.bridge_path)
    bridge = _read(bridge_path)
    manifest = compile_v551_run(
        bridge,
        run_id=args.run_id,
        bridge_path=bridge_path,
        output_root=args.output_root,
        write_csv=args.write_csv,
    )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
