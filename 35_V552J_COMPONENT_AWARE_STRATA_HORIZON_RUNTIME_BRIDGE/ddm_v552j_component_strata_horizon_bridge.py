#!/usr/bin/env python3
"""Component-aware V552 question-semantic hierarchy bridge for V551J joint packets.

This module refuses to collapse joint-packet components into a scalar strata/horizon
claim unless every packet component is matched and the authoritative values are
unanimous. The component vector remains the primary authority surface.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pandas as pd

BRIDGE_VERSION = "v3.1"
COMPONENT_VECTOR_COLUMN = "component_response_vector_json"
QUESTION_ID_FIELDS = ("v551_question_id", "v550j_item_question_id")
VAR_CODE_FIELDS = ("v551_var_code", "v550j_item_var_code")
AUTHORITY_FIELDS = (
    "question_semantic_hierarchy_id",
    "facet_id", "facet_label", "driver_id", "driver_label",
    "stratum_id", "stratum_label", "strata_relevance", "strata_path",
    "conditional_strata_weights", "position_conditioning", "position_modifiers",
    "position_conditioning_confidence", "horizon_affordance", "horizon_type",
    "horizon_scope", "horizon_openness", "horizon_reach", "horizon_durability",
    "horizon_enemy_relation", "horizon_valence", "horizon_sustaining_power",
    "relation_axis_id", "target_entity_id", "semantic_role", "semantic_subrole",
    "semantic_confidence", "semantic_note", "support_status", "confidence_tier",
    "basis", "status",
)
SCALAR_SUMMARY_FIELDS = (
    "stratum_id", "stratum_label", "strata_path", "conditional_strata_weights",
    "position_conditioning", "position_modifiers", "horizon_affordance",
    "horizon_type", "horizon_scope", "horizon_openness", "horizon_reach",
    "horizon_durability", "horizon_enemy_relation", "horizon_valence",
    "horizon_sustaining_power",
)


def _clean(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def _norm(value: Any) -> str:
    return _clean(value).casefold()


def _parse_component_vector(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        raw = value
    else:
        text = _clean(value)
        if not text:
            raise ValueError("missing component_response_vector_json")
        try:
            raw = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid component_response_vector_json: {exc}") from exc
    if not isinstance(raw, list) or not raw:
        raise ValueError("component_response_vector_json must be a non-empty list")
    out: list[dict[str, Any]] = []
    seen_orders: set[int] = set()
    for idx, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"component {idx} is not an object")
        try:
            order = int(item.get("item_order", idx))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"component {idx} has invalid item_order") from exc
        if order <= 0 or order in seen_orders:
            raise ValueError("component item_order must be positive and unique within packet")
        seen_orders.add(order)
        question_id = next((_clean(item.get(k)) for k in QUESTION_ID_FIELDS if _clean(item.get(k))), "")
        var_code = next((_clean(item.get(k)) for k in VAR_CODE_FIELDS if _clean(item.get(k))), "")
        if not question_id and not var_code:
            raise ValueError(f"component {order} has neither question id nor variable code")
        normalized = dict(item)
        normalized["item_order"] = order
        normalized["component_question_id"] = question_id
        normalized["component_var_code"] = var_code
        out.append(normalized)
    return sorted(out, key=lambda x: x["item_order"])


@dataclass(frozen=True)
class QshIndexes:
    by_question: dict[str, dict[str, Any]]
    by_scope_var: dict[tuple[str, str, str, str], dict[str, Any]]


def build_qsh_indexes(qsh: pd.DataFrame) -> QshIndexes:
    required = {"source", "wave", "country_code", "question_id", "var_code", *AUTHORITY_FIELDS}
    missing = sorted(required - set(qsh.columns))
    if missing:
        raise ValueError(f"QSH missing required columns: {missing}")
    by_question: dict[str, dict[str, Any]] = {}
    by_scope_var: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for _, row in qsh.iterrows():
        record = row.to_dict()
        qkey = _norm(record.get("question_id"))
        if qkey:
            if qkey in by_question:
                raise ValueError(f"duplicate normalized QSH question_id: {record.get('question_id')!r}")
            by_question[qkey] = record
        skey = tuple(_norm(record.get(k)) for k in ("source", "wave", "country_code", "var_code"))
        if all(skey):
            if skey in by_scope_var:
                raise ValueError(f"duplicate normalized QSH scope/var key: {skey!r}")
            by_scope_var[skey] = record
    return QshIndexes(by_question=by_question, by_scope_var=by_scope_var)


def _match_component(component: dict[str, Any], packet: dict[str, Any], indexes: QshIndexes) -> tuple[str, dict[str, Any] | None]:
    qkey = _norm(component.get("component_question_id"))
    if qkey and qkey in indexes.by_question:
        return "MATCHED_BY_QUESTION_ID", indexes.by_question[qkey]
    skey = (
        _norm(packet.get("source")),
        _norm(packet.get("wave") or packet.get("canonical_wave")),
        _norm(packet.get("country_code")),
        _norm(component.get("component_var_code")),
    )
    if all(skey) and skey in indexes.by_scope_var:
        return "MATCHED_BY_SCOPE_VAR", indexes.by_scope_var[skey]
    return "UNMATCHED_COMPONENT", None


def build_component_bridge(certified_packets: pd.DataFrame, qsh: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    required_packet = {"packet_id", COMPONENT_VECTOR_COLUMN, "source", "wave", "country_code"}
    missing = sorted(required_packet - set(certified_packets.columns))
    if missing:
        raise ValueError(f"certified packet index missing required columns: {missing}")
    if certified_packets["packet_id"].map(_clean).eq("").any():
        raise ValueError("blank packet_id")
    if certified_packets["packet_id"].map(_norm).duplicated().any():
        raise ValueError("duplicate normalized packet_id")
    indexes = build_qsh_indexes(qsh)
    component_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []

    for _, prow in certified_packets.iterrows():
        packet = prow.to_dict()
        packet_id = _clean(packet["packet_id"])
        components = _parse_component_vector(packet[COMPONENT_VECTOR_COLUMN])
        packet_component_records: list[dict[str, Any]] = []
        for component in components:
            match_status, match = _match_component(component, packet, indexes)
            row = {
                "bridge_version": BRIDGE_VERSION,
                "packet_id": packet_id,
                "source": _clean(packet.get("source")),
                "wave": _clean(packet.get("wave")),
                "canonical_wave": _clean(packet.get("canonical_wave")),
                "country_code": _clean(packet.get("country_code")),
                "item_order": component["item_order"],
                "component_question_id": _clean(component.get("component_question_id")),
                "component_var_code": _clean(component.get("component_var_code")),
                "component_response_value_normalized": _clean(component.get("v550j_item_response_value_normalized")),
                "qsh_match_status": match_status,
            }
            for field in AUTHORITY_FIELDS:
                row[field] = _clean(match.get(field)) if match else ""
            component_rows.append(row)
            packet_component_records.append(row)

        matched = [r for r in packet_component_records if r["qsh_match_status"].startswith("MATCHED_")]
        unmatched = [r for r in packet_component_records if r["qsh_match_status"] == "UNMATCHED_COMPONENT"]
        vector = []
        for r in packet_component_records:
            vector.append({
                "item_order": r["item_order"],
                "question_id": r["component_question_id"],
                "var_code": r["component_var_code"],
                "match_status": r["qsh_match_status"],
                **{f: r[f] for f in AUTHORITY_FIELDS},
            })

        unique_map: dict[str, list[str]] = {}
        scalar_map: dict[str, str] = {}
        for field in SCALAR_SUMMARY_FIELDS:
            vals = sorted({_clean(r[field]) for r in matched if _clean(r[field])})
            unique_map[field] = vals
            scalar_map[f"packet_{field}"] = vals[0] if len(matched) == len(components) and len(vals) == 1 else ""

        if not matched:
            authority_status = "NO_COMPONENT_STRATA_HORIZON_AUTHORITY"
        elif unmatched:
            authority_status = "PARTIAL_COMPONENT_STRATA_HORIZON_AUTHORITY"
        elif any(len(vals) > 1 for vals in unique_map.values()):
            authority_status = "COMPLETE_HETEROGENEOUS_COMPONENT_AUTHORITY"
        else:
            authority_status = "COMPLETE_HOMOGENEOUS_COMPONENT_AUTHORITY"
        summary_rows.append({
            "bridge_version": BRIDGE_VERSION,
            "packet_id": packet_id,
            "source": _clean(packet.get("source")),
            "wave": _clean(packet.get("wave")),
            "canonical_wave": _clean(packet.get("canonical_wave")),
            "country_code": _clean(packet.get("country_code")),
            "component_count": len(components),
            "matched_component_count": len(matched),
            "unmatched_component_count": len(unmatched),
            "component_match_coverage": len(matched) / len(components),
            "component_strata_horizon_authority_status": authority_status,
            "component_strata_horizon_vector_json": json.dumps(vector, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            "component_strata_horizon_unique_values_json": json.dumps(unique_map, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            **scalar_map,
        })

    component_df = pd.DataFrame(component_rows)
    summary_df = pd.DataFrame(summary_rows)
    if len(summary_df) != len(certified_packets):
        raise AssertionError("packet summary cardinality changed")
    expected_components = sum(len(_parse_component_vector(v)) for v in certified_packets[COMPONENT_VECTOR_COLUMN])
    if len(component_df) != expected_components:
        raise AssertionError("component cardinality changed")
    report = {
        "bridge_version": BRIDGE_VERSION,
        "packet_rows": int(len(certified_packets)),
        "component_rows": int(len(component_df)),
        "matched_component_rows": int(component_df["qsh_match_status"].str.startswith("MATCHED_").sum()),
        "unmatched_component_rows": int(component_df["qsh_match_status"].eq("UNMATCHED_COMPONENT").sum()),
        "packet_status_counts": {str(k): int(v) for k, v in summary_df["component_strata_horizon_authority_status"].value_counts().sort_index().items()},
        "scalar_flattening_rule": "ONLY_COMPLETE_COVERAGE_AND_UNANIMOUS_NONEMPTY_VALUE",
        "primary_authority_surface": "component_strata_horizon_vector_json",
    }
    return component_df, summary_df, report


def enrich_packet_index(packet_index: pd.DataFrame, packet_summary: pd.DataFrame) -> pd.DataFrame:
    if "packet_id" not in packet_index.columns or "packet_id" not in packet_summary.columns:
        raise ValueError("packet_id required")
    packet_keys = packet_index["packet_id"].map(_norm)
    summary_keys = packet_summary["packet_id"].map(_norm)
    if packet_keys.eq("").any():
        raise ValueError("blank packet index packet_id")
    if summary_keys.eq("").any():
        raise ValueError("blank packet summary packet_id")
    if packet_keys.duplicated().any():
        raise ValueError("duplicate normalized packet index packet_id")
    if summary_keys.duplicated().any():
        raise ValueError("duplicate normalized packet summary packet_id")
    packet_key_set = set(packet_keys)
    summary_key_set = set(summary_keys)
    orphan_summary = sorted(summary_key_set - packet_key_set)
    missing_summary = sorted(packet_key_set - summary_key_set)
    if orphan_summary:
        raise ValueError(f"orphan packet summary packet_id keys: {orphan_summary[:5]}")
    if missing_summary:
        raise ValueError(f"missing packet summary packet_id keys: {missing_summary[:5]}")

    out = packet_index.copy()
    out["__order"] = range(len(out))
    out["__packet_key"] = packet_keys
    summary = packet_summary.copy()
    summary["__packet_key"] = summary_keys
    payload_cols = [c for c in summary.columns if c not in {"packet_id", "source", "wave", "canonical_wave", "country_code", "__packet_key"}]
    collisions = sorted(set(payload_cols) & set(out.columns))
    if collisions:
        raise ValueError(f"packet enrichment column collisions: {collisions}")
    out = out.merge(summary[["__packet_key", *payload_cols]], on="__packet_key", how="left", validate="one_to_one")
    out = out.sort_values("__order", kind="stable").drop(columns=["__order", "__packet_key"]).reset_index(drop=True)
    if len(out) != len(packet_index):
        raise AssertionError("packet row count changed")
    return out
