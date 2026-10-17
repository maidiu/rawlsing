#!/usr/bin/env python3
"""Compile an explicit V552 through V558 handoff map from the latest thin run."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_thin_end_to_end import DEPENDENCY_CHAIN, LAYER_REQUIREMENTS  # noqa: E402
from data.ddm_build_copy.ddm_latest_run import latest_dir  # noqa: E402


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def _thin_layer_roots(thin_root: Path | None) -> dict[str, Path]:
    if thin_root is None:
        return {}
    readiness = _read_json(thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json")
    roots: dict[str, Path] = {}
    for row in readiness.get("layer_reports", []) if isinstance(readiness.get("layer_reports", []), list) else []:
        if not isinstance(row, dict):
            continue
        layer = str(row.get("layer", "")).strip()
        layer_root = str(row.get("layer_output_root", "")).strip()
        if layer and layer_root:
            roots[layer] = Path(layer_root)
    return roots


def _layer_packet_name(layer: str) -> str:
    if layer == "v552j":
        return "v552j_structural_handoff_packet.json"
    if layer == "v553":
        return "v553_temporal_pressure_field_packet.json"
    if layer == "v554":
        return "v554_persona_seed_contract_packet.json"
    if layer == "v555":
        return "v555_life_course_mediation_packet.json"
    if layer == "v556":
        return "v556_pressureflow_attractor_packet.json"
    if layer == "v557":
        return "v557_renderer_contract_packet.json"
    if layer == "v558":
        return "v558_runtime_boundary_packet.json"
    return ""


def _layer_schema_name(layer: str) -> str:
    packet = _layer_packet_name(layer)
    return packet.replace(".json", ".schema.json") if packet else ""


def _build_handoff_rows(
    *,
    repo_root: Path,
    thin_root: Path | None,
    thin_layer_roots: dict[str, Path],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    chain = {item["to"]: item for item in DEPENDENCY_CHAIN}
    for layer in ("v552j", "v553", "v554", "v555", "v556", "v557", "v558"):
        requirements = LAYER_REQUIREMENTS.get(layer, {})
        layer_root = thin_layer_roots.get(layer)
        readiness = _read_json(layer_root / "manifest" / f"{layer}_readiness_report.json") if layer_root else {}
        packet_name = _layer_packet_name(layer)
        packet = _read_json(layer_root / "packets" / packet_name) if layer_root and packet_name else {}
        packet_name = _layer_packet_name(layer)
        schema_name = _layer_schema_name(layer)
        upstream = chain.get(layer, {})
        rows.append(
            {
                "layer": layer,
                "handoff_from": upstream.get("from", ""),
                "handoff_note": upstream.get("handoff", ""),
                "layer_root": str(layer_root) if layer_root else "",
                "layer_status": readiness.get("status", ""),
                "runtime_ready": bool(readiness.get("ready_for_runtime_consumption", False)),
                "implementation_kind": readiness.get("implementation_kind", ""),
                "provisionality": readiness.get("provisionality", ""),
                "scaffold_level": readiness.get("scaffold_level", ""),
                "consumes_layer": packet.get("payload", {}).get("consumes_layer", ""),
                "consumes_artifact": packet.get("payload", {}).get("consumes_artifact", ""),
                "artifact": f"packets/{packet_name}" if packet_name else "",
                "schema": f"schemas/{schema_name}" if schema_name else "",
                "readiness_report": f"manifest/{layer}_readiness_report.json",
                "input_manifest": f"manifest/{layer}_input_manifest.json",
                "required_upstream_artifacts": requirements.get("required_upstream_artifacts", []),
                "required_upstream_authority": requirements.get("required_upstream_authority", []),
                "downstream_outputs_expected": requirements.get("downstream_outputs_expected", []),
                "upstream_layer_context": readiness.get("upstream_layer_context", {}),
                "v553_temporal_context": readiness.get("v553_temporal_context", {}),
                "buildable_from_repo_state": True if layer_root else False,
            }
        )
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# V552 Through V558 Handoff Map",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Latest thin root: `{report['latest_thin_root']}`",
        "",
        "## Layer Chain",
        "",
        "| Layer | From | Consumes | Artifact | Status | Runtime Ready | Buildable |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in report["handoff_rows"]:
        lines.append(
            "| {layer} | {from_layer} | {consumes} | `{artifact}` | {status} | {runtime_ready} | {buildable} |".format(
                layer=row["layer"],
                from_layer=row["handoff_from"] or "root",
                consumes=row["consumes_artifact"] or row["consumes_layer"] or "n/a",
                artifact=row["artifact"] or "n/a",
                status=row["layer_status"] or "n/a",
                runtime_ready="yes" if row["runtime_ready"] else "no",
                buildable="yes" if row["buildable_from_repo_state"] else "no",
            )
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- These are scaffold handoffs, not runtime persona outputs.",
            "- Each layer preserves the consumed upstream contract packet and readiness report in its own layer root.",
            "- `v553` carries the temporal context bundle needed by later layers.",
            "- `v558` is the runtime boundary gate and graft-readiness adapter; it does not generate persona runtime itself.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the V552 through V558 handoff map.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    output_dir = Path(args.output_dir)

    latest_thin_root = latest_dir(repo_root / "data" / "ddm_repository_copy" / "v5_thin_end_to_end" / "runs", "*")
    thin_layer_roots = _thin_layer_roots(latest_thin_root)
    handoff_rows = _build_handoff_rows(repo_root=repo_root, thin_root=latest_thin_root, thin_layer_roots=thin_layer_roots)
    report = {
        "repo_root": str(repo_root),
        "created_at": _read_json((latest_thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json")) .get("created_at", "") if latest_thin_root else "",
        "latest_thin_root": str(latest_thin_root) if latest_thin_root else "",
        "latest_thin_layer_roots": {layer: str(path) for layer, path in thin_layer_roots.items()},
        "handoff_rows": handoff_rows,
    }

    _write_json(output_dir / "V552_THROUGH_V558_HANDOFF_MAP.json", report)
    _write_markdown(output_dir / "V552_THROUGH_V558_HANDOFF_MAP.md", report)
    print(output_dir / "V552_THROUGH_V558_HANDOFF_MAP.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
