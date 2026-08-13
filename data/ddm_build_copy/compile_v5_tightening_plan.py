#!/usr/bin/env python3
"""Compile a companion tightening plan for V552 through V558.

This report is intentionally concrete: it says what would make each layer less
thin while preserving the current scaffold boundaries.
"""

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


def _layer_plan(layer: str, packet: dict[str, Any], readiness: dict[str, Any]) -> dict[str, Any]:
    if layer == "v552j":
        return {
            "next_tightening_step": "preserve the certified spine and reviewable sidecar, then add richer blocker reasons without collapsing them into runtime claims",
            "what_to_add_next": [
                "clearer blocked/reviewable separation in the handoff packet",
                "explicit provenance links to the upstream certified and reviewable artifacts",
                "a stronger validation surface for forbidden claim IDs and completeness",
            ],
            "still_forbidden": [
                "runtime-safe persona content",
                "dialogue",
                "voice",
                "household story",
                "psychological inference",
            ],
        }
    if layer == "v553":
        return {
            "next_tightening_step": "make temporal pressure richer by using multiple waves and explicit cross-wave harmonization authority",
            "what_to_add_next": [
                "multiple-wave temporal overlays",
                "explicit wave-to-wave harmonization evidence",
                "clean separation between temporal pressure and downstream persona inference",
            ],
            "still_forbidden": [
                "life event narration",
                "person memory",
                "parent orientation",
                "pressure-flow routing",
            ],
        }
    if layer == "v554":
        return {
            "next_tightening_step": "enrich the seed contract with demographic and regional slice logic while keeping it a bounded seed, not a person",
            "what_to_add_next": [
                "explicit demographic slice inputs",
                "regional / national / subnational structural priors",
                "more detailed absence registers for what the seed may not generate",
            ],
            "still_forbidden": [
                "full persona",
                "autobiography",
                "voice",
                "belief-as-fact",
            ],
        }
    if layer == "v555":
        return {
            "next_tightening_step": "turn mediation slots into better-defined life-course mediation categories for parent, co-parent, and household channels",
            "what_to_add_next": [
                "explicit mediation channel labels",
                "parent/co-parent/child transmission distinctions",
                "more precise stop reasons for unresolved household mediation",
            ],
            "still_forbidden": [
                "completed biography",
                "carrier membership as fact",
                "household event story",
                "named parent psychology",
            ],
        }
    if layer == "v556":
        return {
            "next_tightening_step": "make pressure-flow attractor scaffolding more explicit about what evidence is needed before any psyche-like runtime work is allowed",
            "what_to_add_next": [
                "pressure-flow routing prerequisites",
                "attractor formation guardrails",
                "clear relation between mediation history and future dynamics",
            ],
            "still_forbidden": [
                "enneagram assignment",
                "finished psyche profile",
                "static trait assignment",
                "chat personality",
            ],
        }
    if layer == "v557":
        return {
            "next_tightening_step": "keep the renderer contract thin, but specify how downstream runtime wiring will consume the pressure-flow contract later",
            "what_to_add_next": [
                "renderer consumption contract for later app wiring",
                "explicit audit notes for safe future runtime adapters",
                "more precise input/output contract notes for UI integration",
            ],
            "still_forbidden": [
                "dialogue",
                "voice",
                "unaudited persona",
                "app-facing persona generation",
            ],
        }
    if layer == "v558":
        return {
            "next_tightening_step": "keep the runtime boundary explicit and non-persona while spelling out the checks that future runtime grafts must satisfy",
            "what_to_add_next": [
                "authority-document lineage checks",
                "runtime gate normalization and blocking rules",
                "future graft-readiness audit notes",
            ],
            "still_forbidden": [
                "runtime persona execution",
                "dialogue generation",
                "voice generation",
                "persona materialization",
            ],
        }
    return {"next_tightening_step": "", "what_to_add_next": [], "still_forbidden": []}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# V552 Through V558 Tightening Plan",
        "",
        f"- Repo root: `{report['repo_root']}`",
        f"- Created at: `{report['created_at']}`",
        f"- Latest thin root: `{report['latest_thin_root']}`",
        "",
        "## Per-Layer Tightening",
        "",
    ]
    for row in report["tightening_rows"]:
        lines.extend(
            [
                f"### {row['layer']}",
                f"- From: `{row['handoff_from']}`",
                f"- Consumes: `{row['consumes_artifact']}`",
                f"- Current status: `{row['layer_status']}`",
                f"- Next tightening step: {row['next_tightening_step']}",
                "- What to add next:",
            ]
        )
        for item in row["what_to_add_next"]:
            lines.append(f"  - {item}")
        lines.append("- Still forbidden:")
        for item in row["still_forbidden"]:
            lines.append(f"  - {item}")
        lines.append("")
    lines.extend(
        [
            "## Notes",
            "",
            "- This plan does not change the current scaffold boundaries.",
            "- It only states what would make each layer less thin while keeping the same downstream safety line.",
            "- The current `v552j` through `v558` thin chain is already buildable from repo state.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the V552 through V558 tightening plan.")
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "architecture_control" / "reports"))
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    output_dir = Path(args.output_dir)

    latest_thin_root = latest_dir(repo_root / "data" / "ddm_repository_copy" / "v5_thin_end_to_end" / "runs", "*")
    thin_layer_roots = _thin_layer_roots(latest_thin_root)
    tightening_rows: list[dict[str, Any]] = []
    chain = {item["to"]: item for item in DEPENDENCY_CHAIN}
    for layer in ("v552j", "v553", "v554", "v555", "v556", "v557", "v558"):
        layer_root = thin_layer_roots.get(layer)
        packet_name = _layer_packet_name(layer)
        packet = _read_json(layer_root / "packets" / packet_name) if layer_root and packet_name else {}
        readiness = _read_json(layer_root / "manifest" / f"{layer}_readiness_report.json") if layer_root else {}
        layer_plan = _layer_plan(layer, packet, readiness)
        tightening_rows.append(
            {
                "layer": layer,
                "handoff_from": chain.get(layer, {}).get("from", ""),
                "handoff_note": chain.get(layer, {}).get("handoff", ""),
                "layer_root": str(layer_root) if layer_root else "",
                "layer_status": readiness.get("status", ""),
                "runtime_ready": bool(readiness.get("ready_for_runtime_consumption", False)),
                "consumes_layer": packet.get("payload", {}).get("consumes_layer", ""),
                "consumes_artifact": packet.get("payload", {}).get("consumes_artifact", ""),
                "next_tightening_step": layer_plan["next_tightening_step"],
                "what_to_add_next": layer_plan["what_to_add_next"],
                "still_forbidden": layer_plan["still_forbidden"],
                "upstream_requirements": packet.get("upstream_requirements", {}),
                "downstream_expectations": packet.get("downstream_expectations", []),
            }
        )

    report = {
        "repo_root": str(repo_root),
        "created_at": _read_json((latest_thin_root / "manifest" / "v5_thin_end_to_end_readiness_report.json")).get("created_at", "") if latest_thin_root else "",
        "latest_thin_root": str(latest_thin_root) if latest_thin_root else "",
        "latest_thin_layer_roots": {layer: str(path) for layer, path in thin_layer_roots.items()},
        "tightening_rows": tightening_rows,
    }

    _write_json(output_dir / "V552_THROUGH_V558_TIGHTENING_PLAN.json", report)
    _write_markdown(output_dir / "V552_THROUGH_V558_TIGHTENING_PLAN.md", report)
    print(output_dir / "V552_THROUGH_V558_TIGHTENING_PLAN.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
