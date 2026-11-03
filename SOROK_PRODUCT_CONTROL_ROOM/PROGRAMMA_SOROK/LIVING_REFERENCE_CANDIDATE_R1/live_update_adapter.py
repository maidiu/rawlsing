#!/usr/bin/env python3
"""Source-graded PROGRAMMA_DELTA adapter for the existing P0/P1 living reference.

The event and its derived phase/work-now projection live in living_reference.state.
The W8-R guide at an immutable Git commit is read, not copied into another graph.
This is a sourcefree candidate only; no native/owner/human science is issued.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import evidence_store as es
import living_reference as lr

SCHEMA = "SOROK_PROGRAMMA_DELTA@1"
GUIDE_SHA = "a9ebf71e62d84e5dcc599662e976eca7fcd0e623"
GUIDE_ROOT = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK"
GATES_FILE = GUIDE_ROOT + "/14_W7_RECURSIVE_PHASE_GATES_AND_WORK_PACKAGES_R1.jsonl"
SEAMS_FILE = GUIDE_ROOT + "/15_W7_VERSIONED_SEAMS_AND_GATE_JOIN_CANDIDATES_R1.jsonl"
JOIN_E_SUBJECT = "7bf2da302996491ddf34b9a039fea47ac982d135"
JOIN_E_SOURCE_PATH = "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/00_RETURN.md"
JOIN_V_REVIEW = "4387dc818a96fda2d5271672505fbd9da1059703"
JOIN_V_REVIEW_PATH = "WORKER_RETURNS/SOROK-20261022-JOIN-HOSTILE-REVIEW-R1/00_RETURN.md"
REVIEW_RRIF_SUBJECT = "598d9e9eaba5143950c63317705fd09104fbf463"
REVIEW_RRIF_NODE = "JOIN_C12_HOLD"
REVIEW_RRIF_SOURCE_PATH = "WORKER_RETURNS/SOROK_RRIF_R2_REAL_SOURCEFREE_CONSUMER_FANIN/00_RETURN.md"
REVIEW_RRIF_REVIEW_PATH = "WORKER_RETURNS/SOROK_RRIF_R2_INDEPENDENT_HOSTILE_FIRST_CONSUMER_REVIEW_R1/00_RETURN.md"
VALID_KINDS = {"RETURN_CANDIDATE", "SCOPED_REVIEW", "REVIEW_REVISE"}
HIGHER_GRADES = {"NATIVE", "OWNER_ADOPTED", "HUMAN_A5", "ORIGINAL_SCIENCE_ISSUED", "FULL_GATE_ACCEPT"}
VALID_SOURCEFREE_GRADES = {"TEST_ONLY_SOURCEFREE", "SOURCEFREE_SCOPED", "DOCUMENTARY_SOURCE", "INDEPENDENT_NEGATIVE_SOURCE"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class DeltaRefused(ValueError):
    pass


def _must(ok: bool, code: str) -> None:
    if not ok:
        raise DeltaRefused(code)


def _sha(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA40.fullmatch(value))


def _git_text(commit: str, path: str) -> str:
    _must(_sha(commit), "INVALID_SOURCE_COMMIT")
    _must(bool(path and not path.startswith("/") and ".." not in Path(path).parts), "INVALID_SOURCE_PATH")
    content = lr._git(["show", f"{commit}:{path}"])
    _must(content is not None, "SOURCE_OBJECT_UNAVAILABLE_LOCAL_FETCH_REQUIRED")
    return content


@lru_cache(maxsize=1)
def guide_index() -> dict:
    _must(lr._git(["cat-file", "-t", GUIDE_SHA]) == "commit", "EXACT_W8R_GUIDE_COMMIT_NOT_FETCHED")
    def rows(path: str) -> list[dict]:
        return [json.loads(line) for line in _git_text(GUIDE_SHA, path).splitlines() if line.strip()]
    gate_rows = rows(GATES_FILE)
    seam_rows = rows(SEAMS_FILE)
    gates = {r["gate_id"]: r for r in gate_rows if r.get("record_type") == "GATE"}
    leaves = {r["id"]: r for r in gate_rows if r.get("record_type") == "EVIDENCE_LEAF"}
    relations = [r for r in gate_rows if r.get("record_type") == "RELATION"]
    packages = [r for r in gate_rows if r.get("record_type") == "WORK_PACKAGE"]
    seams = {r["seam_id"]: r for r in seam_rows if r.get("record_type") == "VERSIONED_SEAM"}
    targets: dict[str, list[str]] = {}
    for gate_id, gate in gates.items():
        targets.setdefault(gate["target_ref"], []).append(gate_id)
    all_refs = set(targets)
    all_refs.update(r.get("ref") for r in gate_rows if r.get("record_type") == "EVIDENCE_LEAF")
    all_refs.update(r.get("required_ref") for r in relations)
    all_refs.discard(None)
    _must(len(gates) == 83 and len(seams) == 38 and len(leaves) == 127, "FROZEN_GUIDE_STRUCTURE_UNEXPECTED")
    _must(len(gates) == len(set(gates)), "DUPLICATE_GATE_ID")
    return {"gates": gates, "leaves": leaves, "relations": relations, "packages": packages,
            "seams": seams, "targets": targets, "refs": all_refs, "cut": GUIDE_SHA}


def _verify_object(ref: Any, *, require_blob: bool = True) -> tuple[dict, str]:
    _must(isinstance(ref, dict), "TYPED_SOURCE_OBJECT_REQUIRED")
    commit, path, blob = (str(ref.get(k) or "") for k in ("commit", "path", "blob"))
    _must(_sha(commit) and bool(path) and (_sha(blob) if require_blob else True), "EXACT_COMMIT_PATH_BLOB_REQUIRED")
    ok, reason = lr._verify_git_object({"commit": commit, "path": path, "blob": blob, "object_type": "blob"})
    _must(ok, "FORGED_OR_MISSING_GIT_SOURCE:" + reason)
    return dict(ref), _git_text(commit, path)


def _verify_locator(source: dict, locator: Any) -> dict:
    _must(isinstance(locator, dict) and bool(str(locator.get("quote") or "").strip()), "EXACT_SOURCE_QUOTE_REQUIRED")
    _must(locator.get("path", source["path"]) == source["path"], "CROSS_PATH_LOCATOR_FORBIDDEN")
    ok, reason, found = lr._verify_return_locator(source, locator)
    _must(ok, "SOURCE_LOCATOR_UNVERIFIED:" + reason)
    return found


def _verify_code(coord: dict, kind: str) -> dict:
    code = coord.get("code")
    symbol = str(coord.get("first_consumer_symbol") or "")
    if kind == "SCOPED_REVIEW":
        _must(code is not None and symbol and symbol != "NONE", "REVIEW_CONSUMER_CODE_REQUIRED")
    if code is None:
        _must(symbol in {"", "NONE"}, "CONSUMER_ASSERTED_WITHOUT_CODE")
        return {"status": "NONE_VERIFIED", "symbol": "NONE", "code": None}
    source, body = _verify_object(code)
    _must(str(coord.get("code_sha") or source["commit"]) == source["commit"], "CODE_SHA_CROSS_CUT")
    if kind == "SCOPED_REVIEW":
        _must(source["commit"] == JOIN_E_SUBJECT, "POSITIVE_REVIEW_FIRST_READER_CROSS_CUT")
    if symbol in {"", "NONE"}:
        _must(kind != "SCOPED_REVIEW", "POSITIVE_REVIEW_WITHOUT_FIRST_CONSUMER")
        producer = str(coord.get("producer_symbol") or "")
        _must(bool(producer) and producer in body, "SOURCE_PRODUCER_SYMBOL_NOT_FOUND")
        return {"status": "EXACT_SOURCE_PRODUCER_FIRST_READER_NONE",
                "symbol": "NONE", "producer_symbol": producer, "code": source}
    _must(symbol in body, "FIRST_CONSUMER_SYMBOL_NOT_IN_CODE")
    return {"status": "SOURCE_PRESENT_NOT_NATIVE", "symbol": symbol,
            "code": source, "grade": "EXACT_CODE_SYMBOL_AT_PINNED_CUT"}


def _positive_join_e(state: dict, payload: dict) -> dict:
    _must(payload.get("node_id") == "JOIN_E_7BF", "SCOPED_ACCEPTANCE_NODE_NOT_JOIN_E")
    _must(payload.get("guide_ref") == "E021@VERIFY", "SCOPED_ACCEPTANCE_WRONG_GUIDE_MEMBER")
    _must(payload.get("subject_sha") == JOIN_E_SUBJECT, "SCOPED_ACCEPTANCE_CROSS_SUBJECT")
    _must((payload.get("source") or {}).get("path") == JOIN_E_SOURCE_PATH,
          "SCOPED_ACCEPTANCE_SOURCE_PATH_MISMATCH")
    _must(payload.get("coordinate", {}).get("root") == "JOIN_E_7BF_SOURCEFREE", "SCOPED_ACCEPTANCE_CROSS_ROOT")
    record = payload.get("review") or {}
    _must(record.get("commit") == JOIN_V_REVIEW, "SCOPED_ACCEPTANCE_CROSS_REVIEW")
    _must(record.get("path") == JOIN_V_REVIEW_PATH, "SCOPED_ACCEPTANCE_REVIEW_PATH_MISMATCH")
    _verify_object(record)
    evid = {"kind": "ACCEPTANCE_RECORD", "reviewed_sha": JOIN_E_SUBJECT,
            "acceptance": {"record_ref": record["commit"] + ":" + record["path"],
                           "record_blob": record["blob"], "subject_sha": JOIN_E_SUBJECT,
                           "scope": ["JOIN_E_7BF"]}}
    ok, reason, details = lr._verify_acceptance_record(state, "JOIN_E_7BF", "review", evid)
    _must(ok, "ACCEPTANCE_SCOPE_OR_IDENTITY_UNVERIFIED:" + reason)
    return {"kind": "SCOPED_REVIEWED_7BF", "subject_sha": JOIN_E_SUBJECT,
            "reviewer": details.get("reviewer_principal"),
            "grade": "INDEPENDENT_SCOPED_SOURCEFREE_ONLY"}


def _negative_review(payload: dict) -> dict:
    _must(payload.get("node_id") == REVIEW_RRIF_NODE, "REVISE_NODE_NOT_JOIN_C12_HOLD")
    _must(payload.get("subject_sha") == REVIEW_RRIF_SUBJECT, "REVISE_SUBJECT_NOT_RRIF_R2")
    _must(payload.get("guide_ref") in {"C12@VERIFY", "C9@INTEGRATE", "E008:LOCAL_GUIDE:TUPLE_MATRIX@SPECIFY"},
          "REVISE_UNMAPPED_SCOPE")
    _must((payload.get("source") or {}).get("path") == REVIEW_RRIF_SOURCE_PATH,
          "REVISE_SOURCE_PATH_MISMATCH")
    record = payload.get("review") or {}
    _must(record.get("commit") == "8090a1ea308ab17f302f55bb2639c3e4cd774c7a",
          "REVISE_REVIEW_CUT_MISMATCH")
    _must(record.get("path") == REVIEW_RRIF_REVIEW_PATH, "REVISE_REVIEW_PATH_MISMATCH")
    ref, body = _verify_object(record)
    _must("REVISE_MATERIAL_DEFECTS" in body and REVIEW_RRIF_SUBJECT in body,
          "REVIEW_DOES_NOT_BIND_NEGATIVE_AND_SUBJECT")
    _must("INDEPENDENT HOSTILE" in body.upper(), "REVIEW_INDEPENDENCE_NOT_ATTESTED_IN_SOURCE")
    _must("T1" in body and "M1" in body and "C1" in body and "D1" in body,
          "REVIEW_MATERIAL_NEGATIVE_DETAILS_MISSING")
    return {"kind": "REVISE_SOURCE_GROUNDED", "subject_sha": REVIEW_RRIF_SUBJECT,
            "grade": "EXACT_INDEPENDENT_NEGATIVE_AT_SOURCE_CUT",
            "review_commit": ref["commit"],
            "caveat": "DOCUMENTARY_REVIEW_PROVENANCE_ONLY_NOT_NEW_INDEPENDENT_CERTIFICATION"}


def validate_delta(state: dict, payload: Any) -> dict:
    _must(isinstance(payload, dict) and payload.get("schema") == SCHEMA, "DELTA_SCHEMA_MISMATCH")
    guide = guide_index()
    kind = str(payload.get("kind") or "")
    _must(kind in VALID_KINDS, "DELTA_KIND_UNSUPPORTED")
    _must(payload.get("guide_sha") == GUIDE_SHA, "GUIDE_CUT_MISMATCH")
    transition_id = str(payload.get("transition_id") or "")
    _must(bool(re.fullmatch(r"[A-Za-z0-9_.:-]{5,128}", transition_id)), "TRANSITION_ID_INVALID")
    _must(not payload.get("fixture_origin"), "FIXTURE_ORIGIN_CANNOT_UPDATE_OPERATING_VIEW")
    grade = str(payload.get("grade") or "")
    _must(grade in VALID_SOURCEFREE_GRADES and grade not in HIGHER_GRADES,
          "UNISSUED_NATIVE_OWNER_OR_HUMAN_GRADE")
    ref = str(payload.get("guide_ref") or "")
    _must(ref in guide["refs"], "UNKNOWN_OR_UNSELECTED_GUIDE_REF")
    _must(payload.get("node_id") in lr._node_map(state), "UNKNOWN_EXISTING_ENGINE_NODE")
    _must(not str(payload.get("node_id")).startswith("PYAT_"), "EXTERNAL_PYAT_BOUNDARY")
    _must(payload.get("claim_mode") in (None, "", "UNSELECTED"), "OWNER_SELECTOR_NOT_ISSUED")
    owner = str(payload.get("owner_slot") or "")
    known_owner = str(lr._node_map(state)[payload["node_id"]].get("owner") or "")
    _must(owner == known_owner and bool(owner), "FABRICATED_OR_MISMATCHED_OWNER_SLOT")
    _must(not payload.get("caller_verified") and not payload.get("owner_adopted"),
          "CALLER_SELF_GRANT_NOT_EVIDENCE")
    _must(bool(str(payload.get("next_evidence") or "").strip()), "NEXT_EVIDENCE_REQUIRED")
    source, _ = _verify_object(payload.get("source"))
    _must(str(payload.get("return_sha") or "") == source["commit"], "RETURN_SHA_SOURCE_COMMIT_MISMATCH")
    # A valid object at another cut is not a receipt for the claimed subject.
    _must(source["commit"] == str(payload.get("subject_sha") or source["commit"]),
          "SOURCE_COMMIT_SUBJECT_MISMATCH")
    if kind == "RETURN_CANDIDATE":
        # A genuine but unrelated Git blob is not a receipt for this node.
        inherited = lr._node_map(state)[payload["node_id"]].get("source_refs") or []
        _must(any(str(x.get("commit")) == source["commit"]
                  and str(x.get("path")) == source["path"]
                  and str(x.get("blob") or x.get("object_id")) == source["blob"]
                  for x in inherited), "RETURN_SOURCE_NOT_A_NODE_ORIGINAL_SOURCE")
    found = _verify_locator(source, payload.get("locator"))
    coord = payload.get("coordinate")
    _must(isinstance(coord, dict) and coord.get("source_cut") == str(payload.get("subject_sha") or source["commit"]),
          "CODE_REVIEW_SOURCE_CUT_NOT_SELECTED")
    _must(str(coord.get("scope") or "") in {"SOURCEFREE_TEST_ONLY", "SOURCEFREE_FORK_COLD_7BF",
          "SOURCEFREE_RRIF_R2_NEGATIVE", "DOCUMENTARY_RETURN_ONLY"}, "UNBOUNDED_SCOPE")
    verified_code = _verify_code(coord, kind)
    extra: dict = {}
    if kind == "SCOPED_REVIEW":
        _must(grade == "SOURCEFREE_SCOPED" and coord["scope"] == "SOURCEFREE_FORK_COLD_7BF",
              "SCOPED_REVIEW_GRADE_OR_SCOPE_MISMATCH")
        extra = _positive_join_e(state, payload)
    elif kind == "REVIEW_REVISE":
        _must(grade == "INDEPENDENT_NEGATIVE_SOURCE" and coord["scope"] == "SOURCEFREE_RRIF_R2_NEGATIVE",
              "REVISE_SCOPE_MISMATCH")
        extra = _negative_review(payload)
    return {"transition_id": transition_id, "guide_ref": ref, "node_id": payload["node_id"],
            "kind": kind, "owner_slot": owner, "source": source, "source_locator": found,
            "code": verified_code, "grade": grade, "subject_sha": payload.get("subject_sha") or source["commit"],
            "coordinate": copy.deepcopy(coord), "next_evidence": payload["next_evidence"],
            "review": extra, "withdraws_transition_id": payload.get("withdraws_transition_id"),
            "source_grade": "EXACT_GIT_SOURCE_DOCUMENTARY_NO_NATIVE_OR_HUMAN_ISSUANCE"}


def apply_delta(state: dict, payload: dict, *, event_id: str | None = None) -> dict:
    """Replay a verified event into the same P0/P1 state. No guide file is mutated."""
    receipt = validate_delta(state, payload)
    old = next((d for d in state.get("programma_deltas", [])
                if d["transition_id"] == receipt["transition_id"]), None)
    if old is not None:
        _must(old["payload_digest"] == lr._digest(payload), "DELTA_ID_COLLISION")
        return {"status": "DUPLICATE_DELTA_IDEMPOTENT", "transition_id": receipt["transition_id"]}
    receipt["payload_digest"] = lr._digest(payload)
    receipt["event_id"] = event_id
    receipt["status"] = ("SOURCE_PRESENT_CANDIDATE" if receipt["kind"] == "RETURN_CANDIDATE"
                         else "SCOPED_SOURCEFREE_ACCEPTED" if receipt["kind"] == "SCOPED_REVIEW"
                         else "EXACT_NEGATIVE_REVIEWED")
    state.setdefault("programma_deltas", []).append(receipt)
    # Material source/review-state transition, scoped to the reviewed cut.
    # Do not overwrite P0/P1's generic node axis, which may represent another
    # source version and whose original owner/native status cannot be issued here.
    scoped = state.setdefault("scoped_transition_states", {}).setdefault(
        receipt["node_id"], {})
    exact = scoped.setdefault(receipt["subject_sha"], {})
    exact[receipt["guide_ref"]] = {
        "source": receipt["source"],
        "source_verification": "EXACT_GIT_OBJECT_AND_LOCATOR",
        "review": ("INDEPENDENT_SCOPED_7BF_REVIEWED_SOURCEFREE_ONLY"
                   if receipt["kind"] == "SCOPED_REVIEW"
                   else "REVIEW_REVISE_MATERIAL_AT_EXACT_CUT"
                   if receipt["kind"] == "REVIEW_REVISE"
                   else "UNREVIEWED_RETURN_CANDIDATE"),
        "engineering": ("SOURCEFREE_REVIEWED_AT_EXACT_7BF_ONLY"
                        if receipt["kind"] == "SCOPED_REVIEW"
                        else "REVISE_MATERIAL_DEFECTS_AT_EXACT_CUT"
                        if receipt["kind"] == "REVIEW_REVISE"
                        else "SOURCE_PRESENT_AUTHOR_TESTED_NOT_NATIVE"),
        "owner_authority": "UNISSUED", "native_science": "UNISSUED",
        "human_evidence": "NOT_PROVEN",
        "transition_id": receipt["transition_id"],
        "event_id": event_id,
    }
    state.setdefault("node_evidence", {}).setdefault(receipt["node_id"], []).append({
        "kind": "PROGRAMMA_DELTA_DOCUMENTARY", "transition_id": receipt["transition_id"],
        "guide_ref": receipt["guide_ref"], "source": receipt["source"], "grade": receipt["grade"],
        "status": receipt["status"], "event_id": event_id,
    })
    state.setdefault("history", []).append({
        "history_id": "H%04d" % (len(state["history"]) + 1),
        "kind": "PROGRAMMA_DELTA",
        "node_id": receipt["node_id"], "guide_ref": receipt["guide_ref"],
        "transition_id": receipt["transition_id"], "source_cut": receipt["subject_sha"],
        "status": receipt["status"], "event_id": event_id,
    })
    lr._recompute(state)
    return {"status": receipt["status"], "transition_id": receipt["transition_id"],
            "guide_ref": receipt["guide_ref"], "claim_scope": receipt["coordinate"]["scope"]}


def _active(state: dict) -> tuple[list[dict], set[str]]:
    # P0/P1 journal withdrawal is already handled during replay; a caller's
    # invented SOROK_HQ text signature cannot authorize editorial mutation.
    return list(state.get("programma_deltas", [])), set()


def project(state: dict) -> dict:
    """Recompute phase members from W8-R, never treat target eligibility as a receipt.

    An accepted sourcefree E021 at 7bf is not a qualifying receipt at a new
    C12 root. Sourcefree author returns never satisfy native or human stages.
    """
    idx = guide_index()
    active, excluded = _active(state)
    by_ref: dict[str, list[dict]] = {}
    for r in active:
        by_ref.setdefault(r["guide_ref"], []).append(r)
    status_by_gate: dict[str, dict] = {}
    for gate_id, gate in idx["gates"].items():
        members = []
        for m in gate.get("members", []):
            member_ref = m["ref"]
            documentary = (m.get("required_scope") == "DOCUMENTARY_REQUIREMENT"
                           and m.get("qualifying_evidence_id") in idx["leaves"]
                           and idx["leaves"][m["qualifying_evidence_id"]].get("status_at_cut")
                           == "SATISFIED_AT_SCOPED_CUT")
            verified_delta = any(
                d["kind"] == "SCOPED_REVIEW"
                and d["guide_ref"] == member_ref
                and d["subject_sha"] == JOIN_E_SUBJECT
                and d["coordinate"]["root"] == "JOIN_E_7BF_SOURCEFREE"
                and m.get("required_scope") in {"DOCUMENTARY_REQUIREMENT", "SOURCEFREE_SCOPED_EXACT"}
                and state.get("axes", {}).get(d["node_id"], {}).get("source_recovery") not in lr.NEGATIVE_SOURCE
                and state.get("axes", {}).get(d["node_id"], {}).get("review") not in lr.NEGATIVE_REVIEW
                for d in by_ref.get(member_ref, [])
            )
            negative = [d for d in by_ref.get(member_ref, []) if d["kind"] == "REVIEW_REVISE"]
            satisfied = bool((documentary or verified_delta) and not negative)
            members.append({"ref": member_ref, "required_scope": m.get("required_scope"),
                            "qualifies_now": satisfied,
                            "reason": ("EXACT_NEGATIVE_PERSISTS" if negative else
                                       "SOURCE_ONLY_EXISTING_LEAF" if documentary else
                                       "EXACT_7BF_SOURCEFREE_REVIEW" if verified_delta else
                                       "UNISSUED_OR_UNVERIFIED_TARGET_RECEIPT"),
                            "predecessor_gates": m.get("predecessor_gates") or [],
                            "present_but_not_promoting": [
                                {"transition_id": d["transition_id"], "grade": d["grade"],
                                 "source_cut": d["subject_sha"]} for d in by_ref.get(member_ref, [])
                            ]})
        if gate.get("logic") in {"ANY_OF", "IF"} and (
                gate.get("selection_required") or gate.get("predicate")):
            decision = "MODE_UNSELECTED_HOLD"
        elif gate.get("logic") == "ANY_OF":
            decision = ("ELIGIBLE_PREREQUISITES_ONLY" if any(m["qualifies_now"] for m in members)
                        else "BLOCKED_MEMBERS_UNISSUED")
        else:
            decision = ("ELIGIBLE_PREREQUISITES_ONLY" if all(m["qualifies_now"] for m in members)
                        else "BLOCKED_MEMBERS_UNISSUED")
        # Even eligible prerequisites DO NOT create evidence of the target stage.
        status_by_gate[gate_id] = {
            "gate_id": gate_id, "target_ref": gate["target_ref"],
            "logic": gate.get("logic"), "claim_scope": gate.get("claim_scope"),
            "selected_mode": "UNSELECTED",
            "decision": decision, "target_stage_issued": False,
            "owner": gate.get("owner"), "members": members,
            "remaining": [m["ref"] for m in members if not m["qualifies_now"]],
        }
    changed = sorted({r["guide_ref"] for r in state.get("programma_deltas", [])})
    pending = []
    for ref in changed:
        entry = [d for d in active if d["guide_ref"] == ref]
        related = [g for g in status_by_gate.values() if g["target_ref"] == ref or
                   any(m["ref"] == ref for m in g["members"])]
        packages = [p for p in idx["packages"] if ref in p.get("affected_targets", [])]
        reverse = sorted({r["target_ref"] for r in idx["relations"] if r.get("required_ref") == ref})
        related_edges = [
            {"edge_id": r["edge_id"], "required_ref": ref,
             "target_ref": r.get("target_ref"),
             "status": ("REVERSE_CANDIDATE_ONLY_NOT_YET_TARGET_RECEIPT"
                        if not any(d["kind"] == "REVIEW_REVISE" for d in entry)
                        else "NEGATIVE_AT_EXACT_REVIEW_CUT_KEEP_OTHER_CUTS"),
             "blocking": r.get("blocks_target", True)}
            for r in idx["relations"] if r.get("required_ref") == ref
        ]
        source_axes = {
            d["node_id"]: {
                "base_axis_preserved": copy.deepcopy(state.get("axes", {}).get(d["node_id"], {})),
                "exact_cut_phase_review": copy.deepcopy(
                    state.get("scoped_transition_states", {}).get(d["node_id"], {})
                         .get(d["subject_sha"], {}).get(ref, {})),
            }
            for d in entry
        }
        pending.append({
            "ref": ref,
            "current_node_axes": source_axes,
            "affected_typed_edges_not_automatically_promoted": related_edges,
            "receipts": [{"id": d["transition_id"], "kind": d["kind"], "grade": d["grade"],
                          "source_cut": d["subject_sha"], "code_reader": d["code"]["symbol"],
                          "source": d["source"], "owner": d["owner_slot"],
                          "next_evidence": d["next_evidence"],
                          "status": d["status"]} for d in entry],
            "editorially_suppressed": [x for x in excluded if any(
                q["transition_id"] == x and q["guide_ref"] == ref for q in state["programma_deltas"])],
            "gate_decisions": [{"id": g["gate_id"], "status": g["decision"],
                                "remaining": g["remaining"],
                                "review_red_at_selected_cut": any(
                                    d["kind"] == "REVIEW_REVISE" for d in entry),
                                "review_red_source_cuts": [
                                    d["subject_sha"] for d in entry if d["kind"] == "REVIEW_REVISE"]}
                               for g in related],
            "possible_reverse_targets_not_automatically_unlocked": reverse,
            "existing_work_packages": [{"id": p.get("work_package_id"),
                                        "owner": p.get("owner"),
                                        "first_deliverable": p.get("source_derived_first_deliverable")}
                                       for p in packages],
        })
    return {
        "schema": "SOROK_PROGRAMMA_LIVE_WORK_VIEW@1",
        "guide_cut": GUIDE_SHA,
        "adapter_scope": "CANDIDATE_SOURCEFREE_READ_ONLY_WITH_HQ_EDITORIAL_OWNER",
        "original_p0_p1_work_now_unchanged": True,
        "changes": len(state.get("programma_deltas", [])), "changed_refs": changed,
        "active_receipts": len(active), "editorially_suppressed": sorted(excluded),
        "gates": status_by_gate, "by_target": idx["targets"], "pending": pending,
        "scoped_transition_states": copy.deepcopy(state.get("scoped_transition_states", {})),
        "native_person_human_claims": "NONE_ISSUED",
        "pending_qualification": ("NO_NEW_PROGRAMMA_DELTA_INGESTED__HISTORICAL_BASELINE_ONLY"
                                  if not state.get("programma_deltas") else
                                  "SOURCE_GRADED_UPDATES__HQ_ADOPTION_PENDING"),
        "readiness_warning": "ELIGIBLE_PREREQUISITES_ONLY IS NOT TARGET_DONE; ALL SAME-TARGET GATES AND OWNER NATIVE HUMAN EVIDENCE STILL REQUIRED",
    }


def _load_current(path: Path) -> dict:
    return lr._load_state(path)


def commit_delta(fixture: dict, *, state_path: Path = lr.STATE, snapshot_path: Path | None = None,
                 expected_head: str) -> dict:
    """Strict CAS and idempotent typed adapter event; existing journal owns history."""
    journal = lr._journal_path(state_path)
    state = lr.rebuild_from_journal(journal, operating=True)
    validate_delta(state, fixture)
    body = lr._event("PROGRAMMA_DELTA", fixture,
                     source=fixture["source"],
                     actor={"principal": "SOURCE_DERIVED_NOT_HQ_IDENTITY",
                            "role": "CANDIDATE_INTAKE", "verified": False})
    return lr.commit_event(body, journal_path=journal, state_path=state_path,
                           snapshot_path=snapshot_path, expected_head=expected_head,
                           strict_expected_head=True, idempotency_key=fixture["transition_id"])


def query(state: dict, command: str, target: str | None = None) -> dict:
    live = state.get("programma_live") or project(state)
    target = target or ""
    if command == "whole":
        return {"purpose": lr.home_view(state).get("purpose"),
                "unfinished": lr.whole_program_gaps(state),
                "candidate_live_updates": live["pending"],
                "source_cut": GUIDE_SHA, "no_new_native_claim": True}
    if command == "focus":
        comp = target.split("@", 1)[0].split(":", 1)[0]
        base = lr.focus_view(state, comp, 1) if comp in lr._node_map(state) else {"id": comp, "status": "NO_EXISTING_NODE"}
        gates = [live["gates"][g] for g in live["by_target"].get(target, [])]
        return {"target": target, "existing_reference": base,
                "guide_phase_gates": gates, "source_cut": GUIDE_SHA,
                "receipts": [r for r in live["pending"] if r["ref"] == target],
                "rule": "ALL same-target gates, actual member receipts and scope remain required"}
    if command == "source-to-product":
        # The guide's phase-qualified local IDs are not P0/P1 node IDs.
        # Normalize to the actual component before consulting the existing graph.
        guide_id = target.split("@", 1)[0]
        comp = guide_id.split(":", 1)[0]
        seam = guide_index()["seams"].get(guide_id)
        scoped_reader = None
        if seam is not None:
            disposition = seam.get("w8r_source_qualified_disposition") or {}
            first_reader = disposition.get("first_reader")
            if isinstance(first_reader, dict) and first_reader.get("path") and first_reader.get("symbol"):
                scoped_reader = {
                    "seam_id": seam["seam_id"],
                    "first_reader": copy.deepcopy(first_reader),
                    "scope": first_reader.get("scope", "SOURCE_GRADED_ONLY"),
                    "full_join_status": disposition.get("whole_gate_status", seam.get("join_status")),
                    "native_importer": (seam.get("actual_consumer_or_none") or {}).get(
                        "actual_native_importer", "NONE_VERIFIED"),
                    "authority": "SCOPED_SOURCE_READER_NOT_NATIVE_OR_OWNER_ADOPTION",
                }
        if comp in lr._node_map(state):
            existing = lr.code_consumer_view(state, comp)
        else:
            existing = {"id": comp, "current_importer": "NONE_VERIFIED",
                        "scoped_sourcefree_first_reader": scoped_reader,
                        "rule": "A qualified historical reader is not a verified native importer."}
        return {"source": GUIDE_SHA, "component": comp, "guide_ref": guide_id,
                "existing_code_consumer": existing,
                "scoped_seam_first_reader": scoped_reader,
                "phase": query(state, "focus", target),
                "no_transitive_acceptance": True}
    if command == "goal":
        focus = query(state, "focus", target)
        if target in live["by_target"]:
            focus["missing_predecessors"] = [
                {"gate": g["gate_id"], "missing": g["remaining"], "logic": g["logic"],
                 "scope": g["claim_scope"]} for g in focus["guide_phase_gates"]]
        return focus
    if command == "work-now":
        return {"existing_P0_P1": state["work_now"].get("candidates", []),
                "existing_parallel_groups": state["work_now"].get("parallel_groups", []),
                "live_phase_changes": live["pending"],
                "programma_live": state["work_now"].get("programma_live"),
                "source_cut": GUIDE_SHA,
                "no_agent_dispatch": True}
    if command == "changes-since":
        events = state.get("programma_deltas", [])
        if target in {"", GUIDE_SHA}:
            recent = events
        else:
            positions = [i for i, r in enumerate(events)
                         if r["transition_id"] == target or r.get("event_id") == target
                         or r.get("subject_sha") == target or r.get("source", {}).get("commit") == target]
            pos = positions[-1] if positions else None
            _must(pos is not None, "UNKNOWN_CHANGE_CUT_OR_EVENT")
            recent = events[pos + 1:]
        return {"since": target or GUIDE_SHA, "count": len(recent), "changes": [
            {"id": r["transition_id"], "guide_ref": r["guide_ref"],
             "kind": r["kind"], "status": r["status"], "source_cut": r["subject_sha"]}
            for r in recent]}
    if command == "freshness":
        return {"guide_sha": GUIDE_SHA, "journal_head": state.get("journal_head"),
                "revision": state.get("revision"), "source_snapshot": state.get("source_snapshot"),
                "changes": live["changes"], "pending": live["pending"],
                "adoption": "OWNER_PENDING", "runtime": "NO_DAEMON",
                "pending_qualification": live["pending_qualification"],
                "changes_since_guide_cut": live["changes"],
                "not_checked_automatically": "No background fetch, process observation or unseen worker import"}
    if command == "candidate-patch":
        return {"status": "HQ_REVIEW_PATCH_CANDIDATE_NOT_APPLIED", "base_guide_sha": GUIDE_SHA,
                "patches": [{"guide_ref": r["ref"], "source_return_receipts": r["receipts"],
                             "proposed_current_stage_gates": r["gate_decisions"],
                             "reverse_edges": r["possible_reverse_targets_not_automatically_unlocked"]}
                            for r in live["pending"]],
                "instruction": "Qualified HQ edits existing 00/06-15 after owner decision; adapter never silently rewrites guide."}
    raise DeltaRefused("UNKNOWN_ADAPTER_VIEW")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", type=Path, default=lr.STATE)
    ap.add_argument("--snapshot", type=Path, default=None)
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("whole", "work-now", "freshness", "candidate-patch"):
        sub.add_parser(name)
    for name in ("focus", "source-to-product", "goal", "changes-since"):
        sub.add_parser(name).add_argument("target")
    i = sub.add_parser("intake")
    i.add_argument("packet", type=Path)
    i.add_argument("--expected-head", required=True,
                   help="Exact existing journal head, not a source SHA")
    args = ap.parse_args(argv)
    try:
        if args.command == "intake":
            packet = json.loads(args.packet.read_text(encoding="utf-8"))
            result = commit_delta(packet, state_path=args.state, snapshot_path=args.snapshot,
                                  expected_head=args.expected_head)
        else:
            result = query(_load_current(args.state), args.command, getattr(args, "target", ""))
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (DeltaRefused, es.JournalError, ValueError) as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
