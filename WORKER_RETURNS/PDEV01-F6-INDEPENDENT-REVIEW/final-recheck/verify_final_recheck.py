"""Focused independent recheck of F6 candidate 22d671 against review 23edffb32.

Reads the exact disposable candidate snapshot and the prior review evidence.
Writes only under WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/final-recheck/.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
SNAP = Path((REVIEW / "evidence/snapshot.path").read_text().strip())
CAND = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-f6")
CAND_COMMIT = "22d6712090970597e0c161b9f12eaece84bda5c5"
PRIOR_COMMIT = "23edffb32141c133c8b45b723bb23f092928115c"
CAND_ROOT = SNAP / "WORKER_RETURNS/PDEV01-F6-COMPARISON"
F6P = CAND_ROOT / "stage/F6P/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
for p in (F6P, F6P / "native", F6P / "oracle", F6P / "tests"):
    sys.path.insert(0, str(p))

from f6p_fixtures import build, request  # noqa: E402
import f6p_partial_bound_evidence_consumer as C  # noqa: E402

PRIOR = REVIEW.parent / "evidence/replay_f6_review.json"
PRIOR = json.loads(PRIOR.read_text())
EVIDENCE = CAND_ROOT / "evidence/replay_f6.json"
SHAPE = CAND_ROOT / "evidence/f6p-receiver-comparison.json"
ROOT_LIMIT = CAND_ROOT / "evidence/checkout_root_hash_limit.json"
F6C_MANIFEST = CAND_ROOT / "evidence/f6c/F6C_OUTPUT_MANIFEST.json"
F6C_HIST = "WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(CAND), "show", f"{commit}:{path}"],
        check=True, capture_output=True,
    ).stdout


def sidecar(value):
    return {
        "bundle_hash": value["native_bundle"]["content_hash"],
        "conditional": value["native_conditional_consumer"],
    }


def semantic_view(result, bundle, world):
    fields = (
        "bundle_decision", "target_joint_status", "uncovered_target_mass",
        "covered_subprobability", "evidence_state", "evidence_reasons",
        "supported_point", "bounds", "exclusions", "sampling", "transport",
        "real_use_authorized", "no_route_probability", "no_selection_weight",
        "consumer_id",
    )
    out = {field: result.get(field) for field in fields}
    out["world"] = world
    out["bundle_decision"] = bundle.get("decision")
    out["target_joint_status"] = bundle.get("target_joint_status")
    product = dict(result.get("source_product") or {})
    product.pop("module_file", None)
    out["source_product"] = product
    return out


def main() -> int:
    evidence = json.loads(EVIDENCE.read_text())
    shape = json.loads(SHAPE.read_text())
    limit = json.loads(ROOT_LIMIT.read_text())
    manifest = json.loads(F6C_MANIFEST.read_text())

    # Exact candidate tree and scope.
    names = subprocess.run(
        ["git", "-C", str(CAND), "show", "--format=", "--name-only", CAND_COMMIT],
        check=True, capture_output=True, text=True,
    ).stdout.splitlines()
    names = [name for name in names if name]
    assert names and all(name.startswith("WORKER_RETURNS/PDEV01-F6-COMPARISON/")
                         for name in names), names

    # Raw exception from the actual snapshot consumer.
    bundle = build("B", "W2_mixed_eligibility_trap")
    result = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    try:
        sidecar(result)
    except Exception as exc:
        assert type(exc) is KeyError
        assert exc.args == ("native_bundle",)
        assert str(exc) == "'native_bundle'"
        raw = {
            "type": type(exc).__name__,
            "args": list(exc.args),
            "str": str(exc),
            "first_missing_field": "native_bundle",
            "f6p_has_native_bundle": "native_bundle" in result,
            "f6p_has_native_conditional_consumer": "native_conditional_consumer" in result,
        }
    else:
        raise AssertionError("F6P unexpectedly satisfied the WP2 sidecar shape")

    boundary = evidence["current_receiver"]["boundary_check"]
    assert boundary["raw_exception_type"] == raw["type"]
    assert boundary["raw_exception_args"] == raw["args"]
    assert boundary["raw_exception_str"] == raw["str"]
    assert boundary["raw_exception_observed"] is True
    assert boundary["wp2_receiver_executed"] is False
    assert boundary["observed_effect"] is None
    assert shape["receiver_shape_check"]["wp2_receiver_executed"] is False
    assert shape["receiver_shape_check"]["observed_effect"] is None

    label = boundary["authored_diagnostic_label"]
    assert label.startswith("COMPARISON_LOCAL_")
    assert label in (CAND_ROOT / "run_comparison.py").read_text()
    assert label not in (F6P / "f6p_partial_bound_evidence_consumer.py").read_text()
    assert label not in (CAND_ROOT / "stage/wp2/wp2.py").read_text()
    assert not any(
        json.loads(json.dumps(value)).get(key) == "NO_NONPARENT_OPTIONS_READ"
        for value in (evidence, shape) for key in ("read_effect",) if isinstance(value, dict)
    )
    old_effects = ("NO_NONPARENT_OPTIONS_READ", "NO_F6M_E04_JOIN")
    found_old_effects = []
    for p in CAND_ROOT.rglob("*"):
        if p.is_file():
            text = p.read_text(errors="replace")
            found_old_effects.extend(term for term in old_effects if term in text)
    assert not found_old_effects, found_old_effects

    # Exact historical F6C output bodies.
    historical = {}
    for key in ("A", "A0", "B"):
        path = CAND_ROOT / f"evidence/f6c/wp2_sub_{key}.json"
        actual = path.read_bytes()
        expected = manifest["outputs"][key]
        hist = git_bytes("c1ebe091fa2bd12b254e5599cf37975fe438d462",
                         f"{F6C_HIST}/wp2_sub_{key}.json")
        ok = (
            hashlib.sha256(actual).hexdigest() == expected["sha256"]
            and git_blob(path) == expected["git_blob"]
            and actual == hist
        )
        assert ok, key
        historical[key] = {
            "bytes": len(actual),
            "sha256": hashlib.sha256(actual).hexdigest(),
            "git_blob": git_blob(path),
            "exact_historical_bytes": True,
        }
    assert manifest["outputs_present_here"] is True
    assert manifest["receipt_contains_output_bodies"] is False
    assert all(manifest["observations"].values())

    # Checkout-root hash limit and semantic equality, using the prior review.
    cand_hashes = {
        world: row["candidate_output_hash"]
        for world, row in PRIOR["candidate_summary_comparison"].items()
    }
    review_hashes = {
        world: row["review_output_hash"]
        for world, row in PRIOR["candidate_summary_comparison"].items()
    }
    assert limit["candidate_output_hashes"] == cand_hashes
    assert limit["review_output_hashes"] == review_hashes
    assert limit["path_only_difference"] is True
    assert limit["semantic_fields_equal"] is True
    assert "module_file" in limit["cause"]

    snap_bundle = build("B", "W1_full_coverage_disjoint")
    snap_result = C.consume_f6m_evidence(
        snap_bundle, request("W1_full_coverage_disjoint"))
    snap_view = semantic_view(snap_result, snap_bundle, "W1_full_coverage_disjoint")
    cand_w1 = shape["results"]["W1_full_coverage_disjoint"]
    prior_w1 = PRIOR["replay"]["W1_full_coverage_disjoint"]["summary"]
    for other, name in ((cand_w1, "candidate"), (prior_w1, "prior")):
        normalized = {key: deepcopy(other[key]) for key in snap_view if key in other}
        normalized["source_product"] = dict(normalized.get("source_product") or {})
        normalized["source_product"].pop("module_file", None)
        assert snap_view == normalized, name
    assert snap_result["output_hash"] not in cand_hashes.values()
    assert snap_result["output_hash"] not in review_hashes.values()

    # Correction test receipts and exact candidate file hashes.
    corr_logs = {}
    for seed in (0, 1):
        p = REVIEW / f"logs/correction_seed{seed}.log"
        text = p.read_text()
        assert "4 passed" in text, p
        corr_logs[f"seed{seed}"] = {"sha256": sha(p), "tail": text.strip().splitlines()[-1]}

    seed0 = (CAND_ROOT / "evidence/run-comparison.seed0.json").read_bytes()
    seed1 = (CAND_ROOT / "evidence/run-comparison.seed1.json").read_bytes()
    comparison_output = {
        "seed0_sha256": hashlib.sha256(seed0).hexdigest(),
        "seed1_sha256": hashlib.sha256(seed1).hexdigest(),
        "seed0_equals_seed1": seed0 == seed1,
        "same_checkout_scope": True,
    }
    assert seed0 == seed1

    output = {
        "schema": "PDEV01_F6_FINAL_RECHECK_EVIDENCE@1.0.0",
        "candidate_commit": CAND_COMMIT,
        "review_commit": PRIOR_COMMIT,
        "snapshot": {
            "path": str(SNAP),
            "files": len([p for p in CAND_ROOT.rglob("*") if p.is_file()]),
            "snapshot_receipt_sha256": sha(REVIEW / "evidence/SNAPSHOT_RECEIPT.json"),
        },
        "candidate_commit_files_all_in_comparison_root": True,
        "raw_keyerror": raw,
        "diagnostic_ownership": {
            "label": label,
            "authored_in_run_comparison": True,
            "emitted_by_f6p": False,
            "emitted_by_wp2": False,
            "wp2_receiver_executed": False,
            "observed_effect": None,
            "old_effect_claims_absent": True,
        },
        "shape_evidence": {
            "raw_exception": shape["receiver_shape_check"]["raw_exception_type"],
            "args": shape["receiver_shape_check"]["raw_exception_args"],
            "partial_bounds_reach_current_wp2_receiver": shape["conclusion"]["partial_bounds_reach_current_wp2_receiver"],
            "wp2_receiver_executed": shape["conclusion"]["wp2_receiver_executed"],
        },
        "f6c_historical_outputs": {
            "manifest_sha256": sha(F6C_MANIFEST),
            "outputs": historical,
            "outputs_present_here": True,
            "receipt_contains_output_bodies": False,
            "observations": manifest["observations"],
        },
        "checkout_root_hash_limit": {
            "candidate_hashes": cand_hashes,
            "review_hashes": review_hashes,
            "snapshot_w1_output_hash": snap_result["output_hash"],
            "semantic_fields_equal": True,
            "path_only_difference": True,
            "cause": limit["cause"],
            "scope": limit["scope"],
        },
        "correction_tests": corr_logs,
        "comparison_output": comparison_output,
        "exact_tree_scope_note": "Candidate correction commit 22d671 changed only WORKER_RETURNS/PDEV01-F6-COMPARISON; production tree content remains the aa18b6b85 content used by the prior exact-tree scan.",
        "scoped_verdict": "ACCEPT_ENGINEERING_CORRECTION__SCIENCE_AUTHORITY_HOLD_UNCHANGED",
        "limits": [
            "Exact candidate snapshot 22d671 only; no original source or production adoption.",
            "F6M/F6P remain sourcefree TEST_ONLY artifacts.",
            "Checkout-root output hashes are path-dependent; only same-checkout seed identity is claimed.",
            "Historical F6C outputs are embedded separately; receipt bodies are not self-contained.",
        ],
    }
    out = REVIEW / "evidence/final_recheck_evidence.json"
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "raw": raw,
        "label": label,
        "f6c": historical,
        "snapshot_w1_hash": snap_result["output_hash"],
        "correction_tests": corr_logs,
        "verdict": output["scoped_verdict"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
