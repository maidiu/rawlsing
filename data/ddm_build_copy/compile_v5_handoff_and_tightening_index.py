#!/usr/bin/env python3
"""Compile a combined V552 through V558 handoff and tightening index."""

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
    return {
        "v552j": "v552j_structural_handoff_packet.json",
        "v553": "v553_temporal_pressure_field_packet.json",
        "v554": "v554_persona_seed_contract_packet.json",
        "v555": "v555_life_course_mediation_packet.json",
        "v556": "v556_pressureflow_attractor_packet.json",
        "v557": "v557_renderer_contract_packet.json",
        "v558": "v558_runtime_boundary_packet.json",
    }.get(layer, "")


def _layer_plan(layer: str) -> dict[str, Any]:
    if layer == "v552j":
        return {
            "purpose": "preserve certified spine and reviewable sidecar while keeping runtime claims out",
            "next_tightening_step": "add richer blocker reasons and provenance without collapsing into runtime claims",
            "top_upgrades": [
                "clearer blocked/reviewable separation",
                "explicit provenance links",
                "stronger forbidden claim ID validation",
            ],
        }
    if layer == "v553":
        return {
            "purpose": "convert structural handoff into temporal pressure scaffolding",
            "next_tightening_step": "bring in multiple-wave harmonization authority and richer cross-wave temporal overlays",
            "top_upgrades": [
                "multi-wave overlays",
                "explicit harmonization evidence",
                "clean separation from persona inference",
            ],
        }
    if layer == "v554":
        return {
            "purpose": "turn temporal pressure into a bounded persona seed contract",
            "next_tightening_step": "add demographic and regional slice logic while keeping the seed non-personal",
            "top_upgrades": [
                "demographic slice inputs",
                "regional / national / subnational priors",
                "stronger absence registers",
            ],
        }
    if layer == "v555":
        return {
            "purpose": "convert seed contract into mediation channels for life-course handling",
            "next_tightening_step": "separate parent/co-parent/child mediation channels more explicitly",
            "top_upgrades": [
                "mediation channel labels",
                "transmission distinctions",
                "more precise household stop reasons",
            ],
        }
    if layer == "v556":
        return {
            "purpose": "prepare pressure-flow attractor scaffolding without assigning psyche",
            "next_tightening_step": "spell out what evidence is required before psyche-like runtime work can occur",
            "top_upgrades": [
                "pressure-flow routing prerequisites",
                "attractor guardrails",
                "mediation-to-dynamics relations",
            ],
        }
    if layer == "v557":
        return {
            "purpose": "define the renderer contract without rendering dialogue or persona",
            "next_tightening_step": "explain how downstream runtime wiring will consume the pressure-flow contract later",
            "top_upgrades": [
                "renderer consumption contract",
                "future app-wiring audit notes",
                "UI integration notes",
            ],
        }
    if layer == "v558":
        return {
            "purpose": "define the runtime input gate and graft-readiness boundary without granting runtime persona execution",
            "next_tightening_step": "separate the runtime boundary from any eventual persona execution substrate and keep authority checks explicit",
            "top_upgrades": [
                "runtime input gate normalization",
                "graft-readiness validation",
                "authority-document lineage and boundary checks",
            ],
        }
    return {"purpose": "", "next_tightening_step": "", "top_upgrades": []}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# V552 Through V558 Handoff and Tightening Index",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Latest thin root: `{report['latest_thin_root']}`",
        "",
        "## How to read this",
        "",
        "- The handoff map tells you what each layer consumes and emits.",
        "- The tightening plan tells you what to add next without breaking the scaffold boundary.",
        "- This index is an implementation guide, not runtime output.",
        "",
        "## Layer Index",
        "",
        "| Layer | From | Consumes | Artifact | Status | Buildable | Runtime Ready | Next Tightening Step |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            "| {layer} | {from_layer} | {consumes} | `{artifact}` | {status} | {buildable} | {runtime_ready} | {next_step} |".format(
                layer=row["layer"],
                from_layer=row["handoff_from"] or "root",
                consumes=row["consumes_artifact"] or row["consumes_layer"] or "n/a",
                artifact=row["artifact"] or "n/a",
                status=row["layer_status"] or "n/a",
                buildable="yes" if row["buildable_from_repo_state"] else "no",
                runtime_ready="yes" if row["runtime_ready"] else "no",
                next_step=row["next_tightening_step"],
            )
        )
    lines.extend(
        [
            "",
            "## Implementation Note",
            "",
            "- Yes: this plan is for the assistant to implement against.",
            "- No: it does not itself change runtime behavior or widen the scaffold boundary.",
            "- The thin chain remains buildable from repo state and intentionally non-runtime.",
            "- `v558` is the last boundary adapter in this chain and remains a gate, not a runtime persona engine.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the V552 through V558 handoff and tightening index.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    output_dir = Path(args.output_dir)

    latest_thin_root = latest_dir(repo_root / "data" / "ddm_repository_copy" / "v5_thin_end_to_end" / "runs", "*")
    thin_layer_roots = _thin_layer_roots(latest_thin_root)
    chain = {item["to"]: item for item in DEPENDENCY_CHAIN}
    rows: list[dict[str, Any]] = []
    for layer in ("v552j", "v553", "v554", "v555", "v556", "v557", "v558"):
        layer_root = thin_layer_roots.get(layer)
        packet_name = _layer_packet_name(layer)
        packet = _read_json(layer_root / "packets" / packet_name) if layer_root and packet_name else {}
        readiness = _read_json(layer_root / "manifest" / f"{layer}_readiness_report.json") if layer_root else {}
        plan = _layer_plan(layer)
        rows.append(
            {
                "layer": layer,
                "handoff_from": chain.get(layer, {}).get("from", ""),
                "handoff_note": chain.get(layer, {}).get("handoff", ""),
                "layer_root": str(layer_root) if layer_root else "",
                "layer_status": readiness.get("status", ""),
                "runtime_ready": bool(readiness.get("ready_for_runtime_consumption", False)),
                "buildable_from_repo_state": bool(layer_root),
                "consumes_layer": packet.get("payload", {}).get("consumes_layer", ""),
                "consumes_artifact": packet.get("payload", {}).get("consumes_artifact", ""),
                "artifact": f"packets/{packet_name}" if packet_name else "",
                "next_tightening_step": plan["next_tightening_step"],
                "purpose": plan["purpose"],
                "top_upgrades": plan["top_upgrades"],
                "required_upstream_artifacts": LAYER_REQUIREMENTS.get(layer, {}).get("required_upstream_artifacts", []),
                "required_upstream_authority": LAYER_REQUIREMENTS.get(layer, {}).get("required_upstream_authority", []),
                "downstream_outputs_expected": LAYER_REQUIREMENTS.get(layer, {}).get("downstream_outputs_expected", []),
            }
        )

    report = {
        "repo_root": str(repo_root),
        "created_at": _read_json((latest_thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json")).get("created_at", "") if latest_thin_root else "",
        "latest_thin_root": str(latest_thin_root) if latest_thin_root else "",
        "latest_thin_layer_roots": {layer: str(path) for layer, path in thin_layer_roots.items()},
        "rows": rows,
    }

    _write_json(output_dir / "V552_THROUGH_V558_HANDOFF_AND_TIGHTENING_INDEX.json", report)
    _write_markdown(output_dir / "V552_THROUGH_V558_HANDOFF_AND_TIGHTENING_INDEX.md", report)
    print(output_dir / "V552_THROUGH_V558_HANDOFF_AND_TIGHTENING_INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
