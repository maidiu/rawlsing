#!/usr/bin/env python3
"""Build-standard helpers for the Rawlsing V5 thin path.

The standard is intentionally explicit about three things:

1. what kind of artifact a build step produced,
2. how provisional or scaffolded it is, and
3. how much continuity was actually checked upstream and downstream.

The goal is to keep thin builds honest about their limits instead of silently
presenting scaffolds as finished semantic layers.
"""

from __future__ import annotations

from typing import Any

from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text

IMPLEMENTATION_KINDS = {
    "certified",
    "reviewable",
    "diagnostic",
    "thin_scaffold",
    "provisional",
    "blocked",
}

CONTINUITY_LEVELS = {
    "not_checked",
    "presence_only",
    "artifact_shape",
    "contract_shape",
    "semantic_chain",
    "cross_wave",
}

CONTINUITY_RESULTS = {
    "pass",
    "partial",
    "blocked",
    "not_checked",
}


def _status_to_provisionality(status: str) -> str:
    if status == "THIN_BLOCKED_MISSING_REQUIRED_INPUT":
        return "blocked"
    if status == "THIN_READY_WITH_INPUT_GAPS":
        return "provisional"
    return "thin_scaffold"


def _continuity_result(status: str, *, checked: bool = True) -> str:
    if not checked:
        return "not_checked"
    if status == "THIN_BLOCKED_MISSING_REQUIRED_INPUT":
        return "blocked"
    if status == "THIN_READY_WITH_INPUT_GAPS":
        return "partial"
    return "pass"


def build_layer_build_record(*, spec: Any, input_inspection: dict[str, Any], status: str, packet_path: str, schema_path: str, audit_path: str, readiness_path: str, input_manifest_path: str, run_id: str) -> dict[str, Any]:
    """Create a reproducible build record for one thin layer."""

    provisionality = _status_to_provisionality(status)
    upstream_continuity = _continuity_result(status, checked=True)
    downstream_continuity = "not_checked"
    continuity_checked_full = False

    record = {
        "run_id": run_id,
        "layer": spec.layer,
        "title": spec.title,
        "artifact_type": spec.artifact_slug,
        "implementation_kind": "thin_scaffold",
        "provisionality": provisionality,
        "scaffold_level": "boundary_contract_only",
        "status": status,
        "input_status": input_inspection["input_status"],
        "missing_required_inputs": list(input_inspection["missing_required_inputs"]),
        "stop_missing_inputs": list(input_inspection["stop_missing_inputs"]),
        "continuity_checked_full": continuity_checked_full,
        "upstream_continuity_scope": "artifact_presence_and_contract_shape",
        "upstream_continuity_result": upstream_continuity,
        "downstream_continuity_scope": "not_checked_in_thin_build",
        "downstream_continuity_result": downstream_continuity,
        "full_upstream_and_downstream_continuity_checked": False,
        "how_built": [
            "inspect required inputs against the layer contract",
            "classify the layer as ready, provisional, or blocked",
            "materialize the contract payload without semantic deepening",
            "write packet, schema, audit, input manifest, and readiness report",
            "record the build in the thin build ledger",
        ],
        "artifact_paths": {
            "packet_path": repo_relative_path_text(packet_path),
            "schema_path": repo_relative_path_text(schema_path),
            "audit_path": repo_relative_path_text(audit_path),
            "readiness_path": repo_relative_path_text(readiness_path),
            "input_manifest_path": repo_relative_path_text(input_manifest_path),
        },
        "continuity_notes": [
            "Upstream continuity is checked only at contract/artifact presence level in the thin build.",
            "Downstream continuity is projected by contract but not semantically validated in the thin build.",
        ],
    }
    return record


def build_review_gate_record(
    *,
    run_id: str,
    layer: str,
    title: str,
    artifact_type: str,
    status: str,
    input_inspection: dict[str, Any],
    artifact_paths: dict[str, str],
    how_built: list[str],
    continuity_notes: list[str],
    upstream_continuity_scope: str = "artifact_presence_and_contract_shape",
    downstream_continuity_scope: str = "not_checked_in_review_gate",
    scaffold_level: str = "review_boundary",
) -> dict[str, Any]:
    """Create a reproducible build record for a review-gate artifact."""

    if status.startswith("BLOCKED"):
        implementation_kind = "blocked"
        provisionality = "blocked"
        upstream_continuity_result = "blocked"
    else:
        implementation_kind = "reviewable"
        provisionality = "provisional"
        upstream_continuity_result = "pass"

    return {
        "run_id": run_id,
        "layer": layer,
        "title": title,
        "artifact_type": artifact_type,
        "implementation_kind": implementation_kind,
        "provisionality": provisionality,
        "scaffold_level": scaffold_level,
        "status": status,
        "input_status": input_inspection.get("input_status", ""),
        "missing_required_inputs": list(input_inspection.get("missing_required_inputs", [])),
        "stop_missing_inputs": list(input_inspection.get("stop_missing_inputs", [])),
        "continuity_checked_full": False,
        "upstream_continuity_scope": upstream_continuity_scope,
        "upstream_continuity_result": upstream_continuity_result,
        "downstream_continuity_scope": downstream_continuity_scope,
        "downstream_continuity_result": "not_checked",
        "full_upstream_and_downstream_continuity_checked": False,
        "how_built": how_built,
        "artifact_paths": {key: repo_relative_path_text(value) for key, value in artifact_paths.items()},
        "continuity_notes": continuity_notes,
    }


def build_thin_build_ledger(*, run_id: str, records: list[dict[str, Any]], final_status: str) -> dict[str, Any]:
    """Assemble the top-level ledger for the thin forward build."""

    provisionality_counts: dict[str, int] = {}
    continuity_counts: dict[str, int] = {}
    for record in records:
        provisionality_counts[record["provisionality"]] = provisionality_counts.get(record["provisionality"], 0) + 1
        continuity_counts[record["upstream_continuity_result"]] = continuity_counts.get(record["upstream_continuity_result"], 0) + 1

    return {
        "run_id": run_id,
        "build_kind": "v5_thin_forward_path",
        "final_status": final_status,
        "implementation_standard": {
            "implementation_kind": sorted(IMPLEMENTATION_KINDS),
            "continuity_levels": sorted(CONTINUITY_LEVELS),
            "continuity_results": sorted(CONTINUITY_RESULTS),
        },
        "layer_records": records,
        "counts": {
            "layer_count": len(records),
            "provisionality_counts": provisionality_counts,
            "upstream_continuity_counts": continuity_counts,
        },
        "build_rules": [
            "Never label a scaffold as finished if downstream continuity has not been checked.",
            "Never report full continuity unless both upstream and downstream continuity were checked.",
            "Never promote blocked inputs to ready status.",
            "Never let a thin layer claim runtime safety.",
        ],
        "created_at": None,
    }


__all__ = [
    "CONTINUITY_LEVELS",
    "CONTINUITY_RESULTS",
    "IMPLEMENTATION_KINDS",
    "build_layer_build_record",
    "build_review_gate_record",
    "build_thin_build_ledger",
]
