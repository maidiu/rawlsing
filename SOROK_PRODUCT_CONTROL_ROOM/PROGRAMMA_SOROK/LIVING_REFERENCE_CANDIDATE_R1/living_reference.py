#!/usr/bin/env python3
"""Deterministic Sorok-only living reference and orchestration map.

The store is a JSON graph generated from the repaired R3 source registry and
source manifest. All operator commands read the same state file. A transition
is appended to immutable history and only candidate/sourcefree axes are
changed; no owner, native or PRE-MAIN state is mutated.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "state.json"
SNAPSHOT = ROOT / "SNAPSHOT.json"
SEED_REGISTRY = ROOT / "seed_source_registry.json"
SEED_GRAPH = ROOT / "seed_graph.json"
SEED_SLOTS = ROOT / "seed_slots.json"
SOURCE_MANIFEST = ROOT / "source_manifest.json"

BUILD_PREMAIN = "f40c26301d7d5b811c1bb92efa4934ad564ce5b3"
LAST_VERIFIED_PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
R3_CUT = "e50d32eb6816578145d17dcd637a0b90b3a1ef40"
R3_REVIEW = "3f3d9ec2fddc36bd4047bc6c730382c65a5e692a"
PROGRAM_MAP = "865b5b01e1a27e99020cf2bb389af8cd4c874b57:SOROK_PRODUCT_CONTROL_ROOM/05_PROGRAM_MAP.md"
HQ_SYNTHESIS = "36ddfd8b787543751d4b350a315af31924d95d6e:SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/HQ_WHOLE_PRODUCT_SCIENCE_AND_ORCHESTRATION_DRAFT_R1/00_WHOLE_PROGRAM_HQ_JUDGMENT.md"

SECTORS = [
    ("S0_S16", "Original product workstreams", ["S%d" % i for i in range(17)], ["S5", "S7", "S13", "S15"], "PRODUCT_OBLIGATIONS_PARTIAL"),
    ("C_A_19", "Terminal C/A person-product milestones", ["C%d" % i for i in range(13)] + ["A%d" % i for i in range(6)], ["C4", "C11", "A5"], "SOURCE_DEFINED_NATIVE_NOT_PROVEN"),
    ("M40", "Historical V3 developmental mechanisms", ["M%02d" % i for i in range(1, 41)], ["M19", "M21", "M25"], "HISTORICAL_CODE_READ_NOT_ADOPTED"),
    ("NEO_N_12", "Sorok Neo requirements", ["N%02d" % i for i in range(1, 13)], ["N10", "N11", "N12"], "THEORY_REVIEWED_NOT_ISSUED"),
    ("O16", "Original science-owner decisions", ["O%02d" % i for i in range(1, 17)], ["O11", "O12", "O13", "O16"], "OWNER_DECISIONS_UNISSUED"),
    ("E15", "Named first-consumer edges", ["E%02d" % i for i in range(1, 16)], ["E08", "E11", "E15"], "EDGE_SOURCE_ONLY"),
    ("MATERIAL_INDEPENDENT_B", "Independent B/material/refusal life", ["L0_MATERIAL", "L1_WORLD", "C4", "C6", "C8", "C9", "C10", "N07", "O08", "O09", "O16", "B-F1CR-R2", "V3CORE-R1", "E04", "E09"], ["B-F1CR-R2", "V3CORE-R1"], "SOURCEFREE_PARTIAL_NATIVE_B_MISSING"),
    ("RELATIONAL_CONSTITUTION", "Relational constitution, care, power and boundaries", ["C5", "C7", "N03", "N05", "N09", "S5", "S14", "O14"], ["S5", "S14"], "SOURCE_DEFINED_PRODUCT_GAP"),
    ("NEEDS_MOTIVE_ACTIVITY", "Needs, objects, motives and situated activity", ["C1", "C2", "C3", "C5", "M01", "M19", "M21", "M25", "N01", "N06", "E02", "E03"], ["M19", "M21"], "SOURCE_DEFINED_PARTIAL"),
    ("LEARNED_PRACTICE_NOCHANGE", "Learned practice versus missing rule/no-change", ["C3", "C9", "E02", "E14", "N05"], ["N05", "E14"], "SOURCE_DEFINED_PARTIAL"),
    ("CONTEXT_PLURALISM", "Context pluralism and role/relationship differentiation", ["C7", "N04", "N08", "M19"], ["N04", "N08"], "SOURCE_DEFINED_PARTIAL"),
    ("CHILDHOOD_DEVELOPMENT_ROLES", "Childhood, development, roles and genealogy", ["C4", "C5", "N04", "N08", "O14", "E10"], ["C4", "O14"], "SOURCE_DEFINED_NATIVE_MISSING"),
    ("USER_PRAXIS", "User action, reflection, privacy and non-diagnosis", ["S7", "S8", "S11", "S15"], ["S7", "S11", "S15"], "PRODUCT_GAP"),
    ("TRUST_INJURY_REPAIR_OPACITY", "Trust, injury, repair and truthful opacity", ["C5", "C7", "N09", "S5", "S11", "S14"], ["S5", "S11", "S14"], "PRODUCT_GAP"),
    ("CANON_HISTORY_EVENT_CLOCK_MEMORY", "Canon, history, event, clock and memory", ["C6", "C8", "C9", "C10", "C12", "M19", "M25", "N10", "N11", "N12", "E08", "E09"], ["C9", "C12", "N10", "N11", "N12"], "SOURCEFREE_PARTIAL_NATIVE_MISSING"),
    ("V2_RENDERING_UX", "V2 rendering, expression and user experience", ["S9", "S11", "R15_V2", "C10", "CP-A5-R2"], ["S9", "S11", "R15_V2", "CP-A5-R2"], "SOURCEFREE_PARTIAL_NO_HUMAN_A5"),
    ("UX_ACCESSIBILITY", "UX, opacity, attention, time and accessibility", ["S11", "S15", "CP-A5-R2", "A5"], ["S11", "S15", "A5"], "PRODUCT_GAP"),
    ("SAFETY_PRIVACY", "Safety, privacy, abuse and cross-branch boundaries", ["S14", "C12", "C9C12-R2", "E08"], ["S14", "C9C12-R2"], "SOURCEFREE_PARTIAL_SOCIAL_GAP"),
    ("PROFIT_RETENTION_ETHICS", "Profit, retention and incentive ethics", ["S13"], ["S13"], "PRODUCT_GAP"),
    ("SOCIAL_POSSIBILITIES", "Independent social possibilities", ["S12"], ["S12"], "PRODUCT_GAP"),
    ("ALPHA_EVALUATION", "Human alpha and evaluation", ["S15", "A5", "CP-A5-R2"], ["S15", "A5"], "NO_HUMAN_A5"),
    ("RECOVERY_ASSETS", "Recovered sourcefree engineering capital", ["CP-A5-R2", "C9C12-R2", "B-F1CR-R2", "V3CORE-R1", "R6", "R7"], ["CP-A5-R2", "C9C12-R2", "B-F1CR-R2", "V3CORE-R1"], "AUTHOR_TESTED_UNADOPTED"),
]

GAPS = [
    {"id": "GAP_S5_NORMATIVE_OUTPUT", "domain": "S5", "node": "L4_S5_FLOURISHING_OWNER", "status": "MISSING", "owner": "HQ / qualified product-science owner", "next": "Issue normative alternatives, uncertainty law and harmful-attachment evaluation.", "consequence": "A5 cannot distinguish flourishing from affection/compliance."},
    {"id": "GAP_S7_PRAXIS_OUTPUT", "domain": "S7", "node": "L4_S7_PRAXIS_OWNER", "status": "MISSING", "owner": "HQ / user-praxis product owner", "next": "Issue evidence threshold, feedback cadence, opt-in and privacy policy.", "consequence": "User reflection can become pseudo-diagnosis or covert scoring."},
    {"id": "GAP_S11_HUMAN_UX", "domain": "S11", "node": "L4_S11_UX_OWNER", "status": "MISSING", "owner": "Product UX owner", "next": "Issue accessible encounter flows and honest opacity behavior.", "consequence": "CP-A5 reader alone is not human-usable A5."},
    {"id": "GAP_S13_REVENUE_MODEL", "domain": "S13", "node": "L4_S13_BUSINESS_OWNER", "status": "MISSING", "owner": "Accountable business/product owner", "next": "Issue non-extractive pricing, notification and retention constraints.", "consequence": "Engagement can be mistaken for human good."},
    {"id": "GAP_S14_SOCIAL_SAFETY", "domain": "S14", "node": "L4_S14_SAFETY_OWNER", "status": "MISSING", "owner": "Safety/privacy owner", "next": "Issue abuse, consent, deletion and cross-user boundaries.", "consequence": "Storage authenticity does not provide social safety."},
    {"id": "GAP_S15_HUMAN_ALPHA", "domain": "S15", "node": "L4_S15_ALPHA_OWNER", "status": "MISSING", "owner": "Alpha/participant-research owner", "next": "Design bounded reference-person trial with ethics and actual participants.", "consequence": "Persuasive LLM presentation cannot establish a historically constituted other."},
    {"id": "GAP_NATIVE_C4_C11_PERSON", "domain": "C_A", "node": "C11", "status": "SOURCEFREE_OR_SOURCE_ONLY", "owner": "Original Pyat/C11/C12 owners", "next": "Separate native world/C11 person authority and actual C12 consumer.", "consequence": "No native continuing person exists."},
    {"id": "GAP_C9_C12_ANCHOR", "domain": "C12", "node": "C9C12-R2", "status": "CANDIDATE", "owner": "C9R/BP4/C12 owners", "next": "External anchor, mirror/outbox and durable actor readset decision.", "consequence": "C12 durability remains sourcefree-only."},
    {"id": "GAP_B_F1CR_ORIGINAL", "domain": "B", "node": "F1CR_CLAIMED_PATCH", "status": "SOURCE_NOT_FOUND", "owner": "F1C/F1CR owner", "next": "Supply original patched bytes or accept/reject reconstruction.", "consequence": "Native B source remains unavailable."},
    {"id": "GAP_NATIVE_SCIENCE_CAN_ADP", "domain": "O", "node": "N10", "status": "NOT_ISSUED", "owner": "CAN/ADP/SCI05 owners", "next": "Issue finite original rules and actor/event evidence.", "consequence": "Sourcefree developmental behavior cannot be called native."},
    {"id": "GAP_PYAT_BOUNDARY", "domain": "PYAT", "node": "PYAT_EXTERNAL_BOUNDARY", "status": "EXTERNAL_OWNER_HELD", "owner": "Pyat HQ/source owner", "next": "Supply qualified world/N11/N12/C11 grant to Sorok C0.", "consequence": "Sorok cannot infer the external world."},
    {"id": "GAP_NATIVE_A5", "domain": "A5", "node": "A5", "status": "NOT_PROVEN", "owner": "Sorok human A5/research owner", "next": "Human participant trial distinct from sourcefree encounter.", "consequence": "No human-product proof."},
]

WORK_NOW = [
    {"id": "WN_S5", "terminal": "S5 flourishing", "gap": "GAP_S5_NORMATIVE_OUTPUT", "prerequisite": "HQ normative decision; no new engine", "code": "CP-A5 sourcefree only", "science": "normative alternatives unissued", "owner": "HQ/product science", "parallel": True, "test": "harmful-attachment counterexample", "consumer": "A5 human evaluation"},
    {"id": "WN_S15", "terminal": "S15 alpha", "gap": "GAP_S15_HUMAN_ALPHA", "prerequisite": "S5/S11 evaluation design and ethics", "code": "CP-A5 reader and R15 lab", "science": "reference-person protocol unissued", "owner": "alpha/research owner", "parallel": True, "test": "persuasive-LLM falsifier", "consumer": "human participants"},
    {"id": "WN_C4_C11", "terminal": "C4/C11 native person", "gap": "GAP_NATIVE_C4_C11_PERSON", "prerequisite": "external Pyat/C11/C12 grants", "code": "historical V3/C11 candidates", "science": "native rules held", "owner": "original owners", "parallel": False, "test": "same-consumer source-fault", "consumer": "C12/A0-A5"},
    {"id": "WN_C9_C12", "terminal": "C9/C12 continuity", "gap": "GAP_C9_C12_ANCHOR", "prerequisite": "owner anchor/mirror decision", "code": "C9C12-R2", "science": "no native science", "owner": "C9R/BP4/C12", "parallel": True, "test": "anchor/clock/fork faults", "consumer": "I1/CP-A5"},
    {"id": "WN_B_F1CR", "terminal": "independent B/material", "gap": "GAP_B_F1CR_ORIGINAL", "prerequisite": "original/patch owner decision", "code": "B-F1CR-R2 reconstruction", "science": "no native B", "owner": "F1C/C10 owners", "parallel": True, "test": "targetless/refusal/material faults", "consumer": "I1 targetless"},
]

PYAT_BOUNDARY = {
    "id": "PYAT_EXTERNAL_BOUNDARY",
    "external_owner": "Pyat HQ / original source and scientific issuer",
    "required_inputs": ["source-qualified objective world/possibility", "exact source/version/as-of/uncertainty", "N11 world acceptance", "N12 wake/defer", "C11/Pyat person weld permission"],
    "sorok_receiver": ["C0", "C4", "C10", "C11", "C12"],
    "sorok_has": "sourcefree boundary model only; no native Pyat world, N11/N12 acceptance or C11 weld",
    "prohibited": ["ingesting Pyat program health", "issuing Pyat operations", "inventing N11/N12", "fused controller"],
    "status": "EXTERNAL_OWNER_HELD",
}

def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def _filter_source_manifest(manifest: dict) -> dict:
    rows = [x for x in manifest["rows"] if x.get("namespace") == "SOROK"]
    return {"schema": "SOROK_LIVING_SOURCE_MANIFEST@1", "build_premain": BUILD_PREMAIN, "last_verified_premain": LAST_VERIFIED_PREMAIN, "rows": rows, "reference_sources": manifest["reference_sources"], "manifest_digest": _digest(rows + manifest["reference_sources"])}

def _axes(row: dict | None, node: dict) -> dict:
    if row is None:
        return {"source_recovery": "INDEX_ONLY", "science": "NOT_ASSESSED", "engineering": "INDEX_ONLY", "authority": "NOT_ADOPTED", "review": "NOT_APPLICABLE", "consumer": "NOT_APPLICABLE", "human": "NOT_PROVEN", "operational": "RETURNED_UNADOPTED" if node.get("id") in {"CP-A5-R2", "C9C12-R2", "B-F1CR-R2", "V3CORE-R1"} else "INDEX_ONLY"}
    operational = "RETURNED_UNADOPTED" if row["id"] in {"CP-A5-R2", "C9C12-R2", "B-F1CR-R2", "V3CORE-R1"} else "RETURNED_SHA__INDEX_INPUT"
    return {"source_recovery": row.get("status_class", "SOURCE_PRESENT"), "science": row.get("science_grade", "NOT_ISSUED"), "engineering": row.get("engineering_grade", "SOURCE_DEFINITION_ONLY"), "authority": row.get("authority_grade", "NOT_ADOPTED"), "review": row.get("independent_review", "NOT_INDEPENDENTLY_REVIEWED"), "consumer": row.get("actual_consumer_state", "NONE_PROVEN_AT_PREMAIN"), "human": row.get("human_grade", "NOT_PROVEN"), "operational": operational}

def build_state() -> dict:
    registry = _load(SEED_REGISTRY)
    graph = _load(SEED_GRAPH)
    slots = _load(SEED_SLOTS)
    manifest = _filter_source_manifest(_load(SOURCE_MANIFEST))
    rows = {x["id"]: x for x in registry["rows"]}
    source_rows = {x["id"]: x for x in manifest["rows"]}
    nodes = [copy.deepcopy(n) for n in graph["nodes"] if not str(n["id"]).startswith("PYAT_") and n["id"] != "L1_PYAT_SEPARATE"]
    node_ids = {n["id"] for n in nodes}
    boundary = dict(PYAT_BOUNDARY, layer="L1", kind="EXTERNAL_BOUNDARY", title="Qualified Pyat world/N11/N12/C11 boundary")
    if boundary["id"] not in node_ids:
        nodes.append(boundary)
    for rid, title in (("R6", "R6 finite 39/R41 source closure"), ("R7", "R7 cross-lineage source closure")):
        if rid not in node_ids:
            nodes.append({"id": rid, "layer": "L5", "kind": "SOURCE_RECOVERY", "title": title, "status": "RETURNED_SHA__UNADOPTED", "source_refs": ["28e38ebbf08bbfaeb152ae022046e1303d9a2e40" if rid == "R6" else "7f25fb9bfc48679a47ccc61b36354f20fef54f1c"], "hq_judgment_required": True})
            node_ids.add(rid)
    edges = [copy.deepcopy(e) for e in graph["edges"] if e["from"] in node_ids or e["from"] == boundary["id"]]
    edges = [e for e in edges if e["from"] in node_ids and e["to"] in node_ids]
    if not any(e["from"] == boundary["id"] and e["to"] == "C0" for e in edges):
        edges.append({"from": boundary["id"], "to": "C0", "relation": "external_source_potential_to_sorok_c0", "status": "EXTERNAL_OWNER_HELD", "hq_judgment_required": True})
    for rid in ("R6", "R7"):
        if "L1_RECOVERY" in node_ids and not any(e["from"] == "L1_RECOVERY" and e["to"] == rid for e in edges):
            edges.append({"from": "L1_RECOVERY", "to": rid, "relation": "recovery_evidence_contained", "status": "RETURNED_SHA__UNADOPTED", "hq_judgment_required": True})
    # remove optional placeholder literals from sector definitions
    sectors = []
    for name, title, required, challenged, status in SECTORS:
        req = [x for x in required if x in node_ids]
        missing = [x for x in required if x not in node_ids]
        sectors.append({"id": name, "title": title, "required_nodes": req, "missing_nodes": missing, "challenged": challenged, "status": status, "coverage": "PARTIAL" if missing or challenged else "PRESENT"})
    axes = {n["id"]: _axes(rows.get(n["id"]), n) for n in nodes}
    state = {
        "schema": "SOROK_PROGRAMMA_LIVING_REFERENCE_STATE@1",
        "version": "R1",
        "build_cut": BUILD_PREMAIN,
        "last_verified_premain": LAST_VERIFIED_PREMAIN,
        "version_vector": {
            "sorok_startup": BUILD_PREMAIN,
            "sorok_current_refreshed": LAST_VERIFIED_PREMAIN,
            "premain_delta_from_startup": {"count": 11, "files": [".github/workflows/pyat-s7fix-independent-custody.yml", "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/00_PROGRAMMA_RAWLSING.md", "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/01_SHARED_LIVING_REFERENCE_CORRESPONDENCE_R1.md", "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/02_CURRENT_RETURN_DELTA_SOROK_OINDEX_R3_20261031.md", "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/18_s7fix_independent_group_check.py", "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/20261031_HQ_S7FIX_PEV2K_HOSTILE_INTAKE.md", "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/00_PROGRAMMA_PYAT.md", "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/01_LIVING_REFERENCE_AND_ORCHESTRATION_CONTRACT_R1.md", "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_PROGRAMMA_SOROK.md", "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/01_LIVING_REFERENCE_AND_ORCHESTRATION_CONTRACT_R1.md", "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/02_SCOPE_CORRECTION_SOROK_ONLY_EXECUTION_R1.md"]},
            "r3_index": R3_CUT,
            "r3_review": R3_REVIEW,
            "program_map": "865b5b01e1a27e99020cf2bb389af8cd4c874b57:2a0a3a42d66f566f92d5c333fbbea4a5adb383b2",
            "hq_synthesis": "36ddfd8b787543751d4b350a315af31924d95d6e:1ba39a965d30e63c5b6183e4af1aa84d95b4021b",
            "r6": "28e38ebbf08bbfaeb152ae022046e1303d9a2e40",
            "r7": "7f25fb9bfc48679a47ccc61b36354f20fef54f1c",
            "four_assets": {"CP-A5-R2": "913765328e4fab12b150ea01421ed6b445158184", "C9C12-R2": "c78404724052496fdec8608c8b0e833c0f7c4ecc", "B-F1CR-R2": "bf3273c294c704ad7c631559b9866d351bb4f103", "V3CORE-R1": "b5cb3f917402b992d7cbe933af0b378d2b37cbfd"}
        },
        "nodes": nodes,
        "edges": edges,
        "source_manifest": manifest,
        "source_count": len(manifest["rows"]),
        "pyat_boundary": boundary,
        "sectors": sectors,
        "gaps": GAPS,
        "work_now": WORK_NOW,
        "workers": [
            {"id": "R3_INDEX", "branch": "agent/sorok-oindex-r3-exact-source-integrity-repair-20261031-r1", "sha": R3_CUT, "status": "RETURNED_UNADOPTED", "editor_model": "OpenCode/DeepSeek V4.1-Flash MAX", "reviewer": "separate R3-IR required", "cost": "UNKNOWN"},
            {"id": "R3_IR_REVIEW", "branch": "review/sorok-oindex-r3-independent-source-and-map-acceptance-20261031", "sha": R3_REVIEW, "status": "SEALED_NOT_ASSUMED_RUNNING", "editor_model": "UNKNOWN", "reviewer": "independent", "cost": "UNKNOWN"},
            {"id": "CP-A5-R2", "branch": "agent/sorok-cp-a5-r2-multicontext-encounter-20261030", "sha": "913765328e4fab12b150ea01421ed6b445158184", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "OpenCode/DeepSeek V4.1-Flash MAX", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
            {"id": "C9C12-R2", "branch": "agent/sorok-c9c12-r2-versioned-writer-reader-clock-20261030", "sha": "c78404724052496fdec8608c8b0e833c0f7c4ecc", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
            {"id": "B-F1CR-R2", "branch": "agent/sorok-b-f1cr-targetless-c10-20261030", "sha": "bf3273c294c704ad7c631559b9866d351bb4f103", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
            {"id": "V3CORE-R1", "branch": "agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030", "sha": "b5cb3f917402b992d7cbe933af0b378d2b37cbfd", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        ],
        "flights": [{"id": "SOROK_SOURCEFREE_REFERENCE", "status": "CANDIDATE_ONLY", "owner": "Sorok HQ/original owners", "note": "No new worker launched by this reference."}],
        "axes": axes,
        "history": [{"history_id": "H0001", "kind": "GENESIS", "state": "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED", "source_vector": {"r3": R3_CUT, "build_premain": BUILD_PREMAIN}}],
        "freshness": {"generated_at": "2026-10-31T00:00:00Z", "refresh_command": "python3 living_reference.py refresh"},
    }
    state["state_digest"] = _digest({k: v for k, v in state.items() if k not in {"history", "state_digest"}})
    return state

def _save(state: dict) -> None:
    state["state_digest"] = _digest({k: v for k, v in state.items() if k not in {"history", "state_digest"}})
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    SNAPSHOT.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def _load_state() -> dict:
    if not STATE.exists():
        _save(build_state())
    return _load(STATE)

def _neighbors(state: dict, node_id: str, depth: int) -> tuple[list[dict], list[dict]]:
    nodes = {n["id"]: n for n in state["nodes"]}
    seen = {node_id}
    result_nodes = [nodes[node_id]] if node_id in nodes else []
    result_edges = []
    frontier = {node_id}
    for _ in range(depth):
        nxt = set()
        for edge in state["edges"]:
            if edge["from"] in frontier and edge["to"] not in seen:
                seen.add(edge["to"]); nxt.add(edge["to"])
            if edge["to"] in frontier and edge["from"] not in seen:
                seen.add(edge["from"]); nxt.add(edge["from"])
            if edge["from"] in frontier or edge["to"] in frontier:
                if edge not in result_edges: result_edges.append(edge)
        result_nodes.extend(nodes[x] for x in sorted(nxt) if x in nodes)
        frontier = nxt
    return result_nodes, result_edges

def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))

def _overview(state: dict) -> dict:
    return {"schema": state["schema"], "version": state["version"], "build_cut": state["build_cut"], "current_premain": state["last_verified_premain"], "version_vector": state["version_vector"], "counts": {"nodes": len(state["nodes"]), "edges": len(state["edges"]), "sources": state["source_count"], "sectors": len(state["sectors"]), "gaps": len(state["gaps"]), "slots": len(_load(SEED_SLOTS)["slots"]), "workers": len(state["workers"])}, "status": "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED", "pyat_boundary": state["pyat_boundary"]}

def _critical_path(state: dict, goal: str) -> list[str] | None:
    nodes = {n["id"]: n for n in state["nodes"]}
    if goal not in nodes: return None
    graph: dict[str, list[str]] = {}
    for e in state["edges"]: graph.setdefault(e["from"], []).append(e["to"])
    q = deque([(goal, [goal])]); seen = {goal}
    while q:
        node, path = q.popleft()
        if nodes.get(node, {}).get("layer") == "L5": return path
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt); q.append((nxt, path + [nxt]))
    return None

def intake_candidate(state: dict, fixture: dict) -> dict:
    item = {"history_id": "H%04d" % (len(state["history"]) + 1), "kind": "INTAKE_RETURN_CANDIDATE", "return_id": fixture.get("id", "UNKNOWN"), "source": fixture.get("branch", ""), "sha": fixture.get("sha", ""), "status": "CANDIDATE_NOT_PROMOTED", "claimed_tests": fixture.get("tests", {}), "evidence": fixture.get("evidence", {})}
    state["history"].append(item)
    if fixture.get("new_requirement"):
        rid = fixture["new_requirement"]
        state["gaps"].append({"id": "GAP_" + rid, "domain": "DISCOVERED_REQUISITE", "node": rid, "status": "UNREPRESENTED_REQUIREMENT", "owner": "UNKNOWN", "next": "Assign source/owner/consumer.", "consequence": "Visible unrepresented requirement."})
        item["new_gap"] = "GAP_" + rid
    return item

def _apply_transition(state: dict, fixture: dict) -> dict:
    node_id = fixture.get("node_id")
    if not node_id or node_id not in {n["id"] for n in state["nodes"]}: raise ValueError("UNKNOWN_NODE")
    if fixture.get("owner_evidence") in (None, "") or fixture.get("reviewer_evidence") in (None, ""): raise ValueError("AUTHORIZED_TRANSITION_EVIDENCE_MISSING")
    dimension = fixture.get("dimension")
    if dimension not in {"source_recovery", "science", "engineering", "authority", "review", "consumer", "human", "operational"}: raise ValueError("UNKNOWN_DIMENSION")
    old = state["axes"][node_id][dimension]
    new = fixture.get("to")
    if not isinstance(new, str) or not new: raise ValueError("INVALID_TARGET_STATE")
    if dimension == "human" and new == "PROVEN" and "HUMAN_PARTICIPANT" not in fixture["owner_evidence"]:
        raise ValueError("HUMAN_PARTICIPANT_EVIDENCE_REQUIRED")
    if dimension == "authority" and new.startswith("NATIVE") and "OWNER_GRANT" not in fixture["owner_evidence"]:
        raise ValueError("OWNER_GRANT_EVIDENCE_REQUIRED")
    state["axes"][node_id][dimension] = new
    h = {"history_id": "H%04d" % (len(state["history"]) + 1), "kind": "AUTHORIZED_TRANSITION", "node_id": node_id, "dimension": dimension, "from": old, "to": new, "owner_evidence": fixture["owner_evidence"], "reviewer_evidence": fixture["reviewer_evidence"]}
    state["history"].append(h)
    # Downstream invalidation is candidate-only; Pyat boundary is never traversed.
    graph = {e["from"]: [] for e in state["edges"]}
    for e in state["edges"]: graph.setdefault(e["from"], []).append(e["to"])
    q = deque(graph.get(node_id, [])); invalidated = []
    while q:
        n = q.popleft()
        if n == "PYAT_EXTERNAL_BOUNDARY": continue
        if n in state["axes"] and n not in invalidated:
            state["axes"][n]["consumer"] = "INVALIDATED_BY_UPSTREAM"
            invalidated.append(n); q.extend(graph.get(n, []))
    h["invalidated"] = sorted(set(invalidated)); h["pyat_boundary_touched"] = False
    state["gaps"].append({"id": "GAP_TRANSITION_CHECK_" + h["history_id"], "domain": "TRANSITION", "node": node_id, "status": "RE_EVALUATE", "owner": fixture.get("owner", "UNKNOWN"), "next": "Re-evaluate downstream consumer evidence.", "consequence": "Prior inherited status may not be current."})
    state["freshness"]["generated_at"] = datetime.now(timezone.utc).isoformat()
    return state

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=STATE)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh")
    sub.add_parser("overview")
    for name in ("source", "consumer", "alternatives", "history", "critical-path"):
        p = sub.add_parser(name); p.add_argument("id")
    z = sub.add_parser("zoom"); z.add_argument("id"); z.add_argument("--depth", type=int, default=1)
    g = sub.add_parser("gaps"); g.add_argument("--domain", default="")
    sub.add_parser("work-now"); sub.add_parser("workers"); sub.add_parser("export")
    i = sub.add_parser("intake-return"); i.add_argument("file", type=Path)
    a = sub.add_parser("apply-authorized-transition"); a.add_argument("file", type=Path)
    args = parser.parse_args(argv)
    if args.command == "refresh":
        state = build_state(); _save(state); _print(_overview(state)); return 0
    state = _load_state()
    if args.command == "overview":
        _print(_overview(state))
    elif args.command == "zoom":
        if args.id not in {n["id"] for n in state["nodes"]}: _print({"error": "UNKNOWN_ID"}); return 1
        nodes, edges = _neighbors(state, args.id, args.depth); _print({"root": args.id, "depth": args.depth, "nodes": nodes, "edges": edges})
    elif args.command == "gaps":
        _print([g for g in state["gaps"] if not args.domain or g["domain"] == args.domain])
    elif args.command == "critical-path":
        _print({"goal": args.id, "path": _critical_path(state, args.id)})
    elif args.command == "source":
        row = next((x for x in state["source_manifest"]["rows"] if x["id"] == args.id), None)
        _print(row or {"error": "UNKNOWN_SOURCE"})
    elif args.command == "consumer":
        out = [e for e in state["edges"] if e["from"] == args.id and (e["to"].startswith("L4") or "consumer" in e.get("relation", ""))]
        _print({"node": args.id, "consumer_edges": out, "axes": state["axes"].get(args.id)})
    elif args.command == "alternatives":
        row = next((x for x in _load(SEED_REGISTRY)["rows"] if x["id"] == args.id), None)
        _print({"id": args.id, "row": (row or {}).get("unresolved_alternatives", []), "product_link": (row or {}).get("product_link")})
    elif args.command == "work-now":
        _print({"decision": "HQ_JUDGMENT_REQUIRED", "candidates": state["work_now"], "note": "Not a priority decree."})
    elif args.command == "workers":
        _print({"workers": state["workers"], "active_local_processes": "NOT_OBSERVED_BY_REFERENCE", "caution": "Git branch does not prove running process."})
    elif args.command == "history":
        _print([h for h in state["history"] if h.get("history_id") == args.id or h.get("node_id") == args.id])
    elif args.command == "export":
        _print(state)
    elif args.command == "intake-return":
        item = intake_candidate(state, _load(args.file))
        _save(state); _print(item)
    elif args.command == "apply-authorized-transition":
        fixture = _load(args.file)
        try:
            _apply_transition(state, fixture)
        except ValueError as error:
            _print({"status": "REFUSED", "reason": str(error)}); return 1
        _save(state); _print({"status": "APPLIED_CANDIDATE_ONLY", "history": state["history"][-1], "axes": state["axes"][fixture["node_id"]], "gaps": state["gaps"][-1]})
    return 0

if __name__ == "__main__":
    sys.exit(main())
