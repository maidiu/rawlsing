#!/usr/bin/env python3
"""Wave harmonization helpers for the V553 temporal layer.

This module is the first substantive implementation step for the V553 path.
It harmonizes multiple waves into a shared structural comparison surface while
preserving wave-specific authority and explicit differences.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_survey_identity import (
    canonical_country_code,
    canonical_family_key,
    canonical_family_label,
    require_survey_identity,
    wave_ordinal,
)
from data.ddm_build_copy.ddm_v550_family_overlay import load_family_overlay
from data.ddm_build_copy.ddm_v550_authority_contract import (
    CERTIFIED,
    normalize_authority_status,
)

try:
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover - fallback for partial environments
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


V553_HARMONIZATION_SCHEMA_VERSION = "v553_wave_harmonization_0.1"
V553_HARMONIZATION_COMPILER_VERSION = "v553_wave_harmonization_0.1"
V553_REQUIRED_AUTHORITY_KINDS = ("semantic", "directionality", "position")
V553_REQUIRED_SHARED_STRUCTURE = ("shared_semantic_columns", "shared_directionality_columns", "shared_position_columns")

SEMANTIC_SIGNAL_COLUMNS = {
    "semantic_role",
    "semantic_subrole",
    "semantic_tags",
    "semantic_lane",
    "evidence_lane",
}
DIRECTIONALITY_SIGNAL_COLUMNS = {
    "directionality_policy",
    "signed_polarity_status",
    "directional_certification_status",
    "response_topology",
    "response_direction",
    "polarity",
    "scale_direction",
    "positive_anchor_label",
    "negative_anchor_label",
    "neutral_anchor_label",
}
POSITION_SIGNAL_COLUMNS = {
    "position_conditioning",
    "position_modifiers",
    "conditional_strata_weights",
    "horizon_affordance",
    "relation_axis_id",
    "target_entity_id",
    "driver_facet_id",
    "structural_mapping_status",
}

OVERLAY_FILENAMES = {
    "semantic": "semantic_authority_overlay.csv",
    "directionality": "directionality_overlay.csv",
    "position": "position_conditioning_overlay.csv",
}


@dataclass(frozen=True)
class WaveDescriptor:
    wave: str
    source: str = ""
    canonical_wave: str | None = None
    country_code: str | None = None
    temporal_year: int | None = None
    authority_dir: str | None = None
    run_root: str | None = None
    v552j_run_root: str | None = None
    latest_v552j_root: str | None = None
    latest_v552j_readiness_report: str | None = None
    v552j_readiness_report_path: str | None = None
    v552j_v553_input_index_path: str | None = None
    v552j_to_v553_handoff_index_path: str | None = None
    v552_structural_fact_index_path: str | None = None
    v552_temporal_key_source_index_path: str | None = None
    v552j_handoff_manifest_path: str | None = None

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> "WaveDescriptor":
        return cls(
            wave=str(mapping.get("wave", "")).strip(),
            source=str(mapping.get("source", "")).strip(),
            canonical_wave=(str(mapping.get("canonical_wave", "")).strip() or None),
            country_code=(
                str(
                    mapping.get("country_code")
                    or mapping.get("country")
                    or ""
                ).strip()
                or None
            ),
            temporal_year=(
                int(
                    mapping.get("temporal_year")
                    or mapping.get("fieldwork_year")
                    or mapping.get("survey_year")
                    or mapping.get("year")
                )
                if str(
                    mapping.get("temporal_year")
                    or mapping.get("fieldwork_year")
                    or mapping.get("survey_year")
                    or mapping.get("year")
                    or ""
                ).strip().isdigit()
                else None
            ),
            authority_dir=(str(mapping.get("authority_dir", "")).strip() or None),
            run_root=(str(mapping.get("run_root", "")).strip() or None),
            v552j_run_root=(str(mapping.get("v552j_run_root", "")).strip() or None),
            latest_v552j_root=(str(mapping.get("latest_v552j_root", "")).strip() or None),
            latest_v552j_readiness_report=(str(mapping.get("latest_v552j_readiness_report", "")).strip() or None),
            v552j_readiness_report_path=(str(mapping.get("v552j_readiness_report_path", "")).strip() or None),
            v552j_v553_input_index_path=(str(mapping.get("v552j_v553_input_index_path", "")).strip() or None),
            v552j_to_v553_handoff_index_path=(str(mapping.get("v552j_to_v553_handoff_index_path", "")).strip() or None),
            v552_structural_fact_index_path=(str(mapping.get("v552_structural_fact_index_path", "")).strip() or None),
            v552_temporal_key_source_index_path=(str(mapping.get("v552_temporal_key_source_index_path", "")).strip() or None),
            v552j_handoff_manifest_path=(str(mapping.get("v552j_handoff_manifest_path", "")).strip() or None),
        )

    def normalized(self) -> "WaveDescriptor":
        identity = require_survey_identity(
            self.source,
            self.canonical_wave or self.wave,
        )
        return WaveDescriptor(
            wave=self.wave or identity.canonical_wave,
            source=identity.source,
            canonical_wave=identity.canonical_wave,
            country_code=canonical_country_code(self.country_code),
            temporal_year=self.temporal_year,
            authority_dir=self.authority_dir,
            run_root=self.run_root,
            v552j_run_root=self.v552j_run_root,
            latest_v552j_root=self.latest_v552j_root,
            latest_v552j_readiness_report=self.latest_v552j_readiness_report,
            v552j_readiness_report_path=self.v552j_readiness_report_path,
            v552j_v553_input_index_path=self.v552j_v553_input_index_path,
            v552j_to_v553_handoff_index_path=self.v552j_to_v553_handoff_index_path,
            v552_structural_fact_index_path=self.v552_structural_fact_index_path,
            v552_temporal_key_source_index_path=self.v552_temporal_key_source_index_path,
            v552j_handoff_manifest_path=self.v552j_handoff_manifest_path,
        )


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def _load_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    frame = pd.read_csv(path, low_memory=False)
    return frame if isinstance(frame, pd.DataFrame) else pd.DataFrame()


def _load_parquet_frame(path_text: str | Path | None) -> pd.DataFrame:
    if not path_text:
        return pd.DataFrame()
    path = Path(path_text)
    if not path.exists():
        return pd.DataFrame()
    try:
        frame = pd.read_parquet(path)
    except Exception:
        return pd.DataFrame()
    return frame if isinstance(frame, pd.DataFrame) else pd.DataFrame()


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _bounded_score(value: float, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        score = default
    if pd.isna(score):
        score = default
    return max(0.0, min(1.0, score))


def _json_array_items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean_text(item) for item in value if _clean_text(item)]
    text = _clean_text(value)
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except Exception:
        return [part.strip() for part in text.split("|") if part.strip()]
    if isinstance(parsed, list):
        return [_clean_text(item) for item in parsed if _clean_text(item)]
    cleaned = _clean_text(parsed)
    return [cleaned] if cleaned else []


def _json_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = _clean_text(value)
    if not text:
        return {}
    try:
        parsed = json.loads(text)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _collect_unique_ids(frame: pd.DataFrame, column_names: Iterable[str]) -> list[str]:
    ids: set[str] = set()
    if frame is None or frame.empty:
        return []
    for column in column_names:
        if column not in frame.columns:
            continue
        for value in frame[column].tolist():
            for item in _json_array_items(value):
                if item:
                    ids.add(item)
    return sorted(ids)


def _overlay_path(
    authority_dir: Path | None,
    source: str,
    wave: str,
    kind: str,
) -> Path | None:
    if authority_dir is None:
        return None
    result = load_family_overlay(
        source,
        wave,
        {
            "semantic": "semantic_authority",
            "directionality": "directionality",
            "position": "position_conditioning",
        }[kind],
        required=False,
        search_roots=[authority_dir],
    )
    return Path(result.path) if result.status == "FOUND" and result.path else None


def _certified_overlay_row_count(frame: pd.DataFrame, kind: str) -> int:
    """Count rows carrying explicit authority for this overlay kind."""
    if frame.empty:
        return 0
    status_candidates = {
        "semantic": (
            "semantic_detail_authority_status",
            "semantic_role_authority_status",
            "semantic_authority_status",
        ),
        "directionality": ("directionality_authority_status",),
        "position": (
            "position_conditioning_authority_status",
            "structural_mapping_authority_status",
        ),
    }[kind]
    status_column = next(
        (candidate for candidate in status_candidates if candidate in frame.columns),
        "",
    )
    if status_column:
        return int(frame[status_column].map(normalize_authority_status).eq(CERTIFIED).sum())

    confidence_candidates = {
        "semantic": ("semantic_confidence",),
        "directionality": ("directionality_confidence",),
        "position": ("position_conditioning_confidence",),
    }[kind]
    confidence_column = next(
        (candidate for candidate in confidence_candidates if candidate in frame.columns),
        "",
    )
    if confidence_column:
        return int(
            frame[confidence_column]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin({"high", "very high", "very_high"})
            .sum()
        )

    return int(len(frame))


def _thin_readiness_path(run_root: Path | None) -> Path | None:
    if run_root is None:
        return None
    path = run_root / "manifest" / "v5_thin_end_to_end_readiness_report.json"
    return path if path.exists() else None


def _load_wave_bundle(descriptor: WaveDescriptor) -> dict[str, Any]:
    desc = descriptor.normalized()
    authority_dir = Path(desc.authority_dir) if desc.authority_dir else None
    run_root = Path(desc.run_root) if desc.run_root else None

    overlays: dict[str, pd.DataFrame] = {}
    overlay_paths: dict[str, str] = {}
    overlay_row_counts: dict[str, int] = {}
    overlay_certified_row_counts: dict[str, int] = {}
    overlay_columns: dict[str, list[str]] = {}
    missing_kinds: list[str] = []
    for kind in OVERLAY_FILENAMES:
        path = _overlay_path(
            authority_dir,
            desc.source,
            desc.canonical_wave or desc.wave,
            kind,
        )
        if path is None:
            missing_kinds.append(kind)
            continue
        frame = _load_frame(path)
        overlays[kind] = frame
        overlay_paths[kind] = str(path)
        overlay_row_counts[kind] = int(len(frame))
        overlay_columns[kind] = list(frame.columns)
        certified_count = _certified_overlay_row_count(frame, kind)
        overlay_certified_row_counts[kind] = certified_count
        if certified_count <= 0:
            missing_kinds.append(kind)

    thin_readiness_path = _thin_readiness_path(run_root) if run_root else None
    thin_readiness = _load_json(thin_readiness_path) if thin_readiness_path else {}
    if not thin_readiness:
        thin_readiness = {"final_status": "MISSING_V5_THIN_READINESS"}
    thin_status = str(thin_readiness.get("final_status", "")).strip()
    thin_ready = bool(thin_readiness.get("final_status")) and not str(thin_status).startswith("BLOCKED")
    thin_layer_count = int(thin_readiness.get("layer_count", 0) or 0)
    v552j_root = Path(desc.latest_v552j_root) if desc.latest_v552j_root else None
    v552j_readiness_path = Path(desc.latest_v552j_readiness_report) if desc.latest_v552j_readiness_report else None
    v552j_readiness = _load_json(v552j_readiness_path) if v552j_readiness_path else {}
    v552j_readiness_status = str(v552j_readiness.get("status", "")).strip() or str(v552j_readiness.get("structural_handoff_status", "")).strip()
    v552j_blocker_context_breakdown_json = str(v552j_readiness.get("blocker_context_breakdown_json", "")).strip()
    v552j_blocker_context_count = int(v552j_readiness.get("blocker_context_count", 0) or 0)
    v552j_handoff_authority_status = str(v552j_readiness.get("status", "")).strip() or "unknown"

    v552j_handoff_packet_path = (v552j_root / "packets" / "v552j_structural_handoff_packet.json") if v552j_root else None
    v552j_handoff_packet = _load_json(v552j_handoff_packet_path) if v552j_handoff_packet_path and v552j_handoff_packet_path.exists() else {}
    provenance_summary = _json_object(v552j_handoff_packet.get("provenance_summary_json"))
    upstream_links = _json_object(provenance_summary.get("upstream_provenance_links"))
    v551j_certified_text = _clean_text(upstream_links.get("v551j_certified_packet_index", ""))
    v551j_reviewable_text = _clean_text(upstream_links.get("v551j_reviewable_evidence_sidecar", ""))
    v551j_run_root_text = _clean_text(upstream_links.get("v551j_run_root", ""))
    v551j_certified_path = Path(v551j_certified_text) if v551j_certified_text else None
    v551j_reviewable_path = Path(v551j_reviewable_text) if v551j_reviewable_text else None
    v551j_run_root = Path(v551j_run_root_text) if v551j_run_root_text else None
    v551j_certified_df = _load_parquet_frame(v551j_certified_path if v551j_certified_path and v551j_certified_path.exists() else None)
    v551j_reviewable_df = _load_parquet_frame(v551j_reviewable_path if v551j_reviewable_path and v551j_reviewable_path.exists() else None)

    v552_optional_inputs = _json_object(upstream_links.get("v552_optional_inputs"))
    v552_relation_axis_df = _load_parquet_frame(v552_optional_inputs.get("v552_relation_axis_pressure_path"))
    v552_target_entity_df = _load_parquet_frame(v552_optional_inputs.get("v552_target_entity_pressure_path"))
    v552_driver_facet_df = _load_parquet_frame(v552_optional_inputs.get("v552_driver_facet_pressure_path"))
    v552_structural_channel_df = _load_parquet_frame(v552_optional_inputs.get("v552_structural_channel_index_path"))
    v552_horizon_constraint_df = _load_parquet_frame(v552_optional_inputs.get("v552_horizon_constraint_index_path"))

    wave_relation_axis_ids = _collect_unique_ids(v551j_certified_df, ["relation_axis_ids_json"])
    wave_target_entity_ids = _collect_unique_ids(v551j_certified_df, ["target_entity_ids_json"])
    wave_driver_facet_ids = _collect_unique_ids(v551j_certified_df, ["driver_facet_ids_json"])
    wave_structural_channel_ids = sorted(
        {
            *_collect_unique_ids(v552_structural_channel_df, ["channel_id"]),
            *_collect_unique_ids(v552_structural_channel_df, ["anchor_axis_id", "anchor_target_id", "anchor_driver_facet_id"]),
        }
    )
    wave_horizon_constraint_ids = sorted(
        {
            *_collect_unique_ids(v552_horizon_constraint_df, ["horizon_constraint_id"]),
            *_collect_unique_ids(v552_horizon_constraint_df, ["basis_relation_axis_id", "basis_target_entity_id", "basis_driver_facet_id"]),
        }
    )

    if not thin_status and run_root:
        thin_status = "MISSING_V5_THIN_READINESS"

    wave_status = "complete"
    if missing_kinds:
        wave_status = "partial"
    if len(missing_kinds) == len(OVERLAY_FILENAMES):
        wave_status = "missing_all_authority_overlays"

    bundle = {
        "wave": desc.wave,
        "source": desc.source,
        "canonical_wave": desc.canonical_wave or desc.wave,
        "country_code": canonical_country_code(desc.country_code),
        "temporal_year": desc.temporal_year,
        "authority_dir": repo_relative_path_text(authority_dir) if authority_dir else "",
        "run_root": repo_relative_path_text(run_root) if run_root else "",
        "v552j_run_root": repo_relative_path_text(Path(desc.v552j_run_root)) if desc.v552j_run_root else "",
        "latest_v552j_root": repo_relative_path_text(v552j_root) if v552j_root else "",
        "latest_v552j_readiness_report": repo_relative_path_text(v552j_readiness_path) if v552j_readiness_path else "",
        "v552j_readiness_report_path": repo_relative_path_text(v552j_readiness_path) if v552j_readiness_path else "",
        "v552j_v553_input_index_path": desc.v552j_v553_input_index_path or "",
        "v552j_to_v553_handoff_index_path": desc.v552j_to_v553_handoff_index_path or "",
        "v552_structural_fact_index_path": desc.v552_structural_fact_index_path or "",
        "v552_temporal_key_source_index_path": desc.v552_temporal_key_source_index_path or "",
        "v552j_handoff_manifest_path": desc.v552j_handoff_manifest_path or "",
        "latest_v551j_root": repo_relative_path_text(v551j_run_root) if v551j_run_root else "",
        "latest_v551j_certified_packet_index": repo_relative_path_text(v551j_certified_path) if v551j_certified_path and v551j_certified_path.exists() else "",
        "latest_v551j_reviewable_evidence_sidecar": repo_relative_path_text(v551j_reviewable_path) if v551j_reviewable_path and v551j_reviewable_path.exists() else "",
        "v552j_readiness_status": v552j_readiness_status,
        "v552j_blocker_context_breakdown_json": v552j_blocker_context_breakdown_json,
        "v552j_blocker_context_count": v552j_blocker_context_count,
        "v552j_handoff_authority_status": v552j_handoff_authority_status,
        "wave_relation_axis_ids": wave_relation_axis_ids,
        "wave_target_entity_ids": wave_target_entity_ids,
        "wave_driver_facet_ids": wave_driver_facet_ids,
        "wave_structural_channel_ids": wave_structural_channel_ids,
        "wave_horizon_constraint_ids": wave_horizon_constraint_ids,
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
        "created_at": utc_now(),
    }
    return bundle


def _shared_columns(frames: Iterable[pd.DataFrame]) -> list[str]:
    frames = [frame for frame in frames if frame is not None and not frame.empty]
    if not frames:
        return []
    shared = set(frames[0].columns)
    for frame in frames[1:]:
        shared &= set(frame.columns)
    return sorted(shared)


def _shared_id_lists(table: pd.DataFrame, column_name: str) -> list[str]:
    values: list[set[str]] = []
    for _, row in table.iterrows():
        items = row.get(column_name, []) or []
        if not isinstance(items, list):
            items = _json_array_items(items)
        values.append({item for item in items if item})
    values = [item for item in values if item]
    if not values:
        return []
    shared = set(values[0])
    for item in values[1:]:
        shared &= set(item)
    return sorted(shared)


def _pairwise_shared_id_lists(left: Any, right: Any) -> list[str]:
    left_items = {item for item in _json_array_items(left) if item}
    right_items = {item for item in _json_array_items(right) if item}
    if not left_items or not right_items:
        return []
    return sorted(left_items & right_items)


def _pairwise_shared_columns(left: list[str], right: list[str]) -> list[str]:
    return sorted(set(left) & set(right))


def _wave_sort_key(row: dict[str, Any]) -> tuple[int, str]:
    wave = str(row.get("wave", "")).strip()
    ordinal = wave_ordinal(row.get("source", ""), row.get("canonical_wave") or wave)
    return (ordinal if ordinal is not None else 10**9, wave)


def build_v553_wave_harmonization_table(descriptors: Iterable[WaveDescriptor | dict[str, Any]]) -> pd.DataFrame:
    bundles = []
    for item in descriptors:
        descriptor = item if isinstance(item, WaveDescriptor) else WaveDescriptor.from_mapping(item)
        bundles.append(_load_wave_bundle(descriptor))
    return pd.DataFrame(bundles)


def build_v553_wave_harmonization_report(table: pd.DataFrame) -> dict[str, Any]:
    source_keys = {
        canonical_family_key(value)
        for value in table.get("source", pd.Series(dtype="object")).dropna()
        if canonical_family_key(value)
    }
    if len(source_keys) > 1:
        raise RuntimeError(
            "V553 harmonization requires one survey family per report; "
            f"found {sorted(source_keys)}"
        )
    source_key = next(iter(source_keys), "")
    source = canonical_family_label(source_key) if source_key else ""
    country_codes = {
        canonical_country_code(value)
        for value in table.get("country_code", pd.Series(dtype="object")).dropna()
        if canonical_country_code(value)
    }
    if len(country_codes) > 1:
        raise RuntimeError(
            "V553 harmonization requires one country per report; "
            f"found {sorted(country_codes)}"
        )
    country_code = next(iter(country_codes), "")
    semantic_frames: list[pd.DataFrame] = []
    directionality_frames: list[pd.DataFrame] = []
    position_frames: list[pd.DataFrame] = []
    for _, row in table.iterrows():
        overlay_paths = row.get("overlay_paths", {}) or {}
        if not isinstance(overlay_paths, dict):
            overlay_paths = {}
        for kind, target in (
            ("semantic", semantic_frames),
            ("directionality", directionality_frames),
            ("position", position_frames),
        ):
            path_text = overlay_paths.get(kind, "")
            if not path_text:
                continue
            frame = _load_frame(Path(path_text))
            if not frame.empty:
                target.append(frame)

    shared_semantic_columns = sorted(
        set(_shared_columns(semantic_frames)) & SEMANTIC_SIGNAL_COLUMNS
    )
    shared_directionality_columns = sorted(
        set(_shared_columns(directionality_frames))
        & DIRECTIONALITY_SIGNAL_COLUMNS
    )
    shared_position_columns = sorted(
        set(_shared_columns(position_frames)) & POSITION_SIGNAL_COLUMNS
    )
    shared_relation_axis_ids = _shared_id_lists(table, "wave_relation_axis_ids")
    shared_target_entity_ids = _shared_id_lists(table, "wave_target_entity_ids")
    shared_driver_facet_ids = _shared_id_lists(table, "wave_driver_facet_ids")
    shared_structural_channel_ids = _shared_id_lists(table, "wave_structural_channel_ids")
    shared_horizon_constraint_ids = _shared_id_lists(table, "wave_horizon_constraint_ids")

    wave_rows = table.to_dict(orient="records")
    sorted_wave_rows = sorted(wave_rows, key=_wave_sort_key)
    wave_names = [str(row.get("wave", "")).strip() for row in wave_rows if str(row.get("wave", "")).strip()]
    wave_status_counts: dict[str, int] = {}
    v552j_readiness_status_counts: dict[str, int] = {}
    v552j_handoff_authority_status_counts: dict[str, int] = {}
    v552j_blocker_context_count = 0
    for row in wave_rows:
        status = _clean_text(row.get("wave_status")) or "unknown"
        wave_status_counts[status] = wave_status_counts.get(status, 0) + 1
        readiness_status = _clean_text(row.get("v552j_readiness_status")) or "unknown"
        v552j_readiness_status_counts[readiness_status] = v552j_readiness_status_counts.get(readiness_status, 0) + 1
        handoff_authority_status = _clean_text(row.get("v552j_handoff_authority_status")) or "unknown"
        v552j_handoff_authority_status_counts[handoff_authority_status] = v552j_handoff_authority_status_counts.get(handoff_authority_status, 0) + 1
        v552j_blocker_context_count += int(row.get("v552j_blocker_context_count", row.get("blocker_count", 0)) or 0)

    ready_for_v553 = bool(
        source_key
        and country_code
        and len(wave_rows) >= 2
        and bool(shared_semantic_columns)
        and bool(shared_directionality_columns)
        and bool(shared_position_columns)
        and all(
            _clean_text(row.get("wave_status")) == "complete"
            for row in wave_rows
        )
    )
    overall_status = "STATUS: READY_FOR_V553_WAVE_HARMONIZATION" if ready_for_v553 else "STATUS: V553_WAVE_HARMONIZATION_NEEDS_MORE_WAVES_OR_SHARED_STRUCTURE"
    if len(wave_rows) < 2:
        overall_status = "STATUS: V553_WAVE_HARMONIZATION_SCAFFOLD_ONLY_SINGLE_WAVE"
    elif not source_key or not country_code:
        overall_status = "STATUS: V553_WAVE_HARMONIZATION_NEEDS_EXPLICIT_IDENTITY"
    elif not shared_semantic_columns:
        overall_status = "STATUS: V553_WAVE_HARMONIZATION_NEEDS_SHARED_SEMANTIC_STRUCTURE"
    elif not shared_directionality_columns:
        overall_status = "STATUS: V553_WAVE_HARMONIZATION_NEEDS_SHARED_DIRECTIONALITY_STRUCTURE"
    elif not shared_position_columns:
        overall_status = "STATUS: V553_WAVE_HARMONIZATION_NEEDS_SHARED_POSITION_STRUCTURE"
    elif not all(
        _clean_text(row.get("wave_status")) == "complete"
        for row in wave_rows
    ):
        overall_status = (
            "STATUS: V553_WAVE_HARMONIZATION_NEEDS_CERTIFIED_WAVE_AUTHORITY"
        )

    wave_pair_evidence: list[dict[str, Any]] = []
    if len(sorted_wave_rows) >= 2:
        for prior_row, current_row in zip(sorted_wave_rows[:-1], sorted_wave_rows[1:]):
            prior_overlay_columns = prior_row.get("overlay_columns", {}) or {}
            current_overlay_columns = current_row.get("overlay_columns", {}) or {}
            if not isinstance(prior_overlay_columns, dict):
                prior_overlay_columns = {}
            if not isinstance(current_overlay_columns, dict):
                current_overlay_columns = {}

            prior_semantic = list(prior_overlay_columns.get("semantic", []) or [])
            current_semantic = list(current_overlay_columns.get("semantic", []) or [])
            prior_directionality = list(prior_overlay_columns.get("directionality", []) or [])
            current_directionality = list(current_overlay_columns.get("directionality", []) or [])
            prior_position = list(prior_overlay_columns.get("position", []) or [])
            current_position = list(current_overlay_columns.get("position", []) or [])

            shared_pair_semantic = sorted(
                set(_pairwise_shared_columns(prior_semantic, current_semantic))
                & SEMANTIC_SIGNAL_COLUMNS
            )
            shared_pair_directionality = sorted(
                set(
                    _pairwise_shared_columns(
                        prior_directionality,
                        current_directionality,
                    )
                )
                & DIRECTIONALITY_SIGNAL_COLUMNS
            )
            shared_pair_position = sorted(
                set(_pairwise_shared_columns(prior_position, current_position))
                & POSITION_SIGNAL_COLUMNS
            )
            shared_pair_relation_axis_ids = _pairwise_shared_id_lists(prior_row.get("wave_relation_axis_ids"), current_row.get("wave_relation_axis_ids"))
            shared_pair_target_entity_ids = _pairwise_shared_id_lists(prior_row.get("wave_target_entity_ids"), current_row.get("wave_target_entity_ids"))
            shared_pair_driver_facet_ids = _pairwise_shared_id_lists(prior_row.get("wave_driver_facet_ids"), current_row.get("wave_driver_facet_ids"))
            shared_pair_structural_channel_ids = _pairwise_shared_id_lists(prior_row.get("wave_structural_channel_ids"), current_row.get("wave_structural_channel_ids"))
            shared_pair_horizon_constraint_ids = _pairwise_shared_id_lists(prior_row.get("wave_horizon_constraint_ids"), current_row.get("wave_horizon_constraint_ids"))
            pair_missing_count = sum(
                1
                for kind in V553_REQUIRED_AUTHORITY_KINDS
                if kind in set(prior_row.get("missing_authority_kinds", []) or [])
                or kind in set(current_row.get("missing_authority_kinds", []) or [])
            )
            pair_status = (
                "aligned"
                if (
                    shared_pair_semantic
                    and shared_pair_directionality
                    and shared_pair_position
                    and pair_missing_count == 0
                )
                else "partial"
            )
            if not shared_pair_semantic:
                pair_status = "insufficient_shared_semantic_structure"
            elif not shared_pair_directionality:
                pair_status = "insufficient_shared_directionality_structure"
            elif not shared_pair_position:
                pair_status = "insufficient_shared_position_structure"

            wave_pair_evidence.append(
                {
                    "run_id": f"{prior_row.get('wave', '')}_to_{current_row.get('wave', '')}",
                    "prior_wave": prior_row.get("wave", ""),
                    "current_wave": current_row.get("wave", ""),
                    "prior_canonical_wave": prior_row.get("canonical_wave", ""),
                    "current_canonical_wave": current_row.get("canonical_wave", ""),
                    "source": prior_row.get("source", ""),
                    "prior_wave_status": prior_row.get("wave_status", ""),
                    "current_wave_status": current_row.get("wave_status", ""),
                    "shared_semantic_columns_json": json.dumps(shared_pair_semantic, sort_keys=True),
                    "shared_directionality_columns_json": json.dumps(shared_pair_directionality, sort_keys=True),
                    "shared_position_columns_json": json.dumps(shared_pair_position, sort_keys=True),
                    "shared_relation_axis_ids_json": json.dumps(shared_pair_relation_axis_ids, sort_keys=True),
                    "shared_target_entity_ids_json": json.dumps(shared_pair_target_entity_ids, sort_keys=True),
                    "shared_driver_facet_ids_json": json.dumps(shared_pair_driver_facet_ids, sort_keys=True),
                    "shared_structural_channel_ids_json": json.dumps(shared_pair_structural_channel_ids, sort_keys=True),
                    "shared_horizon_constraint_ids_json": json.dumps(shared_pair_horizon_constraint_ids, sort_keys=True),
                    "shared_semantic_column_count": len(shared_pair_semantic),
                    "shared_directionality_column_count": len(shared_pair_directionality),
                    "shared_position_column_count": len(shared_pair_position),
                    "shared_relation_axis_id_count": len(shared_pair_relation_axis_ids),
                    "shared_target_entity_id_count": len(shared_pair_target_entity_ids),
                    "shared_driver_facet_id_count": len(shared_pair_driver_facet_ids),
                    "shared_structural_channel_id_count": len(shared_pair_structural_channel_ids),
                    "shared_horizon_constraint_id_count": len(shared_pair_horizon_constraint_ids),
                    "pair_missing_authority_count": pair_missing_count,
                    "pair_harmonization_status": pair_status,
                    "pair_harmonization_score": _bounded_score(
                        (len(shared_pair_semantic) / max(1.0, len(prior_semantic) or 1.0))
                        * 0.5
                        + (len(shared_pair_directionality) / max(1.0, len(prior_directionality) or 1.0)) * 0.25
                        + (len(shared_pair_position) / max(1.0, len(prior_position) or 1.0)) * 0.25
                        - (pair_missing_count * 0.10)
                    ),
                    "created_at": utc_now(),
                    "schema_version": V553_HARMONIZATION_SCHEMA_VERSION,
                    "compiler_version": V553_HARMONIZATION_COMPILER_VERSION,
                }
            )

    per_wave_authority_summary: dict[str, dict[str, Any]] = {}
    per_wave_absence_summary: dict[str, dict[str, Any]] = {}
    per_wave_coverage_summary: dict[str, dict[str, Any]] = {}
    for row in wave_rows:
        wave = _clean_text(row.get("wave"))
        if not wave:
            continue
        overlay_paths = row.get("overlay_paths", {}) or {}
        overlay_row_counts = row.get("overlay_row_counts", {}) or {}
        certified_row_counts = (
            row.get("overlay_certified_row_counts", {}) or {}
        )
        if not isinstance(overlay_paths, dict):
            overlay_paths = {}
        if not isinstance(overlay_row_counts, dict):
            overlay_row_counts = {}
        if not isinstance(certified_row_counts, dict):
            certified_row_counts = {}
        missing = list(row.get("missing_authority_kinds", []) or [])
        per_wave_authority_summary[wave] = {
            "wave_status": row.get("wave_status", ""),
            "thin_status": row.get("thin_status", ""),
            "thin_ready": bool(row.get("thin_ready", False)),
            "thin_layer_count": int(row.get("thin_layer_count", 0) or 0),
            "v552j_readiness_status": row.get("v552j_readiness_status", ""),
            "v552j_blocker_context_count": int(row.get("v552j_blocker_context_count", 0) or 0),
            "v552j_handoff_authority_status": row.get("v552j_handoff_authority_status", ""),
            "missing_authority_kinds": missing,
            "authority_overlay_count": len(
                [
                    kind
                    for kind in V553_REQUIRED_AUTHORITY_KINDS
                    if int(
                        (
                            row.get("overlay_certified_row_counts", {})
                            or {}
                        ).get(kind, 0)
                        or 0
                    )
                    > 0
                ]
            ),
            "authority_overlay_total_count": len(V553_REQUIRED_AUTHORITY_KINDS),
            "shared_relation_axis_id_count": len(row.get("wave_relation_axis_ids", []) or []),
            "shared_target_entity_id_count": len(row.get("wave_target_entity_ids", []) or []),
            "shared_driver_facet_id_count": len(row.get("wave_driver_facet_ids", []) or []),
            "shared_structural_channel_id_count": len(row.get("wave_structural_channel_ids", []) or []),
            "shared_horizon_constraint_id_count": len(row.get("wave_horizon_constraint_ids", []) or []),
        }
        per_wave_absence_summary[wave] = {
            "missing_authority_count": len(missing),
            "missing_authority_kinds": missing,
            "absence_status": "complete" if not missing else "partial",
        }
        per_wave_coverage_summary[wave] = {
            "semantic_rows": int(certified_row_counts.get("semantic", 0) or 0),
            "directionality_rows": int(certified_row_counts.get("directionality", 0) or 0),
            "position_rows": int(certified_row_counts.get("position", 0) or 0),
            "raw_semantic_rows": int(overlay_row_counts.get("semantic", 0) or 0),
            "raw_directionality_rows": int(overlay_row_counts.get("directionality", 0) or 0),
            "raw_position_rows": int(overlay_row_counts.get("position", 0) or 0),
            "authority_overlay_count": len(
                [
                    kind
                    for kind in V553_REQUIRED_AUTHORITY_KINDS
                    if int(
                        (
                            row.get("overlay_certified_row_counts", {})
                            or {}
                        ).get(kind, 0)
                        or 0
                    )
                    > 0
                ]
            ),
            "relation_axis_ids": list(row.get("wave_relation_axis_ids", []) or []),
            "target_entity_ids": list(row.get("wave_target_entity_ids", []) or []),
            "driver_facet_ids": list(row.get("wave_driver_facet_ids", []) or []),
            "structural_channel_ids": list(row.get("wave_structural_channel_ids", []) or []),
            "horizon_constraint_ids": list(row.get("wave_horizon_constraint_ids", []) or []),
            "coverage_status": "complete" if not missing else "partial",
        }

    cross_wave_comparability_matrix: list[dict[str, Any]] = []
    cross_wave_noncomparability_matrix: list[dict[str, Any]] = []
    for evidence in wave_pair_evidence:
        pair_status = _clean_text(evidence.get("pair_harmonization_status")) or "unknown"
        pair_missing_count = int(evidence.get("pair_missing_authority_count", 0) or 0)
        matrix_row = {
            "prior_wave": evidence.get("prior_wave", ""),
            "current_wave": evidence.get("current_wave", ""),
            "shared_semantic_column_count": int(evidence.get("shared_semantic_column_count", 0) or 0),
            "shared_directionality_column_count": int(evidence.get("shared_directionality_column_count", 0) or 0),
            "shared_position_column_count": int(evidence.get("shared_position_column_count", 0) or 0),
            "shared_relation_axis_id_count": int(evidence.get("shared_relation_axis_id_count", 0) or 0),
            "shared_target_entity_id_count": int(evidence.get("shared_target_entity_id_count", 0) or 0),
            "shared_driver_facet_id_count": int(evidence.get("shared_driver_facet_id_count", 0) or 0),
            "shared_structural_channel_id_count": int(evidence.get("shared_structural_channel_id_count", 0) or 0),
            "shared_horizon_constraint_id_count": int(evidence.get("shared_horizon_constraint_id_count", 0) or 0),
            "pair_missing_authority_count": pair_missing_count,
            "comparability_status": "comparable" if pair_status == "aligned" and pair_missing_count == 0 else "partial",
            "wave_pair_evidence_score": float(evidence.get("pair_harmonization_score", 0.0) or 0.0),
        }
        cross_wave_comparability_matrix.append(matrix_row)
        if pair_missing_count > 0 or pair_status != "aligned":
            cross_wave_noncomparability_matrix.append(
                {
                    **matrix_row,
                    "noncomparability_reason": pair_status,
                }
            )

    required_authority_kinds = list(V553_REQUIRED_AUTHORITY_KINDS)
    wave_authority_coverage: dict[str, dict[str, int]] = {}
    for row in wave_rows:
        wave = _clean_text(row.get("wave"))
        if not wave:
            continue
        wave_authority_coverage[wave] = {
            kind: int(
                int(
                    (row.get("overlay_certified_row_counts", {}) or {}).get(
                        kind,
                        0,
                    )
                    or 0
                )
                > 0
            )
            for kind in V553_REQUIRED_AUTHORITY_KINDS
        }

    if wave_rows:
        wave_coverage_score = _bounded_score(len(wave_rows) / max(2.0, len(wave_rows)))
        shared_semantic_score = _bounded_score(min(1.0, len(shared_semantic_columns) / 5.0))
        shared_directionality_score = _bounded_score(min(1.0, len(shared_directionality_columns) / 5.0))
        shared_position_score = _bounded_score(min(1.0, len(shared_position_columns) / 5.0))
        overlay_presence_score = _bounded_score(
            sum(sum(int(v) for v in coverage.values()) for coverage in wave_authority_coverage.values())
            / max(1.0, len(wave_rows) * len(required_authority_kinds))
        )
    else:
        wave_coverage_score = 0.0
        shared_semantic_score = 0.0
        shared_directionality_score = 0.0
        shared_position_score = 0.0
        overlay_presence_score = 0.0

    harmonization_score = _bounded_score(
        (0.30 * wave_coverage_score)
        + (0.30 * shared_semantic_score)
        + (0.15 * shared_directionality_score)
        + (0.15 * shared_position_score)
        + (0.10 * overlay_presence_score)
    )
    readiness_score = _bounded_score(
        harmonization_score
        + (0.10 if ready_for_v553 else -0.15)
    )

    difference_rows = []
    for row in wave_rows:
        missing = list(row.get("missing_authority_kinds", []) or [])
        difference_rows.append(
            {
                "wave": row.get("wave", ""),
                "source": row.get("source", ""),
                "canonical_wave": row.get("canonical_wave", ""),
                "wave_status": row.get("wave_status", ""),
                "missing_authority_kinds_json": json.dumps(missing, sort_keys=True),
                "semantic_overlay_rows": int((row.get("overlay_row_counts", {}) or {}).get("semantic", 0) or 0),
                "directionality_overlay_rows": int((row.get("overlay_row_counts", {}) or {}).get("directionality", 0) or 0),
                "position_overlay_rows": int((row.get("overlay_row_counts", {}) or {}).get("position", 0) or 0),
                "shared_relation_axis_ids_json": json.dumps(list(row.get("wave_relation_axis_ids", []) or []), sort_keys=True),
                "shared_target_entity_ids_json": json.dumps(list(row.get("wave_target_entity_ids", []) or []), sort_keys=True),
                "shared_driver_facet_ids_json": json.dumps(list(row.get("wave_driver_facet_ids", []) or []), sort_keys=True),
                "shared_structural_channel_ids_json": json.dumps(list(row.get("wave_structural_channel_ids", []) or []), sort_keys=True),
                "shared_horizon_constraint_ids_json": json.dumps(list(row.get("wave_horizon_constraint_ids", []) or []), sort_keys=True),
                "shared_relation_axis_id_count": len(row.get("wave_relation_axis_ids", []) or []),
                "shared_target_entity_id_count": len(row.get("wave_target_entity_ids", []) or []),
                "shared_driver_facet_id_count": len(row.get("wave_driver_facet_ids", []) or []),
                "shared_structural_channel_id_count": len(row.get("wave_structural_channel_ids", []) or []),
                "shared_horizon_constraint_id_count": len(row.get("wave_horizon_constraint_ids", []) or []),
                "difference_kind": "shared_temporal_authority_surface",
                "difference_reason": "wave-specific authority and structural id inventory",
                "thin_status": row.get("thin_status", ""),
                "thin_ready": bool(row.get("thin_ready", False)),
                "thin_layer_count": int(row.get("thin_layer_count", 0) or 0),
                "v552j_readiness_status": row.get("v552j_readiness_status", ""),
                "v552j_blocker_context_count": int(row.get("v552j_blocker_context_count", 0) or 0),
                "v552j_handoff_authority_status": row.get("v552j_handoff_authority_status", ""),
            }
        )

    report = {
        "schema_version": V553_HARMONIZATION_SCHEMA_VERSION,
        "compiler_version": V553_HARMONIZATION_COMPILER_VERSION,
        "created_at": utc_now(),
        "source": source,
        "source_family": source,
        "country_code": country_code,
        "required_authority_kinds": required_authority_kinds,
        "required_shared_structure": list(V553_REQUIRED_SHARED_STRUCTURE),
        "blocking_conditions": [
            "at_least_two_waves",
            "one_explicit_survey_family_and_country",
            "shared_semantic_directionality_and_position_signal_columns",
            "wave_specific_certified_authority_rows",
        ],
        "wave_count": int(len(wave_rows)),
        "multiple_waves_present": len(wave_rows) >= 2,
        "wave_names": wave_names,
        "harmonization_scope": "multi_wave_authority_comparison" if len(wave_rows) >= 2 else "single_wave_scaffold",
        "comparison_authority_status": "multi_wave_authorized" if ready_for_v553 else "insufficient_multi_wave_authority",
        "authority_overlay_coverage": wave_authority_coverage,
        "ready_for_v553": ready_for_v553,
        "wave_coverage_score": wave_coverage_score,
        "shared_semantic_score": shared_semantic_score,
        "shared_directionality_score": shared_directionality_score,
        "shared_position_score": shared_position_score,
        "overlay_presence_score": overlay_presence_score,
        "harmonization_score": harmonization_score,
        "readiness_score": readiness_score,
        "overall_status": overall_status,
        "comparability_status": "comparability_authorized" if ready_for_v553 else "comparability_limited",
        "wave_status_counts": wave_status_counts,
        "v552j_readiness_status_counts": v552j_readiness_status_counts,
        "v552j_handoff_authority_status_counts": v552j_handoff_authority_status_counts,
        "v552j_blocker_context_count": v552j_blocker_context_count,
        "shared_semantic_columns": shared_semantic_columns,
        "shared_directionality_columns": shared_directionality_columns,
        "shared_position_columns": shared_position_columns,
        "shared_relation_axis_ids": shared_relation_axis_ids,
        "shared_target_entity_ids": shared_target_entity_ids,
        "shared_driver_facet_ids": shared_driver_facet_ids,
        "shared_structural_channel_ids": shared_structural_channel_ids,
        "shared_horizon_constraint_ids": shared_horizon_constraint_ids,
        "wave_rows": wave_rows,
        "per_wave_authority_summary": per_wave_authority_summary,
        "per_wave_absence_summary": per_wave_absence_summary,
        "per_wave_coverage_summary": per_wave_coverage_summary,
        "cross_wave_comparability_matrix": cross_wave_comparability_matrix,
        "cross_wave_noncomparability_matrix": cross_wave_noncomparability_matrix,
        "wave_pair_evidence": wave_pair_evidence,
        "wave_pair_count": len(wave_pair_evidence),
        "wave_differences": difference_rows,
    }
    return report


def validate_v553_wave_harmonization_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not canonical_family_key(report.get("source")):
        errors.append("v553 wave harmonization missing explicit source")
    if not canonical_country_code(report.get("country_code")):
        errors.append("v553 wave harmonization missing explicit country_code")
    if int(report.get("wave_count", 0) or 0) < 2:
        errors.append("v553 wave harmonization requires at least two waves for full temporal validation")
    if not report.get("shared_semantic_columns"):
        errors.append("v553 wave harmonization missing shared semantic columns")
    if not report.get("shared_directionality_columns"):
        errors.append("v553 wave harmonization missing shared directionality columns")
    if not report.get("shared_position_columns"):
        errors.append("v553 wave harmonization missing shared position columns")
    for key in (
        "shared_relation_axis_ids",
        "shared_target_entity_ids",
        "shared_driver_facet_ids",
        "shared_structural_channel_ids",
        "shared_horizon_constraint_ids",
    ):
        if key not in report or not isinstance(report.get(key), list):
            errors.append(f"v553 wave harmonization missing {key}")
    if not report.get("required_authority_kinds"):
        errors.append("v553 wave harmonization missing required authority kinds")
    if not report.get("wave_names"):
        errors.append("v553 wave harmonization missing wave names")
    if int(report.get("wave_count", 0) or 0) >= 2 and not report.get("wave_pair_evidence"):
        errors.append("v553 wave harmonization missing wave-to-wave evidence")
    wave_rows = report.get("wave_rows", [])
    if not isinstance(wave_rows, list) or not wave_rows:
        errors.append("v553 wave harmonization missing wave rows")
    wave_pair_evidence = report.get("wave_pair_evidence", [])
    if wave_pair_evidence and not isinstance(wave_pair_evidence, list):
        errors.append("v553 wave harmonization evidence must be a list")
    if wave_pair_evidence and int(report.get("wave_pair_evidence_row_count", len(wave_pair_evidence)) or 0) != len(wave_pair_evidence):
        errors.append("v553 wave harmonization evidence row count mismatch")
    for row in wave_rows if isinstance(wave_rows, list) else []:
        missing = row.get("missing_authority_kinds", [])
        if not isinstance(missing, list):
            errors.append(f"wave {row.get('wave', '')}: missing_authority_kinds must be a list")
        elif missing:
            errors.append(
                f"wave {row.get('wave', '')}: missing certified authority kinds {missing}"
            )
    for evidence in wave_pair_evidence if isinstance(wave_pair_evidence, list) else []:
        if not isinstance(evidence, dict):
            errors.append("v553 wave pair evidence must contain objects")
            break
    return errors


def build_v553_wave_harmonization(descriptors: Iterable[WaveDescriptor | dict[str, Any]]) -> tuple[pd.DataFrame, dict[str, Any]]:
    table = build_v553_wave_harmonization_table(descriptors)
    report = build_v553_wave_harmonization_report(table)
    return table, report


__all__ = [
    "V553_HARMONIZATION_SCHEMA_VERSION",
    "V553_HARMONIZATION_COMPILER_VERSION",
    "WaveDescriptor",
    "build_v553_wave_harmonization_table",
    "build_v553_wave_harmonization_report",
    "build_v553_wave_harmonization",
    "validate_v553_wave_harmonization_report",
]
