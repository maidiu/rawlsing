#!/usr/bin/env python3
"""Resolve usable Rawlsing pipeline lineage and print runnable command blocks.

The resolver is fail-closed:
* it scans the repo for candidate run roots,
* validates required artifacts and status fields,
* rejects blocked or empty lineages,
* and emits exact downstream command blocks from the verified roots.

It is generic across survey/source prefixes as long as the repo uses the same
stage layout conventions.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance  # noqa: E402
from data.ddm_build_copy.ddm_v550_manifest import utc_now  # noqa: E402

DEFAULT_DEPENDENCY_LEDGER = ROOT / "docs" / "architecture_control" / "reports" / "rawlsing_manual_pipeline_recovery_spec_through_v554.json"


@dataclass(frozen=True)
class StageResolution:
    stage: str
    root: str
    usable: bool
    status: str
    reason: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_dependency_ledger(path: Path) -> dict[str, Any]:
    ledger = _read_json(path)
    if not ledger:
        raise FileNotFoundError(f"Missing dependency ledger: {path}")
    if not isinstance(ledger.get("stages"), dict):
        raise ValueError(f"Dependency ledger missing stage map: {path}")
    return ledger


def _format_template(template: str, context: dict[str, Any]) -> str:
    try:
        return str(template).format(**context)
    except Exception:
        return str(template)


def _json_status(payload: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _sanitize_task_token(task: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(task or "").strip())
    return token.strip("_") or "task"


def _normalize_wave_token(token: str, *, source_hint: str | None = None) -> tuple[str, str]:
    text = str(token or "").strip()
    if "__" in text:
        source, wave = text.split("__", 1)
        source = source.strip().upper()
        wave = wave.strip()
        if source and wave:
            return source, wave
    if source_hint:
        return source_hint.strip().upper(), text
    raise ValueError(f"Unable to infer source for wave token: {token!r}")


def _normalize_task_token(token: str, *, source_hint: str | None = None) -> tuple[str, str, str]:
    source, wave = _normalize_wave_token(token, source_hint=source_hint)
    return source, wave, f"{source}__{wave}"


def _is_blocked_status(status: str) -> bool:
    text = status.strip().upper()
    return any(token in text for token in ("BLOCKED", "NOT_READY", "FAILED", "EMPTY_NO", "MISSING_REQUIRED"))


def _is_ready_status(status: str) -> bool:
    text = status.strip().upper()
    return "READY" in text or text in {"SUCCESS", "COMPLETE", "COMPLETED", "VALIDATED"}


def _parquet_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        import pyarrow.parquet as pq  # type: ignore

        return int(pq.ParquetFile(path).metadata.num_rows)
    except Exception:
        try:
            return int(len(pd.read_parquet(path)))
        except Exception:
            return 0


def _stage_artifact_rows(path: Path) -> int:
    if not path.exists():
        return 0
    suffix = path.suffix.lower()
    try:
        if suffix == ".parquet":
            return _parquet_row_count(path)
        if suffix == ".csv":
            try:
                return int(pd.read_csv(path, low_memory=False).shape[0])
            except Exception:
                return 0
        if suffix == ".json":
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return 0
            if isinstance(payload, dict):
                return 1 if payload else 0
            if isinstance(payload, list):
                return len(payload)
            return 1 if payload is not None else 0
        return 1 if path.stat().st_size > 0 else 0
    except Exception:
        return 0


def _stage_dependency_manifest(
    source: str,
    wave: str,
    stages: dict[str, StageResolution],
    dependency_ledger: dict[str, Any],
) -> dict[str, Any]:
    source_upper = source.upper()
    source_lower = source.lower()
    shard_id = f"{source_upper}__{wave}"
    context = {
        "repo_root": str(ROOT),
        "source_upper": source_upper,
        "source_lower": source_lower,
        "source": source_upper,
        "wave": wave,
        "shard_id": shard_id,
        "run_id": Path(stages["v550"].root).parent.name if stages["v550"].root else f"{source_lower}{wave}_unresolved",
        "v550_root": stages["v550"].root,
        "v550j_root": stages["v550j"].root,
        "v551_root": stages["v551"].root,
        "v551j_root": stages["v551j"].root,
        "v552_root": stages["v552"].root,
        "v552j_root": stages["v552j"].root,
    }

    def expand_entries(entries: list[dict[str, Any]] | None) -> list[str]:
        resolved: list[str] = []
        for entry in entries or []:
            if not isinstance(entry, dict):
                continue
            template = str(entry.get("path_template") or entry.get("path") or "").strip()
            if not template:
                continue
            try:
                path = template.format(**context)
            except Exception:
                path = template
            resolved.append(path)
        return resolved

    stage_paths: dict[str, Any] = {}
    stages_ledger = dependency_ledger.get("stages", {})
    for stage_name, stage_resolution in stages.items():
        stage_ledger = stages_ledger.get(stage_name, {}) if isinstance(stages_ledger, dict) else {}
        required_inputs = expand_entries(stage_ledger.get("required_inputs"))
        optional_inputs = expand_entries(stage_ledger.get("optional_inputs"))
        command_inputs = expand_entries(stage_ledger.get("command_inputs"))
        stage_paths[stage_name] = {
            "recovery_source": stage_ledger.get("recovery_source", "latest_verified_stage_root"),
            "root": stage_resolution.root,
            "entrypoint": stage_ledger.get("entrypoint", ""),
            "upstream_sources": stage_ledger.get("authoring_sources", []),
            "required_inputs": required_inputs,
            "optional_inputs": optional_inputs,
            "command_inputs": command_inputs,
            "known_failure_modes": stage_ledger.get("known_failure_modes", []),
        }
    stage_paths["wave"] = wave
    stage_paths["source"] = source_upper
    stage_paths["shard_id"] = shard_id
    stage_paths["ledger_path"] = str(DEFAULT_DEPENDENCY_LEDGER)
    return stage_paths


def _stage_manifest_snapshot(source: str, wave: str, stages: dict[str, StageResolution]) -> dict[str, Any]:
    source_upper = source.upper()
    source_lower = source.lower()
    shard_id = f"{source_upper}__{wave}"
    candidate_paths = {
        "v550": [
            Path(stages["v550"].root) / "shard_manifest.json",
            Path(stages["v550"].root) / "shard_status.json",
        ],
        "v550j": [
            Path(stages["v550j"].root) / "joint_patterns" / "v550j_manifest.json",
            Path(stages["v550j"].root) / "joint_patterns" / "v550j_output_validation_report.json",
        ],
        "v551": [
            Path(stages["v551"].root) / "manifest.json",
        ],
        "v551j": [
            Path(stages["v551j"].root) / "manifest" / "v551j_input_provenance_manifest.json",
            Path(stages["v551j"].root) / "manifest" / "v551j_certification_readiness_report.json",
            Path(stages["v551j"].root) / "manifest" / "v551j_review_readiness_report.json",
        ],
        "v552": [
            Path(stages["v552"].root) / "manifest" / "v552_input_provenance_manifest.json",
            Path(stages["v552"].root) / "manifest" / "v552_readiness_report.parquet",
        ],
        "v552j": [
            Path(stages["v552j"].root) / "manifest" / "v552j_runtime_handoff_manifest.json",
            Path(stages["v552j"].root) / "manifest" / "v552j_v553_handoff_manifest.json",
            Path(stages["v552j"].root) / "manifest" / "v552j_readiness_report.json",
        ],
    }
    snapshot: dict[str, Any] = {}
    for stage, paths in candidate_paths.items():
        entries: list[dict[str, Any]] = []
        for path in paths:
            payload = _read_json(path)
            if not payload:
                continue
            entries.append(
                {
                    "path": str(path),
                    "exists": True,
                    "input_documents": payload.get("input_documents", {}),
                    "invocation_command": payload.get("invocation_command", ""),
                    "invocation_script_path": payload.get("invocation_script_path", ""),
                    "source_run_ids": payload.get("source_run_ids", payload.get("source_run_ids_json", "")),
                    "source_documents": payload.get("source_documents", {}),
                }
            )
        snapshot[stage] = {
            "root": stages[stage].root,
            "manifest_candidates": [str(path) for path in paths],
            "loaded_manifests": entries,
        }
    snapshot["wave"] = wave
    snapshot["source"] = source_upper
    snapshot["shard_id"] = shard_id
    return snapshot


def _candidate_dirs(base: Path, pattern: str) -> list[Path]:
    if not base.exists():
        return []
    candidates: list[Path] = []
    for path in base.glob(f"**/{pattern}"):
        if path.is_dir():
            candidates.append(path)
    return candidates


def _discover_source_wave_pairs(repo_root: Path) -> list[tuple[str, str]]:
    stage_roots = [
        repo_root / "data" / "ddm_repository_copy" / "v550" / "shard_runs",
        repo_root / "data" / "ddm_repository_copy" / "v550j" / "runs",
        repo_root / "data" / "ddm_repository_copy" / "v551" / "runs",
        repo_root / "data" / "ddm_repository_copy" / "v551j" / "runs",
        repo_root / "data" / "ddm_repository_copy" / "v552" / "runs",
        repo_root / "data" / "ddm_repository_copy" / "v552j" / "runs",
    ]
    discovered: set[tuple[str, str]] = set()
    for stage_root in stage_roots:
        if not stage_root.exists():
            continue
        for path in stage_root.glob("**/*"):
            text = str(path)
            for match in re.finditer(r"([A-Za-z0-9]+)__([0-9]{4})", text):
                source = match.group(1).strip().upper()
                wave = match.group(2).strip()
                if source and wave.isdigit():
                    discovered.add((source, wave))
    return sorted(discovered, key=lambda item: (item[0], item[1]))


def _rank_candidates(base: Path, candidates: Iterable[Path]) -> list[tuple[int, int, Path]]:
    ranked: list[tuple[int, int, Path]] = []
    for path in candidates:
        try:
            stat = path.stat()
        except Exception:
            continue
        ranked.append((int(getattr(stat, "st_mtime_ns", int(stat.st_mtime * 1_000_000_000))), -len(path.parts), path))
    ranked.sort(reverse=True)
    return ranked


def _latest_usable_candidate(
    base: Path,
    pattern: str,
    *,
    stage: str,
    required_files: tuple[str, ...],
    required_nonempty_files: tuple[str, ...] = (),
    status_paths: tuple[str, ...] = (),
    ready_key_names: tuple[str, ...] = (),
    reject_blocked: bool = True,
    require_ready: bool = False,
) -> StageResolution:
    candidates = _rank_candidates(base, _candidate_dirs(base, pattern))
    best_reason = f"no candidate matched {pattern}"
    for _, _, root in candidates:
        missing = [rel for rel in required_files if not (root / rel).exists()]
        if missing:
            best_reason = f"missing required files: {missing}"
            continue
        nonempty_missing = [rel for rel in required_nonempty_files if _parquet_row_count(root / rel) <= 0]
        if nonempty_missing:
            best_reason = f"empty required artifacts: {nonempty_missing}"
            continue
        status = ""
        status_payload: dict[str, Any] = {}
        for rel in status_paths:
            payload = _read_json(root / rel)
            if payload:
                status_payload = payload
                status = _json_status(payload, ready_key_names) if ready_key_names else _json_status(payload, ("status", "final_status", "readiness_status"))
                break
        if reject_blocked and status and _is_blocked_status(status):
            best_reason = f"blocked status: {status}"
            continue
        if require_ready and status and not _is_ready_status(status):
            best_reason = f"not ready status: {status}"
            continue

        metrics: dict[str, Any] = {}
        for rel in required_nonempty_files:
            metrics[rel] = _parquet_row_count(root / rel)
        for key in ("row_counts", "counts", "core_tables_rebuilt"):
            if isinstance(status_payload.get(key), dict):
                metrics[key] = status_payload.get(key)
        if not status:
            status = _json_status(status_payload, ready_key_names) if ready_key_names else ""
        if not status:
            status = "unknown"
        return StageResolution(stage=stage, root=str(root), usable=True, status=status, metrics=metrics)

    return StageResolution(stage=stage, root="", usable=False, status="BLOCKED_OR_MISSING", reason=best_reason)


def _extract_run_id_from_v550_root(root: str) -> str:
    path = Path(root)
    return path.parent.name if path.parent.name else path.name


def _source_prefix(source: str) -> tuple[str, str]:
    upper = source.upper()
    lower = source.lower()
    return upper, lower


def _discover_wave_specs(repo_root: Path, source_filter: str | None = None) -> list[tuple[str, str]]:
    shard_root = repo_root / "data" / "ddm_repository_copy" / "v550" / "shard_runs"
    specs: set[tuple[str, str]] = set()
    if not shard_root.exists():
        return []
    for path in shard_root.glob("**/*"):
        if not path.is_dir():
            continue
        shard_id = path.name
        if "__" not in shard_id:
            continue
        source, wave = shard_id.split("__", 1)
        source = source.strip().upper()
        wave = wave.strip()
        if not source or not wave.isdigit():
            continue
        if source_filter and source != source_filter.upper():
            continue
        specs.add((source, wave))
    return sorted(specs, key=lambda item: (item[0], item[1]))


def resolve_stage_roots(repo_root: str | Path, source: str, wave: str) -> dict[str, StageResolution]:
    repo = Path(repo_root)
    source_upper, source_lower = _source_prefix(source)
    shard_id = f"{source_upper}__{wave}"

    v550 = _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v550" / "shard_runs",
        shard_id,
        stage="v550",
        required_files=(
            "shard_status.json",
            "shard_scope.parquet",
            "bridge/v551_bridge_index.parquet",
            "core/question_use_contract.parquet",
        ),
        required_nonempty_files=("bridge/v551_bridge_index.parquet", "core/question_use_contract.parquet"),
        status_paths=("shard_status.json",),
        ready_key_names=("status", "final_status", "readiness_status"),
        reject_blocked=True,
        require_ready=False,
    )

    run_id = _extract_run_id_from_v550_root(v550.root) if v550.usable else f"{source_lower}{wave}_unresolved"

    v550j = _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v550j" / "runs",
        f"{source_lower}{wave}_*",
        stage="v550j",
        required_files=(
            f"{shard_id}/joint_patterns/joint_response_pattern_index.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_meaning_summary.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_association_index.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_association_review_surface.parquet",
            f"{shard_id}/joint_patterns/v550j_summary.json",
            f"{shard_id}/joint_patterns/v550j_source_wave_readiness_report.json",
        ),
        required_nonempty_files=(
            f"{shard_id}/joint_patterns/joint_response_pattern_index.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_meaning_summary.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_association_index.parquet",
        ),
        status_paths=(
            f"{shard_id}/joint_patterns/v550j_source_wave_readiness_report.json",
            f"{shard_id}/joint_patterns/v550j_summary.json",
        ),
        ready_key_names=("readiness_status", "final_status", "status"),
        reject_blocked=True,
        require_ready=False,
    )

    v551 = _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v551" / "runs",
        f"{run_id}",
        stage="v551",
        required_files=(
            "manifest.json",
            "relation_evidence_atoms.parquet",
            "relation_review_surface.parquet",
            "exclusion_summary.parquet",
            "numeric_wrapper_audit.parquet",
        ),
        required_nonempty_files=("relation_evidence_atoms.parquet",),
        status_paths=("manifest.json",),
        ready_key_names=("status", "final_status", "readiness_status"),
        reject_blocked=True,
        require_ready=False,
    )

    v551j = _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v551j" / "runs",
        f"{run_id}",
        stage="v551j",
        required_files=(
            "manifest/v551j_certification_readiness_report.json",
            "manifest/v551j_review_readiness_report.json",
            "manifest/v551j_input_provenance_manifest.json",
            "packets/v551j_certified_packet_index.parquet",
            "packets/v551j_reviewable_evidence_sidecar.parquet",
        ),
        required_nonempty_files=(
            "packets/v551j_certified_packet_index.parquet",
            "packets/v551j_reviewable_evidence_sidecar.parquet",
        ),
        status_paths=("manifest/v551j_certification_readiness_report.json", "manifest/v551j_review_readiness_report.json"),
        ready_key_names=("final_status", "status"),
        reject_blocked=True,
        require_ready=False,
    )

    v552 = _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v552" / "runs",
        f"{run_id}",
        stage="v552",
        required_files=(
            "manifest/v552_readiness_report.parquet",
            "manifest/v552_input_provenance_manifest.json",
            "structural/question_semantic_hierarchy.parquet",
            "structural/structural_channel_index.parquet",
            "structural/relation_axis_pressure.parquet",
            "structural/target_entity_pressure.parquet",
            "structural/driver_facet_pressure.parquet",
            "structural/horizon_constraint_index.parquet",
            "structural/v552_artifact_authority_index.parquet",
            "structural/v552_known_absence_register.parquet",
            "structural/v552_structural_fact_index.parquet",
            "structural/v552_temporal_key_source_index.parquet",
        ),
        required_nonempty_files=(
            "structural/v552_structural_fact_index.parquet",
            "structural/question_semantic_hierarchy.parquet",
        ),
        status_paths=("manifest/v552_readiness_report.parquet",),
        ready_key_names=("status", "final_status", "readiness_status"),
        reject_blocked=True,
        require_ready=False,
    )

    v552j = _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v552j" / "runs",
        f"{run_id}",
        stage="v552j",
        required_files=(
            "manifest/v552j_readiness_report.json",
            "manifest/v552j_runtime_handoff_manifest.json",
            "manifest/v552j_v553_handoff_manifest.json",
            "packets/v552j_structural_handoff_packet.json",
            "packets/v552j_v553_input_index.parquet",
            "packets/v552j_to_v553_handoff_index.parquet",
        ),
        required_nonempty_files=(
            "packets/v552j_v553_input_index.parquet",
            "packets/v552j_to_v553_handoff_index.parquet",
        ),
        status_paths=("manifest/v552j_readiness_report.json", "manifest/v552j_runtime_handoff_manifest.json"),
        ready_key_names=("status", "final_status", "readiness_status"),
        reject_blocked=True,
        require_ready=False,
    )

    return {
        "v550": v550,
        "v550j": v550j,
        "v551": v551,
        "v551j": v551j,
        "v552": v552,
        "v552j": v552j,
    }


def _v553_wave_prefix(source: str, waves: list[str]) -> str:
    source_lower = source.lower()
    return f"{source_lower}{'_'.join(waves)}_v553_"


def resolve_v553_root(repo_root: str | Path, source: str, waves: list[str]) -> StageResolution:
    repo = Path(repo_root)
    prefix = _v553_wave_prefix(source, waves)
    return _latest_usable_candidate(
        repo / "data" / "ddm_repository_copy" / "v553" / "runs",
        f"{prefix}*",
        stage="v553",
        required_files=(
            "manifest/v553_temporal_readiness_report.json",
            "manifest/v553_wave_harmonization_report.json",
            "packets/v553_temporal_pressure_field_packet.json",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "packets/v553_interpolated_pressure_over_time.parquet",
            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
        ),
        required_nonempty_files=(
            "packets/v553_temporal_pressure_field_packet.json",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "packets/v553_interpolated_pressure_over_time.parquet",
            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
        ),
        status_paths=("manifest/v553_temporal_readiness_report.json", "manifest/v553_wave_harmonization_report.json"),
        ready_key_names=("overall_status", "status", "final_status"),
        reject_blocked=True,
        require_ready=False,
    )


def _wave_command_block(
    *,
    repo_root: Path,
    source: str,
    wave: str,
    resolutions: dict[str, StageResolution],
    response_option_map: str,
    directionality_authority_dir: str,
    env_file: str,
) -> list[str]:
    source_upper, source_lower = _source_prefix(source)
    shard_id = f"{source_upper}__{wave}"
    v550 = resolutions["v550"]
    v550j = resolutions["v550j"]
    v551 = resolutions["v551"]
    v551j = resolutions["v551j"]
    v552 = resolutions["v552"]
    v552j = resolutions["v552j"]
    v550_run_id = Path(v550.root).parent.name if v550.root else f"{source_lower}{wave}_unresolved"
    v551_run_id = Path(v551.root).name if v551.root else v550_run_id
    v551j_run_id = Path(v551j.root).name if v551j.root else v550_run_id
    v552_run_id = Path(v552.root).name if v552.root else v550_run_id
    v552j_run_id = Path(v552j.root).name if v552j.root else v550_run_id
    v550_shard_dir = f"$COPY_REPO_ROOT/v550/shard_runs/{v550_run_id}/{shard_id}"
    v550j_joint_dir = f"$COPY_REPO_ROOT/v550j/runs/{v550_run_id}/{shard_id}/joint_patterns"
    v551_atoms_path = f"$COPY_REPO_ROOT/v551/runs/{v551_run_id}/relation_evidence_atoms.parquet"
    v551j_root = f"$COPY_REPO_ROOT/v551j/runs/{v551j_run_id}"
    v552_root = f"$COPY_REPO_ROOT/v552/runs/{v552_run_id}"
    v552j_root = f"$COPY_REPO_ROOT/v552j/runs/{v552j_run_id}"
    source_structure_audit = f"$COPY_REPO_ROOT/v550/validation/{source_upper}_{wave}/source_structure_population_audit.csv"

    lines = [
        f"# Wave {wave}",
        'cd "${RAWLSING_REPO_ROOT:?Set RAWLSING_REPO_ROOT}"',
        "",
        f"export COPY_REPO_ROOT=data/ddm_repository_copy",
        f"export BUILD_ROOT=data/ddm_build_copy",
        f"export ENV_FILE={env_file}",
        f"export RESPONSE_OPTION_MAP={response_option_map}",
        f"export DIRECTIONALITY_AUTHORITY_DIR={directionality_authority_dir}",
        f"export RUN_ID={v550_run_id}",
        f"export SHARD_ID={shard_id}",
        f"export V550_SHARD_DIR={v550_shard_dir}",
        f"export V550_VALIDATION_ROOT=$COPY_REPO_ROOT/v550/validation/{source_upper}_{wave}",
        f"export V550J_DIR=$COPY_REPO_ROOT/v550j/runs/{v550_run_id}/{shard_id}/joint_patterns",
        f"export V551_ROOT=$COPY_REPO_ROOT/v551/runs/{v551_run_id}",
        f"export V551J_ROOT={v551j_root}",
        f"export V552_ROOT={v552_root}",
        f"export V552J_ROOT={v552j_root}",
        "",
        "python3 \"$BUILD_ROOT/compile_v550j_joint_response_patterns.py\" \\",
        "  --v550-shard-dir \"$V550_SHARD_DIR\" \\",
        "  --output-root \"$COPY_REPO_ROOT/v550j\" \\",
        "  --registry-path \"${QUESTION_FAMILY_REGISTRY:?Set QUESTION_FAMILY_REGISTRY for this survey family}\" \\",
        "  --env-file \"$ENV_FILE\" \\",
        "  --with-diagnostics \\",
        "  --association-mode publishable \\",
        "  --publish-association-lanes substantive_attitude_association \\",
        "  --no-write-csv \\",
        "  --write-parquet \\",
        "  --verbose",
        "",
        "python3 \"$BUILD_ROOT/compile_v551_relation_evidence_atoms.py\" \\",
        "  --run-id \"$RUN_ID\" \\",
        "  --bridge-path \"$V550_SHARD_DIR/bridge/v551_bridge_index.parquet\" \\",
        "  --question-use-contract-path \"$V550_SHARD_DIR/core/question_use_contract.parquet\" \\",
        f"  --source-structure-audit-path \"{source_structure_audit}\" \\",
        f"  --response-option-map-path \"{response_option_map}\" \\",
        "  --output-root \"$COPY_REPO_ROOT/v551/runs\" \\",
        "  --no-write-csv \\",
        "  --write-parquet \\",
        "  --verbose",
        "",
        "python3 \"$BUILD_ROOT/compile_v551j_joint_evidence_packets.py\" \\",
        "  --run-id \"$RUN_ID\" \\",
        "  --v551-atoms-path \"$V551_ROOT/relation_evidence_atoms.parquet\" \\",
        "  --v550j-pattern-index-path \"$V550J_DIR/joint_response_pattern_index.parquet\" \\",
        "  --v550j-meaning-summary-path \"$V550J_DIR/joint_pattern_meaning_summary.parquet\" \\",
        "  --v550j-association-index-path \"$V550J_DIR/joint_pattern_association_index.parquet\" \\",
        "  --v550j-review-surface-path \"$V550J_DIR/joint_pattern_association_review_surface.parquet\" \\",
    ]
    if v552.root:
        lines.extend(
            [
                "  --v552-question-semantic-hierarchy-path \"$V552_ROOT/structural/question_semantic_hierarchy.parquet\" \\",
                "  --v552-structural-channel-index-path \"$V552_ROOT/structural/structural_channel_index.parquet\" \\",
                "  --v552-relation-axis-pressure-path \"$V552_ROOT/structural/relation_axis_pressure.parquet\" \\",
                "  --v552-target-entity-pressure-path \"$V552_ROOT/structural/target_entity_pressure.parquet\" \\",
                "  --v552-driver-facet-pressure-path \"$V552_ROOT/structural/driver_facet_pressure.parquet\" \\",
                "  --v552-contradiction-surface-path \"$V552_ROOT/structural/contradiction_surface.parquet\" \\",
                "  --v552-horizon-constraint-index-path \"$V552_ROOT/structural/horizon_constraint_index.parquet\" \\",
                "  --v552-parent-prior-manifest-path \"$V552_ROOT/structural/parent_prior_manifest.parquet\" \\",
                "  --v552-artifact-authority-index-path \"$V552_ROOT/structural/v552_artifact_authority_index.parquet\" \\",
                "  --v552-known-absence-register-path \"$V552_ROOT/structural/v552_known_absence_register.parquet\" \\",
                "  --v552-structural-fact-index-path \"$V552_ROOT/structural/v552_structural_fact_index.parquet\" \\",
                "  --v552-temporal-key-source-index-path \"$V552_ROOT/structural/v552_temporal_key_source_index.parquet\" \\",
            ]
        )
    lines.extend([
        "  --emit-review-surface \\",
        "  --emit-certified-index \\",
        "  --output-root \"$COPY_REPO_ROOT/v551j/runs\" \\",
        "  --no-write-csv \\",
        "  --write-parquet \\",
        "  --strict \\",
        "  --verbose",
        "",
        "python3 \"$BUILD_ROOT/compile_v552_structural_ddm.py\" \\",
        "  --run-id \"$RUN_ID\" \\",
        "  --atoms-path \"$V551_ROOT/relation_evidence_atoms.parquet\" \\",
        "  --output-root \"$COPY_REPO_ROOT/v552/runs\" \\",
        "  --no-write-csv \\",
        "  --write-parquet \\",
        "  --verbose",
        "",
        "python3 \"$BUILD_ROOT/compile_v552j_runtime_safe_structural_handoff.py\" \\",
        "  --run-id \"$RUN_ID\" \\",
        "  --v551j-run-root \"$V551J_ROOT\" \\",
        "  --v551j-comparison-root \"$V551J_ROOT\" \\",
        "  --v552-question-semantic-hierarchy-path \"$V552_ROOT/structural/question_semantic_hierarchy.parquet\" \\",
        "  --v552-structural-channel-index-path \"$V552_ROOT/structural/structural_channel_index.parquet\" \\",
        "  --v552-relation-axis-pressure-path \"$V552_ROOT/structural/relation_axis_pressure.parquet\" \\",
        "  --v552-target-entity-pressure-path \"$V552_ROOT/structural/target_entity_pressure.parquet\" \\",
        "  --v552-driver-facet-pressure-path \"$V552_ROOT/structural/driver_facet_pressure.parquet\" \\",
        "  --v552-contradiction-surface-path \"$V552_ROOT/structural/contradiction_surface.parquet\" \\",
        "  --v552-horizon-constraint-index-path \"$V552_ROOT/structural/horizon_constraint_index.parquet\" \\",
        "  --v552-parent-prior-manifest-path \"$V552_ROOT/structural/parent_prior_manifest.parquet\" \\",
        "  --v552-artifact-authority-index-path \"$V552_ROOT/structural/v552_artifact_authority_index.parquet\" \\",
        "  --v552-known-absence-register-path \"$V552_ROOT/structural/v552_known_absence_register.parquet\" \\",
        "  --v552-structural-fact-index-path \"$V552_ROOT/structural/v552_structural_fact_index.parquet\" \\",
        "  --v552-temporal-key-source-index-path \"$V552_ROOT/structural/v552_temporal_key_source_index.parquet\" \\",
        "  --no-write-csv \\",
        "  --write-parquet \\",
        "  --strict \\",
        "  --verbose",
        "",
    ])
    return lines


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Rawlsing Pipeline Lineage Resolver",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Source: `{report['source']}`",
        f"- Waves: `{', '.join(report['waves'])}`",
        "",
        "## Resolved Roots",
        "",
        "| Wave | First unresolved | v550 | v550j | v551 | v551j | v552 | v552j |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in report["wave_resolutions"]:
        lines.append(
            "| {wave} | {floor} | {v550} | {v550j} | {v551} | {v551j} | {v552} | {v552j} |".format(
                wave=row["wave"],
                floor=row.get("first_unresolved_stage") or "resolved",
                v550=row["stages"]["v550"]["root"] or "missing",
                v550j=row["stages"]["v550j"]["root"] or "missing",
                v551=row["stages"]["v551"]["root"] or "missing",
                v551j=row["stages"]["v551j"]["root"] or "missing",
                v552=row["stages"]["v552"]["root"] or "missing",
                v552j=row["stages"]["v552j"]["root"] or "missing",
            )
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This resolver selects usable run roots from actual repo artifacts instead of trusting the newest directory.",
            "- It rejects blocked or empty lineages before command emission.",
            "- The emitted shell block is intentionally per-wave, not a loop, so the command lineage is explicit.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _build_report(
    *,
    repo_root: Path,
    source: str,
    waves: list[str],
    wave_resolutions: list[dict[str, Any]],
    combined_v553: StageResolution | None,
    command_block: str,
    dependency_ledger_path: str = "",
    shell_script_path: str = "",
) -> dict[str, Any]:
    resolved_waves = [row["task_id"] for row in wave_resolutions if all(stage["usable"] for stage in row["stages"].values())]
    unresolved_waves = [row["task_id"] for row in wave_resolutions if not all(stage["usable"] for stage in row["stages"].values())]
    return {
        "repo_root": str(repo_root),
        "source": source.upper(),
        "waves": waves,
        "created_at": utc_now(),
        "shell_script_path": shell_script_path,
        "dependency_ledger_path": dependency_ledger_path,
        "resolved_waves": resolved_waves,
        "unresolved_waves": unresolved_waves,
        "command_block": command_block,
        "wave_resolutions": wave_resolutions,
        "combined_v553": {
            "root": combined_v553.root if combined_v553 else "",
            "usable": combined_v553.usable if combined_v553 else False,
            "status": combined_v553.status if combined_v553 else "",
            "reason": combined_v553.reason if combined_v553 else "",
            "metrics": combined_v553.metrics if combined_v553 else {},
        },
        "provenance": capture_run_provenance(
            input_documents={
                "repo_root": str(repo_root),
                "source": source.upper(),
                "waves": waves,
            },
            extra={
                "command_family": "pipeline_lineage_resolver",
                "survey_prefix": source.upper(),
            },
        ),
    }


def _format_summary_block(resolved_waves: list[str], unresolved_waves: list[str], json_path: Path, sh_path: Path) -> str:
    run_waves = unresolved_waves if unresolved_waves else resolved_waves
    run_shell = f"WRITE_CSV=0 VERBOSE=1 STRICT=1 bash {shlex.quote(str(sh_path))} {' '.join(shlex.quote(w) for w in run_waves)}"
    return "\n".join(
        [
            f"RESOLVED_WAVES: {' '.join(resolved_waves) if resolved_waves else '(none)'}",
            f"UNRESOLVED_WAVES: {' '.join(unresolved_waves) if unresolved_waves else '(none)'}",
            f"# resolver_report: {json_path}",
            f"# resolver_shell_script: {sh_path}",
            f"# run_shell: {run_shell}",
        ]
    )


def _stage_floor(stages: dict[str, StageResolution]) -> str:
    for stage_name in ("v550", "v550j", "v551", "v551j", "v552", "v552j"):
        if not stages[stage_name].usable:
            return stage_name
    return ""


def _write_dynamic_shell_script(
    *,
    path: Path,
    repo_root: Path,
    source: str,
    waves: list[str],
    default_unresolved_waves: list[str],
    response_option_map: str,
    directionality_authority_dir: str,
    env_file: str,
    dependency_ledger_path: str,
) -> None:
    source_upper = source.upper()
    source_lower = source.lower()
    waves_literal = " ".join(shlex.quote(str(w)) for w in waves)
    default_unresolved_literal = " ".join(shlex.quote(str(w)) for w in default_unresolved_waves)
    script = f"""#!/usr/bin/env bash
set -euo pipefail

ROOT={shlex.quote(str(repo_root))}
BUILD="$ROOT/data/ddm_build_copy"
REPO="$ROOT/data/ddm_repository_copy"
COPY_REPO_ROOT="$ROOT/data/ddm_repository_copy"
BUILD_ROOT="$ROOT/data/ddm_build_copy"
SOURCE={shlex.quote(source_upper)}
SOURCE_LOWER={shlex.quote(source_lower)}
DEFAULT_UNRESOLVED_WAVES=({default_unresolved_literal})
GENERATED_WAVES=({waves_literal})
WAVES=()
if [[ ${{#DEFAULT_UNRESOLVED_WAVES[@]}} -gt 0 ]]; then
  WAVES=("${{DEFAULT_UNRESOLVED_WAVES[@]}}")
fi
if (($#)); then
  WAVES=("$@")
fi
ENV_FILE={shlex.quote(env_file)}
RESPONSE_OPTION_MAP={shlex.quote(response_option_map)}
DIRECTIONALITY_AUTHORITY_DIR={shlex.quote(directionality_authority_dir)}
DEPENDENCY_LEDGER_PATH={shlex.quote(dependency_ledger_path)}
export DEPENDENCY_LEDGER_PATH
export COPY_REPO_ROOT BUILD_ROOT
WRITE_CSV="${{WRITE_CSV:-0}}"
VERBOSE="${{VERBOSE:-1}}"
STRICT="${{STRICT:-1}}"
RESOLVER="$BUILD/resolve_pipeline_lineage.py"

csv_args=()
if [[ "$WRITE_CSV" == "1" ]]; then
  csv_args+=(--write-csv)
else
  csv_args+=(--no-write-csv)
fi

verbose_args=()
if [[ "$VERBOSE" == "1" ]]; then
  verbose_args+=(--verbose)
fi

strict_args=()
if [[ "$STRICT" == "1" ]]; then
  strict_args+=(--strict)
fi

parse_task_id() {{
  local task="$1"
  if [[ "$task" == *"__"* ]]; then
    TASK_SOURCE="${{task%%__*}}"
    TASK_WAVE="${{task#*__}}"
  else
    TASK_SOURCE="$SOURCE"
    TASK_WAVE="$task"
  fi
}}

report_path_for_task() {{
  local task="$1"
  python3 - "$task" <<'PY'
import os
import re
import sys
from pathlib import Path

task = re.sub(r"[^A-Za-z0-9_.-]+", "_", sys.argv[1]).strip("_") or "task"
tmpdir = Path(os.environ.get("TMPDIR", "/tmp"))
print(tmpdir / f"rawlsing_lineage_{{task}}.json")
PY
}}

stage_input_guard() {{
  local task="$1"
  local stage="$2"
  local report_json="$3"
  python3 - "$task" "$stage" "$report_json" <<'PY'
import json
import os
import sys
from pathlib import Path

task = sys.argv[1]
stage = sys.argv[2]
report = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
ledger_path = Path(os.environ.get("DEPENDENCY_LEDGER_PATH", ""))
if not ledger_path.exists():
    raise SystemExit(f"missing dependency ledger: {{ledger_path}}")
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
row = next((item for item in report.get("wave_resolutions", []) if str(item.get("task_id") or f"{{item.get('source')}}__{{item.get('wave')}}") == str(task)), None)
if not row:
    raise SystemExit(f"missing wave row for {{task}}")
stages = row.get("stages", {{}})
stage_row = stages.get(stage, {{}})
if stage != next((name for name in ("v550", "v550j", "v551", "v551j", "v552", "v552j") if not stages.get(name, {{}}).get("usable", False)), ""):
    raise SystemExit(f"{{stage}} is not the first unresolved stage for {{task}}")

source = str(row.get("source") or task.split("__", 1)[0] or "").upper()
wave = str(row.get("wave") or task.split("__", 1)[-1] or "")
source_lower = source.lower()
shard_id = f"{{source}}__{{wave}}"
v550_root = str(stages.get("v550", {{}}).get("root") or "")
if v550_root:
    run_id = Path(v550_root).parent.name
else:
    run_id = f"{{source_lower}}{{wave}}_unresolved"
context = {{
    "repo_root": os.getcwd(),
    "source_upper": source,
    "source_lower": source_lower,
    "source": source,
    "wave": wave,
    "shard_id": shard_id,
    "run_id": run_id,
    "v550_root": v550_root,
    "v550j_root": str(stages.get("v550j", {{}}).get("root") or ""),
    "v551_root": str(stages.get("v551", {{}}).get("root") or ""),
    "v551j_root": str(stages.get("v551j", {{}}).get("root") or ""),
    "v552_root": str(stages.get("v552", {{}}).get("root") or ""),
    "v552j_root": str(stages.get("v552j", {{}}).get("root") or ""),
}}

def expand_entry(entry: object) -> str:
    if isinstance(entry, dict):
        template = str(entry.get("path_template") or entry.get("path") or "").strip()
        if not template:
            return ""
        try:
            return template.format(**context)
        except Exception:
            return template
    return str(entry or "").strip()

def must_exist(rel: str, nonempty: bool = False) -> None:
    path = Path(rel)
    if not path.exists():
        raise SystemExit(f"missing required input: {{path}}")
    if nonempty:
        suffix = path.suffix.lower()
        if suffix == ".parquet":
            try:
                import pyarrow.parquet as pq

                row_count = int(pq.ParquetFile(path).metadata.num_rows)
            except Exception:
                try:
                    import pandas as pd

                    row_count = int(len(pd.read_parquet(path)))
                except Exception:
                    row_count = 0
            if row_count <= 0:
                raise SystemExit(f"empty required input: {{path}}")
            return
        if suffix == ".json":
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                raise SystemExit(f"invalid required input: {{path}}: {{exc}}")
            if isinstance(payload, dict) and not payload:
                raise SystemExit(f"empty required input: {{path}}")
            if isinstance(payload, list) and not payload:
                raise SystemExit(f"empty required input: {{path}}")
            return
        if path.stat().st_size <= 0:
            raise SystemExit(f"empty required input: {{path}}")

stage_manifest = ledger.get("stages", {{}}).get(stage, {{}})
required_inputs = [expand_entry(entry) for entry in stage_manifest.get("required_inputs", [])]
if not required_inputs:
    raise SystemExit(f"missing dependency manifest inputs for {{task}} stage {{stage}}")
for doc_path in required_inputs:
    must_exist(str(doc_path), nonempty=True)

optional_inputs = [expand_entry(entry) for entry in stage_manifest.get("optional_inputs", [])]
for doc_path in optional_inputs:
    if doc_path:
        must_exist(str(doc_path), nonempty=False)
PY
}}

log_stage_inputs() {{
  local task="$1"
  local stage="$2"
  case "$stage" in
    v550j)
      echo "[resolver] task $task stage v550j inputs:" >&2
      echo "  V550_SHARD_DIR=$V550_SHARD_DIR" >&2
      echo "  RESPONSE_OPTION_MAP=$RESPONSE_OPTION_MAP" >&2
      echo "  ENV_FILE=$ENV_FILE" >&2
      ;;
    v551)
      echo "[resolver] task $task stage v551 inputs:" >&2
      echo "  V550_SHARD_DIR=$V550_SHARD_DIR" >&2
      echo "  V550_VALIDATION_ROOT=$COPY_REPO_ROOT/v550/validation/${{SOURCE}}_${{WAVE}}" >&2
      echo "  RESPONSE_OPTION_MAP=$RESPONSE_OPTION_MAP" >&2
      ;;
    v551j)
      echo "[resolver] task $task stage v551j inputs:" >&2
      echo "  V551_ROOT=$V551_ROOT" >&2
      echo "  V550J_DIR=$V550J_DIR" >&2
      ;;
    v552)
      echo "[resolver] task $task stage v552 inputs:" >&2
      echo "  V551_ROOT=$V551_ROOT" >&2
      ;;
    v552j)
      echo "[resolver] task $task stage v552j inputs:" >&2
      echo "  V551J_ROOT=$V551J_ROOT" >&2
      echo "  V552_ROOT=$V552_ROOT" >&2
      ;;
  esac
}}

report_stage_floor() {{
  local report_json="$1"
  python3 - "$report_json" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
row = report["wave_resolutions"][0]
for stage_name in ("v550", "v550j", "v551", "v551j", "v552", "v552j"):
    stage = row["stages"][stage_name]
    if not stage.get("usable", False):
        print(stage_name)
        raise SystemExit(0)
print("")
PY
}}

print_wave_plan() {{
  local resolved=()
  local unresolved=()
  local task report_json
  for task in "${{WAVES[@]}}"; do
    report_json="$(resolve_report "$task")"
    eval "$(emit_exports "$report_json")"
    if [[ -z "$(report_stage_floor "$report_json")" ]]; then
      resolved+=("$task")
    else
      unresolved+=("$task")
    fi
  done
  echo "RESOLVED_WAVES: ${{resolved[*]:-(none)}}"
  echo "UNRESOLVED_WAVES: ${{unresolved[*]:-(none)}}"
  echo "# resolver_shell_script: $0"
  echo "# dependency_ledger: $DEPENDENCY_LEDGER_PATH"
  local run_waves=("${{WAVES[@]}}")
  if [[ ${{#run_waves[@]}} -eq 0 ]]; then
    run_waves=("${{DEFAULT_UNRESOLVED_WAVES[@]}}")
  fi
  echo "# run_shell: WRITE_CSV=${{WRITE_CSV:-0}} VERBOSE=${{VERBOSE:-1}} STRICT=${{STRICT:-1}} bash $0 ${{run_waves[*]}}"
}}

resolve_report() {{
  local task="$1"
  parse_task_id "$task"
  local report_json
  report_json="$(report_path_for_task "$task")"
  python3 "$RESOLVER" \
    --repo-root "$ROOT" \
    --dependency-ledger "$DEPENDENCY_LEDGER_PATH" \
    --source "$TASK_SOURCE" \
    --waves "$TASK_WAVE" \
    --report-json "$report_json" \
    --quiet >/dev/null
  printf '%s' "$report_json"
}}

emit_exports() {{
  local report_json="$1"
  python3 - "$report_json" <<'PY'
import json, sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
row = report["wave_resolutions"][0]
stages = row["stages"]
wave = row["wave"]
source = row.get("source", "")

def emit(key, value):
    if value is None:
        value = ""
    print("export " + key + "=" + json.dumps(value))

emit("V550_ROOT", stages["v550"]["root"])
emit("V550_USABLE", "1" if stages["v550"]["usable"] else "0")
emit("V550_STATUS", stages["v550"]["status"])
emit("V550J_ROOT", stages["v550j"]["root"])
emit("V550J_USABLE", "1" if stages["v550j"]["usable"] else "0")
emit("V550J_STATUS", stages["v550j"]["status"])
emit("V551_ROOT", stages["v551"]["root"])
emit("V551_USABLE", "1" if stages["v551"]["usable"] else "0")
emit("V551_STATUS", stages["v551"]["status"])
emit("V551J_ROOT", stages["v551j"]["root"])
emit("V551J_USABLE", "1" if stages["v551j"]["usable"] else "0")
emit("V551J_STATUS", stages["v551j"]["status"])
emit("V552_ROOT", stages["v552"]["root"])
emit("V552_USABLE", "1" if stages["v552"]["usable"] else "0")
emit("V552_STATUS", stages["v552"]["status"])
emit("V552J_ROOT", stages["v552j"]["root"])
emit("V552J_USABLE", "1" if stages["v552j"]["usable"] else "0")
emit("V552J_STATUS", stages["v552j"]["status"])
emit("V550_SHARD_DIR", stages["v550"]["root"])
emit("V550J_DIR", stages["v550j"]["root"])
emit("RUN_ID", Path(stages["v550"]["root"]).parent.name if stages["v550"]["root"] else "")
emit("SHARD_ID", source + "__" + wave)
emit("SOURCE", source)
emit("WAVE", wave)
PY
}}

run_recovery_chain_for_task() {{
  local task="$1"
  local report_json
  report_json="$(resolve_report "$task")"
  eval "$(emit_exports "$report_json")"

  local stage
  stage="$(report_stage_floor "$report_json")"
  if [[ -z "$stage" ]]; then
    echo "[resolver] wave $task: recovery complete" >&2
    return 0
  fi
  if [[ "$stage" == "v550" ]]; then
    echo "[resolver] wave $task: v550 is upstream of this recovery runner; rebuild that shard first" >&2
    return 1
  fi

  stage_input_guard "$task" "$stage" "$report_json"
  log_stage_inputs "$task" "$stage"

  case "$stage" in
    v550j)
  python3 "$BUILD/compile_v550j_joint_response_patterns.py" \
    --v550-shard-dir "$V550_SHARD_DIR" \
    --output-root "$COPY_REPO_ROOT/v550j" \
    --registry-path "${QUESTION_FAMILY_REGISTRY:?Set QUESTION_FAMILY_REGISTRY for this survey family}" \
    --response-option-map "$RESPONSE_OPTION_MAP" \
    --env-file "$ENV_FILE" \
    --with-diagnostics \
    --association-mode publishable \
    --publish-association-lanes substantive_attitude_association \
    --write-parquet \
    "${{csv_args[@]}}" \
    "${{verbose_args[@]}}"
    ;;
    v551)
  python3 "$BUILD/compile_v551_relation_evidence_atoms.py" \
    --run-id "$RUN_ID" \
    --bridge-path "$V550_SHARD_DIR/bridge/v551_bridge_index.parquet" \
    --question-use-contract-path "$V550_SHARD_DIR/core/question_use_contract.parquet" \
    --source-structure-audit-path "$COPY_REPO_ROOT/v550/validation/${{SOURCE}}_${{WAVE}}/source_structure_population_audit.csv" \
    --response-option-map-path "$RESPONSE_OPTION_MAP" \
    --output-root "$COPY_REPO_ROOT/v551/runs" \
    --write-parquet \
    "${{csv_args[@]}}" \
    "${{verbose_args[@]}}"
    ;;
    v551j)
  python3 "$BUILD/compile_v551j_joint_evidence_packets.py" \
    --run-id "$RUN_ID" \
    --v551-atoms-path "$V551_ROOT/relation_evidence_atoms.parquet" \
    --v550j-pattern-index-path "$V550J_DIR/joint_response_pattern_index.parquet" \
    --v550j-meaning-summary-path "$V550J_DIR/joint_pattern_meaning_summary.parquet" \
    --v550j-association-index-path "$V550J_DIR/joint_pattern_association_index.parquet" \
    --v550j-review-surface-path "$V550J_DIR/joint_pattern_association_review_surface.parquet" \
    --emit-review-surface \
    --emit-certified-index \
    --output-root "$COPY_REPO_ROOT/v551j/runs" \
    --write-parquet \
    "${{csv_args[@]}}" \
    "${{strict_args[@]}}" \
    "${{verbose_args[@]}}"
    ;;
    v552)
  python3 "$BUILD/compile_v552_structural_ddm.py" \
    --run-id "$RUN_ID" \
    --atoms-path "$V551_ROOT/relation_evidence_atoms.parquet" \
    --output-root "$COPY_REPO_ROOT/v552/runs" \
    --write-parquet \
    "${{csv_args[@]}}" \
    "${{verbose_args[@]}}"
    ;;
    v552j)
  python3 "$BUILD/compile_v552j_runtime_safe_structural_handoff.py" \
    --run-id "$RUN_ID" \
    --v551j-run-root "$V551J_ROOT" \
    --v551j-comparison-root "$V551J_ROOT" \
    --v552-question-semantic-hierarchy-path "$V552_ROOT/structural/question_semantic_hierarchy.parquet" \
    --v552-structural-channel-index-path "$V552_ROOT/structural/structural_channel_index.parquet" \
    --v552-relation-axis-pressure-path "$V552_ROOT/structural/relation_axis_pressure.parquet" \
    --v552-target-entity-pressure-path "$V552_ROOT/structural/target_entity_pressure.parquet" \
    --v552-driver-facet-pressure-path "$V552_ROOT/structural/driver_facet_pressure.parquet" \
    --v552-contradiction-surface-path "$V552_ROOT/structural/contradiction_surface.parquet" \
    --v552-horizon-constraint-index-path "$V552_ROOT/structural/horizon_constraint_index.parquet" \
    --v552-parent-prior-manifest-path "$V552_ROOT/structural/parent_prior_manifest.parquet" \
    --v552-artifact-authority-index-path "$V552_ROOT/structural/v552_artifact_authority_index.parquet" \
    --v552-known-absence-register-path "$V552_ROOT/structural/v552_known_absence_register.parquet" \
    --v552-structural-fact-index-path "$V552_ROOT/structural/v552_structural_fact_index.parquet" \
    --v552-temporal-key-source-index-path "$V552_ROOT/structural/v552_temporal_key_source_index.parquet" \
    --write-parquet \
    "${{csv_args[@]}}" \
    "${{strict_args[@]}}" \
    "${{verbose_args[@]}}"
    ;;
    *)
    echo "[resolver] wave $task: unknown recovery stage '$stage'" >&2
    return 1
    ;;
  esac

  report_json="$(resolve_report "$task")"
  eval "$(emit_exports "$report_json")"
  local next_stage
  next_stage="$(report_stage_floor "$report_json")"
  if [[ -z "$next_stage" ]]; then
    echo "[resolver] wave $task: recovery complete" >&2
    return 0
  fi
  if [[ "$next_stage" == "$stage" ]]; then
    echo "[resolver] wave $task: stage $stage remains unresolved after one attempt; stopping to avoid repeat loop" >&2
    return 1
  fi
  echo "[resolver] wave $task: completed $stage; next unresolved stage: $next_stage" >&2
  return 0
}}

print_wave_plan

for wave in "${{WAVES[@]}}"; do
  run_recovery_chain_for_task "$wave"
done
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(script, encoding="utf-8")
    path.chmod(0o755)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve usable Rawlsing pipeline lineage and print runnable command blocks.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--source", default=None)
    parser.add_argument("--waves", nargs="*")
    parser.add_argument("--dependency-ledger", default=str(DEFAULT_DEPENDENCY_LEDGER), help="Authored stage dependency ledger to use for required-input contracts.")
    parser.add_argument("--response-option-map", default="data/ddm_build_copy/reports/V550_response_option_map.csv")
    parser.add_argument("--directionality-authority-dir", default="data/ddm_build_copy/directionality_authority")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    parser.add_argument("--report-json", help="Explicit path for the machine-readable lineage report.")
    parser.add_argument("--shell-script-path", help="Explicit path for the generated dynamic shell wrapper.")
    parser.add_argument("--quiet", action="store_true", help="Suppress the printed command block; still write files.")
    parser.add_argument("--emit-v553", action="store_true", help="Also resolve and print a combined V553 block when available.")
    parser.add_argument("--strict", action="store_true", help="Fail if any requested wave cannot be resolved through V552J.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    source_filter = args.source.upper() if args.source and args.source.upper() != "ALL" else None
    dependency_ledger_path = Path(args.dependency_ledger)
    dependency_ledger = _load_dependency_ledger(dependency_ledger_path)
    if args.waves:
        specs: list[tuple[str, str]] = []
        for wave in args.waves:
            if "__" in str(wave):
                specs.append(_normalize_wave_token(wave))
            elif source_filter:
                specs.append((source_filter, str(wave)))
            else:
                print(json.dumps({"error": "source_required_for_bare_waves", "wave": wave, "repo_root": str(repo_root)}), file=sys.stderr)
                return 1
    else:
        if source_filter:
            specs = _discover_wave_specs(repo_root, source_filter=source_filter)
        else:
            specs = _discover_source_wave_pairs(repo_root)
    if not specs:
        print(json.dumps({"error": "no_waves_discovered", "source": source_filter or "ALL", "repo_root": str(repo_root)}), file=sys.stderr)
        return 1
    discovered_sources = sorted({source for source, _wave in specs})
    source_label = discovered_sources[0] if len(discovered_sources) == 1 else "ALL"

    wave_resolutions: list[dict[str, Any]] = []
    command_chunks: list[str] = []
    unresolved: list[str] = []

    for source, wave in specs:
        stages = resolve_stage_roots(repo_root, source, wave)
        stage_floor = _stage_floor(stages)
        task_id = f"{source}__{wave}"
        wave_payload = {
            "source": source,
            "wave": wave,
            "task_id": task_id,
            "resolved": stage_floor == "",
            "first_unresolved_stage": stage_floor,
            "stages": {stage: {"root": res.root, "usable": res.usable, "status": res.status, "reason": res.reason, "metrics": res.metrics} for stage, res in stages.items()},
            "dependency_manifest": _stage_dependency_manifest(source, wave, stages, dependency_ledger),
            "stage_manifests": _stage_manifest_snapshot(source, wave, stages),
        }
        wave_resolutions.append(wave_payload)
        if not all(stages[stage].usable for stage in ("v550", "v550j", "v551", "v551j", "v552", "v552j")):
            unresolved.append(f"{source}__{wave}")
        command_chunks.extend(
            _wave_command_block(
                repo_root=repo_root,
                source=source,
                wave=wave,
                resolutions=stages,
                response_option_map=args.response_option_map,
                directionality_authority_dir=args.directionality_authority_dir,
                env_file=args.env_file,
            )
        )

    combined_v553: StageResolution | None = None
    if args.emit_v553 and len(discovered_sources) == 1:
        combined_v553 = resolve_v553_root(repo_root, discovered_sources[0], [wave for _source, wave in specs])
        if combined_v553.usable:
            command_chunks.extend(
                [
                    f"# Combined V553 resolved root for {'_'.join(wave for _source, wave in specs)}: {combined_v553.root}",
                    "# The resolver records the exact path, but v553 command emission is left to the caller because it requires a wave-spec JSON.",
                    "",
                ]
            )

    command_block = "\n".join(command_chunks).strip() + "\n"
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stamp = created_at.replace(":", "").replace("-", "")
    json_path = Path(args.report_json) if args.report_json else out_dir / f"rawlsing_pipeline_lineage_resolver_{stamp}.json"
    md_path = out_dir / f"rawlsing_pipeline_lineage_resolver_{stamp}.md"
    sh_path = Path(args.shell_script_path) if args.shell_script_path else out_dir / f"rawlsing_pipeline_lineage_resolver_{stamp}.sh"
    report = _build_report(
        repo_root=repo_root,
        source=source_label,
        waves=[f"{source}__{wave}" for source, wave in specs],
        wave_resolutions=wave_resolutions,
        combined_v553=combined_v553,
        command_block=command_block,
        dependency_ledger_path=str(dependency_ledger_path),
        shell_script_path=str(sh_path),
    )
    report["created_at"] = created_at
    _write_json(json_path, report)
    _write_markdown(md_path, report)
    _write_dynamic_shell_script(
        path=sh_path,
        repo_root=repo_root,
        source=source_label,
        waves=[f"{source}__{wave}" for source, wave in specs],
        default_unresolved_waves=unresolved,
        response_option_map=args.response_option_map,
        directionality_authority_dir=args.directionality_authority_dir,
        env_file=args.env_file,
        dependency_ledger_path=str(dependency_ledger_path),
    )

    if args.strict and unresolved:
        resolved = [f"{row['source']}__{row['wave']}" for row in wave_resolutions if f"{row['source']}__{row['wave']}" not in unresolved]
        print(f"RESOLVED_WAVES: {' '.join(resolved)}", file=sys.stderr)
        print(f"UNRESOLVED_WAVES: {' '.join(unresolved)}", file=sys.stderr)
        if args.quiet:
            print(str(json_path))
        else:
            print(json.dumps({"error": "unresolved_waves", "waves": unresolved, "report": str(json_path)}, indent=2), file=sys.stderr)
        return 1

    if args.quiet:
        resolved = [f"{row['source']}__{row['wave']}" for row in wave_resolutions if f"{row['source']}__{row['wave']}" not in unresolved]
        print(f"RESOLVED_WAVES: {' '.join(resolved)}", file=sys.stderr)
        print(f"UNRESOLVED_WAVES: {' '.join(unresolved) if unresolved else '(none)'}", file=sys.stderr)
        print(str(json_path))
    else:
        resolved = [f"{row['source']}__{row['wave']}" for row in wave_resolutions if f"{row['source']}__{row['wave']}" not in unresolved]
        print(f"RESOLVED_WAVES: {' '.join(resolved)}")
        print(f"UNRESOLVED_WAVES: {' '.join(unresolved) if unresolved else '(none)'}")
        run_waves = unresolved or [f"{source}__{wave}" for source, wave in specs]
        print(f"# resolver_report: {json_path}")
        print(f"# resolver_shell_script: {sh_path}")
        print(f"# run_shell: WRITE_CSV=0 VERBOSE=1 STRICT=1 bash {shlex.quote(str(sh_path))} {' '.join(shlex.quote(w) for w in run_waves)}")
        print(command_block.rstrip())
        print()
        print(_format_summary_block(resolved, unresolved, json_path, sh_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
