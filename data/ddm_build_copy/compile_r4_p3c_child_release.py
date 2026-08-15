#!/usr/bin/env python3
"""Compile the verified R4 graph into a deterministic P3C promotion plan.

This module deliberately keeps compilation separate from database mutation.  The
plan is the complete, auditable input to the transactional promoter; no IDs are
allocated and no authority rows are written during compilation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def compile_plan(graph_path: Path, output_path: Path, overlay_path: Path | None = None) -> dict[str, Any]:
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    components = graph.get("components", {})
    if graph.get("database_mutated"):
        raise ValueError("input graph claims database mutation")
    if len(components) != 162 or graph.get("source_component_count") != 162:
        raise ValueError("R4 coverage is not exactly 162 components")
    if graph.get("unresolved_components"):
        raise ValueError("R4 graph contains unresolved components")

    existing_alias_ids: set[str] = set()
    if overlay_path:
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
        for cid, decision in overlay.get("component_decisions", {}).items():
            if decision.get("decision") != "ACCEPT_NEW_FAMILY" and decision.get("canonical_proposition", {}).get("canonical_family_id"):
                existing_alias_ids.add(cid)
    rows = []
    for component_id in sorted(components):
        node = components[component_id]
        if node.get("component_id") != component_id:
            raise ValueError(f"component id mismatch: {component_id}")
        identity = node.get("canonical_identity") or {}
        proposition = node.get("canonical_proposition") or {}
        signature_hash = node.get("semantic_signature_sha256")
        if len(signature_hash or "") != 64:
            raise ValueError(f"missing canonical signature hash: {component_id}")
        members = node.get("member_decisions") or []
        if not members:
            members = [{"lineage_id": lineage_id} for lineage_id in proposition.get("member_lineages", [])]
        if not members:
            raise ValueError(f"missing member decisions: {component_id}")
        lineages = sorted({m.get("lineage_id") for m in members if m.get("lineage_id")})
        if len(lineages) != len(members):
            raise ValueError(f"duplicate or missing lineage in component: {component_id}")
        existing_family_id = node.get("existing_family_id") or ""
        if not existing_family_id and component_id in existing_alias_ids:
            existing_family_id = proposition.get("canonical_family_id") or ""
        genealogy = node.get("genealogy") or proposition.get("genealogy") or {}
        rows.append({
            "component_id": component_id,
            "action": node.get("decision") or node.get("candidate_action"),
            "existing_family_id": existing_family_id,
            "canonical_identity": identity,
            "canonical_proposition": proposition,
            "semantic_signature_sha256": signature_hash,
            "member_lineage_ids": lineages,
            "supporting_pair_ids": sorted(set(node.get("supporting_pair_ids") or [])),
            "evidence_role_ids": sorted(set(node.get("evidence_role_ids") or node.get("evidence_role_links") or proposition.get("evidence_role_links", []) or [])),
            "genealogy": genealogy,
        })

    plan = {
        "plan_version": "R4_P3C_CHILD_RELEASE_PLAN_V1",
        "authority_parent_release": "P3-AUTHORITY-2026-08-02-R184",
        "database_mutated": False,
        "component_count": len(rows),
        "existing_family_alias_count": sum(bool(r["existing_family_id"]) for r in rows),
        "new_family_component_count": sum(not r["existing_family_id"] for r in rows),
        "components": rows,
    }
    plan["plan_sha256"] = sha256_text(stable_json(plan))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return plan


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--overlay", type=Path)
    args = parser.parse_args()
    plan = compile_plan(args.graph, args.output, args.overlay)
    print(json.dumps({k: plan[k] for k in ("plan_version", "component_count", "existing_family_alias_count", "new_family_component_count", "plan_sha256")}, indent=2))


if __name__ == "__main__":
    main()
