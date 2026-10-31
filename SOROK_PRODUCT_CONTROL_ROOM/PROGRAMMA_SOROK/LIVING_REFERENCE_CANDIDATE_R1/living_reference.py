#!/usr/bin/env python3
"""Persistent Sorok-only living reference, evidence merge and causal regrade.

R2 repairs the same R1 reference in place. The state file is the source of truth:
``refresh`` merges the frozen seed graph and source rows into the existing state
instead of rebuilding it. Typed O-SCIENCE evidence is imported as candidate
evidence into the same graph. Derived gaps, work-now, blocked-chain and product
coverage are recomputed from the graph and axes; they are not module constants.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
STATE = ROOT / "state.json"
SNAPSHOT = ROOT / "SNAPSHOT.json"
SEED_REGISTRY = ROOT / "seed_source_registry.json"
SEED_GRAPH = ROOT / "seed_graph.json"
SEED_SLOTS = ROOT / "seed_slots.json"
SOURCE_MANIFEST = ROOT / "source_manifest.json"
OSCIENCE_PATCH = ROOT / "seed_oscience_patch.json"
OSCIENCE_102 = ROOT / "seed_oscience_102.json"
OSCIENCE_BACKWARD = ROOT / "seed_oscience_backward.json"

SCHEMA = "SOROK_PROGRAMMA_LIVING_REFERENCE_STATE@2"
VERSION = "R2"
STARTUP_SHA = "67f667421fc90b22aad95cfc253a16feabc92348"
SEED_BUILD_PREMAIN = "f40c26301d7d5b811c1bb92efa4934ad564ce5b3"
R3_CUT = "e50d32eb6816578145d17dcd637a0b90b3a1ef40"
R3_REVIEW_OLD_NEGATIVE = "3f3d9ec2fddc36bd4047bc6c730382c65a5e692a"
R3_REVIEW_CURRENT = "06f40a3eabb4acfc57f433144224695c2427c25f"
OSCIENCE_CUT = "45efe65f73475e6a815e5fe93c3ee5179de27f67"
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

SPECIFIC_S_GAPS = {
    "S5": ("GAP_S5_NORMATIVE_OUTPUT", "HQ / qualified product-science owner", "Issue normative alternatives, uncertainty law and harmful-attachment evaluation.", "A5 cannot distinguish flourishing from affection/compliance."),
    "S7": ("GAP_S7_PRAXIS_OUTPUT", "HQ / user-praxis product owner", "Issue evidence threshold, feedback cadence, opt-in and privacy policy.", "User reflection can become pseudo-diagnosis or covert scoring."),
    "S11": ("GAP_S11_HUMAN_UX", "Product UX owner", "Issue accessible encounter flows and honest opacity behavior.", "CP-A5 reader alone is not human-usable A5."),
    "S13": ("GAP_S13_REVENUE_MODEL", "Accountable business/product owner", "Issue non-extractive pricing, notification and retention constraints.", "Engagement can be mistaken for human good."),
    "S14": ("GAP_S14_SOCIAL_SAFETY", "Safety/privacy owner", "Issue abuse, consent, deletion and cross-user boundaries.", "Storage authenticity does not provide social safety."),
    "S15": ("GAP_S15_HUMAN_ALPHA", "Alpha/participant-research owner", "Design bounded reference-person trial with ethics and actual participants.", "Persuasive LLM presentation cannot establish a historically constituted other."),
}

PYAT_BOUNDARY = {
    "id": "PYAT_EXTERNAL_BOUNDARY",
    "external_owner": "Pyat HQ / original source and scientific issuer",
    "required_inputs": ["source-qualified objective world/possibility", "exact source/version/as-of/uncertainty", "N11 world acceptance", "N12 wake/defer", "C11/Pyat person weld permission"],
    "sorok_receiver": ["C0", "C4", "C10", "C11", "C12"],
    "sorok_has": "sourcefree boundary model only; no native Pyat world, N11/N12 acceptance or C11 weld",
    "prohibited": ["ingesting Pyat program health", "issuing Pyat operations", "inventing N11/N12", "fused controller"],
    "status": "EXTERNAL_OWNER_HELD",
}

NEGATIVE_SOURCE = {"SOURCE_NOT_FOUND", "SOURCE_WITHDRAWN", "MISSING", "SOURCE_INVALID"}
NEGATIVE_REVIEW = {"REVIEW_FAILED", "SEALED_NEGATIVE"}
NEGATIVE_ENGINEERING = {"FAILED", "REGRESSED"}
NEGATIVE_SCIENCE = {"REFUSED", "NATIVE_ISSUED_REVOKED"}
NEGATIVE_AUTHORITY = {"REVOKED"}
NEGATIVE_ALL = NEGATIVE_SOURCE | NEGATIVE_REVIEW | NEGATIVE_ENGINEERING | NEGATIVE_SCIENCE | NEGATIVE_AUTHORITY

ALLOWED_TRANSITIONS = {
    "source_recovery": {"SOURCE_VERIFIED", "SOURCE_NOT_FOUND", "SOURCE_WITHDRAWN", "MISSING", "CANDIDATE_EVIDENCE", "SOURCE_INVALID"},
    "engineering": {"CANDIDATE_UPGRADED", "INDEPENDENT_ACCEPT_SCOPED", "REGRESSED", "FAILED", "AUTHOR_PASS_VERIFIED", "UNCHANGED", "MISSING_FUNCTION", "CANDIDATE_ONLY"},
    "science": {"CANDIDATE_EVIDENCE", "HYPOTHESIS", "HOLD_MANUAL_VERIFICATION", "REFUSED", "NOT_ISSUED", "CANDIDATE_EVIDENCE_NOT_ISSUED"},
    "authority": {"NOT_ADOPTED", "UNADOPTED", "CANDIDATE_ONLY", "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION", "REVOKED"},
    "review": {"PENDING", "REVIEW_PASSED_SCOPED", "REVIEW_FAILED", "SEALED", "UNREVIEWED_CANDIDATE_EVIDENCE", "SEALED_NEGATIVE"},
    "consumer": {"CANDIDATE_READY", "INVALIDATED_BY_UPSTREAM", "ACTUAL", "NONE_PROVEN_AT_PREMAIN", "NONE_NATIVE", "NOT_APPLICABLE"},
    "human": {"NOT_PROVEN", "CANDIDATE_LAB_DEMO_NOT_HUMAN_A5", "PROVEN"},
    "operational": {"CANDIDATE_ONLY", "RETURNED_UNADOPTED", "ACTIVE_CANDIDATE", "CANDIDATE_EVIDENCE", "RETURNED_SHA__INDEX_INPUT"},
}

AUTHORITY_OWNER_SLOTS = {
    "SOROK_ORIGINAL_PRODUCT_OWNER",
    "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER",
    "ORIGINAL_SOROK_C_A_OWNER",
    "SOROK_ORIGINAL_SCIENCE_OWNER",
    "CAN008_OWNER",
    "CAN011_OWNER",
    "ADP_OWNER",
    "SCI05_OWNER",
    "C9_C12_OWNER",
    "C11_OWNER",
    "PYAT_HQ",
    "SOROK_HQ",
    "SOROK_ALPHA_OWNER",
    "SOROK_PRODUCT_UX_OWNER",
    "SOROK_SAFETY_OWNER",
    "SOROK_BUSINESS_OWNER",
}

EVIDENCE_KINDS = {
    "SOURCE_RECORD",
    "SOURCEFREE_REVIEW",
    "OWNER_GRANT",
    "HUMAN_PARTICIPANT",
    "ORIGINAL_SCIENCE_ISSUANCE",
    "SYNTHETIC_DEMO",
    "UNSTRUCTURED_STRING",
}


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git(args: list[str], cwd: Path | None = None) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd or REPO), *args],
            capture_output=True, text=True, check=False, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode:
        return None
    return result.stdout.strip()


def _head(ref: str) -> dict[str, str]:
    sha = _git(["rev-parse", ref])
    if not sha:
        return {"ref": ref, "sha": "UNKNOWN", "committed_at": "UNKNOWN"}
    when = _git(["show", "-s", "--format=%cI", sha]) or "UNKNOWN"
    return {"ref": ref, "sha": sha, "committed_at": when}


def observe_source_cut(git_enabled: bool = True) -> dict[str, Any]:
    """Read the current source cut from local Git refs when available."""
    if not git_enabled:
        return {
            "read_at": "STATIC_FALLBACK",
            "status": "GIT_DISABLED",
            "heads": {
                "premain": {"ref": "origin/integration/pre-main-reconciliation-r1", "sha": "UNKNOWN", "committed_at": "UNKNOWN"},
                "olive": {"ref": "origin/agent/sorok-programma-living-reference-s2-sourcegraded-operating-map-r1-20261031", "sha": STARTUP_SHA, "committed_at": "UNKNOWN"},
                "r3": {"ref": "origin/agent/sorok-oindex-r3-exact-source-integrity-repair-20261031-r1", "sha": R3_CUT, "committed_at": "UNKNOWN"},
                "r3_review": {"ref": "origin/review/sorok-oindex-r3-independent-source-and-map-acceptance-20261031", "sha": R3_REVIEW_CURRENT, "committed_at": "UNKNOWN"},
                "o_science": {"ref": "OSCIENCE_CUT", "sha": OSCIENCE_CUT, "committed_at": "UNKNOWN"},
            },
        }
    heads = {
        "premain": _head("origin/integration/pre-main-reconciliation-r1"),
        "olive": _head("origin/agent/sorok-programma-living-reference-s2-sourcegraded-operating-map-r1-20261031"),
        "r3": _head("origin/agent/sorok-oindex-r3-exact-source-integrity-repair-20261031-r1"),
        "r3_review": _head("origin/review/sorok-oindex-r3-independent-source-and-map-acceptance-20261031"),
        "o_science": _head(OSCIENCE_CUT),
    }
    observed = sum(1 for head in heads.values() if head["sha"] != "UNKNOWN")
    return {
        "read_at": _utc_now(),
        "status": "OBSERVED_LOCAL_GIT_REFS" if observed == len(heads) else "PARTIAL_GIT_REFS",
        "heads": heads,
        "note": "Git refs are read-only observations. SEALED is not running; branch presence is not a process lease.",
    }


def _filter_source_manifest(manifest: dict) -> dict:
    rows = [x for x in manifest["rows"] if x.get("namespace") == "SOROK"]
    return {
        "schema": "SOROK_LIVING_SOURCE_MANIFEST@1",
        "build_premain": SEED_BUILD_PREMAIN,
        "rows": rows,
        "reference_sources": manifest["reference_sources"],
        "manifest_digest": _digest(rows + manifest["reference_sources"]),
    }


def _axes(row: dict | None, node: dict) -> dict:
    if row is None:
        return {
            "source_recovery": "INDEX_ONLY",
            "science": "NOT_ASSESSED",
            "engineering": "INDEX_ONLY",
            "authority": "NOT_ADOPTED",
            "review": "NOT_APPLICABLE",
            "consumer": "NOT_APPLICABLE",
            "human": "NOT_PROVEN",
            "operational": "RETURNED_UNADOPTED" if node.get("id") in {"CP-A5-R2", "C9C12-R2", "B-F1CR-R2", "V3CORE-R1"} else "INDEX_ONLY",
        }
    operational = "RETURNED_UNADOPTED" if row["id"] in {"CP-A5-R2", "C9C12-R2", "B-F1CR-R2", "V3CORE-R1"} else "RETURNED_SHA__INDEX_INPUT"
    return {
        "source_recovery": row.get("status_class", "SOURCE_PRESENT"),
        "science": row.get("science_grade", "NOT_ISSUED"),
        "engineering": row.get("engineering_grade", "SOURCE_DEFINITION_ONLY"),
        "authority": row.get("authority_grade", "NOT_ADOPTED"),
        "review": row.get("independent_review", "NOT_INDEPENDENTLY_REVIEWED"),
        "consumer": row.get("actual_consumer_state", "NONE_PROVEN_AT_PREMAIN"),
        "human": row.get("human_grade", "NOT_PROVEN"),
        "operational": operational,
    }


def _classify_edge(edge: dict) -> dict:
    relation = str(edge.get("relation") or "")
    low = relation.lower()
    hypothetical = any(token in low for token in ("candidate", "hypothesis", "conceptual", "index_link", "index_containment", "navigation"))
    index_like = any(token in low for token in (
        "historical_exploratory", "historical_workstream", "s0_s16", "readback", "crosswalk",
        "organ_contains", "backward_person_source_path", "index_containment",
    ))
    causal = False
    required = False
    dependency_type = "STRUCTURAL_OR_INDEX"
    if index_like:
        dependency_type = "INDEX_OR_GOVERNANCE"
    else:
        if any(token in low for token in ("requires", "require", "depends", "input", "feeds", "produces", "owner_output")):
            dependency_type = "REQUIRED_DEPENDENCY"
            required = True
            causal = True
        if any(token in low for token in ("consumer", "named_first_consumer")):
            dependency_type = "CONSUMER_DEPENDENCY"
            required = True
            causal = True
        if any(token in low for token in ("governs", "blocks_named_edge")):
            dependency_type = "GOVERNANCE_REQUIREMENT"
            required = True
            causal = False
        if "evidence" in low or "author_test" in low or "negative_preserved" in low:
            dependency_type = "EPISTEMIC_EVIDENCE"
            required = False
            causal = False
    if hypothetical:
        dependency_type = "HYPOTHETICAL_OR_INDEX"
        required = False
        causal = False
    if "scientific_product_requisite_link" in low:
        dependency_type = "HYPOTHETICAL_PRODUCT_REQUISITE"
        required = False
        causal = False
    if "requires_source_input_transformation" in low:
        dependency_type = "CANDIDATE_MISSING_FUNCTION_REQUIREMENT"
        required = False
        causal = False
        hypothetical = True
    result = copy.deepcopy(edge)
    result.setdefault("from", edge.get("from"))
    result.setdefault("to", edge.get("to"))
    result["relation"] = relation
    result["dependency_type"] = dependency_type
    result["required"] = bool(required)
    result["causal"] = bool(causal)
    result["hypothetical"] = bool(hypothetical or dependency_type.startswith("HYPOTHETICAL"))
    result.setdefault("grade", "INDEX_LINK" if not required else "SOURCE_DEFINED_REQUIREMENT")
    result.setdefault("source", {})
    result["edge_id"] = "EDGE_" + _digest({
        "from": result["from"],
        "to": result["to"],
        "relation": relation,
        "source": result.get("source", {}),
    })[:16]
    return result


def _source_rows(registry: dict) -> dict[str, dict]:
    return {row["id"]: row for row in registry["rows"]}


def _workstreams_from_registry(registry: dict) -> list[dict]:
    rows = _source_rows(registry)
    out = []
    for i in range(17):
        sid = f"S{i}"
        row = rows.get(sid)
        if not row:
            continue
        out.append({
            "id": sid,
            "title": row.get("title"),
            "question": row.get("question"),
            "output": row.get("output"),
            "owner": row.get("owner"),
            "source": row.get("evidence_source"),
            "first_consumer": row.get("first_consumer"),
            "first_consumer_required": row.get("first_consumer_required"),
            "product_link": row.get("product_link"),
            "alternatives": row.get("unresolved_alternatives") or row.get("alternatives") or [],
            "candidate_evidence": None,
            "source_grade": "SOURCE_EXACT",
            "science_grade": "NOT_ISSUED",
            "consumer_state": row.get("actual_consumer_state"),
        })
    return out


def _empty_axes_for_node(node: dict) -> dict:
    return {
        "source_recovery": "INDEX_ONLY",
        "science": "NOT_ASSESSED",
        "engineering": "INDEX_ONLY",
        "authority": "NOT_ADOPTED",
        "review": "NOT_APPLICABLE",
        "consumer": "NOT_APPLICABLE",
        "human": "NOT_PROVEN",
        "operational": "CANDIDATE_ONLY",
    }


def _base_nodes_and_edges(graph: dict) -> tuple[list[dict], list[dict]]:
    nodes = [copy.deepcopy(n) for n in graph["nodes"] if not str(n["id"]).startswith("PYAT_") and n["id"] != "L1_PYAT_SEPARATE"]
    node_ids = {n["id"] for n in nodes}
    boundary = dict(PYAT_BOUNDARY, layer="L1", kind="EXTERNAL_BOUNDARY", title="Qualified Pyat world/N11/N12/C11 boundary")
    if boundary["id"] not in node_ids:
        nodes.append(boundary)
        node_ids.add(boundary["id"])
    for rid, title in (("R6", "R6 finite 39/R41 source closure"), ("R7", "R7 cross-lineage source closure")):
        if rid not in node_ids:
            nodes.append({
                "id": rid,
                "layer": "L5",
                "kind": "SOURCE_RECOVERY",
                "title": title,
                "status": "RETURNED_SHA__UNADOPTED",
                "source_refs": ["28e38ebbf08bbfaeb152ae022046e1303d9a2e40" if rid == "R6" else "7f25fb9bfc48679a47ccc61b36354f20fef54f1c"],
                "hq_judgment_required": True,
            })
            node_ids.add(rid)
    edges = [copy.deepcopy(e) for e in graph["edges"] if e["from"] in node_ids and e["to"] in node_ids]
    for e in edges:
        e.setdefault("status", "INDEX_LINK")
        e.setdefault("hq_judgment_required", True)
    if not any(e["from"] == boundary["id"] and e["to"] == "C0" for e in edges):
        edges.append({"from": boundary["id"], "to": "C0", "relation": "external_source_potential_to_sorok_c0", "status": "EXTERNAL_OWNER_HELD", "hq_judgment_required": True})
    for rid in ("R6", "R7"):
        if "L1_RECOVERY" in node_ids and not any(e["from"] == "L1_RECOVERY" and e["to"] == rid for e in edges):
            edges.append({"from": "L1_RECOVERY", "to": rid, "relation": "recovery_evidence_contained", "status": "RETURNED_SHA__UNADOPTED", "hq_judgment_required": True})
    return nodes, [_classify_edge(e) for e in edges]


def _sectors(nodes: list[dict], evidence_nodes: list[str] | None = None) -> list[dict]:
    node_ids = {n["id"] for n in nodes}
    out = []
    for name, title, required, challenged, status in SECTORS:
        req = [x for x in required if x in node_ids]
        missing = [x for x in required if x not in node_ids]
        out.append({
            "id": name,
            "title": title,
            "required_nodes": req,
            "missing_nodes": missing,
            "challenged": challenged,
            "status": status,
            "coverage": "PARTIAL" if missing or challenged else "PRESENT_CANDIDATE",
        })
    if evidence_nodes:
        out.append({
            "id": "OSCIENCE_MISSING_FUNCTIONS",
            "title": "C12→A5 missing function and consumer rows",
            "required_nodes": list(evidence_nodes),
            "missing_nodes": [],
            "challenged": list(evidence_nodes),
            "status": "CANDIDATE_EVIDENCE_UNREVIEWED",
            "coverage": "CANDIDATE_ONLY",
        })
    return out


def _initial_workers() -> list[dict]:
    return [
        {"id": "R3_INDEX", "branch": "agent/sorok-oindex-r3-exact-source-integrity-repair-20261031-r1", "sha": R3_CUT, "status": "RETURNED_UNADOPTED", "editor_model": "OpenCode/DeepSeek V4.1-Flash MAX", "reviewer": "separate R3-IR required", "cost": "UNKNOWN"},
        {"id": "R3_IR_REVIEW", "branch": "review/sorok-oindex-r3-independent-source-and-map-acceptance-20261031", "sha": R3_REVIEW_CURRENT, "status": "SEALED_NOT_ASSUMED_RUNNING", "editor_model": "UNKNOWN", "reviewer": "independent", "cost": "UNKNOWN"},
        {"id": "O_LIVE_R1", "branch": "agent/sorok-programma-living-reference-s2-sourcegraded-operating-map-r1-20261031", "sha": STARTUP_SHA, "status": "SEALED_RETURNED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "O_SCIENCE_R1", "branch": "research/sorok-programma-o-science-product-requisite-coverage-r1-20261031", "sha": OSCIENCE_CUT, "status": "RETURNED_CANDIDATE_EVIDENCE", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "CP-A5-R2", "branch": "agent/sorok-cp-a5-r2-multicontext-encounter-20261030", "sha": "913765328e4fab12b150ea01421ed6b445158184", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "OpenCode/DeepSeek V4.1-Flash MAX", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "C9C12-R2", "branch": "agent/sorok-c9c12-r2-versioned-writer-reader-clock-20261030", "sha": "c78404724052496fdec8608c8b0e833c0f7c4ecc", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "B-F1CR-R2", "branch": "agent/sorok-b-f1cr-targetless-c10-20261030", "sha": "bf3273c294c704ad7c631559b9866d351bb4f103", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "V3CORE-R1", "branch": "agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030", "sha": "b5cb3f917402b992d7cbe933af0b378d2b37cbfd", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
    ]


def _base_state(observed_source: dict[str, Any] | None = None) -> dict:
    registry = _load(SEED_REGISTRY)
    graph = _load(SEED_GRAPH)
    slots = _load(SEED_SLOTS)
    manifest = _filter_source_manifest(_load(SOURCE_MANIFEST))
    rows = _source_rows(registry)
    nodes, edges = _base_nodes_and_edges(graph)
    axes = {}
    for node in nodes:
        if node["id"] == "PYAT_EXTERNAL_BOUNDARY":
            axes[node["id"]] = {
                "source_recovery": "EXTERNAL_OWNER_HELD",
                "science": "NOT_ISSUED",
                "engineering": "EXTERNAL",
                "authority": "EXTERNAL_OWNER",
                "review": "NOT_APPLICABLE",
                "consumer": "EXTERNAL_BOUNDARY",
                "human": "NOT_PROVEN",
                "operational": "EXTERNAL_HELD",
            }
        elif node["id"] in {"R6", "R7"}:
            axes[node["id"]] = _axes(None, node)
        else:
            axes[node["id"]] = _axes(rows.get(node["id"]), node)
    observed = observed_source or observe_source_cut()
    state = {
        "schema": SCHEMA,
        "version": VERSION,
        "build_startup": STARTUP_SHA,
        "seed_build_premain": SEED_BUILD_PREMAIN,
        "source_snapshot": observed,
        "source_cut_stale": False,
        "version_vector": {
            "sorok_startup": STARTUP_SHA,
            "seed_build_premain": SEED_BUILD_PREMAIN,
            "r3_index": R3_CUT,
            "r3_review_old_negative": R3_REVIEW_OLD_NEGATIVE,
            "r3_review_current": R3_REVIEW_CURRENT,
            "o_science": OSCIENCE_CUT,
            "program_map": PROGRAM_MAP,
            "hq_synthesis": HQ_SYNTHESIS,
            "r6": "28e38ebbf08bbfaeb152ae022046e1303d9a2e40",
            "r7": "7f25fb9bfc48679a47ccc61b36354f20fef54f1c",
            "four_assets": {"CP-A5-R2": "913765328e4fab12b150ea01421ed6b445158184", "C9C12-R2": "c78404724052496fdec8608c8b0e833c0f7c4ecc", "B-F1CR-R2": "bf3273c294c704ad7c631559b9866d351bb4f103", "V3CORE-R1": "b5cb3f917402b992d7cbe933af0b378d2b37cbfd"},
        },
        "nodes": nodes,
        "edges": edges,
        "source_manifest": manifest,
        "source_count": len(manifest["rows"]),
        "pyat_boundary": dict(PYAT_BOUNDARY, layer="L1", kind="EXTERNAL_BOUNDARY", title="Qualified Pyat world/N11/N12/C11 boundary"),
        "sectors": _sectors(nodes),
        "workstreams": _workstreams_from_registry(registry),
        "legacy_records": [],
        "missing_functions": [],
        "node_evidence": {},
        "evidence_imports": {},
        "evidence_review_status": "NO_OSCIENCE_IMPORT",
        "intake_gaps": [],
        "authority_holds": [],
        "invalidation_index": {},
        "axes": axes,
        "workers": _initial_workers(),
        "flights": [{"id": "SOROK_SOURCEFREE_REFERENCE", "status": "CANDIDATE_ONLY", "owner": "Sorok HQ/original owners", "note": "No new worker launched by this reference."}],
        "history": [{
            "history_id": "H0001",
            "kind": "GENESIS",
            "state": "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED",
            "source_vector": {"startup": STARTUP_SHA, "seed_build_premain": SEED_BUILD_PREMAIN, "r3": R3_CUT},
            "read_at": observed.get("read_at", "UNKNOWN"),
        }],
        "freshness": {"generated_at": observed.get("read_at", _utc_now()), "refresh_command": "python3 living_reference.py refresh"},
        "seed_slots": slots,
    }
    _recompute(state)
    return state


def build_state(observed_source: dict[str, Any] | None = None) -> dict:
    """Build the clean R2 state from frozen seeds (no prior intake)."""
    return _base_state(observed_source)


def _node_map(state: dict) -> dict[str, dict]:
    return {n["id"]: n for n in state["nodes"]}


def _edge_map(state: dict) -> dict[str, dict]:
    return {e["edge_id"]: e for e in state["edges"]}


def _merge_structural(state: dict, seed: dict) -> dict[str, Any]:
    added_nodes = []
    node_ids = {n["id"] for n in state["nodes"]}
    for node in seed["nodes"]:
        if node["id"] not in node_ids:
            state["nodes"].append(copy.deepcopy(node))
            node_ids.add(node["id"])
            added_nodes.append(node["id"])
            if node["id"] not in state["axes"]:
                state["axes"][node["id"]] = copy.deepcopy(seed["axes"].get(node["id"], _empty_axes_for_node(node)))
    edge_ids = {e["edge_id"] for e in state["edges"]}
    added_edges = []
    for edge in seed["edges"]:
        if edge["edge_id"] not in edge_ids:
            state["edges"].append(copy.deepcopy(edge))
            edge_ids.add(edge["edge_id"])
            added_edges.append(edge["edge_id"])
    existing_rows = {r["id"]: r for r in state["source_manifest"]["rows"]}
    for row in seed["source_manifest"]["rows"]:
        if row["id"] not in existing_rows:
            state["source_manifest"]["rows"].append(copy.deepcopy(row))
    state["source_manifest"]["manifest_digest"] = _digest(
        state["source_manifest"]["rows"] + state["source_manifest"]["reference_sources"])
    state["source_count"] = len(state["source_manifest"]["rows"])
    if not state.get("workstreams"):
        state["workstreams"] = copy.deepcopy(seed["workstreams"])
    return {"added_nodes": added_nodes, "added_edges": added_edges}


def _source_delta(previous: dict, current: dict) -> dict:
    if not previous:
        return {"changed": False, "fields": [], "previous": {}, "current": current}
    prev_heads = previous.get("heads") or {}
    curr_heads = current.get("heads") or {}
    fields = sorted(k for k in set(prev_heads) | set(curr_heads) if (prev_heads.get(k) or {}).get("sha") != (curr_heads.get(k) or {}).get("sha"))
    return {"changed": bool(fields), "fields": fields, "previous": prev_heads, "current": curr_heads}


def refresh_state(existing: dict | None, observed_source: dict[str, Any] | None = None) -> dict:
    """Merge seeds and current source cut into the persisted state without reset."""
    observed = observed_source or observe_source_cut()
    seed = _base_state(observed)
    if existing is None:
        return seed
    state = copy.deepcopy(existing)
    state.setdefault("axes", {})
    merge = _merge_structural(state, seed)
    previous_snapshot = state.get("source_snapshot") or {}
    delta = _source_delta(previous_snapshot, observed)
    state["source_snapshot"] = observed
    state["source_cut_stale"] = bool(delta["changed"])
    state["version"] = VERSION
    state["schema"] = SCHEMA
    state["freshness"] = {"generated_at": observed.get("read_at", _utc_now()), "refresh_command": "python3 living_reference.py refresh"}
    state["history"].append({
        "history_id": "H%04d" % (len(state["history"]) + 1),
        "kind": "REFRESH_MERGE",
        "added_nodes": merge["added_nodes"],
        "added_edges": merge["added_edges"],
        "source_delta": delta,
        "preserved_history_count": len(state["history"]),
        "read_at": observed.get("read_at", _utc_now()),
    })
    if delta["changed"]:
        state["history"].append({
            "history_id": "H%04d" % (len(state["history"]) + 1),
            "kind": "SOURCE_CUT_CHANGED",
            "fields": delta["fields"],
            "previous": delta["previous"],
            "current": delta["current"],
            "read_at": observed.get("read_at", _utc_now()),
        })
    _recompute(state)
    return state


def _load_state(path: Path | None = None) -> dict:
    target = Path(path or STATE)
    if not target.exists():
        state = build_state()
        _save(state, target)
        return state
    state = _load(target)
    if state.get("schema") != SCHEMA:
        # Migrate R1 in place on first R2 read; never discard history.
        state = refresh_state(state, state.get("source_snapshot"))
        _save(state, target)
    return state


def _save(state: dict, path: Path | None = None, snapshot: Path | None = None) -> None:
    target = Path(path or STATE)
    snap = Path(snapshot) if snapshot else (target.parent / SNAPSHOT.name)
    state["state_digest"] = _digest({k: v for k, v in state.items() if k != "state_digest"})
    payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
    for destination in (target, snap):
        destination.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=destination.name + ".", dir=str(destination.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, destination)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def _neighbors(state: dict, node_id: str, depth: int) -> tuple[list[dict], list[dict]]:
    nodes = _node_map(state)
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
                if edge not in result_edges:
                    result_edges.append(edge)
        result_nodes.extend(nodes[x] for x in sorted(nxt) if x in nodes)
        frontier = nxt
    return result_nodes, result_edges


def _required_outgoing(state: dict, node_id: str) -> list[dict]:
    return [e for e in state["edges"]
            if e["from"] == node_id and e.get("required") and e.get("causal") and not e.get("hypothetical")]


def _required_incoming(state: dict, node_id: str) -> list[dict]:
    return [e for e in state["edges"]
            if e["to"] == node_id and e.get("required") and e.get("causal") and not e.get("hypothetical")]


def _reachable_required(state: dict, node_id: str) -> list[str]:
    out: list[str] = []
    seen = {node_id}
    q = deque([node_id])
    while q:
        current = q.popleft()
        for edge in _required_outgoing(state, current):
            target = edge["to"]
            if target in seen or target == "PYAT_EXTERNAL_BOUNDARY":
                continue
            seen.add(target)
            out.append(target)
            q.append(target)
    return sorted(out)


def _axis_blockers(state: dict, node_id: str) -> list[dict]:
    axis = state["axes"].get(node_id, {})
    blockers = []
    for key, values, label in (
        ("source_recovery", NEGATIVE_SOURCE, "source loss"),
        ("science", {"NOT_ISSUED", "REFUSED", "CANDIDATE_EVIDENCE_NOT_ISSUED", "HOLD_MANUAL_VERIFICATION"}, "science not issued"),
        ("authority", {"NOT_ADOPTED", "UNADOPTED", "REVOKED", "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION"}, "owner authority held"),
        ("review", NEGATIVE_REVIEW, "review failed"),
        ("professional", set(), ""),
    ):
        if key == "professional":
            continue
        value = str(axis.get(key, ""))
        if value in values:
            blockers.append({"node": node_id, "axis": key, "status": value, "reason": label})
    if str(axis.get("consumer", "")).startswith("INVALIDATED"):
        blockers.append({"node": node_id, "axis": "consumer", "status": axis["consumer"], "reason": "consumer invalidated"})
    if node_id == "A5" and axis.get("human") != "PROVEN":
        blockers.append({"node": node_id, "axis": "human", "status": axis.get("human", "NOT_PROVEN"), "reason": "no human A5 evidence"})
    for edge in _required_incoming(state, node_id):
        source = edge["from"]
        source_axis = state["axes"].get(source, {})
        if source_axis.get("consumer", "").startswith("INVALIDATED"):
            blockers.append({"node": source, "axis": "consumer", "status": source_axis["consumer"], "reason": "required predecessor invalidated", "edge_id": edge["edge_id"]})
        if source_axis.get("source_recovery") in NEGATIVE_SOURCE:
            blockers.append({"node": source, "axis": "source_recovery", "status": source_axis["source_recovery"], "reason": "required source unavailable", "edge_id": edge["edge_id"]})
    dedup = {}
    for item in blockers:
        dedup[(item["node"], item["axis"], item.get("edge_id", ""))] = item
    return list(dedup.values())


def _impact(state: dict, node_id: str) -> dict:
    downstream = _reachable_required(state, node_id)
    node = _node_map(state).get(node_id, {})
    row = node.get("backward_consumer_row") or {}
    original_workstreams = sorted(set(row.get("original_workstreams") or []))
    l0 = [x for x in downstream if x.startswith("L0_")]
    sectors = sorted({
        s["id"] for s in state["sectors"]
        if node_id in s.get("required_nodes", []) or any(x in s.get("required_nodes", []) for x in downstream)
    })
    return {
        "downstream_required_count": len(downstream) + len(original_workstreams),
        "downstream_required_nodes": downstream,
        "affected_original_workstreams": original_workstreams,
        "affected_l0": l0,
        "affected_sectors": sectors,
    }


def _add_gap(gaps: dict[str, dict], gap: dict) -> None:
    gap_id = gap["id"]
    if gap_id in gaps:
        return
    gap.setdefault("blockers", [])
    gap.setdefault("impact", {"downstream_required_count": 0, "affected_l0": [], "affected_sectors": []})
    gap.setdefault("parallel_group", "CROSS_CUTTING")
    gap.setdefault("hq_judgment_required", True)
    gaps[gap_id] = gap


def compute_gaps(state: dict) -> list[dict]:
    """Derive gaps from current axes, source evidence and typed edges."""
    gaps: dict[str, dict] = {}
    nodes = _node_map(state)
    rows = {r["id"]: r for r in state["source_manifest"]["rows"]}
    workstreams = {w["id"]: w for w in state.get("workstreams", [])}
    for i in range(17):
        sid = f"S{i}"
        if sid not in nodes:
            continue
        row = rows.get(sid, {})
        ws = workstreams.get(sid, {})
        axis = state["axes"].get(sid, {})
        evidence = state.get("node_evidence", {}).get(sid, [])
        consumer = str(axis.get("consumer", ""))
        if consumer == "ACTUAL":
            continue
        specific = SPECIFIC_S_GAPS.get(sid)
        if specific:
            gap_id, owner, nxt, consequence = specific
        else:
            gap_id = f"GAP_WORKSTREAM_{sid}"
            owner = row.get("owner") or "SOROK_PRODUCT_HQ_ORIGINAL_WORKSTREAM_OWNER"
            nxt = f"Produce or verify the original output and name an actual first consumer: {ws.get('output') or row.get('output') or 'UNKNOWN'}"
            consequence = "Source definition is present but no actual product consumer is proven; source identity alone does not qualify the product."
        status = "CANDIDATE_EVIDENCE_CONSUMER_MISSING" if evidence else "SOURCE_DEFINED_CONSUMER_MISSING"
        _add_gap(gaps, {
            "id": gap_id,
            "domain": sid,
            "node": sid,
            "class": "WORKSTREAM_OUTPUT_OR_CONSUMER",
            "status": status,
            "owner": owner,
            "next": nxt,
            "consequence": consequence,
            "source_grade": ws.get("source_grade", "SOURCE_EXACT"),
            "science_grade": axis.get("science", "NOT_ISSUED"),
            "consumer_state": consumer,
            "blockers": _axis_blockers(state, sid),
            "impact": _impact(state, sid),
            "parallel_group": "PRODUCT_WORKSTREAM",
            "evidence_digest": _digest(evidence) if evidence else "",
        })
    for mf in state.get("missing_functions", []):
        node = mf["id"]
        axis = state["axes"].get(node, {})
        if axis.get("consumer") == "ACTUAL":
            continue
        _add_gap(gaps, {
            "id": "GAP_" + node,
            "domain": "C12_A5",
            "node": node,
            "class": "MISSING_FUNCTION",
            "status": "MISSING_FUNCTION_CANDIDATE",
            "owner": mf.get("required_owner") or mf.get("owner") or "UNKNOWN",
            "next": mf.get("transformation") or "Name and implement the missing typed function and actual consumer.",
            "consequence": mf.get("exact_falsifier_or_severance") or "No actual C12→A5 consumer is proven.",
            "required_input": mf.get("input"),
            "expected_output": mf.get("output"),
            "first_actual_downstream_consumer": mf.get("first_actual_downstream_consumer"),
            "blockers": _axis_blockers(state, node),
            "impact": _impact(state, node),
            "parallel_group": "C12_A5_FUNCTION",
            "evidence_digest": _digest(mf.get("source", {})),
        })
    for node_id, gap_id, status, owner, nxt, consequence, group in (
        ("C11", "GAP_NATIVE_C4_C11_PERSON", "SOURCEFREE_OR_SOURCE_ONLY", "Original Pyat/C11/C12 owners", "Separate native world/C11 person authority and actual C12 consumer.", "No native continuing person exists.", "NATIVE_PERSON"),
        ("C9C12-R2", "GAP_C9_C12_ANCHOR", "CANDIDATE", "C9R/BP4/C12 owners", "External anchor, mirror/outbox and durable actor readset decision.", "C12 durability remains sourcefree-only.", "NATIVE_PERSON"),
        ("F1CR_CLAIMED_PATCH", "GAP_B_F1CR_ORIGINAL", "SOURCE_NOT_FOUND", "F1C/F1CR owner", "Supply original patched bytes or accept/reject reconstruction.", "Native B source remains unavailable.", "SOURCE_RECOVERY"),
        ("N10", "GAP_NATIVE_SCIENCE_CAN_ADP", "NOT_ISSUED", "CAN/ADP/SCI05 owners", "Issue finite original rules and actor/event evidence.", "Sourcefree developmental behavior cannot be called native.", "SCIENCE_OWNER"),
        ("A5", "GAP_NATIVE_A5", "NOT_PROVEN", "Sorok human A5/research owner", "Human participant trial distinct from sourcefree encounter.", "No human-product proof.", "HUMAN_ALPHA"),
    ):
        if node_id not in nodes:
            continue
        axis = state["axes"].get(node_id, {})
        resolved = (
            (node_id == "F1CR_CLAIMED_PATCH" and axis.get("source_recovery") not in NEGATIVE_SOURCE)
            or (node_id == "N10" and axis.get("science") in {"ORIGINAL_ISSUED", "NATIVE_ISSUED"})
            or (node_id == "A5" and axis.get("human") == "PROVEN")
            or (node_id in {"C11", "C9C12-R2"} and axis.get("authority") in {"OWNER_ADOPTED", "NATIVE_ISSUED"})
        )
        if not resolved:
            _add_gap(gaps, {
                "id": gap_id,
                "domain": node_id,
                "node": node_id,
                "class": "NATIVE_OR_OWNER_BLOCKER",
                "status": status,
                "owner": owner,
                "next": nxt,
                "consequence": consequence,
                "blockers": _axis_blockers(state, node_id),
                "impact": _impact(state, node_id),
                "parallel_group": group,
            })
    _add_gap(gaps, {
        "id": "GAP_PYAT_BOUNDARY",
        "domain": "PYAT",
        "node": "PYAT_EXTERNAL_BOUNDARY",
        "class": "EXTERNAL_BOUNDARY",
        "status": "EXTERNAL_OWNER_HELD",
        "owner": "Pyat HQ/source owner",
        "next": "Supply qualified world/N11/N12/C11 grant to Sorok C0.",
        "consequence": "Sorok cannot infer the external world.",
        "blockers": [{"node": "PYAT_EXTERNAL_BOUNDARY", "axis": "authority", "status": "EXTERNAL_OWNER_HELD", "reason": "external owner held"}],
        "impact": _impact(state, "PYAT_EXTERNAL_BOUNDARY"),
        "parallel_group": "EXTERNAL_BOUNDARY",
    })
    for node_id, axis in state["axes"].items():
        if str(axis.get("consumer", "")).startswith("INVALIDATED"):
            _add_gap(gaps, {
                "id": "GAP_INVALIDATED_" + node_id,
                "domain": "INVALIDATION",
                "node": node_id,
                "class": "INVALIDATED_CONSUMER",
                "status": "INVALIDATED_BY_UPSTREAM",
                "owner": nodes.get(node_id, {}).get("owner", "UNKNOWN"),
                "next": "Restore the required source/review evidence, then independently re-evaluate the consumer.",
                "consequence": "The consumer claim is no longer current.",
                "blockers": _axis_blockers(state, node_id),
                "impact": _impact(state, node_id),
                "parallel_group": "RECOVERY",
            })
    if state.get("source_cut_stale"):
        _add_gap(gaps, {
            "id": "GAP_SOURCE_CUT_STALE",
            "domain": "SOURCE_CURRENTNESS",
            "node": "L0_GOVERNANCE",
            "class": "SOURCE_CUT_CHANGED",
            "status": "STALE_REQUIRES_REVALIDATION",
            "owner": "Sorok source/index owner",
            "next": "Re-verify exact source rows against the new source cut and re-run the source manifest validator.",
            "consequence": "The persisted reference retains old cut evidence; currentness is not automatically GREEN.",
            "blockers": [],
            "impact": {"downstream_required_count": 0, "affected_l0": [], "affected_sectors": ["S0_S16"]},
            "parallel_group": "SOURCE_CURRENTNESS",
        })
    if state.get("evidence_imports") and state.get("evidence_review_status") != "ACCEPTED":
        _add_gap(gaps, {
            "id": "GAP_OSCIENCE_EVIDENCE_REVIEW_PENDING",
            "domain": "O_SCIENCE",
            "node": "S0",
            "class": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "status": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "owner": "Independent I3 reviewer + Sorok HQ",
            "next": "Review the integrated O-SCIENCE patch at exact digest; do not promote hypothesis links to issued science.",
            "consequence": "17 workstreams, 14 missing functions and 226 hypothesis links remain candidate.",
            "blockers": [],
            "impact": {"downstream_required_count": 17, "affected_l0": [], "affected_sectors": ["S0_S16", "OSCIENCE_MISSING_FUNCTIONS"]},
            "parallel_group": "REVIEW",
        })
    for gap in state.get("intake_gaps", []):
        _add_gap(gaps, gap)
    return sorted(gaps.values(), key=lambda item: item["id"])


def compute_work_now(state: dict) -> dict:
    """Return evidence-backed candidate work, grouped by parallel route, no scalar rank."""
    gaps = state.get("gaps", [])
    groups: dict[str, list[dict]] = {}
    for gap in gaps:
        groups.setdefault(gap.get("parallel_group", "CROSS_CUTTING"), []).append(gap)
    candidates = []
    parallel_groups = []
    for group, items in sorted(groups.items()):
        items = sorted(items, key=lambda g: (-g.get("impact", {}).get("downstream_required_count", 0), g["id"]))
        parallel_groups.append({
            "group": group,
            "candidate_count": len(items),
            "candidate_ids": [g["id"] for g in items],
            "parallel_possible": len(items) > 1,
        })
        for gap in items:
            candidates.append({
                "gap_id": gap["id"],
                "node": gap["node"],
                "domain": gap["domain"],
                "status": gap["status"],
                "owner": gap["owner"],
                "next": gap["next"],
                "consequence": gap["consequence"],
                "blockers": gap.get("blockers", []),
                "impact": gap.get("impact", {}),
                "parallel_group": group,
                "hq_judgment_required": True,
            })
    return {
        "decision": "HQ_JUDGMENT_REQUIRED",
        "source": "DYNAMIC_GAPS_AND_TYPED_BLOCKERS",
        "criteria": ["source_exactness", "typed_required_blocker", "actual_consumer", "science_state", "authority_state", "human_state"],
        "no_scalar_priority": True,
        "candidates": candidates,
        "parallel_groups": parallel_groups,
        "note": "Relative impact and blockers are evidence-backed; they are not a priority decree or a critical scientific path.",
    }


def blocked_chain(state: dict, goal: str) -> dict:
    """Typed required-incoming blocked-chain/impact view, excluding hypothesis edges."""
    nodes = _node_map(state)
    if goal not in nodes:
        return {"goal": goal, "error": "UNKNOWN_GOAL", "kind": "TYPED_BLOCKED_CHAIN"}
    incoming = {node: _required_incoming(state, node) for node in nodes}
    parent: dict[str, str] = {}
    seen = {goal}
    q = deque([goal])
    blocked = []
    while q:
        current = q.popleft()
        blockers = _axis_blockers(state, current)
        if blockers:
            blocked.append({"node": current, "blockers": blockers, "path": _path_to(goal, current, parent)})
        for edge in incoming.get(current, []):
            source = edge["from"]
            if source not in seen and source != "PYAT_EXTERNAL_BOUNDARY":
                seen.add(source)
                parent[source] = current
                q.append(source)
    hypothetical = sum(1 for e in state["edges"] if e.get("hypothetical"))
    return {
        "goal": goal,
        "kind": "TYPED_BLOCKED_CHAIN",
        "blocked": blocked,
        "required_edges_considered": sum(len(v) for v in incoming.values()),
        "hypothetical_edges_excluded": hypothetical,
        "note": "This is a required-blocker/impact view, not a BFS shortest path or a scientific priority.",
    }


def _path_to(goal: str, current: str, parent: dict[str, str]) -> list[str]:
    path = [current]
    cursor = current
    guard = set()
    while cursor != goal and cursor in parent and cursor not in guard:
        guard.add(cursor)
        cursor = parent[cursor]
        path.append(cursor)
    return list(reversed(path)) if path and path[-1] == goal else path


def _critical_path(state: dict, goal: str) -> list[str] | None:
    """Legacy DAG illustration retained for compatibility, not criticality."""
    nodes = _node_map(state)
    if goal not in nodes:
        return None
    graph: dict[str, list[str]] = {}
    for edge in state["edges"]:
        graph.setdefault(edge["from"], []).append(edge["to"])
    q = deque([(goal, [goal])])
    seen = {goal}
    while q:
        node, path = q.popleft()
        if nodes.get(node, {}).get("layer") == "L5":
            return path
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + [nxt]))
    return None


def compute_coverage(state: dict) -> dict:
    nodes = _node_map(state)
    sectors = []
    for sector in state["sectors"]:
        required = sector.get("required_nodes", [])
        present = [x for x in required if x in nodes]
        missing = [x for x in required if x not in nodes]
        invalidated = [x for x in present if str(state["axes"].get(x, {}).get("consumer", "")).startswith("INVALIDATED")]
        status = "BLOCKED" if invalidated else ("PARTIAL_CANDIDATE" if missing or sector.get("challenged") else "PRESENT_CANDIDATE")
        sectors.append({**sector, "present_nodes": present, "invalidated_nodes": invalidated, "coverage": status})
    def status_for(ids: list[str]) -> dict:
        present = [x for x in ids if x in nodes]
        missing = [x for x in ids if x not in nodes]
        evidence = [x for x in present if state["axes"].get(x, {}).get("science") in {"CANDIDATE_EVIDENCE", "CANDIDATE_EVIDENCE_NOT_ISSUED"}]
        invalidated = [x for x in present if str(state["axes"].get(x, {}).get("consumer", "")).startswith("INVALIDATED")]
        return {
            "required_nodes": ids,
            "present": present,
            "missing": missing,
            "candidate_evidence": evidence,
            "invalidated": invalidated,
            "status": "BLOCKED" if invalidated else ("CANDIDATE_EVIDENCE" if evidence else "SOURCE_ONLY_OR_MISSING"),
        }
    product_coverage = {
        "user": status_for(["S7", "S8", "S11", "S15"]),
        "ux": status_for(["S11", "S15", "CP-A5-R2"]),
        "safety": status_for(["S14", "C9C12-R2", "E08"]),
        "economics": status_for(["S13"]),
        "alpha": status_for(["S15", "A5", "CP-A5-R2"]),
        "science": status_for(["N10", "N11", "N12"]),
        "native_person": status_for(["C4", "C11", "C12", "A5"]),
    }
    return {
        "sectors": sectors,
        "product_coverage": product_coverage,
        "authority": "CANDIDATE_NOT_ADOPTED",
        "science": "HOLD_NOT_ISSUED",
        "human": "NOT_PROVEN",
        "engineering": "CANDIDATE_ONLY",
    }


def _recompute(state: dict) -> None:
    state["sectors"] = _sectors(state["nodes"], [m["id"] for m in state.get("missing_functions", [])])
    state["gaps"] = compute_gaps(state)
    state["work_now"] = compute_work_now(state)
    state["coverage"] = compute_coverage(state)
    state["blocked_views"] = {
        "L0_PERSON": blocked_chain(state, "L0_PERSON"),
        "A5": blocked_chain(state, "A5"),
        "C12": blocked_chain(state, "C12"),
    }
    state["readiness"] = {
        "engineering": "CANDIDATE_ONLY",
        "science": "HOLD_NOT_ISSUED",
        "authority": "HOLD_NOT_ADOPTED",
        "human": "NOT_PROVEN",
        "central_invariants": {
            "history_preserved": bool(state.get("history")),
            "source_manifest_rows": len(state.get("source_manifest", {}).get("rows", [])),
            "evidence_import_count": len(state.get("evidence_imports", {})),
            "gaps_derived": len(state.get("gaps", [])),
        },
    }
    state["state_digest"] = _digest({k: v for k, v in state.items() if k != "state_digest"})


def _verify_git_object(source: dict) -> tuple[bool, str]:
    commit = str(source.get("commit") or "")
    path = str(source.get("path") or "")
    object_id = str(source.get("blob") or source.get("object_id") or "")
    expected_type = str(source.get("object_type") or "blob")
    if not commit or not path:
        return False, "SOURCE_COMMIT_OR_PATH_MISSING"
    actual_type = _git(["cat-file", "-t", f"{commit}:{path}"])
    if not actual_type:
        return False, "GIT_OBJECT_MISSING"
    actual_id = _git(["rev-parse", f"{commit}:{path}"])
    if not actual_id:
        return False, "GIT_OBJECT_ID_UNRESOLVED"
    if actual_type != expected_type:
        return False, f"OBJECT_TYPE_MISMATCH:{actual_type}!={expected_type}"
    if object_id and actual_id != object_id:
        return False, f"OBJECT_ID_MISMATCH:{actual_id}!={object_id}"
    return True, actual_id


def _normalized_source(row: dict | None) -> dict:
    if not row:
        return {}
    if row.get("evidence_source"):
        return row["evidence_source"]
    return {
        "commit": row.get("commit"),
        "path": row.get("path"),
        "blob": row.get("blob") or row.get("object_id"),
        "object_type": row.get("object_type", "blob"),
        "source_timestamp": row.get("source_timestamp"),
    }


def _node_source(state: dict, node_id: str) -> dict:
    row = next((r for r in state["source_manifest"]["rows"] if r["id"] == node_id), None)
    if row:
        return _normalized_source(row)
    node = _node_map(state).get(node_id, {})
    return node.get("source") or {}


def _evidence_digest(evidence: dict) -> str:
    return _digest(evidence)


def _require_evidence(evidence: Any) -> dict:
    if not isinstance(evidence, dict):
        raise ValueError("TYPED_EVIDENCE_REQUIRED")
    kind = str(evidence.get("kind") or "")
    if kind not in EVIDENCE_KINDS:
        raise ValueError("UNKNOWN_EVIDENCE_KIND")
    return evidence


def _authority_request(evidence: dict, node_id: str, state: dict) -> dict:
    if evidence["kind"] != "OWNER_GRANT":
        raise ValueError("OWNER_GRANT_EVIDENCE_REQUIRED")
    owner_slot = str(evidence.get("owner_slot") or "")
    if owner_slot not in AUTHORITY_OWNER_SLOTS:
        raise ValueError("WRONG_AUTHORITY_OWNER")
    scope = evidence.get("scope") or []
    if isinstance(scope, str):
        scope = [scope]
    if "*" not in scope and node_id not in scope:
        raise ValueError("EVIDENCE_SCOPE_MISMATCH")
    source = evidence.get("source") or {}
    ok, reason = _verify_git_object(source)
    if not ok:
        raise ValueError("FORGED_OR_MISSING_GIT_SOURCE:" + reason)
    preimage = str(evidence.get("preimage") or "")
    if preimage:
        expected = _digest(_node_source(state, node_id))
        if preimage != expected:
            raise ValueError("PREIMAGE_MISMATCH")
    return {
        "status": "PENDING_MANUAL_VERIFICATION",
        "authority_state": "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION",
        "manual_verification_required": True,
        "reason": "local worker cannot verify an owner signature; owner evidence is preserved unadopted",
    }


def _human_request(evidence: dict) -> dict:
    if evidence["kind"] != "HUMAN_PARTICIPANT":
        raise ValueError("HUMAN_PARTICIPANT_EVIDENCE_REQUIRED")
    for key in ("participant_record_hash", "consent_record", "protocol", "reviewer_role"):
        if not str(evidence.get(key) or "").strip():
            raise ValueError("HUMAN_PARTICIPANT_FIELD_MISSING:" + key)
    if not re.fullmatch(r"[0-9a-f]{64}", str(evidence.get("participant_record_hash") or "")):
        raise ValueError("HUMAN_PARTICIPANT_HASH_INVALID")
    return {
        "status": "SIMULATED_NOT_ADOPTED",
        "human_state": "CANDIDATE_LAB_DEMO_NOT_HUMAN_A5",
        "manual_verification_required": True,
        "reason": "no external participant verification in this environment; never promote to PROVEN",
    }


def _science_request(evidence: dict) -> dict:
    if evidence["kind"] != "ORIGINAL_SCIENCE_ISSUANCE":
        raise ValueError("ORIGINAL_SCIENCE_ISSUANCE_EVIDENCE_REQUIRED")
    for key in ("issuer_slot", "rule_id", "rule_text", "preimage"):
        if not str(evidence.get(key) or "").strip():
            raise ValueError("ORIGINAL_SCIENCE_FIELD_MISSING:" + key)
    return {
        "status": "PENDING_MANUAL_VERIFICATION",
        "science_state": "HOLD_MANUAL_VERIFICATION",
        "manual_verification_required": True,
        "reason": "no local original CAN/ADP/SCI05 verifier; rule is held",
    }


def _is_negative(dimension: str, to: str) -> bool:
    return (
        (dimension == "source_recovery" and to in NEGATIVE_SOURCE)
        or (dimension == "review" and to in NEGATIVE_REVIEW)
        or (dimension == "engineering" and to in NEGATIVE_ENGINEERING)
        or (dimension == "science" and to in NEGATIVE_SCIENCE)
        or (dimension == "authority" and to in NEGATIVE_AUTHORITY)
    )


def _invalidate_required_dependents(state: dict, node_id: str) -> list[str]:
    invalidated = []
    seen = {node_id}
    q = deque([node_id])
    while q:
        current = q.popleft()
        for edge in _required_outgoing(state, current):
            target = edge["to"]
            if target in seen or target == "PYAT_EXTERNAL_BOUNDARY":
                continue
            seen.add(target)
            axis = state["axes"].setdefault(target, _empty_axes_for_node({"id": target}))
            if not str(axis.get("consumer", "")).startswith("INVALIDATED"):
                axis["consumer"] = "INVALIDATED_BY_UPSTREAM"
                invalidated.append(target)
            q.append(target)
    return sorted(invalidated)


def _apply_transition(state: dict, fixture: dict) -> dict:
    node_id = fixture.get("node_id")
    nodes = _node_map(state)
    if not node_id or node_id not in nodes:
        raise ValueError("UNKNOWN_NODE")
    if node_id == "PYAT_EXTERNAL_BOUNDARY" or str(node_id).startswith("PYAT_"):
        raise ValueError("EXTERNAL_PYAT_BOUNDARY_NOT_LOCALLY_MUTABLE")
    dimension = fixture.get("dimension")
    if dimension not in ALLOWED_TRANSITIONS:
        raise ValueError("UNKNOWN_DIMENSION")
    requested_to = str(fixture.get("to") or "")
    if not requested_to:
        raise ValueError("INVALID_TARGET_STATE")
    evidence = fixture.get("evidence")
    if evidence is None:
        evidence = {"owner_evidence": fixture.get("owner_evidence"), "reviewer_evidence": fixture.get("reviewer_evidence")}
    evidence = _require_evidence(evidence)
    status = "APPLIED_CANDIDATE_ONLY"
    target = requested_to
    hold = None
    if dimension == "authority" and requested_to in {"OWNER_ADOPTED", "NATIVE_ISSUED"}:
        hold = _authority_request(evidence, node_id, state)
        target = "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION"
        status = hold["status"]
    elif dimension == "human" and requested_to in {"PROVEN", "HUMAN_A5", "A5_GREEN"}:
        hold = _human_request(evidence)
        target = "CANDIDATE_LAB_DEMO_NOT_HUMAN_A5"
        status = hold["status"]
    elif dimension == "science" and requested_to in {"ORIGINAL_ISSUED", "NATIVE_ISSUED", "ISSUED"}:
        hold = _science_request(evidence)
        target = "HOLD_MANUAL_VERIFICATION"
        status = hold["status"]
    elif requested_to not in ALLOWED_TRANSITIONS[dimension]:
        raise ValueError("TARGET_STATE_NOT_ALLOWED_ON_DIMENSION")
    if evidence["kind"] in {"SOURCE_RECORD", "SOURCEFREE_REVIEW", "OWNER_GRANT", "ORIGINAL_SCIENCE_ISSUANCE"}:
        source = evidence.get("source")
        if not isinstance(source, dict):
            raise ValueError("TYPED_SOURCE_REQUIRED")
        ok, reason = _verify_git_object(source)
        if not ok:
            raise ValueError("FORGED_OR_MISSING_GIT_SOURCE:" + reason)
        preimage = evidence.get("preimage")
        if preimage and preimage != _digest(_node_source(state, node_id)):
            raise ValueError("PREIMAGE_MISMATCH")
    if evidence["kind"] == "SOURCEFREE_REVIEW":
        reviewed_sha = str(evidence.get("reviewed_sha") or "")
        if not reviewed_sha or _git(["cat-file", "-t", reviewed_sha]) != "commit":
            raise ValueError("REVIEWED_SHA_NOT_FOUND")
        if str(evidence.get("review_status") or "").upper() == "FAIL":
            target = "REVIEW_FAILED"
            status = "APPLIED_CANDIDATE_ONLY"
    if evidence["kind"] == "SYNTHETIC_DEMO":
        status = "SIMULATED_NOT_ADOPTED"
        if dimension in {"authority", "human", "science"} and requested_to in {"PROVEN", "OWNER_ADOPTED", "NATIVE_ISSUED", "ORIGINAL_ISSUED"}:
            raise ValueError("SYNTHETIC_DEMO_CANNOT_PROMOTE_AUTHORITY_SCIENCE_OR_HUMAN")
    old = state["axes"][node_id].get(dimension)
    state["axes"][node_id][dimension] = target
    if dimension == "authority" and hold:
        state["axes"][node_id]["authority"] = "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION"
    if dimension == "human" and hold:
        state["axes"][node_id]["human"] = "CANDIDATE_LAB_DEMO_NOT_HUMAN_A5"
    if dimension == "science" and hold:
        state["axes"][node_id]["science"] = "HOLD_MANUAL_VERIFICATION"
    negative = _is_negative(dimension, target) or (dimension == "review" and target == "REVIEW_FAILED")
    invalidated: list[str] = []
    affected: list[str] = []
    restored: list[str] = []
    if negative:
        prior_consumer = state["axes"][node_id].get("consumer")
        if dimension == "source_recovery":
            state["axes"][node_id]["consumer"] = "INVALIDATED_BY_UPSTREAM"
        invalidated = _invalidate_required_dependents(state, node_id)
        entry = state.setdefault("invalidation_index", {}).get(node_id)
        if not isinstance(entry, dict):
            entry = {"dependents": list(entry or []), "self_consumer": prior_consumer if dimension == "source_recovery" else None}
        entry.setdefault("dependents", [])
        entry.setdefault("self_consumer", prior_consumer if dimension == "source_recovery" else None)
        entry["dependents"].extend(x for x in invalidated if x not in entry["dependents"])
        state["invalidation_index"][node_id] = entry
    else:
        affected = sorted({
            e["to"] for e in state["edges"]
            if e["from"] == node_id and not e.get("hypothetical")
        })
        if dimension in {"source_recovery", "review"} and evidence["kind"] in {"SOURCE_RECORD", "SOURCEFREE_REVIEW"}:
            entry = state.setdefault("invalidation_index", {}).pop(node_id, {})
            if isinstance(entry, list):
                entry = {"dependents": entry, "self_consumer": None}
            self_axis = state["axes"].get(node_id)
            if self_axis and str(self_axis.get("consumer", "")).startswith("INVALIDATED") and entry.get("self_consumer"):
                self_axis["consumer"] = entry["self_consumer"]
            for dependent in entry.get("dependents", []):
                axis = state["axes"].get(dependent)
                if axis and str(axis.get("consumer", "")).startswith("INVALIDATED"):
                    axis["consumer"] = "CANDIDATE_READY"
                    restored.append(dependent)
    digest = _evidence_digest(evidence)
    history_id = "H%04d" % (len(state["history"]) + 1)
    record = {
        "history_id": history_id,
        "kind": "AUTHORIZED_TRANSITION" if status.startswith("APPLIED") else "TRANSITION_HOLD",
        "node_id": node_id,
        "dimension": dimension,
        "from": old,
        "to": target,
        "requested_to": requested_to,
        "status": status,
        "evidence_digest": digest,
        "evidence_kind": evidence["kind"],
        "invalidated": invalidated,
        "affected": affected,
        "restored": restored,
        "pyat_boundary_touched": False,
        "authority_hold": hold,
        "source_cut": state.get("source_snapshot", {}).get("read_at", "UNKNOWN"),
    }
    state["history"].append(record)
    if hold:
        state.setdefault("authority_holds", []).append({
            "history_id": history_id,
            "node_id": node_id,
            "dimension": dimension,
            "requested_to": requested_to,
            "status": hold["status"],
            "reason": hold["reason"],
            "evidence_digest": digest,
            "manual_verification_required": True,
        })
    state["freshness"]["generated_at"] = _utc_now()
    _recompute(state)
    return {
        "status": status,
        "history_id": history_id,
        "node_id": node_id,
        "dimension": dimension,
        "from": old,
        "to": target,
        "requested_to": requested_to,
        "invalidated": invalidated,
        "affected": affected,
        "restored": restored,
        "authority_hold": hold,
        "pyat_boundary_touched": False,
    }


def _legacy_record_source(record: dict, r3_rows: dict[str, dict]) -> dict:
    row = r3_rows.get(record.get("id"))
    if not row:
        return {"status": "HOLD_MISSING_SOURCE", "id": record.get("id")}
    es = row.get("evidence_source") or {}
    return {
        "repo": row.get("repository", "maidiu/rawlsing"),
        "commit": es.get("commit"),
        "path": es.get("path"),
        "git_blob": es.get("blob") or es.get("object_id"),
        "object_id": es.get("object_id") or es.get("blob"),
        "object_type": es.get("object_type", "blob"),
        "source_timestamp": es.get("source_timestamp"),
        "grade": "R3_KEYED_EXACT_SOURCE",
    }


def ingest_oscience(
    state: dict,
    patch: dict | None = None,
    *,
    r3_registry: dict | None = None,
    legacy_source: dict | None = None,
    backward: dict | None = None,
    patch_digest: str | None = None,
    source_commit: str = OSCIENCE_CUT,
) -> dict:
    """Import the complete O-SCIENCE patch as candidate evidence into this graph."""
    patch = patch or _load(OSCIENCE_PATCH)
    registry = r3_registry or _load(SEED_REGISTRY)
    legacy = legacy_source or _load(OSCIENCE_102)
    backward = backward or _load(OSCIENCE_BACKWARD)
    digest = patch_digest or _digest(patch)
    if digest in state.get("evidence_imports", {}):
        state["history"].append({
            "history_id": "H%04d" % (len(state["history"]) + 1),
            "kind": "DUPLICATE_IMPORT_NOOP",
            "evidence_digest": digest,
            "read_at": _utc_now(),
        })
        _recompute(state)
        return {
            "status": "DUPLICATE_IMPORT_IDEMPOTENT",
            "evidence_digest": digest,
            "counts": state["evidence_imports"][digest]["counts"],
            "nodes": len(state["nodes"]),
            "edges": len(state["edges"]),
        }
    nodes = _node_map(state)
    r3_rows = _source_rows(registry)
    upserts = patch["workstream_evidence_upserts"]
    new_nodes = patch["new_evidence_nodes"]
    typed_edges = patch["typed_edges"]
    if len(upserts) != 17 or len(new_nodes) != 14 or len(typed_edges) != 226:
        raise ValueError("OSCIENCE_PATCH_COUNT_MISMATCH")
    conflicts = []
    workstreams = {w["id"]: w for w in state.get("workstreams", [])}
    for upsert in upserts:
        sid = upsert["target_node_id"]
        if sid not in nodes:
            raise ValueError("UNKNOWN_WORKSTREAM_TARGET:" + sid)
        row = r3_rows.get(sid, {})
        preserve = upsert.get("preserve_original") or {}
        for key in ("title", "question", "output"):
            if preserve.get(key) != row.get(key):
                conflicts.append({"node": sid, "field": key, "patch": preserve.get(key), "source_exact": row.get(key)})
        workstreams.setdefault(sid, {"id": sid})
        workstreams[sid].update({
            "title": row.get("title"),
            "question": row.get("question"),
            "output": row.get("output"),
            "source": row.get("evidence_source"),
            "candidate_evidence": {
                "domains": upsert.get("domains", []),
                "alternatives": upsert.get("alternatives", []),
                "consumer": upsert.get("consumer"),
                "falsifier": upsert.get("falsifier"),
                "owner": upsert.get("owner"),
                "stage": upsert.get("stage", "CANDIDATE_EVIDENCE"),
                "review": upsert.get("review", "INDEPENDENT_SOROK_HQ_PENDING"),
                "source": upsert.get("source"),
                "grade": "CANDIDATE_EVIDENCE_NOT_ISSUED",
                "evidence_digest": digest,
            },
            "source_grade": "SOURCE_EXACT",
            "science_grade": "CANDIDATE_EVIDENCE_NOT_ISSUED",
            "consumer_state": upsert.get("consumer") or row.get("actual_consumer_state"),
        })
        state.setdefault("node_evidence", {}).setdefault(sid, []).append({
            "kind": "OSCIENCE_WORKSTREAM_EVIDENCE",
            "evidence_digest": digest,
            "source": upsert.get("source"),
            "grade": "CANDIDATE_EVIDENCE_NOT_ISSUED",
            "review": upsert.get("review"),
        })
        axis = state["axes"].setdefault(sid, _empty_axes_for_node(nodes[sid]))
        axis["source_recovery"] = "SOURCE_EXACT"
        axis["science"] = "CANDIDATE_EVIDENCE_NOT_ISSUED"
        axis["review"] = "UNREVIEWED_CANDIDATE_EVIDENCE"
        axis["operational"] = "CANDIDATE_EVIDENCE"
    backward_rows = backward.get("rows", [])
    if len(backward_rows) != 14:
        raise ValueError("BACKWARD_CONSUMER_ROW_COUNT_MISMATCH")
    for index, node in enumerate(new_nodes):
        nid = node["id"]
        if nid in nodes:
            raise ValueError("DUPLICATE_EVIDENCE_NODE:" + nid)
        row = backward_rows[index]
        node_out = copy.deepcopy(node)
        node_out.update({
            "layer": "L2",
            "kind": "MISSING_FUNCTION_CANDIDATE",
            "title": row.get("terminal_or_mid_capability") or nid,
            "status": "CANDIDATE_NOT_NATIVE",
            "source": node.get("source"),
            "backward_consumer_row": row,
            "owner": row.get("required_owner") or node.get("owner"),
            "hq_judgment_required": True,
        })
        state["nodes"].append(node_out)
        nodes[nid] = node_out
        state["axes"][nid] = {
            "source_recovery": "SOURCE_EXACT",
            "science": "CANDIDATE_EVIDENCE_NOT_ISSUED",
            "engineering": "MISSING_FUNCTION",
            "authority": "NOT_ADOPTED",
            "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
            "consumer": "NONE_NATIVE",
            "human": "NOT_PROVEN",
            "operational": "CANDIDATE_EVIDENCE",
        }
        state.setdefault("missing_functions", []).append({
            **row,
            "id": nid,
            "source": node.get("source"),
            "evidence_digest": digest,
            "node_status": "CANDIDATE_NOT_NATIVE",
        })
        state.setdefault("node_evidence", {}).setdefault(nid, []).append({
            "kind": "OSCIENCE_MISSING_FUNCTION",
            "evidence_digest": digest,
            "source": node.get("source"),
            "grade": "CANDIDATE_EVIDENCE_NOT_ISSUED",
        })
    edge_ids = {e["edge_id"] for e in state["edges"]}
    added_edges = 0
    for raw in typed_edges:
        if raw["from"] not in nodes or raw["to"] not in nodes:
            raise ValueError(f"EDGE_ENDPOINT_UNKNOWN:{raw['from']}->{raw['to']}")
        edge = _classify_edge(raw)
        if edge["edge_id"] in edge_ids:
            conflicts.append({"edge_id": edge["edge_id"], "kind": "DUPLICATE_EDGE"})
            continue
        state["edges"].append(edge)
        edge_ids.add(edge["edge_id"])
        added_edges += 1
        pair = [e for e in state["edges"] if e["from"] == edge["from"] and e["to"] == edge["to"] and e["relation"] != edge["relation"]]
        if pair:
            conflicts.append({"from": edge["from"], "to": edge["to"], "kind": "MULTIPLE_RELATIONS", "relations": [edge["relation"]] + [e["relation"] for e in pair]})
    grounded = 0
    missing_sources = []
    records = []
    for record in legacy.get("legacy_definition_records", []):
        item = copy.deepcopy(record)
        source = _legacy_record_source(item, r3_rows)
        item["source"] = source
        item["source_grounding"] = "R3_KEYED_EXACT" if source.get("commit") and source.get("path") else "HOLD_MISSING_SOURCE"
        if item["source_grounding"] == "R3_KEYED_EXACT":
            grounded += 1
        else:
            missing_sources.append(item.get("id"))
        records.append(item)
    if len(records) != 102:
        raise ValueError("LEGACY_RECORD_COUNT_MISMATCH")
    state["legacy_records"] = records
    state["workstreams"] = [workstreams[k] for k in sorted(workstreams, key=lambda x: int(x[1:]) if x[1:].isdigit() else 999)]
    state["evidence_imports"][digest] = {
        "schema": "SOROK_OSCIENCE_IMPORT@1",
        "source_commit": source_commit,
        "patch_schema": patch.get("schema"),
        "imported_at": _utc_now(),
        "review_status": "UNREVIEWED_CANDIDATE_EVIDENCE",
        "counts": {
            "workstream_upserts": len(upserts),
            "legacy_records": len(records),
            "legacy_source_grounded": grounded,
            "new_nodes": len(new_nodes),
            "typed_edges": added_edges,
        },
        "conflicts": conflicts,
        "missing_sources": missing_sources,
    }
    state["evidence_review_status"] = "UNREVIEWED_CANDIDATE_EVIDENCE"
    state["history"].append({
        "history_id": "H%04d" % (len(state["history"]) + 1),
        "kind": "OSCIENCE_PATCH_IMPORTED",
        "evidence_digest": digest,
        "source_commit": source_commit,
        "counts": state["evidence_imports"][digest]["counts"],
        "conflicts": conflicts,
        "read_at": _utc_now(),
    })
    _recompute(state)
    return {
        "status": "CANDIDATE_EVIDENCE_IMPORTED",
        "evidence_digest": digest,
        "counts": state["evidence_imports"][digest]["counts"],
        "nodes": len(state["nodes"]),
        "edges": len(state["edges"]),
        "conflicts": conflicts,
        "legacy_source_grounded": grounded,
        "missing_sources": missing_sources,
    }


def intake_candidate(state: dict, fixture: dict) -> dict:
    """Ingest a returned fixture into the same graph; never auto-promote."""
    if fixture.get("schema", "").startswith("SOROK_PROGRAMMA_O_SCIENCE") or fixture.get("kind") == "OSCIENCE_PATCH":
        return ingest_oscience(state, fixture)
    item = {
        "history_id": "H%04d" % (len(state["history"]) + 1),
        "kind": "INTAKE_RETURN_CANDIDATE",
        "return_id": fixture.get("id", "UNKNOWN"),
        "source": fixture.get("branch", ""),
        "sha": fixture.get("sha", ""),
        "status": "CANDIDATE_NOT_PROMOTED",
        "claimed_tests": fixture.get("tests", {}),
        "evidence": fixture.get("evidence", {}),
        "read_at": _utc_now(),
    }
    state["history"].append(item)
    if fixture.get("new_requirement"):
        rid = fixture["new_requirement"]
        gap = {
            "id": "GAP_" + rid,
            "domain": "DISCOVERED_REQUISITE",
            "node": rid,
            "class": "UNREPRESENTED_REQUIREMENT",
            "status": "UNREPRESENTED_REQUIREMENT",
            "owner": "UNKNOWN",
            "next": "Assign source, competent owner and actual consumer.",
            "consequence": "Visible unrepresented requirement.",
            "blockers": [],
            "impact": {"downstream_required_count": 0, "affected_l0": [], "affected_sectors": []},
            "parallel_group": "DISCOVERED_REQUISITE",
            "hq_judgment_required": True,
        }
        state.setdefault("intake_gaps", []).append(gap)
        item["new_gap"] = gap["id"]
    for update in fixture.get("node_updates", []):
        nid = update.get("id")
        if not nid:
            continue
        if nid not in _node_map(state):
            state["nodes"].append({
                "id": nid,
                "layer": update.get("layer", "L2"),
                "kind": update.get("kind", "DISCOVERED_REQUIREMENT"),
                "title": update.get("title", nid),
                "status": "CANDIDATE_EVIDENCE",
                "source": update.get("source"),
                "hq_judgment_required": True,
            })
            state["axes"][nid] = _empty_axes_for_node({"id": nid})
        state["axes"][nid].update({"operational": "CANDIDATE_EVIDENCE"})
        state.setdefault("node_evidence", {}).setdefault(nid, []).append({
            "kind": "RETURN_CANDIDATE_EVIDENCE",
            "evidence": update.get("evidence"),
            "history_id": item["history_id"],
        })
    for edge in fixture.get("edges", []):
        if edge.get("from") not in _node_map(state) or edge.get("to") not in _node_map(state):
            raise ValueError("INTAKE_EDGE_ENDPOINT_UNKNOWN")
        candidate = _classify_edge(edge)
        if candidate["edge_id"] not in {e["edge_id"] for e in state["edges"]}:
            state["edges"].append(candidate)
    _recompute(state)
    return item


def _overview(state: dict) -> dict:
    return {
        "schema": state["schema"],
        "version": state["version"],
        "source_snapshot": state.get("source_snapshot"),
        "source_cut_stale": state.get("source_cut_stale", False),
        "version_vector": state.get("version_vector"),
        "counts": {
            "nodes": len(state["nodes"]),
            "edges": len(state["edges"]),
            "sources": state["source_count"],
            "sectors": len(state["sectors"]),
            "gaps": len(state["gaps"]),
            "workstreams": len(state.get("workstreams", [])),
            "legacy_records": len(state.get("legacy_records", [])),
            "missing_functions": len(state.get("missing_functions", [])),
            "evidence_imports": len(state.get("evidence_imports", {})),
            "workers": len(state["workers"]),
        },
        "readiness": state.get("readiness"),
        "coverage": state.get("coverage"),
        "pyat_boundary": state["pyat_boundary"],
        "status": "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED",
    }


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=STATE)
    parser.add_argument("--snapshot", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh")
    sub.add_parser("overview")
    for name in ("source", "consumer", "alternatives", "history", "critical-path", "blocked-chain"):
        p = sub.add_parser(name); p.add_argument("id")
    z = sub.add_parser("zoom"); z.add_argument("id"); z.add_argument("--depth", type=int, default=1)
    g = sub.add_parser("gaps"); g.add_argument("--domain", default="")
    sub.add_parser("work-now")
    sub.add_parser("workers")
    sub.add_parser("coverage")
    sub.add_parser("export")
    i = sub.add_parser("intake-return"); i.add_argument("file", type=Path)
    o = sub.add_parser("ingest-oscience"); o.add_argument("file", type=Path, nargs="?")
    a = sub.add_parser("apply-authorized-transition"); a.add_argument("file", type=Path)
    args = parser.parse_args(argv)
    state_path = args.state
    snapshot_path = args.snapshot
    if args.command == "refresh":
        existing = _load_state(state_path) if state_path.exists() else None
        state = refresh_state(existing, observe_source_cut())
        _save(state, state_path, snapshot_path)
        _print(_overview(state))
        return 0
    state = _load_state(state_path)
    if args.command == "overview":
        _print(_overview(state))
    elif args.command == "zoom":
        if args.id not in _node_map(state):
            _print({"error": "UNKNOWN_ID"})
            return 1
        nodes, edges = _neighbors(state, args.id, args.depth)
        _print({"root": args.id, "depth": args.depth, "nodes": nodes, "edges": edges})
    elif args.command == "gaps":
        _print([g for g in state["gaps"] if not args.domain or g["domain"] == args.domain])
    elif args.command == "work-now":
        _print(state["work_now"])
    elif args.command == "blocked-chain":
        _print(blocked_chain(state, args.id))
    elif args.command == "critical-path":
        _print({
            "goal": args.id,
            "kind": "LEGACY_DAG_SHORTEST_PATH_ILLUSTRATION_NOT_CRITICAL",
            "path": _critical_path(state, args.id),
            "warning": "Use blocked-chain for typed required blockers; this path is not a scientific priority.",
        })
    elif args.command == "source":
        row = next((x for x in state["source_manifest"]["rows"] if x["id"] == args.id), None)
        _print(row or {"error": "UNKNOWN_SOURCE"})
    elif args.command == "consumer":
        out = [e for e in state["edges"] if e["from"] == args.id and (e["to"].startswith("L4") or "consumer" in e.get("relation", ""))]
        _print({"node": args.id, "consumer_edges": out, "axes": state["axes"].get(args.id)})
    elif args.command == "alternatives":
        row = next((x for x in state["source_manifest"]["rows"] if x["id"] == args.id), None)
        ws = next((x for x in state.get("workstreams", []) if x["id"] == args.id), None)
        _print({"id": args.id, "row": (row or {}).get("unresolved_alternatives", []), "workstream": ws})
    elif args.command == "workers":
        _print({"workers": state["workers"], "source_snapshot": state.get("source_snapshot"), "caution": "Git branch does not prove running process; missing local process is not owner absence."})
    elif args.command == "coverage":
        _print(state["coverage"])
    elif args.command == "history":
        _print([h for h in state["history"] if h.get("history_id") == args.id or h.get("node_id") == args.id])
    elif args.command == "export":
        _print(state)
    elif args.command == "intake-return":
        fixture = _load(args.file)
        if fixture.get("schema", "").startswith("SOROK_PROGRAMMA_O_SCIENCE"):
            result = ingest_oscience(state, fixture)
        else:
            result = intake_candidate(state, fixture)
        _save(state, state_path, snapshot_path)
        _print(result)
    elif args.command == "ingest-oscience":
        patch = _load(args.file or OSCIENCE_PATCH)
        result = ingest_oscience(state, patch)
        _save(state, state_path, snapshot_path)
        _print(result)
    elif args.command == "apply-authorized-transition":
        fixture = _load(args.file)
        try:
            result = _apply_transition(state, fixture)
        except ValueError as error:
            _print({"status": "REFUSED", "reason": str(error)})
            return 1
        _save(state, state_path, snapshot_path)
        _print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
