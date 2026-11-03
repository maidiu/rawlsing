"""Independent F6 comparison replay — reviewer-owned read-only checks.

This script writes only under WORKER_RETURNS/PDEV01-F6-INDEPENDENT-REVIEW/.
It imports the candidate's staged F6P implementation but never calls the
candidate's `run_comparison.py` (that script writes the candidate evidence).
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
CAND = REVIEW.parent / "PDEV01-F6-COMPARISON"
F6P = CAND / "stage/F6P/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
F6P_REVIEWED = CAND / "stage/F6P-reviewed/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
SHA = "aa18b6b8547c954d844bb0dcf94f70e2e14f15b0"
STARTUP = "773bb412a820949f13a7178b6671327cd56a3bf1"

for p in (F6P, F6P / "native", F6P / "oracle", F6P / "tests"):
    sys.path.insert(0, str(p))

from f6p_fixtures import build, request  # noqa: E402
import f6p_partial_bound_evidence_consumer as C  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

WORLDS = (
    "W1_full_coverage_disjoint",
    "W2_mixed_eligibility_trap",
    "W7_source_excluded_all_strata",
    "W3_minority_whole_stratum_absent",
)
SUMMARY_FIELDS = (
    "world", "bundle_decision", "target_joint_status", "uncovered_target_mass",
    "covered_subprobability", "evidence_state", "evidence_reasons",
    "supported_point", "bounds", "exclusions", "sampling", "transport",
    "real_use_authorized", "no_route_probability", "no_selection_weight",
    "output_hash", "consumer_id", "source_product",
)


def blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_hash(value) -> str:
    """JSON-stable hash for historical receipts that contain numeric floats."""
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode()
    ).hexdigest()


def cell_map(cells) -> dict[str, str]:
    if isinstance(cells, dict):
        return dict(cells)
    return {"|".join(cell["categories"]): cell["probability"] for cell in cells or []}


def bounds_map(bounds) -> dict[str, tuple[str, str]]:
    return {"|".join(cell["categories"]): (cell["lower"], cell["upper"])
            for cell in bounds or []}


def sidecar(value):
    """The exact expression at the pinned wp2.py path/line 94."""
    return {
        "bundle_hash": value["native_bundle"]["content_hash"],
        "conditional": value["native_conditional_consumer"],
    }


def summarize(world: str):
    bundle = build("B", world)
    result = C.consume_f6m_evidence(bundle, request(world))
    out = {field: result.get(field) for field in SUMMARY_FIELDS}
    out["world"] = world
    out["bundle_decision"] = bundle.get("decision")
    out["target_joint_status"] = bundle.get("target_joint_status")
    out["input_bundle_decision"] = (result.get("input_bundle") or {}).get("decision")
    out["input_bundle_target_joint_status"] = (
        result.get("input_bundle") or {}).get("target_joint_status")
    out["input_bundle_content_hash"] = (result.get("input_bundle") or {}).get("content_hash")
    out["bias_sensitivity_bounds"] = result.get("bias_sensitivity_bounds")
    out["scientific_ceiling"] = result.get("scientific_ceiling")
    return bundle, result, out


def assert_bounds(result: dict, world: str) -> dict:
    bounds = result.get("bounds") or []
    bias = result.get("bias_sensitivity_bounds") or []
    covered = cell_map(result.get("covered_subprobability"))
    assert len(bounds) == 4, (world, bounds)
    assert len(bias) == 4, (world, bias)
    base = {}
    for cell in bounds:
        key = "|".join(cell["categories"])
        lo, hi = Q(cell["lower"]), Q(cell["upper"])
        assert lo <= hi, (world, key, lo, hi)
        assert key in covered, (world, key, covered)
        assert lo <= Q(covered[key]) <= hi, (world, key, lo, covered[key], hi)
        base[key] = (lo, hi)
    for cell in bias:
        key = "|".join(cell["categories"])
        lo, hi = Q(cell["lower"]), Q(cell["upper"])
        assert lo <= hi, (world, key, lo, hi)
        assert key in base, (world, key)
        assert lo <= base[key][0] and hi >= base[key][1], (world, key, lo, hi, base[key])
    return {"bounds": bounds, "bias_sensitivity_bounds": bias,
            "all_lower_le_upper": True, "covered_inside_bounds": True,
            "bias_widens_base": True}


def check_world(world: str, oracle: dict) -> dict:
    bundle, result, summary = summarize(world)
    case = oracle["cases"][world]["oracle"]
    expected_uncovered = case.get("uncovered_target_mass",
                                  case.get("expected_uncovered_target_mass"))
    assert result["uncovered_target_mass"] == expected_uncovered, (world, result["uncovered_target_mass"])
    if world == "W1_full_coverage_disjoint":
        assert result["evidence_state"] == "SUPPORTED_SYNTHESIS"
        assert result["supported_point"] == case["conditional_probabilities"]
        assert result["exclusions"] == []
        expected_covered = case["joint_cell_probabilities_in_declared_order"]
    else:
        assert result["evidence_state"] == "PARTIAL_IDENTIFICATION"
        assert result["supported_point"] is None
        expected_covered = case.get("covered_subprobability_in_declared_order")
    if expected_covered is not None:
        assert cell_map(result["covered_subprobability"]) == expected_covered, world
    covered_sum = sum(Q(v) for v in cell_map(result["covered_subprobability"]).values())
    uncovered = Q(result["uncovered_target_mass"])
    assert covered_sum + uncovered == 1, (world, covered_sum, uncovered)
    assert result["input_bundle"]["content_hash"] == bundle["content_hash"]
    assert result["input_bundle"]["decision"] == bundle["decision"]
    assert result["input_bundle"]["target_joint_status"] == bundle["target_joint_status"]
    assert result["source_product"]["module_git_blob"] == "2df811d76db258d98d89ffb43c830cb221ff9a7d"
    assert result["source_product"]["module_sha256"] == "2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871"
    assert result["real_use_authorized"] is False
    assert result["no_route_probability"] is True
    assert result["no_selection_weight"] is True
    assert result["transport"]["permitted"] is False
    assert result["sampling"]["weight_defaulted_to_one"] is False
    assert result["sampling"]["weight_imputation"] == "NONE"
    if world in ("W2_mixed_eligibility_trap", "W7_source_excluded_all_strata", "W3_minority_whole_stratum_absent"):
        assert result["conditional"]["state"] == "UNAVAILABLE"
        assert result["conditional"]["reason"] == "NO_COMPLETE_TARGET_JOINT"
    if world == "W2_mixed_eligibility_trap":
        assert {e["source_id"] for e in result["exclusions"]} == {"S_A"}
        assert {e["stratum"] for e in result["exclusions"]} == {"minority"}
        assert {e["reason"] for e in result["exclusions"]} == {"AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT"}
    if world == "W7_source_excluded_all_strata":
        assert {e["source_id"] for e in result["exclusions"]} == {"S_A"}
        assert {e["stratum"] for e in result["exclusions"]} == {"majority", "minority"}
        assert {e["reason"] for e in result["exclusions"]} == {"AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT"}
    if world == "W3_minority_whole_stratum_absent":
        assert {e["source_id"] for e in result["exclusions"]} == {"S_A", "S_B"}
        assert {e["stratum"] for e in result["exclusions"]} == {"minority"}
        assert {e["reason"] for e in result["exclusions"]} == {"NO_SOURCE_STRATUM"}
    bounds_check = assert_bounds(result, world)
    material = {k: v for k, v in result.items() if k != "output_hash"}
    assert result["output_hash"] == semantic_hash(material), world
    normalized = deepcopy(result)
    normalized["source_product"]["module_file"] = "<F6M_MODULE>"
    normalized.pop("output_hash", None)
    semantic_digest = semantic_hash(normalized)
    return {
        "world": world,
        "summary": summary,
        "checks": {
            "oracle_uncovered": True,
            "oracle_covered": expected_covered is not None,
            "mass_conservation": True,
            "point_refusal": result["supported_point"] is None if world != "W1_full_coverage_disjoint" else result["supported_point"] is not None,
            "bounds": bounds_check,
            "source_provenance": True,
            "authority_fields": True,
            "bundle_identity": True,
            "output_hash_self_consistent": True,
        },
        "semantic_digest_stable_across_roots": semantic_digest,
    }


def run_git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REVIEW.parents[1], check=True,
        text=True, capture_output=True,
    ).stdout


def scan(git_sha: str) -> dict:
    terms = (
        "F6P_PARTIAL_BOUND_EVIDENCE",
        "consume_f6m_evidence",
        "uncovered_target_mass",
        "f6_sidecars",
        "native_bundle",
    )
    result = {}
    for term in terms:
        proc = subprocess.run(
            ["git", "grep", "-n", "-I", term, git_sha, "--"],
            cwd=REVIEW.parents[1], check=False, text=True, capture_output=True,
        )
        lines = [line for line in proc.stdout.splitlines() if line]
        paths = sorted({line.split(":", 2)[1] for line in lines if line.count(":") >= 2})
        production = [p for p in paths if p.startswith("rawlsing_next/")]
        result[term] = {
            "match_count": len(lines),
            "paths": paths[:80],
            "rawlsing_next_matches": production,
            "candidate_scope_matches": [p for p in paths if p.startswith("WORKER_RETURNS/PDEV01-F6-COMPARISON/")],
        }
    wp2_paths = [line for line in run_git("ls-tree", "-r", "--name-only", git_sha).splitlines()
                 if line.endswith("wp2.py")]
    n9_path = "rawlsing_next/pre553_n9_n10w_progressive_candidate.py"
    n9_text = run_git("show", f"{git_sha}:{n9_path}")
    guard_path = "rawlsing_next/pre553_source_relations.py"
    guard_text = run_git("show", f"{git_sha}:{guard_path}")
    guard_lines = guard_text.splitlines()
    guard_start = next(i for i, line in enumerate(guard_lines) if line.startswith("def guard_estimand_composition"))
    guard_block = guard_lines[guard_start:guard_start + 42]
    return {
        "scope": "EXACT_TREE_ONLY",
        "tree": git_sha,
        "terms": result,
        "wp2_tracked_paths": wp2_paths,
        "wp2_is_candidate_stage_only": wp2_paths == [
            "WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py"],
        "n9_path": n9_path,
        "n9_sha256": hashlib.sha256(n9_text.encode()).hexdigest(),
        "n9_f6_schema_reference": any(term in n9_text for term in terms),
        "n9_f6_import_reference": "pre553_heterogeneous_synthesis" in n9_text,
        "guard_path": guard_path,
        "guard_return_annotation": "OperationGuardReceipt",
        "guard_returns_guard_only": "return _guard_receipt(" in "\n".join(guard_block),
        "guard_has_f6_schema": any(term in "\n".join(guard_block) for term in terms),
        "guard_block_sha256": hashlib.sha256("\n".join(guard_block).encode()).hexdigest(),
        "no_rawlsing_next_f6p_terms": all(not row["rawlsing_next_matches"] for row in result.values()),
        "successor_elsewhere_claim": "NOT_MADE; this scan is only the exact tree and does not search unmerged branches or untracked worktrees.",
    }


def f6c_receiver_check() -> dict:
    """Read the pinned historical F6C outputs to test the candidate's claim.

    The copied substitution receipt names these outputs but does not embed
    them.  Reading the pinned historical commit is necessary for the claim.
    """
    f6c = "c1ebe091fa2bd12b254e5599cf37975fe438d462"
    base = "WORKER_RETURNS/PYAT-R35-F6C-NATIVE-COMPARATIVE-R1/consumer_runs"
    receipt_path = f"{base}/wp2_consumer_substitution_receipt.json"
    receipt = json.loads(run_git("show", f"{f6c}:{receipt_path}"))
    outputs = {}
    for key in ("B", "A", "A0"):
        raw = run_git("show", f"{f6c}:{base}/wp2_sub_{key}.json")
        document = json.loads(raw)
        generic = deepcopy(document["generic_read_only_input"])
        sidecars = generic.pop("f6_sidecars")
        outputs[key] = {
            "sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "bytes": len(raw.encode()),
            "nonparent_consumer_sha256": stable_hash(generic["nonparent_consumer"]),
            "generic_without_f6_sidecars_sha256": stable_hash(generic),
            "actual_c1_returns_sha256": stable_hash(document["actual_C1_returns"]),
            "cases_sha256": stable_hash(document["cases"]),
            "f6_sidecars_sha256": stable_hash(sidecars),
        }
    keys = ("B", "A", "A0")
    return {
        "commit": f6c,
        "receipt_path": receipt_path,
        "receipt_sha256": hashlib.sha256(
            json.dumps(receipt, sort_keys=True).encode()).hexdigest(),
        "receipt_contains_output_bodies": False,
        "receipt_names_output_paths": all(
            receipt["runs"][key]["output"].endswith(f"wp2_sub_{key}.json") for key in keys),
        "outputs": outputs,
        "nonparent_consumer_invariant": len({
            outputs[key]["nonparent_consumer_sha256"] for key in keys}) == 1,
        "generic_without_f6_sidecars_invariant": len({
            outputs[key]["generic_without_f6_sidecars_sha256"] for key in keys}) == 1,
        "actual_c1_returns_invariant": len({
            outputs[key]["actual_c1_returns_sha256"] for key in keys}) == 1,
        "cases_invariant": len({
            outputs[key]["cases_sha256"] for key in keys}) == 1,
        "f6_sidecars_differ_by_method_variant": len({
            outputs[key]["f6_sidecars_sha256"] for key in keys}) > 1,
        "wp2_code_edited": receipt["wp2_code_edited"],
        "wp2_blob": receipt["wp2_repro_wp2_py_blob"],
    }


def pin_check() -> dict:
    f6p_src = F6P / "f6p_partial_bound_evidence_consumer.py"
    f6p_reviewed_src = F6P_REVIEWED / "f6p_partial_bound_evidence_consumer.py"
    f6m_src = F6P / "native/rawlsing_next/pre553_heterogeneous_synthesis.py"
    a_src = F6P / "native/rawlsing_next/pre553_heterogeneous_synthesis_A.py"
    a0_src = F6P / "native/rawlsing_next/pre553_heterogeneous_synthesis_A0.py"
    wp2_src = CAND / "stage/wp2/wp2.py"
    independent_test = CAND / "stage/reviewer_root/evidence/court_b/test_court_b_f6p_independent.py"
    expected = {
        "f6p_consumer_blob": "8fa992899293f454d7abded36831a4b4a362df8e",
        "f6p_consumer_sha256": "0bf56dd2f073691575a03f57b02c4a3784400174ace72bddfdfb92b883b82c87",
        "f6m_candidate_blob": "2df811d76db258d98d89ffb43c830cb221ff9a7d",
        "f6m_candidate_sha256": "2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871",
        "f6m_corrected_A_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
        "f6m_A0_blob": "182cc7970d7624f6614015f5a51d0602e1630d52",
        "wp2_blob": "55e567e4d0780c251bf949268d3d477abdc76a9b",
        "wp2_sha256": "185f4b8ae5b5526fefb25d3cbef609b1b3d155561adf0d73655bb7fc46264015",
        "independent_test_blob": "3b42b05e7d1de6a1046c22e532dc77827cb2f9c6",
        "independent_test_sha256": "ccefcd47412068ff127fbd2820da2e3986864f381508aa0fdbf4cbaf9691e451",
    }
    actual = {
        "f6p_consumer_blob": blob(f6p_src),
        "f6p_consumer_sha256": sha256(f6p_src),
        "f6m_candidate_blob": blob(f6m_src),
        "f6m_candidate_sha256": sha256(f6m_src),
        "f6m_corrected_A_blob": blob(a_src),
        "f6m_A0_blob": blob(a0_src),
        "wp2_blob": blob(wp2_src),
        "wp2_sha256": sha256(wp2_src),
        "independent_test_blob": blob(independent_test),
        "independent_test_sha256": sha256(independent_test),
    }
    assert actual == expected, (actual, expected)
    assert blob(f6p_reviewed_src) == expected["f6p_consumer_blob"]
    return {
        "candidate_head": SHA,
        "startup_sha": STARTUP,
        "expected": expected,
        "actual": actual,
        "all_pins_match": True,
        "f6p_reviewed_consumer_same_blob": True,
        "candidate_commit_scope": run_git("show", "--format=", "--name-only", SHA).splitlines(),
        "comparison_evidence_sha256": sha256(CAND / "evidence/f6p-receiver-comparison.json"),
        "run0_sha256": sha256(CAND / "evidence/run-comparison.seed0.json"),
        "run1_sha256": sha256(CAND / "evidence/run-comparison.seed1.json"),
        "run0_equals_run1": (CAND / "evidence/run-comparison.seed0.json").read_bytes()
                            == (CAND / "evidence/run-comparison.seed1.json").read_bytes(),
    }


def main() -> int:
    oracle = json.loads((F6P / "oracle/01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json").read_text())
    pins = pin_check()
    replays = {world: check_world(world, oracle) for world in WORLDS}

    # Candidate evidence is read-only; compare semantic summary fields after
    # normalizing the path-dependent F6M module_file/output_hash.
    cand_evidence = json.loads((CAND / "evidence/f6p-receiver-comparison.json").read_text())
    summary_matches = {}
    for world in WORLDS:
        ours = replays[world]["summary"]
        theirs = cand_evidence["results"][world]
        ours_cmp = {k: v for k, v in ours.items() if k in SUMMARY_FIELDS and k != "output_hash"}
        theirs_cmp = {k: v for k, v in theirs.items() if k in SUMMARY_FIELDS and k != "output_hash"}
        ours_cmp["source_product"] = dict(ours_cmp["source_product"])
        theirs_cmp["source_product"] = dict(theirs_cmp["source_product"])
        ours_cmp["source_product"].pop("module_file", None)
        theirs_cmp["source_product"].pop("module_file", None)
        summary_matches[world] = {
            "semantic_summary_equal": ours_cmp == theirs_cmp,
            "candidate_output_hash": theirs.get("output_hash"),
            "review_output_hash": ours.get("output_hash"),
            "output_hash_equal": ours.get("output_hash") == theirs.get("output_hash"),
            "path_only_difference": ours_cmp == theirs_cmp and ours.get("output_hash") != theirs.get("output_hash"),
        }
        assert summary_matches[world]["semantic_summary_equal"], world

    wp2_text = (CAND / "stage/wp2/wp2.py").read_text()
    wp2_line = wp2_text.splitlines()[93]
    f6p_text = (F6P / "f6p_partial_bound_evidence_consumer.py").read_text()
    comparison_text = (CAND / "run_comparison.py").read_text()
    authored_label = "F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR"
    f6p_w2 = build("B", "W2_mixed_eligibility_trap")
    f6p_result = C.consume_f6m_evidence(f6p_w2, request("W2_mixed_eligibility_trap"))
    try:
        sidecar(f6p_result)
    except Exception as exc:  # exact boundary observation, not an authored type
        raw = {
            "exception_type": type(exc).__name__,
            "exception_args": list(exc.args),
            "exception_str": str(exc),
            "is_key_error_native_bundle": isinstance(exc, KeyError) and exc.args == ("native_bundle",),
            "first_missing_field": (
                "native_bundle" if "native_bundle" not in f6p_result
                else "native_conditional_consumer" if "native_conditional_consumer" not in f6p_result
                else None),
            "f6p_supplies_native_bundle": "native_bundle" in f6p_result,
            "f6p_supplies_native_conditional_consumer": "native_conditional_consumer" in f6p_result,
        }
    else:
        raise AssertionError("F6P unexpectedly supplied the WP2 F6M native sidecar")
    assert raw["is_key_error_native_bundle"]
    assert raw["first_missing_field"] == "native_bundle"
    assert authored_label not in f6p_text
    assert authored_label not in wp2_text
    assert authored_label in comparison_text
    authored_line = next(i for i, line in enumerate(comparison_text.splitlines(), 1)
                         if authored_label in line)
    boundary = {
        "receiver_pin": {
            "path": "WORKER_RETURNS/PDEV01-F6-COMPARISON/stage/wp2/wp2.py",
            "blob": pins["actual"]["wp2_blob"],
            "line": 94,
            "exact_line": wp2_line,
        },
        "raw_observation": raw,
        "authored_diagnostic": {
            "code": authored_label,
            "emitted_by_wp2": authored_label in wp2_text,
            "emitted_by_f6p": authored_label in f6p_text,
            "authored_in_candidate_run_comparison": True,
            "candidate_line": authored_line,
            "classification": "COMPARISON_LOCAL_LABEL_NOT_RECEIVER_TYPED_REFUSAL",
        },
        "read_effect": {
            "candidate_claim": "NO_NONPARENT_OPTIONS_READ; NO_F6M_E04_JOIN",
            "observed": "KeyError raised by applying the pinned WP2 expression to an F6P result; no WP2 product read occurred in this check.",
            "classification": "AUTHORED_STRUCTURAL_INFERENCE",
        },
    }

    f6c = f6c_receiver_check()
    assert f6c["nonparent_consumer_invariant"]
    assert f6c["generic_without_f6_sidecars_invariant"]
    assert f6c["actual_c1_returns_invariant"]
    assert f6c["cases_invariant"]
    assert f6c["f6_sidecars_differ_by_method_variant"]
    assert f6c["wp2_code_edited"] is False

    scope = scan(SHA)
    assert scope["no_rawlsing_next_f6p_terms"], scope["terms"]
    assert scope["wp2_is_candidate_stage_only"]
    assert not scope["n9_f6_schema_reference"]
    assert not scope["n9_f6_import_reference"]
    assert scope["guard_returns_guard_only"]
    assert not scope["guard_has_f6_schema"]

    report = {
        "schema": "PDEV01_F6_INDEPENDENT_REVIEW_EVIDENCE@1.0.0",
        "candidate_head": SHA,
        "reviewer_role": "distinct independent reviewer; sourcefree TEST_ONLY; no issuer/adopter",
        "pins": pins,
        "oracle_path": str((F6P / "oracle/01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json").relative_to(CAND)),
        "replay": replays,
        "candidate_summary_comparison": summary_matches,
        "wp2_boundary": boundary,
        "f6c_historical_receiver_outputs": f6c,
        "scope_scan": scope,
        "verdict_inputs": {
            "actual_semantics_reproduced": True,
            "bounds_present_and_rational": True,
            "uncovered_mass_and_point_refusal_verified": True,
            "wp2_shape_mismatch_verified": True,
            "wp2_raw_exception_is_key_error": True,
            "authored_label_is_not_a_receiver_type": True,
            "candidate_output_hash_is_root_sensitive": any(
                row["path_only_difference"] for row in summary_matches.values()),
            "current_tree_has_no_f6p_receiver": True,
            "successor_elsewhere_not_assumed": True,
            "f6c_receiver_invariance_supported_by_pinned_historical_outputs": True,
            "f6c_receipt_alone_does_not_embed_outputs": True,
        },
        "limits": [
            "No original SAV/DTA, original respondents, weights, population, transport or model-use grant.",
            "F6M/F6P are sourcefree TEST_ONLY artifacts; this review does not adopt them.",
            "The exact-tree scan is not proof of absence in unmerged branches or untracked worktrees.",
            "The WP2 expression is a structural boundary check, not a full WP2 execution.",
        ],
    }
    (REVIEW / "evidence/replay_f6_review.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    (REVIEW / "evidence/wp2_boundary_review.json").write_text(
        json.dumps(boundary, indent=2, sort_keys=True) + "\n")
    (REVIEW / "evidence/scope_scan_review.json").write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "candidate": SHA,
        "all_pins_match": pins["all_pins_match"],
        "worlds": {w: {
            "state": replays[w]["summary"]["evidence_state"],
            "uncovered": replays[w]["summary"]["uncovered_target_mass"],
            "point": replays[w]["summary"]["supported_point"],
            "bounds": len(replays[w]["summary"]["bounds"]),
        } for w in WORLDS},
        "wp2_raw": raw,
        "authored_label": authored_label,
        "authored_line": authored_line,
        "scope_no_rawlsing_next_terms": scope["no_rawlsing_next_f6p_terms"],
        "wp2_candidate_stage_only": scope["wp2_is_candidate_stage_only"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
