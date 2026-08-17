#!/usr/bin/env python3
"""Canonical V552J consumer adapter for V553 wave harmonization.

POSTG5-004 closed the V552J producer contract on the current structural
join/input/handoff indexes. V553 therefore derives structural inventories and
handoff authority from those artifacts rather than requiring the deleted
``v552j_structural_handoff_packet.json`` compatibility packet.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy.ddm_v553_harmonization import (
    WaveDescriptor,
    build_v553_wave_harmonization_report,
    build_v553_wave_harmonization_table as _build_legacy_table,
)

_CANONICAL_INPUT = Path("packets/v552j_v553_input_index.parquet")
_CANONICAL_HANDOFF = Path("packets/v552j_to_v553_handoff_index.parquet")
_CANONICAL_HANDOFF_MANIFEST = Path("manifest/v552j_v553_handoff_manifest.json")
_CANONICAL_READINESS = Path("manifest/v552j_readiness_report.json")


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _read_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _read_parquet(path: Path | None) -> pd.DataFrame:
    if path is None or not path.exists():
        return pd.DataFrame()
    try:
        frame = pd.read_parquet(path)
    except Exception:
        return pd.DataFrame()
    return frame if isinstance(frame, pd.DataFrame) else pd.DataFrame()


def _resolve(path_text: Any, root: Path | None) -> Path | None:
    text = _clean(path_text)
    if not text:
        return None
    path = Path(text)
    if path.is_absolute() or root is None:
        return path
    return root / path


def _descriptor_mapping(item: WaveDescriptor | dict[str, Any]) -> dict[str, Any]:
    descriptor = item if isinstance(item, WaveDescriptor) else WaveDescriptor.from_mapping(item)
    return dict(descriptor.normalized().__dict__)


def _collect_ids(frames: Iterable[pd.DataFrame], columns: Iterable[str]) -> list[str]:
    values: set[str] = set()
    for frame in frames:
        if frame is None or frame.empty:
            continue
        for column in columns:
            if column not in frame.columns:
                continue
            for raw in frame[column].tolist():
                if isinstance(raw, (list, tuple, set)):
                    values.update(_clean(value) for value in raw if _clean(value))
                    continue
                text = _clean(raw)
                if not text:
                    continue
                try:
                    parsed = json.loads(text)
                except Exception:
                    parsed = None
                if isinstance(parsed, list):
                    values.update(_clean(value) for value in parsed if _clean(value))
                else:
                    values.add(text)
    return sorted(values)


def _canonical_context(item: WaveDescriptor | dict[str, Any]) -> dict[str, Any]:
    mapping = _descriptor_mapping(item)
    root_text = _clean(mapping.get("latest_v552j_root")) or _clean(mapping.get("v552j_run_root"))
    root = Path(root_text) if root_text else None

    readiness_path = _resolve(
        mapping.get("v552j_readiness_report_path") or mapping.get("latest_v552j_readiness_report"),
        root,
    )
    if readiness_path is None and root is not None:
        readiness_path = root / _CANONICAL_READINESS
    readiness = _read_json(readiness_path)

    handoff_manifest_path = _resolve(mapping.get("v552j_handoff_manifest_path"), root)
    if handoff_manifest_path is None and root is not None:
        handoff_manifest_path = root / _CANONICAL_HANDOFF_MANIFEST
    handoff_manifest = _read_json(handoff_manifest_path)

    input_path = _resolve(mapping.get("v552j_v553_input_index_path"), root)
    if input_path is None:
        input_path = _resolve(handoff_manifest.get("v553_input_index_path"), root)
    if input_path is None and root is not None:
        input_path = root / _CANONICAL_INPUT

    handoff_path = _resolve(mapping.get("v552j_to_v553_handoff_index_path"), root)
    if handoff_path is None and root is not None:
        handoff_path = root / _CANONICAL_HANDOFF

    input_df = _read_parquet(input_path)
    handoff_df = _read_parquet(handoff_path)
    frames = [input_df, handoff_df]

    status = _clean(readiness.get("status")) or _clean(readiness.get("structural_handoff_status"))
    permission = _clean(handoff_manifest.get("downstream_permission_status")) or _clean(
        readiness.get("downstream_permission_status")
    )

    return {
        "root": str(root) if root else "",
        "readiness_path": str(readiness_path) if readiness_path else "",
        "handoff_manifest_path": str(handoff_manifest_path) if handoff_manifest_path else "",
        "input_path": str(input_path) if input_path else "",
        "handoff_path": str(handoff_path) if handoff_path else "",
        "surface_present": bool((input_path and input_path.exists()) or (handoff_path and handoff_path.exists())),
        "readiness_status": status,
        "handoff_authority_status": permission or status or "unknown",
        "blocker_context_count": int(readiness.get("blocker_context_count", 0) or 0),
        "blocker_context_breakdown_json": _clean(readiness.get("blocker_context_breakdown_json")),
        "relation_axis_ids": _collect_ids(frames, ("relation_axis_id", "relation_axis_ids_json")),
        "target_entity_ids": _collect_ids(frames, ("target_entity_id", "target_entity_ids_json")),
        "driver_facet_ids": _collect_ids(frames, ("driver_facet_id", "driver_facet_ids_json")),
        "structural_channel_ids": _collect_ids(frames, ("structural_channel_id", "structural_channel_ids_json")),
        "horizon_constraint_ids": _collect_ids(frames, ("horizon_constraint_id", "horizon_constraint_ids_json")),
    }


def build_v553_wave_harmonization(
    descriptors: Iterable[WaveDescriptor | dict[str, Any]],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Build harmonization while binding V552J context to its canonical surface.

    The pre-POSTG5 harmonizer remains responsible for authority-overlay and
    cross-wave comparison mechanics. This adapter replaces the structural
    inventory/status inputs that it formerly obtained through the deleted
    compatibility packet with values read directly from current V552J indexes
    and manifests.
    """
    items = list(descriptors)
    table = _build_legacy_table(items)
    contexts = [_canonical_context(item) for item in items]

    for index, context in enumerate(contexts):
        if index >= len(table):
            break
        table.at[index, "v552j_v553_input_index_path"] = context["input_path"]
        table.at[index, "v552j_to_v553_handoff_index_path"] = context["handoff_path"]
        table.at[index, "v552j_handoff_manifest_path"] = context["handoff_manifest_path"]
        table.at[index, "v552j_consumer_surface"] = "canonical_v552j_input_handoff_indexes"
        table.at[index, "obsolete_v552j_structural_handoff_packet_required"] = False
        if context["readiness_status"]:
            table.at[index, "v552j_readiness_status"] = context["readiness_status"]
        if context["handoff_authority_status"]:
            table.at[index, "v552j_handoff_authority_status"] = context["handoff_authority_status"]
        table.at[index, "v552j_blocker_context_count"] = context["blocker_context_count"]
        table.at[index, "v552j_blocker_context_breakdown_json"] = context["blocker_context_breakdown_json"]
        if context["surface_present"]:
            table.at[index, "wave_relation_axis_ids"] = context["relation_axis_ids"]
            table.at[index, "wave_target_entity_ids"] = context["target_entity_ids"]
            table.at[index, "wave_driver_facet_ids"] = context["driver_facet_ids"]
            table.at[index, "wave_structural_channel_ids"] = context["structural_channel_ids"]
            table.at[index, "wave_horizon_constraint_ids"] = context["horizon_constraint_ids"]

    report = build_v553_wave_harmonization_report(table)
    report["v552j_consumer_surface"] = "canonical_v552j_input_handoff_indexes"
    report["obsolete_v552j_structural_handoff_packet_required"] = False
    report["v552j_canonical_surface_by_wave"] = [
        {
            "wave": _clean(table.iloc[index].get("wave")) if index < len(table) else "",
            "input_index_path": context["input_path"],
            "handoff_index_path": context["handoff_path"],
            "handoff_manifest_path": context["handoff_manifest_path"],
            "surface_present": context["surface_present"],
        }
        for index, context in enumerate(contexts)
    ]
    return table, report


__all__ = ["build_v553_wave_harmonization"]
