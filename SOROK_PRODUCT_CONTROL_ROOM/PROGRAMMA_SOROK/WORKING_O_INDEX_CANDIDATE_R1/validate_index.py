#!/usr/bin/env python3
"""Validate the sourcefree Programma Sorok O-INDEX candidate.

The validator checks the Sorok denominator, exact S0-S16 holds, the separate
Pyat N0-N12/F1-F8 namespace, four returned assets, L0-L5 link closure, backward
paths, three traversals, owner slots and the no-native/no-priority ceiling. It
reads JSON and Markdown only; it does not import, execute or adopt candidate
code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

HEX40 = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_KINDS = {
    "TERMINAL_C_A": 19,
    "HISTORIC_V3_MECHANISM": 40,
    "SOROK_NEO_REQUIREMENT": 12,
    "ORIGINAL_SCIENCE_OWNER_DECISION": 16,
    "NAMED_FIRST_CONSUMER_EDGE": 15,
    "DECLARED_S0_S16_WORKSTREAM": 17,
    "NEW_FOUR_RETURN_CODE_ASSET": 4,
}
FOUR = {
    "CP-A5-R2": "913765328e4fab12b150ea01421ed6b445158184",
    "C9C12-R2": "c78404724052496fdec8608c8b0e833c0f7c4ecc",
    "B-F1CR-R2": "bf3273c294c704ad7c631559b9866d351bb4f103",
    "V3CORE-R1": "b5cb3f917402b992d7cbe933af0b378d2b37cbfd",
}
PYAT_IDS = {
    *(f"PYAT_N{index}" for index in range(8)),
    "PYAT_N8E",
    "PYAT_N8S",
    "PYAT_N9",
    "PYAT_N10E",
    "PYAT_N10W",
    "PYAT_N11",
    "PYAT_N12",
    *(f"PYAT_F{index}" for index in range(1, 9)),
}
EXPECTED_SOROK_IDS = {
    *(f"C{index}" for index in range(13)),
    *(f"A{index}" for index in range(6)),
    *(f"M{index:02d}" for index in range(1, 41)),
    *(f"N{index:02d}" for index in range(1, 13)),
    *(f"O{index:02d}" for index in range(1, 17)),
    *(f"E{index:02d}" for index in range(1, 16)),
    *(f"S{index}" for index in range(17)),
    *(f"RCFB_E{index}" for index in range(1, 11)),
    "F1C_ORIGINAL",
    "F1CR_CLAIMED_PATCH",
    "F1CR_R5_RECONSTRUCTION",
    "B1",
    "B2",
    "B3",
    "B3A",
    "B3AS",
    "BP2P4J",
    "S39_S52",
    "R15_V2",
    *FOUR,
}
ALLOWED_STATUS = {
    "SOURCE_PRESENT",
    "ORIGINAL_PENDING",
    "CANDIDATE_ONLY",
    "INDEPENDENT_ACCEPT_SCOPED",
    "NATIVE_ISSUED",
    "UNKNOWN",
}
ALLOWED_CLAIM_EPOCHS = {
    "R7_HISTORICAL_BASELINE",
    "R7_EXACT_HOLD",
    "POST_R6",
    "POST_R7_INTAKE",
    "PRE_MAIN_ADVISORY_ATLAS",
}
GRADE_FIELDS = ("engineering_grade", "science_grade", "authority_grade", "human_grade")


class ValidationError(AssertionError):
    """The candidate violates a declared O-INDEX invariant."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def _load(path: Path) -> dict[str, Any]:
    _require(path.is_file(), f"missing {path.name}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _check_cycle_edges(edges: list[dict[str, Any]], node_ids: set[str]) -> list[list[str]]:
    graph: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for edge in edges:
        graph[edge["from"]].append((edge["to"], edge))
    state: dict[str, int] = {}
    allowed_cycles: list[list[str]] = []

    def visit(node: str, path: list[str]) -> None:
        state[node] = 1
        for target, edge in graph.get(node, []):
            if state.get(target, 0) == 0:
                visit(target, path + [target])
            elif state.get(target) == 1:
                start = path.index(target)
                cycle = path[start:] + [target]
                cycle_edges = []
                for left, right in zip(cycle, cycle[1:]):
                    cycle_edges.extend(item[1] for item in graph[left] if item[0] == right)
                if not all(item.get("cycle_class") or item.get("mutual") for item in cycle_edges):
                    raise ValidationError(f"unmarked circular dependency: {' -> '.join(cycle)}")
                allowed_cycles.append(cycle)
        state[node] = 2

    for node in sorted(node_ids):
        if state.get(node, 0) == 0:
            visit(node, [node])
    return allowed_cycles


def validate(root: Path) -> dict[str, Any]:
    """Return a deterministic validation report or raise ValidationError."""

    checks: list[str] = []
    registry = _load(root / "01_SOURCE_OF_TRUTH_REGISTRY.json")
    orchestration = _load(root / "02_L0_L5_LINKED_ORCHESTRATION_INDEX.json")
    slots = _load(root / "04_UNDECIDED_SCIENCE_DEPENDENCY_AND_OWNER_SLOTS.json")
    for name in (
        "00_START_HERE.md",
        "03_RECOVERY_AND_FOUR_RETURN_ASSET_INDEX.md",
        "05_VALIDATOR_AND_READBACK.md",
        "validate_index.py",
    ):
        _require((root / name).is_file(), f"missing {name}")

    rows = registry["rows"]
    _require(len(rows) == 144, f"expected 144 Sorok rows, got {len(rows)}")
    ids = [row["id"] for row in rows]
    _require(len(ids) == len(set(ids)), "duplicate Sorok registry id")
    _require(set(ids) == EXPECTED_SOROK_IDS, f"Sorok id set mismatch: missing={sorted(EXPECTED_SOROK_IDS - set(ids))} extra={sorted(set(ids) - EXPECTED_SOROK_IDS)}")
    checks.append("144 unique Sorok rows with exact inherited id set")

    kinds: dict[str, int] = {}
    for row in rows:
        kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1
    for kind, expected in EXPECTED_KINDS.items():
        _require(kinds.get(kind) == expected, f"{kind}: expected {expected}, got {kinds.get(kind)}")
    checks.append("19 C/A + 40 M + 12 N + 16 O + 15 E + 17 S + 4 returned assets")

    coverage = registry["coverage"]
    for key, expected in (("C_A", "19/19"), ("M", "40/40"), ("Neo_N", "12/12"), ("O", "16/16"), ("E", "15/15")):
        _require(coverage.get(key) == expected, f"coverage {key} is {coverage.get(key)}")
    _require("0/17" in coverage.get("S0_S16", ""), "S0-S16 coverage must state the exact 0/17 hold")
    checks.append("declared coverage and exact S0-S16 hold")

    metadata = registry.get("source_cut_metadata", {})
    _require(len(metadata) >= 10, "source cut metadata incomplete")
    for row in rows:
        _require(bool(row.get("first_consumer")), f"{row['id']}: empty first_consumer")
        _require(row.get("native_product_accepted") is not True, f"{row['id']}: native promotion")
        _require(row.get("source_science_issued") is not True, f"{row['id']}: science issuance")
        _require(row.get("status_class") in ALLOWED_STATUS, f"{row['id']}: invalid status_class")
        _require(row.get("claim_epoch") in ALLOWED_CLAIM_EPOCHS, f"{row['id']}: untyped claim epoch")
        for field in GRADE_FIELDS:
            _require(isinstance(row.get(field), str) and bool(row[field]), f"{row['id']}: missing {field}")
        for field in ("owner", "owner_type", "current_creator", "direct_consumer", "next_evidence", "source_currentness"):
            _require(isinstance(row.get(field), str) and bool(row[field]), f"{row['id']}: missing {field}")
        _require(isinstance(row.get("unresolved_alternatives"), list) and bool(row["unresolved_alternatives"]), f"{row['id']}: missing unresolved alternatives")
        _require(row["status_class"] != "NATIVE_ISSUED", f"{row['id']}: native-issued claim without native acceptance")
        _require(row["science_grade"] not in ("ISSUED", "NATIVE_ISSUED"), f"{row['id']}: contradictory science grade")
        source = row.get("evidence_source")
        if row["kind"] == "DECLARED_S0_S16_WORKSTREAM":
            _require(source is None, f"{row['id']}: S hold must not fabricate source")
            _require(row["status"].startswith("RECOVERY_EXACT_HOLD"), f"{row['id']}: S hold status")
            _require(row["first_consumer"] == "UNKNOWN", f"{row['id']}: S hold consumer")
            _require(row["status_class"] == "UNKNOWN", f"{row['id']}: S status class")
        else:
            _require(isinstance(source, dict), f"{row['id']}: missing evidence source")
            commit = source.get("commit", "")
            _require(bool(HEX40.match(commit)), f"{row['id']}: source commit")
            _require(bool(source.get("path")), f"{row['id']}: source path")
            _require(commit in metadata and metadata[commit].get("timestamp"), f"{row['id']}: source time/currentness")
    checks.append("no native/science promotion; every row has typed owner, grades, epoch and source time")

    four = {row["id"]: row for row in rows if row["kind"] == "NEW_FOUR_RETURN_CODE_ASSET"}
    _require(set(four) == set(FOUR), "four returned asset set")
    for asset_id, commit in FOUR.items():
        _require(four[asset_id]["evidence_source"]["commit"] == commit, f"{asset_id}: commit")
        _require(four[asset_id]["status"] == "SOURCE_FOUND_ADAPTER_AUTHOR_TESTED__UNADOPTED", f"{asset_id}: adoption")
        _require(four[asset_id]["status_class"] == "CANDIDATE_ONLY", f"{asset_id}: maturity inflation")
        _require(four[asset_id]["claim_epoch"] == "POST_R7_INTAKE", f"{asset_id}: claim epoch")
    checks.append("four returned assets pinned, post-R7, candidate-only and unadopted")

    r6 = registry["r6_source_close"]
    _require(r6["rows"] == 39 and r6["files_read"] == 94, "R6 39/94 close")
    _require(r6["candidate_files"] == 94, "R6 candidate file count")
    _require(sum(r6["dispositions"].values()) == 39, "R6 disposition total")
    _require(r6["dispositions"]["UNRECOVERABLE_EXACT"] == 0, "R6 exact unrecoverable")
    _require(r6["material_function_count"] == 9, "R6 nine material families")
    _require(r6["r41"]["pinned_files"] == 133, "R41 133 pinned files")
    _require(r6["r41"]["selected_tests"] == 26, "R41 26 selected tests")
    _require(r6.get("claim_epoch") == "POST_R6", "R6 claim epoch")
    checks.append("R6 39 rows / 94 files / 9 material families / R41 133 and 26")

    pyat = registry["pyat_namespace"]
    pyat_rows = pyat["rows"]
    _require(len(pyat_rows) == 23, f"expected 23 Pyat rows, got {len(pyat_rows)}")
    _require({row["id"] for row in pyat_rows} == PYAT_IDS, "Pyat N0-N12/F1-F8 id set")
    _require(pyat.get("actor_psyche_created") is False, "Pyat actor psyche created")
    _require(not (set(ids) & PYAT_IDS), "Pyat/Sorok id collision")
    for row in pyat_rows:
        _require(row["namespace"] == "PYAT", f"{row['id']}: namespace")
        source = row.get("source", {})
        _require(bool(HEX40.match(source.get("commit", ""))), f"{row['id']}: source commit")
        _require(bool(source.get("path")), f"{row['id']}: source path")
        _require(bool(HEX40.match(source.get("blob", ""))), f"{row['id']}: source blob")
        _require(source["commit"] in metadata and metadata[source["commit"]].get("timestamp"), f"{row['id']}: source time")
        _require(row.get("status_class") in ALLOWED_STATUS, f"{row['id']}: status")
        _require(row.get("claim_epoch") in ALLOWED_CLAIM_EPOCHS, f"{row['id']}: claim epoch")
        _require(row.get("native_product_accepted") is not True and row.get("source_science_issued") is not True, f"{row['id']}: native/science promotion")
        for field in ("owner", "owner_type", "direct_consumer", "next_evidence", "science_grade", "authority_grade"):
            _require(isinstance(row.get(field), str) and bool(row[field]), f"{row['id']}: missing {field}")
    _require("PYAT_N11" in {row["id"] for row in pyat_rows} and "PYAT_N12" in {row["id"] for row in pyat_rows}, "Pyat N11/N12 missing")
    checks.append("separate Pyat N0-N12/F1-F8 rows, no actor psyche, no id collision")

    nodes = orchestration["nodes"]
    node_ids = [node["id"] for node in nodes]
    _require(len(node_ids) == len(set(node_ids)), "duplicate orchestration node")
    _require(set(ids).issubset(set(node_ids)), "Sorok item missing from L0-L5 nodes")
    _require(PYAT_IDS.issubset(set(node_ids)), "Pyat row missing from L0-L5 nodes")
    edges = orchestration["edges"]
    outgoing = {edge["from"] for edge in edges}
    l3 = {node["id"] for node in nodes if node["layer"] == "L3"}
    orphans = sorted(l3 - outgoing)
    _require(not orphans, f"orphan L3 functions: {orphans}")
    for edge in edges:
        _require(edge["from"] in node_ids and edge["to"] in node_ids, f"dangling edge {edge}")
    checks.append("all Sorok/Pyat items linked; no orphan L3 function; no dangling edge")

    backward = orchestration.get("backward_paths", {})
    for index in range(6):
        key = f"A{index}"
        _require(key in backward and backward[key][0] == key and backward[key][-1] == "C0", f"{key}: backward path")
        _require(all(item in node_ids for item in backward[key]), f"{key}: unknown backward node")
    for index in range(17):
        key = f"S{index}"
        _require(key in backward and backward[key][-1] == "L5_SOURCE_HOLD", f"{key}: backward hold path")
        _require(all(item in node_ids for item in backward[key]), f"{key}: unknown hold node")
    checks.append("backward paths resolve for A0-A5 and S0-S16")

    traversals = orchestration["traversals"]
    _require(len(traversals) == 3, "three traversals")
    _require({item["id"] for item in traversals} == {"T1_CAREGIVING_PERSON", "T2_MATERIAL_REFUSAL", "T3_HISTORICAL_TRANSFORMATION"}, "traversal ids")
    for item in traversals:
        _require(len(item["path"]) >= 15, f"{item['id']}: path too short")
        for node_id in item["path"]:
            _require(node_id in node_ids, f"{item['id']}: unknown node {node_id}")
        _require(bool(item.get("answer_limits")), f"{item['id']}: no answer limits")
    checks.append("three traversals resolve and retain answer limits")

    pyat_separation = orchestration["pyat_namespace_separation"]
    for key in ("SOROK_N11", "SOROK_N12", "PYAT_N11", "PYAT_N12", "V3_M25", "rule"):
        _require(key in pyat_separation, f"missing Pyat separation key {key}")
    _require("PYAT_N11" in outgoing and "PYAT_N12" in outgoing, "Pyat N11/N12 edges missing")
    checks.append("Sorok/Pyat/V3 namespace separation recorded")

    cycles = _check_cycle_edges(edges, set(node_ids))
    checks.append(f"circular dependencies explicitly typed ({len(cycles)} index cycles)")

    _require(slots["counts"]["priority_decisions_made"] == 0, "priority decision made")
    _require(len(slots["slots"]) == 40, f"expected 40 owner slots, got {len(slots['slots'])}")
    for slot_id in ("S0_S16_SOURCE", "F1CR_PATCH", "V3_ZIP_CONTAINER", "PYAT_NAMESPACE", "PYAT_N11", "PYAT_N12", "JOINT_TEST", "PRIORITY"):
        _require(any(slot["slot"] == slot_id for slot in slots["slots"]), f"missing owner slot {slot_id}")
    _require(all(slot.get("priority_decision") == "NOT_MADE_BY_INDEX" for slot in slots["slots"]), "slot priority decision")
    checks.append("40 owner slots; zero priority decisions; Pyat/F1CR/V3/S0-S16 slots")

    _require(orchestration["status"] == "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED", "candidate status")
    _require(registry["o_index_status"] == "WORKING_CANDIDATE_NOT_HQ_ADJUDICATED", "registry candidate status")
    checks.append("candidate-only authority status")

    report = {
        "schema": "SOROK_PROGRAMMA_O_INDEX_VALIDATION@1",
        "result": "PASS",
        "root": str(root),
        "registry_sha256": hashlib.sha256((root / "01_SOURCE_OF_TRUTH_REGISTRY.json").read_bytes()).hexdigest(),
        "orchestration_sha256": hashlib.sha256((root / "02_L0_L5_LINKED_ORCHESTRATION_INDEX.json").read_bytes()).hexdigest(),
        "checks": checks,
        "counts": {
            "sorok_rows": len(rows),
            "pyat_rows": len(pyat_rows),
            "pyat_f_gates": sum(1 for row in pyat_rows if row["id"].startswith("PYAT_F")),
            "four_assets": len(four),
            "l3_nodes": len(l3),
            "edges": len(edges),
            "traversals": len(traversals),
            "owner_slots": len(slots["slots"]),
            "priority_decisions_made": 0,
            "typed_index_cycles": len(cycles),
        },
        "limits": [
            "PASS means the index is internally complete and honest about holds; it does not mean native product or science acceptance.",
            "The validator never executes candidate code and never reads a private source archive.",
            "Pyat N rows use top-view 06 as a read-only lens with the original Pyat owner authoritative; atlas nodes are advisory, and F gates are HQD-125 law, not whole-estate implementation.",
        ],
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = validate(args.root)
    except (ValidationError, KeyError, json.JSONDecodeError) as error:
        print(json.dumps({"result": "FAIL", "error": str(error)}, indent=2))
        return 1
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
