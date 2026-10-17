#!/usr/bin/env python3
"""Fail-closed canonical V552J consumer adapter for V553 wave harmonization.

POSTG5-004 closed the V552J producer contract on the current structural
join/input/handoff surface. V553 consumes that published surface directly and
never recreates or depends on ``v552j_structural_handoff_packet.json``.

This module is also the trust boundary: V552J publication is accepted only
when the producer manifest, canonical join/audit artifacts, V553 input/handoff
indexes, readiness report, and V553 handoff manifest are mutually verifiable.
Missing, unreadable/corrupt, schema-invalid, integrity-invalid, and valid-empty
surfaces remain distinct.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd

from data.ddm_build_copy import ddm_v553_harmonization as _legacy
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    boundary_state_from_payload,
    inspect_artifact,
    read_status_document,
)
from data.ddm_build_copy.ddm_survey_identity import canonical_country_code
from data.ddm_build_copy.ddm_v552j_handoff import (
    AUDIT_COLUMNS,
    JOIN_COLUMNS,
    V552J_JOIN_COMPILER_VERSION,
    V552J_JOIN_SCHEMA_VERSION,
)
from data.ddm_build_copy.ddm_v553_harmonization import WaveDescriptor

SURFACE_VALID_PRESENT = "VALID_PRESENT"
SURFACE_VALID_EMPTY = "VALID_EMPTY"
SURFACE_MISSING = "MISSING"
SURFACE_UNREADABLE = "UNREADABLE_OR_CORRUPT"
SURFACE_SCHEMA_INVALID = "SCHEMA_INVALID"
SURFACE_INTEGRITY_INVALID = "INTEGRITY_INVALID"
VALID_SURFACE_STATUSES = frozenset({SURFACE_VALID_PRESENT, SURFACE_VALID_EMPTY})

_CANONICAL_MANIFEST = Path("manifest.json")
_CANONICAL_READINESS = Path("manifest/v552j_readiness_report.json")
_CANONICAL_HANDOFF_MANIFEST = Path("manifest/v552j_v553_handoff_manifest.json")
_CANONICAL_JOIN = Path("packets/v552j_structural_join_index.parquet")
_CANONICAL_AUDIT = Path("audits/v552j_join_audit.parquet")
_CANONICAL_INPUT = Path("packets/v552j_v553_input_index.parquet")
_CANONICAL_HANDOFF = Path("packets/v552j_to_v553_handoff_index.parquet")

V553_CANONICAL_INDEX_REQUIRED_COLUMNS = tuple(
    dict.fromkeys(
        [
            *JOIN_COLUMNS,
            "v552j_packet_id",
            "v553_input_id",
            "source_family",
            "country",
            "source_v552_structural_fact_id",
            "source_v552_structural_fact_ids_diagnostic_json",
            "source_v552_temporal_key_source_ids_json",
            "source_v552_temporal_key_source_ids_diagnostic_json",
            "structural_fact_lane",
            "structural_fact_grain",
            "single_wave_probe_allowed",
            "ready_for_v553",
            "packet_ready_for_v553",
            "temporal_field_allowed",
            "must_temporalize",
            "temporal_anchor_required",
            "comparability_required",
            "ready_for_runtime_consumption",
            "comparability_status",
            "fallback_permission_profile_key",
            "packet_class",
            "read_permission",
            "blocking_reason",
        ]
    )
)

_REQUIRED_ARTIFACTS = {
    "v552j_structural_join_index": (_CANONICAL_JOIN, "canonical", tuple(JOIN_COLUMNS)),
    "v552j_join_audit": (_CANONICAL_AUDIT, "canonical", tuple(AUDIT_COLUMNS)),
    "v552j_v553_input_index": (_CANONICAL_INPUT, "compatibility", V553_CANONICAL_INDEX_REQUIRED_COLUMNS),
    "v552j_to_v553_handoff_index": (_CANONICAL_HANDOFF, "compatibility", V553_CANONICAL_INDEX_REQUIRED_COLUMNS),
}


class V553CanonicalSurfaceError(RuntimeError):
    """Raised when the V552J publication cannot cross the V553 trust boundary."""

    def __init__(self, status: str, reason: str):
        self.status = status
        self.reason = reason
        super().__init__(f"V553_V552J_CANONICAL_SURFACE_{status}:{reason}")


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


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _clean(value).lower() in {"1", "true", "t", "yes", "y", "on"}


def _descriptor(item: WaveDescriptor | dict[str, Any]) -> WaveDescriptor:
    value = item if isinstance(item, WaveDescriptor) else WaveDescriptor.from_mapping(item)
    return value.normalized()


def _json_array_items(value: Any) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [_clean(item) for item in value if _clean(item)]
    text = _clean(value)
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except Exception:
        return [text]
    if isinstance(parsed, list):
        return [_clean(item) for item in parsed if _clean(item)]
    cleaned = _clean(parsed)
    return [cleaned] if cleaned else []


def _collect_ids(frames: Iterable[pd.DataFrame], columns: Iterable[str]) -> list[str]:
    values: set[str] = set()
    for frame in frames:
        if frame is None or frame.empty:
            continue
        for column in columns:
            if column not in frame.columns:
                continue
            for raw in frame[column].tolist():
                values.update(_json_array_items(raw))
    return sorted(value for value in values if value)


def _base_context(root: Path | None) -> dict[str, Any]:
    return {
        "root": str(root) if root else "",
        "manifest_path": str(root / _CANONICAL_MANIFEST) if root else "",
        "readiness_path": str(root / _CANONICAL_READINESS) if root else "",
        "handoff_manifest_path": str(root / _CANONICAL_HANDOFF_MANIFEST) if root else "",
        "input_path": str(root / _CANONICAL_INPUT) if root else "",
        "handoff_path": str(root / _CANONICAL_HANDOFF) if root else "",
        "surface_status": SURFACE_MISSING,
        "surface_valid": False,
        "surface_present": False,
        "surface_reason": "v552j_run_root_missing",
        "artifact_statuses": {},
        "producer_state": {},
        "readiness_status": "",
        "handoff_authority_status": "unknown",
        "blocker_context_count": 0,
        "blocker_context_breakdown_json": "",
        "relation_axis_ids": [],
        "target_entity_ids": [],
        "driver_facet_ids": [],
        "structural_channel_ids": [],
        "horizon_constraint_ids": [],
    }


def _fail(context: dict[str, Any], status: str, reason: str, **updates: Any) -> dict[str, Any]:
    context.update(updates)
    context.update(
        {
            "surface_status": status,
            "surface_valid": False,
            "surface_present": False,
            "surface_reason": reason,
        }
    )
    return context


def _document(path: Path, label: str) -> tuple[dict[str, Any] | None, str | None, str | None]:
    document = read_status_document(path)
    if not document.exists:
        return None, SURFACE_MISSING, f"{label}_missing:{path}"
    if not document.readable:
        return None, SURFACE_UNREADABLE, f"{label}_unreadable:{path}:{document.error}"
    payload = document.payload
    if not isinstance(payload, dict):
        return None, SURFACE_SCHEMA_INVALID, f"{label}_not_object:{path}"
    return payload, None, None


def _producer_identity(payload: Mapping[str, Any]) -> dict[str, str]:
    raw = payload.get("producer_scope_identity")
    scope = dict(raw) if isinstance(raw, Mapping) else {}
    return {
        "run_id": _clean(scope.get("run_id") or payload.get("producer_run_id") or payload.get("run_id")),
        "source": _clean(scope.get("source") or payload.get("source")),
        "wave": _clean(scope.get("canonical_wave") or scope.get("wave") or payload.get("canonical_wave") or payload.get("wave")),
        "country_code": canonical_country_code(scope.get("country_code") or payload.get("country_code")),
        "shard_id": _clean(scope.get("shard_id") or payload.get("shard_id")),
    }


def _validate_document_contract(
    payload: Mapping[str, Any],
    *,
    label: str,
    expected_identity: Mapping[str, str],
    expected_state: tuple[str, str, str] | None = None,
) -> tuple[tuple[str, str, str] | None, str | None, str | None]:
    if _clean(payload.get("contract_version") or payload.get("boundary_contract_version")) != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        return None, SURFACE_SCHEMA_INVALID, f"{label}_boundary_contract_version_mismatch"
    if _clean(payload.get("schema_version")) != V552J_JOIN_SCHEMA_VERSION:
        return None, SURFACE_SCHEMA_INVALID, f"{label}_schema_version_mismatch"
    if _clean(payload.get("compiler_version")) != V552J_JOIN_COMPILER_VERSION:
        return None, SURFACE_SCHEMA_INVALID, f"{label}_compiler_version_mismatch"
    try:
        state = boundary_state_from_payload(payload)
    except Exception as exc:
        return None, SURFACE_SCHEMA_INVALID, f"{label}_typed_state_invalid:{type(exc).__name__}:{exc}"
    state_tuple = (state.run_integrity_status, state.evidence_status, state.downstream_permission_status)
    if state.run_integrity_status != "PASS":
        return None, SURFACE_INTEGRITY_INVALID, f"{label}_run_integrity_not_pass:{state.run_integrity_status}"
    if expected_state is not None and state_tuple != expected_state:
        return None, SURFACE_INTEGRITY_INVALID, f"{label}_state_mismatch:expected={expected_state}:actual={state_tuple}"

    identity = _producer_identity(payload)
    for key in ("run_id", "source", "wave"):
        if not identity[key]:
            return None, SURFACE_SCHEMA_INVALID, f"{label}_identity_missing:{key}"
        if expected_identity.get(key) and identity[key] != expected_identity[key]:
            return None, SURFACE_INTEGRITY_INVALID, f"{label}_identity_mismatch:{key}:expected={expected_identity[key]}:actual={identity[key]}"
    expected_country = canonical_country_code(expected_identity.get("country_code"))
    if expected_country:
        if not identity["country_code"]:
            return None, SURFACE_SCHEMA_INVALID, f"{label}_identity_missing:country_code"
        if identity["country_code"] != expected_country:
            return None, SURFACE_INTEGRITY_INVALID, f"{label}_identity_mismatch:country_code:expected={expected_country}:actual={identity['country_code']}"
    return state_tuple, None, None


def _artifact_declarations(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("artifacts")
    if not isinstance(raw, list):
        return []
    return [dict(item) for item in raw if isinstance(item, Mapping)]


def _artifact_declaration(
    payload: Mapping[str, Any],
    artifact_name: str,
    expected_path: Path,
    expected_kind: str,
) -> tuple[dict[str, Any] | None, str | None]:
    matches: list[dict[str, Any]] = []
    for row in _artifact_declarations(payload):
        name = _clean(row.get("artifact") or row.get("name"))
        rel = _clean(row.get("path") or row.get("relative_path"))
        if name == artifact_name or Path(rel).name == expected_path.name:
            matches.append(row)
    if len(matches) != 1:
        return None, f"artifact_declaration_count:{artifact_name}:{len(matches)}"
    declaration = matches[0]
    rel = _clean(declaration.get("path") or declaration.get("relative_path"))
    if Path(rel).as_posix() != expected_path.as_posix():
        return None, f"artifact_path_mismatch:{artifact_name}:expected={expected_path}:actual={rel}"
    if _clean(declaration.get("artifact_kind")) != expected_kind:
        return None, f"artifact_kind_mismatch:{artifact_name}:expected={expected_kind}:actual={_clean(declaration.get('artifact_kind'))}"
    if _clean(declaration.get("schema_version")) != V552J_JOIN_SCHEMA_VERSION:
        return None, f"artifact_schema_version_mismatch:{artifact_name}"
    if _clean(declaration.get("compiler_version")) != V552J_JOIN_COMPILER_VERSION:
        return None, f"artifact_compiler_version_mismatch:{artifact_name}"
    declared_hash = _clean(declaration.get("artifact_file_sha256")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
        return None, f"artifact_sha256_missing_or_invalid:{artifact_name}"
    try:
        row_count = int(declaration.get("row_count"))
    except Exception:
        return None, f"artifact_row_count_missing_or_invalid:{artifact_name}"
    if row_count < 0:
        return None, f"artifact_row_count_negative:{artifact_name}"
    return declaration, None


def _validate_frame_schema(
    frame: pd.DataFrame,
    *,
    required_columns: Iterable[str],
    artifact_name: str,
    expected_identity: Mapping[str, str],
) -> str | None:
    missing = sorted(set(required_columns) - set(frame.columns))
    if missing:
        return f"artifact_required_columns_missing:{artifact_name}:{','.join(missing)}"
    if frame.empty:
        return None
    if frame["schema_version"].map(_clean).ne(V552J_JOIN_SCHEMA_VERSION).any():
        return f"artifact_row_schema_version_mismatch:{artifact_name}"
    if frame["compiler_version"].map(_clean).ne(V552J_JOIN_COMPILER_VERSION).any():
        return f"artifact_row_compiler_version_mismatch:{artifact_name}"

    checks = {
        "run_id": expected_identity.get("run_id", ""),
        "source": expected_identity.get("source", ""),
        "canonical_wave": expected_identity.get("wave", ""),
    }
    expected_country = canonical_country_code(expected_identity.get("country_code"))
    if expected_country:
        checks["country_code"] = expected_country
    for column, expected in checks.items():
        if not expected:
            continue
        use = column
        if column == "source" and column not in frame.columns and "source_family" in frame.columns:
            use = "source_family"
        if use not in frame.columns:
            return f"artifact_scope_column_missing:{artifact_name}:{column}"
        observed = {_clean(value) for value in frame[use].tolist() if _clean(value)}
        if observed != {expected}:
            return f"artifact_scope_mismatch:{artifact_name}:{column}:expected={expected}:actual={sorted(observed)}"
    return None


def _verify_artifact(
    *,
    root: Path,
    payload: Mapping[str, Any],
    artifact_name: str,
    expected_path: Path,
    expected_kind: str,
    required_columns: Iterable[str],
    expected_identity: Mapping[str, str],
) -> tuple[pd.DataFrame | None, dict[str, Any], str | None, str | None]:
    declaration, declaration_error = _artifact_declaration(payload, artifact_name, expected_path, expected_kind)
    if declaration_error:
        return None, {"status": SURFACE_SCHEMA_INVALID, "reason": declaration_error}, SURFACE_SCHEMA_INVALID, declaration_error
    assert declaration is not None
    path = root / expected_path
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        reason = f"artifact_escapes_run_root:{artifact_name}:{path}"
        return None, {"status": SURFACE_SCHEMA_INVALID, "reason": reason}, SURFACE_SCHEMA_INVALID, reason

    inspection = inspect_artifact(path)
    if not inspection.exists:
        reason = f"artifact_missing:{artifact_name}:{path}"
        return None, {"status": SURFACE_MISSING, "reason": reason}, SURFACE_MISSING, reason
    if not inspection.readable:
        reason = f"artifact_unreadable_or_corrupt:{artifact_name}:{path}:{inspection.error}"
        return None, {"status": SURFACE_UNREADABLE, "reason": reason}, SURFACE_UNREADABLE, reason
    declared_hash = _clean(declaration.get("artifact_file_sha256")).lower()
    if inspection.artifact_file_sha256.lower() != declared_hash:
        reason = f"artifact_sha256_mismatch:{artifact_name}:expected={declared_hash}:actual={inspection.artifact_file_sha256.lower()}"
        return None, {"status": SURFACE_INTEGRITY_INVALID, "reason": reason}, SURFACE_INTEGRITY_INVALID, reason
    declared_rows = int(declaration["row_count"])
    if int(inspection.row_count or 0) != declared_rows:
        reason = f"artifact_row_count_mismatch:{artifact_name}:expected={declared_rows}:actual={int(inspection.row_count or 0)}"
        return None, {"status": SURFACE_INTEGRITY_INVALID, "reason": reason}, SURFACE_INTEGRITY_INVALID, reason
    try:
        frame = pd.read_parquet(path)
    except Exception as exc:
        reason = f"artifact_full_read_failed:{artifact_name}:{type(exc).__name__}:{exc}"
        return None, {"status": SURFACE_UNREADABLE, "reason": reason}, SURFACE_UNREADABLE, reason
    if not isinstance(frame, pd.DataFrame):
        reason = f"artifact_read_not_dataframe:{artifact_name}"
        return None, {"status": SURFACE_SCHEMA_INVALID, "reason": reason}, SURFACE_SCHEMA_INVALID, reason
    schema_error = _validate_frame_schema(
        frame,
        required_columns=required_columns,
        artifact_name=artifact_name,
        expected_identity=expected_identity,
    )
    if schema_error:
        return None, {"status": SURFACE_SCHEMA_INVALID, "reason": schema_error}, SURFACE_SCHEMA_INVALID, schema_error
    status = SURFACE_VALID_EMPTY if frame.empty else SURFACE_VALID_PRESENT
    return frame, {"status": status, "row_count": int(len(frame)), "path": str(path)}, None, None


def _same_frame(left: pd.DataFrame, right: pd.DataFrame) -> bool:
    if tuple(left.columns) != tuple(right.columns):
        return False
    try:
        return left.reset_index(drop=True).equals(right.reset_index(drop=True))
    except Exception:
        return False


def inspect_v552j_canonical_surface(item: WaveDescriptor | dict[str, Any]) -> dict[str, Any]:
    """Inspect and classify one V552J→V553 publication without accepting invalid input."""
    desc = _descriptor(item)
    root_text = _clean(desc.latest_v552j_root) or _clean(desc.v552j_run_root)
    root = Path(root_text) if root_text else None
    context = _base_context(root)
    if root is None:
        return context
    if not root.exists() or not root.is_dir():
        return _fail(context, SURFACE_MISSING, f"v552j_run_root_missing:{root}")

    manifest_path = root / _CANONICAL_MANIFEST
    manifest, failure_status, failure_reason = _document(manifest_path, "v552j_manifest")
    if failure_status:
        return _fail(context, failure_status, failure_reason or "v552j_manifest_invalid")
    assert manifest is not None

    manifest_identity = _producer_identity(manifest)
    expected_identity = {
        "run_id": manifest_identity["run_id"],
        "source": _clean(desc.source) or manifest_identity["source"],
        "wave": _clean(desc.canonical_wave or desc.wave) or manifest_identity["wave"],
        "country_code": canonical_country_code(desc.country_code) or manifest_identity["country_code"],
        "shard_id": manifest_identity["shard_id"],
    }
    if not expected_identity["run_id"]:
        return _fail(context, SURFACE_SCHEMA_INVALID, "v552j_manifest_identity_missing:run_id")

    state_tuple, failure_status, failure_reason = _validate_document_contract(
        manifest,
        label="v552j_manifest",
        expected_identity=expected_identity,
    )
    if failure_status:
        return _fail(context, failure_status, failure_reason or "v552j_manifest_contract_invalid")
    assert state_tuple is not None
    context["producer_state"] = {
        "run_integrity_status": state_tuple[0],
        "evidence_status": state_tuple[1],
        "downstream_permission_status": state_tuple[2],
    }

    canonical_names = tuple(str(value) for value in manifest.get("canonical_artifact_names") or [])
    if canonical_names != ("v552j_structural_join_index", "v552j_join_audit"):
        return _fail(
            context,
            SURFACE_SCHEMA_INVALID,
            f"canonical_artifact_names_mismatch:{canonical_names}",
        )

    frames: dict[str, pd.DataFrame] = {}
    artifact_statuses: dict[str, Any] = {}
    for artifact_name, (relative_path, kind, required_columns) in _REQUIRED_ARTIFACTS.items():
        frame, artifact_status, failure_status, failure_reason = _verify_artifact(
            root=root,
            payload=manifest,
            artifact_name=artifact_name,
            expected_path=relative_path,
            expected_kind=kind,
            required_columns=required_columns,
            expected_identity=expected_identity,
        )
        artifact_statuses[artifact_name] = artifact_status
        context["artifact_statuses"] = artifact_statuses
        if failure_status:
            return _fail(context, failure_status, failure_reason or f"{artifact_name}_invalid")
        assert frame is not None
        frames[artifact_name] = frame

    readiness_path = root / _CANONICAL_READINESS
    readiness, failure_status, failure_reason = _document(readiness_path, "v552j_readiness")
    if failure_status:
        return _fail(context, failure_status, failure_reason or "v552j_readiness_invalid")
    assert readiness is not None
    _, failure_status, failure_reason = _validate_document_contract(
        readiness,
        label="v552j_readiness",
        expected_identity=expected_identity,
        expected_state=state_tuple,
    )
    if failure_status:
        return _fail(context, failure_status, failure_reason or "v552j_readiness_contract_invalid")

    handoff_manifest_path = root / _CANONICAL_HANDOFF_MANIFEST
    handoff_manifest, failure_status, failure_reason = _document(handoff_manifest_path, "v552j_v553_handoff_manifest")
    if failure_status:
        return _fail(context, failure_status, failure_reason or "v552j_v553_handoff_manifest_invalid")
    assert handoff_manifest is not None
    _, failure_status, failure_reason = _validate_document_contract(
        handoff_manifest,
        label="v552j_v553_handoff_manifest",
        expected_identity=expected_identity,
        expected_state=state_tuple,
    )
    if failure_status:
        return _fail(context, failure_status, failure_reason or "v552j_v553_handoff_manifest_contract_invalid")

    declared_input_path = Path(_clean(handoff_manifest.get("v553_input_index_path")))
    if declared_input_path.as_posix() != _CANONICAL_INPUT.as_posix():
        return _fail(
            context,
            SURFACE_SCHEMA_INVALID,
            f"handoff_manifest_v553_input_index_path_mismatch:expected={_CANONICAL_INPUT}:actual={declared_input_path}",
        )

    input_df = frames["v552j_v553_input_index"]
    handoff_df = frames["v552j_to_v553_handoff_index"]
    join_df = frames["v552j_structural_join_index"]
    if len(join_df) != len(input_df) or len(input_df) != len(handoff_df):
        return _fail(
            context,
            SURFACE_INTEGRITY_INVALID,
            f"canonical_row_count_disagreement:join={len(join_df)}:input={len(input_df)}:handoff={len(handoff_df)}",
        )
    if not _same_frame(input_df, handoff_df):
        return _fail(context, SURFACE_INTEGRITY_INVALID, "v553_input_and_handoff_indexes_differ")

    if "v553_probe_row_count" not in handoff_manifest:
        return _fail(context, SURFACE_SCHEMA_INVALID, "handoff_manifest_v553_probe_row_count_missing")
    if "v553_temporal_field_row_count" not in handoff_manifest:
        return _fail(context, SURFACE_SCHEMA_INVALID, "handoff_manifest_v553_temporal_field_row_count_missing")
    try:
        declared_probe_rows = int(handoff_manifest.get("v553_probe_row_count"))
        declared_temporal_rows = int(handoff_manifest.get("v553_temporal_field_row_count"))
    except Exception:
        return _fail(context, SURFACE_SCHEMA_INVALID, "handoff_manifest_row_counts_invalid")
    actual_probe_rows = int(input_df["ready_for_v553_probe"].map(_truthy).sum()) if not input_df.empty else 0
    actual_temporal_rows = int(input_df["temporal_field_allowed"].map(_truthy).sum()) if not input_df.empty else 0
    if declared_probe_rows != actual_probe_rows:
        return _fail(
            context,
            SURFACE_INTEGRITY_INVALID,
            f"handoff_manifest_probe_row_count_mismatch:expected={declared_probe_rows}:actual={actual_probe_rows}",
        )
    if declared_temporal_rows != actual_temporal_rows:
        return _fail(
            context,
            SURFACE_INTEGRITY_INVALID,
            f"handoff_manifest_temporal_row_count_mismatch:expected={declared_temporal_rows}:actual={actual_temporal_rows}",
        )

    all_empty = len(join_df) == 0 and len(input_df) == 0 and len(handoff_df) == 0
    surface_status = SURFACE_VALID_EMPTY if all_empty else SURFACE_VALID_PRESENT
    context.update(
        {
            "surface_status": surface_status,
            "surface_valid": True,
            "surface_present": True,
            "surface_reason": "verified_full_v552j_publication",
            "readiness_status": _clean(readiness.get("status"))
            or "/".join(state_tuple),
            "handoff_authority_status": state_tuple[2],
            "blocker_context_count": int(readiness.get("blocker_context_count", 0) or 0),
            "blocker_context_breakdown_json": _clean(readiness.get("blocker_context_breakdown_json")),
            "relation_axis_ids": _collect_ids([input_df], ("relation_axis_id", "relation_axis_ids_json")),
            "target_entity_ids": _collect_ids([input_df], ("target_entity_id", "target_entity_ids_json")),
            "driver_facet_ids": _collect_ids([input_df], ("driver_facet_id", "driver_facet_ids_json")),
            "structural_channel_ids": _collect_ids([input_df], ("structural_channel_id", "structural_channel_ids_json")),
            "horizon_constraint_ids": _collect_ids([input_df], ("horizon_constraint_id", "horizon_constraint_ids_json")),
        }
    )
    return context


def _build_canonical_wave_bundle(item: WaveDescriptor | dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    desc = _descriptor(item)
    authority_dir = Path(desc.authority_dir) if desc.authority_dir else None
    run_root = Path(desc.run_root) if desc.run_root else None

    overlay_paths: dict[str, str] = {}
    overlay_row_counts: dict[str, int] = {}
    overlay_certified_row_counts: dict[str, int] = {}
    overlay_columns: dict[str, list[str]] = {}
    missing_kinds: list[str] = []
    for kind in _legacy.OVERLAY_FILENAMES:
        path = _legacy._overlay_path(authority_dir, desc.source, desc.canonical_wave or desc.wave, kind)
        if path is None:
            missing_kinds.append(kind)
            continue
        frame = _legacy._load_frame(path)
        overlay_paths[kind] = str(path)
        overlay_row_counts[kind] = int(len(frame))
        overlay_columns[kind] = list(frame.columns)
        certified_count = _legacy._certified_overlay_row_count(frame, kind)
        overlay_certified_row_counts[kind] = certified_count
        if certified_count <= 0:
            missing_kinds.append(kind)

    thin_readiness_path = _legacy._thin_readiness_path(run_root) if run_root else None
    thin_readiness = _legacy._load_json(thin_readiness_path) if thin_readiness_path else {}
    if not thin_readiness:
        thin_readiness = {"final_status": "MISSING_V5_THIN_READINESS"}
    thin_status = _clean(thin_readiness.get("final_status"))
    thin_ready = bool(thin_status) and not thin_status.startswith("BLOCKED")
    thin_layer_count = int(thin_readiness.get("layer_count", 0) or 0)

    context = inspect_v552j_canonical_surface(desc)
    if not context["surface_valid"]:
        raise V553CanonicalSurfaceError(context["surface_status"], context["surface_reason"])

    if context["surface_status"] == SURFACE_VALID_EMPTY:
        wave_status = "valid_empty_v552j_surface"
    elif missing_kinds:
        wave_status = "partial"
    else:
        wave_status = "complete"
    if len(missing_kinds) == len(_legacy.OVERLAY_FILENAMES):
        wave_status = "missing_all_authority_overlays"

    bundle = {
        "wave": desc.wave,
        "source": desc.source,
        "canonical_wave": desc.canonical_wave or desc.wave,
        "country_code": canonical_country_code(desc.country_code),
        "temporal_year": desc.temporal_year,
        "authority_dir": str(authority_dir) if authority_dir else "",
        "run_root": str(run_root) if run_root else "",
        "v552j_run_root": _clean(desc.v552j_run_root),
        "latest_v552j_root": context["root"],
        "latest_v552j_readiness_report": context["readiness_path"],
        "v552j_readiness_report_path": context["readiness_path"],
        "v552j_v553_input_index_path": context["input_path"],
        "v552j_to_v553_handoff_index_path": context["handoff_path"],
        "v552_structural_fact_index_path": _clean(desc.v552_structural_fact_index_path),
        "v552_temporal_key_source_index_path": _clean(desc.v552_temporal_key_source_index_path),
        "v552j_handoff_manifest_path": context["handoff_manifest_path"],
        "latest_v551j_root": "",
        "latest_v551j_certified_packet_index": "",
        "latest_v551j_reviewable_evidence_sidecar": "",
        "v552j_readiness_status": context["readiness_status"],
        "v552j_blocker_context_breakdown_json": context["blocker_context_breakdown_json"],
        "v552j_blocker_context_count": context["blocker_context_count"],
        "v552j_handoff_authority_status": context["handoff_authority_status"],
        "v552j_consumer_surface": "canonical_v552j_input_handoff_indexes",
        "v552j_consumer_surface_status": context["surface_status"],
        "v552j_consumer_surface_valid": context["surface_valid"],
        "obsolete_v552j_structural_handoff_packet_required": False,
        "wave_relation_axis_ids": context["relation_axis_ids"],
        "wave_target_entity_ids": context["target_entity_ids"],
        "wave_driver_facet_ids": context["driver_facet_ids"],
        "wave_structural_channel_ids": context["structural_channel_ids"],
        "wave_horizon_constraint_ids": context["horizon_constraint_ids"],
        "overlay_paths": overlay_paths,
        "overlay_row_counts": overlay_row_counts,
        "overlay_certified_row_counts": overlay_certified_row_counts,
        "overlay_columns": overlay_columns,
        "missing_authority_kinds": missing_kinds,
        "wave_status": wave_status,
        "thin_readiness": thin_readiness,
        "thin_status": thin_status,
        "thin_ready": thin_ready,
        "thin_layer_count": thin_layer_count,
        "created_at": _legacy.utc_now(),
    }
    return bundle, context


def build_v553_wave_harmonization(
    descriptors: Iterable[WaveDescriptor | dict[str, Any]],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Build V553 harmonization from only fully verified canonical V552J surfaces."""
    bundles: list[dict[str, Any]] = []
    contexts: list[dict[str, Any]] = []
    for item in descriptors:
        bundle, context = _build_canonical_wave_bundle(item)
        bundles.append(bundle)
        contexts.append(context)

    table = pd.DataFrame(bundles)
    report = _legacy.build_v553_wave_harmonization_report(table)
    report["v552j_consumer_surface"] = "canonical_v552j_input_handoff_indexes"
    report["v552j_consumer_surface_validation"] = "fail_closed_full_publication_verification"
    report["obsolete_v552j_structural_handoff_packet_required"] = False
    report["v552j_canonical_surface_by_wave"] = [
        {
            "wave": _clean(table.iloc[index].get("wave")) if index < len(table) else "",
            "manifest_path": context["manifest_path"],
            "input_index_path": context["input_path"],
            "handoff_index_path": context["handoff_path"],
            "readiness_path": context["readiness_path"],
            "handoff_manifest_path": context["handoff_manifest_path"],
            "surface_status": context["surface_status"],
            "surface_valid": context["surface_valid"],
            "surface_present": context["surface_present"],
            "surface_reason": context["surface_reason"],
            "artifact_statuses": context["artifact_statuses"],
        }
        for index, context in enumerate(contexts)
    ]
    return table, report


__all__ = [
    "SURFACE_INTEGRITY_INVALID",
    "SURFACE_MISSING",
    "SURFACE_SCHEMA_INVALID",
    "SURFACE_UNREADABLE",
    "SURFACE_VALID_EMPTY",
    "SURFACE_VALID_PRESENT",
    "V553_CANONICAL_INDEX_REQUIRED_COLUMNS",
    "V553CanonicalSurfaceError",
    "build_v553_wave_harmonization",
    "inspect_v552j_canonical_surface",
]
