"""F6L Phase-A preregistered decision/admission/evidence attacks.

These expectations were frozen in 01_WORLDS_AND_EXACT_EXPECTATIONS.json before
the F6K return was examined.  Tests encode the SAFE expectation; where the
unrepaired candidate is unsafe they are expected to fail, and the failures are
evidence, not permission to edit the expectation.

Native under test: producer blob fc5e37fa5b2f0eb689593b42d95479d1327cb94c.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(RET / "01_STAGED_NATIVE"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))
sys.path.insert(0, str(RET / "01_SOURCE_TRANSPORT/F6C_AUTHOR"))

from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, complementary_binary_bounds, SynthesisError, METHOD)
import rawlsing_next.pre553_heterogeneous_synthesis as PRODUCER  # noqa: E402
import f6l_worlds as W  # noqa: E402
import f6c_worlds  # noqa: E402

PREREG = json.loads((RET / "02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json").read_text())
WORLDS = {w["case"]: w for w in PREREG["worlds"]}
# Cases that attack a shared world rather than introducing a new table set.
CASE_WORLD = {
    "P4_FORGED_REAL_SOURCE_ADMIT_TRUE": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P5_TEST_ORIGIN_BYPASS": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P5B_MIXED_ORIGIN_CONTAMINATION": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P6_MISSING_OWNER_FAIL_CLOSED": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P7_MAPPED_NODE_AUTHORITY_CEILING": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P9_STATUS_VS_ACTUAL_DISTRIBUTION": "P2_NOVEL_2X2_NO_POSITIVITY",
}

COMPLETE_TOKENS = {"SYNTHETIC_CANDIDATE"}
SAFE_INCOMPLETE_MARKERS = ("PARTIAL", "NO_COMPLETE", "INCOMPLETE", "BACKOFF", "UNIDENTIFIED")
REAL_USE = "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE"


def fkey(text):
    return ast.literal_eval(text)


def exp_map(entry, field):
    return {fkey(k): F(v) for k, v in entry["exact_expectations"][field].items()}


def cells(cell_list):
    return {tuple(c["categories"]): F(c["probability"]) for c in cell_list}


def bounds(candidate):
    return {tuple(b["categories"]): (F(b["lower"]), F(b["upper"]))
            for b in candidate["uncertainty"]["source_disagreement_and_uncovered_bounds"]}


def run_case(case, *, test_origin=None, admit=lambda *_: True, calls=None,
             min_raw_support=None):
    entry = WORLDS[CASE_WORLD.get(case, case)]
    target = copy.deepcopy(entry["target"])
    sources = copy.deepcopy(entry["sources"])
    policy = copy.deepcopy(entry["policy"])
    if test_origin is not None:
        for src in sources:
            src["test_origin"] = bool(test_origin)
    if min_raw_support is not None:
        policy["minimum_raw_support"] = int(min_raw_support)
    if calls is not None:
        def callback(*args):
            calls.append({"source_id": args[0].get("source_id"),
                          "phase": args[2]})
            return True
        admit = callback
    return synthesize(target, sources, policy, admit=admit)


def decision_is_partial(decision):
    return (decision not in COMPLETE_TOKENS
            and any(marker in decision for marker in SAFE_INCOMPLETE_MARKERS))


def node_rank(ceiling):
    order = {
        "UNVERIFIED": 0,
        "TEST_ONLY": 1,
        "DESCRIPTIVE_SOCIOLOGICAL_MODEL_ONLY": 2,
        "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE": 3,
    }
    return order.get(ceiling, -1)


# ===========================================================================
# Custody / method identity
# ===========================================================================
def test_native_producer_is_the_pinned_corrected_s03fo_blob():
    raw = Path(PRODUCER.__file__).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"
    assert METHOD == "PRE553_TARGET_JOINT_STANDARDIZATION@1"


# ===========================================================================
# P1: original F6C uncovered-mass world
# ===========================================================================
def test_p1_original_world_arithmetic_and_widened_bounds_are_preserved():
    out = run_case("P1_ORIGINAL_UNCOVERED_WORLD")
    cand = out["candidate"]
    assert cand["distribution"] is None
    assert cells(cand["covered_subprobability"]) == exp_map(
        WORLDS["P1_ORIGINAL_UNCOVERED_WORLD"], "exact_joint_covered_subprobability")
    assert F(cand["uncovered_target_mass"]) == F(1, 5)
    b = bounds(cand)
    assert {k: v[1] for k, v in b.items()} == exp_map(
        WORLDS["P1_ORIGINAL_UNCOVERED_WORLD"], "exact_upper")
    assert {k: v[0] for k, v in b.items()} == exp_map(
        WORLDS["P1_ORIGINAL_UNCOVERED_WORLD"], "exact_lower")


def test_p1_original_world_does_not_assert_a_complete_candidate_when_null():
    out = run_case("P1_ORIGINAL_UNCOVERED_WORLD")
    assert out["candidate"]["distribution"] is None
    assert decision_is_partial(out["decision"]), (
        f"null distribution advertised as {out['decision']!r}")


# ===========================================================================
# P2/P3: novel 2x2 and 3-category no-positivity worlds
# ===========================================================================
@pytest.mark.parametrize("case", ["P2_NOVEL_2X2_NO_POSITIVITY",
                                  "P3_NOVEL_3_CATEGORY_NO_POSITIVITY"])
def test_novel_no_positivity_arithmetic_is_exact(case):
    out = run_case(case)
    cand = out["candidate"]
    assert cand["distribution"] is None
    assert cells(cand["covered_subprobability"]) == exp_map(
        WORLDS[case], "exact_joint_covered_subprobability")
    assert F(cand["uncovered_target_mass"]) == F(
        WORLDS[case]["exact_expectations"]["uncovered_target_mass"])
    b = bounds(cand)
    assert {k: v[1] for k, v in b.items()} == exp_map(WORLDS[case], "exact_upper")
    assert {k: v[0] for k, v in b.items()} == exp_map(WORLDS[case], "exact_lower")


@pytest.mark.parametrize("case", ["P2_NOVEL_2X2_NO_POSITIVITY",
                                  "P3_NOVEL_3_CATEGORY_NO_POSITIVITY"])
def test_novel_no_positivity_is_not_served_as_complete(case):
    out = run_case(case)
    assert out["candidate"]["distribution"] is None
    assert decision_is_partial(out["decision"]), (
        f"distribution=None but decision={out['decision']!r}")


@pytest.mark.parametrize("case", ["P2_NOVEL_2X2_NO_POSITIVITY",
                                  "P3_NOVEL_3_CATEGORY_NO_POSITIVITY"])
def test_novel_no_positivity_consumer_refuses_and_bounds_not_suppressed(case):
    out = run_case(case)
    cond = conditional(out, {out["candidate"]["construct_topology"][0]:
                             out["candidate"]["ordered_categories"][0][0]},
                       out["candidate"]["construct_topology"][1])
    assert cond["state"] == "UNAVAILABLE"
    assert cond["reason"] == "NO_COMPLETE_TARGET_JOINT"
    assert out["candidate"]["covered_subprobability"]
    assert out["candidate"]["uncertainty"]["source_disagreement_and_uncovered_bounds"]


# ===========================================================================
# P4: forged real-source admit=True
# ===========================================================================
def test_p4_unverified_admit_true_cannot_issue_real_source_authority():
    calls = []
    out = run_case("P4_FORGED_REAL_SOURCE_ADMIT_TRUE", test_origin=False, calls=calls)
    assert out["candidate"] is not None
    assert len(calls) == 4
    assert {c["phase"] for c in calls} == {
        "SOURCE_INDEXED_BASELINE", "TARGET_JOINT_STANDARDIZATION"}
    ceilings = [n.get("authority_ceiling") for n in out["evidence_graph"]]
    assert REAL_USE not in ceilings, (
        "a caller-controlled boolean produced EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE")
    status = out.get("owner_admission_status") or out.get("real_source_qualification")
    assert status != "VERIFIED", (
        "owner boundary must remain explicitly unverified, not implicitly issued")


def test_p4_admission_callback_is_not_identity_authentication():
    """The callback receives no token/permission object; it is a pluggable seam."""
    seen = []

    def probe(source, target, phase):
        seen.append((tuple(sorted(source)), tuple(sorted(target)), phase))
        return True

    run_case("P4_FORGED_REAL_SOURCE_ADMIT_TRUE", test_origin=False, admit=probe)
    assert len(seen) == 4
    for source_keys, target_keys, phase in seen:
        assert "permission" not in source_keys
        assert "owner_token" not in source_keys
        assert phase in ("SOURCE_INDEXED_BASELINE", "TARGET_JOINT_STANDARDIZATION")


# ===========================================================================
# P5/P5B: caller-declared test_origin bypass and mixed-origin contamination
# ===========================================================================
def test_p5_test_origin_true_bypasses_admission_entirely():
    calls = []
    out = run_case("P5_TEST_ORIGIN_BYPASS", test_origin=True, calls=calls)
    assert out["test_origin"] is True
    assert calls == []
    assert out["candidate"] is not None


def test_p5_test_origin_output_never_claims_real_source_authority():
    out = run_case("P5_TEST_ORIGIN_BYPASS", test_origin=True)
    ceilings = [n.get("authority_ceiling") for n in out["evidence_graph"]]
    assert out["test_origin"] is True
    assert REAL_USE not in ceilings, (
        "test-only data advertised with real-use authority")


def test_p5b_mixed_origin_does_not_launder_an_unverified_source_into_real_output():
    calls = []
    entry = WORLDS["P5B_MIXED_ORIGIN_CONTAMINATION"]
    target = copy.deepcopy(entry["target"])
    sources = copy.deepcopy(entry["sources"])
    sources[0]["test_origin"] = False   # real, admitted below
    sources[1]["test_origin"] = True    # caller-declared test, skips admission
    policy = copy.deepcopy(entry["policy"])

    def callback(source, tgt, phase):
        calls.append(source["source_id"])
        return True

    out = synthesize(target, sources, policy, admit=callback)
    assert out["test_origin"] is False
    assert out["candidate"] is not None
    assert set(calls) == {"S1"}, "declared-test source must not be the only admitted source"
    ceilings = [n.get("authority_ceiling") for n in out["evidence_graph"]]
    assert REAL_USE not in ceilings, (
        "mixed real/test output issued real-use authority while an unverified "
        "source was silently included")


# ===========================================================================
# P6: missing owner fail-closed (preserved)
# ===========================================================================
def test_p6_missing_owner_refuses_real_source():
    with pytest.raises(SynthesisError):
        run_case("P6_MISSING_OWNER_FAIL_CLOSED", test_origin=False, admit=None)


def test_p6_false_admission_refuses_real_source():
    with pytest.raises(SynthesisError):
        run_case("P6_MISSING_OWNER_FAIL_CLOSED", test_origin=False,
                 admit=lambda *_: False)


# ===========================================================================
# P7: mapped-node authority and hierarchy
# ===========================================================================
def test_p7_every_evidence_node_has_authority_ceiling_and_provenance():
    out = run_case("P7_MAPPED_NODE_AUTHORITY_CEILING", test_origin=True)
    for node in out["evidence_graph"]:
        assert "authority_ceiling" in node, f"{node['node_id']} lacks authority_ceiling"
        assert "parents" in node
        if node["node_id"].startswith("mapped:"):
            assert node.get("mapping_hash"), f"{node['node_id']} lacks mapping_hash"
            assert node.get("value_hash") or node.get("value_ref")


def test_p7_no_node_exceeds_its_native_parent_authority():
    out = run_case("P7_MAPPED_NODE_AUTHORITY_CEILING", test_origin=True)
    by_id = {n["node_id"]: n for n in out["evidence_graph"]}
    for node in out["evidence_graph"]:
        if node["node_id"].startswith("mapped:"):
            parent = by_id[node["parents"][0]]
            assert node_rank(node.get("authority_ceiling")) <= node_rank(
                parent.get("authority_ceiling"))
    target = by_id["target_joint"]
    for parent_id in target["parents"]:
        assert node_rank(target["authority_ceiling"]) <= node_rank(
            by_id[parent_id]["authority_ceiling"])


def test_p7_test_only_graph_has_no_real_use_ceiling():
    out = run_case("P7_MAPPED_NODE_AUTHORITY_CEILING", test_origin=True)
    assert out["test_origin"] is True
    assert all(n.get("authority_ceiling") != REAL_USE for n in out["evidence_graph"])


# ===========================================================================
# P8: distributed support / minority cutoff / silent renormalization
# ===========================================================================
def test_p8_minimum_raw_support_does_not_protect_a_minority_cell():
    a = run_case("P8_DISTRIBUTED_SUPPORT_MIN_1", min_raw_support=1)
    b = run_case("P8_DISTRIBUTED_SUPPORT_MIN_5_CELL_NOT_GATE", min_raw_support=5)
    assert cells(a["candidate"]["distribution"]) == cells(b["candidate"]["distribution"])
    assert F(cells(a["candidate"]["distribution"])[("LOW", "NO")]) == F(7, 50)
    assert [s["source_id"] for s in b["candidate"]["support"]["Z1"]["sources"]] == ["S1", "S2"]


def test_p8_source_exclusion_must_not_be_silent_complete_renormalization():
    out = run_case("P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED",
                   min_raw_support=150)
    support = out["candidate"]["support"]["Z1"]
    assert support["excluded_sources"] == ["S1"]
    assert [s["source_id"] for s in support["sources"]] == ["S2"]
    distribution_is_full = (out["candidate"]["distribution"] is not None
                            and F(out["candidate"]["uncovered_target_mass"]) == 0)
    assert not distribution_is_full, (
        "excluded source's target mass was renormalized away and the result "
        "still advertised as a complete target joint")
    cond = conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")
    assert cond.get("state") != "SUPPORTED_MODEL", (
        "consumer served a complete conditional from a renormalized, "
        "source-excluded estimate")


# ===========================================================================
# P9: status vs actual distribution consumer view
# ===========================================================================
def test_p9_decision_only_consumer_cannot_consume_null_as_complete():
    out = run_case("P9_STATUS_VS_ACTUAL_DISTRIBUTION")

    def decision_only_consumer(bundle):
        if bundle["decision"] in COMPLETE_TOKENS:
            return "CONSUMED_AS_COMPLETE"
        return "REFUSED"

    assert out["candidate"]["distribution"] is None
    assert decision_only_consumer(out) == "REFUSED"
    assert decision_is_partial(out["decision"])


# ===========================================================================
# P10/P11: arithmetic substitution and genuine complete positive
# ===========================================================================
def test_p10_source_substitution_moves_exact_joint_to_recomputed_value():
    out = run_case("P10_ARITHMETIC_SOURCE_SUBSTITUTION")
    assert cells(out["candidate"]["distribution"]) == exp_map(
        WORLDS["P10_ARITHMETIC_SOURCE_SUBSTITUTION"], "exact_joint_covered_subprobability")
    pos = run_case("P11_GENUINE_COMPLETE_TARGET_POSITIVE")
    assert cells(out["candidate"]["distribution"]) != cells(pos["candidate"]["distribution"])


def test_p11_complete_positive_remains_exact_and_usable():
    out = run_case("P11_GENUINE_COMPLETE_TARGET_POSITIVE")
    cand = out["candidate"]
    assert cand["distribution"] is not None
    assert F(cand["uncovered_target_mass"]) == 0
    assert cells(cand["distribution"]) == exp_map(
        WORLDS["P11_GENUINE_COMPLETE_TARGET_POSITIVE"], "exact_joint_covered_subprobability")
    assert sum(cells(cand["distribution"]).values(), F(0)) == 1
    b = bounds(cand)
    assert {k: v[0] for k, v in b.items()} == exp_map(
        WORLDS["P11_GENUINE_COMPLETE_TARGET_POSITIVE"], "exact_lower")
    assert {k: v[1] for k, v in b.items()} == exp_map(
        WORLDS["P11_GENUINE_COMPLETE_TARGET_POSITIVE"], "exact_upper")
    cond = conditional(out, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")
    assert cond["state"] == "SUPPORTED_MODEL"
    assert F(cond["probabilities"]["YES"]) == F(1, 3)
    assert F(cond["model_denominator_mass"]) == F(1, 2)
    assert cond["uncertainty"] == "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED"
    assert out["decision"] in COMPLETE_TOKENS


def test_p11_complete_positive_does_not_invent_variance_or_confidence_interval():
    out = run_case("P11_GENUINE_COMPLETE_TARGET_POSITIVE")
    unc = out["candidate"]["uncertainty"]
    assert unc["sampling_variance"] is None
    assert unc["sampling_status"] == "UNKNOWN_DESIGN"
    assert "not confidence intervals" in unc["limitations"]
    assert "coverage" not in json.dumps(unc).lower()


# ===========================================================================
# Preserved F6J rational results (independently re-executed, not copied)
# ===========================================================================
def test_preserved_frechet_bounds_are_not_a_person_and_not_a_measured_joint():
    fr = complementary_binary_bounds("2/5", "2/5")
    assert fr["dependence"] == "UNIDENTIFIED"
    assert fr["scenario_is_measured"] is False
    assert F(fr["lower"]) == 0
    assert F(fr["upper"]) == F(2, 5)
    assert F(fr["independence_scenario"]) == F(4, 25)
