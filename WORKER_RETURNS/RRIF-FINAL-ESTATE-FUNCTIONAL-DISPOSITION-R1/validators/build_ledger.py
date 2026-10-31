#!/usr/bin/env python3
"""Build the RRIF 1,885-family disposition ledger from exact S7FIX evidence.

The builder never checks out or executes a historical branch. It reads the
S7FIX JSON artifact, maps its current-path references to PRE-MAIN tree blobs,
and applies the I3 owner-mapping correction for the six repaired boundaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

S7FIX = "80bc5d9bf6624c2ea04027322947a41c347330aa"
S7FIX_I3 = "1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088"
PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
S7FIX_DIR = "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR"
I3_DIR = "PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7FIX_I3_HOSTILE"
PATH_RE = re.compile(r"(?P<path>[A-Za-z0-9_./-]+\.(?:py|json|jsonl|yaml|yml|js|ts))")
ALLOWED = {
    "ALREADY_CURRENT",
    "CURRENT_DIFFERENT",
    "CURRENT_TEST_ONLY",
    "HISTORICAL_ONLY",
    "RETIRED_DEFECTIVE",
    "EVIDENCE_ONLY",
    "DUPLICATE_SUPERSEDED",
    "CANDIDATE_ADAPT",
    "NO_REAL_RECEIVER_VERIFIED",
    "AUTHORITY_HELD",
    "NOT_RESOLVED",
}
DECISION = {
    "ALREADY_CURRENT": "PRESERVE_HISTORICAL",
    "CURRENT_DIFFERENT": "HOLD_EXACT_DECISION",
    "CURRENT_TEST_ONLY": "PRESERVE_HISTORICAL",
    "HISTORICAL_ONLY": "PRESERVE_HISTORICAL",
    "RETIRED_DEFECTIVE": "RETIRE",
    "EVIDENCE_ONLY": "PRESERVE_HISTORICAL",
    "DUPLICATE_SUPERSEDED": "RETIRE",
    "CANDIDATE_ADAPT": "HOLD_EXACT_DECISION",
    "NO_REAL_RECEIVER_VERIFIED": "HOLD_EXACT_DECISION",
    "AUTHORITY_HELD": "HOLD_EXACT_DECISION",
    "NOT_RESOLVED": "HOLD_EXACT_DECISION",
}
BOUNDARY = {
    "S7FAM-0869c56ad5e0c899": ("CURRENT_DIFFERENT", "OUTER", "e1fcc98f"),
    "S7FAM-82686a98a4281425": ("CURRENT_DIFFERENT", "OUTER", "47a40b20"),
    "S7FAM-5823124c837704c1": ("CURRENT_DIFFERENT", "OUTER", "20385e92"),
    "S7FAM-6054813ba02c8e44": ("CURRENT_DIFFERENT", "OUTER", "90243295"),
    "S7FAM-a7fe27d3f45643c3": ("CURRENT_DIFFERENT", "OUTER", "5c1d7f0b"),
    "S7FAM-3ced5b9ab5b98431": ("HISTORICAL_ONLY", "NESTED_ABSENT", None),
    "S7FAM-0808b82fba697141": ("HISTORICAL_ONLY", "NESTED_ABSENT", None),
    "S7FAM-739724b429c79765": ("HISTORICAL_ONLY", "NESTED_ABSENT", None),
    "S7FAM-dabfb5ad4dc9f0a4": ("HISTORICAL_ONLY", "NESTED_ABSENT", None),
    "S7FAM-c7246db42c0322e0": ("HISTORICAL_ONLY", "NESTED_ABSENT", None),
    "S7FAM-41da3f505673271b": ("CURRENT_DIFFERENT", "JOIN_CURRENT_DIFFERENT", "77d9be6c"),
}
PRIORITY_OWNER = {
    "C3_R5_PR526": "PRE-MAIN physical decoder/R5 codec owner + native source authority",
    "R9_SOURCE_RUNTIME": "R61 current issuer/role owner + real source consumer owner",
    "P41_E04L_SERVICE": "Original P41/E04L/N9/N10W service owner",
    "SELECTED_WORLD_SEAM": "Selected-world/SC0 owner",
    "F7_P07": "Original EE12/F7 comparability issuer; separate native P07 owner",
    "PE_V2K": "PE owner-bound successor owner; original V2K identity owner",
    "R61_R08_BINDER": "R61-R08 evidence owner + named current adopter",
    "R61_R03_UNIVERSE": "R61 issuer/universe owner",
    "R157_CONFIG": "Pyat source configuration owner",
    "R61_R09_NEGATIVE": "R61-R09 owner",
    "OTHER": "Original component/source owner",
}
P0_FAMILIES = {
    "C3_R5_PR526",
    "R9_SOURCE_RUNTIME",
    "P41_E04L_SERVICE",
    "SELECTED_WORLD_SEAM",
    "F7_P07",
    "PE_V2K",
    "R61_R08_BINDER",
    "R61_R03_UNIVERSE",
    "R157_CONFIG",
    "R61_R09_NEGATIVE",
}


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def tree_blobs(commit: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in run_git("ls-tree", "-r", "--full-tree", commit).splitlines():
        meta, path = line.split("\t", 1)
        _, _, blob = meta.split()
        result[path] = blob
    return result


def flatten(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(flatten(item))
        return out
    return []


def parse_paths(value: Any, known: dict[str, str]) -> list[str]:
    out = set()
    for text in flatten(value):
        for match in PATH_RE.finditer(text):
            path = match.group("path").replace("::", "/")
            if path in known:
                out.add(path)
    return sorted(out)


def family_labels(family: dict[str, Any]) -> set[str]:
    pg = family.get("preserved_group_fields")
    if not isinstance(pg, dict):
        return set()
    labels = pg.get("original_labels") or {}
    return set(labels)


def member_negative_count(family: dict[str, Any]) -> int:
    return len(family.get("review_negative_preservation") or [])


def negative_hashes(family: dict[str, Any]) -> list[str]:
    hashes = []
    for record in family.get("review_negative_preservation") or []:
        digest = record.get("s6_group_review_findings_sha256")
        if digest:
            hashes.append(digest)
    return sorted(set(hashes))


def receiver_text(family: dict[str, Any]) -> str:
    c = family.get("current_receiver_and_integratability") or {}
    text = " | ".join(flatten(c.get("s7_current_receiver")))
    return text or "UNKNOWN"


def member_current_states(family: dict[str, Any]) -> list[str]:
    states = []
    c = family.get("current_receiver_and_integratability") or {}
    for item in c.get("member_current_ownership") or []:
        current = item.get("current") or {}
        for key in ("status", "current_receiver_status"):
            if isinstance(current.get(key), str):
                states.append(current[key])
        receiver = current.get("current_receiver")
        if isinstance(receiver, dict) and isinstance(receiver.get("state"), str):
            states.append(receiver["state"])
        refs = current.get("refs")
        if isinstance(refs, list):
            for ref in refs:
                if isinstance(ref, dict) and ref.get("path", "").startswith("rawlsing_next/tests/"):
                    states.append("TEST_ONLY_REFERENCE")
    return states


def current_paths(family: dict[str, Any], known: dict[str, str]) -> list[str]:
    c = family.get("current_receiver_and_integratability") or {}
    out = set()
    for key in ("s6_current_receiver_candidates", "s6_competing_current_implementations"):
        for item in c.get(key) or []:
            if isinstance(item, dict) and item.get("path") in known:
                out.add(item["path"])
    for item in c.get("s6_group_current_receiver_candidates") or []:
        for sub in item if isinstance(item, list) else [item]:
            if isinstance(sub, dict) and sub.get("path") in known:
                out.add(sub["path"])
    for item in c.get("member_current_ownership") or []:
        current = item.get("current") or {}
        receiver = current.get("current_receiver")
        if isinstance(receiver, dict) and receiver.get("path") in known:
            out.add(receiver["path"])
        for ref in current.get("refs") or []:
            if isinstance(ref, dict) and ref.get("path") in known:
                out.add(ref["path"])
        for text in flatten(current.get("current_receiver_or_unknown")):
            for match in PATH_RE.finditer(text):
                if match.group("path") in known:
                    out.add(match.group("path"))
        for text in flatten(current.get("current_implementation_candidate")):
            for match in PATH_RE.finditer(text):
                if match.group("path") in known:
                    out.add(match.group("path"))
    for item in c.get("s7_s6_first_current_consumer") or []:
        if isinstance(item, dict):
            for text in flatten(item.get("candidates")):
                for match in PATH_RE.finditer(text):
                    if match.group("path") in known:
                        out.add(match.group("path"))
    return sorted(out)


def classify(family: dict[str, Any], labels: set[str], current: list[str], rcvr: str, states: list[str], known: dict[str, str]) -> str:
    fid = family["family_id"]
    if fid in BOUNDARY:
        return BOUNDARY[fid][0]
    c = family.get("current_receiver_and_integratability") or {}
    eng = c.get("engineering_status", "")
    if eng.startswith("RED__"):
        return "RETIRED_DEFECTIVE"
    if eng == "EVIDENCE_ONLY":
        return "EVIDENCE_ONLY"
    if "SUPERSEDED_BETTER" in labels:
        return "DUPLICATE_SUPERSEDED"
    if labels & {"INVALID", "INVALID/TRASH_WITH_GROUNDS", "TRASH_WITH_GROUNDS"}:
        return "RETIRED_DEFECTIVE"
    if "UNIQUE_USEFUL_HELD_BY_ACTUAL_SOURCE_AUTHORITY" in labels:
        return "AUTHORITY_HELD"
    if "EVIDENCE_UNKNOWN" in labels:
        return "NOT_RESOLVED"
    members = family.get("members") or []
    production_paths = [m.get("identity", {}).get("path") for m in members if m.get("identity", {}).get("path") in known and not m.get("identity", {}).get("path", "").startswith("rawlsing_next/tests/")]
    test_paths = [m.get("identity", {}).get("path") for m in members if m.get("identity", {}).get("path") in known and m.get("identity", {}).get("path", "").startswith("rawlsing_next/tests/")]
    matched = [m for m in members if m.get("identity", {}).get("path") in known and known[m["identity"]["path"]] == m.get("identity", {}).get("source_blob")]
    if matched and any(not m["identity"]["path"].startswith("rawlsing_next/tests/") for m in matched):
        return "ALREADY_CURRENT"
    if production_paths:
        return "CURRENT_DIFFERENT"
    if test_paths:
        return "CURRENT_TEST_ONLY"
    if any("TEST" in state for state in states) or "TEST_ONLY" in rcvr:
        return "CURRENT_TEST_ONLY"
    presence = c.get("s7_current_functional_presence", "")
    if presence in {"CURRENT_CODE_PRESENT_OR_EXACT", "CURRENT_REFERENCE_ONLY_UNPROVEN"}:
        if labels & {"UNIQUE_USEFUL_READY", "UNIQUE_USEFUL_NEEDS_ADAPTATION"}:
            return "CANDIDATE_ADAPT"
        return "CURRENT_DIFFERENT"
    if "CURRENT_PATH_ABSENT" in presence:
        return "HISTORICAL_ONLY"
    return "NO_REAL_RECEIVER_VERIFIED"


def actual_receiver(status: str, rcvr: str, current: list[str], states: list[str], boundary: tuple | None = None) -> str:
    if boundary:
        if boundary[1] == "OUTER":
            return "TEST_ONLY_CURRENT_OUTER_AST_DIFFERS__NO_PRODUCTION_IMPORT"
        if boundary[1] == "NESTED_ABSENT":
            return "NO_CURRENT_NESTED_OWNER__HISTORICAL_ONLY"
        return "STATIC_IMPORT_RECEIVERS__CURRENT_EMIT_DIFFERS__EXECUTED_CONSUMER_NOT_RUN"
    if status == "EVIDENCE_ONLY":
        return "TEST_EVIDENCE_ONLY__NO_PRODUCTION_FUNCTION"
    if status == "HISTORICAL_ONLY":
        return "NO_CURRENT_PATH_OR_NESTED_OWNER__HISTORICAL_ONLY"
    if status == "CURRENT_TEST_ONLY":
        return "TEST_ONLY_REFERENCE__NO_PRODUCTION_IMPORT"
    if any("EXACT_AST_SAME_PATH" in state for state in states):
        return "CURRENT_PATH_EXACT_AST__PRODUCTION_IMPORT_NOT_PROVEN"
    if any("DIFFERENT_IMPLEMENTATION" in state for state in states):
        return "CURRENT_PATH_DIFFERENT_AST__PRODUCTION_IMPORT_NOT_PROVEN"
    if "STATIC_IMPORT_RECEIVERS" in rcvr:
        return "STATIC_IMPORT_RECEIVERS__EXECUTED_CONSUMER_NOT_RUN"
    if "TEST_ONLY" in rcvr:
        return "TEST_ONLY_REFERENCE__NO_PRODUCTION_IMPORT"
    if "NO_PRODUCTION_IMPORT_FOUND" in rcvr:
        return "REFERENCE_ONLY__NO_PRODUCTION_IMPORT"
    if "CANDIDATE_LIBRARY_CHAIN" in rcvr:
        return "CANDIDATE_LIBRARY_CHAIN__NO_PRODUCTION_ENTRYPOINT"
    if current:
        return "CURRENT_PATH_REFERENCE__CALLER_NOT_PROVEN"
    return "NO_REAL_RECEIVER_VERIFIED"


def merit(status: str, labels: set[str], current: list[str]) -> str:
    if status == "ALREADY_CURRENT":
        return "CURRENT_SOURCE_IDENTITY_EXACT__NO_INCREMENTAL_CODE_ACTION"
    if status == "CURRENT_DIFFERENT":
        return "CURRENT_IMPLEMENTATION_DIFFERS__HISTORICAL_COMPARATIVE_MERIT_UNPROVEN"
    if status == "CURRENT_TEST_ONLY":
        return "TEST_SCOPE_ONLY__NO_PRODUCTION_MERIT_PROVEN"
    if status == "HISTORICAL_ONLY":
        return "HISTORICAL_IDENTITY_ONLY__CURRENT_MERIT_UNPROVEN"
    if status == "RETIRED_DEFECTIVE":
        return "HISTORICAL_DEFECT__DO_NOT_PROMOTE"
    if status == "EVIDENCE_ONLY":
        return "EVIDENCE_ONLY__NO_PRODUCTION_FUNCTION"
    if status == "DUPLICATE_SUPERSEDED":
        return "HISTORICAL_SUPERSEDED__NO_INCREMENTAL_MERIT"
    if status == "CANDIDATE_ADAPT":
        return "CANDIDATE_NEEDS_NAMED_RECEIVER_AND_FAULT_NEGATIVE"
    if status == "AUTHORITY_HELD":
        return "HELD_BY_ORIGINAL_SOURCE_AUTHORITY__NO_SOURCEFREE_PROMOTION"
    if status == "NO_REAL_RECEIVER_VERIFIED":
        return "REFERENCE_ONLY__NO_REAL_RECEIVER_VERIFIED"
    return "UNRESOLVED__NO_MERIT_DECISION"


def current_owner_status(fid: str, status: str) -> str:
    if fid in BOUNDARY:
        return "RED__I3_CURRENT_OUTER_NESTED_OR_EMIT_MAPPING"
    if status == "ALREADY_CURRENT":
        return "SOURCE_IDENTITY_ONLY__NO_PRODUCTION_RECEIVER_PROOF"
    if status == "CURRENT_DIFFERENT":
        return "CURRENT_PATH_DIFFERS__OWNER_DECISION_NEEDED"
    if status == "HISTORICAL_ONLY":
        return "NO_CURRENT_OWNER"
    if status == "CURRENT_TEST_ONLY":
        return "TEST_ONLY_OWNER"
    return "UNRESOLVED_OR_HELD"


def build(s7fix_path: Path, out_dir: Path) -> dict[str, Any]:
    source = json.loads(s7fix_path.read_text(encoding="utf-8"))
    families = source["corrected_families"]
    known = tree_blobs(PREMAIN)
    out_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    ledger_lines = []
    negative_lines = []
    custody_lines = []
    neg_index = 0
    function_seen: set[str] = set()
    family_seen: set[str] = set()
    for family in families:
        fid = family["family_id"]
        if fid in family_seen:
            raise AssertionError(f"duplicate family {fid}")
        family_seen.add(fid)
        labels = family_labels(family)
        rcvr = receiver_text(family)
        states = member_current_states(family)
        current = current_paths(family, known)
        status = classify(family, labels, current, rcvr, states, known)
        if status not in ALLOWED:
            raise AssertionError(status)
        counts[status] += 1
        c = family.get("current_receiver_and_integratability") or {}
        boundary = BOUNDARY.get(fid)
        current_ast = boundary[2] if boundary else None
        historical_paths = sorted({m.get("identity", {}).get("path") for m in family["members"] if m.get("identity", {}).get("path") in known})
        for path in historical_paths:
            if path not in current:
                current.append(path)
        current = sorted(current)
        current_blobs = [{"path": path, "blob": known[path]} for path in current]
        matched_members = [m["function_id"] for m in family["members"] if m.get("identity", {}).get("path") in known and known[m["identity"]["path"]] == m.get("identity", {}).get("source_blob")]
        members = []
        for member in family["members"]:
            identity = member.get("identity") or {}
            mid = member["function_id"]
            if mid in function_seen:
                raise AssertionError(f"duplicate function {mid}")
            function_seen.add(mid)
            test = member.get("test_status_evidence") or {}
            members.append({
                "function_id": mid,
                "shard": member.get("shard"),
                "original_group_id": member.get("original_group_id"),
                "path": identity.get("path"),
                "symbol": identity.get("symbol"),
                "actual_qualname": identity.get("actual_qualname"),
                "source_blob": identity.get("source_blob"),
                "ast_sha1": identity.get("ast_sha1"),
                "ast_status": identity.get("ast_status"),
                "introducing_commit": identity.get("introducing_commit"),
                "introducing_commit_status": identity.get("introducing_commit_status"),
                "original_label": member.get("original_label"),
                "corrected_disposition": member.get("corrected_disposition"),
                "test_status": {k: test.get(k) for k in ("positive_oracle", "fault_negative_oracle", "cold_replay", "current_first_consumer")},
            })
            custody_lines.append({
                "schema": "RRIF_FUNCTION_ID_CUSTODY@1",
                "function_id": mid,
                "family_id": fid,
                "shard": member.get("shard"),
                "original_group_id": member.get("original_group_id"),
                "path": identity.get("path"),
                "symbol": identity.get("symbol"),
                "actual_qualname": identity.get("actual_qualname"),
                "source_blob": identity.get("source_blob"),
                "ast_sha1": identity.get("ast_sha1"),
                "introducing_commit": identity.get("introducing_commit"),
                "original_label": member.get("original_label"),
                "corrected_disposition": member.get("corrected_disposition"),
            })
        pg = family.get("preserved_group_fields") if isinstance(family.get("preserved_group_fields"), dict) else {}
        priority_family = pg.get("priority_family") or "OTHER"
        neg_count = member_negative_count(family)
        current_implementation_sha = current_blobs[0]["blob"] if len(current_blobs) == 1 else ("MULTIPLE_PATH_BLOBS" if current_blobs else None)
        if boundary and boundary[1] == "NESTED_ABSENT":
            current_implementation_sha = None
        line = {
            "schema": "RRIF_FAMILY_DISPOSITION@1",
            "family_id": fid,
            "family_order": family.get("family_order"),
            "family_name": family.get("family_name"),
            "family_identity_key": family.get("family_identity_key"),
            "owner_scope": family.get("owner_scope"),
            "external_zero_member": family.get("owner_scope") == "EXTERNAL" and not family.get("member_function_ids"),
            "correction": family.get("correction"),
            "original": {
                "member_count": len(members),
                "function_ids": [m["function_id"] for m in members],
                "legacy_group_ids": family.get("legacy_group_ids"),
                "historical_blobs": sorted({m["source_blob"] for m in members if m.get("source_blob")}),
                "variants": members,
                "labels": sorted(labels),
                "inherited_branch_count": pg.get("inherited_branch_count"),
                "negative_record_count": neg_count,
                "negative_hashes": negative_hashes(family),
            },
            "current": {
                "functional_presence": c.get("s7_current_functional_presence"),
                "receiver_evidence": rcvr,
                "current_paths": current,
                "current_path_blobs": current_blobs,
                "current_implementation_sha": current_implementation_sha,
                "current_ast_sha": current_ast,
                "current_ast_sha_scope": "8_HEX_PREFIX_FROM_I3_HOSTILE_COURT" if current_ast else None,
                "current_nested_owner_absent": bool(boundary and boundary[1] == "NESTED_ABSENT"),
                "historical_paths_present": historical_paths,
                "matched_current_member_ids": matched_members,
                "actual_current_import_or_caller": actual_receiver(status, rcvr, current, states, boundary),
                "production_receiver_verified": False,
                "current_owner_mapping_status": current_owner_status(fid, status),
                "current_boundary_role": boundary[1] if boundary else None,
            },
            "tests": {
                "rrif_run": [],
                "historical_status_sample": [m["test_status"] for m in members[:3]],
                "test_scope": "RRIF did not execute historical branch code; current receipts are referenced only. Validator/tests are the only RRIF executions.",
            },
            "grades": {
                "engineering": c.get("engineering_status"),
                "science": c.get("scientific_status"),
                "authority": c.get("authority_status"),
                "human_product": "NOT_APPLICABLE_OR_NOT_PROVEN",
                "native_product_accepted": False,
                "source_science_issued": False,
            },
            "abi": {
                "original": {"paths": sorted({m["path"] for m in members if m.get("path")}), "qualnames": sorted({m["actual_qualname"] for m in members if m.get("actual_qualname")})},
                "current": {"paths": current, "blobs": current_blobs, "ast_sha": current_ast},
                "equivalence": "NOT_CLAIMED__SOURCE_IDENTITY_ONLY" if status == "ALREADY_CURRENT" else ("DIFFERENT_CURRENT_AST" if boundary and boundary[1] in {"OUTER", "JOIN_CURRENT_DIFFERENT"} else ("CURRENT_NESTED_OWNER_ABSENT" if boundary else "NOT_CLAIMED")),
            },
            "comparison": {
                "candidate_comparative_merit": merit(status, labels, current),
                "historical_review": pg.get("s7_final_disposition"),
                "current_receiver_recommendation": c.get("integration_recommendations"),
                "variant_comparisons": [
                    {
                        "function_id": m["function_id"],
                        "path": m.get("path"),
                        "source_blob": m.get("source_blob"),
                        "current_blob_match": bool(m.get("path") in known and m.get("source_blob") == known.get(m["path"])),
                        "current_path_present": bool(m.get("path") in known),
                        "variant_state": ("CURRENT_EXACT_BLOB" if m.get("path") in known and m.get("source_blob") == known.get(m["path"]) else ("CURRENT_NESTED_OWNER_ABSENT" if boundary and boundary[1] == "NESTED_ABSENT" else ("CURRENT_PATH_DIFFERS" if m.get("path") in known else "NO_CURRENT_PATH"))),
                        "variant_decision": DECISION[status],
                    }
                    for m in members
                ],
            },
            "disposition": {
                "status": status,
                "decision": DECISION[status],
                "rrif_priority": "P0" if priority_family in P0_FAMILIES else ("P1" if status in {"ALREADY_CURRENT", "CURRENT_DIFFERENT", "CANDIDATE_ADAPT", "NO_REAL_RECEIVER_VERIFIED", "CURRENT_TEST_ONLY"} else "P2"),
                "priority_family": priority_family,
                "fanin_candidate": False,
                "reason": actual_receiver(status, rcvr, current, states, boundary),
            },
            "owner": {
                "slot": PRIORITY_OWNER.get(priority_family, PRIORITY_OWNER["OTHER"]),
                "status": "NAMED_OWNER_SLOT__NO_ADOPTION" if priority_family != "OTHER" else "ORIGINAL_OWNER_SLOT__UNASSIGNED_OR_HELD",
            },
            "source_evidence": {"s7fix": S7FIX, "artifact": f"{S7FIX_DIR}/CORRECTED_RECEIVER_AND_INTEGRATABILITY.json", "family_key": fid},
            "unknowns": family.get("unknowns") or [],
        }
        if boundary:
            line["current"]["boundary_finding"] = "I3 hostile: current owner mapping RED; historical outer/nested/emit not behaviorally equivalent."
        ledger_lines.append(line)
        for record in family.get("review_negative_preservation") or []:
            neg_index += 1
            negative_lines.append({
                "schema": "RRIF_HISTORICAL_NEGATIVE_RECORD@1",
                "negative_id": f"NEG-{neg_index:04d}",
                "family_id": fid,
                "family_name": family.get("family_name"),
                "member_function_ids": family.get("member_function_ids"),
                "scope": record.get("scope"),
                "original_group_id": record.get("original_group_id"),
                "record_sha256": record.get("s6_group_review_findings_sha256"),
                "source": {"s7fix": S7FIX, "artifact": f"{S7FIX_DIR}/CORRECTED_RECEIVER_AND_INTEGRATABILITY.json"},
                "cause": "PRESERVED_FAMILY_REVIEW_OR_SOURCE_AUTHORITY_NEGATIVE",
                "record": record,
            })
    if len(ledger_lines) != 1885:
        raise AssertionError(len(ledger_lines))
    if function_seen.__len__() != 3135:
        raise AssertionError(len(function_seen))
    if neg_index != 2595:
        raise AssertionError(neg_index)
    if len(custody_lines) != 3135:
        raise AssertionError(len(custody_lines))
    (out_dir / "ALL_1885_FAMILY_DISPOSITIONS.jsonl").write_text("".join(json.dumps(x, separators=(",", ":")) + "\n" for x in ledger_lines), encoding="utf-8")
    (out_dir / "HISTORICAL_NEGATIVES_AND_ANTI_REBUILD.jsonl").write_text("".join(json.dumps(x, separators=(",", ":")) + "\n" for x in negative_lines), encoding="utf-8")
    (out_dir / "FUNCTION_ID_CUSTODY.jsonl").write_text("".join(json.dumps(x, separators=(",", ":")) + "\n" for x in custody_lines), encoding="utf-8")
    branch_roster = source["branch_identity_custody"]
    (out_dir / "BRANCH_ROSTER_845.json").write_text(json.dumps(branch_roster, indent=2) + "\n", encoding="utf-8")
    summary = {
        "schema": "RRIF_LEDGER_BUILD_SUMMARY@1",
        "s7fix": S7FIX,
        "s7fix_i3": S7FIX_I3,
        "s7fix_artifact_sha256": hashlib.sha256(s7fix_path.read_bytes()).hexdigest(),
        "s7fix_artifact_blob": "743f79e2e618d3e5f083c6033ba9f37f0d4c4c07",
        "premain": PREMAIN,
        "premain_rawlsing_next_tree": "1d88d3fbb1d18dadfda946d9cd7f309d84afa479",
        "families": len(ledger_lines),
        "function_ids": len(function_seen),
        "variant_comparisons": len(function_seen),
        "negative_records": neg_index,
        "branch_names": branch_roster["total_branches"],
        "distinct_tips": source["counts"]["distinct_roster_tips"],
        "status_counts": dict(sorted(counts.items())),
        "correction_counts": dict(Counter(f["correction"]["type"] for f in families)),
        "boundary_families": sorted(BOUNDARY),
    }
    (out_dir / "LEDGER_BUILD_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s7fix", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    summary = build(args.s7fix, args.out)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
