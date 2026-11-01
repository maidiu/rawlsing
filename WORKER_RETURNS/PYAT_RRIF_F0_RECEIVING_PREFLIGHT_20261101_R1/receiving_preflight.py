#!/usr/bin/env python3
"""Minimal source-free receiving preflight for the two RRIF code gates.

Reads Git objects only.  Never writes to the repository, never merges, never
executes source-native code, and never grants source/actor/scientific authority.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping


class PreflightError(RuntimeError):
    pass


def _git(repo: str | Path, *args: str, check: bool = True) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        if check:
            raise PreflightError(completed.stderr.strip() or f"git {' '.join(args)} failed")
        return None
    return completed.stdout.strip()


def _resolve_ref(repo: str | Path, ref: str) -> str | None:
    candidates = (ref, f"refs/remotes/origin/{ref}", f"refs/heads/{ref}")
    for candidate in candidates:
        value = _git(repo, "rev-parse", "--verify", candidate, check=False)
        if value:
            return value
    return None


def _diff_paths(repo: str | Path, base: str, head: str) -> list[str]:
    output = _git(repo, "diff", "--name-only", "--no-renames", base, head) or ""
    return [line for line in output.splitlines() if line]


def _blob(repo: str | Path, rev: str, path: str) -> str | None:
    return _git(repo, "rev-parse", "--verify", f"{rev}:{path}", check=False)


def observe_repo(repo: str | Path, allowlist: Mapping[str, Any],
                 premain_ref: str | None = None) -> dict[str, Any]:
    premain_ref = premain_ref or allowlist["premain_ref"]
    premain_head = _resolve_ref(repo, premain_ref)
    if not premain_head:
        raise PreflightError(f"PREMAIN ref not found: {premain_ref}")
    observed: dict[str, Any] = {"premain_head": premain_head, "candidates": {}}
    pin = allowlist["premain_pin"]
    for gate_id, gate in allowlist["gates"].items():
        branch = gate["candidate_branch"]
        sha = _resolve_ref(repo, branch)
        reviewer_sha = _resolve_ref(repo, gate["review_branch"])
        payload_blobs: dict[str, dict[str, str | None]] = {}
        for item in gate["payload"]:
            path = item["path"]
            payload_blobs[path] = {
                "before": _blob(repo, pin, path),
                "after": _blob(repo, sha, path) if sha else None,
            }
        observed["candidates"][gate_id] = {
            "sha": sha,
            "changed": _diff_paths(repo, pin, sha) if sha else [],
            "payload_blobs": payload_blobs,
            "reviewer_sha": reviewer_sha,
        }
    return observed


def _blocker(result: dict[str, Any], text: str) -> None:
    result["blockers"].append(text)


def _matches(required: Mapping[str, Any], actual: Any) -> list[str]:
    problems: list[str] = []
    if not isinstance(actual, Mapping):
        return ["missing test receipt"]
    for key, expected in required.items():
        if key not in actual:
            problems.append(f"missing test receipt field {key}")
        elif actual[key] != expected:
            problems.append(f"test receipt {key}={actual[key]!r}, required {expected!r}")
    return problems


def evaluate_receiving(allowlist: Mapping[str, Any], receipts: Mapping[str, Any],
                       observed: Mapping[str, Any]) -> dict[str, Any]:
    """Pure fail-closed evaluation of the receiving state.

    ``observed`` is the Git-observed state. Synthetic unit tests can supply it
    directly; the CLI builds it with :func:`observe_repo`.
    """
    result: dict[str, Any] = {
        "schema": "PYAT_RRIF_F0_PREFLIGHT_DECISION@1.0.0",
        "premain_pin": allowlist["premain_pin"],
        "observed_premain_head": observed.get("premain_head"),
        "gates": {},
        "selectable_payload": [],
        "blockers": [],
        "receiving_ready": False,
        "authority": "NONE__PREFLIGHT_ONLY",
    }

    if observed.get("premain_head") != allowlist["premain_pin"]:
        _blocker(result, "PREMAIN_HEAD_CHANGED_OR_MISMATCH")

    payload_sets: dict[str, set[str]] = {}
    for gate_id, gate in allowlist["gates"].items():
        payload_sets[gate_id] = {item["path"] for item in gate["payload"]}
    gate_ids = list(payload_sets)
    for index, left in enumerate(gate_ids):
        for right in gate_ids[index + 1:]:
            overlap = payload_sets[left] & payload_sets[right]
            if overlap:
                _blocker(result, f"PAYLOAD_COLLISION {left} vs {right}: {sorted(overlap)}")
    global_blocked = bool(result["blockers"])

    for gate_id, gate in allowlist["gates"].items():
        gate_result: dict[str, Any] = {
            "candidate_sha": gate["candidate_sha"],
            "status": "BLOCKED",
            "blockers": [],
            "review_required": True,
            "selectable": False,
        }
        observed_gate = observed.get("candidates", {}).get(gate_id, {})
        sha = observed_gate.get("sha")
        if sha != gate["candidate_sha"]:
            gate_result["blockers"].append(
                f"CANDIDATE_SHA_MISMATCH observed={sha} required={gate['candidate_sha']}"
            )

        payload_paths = payload_sets[gate_id]
        evidence_prefixes = tuple(gate.get("branch_evidence_prefixes", ()))
        for path in observed_gate.get("changed", []):
            if path in payload_paths:
                continue
            if any(path.startswith(prefix) for prefix in evidence_prefixes):
                continue
            gate_result["blockers"].append(f"CHANGED_PATH_OUTSIDE_ALLOWLIST {path}")

        for item in gate["payload"]:
            observed_blobs = observed_gate.get("payload_blobs", {}).get(item["path"], {})
            if observed_blobs.get("before") != item["before_blob"]:
                gate_result["blockers"].append(
                    f"BEFORE_BLOB_MISMATCH {item['path']} observed={observed_blobs.get('before')} required={item['before_blob']}"
                )
            if observed_blobs.get("after") != item["after_blob"]:
                gate_result["blockers"].append(
                    f"AFTER_BLOB_MISMATCH {item['path']} observed={observed_blobs.get('after')} required={item['after_blob']}"
                )

        reviewer_sha = observed_gate.get("reviewer_sha")
        if not reviewer_sha:
            gate_result["blockers"].append("REVIEWER_BRANCH_ABSENT")
        elif reviewer_sha == allowlist["premain_pin"]:
            gate_result["blockers"].append("REVIEWER_BRANCH_STILL_AT_PREMAIN_NO_RETURN")
        elif reviewer_sha == gate["candidate_sha"]:
            gate_result["blockers"].append("REVIEWER_BRANCH_EQUALS_CANDIDATE")

        gate_receipts = receipts.get("receipts", {}).get(gate_id, {})
        review = gate_receipts.get("review")
        if not isinstance(review, Mapping):
            gate_result["blockers"].append("MISSING_EXACT_INDEPENDENT_REVIEW_RECEIPT")
        else:
            if review.get("verdict") != gate["review_verdict_required"]:
                gate_result["blockers"].append(
                    f"REVIEW_VERDICT {review.get('verdict')!r} != {gate['review_verdict_required']!r}"
                )
            if review.get("reviewed_sha") != gate["candidate_sha"]:
                gate_result["blockers"].append("REVIEW_DOES_NOT_BIND_EXACT_CANDIDATE_SHA")
            if review.get("reviewer_branch") != gate["review_branch"]:
                gate_result["blockers"].append("REVIEWER_BRANCH_MISMATCH")
            if not review.get("receipt_path"):
                gate_result["blockers"].append("REVIEW_RECEIPT_PATH_MISSING")
            if review.get("reviewer_distinct_from_author") is not True:
                gate_result["blockers"].append("REVIEWER_NOT_DISTINCT_FROM_AUTHOR")
            if review.get("reviewer_sha") != reviewer_sha:
                gate_result["blockers"].append("REVIEWER_SHA_DOES_NOT_MATCH_LIVE_BRANCH")

        actual_tests = gate_receipts.get("tests")
        for name, required in gate["required_test_receipts"].items():
            problems = _matches(required, (actual_tests or {}).get(name))
            for problem in problems:
                gate_result["blockers"].append(f"TEST_RECEIPT {name}: {problem}")

        owner_required = gate.get("owner_decision_required")
        if owner_required:
            owner = gate_receipts.get("owner_decision")
            if not isinstance(owner, Mapping):
                gate_result["blockers"].append("MISSING_M2_OWNER_COMPATIBILITY_DECISION")
            else:
                if owner.get("decision") not in owner_required["decision_values_allowing_accept"]:
                    gate_result["blockers"].append(
                        f"M2_OWNER_DECISION {owner.get('decision')!r} does not allow acceptance"
                    )
                if owner.get("reviewed_sha") != gate["candidate_sha"]:
                    gate_result["blockers"].append("M2_OWNER_DECISION_DOES_NOT_BIND_EXACT_CANDIDATE_SHA")
                if list(owner.get("conflict_tests", [])) != owner_required["exact_conflict_tests"]:
                    gate_result["blockers"].append("M2_OWNER_DECISION_CONFLICT_TEST_SET_MISMATCH")
                if not owner.get("owner") or not owner.get("decision_ref"):
                    gate_result["blockers"].append("M2_OWNER_DECISION_LACKS_OWNER_OR_REFERENCE")

        if global_blocked:
            gate_result["blockers"].append("GLOBAL_PREFLIGHT_BLOCKER")
        gate_result["selectable"] = not gate_result["blockers"]
        gate_result["status"] = "SELECTABLE" if gate_result["selectable"] else "BLOCKED"
        if gate_result["selectable"]:
            result["selectable_payload"].extend(item["path"] for item in gate["payload"])
        result["gates"][gate_id] = gate_result

    result["receiving_ready"] = (
        not global_blocked and all(g["selectable"] for g in result["gates"].values())
    )
    if not result["receiving_ready"] and not global_blocked:
        result["blockers"].append("RECEIVING_NOT_READY_ALL_GATES")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--allowlist", required=True)
    parser.add_argument("--receipts")
    parser.add_argument("--premain-ref")
    parser.add_argument("--json-out")
    args = parser.parse_args(argv)

    allowlist = json.loads(Path(args.allowlist).read_text(encoding="utf-8"))
    receipts = (
        json.loads(Path(args.receipts).read_text(encoding="utf-8"))
        if args.receipts
        else {"receipts": {}}
    )
    try:
        observed = observe_repo(args.repo, allowlist, args.premain_ref)
    except PreflightError as exc:
        print(json.dumps({"schema": "PYAT_RRIF_F0_PREFLIGHT_DECISION@1.0.0",
                          "error": str(exc), "receiving_ready": False}, indent=2))
        return 2
    decision = evaluate_receiving(allowlist, receipts, observed)
    rendered = json.dumps(decision, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if decision["receiving_ready"] else 2


if __name__ == "__main__":
    sys.exit(main())
