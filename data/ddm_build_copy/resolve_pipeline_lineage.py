#!/usr/bin/env python3
"""Resolve one coherent Rawlsing producer-run graph, fail closed.

W05 owns orchestration integrity, not stage semantics. This resolver therefore
accepts typed producer boundary state when present and an explicit exact-grammar
legacy adapter for historical manifests. It never infers readiness from row
counts, path names, mtime, or free-text substrings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    DependencyLedgerError,
    boundary_state_from_payload,
    inspect_artifact,
    read_status_document,
    verify_external_dependency_ledger,
)

DEFAULT_DEPENDENCY_LEDGER: Path | None = None
STAGE_ORDER = ("v550", "v550j", "v551", "v551j", "v552", "v552j")


@dataclass(frozen=True)
class StageResolution:
    stage: str
    root: str
    usable: bool
    status: str
    reason: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sanitize_task_token(task: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(task or "").strip())
    return token.strip("_") or "task"


def _normalize_wave_token(token: str, *, source_hint: str | None = None) -> tuple[str, str]:
    text = str(token or "").strip()
    if "__" in text:
        source, wave = text.split("__", 1)
        if source.strip() and wave.strip():
            return source.strip().upper(), wave.strip()
    if source_hint and text:
        return source_hint.strip().upper(), text
    raise ValueError(f"Unable to infer source for wave token: {token!r}")


def _read_json(path: Path) -> dict[str, Any]:
    doc = read_status_document(path)
    return doc.payload if doc.exists and doc.readable else {}


def _load_dependency_ledger(path: Path | None, expected_sha256: str = "") -> dict[str, Any] | None:
    """Load only an explicitly supplied, hash-pinned external ledger.

    The old default pointed to a file absent from both audited source trees.
    A normal resolver invocation therefore has no fake default dependency.
    """
    if path is None:
        return None
    return verify_external_dependency_ledger(path, expected_sha256)


def _stage_status(root: Path, status_paths: Iterable[str], ready_key_names: Iterable[str]) -> tuple[bool, str, str]:
    paths = tuple(status_paths)
    if not paths:
        return False, "", "required status contract not declared"
    failures: list[str] = []
    for rel in paths:
        doc = read_status_document(root / rel)
        if not doc.exists:
            failures.append(f"missing:{rel}")
            continue
        if not doc.readable:
            failures.append(f"unreadable:{rel}:{doc.error}")
            continue
        try:
            state = boundary_state_from_payload(doc.payload, tuple(ready_key_names))
        except BoundaryContractError as exc:
            failures.append(f"invalid:{rel}:{exc}")
            continue
        status = state.source or "/".join(
            (state.run_integrity_status, state.evidence_status, state.downstream_permission_status)
        )
        if not state.permits_downstream:
            return False, status, f"producer boundary does not permit downstream: {rel}"
        return True, status, ""
    return False, "", "required readiness/integrity unverifiable: " + ";".join(failures)


def _validate_root(
    root: Path,
    *,
    stage: str,
    required_files: tuple[str, ...],
    required_nonempty_files: tuple[str, ...] = (),
    status_paths: tuple[str, ...] = (),
    ready_key_names: tuple[str, ...] = (),
) -> StageResolution:
    if not root.is_dir():
        return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"missing exact run root: {root}")

    metrics: dict[str, Any] = {}
    for rel in required_files:
        inspected = inspect_artifact(root / rel)
        if not inspected.exists:
            return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"missing required file: {rel}")
        if not inspected.readable:
            return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"unreadable required file: {rel}: {inspected.error}")
        metrics[rel] = {
            "row_count": inspected.row_count,
            "artifact_file_sha256": inspected.artifact_file_sha256,
            "valid_empty": inspected.valid_empty,
        }

    # Phase A preserves legacy operation-specific nonempty requirements while
    # making corruption distinct from lawful zero rows. Generic cardinality
    # semantics close later under LIN-001..004 after stage hooks merge.
    for rel in required_nonempty_files:
        inspected = inspect_artifact(root / rel)
        if not inspected.exists or not inspected.readable:
            return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"unreadable required evidence: {rel}: {inspected.error}")
        if inspected.row_count is not None and inspected.row_count <= 0:
            return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"empty required evidence: {rel}")

    ok, status, reason = _stage_status(root, status_paths, ready_key_names)
    if not ok:
        return StageResolution(stage, "", False, status or "BLOCKED_OR_MISSING", reason, metrics)
    return StageResolution(stage, str(root), True, status, metrics=metrics)


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
    """Compatibility helper for tests and legacy callers.

    Candidate ranking may find a first-stage producer, but status is always
    fail-closed and unreadable Parquet is never represented as zero rows.
    Run-coupled downstream stages do not use this helper.
    """
    del reject_blocked, require_ready
    if not base.exists():
        return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", f"base missing: {base}")
    candidates = [path for path in base.glob(f"**/{pattern}") if path.is_dir()]
    candidates.sort(key=lambda p: (p.stat().st_mtime_ns, -len(p.parts), str(p)), reverse=True)
    best = f"no candidate matched {pattern}"
    for root in candidates:
        resolved = _validate_root(
            root,
            stage=stage,
            required_files=required_files,
            required_nonempty_files=required_nonempty_files,
            status_paths=status_paths,
            ready_key_names=ready_key_names,
        )
        if resolved.usable:
            return resolved
        best = resolved.reason
    return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", best)


def _discover_source_wave_pairs(repo_root: Path) -> list[tuple[str, str]]:
    shard_root = repo_root / "data/ddm_repository_copy/v550/shard_runs"
    found: set[tuple[str, str]] = set()
    if not shard_root.exists():
        return []
    for path in shard_root.glob("*/*"):
        if path.is_dir() and "__" in path.name:
            source, wave = path.name.split("__", 1)
            if source and wave:
                found.add((source.upper(), wave))
    return sorted(found)


def _discover_wave_specs(repo_root: Path, source_filter: str | None = None) -> list[tuple[str, str]]:
    rows = _discover_source_wave_pairs(repo_root)
    return [row for row in rows if not source_filter or row[0] == source_filter.upper()]


def _extract_run_id_from_v550_root(root: str) -> str:
    path = Path(root)
    return path.parent.name if root else ""


def resolve_stage_roots(repo_root: str | Path, source: str, wave: str) -> dict[str, StageResolution]:
    repo = Path(repo_root)
    source_upper = source.upper()
    shard_id = f"{source_upper}__{wave}"

    v550 = _latest_usable_candidate(
        repo / "data/ddm_repository_copy/v550/shard_runs",
        shard_id,
        stage="v550",
        required_files=("shard_status.json", "shard_scope.parquet", "bridge/v551_bridge_index.parquet", "core/question_use_contract.parquet"),
        required_nonempty_files=("bridge/v551_bridge_index.parquet", "core/question_use_contract.parquet"),
        status_paths=("shard_status.json",),
        ready_key_names=("status", "final_status", "readiness_status"),
    )
    if not v550.usable:
        return {"v550": v550, **{stage: StageResolution(stage, "", False, "BLOCKED_UPSTREAM", "v550 unresolved") for stage in STAGE_ORDER[1:]}}

    run_id = _extract_run_id_from_v550_root(v550.root)
    # Critical invariant: every run-coupled stage is resolved from this exact
    # selected V550 run ID; no source/wave-wide newest-by-mtime V550J search.
    v550j = _validate_root(
        repo / "data/ddm_repository_copy/v550j/runs" / run_id,
        stage="v550j",
        required_files=(
            f"{shard_id}/joint_patterns/joint_response_pattern_index.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_meaning_summary.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_association_index.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_association_review_surface.parquet",
            f"{shard_id}/joint_patterns/v550j_source_wave_readiness_report.json",
        ),
        required_nonempty_files=(
            f"{shard_id}/joint_patterns/joint_response_pattern_index.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_meaning_summary.parquet",
            f"{shard_id}/joint_patterns/joint_pattern_association_index.parquet",
        ),
        status_paths=(f"{shard_id}/joint_patterns/v550j_source_wave_readiness_report.json",),
        ready_key_names=("readiness_status", "final_status", "status"),
    )

    exact = {
        "v551": _validate_root(
            repo / "data/ddm_repository_copy/v551/runs" / run_id,
            stage="v551",
            required_files=("manifest.json", "relation_evidence_atoms.parquet", "relation_review_surface.parquet", "exclusion_summary.parquet", "numeric_wrapper_audit.parquet"),
            required_nonempty_files=("relation_evidence_atoms.parquet",),
            status_paths=("manifest.json",),
            ready_key_names=("status", "final_status", "readiness_status"),
        ),
        "v551j": _validate_root(
            repo / "data/ddm_repository_copy/v551j/runs" / run_id,
            stage="v551j",
            required_files=("manifest/v551j_certification_readiness_report.json", "manifest/v551j_review_readiness_report.json", "manifest/v551j_input_provenance_manifest.json", "packets/v551j_certified_packet_index.parquet", "packets/v551j_reviewable_evidence_sidecar.parquet"),
            required_nonempty_files=("packets/v551j_certified_packet_index.parquet", "packets/v551j_reviewable_evidence_sidecar.parquet"),
            status_paths=("manifest/v551j_certification_readiness_report.json",),
            ready_key_names=("final_status", "status"),
        ),
        "v552": _validate_root(
            repo / "data/ddm_repository_copy/v552/runs" / run_id,
            stage="v552",
            required_files=("manifest/v552_readiness_report.parquet", "manifest/v552_input_provenance_manifest.json", "structural/question_semantic_hierarchy.parquet", "structural/v552_structural_fact_index.parquet"),
            required_nonempty_files=("structural/v552_structural_fact_index.parquet", "structural/question_semantic_hierarchy.parquet"),
            status_paths=("manifest/v552_readiness_report.parquet",),
            ready_key_names=("status", "final_status", "readiness_status"),
        ),
        "v552j": _validate_root(
            repo / "data/ddm_repository_copy/v552j/runs" / run_id,
            stage="v552j",
            required_files=("manifest/v552j_readiness_report.json", "manifest/v552j_runtime_handoff_manifest.json", "manifest/v552j_v553_handoff_manifest.json", "packets/v552j_structural_handoff_packet.json", "packets/v552j_v553_input_index.parquet", "packets/v552j_to_v553_handoff_index.parquet"),
            required_nonempty_files=("packets/v552j_v553_input_index.parquet", "packets/v552j_to_v553_handoff_index.parquet"),
            status_paths=("manifest/v552j_readiness_report.json",),
            ready_key_names=("status", "final_status", "readiness_status"),
        ),
    }
    return {"v550": v550, "v550j": v550j, **exact}


def _stage_floor(stages: dict[str, StageResolution]) -> str:
    return next((stage for stage in STAGE_ORDER if not stages[stage].usable), "")


def _stage_dependency_manifest(source: str, wave: str, stages: dict[str, StageResolution], dependency_ledger: dict[str, Any] | None) -> dict[str, Any]:
    if dependency_ledger is None:
        return {"source": source, "wave": wave, "external_dependency_ledger": "NOT_SUPPLIED", "recovery_commands_enabled": False}
    run_id = _extract_run_id_from_v550_root(stages["v550"].root)
    context = {
        "repo_root": str(ROOT), "source_upper": source.upper(), "source_lower": source.lower(), "source": source.upper(),
        "wave": wave, "shard_id": f"{source.upper()}__{wave}", "run_id": run_id,
        **{f"{stage}_root": stages[stage].root for stage in STAGE_ORDER},
    }
    out: dict[str, Any] = {"source": source, "wave": wave, "recovery_commands_enabled": True}
    for stage, cfg in dependency_ledger.get("stages", {}).items():
        if not isinstance(cfg, dict):
            continue
        paths: list[str] = []
        for item in cfg.get("required_inputs", []):
            if not isinstance(item, dict):
                continue
            template = str(item.get("path_template") or item.get("path") or "")
            if template:
                try:
                    paths.append(template.format(**context))
                except Exception:
                    paths.append(template)
        out[stage] = {"required_inputs": paths, "entrypoint": cfg.get("entrypoint", "")}
    return out


def _wave_command_block(source: str, wave: str, stages: dict[str, StageResolution]) -> list[str]:
    floor = _stage_floor(stages)
    run_id = _extract_run_id_from_v550_root(stages["v550"].root)
    return [
        f"# {source} {wave}",
        f"# coherent producer run_id: {run_id or '(unresolved)'}",
        f"# first unresolved stage: {floor or '(none)'}",
        "# Exact recovery commands require an explicitly hash-verified external dependency ledger.",
        "",
    ]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = ["# Rawlsing Pipeline Lineage Resolver", "", f"- Created: `{report['created_at']}`", f"- Dependency ledger: `{report['dependency_ledger_status']}`", "", "| Task | First unresolved | Producer run |", "| --- | --- | --- |"]
    for row in report["wave_resolutions"]:
        run_id = _extract_run_id_from_v550_root(row["stages"]["v550"]["root"])
        lines.append(f"| {row['task_id']} | {row['first_unresolved_stage'] or 'resolved'} | {run_id or 'unresolved'} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resolve one coherent Rawlsing producer-run graph.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--source", default=None)
    parser.add_argument("--waves", nargs="*")
    parser.add_argument("--dependency-ledger", default=None, help="Optional external recovery ledger; requires --dependency-ledger-sha256.")
    parser.add_argument("--dependency-ledger-sha256", default="", help="Expected SHA-256 for an explicitly supplied external dependency ledger.")
    parser.add_argument("--output-dir", default=str(ROOT / "docs/architecture_control/reports"))
    parser.add_argument("--report-json")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    source_filter = args.source.upper() if args.source and args.source.upper() != "ALL" else None
    ledger_path = Path(args.dependency_ledger) if args.dependency_ledger else None
    try:
        dependency_ledger = _load_dependency_ledger(ledger_path, args.dependency_ledger_sha256)
    except (DependencyLedgerError, OSError, ValueError) as exc:
        print(json.dumps({"error": "DEPENDENCY_LEDGER_INVALID", "detail": str(exc)}), file=sys.stderr)
        return 2

    if args.waves:
        try:
            specs = [_normalize_wave_token(wave, source_hint=source_filter) for wave in args.waves]
        except ValueError as exc:
            print(json.dumps({"error": "wave_parse_failed", "detail": str(exc)}), file=sys.stderr)
            return 2
    else:
        specs = _discover_wave_specs(repo_root, source_filter)
    if not specs:
        print(json.dumps({"error": "no_waves_discovered", "repo_root": str(repo_root)}), file=sys.stderr)
        return 1

    rows: list[dict[str, Any]] = []
    command_chunks: list[str] = []
    unresolved: list[str] = []
    for source, wave in specs:
        stages = resolve_stage_roots(repo_root, source, wave)
        floor = _stage_floor(stages)
        task_id = f"{source}__{wave}"
        if floor:
            unresolved.append(task_id)
        rows.append({
            "source": source, "wave": wave, "task_id": task_id, "resolved": not floor,
            "first_unresolved_stage": floor,
            "stages": {name: {"root": r.root, "usable": r.usable, "status": r.status, "reason": r.reason, "metrics": r.metrics} for name, r in stages.items()},
            "dependency_manifest": _stage_dependency_manifest(source, wave, stages, dependency_ledger),
        })
        command_chunks.extend(_wave_command_block(source, wave, stages))

    created = utc_now()
    out_dir = Path(args.output_dir)
    stamp = re.sub(r"[^0-9]", "", created)[:14]
    json_path = Path(args.report_json) if args.report_json else out_dir / f"rawlsing_pipeline_lineage_resolver_{stamp}.json"
    md_path = out_dir / f"rawlsing_pipeline_lineage_resolver_{stamp}.md"
    report = {
        "schema": "rawlsing_pipeline_lineage_resolver_v2",
        "repo_root": str(repo_root), "created_at": created,
        "source": source_filter or "ALL", "waves": [f"{s}__{w}" for s, w in specs],
        "dependency_ledger_status": "VERIFIED_EXTERNAL" if dependency_ledger is not None else "NOT_REQUIRED_FOR_READ_ONLY_RESOLUTION",
        "dependency_ledger_path": str(ledger_path) if ledger_path else "",
        "dependency_ledger_sha256": args.dependency_ledger_sha256.lower() if ledger_path else "",
        "resolved_waves": [r["task_id"] for r in rows if r["resolved"]],
        "unresolved_waves": unresolved,
        "command_block": "\n".join(command_chunks),
        "wave_resolutions": rows,
    }
    _write_json(json_path, report)
    _write_markdown(md_path, report)

    if not args.quiet:
        print(f"RESOLVED_WAVES: {' '.join(report['resolved_waves']) or '(none)'}")
        print(f"UNRESOLVED_WAVES: {' '.join(unresolved) or '(none)'}")
        print(f"# resolver_report: {json_path}")
        print(report["command_block"].rstrip())
    else:
        print(str(json_path))
    return 1 if args.strict and unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
