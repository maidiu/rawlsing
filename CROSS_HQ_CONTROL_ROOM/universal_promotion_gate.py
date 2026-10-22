"""R56 R00E independent policy claim-transition gate.

The public gate consumes a pinned policy handle and an untrusted submitted
claim. It never treats caller booleans, hashes, traces or mock transports as
native execution authority. R09 and original grants remain unissued.
"""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

CONTRACT_ID = "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0"
DEFAULT_COMMIT = "6d95a78bf6b7bcf70022e303a151255e65edc38a"
DEFAULT_ROOT = "CROSS_HQ_CONTROL_ROOM/universal_execution_policy/r56_sourcefree_v1/revisions/r2"
POLICY_FILES = ("CONTRACT.md", "policy.json", "synthetic_universes.json",
                "decision_cases.json", "freeze.json")
ORIGINAL_OBLIGATIONS = {
    "source_count": 35,
    "per_source_axes": 54,
    "cells": 1890,
    "global": ["F6", "F7", "F8"],
}


@dataclass(frozen=True)
class PinnedPolicyHandle:
    commit: str
    root: str
    variant_id: str
    policy: Mapping[str, Any]
    synthetic: Mapping[str, Any]
    freeze: Mapping[str, Any]
    expected_operations: tuple[Mapping[str, Any], ...]
    expected_ids: tuple[str, ...]
    blobs: Mapping[str, str]
    verified: bool

    def policy_ref(self) -> dict:
        return {"commit": self.commit, "path": self.root,
                "variant_id": self.variant_id}


class GateRefusal(ValueError):
    pass


def _repo_root() -> Path:
    path = Path(__file__).resolve()
    for parent in path.parents:
        if (parent / ".git").exists():
            return parent
    raise GateRefusal("REPOSITORY_ROOT_NOT_FOUND")


def _git_show(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-c", "gc.auto=0", "show", f"{commit}:{path}"],
        cwd=str(repo), text=False)


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_pinned_policy(commit: str = DEFAULT_COMMIT, root: str = DEFAULT_ROOT,
                       variant_id: str = "CANONICAL_V1") -> PinnedPolicyHandle:
    repo = _repo_root()
    raw = {name: _git_show(repo, commit, f"{root}/{name}") for name in POLICY_FILES}
    blobs = {name: _git_blob_sha1(data) for name, data in raw.items()}
    policy = json.loads(raw["policy.json"])
    synthetic = json.loads(raw["synthetic_universes.json"])
    freeze = json.loads(raw["freeze.json"])
    expected_blobs = {
        row["path"].rsplit("/", 1)[-1]: row["git_blob_sha1"]
        for row in freeze.get("successor_content_blobs", [])
    }
    verified = all(blobs.get(name) == expected_blobs.get(name)
                   for name in ("CONTRACT.md", "policy.json",
                                "synthetic_universes.json", "decision_cases.json"))
    if variant_id == "CANONICAL_V1":
        operations = tuple(copy.deepcopy(synthetic["expected_operations"]))
    else:
        variants = {row["variant_id"]: row
                    for row in synthetic.get("independent_materialized_variants", [])}
        if variant_id not in variants:
            raise GateRefusal("UNKNOWN_VARIANT")
        operations = tuple(copy.deepcopy(variants[variant_id]["expected_operations"]))
    ids = tuple(row["operation_id"] for row in operations)
    return PinnedPolicyHandle(commit=commit, root=root, variant_id=variant_id,
                              policy=policy, synthetic=synthetic, freeze=freeze,
                              expected_operations=operations, expected_ids=ids,
                              blobs=blobs, verified=verified)


def canonical_typed_identity(value: Any, *, version: str = "R56-TYPED-K@1") -> dict:
    def encode(item):
        if item is None:
            return {"type": "null"}
        if isinstance(item, bool):
            return {"type": "bool", "value": item}
        if isinstance(item, int):
            return {"type": "integer", "value": str(item)}
        if isinstance(item, float):
            return {"type": "decimal", "value": repr(item)}
        if isinstance(item, str):
            return {"type": "string", "value": item}
        if isinstance(item, (list, tuple)):
            return {"type": "array", "items": [encode(entry) for entry in item]}
        if isinstance(item, Mapping):
            return {"type": "object",
                    "entries": [[str(key), encode(item[key])]
                                for key in sorted(item, key=str)]}
        return {"type": "unsupported", "value": repr(item)}
    return {"identity_version": version, "value": encode(value)}


def operation_identity_digest(operation: Mapping[str, Any]) -> str:
    canonical = json.dumps(canonical_typed_identity(operation), sort_keys=True,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _deep_merge(base: Mapping[str, Any], overlay: Mapping[str, Any]) -> dict:
    result = copy.deepcopy(dict(base))
    for key, value in overlay.items():
        if isinstance(value, Mapping) and isinstance(result.get(key), Mapping):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _candidate_operations(submitted: Mapping[str, Any], expected: tuple[Mapping[str, Any], ...]):
    by_id = {row["operation_id"]: row for row in expected}
    if "operation_objects" in submitted:
        ops = [copy.deepcopy(row) for row in submitted["operation_objects"]]
    elif "operation_ids_override" in submitted:
        ops = []
        for operation_id in submitted["operation_ids_override"]:
            if operation_id in by_id:
                ops.append(copy.deepcopy(by_id[operation_id]))
            else:
                ops.append({"operation_id": operation_id})
    else:
        ops = [copy.deepcopy(row) for row in expected]
    for edit in submitted.get("operation_id_edits", []) or []:
        remove = edit.get("remove")
        add = edit.get("add")
        if remove:
            ops = [row for row in ops if row.get("operation_id") != remove]
        if add:
            ops.append({"operation_id": add})
    for edit in submitted.get("operation_disposition_edits", []) or []:
        for row in ops:
            if row.get("operation_id") == edit.get("operation_id"):
                row["eligible_disposition"] = edit.get("to")
                row.setdefault("axis_bindings", {})["eligibility"] = edit.get("to")
                if "native_evidence" in edit:
                    row["native_evidence"] = edit["native_evidence"]
    for edit in submitted.get("operation_status_edits", []) or []:
        for row in ops:
            if row.get("operation_id") != edit.get("operation_id"):
                continue
            axis = row.setdefault("axis_bindings", {})
            for key in ("eligibility", "execution", "result"):
                if key in edit:
                    axis[key] = edit[key]
            for key in ("denominator", "numerator", "proof_source",
                        "native_state", "substantive_cells"):
                if key in edit:
                    row[key] = edit[key]
            if edit.get("assert_complete"):
                row["asserted_complete"] = True
    return ops


def _ids(ops):
    return [row.get("operation_id") for row in ops]


def _diff(expected_ids, candidate_ids):
    expected_set = set(expected_ids)
    candidate_set = set(candidate_ids)
    counts = {}
    for operation_id in candidate_ids:
        counts[operation_id] = counts.get(operation_id, 0) + 1
    duplicate = sorted(key for key, count in counts.items() if count > 1)
    return {
        "missing": sorted(expected_set - candidate_set),
        "extra": sorted(candidate_set - expected_set),
        "duplicate": duplicate,
        "semantic_mismatch": [],
    }


def _partitions(ops):
    eligibility = {"ELIGIBLE": [], "PROHIBITED": [], "INAPPLICABLE_PROVED": [],
                   "HELD": [], "UNKNOWN": []}
    execution = {"NOT_STARTED": [], "PENDING": [], "COMPLETED": [],
                 "UNSUPPORTED_RUNTIME": [], "ERROR": []}
    result = {"SUPPORTED": [], "OBSERVED_ZERO": [], "VALID_NULL": [],
              "DIFFUSE": [], "VALID_EMPTY": [], "ZERO_SUPPORT": [],
              "UNSUPPORTED": [], "UNKNOWN": []}
    for row in ops:
        operation_id = row.get("operation_id")
        axis = row.get("axis_bindings", {})
        eligibility.setdefault(axis.get("eligibility", "UNKNOWN"), []).append(operation_id)
        execution.setdefault(axis.get("execution", "NOT_STARTED"), []).append(operation_id)
        result.setdefault(axis.get("result", "UNKNOWN"), []).append(operation_id)
    return eligibility, execution, result


def _decision(*, claim_grade, decision, ceiling, reasons, handle,
              expected_ids, diff, ops, extra=None):
    eligibility, execution, result = _partitions(ops)
    payload = {
        "contract_id": CONTRACT_ID,
        "claim_grade_requested": claim_grade,
        "decision": decision,
        "grade_ceiling": ceiling,
        "reason_rule_ids": list(reasons),
        "policy_ref": handle.policy_ref(),
        "considered_expected_ids": sorted(expected_ids),
        "submitted_id_diff": diff,
        "eligibility_partition": eligibility,
        "execution_partition": execution,
        "result_partition": result,
        "unresolved_original_obligations": copy.deepcopy(ORIGINAL_OBLIGATIONS),
        "trusted_native_provenance": "NOT_PRESENT",
        "published_original_grant": "UNISSUED",
        "actual_consumer_values_read": None,
        "positive_claim_scopes": ["TEST_ONLY_POLICY_SHAPE"]
        if ceiling == "LOCAL_ONLY_POLICY_CONSISTENT" else [],
        "held_requirements": ["G3", "G6", "G7", "G8"],
        "expected_count": len(expected_ids),
        "submitted_count": len(ops),
    }
    if extra:
        payload.update(extra)
    return payload


DYNAMIC_OPERATION_KEYS = {
    "axis_bindings", "eligible_disposition", "native_evidence",
    "denominator", "numerator", "proof_source", "native_state",
    "substantive_cells", "asserted_complete",
}
ALLOWED_CLAIM_KINDS = {
    "POLICY_ONLY", "POLICY_STATUS_CHECK_ONLY",
    "POLICY_ATTEMPT_ACCOUNTING_ONLY", "EXECUTED_NATIVE",
}


def _immutable_operation(operation: Mapping[str, Any]) -> dict:
    return {key: copy.deepcopy(value) for key, value in operation.items()
            if key not in DYNAMIC_OPERATION_KEYS}


def _expected_occurrences(handle: PinnedPolicyHandle) -> dict:
    if handle.variant_id == "CANONICAL_V1":
        universes = handle.synthetic.get("test_universes", [])
    else:
        variant = next((row for row in handle.synthetic.get(
            "independent_materialized_variants", [])
            if row.get("variant_id") == handle.variant_id), None)
        universes = variant.get("expected_universes", []) if variant else []
    out = {}
    for universe in universes:
        for occurrence in universe.get("occurrences", []):
            out[occurrence["occurrence_ref"]] = occurrence
    return out


def _occurrence_problem(submitted: Mapping[str, Any], handle: PinnedPolicyHandle) -> str:
    if "occurrence_objects" not in submitted:
        return ""
    supplied = submitted["occurrence_objects"]
    if not isinstance(supplied, list):
        return "UNSUPPORTED_OCCURRENCE_TRANSPORT"
    if not supplied:
        return ""
    expected = _expected_occurrences(handle)
    refs = []
    for occurrence in supplied:
        if not isinstance(occurrence, Mapping) or "occurrence_ref" not in occurrence:
            return "INVALID_OCCURRENCE_OBJECT"
        ref = occurrence["occurrence_ref"]
        refs.append(ref)
        if ref not in expected:
            return "UNKNOWN_OCCURRENCE_REF"
        if operation_identity_digest(occurrence) != operation_identity_digest(expected[ref]):
            return "OCCURRENCE_SEMANTIC_MISMATCH"
    if len(refs) != len(set(refs)):
        return "DUPLICATE_OCCURRENCE_REF"
    return ""


def _status_blocker(expected_by_id, candidate_ops, submitted, claim_kind,
                    typed_axes):
    allowed_eligibility = set(typed_axes.get("eligibility", []))
    allowed_execution = set(typed_axes.get("execution", []))
    allowed_result = set(typed_axes.get("result", []))
    for row in candidate_ops:
        operation_id = row.get("operation_id")
        original = expected_by_id.get(operation_id)
        if original is None:
            continue
        original_eligibility = original.get(
            "eligible_disposition",
            original.get("axis_bindings", {}).get("eligibility"))
        final_eligibility = row.get(
            "eligible_disposition",
            row.get("axis_bindings", {}).get("eligibility"))
        if final_eligibility not in allowed_eligibility:
            return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
        if final_eligibility != original_eligibility:
            if (original.get("topology") == "CROSS_UNIT_REFUSED"
                    and final_eligibility == "ELIGIBLE"
                    and not submitted.get("issued_relation_ref")):
                return ("HOLD_UNIMPLEMENTED_RELATION", ["P03_NO_UNLINKED_CROSS_UNIT"])
            if original_eligibility == "UNKNOWN":
                return ("REFUSE_STATUS", ["P05_HELD_ROLE", "P07_SEPARATE_STATES"])
            if original_eligibility in {"PROHIBITED", "INAPPLICABLE_PROVED"}:
                return ("REFUSE_STATUS", [
                    "P02_NO_ADMIN_AS_CONDITION", "P04_NOT_ADMINISTERED",
                    "P07_SEPARATE_STATES"])
            return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
        axis = row.get("axis_bindings", {})
        execution = axis.get("execution", "NOT_STARTED")
        result = axis.get("result", "UNKNOWN")
        if execution not in allowed_execution or result not in allowed_result:
            return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
        if row.get("asserted_complete") and execution == "PENDING":
            return ("REFUSE_STATUS", ["P07_SEPARATE_STATES", "P06_NO_DROP_MULTISETS"])
        if original_eligibility != "ELIGIBLE" and (
                execution != "NOT_STARTED" or result != "UNKNOWN"):
            return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
        if execution == "COMPLETED":
            if result == "SUPPORTED":
                return ("HOLD_TRUSTED_NATIVE",
                        ["P09_RUNTIME_PROVENANCE_HOLD", "P14_FAIL_CLOSED_TRUST"])
            if result in {"OBSERVED_ZERO", "VALID_NULL", "VALID_EMPTY"}:
                if (claim_kind != "POLICY_STATUS_CHECK_ONLY"
                        or row.get("proof_source") != "TEST_ONLY_HAND_DERIVED"):
                    return ("REFUSE_STATUS", ["P07_SEPARATE_STATES",
                                              "P12_EMPTY_NULL_ZERO_DISTINCT"])
                if result == "OBSERVED_ZERO" and (
                        "denominator" not in row or "numerator" not in row):
                    return ("REFUSE_STATUS", ["P07_SEPARATE_STATES",
                                              "P12_EMPTY_NULL_ZERO_DISTINCT"])
            elif result == "UNKNOWN":
                if not (claim_kind == "POLICY_STATUS_CHECK_ONLY"
                        and row.get("native_state") == "UNRESOLVED"
                        and row.get("substantive_cells") == []
                        and "denominator" in row):
                    return ("REFUSE_STATUS", ["P07_SEPARATE_STATES",
                                              "P12_EMPTY_NULL_ZERO_DISTINCT"])
            elif result not in {"OBSERVED_ZERO", "VALID_NULL", "VALID_EMPTY",
                                "UNKNOWN"}:
                return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
            elif claim_kind != "POLICY_STATUS_CHECK_ONLY":
                return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
        elif execution == "PENDING":
            if result != "UNKNOWN":
                return ("REFUSE_STATUS", ["P07_SEPARATE_STATES"])
    return None


def _handle_consistency(handle: PinnedPolicyHandle):
    if handle.commit != DEFAULT_COMMIT or handle.root != DEFAULT_ROOT:
        return ("REFUSE_PIN", ["P00_INDEPENDENT_PIN"])
    try:
        trusted = load_pinned_policy(handle.commit, handle.root, handle.variant_id)
    except Exception:
        return ("REFUSE_PIN", ["P00_INDEPENDENT_PIN"])
    if not handle.verified or not trusted.verified:
        return ("REFUSE_PIN", ["P00_INDEPENDENT_PIN"])
    if (dict(handle.blobs) != dict(trusted.blobs)
            or dict(handle.policy) != dict(trusted.policy)
            or dict(handle.synthetic) != dict(trusted.synthetic)
            or dict(handle.freeze) != dict(trusted.freeze)):
        return ("REFUSE_PIN", ["P00_INDEPENDENT_PIN"])
    if (tuple(handle.expected_ids) != trusted.expected_ids
            or [dict(row) for row in handle.expected_operations]
            != [dict(row) for row in trusted.expected_operations]):
        return ("REFUSE_FRONTIER", ["P06_NO_DROP_MULTISETS"])
    return None


def evaluate_r56_sourcefree_claim(
    submitted_claim: Mapping[str, Any],
    *,
    externally_pinned_policy: Any,
    verified_evidence: Any = None,
) -> dict:
    if not isinstance(submitted_claim, Mapping):
        raise GateRefusal("SUBMISSION_NOT_MAPPING")
    claim = copy.deepcopy(dict(submitted_claim))
    request = claim.get("request", {}) or {}
    submitted = claim.get("submitted", {}) or {}
    claim_grade = request.get("claim_grade", "LOCAL_OPERATOR")
    empty_diff = {"missing": [], "extra": [], "duplicate": [],
                  "semantic_mismatch": []}
    requested_kind = request.get("claim_kind", "POLICY_ONLY")
    submitted_kind = submitted.get("claim_kind")
    if submitted_kind is not None and submitted_kind not in ALLOWED_CLAIM_KINDS:
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_AUTHORITY", ceiling="NONE",
            reasons=["P08_CLAIM_GRADE_CEILING"], handle=externally_pinned_policy,
            expected_ids=externally_pinned_policy.expected_ids,
            diff=empty_diff, ops=[])
    claim_kind = requested_kind
    if (requested_kind == "POLICY_ONLY"
            and submitted_kind in {"POLICY_ONLY", "POLICY_STATUS_CHECK_ONLY",
                                   "POLICY_ATTEMPT_ACCOUNTING_ONLY"}):
        claim_kind = submitted_kind
    elif (requested_kind == "POLICY_ONLY" and submitted_kind == "EXECUTED_NATIVE"):
        claim_kind = "EXECUTED_NATIVE"
    if not isinstance(externally_pinned_policy, PinnedPolicyHandle):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_PIN", ceiling="NONE",
            reasons=["P00_INDEPENDENT_PIN"],
            handle=PinnedPolicyHandle("", "", "", {}, {}, {}, (), (), {}, False),
            expected_ids=(), diff=empty_diff, ops=[])
    handle = externally_pinned_policy
    expected_ids = handle.expected_ids
    expected = handle.expected_operations
    consistency = _handle_consistency(handle)
    if consistency:
        decision, reasons = consistency
        return _decision(
            claim_grade=claim_grade, decision=decision, ceiling="NONE",
            reasons=reasons, handle=handle, expected_ids=expected_ids,
            diff=empty_diff, ops=[])
    allowed_grades = set(handle.policy.get("claim_grades", []))
    if claim_grade not in allowed_grades:
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_AUTHORITY", ceiling="NONE",
            reasons=["P08_CLAIM_GRADE_CEILING"], handle=handle,
            expected_ids=expected_ids, diff=empty_diff, ops=[])
    if claim_kind not in ALLOWED_CLAIM_KINDS:
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_AUTHORITY", ceiling="NONE",
            reasons=["P08_CLAIM_GRADE_CEILING"], handle=handle,
            expected_ids=expected_ids, diff=empty_diff, ops=[])
    claim_variant = (claim.get("external_policy_resolution", {}) or {}).get("variant_id")
    if claim_variant and claim_variant != handle.variant_id:
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_PIN", ceiling="NONE",
            reasons=["P00_INDEPENDENT_PIN"], handle=handle,
            expected_ids=expected_ids, diff=empty_diff, ops=[],
            extra={"policy_pin_verified": True, "variant_mismatch": True})
    if (submitted.get("policy_selector_source") == "CANDIDATE"
            or submitted.get("self_pin") or submitted.get("self_digest")):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_PIN", ceiling="NONE",
            reasons=["P00_INDEPENDENT_PIN"], handle=handle,
            expected_ids=expected_ids, diff=empty_diff, ops=[],
            extra={"policy_pin_verified": True, "candidate_pin": True})
    rename = submitted.get("candidate_supplied_rename")
    if rename:
        destinations = list(rename.values())
        if len(set(destinations)) != len(destinations):
            return _decision(
                claim_grade=claim_grade, decision="REFUSE_FRONTIER", ceiling="NONE",
                reasons=["P00_INDEPENDENT_PIN", "P06_NO_DROP_MULTISETS",
                         "P16_BIJECTIVE_LABEL_RENAME"],
                handle=handle, expected_ids=expected_ids, diff=empty_diff, ops=[],
                extra={"invalid_rename": "NON_INJECTIVE",
                       "duplicate_destination_label": destinations[0]})
    if (submitted.get("candidate_variant_selection")
            and not claim.get("external_policy_resolution", {}).get("variant_id")):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_PIN", ceiling="NONE",
            reasons=["P00_INDEPENDENT_PIN"], handle=handle,
            expected_ids=expected_ids, diff=empty_diff, ops=[],
            extra={"candidate_variant_selection": True})
    for edit in (submitted.get("operation_status_edits", []) or []) + (
            submitted.get("operation_disposition_edits", []) or []):
        if edit.get("operation_id") not in {row["operation_id"] for row in expected}:
            return _decision(
                claim_grade=claim_grade, decision="REFUSE_STATUS", ceiling="NONE",
                reasons=["P07_SEPARATE_STATES"], handle=handle,
                expected_ids=expected_ids, diff=empty_diff, ops=[])
    occurrence_problem = _occurrence_problem(submitted, handle)
    if occurrence_problem:
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FRONTIER", ceiling="NONE",
            reasons=["P01_OCCURRENCE_ROLE_AND_MEASURE",
                     "P06_NO_DROP_MULTISETS"],
            handle=handle, expected_ids=expected_ids, diff=empty_diff, ops=[],
            extra={"occurrence_problem": occurrence_problem})
    if any(edit.get("duplicate_same_qualified_key") or edit.get("copy_occurrence_ref")
           for edit in (submitted.get("occurrence_edits", []) or [])):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FRONTIER", ceiling="NONE",
            reasons=["P01_OCCURRENCE_ROLE_AND_MEASURE",
                     "P06_NO_DROP_MULTISETS"],
            handle=handle, expected_ids=expected_ids, diff=empty_diff, ops=[])

    candidate_ops = _candidate_operations(submitted, expected)
    candidate_ids = _ids(candidate_ops)
    diff = _diff(expected_ids, candidate_ids)
    expected_by_id = {row["operation_id"]: row for row in expected}
    for row in candidate_ops:
        operation_id = row.get("operation_id")
        if operation_id not in expected_by_id:
            continue
        if (operation_identity_digest(_immutable_operation(row))
                != operation_identity_digest(
                    _immutable_operation(expected_by_id[operation_id]))):
            diff["semantic_mismatch"].append(operation_id)
    diff["semantic_mismatch"] = sorted(set(diff["semantic_mismatch"]))

    mutation = submitted.get("K_mutation")
    if mutation:
        reasons = ["P10_EXACT_K_AND_CURRENTNESS"]
        if "conditions" in str(mutation.get("field", "")) or "value" in str(mutation.get("field", "")):
            reasons.append("P15_ACTUAL_CONSUMER")
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_IDENTITY", ceiling="NONE",
            reasons=reasons, handle=handle, expected_ids=expected_ids,
            diff=diff, ops=candidate_ops, extra={"consumer_evidence": None})
    permission = submitted.get("permission") or {}
    if permission.get("current") == "REVOKED":
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_AUTHORITY", ceiling="NONE",
            reasons=["P10_EXACT_K_AND_CURRENTNESS", "P14_FAIL_CLOSED_TRUST"],
            handle=handle, expected_ids=expected_ids, diff=diff, ops=candidate_ops)
    if ((permission.get("returned_host") and permission.get("requested_host")
         and permission.get("returned_host") != permission.get("requested_host"))
            or (permission.get("returned_purpose")
                and permission.get("requested_purpose")
                and permission.get("returned_purpose") != permission.get("requested_purpose"))):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_AUTHORITY", ceiling="NONE",
            reasons=["P10_EXACT_K_AND_CURRENTNESS",
                     "P13_ORIGINAL_ROSTER_CONSERVATION"],
            handle=handle, expected_ids=expected_ids, diff=diff, ops=candidate_ops)

    status_blocker = _status_blocker(
        expected_by_id, candidate_ops, submitted, claim_kind,
        handle.policy.get("typed_status_axes", {}))
    if status_blocker:
        decision, reasons = status_blocker
        return _decision(
            claim_grade=claim_grade, decision=decision, ceiling="NONE",
            reasons=reasons, handle=handle, expected_ids=expected_ids,
            diff=diff, ops=candidate_ops)

    if submitted.get("claim_of_independent_heterogeneity"):
        witnesses = submitted.get("edge_class_witnesses", []) or []
        if len(set(witnesses)) <= 1:
            return _decision(
                claim_grade=claim_grade, decision="REFUSE_FRONTIER", ceiling="NONE",
                reasons=["P06_NO_DROP_MULTISETS", "P08_CLAIM_GRADE_CEILING"],
                handle=handle, expected_ids=expected_ids, diff=diff,
                ops=candidate_ops)

    counted = submitted.get("scientific_counted_operation_ids", []) or []
    if len(counted) != len(set(counted)):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_DUPLICATE_COUNT",
            ceiling="NONE", reasons=["P11_REPLAY_AND_DEDUP"], handle=handle,
            expected_ids=expected_ids, diff=diff, ops=candidate_ops)

    full_claim = bool(
        submitted.get("claim_of_universal_complete")
        or claim_grade in {"GENERIC_SOURCEFREE", "ORIGINAL35_N11"}
        or submitted.get("claims_scope_is_full_universe", True) is not False
    )
    if (diff["missing"] or diff["extra"] or diff["duplicate"]
            or diff["semantic_mismatch"]) and full_claim:
        if (submitted.get("hold_does_not_waive") is False
                and any(expected_by_id.get(operation_id, {}).get(
                    "axis_bindings", {}).get("eligibility") == "HELD"
                    for operation_id in diff["missing"])):
            reasons = ["P06_NO_DROP_MULTISETS",
                       "P13_ORIGINAL_ROSTER_CONSERVATION"]
        elif handle.variant_id != "CANONICAL_V1" and claim_grade == "GENERIC_SOURCEFREE":
            reasons = ["P06_NO_DROP_MULTISETS", "P08_CLAIM_GRADE_CEILING",
                       "P16_BIJECTIVE_LABEL_RENAME"]
        elif claim_grade == "GENERIC_SOURCEFREE":
            reasons = ["P06_NO_DROP_MULTISETS", "P08_CLAIM_GRADE_CEILING"]
        else:
            reasons = ["P06_NO_DROP_MULTISETS"]
        extra = {"expected_missing_count": len(diff["missing"]),
                 "expected_extra_count": len(diff["extra"]),
                 "expected_missing_ids": diff["missing"]}
        if handle.variant_id != "CANONICAL_V1":
            extra["materialized_variant_ref"] = handle.variant_id
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FRONTIER", ceiling="NONE",
            reasons=reasons, handle=handle, expected_ids=expected_ids,
            diff=diff, ops=candidate_ops, extra=extra)

    if submitted.get("native") is True:
        reasons = ["P09_RUNTIME_PROVENANCE_HOLD"]
        if submitted.get("trace"):
            reasons.append("P15_ACTUAL_CONSUMER")
        if submitted.get("attestation"):
            reasons.append("P14_FAIL_CLOSED_TRUST")
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FORGED_EVIDENCE",
            ceiling="NONE", reasons=reasons, handle=handle,
            expected_ids=expected_ids, diff=diff, ops=candidate_ops)
    if submitted.get("native_event_claim") not in {
            None, "", "NOT_ASSERTED", "TRACE_STRING_ONLY", "REQUIRES_R09"}:
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FORGED_EVIDENCE",
            ceiling="NONE", reasons=["P09_RUNTIME_PROVENANCE_HOLD"],
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops)
    if submitted.get("native_event_claim") == "TRACE_STRING_ONLY" or submitted.get("trace"):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FORGED_EVIDENCE",
            ceiling="NONE",
            reasons=["P09_RUNTIME_PROVENANCE_HOLD", "P15_ACTUAL_CONSUMER"],
            handle=handle, expected_ids=expected_ids, diff=diff, ops=candidate_ops)
    if submitted.get("attestation"):
        return _decision(
            claim_grade=claim_grade, decision="REFUSE_FORGED_EVIDENCE",
            ceiling="NONE",
            reasons=["P09_RUNTIME_PROVENANCE_HOLD", "P14_FAIL_CLOSED_TRUST"],
            handle=handle, expected_ids=expected_ids, diff=diff, ops=candidate_ops)
    transport = submitted.get("transport") or {}
    if isinstance(transport, Mapping) and transport.get("type") == "TEST_ONLY_MOCK":
        if claim_grade == "GENERIC_SOURCEFREE":
            return _decision(
                claim_grade=claim_grade, decision="HOLD_GENERIC_R09",
                ceiling="LOCAL_ONLY_POLICY_CONSISTENT",
                reasons=["P09_RUNTIME_PROVENANCE_HOLD", "P14_FAIL_CLOSED_TRUST"],
                handle=handle, expected_ids=expected_ids, diff=diff,
                ops=candidate_ops)
        return _decision(
            claim_grade=claim_grade, decision="HOLD_TRUSTED_NATIVE",
            ceiling="LOCAL_ONLY_POLICY_CONSISTENT",
            reasons=["P09_RUNTIME_PROVENANCE_HOLD", "P14_FAIL_CLOSED_TRUST"],
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops)

    if claim_grade == "ORIGINAL35_N11":
        return _decision(
            claim_grade=claim_grade, decision="HOLD_ORIGINAL_G8", ceiling="NONE",
            reasons=["P13_ORIGINAL_ROSTER_CONSERVATION",
                     "P08_CLAIM_GRADE_CEILING"],
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops,
            extra={"original_U_item": None, "original_U_unit": None,
                   "original_U_app": None, "original_E_pre": None})
    if submitted.get("native_event_claim") == "REQUIRES_R09":
        return _decision(
            claim_grade=claim_grade, decision="HOLD_TRUSTED_NATIVE",
            ceiling="LOCAL_ONLY_POLICY_CONSISTENT",
            reasons=["P09_RUNTIME_PROVENANCE_HOLD", "P14_FAIL_CLOSED_TRUST"],
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops)
    if claim_grade == "GENERIC_SOURCEFREE":
        reasons = ["P08_CLAIM_GRADE_CEILING", "P09_RUNTIME_PROVENANCE_HOLD"]
        if handle.variant_id != "CANONICAL_V1":
            reasons.append("P16_BIJECTIVE_LABEL_RENAME")
        return _decision(
            claim_grade=claim_grade, decision="HOLD_GENERIC_R09",
            ceiling="LOCAL_ONLY_POLICY_CONSISTENT", reasons=reasons,
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops,
            extra={"materialized_variant_ref": handle.variant_id,
                   "expected_missing_ids": diff["missing"],
                   "expected_extra_ids": diff["extra"]})
    if claim_kind == "EXECUTED_NATIVE":
        return _decision(
            claim_grade=claim_grade, decision="HOLD_TRUSTED_NATIVE",
            ceiling="LOCAL_ONLY_POLICY_CONSISTENT",
            reasons=["P09_RUNTIME_PROVENANCE_HOLD", "P14_FAIL_CLOSED_TRUST"],
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops)

    status_edits = submitted.get("operation_status_edits", []) or []
    if status_edits:
        results = {edit.get("result") for edit in status_edits}
        if results <= {"OBSERVED_ZERO"}:
            reasons = ["P07_SEPARATE_STATES", "P12_EMPTY_NULL_ZERO_DISTINCT"]
        elif results <= {"VALID_NULL", "VALID_EMPTY"}:
            reasons = ["P12_EMPTY_NULL_ZERO_DISTINCT"]
        elif "UNKNOWN" in results:
            reasons = ["P07_SEPARATE_STATES", "P12_EMPTY_NULL_ZERO_DISTINCT"]
        else:
            reasons = ["P07_SEPARATE_STATES"]
        return _decision(
            claim_grade=claim_grade, decision="ALLOW_LOCAL_POLICY_CONSISTENT",
            ceiling="LOCAL_ONLY_POLICY_CONSISTENT", reasons=reasons,
            handle=handle, expected_ids=expected_ids, diff=diff,
            ops=candidate_ops)
    if counted and len(counted) == len(set(counted)) and submitted.get("attempts"):
        return _decision(
            claim_grade=claim_grade, decision="ALLOW_LOCAL_POLICY_CONSISTENT",
            ceiling="LOCAL_ONLY_POLICY_CONSISTENT",
            reasons=["P11_REPLAY_AND_DEDUP"], handle=handle,
            expected_ids=expected_ids, diff=diff, ops=candidate_ops)

    reasons = ["P00_INDEPENDENT_PIN", "P06_NO_DROP_MULTISETS",
               "P08_CLAIM_GRADE_CEILING"]
    if handle.variant_id != "CANONICAL_V1":
        reasons.append("P16_BIJECTIVE_LABEL_RENAME")
    extra = {"expected_missing_ids": diff["missing"],
             "expected_extra_ids": diff["extra"]}
    if handle.variant_id != "CANONICAL_V1":
        extra["materialized_variant_ref"] = handle.variant_id
    return _decision(
        claim_grade=claim_grade, decision="ALLOW_LOCAL_POLICY_CONSISTENT",
        ceiling="LOCAL_ONLY_POLICY_CONSISTENT", reasons=reasons,
        handle=handle, expected_ids=expected_ids, diff=diff,
        ops=candidate_ops, extra=extra)


__all__ = [
    "CONTRACT_ID",
    "DEFAULT_COMMIT",
    "DEFAULT_ROOT",
    "GateRefusal",
    "PinnedPolicyHandle",
    "canonical_typed_identity",
    "evaluate_r56_sourcefree_claim",
    "load_pinned_policy",
    "operation_identity_digest",
]
