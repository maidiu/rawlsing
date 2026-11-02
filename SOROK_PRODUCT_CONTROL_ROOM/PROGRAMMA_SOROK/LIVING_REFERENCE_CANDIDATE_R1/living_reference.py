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
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import deque
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Any

import evidence_store
import programma_p1_seed as p1seed

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
JOURNAL = ROOT / "evidence" / "journal.jsonl"
QUARANTINE = ROOT / "quarantine" / "historical_demo_contamination"
P1_SEED = ROOT / "programma_p1_seed.py"

BASE_NODE_COUNT = 198 + len(p1seed.NODES)
BASE_EDGE_COUNT = 423 + len(p1seed.EDGES)
IMPORTED_NODE_COUNT = BASE_NODE_COUNT + 14
IMPORTED_EDGE_COUNT = BASE_EDGE_COUNT + 226

SCHEMA = "SOROK_PROGRAMMA_LIVING_REFERENCE_STATE@3"
VERSION = "R3"
ENGINEERING_BASELINE = "a89e5ccbe67400168aaea8367f7aa00ca0de7625"
OLIVE_SOURCE_SHA = "67f667421fc90b22aad95cfc253a16feabc92348"
STARTUP_SHA = ENGINEERING_BASELINE
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

NEGATIVE_SOURCE = {
    "SOURCE_NOT_FOUND", "SOURCE_WITHDRAWN", "MISSING", "SOURCE_INVALID",
    "AUTHORIZED_EXCLUSION", "UNREAD", "WITNESS_MISMATCH", "SOURCE_REF_INVALID",
}
NEGATIVE_REVIEW = {"REVIEW_FAILED", "SEALED_NEGATIVE"}
NEGATIVE_ENGINEERING = {"FAILED", "REGRESSED"}
NEGATIVE_SCIENCE = {"REFUSED", "NATIVE_ISSUED_REVOKED"}
NEGATIVE_AUTHORITY = {"REVOKED"}
NEGATIVE_ALL = NEGATIVE_SOURCE | NEGATIVE_REVIEW | NEGATIVE_ENGINEERING | NEGATIVE_SCIENCE | NEGATIVE_AUTHORITY

ALLOWED_TRANSITIONS = {
    "source_recovery": {"SOURCE_VERIFIED", "SOURCE_NOT_FOUND", "SOURCE_WITHDRAWN", "MISSING", "CANDIDATE_EVIDENCE", "SOURCE_INVALID", "AUTHORIZED_EXCLUSION"},
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
    "ACCEPTANCE_RECORD",
    "SOURCE_WITHDRAWAL",
    "AUTHORIZED_EXCLUSION",
}

PROMOTION_TARGETS = {
    "review": {"REVIEW_PASSED_SCOPED", "SEALED"},
    "engineering": {"INDEPENDENT_ACCEPT_SCOPED", "ACTUAL"},
    "authority": {"OWNER_ADOPTED", "NATIVE_ISSUED"},
    "science": {"ORIGINAL_ISSUED", "NATIVE_ISSUED", "ISSUED"},
    "human": {"PROVEN", "HUMAN_A5", "A5_GREEN"},
    "consumer": {"ACTUAL"},
}

EXPLICIT_DEPENDENCIES = {
    "REQUIRED_CAUSAL": {"dependency_type": "REQUIRED_DEPENDENCY", "required": True, "causal": True, "hypothetical": False},
    "CONSTRAINT": {"dependency_type": "PRODUCT_OR_SCOPE_CONSTRAINT", "required": False, "causal": False, "hypothetical": False},
    "HYPOTHESIS": {"dependency_type": "HYPOTHETICAL", "required": False, "causal": False, "hypothetical": True},
    "ALTERNATIVE": {"dependency_type": "ALTERNATIVE", "required": False, "causal": False, "hypothetical": True},
    "EVIDENCE": {"dependency_type": "EPISTEMIC_EVIDENCE", "required": False, "causal": False, "hypothetical": False},
    "HISTORICAL": {"dependency_type": "HISTORICAL", "required": False, "causal": False, "hypothetical": False},
    "MISSING_EDGE": {"dependency_type": "MISSING_EDGE", "required": False, "causal": False, "hypothetical": True},
    "SCOPE_ACCEPTANCE": {"dependency_type": "SCOPED_ACCEPTANCE", "required": False, "causal": False, "hypothetical": False},
    "STATUS_OBSERVATION": {"dependency_type": "OBSERVATION", "required": False, "causal": False, "hypothetical": False},
    "TEST_ONLY": {"dependency_type": "TEST_ONLY", "required": False, "causal": False, "hypothetical": False},
    "CONTRADICTS": {"dependency_type": "CONTRADICTION", "required": False, "causal": False, "hypothetical": True},
    "SUPERSEDES": {"dependency_type": "SUPERSESSION", "required": False, "causal": False, "hypothetical": False},
    "MENTION": {"dependency_type": "MENTION_ONLY", "required": False, "causal": False, "hypothetical": True},
    "NOT_EVIDENCE": {"dependency_type": "NON_EVIDENCE", "required": False, "causal": False, "hypothetical": False},
    "STALE_CROSS_CUT": {"dependency_type": "STALE_CROSS_CUT", "required": False, "causal": False, "hypothetical": False},
    "CONTINUITY": {"dependency_type": "CONTINUITY_ONLY", "required": False, "causal": False, "hypothetical": False},
}

MATURITY_STAGES = ("I", "T", "A", "E", "C", "V")
MATURITY_NEGATIVE = {"MISSING", "UNKNOWN", "UNREAD", "REVIEWED_NEGATIVE", "SUPERSEDED", "NOT_REQUIRED_WITH_REASON"}


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
                "olive": {"ref": "origin/agent/sorok-programma-living-reference-s2-sourcegraded-operating-map-r1-20261031", "sha": OLIVE_SOURCE_SHA, "committed_at": "UNKNOWN"},
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
    explicit = str(edge.get("dependency") or "").upper()
    if explicit in EXPLICIT_DEPENDENCIES:
        result = copy.deepcopy(edge)
        result.setdefault("from", edge.get("from"))
        result.setdefault("to", edge.get("to"))
        result["relation"] = relation
        result.update(EXPLICIT_DEPENDENCIES[explicit])
        result.setdefault("grade", edge.get("grade") or ("SOURCE_DEFINED_REQUIREMENT" if result["required"] else "TYPED_RELATION"))
        result.setdefault("source", {})
        result["edge_id"] = "EDGE_" + _digest({
            "from": result["from"],
            "to": result["to"],
            "relation": relation,
            "source": result.get("source", {}),
            "dependency": explicit,
        })[:16]
        return result
    hypothetical = any(token in low for token in ("candidate", "hypothesis", "conceptual", "index_link", "index_containment", "navigation"))
    index_like = any(token in low for token in (
        "historical_exploratory", "historical_workstream", "s0_s16", "readback", "crosswalk",
        "organ_contains", "backward_person_source_path", "index_containment",
        "mention", "association", "source_location", "located_in", "alternative",
    ))
    causal = False
    required = False
    dependency_type = "STRUCTURAL_OR_INDEX"
    if index_like:
        dependency_type = "INDEX_OR_GOVERNANCE"
    else:
        if any(token in low for token in ("requires", "require", "depends_on", "depends", "input_to", "feeds", "produces", "owner_output")):
            dependency_type = "REQUIRED_DEPENDENCY"
            required = True
            causal = True
        if any(token in low for token in ("named_first_consumer", "first_consumed_by", "consumer_required", "required_consumer")):
            dependency_type = "CONSUMER_DEPENDENCY"
            required = True
            causal = True
        if any(token in low for token in ("governs", "blocks_named_edge", "constrains")):
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
        {"id": "O_LIVE_R1", "branch": "agent/sorok-programma-living-reference-s2-sourcegraded-operating-map-r1-20261031", "sha": OLIVE_SOURCE_SHA, "status": "SEALED_RETURNED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "O_SCIENCE_R1", "branch": "research/sorok-programma-o-science-product-requisite-coverage-r1-20261031", "sha": OSCIENCE_CUT, "status": "RETURNED_CANDIDATE_EVIDENCE", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "CP-A5-R2", "branch": "agent/sorok-cp-a5-r2-multicontext-encounter-20261030", "sha": "913765328e4fab12b150ea01421ed6b445158184", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "OpenCode/DeepSeek V4.1-Flash MAX", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "C9C12-R2", "branch": "agent/sorok-c9c12-r2-versioned-writer-reader-clock-20261030", "sha": "c78404724052496fdec8608c8b0e833c0f7c4ecc", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "B-F1CR-R2", "branch": "agent/sorok-b-f1cr-targetless-c10-20261030", "sha": "bf3273c294c704ad7c631559b9866d351bb4f103", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
        {"id": "V3CORE-R1", "branch": "agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030", "sha": "b5cb3f917402b992d7cbe933af0b378d2b37cbfd", "status": "RETURNED_SHA__AUTHOR_TESTED_UNADOPTED", "editor_model": "UNKNOWN", "reviewer": "NOT_ESTABLISHED", "cost": "UNKNOWN"},
    ]


def _merge_p1_seed(nodes: list[dict], edges: list[dict]) -> tuple[list[dict], list[dict]]:
    node_ids = {n["id"] for n in nodes}
    for node in copy.deepcopy(p1seed.NODES):
        if node["id"] in node_ids:
            continue
        node.setdefault("source_refs", [])
        nodes.append(node)
        node_ids.add(node["id"])
    edge_ids = {e["edge_id"] for e in edges}
    for raw in p1seed.EDGES:
        if raw["from"] not in node_ids or raw["to"] not in node_ids:
            raise ValueError(f"P1_EDGE_ENDPOINT_UNKNOWN:{raw['from']}->{raw['to']}")
        edge = _classify_edge(raw)
        if edge["edge_id"] in edge_ids:
            continue
        edge["source"] = edge.get("source") or {}
        edges.append(edge)
        edge_ids.add(edge["edge_id"])
    return nodes, edges


def _base_state(observed_source: dict[str, Any] | None = None) -> dict:
    registry = _load(SEED_REGISTRY)
    graph = _load(SEED_GRAPH)
    slots = _load(SEED_SLOTS)
    manifest = _filter_source_manifest(_load(SOURCE_MANIFEST))
    rows = _source_rows(registry)
    nodes, edges = _base_nodes_and_edges(graph)
    nodes, edges = _merge_p1_seed(nodes, edges)
    source_verification = {
        node["id"]: _classify_source_refs(node)
        for node in nodes if node.get("programma_p1")
    }
    for node in nodes:
        if node["id"] in source_verification:
            node["source_verification"] = copy.deepcopy(source_verification[node["id"]])
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
        elif node.get("programma_p1"):
            witness = source_verification.get(node["id"], {}).get("status", "INDEX_ONLY")
            if witness == "EXTERNAL_REPORTED_NOT_REVERIFIED":
                witness = "EXTERNAL_REPORTED"
            axes[node["id"]] = {
                "source_recovery": witness if node.get("source_refs") else "INDEX_ONLY",
                "science": "CANDIDATE_EVIDENCE_NOT_ISSUED" if node.get("kind") in {"SCIENTIFIC_ALTERNATIVE", "SCIENCE_AUTHORITY", "OPEN_COURT", "HISTORICAL_QUESTION"} else "NOT_ISSUED",
                "engineering": "SOURCE_DEFINITION_ONLY",
                "authority": "NOT_ADOPTED",
                "review": "UNREVIEWED_CANDIDATE_EVIDENCE",
                "consumer": "NONE_PROVEN_AT_PREMAIN",
                "human": "NOT_PROVEN",
                "operational": "CANDIDATE_ONLY",
            }
        else:
            axes[node["id"]] = _axes(rows.get(node["id"]), node)
    observed = observed_source or observe_source_cut()
    state = {
        "schema": SCHEMA,
        "version": VERSION,
        "build_startup": ENGINEERING_BASELINE,
        "seed_build_premain": SEED_BUILD_PREMAIN,
        "baseline_identity": {
            "engineering_baseline": ENGINEERING_BASELINE,
            "olive_source_cut": OLIVE_SOURCE_SHA,
            "genesis_claim": None,
            "genesis_claim_interpretation": "NO_GENESIS_EVENT_REPLAYED_YET",
        },
        "source_snapshot": observed,
        "source_verification": source_verification,
        "source_cut_stale": False,
        "version_vector": {
            "sorok_startup": ENGINEERING_BASELINE,
            "engineering_baseline": ENGINEERING_BASELINE,
            "olive_source": OLIVE_SOURCE_SHA,
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
        "p1_gap_records": copy.deepcopy(p1seed.GAPS),
        "quarantined_intake": [],
        "quarantine": {},
        "authority_holds": [],
        "invalidation_index": {},
        "consumer_baseline": {},
        "revision": 0,
        "journal_head": evidence_store.GENESIS,
        "axes": axes,
        "workers": _initial_workers(),
        "flights": [{"id": "SOROK_SOURCEFREE_REFERENCE", "status": "CANDIDATE_ONLY", "owner": "Sorok HQ/original owners", "note": "No new worker launched by this reference."}],
        "history": [{
            "history_id": "H0001",
            "kind": "GENESIS",
            "state": "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED",
            "source_vector": {
                "startup": ENGINEERING_BASELINE,
                "engineering_baseline": ENGINEERING_BASELINE,
                "olive_source": OLIVE_SOURCE_SHA,
                "seed_build_premain": SEED_BUILD_PREMAIN,
                "r3": R3_CUT,
            },
            "read_at": observed.get("read_at", "UNKNOWN"),
        }],
        "freshness": {"generated_at": observed.get("read_at", _utc_now()), "refresh_command": "python3 living_reference.py refresh"},
        "seed_slots": slots,
    }
    _verify_seed_acceptance_records(state)
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
    state["build_startup"] = ENGINEERING_BASELINE
    state.setdefault("version_vector", {}).update(seed.get("version_vector", {}))
    identity = dict(seed.get("baseline_identity", {}))
    identity.update({k: v for k, v in state.get("baseline_identity", {}).items() if k in {"genesis_claim", "genesis_claim_interpretation"}})
    state["baseline_identity"] = identity
    state["source_verification"] = copy.deepcopy(seed.get("source_verification", {}))
    for node in state["nodes"]:
        if node["id"] in state["source_verification"]:
            node["source_verification"] = copy.deepcopy(state["source_verification"][node["id"]])
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


class StaleStateRevision(ValueError):
    """A compare-and-swap state write lost to a concurrent revision."""


class TamperedState(ValueError):
    """The derived state file failed its own integrity check."""


def _journal_path(state_path: Path | None = None) -> Path:
    target = Path(state_path or STATE)
    if target.resolve() == STATE.resolve():
        return JOURNAL
    return target.parent / "evidence" / "journal.jsonl"


def _logical_now(state: dict) -> str:
    return str(state.get("logical_time") or _utc_now())


def _event(kind: str, payload: dict, *, created_at: str | None = None, actor: dict | None = None, source: dict | None = None) -> dict:
    return {
        "kind": kind,
        "created_at": created_at or _utc_now(),
        "actor": actor or {"principal": "PROGRAMMA_ENGINEER_R1", "role": "IMPLEMENTER", "verified": False},
        "source": source or {},
        "payload": payload,
    }


def _apply_event(state: dict, event: dict) -> dict:
    kind = event.get("kind")
    payload = event.get("payload") or {}
    state["logical_time"] = event.get("created_at")
    if kind == "GENESIS":
        state["genesis_event"] = event.get("event_id")
        claim = str(payload.get("baseline_sha") or "")
        identity = state.setdefault("baseline_identity", {})
        identity["genesis_claim"] = claim or None
        identity["genesis_claim_interpretation"] = (
            "INHERITED_OLIVE_SOURCE_IDENTITY_NOT_ENGINEERING_BASELINE"
            if claim and claim != ENGINEERING_BASELINE
            else "ENGINEERING_BASELINE"
        )
        return {"kind": kind, "status": "GENESIS"}
    if kind == "CANDIDATE_EVIDENCE":
        importer = payload.get("importer")
        if importer == "OSCIENCE":
            patch = _load(ROOT / payload.get("patch_file", OSCIENCE_PATCH.name))
            actual_digest = _digest(patch)
            asserted_digest = payload.get("patch_digest")
            if asserted_digest and asserted_digest != actual_digest:
                raise ValueError(
                    f"OSCIENCE_PATCH_DIGEST_MISMATCH:{actual_digest}!={asserted_digest}")
            result = ingest_oscience(
                state,
                patch,
                patch_digest=actual_digest,
                source_commit=payload.get("source_commit", OSCIENCE_CUT),
            )
            return {"kind": kind, "status": result.get("status"), "event": event.get("event_id")}
        state.setdefault("node_evidence", {}).setdefault(payload.get("node_id", "UNKNOWN"), []).append({
            "kind": "CANDIDATE_EVIDENCE",
            "payload": payload,
            "event_id": event.get("event_id"),
        })
        return {"kind": kind, "status": "CANDIDATE_EVIDENCE_APPLIED", "event": event.get("event_id")}
    if kind == "QUARANTINE":
        state["quarantine"] = copy.deepcopy(payload)
        state["excluded_events"] = copy.deepcopy(payload.get("excluded_history_ids", []))
        return {"kind": kind, "status": "QUARANTINE_RECORDED", "event": event.get("event_id")}
    if kind == "RETURN_INTAKE":
        result = intake_candidate(state, payload)
        return {"kind": kind, "status": result.get("status"), "result": result, "event": event.get("event_id")}
    if kind == "SOURCE_CUT_REFRESH":
        observed = payload.get("observed") or observe_source_cut()
        refreshed = refresh_state(state, observed)
        state.clear()
        state.update(refreshed)
        return {"kind": kind, "status": "SOURCE_CUT_REFRESHED", "event": event.get("event_id")}
    if kind == "TRANSITION_REQUEST":
        fixture = payload.get("fixture") or {}
        try:
            result = _apply_transition(state, fixture)
        except ValueError as error:
            result = {"status": "REFUSED", "reason": str(error)}
        return {"kind": kind, "status": result.get("status"), "result": result, "event": event.get("event_id")}
    if kind == "EVIDENCE_WITHDRAWAL":
        state.setdefault("withdrawals", []).append({
            "event_id": event.get("event_id"),
            "withdraws_event_id": payload.get("withdraws_event_id"),
            "reason": payload.get("reason", "WITHDRAWN"),
            "node_id": payload.get("node_id"),
            "scope": payload.get("scope"),
            "basis": payload.get("basis"),
            "authority": payload.get("authority"),
            "qualified": bool(payload.get("basis") and payload.get("authority")),
        })
        return {"kind": kind, "status": "WITHDRAWAL_RECORDED", "event": event.get("event_id")}
    state.setdefault("unknown_events", []).append(event.get("event_id"))
    return {"kind": kind, "status": "UNKNOWN_EVENT_TYPE", "event": event.get("event_id")}


def rebuild_from_journal(journal_path: Path | None = None, observed_source: dict[str, Any] | None = None, *, operating: bool = True) -> dict:
    target = Path(journal_path or JOURNAL)
    events = evidence_store.read_journal(target)
    if observed_source is None:
        observed_source = observe_source_cut(git_enabled=False)
    state = _base_state(observed_source)
    state["operating"] = operating
    withdrawn = {
        e.get("payload", {}).get("withdraws_event_id")
        for e in events
        if e.get("kind") == "EVIDENCE_WITHDRAWAL"
    }
    applied = []
    for event in events:
        if event.get("event_id") in withdrawn:
            continue
        result = _apply_event(state, event)
        applied.append({"event_id": event.get("event_id"), "kind": event.get("kind"), "status": result.get("status")})
    state["journal_head"] = events[-1]["event_id"] if events else evidence_store.GENESIS
    state["revision"] = len(events)
    state["journal_applied"] = applied
    state["freshness"] = {
        "generated_at": events[-1]["created_at"] if events else state["freshness"]["generated_at"],
        "refresh_command": "python3 living_reference.py rebuild",
        "journal": str(target),
    }
    _recompute(state)
    state["state_digest"] = _digest({k: v for k, v in state.items() if k != "state_digest"})
    return state


def commit_event(body: dict, *, journal_path: Path | None = None, state_path: Path | None = None, snapshot_path: Path | None = None, expected_head: str | None = None) -> dict:
    target = Path(journal_path or JOURNAL)
    commit_lock_path = target.with_name(target.name + ".commit.lock")
    commit_lock_path.parent.mkdir(parents=True, exist_ok=True)
    with commit_lock_path.open("a+") as commit_lock:
        fcntl.flock(commit_lock.fileno(), fcntl.LOCK_EX)
        try:
            existing_events = evidence_store.read_journal(target)
            _check_journal_regression(existing_events, Path(state_path or STATE))
            appended = evidence_store.append_event(target, body, expected_head=expected_head)
            last_error = None
            for _ in range(3):
                state = rebuild_from_journal(target, operating=True)
                state["revision"] = appended["event"]["sequence"]
                try:
                    _save(state, state_path or STATE, snapshot_path, revision=state["revision"])
                    last_error = None
                    break
                except StaleStateRevision as error:
                    last_error = error
                    continue
            if last_error is not None:
                raise last_error
        finally:
            fcntl.flock(commit_lock.fileno(), fcntl.LOCK_UN)
    applied = state.get("journal_applied", [])
    payload = (appended.get("event") or {}).get("payload") or {}
    subject = payload.get("fixture") or payload
    node_id = subject.get("node_id") or subject.get("id")
    return {
        **appended,
        "revision": state["revision"],
        "state_digest": state["state_digest"],
        "journal_head": state["journal_head"],
        "applied": applied[-1] if applied else None,
        "axes": {node_id: state.get("axes", {}).get(node_id)} if node_id else {},
    }


def journal_summary(path: Path | None = None) -> dict:
    return evidence_store.event_summary(evidence_store.read_journal(Path(path or JOURNAL)))


def _state_marker(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        data = _load(path)
    except (json.JSONDecodeError, OSError, ValueError):
        return None
    expected = _digest({k: v for k, v in data.items() if k != "state_digest"})
    if data.get("state_digest") != expected:
        return None
    revision = data.get("revision")
    head = data.get("journal_head")
    if not isinstance(revision, int) or not head:
        return None
    return {"revision": revision, "head": str(head), "path": str(path)}


def _known_journal_marker(target: Path) -> dict | None:
    markers = [m for m in (_state_marker(target), _state_marker(target.parent / SNAPSHOT.name)) if m]
    if not markers:
        return None
    highest = max(markers, key=lambda m: m["revision"])
    same_revision = [m for m in markers if m["revision"] == highest["revision"]]
    if len({m["head"] for m in same_revision}) > 1:
        raise evidence_store.JournalRegression("STATE_SNAPSHOT_HEAD_DIVERGENCE")
    return highest


def _check_journal_regression(events: list[dict], target: Path, *, recover: bool = False) -> dict | None:
    known = _known_journal_marker(target)
    if known is None:
        return None
    head = events[-1]["event_id"] if events else evidence_store.GENESIS
    ids = {e["event_id"] for e in events}
    if len(events) < known["revision"]:
        if not recover:
            raise evidence_store.JournalRegression(
                f"JOURNAL_PREFIX_OLDER_THAN_KNOWN_STATE:{len(events)}<{known['revision']}")
        return known
    if len(events) == known["revision"] and head != known["head"]:
        if not recover:
            raise evidence_store.JournalRegression("JOURNAL_HEAD_DIVERGES_FROM_KNOWN_STATE")
        return known
    if len(events) > known["revision"] and known["head"] not in ids:
        if not recover:
            raise evidence_store.JournalRegression("JOURNAL_DOES_NOT_CONTAIN_KNOWN_STATE_HEAD")
        return known
    return known


def _load_state(path: Path | None = None, *, recover: bool = False) -> dict:
    target = Path(path or STATE)
    journal = _journal_path(target)
    if journal.exists():
        events = evidence_store.read_journal(journal)
        head = events[-1]["event_id"] if events else evidence_store.GENESIS
        known = _check_journal_regression(events, target, recover=recover)
        if target.exists():
            try:
                disk = _load(target)
            except (json.JSONDecodeError, OSError, ValueError):
                if not recover:
                    raise TamperedState("STATE_FILE_UNREADABLE_OR_TRUNCATED")
                disk = None
            if disk is not None:
                expected = _digest({k: v for k, v in disk.items() if k != "state_digest"})
                if disk.get("state_digest") != expected:
                    if not recover:
                        raise TamperedState("STATE_DIGEST_MISMATCH")
                elif disk.get("journal_head") == head and disk.get("schema") == SCHEMA and int(disk.get("revision") or -1) == len(events):
                    disk["operating"] = True
                    return disk
        state = rebuild_from_journal(journal, operating=True)
        if known and len(events) < known["revision"]:
            state["journal_regression_recovery"] = {
                "known": known,
                "journal_events": len(events),
                "status": "EXPLICIT_RECOVERY_FROM_SHORTER_JOURNAL",
                "accepted_events_preserved": False,
            }
            state["history"].append({
                "history_id": "H%04d" % (len(state["history"]) + 1),
                "kind": "JOURNAL_REGRESSION_RECOVERED",
                "known": known,
                "journal_events": len(events),
                "read_at": _utc_now(),
            })
            _recompute(state)
        _save(state, target, revision=int(state.get("revision") or 0), allow_regression=recover)
        return state
    if not target.exists():
        state = build_state()
        state["operating"] = True
        _save(state, target)
        return state
    state = _load(target)
    expected = _digest({k: v for k, v in state.items() if k != "state_digest"})
    if state.get("state_digest") != expected and not recover:
        raise TamperedState("STATE_DIGEST_MISMATCH")
    if state.get("schema") != SCHEMA:
        state = refresh_state(state, state.get("source_snapshot"))
        _save(state, target)
    state["operating"] = True
    return state


def _save(state: dict, path: Path | None = None, snapshot: Path | None = None, *, expected_revision: int | None = None, revision: int | None = None, allow_regression: bool = False) -> None:
    target = Path(path or STATE)
    snap = Path(snapshot) if snapshot else (target.parent / SNAPSHOT.name)
    lock_path = target.with_name(target.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            current_revision = 0
            if target.exists():
                try:
                    current_revision = int(_load(target).get("revision") or 0)
                except (json.JSONDecodeError, OSError):
                    current_revision = 0
            if expected_revision is not None and current_revision != expected_revision:
                raise StaleStateRevision(f"STALE_REVISION expected={expected_revision} observed={current_revision}")
            new_revision = int(revision) if revision is not None else current_revision + 1
            if new_revision < current_revision and not allow_regression:
                raise StaleStateRevision(f"STALE_REVISION_NEWER_STATE_EXISTS current={current_revision} attempted={new_revision}")
            state["revision"] = new_revision
            state["state_digest"] = _digest({k: v for k, v in state.items() if k != "state_digest"})
            payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
            for destination in dict.fromkeys((target, snap)):
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
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


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


SOURCE_BLOCK_REASONS = {
    "SOURCE_WITHDRAWN": "source withdrawn by qualified owner",
    "SOURCE_NOT_FOUND": "source absence qualified",
    "AUTHORIZED_EXCLUSION": "source path excluded by authorized scope",
    "UNREAD": "source witness not available now",
    "WITNESS_MISMATCH": "source witness bytes mismatch",
    "SOURCE_REF_INVALID": "source reference invalid",
    "MISSING": "source missing",
    "SOURCE_INVALID": "source invalid",
}


def _axis_blockers(state: dict, node_id: str) -> list[dict]:
    axis = state["axes"].get(node_id, {})
    blockers = []
    for key, values, label in (
        ("source_recovery", NEGATIVE_SOURCE, "source loss"),
        ("science", {"NOT_ISSUED", "REFUSED", "CANDIDATE_EVIDENCE_NOT_ISSUED", "HOLD_MANUAL_VERIFICATION"}, "science not issued"),
        ("authority", {"NOT_ADOPTED", "UNADOPTED", "REVOKED", "OWNER_EVIDENCE_PENDING_MANUAL_VERIFICATION"}, "owner authority held"),
        ("review", NEGATIVE_REVIEW, "review failed"),
        ("engineering", NEGATIVE_ENGINEERING, "engineering failed"),
        ("professional", set(), ""),
    ):
        if key == "professional":
            continue
        value = str(axis.get(key, ""))
        if value in values:
            reason = SOURCE_BLOCK_REASONS.get(value, label) if key == "source_recovery" else label
            blockers.append({"node": node_id, "axis": key, "status": value, "reason": reason})
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
    for node_id, report in state.get("source_verification", {}).items():
        status = report.get("status")
        if status not in {"UNREAD", "WITNESS_MISMATCH", "SOURCE_REF_INVALID"}:
            continue
        node = nodes.get(node_id, {})
        _add_gap(gaps, {
            "id": "GAP_WITNESS_" + node_id,
            "domain": "SOURCE_WITNESS",
            "node": node_id,
            "class": "SOURCE_WITNESS_NOT_CURRENT",
            "status": status,
            "owner": node.get("owner", "UNKNOWN"),
            "next": "Re-read the exact witness at its recorded identity; do not claim SOURCE_EXACT from a ref alone.",
            "consequence": "The node keeps a historical or reported status but its current witness is not verified.",
            "blockers": _axis_blockers(state, node_id),
            "impact": _impact(state, node_id),
            "parallel_group": "SOURCE_WITNESS",
            "evidence_status": "WITNESS_STATUS_DERIVED",
            "source_backed": False,
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
        items = sorted(items, key=lambda g: (str(g.get("domain", "")), str(g.get("id", ""))))
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
                "evidence_status": gap.get("evidence_status", "SOURCE_DEFINED"),
                "source_backed": gap.get("source_backed", True),
                "terminal_contribution": gap.get("parent_obligation") or gap.get("consequence") or "UNSPECIFIED",
                "uncertainty": {
                    "status": gap.get("status", "UNKNOWN"),
                    "blocker_count": len(gap.get("blockers", [])),
                    "source_backed": gap.get("source_backed", True),
                    "evidence_status": gap.get("evidence_status", "SOURCE_DEFINED"),
                },
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


def maturity_view(state: dict, node_id: str) -> dict:
    node = _node_map(state).get(node_id)
    if not node:
        return {"error": "UNKNOWN_ID", "id": node_id}
    supplied = node.get("maturity") or {}
    stages = {}
    for stage in MATURITY_STAGES:
        stages[stage] = copy.deepcopy(supplied.get(stage) or {
            "status": "UNKNOWN",
            "note": "No stage-specific evidence in this vertical slice.",
            "owner": node.get("owner", "UNKNOWN"),
        })
    return {
        "id": node_id,
        "title": node.get("title"),
        "owner": node.get("owner"),
        "stages": stages,
        "source_refs": node.get("source_refs", []),
        "source_verification": node.get("source_verification") or state.get("source_verification", {}).get(node_id, {}),
        "rule": "Stages are independent evidence axes; code does not prove theory and native validation is not inferred from a fixture.",
    }


def _gap_record(rec: dict) -> dict:
    out = copy.deepcopy(rec)
    out.setdefault("missing_stages", [])
    out.setdefault("alternatives", [])
    out.setdefault("dependencies", [])
    out.setdefault("blocked_by", [])
    out.setdefault("independently_actionable", not bool(out["blocked_by"]))
    out.setdefault("hq_judgment_required", True)
    out.setdefault("next", out.get("smallest_useful_next_action", "UNKNOWN"))
    out.setdefault("consequence", out.get("falsifier", "The gap remains unresolved."))
    out.setdefault("owner", "UNKNOWN")
    out.setdefault("status", "UNKNOWN")
    out.setdefault("domain", "UNKNOWN")
    out.setdefault("node", out.get("node", "UNKNOWN"))
    out.setdefault("blockers", [])
    out.setdefault("impact", {"downstream_required_count": 0, "affected_l0": [], "affected_sectors": []})
    out.setdefault("parallel_group", "WHOLE_PROGRAM_GAP")
    out.setdefault("evidence_status", "SOURCE_DEFINED")
    out.setdefault("source_backed", True)
    return out


def whole_program_gaps(state: dict, stage: str = "", domain: str = "") -> dict:
    records = {g["id"]: _gap_record(g) for g in state.get("p1_gap_records", [])}
    for gap in state.get("gaps", []):
        if gap["id"] in records:
            continue
        records[gap["id"]] = _gap_record({
            "id": gap["id"],
            "parent_obligation": gap.get("consequence") or gap.get("next"),
            "domain": gap.get("domain", "DERIVED"),
            "node": gap.get("node"),
            "status": gap.get("status", "UNKNOWN"),
            "missing_stages": [],
            "existing_evidence": [gap.get("status", "")] if gap.get("status") else [],
            "alternatives": [],
            "dependencies": [],
            "affected_consumer": gap.get("node"),
            "owner": gap.get("owner", "UNKNOWN"),
            "smallest_useful_next_action": gap.get("next", "UNKNOWN"),
            "falsifier": gap.get("consequence", "The gap remains unresolved."),
            "blocked_by": [b.get("reason", "blocked") for b in gap.get("blockers", [])],
            "independently_actionable": not gap.get("blockers"),
            "derived_gap": True,
            "evidence_status": gap.get("evidence_status", "SOURCE_DEFINED"),
            "source_backed": gap.get("source_backed", True),
            "evidence_locator": gap.get("evidence_locator"),
            "return_sha": gap.get("return_sha"),
            "locator_reason": gap.get("locator_reason"),
            "inference_rationale": gap.get("inference_rationale"),
        })
    selected = []
    for rec in records.values():
        if stage and stage not in rec.get("missing_stages", []) and rec.get("status") != stage:
            continue
        if domain and rec.get("domain") != domain:
            continue
        selected.append(rec)
    groups: dict[str, dict] = {}
    for rec in selected:
        group = groups.setdefault(rec.get("domain", "UNKNOWN"), {"domain": rec.get("domain"), "gaps": []})
        group["gaps"].append(rec)
    return {
        "schema": "SOROK_WHOLE_PROGRAM_GAPS@1",
        "filter": {"stage": stage, "domain": domain},
        "count": len(selected),
        "groups": [groups[k] for k in sorted(groups)],
        "counts_by_stage": {
            s: sum(1 for r in selected if s in r.get("missing_stages", []))
            for s in MATURITY_STAGES
        },
        "independently_actionable": sum(1 for r in selected if r.get("independently_actionable")),
        "blocked": sum(1 for r in selected if r.get("blocked_by")),
        "note": "No completeness denominator and no automatic P0. Existing tickets are not the denominator.",
    }


def _node_brief(state: dict, node_id: str) -> dict:
    node = _node_map(state).get(node_id, {})
    refs = node.get("source_refs") or []
    ref = refs[0] if refs else {}
    return {
        "id": node_id,
        "title": node.get("title"),
        "summary": node.get("summary"),
        "status": node.get("status"),
        "owner": node.get("owner"),
        "source": {
            "commit": ref.get("commit"),
            "path": ref.get("path"),
            "blob": ref.get("blob") or ref.get("object_id"),
            "quote": ref.get("quote"),
            "depth": ref.get("depth"),
        } if ref else {},
        "source_verification": node.get("source_verification", {}),
        "maturity": maturity_view(state, node_id)["stages"] if node_id in _node_map(state) else {},
    }


def home_view(state: dict) -> dict:
    nodes = _node_map(state)
    terminal = []
    for gid in (
        "GAP-Q-HEALTH-FLOURISHING",
        "GAP-CAN011-PRACTICE-ACQUISITION",
        "GAP-V3-YEARLY-PERSONA-MIGRATION",
        "GAP-S13-NONEXTRACTIVE-REVENUE",
        "GAP-S14-PRIVACY-ABUSE",
        "GAP-S11-ACCESSIBLE-ENCOUNTER-UX",
        "GAP-A5-HUMAN-ALPHA",
    ):
        rec = next((g for g in state.get("p1_gap_records", []) if g["id"] == gid), None)
        if rec:
            terminal.append({
                "id": rec["id"],
                "obligation": rec["parent_obligation"],
                "status": rec["status"],
                "missing_stages": rec["missing_stages"],
                "owner": rec["owner"],
                "independently_actionable": rec.get("independently_actionable", True),
            })
    recent = list(state.get("history", []))[-5:]
    witness = [
        {"id": node_id, "title": nodes.get(node_id, {}).get("title"), "status": report.get("status"), "reason": report.get("reason")}
        for node_id, report in state.get("source_verification", {}).items()
        if report.get("status") in {"UNREAD", "WITNESS_MISMATCH", "SOURCE_REF_INVALID"}
    ]
    blocked = [
        {"id": n["id"], "title": n.get("title"), "status": n.get("status")}
        for n in state["nodes"]
        if n.get("programma_p1") and str(n.get("status", "")).lower() in {"held", "missing", "missing_rule", "blocked_named_authority_required", "reported_not_accessed_now", "unknown", "evidence_mismatch_unresolved"}
    ]
    return {
        "schema": "SOROK_PROGRAMMA_HOME@1",
        "purpose": {
            "kind": "UNCHOSEN_NEIGHBOR",
            "id": "PURPOSE_UNCHOSEN_NEIGHBOR",
            "title": nodes.get("PURPOSE_UNCHOSEN_NEIGHBOR", {}).get("title"),
            "purpose": nodes.get("PURPOSE_UNCHOSEN_NEIGHBOR", {}).get("summary"),
            "summary": nodes.get("PURPOSE_UNCHOSEN_NEIGHBOR", {}).get("summary"),
            "status": nodes.get("PURPOSE_UNCHOSEN_NEIGHBOR", {}).get("status"),
            "owner": nodes.get("PURPOSE_UNCHOSEN_NEIGHBOR", {}).get("owner"),
            "source": _node_brief(state, "PURPOSE_UNCHOSEN_NEIGHBOR")["source"],
            "maturity": _node_brief(state, "PURPOSE_UNCHOSEN_NEIGHBOR")["maturity"],
        },
        "intended_human_experience": {
            "astra_b_scene": _node_brief(state, "ASTRA_B_SCENE"),
            "astra_d_longitudinal": _node_brief(state, "ASTRA_D_LONGITUDINAL"),
            "negative_controls": _node_brief(state, "ASTRA_NEGATIVE_CONTROLS"),
        },
        "constraints_100_101": {
            "alpha_100": _node_brief(state, "SOROK_100_ALPHA"),
            "binding_101": _node_brief(state, "SOROK_101_BINDING"),
            "two_call_proposal": _node_brief(state, "SOROK_101_TWO_CALL_PROPOSAL"),
            "hidden_interiority": _node_brief(state, "SOROK_101_HIDDEN_INTERIORITY"),
        },
        "status": "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED",
        "whole_scope": "WHOLE_SCOPE_NOT_YET_PROVEN",
        "one_paragraph": "PROGRAMMA is the living operating reference for the whole Sorok undertaking. It preserves original purposes, rival explanations, exact source and code cuts, actual consumers, negative evidence, maturity gaps, owners and next lawful work. It is not the developmental person and no native/human/PRE-MAIN adoption is issued here.",
        "kernel": "KERNEL_UNRESOLVED",
        "terminal_obligations": terminal,
        "blocked_or_held": blocked,
        "source_witness": witness,
        "recent_change": recent,
        "source_freshness": state.get("source_snapshot"),
        "counts": {
            "nodes": len(state["nodes"]),
            "edges": len(state["edges"]),
            "gaps": state.get("whole_program_gaps", {}).get("count", 0),
            "journal_head": state.get("journal_head"),
        },
        "notice": "Missing edges stay visible. Source counts are not progress. Human A5, native science and PRE-MAIN adoption remain separate.",
    }


def focus_view(state: dict, node_id: str, depth: int = 1) -> dict:
    if node_id not in _node_map(state):
        return {"error": "UNKNOWN_ID", "id": node_id}
    nodes, edges = _neighbors(state, node_id, depth)
    outgoing = [e for e in edges if e["from"] == node_id]
    incoming = [e for e in edges if e["to"] == node_id]
    missing = [e for e in edges if e.get("dependency") == "MISSING_EDGE" or e.get("grade") == "MISSING"]
    return {
        "id": node_id,
        "node": _node_map(state)[node_id],
        "axes": state["axes"].get(node_id),
        "maturity": maturity_view(state, node_id),
        "source_verification": state.get("source_verification", {}).get(node_id),
        "outgoing": outgoing,
        "incoming": incoming,
        "missing_or_unproven": missing,
        "neighbourhood": {"nodes": [n["id"] for n in nodes], "edges": len(edges)},
        "inverse_navigation": "Derived from the same directed edges; no second manual graph.",
    }


def lateral_view(state: dict, node_id: str) -> dict:
    if node_id not in _node_map(state):
        return {"error": "UNKNOWN_ID", "id": node_id}
    edges = [e for e in state["edges"] if e["from"] == node_id or e["to"] == node_id]
    groups: dict[str, list[dict]] = {}
    for edge in edges:
        key = edge.get("dependency") or edge.get("dependency_type") or "OTHER"
        groups.setdefault(key, []).append(edge)
    return {
        "id": node_id,
        "groups": groups,
        "alternatives": [e for e in edges if e.get("dependency") in {"ALTERNATIVE", "CONTRADICTS"}],
        "missing": [e for e in edges if e.get("dependency") == "MISSING_EDGE" or e.get("grade") == "MISSING"],
        "rule": "Association, mention, hypothesis and source-location edges are not required causal blockers.",
    }


def code_consumer_view(state: dict, node_id: str) -> dict:
    node = _node_map(state).get(node_id)
    if not node:
        return {"error": "UNKNOWN_ID", "id": node_id}
    code_edges = [e for e in state["edges"] if e["from"] == node_id or e["to"] == node_id]
    code_edges = [e for e in code_edges if any(token in e.get("relation", "") for token in ("consumer", "calls", "implements", "import", "historically", "first_consumed", "realization"))]
    return {
        "id": node_id,
        "title": node.get("title"),
        "status": node.get("status"),
        "source_refs": node.get("source_refs", []),
        "source_verification": state.get("source_verification", {}).get(node_id),
        "code_and_consumer_edges": code_edges,
        "current_importer": "NONE_VERIFIED" if node_id in {"V3_RUN_ONE_YEAR", "V3_PERSONA_SHEET", "CURRENT_V3_IMPORTER_MISSING"} else "SEE_EDGES",
        "rule": "HISTORICALLY_CALLED_BY is not CURRENTLY_IMPORTED_BY.",
    }


def evidence_view(state: dict, node_id: str) -> dict:
    node = _node_map(state).get(node_id)
    if not node:
        return {"error": "UNKNOWN_ID", "id": node_id}
    return {
        "id": node_id,
        "source_refs": node.get("source_refs", []),
        "node_evidence": state.get("node_evidence", {}).get(node_id, []),
        "axes": state["axes"].get(node_id),
        "maturity": maturity_view(state, node_id),
        "source_verification": state.get("source_verification", {}).get(node_id),
        "acceptance_record": node.get("acceptance_record"),
        "acceptance_verification": node.get("acceptance_verification"),
        "local_hash_custody": "LOCAL_INTEGRITY_ONLY_NOT_EXTERNAL_CUSTODY",
    }


def owners_view(state: dict) -> dict:
    groups: dict[str, list[dict]] = {}
    for gap in state.get("p1_gap_records", []):
        groups.setdefault(gap.get("owner", "UNKNOWN"), []).append({
            "id": gap["id"],
            "obligation": gap["parent_obligation"],
            "status": gap["status"],
            "missing_stages": gap["missing_stages"],
            "next": gap["smallest_useful_next_action"],
        })
    return {
        "owners": [{"owner": owner, "gaps": groups[owner]} for owner in sorted(groups)],
        "rule": "Owner here is a competent domain owner, not an automatic task assignee or a new authority.",
    }


def _negative_axes(axis: dict, *, include_consumer: bool = True) -> list[tuple[str, str]]:
    out = []
    for key, values in (
        ("source_recovery", NEGATIVE_SOURCE),
        ("review", NEGATIVE_REVIEW),
        ("engineering", NEGATIVE_ENGINEERING),
        ("science", NEGATIVE_SCIENCE),
        ("authority", NEGATIVE_AUTHORITY),
    ):
        value = str(axis.get(key, ""))
        if value in values:
            out.append((key, value))
    if include_consumer and str(axis.get("consumer", "")).startswith("INVALIDATED"):
        out.append(("consumer", str(axis.get("consumer", ""))))
    return out


def _recompute_consumer_grades(state: dict) -> None:
    """Restore only when every active required prerequisite is non-negative.

    A second independent RED remains a blocker.  Mention, hypothesis,
    association and source-location edges never enter this calculation.
    Unrelated holds elsewhere are not global prerequisites.
    """
    baseline = state.setdefault("consumer_baseline", {})
    for node_id, axis in state["axes"].items():
        current = str(axis.get("consumer", ""))
        if not current.startswith("INVALIDATED"):
            if current and current not in {"EXTERNAL_BOUNDARY"}:
                baseline.setdefault(node_id, current)
            continue
        if _negative_axes(axis, include_consumer=False):
            continue
        blockers = []
        for edge in _required_incoming(state, node_id):
            source = edge["from"]
            source_axis = state["axes"].get(source, {})
            for key, value in _negative_axes(source_axis):
                blockers.append((source, key, value))
        if blockers:
            continue
        restore = baseline.get(node_id) or "CANDIDATE_READY"
        if str(restore).startswith("INVALIDATED"):
            restore = "CANDIDATE_READY"
        axis["consumer"] = restore


def _recompute(state: dict) -> None:
    state["sectors"] = _sectors(state["nodes"], [m["id"] for m in state.get("missing_functions", [])])
    state["gaps"] = compute_gaps(state)
    _recompute_consumer_grades(state)
    state["whole_program_gaps"] = whole_program_gaps(state)
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


def _sha40(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{40}", value or ""))


def _verify_source_ref(ref: dict) -> tuple[bool, str]:
    if ref.get("repository") == "LOCAL_EXTERNAL_RAWLSING_DESKTOP":
        path = Path(str(ref.get("path") or ""))
        if not path.exists():
            return False, "LOCAL_EXTERNAL_SOURCE_NOT_PRESENT"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = str(ref.get("sha256") or "")
        if expected and actual != expected:
            return False, f"LOCAL_EXTERNAL_SHA256_MISMATCH:{actual}!={expected}"
        return True, "LOCAL_EXTERNAL_SOURCE_VERIFIED"
    if ref.get("repository") not in {None, "maidiu/rawlsing"}:
        return True, "EXTERNAL_REPOSITORY_NOT_REVERIFIED_LOCALLY"
    commit = str(ref.get("commit") or "")
    path = str(ref.get("path") or "")
    blob = str(ref.get("blob") or "")
    if not commit or not path:
        return False, "SOURCE_REF_MISSING_COMMIT_OR_PATH"
    actual_type = _git(["cat-file", "-t", f"{commit}:{path}"])
    if not actual_type:
        return False, "SOURCE_REF_GIT_OBJECT_MISSING"
    actual_blob = _git(["rev-parse", f"{commit}:{path}"])
    if blob and actual_blob != blob:
        return False, f"SOURCE_REF_BLOB_MISMATCH:{actual_blob}!={blob}"
    return True, "GIT_SOURCE_REF_VERIFIED"


def _classify_source_refs(node: dict) -> dict:
    refs = node.get("source_refs") or []
    if not refs:
        return {"status": "INDEX_ONLY", "refs": [], "reason": "NO_SOURCE_REFS"}
    results = []
    for ref in refs:
        repository = ref.get("repository")
        if repository not in {None, "maidiu/rawlsing", "LOCAL_EXTERNAL_RAWLSING_DESKTOP"}:
            results.append({
                "status": "EXTERNAL_REPORTED_NOT_REVERIFIED",
                "reason": "EXTERNAL_REPOSITORY_NOT_REVERIFIED_LOCALLY",
                "ref": ref,
            })
            continue
        ok, reason = _verify_source_ref(ref)
        if ok:
            status = "SOURCE_EXACT"
        elif reason == "LOCAL_EXTERNAL_SOURCE_NOT_PRESENT":
            status = "UNREAD"
        elif reason.startswith("LOCAL_EXTERNAL_SHA256_MISMATCH"):
            status = "WITNESS_MISMATCH"
        else:
            status = "SOURCE_REF_INVALID"
        results.append({"status": status, "reason": reason, "ref": ref})
    statuses = {item["status"] for item in results}
    for status in ("WITNESS_MISMATCH", "UNREAD", "SOURCE_REF_INVALID", "EXTERNAL_REPORTED_NOT_REVERIFIED", "SOURCE_EXACT"):
        if status in statuses:
            return {"status": status, "refs": results, "reason": next(i["reason"] for i in results if i["status"] == status)}
    return {"status": "INDEX_ONLY", "refs": results, "reason": "NO_SOURCE_REFS"}


def verify_source_refs(state: dict) -> dict:
    checked = 0
    failures = []
    external = 0
    node_status = {}
    for node in state["nodes"]:
        if not node.get("programma_p1"):
            continue
        report = _classify_source_refs(node)
        node_status[node["id"]] = report
        for item in report["refs"]:
            checked += 1
            ref = item["ref"]
            if ref.get("repository") not in {None, "maidiu/rawlsing", "LOCAL_EXTERNAL_RAWLSING_DESKTOP"}:
                external += 1
                continue
            if item["status"] != "SOURCE_EXACT":
                failures.append({"node": node["id"], "reason": item["reason"], "ref": ref, "status": item["status"]})
    return {
        "checked_local": checked - external,
        "external_not_reverified_locally": external,
        "failures": failures,
        "node_status": node_status,
        "result": "PASS" if not failures else "FAIL",
        "note": "Git identity and local external bytes are verified; controller/Library/other repositories are not re-read offline. Missing witnesses are reported as UNREAD, not SOURCE_EXACT.",
    }


ACCEPTANCE_VERDICTS = {"ACCEPT_SCOPED", "REVIEW_PASSED_SCOPED", "PASS", "ACCEPT"}


def _record_ref_for_source(ref: dict) -> str:
    commit = str(ref.get("commit") or "")
    path = str(ref.get("path") or "")
    return f"{commit}:{path}" if commit and path else ""


def _node_record_source(node: dict, record_ref: str) -> dict | None:
    for ref in node.get("source_refs") or []:
        if _record_ref_for_source(ref) == record_ref:
            return ref
    return None


def _parse_acceptance_record(state: dict, node_id: str, record_ref: str, *, require_node_subject: bool = True, expected_subject: str | None = None) -> tuple[bool, str, dict]:
    node = _node_map(state).get(node_id)
    if not node:
        return False, "UNKNOWN_NODE", {}
    if not record_ref or ":" not in record_ref:
        return False, "REVIEW_RECORD_REF_MALFORMED", {}
    commit, path = record_ref.split(":", 1)
    if not _sha40(commit) or not path:
        return False, "REVIEW_RECORD_REF_MALFORMED", {}
    ref = _node_record_source(node, record_ref)
    if ref is None:
        return False, "REVIEW_RECORD_NOT_A_NODE_SOURCE", {}
    ok, reason = _verify_git_object({
        "commit": commit, "path": path, "object_type": "blob",
        "blob": ref.get("blob") or ref.get("object_id"),
    })
    if not ok:
        return False, "REVIEW_RECORD_OBJECT_INVALID:" + reason, {}
    blob = _git(["rev-parse", f"{commit}:{path}"]) or ""
    body = _git(["show", f"{commit}:{path}"]) or ""
    if not body.strip():
        return False, "REVIEW_RECORD_EMPTY", {}
    principal_match = re.search(r"^#\s*SOROK\s+([A-Za-z0-9][A-Za-z0-9_-]*)\b", body, re.M)
    principal = principal_match.group(1) if principal_match else ""
    role_match = re.search(r"^\*\*ROLE:\*\*\s*(.+)$", body, re.M)
    role = role_match.group(1).strip() if role_match else ""
    if not principal or not role:
        return False, "REVIEW_RECORD_LACKS_REVIEWER_IDENTITY", {}
    if "independent" not in role.lower():
        return False, "REVIEW_RECORD_ROLE_NOT_INDEPENDENT", {}
    reviewed: list[tuple[str, str]] = []
    for line in body.splitlines():
        if "REVIEWED" in line.upper() and "CUT" in line.upper():
            shas = re.findall(r"\b[0-9a-f]{40}\b", line)
            if len(shas) == 1:
                label = re.sub(r"[`*_]", "", line.split(":", 1)[0]).strip()
                reviewed.append((label, shas[0]))
    if not reviewed:
        return False, "REVIEW_RECORD_LACKS_EXACT_REVIEWED_CUT", {}
    assertion_match = re.search(
        r"ACCEPT_SCOPED[`*_]*\s+for\s+exact\s+([0-9a-f]{3,40})\s+([^.;\n]+)", body, re.I)
    if not assertion_match:
        return False, "REVIEW_RECORD_LACKS_EXACT_ACCEPTING_ASSERTION", {}
    assertion_prefix = assertion_match.group(1).lower()
    assertion = assertion_match.group(2).strip()
    assertion_subjects = [sha for _, sha in reviewed if sha.startswith(assertion_prefix)]
    if len(assertion_subjects) != 1:
        return False, "REVIEW_RECORD_ASSERTION_SUBJECT_AMBIGUOUS", {}
    accepted_subject = assertion_subjects[0]
    subject = ""
    node_subject = str(node.get("subject_sha") or "")
    if require_node_subject:
        if not _sha40(node_subject):
            return False, "NODE_SUBJECT_SHA_REQUIRED", {}
        if node_subject not in {sha for _, sha in reviewed}:
            return False, "NODE_SUBJECT_NOT_IN_REVIEW_RECORD", {}
        if node_subject != accepted_subject:
            return False, "NODE_SUBJECT_DOES_NOT_MATCH_ACCEPTING_ASSERTION", {}
        subject = node_subject
    else:
        if expected_subject and expected_subject != accepted_subject:
            return False, "EXPECTED_SUBJECT_DOES_NOT_MATCH_ACCEPTING_ASSERTION", {}
        subject = accepted_subject
    verdict_match = re.search(r"verdict[^\n]*?\b(ACCEPT_SCOPED|REVIEW_PASSED_SCOPED|PASS|ACCEPT)\b", body, re.I)
    if not verdict_match:
        return False, "REVIEW_RECORD_LACKS_EXPLICIT_VERDICT", {}
    verdict = verdict_match.group(1).upper()
    appointment_match = re.search(
        r"(?:EXACT\s+COMMISSION\s+SEAL|APPOINTMENT(?:[_ ]REF)?)\s*:?\s*\**\s*`?([0-9a-f]{40})",
        body, re.I)
    appointment = appointment_match.group(1) if appointment_match else ""
    if not appointment:
        return False, "REVIEW_RECORD_LACKS_APPOINTMENT_SEAL", {}
    if "appoint" not in body.lower() and "commission" not in body.lower():
        return False, "REVIEW_RECORD_LACKS_APPOINTMENT_OR_INTAKE_EVIDENCE", {}
    if _git(["cat-file", "-t", appointment]) != "commit":
        return False, "APPOINTMENT_REF_NOT_A_REAL_COMMIT", {}
    appointment_message = _git(["show", "-s", "--format=%B", appointment]) or ""
    if subject not in body:
        return False, "REVIEW_RECORD_DOES_NOT_BIND_EXACT_SUBJECT", {}
    if subject[:7] not in appointment_message and subject[:3] not in appointment_message:
        return False, "APPOINTMENT_DOES_NOT_BIND_SUBJECT", {}
    author = _git(["show", "-s", "--format=%ae", subject]) or ""
    if not author:
        return False, "SUBJECT_AUTHOR_UNRESOLVED", {}
    if principal.lower() == author.lower():
        return False, "SELF_REVIEW_PRINCIPAL_NOT_DISTINCT", {}
    details = {
        "reviewer_principal": principal,
        "reviewer_role": role,
        "author_principal": author,
        "author_basis": "SUBJECT_COMMIT_AUTHOR_EMAIL",
        "subject_sha": subject,
        "assertion": assertion,
        "scope": [node_id],
        "verdict": verdict,
        "record_ref": record_ref,
        "record_blob": blob,
        "record_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "appointment_ref": appointment,
        "appointment_message": appointment_message.splitlines()[0] if appointment_message else "",
        "node_subject_sha": node_subject or None,
        "binding": "NODE_SOURCE_REF_EXACT_RECORD_BYTES",
    }
    return True, "INDEPENDENT_ACCEPTANCE_VERIFIED", details


def _verify_acceptance_record(state: dict, node_id: str, dimension: str, evidence: dict) -> tuple[bool, str, dict]:
    """Bind a promotion to an existing competent immutable review record.

    Caller-written principals, subjects, assertions and scopes are never
    evidence.  The node must already carry the exact reviewed subject, and the
    referenced record must be one of that node's own immutable source refs.
    """
    if evidence.get("fixture_origin") or evidence.get("kind") == "SYNTHETIC_DEMO":
        return False, "FIXTURE_ORIGIN_CANNOT_PROMOTE", {}
    record = evidence.get("acceptance") or evidence.get("acceptance_record")
    if not isinstance(record, dict):
        return False, "INDEPENDENT_ACCEPTANCE_RECORD_REQUIRED", {}
    record_ref = str(record.get("record_ref") or "").strip()
    ok, reason, details = _parse_acceptance_record(state, node_id, record_ref, require_node_subject=True)
    if not ok:
        return False, reason, {}
    caller_subject = str(record.get("subject_sha") or "")
    if caller_subject and caller_subject != details["subject_sha"]:
        return False, "CALLER_SUBJECT_DOES_NOT_MATCH_RECORD", {}
    caller_reviewer = str(record.get("reviewer_principal") or "")
    if caller_reviewer and caller_reviewer != details["reviewer_principal"]:
        return False, "CALLER_REVIEWER_DOES_NOT_MATCH_RECORD", {}
    caller_verdict = str(record.get("verdict") or "").upper()
    if caller_verdict and caller_verdict != details["verdict"]:
        return False, "CALLER_VERDICT_DOES_NOT_MATCH_RECORD", {}
    caller_appointment = str(record.get("appointment_ref") or "")
    if caller_appointment and caller_appointment != details["appointment_ref"]:
        return False, "CALLER_APPOINTMENT_DOES_NOT_MATCH_RECORD", {}
    if record.get("record_blob") and str(record["record_blob"]) != details["record_blob"]:
        return False, "REVIEW_RECORD_BLOB_MISMATCH", {}
    scope = record.get("scope") or []
    if isinstance(scope, str):
        scope = [scope]
    if "*" in scope:
        return False, "WILDCARD_SCOPE_NOT_ACCEPTED", {}
    if scope and node_id not in scope:
        return False, "ACCEPTANCE_SCOPE_MISMATCH", {}
    if evidence.get("reviewed_sha") and str(evidence["reviewed_sha"]) != details["subject_sha"]:
        return False, "REVIEWED_SHA_DOES_NOT_MATCH_SUBJECT", {}
    details["dimension"] = dimension
    return True, "INDEPENDENT_ACCEPTANCE_VERIFIED", details


def _verify_seed_acceptance_records(state: dict) -> None:
    for node in state["nodes"]:
        record = node.get("acceptance_record")
        if not isinstance(record, dict):
            continue
        record_ref = str(record.get("record_ref") or "")
        ok, reason, details = _parse_acceptance_record(
            state, node["id"], record_ref, require_node_subject=False,
            expected_subject=str(record.get("subject_sha") or "") or None)
        if not ok:
            node["acceptance_verification"] = {
                "status": "REPORTED_ACCEPTANCE_NOT_VERIFIED",
                "reason": reason,
                "record_ref": record_ref,
            }
            if str(node.get("status", "")).upper() in {"ACCEPT_SCOPED", "INDEPENDENT_ACCEPT_SCOPED"}:
                node["status"] = "REPORTED_ACCEPTANCE_NOT_VERIFIED"
            continue
        node["acceptance_verification"] = {
            "status": "VERIFIED_EXISTING_RECORD",
            "reason": reason,
            "subject_sha": details["subject_sha"],
            "reviewer_principal": details["reviewer_principal"],
            "record_blob": details["record_blob"],
            "record_sha256": details["record_sha256"],
            "appointment_ref": details["appointment_ref"],
        }
    verified_subjects = {
        node.get("acceptance_verification", {}).get("subject_sha")
        for node in state["nodes"]
        if node.get("acceptance_verification", {}).get("status") == "VERIFIED_EXISTING_RECORD"
    }
    for node in state["nodes"]:
        if node.get("acceptance_record") or not node.get("acceptance_binding"):
            continue
        subject = str(node.get("subject_sha") or "")
        if subject and subject in verified_subjects:
            node["acceptance_verification"] = {
                "status": "VERIFIED_EXISTING_RECORD",
                "reason": "BOUND_TO_EXACT_EXISTING_ACCEPTANCE_RECORD",
                "subject_sha": subject,
            }
        else:
            node["acceptance_verification"] = {
                "status": "REPORTED_ACCEPTANCE_NOT_VERIFIED",
                "reason": "NO_EXACT_EXISTING_ACCEPTANCE_RECORD",
                "subject_sha": subject or None,
            }
            if str(node.get("status", "")).upper() in {"ACCEPT_SCOPED", "INDEPENDENT_ACCEPT_SCOPED"}:
                node["status"] = "REPORTED_ACCEPTANCE_NOT_VERIFIED"


def _acceptance_request(state: dict, node_id: str, dimension: str, evidence: dict) -> dict:
    ok, reason, details = _verify_acceptance_record(state, node_id, dimension, evidence)
    if not ok:
        return {
            "status": "PENDING_INDEPENDENT_ACCEPTANCE",
            "reason": reason,
            "manual_verification_required": True,
            "accepted": False,
        }
    return {
        "status": "APPLIED_INDEPENDENT_SCOPED",
        "reason": reason,
        "manual_verification_required": False,
        "accepted": True,
        "acceptance": details,
    }


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


WITHDRAWAL_BASES = {
    "SOURCE_OWNER_WITHDRAWAL",
    "QUALIFIED_ABSENCE_VERIFICATION",
    "SOURCE_INTEGRITY_LOSS",
    "AUTHORIZED_SCOPED_EXCLUSION",
}

WITHDRAWAL_TARGET_BASIS = {
    "SOURCE_WITHDRAWN": {"SOURCE_OWNER_WITHDRAWAL"},
    "SOURCE_NOT_FOUND": {"QUALIFIED_ABSENCE_VERIFICATION"},
    "MISSING": {"QUALIFIED_ABSENCE_VERIFICATION", "SOURCE_INTEGRITY_LOSS"},
    "SOURCE_INVALID": {"SOURCE_INTEGRITY_LOSS"},
    "AUTHORIZED_EXCLUSION": {"AUTHORIZED_SCOPED_EXCLUSION"},
}


def _validate_withdrawal_evidence(state: dict, node_id: str, requested_to: str, evidence: dict) -> dict:
    if evidence.get("kind") == "SYNTHETIC_DEMO" or evidence.get("fixture_origin"):
        if state.get("operating"):
            raise ValueError("FIXTURE_ORIGIN_CANNOT_MUTATE_OPERATING_STATE")
        return {"qualified": False, "basis": "SYNTHETIC_DEMO", "status": "SIMULATED_NOT_QUALIFIED"}
    expected_kind = "AUTHORIZED_EXCLUSION" if requested_to == "AUTHORIZED_EXCLUSION" else "SOURCE_WITHDRAWAL"
    if evidence.get("kind") != expected_kind:
        raise ValueError("QUALIFIED_WITHDRAWAL_EVIDENCE_REQUIRED")
    basis = str(evidence.get("basis") or "")
    if basis not in WITHDRAWAL_BASES:
        raise ValueError("WITHDRAWAL_BASIS_INVALID")
    if basis not in WITHDRAWAL_TARGET_BASIS.get(requested_to, set()):
        raise ValueError("WITHDRAWAL_BASIS_TARGET_MISMATCH")
    scope = evidence.get("scope") or [node_id]
    if isinstance(scope, str):
        scope = [scope]
    if node_id not in scope and "*" not in scope:
        raise ValueError("WITHDRAWAL_SCOPE_MISMATCH")
    authority = str(evidence.get("authority") or "")
    if authority not in AUTHORITY_OWNER_SLOTS and authority not in {"SOROK_HQ", "SOROK_ORIGINAL_PRODUCT_OWNER"}:
        raise ValueError("WITHDRAWAL_AUTHORITY_INVALID")
    event_id = str(evidence.get("withdrawal_event_id") or "")
    if state.get("operating"):
        record = next((
            item for item in state.get("withdrawals", [])
            if item.get("event_id") == event_id
            and item.get("node_id") == node_id
            and item.get("basis") == basis
            and item.get("qualified")
        ), None)
        if not record:
            raise ValueError("QUALIFIED_WITHDRAWAL_EVENT_REQUIRED")
        return {
            "qualified": True,
            "basis": basis,
            "authority": authority,
            "scope": scope,
            "withdrawal_event_id": event_id,
            "status": "QUALIFIED_WITHDRAWAL_OR_EXCLUSION",
        }
    return {
        "qualified": True,
        "basis": basis,
        "authority": authority,
        "scope": scope,
        "withdrawal_event_id": event_id or None,
        "status": "QUALIFIED_NONOPERATING_DECLARATION",
    }


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
    withdrawal = None
    if requested_to in {"SOURCE_NOT_FOUND", "SOURCE_WITHDRAWN", "MISSING", "SOURCE_INVALID", "AUTHORIZED_EXCLUSION"}:
        withdrawal = _validate_withdrawal_evidence(state, node_id, requested_to, evidence)
    synthetic = evidence["kind"] == "SYNTHETIC_DEMO" or bool(evidence.get("fixture_origin"))
    if synthetic and state.get("operating"):
        raise ValueError("FIXTURE_ORIGIN_CANNOT_MUTATE_OPERATING_STATE")
    promotion = requested_to in PROMOTION_TARGETS.get(dimension, set())
    if synthetic and promotion:
        raise ValueError("FIXTURE_ORIGIN_CANNOT_PROMOTE_ANY_DIMENSION")
    status = "APPLIED_CANDIDATE_ONLY"
    target = requested_to
    hold = None
    special_promotion = (
        (dimension == "authority" and requested_to in {"OWNER_ADOPTED", "NATIVE_ISSUED"})
        or (dimension == "human" and requested_to in {"PROVEN", "HUMAN_A5", "A5_GREEN"})
        or (dimension == "science" and requested_to in {"ORIGINAL_ISSUED", "NATIVE_ISSUED", "ISSUED"})
    )
    if requested_to not in ALLOWED_TRANSITIONS[dimension] and not special_promotion:
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
    if promotion and dimension not in {"authority", "human", "science"} and evidence["kind"] != "SOURCEFREE_REVIEW":
        hold = _acceptance_request(state, node_id, dimension, evidence)
        if not hold["accepted"]:
            target = state["axes"][node_id].get(dimension)
            status = hold["status"]
        else:
            target = requested_to
            status = hold["status"]
    if evidence["kind"] == "SOURCEFREE_REVIEW":
        reviewed_sha = str(evidence.get("reviewed_sha") or "")
        if not reviewed_sha or _git(["cat-file", "-t", reviewed_sha]) != "commit":
            raise ValueError("REVIEWED_SHA_NOT_FOUND")
        if str(evidence.get("review_status") or "").upper() == "FAIL":
            target = "REVIEW_FAILED"
            status = "APPLIED_CANDIDATE_ONLY"
        elif promotion or dimension in {"review", "engineering"}:
            hold = _acceptance_request(state, node_id, dimension, evidence)
            if not hold["accepted"]:
                target = state["axes"][node_id].get(dimension)
                status = hold["status"]
            else:
                target = requested_to
                status = hold["status"]
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
    if synthetic:
        status = "SIMULATED_NOT_ADOPTED"
    old = state["axes"][node_id].get(dimension)
    pending = status == "PENDING_INDEPENDENT_ACCEPTANCE"
    if not pending:
        state["axes"][node_id][dimension] = target
        if dimension == "authority" and hold and hold.get("authority_state"):
            state["axes"][node_id]["authority"] = hold["authority_state"]
        if dimension == "human" and hold and hold.get("human_state"):
            state["axes"][node_id]["human"] = hold["human_state"]
        if dimension == "science" and hold and hold.get("science_state"):
            state["axes"][node_id]["science"] = hold["science_state"]
    negative = (not pending) and (_is_negative(dimension, target) or (dimension == "review" and target == "REVIEW_FAILED"))
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
    elif not pending:
        affected = sorted({
            e["to"] for e in state["edges"]
            if e["from"] == node_id and not e.get("hypothetical")
        })
        before = {nid: state["axes"].get(nid, {}).get("consumer") for nid in state["axes"]}
        _recompute_consumer_grades(state)
        restored = sorted(
            nid for nid, value in before.items()
            if str(value).startswith("INVALIDATED") and not str(state["axes"].get(nid, {}).get("consumer", "")).startswith("INVALIDATED")
        )
    digest = _evidence_digest(evidence)
    history_id = "H%04d" % (len(state["history"]) + 1)
    record = {
        "history_id": history_id,
        "kind": "AUTHORIZED_TRANSITION" if status.startswith("APPLIED") else "TRANSITION_HOLD",
        "node_id": node_id,
        "dimension": dimension,
        "from": old,
        "to": target if not pending else old,
        "requested_to": requested_to,
        "status": status,
        "evidence_digest": digest,
        "evidence_kind": evidence["kind"],
        "invalidated": invalidated,
        "affected": affected,
        "restored": restored,
        "pyat_boundary_touched": False,
        "authority_hold": hold if not (hold and hold.get("accepted")) else None,
        "acceptance": hold.get("acceptance") if hold and hold.get("accepted") else None,
        "source_cut": state.get("source_snapshot", {}).get("read_at", "UNKNOWN"),
        "withdrawal": withdrawal,
    }
    state["history"].append(record)
    if hold and not hold.get("accepted"):
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
    state["freshness"]["generated_at"] = state.get("logical_time") or _utc_now()
    _recompute(state)
    return {
        "status": status,
        "history_id": history_id,
        "node_id": node_id,
        "dimension": dimension,
        "from": old,
        "to": target if not pending else old,
        "requested_to": requested_to,
        "invalidated": invalidated,
        "affected": affected,
        "restored": restored,
        "authority_hold": hold if not (hold and hold.get("accepted")) else None,
        "acceptance": hold.get("acceptance") if hold and hold.get("accepted") else None,
        "withdrawal": withdrawal,
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
    actual_digest = _digest(patch)
    if patch_digest and patch_digest != actual_digest:
        raise ValueError(f"OSCIENCE_PATCH_DIGEST_MISMATCH:{actual_digest}!={patch_digest}")
    digest = actual_digest
    if digest in state.get("evidence_imports", {}):
        state["history"].append({
            "history_id": "H%04d" % (len(state["history"]) + 1),
            "kind": "DUPLICATE_IMPORT_NOOP",
            "evidence_digest": digest,
            "read_at": state.get("logical_time") or _utc_now(),
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
        "imported_at": state.get("logical_time") or _utc_now(),
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
        "read_at": state.get("logical_time") or _utc_now(),
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


def _verify_return_locator(source: dict, locator: Any) -> tuple[bool, str, dict]:
    if not isinstance(locator, dict):
        return False, "NO_LOCATOR", {}
    commit = str(source.get("commit") or "")
    path = str(locator.get("path") or source.get("path") or "")
    quote = str(locator.get("quote") or "").strip()
    if not commit or not path or not quote:
        return False, "LOCATOR_INCOMPLETE", {}
    ok, reason = _verify_git_object({"commit": commit, "path": path, "object_type": "blob"})
    if not ok:
        return False, "LOCATOR_OBJECT_INVALID:" + reason, {}
    body = _git(["show", f"{commit}:{path}"]) or ""
    if quote not in body:
        return False, "LOCATOR_QUOTE_NOT_FOUND", {}
    line_start = locator.get("line_start")
    line_end = locator.get("line_end")
    if line_start is not None:
        start_line = max(1, int(line_start))
        end_line = int(line_end) if line_end is not None else start_line
        selected = "\n".join(body.splitlines()[start_line - 1:end_line])
        if quote not in selected:
            return False, "LOCATOR_LINE_RANGE_MISMATCH", {}
    blob = _git(["rev-parse", f"{commit}:{path}"]) or ""
    return True, "LOCATOR_VERIFIED", {
        "commit": commit,
        "path": path,
        "blob": blob,
        "quote": quote,
        "line_start": line_start,
        "line_end": line_end,
    }


def _claim_evidence_status(source: dict, spec: dict, fixture: dict) -> tuple[str, bool, dict, str]:
    locator = spec.get("locator") or spec.get("evidence_locator") or fixture.get("locator")
    ok, reason, verified = _verify_return_locator(source, locator)
    if ok:
        return "SOURCE_LOCATED", True, verified, reason
    if fixture.get("hq_inference") and str(fixture.get("inference_rationale") or "").strip():
        return "HQ_INFERENCE", False, {}, reason
    return "CALLER_CLAIM_UNVERIFIED", False, {}, reason


def intake_candidate(state: dict, fixture: dict) -> dict:
    """Ingest a real returned artifact as candidate evidence; never auto-promote.

    A real exact return SHA is required and must be the source commit.  Caller
    requirements, gaps and node updates are source-backed only when an exact
    locator/quote inside that return verifies.  Otherwise they remain visible as
    caller-claimed or HQ-inferred, never as verified source work.
    """
    if fixture.get("schema", "").startswith("SOROK_PROGRAMMA_O_SCIENCE") or fixture.get("kind") == "OSCIENCE_PATCH":
        return ingest_oscience(state, fixture)
    sha = str(fixture.get("sha") or "")
    source = fixture.get("source") if isinstance(fixture.get("source"), dict) else {}
    synthetic = bool(fixture.get("fixture_origin")) or not _sha40(sha)
    source_ok = False
    source_reason = "NO_SOURCE"
    if not synthetic:
        if _git(["cat-file", "-t", sha]) != "commit":
            source_ok = False
            source_reason = "RETURN_SHA_NOT_A_REAL_COMMIT"
        elif source:
            source_ok, source_reason = _verify_git_object(source)
            if source_ok and str(source.get("commit") or "") != sha:
                source_ok = False
                source_reason = "RETURN_SHA_SOURCE_COMMIT_MISMATCH"
        else:
            source_ok = True
            source_reason = "RETURN_COMMIT_VERIFIED_NO_PAYLOAD_PATH"
            source = {"commit": sha, "object_type": "commit"}
    if synthetic or not source_ok:
        item = {
            "kind": "QUARANTINED_INTAKE_ATTACK",
            "return_id": fixture.get("id", "UNKNOWN"),
            "sha": sha,
            "status": "QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE",
            "reason": "SYNTHETIC_OR_UNVERIFIABLE_RETURN" if synthetic else source_reason,
            "claimed_tests": fixture.get("tests", {}),
            "read_at": state.get("logical_time") or _utc_now(),
        }
        state.setdefault("quarantined_intake", []).append(item)
        _recompute(state)
        return item
    item = {
        "history_id": "H%04d" % (len(state["history"]) + 1),
        "kind": "INTAKE_RETURN_CANDIDATE",
        "return_id": fixture.get("id", "UNKNOWN"),
        "source": fixture.get("branch", ""),
        "sha": sha,
        "source_ref": source,
        "source_verification": source_reason,
        "status": "CANDIDATE_NOT_PROMOTED",
        "claimed_tests": fixture.get("tests", {}),
        "evidence": fixture.get("evidence", {}),
        "source_backed_claims": [],
        "unverified_claims": [],
        "read_at": state.get("logical_time") or _utc_now(),
    }
    state["history"].append(item)
    gap_spec = fixture.get("gap")
    if gap_spec:
        gap = _gap_record(dict(gap_spec))
        status, backed, locator, reason = _claim_evidence_status(source, gap_spec, fixture)
        gap.setdefault("class", "UNREPRESENTED_REQUIREMENT")
        gap.setdefault("blockers", [])
        gap.setdefault("impact", {"downstream_required_count": 0, "affected_l0": [], "affected_sectors": []})
        gap.setdefault("parallel_group", "DISCOVERED_REQUISITE")
        gap.update({
            "evidence_status": status,
            "source_backed": backed,
            "evidence_locator": locator,
            "locator_reason": reason,
            "return_sha": sha,
            "inference_rationale": fixture.get("inference_rationale") if status == "HQ_INFERENCE" else "",
        })
        state.setdefault("intake_gaps", []).append(gap)
        item["new_gap"] = gap["id"]
        (item["source_backed_claims"] if backed else item["unverified_claims"]).append(gap["id"])
    elif fixture.get("new_requirement"):
        rid = fixture["new_requirement"]
        status, backed, locator, reason = _claim_evidence_status(source, fixture, fixture)
        gap = {
            "id": "GAP_" + rid,
            "new_gap": "GAP_" + rid,
            "domain": "DISCOVERED_REQUISITE",
            "node": rid,
            "class": "UNREPRESENTED_REQUIREMENT",
            "status": "UNREPRESENTED_REQUIREMENT",
            "owner": "UNKNOWN",
            "next": "Assign source, competent owner and actual consumer.",
            "consequence": "Visible unrepresented requirement.",
            "missing_stages": ["T", "A", "E", "C", "V"],
            "parent_obligation": "Discovered requirement from a real return.",
            "smallest_useful_next_action": "Assign source, competent owner and actual consumer.",
            "falsifier": "The requirement remains ungrounded or has no consumer.",
            "blockers": [],
            "impact": {"downstream_required_count": 0, "affected_l0": [], "affected_sectors": []},
            "parallel_group": "DISCOVERED_REQUISITE",
            "hq_judgment_required": True,
            "evidence_status": status,
            "source_backed": backed,
            "evidence_locator": locator,
            "locator_reason": reason,
            "return_sha": sha,
            "inference_rationale": fixture.get("inference_rationale") if status == "HQ_INFERENCE" else "",
        }
        state.setdefault("intake_gaps", []).append(gap)
        item["new_gap"] = gap["id"]
        (item["source_backed_claims"] if backed else item["unverified_claims"]).append(gap["id"])
    for update in fixture.get("node_updates", []):
        nid = update.get("id")
        if not nid:
            continue
        status, backed, locator, reason = _claim_evidence_status(source, update, fixture)
        if nid not in _node_map(state):
            if not backed:
                item["unverified_claims"].append("NODE:" + nid)
                continue
            state["nodes"].append({
                "id": nid,
                "layer": update.get("layer", "L2"),
                "kind": update.get("kind", "DISCOVERED_REQUIREMENT"),
                "title": update.get("title", nid),
                "status": "CANDIDATE_EVIDENCE",
                "source": update.get("source") or source,
                "source_refs": [source] if source else [],
                "hq_judgment_required": True,
            })
            state["axes"][nid] = _empty_axes_for_node({"id": nid})
        if backed:
            state["axes"][nid].update({"operational": "CANDIDATE_EVIDENCE"})
            item["source_backed_claims"].append("NODE:" + nid)
        else:
            item["unverified_claims"].append("NODE:" + nid)
        state.setdefault("node_evidence", {}).setdefault(nid, []).append({
            "kind": "RETURN_CANDIDATE_EVIDENCE",
            "evidence": update.get("evidence"),
            "evidence_status": status,
            "source_backed": backed,
            "evidence_locator": locator,
            "locator_reason": reason,
            "return_sha": sha,
            "history_id": item["history_id"],
        })
    for edge in fixture.get("edges", []):
        if edge.get("from") not in _node_map(state) or edge.get("to") not in _node_map(state):
            raise ValueError("INTAKE_EDGE_ENDPOINT_UNKNOWN")
        status, backed, locator, reason = _claim_evidence_status(source, edge, fixture)
        if not backed:
            item["unverified_claims"].append("EDGE:" + str(edge.get("from")) + "->" + str(edge.get("to")))
            continue
        candidate = _classify_edge(edge)
        candidate["evidence_status"] = status
        candidate["source_backed"] = True
        candidate["evidence_locator"] = locator
        candidate["return_sha"] = sha
        if candidate["edge_id"] not in {e["edge_id"] for e in state["edges"]}:
            state["edges"].append(candidate)
            item["source_backed_claims"].append("EDGE:" + candidate["edge_id"])
    _recompute(state)
    return item


def generate_html(state: dict, output: Path) -> Path:
    home = home_view(state)
    gaps = state.get("whole_program_gaps", whole_program_gaps(state))
    nodes = _node_map(state)
    rows = []
    for node in sorted(state["nodes"], key=lambda n: n["id"]):
        if not node.get("programma_p1"):
            continue
        mat = maturity_view(state, node["id"])["stages"]
        chips = " ".join(f"<b>{k}</b>:{escape(str(v.get('status', 'UNKNOWN')))}" for k, v in mat.items())
        rows.append(
            f"<tr id='{escape(node['id'])}'><td><code>{escape(node['id'])}</code></td>"
            f"<td>{escape(str(node.get('title', '')))}</td>"
            f"<td>{escape(str(node.get('owner', '')))}</td>"
            f"<td>{escape(chips)}</td>"
            f"<td>{escape(str(node.get('status', '')))}</td></tr>"
        )
    gap_rows = []
    for group in gaps.get("groups", []):
        for gap in group.get("gaps", []):
            gap_rows.append(
                f"<tr><td><code>{escape(gap['id'])}</code></td><td>{escape(gap.get('domain', ''))}</td>"
                f"<td>{escape(str(gap.get('status', '')))}</td><td>{escape(','.join(gap.get('missing_stages', [])))}</td>"
                f"<td>{escape(str(gap.get('owner', '')))}</td><td>{escape(str(gap.get('smallest_useful_next_action', '')))}</td>"
                f"<td>{escape(str(gap.get('falsifier', '')))}</td></tr>"
            )
    purpose = home["purpose"]
    experience = home["intended_human_experience"]
    constraints = home["constraints_100_101"]
    def brief(item: dict) -> str:
        source = item.get("source") or {}
        quote = source.get("quote") or ""
        return (
            f"<h3>{escape(str(item.get('title') or item.get('id')))}</h3>"
            f"<p>{escape(str(item.get('summary') or ''))}</p>"
            f"<p><b>Status:</b> {escape(str(item.get('status') or 'UNKNOWN'))}; "
            f"<b>Source:</b> <code>{escape(str(source.get('commit') or 'UNKNOWN'))}</code> "
            f"<code>{escape(str(source.get('path') or ''))}</code></p>"
            + (f"<blockquote>{escape(str(quote))}</blockquote>" if quote else "")
        )
    witness_rows = ''.join(
        f"<tr><td><code>{escape(x['id'])}</code></td><td>{escape(str(x.get('title') or ''))}</td>"
        f"<td>{escape(str(x.get('status') or ''))}</td><td>{escape(str(x.get('reason') or ''))}</td></tr>"
        for x in home.get("source_witness", [])
    )
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>PROGRAMMA SOROK living reference</title>
<style>body{{font:14px/1.45 -apple-system,system-ui,sans-serif;margin:24px;max-width:1400px}}table{{border-collapse:collapse;width:100%;margin:12px 0}}td,th{{border:1px solid #ccc;padding:4px;vertical-align:top}}code{{font-size:12px}}.notice{{background:#fff3cd;padding:8px;border:1px solid #d39e00}}blockquote{{border-left:3px solid #999;margin:8px 0;padding-left:12px;color:#333}}</style></head><body>
<h1>PROGRAMMA SOROK — living reference</h1>
<h2>Purpose: meet an unchosen neighbor</h2>
{brief(purpose)}
<h2>Intended human experience</h2>
{brief(experience['astra_b_scene'])}
{brief(experience['astra_d_longitudinal'])}
{brief(experience['negative_controls'])}
<h2>100/101 product constraints</h2>
{brief(constraints['alpha_100'])}
{brief(constraints['binding_101'])}
{brief(constraints['two_call_proposal'])}
{brief(constraints['hidden_interiority'])}
<p class="notice">{escape(home['status'])} — {escape(home['whole_scope'])}. {escape(home['notice'])}</p>
<p>{escape(home['one_paragraph'])}</p>
<p><b>Kernel:</b> {escape(home['kernel'])}</p>
<h2>Terminal obligations</h2><table><tr><th>ID</th><th>Obligation</th><th>Status</th><th>Missing</th><th>Owner</th></tr>
{''.join(f"<tr><td><code>{escape(x['id'])}</code></td><td>{escape(x['obligation'])}</td><td>{escape(x['status'])}</td><td>{escape(','.join(x['missing_stages']))}</td><td>{escape(x['owner'])}</td></tr>" for x in home['terminal_obligations'])}
</table>
<h2>Source witness status</h2><table><tr><th>ID</th><th>Title</th><th>Status</th><th>Reason</th></tr>{witness_rows}</table>
<h2>Whole-Program Gaps</h2><p>Count {gaps['count']}; independently actionable {gaps['independently_actionable']}; blocked {gaps['blocked']}. No completeness denominator.</p>
<table><tr><th>ID</th><th>Domain</th><th>Status</th><th>Missing</th><th>Owner</th><th>Next action</th><th>Falsifier</th></tr>{''.join(gap_rows)}</table>
<h2>Objects and maturity</h2><table><tr><th>ID</th><th>Title</th><th>Owner</th><th>I/T/A/E/C/V</th><th>Status</th></tr>{''.join(rows)}</table>
<p>Generated from the same persisted state as the CLI. Source counts are not progress. Missing edges remain visible. Local hashes are not external custody.</p>
</body></html>
"""
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    return target


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
    print(json.dumps(value, indent=2, sort_keys=False))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=STATE)
    parser.add_argument("--snapshot", type=Path, default=None)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("refresh", "overview", "home", "work-now", "workers", "coverage", "export", "owners", "journal", "verify-journal", "verify-sources", "rebuild", "recover", "demo-isolation"):
        sub.add_parser(name)
    for name in ("source", "consumer", "alternatives", "history", "critical-path", "blocked-chain", "maturity", "lateral", "code", "evidence"):
        p = sub.add_parser(name); p.add_argument("id")
    z = sub.add_parser("zoom"); z.add_argument("id"); z.add_argument("--depth", type=int, default=1)
    f = sub.add_parser("focus"); f.add_argument("id"); f.add_argument("--depth", type=int, default=1)
    g = sub.add_parser("gaps"); g.add_argument("--domain", default="")
    wg = sub.add_parser("whole-gaps"); wg.add_argument("--stage", default=""); wg.add_argument("--domain", default="")
    h = sub.add_parser("html"); h.add_argument("--output", type=Path, default=ROOT / "programma_home.html")
    i = sub.add_parser("intake-return"); i.add_argument("file", type=Path)
    wd = sub.add_parser("withdrawal"); wd.add_argument("file", type=Path)
    o = sub.add_parser("ingest-oscience"); o.add_argument("file", type=Path, nargs="?")
    for name in ("apply-authorized-transition", "commit-transition"):
        a = sub.add_parser(name); a.add_argument("file", type=Path)
    args = parser.parse_args(argv)
    state_path = args.state
    snapshot_path = args.snapshot
    if args.command == "refresh":
        if _journal_path(state_path).exists():
            body = _event("SOURCE_CUT_REFRESH", {"observed": observe_source_cut()})
            _print(commit_event(body, journal_path=_journal_path(state_path), state_path=state_path, snapshot_path=snapshot_path))
            return 0
        existing = _load_state(state_path) if state_path.exists() else None
        state = refresh_state(existing, observe_source_cut())
        _save(state, state_path, snapshot_path, expected_revision=int((existing or {}).get("revision") or 0))
        _print(_overview(state))
        return 0
    if args.command == "journal":
        _print(journal_summary(_journal_path(state_path)))
        return 0
    if args.command == "verify-journal":
        try:
            events = evidence_store.read_journal(_journal_path(state_path))
            _check_journal_regression(events, state_path)
            state = rebuild_from_journal(_journal_path(state_path), operating=True)
            _print({"result": "PASS", "events": len(events), "head": state.get("journal_head"), "state_digest": state.get("state_digest")})
            return 0
        except (evidence_store.JournalError, ValueError) as error:
            _print({"result": "FAIL", "reason": str(error)})
            return 1
    if args.command == "rebuild":
        try:
            events = evidence_store.read_journal(_journal_path(state_path))
            _check_journal_regression(events, state_path)
            state = rebuild_from_journal(_journal_path(state_path), operating=True)
            _save(state, state_path, snapshot_path, revision=int(state.get("revision") or 0))
            _print({"result": "REBUILT", "revision": state.get("revision"), "journal_head": state.get("journal_head"), "state_digest": state.get("state_digest")})
            return 0
        except (evidence_store.JournalError, ValueError) as error:
            _print({"result": "FAIL", "reason": str(error)})
            return 1
    if args.command == "recover":
        state = _load_state(state_path, recover=True)
        _save(state, state_path, snapshot_path)
        _print({"result": "RECOVERED", "revision": state.get("revision"), "state_digest": state.get("state_digest")})
        return 0
    if args.command == "demo-isolation":
        import r2_live_transaction
        _print(r2_live_transaction.demo_isolation())
        return 0
    state = _load_state(state_path)
    if args.command == "overview":
        _print(_overview(state))
    elif args.command == "home":
        _print(home_view(state))
    elif args.command == "zoom":
        if args.id not in _node_map(state):
            _print({"error": "UNKNOWN_ID"})
            return 1
        nodes, edges = _neighbors(state, args.id, args.depth)
        _print({"root": args.id, "depth": args.depth, "nodes": nodes, "edges": edges})
    elif args.command == "focus":
        _print(focus_view(state, args.id, args.depth))
    elif args.command == "lateral":
        _print(lateral_view(state, args.id))
    elif args.command == "maturity":
        _print(maturity_view(state, args.id))
    elif args.command == "code":
        _print(code_consumer_view(state, args.id))
    elif args.command == "evidence":
        _print(evidence_view(state, args.id))
    elif args.command == "gaps":
        _print([g for g in state["gaps"] if not args.domain or g["domain"] == args.domain])
    elif args.command == "whole-gaps":
        _print(whole_program_gaps(state, args.stage, args.domain))
    elif args.command == "owners":
        _print(owners_view(state))
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
        _print(code_consumer_view(state, args.id))
    elif args.command == "alternatives":
        row = next((x for x in state["source_manifest"]["rows"] if x["id"] == args.id), None)
        ws = next((x for x in state.get("workstreams", []) if x["id"] == args.id), None)
        _print({"id": args.id, "row": (row or {}).get("unresolved_alternatives", []), "workstream": ws, "lateral": lateral_view(state, args.id)})
    elif args.command == "workers":
        _print({"workers": state["workers"], "source_snapshot": state.get("source_snapshot"), "caution": "Git branch does not prove running process; missing local process is not owner absence."})
    elif args.command == "coverage":
        _print(state["coverage"])
    elif args.command == "history":
        _print([h for h in state["history"] if h.get("history_id") == args.id or h.get("node_id") == args.id])
    elif args.command == "export":
        _print(state)
    elif args.command == "html":
        _print({"output": str(generate_html(state, args.output)), "nodes": len(state["nodes"]), "gaps": state.get("whole_program_gaps", {}).get("count")})
    elif args.command == "verify-sources":
        _print(verify_source_refs(state))
    elif args.command == "intake-return":
        fixture = _load(args.file)
        if fixture.get("schema", "").startswith("SOROK_PROGRAMMA_O_SCIENCE"):
            result = ingest_oscience(state, fixture)
            _save(state, state_path, snapshot_path)
            _print(result)
        else:
            body = _event("RETURN_INTAKE", fixture, source=fixture.get("source") or {})
            _print(commit_event(body, journal_path=_journal_path(state_path), state_path=state_path, snapshot_path=snapshot_path))
    elif args.command == "withdrawal":
        fixture = _load(args.file)
        body = _event("EVIDENCE_WITHDRAWAL", fixture, source=fixture.get("source") or {})
        _print(commit_event(body, journal_path=_journal_path(state_path), state_path=state_path, snapshot_path=snapshot_path))
    elif args.command == "ingest-oscience":
        patch = _load(args.file or OSCIENCE_PATCH)
        body = _event("CANDIDATE_EVIDENCE", {
            "importer": "OSCIENCE",
            "patch_file": str((args.file or OSCIENCE_PATCH).name),
            "patch_digest": _digest(patch),
            "source_commit": OSCIENCE_CUT,
        })
        _print(commit_event(body, journal_path=_journal_path(state_path), state_path=state_path, snapshot_path=snapshot_path))
    elif args.command in {"apply-authorized-transition", "commit-transition"}:
        fixture = _load(args.file)
        body = _event("TRANSITION_REQUEST", {"fixture": fixture}, source=(fixture.get("evidence") or {}).get("source") or {})
        _print(commit_event(body, journal_path=_journal_path(state_path), state_path=state_path, snapshot_path=snapshot_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
