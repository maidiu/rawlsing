#!/usr/bin/env python3
"""Resolve V550→V552J lineage from producer manifests and governed UID identity.

No source/wave identity is reconstructed from filenames.  A requested
source/wave is resolved once through the W01 catalog, V550 candidates are
selected by manifest UID coherence, and every downstream stage is bound to the
exact producer run/country/shard plus the same UID pair.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_consumer import ProducerBoundaryVerification
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    inspect_artifact,
    read_status_document,
    verify_exact_identity,
    verify_frame_source_wave_identity_coherence,
    verify_manifest_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_pipeline_final_contracts import (
    state_token,
    verify_v550j_producer_manifest,
    verify_v551_producer_manifest,
    verify_v551j_producer_manifest,
    verify_v552_producer_manifest,
    verify_v552j_producer_manifest,
)
from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentity,
    SourceWaveIdentityError,
    closed_35_identities,
    resolve_source_family_identity,
    resolve_source_wave_identity,
)
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import COMPILER_SPECS


@dataclass(frozen=True)
class StageResolution:
    stage: str
    root: str
    usable: bool
    status: str
    reason: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"", "nan", "none", "null", "unknown", "unresolved"} else text


def _blocked(stage: str, reason: str, **metrics: Any) -> StageResolution:
    return StageResolution(stage, "", False, "BLOCKED_OR_MISSING", reason, metrics)


def _verified(stage: str, root: Path, verified: ProducerBoundaryVerification) -> StageResolution:
    payload = verified.manifest_payload
    return StageResolution(
        stage=stage,
        root=str(root),
        usable=True,
        status=state_token(verified),
        metrics={
            "manifest_path": verified.manifest_path,
            "contract_version": verified.state.contract_version,
            "schema_version": _clean(payload.get("schema_version")),
            "compiler_version": _clean(payload.get("compiler_version")),
            "run_integrity_status": verified.state.run_integrity_status,
            "evidence_status": verified.state.evidence_status,
            "downstream_permission_status": verified.state.downstream_permission_status,
            "identity": dict(verified.identity),
        },
    )


def _verified_resolution(stage: str, root: Path, verified: ProducerBoundaryVerification) -> StageResolution:
    """Backward-compatible name for typed producer verification."""
    return _verified(stage, root, verified)


def _payload(path: Path) -> dict[str, Any]:
    document = read_status_document(path)
    if not document.exists or not document.readable:
        return {}
    return dict(document.payload)


def _manifest_mtime(path: Path) -> int:
    try:
        return int(path.stat().st_mtime_ns)
    except Exception:
        return 0


def _v550_manifest_paths(repo: Path) -> list[Path]:
    base = repo / "data/ddm_repository_copy/v550/shard_runs"
    if not base.exists():
        return []
    # Structural location is known; source/wave/run identity is read from bytes.
    paths = list(base.glob("*/*/manifest.json")) + list(base.glob("*/*/shard_manifest.json"))
    unique = {str(path.resolve()): path for path in paths if path.is_file()}
    return sorted(unique.values(), key=_manifest_mtime, reverse=True)


def _v550_candidate(
    manifest_path: Path,
    identity: SourceWaveIdentity,
) -> tuple[StageResolution | None, dict[str, str] | None, str]:
    payload = _payload(manifest_path)
    if not payload:
        return None, None, "manifest_unreadable"
    try:
        coherence = verify_manifest_source_wave_identity_coherence(
            payload,
            expected_source_family_uid=identity.source_family_uid,
            expected_wave_uid=identity.wave_uid,
        )
    except BoundaryContractError as exc:
        # Other governed source/wave objects are ordinary nonmatches.  A
        # contradictory object that claims either requested UID is fail-closed.
        claimed_source_uid = _clean(payload.get("source_family_uid"))
        claimed_wave_uid = _clean(payload.get("wave_uid"))
        if claimed_source_uid == identity.source_family_uid or claimed_wave_uid == identity.wave_uid:
            return None, None, f"contradictory_requested_uid_manifest:{exc}"
        return None, None, "different_uid"

    if coherence.source_family_uid != identity.source_family_uid or coherence.wave_uid != identity.wave_uid:
        return None, None, "different_uid"
    run_id = _clean(payload.get("run_id") or payload.get("producer_run_id"))
    shard_id = _clean(payload.get("shard_id"))
    if not run_id or not shard_id:
        return None, None, "v550_manifest_missing_run_or_shard"
    try:
        exact = verify_exact_identity(
            payload,
            run_id=run_id,
            shard_id=shard_id,
            source_family_uid=identity.source_family_uid,
            wave_uid=identity.wave_uid,
        )
    except BoundaryContractError as exc:
        return None, None, f"v550_exact_identity_invalid:{exc}"
    if payload.get("success") is not True:
        return None, None, "v550_manifest_success_not_true"

    root = manifest_path.parent
    required = (
        root / "bridge/v551_bridge_index.parquet",
        root / "core/question_use_contract.parquet",
    )
    for path in required:
        inspection = inspect_artifact(path)
        if not inspection.exists or not inspection.readable:
            return None, None, f"v550_required_artifact_unreadable:{path.name}:{inspection.error}"
        if inspection.row_count is not None and inspection.row_count <= 0:
            return None, None, f"v550_required_artifact_empty:{path.name}"
    metrics = {
        "manifest_path": str(manifest_path),
        "run_id": run_id,
        "shard_id": shard_id,
        "identity": {
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
            "source": coherence.canonical_display_source,
            "wave": coherence.canonical_display_wave,
        },
    }
    return StageResolution("v550", str(root), True, "PASS", metrics=metrics), exact, ""


def _resolve_v550(repo: Path, identity: SourceWaveIdentity) -> StageResolution:
    first_error = ""
    for manifest in _v550_manifest_paths(repo):
        resolution, _, reason = _v550_candidate(manifest, identity)
        if resolution is not None:
            return resolution
        if reason.startswith("contradictory_requested_uid_manifest"):
            return _blocked("v550", reason)
        if reason not in {"different_uid", "manifest_unreadable"} and not first_error:
            first_error = reason
    return _blocked(
        "v550",
        first_error or f"no usable V550 manifest matched UID {identity.uid_key}",
        source_family_uid=identity.source_family_uid,
        wave_uid=identity.wave_uid,
    )


def _bridge_scope(v550: StageResolution, identity: SourceWaveIdentity) -> dict[str, str]:
    bridge_path = Path(v550.root) / "bridge/v551_bridge_index.parquet"
    frame = pd.read_parquet(bridge_path)
    coherence = verify_frame_source_wave_identity_coherence(
        frame,
        expected_source_family_uid=identity.source_family_uid,
        expected_wave_uid=identity.wave_uid,
        allow_empty=False,
    )
    run_ids = sorted({_clean(value) for value in frame.get("run_id", pd.Series(dtype=str)).tolist() if _clean(value)})
    shard_ids = sorted({_clean(value) for value in frame.get("shard_id", pd.Series(dtype=str)).tolist() if _clean(value)})
    countries = sorted({_clean(value) for value in frame.get("country_code", pd.Series(dtype=str)).tolist() if _clean(value)})
    manifest_run = _clean(v550.metrics.get("run_id"))
    manifest_shard = _clean(v550.metrics.get("shard_id"))
    if run_ids != [manifest_run]:
        raise BoundaryContractError(f"V550_BRIDGE_RUN_ID_MISMATCH:manifest={manifest_run}:bridge={run_ids}")
    if shard_ids and shard_ids != [manifest_shard]:
        raise BoundaryContractError(f"V550_BRIDGE_SHARD_ID_MISMATCH:manifest={manifest_shard}:bridge={shard_ids}")
    if len(countries) > 1:
        raise BoundaryContractError(f"V550_BRIDGE_COUNTRY_NOT_SINGULAR:{countries}")
    return {
        "run_id": manifest_run,
        "shard_id": manifest_shard,
        "country_code": countries[0] if countries else "",
        "source_family_uid": coherence["source_family_uid"],
        "wave_uid": coherence["wave_uid"],
        "source": identity.canonical_display_source,
        "wave": identity.canonical_display_wave,
        "bridge_path": str(bridge_path),
    }


def _same_run_payload(path: Path, run_id: str) -> bool:
    payload = _payload(path)
    if not payload:
        return False
    values = {
        _clean(payload.get("run_id")),
        _clean(payload.get("producer_run_id")),
    } - {""}
    return run_id in values


def _one_verified_candidate(
    *,
    stage: str,
    manifests: Iterable[Path],
    run_id: str,
    verify: Callable[[Path], ProducerBoundaryVerification],
    root_from_manifest: Callable[[Path], Path],
) -> StageResolution:
    same_run = [path for path in manifests if path.is_file() and _same_run_payload(path, run_id)]
    if not same_run:
        return _blocked(stage, f"no manifest with exact run_id={run_id}")
    same_run.sort(key=_manifest_mtime, reverse=True)
    errors: list[str] = []
    for path in same_run:
        try:
            verified = verify(path)
        except BoundaryContractError as exc:
            errors.append(f"{path}:{exc}")
            continue
        return _verified(stage, root_from_manifest(path), verified)
    return _blocked(stage, f"same-run manifest(s) failed exact boundary:{';'.join(errors)}")


def _stage_manifest_sets(repo: Path) -> dict[str, list[Path]]:
    roots = repo / "data/ddm_repository_copy"
    return {
        "v550j": list((roots / "v550j/runs").glob("*/*/joint_patterns/v550j_manifest.json")),
        "v551": list((roots / "v551/runs").glob("*/manifest.json")),
        "v551j": list((roots / "v551j/runs").glob("*/manifest/manifest.json")),
        "v552": list((roots / "v552/runs").glob("*/manifest.json")),
        "v552j": list((roots / "v552j/runs").glob("*/manifest.json")),
    }


def resolve_stage_roots(repo_root: str | Path, source: str, wave: str) -> dict[str, StageResolution]:
    repo = Path(repo_root)
    try:
        identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    except SourceWaveIdentityError as exc:
        blocked = _blocked("v550", f"source_wave_identity_invalid:{exc}")
        return {stage: blocked if stage == "v550" else _blocked(stage, "V550_NOT_USABLE") for stage in ("v550", "v550j", "v551", "v551j", "v552", "v552j")}

    v550 = _resolve_v550(repo, identity)
    stages: dict[str, StageResolution] = {"v550": v550}
    if not v550.usable:
        for stage in ("v550j", "v551", "v551j", "v552", "v552j"):
            stages[stage] = _blocked(stage, "selected V550 producer is not usable")
        return stages

    try:
        scope = _bridge_scope(v550, identity)
    except Exception as exc:
        for stage in ("v550j", "v551", "v551j", "v552", "v552j"):
            stages[stage] = _blocked(stage, f"V550_BRIDGE_IDENTITY_INVALID:{type(exc).__name__}:{exc}")
        return stages

    manifests = _stage_manifest_sets(repo)
    run_id = scope["run_id"]
    shard_id = scope["shard_id"]
    country = scope["country_code"]
    source_label = identity.canonical_display_source
    wave_label = identity.canonical_display_wave
    bridge_path = Path(scope["bridge_path"])

    def v550j_verify(path: Path) -> ProducerBoundaryVerification:
        readiness = path.with_name("v550j_source_wave_readiness_report.json")
        return verify_v550j_producer_manifest(
            path,
            readiness,
            run_id=run_id,
            source=source_label,
            wave=wave_label,
            shard_id=shard_id,
        )

    stages["v550j"] = _one_verified_candidate(
        stage="v550j",
        manifests=manifests["v550j"],
        run_id=run_id,
        verify=v550j_verify,
        root_from_manifest=lambda path: path.parent,
    )

    def v551_verify(path: Path) -> ProducerBoundaryVerification:
        return verify_v551_producer_manifest(
            path,
            run_id=run_id,
            source=source_label,
            wave=wave_label,
            country_code=country,
            shard_id=shard_id,
            bridge_path=bridge_path,
        )

    stages["v551"] = _one_verified_candidate(
        stage="v551",
        manifests=manifests["v551"],
        run_id=run_id,
        verify=v551_verify,
        root_from_manifest=lambda path: path.parent,
    )
    v551_manifest = Path(stages["v551"].metrics.get("manifest_path") or "")

    if stages["v551"].usable:
        def v552_verify(path: Path) -> ProducerBoundaryVerification:
            return verify_v552_producer_manifest(
                path,
                run_id=run_id,
                source=source_label,
                wave=wave_label,
                country_code=country,
                shard_id=shard_id,
                v551_manifest_path=v551_manifest,
            )

        stages["v552"] = _one_verified_candidate(
            stage="v552",
            manifests=manifests["v552"],
            run_id=run_id,
            verify=v552_verify,
            root_from_manifest=lambda path: path.parent,
        )
    else:
        stages["v552"] = _blocked("v552", "V551_NOT_USABLE")
    v552_manifest = Path(stages["v552"].metrics.get("manifest_path") or "")

    v550j_manifest = Path(stages["v550j"].metrics.get("manifest_path") or "")
    if stages["v551"].usable and stages["v550j"].usable:
        def v551j_verify(path: Path) -> ProducerBoundaryVerification:
            return verify_v551j_producer_manifest(
                path,
                run_id=run_id,
                source=source_label,
                wave=wave_label,
                country_code=country,
                shard_id=shard_id,
                v551_manifest_path=v551_manifest,
                v550j_manifest_path=v550j_manifest,
            )

        stages["v551j"] = _one_verified_candidate(
            stage="v551j",
            manifests=manifests["v551j"],
            run_id=run_id,
            verify=v551j_verify,
            root_from_manifest=lambda path: path.parent.parent,
        )
    else:
        stages["v551j"] = _blocked("v551j", "V551_OR_V550J_NOT_USABLE")
    v551j_manifest = Path(stages["v551j"].metrics.get("manifest_path") or "")

    if stages["v551j"].usable and stages["v552"].usable:
        def v552j_verify(path: Path) -> ProducerBoundaryVerification:
            return verify_v552j_producer_manifest(
                path,
                run_id=run_id,
                source=source_label,
                wave=wave_label,
                country_code=country,
                shard_id=shard_id,
                v551j_manifest_path=v551j_manifest,
                v552_manifest_path=v552_manifest,
            )

        stages["v552j"] = _one_verified_candidate(
            stage="v552j",
            manifests=manifests["v552j"],
            run_id=run_id,
            verify=v552j_verify,
            root_from_manifest=lambda path: path.parent,
        )
    else:
        stages["v552j"] = _blocked("v552j", "V551J_OR_V552_NOT_USABLE")

    # Machine identity is explicit in every usable stage resolution.
    for stage, resolution in list(stages.items()):
        if not resolution.usable:
            continue
        metrics = dict(resolution.metrics)
        stage_identity = dict(metrics.get("identity") or {})
        stage_identity.setdefault("source_family_uid", identity.source_family_uid)
        stage_identity.setdefault("wave_uid", identity.wave_uid)
        metrics["identity"] = stage_identity
        stages[stage] = StageResolution(
            stage=resolution.stage,
            root=resolution.root,
            usable=resolution.usable,
            status=resolution.status,
            reason=resolution.reason,
            metrics=metrics,
        )
    return stages


def _discover_wave_specs(repo_root: Path, source_filter: str | None = None) -> list[tuple[str, str]]:
    del repo_root  # discovery is catalog-governed, not filesystem-name-governed
    source_uid = ""
    if source_filter:
        source_uid = resolve_source_family_identity(source_filter).source_family_uid
    rows = [
        (identity.canonical_display_source, identity.canonical_display_wave)
        for identity in closed_35_identities()
        if not source_uid or identity.source_family_uid == source_uid
    ]
    return sorted(rows)


def _stage_floor(stages: dict[str, StageResolution]) -> str:
    for stage in ("v550", "v550j", "v551", "v551j", "v552", "v552j"):
        if not stages[stage].usable:
            return stage
    return ""


def _as_dict(resolution: StageResolution) -> dict[str, Any]:
    return {
        "stage": resolution.stage,
        "root": resolution.root,
        "usable": resolution.usable,
        "status": resolution.status,
        "reason": resolution.reason,
        "metrics": resolution.metrics,
    }


def _wave_row(source: str, wave: str, stages: dict[str, StageResolution]) -> dict[str, Any]:
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    v550_metrics = stages["v550"].metrics if stages["v550"].usable else {}
    return {
        "source": identity.canonical_display_source,
        "wave": identity.canonical_display_wave,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "task_id": identity.uid_key,
        "legacy_task_label": f"{identity.canonical_display_source}|{identity.canonical_display_wave}",
        "run_id": _clean(v550_metrics.get("run_id")),
        "shard_id": _clean(v550_metrics.get("shard_id")),
        "first_unresolved_stage": _stage_floor(stages),
        "base_spine_ready": all(stages[name].usable for name in ("v550", "v551", "v552")),
        "j_branch_traversed": all(stages[name].usable for name in ("v550j", "v551j", "v552j")),
        "stages": {name: _as_dict(value) for name, value in stages.items()},
    }


def _command_block(repo_root: Path, row: dict[str, Any], *, response_option_map: str, env_file: str) -> list[str]:
    stages = row["stages"]
    if not stages["v550"]["usable"]:
        return [f"# {row['legacy_task_label']}: V550 unresolved; no downstream replay command is safe."]
    run_id = row["run_id"]
    shard_id = row["shard_id"]
    build = repo_root / "data/ddm_build_copy"
    copy = repo_root / "data/ddm_repository_copy"
    v550_root = Path(stages["v550"]["root"])
    v550j_joint = Path(stages["v550j"]["root"]) if stages["v550j"]["root"] else copy / "v550j/runs" / run_id / shard_id / "joint_patterns"
    v551_root = Path(stages["v551"]["root"]) if stages["v551"]["root"] else copy / "v551/runs" / run_id
    v551j_root = Path(stages["v551j"]["root"]) if stages["v551j"]["root"] else copy / "v551j/runs" / run_id
    v552_root = Path(stages["v552"]["root"]) if stages["v552"]["root"] else copy / "v552/runs" / run_id
    compiler = {stage: build / Path(rel).name for stage, rel in COMPILER_SPECS.items()}
    return [
        f"# UID task {row['task_id']} ({row['legacy_task_label']})",
        f"RUN_ID={shlex.quote(run_id)}",
        f"SHARD_ID={shlex.quote(shard_id)}",
        f"V550_ROOT={shlex.quote(str(v550_root))}",
        f"V550J_JOINT={shlex.quote(str(v550j_joint))}",
        f"V551_ROOT={shlex.quote(str(v551_root))}",
        f"V551J_ROOT={shlex.quote(str(v551j_root))}",
        f"V552_ROOT={shlex.quote(str(v552_root))}",
        f"RESPONSE_OPTION_MAP={shlex.quote(response_option_map)}",
        f"ENV_FILE={shlex.quote(env_file)}",
        "",
        "# Invoke only the first unresolved stage; every path above came from manifest-bound lineage.",
        f"# first_unresolved_stage={row['first_unresolved_stage'] or 'none'}",
        f"# v550j: python3 {shlex.quote(str(compiler['v550j']))} --v550-shard-dir \"$V550_ROOT\" --output-root {shlex.quote(str(copy/'v550j'))} --registry-path \"$QUESTION_FAMILY_REGISTRY\" --response-option-map \"$RESPONSE_OPTION_MAP\" --env-file \"$ENV_FILE\" --write-parquet --no-write-csv",
        f"# v551: python3 {shlex.quote(str(compiler['v551']))} --run-id \"$RUN_ID\" --bridge-path \"$V550_ROOT/bridge/v551_bridge_index.parquet\" --output-root {shlex.quote(str(copy/'v551'))} --v551-compile-mode canonical --write-parquet --no-write-csv",
        f"# v552: python3 {shlex.quote(str(compiler['v552']))} --run-id \"$RUN_ID\" --v551-manifest-path \"$V551_ROOT/manifest.json\" --output-root {shlex.quote(str(copy/'v552'))} --strict-handoff --write-parquet --no-write-csv",
        f"# v551j: python3 {shlex.quote(str(compiler['v551j']))} --run-id \"$RUN_ID\" --v551-atoms-path \"$V551_ROOT/relation_evidence_atoms.parquet\" --v551-manifest-path \"$V551_ROOT/manifest.json\" --v550j-pattern-index-path \"$V550J_JOINT/joint_response_pattern_index.parquet\" --v550j-pattern-item-index-path \"$V550J_JOINT/joint_response_pattern_item_index.parquet\" --v550j-relation-signature-path \"$V550J_JOINT/joint_pattern_relation_signature.parquet\" --v550j-manifest-path \"$V550J_JOINT/v550j_manifest.json\" --v550j-readiness-report-path \"$V550J_JOINT/v550j_source_wave_readiness_report.json\" --registry-path \"$QUESTION_FAMILY_REGISTRY\" --output-root {shlex.quote(str(copy/'v551j'))} --emit-review-surface --emit-certified-index --strict --write-parquet --no-write-csv",
        f"# v552j: python3 {shlex.quote(str(compiler['v552j']))} --run-id \"$RUN_ID\" --v551j-manifest-path \"$V551J_ROOT/manifest/manifest.json\" --v552-manifest-path \"$V552_ROOT/manifest.json\" --output-root {shlex.quote(str(copy/'v552j'))} --write-parquet --no-write-csv",
    ]


def _write_shell(path: Path, report_path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"""#!/usr/bin/env bash
set -euo pipefail
REPORT={shlex.quote(str(report_path))}
python3 - "$REPORT" <<'PY'
import json,sys
r=json.load(open(sys.argv[1], encoding='utf-8'))
for row in r['wave_resolutions']:
    print(f"# {{row['task_id']}} first_unresolved={{row['first_unresolved_stage'] or 'none'}}")
    print(row['command_block'])
PY
"""
    path.write_text(text, encoding="utf-8")
    path.chmod(0o755)


def build_lineage_report(
    repo_root: str | Path,
    *,
    source: str | None,
    waves: Iterable[str] | None,
    response_option_map: str,
    env_file: str,
) -> dict[str, Any]:
    repo = Path(repo_root)
    if source and waves:
        specs = [(source, wave) for wave in waves]
    elif source:
        specs = _discover_wave_specs(repo, source)
    else:
        specs = _discover_wave_specs(repo, None)
    rows: list[dict[str, Any]] = []
    for family, wave in specs:
        stages = resolve_stage_roots(repo, family, wave)
        row = _wave_row(family, wave, stages)
        row["command_block"] = "\n".join(
            _command_block(repo, row, response_option_map=response_option_map, env_file=env_file)
        )
        rows.append(row)
    return {
        "repo_root": str(repo),
        "identity_discovery": "W01_UID_CATALOG_PLUS_PRODUCER_MANIFESTS",
        "stage_order": ["v550", "v550j", "v551", "v551j", "v552", "v552j"],
        "wave_resolutions": rows,
        "resolved_uid_tasks": [row["task_id"] for row in rows if not row["first_unresolved_stage"]],
        "unresolved_uid_tasks": [row["task_id"] for row in rows if row["first_unresolved_stage"]],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manifest/UID Rawlsing V550→V552J lineage resolver")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--source", default=None)
    parser.add_argument("--waves", nargs="*", default=None)
    parser.add_argument("--response-option-map", default=str(ROOT / "data/ddm_build_copy/reports/V550_response_option_map.csv"))
    parser.add_argument("--directionality-authority-dir", default=str(ROOT / "data/ddm_build_copy/directionality_authority"))
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--report-json", default=str(ROOT / "docs/architecture_control/reports/pipeline_lineage_resolution.json"))
    parser.add_argument("--shell-script", default="")
    parser.add_argument("--dependency-ledger", default="")
    parser.add_argument("--dependency-ledger-sha256", default="")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    # The dependency ledger may remain historical provenance, but it is not used
    # to infer source/wave lineage or to activate V553+.
    report = build_lineage_report(
        args.repo_root,
        source=args.source,
        waves=args.waves,
        response_option_map=args.response_option_map,
        env_file=args.env_file,
    )
    if args.dependency_ledger:
        report["dependency_ledger_provenance"] = {
            "path": args.dependency_ledger,
            "sha256": args.dependency_ledger_sha256,
            "used_for_identity_discovery": False,
        }
    report_path = Path(args.report_json)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    shell_path = Path(args.shell_script) if args.shell_script else report_path.with_suffix(".sh")
    _write_shell(shell_path, report_path)
    report["shell_script_path"] = str(shell_path)
    report_path.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    if not args.quiet:
        print(f"RESOLVED_UID_TASKS: {' '.join(report['resolved_uid_tasks']) or '(none)'}")
        print(f"UNRESOLVED_UID_TASKS: {' '.join(report['unresolved_uid_tasks']) or '(none)'}")
        print(f"# resolver_report: {report_path}")
        print(f"# resolver_shell_script: {shell_path}")
    return 0 if not report["unresolved_uid_tasks"] else 1


__all__ = [
    "StageResolution",
    "resolve_stage_roots",
    "_discover_wave_specs",
    "build_lineage_report",
    "parse_args",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
