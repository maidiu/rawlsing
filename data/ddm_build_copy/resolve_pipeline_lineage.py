#!/usr/bin/env python3
"""W05 lineage-integrity shim over the preserved integration resolver.

W05-B wires the merged V551 v3.0 producer contract without inventing later
V551J/V552/V552J semantics.  Legacy stages remain behind the W05-A adapters
until their producer hooks merge.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy import resolve_pipeline_lineage_impl as _impl
from data.ddm_build_copy.ddm_pipeline_boundary_consumer import verify_v551_v3_producer_manifest
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    boundary_state_from_payload,
    inspect_artifact,
    read_status_document,
    verify_external_dependency_ledger,
)

for _name in dir(_impl):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_impl, _name)

_ORIGINAL_RESOLVE_STAGE_ROOTS = _impl.resolve_stage_roots
StageResolution = _impl.StageResolution
_NO_LEDGER = Path("__RAWLSING_NO_EXTERNAL_DEPENDENCY_LEDGER__")
_LEDGER_SHA = ""
DEFAULT_DEPENDENCY_LEDGER = None


def _load_dependency_ledger(path: Path | None, expected_sha256: str = ""):
    if path is None or Path(path) == _NO_LEDGER:
        return None
    return verify_external_dependency_ledger(path, expected_sha256 or _LEDGER_SHA)


def _validate_root(
    root: Path,
    *,
    stage: str,
    required_files: tuple[str, ...],
    required_nonempty_files: tuple[str, ...] = (),
    status_paths: tuple[str, ...] = (),
    ready_key_names: tuple[str, ...] = (),
    **_kwargs: Any,
) -> StageResolution:
    """Legacy-stage adapter retained until those stages publish typed manifests."""
    if not root.is_dir():
        return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"missing exact run root: {root}")
    metrics: dict[str, Any] = {}
    for rel in required_files:
        artifact = inspect_artifact(root / rel)
        if not artifact.exists:
            return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"missing required file: {rel}")
        if not artifact.readable:
            return StageResolution(
                stage,
                "",
                False,
                "BLOCKED_OR_MISSING",
                f"unreadable required file: {rel}: {artifact.error}",
            )
        metrics[rel] = {
            "row_count": artifact.row_count,
            "artifact_file_sha256": artifact.artifact_file_sha256,
            "valid_empty": artifact.valid_empty,
        }
    for rel in required_nonempty_files:
        artifact = inspect_artifact(root / rel)
        if not artifact.exists or not artifact.readable:
            return StageResolution(
                stage,
                "",
                False,
                "BLOCKED_OR_MISSING",
                f"unreadable required evidence: {rel}: {artifact.error}",
            )
        if artifact.row_count is not None and artifact.row_count <= 0:
            return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"empty required evidence: {rel}")
    failures: list[str] = []
    for rel in status_paths:
        document = read_status_document(root / rel)
        if not document.exists:
            failures.append(f"missing:{rel}")
            continue
        if not document.readable:
            failures.append(f"unreadable:{rel}:{document.error}")
            continue
        try:
            state = boundary_state_from_payload(document.payload, ready_key_names)
        except BoundaryContractError as exc:
            failures.append(f"invalid:{rel}:{exc}")
            continue
        status = state.source or "/".join(
            (state.run_integrity_status, state.evidence_status, state.downstream_permission_status)
        )
        if not state.permits_downstream:
            return StageResolution(
                stage,
                "",
                False,
                status,
                f"producer boundary does not permit downstream: {rel}",
                metrics,
            )
        return StageResolution(stage, str(root), True, status, metrics=metrics)
    return StageResolution(
        stage,
        "",
        False,
        "BLOCKED_OR_MISSING",
        "required readiness/integrity unverifiable: " + ";".join(failures),
        metrics,
    )


def _latest_usable_candidate(
    base: Path,
    pattern: str,
    *,
    stage: str,
    required_files: tuple[str, ...],
    required_nonempty_files: tuple[str, ...] = (),
    status_paths: tuple[str, ...] = (),
    ready_key_names: tuple[str, ...] = (),
    **_kwargs: Any,
) -> StageResolution:
    best_reason = f"no candidate matched {pattern}"
    for _, _, root in _impl._rank_candidates(base, _impl._candidate_dirs(base, pattern)):
        result = _validate_root(
            root,
            stage=stage,
            required_files=required_files,
            required_nonempty_files=required_nonempty_files,
            status_paths=status_paths,
            ready_key_names=ready_key_names,
        )
        if result.usable:
            return result
        best_reason = result.reason
    return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", best_reason)


def _parquet_row_count(path: Path) -> int:
    artifact = inspect_artifact(path)
    if not artifact.exists:
        return 0
    if not artifact.readable:
        raise BoundaryContractError(f"PARQUET_UNREADABLE:{path}:{artifact.error}")
    return int(artifact.row_count or 0)


def _stage_artifact_rows(path: Path) -> int:
    artifact = inspect_artifact(path)
    if not artifact.exists:
        return 0
    if not artifact.readable:
        raise BoundaryContractError(f"ARTIFACT_UNREADABLE:{path}:{artifact.error}")
    return int(artifact.row_count if artifact.row_count is not None else 1)


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


def _unique(frame: pd.DataFrame, *columns: str) -> list[str]:
    for column in columns:
        if column not in frame.columns:
            continue
        values = sorted({_clean(value) for value in frame[column].tolist() if _clean(value)})
        if values:
            return values
    return []


def _v551_expected_identity(v550_root: Path) -> dict[str, str]:
    """Read the exact V550 bridge that V551 v3 consumes and derive its scope."""
    bridge_path = v550_root / "bridge" / "v551_bridge_index.parquet"
    artifact = inspect_artifact(bridge_path)
    if not artifact.exists:
        raise BoundaryContractError(f"V551_BRIDGE_MISSING:{bridge_path}")
    if not artifact.readable:
        raise BoundaryContractError(f"V551_BRIDGE_UNREADABLE:{bridge_path}:{artifact.error}")
    try:
        bridge = pd.read_parquet(bridge_path)
    except Exception as exc:
        raise BoundaryContractError(f"V551_BRIDGE_UNREADABLE:{bridge_path}:{type(exc).__name__}:{exc}") from exc
    run_ids = _unique(bridge, "run_id")
    sources = _unique(bridge, "source", "source_family")
    waves = _unique(bridge, "canonical_wave", "wave")
    countries = _unique(bridge, "country_code")
    shards = _unique(bridge, "shard_id")
    expected_run_id = v550_root.parent.name
    if run_ids != [expected_run_id]:
        raise BoundaryContractError(
            f"V551_BRIDGE_RUN_ID_MISMATCH:expected={expected_run_id}:actual={run_ids}"
        )
    if len(sources) != 1:
        raise BoundaryContractError(f"V551_BRIDGE_SOURCE_NOT_SINGULAR:{sources}")
    if len(waves) != 1:
        raise BoundaryContractError(f"V551_BRIDGE_WAVE_NOT_SINGULAR:{waves}")
    if len(shards) > 1:
        raise BoundaryContractError(f"V551_BRIDGE_SHARD_NOT_SINGULAR:{shards}")
    if not shards and len(countries) != 1:
        raise BoundaryContractError(f"V551_BRIDGE_COUNTRY_NOT_SINGULAR:{countries}")
    return {
        "run_id": expected_run_id,
        "source": sources[0],
        "wave": waves[0],
        "country_code": countries[0] if len(countries) == 1 else "",
        "shard_id": shards[0] if shards else "",
    }


def _resolve_v551_v3(repo_root: Path, v550: StageResolution) -> StageResolution:
    if not v550.usable:
        return StageResolution("v551", "", False, "BLOCKED_OR_MISSING", "selected V550 producer is not usable")
    v550_root = Path(v550.root)
    try:
        identity = _v551_expected_identity(v550_root)
        run_root = repo_root / "data" / "ddm_repository_copy" / "v551" / "runs" / identity["run_id"]
        verified = verify_v551_v3_producer_manifest(
            run_root / "manifest.json",
            run_id=identity["run_id"],
            source=identity["source"],
            wave=identity["wave"],
            country_code=identity["country_code"],
            shard_id=identity["shard_id"],
        )
    except BoundaryContractError as exc:
        return StageResolution("v551", "", False, "BLOCKED_OR_MISSING", f"V551_V3_BOUNDARY_INVALID:{exc}")

    state = verified.state
    payload = verified.manifest_payload
    metrics: dict[str, Any] = {
        "contract_version": state.contract_version,
        "schema_version": payload.get("schema_version", ""),
        "compiler_version": payload.get("compiler_version", ""),
        "run_integrity_status": state.run_integrity_status,
        "evidence_status": state.evidence_status,
        "downstream_permission_status": state.downstream_permission_status,
        "candidate_count": int(payload.get("candidate_count") or 0),
        "promotable_candidate_count": int(payload.get("promotable_candidate_count") or 0),
        "nonpromotable_candidate_count": int(payload.get("nonpromotable_candidate_count") or 0),
        "atom_count": int(payload.get("atom_count") or 0),
        "distribution_coverage_rows": int(payload.get("distribution_coverage_rows") or 0),
        "identity": identity,
        "artifacts": {
            Path(item.path).name: {
                "row_count": item.row_count,
                "artifact_file_sha256": item.artifact_file_sha256,
                "valid_empty": item.valid_empty,
            }
            for item in verified.verified_artifacts
        },
    }
    status = "/".join(
        (state.run_integrity_status, state.evidence_status, state.downstream_permission_status)
    )
    if state.downstream_permission_status == "DENY":
        return StageResolution(
            "v551",
            str(run_root),
            False,
            status,
            "V551 v3 producer integrity PASS but downstream semantic operation is denied",
            metrics,
        )
    # ALLOW and NOT_APPLICABLE are both valid terminal producer states.  The
    # next-stage adapter decides whether an operation exists for this scope.
    return StageResolution("v551", str(run_root), True, status, metrics=metrics)


def resolve_stage_roots(repo_root: str | Path, source: str, wave: str):
    _impl._latest_usable_candidate = _latest_usable_candidate
    _impl._parquet_row_count = _parquet_row_count
    _impl._stage_artifact_rows = _stage_artifact_rows
    stages = _ORIGINAL_RESOLVE_STAGE_ROOTS(repo_root, source, wave)
    repo = Path(repo_root)
    v550 = stages["v550"]
    if v550.usable:
        run_id = _impl._extract_run_id_from_v550_root(v550.root)
        shard_id = Path(v550.root).name
        exact_v550j_root = repo / "data" / "ddm_repository_copy" / "v550j" / "runs" / run_id
        joint_root = f"{shard_id}/joint_patterns"
        stages["v550j"] = _validate_root(
            exact_v550j_root,
            stage="v550j",
            required_files=(
                f"{joint_root}/joint_response_pattern_index.parquet",
                f"{joint_root}/joint_pattern_meaning_summary.parquet",
                f"{joint_root}/joint_pattern_association_index.parquet",
                f"{joint_root}/joint_pattern_association_review_surface.parquet",
                f"{joint_root}/v550j_summary.json",
                f"{joint_root}/v550j_source_wave_readiness_report.json",
            ),
            # Association evidence may be a lawful zero-row surface when the
            # producer declares association_mode=off.  Core pattern/meaning
            # evidence remains required for an applicable V550J scope.
            required_nonempty_files=(
                f"{joint_root}/joint_response_pattern_index.parquet",
                f"{joint_root}/joint_pattern_meaning_summary.parquet",
            ),
            status_paths=(
                f"{joint_root}/v550j_source_wave_readiness_report.json",
                f"{joint_root}/v550j_summary.json",
            ),
            ready_key_names=("readiness_status", "final_status", "status"),
        )
        stages["v551"] = _resolve_v551_v3(repo, v550)
    else:
        stages["v551"] = StageResolution(
            "v551", "", False, "BLOCKED_OR_MISSING", "selected V550 producer is not usable"
        )
    return stages


def main(argv=None):
    global _LEDGER_SHA
    args = list(sys.argv[1:] if argv is None else argv)
    sha = ""
    if "--dependency-ledger-sha256" in args:
        index = args.index("--dependency-ledger-sha256")
        sha = args[index + 1]
        del args[index : index + 2]
    has_ledger = "--dependency-ledger" in args
    if has_ledger and not sha:
        print('{"error":"DEPENDENCY_LEDGER_SHA256_REQUIRED"}', file=sys.stderr)
        return 2
    if not has_ledger:
        args += ["--dependency-ledger", str(_NO_LEDGER)]
    _LEDGER_SHA = sha
    _impl._load_dependency_ledger = lambda path: (
        {"stages": {}}
        if Path(path) == _NO_LEDGER
        else verify_external_dependency_ledger(path, _LEDGER_SHA)
    )
    _impl.resolve_stage_roots = resolve_stage_roots
    old_argv = sys.argv
    sys.argv = [old_argv[0], *args]
    try:
        return _impl.main()
    finally:
        sys.argv = old_argv


_impl._latest_usable_candidate = _latest_usable_candidate
_impl._parquet_row_count = _parquet_row_count
_impl._stage_artifact_rows = _stage_artifact_rows
_impl.resolve_stage_roots = resolve_stage_roots

globals().update(
    _load_dependency_ledger=_load_dependency_ledger,
    _validate_root=_validate_root,
    _latest_usable_candidate=_latest_usable_candidate,
    _parquet_row_count=_parquet_row_count,
    _stage_artifact_rows=_stage_artifact_rows,
    _v551_expected_identity=_v551_expected_identity,
    _resolve_v551_v3=_resolve_v551_v3,
    resolve_stage_roots=resolve_stage_roots,
)

if __name__ == "__main__":
    raise SystemExit(main())
