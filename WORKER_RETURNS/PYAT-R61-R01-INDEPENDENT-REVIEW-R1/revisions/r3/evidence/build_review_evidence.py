"""Build R01V R3 reviewer evidence from the disposable probes (no code edits)."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
RET = Path(__file__).resolve().parents[1]
EVIDENCE = RET / "evidence"
PROBES = RET / "probes"
REPLAY = RET / "replay"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PROBES))

from test_r01v_r3_reviewer import (  # noqa: E402
    _conditioned_joint_case,
)
from prior_test_r01v_independent import (  # noqa: E402
    _frontier as prior_frontier,
    _inventory as prior_inventory,
    _occ as prior_occurrence,
    _policy as prior_policy,
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": 0.0}
    for suite in suites:
        totals["tests"] += int(suite.attrib.get("tests", 0))
        totals["failures"] += int(suite.attrib.get("failures", 0))
        totals["errors"] += int(suite.attrib.get("errors", 0))
        totals["skipped"] += int(suite.attrib.get("skipped", 0))
        totals["time"] += float(suite.attrib.get("time", 0.0))
    return totals


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    case = _conditioned_joint_case()
    (EVIDENCE / "conditional_joint_repro.txt").write_text(
        json.dumps(case, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    inventory = prior_inventory((
        prior_occurrence("alpha"),
        prior_occurrence("beta", target_role=None),
        prior_occurrence("gamma", target_role=None),
        prior_occurrence("delta", target_role=None),
    ))
    policy = replace(
        prior_policy(j=1, k=3, d=3),
        recursion_relation_ref="REC-REVIEW-1",
        baseline_policy_ref="BASE-REVIEW-1",
    )
    frontier = prior_frontier(inventory, policy)
    forks = [op for op in frontier.operations if op.claim_class == "FORK"]
    recursion = {
        "fork_count": len(forks),
        "branch_recursion_depths": sorted({
            (op.branch_depth, op.recursion_depth) for op in forks
        }),
        "baseline_policy_refs": sorted({op.baseline_policy_ref for op in forks}),
        "recursion_relation_refs": sorted({op.recursion_relation_ref for op in forks}),
        "baseline_ref_present": all(op.baseline_ref is not None for op in forks),
        "held_depth_beyond_issued": sum(
            1 for op in frontier.operations
            if op.disposition == "HELD"
            and "DEPTH_BEYOND_ISSUED_BOUND" in op.reasons
        ),
        "deferred_gap": [
            item for item in frontier.deferred
            if item.get("kind") == "RECURSION_BASELINE_NOT_ENUMERATED"
        ],
        "policy_D": policy.bounds["D"],
        "policy_K": policy.bounds["K"],
    }
    (EVIDENCE / "recursion_diagnostic.txt").write_text(
        json.dumps(recursion, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    counts = {
        "author_suite": junit_counts(REPLAY / "author_suite_junit.xml"),
        "adapted_prior_probes": junit_counts(REPLAY / "adapted_prior_probes_junit.xml"),
        "own_probes": junit_counts(REPLAY / "own_probes_junit.xml"),
    }
    (EVIDENCE / "junit_summary.txt").write_text(
        json.dumps(counts, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    identity = {
        "reviewer_branch": "agent/opencode-pyat-r61-r01v-r3-independent-review-r1",
        "worktree": str(ROOT),
        "startup_and_candidate": "9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5",
        "code_commit": "89774b01990a7d18c10cf4f6e819895776a1a633",
        "startup_parent": "f0c602eddaee14a58d6f0935a587a46fcf96c6db",
        "r2_review": "3ac1e498a08648950d31df0bf52750f9335d24fa",
        "r3_repair_commission": "3470da602618b5c04b1f28885b5ad1835169e2d5",
        "r3_review_commission": "ed6cb8675baacc266ec9c85a566380048d30dded",
        "expectations_commit": "1db7de32131a1ec4191fde6bbe3633a08894c357",
        "local_head": git("rev-parse", "HEAD"),
        "author_remote": git(
            "ls-remote", "origin",
            "refs/heads/agent/opencode-pyat-r61-r01-generic-grammar-r1",
        ),
        "reviewer_remote": git(
            "ls-remote", "origin",
            "refs/heads/agent/opencode-pyat-r61-r01v-r3-independent-review-r1",
        ),
        "changed_paths_from_startup": git(
            "diff", "--name-only",
            "f0c602eddaee14a58d6f0935a587a46fcf96c6db",
            "9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5",
        ).splitlines(),
        "environment": {
            "python": platform.python_version(),
            "python_path": sys.executable,
            "platform": platform.platform(),
        },
    }
    code_paths = (
        "rawlsing_next/universal_grammar/types.py",
        "rawlsing_next/universal_grammar/enumerate.py",
        "rawlsing_next/universal_grammar/native_map.py",
        "rawlsing_next/tests/test_universal_grammar.py",
    )
    identity["code_blobs"] = {
        path: git("rev-parse", f"89774b019:{path}") for path in code_paths
    }
    manifest = json.loads(git(
        "show",
        "9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5:"
        "WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r3/manifest.json",
    ))
    identity["author_report_hashes"] = {
        name: hashlib.sha256(subprocess.check_output([
            "git", "show",
            f"9fbf1ec3bbd569b5fd83cfd9e20cb931523a42c5:"
            f"WORKER_RETURNS/PYAT-R61-R01-IMPLEMENTATION-R1/revisions/r3/{name}",
        ], cwd=ROOT)).hexdigest()
        for name in sorted(manifest["report_artifacts_sha256"])
    }
    (EVIDENCE / "startup_and_identity.json").write_text(
        json.dumps(identity, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (EVIDENCE / "startup_and_identity.txt").write_text(
        "\n".join([
            f"reviewer_branch: {identity['reviewer_branch']}",
            f"worktree: {identity['worktree']}",
            f"startup_and_candidate: {identity['startup_and_candidate']}",
            f"code_commit: {identity['code_commit']}",
            f"startup_parent: {identity['startup_parent']}",
            f"r2_review: {identity['r2_review']}",
            f"r3_repair_commission: {identity['r3_repair_commission']}",
            f"r3_review_commission: {identity['r3_review_commission']}",
            f"expectations_commit: {identity['expectations_commit']}",
            f"local_head: {identity['local_head']}",
            f"author_remote: {identity['author_remote']}",
            f"reviewer_remote: {identity['reviewer_remote']}",
            f"python: {identity['environment']['python']}",
            f"python_path: {identity['environment']['python_path']}",
            f"platform: {identity['environment']['platform']}",
            "changed_paths_from_startup:",
            *[f"  {path}" for path in identity["changed_paths_from_startup"]],
            "code_blobs:",
            *[f"  {path} {blob}" for path, blob in sorted(identity["code_blobs"].items())],
            "author_report_hashes:",
            *[f"  {name} {digest}" for name, digest in sorted(identity["author_report_hashes"].items())],
        ]) + "\n", encoding="utf-8"
    )

    results = {
        "schema": "PYAT_R61_R01V_R3_INDEPENDENT_ORACLE_RESULTS@1",
        "candidate_startup": identity["startup_and_candidate"],
        "candidate_code": identity["code_commit"],
        "frozen_expectations": "EXPECTATIONS.md @ " + identity["expectations_commit"],
        "author_suite": counts["author_suite"],
        "adapted_prior_probes": counts["adapted_prior_probes"],
        "own_probes": counts["own_probes"],
        "A1": {
            "result": "PASS",
            "evidence": "conditioned JOINT/CO_TRAVEL single and multi-condition lowering uses exact derived predicate refs in every JOINT/MARGINAL role; actual I05 baseline/mutation/refusal/restoration/cold join passes",
            "condition_values_distinct": True,
            "multi_condition_dependencies": "derived predicate dependency_refs contain both condition predicate refs",
        },
        "A2": {
            "result": "PASS",
            "evidence": "forged op_id typed refused; semantic change with stale op_id typed refused; recomputed canonical ID lowers SUPPORTED",
        },
        "A3": {
            "result": "PASS",
            "evidence": "unsupported-only frontier keeps exact unsupported IDs and allow_empty_frontier false; truly empty complete frontier true; pending frontier false; partitions conserve all operation IDs",
        },
        "A4": {
            "result": "EXACT_CONTRACT_GAP_HONEST_PRESERVED_LIMITATION",
            "evidence": "FORK recursion_depth=0 separate from branch_depth 1/2; policy baseline and recursion refs carried; deferred RECURSION_BASELINE_NOT_ENUMERATED state EXACT_CONTRACT_GAP; D not used as conditioner-depth bound; no D13 PASS claim",
            "remaining_not_delivered": "independent governed recurrence/baseline enumeration",
        },
        "verdict": "ACCEPT_SCOPED_LOCAL",
        "r03": "R01_SCoped qualification; R02 accepted evidence at R56-R02V r2; recursive/minority R03 coverage remains blocked by A4 generic contract gap",
        "not_reached": [
            "R03 total issuance/U43/Batch and recursive/minority execution",
            "R04 serialized restore/byte custody/revocation",
            "R05 five grades/canonical N10E values-read",
            "R06 F5/F6/F7/F8 and observed temporal pairs",
            "original 35/1890 and U/E_pre",
            "N11/N12, production/CI, J52/W52, Browser runtime",
        ],
    }
    (RET / "independent_oracle_results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest_name = "SHA256manifest.json"
    artifacts = {}
    for path in sorted(RET.rglob("*")):
        if not path.is_file() or path.name == manifest_name:
            continue
        artifacts[path.relative_to(RET).as_posix()] = sha256_file(path)
    manifest = {
        "schema": "PYAT_R61_R01V_R3_SHA256_MANIFEST@1",
        "candidate_startup": identity["startup_and_candidate"],
        "candidate_code": identity["code_commit"],
        "verdict": "ACCEPT_SCOPED_LOCAL",
        "excluded_from_manifest": [manifest_name],
        "self_hash_not_claimed": True,
        "artifacts_sha256": artifacts,
    }
    (RET / manifest_name).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
